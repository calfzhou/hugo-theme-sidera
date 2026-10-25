"""Native rich-table topology, HTML semantics, boundaries and composition.
Run with a fresh absolute output directory; no consumer/reference checkout needed.
The showcase browser peer consumes baseline-public and override-public.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import random
import subprocess
import sys

THEME = Path(__file__).resolve().parents[1]
RUN = Path(sys.argv[1]).resolve()
SITE = RUN / 'site'
SITE.mkdir(parents=True, exist_ok=False)
passed = []


def write(name, text):
    path = SITE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def build(name, diagnostic=None, flags=()):
    out = RUN / (name + '-public')
    result = subprocess.run(['hugo', '--source', str(SITE), '--destination', str(out),
        '--cacheDir', str(RUN / (name + '-cache')), '--noBuildLock', '--minify',
        '--panicOnWarning', '--printPathWarnings', '--printI18nWarnings', *flags],
        capture_output=True, text=True, timeout=90)
    log = result.stdout + result.stderr
    (RUN / (name + '.log')).write_text(log)
    if diagnostic:
        assert result.returncode and diagnostic in log and 'negative' in log, (name, log)
    else:
        assert result.returncode == 0, (name, log)
    passed.append(name)
    return out


class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children, self.parts = tag, dict(attrs), [], []
    def all(self, tag=None, cls=None):
        return [n for c in self.children for n in [c, *c.all()]
                if (tag is None or n.tag == tag) and (cls is None or cls in n.attrs.get('class', '').split())]
    def text(self):
        return ''.join(p if isinstance(p, str) else p.text() for p in self.parts)


class HTML(HTMLParser):
    def __init__(self, raw):
        super().__init__()
        self.root = Node()
        self.stack = [self.root]
        self.feed(raw)
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        self.stack[-1].parts.append(node)
        if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:
            self.stack.append(node)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                return
    def handle_data(self, text):
        self.stack[-1].parts.append(text)


write('hugo.toml', f'''baseURL='https://example.invalid/preview/'
title='Rich table checks'
theme='sidera'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[params]
search=true
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
[markup.goldmark.extensions.passthrough]
_merge='deep'
[markup.goldmark.extensions.passthrough.delimiters]
_merge='shallow'
[markup.highlight]
lineNos=true
lineNumbersInTable=true
''')
legacy = {'headers': [{'text': name, 'colspan': 2} for name in ['A series','B series','C series']],
          'rows': [['A0','841 × 1189','B0','1000 × 1414','C0','917 × 1297'],
                   ['A4','210 × 297','B4','250 × 353','C4','229 × 324']]}
merged = {'headers': [[{'text':'Series','rowspan':2}, {'text':'Paper','colspan':2}],
                      ['Size','Dimensions (mm)']],
          'rows': [[{'text':'A series','header':'row','rowspan':2},'A4','210 × 297'],
                   ['A3','297 × 420'], ['Notes', {'text':'- Markdown **lists**\n- [Source](source.txt)\n- $x^2$', 'colspan':2}],
                   ['Code', {'text':'```python\nprint("<unsafe> is code")\n```', 'colspan':2}]],
          'columns': [{'min_width':100}, {'align':'center','min_width':80}, {'align':'end','min_width':180}]}
body_spans = {'headers': ['Group','A','B','C'], 'rows': [
    [{'text':'Block','rowspan':2,'colspan':2},'x','y'], ['z','w'],
    [{'text':'All columns','colspan':4}], ['','','','']]}
covered = {'headers': [[{'text':'H','colspan':2,'rowspan':2}], []],
           'rows': [[{'text':'Whole body','rowspan':2,'colspan':2}], []]}
long = {'headers': merged['headers'], 'columns': merged['columns'],
        'rows': [[{'text':f'Group {i}','header':'row'}, f'A{i}', f'{i} × {i+1}'] for i in range(1,31)]}
write('content/tables/data.yml', 'headers: ["File header"]\nrows:\n  - - "[A native link](source.txt)"\n')
write('content/tables/data.json', json.dumps(merged))
write('content/tables/source.txt','Native attachment.\n')

def shortcode(data, args=''):
    return '{{< rich-table ' + args + ' >}}\n' + json.dumps(data, ensure_ascii=False) + '\n{{< /rich-table >}}\n'

write('layouts/_shortcodes/caption-reference.html', '<figure class="caption-reference"><div>Caption styling reference</div><figcaption>Standard Sidera caption</figcaption></figure>')
body = '''---
title: Rich tables
---
## Ordinary table and caption reference

| Label | Value |
| --- | --- |
| Reference | One |
| Another | Two |

| Label | Value |
| --- | --- |
| Grid reference | One |
| Another | Two |
{.table-grid #plain-grid}

{{< caption-reference >}}

## Grouped headers
''' + shortcode(legacy, 'caption="Paper series" id="legacy"') + '''
## Merged cells and Markdown
''' + shortcode(merged, 'caption="Paper sizes" row_headers=true id="merged"') + '''
## Body rectangles
''' + shortcode(body_spans, 'caption="Rectangular body spans" borders="grid" id="rectangles"') + shortcode(covered) + '''
## Sticky reading window
''' + shortcode(long, 'caption="Sticky headers and first column" borders="grid" sticky_header=true sticky_first_column=true max_height=240 id="sticky"') + '''
## Headerless table
''' + shortcode({'rows': [['Label','Value'],['Two','2']]}, 'row_headers=true') + '''
{{% tabs label="Table container" %}}
{{< tab title="Inside a fold and grid" >}}
{{< folding title="Open the table" >}}
{{< grid columns=1 >}}
{{< cell >}}
{{< rich-table src="data.yml" caption="File table" />}}
{{< /cell >}}
{{< /grid >}}
{{< /folding >}}
{{< /tab >}}
{{% /tabs %}}

{{< rich-table src="data.json" caption="JSON table" borders="rows" />}}

<!--more-->

Following text remains ordinary prose.
'''
write('content/tables/index.md', body)
write('content/tables/index.zh.md', body)
yaml_table = """columns:
  - {min_width: 100}
  - {align: center, min_width: 80}
  - {align: end, min_width: 180}
