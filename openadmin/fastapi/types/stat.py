# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass, field

from openadmin import spec


@dataclass
class Stat:
    function_name: str
    method: spec.HttpMethod
    name: str
    description: str | None
    func: Callable | None = field(default=None)
