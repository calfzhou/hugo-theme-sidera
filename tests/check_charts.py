"""Native chart authoring, resource boundaries, fallbacks and conditional assets.
Run with a fresh absolute output directory; no dependency installation or network.
The showcase's check_charts_browser.mjs consumes these isolated build fixtures.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, re, subprocess, sys
from urllib.parse import urlsplit, unquote

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh output directory'
SITE = RUN / 'site'
SITE.mkdir(parents=True)

def write(name, text):
    path = SITE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

def build(name, base='https://example.invalid/', language='en', success=True):
    out = RUN / (name + '-public')
    locale = 'zh-CN' if language == 'zh' else 'en-US'
    write('probe.toml', f"defaultContentLanguage='{language}'\nlocale='{locale}'\n" + ("[params]\nicons=false\n" if name == 'icons-off' else ''))
    result = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
        '--cacheDir', str(RUN / 'cache'), '--config', 'hugo.toml,probe.toml', '--baseURL', base,
        '--noBuildLock', '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings'],
        capture_output=True, text=True, timeout=90)
    log = result.stdout + result.stderr
    (RUN / (name + '.log')).write_text(log)
    assert (result.returncode == 0) == success, (name, log)
    if not success:
        assert 'Sidera echarts:' in log, (name, log)
    return out

class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.nodes = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

write('hugo.toml', f'''baseURL='https://example.invalid/'
title='Chart checks'
theme='sidera'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[markup.goldmark.parser.attribute]
_merge='shallow'
''')
option = {
    'tooltip': {'trigger': 'axis'}, 'legend': {'top': 0},
    'xAxis': {'type': 'category', 'data': ['Jan', 'Feb', 'Mar']}, 'yAxis': {'type': 'value'},
    'dataZoom': [{'type': 'slider', 'start': 10, 'end': 90}],
    'series': [{'name': 'Sales', 'type': 'bar', 'data': [12, 18, 15]},
               {'name': 'Target', 'type': 'line', 'data': [14, 16, 19]}]
}
encoded = json.dumps(option)
dataset = [{'month': 'Jan', 'sales': 12}, {'month': 'Feb', 'sales': 18}, {'month': 'Mar', 'sales': 15}]
external = {'tooltip': {'trigger': 'axis'}, 'xAxis': {'type': 'category'}, 'yAxis': {},
            'series': [{'name': 'Sales', 'type': 'bar', 'encode': {'x': 'month', 'y': 'sales'}}]}
page = '''---
title: Interactive charts
---
A caption is meaningful prose; the source values are not indexed.
Sales peak in February.

```echarts {id="inline" caption="Sales <&> target"}
''' + encoded + '''
```

{{< echarts id="paired" caption="Shortcode chart" >}}
''' + encoded + '''
{{< /echarts >}}

{{< echarts src="charts/options 文件.json" id="file" caption="File chart" />}}

```echarts {id="data-fence" data="data/sales.json" caption="Separate dataset"}
''' + json.dumps(external) + '''
```

{{< echarts src="charts/dataset.json" data="data/sales.json" id="data-file" />}}

{{% folding title="Hidden charts" %}}
{{< grid columns=2 >}}
{{< cell >}}
{{< echarts id="nested" caption="Nested chart" >}}
''' + encoded + '''
{{< /echarts >}}
{{< /cell >}}
{{< cell >}}
```echarts {id="nested-fence" caption="Inverted chart" class="invert-when-dark"}
{"legend":{},"series":[{"type":"pie","radius":["35%","65%"],"data":[{"name":"A","value":3},{"name":"B","value":5}]}]}
```
{{< /cell >}}
{{< /grid >}}
{{% /folding %}}

```echarts {id="scatter" height=280}
{"xAxis":{},"yAxis":{},"series":[{"type":"scatter","data":[[1,2],[2,4],[3,3]]}]}
```

```echarts {id="multi"}
{"dataset":[{"source":[["x","y"],[1,2],[2,3]]},{"source":[{"x":1,"y":4},{"x":2,"y":5}]}],"xAxis":{},"yAxis":{},"series":[{"type":"line","datasetIndex":0},{"type":"bar","datasetIndex":1}]}
```
'''
write('content/charts/index.md', page)
write('content/charts/charts/options 文件.json', encoded)
write('content/charts/charts/dataset.json', json.dumps(external))
write('content/charts/data/sales.json', json.dumps(dataset))
adaptive = {'title': {'text': 'Ten series'}, 'legend': {}, 'xAxis': {'type': 'category', 'data': [f'i={i}' for i in range(1, 11)]}, 'yAxis': {},
            'series': [{'name': f'm={m}', 'type': 'line', 'data': [round((m + i) / 20, 3) for i in range(10)]} for m in range(1, 11)]}
write('content/adaptive/index.md', '---\ntitle: Adaptive layout\n---\n' + '\n\n'.join(
    '```echarts {id="' + name + '" caption="' + name + '"}\n' + json.dumps(config) + '\n```'
    for name, config in [('adaptive', adaptive), ('titleless', {**adaptive, 'title': {'show': False}}),
                         ('fixed', {**adaptive, 'grid': {'top': 65, 'bottom': 80}})]))
write('content/security/index.md', '---\ntitle: Inert labels\n---\n```echarts {caption="Safe labels"}\n' + json.dumps({**option, 'title': {'text': '<img src=https://blocked.invalid/pixel onerror=alert(1)>'}, 'tooltip': {'formatter': '<script>alert(1)</script>'}}) + '\n```\n')
write('content/failure/index.md', '---\ntitle: Independent failures\n---\n```echarts {id="broken"}\n{"series":[{"type":"line","data":[1,2]}]}\n```\n\n```echarts {id="healthy"}\n' + encoded + '\n```\n')
write('content/empty/index.md', '---\ntitle: Empty dataset\n---\n```echarts\n' + json.dumps({**external, 'dataset': {'source': [[]]}}) + '\n```\n')
write('content/plain/index.md', '---\ntitle: Plain\n---\nNo charts here.\n')
write('content/code/index.md', '---\ntitle: Code only\n---\n```text\n<figure class="content-chart" data-sidera-chart>\n```\n')
write('content/late/index.md', '---\ntitle: Lazy chart\n---\n' + ('A paragraph before the chart.\n\n' * 120) + '\n```echarts\n' + encoded + '\n```\n')
# Rendered cross-page Content/Summary must load a controller; Plain must not.
for mode in ['Content', 'Summary', 'Plain']:
    write(f'content/host-{mode.lower()}.md', f'---\ntitle: Host {mode}\nlayout: host-{mode.lower()}\n---\n')
    write(f'layouts/host-{mode.lower()}.html', '{{ define "main" }}{{ $p := site.GetPage "/charts" }}{{ partial "sidera/shell.html" (dict "Page" . "Content" $p.' + mode + ') }}{{ end }}')
# Explicit summary containing only the first chart.
write('content/charts/index.md', page.replace('{{< echarts id="paired"', '<!--more-->\n\n{{< echarts id="paired"'))
manifest = json.loads((THEME / 'assets/vendor/echarts-6.1.0/provenance.json').read_text())
for name, digest in manifest['files'].items():
    assert hashlib.sha256((THEME / 'assets/vendor/echarts-6.1.0' / name).read_bytes()).hexdigest() == digest

for name, base, lang in [('baseline', 'https://example.invalid/', 'en'),
                         ('subpath', 'https://example.invalid/sidera-showcase/', 'en'),
                         ('chinese', 'https://example.invalid/_chinese/', 'zh'),
                         ('icons-off', 'https://example.invalid/_icons/', 'en')]:
    out = build(name, base, lang)
    raw = (out / 'charts/index.html').read_text(); dom = DOM(raw)
    figures = [attrs for tag, attrs in dom.nodes if 'data-sidera-chart' in attrs]
    assert len(figures) == 9, (name, len(figures))
    assert 'Sales &lt;&amp;&gt; target' in raw and 'Sales peak in February.' in raw
    assert not any(a.get('class') in ('chart-table', 'chart-controls', 'chart-description') for _, a in dom.nodes)
    assert sum(tag == 'details' and a.get('class') == 'chart-source' and 'open' in a for tag, a in dom.nodes) == 9
    for route in ['plain', 'code', 'host-plain']:
        assert 'data-sidera-charts-script' not in (out / route / 'index.html').read_text()
    for route in ['host-content', 'host-summary']:
        assert 'data-sidera-charts-script' in (out / route / 'index.html').read_text(), route
    sources = re.findall(r'<code>(.*?)</code>', raw, re.S)
    from html import unescape
    configs = [json.loads(unescape(s)) for s in sources if unescape(s).startswith('{')]
    assert configs[3]['dataset']['source'] == dataset
    assert configs[4]['dataset']['source'] == dataset
    downloads = [a for tag, a in dom.nodes if tag == 'a' and 'chart-download' in a.get('class', '').split()]
    assert len(downloads) == len(configs) == 9
    if name == 'icons-off':
        assert all(f['data-icons'] == 'false' for f in figures)
        assert '>Download JSON</a>' in raw
    for download, config, source in zip(downloads, configs, sources):
        assert download['download'] == 'chart.json'
        prefix = urlsplit(base).path
        assert download['href'].startswith(prefix + 'charts/source/')
        file = out / unquote(download['href'][len(prefix):])
        assert file.read_text() == unescape(source)
        assert json.loads(file.read_text()) == config
        assert '\n  "' in file.read_text(), 'Source must be readable, not a single minified line'
    frame = next((out / 'charts').glob('echarts-6.1.0.*.html')).read_text()
    assert "connect-src 'none'" in frame and "img-src 'none'" in frame and "script-src 'self'" in frame
    assert 'allow-same-origin' not in frame and 'unsafe-eval' not in frame
    if name == 'subpath':
        assert 'src="/sidera-showcase/vendor/' in frame
        assert 'data-frame="/sidera-showcase/charts/' in raw
    assert ('查看源代码' if lang == 'zh' else 'View source') in raw
    for file in manifest['files']:
        if file != 'echarts.common.min.js': assert (out / 'vendor/echarts-6.1.0' / file).exists()
    # Source payload and controls must not enter search, captions should.
    index = json.loads(next((out / 'search').glob('*.json')).read_text())
    doc = next(d for d in index['documents'] if d['url'].endswith('/charts/'))
    text = json.dumps(doc['sections'])
    assert 'Sales peak in February.' in text and 'Sales <&> target' in text
    assert 'dataZoom' not in text and 'View source' not in text and 'Download JSON' not in text

invalid = {
    'json': '```echarts\n{"series": [}\n```',
    'trailing-comma': '```echarts\n{"series": [],}\n```',
    'yaml': '```echarts\nseries: []\n```',
    'array': '```echarts\n[]\n```',
    'no-series': '```echarts\n{}\n```',
    'series-object': '```echarts\n{"series":{"type":"bar"}}\n```',
    'unknown-type': '```echarts\n{"series":[{"type":"custom"}]}\n```',
    'traversal': '{{< echarts src="../other.json" />}}',
    'remote': '{{< echarts src="https://example.invalid/a.json" />}}',
    'glob': '{{< echarts src="*.json" />}}',
    'missing': '{{< echarts src="missing.json" />}}',
    'both': '{{< echarts src="a.json" >}}' + encoded + '{{< /echarts >}}',
    'empty-caption': '```echarts {caption=" "}\n' + encoded + '\n```',
    'height': '```echarts {height=0}\n' + encoded + '\n```',
    'description-fence': '```echarts {description="Removed parameter"}\n' + encoded + '\n```',
    'description-shortcode': '{{< echarts description="Removed parameter" >}}' + encoded + '{{< /echarts >}}',
    'unknown-argument': '{{< echarts url="a.json" >}}' + encoded + '{{< /echarts >}}',
    'unknown-option': '```echarts\n' + json.dumps({**option, 'toolbox': {}}) + '\n```',
    'array-tooltip': '```echarts\n' + json.dumps({**option, 'tooltip': [{}]}) + '\n```',
    'boolean-tooltip': '```echarts\n' + json.dumps({**option, 'tooltip': True}) + '\n```',
    'html-tooltip': '```echarts\n' + json.dumps({**option, 'tooltip': {'renderMode': 'html'}}) + '\n```',
    'link': '```echarts\n' + json.dumps({**option, 'title': {'link': 'javascript:alert(1)'}}) + '\n```',
    'image': '```echarts\n' + json.dumps({**option, 'series': [{'type': 'line', 'symbol': 'image://https://example.invalid/x'}]}) + '\n```',
    'prototype': '```echarts\n' + json.dumps({**option, 'textStyle': {'__proto__': {'x': 1}}}) + '\n```',
    'dataset-conflict': '{{< echarts data="data.json" >}}' + json.dumps({**option, 'dataset': {'source': []}}) + '{{< /echarts >}}',
    'dataset-array': '{{< echarts data="data.json" >}}' + json.dumps({**option, 'dataset': []}) + '{{< /echarts >}}',
    'dataset-rows': '```echarts\n' + json.dumps({**option, 'dataset': {'source': [1, 2]}}) + '\n```',
    'transform': '```echarts\n' + json.dumps({**option, 'dataset': {'transform': {'type': 'filter'}}}) + '\n```',
    'too-deep': '```echarts\n' + '{"series":[{"type":"line","data":' + '['*26 + '0' + ']'*26 + '}]}\n```',
    'too-many': '```echarts\n' + json.dumps({**option, 'series': [{'type': 'line', 'data': [0] * 10001}]}) + '\n```',
    'too-large': '```echarts\n' + json.dumps({**option, 'title': {'text': 'x' * 1000000}}) + '\n```',
}
write('content/invalid/a.json', encoded)
write('content/invalid/data.json', json.dumps(dataset))
for name, body in invalid.items():
    write('content/invalid/index.md', '---\ntitle: Invalid\n---\n' + body + '\n')
    build('invalid-' + name, success=False)
# Retain fixtures without deleting any files; browser mounts the successful builds.
write('content/invalid/index.md', '---\ntitle: Valid again\n---\nNo chart.\n')
print(f'PASS charts: 4 build variants, {len(invalid)} rejected inputs, native composition, conditional assets and vendor hashes; {RUN}')
