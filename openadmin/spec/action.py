# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class ActionComponent(TypedDict):
    type: Literal["action"]
    id: str
    name: str
    description: str | None
    icon: Icon | None
    color: Color | None
    method: HttpMethod
    is_hidden: bool
    form: NotRequired[list[Property] | None]
    body: NotRequired[list[Property] | None]
    query: NotRequired[list[Property] | None]


class ActionResponse(TypedDict):
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    toast: NotRequired[str]
    table: NotRequired[dict | object]
    message: NotRequired[str]


type Action = ActionResponse | None | str
