# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from openadmin.fastapi import PaginationParamsDep, SearchQueryDep
from openadmin.plugins import AdminPageProtocol, PagePlugin
from openadmin.types import Table as TableResponce

from .state import PluginSharedState
from .types import Table


class SQLAlchemyPagePlugin(PagePlugin):
    def __init__(self, tables: List[Table]) -> None:
        self.tables = tables
        self.shared_state: PluginSharedState = {}

    def after_page_init(self, page: AdminPageProtocol) -> None:
        for table in self.tables:
            default_name = f"{table.get('model').__name__} table"
            default_description = f"Admin page for {table.get('model').__name__} table"

            component_factory = page.table(
                name=table.get("name", default_name),
                description=table.get("description", default_description),
            )
            route = self.__create_table_route(table)

            component_factory(route)

    def __create_table_route(self, table: Table):
        def _(
            page: PaginationParamsDep,
            search: SearchQueryDep,
        ) -> TableResponce:
            return TableResponce(
                data=[
                    {
                        "page": page,
                        "search": search,
                    }
                ]
            )

        return _
