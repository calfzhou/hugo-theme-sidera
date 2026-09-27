# Native MP4 video

Use Hugo 0.166.0 with standard `<` notation, on its own line:

```text
{{< video src="clip.mp4" width=480 title="A short demonstration" >}}
{{< video src="https://example.org/clip.mp4" width=480 title="Remote demonstration" >}}
```

A small local controller enables **native HTML video controls**. No third-party
player, hosted iframe, autoplay, preview-metadata fetch or build-time download.
The reader chooses **Load video**, which attaches the source and requests media,
then uses the browser's play control. Loading never calls play().

## Supported arguments

| Name | Contract |
|---|---|
| src | Required string: exact current-page `.mp4` resource key, or an explicit HTTP(S) MP4 URL with no credentials. Remote query parameters are permitted. |
| width | Optional positive integer, 1–8192 CSS pixels (numeric or decimal string); maximum frame width, not forced intrinsic dimensions. Omitted: available width. No `px`/percent/style expressions. |
| title | Optional nonblank plain-text string, escaped, used for caption and accessible player name. Default: localized Video. No HTML/Markdown rendering. |
| disabled | Optional boolean, false by default. True omits the player and activation control while retaining the file link and explanation. Not a privacy/redaction mechanism. |

Unknown/invalid options and missing local files fail with source position. No loop,
autoplay, provider-specific options, inline HTML, arbitrary code or generic embed API.
MP4 is a container: browser codec compatibility and server delivery are still required.
Serve video/mp4 with a known content length and byte-range support for native seeking.
The sample uses silent H.264/yuv420p; other codecs/browsers are not certified. For
meaningful audio, provide appropriate captions/transcripts; this bounded component
has no text-track authoring API yet. A title is not a substitute for a transcript.

## Resource and network policy

Local keys have no absolute/dot/parent paths, backslashes, percent-encoding, glob,
query/fragment or scheme. Literal spaces and Unicode are accepted. Lookup is only
`.Page.Resources.Get`, never `os.ReadFile`, shared/static fallback or A's page resolver.
Native `.RelPermalink` preserves dates, base paths, languages and opt-in docs mounts.
Hugo's normal symlink exclusion applies; trusted site mounts are not an OS sandbox.
Resources may be published by Hugo independently of whether playback is disabled.
The ordinary file link preserves full original bytes; it does not force a download.

HTTP(S) media is **not contacted at build time or on initial page load**. The reader's
activation contacts the authored host; that host sees the reader's IP and may receive
a referrer according to the site's/browser's policy. Native video has no portable
per-element referrer-policy guarantee. The fallback anchor uses `rel=noreferrer`.
No remote poster, tracking SDK, service proxy, retry daemon or caching API is added.

The player starts idle, visibly enters loading, and becomes ready only after the
browser has loaded frame data. A media error or a 15-second wait exposes an error
message and file link. No automatic retries or playing; a late successful load can
restore ready controls. Each player is independent. No-JS or unavailable controller
keeps the real file link; **inline playback without JS is not promised**. A disabled
player remains a file link even with scripting. Browser-owned native control labels
follow the browser locale; theme-owned labels/statuses use native EN/ZH i18n.

## Composition and conditional resources

Use the accepted [COMPONENTS.md](COMPONENTS.md) convention: outer containers `%`,
nested video `<`. The normal validated output crosses the existing page-local leaf
bridge; the media file is never rendered as Markdown, executed or re-encoded by Hugo.
Works in block/folding/box/grid cells without changing B's explicit inversion rules.
No automatic palette filter is applied to movie pixels. Deliberately marking an
ancestor with an inversion class still filters the whole group, as with other content.

The shared shell detects the actual rendered video element, including an embedded
Content or Summary, before a deferred script inclusion. Plain pages, disabled-only
pages, code examples and plainified list excerpts do not request the controller.
Custom layouts must use the shared shell (or deliberately supply equivalent asset
handling). Site shortcodes/partials retain native precedence; nested overrides must
preserve the documented leaf bridge. No template rename or user restart is required
by this addition; the earlier C2 restart note only applies to that transition.

Showcase: `/handbook/reference/video/`. The local two-second silent test pattern was
created with the already installed FFmpeg, without acquiring media:

```sh
ffmpeg -f lavfi -i 'testsrc2=size=320x180:rate=12:duration=2' \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart -an motion.mp4
```

This is a video specimen, not Mermaid/drawio/badge completion. Their P3-D work remains.
