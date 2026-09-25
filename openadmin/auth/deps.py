# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Awaitable, Callable

from fastapi import Depends, Request


def create_authenticate_dep(
    auth_func: Callable[[Request], None | Awaitable[None]],
):
    def _(req: Request):
        auth_func(req)

    return Depends(_)
