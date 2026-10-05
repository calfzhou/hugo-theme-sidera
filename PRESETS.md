# Native section presets

`preset` is a native taxonomy on sections; blog/notes/docs
are bundled defaults, not types or capability gates. Scope is independent (CONTRACT.md).

## Supplied by Sidera

The theme owns the five native taxonomy definitions and term-URL defaults. Consumers import
only the relevant categories (including the separate native H1–H6 TOC default); no
duplicated definitions or preset registration:

```toml
[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'
[markup.tableOfContents]
_merge = 'shallow'
```

Hugo 0.166 requires this site-side permission. Theme `_merge` cannot grant itself permission.
The TOC import is leaf-scoped; do not enable root-wide/security or broad markup merging
as a shortcut. Site entries can extend/override
these tables; native source assignment keys and public URL patterns are different concerns.

A small native per-language adapter supplies real preset term Pages from the theme's single
`data/sidera/presets.toml` source. Native EN/ZH catalogs supply their titles. This avoids unknown
language-suffix files appearing as accidental ordinary Pages when a site enables only one
language. No new dependency, raw parser/override guard or mandatory site language declaration.

## Collection display identity is not preset vocabulary

Use native `title`/`description` and optional local `params.name` / `params.logo` on the collection's
`_index.md`. The short name labels scoped search/navigation; full title remains for
headings/cards. These identify a particular collection, not all collections using a
preset. Do not put `name` or `logo` in preset defaults/cascade or use it as a routing/scope key.
A notes/wiki/blog/custom root follows the same rule, including roots without a preset.
CONTRACT.md gives the fallback, validation and exact display surfaces.

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
| blog | Recursive publication list, flat classification, top collection-nav, vocabulary-index hubs; menu + recent updates | Same left components, TOC right, update date shown |
| notes | Recursive list, modification order, top collection-nav; menu + tag tree (tags only) + recent publications | Same left components, TOC right, update date shown |
| docs | Children list; menu + page tree + recent updates + recent publications; recent sections enabled | Children mode for sections, same left components, TOC, update date shown |

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
One `recent` type accepts order=publication/modification and scope=owner/global per
instance. The bundled defaults above apply to both the selecting section and its
descendants; contextual taxonomy/archive views use the owner policy. Recent order is
independent of the main list order/pinning/pagination.

The blog and notes section targets select `top=[collection-nav]`; blog also explicitly
selects `taxonomy_hubs=index` (the shared minimal default). Regular descendants do not
acquire a bar by these defaults. Generated scoped browsing views use the owner's resolved
presentation. Docs and unclassified scopes can opt in explicitly; native false/empty/custom
top values retain precedence. No runtime collection-name gate is used.

Preset region arrays can reference site/language named widgets. Define widgets in params.widgets
at site/language level, not in a preset's defaults map. Bundled presets use the reusable recent-updates/recent-published definitions backed
by the single recent renderer.

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

## Automatic captions

`auto_caption` is an inheritable boolean with minimal default true. Existing presets
do not override it; custom preset `defaults.params` / `defaults.cascade.params` may
set it, including false. Actual Page.Params/native cascade still wins. See MARKDOWN.md
for direct-standalone image scope and per-image `.no-caption`. No parser configuration
is emulated through presets; native parser imports remain site-owned.


## Giscus comments

`params.comments` is an inheritable boolean, default false, independent of preset.
The canonical article-end slot renders comments before the final `article_end_text`,
after navigation/docs children, never on later pagers or generated/list views.
Only Giscus ships; site/language-owned identity settings and native provider-partial
overrides are documented in [COMMENTS.md](COMMENTS.md), with exact setup, mapping,
privacy, loading, locale/palette and failure boundaries. No production IDs belong in
the theme. This supersedes earlier future-comment-slot statements.

Loading behavior: configured comments load automatically when the section becomes
visible (immediate fallback without IntersectionObserver). The TOC adds a native
**Join the discussion** action beneath Back to top only for an actual comment slot.
No descriptive normal-state copy/manual button/separate GitHub link; concise failure
and no-JS messages remain. Site-wide `comments=true` can enable all eligible pages,
while page/cascade/preset false still opts out. See COMMENTS.md for privacy/lifecycle.

## Configured Markdown

[CONFIG-MARKDOWN.md](CONFIG-MARKDOWN.md) defines the shared build-time interpolation
path for authored text/profile/footer/license/reference/final-text settings, minimal
site/page title values and the native site-partial extension. Field resolution and
per-instance context stay unchanged. It does not interpolate ordinary body Markdown,
shortcode labels, translation strings or every string setting; no full token catalog.


## Story and AI metadata

`type: story` is a native Hugo field, set locally or through native `cascade.type`;
it is not a params/preset default or a content organization model. Shared article
bodies opt into the story typography described in MARKDOWN.md. Local non-story types
opt out without changing scope, presets or URLs.

`ai_label` is an inheritable custom string in all three params targets, default empty.
Only manual/reviewed/polished/generated are supported; an explicit empty string clears
lower fallbacks. Bundled presets do not assume an AI disclosure. Site authors can
set page/cascade/preset/site-language values where factually appropriate. Labels stay
localized header metadata, outside body indexes and authorship/license semantics.

### Global leftbar fallback

Without a higher-priority selection, left is menu plus recent-updates with explicit
`config.scope=global`: current-language regular pages across all collections and
standalone pages. It stays non-scoped even on an unpreset collection. Preset selections
use owner-scoped recents by default. No profile widget is implicitly selected now;
owners may still explicitly select it or replace/disable any region.

The shared recent count defaults to **10**, not a preset/site-specific count. Main page_size
and list_order are independent; notes still list by modification, blogs by publication.
No article metadata, taxonomy assignments, scope roots or required author fields change.

Home and preset collection lists share large cards, with collection-owned logos
on the right and no artwork placeholder when a logo is absent. Preset type/icon definitions are unchanged; no theme brand
catalog, new content kind or global logo default is introduced. See CONTRACT.md.
