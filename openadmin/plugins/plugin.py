# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC

from .page import AdminPageProtocol


class PagePlugin(ABC):
    def after_page_init(self, page: AdminPageProtocol) -> None: ...
