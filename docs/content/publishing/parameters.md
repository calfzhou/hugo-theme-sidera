---
title: "Public parameter reference"
params:
  ai_label: generated
---

Native fields (`title`, `description`, dates, `draft`, `type`, `url`, `slug`, `weight`,
`build`, `tags`, `categories`, `authors`, `series`, `preset`) stay top-level. Public
theme settings below live under **params**, not an additional namespace. Menu
extensions live under each native entry's params. Private generated fields are not
an authoring API. Unrelated site-owned params are allowed.

For ordinary inheritable settings: effective Page/native cascade → own section
preset defaults → nearest ancestor preset descendant defaults → language/site →
minimal default. See [presets](../organize/presets.md) for all three targets.
Valid false/empty values win; null is not reset. Arrays/maps replace at key boundaries.
Structural/root/local and site-only exceptions are stated explicitly below.

## Settings

| Setting | Meaning / default |
|---|---|
| auto_caption | Boolean, true. Direct standalone Markdown image title then cleaned alt becomes an escaped caption; false opts out using normal page/cascade/preset/site precedence. See [writing](../authoring/_index.md). |
| logo | Optional local collection-root image path; empty/omitted has no artwork. No inheritance/remote fetch; see [collection identity](../organize/_index.md). |
| name | Optional local collection-root short label; string, title fallback when omitted/blank. Not a preset/default/cascade field. See [collection identity](../organize/_index.md). |
| scope_root | Local section boolean; nested false, top-level implicit true. Browsing only. |
| byline | Additional escaped credit text; empty by default. Not author identity. |
| ai_label | Optional disclosure string: manual/reviewed/polished/generated; empty default/explicit clear. Native page/cascade/preset/site resolution; localized article-header text only, not body/index/author identity. See [writing](../authoring/_index.md). |
| navigation_mode | Collection-root policy: list (minimal/blog/notes), siblings (docs), or sequential. Root params override root preset then site/language default; not cascaded or set on member pages. Previous/Next stay within the complete collection sequence; Parent is the actual in-scope parent in siblings/sequential only; omitted in list mode. |
| primary_date | published (minimal/blog) or updated (notes/docs). Per-article date priority shared by cards/headers, independent of sorting; collection cards instead show member activity; normal params/cascade/preset/site precedence. |
| show_authors / show_updated | Native author visibility (true): compact linked names in the header; optional explicit footer authors / Lastmod visibility (minimal false; blog/notes/docs section and descendant presets true). |
| pinned | Page-local effective boolean, default false. Ordinary lists partition pins once before paging; no preset pin inheritance or numeric ranks. |
| list_header | Boolean, default true. Show the recursive section title/intro/tools. false keeps an accessible title and full counts/pagination, but emits no hidden-body TOC. Does not hide taxonomy result titles or docs bodies. |
| list_mode | recursive (regular descendants filtered to owner) or children (immediate document list). Minimal recursive. |
| list_order / page_size | publication or modification descending, or title ascending; stable Title/Path ties. Minimal title / positive integer 10. |
| children | Map with parent-local order, fallback sort=title or name, positive page_size=10, list=true. See [trees](../organize/trees.md). |
| recent_count / recent_sections | Positive integer (default 10); include descendant section documents (default false). Defaults for each recent instance (overridable by config.count/sections); full owner model, independent of main pins/pager. |
| taxonomy_hierarchy | Tags/categories interpreted hierarchically; default []. Notes preset supplies [tags]. Stable owner policy for scoped views; Site policy for globals. |
| taxonomy_page_size | Positive page size for global article results and other taxonomy directories; default 10. Tag/category vocabulary indexes are unpaginated. Scoped article results retain owner page_size. |
| taxonomy_navigation | Ordered configured taxonomy names; default [tags,categories]; []/false hides navigation only. |
| taxonomy_links | Map to section/global term-link preference. Missing entries use tags/categories/series→section and authors/preset→global. No scope/destination means a real global fallback. |
| color_mode | Site/language default dark/light/auto; theme default auto. Saved visitor choice wins. No forced control. |
| left_footer / social_menu | Pinned instance region, default [social]; native menu selector social. Empty menu emits nothing. |
| top | Same instance array/false contract; default []. Blog and notes presets select collection-nav for their sections. |
| taxonomy_hubs | index (shared default) or list (explicit all-content opt-in). Only scoped tag/category hub presentation, not native assignments, hierarchy or term membership. |
| left / right | Ordered component/widget names or inline component/config and widget/config maps, or false; defaults menu + global recent-updates / [toc], with preset overrides. []/false disables, no blank rail. |
| menu / links_menu / text | Native menu selector ('primary'), optional native links menu (''), native-rendered Markdown (''). Empty clears. |
| profile | Whole-map identity card: title/text/image/menu strings; {} clears. Not a preset. |
| widgets | Site/language-only map of named component/config definitions; theme supplies recent-updates/recent-published. Select names or widget/config uses in regions. See component options below. |
| identity | Site/language-only whole map: title/subtitle/image strings; native Site.Title fallback. subtitle supports resting text \| hover text (see [identity](../customize/_index.md#identity-and-appearance)). |
| icons / icon / tag_icons | Decorative visibility (true), named inline registry key (default page) or empty, classification-key icon map ({}). Native menu entries use params.icon and optional params.color (validated hex hover/current accent; see [menus](../customize/navigation.md)). |
| article_footer | Ordered component/widget names or inline component/config and widget/config maps, or false; default [terms,references,outgoing,backlinks,license,share,series,text,links]. Contiguous references/outgoing/backlinks/license/authors/share items form a box. []/false hides the region and its hook. |
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


| Additional site/language-only setting | Meaning / default |
|---|---|
| page_reveal | Boolean true; progressive entry motion, false omits controller. Not page/cascade/preset. |
| link_heading_checks | Boolean false; optional native-heading diagnostics for source links, not all HTML IDs. |
| comment_provider | String giscus; only built-in provider. Trusted native provider partial required for another name. |
| giscus | Site-owned identity/options map; repo/repo_id/category/category_id, strict=false, reactions=true, input_position=top or bottom. See [comments](../reader/comments.md). |

| Additional inheritable setting | Meaning / default |
|---|---|
| search | Boolean true; UI/local-index fetch. Site-wide false omits index generation unless overridden. |
| search_index | Boolean true; include actual published body/title in current-language index. Not access control. |
| link_graph | Boolean true; include published body as source and target of generated relationships. |
| comments | Boolean false; eligible canonical body-end slot. Explicit manual opt-out does not affect other site content. |

`children` defaults resolve to `sort: title`, `page_size: 10`, `list: true`; its
`order` alone is strictly parent-local. `pinned` is a page-local effective boolean,
not a numeric rank or preset pin. `cover` is an effective Page.Params map (including
intentional native cascade), not a preset fallback. Root logo/name never cascade.
Do not author widget definitions, identity, color mode, page motion, heading checks,
provider or Giscus settings in a page/preset/cascade.

## Component options

Top/sidebar family below is allowed in top, left, right and left_footer. Select
components/widgets via region arrays, not a dynamic template path. Omitted options
use their shared parameter fallback; explicit empty values replace; config={} means
defaults. Native widget definitions belong only in site/language params.widgets.

| Component | Allowed config | Default source |
|---|---|---|
| social | menu, icons | social_menu, icons |
| collection-nav | items: array of recent/categories/tags/archive | All four; empty taxonomies disappear |
| menu | menu, icons, taxonomies (array/false) | menu, icons, taxonomy_navigation |
| collections | icons | icons |
| taxonomies | taxonomies (array/false), icons, tag_icons | taxonomy_navigation, icons, tag_icons |
| site-taxonomies | taxonomies (array/false), icons | taxonomy_navigation, icons |
| page-tree | none | Native owner/tree/local order |
| toc | icons | icons |
| recent | order (publication/modification), count (positive integer), sections (boolean), scope (owner/global) | modification, recent_count, recent_sections, owner |
| profile | title, text, image, menu (strings), icons | profile fields, icons |
| text | title (plain string), text (Markdown) | text; no title |
| links | menu, icons | links_menu, icons |

Recent ignores pins/main pagination. Owner scope excludes independent nested roots;
no-owner and explicit global use current-language regular pages, not sections.
Bundled recent-updates/recent-published widgets differ only in order. Repeated
instances keep independent context and IDs.

Article footer allows text/links plus these components:

| Component | Allowed config / fallback |
|---|---|
| terms, series, outgoing, backlinks | none |
| meta | show / show_updated |
| authors | show, edit_url / show_authors, edit_url |
| references | entries / references |
| license | text / license |
| share | targets, icons / share, icons |
| text | title, text / article_text |
| links | menu, icons / article_links_menu, icons |

Site footer allows `links` (menu=footer_menu, icons=false), `text`
(title/text=footer_text) and `credit` (no options, native built_with message).
Supported per-use icons=true can override the default. Repeated footer items are
allowed; incompatible regions, unknown options and unused malformed widgets fail.
Config types follow their setting types; widgets never derive from other widgets.
