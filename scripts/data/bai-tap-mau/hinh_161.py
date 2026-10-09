"""Hình cho bài tập mẫu Chuyên đề 01 (HSG KHTN 9: Công và công suất), lesson_id tạm 161.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi chuyển động tính từ số liệu của đề (tỉ lệ quãng đường/thời gian đúng), không để lộ đáp số."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ───────────── tiện ích ─────────────
def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def mover(dx, dy, dur, inner):
    """Nhóm tịnh tiến thẳng đều (nội suy tuyến tính giữa hai giá trị): chạy một lần khi bấm, dừng ở khung cuối."""
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx:.1f} {dy:.1f}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')

import re as _re
def rich(s, size=13):
    """`F_ms` → F với chỉ số dưới ms (tspan hạ dòng rồi trả lại)."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def tri(pts, c="currentColor", sw=2.4, fill="none"):
    return '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>'


# ───────────── Dạng 1 · kéo thùng trượt đều 8 m, F' xiên 60° ─────────────
def d1(kk):
    p = f"d1{kk}"
    if kk == 0:
        FL = 118; S = 30; X0 = 26; W = 64; H = 38
        b = defs(p) + ground(FL, 16, 410)
        b += R(X0, FL - H, W, H, sw=1.4, dash="5 4", op=.45)
        crate = (R(X0, FL - H, W, H, sw=2.4) + txt(X0 + W / 2, FL - H / 2 + 5, "m = 40 kg", "currentColor", 12, "middle")
                 + arrow(p, "r", X0 + W, FL - H / 2, X0 + W + 52, FL - H / 2, 3) + txt(X0 + W + 8, FL - H / 2 - 10, "F = ?", RED))
        b += mover(8 * S, 0, 4, crate)
        b += seg(X0, 142, X0 + 8 * S, 142, "currentColor", 1.6)
        for i in range(5):
            b += seg(X0 + i * 2 * S, 136, X0 + i * 2 * S, 148, "currentColor", 1.6)
            b += txt(X0 + i * 2 * S, 164, ("0", "2", "4", "6", "8 m")[i], "currentColor", 12, "middle", "400")
        b += txt(16, 24, "μ = 0,25", "currentColor", 13) + txt(16, 42, "g = 10 m/s²", "currentColor", 13, "start", "400")
        b += txt(300, 24, "s = 8 m", ORG) + txt(300, 42, "A = ?", ORG)
        return fig("c1-0", "0 0 420 176", "Thùng hàng được kéo trượt đều 8 mét trên sàn nằm ngang bằng lực kéo nằm ngang",
                   b, "Mô phỏng: thùng trượt đều đúng quãng đường 8 m trên thước (tốc độ minh hoạ 2 m/s, chạy 4 s).")
    FL = 140
    b = defs(p) + ground(FL, 12, 410)
    # trái: bốn lực khi kéo ngang
    cx, W, H = 90, 64, 38
    b += R(cx - 32, FL - H, W, H, sw=2.4)
    cy = FL - H / 2
    b += arrow(p, "r", cx + 32, cy, cx + 86, cy, 3) + txt(cx + 70, cy - 10, "F", RED)
    b += arrow(p, "o", cx - 32, cy, cx - 86, cy, 3) + txt(cx - 80, cy - 16, "F_ms", ORG)
    b += arrow(p, "b", cx, cy, cx, cy - 56, 3) + txt(cx + 8, cy - 50, "N", BLUE)
    b += arrow(p, "g", cx, cy, cx, FL + 18, 3) + txt(cx + 8, FL + 30, "P", GRN)
    b += txt(16, 22, "Kéo ngang: α = 0°", "currentColor", 13, "start", "400")
    # phải: F' xiên 60° và hai thành phần
    qx = 280
    b += R(qx - 32, FL - H, W, H, sw=2.4)
    ox, oy = qx + 32, cy
    L = 70; tx, ty = ox + L * math.cos(math.radians(60)), oy - L * math.sin(math.radians(60))
    b += arrow(p, "r", ox, oy, tx, ty, 3) + txt(tx + 6, ty + 4, "F′", RED)
    b += arrow(p, "b", ox, oy, tx, oy, 2.4, "5 4") + txt(tx + 6, oy + 5, "F′cosα", BLUE, 12)
    b += seg(tx, oy, tx, ty, ORG, 2.4, "5 4") + txt(tx + 8, (oy + ty) / 2 - 8, "F′sinα", ORG, 12)
    b += arc(ox, oy, 26, 0, 60, RED, 1.8) + txt(ox + 15, oy - 7, "α", RED, 13)
    b += txt(220, 22, "Kéo xiên: chỉ F′cosα sinh công", "currentColor", 13, "start", "400")
    return fig("c1-2", "0 0 420 176", "Bên trái bốn lực tác dụng lên thùng khi kéo ngang; bên phải lực kéo xiên góc 60 độ được tách thành hai thành phần",
               b, "Dữ kiện: lực nào dọc theo dịch chuyển thì sinh công; lực vuông góc không sinh công. " + NOTE)


