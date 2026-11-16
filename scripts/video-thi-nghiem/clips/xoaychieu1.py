# Clip: tn-l12-xoaychieu-01 - May phat mini quay tay: bien do U0 theo toc do quay (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-xoaychieu-01.json:
#   so_lieu_mau: n = 2, 4, 6, 8, 10 vong/s -> U0 = 0,95 ; 1,82 ; 2,84 ; 3,67 ; 4,70 V ; U0/n = 0,475 ; 0,455 ; 0,473 ; 0,459 ; 0,470
#   ket_qua_ky_vong: U0/n ~ 0,47 V.s ; rut_ra: f = n (moi vong mot chu ki). tham_so: n toi da 12 vong/s.
# Du doan (khung ben canh, K10: mp4 khong ve nut A-D): dang quay 4 vong/s, quay 8 vong/s thi bien do U0 tren man the nao?
#   A. Khong doi, song chi day hon (hien_tuong_hay_sai #1)   B. Gap doi, song day gap doi (dung: 1,82 -> 3,67 V)
#   C. Gap bon (nham binh phuong)                           D. Giam mot nua (nham voi chu ki)
#   Khong trung Cau 1 trong bai (2 -> 6 vong/s, hoi ca U0 va f).
# Chot (cong B 14/11: hoi nguoc, khong doc thang tu hop chot): U0 = 2,35 V -> n ~ 2,35 / 0,47 = 5 vong/s (mo hinh U0 ~ 0,47.n cua ket_qua_ky_vong; 5 trong khoang 2-12).
# Nam cham chu U: port PIL tu u_magnet trong .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py (thay chot).
# Duong suc giua hai cuc: song song cach deu, tu N (trai) sang S (phai), mui chevron.
from engine import *

ROWS = [(2, "0,95", "0,475"), (4, "1,82", "0,455"), (6, "2,84", "0,473"), (8, "3,67", "0,459"), (10, "4,70", "0,470")]
U0 = {2: 0.95, 4: 1.82, 6: 2.84, 8: 3.67, 10: 4.70}
SCR = (134, 239, 172)
NOTE = (70, 75, 95)
COP, COP_D = (196, 120, 52), (130, 72, 28)

# ---------------- chu co chi so duoi (chi so >= 36 px) ----------------
def rich2(d, x, y, s, size, color=INK, anchor="m", alpha=1.0, bold=True):
    """'U_{0} = 1,82 V': chi so duoi ve bang co max(36, 0,72*size), ha xuong 0,3*size."""
    segs = []
    for p in [p for p in re.split(r"(_\{[^}]*\})", s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], max(36, int(size * 0.72)), size * 0.3))
        else: segs.append((p, size, 0))
    tot = sum(tw(d, t, F(sz, bold)) for t, sz, _ in segs)
    xx = x - tot / 2 if anchor == "m" else (x - tot if anchor == "r" else x)
    for t, sz, dy in segs:
        dtext(d, (xx, y + dy), t, F(sz, bold), color, alpha, "lm"); xx += tw(d, t, F(sz, bold))

def chev(d, x, y, ang, color, L=18, w=5):
    for s in (1, -1):
        a = ang + math.pi - s * math.radians(30)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=color, width=w)

def dashed_h(d, y, x0, x1, color, w=4, dash=16, gap=10):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=color, width=w); x += dash + gap

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

def u_magnet_pil(d, x, y, w, h, arm, yoke, tip, dep=(18, -12), fs=48, sw=4):
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

def generator(d, theta, n_lab):
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
        text(d, (280, 800), n_lab, 50, BLUE)
        text(d, (280, 856), "hình quay chậm", 44, NOTE, bold=False)
    else:
        text(d, (280, 820), "máy phát mini", 44, NOTE, bold=False)
    # day ra: hai vanh truot tren truc -> hai day sang dao dong ky
    for yy in (372, 404):
        d.line([(CXC + 14, yy), (575, yy)], fill=GRAY, width=6)
        d.rounded_rectangle([CXC - 16, yy - 9, CXC + 16, yy + 9], radius=6, fill=(214, 140, 60), outline=NAVY, width=3)

