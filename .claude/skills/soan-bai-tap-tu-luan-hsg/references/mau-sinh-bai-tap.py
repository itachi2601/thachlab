"""Bộ bài tập tự luận Cơ học — Vận dụng → Vận dụng cao, lớp 9 chuyên / HSG KHTN 9.
Sinh: đề (kèm gợi ý 3 tầng) + lời giải, dàn trang theo _tools/trang-mau-sach (school=False).
Mọi đáp số TÍNH bằng Python ở mục "số liệu" rồi mới ghép vào lời giải — sửa số thì sửa ở đó.
Chạy: python3 sinh-bai-tap.py   → *.pdf, *.html, de-chi-de.md (cho agent kiểm), dap-an.json
"""
import math, json, pathlib, re, sys
sys.path.insert(0, "/Users/MAC/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/_tools/trang-mau-sach")
from sach_mau import dung, tieu_de, muc
HERE = pathlib.Path(__file__).parent

# ---------------- SVG helpers (cùng kiểu pre-test) ----------------
def S(w, h, b):
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Arial,sans-serif" font-size="12" fill="#111" stroke="#111" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{b}</svg>')
def T(x, y, s, a="middle", sz=12, wt="normal"):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" font-size="{sz}" font-weight="{wt}" stroke="none">{s}</text>'
def L(x1, y1, x2, y2, w=1.5, d=None, m=False, ms=False):
    a = f' stroke-dasharray="{d}"' if d else ''
    a += ' marker-end="url(#ah)"' if m else ''
    a += ' marker-start="url(#ah)"' if ms else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="{w}"{a}/>'
def R(x, y, w, h, fill="none", sw=1.5):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke-width="{sw}"/>'
def C(cx, cy, r, fill="none", sw=1.5):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke-width="{sw}"/>'
def P(pts, fill="none", sw=1.5, close=False):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")
    return f'<path d="{d}" fill="{fill}" stroke-width="{sw}"/>'
def dot(x, y, r=3): return C(x, y, r, "#111")
def hatch(x1, x2, y, step=12, dy=7):
    return "".join(L(x, y, x - 6, y + dy, 1) for x in range(int(x1) + 6, int(x2), step))
WATER = "#d9e3ee"; GREY = "#9a9a9a"; LIGHT = "#e3e3e3"; WOOD = "#d8c9a3"; OIL = "#f3e2b0"

def car(x, y, lab, flip=False, w=34):
    b = R(x, y - 14, w, 14, LIGHT) + R(x + (4 if not flip else w - 22), y - 24, 18, 10, "#f6f6f6")
    b += C(x + 8, y, 4, GREY) + C(x + w - 8, y, 4, GREY) + T(x + w / 2, y - 30, lab, sz=11, wt="bold")
    return b

# ---------------- hình ----------------
def fig_hai_xe():
    b = L(20, 90, 280, 90, 2.2) + dot(20, 90, 3.5) + dot(280, 90, 3.5)
    b += T(20, 108, "A", wt="bold", sz=13) + T(280, 108, "B", wt="bold", sz=13)
    b += car(28, 86, "40 km/h") + car(238, 86, "20 km/h", True)
    b += L(66, 80, 100, 80, 1.6, m=True) + L(234, 80, 200, 80, 1.6, m=True)
    b += L(20, 128, 280, 128, 1.1, m=True, ms=True) + T(150, 143, "60 km", sz=11, wt="bold")
    b += C(150, 48, 5, "#f6f6f6") + L(150, 53, 150, 70, 1.3) + L(150, 60, 160, 66, 1.2) + L(150, 60, 140, 66, 1.2)
    b += T(150, 36, "xe máy 50 km/h", sz=10.5) + L(120, 48, 95, 48, 1.1, m=True) + L(180, 48, 205, 48, 1.1, m=True)
    return S(300, 150, b)

def fig_song():
    b = R(10, 40, 280, 70, WATER, 0) + L(10, 40, 290, 40, 1.8) + L(10, 110, 290, 110, 1.8)
    for x in (60, 150, 240): b += L(x, 75, x + 24, 75, 1.2, m=True)
    b += T(150, 30, "dòng nước chảy từ A về B", sz=10.5)
    b += L(40, 110, 40, 125, 1.2) + L(260, 110, 260, 125, 1.2)
    b += T(40, 140, "A", wt="bold", sz=13) + T(260, 140, "B", wt="bold", sz=13)
    b += P([(70, 62), (120, 62), (112, 52), (78, 52)], "#f6f6f6", close=True) + T(128, 60, "ca nô", a="start", sz=10.5)
    b += R(44, 92, 30, 8, WOOD) + L(46, 96, 72, 96, 1, "2 2") + T(59, 90, "bè", sz=10.5)
    b += L(40, 155, 260, 155, 1.1, m=True, ms=True) + T(150, 170, "AB = 60 km", sz=11, wt="bold")
    return S(300, 178, b)

def fig_tau():
    b = L(5, 120, 295, 120, 2) + R(90, 108, 130, 12, "#cfcfcf") + T(155, 136, "cầu 400 m", sz=11, wt="bold")
    for x in range(96, 220, 14): b += L(x, 108, x, 120, 1)
    b += P([(95, 108), (120, 92), (190, 92), (215, 108)], sw=1.4)
    for x in (12, 50): b += R(x, 72, 34, 16, LIGHT) + C(x + 7, 90, 3.5, GREY) + C(x + 27, 90, 3.5, GREY)
    b += P([(84, 72), (84, 88), (102, 88), (102, 80), (96, 72)], LIGHT, close=True)
    b += L(12, 66, 102, 66, 1.1, m=True, ms=True) + T(57, 60, "L = ?", sz=11, wt="bold")
    b += L(108, 80, 140, 80, 1.8, m=True) + T(124, 74, "v", sz=12, wt="bold")
    b += L(250, 120, 250, 60, 1.5) + C(250, 58, 4, "#f6f6f6") + T(250, 48, "cột điện", sz=10.5)
    return S(300, 145, b)

def fig_thanh():
    b = R(30, 70, 240, 7, LIGHT) + P([(110, 77), (97, 104), (123, 104)], GREY, close=True) + L(80, 104, 140, 104, 1.6)
    b += T(110, 118, "O", wt="bold", sz=13) + T(30, 62, "A", wt="bold", sz=13) + T(270, 62, "B", wt="bold", sz=13)
    b += L(30, 77, 30, 95, 1.6) + R(14, 95, 32, 26, GREY) + T(30, 112, "50 N", sz=10.5, wt="bold")
    b += L(270, 100, 270, 80, 2.4, m=True) + L(270, 30, 270, 66, 2.4, m=True) + T(284, 48, "F ?", sz=11, wt="bold", a="start")
    b += T(284, 96, "F ?", sz=11, wt="bold", a="start") + T(150, 58, "thanh 1,2 m · 2 kg", sz=10.5)
    b += L(30, 140, 110, 140, 1.1, m=True, ms=True) + T(70, 154, "OA = 0,4 m", sz=10.5)
    b += L(110, 140, 270, 140, 1.1, m=True, ms=True) + T(190, 154, "OB = 0,8 m", sz=10.5)
    for x in (30, 110, 270): b += L(x, 125, x, 144, 1, "2 3")
    return S(300, 162, b)

def fig_nghieng_rr():
    # Hệ toạ độ dọc mặt nghiêng: on(s, off) = A + s·u + off·n, n hướng ra ngoài (lên trên mặt nghiêng).
    A = (20, 160); B = (260, 160); Cc = (260, 100)
    ux, uy = 240 / math.hypot(240, 60), -60 / math.hypot(240, 60)
    nx, ny = uy, -ux
    ang = math.degrees(math.atan2(60, 240))
    def on(s, off=0): return (A[0] + ux * s + nx * off, A[1] + uy * s + ny * off)
    b = P([A, B, Cc], LIGHT, close=True) + hatch(20, 260, 160)
    # khối 60 kg tựa trên mặt nghiêng + ròng rọc động gắn phía trên dốc (vẽ trong hệ xoay: -y là hướng ra ngoài)
    bx, by = on(90)
    b += f'<g transform="translate({bx:.1f},{by:.1f}) rotate({-ang:.2f})">' + R(-22, -24, 44, 24, GREY) + T(0, -8, "60 kg", sz=10.5, wt="bold")
    b += L(22, -12, 36, -12, 1.6) + C(46, -12, 10, "#f6f6f6", 1.6) + dot(46, -12, 2.5) + '</g>'
    s_rr = 90 + 46                      # tâm ròng rọc động: s = 136, off = 12 (bán kính 10)
    s_fix, off_fix = 222, 32            # ròng rọc cố định ở đỉnh dốc, trên giá
    peg = on(240, 2)
    # nhánh dưới (off 2): từ ròng rọc động tới cọc ở đỉnh
    p1 = on(s_rr, 2); b += L(p1[0], p1[1], peg[0], peg[1], 1.4)
    pg0 = on(240, 0); b += L(pg0[0], pg0[1], peg[0] + nx * 6, peg[1] + ny * 6, 2.2) + dot(peg[0], peg[1], 3)
    # nhánh trên (off 22): từ ròng rọc động tới đáy ròng rọc cố định
    p2 = on(s_rr, 22); p3 = on(s_fix, 22); b += L(p2[0], p2[1], p3[0], p3[1], 1.4)
    fx, fy = on(s_fix, off_fix); g0 = on(s_fix, 0)
    b += L(fx, fy, g0[0], g0[1], 2.4) + L(g0[0] - 6, g0[1] + 1.5, g0[0] + 6, g0[1] - 1.5, 2.4) + C(fx, fy, 10, "#f6f6f6", 1.6) + dot(fx, fy, 2.5)
    # dây rời ròng rọc cố định đi thẳng lên tay kéo
    b += L(fx + 10, fy, fx + 10, 40, 1.4) + L(fx + 10, 44, fx + 10, 18, 2.2, m=True)
    b += T(fx + 16, 28, "F = ?", a="start", sz=11, wt="bold")
    b += L(278, 100, 278, 160, 1.1, m=True, ms=True) + T(282, 134, "h = 1 m", a="start", sz=10.5, wt="bold")
    b += L(260, 100, 284, 100, 1, "3 3")
    b += T(130, 180, "mặt nghiêng dài l = 4 m, hiệu suất 80 %", sz=10.5)
    return S(330, 190, b)

