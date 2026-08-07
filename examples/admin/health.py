# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage(
    "Health", icon="heart-pulse", description="System health and infrastructure metrics"
)


@page.stat(
    "API Uptime (%)",
    icon="check-circle",
    color="green",
    description="Percentage of successful API requests over the last 30 days",
)
async def get_api_uptime() -> float:
    return 99.97


@page.stat(
    "Avg Response Time (ms)",
    icon="gauge",
    color="blue",
    description="Average API response time across all endpoints",
)
async def get_avg_response_time() -> int:
    return 84


@page.stat(
    "Active Connections",
    icon="plug",
    color="violet",
    description="Current number of open client connections",
)
async def get_active_connections() -> int:
    return 12


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