# ---------------- dao dong ky ----------------
SX0, SX1, SY0, SY1 = 600, 1010, 340, 760
SYC, PXV = (SY0 + SY1) / 2, 40          # 40 px moi volt, man +-5,25 V

def scope(d, traces, lab=None, lab_col=ORANGE):
    """traces: [(n, mau, w, he_so_ve 0..1)] ; ve song U0(n).sin(2.pi.n.tau) tren cua so 0,5 s."""
    card(d, (560, 250, 1040, 890), fill=WHITE, outline=LIGHT, w=3)
    text(d, (800, 300), "Dao động ký", 44, NOTE, bold=False)
    d.rounded_rectangle([SX0 - 10, SY0 - 10, SX1 + 10, SY1 + 10], radius=14, fill=NAVY)
    for k in range(1, 10):
        x = SX0 + (SX1 - SX0) * k / 10; d.line([(x, SY0), (x, SY1)], fill=(52, 62, 96), width=2)
    for k in range(-5, 6):
        y = SYC - k * PXV; d.line([(SX0, y), (SX1, y)], fill=(52, 62, 96) if k else (90, 100, 140), width=2)
    for n, col, w, kd in traces:
        if kd <= 0: continue
        m = int(300 * kd); pts = []
        for j in range(m + 1):
            tau = 0.5 * j / 300
            pts.append((SX0 + (SX1 - SX0) * j / 300, SYC - PXV * U0[n] * math.sin(2 * math.pi * n * tau)))
        if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")
    if lab: rich2(d, 800, 830, lab, 48, lab_col)

def peak_mark(d, n, col, a=1.0):
    y = SYC - PXV * U0[n]
    x = SX0
    while x < SX1:
        d.line([(x, y), (min(x + 14, SX1), y)], fill=A(col, a), width=3); x += 24

# ---------------- bang so lieu ----------------
TY0 = 940
def table(d, nrows, ratio=0.0, a=1.0, hl=None, y0=TY0):
    cols = (300, 780) if ratio <= 0 else (230, 540, 850)
    card(d, (60, y0, 1020, y0 + 120 + 5 * 76), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    hd = ["n (vòng/s)", "U_{0} (V)", "U_{0}/n"]
    for j, cx in enumerate(cols):
        al = a if j < 2 else a * ratio
        rich2(d, cx, y0 + 55, hd[j], 46, NAVY, alpha=al)
    d.line([(90, y0 + 98), (990, y0 + 98)], fill=A(NAVY, a), width=3)
    for i in range(nrows):
        y = y0 + 140 + i * 76
        if hl is not None and ROWS[i][0] in hl:
            d.rounded_rectangle([80, y - 34, 1000, y + 34], radius=14, fill=A((255, 237, 213), a))
        vals = (str(ROWS[i][0]), ROWS[i][1], ROWS[i][2])
        for j, cx in enumerate(cols):
            al = a if j < 2 else a * ratio
            text(d, (cx, y), vals[j], 46, INK if j < 2 else GREEN, alpha=al)

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    generator(d, 2 * math.pi * 0.32 * t, "n = 4 vòng/s")
    scope(d, [(4, SCR, 5, 1.0)], "U_{0} = 1,82 V")
    peak_mark(d, 4, ORANGE)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 940 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(44)) + 56
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, a), r=34)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", 44, WHITE, alpha=a)
    text(d, (W / 2, y0 + 175), "Quay nhanh gấp đôi: 8 vòng/s.", 48, INK, alpha=a)
    rich2(d, W / 2, y0 + 265, "Biên độ U_{0} trên màn thế nào?", 48, INK, alpha=a)
    tc, te = M[1] + 0.4, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (te - tc))
        d.rounded_rectangle([140, y0 + 452, 940, y0 + 468], radius=8, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 452, 140 + 800 * (1 - p), y0 + 468], radius=8, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
STEP = 1.5
def stages(sc): s0 = sc["M"][0] + 1.0; return [s0 + i * STEP for i in range(5)]

