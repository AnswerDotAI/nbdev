# Qmd Documents


*Qmd documents* are [Markdown]() documents, but with loads of extra
functionality provided by [Quarto](https://quarto.org/) and
[Pandoc](https://pandoc.org/). nbdev uses Quarto to render its pages
(with some extra functionality), and Quarto uses Pandoc to render its
pages (with some extra functionality). Every markdown cell in an nbdev
notebook is treated as qmd, and nbdev can publish plain qmd text files,
and qmd [RenderScripts](../tutorials/renderscript.html). Therefore, it’s
a good idea to be familiar with the main features of qmd.

Just like with RenderScripts, you can use hot/live reloading with plain
qmd text files – so as soon as you save the file, you’ll see the new
output in your web browser (assuming you’ve got `nbdev_preview`
running).

## Computations

You can generate data-driven documents using qmd files. For instance,
consider this table (also shown in the RenderScript tutorial for
comparison), containing a list of the people with testimonials on
nbdev’s home page:

<table>
<colgroup>
<col style="width: 12%" />
<col style="width: 37%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th></th>
<th>Name</th>
<th>Position</th>
</tr>
</thead>
<tbody>
<tr>
<td><img src="../images/chris-lattner.png" style="width:60.0%" /></td>
<td>Chris Lattner</td>
<td>Inventor of Swift and LLVM</td>
</tr>
<tr>
<td><img src="../images/fernando-pérez.jpeg" style="width:60.0%" /></td>
<td>Fernando Pérez</td>
<td>Creator of Jupyter</td>
</tr>
<tr>
<td><img src="../images/david-berg.jpeg" style="width:60.0%" /></td>
<td>David Berg</td>
<td>Software Engineer, Netflix</td>
</tr>
<tr>
<td><img src="../images/erik-gaasedelen.jpeg"
style="width:60.0%" /></td>
<td>Erik Gaasedelen</td>
<td>Software Engineer, Lyft</td>
</tr>
<tr>
<td><img src="../images/roxanna-pourzand.jpeg"
style="width:60.0%" /></td>
<td>Roxanna Pourzand</td>
<td>Product Manager, Transform</td>
</tr>
<tr>
<td><img src="../images/hugo-bowne-anderson.jpeg"
style="width:60.0%" /></td>
<td>Hugo Bowne-Anderson</td>
<td>Head of Developer Relations, Outerbounds</td>
</tr>
</tbody>
</table>

The table above is generated using an embedded [qmd computation
block](https://quarto.org/docs/computations/python.html) from the
following python list:

<div class="column-screen-inset-right">

``` python
testimonials = [
    ('chris-lattner.png', 'Chris Lattner', 'Inventor of Swift and LLVM'),
    ('fernando-pérez.jpeg', 'Fernando Pérez', 'Creator of Jupyter'),
    ('david-berg.jpeg', 'David Berg', 'Software Engineer, Netflix'),
    ('erik-gaasedelen.jpeg', 'Erik Gaasedelen', 'Software Engineer, Lyft'),
    ('roxanna-pourzand.jpeg', 'Roxanna Pourzand', 'Product Manager, Transform'),
    ('hugo-bowne-anderson.jpeg', 'Hugo Bowne-Anderson', 'Head of Developer Relations, Outerbounds')
]
```

</div>

Just like in the RenderScript example, to produce the table from this
python list, the following four lines of code are used:

``` python
print(qmd.tbl_row(['','Name','Position']))
print(qmd.tbl_sep([1,3,4]))
for fname,name,position in testimonials:
    print(qmd.tbl_row([im(fname, 60), name, position]))
```

For data-driven documents such as this one, we add the following to the
YAML frontmatter, which hides the code used to produce outputs, and also
does not add any extra formatting to outputs:

    ---
    execute:
      echo: false
      output: asis
    ---

Compare the source code of the RenderScript example and of the current
page to see how computations are used in RenderScripts compared to plain
qmd text files. We find that we like to use Notebooks for most pages we
build, since they’ve got so much helpful functionality (such as pasting
images directly into cells). We use RenderScripts for complex web pages
like the nbdev home page, and qmd files for pages that are mainly
markdown and don’t need any notebook functionality.

## Formatting

In addition to the [standard markdown
formatting](https://quarto.org/docs/authoring/markdown-basics.html),
Quarto qmd adds many additional features. Look at the full quarto docs
to see everything it can do – we’ll just highlight a few of our
favorites here.

### Divs and classes

You can create HTML
[divs](https://quarto.org/docs/authoring/markdown-basics.html#divs-and-spans),
by surrounding lines with `:::`. Divs can include classes by placing
`{.classname}` after the opening `:::`. Here’s an example:

``` markdown
::: {.border}
This content can be styled with a border
:::
```

This is how that’s rendered:

<div class="border">

This content can be styled with a border

</div>

You might be wondering where that `border` class comes from… Quarto
comes with support for [Bootstrap 5 and Bootswatch
themes](https://quarto.org/docs/output-formats/html-themes.html) so
there’s lots of classes available you can use in your documents.
Remember, all notebook markdown cells are also considered qmd, and can
also use all the formatting tricks discussed in this section.

### Callouts

A special kind of block you can use is the [callout
block](https://quarto.org/docs/authoring/callouts.html). Here’s an
example:

``` markdown
:::{.callout-note}
Note that there are five types of callouts, including:
`note`, `warning`, `important`, `tip`, and `caution`.
:::
```

…and here’s how it’s rendered:

<div>

> **Note**
>
> Note that there are five types of callouts, including: `note`,
> `warning`, `important`, `tip`, and `caution`.

</div>

### Images

You can add images (quarto calls them
[figures](https://quarto.org/docs/authoring/figures.html) to your
document, along with captions, and you can even arrange them into
layouts. Here’s an example:

``` markdown
::: {layout-ncol=3}
![Jupyter](/images/jupyter.svg)

![Vscode](/images/vscode.svg)

![Git](/images/git.svg)
:::
```

<div>

</div>
