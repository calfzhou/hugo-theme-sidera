---
date: 2026-10-25T00:12:00+08:00
lastmod: 2026-10-25T10:06:00+08:00
title: "Structured tables"
params:
  ai_label: generated
---

Use native Markdown tables for simple rows and columns. `rich-table` adds multiple
header rows, merged header/body cells and Markdown-rich cell content. It emits a
native table with explicit header associations, not an interactive spreadsheet.
Reading, scrolling and optional sticky positioning work without JavaScript.

## Authoring syntax

Use a paired `<` shortcode, including when nested inside a fold, tab, box or grid
cell. Its body is YAML or JSON data, not a Markdown container.

```text
{{</* rich-table caption="Paper sizes" */>}}
headers:
  - - {text: Series, rowspan: 2}
    - {text: Paper, colspan: 2}
  - [Size, Dimensions (mm)]
rows:
  - - {text: A series, header: row, rowspan: 2}
    - A4
    - "210 × 297"
  - [A3, "297 × 420"]
{{</* /rich-table */>}}
```

`headers` is an array of rows. A flat array of strings/cell objects is also accepted
as shorthand for a single header row. Omit `headers` or use `headers: []` for a
headerless table. `rows` is a required, nonempty array of body rows. A row is an
array of cells. The first header row defines the column count; without headers,
the first body row defines it.

A string is a cell's Markdown text. Quote numeric, boolean-looking or date-like
text so YAML does not turn it into another type. Use `""` for an empty cell.
An object has these fields:

| Cell field | Meaning |
|---|---|
| `text` | Required Markdown string; may be empty |
| `colspan` | Positive integer; default 1 |
| `rowspan` | Positive integer; default 1 |
| `align` | Optional start, center or end; defaults to the starting column's alignment |
| `header` | Body cells only: row for a row header, or data for an ordinary cell |

All cells in `headers` are column headers. In `rows`, cells default to data cells;
`row_headers=true` makes cells starting in column one row headers by default.
A cell's explicit `header: data` opts out of that default. Row headers may span
several rows or columns, subject to the same placement rules as data cells.

## How merging works

Cells fill the next available position from left to right. **Omit positions covered
by an earlier rowspan**; do not insert nulls or empty-string placeholders. In the
example, the A3 row has two cells because A series already occupies its first slot.
An entirely covered row is represented by an empty array, `[]`.

Each span occupies a rectangle. Overlaps, unfilled slots and cells extending beyond
the table width are errors. Every row must cover the same logical column count,
although it may contain fewer authored cells. Each rowspan must end within its own
section: an HTML cell cannot cross from `thead` into `tbody`.

A row-header cell belongs inside `rows`, even if it is visually next to several data
rows. It renders as `th` in the body; it is not a column-header cell extending down
from the header section. Generated `id`/`headers` associations connect data cells to
all overlapping column headings and applicable row headings to their left.

## Markdown cells

Cells support paragraphs, emphasis, links, images, lists, math and ordinary code
fences through the native page Markdown renderer. Source-relative links/resources
resolve against the owning page, including when data comes from a subdirectory.
Keep Goldmark raw HTML disabled. Headings and active embeds diagnose; nested
shortcodes are not a cell-data interface. The table itself may be nested in supported
Sidera containers using the usual outer-`%` / inner-`<` notation.

Use YAML block scalars for substantial cell content:

```yaml
rows:
  - - {text: Notes, header: row}
    - text: |
        - Keep **one clear observation**.
        - Link to the [source](source.txt).
        - Explain the relationship $x^2$.
      colspan: 2
      align: start
```

This body defines three columns. A header section, if present, must also define
three columns. Code fences in a block scalar remain code, not executable source.

## Column alignment and sizing

Optional `columns` contains one object per logical column. Each object supports
`align` (start, center, end; default start) and `min_width` (integer 32–720 pixels).
An omitted width inherits the shortcode's `cellwidth` (default 140 pixels).

