#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 10 (Gia công ren), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Hình vẽ minh hoạ, không theo tỉ lệ. Chữ ≥ 12 trong viewBox 420 (đọc được ở 375px).
"""
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, BLUE, GREEN, ORANGE = "#dc2626", "#0284c7", "#059669", "#ea580c"
METAL = 'fill="#94a3b8" fill-opacity="0.28"'


def T(x, y, s, size=13, anchor="start", w="400", c="currentColor"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2):
    """Mũi tên thẳng, đầu chữ V 30°."""
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=10)


def Rot(cx, cy, rx, ry, t0, t1, c=RED, w=2.2):
    """Cung elip (độ, y hướng xuống) từ t0 tới t1 + đầu V ở t1: chiều quay."""
    n = 30
    pts = [(cx + rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)),
            cy + ry * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"/>' + chevron(xb, yb, xb - xa, yb - ya, c, w, L=9)


def P(pts, extra='fill="none" stroke="currentColor" stroke-width="2"'):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {extra}/>'


def PL(pts, c="currentColor", w=2):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


# Hình 1: các thông số của ren ngoài (nửa trên, cắt qua trục)
def fig_thong_so():
    o = []
    Pp, yc = 70, 80
    H = Pp * math.sqrt(3) / 2          # tam giác cơ sở 60°
    yr = yc + H
    y2 = (yc + yr) / 2
    roots = [130 + Pp * i for i in range(4)]          # 130 200 270 340
    pts = []
    for r in roots:
        pts += [(r, yr), (r + Pp / 2, yc)]
    pts.append((405, yc + H * 30 / 35))
    body = pts + [(405, 200), (130, 200)]
    o.append(P(body, METAL + ' stroke="none"'))
    o.append(PL(pts, w=2.2))
    o.append(Ln(130, yr, 130, 200, w=1.2))
    # trục ren
    o.append(Ln(110, 215, 410, 215, w=1.2, dash="14 4 3 4"))
    o.append(T(12, 219, "trục ren", 12))
    # ba đường kính (vẽ mức bán kính), nhãn bên trái
    o.append(Ln(112, yc, 410, yc, w=1, dash="4 4"))
    o.append(Ln(112, y2, 410, y2, BLUE, 1.6, "6 4"))
    o.append(Ln(112, yr, 410, yr, w=1, dash="4 4"))
    o.append(T(12, yc + 4, "d ngoài", 13, w="700"))
    o.append(T(12, y2 + 4, "d₂ trung bình", 13, w="700", c=BLUE))
    o.append(T(12, yr + 4, "d₁ trong", 13, w="700"))
    # bước ren P giữa hai đỉnh 235 và 305
    for x in (235, 305):
        o.append(Ln(x, yc - 4, x, 46, w=1))
    o.append(Ln(237, 54, 303, 54, w=1.4))
    o.append(chevron(237, 54, -1, 0, "currentColor", 1.4, L=8))
    o.append(chevron(303, 54, 1, 0, "currentColor", 1.4, L=8))
    o.append(T(270, 46, "P", 14, "middle", "700"))
    # góc prôfin α ở đáy x = 270
    r = 24
    a0, a1 = math.radians(-120), math.radians(-60)
    o.append(f'<path d="M{270 + r * math.cos(a0):.1f},{yr + r * math.sin(a0):.1f} A{r},{r} 0 0 1 '
             f'{270 + r * math.cos(a1):.1f},{yr + r * math.sin(a1):.1f}" fill="none" stroke="{RED}" stroke-width="1.8"/>')
    o.append(T(270, 100, "α", 14, "middle", "700", RED))
    # chú giải, mỗi ý một dòng
    o.append(T(12, 242, "P: bước ren, đo song song với trục", 12))
    o.append(T(12, 260, "α: góc prôfin, ren hệ mét α = 60°", 12, c=RED))
    return fig(svg(270, "Các thông số của ren", o),
               "Hình 1. Các thông số của ren ngoài, vẽ nửa trên mặt cắt qua trục. "
               "d, d₂, d₁ là đường kính, đo qua trục (hình chỉ vẽ tới mức bán kính).")


# Hình 2: ba biên dạng ren
def fig_bien_dang():
    o = []
    names = [("Tam giác", "góc 60°", "bắt chặt"), ("Vuông", "răng vuông", "truyền động"),
             ("Thang", "góc 30°", "truyền động")]
    for i, (n1, n2, n3) in enumerate(names):
        x0 = 10 + i * 140
        if i == 0:
            prof = [(x0, 110), (x0 + 30, 58), (x0 + 60, 110), (x0 + 90, 58), (x0 + 120, 110)]
        elif i == 1:
            prof = [(x0, 110), (x0, 70), (x0 + 30, 70), (x0 + 30, 110), (x0 + 60, 110), (x0 + 60, 70),
                    (x0 + 90, 70), (x0 + 90, 110), (x0 + 120, 110)]
        else:
            dx = 40 * math.tan(math.radians(15))
            prof = []
            for k in (0, 60):
                prof += [(x0 + k + 8, 110), (x0 + k + 8 + dx, 70), (x0 + k + 52 - dx, 70), (x0 + k + 52, 110)]
            prof = [(x0, 110)] + prof + [(x0 + 120, 110)]
        o.append(P(prof + [(x0 + 120, 130), (x0, 130)], METAL + ' stroke="none"'))
        o.append(PL(prof, w=2.2))
        xc = x0 + 60
        o.append(T(xc, 152, n1, 14, "middle", "700"))
        o.append(T(xc, 171, n2, 13, "middle"))
        o.append(T(xc, 190, n3, 13, "middle", c=BLUE))
    return fig(svg(200, "Ba biên dạng ren", o),
               "Hình 2. Ba biên dạng ren thường gặp. Dòng xanh là công dụng chính.")


# Hình 3: ba cách tiến dao khi tiện ren tam giác
def fig_tien_dao():
    o = []
    t30 = math.tan(math.radians(30))
    specs = [("a) Hướng kính", "2 lưỡi cùng cắt", "→ dùng cắt tinh"),
             ("b) Hướng xiên", "1 lưỡi cắt", "→ dùng cắt thô"),
             ("c) Phối hợp", "lưỡi phụ cắt ít", "→ hay dùng nhất")]
    for i, (a, b, c) in enumerate(specs):
        x0 = i * 140
        xc = x0 + 70
        hw = 60 * t30                                  # nửa bề rộng rãnh ở mặt phôi
        o.append(P([(x0 + 6, 60), (xc - hw, 60), (xc, 120), (xc + hw, 60), (x0 + 134, 60),
                    (x0 + 134, 125), (x0 + 6, 125)], METAL + ' stroke="currentColor" stroke-width="1.4"'))
        if i == 0:
            ax = xc
        elif i == 1:
            ax = xc - 20 * t30                         # mũi dao nằm trên đường sườn trái
        else:
            ax = xc - 20 * t30 + 4                     # lệch khỏi sườn trái một ít
        ay = 100
        hb = 35 * t30
        o.append(P([(ax, ay), (ax + hb, ay - 35), (ax + hb, 22), (ax - hb, 22), (ax - hb, ay - 35)],
                   'fill="#64748b" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"'))
        left_c = RED if i == 0 else (ORANGE if i == 2 else "currentColor")
        o.append(Ln(ax, ay, ax - hb, ay - 35, left_c, 3 if left_c != "currentColor" else 1.4))
        o.append(Ln(ax, ay, ax + hb, ay - 35, RED, 3))
        if i == 0:
            o.append(Ar(ax + 36, 26, ax + 36, 60))
        else:
            s, cth = math.sin(math.radians(30)), math.cos(math.radians(30))
            x1, y1 = xc - 64, 20
            o.append(Ar(x1, y1, x1 + 34 * s, y1 + 34 * cth))
        o.append(T(xc, 148, a, 13, "middle", "700"))
        o.append(T(xc, 166, b, 13, "middle"))
        o.append(T(xc, 184, c, 13, "middle", c=BLUE))
    o.append(Ln(12, 202, 34, 202, RED, 3))
    o.append(T(40, 206, "lưỡi đang cắt", 12))
    o.append(Ln(150, 202, 172, 202, ORANGE, 3))
    o.append(T(178, 206, "lưỡi cắt ít", 12))
    o.append(Ar(276, 192, 276, 210, RED, 2))
    o.append(T(286, 206, "hướng tiến dao", 12))
    return fig(svg(216, "Ba cách tiến dao khi tiện ren tam giác", o),
               "Hình 3. Ba cách tiến dao khi tiện ren tam giác (mũi tên đỏ: hướng ăn sâu sau mỗi lần chạy dao).")


# Hình 4: tarô (ren trong) và bàn ren (ren ngoài)
def zig(x, y0, y1, step, amp):
    pts, k, y = [], 0, y0
    while y <= y1 + 0.1:
        pts.append((x + (amp if k % 2 else 0), y))
        y += step / 2
        k += 1
    return pts


def fig_taro_ban_ren():
    o = []
    # --- a) tarô
    o.append(T(105, 16, "a) Tarô: ren trong", 13, "middle", "700"))
    o.append(P([(20, 80), (78, 80), (78, 190), (20, 190)], METAL + ' stroke="none"'))
    o.append(P([(132, 80), (190, 80), (190, 190), (132, 190)], METAL + ' stroke="none"'))
    o.append(PL([(20, 80), (78, 80)] + zig(78, 80, 140, 10, -7) + [(78, 190)], w=1.6))
    o.append(PL([(190, 80), (132, 80)] + zig(132, 80, 140, 10, 7) + [(132, 190)], w=1.6))
    # thân tarô
    o.append(P([(91, 30), (119, 30), (119, 136), (112, 146), (98, 146), (91, 136)],
               'fill="#64748b" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"'))
    for y in range(86, 140, 10):
        o.append(Ln(91, y, 119, y - 6, w=1))
    o.append(Rot(105, 44, 26, 8, 20, 160))
    o.append(Ar(150, 34, 150, 68))
    o.append(T(158, 52, "tiến", 12))
    # chú thích
    o.append(Ln(132, 170, 150, 205, w=1))
    o.append(T(60, 220, "lỗ khoan mồi:", 12, "middle"))
    o.append(T(60, 236, "lớn hơn d₁ một ít", 12, "middle"))
    o.append(T(160, 220, "phần chưa", 12, "middle"))
    o.append(T(160, 236, "có ren", 12, "middle"))
    o.append(Ln(78, 175, 66, 206, w=1))
    # --- b) bàn ren
    o.append(T(315, 16, "b) Bàn ren: ren ngoài", 13, "middle", "700"))
    o.append(P([(300, 28), (330, 28), (330, 200), (300, 200)], METAL + ' stroke="currentColor" stroke-width="1.4"'))
    for y in range(140, 200, 9):
        o.append(Ln(300, y, 330, y - 6, w=1))
    o.append(P([(250, 112), (296, 112), (296, 136), (250, 136)],
               'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'))
    o.append(P([(334, 112), (380, 112), (380, 136), (334, 136)],
               'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'))
    o.append(Rot(315, 100, 62, 10, 200, 340))
    o.append(Ar(392, 128, 392, 92))
    o.append(T(386, 82, "tiến", 12, "end"))
    o.append(T(252, 152, "bàn ren", 12, "end"))
    o.append(T(238, 182, "đã có ren", 12, "middle"))
    o.append(Ln(270, 178, 298, 172, w=1))
    o.append(T(315, 220, "Ø trục tiện nhỏ hơn d", 12, "middle"))
    o.append(T(315, 236, "khoảng 0,1 ÷ 0,2 mm", 12, "middle"))
    return fig(svg(244, "Cắt ren bằng tarô và bàn ren", o),
               "Hình 4. Tarô cắt ren trong, bàn ren cắt ren ngoài. Cắt xong phải quay ngược để rút dụng cụ ra.")


# Hình 5: cán ren bằng bàn cán
def fig_can_ren():
    o = []
    o.append(T(30, 22, "Bàn cán di động (đi lại)", 13, w="700"))
    o.append(Ar(300, 18, 372, 18))
    o.append(P([(30, 36), (390, 36), (390, 72), (30, 72)], 'fill="#64748b" fill-opacity="0.35" stroke="currentColor" stroke-width="1.5"'))
    o.append(P([(30, 124), (390, 124), (390, 160), (30, 160)], 'fill="#64748b" fill-opacity="0.35" stroke="currentColor" stroke-width="1.5"'))
    for x in range(40, 384, 16):
        o.append(Ln(x, 72, x + 10, 36, w=1))
        o.append(Ln(x + 8, 160, x + 18, 124, w=1))
    o.append(f'<circle cx="120" cy="98" r="26" {METAL} stroke="currentColor" stroke-width="2"/>')
    o.append(Rot(120, 98, 14, 14, 200, 470))
    o.append(T(160, 95, "phôi lăn giữa hai bàn,", 13))
    o.append(T(160, 113, "bị ép thành ren, không có phoi", 13, c=GREEN))
    o.append(T(30, 182, "Bàn cán cố định", 13, w="700"))
    o.append(T(30, 202, "Rãnh nghiêng một góc bằng góc xoắn của ren;", 12))
    o.append(T(30, 220, "ren trên hai bàn lệch nhau nửa bước.", 12))
    return fig(svg(228, "Cán ren bằng bàn cán", o),
               "Hình 5. Cán ren bằng bàn cán. Bàn trên đi hết hành trình thì phôi có ren.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig_thong_so), ("<!--FIG2-->", fig_bien_dang), ("<!--FIG3-->", fig_tien_dao),
               ("<!--FIG4-->", fig_taro_ban_ren), ("<!--FIG5-->", fig_can_ren)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
