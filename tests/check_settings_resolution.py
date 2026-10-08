"""Native settings precedence and whole-value map construction in EN/ZH.
Run: python3 tests/check_settings_resolution.py /absolute/fresh-output-directory
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


def page(name, frontmatter):
    # JSON mappings are valid YAML; duplicate native source files for both languages.
    for suffix in ('.md', '.zh.md'):
        write('content/' + name + suffix, '---\n' + json.dumps(frontmatter) + '\n---\nBody.\n')


write('hugo.toml', f'''baseURL='https://example.invalid/'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
defaultContentLanguage='en'
[outputs]
home=['JSON']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[params]
icons=true
recent_count=10
taxonomy_navigation=['tags']
[params.profile]
title='Site profile'
text='Site text'
[params.tag_icons]
one='page'
[params.identity]
title='Site identity'
[languages.en]
weight=1
[languages.en.params]
byline='English site'
[languages.en.params.identity]
subtitle='English identity'
[languages.zh]
weight=2
locale='zh-CN'
[languages.zh.params]
byline='Chinese site'
[languages.zh.params.identity]
subtitle='Chinese identity'
''')
page('preset/custom/_index', {'title': 'Custom', 'params': {'defaults': {
    'params': {'show_updated': True, 'recent_count': 12},
    'cascade': {'params': {'byline': 'Preset child', 'icons': False,
                           'profile': {'title': 'Preset profile'}}},
}}})
page('notes/_index', {'title': 'Notes', 'preset': 'custom',
                      'params': {'byline': 'Ancestor only', 'recent_count': 7}})
page('notes/child', {'title': 'Child'})
page('notes/cleared', {'title': 'Cleared', 'params': {
    'byline': '', 'icons': False, 'profile': {}, 'tag_icons': {},
    'left': False, 'taxonomy_navigation': False,
}})
page('notes/branch/_index', {'title': 'Branch', 'cascade': {'params': {
    'byline': 'Native cascade', 'icons': True, 'profile': {'title': 'Cascade profile'},
}}})
page('notes/branch/child', {'title': 'Cascaded child'})
page('notes/stop/_index', {'title': 'Stop', 'preset': []})
page('notes/stop/child', {'title': 'Stopped child'})
page('plain', {'title': 'Plain'})
paths = ['/notes', '/notes/child', '/notes/cleared', '/notes/branch',
         '/notes/branch/child', '/notes/stop', '/notes/stop/child', '/plain']
write('data/settings_paths.json', json.dumps(paths))
write('layouts/home.json', '''{{ $results := collections.NewScratch }}
{{ range hugo.Data.settings_paths }}
  {{ $page := site.GetPage . }}{{ if not $page }}{{ errorf "missing fixture page %s" . }}{{ end }}
  {{ $before := $page.Params | jsonify }}
  {{ $settings := partial "sidera/settings.html" $page }}
  {{ $cached := partialCached "sidera/settings.html" $page $page.Language.Lang $page.Path }}
  {{ if ne ($settings | jsonify) ($cached | jsonify) }}{{ errorf "settings differ on cached call for %s" . }}{{ end }}
  {{ if ne ($page.Params | jsonify) $before }}{{ errorf "settings mutated page params for %s" . }}{{ end }}
  {{ $results.Set . $settings }}
{{ end }}{{ $results.Values | jsonify }}''')
result = subprocess.run([
    'hugo', '--source', str(SITE), '--destination', str(RUN / 'public'),
    '--cacheDir', str(RUN / 'cache'), '--noBuildLock', '--panicOnWarning',
    '--printPathWarnings', '--printI18nWarnings',
], capture_output=True, text=True, timeout=60)
(RUN / 'build.log').write_text(result.stdout + result.stderr)
assert not result.returncode, result.stdout + result.stderr
for language, output, label in [('en', 'index.json', 'English'), ('zh', 'zh/index.json', 'Chinese')]:
    settings = json.loads((RUN / 'public' / output).read_text())
    expected = {
        '/notes': {'byline': 'Ancestor only', 'recent_count': 7, 'show_updated': True},
        '/notes/child': {'byline': 'Preset child', 'icons': False, 'profile': {'title': 'Preset profile'}},
        '/notes/cleared': {'byline': '', 'icons': False, 'profile': {}, 'tag_icons': {},
                           'left': [], 'taxonomy_navigation': []},
        '/notes/branch': {'byline': 'Native cascade', 'icons': True, 'profile': {'title': 'Cascade profile'}},
        '/notes/branch/child': {'byline': 'Native cascade', 'icons': True, 'profile': {'title': 'Cascade profile'}},
    }
    for path in ['/notes/stop', '/notes/stop/child', '/plain']:
        expected[path] = {'byline': label + ' site', 'icons': True, 'recent_count': 10,
                          'profile': {'title': 'Site profile', 'text': 'Site text'}}
    for path, fields in expected.items():
        for key, value in fields.items():
            assert settings[path][key] == value, (language, path, key, settings[path][key], value)
        assert settings[path]['identity'] == {'title': 'Site identity', 'subtitle': label + ' identity'}
print('PASS', len(paths) * 2, 'native settings precedence/isolation cases')
