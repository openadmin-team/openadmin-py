# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from openadmin.fastapi import AdminPanel

from .admin import (
    analytics,
    auth,
    authors,
    books,
    control_panel,
    docs,
    form_test,
    genres,
    health,
    overview,
    publishers,
    reports,
    tags,
    weekdays,
)
from .lib import lifespan

app = FastAPI(lifespan=lifespan.lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="test")

admin_panel = AdminPanel(
    "Book Library Admin",
    description="Manage and explore the book catalog",
    auth=auth.auth,
)

admin_panel.section(
    "Docs",
    icon="download-cloud",
    pages=[
        docs.page,
    ],
)

admin_panel.section(
    "Library", icon="library", pages=[books.page, authors.page, publishers.page]
)
admin_panel.section(
    "Catalog", icon="library-big", pages=[genres.page, tags.page, analytics.page]
)
admin_panel.section(
    "System",
    icon="server",
    pages=[health.page, reports.page, overview.page, control_panel.page],
)
admin_panel.section(
    "Weekdays", icon="calendar-days", pages=[weekdays.page, form_test.page]
)

app.mount("/admin", admin_panel.app, name="admin_panel")
