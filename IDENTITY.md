# Sidera identity assets

The approved **Parallax B** mark is optional artwork, not a forced consuming-site
identity. It has fixed, opaque slate `#73868c` and bronze `#9a805f` fills on a
transparent background. No adaptive colors, scripts, fonts or remote resources.

| Native asset | Intended use |
|---|---|
| `images/sidera-parallax-circle.svg` | Primary circle-safe avatar; 44px showcase identity |
| `images/sidera-parallax-square.svg` | Same approved paths at 1.16×; square/browser presentation |
| `images/sidera-parallax-32.png` | Transparent 32px favicon fallback rendered from square SVG |

SVG is authoritative. Circle SHA-256:
`ebe20ad690732ea31d77b7a7de72308f305b5927ca2c87fb07b7a007a9b85a68`;
square SHA-256:
`f21dc7afd04c9f4d4873ac39ee03e77d6affc093780d669177636b36e215ec7c`.
These are byte-identical deployment copies of the user-selected 2026-09-30 fixed-color
P3-L outputs (D-119/120); the original design folder is not a build/test dependency.
Eureka directly authored the geometry; no third-party logo, traced raster, font
outline or icon-library shape was used. No license grant or trademark clearance is
asserted. The earlier `images/sidera-mark.svg` remains a historical test asset;
normal showcase identity/covers no longer use it. Nothing is deleted automatically.

## Native site ownership

The theme keeps **no default identity image and no default favicon**. Site/language
`params.identity.image` still selects a safe local asset; empty string removes it.
Native site assets can shadow theme resources at the same virtual path. Identity
links use native Home.RelPermalink, independently of the image choice. `params.icon`
and menu icon/image settings are separate and unchanged.

```toml
[params.identity]
image = 'images/sidera-parallax-circle.svg'
```

Favicon policy belongs to the consuming site's existing
`layouts/_partials/sidera/head-extra.html` hook. Fieldbook opts into just two files:

```go-html-template
{{ $png := resources.Get "images/sidera-parallax-32.png" }}
{{ $svg := resources.Get "images/sidera-parallax-square.svg" }}
<link rel="icon" type="image/png" sizes="32x32" href="{{ $png.RelPermalink }}">
<link rel="icon" type="image/svg+xml" sizes="any" href="{{ $svg.RelPermalink }}">
```

Use your own resources/static favicon and head hook instead, without changing the
reusable theme. Native resource URLs retain baseURL subpaths; shared image files do
not need artificial per-language copies. No manifest, touch-icon set, monochrome
mask icon or optical micro-logo is claimed. Site-supplied GoCalf identity is not
replaced by installing this theme. A consuming site controls avatar and favicon
independently; choosing an avatar does not silently replace its favicon.

PNG reproduction (optional developer tool, not a Hugo build prerequisite), using
installed librsvg **2.62.2**:

```sh
rsvg-convert -w 32 -h 32 assets/images/sidera-parallax-square.svg \
  -o assets/images/sidera-parallax-32.png
```

At 16px the two masses remain recognizable but fine tips soften. At 24–44px more
negative space survives. Similar midtone backgrounds (e.g. `#808080`, about
1.04–1.06:1 solid-fill contrast) are unsuitable. These accepted limits are not fixed
by recoloring or alternate geometry. Local Chromium resource/mask/size checks are
not OS/browser-tab-cache or all-engine favicon certification.
