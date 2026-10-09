# Sidera

An independent **Hugo theme for blogs, notebooks and documentation**, inspired by
**[Hexo Stellar 1.44.0][stellar-144]** by **[xaoxuu][xaoxuu]** — not an official port or its configuration API.

- Native sections/bundles, optional presets, tags, authors and chronological series.
- Ordered body-bearing docs trees; source-relative Markdown links and local resources.
- English/Simplified Chinese UI, light/dark/auto, native menus and configurable widgets.
- Local search/backlinks, math, code inclusion, safe content components, local diagrams and interactive ECharts.
- Optional Giscus comments; no comments or manual publication on ordinary activation.

## Live site

[GoCalf](https://gocalf.com/) is a live site built with Sidera.

## Quick start

Use **Hugo 0.166.0 extended** and Git. This is the verified version, not an untested
support range. Normal builds need no Node, Python, package installer or sibling repo.
Native adapter APIs and the matching bundled KaTeX 0.18.4 assets are version-sensitive.

```sh
hugo new site my-site --format toml
cd my-site
git init
git submodule add https://github.com/calfzhou/hugo-theme-sidera.git themes/sidera
git -C themes/sidera checkout --detach v1.0.0
```

Choose a published stable tag from [Releases](https://github.com/calfzhou/hugo-theme-sidera/releases)
(`v1.0.0` above). A manual release-notes entry alone does not mean its tag is published.
Commit `.gitmodules` and the exact `themes/sidera` gitlink in your site. Existing site
clones need `git submodule update --init --recursive`; this restores the committed
revision, not the newest tag or main tip.
Replace generated `hugo.toml` with this, using your own URL/title before publishing:

```toml
baseURL = 'https://example.org/'
title = 'My notebook'
theme = 'sidera'
defaultContentLanguage = 'en'
locale = 'en-US'

[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'
[markup.tableOfContents]
_merge = 'shallow'
[markup.goldmark.parser]
_merge = 'deep'
[markup.goldmark.parser.attribute]
_merge = 'shallow'
[markup.goldmark.extensions.passthrough]
_merge = 'deep'

[frontmatter]
date = ['date', 'publishDate', 'pubdate', 'published']
publishDate = ['publishDate', 'pubdate', 'published', 'date']
lastmod = ['lastmod', 'modified', 'publishDate', 'pubdate', 'published', 'date']

```

Create `content/notes/_index.md`:

```markdown
---
title: Notes
preset: notes
---
A notebook of useful observations.
```

Create `content/notes/hello/index.md`:

```markdown
---
title: Hello, Sidera
date: 2026-01-01T09:00:00Z
tags: [learning]
---
## One useful idea

Keep the source simple and make the links meaningful.
```

Run `hugo --panicOnWarning`, then
`hugo server --bind 127.0.0.1 --port 1313 --disableFastRender` on a free port.
Stop with Ctrl-C. Build releases into a fresh destination, not a stale preview folder.
The narrow imports above preserve safe Markdown; do not broadly enable unsafe HTML.

## Updates: stable releases or main

Normal consumers select a published tag deliberately:

```sh
git -C themes/sidera fetch origin --tags
git -C themes/sidera checkout --detach v1.0.0
# Build/test your site, then commit the updated themes/sidera gitlink.
```

Owners testing ongoing development can instead follow `main`:

```sh
git -C themes/sidera fetch origin main
git -C themes/sidera switch main
git -C themes/sidera merge --ff-only origin/main
# Build/test your site, then commit the updated themes/sidera gitlink.
```

Check for local changes before either workflow; stop on divergence rather than
resetting work. If an existing submodule has no local main branch, use
`git -C themes/sidera switch --track origin/main` once. Neither a `main` branch
setting nor a build automatically advances a site's committed submodule pin.
Git tags are the version source of truth; there is no separate VERSION file.
See [release notes](docs/content/publishing/releases.md).

## User manual

Read online: [Sidera user manual | GoCalf](http://gocalf.com/sidera/).

[Read the manual source](docs/content/_index.md), starting with
[Getting started](docs/content/getting-started/_index.md). It covers organization,
customization, authoring, reader features, [parameters](docs/content/publishing/parameters.md)
and [shortcodes](docs/content/publishing/shortcodes.md).

To render the manual on your own site, explicitly add:

```toml
[[module.mounts]]
source = 'content'
target = 'content'
[[module.mounts]]
source = 'themes/sidera/docs/content'
target = 'content/manual'
```

No copying or external docs service is required. Choose another prefix if preferred;
[embedding instructions](docs/content/getting-started/embed.md) include the native
`pageRef` menu with `sidera-bold-duotone`. The other original logo-icon styles are
`sidera-bold`, `sidera-linear`, `sidera-line-duotone`. Manual pages visibly disclose
AI generation and keep comments off. Theme UI languages do not auto-translate bodies.

## Help, contributing and rights

[Help and troubleshooting](docs/content/publishing/troubleshooting.md) ·
[Issues](https://github.com/calfzhou/hugo-theme-sidera/issues) ·
[Contributor/agent guidance](AGENTS.md)

Original Sidera material is [MIT licensed](LICENSE), copyright 2026 Calf.
[Third-party notices](THIRD-PARTY-NOTICES.md) retain [Stellar][stellar]'s MIT credit to [xaoxuu][xaoxuu],
Solar CC BY attribution and bundled renderer/font terms; they are also published
with generated pages. This does not license your site content or imply endorsement.

[stellar]: https://xaoxuu.com/wiki/stellar/
[stellar-144]: https://github.com/xaoxuu/hexo-theme-stellar/tree/1.44.0
[xaoxuu]: https://xaoxuu.com/
