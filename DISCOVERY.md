# Content references and local search

Hugo 0.166.0 · no production Node dependency, remote backend or account.

## Try the complete journey

In the showcase, open **Notes → A reading list with room to breathe**. The search
box follows the identity and precedes the configured navigation, as in Stellar.
It initially searches the nearest browsing collection. Type **marginalia**, check
**Search all content**, and follow the Journal result: its native dated URL opens with the
intro keyword highlighted. **Give a link a reason** opens that actual heading;
**连接笔记** opens its bilingual section and reveals the containing fold. Searching
Notes for **matching_pair** also finds actual included source code.

With a nonempty query, results occupy the sidebar's widget area; clear or Escape
restores the original navigation. Page titles sit above result links, with section,
scope and matching excerpt inside. Input/result/body highlighting use the same
literal matching model. No generic modal or replacement of configured menus.

The native **Search all content** checkbox appears only for a nonempty query on an
owned page. Unchecked means the current collection; checked means all eligible content
in the current language. Toggling updates results and the input's scope label immediately,
without clearing the query or moving focus. Clearing/Escape/whitespace-only input hides
and unchecks it, restoring the contextual default; no preference is stored. Global-only
pages have no redundant checkbox, and no-JS leaves it hidden/disabled.

Search and results use the full inner sidebar width, without an extra nested gutter.
The underline uses Stellar's rainbow/background-position animation on hover, focus or
an active query. It pauses when inactive; reduced-motion users get a static gradient.
The existing sidebar/reading-column dimensions remain unchanged.

## Author/site controls

These booleans use the established Page/cascade → preset → site/minimal settings
resolution, with explicit false retained and malformed values diagnosed (including
excluded local drafts):

| `params` key | Default | Meaning |
| --- | --- | --- |
| `search` | true | Show the sidebar/compact-header search and fetch the local index on this page. Does **not** exclude its body from another page's index. Site-wide false disables index generation when no page overrides it. |
| `search_index` | true | Include this published body/title in the current-language search resource. Set false to opt out; menus are irrelevant. |
| `link_graph` | true | Include this published body as both a source and target in generated relationships. False removes both directions; it does not rewrite authored links. |

```yaml
params:
  search_index: false
  link_graph: false
```

For a collection's descendants, use actual `cascade.params`; ordinary section
params do not cascade. Theme-doc content remains opt-in through the existing mount.
Scope is **collection-owner.html**, not a preset name or URL/directory prefix. Nested
independent roots are separate, even under an outer root's path. Global search means
all eligible content in the current language. Cross-language graph links remain
explicit links to the original language, not automatic translation substitution.

### Reference components

`outgoing` and `backlinks` are normal configurable **article_footer** components,
including named/repeated instances. They default after authored `references`, before
license/share. Omit them or disable the footer to hide presentation without changing
content eligibility. `config` is empty; no new graph configuration framework.

```yaml
params:
  article_footer: [terms, references, outgoing, backlinks, license, share, series]
```

The stable native override is `discovery/references.html`, receiving the same footer
instance context. Empty sets emit no section/divider. `params.references` remains a
separate authored Markdown list: it is neither augmented nor used to invent edges.

## Canonical link coverage

- Native Markdown inline/reference/autolink nodes and the container `link` card, including
  those in supported folds/boxes/grids, share the **single exact-source resolver**.
  Page/resource resolution and href diagnostics are unchanged. A root-level File.Dir
  of `/` is normalized before exact File.Path comparison; it is not an extra root.
- The resolver now returns href plus native target internally. The public
  `links/destination.html` href-only helper remains for image hooks/site overrides.
  Source Page identity comes from that same object, not a second Markdown parser.
- For ordinary published-URL links, a metadata-only registry recognizes only an
  **exact native Page.Permalink**, resolving a relative URL against the source's
  published URL. No alias guesses, `.html` stripping, logical basename fallback or
  HTTP request. Source-file links continue to use source-relative—not URL-relative—
  resolution. Changing date/slug/url policy needs no source-link rewrite.
- Hooks/cards annotate actual rendered anchors with `data-content-page`. The graph
  reads these annotations only from `.Content`, never menus, TOC, footers, search
  controls, JSON/script data or its own output. Images/resources/external URLs are
  not Pages and do not become edges. Fragment-only/self links are omitted.
