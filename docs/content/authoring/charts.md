---
date: 2026-10-09T22:10:00+08:00
lastmod: 2026-10-10T21:27:25+08:00
title: "Interactive charts"
params:
  ai_label: generated
---

Use an `echarts` fence or shortcode for interactive **line, bar, pie/donut and
scatter** charts. Both accept the same strict JSON configuration and share one
renderer. No front-matter flag, npm installation or remote chart service is needed.
The bundled runtime is Apache ECharts 6.1.0's unmodified **common** distribution,
not every ECharts chart type or extension.

## Inline JSON

A small bar chart needs only its axes and a data series. The caption is optional:

````text
```echarts {caption="Monthly sales"}
{
  "xAxis": {"type": "category", "data": ["Jan", "Feb", "Mar"]},
  "yAxis": {},
  "series": [{"type": "bar", "data": [12, 18, 15]}]
}
```
````

**Colors are optional.** ECharts supplies the default palette, and Sidera follows the
site's light/dark mode. To customize it, use the native `color` option (singular),
for example `"color": ["#4779c4", "#ce8643"]`; no `colors` option is supported.
Tooltips and legends are also optional: add `"tooltip": {}` for item tooltips, or
`"tooltip": {"trigger": "axis"}` to group axis values; add `"legend": {"top": 0}`
when a legend is useful. Width is responsive and height defaults to 360 pixels.
Line, bar and scatter charts need axes; pie/donut charts do not.

The paired shortcode is equivalent. Use native outer-`%`/nested-`<` notation when
placing it in a [fold, box or grid cell](components.md).

```text
{{</* echarts caption="Monthly sales" */>}}
{
  "xAxis": {"type": "category", "data": ["Jan", "Feb", "Mar"]},
  "yAxis": {},
  "series": [{"type": "bar", "data": [12, 18, 15]}]
}
{{</* /echarts */>}}
```

JSON means quoted property names, no comments or trailing commas, and no JavaScript
assignments, functions or callbacks. ECharts string formatters remain strings;
Sidera never evaluates them as code. To display an example without rendering a
chart, use a `json` or `text` fence instead of `echarts`.

## Configuration files

Keep a larger configuration in an exact resource of the current page bundle:

```text
content/posts/sales/
├── index.md
├── charts/
│   └── sales.json
└── data/
    └── monthly.json
```

```text
{{</* echarts src="charts/sales.json" caption="Monthly sales" /*/>}}
```

The configuration file contains the same JSON option object as an inline chart.
**Use `/>` for a shortcode without a body.** Hugo requires this explicit self-closing
form because the same shortcode also accepts a paired body. Use `src` or inline
JSON, never both. An empty `echarts` fence with a `src` attribute also works.

Resource keys are case-sensitive, exact and relative to the current page's resource
namespace. There is no basename guessing, wildcard, parent traversal, shared-resource
scope, arbitrary filesystem access or remote URL lookup. Spaces and Unicode in
resource filenames are supported.

## Separate datasets

Use `data` to supply one dataset independently of the presentation. For example,
`data/monthly.json` can contain:

```json
[
  {"month": "Jan", "sales": 12},
  {"month": "Feb", "sales": 18},
  {"month": "Mar", "sales": 15}
]
```

````text
```echarts {data="data/monthly.json" caption="Monthly sales"}
{
  "tooltip": {"trigger": "axis"},
  "xAxis": {"type": "category"},
  "yAxis": {"type": "value"},
  "series": [{"type": "bar", "encode": {"x": "month", "y": "sales"}}]
}
```
````

The shortcode supports `data` with either a body or a configuration file:

```text
{{</* echarts src="charts/sales.json" data="data/monthly.json" caption="Monthly sales" /*/>}}
```

Hugo reads both files at build time and puts the data into **`dataset.source`**.
The data file must be a JSON array of row objects or row arrays, not a complete
`dataset` wrapper. Native `dimensions`, `sourceHeader` and series `encode` options
can describe those rows. CSV and YAML are not supported.

With `data`, an optional `dataset` must be one object without an existing `source`,
`transform`, `fromDatasetIndex` or `fromDatasetId`. Conflicts fail the build rather
than silently overwriting data. For multiple datasets, put the complete `dataset`
array in the inline/file configuration and omit `data`. Each source is an array of
rows; client-side dataset transforms are not included. Native explicit `series.data`
still takes precedence for that series—omit it when that series should use a dataset.

**Chart data is public.** It is embedded in the generated HTML; native Hugo may also
publish the bundle's original JSON resources. This feature is not a way to hide
private data.

## Presentation and interaction

Common fence attributes and shortcode parameters:

| Name | Contract |
|---|---|
| `src` | Optional exact current-page `.json` configuration resource; excludes a body |
| `data` | Optional exact current-page `.json` dataset resource |
| `caption` | Optional nonblank plain text; also labels the chart frame |
| `height` | Integer pixel height, 200–1200; default 360; width is responsive |
| `class` / `id` | Safe native component class/id tokens; IDs must be unique on the page |

