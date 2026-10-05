---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T22:48:24+08:00
title: "Troubleshooting and limits"
params:
  ai_label: generated
---

## Start with a strict, fresh build

Use the verified Hugo 0.166.0 extended and the [minimal configuration](../getting-started/_index.md).
Save a new output/cache pair for each diagnostic build:

```sh
mkdir -p .checks
run=$(mktemp -d "$PWD/.checks/build-XXXXXX")
hugo --destination "$run/public" --cacheDir "$run/cache" \
  --panicOnWarning --printPathWarnings --printI18nWarnings
```

For structural checks of included but unpublished content, build **privately**:

```sh
hugo --buildDrafts --buildFuture --buildExpired \
  --destination "$run/all-states" --cacheDir "$run/all-cache" --panicOnWarning
```

Do not deploy all-states output. A successful watcher render is not proof that old
files were removed from disk; fresh output is authoritative. A preview spanning a
new template/format may need one restart, not cache deletion or unsafe HTML.

## Common symptoms

| Symptom | Check |
|---|---|
| A site setting seems ignored | Presets outrank site fallback; effective native page/cascade outranks presets. Ordinary ancestor params do not cascade. |
| A page has no tree/body | Use branch _index.md, children mode and explicit intermediate parents; later child pagers intentionally omit body. |
| Missing source link | Use exact physical Markdown filename in mounted content namespace, not a logical alias or stale relative path. |
| Native heading warning | Check actual heading ID; custom/shortcode IDs are outside link_heading_checks. |
| Raw HTML/unused component warning | Check outer-%/nested-< notation and cooperating render hooks; do not set unsafe=true as a workaround. |
| Missing captions, attributes or math | Import the narrow native parser/passthrough leaves; inspect list/table/linked-image caption rules. |
| Unexpected provider traffic | Enabled comments load on viewport; badges load automatically; remote images/fonts/media follow their own policy. |
| Old content remains searchable | Deploy fresh HTML/index output, reload to use the new fingerprint; hiding search UI is not indexing opt-out. |
| Missing not-found response | Configure the host to serve generated 404.html with HTTP 404; the theme cannot configure hosting/DNS. |

## Source and route boundaries

Contextual route discovery supports local TOML/YAML Markdown in Hugo's mounted
content filesystem, including shared-directory filename translations and the manual
mounts. Scope paths use lowercase ASCII slug segments and native path routes.
Reserved contextual taxonomy/archive/pagination namespaces, malformed assignments,
collisions and invalid draft metadata diagnose. Do not silently repurpose generated
routes or author private params.sidera fields.

Native ignoreFiles and mount files filtering happen before scope/source discovery:

```toml
ignoreFiles = ['(^|/)(_templates|_utils)(/|$)', '(^|/)editor-report\.md$']
```

Alternatively use a content mount with
`files = ['! _templates{,/**}', '! **/_utils{,/**}']`. Root and nested glob paths are
not interchangeable. Exclusion does not remove secrets already committed to Git,
serve as a sandbox for trusted mounts, or make static/snippet mounts private.

Arbitrary content adapters, computed/cascaded route vocabularies, custom taxonomy
source trees, formats or multidimensional mounts require their own checks; broad
Hugo compatibility is not a promise that every such input is discovered. Native
published Pages determine actual memberships. No failed build is publishable.

## Upgrades and help

Pin the theme revision in your site, inspect normal product changes and test an
isolated copy before updating. Check your native overrides against changed helpers,
both UI languages, source links and publication exclusions. Hugo changes can alter
content-adapter APIs and embedded math rendering: review the KaTeX CSS/fonts with
`hugo env` rather than claiming newer/older releases are supported untested.

For help, open a [repository issue](https://github.com/calfzhou/hugo-theme-sidera/issues)
with a minimal public reproducer. Browser/CSP/font/assistive technology behavior
varies; the theme is not a blanket accessibility, legal or all-browser certification.
