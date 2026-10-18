#!/usr/bin/env python3
"""Dựng theory.html cho CNC Bài 1 bản lớp đảo ngược (mẫu). Chạy: python3 build.py"""
import pathlib
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 20


def T(x, y, s, c="currentColor", size=15, anchor="middle", w="700"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def box(x, y, w, h, c):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="{c}" stroke-width="2.5"/>'


def fig1():
    b = ""
    cols = [(BLUE, "A. GV DẠY", ["Nội quy · an toàn", "Máy · điểm chuẩn", "WinNC · lệnh"], "~115 phút"),
            (GRN, "B. HAI TRẠM", ["Máy thật", "WinNC 3D View", "Đổi trạm"], "150 phút"),
            (ORG, "C. KẾT BUỔI", ["Trả bài", "Dặn buổi 2"], "20 phút")]
    for i, (c, head, items, tm) in enumerate(cols):
        x = 10 + i * 140
        b += box(x, 20, 126, 150, c) + T(x + 63, 46, head, c, 15)
        for j, it in enumerate(items):
            b += T(x + 63, 76 + j * 24, it, "currentColor", 14, "middle", "600")
        b += T(x + 63, 158, tm, c, 14)
        if i < 2:
            b += f'<path d="M{x+128},95 l10,0" stroke="currentColor" stroke-width="2.5"/>'
    return wrap("0 0 430 190", "Ba phần của buổi 1", b,
                "Hình 1. Giảng viên dạy khoảng 2 giờ, thực hành hai trạm, kết buổi và dặn bài.")


def fig2():
    d = ('<defs>' + ''.join(
        f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for i, c in (("fx", RED), ("fz", BLUE))) + '</defs>')
    b = d
    px = lambda z: 250 + z * 7
    py = lambda x: 130 - x / 2 * 5
    b += f'<rect x="40" y="{py(26)}" width="{px(0)-40}" height="{130-py(26)}" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(150, 150, "Phôi", "currentColor", 14)
    b += f'<line x1="20" y1="130" x2="340" y2="130" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 5"/>'
    A, B, C, D, E_ = (px(5), py(30)), (px(2), py(20)), (px(-20), py(20)), (px(-20), py(30)), (px(5), py(30))
    seg = lambda p, q, col, dash="": f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{col}" stroke-width="3.5"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
    b += seg(A, B, ORG, "7 5") + seg(B, C, GRN) + seg(C, D, GRN) + seg(D, E_, ORG, "7 5")
    for (p, s_) in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
        b += f'<circle cx="{p[0]}" cy="{p[1]}" r="5" fill="currentColor"/>'
    b += T(A[0] + 14, A[1] - 8, "A", "currentColor", 16) + T(B[0] + 14, B[1] + 4, "B", "currentColor", 16)
    b += T(C[0] - 4, C[1] + 20, "C", "currentColor", 16) + T(D[0] - 4, D[1] - 10, "D", "currentColor", 16)
    b += f'<line x1="300" y1="130" x2="300" y2="70" stroke="{RED}" stroke-width="3" marker-end="url(#fx)"/>' + T(312, 86, "+X", RED, 15, "start")
    b += f'<line x1="300" y1="130" x2="350" y2="130" stroke="{BLUE}" stroke-width="3" marker-end="url(#fz)"/>' + T(332, 150, "+Z", BLUE, 15, "start")
    b += T(10, 20, "Nét đứt: G00 chạy nhanh. Nét liền: G01 cắt theo F.", "currentColor", 13, "start", "600")
    return wrap("0 0 420 170", "Đường đi của dao trong chương trình O0001", b,
                "Hình 2. A(N40) → B(N50) chạy nhanh; B → C(N60) tiện trụ; C → D(N70) lùi ra; D → A(N80) về an toàn.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = src.replace("__FIG1__", fig1()).replace("__FIG2__", fig2())
(HERE / "theory.html").write_text(html, encoding="utf8")
print("ok", len(html))
