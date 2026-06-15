# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel

from openadmin.fastapi import AdminPage

page = AdminPage("Roles & Permissions", description="Manage roles and access control")


@page.stat("Total roles")
async def get_total_roles():
    return 5


@page.table("Roles")
async def get_roles():
    return [
        {"id": 1, "name": "Admin", "users": 3, "permissions": 42},
        {"id": 2, "name": "Editor", "users": 12, "permissions": 18},
        {"id": 3, "name": "Viewer", "users": 87, "permissions": 6},
        {"id": 4, "name": "Moderator", "users": 5, "permissions": 24},
        {"id": 5, "name": "Support", "users": 9, "permissions": 12},
    ]


@page.table("Permissions")
async def get_permissions():
    return [
        {"id": 1, "name": "users:read", "roles": ["Admin", "Editor", "Viewer"]},
        {"id": 2, "name": "users:write", "roles": ["Admin", "Editor"]},
        {"id": 3, "name": "users:delete", "roles": ["Admin"]},
        {"id": 4, "name": "content:publish", "roles": ["Admin", "Editor", "Moderator"]},
    ]


class CreateRoleBody(BaseModel):
    name: str
    description: str


@page.form_post("Create role")
async def create_role(body: CreateRoleBody):
    return {"id": 6, "name": body.name}


class AssignRoleBody(BaseModel):
    user_id: int
    role_id: int


@page.form_patch("Assign role to user")
async def assign_role(body: AssignRoleBody):
    return {"user_id": body.user_id, "role_id": body.role_id}


class DeleteRoleBody(BaseModel):
    id: int


@page.form_delete("Delete role", is_hiden=True)
async def delete_role(body: DeleteRoleBody):
    return {"deleted": body.id}