# ───────────── Dạng 2 · đòn bẩy l1=20 cm, l2=1,2 m, nâng 5 cm ─────────────
def lever_base(p, px, py, rot=0.0):
    beam = f'<line x1="{px - 40}" y1="{py}" x2="{px + 240}" y2="{py}" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>'
    blk = R(px - 38, py - 31, 28, 28, sw=2.4)
    return beam, blk

def d2(kk):
    p = f"d2{kk}"; px, py = 70, 88
    th = math.degrees(math.asin(0.05 / 0.2))   # vật lên 5 cm khi cánh tay 20 cm  → sinθ = 0,25
    pivot = tri([(px, py + 4), (px - 18, py + 32), (px + 18, py + 32)], "currentColor", 2.4)
    b = defs(p)
    if kk == 0:
        dur = 4
        beam, blk = lever_base(p, px, py)
        b += pivot + seg(px - 30, py + 32, px + 30, py + 32, "currentColor", 3)
        b += (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {px} {py};{th:.2f} {px} {py}" dur="{dur}s" '
              f'begin="indefinite" fill="freeze"/>{beam}{blk}</g>')
        xs = [px + 240 * math.cos(math.radians(th * i / 12)) for i in range(13)]
        ys = [py + 240 * math.sin(math.radians(th * i / 12)) for i in range(13)]
        b += (f'<line x1="{xs[0]:.1f}" y1="{ys[0] - 46:.1f}" x2="{xs[0]:.1f}" y2="{ys[0] - 6:.1f}" stroke="{RED}" stroke-width="3" marker-end="url(#{p}-r)">'
              f'{smil("x1", xs, dur)}{smil("y1", [y - 46 for y in ys], dur)}{smil("x2", xs, dur)}{smil("y2", [y - 6 for y in ys], dur)}</line>')
        b += txt(px + 252, py - 28, "F = ?", RED)
        b += txt(16, 26, "vật P = 600 N", "currentColor", 13) + txt(16, 44, "nâng lên h = 5 cm", "currentColor", 13, "start", "400")
        b += txt(px + 236, py + 80, "s = ?", ORG)
        dy = py + 100
        b += dim(p, "b", px - 40, dy, px, dy, "", 0, 0) + dim(p, "b", px, dy, px + 240, dy, "", 0, 0)
        b += txt(px - 38, dy + 20, "l₁ = 20 cm", BLUE, 13) + txt(px + 120, dy + 20, "l₂ = 1,2 m", BLUE, 13, "middle")
        return fig("c2-0", "0 0 420 214", "Đòn bẩy quay quanh điểm tựa: đầu ngắn mang vật nâng lên 5 cm, đầu dài bị đè xuống",
                   b, "Mô phỏng: vật lên 5 cm, đầu dài đi xuống theo hình học của đòn bẩy. Chạy 4 s.")
    beam, blk = lever_base(p, px, py)
    b += pivot + seg(px - 30, py + 32, px + 30, py + 32, "currentColor", 3) + beam + blk
    b += arrow(p, "g", px - 24, py - 74, px - 24, py - 34, 3) + txt(px - 14, py - 52, "P", GRN)
    b += arrow(p, "r", px + 240, py - 46, px + 240, py - 6, 3) + txt(px + 250, py - 28, "F", RED)
    dy = py + 56
    b += dim(p, "b", px - 40, dy, px, dy, "", 0, 0) + dim(p, "b", px, dy, px + 240, dy, "", 0, 0)
    b += txt(16, dy + 22, "l₁ = 20 cm = 0,2 m", BLUE, 13) + txt(px + 150, dy + 22, "l₂ = 1,2 m", BLUE, 13, "middle")
    b += txt(220, 26, "F·l₂ = P·l₁", "currentColor", 14) + txt(220, 46, "s / h = l₂ / l₁", ORG, 14)
    return fig("c2-2", "0 0 420 190", "Đòn bẩy cân bằng: trọng lượng P ở cánh tay đòn l1, lực F ở cánh tay đòn l2",
               b, "Dữ kiện: đổi l₁ và l₂ cùng đơn vị rồi lập tỉ số. " + NOTE)


