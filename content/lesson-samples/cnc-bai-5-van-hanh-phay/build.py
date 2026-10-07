#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 5 (phay MILL 55). Chạy: python3 build.py"""
import json, pathlib, re, math
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 17  # điền theo lint_do_dai.py (làm tròn lên)


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



def mk(ids):
    return '<defs>' + ''.join(
        f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for i, c in ids) + '</defs>'


def rect(x, y, w, h, c="currentColor", sw=2.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="none" stroke="{c}" stroke-width="{sw}"/>'


def fig1_svg():
    b = mk((("m1x", RED), ("m1y", GRN), ("m1z", BLUE)))
    # chấp hành
    b += T(205, 22, "CHẤP HÀNH", ORG, 16)
    b += f'<circle cx="70" cy="66" r="30" fill="none" stroke="{ORG}" stroke-width="2.5"/>'
    for k in range(8):
        a = 2 * math.pi * k / 8
        b += f'<circle cx="{70+20*math.cos(a):.1f}" cy="{66+20*math.sin(a):.1f}" r="4" fill="{ORG}"/>'
    b += T(70, 22, "Ổ dao 8 vị trí", "currentColor", 15)
    b += rect(200, 40, 40, 222)                      # thân máy
    b += rect(110, 50, 90, 40)                       # đầu trục chính
    b += rect(140, 90, 24, 40)                       # trục chính
    b += ln(152, 130, 152, 164, GRN, 8)              # dao
    b += T(134, 118, "Trục chính", "currentColor", 15, "end")
    b += T(164, 156, "Dao", GRN, 15, "start")
    b += rect(124, 172, 56, 24) + rect(100, 196, 104, 26) + rect(40, 222, 170, 16)
    b += T(94, 214, "Ê-tô + phôi", "currentColor", 15, "end")
    b += rect(20, 262, 240, 24) + T(140, 280, "Đế máy", "currentColor", 15)
    b += T(125, 255, "Bàn máy", "currentColor", 15)
    # điều khiển
    b += rect(286, 34, 124, 150, BLUE) + T(348, 58, "ĐIỀU KHIỂN", BLUE, 16)
    b += rect(300, 70, 96, 46) + T(348, 99, "Màn hình", "currentColor", 15)
    b += rect(300, 128, 96, 40) + T(348, 154, "Bàn phím", "currentColor", 15)
    # hệ trục
    b += arrow("m1x", 320, 270, 382, 270, RED) + T(386, 276, "+X", RED, 16, "start")
    b += arrow("m1z", 320, 270, 320, 206, BLUE) + T(328, 214, "+Z", BLUE, 16, "start")
    b += arrow("m1y", 320, 270, 356, 236, GRN) + T(362, 240, "+Y", GRN, 16, "start")
    return wrap("0 0 420 296", "Sơ đồ máy phay CNC EMCO MILL 55", b,
                "Hình 1. Máy phay CNC (sơ đồ minh hoạ, không theo tỉ lệ): phần chấp hành bên trái, phần điều khiển bên phải; Z theo trục chính, X và Y trên mặt bàn.")


def fig2_svg():
    b = ""
    b += rect(40, 240, 300, 18) + rect(120, 214, 140, 26) + rect(150, 170, 90, 44)
    b += T(195, 198, "Phôi", "currentColor", 15) + T(190, 234, "Ê-tô", "currentColor", 15)
    b += rect(160, 30, 70, 40) + rect(183, 70, 24, 36)
    b += ln(195, 106, 195, 150, GRN, 8)
    b += dot(150, 170, RED) + T(140, 164, "W gốc phôi", RED, 15, "end")
    b += dot(195, 106, ORG) + T(214, 112, "N chuẩn dao", ORG, 15, "start")
    b += dot(195, 150, GRN) + T(214, 156, "P mũi dao", GRN, 15, "start")
    b += dot(40, 258, BLUE) + T(30, 282, "M gốc máy", BLUE, 15, "start")
    b += dot(390, 66, "currentColor") + T(406, 96, "R tham chiếu", "currentColor", 15, "end")
    return wrap("0 0 420 292", "Các điểm chuẩn trên máy phay CNC", b,
                "Hình 2. Điểm chuẩn trên máy phay (nhìn chính diện): W ở góc phôi, N ở mũi trục chính, P ở đỉnh dao. Vị trí M, R trên hình chỉ minh hoạ, vị trí thật xem sổ tay máy.")


def fig3_svg():
    b = mk((("m3x", RED), ("m3y", GRN), ("m3r", "currentColor")))
    b += rect(170, 60, 200, 150) + T(270, 142, "Phôi", "currentColor", 16)
    b += dot(170, 210, RED) + T(160, 234, "W", RED, 17, "end")
    # dò X: chạm cạnh trái
    b += f'<circle cx="140" cy="130" r="30" fill="none" stroke="{GRN}" stroke-width="2.5"/>' + dot(140, 130, GRN, 4)
    b += arrow("m3r", 140, 130, 169, 130, "currentColor", 2) + T(152, 122, "R", "currentColor", 15)
    b += T(104, 136, "Xmachine", GRN, 15, "end")
    b += ln(170, 40, 170, 60, RED, 2, "4 3") + T(170, 34, "Xphôi", RED, 15)
    # dò Y: chạm cạnh trước
    b += f'<circle cx="290" cy="240" r="30" fill="none" stroke="{GRN}" stroke-width="2.5"/>' + dot(290, 240, GRN, 4)
    b += arrow("m3r", 290, 240, 290, 211, "currentColor", 2) + T(298, 232, "R", "currentColor", 15, "start")
    b += T(326, 246, "Ymachine", GRN, 15, "start")
    b += T(206, 232, "Yphôi", RED, 15, "start")
    b += T(290, 290, "phía người đứng máy", "currentColor", 14, "middle", "600")
    # hệ trục
    b += arrow("m3x", 30, 280, 80, 280, RED) + T(84, 286, "+X", RED, 16, "start")
    b += arrow("m3y", 30, 280, 30, 232, GRN) + T(38, 240, "+Y", GRN, 16, "start")
    return wrap("0 0 420 298", "Dò cạnh phôi theo X và Y nhìn từ trên", b,
                "Hình 3. Nhìn từ trên xuống: dò cạnh trái (X) và cạnh trước (Y). Màn hình báo tọa độ tâm dao; tâm dao cách cạnh phôi đúng một bán kính R.")


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
    qs[0]["question"] = "Nếu chạy luôn với Offset và gốc phôi của nhóm trước (phôi khác chiều cao, dao lắp lại), chuyện gì dễ xảy ra nhất?"
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Vận hành và cài đặt máy phay CNC EMCO MILL 55", "duration_minutes": 8, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
