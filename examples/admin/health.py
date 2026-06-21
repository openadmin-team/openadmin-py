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
