# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

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

    def get_panel_spec(self) -> spec.Spec:
        sections = []

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
    ) -> None: ...
