# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from .page_protocol import AdminPageProtocol
from .panel_protocol import AdminPanelProtocol
from .plugin_abc import PagePlugin, PanelPlugin

__all__ = [
    "PagePlugin",
    "PanelPlugin",
    "AdminPageProtocol",
    "AdminPanelProtocol",
]
