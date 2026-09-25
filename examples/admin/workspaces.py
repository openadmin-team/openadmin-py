from openadmin.workspaces import AdminWorkspaces
from fastapi import Request

workspeaces = AdminWorkspaces()

@workspeaces.workspace()
async def current_workspace(req: Request): ...

@workspeaces.workspaces()
async def get_workspaces_list(req: Request): ...

@workspeaces.select_workspace()
async def select_workspace(req: Request): ...