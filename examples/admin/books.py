# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy import func, select

from openadmin.fastapi import AdminPage
from openadmin.fastapi.deps import PageDep, SearchQueryDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage("Books", description="Browse and manage the book catalog")


@page.stat("Total Books")
async def get_total_books(session: AsyncSessionDep) -> int:
    result = await session.execute(select(func.count(models.Book.id)))
    return result.scalar_one()


@page.stat("Published Books")
async def get_published_books(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(models.Book.id)).where(models.Book.published_year.isnot(None))
    )
    return result.scalar_one()


@page.stat("Books Without Publisher")
async def get_books_without_publisher(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(models.Book.id)).where(models.Book.publisher_id.is_(None))
    )
    return result.scalar_one()


@page.table("All Books", description="Browse all books with search and pagination")
async def get_all_books(
    session: AsyncSessionDep, pagination: PageDep, search: SearchQueryDep
):
    stmt = (
        select(models.Book, models.Author)
        .join(models.Author, models.Author.id == models.Book.author_id)
        .offset(pagination.page * pagination.per_page)
        .limit(pagination.per_page)
    )
    if search:
        stmt = stmt.where(models.Book.title.ilike(f"%{search}%"))
    result = await session.execute(stmt)
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": f"{author.first_name} {author.last_name}",
            "published_year": book.published_year,
        }
        for book, author in result.all()
    ]


class AddBookBody(BaseModel):
    title: str
    author_id: int
    published_year: int | None = None
    summary: str | None = None
    publisher_id: int | None = None


@page.form_post("Add Book", description="Add a new book to the catalog")
async def add_book(body: AddBookBody, session: AsyncSessionDep):
    book = models.Book(**body.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return {"id": book.id, "title": book.title}


@page.action_delete("Delete Book", description="Remove a book by ID")
async def delete_book(
    session: AsyncSessionDep,
    book_id: int = Query(..., description="Book ID to delete"),
):
    book = await session.get(models.Book, book_id)
    if book:
        await session.delete(book)
        await session.commit()
    return {"deleted": book_id, "found": book is not None}
