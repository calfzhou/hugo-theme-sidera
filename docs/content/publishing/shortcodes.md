---
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
HTML, event handler, SVG or executable argument. Colors: neutral/red/yellow/green.
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

Grid takes only cells/whitespace, at least one cell. Blocks in labels fail. Container
bodies retain native headings, links, alerts, math and fences in one Markdown pass.
No arbitrary plugin nesting or automatic fold-heading behavior is promised.

## Small leaves and cards

| Shortcode | Arguments and defaults |
|---|---|
| kbd | required nonblank literal text |
| mark | required literal text; color=yellow (red/green/yellow) |
| u | required literal text; no whitespace is inserted around output |
| quot | required literal text; ornament=true |
| copy | required literal text; prefix='' (not copied) |
| link | required href/text; icon=link (empty hides); image='', alt='' |

`kbd`, `mark`, `u` are inline. Other leaves are block calls on their own lines.
Text is escaped, not interpreted Markdown. Link destinations reuse exact source
Page/resource resolution or safe local/HTTP(S)/mailto URLs; no remote metadata
fetch. `image` takes visual priority over a named icon; alt defaults to decorative
empty and is invalid without an image. Local/HTTP(S) images are browser-loaded,
not rehosted/fetched at build time. Icons=false does not hide content artwork.

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

## Overrides

Hugo-native site shortcode/render-hook overrides win normally. Nested leaf overrides
must retain `components/leaf.html`; blockquote hooks must retain the private-node
branch, and link hooks the `sidera-inline:` branch. Examples are the shipped thin
wrappers. Never treat author HTML or resource bytes as trusted output. Contributor
entry points and tests live in repository AGENTS.md, not this manual's content tree.
