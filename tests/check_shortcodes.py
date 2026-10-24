"""Inline controls, downloads and tabs: native composition, safety and fallbacks.
Usage: uv run --no-project --no-managed-python python3 tests/check_shortcodes.py <fresh-output>
The showcase browser peer consumes baseline-public; no real-site dependency.
"""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
SITE = RUN / 'site'
SITE.mkdir(parents=True, exist_ok=False)
passed = []


def write(path, text):
    target = SITE / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


def build(name, diagnostic=None, flags=()):
    out = RUN / (name + '-public')
    p = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
        '--cacheDir', str(RUN / (name + '-cache')), '--noBuildLock', '--minify',
        '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings', *flags],
        capture_output=True, text=True, timeout=60)
    log = p.stdout + p.stderr
    (RUN / (name + '.log')).write_text(log)
    if diagnostic:
        assert p.returncode and diagnostic in log and ('negative' in log or diagnostic == 'unknown icon'), (name, log)
    else:
        assert p.returncode == 0, (name, log)
    passed.append(name)
    return out


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


write('hugo.toml', f'''baseURL='https://example.invalid/preview/'
title='Shortcode checks'
theme='sidera'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[params]
search=false
search_index=true
page_reveal=false
[languages.en]
weight=1
locale='en-US'
[languages.zh]
weight=2
locale='zh-CN'
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[markup.goldmark.parser]
_merge='deep'
[markup.goldmark.parser.attribute]
_merge='shallow'
[markup.highlight]
lineNos=true
lineNumbersInTable=true
''')
write('data/icons.yaml', 'custom-test: \'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M2 2H22V22H2Z"/></svg>\'\n')
body = '''---
title: Shortcode controls
---
## Inline details

A{{< icon name="custom-test" color="purple" label="Custom square" >}}B
{{< icon name="star" >}}
{{< hashtag text="Local notes" >}} {{< hashtag text="Linked notes" href="/controls/#second-heading" color="cyan" >}}
{{< hashtag text="External" href="https://example.org/" color="pink" >}}

A{{< emp text="Emphasis" >}}B{{< wavy text="Wave" >}}C{{< del text="Removed" >}}D{{< sup text="2" >}}E{{< sub text="n" >}}F

{{< blur text="Blurred answer" >}} {{< psw text="Spoiler answer" >}}

Hover or focus {{< tip text="A helpful annotation with <escaped> text & no HTML." >}}this **term**{{< /tip >}}.

Inline: A{{< code-inline lang="python" >}}print("你好  <&>"){{< /code-inline >}}B.
HTML: A{{< code-inline lang="html" >}}<b>Hi</b>{{< /code-inline >}}B.
PHP: A{{< code-inline lang="php" >}}<?php echo "hello"; ?>{{< /code-inline >}}B.
Unknown: {{< code-inline lang="not-a-lexer" >}}  <tag>&  {{< /code-inline >}}.

{{< download src="attachments/数据.txt" name="Report 数据.txt" text="Download data" >}}
{{< download src="binary.bin" >}}

{{% tabs active=2 label="Setup method" align="center" id="methods" %}}
{{< tab title="Overview" >}}
## First heading

First panel with **Markdown** and {{< icon name="custom-test" color="red" >}}.

{{< code-inline lang="js" >}}const value = 1;{{< /code-inline >}}

{{< download src="attachments/数据.txt" >}}

{{< tip text="Nested annotation" >}}nested *term*{{< /tip >}}
{{< /tab >}}
{{< tab title="Details" >}}
## Second heading

Second panel with [a native anchor](#first-heading).

{{< box title="Inside a tab" color="yellow" >}}
{{< hashtag text="Nested" color="purple" href="#first-heading" >}}
{{< /box >}}

```python
print("ordinary code block")
```

{{< tabs label="Nested tabs" >}}
{{< tab title="Inner one" >}}
Inner first.
{{< /tab >}}
{{< tab title="Inner two" >}}
### Deep heading

Deep target.
{{< /tab >}}
{{< /tabs >}}
{{< /tab >}}
{{% /tabs %}}

{{% folding title="Folded tabs" %}}
{{< tabs >}}
{{< tab title="Only" >}}
Inside a fold.
{{< /tab >}}
{{< /tabs >}}
{{% /folding %}}
'''
write('content/controls/index.md', body)
write('content/controls/index.zh.md', body.replace('Shortcode controls', 'Shortcode controls — Chinese UI'))
write('content/controls/attachments/数据.txt', 'Exact bytes: 你好\r\n')
(SITE / 'content/controls/binary.bin').write_bytes(bytes(range(256)))
write('content/quiet.md', '---\ntitle: Quiet\n---\nNo content controls.\n')
write('content/plain-code.md', '---\ntitle: Plain code\n---\n{{< code-inline >}}a  b{{< /code-inline >}}\n')
write('content/literal.md', '---\ntitle: Literal\n---\n```text\n{{</* psw text="not live" */>}}\n```\n')
write('content/host.md', '---\ntitle: Host\nlayout: host\n---\nHost only.\n')
write('layouts/host.html', '''{{ define "main" }}{{ $source := site.GetPage "/controls" }}{{ $body := printf `<div class="prose">%s%s</div>` $source.Content $source.Content | safeHTML }}{{ partial "sidera/shell.html" (dict "Page" . "Content" $body) }}{{ end }}''')
write('content/plain.md', '---\ntitle: Plain\nlayout: plain\n---\n')
write('layouts/plain.html', '''{{ define "main" }}<main id="main">{{ (site.GetPage "/controls").Plain }}</main>{{ end }}''')
# Repeated content copies do not copy authored IDs; an author-supplied id is still
# their responsibility. Remove explicit IDs for the duplicate-content fixture.
write('content/duplicate/index.md', body.replace(' id="methods"', ''))
write('content/duplicate/attachments/数据.txt', 'Exact bytes: 你好\r\n')
(SITE / 'content/duplicate/binary.bin').write_bytes(bytes(range(256)))
write('layouts/host.html', (SITE / 'layouts/host.html').read_text().replace('/controls', '/duplicate'))

