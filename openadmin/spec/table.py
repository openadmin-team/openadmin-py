# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, TypedDict

from pydantic import BaseModel, Field

from .http_methods import HttpMethod
from .property import Property


class TableComponent(BaseModel):
    type: Literal["table"]
    id: str
    name: str
    description: str | None
    url: str
    method: HttpMethod
    is_hidden: bool = False
    form: list[Property] | None = Field(None)
    body: list[Property] | None = Field(None)
    query: list[Property] | None = Field(None)


type TableData = (
    list[dict[str | Literal["__view__"], str | int | float | bool]] | object
)


class TableResponse(TypedDict):
    data: TableData
