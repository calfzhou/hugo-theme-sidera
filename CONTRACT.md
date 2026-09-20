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
CSS tokens are implementation values, not a promised settings API. There is no
widget registry, theme-specific global configuration framework or custom menu API.

## Required site policy versus theme defaults

The theme intentionally has **no site configuration file**. The showcase pins these
native policies explicitly; consuming sites should carry them to preserve the
verified contract, rather than assuming the theme installs them:

```toml
baseURL = 'https://example.org/' # replace with the site's URL
locale = 'en-US'
defaultContentLanguage = 'en'
title = 'My site'
timeZone = 'Asia/Shanghai'      # choose intentionally for source timestamps
theme = 'sidera'
disableKinds = ['taxonomy', 'term', 'RSS']

[frontmatter]
date = ['date', 'publishDate', 'pubdate', 'published']
publishDate = ['publishDate', 'pubdate', 'published', 'date']
lastmod = ['lastmod', 'modified', 'publishDate', 'pubdate', 'published', 'date']

[pagination]
path = 'page'
disableAliases = true
```

- `page` is a fixed reserved pagination namespace in the current validators.
  Disabling aliases and global taxonomies/RSS matches the tested output contract;
  notebook tag sections are **not** native taxonomy pages. Feed integration is not
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
- Theme defaults: blogs sort by publication, notebooks by modification, unowned
  sections by title; page size 10; missing pin is false; missing byline/update flag
  does not add either display. Initial appearance is dark; System is opt-in.

## Content and list contract

Use local `content/` Markdown with TOML or YAML front matter. A marked collection
root is a branch section (`_index.md`), not a leaf article (`index.md`):

```toml
+++
title = 'My notebook'
[params]
collection = 'notebook' # blog | notes | notebook | docs | wiki; root only, never cascade
# Optional owner-local settings; do not cascade them:
list_order = 'modification' # publication | modification | title
page_size = 10             # positive integer
[cascade]
[cascade.target]
kind = 'page'
[cascade.params]
byline = 'My team'
show_updated = true
+++
```

Articles derive identity from their nearest marked section, including through
unmarked storage sections. Nested marked collections are isolated in lists;
ordinary Hugo cascade still inherits any outer defaults the inner root does not
override. Article `params.byline` / `params.show_updated` overrides preserve false.
Standalone regular pages need no owner. All use one shared article template.
Leaf bundles keep relative images/downloads and Markdown resources together.

Owner list policy applies to collection roots, storage subsets and tag unions.
Publication uses native PublishDate descending, modification uses Lastmod descending;
ties use Title then logical Path ascending. Title order uses Title/Path. Boolean
article `params.pinned = true` partitions the selected result before pagination;
pins consume slots, spill when necessary, and appear once across the pager chain.
Recent updates is a separate whole-collection top five by Lastmod/Title/Path,
independent of pins and current pager. Counts always cover the complete union.
There are no numeric pin ranks or repeated-pin quotas.

## Notebook tags and routes

Write literal article `params.tags = ['science/quantum', 'science/experiments']`.
No per-article notebook ID, repeated ancestor tags, tag registry or generated-page
authoring is required. Empty/missing tags are allowed; blogs have no scoped tag UI.

- Slash separates hierarchy; lowercasing, trimming and collapsed spaces define
  identity. Ancestors union/deduplicate notes within the nearest notebook only.
- Empty segments, `.`/`..`, backslashes, control characters, non-string elements,
  non-array tags, empty slugs and slug `page` are rejected. Slug collisions include
  implicit ancestors (`a b` vs `a-b`, `C++` vs `C#`).
- Non-ASCII slugs become `u-` + UTF-8 hexadecimal; labels stay readable. No Unicode
  normalization/transliteration is performed. Renaming a tag can change its URL.
- Notebook paths use lowercase ASCII slug segments; roots follow content paths
  plus native language/baseURL prefixes, not custom root URL/slug overrides.
- `<notebook>/tags/` and `<notebook>/page/` are reserved; `page/` is reserved under
  every paginated section. Authored routes, aliases and local static collisions
  fail validation. `tag_view`, `tag_key`, `tag_slug` are generated metadata, not an
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
Fonts are only local/system stacks; no fonts, icons or vendor libraries are bundled.
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
