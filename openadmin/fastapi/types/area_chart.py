# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass, field

from openadmin import spec


@dataclass
class AreaChart:
    function_name: str
    name: str
    description: str | None
    method: spec.HttpMethod
    func: Callable | None = field(default=None)
