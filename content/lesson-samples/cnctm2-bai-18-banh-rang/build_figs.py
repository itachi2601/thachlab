#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 2 – Bài 18 (Công nghệ gia công chi tiết bánh răng),
thay <!--FIGn--> và __PHUT__ trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Hình vẽ minh hoạ, không theo tỉ lệ. Chữ ≥ 12 trong viewBox 420 (đọc được ở 375px).
Màu: xám = thân bánh răng; đỏ = vành răng / mặt vừa gia công; xanh dương = chuẩn định vị;
đỏ đậm mũi tên W = lực kẹp; cam = nhiệt luyện; xanh lá = giai đoạn tinh.
"""
import math
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, BLUE, GREEN, ORANGE, PURPLE = "#dc2626", "#0369a1", "#047857", "#ea580c", "#7c3aed"
WORK = 'fill="#94a3b8" fill-opacity="0.30" stroke="currentColor" stroke-width="1.5"'
TEETH = f'fill="{RED}" fill-opacity="0.22" stroke="currentColor" stroke-width="1.5"'
TOOL = 'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'
MANDREL = f'fill="{BLUE}" fill-opacity="0.16" stroke="{BLUE}" stroke-width="1.4"'


def T(x, y, s, size=13, anchor="start", w="400", c="currentColor"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2, L=10):
    """Mũi tên thẳng, đầu chữ V 30°."""
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=L)


def Dim(x1, y1, x2, y2, label, lx, ly, c=PURPLE, anchor="middle"):
    """Đường kích thước hai đầu mũi tên + nhãn."""
    return (Ln(x1, y1, x2, y2, c, 1.2) + chevron(x2, y2, x2 - x1, y2 - y1, c, 1.2, L=7)
            + chevron(x1, y1, x1 - x2, y1 - y2, c, 1.2, L=7) + T(lx, ly, label, 13, anchor, "700", c))


def R(x, y, w, h, extra=WORK):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {extra}/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def Loc(x, y, direction, n, c=BLUE, side=1):
    """Ký hiệu định vị: tam giác đặc, đỉnh chạm mặt chuẩn tại (x, y); direction = hướng từ đế tới đỉnh
    ('right','left','up','down'); kèm số bậc tự do n đặt cạnh đế."""
    s = 9
    if direction == "right":
        pts = [(x, y), (x - 2 * s, y - s), (x - 2 * s, y + s)]
        lab = (x - 2 * s - 5, y + 5, "end")
    elif direction == "left":
        pts = [(x, y), (x + 2 * s, y - s), (x + 2 * s, y + s)]
        lab = (x + 2 * s + 5, y + 5, "start")
    elif direction == "up":
        pts = [(x, y), (x - s, y + 2 * s), (x + s, y + 2 * s)]
        lab = (x + s + 4 if side > 0 else x - s - 4, y + 2 * s - 4, "start" if side > 0 else "end")
    else:
        pts = [(x, y), (x - s, y - 2 * s), (x + s, y - 2 * s)]
        lab = (x + s + 4 if side > 0 else x - s - 4, y - 2 * s + 10, "start" if side > 0 else "end")
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return f'<polygon points="{p}" fill="{c}"/>' + T(lab[0], lab[1], str(n), 14, lab[2], "700", c)


def mirror_poly(pts, x0, y0, extra):
    """pts = (u, r) nửa trên mặt cắt (u dọc trục, r bán kính). Vẽ nửa trên và nửa dưới đối xứng qua trục y0."""
    up = " ".join(f"{x0 + u:.1f},{y0 - r:.1f}" for u, r in pts)
    dn = " ".join(f"{x0 + u:.1f},{y0 + r:.1f}" for u, r in pts)
    return f'<polygon points="{up}" {extra}/><polygon points="{dn}" {extra}/>'


def ring(x0, y0, u0, u1, r0, r1, extra):
    """Vành (u0..u1, r0..r1) đối xứng qua trục."""
    return mirror_poly([(u0, r0), (u1, r0), (u1, r1), (u0, r1)], x0, y0, extra)


# ---------- Hình 1: các loại bánh răng trụ theo công nghệ
def fig_loai():
    o = []
    rt = 7  # chiều cao vùng răng (đỏ)

    def gear(x0, y0, parts, rim):
        """parts: các vành thân (u0,u1,r0,r1); rim: danh sách vành răng (u0,u1,r_đỉnh)."""
        out = []
        for u0, u1, r0, r1 in parts:
            out.append(ring(x0, y0, u0, u1, r0, r1, WORK))
        for u0, u1, ra in rim:
            out.append(ring(x0, y0, u0, u1, ra - rt, ra, TEETH))
        return out

    # I. Một bậc có mayơ (l/d > 1) — ô trái trên
    x0, y0 = 40, 70
    o += gear(x0, y0, [(0, 60, 13, 24), (34, 60, 24, 40)], [(34, 60, 47)])
    o.append(Ln(x0 - 4, y0, x0 + 74, y0, w=1, dash="8 3 2 3"))
    o.append(Dim(x0, 136, x0 + 60, 136, "l", x0 + 30, 152))
    o.append(Ln(x0, y0 + 24, x0, 140, PURPLE, 0.8, "2 2"))
    o.append(Ln(x0 + 60, y0 + 47, x0 + 60, 140, PURPLE, 0.8, "2 2"))
    o.append(Dim(x0 - 10, y0 - 13, x0 - 10, y0 + 13, "d", x0 - 14, y0 + 5, anchor="end"))
    o.append(T(x0 + 30, 174, "I. Có mayơ", 13, "middle", "700"))
    o.append(T(x0 + 30, 190, "l/d &gt; 1", 12, "middle", c=PURPLE))

    # II. Nhiều bậc — ô giữa trên
    x0 = 168
    o += gear(x0, y0, [(0, 64, 12, 22), (0, 22, 22, 37), (34, 64, 22, 27)], [(0, 22, 44), (34, 64, 34)])
    o.append(Ln(x0 - 8, y0, x0 + 72, y0, w=1, dash="8 3 2 3"))
    o.append(T(x0 + 32, 174, "II. Nhiều bậc", 13, "middle", "700"))
    o.append(T(x0 + 32, 190, "l/d &gt; 1", 12, "middle", c=PURPLE))

    # III. Dạng đĩa (l/d < 1) — ô phải trên
    x0 = 320
    o += gear(x0, y0, [(0, 20, 14, 43)], [(0, 20, 50)])
    o.append(Ln(x0 - 14, y0, x0 + 27, y0, w=1, dash="8 3 2 3"))
    o.append(Dim(x0, 136, x0 + 20, 136, "l", x0 + 10, 152))
    o.append(Ln(x0, y0 + 50, x0, 140, PURPLE, 0.8, "2 2"))
    o.append(Ln(x0 + 20, y0 + 50, x0 + 20, 140, PURPLE, 0.8, "2 2"))
    o.append(Dim(x0 + 34, y0 - 14, x0 + 34, y0 + 14, "d", x0 + 40, y0 + 5, anchor="start"))
    o.append(T(x0 + 10, 174, "III. Dạng đĩa", 13, "middle", "700"))
    o.append(T(x0 + 10, 190, "l/d &lt; 1", 12, "middle", c=PURPLE))

    # IV. Dạng vành — hàng dưới trái
    x0, y0 = 70, 270
    o += gear(x0, y0, [(0, 26, 12, 20), (9, 17, 20, 36), (0, 26, 36, 43)], [(0, 26, 50)])
    o.append(Ln(x0 - 14, y0, x0 + 40, y0, w=1, dash="8 3 2 3"))
    o.append(T(x0 + 13, 342, "IV. Dạng vành", 13, "middle", "700"))
    o.append(T(x0 + 13, 358, "l/d &lt; 1", 12, "middle", c=PURPLE))

    # V. Trục răng — hàng dưới phải (không có lỗ)
    x0 = 200
    o.append(mirror_poly([(0, 0), (0, 10), (60, 10), (60, 0)], x0, y0, WORK))
    o.append(mirror_poly([(92, 0), (92, 10), (180, 10), (180, 0)], x0, y0, WORK))
    o.append(ring(x0, y0, 60, 92, 0, 23, WORK))
    o.append(ring(x0, y0, 60, 92, 23, 30, TEETH))
    o.append(Ln(x0 - 10, y0, x0 + 190, y0, w=1, dash="8 3 2 3"))
    o.append(T(x0 + 90, 342, "V. Trục răng", 13, "middle", "700"))
    o.append(T(x0 + 90, 358, "không có lỗ, gá lỗ tâm", 12, "middle", c=BLUE))
    return fig(svg(366, "Năm loại bánh răng trụ theo đặc tính công nghệ, mặt cắt dọc trục", o),
               "Hình 1. Năm loại bánh răng trụ (mặt cắt dọc trục). Vùng đỏ: vành răng. l: chiều dài lỗ, d: đường kính lỗ.")


# ---------- Hình 2: yêu cầu vị trí tương quan
def fig_yeu_cau():
    o = []
    x0, y0 = 130, 130
    # bánh răng có mayơ, mặt cắt
    o.append(ring(x0, y0, 0, 90, 26, 42, WORK))
    o.append(ring(x0, y0, 50, 90, 42, 80, WORK))
    o.append(ring(x0, y0, 50, 90, 80, 94, TEETH))
    o.append(Ln(x0 - 30, y0, x0 + 140, y0, w=1, dash="8 3 2 3"))
    o.append(T(x0 - 30, y0 - 12, "tâm lỗ", 12))
    # đường tròn cơ sở (nét chấm gạch trong vành răng)
    rb = 84
    o.append(Ln(x0 + 50, y0 - rb, x0 + 90, y0 - rb, GREEN, 1.4, "5 3"))
    o.append(Ln(x0 + 50, y0 + rb, x0 + 90, y0 + rb, GREEN, 1.4, "5 3"))
    # nhãn đồng tâm (phải trên)
    o.append(Ln(x0 + 86, y0 - rb, 262, 38, GREEN, 1))
    o.append(T(264, 26, "Đồng tâm lỗ – đường", 12, c=GREEN, w="700"))
    o.append(T(264, 42, "tròn cơ sở: 0,05 ÷ 0,1", 12, c=GREEN, w="700"))
    # mặt đầu phải: vuông góc
    o.append(Ln(x0 + 90, y0 - 94, x0 + 90, y0 - 26, BLUE, 3))
    o.append(Ln(x0 + 93, y0 - 60, 262, 84, BLUE, 1))
    o.append(T(264, 80, "Mặt đầu ⊥ tâm lỗ:", 12, c=BLUE, w="700"))
    o.append(T(264, 96, "0,01 ÷ 0,015", 12, c=BLUE, w="700"))
    o.append(T(264, 112, "trên 100 mm bán kính", 12, c=BLUE))
    # lỗ
    o.append(Ln(x0 + 30, y0 + 26, 262, 168, PURPLE, 1))
    o.append(T(264, 164, "Lỗ: cấp 6, 7", 12, c=PURPLE, w="700"))
    o.append(T(264, 180, "(lỗ Ø56 cấp 7: 0,030 mm)", 12, c=PURPLE))
    # răng
    o.append(Ln(x0 + 70, y0 + 92, 262, 222, RED, 1))
    o.append(T(264, 218, "Răng: 40 ÷ 45 HRC", 12, c=RED, w="700"))
    o.append(T(264, 234, "Ra 1,25 ÷ 0,63 µm", 12, c=RED))
    return fig(svg(246, "Yêu cầu vị trí tương quan và bề mặt của bánh răng", o),
               "Hình 2. Bốn con số cần nhớ trên một bánh răng có mayơ (mặt cắt). Nét xanh lá đứt: đường tròn cơ sở; nét xanh dương đậm: mặt đầu.")


# ---------- Hình 3: chuẩn định vị theo l/d
def fig_chuan():
    o = []
    # a) l/d > 1 trên trục gá
    x0, y0 = 50, 120
    l, rh, rhub, rrim = 92, 20, 36, 70
    o.append(R(x0 - 26, y0 - rh, 160, 2 * rh, MANDREL))                 # trục gá
    o.append(ring(x0, y0, 0, l, rh, rhub, WORK))
    o.append(ring(x0, y0, 52, l, rhub, rrim - 10, WORK))
    o.append(ring(x0, y0, 52, l, rrim - 10, rrim, TEETH))
    o.append(Ln(x0 - 34, y0, x0 + 142, y0, w=1, dash="8 3 2 3"))
    # định vị: lỗ 4 bậc (tam giác từ trong lỗ chạm thành lỗ), mặt đầu 1 bậc
    o.append(Loc(x0 + 28, y0 - rh, "up", 4, side=1))
    o.append(R(x0 - 12, y0 - rhub, 12, 2 * rhub, MANDREL))                # vai chặn trên trục gá
    o.append(Loc(x0 - 12, y0 + 30, "right", 1))
    # kẹp W ở mặt đầu phải, đầu mũi cách mặt 8 px
    o.append(Ar(x0 + l + 40, y0 - 50, x0 + l + 8, y0 - 50))
    o.append(T(x0 + l + 26, y0 - 58, "W", 13, "middle", "700", RED))
    o.append(T(100, 222, "a) l/d &gt; 1: lỗ 4 bậc,", 13, "middle", "700"))
    o.append(T(100, 240, "mặt đầu 1 bậc", 13, "middle", "700"))
    o.append(T(100, 258, "(trục gá dài)", 12, "middle", c=BLUE))

    # b) l/d < 1: tấm tì + chốt ngắn
    x0 = 300
    l, rh, rrim = 26, 26, 70
    o.append(R(x0 - 12, y0 - 82, 12, 164, MANDREL))                      # tấm tì mặt đầu
    o.append(R(x0 - 26, y0 - rh, 44, 2 * rh, MANDREL))                   # chốt ngắn
    o.append(ring(x0, y0, 0, l, rh, rrim - 10, WORK))
    o.append(ring(x0, y0, 0, l, rrim - 10, rrim, TEETH))
    o.append(Ln(x0 - 24, y0, x0 + l + 50, y0, w=1, dash="8 3 2 3"))
    # bố trí số bậc: mặt đầu 3 (ba tam giác chỉ đại diện bằng một ký hiệu + số), lỗ 2
    o.append(Loc(x0 - 12, y0 - 48, "right", 3))
    o.append(Loc(x0 + 9, y0 - rh, "up", 2, side=1))
    o.append(Ar(x0 + l + 44, y0 - 40, x0 + l + 8, y0 - 40))
    o.append(T(x0 + l + 26, y0 - 48, "W", 13, "middle", "700", RED))
    o.append(T(316, 222, "b) l/d &lt; 1: mặt đầu", 13, "middle", "700"))
    o.append(T(316, 240, "3 bậc, lỗ 2 bậc", 13, "middle", "700"))
    o.append(T(316, 258, "(tấm tì + chốt ngắn)", 12, "middle", c=BLUE))
    return fig(svg(268, "Chuẩn định vị bánh răng theo tỉ số l trên d", o),
               "Hình 3. Tam giác xanh: điểm định vị, số bên cạnh là số bậc tự do khử. Mũi tên W: lực kẹp. Mặt cắt dọc trục, không theo tỉ lệ.")


# ---------- Hình 4: ba giai đoạn của quy trình
def fig_giai_doan():
    o = []
    rows = [
        ("1. Chuẩn", BLUE, ["Lỗ + mặt đầu (một lần gá)", "Then hoa · mặt ngoài"]),
        ("2. Răng", RED, ["Phay / xọc thô, tinh", "Vê đầu răng · cà răng"]),
        ("Nhiệt luyện", ORANGE, ["Tôi bề mặt răng"]),
        ("3. Tinh", GREEN, ["Sửa lỗ · mài mặt đầu", "Mài nghiền / mài răng"]),
        ("Kiểm tra", "currentColor", ["Kích thước · vị trí · ăn khớp"]),
    ]
    y = 12
    xs, w = 12, 300
    for i, (name, c, lines) in enumerate(rows):
        h = 28 + 18 * len(lines)
        fill = f'fill="{c}" fill-opacity="0.10"' if c != "currentColor" else 'fill="none"'
        o.append(f'<rect x="{xs}" y="{y}" width="{w}" height="{h}" rx="8" {fill} stroke="{c}" stroke-width="1.8"/>')
        o.append(T(xs + 12, y + 19, name, 14, w="700", c=c))
        for k, s in enumerate(lines):
            o.append(T(xs + 12, y + 37 + 18 * k, s, 13))
        if i < len(rows) - 1:
            o.append(Ar(xs + w / 2, y + h + 2, xs + w / 2, y + h + 16, "currentColor", 1.8, L=8))
        y += h + 20
    # cột chuẩn bên phải
    top, bot = 12 + 64 + 20, y - 20 - 46 - 20
    o.append(Ln(336, top, 336, bot, BLUE, 3))
    o.append(Ln(330, top, 336, top, BLUE, 2) + Ln(330, bot, 336, bot, BLUE, 2))
    for k, s in enumerate(["Gá theo", "lỗ +", "mặt đầu"]):
        o.append(T(346, (top + bot) / 2 - 14 + 17 * k, s, 13, w="700", c=BLUE))
    return fig(svg(y - 4, "Sơ đồ ba giai đoạn chế tạo bánh răng trụ", o),
               "Hình 4. Ba giai đoạn: Chuẩn – Răng – Tinh. Từ khi có lỗ và mặt đầu, các nguyên công sau đều gá theo chúng (trừ lúc mài lỗ sau tôi: gá theo vành răng).")


# ---------- Hình 5: hai lần gá dùng trục gá
def fig_truc_ga():
    o = []
    y0 = 110
    # a) lần 1: kẹp mâm cặp mặt ngoài phôi, gia công lỗ + mặt đầu phải
    x0 = 40
    l, rh, ro = 70, 20, 54
    o.append(R(x0 - 22, y0 - 80, 14, 160, TOOL))                          # mâm cặp
    o.append(R(x0 - 8, y0 - ro - 14, 30, 14, TOOL))                       # chấu trên
    o.append(R(x0 - 8, y0 + ro, 30, 14, TOOL))                            # chấu dưới
    o.append(ring(x0, y0, 0, l, rh, ro, WORK))
    o.append(Ln(x0 + l, y0 - ro, x0 + l, y0 - rh, RED, 3.2))
    o.append(Ln(x0 + l, y0 + rh, x0 + l, y0 + ro, RED, 3.2))
    o.append(Ln(x0, y0 - rh, x0 + l, y0 - rh, RED, 3.2))
    o.append(Ln(x0, y0 + rh, x0 + l, y0 + rh, RED, 3.2))
    o.append(Ln(x0 - 30, y0, x0 + l + 70, y0, w=1, dash="8 3 2 3"))
    # dao tiện lỗ: cán nằm trên trục, mũi chạm thành lỗ trên
    o.append(R(x0 + 40, y0 - 6, 104, 12, TOOL))
    o.append(f'<polygon points="{x0 + 40},{y0 - 6} {x0 + 52},{y0 - 6} {x0 + 44},{y0 - rh + 1}" {TOOL}/>')
    o.append(T(100, 214, "a) Lần 1: kẹp mặt ngoài,", 13, "middle", "700"))
    o.append(T(100, 232, "làm lỗ + một mặt đầu", 13, "middle", "700"))

    # b) lần 2: lắp trục gá, chống tâm, tiện mặt ngoài + mặt đầu còn lại
    x0 = 268
    o.append(R(x0 - 30, y0 - rh, l + 60, 2 * rh, MANDREL))
    o.append(f'<polygon points="{x0 - 30},{y0} {x0 - 46},{y0 - 10} {x0 - 46},{y0 + 10}" {TOOL}/>')
    o.append(f'<polygon points="{x0 + l + 30},{y0} {x0 + l + 46},{y0 - 10} {x0 + l + 46},{y0 + 10}" {TOOL}/>')
    o.append(ring(x0, y0, 0, l, rh, ro, WORK))
    o.append(Ln(x0, y0 - ro, x0 + l, y0 - ro, RED, 3.2))
    o.append(Ln(x0, y0 + ro, x0 + l, y0 + ro, RED, 3.2))
    o.append(Ln(x0, y0 - ro, x0, y0 - rh, RED, 3.2))
    o.append(Ln(x0, y0 + rh, x0, y0 + ro, RED, 3.2))
    o.append(Ln(x0 - 50, y0, x0 + l + 50, y0, w=1, dash="8 3 2 3"))
    o.append(f'<polygon points="{x0 + 40},{y0 - ro - 2} {x0 + 30},{y0 - ro - 26} {x0 + 52},{y0 - ro - 26}" {TOOL}/>')
    o.append(T(x0 + 35, y0 - ro - 32, "dao", 12, "middle"))
    o.append(T(x0 + 35, 186, "trục gá", 12, "middle", c=BLUE))
    o.append(T(318, 214, "b) Lần 2: lên trục gá,", 13, "middle", "700"))
    o.append(T(318, 232, "tiện mặt ngoài + mặt đầu kia", 13, "middle", "700"))
    return fig(svg(242, "Gia công phôi bánh răng hai lần gá dùng trục gá", o),
               "Hình 5. Hai lần gá dùng trục gá. Nét đỏ: mặt gia công ở lần gá đó. Lần 2 lấy lỗ và mặt đầu vừa làm ở lần 1 làm chuẩn.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
h = src
for tag, f in (("<!--FIG1-->", fig_loai), ("<!--FIG2-->", fig_yeu_cau), ("<!--FIG3-->", fig_chuan),
               ("<!--FIG4-->", fig_giai_doan), ("<!--FIG5-->", fig_truc_ga)):
    assert h.count(tag) == 1, tag
    h = h.replace(tag, f())
assert "__" not in h.replace("__PHUT__", "")

tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
if not m:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600])
    sys.exit(1)
phut = round(float(m.group(1).replace(",", ".")))
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")
print("đã ghi theory.html, đọc ~", phut, "phút")
