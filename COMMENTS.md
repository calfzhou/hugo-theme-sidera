# Article comments (Giscus)

Sidera supplies **Giscus only**, off by default. No build-time provider requests,
GitHub token, backend, package install or other provider adapters are needed.

## Enable on the pages you choose

```yaml
# Regular page or children-mode section front matter
params:
  comments: true
```

The showcase sets site `params.comments=true` for all eligible pages; a consuming
site still chooses its own policy. `comments` is a boolean using normal Page/native cascade → applicable preset →
site/language → minimal `false` precedence. `false` is a real opt-out. A section's
ordinary params do not affect descendants: use `cascade.params.comments`, or a
preset's `defaults.cascade.params`. Site `params.comments=true` opts in eligible
pages globally; presets are not capability gates. Native page false wins.

Eligible locations are regular article pages (including standalone pages) and
children-mode section documents, in their **canonical body rendering only**.
Home/recursive lists, terms, archives, generated indexes and later child/list
pagers do not show comments. No comment footer component/shortcode exists: repeated
footer instances cannot duplicate the widget. Order stays body → article footer →
reading navigation → docs children (where present) → comments → `article_end_text`.
Optional authored end text remains last; the showcase no longer adds its old contact
sentence. Disabling the footer does not disable comments.

The TOC footer adds **Join the discussion / 参与讨论** beneath Back to top, linking
natively to `#sidera-comments` only when that output actually contains the comment
slot. It also works on an eligible page without body headings (no empty heading
list is invented), repeated TOCs, icons=false, no-JS and the existing mobile drawer.
Later pagers, disabled and generated views have no dead comment link. The generic
slot owns the reserved `sidera-comments` ID and focusable, accessibly labeled anchor;
there is no duplicate visible Comments heading. Provider partials render inside it. No provider-specific TOC condition or cached render flag is needed.

## Site-owned configuration and prerequisites

