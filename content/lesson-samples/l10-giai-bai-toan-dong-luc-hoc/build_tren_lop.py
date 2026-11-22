"""Bản THỬ "đường trên lớp" (chiếu tivi): tren-lop.src.html + Hình 1, 3, 5 (FIG1, FIG3, FIG4) lấy từ theory.html -> tren-lop.html.
Chạy sau build_figs.py. Hình cầu nối (?) và mặt nghiêng tách P chép sẵn trong src từ scripts/ruot-tap/hinh-l10-bai20.mjs (cauNoi, docTach). Không đăng DB."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
assert len(svgs) == 4, len(svgs)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
for n in (1, 3, 4):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", svgs[n - 1])
assert "<!--FIG" not in h
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1241, mục 296)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/l10-giai-bai-toan-dong-luc-hoc.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
PUB = HERE.parents[2] / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, "l10-giai-bai-toan-dong-luc-hoc.html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), "l10-giai-bai-toan-dong-luc-hoc-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
