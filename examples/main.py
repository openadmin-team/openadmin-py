# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel
from openadmin.sqlalchemy import SQLAlchemyPanelPlugin

from .lib import database
from .lib.lifespan import lifespan
from .routes import analitics, users, welcome_admin

app = FastAPI(lifespan=lifespan)
admin_panel = AdminPanel(
    plugins=[SQLAlchemyPanelPlugin(async_engine_callback=database.get_async_engine)],
)

admin_panel.include_page(welcome_admin.page)
admin_panel.include_page(users.page, tags=["Users"])
admin_panel.include_page(analitics.page, tags=["Analitics"])

app.mount("/admin", admin_panel)
