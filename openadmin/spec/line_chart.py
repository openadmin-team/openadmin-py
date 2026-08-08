# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, TypedDict

from .http_methods import HttpMethod
from .json_schema import JsonSchema


class LineChartComponent(TypedDict):
    type: Literal["line-chart"]
    id: str
    name: str
    description: str | None
    method: HttpMethod
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


type LineChart = LineChartComponent
