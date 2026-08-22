# Form

A form submits to your own endpoint using whatever request shape you declare — a pydantic body, `Query`/`Form`/`Body` parameters, or a mix.

```python
class AddBookBody(BaseModel):
    title: str
    author_id: int
    published_year: int | None = None


@page.form("Add Book", description="Add a new book to the catalog")
async def add_book(body: AddBookBody, session: AsyncSessionDep) -> spec.Form:
    book = models.Book(**body.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return {"message": f"Added book '{book.title}'"}
```

## Decorator

```python
page.form(
    name: str,
    *,
    method: spec.HttpMethod = "post",
    fields: dict[str, spec.FieldConfig] | None = None,
    description: str | None = None,
    is_hidden: bool = False,
    icon: spec.Icon | None = None,
    color: spec.Color | None = None,
)
```

The decorated function is registered at `<method> /<page-id>/form/<form-id>`, using whichever HTTP method you pass — `get`, `post` (the default), `put`, `patch`, `delete`, or `head`.

## Return value

```python
class FormResponse(TypedDict):
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    toast: NotRequired[str]
    table: NotRequired[dict | object]
    message: NotRequired[str]


type Form = FormResponse | None | str
```

Return `None` for a bare success with no message, a plain string as a shorthand for `message`, or a `FormResponse` dict for full control:

```python
@page.form("Create Webhook", method="post")
async def create_webhook(body: WebhookBody) -> spec.Form:
    return {
        "icon": "webhook",
        "color": "teal",
        "toast": "Webhook created",
        "message": f"Would create a webhook for '{body.event}' -> {body.url}",
        "table": {"id": 1, "url": body.url, "event": body.event},
    }
```

`toast` is a brief transient notification; `message` is shown inline after submission; `table` is an arbitrary JSON payload echoed back to the user (typically the created or affected record) — it's for feedback, not for updating other components.

## Reference fields

`fields` maps a request field name to a `FieldConfig`, turning a plain input into a picker sourced from another table:

```python
class FieldConfig(TypedDict):
    reference: NotRequired[str | None]
    reference_field: NotRequired[str]
    icon: NotRequired[Icon]
    color: NotRequired[Color]
```

```python
from openadmin.fastapi import reference_table


@page.form(
    "Add Author",
    fields={
        "friend": {
            "reference": reference_table(get_all_authors),
            "reference_field": "id",
            "icon": "user",
            "color": "blue",
        }
    },
)
async def add_author(body: AddAuthorBody, session: AsyncSessionDep) -> spec.Form: ...
```

`reference` is the ID of a table (obtained with `reference_table`, so `get_all_authors` must already be decorated with `@page.table(...)`); `reference_field` is the column of that table's rows to submit as the field's value. See [Implementing a Form with a Reference](/cookbook/implementing-form-with-reference) for the full walkthrough.

## Other HTTP methods

```python
@page.form("Rename Environment", method="patch")
async def rename_environment(
    environment_id: int = Query(..., description="Environment to rename"),
    new_name: str = Body(..., embed=True, description="New environment name"),
) -> str:
    return f"Renamed environment #{environment_id} to '{new_name}'"
```

## Hiding a form

`is_hidden=True` keeps the endpoint and its spec entry but removes it from the visible page, the same as with tables and actions.
