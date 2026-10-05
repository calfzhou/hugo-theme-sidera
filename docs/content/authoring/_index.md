---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T23:10:14+08:00
title: "Write content"
params:
  ai_label: generated
  children:
    order: [components, snippets, diagrams, example]
---

Use ordinary Markdown first: headings, lists, tables, links, quotes, fenced code and
native Hugo footnotes. The safe renderer does not require raw HTML. Optional
[components](components.md), [code resources](snippets.md) and [diagrams/media](diagrams.md)
solve specific tasks; see a [small live example](example/_index.md).

## Story typography and AI disclosure

```yaml
---
title: An unhurried walk
type: story
params:
  ai_label: polished
---
```

Native `type: story` selects larger prose, indented/justified paragraphs and decorated
headings in shared article bodies. Other native types keep ordinary styling; it is
not a preset or content organization model. `cascade.type: story` applies it to a
branch; a local non-story type opts out. Lists/code/captions are not indented prose.

`params.ai_label` is an explicit editorial statement, independent of type, author
identity and license. Supported strings are `manual`, `reviewed`, `polished`,
`generated`; empty clears. Labels are localized as Written entirely by a human,
AI-reviewed, AI-polished, AI-generated. Do not write `ai-generated` as the enum or
apply a default unless it is true for that content. Icons-off retains disclosure text.
The inherited [Stellar][stellar] label colors do not meet small-text AA contrast everywhere.

## Source-relative links

```markdown
[Read a page](../other/index.md)
[Read its heading](../other/index.md#useful-heading)
[Return to a branch](../_index.md)
```

Links are relative to the actual source file directory, not its dated published URL.
Include exact `index.md`, `_index.md` or plain filename; no basename search or
invented aliases. Exact resources resolve within/cross bundles and global assets.
Queries/fragments survive. Encode spaces or use angle destinations; explicit
`index.zh.md` selects that actual language, not an automatic translation switch.
Moving source may require link edits; changing only permalink rules does not.

Ordinary public/web paths remain authored URLs and are not crawled. `[Home](/)`
means host root, not the current language/deployment path. Use source `_index.md`
links, native pageRef, or the configured-Markdown native Home extension when you
need those prefixes. Missing `.md` destinations warn; strict builds fail. Optional
site `link_heading_checks: true` checks native heading fragments, not every shortcode
or custom HTML ID. External HTTP(S) links open safely in new tabs.

## Images, captions and attributes

```markdown
![An observable pattern|320](pattern.svg "Caption from title")
{.invert-when-dark #pattern loading="eager"}
```

Import the parser defaults from [Getting started](../getting-started/_index.md).
A direct standalone image gets a caption from nonempty title, then cleaned alt.
Alt remains alternative text; terminal positive `|width` or `|widthxheight` supplies
native dimensions. Backgrounds are transparent; artwork bytes are never recolored.
Default thumbnails use lazy loading and async decoding; optional eager loading is
useful for an opening image. No dimensions are invented when absent.

`auto_caption: false` disables automatic captions for a page/default; `.no-caption`
suppresses one image. Prose-inline, linked, list and table images do not get automatic
figures. Explicit shortcode/figure captions remain. Native next-line attributes work
on standalone images; loose-list indentation matters and tight-list image attrs may
not attach. This is Hugo syntax, not every inline-attribute dialect.

`invert-when-dark` / `invert-when-light` filter the marked element itself. Image
classes do not invert captions; a marked container filters the whole group. Nested
filters compound. Use the [image shortcode](../publishing/shortcodes.md#images) for
explicit background, reliable nested attributes, caption or original-image access.
No automatic gallery/lightbox is added to ordinary Markdown images.

## Alerts, code and math

Native blockquote alerts use `> [!NOTE]`, TIP, IMPORTANT, WARNING or CAUTION, followed
by quoted Markdown. Ordinary fences have native Chroma highlighting, copy UI and
manual fallback. Source code is data, never executed.

With the passthrough import, `$x^2$` is inline math and `$$...$$` is display math.
Escape literal currency as `\$`; code remains non-math. Native build-time KaTeX emits
HTML+MathML with trust disabled and strict errors. Matching local CSS/fonts load
conditionally, with no client math runtime or CDN. Wide display math scrolls locally.
Malformed TeX fails; arbitrary commands, global macros and universal CSP/AT support
are not promised. Describe formulas in prose for search: math subtrees are excluded.

[Hugo's Markdown guidance](https://gohugo.io/content-management/formats/) covers the
underlying engine. Avoid `useEmbedded='always'` if you need theme render hooks.

[stellar]: https://xaoxuu.com/wiki/stellar/
[stellar-144]: https://github.com/xaoxuu/hexo-theme-stellar/tree/1.44.0
[xaoxuu]: https://xaoxuu.com/
