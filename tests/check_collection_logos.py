"""Collection-local logo/identity rendering and strict native asset boundaries.
Run: python3 tests/check_collection_logos.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Logo tests'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
''')
SVG='<svg xmlns="http://www.w3.org/2000/svg" width="120" height="60"><rect width="120" height="60" fill="#369"/></svg>'
write('static/logo.svg',SVG);write('assets/shared.svg',SVG)
for folder,preset,name,logo in [('notes','notes','Field notes','/logo.svg'),('docs','docs','Handbook','shared.svg'),('blog','blog','',''),('clear','notes','Notes',''),('custom','','Custom','/logo.svg')]:
 write(f'content/{folder}/_index.md','---\ntitle: "Full '+folder+' title"\ndescription: "Summary '+folder+'"\n'+('preset: '+preset+'\n' if preset else '')+'params:\n  name: '+json.dumps(name)+'\n  logo: '+json.dumps(logo)+'\n---\n')
 write(f'content/{folder}/article.md','---\ntitle: Article '+folder+'\n---\nBody.\n')
write('content/notes/nested/_index.md','---\ntitle: Independent collection\npreset: notes\nparams:\n  scope_root: true\n  name: Nested\n  logo: logo.svg\n---\n')
write('content/notes/nested/logo.svg',SVG)
class DOM(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,t,a):self.nodes.append((t,dict(a)))
 def cls(self,cls):return [a for t,a in self.nodes if cls in a.get('class','').split()]
passed=[];rejected=[]
def build(label,diagnostic=None,overlay=''):
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr);rejected.append(label)
 else:assert not p.returncode,(label,p.stdout+p.stderr);passed.append(label)
 return out
for label,overlay,prefix in [('baseline','',''),('icons-off','[params]\nicons=false\n',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n",''),('subpath',"baseURL='https://example.invalid/preview/'\n",'/preview')]:
 out=build(label,overlay=overlay);home=(out/'index.html').read_text();d=DOM(home)
 logos=d.cls('collection-logo');assert len(logos)==4 and all(a['alt']=='' for a in logos)
 assert {a['src'] for a in logos}=={prefix+'/logo.svg',prefix+'/shared.svg',prefix+'/notes/nested/logo.svg'}
 assert 'Full notes title' in home and 'Summary notes' in home and 'Field notes' in home
 assert 'Field notes · '+('笔记' if label=='chinese' else 'notes') in home
 if label!='chinese':assert 'Notes · notes' not in home
 expected_icons=0 if label=='icons-off' else 2
 assert len(re.findall(r'<span class="collection-emblem"><svg\b',home))==expected_icons
 assert sum('has-logo' not in a.get('class','') for a in d.cls('collection-emblem'))==2
 if label=='icons-off':assert not any(t=='svg' for t,_ in d.nodes)
 large=DOM((out/'preset/notes/index.html').read_text()).cls('collection-card-logo');assert len(large)==2
 assert all(a['alt']=='' and a['width']=='96' for a in large)
 assert len(DOM((out/'preset/docs/index.html').read_text()).cls('collection-card-logo'))==1
 assert not DOM((out/'notes/article/index.html').read_text()).cls('collection-card-logo')
 assert (out/'shared.svg').read_bytes()==(SITE/'assets/shared.svg').read_bytes()
 assert (out/'notes/nested/logo.svg').read_bytes()==(SITE/'content/notes/nested/logo.svg').read_bytes()
# Validate explicit clearing and literal identity labels.
p=SITE/'content/notes/_index.md';original=p.read_text();p.write_text(original.replace('"/logo.svg"','""'))
out=build('clear');assert len(DOM((out/'index.html').read_text()).cls('collection-logo'))==3
p.write_text(original.replace('Field notes','<img src=x onerror=bad()>'))
out=build('escaped');assert not any(t=='img' and a.get('src')=='x' for t,a in DOM((out/'index.html').read_text()).nodes);p.write_text(original)
cases=[('type','params:\n  logo: false\n','string'),('missing','params:\n  logo: missing.svg\n','missing local image'),('remote','params:\n  logo: https://example.invalid/logo.svg\n','local image'),('data','params:\n  logo: data:image/svg+xml,x\n','local image'),('traversal','params:\n  logo: ../logo.svg\n','local image'),('extension','params:\n  logo: file.txt\n','local image'),('query','params:\n  logo: /logo.svg?v=1\n','local image'),('namespace','logo: /logo.svg\n','belongs under params'),('cascade','cascade:\n  params:\n    logo: /logo.svg\n','do not cascade')]
for name,fm,diagnostic in cases:
 path='content/bad-'+name+'/_index.md';write(path,'---\ntitle: Invalid\n'+fm+'---\n');build('bad-'+name,diagnostic);write(path,'---\ntitle: Repaired\n---\n')
for name,path,text,diag in [('page','content/bad-page.md','params:\n  logo: /logo.svg\n','collection root'),('nested','content/docs/branch/_index.md','params:\n  logo: /logo.svg\n','collection root'),('draft','content/bad-draft/_index.md','draft: true\nparams:\n  logo: []\n','string'),('preset','content/preset/bad/_index.md','params:\n  defaults:\n    params:\n      logo: /logo.svg\n','preset parameter logo')]:
 write(path,'---\ntitle: Invalid\n'+text+'---\n');build(name,diag);write(path,'---\ntitle: Repaired\n---\n')
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'theme':str(THEME),'noNetwork':True},indent=2)+'\n');print('PASS',len(passed),'builds /',len(rejected),'expected logo rejections;',RUN)
