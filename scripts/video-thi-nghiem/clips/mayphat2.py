# Clip: tn-l12-mayphatdien-02 - Ba cuon day lech 120 do quanh MOT nam cham quay (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-mayphatdien-02.json:
#   tham_so: U0 = 6 V moi pha, lech_pha 120 do, f_quay mac dinh 1 vong/s (p = 1 -> f = 1 Hz, T = 1 s), f_quay toi da 3.
#   so_lieu_mau (6 hang): t = 0 ; 0,083 ; 0,167 ; 0,25 ; 0,333 ; 0,417 s va u1, u2, u3 ; tong ba cot = 0 (ghi_chu cua kho).
#   mo_hinh: u1 = U0.cos(2.pi.f.t), u2 = U0.cos(2.pi.f.t - 2.pi/3), u3 = U0.cos(2.pi.f.t + 2.pi/3).
# Du doan (khung ben canh, K10: mp4 khong ve nut A-D): nam cham quay deu, ba den chop the nao?
#   A. Ca ba cung luc   B. Lan luot, cach nhau 1/3 chu ki (dung)   C. Lan luot, cach nhau 1/4 chu ki (lech 90 do)
#   D. Ba nhip nhanh cham khac nhau (khac tan so)  -> hien_tuong_hay_sai #1, #2.
#   Khong trung Cau 3 trong bai (hoi dac diem ba suat dien dong). Khac mayphat1 (f = n.p) va mayphat3 (bien ap).
# Chot (ca moi chua hien): quay 2 vong/s -> f = 2 Hz, T = 0,5 s, den 2 sang sau den 1 la T/3 = 1/6 s ~ 0,17 s.
# Vat li: tu thong qua cuon k ~ cos(phi - theta_k) -> e_k = -dPhi/dt ~ sin(phi - theta_k). Dat phi = theta_1 + 90 + 360.f.t
#   -> u1 = 6.cos(2.pi.t), u2 = 6.cos(2.pi.t - 120), u3 = 6.cos(2.pi.t + 120) dung mo_hinh (cuon 2 lech +120 do theo chieu quay).
#   LED chi sang khi u_k > U0/2 (nguong) -> khong bao gio hai den sang cung luc (quan_sat cua kho).
# Nam cham thang: port PIL tu bar_magnet trong .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py, xoay duoc.
# Duong suc: lan theo truong hai cuc (ra o N, vao o S, khong cat nhau), mui chevron.
from engine import *

U0 = 6.0
ROWS = [("0", "6,0", "−3,0", "−3,0"), ("0,083", "5,2", "0,0", "−5,2"), ("0,167", "3,0", "3,0", "−6,0"),
        ("0,25", "0,0", "5,2", "−5,2"), ("0,333", "−3,0", "6,0", "−3,0"), ("0,417", "−5,2", "5,2", "0,0")]
assert all(abs(sum(float(v.replace(",", ".").replace("−", "-")) for v in r[1:])) < 1e-9 for r in ROWS)
PH = (ORANGE, TEAL, PURPLE)                    # mau pha 1, 2, 3
NOTE = (70, 75, 95)
COP, COP_D = (196, 120, 52), (130, 72, 28)
TH = (-90.0, 30.0, 150.0)                      # goc dat cuon 1, 2, 3 tren man (do, chieu kim dong ho, -90 = dinh)

def u_k(k, ts): return U0 * math.cos(2 * math.pi * ts - 2 * math.pi * k / 3)          # ts: thoi gian mo phong (s), f = 1 Hz
def phi_deg(ts): return TH[0] + 90 + 360 * ts                                          # huong cuc N
assert abs(math.sin(math.radians(phi_deg(0.2) - TH[1])) * U0 - u_k(1, 0.2)) < 1e-9     # e_k ~ sin(phi - theta_k)

def chev(d, x, y, ang, color, L=16, w=4):
    for s in (1, -1):
        a = ang + math.pi - s * math.radians(30)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=color, width=w)

# ---------------- nam cham thang chuan (port PIL tu bar_magnet / svg_lib.py), xoay goc ang ----------------
UM_EDGE = (51, 65, 85)
UM_N = ((220, 38, 38), (248, 113, 113), (185, 28, 28))
UM_S = ((37, 99, 235), (96, 165, 250), (30, 64, 175))

