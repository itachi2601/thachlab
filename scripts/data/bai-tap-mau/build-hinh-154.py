"""Bài tập mẫu Chuyên đề 11 "Cơ học chất lưu: áp suất chất lỏng, bình thông nhau và lực đẩy Archimedes"
(khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 154.
Nguồn: content/hsg9/cd11-co-hoc-chat-luu/nguon.md (mục C, D, E, G; số liệu mọi bài đã tự giải lại bằng code, xem CHECK bên dưới).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-154.py   (idempotent; ghi 154.json)
Hình mô phỏng/hình dữ kiện nằm trong file này (không có hinh_154.py riêng)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "154.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
OIL = "#facc15"

# ═════════════ KIỂM SỐ LIỆU (tự giải lại độc lập, in ra) ═════════════
def CHECK():
    ok = lambda name, got, want, tol=1e-9: (print(f"  {name}: {got:g}" + ("" if abs(got - want) <= tol * max(1, abs(want)) else f"  <-- LỆCH, cần {want}")),
                                           None if abs(got - want) <= tol * max(1, abs(want)) else sys.exit(f"CHECK hỏng: {name}"))
    dn, dd = 10000.0, 8000.0
    # Dạng 1
    p1 = dd * 0.2; pdy = p1 + dn * 0.4; S = 200e-4
    ok("D1 p1", p1, 1600); ok("D1 p_đáy", pdy, 5600); ok("D1 F_đáy", pdy * S, 112)
    ok("D1 P_chất lỏng = F_đáy", 10 * 1000 * S * 0.4 + 10 * 800 * S * 0.2, 112)
    pl = p1 + dn * 0.30; ok("D1 p_lỗ", pl, 4600); ok("D1 F_nắp", pl * 5e-4, 2.3, 1e-9)
    # Dạng 2
    hn = dd * 25 / dn; y = hn * 30 / 50; x = hn * 20 / 50
    ok("D2 h_n", hn, 20); ok("D2 y", y, 12); ok("D2 x", x, 8); ok("D2 S1x=S2y", 30 * x - 20 * y, 0); ok("D2 chênh", 25 - hn, 5)
    ok("D2 thế ngược p_A=p_B", dd * 0.25 - dn * (x + y) / 100, 0)
    # Dạng 3
    hch = 20 * 700 / 1000; Pg = 10 * 700 * 40e-4 * 0.2; Fmax = 10 * 1000 * 40e-4 * 0.2
    ok("D3 h_ch", hch, 14); ok("D3 P", Pg, 5.6); ok("D3 F_A khi nổi", 10 * 1000 * 40e-4 * hch / 100, 5.6)
    ok("D3 m_cân (g)", (Fmax - Pg) / 10 * 1000, 240); ok("D3 Δh", 40 * hch / 160, 3.5)
    # Dạng 4
    FA = 3.6 - 2.4; V = FA / 10000; ok("D4 F_A", FA, 1.2); ok("D4 V (cm3)", V * 1e6, 120); ok("D4 D_v", 0.36 / V, 3000, 1e-9)
    ok("D4 D_X", (3.6 - 2.76) / (10 * V), 700, 1e-9)
    T = 10 * 1000 * 500e-6 - 0.2 * 10; ok("D4 T", T, 3); ok("D4 V_ch (cm3)", 0.2 * 10 / 10000 * 1e6, 200)
    # Dạng 5
    V1 = 540 + 39; V2 = 540 + 39 / 7.8
    ok("D5 V1", V1, 579); ok("D5 V2", V2, 545); ok("D5 Δh", (V1 - V2) / 85, 0.4)
    assert (540 + 39) / (540 / 0.9 + 5) < 1 and (540 + 39) / (540 / 0.9 + 39 / 0.8) < 1, "hệ phải nổi"
    ok("D5 sáp: V2 = V1", 540 + 39 / 1.0 - V1, 0)
    # Dạng 6
    P2 = 3 * 10 / 30; Pn = 3 * 8 / 32; FA6 = P2 - Pn; V6 = FA6 / 10000 * 1e6
    ok("D6 P2", P2, 1); ok("D6 P2'", Pn, 0.75); ok("D6 F_A", FA6, 0.25); ok("D6 V2 (cm3)", V6, 25); ok("D6 D2", 0.1 / (V6 * 1e-6), 4000, 1e-9)
    # Tự luận
    ok("E1", 1e5 + 10 * 1030 * 35, 460500); ok("E2 p", 10 * 800 * 0.8, 6400); ok("E2 F", 6400 * 0.015, 96)
    ok("E3", 1000 * 27.2 / 13600, 2); ok("E4", (800 * 20 - 700 * 10) / 1000, 9)
    ok("E5 D", 0.78 / 1e-4, 7800); ok("E6", 1000 * 12 / 15, 800); ok("E7", 150 / (1 - 900 / 1030), 1188.4615, 1e-6)
    ok("E8 V đặc", 890 / 8.9, 100); ok("E8 D_tb", 890 / 150, 5.9333, 1e-4)
    ok("E9", (800 - 700) * 10 * 1e-3, 1); ok("E10 F_A", 10 * 1000 * 1.56 / 7800, 2); ok("E11", 1000 / 300, 3.3333, 1e-4)
    ok("D5' V sắt", 390 / 7.8, 50); ok("D5' F_Amax", 10 * 1000 * 500e-6, 5); ok("D5' rỗng min", 390 - 50, 340)
    ok("D2b D_g", 1000 * 18 / 20, 900); hnb = (900 * 20 - 800 * 20) / 200; ok("D2b h_n", hnb, 10)
    L = 60.0; xr = L * (1 - math.sqrt(1 - 0.5)); ok("D3' x", xr, 17.5736, 1e-4)
    ok("D3' thế ngược", 0.5 * L * L / 2 - (xr * (L - xr / 2)), 0, 1e-9)
    # G1
    yy = 16 / 3; xx = 2 * yy; ok("G1 y", yy, 5.3333, 1e-4); ok("G1 x", xx, 10.6667, 1e-4)
    ok("G1 thế ngược", 1000 * (40 - xx) - (1000 * yy + 800 * 30), 0, 1e-9)
    d2 = 1.0; d1 = 2 * d2; ok("G1b Δh2", 300 / (10000 * 3) * 100, 1); ok("G1b mặt dầu", 750 / 200 - d2, 2.75)
    # G2
    ok("G2 P_hệ", 10 * 600 * 100e-6 + 10 * 2400 * 100e-6, 3.0); ok("G2 F_Amax", 10 * 1000 * 200e-6, 2.0)
    Vx = 1.0 / 9000; ok("G2 Vx (cm3)", Vx * 1e6, 111.111, 1e-4); ok("G2 T", 2.4 - 1.0, 1.4)
    ok("G2 kiểm A+xốp", (1.0 + 10000 * Vx) - (0.6 + 1000 * Vx) - 1.4, 0, 1e-9)
    # G3
    P2g = 2 * 15 / 25; ok("G3 m2 (g)", P2g / 10 * 1000, 120); Fa = 10 * 1000 * (0.12 / 4000); ok("G3 F_A", Fa, 0.3)
    ok("G3 x", 0.9 * 40 / 2.9, 12.4138, 1e-4); ok("G3 dời", 15 - 36 / 2.9, 2.5862, 1e-4)
CHECK()


# ───────────── tiện ích hình ─────────────
def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def rich(s, size=13):
    parts = re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def liq(x, y, w, h, col=BLUE, op=0.3, anims=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{max(h, 0):.1f}" fill="{col}" fill-opacity="{op}" stroke="none">{anims}</rect>')

def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def anim_tr(vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return (f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"{a:.1f} {b:.1f}" for a, b in vals)}"{k} '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def vessel(x0, x1, ytop, ybot, sw=2.6):
    return (f'<polyline fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linejoin="round" '
            f'points="{x0},{ytop} {x0},{ybot} {x1},{ybot} {x1},{ytop}"/>')

def dashed(x1, y1, x2, y2, c="currentColor", w=1.4, op=.7):
    return seg(x1, y1, x2, y2, c, w, "5 4", op)

def tri(pts, c="currentColor", sw=2.4, fill="none"):
    return '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>'


# ───────────── Dạng 1 · bình trụ hai lớp (nước 40 cm + dầu 20 cm), lỗ cách đáy 10 cm ─────────────
def d1(kk):
    p = f"e1{kk}"; yb = 206; s = 2.4; x0, x1 = 150, 250
    yw = yb - 40 * s; yo = yw - 20 * s; yl = yb - 10 * s
    b = defs(p)
    if kk == 0:
        b += liq(x0, yw, x1 - x0, 40 * s, BLUE, .3, anim("y", [yb, yw, yw], 3.2, "0;0.6;1") + anim("height", [0, 40 * s, 40 * s], 3.2, "0;0.6;1"))
        b += liq(x0, yo, x1 - x0, 20 * s, OIL, .4, anim("y", [yw, yw, yo], 3.2, "0;0.6;1") + anim("height", [0, 0, 20 * s], 3.2, "0;0.6;1"))
    else:
        b += liq(x0, yw, x1 - x0, 40 * s, BLUE, .3) + liq(x0, yo, x1 - x0, 20 * s, OIL, .4)
    b += vessel(x0, x1, yo - 14, yb) + dashed(x0, yw, x1, yw, "currentColor", 1.2, .5)
    b += R(x1 - 2, yl - 5, 10, 10, "currentColor", 2.2, "none")
    b += txt(x0 + 50, yo + 28, "dầu", "currentColor", 13, "middle", "400") + txt(x0 + 50, yw + 40, "nước", "currentColor", 13, "middle", "400")
    b += txt(x1 + 16, yl - 6, "lỗ có nắp", "currentColor", 12, "start", "400") + txt(x1 + 16, yl + 16, "S_l = 5 cm²", "currentColor", 12, "start", "400")
    b += dim(p, "o", x0 - 22, yo + 1, x0 - 22, yw - 1, "", 0, 0) + txt(x0 - 28, (yo + yw) / 2 + 4, "h_d = 20 cm", ORG, 12, "end")
    b += dim(p, "b", x0 - 22, yw + 1, x0 - 22, yb - 1, "", 0, 0) + txt(x0 - 28, (yw + yb) / 2 + 4, "h_n = 40 cm", BLUE, 12, "end")
    b += txt(16, 24, "S = 200 cm²", "currentColor", 13) + txt(16, 44, "D_d = 800 kg/m³", "currentColor", 12, "start", "400") + txt(16, 62, "D_n = 1000 kg/m³", "currentColor", 12, "start", "400")
    if kk == 0:
        b += txt(x0 + 50, yb + 22, "p_đáy = ?   F_đáy = ?", RED, 13, "middle")
        return fig("e1-0", "0 0 420 234", "Bình trụ thẳng đứng chứa lớp nước ở dưới và lớp dầu nổi phía trên, thành bình có một lỗ nhỏ bịt nắp gần đáy",
                   b, "Mô phỏng: rót nước tới 40 cm rồi rót dầu 20 cm lên trên (chạy 3 s). Lỗ có nắp ở thành bình, cách đáy 10 cm.")
    b += dim(p, "o", x1 + 130, yo + 1, x1 + 130, yl - 1, "", 0, 0) + txt(x1 + 138, (yo + yl) / 2 + 4, "h", ORG, 13)
    b += dashed(x1 + 8, yl, x1 + 130, yl, ORG, 1.2, .8)
    b += dim(p, "g", x1 + 100, yl + 1, x1 + 100, yb - 1, "", 0, 0) + txt(x1 + 106, yl + 17, "10 cm", GRN, 12)
    b += txt(x1 + 10, yw + 4, "mặt phân cách", "currentColor", 11, "start", "400")
    return fig("e1-2", "0 0 420 234", "Bình hai lớp chất lỏng: độ sâu h của lỗ đo từ mặt thoáng của lớp dầu xuống tâm lỗ",
               b, "Dữ kiện: h đo từ mặt thoáng xuống điểm xét ; lỗ nằm trong lớp nước. " + NOTE)


# ───────────── Dạng 2 · ống chữ U, S1 = 30 cm², S2 = 20 cm², đổ dầu vào nhánh trái ─────────────
def _u_tube(p, hd_s, kk):
    """Hình ống chữ U tại trạng thái đã cân bằng với cột dầu hd_s (cm). Trả (body, yL, yR, yTop, y0)."""
    s = 3.2; yb = 235; xl0, xl1, xr0, xr1 = 90, 156, 262, 306
    y0 = yb - 40 * s
    hn_s = 0.8 * hd_s; ys_ = hn_s * 30 / 50; xs_ = hn_s * 20 / 50
    yL = y0 + xs_ * s; yR = y0 - ys_ * s; yT = yL - hd_s * s
    return s, yb, (xl0, xl1, xr0, xr1), y0, yL, yR, yT

def d2(kk):
    p = f"e2{kk}"; hd_s = 15 if kk == 0 else 15
    s, yb, (xl0, xl1, xr0, xr1), y0, yL, yR, yT = _u_tube(p, hd_s, kk)
    b = defs(p)
    # nước: nhánh trái, ống nối, nhánh phải
    if kk == 0:
        b += liq(xl0, yL, xl1 - xl0, yb - yL, BLUE, .3, anim("y", [y0, yL], 3, None) + anim("height", [yb - y0, yb - yL], 3, None))
        b += liq(xr0, yR, xr1 - xr0, yb - yR, BLUE, .3, anim("y", [y0, yR], 3, None) + anim("height", [yb - y0, yb - yR], 3, None))
        b += liq(xl0, yT, xl1 - xl0, yL - yT, OIL, .4, anim("y", [y0, yT], 3, None) + anim("height", [0, yL - yT], 3, None))
    else:
        b += liq(xl0, yL, xl1 - xl0, yb - yL, BLUE, .3) + liq(xr0, yR, xr1 - xr0, yb - yR, BLUE, .3) + liq(xl0, yT, xl1 - xl0, yL - yT, OIL, .4)
    b += liq(xl1, 215, xr0 - xl1, 20, BLUE, .3)
    # thành ống chữ U
    b += f'<polyline fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" points="{xl0},34 {xl0},{yb} {xr1},{yb} {xr1},34"/>'
    b += f'<polyline fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" points="{xl1},34 {xl1},215 {xr0},215 {xr0},34"/>'
    b += txt((xl0 + xl1) / 2, 28, "S_1 = 30 cm²", "currentColor", 12, "middle", "400") + txt((xr0 + xr1) / 2, 28, "S_2 = 20 cm²", "currentColor", 12, "middle", "400")
    b += txt((xl0 + xl1) / 2, yT + 24, "dầu", "currentColor", 13, "middle", "400") + txt((xl0 + xl1) / 2, yL + 28, "nước", "currentColor", 13, "middle", "400")
    if kk == 0:
        b += txt(318, 70, "D_d = 800 kg/m³", "currentColor", 11, "start", "400") + txt(318, 88, "D_n = 1000 kg/m³", "currentColor", 11, "start", "400")
        b += txt(318, 120, "đề: dầu 25 cm", ORG, 12, "start", "700") + txt(318, 138, "hình: dầu 15 cm", "currentColor", 12, "start", "400")
        return fig("e2-0", "0 0 420 250", "Ống chữ U hai nhánh tiết diện khác nhau chứa nước, đổ dầu vào nhánh trái làm mực nước nhánh phải dâng lên",
                   b, "Mô phỏng: đổ dần dầu vào nhánh trái (cột dầu mẫu 15 cm để quan sát hiện tượng, không phải 25 cm của đề): nước ở nhánh phải dâng, hai mặt thoáng lệch nhau.")
    b += dashed(xl0 - 8, y0, xr1 + 8, y0, "currentColor", 1.2, .55) + txt(209, y0 - 6, "mức nước ban đầu", "currentColor", 11, "middle", "400")
    b += dashed(xl0 - 8, yL, xr1 + 8, yL, GRN, 1.8, .95)
    b += dot(124, yL, 4.5, GRN) + txt(116, yL - 8, "A", GRN, 14, "end") + dot(284, yL, 4.5, GRN) + txt(292, yL - 8, "B", GRN, 14)
    b += txt(209, yL + 16, "mặt phẳng chuẩn", GRN, 11, "middle", "400")
    b += dim(p, "o", xl0 - 22, yT + 1, xl0 - 22, yL - 1, "", 0, 0) + txt(xl0 - 28, (yT + yL) / 2 + 4, "h_d", ORG, 13, "end")
    b += dim(p, "b", xr1 + 28, yR + 1, xr1 + 28, yL - 1, "", 0, 0) + txt(xr1 + 34, (yR + yL) / 2 + 4, "h_n", BLUE, 13)
    b += txt(16, 232 + 14, "x : nước nhánh trái hạ · y : nước nhánh phải dâng · h_n = x + y", "currentColor", 11, "start", "400")
    return fig("e2-2", "0 0 420 252", "Ống chữ U: mặt phẳng chuẩn đi qua mặt phân cách dầu nước, hai điểm A và B nằm trên mặt phẳng đó",
               b, "Dữ kiện: A trên mặt phân cách (nhánh trái), B cùng độ cao trong nước (nhánh phải). Hình vẽ với dầu 15 cm ; đề là 25 cm. " + NOTE)


# ───────────── Dạng 3 · khối gỗ nổi (hình mẫu D = 500 kg/m³, chìm một nửa) ─────────────
def _block_float(x, ysurf, w=60, hpx=60, frac=.5):
    top = ysurf - hpx * (1 - frac)
    return top, hpx

def d3(kk):
    p = f"e3{kk}"
    if kk == 0:
        ys = 120; xb = 190; w = 60; hp = 60; frac = .5
        top = ys - hp * (1 - frac)
        b = defs(p) + liq(40, ys, 340, 70, BLUE, .3) + vessel(40, 380, 60, 190)
        b += dashed(40, ys, 380, ys, "currentColor", 1.2, .5)
        blk = R(xb, top, w, hp, "currentColor", 2.6, "#92400e", 0, "", 1).replace('fill="#92400e"', 'fill="#92400e" fill-opacity=".35"')
        b += f'<g>{anim_tr([(0, -64), (0, 0), (0, -8), (0, 0), (0, -2), (0, 0)], 2.4, "0;0.35;0.55;0.75;0.9;1")}{blk}</g>'
        b += txt(52, 84, "gỗ mẫu : D = 500 kg/m³", "currentColor", 11, "start", "400") + txt(52, 102, "nước : D = 1000 kg/m³", "currentColor", 11, "start", "400")
        b += txt(262, 40, "khối của đề : D = 700 kg/m³", ORG, 12, "start", "700")
        return fig("e3-0", "0 0 420 204", "Khối gỗ thả xuống mặt nước, dao động rồi nổi yên với một phần chìm trong nước",
                   b, "Mô phỏng: khối gỗ mẫu có D = 500 kg/m³ nên chìm một nửa ; khối gỗ của đề có D khác nên phần chìm khác. Chạy 2,4 s.")
    b = defs(p)
    # trái: nổi tự do, P và F_A bằng nhau (cân bằng) → hai vectơ cùng độ dài
    ys = 120; hp = 60; frac = .7; xb = 70; w = 60; top = ys - hp * (1 - frac)  # khối của đề: D=700, chìm 14/20 = 70%
    b += liq(8, ys, 190, 70, BLUE, .3) + vessel(8, 198, 70, 190) + dashed(8, ys, 198, ys, "currentColor", 1.2, .5)
    b += R(xb, top, w, hp, "currentColor", 2.6, "#92400e").replace('fill="#92400e"', 'fill="#92400e" fill-opacity=".35"')
    cy = top + hp / 2
    b += vec_luc("g", xb + w / 2, cy, 0, 1, 1, 40, 3)[0] + txt(xb + w / 2 + 22, cy + 40, "P", GRN)
    b += vec_luc("b", xb + w / 2, cy, 0, -1, 1, 40, 3)[0] + txt(xb + w / 2 + 22, cy - 30, "F_A", BLUE)
    b += dim(p, "r", xb + w + 14, ys + 1, xb + w + 14, top + hp - 1, "", 0, 0) + txt(xb + w + 20, ys + 20, "h_ch", RED, 13)
    b += txt(14, 40, "Nổi tự do : P = F_A", "currentColor", 13) + txt(14, 58, "(hai vectơ bằng nhau)", "currentColor", 11, "start", "400")
    # phải: quả cân đè, khối vừa chìm hết
    ox = 222; ys2 = 120; xb2 = ox + 100; top2 = ys2 - 4
    b += liq(ox, ys2, 190, 70, BLUE, .3) + vessel(ox, ox + 190, 70, 190) + dashed(ox, ys2, ox + 190, ys2, "currentColor", 1.2, .5)
    b += R(xb2, ys2, w, hp, "currentColor", 2.6, "#92400e").replace('fill="#92400e"', 'fill="#92400e" fill-opacity=".35"')
    b += R(xb2 + 14, ys2 - 24, 32, 24, "currentColor", 2.2, "#475569").replace('fill="#475569"', 'fill="#475569" fill-opacity=".5"') + txt(xb2 + 30, ys2 - 8, "m", "currentColor", 12, "middle")
    b += txt(ox + 6, 40, "Quả cân : chìm vừa hết", "currentColor", 13) + txt(ox + 6, 58, "F_A đạt cực đại", "currentColor", 11, "start", "400")
    b += dim(p, "o", xb2 - 14, ys2 + 1, xb2 - 14, ys2 + hp - 1, "", 0, 0) + txt(xb2 - 20, ys2 + 36, "h = 20 cm", ORG, 12, "end")
    return fig("e3-2", "0 0 420 204", "Bên trái khối gỗ nổi tự do với trọng lực và lực đẩy bằng nhau; bên phải quả cân đặt lên làm khối gỗ vừa chìm hoàn toàn",
               b, "Dữ kiện: nổi tự do thì P = F_A (vectơ bằng nhau) ; thêm quả cân đến khi chìm vừa hết thì lực đẩy cực đại. " + NOTE)


# ───────────── Dạng 4 · lực kế (quả cầu kim loại) + dây buộc đáy bình (khối nhựa) ─────────────
def d4(kk):
    p = f"e4{kk}"
    if kk == 0:
        b = defs(p)
        b += liq(130, 166, 160, 66, BLUE, .3) + vessel(130, 290, 126, 232) + dashed(130, 166, 290, 166, "currentColor", 1.2, .5)
        grp = (circ(210, 48, 4, "currentColor", 2) + R(195, 54, 30, 50, "currentColor", 2.4, "none", 3) + seg(210, 60, 210, 98, GREY, 3, "4 3")
               + seg(210, 104, 210, 170, "currentColor", 2) + circ(210, 186, 16, "currentColor", 2.6, "#64748b").replace('fill="#64748b"', 'fill="#64748b" fill-opacity=".55"')
               + txt(210, 83, "N", "currentColor", 12, "middle"))
        b += f'<g>{anim_tr([(0, -44), (0, 0)], 2.5)}{grp}</g>'
        b += txt(12, 40, "Trong không khí : 3,6 N", "currentColor", 12, "start", "400") + txt(12, 60, "Chìm trong nước : 2,4 N", "currentColor", 12, "start", "400")
        b += txt(12, 80, "Chìm trong chất lỏng X : 2,76 N", "currentColor", 12, "start", "400")
        b += txt(300, 166, "nước", BLUE, 13, "start", "700")
        return fig("e4-0", "0 0 420 240", "Quả cầu kim loại treo vào lực kế được hạ từ không khí xuống chìm hoàn toàn trong nước",
                   b, "Mô phỏng: hạ quả cầu từ không khí xuống chìm hoàn toàn trong nước (chạy 2,5 s). Số chỉ lực kế ghi theo đề.")
    b = defs(p)
    # trái: lực kế + quả cầu chìm trong nước, P và T vẽ đúng tỉ lệ (3,6 N và 2,4 N); lực đẩy chưa biết
    b += liq(10, 130, 190, 80, BLUE, .3) + vessel(10, 200, 90, 210) + dashed(10, 130, 200, 130, "currentColor", 1.2, .5)
    cx, cy = 100, 160; K = 14
    b += seg(cx, 26, cx, cy - 16, "currentColor", 2) + circ(cx, cy, 16, "currentColor", 2.6, "#64748b").replace('fill="#64748b"', 'fill="#64748b" fill-opacity=".55"')
    b += vec_luc("g", cx + 28, cy, 0, 1, 3.6, K, 3)[0] + txt(cx + 36, cy + 48, "P = 3,6 N", GRN, 12)
    b += vec_luc("r", cx + 28, cy, 0, -1, 2.4, K, 3)[0] + txt(cx + 36, cy - 30, "T = 2,4 N", RED, 12)
    b += txt(cx - 40, cy + 4, "F_A ↑ ?", BLUE, 13, "end")
    b += txt(14, 14, "Lực kế : P = T + F_A", "currentColor", 12, "start", "400")
    # phải: khối nhựa buộc dây vào đáy
    ox = 232
    b += liq(ox, 120, 180, 90, BLUE, .3) + vessel(ox, ox + 180, 90, 210) + dashed(ox, 120, ox + 180, 120, "currentColor", 1.2, .5)
    bx, by = ox + 70, 130
    b += seg(bx + 20, by + 40, bx + 20, 210, "currentColor", 2, "4 3") + R(bx, by, 40, 40, "currentColor", 2.6, "#d97706").replace('fill="#d97706"', 'fill="#d97706" fill-opacity=".4"')
    b += txt(bx + 28, by + 62, "dây", "currentColor", 12, "start", "400")
    b += txt(bx - 8, by + 14, "F_A ↑", BLUE, 13, "end") + txt(bx + 50, by + 12, "P ↓", GRN, 13) + txt(bx + 50, by + 30, "T ↓ (dây)", RED, 12)
    b += txt(ox + 6, 14, "Dây buộc đáy : F_A = P + T", "currentColor", 12, "start", "400")
    return fig("e4-2", "0 0 420 224", "Bên trái lực kế giữ quả cầu chìm trong nước; bên phải khối nhựa bị dây buộc xuống đáy bình",
               b, "Dữ kiện: lực kế kéo lên (P và T vẽ đúng tỉ lệ), dây buộc đáy kéo vật xuống ; lực đẩy chưa biết độ lớn nên chỉ ghi hướng. " + NOTE)


# ───────────── Dạng 5 · cục đá chứa mẩu sắt tan trong bình nước 0 °C ─────────────
def d5(kk):
    p = f"e5{kk}"
    if kk == 0:
        yw = 120; b = defs(p) + liq(130, yw, 160, 85, BLUE, .3) + vessel(130, 290, 70, 205)
        b += dashed(130, yw, 330, yw, "currentColor", 1.4, .6)
        ice = (f'<rect x="170" y="{yw - 6}" width="80" height="56" rx="5" fill="#e0f2fe" fill-opacity=".7" stroke="currentColor" stroke-width="2.4">'
               f'{anim("height", [56, 0, 0], 3, "0;0.7;1")}{anim("opacity", [1, 0.2, 0], 3, "0;0.7;1")}</rect>')
        iron = (f'<circle cx="210" cy="{yw + 22}" r="6" fill="#475569" stroke="currentColor" stroke-width="1.6">{anim("cy", [yw + 22, yw + 22, 197], 3, "0;0.4;1")}</circle>')
        b += ice + iron
        b += txt(300, yw + 4, "mực nước ban đầu", "currentColor", 12, "start", "400") + txt(300, yw + 24, "mực nước sau : ?", RED, 13)
        b += txt(12, 40, "đá 540 g (chưa kể sắt)", "currentColor", 13) + txt(12, 60, "gắn sắt 39 g ; nước, đá ở 0 °C", "currentColor", 12, "start", "400")
        return fig("e5-0", "0 0 420 214", "Cục nước đá chứa mẩu sắt nổi trong bình nước; đá tan dần và mẩu sắt chìm xuống đáy bình",
                   b, "Mô phỏng: đá tan hết, mẩu sắt rơi xuống đáy (chạy 3 s). Mực nước sau khi tan là điều cần tìm.")
    b = defs(p); yw = 112
    # trước
    b += liq(10, yw, 180, 90, BLUE, .3) + vessel(10, 190, 62, 202) + dashed(10, yw, 410, yw, "currentColor", 1.2, .55)
    b += R(60, yw - 6, 80, 56, "currentColor", 2.4, "#e0f2fe", 5).replace('fill="#e0f2fe"', 'fill="#e0f2fe" fill-opacity=".7"') + circ(100, yw + 22, 6, "currentColor", 1.6, "#475569")
    b += txt(100, yw - 14, "đá + sắt NỔI", "currentColor", 12, "middle", "700") + txt(14, 40, "Trước : P = F_A", "currentColor", 13)
    b += txt(100, 224, "V_1 = (m đá + m sắt) / D_n", ORG, 11, "middle")
    # sau
    b += liq(230, yw, 180, 90, BLUE, .3) + vessel(230, 410, 62, 202) + circ(320, 195, 6, "currentColor", 1.6, "#475569")
    b += txt(320, yw - 14, "nước mới + sắt CHÌM", "currentColor", 12, "middle", "700") + txt(234, 40, "Sau khi đá tan", "currentColor", 13)
    b += txt(320, 224, "V_2 = m đá / D_n + m sắt / D_s", ORG, 11, "middle") + txt(396, yw + 18, "?", RED, 15, "middle")
    return fig("e5-2", "0 0 420 234", "Trước khi tan đá và sắt nổi chung; sau khi tan nước mới chiếm thể tích theo khối lượng, sắt chìm chiếm thể tích thật",
               b, "Dữ kiện: trước đó cả hệ nổi (thể tích chiếm chỗ tính theo khối lượng), sau đó sắt chìm (thể tích chiếm chỗ tính theo thể tích thật). " + NOTE)


# ───────────── Dạng 6 · đòn bẩy AB = 40 cm, OA = 10 cm; vật 2 nhúng nước ─────────────
def _lever(p, y, oa_cm, scale=8, ax=40, tilt=0.0, water=False, blocks=True, label=True):
    """Thanh AB (40 cm) nằm ngang tại độ cao y, điểm tựa cách A `oa_cm` cm. Trả body."""
    ox = ax + oa_cm * scale; bx = ax + 40 * scale
    b = tri([(ox, y + 3), (ox - 16, y + 30), (ox + 16, y + 30)], "currentColor", 2.4) + seg(ox - 28, y + 30, ox + 28, y + 30, "currentColor", 3)
    b += seg(ax, y, bx, y, "currentColor", 6) + dot(ax, y, 5, "currentColor") + dot(bx, y, 5, "currentColor") + dot(ox, y, 3.5, BG_DOT)
    b += txt(ax - 4, y - 12, "A", "currentColor", 14, "middle") + txt(bx + 4, y - 12, "B", "currentColor", 14, "middle") + txt(ox, y - 12, "O", "currentColor", 14, "middle")
    return b, ox, bx
BG_DOT = "#f8fafc"

def d6(kk):
    p = f"e6{kk}"
    if kk == 0:
        y = 60; sc = 8; ax = 40; ox = ax + 10 * sc; bx = ax + 40 * sc
        th = math.radians(5)
        Ax, Ay = ox - 80 * math.cos(th), y + 80 * math.sin(th)
        Bx, By = ox + 240 * math.cos(th), y - 240 * math.sin(th)
        b = defs(p) + tri([(ox, y + 3), (ox - 16, y + 30), (ox + 16, y + 30)], "currentColor", 2.4) + seg(ox - 28, y + 30, ox + 28, y + 30, "currentColor", 3)
        b += liq(316, 140, 88, 82, BLUE, .3) + vessel(316, 404, 120, 222) + dashed(316, 140, 404, 140, "currentColor", 1.2, .5)
        # thanh + dây + vật chuyển theo góc nghiêng 5° (nội suy tuyến tính, góc nhỏ)
        b += (f'<line x1="{ax}" y1="{y}" x2="{bx}" y2="{y}" stroke="currentColor" stroke-width="6">'
              f'{anim("x1", [ax, Ax], 2.5)}{anim("y1", [y, Ay], 2.5)}{anim("x2", [bx, Bx], 2.5)}{anim("y2", [y, By], 2.5)}</line>')
        l1 = seg(ax, y, ax, y + 40, GREY, 2.4) + R(ax - 16, y + 40, 32, 30, "currentColor", 2.6, "#64748b").replace('fill="#64748b"', 'fill="#64748b" fill-opacity=".5"') + txt(ax, y + 60, "300 g", "currentColor", 11, "middle", "700")
        b += f'<g>{anim_tr([(0, 0), (Ax - ax, Ay - y)], 2.5)}{l1}</g>'
        l2 = seg(bx, y, bx, 190, GREY, 2.4) + R(bx - 14, 190, 28, 26, "currentColor", 2.6, "#92400e").replace('fill="#92400e"', 'fill="#92400e" fill-opacity=".45"') + txt(bx, 207, "vật 2", "currentColor", 11, "middle", "700")
        b += f'<g>{anim_tr([(0, 0), (Bx - bx, By - y)], 2.5)}{l2}</g>'
        b += dot(ox, y, 4, "currentColor") + txt(ax, y - 12, "A", "currentColor", 14, "middle") + txt(bx, y - 22, "B", "currentColor", 14, "middle") + txt(ox, y + 50, "O", "currentColor", 14, "middle")
        b += txt(12, 160, "OA = 10 cm", BLUE, 13) + txt(12, 180, "AB = 40 cm", BLUE, 13) + txt(12, 210, "vật 2 nhúng chìm hoàn toàn", "currentColor", 12, "start", "400")
        return fig("e6-0", "0 0 420 232", "Đòn bẩy treo một vật ở đầu A và một vật nhúng chìm trong nước ở đầu B; thanh nghiêng về phía đầu A",
                   b, "Mô phỏng chiều quay (góc nghiêng phóng đại): khi vật 2 chìm trong nước, đầu B nhẹ đi nên đầu A hạ xuống. Chưa dời điểm tựa. Chạy 2,5 s.")
    b = defs(p); sc = 8; ax = 70
    # trước khi nhúng: P1 vẽ đúng tỉ lệ (3 N, k = 18 px/N); P2 chưa biết
    y1 = 80; bd, ox, bx = _lever(p, y1, 10, sc, ax)
    b += bd + vec_luc("g", ax, y1 + 2, 0, 1, 3, 18, 3)[0] + txt(ax - 8, y1 + 34, "P_1 = 3 N", GRN, 12, "end")
    b += txt(bx + 22, y1 + 36, "P_2 = ?", RED, 13, "end") + seg(bx, y1 + 2, bx, y1 + 14, GREY, 2)
    b += dim(p, "b", ax, y1 + 64, ox, y1 + 64, "", 0, 0) + txt((ax + ox) / 2, y1 + 82, "OA = 10 cm", BLUE, 12, "middle")
    b += dim(p, "b", ox, y1 + 64, bx, y1 + 64, "", 0, 0) + txt((ox + bx) / 2, y1 + 82, "OB = 30 cm", BLUE, 12, "middle")
    b += txt(12, 24, "Trước : vật 2 trong không khí", "currentColor", 13)
    # sau khi nhúng: O dời về phía A 2 cm
    y2 = 232; bd, ox2, bx2 = _lever(p, y2, 8, sc, ax)
    b += bd + vec_luc("g", ax, y2 + 2, 0, 1, 3, 18, 3)[0] + txt(ax - 8, y2 + 34, "P_1 = 3 N", GRN, 12, "end")
    b += txt(bx2 + 22, y2 + 36, "P_2′ = ?", RED, 13, "end") + txt(bx2 - 14, y2 - 26, "F_A ↑ ?", BLUE, 13, "end")
    b += dim(p, "b", ax, y2 + 64, ox2, y2 + 64, "", 0, 0) + txt((ax + ox2) / 2, y2 + 82, "O′A = 8 cm", BLUE, 12, "middle")
    b += dim(p, "b", ox2, y2 + 64, bx2, y2 + 64, "", 0, 0) + txt((ox2 + bx2) / 2, y2 + 82, "O′B = 32 cm", BLUE, 12, "middle")
    b += txt(12, 190, "Sau : vật 2 nhúng nước, dời O về phía A 2 cm", "currentColor", 13)
    return fig("e6-2", "0 0 420 346", "Đòn bẩy trước và sau khi nhúng vật 2 vào nước; điểm tựa dời về phía A hai xentimét",
               b, "Dữ kiện: P₁ vẽ đúng tỉ lệ ; P₂, P₂′ và F_A chưa biết nên chỉ ghi ký hiệu. Dời O thì cả hai cánh tay đòn đều đổi. " + NOTE)


BUILD = [d1, d2, d3, d4, d5, d6]


# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
T_AP = "Khối lượng riêng và áp suất chất lỏng theo độ sâu"
T_FA = "Lực đẩy Archimedes và điều kiện nổi"

DANG = [
 dict(label="Dạng 1 · Dễ · Áp suất chất lỏng nhiều lớp, áp lực lên đáy và lên nắp ở thành bình",
      topic=T_AP,
      problem_html=r"""<p>Một bình hình trụ thẳng đứng, đáy nằm ngang có diện tích $S=200\ \text{cm}^2$, chứa hai lớp chất lỏng không hòa tan: lớp nước dày $40\ \text{cm}$ ở dưới và lớp dầu dày $20\ \text{cm}$ nổi phía trên. Khối lượng riêng của nước là $1000\ \text{kg/m}^3$, của dầu là $800\ \text{kg/m}^3$. Bình để hở; chỉ tính áp suất do hai lớp chất lỏng gây ra, bỏ qua áp suất khí quyển. Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính áp suất do chất lỏng gây ra tại đáy bình.</li><li>Tính áp lực của chất lỏng lên đáy bình.</li><li>Ở thành bình có một lỗ tròn diện tích $5\ \text{cm}^2$, tâm lỗ cách đáy $10\ \text{cm}$, được bịt kín bằng một nắp. Tính lực tối thiểu cần giữ để nắp không bị bật ra (coi áp suất tại mọi điểm của lỗ bằng áp suất tại tâm lỗ).</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Bình thông nhau chứa hai chất lỏng không hòa tan (tiết diện hai nhánh khác nhau)",
      topic=T_AP,
      problem_html=r"""<p>Một ống chữ U có hai nhánh hình trụ thẳng đứng, tiết diện nhánh trái $S_1=30\ \text{cm}^2$, nhánh phải $S_2=20\ \text{cm}^2$. Ban đầu ống chứa nước, mỗi nhánh có cột nước cao $40\ \text{cm}$ tính từ đáy ống, hai mặt thoáng ngang nhau. Người ta đổ dầu ($D_d=800\ \text{kg/m}^3$) vào nhánh trái cho tới khi cột dầu cao $h_d=25\ \text{cm}$. Dầu không hòa tan và không chảy sang nhánh phải ; $D_n=1000\ \text{kg/m}^3$.</p><ol type="a"><li>Tính độ cao $h_n$ của cột nước ở nhánh phải, tính từ mặt phân cách dầu – nước ở nhánh trái.</li><li>Mực nước ở nhánh phải dâng thêm bao nhiêu so với trước khi đổ dầu?</li><li>Mặt thoáng ở nhánh nào cao hơn và cao hơn bao nhiêu?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Vật nổi: phần chìm, quả cân đè và mực nước dâng trong bình",
      topic=T_FA,
      problem_html=r"""<p>Một khối gỗ hình hộp chữ nhật có đáy diện tích $S_g=40\ \text{cm}^2$, cao $h=20\ \text{cm}$, khối lượng riêng $D_g=700\ \text{kg/m}^3$. Khối gỗ được thả nổi thẳng đứng (đáy nằm ngang) trong một bình trụ có diện tích đáy $S=160\ \text{cm}^2$, ban đầu chứa nước sâu $30\ \text{cm}$ (nước không tràn, khối gỗ không chạm đáy bình). Lấy $D_n=1000\ \text{kg/m}^3$, $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính chiều cao phần khối gỗ chìm trong nước.</li><li>Đặt lên mặt trên khối gỗ một quả cân để khối gỗ vừa chìm hoàn toàn (mặt trên ngang mặt nước). Tính khối lượng tối thiểu của quả cân.</li><li>Khi chưa đặt quả cân, mực nước trong bình dâng thêm bao nhiêu so với trước khi thả khối gỗ?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Vật chịu thêm lực căng: lực kế (trọng lượng biểu kiến) và dây buộc đáy bình",
      topic=T_FA,
      problem_html=r"""<p>Một quả cầu đặc bằng kim loại được treo vào lực kế. Lực kế chỉ $3{,}6\ \text{N}$ khi quả cầu ở trong không khí, chỉ $2{,}4\ \text{N}$ khi quả cầu chìm hoàn toàn trong nước và chỉ $2{,}76\ \text{N}$ khi chìm hoàn toàn trong chất lỏng X. Lấy $D_n=1000\ \text{kg/m}^3$, $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính thể tích và khối lượng riêng của quả cầu.</li><li>Tính khối lượng riêng của chất lỏng X.</li><li>Một khối nhựa có thể tích $500\ \text{cm}^3$ và khối lượng $200\ \text{g}$ được buộc vào đáy bình nước bằng một sợi dây nhẹ, không giãn, khối nhựa chìm hoàn toàn. Tính lực căng của dây.</li><li>Cắt dây, khối nhựa nổi lên và nằm yên trên mặt nước. Tính thể tích phần khối nhựa chìm trong nước.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Biến thiên mực nước: cục đá chứa dị vật tan hết",
      topic=T_FA,
      problem_html=r"""<p>Một bình trụ có diện tích đáy $S=85\ \text{cm}^2$ chứa nước ở $0\ ^\circ\text{C}$. Một cục nước đá khối lượng $540\ \text{g}$ (chưa kể mẩu sắt) có gắn một mẩu sắt khối lượng $39\ \text{g}$, nổi trong bình. Khối lượng riêng của nước là $1\ \text{g/cm}^3$, của nước đá là $0{,}9\ \text{g/cm}^3$, của sắt là $7{,}8\ \text{g/cm}^3$. Nước đá tan hết mà nhiệt độ vẫn là $0\ ^\circ\text{C}$.</p><ol type="a"><li>Tính thể tích nước bị cục đá (kèm mẩu sắt) chiếm chỗ lúc đầu.</li><li>Tính thể tích bị chiếm chỗ sau khi đá tan hết. Mực nước trong bình thay đổi bao nhiêu?</li><li>Nếu mẩu sắt được thay bằng mẩu sáp cùng khối lượng ($D=0{,}8\ \text{g/cm}^3$) thì mực nước sau khi đá tan thay đổi thế nào?</li></ol>"""),
 dict(label="Dạng 6 · Nâng cao · Đòn bẩy kết hợp lực đẩy Archimedes: bài ngược tìm khối lượng riêng",
      topic=T_FA,
      problem_html=r"""<p>Thanh AB dài $40\ \text{cm}$, khối lượng không đáng kể, được treo vật 1 khối lượng $300\ \text{g}$ ở đầu A và vật 2 (đặc, chưa biết khối lượng) ở đầu B bằng hai sợi dây nhẹ. Thanh nằm ngang cân bằng khi điểm tựa O cách A $10\ \text{cm}$. Sau đó nhúng chìm hoàn toàn vật 2 trong một bình nước (vật không chạm đáy): thanh mất cân bằng, và muốn thanh nằm ngang trở lại phải dời điểm tựa về phía A thêm $2\ \text{cm}$. Lấy $D_n=1000\ \text{kg/m}^3$, $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính khối lượng của vật 2.</li><li>Tính khối lượng riêng của chất liệu làm vật 2.</li></ol>"""),
]


# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [(r'"hai lớp chất lỏng không hòa tan … nước dày $40$ cm, dầu dày $20$ cm nổi phía trên"', r"$h_n=40$ cm ; $h_d=20$ cm", r"⚠ Hai lớp chồng nhau : áp suất tại đáy là tổng áp suất của từng lớp"),
  (r'"khối lượng riêng nước $1000$, dầu $800$ kg/m³"', r"$D_n=1000$ ; $D_d=800$ kg/m³", r"$d=10D$ ; $p=d\,h$"),
  (r'"bỏ qua áp suất khí quyển"', r"Chỉ tính $p$ do chất lỏng", r"⚠ $h$ đo từ mặt thoáng (hoặc từ mặt phân cách, với lớp bên dưới) xuống điểm xét, không đo từ đáy lên"),
  (r'"áp suất … tại đáy bình"', r"Cần $p_{đáy}$", r"$p=d_dh_d+d_nh_n$"),
  (r'"áp lực … lên đáy ; $S=200$ cm²"', r"$S=200$ cm²", r"$F=p\,S$ ; đổi cm² ra m²"),
  (r'"lỗ tròn $5$ cm², tâm lỗ cách đáy $10$ cm"', r"$S_l=5$ cm² ; cách đáy $10$ cm", r"Lỗ nằm trong lớp nước ; độ sâu tính từ mặt thoáng ; $F=p_l\,S_l$"),
  (r'"lực tối thiểu giữ nắp"', r"Cần $F$", r"Lực giữ bằng áp lực chất lỏng lên nắp : $F=p_l\,S_l$")],
 [(r'"ống chữ U … nước … đổ dầu vào nhánh trái"', r"Hai chất lỏng không hòa tan", r"⚠ Chỉ cùng một chất lỏng đứng yên mới có mặt thoáng ngang nhau ; ở đây hai mặt thoáng lệch nhau"),
  (r'"tiết diện $S_1=30$ cm², $S_2=20$ cm²"', r"$S_1=30$ cm² ; $S_2=20$ cm²", r"⚠ Tiết diện khác nhau : nước hạ $x$ ở nhánh trái, dâng $y$ ở nhánh phải với $S_1x=S_2y$ (không phải $x=y$)"),
  (r'"cột dầu cao $h_d=25$ cm"', r"$h_d=25$ cm ; $D_d=800$ ; $D_n=1000$ kg/m³", r"Mặt phẳng chuẩn qua mặt phân cách ; $p_A=d_dh_d$"),
  (r'"độ cao $h_n$ của cột nước ở nhánh phải"', r"Cần $h_n$", r"$p_B=d_nh_n$ ; $p_A=p_B$"),
  (r'"mực nước ở nhánh phải dâng thêm"', r"Cần $y$", r"$h_n=x+y$ ; $S_1x=S_2y$"),
  (r'"mặt thoáng ở nhánh nào cao hơn"', r"So $h_d$ với $h_n$", r"Hai mặt thoáng cách mặt phẳng chuẩn lần lượt $h_d$ và $h_n$")],
 [(r'"thả nổi thẳng đứng"', r"Cân bằng : hợp lực bằng 0", r"⚠ Vật nổi : $P=F_A$ với $F_A$ tính theo thể tích phần CHÌM $V_{ch}$, không phải cả khối"),
  (r'"$S_g=40$ cm², $h=20$ cm, $D_g=700$ kg/m³"', r"$S_g=40$ cm² ; $h=20$ cm ; $D_g=700$ kg/m³", r"$P=10D_gS_gh$ ; $F_A=10D_nS_gh_{ch}$"),
  (r'"chiều cao phần khối gỗ chìm"', r"Cần $h_{ch}$", r"$P=F_A\Rightarrow\dfrac{h_{ch}}{h}=\dfrac{D_g}{D_n}$"),
  (r'"quả cân … vừa chìm hoàn toàn"', r"$V_{ch}=V$ (cả khối)", r"⚠ $F_A$ cực đại khi chìm hết : $P_{gỗ}+P_{cân}=F_{A(max)}$"),
  (r'"khối lượng tối thiểu của quả cân"', r"Cần $m$", r"$P_{cân}=F_{A(max)}-P_{gỗ}$ ; $m=\dfrac{P_{cân}}{10}$"),
  (r'"bình trụ $S=160$ cm², nước sâu $30$ cm"', r"$S=160$ cm²", r"Nước dâng vì bị vật chiếm chỗ : $\Delta h=\dfrac{V_{ch}}{S}$ (tiết diện BÌNH)"),
  (r'"mực nước dâng thêm"', r"Cần $\Delta h$", r"$V_{ch}=S_g\,h_{ch}$")],
 [(r'"treo vào lực kế … nhúng chìm hoàn toàn"', r"$P=3{,}6$ N ; $P_{bk}=2{,}4$ N", r"⚠ Số chỉ lực kế khi nhúng là trọng lượng biểu kiến $P-F_A$, không phải lực đẩy"),
  (r'"chìm hoàn toàn trong chất lỏng X … $2{,}76$ N"', r"$P_2=2{,}76$ N ; cùng thể tích $V$", r"Cùng vật, cùng chìm hết nên $V$ không đổi ; chỉ khối lượng riêng chất lỏng khác"),
  (r'"thể tích và khối lượng riêng của quả cầu"', r"Cần $V$, $D$", r"$F_A=10D_nV$ ; $D=\dfrac{m}{V}$ với $m=\dfrac{P}{10}$"),
  (r'"khối lượng riêng của chất lỏng X"', r"Cần $D_X$", r"$P-P_2=10D_XV$"),
  (r'"buộc vào đáy bình … chìm hoàn toàn"', r"$V=500$ cm³ ; $m=200$ g", r"⚠ Dây buộc ở đáy kéo vật XUỐNG (vật nhẹ hơn nước) : $F_A=P+T$"),
  (r'"lực căng của dây"', r"Cần $T$", r"$T=F_A-P$ với $F_A=10D_nV$"),
  (r'"cắt dây … nằm yên trên mặt nước"', r"Cần $V_{ch}$", r"⚠ Hết dây : $P=F_A'$ với $F_A'=10D_nV_{ch}$")],
 [(r'"cục nước đá 540 g (chưa kể mẩu sắt) có gắn mẩu sắt 39 g, nổi trong bình"', r"$m_đ=540$ g ; $m_s=39$ g", r"⚠ Cả hệ đang NỔI : $P=F_A$ nên thể tích chiếm chỗ là $\dfrac{m_đ+m_s}{D_n}$ (không phải tổng thể tích thật)"),
  (r'"nước $1$, nước đá $0{,}9$, sắt $7{,}8$ g/cm³"', r"$D_n=1$ ; $D_đ=0{,}9$ ; $D_s=7{,}8$ g/cm³", r"Sắt có $D_s\gt D_n$ nên sẽ chìm khi không còn đá giữ"),
  (r'"đá tan hết mà nhiệt độ vẫn là $0\ ^\circ$C"', r"Nước mới có $D=1$ g/cm³", r"⚠ Khối lượng không đổi khi tan : nước mới chiếm $\dfrac{m_đ}{D_n}$"),
  (r'"thể tích nước bị chiếm chỗ lúc đầu"', r"Cần $V_1$", r"$V_1=\dfrac{m_đ+m_s}{D_n}$"),
  (r'"thể tích bị chiếm chỗ sau khi đá tan"', r"Cần $V_2$", r"$V_2=\dfrac{m_đ}{D_n}+\dfrac{m_s}{D_s}$ (sắt chìm chiếm thể tích thật)"),
  (r'"mực nước thay đổi bao nhiêu ; $S=85$ cm²"', r"$S=85$ cm²", r"$\Delta h=\dfrac{V_1-V_2}{S}$"),
  (r'"thay bằng mẩu sáp cùng khối lượng"', r"$D_{sáp}\lt D_n$", r"Vật nhẹ hơn nước tự nổi : vẫn chiếm chỗ $\dfrac{m}{D_n}$ như lúc còn trong đá")],
 [(r'"thanh AB dài $40$ cm … khối lượng không đáng kể … O cách A $10$ cm"', r"$AB=40$ cm ; $OA=10$ cm ; $OB=30$ cm", r"⚠ Bỏ qua khối lượng thanh : chỉ xét mômen của hai lực tại A, B ; cánh tay đòn tính từ điểm tựa O"),
  (r'"vật 1 khối lượng $300$ g ở đầu A"', r"$m_1=300$ g", r"$P_1=10m_1$ ; $P_1\cdot OA=P_2\cdot OB$"),
  (r'"vật 2 (đặc, chưa biết khối lượng) ở đầu B"', r"Cần $m_2$", r"$P_2=\dfrac{P_1\cdot OA}{OB}$ ; $m_2=\dfrac{P_2}{10}$"),
  (r'"nhúng chìm hoàn toàn vật 2 trong nước"', r"$V_{ch}=V_2$", r"⚠ Lực kéo của dây ở B giảm đúng bằng $F_A$ : $P_2'=P_2-F_A$"),
  (r'"dời điểm tựa về phía A thêm $2$ cm"', r"$O'A=8$ cm ; $O'B=32$ cm", r"⚠ Dời O thì cả hai cánh tay đòn đều đổi : $O'A$ giảm, $O'B$ tăng cùng $2$ cm ; $P_1\cdot O'A=P_2'\cdot O'B$"),
  (r'"khối lượng riêng của chất liệu làm vật 2"', r"Cần $D_2$", r"$F_A=10D_nV_2$ ; $D_2=\dfrac{m_2}{V_2}$")],
]


# ═════════════ LỜI GIẢI (mỗi bước một khối, mỗi công thức một dòng) ═════════════
R1 = [r"<strong>Khái niệm:</strong> chất lỏng gây áp suất lên đáy, thành bình và mọi vật trong lòng nó.",
      r"<strong>Công thức:</strong> $p=d\,h=10D\,h$ ; áp lực $F=p\,S$.",
      r"Nhiều lớp không hòa tan chồng nhau : $p=d_1h_1+d_2h_2+\dots$",
      r"⚠ <strong>Điều kiện:</strong> $h$ đo từ mặt thoáng (hoặc từ mặt phân cách, với lớp bên dưới) xuống điểm xét ; $S$ đổi ra m²."]
R2 = [r"<strong>Khái niệm:</strong> hai điểm cùng độ cao trong cùng một chất lỏng đứng yên có áp suất bằng nhau.",
      r"<strong>Phương pháp:</strong> chọn mặt phẳng chuẩn qua mặt phân cách thấp nhất, lập $p_A=p_B$.",
      r"Bảo toàn thể tích nước : $S_1x=S_2y$ ; cột nước trên mặt phẳng chuẩn : $h_n=x+y$.",
      r"⚠ <strong>Điều kiện:</strong> hai chất lỏng không hòa tan ; chỉ cùng một chất lỏng mới có mặt thoáng ngang nhau."]
R3 = [r"<strong>Khái niệm:</strong> lực đẩy Archimedes $F_A=10D_{cl}V_{ch}$ hướng lên, $V_{ch}$ là thể tích phần chìm.",
      r"<strong>Điều kiện nổi:</strong> $P=F_A$ ; chìm hoàn toàn thì $F_A$ đạt cực đại $F_{A(max)}=10D_{cl}V$.",
      r"Khối hộp thẳng đứng : $\dfrac{h_{ch}}{h}=\dfrac{D_v}{D_{cl}}$ ; nước dâng $\Delta h=\dfrac{V_{ch}}{S_{bình}}$.",
      r"⚠ <strong>Điều kiện:</strong> $V_{ch}$ là phần CHÌM, không phải cả khối ; $S$ trong $\Delta h$ là tiết diện của BÌNH."]
R4 = [r"<strong>Khái niệm:</strong> trọng lượng biểu kiến (số chỉ lực kế khi nhúng) $P_{bk}=P-F_A$.",
      r"<strong>Vật chìm treo lực kế:</strong> $P=F_A+P_{bk}$ · <strong>Vật nhẹ bị dây buộc đáy:</strong> $F_A=P+T$.",
      r"$F_A=10D_{cl}V$ ; $D=\dfrac{m}{V}$ với $m=\dfrac{P}{10}$.",
      r"⚠ <strong>Điều kiện:</strong> xác định chiều của lực căng (lên hay xuống) trước khi lập phương trình cân bằng."]
R5 = [r"<strong>Khái niệm:</strong> vật nổi thì thể tích chiếm chỗ $V_{ch}=\dfrac{m}{D_n}$ (theo khối lượng) ; vật chìm chiếm chỗ đúng thể tích thật của nó.",
      r"<strong>Công thức:</strong> $\Delta h=\dfrac{V_{trước}-V_{sau}}{S}$ (dương là mực nước hạ).",
      r"Nước đá nguyên chất tan thành nước có thể tích đúng bằng phần chìm ban đầu.",
      r"⚠ <strong>Điều kiện:</strong> khối lượng không đổi khi tan ; chỉ dị vật chìm xuống đáy mới làm thể tích chiếm chỗ giảm."]
R6 = [r"<strong>Khái niệm:</strong> đòn bẩy cân bằng khi tổng mômen hai lực quanh điểm tựa bằng nhau.",
      r"<strong>Công thức:</strong> $P_1\cdot OA=P_2\cdot OB$ ; vật nhúng chìm : $P_2'=P_2-F_A$, $F_A=10D_nV$.",
      r"Khối lượng riêng $D=\dfrac{m}{V}$.",
      r"⚠ <strong>Điều kiện:</strong> bỏ qua khối lượng thanh ; dời điểm tựa làm cả hai cánh tay đòn đổi."]

SOLS = [
 sol(R1, [
  ("Áp suất của lớp dầu tại mặt phân cách", [P(r"Trọng lượng riêng của dầu $d_d=10D_d=8000\ \text{N/m}^3$, của nước $d_n=10000\ \text{N/m}^3$."),
     M(r"p_1=d_d\,h_d=8000\cdot0{,}2"), A(r"p_1=1600\ \text{Pa}")]),
  ("Áp suất tại đáy bình", [P(r"Cột nước dày $40\ \text{cm}$ gây thêm áp suất, cộng vào áp suất của lớp dầu:"),
     M(r"p_{đáy}=p_1+d_n\,h_n=1600+10000\cdot0{,}4"), A(r"p_{đáy}=5600\ \text{Pa}")]),
  ("Áp lực lên đáy bình", [P(r"Đổi $S=200\ \text{cm}^2=0{,}02\ \text{m}^2$:"), M(r"F_{đáy}=p_{đáy}\,S=5600\cdot0{,}02"), A(r"F_{đáy}=112\ \text{N}")]),
  ("Lực giữ nắp ở thành bình", [P(r"Tâm lỗ cách đáy $10\ \text{cm}$ nên nằm trong lớp nước, cách mặt phân cách $40-10=30\ \text{cm}$:"),
     M(r"p_l=p_1+d_n\cdot0{,}3=1600+10000\cdot0{,}3=4600\ \text{Pa}"), P(r"Đổi $S_l=5\ \text{cm}^2=5\cdot10^{-4}\ \text{m}^2$:"),
     M(r"F_l=p_l\,S_l=4600\cdot5\cdot10^{-4}"), A(r"F_l=2{,}3\ \text{N}")]),
  ("Kiểm tra", [P(r"Trọng lượng nước : $10\cdot1000\cdot0{,}02\cdot0{,}4=80\ \text{N}$ ; trọng lượng dầu : $10\cdot800\cdot0{,}02\cdot0{,}2=32\ \text{N}$."),
     P(r"Tổng $112\ \text{N}$ bằng áp lực lên đáy ✓ (bình trụ thẳng đứng thì áp lực lên đáy bằng trọng lượng chất lỏng)."),
     P(r"$p_l\lt p_{đáy}$ vì lỗ cao hơn đáy $10\ \text{cm}$ ✓. Tính $h$ từ đáy lên sẽ ra áp suất sai nhiều lần.")])],
  [r"a) $p_{đáy}=5600\ \text{Pa}$", r"b) $F_{đáy}=112\ \text{N}$", r"c) $F_l=2{,}3\ \text{N}$"],
  r"Nhận dạng: đề có <strong>nhiều lớp chất lỏng chồng nhau</strong> → cộng $d\,h$ của từng lớp ; <strong>độ sâu đo từ mặt thoáng</strong>, không đo từ đáy."),
 sol(R2, [
  ("Cột nước bên phải: cân bằng áp suất", [P(r"Mặt phẳng chuẩn là mặt phẳng ngang qua mặt phân cách dầu – nước ở nhánh trái (điểm A). Điểm B ở nhánh phải cùng độ cao, trong nước."),
     M(r"p_A=p_B\Rightarrow d_d\,h_d=d_n\,h_n"), M(r"h_n=\dfrac{d_d\,h_d}{d_n}=\dfrac{8000\cdot25}{10000}"), A(r"h_n=20\ \text{cm}")]),
  ("Nước ở nhánh phải dâng bao nhiêu", [P(r"Nước ở nhánh trái hạ $x$, nhánh phải dâng $y$ ; thể tích nước chuyển sang bằng nhau:"), M(r"S_1x=S_2y\Rightarrow x=\dfrac{S_2}{S_1}\,y"),
     P(r"Cột nước phía trên mặt phẳng chuẩn ở nhánh phải gồm cả đoạn nước hạ ở nhánh trái:"), M(r"h_n=x+y=y\left(1+\dfrac{S_2}{S_1}\right)"),
     M(r"y=\dfrac{h_n\,S_1}{S_1+S_2}=\dfrac{20\cdot30}{30+20}"), A(r"y=12\ \text{cm}")]),
  ("Độ chênh hai mặt thoáng", [P(r"Mặt thoáng dầu cách mặt phẳng chuẩn $h_d$, mặt thoáng nước cách mặt phẳng chuẩn $h_n$ :"),
     M(r"\Delta h=h_d-h_n=25-20"), A(r"\Delta h=5\ \text{cm}"), P(r"Mặt thoáng dầu ở nhánh trái cao hơn, vì dầu nhẹ hơn nước.")]),
  ("Kiểm tra", [P(r"Hạ ở nhánh trái : $x=h_n-y=8\ \text{cm}$ ; $S_1x=30\cdot8=240\ \text{cm}^3=S_2y=20\cdot12$ ✓."),
     P(r"Áp suất tại A : $8000\cdot0{,}25=2000\ \text{Pa}$ ; tại B : $10000\cdot0{,}2=2000\ \text{Pa}$ ✓."),
     P(r"Nếu coi $x=y$ sẽ ra $y=10\ \text{cm}$ và $S_1x\ne S_2y$ — trái bảo toàn thể tích.")])],
  [r"a) $h_n=20\ \text{cm}$", r"b) $y=12\ \text{cm}$", r"c) Mặt thoáng dầu (nhánh trái) cao hơn mặt thoáng nước $5\ \text{cm}$"],
  r"Nhận dạng: <strong>hai chất lỏng trong ống chữ U</strong> → mặt phẳng chuẩn qua mặt phân cách, $p_A=p_B$ ; <strong>tiết diện khác nhau</strong> → $S_1x=S_2y$."),
 sol(R3, [
  ("Phần khối gỗ chìm", [P(r"Gỗ nổi cân bằng, $P=F_A$ :"), M(r"10D_gS_gh=10D_nS_gh_{ch}"), M(r"h_{ch}=h\,\dfrac{D_g}{D_n}=20\cdot\dfrac{700}{1000}"), A(r"h_{ch}=14\ \text{cm}")]),
  ("Quả cân để khối gỗ vừa chìm hết", [P(r"Thể tích khối gỗ : $V=S_gh=40\cdot20=800\ \text{cm}^3=8\cdot10^{-4}\ \text{m}^3$."),
     M(r"P_{gỗ}=10D_gV=10\cdot700\cdot8\cdot10^{-4}=5{,}6\ \text{N}"), M(r"F_{A(max)}=10D_nV=10\cdot1000\cdot8\cdot10^{-4}=8\ \text{N}"),
     P(r"Vừa chìm hết : lực đẩy cực đại cân bằng trọng lượng gỗ cộng quả cân :"), M(r"P_{cân}=F_{A(max)}-P_{gỗ}=8-5{,}6=2{,}4\ \text{N}"),
     M(r"m=\dfrac{P_{cân}}{10}"), A(r"m=0{,}24\ \text{kg}=240\ \text{g}")]),
  ("Mực nước dâng trong bình", [P(r"Nước bị chiếm chỗ đúng bằng thể tích phần chìm :"), M(r"V_{ch}=S_gh_{ch}=40\cdot14=560\ \text{cm}^3"),
     P(r"Thể tích này dàn ra trên tiết diện cả bình :"), M(r"\Delta h=\dfrac{V_{ch}}{S}=\dfrac{560}{160}"), A(r"\Delta h=3{,}5\ \text{cm}")]),
  ("Kiểm tra", [P(r"Lực đẩy khi nổi : $10\cdot1000\cdot560\cdot10^{-6}=5{,}6\ \text{N}=P_{gỗ}$ ✓."),
     P(r"Mực nước mới $30+3{,}5=33{,}5\ \text{cm}\gt h_{ch}=14\ \text{cm}$ nên khối gỗ không chạm đáy ✓."),
     P(r"Dùng cả thể tích $800\ \text{cm}^3$ sẽ ra $\Delta h=5\ \text{cm}$ — lớn hơn thực tế, vì gỗ nổi chỉ chiếm chỗ phần chìm.")])],
  [r"a) $h_{ch}=14\ \text{cm}$", r"b) $m=240\ \text{g}$", r"c) $\Delta h=3{,}5\ \text{cm}$"],
  r"Nhận dạng: <strong>vật nổi thẳng đứng</strong> → $P=F_A$, $\dfrac{h_{ch}}{h}=\dfrac{D_v}{D_n}$ ; <strong>nước dâng trong bình</strong> → $\Delta h=\dfrac{V_{ch}}{S_{bình}}$."),
 sol(R4, [
  ("Lực đẩy của nước lên quả cầu", [P(r"Số chỉ lực kế khi nhúng là trọng lượng biểu kiến, nên lực đẩy là độ giảm số chỉ :"), M(r"F_{A1}=P-P_1=3{,}6-2{,}4"), A(r"F_{A1}=1{,}2\ \text{N}")]),
  ("Khối lượng riêng của quả cầu", [P(r"Quả cầu chìm hoàn toàn nên $V$ là thể tích quả cầu :"), M(r"V=\dfrac{F_{A1}}{10D_n}=\dfrac{1{,}2}{10\cdot1000}=1{,}2\cdot10^{-4}\ \text{m}^3=120\ \text{cm}^3"),
     M(r"m=\dfrac{P}{10}=0{,}36\ \text{kg}"), M(r"D=\dfrac{m}{V}=\dfrac{0{,}36}{1{,}2\cdot10^{-4}}"), A(r"D=3000\ \text{kg/m}^3")]),
  ("Khối lượng riêng của chất lỏng X", [P(r"Cùng quả cầu, cùng thể tích $V$ :"), M(r"F_{A2}=P-P_2=3{,}6-2{,}76=0{,}84\ \text{N}"),
     M(r"D_X=\dfrac{F_{A2}}{10V}=\dfrac{0{,}84}{10\cdot1{,}2\cdot10^{-4}}"), A(r"D_X=700\ \text{kg/m}^3")]),
  ("Lực căng dây giữ khối nhựa", [P(r"$V=500\ \text{cm}^3=5\cdot10^{-4}\ \text{m}^3$ ; $P=10m=2\ \text{N}$ ; lực đẩy khi chìm hết :"), M(r"F_A=10D_nV=10\cdot1000\cdot5\cdot10^{-4}=5\ \text{N}"),
     P(r"Dây buộc ở đáy kéo khối nhựa xuống, vật đứng yên :"), M(r"F_A=P+T\Rightarrow T=F_A-P=5-2"), A(r"T=3\ \text{N}")]),
  ("Cắt dây: phần chìm khi nổi yên", [P(r"Hết lực căng, vật nổi cân bằng :"), M(r"P=F_A'=10D_nV_{ch}"), M(r"V_{ch}=\dfrac{P}{10D_n}=\dfrac{2}{10\cdot1000}=2\cdot10^{-4}\ \text{m}^3"),
     A(r"V_{ch}=200\ \text{cm}^3")]),
  ("Kiểm tra", [P(r"Quả cầu : $D=3000\gt D_n$ nên chìm, đúng với đề ; $D_X=700\lt D_n$ nên lực đẩy trong X nhỏ hơn trong nước ✓ (số chỉ $2{,}76\gt2{,}4$)."),
     P(r"Khối nhựa : $D=\dfrac{0{,}2}{5\cdot10^{-4}}=400\lt D_n$ nên mới cần dây giữ chìm ✓. Phần chìm $\dfrac{200}{500}=40\%=\dfrac{D}{D_n}$ ✓."),
     P(r"Nhầm $F_{A1}$ bằng số chỉ $2{,}4\ \text{N}$ sẽ ra $V=240\ \text{cm}^3$ — gấp đôi.")])],
  [r"a) $V=120\ \text{cm}^3$ · $D=3000\ \text{kg/m}^3$", r"b) $D_X=700\ \text{kg/m}^3$", r"c) $T=3\ \text{N}$", r"d) $V_{ch}=200\ \text{cm}^3$"],
  r"Nhận dạng: <strong>số chỉ lực kế khi nhúng</strong> → $F_A=P-P_{bk}$ ; <strong>dây buộc đáy giữ vật nhẹ</strong> → $F_A=P+T$ (dây kéo xuống)."),
 sol(R5, [
  ("Thể tích chiếm chỗ lúc đầu", [P(r"Cả cục đá và mẩu sắt cùng nổi, $P=F_A$ :"), M(r"10(m_đ+m_s)=10D_nV_1"),
     M(r"V_1=\dfrac{m_đ+m_s}{D_n}=\dfrac{540+39}{1}"), A(r"V_1=579\ \text{cm}^3")]),
  ("Thể tích chiếm chỗ sau khi đá tan", [P(r"Đá tan thành nước, khối lượng giữ nguyên $540\ \text{g}$ ; nước ở $0\ ^\circ\text{C}$ có $D=1\ \text{g/cm}^3$ :"), M(r"V_{nước}=\dfrac{m_đ}{D_n}=540\ \text{cm}^3"),
     P(r"Mẩu sắt chìm xuống đáy, chiếm đúng thể tích thật của nó :"), M(r"V_s=\dfrac{m_s}{D_s}=\dfrac{39}{7{,}8}=5\ \text{cm}^3"),
     M(r"V_2=V_{nước}+V_s=540+5"), A(r"V_2=545\ \text{cm}^3")]),
  ("Mực nước thay đổi", [M(r"V_1-V_2=579-545=34\ \text{cm}^3"), M(r"\Delta h=\dfrac{V_1-V_2}{S}=\dfrac{34}{85}"), A(r"\Delta h=0{,}4\ \text{cm}"), P(r"Thể tích chiếm chỗ giảm nên mực nước <strong>hạ</strong> $0{,}4\ \text{cm}$ ($4\ \text{mm}$).")]),
  ("Thay sắt bằng sáp", [P(r"Sáp có $D=0{,}8\lt D_n$, sau khi đá tan sáp tự nổi, vẫn chiếm chỗ $\dfrac{m}{D_n}=39\ \text{cm}^3$ như lúc còn trong đá :"),
     M(r"V_2=540+39=579\ \text{cm}^3=V_1"), A("T:Mực nước <strong>không đổi</strong>.")]),
  ("Kiểm tra", [P(r"Hệ ban đầu nổi thật : khối lượng riêng trung bình $\dfrac{579}{600+5}\approx0{,}96\lt1$ ✓ (thể tích đá $\dfrac{540}{0{,}9}=600\ \text{cm}^3$)."),
     P(r"Công thức nhanh : $\Delta V=m_s\left(\dfrac{1}{D_n}-\dfrac{1}{D_s}\right)=39\cdot\left(1-\dfrac{1}{7{,}8}\right)=34\ \text{cm}^3$ ✓."),
     P(r"Cục đá nguyên chất (không dị vật) tan thì mực nước không đổi — hiệu ứng ở đây chỉ do mẩu sắt chìm.")])],
  [r"a) $V_1=579\ \text{cm}^3$", r"b) $V_2=545\ \text{cm}^3$ · mực nước hạ $0{,}4\ \text{cm}$", r"c) Mực nước không đổi"],
  r"Nhận dạng: <strong>đá tan có dị vật bên trong</strong> → dị vật nổi thì mực không đổi, dị vật chìm thì mực <strong>hạ</strong> một đoạn $\dfrac{m_s(1/D_n-1/D_s)}{S}$."),
 sol(R6, [
  ("Khối lượng vật 2 (cân bằng ban đầu)", [P(r"$P_1=10m_1=3\ \text{N}$ ; $OA=10\ \text{cm}$ ; $OB=40-10=30\ \text{cm}$ (hai cánh tay đòn cùng đơn vị nên lập tỉ số được ngay) :"),
     M(r"P_1\cdot OA=P_2\cdot OB\Rightarrow P_2=\dfrac{3\cdot10}{30}=1\ \text{N}"), M(r"m_2=\dfrac{P_2}{10}"), A(r"m_2=0{,}1\ \text{kg}=100\ \text{g}")]),
  ("Lực kéo ở B sau khi nhúng", [P(r"Dời O về phía A $2\ \text{cm}$ : $O'A=10-2=8\ \text{cm}$ ; $O'B=30+2=32\ \text{cm}$."),
     P(r"Thanh nằm ngang cân bằng trở lại, lực của dây ở B là $P_2'$ :"), M(r"P_1\cdot O'A=P_2'\cdot O'B"), M(r"P_2'=\dfrac{3\cdot8}{32}"), A(r"P_2'=0{,}75\ \text{N}")]),
  ("Lực đẩy Archimedes lên vật 2", [P(r"Nhúng nước làm lực kéo của dây ở B giảm đúng bằng lực đẩy :"), M(r"F_A=P_2-P_2'=1-0{,}75"), A(r"F_A=0{,}25\ \text{N}")]),
  ("Thể tích vật 2", [P(r"Vật chìm hoàn toàn nên $V_{ch}=V_2$ :"), M(r"V_2=\dfrac{F_A}{10D_n}=\dfrac{0{,}25}{10\cdot1000}=2{,}5\cdot10^{-5}\ \text{m}^3"), A(r"V_2=25\ \text{cm}^3")]),
  ("Khối lượng riêng của vật 2", [M(r"D_2=\dfrac{m_2}{V_2}=\dfrac{0{,}1}{2{,}5\cdot10^{-5}}"), A(r"D_2=4000\ \text{kg/m}^3")]),
  ("Kiểm tra", [P(r"$D_2=4000\gt D_n$ nên vật chìm hoàn toàn khi nhúng vào nước, phù hợp với đề."),
     P(r"Thế ngược : $P_2'\cdot O'B=0{,}75\cdot32=24=P_1\cdot O'A=3\cdot8$ ✓."),
     P(r"Quên đổi cánh tay đòn mới (giữ $OA=10$) thì ra $P_2'=1\ \text{N}$, $F_A=0$ — vô lí vì vật đã nhúng nước.")])],
  [r"a) $m_2=100\ \text{g}$", r"b) $D_2=4000\ \text{kg/m}^3$"],
  r"Nhận dạng: <strong>đòn bẩy có vật nhúng nước</strong> → lực kéo ở đầu đó giảm đúng $F_A$ ; <strong>dời điểm tựa</strong> → cả hai cánh tay đòn đổi."),
]


# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>nhiều lớp chất lỏng chồng nhau</b> → nghĩ tới <b>cộng d·h của từng lớp</b>, h đo từ mặt thoáng xuống.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Áp suất của lớp dầu tại mặt phân cách", "Áp suất do lớp dầu gây ra tại mặt phân cách là bao nhiêu?", 1600, "Pa", 10,
       loi=r"Quên đổi khối lượng riêng sang trọng lượng riêng ($d=10D$) nên ra áp suất nhỏ hơn 10 lần."),
  buoc("Áp suất tại đáy bình", "Áp suất do chất lỏng gây ra tại đáy bình là bao nhiêu?", 5600, "Pa", 30,
       loi=r"Coi cả cột $60\ \text{cm}$ là nước ($p=d_n\cdot0{,}6$), hoặc bỏ lớp dầu vì nó nằm phía trên.",
       ke=[(r"Cộng áp suất của hai lớp : $p=d_dh_d+d_nh_n$", True),
           (r"$p=d_n\,(h_d+h_n)$ coi cả cột chất lỏng là nước", r"Dầu nhẹ hơn nước ($d_d=8000\ \text{N/m}^3$) nên cột dầu gây áp suất nhỏ hơn cột nước cùng độ cao."),
           (r"$p=d_n\,h_n$ vì dầu nằm trên nước nên không đè xuống", r"Mọi lớp chất lỏng nằm phía trên điểm xét đều gây áp suất ; lớp dầu truyền áp suất xuống tận đáy.")]),
  buoc("Áp lực lên đáy bình", "Áp lực của chất lỏng lên đáy bình bằng bao nhiêu?", 112, "N", 1,
       loi=r"Giữ nguyên $S=200$ (cm²) khi nhân với áp suất tính bằng Pa nên ra kết quả sai $10^4$ lần.",
       ke=[(r"$F=p\,S$ với $S$ đổi ra $\text{m}^2$", True),
           (r"$F=\dfrac{p}{S}$", r"Áp suất là lực trên một đơn vị diện tích nên lực là tích $p\cdot S$, không phải thương."),
           (r"$F=p\,S$ với $S=200$ (giữ nguyên cm²)", r"Áp suất tính bằng Pa $=\text{N/m}^2$ nên diện tích phải đổi ra $\text{m}^2$ : $200\ \text{cm}^2=0{,}02\ \text{m}^2$.")]),
  buoc("Lực giữ nắp ở thành bình", "Lực tối thiểu giữ nắp bằng bao nhiêu?", 2.3, "N", 0.05,
       loi=r"Lấy độ sâu của lỗ là $10\ \text{cm}$ (khoảng cách tới đáy) hoặc dùng luôn áp suất tại đáy cho lỗ.",
       ke=[(r"Độ sâu đo từ mặt thoáng ; áp suất tại lỗ = áp suất lớp dầu + áp suất cột nước từ mặt phân cách xuống lỗ", True),
           (r"Độ sâu của lỗ là khoảng cách tới đáy nên $p=d_n\cdot0{,}1$", r"$h$ trong $p=d\,h$ đo từ mặt thoáng xuống điểm xét, không đo từ đáy lên."),
           (r"Lỗ ở sát đáy nên dùng luôn áp suất tại đáy", r"Lỗ cao hơn đáy nên áp suất nhỏ hơn áp suất tại đáy ; mỗi độ sâu có một áp suất riêng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>hai chất lỏng trong ống chữ U</b> → nghĩ tới <b>mặt phẳng chuẩn qua mặt phân cách, p_A = p_B</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cột nước bên phải: cân bằng áp suất", "Cột nước ở nhánh phải, tính từ mặt phẳng chuẩn, cao bao nhiêu?", 20, "cm", 0.3,
       loi=r"Lấy $h_n$ là độ cao mặt nước nhánh phải so với đáy ống, hoặc là phần nước dâng thêm $y$, thay vì cột nước tính từ mặt phẳng chuẩn."),
  buoc("Nước ở nhánh phải dâng bao nhiêu", "Nước ở nhánh phải dâng thêm bao nhiêu so với lúc đầu?", 12, "cm", 0.2,
       loi=r"Cho rằng nước hạ ở nhánh trái bằng nước dâng ở nhánh phải ($x=y$), hoặc coi cột nước $h_n$ chính là đoạn dâng $y$.",
       ke=[(r"Dùng $S_1x=S_2y$ và $h_n=x+y$", True),
           (r"$x=y$ vì nước chuyển từ nhánh này sang nhánh kia", r"Hai nhánh có tiết diện khác nhau nên thể tích nước chuyển bằng nhau chứ độ cao thì khác : $S_1x=S_2y$."),
           (r"$h_n=y$ vì chỉ nhánh phải có nước phía trên mặt phẳng chuẩn", r"Mặt phân cách ở nhánh trái đã hạ $x$ so với mức đầu nên cột nước trên mặt phẳng chuẩn là $x+y$.")]),
  buoc("Độ chênh hai mặt thoáng", "Mặt thoáng dầu cao hơn mặt thoáng nước bao nhiêu?", 5, "cm", 0.2,
       loi=r"Cho rằng bình thông nhau thì hai mặt thoáng luôn ngang nhau, hoặc trừ $h_d$ cho phần dâng $y$ thay vì cho $h_n$.",
       ke=[(r"$\Delta h=h_d-h_n$ vì hai mặt thoáng cách mặt phẳng chuẩn lần lượt $h_d$ và $h_n$", True),
           (r"$\Delta h=0$ vì bình thông nhau luôn có mặt thoáng ngang nhau", r"Nguyên tắc đó chỉ đúng với MỘT chất lỏng đứng yên ; ở đây có hai chất lỏng khác khối lượng riêng."),
           (r"$\Delta h=h_d-y$", r"$y$ là độ dâng so với mức ban đầu, không phải khoảng cách tới mặt phẳng chuẩn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>vật nổi thẳng đứng</b> → nghĩ tới <b>P = F_A</b>, h_ch/h = D_v/D_n ; <b>nước dâng</b> → chia cho tiết diện bình.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Phần khối gỗ chìm", "Chiều cao phần khối gỗ chìm trong nước là bao nhiêu?", 14, "cm", 0.2,
       loi=r"Đảo tỉ số ($h_{ch}=h\,D_n/D_g$) nên ra phần chìm lớn hơn cả chiều cao khối gỗ."),
  buoc("Quả cân để khối gỗ vừa chìm hết", "Khối lượng tối thiểu của quả cân là bao nhiêu?", 240, "g", 2,
       loi=r"Quên trọng lượng khối gỗ (coi $P_{cân}=F_{A(max)}$), hoặc nhầm đơn vị kg và g.",
       ke=[(r"$P_{gỗ}+P_{cân}=F_{A(max)}$ với $V_{ch}=V$ (cả khối)", True),
           (r"$P_{cân}=F_{A(max)}$", r"Lực đẩy phải nâng cả khối gỗ lẫn quả cân ; khối gỗ cũng có trọng lượng."),
           (r"$P_{cân}=P_{gỗ}$ (quả cân nặng bằng khối gỗ)", r"Khối lượng đó thừa ; điều kiện tối thiểu là tổng trọng lượng bằng đúng lực đẩy cực đại.")]),
  buoc("Mực nước dâng trong bình", "Mực nước trong bình dâng thêm bao nhiêu khi thả khối gỗ (chưa có quả cân)?", 3.5, "cm", 0.05,
       loi=r"Chia thể tích cả khối gỗ (thay vì phần chìm) hoặc chia cho tiết diện khối gỗ thay vì tiết diện bình.",
       ke=[(r"$\Delta h=\dfrac{V_{ch}}{S_{bình}}$ : thể tích phần chìm chia tiết diện bình", True),
           (r"$\Delta h=\dfrac{V_{gỗ}}{S_{bình}}$ : dùng thể tích cả khối", r"Gỗ nổi chỉ chiếm chỗ phần chìm, không phải cả khối."),
           (r"$\Delta h=h_{ch}$ : mực dâng bằng phần chìm", r"Thể tích bị chiếm chỗ dàn ra trên tiết diện cả bình nên mực dâng nhỏ hơn nhiều phần chìm.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>số chỉ lực kế khi nhúng</b> → <b>F_A = P − P_bk</b> ; thấy <b>dây buộc đáy</b> → <b>F_A = P + T</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Lực đẩy của nước lên quả cầu", "Lực đẩy Archimedes của nước tác dụng lên quả cầu là bao nhiêu?", 1.2, "N", 0.02,
       loi=r"Lấy chính số chỉ lực kế khi nhúng làm lực đẩy ; số đó là trọng lượng biểu kiến, lực đẩy là phần trọng lượng bị mất."),
  buoc("Khối lượng riêng của quả cầu", "Khối lượng riêng của quả cầu là bao nhiêu?", 3000, "kg/m³", 50,
       loi=r"Lấy trọng lượng chia thể tích (ra trọng lượng riêng), quên chia thêm 10 để ra khối lượng riêng.",
       ke=[(r"Tìm $V$ từ $F_A=10D_nV$, rồi $D=\dfrac{m}{V}$ với $m=\dfrac{P}{10}$", True),
           (r"$V$ từ $F_A=10D_nV$, rồi $D=\dfrac{P}{V}$", r"$\dfrac{P}{V}$ là trọng lượng riêng $d$ (N/m³) ; khối lượng riêng phải dùng $m=\dfrac{P}{10}$."),
           (r"$V=\dfrac{P_1}{10D_n}$ với $P_1$ là số chỉ lực kế khi nhúng", r"Số chỉ khi nhúng là trọng lượng biểu kiến $P-F_A$, không phải lực đẩy ; lực đẩy mới dùng để tìm $V$.")]),
  buoc("Khối lượng riêng của chất lỏng X", "Khối lượng riêng của chất lỏng X là bao nhiêu?", 700, "kg/m³", 10,
       loi=r"Lập tỉ số các số chỉ lực kế thay vì tỉ số các lực đẩy ; hoặc cho rằng thể tích quả cầu đổi khi sang chất lỏng khác.",
       ke=[(r"Cùng $V$ : $P-P_2=10D_XV$", True),
           (r"$D_X=D_n\cdot\dfrac{P_2}{P_1}$ (tỉ số số chỉ lực kế)", r"Phải so các lực đẩy ($P-P_2$ và $P-P_1$), không so số chỉ lực kế."),
           (r"Chất lỏng X nhẹ hơn nên $V$ cũng khác", r"Quả cầu chìm hoàn toàn nên $V$ không đổi ; chỉ khối lượng riêng chất lỏng khác.")]),
  buoc("Lực căng dây giữ khối nhựa", "Lực căng của dây giữ khối nhựa là bao nhiêu?", 3, "N", 0.05,
       loi=r"Lập $P=F_A+T$ như khi treo lực kế ; nhưng dây buộc ở đáy kéo vật xuống, vì vật nhẹ hơn nước.",
       ke=[(r"Dây kéo xuống : $F_A=P+T$", True),
           (r"$P=F_A+T$ như lực kế treo từ trên xuống", r"Dây buộc ở đáy bình kéo khối nhựa xuống, vật nhẹ hơn nước nên $F_A\gt P$."),
           (r"$T=F_A$ vì vật đứng yên", r"Vật còn chịu trọng lực $P$ hướng xuống nên $T=F_A-P$.")]),
  buoc("Cắt dây: phần chìm khi nổi yên", "Thể tích phần khối nhựa chìm khi nổi yên là bao nhiêu?", 200, "cm³", 2,
       loi=r"Cho rằng khối nhựa vẫn chìm hết ($V_{ch}=V$), hoặc tính $V_{ch}$ từ lực căng cũ.",
       ke=[(r"Nổi yên : $P=F_A'=10D_nV_{ch}$", True),
           (r"$V_{ch}=V$ vì vật vẫn ở trong nước", r"Sau khi cắt dây vật nổi lên, chỉ chìm một phần."),
           (r"$V_{ch}=\dfrac{T}{10D_n}$ vì lực đẩy giảm đúng bằng $T$", r"Lực đẩy mới phải cân bằng với trọng lượng $P$ của vật, không liên quan tới $T$ cũ.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>đá tan có dị vật bên trong</b> → nghĩ tới <b>dị vật nổi: mực không đổi ; dị vật chìm: mực hạ</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Thể tích chiếm chỗ lúc đầu", "Thể tích nước bị cục đá kèm mẩu sắt chiếm chỗ lúc đầu là bao nhiêu?", 579, "cm³", 1,
       loi=r"Cộng thể tích thật của đá và sắt ; nhưng cả hệ nổi, thể tích chiếm chỗ được tính theo khối lượng chia $D_n$."),
  buoc("Thể tích chiếm chỗ sau khi đá tan", "Sau khi đá tan hết, thể tích bị chiếm chỗ là bao nhiêu?", 545, "cm³", 1,
       loi=r"Giữ nguyên cho sắt thể tích chiếm chỗ cũ (khối lượng chia $D_n$), hoặc lấy thể tích nước mới bằng thể tích cục đá.",
       ke=[(r"Nước mới chiếm $\dfrac{m_đ}{D_n}$ ; sắt chìm chiếm thể tích thật $\dfrac{m_s}{D_s}$", True),
           (r"Sắt vẫn chiếm chỗ $\dfrac{m_s}{D_n}$ như lúc còn trong đá", r"Lúc đầu cả hệ nổi nên mới tính theo khối lượng ; sắt đã rơi xuống đáy thì chỉ chiếm đúng thể tích thật của nó."),
           (r"Nước mới chiếm $\dfrac{m_đ}{D_đ}$, bằng thể tích cục đá", r"Đá tan thành nước có cùng khối lượng nhưng khối lượng riêng lớn hơn, nên thể tích nhỏ hơn thể tích cục đá.")]),
  buoc("Mực nước thay đổi", "Mực nước trong bình hạ bao nhiêu?", 0.4, "cm", 0.02,
       loi=r"Chia thể tích còn lại cho $S$ thay vì chia độ giảm thể tích, hoặc kết luận mực nước không đổi như với đá nguyên chất.",
       ke=[(r"$\Delta h=\dfrac{V_1-V_2}{S}$ : độ giảm thể tích chiếm chỗ chia tiết diện bình", True),
           (r"$\Delta h=\dfrac{V_2}{S}$", r"Mực nước thay đổi theo độ GIẢM thể tích chiếm chỗ, không theo thể tích còn lại."),
           (r"Mực nước không đổi vì đá tan bù đúng phần đã chìm", r"Đúng với đá nguyên chất ; ở đây mẩu sắt rơi xuống đáy nên thể tích chiếm chỗ giảm.")]),
  buoc("Thay sắt bằng sáp", "Nếu thay mẩu sắt bằng mẩu sáp cùng khối lượng thì mực nước sau khi đá tan sẽ thế nào?",
       loi=r"Cho rằng dị vật nào cũng làm mực nước hạ ; chỉ dị vật chìm xuống đáy mới làm thể tích chiếm chỗ giảm.",
       lua_chon=[(r"Không đổi", True),
                 (r"Hạ xuống", r"Sáp nhẹ hơn nước nên nổi lên, vẫn chiếm chỗ $\dfrac{m}{D_n}$ như lúc còn trong đá ; thể tích chiếm chỗ không giảm."),
                 (r"Dâng lên", r"Đá tan bù đúng phần chìm của nó và sáp vẫn chiếm chỗ như cũ nên tổng không tăng.")],
       ke=[(r"Xét sáp có chìm hay nổi sau khi hết đá rồi so thể tích chiếm chỗ", True),
           (r"Dị vật nào cũng rơi xuống đáy khi hết đá giữ", r"Chỉ vật có $D\gt D_n$ mới chìm ; sáp $D=0{,}8\lt D_n$ tự nổi."),
           (r"Chỉ cần so khối lượng hai mẩu vì chúng bằng nhau", r"Thể tích chiếm chỗ còn phụ thuộc vật nổi hay chìm, không chỉ khối lượng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>vật nhúng nước trên đòn bẩy</b> → lực đầu đó <b>giảm F_A</b> ; <b>dời điểm tựa</b> → <b>cả hai cánh tay đòn đổi</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Khối lượng vật 2 (cân bằng ban đầu)", "Khối lượng của vật 2 là bao nhiêu?", 100, "g", 1,
       loi=r"Lập cân bằng với $OB=40\ \text{cm}$ (chiều dài thanh) thay vì $OB=AB-OA$, hoặc nhầm đơn vị kg và g."),
  buoc("Lực kéo ở B sau khi nhúng", "Sau khi nhúng và dời điểm tựa, lực của dây tác dụng lên đầu B là bao nhiêu?", 0.75, "N", 0.01,
       loi=r"Giữ cánh tay đòn cũ (khi đó lại ra đúng trọng lượng vật 2), hoặc chỉ dời một cánh tay đòn.",
       ke=[(r"Lập cân bằng mới với cánh tay đòn mới : $P_1\cdot O'A=P_2'\cdot O'B$", True),
           (r"Giữ cánh tay đòn cũ : $P_1\cdot OA=P_2'\cdot OB$", r"Điểm tựa đã dời nên $OA$ và $OB$ đều đã đổi ; giữ cũ thì chỉ trở lại trọng lượng ban đầu của vật 2."),
           (r"Chỉ $OB$ tăng $2\ \text{cm}$, còn $OA$ giữ $10\ \text{cm}$", r"Dời O về phía A thì $OA$ giảm $2\ \text{cm}$ và $OB$ tăng $2\ \text{cm}$ (tổng $AB$ không đổi).")]),
  buoc("Lực đẩy Archimedes lên vật 2", "Lực đẩy Archimedes tác dụng lên vật 2 là bao nhiêu?", 0.25, "N", 0.01,
       loi=r"Lấy lực đẩy bằng chính lực còn lại ở B, hoặc lẫn trọng lượng vật 1 vào phép trừ.",
       ke=[(r"Lực kéo ở B giảm đúng bằng lực đẩy : $F_A=P_2-P_2'$", True),
           (r"$F_A=P_2'$", r"$P_2'$ là lực còn lại sau khi trừ lực đẩy, không phải chính lực đẩy."),
           (r"$F_A=P_1-P_2'$", r"$P_1$ là trọng lượng vật ở đầu A, không liên quan tới lực đẩy lên vật 2.")]),
  buoc("Thể tích vật 2", "Thể tích của vật 2 là bao nhiêu?", 25, "cm³", 0.5,
       loi=r"Quên hệ số 10 trong $F_A=10D_nV$ nên ra thể tích lớn gấp 10 lần ; hoặc lấy $V=m_2/D_n$.",
       ke=[(r"Vật chìm hoàn toàn : $F_A=10D_nV_2$", True),
           (r"$V_2=\dfrac{m_2}{D_n}$", r"Đó là thể tích nước có cùng khối lượng với vật, chỉ đúng nếu vật có khối lượng riêng bằng nước."),
           (r"$V_2=\dfrac{F_A}{D_n}$", r"Thiếu hệ số 10 : $F_A=d_nV=10D_nV$, nên thể tích bị tính lớn gấp 10 lần.")]),
  buoc("Khối lượng riêng của vật 2", "Khối lượng riêng của chất liệu làm vật 2 là bao nhiêu?", 4000, "kg/m³", 50,
       loi=r"Dùng trọng lượng chia thể tích (ra trọng lượng riêng) hoặc nhầm khối lượng riêng của nước với của vật.",
       ke=[(r"$D_2=\dfrac{m_2}{V_2}$", True),
           (r"$D_2=\dfrac{P_2}{V_2}$", r"Đó là trọng lượng riêng (N/m³) ; khối lượng riêng dùng khối lượng $m_2$."),
           (r"$D_2=\dfrac{F_A}{10V_2}$", r"Biểu thức đó cho khối lượng riêng của chất lỏng (nước), vì $F_A=10D_nV_2$.")]),
  buoc("Kiểm tra")]),
]


# ═════════════ BÀI TẬP TỰ LUẬN (E, G, và D chưa thành dạng) — đề + hướng dẫn giải ═════════════
def L(*ps): return "".join(f"<p>{x}</p>" for x in ps)

TL = [
 ("Dễ", L(r"Một thợ lặn ở độ sâu $35\ \text{m}$ dưới biển. Khối lượng riêng của nước biển là $1030\ \text{kg/m}^3$, áp suất khí quyển trên mặt biển là $p_0=10^5\ \text{Pa}$. Tính áp suất toàn phần tác dụng lên bộ đồ lặn. Lấy $g=10\ \text{m/s}^2$."),
        L(r"$d=10D=10300\ \text{N/m}^3$ ; áp suất do nước : $p_n=d\,h=10300\cdot35=360500\ \text{Pa}$.", r"Áp suất toàn phần : $p=p_0+p_n=10^5+360500=460500\ \text{Pa}\approx4{,}6\cdot10^5\ \text{Pa}$.")),
 ("Dễ", L(r"Một bình hình trụ chứa dầu hỏa ($D=800\ \text{kg/m}^3$) cao $80\ \text{cm}$. Đáy bình có diện tích $150\ \text{cm}^2$. Tính áp suất và áp lực của dầu lên đáy bình."),
        L(r"$p=10D\,h=10\cdot800\cdot0{,}8=6400\ \text{Pa}$.", r"$F=p\,S=6400\cdot0{,}015=96\ \text{N}$.", r"Kiểm tra : trọng lượng dầu $10\cdot800\cdot0{,}015\cdot0{,}8=96\ \text{N}$ ✓ (bình trụ).")),
 ("Dễ", L(r"Một vật bằng kim loại, khi treo vào lực kế trong không khí thì lực kế chỉ $7{,}8\ \text{N}$, khi nhúng chìm hoàn toàn trong nước thì lực kế chỉ $6{,}8\ \text{N}$. Tính khối lượng riêng của kim loại. Lấy $D_n=1000\ \text{kg/m}^3$."),
        L(r"$F_A=7{,}8-6{,}8=1\ \text{N}$ ; $V=\dfrac{F_A}{10D_n}=\dfrac{1}{10^4}=10^{-4}\ \text{m}^3$.", r"$m=\dfrac{7{,}8}{10}=0{,}78\ \text{kg}$ ; $D=\dfrac{m}{V}=\dfrac{0{,}78}{10^{-4}}=7800\ \text{kg/m}^3$ (sắt).")),
 ("Dễ", L(r"Một khối gỗ hình hộp chữ nhật có đáy $60\ \text{cm}^2$, cao $15\ \text{cm}$, nổi thẳng đứng trong nước, phần nhô khỏi mặt nước cao $3\ \text{cm}$. Tính khối lượng riêng của gỗ."),
        L(r"Phần chìm : $h_{ch}=15-3=12\ \text{cm}$.", r"$P=F_A\Rightarrow D_g=D_n\dfrac{h_{ch}}{h}=1000\cdot\dfrac{12}{15}=800\ \text{kg/m}^3$.")),
 ("Trung bình", L(r"Một ống chữ U tiết diện mỗi nhánh $5\ \text{cm}^2$ chứa thủy ngân ($D=13600\ \text{kg/m}^3$). Đổ vào nhánh trái một cột nước cao $27{,}2\ \text{cm}$. Tính độ chênh lệch giữa hai mực thủy ngân."),
        L(r"Mặt phẳng chuẩn qua mặt phân cách nước – thủy ngân ở nhánh trái. Cột thủy ngân ở nhánh phải cao hơn mặt phẳng này một đoạn $\Delta h$.", r"$d_{Hg}\Delta h=d_nh_n\Rightarrow\Delta h=\dfrac{1000\cdot27{,}2}{13600}=2\ \text{cm}$.", r"Mực thủy ngân ở nhánh phải cao hơn nhánh trái $2\ \text{cm}$.")),
 ("Trung bình", L(r"Một ống chữ U chứa nước. Đổ dầu ($D=800\ \text{kg/m}^3$) vào nhánh trái, cột dầu cao $20\ \text{cm}$ ; đổ xăng ($D=700\ \text{kg/m}^3$) vào nhánh phải, cột xăng cao $10\ \text{cm}$. Tính độ chênh lệch giữa hai mặt phân cách nước – chất lỏng."),
        L(r"Áp suất do cột dầu : $d_dh_d=8000\cdot0{,}2=1600\ \text{Pa}$ ; do cột xăng : $d_xh_x=7000\cdot0{,}1=700\ \text{Pa}$.", r"Chênh áp suất $900\ \text{Pa}$ được cân bằng bởi cột nước : $d_n\Delta h=900\Rightarrow\Delta h=0{,}09\ \text{m}=9\ \text{cm}$.", r"Mặt phân cách ở nhánh trái (có dầu) thấp hơn mặt phân cách ở nhánh phải $9\ \text{cm}$.")),
 ("Trung bình", L(r"Một quả cầu bằng đồng có khối lượng $890\ \text{g}$ và thể tích ngoài $150\ \text{cm}^3$. Quả cầu rỗng hay đặc ? Thả vào nước nó nổi hay chìm ? Biết $D_{Cu}=8900\ \text{kg/m}^3$."),
        L(r"Thể tích đồng nếu đặc : $\dfrac{890}{8{,}9}=100\ \text{cm}^3\lt150\ \text{cm}^3$ nên quả cầu <strong>rỗng</strong> (phần rỗng $50\ \text{cm}^3$).", r"Khối lượng riêng trung bình : $\dfrac{890}{150}\approx5{,}93\ \text{g/cm}^3\gt1\ \text{g/cm}^3$ nên quả cầu <strong>chìm</strong>.")),
 ("Trung bình", L(r"Một khối gỗ hình lập phương cạnh $10\ \text{cm}$, $D=700\ \text{kg/m}^3$, được giữ chìm hoàn toàn trong dầu ($D_d=800\ \text{kg/m}^3$) bằng một sợi dây buộc vào đáy bình. Tính lực căng của dây."),
        L(r"$V=10^{-3}\ \text{m}^3$ ; $F_A=10\cdot800\cdot10^{-3}=8\ \text{N}$ ; $P=10\cdot700\cdot10^{-3}=7\ \text{N}$.", r"Dây kéo xuống : $T=F_A-P=1\ \text{N}$.")),
 ("Trung bình", L(r"Một khối băng hình lập phương nổi trên mặt biển. Phần nổi có thể tích $150\ \text{m}^3$. Biết $D_{băng}=900\ \text{kg/m}^3$, $D_{biển}=1030\ \text{kg/m}^3$. Tính thể tích toàn bộ khối băng."),
        L(r"Nổi cân bằng : $\dfrac{V_{ch}}{V}=\dfrac{D_{băng}}{D_{biển}}=\dfrac{900}{1030}$, nên phần nổi chiếm $1-\dfrac{900}{1030}=\dfrac{130}{1030}$ thể tích.", r"$V=150\cdot\dfrac{1030}{130}\approx1188{,}5\ \text{m}^3$.")),
 ("Trung bình", L(r"Một khối sắt khối lượng $1{,}56\ \text{kg}$ được treo vào lực kế rồi nhúng ngập hoàn toàn (không chạm đáy) vào một bình nước đặt trên cân. Trước khi nhúng, cân chỉ $2{,}5\ \text{kg}$. Số chỉ của lực kế và của cân thay đổi thế nào ? Biết $D_{sắt}=7800\ \text{kg/m}^3$."),
        L(r"$V=\dfrac{1{,}56}{7800}=2\cdot10^{-4}\ \text{m}^3$ ; $F_A=10\cdot1000\cdot2\cdot10^{-4}=2\ \text{N}$.", r"Lực kế giảm từ $15{,}6\ \text{N}$ xuống $13{,}6\ \text{N}$.", r"Nước tác dụng lên sắt lực đẩy $2\ \text{N}$ nên sắt tác dụng lại nước lực $2\ \text{N}$ hướng xuống : cân tăng thêm $2\ \text{N}$, tức chỉ $2{,}7\ \text{kg}$.")),
 ("Trung bình", L(r"Một bình thông nhau có hai nhánh hình trụ tiết diện $S_1=100\ \text{cm}^2$ và $S_2=200\ \text{cm}^2$ chứa nước. Thả nhẹ một khối gỗ khối lượng $1\ \text{kg}$ vào nhánh $S_1$, khối gỗ nổi. Mực nước ở mỗi nhánh dâng lên bao nhiêu ?"),
        L(r"Gỗ nổi nên $V_{ch}=\dfrac{m}{D_n}=1000\ \text{cm}^3$.", r"Nước hai nhánh thông nhau nên dâng cùng một đoạn : $\Delta h=\dfrac{V_{ch}}{S_1+S_2}=\dfrac{1000}{300}\approx3{,}33\ \text{cm}$.")),
 ("Trung bình", L(r"Một cục nước đá nguyên chất khối lượng $200\ \text{g}$ nổi trong một cốc nước hình trụ diện tích đáy $50\ \text{cm}^2$. Mực nước trong cốc thay đổi bao nhiêu khi đá tan hết ?"),
        L(r"Lúc đầu : $V_{ch}=\dfrac{200}{1}=200\ \text{cm}^3$. Sau khi tan : nước mới có thể tích $\dfrac{200}{1}=200\ \text{cm}^3$.", r"Hai thể tích bằng nhau nên mực nước <strong>không đổi</strong> ($\Delta h=0$).")),
 ("Khó", L(r"Một quả cầu rỗng, kín, làm từ $390\ \text{g}$ sắt ($D_s=7800\ \text{kg/m}^3$), có thể tích ngoài $500\ \text{cm}^3$. Quả cầu nổi hay chìm trong nước ? Tính thể tích phần rỗng. Với cùng lượng sắt đó, phần rỗng phải có thể tích tối thiểu bao nhiêu để quả cầu không chìm ?"),
        L(r"Thể tích sắt : $\dfrac{390}{7{,}8}=50\ \text{cm}^3$ ; phần rỗng : $500-50=450\ \text{cm}^3$.", r"$P=10\cdot0{,}39=3{,}9\ \text{N}$ ; $F_{A(max)}=10\cdot1000\cdot500\cdot10^{-6}=5\ \text{N}\gt P$ nên quả cầu <strong>nổi</strong>.", r"Không chìm khi $F_{A(max)}\ge P$ (dấu $=$ là lơ lửng) : $10D_nV_{ngoài}\ge10m\Rightarrow V_{ngoài}\ge\dfrac{390}{1}=390\ \text{cm}^3$.", r"Phần rỗng tối thiểu : $390-50=340\ \text{cm}^3$.")),
 ("Khó", L(r"Một khối gỗ hình lập phương cạnh $20\ \text{cm}$ nổi thẳng trong nước, phần chìm cao $18\ \text{cm}$.", r"a) Tính khối lượng riêng của gỗ.", r"b) Đổ dầu ($D_d=800\ \text{kg/m}^3$) lên trên mặt nước tới khi mặt dầu vừa ngang mặt trên khối gỗ. Khối gỗ vẫn nằm thẳng, đáy ngang. Tính chiều cao phần gỗ chìm trong nước và trong dầu."),
        L(r"a) $D_g=D_n\dfrac{h_{ch}}{a}=1000\cdot\dfrac{18}{20}=900\ \text{kg/m}^3$.", r"b) Gọi $h_n$, $h_d$ là chiều cao phần gỗ trong nước và trong dầu : $h_n+h_d=20\ \text{cm}$.", r"$P=F_{An}+F_{Ad}\Rightarrow D_ga=D_nh_n+D_dh_d$ : $900\cdot20=1000h_n+800(20-h_n)$.", r"$18000=200h_n+16000\Rightarrow h_n=10\ \text{cm}$, $h_d=10\ \text{cm}$.", r"Đổ thêm dầu cho mặt dầu cao hơn mặt trên khối gỗ thì kết quả không đổi, vì khối gỗ đã nằm hoàn toàn trong hai chất lỏng.")),
 ("Nâng cao", L(r"Một thanh đồng chất, tiết diện đều, dài $L=60\ \text{cm}$. Đầu trên O của thanh được gắn vào bản lề cố định đặt phía trên mặt nước ; thanh nghiêng so với mặt nước và đầu dưới A nhúng một phần trong nước. Khi cân bằng, thanh hợp với mặt nước góc $30^\circ$. Biết tỉ số khối lượng riêng của thanh và của nước là $\dfrac{D_t}{D_n}=0{,}5$. Tính chiều dài phần thanh ngập trong nước."),
        L(r"Gọi $x$ là chiều dài phần chìm (tính từ A). Trọng lực đặt ở trung điểm, cách O một đoạn $\dfrac{L}{2}$ ; lực đẩy đặt ở trung điểm phần chìm, cách O một đoạn $L-\dfrac{x}{2}$. Cả hai lực thẳng đứng nên cánh tay đòn lần lượt là $\dfrac{L}{2}\cos30^\circ$ và $\left(L-\dfrac{x}{2}\right)\cos30^\circ$ ($\cos30^\circ$ giản ước, góc nghiêng không ảnh hưởng kết quả).", r"$P\cdot\dfrac{L}{2}=F_A\left(L-\dfrac{x}{2}\right)$ với $P=10D_tSL$, $F_A=10D_nSx$ :", r"$D_t\dfrac{L^2}{2}=D_n\,x\left(L-\dfrac{x}{2}\right)\Rightarrow x^2-2Lx+L^2\dfrac{D_t}{D_n}=0$.", r"$x=L\left(1-\sqrt{1-\dfrac{D_t}{D_n}}\right)=60\left(1-\sqrt{0{,}5}\right)\approx17{,}6\ \text{cm}$ (nghiệm còn lại lớn hơn $L$ nên loại).")),
 ("Nâng cao", L(r"<strong>(Bình thông nhau có khoá đáy, thả vật nổi)</strong> Hai nhánh thẳng đứng tiết diện $S_1=100\ \text{cm}^2$ và $S_2=200\ \text{cm}^2$ được nối với nhau ở đáy bằng một ống nhỏ có khoá K (bỏ qua thể tích ống). Ban đầu K đóng : nhánh $S_1$ chứa nước ($D_n=1000\ \text{kg/m}^3$) cao $h_1=40\ \text{cm}$, nhánh $S_2$ chứa dầu ($D_d=800\ \text{kg/m}^3$) cao $h_2=30\ \text{cm}$.", r"a) Mở khoá K. Tính độ dịch chuyển của mặt thoáng mỗi nhánh khi chất lỏng cân bằng.", r"b) Sau đó thả vào nhánh $S_2$ một khối gỗ lập phương cạnh $10\ \text{cm}$, $D_g=600\ \text{kg/m}^3$. Mặt thoáng mỗi nhánh thay đổi thế nào so với trước khi thả gỗ ?"),
        L(r"a) Áp suất đáy : nhánh 1 là $4000\ \text{Pa}$, nhánh 2 là $2400\ \text{Pa}$ nên nước chảy sang nhánh 2, nằm dưới dầu. Gọi $x$ là độ hạ mực nước nhánh 1, $y$ là độ cao cột nước ở nhánh 2 : $S_1x=S_2y\Rightarrow x=2y$.", r"Cân bằng áp suất tại đáy : $1000(40-2y)=1000y+800\cdot30\Rightarrow y=\dfrac{16}{3}\approx5{,}33\ \text{cm}$, $x\approx10{,}67\ \text{cm}$.", r"Mặt thoáng nhánh 1 hạ $10{,}67\ \text{cm}$ ; mặt thoáng dầu nhánh 2 dâng $5{,}33\ \text{cm}$ (dầu giữ nguyên cột $30\ \text{cm}$, nước chui vào bên dưới).", r"b) Khối gỗ nổi trong dầu ($600\lt800$) : $V_{ch}=\dfrac{m}{D_d}=\dfrac{0{,}6}{800}=750\ \text{cm}^3$, tức phần chìm $7{,}5\ \text{cm}$, nhỏ hơn bề dày lớp dầu nên gỗ không chạm nước.", r"Gỗ làm tăng áp suất tại đáy nhánh 2 thêm $\dfrac{10m}{S_2}=\dfrac{6}{0{,}02}=300\ \text{Pa}$, đẩy nước từ nhánh 2 về nhánh 1. Gọi $\Delta h_1$ là độ dâng nhánh 1, $\Delta h_2$ là độ hạ mặt phân cách ở nhánh 2 : $\Delta h_1=2\Delta h_2$ và $d_n(\Delta h_1+\Delta h_2)=300$.", r"$30000\,\Delta h_2\ (\text{m})=300\Rightarrow\Delta h_2=1\ \text{cm}$, $\Delta h_1=2\ \text{cm}$.", r"Mặt thoáng dầu : dầu và gỗ chiếm cột cao $\dfrac{(S_2\cdot30+750)}{S_2}=33{,}75\ \text{cm}$ trên mặt phân cách, nên mặt thoáng dầu dâng $3{,}75-1=2{,}75\ \text{cm}$.", r"Kết quả : nhánh 1 dâng $2\ \text{cm}$ ; mặt thoáng dầu nhánh 2 dâng $2{,}75\ \text{cm}$.")),
 ("Nâng cao", L(r"<strong>(Hệ hai vật liên kết)</strong> Hai quả cầu đặc A và B cùng thể tích $V=100\ \text{cm}^3$ được nối bằng sợi dây mảnh, nhẹ, không giãn dài $20\ \text{cm}$ rồi thả vào chậu nước sâu. A bằng gỗ có $D_A=600\ \text{kg/m}^3$, B bằng kim loại có $D_B=2400\ \text{kg/m}^3$ ; $D_n=1000\ \text{kg/m}^3$.", r"a) Chứng minh hệ chìm xuống đáy.", r"b) Buộc thêm vào A một khối xốp có $D_x=100\ \text{kg/m}^3$ để hệ lơ lửng trong nước. Tính thể tích khối xốp.", r"c) Khi hệ lơ lửng, tính lực căng của dây nối A với B."),
        L(r"a) $P_A=10\cdot600\cdot10^{-4}=0{,}6\ \text{N}$ ; $P_B=2{,}4\ \text{N}$ ; tổng $3{,}0\ \text{N}$. Lực đẩy cực đại khi cả hai chìm hoàn toàn : $10\cdot1000\cdot2\cdot10^{-4}=2{,}0\ \text{N}\lt3{,}0\ \text{N}$ nên hệ chìm xuống đáy.", r"b) Lơ lửng khi tổng trọng lượng bằng tổng lực đẩy (xốp chìm hoàn toàn) : $3{,}0+1000V_x=2{,}0+10000V_x\Rightarrow V_x=\dfrac{1}{9000}\ \text{m}^3\approx111{,}1\ \text{cm}^3$.", r"c) Xét vật B : $F_{AB}+T=P_B\Rightarrow T=2{,}4-1{,}0=1{,}4\ \text{N}$.", r"Kiểm tra với A và xốp : lực đẩy $1{,}0+1{,}11=2{,}11\ \text{N}$, trọng lượng $0{,}6+0{,}11=0{,}71\ \text{N}$, hiệu $1{,}4\ \text{N}=T$ ✓.")),
 ("Nâng cao", L(r"<strong>(Đòn bẩy và lực đẩy)</strong> Thanh AB dài $40\ \text{cm}$, khối lượng không đáng kể, treo vật khối lượng $m_1=200\ \text{g}$ ở A và vật đặc khối lượng $m_2$ ở B ; thanh nằm ngang cân bằng khi điểm tựa O cách A $15\ \text{cm}$.", r"a) Tính $m_2$.", r"b) Nhúng ngập hoàn toàn vật $m_2$ trong nước ($D_n=1000\ \text{kg/m}^3$). Biết vật làm bằng chất có $D_2=4000\ \text{kg/m}^3$. Phải dời điểm tựa về phía nào và một đoạn bao nhiêu để thanh lại nằm ngang ?"),
        L(r"a) $P_1=2\ \text{N}$ ; $OB=40-15=25\ \text{cm}$ : $P_2=\dfrac{P_1\cdot OA}{OB}=\dfrac{2\cdot15}{25}=1{,}2\ \text{N}$, $m_2=120\ \text{g}$.", r"b) $V_2=\dfrac{0{,}12}{4000}=3\cdot10^{-5}\ \text{m}^3=30\ \text{cm}^3$ ; $F_A=10\cdot1000\cdot3\cdot10^{-5}=0{,}3\ \text{N}$ ; lực kéo ở B còn $P_2'=1{,}2-0{,}3=0{,}9\ \text{N}$.", r"Lực ở B giảm nên cánh tay đòn ở B phải dài ra : dời O về phía A. Đặt $O'A=x$ : $P_1x=P_2'(40-x)\Rightarrow2x=0{,}9(40-x)\Rightarrow x=\dfrac{36}{2{,}9}\approx12{,}41\ \text{cm}$.", r"Đoạn dời : $15-12{,}41\approx2{,}59\ \text{cm}$ về phía A.")),
 ("Nâng cao", L(r"<strong>(Thực hành)</strong> Phòng thực hành có một ống thủy tinh hình chữ U hai nhánh hở thẳng đứng, một thước thẳng có độ chia nhỏ nhất $1\ \text{mm}$, bình nước đã biết $D_n=1000\ \text{kg/m}^3$ và cốc chất lỏng X không hòa tan trong nước, nhẹ hơn nước.", r"a) Trình bày các bước xác định khối lượng riêng $D_X$ của chất lỏng X.", r"b) Thiết lập công thức tính $D_X$ theo các đại lượng đo được.", r"c) Nêu các nguồn sai số chính và cách giảm sai số."),
        L(r"a) Các bước : (1) rót nước vào ống chữ U tới khoảng một phần ba chiều cao, chờ hai mặt nước ngang nhau ; (2) rót chất lỏng X vào một nhánh tới khi cột X cao khoảng $15$ – $25\ \text{cm}$ ; (3) đo $h_X$ là chiều cao cột X từ mặt phân cách tới mặt thoáng của X ; (4) đo $h_n$ là độ cao mặt thoáng nước ở nhánh kia so với mặt phân cách ; (5) lặp lại ba lần với lượng X khác nhau rồi lấy trung bình.", r"b) Mặt phẳng chuẩn qua mặt phân cách, hai điểm cùng độ cao có áp suất bằng nhau : $10D_Xh_X=10D_nh_n\Rightarrow D_X=D_n\dfrac{h_n}{h_X}$.", r"c) Sai số đọc mặt phân cách và mặt thoáng (mặt khum do sức căng bề mặt) : đặt mắt ngang tầm, đọc theo đáy mặt khum. Mỗi chiều cao là hiệu của hai lần đọc (mặt phân cách và mặt thoáng) nên $\Delta h\approx2\ \text{mm}$ khi mỗi lần đọc sai $1\ \text{mm}$. Sai số tỉ đối $\dfrac{\Delta D_X}{D_X}=\dfrac{\Delta h_n}{h_n}+\dfrac{\Delta h_X}{h_X}$ nên dùng cột chất lỏng càng cao càng tốt ; ví dụ $h_X=20\ \text{cm}$, $h_n=16\ \text{cm}$ cho $\dfrac{2}{160}+\dfrac{2}{200}\approx2{,}3\%$, tức khoảng $2\%$.", r"Ống phải thẳng đứng, X không hòa tan hay phản ứng với nước ; nếu hòa tan một phần phải dùng chất lỏng thứ ba không độc làm chất đệm.")),
]

def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))


# ═════════════ GHI FILE ═════════════
write(J, 154, "Chuyên đề 11. Cơ học chất lưu: áp suất chất lỏng, bình thông nhau và lực đẩy Archimedes", DANG, BUILD, ANALYSIS, SOLS, tu_luan())
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "Số liệu mọi dạng và bài tự luận đã tự giải lại bằng Python (CHECK trong build-hinh-154.py) và thay ngược vào đề. Chờ kiểm chéo độc lập (kiem-code) rồi đặt checked=true."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
