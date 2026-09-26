# Native section presets

The P2-M resolver is implemented. `preset` is a native taxonomy on sections; blog/notes/docs
are bundled defaults, not types or capability gates. Scope is independent (CONTRACT.md).

## Supplied by Sidera

The theme owns the five native taxonomy definitions and term-URL defaults. Consumers import
only those categories; no duplicated definitions or preset registration:

```toml
[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'
```

Hugo 0.166 requires this site-side permission. Theme `_merge` cannot grant itself permission.
Do not enable root-wide/security/markup merging as a shortcut. Site entries can extend/override
these tables; native source assignment keys and public URL patterns are different concerns.

A small native per-language adapter supplies real preset term Pages from the theme's single
`data/sidera/presets.toml` source. Native EN/ZH catalogs supply their titles. This avoids unknown
language-suffix files appearing as accidental ordinary Pages when a site enables only one
language. No new dependency, raw parser/override guard or mandatory site language declaration.

## Select, override or add

```yaml
# A section's front matter
preset: notes
```

A one-element array is also native and supported. At most one distinct preset per section;
no ordered mixin list, ordinary-page assignment, or membership cascade. Descendants consult
the selected term's defaults but do not acquire native preset membership. The public term Page
therefore groups the sections that explicitly selected it, including non-root subsections.

Site-authored `content/preset/notes/_index.md` overrides the bundled term **wholly**:

```yaml
title: My notes preset
slug: notes
params:
  left: [menu]                  # the public term Page, not its members
  defaults:
    params:                    # selecting section
      list_order: modification
      taxonomy_hierarchy: [tags]
      left: [menu, taxonomies, recent]
    cascade:
      params:                  # descendant content
        left: [menu, taxonomies, recent]
        right: [toc]
        show_updated: true
```

For a fourth preset, author another term Page, for example `content/preset/field-guide/_index.md`,
with a defaults map and assign `preset: field-guide`. No template enum, built-in icon name or
translation key is required. Ordinary title/body/description are native term content. Optional
`params.icon` defaults can select a supported decorative icon; omission gives a neutral fallback.

Configured language-suffixed site term files override that language; there is no hidden cross-
language metadata/default translation. Native same-path priority works against theme adapter
Pages. Missing subkeys in a replacement term file do not revive bundled defaults. `{}` is a valid
intentionally empty defaults map; an unknown auto-created preset term without a defaults map fails.

## Resolution and clearing

Effective native Page.Params wins. Then a selecting section reads its own preset's defaults.params;
descendants read ancestors' defaults.cascade.params nearest first; language/site/minimal defaults
follow. Ordinary ancestor params never become implicit descendant metadata. Native cascade has
already happened and is not reconstructed or undone by the theme. Preset cascade is a restricted
custom-params fallback map, not another native target/array cascade engine.

Valid false/empty values win; arrays/maps replace per key. `preset: []` blocks farther preset
fallback maps only. It does not clear real native cascade, change scope or erase native taxonomy
assignments. `scope_root` controls browsing membership/context only; selecting a preset never
creates a scope. See CONTRACT.md for exact types and field-domain exceptions.

## Bundled baseline

| Preset | Selecting section | Descendants |
|---|---|---|
| blog | Recursive publication list, flat classification, top collection-nav, vocabulary-index hubs, menu/taxonomies/recent | Same left components, TOC right, update date hidden |
| notes | Recursive list, modification order, hierarchical tags, menu/taxonomies/recent | Same left components, TOC right, update date shown |
| docs | Children list, page-tree/taxonomies, recent sections enabled | Children mode for sections, same tree/taxonomy components, TOC, update date shown |

Explicit section/page/native cascade values can change every applicable capability without
selecting a preset. Site defaults sit below supplied preset values; use native cascade or a term/
page override when you intend to override a preset site-wide. An authored sibling order remains
parent-local and cannot be a preset default. Native authors/series/tags/dates/URLs are not synthesized.

Footer arrays/text/menu selectors and terms_in_header are presentation keys available in all
three targets, including custom fourth presets. The bundled presets intentionally do not
redeclare them: native Page/cascade or authored preset maps may override the minimal closing
panel defaults, while Site.Params remains the common fallback. Cover is native effective
Page.Params only (like authored artwork), not permitted in preset defaults.

The docs preset term is configuration/classification content. It does **not** publish the actual
theme documentation sample. That sample still requires explicit mounts described in DOCS.md.

`list_header` is an inheritable presentation boolean (default true) in all three targets;
only recursive section presentation consumes it. It does not change browsing roots, membership
or list policy. A hidden section intro does not generate a TOC.

Region defaults in any of the three preset targets accept component/config objects as well as
plain names. Native effective Page.Params still wins and arrays replace wholly. Each chosen
instance then overlays its own validated options; unused preset instances are validated too.
One `recent` type accepts order=publication/modification per instance. Bundled selections are
unchanged; Fieldbook explicitly demonstrates new notebook entries and both orders on docs.

The blog section target now selects `top=[collection-nav]` and `taxonomy_hubs=index`. Its
regular descendants do not acquire a bar by that default. Generated scoped browsing views use
the owner's resolved presentation. Other presets remain unchanged and can opt into identical
capabilities through native Page/cascade or preset options; no runtime blog-name gate is used.

Preset region arrays can reference site/language named widgets. Define widgets in params.widgets
at site/language level, not in a preset's defaults map. Existing bundled preset selections remain
unchanged; recent-updates/recent-published are available reusable choices backed by recent.

The minimal taxonomy_hubs default is now index for every scope, including notes/docs and
sections without a preset. The blog entry remains explicit; list is still an owner opt-in.

Blog sections/descendants default show_updated=true, making the update date available in the shared
header reveal. Explicit false still opts out. The default article footer omits meta, so this does
not create a second date below the body. Notes/docs also enable show_updated for their section and descendants.


Date priority is separate from ordering: primary_date=published in blog, updated in notes/docs,
for both defaults.params and defaults.cascade.params. A title-ordered docs section or a
publication-ordered notes section still emphasizes updates. Page/cascade overrides work normally.


Reading navigation is capability-based: navigation_mode defaults to list for Blog/Notes and
siblings for Docs. Any collection root can select list, siblings or sequential, independent of
preset and primary_date. The mode is a root policy; preset definitions use defaults.params only,
not defaults.cascade. Independent nested roots resolve their own policy normally.
