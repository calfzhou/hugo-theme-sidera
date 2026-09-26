# Sidera content and configuration contract

Implemented P2-M model on Hugo **0.166.0**. This is an independent Hugo theme, not a
Stellar configuration port. P2-G adds reusable component styling and configurable footers;
P2-GR corrects whole-site/non-content composition against Stellar. Ordinary Markdown is refined in P2-H (see README); unverified homepage capabilities remain
for the post-P3 integrated review, not this body-only checkpoint.
No Hexo, Node runtime, downloaded dependency, duplicated source repo or Go-module switch is
required to build. Showcase tests use Python stdlib; browser tests use its pinned Node/Chrome.

## Theme versus site ownership

Sidera owns the native taxonomy definitions and term-URL defaults in `hugo.toml`, the
blog/notes/docs preset library and all reusable rendering/validation. The site grants narrow
native import permission, without copying those definitions:

```toml
theme = 'sidera'
[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'
[markup.tableOfContents]
_merge = 'shallow'
```

The theme provides tag→tags, category→categories, author→authors, series→series and
preset→preset. Site keys override or extend those native tables. The last import supplies the theme
TOC range H1–H6 (Stellar defaults); explicit site startLevel/endLevel values still win.
No global/security or broad markup merge is enabled. Date chains, baseURL, language, timezone, page permalinks and pagination
remain deliberate site policy. The verified showcase retains:

```toml
[frontmatter]
date = ['date','publishDate','pubdate','published']
publishDate = ['publishDate','pubdate','published','date']
lastmod = ['lastmod','modified','publishDate','pubdate','published','date']
[pagination]
path = 'page'
disableAliases = true
```

Missing dates stay unknown; Git/mtime/build time do not invent article dates. Journal's
publication-date URL rule is site-specific, not a preset rule. Native reserved metadata,
menus, taxonomy assignments and resources stay native. Other user params remain allowed.

## Structure, browsing scope and presets are separate

A native top-level content section is a browsing root automatically. A nested section stays
within the nearest outer root unless its `_index.md` explicitly sets `params.scope_root=true`.
False/omission on a nested section means shared scope; false does not disable a top-level root.
Never cascade this structural marker. Ordinary root-level pages remain standalone.

```yaml
title: Research
preset: notes
params:
  scope_root: true  # needed only when this is an independently browsed nested section
```

`preset` is an optional native taxonomy assignment, preferably a scalar, with a one-element
array also accepted. **It never changes ownership.** One distinct preset per section; not
on regular pages and not cascaded as membership. A section without a preset has the same
capabilities through explicit params. Fourth/custom presets are native term Pages, not an enum.
Title/Path/native relationships supply identity; articles do not repeat collection IDs.

Owners filter recursive lists and scoped taxonomy/recent views; independent nested roots do
not leak into their outer collection. Native leaf bundles still have no descendant Pages;
body-bearing parents use branch `_index.md`. Do not confuse native parentage with browsing scope.

## Three distinct targets for preset defaults

The term's own `params`/body configure that public term Page. Its member-default fragment is:

```yaml
title: My documentation preset
slug: handbook
params:
  left: [menu]                # public term UI
  defaults:
    params:                  # section explicitly selecting this term
      list_mode: children
      left: [menu, page-tree, taxonomies]
    cascade:
      params:                # descendant content Pages
        list_mode: children
        left: [menu, page-tree, taxonomies]
        right: [toc]
        show_updated: true
```

Resolution of an inheritable custom key:

1. Effective native Page.Params (Hugo already applied actual local/cascade values).
2. A selecting section's own preset `defaults.params`.
3. Ancestor sections' preset `defaults.cascade.params`, nearest first.
4. Current-language Site.Params, then minimal theme defaults.

**Ordinary ancestor Params do not implicitly cascade.** Use real `cascade.params` for
site-authored descendant defaults. A scope boundary is not a cascade firewall: structural
ancestry and real native cascade still apply. `preset: []` deliberately stops farther preset
fallback maps, but does not retract already-effective native values. Omission keeps fallback.
Contextual generated views query the owning section's view policy, not an article's metadata.

