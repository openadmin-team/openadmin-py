# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Awaitable, Callable
from datetime import timedelta

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

    def table(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
        columns: dict[str, spec.ColumnConfigValue] | None = None,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
        refresh: timedelta | None = None,
    ):
        table_id = utils.get_id(name)

        item: spec.TableComponent = {
            "type": "table",
            "id": table_id,
            "name": name,
            "columns": columns,
            "description": description,
            "is_hidden": is_hidden,
            "icon": icon,
            "color": color,
            "method": "get",
            "query": None,
            "body": None,
            "form": None,
            "refresh": refresh // timedelta(milliseconds=1)
            if refresh is not None
            else None,
        }

        self.components.append(item)

        return self.__create_table_admin_decorator(
            item,
            self.router.get(
                f"/table/{table_id}",
                description=description,
                # `spec.Table` unions a bare row iterable with a `TableResponse`
                # dict. FastAPI's inferred response model validates a dict
                # against the iterable arm first, collapsing it to its keys, so
                # response validation is disabled and the return value is
                # serialized as-is.
                response_model=None,
            ),
        )

    def stat(
        self,
        name: str,
        *,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
        description: str | None = None,
        refresh: timedelta | None = None,
    ):
        stat_id = utils.get_id(name)

        item: spec.StatComponent = {
            "type": "stat",
            "id": stat_id,
            "name": name,
            "description": description,
            "icon": icon,
            "color": color,
            "method": "get",
            "query": None,
            "body": None,
            "form": None,
            "refresh": refresh // timedelta(milliseconds=1)
            if refresh is not None
            else None,
        }

        self.components.append(item)

        return self.__create_stat_admin_decorator(
            item,
            self.router.get(
                f"/stat/{stat_id}",
                description=description,
            ),
        )

    def markdown(
        self,
        name: str,
        *,
        description: str | None = None,
        color: spec.Color | None = None,
        icon: spec.Icon | None = None,
        refresh: timedelta | None = None,
    ):
        markdown_id = utils.get_id(name)

        item: spec.MarkdownComponent = {
            "type": "markdown",
            "id": markdown_id,
            "name": name,
            "description": description,
            "color": color,
            "icon": icon,
            "method": "get",
            "query": None,
            "body": None,
            "form": None,
            "refresh": refresh // timedelta(milliseconds=1)
            if refresh is not None
            else None,
        }

        self.components.append(item)

        return self.__create_markdown_admin_decorator(
            item,
            self.router.get(
                f"/markdown/{markdown_id}",
                description=description,
            ),
        )

    def action(
        self,
        name: str,
        *,
        method: spec.HttpMethod = "post",
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        action_id = utils.get_id(name)

        item: spec.ActionComponent = {
            "type": "action",
            "id": action_id,
            "name": name,
            "description": description,
            "is_hidden": is_hidden,
            "icon": icon,
            "color": color,
            "method": method,
            "query": None,
            "body": None,
            "form": None,
        }

        self.components.append(item)

        match method:
            case "get":
                fastapi_decorator = self.router.get(
                    f"/action/{action_id}",
                    description=description,
                )
            case "post":
                fastapi_decorator = self.router.post(
                    f"/action/{action_id}",
                    description=description,
                )
            case "put":
                fastapi_decorator = self.router.put(
                    f"/action/{action_id}",
                    description=description,
                )
            case "delete":
                fastapi_decorator = self.router.delete(
                    f"/action/{action_id}",
                    description=description,
                )
            case "patch":
                fastapi_decorator = self.router.patch(
                    f"/action/{action_id}",
                    description=description,
                )
            case "head":
                fastapi_decorator = self.router.head(
                    f"/action/{action_id}",
                    description=description,
                )

        return self.__create_action_admin_decorator(
            item,
            fastapi_decorator,
        )

    def form(
        self,
        name: str,
        *,
        method: spec.HttpMethod = "post",
        fields: dict[str, spec.FieldConfig] | None = None,
        description: str | None = None,
        is_hidden: bool = False,
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        form_id = utils.get_id(name)

        item: spec.FormComponent = {
            "type": "form",
            "id": form_id,
            "name": name,
            "description": description,
            "is_hidden": is_hidden,
            "icon": icon,
            "color": color,
            "method": method,
            "query": None,
            "body": None,
            "form": None,
            "fields": fields,
        }

        self.components.append(item)

        match method:
            case "get":
                fastapi_decorator = self.router.get(
                    f"/form/{form_id}",
                    description=description,
                )
            case "post":
                fastapi_decorator = self.router.post(
                    f"/form/{form_id}",
                    description=description,
                )
            case "put":
                fastapi_decorator = self.router.put(
                    f"/form/{form_id}",
                    description=description,
                )
            case "delete":
                fastapi_decorator = self.router.delete(
                    f"/form/{form_id}",
                    description=description,
                )
            case "patch":
                fastapi_decorator = self.router.patch(
                    f"/form/{form_id}",
                    description=description,
                )
            case "head":
                fastapi_decorator = self.router.head(
                    f"/form/{form_id}",
                    description=description,
                )

        return self.__create_form_admin_decorator(
            item,
            fastapi_decorator,
        )

    # def area_chart(
    #     self,
    #     name: str,
    #     *,
    #     description: str | None = None,
    # ):
    #     area_chart_id = utils.get_id(name)

    #     item: spec.AreaChart = {
    #         "type": "area-chart",
    #         "id": area_chart_id,
    #         "name": name,
    #         "description": description,
    #         "method": "get",
    #         "query": None,
    #         "body": None,
    #         "form": None,
    #     }
    #     self.components.append(item)

    #     return self.__create_area_chart_admin_decorator(
    #         item,
    #         self.router.get(
    #             f"/area-chart/{area_chart_id}",
    #             description=description,
    #         ),
    #     )

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
        refresh: timedelta | None = None,
    ):
        bar_chart_id = utils.get_id(name)

        item: spec.BarChartComponent = {
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
            "query": None,
            "body": None,
            "form": None,
            "refresh": refresh // timedelta(milliseconds=1)
            if refresh is not None
            else None,
        }

        self.components.append(item)

        return self.__create_bar_chart_admin_decorator(
            item,
            self.router.get(
                f"/bar-chart/{bar_chart_id}",
                description=description,
            ),
        )

    # def line_chart(
    #     self,
    #     name: str,
    #     *,
    #     description: str | None = None,
    # ):
    #     line_chart_id = utils.get_id(name)

    #     item: spec.LineChart = {
    #         "type": "line-chart",
    #         "id": line_chart_id,
    #         "name": name,
    #         "description": description,
    #         "method": "get",
    #         "query": None,
    #         "body": None,
    #         "form": None,
    #     }

    #     self.components.append(item)

    #     return self.__create_line_chart_admin_decorator(
    #         item,
    #         self.router.get(
    #             f"/line-chart/{line_chart_id}",
    #             description=description,
    #         ),
    #     )

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
        refresh: timedelta | None = None,
    ):
        pie_chart_id = utils.get_id(name)

        item: spec.PieChartComponent = {
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
            "query": None,
            "body": None,
            "form": None,
            "refresh": refresh // timedelta(milliseconds=1)
            if refresh is not None
            else None,
        }

        self.components.append(item)

        return self.__create_pie_chart_admin_decorator(
            item,
            self.router.get(
                f"/pie-chart/{pie_chart_id}",
                description=description,
            ),
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

    def __create_stat_admin_decorator(
        self,
        item: spec.Component,
        fastapi_decorator: Callable,
    ):
        def _(func: Callable[..., spec.Stat | Awaitable[spec.Stat]]) -> Callable:
            item["query"] = utils.get_query_params(func)
            item["body"] = utils.get_body_params(func)
            item["form"] = utils.get_form_params(func)

            return fastapi_decorator(func)

        return _

    def __create_table_admin_decorator(
        self,
        item: spec.Component,
        fastapi_decorator: Callable,
    ):
        def _(func: Callable[..., spec.Table | Awaitable[spec.Table]]) -> Callable:
            item["query"] = utils.get_query_params(func)
            item["body"] = utils.get_body_params(func)
            item["form"] = utils.get_form_params(func)

            func.__openadmin_table_id__ = item["id"]  # type: ignore

            return fastapi_decorator(func)

        return _

    def __create_action_admin_decorator(
        self,
        item: spec.Component,
        fastapi_decorator: Callable,
    ):
        def _(func: Callable[..., spec.Action | Awaitable[spec.Action]]) -> Callable:
            item["query"] = utils.get_query_params(func)
            item["body"] = utils.get_body_params(func)
            item["form"] = utils.get_form_params(func)

            func.__openadmin_action_id__ = item["id"]  # type: ignore

            return fastapi_decorator(func)

        return _

    def __create_form_admin_decorator(
        self,
        item: spec.Component,
        fastapi_decorator: Callable,
    ):
        def _(func: Callable[..., spec.Form | Awaitable[spec.Form]]) -> Callable:
            item["query"] = utils.get_query_params(func)
            item["body"] = utils.get_body_params(func)
            item["form"] = utils.get_form_params(func)

            return fastapi_decorator(func)

        return _

    def __create_pie_chart_admin_decorator(
        self,
        item: spec.Component,
        fastapi_decorator: Callable,
    ):
        def _(
            func: Callable[..., spec.PieChart | Awaitable[spec.PieChart]],
        ) -> Callable:
            item["query"] = utils.get_query_params(func)
            item["body"] = utils.get_body_params(func)
            item["form"] = utils.get_form_params(func)

            return fastapi_decorator(func)

        return _

    def __create_bar_chart_admin_decorator(
        self,
        item: spec.Component,
        fastapi_decorator: Callable,
    ):
        def _(
            func: Callable[..., spec.BarChart | Awaitable[spec.BarChart]],
        ) -> Callable:
            item["query"] = utils.get_query_params(func)
            item["body"] = utils.get_body_params(func)
            item["form"] = utils.get_form_params(func)

            return fastapi_decorator(func)

        return _

    # def __create_line_chart_admin_decorator(
    #     self,
    #     item: spec.Component,
    #     fastapi_decorator: Callable,
    # ):
    #     def _(
    #         func: Callable[..., spec.LineChart | Awaitable[spec.LineChart]],
    #     ) -> Callable:
    #         item["query"] = utils.get_query_params(func)
    #         item["body"] = utils.get_body_params(func)
    #         item["form"] = utils.get_form_params(func)

    #         return fastapi_decorator(func)

    #     return _

    # def __create_area_chart_admin_decorator(
    #     self,
    #     item: spec.Component,
    #     fastapi_decorator: Callable,
    # ):
    #     def _(
    #         func: Callable[..., spec.AreaChart | Awaitable[spec.AreaChart]],
    #     ) -> Callable:
    #         item["query"] = utils.get_query_params(func)
    #         item["body"] = utils.get_body_params(func)
    #         item["form"] = utils.get_form_params(func)

    #         return fastapi_decorator(func)

    #     return _

    def __create_markdown_admin_decorator(
        self,
        item: spec.Component,
        fastapi_decorator: Callable,
    ):
        def _(
            func: Callable[..., spec.Markdown | Awaitable[spec.Markdown]],
        ) -> Callable:
            item["query"] = utils.get_query_params(func)
            item["body"] = utils.get_body_params(func)
            item["form"] = utils.get_form_params(func)

            return fastapi_decorator(func)

        return _
