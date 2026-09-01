# Implementing a Form with a Reference

A step-by-step recipe for a form field that picks its value from another table's rows — for example, choosing a book's author from a list of authors instead of typing an author ID by hand. Full option reference is in [Form](/components/form) and [Table](/components/table).

::: info
`AsyncSessionDep`, `Author`, `Book`, and the `select` calls below stand in for your own database session dependency and models — OpenAdmin has no opinion on persistence.
:::

## 1. Define the table the field will reference

The referenced table has to be a normal `@page.table(...)`, decorated before you reference it. It doesn't need to live on the same page as the form:

```python
# admin/authors.py
from openadmin import spec
from openadmin.fastapi import AdminPage

page = AdminPage("Authors", icon="users")


@page.table(
    "All Authors",
    columns={"id": {"label": "ID"}, "name": {"label": "Name"}},
)
async def get_all_authors(session: AsyncSessionDep) -> spec.Table:
    authors = (await session.execute(select(Author))).scalars().all()
    return {
        "data": [{"id": a.id, "name": a.name, "__view__": a.name} for a in authors],
    }
```

`__view__` is what the reference picker displays for each row — set it to whatever best identifies the row to a human, here the author's name instead of their raw ID.

## 2. Define the form's request body

```python
# admin/books.py
from pydantic import BaseModel


class AddBookBody(BaseModel):
    title: str
    author_id: int
```

## 3. Point the field at the table

```python
from openadmin.fastapi import AdminPage, reference

from .authors import get_all_authors

page = AdminPage("Books", icon="book")


@page.form(
    "Add Book",
    fields={
        "author_id": {
            "reference": reference(get_all_authors),
            "reference_field": "id",
            "icon": "user-pen",
            "color": "violet",
        }
    },
)
async def add_book(body: AddBookBody, session: AsyncSessionDep) -> spec.Form:
    book = Book(**body.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return {"message": f"Added book '{book.title}'"}
```

- **`reference`** is the referenced table's generated ID, obtained with `reference(get_all_authors)` — pass the function itself, not a string, so a rename of the table doesn't silently break the link.
- **`reference_field`** is the column of the referenced table's rows to actually submit as `author_id`'s value. The picker shows each row's `__view__` label, but writes `row[reference_field]` when one is chosen — here, the author's `id`.

Because `reference` reads an attribute the `@page.table(...)` decorator stamps directly onto `get_all_authors`, that function must already be decorated by the time `add_book` is defined — in practice, just make sure the module defining the table is imported before the module defining the form runs, as in the example above.

## 4. Cross-page references

The referenced table doesn't have to live on the same `AdminPage` as the form — import the decorated function from wherever it's defined, same as the `from .authors import get_all_authors` above. Only the function object matters; the pages don't need any other relationship.

## Referencing an action instead of a table

The equivalent helper for attaching an action to a table row is `reference`, covered in [Implementing a Table](/cookbook/implementing-table). Both helpers work the same way — they read an ID the decorator stamped onto an already-decorated function.
