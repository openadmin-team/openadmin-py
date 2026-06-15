# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage("User Management", description="CRUD Users")


@page.stat("Active users")
async def get_active_users():
    return 2


@page.stat("Banned users")
async def get_banned_users():
    return 5


@page.table("Users")
async def get_users():
    return [{"id": 2}]