def fig_binh_thong():
    b = R(30, 70, 70, 100, WATER, 0) + R(170, 60, 40, 110, WATER, 0) + R(100, 150, 70, 20, WATER, 0)
    b += P([(30, 30), (30, 170), (210, 170), (210, 30)], sw=2.2) + P([(100, 30), (100, 150), (170, 150), (170, 30)], sw=2.2)
    b += R(31, 64, 68, 6, "#8d8d8d") + R(50, 40, 30, 24, GREY) + T(65, 56, "1 kg", sz=10.5, wt="bold")
    b += T(65, 186, "S₁ = 100 cm²", sz=10.5, wt="bold") + T(190, 186, "S₂ = 50 cm²", sz=10.5, wt="bold")
    b += L(230, 60, 230, 70, 1.1, m=True, ms=True) + T(236, 68, "h = ?", a="start", sz=10.5, wt="bold")
    b += L(210, 70, 236, 70, 1, "3 3")
    return S(300, 195, b)

def fig_go():
    b = R(40, 95, 220, 85, WATER, 0) + P([(40, 30), (40, 180), (260, 180), (260, 30)], sw=2.4) + L(40, 95, 260, 95, 1.8)
    b += R(110, 70, 60, 60, WOOD) + T(140, 104, "gỗ", wt="bold")
    b += L(110, 58, 170, 58, 1.1, m=True, ms=True) + T(140, 52, "S = 100 cm²", sz=10.5, wt="bold")
    b += L(186, 70, 186, 130, 1.1, m=True, ms=True) + T(190, 103, "10 cm", a="start", sz=10.5, wt="bold")
    b += L(170, 70, 190, 70, 1, "3 3") + L(170, 130, 190, 130, 1, "3 3")
    b += L(140, 130, 140, 150, 1.2) + C(140, 158, 8, "#777") + T(152, 162, "sắt (câu c)", a="start", sz=10.5)
    b += L(92, 95, 92, 130, 1.1, m=True, ms=True) + T(86, 116, "x", a="end", sz=11, wt="bold")
    return S(300, 192, b)

def fig_coc():
    b = R(30, 70, 240, 100, WATER, 0) + P([(30, 20), (30, 170), (270, 170), (270, 20)], sw=2.4) + L(30, 70, 270, 70, 1.6)
    b += P([(130, 40), (130, 100), (170, 100), (170, 40)], sw=2) + R(132, 70, 36, 30, "#f6f6f6", 0) + P([(130, 40), (130, 100), (170, 100), (170, 40)], sw=2)
    b += T(150, 32, "cốc 200 g", sz=10.5, wt="bold") + T(150, 115, "S' = 50 cm²", sz=10, a="middle")
    b += L(185, 40, 185, 100, 1.1, m=True, ms=True) + T(190, 58, "12 cm", a="start", sz=10.5, wt="bold")
    b += L(285, 70, 285, 170, 1.1, m=True, ms=True) + T(290, 122, "20 cm", a="start", sz=10.5, wt="bold")
    b += L(270, 170, 292, 170, 1, "3 3") + L(270, 70, 292, 70, 1, "3 3")
    b += T(150, 186, "bình S = 200 cm²", sz=10.5, wt="bold")
    return S(320, 195, b)

def fig_doc():
    A = (15, 150); B = (265, 150); Cc = (265, 90)
    ang = math.degrees(math.atan2(60, 250))
    b = P([A, B, Cc], LIGHT, close=True) + hatch(15, 265, 150)
    ux, uy = 250 / math.hypot(250, 60), -60 / math.hypot(250, 60)
    x0, y0 = 15 + ux * 110, 150 + uy * 110
    b += f'<g transform="translate({x0:.1f},{y0:.1f}) rotate({-ang:.2f})">' + car(-20, 0, "", w=44) + T(2, -30, "1 200 kg", sz=10.5, wt="bold")
    b += L(26, -6, 72, -6, 2.2, m=True) + T(28, -16, "v = 36 km/h", a="start", sz=10) + '</g>'
    b += L(280, 90, 280, 150, 1.1, m=True, ms=True) + T(284, 124, "50 m", a="start", sz=10.5, wt="bold")
    b += L(15, 168, 265, 168, 1.1, m=True, ms=True) + T(140, 183, "dốc dài 1 km", sz=10.5, wt="bold")
    return S(310, 190, b)

def fig_mang():
    b = f'<path d="M20 30 Q 30 150 100 150" fill="none" stroke-width="3"/>'
    b += L(100, 150, 220, 150, 3) + f'<path d="M220 150 Q 290 150 300 50" fill="none" stroke-width="3"/>'
    b += hatch(100, 220, 150, 12, 7)
    b += C(22, 30, 6, GREY) + T(40, 26, "m = 500 g", a="start", sz=10.5, wt="bold")
    b += L(40, 40, 40, 150, 1, "3 3") + L(50, 40, 50, 150, 1.1, m=True, ms=True) + T(55, 98, "h = 5 m", a="start", sz=10.5, wt="bold")
    b += T(100, 166, "M", wt="bold", sz=12) + T(220, 166, "N", wt="bold", sz=12)
    b += T(160, 178, "MN = 10 m, F<tspan baseline-shift=\"sub\" font-size=\"8\">ms</tspan> = 1 N", sz=10.5)
    b += T(60, 180, "máng (1) nhẵn", sz=10) + T(265, 180, "máng (2) nhẵn", sz=10)
    return S(320, 190, b)

def fig_bom():
    b = R(20, 130, 110, 50, WATER, 0) + P([(20, 110), (20, 180), (130, 180), (130, 110)], sw=2) + L(20, 130, 130, 130, 1.4)
    b += T(75, 196, "giếng", sz=10.5) + R(150, 100, 40, 28, LIGHT) + T(170, 118, "bơm", sz=10.5, wt="bold")
    b += L(75, 130, 75, 114, 1.8) + L(75, 114, 150, 114, 1.8)
    b += L(190, 114, 230, 114, 1.8) + L(230, 114, 230, 30, 1.8) + L(230, 30, 262, 30, 1.8)
    b += R(250, 40, 50, 30, WATER, 0) + P([(250, 20), (250, 70), (300, 70), (300, 20)], sw=2) + T(275, 86, "bể 30 m³", sz=10.5)
    b += L(262, 30, 268, 40, 1.2, m=True) + T(292, 14, "v = 4 m/s", a="end", sz=10)
    b += L(10, 40, 10, 130, 1.1, m=True, ms=True) + T(14, 88, "10 m", a="start", sz=10.5, wt="bold") + L(10, 40, 250, 40, 1, "3 3")
    b += T(200, 146, "P = 1,5 kW · H = 60 %", a="start", sz=10.5, wt="bold")
    return S(310, 200, b)

