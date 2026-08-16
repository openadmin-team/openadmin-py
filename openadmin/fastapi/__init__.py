# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from .admin_auth import AdminAuth
from .admin_page import AdminPage
from .admin_panel import AdminPanel
from .deps import PageDep, SearchQueryDep
from .refs import reference_action, reference_table
from .req import LoginReq

__all__ = [
    "AdminAuth",
    "AdminPage",
    "AdminPanel",
    "LoginReq",
    "PageDep",
    "SearchQueryDep",
    "reference_action",
    "reference_table",
]
