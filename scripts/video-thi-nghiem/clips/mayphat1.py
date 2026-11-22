# Clip: tn-l12-mayphatdien-01 - May phat mini quay bang dong co: do tan so theo toc do quay de kiem f = np
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-mayphatdien-01.json (so_lieu_mau, tham_so):
#   n (vong/s) | f do (Hz) | f/n : 5 9,8 1,96 | 10 20,1 2,01 | 15 30,2 2,01 | 20 39,6 1,98 | 25 50,3 2,01 ; p = 2 cap cuc (ro-to 4 cuc).
# Ban 2 (21/11/2026, viec 4 lo 20, cong --do-chu moi):
#   Du doan (danh hien_tuong_hay_sai #1 f = n va #3 lay so cuc lam p): "ro-to 4 cuc, n = 10 vong/s, tan so ke chi may Hz?"
#     khung web hoi A. 5 Hz (n/p)  B. 10 Hz (f = n)  C. 20 Hz (dung, so do 20,1)  D. 40 Hz (p = 4) - clip khong ve nut (K10).
#     Khac Cau 2 cua bai (2 cap cuc, 1500 vong/phut -> 25/50/100/3000 Hz) va hinh Bay 2 cua bai (25 vong/s -> 25/50 Hz).
#   Bay (3 nhip ~3 s): "4 cuc nen p = 4?" (so cuc danh so 1-4) -> duong f = 4n lech xa so do -> ghep N-S thanh 2 cap, p = 2.
#   Chot THU NGHI: ro-to 6 cuc, 900 vong/phut -> f = ? (buoc moi: doi vong/phut ra vong/s; 15 x 3 = 45 Hz, khong hien tren man).
#   Bo dong "Chon dap an o khung cau hoi", chu than canh >= 56 px, dem nguoc 5 cham, bo chot_hoi() (chu 36-42 px).
# Ban 1 (28/10/2026): mau boyle/phongxa2 (dung cu + bang + do thi), tieng bao cues.
from engine import *

ROWS = [(5, 9.8, 1.96), (10, 20.1, 2.01), (15, 30.2, 2.01), (20, 39.6, 1.98), (25, 50.3, 2.01)]  # so_lieu_mau
P = 2                                               # tham_so: p mac dinh = 2 cap cuc (ro-to 2p = 4 cuc)
VIS = 0.05                                          # hinh quay cham: 1 vong/s that -> 0,05 vong/s tren man hinh
DARK_OR = (181, 71, 8)                              # chu cam tren nen sang >= 4,5:1
def fmt(v): return (f"{v:.1f}" if isinstance(v, float) else str(v)).replace(".", ",")

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=30):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.75, cx + wdt / 2, cy + size * 0.75), fill=A(bg, alpha), r=int(size * 0.75))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def dots5(d, t, tc, tend, y, col, a=1.0):
    """Dem nguoc 5 cham (r 40 = 70 px trong mp4), moi cham tat dan theo thoi gian nghi."""
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y, 40, A(LIGHT, a) if j >= 5 - n_off else A(col, a))

def dashed(d, p1, p2, color, w=5, dash=22, gap=14):
    L = math.dist(p1, p2)
    if L < 2: return
    n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

# ---------------- ro-to (2p cuc N/S xen ke) + stato co cuon day o dinh ----------------
def rotor(d, cx, cy, r, ang, npole=4, a=1.0, mark=False):
    """ang (do, chieu kim dong ho): khi ang = 0 tam cuc N thu nhat nam o dinh (duoi cuon day)."""
    sec = 360 / npole
    for k in range(npole):
        a0 = -90 - sec / 2 + ang + k * sec
        col = (239, 68, 68) if k % 2 == 0 else (59, 130, 246)
        d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a0 + sec, fill=A(col, a), outline=A(NAVY, a), width=4)
        m = math.radians(a0 + sec / 2)
        text(d, (cx + 0.62 * r * math.cos(m), cy + 0.62 * r * math.sin(m)), "N" if k % 2 == 0 else "S", 58, WHITE, alpha=a)
    dot(d, cx, cy, r * 0.13, A(GRAY, a), A(NAVY, a))
    if mark:   # cham vang danh dau de dem vong
        m = math.radians(-90 + ang)
        dot(d, cx + 0.9 * r * math.cos(m), cy + 0.9 * r * math.sin(m), r * 0.08, A(YELLOW, a), A(NAVY, a))

