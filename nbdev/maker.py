# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/maker.ipynb.

# %% ../nbs/api/maker.ipynb 1
#|export
from __future__ import annotations

# %% auto 0
__all__ = ['find_var', 'read_var', 'update_var', 'ModuleMaker', 'decor_id', 'make_code_cells', 'relative_import', 'update_import']

# %% ../nbs/api/maker.ipynb 3
#|export
from .config import *
from .imports import *

from fastcore.script import *
from fastcore.basics import *
from fastcore.imports import *
from execnb.nbio import *

import ast,contextlib

from collections import defaultdict
from pprint import pformat
from textwrap import TextWrapper

# %% ../nbs/api/maker.ipynb 8
#|export
def find_var(lines, varname):
    "Find the line numbers where `varname` is defined in `lines`"
    start = first(i for i,o in enumerate(lines) if o.startswith(varname))
    if start is None: return None,None
    empty = ' ','\t'
    if start==len(lines)-1 or lines[start+1][:1] not in empty: return start,start+1
    end = first(i for i,o in enumerate(lines[start+1:]) if o[:1] not in empty)
    return start,len(lines) if end is None else (end+start+1)

# %% ../nbs/api/maker.ipynb 10
#|export
def read_var(code, varname):
    "Eval and return the value of `varname` defined in `code`"
    lines = code.splitlines()
    start,end = find_var(lines, varname)
    if start is None: return None
    res = [lines[start].split('=')[-1].strip()]
    res += lines[start+1:end]
    try: return eval('\n'.join(res))
    except SyntaxError: raise Exception('\n'.join(res)) from None

# %% ../nbs/api/maker.ipynb 12
#|export
def update_var(varname, func, fn=None, code=None):
    "Update the definition of `varname` in file `fn`, by calling `func` with the current definition"
    if fn:
        fn = Path(fn)
        code = fn.read_text()
    lines = code.splitlines()
    v = read_var(code, varname)
    res = func(v)
    start,end = find_var(lines, varname)
    del(lines[start:end])
    lines.insert(start, f"{varname} = {res}")
    code = '\n'.join(lines)
    if fn: fn.write_text(code)
    else: return code

# %% ../nbs/api/maker.ipynb 15
#|export
class ModuleMaker:
    "Helper class to create exported library from notebook source cells"
    def __init__(self, dest, name, nb_path, is_new=True, parse=True):
        dest,nb_path = Path(dest),Path(nb_path)
        store_attr()
        self.fname = dest/(name.replace('.','/') + ".py")
        if is_new: dest.mkdir(parents=True, exist_ok=True)
        else: assert self.fname.exists(), f"{self.fname} does not exist"
        self.dest2nb = nb_path.relpath(self.fname.parent).as_posix()
        self.hdr = f"# %% {self.dest2nb}"

# %% ../nbs/api/maker.ipynb 18
#|export
def decor_id(d):
    "`id` attr of decorator, regardless of whether called as function or bare"
    return d.id if hasattr(d, 'id') else nested_attr(d, 'func.id', '')

# %% ../nbs/api/maker.ipynb 19
#|export
_def_types = ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef
_assign_types = ast.AnnAssign, ast.Assign, ast.AugAssign

def _val_or_id(it): 
    if sys.version_info < (3,8): return [getattr(o, 's', getattr(o, 'id', None)) for o in it.value.elts]
    else:return [getattr(o, 'value', getattr(o, 'id', None)) for o in it.value.elts]
def _all_targets(a): return L(getattr(a,'elts',a))
def _filt_dec(x): return decor_id(x).startswith('patch')
def _wants(o): return isinstance(o,_def_types) and not any(L(o.decorator_list).filter(_filt_dec))

# %% ../nbs/api/maker.ipynb 20
#|export

def _targets(o): return [o.target] if isinstance(o, ast.AnnAssign) else o.targets

@patch
def make_all(self:ModuleMaker, cells):
    "Create `__all__` with all exports in `cells`"
    if cells is None: return ''
    trees = L(cells).map(NbCell.parsed_).concat()
    # include anything mentioned in "_all_", even if otherwise private
    # NB: "_all_" can include strings (names), or symbols, so we look for "id" or "value"
    assigns = trees.filter(risinstance(_assign_types))
    all_assigns = assigns.filter(lambda o: getattr(_targets(o)[0],'id',None)=='_all_')
    all_vals = all_assigns.map(_val_or_id).concat()
    syms = trees.filter(_wants).attrgot('name')
    # assignment targets (NB: can be multiple, e.g. "a=b=c", and/or destructuring e.g "a,b=(1,2)")
    assign_targs = L(L(_targets(assn)).map(_all_targets).concat() for assn in assigns).concat()
    exports = (assign_targs.attrgot('id')+syms).filter(lambda o: o and o[0]!='_')
    return (exports+all_vals).unique()

# %% ../nbs/api/maker.ipynb 21
#|export
def make_code_cells(*ss): return dict2nb({'cells':L(ss).map(mk_cell)}).cells

# %% ../nbs/api/maker.ipynb 24
#|export
def relative_import(name, fname, level=0):
    "Convert a module `name` to a name relative to `fname`"
    assert not level
    sname = name.replace('.','/')
    if not(os.path.commonpath([sname,fname])): return name
    rel = os.path.relpath(sname, fname)
    if rel==".": return "."
    res = rel.replace(f"..{os.path.sep}", ".")
    if not all(o=='.' for o in res): res='.'+res
    return res.replace(os.path.sep, ".")

