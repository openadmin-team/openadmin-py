# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable


def reference(func: Callable) -> str:
    return func.__openadmin_id__  # type: ignore
