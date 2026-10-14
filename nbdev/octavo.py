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
           'octavo_preview', 'octavo_readme', 'repl_qmd_links', 'repl_html_md_links', 'repl_content_visible',
           'repl_frontmatter_keys', 'repl_script_frontmatter_keys', 'report_page_keys', 'migrate_nb_cells',
           'migrate_md_file', 'nbdev_migrate_octavo']

# %% ../nbs/api/20_octavo.ipynb #7b098bb5
from contextlib import redirect_stdout
from io import StringIO
from fastcore.utils import *
from fastcore.script import call_parse
import yaml, shutil, subprocess, threading, webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from octavo import *
from mdhtml import md2gfm
from .config import get_config, import_obj, _load_toml, read_nb
from .doclinks import NbdevLookup
from .process import NBProcessor
from .processors import FilterDefaults, add_links
from .serve import _is_qpy
from .sync import write_nb
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

# %% ../nbs/api/20_octavo.ipynb #267d0150
def _qmd_moves(path):
    "`.qmd` documents and `.qmd.py` render scripts under `path`, mapped to Octavo names"
    path = Path(path)
    ps = L(path.rglob('*.qmd')) + L(path.rglob('*.qmd.py'))
    return {p:p.with_name(re.sub(r'\.qmd(?=\.py$|$)', '.md', p.name)) for p in sorted(ps)
            if not any(o[0] in '._' for o in p.relative_to(path).parts)}

# %% ../nbs/api/20_octavo.ipynb #a6688f7e
def _qmd_repls(src, path, moves):
    "Old and new spellings of each moved document, as seen from `src`"
    def _rel(p, start): return os.path.relpath(p, start).replace(os.sep, '/')
    res = {}
    for old,new in moves.items():
        res[_rel(old, path)] = _rel(new, path)
        res[_rel(old, src.parent)] = _rel(new, src.parent)
    return sorted(res.items(), key=lambda o: len(o[0]), reverse=True)

def repl_qmd_links(txt, moves, src, root):
    "Rewrite relative and root-relative `.qmd` link targets to `.md`"
    for old,new in _qmd_repls(src, root, moves): txt = txt.replace(old, new)
    return txt

def repl_html_md_links(txt):
    "Rewrite Quarto `.html.md` Markdown-copy targets to Octavo's `.md`"
    return re.sub(r'\.html\.md\b', '.md', txt)

# %% ../nbs/api/20_octavo.ipynb #237aea2c
_re_cv = re.compile(r'^:{3,}[^\S\r\n]*\{([^}]*\.content-visible[^}]*)\}[^\S\r\n]*\n(.*?)\n:{3,}[^\S\r\n]*$', re.MULTILINE | re.DOTALL)

def _repl_cv_match(m):
    attrs,body = m.group(1),m.group(2).strip()
    m_fmt = re.search(r'when-format=["\']?(\w+)["\']?', attrs)
    fmt = m_fmt.group(1).lower() if m_fmt else 'html'
    target = 'md' if fmt in ('markdown', 'commonmark', 'md') else fmt
    if target=='html':
        if (m_style := re.search(r'style=["\']([^"\']+)["\']', attrs)):
            body = f'<div style="{m_style.group(1)}">\n{body}\n</div>'
    return f'```{{={target}}}\n{body}\n```'

def repl_content_visible(s):
    "Convert Quarto `::: {.content-visible when-format=...}` to ````{=md}```` / ````{=html}````"
    return _re_cv.sub(_repl_cv_match, s)

# %% ../nbs/api/20_octavo.ipynb #04d5a738
def _dump_fm(fm): return yaml.dump(fm, sort_keys=False, allow_unicode=True, width=10**9)

def repl_frontmatter_keys(s):
    "Move Quarto's `subtitle`, or a legacy `summary`, to the `description` Octavo shows, unless the page has one"
    fm,body = frontmatter(s)
    if not fm or 'description' in fm or not (old := first(k for k in ('subtitle','summary') if k in fm)): return s
    fm['description'] = fm.pop(old)
    return f'---\n{_dump_fm(fm)}---\n\n{body.lstrip(chr(10))}'

# %% ../nbs/api/20_octavo.ipynb #0ceec29d
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
    fm,_ = frontmatter(new)
    return f"{m.group('q')}---\n{_dump_fm(fm)}---{m.group('q')}" + s[m.end():]

# %% ../nbs/api/20_octavo.ipynb #5e633cec
NBDEV_KEYS = {'skip_exec', 'skip_showdoc'}

def _src_fm(p):
    "Frontmatter of the document, notebook or render script at `p`"
    if p.suffix=='.ipynb': txt = first((c.source for c in read_nb(p).cells if c.cell_type in ('markdown','raw') and c.source.startswith('---'))) or ''
    elif p.suffix=='.py': txt = _script_md(m) if (m := _script_fm.match(p.read_text())) else ''
    else: txt = p.read_text()
    return frontmatter(txt)[0]

