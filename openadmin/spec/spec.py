# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from typing import NotRequired, TypedDict

from .section import Section


class Spec(TypedDict):
    version: str
    name: str
    description: NotRequired[str | None]
    sections: list[Section]
