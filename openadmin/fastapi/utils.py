# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import inspect
from typing import Annotated, get_args, get_origin, get_type_hints

import pydantic

from fastapi.params import Body as BodyParam
from fastapi.params import Form as FormParam
from fastapi.params import Query as QueryParam
from openadmin import spec

_SCALAR_LIST_TYPES: dict[type, spec.PropertyType] = {
    str: "list[string]",
    int: "list[integer]",
    float: "list[float]",
    bool: "list[bool]",
}


def _type_to_property_type(tp) -> spec.PropertyType:
    origin = get_origin(tp)
    if origin is list:
        inner = get_args(tp)
        if inner:
            scalar = _SCALAR_LIST_TYPES.get(inner[0])
            if scalar:
                return scalar
        return "list"
    if tp is str:
        return "string"
    if tp is int:
        return "integer"
    if tp is float:
        return "float"
    if tp is bool:
        return "bool"
    if isinstance(tp, type) and issubclass(tp, pydantic.BaseModel):
        return "object"
    return "string"


def _model_to_properties(model: type) -> list[spec.Property]:
    props = []
    for field_name, field_info in model.model_fields.items():
        tp = field_info.annotation
        prop_type = _type_to_property_type(tp)
        nested = None
        if (
            prop_type == "object"
            and isinstance(tp, type)
            and issubclass(tp, pydantic.BaseModel)
        ):
            nested = _model_to_properties(tp)
        elif prop_type == "list":
            inner = get_args(tp)
            if (
                inner
                and isinstance(inner[0], type)
                and issubclass(inner[0], pydantic.BaseModel)
            ):
                nested = _model_to_properties(inner[0])
        display = field_info.title or field_name.replace("_", " ").title()
        alias = field_info.alias or field_name
        props.append(
            spec.Property(
                name=display,
                alias=alias,
                type=prop_type,
                is_required=field_info.is_required(),
                properties=nested,
            )
        )
    return props


def _make_property(param_name: str, tp, marker) -> spec.Property:
    prop_type = _type_to_property_type(tp)
    nested = None
    if (
        prop_type == "object"
        and isinstance(tp, type)
        and issubclass(tp, pydantic.BaseModel)
    ):
        nested = _model_to_properties(tp)

    display = param_name.replace("_", " ").title()
    alias = param_name
    required = True

    if marker is not None:
        if marker.alias:
            alias = marker.alias
        if marker.title:
            display = marker.title
        required = marker.is_required()

    return spec.Property(
        name=display,
        alias=alias,
        type=prop_type,
        is_required=required,
        properties=nested,
    )


def extract_params(
    func,
) -> tuple[
    list[spec.Property] | None, list[spec.Property] | None, list[spec.Property] | None
]:
    """Return (query, body, form) properties extracted from a function's signature."""
    try:
        hints = get_type_hints(func, include_extras=True)
    except Exception:
        return None, None, None

    sig = inspect.signature(func)
    query: list[spec.Property] = []
    body: list[spec.Property] = []
    form: list[spec.Property] = []

    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue

        annotation = hints.get(param_name, inspect.Parameter.empty)
        default = param.default
        marker = None
        actual_type = annotation

        if get_origin(annotation) is Annotated:
            args = get_args(annotation)
            actual_type = args[0]
            for arg in args[1:]:
                if isinstance(arg, (QueryParam, BodyParam, FormParam)):
                    marker = arg
                    break

        if marker is None and isinstance(default, (QueryParam, BodyParam, FormParam)):
            marker = default

        # FormParam must be checked before BodyParam — Form is a subclass of Body
        if isinstance(marker, QueryParam):
            query.append(_make_property(param_name, actual_type, marker))
        elif isinstance(marker, FormParam):
            form.append(_make_property(param_name, actual_type, marker))
        elif isinstance(marker, BodyParam):
            if isinstance(actual_type, type) and issubclass(
                actual_type, pydantic.BaseModel
            ):
                body.extend(_model_to_properties(actual_type))
            else:
                body.append(_make_property(param_name, actual_type, marker))
        elif (
            annotation is not inspect.Parameter.empty
            and default is inspect.Parameter.empty
        ):
            # Unannotated Pydantic model with no default → implicit JSON body
            if isinstance(actual_type, type) and issubclass(
                actual_type, pydantic.BaseModel
            ):
                body.extend(_model_to_properties(actual_type))

    return query or None, body or None, form or None
