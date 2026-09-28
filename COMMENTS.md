# Article comments (Giscus)

Sidera supplies **Giscus only**, off by default. No build-time provider requests,
GitHub token, backend, package install or other provider adapters are needed.

## Enable on the pages you choose

```yaml
# Regular page or children-mode section front matter
params:
  comments: true
```

`comments` is a boolean using normal Page/native cascade → applicable preset →
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
The last authored text remains last; disabling the footer does not disable comments.

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

- Explicit per-document **Load comments** activation, not automatic viewport
  fetching, persistent consent storage, preconnect, or a consent framework.
  Until clicked, configured pages load only the small local controller. Disabled
  and unconfigured pages load neither controller nor Giscus.
- After activation, the official `https://giscus.app/client.js` owns the widget,
  default stylesheet, GitHub authentication/session storage and provider requests.
  Sidera does not read, log, transmit or implement auth tokens. The client is a live
  external dependency, not vendored/pinned or certified by local fixture tests.
- Giscus/GitHub receive network information and the embedding page URL. The official
  client sends its `origin` parameter including **query parameters** (though they
  never change the fixed discussion term). Do not put secrets in URLs; clear a
  sensitive query before loading. The inline notice discloses this connection.
- The document retains `strict-origin`; the injected script and fallback GitHub
  link use no-referrer. The discovered iframe is given no-referrer for subsequent
  navigation, but its first request is initiated by the provider client before
  observation and follows the document policy. This does **not** suppress the
  client's explicit URL parameter. No broad cross-origin CSS or DOM access.
- No JS/local-controller failure: native GitHub link and localized explanation,
  hidden inert load button. Unconfigured: localized explanation only. Pending:
  bounded 15-second connection state. Script failure, provider error or deadline:
  honest unavailable/unconfirmed message with GitHub/page-reload recovery.
- Script insertion/load is **not successful provider loading**. An origin- and
  source-checked widget resize only says Giscus is responding, not that GitHub
  fetched a discussion. The frame reports its own availability. Verified provider
  `Discussion not found` means an empty thread, not a test-created discussion.
  Errors are not erased by later resize messages. No endless spinner or automatic
  retries; reload is the deliberate retry, preventing duplicate upstream listeners.

Both `en` and `zh-CN` provider values are verified. Sidera selects zh-CN for a Chinese
native locale, otherwise en; theme chrome uses native Hugo EN/ZH translations.
Provider language changes require navigation/reload. `light` / `dark` match Sidera's
resolved palette, including live OS changes in Auto. The documented `setConfig`
message updates the existing iframe instead of recreating it. Messages handled by
Sidera check **both** exact origin and that iframe's contentWindow; upstream's own
client listeners remain provider-owned. Repeated local initialization/clicks are
bounded to one activation per document. Standard navigation discards the instance;
BFCache preserves it. Arbitrary SPA/hot-swapped DOM is not a supported new router.

If a CSP is supplied by the consuming site, it must separately allow the provider's
script/frame/style/auth resources. Sidera does not weaken CSP or bypass blockers.
A native Hugo preview open before the new partial/controller was added may require
one cold restart for template lookup. No cache deletion or user-server manipulation.

## The small native extension seam

`comments/render.html` receives `{Page, Owner, Settings}`, performs placement
eligibility and dispatches to `comments/providers/<comment_provider>.html` with
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
