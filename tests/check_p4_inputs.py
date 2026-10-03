"""Focused native tests for positive recent counts and independent card images.
Run: python3 tests/check_p4_inputs.py /absolute/isolated-output-directory
No third-party Python packages, network fetch, or consumer checkout mutation.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh output directory'
RUN.mkdir(parents=True)
SITE = RUN / 'site'
SITE.mkdir()

def write(path, text):
    p = SITE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

CONFIG = f'''baseURL = 'https://example.invalid/preview/'
title = 'Input checks'
theme = '{THEME.name}'
themesDir = {json.dumps(str(THEME.parent))}
timeZone = 'Asia/Shanghai'
disableKinds = ['RSS']
[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'
[markup.goldmark.parser]
_merge = 'deep'
[markup.goldmark.extensions.passthrough]
_merge = 'deep'
'''
write('hugo.toml', CONFIG)
for i in range(40):
    write(f'content/notes/n{i:02}/index.md', f'---\ntitle: "Note {i:02}"\ndate: "2024-01-01T00:00:00+08:00"\n---\nBody.\n')
ROOT = '---\ntitle: Notes\npreset: notes\nparams:\n  left: [recent]\n'
write('content/notes/_index.md', ROOT + '---\n')
IMAGE = '<svg xmlns="http://www.w3.org/2000/svg" width="44" height="44"><rect width="44" height="44" fill="red"/></svg>'
write('content/notes/n00/art.svg', IMAGE)
write('assets/shared.svg', IMAGE)
write('static/logo.ico', 'static-byte-fixture')
CARDS = '''---
title: Cards
---
## Old Heading {id="Old Heading"}

{{< link href="../notes/n00/index.md" text="Article" image="../notes/n00/art.svg" alt="Red & <art>" >}}
{{< link href="https://example.invalid/project" text="Project" image="https://images.invalid/logo?v=1&x=2" >}}
{{< link href="mailto:owner@example.invalid" text="Contact" image="/logo.ico?v=1" >}}
{{< link href="/" text="Home" image="shared.svg" icon="notebook" >}}
{{< link href="/" text="Default" >}}
{{< link href="/" text="Empty" image="" icon="" >}}

{{% folding title="Nested cards" %}}
{{< grid columns=2 >}}
{{< cell >}}
{{< link href="../notes/n00/index.md" text="Nested" image="../notes/n00/art.svg" >}}
{{< /cell >}}
{{< /grid >}}
{{% /folding %}}
'''
write('content/cards/index.md', CARDS)

class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.nodes=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag,dict(attrs)))
    def find(self, tag=None, **attrs):
        return [a for t,a in self.nodes if (not tag or t==tag) and all(a.get(k)==v for k,v in attrs.items())]

passed=[]; rejected=[]
def build(label, diagnostic=None):
    out=RUN/(label+'-public')
    p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--panicOnWarning'],capture_output=True,text=True,timeout=60)
    (RUN/(label+'.log')).write_text(p.stdout+p.stderr)
    if diagnostic:
        assert p.returncode and diagnostic in p.stdout+p.stderr,(label,p.stdout+p.stderr)
        rejected.append(label)
    else:
        assert p.returncode==0,(label,p.stdout+p.stderr)
        passed.append(label)
    return out

def recents(out):
    d=DOM((out/'notes/index.html').read_text())
    return len([a for a in d.find('a') if a.get('href','').startswith('/preview/notes/n') and 'title' in a])

out=build('baseline'); assert recents(out)==10
for count in (1,11,32,100):
    write('content/notes/_index.md',ROOT+f'  recent_count: {count}\n---\n')
    out=build('count-'+str(count));assert recents(out)==min(count,40)
write('content/notes/_index.md', ROOT+'  recent_count: 32\n---\n')
write('hugo.toml',CONFIG+'\n[params]\nicons=false\n')
out=build('icons-off')
d=DOM((out/'cards/index.html').read_text())
imgs=d.find('img',loading='lazy'); assert len(imgs)==5,imgs
assert imgs[0]['src']=='/preview/notes/n00/art.svg'
assert imgs[0]['alt']=='Red & <art>'
assert imgs[1]['src']=='https://images.invalid/logo?v=1&x=2'
assert imgs[1]['alt']==''
assert imgs[2]['src']=='/preview/logo.ico?v=1'
assert imgs[3]['src']=='/preview/shared.svg'
assert d.find('a',href='/preview/notes/n00/')
assert d.find('span',**{'class':'content-link-title'})[0]['title']=='Article'
assert d.find('span',**{'class':'content-link-url'})[0]['title']=='/preview/notes/n00/'
assert d.find('h2',id='Old Heading'), 'Native quoted heading IDs preserve spaces/case'
assert not d.find('span',**{'class':'content-link-icon'})
assert (out/'notes/n00/art.svg').read_bytes()==(SITE/'content/notes/n00/art.svg').read_bytes()
write('hugo.toml',CONFIG)
out=build('icons-on'); d=DOM((out/'cards/index.html').read_text()); assert len(d.find('span',**{'class':'content-link-icon'}))==1
# Instance precedence including reusable widget, site default, preset and cascade.
for label, extra, root in [
 ('site', '[params]\nrecent_count=32\n', ROOT+'---\n'),
 ('instance','',ROOT.replace('  left: [recent]\n','')+'  left: [{component: recent, config: {count: 32}}]\n---\n'),
 ('widget','[params.widgets.many]\ncomponent="recent"\n[params.widgets.many.config]\ncount=32\n',ROOT.replace('left: [recent]','left: [many]')+'---\n'),
 ('cascade','',ROOT+'cascade:\n  params:\n    recent_count: 32\n---\n')]:
    write('hugo.toml',CONFIG+extra);write('content/notes/_index.md',root)
    out=build(label)
    if label!='cascade':assert recents(out)==32
    else:
        d=DOM((out/'notes/n01/index.html').read_text());assert len([a for a in d.find('a') if a.get('href','').startswith('/preview/notes/n') and 'title' in a])==32
write('hugo.toml',CONFIG)
for value in ('0','-1','1.5','true','"32"','[]','{}'):
    for instance in (False,True):
        root=ROOT+('  left: [{component: recent, config: {count: '+value+'}}]\n' if instance else '  recent_count: '+value+'\n')+'---\n'
        # Replace rather than duplicate the left YAML key.
        if instance:root=root.replace('  left: [recent]\n','')
        write('content/notes/_index.md',root)
        build('bad-count-'+str(len(rejected)), 'positive integer')
write('content/notes/_index.md',ROOT+'---\n')
for args in ('image="javascript:alert(1)"','image="data:image/svg+xml,x"','image="//images.invalid/x.svg"','image="mailto:x@y"','image="https:///x.svg"','image="../../../x.svg"','image="/"','image="../notes/n00/index.md"','image=true','image="x.svg" alt=true','alt="orphan"','image="x.svg" onclick="bad()"','image="x%0a.svg"'):
    write('content/cards/index.md','---\ntitle: Bad image\n---\n{{< link href="/" text="Safe card" '+args+' >}}\n')
    build('bad-image-'+str(len(rejected)), 'Sidera')
write('content/cards/index.md',CARDS)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'theme':str(THEME)},indent=2)+'\n')
print(f'PASS {len(passed)} builds / {len(rejected)} expected rejections; {RUN}')
