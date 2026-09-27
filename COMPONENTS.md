# Content components — partial C2 checkpoint

Hugo **0.166.0**, independent native shortcodes. This is an implemented **partial**
checkpoint, not the complete C2 authoring contract. Container composition needs the
explicit decision described below. The user has retired emoji, timeline and enhanced
image components; ordinary Markdown images remain supported.

## Working syntax

Use **standard `{{< … >}}` notation**. Every argument is named. These components are
self-contained: no closing tag or `.Inner`. Inline components can occur in ordinary
paragraphs, tables, lists and native blockquotes/alerts. `quot`, `link` and `copy` go
on their own lines, with blank lines around them. Nested *shortcodes* currently fail
explicitly; ordinary Markdown structure is not shortcode nesting.

```text
{{< kbd text="Ctrl" >}} + {{< kbd text="`" >}}
{{< mark text="✓" color="green" >}}
{{< u text="3, -2, 3" >}}
{{< quot text="Keep the useful parts | leave room to think" >}}
{{< quot text="Without ornament" ornament=false >}}
{{< link href="../article/index.md?from=card#heading" text="Read the article" icon="icon.svg" >}}
{{< link href="example.txt" text="Open the adjacent example" >}}
{{< copy text="AAAA BBBB  CCCC DDDD" prefix="Example fingerprint" >}}
```

| Component | Arguments, types and defaults | Result |
|---|---|---|
| `kbd` | Required nonblank string `text` | Escaped native `kbd`, including literal backtick/Unicode keys. |
| `mark` | Required nonblank string `text`; string `color`: `red`, `green`, `yellow` (default) | Escaped native `mark`, palette-aware background. Status glyph/text remains meaningful without color. |
| `u` | Required nonblank string `text` | Escaped native `u`, accent underline; not a link. |
| `quot` | Required nonblank string `text`; **boolean** `ornament=true` | Centered standout paragraph with optional decorative quotation marks. No heading/TOC entry or invented attribution. `ornament="false"` is invalid; use the boolean. |
| `link` | Required nonblank strings `href`, `text`; optional string `icon` (empty/omitted = generic local link symbol) | One native link card; label and resolved destination remain readable. No automatic description/metadata fetch. |
| `copy` | Required nonblank string `text`; optional string `prefix` (empty/omitted = no label) | Selectable value, shared progressive Copy/Copied/toast/manual fallback; prefix is never copied. |

Inline `u`, `kbd` and `mark` add **no template whitespace** before/after their output.
For example, `{{< u text="aa" >}}bcc` displays `aabcc`; spaces you author remain.

Text arguments are **literal escaped text**, not Markdown, raw HTML, CSS or math.
This matches the audited inline/standout/copy uses. Quotes around numeric text matter:
`text="9"`, not `text=9`. Spaces in copy text are retained exactly; browser manual
textarea copying normalizes CRLF, as in SNIPPETS.md. Do not put secrets in published
shortcode arguments. Copy is not a redaction mechanism.

Unknown options, invalid types/enums/paths and blank required arguments fail with the
shortcode source position. Standard notation merges this trusted template output
**after** the page's Markdown rendering; passing its generated HTML through `%`
notation instead fails under `unsafe=false`. No unsafe renderer setting is installed.

### Link and image resources

Card destinations reuse **A's `links/destination.html`** exact editor-relative `.md`
and native Page/resource resolver, with its warning policy and native query/fragment/
language/permalink behavior. Ordinary public URLs are not fetched or existence-checked.
Local resource links use native resource URLs; unresolved ordinary non-`.md` web paths
retain A's public-URL behavior. Leading-slash public URLs get the native deployment
prefix. No per-article URL map, filesystem body read, relref requirement or link graph.

Only local/public URLs, HTTP(S) and `mailto:` card destinations are accepted. Unsafe
schemes, protocol-relative paths, control characters, spaces in URLs and backslashes
diagnose. Percent-encode URL spaces. Normal Markdown links keep A's existing broader
contract, including `tel:`; this component does not change that render hook.

Icons use exact page resources, assets, then site static paths, or an **explicit
HTTP(S) image URL**. Local extensions: SVG, PNG, JPEG, GIF, WebP, AVIF, ICO. Paths are
literal resource keys: no dot/dot-dot segments, encoding, glob, query/fragment,
backslash or scheme. Missing/unsupported local images diagnose. Remote icons may
request that exact image in the reader's browser; there is no build-time fetch,
page scraper, automatic favicon discovery or metadata service. Prefer approved local
assets. SVG is loaded through `img`, never interpolated as executable inline markup.
Decorative card icons have empty alt; the authored card label supplies the name.

Emoji/sticker shortcodes, timeline and enhanced-image shortcodes are **retired by
user choice**. No blobcat asset/license decision remains necessary. Ordinary Markdown
images, dimensions, captions, inversion classes and native image/resource links remain
unchanged; retirement does not claim a right to redistribute any old image.

### Copy, summaries, assets and overrides

Copy shares the H/C1 button partial and handler; only its label/success/failure/manual
strings are separate, translated in EN/ZH. Keyboard and touch work without hover.
Missing/denied Clipboard API exposes a focused, selected readonly textarea and an
honest failure toast. No-JS hides the button and retains the selectable original text.
No clipboard writes are performed by tests: all API calls are mocked.

These primitives synthesize no headings. Surrounding Markdown headings remain in the
whole-page native TOC. Hugo's native summary behavior applies; use an explicit summary
when a short article preview should exclude controls/resource text. These components
add no library or per-page math assets. The existing B math detection for native body/
summary content remains unchanged. They do not interpret math inside text arguments.

Native site `_shortcodes/<name>.html` overrides win. Card destinations share the A
partial override; a site **Markdown render-link hook** still overrides Markdown links,
not the markup of the independent card shortcode. Image/alert/math hooks are unchanged.
No component registry, arbitrary template-path argument or new params namespace.

## Actual-use Hexo → Hugo conversion coverage

**Working** means only the independent scope above. **Pending** is not an authoring API
or permission to discard a required result during P4 conversion.

| Used row / precise options | Conversion / disposition |
|---|---|
| `folding` (32/5): title, `open:false`, `child:codeblock`; contains headings, code and grid | **Pending composition decision.** Native details/summary is the target. Preserve Warehouse Modeling's actual inner H2/H3 headings/TOC, not merely plain text. |
| `grid` (47/6): default 240px minimum, `c:2`, `c:5`, `w:150px`; `<!-- cell -->` boundaries | **Pending.** Explicit native cells; preserve multiple cards in one cell, quote-contained and numbered/no-caption images. No comment-marker/Hexo interpreter. |
| `box` (3/3): red, optional title, codeblock child | **Pending.** Two actual fenced-code bodies, one named resource link; required snippet composition remains a C2 checkpoint too. B's five alerts are not a blanket replacement. |
| `blockquote` (1/1): author `Bruce Schneier`, source `Applied Cryptography` | **Pending.** Native attributed quote, preserving attribution even though the inspected Stellar implementation does not consume those positional fields. |
| `quot` (6/3): default ornament and `icon:none`, literal pipe in text | **Working:** named `text`; `icon:none` → `ornament=false`. Standout paragraph, not a heading; typographic ornaments instead of unverified icon assets. |
| `image` (7/4): alt/caption, `bg:#f9fafb`, `width:320px`, alternate-original `fancybox:<file>`, `download:true`, `fancybox:true` | **Retired by user choice (D-091):** no dedicated enhanced-image component/viewer/download UI. Use existing Markdown image/caption/size/resource support as needed; no automatic source conversion. |
| `kbd` (30/3): key text/backtick/Unicode | **Working:** `{% kbd Ctrl %}` → `{{< kbd text="Ctrl" >}}`; literal backtick example above. |
| `mark` (36/3): ✓/✗/? with green/red/yellow | **Working:** `{% mark ✓ color:green %}` → `{{< mark text="✓" color="green" >}}`. |
| `u` (120/10): letters, digits, comma-separated selections | **Working:** `{% u 9 %}` → `{{< u text="9" >}}`; keep quoted text exactly. |
| `timeline` (1/1): six authored `<!-- node label -->` groups, containing grids/cards | **Retired by user choice (D-091).** No timeline shortcode implementation or compatibility obligation. |
| `link` (12/4 including wiki wrapper): authored title/icon; adjacent/HTTPS icons and public-key local target | **Working independently:** URL → `href`, label → `text`, `icon` stays explicit. Nested grid/card placement still **Pending**. Local file remains a real native link; no fake Download action or remote metadata. |
| `copy` (1/1): fingerprint text and prefix | **Working:** `{% copy AAAA BBBB prefix:"Key fingerprint" %}` → `{{< copy text="AAAA BBBB" prefix="Key fingerprint" >}}`; exact text excludes prefix. |
| `emoji` (1/1): blobcat party | **Retired by user choice (D-091).** The shortcode/specimen/style were removed; no blobcat asset required. |

