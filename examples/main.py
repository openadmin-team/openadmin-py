# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel

from . import user

panel = AdminPanel("Cool Admin Panel")
app = FastAPI()

panel.section("Users", pages=[user.page])

panel.mount_to(app)
