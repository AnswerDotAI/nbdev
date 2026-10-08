"""Build nbdev documentation with Octavo

Octavo is an alternative to Quarto for building a documentation website from nbdev notebooks. Install `nbdev[octavo]` to use it. A project selects Octavo by placing `octavo.yml` in its configured notebooks directory. Projects without that file continue to use Quarto and do not import Octavo.

The usual `nbdev-docs` command builds the site. Octavo currently builds all pages together. File-selection options are rejected unless left at their defaults; `n_workers` affects only Quarto builds.

Run `nbdev-export` before building to update the generated Python modules and symbol indexes. `nbdev-readme` and `nbdev-contributing` also use Octavo for these projects. `nbdev-prepare` still exports, tests, and cleans notebooks, but skips Quarto configuration generation.

For an existing Quarto project, `nbdev-migrate-octavo` converts documentation sources in place. The converted sources are not intended to work unchanged with both builders. Use `nbdev-preview` to serve the site and rebuild after edits. Refresh the browser manually.

## Migration instructions (share this with your AI)

Before migrating, save a built reference site. Octavo builds replace the output directory. Retaining `_quarto.yml` does not retain the rendered Quarto site or keep converted sources compatible with Quarto.

1. Ensure you have committed your latest changes or backed up your project 
2. From the project root, run `nbdev-docs` while the project still uses Quarto. Confirm the build succeeds and inspect the site. Record existing failures rather than treating them as migration regressions.
3. Copy the complete generated site, including assets and search files, to a separate baseline directory outside the source and build directories.
4. Run `nbdev-migrate-octavo` from the project root. Review its changes and any executable scripts or hooks before attempting another build.
5. Run `nbdev-docs` again to build with Octavo. Keep the baseline untouched. If the build fails, retain its output for diagnosis. Use the manual migration tips below with the baseline path, new output path, and any errors.

Read the retained _quarto.yml, nbdev.yml, pyproject.toml, and generated octavo.yml. Inspect page metadata, stylesheets, render scripts, custom HTML, build hooks, and deployment workflows. Automatic migration renames sources and updates selected document references, directives, metadata, and site settings. It does not port the site's design. It does not copy format.html.css into octavo.yml. It leaves stylesheet files and page-layout metadata unchanged. Existing page-level CSS references can still load; inspect those too. An existing octavo.yml is preserved rather than regenerated.

Identify which checks apply and propose a small migration plan. Inspect optional features only where the project uses them, such as custom homepages, blog listings, embeds, and tabs:

- Styles and custom pages: inspect the rendered Octavo HTML before adapting selectors. Check responsive behavior and dependencies on Bootstrap or Quarto classes. Reuse compatible CSS selectively. Do not enable an old stylesheet wholesale or copy a compatibility layer without checking the current DOM.
- Layouts and themes: review page-layout, sidebars, titles, TOCs, and theme settings. Choose Octavo settings explicitly. Do not assume that renaming a layout preserves its meaning. Octavo's layout: custom is an explicit choice for a custom page, not a general Quarto layout adapter. Check ordinary documentation pages as well as any custom layouts. Compare toc and toc_depth settings with the original metadata, including explicit depth combined with toc: false.
- Embedded and conditional content: review the project's custom markup and format-conditional blocks. Compare when-format and unless-format behavior with the original sources in both HTML and Markdown output. Do not assume automatic conversion preserves exclusion conditions or renders markdown inside an HTML-targeted block. Where needed, adapt HTML-only content to raw {=html} blocks. Verify the result rather than rewriting every block by pattern.
- Render scripts and processors: if the project uses these, check their generated content and assets after migration.
- Navigation and identity: check navbar destinations, dropdowns, icons, favicon, footer, and existing public URLs. Restore omitted icons and preserve the existing footer.
- Additional build outputs: if the project uses custom build hooks, preserve their required outputs using docs_post_build. Check links in any generated indexes.
- Omitted settings: compare the original configuration with Octavo's configuration. List settings that were not carried over, including social metadata, repository actions, theme options, and preview preferences where present. For each, propose a replacement or identify it as intentionally dropped or unsupported. Ask me to approve losses of behavior.
- Installation and deployment: workflows are not migrated. Verify an Octavo-capable nbdev version and the aai-octavo distribution; Python imports remain octavo. Check dependencies required by custom hooks. Verify the documented installation and docs build in a clean environment. Replace direct Quarto build commands where needed with nbdev-docs, including in contributor instructions.
- Output paths: an explicit relative output in octavo.yml is relative to the notebooks directory. Without that setting, nbdev uses its project-relative doc_path. Verify the resolved output directory and the directory published by the deployment workflow.

After approval, make the agreed changes in small steps. Export notebook-authored modules before building. Run nbdev-docs and the relevant repository Markdown commands. Compare the resulting HTML, Markdown, assets, and additional build artifacts with the saved baseline. Check representative API signatures, symbol links, and GitHub source links. Separate pre-existing failures and expected generated differences from migration regressions.

Serve the saved baseline and new output separately. Confirm that each server points to the intended directory. Inspect representative pages at desktop and narrow widths. Test navigation, mobile navigation, anchors, images, and the optional features identified above. Test search and follow result links from both the homepage and a nested page. Exercise the intended hosting subpath, such as /project/, rather than testing only at /. A successful build or static link check does not establish that browser interactions work.

Report the changes, checks actually run, unresolved differences, omitted settings, and decisions requiring my review. Keep the original configuration and baseline until the migration has been reviewed.

Docs: https://nbdev.fast.ai/api/octavo.html.md"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/21_octavo.ipynb.

# %% auto #0
__all__ = ['OctavoProc', 'local_libraries', 'render_script', 'script_pages', 'octavo_config', 'octavo_docs', 'octavo_preview',
           'octavo_readme', 'repl_qmd_links', 'repl_content_visible', 'repl_frontmatter_keys',
           'repl_script_frontmatter_keys', 'migrate_nb_cells', 'migrate_md_file', 'nbdev_migrate_octavo']

# %% ../nbs/api/21_octavo.ipynb #7b098bb5
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

# %% ../nbs/api/21_octavo.ipynb #1cc66460
class OctavoProc(FilterDefaults):
    "Prepare notebook content, metadata, and symbol links for Octavo"
    def __init__(self, local_lib=None, strip_libs=None): self.nl = NbdevLookup(strip_libs=strip_libs or local_lib, local_lib=local_lib)
    def add_links(self, cell): return add_links(cell, nl=self.nl)
    def procs(self): return L(self.add_links if o is add_links else o for o in super().procs())
    def nb_proc(self, nb): return NBProcessor(nb=nb, procs=self.procs(), rm_directives=False)

    def __call__(self, nb):
        super().__call__(nb)
        if getattr(nb, 'frontmatter_', None) and nb.cells[0].cell_type=='raw': nb.cells[0].cell_type = 'markdown'

# %% ../nbs/api/21_octavo.ipynb #9a0258ee
def local_libraries(cfg):
    "Names of the project's declared nbdev symbol indexes"
    proj = _load_toml(cfg.config_file).get('project', {})
    return tuple(proj.get('entry-points', {}).get('nbdev', {}))

# %% ../nbs/api/21_octavo.ipynb #f9f85ebf
def render_script(path):
    "Execute a double-suffix render script and return its printed output with optional page metadata"
    path = Path(path)
    if path.suffix!='.py' or len(path.suffixes)<2: return
    fm = _is_qpy(path) if path.name.endswith('.md.py') else None
    f = StringIO()
    with redirect_stdout(f): exec(compile(path.read_text(encoding='utf-8'), str(path), 'exec'), {})
    return (f'---\n{fm}\n---\n\n' if fm else '') + f.getvalue()

# %% ../nbs/api/21_octavo.ipynb #e85c51f3
def script_pages(root):
    "Render scripts under `root`: `*.md.py` as `Page`s, anything else as `GeneratedFile`s"
    root,pages,files = Path(root),L(),L()
    for o in sorted(root.rglob('*.py')):
        rel = o.relative_to(root)
        if hidden(rel) or (txt:=render_script(o)) is None: continue
        dest = rel.with_suffix('')
        if dest.suffix=='.md': pages.append(Page(str(rel), txt, nm=page_nm(dest)))
        else: files.append(GeneratedFile(str(rel), str(dest), txt))
    return pages,files

# %% ../nbs/api/21_octavo.ipynb #d6904375
def octavo_config(root):
    "Read `octavo.yml` as a settings dictionary; return an empty dictionary for an empty file"
    root = Path(root)
    if not (root/'octavo.yml').is_file(): raise FileNotFoundError(root/'octavo.yml')
    settings = yaml.safe_load((root/'octavo.yml').read_text())
    if settings is None: return {}
    if not isinstance(settings, dict): raise ValueError(f'{root / "octavo.yml"} must contain a YAML mapping')
    return settings

# %% ../nbs/api/21_octavo.ipynb #f6830357
def octavo_docs(
    path:str=None, # Path to the project or its notebooks
):
    "Create Octavo docs and run the optional docs_post_build callback"
    cfg = get_config(path)
    settings = {'output': cfg.doc_path, **octavo_config(cfg.nbs_path)}
    with working_directory(cfg.config_path):
        pages,files = script_pages(cfg.nbs_path)
        docs = scan(cfg.nbs_path, nbproc=OctavoProc(local_lib=local_libraries(cfg))) + pages
        site = Site(docs, root=cfg.nbs_path, files=files, **settings)
        if (miss := site.build()): print(miss)
        if (post := cfg.get('docs_post_build')):
            out = Path(site.settings['output']).expanduser()
            if not out.is_absolute(): out = cfg.nbs_path/out
            import_obj(post)(out.resolve(), cfg)

# %% ../nbs/api/21_octavo.ipynb #db88c5c9
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

# %% ../nbs/api/21_octavo.ipynb #0d38402b
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

# %% ../nbs/api/21_octavo.ipynb #267d0150
def _qmd_moves(path):
    "`.qmd` documents and `.qmd.py` render scripts under `path`, mapped to Octavo names"
    path = Path(path)
    ps = L(path.rglob('*.qmd')) + L(path.rglob('*.qmd.py'))
    return {p:p.with_name(re.sub(r'\.qmd(?=\.py$|$)', '.md', p.name)) for p in sorted(ps)
            if not any(o[0] in '._' for o in p.relative_to(path).parts)}

# %% ../nbs/api/21_octavo.ipynb #a6688f7e
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

# %% ../nbs/api/21_octavo.ipynb #237aea2c
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

# %% ../nbs/api/21_octavo.ipynb #04d5a738
def _dump_fm(fm): return yaml.dump(fm, sort_keys=False, allow_unicode=True, width=10**9)

def repl_frontmatter_keys(s):
    "Normalize legacy and Quarto frontmatter keys for Octavo"
    fm,body = frontmatter(s)
    if not fm: return s
    changed = False
    aliases = [('categories','tags'), ('subtitle','description'), ('summary','description')]
    for old,new in aliases + [(k,k.replace('-','_')) for k in fm if '-' in k and k!='page-layout']:
        if old not in fm: continue
        fm.setdefault(new, fm.pop(old))
        changed = True
    if fm.pop('toc', None) is False:
        fm['toc_depth'] = 0
        changed = True
    if changed: return f'---\n{_dump_fm(fm)}---\n\n{body.lstrip(chr(10))}'
    return s

# %% ../nbs/api/21_octavo.ipynb #0ceec29d
_script_fm = re.compile(r'\A(?P<q>"{3}|\'{3})---\n(?P<fm>.*?)\n---(?P=q)', re.DOTALL)

def repl_script_frontmatter_keys(s):
    "Normalize a render script's leading YAML docstring for Octavo"
    if not (m := _script_fm.match(s)): return s
    old = f"---\n{m.group('fm')}\n---\n"
    new = repl_frontmatter_keys(old)
    if new == old: return s
    fm,_ = frontmatter(new)
    return f"{m.group('q')}---\n{_dump_fm(fm)}---{m.group('q')}" + s[m.end():]

# %% ../nbs/api/21_octavo.ipynb #0c93c529
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
    "Apply `procs` to a Markdown/QMD file in-place"
    txt = path.read_text()
    new_txt = _apply_procs(txt, procs)
    if new_txt!=txt: path.write_text(new_txt)

# %% ../nbs/api/21_octavo.ipynb #01ed763e
def _nav_href(h):
    if not h or '://' in h or h.startswith(('#','mailto:')): return h
    return re.sub(r'\.(?:ipynb|qmd|md)(?=[?#]|$)', '.html', h)

def _nav_item(item):
    res = {'text': item['text']}
    if 'menu' in item: res['children'] = [{'text': m['text'], 'href': _nav_href(m['href'])} for m in item['menu'] if 'href' in m]
    elif 'href' in item: res['href'] = _nav_href(item['href'])
    return res

# %% ../nbs/api/21_octavo.ipynb #acd395a1
_ICON_MAP = {'twitter':'x', 'twitter-x':'x'}
_ICON_LABELS = {'github':'GitHub', 'rss':'RSS'}

def _tool_item(item):
    "An octavo `tools` entry from a Quarto icon link, or None where octavo has no such icon"
    from octavo.theme import ICONS
    ico = _ICON_MAP.get(item['icon'], item['icon'])
    if ico not in ICONS: return None
    return {'icon': ico, 'href': _nav_href(item['href']), 'label': item.get('aria-label') or item.get('text') or _ICON_LABELS.get(ico, ico.title())}

# %% ../nbs/api/21_octavo.ipynb #deb7ee06
def _quarto_config(nbs_path):
    qy_p,ny_p = nbs_path/'_quarto.yml',nbs_path/'nbdev.yml'
    qy = yaml.safe_load(qy_p.read_text()) if qy_p.exists() else {}
    ny = yaml.safe_load(ny_p.read_text()) if ny_p.exists() else {}
    for fname,settings in ((qy_p,qy), (ny_p,ny)):
        if settings is not None and not isinstance(settings, dict): raise ValueError(f'{fname} must contain a YAML mapping')
    return qy or {},ny or {}

# %% ../nbs/api/21_octavo.ipynb #127739bd
def _octavo_output(nbs_path, qy, ny):
    "Return a Quarto output override relative to notebooks, or None when doc_path suffices"
    out_dir = (ny.get('project', {}) or {}).get('output-dir') or (qy.get('project', {}) or {}).get('output-dir')
    if not out_dir: return
    cfg = get_config(nbs_path)
    out_dir = (cfg.config_path/Path(out_dir).expanduser()).resolve()
    if out_dir == cfg.doc_path.resolve(): return
    return os.path.relpath(out_dir, Path(nbs_path).resolve()).replace(os.sep, '/')

# %% ../nbs/api/21_octavo.ipynb #201d0976
def _octavo_nav(nbs_path, qy, ny):
    "Convert Quarto navbar settings into Octavo navigation links and icon tools"
    cfg = {}
    def _nav(k): return nested_idx(qy,'website','navbar',k) or nested_idx(ny,'website','navbar',k) or []
    if nav_left := _nav('left'): cfg['nav_links'] = [_nav_item(o) for o in nav_left if 'text' in o and ('href' in o or 'menu' in o)]
    links = L(_nav('right')+_nav('tools')).filter(lambda o: 'icon' in o and 'href' in o)
    tools = links.map(_tool_item)
    for o,t in zip(links,tools):
        if t is None: print(f"{nbs_path/'octavo.yml'}: dropped tool icon {o['icon']!r} ({o['href']}): not bundled by octavo. Add it back with `icon: <path-or-url>` to your own SVG.")
    if (tools := tools.filter()): cfg['tools'] = list(tools)
    return cfg

# %% ../nbs/api/21_octavo.ipynb #2f2d4b3b
def _create_octavo_cfg(nbs_path):
    "Return Octavo settings derived from `_quarto.yml` and `nbdev.yml`"
    nbs_path = Path(nbs_path).resolve()
    qy,ny = _quarto_config(nbs_path)
    ws_q,ws_n = qy.get('website', {}) or {},ny.get('website', {}) or {}
    fmt_html = (qy.get('format', {}) or {}).get('html', {}) or {}
    cfg = {}
    if (output := _octavo_output(nbs_path, qy, ny)) is not None: cfg['output'] = output
    title = ws_n.get('title') or ws_q.get('title')
    if title: cfg['title'] = title
    site_url = ws_n.get('site-url') or ws_q.get('site-url')
    if site_url: cfg['site_url'] = site_url.rstrip('/')
    if 'toc-depth' in fmt_html:
        try: cfg['toc_depth'] = max(1, int(fmt_html['toc-depth']) - 1)
        except (ValueError, TypeError): pass
    else: cfg['toc_depth'] = 0 if fmt_html.get('toc') is False else 3
    favicon = ws_n.get('favicon') or ws_q.get('favicon')
    if favicon: cfg['favicon'] = favicon
    cfg.update(_octavo_nav(nbs_path, qy, ny))
    return cfg

# %% ../nbs/api/21_octavo.ipynb #c4b4478c
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

    srcs = [p for p in sorted(path.rglob('*')) if p.suffix in ('.ipynb','.qmd','.md')
            and not any(o[0] in '._' for o in p.relative_to(path).parts)]
    scripts = [p for p in sorted(path.rglob('*.qmd.py'))
               if not any(o[0] in '._' for o in p.relative_to(path).parts)]
    for src in srcs:
        procs = [partial(repl_qmd_links, moves=moves, src=src, root=path), repl_content_visible, repl_frontmatter_keys]
        if src.suffix=='.ipynb': migrate_nb_cells(src, procs)
        else:                    migrate_md_file(src, procs)
    for src in scripts: migrate_md_file(src, [repl_script_frontmatter_keys])

    for old,new in moves.items(): old.rename(new)

    if cfg: (path/'octavo.yml').write_text(yaml.dump(cfg, sort_keys=False))
    return moves

# %% ../nbs/api/21_octavo.ipynb #e332ece4
@call_parse
def nbdev_migrate_octavo(
    path:str=None, # Documentation directory (defaults to configured nbs_path)
):
    "Migrate Quarto-era nbdev project to Octavo"
    moves = _migrate_octavo(get_config().nbs_path if path is None else path)
    for old,new in moves.items(): print(f'{old} -> {new}')
