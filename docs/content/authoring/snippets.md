---
title: "Include code resources"
params:
  ai_label: generated
---

Put a text/code file beside your bundle's `index.md` or `_index.md` and use:

```text
{{</* snippet src="example.py" from=2 to=5 options="linenos=table,hl_lines=2" */>}}
```

The rendered selection has native highlighting, copy controls and a full-source
download. It does not execute code or discover/import its dependencies. The
[shortcode reference](../publishing/shortcodes.md#code-resources) owns all options.

## Keep the resource boundary clear

Default scope is exact current-page `.Resources.Get`, not a filesystem search,
static directory or cross-bundle source link. Explicit `scope="shared"` reads only
`assets/snippets/`; a site can deliberately mount public files into that namespace.
Do not mount a home folder, secrets or an entire repository for convenience.
Resource keys use forward slashes: no absolute/dot/parent paths, URL encoding,
query/fragment, globs or network addresses. Literal spaces/Unicode are fine.

Native Hugo excludes symlink resources on the verified runtime. Markdown/HTML under
content may be Pages rather than raw source: use shared resources with the original
extension, or a bundle `.txt` with explicit `lang`, rather than relaxing HTML security.
Missing/non-text resources fail. Neither trusted mounts nor templates are an OS sandbox.

## Selection is not redaction

`from`/`to` are one-based inclusive lines, defaulting to first/last. Bounds must be
positive, ordered and within the file. Empty files permit no explicit bounds.
Indentation, spaces, Unicode, BOM and source line endings are preserved; invalid
UTF-8, NUL, binary controls and bare CR fail. A final newline does not invent a line.

Highlighting/HTML normalize CRLF to LF. The Clipboard API payload retains the exact
selected text; a manual textarea fallback may normalize line endings. The **download
always publishes full original bytes**, not just selected lines. Bundle resources
may publish independently. Never use line selection, hidden controls or drafts as
secret redaction; do not include private source in a publishable bundle.

Title defaults to basename, language to extension (unknown lexer falls back to text).
Highlight line positions are relative to the displayed selection; linenostart
normally starts at its first source line. Auto-generated line anchors distinguish
calls; explicit anchor prefixes must be unique. The shared toolbar is also used for
ordinary fences. See the [live example](example/_index.md#local-code).
