# Clip: tn-l11-vantocdddh-01 - Con lac lo xo nam ngang: do A, T roi tinh v_max va a (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-vantocdddh-01.json:
#   tham_so: A = 4,0 cm (sai so thuoc 0,1 cm); x tu -4 toi 4 cm.
#   cac_buoc.lam: t10 nam lan 8,02; 7,96; 8,08; 7,94; 8,00 s. quan_sat: T tb 0,800 s; omega = 7,854 rad/s.
#   so_lieu_mau.ghi_chu: |v|(0) = 31,42; |v|(2 cm) = 27,21, a(2 cm) = -123,4; |v|(4 cm) = 0, a(4 cm) = -246,7;
#   Delta v_max ~ 1,06 cm/s. hien_tuong_hay_sai[1]: tuong a cung dau voi x -> canh bay.
#   Cau chot: vat o x = -3,0 cm (trong khoang tham_so x, chua hien) -> a = -omega^2 x = +185,1 cm/s^2 (KHONG hien).
# Dan canh rieng cua clip nay (khac motadddh/conangdddh): thuoc + dong ho bam giay + bang t10 o Tien hanh;
#   Ket qua = BA thanh ray nho xep doc (x = 0; 2; 4 cm) moi thanh co mui ten v (xanh) va a (do) dung ti le.
# Chuyen dong o Tien hanh: x = A cos(2 pi s / T), s = so dong ho (T = 0,800 s), tua nhanh x2 (ghi tren man).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (A bang thuoc; bam 10 dao dong lan 5; bang t10 -> T, omega)
#       -> Ket qua (3 vi tri + DAP AN + cong thuc + sai so) -> Bay (a cung dau x) roi Chua noi duoc -> Chot + hoi.
from engine import *

A_CM, T_TB, OMEGA = 4.0, 0.800, 7.854
T10 = [8.02, 7.96, 8.08, 7.94, 8.00]                    # cac_buoc.lam (lan 5 = lan quay)
PTS = [(0.0, "31,42", "0"), (2.0, "27,21", "−123,4"), (4.0, "0", "−246,7")]   # x, toc do, a (ghi_chu)
V_OF = {0.0: 31.42, 2.0: 27.21, 4.0: 0.0}; A_OF = {0.0: 0.0, 2.0: -123.4, 4.0: -246.7}
FAST = 2.0                                              # tua nhanh x2
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55)
BLOCK = (59, 130, 246); RAILC = (120, 125, 145)

_TI = {}
def TI(size):                                           # Times Bold Italic cho omega (omega cua SF giong chu w)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi cong thuc: 'ω' ve bang Times Bold Italic; _{..} chi so duoi, ^{..} so mu (>= 36 px)."""
    fs = []
    for p in [p for p in re.split(r"(ω|_\{[^}]*\}|\^\{[^}]*\})", s) if p]:
        if p == "ω": fs.append((p, TI(size * 1.12), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(max(36, size * 0.62)), size * 0.26))
        elif p.startswith("^{"): fs.append((p[2:-1], F(max(36, size * 0.62)), -size * 0.34))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

# ---------------- ray lon (khung nguon 1080x1920) ----------------
XO, PX, RY = 620, 60, 430           # x man hinh cua O; px moi cm; tam vat
BW, BH = 110, 90                    # vat
WALL = 72
def X(x_cm, xo=XO, px=PX): return xo + x_cm * px

