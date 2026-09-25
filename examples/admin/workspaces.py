# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import Request

from openadmin.workspaces import AdminWorkspaces

workspeaces = AdminWorkspaces()


@workspeaces.workspace()
async def current_workspace(req: Request):
    return 1


@workspeaces.workspaces()
async def get_workspaces_list(req: Request): ...


@workspeaces.select_workspace()
async def select_workspace(req: Request): ...
