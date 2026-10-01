# Named inline icons

Sidera's UI uses a curated **Solar** selection, rendered inline by Hugo. No icon
font, package install, client loader, CDN, sprite fetch or per-icon SVG/image files.
Native image/identity/favicon/content/QR APIs are separate and remain unchanged.

## Names belong to Sidera; source names remain traceable

- `data/sidera/icons.yaml`: **44 Sidera keys → complete SVG strings**.
- `data/sidera/icon_sources.yaml`: the corresponding **Solar name, style, source
  repository/revision/path, author/license and normalized SHA-256** for each key.
  New imports also record their original source-file hash. This is provenance, not
  a second renderer or an API users must configure.
- Most source geometry is from `saoudi-h/solar-icons` at **dcbe867a0**. Original
  icons are by 480 Design; that distribution's panel-left/list-ordered/close/add/
  minus extensions credit **Hakim Saoudi**. All retain Solar CC BY 4.0 attribution.
- Four AI shields and two story ornaments preserve the **exact accepted** geometry/
  opacity from Stellar **1.44.0 / 1f4cb4bc**, `_data/icons.yml`. They are already
  Solar; no silent upgrade/recolor. Per-key provenance distinguishes those pins.

The tables below use Solar's canonical source names, not a public Solar dependency.
BD = Bold Duotone; L = Linear. Call sites use only the **Sidera key**.

| Sidera key | Solar name | Style |
|---|---|---|
| home | home | BD |
| about | user-circle | BD |
| blog | pen-new-square | BD |
| notebook | notebook | BD |
| docs | book-bookmark | BD |
| page | document-text | BD |
| category | folder | BD |
| tag | hashtag | BD |
| authors | users-group-rounded | BD |
| series | bookmark | BD |
| preset | widget | BD |
| star | star | BD |
| planet | planet | BD |
| link | link | BD |
| pin | pin | L |
| calendar | calendar | L |
| color-mode | moon-stars | L |
| sidebar-left | panel-left | L |
| sidebar-right | list-ordered | L |
| comments | chat-square-line | L |
| up | square-double-alt-arrow-up | L |
| arrow-left | alt-arrow-left | L |
| arrow-right | alt-arrow-right | L |
| link-action | link | L |
| email | letter | L |
| qr | qr-code | L |
| broadcast | share | L |
| edit | pen-new-square | L |
| search | magnifier | L |
| close | close | L |
| chevron-right | alt-arrow-right | L |
| plus | add | L |
| minus | minus | L |
| external-link | arrow-right-up | L |
| fit | minimize-square | L |
| expand | maximize | L |
| code | code | L |
| download | download | L |
| shield-user | shield-user | BD |
| shield-check | shield-check | BD |
| shield-up | shield-up | BD |
| shield-warning | shield-warning | BD |
| story-left | double-alt-arrow-left | BD |
| story-right | double-alt-arrow-right | BD |

Menu/collection identities are Bold Duotone; operations and quiet metadata are
Linear. `star` now really is a star; select `planet` for the previous concept.
About is explicit `about`, not guessed from its title or route. Native presets
supply blog/notebook/docs keys; they do not become content-kind gates.

## Add or replace an icon in the site

Create **site `data/icons.yaml`**. It is a flat map of lowercase kebab-case names
and complete normalized SVG strings. Site entries replace a built-in **by key**,
wholly; all other built-ins remain. New keys work without theme-template changes.
No deep merging SVG attributes, file-or-key guessing, aliases or dynamic styles.

For example, paste a normalized Solar SVG under a site-owned name:

```yaml
# Illustration of the format, not a new bundled shape or a Solar attribution.
custom-example: |
  <svg viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.5"/>
  </svg>
```

Use actual Solar geometry for ordinary UI, or authorized brand geometry for the
agreed non-Solar exception. Keep source/name/style/license information as YAML
comments or site-owned provenance data. A site's replacement does not inherit the
original built-in's provenance claim. Fieldbook's committed `reading` key shows
Solar **book-2 / BoldDuotone** with source attribution beside its SVG.

Select built-in or site keys with the same existing settings:

```yaml
# One native menu entry
name: About
pageRef: /about
params:
  icon: about
```

```yaml
# Section front matter; ordinary params are NOT an implicit descendant cascade.
params:
  icon: notebook
  tag_icons:
    practice/notes: reading
cascade:
  params:
    tag_icons:
      practice/notes: reading
```

