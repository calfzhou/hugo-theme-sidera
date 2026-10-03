"""Collection cards show latest native member activity, never root metadata.
Run: python3 tests/check_collection_dates.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Collection activity'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[frontmatter]
date=['date']
publishDate=['publishDate','date']
lastmod=['lastmod','date']
''')
def page(path,title,metadata=''):
 write('content/'+path,'---\ntitle: '+title+'\n'+metadata+'---\nBody.\n')
for preset in ['notes','blog','docs']:
 page(preset+'/_index.md',preset.title(),'preset: '+preset+'\nlastmod: 2028-01-01T00:00:00Z\n')
 page(preset+'/old.md','Old','date: 2024-01-01T00:00:00Z\nlastmod: 2024-02-01T00:00:00Z\n')
 page(preset+'/chapter/_index.md','Chapter','lastmod: 2027-01-01T00:00:00Z\n')
 page(preset+'/chapter/latest.md','Deep latest','date: 2024-01-02T00:00:00Z\nlastmod: 2024-06-01T15:00:00Z\n')
 page(preset+'/offset.md','Earlier timezone','date: 2024-01-03T00:00:00Z\nlastmod: 2024-06-01T22:00:00+08:00\n')
 page(preset+'/undated.md','Undated')
 page(preset+'/draft.md','Draft','draft: true\ndate: 2024-01-01T00:00:00Z\nlastmod: 2029-01-01T00:00:00Z\n')
 page(preset+'/future.md','Future','date: 2099-01-01T00:00:00Z\n')
 page(preset+'/expired.md','Expired','date: 2000-01-01T00:00:00Z\nexpiryDate: 2001-01-01T00:00:00Z\nlastmod: 2029-01-01T00:00:00Z\n')
 page(preset+'/headless/index.md','Headless','headless: true\ndate: 2024-01-01T00:00:00Z\nlastmod: 2029-01-01T00:00:00Z\n')
page('notes/independent/_index.md','Independent','preset: notes\nparams:\n  scope_root: true\n')
page('notes/independent/new.md','Independent latest','date: 2025-01-01T00:00:00Z\n')
page('empty/_index.md','Empty','preset: notes\nlastmod: 2028-01-01T00:00:00Z\n')
page('undated/_index.md','Undated collection','preset: notes\n')
page('undated/entry.md','No date')
page('fallback/_index.md','Publication fallback','preset: notes\n')
page('fallback/entry.md','Only publication','publishDate: 2024-03-01T00:00:00Z\n')
page('hidden/_index.md','Hidden update','preset: notes\nparams:\n  show_updated: false\n')
page('hidden/entry.md','Hidden update article','date: 2024-04-01T00:00:00Z\n')
class Cards(HTMLParser):
 def __init__(self,text):super().__init__();self.current=None;self.cards={};self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='li' and 'article-card' in a.get('class','').split():self.current={'dates':[],'spans':0,'text':''}
  if self.current is not None:
   if tag=='a' and a.get('class')=='card-title':self.current['href']=a['href']
   if tag=='span' and a.get('class')=='card-date':self.current['spans']+=1
   if tag=='time':self.current['dates'].append(a)
 def handle_data(self,text):
  if self.current is not None:self.current['text']+=text
 def handle_endtag(self,tag):
  if tag=='li' and self.current is not None:
   self.cards[self.current['href']]=self.current;self.current=None
passed=[]
for label,overlay,prefix in [('baseline','',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n",''),('subpath',"baseURL='https://example.invalid/preview/'\n",'/preview'),('icons-off','[params]\nicons=false\n',''),('lastmod-only',"[frontmatter]\nlastmod=['lastmod']\n",'')]:
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
 def cards(route):return Cards((out/route/'index.html').read_text()).cards
 for preset in ['notes','blog','docs']:
  collection=cards('preset/'+preset)[prefix+'/'+preset+'/']
  assert collection['spans']==1 and len(collection['dates'])==1
  assert collection['dates'][0]['class']=='modified'
  assert datetime.fromisoformat(collection['dates'][0]['datetime'].replace('Z','+00:00'))==datetime.fromisoformat('2024-06-01T15:00:00+00:00')
  assert ('更新于' if label=='chinese' else 'Updated') in collection['text'],collection
  for name in ['draft','future','expired','headless']:assert not (out/preset/name/'index.html').exists()
 notes=cards('preset/notes')
 for name in ['empty','undated','hidden']:
  c=notes[prefix+'/'+name+'/'];assert c['spans']==0 and not c['dates'];assert '不详' not in c['text'] and 'unknown' not in c['text'].lower()
 for route,date in [('fallback','2024-03-01T00:00:00+00:00'),('notes/independent','2025-01-01T00:00:00+00:00')]:
  assert datetime.fromisoformat(notes[prefix+'/'+route+'/']['dates'][0]['datetime'].replace('Z','+00:00'))==datetime.fromisoformat(date)
 # Regular article cards keep per-page published/updated priority and undated fallback.
 for root,date in [('blog','2024-01-01T00:00:00+00:00'),('notes','2024-02-01T00:00:00+00:00')]:
  c=cards(root)[prefix+'/'+root+'/old/'];assert datetime.fromisoformat(c['dates'][0]['datetime'].replace('Z','+00:00'))==datetime.fromisoformat(date)
  undated=cards(root)[prefix+'/'+root+'/undated/'];assert undated['spans']==1 and not undated['dates']
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'presetKinds':3,'scopeAndPublicationBoundaries':True,'rootDatesIgnored':True,'emptyUndatedAndHiddenOmitDate':True,'publicationFallback':True,'regularArticlePolicyPreserved':True},indent=2)+'\n');print('PASS collection dates:',', '.join(passed))