# ---------------- số liệu (tính thật) ----------------
g = 10
N = {}
# Bài 1
N1 = dict(AB=60, v1=40, v2=20, vm=50)
N1["t_gap"] = N1["AB"] / (N1["v1"] + N1["v2"]); N1["s_gap"] = N1["v1"] * N1["t_gap"]; N1["s_may"] = N1["vm"] * N1["t_gap"]
N1["s2_som"] = N1["v2"] * 0.25; N1["t_c"] = (N1["AB"] - N1["s2_som"]) / (N1["v1"] + N1["v2"]); N1["s_c"] = N1["v1"] * N1["t_c"]
# Bài 2
N2 = dict(v1=18, v2=20, v3=4, t_tong=5 / 3)
N2["vtb2"] = (N2["v2"] + N2["v3"]) / 2; N2["vtb"] = 2 * N2["v1"] * N2["vtb2"] / (N2["v1"] + N2["vtb2"])
N2["AB"] = N2["vtb"] * N2["t_tong"]; N2["sai_tb"] = (N2["v1"] + N2["v2"] + N2["v3"]) / 3
# Bài 3
N3 = dict(AB=60, tx=2, tn=3)
N3["vx"] = N3["AB"] / N3["tx"]; N3["vn"] = N3["AB"] / N3["tn"]; N3["u"] = (N3["vx"] - N3["vn"]) / 2; N3["v"] = (N3["vx"] + N3["vn"]) / 2
N3["t_be"] = N3["AB"] / N3["u"]; N3["d_2h"] = N3["AB"] - N3["u"] * N3["tx"]; N3["t_gap2"] = N3["d_2h"] / N3["v"]
N3["t_gap"] = N3["tx"] + N3["t_gap2"]; N3["s_gap"] = N3["u"] * N3["t_gap"]
# Bài 4
N4 = dict(t_cot=10, t_cau=50, cau=400, L2=150, v2=8)
N4["L"] = N4["cau"] * N4["t_cot"] / (N4["t_cau"] - N4["t_cot"]); N4["v"] = N4["L"] / N4["t_cot"]
N4["t_nguoc"] = (N4["L"] + N4["L2"]) / (N4["v"] + N4["v2"]); N4["t_cung"] = (N4["L"] + N4["L2"]) / (N4["v"] - N4["v2"])
# Bài 5
N5 = dict(AB=1.2, m=2, OA=0.4, PA=50)
N5["P"] = g * N5["m"]; N5["OB"] = N5["AB"] - N5["OA"]; N5["OG"] = N5["AB"] / 2 - N5["OA"]
N5["F"] = (N5["PA"] * N5["OA"] - N5["P"] * N5["OG"]) / N5["OB"]; N5["N"] = N5["PA"] + N5["P"] + N5["F"]
N5["OC"] = N5["P"] * N5["OG"] / N5["PA"]
# Bài 6
N6 = dict(m=60, l=4, h=1, H=0.8)
N6["P"] = g * N6["m"]; N6["F_ly"] = N6["P"] * N6["h"] / N6["l"]; N6["F_rr_ly"] = N6["F_ly"] / 2
N6["F_doc"] = N6["F_ly"] / N6["H"]; N6["Fms"] = N6["F_doc"] - N6["F_ly"]; N6["F"] = N6["F_doc"] / 2
N6["s_day"] = 2 * N6["l"]; N6["A"] = N6["F"] * N6["s_day"]; N6["A_ich"] = N6["P"] * N6["h"]
# Bài 7
N7 = dict(S1=100e-4, S2=50e-4, m=1, dn=10000, dd=8000)
N7["p"] = g * N7["m"] / N7["S1"]; N7["h"] = N7["p"] / N7["dn"]; N7["m2"] = N7["p"] * N7["S2"] / g; N7["hd"] = N7["p"] / N7["dd"]
# Bài 8
N8 = dict(S=100e-4, h=0.10, Dg=600, Dn=1000, Ds=7800)
N8["V"] = N8["S"] * N8["h"]; N8["Pg"] = g * N8["Dg"] * N8["V"]; N8["x"] = N8["Dg"] / N8["Dn"] * N8["h"]
N8["FA_max"] = g * N8["Dn"] * N8["V"]; N8["m_b"] = (N8["FA_max"] - N8["Pg"]) / g
N8["Vs"] = (N8["FA_max"] - N8["Pg"]) / (g * (N8["Ds"] - N8["Dn"])); N8["ms"] = N8["Ds"] * N8["Vs"]; N8["T"] = N8["FA_max"] - N8["Pg"]
# Bài 9
N9 = dict(S=200, S2=50, hc=12, mc=200, m_nuoc=100, m_soi=100, D_soi=2.5)
N9["x_a"] = N9["mc"] / N9["S2"]; N9["dh_a"] = N9["mc"] / N9["S"]; N9["dh_b"] = N9["m_nuoc"] / N9["S"]; N9["x_b"] = (N9["mc"] + N9["m_nuoc"]) / N9["S2"]
N9["dh_c1"] = N9["m_soi"] / N9["S"]; N9["V_soi"] = N9["m_soi"] / N9["D_soi"]; N9["dh_c2"] = N9["V_soi"] / N9["S"]
N9["m_max"] = N9["S2"] * N9["hc"] - N9["mc"]
# Bài 10
N10 = dict(m=1200, l=1000, h=50, v=10, Fc=400, H=0.25, q=4.6e7)
N10["P"] = g * N10["m"]; N10["Fk"] = N10["P"] * N10["h"] / N10["l"] + N10["Fc"]; N10["Pcs"] = N10["Fk"] * N10["v"]
N10["A"] = N10["Fk"] * N10["l"]; N10["Q"] = N10["A"] / N10["H"]; N10["mx"] = N10["Q"] / N10["q"]; N10["Fc_xuong"] = N10["P"] * N10["h"] / N10["l"]
# Bài 11
N11 = dict(m=0.5, h=5, MN=10, Fms=1)
N11["W"] = g * N11["m"] * N11["h"]; N11["v"] = math.sqrt(2 * g * N11["h"]); N11["A_MN"] = N11["Fms"] * N11["MN"]
N11["W_N"] = N11["W"] - N11["A_MN"]; N11["h2"] = N11["W_N"] / (g * N11["m"]); N11["s_tong"] = N11["W"] / N11["Fms"]
N11["W_M2"] = N11["W_N"] - N11["A_MN"]; N11["h1b"] = N11["W_M2"] / (g * N11["m"]); N11["s_cuoi"] = N11["W_M2"] / N11["Fms"]
# Bài 12
N12 = dict(Pdc=1500, H=0.6, h=10, v=4, V_be=30)
N12["Pi"] = N12["Pdc"] * N12["H"]; N12["q_a"] = N12["Pi"] / (g * N12["h"]); N12["e_kg"] = g * N12["h"] + N12["v"] ** 2 / 2
N12["q_b"] = N12["Pi"] / N12["e_kg"]; N12["t"] = N12["V_be"] * 1000 / N12["q_b"]; N12["E_kWh"] = N12["Pdc"] / 1000 * N12["t"] / 3600

def f(x, n=1):
    s = f"{x:.{n}f}".rstrip("0").rstrip(".") if n else f"{x:.0f}"
    return s.replace(".", ",")

# ---------------- cấu trúc đề ----------------
FIGN = [0]
def fig(svg, cap=None):
    FIGN[0] += 1
    return f'<div class="fig">{svg}<br>Hình {FIGN[0]}{(" — " + cap) if cap else ""}</div>'

BAI = []   # dict(n, muc, tieu_de, de(list cau), fig, goi_y(list 3), giai(html), dap_so(list), nhan_dang, bay(list))
def bai(**k): BAI.append(k)

VD, VDC = "Vận dụng", "Vận dụng cao"

bai(n=1, muc="A", lvl=VD, ten="Hai xe và người đưa thư", fig=fig_hai_xe(),
    de=["Hai địa điểm A, B cách nhau 60 km. Lúc 7 h, xe thứ nhất đi từ A về B với tốc độ không đổi 40 km/h; cùng lúc đó xe thứ hai đi từ B về A với tốc độ không đổi 20 km/h.",
        "a) Hai xe gặp nhau lúc mấy giờ? Chỗ gặp cách A bao xa?",
        "b) Cũng lúc 7 h, một người đi xe máy xuất phát từ A với tốc độ 50 km/h, chạy liên tục giữa hai xe: gặp xe này thì quay đầu ngay chạy về phía xe kia, cho đến khi hai xe gặp nhau. Tính tổng quãng đường người đi xe máy đã đi.",
        "c) Nếu xe thứ hai xuất phát sớm hơn 15 phút (lúc 6 h 45), hai xe gặp nhau lúc mấy giờ, cách A bao xa?"],
    goi_y=["Hai vật đi ngược chiều: khoảng cách giảm với tốc độ bằng <b>tổng</b> hai tốc độ.",
           "Câu b: cần quãng đường, mà s = v·t. Người đi xe máy đi trong <b>bao lâu</b>? Thời gian đó đã có ở câu a chưa?",
           "Câu c: lúc 7 h hai xe còn cách nhau bao nhiêu (xe hai đã đi 15 phút)? Rồi làm lại như câu a với khoảng cách mới."],
    giai=[("a) Thời điểm và vị trí gặp nhau",
           [f"Mỗi giờ khoảng cách hai xe giảm: {N1['v1']} + {N1['v2']} = {N1['v1']+N1['v2']} km.",
            f"t = AB / (v₁ + v₂) = {N1['AB']} / {N1['v1']+N1['v2']} = {f(N1['t_gap'])} h.",
            f"Gặp nhau lúc 7 h + 1 h = <b>8 h</b>; cách A: s = v₁·t = {N1['v1']} × {f(N1['t_gap'])} = <b>{f(N1['s_gap'])} km</b>."]),
          ("b) Quãng đường của người đi xe máy",
           ["Người đó chạy liên tục với tốc độ không đổi 50 km/h từ 7 h đến lúc hai xe gặp nhau (8 h), tức là đúng 1 h.",
            f"s = v·t = {N1['vm']} × {f(N1['t_gap'])} = <b>{f(N1['s_may'])} km</b>.",
            "Không cần tính từng lượt đi–về: tổng quãng đường chỉ phụ thuộc tốc độ và tổng thời gian."]),
          ("c) Xe thứ hai đi sớm 15 phút",
           [f"Trong 15 phút = 0,25 h, xe hai đi được: {N1['v2']} × 0,25 = {f(N1['s2_som'])} km.",
            f"Lúc 7 h hai xe còn cách nhau: {N1['AB']} − {f(N1['s2_som'])} = {f(N1['AB']-N1['s2_som'])} km.",
            f"t = {f(N1['AB']-N1['s2_som'])} / {N1['v1']+N1['v2']} = {f(N1['t_c'],4)} h = {f(N1['t_c']*60,0)} phút → gặp lúc <b>7 h 55</b>.",
            f"Cách A: {N1['v1']} × {f(N1['t_c'],4)} ≈ <b>{f(N1['s_c'])} km</b>."])],
    dap=["a) 8 h; cách A 40 km", "b) 50 km", "c) 7 h 55; cách A ≈ 36,7 km"],
    nhan_dang="Thấy <b>hai vật đi ngược chiều, hỏi lúc gặp</b> → chia khoảng cách cho <b>tổng tốc độ</b>; vật thứ ba chạy qua lại → chỉ cần <b>tổng thời gian</b>.",
    bay=["Câu b: cộng từng lượt đi–về (chuỗi vô hạn) — không cần, vì tốc độ không đổi nên s = v·t.",
         "Câu c: quên trừ quãng đường xe hai đã đi trước, hoặc lấy mốc gặp từ 6 h 45 thay vì 7 h."])

