# Include a local code file

Use **Hugo 0.166.0** native resources and highlighting. No code is executed and no
imports, network URLs or arbitrary filesystem paths are followed. Standard notation,
on its own line with surrounding blank lines:

```text
{{< snippet src="solution.py" >}}
{{< snippet src="solution.py" title="The lookup loop" from=4 to=8 options="linenos=table,hl_lines=2,anchorlinenos=true" >}}
{{< snippet src="utilities/labels.py" scope="shared" lang="python" >}}
```

## Resource boundary

- Default `scope="page"`: exact `.Page.Resources.Get` within the current native page
  bundle. Put source beside `index.md`/`_index.md`, or in a child resource directory.
  No source-root fallback, cross-bundle search or A article-link resolver is involved.
  Native resource names/metadata apply; avoid renaming a resource if you want its
  original filename to remain the author-facing key.
- `scope="shared"`: exact `resources.Get` under **`assets/snippets/`**. For the example
  above, use `assets/snippets/utilities/labels.py`. Explicit site-controlled native
  mounts to that namespace are possible; mount only intended public source files,
  never home, secrets or an entire repository. No new default mount is installed.
- Paths are resource keys with forward slashes, not URLs. Absolute paths, dot/dot-dot
  segments, backslashes, schemes, percent encoding, query/fragment and globs fail
  before lookup. Literal spaces and Unicode filenames work; do not URL-encode them.
- Native Hugo excludes file/directory symlinks from these resource namespaces on the
  tested version; both scopes reject them as missing. This is not an OS sandbox for
  untrusted site configuration/templates: maintain trusted mounts and build inputs.
- Missing resources, content Pages, invalid text or bounds fail with the shortcode's
  source position. Only text/code resource data is read. `static/` and arbitrary
  root files are not inclusion inputs. There is no implicit “publish everything”.
  Hugo treats `.md`/`.html` under content as Pages (HTML content is also blocked by
  the existing site security policy), not raw downloadable source. To display those
  formats, use an explicitly shared `assets/snippets/` resource with its original
  extension, or a bundle `.txt` copy with `lang="html"`/`lang="markdown"`. Do not relax
  content security to make a file readable; shared HTML source is tested as data.
- The link uses the resource's native `.RelPermalink`, preserving dated page routes,
  language/baseURL prefixes and opted-in mounted docs. It always publishes/downloads
  the **full original bytes**, not the selection. Used shared resources publish on
  demand. Bundle files may be published by Hugo independently of this shortcode;
  line selection, draft status or hiding a link is **not redaction/privacy**.
- Import dependencies in included code are not discovered, executed or packaged.
  Downloading one Python file does not promise a runnable multi-file program.

Real-site audit: all 791 active calls in the comparable 352-file inventory use
adjacent Python basenames. Coding `_utils` imports are shared execution dependencies,
not active shared snippet calls. For a future explicitly shared inclusion, deliberately
place/mount the approved public utility in `assets/snippets/` and use `scope="shared"`;
do not widen lookup to the whole source tree.

## Exact text and line semantics

| Input/option | Result |
|---|---|
| Omit both `from`/`to` | Entire source, with no trimming or dropped last line. |
| `from=N`, `to=M` | One-based **inclusive** line bounds; either may be omitted (1 / last line). Each selected line retains its original terminator if present. |
| Final LF/CRLF | Ends that line; does not invent an extra empty line. Consecutive terminators represent real empty lines. |
| No final newline | Final line remains unterminated, including when selected alone. |
| Empty file | Empty code block and valid empty download; any explicit bound is invalid. |
| Invalid bounds | Zero, negative, noninteger, reversed or beyond EOF fail; no clamping. Bounds are positive decimal integers up to 9 digits. |
| UTF-8/whitespace | Indentation, tabs, leading/trailing spaces, blank lines, Unicode and UTF-8 BOM retained. Invalid UTF-8, NUL/binary controls and bare CR fail. LF, CRLF and mixed LF/CRLF are supported. Printable text, not arbitrary binary formats. |
| Browser/highlighter | Native Chroma and HTML present CRLF as LF. All other tested text is unchanged. Copy uses separately JSON-escaped selected source, retaining CRLF and exact whitespace; it never copies line numbers/title/toolbar. |
| Clipboard denied/missing | H's selected manual-copy textarea and failure toast. Browser textarea values normalize CRLF to LF; use the full download when exact file bytes matter. No false success. |
| No JavaScript | Highlighted/selectable code, title/language and full download remain; Copy stays hidden. Browser/OS manual selection is not a byte-preservation API. |

