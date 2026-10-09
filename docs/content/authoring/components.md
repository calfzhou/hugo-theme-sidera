---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-09T22:10:00+08:00
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
