# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel

panel = AdminPanel("Cool Admin Panel")
app = FastAPI()

app.mount("/admin", panel.app)
