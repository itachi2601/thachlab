#!/usr/bin/env python3
"""Tách phần trắc nghiệm ABCD của md/<c>.md (pandoc từ Word VnTeach VL12) -> cau-tho/<c>-abcd.json.
Đáp án = phương án nằm trong [...]{.mark} (tô vàng). Không LLM; câu không tách sạch thì gắn flag.
  VL12_DIR=scripts/data/nap-ngan-hang-vl12/c1 python3 parse12.py c1 <dòng-đầu> <dòng-cuối>
Đầu ra cùng định dạng cau-tho của VL10 (part=mc, options=[[L,text,marked]]) để dung-cau.py dùng lại được."""
import json, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nap-ngan-hang-vl10'))
from parse import clean_math, tidy

HERE = os.environ.get('VL12_DIR') or os.getcwd()
Q = re.compile(r'\*\*\s*Câu\s*(\d+)\s*[:.]?\s*(?:\([^)]*\))?\s*\*\*\s*[:.]?\s*')
HEAD = re.compile(r'^\s*#')
M_OPEN, M_CLOSE = '⟦M', 'M⟧'

def mark(s):
    """[...]{.mark} -> ⟦M...M⟧ (lồng ngoặc vuông: tìm ngược từ }{.mark})."""
    out = s
    while True:
        i = out.find(']{.mark}')
        if i < 0: break
        depth, j = 0, i - 1
        while j >= 0:
            c = out[j]
            if c == ']': depth += 1
            elif c == '[':
                if depth == 0: break
                depth -= 1
            j -= 1
        if j < 0: out = out.replace(']{.mark}', M_CLOSE, 1); continue
        out = out[:j] + M_OPEN + out[j + 1:i] + M_CLOSE + out[i + len(']{.mark}'):]
    return out

OPT = re.compile(r'(?:(?<=^)|(?<=[\s⟦]))(?:M)?(?:\*\*)?([ABCD])\.(?:\*\*)?(?=\s|$)')

def split_options(t):
    t = re.sub(r'(?m)^[>\s]+', '', t)
    t = t.replace('⟦M', ' ⟦M').replace('M⟧', 'M⟧ ')
    pos, cur = [], 0
    for L in 'ABCD':
        f = None
        for m in re.finditer(r'(?:^|(?<=[\s⟦M]))(?:\*\*)?' + L + r'\.(?:\*\*)?(?=\s|$|M⟧)', t[cur:], flags=re.M):
            f = m; break
        if not f: return t, [], ['khong-du-A-D']
        pos.append((cur + f.start(), cur + f.end())); cur = cur + f.end()
    stem = t[:pos[0][0]]
    opts = []
    for i, (a, b) in enumerate(pos):
        end = pos[i + 1][0] if i < 3 else len(t)
        body = t[b:end]
        marked = M_CLOSE in body  # đóng ⟧ luôn nằm trong phương án được tô; ⟦ mở có thể rơi ở cuối phương án trước
        opts.append([ 'ABCD'[i], body, marked])
    return stem, opts, []

def unmark(s):
    return s.replace(M_OPEN, '').replace(M_CLOSE, '')

def parse(name, a, b):
    import unicodedata
    lines = unicodedata.normalize('NFC', open(os.path.join(HERE, 'md', name + '.md'), encoding='utf8').read()).split('\n')[a - 1:b]
    blocks, cur = [], None
    for ln in lines:
        if HEAD.match(ln) and not Q.search(ln):
            cur = None; continue
        ms = list(Q.finditer(ln))
        if ms:
            if cur is not None and ms[0].start() > 0: cur['raw'].append(ln[:ms[0].start()])
            cur = {'num': int(ms[0].group(1)), 'raw': [ln[ms[0].end():]]}
            blocks.append(cur)
            continue
        if cur is not None: cur['raw'].append(ln)
    out = []
    for blk in blocks:
        raw = mark('\n'.join(blk['raw']))
        flags = []
        hd = re.search(r'(?m)^[>\s]*\**\s*(?:Hướng dẫn|Lời giải|Giải)\b', raw)
        chon = None
        if hd:
            lg = raw[hd.start():]; raw = raw[:hd.start()]
            mc = re.search(r'Chọn\s*\**\s*([ABCD])\b', lg)
            chon = mc.group(1) if mc else None
        stem, opts, fl = split_options(raw); flags += fl
        item = {'file': name, 'part': 'mc', 'num': blk['num'], 'flags': flags}
        item['stem'] = clean_math(tidy(unmark(stem)))
        item['options'] = [[l, clean_math(tidy(unmark(tx))), m] for l, tx, m in opts]
        ans = [l for l, tx, m in opts if m]
        if not ans: flags.append('khong-gach-chan')
        elif len(ans) > 1: flags.append('nhieu-gach-chan')
        item['answer'] = ans[0] if len(ans) == 1 else None
        item['chon'] = chon
        if not ans and chon: item['answer'] = chon; flags.remove('khong-gach-chan'); flags.append('dap-an-chon')
        item['solution'] = ''
        if re.search(r'!\[', raw): flags.append('co-hinh')
        if 'Hướng dẫn' in raw or 'Lời giải' in raw: flags.append('co-loi-giai-trong-de')
        item['hasImg'] = bool(re.search(r'!\[', raw))
        item['imgs'] = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', raw)
        out.append(item)
    return out

if __name__ == '__main__':
    name, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    items = parse(name, a, b)
    os.makedirs(os.path.join(HERE, 'cau-tho'), exist_ok=True)
    json.dump(items, open(os.path.join(HERE, 'cau-tho', name + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(name, len(items), dict(Counter(x for i in items for x in i['flags'])))
