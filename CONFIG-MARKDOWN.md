# Configured Markdown interpolation

Hugo **0.166.0**. A small build-time mechanism, **not a complete token catalog**.
No JavaScript, network lookup, Git checkout, release metadata or extra dependency.
Ordinary authored Markdown is still rendered by the current Page's `RenderString`
with display=block, existing safe Goldmark settings, source/resource hooks and
conditional math assets. This does not grant a content license.

## Participating fields

Resolution is unchanged: effective Page.Params/native cascade → the three preset
targets → current-language site/minimal defaults; component/widget options overlay
that resolved context locally. False/empty/replacement semantics remain unchanged.

| Surface | Configured Markdown input |
|---|---|
| Text components in top/left/right/left_footer | `params.text`, or `config.text` |
| Profile components in those regions | `params.profile.text`, or `config.text` |
| Article-footer text | `params.article_text`, or text `config.text` |
| Site-footer text | `params.footer_text`, or text `config.text` |
| Article license | String `params.license`, or license string `config.text` |
| Manual reference entries | Each `params.references` string, or references `config.entries` string |
| Final canonical article slot | `params.article_end_text` |

Named widgets participate through these same fields, including per-use overrides.
Titles, menus, labels, image paths, bylines and all other string settings **do not**
interpolate. Neither do article/section bodies, native shortcodes (including their
labels), ordinary math/code, summaries, translation catalogs, `license=true`'s native
neutral translation, or the theme's translated credit. The helper is not applied to
`Content` or search/graph input. Footer source links still use their actual Page's
source directory; one relative path is not automatically portable to every page.

## Small initial vocabulary and syntax

- `{site.title}` — current-language native Site.Title.
- `{page.title}` — the Page actually displaying this component, including native
  list/term Pages; **not** a guessed author or collection title.
- `{url:name}` — the same named value explicitly used as a **whole Markdown link
  destination**, e.g. `[Overview]({url:showcase.home})`. It is a rendering convention,
  not a second value catalog. Do not splice it into a URL or use it as prose/code.

Names are case-sensitive, lowercase dotted identifiers (letters, digits, underscore;
each segment starts with a letter). A dot is mandatory. There is **no property
traversal**: a name indexes only the explicit string map. `theme.version`,
`theme.tree`, `author.name` and `author.url` are intentionally unprovided. Multiple
native authors are not silently collapsed to the first one. Add real values when
needed; do not manufacture versions, release links, authors or permissions.

```toml
[params]
footer_text = '**{site.title}** — notes worth returning to.'
article_text = 'You have been reading **{page.title}**.'
```

### Predictable behavior

- Every repeated token expands. The pass is nonrecursive: a value containing another
  token remains literal. No replacement-order collisions or regex replacement syntax.
- Unknown or empty **text** values stay visibly `{name}`; no guessed fallback, warning
  flood or dropped author/credit. Unknown/empty **URL** values fail the build with a
  token diagnostic rather than emit a silently broken link. Unrecognized brace syntax
  is untouched. An intentionally empty field still clears the field itself.
- For an intentional literal write `\{page.title}` (TOML literal strings keep the
  backslash) or `&#123;page.title&#125;`. Normal Markdown removes the escape and displays
  the braces. Escaped backslashes follow ordinary Markdown pairing.
- No-token input is passed byte-for-byte to RenderString, not trimmed/reformatted.
- Conventional fenced/indented code lines, backtick spans and native `$`/`$$` TeX spans
  in configured text are opaque. This is a conservative lexical guard, **not a second
  Markdown parser**: unmatched backticks/dollars protect the remainder. Use explicit
  brace escapes in complex nested code examples or custom math delimiters. Ordinary
  body/code/shortcode/math rendering never enters this mechanism at all.
- Values are **plain strings, not Markdown/HTML**. Text punctuation and whitespace
  become character references before Markdown parsing. `](...)`, `<img>`, `&copy;`,
  emphasis, backticks, dollar signs and newlines in a value cannot create markup.
  Unicode remains text. Authored surrounding emphasis/links/paragraphs remain active.
- URL mode validates a nonempty local, HTTP(S) or mailto destination using the existing
  URL boundary; protocol-relative, unsafe schemes, whitespace/control characters,
  backslashes, quotes, angle brackets and braces reject. Markdown delimiter punctuation
  is percent-encoded. Existing native link hooks resolve `.md`/resources and escape the
  final HTML attribute. Use a real URL value, **not pre-escaped HTML or Markdown**.
  URLs are not fetched. This does not permit raw HTML or expression execution.

## One native extension route

Create **one site partial** at `layouts/_partials/config-markdown/values.html`:

```go-html-template
{{- return (dict "showcase.home" .Page.Site.Home.Permalink) -}}
```

Then use `[Back to overview]({url:showcase.home})` in any participating field.
This is the committed Fieldbook example; its native absolute home URL follows language
and baseURL/preview settings. This remains the deployment-aware home value. Ordinary `[Home](/)` now safely
retains its authored host-root URL; directory URLs no longer reach file-resource
publication. Interpolated URL values use the same corrected resolver, not a special
placeholder workaround. A literal `/` does not acquire language/baseURL prefixes.
No component copies, theme fork, provider registration,
plugin or configuration namespace is required. Use your own token namespace.

The partial returns a flat map of explicitly selected **string** values. Empty strings
are allowed; non-string values, invalid names and replacement of the two built-ins
fail. Convert intentionally chosen numeric data to a string in trusted native code.
A site partial may select a field from native data, or calculate a value from Page,
Owner or resolved Settings. Never return all Site.Params, private files or credentials.

Context: `Page`, `Owner`, `Settings`; component calls also retain `Region`, `Config`,
`Widget`, `Instance` and their normal native instance metadata. `Text` is the input.
`article_end_text` has the canonical slot context, not a fabricated widget instance.
Do not mutate settings/Pages, render Content, recurse into this helper, or collect
body graph edges from the extension. Templates are trusted native code; values and
configuration-authored strings are never evaluated as templates.

Internally `config-markdown/render.html` calls `interpolate.html` and native
RenderString. Neither partial is cached across pages/instances. Advanced native
components can call the renderer with their existing context plus `Text` (and optional
`Display="inline"`); existing theme consumers keep block mode. A site that overrides
an entire built-in component must explicitly keep this call if it wants interpolation.
This extension seam is the mechanism; further token semantics remain demand-driven.
