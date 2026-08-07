# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import NotRequired, TypedDict


class Error(TypedDict):
    message: str
    code: NotRequired[str]
