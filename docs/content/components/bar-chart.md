# Bar Chart

A bar chart for categorical data — one bar per category, with an optional legend.

```python
@page.bar_chart("Books per Genre", description="Absolute book count for each genre")
async def get_books_per_genre(session: AsyncSessionDep):
    ...
    return [{"label": row.name, "value": row.count} for row in result]
```

## Decorator

```python
page.bar_chart(
    name: str,
    *,
    description: str | None = None,
    icon: spec.Icon | None = None,
    color: spec.Color | None = None,
    caption: str | None = None,
    caption_description: str | None = None,
    caption_icon: spec.Icon | None = None,
    config: dict[str, spec.BarChartConfigValue] | None = None,
    data_key: str | None = None,
    refresh: timedelta | None = None,
)
```

The decorated function is registered as `GET /<page-id>/bar-chart/<bar-chart-id>`.

## Return value

```python
type BarChartData = (
    list[dict[str, int | float | str]]
    | list[dict[Literal["data", "value"], int | float | str]]
    | object
)

class BarChartResponce(TypedDict):
    config: NotRequired[dict[str, BarChartConfigValue]]
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    refresh: NotRequired[int | None]
    data: BarChartData

type BarChart = BarChartData | BarChartResponce
```

The simplest shape is a bare list of `{"label": ..., "value": ...}` dicts:

```python
return [{"label": "Fiction", "value": 128}, {"label": "History", "value": 47}]
```

Return a `BarChartResponce` dict instead when you need to override `config`, `icon`, `color`, or `refresh` per response.

## Config and legend

`config` maps a data key to display metadata used for the legend:

```python
class BarChartConfigValue(TypedDict):
    name: NotRequired[str]
    color: NotRequired[Color]
    icon: NotRequired[Icon]
```

`data_key` selects which field in your row dicts holds the series value, for shapes that don't already use the default `label`/`value` keys.
