# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import UTC, datetime, timedelta
from random import randint
from time import sleep
from typing import Annotated

from fastapi import Body, Depends, Form, Query
from pydantic import BaseModel

from openadmin import spec
from openadmin.fastapi import AdminPage, reference_action
from openadmin.fastapi.deps import PageDep, SearchDep

page = AdminPage(
    "Control Panel",
    icon="settings",
    description="Every action/form parameter and response shape, demoed with example data",
)


def current_actor(
    actor: str = Query("system", description="Who is performing this operation"),
) -> str:
    return actor


ActorDep = Annotated[str, Depends(current_actor)]


# ---------------------------------------------------------------------------
# Actions — one per HTTP verb, each showing a different param source and a
# different Action response shape. Nothing here mutates real state.
# ---------------------------------------------------------------------------


@page.action(
    "Ping Service",
    method="get",
    description="Check whether a downstream service is reachable",
    icon="activity",
    color="green",
    is_hidden=False,
)
async def ping_service(
    target: str = Query("api", description="Service name to ping"),
) -> spec.Action:
    return {
        "icon": "activity",
        "color": "green",
        "toast": f"{target} responded in 12ms",
        "message": f"Pinged '{target}' — reachable (example response, nothing was contacted)",
    }


class NotificationBody(BaseModel):
    title: str
    body: str
    recipient: str | None = None


@page.action(
    "Send Test Notification",
    method="post",
    description="Send a one-off notification through the messaging provider",
    icon="send",
    color="blue",
)
async def send_test_notification(
    body: NotificationBody,
    actor: ActorDep,
    dry_run: bool = Query(True, description="Simulate without actually sending"),
) -> str:
    target = body.recipient or "all subscribers"
    verb = "Would send" if dry_run else "Sent"
    return (
        f"{verb} '{body.title}' to {target} (requested by {actor}) — "
        "example only, nothing was sent"
    )


@page.action(
    "Update Feature Flag",
    method="put",
    description="Flip a feature flag on or off for every user",
    icon="toggle-left",
    color="violet",
    is_hidden=True,
)
async def update_feature_flag(
    flag_name: str = Query(..., description="Flag key, e.g. new-dashboard"),
    enabled: bool = Query(..., description="New flag state"),
) -> spec.Action:
    return {
        "toast": f"{flag_name} -> {enabled}",
        "message": "Preview of the change below (example data, flag was not modified)",
        "table": [{"flag": flag_name, "previous": not enabled, "new": enabled}],
    }


@page.action(
    "Rotate API Key",
    method="patch",
    description="Issue a new API key and retire the previous one",
    icon="key",
    color="amber",
)
async def rotate_api_key(
    key_name: str = Form(..., description="Key to rotate"),
    expires_in_days: int = Form(30, description="Validity period for the new key"),
) -> spec.Action:
    return None


@page.action(
    "Purge Temp Files",
    method="delete",
    description="Delete temporary files older than a given age",
    icon="trash-2",
    color="red",
)
async def purge_temp_files(
    older_than_days: int = Query(7, ge=0, description="Age threshold in days"),
) -> spec.Action:
    return {
        "message": (
            f"Would delete files older than {older_than_days} days "
            "(example — nothing was purged)"
        )
    }


# ---------------------------------------------------------------------------
# Feature flags — a searchable table with a badge-styled status column and
# per-row Enable/Disable actions. Held in memory for the demo.
# ---------------------------------------------------------------------------


