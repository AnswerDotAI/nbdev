import os
from execnb.nbio import write_nb
from execnb.shell import CaptureShell
from nbdev.process import read_nb, read_qmd
from io import StringIO
from contextlib import redirect_stdout
from fastcore.foundation import working_directory
from nbdev.test import no_eval
from nbdev.config import get_config
    
def exec_scr(src, dst, md):
    f = StringIO()
    g = {}
    with redirect_stdout(f): exec(compile(src.read_text(), src, 'exec'), g)
    res = ""
    if md: res += "---\n" + md + "\n---\n\n"
    dst.write_text(res + f.getvalue())
    
def exec_qmd(src, dst, cb):
    nb = read_qmd(src)
    k = CaptureShell()
    with working_directory(src.parent): k.run_all(nb, exc_stop=False, preproc=no_eval)
    cb()(nb)
    write_nb(nb, dst.with_suffix(".ipynb"))

def exec_nb(src, dst, cb):
    nb = read_nb(src)
    cb()(nb)
    write_nb(nb, dst)

def main(o):
    src,dst,x = o
    os.environ["IN_TEST"] = "1"
    if src.suffix=='.ipynb': exec_nb(src, dst, x)
    elif src.suffix=='.qmd': exec_qmd(src, dst, x)
    elif src.suffix=='.py': exec_scr(src, dst, x)
    else: raise Exception(src)
    del os.environ["IN_TEST"]

