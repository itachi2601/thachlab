#!/usr/bin/env python3
"""Sinh hình SVG cho GCPT – Bài 8 (EBM + plasma), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn). Quy ước màu: đỏ = chùm/hồ quang, xanh = chuyển động, cam = kim loại nóng/điện cực.
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


def fig1():
    o = []
    o.append(rect(130, 12, 40, 16, f'fill="{O}" fill-opacity="0.6" stroke="currentColor" stroke-width="1.6"'))
    o.append(T(182, 25, "Catốt nung nóng phát electron"))
    o.append(rect(106, 44, 36, 8)); o.append(rect(158, 44, 36, 8))
    o.append(T(206, 54, "Anốt: tăng tốc, 50–150 kV"))
    o.append(rect(100, 94, 24, 28)); o.append(rect(176, 94, 24, 28))
    o.append(T(212, 112, "Thấu kính từ: hội tụ chùm"))
    o.append(rect(108, 136, 16, 16)); o.append(rect(176, 136, 16, 16))
    o.append(T(212, 148, "Cuộn lệch: quét chùm", size=12))
    o.append(f'<polygon points="146,30 154,30 151,236 149,236" fill="{R}"/>')
    o.append(chevron(150, 82, 0, 1, R, 2, 9))
    o.append(chevron(150, 168, 0, 1, R, 2, 9))
    o.append(f'<rect x="20" y="172" width="250" height="108" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="6 4"/>')
    o.append(T(28, 190, "Buồng chân không", w="700"))
    o.append(rect(95, 236, 110, 26, WP))
    o.append(f'<polygon points="144,236 156,236 150,250" fill="#ffffff" stroke="currentColor" stroke-width="1.2"/>')
    o.append(rect(80, 262, 140, 8, PART))
    o.append(T(28, 212, "chùm hội tụ", c=R, w="700"))
    o.append(T(28, 227, "vết cỡ vài chục µm", c=R, size=12))
    o.append(T(104, 254, "phôi", a="start", size=12))
    o.append(f'<line x1="270" y1="226" x2="296" y2="226" stroke="currentColor" stroke-width="2.2"/>')
    o.append(rect(296, 206, 112, 40, PART))
    o.append(T(352, 231, "Bơm chân không", a="middle", size=12))
    o.append(T(14, 305, "Tia X phát ra khi electron bị hãm → vỏ máy che chắn kín", size=12, w="700"))
    return fig(svg(316, "Sơ đồ máy gia công chùm điện tử", o),
               "Hình 1. Sơ đồ nguyên lý EBM. Chùm electron (đỏ) đi từ catốt xuống phôi trong buồng đã hút chân không.")


def fig2():
    o = []
    o.append(rect(120, 12, 60, 54, 'fill="none" stroke="currentColor" stroke-width="1.8"'))
    o.append(T(14, 30, "Mỏ cắt", w="700"))
    o.append(rect(144, 28, 12, 44, f'fill="{O}" fill-opacity="0.7" stroke="currentColor" stroke-width="1.4"'))
    o.append(T(196, 40, "Điện cực (âm)"))
    o.append(f'<polygon points="124,66 176,66 158,102 142,102" {PART}/>')
    o.append(T(196, 92, "Vòi phun thu hẹp"))
    o.append(ar(60, 46, 116, 52, B))
    o.append(T(14, 62, "Khí nén", c=B, w="700"))
    o.append(f'<polygon points="146,102 154,102 151,152 149,152" fill="{R}"/>')
    o.append(T(196, 130, "Hồ quang plasma", c=R, w="700"))
    o.append(rect(50, 152, 96, 40, WP)); o.append(rect(156, 152, 94, 40, WP))
    o.append(T(34, 176, "phôi", size=12, a="end"))
    for dy in (0, 12, 24):
        o.append(f'<circle cx="{151 + (dy % 8) - 4}" cy="{200 + dy}" r="2.4" fill="{O}"/>')
    o.append(T(166, 226, "Kim loại chảy bị thổi xuống", c=O, size=12))
    o.append(f'<line x1="250" y1="172" x2="330" y2="172" stroke="currentColor" stroke-width="2.2"/>')
    o.append(T(256, 164, "Kẹp nối phôi (cực dương)", size=12))
    o.append(ar(300, 54, 380, 54, B))
    o.append(T(300, 44, "Hướng cắt", c=B, size=12, w="700"))
    return fig(svg(244, "Sơ đồ cắt plasma", o),
               "Hình 2. Cắt plasma. Hồ quang giữa điện cực và phôi ion hoá khí; tia plasma nóng chảy kim loại và thổi xỉ ra khỏi rãnh cắt.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
