"""Linh kiện vẽ sơ đồ mạch điện + đồ thị cho CĐ03 HSG (lesson 159). Dùng chung cho
content/hsg9/cd03-dien-tro-dinh-luat-ohm/build_figs.py (lý thuyết) và build-hinh-159.py (bài tập mẫu).
Nhãn có chỉ số dưới: viết `R_A`, `R_{max}`, `I_min`, `U_V` -> tspan hạ dòng (hàm rich)."""
import os, re, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from hinh import *          # RED BLUE ORG GRN, seg, poly, dot, lbl, arrow, chevron, text, fig …
from svg_lib import chevron, wrap

GREY = "#94a3b8"


def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')


def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def rich(s, size=13):
    """`R_A` hoặc `R_{max}` -> chỉ số dưới (tspan hạ dòng rồi trả lại)."""
    out, pos = "", 0
    ms = list(re.finditer(r"_\{([^}]+)\}|_([A-Za-z0-9]+)", s))
    for k, m in enumerate(ms):
        out += s[pos:m.start()] if k == 0 else ""
        out += f'<tspan dy="4" font-size="{size - 3}">{m.group(1) or m.group(2)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        rest = s[m.end():nxt]
        if rest:
            out += f'<tspan dy="-4">{rest}</tspan>'
        pos = m.end()
    return out if ms else s


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    size = max(size, 14)
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def tick(x, y, s=7):
    return seg(x, y - s, x, y + s, "currentColor", 2)


# ───────── Ký hiệu mạch điện (nét currentColor, 2 px) ─────────
def wire(*pts, c="currentColor", w=2):
    return poly(list(pts), c, w)


def resistor(cx, cy, label="", w=54, h=16, c="currentColor", lab_dy=-14, size=13):
    """Điện trở nằm ngang, tâm (cx, cy); dây nối ngoài do người gọi vẽ."""
    return R(cx - w / 2, cy - h / 2, w, h, c, 2.4) + (txt(cx, cy + lab_dy - h / 2 + 6, label, c, size, "middle") if label else "")


def rheostat(cx, cy, label="", w=76, h=16, pos=None, c="currentColor", lab_dy=-14, size=13):
    """Biến trở: điện trở có mũi tên xiên cắt qua (con chạy). pos = vị trí con chạy 0..1 (theo chiều rộng) nếu muốn vẽ."""
    b = R(cx - w / 2, cy - h / 2, w, h, c, 2.4)
    px = cx if pos is None else cx - w / 2 + pos * w
    b += seg(px - 12, cy + 18, px + 12, cy - 20, ORG, 2.2) + chevron(px + 12, cy - 20, 24, -38, ORG, 2.2, 9)
    if label:
        b += txt(cx, cy + lab_dy - h / 2 - 8, label, c, size, "middle")
    return b


def battery(cx, cy, label="", c="currentColor", size=13, side="left"):
    """Nguồn: gạch dài (cực +) trên, gạch ngắn (cực −) dưới, đặt trên dây dọc x = cx."""
    b = seg(cx - 14, cy - 5, cx + 14, cy - 5, c, 2.6) + seg(cx - 8, cy + 5, cx + 8, cy + 5, c, 4)
    b += txt(cx + (20 if side == "left" else -20), cy - 6, "+", c, 13, "start" if side == "left" else "end", "700")
    if label:
        b += txt(cx + (20 if side == "left" else -20), cy + 14, label, c, size, "start" if side == "left" else "end")
    return b


