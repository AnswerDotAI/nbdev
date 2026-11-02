"Word-level terminal diffs of plain text, shared by file and notebook rendering."

from difflib import unified_diff, SequenceMatcher
from fastcore.utils import *

__all__ = ['MAXLEN', 'MIN_RATIO', 'truncate', 'render_line', 'source_diff', 'render_source_diff']

MAXLEN = 180 # Most visible characters per displayed line; 0 means unlimited
MIN_RATIO = 0.5 # Minimum shared-word similarity for merging a changed line pair
_dcolors = {'## …':'\x1b[34m', '# ':'\x1b[1;7m', '#':'\x1b[1m', '-':'\x1b[31m', '+':'\x1b[32m', '@':'\x1b[36m'}
_wcolors = {'-':'\x1b[31;9m', '+':'\x1b[32m'}
_wmarks = {'-':('[-','-]'), '+':('{+','+}')}


def truncate(s, maxlen):
    "Cut `s` to `maxlen`, marking the number of omitted characters; 0 means unlimited."
    if not maxlen or len(s)<=maxlen: return s
    return truncstr(s, maxlen, suf=lambda n: f'…[{humanize(n)}]')[:maxlen]


def render_line(
    line, # A display line, including its diff or heading marker
    maxlen=MAXLEN, # Maximum visible length; 0 means unlimited
    color=False # Add ANSI colors?
):
    "Truncate and optionally color a line by its leading display marker."
    line = truncate(line, maxlen)
    c = next((v for k,v in _dcolors.items() if line.startswith(k)), '') if color else ''
    return f'{c}{line}\x1b[0m' if c else line


def _source_lines(old, new, context, final_newline):
    def lines(s): return s.splitlines(keepends=True) if final_newline else [l+'\n' for l in s.splitlines()]
    return list(unified_diff(lines(old), lines(new), n=context))


def source_diff(
    old_source, # Original source string
    new_source, # New source string
    context=3, # Unchanged lines shown either side of a change
    final_newline=True # Distinguish a missing final newline (unnecessary for notebook cells)?
):
    "Unified source diff, including missing-final-newline markers."
    lines = _source_lines(old_source, new_source, context, final_newline)
    return '\n'.join(l.removesuffix('\n') + ('' if l.endswith('\n') else '\n\\ No newline at end of file') for l in lines)


def _word_diff(a, b):
    if a==b: return None
    if SequenceMatcher(None, re.findall(r'\w+', a), re.findall(r'\w+', b), autojunk=False).ratio()<MIN_RATIO: return None
    ta,tb = (re.findall(r'\w+|\s+|[^\w\s]', s) for s in (a,b))
    res = []
    for tag,i1,i2,j1,j2 in SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if tag=='equal': res.append((' ', ''.join(ta[i1:i2])))
        else:
            if i2>i1: res.append(('-', ''.join(ta[i1:i2])))
            if j2>j1: res.append(('+', ''.join(tb[j1:j2])))
    return res


def _refine(lines):
    res,i = [],0
    while i<len(lines):
        if not lines[i].startswith('-'):
            res.append(lines[i])
            i += 1
            continue
        j = i
        while j<len(lines) and lines[j].startswith('-'): j += 1
        k = j
        while k<len(lines) and lines[k].startswith('+'): k += 1
        olds,news = lines[i:j],lines[j:k]
        bo,bn = [],[]
        for o,n in zip(olds,news):
            w = _word_diff(o[1:], n[1:])
            if w: res,bo,bn = res+bo+bn+[w],[],[]
            else: bo,bn = bo+[o],bn+[n]
        res += bo+olds[len(news):]+bn+news[len(olds):]
        i = k
    return res


def _slice_spans(spans, start, end):
    res,pos = [],0
    for k,t in spans:
        a,b = max(0,start-pos), min(len(t),end-pos)
        if a<b: res.append((k,t[a:b]))
        pos += len(t)
        if pos>=end: break
    return res


def _span_width(spans, color): return sum(len(t)+(4 if k!=' ' and not color else 0) for k,t in spans)


def _render_spans(spans, maxlen, color):
    total = sum(len(t) for _,t in spans)
    start,end = 0,total
    if maxlen and _span_width(spans, color)+1>maxlen:
        first = int(spans[0][0]==' ')
        prefix = len(spans[0][1]) if first else 0
        last = first
        while last<len(spans) and spans[last][0]!=' ': last += 1
        room = maxlen-1-_span_width(spans[first:last], color)-2*len(f'…[{total}]')
        start = max(0,prefix-min(20,maxlen//4,max(0,room)))
        end = min(total,start+maxlen-1)
        while True:
            shown = _slice_spans(spans, start, end)
            head,tail = (f'…[{start}]' if start else ''), (f'…[{total-end}]' if end<total else '')
            excess = 1+len(head)+_span_width(shown, color)+len(tail)-maxlen
            if excess<=0: break
            if end==start: return truncate('!'+head+tail, maxlen)
            end = max(start,end-excess)
    else: shown,head,tail = spans,'',''
    def fmt(k,t):
        if k==' ': return t
        if color: return f'{_wcolors[k]}{t}\x1b[0m'
        return _wmarks[k][0]+t+_wmarks[k][1]
    return '!'+head+''.join(fmt(k,t) for k,t in shown)+tail


def render_source_diff(
    old_source, # Original source string
    new_source, # New source string
    maxlen=MAXLEN, # Maximum visible length; 0 means unlimited
    color=False, # Add ANSI colors instead of [-removed-]/{+added+} markers?
    context=3, # Unchanged lines shown either side of a change
    final_newline=True # Distinguish a missing final newline (unnecessary for notebook cells)?
):
    "Render source changes, cropping long word-diff lines around the first change."
    lines = _source_lines(old_source, new_source, context, final_newline)
    if not lines: return ''
    body = [l.removesuffix('\n') for l in lines[2:]]
    res = [render_line(l, maxlen, color) if isinstance(l,str) else _render_spans(l, maxlen, color) for l in _refine(body)]
    if final_newline:
        for name,text in (('old',old_source), ('new',new_source)):
            if text and not text.endswith('\n'): res.append(render_line(fr'\ No newline at end of {name} file', maxlen, color))
    return '\n'.join(res)
