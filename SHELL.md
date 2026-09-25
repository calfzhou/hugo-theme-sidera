# Page shell, components and native footers (P2-F/G)

Implemented on Hugo 0.166.0. This is an independent Hugo theme, not Stellar's
configuration API. The collection-overview home remains the default. Reusable cards and
configurable article/site footers are implemented. P2-GR now refines whole-site/non-content composition; detailed Markdown and the
selected-collection home option remain separate; this is not whole-P2 acceptance.

## Defaults and configuration

Public consumer settings now use native `params`, not a blanket `params.sidera` map.
Native taxonomies/menus/date fields remain native. [CONTRACT.md](CONTRACT.md) is the complete
field/type/domain reference and [PRESETS.md](PRESETS.md) describes the three-target fallback.
Private generated navigation metadata remains namespaced; no old public-key reader or alias.

Fixed components: menu, collections, taxonomies, **page-tree**, site-taxonomies, toc,
recent, profile, text, links. A profileless section can select the same components as any
preset. page-tree replaces the old docs-tree component name and has no docs-preset gate.
Arrays replace; false/[] disables a region. Unknown names/options diagnose; repeated components are supported. Empty or
inapplicable components emit no empty region. Desktop left-shell views preserve the reading
track position when the right is absent rather than stretching the article into it. Standalone pages retain
the full shell; compact is explicit. Identity/home and appearance remain accessible when left is off.

Minimal defaults are left=[menu,profile], right=[toc], menu=primary, recent_count=5, icons=true.
Preset section/descendant maps may supply different defaults. Site/language values are below
preset values: use a native config cascade when deliberately overriding a preset site-wide.

```toml
# Useful fallback content and identity. It does not forcibly override preset region defaults.
[params.identity]
subtitle = 'A place for evolving ideas'
image = 'images/sidera-mark.svg'
[params.profile]
title = 'About this site'
text = 'A site-authored **profile**.'

[[menus.primary]]
name = 'Notes'
pageRef = '/field-notes'
weight = 10
[[menus.primary]]
name = 'Contact'
url = 'mailto:hello@example.org'
weight = 20
```

For a site's intentional whole-site layout override, native cascade already wins before preset fallback:

```toml
[cascade.params]
left = ['menu', 'taxonomies']
right = ['toc', 'recent', 'profile']
```

For one section's own UI, use its params. For its descendants, use native cascade.params:

```yaml
params:
  left: [menu, taxonomies]
cascade:
  params:
    left: [menu, taxonomies, recent]
```

Ordinary section params do not silently cascade. Native effective Page.Params is first, then
own selected-section preset defaults or ancestor descendant-default maps, then language/site/
minimal fallback. false/empty string/array/map remain meaningful; local nested maps replace
cascaded maps. No raw cascade reconstruction. children.order remains its narrow parent-local exception.
`preset: []` stops farther preset fallback only; scope_root controls browsing, not cascade reset.

A compact standalone page uses `params.left: false` and `params.right: []`. Empty text/menu
strings clear those values; profile={} clears the identity card. Identity is site/language-only.
Both footer arrays use the same presence-based resolver; see the footer contract below.

## Site identity interactions

The image is a circular home link (48px target, 44px image with a 2px ring inset).
Title and subtitle share a second home link covering their entire text box, not just glyphs.
Neither target underlines. Hover/focus on the image reveals Stellar's rotating rainbow ring
(4-second revolution). Hover/focus anywhere in the text box transitions the subtitle upward:

```toml
[params.identity]
subtitle = 'Notes & everyday tools | Small ideas, kept close'
```

The first `|` separates the resting and alternate text; later pipes remain literal in the
alternate. Both sides are trimmed, escaped plain text; an unsplit subtitle stays unchanged.
The two lines share a grid cell so differently sized/wrapped messages do not shift the page.
The alternate slogan is decorative to assistive technology; the home link keeps a stable name.
No JS is needed. Reduced motion shows a static ring and swaps text without movement.
Both links use the native language/subpath-aware home URL, including mobile and compact shells.

## Native menus and data

