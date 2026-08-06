# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from fastapi import FastAPI
from openadmin import spec

from . import utils
from .admin_page import AdminPage


class AdminPanel:
    def __init__(self, name: str, *, description: str | None = None) -> None:
        self.version = "1.0.0"
        self.name = name
        self.description = description
        self.sections: list[spec.Section] = []

        self.app = FastAPI()
        self.__mount_spec_route(self.app)

    @property
    def spec(self) -> spec.Spec:
        return {
            "id": f"{utils.gen_id(self.name)}",
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "sections": self.sections,
        }

    def section(
        self,
        name: str,
        *,
        description: str | None = None,
        icon: spec.Icon | None = None,
        pages: list[AdminPage],
    ) -> None:
        section_id = utils.gen_id(name)

        self.sections.append(
            {
                "id": section_id,
                "name": name,
                "description": description,
                "icon": icon,
                "pages": [page.spec for page in pages],
            }
        )

        for page in pages:
            self.app.include_router(
                prefix=f"/{section_id}",
                router=page.router,
                tags=[name],
            )

    def __mount_spec_route(self, app: FastAPI) -> None:
        app.get(
            "/spec.json",
            response_model=spec.Spec,
        )(lambda: self.spec)
