# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel

from .component import Component
from .icons import Icon


class Page(BaseModel):
    id: str
    name: str
    description: str | None
    icon: Icon | None
    components: List[Component]