# ───────────── Dạng 3 · hai máy nâng cùng độ cao 4 m ─────────────
def d3(kk):
    p = f"d3{kk}"; GY = 200
    if kk == 0:
        S = 32; HH = 4 * S; cxs = (110, 290); ms = ((46, 36, "50 kg", 20 / 4), (46, 28, "30 kg", 8 / 4)); names = ("Máy A", "Máy B")
        b = defs(p) + ground(GY, 40, 360)
        for i, cx in enumerate(cxs):
            w, h, lab, dur = ms[i]
            top0 = GY - h
            b += txt(cx, 16, names[i], "currentColor", 13, "middle")
            b += seg(cx - 26, 22, cx + 26, 22, "currentColor", 3)
            b += (f'<line x1="{cx}" y1="22" x2="{cx}" y2="{top0}" stroke="{GREY}" stroke-width="2">{smil("y2", [top0, top0 - HH], dur)}</line>')
            inner = R(cx - w / 2, top0, w, h, sw=2.4) + txt(cx, top0 + h / 2 + 4, lab, "currentColor", 12, "middle")
            b += mover(0, -HH, dur, inner)
        b += seg(60, GY - HH, 330, GY - HH, GREY, 1.4, "5 4")
        b += dim(p, "o", 196, GY - 2, 196, GY - HH + 2, "", 0, 0) + txt(204, GY - HH / 2 + 4, "h = 4 m", ORG)
        b += txt(110, 226, "t = 20 s", "currentColor", 13, "middle", "400") + txt(290, 226, "t = 8 s", "currentColor", 13, "middle", "400")
        return fig("c3-0", "0 0 420 236", "Hai máy nâng hai vật nặng khác nhau lên cùng độ cao 4 mét, máy B xong trước máy A",
                   b, "Mô phỏng: chạy nhanh 4 lần (máy A mất 5 s, máy B mất 2 s; tỉ lệ thời gian giữ đúng 20 : 8).")
    b = defs(p) + ground(GY - 40, 40, 380)
    for cx, w, h, lab, t_, col in ((110, 46, 36, "50 kg", "20 s", "Máy A"), (290, 46, 28, "30 kg", "8 s", "Máy B")):
        top0 = GY - 40 - h
        b += R(cx - w / 2, top0, w, h, sw=2.4) + txt(cx, top0 + h / 2 + 4, lab, "currentColor", 12, "middle")
        b += arrow(p, "o", cx, top0 - 6, cx, top0 - 62, 3)
        b += txt(cx, top0 - 72, f"{col}: {t_}", "currentColor", 13, "middle")
    b += txt(200, 40, "cùng h = 4 m", ORG, 13, "middle")
    b += txt(16, 188, "Công: lượng việc đã làm (J)", BLUE, 12, "start", "400") + txt(16, 206, "Công suất: làm nhanh hay chậm (W)", GRN, 12, "start", "400")
    return fig("c3-2", "0 0 420 236", "Máy A và máy B nâng vật lên cùng độ cao với khối lượng và thời gian khác nhau",
               b, "Dữ kiện: cùng độ cao, khác khối lượng và khác thời gian. " + NOTE)


