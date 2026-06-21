# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage("Health", description="System health and infrastructure metrics")


@page.stat("API Uptime (%)")
async def get_api_uptime() -> float:
    return 99.97


@page.stat("Avg Response Time (ms)")
async def get_avg_response_time() -> int:
    return 84


@page.stat("Active Connections")
async def get_active_connections() -> int:
    return 12


@page.line_chart(
    "Response Time (last 24h)",
    description="Simulated p95 latency over the past 24 hours",
)
async def get_response_time_chart():
    hours = [f"{h:02d}:00" for h in range(24)]
    values = [
        72,
        68,
        65,
        63,
        61,
        60,
        66,
        78,
        95,
        110,
        105,
        98,
        101,
        99,
        97,
        102,
        108,
        115,
        112,
        104,
        98,
        91,
        84,
        79,
    ]
    return [{"label": label, "value": value} for label, value in zip(hours, values)]


@page.markdown("Health Status")
async def get_health_status() -> str:
    return """# System Health

All services are operating normally.

| Service        | Status  | Latency |
|----------------|---------|---------|
| API            | ✅ Up   | 84 ms   |
| Database       | ✅ Up   | 3 ms    |
| Cache          | ✅ Up   | 1 ms    |
| Queue          | ✅ Up   | 12 ms   |

Last checked: just now.
"""