Menus use ordinary native ordering/weights, `pageRef`, external `url`, language
menus and current/ancestor helpers. Two levels are supported. A parent without a
destination is a heading; destinationless leaves and unresolved pageRefs fail.
Parent page links remain links. Native menu labels are site-authored—not silently
translated identifiers. Both English and Chinese theme-owned wording uses i18n.
A `menus.<name>.params.icon` value can override its decorative icon. Icon names:
`home`, `blog`, `notebook`, `docs`, `page`, `tag`, `link`, `star`; `''` means none.
Optional `menus.<name>.params.color` supplies that entry's icon/selection-dot accent on
hover, focus-visible or current/ancestor selection. Omission or `''` uses the theme accent.
It accepts hex `#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`; invalid types/CSS diagnose at build time for rendered entries,
even with icons off. Labels stay neutral, and a hover-only row does not acquire a selection dot.
The accent belongs to the entry, not its parent/child or a Page's inherited settings.

```toml
[[menus.primary]]
name = 'Journal'
pageRef = '/journal'
[menus.primary.params]
icon = 'blog'
color = '#ffbd2b'
```

Main `menu` components use Stellar's 1.5rem (27px at the default root size) icons, 12px
icon/label gap, 4px adjacent-row gaps and 8px selected dots. Discovered fallback main links
use the same sizing/spacing. Profile/link/footer menus retain their smaller icon treatment.
Selection dots belong only to main-menu links (including their selected ancestors), even with
icons=false. Tag/page trees, taxonomy hubs and auxiliary link/profile menus use their current-row
highlight without dots. Tree counts remain visible and right-aligned across branches, leaves and
indentation levels; every row reserves the same disclosure column. These are local native
menu params; arbitrary CSS strings, URLs and authored SVG are never accepted as color values.

No config-supplied SVG/HTML, `pre`/`post` markup, callbacks or forced new tabs.

URLs allow local URLs and `http://`, `https://`, `mailto:`; dangerous schemes,
backslashes and control/whitespace characters reject. Use `pageRef` for internal
Pages so Hugo supplies language/baseURL/dated permalinks, and explicit `https://`
for external links. Hugo itself normalizes protocol-relative `//host` into a local
path before exposing menu entries; it is not a supported external-link spelling.
Native `url` destinations, unlike `pageRef`, remain site-authored and require the
site's own route/link checks. The theme doesn't invent destinations for absent
features. `links`/profile menus are absent when the selected menu is absent.

- **Taxonomies:** complete nearest-owner flat/hierarchical views, full deduplicated counts, current
  tag and active ancestor branches. On articles all assigned branches open. Sidebar headings
  use the localized taxonomy label alone, without repeating the collection name.
- **Page tree:** native immediate children and local order drive the complete tree, regardless of preset;
  ancestor/current branches open. A parent body's link and its disclosure are
  separate keyboard targets. No secondary paginator.
- **Recent (`recent`):** each instance selects `config.order=modification` (default,
  caption Recent updates) or `publication` (caption Recently published). Lastmod descending versus PublishDate descending,
  then Title/Path ascending; zero dates sort last. Both ignore pins and the main paginator.
  Owner scope excludes nested independently marked collections. recent_sections=true includes
  descendant sections as well as regular leaves. With no owner, both use current-language
  Site.RegularPages. Rows show only one ellipsized title, with the full escaped title in the
  native tooltip/accessibility name; no date or scope-explanation line.
- **TOC:** native headings, only with the rendered article/docs body; no TOC on
  later docs child pagers whose body is intentionally omitted. Full standalone
  support. A right native popover drawer is available below 1181px; without JS/Popover support the region stays open in flow.
- **Native taxonomies:** shared `tags`/`categories` on every content kind, global
  native indexes/results plus owner-scoped projections. See [TAXONOMIES.md](TAXONOMIES.md)
  for hierarchy/flat policy, deduplicated counts and pagination. These are now
  functional pages, not only navigation to future taxonomy templates.

## Per-instance configuration

The same entry format works in **left, right, article_footer and site_footer**:

```yaml
params:
  left:
    - menu
    - component: recent
      config: {order: publication, count: 5}
    - component: recent
      config: {order: modification, count: 8}
    - component: text
      config: {text: 'A short **site note**.'}
  article_footer:
    - terms
    - component: text
      config: {text: 'Thanks for reading.'}
    - component: links
      config: {menu: article}
```

