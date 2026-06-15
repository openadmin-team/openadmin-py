# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage

page = AdminPage("Comments", description="Moderate user comments")


@page.stat("Total comments")
async def get_total_comments():
    return 2841


@page.stat("Pending review")
async def get_pending_review():
    return 14


@page.pie_chart("Comments by status")
async def get_comments_by_status():
    return [
        {"label": "Approved", "value": 2680},
        {"label": "Pending", "value": 14},
        {"label": "Spam", "value": 147},
    ]


@page.table("Recent comments")
async def get_recent_comments():
    return [
        {
            "id": 1,
            "author": "alice",
            "post": "Getting started",
            "body": "Great article!",
            "status": "approved",
        },
        {
            "id": 2,
            "author": "unknown",
            "post": "Advanced tips",
            "body": "Buy cheap meds...",
            "status": "spam",
        },
        {
            "id": 3,
            "author": "dave",
            "post": "Getting started",
            "body": "Could you clarify step 3?",
            "status": "pending",
        },
    ]


@page.action_post(
    "Approve all pending", description="Approve every comment awaiting review"
)
async def approve_all_pending():
    return {"approved": 14}


@page.action_delete(
    "Delete all spam", description="Permanently remove all spam comments", is_hiden=True
)
async def delete_all_spam():
    return {"deleted": 147}
