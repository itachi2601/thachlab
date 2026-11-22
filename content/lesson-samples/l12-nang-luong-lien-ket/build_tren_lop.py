"""Bản THỬ "đường trên lớp" (chiếu máy chiếu): tren-lop.src.html + Hình 1, 2 (FIG1–2) lấy từ theory.html -> tren-lop.html.
Chạy sau build_figs.py. Không đăng DB."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
assert len(svgs) == 3, len(svgs)  # Hình 1, 2, 4 (Hình 3 là ảnh OpenStax; màn 5a dùng hình Tập)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
for n in (1, 2):   # Hình 4 (svgs[2]) không dùng: nhãn chồng nhau khi phóng; màn 5d dùng hình soSanhNL của hinh-ch4.mjs
    assert h.count(f"<!--FIG{n}-->") == 1, n
    s = svgs[n - 1]
    if n == 2:   # màn 4a: che "toả 28,30 MeV" + dòng tính tới khi lớp trả lời "đi đâu?" (góp ý lớp ảo)
        s, k = re.subn(r'<text (?=[^>]*>(?:toả|28,30 MeV|0,030377 u × 931,5 MeV/u = 28,30 MeV)</text>)', '<text class="an-o" data-o="a4a" ', s)
        assert k == 3, k
    h = h.replace(f"<!--FIG{n}-->", s)
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1192, mục 147)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/l12-nang-luong-lien-ket.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
PUB = HERE.parents[2] / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, "l12-nang-luong-lien-ket.html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), "l12-nang-luong-lien-ket-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