A name string is shorthand for `{component: name, config: {}}`, not a legacy alias. Repeat
any component within/across regions, with different settings or defaults. No author IDs are
required. Site identity and the main article remain site/page settings, not entries in these regions. Only `component` and optional `config` are accepted; arbitrary template paths,
unknown options, wrong types and components in the wrong region fail the build.

The existing native Page/cascade → preset → site/default resolution first selects the whole
region array and default settings. Then each instance overlays **only its supported options**
on a fresh local settings map. Omitted options inherit; explicit false/empty strings/arrays/maps
win. Supplied maps (such as tag_icons) replace, not deep-merge. For profile, each flat config
field overrides that field in the resolved profile; `image: ''` removes the inherited image.
`config: {}` means all defaults, not “disable”. Use false/[] on a region to disable it.
Neither Page.Params, the cached page settings, another instance nor a region hook is mutated.

### Sidebar options

| Component | Instance `config` keys | Default source |
|---|---|---|
| menu | menu (string), icons (bool), taxonomies (array or false, for fallback navigation) | menu, icons, taxonomy_navigation |
| collections | icons (bool) | icons |
| taxonomies | taxonomies (array or false), icons (bool), tag_icons (map of fixed icon names) | taxonomy_navigation, icons, tag_icons |
| site-taxonomies | taxonomies (array or false), icons (bool) | taxonomy_navigation, icons |
| page-tree | No presentation options yet; config may be omitted or empty | Native owner/tree/local order, not instance data |
| toc | icons (bool) | icons |
| recent | order (publication/modification), count (integer 1–10), sections (bool) | modification; recent_count; recent_sections |
| profile | title, text, image, menu (strings), icons (bool) | Corresponding profile fields; icons |
| text | text (Markdown string) | text |
| links | menu (string), icons (bool) | links_menu; icons |

Taxonomy names must exist in the current native site vocabulary. Hierarchy, source membership,
term-link policy, tree ordering, scope boundaries and paging remain page/site model decisions;
they are not silently overridden by an instance. Image/Markdown/menu URL safety uses the existing
native consumers. Raw local source validates instance shapes/options including drafts; resolving
excluded resources/native references still requires the documented all-states build.

### Footer options

`text.config.text` and `links.config.menu/icons` work in both footers, defaulting to the existing
article_text/article_links_menu or footer_text/footer_menu settings. Article `meta.config.show`
and `authors.config.show` default to show_updated/show_authors but only affect that footer
instance, not the article header. Terms, series and site credit have no additional presentation
options yet; their config may be omitted or empty. All footer items can repeat.

### IDs and trusted overrides

Instances have region/type/occurrence identities (`data-instance`, also `.Instance` in partials).
Repeated TOCs, taxonomy trees and footer attribution/terms receive distinct IDs. First occurrences
keep their natural region IDs; subsequent occurrences get deterministic numeric suffixes, even
if an earlier instance emits no content. Native heading anchors stay shared; collapsing one TOC
or tree does not collapse its siblings. Main-menu selection indicators stay limited to `menu`
instances, not auxiliary links/profile menus.

Trusted fixed component partial overrides receive the usual Page/Owner/Region plus **Config**,
local **Settings**, **Instance**, **IDScope** and **IDSuffix**. Use IDScope/Instance when producing
DOM IDs, not Region alone. Footer hooks still run once with the base region settings; they do not
inherit the last component's local options. Built-ins share existing renderers, not copied backends.

One `recent` instance can show new notebook entries while another shows updates. Both ignore
pins/main pagers, use the full nearest-owner collection, exclude independent nested scopes, and
sort ties by Title/Path with zero dates last. Without an owner they use current-language regular
pages. The bundled presets retain their existing selections; Fieldbook explicitly demonstrates
publication-order recent links on Notes and both orders on Handbook.

## Assets, escaping and extensions

Titles/menu labels are ordinary escaped text. Markdown uses native RenderString,
**not blanket safeHTML**. Goldmark's default raw-HTML rejection remains; a strict
build rejects its warning. Enabling unsafe Markdown is a deliberate site trust
choice, not a theme default. Native generated TOC markup alone is decorated with
unique region IDs. Author-supplied SVG/HTML strings cannot become icons or code.

