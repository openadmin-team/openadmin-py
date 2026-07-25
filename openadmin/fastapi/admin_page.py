# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re
import uuid
from collections.abc import Callable

from fastapi import APIRouter, FastAPI
from openadmin import spec

from . import counters
from .action import Action
from .area_chart import AreaChart
from .bar_chart import BarChart
from .component import Component
from .form import Form
from .line_chart import LineChart
from .markdown import Markdown
from .pie_chart import PieChart
from .stat import Stat
from .table import Table
from .utils import extract_params

_SPECIAL_CHARS_RE = re.compile(r"[^a-zA-Z0-9\s]")


class AdminPage:
    def __init__(
        self,
        name: str,
        *,
        icon: spec.Icon | None = None,
        description: str | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.icon: spec.Icon | None = icon
        self.state: list[Component] = []
        self.router = APIRouter(prefix=f"/{name.lower().replace(' ', '-')}")
        self.key_repeat_count: dict[str, int] = {}
        self.page_count = counters.get_next("page")
        self.page_kebab_name, _ = self.__get_kebab_and_unique_name(self.name)

    def get_page_spec(self, app: FastAPI) -> spec.Page:
        components: list[spec.Component] = []

        for item in self.state:
            url = app.url_path_for(item.function_name)
            query, body, form = (
                extract_params(item.func) if item.func else (None, None, None)
            )

            if isinstance(item, Stat):
                components.append(
                    spec.StatComponent(
                        type="stat",
                        id=item.id,
                        color=item.color,
                        icon=item.icon,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, Table):
                components.append(
                    spec.TableComponent(
                        type="table",
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                        body=body,
                        form=form,
                        is_hidden=item.is_hidden,
                    )
                )
            elif isinstance(item, AreaChart):
                components.append(
                    spec.AreaChart(
                        type="area-chart",
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, BarChart):
                components.append(
                    spec.BarChartComponent(
                        type="bar-chart",
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                        icon=item.icon,
                        caption=item.caption,
                        caption_icon=item.caption_icon,
                        caption_description=item.caption_description,
                        color=item.color,
                        config=item.config,
                        data_key=item.data_key,
                    )
                )
            elif isinstance(item, LineChart):
                components.append(
                    spec.LineChart(
                        type="line-chart",
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, PieChart):
                components.append(
                    spec.PieChartComponent(
                        type="pie-chart",
                        id=item.id,
                        config=item.config,
                        icon=item.icon,
                        name_key=item.name_key,
                        color=item.color,
                        value_key=item.value_key,
                        caption=item.caption,
                        caption_icon=item.caption_icon,
                        caption_description=item.caption_description,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, Action):
                components.append(
                    spec.Action(
                        type="action",
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        is_hidden=item.is_hidden,
                        query=query,
                        body=body,
                        form=form,
                    )
                )
            elif isinstance(item, Form):
                components.append(
                    spec.Form(
                        type="form",
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        is_hidden=item.is_hidden,
                        query=query,
                        body=body,
                        form=form,
                    )
                )
            elif isinstance(item, Markdown):
                components.append(
                    spec.Markdown(
                        type="markdown",
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )

        return spec.Page(
            id=f"{self.page_kebab_name}-{self.page_count}",
            name=self.name,
            description=self.description,
            icon=self.icon,
            components=components,
        )

    def _wrap_user_handler(self, item: Component, fastapi_decorator) -> Callable:
        def decorator(func: Callable) -> Callable:
            item.func = func
            return fastapi_decorator(func)

        return decorator

    def __get_kebab_and_unique_name(self, name: str) -> tuple[str, str]:
        kebab_name = _SPECIAL_CHARS_RE.sub("", name).lower().replace(" ", "-")

        if kebab_name in self.key_repeat_count:
            number = self.key_repeat_count[kebab_name]
            self.key_repeat_count[kebab_name] += 1
            kebab_name = f"{kebab_name}-{number}"
        else:
            self.key_repeat_count[kebab_name] = 1

        return kebab_name, f"{kebab_name}-{uuid.uuid4()}"

    def table(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Table(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            id=kebab_name,
            is_hidden=is_hidden,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/table/{kebab_name}", name=unique_name, description=description
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
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Stat(
            function_name=unique_name,
            method="get",
            color=color,
            icon=icon,
            name=name,
            description=description,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/stat/{kebab_name}", name=unique_name, description=description
            ),
        )

    def markdown(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Markdown(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            id=kebab_name,
        )
        self.state.append(item)

        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/markdown/{kebab_name}",
                name=unique_name,
                description=description,
            ),
        )

    def action_post(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="post",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.post(
                f"/action/{kebab_name}", name=unique_name, description=description
            ),
        )

    def action_get(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/action/{kebab_name}", name=unique_name, description=description
            ),
        )

    def action_put(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="put",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.put(
                f"/action/{kebab_name}", name=unique_name, description=description
            ),
        )

    def action_patch(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="patch",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.patch(
                f"/action/{kebab_name}", name=unique_name, description=description
            ),
        )

    def action_delete(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="delete",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.delete(
                f"/action/{kebab_name}", name=unique_name, description=description
            ),
        )

    def form_post(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="post",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.post(
                f"/form/{kebab_name}", name=unique_name, description=description
            ),
        )

    def form_put(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="put",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.put(
                f"/form/{kebab_name}", name=unique_name, description=description
            ),
        )

    def form_patch(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="patch",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.patch(
                f"/form/{kebab_name}", name=unique_name, description=description
            ),
        )

    def form_delete(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hidden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="delete",
            name=name,
            description=description,
            is_hidden=is_hidden,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.delete(
                f"/form/{kebab_name}", name=unique_name, description=description
            ),
        )

    def area_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = AreaChart(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/area-chart/{kebab_name}", name=unique_name, description=description
            ),
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
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = BarChart(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            id=kebab_name,
            icon=icon,
            color=color,
            caption_description=caption_description,
            caption=caption,
            caption_icon=caption_icon,
            config=config,
            data_key=data_key,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/bar-chart/{kebab_name}", name=unique_name, description=description
            ),
        )

    def line_chart(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = LineChart(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            id=kebab_name,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/line-chart/{kebab_name}", name=unique_name, description=description
            ),
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
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = PieChart(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            id=kebab_name,
            config=config,
            icon=icon,
            name_key=name_key,
            value_key=value_key,
            color=color,
            caption=caption,
            caption_description=caption_description,
            caption_icon=caption_icon,
        )
        self.state.append(item)
        return self._wrap_user_handler(
            item,
            self.router.get(
                f"/pie-chart/{kebab_name}", name=unique_name, description=description
            ),
        )
