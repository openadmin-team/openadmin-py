# Pie Chart

A pie chart for showing a proportional breakdown across categories.

```python
@page.pie_chart("Genre Distribution", description="Share of books across all genres")
async def get_genre_distribution(session: AsyncSessionDep) -> spec.PieChart:
    ...
    return {"data": [{"name": row.name, "value": row.count} for row in result]}
```

## Decorator

```python
page.pie_chart(
    name: str,
    *,
    description: str | None = None,
    config: dict[str, spec.PieChartConfigValue] | None = None,
    icon: spec.Icon | None = None,
    name_key: str | None = None,
    value_key: str | None = None,
    color: spec.Color | None = None,
    caption: str | None = None,
    caption_description: str | None = None,
    caption_icon: spec.Icon | None = None,
    refresh: timedelta | None = None,
)
```

The decorated function is registered as `GET /<page-id>/pie-chart/<pie-chart-id>`.

## Return value

```python
type PieChartData = (
    list[dict[str, int | float | str]]
    | list[dict[Literal["name", "value"], int | float | str]]
    | object
)


class PieChartResponce(TypedDict):
    config: NotRequired[dict[str, PieChartConfigValue]]
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    data: PieChartData
    refresh: NotRequired[int | None]


type PieChart = PieChartData | PieChartResponce
```

There are two ways to shape the data. Use the default `name`/`value` keys and return a bare list:

```python
@page.pie_chart("Genre Distribution")
async def get_genre_distribution(session: AsyncSessionDep) -> spec.PieChart:
    return {"data": [{"name": g.name, "value": count} for g, count in rows]}
```

Or use your own field names and tell the chart which ones to read with `name_key`/`value_key`:

```python
@page.pie_chart("Genre Distribution", name_key="genre", value_key="count")
async def get_genre_distribution(session: AsyncSessionDep):
    return [{"genre": g.name, "count": count} for g, count in rows]
```

## Config and legend

`config` maps a data key to display metadata used for the legend, the same shape as on [bar charts](/components/bar-chart):

```python
class PieChartConfigValue(TypedDict):
    name: NotRequired[str]
    color: NotRequired[Color]
    icon: NotRequired[Icon]
```