def spring(d, xa, xb, y, amp=24, n=12, col=NAVY, w=5):
    e = 14; pts = [(xa, y), (xa + e, y)]
    L = (xb - e) - (xa + e)
    for i in range(1, 2 * n):
        pts.append((xa + e + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(xb - e, y), (xb, y)]
    d.line(pts, fill=col, width=w, joint="curve")

def rail(d, x_cm, ruler=True, olab=True, alpha=1.0):
    """Ray lon: tuong trai, lo xo, vat tam X(x_cm), thuoc mm duoi ray, vach O net dut."""
    c = lambda col: A(col, alpha)
    d.rectangle([50, 330, WALL, 492], fill=c(GRAY))
    for yy in range(340, 490, 24): d.line([(50, yy + 14), (WALL - 2, yy)], fill=c(NAVY), width=2)
    d.rectangle([50, 478, 1020, 492], fill=c(RAILC))
    for yy in range(360, 480, 22): d.line([(XO, yy), (XO, yy + 11)], fill=c(MUTED), width=3)   # VTCB O
    if olab: text(d, (XO, 316), "O", 40, MUTED, alpha=alpha)
    xc = X(x_cm)
    spring(d, WALL, xc - BW / 2, RY, n=9, col=c(NAVY))
    d.rounded_rectangle([xc - BW / 2, RY - BH / 2, xc + BW / 2, RY + BH / 2], radius=12, fill=c(BLOCK), outline=c(NAVY), width=4)
    text(d, (xc, RY), "m", 44, WHITE, alpha=alpha)
    if not ruler: return
    d.rectangle([X(-5), 505, X(5), 545], fill=c((250, 240, 200)), outline=c(NAVY), width=2)
    for k in range(-50, 51):                             # vach mm (ve moi 1 mm la qua day -> moi 0,5 cm)
        if k % 5: continue
        L = 22 if k % 10 == 0 else 12
        d.line([(X(k / 10), 505), (X(k / 10), 505 + L)], fill=c(NAVY), width=3 if L == 22 else 2)
    for k in range(-4, 5):
        text(d, (X(k), 580), (str(k) if k >= 0 else "−" + str(-k)), 38, MUTED, bold=False, alpha=alpha)
    text(d, (X(-5) - 40, 580), "cm", 38, MUTED, bold=False, alpha=alpha)

def stopwatch(d, s, n, running, alpha=1.0, box=(60, 735, 520, 1000), hook=False):
    x0, y0, x1, y1 = box; cx = (x0 + x1) / 2
    card(d, box, fill=A((70, 78, 100), alpha), r=24)
    text(d, (cx, y0 + 40), "đồng hồ bấm giây" if hook else "đồng hồ · lần 5", 38, WHITE, bold=False, alpha=alpha)
    card(d, (x0 + 30, y0 + 75, x1 - 30, y0 + 175), fill=A((220, 240, 225), alpha), r=14)
    text(d, (cx, y0 + 125), vn(s) + " s", 76, (20, 60, 30), alpha=alpha)
    if not hook: text(d, (cx, y0 + 222), f"đếm: {n}/10 dao động", 40, WHITE, alpha=alpha)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rail(d, A_CM)
    k = appear(t, 0.6, 0.5)                              # do lech 4,0 cm (O -> vat)
    if k > 0:
        y = 360
        arrow(d, (XO + 6, y), (X(A_CM) - 6, y), A(ORANGE, k), w=5, head=18)
        text(d, ((XO + X(A_CM)) / 2 + 30, 318), "4,0 cm", 40, ORANGE, alpha=k)
    stopwatch(d, 0.0, 0, False, alpha=appear(t, 1.0, 0.5), box=(280, 660, 800, 870), hook=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    # vat mo (net dut) o O: diem xuat phat trong cau hoi; khong ve v, a
    for xx in range(int(XO - BW / 2), int(XO + BW / 2), 20):
        d.line([(xx, RY - BH / 2), (xx + 10, RY - BH / 2)], fill=A(BLUE, a), width=3)
        d.line([(xx, RY + BH / 2), (xx + 10, RY + BH / 2)], fill=A(BLUE, a), width=3)
    for yy in range(int(RY - BH / 2), int(RY + BH / 2), 20):
        d.line([(XO - BW / 2, yy), (XO - BW / 2, yy + 10)], fill=A(BLUE, a), width=3)
        d.line([(XO + BW / 2, yy), (XO + BW / 2, yy + 10)], fill=A(BLUE, a), width=3)
    y0 = 990 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 245, "Vật đi từ O ra biên +4 cm.\nTốc độ và độ lớn gia tốc\nthay đổi thế nào?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
REL = 0.3                       # tha vat sau M[1] + REL
def do_state(t, sc):
    """-> (s dong ho, x cm, so dao dong dem duoc, da dung). Mot nguon duy nhat cho vat, dong ho, bang."""
    M = sc["M"]
    if t < M[1] + REL: return 0.0, A_CM, 0, False
    s = min(T10[4], (t - M[1] - REL) * FAST)
    x = A_CM * math.cos(2 * math.pi * s / T_TB)
    n = int(s / T_TB + 1e-6)
    return s, x, n, s >= T10[4] - 1e-9

def s_do(img, d, t, sc):
    M = sc["M"]
    s, x, n, stop = do_state(t, sc)
    rail(d, x)
    ka = appear(t, 0.9, 0.4)                             # thuoc: A = 4,0 cm (chi khi vat con o bien)
    if ka > 0 and t < M[1] + REL:
        y = 640
        d.line([(XO, y), (X(A_CM), y)], fill=A(ORANGE, ka), width=5)
        for xx in (XO, X(A_CM)): d.line([(xx, y - 16), (xx, y + 16)], fill=A(ORANGE, ka), width=5)
        text(d, ((XO + X(A_CM)) / 2, 690), "A = 4,0 cm", 42, ORANGE, alpha=ka)
    if t < M[1] - 0.2: return
    kb = appear(t, M[1] - 0.2, 0.4)
    stopwatch(d, s, n, not stop, alpha=kb)
    if M[1] + REL <= t and not stop:
        card(d, (60, 1020, 360, 1084), fill=ORANGE, r=32); text(d, (210, 1052), "tua nhanh ×2", 38, WHITE)
    # bang t10: lan 1-4 da do, lan 5 dien khi dong ho dung
    tx0, tx1, ty0 = 560, 1020, 735
    card(d, (tx0, ty0, tx1, ty0 + 420), fill=A(WHITE, kb), outline=A(NAVY, kb), r=20, w=3)
    text(d, (650, ty0 + 40), "Lần", 40, INK, alpha=kb)
    eq(d, 860, ty0 + 40, "t_{10} (s)", 40, INK, alpha=kb)
    d.line([(tx0 + 10, ty0 + 78), (tx1 - 10, ty0 + 78)], fill=A(NAVY, kb), width=3)
    for i, v in enumerate(T10):
        y = ty0 + 115 + i * 64
        if i == 4:
            if not stop: text(d, (650, y), "5", 40, INK, alpha=kb); continue
            kr = appear(t, M[1] + REL + T10[4] / FAST + 0.05, 0.3)
            d.rounded_rectangle([tx0 + 14, y - 30, tx1 - 14, y + 30], radius=10, fill=A((255, 237, 213), kr))
        text(d, (650, y), str(i + 1), 40, INK, alpha=kb)
        text(d, (860, y), vn(v), 40, INK, alpha=kb)
    if stop:                                             # T trung binh, omega
        kt = appear(t, M[1] + REL + T10[4] / FAST + 0.5, 0.45)
        card(d, (60, 1190, 1020, 1430), fill=A((239, 246, 255), kt), outline=A(BLUE, kt), r=22, w=3)
        eq(d, W / 2, 1260, "T trung bình = 0,800 s", 46, INK, alpha=kt)
        eq(d, W / 2, 1360, "ω = 2π/T = 7,854 rad/s", 46, DBLUE, alpha=kt)

# ---------------- canh 3: Ket qua (ba vi tri, vat dang ra bien) ----------------
MXO, MPX = 470, 45
RV, RA = 7.0, 240 / 246.7                                # px moi cm/s; px moi cm/s^2
ROWY = [340, 620, 900]
def mini(d, y, x_cm, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([50, y - 50, 66, y + 44], fill=c(GRAY))
    d.rectangle([50, y + 36, 1000, y + 46], fill=c(RAILC))
    for yy in range(y - 46, y + 36, 18): d.line([(MXO, yy), (MXO, yy + 9)], fill=c(MUTED), width=3)
    xc = MXO + x_cm * MPX
    spring(d, 66, xc - 40, y, amp=16, n=6, col=c(NAVY), w=4)
    d.rounded_rectangle([xc - 40, y - 32, xc + 40, y + 32], radius=10, fill=c(BLOCK), outline=c(NAVY), width=3)
    return xc

def s_dapan(img, d, t, sc):
    M = sc["M"]
    for i, (xc_cm, vs, as_) in enumerate(PTS):
        k = appear(t, 0.5 + 1.0 * i, 0.4)
        if k <= 0: continue
        y = ROWY[i]; xc = mini(d, y, xc_cm, k)
        text(d, (60, y - 92), "x = 0" if xc_cm == 0 else f"x = {vn(xc_cm, 1)} cm", 40, INK, anchor="lm", alpha=k)
        lv = V_OF[xc_cm] * RV                            # v huong ra bien (+), a huong ve O
        if lv > 0:
            arrow(d, (xc, y - 62), (xc + lv, y - 62), A(BLUE, k), w=7, head=22)
            text(d, (xc + lv + 14, y - 62), "v", 42, DBLUE, anchor="lm", alpha=k)
        la = -A_OF[xc_cm] * RA
        if la > 0:
            arrow(d, (xc, y + 72), (xc - la, y + 72), A(RED, k), w=7, head=22)
            text(d, (xc - la - 14, y + 72), "a", 42, DRED, anchor="rm", alpha=k)
        msg = f"tốc độ {vs} cm/s · a = {as_}" + (" cm/s²" if as_ != "0" else "")
        text(d, (W / 2, y + 128), msg, 40, INK, alpha=k)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        lab = "ĐÁP ÁN · tốc độ giảm, |a| tăng"
        pw = tw(d, lab, F(42)) + 56
        card(d, (W / 2 - pw / 2, 1066, W / 2 + pw / 2, 1130), fill=A(NAVY, kb), r=32)
        text(d, (W / 2, 1098), lab, 42, WHITE, alpha=kb)
    kf = appear(t, M[1] + 0.5, 0.45)
    if kf > 0:
        card(d, (40, 1150, 1040, 1450), fill=A((236, 253, 243), kf), outline=A(GREEN, kf), r=22, w=3)
        eq(d, W / 2, 1210, "v_{max} = Aω = 31,42 cm/s", 46, DBLUE, alpha=kf)
        eq(d, W / 2, 1300, "a = −ω^{2}x", 46, DRED, alpha=kf)
        ks = appear(t, M[1] + 1.2, 0.45)
        eq(d, W / 2, 1390, "sai số v_{max} ≈ 1,06 cm/s (thước, đồng hồ)", 40, INK, alpha=ks)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
XB = 2.0
def s_bay(img, d, t, sc):
    M = sc["M"]
    rail(d, XB)
    y = 360                                              # li do x: O -> vat
    d.line([(XO + 4, y), (X(XB) - 4, y)], fill=ORANGE, width=5)
    arrow(d, (XO + 4, y), (X(XB) - 4, y), ORANGE, w=5, head=18)
    text(d, (X(XB) + 20, 318), "x = +2,0 cm", 40, ORANGE)
    kc = appear(t, 1.5, 0.4)                             # a ve O hien CUNG luc chu ✓
    k2 = appear(t, M[1] - 0.1, 0.45)
    ka = max(kc, k2)
    if ka > 0:
        arrow(d, (X(XB), 650), (X(XB) - 123.4 * RA, 650), A(RED, ka), w=8, head=24)
        text(d, (X(XB) - 123.4 * RA - 14, 650), "a", 44, DRED, anchor="rm", alpha=ka)
    a1 = appear(t, 0.0, 0.3) * (1 - appear(t, M[1] - 0.3, 0.2))   # bay tat han truoc khi hop sau hien
    if a1 > 0:
        y0 = 760
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“a cùng dấu với x”"
        ks = clamp((t - 0.9) / 0.4); f = F(50); lw = tw(d, q, f); yy = y0 + 180
        text(d, (W / 2, yy), q, 50, DRED, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A((140, 15, 15), a1), width=7)
        kk = a1 * kc
        ctext(d, y0 + 300, "✓ a luôn hướng về O", 46, DGREEN, maxw=920, alpha=kk)
        ctext(d, y0 + 390, "x = +2,0 cm → a = −123,4 cm/s²", 44, INK, maxw=940, alpha=kk)
    if k2 > 0:
        y0 = 760 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Ma sát: đã bỏ qua", "• Biên độ khác 4,0 cm: chưa đo")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 190 + j * 110), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot -> THU NGHI: vat o x = -3,0 cm (chua tung hien), a bao nhieu (+185,1 cm/s^2, khong hien); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Qua O: tốc độ lớn nhất.\nỞ biên: |a| lớn nhất.", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1180), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.9, 0.5)
    ctext(d, 800, "Vật ở x = −3,0 cm.\nGia tốc khoảng bao nhiêu?", 48, INK, maxw=920, alpha=kq)
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 920, 970, 1150), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 970, "Gợi ý", 38, INK, alpha=kh)
    ctext(d, 1075, "Nhìn lại ray x = 2,0 cm", 44, ORANGE, maxw=820, alpha=kh)
    if kq > 0:                                           # hinh: vat o -4 cm, khong ve mui ten a
        y = 1340; xo, px = 560, 48
        d.rectangle([80, y - 60, 98, y + 50], fill=A(GRAY, kq))
        d.rectangle([80, y + 42, 1000, y + 52], fill=A(RAILC, kq))
        for yy in range(y - 56, y + 42, 18): d.line([(xo, yy), (xo, yy + 9)], fill=A(MUTED, kq), width=3)
        xc = xo - 3 * px
        spring(d, 98, xc - 40, y, amp=16, n=6, col=A(NAVY, kq), w=4)
        d.rounded_rectangle([xc - 40, y - 34, xc + 40, y + 34], radius=10, fill=A(BLOCK, kq), outline=A(NAVY, kq), width=3)
        for xv, lab in ((-3, "−3"), (0, "0"), (3, "3")):
            d.line([(xo + xv * px, y + 52), (xo + xv * px, y + 70)], fill=A(NAVY, kq), width=3)
            text(d, (xo + xv * px, y + 100), lab, 38, MUTED, bold=False, alpha=kq)
        text(d, (xo + 3 * px + 60, y + 100), "cm", 38, MUTED, bold=False, alpha=kq)
        text(d, (xc, y - 90), "a = ?", 44, PURPLE, alpha=kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    rel = do["t0"] + do["M"][1] + REL
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + 0.15, "ding"), (rel, "tap")]
    out += [(rel + k * T_TB / FAST, "tick") for k in range(1, 10)]
    out += [(rel + T10[4] / FAST, "tap")]
    out += [(da["t0"] + da["M"][1] - 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-vantocdddh-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Vận tốc, gia tốc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Con lắc lò xo nằm ngang", draw=s_hook, tail=0.8, caps=[
   ("Kéo lệch 4,0 cm rồi thả.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đo biên độ bằng thước mm.", 3.2),
   ("Bấm giờ 10 dao động, đo năm lần.", 7.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Ba vị trí, vật đang ra biên.", 4.0),
   ("Qua O nhanh nhất, gia tốc bằng 0.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy hay gặp khi thế số.", 4.2),
   ("Kết quả này còn giới hạn.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])
