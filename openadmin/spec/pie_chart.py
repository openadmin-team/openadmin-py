# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class PieChartConfigValue(TypedDict):
    name: NotRequired[str]
    color: NotRequired[Color]
    icon: NotRequired[Icon]


class PieChartComponent(TypedDict):
    type: Literal["pie-chart"]
    id: str
    name: str
    config: dict[str, PieChartConfigValue] | None
    icon: Icon | None
    name_key: str | None
    value_key: str | None
    color: Color | None
    description: str | None
    caption: str | None
    caption_description: str | None
    caption_icon: Icon | None
    url: str
    method: HttpMethod
    query: NotRequired[list[Property] | None]


type PieChartData = (
    list[dict[str, int | float | str]]
    | list[dict[Literal["name", "value"], int | float | str]]
    | object
)


class PieChartResponce(TypedDict):
    config: NotRequired[dict[str, PieChartConfigValue]]
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    data: PieChartData


type PieChart = PieChartData | PieChartResponce