`snippet` remains the accepted C1 contract in SNIPPETS.md. AnimCube is site-owned P4.
Diagrams, video, GitHub badge and other D embeds, E references/search and F comments
are outside this partial C2 implementation.

## Composition decision required before the remaining family

Hugo 0.166 pre-renders a nested `%` shortcode's `.Inner`. In B's `.md` wrapper, that
HTML then enters the outer safe Markdown pass, where it is omitted. Dropping Parent
guards is not a fix. Standard HTML children have the same problem if their parent
runs the combined `.Inner` through RenderString. No unsafe HTML or marker-regex escape
hatch has been added.

A small **isolated probe**, not a live theme API, demonstrates a possible native route:

```text
{{% frame %}}
## Outer heading
{{< slot >}}
### Nested heading
Native Markdown, then another standard slot if needed.
{{< /slot >}}
{{% /frame %}}
```

Here the outer `%` frame and nested `<` slots all deliberately emit **native Markdown
block nodes**; the existing safe Markdown pass renders them once. Three levels retain
native headings/TOC and links, and authored raw HTML still fails. Extending B's private
node hook can supply details/grid/event semantics. HTML-producing leaves such as
snippet/card need an explicit, validated native-node bridge; dropping their existing
HTML into this probe still fails. That integration is **not yet implemented or proved**.

