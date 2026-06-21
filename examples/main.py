# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel

from .admin import health
from .lib import lifespan

app = FastAPI(lifespan=lifespan.lifespan)
admin_panel = AdminPanel("Awesome Admin panel")

admin_panel.section("System", pages=[health.page])

admin_panel.mount_to(app)