def stator(d, cx, cy, r, a=1.0):
    ri, ro = r + 22, r + 50
    d.ellipse([cx - ro, cy - ro, cx + ro, cy + ro], fill=A((200, 204, 214), a), outline=A(NAVY, a), width=4)
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=A(BG, a), outline=A(NAVY, a), width=4)
    d.rectangle([cx - 26, cy - ri - 6, cx + 26, cy - r - 8], fill=A((200, 204, 214), a), outline=A(NAVY, a), width=3)
    yt, yb = cy - ro - 4, cy - r - 10
    d.rounded_rectangle([cx - 46, yt + 18, cx + 46, yb], radius=10, fill=A((214, 140, 60), a), outline=A(NAVY, a), width=3)
    for y in range(int(yt + 26), int(yb - 4), 11):
        d.line([(cx - 46, y), (cx + 46, y + 5)], fill=A((150, 85, 30), a), width=3)
    return (cx - 24, yt + 18), (cx + 24, yt + 18)    # hai dau day ra

# ---------------- bo thi nghiem: may phat + tan so ke + den ----------------
RX, RY, RR = 290, 700, 150
def rig(d, ang, reading, lit, n_lbl=None):
    """reading: chuoi tren tan so ke; lit: 0..1 do sang den; n_lbl: chuoi toc do (None = khong ve the toc do)."""
    l1, l2 = stator(d, RX, RY, RR)
    rotor(d, RX, RY, RR, ang, mark=True)
    text(d, (RX, RY + RR + 72), "rô-to 4 cực", 58, NAVY)
    # day: hai dau cuon day -> hai cuc tan so ke (day 1 vong cao hon, khong cat day 2)
    d.line([l1, (l1[0], 448), (600, 448)], fill=GRAY, width=12, joint="curve")
    d.line([l2, (l2[0], 478), (600, 478)], fill=GRAY, width=12, joint="curve")
    # tan so ke
    card(d, (600, 250, 1030, 640), fill=WHITE, outline=NAVY, r=28, w=4)
    text(d, (815, 300), "tần số kế", 56, NAVY)
    d.rounded_rectangle([630, 345, 1000, 470], radius=16, fill=NAVY)
    text(d, (815, 408), reading, 72, (134, 239, 172))
    text(d, (815, 560), "Hz", 60, NAVY)
    for yy in (448, 478): dot(d, 600, yy, 11, NAVY)
    # den nho mac song song voi tan so ke
    for xx in (785, 845): d.line([(xx, 640), (xx, 760)], fill=GRAY, width=10)
    if lit > 0:
        for rr, al in ((120, 0.18), (92, 0.28), (70, 0.4)):
            dot(d, 815, 800, rr * (0.6 + 0.4 * lit), A(YELLOW, al * lit))
    dot(d, 815, 800, 54, mix((235, 235, 235), (255, 236, 140), lit), NAVY)
    d.rectangle([795, 850, 835, 890], fill=GRAY, outline=NAVY, width=3)
    text(d, (815, 945), "đèn", 58, NAVY)
    if n_lbl is not None:
        card(d, (40, 250, 560, 420), fill=WHITE, outline=BLUE, r=28, w=4)
        text(d, (300, 305), n_lbl, 60, BLUE)
        text(d, (300, 375), "(chiếu chậm)", 56, NAVY, bold=False)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    rig(d, 0, "– – –", 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 75, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 205), "Quay n = 10 vòng/s:", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 305), "tần số kế chỉ mấy Hz?", 62, INK, alpha=a)     # K10: khong ve nut A-D
    dots5(d, t, M[1] + 0.3, sc["T"] - 0.1, y0 + 470, PURPLE, a)

