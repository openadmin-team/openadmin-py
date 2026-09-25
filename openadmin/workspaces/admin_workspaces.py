# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Awaitable, Callable
from typing import Any


class AdminWorkspaces:
    def __init__(self) -> None:
        self.workspace_func: Callable[[Any], None | Awaitable[None]] = (
            self.__create_default_workspace_func()
        )
        self.workspaces_func: Callable[[Any], None | Awaitable[None]] = (
            self.__create_default_workspaces_func()
        )
        self.select_workspace_func: Callable[[str, Any], None | Awaitable[None]] = (
            self.__create_default_select_workspace_func()
        )

    def workspace(self):
        def _(
            func: Callable[..., None | Awaitable[None]],
        ) -> Callable:

            self.workspace_func = func

            return func

        return _

    def workspaces(self):
        def _(
            func: Callable[..., None | Awaitable[None]],
        ) -> Callable:

            self.workspaces_func = func

            return func

        return _

    def select_workspace(self):
        def _(
            func: Callable[..., None | Awaitable[None]],
        ) -> Callable:

            self.select_workspace_func = func

            return func

        return _

    def __create_default_workspace_func(
        self,
    ) -> Callable[[Any], None | Awaitable[None]]: ...

    def __create_default_workspaces_func(
        self,
    ) -> Callable[[Any], None | Awaitable[None]]: ...

    def __create_default_select_workspace_func(
        self,
    ) -> Callable[[str, Any], None | Awaitable[None]]: ...
