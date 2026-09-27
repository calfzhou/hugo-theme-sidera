# Content components

Hugo **0.166.0**. Native Markdown/render hooks, a small set of shortcodes, and the
existing shared copy UI. No Hexo interpreter, extra library, remote preview service
or unsafe HTML setting. C2 is implemented for user review; later P3 slices are separate.

## Authoring and composition

Use **Markdown `%` notation for the outermost container**, and **standard `<` notation
for every nested component**. A container used alone takes `%`; the same container
nested in another takes `<`. Self-contained components (`snippet`, `link`, `copy`,
`quot`, `kbd`, `mark`, `u`) always take `<`, including when used alone.

```text
{{% folding title="Supporting material" %}}
Ordinary Markdown, a [source link](../article/index.md) and $x^2$.

{{< grid columns=2 >}}
{{< cell >}}
![A captioned image|160](image.svg)

{{< link href="../article/index.md#heading" text="Read the article" >}}
{{< /cell >}}
{{< cell class="no-caption" >}}
{{< box color="red" child="codeblock" >}}
{{< snippet src="solution.py" from=2 to=5 >}}
{{< /box >}}
{{< /cell >}}
{{< /grid >}}
{{% /folding %}}
```

Use blank lines around block content. There is no `<!-- cell -->` syntax: each cell
has explicit opening/closing tags. A cell may contain several cards, images, ordinary
Markdown or supported shortcodes. A grid accepts **only cells and whitespace**, and
requires at least one cell. Cells require an immediate grid parent.

`block`, `folding`, `box`, `grid` and `cell` are supported parents. Unknown shortcode
parents fail, rather than sending already-generated HTML through Markdown. Site-owned
future embeds need their own integration; neither AnimCube nor D embeds are supplied.
Four-level real-use compositions are tested; this is not arbitrary plugin nesting.

### Container arguments

All arguments are named. Unknown options/types and unsafe tokens fail with source
position. **Common optional strings:** `class=""`, `id=""`. ASCII class/ID tokens begin
with a letter or underscore, then letters/digits/underscore/hyphen; classes may be
space-separated. No HTML tag, script, style string, event handler or arbitrary SVG.

| Container | Additional arguments | Behavior/defaults |
|---|---|---|
| `folding` | Required nonblank string `title`; boolean `open=false`; string `color="neutral"`; string `child=""` | Native `details`/`summary`. Enter/Space/touch and no-JS disclosure work. No custom accordion JS. |
| `box` | Optional string `title=""`, `color="neutral"`, `child=""` | A named/unnamed presentation box; not a sixth alert type. Use B's native five alert types when that is the intended meaning. |
| `grid` | `columns` or `min_width`, mutually exclusive | Omit both: **240px** minimum with auto-fill. `columns`: integer 1–6, fixed count (including partially occupied rows). `min_width`: integer 64–720 CSS pixels, capped to available width. Numeric values or decimal strings accepted; no arbitrary CSS units. Gap fixed at 16px. |
| `cell` | Common class/id only | One explicit grid cell; no mandatory card or figure wrapper. |
| `block` | Common class/id only | B's general div-like Markdown container, now composable; existing root `%` syntax unchanged. |

`color` allows **neutral, red, yellow, green**. `child` allows **empty or codeblock**:
codeblock adjusts padding/surfaces but does not hide C1's title, language, copy or full
source download. This is the audited presentation subset, not every Stellar option.

Container titles support **inline Markdown** with native hooks, including emphasis,
links and math. They are labels, not TOC headings; block content in a title diagnoses.
Title HTML written by the author still triggers the safe renderer's raw-HTML policy.
Math in a title alone loads B's conditional matched local KaTeX assets. Ordinary pages
without math do not load them. No client math library is added.

### Headings, summaries and rendering safety

Container bodies participate in **one whole-page Markdown pass**, so native headings,
fragments, links, attributes, images, alerts, fences and math retain their context.
Headings can naturally remain in Hugo's TOC; **special fold-heading behavior is not a
requirement** and no automatic disclosure-opening/hidden-heading navigation machinery
is supplied. Ordinary folds are useful without any heading inside them.

