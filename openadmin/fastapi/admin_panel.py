# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict, List

from fastapi import FastAPI
from openadmin import spec

from . import types
from .admin_page import AdminPage


class AdminPanel:
    def __init__(self, name: str, *, description: str | None = None) -> None:
        self.version = "1.0.0"
        self.name = name
        self.description = description
        self.state: List[types.Section] = []
        self.app = FastAPI()
        self.key_repeat_count: Dict[str, int] = {}
        self.__init_spec_route(self.app)

    def get_panel_spec(self) -> spec.Spec:
        sections: List[spec.Section] = []

        for section in self.state:
            sections.append(
                spec.Section(
                    name=section.name,
                    description=section.description,
                    pages=[p.get_page_spec(self.app) for p in section.pages],
                )
            )

        return spec.Spec(
            version=self.version,
            name=self.name,
            description=self.description,
            sections=sections,
        )

    def section(
        self,
        name: str,
        *,
        description: str | None = None,
        pages: List[AdminPage],
    ) -> None:
        kebab_name = name.lower().replace(" ", "-")

        if kebab_name in self.key_repeat_count:
            number = self.key_repeat_count[kebab_name]
            kebab_name = f"{kebab_name}-{number}"
            self.key_repeat_count[kebab_name] += 1
        else:
            self.key_repeat_count[kebab_name] = 1

        self.state.append(
            types.Section(
                name=name,
                description=description,
                pages=pages,
            )
        )

        for page in pages:
            self.app.include_router(prefix=kebab_name, router=page.router, tags=[name])

    def __init_spec_route(self, app: FastAPI) -> None:
        @app.get("/spec.json")
        async def _():
            return self.get_panel_spec()
