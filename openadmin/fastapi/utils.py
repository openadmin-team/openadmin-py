# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated, Any, cast

from pydantic import BaseModel, TypeAdapter, create_model

from fastapi import params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant
from openadmin import spec

from . import counter

_SPECIAL_CHARS_RE = re.compile(r"[^a-zA-Z0-9\s]")


def get_id(seed: str) -> str:
    """Generate a unique ID based on a seed string."""
    kebab_name = _SPECIAL_CHARS_RE.sub("", seed).lower().replace(" ", "-")
    count = counter.inc(kebab_name)
    return kebab_name + (f"-{count}" if count != 0 else "")


def get_query_params(func: Callable) -> spec.JsonSchema | None:
    dependant = _get_flat_dependant(func)
    return _object_schema(dependant.query_params)


def get_form_params(func: Callable) -> spec.JsonSchema | None:
    dependant = _get_flat_dependant(func)
    fields = [field for field in dependant.body_params if _is_form_field(field)]
    return _unwrappable_schema(fields)


def get_body_params(func: Callable) -> spec.JsonSchema | None:
    dependant = _get_flat_dependant(func)
    fields = [field for field in dependant.body_params if _is_body_field(field)]
    return _unwrappable_schema(fields)


@dataclass
class _FlatParams:
    """Params pulled from a `Dependant` and all of its sub-dependencies.

    FastAPI's own flattening helper (`get_flat_dependant`) has been renamed
    or removed across versions, so it isn't relied on here -- this walks the
    dependency tree the same way it used to, using only `Dependant.call`,
    `.dependencies`, `.query_params` and `.body_params`, which have stayed
    stable across FastAPI versions.
    """

    query_params: list[Any]
    body_params: list[Any]


def _get_flat_dependant(func: Callable) -> _FlatParams:
    """Resolve `func`'s params the same way FastAPI does, including params
    pulled in through `Depends(...)` (e.g. `PageDep`, `SearchQueryDep`)."""
    dependant = get_dependant(path="", call=func)
    return _flatten_params(dependant)


def _flatten_params(
    dependant: Dependant, visited: set[Callable | None] | None = None
) -> _FlatParams:
    if visited is None:
        visited = set()
    visited.add(dependant.call)

    flat = _FlatParams(
        query_params=list(dependant.query_params),
        body_params=list(dependant.body_params),
    )
    for sub_dependant in dependant.dependencies:
        if sub_dependant.call in visited:
            continue
        flat_sub = _flatten_params(sub_dependant, visited)
        flat.query_params.extend(flat_sub.query_params)
        flat.body_params.extend(flat_sub.body_params)
    return flat


def _is_form_field(field: Any) -> bool:
    return isinstance(field.field_info, params.Form)


def _is_body_field(field: Any) -> bool:
    return isinstance(field.field_info, params.Body) and not isinstance(
        field.field_info, params.Form
    )


def _should_embed(fields: list[Any]) -> bool:
    """Mirror FastAPI's own rule for when a body/form is wrapped under its
    param name vs. used as-is (e.g. a lone `Body(...)` pydantic model is the
    whole body; two body params, or an explicit `embed=True`, are nested)."""
    if not fields:
        return False

    if len(fields) > 1:
        return True

    field_info = fields[0].field_info
    if getattr(field_info, "embed", None):
        return True

    annotation = field_info.annotation
    return isinstance(field_info, params.Form) and not (
        isinstance(annotation, type) and issubclass(annotation, BaseModel)
    )


def _object_schema(fields: list[Any]) -> spec.JsonSchema | None:
    if not fields:
        return None

    field_definitions: dict[str, Any] = {
        field.alias: (field.field_info.annotation, field.field_info) for field in fields
    }
    model = create_model("Schema", **field_definitions)  # type: ignore[call-overload]
    return cast(spec.JsonSchema, model.model_json_schema())


def _unwrappable_schema(fields: list[Any]) -> spec.JsonSchema | None:
    if not fields:
        return None

    if not _should_embed(fields):
        field = fields[0]
        annotation = Annotated[field.field_info.annotation, field.field_info]
        return cast(spec.JsonSchema, TypeAdapter(annotation).json_schema())

    return _object_schema(fields)
