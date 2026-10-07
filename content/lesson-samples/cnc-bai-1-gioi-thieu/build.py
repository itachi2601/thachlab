#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 1. Chạy: python3 build.py"""
import json, pathlib, re, math
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 16  # điền theo lint_do_dai.py


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
    d = ('<defs>' + ''.join(
        f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for i, c in (("a", "currentColor"), ("b", BLUE), ("o", ORG), ("g", GRN))) + '</defs>')
    b = d
    b += box(20, 10, 170, 44) + T(105, 38, "Chương trình")
    b += box(230, 10, 170, 44) + T(315, 38, "Phôi")
    b += box(20, 100, 170, 54, BLUE) + T(105, 132, "ĐIỀU KHIỂN", BLUE)
    b += box(230, 100, 170, 54, ORG) + T(315, 132, "CHẤP HÀNH", ORG)
    b += box(230, 200, 170, 44, GRN) + T(315, 228, "Chi tiết", GRN)
    b += arrow("a", 105, 54, 105, 98, "currentColor")
    b += arrow("a", 315, 54, 315, 98, "currentColor")
    b += arrow("g", 315, 154, 315, 198, GRN)
    b += arrow("b", 192, 115, 228, 115, BLUE)          # lệnh: điều khiển -> chấp hành
    b += arrow("o", 228, 140, 192, 140, ORG)            # phản hồi: chấp hành -> điều khiển
    b += T(105, 182, "lệnh →", BLUE, 15) + T(105, 204, "← phản hồi", ORG, 15)
    return wrap("0 0 420 256", "Sơ đồ khối máy CNC", b,
                "Hình 1. Máy CNC: phần điều khiển ra lệnh, phần chấp hành thực hiện và phản hồi vị trí, lỗi. Vào: phôi + chương trình; ra: chi tiết.")


def fig2_svg():
    d = ('<defs>' + ''.join(
        f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for i, c in (("x", RED), ("y", GRN), ("z", BLUE))) + '</defs>')
    b = d
    # Tiện
    b += T(10, 22, "MÁY TIỆN", "currentColor", 16, "start")
    b += f'<rect x="30" y="50" width="26" height="90" rx="4" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(43, 42, "Mâm cặp", "currentColor", 14)
    b += f'<rect x="56" y="82" width="190" height="26" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += ln(20, 95, 330, 95, "currentColor", 1.5, "6 5")
    b += T(150, 130, "Phôi", "currentColor", 14)
    b += arrow("z", 256, 95, 340, 95, BLUE)
    b += T(345, 100, "+Z", BLUE, 16, "start")
    b += arrow("x", 300, 95, 300, 38, RED)
    b += T(310, 52, "+X", RED, 16, "start")
    b += ln(180, 60, 180, 82, GRN, 4) + T(190, 66, "Dao", GRN, 14, "start")
    b += T(360, 125, "(Y: không có)", "currentColor", 14, "end", "600")
    # Phay
    b += T(10, 182, "MÁY PHAY", "currentColor", 16, "start")
    b += f'<rect x="60" y="272" width="220" height="22" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(170, 310, "Bàn máy", "currentColor", 14)
    b += f'<rect x="130" y="246" width="100" height="26" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += ln(180, 196, 180, 246, GRN, 8) + T(192, 215, "Dao", GRN, 14, "start")
    b += arrow("z", 330, 280, 330, 205, BLUE) + T(340, 212, "+Z", BLUE, 16, "start")
    b += arrow("x", 330, 280, 400, 280, RED) + T(372, 302, "+X", RED, 16, "start")
    b += arrow("y", 330, 280, 372, 242, GRN) + T(380, 244, "+Y", GRN, 16, "start")
    return wrap("0 0 420 320", "Hệ trục tọa độ máy tiện và máy phay", b,
                "Hình 2. Máy tiện: Z dọc trục chính (+Z xa mâm cặp), X theo đường kính, không có Y. Máy phay: X, Y trên mặt bàn, Z theo trục chính.")


def fig3_svg():
    d = ('<defs><marker id="h" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>')
    b = d
    b += f'<rect x="20" y="70" width="40" height="120" rx="4" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(40, 62, "Mâm cặp", "currentColor", 14)
    b += f'<rect x="60" y="100" width="190" height="60" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += ln(10, 130, 410, 130, "currentColor", 1.5, "6 5")
    # N/T trên ổ dao + mũi dao P
    b += f'<rect x="290" y="14" width="120" height="50" rx="6" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += dot(310, 39, ORG) + T(326, 45, "N/T", ORG, 17, "start")
    b += ln(300, 64, 232, 100, GRN, 4)
    b += dot(232, 100, GRN) + T(212, 92, "P", GRN, 17)
    # M, W, R trên trục
    b += dot(60, 130, BLUE) + dot(250, 130, RED) + dot(395, 130, "currentColor")
    b += ln(60, 130, 60, 205, BLUE, 2, "4 4") + T(60, 228, "M", BLUE, 18)
    b += ln(250, 130, 250, 205, RED, 2, "4 4") + T(250, 228, "W", RED, 18)
    b += ln(395, 130, 395, 205, "currentColor", 2, "4 4") + T(395, 228, "R", "currentColor", 18)
    return wrap("0 0 420 244", "Các điểm chuẩn trên máy tiện CNC", b,
                "Hình 3. Máy tiện: M gốc máy (cố định), W gốc phôi (đổi theo gá), R điểm tham chiếu, N/T điểm chuẩn ổ dao, P mũi dao.")


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
    qs[0]["question"] = "Điều gì làm máy CNC cho ra 50 chi tiết đồng đều, còn máy vạn năng thì khó?"
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Giới thiệu chung về máy tiện phay CNC", "duration_minutes": 8, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
