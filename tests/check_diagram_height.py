"""Tall Mermaid/drawio fixtures for natural inline-height and bounded-modal E2E."""
from pathlib import Path
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
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
mermaid='flowchart TD\n'+'\n'.join(f' N{i}[Step {i}] --> N{i+1}[Step {i+1}]' for i in range(14))
write('content/check/index.md','---\ntitle: Natural diagram height\n---\n## Mermaid\n\n```mermaid\n'+mermaid+'\n```\n\n## Drawio\n\n{{< diagramsnet src="tall.drawio" >}}\n\n## After diagrams\n\nThe article continues below both complete images.\n')
write('content/check/tall.drawio','''<mxfile><diagram id="height" name="Height"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" value="Tall diagram" style="rounded=0;whiteSpace=wrap;html=0;" vertex="1" parent="1"><mxGeometry x="0" y="0" width="220" height="1200" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>''')
p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(RUN/'baseline-public'),'--cacheDir',str(RUN/'cache'),'--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60);(RUN/'build.log').write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
html=(RUN/'baseline-public/check/index.html').read_text();assert html.count('class="diagram-view"')==2 and 'id="after-diagrams"' in html
assert (RUN/'baseline-public/check/tall.drawio').read_bytes()==(SITE/'content/check/tall.drawio').read_bytes()
print('PASS native tall-diagram fixtures; browser height/scroll checks required')
