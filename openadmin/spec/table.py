# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal

from pydantic import BaseModel, Field

from .http_methods import HttpMethod
from .property import Property


class Table(BaseModel):
    type: Literal["table"]
    id: str
    name: str
    description: str | None
    url: str
    method: HttpMethod
    form: list[Property] | None = Field(None)
    body: list[Property] | None = Field(None)
    query: list[Property] | None = Field(None)
