# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel

from .admin import (
    analytics,
    authors,
    books,
    genres,
    health,
    overview,
    publishers,
    reports,
    tags,
)
from .lib import lifespan

app = FastAPI(lifespan=lifespan.lifespan)
admin_panel = AdminPanel(
    "Book Library Admin", description="Manage and explore the book catalog"
)

admin_panel.section("Library", pages=[books.page, authors.page, publishers.page])
admin_panel.section("Catalog", pages=[genres.page, tags.page, analytics.page])
admin_panel.section("System", pages=[health.page, reports.page, overview.page])

admin_panel.mount_to(app)
