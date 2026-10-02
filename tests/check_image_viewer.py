"""Opt-in original-image source/markup/conditional assets. No browser/network/package.
Run: python3 tests/check_image_viewer.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Original images'
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
SVG='<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200"><rect x="200" y="200" width="1200" height="800" fill="#277"/></svg>'
write('content/images/thumb.svg',SVG.replace('1600','160').replace('1200','120').replace('200','20').replace('800','80'))
for n in ('original','second','slow','broken'):write('content/images/'+n+'.svg',SVG)
write('assets/shared.svg',SVG);write('static/static.svg',SVG)
BODY='''---
title: Thumbnail and original
---
{{< image src="thumb.svg" alt="Plain" id="plain" >}}
{{< image src="thumb.svg" original="original.svg" alt="Distinct original" caption="Caption <text> & meaning" width=160 background="#f9fafb" id="thumb" >}}
{{< image src="thumb.svg" original="second.svg" alt="Second original" caption="" id="second" >}}
{{< image src="thumb.svg" original="broken.svg" alt="Broken original" id="broken" >}}
{{< image src="thumb.svg" original="slow.svg" alt="Slow original" id="slow" >}}
{{< image src="thumb.svg" original="https://images.invalid/original" alt="Remote original" id="remote" >}}
{{< image src="thumb.svg" original="/static.svg" alt="Static original" id="static" >}}
{{< image src="thumb.svg" original="shared.svg" alt="Shared original" id="shared" >}}

{{% folding title="Hidden image" %}}
{{< grid columns=2 >}}
{{< cell >}}
{{< image src="thumb.svg" original="original.svg" alt="Nested original" class="invert-when-dark" id="nested" >}}
{{< /cell >}}
{{< /grid >}}
{{% /folding %}}

{{% block class="invert-when-dark" %}}
{{< image src="thumb.svg" original="original.svg" alt="Group inversion" id="group" >}}
{{% /block %}}
'''
write('content/images/index.md',BODY)
write('content/plain/index.md','---\ntitle: No viewer\n---\n{{< image src="shared.svg" alt="Plain image" >}}\n')
class DOM(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,t,a):self.nodes.append((t,dict(a)))
passed=[];rejected=[]
def build(label,diagnostic=None,overlay=''):
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning','--printI18nWarnings'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr);rejected.append(label)
 else:assert not p.returncode,(label,p.stdout+p.stderr);passed.append(label)
 return out
for label,overlay in [('baseline',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n"),('icons-off','[params]\nicons=false\n'),('subpath',"baseURL='https://example.invalid/preview/'\n")]:
 out=build(label,overlay=overlay);raw=(out/'images/index.html').read_text();dom=DOM(raw)
 openers=[a for t,a in dom.nodes if t=='a' and 'data-image-open' in a];assert len(openers)==9
 prefix='/preview' if label=='subpath' else ''
 assert openers[0]['href']==prefix+'/images/original.svg'
 assert openers[0]['aria-label'].endswith('Distinct original')
 assert all(a['aria-label'] for a in openers)
 assert sum('data-sidera-image-viewer' in a for _,a in dom.nodes)==1
 assert 'data-sidera-image-viewer' not in (out/'plain/index.html').read_text()
 assert (out/'images/original.svg').read_bytes()==(SITE/'content/images/original.svg').read_bytes()
 assert (out/'images/thumb.svg').read_bytes()==(SITE/'content/images/thumb.svg').read_bytes()
 assert 'Caption &lt;text&gt; &amp; meaning' in raw
 assert not any(t in ('iframe','object','embed') for t,_ in dom.nodes)
 assert 'ZgotmplZ' not in raw
 if label=='icons-off':assert not any(t=='svg' for t,_ in dom.nodes)
 if label=='chinese':assert '下载原图' in raw and '关闭图片' in raw
for n,value in enumerate(['true','"javascript:alert(1)"','"data:image/svg+xml,x"','"//external.invalid/x.png"','"../../../x.png"','"file.py"','"mailto:a@b"']):
 write('content/images/index.md','---\ntitle: Bad original\n---\n{{< image src="thumb.svg" alt="x" original='+value+' >}}\n');build('invalid-'+str(n),'Sidera')
write('content/images/index.md',BODY)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'theme':str(THEME)},indent=2)+'\n');print('PASS',len(passed),'native viewer builds /',len(rejected),'expected rejections;',RUN)
