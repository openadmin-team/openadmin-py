# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .json_schema import JsonSchema
from .error import Error


class TableComponent(TypedDict):
    type: Literal["table"]
    id: str
    name: str
    description: str | None
    icon: Icon | None
    color: Color | None
    method: HttpMethod
    is_hidden: bool
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


type TableData = (
    list[dict[str | Literal["__view__"], str | int | float | bool | None]] | object
)


class TableResponse(TypedDict):
    data: TableData
    icon: NotRequired[Icon]
    color: NotRequired[Color]


type Table = TableData | TableResponse | Error
