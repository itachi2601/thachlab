#!/usr/bin/env python3
"""Sinh hình SVG cho GCPT – Bài 10 (bồi đắp, lai), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn). Quy ước màu: đỏ = laser/vũng chảy, xanh = chuyển động, cam = bột/kim loại đắp.
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


PWD = f'fill="{O}" fill-opacity="0.18" stroke="none"'
SOLID = f'fill="{O}" fill-opacity="0.65" stroke="currentColor" stroke-width="1.6"'


def fig1():
    o = []
    o.append(rect(14, 12, 64, 26)); o.append(T(46, 29, "Laser", a="middle", w="700"))
    o.append(f'<line x1="78" y1="25" x2="150" y2="25" stroke="{R}" stroke-width="2.4"/>')
    o.append(f'<line x1="140" y1="36" x2="160" y2="14" stroke="currentColor" stroke-width="4"/>')
    o.append(T(172, 20, "Gương quét"))
    o.append(f'<line x1="150" y1="25" x2="150" y2="144" stroke="{R}" stroke-width="2.4"/>')
    o.append(chevron(150, 140, 0, 1, R, 2.2, 9))
    # buồng chế tạo: bột + chi tiết
    o.append(f'<rect x="70" y="150" width="160" height="84" {PWD}/>')
    o.append(f'<path d="M70,150 V234 H230 V150" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(f'<rect x="124" y="176" width="52" height="58" {SOLID}/>')
    o.append(f'<rect x="124" y="170" width="52" height="6" fill="{R}" fill-opacity="0.75"/>')
    o.append(f'<line x1="70" y1="234" x2="230" y2="234" stroke="currentColor" stroke-width="5"/>')
    o.append(T(76, 250, "bàn chế tạo", size=12))
    o.append(ar(96, 190, 96, 224, B, 2.2, 9))
    o.append(T(14, 200, "hạ 1", size=12, c=B, w="700")); o.append(T(14, 215, "lớp", size=12, c=B, w="700"))
    # cấp bột + lưỡi gạt
    o.append(rect(250, 160, 60, 74, PWD.replace("stroke=\"none\"", "stroke=\"currentColor\" stroke-width=\"1.6\"")))
    o.append(T(280, 205, "bột", a="middle", c=O, w="700"))
    o.append(f'<rect x="238" y="140" width="8" height="12" fill="currentColor"/>')
    o.append(ar(262, 146, 212, 146, B, 2.2, 9))
    o.append(T(266, 138, "lưỡi gạt trải bột", size=12, c=B))
    o.append(T(182, 207, "chi tiết", size=12, a="start"))
    o.append(T(330, 190, "bột đỡ chi tiết,", size=12)); o.append(T(330, 205, "phần nhô ra", size=12)); o.append(T(330, 220, "cần chống đỡ", size=12))
    return fig(svg(262, "Sơ đồ LPBF nung chảy lớp bột", o),
               "Hình 1. LPBF. Laser (đỏ) quét theo lát cắt, nung chảy lớp bột (cam nhạt) thành lớp đặc (cam đậm); bàn hạ một lớp rồi lưỡi gạt trải lớp mới.")


def fig2():
    o = []
    o.append(f'<polygon points="122,12 178,12 160,84 140,84" {PART}/>')
    o.append(T(190, 30, "Đầu phun: laser + bột"))
    o.append(f'<line x1="150" y1="12" x2="150" y2="112" stroke="{R}" stroke-width="2.4"/>')
    for x0 in (124, 176):
        o.append(f'<line x1="{x0}" y1="62" x2="150" y2="112" stroke="{O}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    o.append(T(14, 60, "bột (cam)", c=O, size=12, w="700"))
    o.append(f'<ellipse cx="150" cy="114" rx="26" ry="7" fill="{R}" fill-opacity="0.8"/>')
    o.append(T(190, 108, "vũng chảy", c=R, w="700"))
    o.append(f'<rect x="94" y="122" width="112" height="14" {SOLID}/>')
    o.append(T(214, 132, "lớp đã đắp", size=12))
    o.append(rect(50, 136, 300, 30, WP))
    o.append(T(60, 156, "nền: phôi hoặc chi tiết cần sửa", size=12))
    o.append(ar(236, 74, 300, 74, B, 2.2, 9))
    o.append(T(236, 64, "đầu di chuyển", size=12, c=B, w="700"))
    return fig(svg(180, "Sơ đồ đắp năng lượng định hướng DED", o),
               "Hình 2. DED. Bột (hoặc dây) và tia laser đến cùng một điểm; vũng chảy đông lại thành vệt đắp ngay trên nền.")


def box(x, y, w, h, title, sub):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" {PART}/>'
            + T(x + w / 2, y + 22, title, a="middle", w="700", size=13)
            + T(x + w / 2, y + 40, sub, a="middle", size=11.5))


def fig3():
    o = []
    steps = (("1. In gần hình (LPBF)", "hình khó, kênh cong"), ("2. Giảm ứng suất", "xử lý nhiệt trong lò"),
             ("3. Cắt khỏi bàn", "thường bằng cắt dây"), ("4. Phay, mài tinh", "mặt lắp ghép, lượng dư"),
             ("5. Kiểm tra", "kích thước, kênh thông"))
    y = 10
    for i, (t, s) in enumerate(steps):
        o.append(box(70, y, 280, 50, t, s))
        if i < len(steps) - 1:
            o.append(ar(210, y + 50, 210, y + 66, B, 2.2, 8))
        y += 66
    return fig(svg(332, "Chuỗi công nghệ lai: in gần hình rồi gia công tinh", o),
               "Hình 3. Chuỗi lai điển hình cho chi tiết có hình khó và mặt chính xác. Mỗi công nghệ làm phần nó giỏi nhất.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2), ("<!--FIG3-->", fig3)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
