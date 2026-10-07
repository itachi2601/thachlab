#!/usr/bin/env python3
"""Dựng HTML in sách từ nội dung thachlab (public/data/lessons + scripts/data/bai-tap-mau).

  python3 build.py lesson 49          → src/lesson-49.html
  python3 build.py all                → mọi bài của chương
  python3 build.py front              → src/front.html (bìa, mục lục…)
Xem make.py để dựng PDF trọn chương.
"""
import hashlib, html as htmllib, json, re, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image

import bw

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SRC = ROOT / 'src'
IMG = ROOT / 'assets' / 'img'
BASE_URL = 'https://thachlab.id.vn'

CUR = {'lid': 0}

CHAPTER = {'num': 2, 'title': 'Động học', 'sub': 'Mô tả chuyển động — chưa cần hỏi vì sao vật chuyển động',
           'lessons': [49, 50, 51, 52, 53, 54, 55, 56, 57]}


def lesson_url(lid): return f'{BASE_URL}/lop-hoc/bai?id={lid}'
def answers_url(lid): return f'{BASE_URL}/sach/dap-an/?bai={lid}'


def _cfg(name):
    p = SRC / name
    d = json.load(open(p)) if p.exists() else {}
    return {int(k): v for k, v in d.items() if not k.startswith('_')}


DANG_CHUNG = _cfg('dang-chung.json')   # {lid: [chỉ số Dạng được giảng trên lớp]}; mặc định [1, 2]
TIET = _cfg('tiet.json')               # {lid: ['muc:II', 'bai-tap-mau', ...]}; mặc định tiết 1 hết mục II, tiết 2 hết Bài tập mẫu


def dang_chung(lid, n):
    want = DANG_CHUNG.get(lid) or [1, 2]
    return [k for k in want if 1 <= k <= n]


def tiet_marks(lid, has_bt):
    anchors = TIET.get(lid) or (['muc:II', 'bai-tap-mau'] if has_bt else ['muc:II', 'muc:V'])
    return {a: i + 1 for i, a in enumerate(anchors)}


def tiet_mark(n):
    return f'<div class="tiet"><span class="tiet-l">hết tiết {n}</span></div>'


def timer():
    """Biểu tượng cố định ở góc mọi khung có ô điền: em tự điền 1 phút trước khi thầy chữa."""
    return f'<span class="t1">{bw.ICONS["clock"]}1′</span>'


# ------------------------------------------------------------------ đọc dữ liệu
def load_lesson(lid):
    d = json.load(open(REPO / f'public/data/lessons/{lid}.json'))
    theory = next(it for it in d['items'] if it['kind'] == 'ly_thuyet')['body_html']
    bt = None
    p = REPO / f'scripts/data/bai-tap-mau/{lid}.json'
    if p.exists():
        bt = json.load(open(p))
    title = d['lesson']['title']
    m = re.match(r'Bài\s+(\d+)\.\s*(.*)', title)
    return {'id': lid, 'num': int(m.group(1)) if m else 0, 'name': m.group(2) if m else title,
            'title': title, 'theory': theory, 'bt': bt}


# ------------------------------------------------------------------ tiện ích
def soup_of(html):
    return BeautifulSoup(html, 'html.parser')


def frag(html):
    return BeautifulSoup(html, 'html.parser')


def plain(el):
    return re.sub(r'\s+', ' ', el.get_text(' ', strip=True) if hasattr(el, 'get_text') else str(el))


def dl(n):
    return f'<div class="dl" style="--n:{n}">' + '<i></i>' * n + '</div>'


def protect_svgs(html):
    store = []
    def rep(m):
        store.append(m.group(0)); return f'<!--SVG{len(store)-1}-->'
    return re.sub(r'<svg\b.*?</svg>', rep, html, flags=re.S), store


def restore_svgs(html, store):
    return re.sub(r'<!--SVG(\d+)-->', lambda m: store[int(m.group(1))], html)


# ------------------------------------------------------------------ điền khuyết
REL = re.compile(r'(=|\\leq?\b|\\geq?\b|\\neq|\\approx|\\lt|\\gt|<|>)')


def blank_math(html, keys, mode):
    """Thay công thức trọng tâm bằng ô trống đánh số; đáp án gom về cuối bài.
    mode 'key': mọi biểu thức có dấu quan hệ trong khung GHI NHỚ; 'body': công thức hiển thị + biểu thức dài có dấu '='."""
    def disp(m):
        n = keys.fadd(m.group(1).strip(), True)
        return f'<div class="fb-disp"><i class="fbn">{n}</i></div>'
    def inline(m):
        tex = m.group(1)
        if not REL.search(tex): return m.group(0)
        if mode == 'body' and (len(tex) < 8 or '=' not in tex): return m.group(0)
        if mode == 'key' and len(tex) < 3: return m.group(0)
        n = keys.fadd(tex.strip(), False)
        w = max(13, min(60, round(len(re.sub(r'\\[a-z]+', 'x', tex)) * 1.5)))
        return f'<span class="fb" style="min-width:{w}mm"><i class="fbn">{n}</i></span>'
    html = re.sub(r'\$\$(.*?)\$\$', disp, html, flags=re.S)
    html = re.sub(r'(?<!\$)\$([^$\n]+?)\$(?!\$)', inline, html)
    return html


