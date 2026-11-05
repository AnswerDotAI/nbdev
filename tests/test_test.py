from fastcore.nbio import new_nb, write_nb, mk_cell
from nbdev.test import nbdev_test


def test_fresh_process_per_notebook(tmp_path):
    "State one notebook leaves on an imported module never reaches the next, even on a single worker"
    write_nb(new_nb([mk_cell('import json\njson.leak = 1')]), tmp_path/'a.ipynb')
    write_nb(new_nb([mk_cell('import json\nassert not hasattr(json, "leak")')]), tmp_path/'b.ipynb')
    nbdev_test(path=tmp_path, n_workers=1)
