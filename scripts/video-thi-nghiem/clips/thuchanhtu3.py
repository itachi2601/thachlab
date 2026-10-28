# Clip: tn-l12-thuchanhtu-03 - Day hop goc voi duong suc: luc giam theo sin theta (ban 1, 28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanhtu-03.json:
#   tham_so I = 3,0 A; so_lieu_mau (theta, dm g, sin, ti so): 90 -> 1,45 ; 60 -> 1,26 (0,87) ; 30 -> 0,73 (0,50);
#   rut_ra: B tinh theo F = BIl khi lech 60 do thap hon that 13%. Ghi chu JSON: "so lieu minh hoa".
# Du doan (theta = 30 do, Dm = ?): A 0,48 g = 1,45.30/90 (ti le theta) ; B 0,73 g = 1,45.sin30 (dung, so_lieu_mau) ;
#   C 1,26 g = 1,45.cos30 (= gia tri o 60 do trong so_lieu_mau) ; D 1,45 g (khong doi).
# Hinh: nhin tu tren xuong; tu truong deu giua hai mat cuc = duong suc song song cach deu, N (trai) -> S (phai).
#   Dong dien chay theo day tu dau tren-phai xuong duoi-trai: F ~ I l x B = +sin(theta) z -> F len (ra khoi man hinh),
#   khop quy tac ban tay trai. Phan luc F' len nam cham huong xuong -> can chi them Dm (da TARE). Do dai mui ten ~ sin theta.
from engine import *

ROWS = [(90, 1.45, 1.0, 1.0), (60, 1.26, 0.866, 0.869), (30, 0.73, 0.5, 0.503)]
COPPER = (184, 115, 51)
PX0, PY0, PX1, PY1 = 60, 236, 1020, 744           # khung hinh nhin tu tren
CX, CY, HL = 540, 517, 170                        # tam day, nua chieu dai canh khung
LX0, LX1 = 150, 930
LINES = [315 + 45 * i for i in range(9)]


def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")


def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)


def dashed(d, p1, p2, color, w=3, dash=12, gap=9):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))],
               fill=color, width=w)


def tag(d, x, y, s, size, color, alpha=1.0, anchor="m"):
    wd = tw(d, s, F(size)) + 22
    if anchor == "l": x = x + wd / 2
    d.rounded_rectangle([x - wd / 2, y - size * 0.64, x + wd / 2, y + size * 0.64], radius=10, fill=A(WHITE, 0.94 * alpha))
    text(d, (x, y), s, size, color, alpha=alpha)


def pill(d, cx, cy, s, size, fg, bg, alpha=1.0):
    wd = tw(d, s, F(size)) + 52
    card(d, (cx - wd / 2, cy - size * 0.85, cx + wd / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)


def out_mark(d, x, y, color, r=22):               # ky hieu "huong ra khoi man hinh" (ve tay, font khong co glyph)
    d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE, outline=color, width=5)
    dot(d, x, y, 7, color)


# ---------------- hinh nhin tu tren: hai mat cuc + duong suc + canh khung ----------------
def top_view(d, th, on=True, show_th=True, th_label=True):
    card(d, (PX0, PY0, PX1, PY1), fill=WHITE, outline=LIGHT, w=3)
    for y in LINES:
        d.line([(LX0, y), (LX1, y)], fill=(130, 155, 205), width=3)
        for x in (290, 790): chevron(d, x, y, 0, (130, 155, 205))
    d.rounded_rectangle([80, 290, LX0, 700], radius=10, fill=RED)
    d.rounded_rectangle([LX1, 290, 1000, 700], radius=10, fill=BLUE)
    text(d, (115, 495), "N", 44, WHITE); text(d, (965, 495), "S", 44, WHITE)
    tag(d, 84, 262, "nhìn từ trên xuống", 32, MUTED, anchor="l")
    arrow(d, (700, 262), (790, 262), BLUE, w=4, head=16); text(d, (804, 262), "B", 38, BLUE, anchor="lm")
    # thuoc do goc (vach 0-30-60-90)
    for a in (0, 30, 60, 90):
        r = math.radians(a)
        d.line([(CX + 205 * math.cos(r), CY - 205 * math.sin(r)), (CX + 228 * math.cos(r), CY - 228 * math.sin(r))],
               fill=GRAY, width=3)
    d.arc([CX - 216, CY - 216, CX + 216, CY + 216], 270, 360, fill=A(GRAY, 0.45), width=2)
    for a in (30, 60):
        r = math.radians(a); tag(d, CX + 262 * math.cos(r), CY - 262 * math.sin(r), f"{a}°", 32, MUTED)
    # canh duoi khung (dong) nghieng goc th so voi duong suc
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    pa = (CX + HL * c, CY - HL * s); pb = (CX - HL * c, CY + HL * s)       # dau tren-phai, dau duoi-trai
    d.line([pa, pb], fill=COPPER, width=16)
    for p in (pa, pb): dot(d, p[0], p[1], 11, COPPER, outline=WHITE)
    if on:                                        # chieu dong: tu dau tren-phai ve dau duoi-trai
        ox, oy = -40 * s, -40 * c                 # lech sang phia tren-trai cua day
        m1 = (CX + 0.95 * HL * c + ox, CY - 0.95 * HL * s + oy); m2 = (CX + 0.4 * HL * c + ox, CY - 0.4 * HL * s + oy)
        arrow(d, m1, m2, ORANGE, w=8, head=28)
        tag(d, CX + 0.62 * HL * c - 82 * s, CY - 0.62 * HL * s - 82 * c, "I", 40, ORANGE)
    if show_th and th > 2:
        d.line([(CX, CY), (CX + 150, CY)], fill=GREEN, width=4)
        d.arc([CX - 92, CY - 92, CX + 92, CY + 92], 360 - th, 360, fill=GREEN, width=5)
        am = math.radians(th / 2)
        if th_label: tag(d, CX + 128 * math.cos(am), CY - 128 * math.sin(am), "θ", 38, GREEN)
    if on and th > 2:
        out_mark(d, CX, CY, GREEN)
        text(d, (CX - 36, CY - 46), "F hướng lên", 32, GREEN, anchor="rm")


