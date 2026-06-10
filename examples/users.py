# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from sqlalchemy import func, select

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
                    "columns": [
                        Author.id,
                        Author.first_name,
                        Author.bio,
                    ],
                    "actions": [
                        "create",
                        "delete",
                        "read",
                        "update",
                    ],
                    "sort": [
                        Author.id,
                        Author.first_name,
                    ],
                    "stats": [
                        {
                            "name": "Books per author",
                            "description": "Number of books per author",
                            "query": select(func.count(Author.id)).select_from(Author),
                        },
                        {
                            "name": "Total books",
                            "description": "Total number of books",
                            "query": select(func.count(Book.id)),
                        },
                    ],
                },
                {
                    "name": "Books tables",
                    "model": Book,
                    "description": "Books admin table",
                    "columns": [
                        Book.id,
                        Book.title,
                    ],
                    "actions": [
                        "read",
                        "update",
                    ],
                    "sort": [
                        Book.id,
                        Book.title,
                    ],
                    "stats": [
                        {
                            "name": "Total books",
                            "description": "Total number of books",
                            "query": select(func.count(Book.id)),
                        },
                    ],
                },
            ]
        )
    ],
)
