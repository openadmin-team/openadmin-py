# What is OpenAdmin?

OpenAdmin is a FastAPI-native library for building admin dashboards. You define pages as plain Python functions decorated with typed helpers — no templates, no separate frontend project, no configuration files to maintain. Every page is a FastAPI router; every widget on that page is just an endpoint.

```python
@page.stat("Total Users")
async def total_users() -> spec.Stat:
    return 1_024
```

That function is a normal `async def` FastAPI handler. It also happens to describe a stat tile that shows up in the admin UI, because OpenAdmin inspects its signature and return type to build a specification the bundled frontend renders.

## The core idea

An admin panel is a tree of four kinds of objects:

- **`AdminPanel`** — the panel itself. It is a small wrapper around a `FastAPI()` app, meant to be mounted onto your real application with `app.mount("/admin", admin.app)`.
- **Sections** — top-level groups in the navigation, registered on the panel with `admin.section(...)`. A section is just a name plus a list of pages.
- **`AdminPage`** — a page inside a section. Internally it holds a FastAPI `APIRouter`, so everything you already know about routers, dependencies, and path operations applies.
- **Components** — the widgets on a page: stats, tables, forms, actions, charts, and markdown blocks. Each one is registered with a decorator on an `AdminPage` (`@page.stat(...)`, `@page.table(...)`, etc.) and becomes both a real HTTP endpoint and an entry in the page's spec.

```
AdminPanel
└── section("Library")
    └── AdminPage("Books")
        ├── @page.stat("Total Books")
        ├── @page.table("All Books")
        ├── @page.form("Add Book")
        └── @page.action("Delete Book")
```

See [Components](/components/) for a full walkthrough of each widget type.

## How it fits together

Every decorator does two things at once:

1. It registers your function as a real route on the page's router — with FastAPI's usual dependency injection, `Query`/`Body`/`Form` parameters, pydantic models, and OpenAPI docs.
2. It records metadata (name, icon, color, the parameters it accepts, and so on) into a `Spec` — a plain nested `TypedDict` structure (`openadmin.spec.Spec` → `Section` → `Page` → `Component`) describing the whole panel.

The panel exposes that structure at `GET /api/openadmin.json`. The bundled frontend (served from the same panel at `/`) fetches this spec once to build the navigation and layout, then calls each component's own endpoint — the same one your decorator wrapped — to fetch or refresh its data. Because it's the same endpoint either way, you can `curl` any widget directly, exercise it from FastAPI's `/docs`, or write ordinary tests against it.

## What's included

- **Stats** — a single value: a count, a percentage, a boolean.
- **Tables** — paginated, searchable grids with per-row actions and styled columns (badges, images, links, files).
- **Forms** — structured forms that submit to your own endpoint, with optional reference fields that look values up from another table.
- **Actions** — one-off buttons that call an endpoint, either standalone or attached to a table row.
- **Charts** — bar and pie charts today, with area and line chart types defined in the spec for future support.
- **Markdown** — static or dynamic rich text blocks for guides, changelogs, or contextual notes.

Because a page is a router and a widget is an endpoint, everything FastAPI already gives you — dependency injection, background tasks, database sessions, response validation, middleware — works unchanged. There is no separate query language or templating layer to learn.

## Next steps

- [Getting Started](/introduction/getting-started) — build a minimal panel end to end.
- [Components](/components/) — the full reference for every widget type.
- [Authentication](/auth/) — gate the panel behind a login screen.
