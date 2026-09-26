# hugo-theme-sidera
Sidera — A Hugo theme for blogs, notebooks, and connected knowledge. Inspired by Stellar.


## Development status

P2-M now implements portable public params, independent scope_root boundaries, optional native
section presets with three-target defaults, capability-based lists/trees, native multi-author
attribution and section-scoped series views/navigation. Sidera supplies its taxonomy definitions
and preset terms; consumers import rather than duplicate them. [Current contract](CONTRACT.md).


P2-F implements the approved recognizable shell and native customization baseline:
left-anchored soft-glass identity/navigation, bounded compact main, optional right
region, complete notes/docs trees, native menus and scoped components. See
[SHELL.md](SHELL.md) for the **implemented** settings and extensions. P2-A–W's
organization, appearance, localization and opt-in docs foundations remain intact.
P2-G/GR covers cards, both rails and functional configurable footers. P2-H now refines
ordinary Markdown inside that accepted frame; final integrated acceptance follows P3. This is
not whole-theme completion, a production migration or an official Stellar port.
Distribution licensing is a separate unresolved gate.

## Visual foundation and provenance

- Native CSS: neutral charcoal surfaces, cyan hierarchy, 18px prose in a 696px
  main region (656px inner prose), local WenKai UI/reading and explicit portable
  Helvetica Neue/PingFang/Arial fallback. Local Source Code Pro/Menlo code.
- Optional 288px left and independent right regions. In-flow right disclosure
  below 1231px, left below 761px. No-JS leaves navigation open; no focus trap.
- Original fixed inline icons and optional local identity/profile images. No
  font/icon framework, downloads, remote backgrounds or integration placeholders.
- Native effective Page.Params → target-specific preset fallback → language/site semantics
  are documented with native cascade caveats; ordered region arrays/maps replace completely. Same
  full shell for standalone pages; compact is an explicit override.
- Shared ordinary reading, local wide-code/table scrolling, native TOC, meaningful
  current/ancestor navigation and one paginator per applicable list. G adds local covers,
  normalized term badges, numbered pagination, scroll-aware TOC and ordered native footers.

Stellar 1.44.0 source is the primary visual/interaction reference. G adapts selected CSS
rules for collection rows, cards, sidebar/TOC and footer surfaces; the full MIT copyright
notice (2021 xaoxuu) is retained in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
Hugo templates and progressive native JavaScript use Sidera's existing model. No EJS,
Stylus pipeline, third-party fonts/icons or service runtime is introduced. The overall
Sidera distribution license remains unresolved; the upstream notice does not grant one.

## Color mode and ordinary reading

The theme default is **auto** (follow the OS). Set native site/language
`params.color_mode` to `dark`, `light` or `auto` for new visitors; a saved valid visitor choice
wins. The public setting and API use **Color mode** consistently. The optional social-menu action `Sidera.cycleColorMode()` cycles dark → light → auto and shows a brief localized notification.
The leftbar's pinned `left_footer` region defaults to `social`, but emits no controls without
a configured menu. Owners can omit the switch or the entire footer. See SHELL.md for local
custom icons, the six-entry bound, native menu configuration and the fixed onclick whitelist.

The head script applies the chosen palette before body paint and stores it locally. Auto follows
OS changes live; manual modes do not. Denied storage leaves a working page-local choice. With
JavaScript unavailable, CSS follows the owner/OS default and hides the inert action while keeping
ordinary links. No remote resources, framework or mandatory appearance select are required.
A restrictive CSP must authorize the existing head script; no full CSP compatibility claim is made.

Ordinary Markdown uses the existing 18px local/system reading stack and bounded article
track, with 1.7 line height, explicit heading hierarchy and compact nested lists/quotes.
Quotation text is muted separately from the rest of the prose; its hover/focus bar uses
a subdued half-opacity accent, following Stellar. Links and emphasis are not faded as a group.
Body links and code tokens adapt the existing palette for contrast, including highlighted
code lines; global shell colors/fonts are unchanged. No new parameter is needed. Text selection follows browser/OS defaults site-wide, as in
Stellar; there is no global or article-only selection-color override.