def blank_table(html):
    """Bảng phân tích đề: giữ cột 'Câu trong đề', các cột còn lại để học sinh tự điền."""
    soup = soup_of(html)
    for tb in soup.find_all('table'):
        if 'data' not in tb.get('class', []) and 'tl-table--data' not in tb.get('class', []): continue
        for tr in tb.find_all('tr'):
            tds = tr.find_all('td')
            for td in tds[1:]:
                td.clear(); td.append(frag('<div class="fill"></div>'))
        for th in tb.find_all('th')[1:]:
            th.append(frag(' <small class="te">(em điền)</small>'))
    return str(soup)


# ------------------------------------------------------------------ chuyển lý thuyết
class Keys:
    """Gom đáp án để in ở cuối bài."""
    def __init__(self):
        self.items = []; self.where = ''; self.counter = 0; self.formulas = []
        self.challenges = []   # thử thách phân tầng (dời xuống Luyện thêm)
    def fadd(self, tex, display):
        self.formulas.append({'tex': tex, 'display': display}); return len(self.formulas)

    def add(self, **kw):
        self.counter += 1
        kw['n'] = self.counter; kw['where'] = self.where
        self.items.append(kw); return self.counter


HINT_RE = re.compile(r'\s*[\(（][^)）]*(bấm|nghĩ|tự trả lời|tự tính|nói bằng lời)[^)）]*[\)）]\s*')
SELFQ_RE = re.compile(r'(rồi bấm|rồi mới bấm|nghĩ rồi|nghĩ trước|tự trả lời|tự tính|bấm xem gợi ý|gợi ý:)', re.I)


def clean_summary(s):
    s = re.sub(r'<small>.*?</small>', '', s, flags=re.S)
    s = HINT_RE.sub('', s)
    return s.strip()


def conv_details(det, keys, ctx=''):
    summ = det.find('summary')
    s_html = summ.decode_contents() if summ else ''
    s_plain = plain(summ) if summ else ''
    summ.extract() if summ else None
    body = det.decode_contents()
    low = s_plain
    if 'Thử thách' in low:
        # v6: thử thách phân tầng dời xuống mục "Luyện thêm" cuối bài (chỉ in đề, em làm vào vở)
        for li in det.find_all('li'):
            li_html = li.decode_contents()
            mm = re.search(r'^(.*?)(<em>\s*(?:\(|Đáp)[\s\S]*)$', li_html, re.S)
            if mm:
                qtxt, ans = mm.group(1).strip(), re.sub(r'</?em>', '', mm.group(2)).strip()
                ans = ans[1:-1] if ans.startswith('(') and ans.endswith(')') else ans
            else:
                qtxt, ans = li_html, ''
            sm = re.match(r'\s*((?:★|⭐)+)\s*', qtxt)
            stars = sm.group(1).replace('⭐', '★') if sm else ''
            qtxt = qtxt[sm.end():] if sm else qtxt
            keys.add(kind='thuthach', title='Thử thách', body=ans, tag='Thử thách')
            keys.challenges.append({'n': keys.counter, 'stars': stars, 'q': qtxt})
        return ''
    if low.startswith('Xem bước'):
        n = keys.add(kind='fill', body=body, tag='Điền bước còn thiếu')
        return (f'<div class="selfq"><div class="sq-h"><span class="sq-n">{n}</span> Em điền các bước còn thiếu</div>'
                f'{dl(3)}<div class="sq-k">Đáp án số {n}: quét mã QR cuối bài</div></div>')
    is_self = ctx == 'trabai' or bool(SELFQ_RE.search(s_html)) or ('?' in s_plain and not re.search(r'Bấm xem:|Xem thêm|bốn nơi', s_plain)) \
        or s_plain.startswith('🧮 Tự tính trước')
    if is_self and 'lời giải' not in low.lower():
        title = clean_summary(s_html)
        tag = 'Trả bài' if ctx == 'trabai' else 'Tự hỏi'
        n = keys.add(kind='selfq', q=title, body=body, tag=tag)
        lines = 2
        return (f'<div class="selfq"><div class="sq-h"><span class="sq-n">{n}</span><span>{title}</span></div>'
                f'{dl(lines)}</div>')
    # còn lại: hiện thẳng (lời giải mẫu, mở rộng, đời sống)
    title = clean_summary(s_html)
    title = re.sub(r'^(<span class="ico">.*?</span>)?\s*(Bấm xem|Xem thêm)\s*:?\s*', r'\1 ', title).strip()
    if 'lời giải' in low.lower():
        return ('<div class="gnote"><div class="gn-l">Lời giải — ghi cùng thầy cô, hoặc xem trên web (quét mã QR đầu bài)' + timer() + '</div>'
                + dl(4) + '</div>')
    is_sol = False
    cls = 'reveal sol-inline' if is_sol else 'reveal'
    return f'<div class="{cls}"><div class="rv-h">{title or "Lời giải mẫu"}</div><div class="rv-b">{body}</div></div>'


