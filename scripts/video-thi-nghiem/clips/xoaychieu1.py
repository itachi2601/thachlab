# Clip: tn-l12-xoaychieu-01 - May phat mini quay tay: bien do U0 theo toc do quay
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-xoaychieu-01.json:
#   so_lieu_mau: n = 2, 4, 6, 8, 10 vong/s -> U0 = 0,95 ; 1,82 ; 2,84 ; 3,67 ; 4,70 V ; U0/n = 0,475 ; 0,455 ; 0,473 ; 0,459 ; 0,470
#   (TB 0,466 ≈ 0,47 V.s); rut_ra: f = n (moi vong mot chu ki). tham_so: n 1..12 vong/s.
#   LUU Y kho: tham_so mac dinh N=100, B=0,1 T, S=0,02 m2 cho E0 = NBS.2.pi.n ≈ 1,26.n V, KHONG khop U0/n ≈ 0,47 cua so_lieu_mau
#   -> clip KHONG hien N, B, S (bao thay).
# Ban 2 (26/11/2026, viec 4 lo 32, cong --do-chu moi): canh hook / do / ans / bay / gioi / end nhu mau xoaychieu2.
#   Du doan (K10 khong ve nut; khung web A-D): 4 -> 8 vong/s, bien do U0? -> gap doi (hien_tuong_hay_sai #1: chi tan so tang).
#   Bay: "quay nhanh: song chi day hon?" -> so voi man do duoc: cao va day gap doi.
#   Chot (khung web A-D, dap an KHONG hien): man do U0 = 2,35 V -> n ≈ 2,35 / 0,47 = 5 vong/s (ca suy tu U0/n, 5 trong 1..12).
# Toa do mp4 = 65 + 0,88.x; chu >= 56 px (ra >= 49 px).
from engine import *

ROWS = [(2, "0,95", "0,475"), (4, "1,82", "0,455"), (6, "2,84", "0,473"), (8, "3,67", "0,459"), (10, "4,70", "0,470")]
U0 = {2: 0.95, 4: 1.82, 6: 2.84, 8: 3.67, 10: 4.70, 5: 2.35}
assert all(abs(U0[n] / n - float(r.replace(",", "."))) < 6e-4 for n, _, r in ROWS)
assert round(2.35 / 0.47) == 5 and abs(sum(U0[n] / n for n in (2, 4, 6, 8, 10)) / 5 - 0.466) < 1e-3
SCR = (134, 239, 172)
NOTE = (70, 75, 95)
COP, COP_D = (196, 120, 52), (130, 72, 28)
DGREEN = (21, 128, 61); DARK_OR = (181, 71, 8)

def chev(d, x, y, ang, color, L=18, w=5):
    for s in (1, -1):
        a = ang + math.pi - s * math.radians(30)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=color, width=w)

# ---------------- nam cham chu U chuan (port PIL tu u_magnet / svg_lib.py) ----------------
UM_BODY, UM_DARK, UM_EDGE = (203, 213, 225), (148, 163, 184), (51, 65, 85)
UM_N = ((220, 38, 38), (248, 113, 113), (185, 28, 28))      # mat truoc, mat tren, mat ben
UM_S = ((37, 99, 235), (96, 165, 250), (30, 64, 175))

