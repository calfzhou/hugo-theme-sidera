# Third-party notices

Original Sidera code, documentation and Parallax artwork are licensed under the
MIT license in LICENSE, copyright (c) 2026 Calf. The following third-party material
retains its own terms and attribution. A consuming site owns its content license.


Component CSS in assets/css/sidera.css adapts layout, palette, banner, identity and component rules from
[hexo-theme-stellar 1.44.0][stellar-144] (1f4cb4bc): collection, list, sidebar, widgets, footers, pagination and toast. Site notification motion also follows
[Stellar][stellar] main.js hud.toast/theme.js; article-date reveal follows navbar/dateinfo.ejs and bread-nav.styl; Sidera uses plain-text messages instead of upstream innerHTML.
Pinned collection tabs also adapt navbar.styl and the bar-glass/newblur mixins in _defines/func.styl; geometry tracking follows main.js navbarPin.
Reading navigation follows the read-next block in partial/related.styl.
Article pills also follow article-tags.styl and the tag-chip mixin in _defines/func.styl.
Opt-in story typography also adapts pages/article-story.styl, article-indent.styl and
_common/title.styl. H3 decorations reuse the already-attributed Solar double-arrow
geometry below as inline registry SVGs; quotation decorations use font punctuation, not a new icon.
AI label wording/presentation follows languages/en.yml, zh-CN.yml and bread-nav.styl,
with its exact configured label colors and the four Solar shields credited below;
no provider framework.
Ordinary Markdown styles also adapt _components/md.styl, pages/article-tech.styl and
_common/base.styl, title.styl, blockquote.styl, pre.styl and highlight.styl.
In-article scrollbar styling also adapts scrollbar-codeblock in _defines/func.styl, with
keyboard/touch visibility and a native forced-colors fallback.
Code-toolbar presentation also follows _plugins/copycode.styl; temporary copy feedback follows
source/js/plugins/copycode.js, with native buttons, localized failure text and manual-copy fallback. Native
Goldmark/Chroma structure replaces Hexo markup; readable palette tokens and keyboard
scrollbars are retained rather than copying hidden scrollbars or low-contrast colors.
Sidera uses native Hugo templates/JavaScript, not the Hexo or Stylus runtime.
This upstream notice applies to those adaptations; original Sidera material is
covered separately by LICENSE, and site content retains its own rights. No reading/UI fonts are bundled; matched KaTeX math fonts are documented below. The small local icon subset below has a separate license.

MIT License

Copyright (c) 2021 xaoxuu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Solar icons — 480 Design and maintained extensions (CC BY 4.0)

