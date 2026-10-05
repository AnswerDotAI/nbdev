r"Pandoc filter for README documentation links."

from fastcore.utils import *
from fastcore.script import *
from nbdev.config import *
from urllib.parse import urlsplit, urlunsplit, urljoin


def doc_link(target, base, nbdir='.'):
    "Convert a relative documentation link to its hosted URL."
    u = urlsplit(target)
    p = Path(u.path)
    if u.scheme or u.netloc or p.suffix not in ('.ipynb', '.qmd', '.html', '.txt'): return target
    if p.suffix=='.ipynb': p = nbpath2html(p)
    elif p.suffix=='.qmd': p = p.with_suffix('.html')
    path = urljoin(nbdir.rstrip('/')+'/', p.as_posix()).lstrip('/')
    return urljoin(base.rstrip('/')+'/', urlunsplit(('', '', path, u.query, u.fragment)))


def rewrite_links(node, base, nbdir='.'):
    "Rewrite documentation links in a Pandoc syntax tree."
    if isinstance(node, list):
        for item in node: rewrite_links(item, base, nbdir)
    elif isinstance(node, dict):
        if node.get('t')=='Link': node['c'][2][0] = doc_link(node['c'][2][0], base, nbdir)
        for item in node.values(): rewrite_links(item, base, nbdir)


@call_parse
def main(
    fmt:str, # Output format supplied by Pandoc
):
    "Rewrite documentation links in Pandoc JSON from stdin."
    cfg,doc = get_config(),loads(sys.stdin.read())
    rewrite_links(doc['blocks'], cfg.doc_url, Path(cfg.readme_nb).parent.as_posix())
    print(dumps(doc))