Presence wins: valid false, empty string/array/map override lower tiers. Null is not a reset
API. Arrays and maps replace at their key boundary; native local-map cascade replacement and
site/language config merging happen before this resolver. No raw-file cascade reconstruction,
full second cascade matcher, implicit native taxonomy assignment or legacy dual reader.
Preset defaults accept only implemented inheritable custom keys, not native fields, pins,
identity/scope markers, author assignments or parent-local child order.

## Public custom settings

All these are under **`params`**, not `params.sidera`. Grouping is retained where meaningful.

| Setting | Meaning / default |
|---|---|
| scope_root | Local section boolean; nested false, top-level implicit true. Browsing only. |
| byline | Additional escaped credit text; empty by default. Not author identity. |
| navigation_mode | Collection-root policy: list (minimal/blog/notes), siblings (docs), or sequential. Root params override root preset then site/language default; not cascaded or set on member pages. Previous/Next stay within the complete collection sequence; Parent is the actual in-scope parent in siblings/sequential only; omitted in list mode. |
| primary_date | published (minimal/blog) or updated (notes/docs). Per-page date priority shared by cards/headers, independent of sorting; normal params/cascade/preset/site precedence. |
| show_authors / show_updated | Native author visibility (true): compact linked names in the header; optional explicit footer authors / Lastmod visibility (minimal false; blog/notes/docs section and descendant presets true). |
| pinned | Page-local effective boolean, default false. Ordinary lists partition pins once before paging; no preset pin inheritance or numeric ranks. |
| list_header | Boolean, default true. Show the recursive section title/intro/tools. false keeps an accessible title and full counts/pagination, but emits no hidden-body TOC. Does not hide taxonomy result titles or docs bodies. |
| list_mode | recursive (regular descendants filtered to owner) or children (immediate document list). Minimal recursive. |
| list_order / page_size | publication or modification descending, or title ascending; stable Title/Path ties. Minimal title / positive integer 10. |
| children | Map with parent-local order, fallback sort=title or name, positive page_size=10, list=true. See DOCS.md. |
| recent_count / recent_sections | 1–10 (default 5); include descendant section documents (default false). Defaults for each recent instance (overridable by config.count/sections); full owner model, independent of main pins/pager. |
| taxonomy_hierarchy | Tags/categories interpreted hierarchically; default []. Notes preset supplies [tags]. Stable owner policy for scoped views; Site policy for globals. |
| taxonomy_page_size | Positive global/index page size; default 10. Scoped result lists retain owner page_size. |
| taxonomy_navigation | Ordered configured taxonomy names; default [tags,categories]; []/false hides navigation only. |
| taxonomy_links | Map to section/global term-link preference. Missing entries use tags/categories/series→section and authors/preset→global. No scope/destination means a real global fallback. |
| color_mode | Site/language default dark/light/auto; theme default auto. Saved visitor choice wins. No forced control. |
| left_footer / social_menu | Pinned instance region, default [social]; native menu selector social. Empty menu emits nothing. |
| top | Same instance array/false contract; default []. Blog preset selects collection-nav for the section. |
| taxonomy_hubs | index (shared default) or list (explicit all-content opt-in). Only scoped tag/category hub presentation, not native assignments, hierarchy or term membership. |
| left / right | Ordered component/widget names or inline component/config and widget/config maps, or false; defaults [menu,profile] / [toc], with preset overrides. []/false disables, no blank rail. |
| menu / links_menu / text | Native menu selector ('primary'), optional native links menu (''), native-rendered Markdown (''). Empty clears. |
| profile | Whole-map identity card: title/text/image/menu strings; {} clears. Not a preset. |
| widgets | Site/language-only map of named component/config definitions; theme supplies recent-updates/recent-published. Select names or widget/config uses in regions. See SHELL.md. |
| identity | Site/language-only whole map: title/subtitle/image strings; native Site.Title fallback. subtitle supports resting text \| hover text (see SHELL.md). |
| icons / icon / tag_icons | Decorative visibility (true), fixed icon name/empty, classification-key icon map ({}). Native menu entries use params.icon and optional params.color (validated hex hover/current accent; see SHELL.md). |
| article_footer | Ordered component/widget names or inline component/config and widget/config maps, or false; default [terms,references,license,share,series,text,links]. Contiguous references/license/authors/share items form a box. []/false hides the region and its hook. |
| site_footer | Ordered link/text/credit component or derived-widget references, or false; default [links,text,credit]. []/false hides the region and hook. |
| references | Array of Markdown strings, default []; blank entries omitted. Authored references only, not automatic backlinks. |
| license | Markdown string, true (localized neutral default), or false. Default true; empty string also hides. Content notice, not a theme software license. |
| share | Ordered unique array of link/wechat/weibo/email or false; default [link,wechat,email]. []/false hides. Local Hugo QR, no QR service. |
| edit_url | Explicit safe URL string, default empty; shown when the optional footer Authors component is explicitly selected; no automatic repository mapping/API. show_authors=false hides that section including edit link. |
| article_end_text | Optional final Markdown after navigation and any docs child list, default empty. Native site/cascade/page overrides; independent of footer text/visibility. Empty clears. |
| article_text / article_links_menu | Native Markdown closing text / native menu name; both default ''. Empty clears. |
| footer_text / footer_menu | Native Markdown site-footer text / two-level native sitemap menu; both default ''. Empty clears. |
| terms_in_header | Boolean, default false. Opt-in duplicate header terms; footer terms remain independently selectable. |
| cover | Effective Page.Params image/alt map, default absent; {} or image='' hides. image requires explicit alt ('' for decorative). Local safe resource lookup; no preset-default cover or automatic image selection. |
| avatar | Author-term local portrait string; empty means none. Safe local image lookup. |
| series_order | Publication order only: oldest PublishDate first, undated last, stable Title/Path ties. Omission or publication accepted; weight/other values diagnose. Native series_weight has no effect on Sidera series order. |

