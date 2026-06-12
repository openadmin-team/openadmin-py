# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import database


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with database.lifespan():
        yield
