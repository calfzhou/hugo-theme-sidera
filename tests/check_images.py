"""Native opt-in background-image cases, C2 nesting, resource integrity and safety.
Run: python3 tests/check_images.py /absolute/fresh-output-directory
No packages, renderer installs, remote fetches or consumer mutations.
"""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve()
assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/preview/'
title='Images'
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
SVG='<svg xmlns="http://www.w3.org/2000/svg" width="120" height="60"><rect x="10" y="10" width="100" height="40" fill="black"/></svg>'
write('content/images/art.svg',SVG);write('assets/shared.svg',SVG);write('static/public.svg',SVG)
BODY='''---
title: Image backgrounds
---
![Ordinary image](art.svg)
{id="plain"}

![Invert in dark](art.svg)
{.invert-when-dark id="dark-image"}

![Invert in light](art.svg)
{.invert-when-light id="light-image"}

{{< image src="art.svg" alt="No forced background" id="plain-shortcode" >}}
{{< image src="art.svg" alt="Meaningful alt" caption="Explicit <caption> & text" width=120 height=60 background="#f9fafb" id="pale" >}}
{{< image src="shared.svg" alt="" background="transparent" id="decorative" >}}
{{< image src="/public.svg?version=1" alt="No caption" caption="" id="static" >}}
{{< image src="https://images.invalid/dynamic?id=1" alt="External reference" caption="" >}}
{{< image src="art.svg" alt="Caption suppressed by class" class="no-caption" >}}

{{% folding title="Nested images" %}}
{{< grid columns=2 >}}
{{< cell >}}
{{< image src="art.svg" alt="Nested & image" width="100" background="#fff" class="invert-when-dark" id="nested" >}}
{{< /cell >}}
{{< /grid >}}
{{% /folding %}}

{{% timeline %}}
{{< event title="A dated image" >}}
{{< image src="art.svg" alt="Timeline image" caption="" background="#ffffff80" id="timeline-image" >}}
{{< /event >}}
{{% /timeline %}}

{{% block class="invert-when-dark" id="group" %}}
Group intent, not only images:
![Group image](art.svg)
{{% /block %}}
'''
write('content/images/index.md',BODY)
class DOM(HTMLParser):
 def __init__(self,html):super().__init__();self.nodes=[];self.feed(html)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
 def id(self,id):return next(a for t,a in self.nodes if a.get('id')==id)
passed=[];rejected=[]
def build(label,diagnostic=None,overlay=''):
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr);rejected.append(label)
 else:assert not p.returncode,(label,p.stdout+p.stderr);passed.append(label)
 return out
for label,overlay in [('baseline',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n"),('auto-caption-off','[params]\nauto_caption=false\nicons=false\n')]:
 out=build(label,overlay=overlay);raw=(out/'images/index.html').read_text();d=DOM(raw)
 assert d.id('pale')['src']=='/preview/images/art.svg'
 assert d.id('pale')['alt']=='Meaningful alt' and d.id('pale')['width']=='120' and d.id('pale')['height']=='60'
 assert d.id('pale')['style']=='background-color:#f9fafb'
 assert d.id('static')['src']=='/preview/public.svg?version=1'
 assert d.id('decorative')['src']=='/preview/shared.svg' and d.id('decorative')['alt']==''
 assert d.id('nested')['class']=='invert-when-dark'
 assert d.id('timeline-image')['style']=='background-color:#ffffff80'
 assert 'Explicit &lt;caption&gt; &amp; text' in raw
 assert (out/'images/art.svg').read_bytes()==(SITE/'content/images/art.svg').read_bytes()
 assert 'ZgotmplZ' not in raw and 'data-sidera-leaf' not in raw
 # Page/cascade/preset auto-caption behavior is reused; explicit caption survives opt-out.
 expected=1 if label=='auto-caption-off' else 6
 assert sum(t=='figcaption' for t,_ in d.nodes)==expected,(label,sum(t=='figcaption' for t,_ in d.nodes))
cases=[('missing-src','alt="x"','nonblank src'),('missing-alt','src="art.svg"','explicit alt'),('src-type','src=true alt="x"','must be a string'),('alt-type','src="art.svg" alt=42','must be a string'),('caption-type','src="art.svg" alt="x" caption=true','must be a string'),('background-type','src="art.svg" alt="x" background=true','must be a string'),('background-css','src="art.svg" alt="x" background="url(https://x.invalid/a)"','background must'),('background-injection','src="art.svg" alt="x" background="#fff;display:none"','background must'),('background-blank','src="art.svg" alt="x" background=""','background must'),('width-zero','src="art.svg" alt="x" width=0','positive integer'),('width-float','src="art.svg" alt="x" width=2.5','positive integer'),('height-unit','src="art.svg" alt="x" height="20px"','positive integer'),('class','src="art.svg" alt="x" class="bad;style"','invalid class'),('id','src="art.svg" alt="x" id="bad id"','invalid id'),('event','src="art.svg" alt="x" onload="bad()"','unsupported parameter'),('retired-viewer','src="art.svg" alt="x" fancybox="true"','unsupported parameter'),('data-url','src="data:image/svg+xml,x" alt="x"','unsafe URL'),('protocol-relative','src="//images.invalid/x.svg" alt="x"','unsafe URL'),('mailto','src="mailto:a@b" alt="x"','safe local image'),('traversal','src="../../../x.svg" alt="x"','leaves the content root'),('raw-svg','src="<svg></svg>" alt="x"','image extension')]
for label,args,diagnostic in cases:
 write('content/images/index.md','---\ntitle: Negative image\n---\n{{< image '+args+' >}}\n');build(label,diagnostic)
write('content/images/index.md',BODY)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'theme':str(THEME)},indent=2)+'\n');print('PASS',len(passed),'builds /',len(rejected),'expected image rejections;',RUN)
