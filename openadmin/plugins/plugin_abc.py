# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC

from .page_protocol import AdminPageProtocol
from .panel_protocol import AdminPanelProtocol


class PagePlugin(ABC):
    def after_page_init(self, page: AdminPageProtocol) -> None: ...


class PanelPlugin(PagePlugin):
    def before_panel_init(self, page: AdminPanelProtocol) -> None: ...

    def after_panel_init(self, page: AdminPanelProtocol) -> None: ...
