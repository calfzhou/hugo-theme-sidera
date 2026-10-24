"""Native styling fixtures: secondary text, controls, inline labels and layouts.
Run with a fresh absolute output directory; uses installed Hugo and the local theme.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh output directory'
SITE = RUN / 'site'
SITE.mkdir(parents=True)


def write(name, text):
    path = SITE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def page(name, title, body, params=None, **other):
    meta = {'title': title, 'date': '2026-01-01T00:00:00+08:00', **other}
    if params:
        meta['params'] = params
    for suffix in ['', '.zh']:
        write('content/' + name + suffix + '.md', '---\n' + json.dumps(meta) + '\n---\n' + body)


config = {
    'baseURL': 'https://example.invalid/preview/', 'title': 'Style consistency',
    'theme': THEME.name, 'themesDir': str(THEME.parent), 'disableKinds': ['RSS'],
    'languages': {'en': {'weight': 1}, 'zh': {'weight': 2, 'locale': 'zh-CN'}},
    'taxonomies': {'_merge': 'shallow'}, 'permalinks': {'term': {'_merge': 'shallow'}},
    'markup': {'goldmark': {'parser': {'_merge': 'deep', 'attribute': {'_merge': 'shallow'}}}},
    'params': {
        'comments': False, 'jsx': True, 'page_reveal': False,
        'identity': {'image': 'images/sidera-parallax-circle.svg'},
        'article_end_text': 'A closing [text link](/probe/#reading).',
        'references': ['A [reference link](/probe/#reading).'],
        'article_text': 'An [article footer link](/probe/#reading).',
        'footer_text': 'A [site footer link](/probe/#reading).',
        'left': ['menu', 'random', 'recent-updates'], 'right': ['toc'],
    },
    'menus': {
        'primary': [{'name': 'Overview', 'pageRef': '/', 'weight': 1},
                    {'name': 'Probe', 'pageRef': '/probe', 'weight': 2},
                    {'name': 'Notes', 'pageRef': '/notes', 'weight': 3}],
        'social': [{'name': 'Probe', 'pageRef': '/probe', 'params': {'icon': 'link'}},
                   {'name': 'Overview', 'pageRef': '/', 'params': {'icon': 'home'}}],
    },
}
write('hugo.json', json.dumps(config))
body = '''## Reading

A [body link](#reading) with ordinary content and `inline code`.

> A readable quotation with supporting context.

{{< link href="/probe/" text="A linked reference card" >}}

{{% folding title="An important detail" %}}
Plain text label.
{{% /folding %}}

{{% folding title="An **important** detail" %}}
Formatted text label.
{{% /folding %}}

{{% folding title="A **long label** with [a local link](#reading), *emphasis*, and several words that must wrap together at a narrow width" %}}
Nested content is still Markdown.
{{% /folding %}}

{{% timeline %}}
{{< event title="First observation" >}}
A timeline entry.
{{< /event >}}
{{% /timeline %}}

## Controls

```javascript
const meaning = "One palette, many contexts";
```

{{< video src="https://example.invalid/not-loaded.mp4" title="A video control" >}}

{{< image src="sample.svg" original="sample.svg" alt="Local sample" width=160 >}}

{{< jsx src="Controls.jsx" title="Controls" />}}

{{< jsx src="Controls.jsx" title="Sandbox controls" mode="sandbox" height=240 />}}

## More reading

''' + ('An ordinary paragraph keeps the preview readable beside the navigation.\n\n' * 8)
page('probe/index', 'Content and controls', body)
write('content/probe/sample.svg', '<svg xmlns="http://www.w3.org/2000/svg" width="160" height="80"><rect width="160" height="80" fill="#387bcc"/></svg>')
write('content/probe/Controls.jsx', '''export default function Controls(){return <div className="jsx-stack">
<div className="jsx-row"><button type="button">Enabled</button><button type="button" disabled>Disabled</button></div>
<label>Example input<input placeholder="An input" /></label>
<p style={{color:'var(--secondary-text)'}}>Secondary text</p></div>}''')
page('compact', 'Compact header', '## Compact layout\n\nSame social controls without a left sidebar.\n\n' + ('Reading content.\n\n' * 8), {'left': [], 'right': []})
page('guide/_index', 'Guide', 'A short document tree.', preset='docs')
page('guide/first', 'First chapter', '## Chapter one\n\nRead the instructions.\n\n## Details\n\nMore context.')
page('guide/second', 'Second chapter', '## Chapter two\n\nContinue reading.')
page('notes/_index', 'Notes', '## Notes overview\n\n' + ('A collection of examples.\n\n' * 18), preset='notes', params={'page_size': 2})
for i in range(6):
    page(f'notes/note-{i}', f'Note {i}', '## Note heading\n\nAn example note for pagination.', tags=['sample'])

result = subprocess.run([
    'hugo', '--source', str(SITE), '--destination', str(RUN / 'public'),
    '--cacheDir', str(RUN / 'cache'), '--noBuildLock', '--minify',
    '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings',
], capture_output=True, text=True, timeout=90)
(RUN / 'build.log').write_text(result.stdout + result.stderr)
assert result.returncode == 0, result.stdout + result.stderr


class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


for lang in ['', 'zh/']:
    raw = (RUN / 'public' / lang / 'probe/index.html').read_text()
    nodes = DOM(raw).nodes
    labels = [a for _, a in nodes if a.get('class') == 'folding-title']
    assert len(labels) == 3
    assert '<strong>important</strong>' in raw
    assert not any(tag == 'script' and a.get('src', '').startswith('http') for tag, a in nodes)
    assert any(a.get('class') == 'article-end' for _, a in nodes)
    assert not any('data-sidera-giscus' in a for _, a in nodes)
    assert [a['data-mode'] for _, a in nodes if 'data-sidera-jsx' in a] == ['page', 'sandbox']
print('PASS native style fixtures: EN/ZH, safe inline fold titles, footer/end slots, page/sandbox JSX, compact layout and pagination; retained', RUN)
