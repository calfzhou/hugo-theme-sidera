"""Cached menu data retains page state, language/entry identity and validation.
Run: python3 tests/check_menus.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import copy
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


for name, title in [('notes/_index', 'Notes'), ('notes/child', 'Child'), ('other/_index', 'Other')]:
    for suffix in ('.md', '.zh.md'):
        write('content/' + name + suffix, f'---\ntitle: {title}\n---\nBody.\n')
base = {
    'baseURL': 'https://example.invalid/', 'theme': THEME.name, 'themesDir': str(THEME.parent),
    'defaultContentLanguage': 'en', 'disableKinds': ['RSS'],
    'languages': {'en': {'weight': 1}, 'zh': {'weight': 2, 'locale': 'zh-CN'}},
    'taxonomies': {'_merge': 'shallow'}, 'permalinks': {'term': {'_merge': 'shallow'}},
    'params': {'footer_menu': 'footer'},
    'menus': {
        'primary': [
            {'identifier': 'home', 'name': 'Primary home', 'pageRef': '/', 'weight': 1},
            {'identifier': 'notes', 'name': 'Primary notes', 'pageRef': '/notes', 'weight': 2,
             'params': {'color': '#aBc4', 'icon': 'notebook'}},
            {'identifier': 'group', 'name': 'Group', 'weight': 3},
            {'identifier': 'child', 'parent': 'group', 'name': 'Primary child', 'pageRef': '/notes/child'},
            {'identifier': 'same-a', 'name': 'Repeated label', 'url': '/one/', 'weight': 4},
            {'identifier': 'same-b', 'name': 'Repeated label', 'url': '/two/', 'weight': 5},
            {'identifier': 'outside', 'name': 'External', 'url': 'https://outside.invalid/?a=1&b=2', 'weight': 6},
        ],
        'footer': [{'identifier': 'notes', 'name': 'Footer notes', 'url': '/different/'}],
    },
}


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.active = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.active = dict(attrs)
            self.active['text'] = ''
            self.links.append(self.active)

    def handle_data(self, data):
        if self.active is not None:
            self.active['text'] += data

    def handle_endtag(self, tag):
        if tag == 'a':
            self.active = None

    def named(self, name):
        return [link for link in self.links if link['text'].strip() == name]


passed, rejected = [], []


def build(name, cfg, diagnostic=None):
    write('hugo.json', json.dumps(cfg))
    out = RUN / (name + '-public')
    result = subprocess.run([
        'hugo', '--source', str(SITE), '--destination', str(out), '--cacheDir', str(RUN / 'cache'),
        '--noBuildLock', '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings',
    ], capture_output=True, text=True, timeout=60)
    text = result.stdout + result.stderr
    (RUN / (name + '.log')).write_text(text)
    if diagnostic:
        assert result.returncode and diagnostic in text, (name, text)
        rejected.append(name)
    else:
        assert not result.returncode, (name, text)
        passed.append(name)
    return out


for name, prefix, icons in [('baseline', '', True), ('subpath', '/preview', True), ('icons-off', '', False)]:
    cfg = copy.deepcopy(base)
    cfg['baseURL'] = 'https://example.invalid' + prefix + '/'
    cfg['params']['icons'] = icons
    out = build(name, cfg)
    for language_prefix in ['', '/zh']:
        for route, expected in [('', None), ('notes/', 'page'), ('notes/child/', 'location'), ('other/', None)]:
            raw = (out / language_prefix.strip('/') / route / 'index.html').read_text()
            links = Links(raw)
            notes = links.named('Primary notes')[0]
            assert notes['href'] == prefix + language_prefix + '/notes/', notes
            assert notes.get('aria-current') == expected, (route, notes)
            assert notes['style'] == '--menu-accent: #aBc4', notes
            child = links.named('Primary child')[0]
            assert child.get('aria-current') == ('page' if route == 'notes/child/' else None), (route, child)
            assert {link['href'] for link in links.named('Repeated label')} == {prefix + '/one/', prefix + '/two/'}
            assert links.named('Footer notes')[0]['href'] == prefix + '/different/'
            external = links.named('External')[0]
            assert external['target'] == '_blank' and external['href'] == 'https://outside.invalid/?a=1&b=2'
            assert set(external['rel'].split()) == {'noopener', 'noreferrer'}
            if not icons:
                assert '<svg' not in raw

# Repeated appearances must not let a cached success hide a malformed entry.
for name, field, value, diagnostic in [
    ('color', 'params', {'color': 'red'}, 'params.color must be a hex color'),
    ('color-type', 'params', {'color': False}, 'params.color must be a hex color string'),
    ('icon', 'params', {'icon': 'missing-icon'}, 'unknown icon'),
    ('unsafe-fallback', 'url', 'javascript:alert(1)', 'unsafe URL'),
    ('missing-page', 'pageRef', '/missing', 'unresolved pageRef'),
]:
    cfg = copy.deepcopy(base)
    cfg['params']['icons'] = False
    cfg['menus']['primary'][1][field] = value
    build('reject-' + name, cfg, diagnostic)
cfg = copy.deepcopy(base)
cfg['menus']['primary'].append({'name': 'Empty leaf', 'identifier': 'empty'})
build('reject-empty', cfg, 'neither a destination nor children')
cfg = copy.deepcopy(base)
cfg['menus']['primary'] += [
    {'identifier': 'nested', 'name': 'Nested group', 'parent': 'group'},
    {'identifier': 'too-deep', 'name': 'Deep', 'parent': 'nested', 'url': '/deep/'},
]
build('reject-depth', cfg, 'exceeds two levels')
(RUN / 'results.json').write_text(json.dumps({'passed': passed, 'rejected': rejected}, indent=2) + '\n')
print('PASS', len(passed), 'menu variants /', len(rejected), 'expected rejections')
