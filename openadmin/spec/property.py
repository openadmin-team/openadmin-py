# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from __future__ import annotations

from typing import NotRequired, TypedDict

from .property_type import PropertyType


class Property(TypedDict):
    name: str  # shown to user in admin panel
    alias: str  # goes to body or form for backend
    type: PropertyType
    is_required: bool
    properties: NotRequired[list[Property] | None]
