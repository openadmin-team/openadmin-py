# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any, Generator

from openadmin.plugins import PanelPlugin
from sqlalchemy.ext.asyncio import AsyncEngine

from . import state


class SQLAlchemyPanelPlugin(PanelPlugin):
    def __init__(self, async_engine_dep: Generator[AsyncEngine, Any, None]):
        self.shared_state = state.get_shared_state()
        self.shared_state["async_engine_dep"] = async_engine_dep
