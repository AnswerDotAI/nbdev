"""Configuring nbdev and bootstrapping notebook export"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/01_config.ipynb.

# %% auto 0
__all__ = ['pyproj_tmpl', 'nbdev_create_config', 'get_config', 'config_key', 'is_nbdev', 'create_output', 'show_src',
           'update_version', 'update_proj', 'add_init', 'write_cells']

# %% ../nbs/api/01_config.ipynb
from datetime import datetime
from fastcore.docments import *
from fastcore.utils import *
from fastcore.meta import *
from fastcore.script import *
from fastcore.style import *
from fastcore.xdg import *

import ast
from IPython.display import Markdown
from execnb.nbio import read_nb,NbCell
from urllib.error import HTTPError

# %% ../nbs/api/01_config.ipynb
_nbdev_home_dir = 'nbdev' # sub-directory of xdg base dir
_nbdev_cfg_name = 'settings.ini'

# %% ../nbs/api/01_config.ipynb
def _git_repo():
    try: return repo_details(run('git config --get remote.origin.url'))[1]
    except OSError: return

# %% ../nbs/api/01_config.ipynb
# When adding a named default to the list below, be sure that that name
# is also added to one of the sections in `_nbdev_cfg_sections` as well,
# or it won't get written by `nbdev_create_config`:
def _apply_defaults(
    cfg,
    lib_name='%(repo)s', # Package name
    git_url='https://github.com/%(user)s/%(repo)s', # Repo URL
    custom_sidebar:bool_arg=False, # Use a custom sidebar.yml?
    nbs_path:Path='nbs', # Path to notebooks
    lib_path:Path=None, # Path to package root (default: `repo` with `-` replaced by `_`)
    doc_path:Path='_docs', # Path to rendered docs
    tst_flags='notest', # Test flags
    version='0.0.1', # Version of this release
    doc_host='https://%(user)s.github.io',  # Hostname for docs
    doc_baseurl='/%(repo)s',  # Base URL for docs
    keywords='nbdev jupyter notebook python', # Package keywords
    license='apache2', # License for the package
    copyright:str=None, # Copyright for the package, defaults to '`current_year` onwards, `author`'
    status='3', # Development status PyPI classifier
    min_python='3.9', # Minimum Python version PyPI classifier
    audience='Developers', # Intended audience PyPI classifier
    language='English', # Language PyPI classifier
    recursive:bool_arg=True, # Include subfolders in notebook globs?
    black_formatting:bool_arg=False, # Format libraries with black?
    readme_nb='index.ipynb', # Notebook to export as repo readme
    title='%(lib_name)s', # Quarto website title
    allowed_metadata_keys='', # Preserve the list of keys in the main notebook metadata
    allowed_cell_metadata_keys='', # Preserve the list of keys in cell level metadata
    jupyter_hooks:bool_arg=False, # Run Jupyter hooks?
    clean_ids:bool_arg=True, # Remove ids from plaintext reprs?
    clear_all:bool_arg=False, # Remove all cell metadata and cell outputs?
    cell_number:bool_arg=True, # Add cell number to the exported file
    put_version_in_init:bool_arg=True, # Add the version to the main __init__.py in nbdev_export
    update_pyproject:bool_arg=True, # Create/update pyproject.toml with correct project name
    skip_procs:str='', # A comma-separated list of processors that you want to skip
):
    "Apply default settings where missing in `cfg`."
    if getattr(cfg,'repo',None) is None:
        cfg.repo = _git_repo()
        if cfg.repo is None:
            _parent = Path.cwd()
            cfg.repo = _parent.parent.name if _parent.name=='nbs' else _parent.name
    if lib_path is None: lib_path = cfg.repo.replace('-', '_')
    if copyright is None: copyright = f"{datetime.now().year} onwards, %(author)s"
    for k,v in locals().items():
        if k.startswith('_') or k == 'cfg' or cfg.get(k) is not None: continue
        cfg[k] = v
    return cfg

# %% ../nbs/api/01_config.ipynb
def _get_info(owner, repo, default_branch='main', default_kw='nbdev'):
    from ghapi.all import GhApi
    api = GhApi(owner=owner, repo=repo, token=os.getenv('GITHUB_TOKEN'))
    
    try: r = api.repos.get()
    except HTTPError:
        msg= [f"""Could not access repo: {owner}/{repo} to find your default branch - `{default_branch}` assumed.
Edit `settings.ini` if this is incorrect.
In the future, you can allow nbdev to see private repos by setting the environment variable GITHUB_TOKEN as described here:
https://nbdev.fast.ai/api/release.html#setup"""]
        print(''.join(msg))
        return default_branch,default_kw,''
    
    return r.default_branch, default_kw if not getattr(r, 'topics', []) else ' '.join(r.topics), r.description

