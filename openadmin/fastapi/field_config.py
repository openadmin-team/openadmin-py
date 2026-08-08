# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable
from typing import NotRequired, TypedDict

from openadmin import spec


class FieldConfig(TypedDict):
    reference: NotRequired[str | Callable | None]
    reference_field: NotRequired[str]
    icon: NotRequired[spec.Icon]
    color: NotRequired[spec.Color]