def bar_magnet_pil(d, cx, cy, L, H, ang=0.0, dep=(10, -7), fs=44, sw=4):
    """Tam (cx, cy), dai L, cao H; ang (do): huong cuc N tren man (0 = sang phai, duong = chieu kim dong ho).
    Mat sau doi dep; cac mat ben thay duoc (phap tuyen cung huong dep) to mau mat tren/mat ben nhu ban SVG."""
    r = math.radians(ang); ca, sa = math.cos(r), math.sin(r); dx, dy = dep
    P = lambda u, v: (cx + u * ca - v * sa, cy + u * sa + v * ca)
    h, l = H / 2, L / 2
    edges = [((0, -h), (l, -h), UM_N, (0, -1)), ((-l, -h), (0, -h), UM_S, (0, -1)),
             ((0, h), (l, h), UM_N, (0, 1)), ((-l, h), (0, h), UM_S, (0, 1)),
             ((l, -h), (l, h), UM_N, (1, 0)), ((-l, -h), (-l, h), UM_S, (-1, 0))]
    for a, b, pal, (nu, nv) in edges:
        nx, ny = nu * ca - nv * sa, nu * sa + nv * ca
        if nx * dx + ny * dy <= 0: continue
        pa, pb = P(*a), P(*b)
        col = pal[1] if -ny > 0.5 else pal[2]
        d.polygon([pa, pb, (pb[0] + dx, pb[1] + dy), (pa[0] + dx, pa[1] + dy)], fill=col, outline=UM_EDGE, width=sw)
    d.polygon([P(0, -h), P(l, -h), P(l, h), P(0, h)], fill=UM_N[0], outline=UM_EDGE, width=sw)
    d.polygon([P(-l, -h), P(0, -h), P(0, h), P(-l, h)], fill=UM_S[0], outline=UM_EDGE, width=sw)
    text(d, P(l / 2, 0), "N", fs, WHITE); text(d, P(-l / 2, 0), "S", fs, WHITE)

# ---------------- duong suc cua nam cham thang (toa do rieng: N o +u) ----------------
ML, MHH = 230, 62
def _trace(ang):
    a = ML / 2 - 14; nx, sx = a, -a
    x, y = nx + 6 * math.cos(ang), -6 * math.sin(ang); pts = [(x, y)]
    for _ in range(3000):
        ex = ey = 0.0
        for px, q in ((nx, 1), (sx, -1)):
            ddx, ddy = x - px, y; r3 = (ddx * ddx + ddy * ddy) ** 1.5; ex += q * ddx / r3; ey += q * ddy / r3
        n = math.hypot(ex, ey); x += 3 * ex / n; y += 3 * ey / n; pts.append((x, y))
        if math.hypot(x - sx, y) < 8: break
    return pts
FIELD = [_trace(math.radians(a)) for a in (96, 135)]   # dinh duong ngoai ~157 px < mat trong cuon day (175 px): khong ra ngoai stato

def field(d, cx, cy, ang, a=1.0):
    r = math.radians(ang); ca, sa = math.cos(r), math.sin(r); c = A(PURPLE, 0.5 * a)
    for ln in FIELD:
        for sg in (1, -1):
            pts = [(cx + u * ca - sg * v * sa, cy + u * sa + sg * v * ca) for u, v in ln]
            d.line(pts, fill=c, width=4, joint="curve")
            k = max(range(len(ln)), key=lambda n: abs(ln[n][1]))                  # dinh cung: chevron chi N -> S
            (x0, y0), (x1, y1) = pts[max(0, k - 3)], pts[min(len(pts) - 1, k + 3)]
            chev(d, pts[k][0], pts[k][1], math.atan2(y1 - y0, x1 - x0), A(PURPLE, 0.8 * a))