def report_page_keys(p):
    "Print the frontmatter keys of `p` that neither Octavo nor nbdev reads"
    unk = unknown_keys(snake_keys(_src_fm(p)), PAGE_KEYS|NBDEV_KEYS)
    if unk: print(f"{p}: Octavo ignores {', '.join(k.replace('_','-') for k in unk)}")

# %% ../nbs/api/20_octavo.ipynb #0c93c529
def _apply_procs(txt, procs):
    for p in procs: txt = p(txt)
    return txt

def migrate_nb_cells(path, procs):
    "Apply `procs` to all markdown cells in a notebook in-place"
    nb,changed = read_nb(path),False
    for c in nb.cells:
        if c.cell_type != 'markdown' or not c.get('source'): continue
        new_src = _apply_procs(c.source, procs)
        if new_src != c.source: c.source,changed = new_src,True
    if changed: write_nb(nb, path)

def migrate_md_file(path, procs):
    "Apply `procs` to a Markdown, QMD or text file in-place"
    txt = path.read_text()
    new_txt = _apply_procs(txt, procs)
    if new_txt!=txt: path.write_text(new_txt)

# %% ../nbs/api/20_octavo.ipynb #01ed763e
def _nav_href(h):
    "Quarto link `h`, with a documentation source path changed to its published HTML page"
    if not h or '://' in h or h.startswith(('#','mailto:')): return h
    m = re.fullmatch(r'(.*?)([^/?#]+)\.(?:ipynb|qmd|md)([?#].*)?', h)
    return f'{m[1]}{page_nm(m[2])}.html{m[3] or ""}' if m else h

def _nav_item(item):
    res = {'text': item['text']}
    if 'menu' in item: res['children'] = [{'text': m['text'], 'href': _nav_href(m['href'])} for m in item['menu'] if 'href' in m]
    elif 'href' in item: res['href'] = _nav_href(item['href'])
    return res

# %% ../nbs/api/20_octavo.ipynb #acd395a1
_ICON_MAP = {'twitter':'x', 'twitter-x':'x'}
_ICON_LABELS = {'github':'GitHub', 'rss':'RSS'}

def _tool_item(item):
    "An octavo `tools` entry from a Quarto icon link, or None where octavo has no such icon"
    from octavo.theme import ICONS
    ico = _ICON_MAP.get(item['icon'], item['icon'])
    if ico not in ICONS: return None
    return {'icon': ico, 'href': _nav_href(item['href']), 'label': item.get('aria-label') or item.get('text') or _ICON_LABELS.get(ico, ico.title())}

# %% ../nbs/api/20_octavo.ipynb #deb7ee06
def _quarto_config(nbs_path):
    qy_p,ny_p = nbs_path/'_quarto.yml',nbs_path/'nbdev.yml'
    qy = yaml.safe_load(qy_p.read_text()) if qy_p.exists() else {}
    ny = yaml.safe_load(ny_p.read_text()) if ny_p.exists() else {}
    for fname,settings in ((qy_p,qy), (ny_p,ny)):
        if settings is not None and not isinstance(settings, dict): raise ValueError(f'{fname} must contain a YAML mapping')
    return qy or {},ny or {}

# %% ../nbs/api/20_octavo.ipynb #127739bd
def _octavo_output(nbs_path, qy, ny):
    "Return a Quarto output override relative to notebooks, or None when doc_path suffices"
    out_dir = (ny.get('project', {}) or {}).get('output-dir') or (qy.get('project', {}) or {}).get('output-dir')
    if not out_dir: return
    cfg = get_config(nbs_path)
    out_dir = (cfg.config_path/Path(out_dir).expanduser()).resolve()
    if out_dir == cfg.doc_path.resolve(): return
    return os.path.relpath(out_dir, Path(nbs_path).resolve()).replace(os.sep, '/')

# %% ../nbs/api/20_octavo.ipynb #201d0976
def _octavo_nav(nbs_path, qy, ny):
    "Convert Quarto navbar settings into Octavo navigation links and icon tools"
    cfg = {}
    def _nav(k): return nested_idx(qy,'website','navbar',k) or nested_idx(ny,'website','navbar',k) or []
    if nav_left := _nav('left'): cfg['nav-links'] = [_nav_item(o) for o in nav_left if 'text' in o and ('href' in o or 'menu' in o)]
    links = L(_nav('right')+_nav('tools')).filter(lambda o: 'icon' in o and 'href' in o)
    tools = links.map(_tool_item)
    for o,t in zip(links,tools):
        if t is None: print(f"{nbs_path/'octavo.yml'}: dropped tool icon {o['icon']!r} ({o['href']}): not bundled by octavo. Add it back with `icon: <path-or-url>` to your own SVG.")
    if (tools := tools.filter()): cfg['tools'] = list(tools)
    return cfg