# ───────────── Dạng 4 · mặt phẳng nghiêng l=5 m, h=1,5 m ─────────────
def d4(kk):
    p = f"d4{kk}"; S = 50; l = 5.0; h = 1.5
    ox, oy = 56, 184
    hh = S * h; hx = math.sqrt((S * l) ** 2 - hh ** 2); th = math.degrees(math.asin(h / l)); tr = math.radians(th)
    topx, topy = ox + hx, oy - hh
    def wp(lx, ly):   # toạ độ cục bộ (dọc ván, vuông góc ván hướng lên là ly<0) → toạ độ hình
        return ox + lx * math.cos(tr) + ly * math.sin(tr), oy - lx * math.sin(tr) + ly * math.cos(tr)
    b = defs(p) + seg(16, oy, 410, oy, "currentColor", 2) + seg(ox, oy, topx, topy, "currentColor", 3.4)
    b += R(topx, topy, 96, oy - topy, sw=2.2) + txt(topx + 10, topy + 24, "sàn xe", "currentColor", 12, "start", "400")
    b += seg(topx, topy, topx, oy, "currentColor", 1.2, "5 4", .6)
    b += dim(p, "o", topx + 80, topy + 3, topx + 80, oy - 3, "", 0, 0) + txt(topx + 72, (topy + oy) / 2 + 4, "h = 1,5 m", ORG, 13, "end")
    b += txt(ox + (108 if kk == 0 else 175), oy - 12, "l = 5 m", BLUE, 13, "middle")
    if kk == 0:
        blk = R(6, -26, 34, 26, sw=2.4) + txt(23, -8, "60 kg", "currentColor", 12, "middle")
        blk += arrow(p, "r", -34, -13, 4, -13, 3) + txt(-36, -24, "F = ?", RED, 12)
        b += f'<g transform="translate({ox} {oy}) rotate({-th:.2f})">{R(6, -26, 34, 26, sw=1.4, dash="5 4", op=.45)}{mover(S * l - 46, 0, 5, blk)}</g>'
        b += txt(250, 26, "F_ms = 60 N", ORG) + txt(250, 46, "A = ?", ORG)
        return fig("c4-0", "0 0 420 200", "Vật khối lượng 60 kg được đẩy lên sàn xe tải cao 1,5 mét bằng tấm ván dài 5 mét",
                   b, "Mô phỏng: vật đi hết chiều dài ván 5 m (tốc độ minh hoạ 1 m/s, chạy 5 s); hình vẽ đúng tỉ lệ l, h.")
    cx, cy = wp(120, -13)
    ux, uy = math.cos(tr), -math.sin(tr)            # hướng dọc ván lên
    nx, ny = -math.sin(tr), -math.cos(tr)           # pháp tuyến
    b += f'<g transform="translate({ox} {oy}) rotate({-th:.2f})">{R(103, -26, 34, 26, sw=2.4)}</g>'
    b += arrow(p, "r", cx, cy, cx + 50 * ux, cy + 50 * uy, 3) + txt(cx + 50 * ux + 4, cy + 50 * uy - 4, "F", RED)
    b += arrow(p, "o", cx, cy, cx - 44 * ux, cy - 44 * uy, 3) + txt(cx - 44 * ux - 38, cy - 44 * uy + 4, "F_ms", ORG)
    b += arrow(p, "g", cx, cy, cx, cy + 46, 3) + txt(cx + 8, cy + 40, "P", GRN)
    b += arrow(p, "b", cx, cy, cx + 44 * nx, cy + 44 * ny, 3) + txt(cx + 44 * nx - 14, cy + 44 * ny - 4, "N", BLUE)
    b += txt(16, 24, "Công có ích: P·h (theo độ cao h)", BLUE, 13, "start", "400") + txt(16, 44, "Công hao phí: F_ms·l (theo chiều dài l)", ORG, 13, "start", "400")
    return fig("c4-2", "0 0 420 200", "Vật trên mặt phẳng nghiêng chịu lực đẩy dọc ván, lực ma sát ngược chiều, trọng lực và phản lực",
               b, "Dữ kiện: công có ích tính theo độ cao h, công hao phí tính theo chiều dài ván l. Hình vẽ đúng tỉ lệ l, h.")


