#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_bundle.py — Ghép "draft đề" (JSON do trợ lý soạn) thành gói
`thachlab.lesson-bundle/v1` dán vào /quan-tri/nhap-bai, và chạy sẵn bộ kiểm tra
mà trang admin sẽ chạy (validateBundle trong services/lesson-import.ts) để bắt lỗi
TRƯỚC khi mở trình duyệt.

    python3 build_bundle.py draft.json --grade 12 -o bundle.json

`--grade` để script tải danh mục chủ đề của khối (REST anon-key, tự đọc .env.local) rồi
**soát tên `topic` của từng câu**: sai chính tả / không có trong danh mục là LỖI, vì
`ExamRunner` tra `topic_id` theo đúng tên — lệch một chữ là câu đó rơi khỏi phân tích chủ
đề và cảnh báo phụ đạo mà không báo gì. Danh mục có hai tầng (bài học → yêu cầu cần đạt):
gắn vào **yêu cầu cần đạt**; gắn ở mức cả bài chỉ là cảnh báo, không chặn. Chủ đề thật sự
mới thì khai báo có ý thức:

    python3 build_bundle.py draft.json --grade 12 --new-topic "Hiệu suất động cơ nhiệt"

Cờ khác: `--topics topics.json` (dùng danh mục tải sẵn, khỏi gọi mạng),
`--allow-untagged` (hạ mọi lỗi nhãn xuống cảnh báo — chỉ khi thầy chấp nhận mất số liệu).

## draft.json — trợ lý soạn file này

{
  "meta": {
    "title": "Kiểm tra: Chuyển động biến đổi đều & Rơi tự do",   // bắt buộc
    "topic": "Chuyển động biến đổi đều · Rơi tự do",              // nên có
    "difficulty": "" | "de" | "trung-binh" | "kho",               // mặc định ""
    "duration_minutes": 45,                                       // mặc định 20
    "subject_code": "vat-ly"                                      // mặc định "vat-ly"
  },
  "theory_html": "<h2 ...>Công thức trọng tâm</h2>...",   // để "" nếu chỉ đăng đề (mục Lý thuyết của bài giữ nguyên)
  "questions": [
    { "type": "multiple_choice",
      "topic": "Các công thức của chuyển động thẳng biến đổi đều",  // tên yêu cầu cần đạt, khớp question_topics của khối
      "form": "bai_tap",                      // "ly_thuyet" | "bai_tap"
      "question": "Công thức tính quãng đường ... là",
      "options": ["$s=v_0t+\\frac12at^2$", "…", "…", "…"],   // ĐÚNG 4
      "answer": 0,                                            // chỉ số 0..3 của phương án đúng
      "explanation": "…" },                                    // bắt buộc
    { "type": "true_false",
      "question": "Xét các phát biểu về rơi tự do:",
      "statements": [
        { "text": "…", "answer": true },
        { "text": "…", "answer": false },
        { "text": "…", "answer": true },
        { "text": "…", "answer": false } ],                    // ĐÚNG 4
      "explanation": "…" },
    { "type": "short_answer",
      "question": "… (ghi số, làm tròn 1 chữ số thập phân)",
      "answer": "3,4",                                         // chuỗi số, ≤ 4 ký tự, phẩy thập phân
      "explanation": "…" }
  ],
  "raster_images": [                                            // ưu tiên: ảnh trích thẳng từ file gốc (docx media / pdfimages); chỉ vẽ SVG khi không trích được
    { "name": "do-thi-v-t.jpg", "dataUri": "data:image/jpeg;base64,…",
      "alt": "Đồ thị v-t", "placeholder": "media/do-thi-v-t.jpg" }
  ]
}

