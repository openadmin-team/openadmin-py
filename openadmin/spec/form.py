# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal

from pydantic import BaseModel, Field

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class Form(BaseModel):
    type: Literal["form"]
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
