#!/usr/bin/env python3
"""Vẽ hình SVG cho tab Bài mẫu CNC (Bài 2 tiện, Bài 3 phay).

Chạy: python3 scripts/cnc/ve-hinh-bai-mau.py  → ghi services/cnc-worked-examples-hinh.ts
Hình nét đơn giản, màu theo currentColor (đổi theo nền sáng/tối); viewBox rộng 360 để chữ 16 ≈ 13px ở màn 360px.
Toạ độ trong hình lấy đúng số trên bản vẽ của từng ví dụ ở services/cnc-worked-examples.ts — sửa số thì sửa cả hai.
"""
from __future__ import annotations

import json
import math
import pathlib

W = 360
ACCENT = "#ea580c"  # điểm W, điểm bắt đầu
FONT = 'font-family="ui-sans-serif,system-ui,sans-serif" font-size="16"'


def num(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def svg(height: int, body: list[str], label: str) -> str:
    return (
        f'<svg viewBox="0 0 {W} {height}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg" '
        f'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">' + "".join(body) + "</svg>"
    )


def text(x: float, y: float, s: str, anchor: str = "middle", color: str = "currentColor", weight: str = "500") -> str:
    return (
        f'<text x="{num(x)}" y="{num(y)}" text-anchor="{anchor}" fill="{color}" stroke="none" font-weight="{weight}" {FONT}>{s}</text>'
    )


# ---------------------------------------------------------------- TIỆN
def turning(
    label: str,
    stock_d: float,
    start: tuple[float, float],
    segs: list[tuple],
    stock_end: float,
    k: float,
    diam_labels: list[tuple[float, str, int]],
    z_ticks: list[tuple[float, int]],
    notes: list[tuple[float, float, str, str]],
    face_x: float = 300,
) -> str:
    """start=(z,d); segs: ('L', z, d) | ('A', z, d, r, 'G02'|'G03'). z ≤ 0, mặt đầu phải z=0 (gốc W)."""
    yc = 40 + stock_d / 2 * k + 34  # chừa 2 hàng nhãn Ø phía trên

    def X(z: float) -> float:
        return face_x + z * k

    def Yt(d: float) -> float:
        return yc - d / 2 * k

    def Yb(d: float) -> float:
        return yc + d / 2 * k

    # đường bao trên
    top = [f"M{num(X(start[0]))} {num(Yt(start[1]))}"]
    pts = [(start[0], start[1])]
    for s in segs:
        if s[0] == "L":
            top.append(f"L{num(X(s[1]))} {num(Yt(s[2]))}")
        else:
            _, z, d, r, g = s
            sweep = 1 if g == "G02" else 0
            top.append(f"A{num(r * k)} {num(r * k)} 0 0 {sweep} {num(X(z))} {num(Yt(d))}")
        pts.append((s[1], s[2]))
    end_z, end_d = pts[-1]
    if end_d < stock_d:
        top.append(f"L{num(X(end_z))} {num(Yt(stock_d))}")
    chuck_x = X(stock_end)
    top.append(f"L{num(chuck_x)} {num(Yt(stock_d))}")
    top.append(f"L{num(chuck_x)} {num(Yb(stock_d))}")
    if end_d < stock_d:
        top.append(f"L{num(X(end_z))} {num(Yb(stock_d))}")
    # đường bao dưới, đi ngược
    bottom = [f"L{num(X(end_z))} {num(Yb(end_d))}"]
    for i in range(len(segs) - 1, -1, -1):
        s = segs[i]
        pz, pd = pts[i]
        if s[0] == "L":
            bottom.append(f"L{num(X(pz))} {num(Yb(pd))}")
        else:
            _, z, d, r, g = s
            sweep = 1 if g == "G02" else 0  # lật gương + đi ngược = giữ nguyên chiều quét
            bottom.append(f"A{num(r * k)} {num(r * k)} 0 0 {sweep} {num(X(pz))} {num(Yb(pd))}")
    outline = " ".join(top + bottom) + " Z"

    body: list[str] = []
    # phôi ban đầu (nét đứt)
    body.append(
        f'<rect x="{num(chuck_x)}" y="{num(Yt(stock_d))}" width="{num(X(0) - chuck_x)}" height="{num(stock_d * k)}" '
        f'stroke-width="1.2" stroke-dasharray="5 4" opacity=".45"/>'
    )
    body.append(f'<path d="{outline}" stroke-width="2.2" fill="currentColor" fill-opacity=".08"/>')
    # mâm cặp
    jaw_w = 16
    body.append(
        f'<rect x="{num(chuck_x - jaw_w)}" y="{num(Yt(stock_d) - 6)}" width="{jaw_w}" height="22" stroke-width="1.5" fill="currentColor" fill-opacity=".25"/>'
    )
    body.append(
        f'<rect x="{num(chuck_x - jaw_w)}" y="{num(Yb(stock_d) - 16)}" width="{jaw_w}" height="22" stroke-width="1.5" fill="currentColor" fill-opacity=".25"/>'
    )
    # đường tâm
    body.append(
        f'<line x1="{num(chuck_x - jaw_w - 6)}" y1="{num(yc)}" x2="{num(X(0) + 30)}" y2="{num(yc)}" stroke-width="1" stroke-dasharray="14 4 3 4" opacity=".7"/>'
    )
    # gốc W
    body.append(f'<circle cx="{num(X(0))}" cy="{num(yc)}" r="5" stroke="{ACCENT}" stroke-width="2.4" fill="none"/>')
    body.append(text(X(0) + 10, yc - 8, "W", "start", ACCENT, "700"))
    # trục toạ độ nhỏ: +X lên, Z sang phải
    ax, ay = X(0) + 30, yc + 40
    body.append(f'<path d="M{num(ax)} {num(ay)} h22 M{num(ax+22)} {num(ay)} l-6 -4 M{num(ax+22)} {num(ay)} l-6 4" stroke-width="1.5"/>')
    body.append(f'<path d="M{num(ax)} {num(ay)} v-22 M{num(ax)} {num(ay-22)} l-4 6 M{num(ax)} {num(ay-22)} l4 6" stroke-width="1.5"/>')
    body.append(text(ax + 26, ay + 5, "Z", "start"))
    body.append(text(ax - 4, ay - 28, "X", "middle"))
    # nhãn đường kính phía trên
    for z, s, row in diam_labels:
        y = Yt(stock_d) - 12 - row * 20
        body.append(text(X(z), y, s))
    # mốc Z tính từ mặt đầu (ghi kích thước kiểu toạ độ)
    y0 = Yb(stock_d) + 8
    for z, row in z_ticks:
        y1 = y0 + 14 + row * 18
        body.append(f'<line x1="{num(X(z))}" y1="{num(y0)}" x2="{num(X(z))}" y2="{num(y1)}" stroke-width="1" opacity=".7"/>')
        body.append(text(X(z), y1 + 15, num(abs(z))))
    body.append(f'<line x1="{num(X(0))}" y1="{num(y0)}" x2="{num(X(0))}" y2="{num(y0 + 14)}" stroke-width="1" opacity=".7"/>')
    body.append(text(X(0), y0 + 29, "0"))
    for z, d, s, anchor in notes:
        body.append(text(X(z), Yt(d), s, anchor))
    max_row = max([r for _, r in z_ticks] + [0])
    height = int(y0 + 14 + max_row * 18 + 26)
    return svg(height, body, label)


# ---------------------------------------------------------------- PHAY (nhìn từ trên xuống)
def rounded_rect(x0: float, y0: float, x1: float, y1: float, r: float, P) -> str:
    """Hình chữ nhật bo góc trong toạ độ chi tiết (y hướng lên), P(x,y)→(px,py)."""
    def p(x, y):
        a, b = P(x, y)
        return f"{num(a)} {num(b)}"

    rr = r * P.k
    return (
        f"M{p(x0 + r, y0)} L{p(x1 - r, y0)} A{num(rr)} {num(rr)} 0 0 0 {p(x1, y0 + r)} "
        f"L{p(x1, y1 - r)} A{num(rr)} {num(rr)} 0 0 0 {p(x1 - r, y1)} "
        f"L{p(x0 + r, y1)} A{num(rr)} {num(rr)} 0 0 0 {p(x0, y1 - r)} "
        f"L{p(x0, y0 + r)} A{num(rr)} {num(rr)} 0 0 0 {p(x0 + r, y0)} Z"
    )


class Mapper:
    def __init__(self, k: float, ox: float, oy: float):
        self.k, self.ox, self.oy = k, ox, oy

    def __call__(self, x: float, y: float):
        return self.ox + x * self.k, self.oy - y * self.k


def axes(P: Mapper, x: float, y: float) -> list[str]:
    ox, oy = P(x, y)
    return [
        f'<circle cx="{num(ox)}" cy="{num(oy)}" r="5" stroke="{ACCENT}" stroke-width="2.4"/>',
        f'<path d="M{num(ox)} {num(oy)} h26 m0 0 l-6 -4 m6 4 l-6 4 M{num(ox)} {num(oy)} v-26 m0 0 l-4 6 m4 -6 l4 6" stroke="{ACCENT}" stroke-width="1.6"/>',
        text(ox + 30, oy + 5, "X", "start", ACCENT, "700"),
        text(ox, oy - 31, "Y", "middle", ACCENT, "700"),
        text(ox - 8, oy + 19, "W", "end", ACCENT, "700"),
    ]


def hdim(P: Mapper, x0: float, x1: float, y_px: float, s: str) -> list[str]:
    a, _ = P(x0, 0)
    b, _ = P(x1, 0)
    return [
        f'<path d="M{num(a)} {num(y_px)} H{num(b)} M{num(a)} {num(y_px-5)} v10 M{num(b)} {num(y_px-5)} v10" stroke-width="1" opacity=".8"/>',
        text((a + b) / 2, y_px - 6, s),
    ]


def vdim(P: Mapper, y0: float, y1: float, x_px: float, s: str) -> list[str]:
    _, a = P(0, y0)
    _, b = P(0, y1)
    return [
        f'<path d="M{num(x_px)} {num(a)} V{num(b)} M{num(x_px-5)} {num(a)} h10 M{num(x_px-5)} {num(b)} h10" stroke-width="1" opacity=".8"/>',
        text(x_px + 8, (a + b) / 2 + 5, s, "start"),
    ]


def phay_vd1() -> str:
    # phôi 60×50, chi tiết 50×40 bo R5, W ở tâm
    P = Mapper(4.4, 165, 140)
    sx0, sy0 = P(-30, 25)
    b: list[str] = [
        f'<rect x="{num(sx0)}" y="{num(sy0)}" width="{num(60*P.k)}" height="{num(50*P.k)}" stroke-width="1.2" stroke-dasharray="5 4" opacity=".45"/>',
        f'<path d="{rounded_rect(-25, -20, 25, 20, 5, P)}" stroke-width="2.2" fill="currentColor" fill-opacity=".08"/>',
    ]
    b += axes(P, 0, 0)
    b += hdim(P, -25, 25, P(0, 25)[1] - 10, "50")
    b += vdim(P, -20, 20, P(25, 0)[0] + 32, "40")
    rx, ry = P(25 - 5 + 5 * math.cos(math.pi / 4), 20 - 5 + 5 * math.sin(math.pi / 4))
    b.append(f'<path d="M{num(rx)} {num(ry)} l14 -14 h10" stroke-width="1"/>')
    b.append(text(rx + 26, ry - 10, "R5", "start"))
    b.append(text(P(-30, 0)[0], P(0, -25)[1] + 26, "Phôi 60×50 (nét đứt) · sâu 3", "start"))
    return svg(300, b, "Tấm 50×40 bo 4 góc R5, gốc W ở tâm")


def plate(P: Mapper, holes: bool, pocket: bool) -> list[str]:
    x0, y0 = P(0, 60)
    b = [f'<rect x="{num(x0)}" y="{num(y0)}" width="{num(80*P.k)}" height="{num(60*P.k)}" stroke-width="2.2" fill="currentColor" fill-opacity=".06"/>']
    for hx, hy in [(10, 10), (70, 10), (70, 50), (10, 50)]:
        cx, cy = P(hx, hy)
        if holes:
            b.append(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(4*P.k)}" stroke-width="2"/>')
            b.append(f'<path d="M{num(cx-24)} {num(cy)} h48 M{num(cx)} {num(cy-24)} v48" stroke-width=".9" stroke-dasharray="8 3 2 3" opacity=".7"/>')
        else:
            b.append(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(4*P.k)}" stroke-width="1.2" opacity=".45"/>')
    if pocket:
        b.append(f'<path d="{rounded_rect(25, 20, 55, 40, 6, P)}" stroke-width="2.2" fill="currentColor" fill-opacity=".14"/>')
    return b


def phay_vd2() -> str:
    P = Mapper(3.4, 50, 250)
    b = plate(P, True, False)
    b += axes(P, 0, 0)
    b += hdim(P, 0, 10, P(0, 60)[1] - 10, "10")
    b += hdim(P, 10, 70, P(0, 60)[1] - 10, "60")
    b += hdim(P, 0, 80, P(0, 60)[1] - 38, "80")
    b += vdim(P, 0, 10, P(80, 0)[0] + 12, "10")
    b += vdim(P, 10, 50, P(80, 0)[0] + 12, "40")
    cx, cy = P(70, 50)
    b.append(f'<path d="M{num(cx+10)} {num(cy+10)} l18 18" stroke-width="1"/>')
    b.append(text(P(40, 0)[0], P(0, 30)[1] + 6, "4 lỗ Ø8 xuyên"))
    b.append(text(P(40, 0)[0], P(0, 30)[1] + 28, "tấm dày 12", "middle"))
    return svg(300, b, "Tấm 80×60 dày 12 với 4 lỗ Ø8 cách mép 10, gốc W ở góc dưới trái")


def phay_vd3() -> str:
    P = Mapper(3.4, 50, 250)
    b = plate(P, False, True)
    b += axes(P, 0, 0)
    b += hdim(P, 0, 25, P(0, 60)[1] - 10, "25")
    b += hdim(P, 25, 55, P(0, 60)[1] - 10, "30")
    b += vdim(P, 0, 20, P(80, 0)[0] + 12, "20")
    b += vdim(P, 20, 40, P(80, 0)[0] + 12, "20")
    rx, ry = P(55 - 6 + 6 * math.cos(math.pi / 4), 40 - 6 + 6 * math.sin(math.pi / 4))
    b.append(f'<path d="M{num(rx)} {num(ry)} l16 -16 h8" stroke-width="1"/>')
    b.append(text(rx + 27, ry - 11, "R6", "start"))
    b.append(text(P(40, 0)[0], P(0, 30)[1] + 6, "sâu 3"))
    b.append(text(P(40, 0)[0], P(0, 12)[1] + 6, "hốc 30×20, tâm (40; 30)"))
    return svg(300, b, "Hốc chữ nhật 30×20 bo góc R6 ở giữa tấm 80×60, gốc W ở góc dưới trái")


def tien_vd1() -> str:
    return turning(
        "Trục bậc Ø26 dài 18, vát 1×45°, phôi Ø32",
        32, (0, 24), [("L", -1, 26), ("L", -18, 26), ("L", -18, 32)], -36, 5.6,
        [(-9, "Ø26", 0), (-27, "Ø32", 0)],
        [(-18, 0)],
        [(0.4, 30, "1×45°", "start")],
        face_x=290,
    )


def tien_vd2() -> str:
    return turning(
        "Côn Ø16–Ø24 dài 12, Ø24 tới 22, cung R6 lên Ø36, Ø36 tới 40",
        40, (0, 16), [("L", -12, 24), ("L", -22, 24), ("A", -28, 36, 6, "G02"), ("L", -40, 36), ("L", -40, 40)], -48, 4.8,
        [(-1.5, "Ø16", 0), (-17, "Ø24", 0), (-34, "Ø36", 0), (-44, "Ø40", 1)],
        [(-12, 0), (-22, 0), (-28, 1), (-40, 0)],
        [(-22.6, 31.5, "R6", "end")],
        face_x=300,
    )


def tien_vd3() -> str:
    return turning(
        "Trục nhiều bậc: vát 2×45°, Ø20, Ø26 côn lên Ø30, cung R4 lên Ø38, phôi Ø40",
        40, (0, 16),
        [("L", -2, 20), ("L", -15, 20), ("L", -15, 26), ("L", -25, 30), ("L", -35, 30), ("A", -39, 38, 4, "G02"), ("L", -50, 38), ("L", -50, 40)],
        -56, 4.3,
        [(-8, "Ø20", 0), (-15, "Ø26", 1), (-27, "Ø30", 0), (-45, "Ø38", 0)],
        [(-2, 1), (-15, 0), (-25, 1), (-35, 0), (-39, 1), (-50, 0)],
        [(0.6, 26, "2×45°", "start"), (-35.8, 34, "R4", "end")],
        face_x=300,
    )


FIGS = {
    "tien-vd1": tien_vd1(),
    "tien-vd2": tien_vd2(),
    "tien-vd3": tien_vd3(),
    "phay-vd1": phay_vd1(),
    "phay-vd2": phay_vd2(),
    "phay-vd3": phay_vd3(),
}

out = pathlib.Path(__file__).resolve().parents[2] / "services" / "cnc-worked-examples-hinh.ts"
lines = [
    "// SINH TỰ ĐỘNG bởi scripts/cnc/ve-hinh-bai-mau.py — đừng sửa tay, sửa script rồi chạy lại.",
    "export const CNC_WORKED_FIGURES: Record<string, string> = {",
]
for key, value in FIGS.items():
    lines.append(f"  {json.dumps(key)}: {json.dumps(value, ensure_ascii=False)},")
lines.append("};")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
for key, value in FIGS.items():
    print(key, len(value), "bytes")
