---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T22:48:24+08:00
title: "Reader features"
params:
  ai_label: generated
  children:
    order: [comments, configured-markdown]
---

## Search your current collection or the whole language

Search is local: a published, current-language JSON index and browser matching, no
remote query service or account. On a collection page it starts in that browsing
scope. Type a query, optionally select **Search all content**, and follow a page
or heading result. Clear/Escape restores navigation. Desktop Cmd/Ctrl+K focuses
search; arrow keys move through results. No-JS leaves ordinary browsing available.

Matching is literal, case/diacritic-insensitive substring matching, not regex,
fuzzy search or CJK word segmentation. Results require all query tokens in one
section or the page title. The bounded UI accepts up to 160 UTF-16 units/eight
unique tokens and returns at most 40 results. Destination links carry `?kw=` and
real heading IDs; safe text-node highlights can open the relevant fold. Queries
therefore appear in history and ordinary host request logs: do not search secrets.

The local index is prefetched with no persistent browser cache and revalidated on
focus. Its fingerprint changes with the build; reload an old page to discover a
new deployment's index. It contains published normalized body text, not source
paths or hidden copy payloads. Formulas/diagram internals/control text are excluded;
prose descriptions, captions and displayed code/snippet selections are searchable.

## References connect real content

The default article footer can show outgoing links and backlinks from rendered
native links/link cards. Repeated query/hash mentions collapse to one Page pair.
Self links, images/resources, external URLs, menus, TOC and footer references do
not invent body relationships. Explicit cross-scope/language links retain their
actual targets; no translation guessing or network crawl is involved.

`params.references` is separately authored Markdown credit, not an automatic graph.
Raw HTML, arbitrary third-party shortcode markup or custom hooks without the
native target annotation are not universally indexed as relationships.

## Visibility is not privacy

The [parameter reference](../publishing/parameters.md) describes three independent
booleans: `search` controls the UI/fetch, `search_index` controls inclusion in a
language index, and `link_graph` controls both graph directions. Hiding a menu or
search box does not remove a public page. Scope filtering is browser-side UX over
an already public index, not access control.

Native publication/body eligibility excludes drafts, future/expired, headless and
unlisted/link-only bodies in normal output. A private all-states validation build
changes those facts. Always deploy a fresh output directory and never publish that
private build. See [troubleshooting](../publishing/troubleshooting.md).

## Optional interactions

[Comments](comments.md) are off by default and require your own verified Giscus
setup. [Configured Markdown](configured-markdown.md) can personalize sidebar/footer
text without executing a template in configuration. Sharing/edit links are described
with [footer choices](../customize/navigation.md#footer-choices).
