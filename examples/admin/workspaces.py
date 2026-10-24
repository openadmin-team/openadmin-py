# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from urllib.parse import quote

from fastapi import HTTPException, Request

from openadmin.workspaces import AdminWorkspaces, Workspace

SESSION_KEY = 'workspace_id'

admin_workspaces = AdminWorkspaces()


def avatar(seed: str) -> str:
    return f'https://api.dicebear.com/9.x/shapes/svg?seed={quote(seed)}'


workspaces: list[Workspace] = [
    {'id': 'default', 'name': 'Default', 'avatar': avatar('default'), 'description': 'Main workspace'},
    {'id': 'marketing', 'name': 'Marketing', 'avatar': avatar('marketing'), 'description': 'Campaigns and content'},
    {'id': 'engineering', 'name': 'Engineering', 'avatar': avatar('engineering'), 'description': 'Product and infra'},
    {'id': 'support', 'name': 'Support', 'avatar': avatar('support'), 'description': 'Tickets and customer success'},
    {'id': 'finance', 'name': 'Finance', 'avatar': avatar('finance'), 'description': 'Billing and reporting'},
    {'id': 'staging', 'name': 'Staging', 'avatar': avatar('staging'), 'description': 'Sandbox for testing changes'},
]


def find_workspace(id: str) -> Workspace | None:
    return next((w for w in workspaces if w['id'] == id), None)


@admin_workspaces.workspace()
async def get_workspace(req: Request) -> Workspace:
    return find_workspace(req.session.get(SESSION_KEY, '')) or workspaces[0]


@admin_workspaces.workspaces()
async def get_workspaces(req: Request) -> list[Workspace]:
    return workspaces


@admin_workspaces.select_workspace()
async def select_workspace(req: Request, id: str) -> None:
    if find_workspace(id) is None:
        raise HTTPException(status_code=404, detail=f'Workspace {id!r} not found')
    req.session[SESSION_KEY] = id