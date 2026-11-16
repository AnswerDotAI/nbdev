import os
from fastcore.nbio import read_nb,write_nb
from nbdev.doclinks import NbdevLookup
from nbdev.frontmatter import _re_fm_md
from io import StringIO
from contextlib import redirect_stdout

def link_qmd(text):
    "Linkify a Quarto document without changing its YAML frontmatter."
    fm = _re_fm_md.match(text)
    start = fm.end() if fm else 0
    return text[:start] + NbdevLookup().linkify(text[start:])

def exec_scr(src, dst, md):
    f = StringIO()
    g = {}
    with redirect_stdout(f): exec(compile(src.read_text(), src, 'exec'), g)
    res = ""
    if md: res += "---\n" + md + "\n---\n\n"
    text = res + f.getvalue()
    dst.write_text(link_qmd(text) if dst.suffix=='.qmd' else text)

def exec_nb(src, dst, cb):
    nb = read_nb(src)
    cb()(nb)
    write_nb(nb, dst)

def main(o):
    src,dst,x = o
    os.environ["IN_TEST"] = "1"
    if src.suffix=='.ipynb': exec_nb(src, dst, x)
    elif src.suffix=='.py': exec_scr(src, dst, x)
    elif src.suffix=='.qmd': dst.write_text(link_qmd(src.read_text()))
    else: raise Exception(src)
    del os.environ["IN_TEST"]