def meter(cx, cy, letter, c="currentColor", r=12, size=14):
    return circ(cx, cy, r, c, 2.2) + txt(cx, cy + 5, letter, c, size, "middle")


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# ───────── Đồ thị: lưới + trục ─────────
def graph_axes(ox, oy, wpx, hpx, xlab, ylab, xt=(), yt=(), kx=1.0, ky=1.0, grid=True):
    """Trục gốc (ox, oy). xt, yt = các giá trị chia vạch (đơn vị thật), kx, ky = px mỗi đơn vị."""
    b = ""
    if grid:
        for v in xt:
            if v: b += seg(ox + kx * v, oy, ox + kx * v, oy - hpx, GREY, 1, "4 4", .45)
        for v in yt:
            if v: b += seg(ox, oy - ky * v, ox + wpx, oy - ky * v, GREY, 1, "4 4", .45)
    b += seg(ox, oy, ox + wpx + 10, oy, "currentColor", 1.8) + chevron(ox + wpx + 10, oy, 1, 0, "currentColor", 1.8, 9)
    b += seg(ox, oy, ox, oy - hpx - 10, "currentColor", 1.8) + chevron(ox, oy - hpx - 10, 0, -1, "currentColor", 1.8, 9)
    for v in xt:
        b += seg(ox + kx * v, oy, ox + kx * v, oy + 5, "currentColor", 1.4) + txt(ox + kx * v, oy + 19, f"{v:g}".replace(".", ","), "currentColor", 12, "middle", "400")
    for v in yt:
        b += seg(ox - 5, oy - ky * v, ox, oy - ky * v, "currentColor", 1.4) + txt(ox - 8, oy - ky * v + 4, f"{v:g}".replace(".", ","), "currentColor", 12, "end", "400")
    b += txt(ox + wpx + 10, oy + 32, xlab, "currentColor", 13, "end") + txt(ox + 6, oy - hpx - 12, ylab, "currentColor", 13, "start")
    return b


# ───────── Sơ đồ dùng chung ─────────
def hwire(y, x0, x1, gaps=(), c="currentColor"):
    """Dây ngang từ x0 đến x1, bỏ các khoảng (a, b) nơi đặt linh kiện."""
    xs, b = x0, ""
    for a, e in sorted(gaps):
        b += seg(xs, y, a, y, c, 2)
        xs = e
    return b + seg(xs, y, x1, y, c, 2)


def vwire(x, y0, y1, gaps=(), c="currentColor"):
    ys, b = y0, ""
    for a, e in sorted(gaps):
        b += seg(x, ys, x, a, c, 2)
        ys = e
    return b + seg(x, ys, x, y1, c, 2)


def mach_bien_tro(label_u="U = 24 V", label_r="R = 30 Ω", label_b="biến trở 50 Ω", with_a=True, pos=None):
    """Nguồn — điện trở phụ R — biến trở (nối tiếp) — ampe kế. Thân SVG, viewBox 0 0 380 170."""
    L, Rr, T, B = 36, 344, 44, 128
    b = hwire(T, L, Rr, [(103, 157), (210, 290)]) + vwire(Rr, T, B) + hwire(B, L, Rr, [(178, 202)] if with_a else []) + vwire(L, T, B, [(74, 100)])
    b += battery(L, 87, label_u)
    b += resistor(130, T) + txt(130, T - 18, label_r, "currentColor", 13, "middle")
    b += rheostat(250, T, "", 80, 16, pos) + txt(250, T - 32, label_b, ORG, 13, "middle")
    if with_a:
        b += meter(190, B, "A", RED)
    return b


def mach_dung_cu(R_label="R = 24 Ω", ra="R_A = 1 Ω", rv="R_V = 600 Ω", u="U = 15 V"):
    """Nguồn — ampe kế (R_A) — R, vôn kế (R_V) song song với R. viewBox 0 0 380 170."""
    L, Rr, T, B = 36, 344, 44, 150
    b = hwire(T, L, Rr, [(88, 112), (200, 260)]) + vwire(Rr, T, B) + hwire(B, L, Rr) + vwire(L, T, B, [(84, 110)])
    b += battery(L, 97, u)
    b += meter(100, T, "A", RED) + txt(100, T - 20, ra, RED, 13, "middle")
    b += resistor(230, T, "", 60) + txt(230, T - 18, R_label, "currentColor", 13, "middle")
    b += wire((200, T), (200, 104), (218, 104), c=BLUE) + wire((242, 104), (260, 104), (260, T), c=BLUE)
    b += meter(230, 104, "V", BLUE) + txt(230, 136, rv, BLUE, 13, "middle")
    return b
