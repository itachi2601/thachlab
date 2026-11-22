"""Bản THỬ "đường trên lớp" (chiếu tivi): tren-lop.src.html + Hình 1–4 lấy từ theory.html -> tren-lop.html.
SVG thứ 1–4 trong theory.html (búa nhổ đinh, thước có trục, vô lăng, thanh gỗ + túi gạo) thay vào <!--FIG1-->…<!--FIG4-->.
Hình 2 của bài web (lực xiên) là ảnh OpenStax, không phải SVG: màn 2d dùng hình lực xiên chép sẵn trong src từ
scripts/ruot-tap/hinh-l10-bai21.mjs (lucXien) để khớp Tập. Chạy sau build_figs.py. Không đăng DB."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
assert len(svgs) == 4, len(svgs)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
# cắt lề trắng (đo getBBox khi đã phóng chữ) để hình to ra trong cột 34–44% màn
CAT = {1: ('viewBox="0 0 440 222"', 'viewBox="4 24 432 196"'), 2: ('viewBox="0 0 440 270"', 'viewBox="10 0 422 270"'),
       3: ('viewBox="0 0 440 290"', 'viewBox="80 -6 280 280"'), 4: ('viewBox="0 0 440 270"', 'viewBox="22 6 396 262"')}
for n in (1, 2, 3, 4):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    cu, moi = CAT[n]
    assert svgs[n - 1].count(cu) == 1, n
    h = h.replace(f"<!--FIG{n}-->", svgs[n - 1].replace(cu, moi))
assert "<!--FIG" not in h
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1242, mục 129)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/l10-moment-luc.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
PUB = HERE.parents[2] / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, "l10-moment-luc.html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), "l10-moment-luc-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
