# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel

from openadmin.fastapi import AdminPage

page = AdminPage("Settings", description="Application-wide configuration")


@page.table("Current settings")
async def get_current_settings():
    return [
        {"key": "site_name", "value": "My App", "last_updated": "2026-05-01"},
        {"key": "maintenance_mode", "value": "false", "last_updated": "2026-04-10"},
        {"key": "max_upload_mb", "value": "50", "last_updated": "2026-03-22"},
        {"key": "signup_enabled", "value": "true", "last_updated": "2026-01-15"},
    ]


class GeneralSettingsBody(BaseModel):
    site_name: str
    signup_enabled: bool
    max_upload_mb: int


@page.form_put("Save general settings")
async def save_general_settings(body: GeneralSettingsBody):
    return {"ok": True, "site_name": body.site_name}


class MaintenanceBody(BaseModel):
    enabled: bool
    message: str


@page.form_patch("Toggle maintenance mode")
async def toggle_maintenance(body: MaintenanceBody):
    return {"maintenance_mode": body.enabled}


class SmtpSettingsBody(BaseModel):
    host: str
    port: int
    username: str
    password: str


@page.form_put("Save SMTP settings")
async def save_smtp_settings(body: SmtpSettingsBody):
    return {"ok": True, "host": body.host}


@page.action_post(
    "Send test email", description="Send a test email using current SMTP settings"
)
async def send_test_email():
    return {"sent": True}
