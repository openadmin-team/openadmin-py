# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import func, select

from openadmin import sqlalchemy

from ..lib.models import Book

page = sqlalchemy.AdminPage(
    "My books",
    model=Book,
    stats=[
        {
            "name": "Total books",
            "description": "Total amount of books",
            "query": select(func.count()).select_from(Book),
        }
    ],
    tables=[
        {
            "model": Book,
        }
    ],
)
