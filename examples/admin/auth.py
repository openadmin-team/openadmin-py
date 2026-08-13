# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import HTTPException, Request, status

from openadmin.fastapi import AdminAuth, LoginReq

auth = AdminAuth()


@auth.login()
def login(req: Request, login_req: LoginReq) -> None:
    if login_req.username == "admin" and login_req.password == "admin":
        req.session.update({"token": "admin-token"})
    else:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid username or password"
        )


@auth.authenticate()
def authenticate(req: Request) -> None:
    token = req.session.get("token")

    if not token == "admin-token":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")

@auth.logout()
def logout(req: Request) -> None:
    req.session.clear()
