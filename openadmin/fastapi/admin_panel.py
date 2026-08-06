# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from fastapi import FastAPI
from openadmin import spec

from . import counter, utils
from .admin_page import AdminPage


class AdminPanel:
    def __init__(self, name: str, *, description: str | None = None) -> None:
        self.version = "1.0.0"
        self.name = name
        self.description = description
        self.sections: list[spec.Section] = []

    def section(
        self,
        name: str,
        *,
        description: str | None = None,
        icon: spec.Icon | None = None,
        pages: list[AdminPage],
    ) -> None:
        self.sections.append(
            {
                "id": f"{utils.kebab_name(name)}-{counter.inc('section')}",
                "name": name,
                "description": description,
                "icon": icon,
                "pages": [page.page for page in pages],
            }
        )

    @property
    def spec(self) -> spec.Spec:
        return {
            "id": f"{utils.kebab_name(self.name)}-{counter.inc('page')}",
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "sections": self.sections,
        }

    @property
    def app(self) -> FastAPI:
        app = FastAPI()

        app.get(
            "/spec.json",
            response_model=spec.Spec,
        )(lambda: self.spec)

        return app

    def __mount_spec_route(self, app: FastAPI) -> None:
        def _() -> spec.Spec:
            return {
                "id": f"{utils.kebab_name(self.name)}-{counter.inc('page')}",
                "name": self.name,
                "version": self.version,
                "description": self.description,
                "sections": self.sections,
            }

        app.get(
            "/spec.json",
            response_model=spec.Spec,
        )(_)
