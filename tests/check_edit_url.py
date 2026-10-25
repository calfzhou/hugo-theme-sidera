"""Source-aware edit links: native files, mounts, overrides and safe destinations.
Run: python3 tests/check_edit_url.py /absolute/fresh-output
"""
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
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


def page(name, params=None, body='## Source\n\nA source-editing example.\n', **meta):
    write(name, '---\n' + json.dumps({'title': 'Edit this source', 'date': '2026-01-01T00:00:00Z',
                                   'params': params or {}, **meta}) + '\n---\n' + body)


REPO = 'https://github.com/example/site/blob/main/content/'
DOCS = 'https://github.com/example/docs/blob/docs-branch/'
mappings = [{'path': '', 'url': REPO}, {'path': 'notes/Guides/', 'url': DOCS},
            {'path': 'notes/Guides/private/', 'url': ''},
            {'path': 'notes/guides/', 'url': 'https://example.invalid/wrong-case/'},
            {'path': 'manual/', 'url': 'https://github.com/example/theme/blob/main/docs/content/'}]
base = {
    'baseURL': 'https://example.invalid/preview/', 'title': 'Edit link checks',
    'theme': THEME.name, 'themesDir': str(THEME.parent), 'disableKinds': ['RSS'],
    'languages': {'en': {'weight': 1}, 'zh': {'weight': 2, 'locale': 'zh-CN'}},
    'taxonomies': {'_merge': 'shallow'}, 'permalinks': {'term': {'_merge': 'shallow'}},
    'outputs': {'home': ['HTML', 'JSON']},
    'module': {'mounts': [{'source': 'content', 'target': 'content'},
                          {'source': 'external-docs', 'target': 'content/manual'}]},
    'params': {'comments': False, 'page_reveal': False, 'left': False, 'right': ['toc'], 'comment_provider': 'fixture',
               'article_footer': ['share'], 'share': ['link', 'wechat', 'email'], 'edit_url': mappings},
}
for suffix in ['', '.zh']:
    page('content/notes/_index' + suffix + '.md')
    page('content/notes/plain' + suffix + '.md', {'comments': True}, url=('/zh' if suffix else '') + '/published-name/')
    page('content/notes/bundle/index' + suffix + '.md')
    page('content/notes/Guides/_index' + suffix + '.md')
    page('content/notes/Guides/Case' + suffix + '.md')
    page('content/notes/Guides/private/hidden' + suffix + '.md')
    page('content/notes/Guides-other/no-prefix-collision' + suffix + '.md')
    page('content/guides-lower/no-case-folding' + suffix + '.md')
    page('content/notes/cleared' + suffix + '.md', {'edit_url': ''})
    page('content/notes/empty-array' + suffix + '.md', {'edit_url': []})
    page('content/notes/hidden' + suffix + '.md', {'show_authors': False}, authors=['Ada'])
    page('content/notes/edit-only' + suffix + '.md', {'share': False, 'show_authors': False}, authors=['Ada'])
    page('content/notes/edit-only-empty' + suffix + '.md', {'share': []})
    page('content/notes/no-actions' + suffix + '.md', {'share': False, 'edit_url': ''})
    page('content/notes/literal' + suffix + '.md', {'edit_url': 'https://example.net/edit?file=one&mode=two'})
    page('content/notes/instance' + suffix + '.md', {'right': [
        {'component': 'toc', 'config': {'edit_url': [{'path': 'notes/', 'url': DOCS}]}},
        {'component': 'toc', 'config': {'icons': False, 'edit_url': ''}}, 'edit-widget']})
    page('content/notes/cascade/_index' + suffix + '.md', cascade={'params': {'edit_url': [{'path': 'notes/cascade/', 'url': DOCS}]}})
    page('content/notes/cascade/child' + suffix + '.md')
    page('content/notes/nohead' + suffix + '.md', body='A page without headings.')
    page('content/notes/nohead-none' + suffix + '.md', {'edit_url': ''}, body='No headings or edit link.')
    page('content/notes/comments-only' + suffix + '.md', {'edit_url': '', 'comments': True}, body='Only the discussion action.')
    page('external-docs/_index' + suffix + '.md')
    page('external-docs/install' + suffix + '.md')
