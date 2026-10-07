#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 7. Chạy: python3 build.py"""
import json, pathlib, re, math
from svg_lib import RED, BLUE, ORG, GRN, wrap, text
from svg_lib import defs as sdefs, arrow as sarrow

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 15  # điền theo lint_do_dai.py


def T(x, y, s, c="currentColor", size=15, anchor="middle", w="700"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def box(x, y, w, h, c="currentColor", fill="none"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{c}" stroke-width="2.5"/>'


def ln(x1, y1, x2, y2, c="currentColor", w=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def dot(x, y, c, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def arrow(pid, x1, y1, x2, y2, c, w=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="url(#{pid})"/>'


def defs(pid, c):
    return (f'<defs><marker id="{pid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker></defs>')



def fig1_svg():
    b = sdefs("f1")
    k = 3.4
    px = lambda x: 40 + k * x
    py = lambda y: 234 - k * y
    b += f'<rect x="40" y="30" width="340" height="204" rx="6" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    for (x, y) in ((20, 15), (80, 15), (80, 45), (20, 45)):
        b += f'<circle cx="{px(x):.0f}" cy="{py(y):.0f}" r="10" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="4 3"/>'
        b += f'<circle cx="{px(x)+10.2:.1f}" cy="{py(y):.0f}" r="10" fill="none" stroke="{ORG}" stroke-width="3"/>'
    b += text(210, 140, "Tấm đế sau gia công", "currentColor", 15, "middle", "700")
    b += text(40, 262, "Nét đứt: vị trí đúng bản vẽ", "currentColor", 14)
    b += text(40, 282, "Nét liền cam: lỗ thực tế, cùng lệch sang phải 3 mm", ORG, 14)
    return wrap("0 0 420 292", "Bốn lỗ cùng lệch về một phía", b,
                "Hình 1. Cả bốn lỗ dịch cùng một vector so với vị trí đúng; hình dạng từng lỗ vẫn tròn và đúng cỡ.")


def fig2_svg():
    b = sdefs("f2")
    b += '<rect x="120" y="80" width="180" height="100" rx="22" fill="none" stroke="currentColor" stroke-width="3"/>'
    b += f'<rect x="96" y="56" width="228" height="148" rx="46" fill="none" stroke="{ORG}" stroke-width="2.5" stroke-dasharray="7 5"/>'
    b += f'<circle cx="210" cy="204" r="24" fill="none" stroke="{GRN}" stroke-width="3"/>'
    b += f'<circle cx="210" cy="204" r="3" fill="{GRN}"/>'
    b += text(210, 135, "biên dạng chi tiết", "currentColor", 15, "middle", "700")
    b += text(210, 40, "đường tâm dao", ORG, 15, "middle", "700")
    b += text(246, 232, "dao, bán kính r", GRN, 14)
    b += f'<line x1="97" y1="130" x2="119" y2="130" stroke="{BLUE}" stroke-width="4"/>'
    b += text(108, 120, "r", BLUE, 15, "middle", "700")
    return wrap("0 0 420 250", "Đường tâm dao dời ra một bán kính so với biên dạng", b,
                "Hình 2. Tâm dao chạy trên đường nét đứt, cách biên dạng đúng một bán kính dao r. Bù bán kính dao để máy tự làm việc dời này.")


def fig3_svg():
    b = sdefs("f3")
    k = 3.4
    px = lambda x: 40 + k * x
    py = lambda y: 250 - k * y
    b += f'<rect x="40" y="46" width="340" height="204" rx="34" fill="none" stroke="currentColor" stroke-width="3"/>'
    for (x, y) in ((20, 15), (80, 15), (80, 45), (20, 45)):
        b += f'<circle cx="{px(x):.0f}" cy="{py(y):.0f}" r="11" fill="none" stroke="{GRN}" stroke-width="3"/>'
    b += text(210, 154, "4 lỗ M8×1,25, khoan Ø6,8", GRN, 14, "middle", "700")
    pts = {"A": (10, 0, 0, 20, "middle"), "B": (90, 0, 0, 20, "middle"), "C": (100, 10, 10, 4, "start"),
           "D": (100, 50, 10, 4, "start"), "E": (90, 60, 0, -10, "middle"), "F": (10, 60, 0, -10, "middle"),
           "G": (0, 50, -10, 4, "end"), "H": (0, 10, -10, 4, "end")}
    for n, (x, y, dx, dy, an) in pts.items():
        b += f'<circle cx="{px(x):.0f}" cy="{py(y):.0f}" r="5" fill="{RED}"/>'
        b += text(round(px(x) + dx), round(py(y) + dy), n, RED, 16, an, "700")
    b += f'<circle cx="40" cy="250" r="6" fill="{BLUE}"/>' + text(22, 268, "W", BLUE, 17, "middle", "700")
    return wrap("0 0 420 276", "Tấm đế 100×60 với tám điểm biên dạng", b,
                "Hình 3. Tấm 100 × 60, góc lượn R10, gốc W ở góc dưới trái. A đến H là điểm đầu và điểm cuối các đoạn thẳng, cung.")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = (src.replace("__FIG1__", fig1_svg()).replace("__FIG2__", fig2_svg())
          .replace("__FIG3__", fig3_svg()).replace("__PHUT__", str(PHUT)))
(HERE / "theory.html").write_text(html, encoding="utf8")

MC = "multiple_choice"


# Bài tự kiểm tra trong bundle: lấy lại từ HTML (câu + 4 phương án + đáp án + giải thích)
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
# Câu dự đoán nằm trong tl-box--think với <p> ngoài tl-quiz
if qs:
    qs[0]["question"] = "Nguyên nhân nhiều khả năng nhất khiến cả bốn lỗ cùng lệch về một phía?"
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Gia công phay CNC", "duration_minutes": 8, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