def conv_quiz(box, keys):
    label = box.find('p', class_='tl-label')
    quiz = box.find('div', class_='tl-quiz')
    qnodes = []
    after = list(label.next_siblings) if label else list(box.children)
    for el in after:
        if el is quiz: break
        if isinstance(el, Tag): qnodes.append(el)
    qhtml = ''.join(str(e) for e in qnodes)
    label_plain = plain(label) if label else ''
    m = re.search(r'<strong>\s*(Câu\s*\d+)\.?\s*</strong>\s*', qhtml)
    if m:
        tag = m.group(1).upper(); qhtml = qhtml.replace(m.group(0), '', 1)
    elif 'Dự đoán' in label_plain:
        tag = 'DỰ ĐOÁN'
    else:
        tag = 'CÂU HỎI'
    sub = re.sub(r'^[^\wÀ-ỹ]*', '', label_plain)
    opts, correct = [], []
    for lab in quiz.find_all('label', class_='tl-opt'):
        t = lab.decode_contents()
        mm = re.match(r'\s*([A-D])\.\s*(.*)', t, re.S)
        if not mm: continue
        opts.append((mm.group(1), mm.group(2).strip()))
        if 'tl-ok' in lab.get('class', []): correct.append(mm.group(1))
    fb_ok = quiz.find(class_='tl-fb--ok'); fb_no = quiz.find(class_='tl-fb--no')
    n = keys.add(kind='quiz', tag=tag, sub=sub, letter=''.join(correct),
                 ok=fb_ok.decode_contents() if fb_ok else '', no=fb_no.decode_contents() if fb_no else '')
    why = f'<div class="q-why">Vì sao em chọn vậy?</div>{dl(1)}' if tag == 'DỰ ĐOÁN' else ''
    long_opts = any(len(re.sub(r'<[^>]+>|\$[^$]*\$', 'x', o[1])) > 34 for o in opts)
    lis = ''.join(f'<li><span class="ob">{l}</span><span class="ot">{t}</span></li>' for l, t in opts)
    ol = f'<ol class="opts {"long" if long_opts else "short"}">{lis}</ol>'
    return (f'<div class="quiz"><div class="q-h"><span class="q-tag">{tag}</span><span class="q-sub">{sub}</span></div>'
            f'<div class="q-t">{qhtml}</div>{ol}'
            f'{why}<div class="q-f"><span>Em chọn: <span class="blank"></span></span>'
            f'<span class="q-k">đáp án số <b>{n}</b> · QR cuối bài</span></div></div>')


def conv_think(box, keys):
    """tl-box--think không phải quiz: Trả bài, Điền bước, Đọc bảng…"""
    label = box.find('p', class_='tl-label')
    if label is None:   # nhãn nằm ngay trong đoạn đầu: <p><strong>Điền bước…</strong> — …</p>
        p0 = box.find('p'); st = p0.find('strong') if p0 else None
        lab_html = st.decode_contents() if st else 'Em thử'
        if st:
            st.extract()
            txt = re.sub(r'^\s*[—-]\s*', '', p0.decode_contents())
            p0.clear(); p0.append(frag(txt))
        lab_plain = re.sub(r'<[^>]+>', '', lab_html)
    else:
        lab_html = label.decode_contents(); lab_plain = plain(label)
        label.extract()
    ctx = 'trabai' if 'Trả bài' in lab_plain else ''
    for det in box.find_all('details'):
        det.replace_with(frag(conv_details(det, keys, ctx)))
    cls = 'think trabai' if ctx else 'think'
    lab_html = HINT_RE.sub('', lab_html)
    inner = box.decode_contents()
    extra = ''
    if 'Điền bước' in lab_plain:
        inner = re.sub(r'\?', '<span class="blank wide"></span>', inner) if False else inner
    return f'<div class="{cls}"><div class="th-h">{lab_html}</div>{inner}</div>'


def conv_exp(box):
    label = box.find('p', class_='tl-label')
    lab_html = label.decode_contents(); label.extract()
    steps_html = ''
    ol = box.find('ol', class_='tl-steps')
    if ol:
        rows = []
        for li in ol.find_all('li', recursive=False):
            st = li.find('strong')
            if st and re.match(r'^[^:]{1,14}:$', plain(st)):
                head = plain(st).rstrip(':'); st.extract()
                rows.append(f'<div class="step"><div class="st-l">{head}</div><div class="st-b">{li.decode_contents().strip()}</div></div>')
            else:
                rows.append(f'<div class="step"><div class="st-l">·</div><div class="st-b">{li.decode_contents()}</div></div>')
        steps_html = ''.join(rows); ol.extract()
    rest = box.decode_contents()
    sim = '<span class="simtag">▶ có mô phỏng trên web</span>' if box.get('data-exp') else ''
    return (f'<div class="exp"><div class="exp-h"><span>{lab_html}</span>{sim}</div>{steps_html}{rest}'
            f'<div class="exp-w"><span>Số liệu / điều em quan sát:</span>{timer()}{dl(2)}</div></div>')


def conv_box(box):
    cls = box.get('class', [])
    label = box.find('p', class_='tl-label')
    lab_html = label.decode_contents() if label else ''
    if label: label.extract()
    inner = box.decode_contents()
    if 'tl-box--rule' in cls and 'Đề bài' not in lab_html:
        return f'<div class="takeaway"><div class="tk-h">{lab_html}</div>{inner}</div>'
    return f'<div class="problem"><div class="pb-h">{lab_html}</div>{inner}</div>'


def web_note():
    return (f'<div class="fig-web"><span class="qr mini" data-url="{lesson_url(CUR["lid"])}"></span>'
            '<span><b>Trên lớp:</b> chiếu mô phỏng này trên web. Quét mã để tự chạy lại ở nhà.</span></div>')


def gnote(label, n):
    return f'<div class="gnote"><div class="gn-l">{label}</div>{dl(n)}</div>'