# %% ../nbs/api/maker.ipynb 26
#|export
# Based on https://github.com/thonny/thonny/blob/master/thonny/ast_utils.py
def _mark_text_ranges(
    source: str|bytes, # Source code to add ranges to
):
    "Adds `end_lineno` and `end_col_offset` to each `node` recursively. Used for Python 3.7 compatibility"
    from asttokens.asttokens import ASTTokens
    # We need to reparse the source to get a full tree to walk
    root = ast.parse(source)
    ASTTokens(source, tree=root)
    for child in ast.walk(root):
        if hasattr(child,"last_token"):
            child.end_lineno,child.end_col_offset = child.last_token.end
        # Some tokens stay without end info
        if hasattr(child,"lineno") and (not hasattrs(child, ["end_lineno","end_col_offset"])):
            child.end_lineno, child.end_col_offset = child.lineno, child.col_offset+2
    return root.body

# %% ../nbs/api/maker.ipynb 27
#|export
def update_import(source, tree, libname, f=relative_import):
    if not tree: return
    if sys.version_info < (3,8): tree = _mark_text_ranges(source)
    imps = L(tree).filter(risinstance(ast.ImportFrom))
    if not imps: return
    src = source.splitlines(True)
    for imp in imps:
        nmod = f(imp.module, libname, imp.level)
        lin = imp.lineno-1
        sec = src[lin][imp.col_offset:imp.end_col_offset]
        newsec = re.sub(f"(from +){'.'*imp.level}{imp.module or ''}", fr"\1{nmod}", sec)
        src[lin] = src[lin].replace(sec,newsec)
    return src

@patch
def import2relative(cell:NbCell, libname):
    src = update_import(cell.source, cell.parsed_(), libname)
    if src: cell.set_source(src)

# %% ../nbs/api/maker.ipynb 29
#|export
@patch
def _last_future(self:ModuleMaker, cells):
    "Returns the location of a `__future__` in `cells`"
    trees = cells.map(NbCell.parsed_)
    try: return max(i for i,tree in enumerate(trees) if tree and any(
         isinstance(t,ast.ImportFrom) and t.module=='__future__' for t in tree))+1
    except ValueError: return 0

# %% ../nbs/api/maker.ipynb 30
#|export
def _import2relative(cells, lib_name=None):
    "Converts `cells` to use `import2relative` based on `lib_name`"
    if lib_name is None: lib_name = get_config().lib_name
    for cell in cells: cell.import2relative(lib_name)

# %% ../nbs/api/maker.ipynb 31
#|export
def _retr_mdoc(cells):
    "Search for `_doc_` variable, used to create module docstring"
    trees = L(cells).map(NbCell.parsed_).concat()
    for o in trees:
        if isinstance(o, _assign_types) and getattr(_targets(o)[0],'id',None)=='_doc_':
            v = try_attrs(o.value, 'value', 's') # py37 uses `ast.Str.s`
            return f'"""{v}"""\n\n' 
    return ""

# %% ../nbs/api/maker.ipynb 33
#|export
@patch
def make(self:ModuleMaker, cells, all_cells=None, lib_path=None):
    "Write module containing `cells` with `__all__` generated from `all_cells`"
    config = get_config()
    if all_cells is None: all_cells = cells
    cells,all_cells = L(cells),L(all_cells)
    if self.parse: 
        if not lib_path: lib_path = config.lib_path
        mod_dir = os.path.relpath(self.fname.parent, Path(lib_path).parent)
        _import2relative(all_cells, mod_dir)
    if not self.is_new: return self._make_exists(cells, all_cells)

    self.fname.parent.mkdir(exist_ok=True, parents=True)
    last_future = 0
    if self.parse:
        _all = self.make_all(all_cells)
        last_future = self._last_future(cells) if len(all_cells)>0 else 0
        width = int(config.lib_max_width)
        tw = TextWrapper(
            width=width, initial_indent='', subsequent_indent=' '*11, break_long_words=False
        )
        all_str = '\n'.join(tw.wrap(str(_all)))
    with self.fname.open('w') as f:
        f.write(_retr_mdoc(cells))
        f.write(f"# AUTOGENERATED! DO NOT EDIT! File to edit: {self.dest2nb}.")
        if last_future > 0: write_cells(cells[:last_future], self.hdr, f)
        if self.parse: f.write(f"\n\n# %% auto 0\n__all__ = {all_str}")
        write_cells(cells[last_future:], self.hdr, f)
        f.write('\n')

# %% ../nbs/api/maker.ipynb 38
#|export
@patch
def _update_all(self:ModuleMaker, all_cells, alls):
    return pformat(alls + self.make_all(all_cells), width=160)

@patch
def _make_exists(self:ModuleMaker, cells, all_cells=None):
    "`make` for `is_new=False`"
    if all_cells and self.parse:
        update_var('__all__', partial(self._update_all, all_cells), fn=self.fname)
    with self.fname.open('a') as f: write_cells(cells, self.hdr, f)

# %% ../nbs/api/maker.ipynb 44
#|export
def _basic_export_nb2(fname, name, dest=None):
    "A basic exporter to bootstrap nbdev using `ModuleMaker`"
    if dest is None: dest = get_config().lib_path
    cells = L(c for c in read_nb(fname).cells if re.match(r'#\|\s*export', c.source))
    ModuleMaker(dest=dest, name=name, nb_path=fname).make(cells)
