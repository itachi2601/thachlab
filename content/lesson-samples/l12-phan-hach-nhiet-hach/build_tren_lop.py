"""Bản THỬ "đường trên lớp" (chiếu tivi): tren-lop.src.html + Hình 3 (hệ số k) và Hình 4 (nhiệt hạch, Mặt trời) lấy từ theory.html -> tren-lop.html.
Hình phân hạch U-235, sơ đồ nhà máy, phản ứng D + T chép sẵn trong src từ scripts/ruot-tap/hinh-ch4.mjs. Không đăng DB."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
assert len(svgs) == 2, len(svgs)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
for n in (1, 2):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", svgs[n - 1])
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1193, mục 181)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/l12-phan-hach-nhiet-hach.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
SLUG = "l12-phan-hach-nhiet-hach"
PUB = HERE.parents[2] / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, SLUG + ".html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), SLUG + "-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
