import os, re, shlex, subprocess, sys
from fastcore.nbio import new_nb, write_nb
from nbdev.diff_core import render_source_diff, source_diff


def test_source_changes():
    old = 'x=1\ny=2\nz=3\nk=4\n'
    new = 'x = 100\ny=2\nw=5\nq=6\n'
    result = render_source_diff(old, new)
    assert '!x{+ +}=[-1-]{+ 100+}' in result
    assert '-z=3\n-k=4\n+w=5\n+q=6' in result
    assert '+hello' in render_source_diff('', 'hello\n')
    assert '-hello' in render_source_diff('hello\n', '')
    assert not render_source_diff(old, old)


def test_long_line_changes():
    prefix = ' '.join(f'word{i}' for i in range(80))+' '
    tail = ' '.join(f'tail{i}' for i in range(80))
    old, new = prefix+'green '+tail+' old\n', prefix+'blue '+tail+' new\n'
    for color in (False, True):
        result = render_source_diff(old, new, maxlen=80, color=color)
        visible = re.sub(r'\x1b\[[\d;]*m', '', result)
        assert all(len(line)<=80 for line in visible.splitlines())
        assert 'green' in result and 'blue' in result and 'word0 ' not in result
        assert '…[' in result and ' new' not in result
        if color: assert '\x1b[31;9mgreen\x1b[0m' in result and '\x1b[32mblue\x1b[0m' in result
        else: assert '[-green-]{+blue+}' in result
    full = render_source_diff(old, new, maxlen=0)
    assert 'word0 ' in full and '[-old-]{+new+}' in full
    before,after = 'a'*22,'b'*22
    result = render_source_diff(prefix+before+' '+tail, prefix+after+' '+tail, maxlen=80)
    assert f'[-{before}-]{{+{after}+}}' in result


def test_final_newline():
    assert r'\ No newline at end of file' in source_diff('hello\n', 'hello')
    assert 'new file' in render_source_diff('hello\n', 'hello')
    assert 'old file' in render_source_diff('hello', 'hello\n')
    assert not render_source_diff('hello\n', 'hello', final_newline=False)


def test_git_driver(tmp_path):
    env = {**os.environ, 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1'}
    def git(*args):
        return subprocess.run(['git', *args], cwd=tmp_path, env=env, capture_output=True, text=True, check=True).stdout
    driver = tmp_path/'driver.py'
    driver.write_text('from nbdev.diff import nbdev_diff_driver\nnbdev_diff_driver()')
    git('init', '-q')
    git('config', 'user.name', 'nbdev')
    git('config', 'user.email', 'nbdev@fast.ai')
    git('config', 'diff.nbdev.command', shlex.join([sys.executable, str(driver), '--maxlen', '80']))
    (tmp_path/'.gitattributes').write_text('*.md diff=nbdev\n*.py diff=nbdev\n*.ipynb diff=nbdev\n')
    note, source = tmp_path/'note.md', tmp_path/'source.py'
    prefix = 'A notebook has words. '*20
    note.write_text(prefix+'This is a green notebook.\n')
    source.write_text('#| export\nx=1\n')
    nb_path = tmp_path/'demo.ipynb'
    nb = new_nb(['#| export\nx=1'])
    write_nb(nb, nb_path)
    git('add', '.')
    git('commit', '-qm', 'initial')
    note.write_text(prefix+'This is a blue notebook.\n')
    source.write_text('#| exports\nx=100\n')
    nb.cells[0].source = '#| export\nx=100'
    write_nb(nb, nb_path)
    result = git('diff')
    assert '[-green-]{+blue+}' in result
    assert all(len(line)<=80 for line in result.splitlines() if line.startswith('!'))
    assert '-#| export\n+#| exports' in result and '## modified' in result and '[export]' in result
    assert '[-1-]{+100+}' in result
    git('add', '.')
    git('commit', '-qm', 'edited')
    git('mv', 'note.md', 'renamed.md')
    git('update-index', '--chmod=+x', 'source.py')
    result = git('diff', '--cached', '--find-renames')
    assert 'note.md' in result and 'renamed.md' in result
    assert '100644' in result and '100755' in result
