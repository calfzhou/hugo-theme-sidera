# Native taxonomies and contextual views

Sidera supplies native tags, categories, authors, series and preset definitions. The site imports
the theme categories with `_merge='shallow'` as described in CONTRACT.md; no duplicate registration.
All native assignments are authored at top level, not under params:

```yaml
title: A useful observation
tags: [science/quantum, tools/python]
categories: [learning]
authors: [editor, researcher]
series: model-workshop
params:
  pinned: true
  show_updated: false
```

A regular page/bundle moves between blog/notes/docs/profileless folders without rewriting those
assignments. Owner/URLs/defaults/relative links follow location naturally. A branch remains native
`_index.md`; series membership remains the same native term but its local sequence follows its
new scope. No per-article owner ID, repeated ancestor tags or parallel assignment source.

## Global identity; scoped projection

| Role | Native global view | Sidera contextual view |
|---|---|---|
| tags/categories | Published assignments across the language Site | Same assignments filtered to nearest browsing root; flat or hierarchical interpretation |
| authors | Shared author identity/profile and work across sections | That author's work within one scope; author identity is not duplicated |
| series | Shared term and global member union | One sequence within a browsing scope; same term across sections is valid |
| preset | Public grouping of explicitly classified sections | Supplies three-target defaults, not automatic article membership; see PRESETS.md |

Examples: `/tags/`, `/tags/science/`, `/journal/tags/`, `/journal/tags/science/`,
`/authors/editor/`, `/journal/authors/editor/`, `/series/model-workshop/`,
`/journal/series/model-workshop/`. Scoped author/series hubs list terms and full-member counts;
scoped tags/categories retain the proven all-content hub plus complete term navigation.
Independent nested roots do not leak into their parent. Generated views never become docs
chapters or recent documents. Actual native Page/Pager URLs supply links and language/baseURL prefixes.

Ordinary article links follow `params.taxonomy_links`, a whole-map selection whose missing entries
use these minimal defaults: tags/categories/series → section, authors/preset → global. Values are
section/global; no available section/destination means a real global fallback. Sidebar selection
`taxonomy_navigation` is separate display policy; hiding it does not remove pages or assignments.
Explicit contextual “all tags in this collection” links retain their stated local meaning.

## Classification hierarchy is optional

Minimal/site default is **flat**, including for blogs. The notes preset opts into hierarchical
tags only. A scope or site can explicitly configure `params.taxonomy_hierarchy=['tags','categories']`,
[] for flat, or either classification separately. Owner policy controls scoped views; Site policy
controls globals, not an arbitrary article's presentation override. The showcase deliberately
configures its named collection fixtures to preserve the established hierarchy examples.

With hierarchy, `science/quantum` supplies ancestor `science`; parent membership is the union of
direct/descendant assignments, deduplicated before counts/sorting/pagination. Flat views use exact
assignments: `science/quantum` is one term. Native parent term `.Pages` can contain descendants and
duplicates in Hugo 0.166, so the shared model does not treat it as exact flat membership.

Inferred unused parent routes may remain empty (D-010). Explicitly authored empty global terms
are valid. Global indexes page over root terms in hierarchy mode, direct terms in flat mode;
scoped content results retain owner list policy. `taxonomy_page_size` is a positive integer;
ordinary owner `page_size` controls scoped result lists. One paginator per mutually exclusive view.

## Authors and series

`authors` supports a scalar or ordered array; array is the recommended multi-author form.
Linked authors preserve native GetTerms order with duplicate identities removed. Author term native
title/description/body describe the person/organization; optional local `params.avatar` uses safe
native resource lookup. `show_authors=false` hides article attribution without changing membership.
`byline` is separate optional free-form credit, not a parsed author ID or implicit assignment.

`series` accepts a scalar or one-element array; more than one distinct series per page diagnoses.
Series membership remains native/global; contextual term results and previous/next links use the
full eligible owner subset independently of the current pager. Cross-section same-term membership
is ordinary valid data, not a reason to prefix keys or reject the content.

Series always use oldest PublishDate first, undated last, then stable Title/Path ties. The former
optional weight mode is removed: omit params.series_order (recommended) or use publication;
weight/other values fail with a migration diagnostic. Native series_weight may remain metadata
but never changes the sequence. Pins, Lastmod, primary_date and main-list order do not reorder it.
Global series term results also sort the complete union by publication date without pins; articles
with an owner still use only that owner's subset for their positions and reading navigation.

Cards show a compact series name and current/total badge. The article's existing series component
now contains a native collapsible ordered outline, current-page highlight and explicitly labeled
Previous/Next in series. Context/positions are shared and cached per term/owner so list pagination
cannot shrink the count. No series means no badge or outline; a singleton has Part 1 of 1 and no
neighbor links. Standalone pages with no owner use the global series sequence. Existing
taxonomy_links policy controls the overview link; member positions stay owner-scoped when owned.

## Metadata, URLs and boundaries

Author term Pages and series term Pages can be authored/overridden normally, for example
`content/authors/editor/_index.md`. Use an explicit native slug/url when a route must not follow a
changed display title. Native term `:slug` defaults also preserve adapter-provided safe Unicode
slugs. Contextual views reuse shared native metadata rather than inventing another per-scope
identity/metadata registry. Native term UI params do not become member defaults; only preset defaults do.

Local literal TOML/YAML source discovery generates the required contextual and inferred routes.
Actual native published Pages determine membership. Both scalar/array authors/series and the
supported raw metadata validation are covered; invalid drafts are not exempt. Native all-states
validation still matters for excluded Page/reference/default checks. Shared-directory filename
translations and root/subpath routes are tested. Broader arbitrary mounts/generated/computed or
cascaded vocabulary/custom taxonomy source trees are not universal discovery support; validate
such source layouts explicitly before production use. This is not a new limitation on native Hugo.

Structural source/route namespaces, malformed paths, Unicode slug conflicts, aliases/static
collisions and private generated metadata remain guarded. Tags/categories use the documented
flat string-array input; nested arrays are not a native hierarchy API. Author/series keys are
flat identities; they do not activate slash hierarchy. All labels are escaped; body/credit content
uses native Markdown/plain text; theme-owned copy stays EN/ZH, with no client-side membership engine.

P2-G changes presentation only: article term badges live in the selected footer by default
(optional duplicate header), cards reuse normalized direct assignments, ordered authors may
also be selected as closing attribution, and the existing scoped series sequence appears
in the article footer. Hiding/reordering a display item never changes native membership.

P2-GR presentation uses Stellar-style compact tag chips for flat global tags and quiet
directory rows for categories/hierarchical indexes. Full native counts, nested links and
pagination remain. Contextual result headers consolidate global/scoped links and show
the full count once in the list metadata; authors/series breadcrumbs use native display
titles rather than the raw assignment key. No membership or sequence policy changes.


Collection browsing refinement: `taxonomy_hubs=index` renders scoped tag/category roots as
vocabulary indexes (shared default for every scope); explicit `list` retains the alternative
all-content list. Term pages, native assignments and full union counts are unchanged. Wide
categories honor the existing hierarchy flag; flat tag chips do not flatten hierarchical tags.
Global indexes share this source-based renderer. `All categories` is the sidebar hub caption.
