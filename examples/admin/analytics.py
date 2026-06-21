# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import func, select

from openadmin.fastapi import AdminPage

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage(
    "Analytics", description="Library-wide publication trends and insights"
)


@page.stat("Earliest Publication")
async def get_earliest_publication(session: AsyncSessionDep) -> int | str:
    result = await session.execute(
        select(func.min(models.Book.published_year)).where(
            models.Book.published_year.isnot(None)
        )
    )
    return result.scalar_one_or_none() or "N/A"


@page.stat("Latest Publication")
async def get_latest_publication(session: AsyncSessionDep) -> int | str:
    result = await session.execute(
        select(func.max(models.Book.published_year)).where(
            models.Book.published_year.isnot(None)
        )
    )
    return result.scalar_one_or_none() or "N/A"


@page.stat("Books with Summary")
async def get_books_with_summary(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(models.Book.id)).where(models.Book.summary.isnot(None))
    )
    return result.scalar_one()


@page.line_chart(
    "Publications by Decade", description="Number of books published per decade"
)
async def get_publications_by_decade(session: AsyncSessionDep):
    stmt = (
        select(
            (func.floor(models.Book.published_year / 10) * 10).label("decade"),
            func.count(models.Book.id).label("count"),
        )
        .where(models.Book.published_year.isnot(None))
        .group_by("decade")
        .order_by("decade")
    )
    result = await session.execute(stmt)
    return [{"label": f"{int(row.decade)}s", "value": row.count} for row in result]


@page.area_chart(
    "Books Published by Era", description="Book volume across broad historical eras"
)
async def get_books_by_era(session: AsyncSessionDep):
    eras: list[tuple[str, int | None, int | None]] = [
        ("Pre-1900", None, 1900),
        ("1900–1950", 1900, 1950),
        ("1950–1980", 1950, 1980),
        ("1980–2000", 1980, 2000),
        ("2000–2010", 2000, 2010),
        ("2010–2020", 2010, 2020),
        ("2020+", 2020, None),
    ]
    rows = []
    for label, start, end in eras:
        stmt = select(func.count(models.Book.id)).where(
            models.Book.published_year.isnot(None)
        )
        if start is not None:
            stmt = stmt.where(models.Book.published_year >= start)
        if end is not None:
            stmt = stmt.where(models.Book.published_year < end)
        count = (await session.execute(stmt)).scalar_one()
        rows.append({"label": label, "value": count})
    return rows


@page.markdown("Library Overview")
async def get_library_overview(session: AsyncSessionDep) -> str:
    total_books = (
        await session.execute(select(func.count(models.Book.id)))
    ).scalar_one()
    total_authors = (
        await session.execute(select(func.count(models.Author.id)))
    ).scalar_one()
    total_publishers = (
        await session.execute(select(func.count(models.Publisher.id)))
    ).scalar_one()
    total_genres = (
        await session.execute(select(func.count(models.Genre.id)))
    ).scalar_one()
    total_tags = (await session.execute(select(func.count(models.Tag.id)))).scalar_one()

    return f"""# Library Overview

This catalog contains **{total_books:,} books** written by **{total_authors} authors**
and published by **{total_publishers} publishers**.

## Classification

The collection is organized across **{total_genres} genres** and annotated with **{total_tags} tags**,
enabling precise discovery and filtering across the full catalog.

## Coverage

Books span multiple centuries of publication history, from early historical works through
contemporary releases, with particular depth in the 20th and 21st century catalog.
"""
