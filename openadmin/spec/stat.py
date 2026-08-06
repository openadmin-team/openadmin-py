# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class StatComponent(TypedDict):
    type: Literal["stat"]
    id: str
    icon: Icon | None
    color: Color | None
    name: str
    description: str | None
    url: str
    method: HttpMethod
    query: NotRequired[list[Property] | None]


type StatValue = str | int | float | bool | None


class StatResponse(TypedDict):
    value: StatValue
    icon: NotRequired[Icon]
    color: NotRequired[Color]


type Stat = StatValue | StatResponse
