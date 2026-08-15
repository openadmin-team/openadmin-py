# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Iterable
from typing import Any, Literal, NotRequired

from typing_extensions import TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .json_schema import JsonSchema

type ColumnStyle = Literal["avatar", "image", "badge", "link"]


class ColumnConfigValue(TypedDict):
    style: NotRequired[ColumnStyle]
    label: NotRequired[str]
    icon: NotRequired[Icon]
    color: NotRequired[Color]


class ActionConfig(TypedDict):
    action: str
    label: NotRequired[str]
    icon: NotRequired[Icon]
    color: NotRequired[Color]

    query: dict[str, Any]
    body: dict[str, Any]
    form: dict[str, Any]


class TableComponent(TypedDict):
    type: Literal["table"]
    id: str
    name: str
    description: str | None
    columns: dict[str, ColumnConfigValue] | None
    icon: Icon | None
    color: Color | None
    method: HttpMethod
    is_hidden: bool
    refresh: int | None
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


TableData = Iterable[
    TypedDict(
        "TableRow",
        {
            "__view__": str | int | float | bool | None,
            "__actions__": list[ActionConfig],
            "__style__": ColumnStyle | None,
        },
        extra_items=str | int | float | bool | None,
    )
    | object
]


class TableResponse(TypedDict):
    data: TableData
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    refresh: NotRequired[int | None]


type Table = TableData | TableResponse
