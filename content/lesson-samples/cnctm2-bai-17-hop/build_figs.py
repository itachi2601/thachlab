#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 2 – Bài 17 (Công nghệ gia công chi tiết dạng hộp),
thay <!--FIGn--> và __PHUT__ trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Mọi hình là sơ đồ nguyên lý tự vẽ, không theo tỉ lệ (trừ Hình 6 vẽ theo tỉ lệ 1,5 px/mm).
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
RED, BLUE, GREEN, ORANGE, GREY = "#dc2626", "#0369a1", "#047857", "#ea580c", "#64748b"
METAL = 'fill="#94a3b8" fill-opacity="0.28" stroke="currentColor" stroke-width="1.5"'
FIX = 'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.3"'


def T(x, y, s, size=13, anchor="start", w="400", c="currentColor"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2, L=10):
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=L)


def Dim(x1, y1, x2, y2, c=BLUE, w=1.4):
    """Đường kích thước hai đầu mũi tên."""
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=8) + chevron(x1, y1, x1 - x2, y1 - y2, c, w, L=8)


def R(x, y, w, h, extra=METAL):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {extra}/>'


def C(cx, cy, r, extra='fill="none" stroke="currentColor" stroke-width="1.5"'):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {extra}/>'


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def dv(x, y, n, c=BLUE, up=True):
    """Ký hiệu định vị: chữ V chạm mặt tại (x, y), chân có gạch nền; kèm số bậc tự do khử."""
    s = 1 if up else -1           # up=True: ký hiệu nằm dưới mặt, đỉnh hướng lên
    o = [f'<polyline points="{x - 16:.1f},{y + s * 13:.1f} {x - 7:.1f},{y + s * 13:.1f} {x:.1f},{y:.1f} '
         f'{x + 7:.1f},{y + s * 13:.1f}" fill="none" stroke="{c}" stroke-width="2"/>']
    o.append(T(x + 11, y + s * 13 + (5 if up else -1), str(n), 13, "start", "700", c))
    return "".join(o)


# Hình 1: hộp liền và hộp rời
def fig_loai_hop():
    o = []
    # a) hộp liền: thân một khối, lỗ trên một thân
    o.append(T(105, 18, "a) Hộp liền", 13, "middle", "700"))
    o.append(R(24, 34, 162, 110))
    for cx, cy, r in ((62, 72, 16), (122, 102, 20), (160, 66, 12)):
        o.append(C(cx, cy, r, f'fill="#ffffff" fill-opacity="0.9" stroke="{BLUE}" stroke-width="2"'))
    o.append(T(105, 166, "lỗ nằm ở một thân", 12, "middle"))
    o.append(T(105, 184, "hộp tốc độ, thân xy-lanh", 12, "middle", c=GREY))
    # b) hộp rời: thân + nắp, lỗ chia đôi ở mặt ghép
    o.append(T(315, 18, "b) Hộp rời", 13, "middle", "700"))
    yj = 88
    o.append(R(234, 40, 162, yj - 40 - 2))           # nắp
    o.append(R(234, yj + 2, 162, 140 - yj - 2))      # thân
    for cx, r in ((280, 20), (352, 15)):
        o.append(C(cx, yj, r, f'fill="#ffffff" fill-opacity="0.9" stroke="{BLUE}" stroke-width="2"'))
    o.append(Ln(222, yj, 408, yj, RED, 2.2, "7 4"))
    o.append(T(316, 62, "nắp", 12, "middle"))
    o.append(T(316, 134, "thân", 12, "middle"))
    o.append(T(315, 166, "lỗ nằm ở hai nửa", 12, "middle"))
    o.append(T(315, 184, "hộp giảm tốc, gối đỡ hai nửa", 12, "middle", c=GREY))
    o.append(T(315, 204, "Nét đỏ đứt: mặt ghép", 12, "middle", c=RED))
    return fig(svg(220, "Hộp liền và hộp rời", o),
               "Hình 1. Hộp liền có hệ lỗ trên một thân; hộp rời có hệ lỗ chia đôi trên hai nửa thân ghép lại.")


