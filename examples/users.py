# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import func, or_, select

from openadmin.fastapi import AdminPage, PaginationParamsDep, SearchQueryDep
from openadmin.types import AreaChart, BarChart, PieChart, Stat, Table

from .database import AsyncSessionDep
from .models import Author, Book, BookToGenre, Genre

page = AdminPage('Users')


@page.stat('Total Authors')
async def total_authors(session: AsyncSessionDep) -> Stat:
    result = await session.execute(select(func.count()).select_from(Author))
    return Stat(value=result.scalar_one())


@page.stat('Authors with Bio')
async def authors_with_bio(session: AsyncSessionDep) -> Stat:
    result = await session.execute(
        select(func.count()).select_from(Author).where(Author.bio.is_not(None))
    )
    return Stat(value=result.scalar_one())


@page.stat('Total Books')
async def total_books(session: AsyncSessionDep) -> Stat:
    result = await session.execute(select(func.count()).select_from(Book))
    return Stat(value=result.scalar_one())


@page.table('Authors')
async def authors_table(
    session: AsyncSessionDep,
    pagination: PaginationParamsDep,
    search: SearchQueryDep,
) -> Table:
    stmt = select(Author)
    if search:
        pattern = f'%{search}%'
        stmt = stmt.where(or_(Author.first_name.ilike(pattern), Author.last_name.ilike(pattern)))
    stmt = stmt.offset(pagination.page * pagination.per_page).limit(pagination.per_page)
    authors = (await session.execute(stmt)).scalars().all()
    return Table(
        data=[
            {'id': a.id, 'first_name': a.first_name, 'last_name': a.last_name, 'has_bio': a.bio is not None}
            for a in authors
        ]
    )


@page.table('Books by Author')
async def books_by_author_table(
    session: AsyncSessionDep,
    pagination: PaginationParamsDep,
    search: SearchQueryDep,
) -> Table:
    stmt = (
        select(Author, func.count(Book.id).label('book_count'))
        .outerjoin(Book, Book.author_id == Author.id)
        .group_by(Author.id)
        .order_by(func.count(Book.id).desc())
    )
    if search:
        pattern = f'%{search}%'
        stmt = stmt.where(or_(Author.first_name.ilike(pattern), Author.last_name.ilike(pattern)))
    stmt = stmt.offset(pagination.page * pagination.per_page).limit(pagination.per_page)
    rows = (await session.execute(stmt)).all()
    return Table(
        data=[{'author': f'{a.first_name} {a.last_name}', 'book_count': count} for a, count in rows]
    )


@page.bar_chart('Books per Genre', 'Number of books in each genre')
async def books_per_genre_chart(session: AsyncSessionDep) -> BarChart:
    stmt = (
        select(Genre.name, func.count(BookToGenre.book_id).label('books'))
        .join(BookToGenre, BookToGenre.genre_id == Genre.id)
        .group_by(Genre.id)
        .order_by(func.count(BookToGenre.book_id).desc())
    )
    rows = (await session.execute(stmt)).all()
    return BarChart(
        data=[{'genre': name, 'books': count} for name, count in rows],
        config={'books': {'label': 'Books', 'color': '#6366f1'}},
    )


@page.pie_chart('Authors with Bio', 'Distribution of authors with and without biographies')
async def authors_bio_chart(session: AsyncSessionDep) -> PieChart:
    with_bio = (
        await session.execute(select(func.count()).select_from(Author).where(Author.bio.is_not(None)))
    ).scalar_one()
    without_bio = (
        await session.execute(select(func.count()).select_from(Author).where(Author.bio.is_(None)))
    ).scalar_one()
    return PieChart(
        data=[{'segment': 'With Bio', 'count': with_bio}, {'segment': 'Without Bio', 'count': without_bio}],
        config={'count': {'label': 'Authors', 'color': '#10b981'}},
    )


@page.area_chart('Books by Decade', 'Number of books published per decade')
async def books_by_decade_chart(session: AsyncSessionDep) -> AreaChart:
    decade = (func.floor(Book.published_year / 10) * 10).label('decade')
    stmt = (
        select(decade, func.count().label('books'))
        .where(Book.published_year.is_not(None))
        .group_by('decade')
        .order_by('decade')
    )
    rows = (await session.execute(stmt)).all()
    return AreaChart(
        data=[{'decade': f'{int(d)}s', 'books': count} for d, count in rows],
        config={'books': {'label': 'Books Published', 'color': '#f59e0b'}},
    )
