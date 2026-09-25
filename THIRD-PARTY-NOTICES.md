# Third-party notices

Component CSS in assets/css/sidera.css adapts layout, palette, banner, identity and component rules from
hexo-theme-stellar 1.44.0 (1f4cb4bc): collection, list, sidebar, widgets, footers and toast. Site notification motion also follows
Stellar main.js hud.toast/theme.js; Sidera uses plain-text messages instead of upstream innerHTML.
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
default:hashtag, example:planet, default:pin, default:calendar, default:theme, default:upup.
Sidera changes only SVG root sizing/class/accessibility attributes and semantic
names; paths and duotone opacity are unchanged. The home/link icons remain
original Sidera artwork. No arbitrary authored SVG is interpreted as an icon.

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