for name, flags, prefix in [('baseline', (), '/preview'), ('root', ('--baseURL', 'https://example.invalid/'), '')]:
    out = build(name, flags=flags)
    for lang in ['', 'zh/']:
        raw = (out / lang / 'controls/index.html').read_text()
        nodes = HTML(raw).nodes
        assert sum("content-tabs" in a.get("class", "").split() for t, a in nodes) == 3
        assert sum("content-tab" in a.get("class", "").split() for t, a in nodes) == 5
        assert 'data-sidera-content-controls' in raw
        assert 'data-sidera-leaf=' not in raw and 'sidera-inline:' not in raw and 'data-sidera-container=' not in raw
        assert not any('hidden' in a for t, a in nodes if 'content-tab' in a.get('class', '').split())
        assert not any(a.get('role') == 'tab' for t, a in nodes), 'No dead JS controls in source'
        assert any(a.get('role') == 'img' and a.get('aria-label') == 'Custom square' for t, a in nodes)
        hashtags = [(t, a) for t, a in nodes if a.get('class') == 'content-hashtag']
        assert hashtags[0][0] == 'span' and 'href' not in hashtags[0][1]
        assert hashtags[1][1]['href'] == prefix + '/controls/#second-heading'
        assert any(a.get('href') == '#first-heading' for t, a in nodes)
        assert 'A<span class=content-emp>Emphasis</span>B' in raw
        assert 'class="content-code-inline chroma"' in raw
        inline = re.findall(r'<span class="content-code-inline chroma">(.*?)</code></span>', raw, re.S)
        assert len(inline) == 5 and all('\n' not in code and '<pre' not in code and 'lntable' not in code for code in inline)
        assert all('class=ln' not in code for code in inline)
        assert '<tag>&' in unescape(re.sub('<[^>]+>', '', inline[3]))
        downloads = [a for t, a in nodes if a.get('class') == 'content-download']
        assert downloads[0]['download'] == 'Report 数据.txt'
        assert downloads[0]['href'].startswith(prefix + '/controls/attachments/')
        assert (out / 'controls/binary.bin').read_bytes() == bytes(range(256))
        assert (out / 'controls/attachments/数据.txt').read_bytes() == (SITE / 'content/controls/attachments/数据.txt').read_bytes()
    assert '>a  b</code>' in (out / 'plain-code/index.html').read_text()
    for route in ['quiet', 'literal', 'plain', 'plain-code']:
        assert 'data-sidera-content-controls' not in (out / route / 'index.html').read_text(), route
    assert 'data-sidera-content-controls' in (out / 'host/index.html').read_text()
    plain = unescape(re.sub('<[^>]+>', '', (out / 'plain/index.html').read_text()))
    assert 'Deep target' in plain and 'ordinary code block' in plain

