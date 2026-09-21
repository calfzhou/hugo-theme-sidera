# Docs/page-tree proof

P2-W, tested on Hugo **0.166.0**. This is a native content-model proof, not the
finished docs visual design. No series, collaborative editing, version history,
search or backlink feature is implied.

## Names and ownership

Public vocabulary is **blog / notes / docs** (博客 / 笔记 / 文档). A notebook is
still an ordinary collection title; wiki is a conceptual synonym for docs.
`params.sidera.collection` accepts `blog`, `notes`, `notebook`, `docs`, `wiki`.
The small normalization boundary keeps **notebook** as the internal notes marker
for compatibility, and normalizes `notes → notebook`, `wiki → docs`. Existing
notebook content, layout names and translation keys remain valid. Collection
names, titles and folders are arbitrary, with multiple/nested independent owners.
Never cascade the collection marker. There is no universal content schema.

## Author a body-bearing tree

```text
content/handbook/
  _index.md
  intro/_index.md
  intro/setup/_index.md
  reference/_index.md
```

Each `_index.md` is an ordinary authored document with a body and URL, represented
by Hugo as a **section Page**, not an empty folder. Use a branch even for today's
childless chapter: adding a child later preserves its identity and URL. A normal
`index.md` is a leaf bundle and cannot acquire independently published children.
Regular `.md`/leaf documents can be final children too, but cannot paginate children.

Put `_index.md` at intermediate directories. Sidera rejects flattened regular
children from unmarked storage directories within docs, rather than pretending
those directories are native nodes. Non-page resources such as SVGs belong to
branch bundles; companion Markdown is **content**, not a downloadable Markdown
resource as it is inside a leaf bundle.

Only the root needs `params.sidera.collection = 'docs'`. Each Page's native `.Pages`,
`.Parent`, `.Ancestors` and nearest owner determine membership. Nested marked
collections are independent: the outer tree/list does not absorb them. They
remain available in the collection navigation. No docs adapter or source tree
loader creates these Pages; the existing adapter remains notes-only.

## Parent-owned ordering and optional child lists

Example root `_index.md` (TOML; equivalent lowercase YAML keys also work):

```toml
+++
title = 'Workshop handbook'
[params.sidera]
collection = 'docs'
[params.sidera.children]
order = ['intro', 'reference']
sort = 'title'
page_size = 2
list = true
+++
The handbook has its own introduction, before its immediate-child list.
```

- `order`: optional array of **immediate-child logical names**, relative to this
  parent's native `.Path`. Exact names only: not titles, URL slugs, filenames,
  language suffixes or descendant paths. A regular `leaf.md` with `slug='custom'`
  is still referenced as `leaf`. Empty `[]` means use fallback for everything.
- `sort`: `title` (default) or `name`, ascending. `name` means logical Path;
  `title` sorts by Title then logical Path. Native weight/date/discovery order
  does not supersede the explicit sequence or settle ties.
- `page_size`: positive integer, default 10.
- `list`: boolean, default true. Explicit false disables only the under-body list,
  not the full tree. Childless documents create no paginator or empty list UI.
- Unknown settings, invalid types, duplicate references, unknown names,
  nonchildren and unsupported flattened paths fail with parent/path diagnostics.

The full tree and paginated list use the same ordering helper. Only eligible
native immediate children of this owner enter either; descendants do not flatten
into a parent list. Exactly one paginator is created on an eligible docs section;
ordinary collection/tag views use their separate, mutually exclusive renderer.
Canonical first page shows full prose and TOC. Later pagers retain title/context,
link back to the full document, and show only that pager's children. Authors do
not have to split or shorten their prose.

**Local versus cascading settings:** order is always read from this native Page's
own TOML/YAML source, never inherited. This narrowly reuses the existing front
matter reader with `.File.Filename`; it does not discover Pages or walk directories.
Hugo's merged Params do not distinguish local from cascaded values, which is why
order cannot safely be read from merged Params alone. Even an accidentally
cascaded order has no effect. Fallback settings use native Params and may cascade:

```toml
[cascade.params.sidera.children]
sort = 'name'
page_size = 3
```

On the tested Hugo, a child's own `params.sidera` table (even with unrelated keys) replaces the cascaded
table; missing keys in that local table take theme defaults, not a deep merge.
Repeat desired fallback values in a local table when overriding it. There is no
parallel theme inheritance engine or separate global ordering registry.

## Publication, language and validation

