r"""Build nbdev documentation with Octavo

Octavo is an alternative to Quarto for building a documentation website from nbdev notebooks. Install `nbdev[octavo]` to use it. A project selects Octavo by placing `octavo.yml` in its configured notebooks directory. Projects without that file continue to use Quarto and do not import Octavo.

The usual `nbdev-docs` command builds the site. Octavo currently builds all pages together. File-selection options are rejected unless left at their defaults; `n_workers` affects only Quarto builds.

Run `nbdev-export` before building to update the generated Python modules and symbol indexes. `nbdev-readme` and `nbdev-contributing` also use Octavo for these projects. `nbdev-prepare` still exports, tests, and cleans notebooks, but skips Quarto configuration generation.

For an existing Quarto project, `nbdev-migrate-octavo` converts documentation sources in place. The converted sources are not intended to work unchanged with both builders. Use `nbdev-preview` to serve the site and rebuild after edits. Refresh the browser manually.

## Migration instructions (share this with your AI)

Octavo builds into the same output directory as Quarto and replaces what's there. The migration also converts the sources in place, and they won't build with Quarto afterwards, even if you keep `_quarto.yml`. So save the Quarto site first:

1. Commit or back up the project.
2. From the project root, run `nbdev-docs` while the project still uses Quarto. Check that the build works, and note any failures it already has, so you don't mistake them for migration problems later.
3. Copy the whole built site, including assets and search files, to a directory outside the project's source and output directories. This copy is the baseline you compare against.
4. Run `nbdev-migrate-octavo` from the project root. Read its changes and everything it prints: it reports the settings it couldn't carry over.
5. Run `nbdev-docs` again to build with Octavo. If the build fails, keep its output for diagnosis.

`nbdev-migrate-octavo` renames `.qmd` sources to `.md`, updates references to them, converts directives, and moves a page's `subtitle` to `description`. Octavo reads Quarto's other front matter and settings names as they are. The migration writes `octavo.yml` from `_quarto.yml` and `nbdev.yml`, and leaves an existing `octavo.yml` alone. It doesn't port the site's design. It leaves stylesheet files unchanged, and it doesn't add the stylesheets listed under `format.html.css` in `_quarto.yml` to `octavo.yml`. Stylesheets that a page lists in its own front matter still load.

Read the original `_quarto.yml`, `nbdev.yml` and `pyproject.toml`, and the new `octavo.yml`. Go through the checks below that apply to the project, skipping features it doesn't use, and propose a short migration plan. Ask me before accepting anything that loses behavior.

- **Styles and custom pages.** Octavo's HTML has no Bootstrap or Quarto classes. Look at the rendered Octavo HTML before reusing old CSS, and copy over only the rules that still apply. Don't enable an old stylesheet wholesale or add a compatibility layer. Check narrow screens too.
- **Wide content.** Octavo has no equivalent of Quarto's `page-layout: full` or column classes such as `.column-page` and `.column-screen-inset-right`. Widen those pages with your own CSS, in a stylesheet listed in the page's `css` front matter.
- **Layouts and tables of contents.** Octavo reads Quarto's `page-layout`, `toc` and `toc-depth` with the same meanings, but of the `page-layout` values it supports only `custom`, for a hand-built page. Check pages that used `article` or `full`, and compare tables of contents with the baseline on ordinary pages as well as custom ones.
- **Sidebar.** If the project has a hand-written `sidebar.yml` (`custom_sidebar` in `pyproject.toml`), the migration turns it into `sidebar-links` in `octavo.yml`. Compare its sections and order with the baseline. Add the pages behind any entries it reported as dropped, such as `auto` or globs, as explicit links.
- **Scripts.** The migration doesn't carry over scripts that Quarto added through `include-in-header`, `include-after-body` or raw HTML. Load them with Octavo's `js` setting, in `octavo.yml` for the whole site or in a page's front matter. Octavo loads them as module scripts (`<script type="module">`).
- **Maths.** The migration sets `math: dollars`, Quarto's `$...$` syntax. Check the pages with maths. A literal dollar sign in a paragraph that also has maths needs escaping as `\$`.
- **Conditional and embedded content.** Compare `when-format` and `unless-format` blocks with the originals, in both the HTML and the Markdown output. The conversion doesn't always keep exclusion conditions, and Markdown inside an HTML-only block isn't rendered. Where needed, turn HTML-only content into a raw `{=html}` block. Check each result rather than rewriting every block by pattern.
- **`{python}` blocks.** Octavo runs the `{python}` blocks in `.md` files on every build, and the page shows only their output, not the code. Quarto also showed the code. Compare pages that have these blocks with the baseline. If the project set `execute: enabled: false` in `_quarto.yml`, the blocks didn't run under Quarto at all.
- **Shortcodes.** Octavo doesn't support Quarto shortcodes such as `{{< include file.md >}}` or `{{< video url >}}`. They appear as literal text. Search the sources for `{{<` and report each use.
- **Render scripts and processors.** If the project has render scripts (such as `page.md.py` or `drawing.svg.py`) or custom nbdev processors, check the content and assets they produce.
- **Code that finds docs by name.** Search the whole project for `.qmd`, including build scripts, tests, generators and contributor docs, and update paths, globs and extension checks. A glob that matches nothing fails silently. Run the full test suite, not only `nbdev-docs`, and check that tests that read doc pages still find them. Regenerate saved notebook outputs that contain `.qmd` links.
- **Published files.** Quarto published only linked files and declared resources. Octavo publishes every visible file in the notebooks directory (no part of its path starts with `.` or `_`), as a page or as a copied file. Compare the output file list with the baseline. To keep stray files such as READMEs or notes out, add glob patterns to `exclude` in `octavo.yml`. Patterns are relative to the notebooks directory, and a pattern that matches a directory excludes everything in it. Don't exclude Quarto-only files: they're deleted at the end.
- **Navigation and URLs.** Check navbar links, dropdowns, icons, favicon, footer and existing public URLs. Restore icons the migration dropped, and keep the existing footer. Markdown copies of notebook pages move from `page.html.md` to `page.md`, and Octavo doesn't redirect the old addresses. Report this rather than working around it.
- **Settings that weren't carried over.** List the site and page settings the migration reported as having no Octavo equivalent, and any theme options and preview preferences. Octavo uses a page's `image` front matter as its link preview image when `site-url` is set, and a page can set its own `open-graph` or `twitter-card` options. It doesn't pick a preview image from the page content, so list the pages that relied on that. For each setting, propose a replacement or say it's dropped. Quarto's repo-actions links, such as "Report an issue", are dropped on purpose: don't list them.
- **Build hooks.** If the project has custom build hooks, keep the outputs they produce with nbdev's `docs_post_build` setting, and check the links in any indexes they generate.
- **Output directory.** A relative `output` in `octavo.yml` is relative to the notebooks directory. Without it, nbdev uses `doc_path`, which is relative to the project. Check that this is the directory the deployment workflow publishes.

Once I've approved the plan, make the changes in small steps, running `nbdev-export` before each build. Then:

- run `nbdev-docs` and the project's other Markdown commands, such as `nbdev-readme`;
- compare the HTML, Markdown, assets and other build outputs with the baseline, and check a few API signatures, symbol links and GitHub source links;
- sort the differences into failures the baseline already had, expected changes, and regressions.

A clean build doesn't show that the site works in a browser. Serve the baseline and the new site separately, and check that each server points at the directory you meant. Serve the new site under its real subpath, such as `/project/`, not only at `/`. Then, on a few representative pages at desktop and phone widths, test:

- navigation in the menu's
- anchors and images;
- search, following results from the homepage and from a nested page;
- the optional features you found in the checks above.

Report what you changed, which checks you actually ran, the differences you couldn't resolve, the settings that weren't carried over, and the decisions I need to make. Keep the original configuration and the baseline until I've reviewed the migration.

After the review, delete `_quarto.yml`, plus the files it lists under `metadata-files` and `syntax-definitions` that nothing else in the project uses, such as `nbdev.yml` and `sidebar.yml`.

Docs: https://nbdev.fast.ai/api/octavo.html.md"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/20_octavo.ipynb.

# %% auto #0
__all__ = ['NBDEV_KEYS', 'OctavoProc', 'local_libraries', 'render_script', 'script_pages', 'octavo_config', 'octavo_docs',
           'octavo_preview', 'octavo_readme', 'repl_script_frontmatter_keys', 'nbdev_migrate_octavo']

# %% ../nbs/api/20_octavo.ipynb #7b098bb5
from contextlib import redirect_stdout
from io import StringIO
from fastcore.utils import *
from fastcore.script import call_parse
import yaml, shutil, subprocess, threading, webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from octavo import *
from octavo.migrate import *
from mdhtml import md2gfm
from .config import get_config, import_obj, _load_toml
from .doclinks import NbdevLookup
from .process import NBProcessor
from .processors import FilterDefaults, add_links
from .serve import _is_qpy
from .quarto import _doc_mtime_not_older, fs_watchdog

# %% ../nbs/api/20_octavo.ipynb #1cc66460
class OctavoProc(FilterDefaults):
    "Prepare notebook content, metadata, and symbol links for Octavo"
    def __init__(self, local_lib=None, strip_libs=None): self.nl = NbdevLookup(strip_libs=strip_libs or local_lib, local_lib=local_lib)
    def add_links(self, cell): return add_links(cell, nl=self.nl)
    def procs(self): return L(self.add_links if o is add_links else o for o in super().procs())
    def nb_proc(self, nb): return NBProcessor(nb=nb, procs=self.procs(), rm_directives=False)

    def __call__(self, nb):
        super().__call__(nb)
        if getattr(nb, 'frontmatter_', None) and nb.cells[0].cell_type=='raw': nb.cells[0].cell_type = 'markdown'

# %% ../nbs/api/20_octavo.ipynb #9a0258ee
def local_libraries(cfg):
    "Names of the project's declared nbdev symbol indexes"
    proj = _load_toml(cfg.config_file).get('project', {})
    return tuple(proj.get('entry-points', {}).get('nbdev', {}))

# %% ../nbs/api/20_octavo.ipynb #f9f85ebf
def render_script(path):
    "Execute a double-suffix render script and return its printed output with optional page metadata"
    path = Path(path)
    if path.suffix!='.py' or len(path.suffixes)<2: return
    fm = _is_qpy(path) if path.name.endswith('.md.py') else None
    f = StringIO()
    with redirect_stdout(f): exec(compile(path.read_text(encoding='utf-8'), str(path), 'exec'), {})
    return (f'---\n{fm}\n---\n\n' if fm else '') + f.getvalue()

# %% ../nbs/api/20_octavo.ipynb #e85c51f3
def script_pages(root,         # Documentation directory
                 exclude=None): # Glob patterns of paths to skip, as in Octavo's `exclude` setting
    "Render scripts under `root`: `*.md.py` as `Page`s, anything else as `GeneratedFile`s"
    root,pages,files = Path(root),L(),L()
    for rel in source_files(root, exclude).map(Path).filter(lambda o: o.suffix=='.py'):
        if (txt:=render_script(root/rel)) is None: continue
        dest = rel.with_suffix('')
        if dest.suffix=='.md': pages.append(Page(str(rel), txt, nm=page_nm(dest)))
        else: files.append(GeneratedFile(str(rel), str(dest), txt))
    return pages,files

# %% ../nbs/api/20_octavo.ipynb #d6904375
def octavo_config(root):
    "Settings from `octavo.yml`, as Octavo's `read_cfg` reads them; the file must exist"
    if not (p := Path(root)/CFG_FILE).is_file(): raise FileNotFoundError(p)
    return read_cfg(root)

# %% ../nbs/api/20_octavo.ipynb #f6830357
def octavo_docs(
    path:str=None, # Path to the project or its notebooks
):
    "Create Octavo docs and run the optional docs_post_build callback"
    cfg = get_config(path)
    settings = {'output': cfg.doc_path, **octavo_config(cfg.nbs_path)}
    with working_directory(cfg.config_path):
        pages,files = script_pages(cfg.nbs_path, settings.get('exclude'))
        docs = scan(cfg.nbs_path, nbproc=OctavoProc(local_lib=local_libraries(cfg)), exclude=settings.get('exclude')) + pages
        site = Site(docs, root=cfg.nbs_path, files=files, **settings)
        if (miss := site.build()): print(miss)
        if (post := cfg.get('docs_post_build')):
            out = Path(site.settings['output']).expanduser()
            if not out.is_absolute(): out = cfg.nbs_path/out
            import_obj(post)(out.resolve(), cfg)

# %% ../nbs/api/20_octavo.ipynb #db88c5c9
def octavo_preview(
    path:str=None, # Path to the project or its notebooks
    port:int=None, # HTTP port (defaults to 8000)
    host:str=None, # Bind address (defaults to localhost)
    no_browser:bool=False, # Do not open a browser
):
    "Serve documentation and rebuild when project files change"
    cfg = get_config(path)
    root = cfg.config_path.resolve()
    settings = octavo_config(cfg.nbs_path)
    out = (cfg.nbs_path/Path(settings.get('output', cfg.doc_path)).expanduser()).resolve()
    if root.is_relative_to(out) or cfg.nbs_path.resolve().is_relative_to(out): raise ValueError('Output must not contain sources')
    changed = threading.Event()

    def rebuild():
        try: subprocess.run(['nbdev-docs', '--path', str(root)], cwd=root, check=True)
        except subprocess.CalledProcessError:
            shutil.rmtree(out, ignore_errors=True)
            out.mkdir(parents=True, exist_ok=True)
            (out/'index.html').write_text('<h1>Build failed - see terminal</h1>')
            print('Build failed; waiting for another edit.', flush=True)

    def on_change(event):
        if event.event_type not in ('created', 'modified', 'deleted', 'moved'): return
        if event.is_directory and event.event_type=='modified': return
        for name in (event.src_path, getattr(event, 'dest_path', '')):
            if not name: continue
            src = Path(name).resolve()
            if src.is_relative_to(out) or not src.is_relative_to(root): continue
            if any(p.startswith('.') or p=='__pycache__' for p in src.relative_to(root).parts): continue
            changed.set()

    handler = partial(SimpleHTTPRequestHandler, directory=str(out))
    with ThreadingHTTPServer((host or 'localhost', 8000 if port is None else port), handler) as server:
        url = f'http://{host or "localhost"}:{server.server_port}'
        with fs_watchdog(on_change, root):
            rebuild()
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                print(f'{url} - refresh your browser after rebuilding', flush=True)
                if not no_browser: webbrowser.open(url)
                while True:
                    changed.wait()
                    changed.clear()
                    while changed.wait(0.2): changed.clear()
                    rebuild()
            finally: server.shutdown()

# %% ../nbs/api/20_octavo.ipynb #0d38402b
def octavo_readme(
    path:str=None, # Path to the project or its notebooks
    chk_time:bool=False, # Only build if the source is newer
    contributing:bool=False, # Render CONTRIBUTING instead of README
):
    "Render a repository Markdown document from a notebook's stored outputs"
    cfg = get_config(path)
    nbname = cfg.get('contributing_nb', 'contributing.ipynb') if contributing else cfg.readme_nb
    root = Path(path).absolute() if path else cfg.nbs_path
    src = root/nbname
    if not src.exists(): src = cfg.nbs_path/nbname
    if not src.exists(): return
    name = 'CONTRIBUTING' if contributing else 'README'
    dest = cfg.config_path/f'{name}.md'
    if chk_time and _doc_mtime_not_older(dest, src): return
    octavo_config(cfg.nbs_path)
    with working_directory(cfg.config_path):
        proc = OctavoProc(strip_libs=local_libraries(cfg))
        doc = md2doc(ipynb2md(src, nbproc=proc))
        head = f'# {doc.meta["title"]}\n\n' if doc.meta.get('title') else ''
        if desc:=doc.meta.get('description'): head += f'{desc}\n\n'
        md2gfm(head + doc.body, dest=dest, imgdir=cfg.config_path/f'{src.stem}_files', raw=('md', 'html'))

# %% ../nbs/api/20_octavo.ipynb #deb7ee06
def _quarto_config(nbs_path): return read_quarto_config(nbs_path/'_quarto.yml'),read_quarto_config(nbs_path/'nbdev.yml')

# %% ../nbs/api/20_octavo.ipynb #127739bd
def _octavo_output(nbs_path, qy, ny):
    "Return a Quarto output override relative to notebooks, or None when doc_path suffices"
    out_dir = (ny.get('project', {}) or {}).get('output-dir') or (qy.get('project', {}) or {}).get('output-dir')
    if not out_dir: return
    cfg = get_config(nbs_path)
    out_dir = (cfg.config_path/Path(out_dir).expanduser()).resolve()
    if out_dir == cfg.doc_path.resolve(): return
    return os.path.relpath(out_dir, Path(nbs_path).resolve()).replace(os.sep, '/')

# %% ../nbs/api/20_octavo.ipynb #e0912069
def _octavo_sidebar(nbs_path):
    "Convert the project's custom sidebar when enabled"
    p = Path(nbs_path)/'sidebar.yml'
    if not get_config(nbs_path).custom_sidebar or not p.exists(): return {}
    sb = nested_idx(yaml.safe_load(p.read_text()) or {}, 'website', 'sidebar') or {}
    return quarto_sidebar(sb, p)

# %% ../nbs/api/20_octavo.ipynb #2f2d4b3b
def _create_octavo_cfg(nbs_path):
    "Convert Quarto settings with nbdev's overlay, output path and custom sidebar"
    nbs_path = Path(nbs_path).resolve()
    qy,ny = _quarto_config(nbs_path)
    output = _octavo_output(nbs_path, qy, ny)
    cfg = quarto_config(qy, nbs_path, overrides=ny) | _octavo_sidebar(nbs_path)
    if output is not None: cfg['output'] = output
    return cfg

# %% ../nbs/api/20_octavo.ipynb #5927e211
_script_fm = re.compile(r'\A(?P<q>"{3}|\'{3})---\n(?P<fm>.*?)\n---(?P=q)', re.DOTALL)

def _script_md(m):
    "Frontmatter block from a `_script_fm` match on a render script"
    return f"---\n{m.group('fm')}\n---\n"

def repl_script_frontmatter_keys(s):
    "Normalize a render script's leading YAML docstring for Octavo"
    if not (m := _script_fm.match(s)): return s
    old = _script_md(m)
    new = repl_frontmatter_keys(old)
    if new == old: return s
    return m.group('q') + new.rstrip('\n') + m.group('q') + s[m.end():]

# %% ../nbs/api/20_octavo.ipynb #c4b4478c
NBDEV_KEYS = {'skip_exec', 'skip_showdoc'}

def _migrate_octavo(path):
    "Migrate documents and nbdev render scripts using the project's configuration"
    path = Path(path).expanduser()
    scripts = source_files(path).map(lambda o: path/o).filter(lambda p: p.name.endswith('.qmd.py'))
    script_moves = {p:p.with_name(p.name.removesuffix('.qmd.py')+'.md.py') for p in scripts}
    moves = migrate_quarto(path, config=_create_octavo_cfg, extra_keys=NBDEV_KEYS, extra_moves=script_moves)
    for p in script_moves.values():
        migrate_md_file(p, [repl_script_frontmatter_keys])
        if m := _script_fm.match(p.read_text()):
            report_page_keys(p, extra_keys=NBDEV_KEYS, metadata=frontmatter(_script_md(m))[0])
    return moves

# %% ../nbs/api/20_octavo.ipynb #e332ece4
@call_parse
def nbdev_migrate_octavo(
    path:str=None, # Documentation directory (defaults to configured nbs_path)
):
    "Migrate Quarto-era nbdev project to Octavo"
    moves = _migrate_octavo(get_config().nbs_path if path is None else path)
    for old,new in moves.items(): print(f'{old} -> {new}')
