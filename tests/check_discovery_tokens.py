"""Exact rendered-text semantics for the local token memo, independent of timing.
No Markdown/raw HTML trust changes; strings enter a template-only test fixture.
"""
from pathlib import Path
import json,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
(SITE/'layouts').mkdir();(SITE/'data').mkdir()
(SITE/'hugo.toml').write_text(f'''baseURL='https://example.invalid/'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['taxonomy','term','RSS','sitemap','404']
[outputs]
home=['JSON']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
''')
cases=[
 ('entities','<p>A &amp; B&nbsp;C</p>','A & B C'),
 ('same-tag-different-ancestry','<div hidden><span class="n">SECRET</span></div><span class="n">Visible</span>','Visible'),
 ('hidden-attribute-value','<span title="hidden aria-hidden data-search-exclude">Visible</span><span hidden>SECRET</span>','Visible'),
 ('skip-control','<p>Before<button><span class="n">SECRET</span></button>After</p>','BeforeAfter'),
 ('captions','<div class="no-caption"><figure><figcaption>SECRET</figcaption></figure></div><figure><figcaption>Caption</figcaption></figure>','Caption'),
 ('code','<pre><code><span class="line"><span class="cl"><span class="k">return</span> <span class="n">value</span> &lt;tag&gt;</span></span></code></pre>','return value <tag>'),
 ('skipped-math','<p>Before<span class="katex"><span class="n">SECRET</span></span>After</p>','BeforeAfter'),
 ('opaque','<!-- SECRET --><script>SECRET</script><style>SECRET</style><template><span>SECRET</span></template><p>Visible</p>','Visible'),
 ('void','<p>A<img hidden src="x"><input value="SECRET">B<br>C</p>','AB C'),
 ('skip-nested-voids','<p>Before</p><div hidden><div><img src="x"><br><span>SECRET</span><hr/></div><span>SECRET</span></div><p>After</p>','Before After'),
 ('skip-self-closing','<p>A<span hidden><i/><span>SECRET</span></span>B</p>','AB'),
 ('skip-caption-state','<div hidden><div class="no-caption"><figure><figcaption>SECRET</figcaption></figure></div></div><figure><figcaption>Visible</figcaption></figure>','Visible'),
 ('caption-skip-nesting','<div class="no-caption"><figure><figcaption><span><b>SECRET</b></span></figcaption><p>Visible</p></figure></div>','Visible'),
 ('quoted-flags','<span title=\'class="katex" hidden data-search-exclude\' aria-label=\'hidden\'>Visible</span><span aria-hidden=\'true\'>SECRET</span><span data-search-exclude=\'\'>SECRET</span>','Visible'),
 ('mixed-attribute-case',"<span CLASS='katex'><b>SECRET</b></span><span HiDdEn>SECRET</span><span CLASS='visible'>Visible</span>",'Visible'),
 ('duplicate-class','<span class="katex" class="visible">Visible</span><span class="visible" class="katex">SECRET</span>','Visible'),
 ('large-excluded-subtree','<p>Before</p><span class="katex">'+('<span><i hidden>SECRET</i><img><br/></span>'*1500)+'</span><p>After</p>','Before After'),
 ('deep-excluded-subtree','<p>Before</p><div hidden>'+('<span>'*80)+'SECRET'+('</span>'*80)+'</div><p>After</p>','Before After'),

]
records=[{'name':n,'html':h,'want':[{'id':'','title':'','text':t}]} for n,h,t in cases]
records.append({'name':'heading-and-state','html':'<p>Intro</p><h2 id="café"><span class="heading-anchor">SECRET</span><span class="heading-text">Name &amp; <span>Code</span></span></h2><p>Body</p><h3 id="next">Next</h3><p>Tail</p>','want':[{'id':'','title':'','text':'Intro'},{'id':'café','title':'Name & Code','text':'Name & Code Body'},{'id':'next','title':'Next','text':'Next Tail'}]})
records.append({'name':'hidden-heading-restores-state','html':'<h2 id="visible">Before<span hidden><h3 id="secret">SECRET</h3><input></span>After</h2><p>Body</p>','want':[{'id':'','title':'','text':''},{'id':'visible','title':'BeforeAfter','text':'BeforeAfter Body'}]})
(SITE/'data/cases.json').write_text(json.dumps(records))
(SITE/'layouts/home.json').write_text('''{{ $results := slice }}{{ range hugo.Data.cases }}{{ $got := partial "discovery/text.html" .html }}{{ if ne ($got | jsonify) (.want | jsonify) }}{{ errorf "discovery token %s: got %s want %s" .name ($got | jsonify) (.want | jsonify) }}{{ end }}{{ $results = $results | append .name }}{{ end }}{{ $results | jsonify }}''')
p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(RUN/'public'),'--cacheDir',str(RUN/'cache'),'--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60);(RUN/'build.log').write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
print('PASS',len(records),'exact discovery token/ancestry/heading/code/caption cases')
