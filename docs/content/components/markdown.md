# Markdown

A markdown component renders static or dynamic rich text on a page — guides, changelogs, release notes, or any contextual copy.

```python
@page.markdown("Release Notes", icon="scroll-text", color="indigo")
def release_notes() -> spec.Markdown:
    return """
# 1.4.0

- Added CSV export to tables
- Fixed pagination off-by-one on the last page
"""
```

## Decorator

```python
page.markdown(
    name: str,
    *,
    description: str | None = None,
    color: spec.Color | None = None,
    icon: spec.Icon | None = None,
    refresh: timedelta | None = None,
)
```

The decorated function is registered as `GET /<page-id>/markdown/<markdown-id>`.

## Return value

```python
type MarkdownContent = str


class MarkdownResponse(TypedDict):
    icon: NotRequired[Icon]
    color: NotRequired[Color]
    refresh: NotRequired[int | None]
    content: MarkdownContent


type Markdown = MarkdownContent | MarkdownResponse
```

Return a bare string for the common case, or a `MarkdownResponse` dict to override `icon`/`color`/`refresh` per response:

```python
@page.markdown("Status", refresh=timedelta(seconds=30))
async def status_markdown(session: AsyncSessionDep) -> spec.MarkdownResponse:
    healthy = await check_health(session)
    return {
        "content": "All systems operational."
        if healthy
        else "**Degraded** — investigating.",
        "color": "emerald" if healthy else "amber",
    }
```

## Supported syntax

The renderer supports GitHub-flavored Markdown plus a handful of inline HTML extras:

- Headings (`#` through `######`), emphasis (`**bold**`, `*italic*`, `~~strikethrough~~`), `<mark>highlight</mark>`
- Inline code and fenced code blocks with syntax highlighting (` ```python `, ` ```bash `, ` ```json `, ...)
- Inline, reference-style, and bare autolinks
- Superscript/subscript (`<sup>`, `<sub>`), `<abbr>`, `<kbd>`
- Ordered, unordered, and task lists (`- [x]`), including nesting
- Definition lists (`<dl>`/`<dt>`/`<dd>`)
- Blockquotes, including nested blockquotes
- Tables, with left/center/right column alignment
- Images (`![alt](src)`)
- Disclosures (`<details>`/`<summary>`)

```markdown
## Task lists

- [x] Write the first draft
- [ ] Ship it

<details>
<summary>Click to expand</summary>

Hidden by default.

</details>
```
