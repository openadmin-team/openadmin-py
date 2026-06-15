# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel

from openadmin.fastapi import AdminPage

page = AdminPage("Media", description="Manage uploaded images and files")


@page.stat("Total files")
async def get_total_files():
    return 5632


@page.stat("Storage used (MB)")
async def get_storage_used():
    return 8741


@page.pie_chart("Files by type")
async def get_files_by_type():
    return [
        {"label": "Images", "value": 4210},
        {"label": "Documents", "value": 890},
        {"label": "Videos", "value": 312},
        {"label": "Other", "value": 220},
    ]


@page.table("Recent uploads")
async def get_recent_uploads():
    return [
        {
            "id": 1,
            "name": "hero.png",
            "type": "image",
            "size_kb": 142,
            "uploaded_by": "alice",
        },
        {
            "id": 2,
            "name": "report.pdf",
            "type": "document",
            "size_kb": 890,
            "uploaded_by": "bob",
        },
        {
            "id": 3,
            "name": "intro.mp4",
            "type": "video",
            "size_kb": 51200,
            "uploaded_by": "carol",
        },
    ]


class RenameFileBody(BaseModel):
    id: int
    name: str


@page.form_patch("Rename file")
async def rename_file(body: RenameFileBody):
    return {"id": body.id, "name": body.name}


class DeleteFileBody(BaseModel):
    id: int


@page.form_delete("Delete file", is_hiden=True)
async def delete_file(body: DeleteFileBody):
    return {"deleted": body.id}


@page.action_delete(
    "Purge unused files",
    description="Delete files not linked to any content",
    is_hiden=True,
)
async def purge_unused_files():
    return {"deleted": 204}
