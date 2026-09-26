+++
title = "Publish the sample"

+++

A consuming site chooses a native filesystem mount and a namespace. No route prefix is embedded in these links.

[Return to the documentation root](../_index.md).

## Page shell

The shared shell also applies to standalone pages. New layout settings live under
`params`: `left` and `right` are ordered component arrays; `false` or `[]`
disables a region. Omitted keys use the applicable preset defaults, then site settings; ordinary ancestor
params do not implicitly cascade. A right `toc` component disappears when there are no body headings.
See the theme's SHELL.md for the implemented contract; footer customization is not
part of this slice.