Fixed components: social, collection-nav, menu, collections, taxonomies, **page-tree**, site-taxonomies, toc,
recent, profile, text, links. A page tree is available irrespective of preset/list mode.
In recursive list mode, native non-section storage folders may flatten into their parent tree;
children-mode document trees retain the P2-W explicit intermediate-branch/order checks.
Unknown components/options/malformed fields diagnose; repeated component instances are allowed. Fixed icons remain home/blog/notebook/
docs/page/tag/category/link/star; custom preset names are never used as required icon/i18n enum values.

Native assignments are `tags`, `categories`, `authors`, `series`, `preset` at top level.
Authors support multiple ordered identities. Series accepts one distinct native term per page;
its global union and independent section-scoped sequence coexist. See TAXONOMIES.md.

## Presets and migration

The theme's native per-language adapter supplies real blog/notes/docs term Pages from one
bundled data source, with native site-over-theme replacement. Site-authored same-path term files
replace the whole definition, not an implicit deep merge. Term titles/body are ordinary authored
content; bundled labels use native EN/ZH i18n. No need to re-register presets in the showcase.
[PRESETS.md](PRESETS.md) explains overriding/adding a term and the bundled defaults.

Pre-release migration is direct: collection markers become native preset plus explicit scope_root
where independent nesting is intended; public params lose the blanket wrapper; article defaults
move from owner metadata to native cascade when needed. Root-only values remain root-only. Existing
notebook/wiki enum aliases are not a compatibility layer—author native notes/docs/custom terms.
The old docs-tree component is now page-tree. No real-site content was converted.

Only generated internals remain under `params.sidera`: tag_view, tag_key, tag_slug, tag_taxonomy,
inferred_term, term_key. Do not author them; unrelated user namespaces/params are not banned.

