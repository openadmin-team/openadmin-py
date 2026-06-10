# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Protocol

from .page import AdminPageProtocol


class PagePluginProtocol(Protocol):
    def after_page_init(self, page: AdminPageProtocol) -> None: ...
