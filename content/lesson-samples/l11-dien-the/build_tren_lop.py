"""Bản THỬ "đường trên lớp" (chiếu máy chiếu): tren-lop.src.html + Hình 1, 2, 3 lấy từ theory.html -> tren-lop.html.
Chạy sau build_figs.py. Không đăng DB."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
assert len(svgs) == 3, len(svgs)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
for n in (1, 2, 3):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", svgs[n - 1])
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1215, mục 198)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
