"""External HTTP(S) target policy across native Markdown and theme URL surfaces.
Run: python3 tests/check_external_links.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='External links'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[params]
footer_menu='footer'
footer_text='[Footer text](https://outside.invalid/text)'
license='[License](https://outside.invalid/license)'
article_footer=['references','license','authors']
edit_url='https://outside.invalid/edit'
references=['[Reference](https://outside.invalid/reference)']
[[menus.footer]]
name='External menu'
url='https://outside.invalid/menu?a=1&b=2'
[[menus.footer]]
name='Internal absolute menu'
url='https://example.invalid/internal/'
[[menus.social]]
name='Social web'
url='https://outside.invalid/social'
[[menus.social]]
name='Social email'
url='mailto:reader@example.invalid'
''')
write('content/check/index.md','''---
title: External links
---
[Local popup test](http://127.0.0.1:14810/internal/)

[External](https://outside.invalid/path?q=1&b=2#heading "Title & tooltip")

<https://outside.invalid/auto>

[Same absolute](https://example.invalid/internal/)

[Same port](https://EXAMPLE.invalid:443/internal/)

[Other scheme](http://example.invalid/internal/)

[Other port](https://example.invalid:444/internal/)

[Subdomain](https://sub.example.invalid/)

[Lookalike](https://example.invalid.outside.invalid/)

[Protocol relative](//outside.invalid/protocol)

[Same protocol relative](//example.invalid/internal/)

[Relative](../internal/index.md#heading)

[Root](/internal/)

[Anchor](#heading)

[Email](mailto:reader@example.invalid)

[Telephone](tel:+12345678)

[![Linked image](art.svg)](https://outside.invalid/image)

{{% folding title="Nested links" %}}
[Inside fold](https://outside.invalid/fold)
{{% /folding %}}

{{< link href="https://outside.invalid/card" text="External card" image="art.svg" >}}

{{< link href="https://example.invalid/internal/" text="Internal card" >}}

{{< image src="art.svg" original="https://outside.invalid/original.svg" alt="External original" >}}

{{< image src="art.svg" original="art.svg" alt="Internal original" >}}

{{< badge_github user="owner" repo="repo" disabled=true >}}

{{< video src="https://outside.invalid/movie.mp4" >}}

## Heading

`<a href="https://outside.invalid/literal">Literal</a>`
''')
write('content/check/art.svg','<svg xmlns="http://www.w3.org/2000/svg" width="80" height="40"><rect width="80" height="40" fill="#369"/></svg>')
write('content/internal/index.md','---\ntitle: Internal destination\n---\n## Heading\n')
# Exercise helper authority comparisons that are independent of page rendering.
write('layouts/_partials/sidera/head-extra.html','''{{ range $url, $want := dict "https://example.invalid:443/x" false "HTTPS://EXAMPLE.invalid/x" false "https://outside.invalid/x" true "https://example.invalid@outside.invalid/x" true "https://example.invalid:444/x" true "mailto:a@outside.invalid" false "tel:+123" false "#x" false "/x" false "../x" false }}{{ if ne (partial "links/external.html" $url) $want }}{{ errorf "Bad origin classification: %s" $url }}{{ end }}{{ end }}''')
class Anchors(HTMLParser):
 def __init__(self,text):super().__init__();self.links=[];self.feed(text)
 def handle_starttag(self,t,a):
  if t=='a':assert len(a)==len(dict(a)),a;self.links.append(dict(a))
passed=[]
for label,overlay in [('baseline',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n"),('subpath',"baseURL='https://example.invalid/preview/'\n"),('icons-off','[params]\nicons=false\n')]:
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
 raw=(out/'check/index.html').read_text();links=Anchors(raw).links;external=0
 for a in links:
  href=a.get('href','');u=urlsplit(href);scheme=u.scheme or ('https' if u.netloc else '')
  ext=scheme in ('http','https') and u.hostname and (scheme!='https' or u.hostname.lower()!='example.invalid' or u.port not in (None,443))
  if ext:
   assert a.get('target')=='_blank',(label,a);assert {'noopener','noreferrer'}<=set(a.get('rel','').split()),a;external+=1
  else:assert a.get('target') in (None,''),(label,a)
 assert external>=15,external
 a=next(a for a in links if a.get('title')=='Title & tooltip');assert a['href']=='https://outside.invalid/path?q=1&b=2#heading'
 assert 'data-content-page' not in a
 assert any(a.get('data-content-page')=='/preview/internal/' if label=='subpath' else a.get('data-content-page')=='/internal/' for a in links)
 assert '&lt;a href=' in raw
 assert 'href="https://outside.invalid/literal" target=' not in raw
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'externalSurfaces':'Markdown/autolinks/nested/linked images/cards/original links/menus/social/footer/license/references/edit/video/badge','internalAbsoluteAndRelativeSameTab':True,'safeRel':True},indent=2)+'\n');print('PASS external link policy:',', '.join(passed))
