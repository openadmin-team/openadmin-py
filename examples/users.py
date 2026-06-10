# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from openadmin.fastapi import AdminPage
from openadmin.sqlalchemy import SQLAlchemyPagePlugin

from .models import Author, Book

page = AdminPage(
    "Users",
    plugins=[
        SQLAlchemyPagePlugin(
            tables=[
                {
                    "name": "Authors table",
                    "model": Author,
                    "description": "Author admin table",
                },
                {
                    "name": "Books tables",
                    "model": Book,
                    "description": "Books admin table",
                },
            ]
        )
    ],
)
