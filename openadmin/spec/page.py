# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel

from .components import Component


class Page(BaseModel):
    name: str
    description: str | None
    components: List[Component]
