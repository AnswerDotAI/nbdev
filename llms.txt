# nbdev

nbdev makes exploration an integral part of your workflow, all while promoting software engineering best practices. It allows you to write, test, document, and distribute software packages and technical articles — all in one place, your notebook.

Here are some of nbdev's features:

- **Supports literate programming**: write prose, code, and tests in notebooks — no context-switching
- **Git-friendly notebooks**: human-readable merge conflicts; no unwanted metadata
- **Two-way sync between notebooks and plaintext source code**: allows you to use your IDE for code navigation or quick edits
- **Beautiful technical documentation**: documentation is automatically generated using Quarto and hosted on GitHub Pages; docs support LaTeX, are searchable, and are automatically hyperlinked (including out-of-the-box support for many packages via nbdev-index)
- **Seamless testing**: write tests as ordinary notebook cells, run them in parallel with a single command; out-of-the-box continuous integration with GitHub Actions to ensure tests pass before every merge
- **Simplified package release**: publish packages to PyPI and conda; Python best practices are automatically followed (e.g. only exported objects are included in `__all__`)

## Tutorials

- [Getting started](https://nbdev.fast.ai/getting_started.html.md)
- [Tutorial](https://nbdev.fast.ai/tutorials/tutorial.html.md)
- [Best practices](https://nbdev.fast.ai/tutorials/best_practices.html.md)

## API

- [API List](https://nbdev.fast.ai/apilist.txt): A succint list of all functions and methods in nbdev.

## Optional

- [Git-Friendly Jupyter](https://nbdev.fast.ai/tutorials/git_friendly_jupyter.html.md): How to use nbdev hooks for git-friendly Jupyter notebooks
- [Blogging](https://nbdev.fast.ai/tutorials/blogging.html.md: Creating a blog with notebooks)
- [Pre-Commit Hooks](https://nbdev.fast.ai/tutorials/pre_commit.html.md): How to use nbdev’s git pre-commit hooks
- [Documentation Only Sites](https://nbdev.fast.ai/tutorials/docs_only.html.md): How to create nbdev powered docs without a library!
- [Modular nbdev](https://nbdev.fast.ai/tutorials/modular_nbdev.html.md): How to use nbdev’s various tools separately
- [Writing nbdev plugins](https://nbdev.fast.ai/tutorials/extensions.html.md): How to customize nbdev processors to do what you want
- [nbdev1 Migration](https://nbdev.fast.ai/tutorials/migrating.html.md): How to change your nbdev1 repo to work with nbdev2
- [nbdev.config](https://nbdev.fast.ai/api/config.html.md): Configuring nbdev and bootstrapping notebook export
- [nbdev.maker](https://nbdev.fast.ai/api/maker.html.md): Create one or more modules from selected notebook cells
- [nbdev.process](https://nbdev.fast.ai/api/process.html.md): A notebook processor
- [nbdev.export](https://nbdev.fast.ai/api/export.html.md): Exporting a notebook to a library
- [nbdev.doclinks](https://nbdev.fast.ai/api/doclinks.html.md): Generating a documentation index from a module
- [nbdev.sync](https://nbdev.fast.ai/api/sync.html.md): Propagate small changes in the library back to notebooks
- [nbdev.merge](https://nbdev.fast.ai/api/merge.html.md): Fix merge conflicts in jupyter notebooks
- [nbdev.showdoc](https://nbdev.fast.ai/api/showdoc.html.md): Display symbol documentation in notebook and website
- [nbdev.frontmatter](https://nbdev.fast.ai/api/frontmatter.html.md): A YAML and formatted-markdown frontmatter processor
- [nbdev.processor](https://nbdev.fast.ai/api/processors.html.md): Some processors for NBProcessor
- [nbdev.clean](https://nbdev.fast.ai/api/clean.html.md): Strip superfluous metadata from notebooks
- [nbdev.test](https://nbdev.fast.ai/api/test.html.md): Run unit tests on notebooks in parallel
- [nbdev.cli](https://nbdev.fast.ai/api/cli.html.md): CLI commands
- [nbdev.quarto](https://nbdev.fast.ai/api/quarto.html.md): Install and interact with Quarto from nbdev
- [nbdev.qmd](https://nbdev.fast.ai/api/qmd.html.md): Basic qmd generation helpers (experimental)
- [nbdev.migrate](https://nbdev.fast.ai/api/migrate.html.md): Utilities for migrating to nbdev
- [nbdev.serve](https://nbdev.fast.ai/api/serve.html.md): A parallel ipynb processor (experimental)
- [nbdev.release](https://nbdev.fast.ai/api/release.html.md): Auto-generated tagged releases and release notes from GitHub issues