headers:
  - - {text: Series, rowspan: 2}
    - {text: Paper, colspan: 2}
  - [Size, Dimensions]
rows:
  - - {text: A series, header: row, rowspan: 2}
    - A4
    - "210 × 297"
  - [A3, "297 × 420"]
"""
write('content/yaml/index.md','---\ntitle: Native YAML\n---\n{{< rich-table >}}\n'+yaml_table+'{{< /rich-table >}}\n{{< rich-table src="table.yaml" />}}\n')
write('content/yaml/table.yaml', yaml_table)
write('content/quiet.md', '---\ntitle: Quiet\n---\nAn ordinary | sentence.\n')
write('content/plain.md', '---\ntitle: Plain\nlayout: plain\n---\n')
write('layouts/plain.html','{{ define "main" }}<main id="main">{{ (site.GetPage "/tables").Plain }}</main>{{ end }}')
write('content/host.md','---\ntitle: Repeated table host\nlayout: host\n---\n')
# Drop author IDs for the repeat fixture; author-supplied IDs are their responsibility.
write('content/repeated/index.md', body.replace(' id="legacy"','').replace(' id="merged"','').replace(' id="rectangles"','').replace(' id="sticky"',''))
for name in ['data.yml','data.json','source.txt']:
    write('content/repeated/'+name, (SITE/'content/tables'/name).read_text())
write('layouts/host.html', '''{{ define "main" }}{{ $p := site.GetPage "/repeated" }}{{ $html := printf `<div class="prose">%s%s%s</div>` $p.Content $p.Content $p.Summary | safeHTML }}{{ partial "sidera/shell.html" (dict "Page" . "Content" $html) }}{{ end }}''')


# Vary span rectangles independently of the template's placement implementation.
rng = random.Random(47)
random_grids = []
random_sources = []
for case in range(10):
    height, width = 5, 6
    grid = [[None] * width for _ in range(height)]
    rows = [[] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if grid[y][x] is not None:
                continue
            rectangles = [(h, w) for h in range(1, min(3, height-y)+1) for w in range(1, min(3, width-x)+1)
                          if all(grid[yy][xx] is None for yy in range(y, y+h) for xx in range(x, x+w))]
            h, w = rng.choice(rectangles)
            label = f"cell-{case}-{y}-{x}"
            rows[y].append({'text': label, 'rowspan': h, 'colspan': w})
            for yy in range(y, y+h):
                for xx in range(x, x+w):
                    grid[yy][xx] = label
    random_sources.append(shortcode({'headers':['A','B','C','D','E','F'], 'rows':rows}))
    random_grids.append(grid)
write('content/rectangles.md', '---\ntitle: Generated rectangles\n---\n' + '\n'.join(random_sources))
write('content/plain-slot.md', '---\ntitle: Plain shell slot\nlayout: plain-slot\n---\n')
write('layouts/plain-slot.html', '{{ define "main" }}{{ partial "sidera/shell.html" (dict "Page" . "Content" "<em>Literal string stays escaped</em>") }}{{ end }}')

def verify(raw, expected_count):
    root = HTML(raw).root
    tables = root.all(cls='rich-table')
    assert len(tables) == expected_count, len(tables)
    generated = []
    for table in tables:
        heads = {n.attrs['id']: n for n in table.all('th') if 'id' in n.attrs}
        generated.extend(heads)
        for cell in table.all():
            if cell.tag in ['td','th']:
                for key in cell.attrs.get('headers', '').split():
                    assert key in heads, (key, list(heads))
                    assert key != cell.attrs.get('id'), 'No self-reference'
    assert len(generated) == len(set(generated)), 'Generated IDs must be unique even in repeated Content/Summary'
    captions = root.all('figcaption')
    caption_ids = {n.attrs['id']:n for n in captions if 'id' in n.attrs}
    assert len(caption_ids) == sum('id' in n.attrs for n in captions)
    for figure in root.all(cls='content-rich-table'):
        assert figure.tag == 'figure'
        scroll = next(n for n in figure.children if 'rich-table-scroll' in n.attrs.get('class','').split())
        table = next(n for n in scroll.children if n.tag == 'table')
        assert not [n for n in table.children if n.tag == 'caption']
        visible = [n for n in figure.children if n.tag == 'figcaption']
        if visible:
            assert figure.children[-1] is visible[0]
            assert table.attrs['aria-labelledby'] == visible[0].attrs['id']
            assert visible[0].attrs['id'] in caption_ids
        else:
            assert table.attrs['aria-label']

    assert 'sidera-rich-table-start' not in raw and 'sidera-rich-table-end' not in raw
    assert 'sidera-inline:' not in raw and 'data-sidera-leaf=' not in raw
    return root

for name, flags in [('baseline',()), ('root',('--baseURL','https://example.invalid/'))]:
    out = build(name, flags=flags)
    for locale in ['', 'zh/']:
        raw = (out/locale/'tables/index.html').read_text()
        root = verify(raw, 8)
        assert len(root.all(cls='content-rich-table')) == 8
        assert len(root.all(cls='table-grid')) == 1
        assert root.all(cls='table-grid')[0].attrs['id'] == 'plain-grid'
        for figure in root.all(cls='content-rich-table'):
            mode = 'grid' if figure.attrs.get('id') in ['rectangles','sticky'] else 'rows'
            assert figure.all(cls='rich-table')[0].attrs['data-borders'] == mode

        table = next(n for n in root.all(cls='content-rich-table') if n.attrs.get('id') == 'merged').all(cls='rich-table')[0]
        ths = table.all('th')
        series = next(n for n in ths if n.text().strip() == 'Series')
        group = next(n for n in ths if n.text().strip() == 'Paper')
        rowhead = next(n for n in ths if n.text().strip() == 'A series')
        size = next(n for n in ths if n.text().strip() == 'Size')
        a3 = next(n for n in table.all('td') if n.text().strip() == 'A3')
        assert series.attrs['rowspan'] == '2' and group.attrs['colspan'] == '2'
        assert rowhead.attrs['rowspan'] == '2'
        assert set(a3.attrs['headers'].split()) == {group.attrs['id'], size.attrs['id'], rowhead.attrs['id']}
        assert table.all('ul') and table.all(cls='code-block') and table.all(cls='lntable')
        assert 'data-sidera-math' in raw
        assert not table.all('script')
        assert root.all(cls='rich-table')[0].all('th')[0].attrs['colspan'] == '2'
        assert any(a.attrs.get('href') == ('/' if name == 'root' else '/preview/') + 'tables/source.txt' for a in root.all('a'))
        assert any(n.attrs.get('aria-label') == ('可滚动的数据表格' if locale else 'Scrollable data table') for n in root.all(cls='rich-table-scroll'))
    verify((out/'host/index.html').read_text(),24)
    yaml_root = verify((out/'yaml/index.html').read_text(),2)
    assert sum(n.attrs.get('rowspan') == '2' for n in yaml_root.all('th')) == 4
    assert sum(n.attrs.get('colspan') == '2' for n in yaml_root.all('th')) == 2
    rectangles = verify((out/'rectangles/index.html').read_text(),10).all(cls='rich-table')
    for table, expected in zip(rectangles, random_grids):
        grid = [[None] * 6 for _ in range(5)]
        tbody = next(n for n in table.children if n.tag == 'tbody')
        for y, tr in enumerate(tbody.children):
            cursor = 0
            for cell in tr.children:
                while grid[y][cursor] is not None:
                    cursor += 1
                for yy in range(y, y+int(cell.attrs['rowspan'])):
                    for xx in range(cursor, cursor+int(cell.attrs['colspan'])):
                        assert grid[yy][xx] is None
                        grid[yy][xx] = cell.text().strip()
                cursor += int(cell.attrs['colspan'])
        assert grid == expected
    assert 'Literal string stays escaped' in (out/'plain-slot/index.html').read_text()
    assert not HTML((out/'plain-slot/index.html').read_text()).root.all('em')
    for index_file in (out/'search').glob('*.json'):
        assert 'sidera-rich-table' not in index_file.read_text() and 'sidera-rt-' not in index_file.read_text()
    assert not HTML((out/'plain/index.html').read_text()).root.all(cls='rich-table')
    assert 'Whole body' in (out/'plain/index.html').read_text()

# Diagnose bad author data before HTML emission; no browser repair of invalid grids.
bad = [
    ('yaml-zero', 'rows: [[{text: X, colspan: 0}]]', '', 'integer in 1'),
    ('yaml-fraction', 'rows: [[{text: X, colspan: 1.5}]]', '', 'integer in 1'),
    ('yaml-string', 'rows: [[{text: X, colspan: \"2\"}]]', '', 'must be an integer'),
    ('yaml-large', 'rows: [[{text: X, colspan: 18446744073709551615}]]', '', 'integer in 1'),
    ('border-enum', '{"rows":[["x"]]}', 'borders="all"', 'borders must be rows or grid'),
    ('border-empty', '{"rows":[["x"]]}', 'borders=""', 'borders must be rows or grid'),
    ('border-type', '{"rows":[["x"]]}', 'borders=true', 'must be a string'),
    ('empty', '{}', '', 'nonempty body'),
    ('missing-rows', '{"headers":["A"]}', '', 'body must be an array'),
    ('scalar', '"hello"', '', 'object with headers/rows'),
    ('header-type', '{"headers":"bad","rows":[["x"]]}', '', 'headers must be an array'),
    ('header-empty-row', '{"headers":[[]],"rows":[["x"]]}', '', 'header rows must define'),
    ('mixed-header', '{"headers":[["a"],"b"],"rows":[["x"]]}', '', 'row 2 must be an array'),
    ('ragged', '{"headers":["a","b"],"rows":[["x"]]}', '', 'unfilled column'),
    ('wide', '{"headers":["a"],"rows":[["x","y"]]}', '', 'exceeds table width'),
    ('overlap', json.dumps({'headers':['A','B','C'], 'rows':[['a',{'text':'b','rowspan':2},'c'],[{'text':'bad','colspan':2},'d']]}), '', 'overlaps a previous span'),
    ('head-body-cross', json.dumps({'headers':[[{'text':'a','rowspan':2}]],'rows':[['b']]}), '', 'crosses the head section boundary'),
    ('body-cross', json.dumps({'rows':[[{'text':'a','rowspan':2}]]}), '', 'crosses the body section boundary'),
    ('zero', '{"rows":[[{"text":"x","rowspan":0}]]}', '', 'integer in 1'),
    ('fraction', '{"rows":[[{"text":"x","colspan":1.5}]]}', '', 'integer in 1'),
    ('span-string', '{"rows":[[{"text":"x","colspan":"2"}]]}', '', 'must be an integer'),
    ('span-bool', '{"rows":[[{"text":"x","colspan":true}]]}', '', 'must be an integer'),
    ('cell-numeric', '{"rows":[[42]]}', '', 'quote numeric text'),
    ('cell-missing-text', '{"rows":[[{"colspan":1}]]}', '', 'requires text'),
    ('cell-key', '{"rows":[[{"text":"x","style":"color:red"}]]}', '', 'unsupported cell key'),
    ('cell-header', '{"rows":[[{"text":"x","header":"col"}]]}', '', 'header must be row or data'),
    ('head-row-header', '{"headers":[{"text":"x","header":"row"}],"rows":[["x"]]}', '', 'only valid in body'),
    ('column-count', '{"columns":[{}],"rows":[["a","b"]]}', '', 'columns must match'),
    ('column-width', '{"columns":[{"min_width":-3}],"rows":[["a"]]}', '', '32..720'),
    ('column-type', '{"columns":[{"min_width":"140"}],"rows":[["a"]]}', '', 'must be an integer'),
    ('column-align', '{"columns":[{"align":"left"}],"rows":[["a"]]}', '', 'align must be'),
    ('data-key', '{"rows":[["x"]],"style":"bad"}', '', 'unsupported data key'),
    ('cell-heading', '{"rows":[["# Not a cell heading"]]}', '', 'not headings'),
    ('raw-html', '{"rows":[["<script>bad()</script>"]]}', '', 'Raw HTML omitted'),
    ('boolean-param', '{"rows":[["x"]]}', 'row_headers="true"', 'must be a boolean'),
    ('unknown-param', '{"rows":[["x"]]}', 'onclick="bad"', 'unsupported parameter'),
    ('width-param', '{"rows":[["x"]]}', 'cellwidth=0', '32..720'),
    ('height-param', '{"rows":[["x"]]}', 'max_height=10', '160..1200'),
    ('class', '{"rows":[["x"]]}', 'class="bad()"', 'invalid class'),
    ('src-body', '{"rows":[["x"]]}', 'src="x.yml"', 'choose src or'),
    ('src-path', '', 'src="../secret.yml"', 'exact local'),
    ('src-url', '', 'src="https://example.org/a.json"', 'exact local'),
    ('src-missing', '', 'src="missing.yml"', 'missing page resource'),
    ('sticky-span', '{"rows":[[{"text":"x","colspan":2}]]}', 'sticky_first_column=true', 'first-column cells'),
    ('row-limit', json.dumps({'rows':[['x']] * 201}), '', 'exceeds 200 rows'),
    ('column-limit', json.dumps({'rows':[['x'] * 33]}), '', 'exceeds 32 columns'),
    ('text-limit', json.dumps({'rows':[['x' * 16385]]}), '', 'exceeds 16 KiB'),
    ('bytes-limit', 'x' * 262145, '', '256 KiB'),
]
for name, data, args, message in bad:
    write('content/negative.md', '---\ntitle: Negative\n---\n{{< rich-table '+args+' >}}\n'+data+'\n{{< /rich-table >}}')
    build('reject-'+name, message)
write('content/negative.md','---\ntitle: Repaired\n---\nValid.')
# Trusted site styles remain ordinary native overrides, not template style strings.
write('layouts/_partials/sidera/head-extra.html','<style>.content-rich-table { --line: rgb(100, 90, 80); }</style>')
build('override')
(RUN/'results.json').write_text(json.dumps({'passed':passed},indent=2)+'\n')
print('PASS rich tables:',len(passed),'builds; retained:',RUN)