`question` / `explanation` là văn bản thường thì script tự bọc <p>; nếu đã có thẻ HTML
thì để nguyên. `options` và `statements[].text` giữ nguyên chuỗi (KaTeX đọc $...$).
"""
import argparse
import difflib
import json
import os
import re
import sys
import urllib.parse
import urllib.request

SCHEMA = "thachlab.lesson-bundle/v1"
P_CLS = 'text-base leading-relaxed my-2'

LEFTOVER = [
    (r'\\includegraphics\{', r'\includegraphics{…}'),
    (r'\\begin\{tabular\}', r'\begin{tabular}'),
    (r'\\section\{|\\subsection\{', r'\section{…}'),
    (r'\\\[|\\\]', r'\[ … \]'),
    (r'\\textbf\{|\\textit\{', r'\textbf{…}'),
]


def clean_topic(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def topic_key(s):
    return clean_topic(s).lower()


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *(['..'] * 4)))


def env_value(key):
    v = os.environ.get(key)
    if v:
        return v
    try:
        with open(os.path.join(repo_root(), '.env.local'), encoding='utf-8') as f:
            for line in f:
                if line.startswith(key + '='):
                    return line.split('=', 1)[1].strip()
    except OSError:
        pass
    return None


def fetch_topics(grade):
    """Danh mục chủ đề của một khối, đọc bằng anon-key (chỉ SELECT). (rows, err)

    Danh mục hai tầng: hàng có parent_id = null là chủ đề của cả BÀI, hàng có
    parent_id là một YÊU CẦU CẦN ĐẠT trong bài đó. Câu hỏi nên gắn vào yêu cầu cần
    đạt cho mịn — mục phụ đạo vẫn gom lên tầng bài khi thống kê."""
    url = env_value('NEXT_PUBLIC_SUPABASE_URL')
    key = env_value('NEXT_PUBLIC_SUPABASE_ANON_KEY')
    if not url or not key:
        return None, 'không tìm thấy NEXT_PUBLIC_SUPABASE_URL / _ANON_KEY (env hoặc .env.local)'
    q = (url.rstrip('/') + '/rest/v1/question_topics?select=id,name,grade,parent_id&grade=eq.'
         + urllib.parse.quote(str(grade)))
    req = urllib.request.Request(q, headers={'apikey': key, 'Authorization': 'Bearer ' + key})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            rows = json.load(r)
    except Exception as e:
        return None, f'gọi REST lỗi: {e}'
    if not isinstance(rows, list):
        return None, f'REST trả về không phải danh sách: {rows}'
    return [r for r in rows if r.get('name')], None


def topics_from_file(path, grade):
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        die(f'không đọc được {path}: {e}')
    if isinstance(data, dict):
        data = data.get('topics') or data.get('data') or []
    rows = []
    for row in data:
        if isinstance(row, str):
            rows.append({'name': row})
        elif isinstance(row, dict) and row.get('name'):
            if grade and row.get('grade') and str(row['grade']) != str(grade):
                continue
            rows.append(row)
    return rows


def die(msg):
    print("LỖI: " + msg, file=sys.stderr)
    sys.exit(1)


def has_html(s):
    return bool(re.search(r'<[a-zA-Z/][^>]*>', s or ''))


def as_p(s):
    s = (s or '').strip()
    if not s:
        return ''
    if has_html(s):
        return s
    return f'<p class="{P_CLS}">{s}</p>'


def unbalanced_dollars(html):
    return len(re.findall(r'(?<!\\)\$', html)) % 2 != 0


def scan_html(html, label, errors):
    for pat, name in LEFTOVER:
        if re.search(pat, html):
            errors.append(f'{label}: còn sót LaTeX "{name}" — chuyển sang HTML/$...$ trước.')
    if unbalanced_dollars(html):
        errors.append(f'{label}: số dấu $ lẻ — công thức chưa đóng.')
    if re.search(r'<script\b|<style\b', html, re.I):
        errors.append(f'{label}: có <script>/<style> — không được phép.')
    if re.search(r'\son\w+\s*=', html, re.I):
        errors.append(f'{label}: có thuộc tính on*= (JS) — không được phép.')
    n = len(html.encode('utf-8'))
    if n > 1.5 * 1024 * 1024:
        errors.append(f'{label}: HTML quá lớn ({n // 1024} KB > 1.5 MB).')


def check_tags(q, label, ctx, errors, warnings):
    """Nhãn chủ đề + loại. Chỉ có giá trị khi `topic` khớp ĐÚNG tên trong danh mục:
    ExamRunner tra topic_id theo tên, mà tutoring_needs.topic_id là NOT NULL."""
    bad = warnings if ctx['allow_untagged'] else errors
    catalog = ctx['catalog']
    name = clean_topic(q.get('topic', ''))
    if not name:
        bad.append(f'{label}: thiếu "topic" — mỗi câu cần tên chủ đề khớp danh mục của khối.')
    elif catalog is None:
        q['topic'] = name
    else:
        key = topic_key(name)
        if key in catalog:
            q['topic'] = catalog[key]          # chuẩn hoá chính tả theo danh mục
            if key in ctx['coarse']:
                # Bài này đã tách yêu cầu cần đạt: gắn ở mức cả bài vẫn thống kê được,
                # chỉ là thầy không biết em hổng đúng phần nào. Nhắc, không chặn.
                ctx['coarse_used'].append(label)
                warnings.append(
                    f'{label}: "{catalog[key]}" là chủ đề của cả bài. Bài này có yêu cầu cần đạt: '
                    + ' | '.join(ctx['children'].get(key, [])[:6])
                    + ' — chọn đúng một yêu cầu thì phân tích mới chỉ ra được chỗ hổng.')
        elif key in ctx['new_keys']:
            q['topic'] = name
            ctx['new_used'][key] = name
        else:
            # Hay gặp nhất là gọi tắt ("Nội năng" ↔ "Nội năng. Định luật 1 …") — so khớp
            # chuỗi con trước, difflib chỉ bắt được lỗi chính tả.
            near = [v for k, v in catalog.items() if key in k or k in key]
            near += [m for m in difflib.get_close_matches(name, list(catalog.values()), n=3, cutoff=0.55)
                     if m not in near]
            hint = f' Gần nhất: {" | ".join(near[:3])}.' if near else ''
            bad.append(
                f'{label}: chủ đề "{name}" không có trong danh mục khối {ctx["grade"]}.{hint} '
                f'Sửa đúng tên, hoặc khai báo chủ đề mới: --new-topic "{name}".')
    if q.get('form') not in ('ly_thuyet', 'bai_tap'):
        bad.append(f'{label}: "form" phải là "ly_thuyet" hoặc "bai_tap".')


def check_question(q, i, errors, warnings, ctx):
    label = f'Câu {i + 1}'
    t = q.get('type')
    qtext = q.get('question', '')
    if not str(qtext).strip():
        errors.append(f'{label}: thiếu nội dung câu hỏi.')
    expl = str(q.get('explanation', '')).strip()
    if not expl and t != 'essay':
        warnings.append(f'{label}: thiếu lời giải (explanation).')
    for field in ('question', 'explanation'):
        if q.get(field):
            scan_html(str(q[field]), f'{label}.{field}', errors)

    check_tags(q, label, ctx, errors, warnings)

    if t == 'multiple_choice':
        opts = q.get('options')
        if not isinstance(opts, list) or len(opts) != 4:
            errors.append(f'{label}: trắc nghiệm phải có ĐÚNG 4 phương án.')
        a = q.get('answer')
        if not isinstance(a, int) or isinstance(a, bool) or a < 0 or a > 3:
            errors.append(f'{label}: answer phải là số nguyên 0..3 (chỉ số phương án đúng).')
        for j, o in enumerate(opts or []):
            if unbalanced_dollars(str(o)):
                errors.append(f'{label} phương án {"ABCD"[j] if j < 4 else j}: số dấu $ lẻ.')
    elif t == 'true_false':
        st = q.get('statements')
        if not isinstance(st, list) or len(st) != 4:
            errors.append(f'{label}: đúng/sai phải có ĐÚNG 4 ý.')
        else:
            for k, s in enumerate(st):
                if not isinstance(s, dict) or not isinstance(s.get('answer'), bool):
                    errors.append(f'{label} ý {"abcd"[k]}: cần answer là true/false.')
                if not str(s.get('text', '')).strip():
                    errors.append(f'{label} ý {"abcd"[k]}: thiếu nội dung.')
                elif unbalanced_dollars(str(s.get('text', ''))):
                    errors.append(f'{label} ý {"abcd"[k]}: số dấu $ lẻ.')
    elif t == 'short_answer':
        a = str(q.get('answer', '')).strip()
        if not a:
            errors.append(f'{label}: thiếu đáp án.')
        elif len(a) > 4:
            errors.append(f'{label}: đáp án "{a}" dài quá 4 ký tự.')
        elif not re.fullmatch(r'-?\d+([.,]\d+)?', a):
            warnings.append(f'{label}: đáp án "{a}" không phải dạng số — trang sẽ cảnh báo.')
    elif t == 'essay':
        warnings.append(f'{label}: câu tự luận không chấm tự động — tránh nếu không thật cần.')
    else:
        errors.append(f'{label}: loại câu không hợp lệ ("{t}"). Dùng multiple_choice | true_false | short_answer.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('draft')
    ap.add_argument('-o', '--out', default='bundle.json')
    ap.add_argument('--grade', help='khối của đề (9|10|11|12) — để tải & soát danh mục chủ đề')
    ap.add_argument('--topics', help='file JSON danh mục chủ đề tải sẵn (thay cho gọi REST)')
    ap.add_argument('--new-topic', action='append', default=[], metavar='TÊN',
                    help='khai báo một chủ đề CHƯA có trong danh mục (lặp lại được)')
    ap.add_argument('--allow-untagged', action='store_true',
                    help='hạ lỗi nhãn xuống cảnh báo — đề sẽ không vào phân tích chủ đề')
    a = ap.parse_args()

    try:
        d = json.load(open(a.draft, encoding='utf-8'))
    except Exception as e:
        die(f'không đọc được {a.draft}: {e}')

    meta = d.get('meta', {})
    title = str(meta.get('title', '')).strip()
    if not title:
        die('meta.title trống.')
    diff = meta.get('difficulty', '') or ''
    if diff not in ('', 'de', 'trung-binh', 'kho'):
        die(f'meta.difficulty không hợp lệ ("{diff}").')

    theory = str(d.get('theory_html', '')).strip()

    questions = d.get('questions')
    if not isinstance(questions, list) or not questions:
        die('questions trống.')

    errors, warnings = [], []
    if theory:
        scan_html(theory, 'Lý thuyết', errors)
    else:
        # Gói chỉ có đề vẫn hợp lệ: lúc đăng, mục Lý thuyết của bài được giữ nguyên.
        warnings.append('Gói không có theory_html — mục Lý thuyết của bài sẽ giữ nguyên.')

    # Danh mục chủ đề của khối: --topics (file) > --grade (REST) > không soát tên
    rows, catalog_note = None, None
    if a.topics:
        rows = topics_from_file(a.topics, a.grade)
        if not rows:
            die(f'{a.topics} không có tên chủ đề nào.')
    elif a.grade:
        rows, err = fetch_topics(a.grade)
        if rows is None:
            die(f'không tải được danh mục chủ đề khối {a.grade} ({err}). '
                f'Dùng --topics <file.json>, hoặc --allow-untagged nếu đành chịu.')
        if not rows:
            catalog_note = (f'danh mục chủ đề khối {a.grade} đang TRỐNG — thêm ở '
                            f'Quản trị → Chủ đề câu hỏi trước khi soát được tên.')
            rows = None
    else:
        catalog_note = ('chưa soát tên chủ đề (thiếu --grade hoặc --topics) — tên lệch một chữ '
                        'là câu đó rơi khỏi phân tích chủ đề mà không báo lỗi.')
    if catalog_note:
        warnings.append(catalog_note)

    # Chủ đề tầng bài đã có yêu cầu cần đạt con -> gắn nhãn ở mức đó là còn thô.
    coarse, children = set(), {}
    if rows:
        by_id = {r.get('id'): r for r in rows if r.get('id') is not None}
        for r in rows:
            parent = by_id.get(r.get('parent_id'))
            if parent is None:
                continue
            pkey = topic_key(str(parent['name']))
            coarse.add(pkey)
            children.setdefault(pkey, []).append(clean_topic(str(r['name'])))

    ctx = {
        'catalog': {topic_key(str(r['name'])): clean_topic(str(r['name'])) for r in rows} if rows else None,
        'coarse': coarse,
        'children': children,
        'coarse_used': [],
        'new_keys': {topic_key(n) for n in a.new_topic},
        'new_used': {},
        'grade': a.grade or '?',
        'allow_untagged': a.allow_untagged,
    }

    norm_q = []
    for i, q in enumerate(questions):
        q = dict(q)
        q['question'] = as_p(q.get('question', ''))
        if q.get('explanation'):
            q['explanation'] = as_p(q['explanation'])
        check_question(q, i, errors, warnings, ctx)
        norm_q.append(q)

    unused_new = [n for n in a.new_topic if topic_key(n) not in ctx['new_used']]
    for n in unused_new:
        warnings.append(f'--new-topic "{n}" khai báo nhưng không câu nào dùng — bỏ cờ này đi.')

    imgs = d.get('raster_images', []) or []
    declared = set()
    for i, img in enumerate(imgs):
        if not isinstance(img, dict):
            errors.append(f'Ảnh {i + 1}: không phải object.')
            continue
        if not str(img.get('dataUri', '')).startswith('data:image/'):
            errors.append(f'Ảnh {i + 1}: dataUri phải bắt đầu bằng "data:image/".')
        ph = str(img.get('placeholder', '')).strip()
        if not ph:
            errors.append(f'Ảnh {i + 1}: thiếu placeholder.')
        declared.add(ph)
        b64 = str(img.get('dataUri', '')).split(',', 1)[-1]
        if len(b64) * 0.75 > 1.5 * 1024 * 1024:
            errors.append(f'Ảnh {i + 1}: nặng > 1.5 MB — nén lại (~1400px, JPEG 0.8).')

    all_html = theory + '\n' + '\n'.join(
        str(q.get('question', '')) + str(q.get('explanation', '')) for q in norm_q)
    for m in re.findall(r'\bmedia/[\w./-]+', all_html):
        if m not in declared:
            errors.append(f'Placeholder ảnh "{m}" chưa khai báo trong raster_images.')

    bundle = {
        'schema': SCHEMA,
        'theory_title': meta.get('theory_title', 'Công thức trọng tâm'),
        'theory_html': theory,
        'worked_examples': [],
        'exam': {
            'title': title,
            'topic': str(meta.get('topic', '')).strip(),
            'difficulty': diff,
            'duration_minutes': int(meta.get('duration_minutes', 20) or 20),
            'subject_code': meta.get('subject_code', 'vat-ly') or 'vat-ly',
            'questions': norm_q,
            # Chủ đề chưa có trong danh mục — trang /quan-tri/nhap-bai sẽ tạo chúng
            # cho đúng Chương → Bài đang chọn khi đăng.
            'new_topics': sorted(ctx['new_used'].values()),
        },
        'raster_images': imgs,
    }

    counts = {}
    for q in norm_q:
        counts[q.get('type')] = counts.get(q.get('type'), 0) + 1
    summary = ' · '.join(f'{v} {k}' for k, v in counts.items())

    if warnings:
        print('CẢNH BÁO (không chặn đăng):')
        for w in warnings:
            print('  ! ' + w)
    if errors:
        print('\nLỖI (trang admin sẽ chặn Đăng — sửa draft rồi chạy lại):')
        for e in errors:
            print('  ✕ ' + e)
        sys.exit(1)

    json.dump(bundle, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tagged = sum(1 for q in norm_q
                 if clean_topic(q.get('topic', '')) and q.get('form') in ('ly_thuyet', 'bai_tap'))
    used = sorted({clean_topic(q.get('topic', '')) for q in norm_q if clean_topic(q.get('topic', ''))})
    new_used = sorted(ctx['new_used'].values())
    print(f'\n✓ {a.out} — {len(norm_q)} câu ({summary}), {len(imgs)} ảnh. Không có lỗi.')
    print(f'  Nhãn: {tagged}/{len(norm_q)} câu · {len(used)} chủ đề'
          + (f' ({len(new_used)} mới: {", ".join(new_used)})' if new_used else '')
          + (f' · {len(ctx["coarse_used"])} câu còn ở mức cả bài' if ctx['coarse_used'] else ''))
    if new_used:
        print('  Ở mục 3 trang nhập bài, để nguyên ô "Tạo chủ đề mới cho bài này".')
    print('  Mở /quan-tri/nhap-bai và dán file này.')


if __name__ == '__main__':
    main()
