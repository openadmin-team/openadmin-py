# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Awaitable, Callable
from typing import Annotated

from fastapi import Depends, Query, Request

from .req import PaginationParams


def pagination_params(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, description="Number of items per page"),
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)


def get_search_query(
    search: str | None = Query(None, min_length=1, description="Search query"),
) -> str | None:
    return search


def create_authenticate_dep(auth_func: Callable[[Request], None | Awaitable[None]], skip: list[str] | None = None,):
    def _(req: Request):

        if req.url.path in (skip or []):
            return

        auth_func(req)

    return Depends(_)


PageDep = Annotated[PaginationParams, Depends(pagination_params)]
SearchQueryDep = Annotated[str | None, Depends(get_search_query)]
