# hugo-theme-sidera
Sidera — A Hugo theme for blogs, notebooks, and connected knowledge. Inspired by Stellar.


## Development status

P2-A adds the first dark, responsive reading shell to the verified Hugo collection
proof: peer collection navigation, notebook tag hierarchy, shared article/list/tag
surfaces and native pagination. It is a reviewable visual foundation, not a complete
publishing theme or an official Stellar port. Light mode and final font distribution
remain open; there is no nonfunctional mode/search/comment control.

## Visual foundation and provenance

- Native CSS in `assets/css/sidera.css`: ink/slate surfaces, mint links, readable
  metadata, 18px prose and bounded content width. Local WenKai/Iowan/Georgia reading
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
