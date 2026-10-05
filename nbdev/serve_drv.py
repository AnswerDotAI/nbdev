import os
from fastcore.nbio import read_nb,nb2str
from io import StringIO
from contextlib import redirect_stdout

def exec_scr(src, dst, md):
    f = StringIO()
    g = {}
    with redirect_stdout(f): exec(compile(src.read_text(encoding='utf-8'), src, 'exec'), g)
    res = ""
    if md: res += "---\n" + md + "\n---\n\n"
    dst.write_text(res + f.getvalue(), encoding='utf-8', newline='\n')

def exec_nb(src, dst, cb):
    nb = read_nb(src)
    cb()(nb)
    dst.write_text(nb2str(nb), encoding='utf-8', newline='\n')

def main(o):
    src,dst,x = o
    os.environ["IN_TEST"] = "1"
    if src.suffix=='.ipynb': exec_nb(src, dst, x)
    elif src.suffix=='.py': exec_scr(src, dst, x)
    else: raise Exception(src)
    del os.environ["IN_TEST"]

