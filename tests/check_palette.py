"""Named content colors, safe native composition and one shared CSS vocabulary.
Run with a fresh absolute output path. The showcase browser check uses this fixture.
"""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
SITE = RUN / 'site'
SITE.mkdir(parents=True, exist_ok=False)
NAMES = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink', 'neutral']
ALERTS = {'note': 'blue', 'tip': 'green', 'important': 'purple', 'warning': 'yellow', 'caution': 'red'}
passed = []


def write(path, text):
    path = SITE / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def build(name, diagnostic=None, extra=()):
    out = RUN / (name + '-public')
    result = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
        '--cacheDir', str(RUN / (name + '-cache')), '--noBuildLock', '--minify',
        '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings', *extra],
        capture_output=True, text=True, timeout=60)
    log = result.stdout + result.stderr
    (RUN / (name + '.log')).write_text(log)
    if diagnostic:
        assert result.returncode and diagnostic in log and 'negative.md' in log, (name, log)
    else:
        assert not result.returncode, (name, log)
    passed.append(name)
    return out


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


write('hugo.toml', f'''baseURL='https://example.invalid/preview/'
title='Palette checks'
theme='sidera'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[params]
search=false
search_index=false
page_reveal=false
[languages.en]
weight=1
locale='en-US'
[languages.zh]
weight=2
locale='zh-CN'
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[markup.goldmark.parser.attribute]
_merge='shallow'
''')
parts = ['---\ntitle: Content palette\n---\n', '## Color families\n', '{{% grid min_width=180 id="palette-grid" %}}']
for name in NAMES:
    parts.append(f'''{{{{< cell >}}}}
{{{{< box title="{name.title()}" color="{name}" id="box-{name}" >}}}}
Body text with **emphasis** and a [local link](#color-families).

{{{{< mark text="Highlighted {name}" color="{name}" >}}}}
{{{{< /box >}}}}
{{{{< folding title="More **{name}**" color="{name}" id="fold-{name}" >}}}}
Supporting text.
{{{{< /folding >}}}}
{{{{< /cell >}}}}''')
parts += ['{{% /grid %}}', '## Alerts\n']
for alert in ALERTS:
    parts.append(f'> [!{alert}]\n> The {alert} message remains meaningful without color.\n')
parts += ['> [!tip] Custom title stays an ordinary quote.\n> Not a basic alert.\n',
    '## Defaults\n', 'A{{< mark text="<&>" >}}B\n',
    '{{% box id="default-box" %}}\nDefault neutral.\n{{% /box %}}',
    '{{% folding title="Default fold" id="default-fold" %}}\nDefault neutral.\n{{% /folding %}}',
    '## Nested families\n']
# Every outer family contains every inner family, including explicit/default neutral.
for outer in NAMES:
    parts.append(f'{{{{% box color="{outer}" id="outer-{outer}" %}}}}')
    for inner in NAMES:
        parts.append(f'''{{{{< box color="{inner}" title="{inner}" id="nested-{outer}-{inner}" >}}}}
Nested body. {{{{< mark text="{inner}" color="{inner}" >}}}}
{{{{< folding title="Inner {inner}" color="{inner}" >}}}}
Inner body.
{{{{< /folding >}}}}
{{{{< /box >}}}}''')
    parts += ['{{< box >}}\nUncolored child.\n{{< /box >}}', '{{< mark text="Default yellow" >}}\n']
    for alert in ALERTS:
        parts.append(f'> [!{alert}]\n> Nested alert.\n')
    parts.append('{{% /box %}}')
text = '\n\n'.join(parts) + '\n'
write('content/palette.md', text)
write('content/palette.zh.md', text.replace('title: Content palette', 'title: Palette — Chinese controls'))

