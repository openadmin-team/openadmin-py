# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .http_methods import HttpMethod
from .property import Property


class AreaChart(TypedDict):
    type: Literal["area-chart"]
    id: str
    name: str
    description: str | None
    url: str
    method: HttpMethod
    query: NotRequired[list[Property] | None]
