# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from fastapi import APIRouter
from openadmin.plugins import PagePlugin
from openadmin.types import AreaChart, BarChart, LineChart, PieChart, Stat, Table


class AdminPage(APIRouter):
    def __init__(self, name: str, *, plugins: List[PagePlugin] | None = None):
        super().__init__(prefix=f"/{name.lower().replace(' ', '-')}")

        if plugins:
            for plugin in plugins:
                plugin.after_page_init(self)

    def stat(
        self,
        name: str,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/stat/{kebab_name}",
            summary=name,
            description=description,
            response_model=Stat,
        )

    def table(
        self,
        name: str,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/table/{kebab_name}",
            summary=name,
            description=description,
            response_model=Table,
        )

    def markdown(self, name: str):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/markdown/{kebab_name}",
            summary=name,
            response_model=str,
        )

    def action_get(
        self,
        name: str,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/action/{kebab_name}",
            summary=name,
            description=description,
        )

    def action_post(
        self,
        name: str,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.post(
            f"/action/{kebab_name}",
            summary=name,
            description=description,
        )

    def action_put(
        self,
        name: str,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.put(
            f"/action/{kebab_name}",
            summary=name,
            description=description,
        )

    def action_patch(
        self,
        name: str,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.patch(
            f"/action/{kebab_name}",
            summary=name,
            description=description,
        )

    def action_delete(
        self,
        name: str,
        description: str | None = None,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.delete(
            f"/action/{kebab_name}",
            summary=name,
            description=description,
        )

    def form_post(
        self,
        name: str,
        description: str,
        hide: bool = False,
    ):
        kebab_name = name.lower().replace(" ", "-")
        hide_path = ""

        if hide:
            hide_path = "__hide__/"

        return self.post(
            f"/form/{hide_path}{kebab_name}",
            summary=name,
            description=description,
        )

    def form_put(
        self,
        name: str,
        description: str,
        hide: bool = False,
    ):
        kebab_name = name.lower().replace(" ", "-")
        hide_path = ""

        if hide:
            hide_path = "__hide__/"

        return self.put(
            f"/form/{hide_path}{kebab_name}",
            summary=name,
            description=description,
        )

    def form_patch(
        self,
        name: str,
        description: str,
        hide: bool = False,
    ):
        kebab_name = name.lower().replace(" ", "-")
        hide_path = ""

        if hide:
            hide_path = "__hide__/"

        return self.patch(
            f"/form/{hide_path}{kebab_name}",
            summary=name,
            description=description,
        )

    def form_delete(
        self,
        name: str,
        description: str,
        hide: bool = False,
    ):
        kebab_name = name.lower().replace(" ", "-")
        hide_path = ""

        if hide:
            hide_path = "__hide__/"

        return self.delete(
            f"/form/{hide_path}{kebab_name}",
            summary=name,
            description=description,
        )

    def area_chart(
        self,
        name: str,
        description: str,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/area-chart/{kebab_name}",
            summary=name,
            description=description,
            response_model=AreaChart,
        )

    def bar_chart(
        self,
        name: str,
        description: str,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/bar-chart/{kebab_name}",
            summary=name,
            description=description,
            response_model=BarChart,
        )

    def line_chart(
        self,
        name: str,
        description: str,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/line-chart/{kebab_name}",
            summary=name,
            description=description,
            response_model=LineChart,
        )

    def pie_chart(
        self,
        name: str,
        description: str,
    ):
        kebab_name = name.lower().replace(" ", "-")
        return self.get(
            f"/pie-chart/{kebab_name}",
            summary=name,
            description=description,
            response_model=PieChart,
        )
