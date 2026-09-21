# Page shell and native regions (P2-F)

Implemented on Hugo 0.166.0. This is an independent Hugo theme, not Stellar's
configuration API. The collection-overview home remains the default. Cards,
selected-collection home, blog taxonomy index/result templates and configurable
article/site footers are later P2 work—not installed settings in this guide.

## Defaults and configuration

All **new shell settings** are under `params.sidera`. Existing collection markers,
notes tags, list policies, pins, article metadata and `children` settings retain
their current locations in CONTRACT.md and DOCS.md. F deliberately avoids an
unrelated mass rename. There are no dual readers or old/new precedence aliases.
`notes`/`notebook` and `docs`/`wiki` are intentional kind synonyms, not key shims.

| Setting | Default / supported values |
| --- | --- |
| `left` | Notes: `['menu','notes-tags','recent']`; blog: `['menu','blog-taxonomies','recent']`; docs: `['menu','docs-tree']`; other: `['menu','profile']` |
| `right` | `['toc']`; disappears unless a rendered reading body has headings |
| `menu` | `'primary'`; a missing/empty native menu gets Home + discovered collections + ownerless regular pages; `''` clears it |
| `links_menu` | `''`; name of a native menu; absent/empty menu emits nothing |
| `text` | `''`; authored Markdown via native Page.RenderString |
| `profile` | `{}`; optional `title`, `text` (Markdown), `image`, `menu` strings; replaced as a whole map |
| `identity` | `{}`; site/language only: optional `title` (otherwise native site title), `subtitle`, local `image` |
| `recent_count` | `5`; integer 1–10, never zero-as-default |
| `blog_taxonomies` | `['tags','categories']`; reorders/hides navigation to actual native `blog_tags` / `blog_categories` taxonomy Pages |
| `icons` | `true`; `false` hides decorative icons, not text |
| `icon` | Optional fixed icon name on a collection Page, used in auto/native navigation |
| `tag_icons` | `{}`; normalized full notes-tag keys mapped to fixed icon names; whole-map replacement |

Fixed region components: `menu`, `collections`, `notes-tags`, `docs-tree`,
`blog-taxonomies`, `toc`, `recent`, `profile`, `text`, `links`. Unknown names,
duplicates **within one list**, malformed settings and invalid counts diagnose.
Deliberately placing a component in both regions is valid; generated IDs stay unique.
Components with no data emit nothing. A region with no rendered component/hook
has **no empty grid track**. Identity/home and appearance move into a compact
header when left is absent. Standalone pages use the same full shell by default.

```toml
# Site / current native language settings. Omit left/right for contextual defaults.
[params.sidera]
menu = 'primary'
[params.sidera.identity]
subtitle = 'A place for evolving ideas'
# Optional original theme mark; or supply your own local resource.
image = 'images/sidera-mark.svg'

[[menus.primary]]
name = 'Notes'
pageRef = '/field-notes'
weight = 10
[[menus.primary]]
name = 'Contact'
url = 'mailto:hello@example.org'
weight = 20
```

## Presence, owner scope and native cascade

Each key resolves independently from:

1. Current native Page.Params.sidera, including native cascade.
2. Nearest marked owner.Params.sidera.
3. Current-language Site.Params.sidera (native site/language configuration merge).
4. Theme page-kind default.

Arrays replace, never append. `false` and `[]` disable a region (also supported for
`blog_taxonomies`); `true` is invalid. Empty strings clear text/menu settings.
Maps replace entirely at the resolver boundary; `{}` clears a profile. Identity
is deliberately site/language-owned. Native language-config merging happens before
this resolver; it does not reconstruct the origin of native merged params.

Hugo 0.166: a page-local `sidera` table replaces the *cascaded* table. Omitted local
subkeys then fall back to owner/site/default—not to reconstructed cascade data.
Native cascade can cross nested owners unless targeted or locally overridden;
ownership is not a cascade firewall. Prefer settings on the owning root, with
page-local exceptions. Source-local `children.order` remains the separate proven
P2-W exception; the shell never reparses page source to invent inheritance.

```toml
# Collection root front matter; keep its existing native/custom fields.
[params.sidera]
left = ['menu', 'notes-tags']
right = ['recent', 'profile']
recent_count = 3
[params.sidera.profile]
title = 'Field notebook'
text = 'Small observations that can grow into useful references.'
```

This also replaces the article's default right TOC. A reading page may override
`right=['toc']`. Explicit compact standalone front matter is simply:

```toml
[params.sidera]
left = false
right = []
```

No footer-disable setting is implied: configurable footers belong to H.

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

- **Notes:** complete nearest-owner hierarchy, full deduplicated counts, current
  tag and active ancestor branches. On articles all assigned branches open.
- **Docs:** existing immediate-child order helper drives the complete tree;
  ancestor/current branches open. A parent body's link and its disclosure are
  separate keyboard targets. No secondary paginator.
- **Recent:** Lastmod/Title/Path, independent of pins and current pager. Owner
  scope excludes nested independently marked collections. Docs include their
  body-bearing descendant sections as well as regular leaves. With no owner,
  recent means current-language Site.RegularPages (explicitly global).
- **TOC:** native headings, only with the rendered article/docs body; no TOC on
  later docs child pagers whose body is intentionally omitted. Full standalone
  support. A right disclosure moves in flow above main content on narrow screens.
- **Blog taxonomy navigation:** links only to actual native taxonomy Pages;
  ordinary site menus can also point to actual native terms. F does not install
  G's taxonomy index/result templates, assignments validation, counts or pagers.
  Enabling taxonomies now requires site-owned templates; do not mistake navigation
  support for completion of blog-taxonomy browsing. The showcase remains default-off.

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
