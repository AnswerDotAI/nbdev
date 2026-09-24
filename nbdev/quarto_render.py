"Parallel Quarto website rendering in isolated project copies."

import json, shutil, subprocess, tempfile
from pathlib import Path
from xml.etree import ElementTree as ET
from fastcore.parallel import parallel
from fastcore.utils import defaults


def _quarto(path, *args):
    res = subprocess.run(['quarto', *map(str, args)], cwd=path, capture_output=True, text=True)
    if res.returncode: raise RuntimeError(res.stderr or res.stdout or f'Quarto exited with status {res.returncode}')
    return res.stdout


def _render_batch(job):
    path, inputs, output = job
    _quarto(path, 'render', *inputs, '--no-cache', '--no-clean', '--output-dir', output)
    return output


def _merge_site(outputs, dest):
    search, urls, homepage = {}, {}, None
    sitemap = None
    for output in outputs:
        idx = output/'index.html'
        if idx.exists() and (homepage is None or 'http-equiv="refresh"' not in idx.read_text()): homepage = idx
        if (output/'search.json').exists():
            for entry in json.loads((output/'search.json').read_text()): search[entry['href']] = entry
        if (output/'sitemap.xml').exists():
            sitemap = ET.parse(output/'sitemap.xml')
            for entry in sitemap.getroot(): urls[entry.find('{*}loc').text] = entry
        shutil.copytree(output, dest, dirs_exist_ok=True)
    if homepage: shutil.copy2(homepage, dest/'index.html')
    if search: (dest/'search.json').write_text(json.dumps(list(search.values())))
    if sitemap is not None:
        sitemap.getroot()[:] = urls.values()
        ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        sitemap.write(dest/'sitemap.xml', encoding='utf-8', xml_declaration=True)


def render_quarto(path, output_dir, n_workers=defaults.cpus):
    "Render a project, parallelizing website pages with isolated Quarto workers."
    path, output_dir = Path(path).resolve(), Path(output_dir).resolve()
    if output_dir == path or output_dir in path.parents: raise ValueError('Output directory must not contain the project')
    if n_workers <= 1:
        _quarto(path, 'render', '--no-cache', '--output-dir', output_dir)
        return
    info = json.loads(_quarto(path, 'inspect'))
    project = info['config']['project']
    website = info['config'].get('website', {})
    if project['type'] != 'website' or project.get('pre-render') or project.get('post-render') or website.get('llms-txt'):
        return render_quarto(path, output_dir, n_workers=1)
    inputs = [str(Path(p).relative_to(path)) for p in info['files']['input']]
    if len(inputs) < 2: return render_quarto(path, output_dir, n_workers=1)
    n_workers = min(n_workers, len(inputs))
    print(f'Rendering {len(inputs)} pages with {n_workers} Quarto workers')
    excluded = {path/'.quarto', (path/project.get('output-dir', '_site')).resolve(), output_dir}
    def ignore(src, names): return [n for n in names if Path(src)/n in excluded]
    with tempfile.TemporaryDirectory(prefix='nbdev-quarto-') as tmp:
        jobs = []
        for i in range(n_workers):
            worker = Path(tmp)/str(i)
            shutil.copytree(path, worker, ignore=ignore)
            jobs.append((worker, inputs[i::n_workers], Path(tmp)/f'output-{i}'))
        outputs = parallel(_render_batch, jobs, n_workers=n_workers, threadpool=True)
        merged = Path(tmp)/'merged'
        _merge_site(outputs, merged)
        if output_dir.exists(): shutil.rmtree(output_dir)
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(merged, output_dir)