# ---------------- so do luc nhin ngang (cap truc doi) ----------------
def force_side(d, sv, alpha=1.0):
    card(d, (540, 770, 1020, 1000), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (1000, 796), "nhìn ngang", 32, MUTED, bold=False, anchor="rm")
    L = 92 * sv / 1.45
    # day (tiet dien) va luc F len
    dot(d, 640, 920, 13, COPPER, outline=WHITE)
    text(d, (610, 965), "dây", 32, COPPER, anchor="mm")
    if L > 6:
        arrow(d, (640, 905), (640, 905 - L), GREEN, w=6, head=18)
        text(d, (662, 905 - L * 0.55), "F", 38, GREEN, anchor="lm")
    # nam cham tren dia can va phan luc F' xuong
    text(d, (860, 836), "nam châm", 32, NAVY)
    d.rounded_rectangle([780, 860, 940, 936], radius=10, fill=(214, 220, 236), outline=NAVY, width=3)
    d.line([(760, 944), (960, 944)], fill=NAVY, width=6)
    text(d, (860, 972), "đĩa cân", 32, MUTED, bold=False)
    if L > 6:
        arrow(d, (860, 866), (860, 866 + L * 0.9), PURPLE, w=6, head=18)
        text(d, (846, 870 + L * 0.45), "F'", 38, PURPLE, anchor="rm")


# ---------------- do thi Dm theo theta (truc co dinh) ----------------
def plot(d, box, recs, curve=0.0, hl=None):
    x0, yt, x1, yb = box
    X = lambda a: x0 + a / 90 * (x1 - x0); Y = lambda v: yb - v / 1.6 * (yb - yt)
    for v in (0.5, 1.0, 1.5):
        dashed(d, (x0, Y(v)), (x1, Y(v)), LIGHT, 3)
        text(d, (x0 - 14, Y(v)), vn(v, 1), 34, MUTED, bold=False, anchor="rm")
    for a in (0, 30, 60, 90):
        if a: dashed(d, (X(a), yt), (X(a), yb), LIGHT, 3)
        text(d, (X(a), yb + 34), f"{a}°", 34, MUTED, bold=False)
    d.line([(x0, yb), (x1 + 24, yb)], fill=NAVY, width=5)
    d.polygon([(x1 + 40, yb), (x1 + 22, yb - 10), (x1 + 22, yb + 10)], fill=NAVY)
    d.line([(x0, yb), (x0, yt - 16)], fill=NAVY, width=5)
    d.polygon([(x0, yt - 32), (x0 - 10, yt - 14), (x0 + 10, yt - 14)], fill=NAVY)
    text(d, (x0 + 22, yt - 22), "Δm (g)", 34, INK, anchor="lm")
    text(d, (x1 + 40, yb - 34), "θ", 38, INK, anchor="rm")
    if curve > 0:
        n = 40; amax = 90 * curve
        d.line([(X(amax * k / n), Y(1.45 * math.sin(math.radians(amax * k / n)))) for k in range(n + 1)],
               fill=BLUE, width=6, joint="curve")
    for r in recs:
        if hl == r[0]: d.ellipse([X(r[0]) - 26, Y(r[1]) - 26, X(r[0]) + 26, Y(r[1]) + 26], outline=GREEN, width=5)
        dot(d, X(r[0]), Y(r[1]), 13, ORANGE, outline=WHITE)
        text(d, (X(r[0]) - 22, Y(r[1]) - 34), vn(r[1]), 34, ORANGE, anchor="rm" if r[0] == 90 else "mm")
    return X, Y


