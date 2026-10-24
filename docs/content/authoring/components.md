---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-23T23:08:07+08:00
title: "Compose content"
params:
  ai_label: generated
---

Containers combine Markdown without turning raw HTML on. Use **outer `%` notation**
for the outermost container and **nested `<` notation** for every inner component.
Self-contained leaves always use `<`, even alone. Blank lines matter.

```text
{{%/* folding title="Supporting material" */%}}
Ordinary Markdown and $x^2$.

{{</* grid columns=2 */>}}
{{</* cell */>}}
A first cell with **formatted text**.
{{</* /cell */>}}
{{</* cell */>}}
{{</* box title="Remember" color="green" */>}}
Keep the source small.
{{</* /box */>}}
{{</* /cell */>}}
{{</* /grid */>}}
{{%/* /folding */%}}
```

Use `folding` for native disclosure, `box` for a titled/color presentation,
`grid`/`cell` for responsive columns, and `block` for safe classes/IDs. Grid accepts
only direct cells and whitespace; cell needs an immediate grid parent. Container
titles support inline Markdown, links and math, not blocks or trusted author HTML.
Native headings remain in the page's TOC; a fold title itself is not a heading.

## Content colors

`mark`, `box` and `folding` share these names: **red, orange, yellow, green, cyan,
blue, purple, pink, neutral**. Names are lowercase Sidera color families, not fixed
CSS keyword colors. Omitting `color` keeps the defaults: yellow for `mark`, neutral
for `box` and `folding`.

```text
{{</* mark text="A detail to remember" color="purple" */>}}

{{%/* box title="A useful connection" color="cyan" */%}}
Body text stays neutral. {{</* mark text="A separate highlight" color="pink" */>}}
{{%/* /box */%}}
```

Each family has text, accent, border, surface and highlight variants. Boxes and
folds use quiet surfaces and borders; their titles use the text variant. Marks
use a stronger highlight with neutral text. Each nested component selects its own
family, including a default neutral container inside a colored one.

Native Markdown alerts share the palette: note → blue, tip → green,
important → purple, warning → yellow, caution → red. Their bars use the accent
variant and their visible labels use the text variant. Keep meaningful words:
color alone should not carry a warning, status or category distinction.

Colors follow light/dark/auto mode without component JavaScript. Printed components
use light colors even from dark mode; marks also receive an underline so emphasis
survives when background printing is disabled. This does not expand closed folds
or provide a separate page-wide print layout. Forced-colors mode uses system colors
and keeps mark outlines.

For site CSS customization, `--palette-<name>-text`, `-accent`, `-border`, `-surface`
and `-highlight` are shared family tokens. Define overrides at `:root`; adaptive
values can use CSS `light-dark(light-value,dark-value)`. Check contrast in both modes
and print after overriding them. Site interaction accents and links reuse the cyan and blue families with their own
interface roles. Chart palettes and image artwork have independent styling.

## Timeline and small leaves

```text
{{%/* timeline */%}}
{{</* event title="First observation" */>}}
Ordinary Markdown. Authors control the order and label.
{{</* /event */>}}
{{</* event title="Later" */>}}
More detail, a grid or a supported leaf component.
{{</* /event */>}}
{{%/* /timeline */%}}
```

Timeline requires direct event children; event titles are literal strings, not parsed
dates/Markdown. It is authored content, not a sidebar feed or data service.

Use `kbd`, `mark` and `u` inline for escaped text. Standalone `quot`, `copy`, `link`,
`snippet`, `image`, `video`, `diagramsnet`, `echarts`, `badge_github` belong on their own lines.
Attribution is ordinary Markdown. Link cards use an authored destination/label;
optional content image/alt is separate from the named icon. Nothing fetches remote
metadata to manufacture a preview. Quote numeric text strings and use actual booleans,
not strings that happen to say false.

The [shortcode reference](../publishing/shortcodes.md) is the authoritative argument
list. No emoji shortcode or generic embed/plugin API ships. A site-owned shortcode
is not automatically safe to nest: its trusted override must preserve the component
leaf bridge. Do not enable unsafe HTML, suppress warnings or guess notation to work
around a build failure. See the [live composition](example/_index.md).
