# Table

A table is a paginated, searchable grid, with optional styled columns and per-row actions.

```python
@page.table("Recent Users")
async def recent_users() -> spec.Table:
    return {
        "data": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "viewer"},
        ]
    }
```

## Decorator

```python
page.table(
    name: str,
    *,
    description: str | None = None,
    is_hidden: bool = False,
    columns: dict[str, spec.ColumnConfigValue] | None = None,
    icon: spec.Icon | None = None,
    color: spec.Color | None = None,
    refresh: timedelta | None = None,
)
```

The decorated function is registered as `GET /<page-id>/table/<table-id>`. Unlike actions and forms, a table's method is always `get`.

## Return value

```python
class TableResponse(TypedDict):
    data: TableData
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    refresh: NotRequired[int | None]
    total: NotRequired[int]

type Table = TableData | TableResponse
```

`TableData` is an iterable of row dicts. The simplest table returns a bare list:

```python
@page.table("Books by Author", description="Number of books per author")
async def get_books_by_author(session: AsyncSessionDep):
    ...
    return [{"author": name, "book_count": count} for name, count in rows]
```

Return a `TableResponse` dict instead when you need `total` for pagination (see below) or want to override `icon`/`color`/`refresh` per response.

## Columns

`columns` maps a field name in your row dicts to display metadata:

```python
class ColumnConfigValue(TypedDict):
    style: NotRequired[Literal["image", "badge", "link", "file"]]
    label: NotRequired[str]
    icon: NotRequired[Icon]
    color: NotRequired[Color]
```

```python
@page.table(
    "All Books",
    columns={
        "id": {"label": "ID", "icon": "hash", "color": "slate"},
        "cover": {"style": "image", "label": "Cover", "icon": "image", "color": "sky"},
        "title": {"label": "Title", "icon": "book-text", "color": "blue"},
        "status": {"style": "badge", "label": "Status", "icon": "badge-check", "color": "emerald"},
        "reference": {"style": "link", "label": "Reference", "icon": "external-link", "color": "indigo"},
        "attachment": {"style": "file", "label": "Attachment", "icon": "file", "color": "amber"},
    },
)
async def get_all_books(...) -> spec.Table: ...
```

A column left out of `columns` is still shown, using its raw key as the label.

## Pagination and search

`openadmin.fastapi.deps` ships two dependencies for the common case:

```python
from openadmin.fastapi.deps import PageDep, SearchDep

@page.table("All Books")
async def get_all_books(
    session: AsyncSessionDep, pagination: PageDep, search: SearchDep
) -> spec.Table:
    stmt = (
        select(models.Book)
        .offset((pagination.page - 1) * pagination.per_page)
        .limit(pagination.per_page)
    )
    if search:
        stmt = stmt.where(models.Book.title.ilike(f"%{search}%"))
    ...
```

`PageDep` resolves to a `PaginationParams(page: int, per_page: int)` read from the `page`/`per_page` query parameters (default `page=1`, `per_page=10`). `SearchDep` resolves to `str | None` from a `search` query parameter. Return `total` in a `TableResponse` so the frontend knows how many pages exist:

```python
return {"data": [...], "total": total_count}
```

## Per-row keys

A row dict can include three special keys alongside your own columns:

- **`__view__`** — a compact label used to represent the whole row elsewhere (for example, when the row is offered as an option in a form's reference picker — see [Implementing a Form with a Reference](/cookbook/implementing-form-with-reference)).
- **`__actions__`** — a list of buttons attached to that row. Each entry references an action registered elsewhere on the page via `reference_action`:

  ```python
  from openadmin.fastapi import reference_action

  "__actions__": [
      {
          "label": "Delete this user",
          "action": reference_action(delete_author),
          "query": {"id": author.id},
          "color": "red",
          "icon": "trash",
      },
  ],
  ```

- **`__values__`** — per-cell overrides of `style`/`label`/`icon`/`color` for that row's specific columns, when a single column's styling depends on the row's data:

  ```python
  "__values__": {
      "status": {"color": "green" if flag["enabled"] else "red", "icon": "antenna"},
  },
  ```

## Hiding a table

`is_hidden=True` keeps the route and spec entry but removes the table from the visible page. This is how a table can act purely as a data source for a form's reference field, without also cluttering the page it's declared on. See [Implementing a Table](/cookbook/implementing-table) for the full pattern.
