#!/usr/bin/env python3
"""Tách md/*.md (pandoc từ Word GV) thành câu hỏi có cấu trúc -> cau-tho/<file>.json.
Không dùng LLM. Câu nào không tách sạch thì gắn flag, không đoán.
  python3 parse.py c3-1 c3-2 ..."""
import json, re, sys, os

HERE = os.environ.get('VL10_DIR') or os.path.dirname(os.path.abspath(__file__))

def clean_math(s):
    """Làm gọn LaTeX sinh từ MathType (\\mathit{F}\\mathbf{=}...)."""
    def fix(m):
        t = m.group(1)
        for _ in range(4):
            t = re.sub(r'\\mathit\{((?:[^{}]|\{[^{}]*\})*)\}', r'\1', t)
            t = re.sub(r'\\mathbf\{((?:[^{}]|\{[^{}]*\})*)\}', r'\1', t)
            t = re.sub(r'\\mathrm\{([^{}]*)\}', r'\\mathrm{\1}', t)
        t = re.sub(r'\\(Delta|delta|leq|geq|alpha|beta|gamma|omega|Omega|pi|mu|theta|varphi|lambda|rho|sigma|tau|approx|cdot|times|neq|rightarrow|Rightarrow|uparrow|downarrow)(?=[A-Za-z])', r'\\\1 ', t)
        t = t.replace('\\ ', ' ')
        t = re.sub(r'\s+', ' ', t).strip()
        return '$' + t + '$'
    s = re.sub(r'\$([^$\n]+)\$', fix, s)
    # dán chữ liền công thức: "$10$trượt" -> "$10$ trượt"
    s = re.sub(r'(?<=[^\s$])\$(?=[A-Za-zÀ-ỹ])(?<!\$\$)', lambda m: m.group(0), s)
    s = re.sub(r'(\$[^$\n]+\$)(?=[A-Za-zÀ-ỹ])', r'\1 ', s)
    return s

