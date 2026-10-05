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

Inferred unused parent routes may remain empty. Explicitly authored empty global terms
are valid. Global and scoped tag/category indexes show the complete vocabulary without pagination:
all root terms and their children in hierarchy mode, all direct terms in flat mode.
`taxonomy_page_size` still controls global term article results and other taxonomy
directories; ordinary owner `page_size` controls scoped article results. Explicit
all-content list hubs retain their normal list policy. One paginator per paginated view.

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
weight/other values fail validation. Native series_weight may remain metadata
but never changes the sequence. Pins, Lastmod, primary_date and main-list order do not reorder it.
Global series term results also sort the complete union by publication date without pins; articles
with an owner still use only that owner's subset for their positions and reading navigation.

Cards show a compact series name and current/total badge. The article's existing series component
now contains a native collapsible ordered outline and current-page highlight. The separate
Previous/Next in series pair is omitted; adjacent chapters remain available in the outline. Context/positions are shared and cached per term/owner so list pagination
cannot shrink the count. No series means no badge or outline; a singleton has Part 1 of 1 and no
neighbor links. Standalone pages with no owner use the global series sequence. Existing
taxonomy_links policy controls the overview link; member positions stay owner-scoped when owned.

## Metadata, URLs and boundaries

Author term Pages and series term Pages can be authored/overridden normally, for example
`content/authors/editor/_index.md`. Use an explicit native slug/url when a route must not follow a
changed display title. Native term `:slug` defaults also preserve adapter-provided safe Unicode
slugs. Contextual views reuse shared native metadata rather than inventing another per-scope
identity/metadata registry. Native term UI params do not become member defaults; only preset defaults do.

Literal TOML/YAML source discovery generates contextual and inferred routes from
Hugo's **mounted content filesystem**, with Hugo's native source-ignore policy.
Native `ignoreFiles`, content mount `files` inclusions/exclusions and default ignored
editor filenames apply before scope discovery, front-matter inspection or authored
term override detection. Excluded sources cannot create empty taxonomy/collection
routes or shadow an inferred term. Directories without included Markdown do not
become collections merely because support files exist on disk.

Use the site's native Hugo configuration, not a separate Sidera exclusion setting:

```toml
ignoreFiles = ['(^|/)(_templates|_utils)(/|$)', '(^|/)editor-report\.md$']
```

Alternatively, filter the content mount itself:

```toml
[[module.mounts]]
source = 'content'
target = 'content'
files = ['! _templates{,/**}', '! **/_utils{,/**}']
```

Mount globs are path-sensitive: a root path and a nested path are not interchangeable.
Use `{,/**}` to exclude a directory itself and its descendants. Native exclusions are
not secrecy for files already committed to Git, nor authorization to mount private
content as static assets or shared snippets.

**Draft/future/expired is not source exclusion.** Included Markdown still receives
structural metadata validation even when not currently published. Native published
Pages determine memberships and search/graph bodies. Leaf bundle Markdown resources
remain resources; shared-directory filename translations retain their existing
selection rules. No source content or generated code is executed.

The adapter's early filesystem bridge is tested with **Hugo 0.166.0**; it uses the
adapter Site's content filesystem and SourceSpec, not the wrapped rendering Site.
These Go-backed adapter members are version-sensitive, so rerun the native regression
when upgrading Hugo. No config-file parser, duplicated ignore rules, environment
reader or dependency installation is involved. Arbitrary computed/cascaded vocabulary,
custom source trees or multidimensional mounts still require explicit validation;
this does not promise every native Hugo content organization as discovered vocabulary.

Run `python3 tests/check_content_exclusions.py /absolute/fresh-output-directory`
for native ignore/mount/config-overlay/environment, HTML/plain Markdown/resource,
multilingual, symlink, inferred-term and included-invalid-content coverage.

Structural source/route namespaces, malformed paths, Unicode slug conflicts, aliases/static
collisions and private generated metadata remain guarded. Tags/categories use the documented
flat string-array input; nested arrays are not a native hierarchy API. Author/series keys are
flat identities; they do not activate slash hierarchy. All labels are escaped; body/credit content
uses native Markdown/plain text; theme-owned copy stays EN/ZH, with no client-side membership engine.

Article term badges live in the selected footer by default
(optional duplicate header), cards reuse normalized direct assignments, ordered authors may
also be selected as closing attribution, and the existing scoped series sequence appears
in the article footer. Hiding/reordering a display item never changes native membership.

Presentation uses Stellar-style compact tag chips for flat global tags and quiet
directory rows for categories/hierarchical indexes. Full native counts and nested links
remain; pagination applies to article results, not tag/category vocabulary indexes. Contextual result headers consolidate global/scoped links and show
the full count once in the list metadata; authors/series breadcrumbs use native display
titles rather than the raw assignment key. No membership or sequence policy changes.


Collection browsing refinement: `taxonomy_hubs=index` renders scoped tag/category roots as
vocabulary indexes (shared default for every scope); explicit `list` retains the alternative
all-content list. Term pages, native assignments and full union counts are unchanged. Wide
categories honor the existing hierarchy flag; flat tag chips do not flatten hierarchical tags.
Global indexes share this source-based renderer. `All categories` is the sidebar hub caption.
