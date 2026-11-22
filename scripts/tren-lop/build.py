"""Khung build bản chiếu "trên lớp" dùng chung (skill ban-chieu-tren-lop). Mẫu gốc: content/lesson-samples/l11-dien-the.
CSS/JS chung = scripts/tren-lop/khung.css + khung.js (rút nguyên khối từ bài mẫu; mỗi bài khai cỡ hình .fN trong <style> riêng).
tren-lop.src.html của từng bài có <!--CSS-->, <!--JS-->, <!--FIGn--> (hình thứ n trong theory.html), tuỳ chọn <!--QR-->.
Ra tren-lop.html (cạnh src) + public/dev/tren-lop/<slug>.html và <slug>-ghi-chu.html (noindex).
Dùng trong build_tren_lop.py của bài:  import sys; sys.path.insert(0, ...); from build import dung; dung(__file__)"""
import pathlib, re

KHUNG = pathlib.Path(__file__).resolve().parent
ROOT = KHUNG.parents[1]


def dung(file, qr=None):
    here = pathlib.Path(file).resolve().parent
    slug = here.name
    svgs = re.findall(r"<svg.*?</svg>", (here / "theory.html").read_text(encoding="utf8"), re.S)
    h = (here / "tren-lop.src.html").read_text(encoding="utf8")
    for tag, f in (("CSS", "khung.css"), ("JS", "khung.js")):
        assert h.count(f"<!--{tag}-->") == 1, tag
        h = h.replace(f"<!--{tag}-->", (KHUNG / f).read_text(encoding="utf8"))
    for n in sorted({int(x) for x in re.findall(r"<!--FIG(\d+)-->", h)}):
        assert n <= len(svgs), (n, len(svgs))
        h = h.replace(f"<!--FIG{n}-->", svgs[n - 1])
    if "<!--QR-->" in h:
        assert qr, "thiếu file QR"
        h = h.replace("<!--QR-->", (here / qr).read_text(encoding="utf8"))
    assert "<!--" + "FIG" not in h
    (here / "tren-lop.html").write_text(h, encoding="utf8")
    print("tren-lop.html", len(h))
    pub = ROOT / "public" / "dev" / "tren-lop"
    pub.mkdir(parents=True, exist_ok=True)
    noi = '<meta name="robots" content="noindex">\n'
    for src, dst in ((h, f"{slug}.html"), ((here / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), f"{slug}-ghi-chu.html")):
        assert src.count('<meta charset="utf-8">\n') == 1, dst
        (pub / dst).write_text(src.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + noi), encoding="utf8")
        print("public/dev/tren-lop/" + dst)
