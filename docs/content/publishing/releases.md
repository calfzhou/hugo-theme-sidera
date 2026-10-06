---
date: 2026-10-06T10:22:39+08:00
lastmod: 2026-10-06T10:22:39+08:00
title: "Releases and upgrades"
params:
  ai_label: generated
---

Git tags are Sidera's version source of truth. Check the
[published releases](https://github.com/calfzhou/hugo-theme-sidera/releases) before
selecting a version; notes in this manual do not by themselves publish a tag.
The GitHub Release uses the corresponding section below, not a second changelog.

## Choose an update channel

Use a published stable tag for a normal site. Fetch tags, check out your selected
tag in `themes/sidera`, build and test your site, then commit that exact gitlink.
Keep the previous site commit for an ordinary dependency rollback.

Owners may instead update from `origin/main` deliberately, using a clean checkout
and a fast-forward-only theme update. Test before committing the new consumer pin.
Main can contain unreleased changes. Clone/submodule-update/build restores the
committed pin; it does not automatically select the newest main commit or release.
See the repository [README](https://github.com/calfzhou/hugo-theme-sidera/blob/main/README.md)
for both command sequences, and [troubleshooting](troubleshooting.md) for checks.

## v1.0.0

First Sidera release: an independent Hugo theme for blogs, notebooks and documentation,
inspired by Hexo Stellar 1.44.0 rather than compatible with its configuration API.

- Native sections and page bundles, optional blog/notes/docs presets, tags and
  categories, authors, chronological series and ordered documentation trees.
- English/Simplified Chinese UI; light, dark and automatic appearance; native menus,
  configurable sidebars and footers, local icons and a localized custom 404 page.
- Source-relative Markdown links and local resources; local full-text/heading search,
  outgoing links and backlinks; code inclusion/downloads, math and safe content components.
- Locally bundled Mermaid/drawio rendering, optional images/video/badges and Giscus
  comments; progressive page-entry motion with reduced-motion and no-JS fallbacks.
- Optional, shallow user manual with visible AI-generated disclosure. Activating the
  theme alone publishes neither the manual nor comments.

**Requirements:** Git and **Hugo 0.166.0 extended**, the verified engine version.
Bundled KaTeX 0.18.4 assets match that renderer. Normal builds need no Node, Python
or package installer; no wider Hugo compatibility range is asserted.

**Limits:** comments and other external providers require their own setup/network;
body translations are author-owned; search hiding is not a privacy boundary. Use
native publication/exclusion rules for private content. Existing AI-label colors
are intentional and do not all meet AA text contrast in light mode.

**Rights:** original Sidera material is MIT, copyright 2026 Calf. Stellar, Solar and
bundled renderer/font notices retain their respective terms; site content is not
relicensed. See [credits and licenses](https://github.com/calfzhou/hugo-theme-sidera/blob/main/docs/content/publishing/credits.md).