- Query/hash variants and repeated mentions collapse to one directed Page pair.
  Lists sort by native URL for deterministic output. No occurrence counts or
  graph visualization. Cross-scope and explicit cross-language edges are allowed.
- Known unpublished, headless, link-only, unlisted and opt-out targets are absent
  from relationships. This does not weaken A's unresolved-source warnings or make
  an authored link to a missing destination safe.
- Raw HTML, arbitrary third-party shortcode HTML, JS-generated links and a custom
  hook that omits the annotation are **not universally covered**. Site hook authors
  can use `links/resolve.html` and `links/content-target.html`, plus the annotation,
  while retaining the container bridge branch. Raw author HTML remains disabled.

## Native lifecycle and publication privacy

The shared body partial is called **only at a Page's own actual body location**. It
sets one idempotent Page-local rendering flag; cards/summaries don't set it. After
all sites/output formats have rendered, native `templates.Defer` runs the footer
and search-resource readers. Ordinary authored footer items/hooks are prepared before
that barrier, preserving math/resource detection; only relationships and final footer
assembly are deferred, so empty graph sections leave no empty boxes. A pure cached catalog enumerates native `Site.Pages`,
selects real file-backed home/page/section bodies with that rendering proof, and
reads their completed `.Content`. No Site.Store edge accumulator, render-order
mutation, `.Content` call in a link hook, or graph-to-graph recursion. A↔B cycles,
heading checks, one/two-worker builds and repeated builds are tested.

Native Site.Pages controls publication/list membership; effective native
`Page.Params.build.render`, HTML output, current section body settings and actual
own-body rendering jointly control eligibility. Hugo server can retain a Page.Store
flag across render-policy edits, so that flag alone is deliberately insufficient. Thus `build.render=link` cannot leak an unrendered body,
`list=never/local` is not promoted into a global index, and draft/future/expired/
headless bodies remain absent in ordinary builds. A deliberately displayed section
intro can be indexed; a suppressed intro cannot. Generated term/preset/archive/list
UI and paginator copies do not become documents. There is one current-language
fingerprinted JSON resource containing only public URL/title/scope/context/normalized
sections—no source paths, raw XML, code-copy data attributes or private bridge tokens.

`--buildDrafts --buildFuture --buildExpired` deliberately changes publication and
search membership: this is a **private validation build**, never a production privacy
filter. `search_index=false` is discoverability, not access control: a rendered page
is still public. Scope filtering is client-side UX over that already-public language
index, **not publication security**. Use fresh output destinations for deployment;
a stale directory can retain formerly public pages/resources. This feature does
not retroactively erase already deployed HTML/indexes or fix all historical Hugo
adapter/new-page watcher limitations.

## Text and heading model

The generated resource contains normalized **sections**: an introduction followed
by each actual H1–H6 ID/title and its body up to the next heading. No slug regeneration.
The browser computes UTF-16 section offsets by cumulative `text.length + 1`; matches
and DOM positions use the same offsets, avoiding Go byte/JavaScript character drift.
Native HTML tokenization (not raw-Markdown regex) and browser DOM traversal share the
small data-owned tag/class exclusion rules. Tests compare every generated section
with its actual rendered DOM text/heading identity, including composed/decomposed
accents, CJK and non-BMP offset checks.

Included: ordinary text/links/tables/alerts; supported container titles/body/cards/
inline kbd/u/quot/copy values; real fences and displayed snippet selections; visible
image/video/diagram captions. Inline formatting and syntax-highlight spans do not
split words. Whitespace is collapsed consistently; entities are decoded once.

Deliberately excluded from both indexing and marking:

- KaTeX's complete math subtree (neither duplicated MathML/HTML nor unlocatable TeX).
  Describe mathematical ideas in adjacent prose for search.
- Diagram internals, Mermaid source-toggle text, raw drawio XML, renderer iframes/SVG
  images; index captions/adjacent descriptions instead. No renderer changes.
- Toolbars, buttons, code filenames/download labels, line numbers, copy payloads,
  fallback/assistive/control text, hidden attributes, scripts/styles, raw HTML payloads.
- Existing authored `mark` regions, preserving their semantics without nesting marks.
- Image alt-only text and captions suppressed by native `no-caption` ancestors.

This is full-text search of the documented **rendered-text** subset, not OCR, formula
search, arbitrary CSS visibility inference or every custom template's HTML. The native
reader expects well-formed theme-generated markup. Trusted custom body templates own
compatibility; `data-search-exclude` omits a subtree from text extraction/highlighting.
It is not a secret-redaction mechanism and does not disable a graph edge annotation.

