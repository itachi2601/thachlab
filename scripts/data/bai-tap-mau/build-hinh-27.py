"""Bài 27 (Bài 8. Mô tả sóng, VL11): dựng 5 dạng bài tập mẫu, hình mô phỏng sóng TÍNH THẬT, phân tích, lời giải, buoc[] tự giải từng bước.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-27.py   → ghi scripts/data/bai-tap-mau/27.json (review.checked=false cho tới khi kiểm chéo).

Mô phỏng sóng: sóng chạy y = A·cos(ωt − kx) dựng bằng MỘT đường hình sin dịch phải đúng λ mỗi chu kì (animateTransform, lặp n chu kì) —
chính xác theo công thức, không cần lấy mẫu; điểm dao động tại chỗ dùng 24 mẫu/chu kì nội suy tuyến tính (sai số < 1% biên độ)."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "27.json")
OLD = os.path.join(HERE, "old", "27.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
TOPIC_164 = "Bước sóng, chu kì, tần số, tốc độ truyền sóng"
TOPIC_165 = "Phương trình sóng và đồ thị sóng"

# ───────────── helper riêng của bài 27 (tiền tố w27) ─────────────
def pts_str(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def wave_pts(xa, xb, step, y0, A, lam, xo, ph=0.0):
    """Hình dạng sóng tại t=0: y = y0 − A·cos(2π(x−xo)/λ + ph)  (màn hình: y xuống, nên dấu − là 'lên')."""
    out, x = [], xa
    while x <= xb + 1e-9:
        out.append((x, y0 - A * math.cos(2 * math.pi * (x - xo) / lam + ph)))
        x += step
    return out

def smilr(attr, vals, dur, repeat=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" dur="{dur:.2f}s" '
            f'repeatCount="{repeat}" begin="indefinite" fill="freeze"/>')

def travel(cid, xl, xr, ytop, hgt, pts, lam, T_sim, n, color=GRN, w=2.4, grow=False):
    """Sóng chạy sang phải: đường hình sin dịch đúng λ mỗi T_sim, lặp n lần. grow=True: sóng lan dần từ x=xl (đầu sóng chạy cùng tốc độ v=λ/T)."""
    cw = (f'<animate attributeName="width" from="0" to="{xr - xl:.1f}" dur="{n * T_sim:.2f}s" begin="indefinite" fill="freeze"/>' if grow else "")
    return (f'<clipPath id="{cid}"><rect x="{xl}" y="{ytop}" width="{0 if grow else xr - xl}" height="{hgt}">{cw}</rect></clipPath>'
            f'<g clip-path="url(#{cid})"><g><polyline fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" points="{pts_str(pts)}"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{lam:.1f} 0" dur="{T_sim:.2f}s" repeatCount="{n}" '
            f'begin="indefinite" fill="freeze"/></g></g>')

def bob(cx, y0, A, theta, T_sim, n, N=24, r=5.5, fill=ORG):
    """Phần tử tại cx dao động tại chỗ: y = y0 − A·cos(θ − ωt), θ = pha tại cx của hình dạng sóng t=0."""
    vals = [y0 - A * math.cos(theta - 2 * math.pi * j / N) for j in range(N + 1)]
    return (f'<circle cx="{cx:.1f}" cy="{vals[0]:.1f}" r="{r}" fill="{fill}" stroke="currentColor" stroke-width="1.5">'
            f'{smilr("cy", vals, T_sim, n)}</circle>')

def base(y, x0=16, x1=404):
    return seg(x0, y, x1, y, "currentColor", 1.2, "4 4", .45)

# ───────────── Dạng 1: đếm ngọn sóng. 9 lần nhô lên / 20 s, λ = 4,5 m ⇒ T = 2,5 s, v = 1,8 m/s ─────────────
def d1(k):
    p = f"w27a{k}"; y0, A, lam, xb = 98, 24, 90, 210            # 4,5 m ↔ 90 px
    pts = wave_pts(16 - lam, 404, 4, y0, A, lam, xb, 0)
    if k == 0:
        T_sim, n = 1.25, 8                                        # 8 chu kì × 2,5 s = 20 s thật, chạy nhanh 2 lần
        b = defs(p) + base(y0) + travel("cpw27a", 16, 404, 24, 150, pts, lam, T_sim, n)
        b += bob(xb, y0, A, 0, T_sim, n) + lbl(xb, y0 - A - 16, "phao", ORG, 13, "middle", "700")
        b += arrow(p, "b", 20, 30, 70, 30, 3) + lbl(76, 35, "sóng truyền", BLUE, 13, "start", "700")
        b += lbl(404, 35, "T = ?    v = ?", ORG, 13, "end", "700")
        b += lbl(16, 178, "Hai ngọn sóng liên tiếp cách nhau 4,5 m", "currentColor", 13, "start", "400")
        return fig("d1-0", "0 0 420 190", "Sóng chạy trên mặt hồ, chiếc phao chỉ nhô lên hạ xuống tại chỗ",
                   b, "Mô phỏng: sóng chạy sang phải, phao chỉ nhô lên hạ xuống tại chỗ; chạy nhanh 2 lần (10 s thay cho 20 s). Sóng tính theo công thức.")
    b = defs(p) + base(y0) + poly(pts, GRN, 2.4)
    b += dot(xb, y0 - A, 5.5, ORG) + lbl(xb - 12, y0 - A - 4, "phao", ORG, 13, "end", "700")
    b += dot(xb + lam, y0 - A, 4, GRN)
    b += dim(p, "b", xb, y0 - A - 22, xb + lam, y0 - A - 22, "λ = 4,5 m", xb + lam / 2, y0 - A - 30, "middle")
    b += lbl(16, 150, "9 lần nhô lên → 8 chu kì (không phải 9)", ORG, 13, "start", "700")
    b += lbl(16, 172, "Δt = 20 s ứng với 8 chu kì", "currentColor", 13, "start", "400")
    return fig("d1-2", "0 0 420 190", "Hai ngọn sóng liên tiếp cách nhau một bước sóng, chín lần nhô lên ứng với tám chu kì", b, "Dữ kiện: bước sóng và số chu kì. " + NOTE)

# ───────────── Dạng 2: hai điểm trên phương truyền. v = 1,2 m/s, f = 20 Hz ⇒ λ = 6 cm; d = 10,5 cm ─────────────
def d2(k):
    p = f"w27b{k}"; y0, A, lam, xo = 98, 26, 96, 30            # λ = 96 px (minh hoạ), các chấm cách nhau λ/4
    if k == 0:
        pts = wave_pts(16 - lam, 404, 4, y0, A, lam, xo, 0)
        T_sim, n = 1.5, 4
        b = defs(p) + base(y0) + travel("cpw27b", 16, 404, 24, 150, pts, lam, T_sim, n)
        for j in range(5):
            x = 130 + j * lam / 4
            b += bob(x, y0, A, 2 * math.pi * (x - xo) / lam, T_sim, n, 24, 5)
        b += arrow(p, "b", 20, 30, 70, 30, 3) + lbl(76, 35, "sóng truyền", BLUE, 13, "start", "700")
        b += lbl(16, 178, "Các chấm cam: phần tử dây, chỉ dao động tại chỗ", "currentColor", 13, "start", "400")
        return fig("d2-0", "0 0 420 190", "Sóng ngang chạy trên dây, năm phần tử dây dao động tại chỗ với pha lệch dần",
                   b, "Mô phỏng: sóng chạy trên dây; mỗi chấm dao động tại chỗ, chấm càng xa nguồn càng trễ pha. Sóng tính theo công thức; bấm Chạy mô phỏng.")
    ya = 96
    b = defs(p) + arrow(p, "g", 24, ya, 396, ya, 2.4) + lbl(398, ya - 8, "x", GRN, 13, "end", "700")
    b += dot(100, ya, 6, ORG) + dot(300, ya, 6, ORG) + lbl(100, ya + 24, "M", ORG, 14, "middle", "700") + lbl(300, ya + 24, "N", ORG, 14, "middle", "700")
    b += dim(p, "b", 100, ya - 34, 300, ya - 34, "d = 10,5 cm", 200, ya - 44, "middle")
    b += arrow(p, "r", 150, ya + 44, 250, ya + 44, 3) + lbl(200, ya + 66, "sóng truyền M → N", RED, 13, "middle", "700")
    b += lbl(24, 24, "Cùng một phương truyền", "currentColor", 13, "start", "400") + lbl(396, 24, "λ = ?   Δφ = ?", ORG, 13, "end", "700")
    return fig("d2-2", "0 0 420 180", "Hai điểm M, N trên cùng phương truyền sóng cách nhau 10,5 cm", b, "Dữ kiện: hai điểm cùng phương truyền, khoảng cách d. " + NOTE)

# ───────────── Dạng 3: u = 5cos(8πt − 0,2πx) cm  ⇒ A=5, f=4, λ=10 cm, v=0,4 m/s, vmax=40π ─────────────
def d3(k):
    p = f"w27c{k}"
    if k == 0:
        y0, A, lam, xo = 98, 30, 100, 40
        pts = wave_pts(xo - lam, 404, 4, y0, A, lam, xo, 0)
        T_sim, n = 1.0, 5
        b = defs(p) + base(y0, xo, 404) + travel("cpw27c", xo, 404, 24, 150, pts, lam, T_sim, n)
        b += bob(xo, y0, A, 0, T_sim, n, 24, 6) + lbl(xo - 8, y0 + 24, "O", ORG, 14, "end", "700")
        b += arrow(p, "b", 70, 30, 120, 30, 3) + lbl(126, 35, "sóng truyền", BLUE, 13, "start", "700")
        b += lbl(16, 178, "u = 5cos(8πt − 0,2πx) cm  (x: cm, t: s)", "currentColor", 13, "start", "700")
        return fig("d3-0", "0 0 420 190", "Sóng chạy trên dây từ đầu O, đầu O dao động tại chỗ",
                   b, "Mô phỏng: sóng chạy trên dây từ O (chạy chậm 4 lần). Sóng tính theo công thức; bấm Chạy mô phỏng.")
    b = defs(p)
    b += lbl(24, 40, "Phương trình của đề:", "currentColor", 13, "start", "400")
    b += (f'<text x="24" y="72" font-size="20" font-weight="700" fill="currentColor">u = <tspan fill="{RED}">5</tspan> cos( <tspan fill="{BLUE}">8π</tspan> t − '
          f'<tspan fill="{ORG}">0,2π</tspan> x )</text>')
    b += lbl(24, 110, "Dạng chuẩn:", "currentColor", 13, "start", "400")
    b += (f'<text x="24" y="142" font-size="20" font-weight="700" fill="currentColor">u = <tspan fill="{RED}">A</tspan> cos( <tspan fill="{BLUE}">ω</tspan> t − '
          f'<tspan fill="{ORG}">(2π/λ)</tspan> x )</text>')
    b += lbl(24, 176, "Ghép từng màu: A ↔ 5 · ω ↔ hệ số của t · 2π/λ ↔ hệ số của x", "currentColor", 12, "start", "400")
    return fig("d3-2", "0 0 420 190", "Ghép phương trình của đề với dạng chuẩn theo từng màu", b, "Dữ kiện: so từng hệ số với dạng chuẩn. " + NOTE)

# ───────────── Dạng 4: u_O = 4cos(20πt − π/2) cm, v = 1,5 m/s, d = 20 cm ⇒ λ = 15 cm, u_M = 4cos(20πt − 19π/6) ─────────────
def d4(k):
    p = f"w27d{k}"
    if k == 0:
        y0, A, lam, xo = 98, 28, 60, 50                         # λ = 60 px (minh hoạ)
        T_sim, n = 1.0, 5                                        # 5 chu kì: đầu sóng đi 5λ, chạy chậm 10 lần (0,5 s thật)
        pts = wave_pts(xo - lam, 404, 4, y0, A, lam, xo, math.pi / 2)    # u(O,t)=A·sin(ωt): xuất phát từ vị trí cân bằng, đi lên
        b = defs(p) + base(y0, xo, 404) + travel("cpw27d", xo, xo + n * lam, 24, 150, pts, lam, T_sim, n, GRN, 2.4, grow=True)
        b += bob(xo, y0, A, math.pi / 2, T_sim, n, 24, 6) + lbl(xo - 8, y0 + 24, "O", ORG, 14, "end", "700")
        b += arrow(p, "b", 90, 30, 140, 30, 3) + lbl(146, 35, "sóng truyền", BLUE, 13, "start", "700")
        b += lbl(16, 178, "Nguồn O bắt đầu dao động tại t = 0; sóng lan dần sang phải", "currentColor", 13, "start", "400")
        return fig("d4-0", "0 0 420 190", "Nguồn O bắt đầu dao động, sóng lan dần ra xa trên dây",
                   b, "Mô phỏng: đầu sóng chạy cùng tốc độ truyền sóng (chạy chậm 10 lần). Sóng tính theo công thức; bấm Chạy mô phỏng.")
    ya = 88
    b = defs(p) + arrow(p, "g", 24, ya, 396, ya, 2.4) + lbl(398, ya - 8, "x", GRN, 13, "end", "700")
    b += dot(60, ya, 6, ORG) + dot(320, ya, 6, ORG) + lbl(60, ya + 24, "O", ORG, 14, "middle", "700") + lbl(320, ya + 24, "M", ORG, 14, "middle", "700")
    b += dim(p, "b", 60, ya - 30, 320, ya - 30, "d = 20 cm", 190, ya - 40, "middle")
    b += arrow(p, "r", 120, ya + 38, 220, ya + 38, 3) + lbl(230, ya + 43, "v = 1,5 m/s", RED, 13, "start", "700")
    b += lbl(24, 18, "u_O = 4cos(20πt − π/2) cm", "currentColor", 13, "start", "700")
    b += lbl(24, 164, "⚠ u_M chỉ đúng khi sóng đã tới M", ORG, 13, "start", "700")
    b += lbl(24, 186, "So t = 0,15 s với thời gian sóng đi từ O tới M", "currentColor", 13, "start", "400")
    return fig("d4-2", "0 0 420 198", "Nguồn O, điểm M cách O 20 cm, sóng truyền sang phải với tốc độ 1,5 m/s", b, "Dữ kiện: khoảng cách d, tốc độ v, thời điểm cần xét. " + NOTE)

# ───────────── Dạng 5: hai đồ thị. u(x,t)=3cos(5πt − πx/12 + π/2) cm: λ=24 cm, T=0,4 s, v=60 cm/s ─────────────
YA, YB = 86, 246                         # trục hoành của hình (a), (b)
XO, SXA, SXB, SY = 52, 9.0, 412.0, 15.0  # px/cm, px/s, px/cm biên độ

def graphs(p, ann=False):
    """Hai đồ thị của đề: (a) u theo x lúc t=0; (b) u theo t của điểm M (x=6 cm). ann=True thêm kích thước λ, T và hai điểm M, N."""
    b = ""
    for xc in range(0, 37, 6):
        X = XO + SXA * xc
        b += seg(X, YA - 52, X, YA + 52, "currentColor", 1, "2 4", .22) + lbl(X, YA + 70, f"{xc}", "currentColor", 12, "middle", "400")
    for tc in range(0, 5):
        X = XO + SXB * 0.2 * tc
        b += seg(X, YB - 52, X, YB + 52, "currentColor", 1, "2 4", .22) + lbl(X, YB + 70, ("0" if tc == 0 else f"0,{2 * tc}"), "currentColor", 12, "middle", "400")
    for Y0 in (YA, YB):
        for s in (1, -1):
            b += seg(XO, Y0 - s * 3 * SY, XO + 330, Y0 - s * 3 * SY, "currentColor", 1, "2 4", .22)
            b += lbl(XO - 8, Y0 - s * 3 * SY + 4, "3" if s == 1 else "−3", "currentColor", 12, "end", "400")
        b += arrow(p, "g", XO - 8, Y0, XO + 346, Y0, 2) + arrow(p, "g", XO, Y0 + 54, XO, Y0 - 58, 2)
        b += lbl(XO + 6, Y0 - 66, "u (cm)", GRN, 12, "start", "700")
    b += lbl(414, YA + 22, "x (cm)", GRN, 12, "end", "700") + lbl(414, YB + 22, "t (s)", GRN, 12, "end", "700")
    ca = [(XO + SXA * x / 2, YA - SY * 3 * math.sin(math.pi * (x / 2) / 12)) for x in range(0, 73)]
    cb = [(XO + SXB * t / 100, YB - SY * 3 * math.cos(5 * math.pi * t / 100)) for t in range(0, 81)]
    b += poly(ca, GRN, 2.4) + poly(cb, GRN, 2.4)
    b += lbl(414, YA - 70, "(a) li độ theo x, tại t = 0", "currentColor", 12, "end", "700")
    b += lbl(414, YB - 70, "(b) li độ theo t, điểm M (x = 6 cm)", "currentColor", 12, "end", "700")
    if ann:
        X6, X30, yc = XO + SXA * 6, XO + SXA * 30, YA - 3 * SY
        b += dim(p, "b", X6, yc - 12, X30, yc - 12, "λ = ?", (X6 + X30) / 2, yc - 20, "middle")
        b += dot(X6, yc, 5, ORG) + lbl(X6 - 8, yc + 18, "M", ORG, 13, "end", "700")
        XN = XO + SXA * 15
        b += dot(XN, YA - SY * 3 * math.sin(math.pi * 15 / 12), 5, RED) + lbl(XN - 10, YA - SY * 3 * math.sin(math.pi * 15 / 12) + 18, "N (cách M 9 cm)", RED, 12, "end", "700")
        X0, X4 = XO, XO + SXB * 0.4
        b += dim(p, "b", X0 + 2, YB - 3 * SY - 12, X4, YB - 3 * SY - 12, "T = ?", (X0 + X4) / 2, YB - 3 * SY - 20, "middle")
    return b

def static_graph_figure():
    """Hình của ĐỀ (không có data-bt nên strip() không xoá)."""
    p = "w27e"
    return ('<figure class="fig" data-tl="1"><svg viewBox="0 0 420 330" role="img" aria-label="Hai đồ thị: li độ theo toạ độ x tại t bằng 0 và li độ theo thời gian của điểm M">'
            + defs(p) + graphs(p) + '</svg><figcaption>Hình (a): đồ thị u – x. Hình (b): đồ thị u – t của điểm M.</figcaption></figure>')

def d5(k):
    p = f"w27e{k}"
    if k == 0:
        lam, T_sim, n = 216, 2.0, 2                              # λ = 24 cm ↔ 216 px; mỗi chu kì mô phỏng 2 s (chậm 5 lần)
        y0, A = 70, 3 * SY
        pts = wave_pts(XO - lam, XO + 330, 4, y0, A, lam, XO, -math.pi / 2)     # u(x,0) = 3·sin(πx/12)
        b = defs(p) + base(y0, XO, XO + 330) + lbl(XO - 8, y0 + 4, "dây", "currentColor", 12, "end", "400")
        b += travel("cpw27e", XO, XO + 330, 22, 100, pts, lam, T_sim, n)
        xm = XO + SXA * 6
        b += seg(xm, y0 - A - 10, xm, y0 + A + 10, ORG, 1.4, "4 3", .8) + lbl(xm, y0 - A - 14, "M", ORG, 13, "middle", "700")
        b += bob(xm, y0, A, 2 * math.pi * (xm - XO) / lam - math.pi / 2, T_sim, n, 24, 5.5)
        # đồ thị u–t của M vẽ dần: x tỉ lệ thời gian, 2 chu kì
        yb = 190; x0t, wt = 52, 360
        ct = [(x0t + wt * j / 96, yb - A * math.cos(2 * math.pi * 2 * j / 96)) for j in range(97)]
        b += arrow(p, "g", x0t - 8, yb, x0t + wt + 14, yb, 2) + arrow(p, "g", x0t, yb + 40, x0t, yb - 44, 2)
        b += lbl(x0t + 10, yb - 44, "u của M", GRN, 12, "start", "700") + lbl(414, yb + 18, "t", GRN, 12, "end", "700")
        b += (f'<polyline fill="none" stroke="{GRN}" stroke-width="2.4" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" points="{pts_str(ct)}">'
              f'<animate attributeName="stroke-dashoffset" from="1" to="0" dur="{n * T_sim:.2f}s" begin="indefinite" fill="freeze"/></polyline>')
        vals = [yb - A * math.cos(2 * math.pi * 2 * j / 48) for j in range(49)]
        b += (f'<circle cx="{x0t}" cy="{vals[0]:.1f}" r="5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">'
              f'<animate attributeName="cx" from="{x0t}" to="{x0t + wt}" dur="{n * T_sim:.2f}s" begin="indefinite" fill="freeze"/>'
              f'<animate attributeName="cy" values="{";".join(f"{v:.1f}" for v in vals)}" dur="{n * T_sim:.2f}s" begin="indefinite" fill="freeze"/></circle>')
        return fig("d5-0", "0 0 420 240", "Sóng chạy trên dây và đồ thị li độ theo thời gian của điểm M được vẽ dần",
                   b, "Mô phỏng: sóng chạy trên dây, chấm cam là điểm M; đường dưới là đồ thị u – t của M được vẽ dần (chạy chậm 5 lần). Sóng tính theo công thức; bấm Chạy mô phỏng.")
    b = defs(p) + graphs(p, ann=True)
    return fig("d5-2", "0 0 420 330", "Hai đồ thị đã đánh dấu: bước sóng đo trên đồ thị u – x, chu kì đo trên đồ thị u – t, điểm M và điểm N", b,
               "Dữ kiện: trục hoành x cho bước sóng, trục hoành t cho chu kì. " + NOTE)

BUILD = [d1, d2, d3, d4, d5]

# ───────────── Đề ─────────────
def ol(*items):
    return '<ol type="a">' + "".join(f"<li>{x}</li>" for x in items) + "</ol>"

DANG = [
 dict(label="Dạng 1 · Dễ · Đếm ngọn sóng: tìm chu kì, tần số và tốc độ truyền sóng", topic=TOPIC_164,
      problem_html="<p>Một chiếc phao nổi trên mặt hồ. Sóng lan truyền trên mặt hồ; người quan sát đếm được phao nhô lên $9$ lần (tính từ lần nhô lên đầu tiên đến lần thứ chín) trong khoảng thời gian $20\\ \\text{s}$, và đo được khoảng cách giữa hai ngọn sóng liên tiếp là $4{,}5\\ \\text{m}$.</p>"
                   + ol("Tính chu kì và tần số của sóng.", "Tính tốc độ truyền sóng.")),
 dict(label="Dạng 2 · Trung bình · Hai điểm trên phương truyền: độ lệch pha và khoảng cách", topic=TOPIC_164,
      problem_html="<p>Sóng ngang truyền trên một sợi dây dài, theo chiều từ M đến N, với tốc độ $v=1{,}2\\ \\text{m/s}$ và tần số $f=20\\ \\text{Hz}$. Hai điểm M, N trên dây cách nhau $10{,}5\\ \\text{cm}$.</p>"
                   + ol("Tính bước sóng.", "Tính độ lệch pha giữa dao động của M và N. M và N dao động cùng pha, ngược pha hay vuông pha?",
                        "Điểm P trên dây, gần M nhất và dao động ngược pha với M, cách M bao nhiêu?")),
 dict(label="Dạng 3 · Trung bình · Đọc phương trình sóng: biên độ, tần số, bước sóng, tốc độ", topic=TOPIC_165,
      problem_html="<p>Một sóng cơ lan truyền trên một sợi dây dài theo phương Ox với phương trình $u=5\\cos(8\\pi t-0{,}2\\pi x)$ (cm), trong đó $x$ đo bằng cm, $t$ đo bằng giây.</p>"
                   + ol("Tìm biên độ, chu kì và tần số của sóng.", "Tìm bước sóng và tốc độ truyền sóng (đơn vị m/s).",
                        "Tìm tốc độ dao động cực đại của một phần tử dây và cho biết nó lớn hơn hay nhỏ hơn tốc độ truyền sóng.")),
 dict(label="Dạng 4 · Khó · Viết phương trình dao động tại M, li độ và chiều chuyển động", topic=TOPIC_165,
      problem_html="<p>Nguồn O trên một sợi dây rất dài dao động theo phương trình $u_O=4\\cos\\left(20\\pi t-\\dfrac{\\pi}{2}\\right)$ (cm), tạo ra sóng truyền theo chiều dương trục Ox với tốc độ $1{,}5\\ \\text{m/s}$. Biên độ sóng không đổi, nguồn O bắt đầu dao động tại $t=0$. Điểm M trên dây cách O một đoạn $20\\ \\text{cm}$.</p>"
                   + ol("Tính chu kì và bước sóng.", "Viết phương trình dao động của M.", "Tại thời điểm $t=0{,}15\\ \\text{s}$, M có li độ bao nhiêu và đang chuyển động theo chiều nào?")),
 dict(label="Dạng 5 · Khó · Đọc hai đồ thị u–x và u–t, viết phương trình dao động", topic=TOPIC_165,
      problem_html="<p>Một sóng cơ hình sin truyền trên một sợi dây dài theo chiều dương trục Ox. Hình (a) là đồ thị li độ theo toạ độ $x$ của các điểm trên dây tại thời điểm $t=0$. Hình (b) là đồ thị li độ theo thời gian $t$ của điểm M trên dây có toạ độ $x_M=6\\ \\text{cm}$.</p>"
                   + static_graph_figure()
                   + ol("Đọc đồ thị, tìm biên độ, bước sóng và chu kì của sóng.", "Tính tốc độ truyền sóng.", "Viết phương trình dao động của M.",
                        "Điểm N trên dây cách M $9\\ \\text{cm}$ theo chiều truyền sóng. Viết phương trình dao động của N.")),
]

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [("\"nhô lên $9$ lần … trong $20$ s\"", "$n=9$ lần nhô lên; $\\Delta t=20$ s", "⚠ Đếm từ lần đầu đến lần cuối: $n$ lần nhô lên chỉ có $(n-1)$ chu kì"),
  ("\"khoảng cách giữa hai ngọn sóng liên tiếp là $4{,}5$ m\"", "$\\lambda=4{,}5$ m", "Bước sóng = khoảng cách hai ngọn sóng liên tiếp"),
  ("\"chu kì và tần số\"", "Cần $T$, $f$", "$T=\\dfrac{\\Delta t}{n-1}$; $f=\\dfrac{1}{T}$"),
  ("\"tốc độ truyền sóng\"", "Cần $v$", "$v=\\dfrac{\\lambda}{T}=\\lambda f$ (sóng đi một bước sóng trong một chu kì)")],
 [("\"tốc độ $v=1{,}2$ m/s … tần số $f=20$ Hz\"", "$v=1{,}2$ m/s; $f=20$ Hz", "$\\lambda=\\dfrac{v}{f}$ (đổi về cùng hệ đơn vị)"),
  ("\"hai điểm M, N cách nhau $10{,}5$ cm\"", "$d=10{,}5$ cm", "$\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$; lập tỉ số $\\dfrac{d}{\\lambda}$"),
  ("\"hai điểm M, N trên dây\"", "Cùng một phương truyền", "⚠ $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$ chỉ dùng cho hai điểm cùng nằm trên một phương truyền sóng"),
  ("\"cùng pha, ngược pha hay vuông pha?\"", "Cần gọi tên $\\Delta\\varphi$", "Cùng pha $k2\\pi$ · ngược pha $(2k+1)\\pi$ · vuông pha $(2k+1)\\dfrac{\\pi}{2}$"),
  ("\"gần M nhất và dao động ngược pha\"", "Ngược pha, gần nhất", "$\\Delta\\varphi=\\pi$")],
 [("\"$u=5\\cos(8\\pi t-0{,}2\\pi x)$\"", "$A=5$ cm; hệ số của $t$: $8\\pi$; của $x$: $0{,}2\\pi$", "Đối chiếu $u=A\\cos\\left(\\omega t-\\dfrac{2\\pi x}{\\lambda}\\right)$"),
  ("\"$x$ đo bằng cm, $t$ đo bằng giây\"", "$x$: cm; $t$: s", "⚠ Đơn vị: $\\lambda$ ra cm (cùng đơn vị với $x$); đổi sang m khi đề hỏi m/s"),
  ("\"chu kì và tần số\"", "Cần $T$, $f$", "$\\omega=2\\pi f$; $T=\\dfrac{1}{f}$"),
  ("\"bước sóng và tốc độ truyền sóng\"", "Cần $\\lambda$, $v$", "Hệ số của $x$ bằng $\\dfrac{2\\pi}{\\lambda}$; $v=\\lambda f$"),
  ("\"tốc độ dao động cực đại\"", "Cần $v_{max}$", "$v_{max}=\\omega A$ (do nguồn quyết định, khác $v$ do môi trường)")],
 [("\"nguồn O … $u_O=4\\cos\\left(20\\pi t-\\dfrac{\\pi}{2}\\right)$\"", "$A=4$ cm; $\\omega=20\\pi$; $\\varphi_0=-\\pi/2$", "$\\omega=2\\pi f$; $T=\\dfrac{1}{f}$"),
  ("\"chiều dương trục Ox … tốc độ $1{,}5$ m/s\"", "$v=1{,}5$ m/s; chiều $+Ox$", "Sóng tới sau thì trừ pha; $\\lambda=\\dfrac{v}{f}$"),
  ("\"M cách O $20$ cm\"", "$d=20$ cm", "$u_M=A\\cos\\left(\\omega t+\\varphi_0-\\dfrac{2\\pi d}{\\lambda}\\right)$"),
  ("\"tại thời điểm $t=0{,}15$ s\"", "$t=0{,}15$ s", "⚠ $u_M$ chỉ đúng khi $t\\ge\\dfrac{d}{v}$ (sóng đã tới M): kiểm tra trước khi thay"),
  ("\"li độ … và chiều chuyển động\"", "Cần $u_M$ và dấu của $v_M$", "$v_M=u_M'=-\\omega A\\sin(\\text{pha})$; $v_M\\gt0$ là đi lên")],
 [("\"hình (a): li độ theo toạ độ $x$ … tại $t=0$\"", "Trục hoành là $x$ (cm)", "⚠ Đọc nhãn trục hoành trước: đồ thị $u-x$ có hai đỉnh liên tiếp cách nhau $\\lambda$"),
  ("\"hình (b): li độ theo thời gian $t$ của điểm M\"", "Trục hoành là $t$ (s)", "Đồ thị $u-t$: hai đỉnh liên tiếp cách nhau $T$; $\\omega=\\dfrac{2\\pi}{T}$"),
  ("\"tính tốc độ truyền sóng\"", "Cần $v$", "$v=\\dfrac{\\lambda}{T}$ ($\\lambda$ từ hình (a), $T$ từ hình (b))"),
  ("\"viết phương trình dao động của M\"", "Cần $A$, $\\omega$, $\\varphi_0$", "$u_M=A\\cos(\\omega t+\\varphi_0)$; hình (b) cho biết $u_M$ lúc $t=0$"),
  ("\"N cách M $9$ cm theo chiều truyền sóng\"", "$d=9$ cm", "N nhận sóng sau M nên trễ pha: $u_N=A\\cos\\left(\\omega t+\\varphi_0-\\dfrac{2\\pi d}{\\lambda}\\right)$")],
]

# ───────────── Lời giải ─────────────
SOLS = [
 sol(["<strong>Khái niệm:</strong> chu kì $T$ là thời gian một dao động toàn phần; bước sóng $\\lambda$ là khoảng cách hai ngọn sóng liên tiếp.",
      "<strong>Công thức:</strong> $f=\\dfrac{1}{T}$ · $v=\\dfrac{\\lambda}{T}=\\lambda f$.",
      "⚠ <strong>Điều kiện đếm:</strong> $n$ lần nhô lên (từ lần đầu đến lần cuối) chỉ có $(n-1)$ chu kì."], [
  ("Chu kì", [P("Phao nhô lên $9$ lần nên có $9-1=8$ chu kì trong $20$ s:"), M(r"T=\dfrac{\Delta t}{n-1}=\dfrac{20}{8}"), A(r"T=2{,}5\ \text{s}")]),
  ("Tần số", [M(r"f=\dfrac{1}{T}=\dfrac{1}{2{,}5}"), A(r"f=0{,}4\ \text{Hz}")]),
  ("Tốc độ truyền sóng", [P("Hai ngọn sóng liên tiếp cách nhau một bước sóng: $\\lambda=4{,}5$ m."), M(r"v=\dfrac{\lambda}{T}=\dfrac{4{,}5}{2{,}5}"), A(r"v=1{,}8\ \text{m/s}")]),
  ("Kiểm tra", [P("Cách khác: $v=\\lambda f=4{,}5\\cdot0{,}4=1{,}8$ m/s ✓"), P("Trong $20$ s sóng đi được $1{,}8\\cdot20=36$ m; phao chỉ nhô lên hạ xuống tại chỗ.")])],
  ["a) $T=2{,}5\\ \\text{s}$ · $f=0{,}4\\ \\text{Hz}$", "b) $v=1{,}8\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>số lần nhô lên</strong> trong một khoảng thời gian → có $(n-1)$ chu kì, rồi $v=\\dfrac{\\lambda}{T}$."),
 sol(["<strong>Khái niệm:</strong> hai điểm trên cùng phương truyền cách nhau $d$ thì dao động lệch pha nhau.",
      "<strong>Công thức:</strong> $\\lambda=\\dfrac{v}{f}$ · $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$.",
      "Cùng pha: $k2\\pi$ · ngược pha: $(2k+1)\\pi$ · vuông pha: $(2k+1)\\dfrac{\\pi}{2}$.",
      "⚠ <strong>Điều kiện:</strong> hai điểm cùng nằm trên một phương truyền sóng."], [
  ("Bước sóng", [P("Đổi $v=1{,}2$ m/s $=120$ cm/s:"), M(r"\lambda=\dfrac{v}{f}=\dfrac{120}{20}"), A(r"\lambda=6\ \text{cm}")]),
  ("Tỉ số $\\dfrac{d}{\\lambda}$", [M(r"\dfrac{d}{\lambda}=\dfrac{10{,}5}{6}"), A(r"\dfrac{d}{\lambda}=1{,}75")]),
  ("Độ lệch pha", [M(r"\Delta\varphi=\dfrac{2\pi d}{\lambda}=2\pi\cdot1{,}75"), A(r"\Delta\varphi=3{,}5\pi\ \text{rad}")]),
  ("Gọi tên độ lệch pha", [M(r"\Delta\varphi=3{,}5\pi=7\cdot\dfrac{\pi}{2}=(2k+1)\dfrac{\pi}{2}\ \ (k=3)"), A("T:M và N <strong>vuông pha</strong>.")]),
  ("Điểm ngược pha gần nhất", [P("Ngược pha gần nhất: $\\Delta\\varphi=\\pi$."), M(r"\pi=\dfrac{2\pi d_{min}}{\lambda}\Rightarrow d_{min}=\dfrac{\lambda}{2}=\dfrac{6}{2}"), A(r"d_{min}=3\ \text{cm}")])],
  ["a) $\\lambda=6\\ \\text{cm}$", "b) $\\Delta\\varphi=3{,}5\\pi\\ \\text{rad}$: M và N vuông pha", "c) $d_{min}=3\\ \\text{cm}$"],
  "Nhận dạng: đề cho <strong>khoảng cách hai điểm</strong> và hỏi <strong>cùng, ngược hay vuông pha</strong> → lập $\\dfrac{d}{\\lambda}$ rồi tính $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$."),
 sol(["<strong>Khái niệm:</strong> phương trình sóng cho li độ của điểm có toạ độ $x$ tại thời điểm $t$.",
      "<strong>Dạng chuẩn:</strong> $u=A\\cos\\left(\\omega t-\\dfrac{2\\pi x}{\\lambda}\\right)$ (sóng truyền theo $+Ox$).",
      "<strong>Công thức:</strong> $\\omega=2\\pi f$ · $T=\\dfrac{1}{f}$ · $v=\\lambda f$ · $v_{max}=\\omega A$.",
      "⚠ <strong>Điều kiện:</strong> $\\lambda$ cùng đơn vị với $x$; đổi sang m khi đề hỏi m/s."], [
  ("Biên độ, chu kì, tần số", [P("Đối chiếu dạng chuẩn: $A=5$ cm; $\\omega=8\\pi$ rad/s."), M(r"f=\dfrac{\omega}{2\pi}=\dfrac{8\pi}{2\pi}"), A(r"f=4\ \text{Hz}"), M(r"T=\dfrac{1}{f}=0{,}25\ \text{s}")]),
  ("Bước sóng", [P("Hệ số của $x$ bằng $\\dfrac{2\\pi}{\\lambda}$:"), M(r"\dfrac{2\pi}{\lambda}=0{,}2\pi"), M(r"\lambda=\dfrac{2\pi}{0{,}2\pi}"), A(r"\lambda=10\ \text{cm}")]),
  ("Tốc độ truyền sóng", [M(r"v=\lambda f=10\cdot4=40\ \text{cm/s}"), P("Đổi sang m/s:"), A(r"v=0{,}4\ \text{m/s}")]),
  ("Tốc độ dao động cực đại", [M(r"v_{max}=\omega A=8\pi\cdot5"), A(r"v_{max}=40\pi\approx125{,}7\ \text{cm/s}")]),
  ("So sánh hai tốc độ", [M(r"\dfrac{v_{max}}{v}=\dfrac{40\pi}{40}=\pi\approx3{,}14"), A("T:$v_{max}$ <strong>lớn hơn</strong> $v$ khoảng $3{,}14$ lần."),
                         P("Không mâu thuẫn: $v$ do môi trường quyết định, $v_{max}$ do nguồn quyết định.")])],
  ["a) $A=5\\ \\text{cm}$ · $T=0{,}25\\ \\text{s}$ · $f=4\\ \\text{Hz}$", "b) $\\lambda=10\\ \\text{cm}$ · $v=0{,}4\\ \\text{m/s}$", "c) $v_{max}\\approx125{,}7\\ \\text{cm/s}$, lớn hơn $v$"],
  "Nhận dạng: đề cho <strong>phương trình sóng</strong> có cả $t$ và $x$ → đối chiếu hệ số với dạng chuẩn, nhớ đổi đơn vị."),
 sol(["<strong>Khái niệm:</strong> M dao động giống O nhưng trễ pha $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$ (sóng đi mất $\\dfrac{d}{v}$).",
      "<strong>Định luật:</strong> sóng tới sau thì trừ pha: $u_M=A\\cos\\left(\\omega t+\\varphi_0-\\dfrac{2\\pi d}{\\lambda}\\right)$.",
      "<strong>Công thức:</strong> $\\lambda=\\dfrac{v}{f}$ · $v_M=u_M'=-\\omega A\\sin(\\text{pha})$.",
      "⚠ <strong>Điều kiện:</strong> biên độ không đổi; $u_M$ chỉ đúng khi $t\\ge\\dfrac{d}{v}$."], [
  ("Chu kì và bước sóng", [M(r"\omega=20\pi\Rightarrow f=10\ \text{Hz},\ \ T=0{,}1\ \text{s}"), P("Đổi $v=1{,}5$ m/s $=150$ cm/s:"), M(r"\lambda=\dfrac{v}{f}=\dfrac{150}{10}"), A(r"\lambda=15\ \text{cm}")]),
  ("Phương trình dao động của M", [M(r"\Delta\varphi=\dfrac{2\pi d}{\lambda}=\dfrac{2\pi\cdot20}{15}=\dfrac{8\pi}{3}"), P("Pha của M bằng pha của O trừ $\\Delta\\varphi$:"),
                                  M(r"u_M=4\cos\left(20\pi t-\dfrac{\pi}{2}-\dfrac{8\pi}{3}\right)"), A(r"u_M=4\cos\left(20\pi t-\dfrac{19\pi}{6}\right)\ \text{cm}")]),
  ("Sóng đã tới M chưa", [M(r"t_0=\dfrac{d}{v}=\dfrac{20}{150}\approx0{,}133\ \text{s}"), P("$t=0{,}15\\ \\text{s}\\gt t_0$: M đã dao động, dùng được $u_M$.")]),
  ("Li độ tại $t=0{,}15$ s", [M(r"u_M=4\cos\left(20\pi\cdot0{,}15-\dfrac{19\pi}{6}\right)=4\cos\left(3\pi-\dfrac{19\pi}{6}\right)"), M(r"=4\cos\left(-\dfrac{\pi}{6}\right)"), A(r"u_M=2\sqrt3\approx3{,}46\ \text{cm}")]),
  ("Chiều chuyển động", [M(r"v_M=u_M'=-80\pi\sin\left(-\dfrac{\pi}{6}\right)"), M(r"v_M=+40\pi\approx125{,}7\ \text{cm/s}\gt0"), A("T:M đang đi <strong>lên</strong> (chiều dương).")]),
  ("Kiểm tra", [P("Từ lúc sóng tới M: $t-t_0\\approx0{,}0167\\ \\text{s}=\\dfrac{T}{6}$."), P("O xuất phát từ vị trí cân bằng đi lên nên M cũng vậy: $u_M=4\\sin\\dfrac{\\pi}{3}\\approx3{,}46$ cm ✓.")])],
  ["a) $T=0{,}1\\ \\text{s}$ · $\\lambda=15\\ \\text{cm}$", "b) $u_M=4\\cos\\left(20\\pi t-\\dfrac{19\\pi}{6}\\right)\\ \\text{cm}$", "c) $u_M\\approx3{,}46\\ \\text{cm}$, đang đi lên"],
  "Nhận dạng: đề cho <strong>phương trình nguồn</strong> và hỏi <strong>M cách nguồn $d$</strong> → trừ độ trễ pha $\\dfrac{2\\pi d}{\\lambda}$, kiểm $t\\ge\\dfrac{d}{v}$."),
 sol(["<strong>Khái niệm:</strong> đồ thị $u-x$ (một lúc): hai đỉnh liên tiếp cách nhau $\\lambda$. Đồ thị $u-t$ (một điểm): hai đỉnh liên tiếp cách nhau $T$.",
      "<strong>Công thức:</strong> $v=\\dfrac{\\lambda}{T}$ · $\\omega=\\dfrac{2\\pi}{T}$ · $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$.",
      "Sóng tới sau thì trừ pha: $u_N=A\\cos\\left(\\omega t+\\varphi_0-\\dfrac{2\\pi d}{\\lambda}\\right)$.",
      "⚠ <strong>Điều kiện:</strong> đọc nhãn trục hoành trước: $x$ cho $\\lambda$, $t$ cho $T$."], [
  ("Bước sóng từ đồ thị (a)", [P("Trục hoành là $x$ (cm). Hai đỉnh liên tiếp ở $x=6$ cm và $x=30$ cm:"), M(r"\lambda=30-6"), A(r"\lambda=24\ \text{cm}"), P("Đỉnh cao $3$ cm nên biên độ $A=3$ cm.")]),
  ("Chu kì từ đồ thị (b)", [P("Trục hoành là $t$ (s). Hai đỉnh liên tiếp ở $t=0$ và $t=0{,}4$ s:"), A(r"T=0{,}4\ \text{s}")]),
  ("Tốc độ truyền sóng", [M(r"v=\dfrac{\lambda}{T}=\dfrac{24}{0{,}4}"), A(r"v=60\ \text{cm/s}")]),
  ("Phương trình của M", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{0{,}4}=5\pi\ \text{rad/s}"), P("Lúc $t=0$, M ở biên dương ($u_M=3$ cm) nên $\\varphi_0=0$:"), A(r"u_M=3\cos(5\pi t)\ \text{cm}")]),
  ("Phương trình của N", [M(r"\Delta\varphi=\dfrac{2\pi d}{\lambda}=\dfrac{2\pi\cdot9}{24}=\dfrac{3\pi}{4}"), P("N nhận sóng sau M nên trễ pha:"), A(r"u_N=3\cos\left(5\pi t-\dfrac{3\pi}{4}\right)\ \text{cm}")]),
  ("Kiểm tra", [P("$\\lambda=vT=60\\cdot0{,}4=24$ cm ✓ (khớp hình (a))."),
                P("Lúc $t=0$: $u_N=3\\cos\\dfrac{3\\pi}{4}\\approx-2{,}12$ cm; hình (a) ở $x=15$ cm: $3\\sin\\dfrac{15\\pi}{12}\\approx-2{,}12$ cm ✓.")])],
  ["a) $A=3\\ \\text{cm}$ · $\\lambda=24\\ \\text{cm}$ · $T=0{,}4\\ \\text{s}$", "b) $v=60\\ \\text{cm/s}$", "c) $u_M=3\\cos(5\\pi t)\\ \\text{cm}$", "d) $u_N=3\\cos\\left(5\\pi t-\\dfrac{3\\pi}{4}\\right)\\ \\text{cm}$"],
  "Nhận dạng: đề cho <strong>hai đồ thị</strong> → đọc nhãn trục hoành: $x$ cho $\\lambda$, $t$ cho $T$, rồi $v=\\dfrac{\\lambda}{T}$."),
]

# ───────────── Tự giải từng bước (số bước khớp 1-1 với SOLS) ─────────────
STEPS = [
 dict(nhan_dang="Thấy <b>phao nhô lên n lần trong t giây</b> → có $(n-1)$ chu kì; rồi $v=\\dfrac{\\lambda}{T}$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Chu kì", "Chu kì $T$ của sóng bằng bao nhiêu?", 2.5, "s", 0.05,
       loi="Chia $20$ s cho số lần nhô lên: $9$ lần từ lần đầu đến lần cuối chỉ có $8$ khoảng, tức $8$ chu kì."),
  buoc("Tần số", "Tần số $f$ của sóng bằng bao nhiêu?", 0.4, "Hz", 0.01,
       loi="Lấy $f=T$: hai đại lượng này nghịch đảo nhau, $f=\\dfrac{1}{T}$.",
       ke=[("$f=\\dfrac{1}{T}$", True),
           ("$f=T$", "Tần số (Hz) và chu kì (s) là hai đại lượng nghịch đảo, không bằng nhau."),
           ("$f=\\dfrac{n}{\\Delta t}$ với $n=9$", "Số lần nhô lên là $9$ nhưng chỉ có $8$ chu kì: phải dùng $\\dfrac{n-1}{\\Delta t}$.")]),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu?", 1.8, "m/s", 0.02,
       loi="Nhân $\\lambda$ với $T$ thay vì chia, hoặc lấy $\\lambda$ chia cho cả $20$ s.",
       ke=[("$v=\\dfrac{\\lambda}{T}$ (sóng đi một bước sóng trong một chu kì)", True),
           ("$v=\\lambda\\cdot T$", "Nhân cho đơn vị m·s, không phải m/s; sóng đi $\\lambda$ trong thời gian $T$ nên phải chia."),
           ("$v=\\dfrac{\\lambda}{20}$ (chia cho cả khoảng thời gian đếm)", "$20$ s là thời gian của $8$ chu kì, không phải của một bước sóng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>khoảng cách hai điểm</b> và hỏi <b>cùng, ngược hay vuông pha</b> → lập $\\dfrac{d}{\\lambda}$, tính $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu?", 6, "cm", 0.1,
       loi="Chia $1{,}2$ cho $20$ mà không đổi đơn vị: $v$ tính bằng m/s nên $\\lambda$ ra mét, phải đổi sang cm."),
  buoc("Tỉ số $\\dfrac{d}{\\lambda}$", "Tỉ số $\\dfrac{d}{\\lambda}$ bằng bao nhiêu?", 1.75, None, 0.01,
       loi="Lấy $\\dfrac{\\lambda}{d}$ (ngược) hoặc chia $d$ cho bước sóng đã tính sai đơn vị.",
       ke=[("Lập $\\dfrac{d}{\\lambda}$ để biết $d$ chứa bao nhiêu bước sóng", True),
           ("Lấy $d\\cdot\\lambda$", "Tích hai độ dài không cho biết số bước sóng; phải lập tỉ số."),
           ("Lấy $\\dfrac{d}{v}$", "$\\dfrac{d}{v}$ là thời gian sóng đi từ M tới N, không phải số bước sóng.")]),
  buoc("Độ lệch pha", "Độ lệch pha $\\Delta\\varphi$ bằng bao nhiêu lần $\\pi$ (rad)?", 3.5, "π rad", 0.02,
       loi="Dùng $\\Delta\\varphi=\\pi\\dfrac{d}{\\lambda}$ (thiếu hệ số $2$) hoặc $2\\pi\\dfrac{\\lambda}{d}$ (ngược).",
       ke=[("$\\Delta\\varphi=2\\pi\\dfrac{d}{\\lambda}$ (mỗi bước sóng ứng với $2\\pi$)", True),
           ("$\\Delta\\varphi=\\pi\\dfrac{d}{\\lambda}$", "Một bước sóng ứng với $2\\pi$; $\\pi$ chỉ ứng với nửa bước sóng."),
           ("$\\Delta\\varphi=2\\pi\\dfrac{\\lambda}{d}$", "Ngược rồi: đi càng xa thì trễ pha càng nhiều, nên $d$ nằm ở tử số.")]),
  buoc("Gọi tên độ lệch pha", "M và N dao động thế nào với nhau?",
       lua_chon=[("Vuông pha", True),
                 ("Ngược pha", "Ngược pha cần $\\Delta\\varphi$ là số lẻ lần $\\pi$; ở đây $\\Delta\\varphi$ là số lẻ lần $\\dfrac{\\pi}{2}$."),
                 ("Cùng pha", "Cùng pha cần $\\Delta\\varphi$ là số chẵn lần $\\pi$ (nguyên lần $2\\pi$).")],
       loi="Thấy phần lẻ của $\\dfrac{d}{\\lambda}$ khác $0{,}25$ rồi kết luận không vuông pha; cứ cộng thêm vòng $2\\pi$ trọn vẹn hoặc nửa vòng thì vẫn vuông pha.",
       ke=[("Viết $\\Delta\\varphi$ dưới dạng số lẻ lần $\\dfrac{\\pi}{2}$ hay số lẻ lần $\\pi$", True),
           ("Chỉ xét phần nguyên của $\\dfrac{d}{\\lambda}$", "Phần nguyên chỉ là các vòng $2\\pi$ trọn vẹn; phần lẻ mới quyết định cùng, ngược hay vuông pha."),
           ("Xét dấu của $\\Delta\\varphi$", "Dấu chỉ cho biết ai trễ pha hơn, không cho biết cùng, ngược hay vuông pha.")]),
  buoc("Điểm ngược pha gần nhất", "Điểm ngược pha với M gần nhất cách M bao nhiêu?", 3, "cm", 0.1,
       loi="Lấy $d=\\lambda$ (đó là điểm cùng pha gần nhất) hoặc $d=\\dfrac{\\lambda}{4}$ (vuông pha).",
       ke=[("Ngược pha gần nhất ứng với $\\Delta\\varphi=\\pi$, tức $d=\\dfrac{\\lambda}{2}$", True),
           ("$d=\\lambda$", "Đó là khoảng cách cùng pha gần nhất."),
           ("$d=\\dfrac{\\lambda}{4}$", "Đó là khoảng cách vuông pha gần nhất ($\\Delta\\varphi=\\dfrac{\\pi}{2}$).")])]),
 dict(nhan_dang="Thấy <b>phương trình sóng có cả $t$ và $x$</b> → đối chiếu dạng chuẩn: hệ số của $t$ là $\\omega$, của $x$ là $\\dfrac{2\\pi}{\\lambda}$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Biên độ, chu kì, tần số", "Tần số $f$ của sóng bằng bao nhiêu?", 4, "Hz", 0.05,
       loi="Lấy $f=8\\pi$ hoặc $f=8$: hệ số của $t$ là $\\omega=2\\pi f$, không phải $f$."),
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu?", 10, "cm", 0.2,
       loi="Lấy $\\lambda=\\dfrac{1}{0{,}2}$ (bỏ sót $\\pi$ và hệ số $2$) hoặc coi hệ số của $x$ chính là $\\lambda$.",
       ke=[("Hệ số của $x$ bằng $\\dfrac{2\\pi}{\\lambda}$", True),
           ("Hệ số của $x$ chính là $\\lambda$", "Số hạng của đề là $\\dfrac{2\\pi x}{\\lambda}$, nên hệ số của $x$ là $\\dfrac{2\\pi}{\\lambda}$."),
           ("Hệ số của $x$ bằng $\\dfrac{1}{\\lambda}$", "Thiếu $2\\pi$: pha trễ là $\\dfrac{2\\pi x}{\\lambda}$.")]),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu?", 0.4, "m/s", 0.01,
       loi="Tính ra số đúng theo cm/s nhưng quên đổi sang m/s theo yêu cầu của đề.",
       ke=[("$v=\\lambda f$, rồi đổi đơn vị sang m/s", True),
           ("$v=\\dfrac{\\lambda}{f}$", "$\\dfrac{\\lambda}{f}$ có đơn vị cm·s; $v=\\dfrac{\\lambda}{T}=\\lambda f$."),
           ("$v=\\omega A$", "$\\omega A$ là tốc độ dao động cực đại của phần tử, không phải tốc độ truyền sóng.")]),
  buoc("Tốc độ dao động cực đại", "Tốc độ dao động cực đại $v_{max}$ của phần tử dây bằng bao nhiêu?", 125.7, "cm/s", 1,
       loi="Quên nhân biên độ (lấy $\\omega$) hoặc nhầm với tốc độ truyền sóng.",
       ke=[("$v_{max}=\\omega A$ (lấy đạo hàm của $u$ theo $t$)", True),
           ("$v_{max}=\\lambda f$", "Đó là tốc độ truyền sóng, không phải tốc độ dao động của phần tử."),
           ("$v_{max}=\\omega$", "Thiếu biên độ: li độ cực đại là $A$ nên $v_{max}=\\omega A$.")]),
  buoc("So sánh hai tốc độ", "So sánh $v_{max}$ với tốc độ truyền sóng $v$?",
       lua_chon=[("$v_{max}$ lớn hơn $v$; hai đại lượng khác nhau nên không mâu thuẫn", True),
                 ("Vô lí, phần tử không thể chạy nhanh hơn sóng", "Sóng truyền pha, còn phần tử dao động tại chỗ; hai tốc độ do hai yếu tố khác nhau quyết định."),
                 ("$v_{max}$ luôn bằng $v$", "Không có quy luật bằng nhau: $v$ do môi trường, $v_{max}=\\omega A$ do nguồn.")],
       loi="Cho rằng hai tốc độ phải bằng nhau hoặc cái này luôn nhỏ hơn cái kia vì cùng ký hiệu $v$.",
       ke=[("Tính tỉ số $\\dfrac{v_{max}}{v}$ với cùng đơn vị rồi kết luận", True),
           ("Kết luận ngay vì sóng truyền nhanh hơn phần tử", "Không có quy luật định sẵn; phải so số liệu của từng đề."),
           ("So $v_{max}$ với $\\lambda$", "Hai đại lượng khác thứ nguyên (cm/s và cm), không so sánh được.")])]),
 dict(nhan_dang="Thấy <b>phương trình nguồn</b> và <b>M cách nguồn đoạn $d$</b> → trừ độ trễ pha $\\dfrac{2\\pi d}{\\lambda}$; kiểm $t\\ge\\dfrac{d}{v}$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chu kì và bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu?", 15, "cm", 0.2,
       loi="Quên đổi $v$ sang cm/s trước khi chia cho $f$, hoặc lấy $f=20$ thay vì $f=10$ Hz (hệ số của $t$ là $\\omega=2\\pi f$)."),
  buoc("Phương trình dao động của M", "Phương trình dao động của M là?",
       lua_chon=[("$u_M=4\\cos\\left(20\\pi t-\\dfrac{19\\pi}{6}\\right)$ cm", True),
                 ("$u_M=4\\cos\\left(20\\pi t-\\dfrac{8\\pi}{3}\\right)$ cm", "Quên pha ban đầu $-\\dfrac{\\pi}{2}$ của O: pha của M là pha của O trừ thêm độ trễ $\\dfrac{8\\pi}{3}$."),
                 ("$u_M=4\\cos\\left(20\\pi t-\\dfrac{\\pi}{2}+\\dfrac{8\\pi}{3}\\right)$ cm", "Sai dấu: sóng truyền theo $+Ox$, M nhận sóng sau O nên pha phải trừ (trễ), không cộng.")],
       loi="Cộng độ trễ pha thay vì trừ, hoặc bỏ quên pha ban đầu của nguồn.",
       ke=[("Tính $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$ rồi trừ vào pha của O", True),
           ("Cộng $\\Delta\\varphi$ vào pha của O", "Sóng truyền theo $+Ox$: M nhận sóng sau nên trễ pha, phải trừ."),
           ("Dùng $\\Delta\\varphi=\\dfrac{2\\pi\\lambda}{d}$", "Ngược rồi: $d$ ở tử số, đi càng xa thì trễ pha càng nhiều.")]),
  buoc("Sóng đã tới M chưa", "Sóng truyền từ O tới M mất bao lâu?", 0.1333, "s", 0.003,
       loi="Đổi sai đơn vị ($d$ theo cm chia cho $v$ theo m/s), hoặc bỏ qua bước này vì tưởng $u_M$ đúng với mọi $t$.",
       ke=[("Tính $t_0=\\dfrac{d}{v}$ rồi so với $t$ đề cho", True),
           ("Thay $t$ vào $u_M$ ngay vì $u_M$ luôn đúng", "$u_M$ chỉ đúng khi $t\\ge\\dfrac{d}{v}$; trước đó sóng chưa tới nên M còn đứng yên."),
           ("So $t$ với chu kì $T$", "Chu kì không cho biết sóng đã tới M chưa; cần thời gian truyền $\\dfrac{d}{v}$.")]),
  buoc("Li độ", "Li độ $u_M$ của M tại $t=0{,}15$ s bằng bao nhiêu?", 3.46, "cm", 0.05,
       loi="Bấm máy ở chế độ độ (DEG) thay vì radian, hoặc thay $t$ vào $u_O$ thay vì $u_M$.",
       ke=[("Thay $t$ vào $u_M$, tính pha bằng radian", True),
           ("Thay $t$ vào $u_O$", "$u_O$ là li độ của nguồn; M dao động trễ pha hơn O."),
           ("Thay $t-\\dfrac{d}{v}$ vào $u_M$", "Độ trễ $\\dfrac{d}{v}$ đã nằm trong pha $-\\dfrac{2\\pi d}{\\lambda}$ của $u_M$; trừ thêm là trừ hai lần.")]),
  buoc("Chiều chuyển động", "M đang chuyển động theo chiều nào?",
       lua_chon=[("Đi lên (chiều dương)", True),
                 ("Đi xuống (chiều âm)", "Dấu của $v_M=-\\omega A\\sin(\\text{pha})$: ở đây $\\sin(\\text{pha})$ âm nên $v_M\\gt0$."),
                 ("Đang dừng ở biên", "Ở biên li độ bằng $\\pm A$; li độ vừa tính nhỏ hơn biên độ nên M chưa tới biên.")],
       loi="Thấy li độ dương rồi kết luận đi lên (hoặc đi xuống) mà không xét dấu của $v_M$.",
       ke=[("Xét dấu $v_M=u_M'=-\\omega A\\sin(\\text{pha})$", True),
           ("Xét dấu của $u_M$: dương thì đi lên", "Dấu li độ chỉ cho biết M ở phía nào của vị trí cân bằng, không cho biết chiều chuyển động."),
           ("Xét dấu của pha: pha âm thì đi xuống", "Pha âm hay dương không quyết định; phải xét $\\sin(\\text{pha})$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>đồ thị sóng</b> → đọc nhãn trục hoành: $x$ cho $\\lambda$, $t$ cho $T$; rồi $v=\\dfrac{\\lambda}{T}$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Bước sóng từ đồ thị (a)", "Bước sóng $\\lambda$ đọc từ đồ thị bằng bao nhiêu?", 24, "cm", 0.5,
       loi="Đọc khoảng từ đỉnh tới vị trí cân bằng kế tiếp (một phần tư) hoặc từ đỉnh tới đáy (một nửa) thay vì hai đỉnh liên tiếp."),
  buoc("Chu kì từ đồ thị (b)", "Chu kì $T$ đọc từ đồ thị bằng bao nhiêu?", 0.4, "s", 0.01,
       loi="Lẫn hai đồ thị: lấy khoảng giữa hai đỉnh ở hình (a) làm chu kì (đó là bước sóng) vì không đọc nhãn trục hoành.",
       ke=[("Hai đỉnh liên tiếp trên trục thời gian của hình (b) cách nhau $T$", True),
           ("Lấy khoảng giữa hai đỉnh ở hình (a) làm $T$", "Trục hoành hình (a) là $x$, nên khoảng đó là bước sóng chứ không phải chu kì."),
           ("Lấy thời gian từ đỉnh tới vị trí cân bằng kế tiếp làm $T$", "Đó chỉ là $\\dfrac{T}{4}$; chu kì là khoảng giữa hai đỉnh liên tiếp.")]),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu?", 60, "cm/s", 1,
       loi="Chia ngược ($\\dfrac{T}{\\lambda}$), hoặc dùng biên độ thay cho bước sóng.",
       ke=[("$v=\\dfrac{\\lambda}{T}$ với $\\lambda$ từ hình (a), $T$ từ hình (b)", True),
           ("$v=\\dfrac{A}{T}$", "Biên độ không phải quãng đường sóng truyền; sóng đi một $\\lambda$ trong một $T$."),
           ("$v=\\lambda\\cdot T$", "Nhân cho đơn vị cm·s; tốc độ phải là $\\lambda$ chia cho $T$.")]),
  buoc("Phương trình của M", "Phương trình dao động của M là?",
       lua_chon=[("$u_M=3\\cos(5\\pi t)$ cm", True),
                 ("$u_M=3\\cos(0{,}4t)$ cm", "Hệ số của $t$ là $\\omega=\\dfrac{2\\pi}{T}$, không phải $T$."),
                 ("$u_M=3\\cos\\left(5\\pi t+\\dfrac{\\pi}{2}\\right)$ cm", "Hình (b) có đỉnh ngay tại $t=0$ nên pha ban đầu bằng $0$; $\\dfrac{\\pi}{2}$ ứng với M đang ở vị trí cân bằng.")],
       loi="Lấy $\\omega$ bằng $T$ thay vì $\\dfrac{2\\pi}{T}$, hoặc đoán pha ban đầu mà không nhìn li độ lúc $t=0$ trên hình (b).",
       ke=[("Lấy $\\omega=\\dfrac{2\\pi}{T}$ và $\\varphi_0$ từ li độ lúc $t=0$ trên hình (b)", True),
           ("Lấy $\\omega$ và $\\varphi_0$ từ hình (a)", "Hình (a) có trục hoành là $x$: không cho biết tần số hay pha theo thời gian của M."),
           ("Lấy $\\omega=\\dfrac{2\\pi}{\\lambda}$", "$\\dfrac{2\\pi}{\\lambda}$ là hệ số của $x$; $\\omega$ gắn với chu kì $T$.")]),
  buoc("Phương trình của N", "Phương trình dao động của N là?",
       lua_chon=[("$u_N=3\\cos\\left(5\\pi t-\\dfrac{3\\pi}{4}\\right)$ cm", True),
                 ("$u_N=3\\cos\\left(5\\pi t+\\dfrac{3\\pi}{4}\\right)$ cm", "N ở phía sóng tới sau M nên trễ pha: phải trừ."),
                 ("$u_N=3\\cos\\left(5\\pi t-\\dfrac{3\\pi}{2}\\right)$ cm", "Dùng $\\lambda=12$ cm (một nửa) thay vì bước sóng đọc được ở hình (a): $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$.")],
       loi="Cộng thay vì trừ độ trễ pha, hoặc dùng sai bước sóng khi tính $\\dfrac{2\\pi d}{\\lambda}$.",
       ke=[("Tính $\\Delta\\varphi=\\dfrac{2\\pi d}{\\lambda}$ rồi trừ vào pha của M", True),
           ("Dùng $\\Delta\\varphi=\\dfrac{2\\pi d}{v}$", "Mẫu số phải là bước sóng $\\lambda$; $\\dfrac{d}{v}$ là thời gian trễ, không phải số bước sóng."),
           ("Dùng $\\Delta\\varphi=2\\pi\\dfrac{d}{T}$", "$d$ là độ dài (cm), $T$ là thời gian (s): không chia được cho nhau; phải chia $d$ cho $\\lambda$.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Tự luận: các ví dụ cũ chưa biên tập (giữ nguyên lời giải gốc) ─────────────
old = json.load(open(OLD))["questions"]
# 0 = bờ biển 20 ngọn sóng; 4 = thuyền KNTT; 6 = dao động kí (hình đã xem: 1 chu kì = 3 ô); 7 = CTST lệch pha; 8 = cường độ sóng (bài 28)
# 1 → Dạng 1 · 2 → Dạng 3 (v_max) · 3 → Dạng 2 · 5 → Dạng 3 (đọc phương trình) — đã biên tập thành dạng mới, không đưa vào tự luận
TU_LUAN = tu_luan_tu(old, [6, 0, 4, 7, 8], {6: "Dễ", 0: "Dễ", 4: "Trung bình", 7: "Khó", 8: "Nâng cao"})

if not os.path.exists(J) or "--moi" in sys.argv or json.load(open(J)).get("lesson_id") != 27:
    write(J, 27, "Bài 8. Mô tả sóng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
d = json.load(open(J))
for i, q in enumerate(d["dang_bai"]):          # luôn dựng lại nội dung từ DANG (đề đổi → ghi lại)
    q["label"], q["topic"], q["problem_html"] = DANG[i]["label"], DANG[i]["topic"], DANG[i]["problem_html"]
d["generated_at"] = "2026-10-09"
d["tu_luan"] = TU_LUAN
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