# ---------------- stato: vong nhua + ba cuon day ----------------
RCX, RCY, RR = 390, 590, 205
def coil(d, k):
    th = math.radians(TH[k]); ux, uy = math.cos(th), math.sin(th); tx, ty = -uy, ux
    cx, cy = RCX + RR * ux, RCY + RR * uy
    Q = lambda s, h: (cx + s * tx + h * ux, cy + s * ty + h * uy)        # s doc tiep tuyen, h theo ban kinh
    d.polygon([Q(-62, -30), Q(62, -30), Q(62, 30), Q(-62, 30)], fill=COP, outline=NAVY, width=4)
    for s in range(-50, 56, 13):
        d.line([Q(s, -30), Q(s + 6, 30)], fill=COP_D, width=3)
    bx, by = RCX + (RR + 78) * ux, RCY + (RR + 78) * uy
    dot(d, bx, by, 30, PH[k], outline=WHITE)
    text(d, (bx, by), str(k + 1), 44, WHITE)

def stator(d, show120=False):
    d.ellipse([RCX - RR - 14, RCY - RR - 14, RCX + RR + 14, RCY + RR + 14], outline=(203, 213, 225), width=28)
    d.ellipse([RCX - RR - 14, RCY - RR - 14, RCX + RR + 14, RCY + RR + 14], outline=NAVY, width=3)
    d.ellipse([RCX - RR + 14, RCY - RR + 14, RCX + RR - 14, RCY + RR - 14], outline=NAVY, width=3)
    if show120:
        r = RR + 36
        d.arc([RCX - r, RCY - r, RCX + r, RCY + r], TH[0] + 14, TH[1] - 14, fill=NAVY, width=4)
        a = math.radians(-30); text(d, (RCX + (RR + 100) * math.cos(a), RCY + (RR + 100) * math.sin(a)), "120°", 46, NAVY)

def leds(d, lit):
    text(d, (880, 300), "Ba đèn", 44, NOTE, bold=False)
    for k in range(3):
        y = 420 + k * 170
        b = lit[k]
        if b > 0:
            for j in range(6, 0, -1): dot(d, 900, y, 40 + j * 11, A((250, 204, 21), 0.09 * b))
        dot(d, 900, y, 44, mix((235, 235, 235), (255, 236, 140), b), outline=NAVY)
        dot(d, 790, y, 30, PH[k], outline=WHITE); text(d, (790, y), str(k + 1), 44, WHITE)

def led_lit(ts): return [clamp((u_k(k, ts) / U0 - 0.5) / 0.5) for k in range(3)]

def rig(d, ts, lit, show120=False, spin_arrow=False):
    card(d, (40, 250, 1040, 880), fill=WHITE, outline=LIGHT, w=3)
    ang = phi_deg(ts)
    field(d, RCX, RCY, ang)
    stator(d, show120)
    for k in range(3): coil(d, k)
    bar_magnet_pil(d, RCX, RCY, ML, MHH, ang)
    dot(d, RCX, RCY, 9, NAVY)
    if spin_arrow:                                     # chieu quay: cung kim dong ho
        r = 150; d.arc([RCX - r, RCY - r, RCX + r, RCY + r], -130, -60, fill=ORANGE, width=8)
        a = math.radians(-60); chev(d, RCX + r * math.cos(a), RCY + r * math.sin(a), a + math.pi / 2, ORANGE, L=26, w=8)
    leds(d, lit)