def do_state(t, sc):
    """(so hang da hien, n hien tai, goc khung) - mot ham cho ca may, man, bang (dong bo)."""
    st = stages(sc); k = sum(1 for s in st if t >= s); th = 0.0
    for i, s in enumerate(st):
        e = st[i + 1] if i + 1 < len(st) else 1e9
        if t > s: th += 2 * math.pi * 0.08 * ROWS[i][0] * (min(t, e) - s)
    return k, (ROWS[k - 1][0] if k else None), th

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    k, n, th = do_state(t, sc)
    generator(d, th, f"n = {n} vòng/s" if n else "n = 0")
    if n:
        scope(d, [(n, SCR, 5, 1.0)], "U_{0} = " + U0_TXT[n]); peak_mark(d, n, ORANGE)
    else:
        scope(d, [], None)
        d.line([(SX0, SYC), (SX1, SYC)], fill=SCR, width=5)
    table(d, k, hl=[n] if n else None)

U0_TXT = {r[0]: r[1] + " V" for r in ROWS}

# ---------------- canh 3: dap an + rut ra + chua noi duoc ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    generator(d, 2 * math.pi * 0.64 * t, "n = 8 vòng/s")
    scope(d, [(4, (90, 140, 120), 4, 1.0), (8, SCR, 6, ease((t - 0.3) / 0.8))])
    d.rectangle([570, 790, 1030, 880], fill=WHITE)
    if t > 1.1:
        peak_mark(d, 4, (150, 160, 190)); peak_mark(d, 8, ORANGE)
        text(d, (800, 835), "1,82 V → 3,67 V", 48, ORANGE)
    b = appear(t, 0.3)
    pw = tw(d, "ĐÁP ÁN · gấp đôi", F(48)) + 70
    card(d, (W / 2 - pw / 2, 905, W / 2 + pw / 2, 985), fill=A((220, 252, 231), b), outline=A(GREEN, b), r=40, w=4)
    text(d, (W / 2, 945), "ĐÁP ÁN · gấp đôi", 48, GREEN, alpha=b)
    r = appear(t, M[1] - 0.1, 0.6)
    table(d, 5, ratio=r, hl=[4, 8], y0=1010)
    if r > 0:
        rich2(d, W / 2, 1560, "U_{0} tỉ lệ với n  ·  f = n", 50, BLUE, alpha=appear(t, M[1] + 1.2))
    c = appear(t, M[2] - 0.1)
    if c > 0:
        card(d, (60, 1010, 1020, 1600), fill=A(WHITE, c), outline=A(NAVY, c), w=5)
        text(d, (W / 2, 1090), "Chưa nói được gì?", 50, NAVY, alpha=c)
        for j, s in enumerate(("Dạng sin có chính xác không", "Giá trị hiệu dụng bao nhiêu")):
            y = 1230 + j * 130
            dot(d, 130, y, 10, A(NAVY, c))
            text(d, (160, y), s, 46, INK, anchor="lm", alpha=c)

# ---------------- canh 4: bay ----------------
def mini_scope(d, x0, n_amp, cycles, ok, a_fig=1.0, a_mark=1.0):
    y0, y1 = 520, 900; yc = (y0 + y1) / 2
    d.rounded_rectangle([x0, y0, x0 + 440, y1], radius=14, fill=A(NAVY, a_fig))
    for k in (-2, -1, 1, 2): d.line([(x0 + 10, yc - k * 40), (x0 + 430, yc - k * 40)], fill=A((52, 62, 96), a_fig), width=2)
    d.line([(x0 + 10, yc), (x0 + 430, yc)], fill=A((90, 100, 140), a_fig), width=2)
    for amp, cyc, col, w in ((1.82, 2, (90, 140, 120), 4), (n_amp, cycles, SCR, 6)):
        pts = [(x0 + 15 + 410 * j / 240, yc - 40 * amp * math.sin(2 * math.pi * cyc * j / 240)) for j in range(241)]
        d.line(pts, fill=A(col, a_fig), width=w, joint="curve")
    cx = x0 + 220
    if ok:
        d.line([(cx - 30, 960), (cx - 8, 985), (cx + 34, 930)], fill=A(GREEN, a_mark), width=10, joint="curve")
    else:
        d.line([(cx - 26, 932), (cx + 26, 984)], fill=A(RED, a_mark), width=10)
        d.line([(cx + 26, 932), (cx - 26, 984)], fill=A(RED, a_mark), width=10)

