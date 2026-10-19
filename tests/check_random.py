"""Shared random-article pools and component/default/publication contracts.
Run: uv run --no-project --no-managed-python python3 tests/check_random.py <fresh-output>
"""
from pathlib import Path
from html.parser import HTMLParser
import copy
import json
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
RUN.mkdir(parents=True, exist_ok=False)
SITE = RUN / 'site'


def write(path, text):
    path = SITE / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def page(path, **meta):
    write('content/' + path + '.md', '---\n' + json.dumps({'title': path, **meta}) + '\n---\nArticle body.\n')


class HTML(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.buttons = []
        self.scripts = []
        self.components = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'button' and 'data-sidera-random' in attrs:
            self.buttons.append(attrs)
        if tag == 'script' and 'data-sidera-random-script' in attrs:
            self.scripts.append(attrs)
        if 'data-component' in attrs:
            self.components.append(attrs['data-component'])


base = {
    'baseURL': 'https://example.invalid/preview/', 'theme': THEME.name,
    'themesDir': str(THEME.parent), 'defaultContentLanguage': 'en',
    'languages': {'en': {'weight': 1}, 'zh': {'weight': 2, 'locale': 'zh-CN'}},
    'disableKinds': ['RSS'], 'taxonomies': {'_merge': 'shallow'},
    'permalinks': {'term': {'_merge': 'shallow'}},
    'params': {'search': False, 'search_index': False},
}
for lang in ['', '.zh']:
    for name, preset in [('journal', 'blog'), ('notes', 'notes'), ('docs', 'docs')]:
        page(f'{name}/_index{lang}', preset=preset)
        page(f'{name}/article{lang}')
    page(f'standalone{lang}')
    page(f'notes/nested/_index{lang}', params={'scope_root': True})
    page(f'notes/nested/article{lang}')
    page(f'notes/unindexed{lang}', params={'search_index': False})
    page(f'notes/draft{lang}', draft=True)
    page(f'notes/future{lang}', publishDate='2999-01-01T00:00:00Z')
    page(f'notes/expired{lang}', expiryDate='2000-01-01T00:00:00Z')
    page(f'notes/link-only{lang}', build={'render': 'link'})
    page(f'notes/never{lang}', build={'render': 'never'})
    page(f'notes/unlisted{lang}', build={'list': 'never'})
    page(f'notes/json-only{lang}', outputs=['JSON'])
    page(f'notes/custom-url{lang}', url=f'/special{"-zh" if lang else ""}/')
    page(f'custom{lang}', params={'left': ['menu'], 'right': []})
    page(f'repeats{lang}', params={
        'top': ['random'], 'left': ['random', {'component': 'random', 'config': {'icons': False}}],
        'right': ['random'], 'left_footer': ['random'],
    })
write('layouts/single.json', '{{ dict "title" .Title | jsonify }}')
passed = []


def build(name, cfg, diagnostic=None):
    write('hugo.json', json.dumps(cfg))
    out = RUN / (name + '-public')
    result = subprocess.run([
        'hugo', '--source', str(SITE), '--destination', str(out),
        '--cacheDir', str(RUN / (name + '-cache')), '--noBuildLock', '--minify',
        '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings',
    ], capture_output=True, text=True, timeout=60)
    log = result.stdout + result.stderr
    (RUN / (name + '.log')).write_text(log)
    if diagnostic:
        assert result.returncode and diagnostic in log, (name, log)
    else:
        assert not result.returncode, (name, log)
    passed.append(name)
    return out


for name, prefix, icons in [('baseline', '/preview', True), ('root', '', True), ('icons-off', '/preview', False)]:
    cfg = copy.deepcopy(base)
    cfg['baseURL'] = 'https://example.invalid' + prefix + '/'
    cfg['params']['icons'] = icons
    out = build(name, cfg)
    for lang in ['', 'zh/']:
        shared = set()
        expected = {prefix + '/' + lang + route + '/' for route in [
            'journal/article', 'notes/article', 'docs/article', 'standalone',
            'notes/nested/article', 'notes/unindexed', 'custom', 'repeats',
        ]}
        expected.add(prefix + '/special' + ('-zh' if lang else '') + '/')
        for route in ['', 'journal/', 'journal/article/', 'notes/', 'notes/article/', 'docs/', 'docs/article/', 'standalone/', 'repeats/']:
            html = HTML(out / lang / route / 'index.html')
            assert len(html.buttons) == (5 if route == 'repeats/' else 1), (name, lang, route)
            assert all(b['type'] == 'button' and 'hidden' in b for b in html.buttons)
            assert len(html.scripts) == 1
            script = html.scripts[0]
            assert script['data-current'] == prefix + '/' + lang + route
            shared.add(script['data-index'])
            assert script['data-index'].startswith(prefix + '/random/')
            pool = json.loads((out / script['data-index'].removeprefix(prefix + '/')).read_text())
            assert len(pool) == len(set(pool)) and set(pool) == expected, (name, lang, pool, expected)
            # All ordinary articles, including the current one, share this exact pool.
            if route.endswith('article/'):
                assert script['data-current'] in pool
            raw = (out / lang / route / 'index.html').read_text()
            assert ('随机文章' if lang else 'Random article') in raw
            if not icons:
                assert '<svg' not in raw
        assert len(shared) == 1, shared
        custom = HTML(out / lang / 'custom/index.html')
        assert not custom.buttons and not custom.scripts
    assert len(list((out / 'random').glob('*.json'))) == 2

# Explicit site-level composition replaces the general default; presets still own
# their configured defaults, as before. A disabled region must remain disabled.
cfg = copy.deepcopy(base)
cfg['params'].update({'left': [], 'right': []})
out = build('custom-default', cfg)
assert not HTML(out / 'index.html').buttons
assert not HTML(out / 'standalone/index.html').buttons
assert HTML(out / 'docs/article/index.html').buttons

# No scope/filter knobs: reject unsupported options through the normal schema.
for config in [{'scope': 'global'}, {'icons': 'yes'}]:
    cfg = copy.deepcopy(base)
    cfg['params']['left'] = [{'component': 'random', 'config': config}]
    build('reject-' + next(iter(config)), cfg, 'unknown random config option' if 'scope' in config else 'must be boolean')

# Isolated empty and singleton language pools (no destructive fixture cleanup).
for name, article in [('empty', False), ('single', True)]:
    SITE = RUN / (name + '-site')
    cfg = copy.deepcopy(base)
    cfg.pop('languages')
    cfg['baseURL'] = 'https://example.invalid/' + name + '/'
    page('_index')
    if article:
        page('only')
    out = build(name, cfg)
    home = HTML(out / 'index.html')
    assert bool(home.buttons) == article
    if article:
        only = HTML(out / 'only/index.html')
        assert not only.buttons and not only.scripts
        pool = json.loads(next((out / 'random').glob('*.json')).read_text())
        assert pool == ['/single/only/']
    else:
        assert not home.scripts and not (out / 'random').exists()

(RUN / 'results.json').write_text(json.dumps(passed, indent=2) + '\n')
print('PASS random article:', ', '.join(passed))