encoded = 'notes/中文 +#%&.md'
page('content/' + encoded, url='/encoded/')
base['params']['widgets'] = {'edit-widget': {'component': 'toc', 'config': {'edit_url': [{'path': '', 'url': DOCS}]}}}
# A local provider exercises the actual comments-slot/HasComments path without any network service.
write('layouts/_partials/comments/providers/fixture.html', '<p>Local discussion fixture.</p>')
# Observe native identity and the resolver separately from sidebar eligibility.
write('layouts/home.json', '''{{ $rows := slice }}
{{ range site.Pages }}
  {{ $settings := partial "sidera/settings.html" . }}
  {{ $file := "" }}{{ $adapter := false }}{{ with .File }}{{ $file = .Path }}{{ $adapter = .IsContentAdapter }}{{ end }}
  {{ $url := partial "sidera/edit-url.html" (dict "Page" . "Settings" $settings) }}
  {{ $rows = $rows | append (dict "file" $file "adapter" $adapter "url" $url "route" .RelPermalink) }}
{{ end }}{{ $rows | jsonify }}''')


class Edits(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'toc-edit' in attrs.get('class', '').split():
            self.links.append(attrs)


def build(label, cfg, diagnostic=None):
    write('hugo.json', json.dumps(cfg))
    out = RUN / (label + '-public')
    result = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
                             '--cacheDir', str(RUN / (label + '-cache')), '--noBuildLock',
                             '--minify', '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings'],
                            capture_output=True, text=True, timeout=60)
    log = result.stdout + result.stderr
    (RUN / (label + '.log')).write_text(log)
    if diagnostic:
        assert result.returncode and diagnostic in log, (label, log)
    else:
        assert not result.returncode, (label, log)
    return out


for label, icons in [('baseline', True), ('icons-off', False), ('root-reordered', True), ('drawers', True)]:
    cfg = deepcopy(base)
    cfg['params']['icons'] = icons
    if label in ('drawers', 'icons-off'):
        cfg['params']['left'] = ['menu']
        cfg['menus'] = {'primary': [{'name': 'Home', 'pageRef': '/'}]}
    if label == 'root-reordered':
        cfg['baseURL'] = 'https://example.invalid/'
        cfg['params']['edit_url'].reverse()
    out = build(label, cfg)
    for lang in ['', 'zh/']:
        rows = json.loads((out / lang / 'index.json').read_text())
        assert any(not r['file'] for r in rows)
        assert any(r['adapter'] for r in rows)
        for row in rows:
            source, url = row['file'], row['url']
            expected = REPO + quote(source, safe='/') if source else ''
            if source.startswith('notes/Guides/'):
                expected = DOCS + quote(source.removeprefix('notes/Guides/'), safe='/')
            if source.startswith('notes/Guides/private/') or '/cleared' in source or '/empty-array' in source or '/no-actions' in source or '/nohead-none' in source or '/comments-only' in source:
                expected = ''
            if source.startswith('manual/'):
                expected = 'https://github.com/example/theme/blob/main/docs/content/' + source.removeprefix('manual/')
            if source.startswith('notes/cascade/'):
                expected = DOCS + source.removeprefix('notes/cascade/')
            if '/literal' in source:
                expected = 'https://example.net/edit?file=one&mode=two'
            if row['adapter']:
                expected = ''
            assert url == expected, (row, expected)
            route = row['route'].removeprefix('/preview/').strip('/')
            html = (out / route / 'index.html').read_text()
            links = Edits(html).links
            # Regular files exercise the actual sidebar; generated fileless pages resolve no mapped URL.
            if source.startswith('notes/') and '/_index' not in source:
                if not expected:
                    assert not links, row
                elif '/instance' in source:
                    assert [a['href'] for a in links] == [DOCS + source.removeprefix('notes/'), DOCS + source]
                else:
                    assert len(links) == 1 and links[0]['href'] == expected, (row, links)
                    assert links[0]['target'] == '_blank'
                    assert set(links[0]['rel'].split()) == {'noopener', 'noreferrer'}
                    assert ('编辑本文' if lang else 'Edit this article') in html
                assert 'footer-authors' not in html and 'author-list' not in html and 'article-edit' not in html
                if '/nohead.' in source:
                    assert 'class=article-toc' not in html and 'class=toc-top' in html and 'class=toc-edit' in html
                if '/nohead-none' in source:
                    assert 'class=toc-footer' not in html and 'id=right-region' not in html
                if '/comments-only' in source:
                    assert 'class=toc-comments' in html and 'class=toc-edit' not in html
                if '/edit-only' in source:
                    assert 'share-action ' not in html and 'share-qr' not in html
                    assert 'article-footer-share-1-heading' not in html
                if '/no-actions' in source:
                    assert 'article-share' not in html and 'article-footer-box' not in html
                if '/hidden' in source or '/edit-only.' in source:
                    assert 'header-assigned-authors' not in html
                if not icons:
                    assert '<svg' not in html
    assert Edits((out / 'encoded/index.html').read_text()).links[0]['href'] == REPO + quote(encoded, safe='/')

