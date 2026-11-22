"""Bản THỬ "đường trên lớp" (chiếu tivi): tren-lop.src.html + 6 hình lấy từ Tập bài 23 -> tren-lop.html.
Hình = hình trong Tập (scripts/ruot-tap/hinh-l10-bai23.mjs, tự vẽ, chữ 20 / viewBox 320–366): sanBang, phanTichLuc, dauCong,
docTrongLuc, xachXo, vanTruot -> <!--FIG1-->…<!--FIG6-->. Sinh mã QR bằng build_qr.mts trước (đề 1244, mục 233). Không đăng DB."""
import pathlib, re, subprocess, json
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
JS = ("import {hinhL10b23 as H} from './scripts/ruot-tap/hinh-l10-bai23.mjs';"
      "const o={};for(const k of ['sanBang','phanTichLuc','dauCong','docTrongLuc','xachXo','vanTruot'])"
      "o[k]=H[k]().match(/<svg[\\s\\S]*<\\/svg>/)[0];console.log(JSON.stringify(o));")
figs = json.loads(subprocess.run(["node", "--input-type=module", "-e", JS], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
h = (HERE / "tren-lop.src.html").read_text(encoding="utf8")
for n, k in enumerate(["sanBang", "phanTichLuc", "dauCong", "docTrongLuc", "xachXo", "vanTruot"], 1):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    svg = figs[k]
    # id marker trùng nhau giữa các hình trên cùng trang: thêm hậu tố theo số hình
    svg = re.sub(r'id="(\w+)"', lambda m: f'id="{m.group(1)}-w{n}"', svg)
    svg = re.sub(r'url\(#(\w+)\)', lambda m: f'url(#{m.group(1)}-w{n})', svg)
    h = h.replace(f"<!--FIG{n}-->", svg)
assert "<!--FIG" not in h
qr = (HERE / "tren-lop-qr.svg").read_text(encoding="utf8")   # sinh bằng build_qr.mts (đề 1244, mục 233)
assert h.count("<!--QR-->") == 1
h = h.replace("<!--QR-->", qr)
(HERE / "tren-lop.html").write_text(h, encoding="utf8")
print("tren-lop.html", len(h))
# Bản lên web (tĩnh, không index): /dev/tren-lop/l10-nang-luong-cong-co-hoc.html + ghi chú dạy. Trang mục lục: app/dev/tren-lop/page.tsx
PUB = ROOT / "public" / "dev" / "tren-lop"
PUB.mkdir(parents=True, exist_ok=True)
NOI = '<meta name="robots" content="noindex">\n'
for src, dst in ((h, "l10-nang-luong-cong-co-hoc.html"), ((HERE / "tren-lop-ghi-chu.html").read_text(encoding="utf8"), "l10-nang-luong-cong-co-hoc-ghi-chu.html")):
    assert src.count("<meta charset=\"utf-8\">\n") == 1, dst
    (PUB / dst).write_text(src.replace("<meta charset=\"utf-8\">\n", "<meta charset=\"utf-8\">\n" + NOI), encoding="utf8")
    print("public/dev/tren-lop/" + dst)
