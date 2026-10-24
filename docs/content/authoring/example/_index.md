---
date: 2026-10-05T22:48:24+08:00
lastmod: 2026-10-24T20:06:00+08:00
title: "A small working example"
params:
  ai_label: generated
---

This page renders a local component, formula and code resource. It does not load a
comment provider, badge, remote image, video or diagram library. Its adjacent source
is a downloadable resource, never an executable build step.

## A useful disclosure

{{% folding title="Keep the explanation close" open=true %}}
A native disclosure keeps ordinary **Markdown** and source links intact. Read the
[composition guide](../components.md), then choose the smallest component you need.

{{< mark text="Local and safe" color="green" >}}
{{% /folding %}}

## A small formula

The sum of the first $n$ positive integers is $n(n+1)/2$.
Math is rendered at build time and styled with local KaTeX resources.

## Local code

{{< snippet src="sum.py" lang="python" title="A simple sum" >}}

The original file remains available through its native download. Read
[resource boundaries](../snippets.md) before including source of your own.

## A few inline details

{{< icon name="star" color="yellow" label="A useful detail" >}}
{{< hashtag text="Local source" color="cyan" >}}
A {{< tip text="The original attachment stays available without JavaScript." >}}downloadable **example**{{< /tip >}}
can be explained with {{< code-inline lang="python" >}}sum(range(1, n + 1)){{< /code-inline >}}.

{{< download src="sum.py" text="Download the Python example" >}}

{{% tabs label="Example explanations" %}}
{{< tab title="Formula" >}}
Use $n(n+1)/2$ to add the first $n$ positive integers.
{{< /tab >}}
{{< tab title="Notation" >}}
x{{< sup text="2" >}} and H{{< sub text="2" >}}O keep the surrounding text color.
{{< emp text="Emphasis dots" >}}, {{< wavy text="a wavy underline" >}} and
{{< del text="an old wording" >}} provide distinct decorations.

A fictional answer: {{< blur text="Forty-two" >}} or {{< psw text="Forty-two" >}}.
These are visual effects, not protection for secrets.
{{< /tab >}}
{{% /tabs %}}