Native `Site.GetPage` can resolve a draft/future/expired/headless/unlisted child
while native `.Pages` omits it. Such an ordered reference is valid and is skipped
without producing a dead navigation link or making strict builds fail on warnings.
If absent in the current language, the exact logical path is checked in the other
configured native Sites. A known child there is valid but not fabricated here.
A name unknown in **all** configured languages fails as a probable typo.

The default proof covers normal native publication and `build.list='never'` /
`build.render='never'`. Native `build.render='link'` is a deliberate link-only
Page, not evidence that an HTML target is published: do not use it for an ordinary
local docs node. Exotic cascading build modes/custom outputs/other content adapters
and arbitrary content mounts are not certified by this proof.

Draft is not a metadata exemption. Existing invalid-draft tag validation is
unchanged. Referenced excluded docs also validate their own settings/order.
Native published collections do not enumerate **unreferenced** excluded docs;
run an all-states validation build to check those, then a fresh publication build.
This is native Hugo validation, not a new raw metadata walker:

```sh
mkdir -p .checks
run=$(mktemp -d "$PWD/.checks/docs-validate-XXXXXX")
hugo --buildDrafts --buildFuture --buildExpired \
  --destination "$run/validation-only" --cacheDir "$run/cache-validation" \
  --panicOnWarning --printPathWarnings --printI18nWarnings
# Do not publish validation-only output (it intentionally includes drafts).
hugo --destination "$run/public" --cacheDir "$run/cache-public" \
  --panicOnWarning --printPathWarnings --printI18nWarnings
```

Each authored language body is a file, not an i18n-generated translation. Tested:
unsuffixed default-language docs, authored `_index.zh.md` chapters in a configured
`zh` Site (`locale='zh-CN'`), missing translations, language/baseURL prefixes, and
Chinese-only UI around the original English dummy body. UI labels use native
English/Chinese catalogs. No fake language switcher is introduced.

## Optional theme-owned sample: default off

The single source is **`docs/content/` in this theme**, outside automatic theme
`content/`. Merely activating Sidera creates no bundled docs Pages, routes,
collection links or sitemap entries. The normal theme content mount still supplies
the notes adapter.

A consuming site can opt in explicitly, using a noncolliding namespace:

```toml
[[module.mounts]]
source = 'content'
target = 'content'
[[module.mounts]]
source = 'themes/sidera/docs/content'
target = 'content/sidera' # consumer's choice; also tested: content/manuals/theme
```

These are **filesystem mounts**, not Go-module dependencies. Keep the Git submodule
workflow. The first mount preserves site content when overriding that component;
layouts, assets, i18n and the theme's own adapter remain mounted natively.
Omit the optional second entry for off mode, rather than hiding a menu or drafting
the docs. Do not copy theme docs into site content.

Use `{{< relref "./authoring" >}}`, `{{< relref ".." >}}` and similar native logical
relative references in branch bodies. Plain relative image paths work at the
canonical branch URL; bodies are not repeated at `/page/N/`. Both chosen prefixes,
a baseURL subpath and language prefixes preserve links/resources. Plain URL-relative
links do not track arbitrary slug/url changes; use native relref for document links.
This does not implement P3 editor-file-relative links, render hooks or backlinks.

### Overrides and collisions

Choose an unused namespace by default. Hugo merges mounts in precedence order:
with site content first, the **same mounted source filename** in site content
intentionally replaces the bundled file (tested for a chapter, preserving its
children). This is an override, not a merge of two bodies; audit such overlaps and
use mount `files` filters when you want an explicit exclusion. Native templates
cannot see files already masked by mount resolution. Do not rely on a warning for
a same-filename override, and do not overlap unrelated collections accidentally.

Different logical Pages publishing to the same URL fail the required strict
`--printPathWarnings --panicOnWarning` build. Hugo also silently coalesces a
branch and a sibling `.md` of the same logical identity; Sidera checks native
branch source companions for this collision in the tested local Markdown layout.
This is a bounded guard, not a universal virtual-filesystem collision auditor.
Do not combine leaf and branch index files for the same node.

The showcase commits a separate site-owned Workshop handbook, published by default.
Its optional `docs-on.toml` configuration opts in to this small theme-owned sample;
the ordinary showcase configuration leaves it off. They are inspection fixtures, not a complete Sidera
manual or claims of unimplemented features. Tree/sidebar/list/card polish and
customization remain P2-E–I work after model review.

## P2-F shell integration

The ordered tree is now a configurable `docs-tree` region component, with distinct
parent links and native disclosures opening the active branch. See [SHELL.md](SHELL.md).
Child/body/paginator order remains unchanged; no TOC is emitted on later child
pagers without the body. Normal theme activation still does not publish these docs.
