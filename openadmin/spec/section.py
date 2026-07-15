# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel

from .components import Icon
from .page import Page


class Section(BaseModel):
    name: str
    description: str | None
    icon: Icon | None
    pages: List[Page]
