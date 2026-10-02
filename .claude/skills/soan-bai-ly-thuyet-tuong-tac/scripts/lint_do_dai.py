#!/usr/bin/env python3
"""Kiểm ĐỘ DÀI bài lý thuyết tương tác — hạn mức ở `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`.

Dùng:
    python3 lint_do_dai.py <theory.html> [<theory.html> ...] [--wpm 140] [--json] [--khong-canh-bao]

Không cần trình duyệt. Đo:
  - tổng từ, **từ hiện ngay** (bỏ nội dung trong `<details>`, GIỮ `<summary>` vì câu hỏi/hộp
    "xem thêm" là chữ học sinh thật sự nhìn thấy), phút đọc ước tính;
  - mỗi mục `<h3>`: từ hiện ngay / tổng, số **nhịp** (`<details>` · `.tl-quiz` · `<figure>`),
    **đoạn liền dài nhất** = số từ nhìn thấy giữa hai nhịp liên tiếp.

Thoát 1 nếu có lỗi cứng (✗); cảnh báo (⚠) không đổi exit code.
Vì sao các ngưỡng này: xem bảng "Hạn mức" trong tài liệu trên (số đo 5 bài mẫu 2/10/2026).
"""
import argparse, html, json, os, re, sys

WPM = 140                  # từ/phút khi đọc chữ Việt trên điện thoại, có công thức phải dừng nghĩ

TONG_WARN, TONG_ERR = 2000, 2500      # từ hiện ngay cả bài  (~14 phút / ~18 phút)
MUC_WARN, MUC_ERR = 400, 600          # từ hiện ngay một mục  (~3 phút / ~4,3 phút)
BTM_WARN, BTM_ERR = 600, 900          # mục "Bài toán mẫu" — đây là đoạn BUỘC đọc liền có chủ đích
LIEN_WARN, LIEN_ERR = 300, 400        # từ liền không có nhịp nào (~2 phút / ~2,9 phút)
QUIZ_MIN, QUIZ_MAX = 4, 8
MUC_MIN, MUC_MAX = 6, 8
DETAILS_MIN, HINH_MIN = 4, 2

NHIP = re.compile(r'<details\b|class="tl-quiz|<figure\b', re.I)
DETAILS = re.compile(r'<details\b.*?</details>', re.S | re.I)
SUMMARY = re.compile(r'<summary\b[^>]*>(.*?)</summary>', re.S | re.I)
SVG = re.compile(r'<svg\b.*?</svg>', re.S | re.I)
COMMENT = re.compile(r'<!--.*?-->', re.S)


