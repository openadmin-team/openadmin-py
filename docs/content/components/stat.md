# Stat

A stat displays a single value — a count, a percentage, a boolean, or plain text.

```python
@page.stat("Total Users")
async def total_users() -> spec.Stat:
    return 1_024
```

## Decorator

```python
page.stat(
    name: str,
    *,
    icon: spec.Icon | None = None,
    color: spec.Color | None = None,
    description: str | None = None,
    refresh: timedelta | None = None,
)
```

The decorated function is registered as `GET /<page-id>/stat/<stat-id>`.

## Return value

```python
type StatValue = str | int | float | bool | None


class StatResponse(TypedDict):
    value: StatValue
    refresh: NotRequired[int | None]
    icon: NotRequired[Icon]
    color: NotRequired[Color]


type Stat = StatValue | StatResponse
```

Return the bare value when you have nothing else to say:

```python
@page.stat("Active Sessions")
async def active_sessions() -> spec.Stat:
    return 42
```

Return a `StatResponse` dict to override the icon, color, or refresh interval per-response (useful when they depend on the value itself, e.g. a red icon when a count is above a threshold):

```python
@page.stat("Total Authors")
async def get_total_authors(session: AsyncSessionDep) -> spec.StatResponse:
    result = await session.execute(select(func.count(models.Author.id)))
    return {"value": result.scalar_one(), "icon": "users", "color": "indigo"}
```

## Auto-refreshing

Pass `refresh` to poll the stat's endpoint automatically:

```python
from datetime import timedelta


@page.stat("Random Number", icon="sun", color="yellow", refresh=timedelta(seconds=1))
def random_number():
    return randint(100, 1000)
```

## Parameters

Like every component, a stat function can take `Query`, `Body`, `Depends`, and pydantic parameters — they're inferred from the signature and become part of the component's spec, same as any other FastAPI endpoint:

```python
@page.stat("Books Without Publisher")
async def get_books_without_publisher(session: AsyncSessionDep) -> int:
    result = await session.execute(
        select(func.count(models.Book.id)).where(models.Book.publisher_id.is_(None))
    )
    return result.scalar_one()
```
