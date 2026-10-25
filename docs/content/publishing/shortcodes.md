---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-25T10:06:00+08:00
title: "Shortcode reference"
params:
  ai_label: generated
---

All theme shortcode arguments are **named**. Unknown options, wrong types and unsafe
paths diagnose. Quote literal numeric strings; booleans are true/false, not quoted.
Use outer `%` for standalone containers, nested `<` for containers inside containers,
and `<` for every self-contained leaf. See [composition](../authoring/components.md).
Escaped examples below are text, not live provider calls.

## Containers

Common optional `class` / `id` strings use safe ASCII tokens (letter/underscore,
then letters/digits/underscore/hyphen; classes may be space separated). No style,
HTML, event handler, SVG or executable argument. Colors: red, orange, yellow, green,
cyan, blue, purple, pink and neutral. These are adaptive Sidera families, not CSS
keyword values; see [content colors](../authoring/components.md#content-colors).
`child` permits empty or codeblock; it adjusts presentation, not inclusion behavior.

| Shortcode | Arguments and defaults |
|---|---|
| block | common class/id only |
| folding | required nonblank title (inline Markdown); open=false; color=neutral; child='' |
| box | title='' (inline Markdown); color=neutral; child='' |
| grid | columns integer 1–6 OR min_width integer 64–720 pixels; mutually exclusive; default auto-fill minimum 240px |
| cell | common class/id only; immediate grid parent required |
| timeline | common class/id only; one or more direct events, whitespace only between |
| event | required nonblank literal string title; common class/id; immediate timeline parent |
| tabs | active=1 (one-based integer within tab count); align=start/center/end; label=localized “Content tabs”; common class/id |
| tab | required nonblank literal title; common class/id; immediate tabs parent |

Grid takes only cells/whitespace, at least one cell. Tabs takes only direct tabs and
whitespace, at least one tab. Tab bodies use the same single Markdown pass as other
containers; nesting tabs inside a tab, box, fold or grid cell is supported. Blocks in labels fail. Container
bodies retain native headings, links, alerts, math and fences in one Markdown pass.
No arbitrary plugin nesting or automatic fold-heading behavior is promised.

## Small leaves and cards

| Shortcode | Arguments and defaults |
|---|---|
| kbd | required nonblank literal text |
| mark | required literal text; color=yellow (the same nine named families as containers) |
| u | required literal text; no whitespace is inserted around output |
| icon | required name from the built-in/site icons registry; optional palette color; label='' (decorative) |
| hashtag | required literal text; href='' (non-link chip); color=blue |
| blur / psw | required literal text; cosmetic blur or concealment, revealable by hover/focus/touch |
| emp / wavy / del / sup / sub | required literal text; emphasis dots, wave underline, deletion, superscript, subscript |
| tip | required literal text for the annotation; paired body for noninteractive inline Markdown |
| download | required current-page bundle src; name=source basename; text=download filename |
| code-inline | paired nonblank single-line code body; lang=text; unknown lexer falls back to plain text |
| quot | required literal text; ornament=true |
| copy | required literal text; prefix='' (not copied) |
| link | required href/text; icon=link (empty hides); image='', alt='' |

`kbd`, `mark`, `u`, `icon`, `hashtag`, all text decorations, `tip`, `download` and
`code-inline` are inline. Other leaves are block calls on their own lines.
Text is escaped, not interpreted Markdown. Link destinations reuse exact source
Page/resource resolution or safe local/HTTP(S)/mailto URLs; no remote metadata
fetch. `image` takes visual priority over a named icon; alt defaults to decorative
empty and is invalid without an image. Local/HTTP(S) images are browser-loaded,
not rehosted/fetched at build time. Icons=false does not hide content artwork.

## Inline controls and attachments

`icon` uses the same validated SVG registry as theme UI: built-in names or site
`data/icons.yaml` entries. No image URLs, raw SVG or style argument. Omitted color
inherits surrounding text; explicit color uses a Sidera family. Use `label` when the
icon conveys meaning on its own. Authored icons remain visible with `icons=false`;
the decorative icon on a download link does not.

`hashtag` accepts the same safe destinations as `link`, using `href` consistently.
Omitting `href` produces a noninteractive chip, not an empty anchor. Colors do not
cycle across builds. `sup` and `sub` always inherit the surrounding text color.

`tip` is an annotation, not a callout. Write `text="Explanation"` and put the term
between opening/closing shortcodes; its body may contain emphasis, inline code or
math, but not links, controls, images or blocks. Hover/focus/click shows the bubble;
Escape dismisses it when enhanced. Without JavaScript, hover/focus still shows it.

`blur` and `psw` are **not password protection or redaction**. Their source text is
public and available to assistive technology. Hover previews; click/Enter/Space
reveals or conceals. Without JavaScript, focus reveals. Printing reveals the text,
tab panels and annotations. Never put a real password or secret in these components.

`download` only publishes an existing native page-bundle attachment. `src` may
contain subdirectories, spaces and Unicode; traversal, encoded paths, globs,
absolute paths and URLs reject. A content Page is not an attachment. Optional
`name` is a single filename (not a path); labels are literal escaped text. Bytes
are unchanged; no remote fetching, file execution or platform-specific MIME logic.
The browser controls whether the native `download` hint opens or saves the file.

`code-inline` trims surrounding whitespace and rejects line breaks. Interior spaces
are retained through HTML minification, including in string literals. It reuses
native Chroma and Sidera's adaptive syntax colors, without block wrappers, line
numbers, copy controls or configurable highlighter options. Use named `lang`, not
the positional argument of older site-owned implementations. Site shortcodes still
override theme shortcodes until the site owner deliberately removes the overrides.

## Structured tables

`rich-table` is a paired `<` leaf with YAML/JSON body, or a bodyless
`{{</* rich-table src="table.yaml" /*/>}}` call. It supports Markdown cells,
multi-row headers and rectangular row/column spans within header or body sections.

| Argument | Contract |
|---|---|
| src | Optional exact current-page `.yaml` / `.yml` / `.json` resource; excludes inline body |
| caption | Optional literal caption below the table, centered like other figure captions; empty suppresses it |
| label | Nonblank scroll-region label; localized default; caption takes precedence |
| borders | rows (default) or grid; grid adds subtle vertical separators at actual cell boundaries |
| cellwidth | Default per-column minimum: integer 32–720px, default 140 |
| row_headers | Boolean, default false; cells starting in the first body column become row headers |
| sticky_header | Boolean, default false; pins the complete header inside a bounded scroll region |
| sticky_first_column | Boolean, default false; first-column cells must have colspan=1 |
| max_height | Optional integer 160–1200px; defaults to 480 with sticky_header, otherwise unbounded |
| class / id | Common safe tokens |

The data object accepts `headers`, required `rows`, and optional `columns`. Strings
are Markdown cells; objects add `text`, `rowspan`, `colspan`, `align`, and body-only
`header: row` / `data`. Omit slots covered by rowspans; empty strings are real cells.
Header-to-body rowspans, overlapping rectangles and holes diagnose. See
[structured tables](../authoring/tables.md) for the schema, examples, accessibility,
print behavior and size limits.

## Images

```text
{{</* image src="thumbnail.jpg" original="original.jpg" alt="A useful description" width=320 */>}}
```

Required strings: `src` and explicit `alt` (empty for decorative). Optional strings:
`original=''`, `background` (transparent or hex only), `caption`, class/id; optional
positive integer pixel width/height; loading=lazy or eager (default lazy, async decoding).
Caption omitted follows auto_caption/alt; explicit text overrides, empty or no-caption
suppresses. No arbitrary CSS, processing, cropping or artwork rewriting.

Src/original independently resolve exact native bundle/cross-bundle/assets or
same-site/HTTP(S) image URLs. Unsafe schemes/protocol-relative/traversal reject.
Original enables a native-link thumbnail plus progressive modal zoom/pan/download;
no request for a distinct original until opened, no gallery/editor/automatic retry.
No-JS opens original directly. Download is a native anchor: cross-origin policies
may open rather than save. Alt/caption remain independent and escaped.

`class="invert-when-dark invert-soft"` applies the optional soft visual conversion
to the image, not its caption; the expanded original preserves that effect.
See [image inversion classes](../authoring/_index.md#images-captions-and-attributes).

## Code resources

| snippet argument | Contract |
|---|---|
| src | Required exact resource key |
| scope | page (default), or shared under assets/snippets/ |
| from / to | Positive inclusive line bounds; omitted first/last; no clamp |
| title | Basename default; explicit nonblank plain string |
| lang | Extension default; empty/text is plain text; unknown lexer falls back to text |
| options | Comma-separated supported native highlighter options below |

Supported options: linenos=true/false/inline/table; linenumbersintable=true/false;
linenostart=positive integer; hl_lines=selection-relative positions/ranges;
anchorlinenos=true/false; lineanchors=safe unique prefix. Defaults start numbering
at the first selected source line. No inline/wrapper/data override option. At site
config level use native lineNos=true and lineNumbersInTable=false for inline numbers;
lineNos='inline' is not accepted there on the verified Hugo version.

Full downloads preserve complete original bytes; selection/copy is not redaction.
Only valid text resources, not arbitrary filesystem/network input or execution.
Read [code resources](../authoring/snippets.md) for exact line-ending/publication rules.

## Media and badges

| Shortcode | Arguments and supported input |
|---|---|
| video | required src: current-page MP4 key or explicit HTTP(S) MP4; width optional integer 1–8192; title optional nonblank literal; disabled=false |
| diagramsnet | required src: exact current-page .drawio resource; optional nonblank literal caption |
| badge_github | required string user/repo; branch optional string; release=false; disabled=false |

Video attaches media only on Load video and never auto-plays; no-JS retains file link.
Drawio is a local one-page uncompressed viewer, not an editor or arbitrary stencil
loader. Badge images automatically contact Shields when enabled; disabled keeps
only the repository link. Provider reliability and media codecs remain external limits.
No diagram title/disabled aliases are accepted. Native Mermaid is a fence, not a
shortcode; only caption/class/id attributes are supported. Read
[diagrams, video and badges](../authoring/diagrams.md) before enabling them.

## Interactive charts

`echarts` accepts either an inline JSON body or an exact current-page `.json` `src`,
plus optional `.json` `data`. Both forms share the native `echarts` fence renderer.
Use `{{</* echarts src="chart.json" /*/>}}` for a bodyless shortcode; `/>` is required.
Optional `caption` is nonblank plain text; `height` is 200–1200 pixels
(default 360); safe `class`/`id` tokens are supported. No `title`, `disabled`, remote
URL, CSV, YAML or JavaScript callback aliases. Line, bar, pie/donut and scatter charts
stay interactive in local sandboxed frames, with source viewing and a self-contained JSON download.
Read [interactive charts](../authoring/charts.md) for examples, dataset conflicts,
option boundaries, accessibility and CSP requirements.

## JSX tools (opt-in)

`jsx` accepts a module body or an exact page-bundle `src` ending in `.jsx`. Optional
arguments are `css`, `title`, `caption`, `fallback`, `appearance` (`plain` by default,
or `card`), `mode` (`page` by default, or `sandbox`) and sandbox `height` (160–1200
pixels, default 280). Title is a plain-text label above the component; caption is
plain text below. Neither is required. Plain appearance has no outer border,
background or padding; appearance is independent of execution mode. Bodyless calls
use `/>`. Requires the site's explicit `params.jsx = true`; unlike `snippet`, this compiles executable
JavaScript. See [Interactive JSX](../authoring/jsx.md) for imports, trust and fallbacks.

## Overrides

Hugo-native site shortcode/render-hook overrides win normally. Nested leaf overrides
must retain `components/leaf.html`; blockquote hooks must retain the private-node
branch, and link hooks the `sidera-inline:` branch. Examples are the shipped thin
wrappers. Never treat author HTML or resource bytes as trusted output. Contributor
entry points and tests live in repository AGENTS.md, not this manual's content tree.