invalid = [
    ('icon-unknown', '{{< icon name="missing" >}}', 'unknown icon'),
    ('icon-url', '{{< icon name="https://example.org/icon.svg" >}}', 'unknown icon'),
    ('icon-type', '{{< icon name=1 >}}', 'must be a string'),
    ('icon-css', '{{< icon name="star" color="#abc" >}}', 'color must be'),
    ('hashtag-script', '{{< hashtag text="x" href="javascript:alert(1)" >}}', 'unsafe URL'),
    ('hashtag-relative', '{{< hashtag text="x" href="//example.org/" >}}', 'unsafe URL'),
    ('hashtag-source', '{{< hashtag text="x" href="missing.md" >}}', 'Sidera link source'),
    ('decoration-param', '{{< emp text="x" style="bad" >}}', 'unsupported parameter'),
    ('decoration-empty', '{{< blur text=" " >}}', 'must be nonblank'),
    ('decoration-position', '{{< psw "x" >}}', 'requires named'),
    ('tip-block', '{{< tip text="x" >}}## Heading{{< /tip >}}', 'noninteractive inline'),
    ('tip-link', '{{< tip text="x" >}}[Link](https://example.org/){{< /tip >}}', 'noninteractive inline'),
    ('tip-empty', '{{< tip text="x" >}} {{< /tip >}}', 'noninteractive inline'),
    ('code-multiline', '{{< code-inline lang="python" >}}a\nb{{< /code-inline >}}', 'single-line'),
    ('code-option', '{{< code-inline options="noClasses=true" >}}a{{< /code-inline >}}', 'unsupported parameter'),
    ('code-positional', '{{< code-inline python >}}a{{< /code-inline >}}', 'requires named'),
    ('download-missing', '{{< download src="missing.zip" >}}', 'missing bundle attachment'),
    ('download-traversal', '{{< download src="../private.txt" >}}', 'invalid resource path'),
    ('download-encoded', '{{< download src="%2e%2e/private.txt" >}}', 'invalid resource path'),
    ('download-glob', '{{< download src="*.txt" >}}', 'invalid resource path'),
    ('download-name', '{{< download src="x.txt" name="../x" >}}', 'name must be a filename'),
    ('tab-parent', '{{% tab title="x" %}}Body{{% /tab %}}', 'requires a tabs parent'),
    ('tabs-empty', '{{% tabs %}} {{% /tabs %}}', 'at least one tab'),
    ('tabs-body', '{{% tabs %}}Extra\n{{< tab title="x" >}}Body{{< /tab >}}{{% /tabs %}}', 'only tab children'),
    ('tabs-child', '{{% tabs %}}{{< mark text="x" >}}{{% /tabs %}}', 'requires tab children'),
    ('tabs-active', '{{% tabs active=2 %}}{{< tab title="x" >}}Body{{< /tab >}}{{% /tabs %}}', 'exceeds tab count'),
    ('tabs-active-type', '{{% tabs active="1" %}}{{< tab title="x" >}}Body{{< /tab >}}{{% /tabs %}}', 'positive integer'),
    ('tabs-align', '{{% tabs align="bad" %}}{{< tab title="x" >}}Body{{< /tab >}}{{% /tabs %}}', 'align must be'),
    ('tabs-title', '{{% tabs %}}{{< tab title=" " >}}Body{{< /tab >}}{{% /tabs %}}', 'nonblank title'),
]
for name, source, diagnostic in invalid:
    write('content/negative.md', '---\ntitle: Negative\n---\n' + source + '\n')
    build('reject-' + name, diagnostic)
write('content/negative.md', '---\ntitle: Repaired\n---\nValid.\n')
write('off.toml', '[params]\nicons=false\n')
out = build('icons-off', flags=('--config', 'hugo.toml,off.toml'))
raw = (out / 'controls/index.html').read_text()
assert '<span class=content-icon' in raw and 'Download data' in raw
assert all('<svg' not in a for a in re.findall(r'<a class=content-download.*?</a>', raw))
(RUN / 'results.json').write_text(json.dumps({'passed': passed}, indent=2) + '\n')
print('PASS shortcodes:', len(passed), 'builds; retained:', RUN)
