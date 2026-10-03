"""Preset/root/descendant/global left defaults and recent ordering/scope boundaries.
Run: python3 tests/check_leftbar_defaults.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Leftbar defaults'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[frontmatter]
date=['date']
lastmod=['lastmod','date']
''')
for folder in ('notes','blog','docs'):
 write(f'content/{folder}/_index.md',f'---\ntitle: {folder.title()}\npreset: {folder}\n---\n')
 for i in range(7):
  write(f'content/{folder}/n{i}.md',f'---\ntitle: {folder} {i}\ndate: 2024-01-0{i+1}\nlastmod: 2024-02-0{7-i}\ntags: [shared/child]\ncategories: [category]\n'+('params:\n  pinned: true\n' if i==3 else '')+'---\nBody.\n')
write('content/docs/chapter/_index.md','---\ntitle: Chapter\ndate: 2024-03-01\nlastmod: 2024-04-01\n---\nChapter.\n')
write('content/notes/independent/_index.md','---\ntitle: Independent root\nparams:\n  scope_root: true\n---\n')
write('content/notes/independent/new.md','---\ntitle: New independent page\ndate: 2025-11-01\nlastmod: 2025-11-01\n---\n')
write('content/custom/_index.md','---\ntitle: Unpreset\n---\n')
write('content/custom/entry.md','---\ntitle: Custom entry\ndate: 2025-10-01\n---\n')
write('content/standalone.md','---\ntitle: Latest standalone\ndate: 2025-12-01\n---\n')
class DOM(HTMLParser):
 def __init__(self,text):super().__init__();self.lists=[];self.stack=[];self.taxonomies=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='ul':
   index=None
   if 'data-recent' in a:index=len(self.lists);self.lists.append({'order':a['data-recent'],'id':a['id'],'hrefs':[]})
   self.stack.append(index)
  if tag=='a' and self.stack and self.stack[-1] is not None:self.lists[self.stack[-1]]['hrefs'].append(a['href'])
  if tag=='nav' and a.get('data-tree-scope')=='owner':self.taxonomies.append(a.get('aria-label'))
 def handle_endtag(self,tag):
  if tag=='ul':self.stack.pop()
def read(out,route):
 raw=(out/route.strip('/')/'index.html').read_text();return raw,DOM(raw)
passed=[];rejected=[]
def build(label,overlay='',diagnostic=None):
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr);rejected.append(label)
 else:assert not p.returncode,(label,p.stdout+p.stderr);passed.append(label)
 return out
for label,overlay,prefix in [('baseline','',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\nbaseURL='https://example.invalid/preview/'\n",'/preview')]:
 out=build(label,overlay)
 for folder,components,orders in [('notes',['menu','taxonomies','recent'],['publication']),('blog',['menu','recent'],['modification']),('docs',['menu','page-tree','recent','recent'],['modification','publication'])]:
  for route in [f'/{folder}/',f'/{folder}/n0/',f'/{folder}/tags/shared/child/']:
   raw,d=read(out,route);assert re.findall(r'data-component="([^"]+)" data-instance="left-[^"]+"',raw)==components,(route,raw[:200])
   assert [x['order'] for x in d.lists]==orders,(route,d.lists)
   assert len({x['id'] for x in d.lists})==len(d.lists)
   assert d.taxonomies==(['标签' if label=='chinese' else 'Tags'] if folder=='notes' else []),(route,d.taxonomies)
   for recent in d.lists:
    seq=list(range(6,-1,-1)) if recent['order']=='publication' else list(range(7))
    paths=[f'{prefix}/{folder}/n{i}/' for i in seq]
    if folder=='docs':paths.insert(0,prefix+'/docs/chapter/')
    assert recent['hrefs']==paths[:5],(route,recent,paths[:5])
  # Collection header has no redundant browse-tags CTA; native hubs survive.
  root=read(out,f'/{folder}/')[0]
  assert 'class="view-tools"' not in root and '浏览标签 →' not in root and 'Browse tags →' not in root
  assert (out/folder/'tags/index.html').is_file()
  if folder=='notes':assert 'data-list-order="modification"' in read(out,'/notes/')[0]
 # Minimal/global default stays non-scoped even within an unpreset root.
 for route in ['/','/standalone/','/custom/','/custom/entry/']:
  raw,d=read(out,route);assert len(d.lists)==1 and d.lists[0]['order']=='modification'
  assert d.lists[0]['hrefs'][:3]==[prefix+'/standalone/',prefix+'/notes/independent/new/',prefix+'/custom/entry/'],(route,d.lists)
  assert len(d.lists[0]['hrefs'])==5
# Explicit per-instance scope: same renderer, no global owner mutation.
write('content/probe.md','''---
title: Instance scope probe
params:
  left:
    - component: recent
      config: {scope: global, order: publication, count: 2}
---
''')
out=build('instance');assert read(out,'/probe/')[1].lists[0]['hrefs']==['/standalone/','/notes/independent/new/']
# Existing opt-out/custom composition semantics remain authoritative.
out=build('disabled','[cascade.params]\nleft=false\n');assert not read(out,'/notes/n0/')[1].lists
for n,value in enumerate(['"bad"','true','2','["global"]']):
 build('invalid-scope-'+str(n),'[params.widgets.unused]\ncomponent="recent"\n[params.widgets.unused.config]\nscope='+value+'\n', 'config.scope')
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'theme':str(THEME),'recentDefaultCount':5,'globalRegularPages':True,'notesMainOrder':'modification'},indent=2)+'\n');print('PASS',len(passed),'builds /',len(rejected),'expected scope rejections;',RUN)
