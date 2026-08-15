# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Annotated

from fastapi import Body, Depends, Form, Query
from pydantic import BaseModel
from random import randint
from openadmin import spec
from openadmin.fastapi import AdminPage
from datetime import timedelta
from time import sleep

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

@page.stat('Random number 1', icon='sun', color='yellow', refresh=timedelta(seconds=1))
def random_number_1():
    sleep(5)
    return randint(100, 1000)

@page.stat('Random number 2', icon='moon', color='blue')
def random_number_2():
    sleep(5)
    return randint(100, 1000)

@page.stat('Random number 3', icon='mars', color='red')
def random_number_3():
    sleep(5)
    return randint(100, 1000)