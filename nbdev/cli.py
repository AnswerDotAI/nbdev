# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_cli.ipynb (unless otherwise specified).

__all__ = ['nbdev_migrate2magic', 'nbdev_build_lib', 'nbdev_update_lib', 'nbdev_diff_nbs', 'nbdev_test_nbs',
           'make_readme', 'nbdev_build_docs', 'nbdev_nb2md', 'nbdev_detach', 'nbdev_read_nbs', 'nbdev_trust_nbs',
           'nbdev_fix_merge', 'bump_version', 'nbdev_bump_version', 'nbdev_install_git_hooks', 'nbdev_new']

# Cell
from .imports import *
from .export import *
from .sync import *
from .merge import *
from .export2html import *
from .test import *
from fastscript import call_parse,Param,bool_arg

# Cell
import re,nbformat

# Internal Cell
def _code_patterns_and_replace_fns():
    "return a list of pattern/function tuples that can migrate flags used in code cells"
    patterns_and_replace_fns = []

    def _replace_fn(magic, m):
        "return a magic flag for a comment flag matched in `m`"
        return f'%{magic}' if m.group(1) is None else f'%{magic} {m.group(1).strip()}'

    def _add_pattern_and_replace_fn(comment_flag, magic_flag):
        "add a pattern/function tuple to go from comment to magic flag"
        pattern = re.compile(rf"""
# Matches a comment flag line (e.g. #exporti) and catches parameter in group 1:
^              # beginning of line (since re.MULTILINE is passed)
\s*            # any number of whitespace
\#\s*          # "#", then any number of whitespace
{comment_flag} #
([ \t]+\S+)?   # catch a group, with leading spaces and/or tabs, followed by any non-whitespace chars
\s*            # any number of whitespace
$              # end of line (since re.MULTILINE is passed)
""", re.IGNORECASE | re.MULTILINE | re.VERBOSE)
        # note: fn has to be single arg so we can use it in `pattern.sub` calls later
        patterns_and_replace_fns.append((pattern, partial(_replace_fn, magic_flag)))

    _add_pattern_and_replace_fn('default_exp', 'nbdev_default_export')
    _add_pattern_and_replace_fn('exports', 'nbdev_export_and_show')
    _add_pattern_and_replace_fn('exporti', 'nbdev_export_internal')
    _add_pattern_and_replace_fn('export', 'nbdev_export')
    _add_pattern_and_replace_fn('hide_input', 'nbdev_hide_input')
    _add_pattern_and_replace_fn('hide_output', 'nbdev_hide_output')
    _add_pattern_and_replace_fn('hide', 'nbdev_hide')
    _add_pattern_and_replace_fn('default_cls_lvl', 'nbdev_default_class_level')
    _add_pattern_and_replace_fn('collapse[_-]output', 'nbdev_collapse_output')
    _add_pattern_and_replace_fn('collapse[_-]show', 'nbdev_collapse_input open')
    _add_pattern_and_replace_fn('collapse[_-]hide', 'nbdev_collapse_input')
    _add_pattern_and_replace_fn('collapse', 'nbdev_collapse_input')
    for flag in Config().get('tst_flags', '').split('|'):
        _add_pattern_and_replace_fn(f'all_{flag}', f'nbdev_{flag}_test all')
        _add_pattern_and_replace_fn(flag, f'nbdev_{flag}_test')
    return patterns_and_replace_fns

# Internal Cell
class CellMigrator():
    """Can migrate a cell using `patterns_and_replace_fns`.
    Keeps track of the number of cells updated in `upd_count`"""
    def __init__(self, patterns_and_replace_fns):
        self.patterns_and_replace_fns,self.upd_count=patterns_and_replace_fns,0
    def __call__(self, cell):
        for pattern, replace_fn in self.patterns_and_replace_fns:
            source=cell.source
            cell.source=pattern.sub(replace_fn, source)
            if source!=cell.source: self.upd_count+=1