def conv_figure(fig):
    cap = fig.find('figcaption')
    for b in fig.find_all('button'): b.extract()
    simtag = ''
    if fig.get('data-exp') or fig.get('data-bt'):
        simtag = '<span class="simtag fig-sim">▶ mô phỏng trên web</span>'
    if cap:
        c = cap.decode_contents()
        c = re.sub(r'\s*Bấm Chạy mô phỏng\.?', '', c)
        c = re.sub(r'\s*[\(（]chạy nhanh[^)）]*[\)）]', '', c)
        c = re.sub(r'\bMô phỏng:', 'Mô phỏng (xem chuyển động trên web):', c)
        cap.clear(); cap.append(frag(c))
    web = web_note() if simtag else ''
    return f'<figure class="fig">{simtag}{fig.decode_contents()}{web}</figure>'


def conv_h3(h):
    t = h.decode_contents()
    m = re.match(r'\s*([IVX]+)\.\s*(.*)', t, re.S)
    if m:
        return f'<h3><span class="rn">{m.group(1)}</span><span class="ht">{m.group(2)}</span></h3>', m.group(1)
    return f'<h3><span class="ht">{t}</span></h3>', ''


def conv_h4(h):
    t = h.decode_contents()
    m = re.match(r'\s*Bẫy\s*(\d+)\s*:\s*(.*)', t, re.S)
    if m:
        return f'<h4 class="trap"><span class="trap-l">BẪY {m.group(1)}</span><span>{m.group(2)}</span></h4>'
    m = re.match(r'\s*(\d+)\.\s*(.*)', t, re.S)
    if m:
        return f'<h4><span class="n">{m.group(1)}</span><span>{m.group(2)}</span></h4>'
    return f'<h4><span>{t}</span></h4>'


def final_pass(body, keys):
    """Khối còn sót dạng gốc (lồng trong khung khác): chuyển nốt, lặp tới khi hết."""
    soup = soup_of(body)
    for _ in range(80):
        el = soup.find('div', class_='tl-box')
        det = None if el else soup.find('details')
        if el is not None:
            cls = el.get('class', [])
            if 'tl-box--exp' in cls: new = conv_exp(el)
            elif 'tl-box--think' in cls: new = conv_quiz(el, keys) if el.find('div', class_='tl-quiz') else conv_think(el, keys)
            else: new = conv_box(el)
            el.replace_with(frag(new))
        elif det is not None:
            det.replace_with(frag(conv_details(det, keys)))
        else:
            break
    for w in soup.find_all('div', class_='table-scroll'): w.unwrap()
    for tb in soup.find_all('table'):
        if 'tl-table' in tb.get('class', []):
            tb['class'] = ['tbl', 'data'] if 'tl-table--data' in tb.get('class', []) else ['tbl']
    return str(soup)


def convert_theory(raw, lid, keys, marks=None):
    marks = marks or {}
    html = raw
    # bước chuỗi
    html = re.sub(r'<p><strong>🔑\s*(.*?)</strong></p>',
                  r'<div class="key"><span class="key-l">GHI NHỚ</span><p>\1</p></div>', html, flags=re.S)
    html = re.sub(r'<p class="tl-conf">.*?</p>',
                  '<p class="conf">Em chắc bao nhiêu? <span class="cb"></span> Chắc &nbsp; <span class="cb"></span> Không chắc</p>',
                  html, flags=re.S)
    html = bw.to_print(html)
    html, store = protect_svgs(html)
    soup = soup_of(html)
    # mục tiêu
    obj = None
    for box in soup.find_all('div', class_='tl-box', recursive=False):
        lab = box.find('p', class_='tl-label')
        if lab and 'Mục tiêu' in plain(lab):
            lis = [li.decode_contents() for li in box.find_all('li')]
            tail = box.find_all('p')[-1]
            obj = {'lis': lis, 'tail': tail.decode_contents() if tail is not lab else ''}
            box.extract(); break
    out = []
    roman = ''
    for el in list(soup.children):
        if isinstance(el, NavigableString):
            if str(el).strip(): out.append(str(el))
            continue
        cls = el.get('class', []) if hasattr(el, 'get') else []
        name = el.name
        if name == 'h3':
            if roman and f'muc:{roman}' in marks: out.append(tiet_mark(marks[f'muc:{roman}']))
            h, roman = conv_h3(el); keys.where = roman; out.append(h)
        elif name == 'h4':
            out.append(conv_h4(el))
            m = re.match(r'\s*(\d+)\.', el.get_text())
            keys.where = f'{roman}.{m.group(1)}' if m and roman else roman
        elif name == 'figure':
            out.append(conv_figure(el))
        elif name == 'div' and 'table-scroll' in cls:
            tb = el.find('table')
            is_data = 'tl-table--data' in tb.get('class', [])
            tb['class'] = ('tbl data' if is_data else 'tbl').split()
            out.append(blank_table(str(tb)) if is_data else str(tb))
        elif name == 'div' and 'key' in cls:
            k = blank_math(str(el), keys, 'key')
            if 'class="fbn"' in k:   # khung GHI NHỚ có ô điền → ⏱ 1′
                k = k.replace('<span class="key-l">GHI NHỚ</span>', '<span class="key-l">GHI NHỚ</span>' + timer(), 1)
            out.append(k)
        elif name in ('p', 'ul', 'ol') and roman == 'II':
            out.append(blank_math(str(el), keys, 'body'))
        elif name == 'div' and 'tl-box' in cls:
            if 'tl-box--exp' in cls: out.append(conv_exp(el))
            elif 'tl-box--think' in cls:
                out.append(conv_quiz(el, keys) if el.find('div', class_='tl-quiz') else conv_think(el, keys))
            else: out.append(conv_box(el))
        elif name == 'details':
            out.append(conv_details(el, keys))
        elif name == 'table':
            el['class'] = ['tbl']; out.append(str(el))
        else:
            out.append(str(el))
    if roman and f'muc:{roman}' in marks: out.append(tiet_mark(marks[f'muc:{roman}']))
    body = final_pass('\n'.join(out), keys)
    body = re.sub(r'(</h3>\s*)<p>', r'\1<p class="lead-p">', body, count=1)
    body = restore_svgs(body, store)
    return body, obj


