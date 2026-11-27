"Word-level terminal diffs of plain text, shared by file and notebook rendering."

from fastcore.diff import MIN_RATIO, diff_lines
from fastcore.utils import *

__all__ = ['MAXLEN', 'truncate', 'render_line', 'render_source_diff']

MAXLEN = 180 # Most visible characters per displayed line; 0 means unlimited
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
    rows = diff_lines(old_source, new_source, context=context, final_newline=final_newline, min_ratio=MIN_RATIO)
    if not rows: return ''
    res = [_render_spans(spans, maxlen, color) if kind=='!' else render_line(kind+''.join(t for _,t in spans), maxlen, color)
           for kind,spans in rows]
    if final_newline:
        for name,text in (('old',old_source), ('new',new_source)):
            if text and not text.endswith('\n'): res.append(render_line(fr'\ No newline at end of {name} file', maxlen, color))
    return '\n'.join(res)
