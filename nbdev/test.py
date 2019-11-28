#AUTOGENERATED! DO NOT EDIT! File to edit: dev/04_test.ipynb (unless otherwise specified).

__all__ = ['check_all_flag', 'get_cell_flags', 'NoExportPreprocessor', 'test_nb']

#Cell
from .imports import *
from .sync import *
from .export import *

from nbconvert.preprocessors import ExecutePreprocessor

#Cell
_re_all_flag = re.compile("""
# Matches any line with #all_something and catches that something in a group:
^         # beginning of line (since re.MULTILINE is passed)
\s*       # any number of whitespace
\#\s*     # # then any number of whitespace
all_(\S+) # all_ followed by a group with any non-whitespace chars
\s*       # any number of whitespace
$         # end of line (since re.MULTILINE is passed)
""", re.IGNORECASE | re.MULTILINE | re.VERBOSE)

#Cell
def check_all_flag(cells):
    "Check for an `# all_flag` cell and then return said flag"
    for cell in cells:
        if check_re(cell, _re_all_flag): return check_re(cell, _re_all_flag).groups()[0]

#Cell
_re_flags = re.compile(f"""
# Matches any line with a test flad and catches it in a group:
^               # beginning of line (since re.MULTILINE is passed)
\s*             # any number of whitespace
\#\s*           # # then any number of whitespace
({Config().get('tst_flags', '')})
\s*             # any number of whitespace
$               # end of line (since re.MULTILINE is passed)
""", re.IGNORECASE | re.MULTILINE | re.VERBOSE)

#Cell
def get_cell_flags(cell):
    "Check for any special test flag in `cell`"
    if cell['cell_type'] != 'code' or len(Config().get('tst_flags',''))==0: return []
    return _re_flags.findall(cell['source'])

#Cell
class NoExportPreprocessor(ExecutePreprocessor):
    "An `ExecutePreprocessor` that executes cells that are not exported and don't have a flag in `flags`"
    def __init__(self, flags, **kwargs):
        self.flags = flags
        super().__init__(**kwargs)

    def preprocess_cell(self, cell, resources, index):
        if 'source' not in cell or cell['cell_type'] != "code": return cell, resources
        for f in get_cell_flags(cell):
            if f not in self.flags:  return cell, resources
        res = super().preprocess_cell(cell, resources, index)
        return res

#Cell
def test_nb(fn, flags=None):
    "Execute tests in notebook in `fn` with `flags`"
    os.environ["IN_TEST"] = '1'
    if flags is None: flags = []
    try:
        nb = read_nb(fn)
        all_flag = check_all_flag(nb['cells'])
        if all_flag is not None and all_flag not in flags: return
        mod = find_default_export(nb['cells'])
        ep = NoExportPreprocessor(flags, timeout=600, kernel_name='python3')
        pnb = nbformat.from_dict(nb)
        ep.preprocess(pnb)
    finally: os.environ.pop("IN_TEST")