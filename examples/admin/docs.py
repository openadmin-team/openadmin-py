# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin import fastapi, spec

page = fastapi.AdminPage("Docs", icon="dock")


@page.markdown("Markdown Guide - Part 1", icon="heading", color="indigo")
def markdown_guide_part_1() -> spec.Markdown:
    return """
# Markdown Guide - Part 1: Text & Headings

This is a long-form guide that exercises most of the Markdown syntax the
*typeset* renderer supports. It is split across three components so each
one stays a manageable size.

## Headings

# Heading level 1
## Heading level 2
### Heading level 3
#### Heading level 4
##### Heading level 5
###### Heading level 6

## Emphasis

Text can be **bold**, *italic*, or ***bold and italic*** at once. Outdated
text can be ~~struck through~~, and important phrases can be
<mark>highlighted</mark> so they stand out.

Inline code looks like `const answer = 42` when you need to reference a
symbol without pulling in a full code block.

## Links

- An inline link: [OpenAdmin documentation](https://example.com/docs)
- A reference-style link: [the CommonMark spec][commonmark]
- A bare autolink: <https://example.com>

[commonmark]: https://example.com/commonmark "CommonMark Spec"

## Small print

Formulas need superscripts, like E = mc<sup>2</sup>, and subscripts, like
H<sub>2</sub>O.

The <abbr title="Hypertext Markup Language">HTML</abbr> spec defines this
as an inline element.

To save your work, press <kbd>Ctrl</kbd> + <kbd>S</kbd>.

---

Part 2 continues with lists, blockquotes, and tables.
"""


@page.markdown("Markdown Guide - Part 2", icon="list-checks", color="teal")
def markdown_guide_part_2() -> spec.Markdown:
    return """
# Markdown Guide - Part 2: Lists, Blockquotes & Tables

## Unordered lists

- First item
- Second item
  - Nested item one
  - Nested item two
- Third item

## Ordered lists

1. Preheat the oven
2. Mix the batter
3. Bake for 25 minutes
   1. Check at the 20 minute mark
   2. Rotate the pan if it browns unevenly

## Task lists

- [x] Write the first draft
- [x] Add code samples
- [ ] Proofread everything
- [ ] Ship it

## Definition lists

<dl>
<dt>Markdown</dt>
<dd>A lightweight markup language for formatting plain text.</dd>
<dt>CommonMark</dt>
<dd>A strongly defined, highly compatible specification of Markdown.</dd>
</dl>

## Blockquotes

> Simplicity is the ultimate sophistication.
>
> — Leonardo da Vinci

> Blockquotes can nest too:
>
> > Like this inner thought, which stays indented under its parent.

---

## Tables

| Feature    | Supported | Notes                       |
| :--------- | :-------: | ---------------------------: |
| Headings   |    yes    |         h1 through h6         |
| Task lists |    yes    |            GFM only           |
| Alignment  |    yes    |     left, center, and right   |

| Left | Center | Right |
| :--- | :----: | ----: |
| a    |   b    |     c |
| aa   |   bb   |    cc |

Part 3 wraps up with code blocks, media, and a disclosure.
"""


@page.markdown("Markdown Guide - Part 3", icon="code", color="violet")
def markdown_guide_part_3() -> spec.Markdown:
    return """
# Markdown Guide - Part 3: Code, Media & Extras

## Inline and block code

Reference a symbol inline with `openadmin.fastapi.AdminPage`, or drop in a
full block:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

```bash
uv run fastapi dev examples/main.py --port 8000
```

```json
{
  "name": "openadmin",
  "type": "markdown"
}
```

## Images

![OpenAdmin logo](/favicon.svg)

## Disclosures

<details>
<summary>Click to expand for more detail</summary>

This content is hidden by default and only shown once the reader opts in,
which is handy for changelogs, FAQs, or anything that would otherwise
clutter the page.

</details>

---

That wraps up the three-part Markdown guide. Thanks for reading all the
way to the end!
"""
