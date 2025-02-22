---
jupyter:
  jupytext:
    cell_markers: 'region,endregion'
    formats: 'ipynb,.pct.py:percent,.lgt.py:light,.spx.py:sphinx,md,Rmd,.pandoc.md:pandoc'
    text_representation:
      extension: '.md'
      format_name: pandoc
      format_version: '2.7.2'
      jupytext_version: '1.1.0'
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
  nbformat: 4
  nbformat_minor: 2
---

::: {.cell .markdown}
This is a
plain-text notebook.
:::

::: {.cell .markdown}
The format of the notebook is `pandoc`.
:::

::: {.cell .code}
``` {.python}
#|default_exp pandoc.test
```
:::

::: {.cell .code}
``` {.python}
#|export
# This is a code cell
def foo():
    return "bar"
```
:::