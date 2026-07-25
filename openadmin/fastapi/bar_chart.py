# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass, field

from openadmin import spec


@dataclass
class BarChart:
    function_name: str
    id: str
    name: str
    description: str | None
    config: dict[str, spec.BarChartConfigValue] | None
    data_key: str | None
    icon: spec.Icon | None
    color: spec.Color | None
    caption: str | None
    caption_description: str | None
    caption_icon: spec.Icon | None
    method: spec.HttpMethod
    func: Callable | None = field(default=None)
