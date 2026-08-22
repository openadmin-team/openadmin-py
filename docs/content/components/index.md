# Components

A component is a single widget on an `AdminPage`. Every component is registered with a decorator, and every decorator does the same two things: it registers a real FastAPI route, and it records the widget's metadata into the page's spec.

| Component | Decorator | Purpose |
| --- | --- | --- |
| [Stat](/components/stat) | `@page.stat(...)` | A single value — a count, a percentage, a boolean |
| [Table](/components/table) | `@page.table(...)` | A paginated, searchable grid with optional per-row actions |
| [Form](/components/form) | `@page.form(...)` | A structured form that submits to your own endpoint |
| [Action](/components/action) | `@page.action(...)` | A one-off button that calls an endpoint |
| [Bar Chart](/components/bar-chart) | `@page.bar_chart(...)` | A categorical bar chart |
| [Pie Chart](/components/pie-chart) | `@page.pie_chart(...)` | A proportional breakdown chart |
| [Markdown](/components/markdown) | `@page.markdown(...)` | A static or dynamic rich text block |
| [Area Chart](/components/area-chart) | — not yet available | Defined in the spec, no decorator yet |
| [Line Chart](/components/line-chart) | — not yet available | Defined in the spec, no decorator yet |

## Shared behavior

A few things apply to every component, not just one:

- **Parameters are inferred from the function signature.** `Query(...)`, `Body(...)`, `Form(...)`, pydantic models, and `Depends(...)` all work exactly as they do in any FastAPI route. OpenAdmin walks the resolved dependency tree and turns the query, body, and form parameters into JSON Schema, which becomes part of the component's spec.
- **`icon` and `color`** accept any value from the shared `Icon` and `Color` literal types in `openadmin.spec` (Lucide icon names and Tailwind-style color names, respectively).
- **`refresh`** (on `stat`, `table`, `markdown`, `bar_chart`, `pie_chart`) takes a `datetime.timedelta`. When set, the frontend polls the component's endpoint on that interval.
- **`is_hidden`** (on `table`, `action`, `form`) registers the endpoint and includes it in the spec, but keeps it out of the visible page layout. This is the mechanism behind row actions and reference fields — see [Implementing a Table](/cookbook/implementing-table) and [Implementing a Form with a Reference](/cookbook/implementing-form-with-reference).
- **`method`** (on `action`, `form`) is any of `get`, `post`, `put`, `patch`, `delete`, `head`, and maps directly to the matching FastAPI router method.

## Referencing one component from another

Two helpers let one component point at another by its generated ID, instead of hardcoding route paths:

```python
from openadmin.fastapi import reference_action, reference_table
```

- `reference_table(table_func)` — returns the ID of a `@page.table(...)`-decorated function. Used in a form field's `reference` to source a value picker from that table's rows.
- `reference_action(action_func)` — returns the ID of a `@page.action(...)`-decorated function. Used in a table row's `__actions__` to attach that action as a row button.

Both simply read an attribute (`__openadmin_table_id__` / `__openadmin_action_id__`) that the decorator stamped onto the function, so the referenced function must already be decorated — but not necessarily called — before you reference it.
