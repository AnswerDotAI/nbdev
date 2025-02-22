---
jupytext:
  formats: ipynb,.pct.py:percent,.lgt.py:light,.spx.py:sphinx,md,Rmd,.pandoc.md:pandoc,.myst.md:myst
  text_representation:
    extension: '.md'
    format_name: myst
    format_version: '0.7'
    jupytext_version: 1.4.0+dev
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

This is a
plain-text notebook.

The format of the notebook is `myst`.

```{code-cell} ipython3
#|default_exp myst.test
```

```{code-cell} ipython3
#|export
# This is a code cell
def foo():
    return "bar"
```