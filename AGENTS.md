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
browser harness.

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