FEATURE_FLAGS: list[dict[str, str | bool]] = [
    {
        "name": "new-dashboard",
        "description": "Enables the redesigned analytics dashboard",
        "enabled": True,
        "created_by": "grace.hopper",
        "created_at": "2026-01-12T09:30:00Z",
        "last_changed_at": "2026-06-02T14:05:00Z",
    },
    {
        "name": "beta-search",
        "description": "Turns on the experimental full-text search backend",
        "enabled": False,
        "created_by": "alan.turing",
        "created_at": "2026-03-04T11:00:00Z",
        "last_changed_at": "2026-03-04T11:00:00Z",
    },
    {
        "name": "dark-mode-v2",
        "description": "Rolls out the refreshed dark theme palette",
        "enabled": True,
        "created_by": "ada.lovelace",
        "created_at": "2025-11-20T16:45:00Z",
        "last_changed_at": "2026-07-30T08:12:00Z",
    },
    {
        "name": "checkout-retry",
        "description": "Automatically retries failed checkout payment attempts",
        "enabled": False,
        "created_by": "margaret.hamilton",
        "created_at": "2026-05-08T13:20:00Z",
        "last_changed_at": "2026-05-15T09:40:00Z",
    },
    {
        "name": "notif-batching",
        "description": "Batches push notifications instead of sending one at a time",
        "enabled": True,
        "created_by": "grace.hopper",
        "created_at": "2025-09-02T10:15:00Z",
        "last_changed_at": "2026-04-11T17:30:00Z",
    },
    {
        "name": "ai-recommendations",
        "description": "Shows AI-generated product recommendations on the home feed",
        "enabled": False,
        "created_by": "katherine.johnson",
        "created_at": "2026-02-18T08:00:00Z",
        "last_changed_at": "2026-02-18T08:00:00Z",
    },
    {
        "name": "gdpr-export-v2",
        "description": "Uses the streaming exporter for user data download requests",
        "enabled": True,
        "created_by": "alan.turing",
        "created_at": "2025-12-01T09:00:00Z",
        "last_changed_at": "2026-07-05T12:45:00Z",
    },
    {
        "name": "multi-currency",
        "description": "Allows prices to be displayed in the shopper's local currency",
        "enabled": False,
        "created_by": "ada.lovelace",
        "created_at": "2026-04-22T15:10:00Z",
        "last_changed_at": "2026-04-22T15:10:00Z",
    },
    {
        "name": "lazy-image-loading",
        "description": "Defers off-screen image loading on catalog pages",
        "enabled": True,
        "created_by": "margaret.hamilton",
        "created_at": "2025-10-14T13:40:00Z",
        "last_changed_at": "2026-01-09T09:55:00Z",
    },
    {
        "name": "two-factor-required",
        "description": "Requires two-factor authentication for admin accounts",
        "enabled": True,
        "created_by": "grace.hopper",
        "created_at": "2025-08-19T11:20:00Z",
        "last_changed_at": "2026-06-30T16:00:00Z",
    },
    {
        "name": "cart-abandonment-email",
        "description": "Sends a reminder email 24 hours after an abandoned cart",
        "enabled": False,
        "created_by": "katherine.johnson",
        "created_at": "2026-03-27T09:45:00Z",
        "last_changed_at": "2026-03-27T09:45:00Z",
    },
    {
        "name": "graphql-gateway",
        "description": "Routes catalog reads through the new GraphQL gateway",
        "enabled": True,
        "created_by": "alan.turing",
        "created_at": "2026-01-30T14:00:00Z",
        "last_changed_at": "2026-05-22T10:10:00Z",
    },
    {
        "name": "warehouse-auto-routing",
        "description": "Automatically routes orders to the nearest warehouse",
        "enabled": False,
        "created_by": "ada.lovelace",
        "created_at": "2026-05-19T08:30:00Z",
        "last_changed_at": "2026-05-19T08:30:00Z",
    },
    {
        "name": "session-replay",
        "description": "Records anonymized session replays for support debugging",
        "enabled": False,
        "created_by": "margaret.hamilton",
        "created_at": "2025-11-03T10:00:00Z",
        "last_changed_at": "2026-02-14T11:25:00Z",
    },
    {
        "name": "loyalty-points-v3",
        "description": "Switches loyalty point accrual to the new rewards engine",
        "enabled": True,
        "created_by": "grace.hopper",
        "created_at": "2026-02-09T16:20:00Z",
        "last_changed_at": "2026-07-18T13:15:00Z",
    },
    {
        "name": "server-side-cart",
        "description": "Moves cart state from local storage to the server",
        "enabled": True,
        "created_by": "katherine.johnson",
        "created_at": "2025-07-22T09:00:00Z",
        "last_changed_at": "2026-03-01T09:00:00Z",
    },
    {
        "name": "vendor-payout-automation",
        "description": "Automates weekly payouts to third-party vendors",
        "enabled": False,
        "created_by": "alan.turing",
        "created_at": "2026-06-11T12:00:00Z",
        "last_changed_at": "2026-06-11T12:00:00Z",
    },
    {
        "name": "accessibility-audit-banner",
        "description": "Shows an in-app banner linking to the accessibility audit report",
        "enabled": True,
        "created_by": "ada.lovelace",
        "created_at": "2025-09-28T14:30:00Z",
        "last_changed_at": "2026-01-16T15:40:00Z",
    },
    {
        "name": "price-match-guarantee",
        "description": "Enables the automated price-match request flow",
        "enabled": False,
        "created_by": "margaret.hamilton",
        "created_at": "2026-04-03T10:50:00Z",
        "last_changed_at": "2026-04-03T10:50:00Z",
    },
    {
        "name": "edge-caching",
        "description": "Serves catalog pages from the CDN edge cache",
        "enabled": True,
        "created_by": "grace.hopper",
        "created_at": "2025-06-30T08:15:00Z",
        "last_changed_at": "2026-05-27T09:35:00Z",
    },
]


def _find_feature_flag(name: str) -> dict[str, str | bool] | None:
    return next((flag for flag in FEATURE_FLAGS if flag["name"] == name), None)


@page.action(
    "Enable Feature Flag",
    method="post",
    description="Turn a feature flag on for every user",
    icon="toggle-right",
    color="green",
    is_hidden=True,
)
async def enable_feature_flag(
    name: str = Query(..., description="Flag name"),
) -> spec.Action:
    flag = _find_feature_flag(name)
    if flag is None:
        return {"toast": f"No such flag '{name}'"}
    flag["enabled"] = True
    flag["last_changed_at"] = datetime.now(UTC).isoformat()
    return {"toast": f"'{name}' enabled"}


