"""Native registry/provenance, original Parallax variants and strict geometry safety.
Run: python3 tests/check_icons.py /absolute/fresh-output-directory
"""
from pathlib import Path
import hashlib,json,re,subprocess,sys,xml.etree.ElementTree as ET
THEME=Path(__file__).resolve().parents[1]
RUN=Path(sys.argv[1]).resolve(); RUN.mkdir(parents=True,exist_ok=False); SITE=RUN/'site';SITE.mkdir()
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.org/'
title='Icon checks'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[[menus.primary]]
name='Parallax manual'
pageRef='/manual'
[menus.primary.params]
icon='sidera-bold-duotone'
''')
keys=['sidera-bold','sidera-bold-duotone','sidera-linear','sidera-line-duotone']
write('content/manual/_index.md','---\ntitle: Icon manual\npreset: docs\nparams:\n  logo: images/sidera-parallax-circle.svg\n---\n'+ '\n'.join('{{< link href="/manual/" text="'+key+'" icon="'+key+'" >}}' for key in keys))
write('layouts/_partials/sidera/head-extra.html','<script type="application/json" id="icons-probe">{{ dict "icons" (partialCached "sidera/icons.html" site "icons") "sources" hugo.Data.sidera.icon_sources | jsonify | safeJS }}</script>')
passed=[]; rejected=[]
def build(name,config='',diagnostic=None):
 write('probe.toml',config);out=RUN/(name+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--config','hugo.toml,probe.toml','--destination',str(out),'--cacheDir',str(RUN/'cache'),'--noBuildLock','--panicOnWarning'],text=True,capture_output=True,timeout=60)
 (RUN/(name+'.log')).write_text(p.stdout+p.stderr)
 if diagnostic:assert p.returncode and diagnostic in p.stdout+p.stderr,(name,p.stdout+p.stderr);rejected.append(name)
 else:assert not p.returncode,(name,p.stdout+p.stderr);passed.append(name)
 return out
out=build('baseline');text=(out/'manual/index.html').read_text()
data=json.loads(re.search(r'id="icons-probe">(.*?)</script>',text,re.S)[1]);assert set(data['icons'])==set(data['sources'])
originals=[];solars=[]
for key,meta in data['sources'].items():
 svg=data['icons'][key].strip();root=ET.fromstring(svg)
 assert hashlib.sha256(svg.encode()).hexdigest()==meta['normalized_sha256'],key
 assert root.attrib['viewBox']=='0 0 24 24' and not {'width','height','style'}&root.attrib.keys()
 if meta.get('kind')=='original':
  originals.append(key)
  assert key in keys and meta['design']=='Sidera Parallax' and meta['author']=='Eureka' and meta['copyright']=='2026 Calf' and meta['license']=='MIT'
  assert meta['style']==key.removeprefix('sidera-')
  assert not {'solar_name','repository','revision','path'}&meta.keys(),key
  assert hashlib.sha256((THEME/meta['source']).read_bytes()).hexdigest()==meta['source_sha256']
 else:
  solars.append(key)
  assert meta['solar_name'] and meta['style'] in ('BoldDuotone','Linear') and meta['revision'] and meta['license']=='CC-BY-4.0'
  assert meta['repository'] in ('saoudi-h/solar-icons','hexo-theme-stellar')
  assert meta['path'] and meta['author'] in ('480 Design','Hakim Saoudi')
assert set(originals)==set(keys) and len(solars)==45
assert len({data['icons'][key] for key in keys})==4
for key in keys:
 svg=data['icons'][key];assert svg in (THEME/'data/sidera/icons.yaml').read_text()
 assert ('opacity="0.4"' in svg)==('duotone' in key)
 assert ('stroke-width="6.25"' in svg)==('line' in key) # transformed to 1.5 viewBox units
assert 'class="icon" aria-hidden="true" focusable="false"' in text
assert '<a class="menu' in text or 'native-menu' in text
# Site data replacement affects the same named menu/card key, never brand images.
custom='<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="7" stroke="currentColor" stroke-width="1.5"/></svg>'
write('data/icons.yaml','sidera-bold-duotone: '+json.dumps(custom)+'\ncustom-example: '+json.dumps(custom)+'\n')
out=build('override');text=(out/'manual/index.html').read_text();assert text.count('r="7"')>=2
for name,cfg in [('icons-off','[params]\nicons=false\n'),('chinese-off',"defaultContentLanguage='zh'\nlocale='zh-CN'\n[params]\nicons=false\n")]:
 out=build(name,cfg)
 for route in ['index.html','manual/index.html']:
  text=(out/route).read_text();visible=re.sub('<script.*?</script>','',text,flags=re.S)
  assert '<svg' not in visible and 'Parallax manual' in visible
 assert 'sidera-parallax-circle.svg' in (out/'index.html').read_text()
 assert 'alt=""' in (out/'index.html').read_text()
# Format guards are identical for originals and Solar: invalid unused overrides fail even off.
bad={
 'script':'<svg viewBox="0 0 24 24"><script>alert(1)</script></svg>',
 'event':'<svg viewBox="0 0 24 24" onload="bad"><path d="M1 1"/></svg>',
 'foreign':'<svg viewBox="0 0 24 24"><foreignObject/></svg>',
 'bitmap':'<svg viewBox="0 0 24 24"><image href="https://example.invalid/x"/></svg>',
 'paint':'<svg viewBox="0 0 24 24"><path fill="red" d="M1 1"/></svg>',
 'size':'<svg viewBox="0 0 24 24" width="20"><path d="M1 1"/></svg>',
 'entity':'<svg viewBox="0 0 24 24"><path fill="&#35;fff" d="M1 1"/></svg>',
 'unbalanced':'<svg viewBox="0 0 24 24"><g><path d="M1 1"/></svg>',
 'duplicate':'<svg viewBox="0 0 24 24" fill="none" fill="currentColor"></svg>',
 'style':'<svg viewBox="0 0 24 24" style="color:red"><path d="M1 1"/></svg>',
 'type':False}
for name,value in bad.items():
 write('data/icons.yaml','unused-unsafe: '+json.dumps(value)+'\n');build('reject-'+name,'[params]\nicons=false\n','Sidera icon')
write('data/icons.yaml','{}\n');write('content/invalid.md','---\ntitle: Invalid\n---\n{{< link href="/" text="Bad" icon="unknown.svg" >}}');build('reject-key',diagnostic='unknown icon')
# Pin original image bytes independently of derivative provenance.
expected={'sidera-parallax-circle.svg':'ebe20ad690732ea31d77b7a7de72308f305b5927ca2c87fb07b7a007a9b85a68','sidera-parallax-square.svg':'f21dc7afd04c9f4d4873ac39ee03e77d6affc093780d669177636b36e215ec7c'}
for name,digest in expected.items():assert hashlib.sha256((THEME/'assets/images'/name).read_bytes()).hexdigest()==digest
for name in [*expected,'sidera-parallax-32.png']:
 assert (THEME/'assets/images'/name).read_bytes()==subprocess.check_output(['git','-C',str(THEME),'show','HEAD:assets/images/'+name])
assert (THEME/'LICENSE').read_bytes()==(THEME/'assets/licenses/sidera-mit.txt').read_bytes()
assert (THEME/'THIRD-PARTY-NOTICES.md').read_bytes()==(THEME/'assets/licenses/sidera-third-party.txt').read_bytes()
(RUN/'results.json').write_text(json.dumps({'passed':passed,'rejected':rejected,'Solar':len(solars),'original':originals},indent=2)+'\n');print('PASS',len(passed),'builds;',len(rejected),'expected rejections; 45 Solar + 4 original entries')
