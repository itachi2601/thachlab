#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_bundle.py — Ghép "draft đề" (JSON do trợ lý soạn) thành gói
`thachlab.lesson-bundle/v1` dán vào /quan-tri/nhap-bai, và chạy sẵn bộ kiểm tra
mà trang admin sẽ chạy (validateBundle trong services/lesson-import.ts) để bắt lỗi
TRƯỚC khi mở trình duyệt.

    python3 build_bundle.py draft.json -o bundle.json

## draft.json — trợ lý soạn file này

{
  "meta": {
    "title": "Kiểm tra: Chuyển động biến đổi đều & Rơi tự do",   // bắt buộc
    "topic": "Chuyển động biến đổi đều · Rơi tự do",              // nên có
    "difficulty": "" | "de" | "trung-binh" | "kho",               // mặc định ""
    "duration_minutes": 45,                                       // mặc định 20
    "subject_code": "vat-ly"                                      // mặc định "vat-ly"
  },
  "theory_html": "<h2 ...>Công thức trọng tâm</h2>...",   // bắt buộc, non-empty (validator chặn nếu rỗng)
  "questions": [
    { "type": "multiple_choice",
      "topic": "Chuyển động biến đổi đều",   // tên chủ đề con — khớp danh mục question_topics của lớp
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
  "raster_images": [                                            // chỉ ảnh chụp/scan thật; đồ thị -> SVG trong HTML
    { "name": "do-thi-v-t.jpg", "dataUri": "data:image/jpeg;base64,…",
      "alt": "Đồ thị v-t", "placeholder": "media/do-thi-v-t.jpg" }
  ]
}

`question` / `explanation` là văn bản thường thì script tự bọc <p>; nếu đã có thẻ HTML
thì để nguyên. `options` và `statements[].text` giữ nguyên chuỗi (KaTeX đọc $...$).
"""
import argparse
import json
import re
import sys

SCHEMA = "thachlab.lesson-bundle/v1"
P_CLS = 'text-base leading-relaxed my-2'

LEFTOVER = [
    (r'\\includegraphics\{', r'\includegraphics{…}'),
    (r'\\begin\{tabular\}', r'\begin{tabular}'),
    (r'\\section\{|\\subsection\{', r'\section{…}'),
    (r'\\\[|\\\]', r'\[ … \]'),
    (r'\\textbf\{|\\textit\{', r'\textbf{…}'),
]


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


def check_question(q, i, errors, warnings):
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

    # Nhãn phân tích (không chặn — nhưng thiếu thì mất số liệu "chủ đề yếu")
    if not str(q.get('topic', '')).strip():
        warnings.append(f'{label}: thiếu "topic" (tên chủ đề con) — cần cho phân tích chủ đề.')
    if q.get('form') not in ('ly_thuyet', 'bai_tap'):
        warnings.append(f'{label}: "form" nên là "ly_thuyet" hoặc "bai_tap".')

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
    if not theory:
        die('theory_html trống — trang admin bắt buộc mục Lý thuyết. '
            'Soạn một khối "Công thức trọng tâm" ngắn cho chủ đề của đề.')

    questions = d.get('questions')
    if not isinstance(questions, list) or not questions:
        die('questions trống.')

    errors, warnings = [], []
    scan_html(theory, 'Lý thuyết', errors)

    norm_q = []
    for i, q in enumerate(questions):
        q = dict(q)
        q['question'] = as_p(q.get('question', ''))
        if q.get('explanation'):
            q['explanation'] = as_p(q['explanation'])
        check_question(q, i, errors, warnings)
        norm_q.append(q)

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
    print(f'\n✓ {a.out} — {len(norm_q)} câu ({summary}), {len(imgs)} ảnh. '
          f'Không có lỗi. Mở /quan-tri/nhap-bai và dán file này.')


if __name__ == '__main__':
    main()
