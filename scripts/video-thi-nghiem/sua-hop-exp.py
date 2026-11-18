#!/usr/bin/env python3
"""Sửa dòng chữ trong hộp thí nghiệm (.tl-box--exp data-exp="<tn>") đồng bộ theory.src.html,
theory.html và theory_html trong bundle.json (nếu có) của một bài.

Dùng:
  python3 scripts/video-thi-nghiem/sua-hop-exp.py <file-sua.json> [--apply]

<file-sua.json> = danh sách {"thu_muc": "content/lesson-samples/<slug>", "exp": "<tn-id>",
                             "cu": "<chuỗi cũ, nguyên văn trong theory.src.html>", "moi": "<chuỗi mới>"}
Thêm "ngoai_hop": true để sửa chỗ ngoài hộp (chuỗi phải duy nhất trong cả file).
Mỗi chuỗi cũ phải xuất hiện ĐÚNG MỘT lần bên trong hộp exp đó ở mọi file có mặt; sai thì dừng, không ghi gì.
Không --apply: chỉ kiểm và in diff ngắn.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def hop(html, exp):
    """Trả (đầu, cuối) của hộp exp: từ thẻ mở tới </div> đóng cùng cấp."""
    # Hộp exp là <div class="tl-box--exp" …> hoặc <details class="tl-details" data-exp=…> (bài L11 thực hành).
    m = re.search(r'<(div|details)\b[^>]*data-exp="%s"' % re.escape(exp), html)
    if not m:
        return None
    i, sau, tag = m.start(), 0, m.group(1)
    for t in re.finditer(r"<%s\b|</%s>" % (tag, tag), html[i:]):
        sau += 1 if not t.group(0).startswith("</") else -1
        if sau == 0:
            return i, i + t.end()
    return None


def sua(html, exp, cu, moi, nhan, ngoai_hop=False):
    if ngoai_hop:  # sửa ngoài hộp (vd. gập bảng số liệu dưới video): chuỗi phải duy nhất trong cả file
        n = html.count(cu)
        if n != 1:
            raise SystemExit(f"✗ {nhan}: chuỗi cũ (ngoài hộp) xuất hiện {n} lần: {cu[:80]!r}")
        return html.replace(cu, moi)
    r = hop(html, exp)
    if r is None:
        raise SystemExit(f"✗ {nhan}: không thấy hộp exp {exp}")
    a, b = r
    doan = html[a:b]
    n = doan.count(cu)
    if n != 1:
        raise SystemExit(f"✗ {nhan}: chuỗi cũ xuất hiện {n} lần trong hộp {exp}: {cu[:80]!r}")
    return html[:a] + doan.replace(cu, moi) + html[b:]


def main():
    ds = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf8"))
    apply = "--apply" in sys.argv
    theo_bai = {}
    for e in ds:
        theo_bai.setdefault(e["thu_muc"], []).append(e)
    ghi = []
    for td, cac in theo_bai.items():
        d = ROOT / td
        for ten in ("theory.src.html", "theory.html"):
            f = d / ten
            if not f.exists():
                continue
            s = f.read_text(encoding="utf8")
            for e in cac:
                s = sua(s, e["exp"], e["cu"], e["moi"], f"{td}/{ten}", e.get("ngoai_hop", False))
            ghi.append((f, s))
        fb = d / "bundle.json"
        if fb.exists():
            raw = fb.read_text(encoding="utf8")
            b = json.loads(raw)
            for e in cac:
                b["theory_html"] = sua(b["theory_html"], e["exp"], e["cu"], e["moi"], f"{td}/bundle.json", e.get("ngoai_hop", False))
            out = json.dumps(b, ensure_ascii=False, indent=(2 if raw.startswith("{\n  \"") else 1)) + ("\n" if raw.endswith("\n") else "")
            ghi.append((fb, out))
        for e in cac:
            print(f"· {td.split('/')[-1]} · {e['exp']}\n  - {e['cu']}\n  + {e['moi']}")
    if apply:
        for f, s in ghi:
            f.write_text(s, encoding="utf8")
        print(f"✓ Đã ghi {len(ghi)} file, {len(ds)} chỗ sửa.")
    else:
        print(f"(kiểm OK {len(ds)} chỗ sửa, {len(ghi)} file — thêm --apply để ghi)")


if __name__ == "__main__":
    main()
