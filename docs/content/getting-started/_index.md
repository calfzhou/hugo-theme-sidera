---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-06T10:22:39+08:00
title: "Getting started"
params:
  ai_label: generated
  children:
    order: [embed]
---

## Install

Use **Hugo 0.166.0 extended** and Git. This is the verified version, not a claimed
minimum or range. In particular, native content-adapter APIs and the bundled KaTeX
0.18.4 CSS/fonts are version-sensitive. Building a site needs no Node, Python,
package installer, sibling repository, credentials or remote rendering service.

Start a new site, initialize Git, and add the public theme:

```sh
hugo new site my-site --format toml
cd my-site
git init
git submodule add https://github.com/calfzhou/hugo-theme-sidera.git themes/sidera
git -C themes/sidera checkout --detach v1.0.0
```

Choose a published stable tag (`v1.0.0` above) from the
[GitHub releases](https://github.com/calfzhou/hugo-theme-sidera/releases). A notes entry
is not proof of publication. Commit `.gitmodules` and the exact theme gitlink in
your site; a submodule is not a floating release. See [release notes and upgrades](../publishing/releases.md). To clone an
existing site, use `git clone --recurse-submodules SITE_URL`, or run
`git submodule update --init --recursive` after cloning. A plain archive of a site
repository does not include its submodule content.

## Configure a minimal site

Replace the generated `hugo.toml` with the following, changing title and baseURL to
your own values before publishing:

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

These narrow imports enable native taxonomies, safe term slugs, H1–H6 TOC, block
attributes/standalone images and dollar-delimited math. Do not import all security
or markup settings, or enable `renderer.unsafe` to silence a warning. The explicit
date chains avoid inventing dates from filesystem time or build time. Time zone,
article permalinks, pagination and deployment remain your site's policies.

## Write your first page

Create `content/notes/_index.md`:

```yaml
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

The home page lists collections automatically. You do not need menus or author
profiles to get a working site. An `index.md` bundle can keep images/code beside it.
See [sections and bundles](../organize/_index.md) before adding more structure.

```sh
hugo --panicOnWarning --printPathWarnings --printI18nWarnings
hugo server --bind 127.0.0.1 --port 1313 --disableFastRender
```

Choose a free port and stop your preview with Ctrl-C. Use a fresh destination for a
release build so old pages/resources cannot survive from an earlier build. Comments
are off by default. Remote content images and optional badges retain their own
network behavior; the minimal site above needs neither.

Next: [embed this manual](embed.md), or consult the official
[Hugo quick start](https://gohugo.io/getting-started/quick-start/) for engine basics.
