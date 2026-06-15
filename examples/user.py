# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel

from openadmin.fastapi import AdminPage

page = AdminPage("User Management", description="CRUD Users")


# --- Stats ---


@page.stat("Active users")
async def get_active_users():
    return 42


@page.stat("Active users")
async def get_banned_users():
    return 3


# --- Table ---


@page.table("Users")
async def get_users():
    return [
        {
            "id": 1,
            "username": "alice",
            "email": "alice@example.com",
            "status": "active",
        },
        {"id": 2, "username": "bob", "email": "bob@example.com", "status": "banned"},
    ]


# --- Charts ---


@page.area_chart("Signups over time")
async def get_signups_over_time():
    return [
        {"date": "2026-01", "value": 12},
        {"date": "2026-02", "value": 27},
        {"date": "2026-03", "value": 19},
        {"date": "2026-04", "value": 35},
    ]


@page.bar_chart("Logins per day")
async def get_logins_per_day():
    return [
        {"day": "Mon", "logins": 80},
        {"day": "Tue", "logins": 95},
        {"day": "Wed", "logins": 70},
        {"day": "Thu", "logins": 110},
        {"day": "Fri", "logins": 60},
    ]


@page.line_chart("Revenue per month")
async def get_revenue_per_month():
    return [
        {"month": "Jan", "revenue": 1200},
        {"month": "Feb", "revenue": 1800},
        {"month": "Mar", "revenue": 1500},
        {"month": "Apr", "revenue": 2100},
    ]


@page.pie_chart("Users by status")
async def get_users_by_status():
    return [
        {"label": "Active", "value": 42},
        {"label": "Banned", "value": 3},
        {"label": "Pending", "value": 8},
    ]


# --- Actions ---


@page.action_post("Sync users", description="Pull latest users from external source")
async def sync_users():
    return {"synced": 5}


@page.action_get("Export CSV", description="Download users as CSV")
async def export_users_csv():
    return {"url": "/exports/users.csv"}


@page.action_put("Restore all banned", description="Lift all active bans")
async def restore_all_banned():
    return {"restored": 3}


@page.action_patch("Recalculate stats", description="Refresh cached stats")
async def recalculate_stats():
    return {"ok": True}


@page.action_delete(
    "Purge inactive users",
    description="Delete users inactive for 1 year",
    is_hiden=True,
)
async def purge_inactive_users():
    return {"deleted": 7}


# --- Forms ---


class CreateUserBody(BaseModel):
    username: str
    email: str
    password: str


@page.form_post("Create user")
async def create_user(body: CreateUserBody):
    return {"id": 99, "username": body.username}


class UpdateUserBody(BaseModel):
    id: int
    username: str
    email: str


@page.form_put("Replace user")
async def replace_user(body: UpdateUserBody):
    return {"id": body.id, "username": body.username}


class PatchUserBody(BaseModel):
    id: int
    email: str


@page.form_patch("Update user email")
async def update_user_email(body: PatchUserBody):
    return {"id": body.id, "email": body.email}


class DeleteUserBody(BaseModel):
    id: int


@page.form_delete("Delete user", is_hiden=True)
async def delete_user(body: DeleteUserBody):
    return {"deleted": body.id}
