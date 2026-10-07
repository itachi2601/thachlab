"""Dựng hình cho 6 dạng bài 57 và chèn vào scripts/data/bai-tap-mau/57.json (idempotent: xoá figure data-bt cũ rồi chèn lại).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-57.py   (thêm --preview để ghi bản xem thử HTML ở scratchpad)"""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from hinh import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "57.json")
VB = "0 0 420 240"
VB3 = "0 0 420 258"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."

def sub(x, y, base, s, c="currentColor", size=13, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{s}</tspan></text>')

def smil(attr, vals, dur):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" dur="{dur:.2f}s" repeatCount="indefinite"/>'

def live(p, pts, vx_px, vy_px, hold, sec_per_interval):
    """Quả cầu + hai mũi tên vận tốc chạy theo quỹ đạo TÍNH THẬT (mẫu cách đều thời gian, nội suy tuyến tính → đúng vật lí).
    vx_px, vy_px: độ dài mũi tên (px, dương = sang phải / xuống) tại từng mẫu. hold: số mẫu giữ nguyên ở cuối trước khi lặp."""
    n = len(pts); idx = list(range(n)) + [n - 1] * hold
    dur = sec_per_interval * (len(idx) - 1)
    X = [pts[i][0] for i in idx]; Y = [pts[i][1] for i in idx]
    VX = [vx_px[i] for i in idx]; VY = [vy_px[i] for i in idx]
    out = f'<circle r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cx", X, dur)}{smil("cy", Y, dur)}</circle>'
    out += f'<line stroke="{BLUE}" stroke-width="3" marker-end="url(#{p}-b)">{smil("x1", X, dur)}{smil("y1", Y, dur)}{smil("x2", [x + v for x, v in zip(X, VX)], dur)}{smil("y2", Y, dur)}</line>'
    out += f'<line stroke="{ORG}" stroke-width="3" marker-end="url(#{p}-o)">{smil("x1", X, dur)}{smil("y1", Y, dur)}{smil("x2", X, dur)}{smil("y2", [y + v for y, v in zip(Y, VY)], dur)}</line>'
    return out

def ball(pts, hold, sec_per_interval):
    """Mô phỏng hiện tượng: quả cầu chạy dọc quỹ đạo TÍNH THẬT (mẫu cách đều thời gian). hold = số mẫu dừng ở cuối trước khi lặp."""
    n = len(pts); idx = list(range(n)) + [n - 1] * hold; dur = sec_per_interval * (len(idx) - 1)
    return (f'<circle r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", [pts[i][0] for i in idx], dur)}{smil("cy", [pts[i][1] for i in idx], dur)}</circle>')

# ───────────── Dạng 1: máy bay thả gói, h=490, v0=60 ─────────────
def d1(k):
    O = (104, 58); g = ngang_geom(490, 60, O, 270, 140); p = f"d1{k}"
    pl = plane(O[0] + 23, O[1] - 3)  # tâm máy bay nằm ngay trên gói hàng
    if k == 0:   # máy bay giữ vận tốc ngang v₀ khi thả: luôn nằm ngay trên gói hàng (đúng vật lí), cùng nhịp với quả cầu
        dx = g["land"][0] - O[0]; idx = list(range(41)) + [40] * 8; dur = (10 / 40) * (len(idx) - 1)
        vals = ";".join(f"{dx * min(i, 40) / 40:.1f} 0" for i in idx)
        pl += arrow(p, "r", O[0], O[1], O[0] + 50, O[1], 3) + lbl(O[0] - 26, O[1] - 26, "v₀ = 60 m/s", RED, 12, "start", "700")
        pl = f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" repeatCount="indefinite"/>{pl}</g>'
    b = defs(p) + ground(g["gy"]) + pl + dot(*O, 4.5, "currentColor")
    b += lbl(16, 22, "máy bay", "currentColor", 13, "start", "400")
    b += poly(g["pts"], GRN, 2.4, "" if k else "6 4") + dot(*g["land"], 4.5, GRN)
    if k == 0:
        b += dim(p, "o", O[0] - 60, O[1], O[0] - 60, g["gy"], "h = 490 m", O[0] - 52, (O[1] + g["gy"]) / 2 + 4)
        b += dim(p, "b", O[0], g["gy"] + 20, g["land"][0], g["gy"] + 20, "L = ?", (O[0] + g["land"][0]) / 2 - 18, g["gy"] + 38)
        b += lbl(O[0] + 70, O[1] + 70, "t = ?", ORG, 13, "start", "700")
        b += ball(g["pts"], 8, 10 / 40)
        return fig("d1-0", VB, "Máy bay bay ngang ở độ cao 490 m thả gói hàng, gói rơi theo nhánh parabol xuống đất", b, "Mô phỏng: máy bay giữ vận tốc ngang v₀, gói hàng luôn ở ngay dưới máy bay (đúng thời gian thật, 10 s). Quỹ đạo tính theo công thức.")
    if k == 1:
        for u in (10, 20, 30):
            b += dot(*g["pts"][u], 3.5, GRN)
        b += live(p, g["pts"], [46] * 41, [0.0 + 70 * u / 40 for u in range(41)], 8, 10 / 40)
        b += lbl(O[0] + 24, g["pts"][10][1] - 12, "vₓ không đổi", BLUE, 13, "start", "700")
        b += lbl(g["pts"][30][0] - 14, g["pts"][30][1] + 44, "v_y tăng dần", ORG, 13, "end", "700")
        b += lbl(250, 28, "Ox: a = 0 (đều)", BLUE, 13, "start", "700") + lbl(250, 46, "Oy: a = g (rơi tự do)", ORG, 13, "start", "700")
        return fig("d1-1", VB, "Ở ba thời điểm cách đều nhau, mũi tên vận tốc ngang bằng nhau còn mũi tên vận tốc thẳng đứng dài dần", b, "Gợi ý 1: hai phương độc lập. Hình động chạy đúng thời gian thật (10 s). " + NOTE.replace("Hình minh hoạ, không đúng tỉ lệ.", "Quỹ đạo tính theo công thức."))
    if k == 2:
        b += axes(p, O[0], O[1], False, 50)
        b += dim(p, "o", O[0] - 60, O[1], O[0] - 60, g["gy"], "h", O[0] - 52, (O[1] + g["gy"]) / 2 + 4)
        b += lbl(g["land"][0] - 6, g["land"][1] - 12, "chạm đất: y = h", ORG, 13, "end", "700")
        b += arrow(p, "r", O[0], O[1], O[0] + 62, O[1], 3) + lbl(O[0] + 24, O[1] - 8, "v₀", RED, 13, "start", "700")
        b += lbl(250, 28, "Đề cho: h, v₀", "currentColor", 13) + lbl(250, 46, "Hỏi: t, L", ORG, 13, "start", "700")
        return fig("d1-2", VB, "Hệ trục Oxy gốc tại chỗ thả, Oy hướng xuống; khi chạm đất y bằng h", b, "Gợi ý 2: chọn gốc O, Oy xuống; chạm đất thì y = h. " + NOTE)
    b += dim(p, "o", O[0] - 4, O[1] + 8, O[0] - 4, g["gy"], "", 0, 0)
    b += lbl(O[0] + 8, (O[1] + g["gy"]) / 2, "① h = ½gt² → t", ORG, 13, "start", "700")
    b += dim(p, "b", O[0], g["gy"] + 20, g["land"][0], g["gy"] + 20, "② L = v₀·t", (O[0] + g["land"][0]) / 2 - 36, g["gy"] + 38)
    return fig("d1-3", VB, "Bước một dùng phương thẳng đứng để tìm thời gian, bước hai dùng phương ngang để tìm tầm xa", b, "Gợi ý 3: ① phương đứng tìm t, ② phương ngang tìm L. " + NOTE)

# ───────────── Dạng 2: vách đá, h=78,4, v0=30 ─────────────
def d2(k):
    O = (64, 56); g = ngang_geom(78.4, 30, O, 230, 150); p = f"d2{k}"
    cliff = f'<rect x="16" y="{O[1]}" width="{O[0] - 16}" height="{g["gy"] - O[1]:.1f}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b = defs(p) + ground(g["gy"]) + cliff + dot(*O, 4.5, "currentColor") + poly(g["pts"], GRN, 2.4, "" if k else "6 4") + dot(*g["land"], 4.5, GRN)
    lx, ly = g["land"]; vx, vy = 30, 39.2; n = math.hypot(vx, vy)
    tan = (lx - 38 * vx / n, ly - 38 * vy / n)
    def inset(labels=True, formula=False):
        A = (336, 66); B = (396, 66); C = (396, 66 + 60 * vy / vx)
        s_ = seg(*A, *B, BLUE, 3) + seg(*B, *C, ORG, 3) + seg(*A, *C, RED, 3)
        s_ = arrow(p, "b", *A, *B, 3) + arrow(p, "o", *B, *C, 3) + arrow(p, "r", *A, *C, 3)
        s_ += arc(A[0], A[1], 26, -math.degrees(math.atan2(vy, vx)), 0, RED, 1.8)
        if labels:
            s_ += sub(A[0] + 30, A[1] - 8, "v", "x", BLUE) + sub(B[0] - 6, (B[1] + C[1]) / 2, "v", "y", ORG, 13, "end") + lbl(A[0] + 4, A[1] + 58, "v", RED, 14, "end", "700")
            s_ += lbl(A[0] + 30, A[1] + 15, "α", RED, 13)
        if formula:
            s_ += lbl(300, 176, "tanα = v_y / vₓ", RED, 13, "start", "700") + lbl(300, 196, "v = √(vₓ² + v_y²)", RED, 13, "start", "700")
        return s_
    if k == 0:
        b += arrow(p, "r", O[0], O[1], O[0] + 58, O[1], 3) + lbl(O[0] + 12, O[1] - 8, "v₀ = 30 m/s", RED, 13, "start", "700")
        b += dim(p, "o", O[0] + 10, O[1] + 4, O[0] + 10, g["gy"], "h = 78,4 m", O[0] + 18, (O[1] + g["gy"]) / 2 + 4)
        b += arrow(p, "r", *tan, lx, ly - 2, 3) + lbl(lx - 8, ly - 46, "v = ?  α = ?", RED, 13, "end", "700")
        b += ball(g["pts"], 8, 4 / 40)
        return fig("d2-0", VB, "Hòn đá ném ngang từ mép vách đá cao 78,4 m, cần tìm vận tốc và góc lúc chạm đất", b, "Mô phỏng: hòn đá ném ngang (đúng thời gian thật, 4 s). Quỹ đạo tính theo công thức.")
    if k == 1:
        b += arrow(p, "r", *tan, lx, ly - 2, 3) + inset(True)
        b += lbl(210, 232, "Vận tốc lúc chạm đất = vₓ ⊥ v_y", "currentColor", 12, "start", "400")
        b += lbl(O[0] + 70, O[1] - 12, "vₓ không đổi", BLUE, 13, "start", "700")
        return fig("d2-1", VB, "Tam giác vận tốc lúc chạm đất: vận tốc ngang và vận tốc thẳng đứng vuông góc, tổng hợp thành vận tốc v", b, "Gợi ý 1: v là tổng hợp của hai thành phần vuông góc. " + NOTE)
    if k == 2:
        b += axes(p, O[0], O[1], False, 46)
        b += dim(p, "o", O[0] + 16, O[1] + 4, O[0] + 16, g["gy"], "t = ? (từ h)", O[0] + 24, (O[1] + g["gy"]) / 2 + 4)
        b += arrow(p, "b", O[0], O[1], O[0] + 58, O[1], 3) + lbl(O[0] + 64, O[1] - 8, "vₓ = v₀ = 30 (đã biết)", BLUE, 13, "start", "700")
        b += lbl(200, 232, "① tìm t từ h  ② v_y = g·t", ORG, 13, "start", "700")
        return fig("d2-2", VB, "Chọn gốc tại mép vách; thời gian rơi tìm từ độ cao còn vận tốc ngang đã biết", b, "Gợi ý 2: tìm t từ h trước, vₓ đã biết ngay. " + NOTE)
    b += arrow(p, "r", *tan, lx, ly - 2, 3) + inset(True, True)
    return fig("d2-3", VB, "Tam giác vận tốc với công thức độ lớn vận tốc và tang của góc", b, "Gợi ý 3: công thức tổng hợp vận tốc. " + NOTE)

# ───────────── Dạng 3: mái nhà, h=19,6, L=15, cây 10 m ở x=10 m ─────────────
def d3(k):
    O = (70, 44); g = ngang_geom(19.6, 7.5, O, 300, 165); p = f"d3{k}"; s = g["s"]; gy = g["gy"]
    house = f'<rect x="16" y="{O[1]}" width="{O[0] - 16}" height="{gy - O[1]:.1f}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    tx = O[0] + s * 10; ttop = gy - s * 10
    tree = seg(tx, gy, tx, ttop, "#4ade80", 4) + seg(tx - 9, ttop, tx + 9, ttop, "#4ade80", 4)
    b = defs(p) + ground(gy) + house + tree + dot(*O, 4.5, "currentColor") + poly(g["pts"], GRN, 2.4, "" if k else "6 4") + dot(*g["land"], 4.5, GRN)
    ty = O[1] + s * 0.5 * G * (10 / 7.5) ** 2
    b += lbl(tx - 8, gy - 8, "cây 10 m", "#4ade80", 13, "end", "700")
    if k == 0:
        b += arrow(p, "r", O[0], O[1], O[0] + 50, O[1], 3) + lbl(O[0] + 4, O[1] - 10, "v₀ = ?", RED, 13, "start", "700")
        b += dim(p, "o", O[0] + 12, O[1] + 4, O[0] + 12, gy, "", 0, 0) + lbl(O[0] + 18, (O[1] + gy) / 2 - 4, "h =", ORG, 13, "start", "700") + lbl(O[0] + 18, (O[1] + gy) / 2 + 12, "19,6 m", ORG, 12, "start", "700")
        b += dim(p, "b", O[0], gy + 20, g["land"][0], gy + 20, "L = 15 m", (O[0] + g["land"][0]) / 2 - 24, gy + 38)
        b += lbl(250, 60, "Ném từ mép mái nhà", "currentColor", 13, "start", "400") + lbl(250, 80, "Cây cách chân nhà 10 m", "currentColor", 13, "start", "400")
        b += ball(g["pts"], 8, 2 * 2 / 40)
        return fig("d3-0", VB3, "Hòn đá ném ngang từ mép mái nhà cao 19,6 m, rơi cách chân nhà 15 m, trên đường bay có một cây cao 10 m cách nhà 10 m", b, "Mô phỏng: hòn đá ném từ mái nhà (chạy chậm 2 lần). Quỹ đạo tính theo công thức.")
    if k == 1:
        b += dim(p, "o", O[0] + 12, O[1] + 4, O[0] + 12, gy, "h → t", O[0] + 18, (O[1] + gy) / 2 + 4)
        b += dim(p, "b", O[0], gy + 20, g["land"][0], gy + 20, "L → v₀ = L / t", (O[0] + g["land"][0]) / 2 - 40, gy + 38)
        b += lbl(250, 70, "Thời gian t chung", ORG, 14, "start", "700") + lbl(250, 90, "nối hai phương", ORG, 14, "start", "700")
        return fig("d3-1", VB3, "Thời gian bay tìm từ độ cao, rồi dùng chính thời gian đó với tầm xa để tìm vận tốc ném", b, "Gợi ý 1: thời gian là cầu nối giữa hai phương. " + NOTE)
    if k == 2:
        b += dot(tx, ty, 5, ORG) + seg(O[0], ty, tx, ty, ORG, 1.6, "5 4") + seg(tx, ty, tx, O[1], ORG, 1.6, "5 4")
        b += dim(p, "o", tx + 12, O[1], tx + 12, ty, "", 0, 0) + lbl(tx + 18, (O[1] + ty) / 2 + 4, "y₁ = đã rơi", ORG, 13, "start", "700")
        b += lbl(tx + 18, (ty + ttop) / 2 + 24, "so với ngọn cây?", "#4ade80", 13, "start", "700")
        b += lbl(tx, gy + 20, "x = 10 m", BLUE, 13, "middle", "700")
        return fig("d3-2", VB3, "Tại vị trí cây, tìm hòn đá đã rơi xuống bao nhiêu rồi so với ngọn cây", b, "Gợi ý 2: tìm lúc đá tới x = 10 m, rồi độ cao còn lại. " + NOTE)
    for i, t in enumerate(["① t = √(2h/g)", "② v₀ = L / t", "③ t₁ = x / v₀", "④ y₁ = ½g·t₁²", "⑤ h − y₁ so với 10 m"]):
        b += lbl(250, 50 + i * 24, t, RED if i < 2 else ORG, 13, "start", "700")
    return fig("d3-3", VB3, "Năm bước tính: thời gian bay, vận tốc ném, thời gian tới cây, độ rơi, độ cao còn lại", b, "Gợi ý 3: các công thức theo thứ tự. " + NOTE)

# ───────────── Dạng 4: ném xiên mặt đất, v0=9,8, α=30° ─────────────
def d4(k):
    s = 300 / (9.8 ** 2 * math.sin(math.radians(60)) / G); O = (90, 112); g = xien_geom(9.8, 30, 0, O, s); p = f"d4{k}"
    vb = "0 0 420 156"; top = g["top"]; land = g["land"]
    b = defs(p) + ground(112) + poly(g["pts"], GRN, 2.4, "" if k else "6 4") + dot(*O, 4.5, "currentColor") + dot(*land, 4.5, GRN)
    ang = math.radians(30)
    if k == 0:
        b += arrow(p, "r", *O, O[0] + 60 * math.cos(ang), O[1] - 60 * math.sin(ang), 3) + lbl(O[0] - 16, 56, "v₀ = 9,8 m/s", RED, 13, "start", "700")
        b += arc(*O, 28, 0, 30, RED) + lbl(O[0] + 32, O[1] - 6, "α = 30°", RED, 12, "start", "700")
        b += dim(p, "o", top[0], top[1] + 2, top[0], 112, "H = ?", top[0] + 6, (top[1] + 112) / 2 + 6)
        b += dim(p, "b", O[0], 134, land[0], 134, "L = ?", (O[0] + land[0]) / 2 - 18, 152)
        b += lbl(250, 30, "t bay = ?", ORG, 13, "start", "700")
        b += ball(g["pts"], 20, 4 / 60)
        return fig("d4-0", vb, "Vận động viên bật nhảy từ mặt đất với vận tốc 9,8 m/s hợp phương ngang 30 độ, cần tìm tầm cao, thời gian bay và tầm xa", b, "Mô phỏng: ném xiên từ mặt đất (chạy chậm 4 lần). Quỹ đạo tính theo công thức.")
    if k == 1:
        ts = [i / 60 for i in range(61)]
        vyv = [g["vy"] - G * t * g["T"] for t in ts]            # m/s, dương = lên
        b += live(p, g["pts"], [60 * g["vx"] / 9.8 * 0.9] * 61, [-v * 7.1 for v in vyv], 20, 3 / 60)
        b += lbl(O[0] + 6, O[1] + 20, "vₓ không đổi", BLUE, 13, "start", "700") + lbl(16, 26, "v_y: lên → 0 → xuống", ORG, 13, "start", "700")
        b += lbl(top[0] - 20, top[1] - 16, "đỉnh: chỉ còn vₓ (v_y = 0)", BLUE, 12, "start", "700")
        return fig("d4-1", vb, "Vận tốc đầu tách thành thành phần ngang không đổi và thành phần thẳng đứng hướng lên; tại đỉnh chỉ còn thành phần ngang", b, "Gợi ý 1: v₀ tách thành hai thành phần; hình động chạy chậm 3 lần. Quỹ đạo tính theo công thức.")
    if k == 2:
        b += seg(top[0], top[1], top[0], 112, "currentColor", 1.2, "4 4", .6)
        b += dim(p, "g", O[0], top[1] - 18, top[0], top[1] - 18, "lên: t₁", O[0] + 24, top[1] - 24) + dim(p, "g", top[0], top[1] - 18, land[0], top[1] - 18, "xuống: t₁", top[0] + 30, top[1] - 24)
        b += dot(*top, 4.5, ORG) + lbl(top[0] + 6, top[1] + 18, "v_y = 0", ORG, 13, "start", "700")
        b += lbl(360, 100, "cùng độ cao → xuống = lên", "currentColor", 12, "end", "400")
        return fig("d4-2", vb, "Quỹ đạo đối xứng qua đỉnh: thời gian đi lên bằng thời gian đi xuống vì điểm rơi cùng độ cao điểm bật", b, "Gợi ý 2: tại đỉnh v_y = 0; lên và xuống đối xứng. " + NOTE)
    b += dim(p, "o", top[0], top[1] + 2, top[0], 112, "H = v₀y² / 2g", top[0] + 6, (top[1] + 112) / 2 + 6)
    b += dim(p, "b", O[0], 134, land[0], 134, "L = vₓ·t", (O[0] + land[0]) / 2 - 24, 152)
    b += lbl(O[0] + 4, 24, "t₁ = v₀y / g ;  t = 2t₁", "currentColor", 13, "start", "700")
    return fig("d4-3", vb, "Công thức tầm cao, thời gian bay và tầm xa ghi lên quỹ đạo", b, "Gợi ý 3: công thức cho từng đại lượng. " + NOTE)

# ───────────── Dạng 5: ném xiên từ vách, h=22,05, v0=14,7, α=30° ─────────────
def d5(k):
    O = (92, 48); s = 300 / (14.7 * math.cos(math.radians(30)) * 3); g = xien_geom(14.7, 30, 22.05, O, s); p = f"d5{k}"
    gy = O[1] + s * 22.05; vb = f"0 0 420 {gy + 40:.0f}"; top = g["top"]; land = g["land"]; ang = math.radians(30)
    cliff = f'<rect x="16" y="{O[1]}" width="{O[0] - 16}" height="{gy - O[1]:.1f}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b = defs(p) + ground(gy) + cliff + poly(g["pts"], GRN, 2.4, "" if k else "6 4") + dot(*O, 4.5, "currentColor") + dot(*land, 4.5, GRN)
    A = (O[0] + s * g["vx"] * 2 * g["tu"], O[1])
    if k == 0:
        b += arrow(p, "r", *O, O[0] + 56 * math.cos(ang), O[1] - 56 * math.sin(ang), 3) + lbl(O[0] + 62, O[1] - 36, "v₀ = 14,7 m/s", RED, 13, "start", "700")
        b += arc(*O, 26, 0, 30, RED) + lbl(O[0] + 30, O[1] + 14, "α = 30°", RED, 12, "start", "700")
        b += lbl(20, O[1] + 40, "h =", ORG, 13, "start", "700") + lbl(20, O[1] + 58, "22,05 m", ORG, 12, "start", "700")
        b += dim(p, "b", O[0], gy + 20, land[0], gy + 20, "L = ?", (O[0] + land[0]) / 2 - 18, gy + 38)
        b += lbl(236, 24, "H_max (so với đất) = ?", ORG, 12, "start", "700") + lbl(300, 100, "t bay = ?", ORG, 13, "start", "700")
        b += ball(g["pts"], 10, 1.5 * 3 / 60)
        return fig("d5-0", vb, "Hòn đá ném lên từ mép vách cao 22,05 m với vận tốc 14,7 m/s hợp phương ngang 30 độ rồi rơi xuống chân vách", b, "Mô phỏng: ném xiên từ mép vách (chạy chậm 1,5 lần). Quỹ đạo tính theo công thức.")
    if k == 1:
        b += seg(O[0], O[1], A[0] + 40, O[1], "currentColor", 1.4, "5 4", .7) + dot(*A, 5, ORG)
        b += lbl(A[0] + 8, O[1] - 8, "A: cùng độ cao với O", ORG, 12, "start", "700")
        b += lbl(O[0] + 6, O[1] - 30, "công thức quen", "currentColor", 12, "start", "700") + lbl(O[0] + 6, O[1] - 16, "chỉ đúng từ O tới A", "currentColor", 12, "start", "700")
        b += dim(p, "o", A[0], O[1] + 4, A[0], gy, "h", A[0] - 10, (O[1] + gy) / 2 + 4, "end")
        b += lbl(A[0] - 16, (O[1] + gy) / 2 + 40, "đất thấp hơn A một đoạn h", ORG, 12, "end", "700")
        return fig("d5-1", vb, "Quỹ đạo quay lại độ cao điểm ném tại điểm A rồi còn rơi thêm một đoạn h xuống mặt đất", b, "Gợi ý 1: công thức quen chỉ đúng khi rơi cùng độ cao. " + NOTE)
    if k == 2:
        b += axes(p, O[0], O[1], True, 36) + dim(p, "o", O[0] + 10, O[1] + 4, O[0] + 10, gy, "", 0, 0)
        b += lbl(O[0] + 16, (O[1] + gy) / 2 + 6, "vị trí đất so với O?", ORG, 13, "start", "700")
        b += lbl(land[0] + 6, land[1] + 24, "chạm đất", ORG, 13, "end", "700")
        b += lbl(250, 44, "→ phương trình theo t", "currentColor", 13, "start", "700") + lbl(250, 62, "→ nghiệm nào nhận?", "currentColor", 13, "start", "700")
        return fig("d5-2", vb, "Hệ trục gốc tại mép vách, Oy hướng lên; mặt đất nằm dưới gốc toạ độ một đoạn bằng độ cao vách", b, "Gợi ý 2: đặt trục Oy lên; mặt đất ở dưới O. " + NOTE)
    for i, t in enumerate(["① y(t) khi chạm đất → t", "② L = vₓ·t", "③ H_max = h + v₀y²/2g", "④ v = √(vₓ² + v_y²)"]):
        b += lbl(130, 112 + i * 20, t, ORG if i != 1 else BLUE, 12, "start", "700")
    return fig("d5-3", vb, "Bốn bước: giải phương trình toạ độ tìm thời gian, tầm xa, độ cao lớn nhất, vận tốc chạm đất", b, "Gợi ý 3: thứ tự bốn bước tính. " + NOTE)

# ───────────── Dạng 6: bài ngược góc ném, v0=14, L=15 ─────────────
def d6(k):
    s = 17; O = (40, 212); p = f"d6{k}"
    a1 = 0.5 * math.degrees(math.asin(0.75)); a2 = 90 - a1
    g1 = xien_geom(14, a1, 0, O, s); g2 = xien_geom(14, a2, 0, O, s); g45 = xien_geom(14, 45, 0, O, s)
    tgt = O[0] + s * 15
    b = defs(p) + ground(O[1])
    flag = seg(tgt, O[1], tgt, O[1] - 26, "#4ade80", 3) + f'<polygon points="{tgt:.1f},{O[1]-26} {tgt+16:.1f},{O[1]-20} {tgt:.1f},{O[1]-14}" fill="#4ade80"/>'
    b += dot(*O, 4.5, "currentColor")
    if k == 0:
        L = 64; ang = math.radians(45)
        b += arrow(p, "r", *O, O[0] + L * math.cos(ang), O[1] - L * math.sin(ang), 3) + lbl(O[0] + L * math.cos(ang) + 6, O[1] - L * math.sin(ang), "v₀ = 14 m/s", RED, 13, "start", "700")
        b += arc(*O, 30, 0, 45, RED) + lbl(O[0] + 34, O[1] - 8, "α = ?", RED, 13, "start", "700")
        b += flag + dim(p, "b", O[0], O[1] + 24, tgt, O[1] + 24, "L = 15 m", (O[0] + tgt) / 2 - 24, O[1] + 42)
        b += poly(g45["pts"], ORG, 2, "6 4", .9) + ball(g45["pts"], 10, 2 * 2.02 / 60)
        return fig("d6-0", "0 0 420 262", "Pháo ở mặt đất bắn đạn với tốc độ 14 m/s, cần chọn góc nghiêng để đạn rơi trúng cờ cách 15 m", b, "Mô phỏng: một lần bắn thử ở góc 45° rơi quá cờ; cần chỉnh góc để rơi đúng 15 m (chạy chậm 2 lần).")
    b += poly(g1["pts"], GRN, 2.4) + poly(g2["pts"], "#a78bfa", 2.4) + flag
    b += dot(*g1["land"], 4.5, GRN) + dot(*g2["land"], 4.5, "#a78bfa")
    b += arc(*O, 34, 0, a1, GRN) + arc(*O, 46, 0, a2, "#a78bfa")
    b += lbl(O[0] + 38, O[1] - 5, "α₁", GRN, 13, "start", "700") + lbl(O[0] + 12, O[1] - 52, "α₂", "#a78bfa", 13, "start", "700")
    if k == 1:
        b += lbl(250, 40, "cùng tầm xa L = 15 m", "currentColor", 13, "start", "700") + lbl(250, 58, "mấy góc ném thoả mãn?", ORG, 13, "start", "700")
        return fig("d6-1", "0 0 420 262", "Hai quỹ đạo khác nhau, một thấp một cao, cùng rơi đúng điểm cách pháo 15 m", b, "Gợi ý 1: hai góc ném khác nhau có thể cùng tầm xa. " + NOTE)
    if k == 2:
        b += poly(g45["pts"], ORG, 2, "6 4", .9) + dot(*g45["land"], 4.5, ORG)
        b += lbl(g45["land"][0], O[1] - 36, "45°: xa nhất", ORG, 12, "end", "700")
        b += lbl(250, 40, "α₁ + α₂ = 90°", "currentColor", 13, "start", "700")
        return fig("d6-2", "0 0 420 262", "Quỹ đạo ném góc 45 độ đi xa nhất; hai góc phụ nhau cho cùng tầm xa", b, "Gợi ý 2: góc 45° xa nhất, hai góc phụ nhau trùng tầm xa. " + NOTE)
    b += lbl(250, 36, "sin2α = g·L / v₀²", RED, 14, "start", "700") + lbl(250, 58, "t = 2v₀·sinα / g", ORG, 13, "start", "700") + lbl(250, 78, "L_max = v₀² / g  (α = 45°)", ORG, 13, "start", "700")
    return fig("d6-3", "0 0 420 262", "Công thức tìm góc, thời gian bay và tầm xa lớn nhất", b, "Gợi ý 3: công thức cần dùng. " + NOTE)

BUILD = [d1, d2, d3, d4, d5, d6]

def tbl(rows):
    body = "".join(f"<tr><td>{c}</td><td>{d_}</td><td>{k_}</td></tr>" for c, d_, k_ in rows)
    return ('<p>Mỗi câu của đề: <strong>cho dữ liệu gì, gọi kiến thức nào?</strong> Hàng có ⚠ là <strong>điều kiện áp dụng</strong> — kiểm tra trước khi dùng công thức.</p>'
            '<div class="table-scroll"><table class="tl-table tl-table--data"><thead><tr><th>Câu trong đề</th><th>Dữ liệu</th><th>Kiến thức liên quan</th></tr></thead><tbody>'
            + body + '</tbody></table></div>')

DK_NGANG = "⚠ Chỉ có trọng lực: $a_x=0$; $a_y=g$ (Ox đều, Oy rơi tự do)"
ANALYSIS = [
 [("\"bay ngang … thả một gói hàng\"", "$\\vec v_0$ nằm ngang, $v_0=60$ m/s", "Ném ngang: tách hai phương độc lập"),
  ("\"độ cao $h=490$ m\"", "$h=490$ m", "Chạm đất khi $y=h$: $h=\\dfrac{1}{2}gt^2$"),
  ("\"bỏ qua lực cản\"", "Chỉ có trọng lực", DK_NGANG),
  ("\"sau bao lâu chạm đất?\"", "Cần $t$", "$t$ chỉ phụ thuộc $h$ và $g$, không phụ thuộc $v_0$"),
  ("\"còn cách … bao xa theo phương ngang\"", "Cần tầm xa $L$", "$L=v_0t$ (Ox thẳng đều)")],
 [("\"ném ngang … $v_0=30$ m/s\"", "$v_0=30$ m/s; $v_x=v_0$", "Ném ngang: $v_x$ không đổi"),
  ("\"vách đá cao $h=78{,}4$ m\"", "$h=78{,}4$ m", "Chạm đất khi $y=h$ → tìm $t$"),
  ("\"bỏ qua lực cản\"", "Chỉ có trọng lực", DK_NGANG),
  ("\"tại lúc chạm đất\"", "Thời điểm $t$ vừa tìm", "$v_y=gt$ tại đúng thời điểm đó"),
  ("\"độ lớn vận tốc\"", "Cần $v$", "$v_x\\perp v_y$ nên $v=\\sqrt{v_x^2+v_y^2}$"),
  ("\"góc hợp bởi vận tốc và phương ngang\"", "Cần $\\alpha$", "$\\tan\\alpha=\\dfrac{v_y}{v_x}$")],
 [("\"mép mái … cao $h=19{,}6$ m\"", "$h=19{,}6$ m", "Chạm đất khi $y=h$ → tìm $t$"),
  ("\"ném ngang\"", "$v_0$ chưa biết", "Ném ngang: $x=v_0t$"),
  ("\"bỏ qua lực cản\"", "Chỉ có trọng lực", DK_NGANG),
  ("\"chạm đất cách chân nhà 15 m\"", "$L=15$ m", "$L=v_0t$ → $v_0=L/t$ ($t$ nối hai phương)"),
  ("\"cách chân nhà 10 m có một cây cao 10 m\"", "$x=10$ m; ngọn cây cao $10$ m", "Tới $x$ lúc $t_1=x/v_0$; đã rơi $y_1=\\dfrac{1}{2}gt_1^2$"),
  ("\"có bay qua ngọn cây không?\"", "So sánh $h-y_1$ với $10$ m", "Còn cao hơn $10$ m thì bay qua")],
 [("\"bật khỏi mặt đất, $v_0=9{,}8$ m/s, góc $30^\\circ$\"", "$v_0$, $\\alpha=30^\\circ$", "Ném xiên: $v_{0x}=v_0\\cos\\alpha$; $v_{0y}=v_0\\sin\\alpha$ (hướng lên)"),
  ("\"bỏ qua lực cản\"", "Chỉ có trọng lực", "⚠ Ox thẳng đều; Oy có gia tốc $-g$ (lên là dương)"),
  ("\"điểm tiếp đất cùng độ cao điểm bật\"", "Cùng độ cao", "⚠ Điều kiện để lên và xuống đối xứng: $t=2t_1$"),
  ("\"các thành phần $v_{0x}$ và $v_{0y}$\"", "Cần $v_{0x}$, $v_{0y}$", "Hai thành phần của $\\vec v_0$"),
  ("\"lên tới điểm cao nhất, tầm cao $H$\"", "Cần $t_1$, $H$", "Tại đỉnh $v_y=0$: $t_1=\\dfrac{v_{0y}}{g}$; $H=\\dfrac{v_{0y}^2}{2g}$"),
  ("\"thời gian bay và tầm xa $L$\"", "Cần $t$, $L$", "$t=2t_1$; $L=v_{0x}t$")],
 [("\"vách đá thẳng đứng cao $h=22{,}05$ m\"", "$h=22{,}05$ m", "Điểm ném cao hơn mặt đất $h$"),
  ("\"ném lên $v_0=14{,}7$ m/s, góc $30^\\circ$\"", "$v_0$, $\\alpha=30^\\circ$", "$v_{0x}=v_0\\cos\\alpha$; $v_{0y}=v_0\\sin\\alpha$"),
  ("\"bỏ qua lực cản\"", "Chỉ có trọng lực", "⚠ Ox đều; Oy gia tốc $-g$"),
  ("\"chạm đất\" (thấp hơn điểm ném)", "Lúc đó $y=-h$", "⚠ Không dùng công thức cùng độ cao; lập $y(t)$ rồi giải: $-h=v_{0y}t-\\dfrac{1}{2}gt^2$"),
  ("\"thời gian từ lúc ném đến lúc chạm đất\"", "Cần $t$", "Nghiệm bậc hai: nhận nghiệm dương"),
  ("\"tầm xa tính từ chân vách\"", "Cần $L$", "$L=v_{0x}t$"),
  ("\"độ cao lớn nhất so với mặt đất\"", "Cần $H_{max}$", "Cao hơn điểm ném $\\dfrac{v_{0y}^2}{2g}$, rồi cộng $h$"),
  ("\"độ lớn vận tốc khi chạm đất\"", "Cần $v$", "$v=\\sqrt{v_x^2+v_y^2}$ với $v_y=v_{0y}-gt$")],
 [("\"bắn đạn lên, $v_0=14$ m/s, nòng nghiêng góc $\\alpha$\"", "$v_0=14$ m/s; $\\alpha$ chưa biết", "Ném xiên: $L$ phụ thuộc $v_0$ và $\\alpha$"),
  ("\"rơi xuống mặt phẳng ngang cùng độ cao nòng pháo\"", "Cùng độ cao", "⚠ Điều kiện dùng $L=\\dfrac{v_0^2\\sin2\\alpha}{g}$"),
  ("\"bỏ qua lực cản\"", "Chỉ có trọng lực", "⚠ Ox đều; Oy gia tốc $-g$"),
  ("\"đạn rơi cách pháo 15 m\"", "$L=15$ m", "$\\sin2\\alpha=\\dfrac{gL}{v_0^2}$"),
  ("\"góc nghiêng bao nhiêu\"", "Cần $\\alpha$", "$\\sin2\\alpha$ cho hai góc $2\\alpha$ → hai góc phụ nhau ($\\alpha$ và $90^\\circ-\\alpha$)"),
  ("\"thời gian bay trong từng trường hợp\"", "Cần $t$ cho mỗi góc", "$t=\\dfrac{2v_0\\sin\\alpha}{g}$"),
  ("\"tầm xa lớn nhất\"", "Cần $L_{max}$", "$\\sin2\\alpha\\le1$: $L_{max}=\\dfrac{v_0^2}{g}$ khi $\\alpha=45^\\circ$")],
]

def strip(html):
    return re.sub(r'<figure class="fig"[^>]*data-bt="[^"]*".*?</figure>', "", html, flags=re.S)

d = json.load(open(J))
for i, fn in enumerate(BUILD):
    q = d["dang_bai"][i]
    q["problem_html"] = strip(q["problem_html"]) + fn(0)          # mô phỏng hiện tượng nằm DƯỚI đề
    q["analysis_html"] = fn(2) + tbl(ANALYSIS[i])                  # thay gợi ý: hình dữ kiện + bảng phân tích đề (như bài mẫu trong lý thuyết)
    q.pop("hints_html", None)
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ok", len(d["dang_bai"]))
