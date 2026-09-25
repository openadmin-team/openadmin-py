# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import Request

from openadmin.workspaces import AdminWorkspaces, Workspace

workspeaces = AdminWorkspaces()


@workspeaces.workspace()
async def current_workspace(req: Request) -> Workspace:
    return {"id": "1", "avatar": "", "name": "a"}


@workspeaces.workspaces()
async def get_workspaces_list(req: Request) -> list[Workspace]:
    return [{"id": "1", "avatar": "", "name": "a"}]


@workspeaces.select_workspace()
async def select_workspace(req: Request): ...