# ---------------- do thi ba suat dien dong ----------------
GX0, GX1 = 170, 990
def graph(d, y0, y1, kx, cursor=None, ticks=False, peaks=0.0, a=1.0):
    yc, s = (y0 + y1) / 2, ((y1 - y0) / 2 - 20) / U0
    X = lambda ts: GX0 + (GX1 - GX0) * ts
    for v in (6, -6):
        d.line([(GX0, yc - s * v), (GX1, yc - s * v)], fill=A((236, 232, 222), a), width=2)
        text(d, (GX0 - 16, yc - s * v), "6" if v > 0 else "−6", 44, MUTED, bold=False, anchor="rm", alpha=a)
    d.line([(GX0, yc), (GX1 + 22, yc)], fill=A(NAVY, a), width=4)
    d.line([(GX0, y1), (GX0, y0)], fill=A(NAVY, a), width=4)
    text(d, (GX0 + 14, y0 - 22), "e (V)", 44, INK, anchor="lm", alpha=a)
    text(d, (GX0 - 16, yc), "0", 44, MUTED, bold=False, anchor="rm", alpha=a)
    if ticks:
        for j, lab in ((1, "T/3"), (2, "2T/3"), (3, "T")):
            x = X(j / 3); d.line([(x, yc - 10), (x, yc + 10)], fill=A(NAVY, a), width=4)
            text(d, (x, yc + 42), lab, 44, INK, alpha=a)
    else:
        text(d, (GX1, yc + 42), "1 s", 44, MUTED, bold=False, alpha=a)
    m = int(240 * clamp(kx))
    for k in range(3):
        if m > 1:
            pts = [(X(j / 240), yc - s * u_k(k, j / 240)) for j in range(m + 1)]
            d.line(pts, fill=A(PH[k], a), width=6, joint="curve")
        if peaks > 0:
            x = X(k / 3); dot(d, x, yc - s * U0, 14, A(PH[k], peaks * a), outline=A(WHITE, peaks * a))
            yy = y0 + 8
            while yy < yc:
                d.line([(x, yy), (x, min(yy + 12, yc))], fill=A(PH[k], peaks * a), width=3); yy += 22
    if cursor is not None:
        d.line([(X(cursor), y0), (X(cursor), y1)], fill=A(NAVY, 0.6 * a), width=3)

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    rig(d, 0.0, [0, 0, 0], show120=True, spin_arrow=True)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 930 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(44)) + 56
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, a), r=34)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", 44, WHITE, alpha=a)
    text(d, (W / 2, y0 + 190), "Nam châm quay đều.", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "Ba đèn chớp thế nào?", 50, INK, alpha=a)
    tc, te = M[1] + 0.4, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (te - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 416], radius=8, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 416], radius=8, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
SLOW = 0.4                                     # chieu cham: 1 s that -> 2,5 s tren man
def ts_do(t): return max(0.0, (t - 0.6) * SLOW)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    ts = ts_do(t)
    rig(d, ts, led_lit(ts) if t > 0.6 else [0, 0, 0])
    text(d, (150, 840), "chiếu chậm", 44, NOTE, bold=False)
    card(d, (40, 910, 1040, 1420), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 945), "Dao động ký ba kênh", 44, NOTE, bold=False)
    graph(d, 1030, 1395, ts, cursor=(ts % 1.0) if ts > 0 else None)
    text(d, (W / 2, 1490), "Mỗi vòng quay = 1 chu kì", 48, BLUE, alpha=appear(t, sc["M"][1] + 0.3))

# ---------------- canh 3: dap an + tong bang 0 + chua noi duoc ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    b = appear(t, 0.2)
    pw = tw(d, "ĐÁP ÁN · cách nhau 1/3 chu kì", F(48)) + 70
    card(d, (W / 2 - pw / 2, 255, W / 2 + pw / 2, 335), fill=A((220, 252, 231), b), outline=A(GREEN, b), r=40, w=4)
    text(d, (W / 2, 295), "ĐÁP ÁN · cách nhau 1/3 chu kì", 48, GREEN, alpha=b)
    card(d, (40, 360, 1040, 830), fill=WHITE, outline=LIGHT, w=3)
    graph(d, 428, 760, 1.0, ticks=True, peaks=appear(t, 0.8))
    text(d, (W / 2, 795), "cùng biên độ 6 V · cùng chu kì T", 44, INK, alpha=appear(t, M[0] + 1.6))
    r = appear(t, M[1] - 0.1) * (1 - appear(t, M[2] - 0.1, 0.3))
    if r > 0:
        card(d, (40, 860, 1040, 1590), fill=A(WHITE, r), outline=A(LIGHT, r), w=3)
        cols = (170, 380, 590, 800, 950)
        for cx, h, col in zip(cols, ("t (s)", "e1", "e2", "e3", "tổng"), (NAVY,) + PH + (GREEN,)):
            text(d, (cx, 915), h, 48, col, alpha=r)
        d.line([(70, 955), (1010, 955)], fill=A(NAVY, r), width=3)
        for i, row in enumerate(ROWS):
            y = 1000 + i * 82; ai = r * appear(t, M[1] + 0.15 * i, 0.3)
            for j, v in enumerate(row): text(d, (cols[j], y), v, 46, INK, alpha=ai)
            text(d, (cols[4], y), "0", 46, GREEN, alpha=r * appear(t, M[1] + 1.4 + 0.12 * i, 0.3))
        text(d, (W / 2, 1520), "e1 + e2 + e3 = 0 mọi lúc", 48, GREEN, alpha=r * appear(t, M[1] + 2.4))
    c = appear(t, M[2] - 0.1)
    if c > 0:
        card(d, (40, 860, 1040, 1300), fill=A(WHITE, c), outline=A(NAVY, c), w=5)
        text(d, (W / 2, 940), "Chưa nói được gì?", 50, NAVY, alpha=c)
        for j, s in enumerate(("Nối hình sao hay tam giác?", "Biên độ chính xác bao nhiêu?")):
            y = 1060 + j * 120
            dot(d, 110, y, 10, A(NAVY, c)); text(d, (140, y), s, 46, INK, anchor="lm", alpha=c)