Native Hugo/Goldmark renders paragraphs, emphasis/strong/strikethrough, ordered/unordered/task
lists, links, rules, tables and footnotes with the site's enabled extensions. Tasks retain
native disabled checkbox semantics; Sidera does not turn them into an interactive service.
Heading IDs, TOC fragments and footnote/backlink roles are not rewritten. The native TOC
range defaults to H1–H6, matching Stellar, through the narrow `markup.tableOfContents` import
in CONTRACT.md. Explicit site range settings still win; leading missing heading levels do not
create extra root indentation. The native heading
render hook adds Stellar-style linked markers for H2 `#`, H3 `=`, H4 `|`, H5 `:`; H1/H6
have no prefix glyph. Compact cyan blocks turn orange on hover or keyboard focus. Accessible
link names/tooltips use native EN/ZH `heading_permalink`; formatted heading text and Hugo's
sanitized attributes remain intact. Long headings wrap beside the marker. These controls
are visible only in `.prose`, not in site/footer Markdown text. Raw HTML remains
subject to Hugo's normal safe default; do not enable `markup.goldmark.renderer.unsafe` just
for ordinary Markdown.

The existing code render hook calls native `transform.HighlightCodeBlock`, overriding only
`noClasses=false` for palette-aware CSS. Hugo itself consumes fence options. Line numbers
(inline/table), line anchors, `lineNoStart` and `hl_lines` remain native; for example:

````md
```python {linenos=table linenostart=8 hl_lines=[3]}
# Lines begin at 8; the third source line is highlighted.
value = 3
print(value)
```
````

Code/line-number tables have one local horizontal scrollport, separate from ordinary data
tables. Line numbers are not selected with code. Ordinary fences have increased vertical padding
and a top-right language label. With JavaScript, hovering/focusing the block reveals a native
Copy button; successful copying shows Copied for three seconds and uses the existing site
toast. Touch layouts expose the language and Copy together without requiring hover.
The corner control stays outside the horizontal scrollport. Clipboard text comes from the
rendered code alone, stripping native line-number spans (not labels or toolbar text); internal
tabs/newlines are preserved. As with native highlighted output, no final source newline is
invented. Denied/unavailable clipboard access reveals and selects a read-only manual-copy field
and shows a localized failure toast, never a false Copied state. No-JS retains language metadata
and selectable/scrollable code without an inert button. Native hl_inline output stays inline
without a toolbar; the built-in highlight shortcode is not replaced by this fence hook.

A pointer click no longer paints a thick/double border. Keyboard focus draws one 2px outline
around the highlighted scrollport, suppressing the redundant inner pre outline. This is focus
feedback, not a code border or syntax-highlighting state. Wide tables/code use Stellar-style 4px transparent tracks with rounded, muted thumbs on
hover or keyboard focus (visible on touch). The thumb strengthens when hovered. A standard
thin-scrollbar fallback covers browsers without WebKit pseudo-elements; forced-colors mode
retains native controls. This also covers the manual-copy textarea, not the document scrollbar
or already-hidden rails/TOC. Keyboard scrolling is spot-checked in Chromium, not certified
across browsers.
Native table column alignment is preserved, with quiet headers and row separators.

Images retain native URLs/alt text and explicit figure sizes, scale down to available width,
and are centered without forced enlargement. Transparent diagrams keep their neutral pale
backing. Markdown image titles are not invented captions. Hugo's native `figure` shortcode
supplies caption/title markup; both stay compact rather than acquiring article-heading gaps.
Footnotes remain in the body, independent of configured article/site footers. There are no
new script assets, plugins, fonts or dependencies in this body pass.


## External article links

Article text links to a different HTTP(S) origin show a small `↗` suffix. It is muted at rest
and follows the link color on hover/focus; a nonbreaking spacer keeps it with the final word.
The arrow is decorative, with a native EN/ZH screen-reader suffix. Internal paths/fragments,
same-origin absolute URLs, mail/tel links and image-only links stay unmarked. Headings with an
authored external text link are included; TOC, menus, metadata and configured footers are not.

