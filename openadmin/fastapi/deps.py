# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Annotated

from fastapi import Depends, Query
from openadmin.types import CursorPaginationParams, PaginationParams, SortParams


def pagination_params(
    page: int = Query(default=0, ge=0, description="Page number"),
    per_page: int = Query(default=10, ge=1, description="Number of items per page"),
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)


def get_search_query(
    search: str | None = Query(None, min_length=1, description="Search query"),
) -> str | None:
    return search


def cursor_pagination_params(
    per_page: int = Query(default=10, ge=1, description="Number of items to return"),
    cursor: str | None = Query(None, description="Cursor for pagination"),
) -> CursorPaginationParams:
    return CursorPaginationParams(per_page=per_page, cursor=cursor)


PaginationParamsDep = Annotated[PaginationParams, Depends(pagination_params)]
CursorPaginationParamsDep = Annotated[
    CursorPaginationParams, Depends(cursor_pagination_params)
]
SearchQueryDep = Annotated[str | None, Depends(get_search_query)]
SortParamsDep = Annotated[SortParams, Query(..., description="Sort parameters")]