# ---------------- canh 4: ba bay ----------------
def icon(d, i, cx, cy, a):
    """Hinh nho canh moi y dung (hien cung dau tich): stato 120 do / mot nam cham / ba song cung tan so."""
    if a <= 0.02: return
    if i == 0:
        d.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], outline=A(NAVY, a), width=4)
        for k in range(3):
            th = math.radians(TH[k]); dot(d, cx + 80 * math.cos(th), cy + 80 * math.sin(th), 16, A(PH[k], a), outline=A(WHITE, a))
    elif i == 1:
        if a > 0.95: bar_magnet_pil(d, cx, cy, 190, 60, 0, fs=44)
    else:
        for k in range(3):
            pts = [(cx - 120 + j * 2, cy - 55 * math.cos(2 * math.pi * j / 120 - 2 * math.pi * k / 3)) for j in range(121)]
            d.line(pts, fill=A(PH[k], a), width=5, joint="curve")

TRAPS = (("Lệch 90° hay 180°", "Lệch 120° trên stato"), ("Ba nam châm", "Một nam châm quay"),
         ("Ba tần số khác nhau", "Cùng tần số"))
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (40, 250, 1040, 1590), fill=WHITE, outline=RED, w=4)
    for i, (sai, dung) in enumerate(TRAPS):
        y = 330 + i * 400
        x, yy = 110, y
        d.line([(x - 22, yy - 22), (x + 22, yy + 22)], fill=RED, width=9); d.line([(x + 22, yy - 22), (x - 22, yy + 22)], fill=RED, width=9)
        text(d, (160, yy), sai, 48, RED, anchor="lm")
        a = appear(t, M[1] + 0.3 + 0.7 * i)
        yy = y + 110
        d.line([(x - 24, yy), (x - 6, yy + 20), (x + 26, yy - 22)], fill=A(GREEN, a), width=9, joint="curve")
        text(d, (160, yy), dung, 48, GREEN, anchor="lm", alpha=a)
        icon(d, i, 850, y + 55, a)
        if i < 2: d.line([(80, y + 220), (1000, y + 220)], fill=LIGHT, width=3)
    a = appear(t, M[1] + 2.6)
    text(d, (W / 2, 1490), "Chỉ khác pha", 50, BLUE, alpha=a)

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
    chot_hoi_gon(d, t, sc, "Ba e cùng tần số, cùng biên độ,\nlệch nhau T/3",
                 "Quay 2 vòng/s: tần số? Đèn 2 sáng sau đèn 1 bao lâu?",
                 "Mỗi vòng quay là mấy chu kì?", tre=2.8)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + 0.6, "tap"),
            (an["t0"] + 0.2, "ding"), (an["t0"] + an["M"][1], "tap"), (an["t0"] + an["M"][2] - 0.1, "tap"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-mayphatdien-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Máy phát điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ba cuộn dây, một nam châm", draw=s_hook, tail=0.3, caps=[
   ("Mỗi cuộn nối một đèn.", 2.9),
   ("Chọn đáp án ở khung câu hỏi.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Quay nam châm khoảng 1 vòng/s.", 3.6),
   ("Nhìn thứ tự sáng của ba đèn.", 4.6)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.5, caps=[
   ("Đỉnh sau chậm hơn đỉnh trước.", 3.6),
   ("Cộng ba giá trị ở mỗi lúc.", 4.4),
   ("Giới hạn của thí nghiệm.", 3.6)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Ba ý sai hay gặp.", 3.4),
   ("Sửa lại từng ý.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.9, caps=[
   ("Dừng video và trả lời.", 7.4)]),
])
