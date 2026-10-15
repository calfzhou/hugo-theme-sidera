"""Native Hugo watch rebuild of an imported JSX dependency. Owned server only."""
from pathlib import Path
import json
import os
import re
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
RUN.mkdir(parents=True, exist_ok=False)
SITE = RUN / 'site'
(SITE / 'content/tool/widgets').mkdir(parents=True)
port = int(os.environ.get('SIDERA_HTTP_PORT', '14984'))
with socket.socket() as probe:
    probe.bind(('127.0.0.1', port))
(SITE / 'hugo.toml').write_text(f'''baseURL='http://127.0.0.1:{port}/sidera-showcase/'
title='JSX watch checks'
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
(SITE / 'content/tool/index.md').write_text('''---
title: Watch test
---
{{< jsx src="widgets/Tool.jsx" />}}
''')
(SITE / 'content/tool/widgets/Tool.jsx').write_text("import {value} from './widgets/helper.js';import {Stack} from 'sidera/ui';export default function W(){return <Stack><p>{value}</p></Stack>}")
helper = SITE / 'content/tool/widgets/helper.js'
helper.write_text("export const value='before-watch';")
layout = SITE / 'assets/js/jsx/layout.jsx'
layout.parent.mkdir(parents=True)
layout.write_text((THEME / 'assets/js/jsx/layout.jsx').read_text().replace('Sidera layout:', 'before-layout-watch:'))
origin = f'http://127.0.0.1:{port}'

def rendered(marker):
    html = urlopen(origin + '/sidera-showcase/tool/', timeout=2).read().decode()
    url = re.search(r'data-module="([^"]+)"', html)[1]
    js = urlopen(origin + url, timeout=2).read().decode()
    return url if marker in js else None

def wait(marker):
    for _ in range(150):
        assert server.poll() is None, 'Owned Hugo server exited'
        try:
            url = rendered(marker)
            if url: return url
        except (OSError, TypeError): pass
        time.sleep(.1)
    raise AssertionError(f'Hugo did not serve {marker}; see {RUN / "hugo.log"}')

with (RUN / 'hugo.log').open('w') as log:
    server = subprocess.Popen(['hugo', 'server', '--source', str(SITE), '--port', str(port),
        '--bind', '127.0.0.1', '--baseURL', origin + '/sidera-showcase/', '--disableFastRender',
        '--noBuildLock', '--destination', str(RUN / 'public'), '--cacheDir', str(RUN / 'cache'),
        '--panicOnWarning'], stdout=log, stderr=log)
    try:
        first = wait('before-watch')
        helper.write_text("export const value='after-watch';")
        second = wait('after-watch')
        assert first != second, 'Dependency edit must change the fingerprint'
        layout.write_text(layout.read_text().replace('before-layout-watch:', 'after-layout-watch:'))
        third = wait('after-layout-watch:')
        assert third != second, 'Native layout asset edit must change the fingerprint'
        (SITE / 'content/tool/index.md').write_text('''---
title: Watch test
---
```jsx-live
export default function Updated(){return <p>changed-fence</p>}
```
''')
        assert wait('changed-fence') != third
        print('PASS native JSX preview: helper, native layout asset and Markdown edits rebuild fingerprinted modules')
    finally:
        server.terminate()
        try: server.wait(timeout=8)
        except subprocess.TimeoutExpired: server.kill(); server.wait(timeout=5)
