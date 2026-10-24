---
date: 2026-10-14T23:05:00+08:00
lastmod: 2026-10-23T23:08:07+08:00
title: "Interactive JSX"
params:
  ai_label: generated
---

Add small React tools to ordinary `.md` articles with a `jsx-live` fence or `jsx`
shortcode. Hugo compiles JSX; the browser runs the component. No MDX conversion,
Node compilation step, CDN, or npm installation is needed for the bundled React
APIs. The rest of the article keeps Hugo's normal Markdown rendering.

## Explicitly trust executable content

Enable this feature in your site's configuration, not article front matter:

```toml
[params]
jsx = true
```

The default is disabled. Enabling it authorizes executable content throughout the
site (or the language whose parameters you configure). Review component code and
imports like other site JavaScript. This is **not** a safe language for untrusted
contributions or generated code that has not been reviewed.

Ordinary `jsx` fences, `snippet` inclusions and files merely attached to a page are
still display-only. Only the explicit `jsx-live` fence or `jsx` shortcode mounts a
component. Goldmark's unsafe HTML setting can remain off.

## A component in a Markdown fence

Use a normal JSX module whose **default export is a React component**:

````text
```jsx-live {title="Counter" caption="Each click adds one." fallback="The counter starts at zero."}
import { useState } from 'react';
import { Row } from 'sidera/ui';

export default function Counter() {
  const [count, setCount] = useState(0);
  return <Row>
    <output className="jsx-metric" aria-live="polite">{count}</output>
    <button type="button" onClick={() => setCount(n => n + 1)}>Add one</button>
  </Row>;
}
```
````

React hooks belong inside components. JSX is not MDX: `**bold**`, headings and lists
inside JSX are not parsed as Markdown. Keep explanations outside the fence or use
normal JSX elements such as `<strong>` and `<p>` inside it. Do not call `createRoot`
yourself; Sidera owns the mount point and gives each instance a unique React ID prefix.

A component can also be placed in a paired shortcode:

```text
{{</* jsx title="Counter" */>}}
import { useState } from 'react';
export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(n => n + 1)}>Count: {count}</button>;
}
{{</* /jsx */>}}
```

This is a **block** component, not an in-sentence inline shortcode. In nested folds,
boxes or grid cells, use the normal outer-`%`/nested-`<` [composition](components.md).
Do not embed Hugo shortcode syntax in JavaScript strings without escaping it;
Hugo processes shortcode delimiters before the JSX compiler sees the source.

## Page-bundle files and imports

```text
content/posts/encoder/
├── index.md
└── widgets/
    ├── Encoder.jsx
    ├── encoding.js
    └── encoder.css
```

```text
{{</* jsx src="widgets/Encoder.jsx" css="widgets/encoder.css" title="Base64 encoder" /*/>}}
```

Use the explicit self-closing `/>` form when there is no body. An empty `jsx-live`
fence with the same `src` attribute is equivalent. `src` must be an exact,
case-sensitive `.jsx` resource key of the current page. No wildcards, traversal,
remote URL or basename guessing. A source file and an inline body cannot compete.

**Local imports use Hugo's page-resource namespace.** Write keys relative to the
page-bundle root, even from a module inside a subdirectory:

```jsx
// widgets/Encoder.jsx
import { useState } from 'react';
import { encode } from './widgets/encoding.js';
```

This deliberately uses `./widgets/encoding.js`, not `./encoding.js`. Hugo's
`importContext` resolves resource keys as written; it is not a general
filesystem-relative module resolver. Use explicit extensions. Keeping widget
modules at the bundle root makes simple `./helper.js` imports natural. Shared
modules in `assets/` and additional installed npm packages follow Hugo's native
resolution rules; Sidera does not fetch or install dependencies during a build.

Sidera also supplies the optional `Stack` and `Row` layout helpers through
`import { Stack, Row } from 'sidera/ui'`. This is a built-in Hugo build alias, not
an npm package to install. It works in inline fences and attached modules, in both
page and sandbox modes. Its small implementation is bundled only when imported.

The supported shared React package imports are `react`, `react/jsx-runtime`,
`react-dom` and `react-dom/client`, pinned to **19.3.0** (Scheduler **0.28.0**).
All page-mode islands use one React instance through an import map. Do not bundle
a second React copy or install libraries requiring an incompatible React version.
Other React subpaths, compiler plugins and arbitrary package compatibility are not
promised. Modern browsers with ES modules and import maps are required.

Use the explicit `css` option for a page-local stylesheet, **not `import './x.css'`**.
The latter is not supported by this integration's Hugo 0.166.0 `js.Build` path and
ordinary CSS imports fail compilation. The stylesheet follows native resource
minification/fingerprinting; URLs in CSS are not rewritten into bundle imports.

Source and compiled assets are public. Hugo can publish original page-bundle
attachments too. Not displaying source in the article does not hide code or secrets.

## Options