Image lookup: current Page resources, nearest-owner resources, global assets, then
site static paths. Identity uses Home/resources/assets/static. Remote images,
traversal, unsupported extensions and missing local images diagnose. Relative
Markdown links inside profile/text have normal native Markdown semantics; use
appropriate site paths. No remote font/resource download or external service.

Stable F hooks under `layouts/_partials/sidera/`: `head-extra.html`,
`left-extra.html`, `right-extra.html`. Empty by default. Context dictionary:
`Page`, `Owner` (false when absent), `Region` (`head`/`left`/`right`), `Settings`
(resolved values). Region extras appear after components; false/empty region
selection suppresses its extra. An otherwise empty region may be supplied by an
extra. Site templates are trusted code, not configurable executable paths.

Each fixed built-in also has a native override under
`layouts/_partials/sidera/components/<fixed-name>.html`, receiving the same context.
There is no arbitrary component name/path registry. Routine menu/profile/text/
region changes do not need template copies. P2-G adds `article-footer-extra.html` and
`site-footer-extra.html` with the same context (Region is article-footer/site-footer).
Empty/false footer selection suppresses its hook; selected but empty built-ins permit
a hook-only footer. No resulting markup means no footer box or spacing.

Example trusted site-only right extra:

```go-html-template
{{ with .Owner }}
  <p><a href="{{ .RelPermalink }}">{{ .Title }}</a></p>
{{ end }}
```

Native CSS tokens: `--ui`, `--reading`, `--code`, `--canvas`, `--surface`, `--panel`,
`--surface-hover`, `--line`, `--text`, `--muted`, `--accent`, `--pin`, `--measure`.
Use head-extra to load an owner CSS asset *after* theme CSS. UI/prose prefer local
LXGW WenKai, then Helvetica Neue/PingFang/Arial; code prefers local Source Code Pro,
then Menlo/Consolas. The portable fallback is visibly different. Owner-supplied
local fonts need their own rights/notices; none are downloaded or distributed here.
The inline mark/link icon are original artwork; a small pinned Solar icon subset and Stellar drawer icons are local, with separate notices in THIRD-PARTY-NOTICES.md. No authored SVG strings are trusted.

Desktop uses Stellar's bounded 720px reading track (696px at a 1440px viewport with
8px scroll gutter), 288px left and 320px right rails. List cards have an 18px inner gutter;
article banners span the reading track. The left rail fills the viewport and scrolls widgets
independently of identity/appearance. Sidebar, drawer and TOC scrollbars are hidden, as in
Stellar; native wheel/touch/keyboard scrolling and focus-reveal still work. This does not hide
the document scrollbar or article code/table scrollbars. Its neutral fading surface uses no borrowed background art.
At 1180px the right region becomes a native auto-popover; at 667px the left does too.
Floating controls, Escape/light-dismiss, explicit close and native focus return remain usable.
Only one drawer opens at a time. No modal focus trap; no-JS/unsupported browsers retain open
in-flow disclosures. Appearance stays a labeled native three-way select, unlike Stellar's
binary theme action: System mode and keyboard usability are retained. No fake search/services.

Native top-level `tags` and `categories` are assignments, not custom settings.
Hierarchy policy (`taxonomy_hierarchy`) and global size (`taxonomy_page_size`)
are site/owner choices described in TAXONOMIES.md; individual article exceptions
do not change the identity/membership rules of their owner’s taxonomy views.


## Article and site footers

Public params, using exactly the same native Page/cascade → applicable preset maps →
Site/minimal fallback. Ordinary section params do not become descendant defaults.

| Region / default items | What renders |
|---|---|
| article_footer=[terms,meta,series,text,links] | terms: actual assigned tags/categories and contextual hubs; meta: native Lastmod only when show_updated; series: existing scoped sequence; text: article_text; links: article_links_menu |
| Optional article item authors | Ordered native authors, local portrait if provided; show_authors still applies. Header attribution remains, so this is intentional extra closing attribution. |
| site_footer=[links,text,credit] | links: footer_menu with native two-level columns; text: footer_text; credit: localized Built with Hugo · Sidera |

