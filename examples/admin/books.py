# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import asyncio
from urllib.parse import quote

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy import func, select

from openadmin import spec
from openadmin.fastapi import AdminPage
from openadmin.fastapi.deps import PageDep, SearchDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage("Books", icon="book", description="Browse and manage the book catalog")


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


BOOK_COVER_URL = "https://img.magnific.com/free-photo/beautiful-tropical-beach-sea-ocean-with-white-cloud-blue-sky-copyspace_74190-8663.jpg?semt=ais_hybrid&w=740&q=80"


@page.table(
    "All Books",
    description="Browse all books with search and pagination",
    icon="book",
    color="blue",
    columns={
        "id": {"label": "ID", "icon": "hash", "color": "slate"},
        "cover": {
            "style": "image",
            "label": "Cover",
            "icon": "image",
            "color": "sky",
        },
        "title": {"label": "Title", "icon": "book-text", "color": "blue"},
        "author": {"label": "Author", "icon": "user-pen", "color": "violet"},
        "published_year": {
            "label": "Published Year",
            "icon": "puzzle",
            "color": "blue",
        },
        "status": {
            "style": "badge",
            "label": "Status",
            "icon": "badge-check",
            "color": "emerald",
        },
        "reference": {
            "style": "link",
            "label": "Reference",
            "icon": "external-link",
            "color": "indigo",
        },
        "attachment": {
            "style": "file",
            "label": "Attachment",
            "icon": "file",
            "color": "amber",
        },
    },
)
async def get_all_books(
    session: AsyncSessionDep, pagination: PageDep, search: SearchDep
) -> spec.Table:
    await asyncio.sleep(5)  # TEMP: simulate latency for manual UX testing
    stmt = (
        select(models.Book, models.Author)
        .join(models.Author, models.Author.id == models.Book.author_id)
        .offset((pagination.page - 1) * pagination.per_page)
        .limit(pagination.per_page)
    )
    if search:
        stmt = stmt.where(models.Book.title.ilike(f"%{search}%"))
    result = await session.execute(stmt)
    return {
        "data": [
            {
                "id": book.id,
                "cover": BOOK_COVER_URL,
                "title": book.title,
                "author": f"{author.first_name} {author.last_name}",
                "published_year": book.published_year,
                "status": "Published" if book.published_year else "Draft",
                "reference": f"https://www.google.com/search?tbm=bks&q={quote(book.title)}",
                "attachment": BOOK_COVER_URL,
                "__values__": {
                    "reference": {"label": "Link to the book"},
                    "attachment": {"label": "Book in pdf"},
                },
            }
            for book, author in result.all()
        ],
    }


class AddBookBody(BaseModel):
    title: str
    author_id: int
    published_year: int | None = None
    summary: str | None = None
    publisher_id: int | None = None


@page.table(
    "Books by Author",
    description="Number of books per author",
    icon="users-round",
    color="violet",
    columns={
        "author": {"label": "Author", "icon": "user-pen", "color": "violet"},
        "book_count": {"label": "Book Count", "icon": "book-copy", "color": "blue"},
    },
)
async def get_books_by_author(session: AsyncSessionDep, pagination: PageDep):
    stmt = (
        select(models.Author, func.count(models.Book.id).label("book_count"))
        .join(models.Book, models.Book.author_id == models.Author.id)
        .group_by(models.Author.id)
        .order_by(func.count(models.Book.id).desc())
        .offset((pagination.page - 1) * pagination.per_page)
        .limit(pagination.per_page)
    )
    result = await session.execute(stmt)
    return [
        {
            "author": f"{author.first_name} {author.last_name}",
            "book_count": book_count,
        }
        for author, book_count in result.all()
    ]


@page.form("Add Book", description="Add a new book to the catalog")
async def add_book(body: AddBookBody, session: AsyncSessionDep) -> spec.Form:
    book = models.Book(**body.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return {
        "message": f"Added book '{book.title}'",
        "table": {"id": book.id, "title": book.title},
    }


@page.action("Delete Book", method="delete", description="Remove a book by ID")
async def delete_book(
    session: AsyncSessionDep,
    book_id: int = Query(..., description="Book ID to delete"),
) -> spec.Action:
    book = await session.get(models.Book, book_id)
    if book:
        await session.delete(book)
        await session.commit()
    found = book is not None
    return {
        "message": f"Deleted book #{book_id}"
        if found
        else f"Book #{book_id} not found",
        "table": {"deleted": book_id, "found": found},
    }
