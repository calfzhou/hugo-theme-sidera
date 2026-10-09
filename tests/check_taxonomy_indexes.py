"""Complete global/scoped tag AND category vocabularies; term/article pagers remain."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def page(path,title,fm=''):write('content/'+path,'---\ntitle: '+title+'\n'+fm+'---\nBody.\n')
write('hugo.toml',f'''baseURL='https://example.invalid/'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
''')
# The shared inventory must agree with direct ownership, including nested roots
# and generated views, in each language/publication variant below.
write('layouts/_partials/sidera/head-extra.html','{{- partialCached "check-owners.html" site site.Language.Lang -}}')
write('layouts/_partials/check-owners.html','''{{- $owners := partialCached "collection-owners.html" . .Language.Lang -}}
{{- range .Pages -}}{{- if in (slice "page" "section") .Kind -}}
  {{- if ne (index $owners .Path) (partial "collection-owner.html" .) -}}{{- errorf "ownership inventory mismatch: %s" .Path -}}{{- end -}}
{{- end -}}{{- end -}}''')
for owner in ['notebook','journal']:
 for i in range(5):
  tag='science/math' if i%2 else 'science/physics';category='work/notes' if i%2 else 'work/tools'
  page(f'{owner}/p{i}.md',f'Article {i}',f'tags: [shared, tag-{i}, {tag}]\ncategories: [common, category-{i}, {category}]\n')
page('notebook/annex/_index.md','Independent','params:\n  scope_root: true\n')
page('notebook/annex/leaf.md','Independent page','tags: [only-annex]\ncategories: [only-annex]\n')
page('notebook/private.md','Private','draft: true\ntags: [private-tag]\ncategories: [private-category]\n')
page('empty/_index.md','Empty')
for taxonomy in ['tags','categories']:page(f'{taxonomy}/authored-empty/_index.md','Empty & visible','slug: authored-empty\n')
for i in range(5):page(f'legacy/p{i}.md',f'Legacy {i}','tags: [shared]\ncategories: [common]\n')
class Index(HTMLParser):
 def __init__(self,text):super().__init__();self.entries=[];self.count=None;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='li' and a.get('class')=='taxonomy-node':self.count=int(a['data-term-count'])
  if tag=='a' and a.get('class')=='taxonomy-entry':self.entries.append((a['href'],self.count))
passed=[]
for label,nested,prefix,size,extra,flags in [('hierarchy',True,'',2,'',[]),('flat',False,'',2,'',[]),('chinese-subpath',True,'/preview',2,"defaultContentLanguage='zh'\nlocale='zh-CN'\n",[]),('large-size',True,'',50,'',[]),('icons-off',True,'',2,'',[]),('all-states',True,'',2,'',['--buildDrafts'])]:
 hierarchy='["tags","categories"]' if nested else '[]'
 write('probe.toml',extra+f"baseURL='https://example.invalid{prefix}/'\n[params]\ntaxonomy_page_size={size}\ntaxonomy_hierarchy={hierarchy}\n"+('icons=false\n' if label=='icons-off' else ''))
 for owner,preset in [('notebook','notes'),('journal','blog')]:page(owner+'/_index.md',owner,f'preset: {preset}\nparams:\n  page_size: {size}\n  taxonomy_page_size: {size}\n  taxonomy_hierarchy: {hierarchy}\n')
 page('legacy/_index.md','Explicit list hub',f'params:\n  taxonomy_hubs: list\n  page_size: {size}\n')
 out=RUN/(label+'-public');p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning',*flags],capture_output=True,text=True,timeout=60);(RUN/(label+'.log')).write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
 for taxonomy,shared,parent,children,unique in [('tags','shared','science',['math','physics'],'tag'),('categories','common','work',['notes','tools'],'category')]:
  for owner in ['', 'notebook','journal']:
   route='/'.join(x for x in [owner,taxonomy] if x);raw=(out/route/'index.html').read_text();rows=Index(raw).entries
   counts={href.removeprefix(prefix+'/'+route+'/').strip('/'):count for href,count in rows}
   multiplier=1 if owner else 2
   expected={shared:5 if owner else 15,**{f'{unique}-{i}':multiplier for i in range(5)},parent+'/'+children[0]:2*multiplier,parent+'/'+children[1]:3*multiplier}
   if nested:expected[parent]=5*multiplier
   if not owner:expected.update({'only-annex':1,'authored-empty':0})
   if flags and owner in ('','notebook'):expected['private-'+('tag' if taxonomy=='tags' else 'category')]=1
   assert counts==expected,(label,route,counts,expected)
   assert len(rows)==len(counts) and 'data-page-link' not in raw and not (out/route/'page').exists()
   assert 'Empty &amp; visible' in raw if not owner else 'authored-empty' not in raw
   # Individual term results still paginate (global policy versus owner policy).
   assert (out/route/shared/'page/2/index.html').exists()==((5 if owner else 15)>size)
  empty=(out/'empty'/taxonomy/'index.html').read_text();assert not Index(empty).entries and 'data-page-link' not in empty
  # Explicit all-content hub mode stays a paginated article list, not a vocabulary.
  legacy=(out/'legacy'/taxonomy/'index.html').read_text();assert 'id="articles"' in legacy
  assert (out/'legacy'/taxonomy/'page/2/index.html').exists()==(5>size)
 for owner in ['notebook','journal']:assert (out/owner/'page/2/index.html').exists()==((6 if flags and owner=='notebook' else 5)>size)
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'global_and_scoped_tags_and_categories':True,'term_article_and_explicit_list_pagination_retained':True},indent=2)+'\n');print('PASS 6 variants: complete tags/categories, hierarchy/flat, membership/counts, empty terms, scopes, locales and retained article pagination')
