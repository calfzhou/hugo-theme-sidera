"""Native 404: localization, shell, local SVG, overrides, exclusion and provider safety."""
from pathlib import Path
import json,re,subprocess,sys
THEME=Path(__file__).resolve().parents[1];RUN=Path(sys.argv[1]).resolve();assert not RUN.exists();SITE=RUN/'site';SITE.mkdir(parents=True)
def write(name,text):
 p=SITE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
write('hugo.toml',f'''baseURL='https://example.invalid/'
title='Fixture site'
theme='{THEME.name}'
themesDir={json.dumps(str(THEME.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
[menus]
[[menus.primary]]
name='Home'
pageRef='/'
''')
write('content/_index.md','---\ntitle: Home\n---\nPublic home.\n')
write('content/notes/_index.md','---\ntitle: Notes\npreset: notes\n---\nNotes.\n')
write('content/notes/entry.md','---\ntitle: Public article\ndate: 2024-01-01\n---\nSearchableword.\n')
write('content/private.md','---\ntitle: Private\ndraft: true\n---\nPrivateword.\n')
passed=[]
variants=[('english','','/',True,'Page not found','Back to Home'),('chinese',"defaultContentLanguage='zh'\nlocale='zh-CN'\n",'/',True,'页面不存在','返回主页'),('subpath',"baseURL='https://example.invalid/preview/'\n",'/preview/',True,'Page not found','Back to Home'),('icons-off','[params]\nicons=false\n','/',False,'Page not found','Back to Home'),('bilingual',"baseURL='https://example.invalid/preview/'\n[languages.en]\nweight=1\nlocale='en-US'\n[languages.zh]\nweight=2\nlocale='zh-CN'\n",'/preview/',True,'Page not found','Back to Home'),('comments-enabled',"[params]\ncomments=true\n[params.giscus]\nrepo='fixture/comments'\nrepo_id='R_mock'\ncategory='Announcements'\ncategory_id='DIC_mock'\n",'/',True,'Page not found','Back to Home')]
for name,config,home,icons,title,action in variants:
 write('probe.toml',config);out=RUN/(name+'-public')
 p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(out),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60);(RUN/(name+'.log')).write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
 raw=(out/'404.html').read_text();assert f'<title>404 · {title} | Fixture site</title>' in raw
 assert '<meta name="robots" content="noindex">' in raw
 assert f'class="not-found-home" href="{home}">{action}</a>' in raw
 assert 'class="not-found-code">404</span>' in raw and 'id="search-input"' in raw
 assert ('class="not-found-symbol"' in raw)==icons
 if icons:assert 'M12 3C9.68925' in raw and 'focusable="false"' in raw
 assert 'id="sidera-comments"' not in raw and 'data-sidera-giscus' not in raw and 'class="article-header' not in raw
 assert 'cdn-x/placeholder' not in raw and 'src="https://' not in raw
 assert '/404.html' not in (out/'sitemap.xml').read_text()
 index_url=re.search(r'data-index="([^"]+)"',raw)[1]
 index=json.loads((out/index_url.removeprefix(home)).read_text());assert len(index['documents'])==3
 assert all('/404' not in d['url'] and 'Privateword' not in json.dumps(d) for d in index['documents'])
 if name=='comments-enabled':assert 'data-sidera-giscus' in (out/'notes/entry/index.html').read_text()
 if name=='bilingual':
  zh=(out/'zh/404.html').read_text();assert '404 · 页面不存在' in zh and 'class="not-found-home" href="/preview/zh/"' in zh
  assert '<meta name="robots" content="noindex">' in zh
 for href in re.findall(r'(?:src|href)="([^"#]+)"',raw):
  if href.startswith(home) and (href.endswith('.js') or href.endswith('.css')):assert (out/href.removeprefix(home)).exists(),href
 passed.append(name)
# Native i18n override remains supported, without another 404 metadata schema.
write('i18n/en.toml','[not_found_title]\nother="Custom missing page"\n')
write('probe.toml','');p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(RUN/'override-public'),'--cacheDir',str(RUN/'cache'),'--config','hugo.toml,probe.toml','--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60);assert not p.returncode,p.stdout+p.stderr
assert 'Custom missing page' in (RUN/'override-public/404.html').read_text();passed.append('i18n-override')
(RUN/'results.json').write_text(json.dumps({'passed':passed,'native_404':True,'excluded_from_search_and_sitemap':True,'no_comments_even_when_enabled':True},indent=2)+'\n');print('PASS 7 native 404 variants: locale, subpath, icons-off, comments exclusion and i18n override')
