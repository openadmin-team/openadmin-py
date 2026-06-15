# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage("User Analytics", description="Charts and trends for user activity")


@page.stat("Total users")
async def get_total_users():
    return 1247


@page.stat("New this month")
async def get_new_this_month():
    return 89


@page.area_chart("Signups over time")
async def get_signups_over_time():
    return [
        {"month": "Jan", "value": 54},
        {"month": "Feb", "value": 71},
        {"month": "Mar", "value": 63},
        {"month": "Apr", "value": 89},
        {"month": "May", "value": 102},
    ]


@page.line_chart("Daily active users")
async def get_daily_active_users():
    return [
        {"day": "Mon", "value": 320},
        {"day": "Tue", "value": 410},
        {"day": "Wed", "value": 390},
        {"day": "Thu", "value": 475},
        {"day": "Fri", "value": 360},
        {"day": "Sat", "value": 210},
        {"day": "Sun", "value": 180},
    ]


@page.bar_chart("Logins by country")
async def get_logins_by_country():
    return [
        {"country": "US", "logins": 530},
        {"country": "UK", "logins": 210},
        {"country": "DE", "logins": 175},
        {"country": "CA", "logins": 140},
        {"country": "AU", "logins": 95},
    ]


@page.pie_chart("Users by plan")
async def get_users_by_plan():
    return [
        {"label": "Free", "value": 890},
        {"label": "Pro", "value": 298},
        {"label": "Enterprise", "value": 59},
    ]
