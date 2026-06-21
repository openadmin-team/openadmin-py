# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import func, select

from openadmin.fastapi import AdminPage
from openadmin.fastapi.deps import PageDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage(
    "Reports", description="Tag assignment activity and catalog coverage reports"
)


@page.stat("Total Tag Assignments")
async def get_total_tag_assignments(session: AsyncSessionDep) -> int:
    result = await session.execute(select(func.count()).select_from(models.BookToTag))
    return result.scalar_one()


@page.stat("Avg Tags per Book")
async def get_avg_tags_per_book(session: AsyncSessionDep) -> float:
    subq = (
        select(func.count(models.BookToTag.tag_id).label("cnt"))
        .group_by(models.BookToTag.book_id)
        .subquery()
    )
    result = await session.execute(select(func.avg(subq.c.cnt)))
    return round(float(result.scalar_one() or 0), 2)


@page.stat("Books with 4+ Tags")
async def get_heavily_tagged_books(session: AsyncSessionDep) -> int:
    subq = (
        select(models.BookToTag.book_id)
        .group_by(models.BookToTag.book_id)
        .having(func.count(models.BookToTag.tag_id) >= 4)
        .subquery()
    )
    result = await session.execute(select(func.count()).select_from(subq))
    return result.scalar_one()


@page.table(
    "Most Tagged Books", description="Books with the highest number of tag assignments"
)
async def get_most_tagged_books(session: AsyncSessionDep, pagination: PageDep):
    stmt = (
        select(
            models.Book.id,
            models.Book.title,
            func.count(models.BookToTag.tag_id).label("tag_count"),
        )
        .join(models.BookToTag, models.BookToTag.book_id == models.Book.id)
        .group_by(models.Book.id)
        .order_by(func.count(models.BookToTag.tag_id).desc())
        .offset(pagination.page * pagination.per_page)
        .limit(pagination.per_page)
    )
    result = await session.execute(stmt)
    return [
        {"id": row.id, "title": row.title, "tag_count": row.tag_count} for row in result
    ]


@page.bar_chart(
    "Tag Count Distribution", description="How many books have 0, 1, 2 … tags"
)
async def get_tag_count_distribution(session: AsyncSessionDep):
    # Count books per tag-count bucket (0–6+)
    rows = []
    for bucket in range(7):
        label = f"{bucket}+" if bucket == 6 else str(bucket)
        if bucket == 0:
            tagged_ids = select(func.distinct(models.BookToTag.book_id))
            count = (
                await session.execute(
                    select(func.count(models.Book.id)).where(
                        models.Book.id.not_in(tagged_ids)
                    )
                )
            ).scalar_one()
        elif bucket < 6:
            subq = (
                select(models.BookToTag.book_id)
                .group_by(models.BookToTag.book_id)
                .having(func.count(models.BookToTag.tag_id) == bucket)
                .subquery()
            )
            count = (
                await session.execute(select(func.count()).select_from(subq))
            ).scalar_one()
        else:
            subq = (
                select(models.BookToTag.book_id)
                .group_by(models.BookToTag.book_id)
                .having(func.count(models.BookToTag.tag_id) >= 6)
                .subquery()
            )
            count = (
                await session.execute(select(func.count()).select_from(subq))
            ).scalar_one()
        rows.append({"label": label, "value": count})
    return rows


@page.area_chart(
    "Catalog Coverage", description="Books with genre, tag, and summary metadata"
)
async def get_catalog_coverage(session: AsyncSessionDep):
    total = (await session.execute(select(func.count(models.Book.id)))).scalar_one()
    with_genre = (
        await session.execute(
            select(func.count(func.distinct(models.BookToGenre.book_id)))
        )
    ).scalar_one()
    with_tag = (
        await session.execute(
            select(func.count(func.distinct(models.BookToTag.book_id)))
        )
    ).scalar_one()
    with_summary = (
        await session.execute(
            select(func.count(models.Book.id)).where(models.Book.summary.isnot(None))
        )
    ).scalar_one()
    with_publisher = (
        await session.execute(
            select(func.count(models.Book.id)).where(
                models.Book.publisher_id.isnot(None)
            )
        )
    ).scalar_one()
    return [
        {"label": "Total Books", "value": total},
        {"label": "Has Genre", "value": with_genre},
        {"label": "Has Tag", "value": with_tag},
        {"label": "Has Summary", "value": with_summary},
        {"label": "Has Publisher", "value": with_publisher},
    ]