# ---------------- canh 2: Tien hanh, ghi bang ----------------
RAMP = 0.35
def row_at(i, sc):
    M = sc["M"]
    return [M[0] + 2.0, M[1] - 0.3, M[1] + 1.5, M[1] + 2.2, M[1] + 2.9][i]   # hang n = 10 to nen ~1,4 s

def n_at(t, sc):
    """toc do quay that (vong/s): tang toi n cua hang i trong RAMP giay truoc row_at(i)."""
    if t < row_at(0, sc): return ROWS[0][0] * ease((t - 0.2) / 0.8)
    n = ROWS[0][0]
    for i in range(1, 5):
        s = row_at(i, sc) - RAMP
        if t < s: break
        n = lerp(ROWS[i - 1][0], ROWS[i][0], ease((t - s) / RAMP))
    return n

def do_state(t, sc):
    last = max([i for i in range(5) if t >= row_at(i, sc)], default=-1)
    ramping = any(row_at(i, sc) - RAMP <= t < row_at(i, sc) for i in range(1, 5))
    if last < 0 or ramping: return last, "· · ·"
    return last, fmt(ROWS[last][1])

def angle(t, f):  # tich phan toc do hien thi (do)
    s, x, dt = 0.0, 0.0, 1 / 60
    while x < t: s += 360 * VIS * f(x) * dt; x += dt
    return s

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    last, rd = do_state(t, sc)
    n_now = n_at(t, sc)
    n_lbl = f"n = {ROWS[last][0]} vòng/s" if last >= 0 and rd != "· · ·" else "n tăng dần…"
    rig(d, angle(t, lambda x: n_at(x, sc)), rd, n_now / ROWS[-1][0], n_lbl)
    # dong ho bam giay: dem vong trong 10 s (kim quay 1 vong tuong trung) truoc khi ghi hang dau
    kw = appear(t, 0.3, 0.3) * (1 - appear(t, row_at(0, sc) + 0.4, 0.3))
    if kw > 0:
        q = clamp((t - 0.4) / (row_at(0, sc) - 0.6)); sx, sy, sr = 545, 590, 46
        d.rectangle([sx - 9, sy - sr - 16, sx + 9, sy - sr], fill=A(NAVY, kw))
        dot(d, sx, sy, sr, A(WHITE, kw), A(NAVY, kw))
        if q > 0: d.pieslice([sx - sr + 7, sy - sr + 7, sx + sr - 7, sy + sr - 7], -90, -90 + 360 * q, fill=A((191, 219, 254), kw))
        m = math.radians(-90 + 360 * q)
        d.line([(sx, sy), (sx + (sr - 9) * math.cos(m), sy + (sr - 9) * math.sin(m))], fill=A(RED, kw), width=5)
    card(d, (40, 1010, 1040, 1640), fill=WHITE, outline=NAVY, w=4)
    xs = (300, 770)
    for x, c in zip(xs, ("n (vòng/s)", "f (Hz)")): text(d, (x, 1068), c, 58, NAVY)
    d.line([(80, 1110), (1000, 1110)], fill=NAVY, width=3)
    for i, (n, f, _) in enumerate(ROWS):
        a = appear(t, row_at(i, sc) - 0.25, 0.3); y = 1165 + i * 98
        if a <= 0: continue
        if i == last: d.rounded_rectangle([70, y - 42, 1010, y + 42], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(n), 62, BLUE, alpha=a)
        text(d, (xs[1], y), fmt(f), 62, RED, alpha=a)

