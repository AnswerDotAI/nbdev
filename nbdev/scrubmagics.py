"""Scrub Jupyter magics from exported code"""

__all__ = ['scrub_magics']

import re

_magics_pattern = re.compile(r'^\s*(%%|%).*\n?', re.MULTILINE)

def scrub_magics(cell):
    "Remove Jupyter magic lines (e.g. %%time, %matplotlib) from exported code cells"
    if cell.cell_type != 'code': return
    try: cell.source = _magics_pattern.sub('', cell.source)
    except: pass
