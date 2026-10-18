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
    cols = [(BLUE, "A. TỐI TRƯỚC", ["Đọc 2 mục", "Quiz 5 câu", "Gửi 1 câu hỏi"], "~20 phút"),
            (GRN, "B. TRONG BUỔI", ["GV dạy ~1 giờ", "Thao tác ~3,5 giờ", "Phiếu nhóm"], "5 giờ"),
            (ORG, "C. SAU BUỔI", ["Trả bài", "Tự đánh dấu"], "~10 phút")]
    for i, (c, head, items, tm) in enumerate(cols):
        x = 10 + i * 140
        b += box(x, 20, 126, 150, c) + T(x + 63, 46, head, c, 15)
        for j, it in enumerate(items):
            b += T(x + 63, 76 + j * 24, it, "currentColor", 14, "middle", "600")
        b += T(x + 63, 158, tm, c, 14)
        if i < 2:
            b += f'<path d="M{x+128},95 l10,0" stroke="currentColor" stroke-width="2.5"/>'
    return wrap("0 0 430 190", "Ba giai đoạn của một buổi lớp đảo ngược", b,
                "Hình 1. Chuẩn bị tối trước, dạy và thao tác trong buổi, củng cố sau buổi.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = src.replace("__FIG1__", fig1()).replace("__PHUT__", str(PHUT))
(HERE / "theory.html").write_text(html, encoding="utf8")
print("ok", len(html))