## Matching, navigation and failure behavior

No library/dependency: at most 160 query UTF-16 code units (native input maxlength), eight whitespace-delimited unique
tokens; literal substring matching, case/diacritic-insensitive via NFD. Contiguous CJK
is a literal substring, not word segmentation. Punctuation and regex-like strings are
literal. Every token must occur in one section or its page title; a section result
needs at least one body match. Title-only fallback is explicitly labeled. Ranking is
bounded/additive (title 8, heading 5, body 1 per token), then native URL/section order;
maximum 40 results. No fuzzy matching/stemming or search-engine-scale claim.

The real site's eager/no-persistent-cache preference is retained: local prefetch on
load and revalidation on focus, `cache:no-store`, single in-flight request, 10-second
abort and retry on refocus. Native content-addressed index URLs change when data changes,
and remain consistent with the HTML build that selected them. Reload/navigation picks
up a new deployment; refocusing an already-open old-build page does not discover a new
build's URL. This avoids Hugo's observed stable-resource re-publication issue when
preview content reverts to a previously generated value. No local/
session storage or remote query service. Empty input shows the original widgets;
loading/error/no-result have localized status. If JS is absent or the script fails,
the disabled input explains the fallback and normal browsing works. Turning off
search removes the UI/index fetch. The destination highlighter still loads when
`search_index=true`, so an indexed page with its own input hidden remains a complete
click-through destination. Set both false for neither UI nor controller; an unavailable index never produces phantom results.

Down/Up move between input/results, Enter follows a real anchor, Escape clears then
leaves native drawer dismissal available. Cmd/Ctrl+K focuses on desktop only, preserving
other editable controls, IME and native mobile behavior. Result hover uses a local
spotlight without tilt/reflow; touch/reduced motion retain static feedback. Both palettes
and EN/ZH use existing tokens/catalogs, no remote font/icon framework.

Result links retain native paths and encode `?kw=` plus an optional actual heading
fragment. Safe text-node operations mark at most 100 match ranges, prioritizing the
selected section; matches can cross inline/code spans without changing copied bytes.
Only the relevant destination/first-hit disclosure ancestors open. Anchored results
keep heading position; unanchored hits scroll to the first useful body mark. Clear
removes only generated marks and `kw`, retaining the hash/other query parameters.
Reload/back restores idempotently; no nested marks, source edits or canonical/share URL
mutation. Existing authored marks/links/math/diagrams/control listeners stay intact.

Queries necessarily appear in the target URL, normal history and the static host's
request logs. The document uses `strict-origin` referrers (no URL query/path leakage)
and index fetch/result navigation use `no-referrer`. No query persistence or external
service transmission is added. Custom analytics/scripts remain the site owner's policy.

### Collection display names

The scoped input/accessible label and index `context` use the owning collection's
local `params.name` when provided, otherwise its title. Scope still uses native URL,
not the name. Indexed document `title` and heading sections keep their full native
titles. Standalone/global search retains site context; no article inheritance,
source rewriting or change to graph/comment identity follows from a display name.

## Build-time reuse and freshness

The own-body renderer extracts search sections while Hugo renders pages in parallel,
then stores the result with its exact normalized HTML and discovery-rule snapshot.
The deferred catalog retains native publication, body-eligibility and graph selection.
It reuses sections only when both snapshots match; otherwise it extracts from the
current body. Custom body renderers therefore retain the safe fallback. No `.Content`
call is added to render hooks and no global edge accumulator is introduced.

Within one extraction, `collections.NewScratch` memoizes each distinct HTML tag's
pure interpretation. Parent skip/caption state remains local to the traversal, not
in the memo. The memo does not survive the call or cross pages/languages/builds.
This avoids parsing repeated highlighter spans without removing code from search,
changing hidden/control exclusions, or replacing rendered text with `.Plain`.

Shared settings calls use one language-and-native-Path cache key, including the
cross-language catalog. Validation and all native/cascade/preset rules remain.
`tests/check_discovery_tokens.py OUTPUT` checks exact token/ancestry/heading semantics;
`tests/check_build_cache_preview.py OUTPUT` uses an owned free-port fixture to verify
body/date/count/ownership/publication and discovery-rule changes during live rebuilds.
