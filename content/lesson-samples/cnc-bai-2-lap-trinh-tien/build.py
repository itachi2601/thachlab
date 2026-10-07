#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 2. Chạy: python3 build.py"""
import json, pathlib, re
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 15  # điền theo lint_do_dai.py


def T(x, y, s, c="currentColor", size=15, anchor="middle", w="700", mono=False):
    f = ' font-family="ui-monospace,Menlo,Consolas,monospace"' if mono else ""
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}"{f}>{s}</text>'


def ln(x1, y1, x2, y2, c="currentColor", w=2.5, dash="", mk=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{mk})"' if mk else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}{m}/>'


def marker(i, c):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')


def fig1_svg():
    # 5 px/mm; trục y=125; mặt đầu phải x=380
    S, ax, x0 = 5, 125, 380
    zx = lambda z: x0 + z * S
    b = ln(20, ax, 410, ax, "currentColor", 1.5, "8 5")
    # mâm cặp
    b += f'<rect x="78" y="12" width="42" height="46" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += f'<rect x="78" y="192" width="42" height="46" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(99, 82, "Mâm", "currentColor", 14) + T(99, 99, "cặp", "currentColor", 14)
    # phần phôi kẹp Ø40 (x 120..205)
    b += f'<rect x="120" y="{ax-100}" width="{zx(-35)-120}" height="200" fill="none" stroke="currentColor" stroke-width="2"/>'
    # biên dạng trục bậc (đối xứng)
    r20, r30, ch = 10 * S, 15 * S, 1 * S
    top = [(zx(-35), ax - r30), (zx(-15), ax - r30), (zx(-15), ax - r20), (x0 - ch, ax - r20), (x0, ax - r20 + ch)]
    pts = top + [(x0, ax + r20 - ch), (x0 - ch, ax + r20), (zx(-15), ax + r20), (zx(-15), ax + r30), (zx(-35), ax + r30)]
    b += '<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) + f'" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    b += T(342, 113, "Ø20", BLUE, 16) + T(255, 113, "Ø30", BLUE, 16)
    b += T(415, 58, "vát 1×45°", "currentColor", 14, "end", "600") + ln(386, 62, 380, 76, "currentColor", 1.5)
    b += f'<circle cx="{x0}" cy="{ax}" r="6" fill="{RED}"/>' + T(396, 146, "W", RED, 17)
    # kích thước
    for x in (zx(-15), zx(-35), x0):
        b += ln(x, ax + r30 + 6 if x != x0 else ax + r20 + 6, x, 272, "currentColor", 1.2, "3 3")
    b += ln(zx(-15), 246, x0, 246, "currentColor", 1.5) + T((zx(-15) + x0) / 2, 240, "15", "currentColor", 15)
    b += ln(zx(-35), 270, x0, 270, "currentColor", 1.5) + T(250, 264, "35", "currentColor", 15)
    return wrap("0 0 420 282", "Bản vẽ trục bậc Ø20 và Ø30", b,
                "Hình 1. Trục bậc cần tiện: đoạn Ø20 dài 15 mm, đoạn Ø30 tới 35 mm tính từ mặt đầu, vát 1×45°. W ở tâm mặt đầu phải.")


def fig2_svg():
    rows = [("N50", "số thứ tự khối"), ("G01", "kiểu chuyển động: cắt thẳng"), ("X50.0", "đích theo phương đường kính"),
            ("Z-25.0", "đích dọc trục chính"), ("F0.2", "lượng chạy dao"), (";", "kết thúc khối")]
    cols = [ORG, BLUE, RED, RED, GRN, "currentColor"]
    b = T(210, 26, "N50 G01 X50.0 Z-25.0 F0.2 ;", "currentColor", 17, "middle", "700", True)
    for i, ((tok, mean), c) in enumerate(zip(rows, cols)):
        y = 46 + i * 38
        b += f'<rect x="16" y="{y}" width="104" height="30" rx="6" fill="none" stroke="{c}" stroke-width="2.5"/>'
        b += T(68, y + 21, tok, c, 16, "middle", "700", True)
        b += T(134, y + 21, mean, "currentColor", 15, "start", "600")
    return wrap("0 0 420 280", "Cấu trúc một khối lệnh", b,
                "Hình 2. Một khối lệnh FANUC 21T: mỗi chữ cái kèm con số là một từ lệnh, khối kết thúc bằng dấu chấm phẩy.")


