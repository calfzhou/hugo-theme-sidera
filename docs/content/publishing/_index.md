---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-05T22:48:24+08:00
title: "Reference and help"
params:
  ai_label: generated
  children:
    order: [parameters, shortcodes, troubleshooting, credits]
---

Use these references when a tutorial leaves a configuration detail open:

- [Public parameters](parameters.md): placement, defaults, inheritance, component options.
- [Shortcodes](shortcodes.md): supported arguments, resource boundaries and notation.
- [Troubleshooting](troubleshooting.md): build diagnostics, publication and upgrade checks.
- [Credits and licenses](credits.md): original MIT material and retained upstream rights.

The manual covers the implemented public API, not every Hugo feature or internal
helper. Theme source/tests are authoritative for runtime behavior. Start from the
[minimal site](../getting-started/_index.md) when isolating a problem, and keep
optional services disabled until you intend to use them.

Project development instructions live outside the manual in repository `AGENTS.md`.
For a reproducible issue, include Hugo version, relevant config/front matter and a
small public example at the [repository issue tracker](https://github.com/calfzhou/hugo-theme-sidera/issues).
Do not include credentials, private articles or generated archives of your whole site.