```yaml
columns:
  - {min_width: 100}
  - {align: center, min_width: 80}
  - {align: end, min_width: 180}
headers: [Label, Count, Description]
rows:
  - [Example, "2", "A short description"]
```

Widths are minimums, not fixed widths or percentages. Spanning cells use the sum of
the covered columns' minimums. Content may make columns wider; narrow screens scroll
the table instead of splitting rows into cards. Cell `align` overrides the column
setting. Text stays top-aligned in body cells; column headings are vertically centered.

## Choose the separators

`borders="rows"` is the default: the same horizontal rules as ordinary Markdown
tables, without vertical separators. Use `borders="grid"` when merged headings or
substantial cell content benefit from visible column boundaries:

```text
{{</* rich-table src="comparison.yaml" borders="grid" caption="Comparison" /*/>}}
```

Grid mode adds thin solid vertical separators in the same subtle line color. It
keeps the existing horizontal rules and draws only at real cell edges—never through
a merged cell or around the whole table as a card frame. There is no automatic
switch based on span count; the author chooses each table's presentation.

Ordinary Markdown tables can opt into the same separators with a native table
attribute. Place the attribute line immediately below the table:

```markdown
| Feature | Result |
| --- | --- |
| Reading | Supported |
| Writing | Supported |
{.table-grid}
```

Without `.table-grid`, ordinary tables are unchanged. These selectors apply only
to the selected table's own cells, not to nested tables or code line-number tables.

## Captions and scrolling

`caption` is optional literal text rendered as a native figure caption **below the
table**, centered with the same subdued typography as other Sidera captions. It is
outside the scroll region, so it stays visible and centered even when a wide or tall
table is scrolled. The table is accessibly named by that caption, which also names
the keyboard-focusable scroll region. Without a caption, `label` names the table
and region; its default is localized “Scrollable data table”. Give nearby tables
distinct, meaningful captions or labels.

`sticky_header=true` keeps the whole multi-row header visible inside the table's
scroll region. It gives that region a default maximum height of 480px. `max_height`
can explicitly set 160–1200px, with or without a sticky header. Without either option,
there is no vertical height limit.

`sticky_first_column=true` keeps first-column cells visible while scrolling sideways.
Every cell starting in that column must have `colspan: 1`: a merged cell covering
several columns cannot be partially pinned. Both sticky options default to false.
Only pinned areas use an opaque background so text does not show through from
underneath. In a differently colored container, site CSS can set
`--rich-sticky-bg` to match that containing surface.

The table inherits normal Markdown table typography, cell padding, quiet header
shading and dashed body-row separators. Vertical separators are opt-in; there is
no card frame. Colors follow light/dark/auto mode. Printing removes
the height limit and sticky positioning and lets cell text wrap. Very wide tables
may still need a landscape or larger paper setting. Printing does not open a closed
parent disclosure. Forced-colors mode retains visible grid boundaries.

## Data from a page resource

```text
{{</* rich-table src="data/comparison.yaml" caption="Comparison" /*/>}}
```

`src` is an exact current-page resource key ending in `.yaml`, `.yml` or `.json`.
Use bodyless `/>` notation. Inline data and `src` are mutually exclusive. File
contents use the same schema and validation; no network or arbitrary filesystem
lookup is performed. Native Hugo resource/publication rules still apply: source
data is not a private store or a redaction mechanism.

## Bounds and diagnostics

Data is limited to 256 KiB, 32 columns, 16 header rows and 200 body rows. Each cell's
text is at most 16 KiB. Spans must be integral numbers, not strings, booleans,
fractions or zero. All option/data/cell/column keys are validated. Diagnostics include
the shortcode position and, for cell/topology errors, the section, row and cell.

Safe `class` and `id` tokens are supported like other content components. The native
shell makes generated header IDs unique per rendered table, including repeated
cross-page Content/Summary. Author-supplied IDs still need to be unique. Custom
layouts that bypass the shell and repeat rendered content should pass their final
HTML through `tables/instances.html` with `page` and `html` before output. This helper
accepts trusted rendered HTML, never raw Markdown or resource bytes.