bai(n=2, muc="A", lvl=VD, ten="Tốc độ trung bình — nửa quãng đường, nửa thời gian", fig=None,
    de=["Một người đi xe đạp từ A đến B. Nửa quãng đường đầu người đó đi với tốc độ 18 km/h. Trên nửa quãng đường còn lại, nửa thời gian đầu đi với tốc độ 20 km/h, nửa thời gian sau đi với tốc độ 4 km/h (đường xấu).",
        "a) Tính tốc độ trung bình trên nửa quãng đường sau.",
        "b) Tính tốc độ trung bình trên cả quãng đường AB.",
        "c) Biết tổng thời gian đi từ A đến B là 1 h 40 phút. Tính AB."],
    goi_y=["Tốc độ trung bình là <b>tổng quãng đường chia tổng thời gian</b> — không phải trung bình cộng các tốc độ.",
           "Hai đoạn có <b>cùng thời gian</b> thì tốc độ trung bình bằng trung bình cộng; hai đoạn <b>cùng quãng đường</b> thì không. Mỗi câu thuộc trường hợp nào?",
           "Đặt AB = s, viết thời gian từng đoạn theo s rồi cộng lại."],
    giai=[("a) Nửa quãng đường sau (hai đoạn cùng thời gian t′)",
           [f"s₂ = {N2['v2']}·t′ + {N2['v3']}·t′ = {N2['v2']+N2['v3']}·t′; thời gian 2t′.",
            f"v<sub>tb2</sub> = s₂ / (2t′) = {N2['v2']+N2['v3']} / 2 = <b>{f(N2['vtb2'])} km/h</b>."]),
          ("b) Cả quãng đường (hai nửa cùng quãng đường s/2)",
           [f"t₁ = (s/2)/{N2['v1']} = s/{2*N2['v1']}; t₂ = (s/2)/{f(N2['vtb2'])} = s/{f(2*N2['vtb2'])}.",
            f"v<sub>tb</sub> = s / (t₁ + t₂) = 2·v₁·v<sub>tb2</sub> / (v₁ + v<sub>tb2</sub>) = 2 × {N2['v1']} × {f(N2['vtb2'])} / {f(N2['v1']+N2['vtb2'])} = <b>{f(N2['vtb'])} km/h</b>.",
            f"So sánh: trung bình cộng ba tốc độ = ({N2['v1']} + {N2['v2']} + {N2['v3']})/3 = {f(N2['sai_tb'])} km/h — sai."]),
          ("c) Tính AB",
           [f"t = s / v<sub>tb</sub> ⇒ s = v<sub>tb</sub>·t = {f(N2['vtb'])} × 5/3 = <b>{f(N2['AB'])} km</b>.",
            f"Kiểm: t₁ = 12/18 = 2/3 h; t₂ = 12/12 = 1 h; tổng 5/3 h = 1 h 40 phút. Đúng."])],
    dap=["a) 12 km/h", "b) 14,4 km/h", "c) 24 km"],
    nhan_dang="Thấy <b>nửa quãng đường / nửa thời gian</b> → đặt s hoặc t làm ẩn, lập <b>tổng quãng đường / tổng thời gian</b>.",
    bay=["Lấy trung bình cộng các tốc độ cho đoạn cùng quãng đường.", "Quên rằng hai nửa thời gian ở câu a bằng nhau nên có thể gộp."])

bai(n=3, muc="A", lvl=VDC, ten="Ca nô và bè gỗ", fig=fig_song(),
    de=["Một ca nô xuôi dòng từ A đến B hết 2 h và ngược dòng từ B về A hết 3 h. Biết AB = 60 km; tốc độ của ca nô đối với nước và tốc độ của dòng nước đều không đổi.",
        "a) Tính tốc độ của dòng nước và tốc độ của ca nô đối với nước.",
        "b) Một bè gỗ thả trôi theo dòng từ A đến B mất bao lâu?",
        "c) Lúc 6 h, bè bắt đầu trôi từ A; cùng lúc ca nô xuất phát từ A xuôi về B, tới B quay đầu ngay và chạy ngược về A. Ca nô gặp lại bè lúc mấy giờ, tại điểm cách A bao xa?"],
    goi_y=["Tốc độ xuôi = v + u, tốc độ ngược = v − u (v: tốc độ đối với nước, u: tốc độ dòng). Bè trôi với tốc độ u.",
           "Câu c: lúc ca nô tới B, bè đang ở đâu? Từ đó hai vật <b>đi ngược chiều</b> với tốc độ nào?",
           "Cách nhanh: xét chuyển động <b>so với dòng nước</b> — nước đứng yên thì bè đứng yên, ca nô đi với tốc độ v cả hai chiều."],
    giai=[("a) Tốc độ dòng nước và tốc độ ca nô",
           [f"v + u = {N3['AB']}/{N3['tx']} = {f(N3['vx'])} km/h; v − u = {N3['AB']}/{N3['tn']} = {f(N3['vn'])} km/h.",
            f"u = ({f(N3['vx'])} − {f(N3['vn'])})/2 = <b>{f(N3['u'])} km/h</b>; v = ({f(N3['vx'])} + {f(N3['vn'])})/2 = <b>{f(N3['v'])} km/h</b>."]),
          ("b) Bè trôi",
           [f"Bè trôi với tốc độ dòng: t = AB/u = {N3['AB']}/{f(N3['u'])} = <b>{f(N3['t_be'])} h</b>."]),
          ("c) Ca nô gặp lại bè",
           [f"Ca nô tới B sau {N3['tx']} h; khi đó bè đã trôi u·{N3['tx']} = {f(N3['u']*N3['tx'])} km, còn cách B: {N3['AB']} − {f(N3['u']*N3['tx'])} = {f(N3['d_2h'])} km.",
            f"Ca nô ngược dòng ({f(N3['vn'])} km/h) và bè xuôi dòng ({f(N3['u'])} km/h) đi ngược chiều nhau: tốc độ gặp nhau {f(N3['vn'])} + {f(N3['u'])} = {f(N3['v'])} km/h (đúng bằng v).",
            f"t′ = {f(N3['d_2h'])}/{f(N3['v'])} = {f(N3['t_gap2'])} h ⇒ gặp lúc 6 h + {N3['tx']} h + {f(N3['t_gap2'])} h = <b>{6+int(N3['t_gap'])} h</b>.",
            f"Vị trí: bè trôi được u·t = {f(N3['u'])} × {f(N3['t_gap'])} = <b>{f(N3['s_gap'])} km</b> kể từ A.",
            f"Cách 2 (so với nước): bè đứng yên, ca nô đi xa 2v·… rồi quay về với cùng tốc độ v ⇒ thời gian về bằng thời gian đi = 2 h. Kết quả như trên."])],
    dap=["a) u = 5 km/h; v = 25 km/h", "b) 12 h", "c) 10 h; cách A 20 km"],
    nhan_dang="Thấy <b>xuôi – ngược dòng, bè trôi</b> → lập hệ v + u, v − u; gặp bè thì xét <b>so với dòng nước</b>.",
    bay=["Lấy u = (v<sub>xuôi</sub> − v<sub>ngược</sub>) mà quên chia 2.", "Câu c: cho bè đứng yên so với bờ (quên bè vẫn trôi khi ca nô quay về)."])

bai(n=4, muc="A", lvl=VD, ten="Đoàn tàu qua cột điện, qua cầu, qua tàu khác", fig=fig_tau(),
    de=["Một đoàn tàu chuyển động thẳng đều. Tàu chạy qua một cột điện (từ lúc đầu tàu tới cột đến lúc đuôi tàu rời cột) hết 10 s; chạy qua một cây cầu dài 400 m (từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu) hết 50 s.",
        "a) Tính chiều dài L và tốc độ v của đoàn tàu.",
        "b) Tàu gặp một đoàn tàu khác dài 150 m chạy ngược chiều với tốc độ 8 m/s. Hai tàu lướt qua nhau (từ lúc hai đầu tàu gặp nhau đến lúc hai đuôi tàu rời nhau) trong bao lâu?",
        "c) Nếu tàu thứ hai chạy cùng chiều với tốc độ 8 m/s, tàu thứ nhất vượt qua nó mất bao lâu?"],
    goi_y=["Vật có chiều dài: quãng đường đi để \"qua\" một vật mốc = <b>chiều dài tàu + chiều dài vật mốc</b> (cột điện coi như dài 0).",
           "Hai tàu lướt qua nhau: tổng chiều dài hai tàu được \"đi qua\" với <b>tốc độ tương đối</b>. Ngược chiều cộng, cùng chiều trừ.",
           "Câu a: hai phương trình L = v·10 và L + 400 = v·50; thế một vào hai."],
    giai=[("a) Chiều dài và tốc độ tàu",
           [f"Qua cột: L = v·{N4['t_cot']}. Qua cầu: L + {N4['cau']} = v·{N4['t_cau']}.",
            f"Trừ hai vế: {N4['cau']} = v·({N4['t_cau']} − {N4['t_cot']}) ⇒ v = {N4['cau']}/{N4['t_cau']-N4['t_cot']} = <b>{f(N4['v'])} m/s</b>; L = {f(N4['v'])} × {N4['t_cot']} = <b>{f(N4['L'])} m</b>."]),
          ("b) Hai tàu ngược chiều",
           [f"Quãng đường tương đối cần đi: L + L₂ = {f(N4['L'])} + {N4['L2']} = {f(N4['L']+N4['L2'])} m.",
            f"Tốc độ tương đối: v + v₂ = {f(N4['v'])} + {N4['v2']} = {f(N4['v']+N4['v2'])} m/s.",
            f"t = {f(N4['L']+N4['L2'])}/{f(N4['v']+N4['v2'])} ≈ <b>{f(N4['t_nguoc'])} s</b>."]),
          ("c) Hai tàu cùng chiều",
           [f"Tốc độ tương đối: v − v₂ = {f(N4['v']-N4['v2'])} m/s.",
            f"t = {f(N4['L']+N4['L2'])}/{f(N4['v']-N4['v2'])} = <b>{f(N4['t_cung'])} s</b> (hơn 2 phút — vì chỉ nhanh hơn 2 m/s)."])],
    dap=["a) L = 100 m; v = 10 m/s", "b) ≈ 13,9 s", "c) 125 s"],
    nhan_dang="Thấy <b>tàu/đoàn xe có chiều dài qua cầu, qua nhau</b> → quãng đường = <b>tổng chiều dài</b>, tốc độ = <b>tương đối</b>.",
    bay=["Qua cầu lấy quãng đường bằng 400 m (quên cộng chiều dài tàu).", "Câu c lấy tốc độ tương đối là 10 + 8."])

