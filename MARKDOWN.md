# Advanced Markdown and math

B implementation on **Hugo 0.166.0**, with embedded **KaTeX 0.18.4**. Native Markdown
and small render hooks supply alerts, figures, image dimensions and math. One general
Markdown container binds classes/IDs to grouped content. No markdown-it runtime,
whole-source preprocessing, client math JavaScript or mandatory CDN.

## Native configuration

The site imports only these theme-owned parser/rendering defaults:

```toml
[markup.goldmark.parser]
_merge = 'deep'
[markup.goldmark.parser.attribute]
_merge = 'shallow'
[markup.goldmark.extensions.passthrough]
_merge = 'deep'
```

The theme sets `parser.wrapStandAloneImageWithinParagraph=false`,
`parser.attribute.block=true`, and passthrough `enable=true` with inline `$…$` /
block `$$…$$`. Explicit site values still win. This is **not** a broad markup/security
import; `renderer.unsafe` remains false. The parser parent needs `deep` to import
its nested attribute defaults on this runtime; a shallow parent did not do so.
Site owners may instead spell out the same native fields. The separate H1–H6 TOC
import remains in CONTRACT.md.

## Attributes and general palette styles

```md
![Diagram|320](diagram.svg "A readable diagram")
{.invert-when-dark #diagram}

A paragraph with its own classes.
{.custom-block #description}
```

Goldmark accepts next-line attributes on standalone images, paragraphs, quotations,
lists, tables and other supported blocks; heading/fence attributes stay on the opening
line. This is **native Hugo syntax, not complete markdown-it-attrs parity**.
Adjacent image attrs, link/emphasis inline attrs and `:::` containers are not recognized.
Move the image attribute list to the next line during conversion; no image shortcode
is required. Inside a quote, retain the `>` prefix. Inside a **loose list**, indent
the attribute line with the image and keep blank lines between items. Hugo drops
image attrs in the tested tight-list form. For a tight single-image list, put
`{.no-caption}` on the next **outdented** line to mark the list instead: the group's
caption is hidden, with image alt retained. This is the compatible primitive for
the actual numbered images inside grid cells; full grid composition remains C.
Do not claim every attribute position is interchangeable. Conversions in the showcase are synthetic; real-site conversion stays P4.

`invert-when-dark` and `invert-when-light` apply `invert(1) hue-rotate(180deg)` **to the
marked element itself**, not just descendant images. Both classes together invert in
both palettes. Auto mode works without JavaScript. Unmarked elements are untouched.
A marked parent filters its entire rendered group (including text/background/captions);
nested marked elements compound normally. Do not mark both unintentionally. Pair an
authored foreground/background appropriately: filtering text on a transparent surface
alone can reduce contrast. These classes are an explicit author tool, not automatic
image analysis or a promise that inversion preserves every color accurately.

The image hook keeps image classes/IDs on the **image**, so a caption is not filtered
with it. A deliberately marked enclosing block filters the whole figure. Native CSS
can use these classes on any element; no image-only selector restricts them.

## One small general block

Replace the used `::: invert-when-dark … :::` wrapper with:

```text
{{% block class="invert-when-dark" id="diagram-group" %}}
Markdown content here.
{{% /block %}}
```

`block` is a general container with optional safe named class/id tokens. In C2,
use `%` when outermost and `<` when nested in folding/box/grid/cell/block. Ordinary
content and headings remain in one native Markdown pass. Supported nested shortcodes
now use the bounded native-node bridge; see [COMPONENTS.md](COMPONENTS.md) for exact
arguments, contexts, hook overrides, safety and diagnostics. No arbitrary raw HTML.

## Default automatic figures and image sizes

```md
![Description|320](diagram.svg "Caption from title")
![Description|320x160](diagram.svg)
```

A **direct standalone** image becomes a figure when it has a nonempty caption:
nonempty title first, otherwise cleaned alt. Alt remains its own alternative text;
terminal dimensions are removed. Titles also retain their normal tooltip attribute.
Caption text is HTML-escaped plain text, not a second arbitrary Markdown/HTML renderer.
No active rich-caption syntax was established by the bounded real-use audit.

- `.no-caption` on the image omits its generated caption; on a native list/block it
  hides descendant captions with CSS, preserving image alt.
- Empty title and alt produce no empty caption/figure.
- Images within ordinary prose get no generated caption.
- Image-only links remain valid image links without an automatic caption. Goldmark
  still wraps them in a paragraph even when the image's `.IsBlock` is true; the link
  hook removes only Sidera's generated figure wrapper, preserving image attributes
  and A's destination/title behavior. No active linked-image use was found; arbitrary
  markdown-it-figure linked/rich-caption parity is not claimed.
- Existing native `figure` shortcodes keep their explicit behavior.

`params.auto_caption` is a boolean, **true by default**, with the existing native
page/cascade → section preset defaults → site/language → minimal-default precedence.
False opts out; no new resolver or scope firewall. It is accepted in preset defaults
and validated in effective/source params, cascades and excluded local drafts. Example:

```yaml
params:
  auto_caption: false
```

Terminal positive `|width` or `|widthxheight` becomes intrinsic dimensions. Existing
responsive CSS caps width and preserves natural aspect ratio instead of stretching.
Actual reference use is width-only; dimensions are additionally tested. Zero/empty/%
markers are not this contract and remain literal alt text.

Parsed image destinations reuse [A's native helper](LINKS.md): exact resources,
page/bundle permalinks, query/fragment/base path and source context. Native image
attributes support class/id and positive integer width/height; suffix sizes win.
Unknown attributes/invalid sizes emit `sidera-image-attribute` warnings, strict under
`--panicOnWarning`. Goldmark strips event handlers first. No attribute can replace
src/alt or grant unsafe URL protocols.

## Native build-time math

```md
English and 中文 around $x_1^2 + y_2^2 = r^2$.

$$
\begin{aligned}
a_1 &= \frac{x^2}{2} \\
b_2 &= \sqrt{3}
\end{aligned}
$$
```

Goldmark passthrough preserves raw TeX before Markdown consumes underscores/braces/
backslashes. Native `transform.ToMath` emits **HTML+MathML**, strict/throw-on-error,
block-aware display mode and trust disabled. HTML paints boxes, cancellation and
array rules that native MathML alone failed to paint in Chromium; MathML plus the
TeX annotation supplies accessible content. Visual HTML is `aria-hidden`.

No runtime Node, math JavaScript, mutation observer, shortcode per formula, unsafe
math trust or remote CDN/font request. Matching **KaTeX 0.18.4** unmodified CSS and 60
font files are local Hugo resources; MIT LICENSE/provenance and per-file hashes are
included. See THIRD-PARTY-NOTICES.md. Browser fonts load only as needed. Do not casually
upgrade CSS separately from Hugo's embedded renderer; recheck `hugo env` together.

A deferred head hook loads the fingerprinted stylesheet after rendering established
math use. Actual rendered math embedded through the shared shell is detected too,
not just the host page's own `.Content`. Plain pages load no KaTeX stylesheet; a build
with passthrough disabled and no math emits no KaTeX resources. Used assets and LICENSE
are published together; a missing bundled asset fails the build. This does not promise
arbitrary third-party layout embedding outside the shared shell: custom layouts own
that integration. Unrelated native scripts remain as before.

Display equations center when short and scroll locally with keyboard focus when wide.
Inline math uses upstream baseline layout. EN/ZH, palettes and 320px/mobile are tested.
No-JS keeps fully styled math. If CSS/font delivery fails after deployment, source TeX
and MathML remain in the document, but visual layout can break; there is no fabricated
fallback or automatic remote retry. KaTeX HTML contains inline styles, so a restrictive
CSP must explicitly support that output; no universal CSP/browser/AT guarantee.

Malformed TeX/unknown commands fail with source context. Local `\def\arraystretch`,
cases/arrays/line breaks and the bounded real formula sample are tested. No mutable
cross-formula macro registry or arbitrary TeX support is claimed. Escaped `\$5` and
code spans/fences remain non-math on Hugo 0.166; unmatched delimiters remain native
Markdown. Unescaped paired dollars intentionally mean math. Set native passthrough
`enable=false` for ordinary Markdown rather than secret client rendering.

## Inspection and overrides

**Restart an existing preview once after C2's block.md → block.html transition.**
The B-era opposite rename/recovery remains historical evidence; C2 needs a single
HTML shortcode template to carry native Markdown in both approved contexts. A cold
server and same-cache restart are verified; no cache clearing or compatibility alias.

The committed showcase is `/handbook/reference/advanced-markdown/`; Reading List also
proves a note-to-dated-Journal link inside an alert. New block links retain queries
and native headings. `tests/check_advanced_markdown.py` and its browser companion
record source/config/security, asset and actual rendering checks.

Project render hooks retain native precedence. Explicit `useEmbedded='always'`
intentionally bypasses theme link/image hooks; it is never forced here. A custom
blockquote hook must preserve the private-node branch documented in COMPONENTS.md.
Theme documentation remains opt-in. C–F, diagram implementations and real migration
remain separate; this B checkpoint is not whole-P3 acceptance.

## Include code files (C1)

Use `{{< snippet src="solution.py" >}}` on its own line for an adjacent bundle resource.
[SNIPPETS.md](SNIPPETS.md) covers inclusive bounds, native options, exact downloads,
shared resources and line endings. Code is escaped data, not a Markdown fence generated
from file contents. Standard snippet calls can now nest in C2 containers; the
container at the outermost level uses Markdown `%` notation.

## Native MP4 (P3-D video slice)

[VIDEO.md](VIDEO.md) defines `{{< video src="clip.mp4" width=480 >}}`: exact local
resource or authored HTTP(S) MP4, explicit loading, native controls, localized states
and file fallback. It composes with the C2 bridge; no player library, autoplay or
build-time fetch. Other P3-D diagram/badge families remain separate.
