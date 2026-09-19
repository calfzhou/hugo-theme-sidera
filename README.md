# hugo-theme-sidera
Sidera — A Hugo theme for blogs, notebooks, and connected knowledge. Inspired by Stellar.


## Development status

P2-A establishes a responsive reading shell over the verified Hugo collection
proof: peer collection navigation, notebook tag hierarchy, shared article/list/tag
surfaces and native pagination. It is a reviewable visual foundation, not a complete
publishing theme or an official Stellar port. P2-B adds dark/light/system appearance
and ordinary reading refinements. Final font distribution remains open; no search
or comment control is supplied for unimplemented features.

## Visual foundation and provenance

- Native CSS in `assets/css/sidera.css`: ink/slate surfaces, mint links, readable
  metadata, 18px prose and a 65ch maximum prose measure. Local WenKai/Iowan/Georgia reading
  stack, Avenir/Trebuchet UI and Source Code Pro/Menlo code; no font downloads.
- One responsive rail, sticky/scrollable on desktop, an in-flow native disclosure
  below 900px. A tiny `navigation.js` sets its initial breakpoint state and handles
  breakpoint changes; without JS the menu stays open. No modal or focus trap.
- Main article, collection cards, plain-text list excerpts, scoped tag ancestors,
  native TOC when headings exist, recent updates and one native paginator. Transparent
  article images have a neutral pale backing, not automatic theme-aware inversion.
- Site owns content, titles, collections, policies and routes. The theme consumes
  existing Page/owner/tag helpers unchanged. Visual tokens are implementation values,
  not a new settings API. Ordinary Hugo site-template/asset overrides remain possible.

Stellar 1.44.0 is a **visual reference**: sidebar/main composition, layered cards,
notebook classification navigation. GoCalf's configuration confirms dark presentation,
18px WenKai text and a glass sidebar. New Sidera CSS, navigation JS and presentation
markup are independently authored over this project's P1 templates; no Stellar code,
icons, images, fonts, EJS or Stylus have been copied. Stellar's MIT copyright notice
(2021 xaoxuu) must accompany any actual reuse in a later slice. This repository does
not yet specify a distribution license; resolve that before external distribution.
No additional build or runtime dependency has been introduced.

## Appearance and ordinary reading

The initial/default appearance is **dark**, irrespective of OS preference. The
native labeled Appearance select is in the collection navigation (open “Browse
collections” on mobile). Dark and Light are explicit choices; System follows live
`prefers-color-scheme` changes. A small script inlined from `assets/js/appearance.js`
runs before the stylesheet/body, then installs the control after DOM readiness.
It remembers a valid choice in the origin's `sidera-appearance` localStorage key.
Denied storage leaves the choice usable for that document, with dark restored on
navigation if no stored value can be read. No JavaScript: readable dark, open native
navigation, and no appearance control. No animation or framework is needed.

The inline head script is deliberate to avoid a separate request before palette
selection. A deployment with a restrictive CSP must authorize its generated hash
(or use an appropriate site override); if scripting is blocked, the readable dark
fallback remains. CSP deployment configuration is not provided or tested here.

Native Hugo/Chroma code highlighting uses a small render hook with palette-aware
classes, preserving ordinary fenced-code options and avoiding fixed inline theme
colors. Comments, keywords, strings/numbers and ordinary text reuse readable tokens;
advanced code-file tooling and special renderers remain outside this slice. Native
figures/captions keep full mobile width; transparent images keep their neutral pale
backing in both palettes. Wide code/tables use native local scrolling, not widgets.
The dependency-free font stacks remain local/system fallbacks; no fonts are bundled.


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
See the showcase README for the tested content/configuration contract and checks.

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
