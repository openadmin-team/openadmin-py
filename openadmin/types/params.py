# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from typing import Literal

from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int
    per_page: int


class CursorPaginationParams(BaseModel):
    cursor: str | None
    per_page: int


type SortParams = Literal["asc", "desc"]
