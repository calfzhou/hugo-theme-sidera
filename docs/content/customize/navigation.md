---
title: "Menus, regions and footers"
params:
  ai_label: generated
---

## Native menus

```toml
[[menus.primary]]
name = 'Notes'
pageRef = '/notes'
weight = 10
[menus.primary.params]
icon = 'notebook'
color = '#ffbd2b'
```

Use `pageRef` for real internal Pages and current/ancestor highlighting. A literal
URL is not a Page association. Native weights, identifiers and parent entries make
up to two menu levels; a destinationless parent is a heading, a destinationless
leaf is an error. Labels are authored content, not automatically translated keys.
`params.color` is an optional hex hover/current accent, not arbitrary CSS. Empty
`icon` hides decoration. External HTTP(S) opens a new tab with noopener/noreferrer;
use explicit HTTPS, not protocol-relative URLs. No config HTML or arbitrary callbacks.

Optional flat social menu (up to six entries):

```toml
[[menus.social]]
name = 'Email'
url = 'mailto:hello@example.org'
[menus.social.params]
icon = 'email'
[[menus.social]]
name = 'Color mode'
[menus.social.params]
icon = 'color-mode'
onclick = 'Sidera.cycleColorMode()'
```

Only that exact action is accepted; do not combine it with a destination. No-JS
hides the inert action but retains ordinary links. The default left footer selects
this menu when present. Site-owned social brand geometry can use the same icon
registry; image-valued icon arguments are not supported.

## Components, widgets and instances

A component is a built-in renderer. A widget is a site/language-owned configuration
of one component. An instance is one placement. All regions accept names or
`component/config` and `widget/config` objects; repeats are independent.

```toml
[params.widgets.welcome]
component = 'text'
[params.widgets.welcome.config]
title = 'Welcome'
text = 'You are reading **{site.title}**.'
```

```yaml
params:
  left:
    - menu
    - welcome
    - widget: recent-updates
      config: {count: 5, scope: global}
  right: [toc]
  article_footer: [terms, references, outgoing, backlinks, license, share, series]
  site_footer: [links, text, credit]
```

Regions are `top`, `left`, `right`, `left_footer`, `article_footer`, `site_footer`.
An empty array or false disables a region and its extra hook; empty/inapplicable
components leave no blank boxes. Region arrays replace rather than append through
inheritance. Use native cascade for descendant choices; ordinary section params
only style the section. Presets can outrank site fallback choices.

Per-use config overlays supported keys only; maps replace shallowly, explicit empty
values clear, and `{}` means defaults rather than disable. Widgets cannot shadow
built-in names or derive from widgets. Unknown/unused malformed definitions fail.
See the single [component option table](../publishing/parameters.md#component-options)
for allowed regions/options instead of guessing a renderer's internal fields.

## Footer choices

The default article footer includes terms, authored references, outgoing links,
backlinks, license, share, series and optional text/links. Missing data disappears.
The neutral default content notice says “All rights reserved unless otherwise
stated”; **choose your content license yourself**. Sidera's MIT software license
does not change that notice or license your articles.

```yaml
params:
  license: false
  share: [link, email]
  article_text: 'Thanks for reading **{page.title}**.'
  site_footer: [links, text]
  footer_menu: footer
  footer_text: 'An independently maintained notebook.'
```

Site footer `links` uses a native two-level sitemap menu; `credit` uses the native
`built_with` translation. `authors` is an explicit optional article-footer component
for portraits and an authored `edit_url`; header names remain the default attribution.
`show_authors: false` also hides this edit section. `article_end_text` is independent
final Markdown after navigation/children/comments, not footer `article_text`.

Share targets are link (copy with manual fallback), wechat (local build-time QR),
weibo (explicit outbound share link) and email (mailto). No remote QR service or
background Weibo request. Comments have their own placement, not a footer component.

## Native overrides

Use site `layouts/_partials/sidera/head-extra.html`, `top-extra.html`,
`left-extra.html`, `right-extra.html`, `article-footer-extra.html` or
`site-footer-extra.html` for small additions. Context supplies `Page`, `Owner`,
`Region` and resolved `Settings`. Fixed component overrides under
`layouts/_partials/sidera/components/` additionally receive `Config`, `Widget`,
`Instance`, `IDScope` and `IDSuffix`; use them for unique IDs in repeated instances.
Trusted templates own escaping and lifecycle. Routine menu/widget edits need no
whole-layout copies or arbitrary template paths in configuration.
