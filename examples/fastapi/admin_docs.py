# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path

from openadmin.docs import DocsPagePlugin
from openadmin.fastapi import AdminPage

page = AdminPage(
    "Admin docs",
    plugins=[
        DocsPagePlugin(
            path=Path(__file__).parent / "docs",
        ),
    ],
)
