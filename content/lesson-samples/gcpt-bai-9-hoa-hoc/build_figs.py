#!/usr/bin/env python3
"""Sinh hình SVG cho GCPT – Bài 9 (CHM, PCM), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn). Quy ước màu: cam = cản quang/mặt nạ, xanh = tia UV, xám = phôi.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
R, B, O = "#dc2626", "#0284c7", "#ea580c"
WP = 'fill="#94a3b8" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"'
PART = 'fill="#a8a29e" fill-opacity="0.45" stroke="currentColor" stroke-width="1.6"'


def T(x, y, s, c="currentColor", size=12.5, w="400", a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{s}</text>'


def ar(x1, y1, x2, y2, c, w=2.4, L=10):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L))


def rect(x, y, w, h, attr=PART):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {attr}/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


RESIST = f'fill="{O}" fill-opacity="0.65" stroke="currentColor" stroke-width="1.2"'


def panel(ox, oy, kind):
    """Một ô mặt cắt 190 x 118: phôi (xám) + cản quang (cam) + phim/UV/hốc tuỳ bước."""
    o = []
    x0, x1, yt, yb = ox + 10, ox + 180, oy + 66, oy + 96
    gl, gr = ox + 80, ox + 110  # cửa sổ vùng cần ăn
    titles = {"a": "a) Phủ cản quang", "b": "b) Chiếu UV qua phim", "c": "c) Hiện hình", "d": "d) Ăn mòn"}
    o.append(T(ox + 4, oy + 14, titles[kind], w="700"))
    if kind == "d":
        o.append(f'<path d="M{x0},{yt} H{gl - 8} A23,20 0 0 0 {gr + 8},{yt} H{x1} V{yb} H{x0} Z" {WP}/>')
    else:
        o.append(f'<rect x="{x0}" y="{yt}" width="{x1 - x0}" height="{yb - yt}" {WP}/>')
    if kind in ("a", "b"):
        o.append(f'<rect x="{x0}" y="{yt - 7}" width="{x1 - x0}" height="7" {RESIST}/>')
    else:
        o.append(f'<rect x="{x0}" y="{yt - 7}" width="{gl - x0}" height="7" {RESIST}/>')
        o.append(f'<rect x="{gr}" y="{yt - 7}" width="{x1 - gr}" height="7" {RESIST}/>')
    if kind == "b":
        yf = yt - 26
        o.append(f'<rect x="{x0}" y="{yf}" width="{gl - x0}" height="6" fill="currentColor" fill-opacity="0.75"/>')
        o.append(f'<rect x="{gr}" y="{yf}" width="{x1 - gr}" height="6" fill="currentColor" fill-opacity="0.75"/>')
        for x in (gl + 6, gl + 15, gl + 24):
            o.append(ar(x, oy + 22, x, yt - 10, B, 1.8, 7))
        o.append(T(x1 - 2, yf - 4, "phim", size=11.5, a="end"))
    if kind == "d":
        o.append(T(gr + 34, yt + 24, "hốc ăn", size=11.5))
    if kind == "a":
        o.append(T(x0 + 2, yt + 21, "phôi", size=11.5))
        o.append(T(x1 - 2, yt - 12, "cản quang", c=O, size=11.5, a="end"))
    return "".join(o)


def fig1():
    o = [panel(0, 0, "a"), panel(210, 0, "b"), panel(0, 126, "c"), panel(210, 126, "d")]
    o.append(T(14, 262, "e) Tẩy cản quang, rửa, sấy → chi tiết hoàn chỉnh", size=12, w="700"))
    return fig(svg(274, "Bốn bước đầu của quy trình ăn mòn quang hoá", o),
               "Hình 1. PCM: cam là lớp cản quang (mặt nạ), xanh là tia UV, xám là phôi. Hốc ở bước d rộng hơn cửa sổ vì ăn lẹm.")


def fig2():
    o = []
    o.append(f'<path d="M40,96 H100 A110,50 0 0 0 320,96 H380 V196 H40 Z" {WP}/>')
    o.append(f'<rect x="40" y="89" width="110" height="7" {RESIST}/>')
    o.append(f'<rect x="270" y="89" width="110" height="7" {RESIST}/>')
    o.append(T(40, 82, "cản quang (mặt nạ)", c=O, size=12))
    o.append(T(380, 82, "cản quang", c=O, size=12, a="end"))
    o.append(T(48, 186, "phôi", size=12))
    o.append(f'<line x1="150" y1="64" x2="270" y2="64" stroke="currentColor" stroke-width="1.4"/>')
    o.append(f'<line x1="150" y1="60" x2="150" y2="68" stroke="currentColor" stroke-width="1.4"/><line x1="270" y1="60" x2="270" y2="68" stroke="currentColor" stroke-width="1.4"/>')
    o.append(T(210, 54, "cửa sổ mặt nạ", a="middle"))
    o.append(ar(210, 96, 210, 142, B, 2.2, 9))
    o.append(T(222, 124, "d", c=B, size=14, w="700"))
    o.append(ar(150, 108, 100, 108, R, 2.2, 9))
    o.append(T(118, 126, "u", c=R, size=14, w="700"))
    o.append(ar(270, 108, 320, 108, R, 2.2, 9))
    o.append(T(290, 126, "u", c=R, size=14, w="700"))
    o.append(T(14, 218, "Ăn đẳng hướng: u ≈ d, hệ số ăn mòn Fe = d / u ≈ 1", size=12.5, w="700"))
    o.append(T(14, 236, "Thành hốc cong, mép mặt nạ bị ăn lẹm vào dưới", size=12))
    return fig(svg(248, "Mặt cắt hốc ăn mòn có ăn lẹm", o),
               "Hình 2. Mặt cắt hốc ăn mòn. Xanh: độ sâu d. Đỏ: lẹm ngang u dưới mép cản quang.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
