---
title: "Named icons and logo styles"
params:
  ai_label: generated
---

UI icons are small inline SVGs, not fetched image files, icon fonts or a client
framework. Select a semantic key in native menu `params.icon`, section `params.icon`,
`tag_icons`, social entries or the `link` shortcode. Parent color/size controls them.
Identity artwork, collection logos, avatars, content images and QR data remain separate.

## Four Sidera Parallax derivatives

| Key | Style |
|---|---|
| `sidera-bold` | Solid paired crescents |
| `sidera-bold-duotone` | Solid with one crescent at 40% opacity |
| `sidera-linear` | Outlined paired crescents |
| `sidera-line-duotone` | Outlined with one crescent at 40% opacity |

These are **original Sidera derivatives in Solar-like styles**, not upstream Solar
icons. They preserve the opposed crescents/negative-space identity without changing
the fixed-color circle/square brand assets. Use Bold Duotone for a normal menu:

```toml
[[menus.primary]]
name = 'Manual'
pageRef = '/manual'
[menus.primary.params]
icon = 'sidera-bold-duotone'
```

This page's comparison links below render the actual four named registry entries.

## Built-ins and site overrides

Common keys include `home`, `about`, `blog`, `notebook`, `docs`, `page`, `tag`,
`category`, `authors`, `series`, `star`, `planet`, `link`, `code`, `email`,
`color-mode`, `search` and `download`. The authoritative full registry/provenance
lives in repository `data/sidera/icons.yaml` and `icon_sources.yaml`, including
Solar source names/styles/licenses. Unknown nonempty keys diagnose; `''` means none.

Add or replace **one whole entry** in site `data/icons.yaml`:

```yaml
# Site-owned example geometry, not a Solar source claim.
custom-example: |
  <svg viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.5"/>
  </svg>
```

All other built-ins remain. Site replacements do not inherit the replaced artwork's
provenance: retain your own author/source/license record and use authorized artwork.
Definitions validate even if unused or icons are off.

Only one balanced `svg`, `viewBox="0 0 24 24"`, and bounded geometry are accepted:
`g`, `path`, `circle`, `ellipse`, `rect`, `line`, `polyline`, `polygon`. Attributes
must be double-quoted, paint currentColor/none, with numeric geometry, opacity,
strokes, transforms, fill rules and cap/join settings. No intrinsic root size,
style/color, IDs/classes, text/title, defs/masks, links/use/images, events, scripts,
foreignObject, entities, external resources or bitmaps. Maximum 50,000 characters.
This is trusted maintainer data with format guards, not an untrusted SVG importer.

## Color, size and accessibility

The renderer adds `.icon`, `aria-hidden="true"` and `focusable="false"`.
Parents provide accessible text and hit areas. With no override, SVG is 1em and
inherits color; a trusted site stylesheet may set `--icon-size` or `--icon-color`
on the containing control. Main-menu icons use the existing 1.5rem treatment.
Do not put colors/sizes into the registry to customize one menu.

`params.icons: false` hides optional UI decoration but keeps localized visible text
for icon-only actions. Empty selection removes one icon. A supported instance's
`icons: true` can intentionally override inherited false. Brand/content images and
alt text remain; nearby collection titles allow decorative logo `alt=""`.

See [credits](../publishing/credits.md) for retained Solar CC BY attribution and
original Sidera MIT terms. No trademark clearance is claimed.

{{< link href="../_index.md" text="Sidera Bold" icon="sidera-bold" >}}
{{< link href="../_index.md" text="Sidera Bold Duotone" icon="sidera-bold-duotone" >}}
{{< link href="../_index.md" text="Sidera Linear" icon="sidera-linear" >}}
{{< link href="../_index.md" text="Sidera Line Duotone" icon="sidera-line-duotone" >}}
