# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .property import Property


class MarkdownComponent(TypedDict):
    type: Literal["markdown"]
    id: str
    name: str
    description: str | None
    color: Color | None
    icon: Icon | None
    method: HttpMethod
    query: NotRequired[list[Property] | None]


type MarkdownContent = str


class MarkdownResponse(TypedDict):
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    content: MarkdownContent


type Markdown = MarkdownContent | MarkdownResponse
