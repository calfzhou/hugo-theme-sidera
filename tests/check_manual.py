"""Optional manual, README examples, native links/publication/locales and notice delivery.
Run with a fresh absolute output directory; standard library, no network/provider calls.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, urljoin
import json, re, shutil, subprocess, sys

THEME = Path(__file__).resolve().parents[1]

class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.nodes=[]; self.feed(text)
    def handle_starttag(self, tag, attrs): self.nodes.append((tag, dict(attrs)))
    def cls(self, name): return [a for _,a in self.nodes if name in a.get('class','').split()]

def write(root, name, text):
    p=root/name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)

def main():
    run=Path(sys.argv[1]).resolve(); run.mkdir(parents=True, exist_ok=False)
    site=run/'site'; site.mkdir(); (site/'themes').mkdir()
    shutil.copytree(THEME, site/'themes/sidera', ignore=shutil.ignore_patterns('.git', '__pycache__'))
    readme=(THEME/'README.md').read_text()
    cfg=re.search(r'```toml\n(.*?)```', readme, re.S)[1]
    write(site, 'hugo.toml',cfg)
    examples=re.findall(r'```markdown\n(.*?)```',readme,re.S)
    assert len(examples)==2
    for path,body in zip(['content/notes/_index.md','content/notes/hello/index.md'],examples):write(site,path,body)
    sources=sorted((THEME/'docs/content').rglob('*.md'))
    assert all(len(p.relative_to(THEME/'docs/content').parts)<=3 for p in sources)
    assert all('  ai_label: generated\n' in p.read_text().split('---',2)[1] for p in sources)
    expected=[]
    for p in sources:
        rel=p.relative_to(THEME/'docs/content'); expected.append('/'+str(rel.parent if p.stem in ('index','_index') else rel.with_suffix('')).strip('.')+'/')
    expected=[re.sub('/+','/',x) for x in expected]
    # Serialize effective native values/order rather than infer cascade from source alone.
    write(site,'layouts/_partials/sidera/head-extra.html', '''<script type="application/json" id="manual-probe">{{ $s := partialCached "sidera/settings.html" .Page .Page.Language.Lang .Page.Path }}{{ dict "kind" .Page.Kind "ai" $s.ai_label "comments" $s.comments "logo" .Page.Params.logo "order" .Page.Params.children.order | jsonify | safeJS }}</script>''')
    results=[]
    def build(name, overlay=''):
        write(site,'probe.toml',overlay); out=run/(name+'-public')
        p=subprocess.run(['hugo','--source',str(site),'--config','hugo.toml,probe.toml','--destination',str(out),'--cacheDir',str(run/'cache'),'--noBuildLock','--panicOnWarning','--printPathWarnings','--printI18nWarnings'],text=True,capture_output=True,timeout=120)
        (run/(name+'.log')).write_text(p.stdout+p.stderr)
        assert not p.returncode,(name,p.stdout+p.stderr)
        results.append(name);return out
    def mounts(prefix):
        return "\n[[module.mounts]]\nsource='content'\ntarget='content'\n[[module.mounts]]\nsource='themes/sidera/docs/content'\ntarget='content/"+prefix+"'\n[[menus.primary]]\nname='Sidera manual'\npageRef='/"+prefix+"'\n[menus.primary.params]\nicon='sidera-bold-duotone'\n"
    def probe(text):return json.loads(re.search(r'<script[^>]+id="manual-probe"[^>]*>(.*?)</script>',text,re.S)[1])
    # Ordinary activation is README's exact example, without a docs mount/menu.
    off=build('disabled')
    assert (off/'notes/hello/index.html').exists()
    assert not any('Sidera user manual' in p.read_text() for p in off.rglob('*.html'))
    assert not (off/'manual').exists()
    assert '/manual/' not in (off/'sitemap.xml').read_text()
    assert 'Sidera manual' not in (off/'index.html').read_text()
    assert 'docs/content' not in (off/'sitemap.xml').read_text()
    for p in off.rglob('*.json'):
        assert 'Sidera user manual' not in p.read_text()
    def verify(out, prefix, base='', language='', label='AI-generated'):
        urls=[]; sections=0
        for suffix in expected:
            route='/'+('/'.join(x for x in [language,prefix] if x))+suffix
            file=out/route.lstrip('/')/'index.html';assert file.exists(),(out,route)
            text=file.read_text(); dom=DOM(text); data=probe(text)
            sections += data['kind']=='section'
            assert data['ai']=='generated' and data['comments'] is False,(route,data)
            assert label in text and dom.cls('ai-label'),route
            if data['order']:
                child_links=[a['href'].rstrip('/').split('/')[-1] for tag,a in dom.nodes if tag=='a' and 'card-title' in a.get('class','').split()]
                assert child_links==data['order'], (route,child_links,data['order'])
            assert not dom.cls('sidera-comments') and 'giscus.app/client.js' not in text
            assert 'img.shields.io' not in ' '.join(a.get('src','') for _,a in dom.nodes)
            assert not any('diagram-frame' in a.get('src','') for _,a in dom.nodes)
            urls.append(base+route)
            # Check real DOM links/resources and anchors, not escaped example strings.
            for tag,a in dom.nodes:
                target=a.get('href') if tag in ('a','link') else a.get('src') if tag in ('img','script') else None
                if not target:continue
                url=urlsplit(urljoin('https://example.org'+base+route,target))
                if url.scheme not in ('http','https') or url.netloc!='example.org':continue
                path=unquote(url.path)
                if base:
                    assert path.startswith(base+'/'),(route,target,path)
                    path=path[len(base):]
                dest=out/path.lstrip('/')
                if path.endswith('/'):dest=dest/'index.html'
                assert dest.is_file(),(route,target,dest)
                if url.fragment and dest.suffix=='.html':
                    ids={a.get('id') for _,a in DOM(dest.read_text()).nodes}
                    assert unquote(url.fragment) in ids,(route,target,'missing anchor')
        root=(out/('/'.join(x for x in [language,prefix] if x))/'index.html').read_text()
        assert probe(root)['logo']=='images/sidera-parallax-circle.svg'
        assert probe(root)['order']==['getting-started','organize','customize','authoring','reader','publishing']
        # Full six-child order in native immediate cards, not an assumed title sort.
        # Native markup may order attributes differently; DOM is stable.
        links=[a['href'] for tag,a in DOM(root).nodes if tag=='a' and 'card-title' in a.get('class','').split()]
        assert links, 'native child cards missing'
        assert [x.rstrip('/').split('/')[-1] for x in links]==probe(root)['order'],links
        index_files=list((out/'search').rglob('*.json'))
        assert index_files,'search index missing'
        indexes='\n'.join(p.read_text() for p in index_files)
        assert 'Contributing to Sidera' not in indexes and 'Code entry points' not in indexes
        assert 'Source code is data' in indexes or 'Sidera user manual' in indexes
        # All authored manual routes (not generated taxonomy helpers) remain exactly shallow.
        assert len(urls)==len(sources)
        assert sections==sum(p.name=='_index.md' for p in sources)
        for name,asset in [('LICENSE','sidera-mit.txt'),('THIRD-PARTY-NOTICES.md','sidera-third-party.txt')]:
            assert (out/'licenses'/asset).read_bytes()==(THEME/name).read_bytes()
            assert any(a.get('rel')=='license' and a.get('href','').endswith('/'+asset) for _,a in DOM(root).nodes)
        # README/agent/old root guidance are not published as source content.
        assert any(a.get('src','').endswith('/images/sidera-parallax-circle.svg') and a.get('alt')=='' for _,a in DOM((out/(language+'/' if language else '')/'index.html').read_text()).nodes)
        assert not any(p.name in ('AGENTS.md','README.md','CONTRACT.md') for p in out.rglob('*'))
    on=build('baseline',mounts('manual'));verify(on,'manual')
    global_comments=build('global-comments', '[params]\ncomments=true\n'+mounts('manual')); verify(global_comments,'manual')
    assert probe((global_comments/'notes/hello/index.html').read_text())['comments'] is True
    nested=build('nested',"baseURL='https://example.org/preview/'\n"+mounts('library/sidera'));verify(nested,'library/sidera',base='/preview')
    zh=build('chinese',"defaultContentLanguage='zh'\nlocale='zh-CN'\n"+mounts('manual'));verify(zh,'manual',label='由 AI 生成')
    bilingual="defaultContentLanguageInSubdir=true\n[languages.en]\nlocale='en-US'\nweight=1\n[languages.zh]\nlocale='zh-CN'\nweight=2\n"
    both=build('bilingual',bilingual+mounts('manual').replace('menus.primary','languages.en.menus.primary'));verify(both,'manual',language='en')
    assert not (both/'zh/manual/index.html').exists(),'unrequested body translation'
    catalog=(THEME/'i18n/zh-CN.toml').read_text()
    key=re.search(r'\[([^\]]+)\]\nother = "由 AI 生成"',catalog)[1]
    write(site,'i18n/zh-CN.toml',f'[{key}]\nother="Generated disclosure override"\n')
    custom=build('locale-override',"defaultContentLanguage='zh'\nlocale='zh-CN'\n"+mounts('manual'));verify(custom,'manual',label='Generated disclosure override')
    # Consumer article remains unlabeled and comment policy remains its own default.
    assert probe((on/'notes/hello/index.html').read_text())['ai']==''
    # Conditional real math/snippet sample and original bytes.
    example=(on/'manual/authoring/example/index.html').read_text()
    assert 'katex' in example and 'A simple sum' in example
    assert (on/'manual/authoring/example/sum.py').read_bytes()==(THEME/'docs/content/authoring/example/sum.py').read_bytes()
    # Literal demos must never execute providers, code inclusions or missing resources.
    shortcodes=(on/'manual/publishing/shortcodes/index.html').read_text()
    assert not DOM(shortcodes).cls('content-video') and 'data-snippet' not in shortcodes
    record={'passed':results,'manual_nodes':len(sources),'section_nodes':sum(p.name=='_index.md' for p in sources),'max_depth':max(len(p.relative_to(THEME/'docs/content').parts) for p in sources),'hugo':subprocess.check_output(['hugo','version'],text=True).strip()}
    (run/'results.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))

if __name__=='__main__':main()
