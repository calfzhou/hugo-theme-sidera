---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T22:48:24+08:00
title: "Optional Giscus comments"
params:
  ai_label: generated
---

Giscus is the only built-in provider, **off by default**. Before enabling it, use the
[official configurator](https://giscus.app/) to verify a public repository with
Discussions enabled, Giscus App access and a real category (Announcements is
recommended; not polls-only). Repository/category node IDs are not display names.
Do not place a GitHub token in public config.

After verification, put these site/language settings in your own config, replacing
all four marked strings. This schema illustration is **not operational metadata**:

```toml
[params.giscus]
repo = 'OWNER/REPOSITORY'
repo_id = 'COPY_REPOSITORY_NODE_ID'
category = 'COPY_CATEGORY_DISPLAY_NAME'
category_id = 'COPY_CATEGORY_NODE_ID'
strict = false
reactions = true
input_position = 'top'
```

Then set `params.comments: true` only on intended pages, by native cascade, or as a
site fallback. Page false wins. Provider/identity settings are site/language-only,
not page/preset/cascade options. Missing identity shows unconfigured text with no
provider requests. Unknown fields/invalid types diagnose. Repository/app/category
changes are separate owner actions; do not post test comments/reactions to verify setup.

## Loading and placement

Configured comments load automatically when their canonical article-end slot becomes
visible, immediately when IntersectionObserver is unavailable. They contact Giscus/
GitHub and disclose network information and the embedding URL. There is no consent
button or separate loading mode. Keep secrets out of URL query strings. Disabled or
unconfigured pages do not load the provider; this manual explicitly stays disabled.

Comments follow body/footer, reading navigation and any docs child list, before
`article_end_text`. They appear on regular pages and children-mode section bodies,
not home/lists/generated views or later child pagers. The TOC offers a native Join
the discussion link only when the slot exists. No footer component/shortcode is needed.
No-JS, blocked resources and timeout/error show honest localized fallback states.

## URL identity matters

Discussion term is the **path of native Page.Permalink**, with leading slash and a
terminal file extension removed; `/` becomes `index`. Trailing slash, deployment
subpath, locale and escaping matter. Host/port/query/hash do not identify a thread.
Different translated URLs have separate discussions. Changing a path can change a
thread even when redirects work. Local preview backlinks may be localhost: do not
post from previews. `strict=false` is the default; strict matching requires the
corresponding discussion hash and does not retrofit existing threads.

Theme controls use EN/ZH; provider locale is en or zh-CN. A small stylesheet uses
Giscus's supported theme API to match Sidera's baseline light/dark/font stack, not
cross-origin DOM access or arbitrary site CSS synchronization. Giscus is an external,
unpinned live service and has its own auth/storage/CSP needs. Sidera does not weaken
CSP or bypass blockers. Native provider partial overrides are trusted site code;
no other provider ships by implication.
