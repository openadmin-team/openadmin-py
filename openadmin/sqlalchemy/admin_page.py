# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Sequence

from fastapi.params import Depends

from openadmin import fastapi, spec
from sqlalchemy.orm import DeclarativeBase

from . import types


class AdminPage(fastapi.AdminPage):
    def __init__(
        self,
        name: str,
        *,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
        description: str | None = None,
        dependencies: Sequence[Depends] | None = None,
        model: type[DeclarativeBase] | None = None,
        stats: list[types.Stat] | None = None,
        tables: list[types.Table] | None = None,
        actions: list[types.Action] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            icon=icon,
            color=color,
            dependencies=dependencies,
            description=description,
        )

        self.model = model or []
        self.stats = stats or []
        self.tables = tables or []
        self.actions = actions or []
