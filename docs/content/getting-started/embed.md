---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T23:21:29+08:00
title: "Embed the manual"
params:
  ai_label: generated
---

The manual belongs to the theme's `docs/content` directory, outside its default
content mount. Do not copy the corpus into your site or run an external docs service.
Choose a namespace with these **site-owned** native mounts:

```toml
[[module.mounts]]
source = 'content'
target = 'content'
[[module.mounts]]
source = 'themes/sidera/docs/content'
target = 'content/manual'

[[menus.primary]]
name = 'Sidera manual'
pageRef = '/manual'
weight = 20
[menus.primary.params]
icon = 'sidera-bold-duotone'
```

Keep the first mount: explicitly replacing content mounts should not drop your
ordinary site content. Mount only the manual, **not the theme repository root**.
README, agent guidance, licenses and technical tests are not content pages.

You can instead use `target = 'content/library/sidera'` and
`pageRef = '/library/sidera'`. The manual root explicitly sets `scope_root: true`;
source-relative links and native resources follow its chosen mount and deployment
prefix. If `library` is itself a children-mode document tree, author its `_index.md`
too. Do not hard-code a URL prefix into manual source links.

The root uses the existing fixed-color Parallax circle as its collection logo.
The menu above independently chooses a color-inheriting UI icon. Disabling UI
icons does not remove the collection image.

## Languages and site policy

Unsuffixed manual files belong to your default content language. For English-only
manual content on a multilingual site, keep English as that default or apply a
native language-specific mount and verify it. A Chinese-only site can use Chinese
controls around the unchanged English body. Adding a real translation later uses
native `_index.zh.md` / `topic.zh.md` filenames with matching language keys, policies
and AI labels; an absent translation is not an English fallback page.

Every current manual node explicitly sets `params.ai_label: generated`. The root
also disables comments locally and by cascade so an embedding site's global
comment policy does not contact a provider merely to display this manual. Preserve
that quiet behavior when overriding manual pages. Your unrelated content is not
relabeled or otherwise changed.

On a multilingual site with an English-only manual, define its menu under
`[[languages.en.menus.primary]]` and `[languages.en.menus.primary.params]`, not
the global menu. A global pageRef would also target the absent Chinese manual
and correctly fail validation.

Native same-path site content can replace a mounted page; it is a replacement,
not a body merge. Keep its required tree/order metadata coherent. Remove the
manual mount and its own menu entry to unpublish it; build into a fresh output
directory. The always-available **docs preset term** is not the manual and does
not mean manual publication is enabled.

## Dates and the default sidebar

The manual keeps explicit native `date` and `lastmod` values in each page's front
matter. They travel with the source when mounted; copying a checkout or rebuilding
does not reset them. No runtime Git history or filesystem timestamp is required.

The manual inherits the normal docs preset leftbar: menu, page tree, recently
updated and recently published. It does not replace the preset's region selection;
normal native consumer cascade/override rules still apply.