# ───────────── Dạng 5 · palăng 1 cố định + 1 động, m_r = 4 kg, m = 76 kg, h = 3 m ─────────────
def d5(kk):
    p = f"d5{kk}"; r = 12; xm = 130; xf = xm + 2 * r; ytop = 18; yf = 44; ym0 = 144; gy = 200; S = 22
    lift = 3 * S; free = 2 * lift; yfree0 = 60; dur = 5
    mov_in = (circ(xm, ym0, r, "currentColor", 2.6) + dot(xm, ym0, 2.5, "currentColor")
              + f'<path d="M{xm - r},{ym0} A{r},{r} 0 0 0 {xm + r},{ym0}" fill="none" stroke="{GREY}" stroke-width="2.4"/>'
              + seg(xm, ym0 + r, xm, gy - 34, "currentColor", 2) + R(xm - 22, gy - 34, 44, 34, sw=2.4) + txt(xm, gy - 12, "76 kg", "currentColor", 12, "middle"))
    fixed = (seg(xf, ytop, xf, yf, "currentColor", 2) + circ(xf, yf, r, "currentColor", 2.6) + dot(xf, yf, 2.5)
             + f'<path d="M{xf - r},{yf} A{r},{r} 0 0 1 {xf + r},{yf}" fill="none" stroke="{GREY}" stroke-width="2.4"/>')
    b = defs(p) + seg(xm - 50, ytop, xf + 50, ytop, "currentColor", 3.4) + seg(100, gy, 200, gy, "currentColor", 3.4) + fixed
    b += dot(xm - r, ytop, 3, "currentColor")
    if kk == 0:
        b += f'<line x1="{xm - r}" y1="{ytop}" x2="{xm - r}" y2="{ym0}" stroke="{GREY}" stroke-width="2.4">{smil("y2", [ym0, ym0 - lift], dur)}</line>'
        b += f'<line x1="{xm + r}" y1="{ym0}" x2="{xm + r}" y2="{yf}" stroke="{GREY}" stroke-width="2.4">{smil("y1", [ym0, ym0 - lift], dur)}</line>'
        b += f'<line x1="{xf + r}" y1="{yf}" x2="{xf + r}" y2="{yfree0}" stroke="{GREY}" stroke-width="2.4">{smil("y2", [yfree0, yfree0 + free], dur)}</line>'
        b += mover(0, -lift, dur, mov_in)
        b += mover(0, free, dur, circ(xf + r, yfree0, 5, RED, 2, RED) + txt(xf + r + 10, yfree0 + 5, "F = ?", RED, 13))
        b += dim(p, "o", 80, gy - 2, 80, gy - lift + 2, "", 0, 0) + txt(72, gy - lift / 2 + 4, "h = 3 m", ORG, 13, "end")
        b += txt(236, 40, "vật: m = 76 kg", "currentColor", 13) + txt(236, 60, "ròng rọc động: m_r = 4 kg", "currentColor", 13)
        b += txt(236, 90, "dây đi xuống: s = ?", ORG, 13) + txt(236, 110, "A_tp = ?", ORG, 13) + txt(236, 130, "H = ?", ORG, 13)
        return fig("c5-0", "0 0 420 232", "Palăng gồm một ròng rọc cố định và một ròng rọc động nâng vật lên 3 mét, đầu dây tự do đi xuống gấp đôi",
                   b, "Mô phỏng: vật lên 3 m, đầu dây đi xuống theo đúng tỉ lệ; chạy 5 s.")
    b += f'<line x1="{xm - r}" y1="{ytop}" x2="{xm - r}" y2="{ym0}" stroke="{GREY}" stroke-width="2.4"/>'
    b += f'<line x1="{xm + r}" y1="{ym0}" x2="{xm + r}" y2="{yf}" stroke="{GREY}" stroke-width="2.4"/>'
    b += f'<line x1="{xf + r}" y1="{yf}" x2="{xf + r}" y2="{yfree0 + 70}" stroke="{GREY}" stroke-width="2.4"/>'
    b += mov_in
    b += arrow(p, "r", xf + r, yfree0 + 50, xf + r, yfree0 + 88, 3) + txt(xf + r + 10, yfree0 + 84, "F", RED, 13)
    b += txt(xm - r - 8, 104, "①", ORG, 14, "end") + txt(xm + r + 6, 104, "②", ORG, 14)
    b += txt(236, 40, "Đếm đoạn dây đỡ vật", "currentColor", 12, "start", "400") + txt(236, 56, "và ròng rọc động", "currentColor", 12, "start", "400")
    b += txt(236, 84, "P_t = P_v + P_r", BLUE, 13) + txt(236, 104, "F = P_t / n", ORG, 13) + txt(236, 124, "s = n·h", ORG, 13)
    return fig("c5-2", "0 0 420 232", "Hai đoạn dây đỡ khối gồm vật và ròng rọc động; đầu dây tự do kéo xuống",
               b, "Dữ kiện: đếm đoạn dây đỡ khối vật và ròng rọc động (không đếm số ròng rọc). " + NOTE)