def _arc(cx, cy, R, a0, a1, n=10):
    return [(cx + R * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + R * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
            for k in range(n + 1)]

def _u_poly(x, y, w, h, arm, yoke, r, ri):
    yi = y + h - yoke
    p = [(x, y)] + _arc(x + r, y + h - r, r, 180, 90) + _arc(x + w - r, y + h - r, r, 90, 0) + [(x + w, y), (x + w - arm, y)]
    p += _arc(x + w - arm - ri, yi - ri, ri, 0, 90) + _arc(x + arm + ri, yi - ri, ri, 90, 180) + [(x + arm, y)]
    return p

def u_magnet_pil(d, x, y, w, h, arm, yoke, tip, dep=(18, -12), fs=56, sw=4):
    """Nam cham chu U nhin chinh dien hoi xien (mat sau doi dep). Canh huong len, cuc N canh trai, S canh phai."""
    dx, dy = dep; r = min(arm, yoke) * 0.7; ri = min(arm, yoke) * 0.35; xr = x + w
    P = lambda pts, f: d.polygon(pts, fill=f, outline=UM_EDGE, width=sw)
    P([(a + dx, b + dy) for a, b in _u_poly(x, y, w, h, arm, yoke, r, ri)], UM_DARK)
    P([(xr, y), (xr + dx, y + dy), (xr + dx, y + h - r + dy), (xr, y + h - r)], UM_DARK)          # mat ben phai
    P([(xr, y), (xr + dx, y + dy), (xr + dx, y + tip + dy), (xr, y + tip)], UM_S[2])
    P([(x + arm, y), (x + arm + dx, y + dy), (x + arm + dx, y + tip + dy), (x + arm, y + tip)], UM_N[2])  # mat trong canh N
    P([(x, y), (x + arm, y), (x + arm + dx, y + dy), (x + dx, y + dy)], UM_N[1])                  # mat tren hai canh
    P([(xr - arm, y), (xr, y), (xr + dx, y + dy), (xr - arm + dx, y + dy)], UM_S[1])
    k = 0.2929 * r
    d.line([(xr - k, y + h - k), (xr - k + dx, y + h - k + dy)], fill=UM_EDGE, width=sw)
    P(_u_poly(x, y, w, h, arm, yoke, r, ri), UM_BODY)
    d.rectangle([x, y, x + arm, y + tip], fill=UM_N[0], outline=UM_EDGE, width=sw)
    d.rectangle([xr - arm, y, xr, y + tip], fill=UM_S[0], outline=UM_EDGE, width=sw)
    text(d, (x + arm / 2, y + tip / 2), "N", fs, WHITE)
    text(d, (xr - arm / 2, y + tip / 2), "S", fs, WHITE)

# ---------------- may phat mini: nam cham U + khung day quay giua hai cuc ----------------
MX, MY, MW, MH, ARM, YOKE, TIP = 90, 440, 360, 300, 80, 80, 150
GX0, GX1 = MX + ARM, MX + MW - ARM               # mat trong cuc N, cuc S
CXC, CYC = (GX0 + GX1) / 2, MY + TIP / 2         # tam khung day

def generator(d, theta, n_lab, slow=False):
    """theta: goc quay khung (rad). n_lab: chuoi toc do (None = chua quay)."""
    card(d, (40, 250, 520, 890), fill=WHITE, outline=LIGHT, w=3)
    # truc + tay quay o tren
    d.line([(CXC, CYC - 60), (CXC, 330)], fill=NAVY, width=8)
    cr = 34; hx = CXC + cr * math.cos(theta); hy = 330 + 0.35 * cr * math.sin(theta)
    d.ellipse([CXC - cr, 330 - 12, CXC + cr, 330 + 12], outline=NAVY, width=5)
    d.line([(CXC, 330), (hx, hy)], fill=NAVY, width=7)
    d.line([(hx, hy), (hx, hy - 40)], fill=ORANGE, width=12)
    u_magnet_pil(d, MX, MY, MW, MH, ARM, YOKE, TIP)
    # duong suc giua hai cuc: song song, cach deu, N -> S
    for yy in (MY + 30, MY + 75, MY + 120):
        d.line([(GX0 + 4, yy), (GX1 - 4, yy)], fill=A(PURPLE, 0.75), width=4)
        chev(d, GX0 + 34, yy, 0, A(PURPLE, 0.9), L=16, w=4); chev(d, GX1 - 14, yy, 0, A(PURPLE, 0.9), L=16, w=4)
    # khung day (nhin chinh dien, quay quanh truc dung): be rong = 150.|cos theta|
    hw = 75 * abs(math.cos(theta)); hh = 58
    front = math.cos(theta) >= 0
    col = COP if front else COP_D
    if hw > 3:
        for k in range(3):
            g = k * 7
            d.rectangle([CXC - max(0, hw - g), CYC - hh + g, CXC + max(0, hw - g), CYC + hh - g], outline=col, width=5)
    else:
        d.line([(CXC, CYC - hh), (CXC, CYC + hh)], fill=col, width=9)
    d.line([(CXC, CYC - hh), (CXC, CYC - 60)], fill=NAVY, width=6)
    if n_lab:
        text(d, (280, 790), n_lab, 56, BLUE)
    if slow:
        text(d, (280, 852), "hình quay chậm", 56, NOTE, bold=False)
    # day ra: hai vanh truot tren truc -> hai day sang dao dong ky
    for yy in (372, 404):
        d.line([(CXC + 14, yy), (575, yy)], fill=GRAY, width=6)
        d.rounded_rectangle([CXC - 16, yy - 9, CXC + 16, yy + 9], radius=6, fill=(214, 140, 60), outline=NAVY, width=3)

# ---------------- dao dong ki (khung tuy y) ----------------
PXV = 40                                  # 40 px moi volt, man +-5,25 V
def scope(d, box, traces, title=True, lab=None, marks=()):
    """box: o man (x0,y0,x1,y1). traces: [(n, bien do, mau, w, he_so_ve)] ; ve U0.sin(2.pi.n.tau) tren cua so 0,5 s."""
    x0, y0, x1, y1 = box; yc = (y0 + y1) / 2
    d.rounded_rectangle([x0 - 10, y0 - 10, x1 + 10, y1 + 10], radius=14, fill=NAVY)
    for k in range(1, 10):
        x = x0 + (x1 - x0) * k / 10; d.line([(x, y0), (x, y1)], fill=(52, 62, 96), width=2)
    for k in range(-5, 6):
        y = yc - k * PXV; d.line([(x0, y), (x1, y)], fill=(52, 62, 96) if k else (90, 100, 140), width=2)
    for n, amp, col, w, kd in traces:
        if kd <= 0: continue
        m = int(300 * kd)
        pts = [(x0 + (x1 - x0) * j / 300, yc - PXV * amp * math.sin(2 * math.pi * n * 0.5 * j / 300)) for j in range(m + 1)]
        if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")
    for amp, col in marks:
        y = yc - PXV * amp; x = x0
        while x < x1:
            d.line([(x, y), (min(x + 14, x1), y)], fill=col, width=3); x += 24

def scope_card(d, traces, lab=None, marks=()):
    card(d, (560, 250, 1040, 890), fill=WHITE, outline=LIGHT, w=3)
    text(d, (800, 296), "Dao động kí", 56, NOTE, bold=False)
    scope(d, (600, 350, 1010, 770), traces, marks=marks)
    if lab: text(d, (800, 836), lab, 56, ORANGE)

# ---------------- bang so lieu ----------------
def table(d, nrows, ratio=0.0, hl=None, y0=940):
    cols = (300, 780) if ratio <= 0 else (190, 470, 820)
    card(d, (40, y0, 1040, y0 + 120 + 5 * 76), fill=WHITE, outline=LIGHT, w=3)
    hd = ["n (vòng/s)", "U₀ (V)", "U₀/n (V·s)"]
    for j, cx in enumerate(cols):
        text(d, (cx, y0 + 55), hd[j], 56, NAVY, alpha=1.0 if j < 2 else ratio)
    d.line([(70, y0 + 98), (1010, y0 + 98)], fill=NAVY, width=3)
    for i in range(nrows):
        y = y0 + 140 + i * 76
        if hl is not None and ROWS[i][0] in hl:
            d.rounded_rectangle([60, y - 34, 1020, y + 34], radius=14, fill=(255, 237, 213))
        vals = (str(ROWS[i][0]), ROWS[i][1], ROWS[i][2])
        for j, cx in enumerate(cols):
            text(d, (cx, y), vals[j], 56, INK if j < 2 else DGREEN, alpha=1.0 if j < 2 else ratio)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    generator(d, 2 * math.pi * 0.32 * t, None)
    scope_card(d, [(4, U0[4], SCR, 5, 1.0)], "U₀ = 1,82 V", marks=((U0[4], ORANGE),))
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 185), "Quay nhanh gấp đôi: 8 vòng/s.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "Biên độ U₀ thế nào?", 58, INK, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 380, 970, y0 + 500], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 380, 110 + 860 * (1 - p), y0 + 500], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
STEP = 1.5
def stages(sc): s0 = sc["M"][0] + 1.0; return [s0 + i * STEP for i in range(5)]

