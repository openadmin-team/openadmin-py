# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .error import Error
from .http_methods import HttpMethod
from .icons import Icon
from .json_schema import JsonSchema


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
    method: HttpMethod
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


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


type PieChart = PieChartData | PieChartResponce | Error
