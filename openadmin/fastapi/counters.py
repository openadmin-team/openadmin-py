# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal

__counters = {}


def get_next(key: Literal["page"]) -> int:
    if key not in __counters:
        __counters[key] = 1

    value = __counters[key]
    __counters[key] += 1

    return value
