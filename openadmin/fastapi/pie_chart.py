# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Dict

from openadmin import spec


@dataclass
class PieChart:
    function_name: str
    id: str
    name: str
    config: Dict[str, spec.PieChartConfigValue] | None
    icon: spec.Icon | None
    name_key: str | None
    value_key: str | None
    color: spec.Color | None
    caption: str | None
    caption_description: str | None
    caption_icon: spec.Icon | None
    description: str | None
    method: spec.HttpMethod
    func: Callable | None = field(default=None)
