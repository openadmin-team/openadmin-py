# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal

from pydantic import BaseModel

from .http_methods import HttpMethod


class Action(BaseModel):
    type: Literal["action"]
    name: str
    description: str | None
    url: str
    method: HttpMethod
    is_hidden: bool
