# Supported site contract

Sidera is an independent Hugo-native theme for peer blogs, notes and docs, with
shared article rendering. Stellar is a visual reference, not a configuration or
feature-compatibility API. This guide describes the implemented P2 boundary, not
all Hugo inputs or a production migration guarantee.

## Prerequisites and ownership

Verified with **Hugo 0.166.0+extended+withdeploy** on macOS. This is the tested
version, not a claim that every older version works or that the deploy/extended
features are required. Sidera uses native templates, content adapters, CSS and JS;
no Node, npm, Hexo, Go module, font download or sibling repository is a build input.
The showcase's optional tests use Python 3.9+ stdlib; browser tests additionally
use its `.nvmrc` Node 24.12.0 and installed Chrome (override `CHROME_BIN` if needed).

| Site owns | Theme owns |
| --- | --- |
| Content, collection roots/titles, bylines, publication choices, locale/timezone, date chains, permalinks and final homepage intent | Owner lookup, tag sections/unions/validation, list sorting/pins/pagination, reusable article/list/tag/navigation presentation |
| Native configuration and same-path template/asset/i18n overrides | Native English/Simplified Chinese catalogs, dark-first appearance and progressive enhancement |

The collection overview supplied by `layouts/home.html` demonstrates peers; it
is **not** a decision about a real site's final homepage. Overrides should preserve
native UI translations, one paginator per list, ownership and namespace checks.
The implemented [shell contract](SHELL.md) adds native menu selection, scoped fixed
components, CSS tokens and small native override hooks. No widget registry or
parallel menu engine is introduced.

## Required site policy versus theme defaults

The theme supplies taxonomy definitions and native term URL defaults in its own
configuration; the site enables category-specific native import. Locale/date chains,
page permalinks and pagination remain site-owned. See [PRESETS.md](PRESETS.md) for
this P2-M prerequisite and the not-yet-migrated resolver boundary:

```toml
baseURL = 'https://example.org/' # replace with the site's URL
locale = 'en-US'
defaultContentLanguage = 'en'
title = 'My site'
timeZone = 'Asia/Shanghai'      # choose intentionally for source timestamps
theme = 'sidera'
disableKinds = ['RSS']
[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'

[frontmatter]
date = ['date', 'publishDate', 'pubdate', 'published']
publishDate = ['publishDate', 'pubdate', 'published', 'date']
lastmod = ['lastmod', 'modified', 'publishDate', 'pubdate', 'published', 'date']

[pagination]
path = 'page'
disableAliases = true
```

- `page` is a fixed reserved pagination namespace in the current validators.
  Disabling pagination aliases and RSS matches the tested output contract; native tags/categories are enabled.
  Collection-scoped taxonomy sections are projections over the same native assignments. Feed integration is not
  implemented. These are site policies, not theme defaults or claims that all
  other Hugo settings are invalid.
- Date chains are site-owned, metadata-only: no Git/mtime/build-clock dates.
  Missing publication stays unknown; a modification-only note must not invent a
  publication date. `updated` is **not** included above; mapping that legacy field
  needs an explicit site alias/conversion choice with real fixtures.
- Permalinks are optional site policy. The showcase's Journal-only
  `/journal/:year/:month/:day/:slugorcontentbasename/` is not a theme default.
  Hugo date tokens use `.Date`; that site's convention treats `date` as publication.
  Discuss consequential authoring/URL changes rather than changing the policy silently.
- Locale/translation choices are native Hugo settings; see [I18N.md](I18N.md) for
  Chinese-only UI, bilingual filenames, site overrides and extension/fallback rules.
- Current consumer defaults (preset resolver migration still pending): blogs sort by publication, notebooks by modification, unowned
  sections by title; page size 10; missing pin is false; missing byline/update flag
  does not add either display. Initial appearance is dark; System is opt-in.

## Content and list contract

Use local `content/` Markdown with TOML or YAML front matter. A marked collection
root is a branch section (`_index.md`), not a leaf article (`index.md`):

```toml
+++
title = 'My notebook'
[params.sidera]
byline = 'My team'
show_updated = true
collection = 'notebook' # blog | notes | notebook | docs | wiki; root only, never cascade
# Optional owner-local settings; do not cascade them:
list_order = 'modification' # publication | modification | title
page_size = 10             # positive integer
+++
```

Articles derive identity from their nearest marked section, including through
unmarked storage sections. Nested marked collections are isolated in lists;
article byline/update defaults use Page → nearest marked owner → current-language
Site, preserving explicit empty/false values. Native cascade still follows ancestry,
but a local `sidera` table replaces its cascaded counterpart. Article `params.sidera.byline` / `params.sidera.show_updated` overrides preserve false.
Standalone regular pages need no owner. All use one shared article template.
Leaf bundles keep relative images/downloads and Markdown resources together.

