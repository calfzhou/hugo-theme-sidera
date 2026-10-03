"""List Markdown images are caption-free, including inside C2 grid/fold containers.
Run: python3 tests/check_list_images.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='List images'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
''')
write('content/check/image.svg','<svg xmlns="http://www.w3.org/2000/svg" width="80" height="40"><rect width="80" height="40" fill="orange"/></svg>')
write('content/check/index.md','''---
title: Lists and images
---
![Before](image.svg "Standalone before")

3. ![Ordered|80x40](image.svg "AUTO_ONLY_LIST_CAPTION")
4. ![Pair A](image.svg) ![Pair B](image.svg)

- ![Bullet](image.svg)
- Text ![Inline](image.svg) text
- [![Linked](image.svg)](../target/index.md)

1. Loose paragraph

   ![Loose|80](image.svg "LOOSE_ONLY_CAPTION")
   {.invert-when-dark #loose-image}

   - ![Nested](image.svg)

2. Another paragraph

   ![Loose second](image.svg)

- [ ] ![Task](image.svg)

{{% grid columns=2 %}}
{{< cell >}}
1. ![Grid](image.svg "GRID_ONLY_CAPTION")
{{< /cell >}}
{{< cell >}}
5. ![Grid pair A](image.svg) ![Grid pair B](image.svg)
{{< /cell >}}
{{% /grid %}}

{{% folding title="Folded list" %}}
- ![Fold](image.svg)
{{% /folding %}}

- Explicit image follows:

  {{< image src="image.svg" alt="Explicit" caption="Explicit caption" >}}

- Explicit native figure follows:

  {{< figure src="image.svg" caption="Native caption" >}}

- Literal: `<li><figure class="md-figure"><img><figcaption>literal</figcaption></figure></li>`

![After](image.svg "Standalone after")

> ![Quote](image.svg "Quote caption")

| Image |
| --- |
| ![Table](image.svg "TABLE_ONLY_CAPTION") |
''')
write('content/target/index.md','---\ntitle: Target\ntags: [list-probe]\n---\nTarget.\n')
for path in ['content/_index.md','content/collection/_index.md','content/tags/list-probe/_index.md']:
 write(path,'---\ntitle: List body\n'+('slug: list-probe\n' if '/tags/' in path else '')+'---\n- ![Body image](/check/image.svg "BODY_ONLY_CAPTION")\n')
# Exercise the shared output boundary independently: lists, opaque elements and
# comments are tokenized without altering their bytes; explicit figures survive.
write('layouts/_partials/sidera/head-extra.html','''{{ $page := site.GetPage "/check" }}{{ $configured := partial "config-markdown/render.html" (dict "Page" $page "Text" `- ![Configured](image.svg "CONFIG_ONLY_CAPTION")`) }}{{ if strings.Contains (string $configured) "<figcaption>" }}{{ errorf "Config Markdown list caption" }}{{ end }}
{{ $figure := `<figure class="md-figure"><img src="x" alt="x"><figcaption>auto</figcaption></figure>` }}
{{ $opaque := printf `<!-- <li>%s</li> --><script>let x='<li>%s</li>';</script><template><li>%s</li></template>` $figure $figure $figure }}
{{ $input := printf `%s<ol><li>%s<ul><li>%s</li></ul>%s</li></ol>%s` $opaque $figure $figure $figure $figure }}
{{ $want := printf `%s<ol><li><img src="x" alt="x"><ul><li><img src="x" alt="x"></li></ul><img src="x" alt="x"></li></ol>%s` $opaque $figure }}
{{ $got := string (partial "images/list-captions.html" $input) }}
{{ if ne $got $want }}{{ errorf "List filter boundary mismatch" }}{{ end }}
{{ if ne (string (partial "images/list-captions.html" $got)) $got }}{{ errorf "List filter not idempotent" }}{{ end }}
''')
class DOM(HTMLParser):
 void={'img','br','hr','input','link','meta','source','area','embed','param','col','wbr'}
 def __init__(self,text):super().__init__();self.stack=[];self.nodes=[];self.feed(text)
 def handle_starttag(self,t,a):
  a=dict(a);self.nodes.append((t,a,tuple(self.stack)))
  if t not in self.void:self.stack.append(t)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i]==t:self.stack=self.stack[:i];break
passed=[]
for label,overlay,prefix,captions in [('baseline','','',5),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n",'',5),('subpath',"baseURL='https://example.invalid/preview/'\n",'/preview',5),('auto-off','[params]\nauto_caption=false\n','',2)]:
 write('probe.toml',overlay);out=RUN/(label+'-public')
 result=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(result.stdout+result.stderr);assert not result.returncode,result.stdout+result.stderr
 raw=(out/'check/index.html').read_text();d=DOM(raw)
 assert not any(t=='figure' and a.get('class')=='md-figure' and 'li' in stack for t,a,stack in d.nodes)
 assert sum(t=='figcaption' for t,_,_ in d.nodes)==captions,(label,captions)
 images=[a for t,a,stack in d.nodes if t=='img' and 'li' in stack]
 assert len(images)==16,(label,len(images))
 ordered=next(a for a in images if a.get('alt')=='Ordered');assert ordered['width']=='80' and ordered['height']=='40' and ordered['title']=='AUTO_ONLY_LIST_CAPTION'
 loose=next(a for a in images if a.get('alt')=='Loose');assert loose['id']=='loose-image' and loose['class']=='invert-when-dark' and loose['width']=='80'
 assert all(a['src']==prefix+'/check/image.svg' for a in images if a.get('alt')!='')
 assert any(t=='ol' and a.get('start')=='3' for t,a,_ in d.nodes)
 assert any(t=='a' and a.get('href')==prefix+'/target/' and 'li' in stack for t,a,stack in d.nodes)
 assert 'Explicit caption' in raw and 'Native caption' in raw
 assert '&lt;li&gt;' in raw and 'literal' in raw
 search=''.join(p.read_text() for p in (out/'search').glob('*.json'))
 assert search and all(s not in search for s in ['AUTO_ONLY_LIST_CAPTION','LOOSE_ONLY_CAPTION','GRID_ONLY_CAPTION','TABLE_ONLY_CAPTION'])
 assert 'Explicit caption' in search and 'Native caption' in search
 for route in ['index.html','collection/index.html','tags/list-probe/index.html']:
  body=(out/route).read_text();assert '<figcaption>BODY_ONLY_CAPTION</figcaption>' not in body and 'alt="Body image"' in body,route
 assert (out/'check/image.svg').read_bytes()==(SITE/'content/check/image.svg').read_bytes()
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'listImages':16,'automaticListFigures':0,'searchCaptionsAbsent':True,'explicitAndStandalonePreserved':True},indent=2)+'\n');print('PASS native list image checks:',', '.join(passed))
