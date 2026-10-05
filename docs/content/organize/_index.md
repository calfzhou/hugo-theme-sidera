---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T23:21:29+08:00
title: "Organize content"
params:
  ai_label: generated
  children:
    order: [presets, taxonomies, trees]
---

Use Hugo's native content tree. Directories are storage; branch and leaf bundles
express actual documents. Sidera adds browsing policies without a parallel page-ID
or collection registry.

```text
content/
  _index.md                 # optional home introduction
  about.md                  # standalone page
  journal/
    _index.md               # collection root, optionally preset: blog
    first-post/
      index.md              # article leaf bundle
      photo.jpg             # public resource
  handbook/
    _index.md               # optionally preset: docs
    basics/
      _index.md             # body-bearing parent
      install.md            # child document
```

`index.md` is a leaf: adjacent Markdown may be content resources, not independent
child pages. `_index.md` is a branch and can have a body plus children. For an
ordered document tree, author every intended intermediate branch explicitly.
Native title, description, date, lastmod, draft, type, URL and taxonomy assignments
stay at top level; theme presentation belongs under `params`.

## Browsing scope is independent

Top-level sections automatically form browsing roots. A nested section normally
shares its nearest root. Give a nested `_index.md` local `params.scope_root: true`
only when it needs independent search/navigation/lists. Do not cascade this marker.
An outer collection excludes the independent root's articles from its own lists.
A scope boundary does not block actual native cascade inheritance.

Collections may share a preset but have separate names and logos:

```yaml
---
title: Notes on observing the night sky
description: Measurements, reading and experiments.
preset: notes
params:
  name: Sky notes
  logo: images/observatory.svg
---
```

`name` is a concise context label, not a route or ID. `title` stays the full heading
and card/search title. `description` supplies summary copy. Logo/name are local
root fields, not site defaults or descendant metadata. Missing logo means a text-only
card; collection cards show latest owned article activity rather than root edit time.

## Choose the right organizing tool

- [Presets and inheritance](presets.md): optional blog, notes or docs defaults.
- [Taxonomies, authors and series](taxonomies.md): shared identities and contextual views.
- [Ordered document trees](trees.md): body-bearing branches and reading order.

For generic engine concepts see Hugo's [content organization](https://gohugo.io/content-management/organization/)
and [page bundles](https://gohugo.io/content-management/page-bundles/).

## Dates and maintenance

For maintained documentation, keep explicit native timestamps:

```yaml
date: 2026-01-01T09:00:00+08:00
lastmod: 2026-01-03T14:30:00+08:00
```

Keep `date` as the original creation date; update `lastmod` when the page receives
a meaningful content or configuration change. Include a timezone offset. Do not
bump every page on each build, deploy or unrelated edit. These are page-local fields,
not dates to cascade over a whole collection. The docs preset emphasizes updates
and uses these timestamps for its recent-document lists; missing dates are not
invented by the theme. A consuming site still owns its native date-resolution policy.
