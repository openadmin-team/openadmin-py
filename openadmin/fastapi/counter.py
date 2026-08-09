# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


__state: dict[str, int] = {}


def inc(
    key: str,
) -> int:
    """Increment the counter for the given key and return the new value."""

    if key not in __state:
        __state[key] = 0
    else:
        __state[key] += 1

    return __state[key]
