---
title: "Ordered document trees"
params:
  ai_label: generated
---

Use `_index.md` for body-bearing parents and `index.md` or `topic.md` for leaves.
The docs preset selects children mode and a full page tree, but those capabilities
are available to any section without a preset.

```yaml
---
title: Handbook
preset: docs
params:
  children:
    order: [start, reference]
    sort: title
    page_size: 10
    list: true
  navigation_mode: sequential
---
An introduction that remains visible above the child list.
```

`children.order` is a **parent-local partial order** of immediate logical child
names: not titles, URLs, extensions or descendant paths. Named children come first;
remaining children sort by title/Path, or by logical name/Path with `sort: name`.
Native weight does not override this policy. Do not cascade the order or put it in
a preset. Repeat other child settings when a local whole-map replacement needs them.

Known draft or other-language children can be named but are absent from the current
list/tree. Unknown names, duplicates, nonchildren, ambiguous bundle sources and
missing intermediate branches in a children-mode tree diagnose rather than being
silently reordered.

## List, tree and reading navigation are independent

`children.list: false` hides the direct-child cards, not the body or navigation tree.
The tree always shows the complete eligible sequence. Paginating a long child list
shows full body/TOC only on canonical page 1; later pagers link back to that body.
A page-tree component can also accompany a recursive article list.

Choose `navigation_mode` on the **collection root only**:

- `list`: the collection's main list, with its sort/pins; no Parent control.
- `siblings`: the actual parent's complete ordered children; includes Parent.
- `sequential`: root then ordered subtrees, depth-first; includes Parent.

Docs default to siblings; blog/notes to list. Independent nested roots own their
own sequence. Controls never wrap or invent missing parents/translations and do not
depend on child-card pagination or browser history. Series outlines are independent.

This manual itself uses no more than three authored levels: root → group → topic.
That is its editorial organization, not a new runtime limit on your own trees.

![A parent and two connected child nodes](../nodes.svg "A body-bearing parent can link to child documents.")