Owner list policy applies to collection roots, storage subsets and tag unions.
Publication uses native PublishDate descending, modification uses Lastmod descending;
ties use Title then logical Path ascending. Title order uses Title/Path. Boolean
article `params.sidera.pinned = true` partitions the selected result before pagination;
pins consume slots, spill when necessary, and appear once across the pager chain.
Recent updates is a configurable region component, default top five by Lastmod/Title/Path,
independent of pins and current pager. Counts always cover the complete union.
There are no numeric pin ranks or repeated-pin quotas.

## Native tags/categories and collection routes

Write literal article `tags = ['science/quantum', 'science/experiments']`.
No per-article notebook ID, repeated ancestor tags, tag registry or generated-page
authoring is required. Empty/missing assignments are allowed in every collection kind. [TAXONOMIES.md](TAXONOMIES.md) defines the shared native authoring, global/scoped views and hierarchy choices.

- Slash separates hierarchy; lowercasing, trimming and collapsed spaces define
  identity. Hierarchy (enabled by default) unions/deduplicates Pages globally or within the nearest collection; flat mode uses direct assignments.
- Empty segments, `.`/`..`, backslashes, control characters, non-string elements,
  non-array tags, empty slugs and slug `page` are rejected. Slug collisions include
  implicit ancestors (`a b` vs `a-b`, `C++` vs `C#`).
- Non-ASCII slugs become `u-` + UTF-8 hexadecimal; labels stay readable. No Unicode
  normalization/transliteration is performed. Renaming a tag can change its URL.
- Notebook paths use lowercase ASCII slug segments; roots follow content paths
  plus native language/baseURL prefixes, not custom root URL/slug overrides.
- `<collection>/tags/`, `<collection>/categories/` and `<collection>/page/` are reserved; `page/` is reserved under
  every paginated section. Authored routes, aliases and local static collisions
  fail validation. `params.sidera.tag_view`, `params.sidera.tag_key`, `params.sidera.tag_slug` are generated metadata, not an
  authoring API. Draft status never exempts invalid structural metadata.

## Verification and known boundaries

From a consuming site with this theme installed and configured:

```sh
mkdir -p .checks
run=$(mktemp -d "$PWD/.checks/build-XXXXXX")
hugo --destination "$run/public" --cacheDir "$run/cache" \
  --panicOnWarning --printPathWarnings --printI18nWarnings
# User-owned convenience preview on an available port; stop with Ctrl-C:
hugo server --bind 127.0.0.1 --port 14420 --disableFastRender
```

Only a **successful fresh build into a new destination** is authoritative. Known
adapter watcher/stale-output limitations are tolerated during migration;
`--disableFastRender` does not repair them. Never publish a failed build.
Unpublished-only tags may expose labels/empty routes even when bodies are excluded:
use public vocabulary in showcase fixtures. Harmless empty routes are tolerated;
private vocabulary and valid build-option/public-list semantics need relevant
P3/P4 checks before real publication, not universal pre-P2 loader certification.

Shared-directory filename translations are tested; separate language contentDirs,
arbitrary mounts, other adapters/formats and cascaded/computed tag discovery are
not established. Do not silently adopt those limits as real-site authoring changes.

English/Chinese light/dark desktop/mobile checks and keyboard/no-JS/storage/System
fallbacks are Chromium/macOS evidence, not full accessibility/browser certification.
Fonts are local/system stacks; no fonts or vendor libraries are bundled. F includes
original geometric inline icons and a small optional original SVG mark.
Restrictive CSP must allow the generated inline appearance script hash or use a
site override. Rich source features (links/backlinks, code-file tools, search,
math/diagrams/embeds, comments/feeds) remain P3, not a promised P2 compatibility layer.
Distribution licensing is unresolved; local development readiness is not permission
to publish/distribute. See [README.md](README.md) for provenance and appearance details.

## Docs extension (P2-W)

[DOCS.md](DOCS.md) defines the proven body-bearing page tree, parent-local ordering,
optional direct-child pagination, compatibility aliases and opt-in theme sample.
It supersedes the earlier arbitrary-mount exclusion only for the two tested optional
docs namespaces. Notes metadata discovery remains local-site-content scoped.
Shared article presentation now lives in `layouts/_partials/article.html`; normal
`layouts/page.html` is a wrapper, and docs sections use the same partial.

## Pre-release namespace consolidation

Existing section/article/shell consumer fields still live under `params.sidera`, including menu-entry
`params.sidera.icon`. Native title/date/lastmod/draft/slug/url/menus/taxonomy fields
stay native. No old flat-field readers or aliases remain. Site-owned unrelated
custom params are allowed; this namespace rule is about fields Sidera defines.
See SHELL.md for migration of article defaults out of the old cascade examples.

The shared native taxonomy follow-up supersedes earlier notes-only assignment and
blog-only taxonomy recommendations. `tags`/`categories` are native fields, not
Sidera params. [TAXONOMIES.md](TAXONOMIES.md) is the current taxonomy contract.

P2-M's new bundled preset metadata is the explicit exception: native `preset`
assignment and term `params.defaults`. See PRESETS.md; consuming those defaults and
migrating the older public fields is still pending.
