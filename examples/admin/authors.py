# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel
from sqlalchemy import func, select

from openadmin.fastapi import AdminPage
from openadmin.fastapi.deps import PageDep, SearchQueryDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage(
    "Authors", description="Manage book authors and view productivity stats"
)


@page.stat("Total Authors")
async def get_total_authors(session: AsyncSessionDep) -> int:
    result = await session.execute(select(func.count(models.Author.id)))
    return result.scalar_one()


@page.stat("Authors with Bio")
async def get_authors_with_bio(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(models.Author.id)).where(models.Author.bio.isnot(None))
    )
    return result.scalar_one()


@page.stat("Avg Books per Author")
async def get_avg_books_per_author(session: AsyncSessionDep) -> float:
    subq = (
        select(func.count(models.Book.id).label("cnt"))
        .group_by(models.Book.author_id)
        .subquery()
    )
    result = await session.execute(select(func.avg(subq.c.cnt)))
    return round(float(result.scalar_one() or 0), 2)


@page.table("All Authors", description="Browse authors with search and book counts")
async def get_all_authors(
    session: AsyncSessionDep, pagination: PageDep, search: SearchQueryDep
):
    stmt = (
        select(models.Author, func.count(models.Book.id).label("book_count"))
        .outerjoin(models.Book, models.Book.author_id == models.Author.id)
        .group_by(models.Author.id)
        .offset(pagination.page * pagination.per_page)
        .limit(pagination.per_page)
    )
    if search:
        full_name = models.Author.first_name + " " + models.Author.last_name
        stmt = stmt.where(full_name.ilike(f"%{search}%"))
    result = await session.execute(stmt)
    return [
        {
            "id": author.id,
            "name": f"{author.first_name} {author.last_name}",
            "bio": (author.bio[:80] + "...")
            if author.bio and len(author.bio) > 80
            else author.bio,
            "book_count": count,
        }
        for author, count in result.all()
    ]


@page.bar_chart(
    "Top Authors by Book Count",
    description="The 10 most prolific authors in the catalog",
)
async def get_top_authors(session: AsyncSessionDep):
    stmt = (
        select(
            (models.Author.first_name + " " + models.Author.last_name).label("name"),
            func.count(models.Book.id).label("count"),
        )
        .join(models.Book, models.Book.author_id == models.Author.id)
        .group_by(models.Author.id)
        .order_by(func.count(models.Book.id).desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    return [{"label": row.name, "value": row.count} for row in result]


class AddAuthorBody(BaseModel):
    first_name: str
    last_name: str
    bio: str | None = None


@page.form_post("Add Author", description="Register a new author in the catalog")
async def add_author(body: AddAuthorBody, session: AsyncSessionDep):
    author = models.Author(**body.model_dump())
    session.add(author)
    await session.commit()
    await session.refresh(author)
    return {"id": author.id, "name": f"{author.first_name} {author.last_name}"}
