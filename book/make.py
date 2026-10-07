#!/usr/bin/env python3
"""Dựng trọn chương: render từng bài (song song) → đánh số trang → ghép PDF.
   python3 make.py            (cả chương)
   python3 make.py 49 50      (chỉ một số bài, để thử)
"""
import json, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fitz
import build, front, assets_gen

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
FRONT_PAGES = 5   # bìa, cách dùng, mục lục, cách đọc hình, bản đồ chương


def render(html, pdf):
    r = subprocess.run(['node', 'render.mjs', str(html), str(pdf)], cwd=ROOT, capture_output=True, text=True)
    m = re.search(r'PAGES (\d+)', r.stdout)
    if r.returncode or not m or 'LỖI' in r.stdout:
        print(r.stdout, r.stderr); raise SystemExit(f'render lỗi: {html}')
    return int(m.group(1))


def lesson_job(lid, start, filler=False):
    p, keys = build.build_lesson(lid, start, filler=filler)
    n = render(p, OUT / f'lesson-{lid}.pdf')
    return lid, n


def main():
    only = [int(x) for x in sys.argv[1:]]
    lessons = only or build.CHAPTER['lessons']
    t0 = time.time()
    # 1) đếm trang (bắt buộc số chẵn: thêm trang nháp nếu lẻ)
    with ThreadPoolExecutor(3) as ex:
        res = dict(ex.map(lambda l: lesson_job(l, 1), lessons))
    fill = {l: False for l in lessons}   # không đệm trang trống: tiết kiệm giấy
    redo = []
    if redo:
        with ThreadPoolExecutor(3) as ex:
            r2 = dict(ex.map(lambda l: lesson_job(l, 1, True), redo))
        res.update(r2)
    print('đếm trang:', res, f'{time.time()-t0:.0f}s')
    # 2) vị trí bắt đầu mỗi bài
    pages, cur = {}, FRONT_PAGES + 1
    for l in lessons:
        pages[str(l)] = {'start': cur, 'n': res[l]}; cur += res[l]
    json.dump(pages, open(OUT / 'pages.json', 'w'), indent=1)
    # 3) dựng lại với số trang thật
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(lambda l: lesson_job(l, pages[str(l)]['start'], fill[l]), lessons))
    answers = {l: build.export_web(l)[1] for l in lessons}   # cùng nguồn với public/sach-data/dap-an-<id>.json
    # 4) phần đầu / cuối
    take = []
    for l in lessons:
        L = build.load_lesson(l)
        m = re.search(r'<div class="tl-box tl-box--rule">\s*<p class="tl-label">[^<]*Mang về[^<]*</p>(.*?)</div>', L['theory'], re.S)
        if m: take.append((L['num'], L['name'], bw_clean(m.group(1))))
    back_start = FRONT_PAGES + 1 + sum(res[l] for l in lessons)
    front.build_back(pages, take, answers, back_start); n_back = render(ROOT / 'src/back.html', OUT / 'back.pdf')
    # mục lục đủ: trang mục con lấy từ PDF đã dựng (bài tập mẫu, luyện thêm, tổng kết, tự đánh giá, bảng đáp án)
    toc = {'sections': {}, 'back': {}}
    for l in lessons:
        toc['sections'][l] = {k: page_of(OUT / f'lesson-{l}.pdf', t, pages[str(l)]['start'])
                              for k, t in (('bt', 'BÀI TẬP MẪU'), ('lt', 'LUYỆN THÊM'))}
    for k, t in (('sum', 'TỔNG KẾT CHƯƠNG'), ('self', 'TỰ ĐÁNH GIÁ'), ('ak', 'BẢNG ĐÁP ÁN')):
        toc['back'][k] = page_of(OUT / 'back.pdf', t, back_start)
    front.build_front(pages, toc); n_front = render(ROOT / 'src/front.html', OUT / 'front.pdf')
    if n_front != FRONT_PAGES:
        raise SystemExit(f'phần đầu sách {n_front} trang, make.py đang giả định FRONT_PAGES={FRONT_PAGES} — sửa hằng rồi chạy lại')
    # 5) ghép
    book = fitz.open()
    toc = []
    def add(pdf, title=None):
        d = fitz.open(pdf); start = len(book); book.insert_pdf(d)
        if title: toc.append([1, title, start + 1])
    add(OUT / 'front.pdf', 'Bìa & phần đầu')
    for l in lessons:
        L = build.load_lesson(l); add(OUT / f'lesson-{l}.pdf', L['title'])
    add(OUT / 'back.pdf', 'Tổng kết chương, tự đánh giá & bảng đáp án')
    book.set_toc(toc)
    out = OUT / 'vat-li-10-chuong-2-dong-hoc.pdf'
    book.save(out, deflate=True, garbage=3)
    print('XONG', out, len(book), 'trang', f'{time.time()-t0:.0f}s')


def page_of(pdf, text, start):
    """Số trang (trong sách) của trang đầu tiên chứa `text` trong một PDF con; 0 nếu không có."""
    d = fitz.open(pdf); key = re.sub(r'\s+', '', text)   # chữ dãn (letter-spacing) bị tách "T Ổ N G" khi trích
    for i, pg in enumerate(d):
        if key in re.sub(r'\s+', '', pg.get_text()): return start + i
    return 0


def bw_clean(h):
    import bw
    return bw.to_print(h)


if __name__ == '__main__':
    main()