## Validation, authoring and lifecycle boundary

The contextual route adapter still inventories supported **local TOML/YAML Markdown**, including
filename translations, and recognizes the built-in taxonomy source roots. Native published Pages
supply actual memberships/counts. Arbitrary custom taxonomy source trees, content mounts/adapters,
other formats and computed/cascaded route vocabulary are not universal loader support. Additional
native taxonomy configuration/global groups are possible; validate new source layouts explicitly
rather than assuming this bounded inventory handles every Hugo input.

Scope source paths currently use lowercase ASCII slug segments and their native path routes;
reserved pagination/context taxonomy namespaces, malformed/sluggable assignments and collisions
are validated independently of preset labels. Do not silently broaden those verified route limits
into a promise about an arbitrary site. Native term URL remapping/language/subpath behavior is tested.

Draft is not a structural-validation exemption. Raw local scalar/cardinality/route checks cover
excluded source; references/parent-local document rules additionally require the documented native
all-states validation build for unreferenced excluded content, as in P2-W. Fresh successful builds
into new destinations remain authoritative; watcher defects and harmless empty inferred term routes
retain D-010's migration tolerance, not production privacy approval. No failed build is publishable.

```sh
mkdir -p .checks
run=$(mktemp -d "$PWD/.checks/build-XXXXXX")
hugo --destination "$run/public" --cacheDir "$run/cache" --panicOnWarning --printPathWarnings --printI18nWarnings
# Structural review of otherwise excluded content, to a separate private local destination:
hugo --buildDrafts --buildFuture --buildExpired --destination "$run/all-states" --cacheDir "$run/all-cache" --panicOnWarning --printPathWarnings
```

Bundled actual docs remain outside default content and need explicit mounts (DOCS.md); preset
metadata never enables them. Standalone reading/shell, localization, dark/light/auto behavior,
local resources and safety remain intact. P3-A adds the [source-link contract](LINKS.md); no later P3 service/renderers, full browser/accessibility
certification, distribution license grant or P2 visual completion is implied.

## Component instances

All six configurable regions accept component/widget names, `{component: name, config: {...}}`
and `{widget: name, config: {...}}` entries.
Config is a typed component-specific presentation overlay after the normal resolver. Named
widgets add reusable defaults before per-use options; they do not change the resolved data scope. Repeats are supported and get distinct DOM IDs. No Page.Params/cache mutation or native
model change. SHELL.md contains the complete per-component option/default table and empty semantics.
There is one recent component with instance order=modification/publication, not a second component.


Collection browsing adds private generated `params.sidera.archive_view` and the reserved
`archives` namespace at supported local roots. Archives are native list-excluded rendered Pages,
not content-kind/scope roots. The root's native publication subset drives one separate archive
paginator; list/tree/recent/taxonomy membership stays unchanged. See SHELL.md for the component,
index presentation, collision guards and bounded-source limitations.

Widget definitions are native site/language params, not Page/preset metadata. Built-in component
names cannot be shadowed and widgets cannot derive from other widgets. Native config merging
precedes validation; per-use options replace shallowly and IDs count the resolved component kind.
The two recent widget names are reusable definitions, not additional components or legacy aliases.

Social entries use native menu params.icon/image or the whitelisted onclick action
Sidera.cycleColorMode(). No arbitrary JavaScript, fetched icon content or template paths are
accepted. Owner color-mode defaults are separate from page/instance settings and visitor storage.
SHELL.md defines exact behavior, local-image safety, six-entry bound and no-JS fallback.

## Source-link diagnostics

[LINKS.md](LINKS.md) is the authoring/override contract. Site/language-only
`params.link_heading_checks` is a boolean, default false; it is not inherited through
page/cascade/preset settings. Unresolved sources warn by default through native
`sidera-link-source`; native-heading checks are opt-in because non-heading IDs are valid.
No native markup or security setting is changed to activate the theme link hook.
