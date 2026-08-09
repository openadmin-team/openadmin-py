# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any, TypedDict, Union

JsonSchema = TypedDict(
    "JsonSchema",
    {
        # --- meta / referencing ---
        "$schema": str,
        "$ref": str,
        "$defs": dict[str, "JsonSchema"],
        "definitions": dict[str, "JsonSchema"],
        "title": str,
        "description": str,
        # --- core typing ---
        "type": str | list[str],
        "enum": list[Any],
        "const": Any,
        "default": Any,
        "format": str,
        # --- object ---
        "properties": dict[str, "JsonSchema"],
        "required": list[str],
        "additionalProperties": Union[bool, "JsonSchema"],
        # --- array ---
        "items": Union["JsonSchema", list["JsonSchema"]],
        "prefixItems": list["JsonSchema"],
        "minItems": int,
        "maxItems": int,
        # --- string ---
        "minLength": int,
        "maxLength": int,
        "pattern": str,
        # --- number ---
        "minimum": int | float,
        "maximum": int | float,
        "exclusiveMinimum": int | float,
        "exclusiveMaximum": int | float,
        "multipleOf": int | float,
        # --- composition ---
        "anyOf": list["JsonSchema"],
        "oneOf": list["JsonSchema"],
        "allOf": list["JsonSchema"],
        "not": "JsonSchema",
    },
    total=False,
)
