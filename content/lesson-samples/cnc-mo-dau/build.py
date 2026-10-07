#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Phần mở đầu. Chạy: python3 build.py"""
import json, pathlib, re, math
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 13  # điền theo lint_do_dai.py


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
    b = ""
    b += f'<circle cx="210" cy="34" r="9" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += f'<circle cx="210" cy="62" r="22" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += f'<rect x="194" y="55" width="32" height="10" rx="3" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    b += ln(210, 84, 210, 172) + ln(210, 102, 165, 150) + ln(210, 102, 255, 150)
    b += ln(210, 172, 190, 250) + ln(210, 172, 230, 250)
    b += dot(165, 150, "currentColor", 5) + dot(188, 126, ORG, 7) + dot(255, 150, RED, 7)
    b += f'<rect x="168" y="250" width="40" height="13" rx="4" fill="{GRN}"/>' + f'<rect x="214" y="250" width="40" height="13" rx="4" fill="{GRN}"/>'
    b += ln(30, 266, 390, 266, "currentColor", 1.5)
    b += ln(150, 34, 200, 34, "currentColor", 1.5) + T(145, 39, "Tóc buộc gọn", "currentColor", 14, "end")
    b += ln(150, 126, 180, 126, ORG, 1.5) + T(145, 131, "Tay áo cài gọn", ORG, 14, "end")
    b += ln(130, 252, 168, 254, GRN, 1.5) + T(125, 258, "Giày kín mũi", GRN, 14, "end")
    b += ln(228, 60, 270, 60, BLUE, 1.5) + T(275, 65, "Kính bảo hộ", BLUE, 14, "start")
    b += ln(262, 150, 272, 150, RED, 1.5) + T(275, 138, "Không đeo găng", RED, 14, "start") + T(275, 157, "khi máy còn quay", RED, 14, "start")
    return wrap("0 0 420 280", "Người đứng máy với trang phục bảo hộ đúng", b,
                "Hình 1. Kiểm tra bản thân trước khi đứng máy: tóc, kính, tay áo, giày; không găng khi chi tiết còn quay.")


def fig2_svg():
    d = ('<defs><marker id="cnc0-h" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>')
    b = d
    rows = [("1. NHẤN nút dừng khẩn", RED), ("2. CHỜ mọi chuyển động dừng hẳn", ORG),
            ("3. BÁO giảng viên, giữ nguyên hiện trường", BLUE), ("4. CHỈ chạy lại khi được cho phép", GRN)]
    for i, (t, c) in enumerate(rows):
        y = 10 + 70 * i
        b += box(30, y, 360, 48, c) + T(210, y + 30, t, c, 15)
        if i < 3:
            b += arrow("cnc0-h", 210, y + 48, 210, y + 68, "currentColor", 2.5)
    return wrap("0 0 420 270", "Bốn bước sau khi có sự cố", b,
                "Hình 2. Sau khi xảy ra sự cố: nhấn nút dừng khẩn, chờ dừng hẳn, báo giảng viên, chỉ chạy lại khi được phép.")


def fig3_svg():
    rows = [("Seiri · Sàng lọc", "bỏ cái không cần", RED), ("Seiton · Sắp xếp", "mỗi thứ một chỗ", ORG),
            ("Seiso · Sạch sẽ", "lau và kiểm tra", GRN), ("Seiketsu · Săn sóc", "giữ thành chuẩn", BLUE),
            ("Shitsuke · Sẵn sàng", "thành thói quen", "currentColor")]
    b = ""
    for i, (a, t, c) in enumerate(rows):
        y = 8 + 60 * i
        b += box(15, y, 390, 50, c) + T(30, y + 31, a, c, 16, "start") + T(392, y + 31, t, "currentColor", 14, "end", "600")
    return wrap("0 0 420 310", "Năm bước 5S", b,
                "Hình 3. 5S: năm chữ S theo thứ tự, mỗi chữ một việc cụ thể ở xưởng.")


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
    qs[0]["question"] = "Máy đang quay, phoi dài quấn quanh phôi, một bạn đeo găng định gạt phoi. Việc đúng nhất là gì?"
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — An toàn lao động và 5S", "duration_minutes": 8, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
