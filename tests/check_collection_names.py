"""Local collection identity vs full native title/description; no site fixture dependency.
Run: python3 tests/check_collection_names.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
CONFIG=f'''baseURL='https://example.invalid/'
title='Name checks'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[params]
left=['collections']
'''
write('hugo.toml',CONFIG)
for folder,preset,name,title in [('notes','notes','Notes','A long notebook title'),('journal','blog','Journal','A long blog title'),('docs','docs','Docs','A long documentation title'),('custom','', 'Custom','An independent unpreset root'),('fallback','notes','','Title fallback')]:
 fm='---\ntitle: '+json.dumps(title)+'\nlinkTitle: '+json.dumps('Native breadcrumb '+folder)+'\ndescription: '+json.dumps('Summary for '+folder)+'\n'
 if preset:fm+='preset: '+preset+'\n'
 fm+='params:\n  left: [collections, page-tree]\n'
 if name:fm+='  name: '+json.dumps(name)+'\n'
 fm+='cascade:\n  params:\n    left: [collections, page-tree]\n---\n'
 write('content/'+folder+'/_index.md',fm)
 write('content/'+folder+'/article/index.md','---\ntitle: "Full article '+folder+'"\ntags: [shared]\n---\n## Article heading\n\nA body.\n')
write('content/notes/nested/_index.md','---\ntitle: A nested independent collection\nparams:\n  scope_root: true\n  name: Nested\n---\n')
write('content/notes/nested/entry.md','---\ntitle: Nested full article\n---\nNested body.\n')
write('content/standalone.md','---\ntitle: A standalone page\n---\nNo collection name.\n')
class DOM(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
 def byid(self,id):return next(a for _,a in self.nodes if a.get('id')==id)
passed=[];rejected=[]
def build(label,diagnostic=None,overlay=''):
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr);rejected.append(label)
 else:assert not p.returncode,(label,p.stdout+p.stderr);passed.append(label)
 return out
for label,overlay in [('baseline',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n"),('global-not-inherited','[params]\nname="NOT A COLLECTION NAME"\n')]:
 out=build(label,overlay=overlay)
 for folder,name in [('notes','Notes'),('journal','Journal'),('docs','Docs'),('custom','Custom'),('fallback','Title fallback')]:
  root=(out/folder/'index.html').read_text();article=(out/folder/'article/index.html').read_text();dom=DOM(article)
  assert name in dom.byid('search-input')['placeholder']
  assert name in dom.byid('search-input')['aria-label']
  assert '<h1>Full article '+folder+'</h1>' in article
  if folder!='fallback':assert 'data-collection-link href="/'+folder+'/">'+name+'</a>' in article
  else:assert '>Native breadcrumb fallback</a>' in article
  expected_title={'notes':'A long notebook title','journal':'A long blog title','docs':'A long documentation title','custom':'An independent unpreset root','fallback':'Title fallback'}[folder]
  assert '<h1>'+expected_title+'</h1>' in root
  assert 'class="tree-root"' in article and '>'+name+'</a>' in article
  if folder=='docs':assert 'data-navigation="parent"' in article and '<span>Docs</span>' in article
  assert 'Summary for '+folder in (out/'index.html').read_text()
  assert 'NOT A COLLECTION NAME' not in article
 assert 'Nested' in DOM((out/'notes/nested/entry/index.html').read_text()).byid('search-input')['placeholder']
 docs=json.loads(next((out/'search').glob('*.json')).read_text())['documents']
 for doc in docs:
  if doc['url']=='/notes/article/':assert doc['title']=='Full article notes' and doc['context']=='Notes'
  if doc['url']=='/notes/':assert doc['title']=='A long notebook title' and doc['context']=='Notes'
  if doc['url']=='/notes/nested/entry/':assert doc['context']=='Nested'
 assert '>Notes</a>' in (out/'tags/shared/index.html').read_text()
 # Search has no collection owner for root-level standalone pages.
 assert 'Title fallback' not in DOM((out/'standalone/index.html').read_text()).byid('search-input')['placeholder']
# Escaped name and explicit blank fallbacks do not mutate the native title.
p=SITE/'content/notes/_index.md';original=p.read_text()
p.write_text(original.replace('name: "Notes"','name: "<img src=x onerror=bad()> & Notes"'))
out=build('escaped');raw=(out/'notes/article/index.html').read_text();assert not any(t=='img' and a.get('src')=='x' for t,a in DOM(raw).nodes);assert '&lt;img' in raw
p.write_text(original.replace('name: "Notes"','name: "   "'))
out=build('blank');assert 'A long notebook title' in DOM((out/'notes/article/index.html').read_text()).byid('search-input')['placeholder'];assert '>Native breadcrumb notes</a>' in (out/'notes/article/index.html').read_text()
p.write_text(original)
# Local identity cannot become inherited metadata or a preset default.
cases=[('number','content/negative/_index.md','---\ntitle: Negative\nparams:\n  name: 42\n---\n','must be a string'),('bool','content/negative/_index.md','---\ntitle: Negative\nparams:\n  name: false\n---\n','must be a string'),('top-level','content/negative/_index.md','---\ntitle: Negative\nname: Wrong namespace\n---\n','belongs under params'),('page','content/negative/index.md','---\ntitle: Negative\nparams:\n  name: Wrong kind\n---\n','collection root'),('nested','content/notes/branch/_index.md','---\ntitle: Shared branch\nparams:\n  name: Not independent\n---\n','collection root'),('cascade','content/negative/_index.md','---\ntitle: Negative\ncascade:\n  params:\n    name: Leaked\n---\n','do not cascade'),('draft','content/negative/_index.md','---\ntitle: Negative\ndraft: true\nparams:\n  name: []\n---\n','must be a string'),('preset','content/preset/unused/_index.md','---\ntitle: Unused preset\nparams:\n  defaults:\n    params:\n      name: Same for everybody\n---\n','preset parameter name')]
for label,path,text,diagnostic in cases:
 path=path.replace('content/negative/','content/negative-'+label+'/')
 write(path,text);build(label,diagnostic);write(path,'---\ntitle: Repaired fixture\n---\n')
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'theme':str(THEME)},indent=2)+'\n');print('PASS',len(passed),'builds /',len(rejected),'expected name rejections;',RUN)
