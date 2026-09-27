{{- $_hugo_config := `{ "version": 2 }` -}}
{{- /* Emit a native block node, not raw HTML. Goldmark then owns nested Markdown,
     headings/TOC and render hooks. A reserved marker selects div presentation. */ -}}
{{- if and .Params (not .IsNamedParams) -}}{{- errorf "Sidera block accepts named class/id only (%s)" .Position -}}{{- end -}}
{{- range $key, $value := .Params -}}
  {{- if not (in (slice "class" "id") $key) -}}{{- errorf "Sidera block: unsupported parameter %q (%s)" $key $.Position -}}{{- end -}}
  {{- $pattern := `^[A-Za-z_][A-Za-z0-9_-]*(?: [A-Za-z_][A-Za-z0-9_-]*)*$` -}}
  {{- if eq $key "id" -}}{{- $pattern = `^[A-Za-z_][A-Za-z0-9_-]*$` -}}{{- end -}}
  {{- if not (findRE $pattern (string $value)) -}}{{- errorf "Sidera block: invalid %s token(s) (%s)" $key $.Position -}}{{- end -}}
{{- end -}}
{{- with .Parent -}}{{- errorf "Sidera block must be a top-level Markdown shortcode, not nested in another shortcode (%s)" $.Position -}}{{- end -}}
{{- $inner := strings.TrimSpace .Inner -}}
{{- $body := printf "\n\n> %s\n{data-sidera-block=true" (replace $inner "\n" "\n> ") -}}
{{- with .Get "class" -}}{{- $body = printf "%s class=%q" $body . -}}{{- end -}}
{{- with .Get "id" -}}{{- $body = printf "%s id=%q" $body . -}}{{- end -}}
{{- printf "%s}\n\n" $body -}}
