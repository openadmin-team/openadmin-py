# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Awaitable, Callable

from fastapi import APIRouter, Request

from .req import LoginReq


class AdminAuth:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.authenticate_func: Callable[[Request], None | Awaitable[None]] = (
            self.__create_default_authenticate()
        )
        self.login_func: Callable[[Request, LoginReq], None | Awaitable[None]] = (
            self.__create_default_login()
        )
        self.logout_func: Callable[[Request], None | Awaitable[None]] = (
            self.__create_default_logout()
        )

    def login(self):
        return self.__create_login_decorator()

    def authenticate(self):
        return self.__create_authenticate_decorator()

    def logout(self):
        return self.__create_logout_decorator()

    def __create_login_decorator(
        self,
    ):
        def _(
            func: Callable[[Request, LoginReq], None],
        ) -> Callable:

            self.login_func = func

            return func

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

    def __create_logout_decorator(
        self,
    ):
        def _(
            func: Callable[[Request], None | Awaitable[None]],
        ) -> Callable:

            self.logout_func = func

            return func

        return _

    def __create_default_login(
        self,
    ) -> Callable[[Request, LoginReq], None | Awaitable[None]]: ...

    def __create_default_authenticate(
        self,
    ) -> Callable[[Request], None | Awaitable[None]]: ...

    def __create_default_logout(
        self,
    ) -> Callable[[Request], None | Awaitable[None]]: ...