Article footer renders after a real shared article/section body, not on later child-list
pagers without that body. Metadata/header byline and publication dates retain their behavior.
Terms move to the footer by default; terms_in_header=true duplicates them with unique IDs.
No terms, date, series, menu or text means no corresponding item/divider. A wholly empty footer
has no container. No empty assigned-term list is emitted just to preserve an old DOM ID.
`meta` may repeat the header's update date as a closing record; omit it if unwanted.

```yaml
# One page (or params in a real native cascade for descendants)
params:
  article_footer: [terms, authors, text, links, series]
  article_text: 'Thanks for reading. [About this site](/about/).'
  article_links_menu: article
  site_footer: [links, text] # deliberately no theme credit
  footer_menu: footer
  footer_text: 'An independently maintained notebook.'
  terms_in_header: false
```

Menu columns use native entries with identifier/name and children with parent; a parent
may have a real pageRef link or be a heading. Native weights/ordering/current states and
URL/depth validation are shared with sidebar menus. Authored Markdown is rendered by
RenderString with the site's normal raw-HTML policy. No inferred license, hidden service,
placeholder share/comment control, external resource, or automatic copyright year.
Arrays reject unknown components/options; repeated instances are supported; false/[] disables; empty strings clear text/menu.
Unused preset maps also validate these fields. Excluded Page-level references/presentation
values require the normal all-states build; draft is not an exemption.

Small trusted override at `layouts/_partials/sidera/article-footer-extra.html`:

```go-html-template
{{ with .Page.Params.closing_note }}<p>{{ . }}</p>{{ end }}
```

`closing_note` here is site-owned escaped text, not a new built-in param. Native template
code is trusted; no arbitrary partial path or executable code is accepted from config.

## Cards and interaction

Ordinary result cards and immediate-child cards share one native card partial. Local covers
are optional, clipped to 2:1, with no hero/gallery mode or automatic remote image. Excerpt
uses native description, then plain native Summary; two desktop/three narrow lines. The
main date follows modification-first lists, otherwise publication (docs children use
Lastmod). Zero dates remain localized/unknown. Pins do not change their sorting contract.
Direct term badges use the existing normalized assignment/link model, not another taxonomy
backend. Counts/indexes, complete pager chains and scoped/global links remain native.

```yaml
params:
  cover:
    image: sample.svg # Page/owner resource, assets, then static
    alt: Two connected sample nodes # explicit; empty only when decorative
```

Cover is read from effective native Page.Params, including deliberate native cascade.
It is not a preset fallback setting: a preset must not accidentally choose member artwork.
{} clears it. Missing alt, malformed maps, unsafe paths and missing published assets diagnose;
raw local excluded sources receive the map/type/alt checks too. No image gets invented from
an article's first body image. Cards keep semantic headings with a stretched title target;
term/owner links remain independent keyboard and pointer targets.

`list_header=false` can hide a redundant recursive section title/intro/tools when its identity
is already in the menu. The default stays true; it uses the same Page/cascade/preset/site boolean
precedence. The accessible title, full list count, policy and pager remain; contextual taxonomy
headings and docs bodies are unaffected. See the live Fieldbook example in the showcase.

Rows share glass/quiet-surface hover, focus-visible, pressed and current/ancestor states.
Native tree links are independent from native disclosure summaries. The TOC uses real
anchors/history and a small passive, frame-batched scroll tracker for aria-current=location;
no click interception or remote content engine. Its scrollport keeps a newly current row visible without scrolling the document or stealing focus. Back-to-top is a
native link. Both rails retain sticky desktop behavior with narrow native drawers and an in-flow no-JS fallback.
Fine-pointer card tilt/spotlight adapts Stellar/React Bits; keyboard gets title/focus feedback without tilt. Reduced motion and touch remove tilt/spotlight, transitions and cover zoom; no JS leaves open, usable navigation.
Stellar-adapted styles retain [the upstream MIT notice](THIRD-PARTY-NOTICES.md). The theme's
own overall distribution license remains unresolved; this notice is not a new license grant.
