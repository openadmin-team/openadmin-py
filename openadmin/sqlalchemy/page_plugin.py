# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from openadmin.plugins import PagePlugin

from .types import Table


class SQLAlchemyPagePlugin(PagePlugin):
    def __init__(self, tables: List[Table]) -> None:
        self.tables = tables
