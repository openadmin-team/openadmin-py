# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from functools import lru_cache
from typing import Any, Generator, NotRequired, TypedDict

from sqlalchemy.ext.asyncio import AsyncEngine


class PluginSharedState(TypedDict):
    async_engine_dep: NotRequired[Generator[AsyncEngine, Any, None]]


@lru_cache()
def get_shared_state() -> PluginSharedState:
    return {}