# Hình 2: yêu cầu hệ lỗ — mặt cắt ngang hộp, hai hàng lỗ trên hai vách
def fig_yeu_cau():
    o = []
    xl, xr, wv = 70, 300, 18          # vách trái, vách phải, bề dày vách
    ytop, ybot = 40, 196
    rows = ((84, 18, "1"), (150, 13, "2"))
    for x0 in (xl, xr):
        cuts = sorted((y - r, y + r) for y, r, _ in rows)
        y = ytop
        for a, b in cuts:
            o.append(R(x0, y, wv, a - y))
            y = b
        o.append(R(x0, y, wv, ybot - y))
    o.append(R(xl, ytop - 14, xr + wv - xl, 14))                # vách trên
    for x0 in (xl, xr):                                          # mặt lỗ (xanh) trên từng vách
        for y, r, _ in rows:
            o.append(Ln(x0, y - r, x0 + wv, y - r, BLUE, 2.6))
            o.append(Ln(x0, y + r, x0 + wv, y + r, BLUE, 2.6))
    o.append(R(xl, ybot, xr + wv - xl, 16))                     # đáy hộp = mặt chuẩn
    o.append(Ln(xl - 10, ybot + 16, xr + wv + 10, ybot + 16, RED, 3))
    o.append(T(xl + 120, ybot + 32, "mặt chuẩn (đáy)", 12, "middle", c=RED))
    for y, r, name in rows:
        o.append(Ln(xl - 30, y, (378 if name == "1" else 406), y, w=1, dash="10 3 2 3"))
        o.append(T(xl - 36, y + 5, name, 13, "end", "700"))
    o.append(T(xl + wv + 8, 84 - 26, "hàng lỗ 1: đồng tâm hai vách", 12, c=GREEN))
    o.append(T(xl + wv + 8, 150 - 20, "trục 2 song song trục 1", 12))
    # kích thước A giữa hai trục
    xa = 372
    o.append(Dim(xa, 84, xa, 150))
    o.append(T(xa + 8, 122, "A", 14, "start", "700", BLUE))
    # kích thước trục 2 tới mặt chuẩn
    xb = 400
    o.append(Ln(xr + wv + 4, ybot + 16, 406, ybot + 16, BLUE, 1, "3 3"))
    o.append(Dim(xb, 150, xb, ybot + 16))
    o.append(T(xb - 6, ybot - 4, "H", 14, "end", "700", BLUE))
    o.append(T(xl - 6, 60, "vách", 12, "end"))
    o.append(T(xr + wv + 6, 60, "vách", 12))
    return fig(svg(240, "Yêu cầu kỹ thuật của hệ lỗ trong hộp", o),
               "Hình 2. Mặt cắt hộp: hai hàng lỗ trên hai vách. Cần đạt: lỗ trên hai vách đồng tâm, hai trục song song, khoảng cách tâm A và khoảng cách H tới mặt chuẩn đúng dung sai.")


def tram(cx, cy, r, half):
    """Chốt trám nhìn từ trên: đường tròn r bị vạt hai bên theo phương ngang (x = cx ± half)."""
    h = math.sqrt(r * r - half * half)
    return (f'<path d="M{cx - half:.1f},{cy - h:.1f} A{r},{r} 0 0,1 {cx + half:.1f},{cy - h:.1f} L{cx + half:.1f},{cy + h:.1f} '
            f'A{r},{r} 0 0,1 {cx - half:.1f},{cy + h:.1f} Z" fill="{BLUE}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1.4"/>')


