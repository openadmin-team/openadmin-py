# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import inspect
from collections.abc import Awaitable, Callable

from fastapi import Depends, Request


def create_authenticate_dep(
    auth_func: Callable[[Request], None | Awaitable[None]],
):
    async def _(req: Request) -> None:
        result = auth_func(req)
        if inspect.isawaitable(result):
            await result

    return Depends(_)
