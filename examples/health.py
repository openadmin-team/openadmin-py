# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage("Health", description="System health and infrastructure metrics")


@page.stat("API uptime (%)")
async def get_api_uptime():
    return 99.97


@page.stat("Avg response time (ms)")
async def get_avg_response_time():
    return 84


@page.stat("Open incidents")
async def get_open_incidents():
    return 0


@page.area_chart("Response time over 24h")
async def get_response_time_24h():
    return [
        {"hour": "00:00", "ms": 72},
        {"hour": "03:00", "ms": 65},
        {"hour": "06:00", "ms": 70},
        {"hour": "09:00", "ms": 110},
        {"hour": "12:00", "ms": 98},
        {"hour": "15:00", "ms": 105},
        {"hour": "18:00", "ms": 92},
        {"hour": "21:00", "ms": 78},
    ]


@page.line_chart("Error rate over 7 days")
async def get_error_rate_7d():
    return [
        {"day": "Mon", "rate": 0.12},
        {"day": "Tue", "rate": 0.09},
        {"day": "Wed", "rate": 0.15},
        {"day": "Thu", "rate": 0.08},
        {"day": "Fri", "rate": 0.11},
        {"day": "Sat", "rate": 0.07},
        {"day": "Sun", "rate": 0.06},
    ]


@page.bar_chart("Requests per service")
async def get_requests_per_service():
    return [
        {"service": "auth", "requests": 42100},
        {"service": "api", "requests": 318400},
        {"service": "media", "requests": 95200},
        {"service": "notifications", "requests": 28700},
    ]


@page.table("Recent incidents")
async def get_recent_incidents():
    return [
        {
            "id": 1,
            "title": "DB slow queries",
            "severity": "warning",
            "resolved": True,
            "at": "2026-06-10T14:00Z",
        },
        {
            "id": 2,
            "title": "CDN outage",
            "severity": "critical",
            "resolved": True,
            "at": "2026-05-28T03:00Z",
        },
    ]


@page.action_post(
    "Run health check", description="Trigger a full system health check now"
)
async def run_health_check():
    return {"status": "ok", "checks": 12, "passed": 12}