# Hình 3: chuẩn một mặt phẳng + hai lỗ
def fig_chuan():
    o = []
    o.append(T(12, 18, "a) Nhìn ngang (cắt qua hai lỗ chuẩn)", 13, "start", "700"))
    x0, x1, yt, yb = 50, 370, 40, 104          # hộp
    xp1, xp2 = 100, 320                        # hai lỗ chuẩn
    o.append(R(x0, yt, x1 - x0, yb - yt, f'fill="{ORANGE}" fill-opacity="0.15" stroke="{ORANGE}" stroke-width="2"'))
    o.append(Ln(x0, yb, x1, yb, RED, 3))         # mặt chuẩn
    plate_y = 140
    o.append(R(30, plate_y, 360, 14, FIX))       # thân đồ gá
    for xp, wpin in ((xp1, 14), (xp2, 8)):
        o.append(R(xp - 9, yb - 14, 18, 14, 'fill="#ffffff" fill-opacity="0.9" stroke="currentColor" stroke-width="1.2"'))
        o.append(R(xp - 14, yb + 5, 28, plate_y - yb - 5, FIX))                      # bệ chốt, không chạm hộp
        o.append(R(xp - wpin / 2, yb - 7, wpin, 12, f'fill="{BLUE}" fill-opacity="0.75" stroke="{BLUE}" stroke-width="1.4"'))  # chốt ngắn ≈ ½ đường kính
    # đế tì mặt phẳng (giữa hai chốt)
    for xs in (170, 250):
        o.append(R(xs - 12, yb, 24, plate_y - yb, FIX))
    o.append(dv(210, yb + 1, 3, RED))
    o.append(T(210, 172, "đế tì mặt phẳng: 3 bậc", 12, "middle", c=RED))
    o.append(T(xp1, 190, "chốt trụ ngắn: 2", 12, "middle", c=BLUE))
    o.append(T(xp2, 190, "chốt trám ngắn: 1", 12, "middle", c=BLUE))
    o.append(T(210, 76, "hộp", 13, "middle", c=ORANGE))
    # b) nhìn từ trên xuống mặt đáy
    o.append(T(12, 220, "b) Nhìn mặt đáy: hai lỗ chéo góc", 13, "start", "700"))
    bx0, by0, bx1, by1 = 50, 232, 370, 322
    o.append(R(bx0, by0, bx1 - bx0, by1 - by0, f'fill="{ORANGE}" fill-opacity="0.15" stroke="{ORANGE}" stroke-width="2"'))
    h1, h2 = (86, 277), (334, 277)
    o.append(Ln(*h1, *h2, w=1, dash="5 4"))
    for (cx, cy) in (h1, h2):
        o.append(C(cx, cy, 11, 'fill="#ffffff" fill-opacity="0.9" stroke="currentColor" stroke-width="1.4"'))
    o.append(C(*h1, 8, f'fill="{BLUE}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1.4"'))
    # chốt trám: vạt hai mặt dọc phương nối hai lỗ (gần ngang), phần trụ còn lại chặn xoay
    o.append(tram(*h2, 8, 5))
    o.append(T(86, 306, "chốt trụ", 12, "middle", c=BLUE))
    o.append(T(334, 306, "chốt trám", 12, "middle", c=BLUE))
    o.append(T(210, 268, "xa nhau nhất", 12, "middle"))
    return fig(svg(332, "Chuẩn tinh một mặt phẳng và hai lỗ", o),
               "Hình 3. Chuẩn tinh thống nhất: mặt đáy tì trên đế (khử 3 bậc), lỗ 1 lồng chốt trụ (2 bậc), lỗ 2 lồng chốt trám (1 bậc). Mặt vạt của chốt trám vuông góc với đường nối hai lỗ. Số trên hình là số bậc tự do khử.")


# Hình 4: thứ tự nguyên công
def fig_thu_tu():
    o = []
    steps = [
        (GREY, "0", "Phôi đúc gang · khử ứng suất dư"),
        (RED, "1", "Phay mặt phẳng chuẩn (gá chuẩn thô)"),
        (RED, "2", "Khoan – khoét – doa 2 lỗ chuẩn"),
        (BLUE, "3", "Gia công các mặt phẳng còn lại"),
        (BLUE, "4", "Thô, bán tinh các lỗ lắp ghép"),
        (BLUE, "5", "Khoan, ta rô lỗ kẹp chặt"),
        (BLUE, "6", "Gia công tinh lỗ lắp ghép"),
        (GREEN, "7", "Tổng kiểm tra"),
    ]
    y, bh, gap, bx, bw = 12, 30, 22, 46, 310
    for c, n, s in steps:
        if n != "0":
            o.append(Ar(bx + 20, y - gap + 2, bx + 20, y - 8, "currentColor", 1.6, L=6))
        o.append(R(bx, y, bw, bh, f'fill="{c}" fill-opacity="0.10" stroke="{c}" stroke-width="1.8" rx="5"'))
        o.append(T(bx + 20, y + 20, n, 14, "middle", "700", c))
        o.append(T(bx + 40, y + 20, s, 13))
        y += bh + gap
    # ngoặc giai đoạn
    def brace(y0, y1, label, c):
        xb = bx + bw + 8
        o.append(f'<polyline points="{xb},{y0} {xb + 8},{y0} {xb + 8},{y1} {xb},{y1}" fill="none" stroke="{c}" stroke-width="1.6"/>')
        o.append(T(xb + 14, (y0 + y1) / 2 + 5, label, 13, "start", "700", c))
    s1 = 12 + 1 * (bh + gap)
    brace(s1, s1 + 2 * bh + gap, "GĐ 1", RED)
    s2 = 12 + 3 * (bh + gap)
    brace(s2, s2 + 4 * bh + 3 * gap, "GĐ 2", BLUE)
    yt = 12 + 8 * (bh + gap) + 6
    o.append(T(12, yt, "GĐ 1: tạo chuẩn tinh thống nhất", 12, c=RED))
    o.append(T(12, yt + 18, "GĐ 2: dùng chuẩn đó cho mọi nguyên công còn lại", 12, c=BLUE))
    return fig(svg(yt + 28, "Thứ tự nguyên công gia công chi tiết hộp", o),
               "Hình 4. Quy trình điển hình: tạo chuẩn trước, mặt phẳng trước lỗ, lỗ thô trước lỗ tinh, kiểm cuối. Bước 0 khử ứng suất: theo yêu cầu của giáo trình, cách làm cụ thể là thông lệ; bước 1 gá theo chuẩn thô: thông lệ.")


