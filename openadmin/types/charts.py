# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class AreaChart(BaseModel):
    data: List[Dict[str, int | float | str]] = Field(default=[])
    config: Dict[str, Dict[Literal["label", "color"], str]]


class BarChart(BaseModel):
    data: List[Dict[str, int | float | str]] = Field(default=[])
    config: Dict[str, Dict[Literal["label", "color"], str]]


class LineChart(BaseModel):
    data: List[Dict[str, int | float | str]] = Field(default=[])
    config: Dict[Literal["views", "str"] | str, Dict[Literal["label", "color"], str]]


class PieChart(BaseModel):
    data: List[Dict[str, int | float | str]] = Field(default=[])
    config: Dict[str, Dict[Literal["label", "color"], str]]
