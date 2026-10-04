"""Blog/notes section defaults; owner views, article exclusion and explicit overrides."""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
''')
scopes={'notes':'notes','other-notes':'notes','blog':'blog','docs':'docs','plain':None,'off':'notes','empty':'notes','custom':'notes','unclassified':'notes'}
for root,preset in scopes.items():
 fm=('preset: '+preset+'\n' if preset else '')+'params:\n  page_size: 1\n'
 if root=='off':fm+='  top: false\n'
 if root=='empty':fm+='  top: []\n'
 if root=='custom':fm+='  top:\n    - component: collection-nav\n      config:\n        items: [archive, tags, recent]\n'
 write(f'content/{root}/_index.md','---\ntitle: '+root+'\n'+fm+'---\nCollection.\n')
 for i in range(2):
  fields='' if root=='unclassified' else 'tags: [shared]\ncategories: [category]\n'
  write(f'content/{root}/entry-{i}.md',f'---\ntitle: Entry {i}\ndate: 2024-01-0{i+1}\n{fields}---\nArticle.\n')
write('content/about.md','---\ntitle: About\n---\nStandalone.\n')
class Tabs(HTMLParser):
 def __init__(self,text):super().__init__();self.active=False;self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='nav' and 'data-collection-nav' in a:self.active=True
  if self.active and tag=='a':self.links.append({'href':a['href'],'current':a.get('aria-current'),'text':''})
 def handle_data(self,text):
  if self.active and self.links:self.links[-1]['text']+=text
 def handle_endtag(self,tag):
  if tag=='nav':self.active=False
passed=[]
for label,overlay,prefix in [('english','',''),('chinese-subpath',"defaultContentLanguage='zh'\nlocale='zh-CN'\nbaseURL='https://example.invalid/preview/'\n",'/preview')]:
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60);(RUN/(label+'.log')).write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
 for root in scopes:
  tabs=Tabs((out/root/'index.html').read_text()).links
  if root in ['docs','plain','off','empty']:assert not tabs,root;continue
  parts=['','categories/','tags/','archives/']
  if root=='custom':parts=['archives/','tags/','']
  if root=='unclassified':parts=['','archives/']
  expected=[prefix+'/'+root+'/'+part for part in parts];assert [a['href'] for a in tabs]==expected,(label,root,tabs)
  labels={'':'全部文章' if prefix else 'All posts','categories/':'分类' if prefix else 'Categories','tags/':'标签' if prefix else 'Tags','archives/':'归档' if prefix else 'Archive'}
  assert [a['text'] for a in tabs]==[labels[x] for x in parts]
  for suffix,current,state in [('', '', 'page'),('page/2/', '', 'page'),('tags/','tags/','page'),('tags/shared/','tags/','location'),('categories/','categories/','page'),('archives/','archives/','page')]:
   if current not in parts:continue
   path=out/root/suffix/'index.html';assert path.exists(),path
   links=Tabs(path.read_text()).links;assert [a['href'] for a in links]==expected,(root,suffix,links)
   selected=[(a['href'],a['current']) for a in links if a['current']];assert selected==[(prefix+'/'+root+'/'+current,state)],(root,suffix,selected)
  if root in ['notes','other-notes']:assert 'data-list-order="modification"' in (out/root/'index.html').read_text()
 for root in scopes:assert not Tabs((out/root/'entry-0/index.html').read_text()).links,root
 assert not Tabs((out/'about/index.html').read_text()).links and not Tabs((out/'index.html').read_text()).links
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'notes_blog_defaults':True,'articles_docs_plain_unaffected':True,'overrides_and_owner_states':True},indent=2)+'\n');print('PASS notes/blog top-bar defaults, owner browsing states, empty vocabularies, overrides and EN/ZH/subpath')
