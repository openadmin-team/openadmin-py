# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import func, select

from openadmin import spec
from openadmin.fastapi import AdminPage

from ..lib import models
from ..lib.database import AsyncSessionDep

page = AdminPage(
    "Analytics",
    icon="bar-chart",
    description="Library-wide publication trends and insights",
)


@page.stat(
    "Earliest Publication",
    icon="sun",
    description="This is earliest publications for the last quorder",
    color="red",
)
async def get_earliest_publication(session: AsyncSessionDep) -> spec.Stat:
    result = await session.execute(
        select(func.min(models.Book.published_year)).where(
            models.Book.published_year.isnot(None)
        )
    )
    return result.scalar_one_or_none()


@page.stat(
    "Latest Publication",
    description="Most recent publication year found in the catalog",
)
async def get_latest_publication(session: AsyncSessionDep) -> spec.Stat:
    result = await session.execute(
        select(func.max(models.Book.published_year)).where(
            models.Book.published_year.isnot(None)
        )
    )

    return {
        "value": result.scalar_one_or_none() or "N/A",
        "color": "blue",
        "icon": "clock",
    }


@page.stat(
    "Books with Summary",
    icon="book-check",
    color="teal",
    description="Number of books that include a summary",
)
async def get_books_with_summary(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(models.Book.id)).where(models.Book.summary.isnot(None))
    )
    return result.scalar_one()


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