# ---------------- canh 3: Dap an + do thi f(n) ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    ka = appear(t, 0.2, 0.4)
    pill(d, W / 2, 300, "ĐÁP ÁN: ≈ 20 Hz", 56, WHITE, GREEN, ka)
    x0, x1, yb, yt = 200, 960, 920, 470
    X = lambda n: x0 + n / 30 * (x1 - x0); Y = lambda f: yb - f / 60 * (yb - yt)
    card(d, (40, 380, 1040, 1010), fill=WHITE, outline=NAVY, w=3)
    for f in (20, 40, 60): d.line([(x0, Y(f)), (x1, Y(f))], fill=LIGHT, width=3)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 30)], fill=NAVY, width=5)
    text(d, (x0 + 22, yt - 40), "f (Hz)", 58, NAVY, anchor="lm")
    text(d, (x1 + 20, yb - 48), "n (vòng/s)", 58, NAVY, anchor="rm")
    for n in (0, 10, 20, 30):
        d.line([(X(n), yb), (X(n), yb + 10)], fill=NAVY, width=3); text(d, (X(n), yb + 46), str(n), 56, NAVY, bold=False)
    for f in (20, 40, 60):
        d.line([(x0 - 10, Y(f)), (x0, Y(f))], fill=NAVY, width=4); text(d, (x0 - 18, Y(f)), str(f), 56, NAVY, bold=False, anchor="rm")
    kc = ease((t - M[0] - 1.0) / 1.2)
    if kc > 0:
        d.line([(X(0), Y(0)), (X(29 * kc), Y(2 * 29 * kc))], fill=A(BLUE, 0.6), width=7)
        text(d, (X(13) - 20, Y(34)), "f = 2n", 60, BLUE, anchor="rm", alpha=appear(t, M[0] + 2.0))
    for i, (n, f, _) in enumerate(ROWS):
        a = appear(t, 0.4 + i * 0.15, 0.35)
        if a > 0: dot(d, X(n), Y(f), 15 * back(a), ORANGE, WHITE)
    # the ti so f/n: dong 1 o phu de 2, dong 2 sau >= 2 s
    a1 = appear(t, M[1] - 0.2)
    if a1 <= 0: return
    card(d, (40, 1040, 1040, 1640), fill=A(WHITE, a1), outline=A(GREEN, a1), w=5)
    text(d, (W / 2, 1150), "f/n: 1,96 → 2,01", 64, INK, alpha=a1)
    a2 = appear(t, M[1] + 1.9)
    if a2 > 0:
        card(d, (110, 1290, 970, 1560), fill=A((220, 252, 231), a2), r=28)
        text(d, (W / 2, 1425), "≈ 2 = số cặp cực p", 66, GREEN, alpha=a2)

# ---------------- canh 4: co che - moi vong cho p chu ki ----------------
WX0, WX1, WY = 170, 950, 1070
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    th = 360 * ease((t - 0.5) / 5.0)                   # quay dung 1 vong, cham
    cx, cy, r = 400, 560, 170
    stator(d, cx, cy, r)
    rotor(d, cx, cy, r, th, mark=True)
    text(d, (790, 330), "cuộn dây", 58, (150, 85, 30))
    arrow(d, (660, 335), (cx + 60, cy - r - 40), (150, 85, 30), w=5, head=16)
    # do thi dien ap tren cuon day theo goc quay: e ~ sin(p.theta)
    card(d, (40, 830, 1040, 1290), fill=WHITE, outline=NAVY, w=3)
    text(d, (WX0, 890), "điện áp", 58, ORANGE, anchor="lm")
    d.line([(WX0, WY), (WX1, WY)], fill=NAVY, width=4)
    for deg in (0, 180, 360):
        xx = WX0 + deg / 360 * (WX1 - WX0)
        d.line([(xx, WY - 8), (xx, WY + 8)], fill=NAVY, width=3)
        text(d, (xx, WY + 165), f"{deg}°", 56, NAVY, bold=False)
    nseg = int(200 * th / 360)
    if nseg >= 2:
        pts = [(WX0 + j / 200 * (WX1 - WX0), WY - 115 * math.sin(math.radians(P * 360 * j / 200))) for j in range(nseg + 1)]
        d.line(pts, fill=ORANGE, width=7, joint="curve")
    cyc = int(P * th / 360 + 1e-6)
    card(d, (40, 1320, 1040, 1640), fill=WHITE, outline=BLUE, w=5)
    text(d, (W / 2, 1400), f"Số chu kì: {cyc}", 64, ORANGE)
    text(d, (W / 2, 1545), "1 vòng = p chu kì", 64, BLUE, alpha=appear(t, M[1] + 0.2))

