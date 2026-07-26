# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin import fastapi

page = fastapi.AdminPage("Docs", icon="dock")


@page.markdown("Comany policy", icon="podcast", color="blue")
def company_policy():
    return """
# Hello World

This is new text

---

- Cake
- Limonade
"""