bai(n=5, muc="B", lvl=VD, ten="Thanh đồng chất trên điểm tựa", fig=fig_thanh(),
    de=["Thanh AB đồng chất, tiết diện đều, dài 1,2 m, khối lượng 2 kg, đặt trên điểm tựa O với OA = 0,4 m. Treo tại đầu A một vật có trọng lượng 50 N. Lấy g = 10 N/kg.",
        "a) Để thanh cân bằng nằm ngang, phải tác dụng vào đầu B một lực F theo phương thẳng đứng. F hướng lên hay hướng xuống? Tính F.",
        "b) Tính lực mà điểm tựa O tác dụng lên thanh khi đó.",
        "c) Bỏ lực F. Phải dời vật 50 N tới điểm C nào trên thanh để thanh tự cân bằng nằm ngang? Tính OC và cho biết C nằm về phía A hay phía B."],
    goi_y=["Điều kiện cân bằng của đòn bẩy: tổng mômen làm quay thuận chiều kim đồng hồ bằng tổng mômen làm quay ngược chiều (F₁·d₁ = F₂·d₂, d tính từ O).",
           "Thanh <b>có khối lượng</b>: trọng lượng thanh đặt tại <b>trung điểm</b> — trung điểm nằm bên nào của O? Nó làm thanh quay chiều nào?",
           "Câu b: thanh đứng yên theo phương thẳng đứng ⇒ lực đỡ của O cân bằng với tổng các lực kéo xuống."],
    giai=[("a) Chiều và độ lớn của F",
           [f"Trọng lượng thanh P = {N5['m']}·g = {f(N5['P'])} N, đặt tại trung điểm G cách A 0,6 m ⇒ cách O: OG = {f(N5['OG'])} m, về phía B.",
            f"Vật 50 N ở A kéo thanh quay về phía A (mômen {N5['PA']} × {N5['OA']} = {f(N5['PA']*N5['OA'])} N·m); P tại G kéo về phía B (mômen {f(N5['P'])} × {f(N5['OG'])} = {f(N5['P']*N5['OG'])} N·m).",
            f"Phía A thắng ⇒ F tại B phải <b>hướng xuống</b> để bù: {f(N5['PA']*N5['OA'])} = {f(N5['P']*N5['OG'])} + F × {f(N5['OB'])} ⇒ F = <b>{f(N5['F'])} N</b>."]),
          ("b) Lực của điểm tựa",
           [f"Ba lực kéo xuống: 50 + {f(N5['P'])} + {f(N5['F'])} ⇒ N = <b>{f(N5['N'])} N</b>, hướng lên."]),
          ("c) Vị trí C",
           [f"Chỉ còn vật và trọng lượng thanh: 50 × OC = {f(N5['P'])} × {f(N5['OG'])} ⇒ OC = <b>{f(N5['OC']*100)} cm</b>, về phía A."])],
    dap=["a) F hướng xuống, F = 20 N", "b) 90 N", "c) OC = 8 cm (về phía A)"],
    nhan_dang="Thấy <b>thanh có khối lượng</b> trên điểm tựa → thêm <b>trọng lượng thanh tại trung điểm</b> vào phương trình mômen.",
    bay=["Bỏ qua trọng lượng thanh (coi thanh nhẹ).", "Lấy cánh tay đòn của P là 0,6 m (đo từ A thay vì từ O).", "Chọn F hướng lên theo cảm tính rồi ra số âm mà không nhận ra."])

bai(n=6, muc="B", lvl=VDC, ten="Mặt phẳng nghiêng kết hợp ròng rọc động", fig=fig_nghieng_rr(),
    de=["Kéo một vật khối lượng 60 kg lên theo mặt phẳng nghiêng dài 4 m, cao 1 m bằng hệ gồm một ròng rọc động gắn vào vật và một ròng rọc cố định ở đỉnh dốc (hình); các đoạn dây đều song song với mặt nghiêng. Hiệu suất của riêng mặt phẳng nghiêng (tỉ số giữa công nâng vật và công của lực kéo vật dọc mặt nghiêng) là 80 %; ròng rọc nhẹ, trục không ma sát; dây nhẹ, không giãn. Lấy g = 10 N/kg.",
        "a) Nếu mặt nghiêng không có ma sát, lực kéo ở đầu dây là bao nhiêu?",
        "b) Với hiệu suất 80 %, tính lực ma sát giữa vật và mặt nghiêng và lực kéo thực tế ở đầu dây.",
        "c) Để đưa vật từ chân lên đỉnh dốc, người kéo phải kéo dây đi một đoạn bao nhiêu và thực hiện công bao nhiêu? Tính hiệu suất của cả hệ."],
    goi_y=["Hai máy cơ nối tiếp: mặt phẳng nghiêng (lợi về lực l/h) rồi ròng rọc động (lợi 2 lần về lực, thiệt 2 lần về đường đi).",
           "Hiệu suất 80 % là của <b>mặt nghiêng</b>: A<sub>ích</sub> = P·h, A<sub>toàn phần</sub> = F<sub>dọc</sub>·l. Lực dọc mặt nghiêng là lực nào trong hệ — lực ở đầu dây hay lực do ròng rọc động truyền?",
           "Công hao phí trên mặt nghiêng = F<sub>ms</sub>·l. Ròng rọc không ma sát nên công ở đầu dây = công dọc mặt nghiêng."],
    giai=[("a) Không ma sát",
           [f"P = {f(N6['P'],0)} N. Lực dọc mặt nghiêng (lí tưởng): F₀ = P·h/l = {f(N6['P'],0)} × {N6['h']}/{N6['l']} = {f(N6['F_ly'])} N.",
            f"Ròng rọc động lợi 2 lần: F = F₀/2 = <b>{f(N6['F_rr_ly'])} N</b>."]),
          ("b) Có ma sát, hiệu suất 80 %",
           [f"H = P·h / (F<sub>dọc</sub>·l) ⇒ F<sub>dọc</sub> = P·h/(H·l) = {f(N6['A_ich'],0)}/(0,8 × {N6['l']}) = {f(N6['F_doc'],2)} N.",
            f"F<sub>ms</sub> = F<sub>dọc</sub> − F₀ = {f(N6['F_doc'],2)} − {f(N6['F_ly'])} = <b>{f(N6['Fms'],2)} N</b>.",
            f"Lực kéo đầu dây: F = F<sub>dọc</sub>/2 = <b>{f(N6['F'],2)} N</b>."]),
          ("c) Đoạn dây, công, hiệu suất hệ",
           [f"Vật đi 4 m dọc dốc ⇒ dây kéo đi 2 × 4 = <b>{f(N6['s_day'])} m</b>.",
            f"A = F·s = {f(N6['F'],2)} × {f(N6['s_day'])} = <b>{f(N6['A'])} J</b> (bằng F<sub>dọc</sub>·l = {f(N6['F_doc'],2)} × 4).",
            f"A<sub>ích</sub> = P·h = {f(N6['A_ich'],0)} J ⇒ H<sub>hệ</sub> = {f(N6['A_ich'],0)}/{f(N6['A'])} = <b>80 %</b> — ròng rọc không ma sát nên hiệu suất hệ bằng hiệu suất mặt nghiêng."])],
    dap=["a) 75 N", "b) F<sub>ms</sub> = 37,5 N; F = 93,75 N", "c) 8 m; 750 J; H = 80 %"],
    nhan_dang="Thấy <b>hai máy cơ nối tiếp, cho hiệu suất</b> → tách từng máy: lực nào đi vào máy nào; <b>công không đổi qua ròng rọc không ma sát</b>.",
    bay=["Chia hiệu suất cho lực ở đầu dây (sau ròng rọc) thay vì lực dọc mặt nghiêng.", "Quên dây đi gấp đôi quãng đường vật.", "Nhân hiệu suất 80 % với 0,5 của ròng rọc (lẫn lợi về lực với hiệu suất)."])

bai(n=7, muc="C", lvl=VD, ten="Bình thông nhau có pittông", fig=fig_binh_thong(),
    de=["Bình thông nhau gồm hai nhánh hình trụ tiết diện S₁ = 100 cm² và S₂ = 50 cm², chứa nước (trọng lượng riêng 10 000 N/m³). Đặt lên mặt nước nhánh lớn một pittông mỏng, nhẹ, khít rồi đặt lên pittông một quả cân 1 kg. Lấy g = 10 N/kg.",
        "a) Mực nước hai nhánh chênh lệch bao nhiêu? Nhánh nào cao hơn?",
        "b) Đặt lên mặt nước nhánh nhỏ một pittông nhẹ, khít. Phải đặt lên pittông này quả cân khối lượng bao nhiêu để mực nước hai nhánh ngang nhau?",
        "c) Bỏ pittông ở nhánh nhỏ (nhánh lớn vẫn còn pittông và quả cân 1 kg). Đổ dầu (trọng lượng riêng 8 000 N/m³, không tan trong nước) vào nhánh nhỏ cho đến khi mặt nước hai nhánh ngang nhau. Tính chiều cao cột dầu."],
    goi_y=["Hai điểm trong <b>cùng một chất lỏng đứng yên, cùng độ cao</b> thì có cùng áp suất. Chọn mặt so sánh tại mặt dưới pittông nhánh lớn.",
           "Pittông truyền áp suất p = F/S — S nào? Áp suất ở nhánh nhỏ phải tăng bằng bao nhiêu để cân bằng: bằng cột nước cao h (p = d·h), hoặc bằng quả cân khác, hoặc bằng cột dầu.",
           "Câu b: cùng áp suất, tiết diện khác nhau ⇒ lực khác nhau: F₂/S₂ = F₁/S₁."],
    giai=[("a) Độ chênh mực nước",
           [f"Áp suất quả cân gây ra: p = F/S₁ = {g*N7['m']}/{N7['S1']} = {f(N7['p'],0)} Pa.",
            f"Cột nước nhánh nhỏ phải cao hơn mặt dưới pittông: h = p/d = {f(N7['p'],0)}/{N7['dn']} = <b>{f(N7['h']*100)} cm</b>; <b>nhánh nhỏ</b> cao hơn."]),
          ("b) Quả cân ở nhánh nhỏ",
           [f"Cùng mực ⇒ cùng áp suất: F₂/S₂ = F₁/S₁ ⇒ F₂ = F₁·S₂/S₁ = 10 × 50/100 = {f(N7['m2']*g)} N ⇒ m₂ = <b>{f(N7['m2'])} kg</b>."]),
          ("c) Cột dầu",
           [f"Cột dầu phải gây áp suất đúng bằng p: d<sub>dầu</sub>·h<sub>d</sub> = {f(N7['p'],0)} ⇒ h<sub>d</sub> = {f(N7['p'],0)}/{N7['dd']} = <b>{f(N7['hd']*100)} cm</b>.",
            "Lưu ý: so sánh áp suất tại mặt nước (mặt phân cách dầu–nước) ở nhánh nhỏ với mặt dưới pittông — hai mặt này ngang nhau nên không có thêm cột nước nào."])],
    dap=["a) 10 cm; nhánh nhỏ cao hơn", "b) 0,5 kg", "c) 12,5 cm"],
    nhan_dang="Thấy <b>bình thông nhau có pittông / hai chất lỏng</b> → chọn <b>mặt đẳng áp</b> trong cùng một chất lỏng, viết p hai bên.",
    bay=["Lấy m₂ = 1 kg vì \"cùng áp suất\" (quên tiết diện khác nhau).", "Câu c dùng d của nước thay vì của dầu.", "Chọn mặt so sánh nằm trong dầu (không cùng chất lỏng)."])