# ---------------- canh 1: Du doan ----------------
OPTS = [("A", "0,48 g"), ("B", "0,73 g"), ("C", "1,26 g"), ("D", "1,45 g")]


def s_hook(img, d, t, sc):
    top_view(d, 90, on=True)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    if k <= 0:
        card(d, (60, 790, 1020, 950), fill=WHITE, outline=NAVY, w=4, r=24)
        text(d, (300, 870), "I = 3,0 A", 46, ORANGE)
        text(d, (760, 870), "cân: 1,45 g", 46, ORANGE)
        return
    y0 = 776 + (1 - k) * 40
    card(d, (40, y0, 1040, y0 + 860), fill=A(WHITE, k), outline=A(PURPLE, k), w=5)
    pill(d, W / 2, y0 + 52, "DỰ ĐOÁN", 36, WHITE, PURPLE, k)
    text(d, (W / 2, y0 + 130), "θ = 90°, I = 3,0 A: cân chỉ 1,45 g.", 40, INK, alpha=k)
    text(d, (W / 2, y0 + 184), "Giữ I, xoay dây tới θ = 30°.", 40, INK, alpha=k)
    text(d, (W / 2, y0 + 238), "Cân chỉ khoảng bao nhiêu?", 40, INK, alpha=k)
    for i, (lab, val) in enumerate(OPTS):
        bx = 80 + (i % 2) * 470; by = y0 + 300 + (i // 2) * 250
        card(d, (bx, by, bx + 450, by + 220), fill=A((247, 248, 252), k), outline=A(NAVY, k), r=24, w=4)
        text(d, (bx + 70, by + 110), lab + ".", 52, NAVY, alpha=k)
        text(d, (bx + 270, by + 110), val, 60, NAVY, alpha=k)
    t1, t2 = sc["M"][1] + 0.4, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, y0 + 818, 940, y0 + 830], radius=6, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, y0 + 818, 140 + 800 * (1 - q), y0 + 830], radius=6, fill=A(PURPLE, k))


# ---------------- canh 2: Tien hanh ----------------
def state(t, sc):
    """(theta, dong dien bat?, so doc dang hien hoac None, cac diem da ghi)"""
    M = sc["M"]; th = 90.0; on = True; rd = ROWS[0]; recs = []
    if t >= M[0] + 0.4: recs = [ROWS[0]]
    for j, (mk, a0, a1, row) in enumerate(((M[1], 90, 60, ROWS[1]), (M[3], 60, 30, ROWS[2]))):
        if t >= mk + 0.1:
            on = False; rd = None
            th = lerp(a0, a1, ease((t - mk - 0.3) / 1.3))
        if t >= mk + 1.8: on = True
        if t >= mk + 2.0: rd = row; recs = recs + [row]
    return th, on, rd, recs


def s_do(img, d, t, sc):
    th, on, rd, recs = state(t, sc)
    top_view(d, th, on=on)
    text(d, (990, 718), f"θ = {round(th)}°", 40, GREEN, anchor="rm")
    card(d, (60, 770, 520, 1000), fill=WHITE, outline=NAVY, w=4, r=24)
    if rd is not None:
        text(d, (290, 822), "cân đã trừ bì (tare)", 32, MUTED, bold=False)
        text(d, (290, 890), f"Δm = {vn(rd[1])} g", 52, ORANGE)
        text(d, (290, 958), "I = 3,0 A · minh hoạ", 32, MUTED, bold=False)
    elif on:
        text(d, (290, 885), "đóng mạch…", 40, MUTED, bold=False)
    else:
        text(d, (290, 860), "ngắt mạch", 42, RED)
        text(d, (290, 930), "rồi mới xoay giá", 34, MUTED, bold=False)
    force_side(d, rd[1] if (rd is not None and on) else 0.0)
    card(d, (60, 1024, 1020, 1650), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (210, 1100, 920, 1560), recs)
    text(d, (980, 1060), "số liệu minh hoạ", 32, MUTED, bold=False, anchor="rm")


