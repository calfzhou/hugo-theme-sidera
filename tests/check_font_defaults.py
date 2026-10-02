"""Native font-family selection tests, no font acquisition or consumer dependencies.
Usage: python3 tests/check_font_defaults.py /absolute/fresh-output-directory
"""
from pathlib import Path
import base64
import json
import re
import subprocess
import sys
from html.parser import HTMLParser

THEME=Path(__file__).resolve().parents[1]
RUN=Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh isolated output directory'
SITE=RUN/'site';SITE.mkdir(parents=True)
UI='"LXGW WenKai", "Helvetica Neue", Helvetica, "Lucida Grande", Lucida, Tahoma, Arial, "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", "Heiti SC", "WenQuanYi Micro Hei", STXiHei, SimHei, sans-serif'
INLINE='"LXGW WenKai", "Source Code Pro", Monaco, Menlo, Consolas, "Courier New", monospace'
CODE='"Source Code Pro", Monaco, Menlo, Consolas, "Courier New", "LXGW WenKai Mono", "LXGW WenKai", monospace'

def write(name,text):
    p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)

write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Font defaults'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[markup.goldmark.extensions.passthrough]
_merge='deep'
[params]
comments=false
''')
write('content/fonts/index.md','''---
title: Font selection — 字体选择
---
## Heading — 中文

Prose 正文 with `inline_code 中文` and {{< kbd text="Ctrl" >}}.

```python
print("Source block 中文")
```

{{< snippet src="sample.py" >}}
''')
write('content/fonts/sample.py','print("Exact source bytes 中文")\n')
# Test both native Giscus stylesheet variants without enabling a provider.
write('layouts/_partials/sidera/head-extra.html','''{{ range $mode, $css := partial "comments/themes.html" . }}
<meta name="font-check-giscus-{{ $mode }}" content="{{ $css }}">
{{ end }}''')
css=(THEME/'assets/css/sidera.css').read_text()
for name,value in [('ui',UI),('reading','var(--ui)'),('inline-code',INLINE),('code',CODE)]:
    assert f'--{name}: {value};' in css,name
assert '.prose code { font-family: var(--inline-code);' in css
assert re.search(r'\.prose pre \{[^}]*var\(--code\)',css)
assert '.prose pre code { padding: 0; font: inherit;' in css
assert re.search(r'\.prose \.code-copy-fallback \{[^}]*var\(--code\)',css)
assert '@font-face' not in css and '@import' not in css
class DOM(HTMLParser):
    def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))

def build(label,extra=()):
    out=RUN/(label+'-public')
    p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--panicOnWarning','--printI18nWarnings',*extra],capture_output=True,text=True,timeout=60)
    (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
    assert p.returncode==0,p.stdout+p.stderr
    raw=(out/'fonts/index.html').read_text();dom=DOM(raw)
    for tag,attrs in dom.nodes:
        if tag in ('script','link'):
            url=attrs.get('src',attrs.get('href',''))
            assert not url.startswith(('https://','http://','//')),url
    for mode in ('light','dark'):
        url=next(a['content'] for t,a in dom.nodes if t=='meta' and a.get('name')=='font-check-giscus-'+mode)
        giscus=base64.b64decode(url.split(',',1)[1]).decode()
        assert giscus.count('@import')==1 and f'https://giscus.app/themes/{mode}.css' in giscus
        assert '@font-face' not in giscus
        # CSS minification removes optional quotes; compare ordered family names.
        stack=re.search(r'font-family:([^;}]+)',giscus).group(1)
        normalize=lambda x:[v.strip().strip('"\'').lower() for v in x.split(',')]
        assert normalize(stack)==normalize(UI),(mode,stack)
    assert (out/'fonts/sample.py').read_bytes()==(SITE/'content/fonts/sample.py').read_bytes()
    assert 'data-sidera-comments-script' not in raw
    assert not list(out.rglob('*.woff*'))
    return out

build('baseline')
write('chinese.toml',"locale='zh-CN'\ndefaultContentLanguage='zh'\n")
build('chinese',('--config','hugo.toml,chinese.toml'))
hook=SITE/'layouts/_partials/sidera/head-extra.html'
hook.write_text(hook.read_text()+'''\n<style>:root { --ui: serif; --reading: sans-serif; --inline-code: cursive; --code: monospace; }</style>\n''')
build('override')
(RUN/'results.json').write_text(json.dumps({'builds':3,'stacks':{'ui':UI,'inline':INLINE,'code':CODE},'giscus_variants':2,'no_font_loader_added':True,'source_bytes_preserved':True,'theme':str(THEME)},indent=2)+'\n')
print('PASS 3 native font builds; retained',RUN)
