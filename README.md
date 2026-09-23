# hugo-theme-sidera
Sidera — A Hugo theme for blogs, notebooks, and connected knowledge. Inspired by Stellar.


## Development status

P2-F implements the approved recognizable shell and native customization baseline:
left-anchored soft-glass identity/navigation, bounded compact main, optional right
region, complete notes/docs trees, native menus and scoped components. See
[SHELL.md](SHELL.md) for the **implemented** settings and extensions. P2-A–W's
organization, appearance, localization and opt-in docs foundations remain intact.
Finished cards and full configurable footers are still G/H work; this is
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
- Site/language → nearest owner → Page presence semantics are documented with
  native cascade caveats; ordered region arrays/maps replace completely. Same
  full shell for standalone pages; compact is an explicit override.
- Shared ordinary reading, local wide-code/table scrolling, native TOC, meaningful
  current/ancestor navigation and one paginator per applicable list. Card/date/
  footer finishing work is explicitly not considered complete in F.

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
native labeled Appearance select is in the left navigation (open “Browse
collections & tags” on mobile), or the compact header when left is absent. Dark and Light are explicit choices; System follows live
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

## Parameter namespace

Existing section/article/shell consumer fields remain under `params.sidera` until
the P2-M consumer migration. New preset terms use `params.defaults` (see PRESETS.md). This pre-release schema replaces the former flat custom
fields outright; there are no compatibility readers. Native Hugo fields and
non-Sidera site params stay native. Byline/update defaults belong on the collection
root (Page → owner → Site resolution), avoiding native cascade table replacement
when a note authors its own tags. See [CONTRACT.md](CONTRACT.md) and [SHELL.md](SHELL.md).

## Shared native taxonomies

[Tags and categories](TAXONOMIES.md) now use the same native top-level fields for
blogs, notes, docs and standalone pages. Global/scoped views, configurable hierarchy,
counts, pagination and article links are implemented. A regular page/bundle can move
between collection folders without rewriting its taxonomy metadata.


## P2-M prerequisite: theme-owned definitions and preset terms

[PRESETS.md](PRESETS.md) documents Sidera-owned taxonomy/term-URL defaults and native
blog/notes/docs preset term Pages. Sites import these categories instead of repeating
the definitions. Native site term overrides and EN/ZH work without an extra registry.
This is a prerequisite, **not the completed parameter/preset consumer migration**;
current collection/params.sidera behavior remains until that next authorized slice.
Actual bundled docs still require explicit opt-in, independent of the docs preset term.