bai(n=8, muc="C", lvl=VDC, ten="Khối gỗ nổi, vật đặt trên và vật treo dưới", fig=fig_go(),
    de=["Khối gỗ hình hộp chữ nhật, diện tích đáy 100 cm², cao 10 cm, khối lượng riêng 600 kg/m³, thả nổi trong nước (khối lượng riêng 1 000 kg/m³). Lấy g = 10 N/kg.",
        "a) Tính chiều cao phần gỗ chìm trong nước.",
        "b) Đặt lên mặt gỗ một vật nhỏ khối lượng m. Tính m để mặt trên của gỗ vừa ngang mặt nước.",
        "c) Bỏ vật ở câu b. Dùng dây mảnh, không giãn treo dưới đáy gỗ một quả cầu bằng sắt (khối lượng riêng 7 800 kg/m³, ngập hoàn toàn trong nước) thì gỗ cũng vừa chìm hết. Bỏ qua thể tích dây. Tính thể tích và khối lượng quả cầu.",
        "d) Trong trường hợp c, dây chịu lực căng bao nhiêu?"],
    goi_y=["Vật nổi cân bằng: lực đẩy Archimedes bằng tổng trọng lượng của <b>những gì nó phải đỡ</b>. F<sub>A</sub> = d<sub>nước</sub>·V<sub>chìm</sub>.",
           "Câu c: hệ gỗ + sắt cân bằng. Có <b>hai</b> lực đẩy Archimedes (gỗ chìm hết và sắt chìm hết) và hai trọng lượng. Viết cho cả hệ, không cần lực căng dây.",
           "Câu d: xét riêng gỗ (hoặc riêng sắt): lực căng dây = chênh lệch giữa trọng lượng và lực đẩy của riêng vật đó."],
    giai=[("a) Phần chìm",
           [f"V = {f(N8['S']*1e4,0)} × {f(N8['h']*100,0)} = {f(N8['V']*1e6,0)} cm³; P<sub>gỗ</sub> = 10·D<sub>g</sub>·V = {f(N8['Pg'])} N.",
            f"Nổi: F<sub>A</sub> = P<sub>gỗ</sub> ⇒ 10·D<sub>n</sub>·S·x = 10·D<sub>g</sub>·S·h ⇒ x = h·D<sub>g</sub>/D<sub>n</sub> = 10 × 600/1 000 = <b>{f(N8['x']*100)} cm</b>."]),
          ("b) Vật đặt trên",
           [f"Gỗ chìm hết: F<sub>A,max</sub> = 10 × 1 000 × {f(N8['V'],4)} = {f(N8['FA_max'])} N.",
            f"F<sub>A,max</sub> = P<sub>gỗ</sub> + 10·m ⇒ m = ({f(N8['FA_max'])} − {f(N8['Pg'])})/10 = <b>{f(N8['m_b'])} kg</b>."]),
          ("c) Quả cầu sắt treo dưới",
           [f"Hệ gỗ + sắt: F<sub>A,gỗ</sub> + F<sub>A,sắt</sub> = P<sub>gỗ</sub> + P<sub>sắt</sub>.",
            f"{f(N8['FA_max'])} + 10·1 000·V<sub>s</sub> = {f(N8['Pg'])} + 10·7 800·V<sub>s</sub> ⇒ V<sub>s</sub> = {f(N8['FA_max']-N8['Pg'])}/(10 × 6 800) ≈ {f(N8['Vs'],6)} m³ ≈ <b>{f(N8['Vs']*1e6)} cm³</b>.",
            f"m<sub>s</sub> = D<sub>s</sub>·V<sub>s</sub> = 7 800 × {f(N8['Vs'],6)} ≈ <b>{f(N8['ms'],3)} kg</b> (≈ 459 g)."]),
          ("d) Lực căng dây",
           [f"Xét riêng gỗ: F<sub>A,gỗ</sub> = P<sub>gỗ</sub> + T ⇒ T = {f(N8['FA_max'])} − {f(N8['Pg'])} = <b>{f(N8['T'])} N</b>.",
            f"Kiểm bằng sắt: T = P<sub>s</sub> − F<sub>A,s</sub> = {f(N8['ms']*g,2)} − {f(N8['Vs']*1e4,2)} ≈ 4,0 N. Khớp."])],
    dap=["a) 6 cm", "b) 0,4 kg", "c) ≈ 58,8 cm³; ≈ 0,459 kg", "d) 4 N"],
    nhan_dang="Thấy <b>vật nổi + vật gắn thêm</b> → viết cân bằng cho <b>cả hệ</b> (tổng F<sub>A</sub> = tổng P); cần lực dây thì tách riêng một vật.",
    bay=["Câu c quên lực đẩy Archimedes tác dụng lên quả cầu sắt (coi như chỉ thêm trọng lượng).", "Câu b lấy m = 0,4 kg rồi dùng luôn cho câu c (vật treo dưới nước nhẹ hơn vật đặt trên).", "Đổi cm³ ↔ m³ sai 10³ lần."])

bai(n=9, muc="C", lvl=VDC, ten="Cốc nổi trong bình — mực nước thay đổi thế nào?", fig=fig_coc(),
    de=["Bình hình trụ đủ cao, tiết diện S = 200 cm², đựng nước, mực nước cao 20 cm. Thả vào bình một cốc hình trụ thành mỏng (bỏ qua thể tích thành cốc), khối lượng 200 g, tiết diện 50 cm², cao 12 cm; cốc nổi thẳng đứng, miệng hướng lên, đáy không chạm đáy bình. Khối lượng riêng của nước 1 g/cm³.",
        "a) Cốc chìm sâu bao nhiêu? Mực nước trong bình dâng thêm bao nhiêu?",
        "b) Rót vào cốc 100 g nước. Cốc chìm sâu bao nhiêu? Mực nước trong bình dâng thêm bao nhiêu so với câu a?",
        "c) Thay vì rót nước, bỏ vào cốc một hòn sỏi 100 g (khối lượng riêng 2,5 g/cm³). Tính độ dâng thêm của mực nước trong bình (so với câu a) trong hai trường hợp: sỏi nằm trong cốc, và sỏi được thả thẳng xuống đáy bình (cốc rỗng vẫn nổi). Trường hợp nào mực nước cao hơn, cao hơn bao nhiêu?",
        "d) Rót nước vào cốc tối đa bao nhiêu gam thì cốc vẫn chưa bị ngập (miệng cốc vừa chạm mặt nước)?"],
    goi_y=["Vật nổi chiếm chỗ một thể tích nước có <b>khối lượng bằng khối lượng vật</b> (F<sub>A</sub> = P ⇒ V<sub>chìm</sub>·D<sub>n</sub> = m). Mực nước dâng Δh = V<sub>chìm</sub>/S.",
           "Câu c: sỏi trong cốc thì chiếm chỗ theo <b>khối lượng</b> (nổi cùng cốc); sỏi dưới đáy thì chiếm chỗ theo <b>thể tích thật</b>. Thể tích nào lớn hơn khi D<sub>sỏi</sub> > D<sub>nước</sub>?",
           "Câu d: cốc chìm sâu nhất là 12 cm — tổng khối lượng cốc + nước trong cốc tối đa bằng bao nhiêu gam nước chiếm chỗ?"],
    giai=[("a) Cốc rỗng",
           [f"Nổi: V<sub>chìm</sub> = m<sub>cốc</sub>/D<sub>n</sub> = {N9['mc']} cm³ ⇒ chìm sâu x = {N9['mc']}/{N9['S2']} = <b>{f(N9['x_a'])} cm</b>.",
            f"Mực nước dâng Δh = V<sub>chìm</sub>/S = {N9['mc']}/{N9['S']} = <b>{f(N9['dh_a'])} cm</b>."]),
          ("b) Rót 100 g nước vào cốc",
           [f"V<sub>chìm</sub> = ({N9['mc']} + {N9['m_nuoc']})/1 = {N9['mc']+N9['m_nuoc']} cm³ ⇒ x = {N9['mc']+N9['m_nuoc']}/{N9['S2']} = <b>{f(N9['x_b'])} cm</b>.",
            f"Dâng thêm so với a: {N9['m_nuoc']}/{N9['S']} = <b>{f(N9['dh_b'])} cm</b> (bằng đúng như rót 100 g nước thẳng vào bình)."]),
          ("c) Sỏi trong cốc và sỏi dưới đáy",
           [f"Sỏi trong cốc: cốc nổi, chiếm thêm {N9['m_soi']} cm³ ⇒ dâng thêm {N9['m_soi']}/{N9['S']} = <b>{f(N9['dh_c1'])} cm</b>.",
            f"Sỏi dưới đáy: chiếm đúng thể tích sỏi V = {N9['m_soi']}/{f(N9['D_soi'])} = {f(N9['V_soi'])} cm³ ⇒ dâng thêm {f(N9['V_soi'])}/{N9['S']} = <b>{f(N9['dh_c2'])} cm</b>.",
            f"Sỏi trong cốc làm mực nước <b>cao hơn</b> {f(N9['dh_c1']-N9['dh_c2'])} cm. Lí do: khi nổi, sỏi \"mượn\" cốc để chiếm chỗ theo khối lượng (100 cm³ nước), lớn hơn thể tích thật 40 cm³ vì sỏi nặng hơn nước."]),
          ("d) Lượng nước tối đa",
           [f"Chìm tối đa 12 cm ⇒ V<sub>chìm,max</sub> = {N9['S2']} × {N9['hc']} = {N9['S2']*N9['hc']} cm³ ⇒ đỡ được tối đa {N9['S2']*N9['hc']} g.",
            f"m<sub>nước,max</sub> = {N9['S2']*N9['hc']} − {N9['mc']} = <b>{f(N9['m_max'],0)} g</b>."])],
    dap=["a) chìm 4 cm; dâng 1 cm", "b) chìm 6 cm; dâng thêm 0,5 cm", "c) trong cốc: +0,5 cm; dưới đáy: +0,2 cm → cao hơn 0,3 cm", "d) 400 g"],
    nhan_dang="Thấy <b>vật nổi trong bình, hỏi mực nước</b> → vật nổi chiếm chỗ theo <b>khối lượng</b>, vật chìm chiếm chỗ theo <b>thể tích</b>.",
    bay=["Câu c cho rằng hai trường hợp như nhau vì \"cùng hòn sỏi\".", "Quên chia cho tiết diện của bình (lấy tiết diện cốc) khi tính Δh.", "Câu a lấy Δh = x (độ chìm)."])

