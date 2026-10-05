---
title: "Taxonomies, authors and series"
params:
  ai_label: generated
---

Use native top-level assignments across all content kinds:

```yaml
---
title: Observing a useful pattern
authors: [editor, researcher]
tags: [science/optics, tools]
categories: [learning]
series: field-notes
---
```

The theme's narrow taxonomy imports supply tags, categories, authors, series and
preset. Moving an article to another section does not require another assignment
schema. Its URLs, relative links, owner and fallback settings may change.

## Global identities and local browsing

Native global terms gather published assignments across the current language.
Sidera's contextual views filter those assignments to a browsing root: for example,
`/tags/tools/` versus `/notes/tags/tools/`. Nested independent roots stay separate.
Generated taxonomy/archive pages are navigation, not authored docs chapters.

Tags/categories are flat by default; the notes preset interprets tags hierarchically.
`params.taxonomy_hierarchy: [tags, categories]` opts either vocabulary into hierarchy
at a collection root (or the site for global views). `science/optics` then includes
ancestor `science`, with deduplicated member counts. In flat mode the slash remains
part of one exact term. Do not repeat every ancestor on each article.

Tag/category vocabulary indexes and archives are complete, unpaginated views.
Term article results still paginate. Hide taxonomy navigation without deleting
assignments using `taxonomy_navigation: []`. Term links use `taxonomy_links`:
tags/categories/series prefer section destinations, authors/preset prefer global;
missing scoped destinations fall back to actual globals.

## Describe authors

Create `content/authors/editor/_index.md` with native title, description and body.
Optional local `params.avatar` selects a safe local image. Multiple authors retain
their authored order; `byline` is separate credit text. `show_authors: false` hides
attribution, not membership. Native global author identity is not duplicated for
each collection. Explicit term slug/URL can keep a route stable when changing a name.

## Sequence a series

One distinct native series term per article is supported. The same term can appear
in several collections: each collection has its own sequence; the global term shows
the union. The order is **oldest PublishDate first**, undated last, then Title/Path
ties. Pins, lastmod, main-list order and native `series_weight` do not reorder it.
Omit `series_order` or use `publication`; no weight mode is supported.

Cards show position/total, and the article footer's `series` component gives the
complete collapsible outline. Removing that component hides the outline, not
membership or card badges. Collection Previous/Parent/Next is a separate sequence.

## Keep private inputs out of publication

Use native `ignoreFiles` or mount `files` filtering for editor support files; they
are respected before source discovery. Draft/future/expired content is still an
included source and must have structurally valid metadata. See
[troubleshooting and limits](../publishing/troubleshooting.md) for route/source
boundaries and private validation builds. Search opt-outs and hidden menus are not
access controls. Generic taxonomy setup is documented by
[Hugo](https://gohugo.io/content-management/taxonomies/).
