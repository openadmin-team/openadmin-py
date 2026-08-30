# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel
from sqlalchemy import func, select

from openadmin import spec
from openadmin.fastapi import AdminPage
from openadmin.fastapi.deps import PageDep, SearchDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage(
    "Publishers",
    icon="building-2",
    description="Manage publishers and their catalog share",
)


@page.stat("Total Publishers")
async def get_total_publishers(session: AsyncSessionDep) -> int:
    result = await session.execute(select(func.count(models.Publisher.id)))
    return result.scalar_one()


@page.stat("Countries Represented")
async def get_countries_represented(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(func.distinct(models.Publisher.country))).where(
            models.Publisher.country.isnot(None)
        )
    )
    return result.scalar_one()


@page.stat("Books Without Publisher")
async def get_books_without_publisher(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(models.Book.id)).where(models.Book.publisher_id.is_(None))
    )
    return result.scalar_one()


@page.table(
    "All Publishers",
    description="Browse publishers with their book counts",
    icon="building-2",
    color="amber",
    columns={
        "id": {"label": "ID", "icon": "hash", "color": "slate"},
        "name": {"label": "Name", "icon": "building-2", "color": "amber"},
        "country": {"label": "Country", "icon": "globe", "color": "sky"},
        "book_count": {"label": "Book Count", "icon": "book-copy", "color": "blue"},
    },
)
async def get_all_publishers(
    session: AsyncSessionDep, pagination: PageDep, search: SearchDep
):
    stmt = (
        select(models.Publisher, func.count(models.Book.id).label("book_count"))
        .outerjoin(models.Book, models.Book.publisher_id == models.Publisher.id)
        .group_by(models.Publisher.id)
        .order_by(func.count(models.Book.id).desc())
        .offset((pagination.page - 1) * pagination.per_page)
        .limit(pagination.per_page)
    )
    if search:
        stmt = stmt.where(models.Publisher.name.ilike(f"%{search}%"))
    result = await session.execute(stmt)
    return [
        {"id": pub.id, "name": pub.name, "country": pub.country, "book_count": count}
        for pub, count in result.all()
    ]


@page.pie_chart("Books by Publisher", description="Top 10 publishers by book count")
async def get_books_by_publisher(session: AsyncSessionDep):
    stmt = (
        select(models.Publisher.name, func.count(models.Book.id).label("count"))
        .join(models.Book, models.Book.publisher_id == models.Publisher.id)
        .group_by(models.Publisher.id)
        .order_by(func.count(models.Book.id).desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    return [{"label": row.name, "value": row.count} for row in result]


class AddPublisherBody(BaseModel):
    name: str
    country: str | None = None


@page.form("Add Publisher", description="Register a new publisher")
async def add_publisher(body: AddPublisherBody, session: AsyncSessionDep) -> spec.Form:
    publisher = models.Publisher(**body.model_dump())
    session.add(publisher)
    await session.commit()
    await session.refresh(publisher)
    return {"toast": f"Added publisher '{publisher.name}'"}
