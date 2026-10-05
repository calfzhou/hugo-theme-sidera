"""Default-on local page motion, opt-out, locale and invalid-input contracts."""
from pathlib import Path
import json,os,re,subprocess,sys
T=Path(__file__).resolve().parents[1];R=Path(sys.argv[1]).resolve();R.mkdir(parents=True,exist_ok=False)
S=R/'site';(S/'content/notes').mkdir(parents=True)
base=f'''baseURL='https://example.invalid/'
theme={json.dumps(T.name)}
themesDir={json.dumps(str(T.parent))}
disableKinds=['RSS']
[taxonomies]
_merge='shallow'
[permalinks.term]
_merge='shallow'
'''
(S/'hugo.toml').write_text(base)
(S/'content/notes/_index.md').write_text('---\ntitle: Notes\npreset: notes\n---\n')
article='---\ntitle: A\n---\n## Target\n\nReadable text.\n'
(S/'content/notes/a.md').write_text(article)
checks=[]
for label,extra,page,ok,on in [
 ('default','',article,True,True),('off','[params]\npage_reveal=false\n',article,True,False),
 ('on','[params]\npage_reveal=true\n',article,True,True),
 ('zh',"defaultContentLanguage='zh'\nlocale='zh-CN'\n",article,True,True),
 ('bilingual','[languages.en]\nweight=1\n[languages.zh]\nweight=2\n[languages.zh.params]\npage_reveal=false\n',article,True,True),
 ('invalid-site','[params]\npage_reveal="false"\n',article,False,False),
 ('invalid-page','',article.replace('title: A','title: A\nparams:\n  page_reveal: false'),False,False),
 ('invalid-top-level','',article.replace('title: A','title: A\npage_reveal: false'),False,False),
 ('invalid-cascade','',article.replace('title: A','title: A\ncascade:\n  params:\n    page_reveal: false'),False,False),
 ('invalid-draft','',article.replace('title: A','title: A\ndraft: true\nparams:\n  page_reveal: false'),False,False),
]:
 (S/'extra.toml').write_text(extra);(S/'content/notes/a.md').write_text(page)
 out=R/(label+'-public')
 p=subprocess.run(['hugo','--source',str(S),'--config','hugo.toml,extra.toml','--destination',str(out),'--cacheDir',str(R/'cache'),'--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=45,env={**os.environ,'GOMAXPROCS':'2'})
 (R/(label+'.log')).write_text(p.stdout+p.stderr)
 if not ok:assert p.returncode and 'page_reveal' in p.stdout+p.stderr,(label,p.stdout,p.stderr)
 else:
  assert not p.returncode,(label,p.stdout,p.stderr)
  files=list(out.rglob('*.html'));assert files
  for file in files:
   text=file.read_text()
   if 'class="site-shell' not in text:continue # Native redirect pages do not render the shell.
   wanted=on and not (label=='bilingual' and file.relative_to(out).parts[0]=='zh')
   assert ('data-sidera-page-reveal' in text)==wanted,(label,file)
   if wanted:
    src=re.search(r'data-sidera-page-reveal src="([^"]+)"',text)[1]
    assert (out/src.lstrip('/')).is_file()
    assert 'integrity="sha256-' in text
   assert not re.search(r'opacity:\s*0',re.sub(r'<script.*?</script>','',text,flags=re.S)),file
  assert bool(list((out/'js').glob('page-reveal.*')))==on
 checks.append({'name':label,'expected':'build' if ok else 'rejection','pass':True})
(R/'results.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS',len(checks),'page-reveal config/native checks')
