# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re
from collections.abc import Callable
from typing import Annotated, Any, cast

from pydantic import BaseModel, TypeAdapter, create_model

from fastapi import params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant, get_flat_dependant
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


def _get_flat_dependant(func: Callable) -> Dependant:
    """Resolve `func`'s params the same way FastAPI does, including params
    pulled in through `Depends(...)` (e.g. `PageDep`, `SearchQueryDep`)."""
    dependant = get_dependant(path="", call=func)
    return get_flat_dependant(dependant, skip_repeats=True)


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