# ───────────── Dạng 6 · máy bơm giếng sâu 12 m ─────────────
def d6(kk):
    p = f"d6{kk}"
    if kk == 0:
        gyy = 62; S = 12; HH = 12 * S; x0, x1 = 110, 210; px = 160; bot = gyy + HH
        b = defs(p) + seg(16, gyy, x0, gyy, "currentColor", 3.4) + seg(x1, gyy, 410, gyy, "currentColor", 3.4)
        b += seg(x0, gyy, x0, bot, "currentColor", 2.4) + seg(x1, gyy, x1, bot, "currentColor", 2.4) + seg(x0, bot, x1, bot, "currentColor", 2.4)
        b += R(x0 + 2, bot - 14, x1 - x0 - 4, 12, BLUE, 1.6, "none") + seg(px, bot - 8, px, gyy - 6, GREY, 6, "", .55)
        b += R(px - 22, gyy - 34, 44, 26, sw=2.4) + txt(px, gyy - 16, "bơm", "currentColor", 12, "middle")
        b += arrow(p, "b", px + 22, gyy - 21, 262, gyy - 21, 3) + R(262, gyy - 38, 70, 36, BLUE, 2, "none") + txt(297, gyy - 15, "bể", BLUE, 12, "middle")
        b += mover(0, -(HH - 22), 5, circ(px, bot - 22, 7, BLUE, 2, BLUE))
        b += dim(p, "o", 86, gyy + 3, 86, bot - 3, "", 0, 0) + txt(78, (gyy + bot) / 2 + 4, "h = 12 m", ORG, 13, "end")
        b += txt(236, 120, "P_tp = 1250 W", "currentColor", 13) + txt(236, 142, "hiệu suất H = 80%", "currentColor", 13) + txt(236, 164, "thời gian t = 6 phút", "currentColor", 13)
        b += txt(236, 196, "khối lượng nước m = ?", ORG, 13) + txt(236, 216, "thể tích V = ?", ORG, 13)
        return fig("c6-0", "0 0 420 232", "Máy bơm nâng nước từ giếng sâu 12 mét lên miệng giếng rồi đẩy vào bể chứa",
                   b, "Mô phỏng: một phần tử nước được nâng đúng 12 m (tốc độ minh hoạ, chạy 5 s); số nước bơm được là điều cần tìm.")
    b = defs(p)
    boxes = [(16, "P toàn phần", "P_tp = 1250 W"), (150, "P có ích", "P_ci = H·P_tp"), (284, "A có ích", "A_ci = P_ci·t")]
    for i, (x, a, c) in enumerate(boxes):
        b += R(x, 50, 120, 56, "currentColor", 2.2, "none", 8) + txt(x + 60, 74, a, "currentColor", 12, "middle") + txt(x + 60, 96, c, ORG if i else "currentColor", 13, "middle")
        if i < 2:
            b += arrow(p, "b", x + 122, 78, x + 148, 78, 3)
    b += txt(344, 140, "A_ci = 10·m·h", ORG, 13, "middle") + arrow(p, "o", 344, 112, 344, 124, 2.4)
    b += txt(16, 150, "⚠ Công suất ghi trên máy là toàn phần", "currentColor", 13, "start", "400")
    b += txt(16, 172, "1 lít nước = 1 kg · 1 m³ = 1000 lít", "currentColor", 13, "start", "400")
    return fig("c6-2", "0 0 420 190", "Từ công suất toàn phần của máy bơm suy ra công suất có ích, công có ích rồi khối lượng nước",
               b, "Dữ kiện: chuỗi tính từ công suất toàn phần đến khối lượng nước. " + NOTE)


