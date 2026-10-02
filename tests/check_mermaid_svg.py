"""Native regression fixture for XML-safe Mermaid labels; no dependencies/network.
Run: python3 tests/check_mermaid_svg.py /absolute/fresh-output-directory
The browser must additionally decode returned SVG; an '<svg' string is not enough.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh output directory'
SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
controller=(THEME/'assets/js/mermaid-frame.js').read_text()
assert re.search(r'htmlLabels:false,\s*fontFamily:',controller)
assert 'flowchart:{htmlLabels:' not in controller
assert "'htmlLabels'" in controller.split('secure:',1)[1]
manifest=json.loads((THEME/'assets/vendor/mermaid-11.17.2/provenance.json').read_text())
for name,digest in manifest['files'].items():assert hashlib.sha256((THEME/'assets/vendor/mermaid-11.17.2'/name).read_bytes()).hexdigest()==digest
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Mermaid labels'
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
write('content/diagram/index.md',r'''---
title: Multiline SVG labels
---
```mermaid
flowchart LR
  root["First line\n第二行 & context\n[S][E]"] --> next[Next]
```

{{% folding title="Nested diagram" %}}
```mermaid
flowchart LR
  node["`One
Two
Three`"] --> next[Next]
```
{{% /folding %}}
''')
write('content/plain/index.md','---\ntitle: Plain page\n---\nNo diagram.\n')
class DOM(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
passed=[]
for label,base,config in [('baseline','https://example.invalid/',''),('chinese','https://example.invalid/preview/',"locale='zh-CN'\ndefaultContentLanguage='zh'\n")]:
 write('probe.toml',config);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--baseURL',base,'--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
 raw=(out/'diagram/index.html').read_text();dom=DOM(raw)
 assert len([a for t,a in dom.nodes if a.get('data-sidera-diagram')=='mermaid'])==2
 assert 'First line\\n第二行 &amp; context\\n[S][E]' in raw
 assert 'data-sidera-diagrams-script' not in (out/'plain/index.html').read_text()
 frame=next((out/'diagrams').glob('mermaid-11.17.2.*.html')).read_text()
 assert "connect-src 'none'" in frame and "frame-src 'none'" in frame and "script-src 'self'" in frame
 assert 'allow-same-origin' not in frame and 'unsafe-eval' not in frame
 built=next((out/'js').glob('mermaid-frame.*.js')).read_text()
 assert 'htmlLabels:!1' in built or 'htmlLabels:false' in built
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'vendorHashesUnchanged':True,'rootLabelPolicySecured':True,'sandboxCSPUnchanged':True,'browserDecodeRequired':True},indent=2)+'\n')
print('PASS native label policy/fixtures, pinned vendor integrity and sandbox CSP;',RUN)
