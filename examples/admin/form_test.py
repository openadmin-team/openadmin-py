# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import date as date_type
from datetime import datetime

from openadmin import spec
from openadmin.fastapi import AdminPage

page = AdminPage("Test forms", icon="test-tube")


@page.form("Test all fields", method="post", icon="university", color="green")
def get_info(
    string: str,
    int: int,
    float: float,
    date: datetime,
    day: date_type,
    bool: bool,
    list_of_strings: list[str],
    list_of_ints: list[int],
) -> spec.Form:
    return {
        "toast": f"All good ! {string=} {int=} {float=} {date=} {day=} {bool=} {list_of_ints=} {list_of_strings=}"
    }
