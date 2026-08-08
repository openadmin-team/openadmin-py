# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from openadmin import spec


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    admin_exc: spec.Error = {
        "message": exc.detail,
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=admin_exc,
    )


async def app_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    admin_exc: spec.Error = {
        "message": str(exc),
    }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=admin_exc,
    )
