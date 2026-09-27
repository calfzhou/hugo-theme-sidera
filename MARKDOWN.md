# Advanced Markdown — B checkpoint, not full compatibility

Verified on Hugo **0.166.0**, whose `hugo env` reports embedded **KaTeX 0.18.4**.
Basic alerts and Obsidian image dimensions are implemented. Inline/display math has
an inspectable native MathML candidate, **not complete real-source visual parity**.
Image-attribute/container conversion and automatic-caption policy require review.
No Hexo parser, raw-source preprocessing, client math library or new dependency ships.

## Basic alerts

```md
> [!Note]
> A **formatted** paragraph and [source link](../post/index.md).
>
> - Ordinary nested content remains Markdown.
```

NOTE, TIP, IMPORTANT, WARNING and CAUTION are case-insensitive native alert nodes.
They render as labeled `aside` notes, not urgent ARIA live regions. Labels use native
EN/ZH catalogs. The thin colored border and spacing follow the source site's alert
presentation; ordinary quotations keep their accepted style, even inside alerts.
No copied icon assets or dependency was added.

The actual `[!tip] Goal` form was **not** an alert in the reference plugin. Titled,
signed and unknown designators remain blockquotes here. Native Hugo lowercases the
designator when reconstructing these forms; arbitrary original-case/paragraph-layout
parity is not promised. No new collapsible-alert convention is installed.

## Images and safe resource resolution

```md
![Description|320](diagram.svg "A tooltip")
![Description|320x160](diagram.svg)
```

The terminal positive-integer size suffix becomes width/height and is removed from
alt text. Existing responsive CSS caps width and retains the image's natural aspect
ratio; height is an intrinsic hint, not a request to distort it. Width-only syntax is
actually used; two dimensions are additionally tested. Zero/empty/percentage forms
are not this contract and remain literal alt text. Titles remain tooltips; empty alt
stays empty. **Neither title nor alt automatically becomes a caption yet.**

Parsed image destinations reuse the [A destination helper](LINKS.md): native resource
permalinks, queries/fragments, owning bundles, base paths and current source context.
It does not guess a published URL or enable unsafe schemes. Image-only text links
still use A's link hook. A project image hook wins normally; explicit native
`useEmbedded='always'` intentionally bypasses theme hooks and their enhancements.

If the site explicitly enables native standalone-image attributes, id/class and
positive integer width/height are supported. The size suffix wins over attribute
sizes. Unknown attributes and invalid attribute dimensions emit
`sidera-image-attribute` warnings (fatal with `--panicOnWarning`); source context is
included. Native Goldmark strips event handlers first. Attributes cannot replace
src, alt, or introduce inline style/script. No unsafe HTML setting is needed.

**This does not parse `![alt](src){.class}`.** Native image attributes go on the next
line and require `wrapStandAloneImageWithinParagraph=false` plus `attribute.block=true`.
Those settings are **not enabled by the theme or normal showcase** pending authoring
agreement. Inline emphasis/link attributes and `:::invert-when-dark/light` are not
native grammar. No broad regex converter, discarded braces, or fake wrapper support.
Palette inversion CSS and automatic figures remain unimplemented at this checkpoint.

## Native math candidate

The showcase explicitly imports only the native passthrough leaf:

```toml
[markup.goldmark.extensions.passthrough]
_merge = 'deep'
```

The theme's leaf supplies `enable=true`, inline `$…$` and block `$$…$$`. Do not import
all of `markup` or `renderer`; parser security remains unchanged. Sites can instead
supply native settings explicitly or override `enable=false`. No custom params,
preset/cascade parser emulation or per-formula shortcode is introduced.

Goldmark preserves raw TeX before emphasis/escaping. The passthrough hook calls native
`transform.ToMath` with MathML output, block-aware display mode, strict errors and
throw-on-error. Trust stays disabled. Malformed TeX and unknown commands fail the
build with source position; a forbidden trusted command cannot emit an active link.
There is no fabricated fallback formula. With passthrough disabled, the content is
ordinary Markdown (including its normal transformations), not secretly client-rendered.

Inline output has native math baseline behavior. Display output has a centered,
keyboard-scrollable local wrapper and localized accessible label. Native MathML and
TeX annotations remain in the output with JavaScript disabled. No additional CSS,
fonts, script, network request or page-wide math resource flag is needed for this
candidate. No cross-formula mutable macro registry; local `\def\arraystretch` is tested.
Single-backslash escaped currency `\$5` and code spans/fences remain non-math in the
installed runtime. Unescaped paired dollars intentionally mean math; no heuristic
can reliably distinguish prose currency from intended TeX. Unmatched delimiters
remain native Markdown. Other Hugo versions must be retested.

### Material limitation and proposed replacement output

Chromium does not paint all native MathML `menclose`/array-line features: **boxes,
`\xcancel` and array rules used by actual articles lose their visible semantics**.
The showcase deliberately exposes this limit. MathML presence or a successful build
is not full math acceptance. Browser math glyphs also differ from KaTeX's HTML fonts.

Recommended next decision: keep Hugo's **build-time KaTeX**, switch output to
`htmlAndMathml`, and vendor matching **KaTeX 0.18.4 CSS/fonts (MIT)** locally with
provenance/license and conditional loading. No KaTeX JavaScript is necessary. This
new concrete asset dependency is **proposed, not downloaded or approved**. Its
rendered parity, conditional head timing (including summaries), failure behavior and
resource paths must be tested after approval. Do not deploy the candidate as a
complete replacement for real math-heavy articles.

## Inspection and boundary

The committed showcase page is `/handbook/reference/advanced-markdown/`; the existing
Reading List note also contains a notes-to-dated-Journal link inside a callout.
`tests/check_advanced_markdown.py` verifies the native subset and preserves explicit
unconverted/next-line parser controls. Its browser companion checks the live page,
not a second UI framework. Theme docs remain opt-in; this guide is not auto-mounted.
C–F, diagrams, search/comments and real-site migration are not delivered here.
