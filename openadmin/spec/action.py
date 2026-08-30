# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .json_schema import JsonSchema


class ActionComponent(TypedDict):
    type: Literal["action"]
    id: str
    name: str
    description: str | None
    icon: Icon | None
    color: Color | None
    method: HttpMethod
    is_hidden: bool
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


class ActionResponse(TypedDict):
    toast: NotRequired[str]
    clipboard: NotRequired[str]


type Action = ActionResponse | None | str