# ───────────── Dạng 7 · ô tô 1,5 tấn lên dốc 300 m, cao 15 m (độ dốc vẽ phóng đại) ─────────────
def d7(kk):
    p = f"d7{kk}"; ox, oy = 24, 190; ex, ey = 374, 120
    L = math.hypot(ex - ox, ey - oy); th = math.degrees(math.atan2(oy - ey, ex - ox)); tr = math.radians(th)
    b = defs(p) + seg(16, oy, 410, oy, "currentColor", 2) + seg(ox, oy, ex, ey, "currentColor", 3.4) + seg(ex, ey, ex, oy, "currentColor", 1.2, "5 4", .6)
    b += dim(p, "o", ex + 22, ey + 3, ex + 22, oy - 3, "", 0, 0) + txt(ex - 8, (ey + oy) / 2 + 24, "h = 15 m", ORG, 13, "end")
    if kk == 0:
        b += txt(190, oy - 8, "l = 300 m", BLUE, 13, "middle")
    car = (R(0, -22, 60, 12, sw=2.4) + f'<polyline points="14,-22 24,-32 44,-32 52,-22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/>'
           + circ(14, -6, 6, "currentColor", 2.4) + circ(46, -6, 6, "currentColor", 2.4))
    if kk == 0:
        ghost = car.replace('stroke="currentColor"', 'stroke="currentColor" opacity=".4"')
        b += f'<g transform="translate({ox + 8} {oy}) rotate({-th:.2f})">{ghost}{mover(L - 80, 0, 6, car)}</g>'
        b += txt(16, 24, "m = 1,5 tấn", "currentColor", 13) + txt(16, 44, "v = 18 km/h (đều)", "currentColor", 13) + txt(16, 66, "F_c = 450 N", ORG, 13)
        b += txt(236, 24, "F = ?", RED) + txt(236, 44, "A = ?   H = ?", RED) + txt(236, 64, "P_cs = ?", RED)
        return fig("c7-0", "0 0 420 206", "Ô tô chuyển động đều lên dốc dài 300 mét, cao 15 mét",
                   b, "Mô phỏng: ô tô đi hết chiều dài dốc (chạy nhanh 10 lần: 60 s thật = 6 s); độ nghiêng vẽ phóng đại.")
    ux, uy = math.cos(tr), -math.sin(tr)
    X = 170
    b += f'<g transform="translate({ox + X} {oy}) rotate({-th:.2f})">{car}</g>'
    cx, cy = ox + X + 30 * math.cos(tr) - 16 * math.sin(tr), oy - X * 0 - (X + 30) * 0 - 30 * math.sin(tr) - 16 * math.cos(tr)
    cy = oy - (X + 0) * math.sin(tr) * 0 - 30 * math.sin(tr) - 16 * math.cos(tr) - X * (ey - oy) / (ex - ox) * -1 * -1 * 0
    cy = oy - ((X + 30) * (oy - ey) / (ex - ox)) - 16
    b += arrow(p, "r", cx, cy, cx + 44 * ux, cy + 44 * uy, 3) + txt(cx + 44 * ux + 4, cy + 44 * uy - 6, "F", RED)
    b += arrow(p, "o", cx, cy, cx - 40 * ux, cy - 40 * uy, 3) + txt(cx - 40 * ux - 26, cy - 40 * uy + 2, "F_c", ORG)
    b += arrow(p, "g", cx, cy, cx, cy + 36, 3) + txt(cx + 8, cy + 36, "P", GRN)
    b += txt(16, 24, "F = F_c + P·h / l", "currentColor", 13)
    b += txt(16, 44, "P·h / l : trọng lực dọc dốc", BLUE, 12, "start", "400")
    b += txt(16, 64, "P_cs = F·v", "currentColor", 13) + txt(16, 84, "(đổi v ra m/s)", "currentColor", 12, "start", "400")
    return fig("c7-2", "0 0 420 206", "Ô tô chuyển động đều lên dốc: lực kéo cân bằng lực cản và thành phần trọng lực dọc dốc",
               b, "Dữ kiện: lực kéo thắng cả lực cản lẫn thành phần trọng lực dọc dốc. " + NOTE + " Độ nghiêng vẽ phóng đại.")


BUILD = [d1, d2, d3, d4, d5, d6, d7]