# Hình 5: gia công hàng 4 lỗ đồng trục
def fig_hang_lo():
    o = []
    walls = [(60, "φ1"), (150, "φ2"), (240, "φ3"), (330, "φ4")]
    wv, r = 16, 12

    def panel(y0, title, done, guide, dao_from):
        yc = y0 + 58
        o.append(T(12, y0 + 14, title, 13, "start", "700"))
        o.append(R(walls[0][0], y0 + 20, walls[-1][0] + wv - walls[0][0], 6))     # thành trên
        o.append(R(walls[0][0], y0 + 90, walls[-1][0] + wv - walls[0][0], 6))     # thành dưới
        for x, name in walls:
            o.append(R(x, y0 + 26, wv, yc - r - (y0 + 26)))
            o.append(R(x, yc + r, wv, (y0 + 90) - (yc + r)))
            col = GREEN if name in done else "currentColor"
            o.append(T(x + wv / 2, y0 + 114, name, 13, "middle", "700", col))
            if name in done:
                o.append(Ln(x, yc - r, x + wv, yc - r, GREEN, 3))
                o.append(Ln(x, yc + r, x + wv, yc + r, GREEN, 3))
            if name in guide:
                o.append(R(x + 2, yc - r + 1, wv - 4, 4, f'fill="{ORANGE}" stroke="none"'))
                o.append(R(x + 2, yc + r - 5, wv - 4, 4, f'fill="{ORANGE}" stroke="none"'))
        o.append(Ln(24, yc, 396, yc, w=1, dash="10 3 2 3"))
        if dao_from == "phai":
            # trục dao công xôn từ phải, đã qua φ4, đang ở φ3
            o.append(R(250, yc - 5, 160, 10, f'fill="{GREY}" fill-opacity="0.6" stroke="currentColor" stroke-width="1"'))
            o.append(R(250, yc - 10, 6, 20, f'fill="{RED}" stroke="none"'))      # lưỡi dao ở φ3
            o.append(Ar(404, yc - 16, 364, yc - 16, RED))
            o.append(T(384, yc - 24, "tiến dao", 12, "middle", c=RED))
        else:
            # trục dao dài xuyên suốt, dẫn ở φ1 và φ4
            o.append(R(30, yc - 5, 380, 10, f'fill="{GREY}" fill-opacity="0.6" stroke="currentColor" stroke-width="1"'))
            for x, name in walls[1:3]:                                                   # lưỡi dao ở φ2, φ3
                o.append(R(x + 5, yc - 10, 6, 20, f'fill="{RED}" stroke="none"'))
        return yc

    panel(8, "a) Thô: dao công xôn từ một phía", ["φ4"], [], "phai")
    o.append(T(12, 144, "Bước 1: φ4 → bước 2: φ3; quay bàn 180°", 12))
    o.append(T(12, 160, "rồi bước 3: φ1 → bước 4: φ2", 12))
    panel(178, "b) Tinh, cách 2: hai lỗ ngoài dẫn hướng", ["φ1", "φ4"], ["φ1", "φ4"], "xuyen")
    o.append(T(12, 314, "φ4, φ1 xong trước (xanh), lắp bạc dẫn (cam),", 12))
    o.append(T(12, 330, "trục dao đi xuyên qua, lưỡi đỏ doa φ2, φ3", 12))
    return fig(svg(340, "Gia công hàng bốn lỗ đồng trục", o),
               "Hình 5. Hàng 4 lỗ đồng trục (mặt cắt, theo ví dụ của giáo trình). a) Gia công thô một nửa số lỗ từ một phía, quay bàn 180° làm nửa còn lại. b) Gia công tinh: làm hai lỗ ngoài cùng trước rồi dùng chúng dẫn hướng trục dao.")


