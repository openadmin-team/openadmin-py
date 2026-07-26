# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass, field

from openadmin import spec


@dataclass
class Markdown:
    function_name: str
    id: str
    name: str
    description: str | None
    icon: spec.Icon | None
    color: spec.Color | None
    method: spec.HttpMethod
    func: Callable | None = field(default=None)
