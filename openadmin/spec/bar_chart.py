# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal

from pydantic import BaseModel, Field

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class BarChartComponent(BaseModel):
    type: Literal["bar-chart"]
    id: str
    name: str
    description: str | None
    icon: Icon | None
    color: Color | None
    caption: str | None
    caption_description: str | None
    caption_icon: Icon | None
    url: str
    method: HttpMethod
    query: list[Property] | None = Field(None)