# ------------------------------------------------------------------ bài tập mẫu
LEVEL = {'Dễ': ('★', 'DỄ'), 'Trung bình': ('★★', 'TRUNG BÌNH'), 'Khó': ('★★★', 'KHÓ')}


def table_fix(html):
    html = re.sub(r'<div class="table-scroll">(.*?)</div>', r'\1', html, flags=re.S)
    html = html.replace('tl-table tl-table--data', 'tbl data').replace('class="tl-table"', 'class="tbl"')
    return html


def clean_fig_caption_bt(html):
    html = table_fix(html)
    def fig(m):
        inner = m.group(2)
        if '<button' not in inner:
            return m.group(0)
        inner = re.sub(r'<button[^>]*>.*?</button>', '', inner, flags=re.S)
        inner = re.sub(r'\s*Bấm Chạy mô phỏng\.?', '', inner)
        inner = re.sub(r'\s*[\(（]chạy nhanh[^)）]*[\)）]', '', inner)
        inner = re.sub(r'\bMô phỏng:', 'Mô phỏng (xem chuyển động trên web):', inner)
        return (f'<figure class="fig"{m.group(1)}><span class="simtag fig-sim">▶ mô phỏng trên web</span>{inner}</figure>')
    return re.sub(r'<figure class="fig"([^>]*)>(.*?)</figure>', fig, html, flags=re.S)


def sol_clean(html):
    html = table_fix(html)
    html = html.replace('class="tl-box"', 'class="recall"')
    html = html.replace('class="tl-label"', 'class="rc-h"')
    return html


def dang_parts(x, k):
    parts = [p.strip() for p in x['label'].split('·')]
    num = parts[0].upper() if parts else f'DẠNG {k}'
    lvl = parts[1] if len(parts) > 1 else ''
    stars, lvl_name = LEVEL.get(lvl, ('', lvl.upper()))
    title = ' · '.join(parts[2:]) if len(parts) > 2 else x.get('topic', '')
    return num, stars, lvl_name, title


def dang_answer(x):
    """Đáp số (khối 'Đáp số' cuối lời giải) — in ở bảng đáp án thuần cuối sách."""
    m = re.search(r'<div class="bt-final">(.*?)</div>', x.get('solution_html', ''), re.S)
    if not m: return ''
    return re.sub(r'<p>\s*<strong>Đáp số</strong>\s*</p>', '', m.group(1)).strip()


def similar_to(x, bt, main):
    """Dạng luyện thêm 'tương tự Dạng n' = Dạng chung có cùng chủ đề (YCCĐ); không có thì để trống."""
    for k in main:
        if bt['dang_bai'][k - 1].get('topic') == x.get('topic'): return k
    return 0


GRAPH_RE = re.compile(r'đồ thị|hình (?:vẽ|bên|dưới|trên)|như hình', re.I)


def render_bt(bt, lid, keys, marks=None):
    """Bài tập mẫu v6: chỉ Dạng CHUNG NHẤT (dang-chung.json) giữ đủ đề + hình + bảng phân tích + ô lời giải
    ghi cùng thầy cô; các Dạng còn lại + thử thách phân tầng gộp thành 'Luyện thêm' (chỉ in đề)."""
    marks = marks or {}
    main = dang_chung(lid, len(bt['dang_bai']))
    out = []
    for k in main:
        x = bt['dang_bai'][k - 1]
        num, stars, lvl_name, title = dang_parts(x, k)
        prob = clean_fig_caption_bt(x['problem_html'])
        ana = re.sub(r'<figure class="fig".*?</figure>', '', clean_fig_caption_bt(x['analysis_html']), flags=re.S)
        ana = blank_table(ana)
        ana = re.sub(r'<p>Mỗi câu của đề:.*?</p>', '<p>Mỗi câu của đề cho dữ liệu gì, gọi kiến thức nào? Điền vào hai cột bên phải. Hàng có ⚠ là <b>điều kiện áp dụng</b>.</p>', ana, flags=re.S)
        out.append(f'''<article class="dang">
<div class="dang-top"><header class="dang-h"><span class="dang-n">{num}</span><span class="lvl">{stars} {lvl_name}</span><h3>{title}</h3></header>
<div class="de"><div class="de-l">Đề bài</div>{prob}</div></div>
<div class="pt"><div class="pt-l">Phân tích đề — em tự điền</div>{timer()}{ana}</div>
<div class="solbox"><div class="sol-l">Lời giải — ghi cùng thầy cô</div>{timer()}</div>
</article>''')
        if f'dang:{k}' in marks: out.append(tiet_mark(marks[f'dang:{k}']))
    if 'bai-tap-mau' in marks: out.append(tiet_mark(marks['bai-tap-mau']))
    return bw.to_print('\n'.join(out)), main