Containers emit native block nodes carrying private keys. The blockquote hook changes
only those known nodes into the requested container. HTML-producing children render
through their normal validated templates, then return a private native block/inline
node instead of raw HTML. The hook restores only that already-rendered template output.
It never turns `.Inner`, file contents or author-provided HTML into trusted markup.

Keys include the **full native ancestor/ordinal path**, not only a child's ordinal:
Hugo reuses child ordinals in different parents. Page-scoped Store entries prevent
sibling/language/page collisions and preserve distinct snippet line anchors. These
are transient rendering slots, not a global cache, resource registry or link graph.
Forged/missing/private keys diagnose; a key can never name a template or filesystem
path. Snippet resource boundaries and selected-only payloads remain unchanged.

At native end-of-render validation, an unconsumed generated node fails with a useful
notation/hook/parser diagnostic. Wrong `%` nesting can also trigger native raw-HTML
warnings. Plain text can accidentally survive wrong notation; that is **not supported
syntax**. Do not suppress warnings or enable unsafe HTML to make it appear to work.

Hugo's normal Summary behavior remains. For a concise excerpt excluding controls/code
labels, author an explicit summary. Actual rendered container Content and Summary
embedded through the shared shell retain conditional math resources. Tested page-local
stores do not promise arbitrary third-party layouts/output formats or source inclusion.

**Preview transition:** C2 changes B's `block.md` template to `block.html` to carry the
same named component in both contexts. Restart an already-running `hugo server` once
after updating. Cold builds/server and restart with the same cache are verified. No
cache clearing, legacy template alias, user-server manipulation or watcher fix.

## Self-contained components