| Name | Contract |
|---|---|
| `src` | Optional exact current-page `.jsx` resource; excludes a body |
| `css` | Optional exact current-page `.css` resource |
| `title` | Optional nonblank plain-text label above the component; not an article heading |
| `caption` | Optional nonblank plain-text figure caption below the component |
| `appearance` | `plain` (default) or `card`; independent of execution mode |
| `fallback` | Optional nonblank plain text for no-JS/loading/error/print; localized generic text when omitted |
| `mode` | `page` (default) or `sandbox` |
| `height` | Sandbox only; integer 160–1200 pixels, default 280 |

Each entry source is limited to 1 MB. This is not a limit on imported libraries or
the component's runtime resource usage. Unknown options, invalid paths and JSX
syntax errors fail the build. Missing default exports and rendering/import failures
show a local error and the authored fallback without replacing the article.

## Titles, captions and appearance

Components are **frameless by default**: no outer border, background or padding.
Normal vertical separation from surrounding prose remains. `appearance="card"`
adds a padded, bordered panel; it does not change execution permissions. Internal
controls and result panels keep their styling in either appearance.

```text
{{</* jsx src="Calculator.jsx" title="Reading-time estimate" caption="Adjust the speed to compare estimates." appearance="card" /*/>}}
```

A title identifies the tool above its controls; it does not create a heading or
TOC entry. A caption describes it below, using the same styling as image and
diagram captions. Both are optional: omit a title when the article heading or
component already supplies one, and avoid repeating the same text in both places.
An isolated iframe is labeled by title, then caption, then a localized default.

## Optional layout helpers

Use native elements for controls and meaning. `Stack` and `Row` only arrange their
children; they do not introduce another control library or automatically assign
form, toolbar or field semantics.

```jsx
import { useState } from 'react';
import { Stack, Row } from 'sidera/ui';

export default function Actions() {
  const [count, setCount] = useState(0);
  return <Stack>
    <output aria-live="polite">Count: {count}</output>
    <Row style={{ justifyContent: 'flex-end' }}>
      <button type="button" onClick={() => setCount(0)}>Reset</button>
      <button type="button" onClick={() => setCount(n => n + 1)}>Add one</button>
    </Row>
  </Stack>;
}
```

| Helper | Default layout |
|---|---|
| `Stack` | Vertical grid, full-width children, standard spacing |
| `Row` | Horizontal flex row, vertically centered, wrapping on small screens |

Both render a single `div` using the same CSS as `jsx-stack` / `jsx-row`. Native
elements with those classes remain supported; wrappers and classes can be mixed.
Normal div props, including `id`, `className`, `style`, `aria-*`, `data-*`, event
handlers, children and React refs, pass through. Keep actual forms, labels,
fieldsets and outputs as native elements.

The optional `gap` prop accepts one of `none`, `small`, `normal`, or `large`:

| Value | Spacing |
|---|---|
| `none` | Zero |
| `small` | Compact spacing, useful for a label/control group |
| `normal` (default) | Existing theme spacing for that layout; Stack and Row have different defaults |
| `large` | More separation between groups |

Unsupported gap values trigger the component's normal error fallback. Use `style`
for a deliberate custom value rather than passing arbitrary CSS to `gap`.

### Row alignment

Use standard Flexbox through `style`; there are no separate `align` or `justify`
props. For example, `<Row style={{ justifyContent: 'center' }}>` centers a group.

| `justifyContent` | Horizontal placement in the default left-to-right row |
|---|---|
| `flex-start` | Start/left (default) |
| `center` | Centered group |
| `flex-end` | End/right |
| `space-between` | First/last items at opposite edges; remaining space between |
| `space-evenly` | Equal free space between items and at both edges |

`alignItems` controls the cross axis: `center` is the default; `flex-start`,
`flex-end`, `baseline`, and `stretch` are useful alternatives. The `gap` is minimum
spacing, not a replacement for alignment. Wrapped rows distribute space separately
on each line. Repeated alignment choices can instead live in a component-scoped
CSS class; no extra wrapper component is required.

## Styling and page integration

Start without a component stylesheet. Native buttons, labels, inputs, selects and
textareas inherit Sidera's typography, palette, focus and disabled treatment.
`aria-invalid="true"` marks invalid controls; `aria-pressed` gives toggle buttons
a selected appearance. These defaults are scoped to JSX roots, not ordinary article
content, and are also available in sandbox mode. Errors and invalid-control borders
use `--danger`, independently of pinned-label styling.

### Author-facing CSS classes

These classes are supported authoring conveniences inside a JSX component. Use
them directly with native elements, or alongside `Stack` and `Row`. They avoid
recreating ordinary theme styles; custom classes remain welcome for special UI.

| Class | Purpose |
| --- | --- |
| `jsx-stack` | Vertical layout with standard gaps, without extra paragraph margins |
| `jsx-field` | A label and its control/help text grouped with a smaller gap |
| `jsx-row` | Wrapping row of actions or related values |
| `jsx-gap-none` / `jsx-gap-small` / `jsx-gap-large` | Gap modifiers for `jsx-stack` or `jsx-row`; omit for normal spacing |
| `jsx-note` | Muted help or secondary text |
| `jsx-error` | Validation message; empty messages take no space |
| `jsx-result` | Result panel with the theme accent and spacing for child elements |
| `jsx-metric` | Prominent numeric value |

