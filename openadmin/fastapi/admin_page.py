# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import uuid
from collections.abc import Callable

from fastapi import APIRouter, FastAPI
from openadmin import spec

from . import types
from .utils import extract_params


class AdminPage:
    def __init__(
        self,
        name: str,
        *,
        description: str | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.state: list[types.Component] = []
        self.router = APIRouter(prefix=f"/{name.lower().replace(' ', '-')}")
        self.key_repeat_count: dict[str, int] = {}

    def get_page_spec(self, app: FastAPI) -> spec.Page:
        components: list[spec.Component] = []

        for item in self.state:
            url = app.url_path_for(item.function_name)
            query, body, form = (
                extract_params(item.func) if item.func else (None, None, None)
            )

            if isinstance(item, types.Stat):
                components.append(
                    spec.Stat(
                        type="stat",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, types.Table):
                components.append(
                    spec.Table(
                        type="table",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                        body=body,
                        form=form,
                    )
                )
            elif isinstance(item, types.AreaChart):
                components.append(
                    spec.AreaChart(
                        type="area-chart",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, types.BarChart):
                components.append(
                    spec.BarChart(
                        type="bar-chart",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, types.LineChart):
                components.append(
                    spec.LineChart(
                        type="line-chart",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, types.PieChart):
                components.append(
                    spec.PieChart(
                        type="pie-chart",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        query=query,
                    )
                )
            elif isinstance(item, types.Action):
                components.append(
                    spec.Action(
                        type="action",
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
            elif isinstance(item, types.Form):
                components.append(
                    spec.Form(
                        type="form",
                        name=item.name,
                        description=item.description,
                        method=item.method,
                        url=url,
                        is_hiden=item.is_hiden,
                        query=query,
                        body=body,
                        form=form,
                    )
                )

        return spec.Page(
            name=self.name,
            description=self.description,
            components=components,
        )

    def _wrap(self, item: types.Component, fastapi_decorator) -> Callable:
        def decorator(func: Callable) -> Callable:
            item.func = func
            return fastapi_decorator(func)

        return decorator

    def __get_kebab_and_unique_name(self, name: str) -> tuple[str, str]:
        kebab_name = name.lower().replace(" ", "-")

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
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Table(
            function_name=unique_name, method="get", name=name, description=description
        )
        self.state.append(item)
        return self._wrap(
            item,
            self.router.get(
                f"/table/{kebab_name}", name=unique_name, description=description
            ),
        )

    def stat(
        self,
        name: str,
        *,
        description: str | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Stat(
            function_name=unique_name, method="get", name=name, description=description
        )
        self.state.append(item)
        return self._wrap(
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
    ): ...

    def action_post(
        self,
        name: str,
        *,
        description: str | None = None,
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Action(
            function_name=unique_name,
            method="post",
            name=name,
            description=description,
            is_hidden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Action(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            is_hidden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Action(
            function_name=unique_name,
            method="put",
            name=name,
            description=description,
            is_hidden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Action(
            function_name=unique_name,
            method="patch",
            name=name,
            description=description,
            is_hidden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Action(
            function_name=unique_name,
            method="delete",
            name=name,
            description=description,
            is_hidden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Form(
            function_name=unique_name,
            method="post",
            name=name,
            description=description,
            is_hiden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Form(
            function_name=unique_name,
            method="put",
            name=name,
            description=description,
            is_hiden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Form(
            function_name=unique_name,
            method="patch",
            name=name,
            description=description,
            is_hiden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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
        is_hiden: bool = False,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.Form(
            function_name=unique_name,
            method="delete",
            name=name,
            description=description,
            is_hiden=is_hiden,
        )
        self.state.append(item)
        return self._wrap(
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

        item = types.AreaChart(
            function_name=unique_name, method="get", name=name, description=description
        )
        self.state.append(item)
        return self._wrap(
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
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.BarChart(
            function_name=unique_name, method="get", name=name, description=description
        )
        self.state.append(item)
        return self._wrap(
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

        item = types.LineChart(
            function_name=unique_name, method="get", name=name, description=description
        )
        self.state.append(item)
        return self._wrap(
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
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = types.PieChart(
            function_name=unique_name, method="get", name=name, description=description
        )
        self.state.append(item)
        return self._wrap(
            item,
            self.router.get(
                f"/pie-chart/{kebab_name}", name=unique_name, description=description
            ),
        )
