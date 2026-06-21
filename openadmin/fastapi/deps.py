# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Annotated

from fastapi import Depends, Query

from .types import PaginationParams


def pagination_params(
    page: int = Query(default=0, ge=0, description="Page number"),
    per_page: int = Query(default=10, ge=1, description="Number of items per page"),
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)


PageDep = Annotated[PaginationParams, Depends(pagination_params)]
