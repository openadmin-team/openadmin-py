# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import (
    NotRequired,
    TypedDict,
)

from sqlalchemy.sql import Select


class Stat(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    query: (
        Select[tuple[int]]
        | Select[tuple[str]]
        | Select[tuple[float]]
        | Select[tuple[bool]]
    )
