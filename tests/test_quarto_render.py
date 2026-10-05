import json, shutil, subprocess, pytest
from xml.etree import ElementTree as ET
from fastcore.test import test_eq as teq
from nbdev.quarto_render import render_quarto
from nbdev.quarto import nbdev_readme, refresh_quarto_yml
from nbdev.readme_filter import doc_link
from fastcore.nbio import new_nb, mk_cell, write_nb


@pytest.mark.skipif(not shutil.which('quarto'), reason='requires Quarto')
def test_readme_links(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path/'pyproject.toml').write_text(r'''[project]
name = "example"
[project.urls]
Documentation = "https://example.com/project/"
[tool.nbdev]
''')
    nbs = tmp_path/'nbs'
    nbs.mkdir()
    base = 'https://example.com/project/'
    links = [('guide/01_Intro.ipynb?q=1#intro', base+'guide/intro.html?q=1#intro'),
        ('guide/02_intro.qmd', base+'guide/02_intro.html'), ('guide/intro.html', base+'guide/intro.html'),
        ('/llms.txt', base+'llms.txt'), ('llms-ctx.txt', base+'llms-ctx.txt'),
        ('https://other.com/guide.html', 'https://other.com/guide.html'),
        ('#section', '#section'), ('LICENSE', 'LICENSE')]
    text = '\n\n'.join([*(f'[Link]({src})' for src,_ in links),
        r'[Reference][guide] ![Image](image.png)', r'[guide]: guide/01_Intro.ipynb#intro',
        '```markdown\n[Example](guide/01_Intro.ipynb)\n```'])
    write_nb(new_nb([mk_cell('# Example', 'markdown'), mk_cell(text, 'markdown')]), nbs/'index.ipynb')
    refresh_quarto_yml()
    nbdev_readme.__wrapped__()
    result = (tmp_path/'README.md').read_text()
    for _,dest in links: assert f']({dest})' in result
    assert f'[Reference]({base}guide/intro.html#intro)' in result
    assert '![Image](image.png)' in result and '[Example](guide/01_Intro.ipynb)' in result
    teq(doc_link('../guide/01_intro.ipynb', base, 'start'), base+'guide/intro.html')
    teq(doc_link('/llms.txt', base, 'start'), base+'llms.txt')
    teq(doc_link('//other.com/llms.txt', base), '//other.com/llms.txt')


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