def render_luyen_them(bt, lid, keys, main):
    """Luyện thêm — bài tương tự: các Dạng không giảng trên lớp + thử thách phân tầng. Chỉ đề, không bảng
    phân tích, không mô phỏng, không ô lời giải (làm vào vở). Đáp số ở bảng cuối sách; lời giải đầy đủ trên web."""
    items = []
    if bt:
        for k, x in enumerate(bt['dang_bai'], 1):
            if k in main: continue
            num, stars, lvl_name, title = dang_parts(x, k)
            prob = clean_fig_caption_bt(x['problem_html'])
            txt = re.sub(r'<figure.*?</figure>', '', prob, flags=re.S)
            if GRAPH_RE.search(re.sub(r'<[^>]+>', '', txt)):
                # đề đọc đồ thị: giữ hình (thu nhỏ) vì không có hình thì không làm được
                prob = re.sub(r'<span class="simtag fig-sim">.*?</span>', '', prob, flags=re.S).replace('<figure class="fig"', '<figure class="fig fig-sm"')
            else:
                prob = txt
            sim = similar_to(x, bt, main)
            rel = f'<span class="lt-rel">tương tự Dạng {sim}</span>' if sim else '<span class="lt-rel">dạng riêng · lời giải trên web</span>'
            items.append(f'<div class="lt"><div class="lt-h"><span class="dang-n">{num}</span><span class="lvl">{stars} {lvl_name}</span>{rel}<span class="lt-k">đáp số: bảng cuối sách</span></div>'
                         f'<div class="lt-t">{title}</div>{prob}</div>')
    for c in keys.challenges:
        items.append(f'<div class="lt lt-ch"><div class="lt-h"><span class="dang-n">THỬ THÁCH</span><span class="lvl">{c["stars"]}</span>'
                     f'<span class="lt-k">đáp số: bảng cuối sách, số <b>{c["n"]}</b></span></div><p>{c["q"]}</p></div>')
    if not items: return ''
    return bw.to_print(f'<section class="ltsec"><div class="sec-band"><span class="sb-k">LUYỆN THÊM — BÀI TƯƠNG TỰ</span>'
                       f'<span class="sb-t">Làm vào vở · chọn mức ★ vừa sức · đáp số ở bảng cuối sách · lời giải đầy đủ: quét mã QR</span></div>'
                       + ''.join(items) + '</section>')


# ------------------------------------------------------------------ tự luận
def fetch_img(url):
    IMG.mkdir(parents=True, exist_ok=True)
    h = hashlib.md5(url.encode()).hexdigest()[:16]
    dst = IMG / f'{h}.jpg'
    if not dst.exists():
        raw = IMG / f'{h}.src'
        r = subprocess.run(['curl', '-sS', '-L', '-m', '40', '-o', str(raw), url], capture_output=True, text=True)
        try:
            im = Image.open(raw).convert('L')
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            im.save(dst, 'JPEG', quality=78, optimize=True)
        except Exception as e:
            print('  ! ảnh lỗi', url, e); return None
        finally:
            raw.unlink(missing_ok=True)
    return f'../assets/img/{h}.jpg'


def strip_attrs(el):
    for t in el.find_all(True):
        if t.name == 'img':
            src = t.get('src', '')
            local = fetch_img(src) if src.startswith('http') else src
            t.attrs = {'src': local or '', 'class': ['pimg']}
        elif t.name in ('td', 'th'):
            t.attrs = {k: v for k, v in t.attrs.items() if k in ('colspan', 'rowspan')}
        else:
            t.attrs = {}


def prob_html(raw):
    raw = re.sub(r'</?strong>', '', raw)
    segs = [x for x in re.split(r'\s*<br\s*/?>\s*', raw) if re.sub(r'<[^>]+>|\s', '', x) or '<img' in x]
    # bỏ "Bài n." đầu đề (đã có huy hiệu); giữ nguồn trích dẫn
    if segs:
        segs[0] = re.sub(r'(?:(<img[^>]*>)\s*)?Bài\s*\d+\s*[.:]*\s*', lambda m: (m.group(1) or ''), segs[0], count=1)
        segs[0] = re.sub(r'<em>\s*(\(Trích[^<]*\))\s*</em>', r'<span class="src">\1</span> ', segs[0])
        segs[0] = re.sub(r'^\s*:\s*', '', segs[0])
    rest = segs[1:]
    if len(rest) >= 2:
        out, label = [], 0
        for sgm in rest:
            plain_t = re.sub(r'<[^>]+>', '', sgm).strip()
            if plain_t.endswith(':') and label == 0:
                out.append(sgm); continue
            out.append(f'<span class="sub-l">{chr(97+label)})</span> {sgm}'); label += 1
        rest = out
    return ''.join(f'<p>{x}</p>' for x in ([segs[0]] if segs else []) + rest)


