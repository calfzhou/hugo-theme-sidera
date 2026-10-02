"""Automatic captions are standalone-only, not Markdown table cell/header labels.
Run: python3 tests/check_table_images.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Table captions'
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
SVG='<svg xmlns="http://www.w3.org/2000/svg" width="80" height="40"><rect width="80" height="40" fill="orange"/></svg>'
write('content/check/image.svg',SVG)
BODY=r'''---
title: Images in tables
---
![Standalone|80](image.svg "Standalone caption")

Inline ![Inline](image.svg "Inline tooltip") text.

| ![Header](image.svg "Header tooltip") | Value |
| :--- | ---: |
| ![One](image.svg "Cell tooltip") | one |
| Text ![Mixed](image.svg) text | two |
| ![First](image.svg) ![Second](image.svg) | three |
| [![Linked](image.svg "Linked tooltip")](../target/index.md#target) | four |
| `![Literal](image.svg)` | **Bold** and [link](../target/index.md) |
{#native-table .source-linebreaks data-probe="ok" title="quoted & value" onclick="bad()"}

{{% folding title="Nested table" %}}
| Image | Text |
| --- | :---: |
| ![Nested](image.svg "Nested tooltip") | A table inside a fold |
{{% /folding %}}

> ![Quote image](image.svg "Quote caption")

{{< image src="image.svg" alt="Explicit image" caption="Authored caption" >}}
'''
write('content/check/index.md',BODY)
write('content/target/index.md','---\ntitle: Target\n---\n## Target\n')
class DOM(HTMLParser):
 void={'img','br','hr','input','link','meta','source','area','embed','param','col','wbr'}
 def __init__(self,text):super().__init__();self.stack=[];self.nodes=[];self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);table=any(tag=='table' for tag in self.stack);self.nodes.append((t,a,table))
  if t not in self.void:self.stack.append(t)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i]==t:self.stack=self.stack[:i];break
passed=[]
for label,overlay,prefix,caption_count in [('baseline','','',3),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n",'',3),('subpath',"baseURL='https://example.invalid/preview/'\n",'/preview',3),('auto-off','[params]\nauto_caption=false\n','',1)]:
 write('probe.toml',overlay);out=RUN/(label+'-public')
 result=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(result.stdout+result.stderr);assert not result.returncode,result.stdout+result.stderr
 raw=(out/'check/index.html').read_text();d=DOM(raw)
 assert not any(t in ('figure','figcaption') and table for t,_,table in d.nodes)
 assert sum(t=='figcaption' for t,_,_ in d.nodes)==caption_count
 images=[a for t,a,table in d.nodes if t=='img' and table];assert len(images)==7,(label,images)
 assert {a['alt'] for a in images}=={'Header','One','Mixed','First','Second','Linked','Nested'}
 one=next(a for a in images if a['alt']=='One');assert one['title']=='Cell tooltip'
 assert next(a for t,a,_ in d.nodes if t=='img' and a.get('alt')=='Standalone')['width']=='80'
 assert all(a['src']==prefix+'/check/image.svg' for a in images)
 assert any(t=='a' and a.get('href')==prefix+'/target/#target' and table for t,a,table in d.nodes)
 table=next(a for t,a,_ in d.nodes if t=='table' and a.get('id')=='native-table')
 assert table['class']=='source-linebreaks' and table['data-probe']=='ok' and table['title']=='quoted & value'
 assert not any('onclick' in a for _,a,_ in d.nodes)
 assert any(a.get('style')=='text-align: right' for t,a,_ in d.nodes if t in ('th','td'))
 assert '<strong>Bold</strong>' in raw and '![Literal](image.svg)' in raw
 assert (out/'check/image.svg').read_bytes()==(SITE/'content/check/image.svg').read_bytes()
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'tableImageCount':7,'automaticTableCaptions':0,'standaloneInlineAndExplicitBehaviorPreserved':True},indent=2)+'\n');print('PASS 4 native table-image cases: captions, resources, sizes, links, alignment/attributes, C2 nesting and overrides;',RUN)
