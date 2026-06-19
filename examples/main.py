# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel

from . import (
    health,
    users,
)

panel = AdminPanel("Cool Admin Panel")
app = FastAPI()

panel.section(
    "Users",
    pages=[
        users.page,
    ],
)

panel.section(
    "System",
    pages=[
        health.page,
    ],
)

panel.mount_to(app)
