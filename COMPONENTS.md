# Content components

Hugo **0.166.0**. Native Markdown/render hooks, a small set of shortcodes, and the
existing shared copy UI. No Hexo interpreter, extra library, remote preview service
or unsafe HTML setting. C2 is implemented for user review; later P3 slices are separate.

## Authoring and composition

Use **Markdown `%` notation for the outermost container**, and **standard `<` notation
for every nested component**. A container used alone takes `%`; the same container
nested in another takes `<`. Self-contained components (`snippet`, `link`, `image`, `copy`,
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

`block`, `folding`, `box`, `grid`, `cell`, `timeline` and `event` are supported parents
(`grid` only accepts cells, `timeline` only accepts events). Unknown shortcode
parents fail, rather than sending already-generated HTML through Markdown. Site-owned
future embeds need their own integration. D supplies video, diagramsnet and badge_github
through this bridge; AnimCube remains site-owned P4.
Four-level original compositions and timeline → event → grid → cell → leaf are tested; this is not arbitrary plugin nesting.

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
{{< link href="../article/index.md?from=card#heading" text="Read the article" icon="notebook" >}}
{{< copy text="AAAA BBBB  CCCC DDDD" prefix="Example fingerprint" >}}
```

| Component | Arguments/types/defaults | Result |
|---|---|---|
| `kbd` | Required nonblank string `text` | Escaped native keyboard token, including backtick/Unicode. |
| `mark` | Required nonblank string `text`; string `color="yellow"`: red/green/yellow | Escaped native highlighted text. Status glyphs remain meaningful without color. |
| `u` | Required nonblank string `text` | Native underline, not a link. Adds no whitespace: the example displays `aabcc`. |
| `quot` | Required nonblank string `text`; boolean `ornament=true` | Standout paragraph with optional typographic ornaments, no invented heading/attribution. |
| `link` | Required nonblank strings `href`, `text`; optional string `icon="link"`; explicit empty hides; optional strings `image=""`, `alt=""` | One real link card, authored label, native destination; optional content image takes visual priority over the named icon. No metadata fetch. |
| `copy` | Required nonblank string `text`; optional string `prefix=""` | Selectable value and progressive shared Copy/Copied/toast/manual fallback. Prefix inherits the surrounding paragraph font family and is not copied; value typography is unchanged. |

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

Icons now select a built-in or site-defined **inline registry key**, consistently
with menu/collection/tag icons. Omission uses link; explicit empty omits the icon.
Resolved params.icons=false suppresses decoration, retaining the card label/URL.
[ICONS.md](ICONS.md) documents native site data/icons.yaml and validated geometry.
Former file/HTTP(S) content-artwork arguments belong in `image`, not the icon registry; no automatic
fetch/path guessing. This changes icon arguments, not card destination resolution
or ordinary image support. Cards use links/resolve.html for href and Page identity;
a trusted resolver override returns that dictionary, not only a URL string.

### Card content images

```text
{{< link href="../article/index.md" text="Read the article" image="artwork.svg" alt="" >}}
{{< link href="https://example.org/" text="Project" image="https://example.org/logo.png" alt="Project artwork" >}}
```

`href` and `image` are independent strings. A nonempty image takes the visual slot
instead of `icon`; omission/empty image retains the existing default link icon.
`params.icons=false` hides named decoration, **not content images**. The optional
literal escaped `alt` defaults to empty (decorative/redundant beside the required
card text); give meaningful alternative text when artwork adds information. `alt`
without an image diagnoses. There is no automatic image-failure icon substitution.

Card images and ordinary prose images have transparent CSS backgrounds by default.
The card surface stays intact. Any background drawn
inside an image file remains part of its artwork; the theme never removes/recolors it.
Link cards do not receive the decorative external-link arrow: their visible URL
already exposes the destination. The localized screen-reader external-link description
is retained. Ordinary external prose links keep their existing arrow/behavior.

Native exact bundle/cross-bundle/global asset resolution is shared with ordinary
images/links; static/public leading-slash paths receive the deployment prefix once.
Local paths require an image suffix (including SVG and ICO); ordinary public paths
are not existence-checked. HTTP(S) image URLs may have dynamic paths; no build-time
request, scraping, download, optimization or rehosting occurs. The reader's browser
loads the authored URL lazily under its normal image/referrer policy. Remote failure
leaves the card text/destination usable. Protocol-relative, mailto/data/javascript,
controls, backslashes and above-content-root paths are rejected. Author SVG markup
is never inlined: SVG resources are isolated by native `img`. Selected artwork and
its rights remain the author's responsibility, separate from UI icon policy.

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
| image 7/4: background/width/original viewer/download | Limited native `image` presentation is now explicitly requested in P4 for opt-in backgrounds. Normal Markdown stays primary; D-145 adds explicit original-image popup/download behavior through `original`, not a full Stellar plugin port. Preserve original targets in that field or ordinary links. |
| kbd 30/3: keys/backtick/Unicode | `{% kbd Ctrl %}` → `{{< kbd text="Ctrl" >}}`. |
| mark 36/3: ✓/✗/? and three colors | `{% mark ✓ color:green %}` → `{{< mark text="✓" color="green" >}}`. |
| u 120/10: letters/digits/selections | `{% u 9 %}` → `{{< u text="9" >}}`; adjacent characters stay adjacent. |
| timeline 1/1 | **Reopened by explicit P4 user request:** native `timeline` with paired `event title` children; preserve former node-comment labels. No sidebar/API widget. |
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

## Diagrams and GitHub badges (D)

[DIAGRAMS.md](DIAGRAMS.md) defines native Mermaid fences, local `diagramsnet` and
`badge_github` block leaves. Outermost containers still use `%`, nested leaves `<`.
The underscore in badge_github is a native shortcode name, not an alternate bridge.
No full editor, hosted diagram transfer, consent button for the approved automatic
Shields images, or retired C2 component is added.

## Configured Markdown (P3-F2)

[CONFIG-MARKDOWN.md](CONFIG-MARKDOWN.md) defines the shared build-time interpolation
path for authored text/profile/footer/license/reference/final-text settings, minimal
site/page title values and the native site-partial extension. Field resolution and
per-instance context stay unchanged. It does not interpolate ordinary body Markdown,
shortcode labels, translation strings or every string setting; no full token catalog.

## In-article timeline (P4)

This is an authored **content component**, not the Stellar sidebar timeline/data-service
widget. It supersedes the earlier retirement of this content tag only. No feed, API,
remote fetching, extra JavaScript or Hexo comment-marker parser is implemented.

```text
{{% timeline %}}
{{< event title="2025 年" >}}
Ordinary Markdown and source links.

{{< grid columns=2 >}}
{{< cell >}}
{{< link href="../project/index.md" text="A project" image="art.svg" >}}
{{< /cell >}}
{{< cell >}}
Another card or Markdown body.
{{< /cell >}}
{{< /grid >}}
{{< /event >}}
{{< event title="2008 年或更早" >}}
An approximate date is valid; labels are not parsed as timestamps.
{{< /event >}}
{{% /timeline %}}
```

- Outermost timeline uses `%`; nested timeline/events and all nested components use
  `<`, exactly like existing C2 containers. A timeline can itself be inside a fold/cell.
- `timeline` accepts common optional `class`/`id` only, and requires one or more direct
  `event` children, with whitespace between. Stray prose/leaves diagnose rather than
  disappearing. `event` requires an immediate timeline parent and a nonblank **string**
  `title`; it also accepts common `class`/`id`. Quote year-only labels (`title="2025"`).
- Labels are escaped literal text, not HTML/Markdown or synthetic headings. No forced
  ISO date, chronological sorting, reverse mode or invented machine timestamp.
  Authors control order and may repeat/approximate dates. Native body headings retain
  their IDs/TOC/search destinations; labels stay readable/indexable body text.
- Semantic ordered list/items preserve sequence with decorative line/markers. Rounded
  content surfaces and marker hover follow Stellar's content timeline; keyboard focus
  within each entry receives the same marker emphasis, with reduced-motion support.
  Existing source/resource/card/math/fold/grid behavior and safe native rendering remain.
- No default heading, English-only control or translation string is introduced. No-JS
  retains all content; nested details remain operable. `icons=false` does not remove
  content/chronology or content images; the line/dots are structural CSS decoration.

Convert Stellar `<!-- node LABEL -->` segments into paired `event title="LABEL"`
blocks in a content commit, not a move-only commit. Preserve every label, paragraph,
card/image reference and attribution. Do not author HTML comments as a hidden parser API.
`python3 tests/check_timeline.py /absolute/fresh-output-directory` tests native positive,
negative, nested resource/source/heading/math and literal-label cases without network.

### Link-card presentation

Resting and interactive cards follow Stellar's plain content-link style: 300px maximum
card width within its container, 12px corners, .75rem inner spacing and 2.75rem
contained artwork. Title is two lines, destination one ellipsized line. Both retain
full DOM text and escaped native title tooltips; no content/reference is truncated
at build time. Font sizes follow prose/story context (body minus 2px / 3px), rather
than fixed small labels. Dark resting cards have no outline/shadow; light resting
cards keep a quiet shadow. Their surface color does not change on hover.

Pointer hover reuses the existing Stellar-derived Sidera spotlight/tilt handler, with
light lift shadow or dark accent glow. Keyboard focus keeps a visible outline and
highlight without tilt; touch/coarse-pointer/reduced-motion disable pointer motion.
No-JS leaves native usable links and CSS hover/focus feedback. This does not change
ordinary Markdown links, safe href resolution, card-image source/bytes or icons policy.

## Optional image background (P4 review)

Ordinary Markdown images now have **transparent CSS backgrounds by default**. This
changes theme paint, not pixels or backgrounds inside PNG/JPEG/SVG files. Native
Markdown remains the usual authoring path, including next-line inversion attributes.
Use this small shared shortcode only when explicit presentation is useful:

```text
{{< image src="diagram.svg" alt="A diagram" width=320 background="#f9fafb" >}}
{{< image src="diagram.svg" alt="A diagram" caption="An explicit caption" class="invert-when-dark" >}}
```

- Required **string** `src` and explicit **string** `alt` (empty for decorative images).
  Src reuses the safe card-image resolver: exact native page/cross-bundle/assets,
  same-site public paths and HTTP(S), with no build-time network fetch or rewriting
  of artwork. Unsafe schemes, protocol-relative paths and above-root traversal reject.
- Optional `loading`: `lazy` (default) or `eager`; thumbnails always use
  `decoding="async"`. Eager is useful for an important opening image; popup originals
  still load only when opened. No source rewriting or custom lazy-loader script.
- Optional `background`: `transparent` or hex `#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`.
  Omission has no forced matte. No arbitrary CSS, `url()`, raw style or SVG author input.
  A background applies to the **image**, not its caption or the whole article.
- Optional positive integer pixel `width`/`height` (decimal strings also accepted),
  emitted as native dimensions. Responsive CSS still preserves natural image ratio;
  this is not crop/stretch processing. Alt is literal, not Obsidian size syntax here.
- Optional literal string `caption`: omitted follows `auto_caption` and alt; explicit
  text overrides automatic behavior, empty hides. Image class `no-caption` also hides.
  Alt/caption are independently escaped, never interpreted as executable HTML.
- Optional `class`/`id` use the existing safe ASCII component token grammar and apply
  to the image. `invert-when-dark`/`invert-when-light` work as for native Markdown images;
  captions do not invert merely because the image does.
- Standalone `<` notation on its own line; nested `<` in the existing outer-`%` C2
  containers (folds/grids/cells/boxes/timeline events) uses the same safe leaf bridge.
- Images without `original` remain plain images. D-145 adds the bounded opt-in viewer
  below; no image editor, gallery, automatic download or remote metadata service. Old
  Stellar `fancybox`/`download` argument aliases are not accepted. Icons-off does not
  hide content images or leave controls blank.

`python3 tests/check_images.py /absolute/fresh-output-directory` checks native
resources/captions/nesting/typed-safe inputs without network or consumer edits.

## Thumbnail and original image (P4 review)

```text
{{< image src="thumbnail.jpg" original="original.jpg" alt="A useful description" width=320 >}}
```

`original` is an optional **string image URL**, independently resolved/validated with
the same native resource/HTTP(S) policy as src. Omission/empty keeps the plain image;
use the same URL for src/original when a separate thumbnail file does not exist.
The original file is published unchanged, never resized/rehosted or fetched at build.

The thumbnail is a real link to the original, with a zoom-in cursor. A supported
JavaScript browser enhances an unmodified primary click/Enter into one reusable native
modal; modified clicks remain normal links. Without JS/dialog support it still opens
the original directly. Merely rendering/hovering the thumbnail does not request the
separate original. If src and original are the same URL, the thumbnail naturally has
already loaded that file; there is no claim that this saves the original transfer.

The popup uses the existing diagram-style surfaces and named icons, with localized
zoom out/fit/zoom in/download/close controls. Fit respects natural size (no forced
upscale), zoom is .25–8× the fit scale, arrows/native touch scrolling and mouse drag
pan the image. Keyboard focus stays inside, Escape/backdrop/Close dismiss, and focus
returns to the thumbnail. A loading/error message keeps Close/original access usable;
late image decoding cannot overwrite a newer view. No inline SVG/HTML injection.

The download control is a **native original-URL anchor** with `download`; it does not
fetch a Blob, proxy, rehost or trigger automatically. Cross-origin servers/browser
policies may ignore download and open the resource instead (in a separate tab with
noopener). No CORS workaround or forced cross-origin download is promised.

Caption/alt are preserved independently. The image's explicit background and effective
inversion classes transfer to the original once, following palette changes, without
inverting caption/controls or altering source bytes. Icons-off supplies visible labels;
no-JS retains native access. Ordinary Markdown images and images without original gain
no click handler or viewer assets. There is no gallery, rotation/crop/editor, auto-retry,
preload of all originals, remote metadata lookup or new dependency.

`python3 tests/check_image_viewer.py /absolute/fresh-output-directory` checks original
URLs, conditional resources, source bytes, locales, icons-off and unsafe inputs. Browser
checks additionally cover lazy requests, modal/zoom/pan/focus, failed/late loads and fallback.
