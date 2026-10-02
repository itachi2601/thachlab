#!/usr/bin/env python3
"""Kiểm ĐỘ DÀI bài lý thuyết tương tác — hạn mức ở `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`.

Dùng:
    python3 lint_do_dai.py <theory.html> [<theory.html> ...] [--wpm 140] [--json] [--khong-canh-bao]

Không cần trình duyệt. Đo trên **chữ học sinh thật sự nhìn thấy khi mở trang**:
  - Bỏ nội dung trong `<details>` (chỉ giữ `<summary>`) và bỏ `<div class="tl-fb…">` (phản hồi
    quiz chỉ hiện sau khi chọn đáp án — CSS ẩn) và bỏ `<svg>`.
  - "Từ hiện ngay" = phần còn lại. Phút đọc = từ hiện ngay / `--wpm` (mặc định 140).
  - Mục: chia theo `<h3>` VÀ `<h4>` (mục con). `<h3>` có mục con thì chỉ là dòng nhóm, không tính
    hạn mức — vì người đọc thấy tiêu đề con ngắt đoạn.
  - Nhịp = `<details>` · `.tl-quiz` · `<figure>`. "Đoạn liền" = số từ hiện ngay giữa hai nhịp liên
    tiếp; tiêu đề KHÔNG tính là nhịp (tiêu đề không cho học sinh làm gì).

Thoát 1 nếu có lỗi cứng (✗); cảnh báo (⚠) không đổi exit code.
Vì sao các ngưỡng này: xem bảng "Hạn mức" trong tài liệu trên (số đo 5 bài mẫu 2/10/2026).
"""
import argparse, html, json, re, sys

WPM = 140                     # từ/phút khi đọc chữ Việt trên điện thoại, có công thức phải dừng nghĩ

TONG_WARN, TONG_ERR = 2000, 2500      # từ hiện ngay cả bài     (~14 phút / ~18 phút)
MUC_WARN, MUC_ERR = 350, 480          # từ hiện ngay một mục    (~2,5 phút / ~3,4 phút)
BTM_WARN, BTM_ERR = 500, 700          # mục "Bài toán mẫu" — đoạn BUỘC đọc liền có chủ đích nên nới
LIEN_WARN, LIEN_ERR = 300, 400        # từ liền không có nhịp   (~2 phút / ~2,9 phút)
QUIZ_MIN, QUIZ_MAX = 4, 8
MUC_MIN, MUC_MAX = 6, 8               # đếm theo <h3>
DETAILS_MIN, HINH_MIN = 4, 2

DETAILS = re.compile(r"<details\b.*?</details>", re.S | re.I)
DETAILS_SVG = re.compile(r"<svg\b.*?</svg>", re.S | re.I)
FB = re.compile(r'<div class="tl-fb\b.*?</div>', re.S | re.I)
SUMMARY = re.compile(r"<summary\b[^>]*>(.*?)</summary>", re.S | re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)
NHIP = re.compile(r'<details\b|class="tl-quiz|<figure\b', re.I)
HEAD = re.compile(r"<h([34])\b[^>]*>(.*?)</h\1>", re.S | re.I)


