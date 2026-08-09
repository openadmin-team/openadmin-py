# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from typing import TypedDict

from .icons import Icon
from .page import Page


class Section(TypedDict):
    id: str
    name: str
    description: str | None
    icon: Icon | None
    pages: list[Page]
