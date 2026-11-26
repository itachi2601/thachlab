#!/usr/bin/env python3
"""Đặt HAI MỐC thời gian ở dòng đầu bài: "Đọc ~N phút · học kỹ (làm câu, mở ô, xem clip) ~M phút".

N vẫn do build_figs.py của bài thay `__PHUT__` (lint_do_dai.py: từ hiện ngay / 140).
M = `phut_hoc_ky` của lint_do_dai.py (tổng từ kể cả ô mở + phản hồi quiz, giây clip, 30 s/câu),
làm tròn lên — script này ghi M thẳng vào theory.src.html, theory.html và theory_html của bundle.json
(số nằm sẵn trong nguồn nên build_figs.py chỉ chép qua, không cần chỗ trống mới).

Dùng (từ gốc repo), CHẠY SAU build_figs.py / build_bundle.py:
    python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/dat_phut_hai_moc.py <thư mục bài> [...]
    python3 .../dat_phut_hai_moc.py --tat-ca          # mọi bài trong content/ có dòng phút
    thêm --kiem  : chỉ báo bài nào M lệch, không ghi (thoát 1 nếu lệch)

Bài cũ còn câu chữ "Thời gian đọc khoảng …"/"Đọc khoảng …"/"Khoảng … phút ·" được đổi sang hai mốc.
"""
import argparse, glob, json, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_do_dai  # noqa: E402

KY = "học kỹ (làm câu, mở ô, xem clip)"
P = r"(__PHUT__|\d+|\?)"
# (mẫu cũ, mẫu mới) — {M} thay bằng số phút học kỹ
DOI = [
    (re.compile(r"Thời gian đọc khoảng <strong>" + P + r" phút</strong>"), r"Đọc ~<strong>\1 phút</strong> · " + KY + " ~<strong>{M} phút</strong>"),
    (re.compile(r"Đọc khoảng <strong>" + P + r" phút</strong>"), r"Đọc ~<strong>\1 phút</strong> · " + KY + " ~<strong>{M} phút</strong>"),
    (re.compile(r"Đọc khoảng " + P + r" phút"), r"Đọc ~\1 phút · " + KY + " ~{M} phút"),
    (re.compile(r"Khoảng " + P + r" phút ·"), r"Đọc ~\1 phút · " + KY + " ~{M} phút ·"),
]
SO_KY = re.compile(re.escape(KY) + r" ~(<strong>)?(\d+|\{M\})( phút)")


def doi_cau(s, m):
    for re_cu, moi in DOI:
        s = re_cu.sub(moi.replace("{M}", str(m)), s, count=1)
    return SO_KY.sub(lambda x: f"{KY} ~{x.group(1) or ''}{m}{x.group(3)}", s)


def co_dong_phut(s):
    return any(r.search(s) for r, _ in DOI) or SO_KY.search(s)


def xu_ly(d, chi_kiem):
    src, hp, bp = (os.path.join(d, f) for f in ("theory.src.html", "theory.html", "bundle.json"))
    h = open(hp, encoding="utf8").read()
    if not co_dong_phut(h):
        return None
    h_moi = doi_cau(h, 0)  # câu chữ mới trước (thêm vài từ), rồi mới đo
    tmp = hp + ".tmp-phut.html"
    open(tmp, "w", encoding="utf8").write(h_moi)
    try:
        kq = lint_do_dai.kiem(tmp)
    finally:
        os.remove(tmp)
    m = math.ceil(kq["phut_hoc_ky"])
    cu = SO_KY.search(h)
    lech = not cu or cu.group(2) != str(m)
    if chi_kiem:
        return m, lech
    open(hp, "w", encoding="utf8").write(doi_cau(h, m))
    if os.path.exists(src):
        s = open(src, encoding="utf8").read()
        if co_dong_phut(s):
            open(src, "w", encoding="utf8").write(doi_cau(s, m))
    if os.path.exists(bp):
        raw = open(bp, encoding="utf8").read()
        th = json.loads(raw).get("theory_html")
        if th and co_dong_phut(th):
            moi = doi_cau(th, m)
            for ea in (False, True):
                a, b = json.dumps(th, ensure_ascii=ea)[1:-1], json.dumps(moi, ensure_ascii=ea)[1:-1]
                if a in raw:
                    raw = raw.replace(a, b)
                    break
            else:
                sys.exit(f"✗ {bp}: không tìm thấy theory_html nguyên văn để thay — sửa tay")
            open(bp, "w", encoding="utf8").write(raw)
    return m, lech


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*")
    ap.add_argument("--tat-ca", action="store_true")
    ap.add_argument("--kiem", action="store_true")
    a = ap.parse_args()
    dirs = a.dirs or []
    if a.tat_ca:
        dirs += sorted({os.path.dirname(p) for p in glob.glob("content/**/theory.html", recursive=True)
                        if "/gemini/" not in p and "/xem-thu/" not in p})
    so_lech = 0
    for d in dirs:
        r = xu_ly(d.rstrip("/"), a.kiem)
        if r is None:
            continue
        m, lech = r
        so_lech += lech
        print(f"{'✗ LỆCH' if (a.kiem and lech) else '·'} {d}: học kỹ ~{m} phút")
    return 1 if (a.kiem and so_lech) else 0


if __name__ == "__main__":
    sys.exit(main())
