# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from openadmin import spec

from . import counter, utils


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
        self.components: list[spec.Component] = []

    @property
    def page(self) -> spec.Page:
        return {
            "id": f"{utils.kebab_name(self.name)}-{counter.inc('page')}",
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
        color: spec.Color | None = None,
        icon: spec.Icon | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Markdown(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            id=kebab_name,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="post",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="get",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="put",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="patch",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Action(
            function_name=unique_name,
            method="delete",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="post",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="put",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="patch",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
        icon: spec.Icon | None = None,
        color: spec.Color | None = None,
    ):
        kebab_name, unique_name = self.__get_kebab_and_unique_name(name)

        item = Form(
            function_name=unique_name,
            method="delete",
            name=name,
            description=description,
            is_hidden=is_hidden,
            icon=icon,
            color=color,
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
