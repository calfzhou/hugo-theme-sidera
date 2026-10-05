---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T22:48:24+08:00
title: "Presets and inheritance"
params:
  ai_label: generated
---

Set native `preset: blog`, `notes` or `docs` on a section, or configure its capabilities
directly. Presets never create browsing roots, change native content type or assign
membership to every article. One distinct preset per section is supported, as a
scalar or one-element array; do not assign it to regular pages or cascade membership.

## Bundled choices

| Preset | Selecting section | Descendants |
|---|---|---|
| blog | Recursive publication list; collection navigation; flat classification; menu and recent updates | Same left components, TOC, update date available; published date first |
| notes | Recursive modification list; collection navigation; hierarchical tags; menu, tag tree and recent publications | Same left components, TOC, update date available; updated date first |
| docs | Immediate-child list; menu, page tree and both recent orders; sibling reading navigation | Children mode for sections, same left components, TOC; updated date first |

All support native authors, taxonomies, shared Markdown and opt-outs. The default
recent count is 10, independent of article pagination. Full details of individual
settings belong in the [parameter reference](../publishing/parameters.md).

## Three targets, not one inherited map

A native preset term's ordinary params style **that public term page**. Its two
default fragments target the selecting section and descendant content separately.
Create `content/preset/field-guide/_index.md` for a custom preset:

```yaml
---
title: Field guide
params:
  left: [menu]
  defaults:
    params:
      list_mode: children
      navigation_mode: sequential
      left: [menu, page-tree]
    cascade:
      params:
        list_mode: children
        left: [menu, page-tree]
        right: [toc]
        show_updated: true
---
A public description of this preset.
```

A section may now select `preset: field-guide`. There is no matching icon name,
translation key or type enum requirement. A site file at a bundled term's path,
such as `content/preset/notes/_index.md`, replaces the **whole definition**; omitted
subkeys do not revive bundled defaults. Supply a defaults map, even if `{}`.

## Understand precedence

For an inheritable custom key, first match wins:

1. Effective native page params, including actual Hugo cascade values.
2. A selecting section's own preset `defaults.params`.
3. Ancestor presets' `defaults.cascade.params`, nearest first.
4. Current-language site params, then minimal theme defaults.

Ordinary ancestor `params` do **not** cascade. To override a preset for a branch,
use local params for the branch itself and `cascade.params` for descendants:

```yaml
params:
  left: [menu, page-tree]
cascade:
  params:
    left: [menu, page-tree]
```

Valid `false`, empty strings/arrays/maps win; null is not a reset API. Arrays and
maps replace at their key boundary, after native Hugo merging. `preset: []` stops
farther preset fallback maps, not effective native cascade, scope or taxonomy
membership. Native fields such as `type` need native cascade, not preset defaults.
Root identity, `scope_root`, parent-local child order, pins, covers and taxonomy
assignments do not belong in preset fallback maps.
