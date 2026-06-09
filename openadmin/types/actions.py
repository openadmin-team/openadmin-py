# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal

from pydantic import BaseModel, Field


class Action(BaseModel):
    color: str | Literal["danger", "warning", "info"]
    method: Literal["POST", "GET", "PUT", "PATCH", "DELETE"]
    url: str
    body: dict | None = Field(None)
