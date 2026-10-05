# Sidera

A Hugo theme for blogs, notebooks, documentation and connected knowledge, inspired
by Stellar. Sidera uses native content, taxonomies, resources and template lookup;
it is not a Stellar configuration port.

## Requirements and setup

Use **Hugo 0.166.0 extended**. Building does not require Node, Python, a package
installer or a sibling source checkout. Initialize the consuming site's exact
committed theme submodule with `git submodule update --init --recursive`.

A consuming site's minimal configuration includes:

```toml
theme = 'sidera'
[taxonomies]
_merge = 'shallow'
[permalinks.term]
_merge = 'shallow'
[markup.tableOfContents]
_merge = 'shallow'
```

Choose the site's base URL, language, time zone, date chains and article permalinks
explicitly. [CONTRACT.md](CONTRACT.md) is the authoritative content/configuration
reference, including narrow markup imports for advanced Markdown. Do not broadly
merge security settings or enable unsafe HTML merely to render ordinary content.

```sh
hugo --panicOnWarning
hugo server --bind 127.0.0.1 --port 1313 --disableFastRender
```

Use a free preview port and stop the server with Ctrl-C. Authoritative build checks
should use a fresh destination; preview state is not proof that removed or excluded
files are absent from a deployment artifact.

## Content model

- Native top-level sections are browsing roots; nested roots opt in with local
  `params.scope_root: true`.
- `preset: blog`, `notes` or `docs` on a section supplies optional defaults. It does
  not establish scope or impose a content type. Native cascade and explicit false /
  empty overrides retain precedence.
- Tags, categories, authors and series use native top-level metadata. Global
  identities and contextual views share one source of truth. Archives and tag /
  category vocabulary indexes are complete; article/term results paginate.
- `index.md` forms a leaf bundle; `_index.md` forms a body-bearing branch. Source-
  relative Markdown links and adjacent public resources remain editor-friendly.
- Missing dates are not invented from Git, filesystem modification time or build
  time. `type: story` selects reading typography; optional `params.ai_label` is an
  explicit localized disclosure, not an authorship or license claim.
- Native content exclusions apply before taxonomy/scope discovery. Editor settings,
  templates and support files should be excluded explicitly; hidden UI is not privacy.

## Guides

| Area | Reference |
|---|---|
| Content, native fields, scope and validation | [CONTRACT.md](CONTRACT.md) |
| Optional presets and inheritance | [PRESETS.md](PRESETS.md) |
| Menus, sidebars, footers, widgets and appearance | [SHELL.md](SHELL.md) |
| Tags, categories, authors, series and exclusions | [TAXONOMIES.md](TAXONOMIES.md) |
| Body-bearing page trees and opt-in documentation | [DOCS.md](DOCS.md) |
| Markdown, images, attributes, math, code and story text | [MARKDOWN.md](MARKDOWN.md) |
| Native source links, resources, queries and fragments | [LINKS.md](LINKS.md) |
| Exact code-file inclusion and downloads | [SNIPPETS.md](SNIPPETS.md) |
| Containers, cards, timeline, images and inline components | [COMPONENTS.md](COMPONENTS.md) |
| Mermaid, drawio and GitHub badges | [DIAGRAMS.md](DIAGRAMS.md) |
| Click-to-load video | [VIDEO.md](VIDEO.md) |
| Search, destination highlighting and reference graph | [DISCOVERY.md](DISCOVERY.md) |
| Optional Giscus comments and identity/privacy rules | [COMMENTS.md](COMMENTS.md) |
| Build-time configured Markdown interpolation | [CONFIG-MARKDOWN.md](CONFIG-MARKDOWN.md) |
| English/Chinese UI messages | [I18N.md](I18N.md) |
| Named Solar icons and site overrides | [ICONS.md](ICONS.md) |
| Optional Parallax identity resources | [IDENTITY.md](IDENTITY.md) |

Routine customization uses native site/language params, menus, cascade and data.
Advanced overrides use Hugo's normal partial/asset lookup. Font stacks do not
implicitly download fonts; external font loading remains a site choice.

Comments are off by default. Set up the consuming site's own verified Giscus
repository/category identity before enabling them. Remote images, badges, fonts,
video and comment providers retain the network policies documented in their guides.
No site token belongs in public configuration.

## Not-found page

The native `404.html` uses a local Solar warning visual, localized recovery text and
Home action within the shared shell. It has no article metadata/comments or search /
sitemap membership and carries `noindex`. Hosts must independently serve it with
HTTP 404 for missing URLs. Generating a file does not configure hosting or DNS.

## Verification

Tests in `tests/` create isolated fixtures and require a fresh output-directory
argument. Python checks use the standard library; browser checks use the consuming
project's documented isolated harness, never an unrelated live browser profile.

```sh
python3 tests/check_content_exclusions.py /absolute/fresh-exclusion-check
python3 tests/check_taxonomy_indexes.py /absolute/fresh-taxonomy-check
python3 tests/check_archives.py /absolute/fresh-archive-check
```

Keep generated output outside tracked source. Do not execute included article code,
post provider comments/reactions, or publish a test site as part of local verification.
Version-sensitive adapter APIs are tested on the declared Hugo version; rerun the
relevant checks before upgrading.

## Attribution and rights

[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) records Stellar, Solar, KaTeX,
diagram runtime and other applicable provenance/terms. Its matching asset is linked
from generated pages so notices remain available after minification. Keep both
copies synchronized. Third-party terms do not grant an overall distribution license
for original Sidera code/artwork or license a consuming site's content.