bai(n=10, muc="D", lvl=VD, ten="Ô tô lên dốc — lực kéo, công suất, nhiên liệu", fig=fig_doc(),
    de=["Ô tô khối lượng 1 200 kg chuyển động đều lên một dốc dài 1 km, cao 50 m với tốc độ 36 km/h. Khi lên dốc, lực cản chuyển động (ma sát và không khí) không đổi và bằng 400 N. Lấy g = 10 N/kg.",
        "a) Tính lực kéo của động cơ và công suất của động cơ.",
        "b) Động cơ có hiệu suất 25 %; xăng toả 4,6·10⁷ J/kg khi cháy. Tính lượng xăng tiêu thụ khi xe lên hết dốc.",
        "c) Khi xuống dốc này, tài xế tắt máy và đạp phanh nhẹ để xe chạy đều. Tổng lực cản (ma sát, không khí và phanh) lúc đó bằng bao nhiêu?"],
    goi_y=["Lực kéo khi lên dốc đều phải làm hai việc: <b>nâng xe lên cao</b> (chống trọng lực) và <b>thắng lực cản</b>. Công suất = F·v.",
           "Chuyển động <b>đều</b> trên dốc: công của lực kéo = công nâng (P·h) + công thắng cản (F<sub>c</sub>·l). Tốc độ đổi sang m/s chưa?",
           "Câu c: xuống dốc, lực nào \"kéo\" xe thay cho động cơ? Chạy đều nghĩa là lực đó cân bằng với lực cản."],
    giai=[("a) Lực kéo và công suất",
           [f"P = {f(N10['P'],0)} N; v = 36 km/h = {N10['v']} m/s.",
            f"Lên đều: F<sub>k</sub>·l = P·h + F<sub>c</sub>·l ⇒ F<sub>k</sub> = P·h/l + F<sub>c</sub> = {f(N10['P'],0)} × {N10['h']}/{N10['l']} + {N10['Fc']} = <b>{f(N10['Fk'],0)} N</b>.",
            f"𝒫 = F<sub>k</sub>·v = {f(N10['Fk'],0)} × {N10['v']} = <b>{f(N10['Pcs']/1000)} kW</b>."]),
          ("b) Lượng xăng",
           [f"Công động cơ sinh ra: A = F<sub>k</sub>·l = {f(N10['Fk'],0)} × {N10['l']} = {f(N10['A']/1e6)}·10⁶ J.",
            f"Nhiệt lượng xăng phải toả: Q = A/H = {f(N10['A']/1e6)}·10⁶/0,25 = {f(N10['Q']/1e6)}·10⁶ J.",
            f"m = Q/q = {f(N10['Q']/1e6)}·10⁶/(4,6·10⁷) ≈ <b>{f(N10['mx'],3)} kg ≈ 87 g</b>."]),
          ("c) Xuống dốc tắt máy, chạy đều",
           [f"Thành phần trọng lực kéo xe xuống dọc dốc có độ lớn P·h/l = {f(N10['Fc_xuong'],0)} N (lợi về lực của mặt nghiêng).",
            f"Chạy đều ⇒ tổng lực cản = <b>{f(N10['Fc_xuong'],0)} N</b>; trong đó ma sát và không khí vẫn khoảng 400 N, phần còn lại 200 N là lực phanh."])],
    dap=["a) 1 000 N; 10 kW", "b) ≈ 0,087 kg (87 g)", "c) 600 N"],
    nhan_dang="Thấy <b>xe lên dốc đều, có lực cản</b> → F<sub>kéo</sub> = <b>P·h/l + F<sub>cản</sub></b>; công suất = F·v (v đổi ra m/s).",
    bay=["Quên đổi 36 km/h ra m/s.", "Nhân hiệu suất với công (Q = A·H) thay vì chia.", "Câu c trả lời 400 N (không nhận ra lực cản phải cân bằng với thành phần trọng lực)."])

bai(n=11, muc="D", lvl=VDC, ten="Hai máng nhẵn nối bằng đoạn đường có ma sát", fig=fig_mang(),
    de=["Vật nhỏ khối lượng 500 g được thả không vận tốc đầu từ độ cao h = 5 m trên máng cong nhẵn (1). Chân máng nối với đoạn đường nằm ngang MN dài 10 m; trên MN lực ma sát không đổi 1 N. Đầu N nối với máng cong nhẵn (2). Lấy g = 10 N/kg, bỏ qua sức cản không khí.",
        "a) Tính tốc độ của vật khi tới M.",
        "b) Vật lên tới độ cao lớn nhất bao nhiêu trên máng (2)?",
        "c) Cuối cùng vật dừng lại ở đâu? Tính tổng quãng đường vật đã đi trên đoạn MN."],
    goi_y=["Trên máng nhẵn: cơ năng bảo toàn (thế năng ↔ động năng). Trên MN: cơ năng <b>giảm đúng bằng công của lực ma sát</b> A<sub>ms</sub> = F<sub>ms</sub>·s.",
           "Trước khi viết công thức, hỏi: đoạn nào có lực không bảo toàn? Chỉ đoạn đó mới làm mất cơ năng. Vật có thể đi qua MN <b>nhiều lần</b>.",
           "Câu c: toàn bộ cơ năng ban đầu cuối cùng biến hết thành công ma sát: W₀ = F<sub>ms</sub>·s<sub>tổng</sub>. Rồi lần theo từng lượt để biết dừng ở đâu."],
    giai=[("a) Tốc độ tại M",
           [f"Cơ năng ban đầu W₀ = m·g·h = 0,5 × 10 × 5 = {f(N11['W'])} J.",
            f"Máng (1) nhẵn: ½mv² = W₀ ⇒ v = √(2gh) = √(2 × 10 × 5) = <b>{f(N11['v'])} m/s</b>."]),
          ("b) Độ cao trên máng (2)",
           [f"Qua MN lần 1 mất A<sub>ms</sub> = {N11['Fms']} × {N11['MN']} = {f(N11['A_MN'])} J ⇒ tại N còn W = {f(N11['W'])} − {f(N11['A_MN'])} = {f(N11['W_N'])} J.",
            f"Máng (2) nhẵn: m·g·h₂ = {f(N11['W_N'])} ⇒ h₂ = {f(N11['W_N'])}/(0,5 × 10) = <b>{f(N11['h2'])} m</b>."]),
          ("c) Vị trí dừng và tổng quãng đường trên MN",
           [f"Tổng quãng đường trên MN: F<sub>ms</sub>·s = W₀ ⇒ s = {f(N11['W'])}/{N11['Fms']} = <b>{f(N11['s_tong'])} m</b>.",
            f"Lần theo: về tới M lần 2 còn {f(N11['W_N'])} − {f(N11['A_MN'])} = {f(N11['W_M2'])} J ⇒ lên máng (1) cao {f(N11['h1b'])} m rồi quay lại M.",
            f"Từ M đi tiếp được {f(N11['W_M2'])}/{N11['Fms']} = {f(N11['s_cuoi'])} m < 10 m ⇒ dừng trên MN, <b>cách M {f(N11['s_cuoi'])} m</b> (cách N 5 m).",
            f"Kiểm: 10 + 10 + 5 = 25 m. Khớp."])],
    dap=["a) 10 m/s", "b) 3 m", "c) dừng cách M 5 m (giữa MN); tổng quãng đường trên MN là 25 m"],
    nhan_dang="Thấy <b>máng nhẵn + đoạn có ma sát</b> → cơ năng chỉ mất trên đoạn ma sát: <b>ΔW = F<sub>ms</sub>·s</b>; hỏi \"dừng ở đâu\" thì lấy W₀/F<sub>ms</sub> rồi lần theo.",
    bay=["Câu c kết luận vật dừng ở N hoặc dừng ngay lần đầu qua MN.", "Dùng v tại M để tính h₂ mà quên trừ công ma sát.", "Tính tổng quãng đường 25 m rồi nói dừng cách M 25 m (quên MN chỉ dài 10 m)."])

