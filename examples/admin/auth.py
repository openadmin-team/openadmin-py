# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import Request

from openadmin.fastapi import AdminAuth, LoginReq

auth = AdminAuth()


@auth.login()
def login(req: Request, login: LoginReq) -> None: ...


@auth.authenticate()
def authenticate(req: Request) -> None: ...
