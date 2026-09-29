# Third-party notices

Component CSS in assets/css/sidera.css adapts layout, palette, banner, identity and component rules from
hexo-theme-stellar 1.44.0 (1f4cb4bc): collection, list, sidebar, widgets, footers, pagination and toast. Site notification motion also follows
Stellar main.js hud.toast/theme.js; article-date reveal follows navbar/dateinfo.ejs and bread-nav.styl; Sidera uses plain-text messages instead of upstream innerHTML.
Pinned collection tabs also adapt navbar.styl and the bar-glass/newblur mixins in _defines/func.styl; geometry tracking follows main.js navbarPin.
Reading navigation follows the read-next block in partial/related.styl.
Article pills also follow article-tags.styl and the tag-chip mixin in _defines/func.styl.
Ordinary Markdown styles also adapt _components/md.styl, pages/article-tech.styl and
_common/base.styl, title.styl, blockquote.styl, pre.styl and highlight.styl.
In-article scrollbar styling also adapts scrollbar-codeblock in _defines/func.styl, with
keyboard/touch visibility and a native forced-colors fallback.
Code-toolbar presentation also follows _plugins/copycode.styl; temporary copy feedback follows
source/js/plugins/copycode.js, with native buttons, localized failure text and manual-copy fallback. Native
Goldmark/Chroma structure replaces Hexo markup; readable palette tokens and keyboard
scrollbars are retained rather than copying hidden scrollbars or low-contrast colors.
Sidera uses native Hugo templates/JavaScript, not the Hexo or Stylus runtime.
This notice applies to those adaptations; it does not grant a distribution license
for the rest of Sidera or site content. No third-party fonts are bundled. The small local icon subset below has a separate license.

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


## Solar icons — 480 Design (CC BY 4.0)

The fixed SVG bodies in `layouts/_partials/sidera/icon.html` are by **480 Design**,
from [Solar Icon Set](https://github.com/480-Design/Solar-Icon-Set), also published
in the [author's Figma file](https://www.figma.com/community/file/1166831539721848736).
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
([legal code](https://creativecommons.org/licenses/by/4.0/legalcode)).
No endorsement by the original author is implied.

Local source/version: Stellar **1.44.0, commit 1f4cb4bc**, `_data/icons.yml`.
Retained keys: default:documents, default:category, example:notebook,
default:hashtag, example:planet, default:pin, default:calendar, default:theme, default:upup, default:tocomment, default:arrow-left, default:arrow-right, default:edit.
Sidera changes only SVG root sizing/class/accessibility attributes and semantic
names; paths and duotone opacity are unchanged. The home/link and email/QR/broadcast action icons remain
original Sidera artwork; share actions do not reuse unverified vendor logos. No arbitrary authored SVG is interpreted as an icon.

The local registry's Solar attribution is corroborated by Iconify's Solar collection
metadata (`https://raw.githubusercontent.com/iconify/icon-sets/master/json/solar.json`,
checked 2026-09-24): author 480 Design; license CC-BY-4.0; 24px grid. This lookup
verifies provenance, not an unpinned runtime dependency: the distributed paths are
pinned to the Stellar commit above. No icon package, CDN, font or framework is required.
Source permission is not an overall Sidera distribution-license grant.

## Stellar drawer artwork

`default:leftbar` and `default:rightbar` are the paired custom UI icons from the same
Stellar commit, covered by its MIT notice above. The separator ID becomes a class
to avoid duplicate IDs; root attributes supply decorative accessible semantics.

## React Bits

The card hover spotlight in Sidera CSS/navigation.js adapts Stellar’s card-hover
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
copied file's SHA-256. The focused B test verifies those hashes and CSS font paths.

Hugo embeds the build-time KaTeX renderer; these assets only style its HTML+MathML
output. Publish them conditionally with matching native resources, including LICENSE;
no CDN, client renderer, remotely fetched font, or runtime Node dependency is needed.
A later Hugo/KaTeX upgrade must review the renderer/assets together, not silently
mix versions. This upstream permission is not a Sidera distribution-license grant.

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

## Used content components (C2)

The content primitive CSS also adapts Stellar 1.44.0
`source/css/_components/tag-plugins/{inline-labels,mark,quot,link,copy,folding,grid,note}.styl`,
covered by the xaoxuu MIT notice above. Native shortcodes, typed arguments and the
existing Sidera Clipboard handler replace Hexo tags/browser onclick strings.
Quote ornaments are typographic characters, not copied icon paths. No new third-party
sticker/font/icon package was added. The emoji shortcode and blobcat requirement
were subsequently retired by user choice; no third-party sticker was distributed.

## P3-D local diagram runtimes

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
These preserve upstream obligations, not a Sidera distribution license grant or a
complete legal certification of every upstream bundled dependency.

Both vendored bundles remain byte-identical; Sidera's controller/setup/sandbox code
is separate. No CDNs or fonts load for diagrams. Actual diagram pages publish the
relevant original licenses as native resources. The opaque sandbox intentionally
blocks unused networking/eval/editing; its output becomes an inert SVG image. See
DIAGRAMS.md for the exact feature, security, source-only fallback and CSP boundaries.

### P3-E search presentation and journey

The inline sidebar search layout, widget replacement while searching, title-above-link
result structure, section/excerpt treatment, keyword accents and `?kw=`/heading journey
are adapted from the read-only Stellar **1.44.0** reference: `layout/_partial/sidebar/search.ejs`,
`source/css/_components/sidebar/{search,sidebar}.styl`, and `source/js/search/{local-search,highlight,shortcut}.js`.
The existing Stellar MIT license above applies to these adaptations (copyright 2021 xaoxuu).
Sidera's native eligibility/graph generation, shared text model and bounded literal DOM
matching are separately implemented, without copying query-as-HTML or raw-source filters.
The tiny search magnifier is original SVG geometry, not an additional upstream asset.
No search dependency, remote backend, CDN or distribution-license decision is introduced.

Search's animated rainbow also follows Stellar 1.44.0 `_config.yml`'s
`style.gradient.searchbar` and `search.styl`'s 20-second background-position motion;
Sidera adds inactive pause and reduced-motion handling under the same retained MIT notice.