HTML, backticks/fence-looking text and shortcode-looking characters in files are
escaped highlighted **data**, never passed through Markdown or shortcode expansion.
The original byte-for-byte download is the authority for line-ending/encoding fidelity.
The JSON source attribute costs one additional escaped copy of the displayed selection;
no full hidden file is embedded for a partial selection.

## Title, language and native highlight options

`title` defaults to the source basename. A supplied title must be nonblank; it is plain
escaped text, not Markdown/HTML. The separate localized Download full source link uses
native browser `download` behavior (the browser/server may determine the saved filename).

`lang` defaults to the filename extension (lowercase), or localized Text without one.
An explicit language wins, including `lang="text"` or `lang=""` for plain text.
Identifiers accept letters/digits/underscore/plus/hyphen. Unknown identifiers retain
their visible label but fall back to the plain-text lexer; no heuristic guessing.
This applies to extension defaults as well. Invalid identifiers fail, rather than
entering HTML attributes unchecked.

`options` is a comma-separated native highlight option string with a bounded
presentation subset (case-insensitive keys):

- `linenos=true|false|inline|table`, `linenumbersintable=true|false`.
- `linenostart=N`: positive decimal; defaults to the first selected **source** line.
- `hl_lines=2-4 7`: native positions relative to the **displayed selection**, independent
  of linenostart. Native handling applies to highlight positions outside the selection.
- `anchorlinenos=true|false`, `lineanchors=unique-prefix`: safe ASCII ID prefix; when
  omitted, the shortcode's page ordinal generates distinct prefixes. Provide unique
  explicit prefixes if overriding; no promise of stable line IDs after reordering calls.

Other native site highlighting defaults remain in effect. Inclusions deliberately force
block output, class-based theme palettes, no guessing and the normal `highlight` wrapper;
`code`, `type`, raw wrapper/style or inline options cannot replace the included data/UI.
Unsupported/malformed options fail. Ordinary fenced code retains all its native options
and project render-hook precedence, including inline output; its behavior is unchanged.
For site-wide inline line numbers on Hugo 0.166 use `lineNos=true` plus
`lineNumbersInTable=false`; `lineNos="inline"` at the configuration level fails in the
native runtime (shortcode options accept it).

## Composition and customization

Use self-contained **standard `{{< ... >}}` notation**, with ordinary surrounding
Markdown, alerts, figures, source links and math. Markdown `%` notation sends generated
HTML into the safe Markdown pass and is unsupported; strict builds reject the omitted
raw HTML. Do not enable unsafe HTML to force it through.

C2 supports snippets inside block/folding/box/cell containers: outer container `%`,
nested snippet `<`. The original source/resource/selection/highlighting runs unchanged;
only its trusted generated output crosses a page-local native-node bridge. No source
is run through Markdown. Native ancestor ordinals give unique nested line-anchor
prefixes; standalone default prefixes remain unchanged. [COMPONENTS.md](COMPONENTS.md)
defines the complete contract. No filename heading is synthesized.

Native site `layouts/_shortcodes/snippet.html` overrides the theme shortcode. For nested use, preserve its small leaf-bridge wrapper
as documented in COMPONENTS.md; overriding the renderer partial is another focused option. Both H
fences and inclusions reuse `layouts/_partials/code-block.html` for the same toolbar,
copy/toast/manual fallback and scroll presentation. A custom fenced-code hook is still
independent of the inclusion highlighter; a site partial override can affect both UIs.
No new registry, dependency, parser import or unsafe setting is required. Bundled docs
remain default-off. C2 changes the block template format: restart an already-running preview once.
No cache deletion or user-server operation is performed by the theme.

## Hexo conversion

```text
{% snippet solution.py %}
→ {{< snippet src="solution.py" >}}

{% snippet solution.py "Lookup loop" lang:python from:4 to:8 %}
→ {{< snippet src="solution.py" title="Lookup loop" lang="python" from=4 to=8 >}}
```

Keep the file in the page bundle. Review any explicit old bounds: the old plugin used
an end index/default `-1` and trimmed text; do **not** reproduce that trailing-content
loss. No active from/to use was found in the bounded source audit. Full real-site
conversion is P4, not performed by this feature.
