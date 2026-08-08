# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .json_schema import JsonSchema


class FieldConfig(TypedDict):
    reference: NotRequired[str | None]
    reference_field: NotRequired[str]
    icon: NotRequired[Icon]
    color: NotRequired[Color]


class FormComponent(TypedDict):
    type: Literal["form"]
    id: str
    name: str
    description: str | None
    fields: dict[str, FieldConfig] | None
    icon: Icon | None
    color: Color | None
    method: HttpMethod
    is_hidden: bool
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


class FormResponse(TypedDict):
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    toast: NotRequired[str]
    table: NotRequired[dict | object]
    message: NotRequired[str]


type Form = FormResponse | None | str
