#!/usr/bin/env python3
"""Tách câu Đúng–Sai a)–d) của md/<c>.md -> cau-tho/<tên>.json (part='tf', statements=[[l,text,'Đ'|'S']]).
Đáp án lấy từ phần Hướng dẫn ("a) Đúng; b) Sai"); nếu có tô vàng ({.mark}) trên mệnh đề thì đối chiếu, lệch -> flag.
  VL12_DIR=.../c1 python3 parse12ds.py c1 <dòng-đầu> <dòng-cuối> [tên-file-ra]"""
import json, re, sys, os, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nap-ngan-hang-vl10'))
from parse import clean_math, tidy
HERE = os.environ.get('VL12_DIR') or os.getcwd()
Q = re.compile(r'\*\*\s*Câu\s*(\d+)\s*[:.]?\s*(?:\([^)]*\))?\s*\*\*\s*[:.]?\s*')
HEAD = re.compile(r'^\s*#')
ST = re.compile(r'(?m)(?:^|(?<=\\\n))[>\s]*(?:\d+\.\s+)?\**\s*([a-d])\)\**\s*(?=\S)')
GUIDE = re.compile(r'(?m)^[>\s]*\**\s*(?:Hướng dẫn|Lời giải|Giải|HƯỚNG DẪN)\b')
VERD = re.compile(r'(?<![\w])([a-d])\)[\}\$\*\s]*(Đúng|Sai|ĐÚNG|SAI)')

def parse(name, a, b):
    lines = unicodedata.normalize('NFC', open(os.path.join(HERE, 'md', name + '.md'), encoding='utf8').read()).split('\n')[a - 1:b]
    blocks, cur = [], None
    for ln in lines:
        if HEAD.match(ln) and not Q.search(ln): cur = None; continue
        ms = list(Q.finditer(ln))
        if ms:
            cur = {'num': int(ms[0].group(1)), 'raw': [ln[ms[0].end():]]}; blocks.append(cur); continue
        if cur is not None: cur['raw'].append(ln)
    out = []
    for blk in blocks:
        raw = '\n'.join(blk['raw']); flags = []
        hd = GUIDE.search(raw)
        guide = raw[hd.start():] if hd else ''
        body = raw[:hd.start()] if hd else raw
        ms = [m for m in ST.finditer(body)]
        # lấy bộ a,b,c,d đầu tiên theo thứ tự
        pos, cur_i = [], 0
        for L in 'abcd':
            f = next((m for m in ms if m.group(1) == L and m.start() >= cur_i), None)
            if not f: break
            pos.append(f); cur_i = f.end()
        if len(pos) < 4: flags.append('khong-du-a-d'); stem, sts = body, []
        else:
            stem = body[:pos[0].start()]
            sts = []
            for i, m in enumerate(pos):
                end = pos[i + 1].start() if i < 3 else len(body)
                t = body[m.end():end]
                mk = (']{.mark}' in t) or ('⟦U⟧' in t)
                sts.append([m.group(1), t, mk])
            # sau d) có thể còn đoạn chung -> chỉ giữ tới hết đoạn
            t = sts[3][1]; k = re.search(r'\n\s*\n', t)
            if k: sts[3][1] = t[:k.start()]
        verd = {}
        for m in VERD.finditer(guide):
            verd.setdefault(m.group(1), 'Đ' if m.group(2).lower() == 'đúng' else 'S')
        res = []
        if sts:
            anyMark = any(s[2] for s in sts)
            for l, t, mk in sts:
                v = verd.get(l)
                if v is None and not hd: v = 'Đ' if mk else 'S'  # không có hướng dẫn: tô vàng = Đúng
                if v is None: flags.append('thieu-dap-an-' + l); v = '?'
                if hd and anyMark and (v == 'Đ') != mk: flags.append('lech-to-vang-' + l)
                res.append([l, clean_math(tidy(re.sub(r'\[([^\]]*)\]\{\.mark\}', r'\1', t.replace('⟦U⟧','')))).rstrip('\\ \n'), v])
        raw_all = raw
        if re.search(r'!\[|<table|\\includegraphics', body): flags.append('co-hinh')
        if not hd and not any(s[2] for s in sts): flags.append('khong-co-dap-an')
        out.append({'file': name, 'part': 'tf', 'num': blk['num'], 'flags': sorted(set(flags)),
                    'stem': clean_math(tidy(re.sub(r'\[([^\]]*)\]\{\.mark\}', r'\1', stem))), 'statements': res,
                    'solution': '', 'hasImg': 'co-hinh' in flags, 'imgs': re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body)})
    return out

if __name__ == '__main__':
    name, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    outn = sys.argv[4] if len(sys.argv) > 4 else name + '-ds'
    items = parse(name, a, b)
    os.makedirs(os.path.join(HERE, 'cau-tho'), exist_ok=True)
    json.dump(items, open(os.path.join(HERE, 'cau-tho', outn + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(outn, len(items), dict(Counter(x for i in items for x in i['flags'])))
