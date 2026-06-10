# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import PaginationParamsDep, SearchQueryDep
from openadmin.plugins import AdminPageProtocol, PagePlugin
from openadmin.types import Stat as StatResponse
from openadmin.types import Table as TableResponse
from sqlalchemy import String, Text, or_, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from . import state
from .types import List, Stat, Table


class SQLAlchemyPagePlugin(PagePlugin):
    def __init__(
        self, *, tables: List[Table] | None = None, stats: List[Stat] | None = None
    ) -> None:
        self.tables = tables
        self.stats = stats
        self.shared_state = state.get_shared_state()

    def after_page_init(self, page: AdminPageProtocol) -> None:
        for table in self.tables:
            model = table.get("model")
            default_name = f"{model.__name__} table"
            default_description = f"Admin page for {model.__name__} table"

            page.table(
                name=table.get("name", default_name),
                description=table.get("description", default_description),
            )(self.__create_table_route(table))

            for stat in table.get("stats", []):
                page.stat(
                    name=stat.get("name", f"{model.__name__} stat"),
                    description=stat.get("description"),
                )(self.__create_stat_route(stat))

    def __create_table_route(self, table: Table):
        async def _(
            pagination: PaginationParamsDep,
            search: SearchQueryDep,
        ) -> TableResponse:
            engine = self.__get_async_engine()
            model = table.get("model")
            columns = table.get("columns")
            sort_cols = table.get("sort")

            stmt = select(*columns) if columns else select(model)

            if search:
                if columns:
                    searchable = [
                        col
                        for col in columns
                        if isinstance(col.property.columns[0].type, (String, Text))
                    ]
                else:
                    searchable = [
                        col
                        for col in model.__table__.columns
                        if isinstance(col.type, (String, Text))
                    ]
                if searchable:
                    stmt = stmt.where(
                        or_(*(col.ilike(f"%{search}%") for col in searchable))
                    )

            if sort_cols:
                stmt = stmt.order_by(*sort_cols)

            stmt = stmt.offset(pagination.page * pagination.per_page).limit(
                pagination.per_page
            )

            async with AsyncSession(engine) as session:
                result = await session.execute(stmt)

            if columns:
                col_names = [col.key for col in columns]
                rows = [dict(zip(col_names, row)) for row in result.all()]
            else:
                rows = [
                    {c.key: getattr(row, c.key) for c in model.__table__.columns}
                    for row in result.scalars().all()
                ]

            return TableResponse(data=rows)  # type: ignore

        return _

    def __create_stat_route(self, stat: Stat):
        async def _() -> StatResponse:
            engine = self.__get_async_engine()
            async with AsyncSession(engine) as session:
                result = await session.execute(stat["query"])
                return StatResponse(value=result.scalar())  # type: ignore

        return _

    def __get_async_engine(self) -> AsyncEngine:
        engine_callback = self.shared_state.get("async_engine_callback")

        if not engine_callback:
            raise RuntimeError("Async engine callback not set in SQLAlchemyPanelPlugin")

        return engine_callback()  # type: ignore