The **45 Solar inline SVG entries** in `data/sidera/icons.yaml` use Solar Icons.
Original artwork: **480 Design**, [Solar Icon Set](https://github.com/480-Design/Solar-Icon-Set),
[original Figma set](https://www.figma.com/community/file/1166831539721848736).
License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
([legal code](https://creativecommons.org/licenses/by/4.0/legalcode)). No endorsement implied.

New selections are pinned to the maintained distribution
[saoudi-h/solar-icons](https://github.com/saoudi-h/solar-icons), **dcbe867a0**,
`packages/core/svgs/`. Its **panel-left, list-ordered, close, add and minus** geometry
is attributed in that repository to **Hakim Saoudi** as maintained extensions.
Those entries retain the same declared CC BY 4.0 terms; package-code MIT is not
misrepresented as the artwork license.

`data/sidera/icon_sources.yaml` maps every **Solar-derived semantic key** to the
exact Solar name/style, origin/revision/path, author/license, normalized SHA-256
and (for new selections) original source-file hash. Normalization removes intrinsic
SVG size, converts fixed source paint to currentColor, retains geometry/stroke/
duotone opacity, and adds decorative accessibility attributes only at rendering.

The shield-user/check/up/warning and story double arrows preserve their
exact geometry from [Stellar][stellar] **1.44.0 / 1f4cb4bc**, `_data/icons.yml`, rather than
silently exchanging them for a newer maintained rendition. All other built-in UI
artwork, including search, sharing, drawers and diagram operations, now uses the
registry. Site-provided replacements are the site's responsibility and cannot
claim the replaced entry's provenance automatically. See docs/content/customize/icons.md for the bounded
custom SVG format and data/sidera/icon_sources.yaml for the per-key mapping. No package, font, CDN or client
icon loader is required. Original Sidera material is covered separately by LICENSE.

### Historical [Stellar][stellar] drawer attribution retained

The earlier default:leftbar/default:rightbar custom artwork was adapted under
[Stellar][stellar]'s MIT notice above. It is superseded at runtime by Solar panel/list icons;
the historical credit is retained, not a claim that these custom paths still ship.
Earlier handmade home/link/share/search and diagram SVGs are likewise no longer
runtime UI artwork. Reference/history files are not removed by this integration.

## Font Awesome Free brand icons — Fonticons, Inc. (CC BY 4.0)

The **14 brand SVG entries** in `data/sidera/icons.yaml` come from
[Font Awesome Free 7.3.1](https://github.com/FortAwesome/Font-Awesome/tree/14c65a3747d0f3b751f15831fc719236aea8729d/svgs/brands),
revision **14c65a3747d0f3b751f15831fc719236aea8729d**: github, facebook,
linkedin, slack, instagram, tiktok, wordpress, whatsapp, telegram, skype,
bilibili, x-twitter, weixin and weibo.

Copyright 2026 Fonticons, Inc. (https://fontawesome.com).
Icons: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
([legal code](https://creativecommons.org/licenses/by/4.0/legalcode)).
The font/code licenses below do not replace the SVG artwork license; no Font Awesome
font, CSS, JavaScript or runtime loader is bundled.

Normalization retains path data unchanged, fits and centers the source viewBox in
Sidera's 24 × 24 coordinate system with a uniform geometry transform, and uses
currentColor with no intrinsic size. These brand keys have no style variants.
Per-icon original attribution comments are retained verbatim as `attribution`
values in `data/sidera/icon_sources.yaml`, alongside source name/path/revision,
author/license, original viewBox and source/normalized SHA-256 hashes. Comments
are not part of the validated geometry strings. Attribution is also published
through this notice on generated pages.

Brand icons are trademarks of their respective owners; use them only to represent
the corresponding company, product or service. No endorsement or trademark
clearance is implied. The upstream `LICENSE.txt` is reproduced verbatim below:

```text
Fonticons, Inc. (https://fontawesome.com)

--------------------------------------------------------------------------------

Font Awesome Free License

Font Awesome Free is free, open source, and GPL friendly. You can use it for
commercial projects, open source projects, or really almost whatever you want.
Full Font Awesome Free license: https://fontawesome.com/license/free.

--------------------------------------------------------------------------------

# Icons: CC BY 4.0 License (https://creativecommons.org/licenses/by/4.0/)

The Font Awesome Free download is licensed under a Creative Commons
Attribution 4.0 International License and applies to all icons packaged
as SVG and JS file types.

--------------------------------------------------------------------------------

# Fonts: SIL OFL 1.1 License

In the Font Awesome Free download, the SIL OFL license applies to all icons
packaged as web and desktop font files.

Copyright (c) 2026 Fonticons, Inc. (https://fontawesome.com)
with Reserved Font Name: "Font Awesome".

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL

SIL OPEN FONT LICENSE
Version 1.1 - 26 February 2007

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting — in part or in whole — any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.

--------------------------------------------------------------------------------

# Code: MIT License (https://opensource.org/licenses/MIT)

In the Font Awesome Free download, the MIT license applies to all non-font and
non-icon files.

Copyright 2026 Fonticons, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

--------------------------------------------------------------------------------

# Attribution

Attribution is required by MIT, SIL OFL, and CC BY licenses. Downloaded Font
Awesome Free files already contain embedded comments with sufficient
attribution, so you shouldn't need to do anything additional when using these
files normally.

We've kept attribution comments terse, so we ask that you do not actively work
to remove them from files, especially code. They're a great way for folks to
learn about Font Awesome.

--------------------------------------------------------------------------------

# Brand Icons

All brand icons are trademarks of their respective owners. The use of these
trademarks does not indicate endorsement of the trademark holder by Font
Awesome, nor vice versa. **Please do not use brand logos for any purpose except
to represent the company, product, or service to which they refer.**
```

## React Bits

The card hover spotlight in Sidera CSS/navigation.js adapts [Stellar][stellar]’s card-hover
implementation, which in turn adapts Spotlight Card in
[React Bits](https://github.com/DavidHDev/react-bits).

MIT License

Copyright (c) 2026 David Haz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## KaTeX 0.18.4 — matching Hugo 0.166.0's embedded renderer

`assets/vendor/katex-0.18.4/` contains the **unmodified** upstream `dist/katex.min.css`,
60 font files (WOFF2/WOFF/TTF) and MIT LICENSE. No upstream JavaScript is bundled.
Source: https://registry.npmjs.org/katex/-/katex-0.18.4.tgz (KaTeX npm package).
Retrieved using `npm pack katex@0.18.4 --ignore-scripts`; no install or lifecycle
script. `provenance.json` records npm SHA-512 integrity, archive SHA-256 and every
copied file's SHA-256. The asset checks verify those hashes and CSS font paths.

Hugo embeds the build-time KaTeX renderer; these assets only style its HTML+MathML
output. Publish them conditionally with matching native resources, including LICENSE;
no CDN, client renderer, remotely fetched font, or runtime Node dependency is needed.
A later Hugo/KaTeX upgrade must review the renderer/assets together, not silently
mix versions. Original Sidera licensing is specified separately in LICENSE.

The MIT License (MIT)

Copyright (c) 2013-2020 Khan Academy and other contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Used content components (container)

The content primitive CSS also adapts [Stellar 1.44.0][stellar-144]
`source/css/_components/tag-plugins/{inline-labels,mark,quot,link,copy,folding,grid,note}.styl`,
covered by the [xaoxuu][xaoxuu] MIT notice above. Native shortcodes, typed arguments and the
existing Sidera Clipboard handler replace Hexo tags/browser onclick strings.
Quote ornaments are typographic characters, not copied icon paths. No new third-party
sticker/font/icon package was added. The emoji shortcode and blobcat requirement
were subsequently retired by user choice; no third-party sticker was distributed.

## Local diagram runtimes

**Mermaid 11.17.2**: unmodified npm `dist/mermaid.min.js`, root MIT LICENSE (Knut
Sveidqvist) and upstream bundled notices. Release `mermaid@11.17.2`, `dcb694d`;
https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4011.17.2 . The npm archive's
SHA-512 integrity is verified before extraction; archive/per-file hashes and origin
are in `assets/vendor/mermaid-11.17.2/provenance.json`. The selected 11.x includes the
previously reviewed 11.16.1 CSS/config security fixes and 11.17.2's edge-path fix;
this is not a blind latest-major upgrade or a guarantee against future advisories.

**drawio viewer 31.5.2**: unmodified tagged `src/main/webapp/js/viewer-static.min.js`,
`stencils/basic.xml` and root Apache-2.0 LICENSE, JGraph. Release `v31.5.2`, `0037930`;
https://github.com/jgraph/drawio/releases/tag/v31.5.2 . File hashes and exact upstream
paths are in `assets/vendor/drawio-31.5.2/provenance.json`. Basic stencils are kept as
upstream XML; no arbitrary remote package is fetched. No editor/backend is installed.

Original embedded notices remain intact, including DOMPurify (Apache-2.0/MPL-2.0),
pako (MIT/Zlib), Lodash and Cytoscape-related MIT notices. Additional full licenses
for the explicitly identified bundled DOMPurify versions 3.4.12/3.4.15, pako 2.2.0
and lodash-es 4.18.1 were extracted from their exact npm packages (ignore-scripts,
no installation); source/archive integrity is recorded alongside each copied file.
These preserve upstream obligations independently of Sidera’s LICENSE; they are not
a complete legal certification of every upstream bundled dependency.

Both vendored bundles remain byte-identical; Sidera's controller/setup/sandbox code
is separate. No CDNs or fonts load for diagrams. Actual diagram pages publish the
relevant original licenses as native resources. The opaque sandbox intentionally
blocks unused networking/eval/editing; its output becomes an inert SVG image. See
docs/content/authoring/diagrams.md for the exact feature, security, source-only fallback and CSP boundaries.

## Local interactive chart runtime

**Apache ECharts 6.1.0**: unmodified npm `dist/echarts.common.min.js` (line, bar,
pie and scatter, with SVG/Canvas renderers and common components). Source:
https://registry.npmjs.org/echarts/-/echarts-6.1.0.tgz . Retrieved with
`npm pack echarts@6.1.0 --ignore-scripts`; no installation or lifecycle scripts.
The package's Apache-2.0 LICENSE, NOTICE and BSD-3-Clause `licenses/LICENSE-d3`
are retained verbatim in `assets/vendor/echarts-6.1.0/`. ECharts' NOTICE states:

Apache ECharts
Copyright 2017-2026 The Apache Software Foundation

This product includes software developed at
The Apache Software Foundation (https://www.apache.org/).

The bundled dependencies **zrender 6.1.0** (BSD-3-Clause) and **tslib 2.3.0**
(0BSD) retain their exact npm LICENSE and, for tslib, CopyrightNotice files.
`provenance.json` records every source archive, npm SHA-512 integrity, archive
SHA-256, copied member and file SHA-256. The resource pipeline verifies all copied
hashes and publishes these notices with the conditional chart assets. The common
bundle remains byte-identical; Sidera's original integration is separate and uses
SVG rendering in live opaque sandboxes, not remote services or injected host HTML.
See docs/content/authoring/charts.md for supported input and runtime restrictions.
Original Sidera material remains MIT licensed; these components retain their terms.

### Search presentation and journey

The inline sidebar search layout, widget replacement while searching, title-above-link
result structure, section/excerpt treatment, keyword accents and `?kw=`/heading journey
are adapted from the read-only [Stellar][stellar] **1.44.0** reference: `layout/_partial/sidebar/search.ejs`,
`source/css/_components/sidebar/{search,sidebar}.styl`, and `source/js/search/{local-search,highlight,shortcut}.js`.
The existing [Stellar][stellar] MIT license above applies to these adaptations (copyright 2021 [xaoxuu][xaoxuu]).
Sidera's native eligibility/graph generation, shared text model and bounded literal DOM
matching are separately implemented, without copying query-as-HTML or raw-source filters.
The search magnifier and result/external/close glyphs now use the Solar registry
credited above; original Sidera logo derivatives are attributed separately below.
No search dependency, remote backend or CDN is introduced.

Search's animated rainbow also follows [Stellar 1.44.0][stellar-144] `_config.yml`'s
`style.gradient.searchbar` and `search.styl`'s 20-second background-position motion;
Sidera adds inactive pause and reduced-motion handling under the same retained MIT notice.

## Original Parallax artwork

`assets/images/sidera-parallax-circle.svg` and `sidera-parallax-square.svg` are
byte-identical copies of Eureka's directly authored fixed-color Parallax B,
selected by the user on 2026-09-30. The 32px
PNG is a direct librsvg rendition of the square SVG. There is no third-party logo,
font outline, raster trace or external icon provenance for this mark. See docs/content/customize/_index.md
for native usage and visual limits; original icon records retain source hashes.
Original Parallax artwork is covered by Sidera’s MIT LICENSE. No trademark clearance
is asserted. The four sidera-bold, sidera-bold-duotone, sidera-linear and
sidera-line-duotone entries are original derivatives of this mark in Solar-like
styles, not upstream Solar icons. Eureka authored the geometry; copyright 2026 Calf.
Their per-key records use original-design provenance, not fabricated Solar paths.

## Notice delivery

This document is also copied verbatim to `assets/licenses/sidera-third-party.txt`,
which the shared head publishes as a native local resource linked with `rel=license`.
The native manual validator checks equality so the rendered-site notice cannot silently
drift. This preserves the existing third-party terms in static output even when
Hugo minification removes CSS comments; it does not replace LICENSE or license site content.
Keep both copies synchronized when updating notices. Vendor-specific license files
continue to publish with their conditional math/diagram resources.

## In-article timeline

Timeline line/marker/header/card styling adapts [Stellar 1.44.0][stellar-144] (1f4cb4bc),
source/css/_components/tag-plugins/timeline.styl, copyright 2021 [xaoxuu][xaoxuu],
under the MIT notice retained above. Native timeline/event composition is
implemented by Sidera; no sidebar timeline, API service or JS widget is copied.

[stellar]: https://xaoxuu.com/wiki/stellar/
[stellar-144]: https://github.com/xaoxuu/hexo-theme-stellar/tree/1.44.0
[xaoxuu]: https://xaoxuu.com/

## Optional JSX islands

The explicit `jsx-live` fence and `jsx` shortcode compile trusted author components
with Hugo's native esbuild pipeline. Conditional local assets contain unmodified
production source from React 19.3.0, React DOM 19.3.0 and Scheduler 0.28.0,
from their exact npm distributions. Copyright (c) Meta Platforms, Inc. and affiliates.
All three are MIT licensed. See `assets/vendor/react-19.3.0/provenance.json` for
package integrity and per-file SHA-256; their verbatim licenses live alongside
the sources and are published when JSX is used. Sidera's mounting, fallback and
theme integration code is original MIT-licensed work.

MIT License

Copyright (c) Meta Platforms, Inc. and affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