**Proposed decision:** keep whole-page TOC and accept this mixed outer-`%`/nested-`<`
authoring convention plus a bounded native-node bridge for known components. It is a
real syntax/implementation choice, not arbitrary plugin timing. The simpler standard
RenderString-container alternative excludes inner headings from the page TOC and
still needs an explicit safe child-output strategy; it is **not** an accepted fallback.
No consequential compromise has been imposed. C2 remains partial until this is settled,
implemented and verified against actual nesting, assets, summaries and interactions.

### What the authoring choice means

The remaining real requirement is simple: a folding/box/grid container must be able
to hold Markdown, code snippets and links without losing content or headings in the
page TOC. The implementation must also keep raw HTML disabled.

The proposed author-facing rule is **`%` for the outermost container, `<` for nested
components**. A grid used on its own would use `%`; that same grid nested in a folding
container would use `<`. Existing self-contained leaf calls such as `snippet` retain
`<`. This is an extra notation rule, not a request to enable unsafe rendering.

The isolated frame/slot test above shows the heading-preserving part works. Actual
folding/grid/box and the safe handling of HTML-producing children still need work.
The proposal remains unapproved; this explanation does not change the live API.

An **attributed blockquote** simply shows a quoted passage plus its author/source,
e.g. a quote credited to Bruce Schneier and *Applied Cryptography*. Ordinary Markdown
can already retain that credit; a dedicated shortcode is not inherently necessary.
Its final presentation/replacement remains under discussion.
