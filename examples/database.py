# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from . import models, seed

DB_PATH = Path(__file__).parent / "database.sqlite"


@asynccontextmanager
async def lifespan():
    engine = get_async_engine()

    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
        await seed.seed(engine)

    yield

    await engine.dispose()


@lru_cache()
def get_async_engine() -> AsyncEngine:
    return create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")


async def get_async_sessionmaker(
    engine: AsyncEngine = Depends(get_async_engine),
) -> async_sessionmaker:
    return async_sessionmaker(engine)


async def get_async_session(
    sessionmaker: async_sessionmaker = Depends(get_async_sessionmaker),
):
    async with sessionmaker() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
