# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import func, select

from openadmin.fastapi import AdminPage
from openadmin.fastapi.deps import PageDep

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage("Genres", description="Browse and analyze the genre taxonomy")


@page.stat("Total Genres")
async def get_total_genres(session: AsyncSessionDep) -> int:
    result = await session.execute(select(func.count(models.Genre.id)))
    return result.scalar_one()


@page.stat("Most Popular Genre")
async def get_most_popular_genre(session: AsyncSessionDep) -> str:
    stmt = (
        select(models.Genre.name)
        .join(models.BookToGenre, models.BookToGenre.genre_id == models.Genre.id)
        .group_by(models.Genre.id)
        .order_by(func.count(models.BookToGenre.book_id).desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() or "N/A"


@page.stat("Books Without Genre")
async def get_books_without_genre(session: AsyncSessionDep) -> int:
    subq = select(models.BookToGenre.book_id)
    result = await session.execute(
        select(func.count(models.Book.id)).where(models.Book.id.not_in(subq))
    )
    return result.scalar_one()


@page.table("All Genres", description="All genres sorted by book count")
async def get_all_genres(session: AsyncSessionDep, pagination: PageDep):
    stmt = (
        select(models.Genre, func.count(models.BookToGenre.book_id).label("book_count"))
        .outerjoin(models.BookToGenre, models.BookToGenre.genre_id == models.Genre.id)
        .group_by(models.Genre.id)
        .order_by(func.count(models.BookToGenre.book_id).desc())
        .offset(pagination.page * pagination.per_page)
        .limit(pagination.per_page)
    )
    result = await session.execute(stmt)
    return [
        {"id": g.id, "name": g.name, "book_count": count} for g, count in result.all()
    ]


@page.pie_chart("Genre Distribution", description="Share of books across all genres")
async def get_genre_distribution(session: AsyncSessionDep):
    stmt = (
        select(models.Genre.name, func.count(models.BookToGenre.book_id).label("count"))
        .join(models.BookToGenre, models.BookToGenre.genre_id == models.Genre.id)
        .group_by(models.Genre.id)
        .order_by(func.count(models.BookToGenre.book_id).desc())
    )
    result = await session.execute(stmt)
    return [{"label": row.name, "value": row.count} for row in result]


@page.bar_chart("Books per Genre", description="Absolute book count for each genre")
async def get_books_per_genre(session: AsyncSessionDep):
    stmt = (
        select(models.Genre.name, func.count(models.BookToGenre.book_id).label("count"))
        .join(models.BookToGenre, models.BookToGenre.genre_id == models.Genre.id)
        .group_by(models.Genre.id)
        .order_by(models.Genre.name)
    )
    result = await session.execute(stmt)
    return [{"label": row.name, "value": row.count} for row in result]
