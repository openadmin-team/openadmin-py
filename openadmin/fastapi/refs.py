# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable


def reference_table(func: Callable) -> str:
    return func.__openadmin_table_id__  # type: ignore


def reference_action(func: Callable) -> str:
    return func.__openadmin_action_id__  # type: ignore
