"""Executable JSX opt-in, native compilation, publication and resource contracts.
Run with a fresh absolute output path. Standard library only, no npm or network.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
assert not RUN.exists(), 'Use a fresh output directory'
SITE = RUN / 'site'
SITE.mkdir(parents=True)


def write(name, text):
    path = SITE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def build(name, overlay='', success=True, args=()):
    write('probe.toml', overlay)
    out = RUN / (name + '-public')
    p = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
                        '--config', 'hugo.toml,probe.toml', '--cacheDir', str(RUN / 'cache'),
                        '--noBuildLock', '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings', *args],
                       text=True, capture_output=True, timeout=90)
    (RUN / (name + '.log')).write_text(p.stdout + p.stderr)
    assert (p.returncode == 0) == success, (name, p.stdout, p.stderr)
    if not success:
        assert 'Sidera JSX:' in p.stderr or 'JSBUILD' in p.stderr, (name, p.stderr)
    return out


class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.nodes = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


write('hugo.toml', f'''baseURL='https://example.invalid/'
title='JSX checks'
theme='sidera'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[params]
jsx=true
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[markup.goldmark.parser.attribute]
_merge='shallow'
''')
code = '''import {useState, useId} from 'react';
export default function Widget(){const [n,set]=useState(0);const id=useId();return <div><label htmlFor={id}>Count</label><input id={id} value={n} readOnly/><button onClick={()=>set(x=>x+1)}>Add</button></div>;}'''
page = '''---
title: Widgets
---
Native prose.
```jsx-live {title="Title <&>" caption="Caption <&>" fallback="Readable fallback"}
''' + code + '''
```
<!--more-->
{{< jsx src="widgets/Tool.jsx" css="widgets/tool.css" title="Attached title" caption="Attached" appearance="card" />}}
{{< jsx title="Paired title" appearance="plain" >}}
''' + code + '''
{{< /jsx >}}
```jsx-live {src="widgets/Tool.jsx" mode="sandbox" height=240 title="Frame title" appearance="card"}
```
{{% folding title="Hidden" %}}
{{< grid columns=2 >}}
{{< cell >}}
{{< jsx src="widgets/Tool.jsx" />}}
{{< /cell >}}
{{< cell >}}
```jsx-live
''' + code + '''
```
{{< /cell >}}
{{< /grid >}}
{{% /folding %}}
```jsx-live
import Widget from './widgets/Tool.jsx';
export default Widget;
```
'''
write('content/widgets/index.md', page)
write('content/widgets/widgets/Tool.jsx', "import { value } from './widgets/helper.js'; export default function Tool(){return <p>{value}</p>;}")
write('content/widgets/widgets/helper.js', "export const value='dependency-one';")
write('content/widgets/widgets/tool.css', '.jsx-root p { color: var(--accent); }')
write('content/ordinary.md', '---\ntitle: Ordinary\n---\n```jsx\n' + code + '\n```\n')
write('content/literal.md', '---\ntitle: Literal\n---\n```text\n<figure class="content-jsx" data-sidera-jsx>\n```\n')
write('content/compile-only/index.md', '''---
title: No build-time execution
---
```jsx-live
throw new Error('runtime-only-probe');
export default function Widget(){return <p>{'<script>alert(1)</script>'}</p>;}
```
''')
write('content/failure/index.md', '---\ntitle: Independent failures\n---\n' + '\n\n'.join('```jsx-live\n' + c + '\n```' for c in [
    "throw new Error('module-failure'); export default ()=> <p>unreachable</p>;",
    "export default function Broken(){throw new Error('render-failure')}",
    "export const noDefault = 42;",
    code,
]))
# Shared styling works with no component stylesheet, in page and opaque-frame
# modes. A separately scoped author stylesheet must still override the defaults.
style_code = '''import {useState, useId} from 'react';
export default function Form(){
 const [invalid,setInvalid]=useState(false);const id=useId();
 return <div className="jsx-stack style-probe">
  <div className="jsx-field"><label htmlFor={id}>Name</label>
   <input id={id} defaultValue="Sidera" aria-invalid={invalid} aria-describedby={id+'-hint '+id+'-error'}/></div>
  <p id={id+'-hint'} className="jsx-note">Shared help text.</p>
  <div className="jsx-row"><button onClick={()=>setInvalid(value=>!value)}>Toggle error</button>
   <button disabled>Disabled</button><label><input type="checkbox"/> Ready</label>
   <label><input type="radio" name={id+'-choice'}/> Choice</label></div>
  <p id={id+'-error'} className="jsx-error" aria-live="polite">{invalid?'Example validation error.':''}</p>
  <output className="jsx-result"><span className="jsx-note">Result</span><strong>Native result</strong></output>
 </div>;
}'''
write('content/styling/index.md', '''---
title: Native component styling
---
Ordinary paragraph outside the widgets.

{{< jsx src="Form.jsx" title="Native defaults" caption="No custom stylesheet." />}}
{{< jsx src="Form.jsx" mode="sandbox" height=480 title="Native frame defaults" caption="The same controls in a sandbox." appearance="card" />}}
{{< jsx src="Custom.jsx" css="custom.css" title="Author customization" appearance="card" />}}
''')
write('content/styling/Form.jsx', style_code)
write('content/styling/Custom.jsx', style_code.replace('jsx-stack style-probe', 'jsx-stack style-probe author-ui'))
write('content/styling/custom.css', '.author-ui .jsx-result { border-inline-start-width: 7px; } .author-ui .jsx-note { color: var(--accent); }')
# Layout wrappers must remain equivalent to the existing native CSS classes.
layout_code = '''import {useId, useRef, useState} from 'react';
import {Stack, Row} from 'sidera/ui';
export default function Layouts(){
 const id=useId(), ref=useRef(null);const [count,setCount]=useState(0);
 return <Stack id={id} className="layout-probe" data-probe="layouts">
  {['none','small','normal','large'].map(gap=><Stack key={gap} data-gap-case={gap}>
   <Stack gap={gap} data-layout="stack"><span>A</span><span>B</span></Stack>
   <div className={'jsx-stack'+(gap==='normal'?'':' jsx-gap-'+gap)} data-native="stack"><span>A</span><span>B</span></div>
   <Row gap={gap} data-layout="row"><button>First deliberately wide action</button><button>Second deliberately wide action</button></Row>
   <div className={'jsx-row'+(gap==='normal'?'':' jsx-gap-'+gap)} data-native="row"><button>First deliberately wide action</button><button>Second deliberately wide action</button></div>
  </Stack>)}
  <Row ref={ref} className="custom-layout" role="group" aria-label="Layout actions" data-events="true" style={{gap:'7px'}}
    onClick={()=>setCount(value=>value+(ref.current?.tagName==='DIV'?1:100))}>
   <button type="button">Count click</button>
  </Row>
  <output aria-live="polite">{count}</output>
 </Stack>;
}'''
write('content/layouts/index.md', '''---
title: Minimal layout wrappers
---
{{< jsx src="Layouts.jsx" css="custom.css" title="Page layouts" />}}
{{< jsx src="Layouts.jsx" css="custom.css" mode="sandbox" height=1200 title="Sandbox layouts" />}}
''')
write('content/layouts/Layouts.jsx', layout_code)
write('content/layouts/custom.css', '.layout-probe .custom-layout { justify-content: flex-end; }')
# Invalid gap values fail locally through the ordinary JSX error boundary.
write('content/layout-failure/index.md', '''---
title: Invalid layout gap
---
```jsx-live
import {Stack} from 'sidera/ui'; export default ()=> <Stack gap="unknown">Invalid</Stack>;
```
```jsx-live {mode="sandbox"}
import {Row} from 'sidera/ui'; export default ()=> <Row gap="constructor">Invalid</Row>;
```
''')
# Compile complete examples from the actual manual, not a second hand-copied API.
manual = (THEME / 'docs/content/authoring/jsx.md').read_text()
examples = [body for body in re.findall(r'^```(?:jsx|jsx-live[^\n]*)\n(.*?)^```$', manual, re.M | re.S)
            if 'export default function' in body]
assert len(examples) >= 4, 'Expected complete fence, layout, form and page-integration examples'
write('content/manual-examples/index.md', '---\ntitle: Manual examples\n---\n' +
      '\n\n'.join('```jsx-live\n' + body + '\n```' for body in examples))
for css_class in ['jsx-stack', 'jsx-row', 'jsx-field', 'jsx-note', 'jsx-error', 'jsx-result',
                  'jsx-metric', 'jsx-gap-none', 'jsx-gap-small', 'jsx-gap-large']:
    assert f'`{css_class}`' in manual, css_class
    assert '.' + css_class in (THEME / 'assets/css/jsx.css').read_text(), css_class
write('content/private/index.md' , '---\ntitle: Draft\ndraft: true\n---\n```jsx-live\nexport default function Draft(){return <p>PRIVATE-JSX-SENTINEL</p>;}\n```')
for mode in ['Content', 'Summary', 'Plain']:
    write(f'content/host-{mode.lower()}.md', f'---\ntitle: Host {mode}\nlayout: host-{mode.lower()}\n---\n')
    write(f'layouts/host-{mode.lower()}.html', '{{ define "main" }}{{ $p := site.GetPage "/widgets" }}{{ partial "sidera/shell.html" (dict "Page" . "Content" $p.' + mode + ') }}{{ end }}')

for name, overlay in [('baseline', ''), ('prefix', "baseURL='https://example.invalid/sidera-showcase/'\n"),
                       ('chinese', "defaultContentLanguage='zh'\nlocale='zh-CN'\n")]:
    out = build(name, overlay)
    text = (out / 'widgets/index.html').read_text()
    dom = DOM(text)
    assert sum('data-sidera-jsx' in a for _, a in dom.nodes) == 7
    assert 'Caption &lt;&amp;&gt;' in text and 'Title &lt;&amp;&gt;' in text and 'Readable fallback' in text
    figures = re.findall(r'<figure\b[^>]*data-sidera-jsx\b.*?</figure>', text, re.S)
    assert len(figures) == 7
    for index, figure in enumerate(figures):
        nodes = DOM(figure).nodes
        attrs = nodes[0][1]
        assert attrs['data-appearance'] == ('card' if index in (1, 3) else 'plain')
        title = [i for i, (_, a) in enumerate(nodes) if a.get('class') == 'jsx-title']
        body = next(i for i, (_, a) in enumerate(nodes) if a.get('class') == 'jsx-root')
        assert bool(title) == (index < 4)
        if title:
            assert title[0] < body and nodes[title[0]][0] == 'div'
        caption = [i for i, (tag, _) in enumerate(nodes) if tag == 'figcaption']
        assert bool(caption) == (index < 2)
        if caption:
            assert caption[0] == len(nodes) - 1 and caption[0] > body
    assert DOM(figures[0]).nodes[0][1]['data-label'] == 'Title <&>'
    assert DOM(figures[3]).nodes[0][1]['data-label'] == 'Frame title'
    assert sum('data-sidera-jsx-script' in a for _, a in dom.nodes) == 1
    assert sum(a.get('type') == 'importmap' for _, a in dom.nodes) == 1
    assert 'jsx-source' not in text and 'View JSX source' not in text
    assert 'const [n,set]' not in text, 'Executable source is not embedded as article text'
    assert '此组件需要 JavaScript。' in text if name == 'chinese' else 'This component needs JavaScript.' in text
    for route in ['ordinary', 'literal', 'host-plain']:
        assert 'type="importmap"' not in (out / route / 'index.html').read_text(), route
    for route in ['host-content', 'host-summary']:
        assert 'data-sidera-jsx-script' in (out / route / 'index.html').read_text(), route
    from urllib.parse import urlsplit
    for _, attrs in dom.nodes:
        if 'data-sidera-jsx' not in attrs:
            continue
        url = attrs['data-module']
        assert url.startswith('/sidera-showcase/') if name == 'prefix' else url.startswith('/jsx/')
        file = out / urlsplit(url).path.removeprefix('/sidera-showcase').lstrip('/')
        assert file.is_file(), file
        if attrs['data-mode'] == 'sandbox':
            frame = file.read_text()
            assert "connect-src 'none'" in frame and 'type="module"' not in frame
    styling = DOM((out / 'styling/index.html').read_text())
    islands = [a for _, a in styling.nodes if 'data-sidera-jsx' in a]
    assert [a['data-mode'] for a in islands] == ['page', 'sandbox', 'page']
    assert [bool(a['data-css']) for a in islands] == [False, False, True]
    assert len(list((out / 'jsx').glob('react-runtime.*.js'))) == 1
    assert not (out / 'private').exists()
    assert all('PRIVATE-JSX-SENTINEL' not in f.read_text() for f in (out / 'jsx').rglob('*.js'))
    assert 'runtime-only-probe' in ''.join(f.read_text() for f in (out / 'jsx/components').glob('*.js'))

# Editing an imported file must not return a stale native js.Build cache product.
write('content/widgets/widgets/helper.js', "export const value='dependency-two';")
out = build('dependency-change')
modules = ''.join(f.read_text() for f in (out / 'jsx/components').glob('*.js'))
assert 'dependency-two' in modules and 'dependency-one' not in modules
build('disabled', '[params]\njsx=false\n', False)
build('bad-opt-in', '[params]\njsx="yes"\n', False)

invalid = {
    'missing': '{{< jsx src="missing.jsx" />}}',
    'traversal': '{{< jsx src="../Tool.jsx" />}}',
    'remote': '{{< jsx src="https://example.org/widget.jsx" />}}',
    'wildcard': '{{< jsx src="widgets/*.jsx" />}}',
    'competing': '{{< jsx src="widgets/Tool.jsx" >}}export default 1{{< /jsx >}}',
    'empty': '{{< jsx />}}',
    'unknown': '{{< jsx src="widgets/Tool.jsx" wat="x" />}}',
    'mode': '{{< jsx src="widgets/Tool.jsx" mode="unsafe" />}}',
    'appearance': '{{< jsx src="widgets/Tool.jsx" appearance="borderless" />}}',
    'blank-appearance': '{{< jsx src="widgets/Tool.jsx" appearance=" " />}}',
    'appearance-type': '{{< jsx src="widgets/Tool.jsx" appearance=true />}}',
    'blank-title': '{{< jsx src="widgets/Tool.jsx" title=" " />}}',
    'title-type': '{{< jsx src="widgets/Tool.jsx" title=true />}}',
    'fence-appearance': '```jsx-live {src="widgets/Tool.jsx" appearance="other"}\n```',
    'height': '{{< jsx src="widgets/Tool.jsx" mode="sandbox" height=0 />}}',
    'page-height': '{{< jsx src="widgets/Tool.jsx" height=200 />}}',
    'css-path': '{{< jsx src="widgets/Tool.jsx" css="../tool.css" />}}',
    'syntax': '```jsx-live\nexport default function W(){return <Unclosed>}\n```',
    'layout-export': "```jsx-live\nimport {Grid} from 'sidera/ui'; export default () => <Grid/>;\n```",
    'css-import': "```jsx-live\nimport './widgets/tool.css'; export default () => <p>test</p>;\n```",
}
for name, body in invalid.items():
    write('content/widgets/index.md', '---\ntitle: Invalid\n---\n' + body)
    build('invalid-' + name, success=False)
manifest = json.loads((THEME / 'assets/vendor/react-19.3.0/provenance.json').read_text())
for filename, digest in manifest['files'].items():
    assert hashlib.sha256((THEME / 'assets/vendor/react-19.3.0' / filename).read_bytes()).hexdigest() == digest
assert (THEME / 'THIRD-PARTY-NOTICES.md').read_bytes() == (THEME / 'assets/licenses/sidera-third-party.txt').read_bytes()
print('PASS JSX: authoring forms, import contexts, nested composition, prefix, locales, conditional assets, manual examples/classes, dependency rebuild, draft boundary, compile-only execution, invalid inputs and vendor integrity')
print(RUN)