# Hình 6: kiểm khoảng cách tâm bằng hai trục kiểm (tỉ lệ 1,5 px/mm)
def fig_kiem():
    k = 1.5
    d1, d2, A = 62, 47, 120
    c1x = 70 + k * d1 / 2
    c2x = c1x + k * A
    cy = 112
    o = []
    o.append(R(22, 40, 386, 144, 'fill="#94a3b8" fill-opacity="0.18" stroke="currentColor" stroke-width="1.2"'))
    for cx, d in ((c1x, d1), (c2x, d2)):
        o.append(C(cx, cy, k * d / 2 + 2, 'fill="#ffffff" fill-opacity="0.9" stroke="currentColor" stroke-width="1.5"'))
        o.append(C(cx, cy, k * d / 2, f'fill="{GREEN}" fill-opacity="0.25" stroke="{GREEN}" stroke-width="2"'))
        o.append(Ln(cx - 6, cy, cx + 6, cy, w=1.2) + Ln(cx, cy - 6, cx, cy + 6, w=1.2))
    xl = c1x - k * d1 / 2
    xr = c2x + k * d2 / 2
    yM = 22
    o.append(Ln(xl, yM - 6, xl, cy, RED, 1, "3 3"))
    o.append(Ln(xr, yM - 6, xr, cy, RED, 1, "3 3"))
    o.append(Dim(xl, yM, xr, yM, RED, 1.6))
    o.append(T((xl + xr) / 2, yM - 6, "M: thước cặp đo ngoài hai trục kiểm", 12, "middle", c=RED))
    yA = 204
    o.append(Ln(c1x, cy + 8, c1x, yA + 6, BLUE, 1, "3 3"))
    o.append(Ln(c2x, cy + 8, c2x, yA + 6, BLUE, 1, "3 3"))
    o.append(Dim(c1x, yA, c2x, yA))
    o.append(T((c1x + c2x) / 2, yA - 6, "A (khoảng cách tâm)", 12, "middle", c=BLUE))
    o.append(T(c1x, cy - 14, "d₁", 13, "middle", "700", GREEN))
    o.append(T(c2x, cy - 14, "d₂", 13, "middle", "700", GREEN))
    o.append(T(12, 232, "A = M − (d₁ + d₂) / 2", 14, "start", "700"))
    # kiểm: nhãn d không đè tâm chữ thập, nằm trong trục kiểm
    for d in (d1, d2):
        assert k * d / 2 > 14 + 13 + 4, d          # nhãn d nằm trọn trong trục kiểm, trên chữ thập
    assert xl > 24 and xr < 406, (xl, xr)
    return fig(svg(244, "Kiểm khoảng cách tâm hai lỗ bằng trục kiểm", o),
               "Hình 6. Đút trục kiểm vừa khít vào hai lỗ, đo kích thước ngoài M rồi trừ nửa tổng hai đường kính trục kiểm (vẽ theo tỉ lệ của bài toán mẫu).")


h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig_loai_hop, fig_yeu_cau, fig_chuan, fig_thu_tu, fig_hang_lo, fig_kiem), 1):
    tag = f"<!--FIG{n}-->"
    assert h.count(tag) == 1, tag
    h = h.replace(tag, f())
assert "<!--FIG" not in h
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
if not m:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600])
    sys.exit(1)
phut = math.ceil(float(m.group(1).replace(",", ".")))
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")
print("đã ghi theory.html ·", phut, "phút đọc")