# ---------------- canh 5: chua noi duoc gi ----------------
def s_chua(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.3, 0.4); k2 = appear(t, 2.4, 0.4)
    card(d, (40, 260, 1040, 1100), fill=A(WHITE, k1), outline=A(NAVY, k1), w=5)
    rotor(d, 290, 560, 160, 0, npole=4, a=k1)
    text(d, (290, 820), "p = 2: đã đo", 60, GREEN, alpha=k1)
    if k2 > 0:
        rotor(d, 790, 560, 160, 0, npole=2, a=0.35 * k2)
        text(d, (790, 560), "?", 200, NAVY, alpha=k2)
        text(d, (790, 820), "p = 1: chưa đo", 60, DARK_OR, alpha=k2)

# ---------------- canh 6: Bay (3 nhip ~3 s, moi nhip mot phu de) ----------------
TX0, TX1, TYB, TYT = 210, 950, 1510, 1000
def TXf(n): return TX0 + n / 30 * (TX1 - TX0)
def TYf(f): return TYB - f / 120 * (TYB - TYT)
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; b1, b2, b3 = (m - 0.1 for m in M)
    k1 = appear(t, b1, 0.4); k2 = appear(t, b2, 0.4); k3 = appear(t, b3, 0.4)
    pill(d, W / 2, 292, "BẪY", 56, WHITE, RED, k1)
    text(d, (W / 2, 395), "4 cực nên p = 4?", 64, INK, alpha=k1)
    ks = appear(t, b2 + 1.6, 0.4)                # SAI chi hien khi duong p = 4 da ve xong (co bang chung)
    if ks > 0: pill(d, 930, 292, "SAI", 56, WHITE, RED, ks)
    cx, cy, r = W / 2, 660, 165
    rotor(d, cx, cy, r, 45, a=k1)     # xoay 45 do: cap 1 = nua phai (N tren + S duoi), cap 2 = nua trai
    kn = k1 * (1 - k3)
    for j in range(4):                # nhip 1: danh so tung cuc
        m = math.radians(-45 + j * 90)
        x, y = cx + (r + 62) * math.cos(m), cy + (r + 62) * math.sin(m)
        dot(d, x, y, 36, A(WHITE, kn), A(RED, kn)); text(d, (x, y), str(j + 1), 56, RED, alpha=kn)
    if k3 > 0:                        # nhip 3: ghep hai cuc N-S ke nhau thanh mot cap
        for k, col in ((0, PURPLE), (1, TEAL)):
            a0 = -90 + k * 180
            d.arc([cx - r - 26, cy - r - 26, cx + r + 26, cy + r + 26], a0 + 6, a0 + 174, fill=A(col, k3), width=12)
            text(d, (cx + (1 if k == 0 else -1) * (r + 150), cy), f"cặp {k + 1}", 60, col, alpha=k3)
    # nhip 2: do thi so do + duong f = 4n (p = 4) lech xa; nhip 3 them duong f = 2n qua cac diem
    if k2 <= 0: return
    card(d, (40, 900, 1040, 1640), fill=A(WHITE, k2), outline=A(NAVY, k2), w=3)
    d.line([(TX0, TYB), (TX1 + 25, TYB)], fill=A(NAVY, k2), width=5); d.line([(TX0, TYB), (TX0, TYT - 20)], fill=A(NAVY, k2), width=5)
    text(d, (TX0 + 22, TYT - 30), "f (Hz)", 58, NAVY, anchor="lm", alpha=k2)
    for n in (0, 10, 20, 30): text(d, (TXf(n), TYB + 48), str(n), 56, NAVY, bold=False, alpha=k2)
    for f in (50, 100):
        d.line([(TX0 - 10, TYf(f)), (TX0, TYf(f))], fill=A(NAVY, k2), width=4)
        text(d, (TX0 - 18, TYf(f)), str(f), 56, NAVY, bold=False, anchor="rm", alpha=k2)
    text(d, (TX0 - 18, TYB), "0", 56, NAVY, bold=False, anchor="rm", alpha=k2)
    kl = ease((t - b2 - 0.3) / 1.0)
    if kl > 0:
        dashed(d, (TXf(0), TYf(0)), (TXf(28 * kl), TYf(4 * 28 * kl)), A(RED, k2), w=7)
        text(d, (TXf(17) - 24, TYf(80)), "p = 4", 60, RED, anchor="rm", alpha=appear(t, b2 + 1.0))
    for n, f, _ in ROWS: dot(d, TXf(n), TYf(f), 14, A(ORANGE, k2), A(WHITE, k2))
    text(d, (TXf(25), TYf(50.3) + 70), "số đo", 58, ORANGE, alpha=k2)
    if k3 > 0:
        d.line([(TXf(0), TYf(0)), (TXf(29), TYf(58))], fill=A(GREEN, k3), width=7)
        text(d, (TXf(27) + 30, TYf(54) - 60), "p = 2", 60, GREEN, anchor="rm", alpha=k3)

