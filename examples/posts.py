# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel

from openadmin.fastapi import AdminPage

page = AdminPage("Posts", description="Manage blog posts and articles")


@page.stat("Published posts")
async def get_published_posts():
    return 314


@page.stat("Drafts")
async def get_drafts():
    return 27


@page.area_chart("Posts published over time")
async def get_posts_over_time():
    return [
        {"month": "Jan", "value": 22},
        {"month": "Feb", "value": 31},
        {"month": "Mar", "value": 28},
        {"month": "Apr", "value": 40},
        {"month": "May", "value": 35},
    ]


@page.table("All posts")
async def get_all_posts():
    return [
        {
            "id": 1,
            "title": "Getting started",
            "author": "alice",
            "status": "published",
            "views": 1200,
        },
        {
            "id": 2,
            "title": "Advanced tips",
            "author": "bob",
            "status": "published",
            "views": 840,
        },
        {
            "id": 3,
            "title": "Draft post",
            "author": "carol",
            "status": "draft",
            "views": 0,
        },
    ]


@page.action_post("Publish all drafts", description="Publish every draft post at once")
async def publish_all_drafts():
    return {"published": 27}


@page.action_get("Export posts", description="Download all posts as JSON")
async def export_posts():
    return {"url": "/exports/posts.json"}


class CreatePostBody(BaseModel):
    title: str
    content: str
    author_id: int


@page.form_post("Create post")
async def create_post(body: CreatePostBody):
    return {"id": 315, "title": body.title}


class UpdatePostBody(BaseModel):
    id: int
    title: str
    content: str


@page.form_patch("Edit post")
async def edit_post(body: UpdatePostBody):
    return {"id": body.id, "title": body.title}


class DeletePostBody(BaseModel):
    id: int


@page.form_delete("Delete post", is_hiden=True)
async def delete_post(body: DeletePostBody):
    return {"deleted": body.id}
