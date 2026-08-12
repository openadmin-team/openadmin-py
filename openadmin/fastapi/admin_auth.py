# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Awaitable, Callable

from fastapi import APIRouter, Request

from .req import LoginReq


class AdminAuth:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.authenticate_func: Callable[[Request], None | Awaitable[None]] | None = (
            None
        )

    def login(self):
        return self.__create_login_decorator(
            self.router.post(
                "/login",
            )
        )

    def authenticate(self):
        return self.__create_authenticate_decorator()

    def __create_login_decorator(
        self,
        fastapi_decorator: Callable,
    ):
        def _(
            func: Callable[[Request, LoginReq], None],
        ) -> Callable:

            return fastapi_decorator(func)

        return _

    def __create_authenticate_decorator(
        self,
    ):
        def _(
            func: Callable[[Request], None | Awaitable[None]],
        ) -> Callable:

            self.authenticate_func = func

            return func

        return _
