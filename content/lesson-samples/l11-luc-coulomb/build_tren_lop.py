"""Bản chiếu trên lớp (tivi 50"): tren-lop.src.html + hình -> tren-lop.html, rồi chép bản web noindex sang public/dev/tren-lop/.
<!--FIGn--> = thẻ <svg> thứ n trong theory.html; <!--TAP:ten--> = hình hinhL11b16.ten() của ruột tập (scripts/ruot-tap/hinh-l11-bai16.mjs);
<!--QR--> = tren-lop-qr.svg (sinh bằng build_qr.mts, đề 1211, mục 186). Không đăng DB."""
import json, pathlib, re, subprocess
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
svgs = re.findall(r"<svg.*?</svg>", (HERE / "theory.html").read_text(encoding="utf8"), re.S)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
for n in sorted({int(x) for x in re.findall(r"<!--FIG(\d+)-->", h)}):
    assert h.count(f"<!--FIG{n}-->") == 1 and n <= len(svgs), n
    h = h.replace(f"<!--FIG{n}-->", svgs[n - 1])
ten = sorted(set(re.findall(r"<!--TAP:(\w+)-->", h)))
if ten:
    js = ("import { hinhL11b16 as H } from './scripts/ruot-tap/hinh-l11-bai16.mjs';"
          f"const o={{}}; for (const k of {json.dumps(ten)}) o[k]=H[k](); console.log(JSON.stringify(o));")
    tap = json.loads(subprocess.run(["node", "--input-type=module", "-e", js], cwd=ROOT, check=True, capture_output=True, text=True).stdout)
    for k in ten:
        s = re.search(r"<svg.*?</svg>", tap[k], re.S).group(0)   # bỏ <figure>/<figcaption> của Tập
        h = h.replace(f"<!--TAP:{k}-->", s)
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/<slug>.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
SLUG = "l11-luc-coulomb"
PUB = ROOT / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, f"{SLUG}.html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), f"{SLUG}-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
