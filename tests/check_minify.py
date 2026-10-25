"""Deferred head/footer whitespace and native HTML minification, using native resource minification.
Usage: python3 tests/check_minify.py /absolute/fresh-output-directory [minified-site-output]
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
SITE = RUN / 'site'
assert not RUN.exists(), 'Use a fresh output directory'
SITE.mkdir(parents=True)


def write(name, text):
    path = SITE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.assets = []
        self.nodes = []
        self.pre = []
        self.stack = []
        self.gaps = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if tag == 'pre':
            self.pre.append('')
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(tag)
        if (tag == 'script' and 'src' in attrs) or tag == 'link':
            self.assets.append((tag, attrs))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index] == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        if 'pre' in self.stack:
            self.pre[-1] += data
        if not set(self.stack) & {'pre', 'textarea', 'script', 'style'} and not data.strip(' \t\r\n\f'):
            if re.search(r'\n[ \t]+|\n\s*\n|[ \t]{2,}', data):
                self.gaps.append((tuple(self.stack), data))


def audit_output(out):
    files = list(out.rglob('*.html'))
    assert files, ('Missing HTML output', out)
    for file in files:
        assert not HTML(file.read_text()).gaps, ('Excess markup whitespace', file)
    assert not (out / 'sidera-internal').exists(), 'Internal fragments must not publish'
    return len(files)


write('hugo.toml', f'''baseURL='https://example.invalid/preview/'
title='Minification checks'
theme={json.dumps(THEME.name)}
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[params]
jsx=true
article_footer=['terms','references','outgoing','backlinks','license','share','series','text','links','meta']
share=['link','wechat','weibo','email']
show_updated=true
edit_url='/preview/'
references=['Words **stay** separate.']
article_text='Footer **words** stay separate.'
article_links_menu='footer-test'
[[menus.footer-test]]
name='Two words'
url='/preview/'
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[markup.goldmark.parser.attribute]
_merge='shallow'
[markup.goldmark.extensions.passthrough]
_merge='deep'
''')
code = 'first line\n\n    indented line\n\nlast line\n'
write('content/ordinary.md', '---\ntitle: Ordinary\ndate: 2026-01-01T00:00:00Z\nauthors: [Ada Reader]\nseries: [Reading notes]\ntags: [space sensitive, second]\ncategories: [examples]\n---\nWords **stay** separate. [Features](features.md).\n\n```text\n' + code + '```\n')
write('content/features.md', '''---
title: Features
date: 2026-01-02T00:00:00Z
authors: [Ada Reader]
series: [Reading notes]
tags: [third]
---
Inline math $x^2$.

```jsx-live {mode="sandbox"}
export default function Example(){return <p>Ready</p>;}
```

```jsx-live
export default function Other(){return <p>Page mode</p>;}
```
''')


def build(label, flags):
    out = RUN / label
    result = subprocess.run([
        'hugo', '--source', str(SITE), '--destination', str(out),
        '--cacheDir', str(RUN / 'cache'), '--noBuildLock', '--panicOnWarning',
        '--printPathWarnings', '--printI18nWarnings', *flags,
    ], text=True, capture_output=True, timeout=90)
    (RUN / (label + '.log')).write_text(result.stdout + result.stderr)
    assert result.returncode == 0, result.stdout + result.stderr
    return out


# Deliberately verbose consumer markup: fixes must operate on rendered fragments,
# not depend on the formatting of today's built-in templates.
write('layouts/_partials/sidera/article-footer-extra.html', """
<div data-whitespace-probe="{{ .Page.Title }}">

    <p><span>one</span> <span>two</span></p>

    <pre>first line

    indented line

last line</pre>
    <textarea>first line

    indented line

last line</textarea>
</div>
""")
plain = build('plain', [])
mini = build('minified', ['--minify'])
audit_output(mini)
for file in mini.rglob('*.html'):
    text = file.read_text()
    original = (plain / file.relative_to(mini)).read_text()
    assert HTML(text).assets == HTML(original).assets, file
    assert HTML(text).pre == HTML(original).pre, file

ordinary = (mini / 'ordinary/index.html').read_text()
assert code.rstrip('\n') in HTML(ordinary).pre, 'Preserve code indentation and empty lines'
assert 'Words <strong>stay</strong> separate.' in ordinary
assert 'data-sidera-search' in ordinary
for component in ('terms', 'references', 'outgoing', 'license', 'share', 'series', 'text', 'links', 'meta'):
    assert any(a.get("data-footer-item") == component for _, a in HTML(ordinary).nodes), component
assert 'Footer <strong>words</strong> stay separate.' in ordinary
assert '<span>one</span> <span>two</span>' in ordinary
assert '<textarea>' + code.rstrip('\n') + '</textarea>' in ordinary
assert 'assigned-tags' in ordinary and 'assigned-categories' in ordinary
assert '<span>space sensitive</span>' in ordinary
assert '<span>third</span>' not in ordinary
features = (mini / 'features/index.html').read_text()
assert 'data-sidera-math' in features and 'data-sidera-jsx-script' in features
for text, title in [(ordinary, 'Ordinary'), (features, 'Features')]:
    assert [a['data-whitespace-probe'] for _, a in HTML(text).nodes if 'data-whitespace-probe' in a] == [title], 'Fragment cache isolation'
# Rebuild with changed custom markup into another fresh destination, reusing cache.
hook = SITE / 'layouts/_partials/sidera/article-footer-extra.html'
hook.write_text(hook.read_text().replace('<span>two</span>', '<span>changed</span>'))
updated = build('updated-hook', ['--minify'])
assert '<span>one</span> <span>changed</span>' in (updated / 'ordinary/index.html').read_text()
write('off.toml', '[params]\nsearch=false\nsearch_index=false\n')
off = build('search-off', ['--minify', '--config', 'hugo.toml,off.toml'])
head = (off / 'ordinary/index.html').read_text().split('<head>', 1)[1].split('</head>', 1)[0]
assert 'data-sidera-search' not in head
assert not re.search(r'\n[ \t]*\n', head)
if len(sys.argv) > 2:
    print('PASS minified artifact whitespace:', audit_output(Path(sys.argv[2]).resolve()), 'HTML files including frames')
print('PASS native minification: pages/frames, verbose custom hooks, cache isolation, assets, search on/off, math/JSX, inline/pre/textarea whitespace')