```text
{{< kbd text="Ctrl" >}} + {{< kbd text="`" >}}
{{< mark text="✓" color="green" >}}
{{< u text="aa" >}}bcc
{{< quot text="A thought | worth keeping" ornament=false >}}
{{< link href="../article/index.md?from=card#heading" text="Read the article" icon="icon.svg" >}}
{{< copy text="AAAA BBBB  CCCC DDDD" prefix="Example fingerprint" >}}
```

| Component | Arguments/types/defaults | Result |
|---|---|---|
| `kbd` | Required nonblank string `text` | Escaped native keyboard token, including backtick/Unicode. |
| `mark` | Required nonblank string `text`; string `color="yellow"`: red/green/yellow | Escaped native highlighted text. Status glyphs remain meaningful without color. |
| `u` | Required nonblank string `text` | Native underline, not a link. Adds no whitespace: the example displays `aabcc`. |
| `quot` | Required nonblank string `text`; boolean `ornament=true` | Standout paragraph with optional typographic ornaments, no invented heading/attribution. |
| `link` | Required nonblank strings `href`, `text`; optional string `icon=""` | One real link card, authored label/icon, native destination; no metadata fetch. |
| `copy` | Required nonblank string `text`; optional string `prefix=""` | Selectable value and progressive shared Copy/Copied/toast/manual fallback. Prefix is not copied. |

Text arguments are **literal escaped text**, not Markdown/HTML/math. Quote numeric
text (`text="9"`, not `text=9`). Boolean options use `false`, not `"false"`. Inline
u/kbd/mark preserve adjacent and explicitly spaced text in paragraphs, lists and
tables, including inside supported containers. Their use inside another Markdown
link/image label is not a certified nesting context; use an ordinary text label there.
Block link/copy/quot/snippet calls belong on their own lines, not inside a paragraph.

Copy shares H/C1's button/handler and localized EN/ZH feedback. Missing/denied clipboard
selects a readonly manual-copy field and reports failure. No-JS hides the action and
keeps the value selectable. Exact API text excludes labels/line numbers; browser manual
textarea normalizes CRLF. Tests mock all clipboard writes. Selection is not redaction.

### Links and resources

Cards reuse **A's exact source/native Page/resource destination partial**, including
editor-relative `.md`, dated/custom/language URLs, query/fragment and source warnings.
Ordinary public URLs are not fetched/existence-checked. Leading-slash public URLs get
the deployment prefix; native resource/Page URLs are not prefixed twice. Local file
links point to real resources/native URLs, not fabricated download metadata.

Card destinations allow local/public URLs, HTTP(S) and mailto. Unsafe schemes,
protocol-relative URLs, controls, backslashes and URL spaces diagnose. Normal Markdown
links keep A's contract, including tel; this does not change their resolver policy.

Icons use exact page resources, assets, then static, or an explicit HTTP(S) image URL.
Local extensions: SVG, PNG, JPEG, GIF, WebP, AVIF, ICO. Local keys allow no traversal,
encoding, query/fragment, glob, backslash or scheme. Missing local images fail. Remote
icons request only the explicitly authored image in the reader's browser; no build-time
fetch or favicon discovery. Prefer approved local images. SVG stays an `img` resource,
never injected inline. Decorative icon alt is empty; the card label supplies its name.

## Native overrides

Site shortcode and render-hook lookup precedence is unchanged. A shortcode used **inside
a container** must preserve the bridge: render its trusted HTML into `$html`, then call
`components/leaf.html` with `shortcode`, `html`, and `inline` (true only for text-like
inline output), passing the result through `safeHTML` in the shortcode template.
The existing theme wrappers are minimal working examples; renderer partials live in
`layouts/_partials/components/`. H/C1 still share `code-block.html`/`copy-button.html`.

A custom blockquote/alert hook must retain `components/blockquote.html` for private
container/leaf nodes. A custom link hook must retain the `sidera-inline:` branch calling
`components/render-leaf.html`; normal destinations stay site-owned. Cooperating overrides
are tested. `useEmbedded='always'` intentionally bypasses theme hooks and is incompatible
with nested inline leaves; it diagnoses instead of silently dropping them. A's embedded
control tests separately exercise native resolution with ordinary text at that point.
No setting forces embedded hooks or overrides a site's native lookup choice.

## Hexo → Hugo: every used C2 row

| Used row / audited forms | Conversion / disposition |
|---|---|
| folding 32/5: title, open:false, child:codeblock | `{% folding Title open:false %}` → `{{% folding title="Title" open=false %}} … {{% /folding %}}`; nested container uses `<`. |
| grid 47/6: default, c:2/c:5, w:150px | `c:2` → `columns=2`; `w:150px` → `min_width=150`; each `<!-- cell -->` segment → paired `< cell >`. Multiple cards in one cell work. |
| box 3/3: optional title, red, codeblock | Named title/color/child on `box`; keep ordinary fences or use C1 snippet. Native alert syntax stays an alternative only when semantically appropriate. |
| attributed blockquote 1/1 | **No dedicated shortcode by user choice.** Ordinary `>` paragraphs plus `> — Author, *Source*` retain credit. |
| quot 6/3: text/pipe, icon:none | Named literal text; `icon:none` → boolean `ornament=false`. Paragraph, not a heading. |
| image 7/4: background/width/original viewer/download | **Enhanced-image component retired by user choice.** Existing Markdown image/resource/dimension/caption behavior remains; no viewer parity claim or real-source conversion. |
| kbd 30/3: keys/backtick/Unicode | `{% kbd Ctrl %}` → `{{< kbd text="Ctrl" >}}`. |
| mark 36/3: ✓/✗/? and three colors | `{% mark ✓ color:green %}` → `{{< mark text="✓" color="green" >}}`. |
| u 120/10: letters/digits/selections | `{% u 9 %}` → `{{< u text="9" >}}`; adjacent characters stay adjacent. |
| timeline 1/1 | **Retired by user choice.** No timeline interpreter/component. |
| link 12/4 including wrapper: label/icon/local target | URL → href, label → text, icon explicit. Works inside cells/folds/boxes; no remote metadata service. |
| copy 1/1: fingerprint + prefix | Named text/prefix; exact value only copied, no git-command modes. |
| emoji 1/1: blobcat party | **Retired by user choice.** No emoji shortcode or blobcat asset/license requirement. |

[SNIPPETS.md](SNIPPETS.md) is authoritative for C1 scopes/selection/options/full bytes.
AnimCube stays site-owned P4. D embeds, E references/search and F comments are not C2.

## Native MP4 (P3-D video slice)

[VIDEO.md](VIDEO.md) defines `{{< video src="clip.mp4" width=480 >}}`: exact local
resource or authored HTTP(S) MP4, explicit loading, native controls, localized states
and file fallback. It composes with the C2 bridge; no player library, autoplay or
build-time fetch. Other P3-D diagram/badge families remain separate.