# No matching edit link and no share targets must leave no empty row or box.
cfg = deepcopy(base)
cfg['params']['edit_url'] = [{'path': 'unmatched/', 'url': DOCS}]
cfg['params']['share'] = False
out = build('unmatched', cfg)
assert 'article-share' not in (out / 'published-name/index.html').read_text()
assert 'article-footer-box' not in (out / 'published-name/index.html').read_text()
# Footer selection is independent; selecting/omitting the TOC controls the edit action.
cfg = deepcopy(base)
del cfg['params']['article_footer']
out = build('default-footer', cfg)
assert Edits((out / 'published-name/index.html').read_text()).links
for label, footer in [('omitted', ['license']), ('disabled', False)]:
    cfg['params']['article_footer'] = footer
    out = build(label, cfg)
    assert Edits((out / 'published-name/index.html').read_text()).links
for label, right in [('no-sidebar', False), ('no-toc', ['text'])]:
    cfg['params']['right'] = right
    out = build(label, cfg)
    assert not Edits((out / 'published-name/index.html').read_text()).links

bad = [
    (False, 'edit_url must be'), ({'notes/': REPO}, 'edit_url must be'),
    ([42], 'path/url records'), ([{'path': 'notes/'}], 'require path and url strings'),
    ([{'path': '', 'url': 1}], 'require path and url strings'),
    ([{'path': '', 'url': REPO, 'extra': True}], 'unknown edit_url mapping field'),
    ([{'path': '../', 'url': REPO}], 'content-relative directory'),
    ([{'path': '/notes/', 'url': REPO}], 'content-relative directory'),
    ([{'path': 'notes', 'url': REPO}], 'content-relative directory'),
    ([{'path': 'notes//nested/', 'url': REPO}], 'content-relative directory'),
    ([{'path': 'notes/./', 'url': REPO}], 'content-relative directory'),
    ([{'path': 'notes\\bad/', 'url': REPO}], 'content-relative directory'),
    ([{'path': '', 'url': REPO}, {'path': '', 'url': ''}], 'duplicate edit_url path'),
    ([{'path': '', 'url': 'javascript:alert(1)'}], 'unsafe URL'),
    ([{'path': '', 'url': '//example.org/'}], 'unsafe URL'),
    ([{'path': '', 'url': '/local/'}], 'absolute HTTP(S) directory'),
    ([{'path': '', 'url': REPO.rstrip('/')}], 'absolute HTTP(S) directory'),
    ([{'path': '', 'url': REPO + '?query/'}], 'absolute HTTP(S) directory'),
    ([{'path': '', 'url': REPO + '#fragment/'}], 'absolute HTTP(S) directory'),
]
for index, (value, diagnostic) in enumerate(bad):
    cfg = deepcopy(base)
    cfg['params']['edit_url'] = value
    build('reject-' + str(index), cfg, diagnostic)
# Validate hidden draft and unused widget values too, not only rendered links.
page('content/draft.md', {'edit_url': [{'path': '../', 'url': REPO}]}, draft=True)
build('reject-draft', base, 'content-relative directory')
page('content/draft.md', draft=True)
cfg = deepcopy(base)
cfg['params']['widgets']['unused'] = {'component': 'toc', 'config': {'edit_url': [{'path': '', 'url': 'javascript:x'}]}}
build('reject-widget', cfg, 'unsafe URL')
print('PASS edit URLs: native paths/bundles/sections/translations/mounts, encoding, longest prefix, exclusions, overrides, instances, sidebar order/eligibility, no duplicate footer link, EN/ZH/icons-off and validation')
