# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Callable, Awaitable, Any

class AdminWorkspaces:
    def __init__(self) -> None:
        self.workspace_func: Callable[[Any], None | Awaitable[None]]
        self.workspaces_func: Callable[[Any], None | Awaitable[None]]
        self.select_workspace_func: Callable[[str, Any], None | Awaitable[None]]

    def workspace(self): ...

    def workspaces(self): ...

    def select_workspace(self): ...
