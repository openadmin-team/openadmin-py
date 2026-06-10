# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from openadmin.fastapi import AdminPage
from openadmin.sqlalchemy import SQLAlchemyPagePlugin

from .models import Author

page = AdminPage(
    "Users",
    plugins=[
        SQLAlchemyPagePlugin(
            tables=[
                {
                    "name": "Auto gen author table",
                    "model": Author,
                    "description": "Author admin panel",
                },
            ]
        )
    ],
)
