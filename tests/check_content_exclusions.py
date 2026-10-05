"""Native exclusions apply to source discovery, not just final HTML publication.
Run with a fresh output directory; no dependencies or user/editor processes.
"""
from pathlib import Path
import json, os, subprocess, sys
THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
RUN.mkdir(parents=True, exist_ok=False)
results = []

def case(name, policy, *, flags=(), bad='', alternate=False, bilingual=False, links=False, environment=None, overlay=''):
    site = RUN/name/'site'; site.mkdir(parents=True)
    def write(path, text):
        p = site/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)
    root = 'writing' if alternate else 'content'
    config = f'''baseURL='https://example.invalid/'
theme={json.dumps(THEME.name)}
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
{policy}
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[outputs]
page=['HTML','Plain']
[mediaTypes.'text/markdown']
suffixes=['md']
[outputFormats.Plain]
mediaType='text/markdown'
isPlainText=true
baseName='index'
'''
    if bilingual:
        config += "[languages.en]\nweight=1\n[languages.zh]\nweight=2\n"
    write('hugo.toml', config)
    if overlay:
        write('excludes.toml', overlay)
        flags = [*flags, '--config', 'hugo.toml,excludes.toml']
    write('layouts/_default/single.plain.md', '{{ .RawContent }}')
    def page(path, title, meta='', body='PUBLIC_BODY'):
        write(root+'/'+path, '---\ntitle: '+title+'\n'+meta+'---\n'+body+'\n')
    page('notes/_index.md', 'Notes', 'preset: notes\n')
    page('notes/a.md', 'Alpha', 'tags: [topic]\n', '[Beta](b.md)')
    page('notes/b.md', 'Beta', 'tags: [topic]\n')
    page('notes/bundle/index.md', 'Bundle')
    write(root+'/notes/bundle/code.txt', 'PUBLIC_RESOURCE')
    # These fail native Markdown parsing or theme metadata validation if inspected.
    secret = '---\ntitle: PRIVATE_SENTINEL\ntags: [[invalid]]\n---\n{{< unknown-secret-shortcode >}}\n'
    for directory in ['.obsidian', '_templates', 'vault-only', 'notes/cache']:
        for filename in ['private.md', 'private.txt', 'settings.json']:
            write(root+'/'+directory+'/'+filename, secret)
    for path in ['notes/tags.md', 'tags/topic/_index.md', 'notes/ignored.md']:
        write(root+'/'+path, secret)
    if alternate:
        # A same-name physical source outside the native mount must not shadow it.
        write('content/notes/a.md', secret)
    if bilingual:
        page('notes/_index.zh.md', '笔记', 'preset: notes\n')
        page('notes/a.zh.md', '甲', 'tags: [topic]\n', '[乙](b.md)')
        page('notes/b.zh.md', '乙', 'tags: [topic]\n')
    if links:
        outside=RUN/'symlink-target';outside.mkdir(exist_ok=True)
        (outside/'secret.md').write_text(secret)
        (site/root/'linked').symlink_to(outside, target_is_directory=True)
        (site/root/'notes/linked.md').symlink_to(outside/'secret.md')
    if bad:
        page('notes/bad.md', 'Bad', 'tags: [[invalid]]\n'+('draft: true\n' if bad=='draft' else ''))
    out=RUN/name/'public'
    p=subprocess.run(['hugo','--source',str(site),'--destination',str(out),
        '--cacheDir',str(RUN/name/'cache'),'--noBuildLock','--panicOnWarning',*flags],
        capture_output=True,text=True,timeout=60,env={**os.environ,'GOMAXPROCS':'2',**(environment or {})})
    (RUN/name/'build.log').write_text(p.stdout+p.stderr)
    if bad:
        assert p.returncode and 'tag' in p.stderr.lower(), (name,p.stdout,p.stderr)
        results.append({'case':name,'included_invalid_rejected':bad});return
    assert p.returncode==0,(name,p.stdout,p.stderr)
    for path in out.rglob('*'):
        if path.is_file():
            assert b'PRIVATE_SENTINEL' not in path.read_bytes(),(name,path)
            assert not any(part in ['.obsidian','_templates','vault-only','cache','linked'] for part in path.relative_to(out).parts),(name,path)
    for prefix in ['','zh/'] if bilingual else ['']:
        assert (out/prefix/'notes/a/index.html').exists()
        assert (out/prefix/'notes/b/index.md').read_text().strip()=='PUBLIC_BODY'
        assert (out/prefix/'tags/topic/index.html').exists(), 'Excluded term must not shadow native inference'
        text=(out/prefix/'notes/a/index.html').read_text()
        assert '/notes/b/' in text and 'reference-list' in text
    assert (out/'notes/bundle/code.txt').read_text()=='PUBLIC_RESOURCE'
    assert not (out/'notes/ignored').exists()
    results.append({'case':name,'html_plain_resources_indexes':True})

ignore="ignoreFiles=['(^|/)(_templates|vault-only|cache)(/|$)', 'notes/(tags|ignored)\\.md$', 'tags/topic/_index\\.md$']"
patterns=['! _templates{,/**}', '! vault-only{,/**}', '! notes/cache{,/**}',
          '! notes/tags.md', '! notes/ignored.md', '! tags/topic/_index.md']
def mounts(root='content', extra=()):
    return '[[module.mounts]]\nsource='+json.dumps(root)+'\ntarget="content"\nfiles='+json.dumps(patterns+list(extra))+'\n'
case('ignore-only', ignore)
case('mount-only', mounts())
case('mount-inclusions', mounts(extra=['notes/**']))
case('config-overlay', '', overlay=ignore)
case('environment-ignore', '', environment={'HUGO_IGNOREFILES': '(^|/)(_templates|vault-only|cache)(/|$)|notes/(tags|ignored)\\.md$|tags/topic/_index\\.md$'})
case('all-states', ignore, flags=['--buildDrafts','--buildFuture','--buildExpired'])
case('bilingual', ignore, bilingual=True)
case('alternate-mount', mounts('writing'), alternate=True)
case('symlinks', ignore, links=True)
case('included-invalid', ignore, bad='published')
case('included-invalid-draft', ignore, bad='draft')
(RUN/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS',len(results),'native discovery/exclusion cases')