Native preset defaults may select a custom icon key. Supported `tag_icons` instance
maps use the same registry. Sidebar/index/card tag cues and article terms honor the
resolved mapping; global taxonomy icons distinguish categories/authors/series/preset.
Keys are case-sensitive. An explicit **empty selection** (`icon: ''`) omits the
icon; an unknown nonempty name diagnoses. A registry definition itself must contain
valid SVG, not an empty string. Validation also checks unused entries and icons-off
builds so bad definitions cannot silently become active later.

Link cards now consistently use keys:

```text
{{< link href="../article/index.md" text="Read more" icon="reading" >}}
{{< link href="../article/index.md" text="Text only" icon="" >}}
```

Omitting icon selects `link`. The same applies to native social menu `params.icon`.
**Pre-release migration:** former `link icon="file.svg"` / remote-image destinations
are no longer icon inputs. Former social `params.image` diagnoses with the replacement
instructions. Define an inline registry entry and select its key. Identity/profile/
avatar/cover images and ordinary Markdown images are not retired. Old unreferenced
showcase social files remain as historical source, not loaded runtime icons; this
change does not authorize deleting user files or converting the real site.

## Geometry, presentation and trust

SVG is **trusted maintainer-authored site data**, never raw SVG from menu/section/
tag/shortcode strings, user comments or remote input. The supported bounded format
is deliberately small; `safeHTML` alone is not a sanitizer.

- One balanced `svg` root, **viewBox="0 0 24 24"**, at most 50,000 characters.
- Allowed geometry: `g`, `path`, `circle`, `ellipse`, `rect`, `line`, `polyline`,
  `polygon`. Double-quoted geometric attributes, numeric coordinates/opacity/stroke,
  path data, transforms, fill rules and cap/join attributes are supported.
- Paint is only **currentColor / none**. Keep intrinsic duotone opacity and Solar's
  native 1.5 viewBox-unit linear stroke; do not fake styles by changing global fill.
- No root width/height, inline style/color, IDs/classes, text/title, links/use/image,
  defs/masks, event handlers, script, foreignObject, entities or embedded/external
  resources. The optional standard SVG namespace is allowed. Complex brand art must
  be normalized into this subset or remain in the separate identity-image path.
- Bad data fails the build and yields no registry markup. This is a geometry format
  guard, not an OS sandbox for untrusted site templates or a general SVG importer.

The shared `sidera/icon.html` partial adds `.icon`, aria-hidden and nonfocusable
semantics. Control parents supply native localized labels and usable hit areas.
The icon has no fixed display size/palette. Its wrapper inherits or sets:

```css
.my-control {
  color: var(--text);
  --icon-size: 1.25em;
  /* Optional icon-only accent, still owned by the surrounding element: */
  --icon-color: var(--accent);
}
```

Without these variables, SVG is **1em and inherits color**. Existing main-menu,
metadata, TOC, social and diagram contexts own their different sizes/accents.
AI label parents retain exact blue/green/orange; the icon registry does not contain
those colors. Their accepted light-contrast limitation remains, not an AA claim.

Search-result/external-link/modal symbols clone small **server-rendered template
nodes**; JS contains no second SVG catalogue or string-to-HTML icon injection.
Story H3 ornaments use the registry rather than CSS SVG data URIs. Their decorative
markup stays out of heading text/search/TOC and is visible only in story bodies.

## Icons off and deliberate exceptions

`params.icons=false` and supported per-instance overrides preserve their native
precedence. Theme-owned decorations disappear; icon-only search/diagram/pager actions
receive localized **visible text**, not blank controls. Native tree/folding summaries
retain perceivable operation text and keyboard/no-JS state behavior. Search/highlight,
source downloads, menus, current state, source links and comments remain functional.
An instance's own `icons=true` can intentionally override a page's false setting.

Heading marker characters, quotation marks, breadcrumbs, bullets/ellipses, current
dots, story slashes/halo and the hollow logo rainbow are typography/layout, not an
alternate icon set. Native media/details/checkbox controls and Giscus's own UI are
browser/provider-owned. Identity logos, avatars, content figures, rendered diagrams,
Shields images and **actual QR data** remain images, not registry icons.

All third-party notices remain in THIRD-PARTY-NOTICES.md and its published mirror.
No Sidera software/artwork license or trademark clearance is granted by this guide.
