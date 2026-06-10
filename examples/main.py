# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel
from openadmin.sqlalchemy import SQLAlchemyPanelPlugin

from . import users
from .lifespan import lifespan

app = FastAPI(lifespan=lifespan)
admin_panel = AdminPanel(
    plugins=[SQLAlchemyPanelPlugin()],
)

admin_panel.include_page(users.page, tags=["Users"])

app.mount("/admin", admin_panel)
