# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Literal

from pydantic import BaseModel, Field

from .http_methods import HttpMethod
from .property import Property


class Table(BaseModel):
    type: Literal["table"]
    name: str
    description: str | None
    url: str
    method: HttpMethod
    form: List[Property] | None = Field(None)
    body: List[Property] | None = Field(None)
    query: List[Property] | None = Field(None)