# ---------------- canh 3: Dap an + Rut ra ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 236, 1020, 700), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (210, 300, 920, 610), ROWS, curve=ease((t - M[1] + 0.2) / 1.2), hl=30 if t > M[0] else None)
    kc = appear(t, M[1] + 0.6, 0.4)
    if kc > 0: text(d, (910, 470), "đường: Δm(90°)·sin θ", 34, BLUE, anchor="rm", alpha=kc)
    ka = appear(t, M[0] - 0.1, 0.4)
    if ka > 0: pill(d, 580, 556, "ĐÁP ÁN B · 0,73 g", 34, WHITE, GREEN, ka)
    # bang so lieu
    card(d, (60, 724, 1020, 1100), fill=WHITE, outline=NAVY, w=4, r=24)
    cols = [(170, "θ"), (380, "Δm (g)"), (640, "Δm/Δm(90°)"), (880, "sin θ")]
    for x, h in cols: text(d, (x, 774), h, 34, INK)
    d.line([(90, 806), (990, 806)], fill=LIGHT, width=3)
    k2 = appear(t, M[0] + 0.8, 0.45)
    for j, (a, dm, sn, rt) in enumerate(ROWS):
        y = 856 + j * 80
        text(d, (170, y), f"{a}°", 38, NAVY)
        text(d, (380, y), vn(dm), 38, ORANGE)
        text(d, (640, y), vn(rt), 38, GREEN, alpha=k2)
        text(d, (880, y), vn(sn), 38, GREEN, alpha=k2)
    text(d, (980, 1078), "số liệu minh hoạ", 32, MUTED, bold=False, anchor="rm")
    kh = appear(t, M[1] - 0.2, 0.45)
    if kh > 0: d.rounded_rectangle([510, 820, 990, 1048], radius=18, outline=A(GREEN, kh), width=4)
    # the rut ra
    for y, title, ev, col, at in ((1124, "F = B·I·l·sin θ", "lớn nhất khi dây vuông góc đường sức", GREEN, M[1] + 0.8),
                                  (1340, "Lệch 60°: B tính theo F = BIl thấp 13%", "vì sin 60° ≈ 0,87",
                                   ORANGE, M[2] - 0.25)):
        k = appear(t, at, 0.45)
        if k <= 0: continue
        yy = y + (1 - k) * 30
        card(d, (60, yy, 1020, yy + 196), fill=A(WHITE, k), outline=A(col, k), w=5)
        text(d, (W / 2, yy + 62), title, 42, col, alpha=k)
        text(d, (W / 2, yy + 140), ev, 36, MUTED, bold=False, alpha=k)


# ---------------- canh 4: Bay + chua noi duoc ----------------
def mini(d, x0, y0, th, lab, col, al=1.0):     # o nho: 3 duong suc + canh day goc th
    card(d, (x0, y0, x0 + 430, y0 + 250), fill=A((247, 248, 252), al), outline=A(LIGHT, al), r=20, w=3)
    for k in range(3):
        yy = y0 + 50 + k * 55
        d.line([(x0 + 30, yy), (x0 + 400, yy)], fill=A((130, 155, 205), al), width=3)
        chevron(d, x0 + 330, yy, 0, A((130, 155, 205), al))
    cx, cy = x0 + 215, y0 + 105; hl = 80 if th else 110
    c, s_ = math.cos(math.radians(th)), math.sin(math.radians(th))
    cy2 = cy + (27 if th == 0 else 0)
    d.line([(cx - hl * c, cy2 + hl * s_), (cx + hl * c, cy2 - hl * s_)], fill=A(COPPER, al), width=12)
    if th: out_mark(d, cx, cy2, GREEN, r=18)
    text(d, (cx, y0 + 218), lab, 34, col, alpha=al)


