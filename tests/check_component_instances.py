"""Component schemas and copy-on-override settings, through native Hugo templates.
Run: python3 tests/check_component_instances.py /absolute/fresh-output-directory
"""
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


write('hugo.toml', f'''baseURL='https://example.invalid/'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['taxonomy','term','RSS','sitemap','404']
[outputs]
home=['JSON']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
''')
base = {
    'icons': True, 'menu': 'primary', 'links_menu': 'side',
    'article_links_menu': 'article', 'footer_menu': 'footer',
    'taxonomy_navigation': ['tags'], 'tag_icons': {'one': 'page'},
    'recent_count': 10, 'references': ['Reference'], 'license': 'License',
    'share': ['link'],
    'profile': {'title': 'Base', 'text': 'Body', 'image': '', 'menu': 'primary'},
}
cases = [
    ('unchanged', 'left', 'menu', {}),
    ('false-and-empty', 'left', {'component': 'menu', 'config': {
        'icons': False, 'menu': '', 'taxonomies': False}},
        {'icons': False, 'menu': '', 'taxonomy_navigation': []}),
    ('clear-map', 'left', {'component': 'taxonomies', 'config': {'tag_icons': {}}},
        {'tag_icons': {}}),
    ('profile-fields', 'left', {'component': 'profile', 'config': {'title': '', 'text': ''}},
        {'profile': {'title': '', 'text': '', 'image': '', 'menu': 'primary'}}),
    ('side-links', 'left', {'component': 'links', 'config': {'menu': 'custom'}},
        {'links_menu': 'custom'}),
    ('article-links', 'article-footer', {'component': 'links', 'config': {'menu': 'custom'}},
        {'article_links_menu': 'custom'}),
    ('site-links', 'site-footer', {'component': 'links', 'config': {'menu': 'custom'}},
        {'footer_menu': 'custom', 'icons': False}),
    ('site-links-explicit-icons', 'site-footer', {'component': 'links', 'config': {'icons': True}}, {}),
    ('clear-references', 'article-footer', {'component': 'references', 'config': {'entries': []}},
        {'references': []}),
    ('disable-license', 'article-footer', {'component': 'license', 'config': {'text': False}},
        {'license': False}),
    ('empty-config', 'left', {'component': 'menu', 'config': {}}, {}),
    ('unchanged-after-overrides', 'left', 'menu', {}),
]
write('data/cases.json', json.dumps([
    {'name': name, 'region': region, 'entry': entry, 'want': {**base, **overrides}}
    for name, region, entry, overrides in cases
]))
write('data/base.json', json.dumps(base))
write('layouts/home.json', '''{{ $base := hugo.Data.base }}{{ $before := $base | jsonify }}
{{ $passed := slice }}
{{ range hugo.Data.cases }}
  {{ $got := partial "sidera/instance.html" (dict "Entry" .entry "Region" .region "Page" site.Home "Settings" $base) }}
  {{ if ne ($got.Settings | jsonify) (.want | jsonify) }}
    {{ errorf "instance %s: got %s want %s" .name ($got.Settings | jsonify) (.want | jsonify) }}
  {{ end }}
  {{ if ne ($base | jsonify) $before }}{{ errorf "instance %s mutated shared settings" .name }}{{ end }}
  {{ $passed = $passed | append .name }}
{{ end }}{{ $passed | jsonify }}''')
result = subprocess.run([
    'hugo', '--source', str(SITE), '--destination', str(RUN / 'public'),
    '--cacheDir', str(RUN / 'cache'), '--noBuildLock', '--panicOnWarning',
    '--printPathWarnings', '--printI18nWarnings',
], capture_output=True, text=True, timeout=60)
(RUN / 'build.log').write_text(result.stdout + result.stderr)
assert not result.returncode, result.stdout + result.stderr
passed = json.loads((RUN / 'public/index.json').read_text())
assert len(passed) == len(cases)
print('PASS', len(passed), 'component schema/settings isolation cases')
