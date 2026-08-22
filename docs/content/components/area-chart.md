# Area Chart

::: warning Not yet available
`AreaChart` is defined in `openadmin.spec` and included in the `Component` union, but `AdminPage` doesn't expose an `area_chart(...)` decorator yet — the implementation is present in the source but commented out. This page documents the spec shape as a preview of what's coming; there's no way to register one today.
:::

## Spec shape

```python
class AreaChartComponent(TypedDict):
    type: Literal["area-chart"]
    id: str
    name: str
    description: str | None
    refresh: int | None
    method: HttpMethod
    form: JsonSchema | None
    body: JsonSchema | None
    query: JsonSchema | None

type AreaChart = AreaChartComponent
```

In the meantime, a time-series trend can be approximated with a [bar chart](/components/bar-chart).
