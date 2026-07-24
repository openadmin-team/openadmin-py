# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from fastapi import FastAPI, HTTPException, status
from openadmin import spec

from .admin_page import AdminPage
from .section import Section


class AdminPanel:
    def __init__(self, name: str, *, description: str | None = None) -> None:
        self.version = "1.0.0"
        self.name = name
        self.description = description
        self.state: list[Section] = []
        self.app = FastAPI()
        self.key_repeat_count: dict[str, int] = {}
        self.__init_spec_route(self.app)
        self.root: FastAPI | None = None

    def get_panel_spec(self, app: FastAPI) -> spec.Spec:
        sections: list[spec.Section] = []

        for section in self.state:
            sections.append(
                spec.Section(
                    id=section.id,
                    name=section.name,
                    description=section.description,
                    icon=section.icon,
                    pages=[p.get_page_spec(app) for p in section.pages],
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
        icon: spec.Icon | None = None,
        pages: list[AdminPage],
    ) -> None:
        kebab_name = name.lower().replace(" ", "-")

        if kebab_name in self.key_repeat_count:
            number = self.key_repeat_count[kebab_name]
            kebab_name = f"{kebab_name}-{number}"
            self.key_repeat_count[kebab_name] += 1
        else:
            self.key_repeat_count[kebab_name] = 1

        self.state.append(
            Section(
                id=kebab_name,
                name=name,
                description=description,
                icon=icon,
                pages=pages,
            )
        )

        for page in pages:
            self.app.include_router(
                prefix=f"/{kebab_name}", router=page.router, tags=[name]
            )

    def mount_to(self, root: FastAPI) -> None:
        self.root = root
        root.mount("/openadmin", self.app)

    def __init_spec_route(self, app: FastAPI) -> None:
        @app.get(
            "/spec.json",
            response_model=spec.Spec,
        )
        async def _():
            if not self.root:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Admin panel should be mounted to root, user admin_panel.mount_to(app)",
                )

            return self.get_panel_spec(self.root)
