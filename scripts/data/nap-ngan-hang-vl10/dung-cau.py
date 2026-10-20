#!/usr/bin/env python3
"""cau-tho/*.json -> cau-bank.json (định dạng question_bank: type/question/options/answer/statements).
Bỏ (ghi vào loai-ra.json kèm lý do): câu có hình, câu cờ lỗi tách, câu tự luận định tính.
  python3 dung-cau.py c3-1 c3-2 ..."""
import json, re, sys, os
H = os.path.dirname(os.path.abspath(__file__))
P = '<p class="text-base leading-relaxed my-2">'

def inline(s):
    s = s.replace('\\\n', '\n')
    s = re.sub(r'\[([^\]]*)\]\{\.(?:mark|underline)\}', r'\1', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s, flags=re.S)
    s = re.sub(r'(?<![\w$])(\w+)~([^~\s]+)~', r'$\1_{\2}$', s)
    s = re.sub(r'(\w)\^([^\^\s]+)\^', r'\1$^{\2}$', s)
    s = re.sub(r'~([^~\s]+)~', r'$_{\1}$', s)
    s = re.sub(r'\^([^\^\s]+)\^', r'$^{\1}$', s)
    s = s.replace('<', '&lt;') if False else s
    return s.strip()

def html(s):
    paras = [p for p in re.split(r'\n\s*\n', s.strip()) if p.strip()]
    return ''.join(P + inline(p.replace('\n', ' ')) + '</p>' for p in paras)

def ok_text(s): return bool(s and s.strip())

keep, out = [], []
for n in sys.argv[1:]:
    for seq, it in enumerate(json.load(open(f'{H}/cau-tho/{n}.json')), 1):
        key = f"{it['file']}-{it['part']}-{seq:03d}"
        why = []
        if it['part'] == 'tl': why.append('tu-luan-dinh-tinh')
        for f in it['flags']:
            if f in ('khong-du-A-D', 'khong-gach-chan', 'nhieu-gach-chan', 'bang-dung-sai-khong-du-4-y', 'con-ole'): why.append(f)
        if it.get('hasImg') or 'co-hinh' in it['flags'] and re.search(r'!\[', it.get('stem', '')): why.append('co-hinh-trong-de')
        if re.search(r'!\[', ' '.join(o[1] for o in it.get('options', []))): why.append('hinh-trong-phuong-an')
        if any(len(o[1])>400 for o in it.get('options',[])): why.append('phuong-an-qua-dai-nghi-dinh-chu')
        if why: out.append({'key': key, 'why': why}); continue
        q = {'key': key, 'src': it['file'], 'num': it['num'], 'gocLoiGiai': it['solution'], 'form': 'bai_tap'}
        if it['part'] == 'mc':
            q.update(type='multiple_choice', question=html(it['stem']), options=[inline(o[1]) for o in it['options']], answer='ABCD'.index(it['answer']))
        elif it['part'] == 'tf':
            q.update(type='true_false', question=html(it['stem']), statements=[{'text': inline(s[1]), 'answer': s[2] == 'Đ'} for s in it['statements']])
        else:
            q.update(type='short_answer', question=html(it['stem']), answer=None)
        keep.append(q)
json.dump(keep, open(f'{H}/cau-bank.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open(f'{H}/loai-ra.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('giu', len(keep), Counter(q['type'] for q in keep)); print('loai', len(out), Counter(w for o in out for w in o['why']))
