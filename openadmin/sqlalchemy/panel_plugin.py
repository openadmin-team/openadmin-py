# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any, Callable

from openadmin.plugins import PanelPlugin
from sqlalchemy.ext.asyncio import AsyncEngine

from . import state


class SQLAlchemyPanelPlugin(PanelPlugin):
    def __init__(self, async_engine_callback: Callable[[Any], AsyncEngine]):
        self.shared_state = state.get_shared_state()
        self.shared_state["async_engine_callback"] = async_engine_callback
