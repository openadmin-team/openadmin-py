# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal

type PropertyType = Literal[
    "integer",
    "string",
    "bool",
    "float",
    "object",
    "list",
    "list[integer]",
    "list[string]",
    "list[bool]",
    "list[float]",
]
