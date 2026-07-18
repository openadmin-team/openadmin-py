# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from pydantic import BaseModel, Field

from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class Stat(BaseModel):
    type: Literal["stat"]
    id: str
    name: str
    description: str | None
    url: str
    method: HttpMethod
    query: list[Property] | None = Field(None)


type StatValue = str | int | float | bool | None


class StatResponse(TypedDict):
    value: StatValue
    icon: NotRequired[Icon]
