# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from fastapi import UploadFile
from openadmin import spec
from openadmin.fastapi import AdminPage
from typing import Literal
from enum import Enum, StrEnum

page = AdminPage("Test forms", icon="test-tube")

class Methods(Enum):
    GET = "GET"
    POST = "POST"

class MethodsStr(StrEnum):
    GET = "GET"
    POST = "POST"

@page.form("Test all fields", method="post", icon="university", color="green")
def get_info(
    string: str,
    int: int,
    float: float,
    date: datetime,
    bool: bool,
    list_of_strings: list[str],
    list_of_ints: list[int],
    file: UploadFile,
    files: list[UploadFile],
    literals: Literal['get', 'post'],
    enum: Methods,
    str_enum: MethodsStr,
) -> spec.Form:
    return {
        "toast": f"All good ! {string=} {int=} {float=} {date=} {bool=} {list_of_ints=} {list_of_strings=} {file.filename=} {len(files)=}"
    }
