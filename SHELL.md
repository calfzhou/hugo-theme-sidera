# Page shell and native regions (P2-F)

Implemented on Hugo 0.166.0. This is an independent Hugo theme, not Stellar's
configuration API. The collection-overview home remains the default. Cards,
selected-collection home and configurable article/site footers are later P2 work—not installed settings in this guide.

## Defaults and configuration

Public consumer settings now use native `params`, not a blanket `params.sidera` map.
Native taxonomies/menus/date fields remain native. [CONTRACT.md](CONTRACT.md) is the complete
field/type/domain reference and [PRESETS.md](PRESETS.md) describes the three-target fallback.
Private generated navigation metadata remains namespaced; no old public-key reader or alias.

Fixed components: menu, collections, taxonomies, **page-tree**, site-taxonomies, toc,
recent, profile, text, links. A profileless section can select the same components as any
preset. page-tree replaces the old docs-tree component name and has no docs-preset gate.
Arrays replace; false/[] disables a region. Unknown names/duplicates diagnose. Empty or
inapplicable components emit nothing and leave no ghost grid track. Standalone pages retain
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
No article/site footer configuration is advertised yet; that remains H.

## Native menus and data

Menus use ordinary native ordering/weights, `pageRef`, external `url`, language
menus and current/ancestor helpers. Two levels are supported. A parent without a
destination is a heading; destinationless leaves and unresolved pageRefs fail.
Parent page links remain links. Native menu labels are site-authored—not silently
translated identifiers. Both English and Chinese theme-owned wording uses i18n.
A `menus.<name>.params.icon` value can override its decorative icon. Icon names:
`home`, `blog`, `notebook`, `docs`, `page`, `tag`, `link`, `star`; `''` means none.
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
  tag and active ancestor branches. On articles all assigned branches open.
- **Page tree:** native immediate children and local order drive the complete tree, regardless of preset;
  ancestor/current branches open. A parent body's link and its disclosure are
  separate keyboard targets. No secondary paginator.
- **Recent:** Lastmod/Title/Path, independent of pins and current pager. Owner
  scope excludes nested independently marked collections. recent_sections=true includes
  body-bearing descendant sections as well as regular leaves. With no owner,
  recent means current-language Site.RegularPages (explicitly global).
- **TOC:** native headings, only with the rendered article/docs body; no TOC on
  later docs child pagers whose body is intentionally omitted. Full standalone
  support. A right disclosure moves in flow above main content on narrow screens.
- **Native taxonomies:** shared `tags`/`categories` on every content kind, global
  native indexes/results plus owner-scoped projections. See [TAXONOMIES.md](TAXONOMIES.md)
  for hierarchy/flat policy, deduplicated counts and pagination. These are now
  functional pages, not only navigation to future taxonomy templates.

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
region changes do not need template copies. No article/site-footer hook is
advertised yet.

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
The inline mark and geometric icons are original project artwork.

Desktop at 1440: left x32/w288, main x384/w696, optional right x1112.
Below 1231px right becomes an in-flow native disclosure; below 761px left does too.
No JS leaves navigation open and dark readable; appearance controls stay hidden.
No modal/focus trap, fake search, remote background or persistent review server.

Native top-level `tags` and `categories` are assignments, not custom settings.
Hierarchy policy (`taxonomy_hierarchy`) and global size (`taxonomy_page_size`)
are site/owner choices described in TAXONOMIES.md; individual article exceptions
do not change the identity/membership rules of their owner’s taxonomy views.
