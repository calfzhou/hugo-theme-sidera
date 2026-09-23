# Theme-owned native taxonomy and preset defaults

## Implementation checkpoint

Sidera now supplies the native taxonomy definitions and bundled preset **term Pages**.
The consuming showcase no longer duplicates them. This is the first P2-M implementation
slice: **the existing collection/params.sidera consumers have not yet migrated** to the
three-target preset resolver. Do not replace current collection markers with preset alone
yet. Authors/series have native global grouping, not finished attribution/sequence/scoped UI.
The ownership/root rule remains under user discussion; no migration completion is claimed.

## Native configuration import

Hugo 0.166 does not import theme taxonomy/term-permalink categories by default. The site
permits only these categories, without repeating their definitions:

```toml
[ taxonomies ]
_merge = 'shallow'
[ permalinks.term ]
_merge = 'shallow'
```

The definitions live in the theme's `hugo.toml`:

| Native singular key | Authored assignment / native taxonomy |
|---|---|
| tag | tags |
| category | categories |
| author | authors |
| series | series |
| preset | preset |

Site values win; a site may add another taxonomy key or override a term URL rule in these
same native tables. No root-level permissive `_merge`, security/markup import, generated
site config or duplicated taxonomy registry. Existing date/permalink-page/pagination policies
remain site-owned. The current named Sidera roles still use the documented assignment keys;
renaming them is not the same as overriding a public URL.

## Bundled term Pages and language behavior

The theme owns one defaults source, `data/sidera/presets.toml`. A small native content adapter
at `content/preset/_content.gotmpl` creates the blog/notes/docs native term Pages in each
configured language, with existing EN/ZH catalog titles and stable slugs. There is no custom
content parser, automatic preset assignment or preset-name capability switch.

Why an adapter rather than physical `_index.zh.md` files? With English-only configuration,
Hugo treats an unconfigured language suffix as an ordinary content name, creating unwanted
Pages. Native per-language adapter execution avoids those extra standalone pages without
forcing sites to enable another language or add language-specific mounts. It does not require
a new dependency or a second taxonomy engine.

Normal site content wins over a same-path theme adapter Page. To override blog, author
`content/preset/blog/_index.md` (or a configured language-suffixed equivalent):

```yaml
title: My blog preset
slug: blog
params:
  defaults:
    params:
      list_order: title
    cascade:
      params:
        show_updated: true
```

The site file replaces the whole term, including its defaults map; omitted bundled settings
are not secretly deep-merged back. A site can add a fourth preset as another native term Page;
no theme enum change. The data file is bundled implementation source, not a required site
configuration surface or a second source of user membership. Use native term Pages for the
public override path.

`params.defaults.params` and `params.defaults.cascade.params` are published metadata for
the upcoming resolver. Ordinary term params/body still describe that public term. At this
checkpoint those defaults are inspectable but **do not yet change section/article rendering**.

Preset term pages are not bundled theme documentation. The actual docs sample stays under
`docs/content`, outside automatic publication. Its existing explicit consumer mount remains
required; normal builds do not gain `/sidera/` or the sample's resources/nav/sitemap.

## Verification

The showcase's `tests/check_theme_defaults.py` covers native taxonomy import without duplicate
site declarations, term Page kinds/data, scalar preset and multi-author assignments, global
native groups, full site term replacement, fourth preset/additional taxonomy, site URL override,
English-only/Chinese-only/bilingual isolation and no accidental docs or language-suffix Pages.
It uses strict fresh isolated builds; it is not a claim that the remaining P2-M resolver/scoped
series migration or visual acceptance has been completed.
