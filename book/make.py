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
FRONT_PAGES = 4


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
    for l in lessons: build.export_web(l)
    # 4) phần đầu / cuối
    front.build_front(pages); render(ROOT / 'src/front.html', OUT / 'front.pdf')
    take = []
    for l in lessons:
        L = build.load_lesson(l)
        m = re.search(r'<div class="tl-box tl-box--rule">\s*<p class="tl-label">[^<]*Mang về[^<]*</p>(.*?)</div>', L['theory'], re.S)
        if m: take.append((L['num'], L['name'], bw_clean(m.group(1))))
    front.build_back(pages, take); n_back = render(ROOT / 'src/back.html', OUT / 'back.pdf')
    # 5) ghép
    book = fitz.open()
    toc = []
    def add(pdf, title=None):
        d = fitz.open(pdf); start = len(book); book.insert_pdf(d)
        if title: toc.append([1, title, start + 1])
    add(OUT / 'front.pdf', 'Bìa & phần đầu')
    for l in lessons:
        L = build.load_lesson(l); add(OUT / f'lesson-{l}.pdf', L['title'])
    add(OUT / 'back.pdf', 'Tổng kết chương & tự đánh giá')
    book.set_toc(toc)
    out = OUT / 'vat-li-10-chuong-2-dong-hoc.pdf'
    book.save(out, deflate=True, garbage=3)
    print('XONG', out, len(book), 'trang', f'{time.time()-t0:.0f}s')


def bw_clean(h):
    import bw
    return bw.to_print(h)


if __name__ == '__main__':
    main()
