import json, shutil, subprocess, pytest
from xml.etree import ElementTree as ET
from fastcore.test import test_eq as teq
from nbdev.quarto_render import render_quarto


@pytest.mark.skipif(not shutil.which('quarto'), reason='requires Quarto')
def test_website(tmp_path):
    root = tmp_path/'source'
    root.mkdir()
    (root/'_quarto.yml').write_text(r'''project:
  type: website
website:
  title: Parallel render
  site-url: https://example.com/
  sidebar:
    contents: [index.qmd, alpha.qmd, beta.qmd]
format:
  html: default
  commonmark: default
execute:
  enabled: false
''')
    for name in ('index', 'alpha', 'beta'):
        (root/f'{name}.qmd').write_text(fr'''---
title: {name}
---
## Detail

Page {name}. [Alpha](alpha.qmd#detail). [Download](data.txt).
''')
    (root/'data.txt').write_text('shared resource')
    serial, parallel = tmp_path/'serial', tmp_path/'parallel'
    render_quarto(root, serial, n_workers=1)
    render_quarto(root, parallel, n_workers=2)
    search = lambda d: {e['href']: e['text'] for e in json.loads((d/'search.json').read_text())}
    urls = lambda d: {e.text for e in ET.parse(d/'sitemap.xml').findall('.//{*}loc')}
    teq(search(serial), search(parallel))
    teq(urls(serial), urls(parallel))
    teq(len(urls(parallel)), 3)
    for name in ('index', 'alpha', 'beta'):
        html = (parallel/f'{name}.html').read_text()
        assert 'alpha.html#detail' in html and 'data.txt' in html
        assert (parallel/f'{name}.md').exists()
    teq((parallel/'data.txt').read_text(), 'shared resource')
    assert (parallel/'site_libs').is_dir()
    assert 'http-equiv="refresh"' not in (parallel/'index.html').read_text()
    (root/'beta.qmd').write_text('---\ntitle: beta\n---\n## Detail\n\nUpdated beta.')
    subprocess.run(['quarto', 'render', 'beta.qmd', '--quiet', '--output-dir', str(parallel)], cwd=root, check=True)
    teq(set(search(serial)), set(search(parallel)))
    assert 'Updated beta.' in search(parallel)['beta.html#detail']
    (root/'beta.qmd').write_text('---\nfilters: [missing.lua]\n---\nBroken.')
    with pytest.raises(RuntimeError, match='missing.lua'): render_quarto(root, parallel, n_workers=2)
    assert 'Updated beta.' in search(parallel)['beta.html#detail']