def tidy(s):
    s = s.replace('\\.', '.').replace('\\(', '(').replace('\\)', ')').replace('\\*', '*').replace('\\[', '[').replace('\\]', ']')
    s = re.sub(r'\{\.mark\}|\{\.underline\}', '', s) if False else s
    s = re.sub(r'\]\{\.(?:mark|underline)\}', '', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

Q_START = re.compile(r'^\*\*(?:\[)?\s*(?:Câu|Bài)\s*(\d+)\s*[:.]?\s*(?:\])?\s*\*\*\s*[:.]?\s*(.*)$', re.I)
SEC = [
    (re.compile(r'TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN|PHẦN I\.', re.I), 'mc'),
    (re.compile(r'TRẮC NGHIỆM ĐÚNG SAI|PHẦN II\.', re.I), 'tf'),
    (re.compile(r'TRẢ LỜI NGẮN|PHẦN III\.', re.I), 'sa'),
    (re.compile(r'TỰ LUẬN', re.I), 'tl'),
    (re.compile(r'BÀI TẬP VÍ DỤ|PHƯƠNG PHÁP GIẢI|BÀI TẬP KIẾN THỨC', re.I), 'skip'),
]
SOL = re.compile(r'^\**\s*Hướng dẫn giả[iy]\s*\**\s*:?\**\s*$', re.I)

def section_of(line):
    if len(line) > 200 or not line.strip():
        return None
    plain = re.sub(r'[\*\[\]>{}.mark]', '', line) if False else line
    if Q_START.match(line):
        return None
    for rx, k in SEC:
        if rx.search(line) and len(line) < 160:
            return k
    return None

OPT = re.compile(r'(?:^|(?<=[\s\[]))(?:\*\*)?\[?(?:\*\*)?\[?([ABCD])\]?(\{\.underline\})?\.?\]?(\{\.underline\})?(?:\*\*)?(?=[\s\n]|$)')

def split_options(text):
    """Trả (stem, [(letter, text, underlined)], flags)."""
    t = re.sub(r'^>\s?', '', text, flags=re.M)
    t = re.sub(r'\n+', ' \n', t)
    pos = []
    cur = 0
    for L in 'ABCD':
        found = None
        for m in OPT.finditer(t, cur):
            if m.group(1) == L and '.' in m.group(0):
                found = m; break
        if not found:
            return t, [], ['khong-du-A-D']
        pos.append(found); cur = found.end()
    stem = t[:pos[0].start()].strip()
    opts = []
    for i, m in enumerate(pos):
        end = pos[i + 1].start() if i + 1 < 4 else len(t)
        body = t[m.end():end]
        und = bool(m.group(2) or m.group(3))
        # trường hợp cả phương án được gạch chân: [A. nội dung]{.underline}
        opts.append([m.group(1), body.strip(), und])
    return stem, opts, []

def parse_file(name):
    lines = open(os.path.join(HERE, 'md', name + '.md'), encoding='utf8').read().split('\n')
    sec = None
    blocks = []
    cur = None
    for ln in lines:
        s = section_of(ln)
        if s:
            sec = s; cur = None; continue
        m = Q_START.match(ln)
        if m and sec in ('mc', 'tf', 'sa', 'tl'):
            cur = {'file': name, 'part': sec, 'num': int(m.group(1)), 'raw': [m.group(2)]}
            blocks.append(cur); continue
        if cur is not None:
            cur['raw'].append(ln)
    out = []
    for b in blocks:
        raw = re.sub(r'(?m)^>\s?', '', '\n'.join(b['raw']))
        parts = re.split(r'\n\**\s*Hướng dẫn giả[iy]\s*\**\s*:?\**\s*\n', raw, maxsplit=1, flags=re.I)
        body = parts[0]; sol = parts[1] if len(parts) > 1 else ''
        flags = []
        item = {'file': b['file'], 'part': b['part'], 'num': b['num'], 'flags': flags}
        if b['part'] == 'mc':
            stem, opts, fl = split_options(body)
            flags += fl
            item['stem'] = clean_math(tidy(stem))
            item['options'] = [[l, clean_math(tidy(tx)), u] for l, tx, u in opts]
            ans = [l for l, tx, u in opts if u]
            if not ans:
                # underline có thể bao cả phương án sau dấu chấm
                flags.append('khong-gach-chan')
            elif len(ans) > 1:
                flags.append('nhieu-gach-chan')
            item['answer'] = ans[0] if len(ans) == 1 else None
        elif b['part'] == 'tf':
            if '<table' in body:  # pandoc xuất bảng HTML khi ô có nhiều đoạn → đổi về dòng pipe
                def _tb(m):
                    out = []
                    for tr in re.findall(r'<tr>(.*?)</tr>', m.group(0), flags=re.S):
                        cells = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', c)).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, flags=re.S)]
                        if len(cells) == 2: out.append('| ' + cells[0] + ' | ' + cells[1] + ' |')
                    return '\n\n' + '\n'.join(out) + '\n'
                body = re.sub(r'<table>.*?</table>', _tb, body, flags=re.S)
            rows = re.findall(r'^\|\s*([a-d])\\?\.\s*(.*?)\s*\|\s*\**\s*([ĐSđs])\s*\**\s*\|', body, flags=re.M)
            stem = body.split('\n\n|')[0] if '\n\n|' in body else body.split('\n|')[0]
            item['stem'] = clean_math(tidy(stem))
            item['statements'] = [[l, clean_math(tidy(tx)), v.upper()] for l, tx, v in rows]
            if [r[0] for r in rows] != ['a', 'b', 'c', 'd']:
                # dạng không bảng: 4 ý a\. b\. c\. d\. là dòng thường, đúng/sai nằm trong lời giải
                lines = body.split('\n')
                st = {}
                for ln in lines:
                    m2 = re.match(r'^\s*([a-d])\s*(?:\\)?[.)]\s*(.+)$', ln)
                    if m2 and m2.group(1) not in st: st[m2.group(1)] = m2.group(2).strip()
                first = re.search(r'(?m)^\s*a\s*(?:\\)?[.)]', body)
                stem2 = body[:first.start()] if first else body
                vs = {}
                for ln in sol.split('\n'):
                    m3 = re.match(r'^\s*([a-d])\s*(?:\\)?[.)]\s*(.+)$', ln)
                    if m3 and m3.group(1) not in vs:
                        t3 = m3.group(2)
                        v = re.findall(r'\*\*\s*(đúng|sai)\s*\*\*', t3[:240], flags=re.I)
                        if not v: v = re.findall(r'(?:phát biểu|ý|mệnh đề|nhận định|kết luận)[^.;]{0,40}?\b(đúng|sai)\b', t3[:240], flags=re.I)
                        if len(set(x.lower() for x in v)) == 1: vs[m3.group(1)] = 'Đ' if v[0].lower() == 'đúng' else 'S'
                if sorted(st) == ['a', 'b', 'c', 'd'] and sorted(vs) == ['a', 'b', 'c', 'd']:
                    rows = [(l, st[l], vs[l]) for l in 'abcd']
                    item['stem'] = clean_math(tidy(stem2))
                    flags.append('ds-tu-loi-giai')
                else:
                    flags.append('bang-dung-sai-khong-du-4-y')
                    if sorted(st) == ['a', 'b', 'c', 'd']: flags.append('thieu-' + ''.join(sorted(set('abcd') - set(vs))))
            item['statements'] = [[l, clean_math(tidy(tx)), v.upper()] for l, tx, v in rows]
        else:  # sa / tl
            item['stem'] = clean_math(tidy(body))
        item['solution'] = clean_math(tidy(sol))
        if not sol.strip():
            flags.append('khong-co-loi-giai')
        if re.search(r'!\[', body) or re.search(r'!\[', sol):
            flags.append('co-hinh')
        if '⟦' in raw or '[OLE' in raw:
            flags.append('con-ole')
        item['hasImg'] = bool(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body))
        item['imgs'] = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body)
        out.append(item)
    return out

if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'cau-tho'), exist_ok=True)
    tot = {}
    for n in sys.argv[1:]:
        items = parse_file(n)
        json.dump(items, open(os.path.join(HERE, 'cau-tho', n + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        from collections import Counter
        c = Counter(i['part'] for i in items)
        f = Counter(x for i in items for x in i['flags'])
        print(n, len(items), dict(c), dict(f))