# %% ../nbs/api/01_config.ipynb
def _fetch_from_git(raise_err=False):
    "Get information for settings.ini from the user."
    res={}
    try:
        url = run('git config --get remote.origin.url')
        res['user'],res['repo'] = repo_details(url)
        res['branch'],res['keywords'],desc = _get_info(owner=res['user'], repo=res['repo'])
        if desc: res['description'] = desc
        res['author'] = run('git config --get user.name').strip() # below two lines attempt to pull from global user config
        res['author_email'] = run('git config --get user.email').strip()
    except OSError as e:
        if raise_err: raise(e)
    else: res['lib_name'] = res['repo'].replace('-','_')
    return res

# %% ../nbs/api/01_config.ipynb
def _prompt_user(cfg, inferred):
    "Let user input values not in `cfg` or `inferred`."
    res = cfg.copy()
    for k,v in cfg.items():
        inf = inferred.get(k,None)
        msg = S.light_blue(k) + ' = '
        if v is None:
            if inf is None: res[k] = input(f'# Please enter a value for {k}\n'+msg)
            else:
                res[k] = inf
                print(msg+res[k]+' # Automatically inferred from git')
    return res

# %% ../nbs/api/01_config.ipynb
def _cfg2txt(cfg, head, sections, tail=''):
    "Render `cfg` with commented sections."
    nm = cfg.d.name
    res = f'[{nm}]\n'+head
    for t,ks in sections.items():
        res += f'### {t} ###\n'
        for k in ks.split(): res += f"{k} = {cfg._cfg.get(nm, k, raw=True)}\n" # TODO: add `raw` to `Config.get`
        res += '\n'
    res += tail
    return res.strip()

# %% ../nbs/api/01_config.ipynb
_nbdev_cfg_head = '''# All sections below are required unless otherwise specified.
# See https://github.com/AnswerDotAI/nbdev/blob/main/settings.ini for examples.

'''
_nbdev_cfg_sections = {'Python library': 'repo lib_name version min_python license black_formatting',
                       'nbdev': 'doc_path lib_path nbs_path recursive tst_flags put_version_in_init update_pyproject',
                       'Docs': 'branch custom_sidebar doc_host doc_baseurl git_url title',
                       'PyPI': 'audience author author_email copyright description keywords language status user'}
_nbdev_cfg_tail = '''### Optional ###
# requirements = fastcore pandas
# dev_requirements = 
# console_scripts =
# conda_user = 
# package_data = 
'''

# %% ../nbs/api/01_config.ipynb
@call_parse
@delegates(_apply_defaults, but='cfg')
def nbdev_create_config(
    repo:str=None, # Repo name
    branch:str=None, # Repo default branch
    user:str=None, # Repo username
    author:str=None, # Package author's name
    author_email:str=None, # Package author's email address
    description:str=None, # Short summary of the package
    path:str='.', # Path to create config file
    cfg_name:str=_nbdev_cfg_name, # Name of config file to create
    **kwargs
):
    "Create a config file."
    req = {k:v for k,v in locals().items() if k not in ('path','cfg_name','kwargs')}
    inf = _fetch_from_git()
    d = _prompt_user(req, inf)
    cfg = Config(path, cfg_name, d, save=False)
    if cfg.config_file.exists(): warn(f'Config file already exists: {cfg.config_file} and will be used as a base')
    cfg = _apply_defaults(cfg, **kwargs)
    txt = _cfg2txt(cfg, _nbdev_cfg_head, _nbdev_cfg_sections, _nbdev_cfg_tail)
    cfg.config_file.write_text(txt)
    cfg_fn = Path(path)/cfg_name
    print(f'{cfg_fn} created.')

# %% ../nbs/api/01_config.ipynb
def _nbdev_config_file(cfg_name=_nbdev_cfg_name, path=None):
    cfg_path = Path.cwd() if path is None else Path(path)
    return getattr(Config.find(cfg_name), 'config_file', cfg_path/cfg_name)

# %% ../nbs/api/01_config.ipynb
def _xdg_config_paths(cfg_name=_nbdev_cfg_name):
    xdg_config_paths = reversed([xdg_config_home()]+xdg_config_dirs())
    return [o/_nbdev_home_dir/cfg_name for o in xdg_config_paths]

# %% ../nbs/api/01_config.ipynb
def _type(t): return bool if t==bool_arg else t
_types = {k:_type(v['anno']) for k,v in docments(_apply_defaults,full=True,returns=False).items() if k != 'cfg'}

@functools.lru_cache(maxsize=None)
def get_config(cfg_name=_nbdev_cfg_name, path=None):
    "Return nbdev config."
    cfg_file = _nbdev_config_file(cfg_name, path)
    extra_files = _xdg_config_paths(cfg_name)
    cfg = Config(cfg_file.parent, cfg_file.name, extra_files=extra_files, types=_types)
    return _apply_defaults(cfg)

