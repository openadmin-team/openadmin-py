<div align="center">
  <img src="docs/assets/logo.png" alt="OpenAdmin" width="120" />

  <h1>OpenAdmin</h1>

  <p>Admin dashboards as FastAPI routes. No templates, no frontend project, no config files.</p>

  <a href="https://pypi.org/project/openadmin/"><img src="https://img.shields.io/pypi/v/openadmin?style=flat-square&label=pypi&color=blue" alt="PyPI" /></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.14%2B-blue?style=flat-square" alt="Python" /></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/built%20on-FastAPI-009688?style=flat-square" alt="FastAPI" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0--or--later-green?style=flat-square" alt="License" /></a>

  <p><a href="https://openadmin-team.github.io/openadmin-py/">Documentation</a></p>
</div>

---

**Under active development.** APIs may change between releases.

---

OpenAdmin is a FastAPI-native library for building admin panels. A page is a router, a widget is an endpoint — stats, tables, forms, actions, and charts, defined with typed decorators in plain Python.

```python
from openadmin import spec
from openadmin.fastapi import AdminPage, AdminPanel

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


admin = AdminPanel("My Admin")
admin.section("General", pages=[page])
```

```python
from fastapi import FastAPI

app = FastAPI()
app.mount("/admin", admin.app)
```

Each decorated function is a normal FastAPI handler — dependency injection, `Query`/`Body` parameters, and OpenAPI docs all work as they would on any route.

## Installation

```bash
pip install openadmin
# or
uv add openadmin
```

## Documentation

Everything else — the full component reference, authentication, and worked cookbook recipes — lives at:

**[openadmin-team.github.io/openadmin-py](https://openadmin-team.github.io/openadmin-py/)**

- [Getting Started](https://openadmin-team.github.io/openadmin-py/introduction/getting-started) — build a minimal panel end to end
- [Components](https://openadmin-team.github.io/openadmin-py/components/) — stats, tables, forms, actions, and charts
- [Authentication](https://openadmin-team.github.io/openadmin-py/auth/) — gate the panel behind a login screen
- [Cookbook](https://openadmin-team.github.io/openadmin-py/cookbook/implementing-auth) — recipes for row actions, reference fields, and auth

## Development

```bash
# Run the example app
make dev/example

# Run all checks (format, lint, types, tests, security)
make check

# Auto-fix formatting and lint issues
make fix
```

## License

[AGPL-3.0-or-later](LICENSE) — © 2026 OpenAdmin