def _text(s):
    s = COMMENT.sub(" ", s)
    s = SVG.sub(" ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)


def dem_tu(s):
    return len(_text(s).split())


def hien_ngay(s):
    """Bỏ nội dung trong <details>, giữ lại <summary> (chữ học sinh thấy khi chưa bấm)."""
    ra, i = [], 0
    for m in DETAILS.finditer(s):
        ra.append(s[i:m.start()])
        sm = SUMMARY.search(m.group(0))
        if sm:
            ra.append(sm.group(1))
        i = m.end()
    ra.append(s[i:])
    return "".join(ra)


def tach_muc(t):
    ra = []
    for p in re.split(r"<h3\b[^>]*>", t)[1:]:
        dau, _, than = p.partition("</h3>")
        tieu_de = re.sub(r"\s+", " ", _text(dau)).strip()
        if len(tieu_de) > 58:
            tieu_de = tieu_de[:57].rstrip() + "…"
        ra.append((tieu_de, than))
    return ra


def do_muc(than):
    """Trả (từ hiện ngay, tổng từ, số nhịp, đoạn liền dài nhất)."""
    prev, doan, nhip = 0, [], 0
    for m in NHIP.finditer(than):
        seg = than[prev:m.start()]
        if m.group(0).lower().startswith("<details"):
            khoi = DETAILS.match(than, m.start())   # đúng khối details này, không nhảy sang khối sau
            sm = SUMMARY.search(khoi.group(0)) if khoi else None
            if sm:
                seg += sm.group(1)
        doan.append(dem_tu(seg))
        nhip += 1
        prev = m.end()
    doan.append(dem_tu(than[prev:]))
    return dem_tu(hien_ngay(than)), dem_tu(than), nhip, (max(doan) if doan else 0)


def kiem(path):
    t = open(path, encoding="utf8").read()
    hien, tong = dem_tu(hien_ngay(t)), dem_tu(t)
    muc = tach_muc(t)
    quiz = len(re.findall(r"tl-quiz", t))
    hinh = len(re.findall(r"<figure\b", t))
    details = len(re.findall(r"<details\b", t))
    loi, canh_bao, hang = [], [], []

    for ten, than in muc:
        h, tg, nhip, lien = do_muc(than)
        btm = "bài toán mẫu" in ten.lower()
        mw, me = (BTM_WARN, BTM_ERR) if btm else (MUC_WARN, MUC_ERR)
        hang.append((ten, h, tg, nhip, lien))
        if h > me:
            loi.append(f'mục "{ten}": {h} từ hiện ngay > {me} — tách thành 2 mục con')
        elif h > mw:
            canh_bao.append(f'mục "{ten}": {h} từ hiện ngay > {mw} — cân nhắc tách mục')
        if lien > LIEN_ERR:
            loi.append(f'mục "{ten}": đoạn liền {lien} từ không có nhịp nào > {LIEN_ERR}')
        elif lien > LIEN_WARN:
            canh_bao.append(f'mục "{ten}": đoạn liền {lien} từ > {LIEN_WARN} — chèn quiz/details/hình')
        if nhip == 0:
            canh_bao.append(f'mục "{ten}": không có nhịp nào (details/quiz/hình)')

    if not muc:
        loi.append("không có <h3> mốc I., II.…")
    if hien > TONG_ERR:
        loi.append(f"tổng {hien} từ hiện ngay > {TONG_ERR} (~{hien / WPM:.0f} phút) — cắt hoặc tách bài")
    elif hien > TONG_WARN:
        canh_bao.append(f"tổng {hien} từ hiện ngay > {TONG_WARN} (~{hien / WPM:.0f} phút) — gần trần")
    if quiz > QUIZ_MAX:
        loi.append(f"{quiz} quiz > {QUIZ_MAX} — quá tải, bỏ bớt")
    elif quiz < QUIZ_MIN:
        canh_bao.append(f"chỉ {quiz} quiz < {QUIZ_MIN}")
    if not (MUC_MIN <= len(muc) <= MUC_MAX):
        canh_bao.append(f"{len(muc)} mục, ngoài khoảng {MUC_MIN}–{MUC_MAX}")
    if details < DETAILS_MIN:
        canh_bao.append(f"chỉ {details} <details> < {DETAILS_MIN} (mất phần mở rộng cho HS khá)")
    if hinh < HINH_MIN:
        canh_bao.append(f"chỉ {hinh} hình < {HINH_MIN}")

    return dict(file=path, hien=hien, tong=tong, muc=muc.__len__(), quiz=quiz, hinh=hinh,
                details=details, phut=hien / WPM, hang=hang, loi=loi, canh_bao=canh_bao)


def nghin(n):
    return f"{n:,}".replace(",", ".")


def in_nguoi(kq, chi_loi=False):
    print(f"\n{kq['file']}")
    print(f"  {nghin(kq['hien'])} từ hiện ngay / {nghin(kq['tong'])} từ tổng · ~{kq['phut']:.1f} phút "
          f"· {kq['muc']} mục · {kq['quiz']} quiz · {kq['hinh']} hình · {kq['details']} details")
    print(f"  {'mục':<60} {'hiện':>6} {'tổng':>6} {'nhịp':>5} {'liền':>5}")
    for ten, h, tg, nhip, lien in kq["hang"]:
        co = "✗" if lien > LIEN_ERR else ("⚠" if lien > LIEN_WARN else " ")
        print(f"  {ten:<60} {nghin(h):>6} {nghin(tg):>6} {nhip:>5} {lien:>5} {co}")
    if not chi_loi:
        for c in kq["canh_bao"]:
            print("  ⚠", c)
    for e in kq["loi"]:
        print("  ✗", e)


def main():
    global WPM
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--wpm", type=int, default=WPM, help="từ/phút để ước tính thời gian đọc")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--khong-canh-bao", action="store_true", help="chỉ in lỗi cứng")
    a = ap.parse_args()
    WPM = a.wpm

    kqs = [kiem(f) for f in a.files]
    if a.json:
        print(json.dumps(kqs, ensure_ascii=False, indent=2))
    else:
        for kq in kqs:
            in_nguoi(kq, chi_loi=a.khong_canh_bao)
        n_loi = sum(len(k["loi"]) for k in kqs)
        n_cb = sum(len(k["canh_bao"]) for k in kqs)
        print(f"\n{len(kqs)} bài · {n_loi} lỗi cứng · {n_cb} cảnh báo"
              + ("  [--khong-canh-bao]" if a.khong_canh_bao else ""))
    return 1 if any(k["loi"] for k in kqs) else 0


if __name__ == "__main__":
    sys.exit(main())
