"""Native in-article timeline tests. No source conversion, network or dependencies.
Run: python3 tests/check_timeline.py /absolute/fresh-output-directory
"""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve()
assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Timeline fixture'
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
BODY='''---
title: Timeline — 历程
type: story
---
{{% timeline id="history" %}}
{{< event title="2025 年" >}}
A maintained record with a [source link](../target/index.md#Old%20Heading).

{{< grid columns=2 >}}
{{< cell >}}
{{< link href="../target/index.md" text="A useful project" image="art.svg" >}}
{{< /cell >}}
{{< cell >}}
{{< link href="../target/index.md" text="Another project" >}}
{{< link href="../target/index.md" text="A second card in one cell" >}}
{{< /cell >}}
{{< /grid >}}
{{< /event >}}
{{< event title="2024 年（For 公开的笔记）" id="public-notes" >}}
## Native Heading {id="Native Heading"}

Text, `inline code`, {{< u text="underline" >}} and $x^2$.

{{< folding title="Supporting detail" >}}
{{< box color="red" >}}
{{< snippet src="sample.py" >}}
{{< /box >}}
{{< /folding >}}
{{< /event >}}
{{< event title="2008 年或更早" >}}
> A quotation with preserved credit.
>
> — An author, *A book*

![A local image](art.svg)
{{< /event >}}
{{% /timeline %}}

{{% folding title="Nested timeline" %}}
{{< timeline >}}
{{< event title="A second history" >}}
Distinct source/copy controls:
{{< snippet src="sample.py" >}}
{{< /event >}}
{{< /timeline >}}
{{% /folding %}}
'''
write('content/history/index.md',BODY)
write('content/target/index.md','---\ntitle: Destination\n---\n## Old Heading {id="Old Heading"}\n')
write('content/history/sample.py','print("Preserve source bytes 中文")\n')
write('content/history/art.svg','<svg xmlns="http://www.w3.org/2000/svg" width="44" height="44"><rect width="44" height="44" fill="red"/></svg>')
class DOM(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
 def cls(self,name):return [a for t,a in self.nodes if name in a.get('class','').split()]
passed=[];rejected=[]
def build(label,diagnostic=None,flags=()):
 out=RUN/(label+'-public');p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--panicOnWarning',*flags],capture_output=True,text=True,timeout=60)
 (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:
  assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr);rejected.append(label)
 else:assert p.returncode==0,(label,p.stdout+p.stderr);passed.append(label)
 return out

def verify(out):
 raw=(out/'history/index.html').read_text();d=DOM(raw)
 assert len(d.cls('content-timeline'))==2 and len(d.cls('timeline-event'))==4
 assert len(d.cls('content-link-card'))==3
 assert '2025 年' in raw and '2024 年（For 公开的笔记）' in raw and '2008 年或更早' in raw
 assert any(t=='h2' and a.get('id')=='Native Heading' for t,a in d.nodes)
 assert any(t=='a' and a.get('href')=='/target/#Old%20Heading' for t,a in d.nodes)
 assert 'data-sidera-container' not in raw and 'data-sidera-leaf' not in raw
 assert raw.count('data-code-source=')==2 and 'class="katex"' in raw
 assert (out/'history/sample.py').read_bytes()==(SITE/'content/history/sample.py').read_bytes()
 assert (out/'history/art.svg').read_bytes()==(SITE/'content/history/art.svg').read_bytes()
 ids=[a['id'] for _,a in d.nodes if 'id' in a];assert len(ids)==len(set(ids))
 assert any('Native Heading' in p.read_text() for p in (out/'search').glob('*.json'))
for label,overlay in [('baseline',''),('chinese',"locale='zh-CN'\ndefaultContentLanguage='zh'\n"),('icons-off','[params]\nicons=false\n')]:
 write('probe.toml',overlay);verify(build(label,flags=('--config','hugo.toml,probe.toml')))
write('content/escaped/index.md','---\ntitle: Literal labels\n---\n{{% timeline %}}{{< event title="<script>not markup</script> & date" >}}Content{{< /event >}}{{% /timeline %}}\n')
out=build('escaped');assert '&lt;script&gt;not markup&lt;/script&gt;' in (out/'escaped/index.html').read_text()
bad=[
 ('empty','{{% timeline %}}{{% /timeline %}}','at least one event'),
 ('stray','{{% timeline %}}Stray text{{< event title="Year" >}}Body{{< /event >}}{{% /timeline %}}','only event children'),
 ('leaf','{{% timeline %}}{{< link href="/" text="x" >}}{{% /timeline %}}','requires event children'),
 ('orphan','{{% event title="x" %}}Body{{% /event %}}','timeline parent'),
 ('parent','{{% box %}}{{< event title="x" >}}Body{{< /event >}}{{% /box %}}','timeline parent'),
 ('title','{{% timeline %}}{{< event >}}Body{{< /event >}}{{% /timeline %}}','nonblank title'),
 ('type','{{% timeline %}}{{< event title=2025 >}}Body{{< /event >}}{{% /timeline %}}','must be a string'),
 ('positional','{{% timeline x %}}{{< event title="x" >}}Body{{< /event >}}{{% /timeline %}}','named parameters'),
 ('api','{{% timeline api="https://example.invalid" %}}{{< event title="x" >}}Body{{< /event >}}{{% /timeline %}}','unsupported parameter'),
 ('style','{{% timeline %}}{{< event title="x" style="bad()" >}}Body{{< /event >}}{{% /timeline %}}','unsupported parameter'),
 ('id','{{% timeline id="bad id" %}}{{< event title="x" >}}Body{{< /event >}}{{% /timeline %}}','invalid id'),
 ('raw','{{% timeline %}}{{< event title="x" >}}<script>bad()</script>{{< /event >}}{{% /timeline %}}','Raw HTML omitted'),
 ('notation','{{< timeline >}}{{< event title="x" >}}Body{{< /event >}}{{< /timeline >}}','was not consumed')]
for label,body,diagnostic in bad:
 write('content/negative.md','---\ntitle: Negative\n---\n'+body+'\n');build(label,diagnostic)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'theme':str(THEME)},indent=2)+'\n');print('PASS',len(passed),'builds /',len(rejected),'rejections;',RUN)