def fig3_svg():
    S, ax, x0 = 8, 230, 370
    P = lambda X, Z: (x0 + Z * S, ax - X / 2 * S)
    b0 = ""
    S0 = P(30, 2)
    pts = {"S": P(18, 2), "A": P(18, 0), "B": P(20, -1), "C": P(20, -15), "D": P(30, -15), "E": P(30, -35), "F": P(42, -35)}
    b = "<defs>" + marker("g3", GRN) + marker("o3", ORG) + marker("k3", "currentColor") + "</defs>"
    b += ln(30, ax, 412, ax, "currentColor", 1.5, "8 5")
    # phôi Ø40 (nửa trên)
    y40 = ax - 20 * S
    b += ln(40, y40, x0, y40, "currentColor", 1.5, "5 4") + ln(x0, y40, x0, ax, "currentColor", 1.5, "5 4")
    b += T(150, y40 - 8, "phôi Ø40", "currentColor", 14, "middle", "600")
    k = list(pts)
    for a, c in zip(k, k[1:]):
        (x1, y1), (x2, y2) = pts[a], pts[c]
        b += ln(x1, y1, x2, y2, GRN, 3, mk="" if a in "SA" else "g3")
    b += ln(S0[0], S0[1], pts["S"][0], pts["S"][1], ORG, 2.5, "6 4", "o3") + f'<circle cx="{S0[0]}" cy="{S0[1]}" r="4.5" fill="{ORG}"/>'
    for n, (x, y) in pts.items():
        b += f'<circle cx="{x}" cy="{y}" r="4.5" fill="{ORG}"/>'
    lab = {"S": (S0[0] + 14, S0[1] - 4, "start"), "A": (370, 184, "middle"), "B": (356, 138, "middle"), "C": (250, 174, "middle"),
           "D": (240, 102, "end"), "E": (80, 128, "end"), "F": (80, 66, "end")}
    for n, (x, y, an) in lab.items():
        b += T(x, y, n, ORG, 16, an)
    b += f'<circle cx="{x0}" cy="{ax}" r="6" fill="{RED}"/>' + T(384, 254, "W", RED, 17)
    b += ln(40, ax, 40, ax - 60, "currentColor", 2.5, mk="k3") + T(50, ax - 46, "+X", "currentColor", 15, "start")
    b += T(150, 258, "Z âm: về phía mâm cặp", "currentColor", 14, "middle", "600")
    return wrap("0 0 420 270", "Đường tiện tinh trục bậc", b,
                "Hình 3. Đường dao tiện tinh (nửa trên trục): từ S chạy nhanh G00 (nét đứt) tới X18.0 Z2.0, rồi cắt: A–B vát, B–C đoạn Ø20, C–D lên bậc, D–E đoạn Ø30, E–F rút dao. Vẽ theo bán kính, chương trình ghi X theo đường kính.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = (src.replace("__FIG1__", fig1_svg()).replace("__FIG2__", fig2_svg())
          .replace("__FIG3__", fig3_svg()).replace("__PHUT__", str(PHUT)))
(HERE / "theory.html").write_text(html, encoding="utf8")

MC = "multiple_choice"
qs = []
for blk in re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb tl-fb--no">', html, re.S):
    qm = re.search(r'<p>(.*?)</p>', blk, re.S)
    opts = re.findall(r'<label[^>]*class="tl-opt (tl-ok|tl-no)">[A-D]\. (.*?)</label>', blk, re.S)
    fb = re.search(r'<div class="tl-fb tl-fb--ok"><p>(.*?)</p></div>', blk, re.S)
    if len(opts) != 4:
        continue
    q = qm.group(1) if qm else "Chọn đáp án đúng."
    txt = lambda s: re.sub(r"<[^>]+>", "", s)
    qs.append({"type": MC, "question": txt(q), "options": [txt(o[1]) for o in opts],
               "answer": [o[0] for o in opts].index("tl-ok"), "explanation": txt(fb.group(1)) if fb else ""})
if qs:  # câu dự đoán: đề nằm ngoài tl-quiz
    qs[0]["question"] = ("Bản vẽ ghi đoạn trục Ø20, chương trình ghi G01 X10.0 Z-15.0. "
                         "Vì sao chi tiết mô phỏng ra Ø10 thay vì Ø20?")
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Lập trình tiện CNC với Win-NC32 / FANUC 21T", "duration_minutes": 10, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