# %% ../nbs/api/01_config.ipynb
def config_key(c, default=None, path=True, missing_ok=None):
    "Deprecated: use `get_config().get` or `get_config().path` instead."
    warn("`config_key` is deprecated. Use `get_config().get` or `get_config().path` instead.", DeprecationWarning)
    return get_config().path(c, default) if path else get_config().get(c, default)

# %% ../nbs/api/01_config.ipynb
def is_nbdev(): return _nbdev_config_file().exists()

# %% ../nbs/api/01_config.ipynb
def create_output(txt, mime):
    "Add a cell output containing `txt` of the `mime` text MIME sub-type"
    return [{"data": { f"text/{mime}": str(txt).splitlines(True) },
             "execution_count": 1, "metadata": {}, "output_type": "execute_result"}]

# %% ../nbs/api/01_config.ipynb
def show_src(src, lang='python'): return Markdown(f'```{lang}\n{src}\n```')

# %% ../nbs/api/01_config.ipynb
pyproj_tmpl = """[build-system]
requires = ["setuptools>=64.0"]
build-backend = "setuptools.build_meta"

[project]
name = "FILL_IN"
requires-python="FILL_IN"
dynamic = [ "keywords", "description", "version", "dependencies", "optional-dependencies", "readme", "license", "authors", "classifiers", "entry-points", "scripts", "urls"]

[tool.uv]
cache-keys = [{ file = "pyproject.toml" }, { file = "settings.ini" }, { file = "setup.py" }]
"""

# %% ../nbs/api/01_config.ipynb
_re_version = re.compile(r'^__version__\s*=.*$', re.MULTILINE)
_re_proj = re.compile(r'^name\s*=\s*".*$', re.MULTILINE)
_re_reqpy = re.compile(r'^requires-python\s*=\s*".*$', re.MULTILINE)
_init = '__init__.py'
_pyproj = 'pyproject.toml'

def update_version(path=None):
    "Add or update `__version__` in the main `__init__.py` of the library."
    path = Path(path or get_config().lib_path)
    fname = path/_init
    if not fname.exists(): fname.touch()
    version = f'__version__ = "{get_config().version}"'
    code = fname.read_text()
    if _re_version.search(code) is None: code = version + "\n" + code
    else: code = _re_version.sub(version, code)
    fname.write_text(code)

def _has_py(fs): return any(1 for f in fs if f.endswith('.py'))

def update_proj(path):
    "Create or update `pyproject.toml` in the project root."
    fname = path/_pyproj
    if not fname.exists(): fname.write_text(pyproj_tmpl)
    txt = fname.read_text()
    txt = _re_proj.sub(f'name="{get_config().lib_name}"', txt)
    txt = _re_reqpy.sub(f'requires-python=">={get_config().min_python}"', txt)
    fname.write_text(txt)

def add_init(path=None):
    "Add `__init__.py` in all subdirs of `path` containing python files if it's not there already."
    # we add the lowest-level `__init__.py` files first, which ensures _has_py succeeds for parent modules
    path = Path(path or get_config().lib_path)
    path.mkdir(exist_ok=True)
    if not (path/_init).exists(): (path/_init).touch()
    for r,ds,fs in os.walk(path, topdown=False):
        r = Path(r)
        subds = (os.listdir(r/d) for d in ds)
        if _has_py(fs) or any(filter(_has_py, subds)) and not (r/_init).exists(): (r/_init).touch()
    if get_config().get('put_version_in_init', True): update_version(path)
    if get_config().get('update_pyproject', True): update_proj(path.parent)

# %% ../nbs/api/01_config.ipynb
def write_cells(cells, hdr, file, offset=0, cell_number=True, solo_nb=False):
    "Write `cells` to `file` along with header `hdr` starting at index `offset` (mainly for nbdev internal use)."
    for cell in cells:
        if cell.cell_type=='code' and cell.source.strip():
            idx = f" {cell.idx_+offset}" if cell_number else ""
            file.write(f'\n\n{hdr}{idx}\n{cell.source}') if not solo_nb else file.write(f'\n\n{cell.source}')

# %% ../nbs/api/01_config.ipynb
def _basic_export_nb(fname, name, dest=None):
    "Basic exporter to bootstrap nbdev."
    if dest is None: dest = get_config().lib_path
    add_init()
    fname,dest = Path(fname),Path(dest)
    nb = read_nb(fname)

    # grab the source from all the cells that have an `export` comment
    cells = L(cell for cell in nb.cells if re.match(r'#\s*\|export', cell.source))

    # find all the exported functions, to create `__all__`:
    trees = cells.map(NbCell.parsed_).concat()
    funcs = trees.filter(risinstance((ast.FunctionDef,ast.ClassDef))).attrgot('name')
    exp_funcs = [f for f in funcs if f[0]!='_']

    # write out the file
    with (dest/name).open('w',encoding="utf-8") as f:
        f.write(f"# %% auto 0\n__all__ = {exp_funcs}")
        write_cells(cells, f"# %% {fname.relpath(dest)}", f)
        f.write('\n')
