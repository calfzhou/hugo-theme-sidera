"""Native cascaded authors and safe linked configured-Markdown interpolation.
Standard library only; pass a fresh absolute output directory. No network calls.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
RUN.mkdir(parents=True, exist_ok=False)
SITE = RUN / 'site'
SITE.mkdir()


def write(path, text):
    p = SITE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


CONFIG = f'''baseURL = 'https://example.invalid/preview/'
title = 'Site *title*'
theme = '{THEME.name}'
themesDir = {json.dumps(str(THEME.parent))}
disableKinds = ['RSS']
[cascade]
authors = ['editor']
[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'
[params]
license = 'By {{page.authors}}.'
'''
write('hugo.toml', CONFIG)
write('content/notes/_index.md', '---\ntitle: Notes\npreset: notes\n---\nNotes.\n')
write('content/authors/_index.md', '---\ntitle: Authors\nauthors: []\n---\n')
write('content/authors/editor/_index.md', '---\ntitle: Editor\nauthors: []\n---\n')
HOSTILE = 'AI ](https://evil.invalid/) <img src=x onerror=alert(1)> & **bold** {page.title}'
write('content/authors/ai/_index.md', '---\ntitle: ' + json.dumps(HOSTILE) + '\nurl: /people/ai-(writer)/\nauthors: []\n---\n')
for name, fm in [('default', ''), ('multiple', 'authors: [ai, editor]\n'),
                 ('empty', 'authors: []\n'), ('hidden', 'authors: [ai]\nparams:\n  show_authors: false\n')]:
    write(f'content/notes/{name}/index.md', f'---\ntitle: "{name} *title*"\nlayout: probe\n{fm}---\nBody token: {{page.authors}}.\n')
write('content/manual/_index.md', '---\ntitle: Manual\npreset: docs\nauthors: []\ncascade:\n  authors: []\n---\n')
write('content/manual/intro.md', '---\ntitle: Intro\nlayout: probe\n---\nManual.\n')
CASES = {
    'authors': '{page.authors}',
    'license': 'By {page.authors}.',
    'repeated': '{page.authors} / {page.authors}',
    'text': '{site.title} / {page.title} / {custom.value}',
    'unknown': '{unknown.value}',
    'code': '`{page.authors}`',
    'escaped': r'\{page.authors}',
    'fence': '```text\n{page.authors}\n```',
    'url': '[Home]({url:site.home})',
}
write('data/cases.json', json.dumps(CASES))
write('layouts/_partials/config-markdown/values.html', '{{ return (dict "custom.value" "[bad](https://evil.invalid/) {page.authors}" "site.home" .Page.Site.Home.Permalink) }}')
# Inspect the actual renderer results without HTML output escaping hiding mistakes.
write('layouts/probe.html', '''{{ $ctx := dict "Page" . "Owner" (partial "collection-owner.html" .) "Settings" (partial "sidera/settings.html" .) }}
{{ $results := dict "body" (.Content | string) }}
{{ range $name, $text := hugo.Data.cases }}{{ $results = merge $results (dict $name (partial "config-markdown/render.html" (merge $ctx (dict "Text" $text)))) }}{{ end }}
{{ $results = merge $results (dict "math" (partial "config-markdown/interpolate.html" (merge $ctx (dict "Text" "${page.authors}$")))) }}
{{ $results | jsonify | safeHTML }}''')


def build(name, failure=None):
    out = RUN / (name + '-public')
    p = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
                        '--cacheDir', str(RUN / 'cache'), '--noBuildLock', '--panicOnWarning',
                        '--printPathWarnings', '--printI18nWarnings'], capture_output=True,
                       text=True, timeout=120)
    (RUN / (name + '.log')).write_text(p.stdout + p.stderr)
    if failure:
        assert p.returncode and failure in p.stdout + p.stderr, (name, p.stdout, p.stderr)
    else:
        assert not p.returncode, (name, p.stdout, p.stderr)
    return out


class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.tags = []
        self.text = ''
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == 'a':
            self.links.append(dict(attrs)['href'])

    def handle_data(self, text):
        self.text += text


out = build('native')
read = lambda name: json.loads((out / 'notes' / name / 'index.html').read_text())
default, multiple, empty, hidden = [read(x) for x in ('default', 'multiple', 'empty', 'hidden')]
assert DOM(default['authors']).links == ['/preview/authors/editor/']
assert DOM(default['authors']).text.strip() == 'Editor'
assert DOM(multiple['authors']).links == ['/preview/people/ai-%28writer%29/', '/preview/authors/editor/']
assert DOM(multiple['authors']).text.strip() == HOSTILE + ', Editor'
assert set(DOM(multiple['authors']).tags) <= {'p', 'a'}
assert 'https://evil.invalid/' not in DOM(multiple['authors']).links
assert empty['authors'] == ''
assert DOM(hidden['authors']).text.strip() == HOSTILE  # Header visibility does not erase license credit.
assert json.loads((out / 'manual/intro/index.html').read_text())['authors'] == ''
assert (out / 'notes/authors/editor/index.html').is_file()  # Cascade-only native identity.
assert not (out / 'authors/_index.md').exists()
assert not (out / 'notes/authors/_index.md').exists()
for data in (default, multiple, empty, hidden):
    for key in ('body', 'code', 'escaped', 'fence'):
        assert '{page.authors}' in DOM(data[key]).text, (key, data[key])
    assert data['math'] == '${page.authors}$'
    assert '{unknown.value}' in data['unknown']
    assert not DOM(data['text']).links and '{page.authors}' in DOM(data['text']).text
    assert DOM(data['url']).links == ['https://example.invalid/preview/']
    assert DOM(data['repeated']).links == DOM(data['authors']).links * 2

# Rich linked text cannot be used as a URL or overridden via the string extension.
write('data/cases.json', json.dumps({'bad': '[bad]({url:page.authors})'}))
build('authors-url', 'page.authors is linked text, not a URL')
write('data/cases.json', json.dumps(CASES))
write('layouts/_partials/config-markdown/values.html', '{{ return (dict "page.authors" "Forged") }}')
build('reserved', 'must not replace built-in page.authors')
print('PASS: default/override/multiple/empty authors; native prefix/custom links; cascade routes; escaping/nonrecursive/code/math; rejected URL/override.')
