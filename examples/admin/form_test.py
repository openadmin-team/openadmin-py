# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import date, datetime
from enum import Enum, StrEnum
from typing import Literal

from fastapi import UploadFile

from openadmin import spec
from openadmin.fastapi import AdminPage

page = AdminPage("Test forms", icon="test-tube")


class Methods(Enum):
    GET = "GET"
    POST = "POST"


class MethodsStr(StrEnum):
    GET = "GET"
    POST = "POST"


@page.form(
    "Test all fields", 
    method="post", 
    icon="university", 
    color="green",
    fields={
        'string': {'icon': 'type', 'color': 'blue'},
        'int': {'icon': 'hash', 'color': 'indigo'},
        'float': {'icon': 'binary', 'color': 'violet'},
        'date': {'icon': 'calendar-days', 'color': 'purple'},
        'dates': {'icon': 'calendar', 'color': 'fuchsia'},
        'bool': {'icon': 'toggle-left', 'color': 'pink'},
        'list_of_strings': {'icon': 'list', 'color': 'rose'},
        'list_of_ints': {'icon': 'list-ordered', 'color': 'red'},
        'file': {'icon': 'file-up', 'color': 'orange'},
        'files': {'icon': 'files', 'color': 'amber'},
        'rich_text': {'icon': 'pilcrow', 'color': 'yellow', 'style': 'rich-text'},
        'literals': {'icon': 'list-filter', 'color': 'lime'},
        'enum': {'icon': 'tag', 'color': 'green'},
        'str_enum': {'icon': 'tags', 'color': 'emerald'},
        'list_literals': {'icon': 'list-checks', 'color': 'teal'},
        'list_enum': {'icon': 'layers', 'color': 'cyan'},
        'list_str_enum': {'icon': 'list-tree', 'color': 'sky'},
    }
)
def get_info(
    string: str,
    int: int,
    float: float,
    date: list[datetime],
    dates: list[date],
    bool: bool,
    list_of_strings: list[str],
    list_of_ints: list[int],
    file: UploadFile,
    files: list[UploadFile],
    rich_text: str,
    literals: Literal["get", "post"],
    enum: Methods,
    str_enum: MethodsStr,
    list_literals: list[Literal["get", "post"]],
    list_enum: list[Methods],
    list_str_enum: list[MethodsStr],
) -> spec.Form:
    return {
        "toast": f"All good ! {rich_text=} {list_literals=} {list_str_enum=} {list_enum=} {enum=} {literals=} {str_enum} {string=} {int=} {float=} {date=} {dates=} {bool=} {list_of_ints=} {list_of_strings=} {file.filename=} {len(files)=}"
    }
