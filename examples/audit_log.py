# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage("Audit Log", description="Admin actions and security events")


@page.stat("Events this week")
async def get_events_this_week():
    return 94


@page.stat("Unique actors")
async def get_unique_actors():
    return 11


@page.bar_chart("Admin actions per day")
async def get_actions_per_day():
    return [
        {"day": "Mon", "actions": 8},
        {"day": "Tue", "actions": 15},
        {"day": "Wed", "actions": 12},
        {"day": "Thu", "actions": 21},
        {"day": "Fri", "actions": 18},
        {"day": "Sat", "actions": 5},
        {"day": "Sun", "actions": 3},
    ]


@page.table("Audit events")
async def get_audit_events():
    return [
        {
            "id": 1,
            "actor": "admin",
            "action": "delete_user",
            "target": "user:42",
            "at": "2026-06-16T09:00Z",
        },
        {
            "id": 2,
            "actor": "admin",
            "action": "update_settings",
            "target": "settings:site_name",
            "at": "2026-06-15T14:30Z",
        },
        {
            "id": 3,
            "actor": "mod1",
            "action": "ban_user",
            "target": "user:17",
            "at": "2026-06-15T11:00Z",
        },
        {
            "id": 4,
            "actor": "admin",
            "action": "create_role",
            "target": "role:6",
            "at": "2026-06-14T16:45Z",
        },
    ]


@page.action_get("Export audit log", description="Download full audit log as CSV")
async def export_audit_log():
    return {"url": "/exports/audit.csv"}


@page.action_delete(
    "Archive old events",
    description="Move events older than 180 days to cold storage",
    is_hiden=True,
)
async def archive_old_events():
    return {"archived": 3820}
