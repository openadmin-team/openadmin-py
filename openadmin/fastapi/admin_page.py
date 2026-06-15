# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import uuid
from typing import Dict, List

from fastapi import APIRouter, FastAPI
from openadmin import spec

from . import types


class AdminPage:
    def __init__(
        self,
        name: str,
        *,
        description: str | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.state: List[types.Stat | types.Table] = []
        self.router = APIRouter(prefix=name.lower().replace(" ", "-"))
        self.key_repeat_count: Dict[str, int] = {}

    def get_page_spec(self, app: FastAPI) -> spec.Page:
        components: List[spec.Component] = []

        for item in self.state:
            url = app.url_path_for(
                item.function_name,
            )

            if isinstance(item, types.Stat):
                components.append(
                    spec.Stat(
                        type="stat",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                    )
                )

            if isinstance(item, types.Table):
                components.append(
                    spec.Table(
                        type="table",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                    )
                )

        return spec.Page(
            name=self.name,
            description=self.description,
            components=components,
        )

    def table(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")

        if kebab_name in self.key_repeat_count:
            number = self.key_repeat_count[kebab_name]
            kebab_name = f"{kebab_name}-{number}"
            self.key_repeat_count[kebab_name] += 1
        else:
            self.key_repeat_count[kebab_name] = 1

        unique_name = f"{kebab_name}-{uuid.uuid4()}"

        self.state.append(
            types.Table(
                function_name=unique_name,
                method="get",
                name=name,
                description=description,
            )
        )

        return self.router.get(
            f"table/{kebab_name}",
            name=unique_name,
            description=description,
        )

    def stat(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")

        if kebab_name in self.key_repeat_count:
            number = self.key_repeat_count[kebab_name]
            kebab_name = f"{kebab_name}-{number}"
            self.key_repeat_count[kebab_name] += 1
        else:
            self.key_repeat_count[kebab_name] = 1

        unique_name = f"{kebab_name}-{uuid.uuid4()}"

        self.state.append(
            types.Stat(
                function_name=unique_name,
                method="get",
                name=name,
                description=description,
            )
        )

        return self.router.get(
            f"stat/{kebab_name}",
            name=unique_name,
            description=description,
        )

    def markdowm(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def action_post(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def action_get(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def action_put(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def action_patch(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def action_delete(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def form_post(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def form_put(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def form_patch(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def form_delete(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def area_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def bar_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def line_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...

    def pie_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ): ...
