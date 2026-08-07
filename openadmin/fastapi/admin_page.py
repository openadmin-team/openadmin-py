# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable

from fastapi import APIRouter
from openadmin import spec

from . import utils


class AdminPage:
    def __init__(
        self,
        name: str,
        *,
        icon: spec.Icon | None = None,
        description: str | None = None,
    ) -> None:
        self.id = utils.get_id(name)
        self.name = name
        self.description = description
        self.icon: spec.Icon | None = icon
        self.components: list[spec.Component] = []

        self.router = APIRouter(
            prefix=f"/{self.id}",
        )

    @property
    def spec(self) -> spec.Page:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "components": self.components,
        }

    def table(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        table_id = utils.get_id(name)
        item: spec.TableComponent = {
            "type": "table",
            "id": table_id,
            "name": name,
            "description": description,
            "is_hidden": is_hidden,
            "icon": icon,
            "color": color,
            "method": "get",
        }
        self.components.append(item)

        return self.__create_admin_decorator(
            item,
            self.router.get(
                f"/table/{table_id}",
                description=description,
            ),
        )

    def stat(
        self,
        name: str,
        *,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
        description: str | None = None,
    ):
        stat_id = utils.get_id(name)

        self.components.append(
            {
                "type": "stat",
                "id": stat_id,
                "name": name,
                "description": description,
                "icon": icon,
                "color": color,
                "method": "get",
            }
        )

        return self.router.get(
            f"/stat/{stat_id}",
            description=description,
        )

    def markdown(
        self,
        name: str,
        *,
        description: str | None = None,
        color: spec.Color | None = None,
        icon: spec.Icon | None = None,
    ):
        markdown_id = utils.get_id(name)

        self.components.append(
            {
                "type": "markdown",
                "id": markdown_id,
                "name": name,
                "description": description,
                "color": color,
                "icon": icon,
                "method": "get",
            }
        )

        return self.router.get(
            f"/markdown/{markdown_id}",
            description=description,
        )

    def action_post(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        action_id = utils.get_id(name)

        self.components.append(
            {
                "type": "action",
                "id": action_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "post",
            }
        )

        return self.router.post(
            f"/action/{action_id}",
            description=description,
        )

    def action_get(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        action_id = utils.get_id(name)

        self.components.append(
            {
                "type": "action",
                "id": action_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "get",
            }
        )

        return self.router.get(
            f"/action/{action_id}",
            description=description,
        )

    def action_put(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        action_id = utils.get_id(name)

        self.components.append(
            {
                "type": "action",
                "id": action_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "put",
            }
        )

        return self.router.put(
            f"/action/{action_id}",
            description=description,
        )

    def action_patch(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        action_id = utils.get_id(name)

        self.components.append(
            {
                "type": "action",
                "id": action_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "patch",
            }
        )

        return self.router.patch(
            f"/action/{action_id}",
            description=description,
        )

    def action_delete(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        action_id = utils.get_id(name)

        self.components.append(
            {
                "type": "action",
                "id": action_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "delete",
            }
        )

        return self.router.delete(
            f"/action/{action_id}",
            description=description,
        )

    def form_post(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        form_id = utils.get_id(name)

        self.components.append(
            {
                "type": "form",
                "id": form_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "post",
            }
        )

        return self.router.post(
            f"/form/{form_id}",
            description=description,
        )

    def form_put(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        form_id = utils.get_id(name)

        self.components.append(
            {
                "type": "form",
                "id": form_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "put",
            }
        )

        return self.router.put(
            f"/form/{form_id}",
            description=description,
        )

    def form_patch(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        form_id = utils.get_id(name)

        self.components.append(
            {
                "type": "form",
                "id": form_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "patch",
            }
        )

        return self.router.patch(
            f"/form/{form_id}",
            description=description,
        )

    def form_delete(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        form_id = utils.get_id(name)

        self.components.append(
            {
                "type": "form",
                "id": form_id,
                "name": name,
                "description": description,
                "is_hidden": is_hidden,
                "icon": icon,
                "color": color,
                "method": "delete",
            }
        )

        return self.router.delete(
            f"/form/{form_id}",
            description=description,
        )

    def area_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        area_chart_id = utils.get_id(name)

        self.components.append(
            {
                "type": "area-chart",
                "id": area_chart_id,
                "name": name,
                "description": description,
                "method": "get",
            }
        )

        return self.router.get(
            f"/area-chart/{area_chart_id}",
            description=description,
        )

    def bar_chart(
        self,
        name: str,
        *,
        description: str | None = None,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
        caption: str | None = None,
        caption_description: str | None = None,
        caption_icon: spec.Icon | None = None,
        config: dict[str, spec.BarChartConfigValue] | None = None,
        data_key: str | None = None,
    ):
        bar_chart_id = utils.get_id(name)

        self.components.append(
            {
                "type": "bar-chart",
                "id": bar_chart_id,
                "name": name,
                "description": description,
                "config": config,
                "data_key": data_key,
                "icon": icon,
                "color": color,
                "caption": caption,
                "caption_description": caption_description,
                "caption_icon": caption_icon,
                "method": "get",
            }
        )

        return self.router.get(
            f"/bar-chart/{bar_chart_id}",
            description=description,
        )

    def line_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        line_chart_id = utils.get_id(name)

        self.components.append(
            {
                "type": "line-chart",
                "id": line_chart_id,
                "name": name,
                "description": description,
                "method": "get",
            }
        )

        return self.router.get(
            f"/line-chart/{line_chart_id}",
            description=description,
        )

    def pie_chart(
        self,
        name: str,
        *,
        description: str | None = None,
        config: dict[str, spec.PieChartConfigValue] | None = None,
        icon: spec.Icon | None = None,
        name_key: str | None = None,
        value_key: str | None = None,
        color: spec.Color | None = None,
        caption: str | None = None,
        caption_description: str | None = None,
        caption_icon: spec.Icon | None = None,
    ):
        pie_chart_id = utils.get_id(name)

        self.components.append(
            {
                "type": "pie-chart",
                "id": pie_chart_id,
                "name": name,
                "description": description,
                "config": config,
                "icon": icon,
                "name_key": name_key,
                "value_key": value_key,
                "color": color,
                "caption": caption,
                "caption_description": caption_description,
                "caption_icon": caption_icon,
                "method": "get",
            }
        )

        return self.router.get(
            f"/pie-chart/{pie_chart_id}",
            description=description,
        )

    def __create_admin_decorator[T](
        self, item: spec.Component, fastapi_decorator: Callable
    ):
        def _(func: Callable[[], T]) -> Callable:
            query, body, form = utils.extract_params(func)

            item["query"] = query
            item["body"] = body  # type: ignore
            item["form"] = form  # type: ignore

            return fastapi_decorator(func)

        return _
