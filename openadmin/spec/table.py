# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from pydantic import BaseModel, Field

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class TableComponent(BaseModel):
    type: Literal["table"]
    id: str
    name: str
    description: str | None
    url: str
    icon: Icon | None
    color: Color | None
    method: HttpMethod
    is_hidden: bool
    form: list[Property] | None = Field(None)
    body: list[Property] | None = Field(None)
    query: list[Property] | None = Field(None)


type TableData = (
    list[dict[str | Literal["__view__"], str | int | float | bool]] | object
)


class TableResponse(TypedDict):
    data: TableData
    icon: NotRequired[Icon]
    color: NotRequired[Color]


type Table = TableData | TableResponse
