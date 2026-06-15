# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from openadmin.fastapi import AdminPanel

from . import (
    activity_log,
    audit_log,
    comments,
    health,
    media,
    posts,
    roles,
    settings,
    user,
    user_analytics,
)

panel = AdminPanel("Cool Admin Panel")
app = FastAPI()

panel.section(
    "Users",
    pages=[
        user.page,
        user_analytics.page,
        roles.page,
        activity_log.page,
    ],
)

panel.section(
    "Content",
    pages=[
        posts.page,
        comments.page,
        media.page,
    ],
)

panel.section(
    "System",
    pages=[
        settings.page,
        audit_log.page,
        health.page,
    ],
)

panel.mount_to(app)