def render_tuluan(tl, lid, keys):
    if not tl or not tl.get('body_html'):
        return ''
    html = tl['body_html']
    html = bw.to_print(html)
    html, store = protect_svgs(html)
    soup = soup_of(html)
    items, cur = [], None
    for el in soup.children:
        if not isinstance(el, Tag): continue
        if el.name == 'h4':
            cur = {'title': plain(el), 'prob': '', 'sol': ''}; items.append(cur)
        elif el.name == 'div' and el.find('table') and cur is not None:
            ths = el.find_all('th')
            block = ''
            for th in ths:
                strip_attrs(th)
                block += th.decode_contents()
            tds = el.find_all('td')
            cur['prob'] = block
        elif el.name == 'details' and cur is not None:
            s = el.find('summary')
            if s: s.extract()
            strip_attrs(el)
            cur['sol'] = el.decode_contents()
    picked, cnt = [], {}
    for it in items:
        mm = re.match(r'Bài\s*\d+\s*·\s*(.*)', it['title']); lv = mm.group(1) if mm else ''
        cnt[lv] = cnt.get(lv, 0) + 1
        if cnt[lv] <= 2: picked.append(it)
    skipped = len(items) - len(picked)
    items = picked
    out = []
    for it in items:
        m = re.match(r'Bài\s*(\d+)\s*·\s*(.*)', it['title'])
        num, lvl = (m.group(1), m.group(2)) if m else ('', '')
        stars, lvl_name = LEVEL.get(lvl, ('', lvl.upper()))
        prob = prob_html(it['prob'])
        sol_plain = re.sub(r'<[^>]+>|\$[^$]*\$', 'x', it['sol'])
        n_lines = max(3, min(6, round(len(sol_plain) / 110) + 2))
        kn = keys.add(kind='tuluan', tag=f'Bài {num}', body=it['sol'], where='Tự luyện')
        out.append(f'''<div class="tl-prob">
<div class="tp-h"><span class="tp-n">BÀI {num}</span><span class="lvl">{stars} {lvl_name}</span><span class="tp-k">đáp án số {kn} · cuối bài</span></div>
<div class="tp-t">{prob}</div>
<div class="tp-w">{dl(n_lines)}</div></div>''')
    if skipped:
        out.append(f'<p class="more-web">Còn {skipped} bài tự luyện khác (đủ ba mức) trên web — quét mã QR đầu bài.</p>')
    return restore_svgs('\n'.join(out), store)


# ------------------------------------------------------------------ đáp án
def render_keys(keys, lid):
    if not keys.items and not keys.formulas: return ''
    rows = []
    for k in keys.items:
        n = k['n']; where = f'mục {k["where"]}' if k.get('where') else ''
        if k['kind'] == 'quiz':
            no = f'<p class="k-no"><b>Nếu em chọn sai:</b> {k["no"]}</p>' if k['no'] else ''
            ok = k['ok']
            rows.append(f'<div class="k"><div class="k-h"><span class="k-n">{n}</span><span class="k-t">{k["tag"].capitalize()} <small>{where}</small></span><span class="k-a">{k["letter"]}</span></div><div class="k-b">{ok}{no}</div></div>')
        elif k['kind'] == 'bt':
            rows.append(f'<div class="k k-sol"><div class="k-h"><span class="k-n">{n}</span><span class="k-t">{k["tag"]} <small>{k["title"]}</small></span></div><div class="k-b">{k["body"]}</div></div>')
        elif k['kind'] == 'thuthach':
            rows.append(f'<div class="k"><div class="k-h"><span class="k-n">{n}</span><span class="k-t">Thử thách <small>{where}</small></span></div><div class="k-b"><p>{k["body"]}</p></div></div>')
        else:
            q = f'<p class="k-q">{k["q"]}</p>' if k.get('q') else ''
            rows.append(f'<div class="k"><div class="k-h"><span class="k-n">{n}</span><span class="k-t">{k["tag"]} <small>{where}</small></span></div><div class="k-b">{q}{k["body"]}</div></div>')
    fm = ''
    if keys.formulas:
        cells = ''.join(f'<div class="fm"><i class="fbn">{i}</i><span>{"$$" + f["tex"] + "$$" if f["display"] else "$" + f["tex"] + "$"}</span></div>'
                        for i, f in enumerate(keys.formulas, 1))
        fm = f'<div class="fm-box"><div class="fm-h">Công thức điền khuyết <small>(ô vuông nhỏ có số trong bài)</small></div><div class="fm-g">{cells}</div></div>'
    return ('<section class="keys"><header class="keys-h"><span class="keys-tag">ĐÁP ÁN &amp; GỢI Ý</span>'
            '<span class="keys-tip">Đáp án các câu hỏi và ô điền trong bài. Làm xong rồi mới mở. Luyện tập và lời giải bài tập: trên web.</span></header>'
            f'{fm}<div class="keys-c">{"".join(rows)}</div></section>')


# ------------------------------------------------------------------ trang bài
def head_html(title, start=1, extra=''):
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="../node_modules/katex/dist/katex.min.css">
<link rel="stylesheet" href="../node_modules/@fontsource/be-vietnam-pro/400.css">
<link rel="stylesheet" href="../node_modules/@fontsource/be-vietnam-pro/400-italic.css">
<link rel="stylesheet" href="../node_modules/@fontsource/be-vietnam-pro/500.css">
<link rel="stylesheet" href="../node_modules/@fontsource/be-vietnam-pro/700.css">
<link rel="stylesheet" href="../node_modules/@fontsource/be-vietnam-pro/800.css">
<link rel="stylesheet" href="../node_modules/@fontsource/bricolage-grotesque/700.css">
<link rel="stylesheet" href="../node_modules/@fontsource/bricolage-grotesque/800.css">
<link rel="stylesheet" href="../node_modules/@fontsource/caveat/600.css">
<link rel="stylesheet" href="book.css">
<style>body{{counter-reset:page {start - 1}}}{extra}</style>
<script src="../node_modules/katex/dist/katex.min.js"></script>
<script src="../node_modules/katex/dist/contrib/auto-render.min.js"></script>
<script src="../node_modules/qrcode-generator/dist/qrcode.js"></script>
<script>window.PagedConfig={{auto:false}}</script>
<script src="../node_modules/pagedjs/dist/paged.polyfill.js"></script>
<script src="book.js" defer></script>
</head><body data-start="{start}">'''


def build_lesson(lid, start=1, filler=False):
    L = load_lesson(lid)
    keys = Keys(); CUR['lid'] = lid
    marks = tiet_marks(lid, bool(L['bt']))
    theory, obj = convert_theory(L['theory'], lid, keys, marks)
    bt_html = tl_html = ''
    main = []
    if L['bt']:
        bt_html, main = render_bt(L['bt'], lid, keys, marks)
        tl_html = ''
    lt_html = render_luyen_them(L['bt'], lid, keys, main)
    keys_html = render_keys(keys, lid)
    chap = f'CHƯƠNG {CHAPTER["num"]} · {CHAPTER["title"].upper()}'
    idx = CHAPTER['lessons'].index(lid)
    minimap = ''.join('■' if i == idx else '□' for i in range(len(CHAPTER['lessons'])))
    obj_html = ''
    if obj:
        lis = ''.join(f'<li>{x}</li>' for x in obj['lis'])
        obj_html = f'<div class="objectives"><div class="ob-h">{bw.ICONS["target"]} Mục tiêu bài học</div><ul>{lis}</ul><p class="ob-t">{obj["tail"]}</p></div>'
        obj_html = bw.to_print(obj_html)
    nn = f'{L["num"]:02d}'
    hero = f'''<header class="lopen">
  <div class="lo-top"><span>{chap}</span><span>BÀI {L["num"]}</span></div>
  <div class="lo-num">{nn}</div>
  <h1 class="lo-title">{L["name"]}</h1>
  <div class="lo-qr"><span class="qr" data-url="{lesson_url(lid)}"></span><span class="qr-t">Quét mã<br>để xem mô phỏng<br>& làm bài trực tuyến</span></div>
