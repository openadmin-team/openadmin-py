# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Sequence
from enum import Enum

from fastapi import FastAPI
from openadmin.plugins import PanelPlugin

from .page import AdminPage


class AdminPanel(FastAPI):
    def __init__(self, *, plugins: Sequence[PanelPlugin] | None = None) -> None:
        if plugins:
            for plugin in plugins:
                plugin.before_panel_init(self)

        super().__init__()
        self.plugins = plugins or []

        if self.plugins:
            for plugin in self.plugins:
                plugin.after_panel_init(self)

    def include_page(
        self,
        page: AdminPage,
        tags: list[str | Enum] | None = None,
    ):
        return self.include_router(router=page, tags=tags)
