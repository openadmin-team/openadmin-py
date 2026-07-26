# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin import fastapi, spec

page = fastapi.AdminPage("Docs", icon="dock")


@page.markdown("Comany policy 1", icon="podcast", color="blue")
def company_policy_1() -> spec.Markdown:
    return """
# Hello World

This is new text

---

- Cake
- Limonade
"""


@page.markdown("Comany policy 2")
def company_policy_2() -> spec.Markdown:
    return {
        "content": """
                    # Hello World

                    This is new text

                    ---

                    - Cake
                    - Limonade
        """,
        "color": "yellow",
        "icon": "a-arrow-up",
    }