@page.action(
    "Disable Feature Flag",
    method="post",
    description="Turn a feature flag off for every user",
    icon="toggle-left",
    color="red",
    is_hidden=True,
)
async def disable_feature_flag(
    name: str = Query(..., description="Flag name"),
) -> spec.Action:
    flag = _find_feature_flag(name)
    if flag is None:
        return {"toast": f"No such flag '{name}'"}
    flag["enabled"] = False
    flag["last_changed_at"] = datetime.now(UTC).isoformat()
    return {"toast": f"'{name}' disabled"}


@page.table(
    "Feature Flags",
    description="Search feature flags and enable or disable them",
    icon="flag",
    color="violet",
    columns={
        "name": {"label": "Name", "icon": "flag", "color": "violet"},
        "description": {
            "label": "Description",
            "icon": "notepad-text",
            "color": "gray",
        },
        "status": {
            "style": "badge",
            "label": "Status",
            "icon": "toggle-right",
            "color": "emerald",
        },
        "created_by": {"label": "Created By", "icon": "user", "color": "indigo"},
        "created_at": {
            "label": "Created At",
            "icon": "calendar-plus",
            "color": "slate",
        },
        "last_changed_at": {
            "label": "Last Changed At",
            "icon": "history",
            "color": "amber",
        },
    },
)
async def get_feature_flags(search: SearchDep, pagination: PageDep) -> spec.Table:
    flags = FEATURE_FLAGS
    if search:
        needle = search.lower()
        flags = [
            flag
            for flag in flags
            if needle in str(flag["name"]).lower()
            or needle in str(flag["description"]).lower()
        ]

    start = (pagination.page - 1) * pagination.per_page
    page_flags = flags[start : start + pagination.per_page]

    return {
        "data": [
            {
                "name": flag["name"],
                "description": flag["description"],
                "status": "on" if flag["enabled"] else "off",
                "created_by": flag["created_by"],
                "created_at": flag["created_at"],
                "last_changed_at": flag["last_changed_at"],
                "__actions__": [
                    {
                        "label": "Disable",
                        "action": reference_action(disable_feature_flag),
                        "query": {"name": flag["name"]},
                        "icon": "toggle-left",
                        "color": "red",
                    }
                    if flag["enabled"]
                    else {
                        "label": "Enable",
                        "action": reference_action(enable_feature_flag),
                        "query": {"name": flag["name"]},
                        "icon": "toggle-right",
                        "color": "green",
                    },
                ],
            }
            for flag in page_flags
        ],
        "total": len(flags),
    }


# ---------------------------------------------------------------------------
# Forms — one per HTTP verb (post/put/patch/delete demoed here).
# ---------------------------------------------------------------------------


class WebhookBody(BaseModel):
    url: str
    event: str
    secret: str | None = None


@page.form(
    "Create Webhook",
    method="post",
    description="Register a new outgoing webhook",
    icon="webhook",
    color="teal",
)
async def create_webhook(body: WebhookBody) -> spec.Form:
    return {
        "icon": "webhook",
        "color": "teal",
        "toast": "Webhook created",
        "message": f"Would create a webhook for '{body.event}' -> {body.url}",
        "table": {
            "data": [{"id": 1, "url": body.url, "event": body.event}],
            "icon": "webhook",
            "color": "teal",
        },
    }


class RateLimitBody(BaseModel):
    requests_per_minute: int
    burst_size: int = 0


@page.form(
    "Update Rate Limit",
    method="put",
    description="Replace the current API rate-limit configuration",
    icon="gauge",
    color="cyan",
    is_hidden=True,
)
async def update_rate_limit(body: RateLimitBody) -> spec.Form:
    return {
        "icon": "gauge",
        "color": "cyan",
        "toast": f"Rate limit set to {body.requests_per_minute}/min "
        f"(burst {body.burst_size}) — example only, nothing was saved",
    }


@page.form(
    "Rename Environment",
    method="patch",
    description="Rename an existing deployment environment",
    icon="pencil",
    color="orange",
)
async def rename_environment(
    environment_id: int = Query(..., description="Environment to rename"),
    new_name: str = Body(..., embed=True, description="New environment name"),
) -> str:
    return (
        f"Would rename environment #{environment_id} to '{new_name}' "
        "(example only, nothing was renamed)"
    )


@page.form(
    "Schedule Config Reset",
    method="delete",
    description="Queue a configuration reset for the next maintenance window",
    icon="rotate-ccw",
    color="rose",
    is_hidden=False,
)
async def schedule_config_reset(
    config_id: int = Query(..., description="Config entry to reset"),
) -> spec.Form:
    return None


@page.stat("Random number 1", icon="sun", color="yellow", refresh=timedelta(seconds=1))
def random_number_1():
    sleep(1)
    return randint(100, 1000)


@page.stat("Random number 2", icon="moon", color="blue")
def random_number_2():
    sleep(1)
    return randint(100, 1000)


@page.stat("Random number 3", icon="mars", color="red")
def random_number_3():
    sleep(1)
    return randint(100, 1000)
