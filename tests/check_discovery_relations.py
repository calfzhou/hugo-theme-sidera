"""Indexed references: exact relationship semantics and owned live rebuilds.
Run: python3 tests/check_discovery_relations.py /absolute/fresh-output-directory
Uses SIDERA_PREVIEW_PORT (default 14851); never attaches to an existing server.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh output directory'
RUN.mkdir(parents=True)


def write(site, name, text):
    path = site / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def config(base_url):
    return f'''baseURL={json.dumps(base_url)}
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
'''


class Relations(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.kind = None
        self.items = {'outgoing': [], 'backlinks': []}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'ul':
            self.kind = attrs.get('data-content-relations')
        if tag == 'a' and self.kind:
            self.items[self.kind].append((attrs['href'], attrs.get('hreflang')))

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.kind = None


# The catalog contract already deduplicates links and filters body publication.
# Keep graph opt-outs here to exercise both index directions independently.
site = RUN / 'catalog-site'
write(site, 'hugo.toml', config('https://example.invalid/') + "\n[outputs]\nhome=['JSON']\n")
rows = [
    ('a', True, ['/a/', '/b/', '/c/', '/fr/d/', '/missing/'], 'en'),
    ('b', True, ['/a/', '/c/'], 'en'),
    ('c', False, ['/a/', '/b/'], 'en'),
    ('fr/d', True, ['/a/'], 'fr'),
    ('empty', True, [], 'en'),
]
catalog = [dict(url=f'/{name}/', title=name, graph=graph, links=links, language=lang)
           for name, graph, links, lang in rows]
write(site, 'data/catalog.json', json.dumps(catalog))
write(site, 'layouts/_partials/discovery/catalog.html', '{{- return hugo.Data.catalog -}}')
write(site, 'layouts/home.json', '''{{ $results := slice }}
{{ range slice "/a/" "/b/" "/c/" "/fr/d/" "/empty/" "/missing/" }}
  {{ $url := . }}{{ range slice "outgoing" "backlinks" }}{{ $name := . }}{{ range slice true false }}
    {{ $ctx := dict "Page" (dict "RelPermalink" $url "Language" (dict "Lang" "en")) "Settings" (dict "link_graph" .) "Name" $name "Instance" "probe" }}
    {{ $html := partial "discovery/references.html" $ctx }}
    {{ $results = $results | append (dict "url" $url "kind" $name "enabled" . "html" $html) }}
  {{ end }}{{ end }}
{{ end }}{{ $results | jsonify }}''')
result = subprocess.run([
    'hugo', '--source', str(site), '--destination', str(RUN / 'catalog-public'),
    '--cacheDir', str(RUN / 'catalog-cache'), '--noBuildLock', '--panicOnWarning',
    '--printPathWarnings', '--printI18nWarnings',
], capture_output=True, text=True, timeout=60)
(RUN / 'catalog.log').write_text(result.stdout + result.stderr)
assert not result.returncode, result.stdout + result.stderr
records = json.loads((RUN / 'catalog-public/index.json').read_text())
by_url = {row['url']: row for row in catalog}
for record in records:
    own = by_url.get(record['url'])
    expected = []
    if own and record['enabled']:
        for other in catalog:
            if not other['graph'] or other['url'] == own['url']:
                continue
            linked = (other['url'] in own['links'] if record['kind'] == 'outgoing'
                      else own['url'] in other['links'])
            if linked:
                expected.append((other['url'], other['language'] if other['language'] != 'en' else None))
    assert Relations(record['html']).items[record['kind']] == sorted(expected), record
assert len(records) == 24

# Exercise the real body catalog in an isolated server, including publication and
# duplicate hash/query links. Each rebuild must invalidate the graph index.
site = RUN / 'preview-site'
port = int(os.environ.get('SIDERA_PREVIEW_PORT', '14851'))
base = f'http://127.0.0.1:{port}'
write(site, 'hugo.toml', config(base + '/'))
write(site, 'content/notes/_index.md', '---\ntitle: Notes\npreset: notes\n---\n')


def article(name, body='', extra=''):
    return f'---\ntitle: {name.upper()}\n{extra}---\n{body}\n'


write(site, 'content/notes/a.md', article('a', '[B](b.md) [B again](b.md?q=1#body) [Self](a.md)'))
write(site, 'content/notes/b.md', article('b', '## Body\n'))
write(site, 'content/notes/c.md', article('c'))
checks = []


def state(name):
    with urllib.request.urlopen(base + f'/notes/{name}/', timeout=3) as response:
        html = response.read().decode()
    # Do not mistake Hugo's injected error page for an empty relationship list.
    if 'data-search-body' not in html:
        raise ValueError('Waiting for a complete rendered article')
    return {kind: [url for url, _ in items] for kind, items in Relations(html).items.items()}


def wait(label, expected):
    last = None
    for _ in range(160):
        try:
            last = {name: state(name) for name in expected}
            if all(all(last[name][kind] == urls for kind, urls in fields.items())
                   for name, fields in expected.items()):
                checks.append(label)
                return
        except (OSError, ValueError):
            pass
        time.sleep(.15)
    raise AssertionError((label, last, expected))


probe = socket.socket()
probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
probe.bind(('127.0.0.1', port))
probe.close()
with (RUN / 'preview.log').open('w') as log:
    proc = subprocess.Popen([
        'hugo', 'server', '--source', str(site), '--bind', '127.0.0.1',
        '--port', str(port), '--baseURL', base + '/', '--disableFastRender',
        '--noHTTPCache', '--noBuildLock', '--destination', str(RUN / 'preview-public'),
        '--cacheDir', str(RUN / 'preview-cache'),
    ], stdout=log, stderr=subprocess.STDOUT, env={**os.environ, 'GOMAXPROCS': '2'})
    try:
        wait('deduplicated edge and no self-link', {'a': {'outgoing': ['/notes/b/']}, 'b': {'backlinks': ['/notes/a/']}})
        write(site, 'content/notes/a.md', article('a', '[C](c.md)'))
        wait('replace edge clears old backlink', {'a': {'outgoing': ['/notes/c/']}, 'b': {'backlinks': []}, 'c': {'backlinks': ['/notes/a/']}})
        write(site, 'content/notes/c.md', article('c', extra='params:\n  link_graph: false\n'))
        wait('target graph opt-out', {'a': {'outgoing': []}, 'c': {'backlinks': []}})
        write(site, 'content/notes/c.md', article('c'))
        wait('restore target', {'a': {'outgoing': ['/notes/c/']}, 'c': {'backlinks': ['/notes/a/']}})
        write(site, 'content/notes/a.md', article('a', '[C](c.md)', extra='params:\n  link_graph: false\n'))
        wait('source graph opt-out', {'a': {'outgoing': []}, 'c': {'backlinks': []}})
        write(site, 'content/notes/a.md', article('a', '[C](c.md)'))
        wait('restore source', {'a': {'outgoing': ['/notes/c/']}, 'c': {'backlinks': ['/notes/a/']}})
        write(site, 'content/notes/a.md', article('a', 'No links.'))
        wait('remove edge', {'a': {'outgoing': []}, 'c': {'backlinks': []}})
        write(site, 'content/notes/a.md', article('a', '[C](c.md)'))
        wait('restore edge', {'a': {'outgoing': ['/notes/c/']}, 'c': {'backlinks': ['/notes/a/']}})
        write(site, 'content/notes/a.md', article('a', '[C](c.md)', extra='draft: true\n'))
        wait('draft source leaves catalog', {'c': {'backlinks': []}})
        # Republishing after this can leave unrelated footer output stale on
        # Hugo 0.166.0, also with the original scan-based implementation.
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
(RUN / 'results.json').write_text(json.dumps({'static_cases': len(records), 'preview': checks}, indent=2) + '\n')
print('PASS', len(records), 'relation cases /', len(checks), 'live graph rebuild cases')
