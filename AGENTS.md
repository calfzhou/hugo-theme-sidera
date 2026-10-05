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
| Providers/diagrams | layouts/_partials/comments/, diagrams/; matching local assets/controllers |
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
```

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

Icons are trusted bounded geometry with currentColor/parent sizing. Solar entries
retain pinned source/name/style/author/CC BY records; original Sidera derivatives
use explicit original-design records, not fabricated Solar paths. Fixed-color
Parallax circle/square/favicon bytes are independent and must remain unchanged.

Check branch/status and preserve unrelated edits. Keep coherent commits with
Co-Authored-By: Eureka when Eureka contributes. Ask before deleting files; publication,
release and consumer dependency updates need their own authorization. Update manual,
validation and focused regression together for any public contract change.
