#!/usr/bin/env python3
"""Hồ sơ sách, sổ khoá và soát lệch sách ↔ web.

  python3 sach.py list                 → các cuốn có hồ sơ trong book/sach/
  python3 sach.py lech <mã>            → tải nội dung web (DB) về book/cache rồi so với sổ khoá
  python3 sach.py lech <mã> --khong-tai  → chỉ so cache đang có (không gọi mạng)

Hồ sơ  book/sach/<mã>.json       : thầy chỉnh (bài nào, Dạng chung, vạch tiết, chữ bìa, bản đồ chương, tự đánh giá).
Sổ khoá book/sach/<mã>.lock.json : make.py ghi sau khi dựng trọn cuốn — sách đang có dựng từ bản nội dung nào.
Cache  book/cache/<lesson>.json  : bản web thật, do `npx tsx book/lay-noi-dung.mts <mã>` tải (gitignore).
Thiết kế: docs/THIET-KE-SKILL-SACH-DONG-BO.md
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SACH = ROOT / 'sach'
CACHE = ROOT / 'cache'
BTM_FIELDS = ('label', 'topic', 'problem_html', 'analysis_html', 'solution_html')   # phần của một Dạng mà sách dùng


def ds():
    return sorted(p.stem for p in SACH.glob('*.json') if not p.name.endswith('.lock.json'))


def ho_so(ma):
    p = SACH / f'{ma}.json'
    if not p.exists():
        raise SystemExit(f'không có hồ sơ sách "{ma}" — đang có: {", ".join(ds()) or "(trống)"}')
    d = json.load(open(p))
    for k in ('lop', 'chuong', 'ten', 'lessons'):
        if k not in d: raise SystemExit(f'{p.name}: thiếu trường "{k}"')
    d['ma'] = ma
    d['lessons'] = [int(x) for x in d['lessons']]
    for k in ('dang_chung', 'tiet'):
        d[k] = {int(a): b for a, b in (d.get(k) or {}).items()}
    return d


def khoa_path(ma): return SACH / f'{ma}.lock.json'


def doc_khoa(ma):
    p = khoa_path(ma)
    return json.load(open(p)) if p.exists() else {}


def doc_cache(lid):
    p = CACHE / f'{lid}.json'
    if not p.exists():
        raise SystemExit(f'chưa có book/cache/{lid}.json — tải nội dung web trước: npx tsx book/lay-noi-dung.mts <mã>')
    return json.load(open(p))


def van_tay(s):
    """Dấu vân tay nội dung; chuẩn hoá khoảng trắng để đổi format không tính là lệch."""
    return hashlib.sha256(re.sub(r'\s+', ' ', s or '').strip().encode()).hexdigest()[:16]


def btm_gon(dang_bai):
    return [{k: (x.get(k) or '') for k in BTM_FIELDS} for x in (dang_bai or [])]


def van_tay_bai(c):
    return {'ly_thuyet': van_tay(c.get('theory', '')),
            'btm': van_tay(json.dumps(btm_gon(c.get('dang_bai')), ensure_ascii=False, sort_keys=True))}


def bo_dem(data):
    """Bộ đếm quyết định ĐÁNH SỐ trong sách (đổi là sách đã phát lệch số với đáp án)."""
    return {'o_dien': len(data['formulas']), 'cau': sum(1 for it in data['items'] if it['kind'] == 'quiz'),
            'dang': len(data['worked'])}


def soat(ma):
    """So cache hiện có với sổ khoá. Trả [(lid, tên, phần, mức, ghi chú)]; mức: khớp | chữ | đánh số | mới."""
    import build
    build.use(ma)
    hs, khoa = build.SACH, doc_khoa(ma)
    rows = []
    for lid in hs['lessons']:
        c = doc_cache(lid); vt = van_tay_bai(c); cu = (khoa.get('bai') or {}).get(str(lid))
        repo = REPO / f'scripts/data/bai-tap-mau/{lid}.json'
        nhap = ''
        if repo.exists():
            r = van_tay(json.dumps(btm_gon(json.load(open(repo)).get('dang_bai')), ensure_ascii=False, sort_keys=True))
            if r != vt['btm']: nhap = 'repo có bản bài tập mẫu KHÁC bản đã đăng (sách theo web)'
        if not cu:
            rows.append((lid, c['title'], '—', 'mới', nhap or 'chưa từng dựng')); continue
        lech = [k for k in ('ly_thuyet', 'btm') if cu.get(k) != vt[k]]
        if not lech:
            rows.append((lid, c['title'], '—', 'khớp', nhap)); continue
        dem = bo_dem(build.answers_data(lid))
        doi = [f'{k} {cu.get(k)}→{dem[k]}' for k in ('o_dien', 'cau', 'dang') if cu.get(k) != dem[k]]
        phan = ' + '.join({'ly_thuyet': 'Lý thuyết', 'btm': 'Bài tập mẫu'}[k] for k in lech)
        rows.append((lid, c['title'], phan, 'đánh số' if doi else 'chữ', '; '.join(doi + ([nhap] if nhap else []))))
    return rows


def in_bang(ma, rows):
    khoa = doc_khoa(ma)
    print(f'\nSách {ma} · ' + (f'bản {khoa["ban"]} dựng {khoa["ngay"]}, {khoa["tong_trang"]} trang' if khoa else 'chưa có sổ khoá (chưa dựng lần nào)'))
    for lid, ten, phan, muc, ghi in rows:
        print(f'  {lid:>4}  {muc:<8} {phan:<24} {ten[:44]:<44} {ghi}')
    dem = {m: sum(1 for r in rows if r[3] == m) for m in ('khớp', 'chữ', 'đánh số', 'mới')}
    print('  → ' + ' · '.join(f'{k}: {v}' for k, v in dem.items() if v))
    if dem['đánh số']: print('  ĐÁNH SỐ đổi: dựng lại sẽ tăng số bản; sách đã phát giữ đáp án bản cũ.')
    elif dem['chữ'] or dem['mới']: print(f'  Dựng lại: python3 make.py {ma}')
    else: print('  Sách khớp web — không cần dựng lại.')


def main():
    a = sys.argv[1:]
    if not a or a[0] == 'list':
        for ma in ds():
            h = ho_so(ma); k = doc_khoa(ma)
            print(f'{ma:<28} Vật lí {h["lop"]} · Chương {h["chuong"]} · {h["ten"]} · {len(h["lessons"])} bài · '
                  + (f'bản {k["ban"]} ({k["ngay"]})' if k else 'chưa dựng'))
        return
    if a[0] == 'lech' and len(a) > 1:
        ma = a[1]; ho_so(ma)
        if '--khong-tai' not in a:
            r = subprocess.run(['npx', 'tsx', 'book/lay-noi-dung.mts', ma], cwd=REPO)
            if r.returncode: raise SystemExit('không tải được nội dung web (cần mạng + .env.local; chạy trong tab terminal, không qua sandbox)')
        in_bang(ma, soat(ma)); return
    raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
