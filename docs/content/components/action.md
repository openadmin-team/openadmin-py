# Action

An action is a one-off button that calls an endpoint — standalone on a page, or attached to a table row.

```python
@page.action("Delete Book", method="delete", description="Remove a book by ID")
async def delete_book(
    session: AsyncSessionDep, book_id: int = Query(...)
) -> spec.Action:
    book = await session.get(models.Book, book_id)
    if book:
        await session.delete(book)
        await session.commit()
    return {"message": f"Deleted book #{book_id}"}
```

## Decorator

```python
page.action(
    name: str,
    *,
    method: spec.HttpMethod = "post",
    description: str | None = None,
    is_hidden: bool = False,
    icon: spec.Icon | None = None,
    color: spec.Color | None = None,
)
```

The decorated function is registered at `<method> /<page-id>/action/<action-id>`, using whichever HTTP method you pass — `get`, `post` (the default), `put`, `patch`, `delete`, or `head`.

## Return value

```python
class ActionResponse(TypedDict):
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    toast: NotRequired[str]
    table: NotRequired[dict | object]
    message: NotRequired[str]


type Action = ActionResponse | None | str
```

Same shape as a [form](/components/form)'s response: return `None` for a silent success, a string as shorthand for `message`, or a full `ActionResponse` dict with `toast`/`message`/`table` for richer feedback.

```python
@page.action("Ping Service", method="get", icon="activity", color="green")
async def ping_service(target: str = Query("api")) -> spec.Action:
    return {
        "toast": f"{target} responded in 12ms",
        "message": f"Pinged '{target}' — reachable",
    }
```

## Parameters by HTTP method

Actions take parameters the same way any FastAPI endpoint does — `Query` for `get`/`delete`, a pydantic model or `Body(...)` for `post`/`put`/`patch`, `Form(...)` fields when appropriate:

```python
@page.action("Rotate API Key", method="patch", icon="key", color="amber")
async def rotate_api_key(
    key_name: str = Form(..., description="Key to rotate"),
    expires_in_days: int = Form(30, description="Validity period for the new key"),
) -> spec.Action: ...
```

## Attaching an action to a table row

Give an action `is_hidden=True` when its only purpose is to be triggered from a row, then reference it from that row's `__actions__` with `reference_action`:

```python
from openadmin.fastapi import reference_action

@page.action("Delete Author", is_hidden=True)
async def delete_author(id: str) -> spec.Action:
    ...
    return {"toast": f"User with id {id} deleted"}


@page.table("All Authors")
async def get_all_authors(...) -> spec.Table:
    return {
        "data": [
            {
                "id": author.id,
                "name": ...,
                "__actions__": [
                    {
                        "label": "Delete this user",
                        "action": reference_action(delete_author),
                        "query": {"id": author.id},
                        "color": "red",
                        "icon": "trash",
                    },
                ],
            }
            for author in authors
        ],
    }
```

`reference_action` reads the ID that the `@page.action(...)` decorator stamped onto `delete_author`, so `delete_author` must already be decorated before it's referenced this way — a plain top-to-bottom ordering requirement, not special behavior. See [Implementing a Table](/cookbook/implementing-table) for the full recipe.