def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Bẫy", 50, RED)
    text(d, (W / 2, 400), "Quay 4 → 8 vòng/s", 50, INK)
    card(d, (40, 450, 520, 1020), fill=WHITE, outline=RED, w=4)
    text(d, (280, 490), "Nghĩ sai", 46, RED)
    mini_scope(d, 60, 1.82, 4, False)
    a2 = appear(t, M[1] - 0.1)
    card(d, (560, 450, 1040, 1020), fill=A(WHITE, a2), outline=A(GREEN, a2), w=4)
    text(d, (800, 490), "Thật", 46, GREEN, alpha=a2)
    if a2 > 0: mini_scope(d, 580, 3.67, 4, True, a_fig=a2, a_mark=a2)
    text(d, (280, 1070), "chỉ dày hơn", 44, RED)
    text(d, (800, 1070), "cao và dày hơn", 44, GREEN, alpha=a2)
    a3 = appear(t, M[1] + 1.4)
    if a3 > 0:
        card(d, (60, 1140, 1020, 1400), fill=A((236, 253, 243), a3), outline=A(GREEN, a3), w=5)
        text(d, (W / 2, 1225), "Từ thông biến thiên nhanh hơn", 48, BLUE, alpha=a3)
        text(d, (W / 2, 1315), "→ suất điện động lớn hơn", 48, BLUE, alpha=a3)

# ---------------- canh 5: chot + cau hoi ----------------
# Chot + THU NGHI: nhu chot_hoi cua engine nhung hop cau hoi thu theo noi dung, goi y hien tre (cong B 14/11).
def chot_hoi_gon(d, t, sc, chot, hoi, goi_y=None, tre=2.5):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, chot, 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    hq = len(wrap(d, hoi, F(48), 880)) * 48 * 1.22
    y1 = int(760 + hq + 40)
    card(d, (40, 620, 1040, y1), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(44)) + 56
    card(d, (W / 2 - pw / 2, 646, W / 2 + pw / 2, 718), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 682), "THỬ NGHĨ", 44, WHITE, alpha=k1)
    ctext(d, 760 + hq / 2 - 10, hoi, 48, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    if goi_y:
        kh = appear(t, M[0] + tre, 0.5)
        if kh > 0:
            card(d, (110, y1 + 40, 970, y1 + 250), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
            text(d, (W / 2, y1 + 95), "Gợi ý", 44, MUTED, alpha=kh)
            ctext(d, y1 + 180, goi_y, 48, ORANGE, maxw=820, alpha=kh)

def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi_gon(d, t, sc, "Quay nhanh gấp k lần:\nbiên độ, tần số đều gấp k",
                 "Màn đo được U0 = 2,35 V. Máy đang quay khoảng mấy vòng/s?",
                 "Nhớ cột U0/n trong bảng", tre=2.8)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + s, "tap") for s in stages(do)]
    out += [(an["t0"] + 0.3, "ding"), (an["t0"] + an["M"][2] - 0.1, "tap"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-xoaychieu-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Máy phát mini quay tay", draw=s_hook, tail=0.3, caps=[
   ("Đang quay 4 vòng/s.", 2.5),
   ("Chọn đáp án ở khung câu hỏi.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đếm vòng, đọc biên độ trên màn.", 3.8),
   ("Tăng dần: 2 đến 10 vòng/s.", 5.2)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.5, caps=[
   ("Gấp đôi tốc độ, gấp đôi biên độ.", 3.7),
   ("Biên độ chia n gần như không đổi.", 3.8),
   ("Giới hạn của thí nghiệm.", 4.0)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Bẫy: chỉ tần số tăng?", 3.8),
   ("Biên độ cũng tăng theo n.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video và trả lời.", 7.4)]),
])
