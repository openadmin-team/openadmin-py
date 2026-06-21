# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import Query
from sqlalchemy import func, select

from openadmin.fastapi import AdminPage
from openadmin.fastapi.deps import PageDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage("Tags", description="Manage and analyze book tags")


@page.stat("Total Tags")
async def get_total_tags(session: AsyncSessionDep) -> int:
    result = await session.execute(select(func.count(models.Tag.id)))
    return result.scalar_one()


@page.stat("Books Tagged")
async def get_books_tagged(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(func.distinct(models.BookToTag.book_id)))
    )
    return result.scalar_one()


@page.stat("Most Popular Tag")
async def get_most_popular_tag(session: AsyncSessionDep) -> str:
    stmt = (
        select(models.Tag.name)
        .join(models.BookToTag, models.BookToTag.tag_id == models.Tag.id)
        .group_by(models.Tag.id)
        .order_by(func.count(models.BookToTag.book_id).desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() or "N/A"


@page.table("All Tags", description="All tags sorted by usage count")
async def get_all_tags(session: AsyncSessionDep, pagination: PageDep):
    stmt = (
        select(models.Tag, func.count(models.BookToTag.book_id).label("usage_count"))
        .outerjoin(models.BookToTag, models.BookToTag.tag_id == models.Tag.id)
        .group_by(models.Tag.id)
        .order_by(func.count(models.BookToTag.book_id).desc())
        .offset(pagination.page * pagination.per_page)
        .limit(pagination.per_page)
    )
    result = await session.execute(stmt)
    return [
        {"id": tag.id, "name": tag.name, "usage_count": count}
        for tag, count in result.all()
    ]


@page.bar_chart("Top Tags by Usage", description="The 15 most frequently used tags")
async def get_top_tags(session: AsyncSessionDep):
    stmt = (
        select(models.Tag.name, func.count(models.BookToTag.book_id).label("count"))
        .join(models.BookToTag, models.BookToTag.tag_id == models.Tag.id)
        .group_by(models.Tag.id)
        .order_by(func.count(models.BookToTag.book_id).desc())
        .limit(15)
    )
    result = await session.execute(stmt)
    return [{"label": row.name, "value": row.count} for row in result]


@page.action_delete(
    "Remove Tag from Book", description="Detach a specific tag from a book"
)
async def remove_tag_from_book(
    session: AsyncSessionDep,
    book_id: int = Query(..., description="Book ID"),
    tag_id: int = Query(..., description="Tag ID"),
):
    link = await session.get(models.BookToTag, (book_id, tag_id))
    if link:
        await session.delete(link)
        await session.commit()
    return {"book_id": book_id, "tag_id": tag_id, "removed": link is not None}
