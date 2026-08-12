# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import HTTPException, Request, status

from openadmin.fastapi import AdminAuth, LoginReq

auth = AdminAuth()


@auth.login()
def login(req: Request, login: LoginReq) -> None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED login")


@auth.authenticate()
def authenticate(req: Request) -> None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED authenticate")
