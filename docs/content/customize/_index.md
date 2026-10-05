---
title: "Customize your site"
params:
  ai_label: generated
  children:
    order: [navigation, icons]
---

Start with native configuration and data. Use small site partial/asset overrides only
when the supported settings cannot express your choice; do not copy the whole theme.
[Menus and regions](navigation.md) select content; [named icons](icons.md) select UI
artwork. The [parameter reference](../publishing/parameters.md) owns the defaults.

## Identity and appearance

```toml
[params]
color_mode = 'auto'
page_reveal = false
[params.identity]
title = 'My notebook'
subtitle = 'Ideas worth keeping | A little more every day'
image = 'images/sidera-parallax-circle.svg'
```

Identity title falls back to the native site title. The first pipe separates the
resting/hover subtitle; labels remain plain escaped text. Identity image is empty
by default. It is distinct from collection `params.logo`, an author's `avatar`,
a list card's `cover` and an inline menu icon. Safe local images resolve from
native resources/assets/static; identity never downloads an image at build time.

Color mode is auto/light/dark; a saved visitor choice wins. Auto follows the OS.
The optional social-menu action cycles dark → light → auto. With no JavaScript,
CSS follows the owner default/OS and ordinary navigation stays usable. Default-on
page-entry motion respects reduced motion, focus, history and hash navigation;
site/language `page_reveal: false` omits it.

### Original Parallax brand images

The optional assets are `images/sidera-parallax-circle.svg`,
`images/sidera-parallax-square.svg` and `images/sidera-parallax-32.png`. Circle and
square use fixed slate `#73868c` and bronze `#9a805f`, not currentColor. Native site
assets can override the same virtual paths. Fine tips soften at 16px; similar
midtone backgrounds are unsuitable. These are not all-engine favicon guarantees.

Favicons are site policy. In `layouts/_partials/sidera/head-extra.html`:

```go-html-template
{{ with resources.Get "images/sidera-parallax-square.svg" }}
<link rel="icon" type="image/svg+xml" sizes="any" href="{{ .RelPermalink }}">
{{ end }}
{{ with resources.Get "images/sidera-parallax-32.png" }}
<link rel="icon" type="image/png" sizes="32x32" href="{{ .RelPermalink }}">
{{ end }}
```

### Fonts and CSS

Use the same head hook to load a site-owned CSS resource **after** theme CSS.
Override `--ui`, `--reading`, `--inline-code` and `--code` separately when needed.
The baseline UI/prose stack starts with LXGW WenKai and falls back through system
fonts; fenced code starts with Source Code Pro and monospace alternatives. Naming
those fonts does not download them. Loading or licensing additional fonts is the
site's choice. Bundled conditional KaTeX math fonts are separate. Giscus matches
the baseline stack, not arbitrary site CSS overrides automatically.

## English and Chinese UI

For Chinese controls around unsuffixed content:

```toml
defaultContentLanguage = 'zh'
locale = 'zh-CN'
```

For shared-directory filename translations:

```toml
defaultContentLanguage = 'en'
defaultContentLanguageInSubdir = true
[languages.en]
locale = 'en-US'
weight = 1
[languages.zh]
locale = 'zh-CN'
weight = 2
```

Author `_index.zh.md` / `index.zh.md` for real Chinese counterparts, including their
own root policies/cascades. Unsuffixed pages belong to the default language; no
body is auto-translated and no links to absent translations are invented.

Override only desired messages in site `i18n/en.toml` or `i18n/zh-CN.toml`:

```toml
[built_with]
other = 'Built with [Hugo](https://gohugo.io/) · **Sidera**'
```

`built_with` and the neutral content `license_default` are Markdown; other catalogs
are plain escaped text. Hugo falls back to the configured default language, not
always English. Use strict builds with `--printI18nWarnings` to catch missing keys.
