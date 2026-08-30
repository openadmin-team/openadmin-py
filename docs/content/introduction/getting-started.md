# Getting Started

This walks through building a minimal admin panel from scratch: one page, one stat, one table, mounted onto a FastAPI app.

## Requirements

- Python 3.14+
- FastAPI

## Installation

```bash
pip install openadmin
```

or with `uv`:

```bash
uv add openadmin
```

## Build a page

An `AdminPage` holds the widgets for one page in the navigation. Widgets are added by decorating functions with `@page.stat`, `@page.table`, `@page.form`, and `@page.action`.

```python
# app/admin/dashboard.py
from openadmin import spec
from openadmin.fastapi import AdminPage

page = AdminPage("Dashboard", icon="layout-dashboard")


@page.stat("Total Users")
async def total_users() -> spec.Stat:
    return 1_024


@page.table("Recent Users")
async def recent_users() -> spec.Table:
    return {
        "data": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "viewer"},
        ]
    }
```

Each decorated function is a normal `async def` (or sync `def`) handler — it can take `Query`/`Body` parameters, use `Depends(...)` for a database session, and return whatever your return type declares. The decorator infers the parameter schema from the function signature the same way FastAPI does.

## Assemble the panel

`AdminPanel` is the top-level object. Pages are grouped into named sections:

```python
# app/admin/panel.py
from openadmin.fastapi import AdminPanel

from .dashboard import page as dashboard_page

admin = AdminPanel("My Admin", description="Internal operations panel")

admin.section("General", icon="layout-grid", pages=[dashboard_page])
```

## Mount it on your app

`AdminPanel.app` is a real `FastAPI()` instance, so it mounts like any sub-application:

```python
# app/main.py
from fastapi import FastAPI

from .admin.panel import admin

app = FastAPI()
app.mount("/admin", admin.app)
```

## Run it

```bash
fastapi dev app/main.py
```

Visit `http://localhost:8000/admin/` for the UI, or `http://localhost:8000/admin/api/openadmin.json` to see the raw spec that drives it.

::: tip
The panel is unprotected by default — anyone who can reach `/admin` can view and act on every widget. See [Authentication](/auth/) before deploying anywhere reachable by untrusted users.
:::

## Next steps

- [Components](/components/) — every widget type, with its full option list.
- [Authentication](/auth/) — add a login screen.
- [Cookbook](/cookbook/implementing-table) — worked recipes for common patterns like reference fields and row actions.
