# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict, List, Literal, NotRequired, TypedDict

from pydantic import BaseModel, Field

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class PieChartConfigValue(TypedDict):
    label: NotRequired[str]
    color: NotRequired[Color]
    icon: NotRequired[Icon]


class PieChartComponent(BaseModel):
    type: Literal["pie-chart"]
    id: str
    name: str
    config: Dict[str, PieChartConfigValue] | None
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
    query: list[Property] | None = Field(None)


type PieChartData = List[Dict[str, int | float | str]] | object


class PieChartResponce(TypedDict):
    config: NotRequired[Dict[str, PieChartConfigValue]]
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    data: PieChartData


type PieChart = PieChartData | PieChartResponce