bai(n=12, muc="D", lvl=VDC, ten="Máy bơm nước — công suất, hiệu suất, động năng dòng nước", fig=fig_bom(),
    de=["Một máy bơm có công suất tiêu thụ điện 1,5 kW, hiệu suất 60 %, hút nước từ giếng lên bể đặt cao hơn mặt nước giếng 10 m. Khối lượng riêng của nước 1 000 kg/m³, g = 10 N/kg.",
        "a) Bỏ qua động năng của nước. Mỗi giây máy bơm được bao nhiêu lít nước?",
        "b) Thực tế nước ra khỏi vòi (ở miệng bể) với tốc độ 4 m/s. Tính lại lượng nước bơm được mỗi giây.",
        "c) Với kết quả câu b, bơm đầy bể 30 m³ mất bao lâu? Máy tiêu thụ bao nhiêu kWh điện?"],
    goi_y=["Công suất có ích = hiệu suất × công suất máy. Công có ích mỗi giây dùng để tăng <b>thế năng</b> (và câu b thêm <b>động năng</b>) cho lượng nước bơm trong giây đó.",
           "Với 1 kg nước: thế năng tăng g·h, động năng ½v². Năng lượng có ích trong 1 s chia cho năng lượng cần cho 1 kg ⇒ số kg mỗi giây.",
           "Điện năng tiêu thụ tính theo công suất <b>toàn phần</b> (1,5 kW), không phải phần có ích."],
    giai=[("a) Bỏ qua động năng",
           [f"𝒫<sub>ích</sub> = H·𝒫 = 0,6 × 1 500 = {f(N12['Pi'],0)} W.",
            f"Mỗi giây: 𝒫<sub>ích</sub> = m·g·h ⇒ m = {f(N12['Pi'],0)}/(10 × 10) = <b>{f(N12['q_a'])} kg = 9 L</b>."]),
          ("b) Kể cả động năng",
           [f"Mỗi kg nước cần: g·h + ½v² = 100 + ½ × 4² = {f(N12['e_kg'],0)} J.",
            f"m = {f(N12['Pi'],0)}/{f(N12['e_kg'],0)} ≈ <b>{f(N12['q_b'],2)} kg/s ≈ 8,33 L/s</b> (ít hơn câu a vì một phần năng lượng thành động năng)."]),
          ("c) Thời gian và điện năng",
           [f"t = {N12['V_be']*1000}/{f(N12['q_b'],2)} = <b>{f(N12['t'],0)} s = 1 h</b>.",
            f"Điện năng: A = 𝒫·t = 1,5 kW × 1 h = <b>{f(N12['E_kWh'],2)} kWh</b>."])],
    dap=["a) 9 L/s", "b) ≈ 8,33 L/s", "c) 3 600 s = 1 h; 1,5 kWh"],
    nhan_dang="Thấy <b>máy bơm, hiệu suất, lưu lượng</b> → viết <b>năng lượng có ích trong 1 s</b> = (g·h + ½v²) × khối lượng nước mỗi giây.",
    bay=["Quên nhân hiệu suất (lấy 1 500 W làm công suất có ích).", "Câu c tính điện năng bằng 900 W.", "Câu b lấy động năng ½mv² với m là 9 kg của câu a (vòng luẩn quẩn) thay vì tính cho 1 kg."])

# ---------------- ghép HTML ----------------
MUC = {"A": "Chuyển động cơ học", "B": "Lực, đòn bẩy, máy cơ đơn giản", "C": "Áp suất chất lỏng, lực đẩy Archimedes", "D": "Công, công suất, năng lượng"}
EYE = "Khoa học tự nhiên 9 · Vật lí · Lớp 9 chuyên / HSG"

def de_html():
    out = ""; cur = None
    for b in BAI:
        if b["muc"] != cur:
            cur = b["muc"]; out += muc(cur, MUC[cur])
        de = "<br>".join(b["de"])
        tag = f'<b class="n">Bài {b["n"]} · {b["lvl"]}</b> — <b>{b["ten"]}</b><br>'
        figh = fig(b["fig"]) if b["fig"] else ""
        out += f'<div class="q">{figh}<div class="txt">{tag}{de}</div></div>'
    return out

def goi_y_html():
    out = muc("E", "Gợi ý (che lại, chỉ mở khi bí quá 10 phút)")
    out += '<p><i>Ba tầng gợi ý theo thứ tự: 1 — kiến thức cần gọi lại; 2 — câu hỏi về điều kiện áp dụng; 3 — hướng tính. Chỉ mở tầng kế khi tầng trước chưa đủ.</i></p>'
    for b in BAI:
        out += f'<div class="sol"><b>Bài {b["n"]}.</b><ol style="margin:1mm 0 0 5mm;padding:0">' + "".join(f"<li>{s}</li>" for s in b["goi_y"]) + "</ol></div>"
    return out

def giai_html():
    out = ""; cur = None
    for b in BAI:
        if b["muc"] != cur:
            cur = b["muc"]; out += muc(cur, MUC[cur])
        out += f'<div class="keep"><div class="sol" style="margin-top:5mm"><b style="font-size:12.5pt;color:#1f3a5f">Bài {b["n"]} · {b["lvl"]} — {b["ten"]}</b></div>'
        for i, (tit, lines) in enumerate(b["giai"]):
            out += f'<div class="sol"><b>{tit}</b><br>' + "<br>".join(lines) + "</div>" + ("</div>" if i == 0 else "")
        out += '<div class="keep"><div class="note"><span class="lab">Đáp số</span>' + "<br>".join(b["dap"]) + "</div>"
        out += f'<p style="font-size:10.5pt;color:#444"><b>Nhận dạng:</b> {b["nhan_dang"]}</p>'
        out += '<div class="sol"><div class="bad"><b>Bẫy thường gặp:</b><br>' + "<br>".join("• " + s for s in b["bay"]) + "</div></div></div>"
    return out

bang = '<table><tr><th>Bài</th><th>Mảng</th><th>Mức</th><th>Nội dung</th></tr>' + "".join(
    f'<tr><td>{b["n"]}</td><td>{b["muc"]}. {MUC[b["muc"]]}</td><td>{b["lvl"]}</td><td>{b["ten"]}</td></tr>' for b in BAI) + "</table>"

head = tieu_de(EYE, "Bài tập tự luận Cơ học — Vận dụng và Vận dụng cao", "12 bài · 4 mảng · mỗi bài 3–4 ý, ý sau khó hơn ý trước<br>Họ tên: ………………………………………… Lớp: ………")
head += '''<div class="box"><span class="lab">Quy ước và cách làm</span>g = 10 N/kg. Khối lượng riêng của nước 1 000 kg/m³ (1 g/cm³), trọng lượng riêng 10 000 N/m³. Bỏ qua sức cản không khí nếu đề không nói.<br>
<b>Trước khi giải mỗi bài, viết ra giấy 3 dòng:</b> (1) bài dùng kiến thức gì; (2) điều kiện để dùng được kiến thức đó có thoả không; (3) công thức. Rồi mới tính.<br>
<b>Trình bày:</b> mỗi bước một dòng, có chữ rồi mới thế số; kết quả 3–4 chữ số có nghĩa, kèm đơn vị. Gợi ý ở cuối đề — chỉ mở khi đã nghĩ quá 10 phút. Lời giải ở tập riêng: làm xong mới đối chiếu, sai thì gấp lại giải lại từ đầu.</div>'''
dung(str(HERE / "bai-tap-tu-luan-co-hoc.pdf"), "Bài tập tự luận Cơ học VD–VDC", "Bài tập tự luận Cơ học · KHTN 9 chuyên",
     head + muc("0", "Bảng tổng quan") + bang + de_html() + goi_y_html() + '<p style="text-align:center;margin-top:8mm">— HẾT —</p>', school=False)

FIGN[0] = 0
da = tieu_de(EYE, "Lời giải, đáp số và bẫy thường gặp — Bài tập tự luận Cơ học", "Dành cho người chữa bài · đối chiếu sau khi học sinh đã tự làm")
da += '''<div class="box"><span class="lab">Cách dùng</span>Mỗi bài: lời giải từng ý (chữ trước, số sau) → ô Đáp số → dòng Nhận dạng → Bẫy thường gặp. Chữa bài: chỉ chỗ thiếu và hỏi về điều kiện áp dụng, không giải hộ. Học sinh sai: gấp vở, giải lại trên giấy trắng; 3 ngày sau che lời giải giải lại.</div>'''
da += giai_html()
dung(str(HERE / "bai-tap-tu-luan-co-hoc-loi-giai.pdf"), "Bài tập tự luận Cơ học — Lời giải", "Bài tập tự luận Cơ học · Lời giải", da, school=False)

# ---------------- xuất cho agent kiểm (chỉ đề, không đáp án) ----------------
def strip(s): return re.sub(r"<[^>]+>", "", s)
md = "# Đề (chỉ đề, không đáp án) — để giải độc lập\n\nQuy ước: g = 10 N/kg; D_nước = 1000 kg/m³; d_nước = 10 000 N/m³.\n\n"
for b in BAI:
    md += f"## Bài {b['n']} ({b['lvl']}) — {b['ten']}\n" + "\n".join(strip(s) for s in b["de"]) + "\n\n"
    if b["fig"]: md += "(Có hình: " + {1:"đường AB, hai xe đi ngược chiều, xe máy ở giữa",3:"sông chảy từ A về B, ca nô và bè",4:"tàu, cầu 400 m, cột điện",5:"thanh AB tựa O, vật ở A, F ở B",6:"mặt nghiêng, ròng rọc động gắn vật, dây song song mặt nghiêng, một đầu dây buộc cọc ở đỉnh, nhánh kia qua ròng rọc cố định ở đỉnh tới tay kéo",7:"bình thông nhau, pittông + quả cân ở nhánh lớn",8:"gỗ nổi, quả cầu sắt treo dưới",9:"bình trụ, cốc nổi",10:"ô tô trên dốc",11:"máng (1) – MN – máng (2)",12:"giếng, bơm, bể"}.get(b["n"],"") + ")\n\n"
(HERE / "de-chi-de.md").write_text(md)
json.dump({b["n"]: b["dap"] for b in BAI}, open(HERE / "dap-an.json", "w"), ensure_ascii=False, indent=1)
print("OK", len(BAI), "bài;", FIGN, "hình")
