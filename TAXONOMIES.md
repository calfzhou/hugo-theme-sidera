# Shared native tags and categories

Blogs, notes, docs and standalone pages share **one authoring format**. A page's
location determines its collection and browsing policy, not its taxonomy fields.

```toml
+++
title = 'A useful observation'
date = 2024-03-04T10:00:00Z
tags = ['science/quantum', 'tools/python']
categories = ['learning/experiments']

[params.sidera]
pinned = true
show_updated = false
+++
```

These are Hugo-native assignments, authored at the top level. Hugo exposes them
internally through Page.Params and Page.GetTerms; that does **not** make them
Sidera-defined fields. There is no `sidera.tags`, `sidera.categories`, `blog_tags`
or `blog_categories` reader or duplicate assignment source.

Moving the same regular Markdown page or leaf bundle between marked blog, notes
and docs collections requires **no front-matter rewrite**. Native URLs, inherited
bylines, list ordering and relative links can naturally change with location.
A docs branch remains a native `_index.md`; changing leaf/branch structure is a
native bundle operation, not a different taxonomy schema. Parent-owned docs order
stays on the parent, never repeated on the child.

## Required native site configuration

```toml
disableKinds = ['RSS'] # taxonomy and term output must stay enabled
[taxonomies]
tag = 'tags'
category = 'categories'
[permalinks.term]
tags = '/tags/:slug/'
categories = '/categories/:slug/'
```

The explicit native `:slug` rules honor filesystem-safe slugs supplied for Unicode
terms (including composed/decomposed forms on macOS). Ordinary ASCII routes remain
familiar. The root taxonomy URLs and term patterns can be remapped using native
`permalinks.taxonomy` / `permalinks.term`, retaining `:slug`; links come from actual
Page.RelPermalink, never concatenated browser URLs. Native language/baseURL prefixes
are preserved. For authored term Pages, set native `slug` or `url` when you want a
stable explicit route independent of the native `:slug` fallback to their title.

## One vocabulary, two views

- **Global:** native `/tags/` and `/categories/`, with native term Pages. Results
  cover published regular pages and assigned sections (including docs branches)
  across collections in the current language. Result cards name/link their owner.
- **Collection-scoped:** `<collection>/tags/` and `<collection>/categories/`, using
  the same assignments, filtered to the nearest marked owner. Nested independent
  collections never leak into their parent. Hubs include the owner's eligible
  regular pages (including untagged pages); docs also include descendant documents.
- Generated taxonomy views are navigation, **not docs children or recent documents**.
  The native ordered docs tree/list/paginator remains independent.
- Shared article rendering links both tags and categories, including docs and
  standalone content. Scoped destinations are used where available; otherwise
  native global destinations apply. There is no blog-versus-note conversion step.

The two views do not create two sources of metadata. Native taxonomies remain the
source; the adapter supplies contextual views and otherwise missing ancestor Pages.
This replaces the earlier blog-only/global-versus-custom-notes recommendation.

## Flat or hierarchical interpretation

Sidera's default is hierarchy for both taxonomies. These **presentation policies**
belong under `params.sidera`, on Site/current language or the owning collection:

```toml
[params.sidera]
taxonomy_hierarchy = ['tags', 'categories'] # [] = flat; ['categories'] = categories only
taxonomy_page_size = 10                   # positive integer; global indexes/results
```

Owner settings replace the site's list; empty means flat. This policy belongs to
the site/collection, not each article: moving an article adopts its new collection's
organization without changing the article's tags. Global views use Site policy;
owner views use the owner override. Index pagination is over root terms when
hierarchical, all direct terms when flat. Collection results retain the existing
owner list order/size/pin policy. Global results use PublishDate/Title/Path with
pins once before pagination. Every Page creates at most one native paginator.

With hierarchy, `foo/bar` supplies `foo → bar`; clicking `foo` returns the deduplicated
union beneath it, including direct `foo` assignments. With flat interpretation,
`foo/bar` is one displayed term and `foo` contains only direct `foo` assignments.
The native stored assignment stays `foo/bar` in both cases.

Hugo 0.166's parent term `.Pages` can include descendants **and duplicate Pages**.
Sidera therefore computes exact/ancestor membership from direct Page assignments
and deduplicates before counts, pins and pagination. It does not use a native
parent's recursive count as proof of either flat or hierarchical membership.

Flat mode changes interpretation/navigation, not route cleanup. Inferred ancestor
routes may remain published as harmless empty views when they have no direct
assignment; they are not shown as populated terms. An explicitly authored empty
native term remains visible with zero results and no fake pager.

## Shell controls

```toml
[params.sidera]
left = ['menu', 'taxonomies', 'recent']
right = ['toc']
taxonomy_navigation = ['tags', 'categories'] # display order only, NOT definitions/assignments
```

`taxonomies` is the contextual tree/flat list; `site-taxonomies` links the native
global indexes. Both work in either region. Empty contextual vocabularies disappear.
Native menus can use `pageRef='/tags'` or `/categories`, independent of public URL
remapping. Index/result pages, article links and collection browsing work even when
those sidebar components are omitted. This is not a sidebar-only implementation.

Pre-release component names are now `taxonomies` (formerly `notes-tags`) and
`site-taxonomies` (formerly `blog-taxonomies`); navigation selection is
`taxonomy_navigation` (formerly `blog_taxonomies`). No compatibility aliases.
Individual fixed-component overrides use the same names under
`layouts/_partials/sidera/components/`, with the existing Page/Owner/Region/Settings
context. Existing `tag_icons` supplies fixed decorative term icons, not SVG strings.

## Native data, validation and current boundaries

- Literal arrays of strings in local TOML/YAML Markdown are the proven source
  contract. Both taxonomies and all collection kinds use the same validation,
  including invalid drafts. Case/segment whitespace normalization, malformed paths,
  reserved `page` segments, scoped slug conflicts and native path collisions receive
  contextual errors. Same-named terms across collections are ordinary shared terms.
- Counts/list membership use actual native published Pages, not the raw file inventory.
  The existing local adapter discovers route vocabulary before publication filtering;
  excluded-only vocabulary can therefore leave empty routes. This remains the
  documented D-010 migration tolerance, **not private-vocabulary publication approval**.
- Native branch/leaf resources and translation-by-filename in shared content/ are
  tested. Discovery of implicit ancestors/context routes still reads local `content/`.
  Arbitrary mounted/generated taxonomies, cascaded/computed assignments and other
  front-matter formats are not universal loader support. For a source outside that
  proven inventory, native direct term Pages may exist, but missing implicit ancestors
  diagnose rather than becoming dead links. Do not infer mounted-taxonomy acceptance
  from the separate default-off bundled-docs mount proof.
- Bundled docs remain off by default and their existing body/tree/order/resource
  behavior still works under explicit docs-on. The persistent site handbook provides
  the tagged/docs-branch example. Source inventory never rebuilds the real reference.
- Titles/labels are escaped; bodies use native Markdown. All theme wording uses
  EN/ZH i18n. No JavaScript-only membership, filter backend, dependency or registry.

Tests include the same bundle moved notes → blog → docs with identical source bytes
and intact adjacent assets; parent+child duplicate assignments; flat and independent
owner policies; categories across kinds; explicit empty terms; native URL remapping;
bilingual/subpath routes; published-state filtering and invalid metadata. Browser
checks exercise global/scoped browsing, keyboard/pagers, responsive palettes and
no-JS. They are Chromium/macOS evidence, not complete browser/accessibility certification.
