#!/usr/bin/env python3
"""Áp phản hồi duyệt -> cau-final.json (trong VL10_DIR). Chạy: VL10_DIR=<dir> python3 ap-duyet.py"""
import json, os, sys
H = os.environ.get('VL10_DIR') or os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bang import fix_html
dec = json.load(open(f'{H}/duyet/phan-hoi.json'))
cau = json.load(open(f'{H}/cau-bank.json'))
hk = {o['key']: o for o in json.load(open(f'{H}/ket-qua-haiku.json'))}
sn = {o['key']: o for o in json.load(open(f'{H}/ket-qua.json')) if o['trangThai'] != 'chua-co-ket-qua'}
final, drop, manual = [], [], []
for q in cau:
    k = q['key']; d = dec.get(k)
    src = sn[k] if k in sn and sn[k]['trangThai'] == 'khop' else hk[k]
    ex = src.get('explanation', '')
    if (k in sn and sn[k]['trangThai'] == 'LECH') or (k not in sn and hk[k]['trangThai'] != 'khop'):
        c = (d or {}).get('choice')
        s = sn.get(k) or hk[k]
        if c in (None, 'bo'): drop.append((k, c)); continue
        if c == 'ai':
            a = s['giai']; ex = s['explanation']
            if a is None: drop.append((k, 'ai-ma-khong-co-ket-qua')); continue
            if q['type'] == 'multiple_choice': q['answer'] = 'ABCD'.index(str(a)[0].upper())
            elif q['type'] == 'true_false':
                for st, v in zip(q['statements'], a): st['answer'] = bool(v)
            else: q['answer'] = str(a)
        elif c == 'khac':
            drop.append((k, 'khac-can-xu-ly-tay')); continue
        else: ex = ''; manual.append(k)   # theo nguồn: lời giải AI nói ngược → viết tay
    elif q['type'] == 'short_answer':
        q['answer'] = str(src['giai'])
    q['question'] = fix_html(q['question'])
    q['explanation'] = ex; q['duyet'] = (d or {}).get('choice', 'khop-2-nguon')
    final.append(q)
json.dump(final, open(f'{H}/cau-final.json', 'w'), ensure_ascii=False, indent=1)
print(len(final), 'giữ;', 'bỏ/chưa xử lý:', drop, '| cần viết tay lời giải:', manual)
print(sum(1 for q in final if not q['explanation']), 'câu rỗng lời giải;', sum(1 for q in final if q['type'] == 'short_answer' and not q.get('answer')), 'TLN rỗng đáp số')