def _text(s):
    s = COMMENT.sub(" ", s)
    s = DETAILS_SVG.sub(" ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)


def dem_tu(s):
    return len(_text(s).split())


def hien_ngay(s):
    """Bỏ nội dung <details> (giữ summary) và phản hồi quiz (giữ câu hỏi + lựa chọn)."""
    s = FB.sub(" ", s)
    ra, i = [], 0
    for m in DETAILS.finditer(s):
        ra.append(s[i:m.start()])
        sm = SUMMARY.search(m.group(0))
        if sm:
            ra.append(sm.group(1))
        i = m.end()
    ra.append(s[i:])
    return "".join(ra)


def doan_liem(than):
    """(từ hiện ngay, số nhịp, đoạn liền dài nhất) của một khối."""
    prev, doan, nhip = 0, [], 0
    for m in NHIP.finditer(than):
        seg = than[prev:m.start()]
        if m.group(0).lower().startswith("<details"):
            khoi = DETAILS.match(than, m.start())
            sm = SUMMARY.search(khoi.group(0)) if khoi else None
            if sm:
                seg += sm.group(1)
        doan.append(dem_tu(FB.sub(" ", seg)))
        nhip += 1
        prev = m.end()
    doan.append(dem_tu(FB.sub(" ", than[prev:])))
    return dem_tu(hien_ngay(than)), nhip, (max(doan) if doan else 0)


def tach_muc(t):
    """Danh sách (cấp, tiêu đề, html) theo thứ tự tài liệu, chia ở mọi <h3>/<h4>."""
    ra, moc = [], list(HEAD.finditer(t))
    for i, m in enumerate(moc):
        cuoi = moc[i + 1].start() if i + 1 < len(moc) else len(t)
        ra.append((int(m.group(1)), re.sub(r"\s+", " ", _text(m.group(2))).strip(), t[m.end():cuoi]))
    return ra


def kiem(path):
    t = open(path, encoding="utf8").read()
    hien = dem_tu(hien_ngay(t))
    muc = tach_muc(t)
    so_h3 = len([1 for cap, _, _ in muc if cap == 3])
    quiz = len(re.findall(r"tl-quiz", t))
    hinh = len(re.findall(r"<figure\b", t))
    details = len(re.findall(r"<details\b", t))
    loi, canh_bao, hang = [], [], []

    # <h3> nào có <h4> con thì chỉ là dòng nhóm (người đọc thấy tiêu đề con ngắt đoạn) → không tính hạn mức
    nhom = set()
    for i, (cap, _, _) in enumerate(muc):
        if cap != 3:
            continue
        for j in range(i + 1, len(muc)):
            if muc[j][0] == 3:
                break
            if muc[j][0] == 4:
                nhom.add(i)
                break

    for i, (cap, ten, than) in enumerate(muc):
        h, nhip, lien = doan_liem(than)
        if i in nhom:
            hang.append((cap, ten + "  (nhóm)", None, None, None))
            continue
        btm = "bài toán mẫu" in ten.lower()
        mw, me = (BTM_WARN, BTM_ERR) if btm else (MUC_WARN, MUC_ERR)
        hang.append((cap, ten, h, nhip, lien))
        if h > me:
            loi.append(f'mục "{ten}": {h} từ hiện ngay > {me} — tách thành mục con')
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
    if not (MUC_MIN <= so_h3 <= MUC_MAX):
        canh_bao.append(f"{so_h3} mục lớn, ngoài khoảng {MUC_MIN}–{MUC_MAX}")
    if details < DETAILS_MIN:
        canh_bao.append(f"chỉ {details} <details> < {DETAILS_MIN} (mất phần mở rộng cho HS khá)")
    if hinh < HINH_MIN:
        canh_bao.append(f"chỉ {hinh} hình < {HINH_MIN}")

    return dict(file=path, hien=hien, tong=dem_tu(t), so_h3=so_h3, so_muc=len(muc), quiz=quiz,
                hinh=hinh, details=details, phut=hien / WPM, hang=hang, loi=loi, canh_bao=canh_bao)


def nghin(n):
    return f"{n:,}".replace(",", ".")


def in_nguoi(kq, chi_loi=False):
    print(f"\n{kq['file']}")
    print(f"  {nghin(kq['hien'])} từ hiện ngay / {nghin(kq['tong'])} từ cả file · ~{kq['phut']:.1f} phút "
          f"· {kq['so_h3']} mục lớn + mục con · {kq['quiz']} quiz · {kq['hinh']} hình · {kq['details']} details")
    print(f"  {'mục':<58} {'hiện':>6} {'nhịp':>5} {'liền':>5}")
    for cap, ten, h, nhip, lien in kq["hang"]:
        nhan = ("  " if cap == 4 else "") + ten
        if h is None:
            print(f"  {nhan:<58} {'—':>6} {'—':>5} {'—':>5}")
            continue
        co = "✗" if lien > LIEN_ERR else ("⚠" if lien > LIEN_WARN else " ")
        print(f"  {nhan:<58} {nghin(h):>6} {nhip:>5} {lien:>5} {co}")
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
        print(f"\n{len(kqs)} bài · {n_loi} lỗi cứng · {n_cb} cảnh báo")
    return 1 if any(k["loi"] for k in kqs) else 0


if __name__ == "__main__":
    sys.exit(main())