</header>'''
    html = head_html(L['title'], start)
    html += f'''<section class="lesson" data-chap="{chap}" data-lesson="Bài {L['num']}. {L['name']}" data-map="{minimap}">
{hero}
{obj_html}
<div class="theory">{theory}</div>
</section>'''
    if bt_html:
        html += f'<section class="btsec"><div class="sec-band"><span class="sb-k">BÀI TẬP MẪU</span><span class="sb-t">Đọc đề · tách dữ liệu · chọn công thức · ghi lời giải cùng thầy cô</span></div>{bt_html}</section>'
    html += lt_html
    web = (f'<div class="websec"><div class="ws-i"><span class="qr" data-url="{lesson_url(lid)}"></span><div><div class="ws-h">Ở nhà: luyện tập &amp; giải đề</div>'
           '<p>Trắc nghiệm, tự luận ba mức, lời giải chi tiết, theo dõi tiến độ.</p></div></div>'
           f'<div class="ws-i"><span class="qr" data-url="{answers_url(lid)}"></span><div><div class="ws-h">Đáp án &amp; gợi ý</div>'
           '<p>Phân tích từng câu, ô điền, lời giải mọi Dạng. Làm xong rồi hãy quét.</p></div></div></div>')
    html += web
    if tl_html:
        html += f'<section class="tlsec"><div class="sec-band"><span class="sb-k">TỰ LUYỆN</span><span class="sb-t">Từ dễ đến khó · viết bài làm vào chỗ chấm</span></div>{tl_html}</section>'
    if filler:
        import front
        html += front.filler()
    html += '</body></html>'
    out = SRC / f'lesson-{lid}.html'
    out.write_text(html)
    return out, keys


def export_web(lid):
    """Đáp án & gợi ý cho trang /sach/dap-an/?bai=<id> (public/data/sach/dap-an-<id>.json)."""
    import json as _json
    bw.WEB = True
    try:
        L = load_lesson(lid); keys = Keys(); CUR['lid'] = lid
        convert_theory(L['theory'], lid, keys)
        items = []
        for k in keys.items:
            if k['kind'] not in ('quiz', 'selfq', 'fill', 'thuthach'): continue
            items.append({'n': k['n'], 'kind': k['kind'], 'tag': (k.get('tag') or '').capitalize() if k['kind'] == 'quiz' else k.get('tag', ''),
                          'where': k.get('where', ''), 'letter': k.get('letter', ''), 'q': k.get('q', ''),
                          'ok': k.get('ok', ''), 'no': k.get('no', ''), 'body': k.get('body', '')})
        worked = []
        bt = L['bt'] or {'dang_bai': []}
        main = dang_chung(lid, len(bt['dang_bai']))
        for i, x in enumerate(bt['dang_bai'], 1):
            parts = [p.strip() for p in x['label'].split('·')]
            worked.append({'n': i, 'label': ' · '.join(parts[:2]), 'title': ' · '.join(parts[2:]) or x.get('topic', ''),
                           'solution': x['solution_html'], 'answer': bw.to_print(dang_answer(x)),
                           'inClass': i in main, 'similarTo': 0 if i in main else similar_to(x, bt, main)})
    finally:
        bw.WEB = False
    data = {'lessonId': lid, 'title': L['title'], 'num': L['num'], 'name': L['name'],
            'chapter': f'CHƯƠNG {CHAPTER["num"]} · {CHAPTER["title"].upper()}',
            'formulas': [{'n': i, 'tex': f['tex'], 'display': f['display']} for i, f in enumerate(keys.formulas, 1)],
            'items': items, 'worked': worked}
    out = REPO / 'public' / 'sach-data' / f'dap-an-{lid}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(_json.dumps(data, ensure_ascii=False))
    return out, data


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'lesson':
        p, k = build_lesson(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1)
        print(p, len(k.items), 'đáp án')
    elif cmd == 'web':
        for lid in CHAPTER['lessons']:
            print(export_web(lid)[0])
    elif cmd == 'all':
        for lid in CHAPTER['lessons']:
            p, k = build_lesson(lid); print(p, len(k.items))
