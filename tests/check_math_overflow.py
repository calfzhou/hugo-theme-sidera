"""Native fixture for math overflow browser regression; no remote resources.
Run with a fresh absolute output directory, then inspect with the local E2E harness.
"""
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
[markup.goldmark.extensions.passthrough]
_merge='deep'
''')
write('content/check/index.md',r'''---
title: Math overflow
---
## Tall brace

$$
\begin{cases}
  0 & \text{for }a\notin s[i:j+1] \\
  1 & \text{for }\exists!a\in s[i:j+1] \\
  f(first+1,last-1)+2
\end{cases}
$$

## Nested cases

$$
f(d)=\begin{cases}
 f(d-1) & \text{otherwise} \\
 \min\begin{cases}
  f(d-1)+c_1 \\
  f(d-7)+c_2 \\
  f(d-30)+c_3
 \end{cases}
\end{cases}
$$

## Fraction and superscripts

$$
\left\{\frac{\displaystyle\sum_{i=0}^{n} x_i^2}{\sqrt{1+\frac{a}{b}}}\right\}^{m+1}
$$

## Matrix

$$
\begin{pmatrix}
a & b & c \\
d & e & f \\
g & h & i \\
j & k & l
\end{pmatrix}
$$

## Wide formula

$$
f(x)=x_1+x_2+x_3+x_4+x_5+x_6+x_7+x_8+x_9+x_{10}+x_{11}+x_{12}+x_{13}+x_{14}+x_{15}
$$

## Ordinary formula

$$
x^2+y^2=z^2
$$
''')
p=subprocess.run(['hugo','--source',str(SITE),'--destination',str(RUN/'baseline-public'),'--cacheDir',str(RUN/'cache'),'--noBuildLock','--panicOnWarning'],capture_output=True,text=True,timeout=60);(RUN/'build.log').write_text(p.stdout+p.stderr);assert not p.returncode,p.stdout+p.stderr
html=(RUN/'baseline-public/check/index.html').read_text();assert html.count('class="math-display"')==6 and html.count('<math ')==6
assert html.count('tabindex="0" role="group"')>=6
print('PASS 6 native math fixtures; browser overflow/keyboard checks still required')