# %% ../nbs/api/20_octavo.ipynb #e0912069
def _sidebar_item(o, drop):
    "An Octavo `sidebar-links` item from Quarto sidebar entry `o`; `drop` reports entries without an equivalent"
    if isinstance(o, str): o = dict(href=o)
    res = {}
    if (text := o.get('section') or o.get('text')) == '---': return None
    if text: res['text'] = text
    if href := o.get('href'):
        if href=='auto' or '*' in href: return drop(href)
        res['href'] = _nav_href(href)
    if 'contents' in o: res['children'] = [i for c in listify(o['contents']) if (i := _sidebar_item(c, drop))]
    return res or None

def _octavo_sidebar(nbs_path):
    "Convert a hand-written `sidebar.yml` into Octavo `sidebar-links`"
    p = Path(nbs_path)/'sidebar.yml'
    if not get_config(nbs_path).custom_sidebar or not p.exists(): return {}
    sb = nested_idx(yaml.safe_load(p.read_text()) or {}, 'website', 'sidebar') or {}
    if not isinstance(sb, dict):
        print(f'{p}: not converted: Octavo supports one sidebar. Set `sidebar-links` in octavo.yml by hand.')
        return {}
    def drop(h): print(f'{p}: dropped sidebar entry {h!r}: Octavo has no equivalent. List those pages explicitly.')
    links = [i for o in listify(sb.get('contents')) if (i := _sidebar_item(o, drop))]
    return {'sidebar-links': links} if links else {}

# %% ../nbs/api/20_octavo.ipynb #2f2d4b3b
_WEBSITE_KEYS = ('title', 'site-url', 'favicon', 'description', 'open-graph', 'twitter-card')
_HTML_KEYS = ('toc', 'toc-depth')

def _create_octavo_cfg(nbs_path):
    "Octavo settings from `_quarto.yml` and `nbdev.yml`, reporting the Quarto settings Octavo has no equivalent for"
    nbs_path = Path(nbs_path).resolve()
    qy,ny = _quarto_config(nbs_path)
    ws = {**(qy.get('website') or {}), **(ny.get('website') or {})}
    html = nested_idx(qy, 'format', 'html') or {}
    # Quarto reads `$…$` as inline maths, and Octavo does only with this setting.
    cfg = {'math': 'dollars'}
    if (output := _octavo_output(nbs_path, qy, ny)) is not None: cfg['output'] = output
    cfg |= {k:ws[k] for k in _WEBSITE_KEYS if ws.get(k)} | {k:html[k] for k in _HTML_KEYS if k in html}
    if 'site-url' in cfg: cfg['site-url'] = cfg['site-url'].rstrip('/')
    cfg |= _octavo_nav(nbs_path, qy, ny) | _octavo_sidebar(nbs_path)
    drop = [f'website.{k}' for k in ws if k not in (*_WEBSITE_KEYS, 'navbar', 'sidebar')] + [f'format.html.{k}' for k in html if k not in _HTML_KEYS]
    drop += [k.replace('_','-') for k in unknown_keys(snake_keys(cfg), SITE_KEYS)]
    if drop: print(f"{nbs_path}: Octavo has no equivalent for {', '.join(drop)}")
    return cfg

# %% ../nbs/api/20_octavo.ipynb #c4b4478c
def _migrate_octavo(path):
    "Migrate documentation sources in place, create missing Octavo configuration, and return the rename mapping"
    path = Path(path).expanduser()
    if not path.is_dir(): raise NotADirectoryError(path)
    moves = _qmd_moves(path)
    for new in moves.values():
        if new.exists(): raise FileExistsError(f'Cannot rename to existing file: {new}')
    qy = path/'_quarto.yml'
    if (path/'octavo.yml').exists(): octavo_config(path)
    elif not qy.is_file(): raise FileNotFoundError(qy)
    cfg = _create_octavo_cfg(path) if qy.exists() and not (path/'octavo.yml').exists() else None

    files = source_files(path).map(lambda o: path/o)
    srcs = files.filter(lambda p: p.suffix in ('.ipynb','.qmd','.md','.txt'))
    scripts = files.filter(lambda p: p.name.endswith('.qmd.py'))
    for src in srcs:
        procs = [partial(repl_qmd_links, moves=moves, src=src, root=path), repl_html_md_links]
        if src.suffix!='.txt': procs += [repl_content_visible, repl_frontmatter_keys]
        if src.suffix=='.ipynb': migrate_nb_cells(src, procs)
        else:                    migrate_md_file(src, procs)
    for src in scripts: migrate_md_file(src, [repl_script_frontmatter_keys])

    for old,new in moves.items(): old.rename(new)
    for src in srcs+scripts:
        if src.suffix!='.txt': report_page_keys(moves.get(src, src))

    if cfg: (path/'octavo.yml').write_text(yaml.dump(cfg, sort_keys=False))
    return moves

# %% ../nbs/api/20_octavo.ipynb #e332ece4
@call_parse
def nbdev_migrate_octavo(
    path:str=None, # Documentation directory (defaults to configured nbs_path)
):
    "Migrate Quarto-era nbdev project to Octavo"
    moves = _migrate_octavo(get_config().nbs_path if path is None else path)
    for old,new in moves.items(): print(f'{old} -> {new}')
