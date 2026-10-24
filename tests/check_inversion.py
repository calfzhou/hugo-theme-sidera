"""Opt-in inversion strength, native image markup and diagram fixtures.
Run with a fresh absolute output directory; no external files or services.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh output directory'
SITE = RUN / 'site'
SITE.mkdir(parents=True)
CASES = {
    'none': '', 'alone': 'invert-soft',
    'dark': 'invert-when-dark', 'dark-soft': 'invert-when-dark invert-soft',
    'light': 'invert-when-light', 'light-soft': 'invert-when-light invert-soft',
    'both': 'invert-when-dark invert-when-light',
    'both-soft': 'invert-when-dark invert-when-light invert-soft',
}


def write(name, text):
    p = SITE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


write('hugo.json', json.dumps({
    'baseURL': 'https://example.invalid/preview/', 'title': 'Inversion checks',
    'theme': THEME.name, 'themesDir': str(THEME.parent), 'disableKinds': ['RSS'],
    'params': {'comments': False, 'page_reveal': False, 'search': False, 'search_index': False},
    'languages': {'en': {'weight': 1}, 'zh': {'weight': 2, 'locale': 'zh-CN'}},
    'taxonomies': {'_merge': 'shallow'}, 'permalinks': {'term': {'_merge': 'shallow'}},
    'markup': {'goldmark': {'parser': {'_merge': 'deep', 'attribute': {'_merge': 'shallow'}}}},
}))
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="180" viewBox="0 0 400 180"><rect width="400" height="180" fill="white"/><path d="M60 90H340" stroke="#17191b" stroke-width="3"/><rect x="20" y="50" width="130" height="80" rx="8" fill="#feedec" stroke="#c0524e" stroke-width="3"/><rect x="250" y="50" width="130" height="80" rx="8" fill="#eaf3fe" stroke="#387bcc" stroke-width="3"/><text x="85" y="96" font-family="sans-serif" font-size="22" text-anchor="middle" fill="#17191b">Input</text><text x="315" y="96" font-family="sans-serif" font-size="22" text-anchor="middle" fill="#17191b">Output</text></svg>'''
write('content/inversion/sample.svg', svg)
write('content/inversion/original.svg', svg.replace('width="400" height="180"', 'width="1200" height="540"', 1))
parts = ['---\ntitle: Inversion strength\n---\n', '## Image cases\n']
for name, cls in CASES.items():
    classes = ''.join(' .' + c for c in cls.split())
    parts.append(f'''### {name}

![Markdown {name}](sample.svg)
{{#md-{name}{classes} .no-caption width=240 loading="eager"}}

{{{{< image src="sample.svg" original="original.svg" alt="Image {name}" caption="Caption {name}" width=240 loading="eager" id="image-{name}"{(' class="'+cls+'"') if cls else ''} >}}}}

{{{{% block id="group-{name}"{(' class="'+cls+'"') if cls else ''} %}}}}
{{{{< image src="sample.svg" original="original.svg" alt="Grouped {name}" width=240 id="group-image-{name}" >}}}}
{{{{% /block %}}}}
''')
parts.append('''## Nested scope

{{% block class="invert-soft" id="modifier-parent" %}}
{{< image src="sample.svg" original="original.svg" class="invert-when-dark" alt="Modifier does not inherit" id="not-inherited" width=240 >}}
{{% /block %}}

{{% block class="invert-when-dark" id="direction-parent" %}}
{{< image src="sample.svg" original="original.svg" class="invert-soft" alt="Child modifier cannot affect a parent" id="modifier-child" width=240 >}}
{{% /block %}}

{{% block class="invert-when-dark invert-soft" id="nested-parent" %}}
{{< image src="sample.svg" original="original.svg" class="invert-when-dark" alt="Explicit nested filters" id="nested-child" width=240 >}}
{{% /block %}}

## Diagrams
''')
for name, cls in [('alone', 'invert-soft'), ('dark', 'invert-when-dark'), ('dark-soft', 'invert-when-dark invert-soft'), ('light-soft', 'invert-when-light invert-soft'), ('both-soft', 'invert-when-dark invert-when-light invert-soft')]:
    parts.append(f'''```mermaid {{id="mermaid-{name}" class="{cls}"}}
flowchart LR
  A[Read] --> B[Render]
```

{{{{% block id="drawio-{name}" class="{cls}" %}}}}
{{{{< diagramsnet src="sample.drawio" caption="Drawio {name}" >}}}}
{{{{% /block %}}}}
''')
parts.append('''{{% block id="nested-diagram" class="invert-when-dark invert-soft" %}}
{{< block class="invert-when-dark" >}}
{{< diagramsnet src="sample.drawio" caption="Nested filters" >}}
{{< /block >}}
{{% /block %}}

```echarts {id="chart-soft" class="invert-when-dark invert-soft" height=240}
{"xAxis":{"type":"category","data":["A","B"]},"yAxis":{},"series":[{"type":"bar","data":[2,3]}]}
```
''')
body = '\n'.join(parts)
write('content/inversion/index.md', body)
write('content/inversion/index.zh.md', body.replace('title: Inversion strength', 'title: Inversion strength — Chinese controls'))
write('content/inversion/sample.drawio', '<mxfile><diagram name="Example" id="example"><mxGraphModel grid="1" page="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="a" value="Read source" style="rounded=1;whiteSpace=wrap;html=0;" vertex="1" parent="1"><mxGeometry x="20" y="20" width="180" height="70" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>')


class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


for name, args in [('baseline', []), ('root', ['--baseURL', 'https://example.invalid/']), ('icons-off', ['--config', 'hugo.json,icons-off.toml'])]:
    write('icons-off.toml', '[params]\nicons=false\n')
    out = RUN / (name + '-public')
    result = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
        '--cacheDir', str(RUN / (name + '-cache')), '--noBuildLock', '--minify',
        '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings', *args],
        capture_output=True, text=True, timeout=90)
    (RUN / (name + '.log')).write_text(result.stdout + result.stderr)
    assert not result.returncode, (name, result.stdout, result.stderr)
    for locale in ['', 'zh/']:
        raw = (out / locale / 'inversion/index.html').read_text()
        nodes = DOM(raw).nodes
        by_id = {a['id']: (tag, a) for tag, a in nodes if 'id' in a}
        for key, cls in CASES.items():
            for prefix in ['md-', 'image-', 'group-']:
                assert set(cls.split()) <= set(by_id[prefix + key][1].get('class', '').split())
        assert 'data-sidera-image-viewer' in raw and 'data-sidera-diagrams-script' in raw
        assert 'data-sidera-container=' not in raw
        if name == 'icons-off':
            assert not any(tag == 'svg' for tag, _ in nodes)
    assert (out / 'inversion/original.svg').read_text() == (SITE / 'content/inversion/original.svg').read_text()
(RUN / 'results.json').write_text(json.dumps({'cases': CASES, 'builds': ['baseline', 'root', 'icons-off']}, indent=2) + '\n')
print('PASS inversion fixtures: eight class combinations, native Markdown/shortcodes/wrappers, nesting, images/diagrams/chart, EN/ZH, root/prefix and icons-off;', RUN)
