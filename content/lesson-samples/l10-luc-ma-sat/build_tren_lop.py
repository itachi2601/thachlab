"""Bản THỬ "đường trên lớp" (chiếu tivi): tren-lop.src.html + Hình 2, Hình 4 lấy từ theory.html -> tren-lop.html.
SVG thứ 2 và 3 trong theory.html (Hình 3 dốc nghiêng là ảnh OpenStax, không phải SVG) thay vào <!--FIG2-->, <!--FIG3-->.
Hình An đẩy thùng và đồ thị O–A–B–C chép sẵn trong src từ scripts/ruot-tap/hinh-l10-bai18.mjs (anDay, doThi) để khớp Tập.
Chạy sau build_figs.py. Không đăng DB."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
assert len(svgs) == 3, len(svgs)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
# cắt lề trắng của Hình 2, 4 (viewBox 440 rộng, hình vẽ nằm giữa) để hình to ra trong cột 44–48% màn
CAT = {2: ('viewBox="0 0 440 260"', 'viewBox="100 18 300 242"'), 3: ('viewBox="0 0 440 240"', 'viewBox="30 28 390 214"')}
for n in (2, 3):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    cu, moi = CAT[n]
    assert svgs[n - 1].count(cu) == 1, n
    h = h.replace(f"<!--FIG{n}-->", svgs[n - 1].replace(cu, moi))
assert "<!--FIG" not in h
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1239, mục 123)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/l10-luc-ma-sat.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
PUB = HERE.parents[2] / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, "l10-luc-ma-sat.html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), "l10-luc-ma-sat-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