The following is a **schema example**, not usable GitHub metadata. Replace all four
identity strings with the values returned by the official [configurator](https://giscus.app/).
Never use a display name in place of a node ID.

```toml
[params]
comment_provider = 'giscus' # default; only built-in implementation

[params.giscus]
repo = 'OWNER/REPOSITORY'
repo_id = 'COPY_REPOSITORY_NODE_ID'
category = 'COPY_CATEGORY_DISPLAY_NAME'
category_id = 'COPY_CATEGORY_NODE_ID'
strict = false            # optional, default false; see identity below
reactions = true          # optional, default true
input_position = 'top'    # optional, top (default) or bottom
```

`giscus` and `comment_provider` belong only in site/language params, not page,
cascade or preset definitions. Unknown options, invalid types, unsafe provider
paths/repository names and malformed node-ID strings diagnose. Empty/missing
identity fields yield a localized **unconfigured** message and **no controller or
provider request**. Syntax validation cannot establish that real IDs match a repo;
that requires read-only verification through GitHub/Giscus. These IDs are public
identifiers, not credentials. Do not put auth tokens in configuration.

Before enabling a live widget:

1. Verify the chosen repository is public and GitHub Discussions is enabled.
2. Verify the **Giscus GitHub App** is installed with access to that repository.
   Repo App installation and a visitor's optional OAuth sign-in are different.
3. Select a real category. Giscus recommends the **Announcements** category type
   (only maintainers and Giscus create discussions); do not select a polls-only
   category. Check the configurator's readiness and generated node IDs.
4. Load read-only if desired. **Do not submit a test comment or reaction**: either
   can create a discussion. Absence of an existing thread is not setup failure.

Installation/permission changes, enabling Discussions and category creation are
remote mutations requiring the owner's explicit approval. Configuration is not
consent for those actions. No theme code activates them.

The showcase's selected repository is documented in its own README/config, not in
this reusable implementation. External setup may still be blocked independently
of passing local tests.

## Stable discussion identity, not a new authoring ID system

Sidera uses Giscus's verified `mapping="specific"` / `term` support. At build time
it takes **the path of Hugo's native Page.Permalink**, applies Giscus's actual
pathname transform (remove leading `/`, remove a terminal file extension; `/`
becomes `index`), and sends that fixed term. For example:

- `/journal/2026/04/14/connect-the-useful-parts/` → `journal/2026/04/14/connect-the-useful-parts/`
- `/preview/zh/notes/a/` → `preview/zh/notes/a/`
- `/notes/a.html` → `notes/a`

Native date/slug/custom URL, language prefixes, URL escaping and baseURL **path**
are retained. Hostname/port, `?kw=`, tracking parameters, appearance settings and
fragments are not part of the term. A normal local `hugo server` using the same
configured base path uses the same term as the static build. A different baseURL
path intentionally changes identity; retain the deployment path when previewing.
Native filename translations with different URLs have separate discussions.

On activation the initializer supplies a `giscus:backlink` meta value from Page.Permalink, so new
thread backlinks do not use search/tracking parameters. A preview backlink can
still point to localhost; **don't post from a preview**. No aliases, historical
threads or real-site URLs are rewritten.

Path-derived terms avoid new front matter and agree with the current real site's
pathname concept. A global content ID would survive URL moves but would require
new authoring/identity policy and reconciliation of old threads; it is **not**
introduced here. P4 must compare actual legacy pathname terms, including suffix/
slash/locale/encoding and discussion hashes, separately from redirects. `strict`
defaults false, like the existing reference. New isolated repositories may choose
true to avoid fuzzy matches; existing discussions need the corresponding SHA-1
in their body before strict matching is enabled. This integration does not edit
those hashes or infer historical compatibility.

## Loading, privacy and honest states

- On an enabled/configured page, the local controller waits until the **comment
  section enters the viewport**, then loads Giscus once. Scrolling or the native
  TOC link both work; a page opened at the comment fragment loads automatically.
  Without IntersectionObserver the fallback loads immediately. There is no manual
  load button, per-visitor consent store, preconnect or separate loading setting.
- Disabled/unconfigured pages make **no Giscus requests**. Normal idle/loading/
  responding/empty states add no visible descriptive paragraphs. Loading is a short
  assistive status; no-JS/local-script failure, unavailable and unconfigured states
  retain concise, honest messages. The separate “Browse discussions on GitHub” link
  is removed; the third-party iframe's own links and controls remain provider-owned.
- The official `https://giscus.app/client.js` owns its iframe, default stylesheet,
  GitHub auth/session storage and provider requests. Sidera does not read, log or
  implement auth tokens. This is a live external dependency, not vendored/pinned.
- **Automatic loading contacts Giscus/GitHub** and sends network information and the
  embedding page URL. The official client's origin parameter includes query
  parameters, although they never change the fixed discussion term. Do not put
  secrets in URLs. This provider policy is documented here rather than repeated
  as a paragraph above every widget; site owners choose whether to enable comments.
- HTTP policy is unchanged: document strict-origin, injected script no-referrer,
  discovered iframe no-referrer for subsequent navigation. The first iframe request
  is initiated by the provider before observation and follows document policy;
  this does not hide its explicit URL parameter. Styling uses the supported theme
  API below, never cross-origin DOM access.
- The connection deadline starts **on viewport activation**, not while the section
  is offscreen. Script failure, provider error or 15-second timeout yields a visible
  unavailable message with page-reload recovery. No endless spinner or auto retries.
- Script insertion/load is not proof of provider success. A source/origin-checked
  resize only marks responding internally; an explicit Discussion-not-found message
  marks empty. Both stay visually quiet, letting the widget speak for itself. An
  error is not erased by later resize events. No thread is created without a reader
  submitting a comment/reaction; tests must not do that.

Both `en` and `zh-CN` provider values are verified. Sidera selects zh-CN for a Chinese
native locale, otherwise en; theme chrome uses native Hugo EN/ZH translations.
Provider language changes require navigation/reload. The two fixed theme styles below
match Sidera's resolved light/dark palette, including live OS changes in Auto. The documented `setConfig`
message updates the existing iframe instead of recreating it. Messages handled by
Sidera check **both** exact origin and that iframe's contentWindow; upstream's own
client listeners remain provider-owned. Repeated local initialization/viewport entries are
bounded to one activation per document. Standard navigation discards the instance;
BFCache preserves it. Arbitrary SPA/hot-swapped DOM is not a supported new router.

If a CSP is supplied by the consuming site, it must separately allow the provider's
script/frame/style/auth resources. Sidera does not weaken CSP or bypass blockers.
A native Hugo preview open before the new partial/controller was added may require
one cold restart for template lookup. No cache deletion or user-server manipulation.

## Simple Sidera styling

The fixed `assets/css/giscus.css` asset matches **Sidera's baseline UI font stack and
light/dark colors**: normal/muted text, page/input/panel backgrounds, borders, links
and button accents. Giscus retains its own layout, sizing, controls, Markdown/code
syntax and semantic error/success colors. No selector-heavy redesign, hosted fonts,
font downloads, custom-theme settings or runtime CSS-token synchronization.

Hugo renders/minifies the same small asset twice, with the literal `light` and `dark`
inputs. `comments/themes.html` returns two fixed CSS **data URLs**, supplied through
Giscus's supported `theme` / `setConfig` API. Each stylesheet imports the matching
built-in `https://giscus.app/themes/light.css` or `dark.css`, then overrides only the
font and palette tokens. The imported base keeps all provider defaults and controls
intact; it is served by Giscus, not copied into Sidera. Giscus's current custom-theme
URL resolver/stylesheet loader and read-only live rendering were verified for this
mechanism. No iframe DOM access, inline script, user-authored URL or new backend.

This avoids separate site CSS hosting/CORS setup, including in normal local previews.
Each encoded style is under 2 KiB; only configured widgets carry it. No visitor/page
content or credentials are included. The same iframe adopts palette changes. The
provider loads its ordinary base CSS on activation, not before the section is visible.

The font stack uses locally installed fonts and ordinary system fallbacks, like the
site. This matches the current Sidera baseline, **not arbitrary future site CSS
customizations automatically**. A trusted consuming site can override the native asset
or provider partial later. Keep larger customization/hosted-font needs separate.
Provider CSS/CSP changes can affect custom themes; no all-browser/CSP guarantee or
permission relaxation is implied. A preview open before the new asset/partial was
added may need one cold restart; the owned preview verified same-cache recovery,
without clearing user caches.

Provider references inspected for styling:
[creating themes](https://github.com/giscus/giscus/blob/main/CONTRIBUTING.md#creating-new-themes),
[custom theme variables](https://github.com/giscus/giscus/blob/main/styles/themes/custom_example.css),
[URL resolution](https://github.com/giscus/giscus/blob/main/lib/utils.ts),
[stylesheet loading](https://github.com/giscus/giscus/blob/main/lib/hooks.ts).

## The small native extension seam

`comments/render.html` receives `{Page, Owner, Settings}`, performs placement
eligibility, owns the accessible anchor wrapper and dispatches to `comments/providers/<comment_provider>.html` with
`Config` added (`Provider`, `Giscus`). The name is a validated lowercase slug and
the partial must exist; it is **not an arbitrary path or executable config value**.
Override either partial in the consuming site's `layouts/_partials/` normally.
A future provider can supply one named partial and its own narrow site config/
validation without modifying article templates. Only Giscus ships today. No registry,
SDK abstraction, service manager, unused adapter, or option advertised without a
consumer. Site overrides are trusted native Hugo code and own their safety/lifecycle.

Authoritative provider references inspected for this slice:
[configurator](https://giscus.app/),
[advanced usage/messages/strict/backlink](https://github.com/giscus/giscus/blob/main/ADVANCED-USAGE.md),
[official client mapping/lifecycle](https://github.com/giscus/giscus/blob/main/client.ts).
