# Implementing a Table

A step-by-step recipe for a searchable, paginated table with styled columns and a per-row delete action. Full option reference is in [Table](/components/table) and [Action](/components/action).

::: info
`AsyncSessionDep`, `User`, and the `select`/`func` calls below stand in for your own database session dependency and models — OpenAdmin has no opinion on persistence. `PageDep`/`SearchDep` are the only dependencies that come from OpenAdmin itself.
:::

## 1. Define the page

```python
# admin/users.py
from openadmin import spec
from openadmin.fastapi import AdminPage, reference_action
from openadmin.fastapi.deps import PageDep, SearchDep

page = AdminPage("Users", icon="users")
```

## 2. Add pagination and search

`PageDep` and `SearchDep` cover the common case — `page`/`per_page` and `search` query parameters, parsed for you:

```python
@page.table(
    "All Users",
    description="Browse users with search and pagination",
    icon="users",
    color="blue",
    columns={
        "id": {"label": "ID", "icon": "hash", "color": "slate"},
        "name": {"label": "Name", "icon": "user", "color": "indigo"},
        "role": {"style": "badge", "label": "Role", "icon": "shield", "color": "emerald"},
    },
)
async def get_all_users(session: AsyncSessionDep, pagination: PageDep, search: SearchDep) -> spec.Table:
    stmt = select(User).offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
    count_stmt = select(func.count(User.id))
    if search:
        stmt = stmt.where(User.name.ilike(f"%{search}%"))
        count_stmt = count_stmt.where(User.name.ilike(f"%{search}%"))

    users = (await session.execute(stmt)).scalars().all()
    total = (await session.execute(count_stmt)).scalar_one()

    return {
        "data": [{"id": u.id, "name": u.name, "role": u.role} for u in users],
        "total": total,
    }
```

Returning `total` is what lets the frontend render correct page controls — without it, pagination still works, but it can't show a page count.

`columns` controls display, not data: `style: "badge"` renders the `role` cell as a badge; leave a column out of `columns` and it still shows, using its raw key as the label. See [Table](/components/table) for the other styles (`image`, `link`, `file`).

## 3. Add a delete action

Declare the action with `is_hidden=True` — it exists purely to be triggered from a row, not to be shown on the page as its own button:

```python
@page.action("Delete User", method="delete", is_hidden=True)
async def delete_user(session: AsyncSessionDep, user_id: int = Query(...)) -> spec.Action:
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)
        await session.commit()
    return {"toast": f"User #{user_id} deleted" if user else f"User #{user_id} not found"}
```

## 4. Attach it to each row

Reference the action by function, not by string ID, so a rename doesn't silently break the link:

```python
@page.table("All Users", ...)
async def get_all_users(...) -> spec.Table:
    ...
    return {
        "data": [
            {
                "id": u.id,
                "name": u.name,
                "role": u.role,
                "__actions__": [
                    {
                        "label": "Delete",
                        "action": reference_action(delete_user),
                        "query": {"user_id": u.id},
                        "icon": "trash",
                        "color": "red",
                    },
                ],
            }
            for u in users
        ],
        "total": total,
    }
```

`reference_action` reads the ID that `@page.action(...)` stamped onto `delete_user`, so `delete_user` needs to be defined (decorated) above `get_all_users` in the file, or at least imported before this function runs — plain Python name resolution, nothing OpenAdmin-specific.

The action's own `query`/`body`/`form` schema (inferred from `Query(...)` on `user_id`) still applies — the `query` dict in `__actions__` is what actually gets sent as that action's parameters when the row's button is clicked.

## 5. Per-cell overrides

When a single column's icon or color depends on the row's data rather than being fixed in `columns`, use `__values__`:

```python
"__values__": {
    "role": {"color": "amber" if u.role == "admin" else "slate"},
},
```

## Next

- Use a table as the source for a form's reference picker: [Implementing a Form with a Reference](/cookbook/implementing-form-with-reference).
- Full column style and per-row key reference: [Table](/components/table).
