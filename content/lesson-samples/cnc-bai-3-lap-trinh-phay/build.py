#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 3. Chạy: python3 build.py"""
import json, pathlib, re
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 16  # điền theo lint_do_dai.py (làm tròn lên)


def T(x, y, s, c="currentColor", size=17, anchor="middle", w="700"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def ln(x1, y1, x2, y2, c="currentColor", w=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def dot(x, y, c, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def arrow(pid, x1, y1, x2, y2, c, w=3, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} marker-end="url(#{pid})"/>'


def markers(pre, pairs):
    return ('<defs>' + ''.join(
        f'<marker id="{pre}{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
        f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for i, c in pairs) + '</defs>')


def fig1_svg():
    # Tấm 60 x 40 mm, 4 px/mm, tâm W tại (210,150)
    k, cx, cy = 4, 210, 150
    x0, x1, y0, y1 = cx - 30 * k, cx + 30 * k, cy - 20 * k, cy + 20 * k  # 90,330,70,230
    b = markers("c3a", (("k", "currentColor"),))
    b += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="currentColor" stroke-width="3"/>'
    b += arrow("c3ak", cx, cy, 375, cy, "currentColor", 2.5) + T(380, cy + 6, "+X", "currentColor", 17, "start")
    b += arrow("c3ak", cx, cy, cx, 35, "currentColor", 2.5) + T(cx + 8, 42, "+Y", "currentColor", 17, "start")
    b += dot(cx, cy, RED, 7) + T(cx + 10, cy + 24, "W", RED, 18, "start")
    for (x, y, s, lx, ly, a) in ((x0, y1, "1", x0 - 8, y1 + 20, "end"), (x1, y1, "2", x1 + 8, y1 + 20, "start"),
                                  (x1, y0, "3", x1 + 8, y0 - 8, "start"), (x0, y0, "4", x0 - 8, y0 - 8, "end")):
        b += dot(x, y, GRN) + T(lx, ly, s, GRN, 18, a)
    # kích thước
    b += ln(x0, 262, x1, 262, "currentColor", 1.5) + ln(x0, 254, x0, 270, "currentColor", 1.5) + ln(x1, 254, x1, 270, "currentColor", 1.5)
    b += T(cx, 288, "60 mm", "currentColor", 15, "middle", "600")
    b += ln(58, y0, 58, y1, "currentColor", 1.5) + ln(50, y0, 66, y0, "currentColor", 1.5) + ln(50, y1, 66, y1, "currentColor", 1.5)
    b += T(46, cy + 5, "40", "currentColor", 15, "end", "600")
    return wrap("0 0 420 298", "Tấm phôi chữ nhật, gốc W ở tâm, bốn góc đánh số", b,
                "Hình 1. Tấm phôi 60 × 40 mm nhìn từ trên xuống (mặt phẳng XY). Gốc W ở tâm; 1, 2, 3, 4 là bốn góc của biên dạng.")


def fig2_svg():
    b = markers("c3b", (("b", BLUE), ("o", ORG), ("k", "currentColor")))
    b += T(210, 26, "Nhìn từ +Z xuống mặt XY (G17)", "currentColor", 16)
    # G02: cùng chiều kim đồng hồ trên màn hình (sweep=1), trái -> đỉnh -> phải
    b += f'<path d="M40,140 A65,65 0 0 1 170,140" fill="none" stroke="{BLUE}" stroke-width="3.5" marker-end="url(#c3bb)"/>'
    b += dot(40, 140, BLUE, 5) + dot(105, 140, "currentColor", 3)
    b += T(105, 196, "G02", BLUE, 20) + T(105, 220, "cùng chiều", BLUE, 15, "middle", "600") + T(105, 240, "kim đồng hồ", BLUE, 15, "middle", "600")
    # G03: ngược chiều kim đồng hồ (sweep=0), phải -> đỉnh -> trái
    b += f'<path d="M380,140 A65,65 0 0 0 250,140" fill="none" stroke="{ORG}" stroke-width="3.5" marker-end="url(#c3bo)"/>'
    b += dot(380, 140, ORG, 5) + dot(315, 140, "currentColor", 3)
    b += T(315, 196, "G03", ORG, 20) + T(315, 220, "ngược chiều", ORG, 15, "middle", "600") + T(315, 240, "kim đồng hồ", ORG, 15, "middle", "600")
    # trục nhỏ
    b += arrow("c3bk", 190, 236, 232, 236, "currentColor", 2) + T(236, 241, "+X", "currentColor", 14, "start")
    b += arrow("c3bk", 190, 236, 190, 198, "currentColor", 2) + T(190, 190, "+Y", "currentColor", 14)
    return wrap("0 0 420 252", "Chiều cung tròn G02 và G03 trong mặt phẳng G17", b,
                "Hình 2. Mặt phẳng G17, nhìn từ +Z xuống: G02 chạy cung cùng chiều kim đồng hồ, G03 ngược chiều. Chấm lớn là điểm đầu cung, chấm nhỏ là tâm cung (I, J).")


def fig3_svg():
    yI, yR, yS, yZ = 50, 125, 170, 230
    b = markers("c3c", (("b", BLUE), ("o", ORG)))
    b += ln(80, yI, 410, yI, "currentColor", 1.8, "7 5") + T(6, yI + 5, "Ban đầu", "currentColor", 15, "start", "600")
    b += ln(80, yR, 410, yR, "currentColor", 1.8, "7 5") + T(6, yR + 5, "Mặt R", "currentColor", 15, "start", "600")
    b += f'<rect x="90" y="{yS}" width="310" height="85" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(6, yS + 5, "Mặt phôi", "currentColor", 15, "start", "600") + T(6, yZ + 5, "Đáy Z", "currentColor", 15, "start", "600")
    b += ln(80, yZ, 150, yZ, "currentColor", 1.2, "3 4")
    for hx in (170, 320):
        b += f'<rect x="{hx-9}" y="{yS}" width="18" height="{yZ-yS}" fill="none" stroke="currentColor" stroke-width="2"/>'
        b += arrow("c3cb", hx - 4, yR, hx - 4, yZ - 2, BLUE, 3)
    b += arrow("c3co", 174, yZ - 2, 174, yR + 2, ORG, 3, "6 4")
    b += arrow("c3co", 324, yZ - 2, 324, yI + 2, ORG, 3, "6 4")
    b += T(188, 154, "G99: về R", ORG, 15, "start")
    b += T(312, 96, "G98: về mặt ban đầu", ORG, 15, "end")
    return wrap("0 0 420 262", "Chu trình khoan: mặt phẳng ban đầu, mặt R, đáy lỗ, G98 và G99", b,
                "Hình 3. Chu trình khoan nhìn từ bên cạnh: mũi xanh là khoan với tốc độ F tới đáy Z; mũi cam nét đứt là rút dao, G99 về mặt R, G98 về mặt phẳng ban đầu.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = (src.replace("__FIG1__", fig1_svg()).replace("__FIG2__", fig2_svg())
          .replace("__FIG3__", fig3_svg()).replace("__PHUT__", str(PHUT)))
(HERE / "theory.html").write_text(html, encoding="utf8")

MC = "multiple_choice"
txt = lambda s: re.sub(r"<[^>]+>", "", s).strip()
qs = []
for blk in re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb tl-fb--no">', html, re.S):
    qm = re.search(r'<p>(.*?)</p>', blk, re.S)
    opts = re.findall(r'<label[^>]*class="tl-opt (tl-ok|tl-no)">[A-D]\. (.*?)</label>', blk, re.S)
    fb = re.search(r'<div class="tl-fb tl-fb--ok"><p>(.*?)</p></div>', blk, re.S)
    if len(opts) != 4 or not qm:
        continue
    qs.append({"type": MC, "question": txt(qm.group(1)), "options": [txt(o[1]) for o in opts],
               "answer": [o[0] for o in opts].index("tl-ok"), "explanation": txt(fb.group(1)) if fb else ""})
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Lập trình phay CNC FANUC 21M", "duration_minutes": 10, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