# Internal Cell
def _migrate2magic(nb, update_md=False):
    "Migrate a single notebook"
    code_cell_migrator=CellMigrator(_code_patterns_and_replace_fns())
    [code_cell_migrator(cell) for cell in nb.cells if cell.cell_type=='code']
    if code_cell_migrator.upd_count!=0:
        nb.cells.insert(0, nbformat.v4.new_code_cell('from nbdev import *'))
    NotebookNotary().sign(nb)
    return nb

# Cell
@call_parse
def nbdev_migrate2magic():
    """Update all notebooks in `nbs_path` to use magic flags."""
    config=Config()
    bck_path=config.config_file.parent/'.nbdev_bck_0'
    i=0
    while bck_path.exists():
        i+=1
        bck_path=config.config_file.parent/f'.nbdev_bck_{i}'
    bck_path.mkdir()
    for fname in config.nbs_path.glob('*.ipynb'):
        shutil.copy2(fname, bck_path)
    print('Copied nbs in', config.nbs_path, 'to', bck_path)
    for fname in config.nbs_path.glob('*.ipynb'):
        print('Migrating', fname)
        nbformat.write(_migrate2magic(read_nb(fname)), str(fname), version=4)

# Internal Cell
def find_in_nbs(fname, patterns):
    """returns notebook name and the source of the 1st code cell in a notebook that
    contains one of `patterns`, searching files in name order"""
    if fname is None:
        files = [f for f in Config().nbs_path.glob('*.ipynb') if not f.name.startswith('_')]
    else: files = glob.glob(fname)
    for file in [Path(f).absolute() for f in sorted(files)]:
        nb=read_nb(file)
        for cell in nb.cells:
            if cell.cell_type!='code': continue
            for pattern in patterns:
                if pattern.search(cell.source): return file, cell.source

# Internal Cell
def migrate2magic_check(fname, on_fail='error'):
    """checks notebooks for comment flags and if found will:
    raise an exception if `on_fail`='error' or print a warning if `on_fail`='warn'"""
    result=find_in_nbs(fname, [o[0] for o in _code_patterns_and_replace_fns()])
    if result is not None:
        msg=f'Warning: Comment flag found in "{result[0]}". Please run nbdev_migrate2magic'
        if on_fail=='error': raise Exception(msg)
        print(msg)

# Cell
@call_parse
def nbdev_build_lib(fname:Param("A notebook name or glob to convert", str)=None):
    "Export notebooks matching `fname` to python modules"
    migrate2magic_check(fname)
    write_tmpls()
    notebook2script(fname=fname)

# Cell
@call_parse
def nbdev_update_lib(fname:Param("A notebook name or glob to convert", str)=None):
    "Propagates any change in the modules matching `fname` to the notebooks that created them"
    migrate2magic_check(fname)
    script2notebook(fname=fname)

# Cell
@call_parse
def nbdev_diff_nbs():
    "Prints the diff between an export of the library in notebooks and the actual modules"
    migrate2magic_check(None)
    diff_nb_script()

# Cell
def _test_one(fname, flags=None, verbose=True):
    print(f"testing: {fname}")
    start = time.time()
    try:
        test_nb(fname, flags=flags)
        return True,time.time()-start
    except Exception as e:
        if "Kernel died before replying to kernel_info" in str(e):
            time.sleep(random.random())
            _test_one(fname, flags=flags)
        if verbose: print(f'Error in {fname}:\n{e}')
        return False,time.time()-start

# Cell
@call_parse
def nbdev_test_nbs(fname:Param("A notebook name or glob to convert", str)=None,
                   flags:Param("Space separated list of flags", str)=None,
                   n_workers:Param("Number of workers to use", int)=None,
                   verbose:Param("Print errors along the way", bool)=True,
                   timing:Param("Timing each notebook to see the ones are slow", bool)=False):
    "Test in parallel the notebooks matching `fname`, passing along `flags`"
    migrate2magic_check(fname)
    if flags is not None: flags = flags.split(' ')
    if fname is None:
        files = [f for f in Config().nbs_path.glob('*.ipynb') if not f.name.startswith('_')]
    else: files = glob.glob(fname)
    files = [Path(f).absolute() for f in sorted(files)]
    if len(files)==1 and n_workers is None: n_workers=0
    # make sure we are inside the notebook folder of the project
    os.chdir(Config().nbs_path)
    results = parallel(_test_one, files, flags=flags, verbose=verbose, n_workers=n_workers)
    passed,times = [r[0] for r in results],[r[1] for r in results]
    if all(passed): print("All tests are passing!")
    else:
        msg = "The following notebooks failed:\n"
        raise Exception(msg + '\n'.join([f.name for p,f in zip(passed,files) if not p]))
    if timing:
        for i,t in sorted(enumerate(times), key=lambda o:o[1], reverse=True):
            print(f"Notebook {files[i].name} took {int(t)} seconds")