# Trusted fixture markup exercises actual UI selectors on each existing shell surface.
write('content/ui-palette.md', """---
title: Interface palette
layout: ui-palette
---
## Interface colors

```javascript
const label = "Color families, independent roles";
```
""")
write('layouts/ui-palette.html', '''{{ define "main" }}
{{ $ui := resources.Get "css/jsx.css" | minify | fingerprint }}<link rel="stylesheet" href="{{ $ui.RelPermalink }}">
<main id="main" class="prose" style="max-width:740px;margin:2rem auto;padding:1rem">
<h1>Interface palette</h1>{{ .Content }}
{{ range slice "canvas" "surface" "panel" "surface-hover" }}
<section class="ui-plane" data-plane="{{ . }}" style="background:var(--{{ . }});padding:20px;margin:12px 0;border-radius:12px">
<h3>{{ . }}</h3>
<div style="display:flex;gap:12px;flex-wrap:wrap">{{ range slice "manual" "reviewed" "polished" "generated" }}<span class="ai-label" data-ai-label="{{ . }}">{{ T (printf "ai_label_%s" .) }}</span>{{ end }}</div>
<p><a class="ui-link" href="#interface-colors">A useful link</a> · <span class="pin-label">Pinned</span> · <span class="jsx-root"><span class="jsx-error">Error message</span></span></p>
<p><span class="search-keyword">Search keyword</span> · <mark class="search-body-mark">Matched body text</mark></p>
<p><span class="search-wrapper is-loading" style="display:inline"><span class="search-button" style="position:static;display:inline;width:auto;height:auto;transform:none">Loading</span></span> · <span class="search-wrapper search-error" style="display:inline"><span class="search-button" style="position:static;display:inline;width:auto;height:auto;transform:none">Search error</span></span></p>
<p><a href="#interface-colors" class="heading-anchor" aria-label="Heading link">#</a> <span class="sidebar-footer" style="display:inline"><a class="social-link" href="#interface-colors" aria-label="Social link">{{ partial "sidera/icon.html" "link" }}</a></span></p>
<pre class="chroma"><code><span class="k">const</span> label = <span class="s">"Independent syntax colors"</span>;</code></pre>
</section>{{ end }}
<div class="content-diagram invert-when-dark" id="fixed-light-probe"><a href="#interface-colors">Fixed-light toolbar link</a></div>
</main>{{ end }}''')

for name, flags, prefix in [('baseline', (), '/preview'), ('root', ('--baseURL', 'https://example.invalid/'), '')]:
    out = build(name, extra=flags)
    for lang in ['', 'zh/']:
        raw = (out / lang / 'palette/index.html').read_text()
        nodes = HTML(raw).nodes
        for color in NAMES:
            assert any(a.get('id') == 'box-' + color and a.get('data-color') == color for _, a in nodes)
            assert any(a.get('id') == 'fold-' + color and a.get('data-color') == color for _, a in nodes)
            assert sum(tag == 'mark' and a.get('data-color') == color for tag, a in nodes) >= 10
        assert 'A<mark class=content-mark data-color=yellow><&></mark>B' in unescape(raw)
        assert all(a['data-color'] == 'neutral' for _, a in nodes if a.get('id') in ['default-box', 'default-fold'])
        assert raw.count('role=note') == 50
        assert ('说明' if lang else 'Note') in raw
        assert '<blockquote>' in raw and 'Custom title stays' in raw
        assert 'data-sidera-container=' not in raw and 'data-sidera-leaf=' not in raw
        stylesheet = next(a['href'] for tag, a in nodes if tag == 'link' and a.get('rel') == 'stylesheet')
        assert stylesheet.startswith(prefix + '/css/')
        css = (out / stylesheet.removeprefix(prefix + '/')).read_text()
        for color in NAMES:
            for role in ['text', 'accent', 'surface', 'highlight', 'border']:
                assert f'--palette-{color}-{role}:' in css
        assert 'light-dark(' in css and '@media print' in css

# Contract applies uniformly; unsafe/unsupported CSS is not accepted as a color.
for component in ['mark', 'box', 'folding']:
    for index, (value, diagnostic) in enumerate([
        ('"teal"', 'color must be'), ('"#ff0000"', 'color must be'),
        ('"url(javascript:bad)"', 'color must be'), ('"Blue"', 'color must be'),
        ('42', 'must be a string')]):
        params = f'color={value}' + (' text="x"' if component == 'mark' else ' title="x"')
        content = ('{{< mark ' + params + ' >}}') if component == 'mark' else ('{{% ' + component + ' ' + params + ' %}}\nBody.\n{{% /' + component + ' %}}')
        write('content/negative.md', '---\ntitle: Invalid color\n---\n' + content + '\n')
        build(f'reject-{component}-{index}', diagnostic)
write('content/negative.md', '---\ntitle: Repaired\n---\nValid.\n')

# CSS family tokens remain normal site-overridable custom properties.
write('layouts/_partials/sidera/head-extra.html', '<style>:root { --palette-blue-highlight: #abcdef; }</style>')
build('override')

# Guard the single validation vocabulary and the absence of old duplicated colors.
css = (THEME / 'assets/css/sidera.css').read_text()
helper = (THEME / 'layouts/_partials/components/color.html').read_text()
assert set(re.findall(r'--palette-([a-z]+)-text:', css)) == set(NAMES)
assert all(f'"{name}"' in helper for name in NAMES)
assert not any(old in css for old in ['#f85149', '#3fb950', '#d29922', '#a371f7', '#2f81f7'])
(RUN / 'results.json').write_text(json.dumps({'passed': passed, 'names': NAMES, 'alerts': ALERTS}, indent=2) + '\n')
print('PASS palette:', ', '.join(passed), '\nRetained:', RUN)
