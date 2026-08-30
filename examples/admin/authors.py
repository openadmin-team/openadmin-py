# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel
from sqlalchemy import func, select

from openadmin import spec
from openadmin.fastapi import AdminPage, reference_action, reference_table
from openadmin.fastapi.deps import PageDep, SearchDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage(
    "Authors",
    icon="users",
    description="Manage book authors and view productivity stats",
)


@page.stat("Total Authors", description="Total number of authors in the catalog")
async def get_total_authors(session: AsyncSessionDep) -> spec.StatResponse:
    result = await session.execute(select(func.count(models.Author.id)))
    return {"value": result.scalar_one(), "icon": "users", "color": "indigo"}


@page.stat(
    "Authors with Bio",
    icon="user-check",
    color="emerald",
    description="Authors that have a biography on file",
)
async def get_authors_with_bio(session: AsyncSessionDep):
    result = await session.execute(
        select(func.count(models.Author.id)).where(models.Author.bio.isnot(None))
    )
    return result.scalar_one()


@page.action(
    "Delete Author",
    is_hidden=True,
)
async def delete_author(id: str) -> spec.Action:
    return {
        "toast": f"User with id {id} deleted and id is saved into clipboard",
        'clipboard': id,
    }


@page.stat(
    "Avg Books per Author",
    icon="library",
    color="amber",
    description="Average number of books published per author",
)
async def get_avg_books_per_author(session: AsyncSessionDep) -> float:
    subq = (
        select(func.count(models.Book.id).label("cnt"))
        .group_by(models.Book.author_id)
        .subquery()
    )
    result = await session.execute(select(func.avg(subq.c.cnt)))
    return round(float(result.scalar_one() or 0), 2)


@page.table(
    "All Authors",
    description="Browse authors with search and book counts",
    icon="user-pen",
    color="indigo",
    columns={
        "id": {"label": "ID", "icon": "hash", "color": "slate"},
        "name": {"label": "Name", "icon": "user", "color": "indigo"},
        "bio": {"label": "Bio", "icon": "notepad-text", "color": "gray"},
        "book_count": {"label": "Book Count", "icon": "book-copy", "color": "emerald"},
    },
)
async def get_all_authors(
    session: AsyncSessionDep, pagination: PageDep, search: SearchDep
) -> spec.Table:
    stmt = (
        select(models.Author, func.count(models.Book.id).label("book_count"))
        .outerjoin(models.Book, models.Book.author_id == models.Author.id)
        .group_by(models.Author.id)
        .offset((pagination.page - 1) * pagination.per_page)
        .limit(pagination.per_page)
    )
    count_stmt = select(func.count(models.Author.id))
    if search:
        full_name = models.Author.first_name + " " + models.Author.last_name
        stmt = stmt.where(full_name.ilike(f"%{search}%"))
        count_stmt = count_stmt.where(full_name.ilike(f"%{search}%"))
    result = await session.execute(stmt)
    total = await session.execute(count_stmt)
    return {
        "data": [
            {
                "id": author.id,
                "name": f"{author.first_name} {author.last_name}",
                "bio": (author.bio[:80] + "...")
                if author.bio and len(author.bio) > 80
                else author.bio,
                "book_count": count,
                "__view__": f"{author.first_name} {author.last_name}",
                "__actions__": [
                    {
                        "label": "Delete this user",
                        "action": reference_action(delete_author),
                        "query": {
                            "id": author.id,
                        },
                        "color": "red",
                        "icon": "trash",
                    },
                    {
                        "label": "Bun this user",
                        "action": reference_action(delete_author),
                        "query": {
                            "id": author.id,
                        },
                        "color": "yellow",
                        "icon": "alarm-clock-check",
                    },
                    {
                        "label": "Unban this user",
                        "action": reference_action(delete_author),
                        "query": {
                            "id": author.id,
                        },
                        "color": "green",
                        "icon": "leaf",
                    },
                ],
            }
            for author, count in result.all()
        ],
        "total": total.scalar_one(),
    }


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


@page.form(
    "Add Author",
    description="Register a new author in the catalog",
    fields={
        "friend": {
            "reference": reference_table(get_all_authors),
            "icon": "user",
            "color": "blue",
            "reference_field": "id",
        }
    },
)
async def add_author(body: AddAuthorBody, session: AsyncSessionDep) -> spec.Form:
    author = models.Author(**body.model_dump())
    session.add(author)
    await session.commit()
    await session.refresh(author)
    name = f"{author.first_name} {author.last_name}"
    return {"toast": f"Added author '{name}'"}
