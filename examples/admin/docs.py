from openadmin import fastapi, spec


page = fastapi.AdminPage("Docs", icon='dock')

@page.markdown("Comany policy", icon='podcast', color='blue')
def company_policy():
    return """
# Hello World

This is new text

---

- Cake
- Limonade
"""