# ---------------- canh 7: THU NGHI (dung ca cau_chot cua khung) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    stator(d, 300, 620, 170)
    rotor(d, 300, 620, 170, 0, npole=6)
    card(d, (600, 300, 1030, 640), fill=WHITE, outline=NAVY, r=28, w=4)
    text(d, (815, 350), "tần số kế", 56, NAVY)
    d.rounded_rectangle([630, 395, 1000, 520], radius=16, fill=NAVY)
    kq = appear(t, 2.6, 0.4)
    text(d, (815, 458), "?", 84, (134, 239, 172), alpha=0.35 + 0.65 * kq)
    text(d, (815, 585), "Hz", 60, NAVY)
    k = 1.0                                     # hien cung luc voi hinh (mot khoi chu moi o dau canh)
    card(d, (50, 1000, 1030, 1640), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1080, "THỬ NGHĨ", 56, WHITE, DARK_OR, k)
    text(d, (W / 2, 1215), "Rô-to 6 cực,", 64, INK, alpha=k)
    text(d, (W / 2, 1320), "quay 900 vòng/phút:", 64, INK, alpha=k)
    text(d, (W / 2, 1425), "f = ? Hz", 66, DARK_OR, alpha=k)
    dots5(d, t, M[0] + 0.5, sc["T"] - 0.1, 1555, DARK_OR, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, wy, ch, tr, e = (sc[k] for k in ("hook", "do", "ans", "why", "chua", "trap", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + row_at(i, do), "tap") for i in range(5)]
    out += [(an["t0"] + 0.2, "ding"), (an["t0"] + an["M"][1] + 1.9, "tap"), (wy["t0"] + wy["M"][1] + 0.2, "tap"),
            (ch["t0"] + 2.4, "tap"), (tr["t0"] + tr["M"][0] - 0.1, "buzz"), (tr["t0"] + tr["M"][2] - 0.1, "tap"),
            (e["t0"] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-mayphatdien-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Máy phát điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Máy phát mini", draw=s_hook, tail=0.3, caps=[
   ("Máy phát nối đèn.", 2.6),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đếm vòng trong 10 s ra n.", 3.2),
   ("Quay nhanh dần, đọc f.", 3.7)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.3, caps=[
   ("Gấp đôi n, không bằng n.", 3.0),
   ("Số 2 ứng với gì?", 3.3)]),
 dict(key="why", title="Vì sao f = n·p?", draw=s_why, tail=0.3, caps=[
   ("Mỗi cặp N–S qua: 1 chu kì.", 3.4),
   ("Quay n vòng/s: f = n·p.", 2.8)]),
 dict(key="chua", title="Chưa nói được gì?", draw=s_chua, tail=0.3, caps=[
   ("Mới thử một máy.", 3.7)]),
 dict(key="trap", title="Bẫy", draw=s_trap, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Đường p = 4 có khớp?", 3.0),
   ("Ghép N với S thành cặp.", 3.0)]),
 dict(key="end", title="Thử nghĩ", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.0)]),
])
