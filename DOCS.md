# Native page trees and opt-in theme documentation

This guide describes the implemented P2-W behavior retained by the capability-first P2-M model.
A page tree is not restricted to a docs preset. Native branch Pages can have bodies and children;
native leaf bundles remain leaves. The same shared reading renderer handles regular pages and
children-mode sections, including native authors/taxonomies, local resources and TOC.

## Author a body-bearing parent

```yaml
title: Handbook
preset: docs
params:
  children:
    order: [start, reference]
    sort: title
    page_size: 10
    list: true
```

Use `_index.md` for every intended intermediate document parent and `index.md` for a terminal
leaf bundle. `children.order` names logical **immediate child names**, not titles, URLs, file
extensions, or descendant paths. It is a partial order: named children first; remaining children
sort by title/Path (default) or logical name/Path. Native weight does not override this contract.

Order is read from that parent's own source using the existing small TOML/YAML reader. It does
not inherit from native cascade or preset defaults. Other child settings use the effective
parameter map; native local maps replace cascaded maps. Maps also replace across preset/site
fallback tiers. An order-only local map can therefore use the minimal sort/size/list fallbacks;
repeat other child settings where an intentional whole-map override needs them.

Known excluded or other-language children can be valid order references but are omitted from
the current list/tree. Unknown names, duplicate entries, nonchildren, ambiguous leaf/branch source,
invalid settings and missing intermediate branches in children-mode document trees diagnose.
Unreferenced excluded documents require the native all-states validation build in CONTRACT.md;
a draft is not exempt from structural correctness.

## Independent capabilities

The docs preset supplies convenient defaults. An unclassified section can configure them itself:

```yaml
params:
  list_mode: children
  left: [menu, page-tree, taxonomies]
  recent_sections: true
cascade:
  params:
    list_mode: children
    left: [menu, page-tree, taxonomies]
    recent_sections: true
```

The page-tree component also works alongside a recursive article list. There, native non-section
storage folders can flatten into their actual section parent; do not invent intermediate Pages.
Independent nested browsing roots are excluded from the outer tree. Selecting `preset: docs`
alone does not make a subsection independent; set local `params.scope_root=true` when intended.

`children.list=false` hides the direct-child list, not the body or complete navigation tree.
There is one paginator per applicable Page. In children mode, the full body/TOC appears only on
canonical page 1; later child pagers keep title/context and a real link to the full document.
The complete tree/count model never shrinks to the current pager. Generated contextual taxonomy
Pages are not authored children or recent documents. Tags/categories/authors/series stay native.

## Publish the theme sample only by explicit opt-in

The theme owns a single sample source under `docs/content`, outside its automatic content mount.
A consuming site can choose a prefix without copying that source:

```toml
[[module.mounts]]
source = 'content'
target = 'content'
[[module.mounts]]
source = 'themes/sidera/docs/content'
target = 'content/sidera'
```

The first entry preserves normal site content when the site overrides its content mounts.
The showcase keeps this in `docs-on.toml`; normal config is off. Its site-owned handbook remains
ordinary content independent of the optional sample. An alternate nested prefix also works;
the sample root explicitly declares scope_root so its browsing identity survives that mount.
Native relref/resource links follow the mounted Page, not hard-coded URL concatenation.

Site files at the same source path override theme/mounted content natively, not as a two-body merge.
Filename-translated authored sample nodes are supported within the tested mount contract. This is
not a universal arbitrary-contentDir/mount/source inventory guarantee for contextual taxonomies.
The separately bundled **docs preset term** is always available and is not this opt-in sample.

The retained showcase P2-W suite verifies exact order/tree/pagers/body, resources/links, default-off,
explicit-on, alternate prefix, native overrides, structural rejection and EN/ZH behavior.

P2-G renders immediate children with the same optional-cover/term/date card as other lists.
The article footer follows canonical body content and stays absent on later child-list pagers.
No tree/order/mount or source-ownership behavior changes.
