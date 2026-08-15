# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Literal, NotRequired, TypedDict

from .colors import Color
from .http_methods import HttpMethod
from .icons import Icon
from .json_schema import JsonSchema


class MarkdownComponent(TypedDict):
    type: Literal["markdown"]
    id: str
    name: str
    description: str | None
    color: Color | None
    icon: Icon | None
    refresh: int | None
    method: HttpMethod
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None


type MarkdownContent = str


class MarkdownResponse(TypedDict):
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    refresh: NotRequired[int | None]
    content: MarkdownContent


type Markdown = MarkdownContent | MarkdownResponse
