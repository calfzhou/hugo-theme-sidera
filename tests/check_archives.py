"""Archives are complete year groups, independent of collection/taxonomy pagination."""
from pathlib import Path
import json,re,subprocess,sys
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
[frontmatter]
date=['date']
publishDate=['publishDate','date']
lastmod=['lastmod','date']
''')
def page(path,title,fm=''):write('content/'+path,'---\ntitle: '+title+'\n'+fm+'---\nBody.\n')
for owner,preset in [('journal','blog'),('notes','notes')]:
 for slug,title,fm in [
 ('latest','Newest','date: 2020-01-01\npublishDate: 2025-03-01\n'),
 ('alpha','Alpha','date: 2024-06-01\n'),('beta','Beta','date: 2024-06-01\nlastmod: 2026-01-01\n'),
 ('pin','Pinned','date: 2023-01-01\nparams:\n  pinned: true\n'),
 ('ancient','Ancient','date: 0001-02-01\n'),('undated','Unknown',''),
 ('draft','Draft','date: 2022-01-01\ndraft: true\n'),
 ('future','Future','date: 2999-01-01\n'),
 ('expired','Expired','date: 2000-01-01\nexpiryDate: 2001-01-01\n'),
 ('unlisted','Unlisted','date: 2026-01-01\nbuild:\n  list: never\n')]:page(f'{owner}/{slug}.md',title,'tags: [one,two,three]\n'+fm)
 page(f'{owner}/headless/index.md','Headless','headless: true\ndate: 2026-01-01\n')
 page(f'{owner}/annex/_index.md','Independent','params:\n  scope_root: true\n')
 page(f'{owner}/annex/other.md','Separate','date: 2026-01-01\n')
page('empty/_index.md','Empty','preset: blog\n')
passed=[]
for label,overlay,prefix,size,flags in [
 ('normal','','',2,[]),
 ('chinese-subpath',"defaultContentLanguage='zh'\nlocale='zh-CN'\nbaseURL='https://example.invalid/preview/'\n",'/preview',2,[]),
 ('size-one','','',1,[]),('size-large','','',20,[]),
 ('all-states','','',2,['--buildDrafts','--buildFuture','--buildExpired'])]:
 for owner,preset in [('journal','blog'),('notes','notes')]:page(owner+'/_index.md',owner,'preset: '+preset+f'\nparams:\n  page_size: {size}\n  taxonomy_page_size: 2\n  list_order: modification\n')
 write('probe.toml',overlay);out=RUN/(label+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning',*flags],capture_output=True,text=True,timeout=60);(RUN/(label+'.log')).write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
 for owner in ['journal','notes']:
  archive=(out/owner/'archives/index.html').read_text();hrefs=re.findall(r'data-archive-article href="([^"]+)"',archive)
  slugs=['latest','alpha','beta','pin','ancient','undated'];years=['2025','2024','2023','0001']
  if flags:slugs=['future','latest','alpha','beta','pin','draft','expired','ancient','undated'];years=['2999','2025','2024','2023','2022','2000','0001']
  assert hrefs==[prefix+'/'+owner+'/'+s+'/' for s in slugs],(label,owner,hrefs)
  groups=re.findall(r'class="archive-year">\s*<h2>(.*?)</h2>',archive)
  assert groups==years+(['日期不详'] if label=='chinese-subpath' else ['Undated']),(label,groups)
  assert f'data-archive-total="{len(slugs)}"' in archive
  assert 'data-page-link' not in archive and 'class="pagination' not in archive
  assert not (out/owner/'archives/page').exists()
  # Native browsing remains paginated independently; a large size naturally fits.
  assert (out/owner/'page/2/index.html').exists()==(len(slugs)>size)
  assert (out/owner/'tags/page/2/index.html').exists()
  assert f'data-page-size="{size}"' in (out/owner/'index.html').read_text()
  separate=(out/owner/'annex/archives/index.html').read_text()
  assert re.findall(r'data-archive-article href="([^"]+)"',separate)==[prefix+'/'+owner+'/annex/other/']
 empty=(out/'empty/archives/index.html').read_text();assert 'data-archive-total="0"' in empty and 'data-archive-article' not in empty
 assert ('此结果中暂无文章。' if label=='chinese-subpath' else 'No articles in this result.') in empty
 passed.append(label)
(RUN/'results.json').write_text(json.dumps({'passed':passed,'archive_complete':True,'regular_and_taxonomy_pagination_retained':True},indent=2)+'\n');print('PASS 5 archive variants: complete year groups, ordering, native exclusions, independent roots, locales, page sizes and other pagers')
