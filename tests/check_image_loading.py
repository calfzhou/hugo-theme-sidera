"""Native image loading defaults/overrides; all image contexts, no runtime loader.
Run: python3 tests/check_image_loading.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Image loading'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
''')
SVG='<svg xmlns="http://www.w3.org/2000/svg" width="120" height="60"><rect width="120" height="60" fill="#369"/></svg>'
for name in ['ordinary','eager','explicit-lazy','inline','list','table','fold','nested-eager','thumb','original','remote-local','far-lazy','far-eager','link-art']:
 write('content/images/'+name+'.svg',SVG)
BODY='''---
title: Loading checks
---
![Ordinary|120x60](ordinary.svg "Ordinary caption")

![Eager|120x60](eager.svg "Eager caption")
{loading="eager" #eager .invert-when-dark}

![Explicit lazy](explicit-lazy.svg)
{loading="lazy"}

Inline ![Inline](inline.svg) text.

1. ![List](list.svg)

| Image |
| --- |
| ![Table](table.svg) |

{{% folding title="Fold" %}}
![Fold](fold.svg)

{{< grid >}}
{{< cell >}}
{{< image src="nested-eager.svg" alt="Nested eager" loading="eager" width=120 height=60 >}}
{{< /cell >}}
{{< /grid >}}
{{% /folding %}}

{{< image src="thumb.svg" original="original.svg" alt="Thumb" width=120 height=60 background="#fff" >}}

{{< image src="https://images.invalid/remote.png" alt="Remote" loading="lazy" >}}

{{< link href="/" text="Link artwork" image="link-art.svg" >}}

{{% block id="spacer" %}}
Long-page spacer used only by the isolated test.
{{% /block %}}

![Far lazy|120x60](far-lazy.svg)
{id="far-lazy"}

{{< image src="far-eager.svg" alt="Far eager" loading="eager" width=120 height=60 id="far-eager" >}}
'''
write('content/images/index.md',BODY)
# Predictable physical distance for the native browser lazy-loading check.
write('layouts/_partials/sidera/head-extra.html','<style>#spacer { height: 20000px; }</style>')
class Images(HTMLParser):
 def __init__(self,text):super().__init__();self.images=[];self.feed(text)
 def handle_starttag(self,t,a):
  if t=='img':
   assert len(a)==len(dict(a)),('duplicate image attribute',a)
   self.images.append(dict(a))
passed=[];rejected=[]
def build(label,overlay='',diagnostic=None):
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr);rejected.append(label)
 else:assert not p.returncode,p.stdout+p.stderr;passed.append(label)
 return out
for label,overlay,prefix in [('baseline','',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n",''),('subpath',"baseURL='https://example.invalid/preview/'\n",'/preview'),('caption-off','[params]\nauto_caption=false\n','')]:
 out=build(label,overlay);raw=(out/'images/index.html').read_text();images=Images(raw).images
 byalt={a['alt']:a for a in images if a.get('alt') in ['Ordinary','Eager','Explicit lazy','Inline','List','Table','Fold','Nested eager','Thumb','Remote','Far lazy','Far eager']}
 assert len(byalt)==12
 for alt,a in byalt.items():
  assert a['loading']==('eager' if alt in ['Eager','Nested eager','Far eager'] else 'lazy')
  assert a['decoding']=='async' and 'data-src' not in a
  if alt!='Remote':assert a['src'].startswith(prefix+'/images/'),(alt,a)
 for alt in ['Ordinary','Eager','Nested eager','Thumb','Far lazy','Far eager']:
  assert byalt[alt]['width']=='120' and byalt[alt]['height']=='60'
 assert byalt['Eager']['id']=='eager' and byalt['Eager']['class']=='invert-when-dark'
 assert byalt['Eager']['title']=='Eager caption' and byalt['Thumb']['style']=='background-color:#fff'
 assert byalt['Remote']['src']=='https://images.invalid/remote.png'
 assert not any(a['src'].endswith('/original.svg') for a in images)
 assert f'href="{prefix}/images/original.svg"' in raw
 assert '<figcaption>List</figcaption>' not in raw and '<figcaption>Table</figcaption>' not in raw
 for name in ['ordinary','eager','thumb','original']:
  assert (out/'images'/f'{name}.svg').read_bytes()==(SITE/'content/images'/f'{name}.svg').read_bytes()
for kind in ['markdown','shortcode']:
 for i,value in enumerate(['""','"auto"','"EAGER"','true','12','"eager onload=bad"']):
  content=f'![Invalid](ordinary.svg)\n{{loading={value}}}' if kind=='markdown' else '{{< image src="ordinary.svg" alt="Invalid" loading='+value+' >}}'
  write('content/images/index.md','---\ntitle: Invalid\n---\n'+content+'\n')
  build(kind+'-invalid-'+str(i),diagnostic='loading must be lazy or eager' if kind=='markdown' or value.startswith('"') else 'loading must be a string')
write('content/images/index.md',BODY)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'defaults':'lazy/async','eagerOverrides':'Markdown standalone attributes and image shortcode','dimensionsSourcesCaptionsPreserved':True},indent=2)+'\n');print('PASS image loading:',len(passed),'builds /',len(rejected),'expected rejections')
