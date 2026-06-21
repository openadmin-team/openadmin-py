# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import func, select, text

from openadmin.fastapi import AdminPage

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage("Overview", description="High-level database and catalog statistics")


@page.stat("Total Records")
async def get_total_records(session: AsyncSessionDep) -> int:
    counts = await _all_table_counts(session)
    return sum(c for _, c in counts)


@page.stat("Schema Tables")
async def get_schema_tables() -> int:
    return 7  # Book, Author, Publisher, Genre, Tag, BookToGenre, BookToTag


@page.stat("Catalog Completeness (%)")
async def get_catalog_completeness(session: AsyncSessionDep) -> float:
    total = (await session.execute(select(func.count(models.Book.id)))).scalar_one()
    if not total:
        return 0.0
    complete = (
        await session.execute(
            select(func.count(models.Book.id)).where(
                models.Book.summary.isnot(None),
                models.Book.published_year.isnot(None),
                models.Book.publisher_id.isnot(None),
            )
        )
    ).scalar_one()
    return round(complete / total * 100, 1)


@page.bar_chart(
    "Records per Table", description="Row count for every table in the schema"
)
async def get_records_per_table(session: AsyncSessionDep):
    counts = await _all_table_counts(session)
    return [{"label": label, "value": count} for label, count in counts]


@page.markdown("Schema Reference")
async def get_schema_reference() -> str:
    return """# Database Schema

## Core tables

| Table           | Description                                    |
|-----------------|------------------------------------------------|
| `book`          | Central entity — title, year, summary          |
| `author`        | Author first/last name and optional bio        |
| `publisher`     | Publisher name and country                     |
| `genre`         | Genre name (unique)                            |
| `tag`           | Tag name (unique)                              |

## Association tables

| Table           | Links                                          |
|-----------------|------------------------------------------------|
| `book_to_genre` | Many-to-many: book ↔ genre                    |
| `book_to_tag`   | Many-to-many: book ↔ tag, with `added_at`     |

All primary keys are auto-incrementing integers.
Foreign keys are enforced at the application layer.
"""


@page.action_get("Ping Database", description="Verify the database connection is alive")
async def ping_database(session: AsyncSessionDep):
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "message": "Database is reachable"}


async def _all_table_counts(session: AsyncSessionDep) -> list[tuple[str, int]]:
    tables: list[tuple[str, type]] = [
        ("book", models.Book),
        ("author", models.Author),
        ("publisher", models.Publisher),
        ("genre", models.Genre),
        ("tag", models.Tag),
        ("book_to_genre", models.BookToGenre),
        ("book_to_tag", models.BookToTag),
    ]
    results = []
    for label, model in tables:
        count = (
            await session.execute(select(func.count()).select_from(model))
        ).scalar_one()
        results.append((label, count))
    return results