def do_state(t, sc):
    st = stages(sc); k = sum(1 for s in st if t >= s); th = 0.0
    for i, s in enumerate(st):
        e = st[i + 1] if i + 1 < len(st) else 1e9
        if t > s: th += 2 * math.pi * 0.08 * ROWS[i][0] * (min(t, e) - s)
    return k, (ROWS[k - 1][0] if k else None), th

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    k, n, th = do_state(t, sc)
    generator(d, th, f"n = {n if n else 0} vòng/s", slow=True)
    if n: scope_card(d, [(n, U0[n], SCR, 5, 1.0)], f"U₀ = {ROWS[k - 1][1]} V", marks=((U0[n], ORANGE),))
    else:
        scope_card(d, [])
        d.line([(600, 560), (1010, 560)], fill=SCR, width=5)
    table(d, k, hl=[n] if n else None)
    text(d, (1030, 1490), "số liệu minh hoạ", 56, NAVY, anchor="rm")

# ---------------- canh 3: Dap an + rut ra ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    s = "ĐÁP ÁN: gấp đôi"; pw = tw(d, s, F(56)) + 70                  # hien ngay tu 0 s
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 340), fill=GREEN, r=39)
    text(d, (W / 2, 301), s, 56, WHITE)
    card(d, (40, 370, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    scope(d, (80, 410, 1000, 840), [(4, U0[4], (90, 140, 120), 4, 1.0), (8, U0[8], SCR, 6, ease((t - 0.2) / 0.8))],
          marks=((U0[4], (150, 160, 190)), (U0[8], ORANGE)))
    text(d, (300, 905), "4 vòng/s: 1,82 V", 56, (70, 120, 100))
    text(d, (780, 905), "8 vòng/s: 3,67 V", 56, DGREEN)
    r = appear(t, M[1] - 0.1, 0.5)
    if r > 0:
        table(d, 5, ratio=r, hl=[4, 8], y0=990)
        text(d, (W / 2, 1550), "U₀ tỉ lệ với n;  f = n (Hz)", 60, BLUE, alpha=appear(t, M[1] + 2.2, 0.4))

# ---------------- canh 4: Bay ----------------
def mini(d, x0, amp, ok, a=1.0):
    y0, y1 = 760, 1160; yc = (y0 + y1) / 2
    d.rounded_rectangle([x0, y0, x0 + 440, y1], radius=14, fill=A(NAVY, a))
    for k in (-4, -2, 2, 4): d.line([(x0 + 10, yc - k * 40), (x0 + 430, yc - k * 40)], fill=A((52, 62, 96), a), width=2)
    d.line([(x0 + 10, yc), (x0 + 430, yc)], fill=A((90, 100, 140), a), width=2)
    for am, cyc, col, w in ((1.82, 2, (90, 140, 120), 4), (amp, 4, SCR, 6)):
        pts = [(x0 + 15 + 410 * j / 240, yc - 40 * am * math.sin(2 * math.pi * cyc * j / 240)) for j in range(241)]
        d.line(pts, fill=A(col, a), width=w, joint="curve")
    cx = x0 + 220
    if ok: d.line([(cx - 30, 1225), (cx - 8, 1250), (cx + 34, 1195)], fill=A(GREEN, a), width=10, joint="curve")
    else:
        d.line([(cx - 26, 1196), (cx + 26, 1248)], fill=A(RED, a), width=10)
        d.line([(cx + 26, 1196), (cx - 26, 1248)], fill=A(RED, a), width=10)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k2, k3 = appear(t, b2, 0.4), appear(t, b3, 0.4)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 260, W / 2 + pw / 2, 336), fill=RED, r=38)
    text(d, (W / 2, 298), "BẪY", 56, WHITE)
    text(d, (W / 2, 420), "Quay 4 → 8 vòng/s:", 64, INK)
    text(d, (W / 2, 515), "sóng chỉ dày hơn?", 64, RED)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1030 - pw2, 260, 1030, 336), fill=A((127, 29, 29), k3), r=38)
        text(d, (1030 - pw2 / 2, 298), "SAI", 56, WHITE, alpha=k3)
    card(d, (40, 590, 520, 1290), outline=RED, w=4)
    text(d, (280, 670), "nghĩ", 60, RED)
    mini(d, 60, 1.82, False)
    card(d, (560, 590, 1040, 1290), fill=A(WHITE, k2), outline=A(GREEN, k2), w=4)
    if k2 > 0:
        text(d, (800, 670), "đo được", 60, DGREEN, alpha=k2)
        mini(d, 580, 3.67, True, a=k2)
    if k3 > 0:
        card(d, (40, 1330, 1040, 1520), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1425), "Cao và dày gấp đôi", 64, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1100), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Dạng sin chính xác?", "• Giá trị hiệu dụng?")):
        text(d, (100, 560 + j * 260), s, 66, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 700), "?", 200, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot cua khung; dap an KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Màn đo được U₀ = 2,35 V.", 60, INK, alpha=k)
    text(d, (W / 2, 540), "Máy quay mấy vòng/s?", 60, DARK_OR, alpha=k)
    scope(d, (150, 640, 930, 1120), [(5, U0[5], SCR, 6, 1.0)], marks=((U0[5], ORANGE),))
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1230, 990, 1380), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1305), "Gợi ý: U₀/n ≈ 0,47 V·s", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s in stages(do)]
            + [(an["t0"] + 0.1, "ding"), (an["t0"] + an["M"][1] - 0.1, "tap"),
               (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-xoaychieu-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Máy phát mini quay tay", draw=s_hook, tail=0.3, caps=[
   ("Đang quay 4 vòng/s.", 3.0),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đếm vòng, đọc biên độ.", 3.6),
   ("Tăng dần 2 đến 10 vòng/s.", 4.6)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Gấp đôi tốc độ, gấp đôi biên độ.", 3.8),
   ("U₀/n gần như không đổi.", 3.6)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("So với màn đo được.", 3.0),
   ("Biên độ cũng gấp đôi.", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Chưa trả lời được:", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.6)]),
])
