---
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