This is a small progressive enhancement in the existing navigation script, scoped to the shared
article body. Browser URL parsing compares the resolved destination's scheme/host/port with the
current page origin, correctly handling protocol-relative URLs, case and default ports. A link
to a production host from a localhost preview is external to that preview, not silently remapped.
No href, title, target or rel is changed; no new tab, link interception or destination fetch.
Hugo's built-in/custom link rendering and multilingual resource resolution remain untouched.
Without JavaScript, links retain their native appearance and behavior without the suffix.
There is no observer for dynamically inserted content, new configuration or separate asset.

## Use and develop

The showcase consumes this repository as a Git submodule at `themes/sidera` and
sets `theme = 'sidera'`. Clone the showcase with `--recurse-submodules`, or run
`git submodule update --init --recursive` in an existing checkout.

For theme development, switch this nested checkout to `main` or a feature branch
before committing. Edit here and build the parent showcase: Hugo reads local
changes without a commit or push. Commit the theme first, then the showcase's
submodule pointer. Push the theme commit before pushing a showcase pointer that
references it. Submodule updates may detach HEAD; they do not replace normal
branch management. The `main` branch hint does not change the showcase's pinned
commit during an ordinary submodule update.

Templates live in `layouts/`; `content/_content.gotmpl` generates notebook tag
sections through Hugo's native theme content mount. Site content, collection
settings, date/permalink policy and pagination configuration remain site-owned.
No Go module, symlink, sibling checkout, or site-local implementation is required.
See [CONTRACT.md](CONTRACT.md) for the self-contained supported content/configuration
contract, required site policies versus defaults, prerequisites and build commands.
The [showcase repository](https://github.com/calfzhou/sidera-showcase) contains the
synthetic fixtures and regression harness; it is not a hidden sibling dependency.

The current adapter reads local site `content/` TOML/YAML Markdown metadata.
Fresh successful builds into new destinations remain the verified workflow;
known incremental/publication limitations are not repaired by this packaging.
Drafts must still use valid metadata. Broader content-loader support and final
production compatibility are not claimed.

## English and Chinese UI

P2-C localizes every theme-owned visible/accessibility label through native Hugo
i18n. English and Simplified Chinese catalogs, locale-aware dates/counts, native
site overrides and a bounded filename-translated bilingual content fixture are
verified. There is no automatic body/title/tag translation or fake language switcher.
See [I18N.md](I18N.md) for configuration, the full key inventory, extension guidance,
escaping/fallback semantics and the explicit content-loader boundary.

## Public parameters and native presets

Public custom settings now live under `params`, with meaningful groups retained. Native fields,
taxonomy assignments, menus and cascade remain native. Only private generated navigation metadata
uses `params.sidera`; no legacy public-key reader or closed blog/notes/docs kind gate remains.
Ordinary section params configure that section; use native cascade for descendant metadata.

`preset` selects optional defaults without changing scope. Top-level sections are browsing roots;
a nested `params.scope_root=true` establishes an independent one. Profileless sections have the
same configured capabilities. The theme's blog/notes/docs term Pages support native site overrides
and custom fourth presets without template code changes. See [PRESETS.md](PRESETS.md).

## Shared native taxonomies

[Tags and categories](TAXONOMIES.md) now use the same native top-level fields for
blogs, notes, docs and standalone pages. Global/scoped views, configurable hierarchy,
counts, pagination and article links are implemented. A regular page/bundle can move
between collection folders without rewriting its taxonomy metadata.


## Theme-owned definitions

[PRESETS.md](PRESETS.md) explains the narrow native import permission, theme-supplied definitions
and per-language term Pages. The full consumer migration is implemented, including false/empty
semantics and old-key removal. Actual theme docs still need explicit opt-in (DOCS.md); publishing
the docs preset term does not publish that documentation tree. P2-H ordinary-Markdown implementation is a review checkpoint, not final acceptance.
P3 special features and distribution licensing remain separate.


Article footers now group References, License, Authors and Share into a configurable panel,
while existing terms/series remain outside it. Authors now default to compact linked header names;
footer author cards are an explicit opt-in.
The default content notice is neutral, not an automatic Creative Commons grant. WeChat QR images
are generated locally by Hugo images.QR (Hugo >=0.141.0); no QR service or client library is used.
See SHELL.md for params, native collection cascades, empty/false behavior and share fallbacks.
