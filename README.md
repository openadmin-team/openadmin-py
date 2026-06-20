<!-- <div align="center">
  <img src="docs/assets/logo.png" alt="OpenAdmin" width="180" />

  <h1>openadmin-py</h1>

  <p>Build admin panels as FastAPI routes — stats, tables, charts, and actions, all in pure Python.</p>

  [![License: AGPL-3.0-or-later](https://img.shields.io/badge/license-AGPL--3.0--or--later-green?style=flat-square)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.14%2B-blue?style=flat-square)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/built%20on-FastAPI-009688?style=flat-square)](https://fastapi.tiangolo.com)
</div> -->

---

**OpenAdmin** is a FastAPI-native library for building admin dashboards. Define pages with typed decorators — no frontend code, no templates, no configuration files. Every page is just a router; every widget is just an endpoint.

## Features

- **Stats** — display single values: counts, totals, booleans, percentages
- **Tables** — paginated, searchable data grids with per-row actions
- **Charts** — area, bar, line, and pie charts with labeled series
- **Actions** — trigger HTTP calls (GET / POST / PUT / PATCH / DELETE) from the UI
- **Forms** — structured forms that POST/PUT/PATCH/DELETE to your own endpoints
- **Markdown** — render rich text content on any page
- **FastAPI-native** — full dependency injection, OpenAPI docs, and router composition out of the box

## Installation

```bash
pip install openadmin-py
# or with uv
uv add openadmin-py
```

## Quick Start

```python
from fastapi import FastAPI
from openadmin.fastapi import AdminPanel, AdminPage
from openadmin.types import Stat, Table

# Create an admin panel (a FastAPI sub-application)
admin = AdminPanel()

# Define a page
page = AdminPage("Dashboard")

@page.stat("Total Users")
async def total_users() -> Stat:
    return Stat(value=1_024)

@page.table("Recent Users")
async def recent_users() -> Table:
    return Table(data=[
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob",   "role": "viewer"},
    ])

# Register the page and mount the panel
admin.include_page(page)

app = FastAPI()
app.mount("/admin", admin)
```

## Usage

### Stats

Display a single numeric or boolean value.

```python
from openadmin.types import Stat

@page.stat("Active Sessions")
async def active_sessions() -> Stat:
    return Stat(value=42)
```

### Tables

Paginated tables with optional search. Use the built-in dependency types to receive pagination and search parameters automatically.

```python
from openadmin.fastapi import PaginationParamsDep, SearchQueryDep
from openadmin.types import Table

@page.table("Users")
async def users_table(
    pagination: PaginationParamsDep,
    search: SearchQueryDep,
) -> Table:
    # pagination.page, pagination.per_page
    # search is str | None
    return Table(data=[...])
```

#### Row Actions

Attach per-row action buttons by including `__actions__` in each row:

```python
from openadmin.types import Action, Table, TableRow

@page.table("Users")
async def users_table() -> Table:
    return Table(data=[
        TableRow(
            id=1,
            name="Alice",
            __actions__=[
                Action(color="danger", method="DELETE", url="/users/1", body=None),
                Action(color="info",   method="POST",   url="/users/1/reset", body=None),
            ],
        )
    ])
```

### Charts

All chart types share the same structure: a `data` list of dicts and a `config` that maps series keys to display labels and colors.

```python
from openadmin.types import BarChart, PieChart

@page.bar_chart("Sales by Region", "Total sales per region this quarter")
async def sales_chart() -> BarChart:
    return BarChart(
        data=[
            {"region": "North", "sales": 120},
            {"region": "South", "sales": 95},
        ],
        config={"sales": {"label": "Sales", "color": "#6366f1"}},
    )

@page.pie_chart("User Roles", "Breakdown of user roles")
async def roles_chart() -> PieChart:
    return PieChart(
        data=[
            {"segment": "Admin",  "count": 5},
            {"segment": "Editor", "count": 20},
            {"segment": "Viewer", "count": 75},
        ],
        config={"count": {"label": "Users", "color": "#10b981"}},
    )
```

### Actions

Expose buttons that trigger HTTP requests — useful for one-off operations like cache clearing or triggering background jobs.

```python
@page.action_post("Clear Cache")
async def clear_cache():
    # your logic here
    return {"status": "cleared"}
```

### Forms

Forms collect user input and submit it to your endpoint. Mark a form hidden if it should not appear in the page navigation.

```python
from pydantic import BaseModel

class InvitePayload(BaseModel):
    email: str
    role: str

@page.form_post("Invite User", "Send an invitation email to a new user")
async def invite_user(payload: InvitePayload):
    # send invite...
    return {"invited": payload.email}
```

### Markdown

Render markdown text directly on a page — useful for instructions, changelogs, or documentation sections.

```python
@page.markdown("Release Notes")
async def release_notes() -> str:
    return "## v1.2.0\n- Added dark mode\n- Fixed pagination bug"
```

## Full Example

A real-world page querying a SQLAlchemy database:

```python
from sqlalchemy import func, select
from openadmin.fastapi import AdminPage, PaginationParamsDep, SearchQueryDep
from openadmin.types import Stat, Table, BarChart

page = AdminPage("Library")

@page.stat("Total Books")
async def total_books(session: AsyncSessionDep) -> Stat:
    result = await session.execute(select(func.count()).select_from(Book))
    return Stat(value=result.scalar_one())

@page.table("Books")
async def books_table(
    session: AsyncSessionDep,
    pagination: PaginationParamsDep,
    search: SearchQueryDep,
) -> Table:
    stmt = select(Book).offset(pagination.page * pagination.per_page).limit(pagination.per_page)
    books = (await session.execute(stmt)).scalars().all()
    return Table(data=[{"title": b.title, "year": b.published_year} for b in books])

@page.bar_chart("Books per Genre", "Number of books in each genre")
async def books_per_genre(session: AsyncSessionDep) -> BarChart:
    rows = (await session.execute(
        select(Genre.name, func.count().label("books"))
        .join(BookToGenre).group_by(Genre.id)
    )).all()
    return BarChart(
        data=[{"genre": name, "books": count} for name, count in rows],
        config={"books": {"label": "Books", "color": "#6366f1"}},
    )
```

See the [`examples/`](examples/) directory for a complete runnable application.

```bash
make dev/run
# → http://127.0.0.1:8000/docs
```

## API Reference

### `AdminPanel`

A `FastAPI` subclass. Use `include_page(page)` to register an `AdminPage`.

| Method | Description |
|---|---|
| `include_page(page, tags=None)` | Mount an `AdminPage` onto the panel |

### `AdminPage`

An `APIRouter` subclass. Each decorator creates a typed GET (or POST/PUT/etc.) endpoint under the page's prefix.

| Decorator | HTTP | Response type |
|---|---|---|
| `@page.stat(name)` | GET | `Stat` |
| `@page.table(name)` | GET | `Table` |
| `@page.markdown(name)` | GET | `str` |
| `@page.area_chart(name, description)` | GET | `AreaChart` |
| `@page.bar_chart(name, description)` | GET | `BarChart` |
| `@page.line_chart(name, description)` | GET | `LineChart` |
| `@page.pie_chart(name, description)` | GET | `PieChart` |
| `@page.action_get/post/put/patch/delete(name)` | * | any |
| `@page.form_post/put/patch/delete(name, description)` | * | any |

### Dependencies

| Name | Type | Description |
|---|---|---|
| `PaginationParamsDep` | `PaginationParams` | `page` and `per_page` query params |
| `SearchQueryDep` | `str \| None` | `search` query param |

### Types

| Type | Fields |
|---|---|
| `Stat` | `value: str \| bool \| int \| float` |
| `Table` | `data: list[TableRow \| dict]` |
| `TableRow` | any fields + `__actions__: list[Action]` |
| `Action` | `color`, `method`, `url`, `body` |
| `AreaChart / BarChart / LineChart / PieChart` | `data: list[dict]`, `config: dict` |

## Development

```bash
# Run the example app
make dev/run

# Run all checks (format, lint, types, tests, security)
make check

# Auto-fix formatting and lint issues
make fix
```

## License

[AGPL-3.0-or-later](LICENSE) — © 2026 OpenAdmin
