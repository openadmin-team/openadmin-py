# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from sqlalchemy import func, select, update

from openadmin.fastapi import AdminPage
from openadmin.sqlalchemy import SQLAlchemyPagePlugin

from ..lib.models import Author, Book

page = AdminPage(
    "Users",
    plugins=[
        SQLAlchemyPagePlugin(
            stats=[
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
            tables=[
                {
                    "name": "Authors table",
                    "model": Author,
                    "query": select(Author).order_by(Author.first_name.desc()),
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
                        {
                            "name": "Reset password",
                            "callback": lambda id: reset_password(id),
                            "query": lambda id: (
                                update(Author)
                                .values({Author.bio: "Some text"})
                                .where(Author.id == id)
                            ),
                        },
                    ],
                    "sort": [
                        Author.id,
                        Author.first_name,
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
                },
            ],
        )
    ],
)


async def reset_password(id: int) -> None: ...
