#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 4 (EMCO TURN 55). Chạy: python3 build.py"""
import json, pathlib, re
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 15  # điền theo lint_do_dai.py (làm tròn lên)


def T(x, y, s, c="currentColor", size=15, anchor="middle", w="700"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def box(x, y, w, h, c="currentColor", fill="none", sw=2.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def ln(x1, y1, x2, y2, c="currentColor", w=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def dot(x, y, c, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def arrow(pid, x1, y1, x2, y2, c, w=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="url(#{pid})"/>'


def markers(pref, pairs):
    return ('<defs>' + ''.join(
        f'<marker id="{pref}{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
        f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for i, c in pairs) + '</defs>')


def fig1_svg():
    """Sơ đồ phần chấp hành máy tiện (nhìn ngang, đơn giản)."""
    b = markers("f1", (("x", RED), ("z", BLUE)))
    ax = 115  # tâm trục chính
    b += ln(10, ax, 410, ax, "currentColor", 1.5, "6 5")
    b += box(10, 60, 70, 110) + T(45, 50, "Trục chính", "currentColor", 15)
    b += box(80, 80, 24, 70) + T(92, 192, "Mâm cặp", "currentColor", 15) + ln(92, 152, 92, 176, "currentColor", 1.5)
    b += box(104, ax - 14, 130, 28) + T(170, ax + 34, "Phôi", "currentColor", 15)
    # ụ động + mũi tâm
    b += box(330, 92, 70, 46)
    b += f'<polygon points="330,{ax-10} 312,{ax} 330,{ax+10}" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(365, 82, "Ụ động", "currentColor", 15)
    # mâm dao + dao
    b += f'<circle cx="270" cy="45" r="26" fill="none" stroke="{ORG}" stroke-width="2.5"/>'
    b += ln(256, 67, 238, ax - 16, GRN, 4)
    b += T(304, 40, "Mâm dao", ORG, 15, "start")
    b += T(222, 78, "Dao", GRN, 15, "end")
    # băng máy
    b += box(10, 200, 400, 18) + T(210, 244, "Băng máy", "currentColor", 15)
    # trục toạ độ
    ox, oy = 290, 182
    b += arrow("f1z", ox, oy, ox + 62, oy, BLUE) + T(ox + 68, oy + 6, "+Z", BLUE, 16, "start")
    b += arrow("f1x", ox, oy, ox, oy - 34, RED) + T(ox - 8, oy - 22, "+X", RED, 16, "end")
    return wrap("0 0 420 256", "Sơ đồ phần chấp hành máy tiện CNC", b,
                "Hình 1. Phần chấp hành (sơ đồ). Z dọc trục chính, X theo đường kính.")


def fig2_svg():
    """Trình tự mở máy đến lúc chạy tay."""
    b = markers("f2", (("a", "currentColor"),))
    steps = [("1. Kiểm tra máy (chưa cấp điện)", "currentColor"),
             ("2. Đóng CP của máy tiện", "currentColor"),
             ("3. Nhấn Power máy tính", "currentColor"),
             ("4. Mở WinNC FANUC 21T", "currentColor"),
             ("5. Reference: về chuẩn", ORG),
             ("6. JOG / MDI: thao tác", BLUE)]
    y, h, gap = 8, 36, 14
    for i, (s, c) in enumerate(steps):
        b += box(60, y, 300, h, c) + T(210, y + 24, s, c, 15)
        if i < len(steps) - 1:
            b += arrow("f2a", 210, y + h, 210, y + h + gap - 1, "currentColor", 2.5)
        y += h + gap
    H = y - gap + 8
    return wrap(f"0 0 420 {H}", "Trình tự mở máy tiện CNC", b,
                "Hình 2. Trình tự mở máy: Reference luôn đứng trước JOG và MDI.")


def fig3_svg():
    """Cách 1 cài Z gốc phôi: MW = MA + AW."""
    b = ""
    ax = 120
    xM, xA, xW = 40, 110, 290
    b += ln(10, ax, 410, ax, "currentColor", 1.5, "6 5")
    b += box(xM, 70, xA - xM, 100) + T(75, 62, "Mâm cặp", "currentColor", 15)
    b += box(xA, ax - 25, xW - xA, 50) + T(200, ax + 19, "Phôi", "currentColor", 15)
    # dao chạm mặt đầu
    b += ln(xW + 3, ax - 22, 340, 40, GRN, 4) + dot(xW + 3, ax - 22, GRN, 5)
    b += T(350, 34, "Dao", GRN, 15, "start")
    # điểm M, A, W
    b += dot(xM, ax, BLUE) + T(xM - 10, ax - 8, "M", BLUE, 17, "end")
    b += dot(xA, ax - 25, "currentColor", 4) + T(xA + 8, ax - 32, "A", "currentColor", 16, "start")
    b += dot(xW, ax, RED) + T(xW + 12, ax + 22, "W", RED, 17, "start")
    # đường dóng
    b += ln(xM, 170, xM, 236, BLUE, 1.5, "4 4")
    b += ln(xA, 170, xA, 206, "currentColor", 1.5, "4 4")
    b += ln(xW, ax + 25, xW, 236, RED, 1.5, "4 4")

    def dim(x1, x2, y, lab, c="currentColor"):
        s = ln(x1, y, x2, y, c, 2)
        s += ln(x1, y - 6, x1, y + 6, c, 2) + ln(x2, y - 6, x2, y + 6, c, 2)
        return s + T((x1 + x2) / 2, y - 7, lab, c, 15)
    b += dim(xM, xA, 200, "MA")
    b += dim(xA, xW, 200, "AW")
    b += dim(xM, xW, 230, "MW = MA + AW", RED)
    return wrap("0 0 420 244", "Cài Z gốc phôi bằng cách đo trực tiếp", b,
                "Hình 3. Cách 1: MW = MA + AW. Vị trí M và dấu khi nhập theo sổ tay máy.")


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
    qs[0]["question"] = "Sau khi mở WinNC FANUC 21T, việc nào phải làm trước khi di chuyển dao bằng tay?"
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Vận hành và cài đặt máy tiện CNC EMCO TURN 55", "duration_minutes": 8, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