Give a meaningful caption and summarize the conclusion in the surrounding article prose.
The visual chart is not a replacement for its data or explanation.

Native ECharts options control tooltips, legends, stacking, line smoothing, donut
radii, axes, colors and data zoom. For a legend above the plot, use
`"legend": {"top": 0}`; when combining a title, legend and zoom slider, configure their
positions so the components do not overlap each other. Interaction is opt-in through those native options,
not an always-present dashboard toolbar.

Use the chart's own legend to toggle series and its configured zoom controls to
explore the data. There are no duplicate series buttons or extra reset controls
below the chart. ECharts tooltips and visual controls are pointer-oriented; not
every chart interaction is keyboard accessible. **View source** and **Download JSON**
use the same hover/focus panel as diagrams and remain keyboard accessible.
On touch devices the panel stays visible. With icons disabled, the actions have
visible text labels instead.

Charts initialize near the viewport, including after opening a closed fold, and
resize with their container. Light/dark mode changes preserve legend/zoom state.
An explicit inversion class keeps the chart palette light to avoid double inversion.
An unspecified chart background is transparent; an explicit `backgroundColor` is
respected. Reduced-motion preferences disable series and marker animations.

### Adaptive plot spacing

For a simple line/bar/scatter chart with one grid, one x-axis and one y-axis,
Sidera measures the native legend, title and axis labels to adjust the plot's top
and bottom margins. A bottom legend can wrap onto more rows without overlapping
the x-axis labels; a titleless chart no longer keeps a title-sized top gap. The
chart height stays fixed, so a taller legend leaves a shorter plotting area.
Spacing is recalculated on resize and light/dark changes; legend selections remain.
Layout corrections are applied without animation so resizing does not interpolate
between competing plot margins. This does not disable the configured animations
for ordinary chart interactions.

Explicit grid `top`, `bottom`, `height`, `y`, `y2`, `containLabel`, `outerBounds` or
`outerBoundsMode` keeps native ECharts layout instead. Multiple grids/axes/titles/
legends, vertical legends, data zoom, mixed pie charts and non-edge-anchored
components are also left author-controlled. This does not reposition a title or
legend that overlaps another component, wrap long titles, or auto-grow the chart.
If there is not enough room for an 80px plot, native margins are retained; increase
`height` or use a paginated `legend.type: "scroll"` for very crowded charts.

## Supported options and safety

The supported top-level option keys are `title`, `legend`, `grid`, `xAxis`, `yAxis`,
`dataset`, `series`, `tooltip`, `axisPointer`, `dataZoom`, `color`, `backgroundColor`,
`textStyle`, `animation`, `animationDuration`, `animationDurationUpdate`,
`animationEasing`, `animationEasingUpdate`, `animationDelay` and `animationDelayUpdate`.
`series` is an array of 1–50 objects with `type` equal to `line`, `bar`, `pie` or
`scatter`. Ordinary JSON options nested under these components use ECharts semantics;
not every semantic mistake can be diagnosed during a Hugo build.

Each JSON input and the combined configuration are limited to 1 MB; arrays to 10,000
items and nesting to 24 levels. Unknown public arguments/top-level options, unsafe
resource paths, invalid JSON and unsupported capabilities fail the build. No custom
series, maps, external extensions, dataset transforms, arbitrary graphics, toolbox,
title links, image symbols/backgrounds or HTML/CSS tooltip customization is supported.
`tooltip` must be an object; tooltips are confined **rich text**, never author HTML.
No callback revival, `eval`, network data loading or HTML rendering is enabled.

Unlike the [diagram viewers](diagrams.md), each initialized chart keeps a live SVG
renderer in its own opaque `allow-scripts` sandbox. Parent/source/origin checks bind
messages to that chart. Its CSP denies networking, images, fonts, nested frames and
eval; scripts are pinned local resources. A custom site CSP must allow same-site
frames and scripts, without relaxing the frame's own policy.

## View and download source

**View source** expands the readable JSON configuration. **Download JSON** saves the
same self-contained configuration as `chart.json`, with any separate dataset already
included in `dataset.source`. This is the build-time configuration, not a snapshot of
current legend selections or zoom, and not a byte-for-byte copy of an authored file.
You can reuse the download as an `src` file without supplying `data` again.

With JavaScript, source starts collapsed; use the panel to toggle it. Without
JavaScript or after a
renderer failure, source stays open and the download link still works. There are no
generated data tables. Explain the chart's meaning in article prose; source access
is not equivalent to an accessible interactive visualization.

Chart source and controls are excluded from search; captions and prose remain
searchable. Libraries are not requested by pages containing only literal examples
or plainified excerpts.
