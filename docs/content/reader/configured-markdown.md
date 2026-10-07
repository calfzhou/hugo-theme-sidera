---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-07T22:24:52+08:00
title: "Configured Markdown"
params:
  ai_label: generated
---

Sidebar text/profile text, article/site footer text, string content licenses,
authored reference entries and final `article_end_text` share a small build-time
interpolation mechanism. Native field resolution happens first; per-instance widget
options remain local. Ordinary article/section bodies, shortcode labels, menu labels,
image paths, titles, bylines and translations do **not** interpolate.

```toml
[params]
footer_text = '**{site.title}** — notes worth returning to.'
article_text = 'You have been reading **{page.title}**.'
```

Built-in values:

- `{site.title}`: current-language native Site.Title, escaped as plain text.
- `{page.title}`: the Page displaying the component, escaped as plain text.
- `{page.authors}`: that Page's native author terms, rendered as linked names in
  native order (duplicates removed). Titles come from author profiles; destinations
  use the same global/scoped link policy as the existing author components.

For example, `license = 'Written by {page.authors}. Licensed under …'` includes
linked credit without hard-coding an author. Use this token directly in prose,
not inside another link, a URL destination or Markdown emphasis delimiters.
An explicit `authors: []` produces empty text; provide a suitable license notice
on pages with no author rather than leaving an incomplete attribution sentence.
`show_authors: false` hides the optional author UI, not this explicitly requested
license credit. Author attribution and AI-generation labels are separate choices.

There is no automatic theme version or release link. Unknown/empty ordinary text
values stay visibly literal. Names are case-sensitive lowercase dotted identifiers,
not property traversal. The pass is nonrecursive. Author names and ordinary values
are escaped data; only `{page.authors}` constructs Markdown links from native terms,
never from author-supplied HTML. Code, TeX and escaped tokens remain literal.

## Add one real value through native lookup

Create site `layouts/_partials/config-markdown/values.html`:

```go-html-template
{{- return (dict "site.home" .Page.Site.Home.Permalink) -}}
```

Then use `[Home]({url:site.home})` in a participating setting. `url:` selects the
same value as a **whole Markdown link destination**, with URL validation and delimiter
escaping. Do not splice it into a path or prose. Missing/empty/unsafe URL tokens
fail rather than emitting a broken link. Native Home.Permalink follows language and
deployment prefix; literal `[Home](/)` still means host root.

The extension returns a flat string map; it cannot replace built-ins. Context has
Page, Owner, Settings and normal component context. Select intended public values
only; never return all Site.Params, private files or credentials. Do not render
Content, mutate context or recurse into the helper. Templates are trusted code;
configuration strings are not evaluated as templates.

## Literal braces and rendering

Use `\{page.title}` or `&#123;page.title&#125;` for a literal. Conventional fenced/
indented code, backtick spans and native dollar TeX spans in configured text stay
opaque. For complex nested examples use explicit escapes; this is a conservative
lexical guard, not a second Markdown parser. No-token text goes unchanged into
native RenderString. Authored Markdown remains active under the same safe HTML
policy and resource hooks. Relative source links use the actual displaying Page's
source directory, so one relative footer link is not portable to every page.
