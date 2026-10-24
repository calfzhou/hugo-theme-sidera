---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-24T20:06:00+08:00
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
Formatted fold titles wrap as one label beside the toggle, including inline
emphasis, links and math. Native headings remain in the page's TOC; a fold title
itself is not a heading.

## Content colors

`mark`, `box`, `folding`, `icon` and `hashtag` share these names: **red, orange, yellow, green, cyan,
blue, purple, pink, neutral**. Names are lowercase Sidera color families, not fixed
CSS keyword colors. Omitting `color` keeps the defaults: yellow for `mark`, neutral
for `box` and `folding`, blue for `hashtag`. Icons inherit text color unless
a family is explicitly selected.

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

## Tabs

Use tabs for alternative instructions, not to hide required reading:

```text
{{%/* tabs label="Installation method" active=1 */%}}
{{</* tab title="Download" */>}}
Ordinary **Markdown**, lists, links and fences.
{{</* /tab */>}}
{{</* tab title="Build locally" */>}}
## Local build

Another method, optionally containing boxes, grids or nested tabs.
{{</* /tab */>}}
{{%/* /tabs */%}}
```

The first tab is initially selected unless `active` specifies another one-based
index. Optional `align` is start, center or end; long strips scroll horizontally
without widening the page. Give multiple groups distinct `label` values. Titles
are literal text. Arrow keys move between tabs; Home/End selects the first/last.
Tab moves from the selected tab into its panel. Heading links and Sidera search
results reveal the enclosing panels and folds. Without the controller all panels
remain readable with their titles; printing also shows every panel.

## Inline details

```text
{{</* icon name="star" color="yellow" label="Favorite" */>}}
{{</* hashtag text="Research" */>}}
{{</* hashtag text="Source" href="https://example.org/" color="purple" */>}}
{{</* tip text="An explanation, not a warning box." */>}}this **term**{{</* /tip */>}}
{{</* blur text="An optional answer" */>}}
{{</* psw text="A fictional spoiler" */>}}
{{</* emp text="Emphasis dots" */>}}
{{</* wavy text="A wavy underline" */>}}
{{</* del text="Deleted text" */>}}
x{{</* sup text="2" */>}} and H{{</* sub text="2" */>}}O
{{</* code-inline lang="python" */>}}print("hello"){{</* /code-inline */>}}
{{</* download src="attachments/report.pdf" name="Report.pdf" text="Download report" */>}}
```

Text decorations use literal escaped text; superscripts and subscripts retain the
surrounding color. `tip` and `code-inline` are paired inline leaves, not Markdown
containers. Use `<` notation for them even inside a container. `blur`/`psw` conceal
only visually, never securely; do not put secrets in article source.

The attachment must exist in the current page bundle. A download can sit inline or
on its own line. Icons use only the built-in or site `data/icons.yaml` registry;
a meaningful standalone icon needs `label`. See [icon customization](../customize/icons.md).

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

Use `kbd`, `mark`, `u` and the inline details above for escaped text. Standalone `quot`, `copy`, `link`,
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
