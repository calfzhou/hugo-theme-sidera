# Contributing to Sidera

Sidera is an independent Hugo theme. Read README.md and the relevant user-manual
page before changing behavior; runtime code and tests are the authority. Keep user
instructions in docs/content, developer guidance here, and execution reports outside
the product. Do not import a consuming site's content, settings or private paths.

## Code entry points

| Concern | Entry points |
|---|---|
| Shared shell/body | layouts/baseof.html; layouts/_partials/article.html; discovery/body.html and footer partials |
| Public settings | layouts/_partials/model/{defaults,settings-valid,preset-defaults}.html; sidera/settings.html; data/sidera/presets.toml |
| Source/discovery model | content/_content.gotmpl; layouts/_partials/model/; collection-owner.html; taxonomies/, docs/, archives/ |
| Markdown and links | layouts/_markup/; layouts/_partials/links/, images/, code-block.html |
| Shortcodes and composition | layouts/_shortcodes/; layouts/_partials/components/; component private-node branches in render hooks |
| Search and references | layouts/_partials/discovery/; assets/js/search.js and discovery data rules |
| Providers/diagrams/charts | layouts/_partials/comments/, diagrams/, charts/; matching local assets/controllers |
| UI, assets, messages | assets/css/, assets/js/, data/sidera/icons.yaml and icon_sources.yaml; i18n/en.toml and zh-CN.toml |

Check actual filenames/callers before editing. Prefer native helpers and existing
small partial seams over a new registry/framework or duplicated rendering path.

## Public invariants

- Native fields/taxonomy assignments stay top-level; public custom fields use params.
  Presets are optional three-target defaults, not types or scope gates. scope_root
  controls browsing independently. Effective native cascade wins; false/empty values
  are meaningful; ordinary ancestor params are not implicit cascades.
- Native Pages determine publication/membership. Source discovery must honor native
  mounted-filesystem exclusions before inspecting metadata. Drafts still validate.
  Contextual route inventory is bounded; do not broaden supported inputs in prose
  without fixtures. Generated internals are not public config.
- Follow source-relative exact-file links and native resource/permalink/language
  identity. Never guess a missing basename/translation or fetch arbitrary resources.
- Containers use outer-%/nested-< notation. Preserve leaf/private-node bridges in
  shortcode, link and blockquote overrides. Render only validated template output
  as trusted HTML; never resource bytes, author HTML or user text.
- Native site lookup overrides theme partials/assets/data. Fixed components receive
  Page/Owner/Region/Settings plus Config/Widget/Instance/IDScope/IDSuffix. Repeated
  instances must not mutate shared settings or produce duplicate IDs.
- docs/content is opt-in, prefix-independent, at most three authored levels including
  its root. Every manual node carries params.ai_label: generated. English body is
  authored once; filenames remain translation-ready. Do not mount root agent files.
  Keep explicit timezone-bearing date/lastmod on every manual node: preserve the
  original creation date, update lastmod for meaningful edits only, never from build
  time or bulk unrelated changes. Keep the manual on the normal docs preset leftbar
  unless a different manual composition is explicitly requested.

## Safety, accessibility and localization

Keep Goldmark unsafe off by default. Do not trade escaping, scheme/path checks,
source limits, SVG geometry validation, renderer sandbox/CSP or message-origin checks
for a successful demo. Code inclusion never executes source; selected lines are not
redaction. Search scopes/hiding controls are not privacy. All-states builds are private.

Theme-owned labels, tooltips, accessible names and JS states use native EN/ZH catalogs.
Translate complete messages with correct plural inputs. Pass escaped text/JSON to JS;
use textContent, not user-string HTML. Preserve keyboard/focus, reduced-motion,
no-JS/failure paths and icons-off visible action text. Site body/menu labels are not
translated automatically. Never post a test comment/reaction or mutate provider setup.

## Local workflow and tests

Use Hugo 0.166.0 extended (check hugo version / hugo env). Normal builds require no
Node/Python installer. Python tests use the standard library; each takes a fresh,
nonexistent absolute output directory outside tracked theme source:

```sh
python3 tests/check_manual.py /absolute/fresh-manual-check
python3 tests/check_icons.py /absolute/fresh-icon-check
python3 tests/check_content_exclusions.py /absolute/fresh-exclusion-check
python3 tests/check_discovery_tokens.py /absolute/fresh-discovery-check
python3 tests/check_discovery_relations.py /absolute/fresh-relations-check
python3 tests/check_component_instances.py /absolute/fresh-instance-check
python3 tests/check_settings_resolution.py /absolute/fresh-settings-check
python3 tests/check_menus.py /absolute/fresh-menu-check
```

Run `tests/check_minify.py /absolute/fresh-output` for shared head/deferred output
changes. Minify completed deferred fragments through `sidera/minify-html.html`,
not by compacting individual templates or stripping final HTML. Pass rendered HTML
only; keep resource keys content-derived and read Content without publishing internal
fragments. Generated frame resources minify before fingerprinting. Cover verbose
custom hooks, inline spaces, pre/textarea contents, distinct pages and frame output.

Random discovery uses `random/resource.html` for one native current-language URL
pool and `assets/js/random.js` for uniform skip-current selection. It is independent
of search and collection scope; keep native publication/list/HTML-render boundaries,
custom region composition, prefix/language URLs and repeated-instance behavior.
Run `tests/check_random.py <fresh-absolute-output>` with uv/Python and
`node tests/check_random.mjs` with the showcase's nvm-selected Node. The showcase's
`tests/check_random_browser.mjs <same-output>` covers real keyboard navigation,
light/dark/mobile, EN/ZH, no-JS/failure and empty/singleton behavior using its owned
browser harness. `tests/check_random_reveal_browser.mjs <same-output>` in the
showcase holds both the controller and URL responses to verify first-paint layout,
loading-time participation in the shared reveal sequence, no replay/layout shift
on readiness, and motion/focus opt-outs. Render random disabled/busy in initial
HTML with a no-script fallback; unhiding it in a deferred script is too late for
first paint. Enable on success and hide on index failure. Do not add a second
animation path or block page reveal on the URL request.

Run the relevant existing check_*.py files for affected images, links, taxonomy,
archive, collection, motion or other behavior. Read a test's entry point before
invoking it; do not assume all tests share a fixture. Strict builds should include
--panicOnWarning --printPathWarnings --printI18nWarnings. Use new output/cache paths,
not unrelated site public directories. Rerun adapter and math checks when changing
Hugo; bundled KaTeX CSS/fonts must match its embedded renderer.

For browser validation use an isolated consumer and a repository-local harness,
explicit free HTTP/debug ports and a fresh owned profile. Verify that test instance,
block unintended external requests, inspect a few relevant light/dark/mobile states,
and stop owned processes. Never attach to an unrelated user browser. Report actual
checks/limits without claiming universal browser, accessibility or legal certification.

## Provenance and changes

