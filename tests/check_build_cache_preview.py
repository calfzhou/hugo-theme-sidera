"""Owned live preview: recent-cache scope/date/count and search body/rule freshness.
Only isolated fixture files are edited. Explicit free port; always stop own server.
"""
from pathlib import Path
from html.parser import HTMLParser
import json,os,re,socket,subprocess,sys,time,urllib.request
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
PORT=int(os.environ.get('SIDERA_PREVIEW_PORT','14845'));BASE=f'http://127.0.0.1:{PORT}'
def write(path,text):
 p=SITE/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='{BASE}/'
title='Cache freshness'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[frontmatter]
date=['date']
lastmod=['lastmod','date']
''')
root='---\ntitle: Notes\npreset: notes\nparams:\n  recent_count: 2\ncascade:\n  params:\n    recent_count: 2\n---\nRoot.\n';write('content/notes/_index.md',root)
a='---\ntitle: A\ndate: 2024-01-01\n---\nBodyOldToken.\n';b='---\ntitle: B\ndate: 2024-02-01\n---\nBody B.\n'
write('content/notes/a.md',a);write('content/notes/b.md',b)
nested='---\ntitle: Nested\nparams:\n  scope_root: true\n---\n';write('content/notes/nested/_index.md',nested)
write('content/notes/nested/c.md','---\ntitle: C\ndate: 2025-01-01\n---\nNested C.\n')
write('content/standalone.md','---\ntitle: Global\ndate: 2026-01-01\n---\nStandalone.\n')
write('data/sidera_discovery.json',(THEME/'data/sidera_discovery.json').read_text())
class Recent(HTMLParser):
 def __init__(self,text):super().__init__();self.active=False;self.links=[];self.feed(text)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='ul' and a.get('data-recent')=='publication':self.active=True
  if self.active and t=='a':self.links.append(a.get('href'))
 def handle_endtag(self,t):
  if t=='ul':self.active=False

def get(path):
 with urllib.request.urlopen(BASE+path,timeout=3) as r:return r.read().decode()
def state():
 html=get('/notes/a/');match=re.search(r'data-index="([^"]+)"',html)
 if not match:raise ValueError('Waiting for complete rebuilt HTML')
 return Recent(html).links,json.loads(get(match[1]))['documents']
def wait(check):
 last=None
 for _ in range(150):
  try:
   last=state()
   if check(*last):return last
  except (OSError,ValueError,AttributeError):pass
  time.sleep(.15)
 raise AssertionError(('preview stale',last))
probe=socket.socket();probe.bind(('127.0.0.1',PORT));probe.close();log=(RUN/'preview.log').open('w')
proc=subprocess.Popen(['hugo','server','--source',str(SITE),'--bind','127.0.0.1','--port',str(PORT),'--baseURL',BASE+'/','--disableFastRender','--noHTTPCache','--destination',str(RUN/'public'),'--cacheDir',str(RUN/'cache')],stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'GOMAXPROCS':'2'})
checks=[]
try:
 wait(lambda links,docs:links==['/notes/b/','/notes/a/']);checks.append('initial owner order')
 write('content/notes/a.md',a.replace('2024-01-01','2024-03-01').replace('BodyOldToken','BodyNewToken'))
 wait(lambda links,docs:links==['/notes/a/','/notes/b/'] and 'BodyNewToken' in json.dumps(docs) and 'BodyOldToken' not in json.dumps(docs));checks.append('date reorder and body refresh')
 write('content/notes/_index.md',root.replace('recent_count: 2','recent_count: 1'))
 wait(lambda links,docs:links==['/notes/a/']);checks.append('cascaded count')
 write('content/notes/nested/_index.md',nested.replace('scope_root: true','scope_root: false'))
 wait(lambda links,docs:links==['/notes/nested/c/']);checks.append('nested ownership boundary change')
 write('content/notes/nested/c.md','---\ntitle: C\ndate: 2025-01-01\ndraft: true\n---\nNested C.\n')
 wait(lambda links,docs:links==['/notes/a/'] and not any(d['url']=='/notes/nested/c/' for d in docs));checks.append('publication exclusion')
 write('content/notes/d.md','---\ntitle: D\ndate: 2024-12-01\n---\nAdded D.\n')
 wait(lambda links,docs:links==['/notes/d/']);checks.append('new article membership')
 rules=json.loads((THEME/'data/sidera_discovery.json').read_text());rules['skipTags'].append('p');write('data/sidera_discovery.json',json.dumps(rules))
 wait(lambda links,docs:'BodyNewToken' not in json.dumps(docs));checks.append('changed discovery rules with unchanged source body')
 rules['skipTags'].remove('p');write('data/sidera_discovery.json',json.dumps(rules))
 wait(lambda links,docs:'BodyNewToken' in json.dumps(docs));checks.append('restored rules')
 (RUN/'results.json').write_text(json.dumps({'passed':checks},indent=2)+'\n');print('PASS',len(checks),'live build-cache freshness cases')
finally:
 proc.terminate()
 try:proc.wait(timeout=10)
 except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)
 log.close();probe=socket.socket();probe.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);probe.bind(('127.0.0.1',PORT));probe.close()
