"""Bản chiếu "đường trên lớp" (tivi 50"): tren-lop.src.html -> tren-lop.html.
<!--FIGn--> = thẻ <svg> thứ n trong theory.html; <!--TAP:ten--> = hình ten() của Tập (scripts/ruot-tap/hinh-l11-bai21.mjs,
cùng hình in trên giấy). Chạy sau build_figs.py. Không đăng DB."""
import json, pathlib, re, subprocess
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
for n in sorted({int(x) for x in re.findall(r"<!--FIG(\d+)-->", h)}):
    assert 1 <= n <= len(svgs), n
    h = h.replace(f"<!--FIG{n}-->", svgs[n - 1])
ten = sorted(set(re.findall(r"<!--TAP:(\w+)-->", h)))
if ten:
    js = ("import('./scripts/ruot-tap/hinh-l11-bai21.mjs').then(m=>{const H=m.hinhL11b21,o={};"
          f"for(const k of {json.dumps(ten)})o[k]=H[k]('').match(/<svg[\\s\\S]*<\\/svg>/)[0];"
          "process.stdout.write(JSON.stringify(o))})")
    tap = json.loads(subprocess.run(["node", "-e", js], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    for k, s in tap.items():
        h = h.replace(f"<!--TAP:{k}-->", s)
assert "<!--FIG" not in h and "<!--TAP:" not in h
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1216, mục 201)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/l11-tu-dien.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
PUB = ROOT / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, "l11-tu-dien.html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), "l11-tu-dien-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