Renderer-owned classes such as `content-jsx`, `jsx-root`, `jsx-title`, `jsx-status`,
`jsx-fallback` and `jsx-frame` are not author layout primitives. Do not add these
wrappers yourself or depend on their internal markup to build a component.

`jsx-result` uses normal UI typography. Use native `<samp>` for machine output;
it gets the theme's monospace font. For example, this component needs **no CSS file**:

```jsx
import { useId, useState } from 'react';
import { Stack } from 'sidera/ui';

export default function Greeting() {
  const id = useId();
  const [name, setName] = useState('Sidera');
  const error = name.trim() ? '' : 'Enter a name.';
  return <Stack>
    <Stack gap="small">
      <label htmlFor={id}>Name</label>
      <input id={id} value={name} onChange={e => setName(e.target.value)}
        aria-invalid={!!error} aria-describedby={`${id}-hint ${id}-error`} />
      <p id={`${id}-hint`} className="jsx-note">Only used in this component.</p>
    </Stack>
    <p id={`${id}-error`} className="jsx-error" aria-live="polite">{error}</p>
    <output className="jsx-result" aria-live="polite">
      {error ? 'Waiting for a name.' : `Hello, ${name}!`}
    </output>
  </Stack>;
}
```

The wrappers and classes are layout/presentation conveniences, not a control
library. Authors still provide labels, validation logic, keyboard interaction and
appropriate live announcements; a CSS
class does not supply accessibility semantics.

### Component-specific styles

Custom styles remain useful for unusual geometry, visualizations or deliberate
presentation choices: a connected calendar table, a larger reading output, or a
fixed-height encoded result. Keep those rules with the component via the optional
`css` resource. Prefer theme tokens such as `--text`, `--muted`, `--accent`,
`--surface`, `--danger` and `--code` over redefining ordinary controls or writing separate
light/dark palettes. Defaults have low specificity so scoped custom classes can
override them without `!important`. For filled custom controls, pair `--accent-fill`
with `--accent-on-fill` and use `--accent-fill-hover` for the hover background.
These three roles and `--danger` are included in the sandbox theme-token bridge.

### Page integration

Page mode renders directly into the article.
Scope custom CSS to your component's class. The page is **not a CSS or JavaScript
sandbox**. Components can use browser APIs, read page storage, make network requests
(subject to the site's policy), and alter the page. For example:

```jsx
export default function LightButton() {
  return <button onClick={() => window.Sidera.setColorMode('light')}>Light mode</button>;
}
```

`Sidera.setColorMode()` accepts `light`, `dark` or `auto`, updates the site's controls
and preserves the visitor preference when storage is available. Components should
clean up subscriptions/listeners in effects. Component-local state is independent
between mounts; JavaScript module-level variables remain shared on the page.

Do not let theme DOM-enhancement scripts mutate React-owned elements. This feature
is intended for small tools, not replacing the article, its headings or navigation.

## Optional sandbox

```text
{{</* jsx src="widgets/Calculator.jsx" mode="sandbox" height=320 title="Calculator" /*/>}}
```

The component runs in an opaque iframe with `allow-scripts` only. Its fixed height
is author-controlled; overflowing content can scroll within the frame. A small
validated message channel updates the light/dark palette and theme tokens. There
is no bridge for storage, theme switching, navigation or arbitrary host operations.

Its CSP permits local scripts/styles but blocks connections, images, fonts, forms,
objects and nested frames. It has no parent DOM access or usable site localStorage.
Libraries that require those capabilities will not work here. The frame gets its
own React realm; it cannot share the parent's live React instance.

This isolates DOM and styling, not CPU/memory consumption. Neither mode makes
infinite loops safe. Render error boundaries do not catch every asynchronous or
event-handler exception. Do not run untrusted code in either mode.

## Loading, fallback and preview

Page-mode modules load near the viewport, including after a closed fold opens.
An imported module's top-level statements run on import, not on first click.
There is no automatic source-code disclosure. The fallback text remains visible
without JavaScript, during loading or after failure. Print output uses fallback text.
Widget values are not server-rendered, included in the article TOC, or dynamically
added to search/RSS. Titles, captions and fallback explanations can be indexed;
runtime controls are excluded from Sidera's search body.

Hugo only **compiles** author code; it does not import or server-render it during
builds. Browser globals can therefore be used by client components, but this does
not turn dependency compilation into a security sandbox. Keep the build toolchain
and any additional installed packages trusted.

Run your normal `hugo server --disableFastRender` preview. Editing the Markdown,
JSX or imported resources triggers Hugo rebuilds; no separate MDX watcher or Node
server is required. A syntax error should be fixed before publishing, not worked
around by enabling unsafe HTML. For restrictive site CSPs, allow the generated
local modules and authorize the generated inline import map; sandbox mode also
requires same-site frames. The frame's own policy stays restrictive.
