# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage("Activity Log", description="Recent user actions and events")


@page.stat("Events today")
async def get_events_today():
    return 348


@page.stat("Failed logins today")
async def get_failed_logins_today():
    return 12


@page.bar_chart("Events per hour")
async def get_events_per_hour():
    return [
        {"hour": "00:00", "events": 14},
        {"hour": "06:00", "events": 38},
        {"hour": "09:00", "events": 120},
        {"hour": "12:00", "events": 95},
        {"hour": "15:00", "events": 110},
        {"hour": "18:00", "events": 72},
        {"hour": "21:00", "events": 31},
    ]


@page.table("Recent events")
async def get_recent_events():
    return [
        {
            "id": 1,
            "user": "alice",
            "action": "login",
            "ip": "1.2.3.4",
            "at": "2026-06-16T08:01Z",
        },
        {
            "id": 2,
            "user": "bob",
            "action": "update_profile",
            "ip": "5.6.7.8",
            "at": "2026-06-16T08:05Z",
        },
        {
            "id": 3,
            "user": "alice",
            "action": "delete_post",
            "ip": "1.2.3.4",
            "at": "2026-06-16T08:12Z",
        },
        {
            "id": 4,
            "user": "carol",
            "action": "login_failed",
            "ip": "9.0.1.2",
            "at": "2026-06-16T08:15Z",
        },
    ]


@page.action_delete(
    "Clear old logs", description="Delete events older than 90 days", is_hiden=True
)
async def clear_old_logs():
    return {"deleted": 1204}