# Cell
_re_index = re.compile(r'^(?:\d*_|)index\.ipynb$')

# Cell
def make_readme():
    "Convert the index notebook to README.md"
    migrate2magic_check(None)
    index_fn = None
    for f in Config().nbs_path.glob('*.ipynb'):
        if _re_index.match(f.name): index_fn = f
    assert index_fn is not None, "Could not locate index notebook"
    print(f"converting {index_fn} to README.md")
    convert_md(index_fn, Config().config_file.parent, jekyll=False)
    n = Config().config_file.parent/index_fn.with_suffix('.md').name
    shutil.move(n, Config().config_file.parent/'README.md')
    if Path(Config().config_file.parent/'PRE_README.md').is_file():
        with open(Config().config_file.parent/'README.md', 'r') as f: readme = f.read()
        with open(Config().config_file.parent/'PRE_README.md', 'r') as f: pre_readme = f.read()
        with open(Config().config_file.parent/'README.md', 'w') as f: f.write(f'{pre_readme}\n{readme}')

# Cell
@call_parse
def nbdev_build_docs(fname:Param("A notebook name or glob to convert", str)=None,
                     force_all:Param("Rebuild even notebooks that haven't changed", bool)=False,
                     mk_readme:Param("Also convert the index notebook to README", bool)=True,
                     n_workers:Param("Number of workers to use", int)=None):
    "Build the documentation by converting notebooks mathing `fname` to html"
    migrate2magic_check(fname)
    notebook2html(fname=fname, force_all=force_all, n_workers=n_workers)
    if fname is None: make_sidebar()
    if mk_readme: make_readme()

# Cell
@call_parse
def nbdev_nb2md(fname:Param("A notebook file name to convert", str),
                dest:Param("The destination folder", str)='.',
                img_path:Param("Folder to export images to")="",
                jekyll:Param("To use jekyll metadata for your markdown file or not", bool_arg)=False,):
    "Convert the notebook in `fname` to a markdown file"
    migrate2magic_check(fname)
    nb_detach_cells(fname, dest=img_path)
    convert_md(fname, dest, jekyll=jekyll, img_path=img_path)

# Cell
@call_parse
def nbdev_detach(path_nb:Param("Path to notebook"),
                 dest:Param("Destination folder", str)="",
                 use_img:Param("Convert markdown images to img tags", bool_arg)=False):
    "Export cell attachments to `dest` and update references"
    migrate2magic_check(None, 'warn')
    nb_detach_cells(path_nb, dest=dest, use_img=use_img)

# Cell
@call_parse
def nbdev_read_nbs(fname:Param("A notebook name or glob to convert", str)=None):
    "Check all notebooks matching `fname` can be opened"
    migrate2magic_check(fname, 'warn')
    files = Config().nbs_path.glob('**/*.ipynb') if fname is None else glob.glob(fname)
    for nb in files:
        try: _ = read_nb(nb)
        except Exception as e:
            print(f"{nb} is corrupted and can't be opened.")
            raise e

# Cell
@call_parse
def nbdev_trust_nbs(fname:Param("A notebook name or glob to convert", str)=None,
                    force_all:Param("Trust even notebooks that haven't changed", bool)=False):
    "Trust noteboks matching `fname`"
    migrate2magic_check(fname, 'warn')
    check_fname = Config().nbs_path/".last_checked"
    last_checked = os.path.getmtime(check_fname) if check_fname.exists() else None
    files = Config().nbs_path.glob('**/*.ipynb') if fname is None else glob.glob(fname)
    for fn in files:
        if last_checked and not force_all:
            last_changed = os.path.getmtime(fn)
            if last_changed < last_checked: continue
        nb = read_nb(fn)
        if not NotebookNotary().check_signature(nb): NotebookNotary().sign(nb)
    check_fname.touch(exist_ok=True)