def s_bay(img, d, t, sc):
    M = sc["M"]
    top_view(d, 0, on=True, show_th=False)
    tag(d, CX, CY + 130, "θ = 0°: dây song song đường sức", 34, NAVY)
    tag(d, CX, CY + 72, "F = 0", 40, RED)
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3
    y = 790
    if a1 > 0:
        card(d, (60, y, 1020, y + 820), fill=A(WHITE, a1), outline=A(RED, a1), w=5)
        pill(d, W / 2, y + 60, "BẪY", 38, WHITE, RED, a1)
        q = "“Dây song song đường sức thì lực từ lớn nhất”"
        ls = wrap(d, q, F(42), 840); ks = clamp((t - M[1] + 0.2) / 0.4) * a1
        for j, l in enumerate(ls):
            yy = y + 160 + j * 56; lw = tw(d, l, F(42))
            text(d, (W / 2, yy), l, 42, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)],
                              fill=A(RED, 0.8 * a1), width=4)
        for j, (th, lab, col) in enumerate(((0, "θ = 0°: F = 0", RED), (90, "θ = 90°: F lớn nhất", GREEN))):
            mini(d, 100 + j * 450, y + 270, th, lab, col, a1)
        k2 = appear(t, M[1], 0.45) * a1
        ctext(d, y + 600, "Sai: θ = 0° thì sin θ = 0, F = 0", 44, RED, alpha=k2)
        ctext(d, y + 720, "B nam châm không đổi khi xoay dây", 38, MUTED, bold=False, maxw=860, alpha=k2)
    if k3 > 0:
        card(d, (60, y, 1020, y + 820), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, y + 70), "Thí nghiệm chưa nói được", 44, NAVY, alpha=k3)
        for j, s in enumerate(("• Góc khác ngoài 90°, 60°, 30°", "• F có tỉ lệ với l? (chưa đổi l)",
                               "• Số liệu: minh hoạ, không đo thật")):
            text(d, (110, y + 220 + j * 150), s, 40, INK, bold=False, anchor="lm", alpha=k3)


# ---------------- canh 5: Chot + cau hoi ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 250, 1020, 500), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 375, "Xoay dây: B không đổi, lực từ đổi theo sin θ", 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 540, 1040, 1090), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 570, W / 2 + pw / 2, 634), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 602), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 730, "Vì sao phải chỉnh dây vuông góc\nđường sức trước khi đo B?", 46, INK, maxw=880,
          alpha=appear(t, M[0] + 0.4, 0.5))
    text(d, (W / 2, 850), "θ = 90°: 1,45 g  ·  θ = 60°: 1,26 g", 40, MUTED, bold=False, alpha=k1)
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 910, 970, 1060), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 985, "Gợi ý: nhìn lại cột sin θ", 42, ORANGE, maxw=820, alpha=kh)
    # hinh nhac lai (khong so): day lech goc theta trong tu truong deu
    km = appear(t, M[0] + 0.3, 0.5)
    card(d, (60, 1120, 1020, 1650), fill=A(WHITE, km), outline=A(LIGHT, km), w=3)
    for k in range(6):
        yy = 1180 + k * 80
        d.line([(120, yy), (960, yy)], fill=A((130, 155, 205), km), width=3)
        chevron(d, 760, yy, 0, A((130, 155, 205), km))
    text(d, (130, 1150), "B", 38, BLUE, anchor="lm", alpha=km)
    cx, cy = 540, 1420; c, s_ = math.cos(math.radians(60)), math.sin(math.radians(60))
    d.line([(cx - 180 * c, cy + 180 * s_), (cx + 180 * c, cy - 180 * s_)], fill=A(COPPER, km), width=14)
    d.line([(cx, cy), (cx + 150, cy)], fill=A(GREEN, km), width=4)
    d.arc([cx - 90, cy - 90, cx + 90, cy + 90], 300, 360, fill=A(GREEN, km), width=5)
    tag(d, cx + 125 * math.cos(math.radians(30)), cy - 125 * math.sin(math.radians(30)), "θ", 38, GREEN, alpha=km)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][1] + 1.8, "tap"), (do["t0"] + do["M"][3] + 1.8, "tap"),
            (r["t0"] + r["M"][0] - 0.1, "ding"), (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]


CLIP = dict(id="tn-l12-thuchanhtu-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Đo cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dây hợp góc với đường sức", draw=s_hook, tail=0.3, caps=[
   ("Dây vuông góc đường sức: cân chỉ 1,45 g.", 2.8),
   ("Dừng vài giây, chọn A, B, C hay D.", 6.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("θ = 90°: dây vuông góc đường sức.", 2.6),
   ("Ngắt mạch, xoay giá tới θ = 60°.", 2.6),
   ("Đóng mạch lại: cân chỉ 1,26 g.", 2.4),
   ("Ngắt, xoay tiếp tới θ = 30°.", 2.6),
   ("Đóng mạch: cân chỉ 0,73 g, giảm nhiều.", 2.8)]),
 dict(key="rut", title="Kết luận", draw=s_rut, tail=0.4, caps=[
   ("30° cho 0,73 g: đáp án B.", 2.4),
   ("Δm chia Δm(90°) đúng bằng sin θ.", 3.0),
   ("Dây lệch 60°: B tính ra thấp hơn 13%.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Bẫy: song song đường sức, lực lớn nhất?", 3.0),
   ("Sai: song song thì F = 0, B vẫn như cũ.", 3.0),
   ("Thí nghiệm này chưa nói được gì?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Thử nghĩ: vì sao phải chỉnh θ = 90°?", 4.4)]),
])
