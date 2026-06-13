# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from openadmin.fastapi import AdminPage

page = AdminPage("Welcome to admin")


@page.markdown("Overview")
async def overview() -> str:
    return """
# Welcome to the Admin Panel

Use this panel to monitor platform health, review recent activity, and manage your system.

## Quick Links
- **Users** — manage accounts, roles, and bans
- **Posts** — moderate content and track engagement
- **Tasks** — monitor user task completion across the platform

> All times are shown in UTC.
"""