# Cell
@call_parse
def nbdev_fix_merge(fname:Param("A notebook filename to fix", str),
                    fast:Param("Fast fix: automatically fix the merge conflicts in outputs or metadata", bool)=True,
                    trust_us:Param("Use local outputs/metadata when fast mergning", bool)=True):
    "Fix merge conflicts in notebook `fname`"
    migrate2magic_check(fname, 'warn')
    fix_conflicts(fname, fast=fast, trust_us=trust_us)

# Cell
def bump_version(version, part=2):
    version = version.split('.')
    version[part] = str(int(version[part]) + 1)
    for i in range(part+1, 3): version[i] = '0'
    return '.'.join(version)

# Cell
@call_parse
def nbdev_bump_version(part:Param("Part of version to bump", int)=2):
    "Increment version in `settings.py` by one"
    migrate2magic_check(None, 'warn')
    cfg = Config()
    print(f'Old version: {cfg.version}')
    cfg.d['version'] = bump_version(Config().version, part)
    cfg.save()
    update_version()
    print(f'New version: {cfg.version}')

# Cell
import subprocess

# Cell
@call_parse
def nbdev_install_git_hooks():
    "Install git hooks to clean/trust notebooks automatically"
    try: path = Config().config_file.parent
    except: path = Path.cwd()
    fn = path/'.git'/'hooks'/'post-merge'
    #Trust notebooks after merge
    with open(fn, 'w') as f:
        f.write("""#!/bin/bash
echo "Trusting notebooks"
nbdev_trust_nbs
"""
        )
    os.chmod(fn, os.stat(fn).st_mode | stat.S_IEXEC)
    #Clean notebooks on commit/diff
    with open(path/'.gitconfig', 'w') as f:
        f.write("""# Generated by nbdev_install_git_hooks
#
# If you need to disable this instrumentation do:
#
# git config --local --unset include.path
#
# To restore the filter
#
# git config --local include.path .gitconfig
#
# If you see notebooks not stripped, checked the filters are applied in .gitattributes
#
[filter "clean-nbs"]
        clean = nbdev_clean_nbs --read_input_stream True
        smudge = cat
        required = true
[diff "ipynb"]
        textconv = nbdev_clean_nbs --disp True --fname
""")
    cmd = "git config --local include.path ../.gitconfig"
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd.split(), shell=False, check=False, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Success: hooks are installed and repo's .gitconfig is now trusted")
    else:
        print("Failed to trust repo's .gitconfig")
        if result.stderr: print(f"Error: {result.stderr.decode('utf-8')}")
    try: nb_path = Config().nbs_path
    except: nb_path = Path.cwd()
    with open(nb_path/'.gitattributes', 'w') as f:
        f.write("""**/*.ipynb filter=clean-nbs
**/*.ipynb diff=ipynb
"""
               )

# Cell
_template_git_repo = "https://github.com/fastai/nbdev_template.git"

# Cell
@call_parse
def nbdev_new(name: Param("A directory to create the project in", str)):
    "Create a new nbdev project with a given name."

    path = Path(f"./{name}").absolute()

    if path.is_dir():
        print(f"Directory {path} already exists. Aborting.")
        return

    print(f"Creating a new nbdev project {name}.")

    try:
        subprocess.run(['git', 'clone', f'{_template_git_repo}', f'{path}'], check=True, timeout=5000)
        shutil.rmtree(path/".git")
        subprocess.run("git init".split(), cwd=path, check=True)
        subprocess.run("git add .".split(), cwd=path, check=True)
        subprocess.run("git commit -am \"Initial\"".split(), cwd=path, check=True)

        print(f"Created a new repo for project {name}. Please edit settings.ini and run nbdev_build_lib to get started.")
    except Exception as e:
        print("An error occured while copying nbdev project template:")
        print(e)
        if os.path.isdir(path): shutil.rmtree(path)