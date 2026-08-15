# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .json_schema import JsonSchema


class BarChartConfigValue(TypedDict):
    name: NotRequired[str]
    color: NotRequired[Color]
    icon: NotRequired[Icon]


class BarChartComponent(TypedDict):
    type: Literal["bar-chart"]
    id: str
    name: str
    description: str | None
    config: dict[str, BarChartConfigValue] | None
    data_key: str | None
    icon: Icon | None
    color: Color | None
    caption: str | None
    caption_description: str | None
    caption_icon: Icon | None
    refresh: int | None
    method: HttpMethod
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


type BarChartData = (
    list[dict[str, int | float | str]]
    | list[dict[Literal["data", "value"], int | float | str]]
    | object
)


class BarChartResponce(TypedDict):
    config: NotRequired[dict[str, BarChartConfigValue]]
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    refresh: NotRequired[int | None]
    data: BarChartData


type BarChart = BarChartData | BarChartResponce