Original material uses LICENSE (MIT, Calf); imported material retains its own terms.
Keep public credits linked: [Stellar](https://xaoxuu.com/wiki/stellar/),
[Stellar 1.44.0 source](https://github.com/xaoxuu/hexo-theme-stellar/tree/1.44.0),
and [xaoxuu](https://xaoxuu.com/). Preserve verbatim upstream license text.
Keep THIRD-PARTY-NOTICES.md and assets/licenses/sidera-third-party.txt identical;
LICENSE and assets/licenses/sidera-mit.txt must also match. Preserve conditional
vendor/font notices and byte hashes; no unnecessary dependency/font downloads.

Icons are trusted bounded geometry with currentColor/parent sizing. Select non-brand
UI icons from Solar unless a specific exception is justified and recorded. Select
brand icons from Font Awesome Free `svgs/brands/`, importing only needed names, not
the catalog. Brand keys use exact upstream names without Solar-style variants;
distinct upstream designs remain separate names. Fit/center source viewBoxes in
24 × 24 with uniform geometry transforms, preserving aspect ratio and path data;
never embed brand colors or intrinsic SVG size. No new renderer or runtime loader.
Solar entries retain pinned source/name/style/author/CC BY records; Font Awesome
brand entries retain name/repository/revision/path/author/CC BY, source viewBox,
original attribution and source/normalized hashes in icon_sources.yaml. Keep the
upstream license and trademark restrictions in both notice mirrors. Reference
checkouts are optional/read-only, never test/build dependencies. Run check_icons.py
for geometry/provenance, named rendering, overrides and icons-off regressions.
Original Sidera derivatives use explicit original-design records, not fabricated
Solar paths. Fixed-color
Parallax circle/square/favicon bytes are independent and must remain unchanged.

Ongoing theme development uses `main`; ordinary refinements do not require a
long-lived feature branch. Check branch/status and preserve unrelated edits. Keep coherent commits with
Co-Authored-By: Eureka when Eureka contributes. Ask before deleting files; publication,
release and consumer dependency updates need their own authorization. Update manual,
validation and focused regression together for any public contract change.


## Content palette

`components/color.html` validates the nine named families for mark/box/folding.
`assets/css/sidera.css` owns their shared `--palette-<family>-<role>` tokens;
components bind all five local roles independently so nested colors cannot leak.
Keep explicit sRGB values and the adjacent final OKLCH role coordinates synchronized.
Native `color-scheme` / `light-dark()` handles light, dark, auto and component print
styles without a new asset pipeline or palette controller. Interface roles alias the families; keep errors/pins/syntax independent and pair
filled controls with their foregrounds. The small Giscus CSS mirror must match
default host roles without importing the entire stylesheet into its data URL.
Forward supported new control tokens through both JSX bridge allowlists. Artwork
and vendor palettes remain separate; do not recolor them as incidental cleanup.

Run `tests/check_palette.py <fresh-absolute-output>` with uv/Python. In the showcase,
`tests/check_palette_browser.mjs <same-output>` verifies nested colors, contrast,
alerts, mode changes, mobile, native focus/disclosure, print without backgrounds,
forced colors, no-JS and site overrides through the owned browser harness. Run
`tests/check_ui_palette_browser.mjs <same-output>` for UI-role mappings, contrast
on shell surfaces, hover, auto/no-JS and fixed-light inversion chrome. The existing
mocked-comments and JSX browser suites verify cross-frame parity and overrides. Existing
showcase content-component, composition and advanced-Markdown suites still apply.

Use `--secondary-text` for readable low-emphasis labels and `--quiet` for decorative
faint details. Form boundaries use `--control-border`, not the panel separator.
Keep one shrinkable `folding-title` label beside the native disclosure toggle;
inline Markdown must never become separate summary flex items. Generic text-link
rules cover authored article-end content but must not override control/card states.
Keep compact and sidebar social controls equivalent, disabled controls inert, and
mobile toolbar clearance present before controller readiness.
Run `tests/check_style_consistency.py <fresh-output>` and the showcase's
`tests/check_style_consistency_browser.mjs <same-output>` for these cross-component
invariants. The existing Markdown/composition, topbar, JSX and mocked-comments
suites cover native behavior and source/iframe boundaries.

`invert-soft` modifies an inversion direction on the same element only; by itself
it neither filters descendants nor opts diagrams out of native palette adaptation.
Keep full inversion as the default, both-direction behavior explicit, and nested
filters compositional. Viewers copy computed filters rather than inferring strength
from class names. Run `tests/check_inversion.py <fresh-output>` and the showcase's
`tests/check_inversion_browser.mjs <same-output>` for CSS modes and modal parity.

## Native release checklist

Release identity is an immutable annotated Git tag; do not add a parallel version
file or package/version automation. Maintain user-facing notes only in
`docs/content/publishing/releases.md`, with native date/lastmod and AI-label rules.
Before releasing: inspect clean main/remote ancestry, verify examples/manual and
relevant tests with the supported Hugo, retain all license mirrors, and build a
consumer from the exact anonymously fetched public commit. Ask for authorization
showing the version, full tested commit and extracted notes. A normal main push is
not release permission. Check both local/remote tags and GitHub Releases for a
collision; stop rather than replace any existing release/tag.

After approval, use ordinary Git and optionally GitHub CLI (or GitHub's release UI):

```sh
version=v1.0.0
commit=$(git rev-parse HEAD) # must equal the approved, tested public commit
notes=$(mktemp)
git show "$commit:docs/content/publishing/releases.md" |
  awk -v heading="## $version" '$0 == heading { found=1; print; next } found && /^## / { exit } found { print }' > "$notes"
test -s "$notes"
git tag -a "$version" "$commit" -F "$notes"
git push origin "refs/tags/$version"
gh release create "$version" --verify-tag --title "Sidera $version" --notes-file "$notes"
```

Verify the remote peeled tag equals the approved commit and the Release is actually
published. Never force-move a tag; correct a released defect in a new version. Keep
consumer updates, source merges and site deployments as separate authorized actions.

## Interactive charts

`charts/figure.html` is the shared fence/shortcode boundary. Keep exact native page
resource lookup, strict JSON, byte/depth/array limits and capability rejection in
both authoring paths. Inline/file configuration must not compete; external data
must not overwrite a dataset source. Use the native leaf bridge for nesting.
The pinned ECharts common bundle deliberately supports line/bar/pie/scatter, not
all ECharts modules. Retain verbatim vendor files/notices and manifest hashes.
Do not enable HTML tooltips, image/URL options, callbacks, same-origin sandbox
permissions, eval or network access to make a chart work. Frames are interactive;
do not substitute diagram-style inert SVG images. Resolved source and JSON download must remain available
without JS and after failure; use data-search-exclude for payload/control subtrees.
Reuse diagram hover/focus/touch toolbar styling; icons-off must retain visible text.

Run `tests/check_charts.py /absolute/fresh-output` here using uv/Python 3.11+.
In the showcase, `tests/check_charts_browser.mjs` consumes that directory through
its owned browser harness (explicit free HTTP/CDP ports, nvm-selected Node). Cover
prefix/locales, Content/Summary versus Plain, folds/grids, interaction/state,
reduced motion, no-JS/failure, safe messages and no external renderer requests.

Adaptive chart spacing is limited to single-grid Cartesian charts without explicit
vertical grid bounds or additional layout components. `chart-layout.js` measures
pinned ECharts component views, not DOM text or guessed row counts. Keep passes
bounded and out of render-event feedback loops. Do not measure animated axis views;
queue margin changes with lazyUpdate and consume them through a nonanimated resize.
Browser resize tests must restore normal motion after reduced-motion checks and
sample continuous width sweeps, not just settled endpoints. Preserve author geometry and source
JSON. Run `node tests/check_chart_layout.cjs` with the showcase's nvm-selected Node
for native renderer geometry; the showcase browser suite also tests resize, palette,
selection and axis/legend separation in actual sandboxed frames.

## Executable JSX islands

`params.jsx = true` is an explicit site/language trust opt-in, not an inherited
page setting. `jsx-live` and `jsx` share `jsx/island.html`; ordinary JSX code fences
and snippet inclusion remain inert. Author modules compile through native js.Build,
never SSR/eval/build-time module execution. Page mode intentionally has full page
privileges; do not describe it as a sandbox. Opaque frame mode keeps allow-scripts
only, fixed bounded height, local classic scripts and restrictive CSP. Parent and
source/origin checks limit the frame protocol to readiness/error and theme tokens.

React/React DOM 19.3.0 and Scheduler 0.28.0 production files are verbatim vendored
npm artifacts; retain manifest hashes, original licenses and both notice mirrors.
Page-mode components externalize the four supported React imports to one versioned
runtime through a generated import map. Emit runtime assets only for actual HTML
islands (including cross-page Content/Summary), not Plain or literal code examples.
Keep native page resources/importContext and dependency rebuild behavior. Local
imports use exact bundle-root keys, including from nested modules; do not guess a
helper basename or silently use a different directory on collision. Keep the bundle
module digest (including the `sidera/ui` layout shim) in the compilation key:
virtual importContext/shim dependencies otherwise remain stale across Hugo server
rebuilds. `sidera/ui` exports only Stack/Row, bundles through native js.Build, and
uses the existing CSS classes; preserve native props/refs and do not grow a second
control system or inject global React instances. CSS is
an explicit local resource option: Hugo 0.166.0 js.Build can return a CSS output
as the JS resource when importing CSS; a JS loader for .css makes ordinary CSS
imports fail compilation rather than silently emitting a broken script.

Keep ordinary control, layout, help/error and result styling in `assets/css/jsx.css`,
scoped to JSX roots with overridable defaults. Specialized component geometry and
presentation belong to the consuming site. Shared page/frame styling tests must
cover no-custom-CSS forms, explicit scoped overrides, ordinary prose isolation and
the validated theme-token channel; do not widen frame permissions for styling.

Run `tests/check_jsx.py <fresh-absolute-output>` with uv/Python. In the showcase,
build the real site into `<run>/public` and run `tests/check_jsx_browser.mjs <run>`
with the documented owned harness and free ports. `tests/check_jsx_preview.py
<fresh-absolute-output>` validates native watch rebuilds with an owned Hugo server. Cover native imports, repeats,
folds, Unicode, page API, Stack/Row parity/props/gaps, plain/card and title/caption placement,
light/dark/mobile, frame isolation, no-JS and failures.

## Inline controls and tabs

Run `tests/check_shortcodes.py <fresh-absolute-output>` and the showcase peer
`tests/check_shortcodes_browser.mjs <same-output>` for icons/hashtags/annotations,
text decorations, code-inline, bundle downloads and tabs. The browser check uses
the owned harness and covers EN/ZH, nested/repeated output, no-JS/script failure,
keyboard/touch-sized layouts, print/forced colors and inherited sup/sub colors.
Run existing composition/content-component, palette, icons and search suites when
changing their shared helpers. Keep `components/leaf.html`'s literal fallback label
and hyphenated shortcode keys; no parsing of Markdown or private author HTML.

`content-controls.js` creates ARIA tab controls and IDs per DOM instance, not per
cached source Page. Source panels stay visible without JS. `sidera:reveal` bridges
search to tab disclosure without exposing a global controller. Search may traverse
inactive native tabpanels but must still skip other hidden/private control nodes.
Sup/sub inherit text color, including print. Code-inline encodes generated text-node
whitespace before native minification; never trust author code as HTML or execute it.

## Structured tables

`tables/options.html`, `cell.html`, `section.html` and `model.html` validate bounded
native data and fill an occupancy grid before `render.html` emits any table. Keep
YAML/JSON schema and topology validation separate from HTML/Markdown rendering;
never silently shift a span past an occupied slot. Header/body grids share a width
but rowspans cannot cross their boundary. All body data cells receive explicit
column/row header references, including multirow and rectangular groups.

`tables/instances.html` rebases generated ID/headers/aria-labelledby attributes in trusted rendered
fragments at the shell boundary, before minification. Preserve its paired template
markers through shortcode/native composition; do not elevate plain strings to safe
HTML. This avoids cached Content/Summary duplicate IDs without client JavaScript.
Do not parse Markdown, rewrite author IDs/text or register a second renderer.

Run `tests/check_rich_tables.py <fresh-output>` and the showcase peer
`tests/check_rich_tables_browser.mjs <same-output>`. Cover native YAML/JSON, rejected
schema/spans, headers/row associations, nested code line-number tables, folds/grids/
tabs, repeated Content/Summary, locales/prefixes, no-JS, CSS-only sticky geometry,
opaque overlays, keyboard scrolling, print/forced colors and site style overrides.
Rerun minification, composition, discovery and palette suites after shared changes.

Rich-table presentation inherits normal Markdown th/td rules; do not reintroduce
card frames or independent caption typography. Vertical separators are explicitly
opt-in via rich-table borders="grid" or native table class="table-grid"; defaults
remain horizontal-only. Use logical cell boundaries, not rich-row :first-child:
a carried rowspan can put the first authored cell in a later column. Scope rules
to direct cells so nested tables and Chroma layouts remain independent. Keep the
native figcaption below and outside `.rich-table-scroll`, and name the table via
its rebased caption ID. Only sticky surfaces need opaque backing. The browser
suite compares ordinary/rich cells and standard/rich figure captions in both modes
and checks that captions remain visible and centered during inner scrolling.

## Source-edit links

`model/edit-url.html` validates literal URLs or path/url mapping records;
`sidera/edit-url.html` resolves the longest virtual `.File.Path` directory prefix.
Preserve literal URL compatibility and whole-value settings overrides.
The toc component owns the edit link, between Back to top and Join the discussion.
Match their shared row/icon styles. Edit visibility is independent of headings,
comments, authors and footer settings; an entirely empty TOC component emits no
sidebar. Keep native anchors, repeated-instance overrides and mobile drawer/no-JS
behavior without a duplicate footer action. Do not derive source filenames from
permalinks, expose physical filesystem paths, or fetch contributor APIs. Mapped links
must skip native File.IsContentAdapter sources as well as fileless pages; adapter
files are generators, not the displayed article source.
Mapping records retain path case that Hugo would lose in parameter map keys.
Use the shared toc-top/toc-edit/toc-comments rules and locale/icon behavior, not a
separate button system. Run `tests/check_edit_url.py <fresh-output>` here and the showcase's
`tests/check_edit_url_browser.mjs <same-output>` through its owned browser harness;
rerun the existing article-footer suite after changes to the shared footer.
