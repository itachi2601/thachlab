# Clip: tn-l10-trondeu-03 - Do chu ki dia xoay lo vi song (3 vong x 5 lan), suy ra f va omega (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trondeu-03.json:
#   tham_so: T0 = 10,0 s (chu ki that, mac dinh), r = 0,14 m (bang dinh cach tam 14,0 cm), n = 3 vong, dt sai so 0,2 s.
#   so_lieu_mau: dt 3 vong = 30,2 / 29,8 / 30,1 / 30,4 / 29,9 s ; ghi_chu: TB 30,08 s -> T = 10,027 s ; rut_ra: T ~ 10,03 s,
#   f ~ 0,100 Hz, omega ~ 0,627 rad/s.
# Dia ve quay DEU dung T0 = 10,0 s: goc bang dinh theta = 2.pi.R/T0 (R = thoi gian that, s), bang dinh qua moc khi R = 10k.
#   Dong ho bam lech tay (moi lan bam <= 0,2 s) cho ra dung so kho: lan 1 bat dau 0 dung 30,2 (dung tre 0,2 s -> bang dinh
#   qua moc 7,2 do, co dung hinh) ; lan 2: 40 -> 69,8 ; lan 3: 80 -> 110,1 ; lan 4: 119,8 -> 150,2 ; lan 5: 160,1 -> 190,0.
#   So vong (lan 1) dem lan bang dinh qua moc -> doi so dung luc dong ho 10,0/20,0/30,0 (kiem bang ma moi 0,05 s).
# Du doan (K10: chi cau hoi + hinh): 3 vong ~ 30 s -> omega khoang bao nhieu? Dap an: khoang 0,6 rad/s.
#   Nhieu: khoang 0,1 (nham f), khoang 0,2 (quen chia 3: 2.pi/30), khoang 0,3 (pi/T, quen x2) - deu xa 0,627.
# Truc chinh: HINH DIA QUAY + DONG HO + do thi cham dt (khong bang).
# Cau chot hoi r = 7 cm (chua tung hien, trong mien tham_so 5-15 cm): omega KHONG doi (nguoc phan xa "gan tam -> cham").
from engine import *

T0, R_CM, PXCM = 10.0, 14.0, 20.0          # chu ki that (s), ban kinh bang dinh (cm), px/cm (dia 15 cm = 300 px)
DT = [30.2, 29.8, 30.1, 30.4, 29.9]          # thoi gian 3 vong (s)
TRIALS = [(0.0, 30.2), (40.0, 69.8), (80.0, 110.1), (119.8, 150.2), (160.1, 190.0)]   # (R bam bat dau, R bam dung)
TB, TT, FF_, WW = "30,08", "10,03", "0,100", "0,627"
GLASS = (226, 238, 248); GLASS_D = (148, 163, 184); TAPE = ORANGE; FLOOR = (236, 231, 220)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

_TI = {}
def TI(size):                                # Times Bold Italic cho omega, pi, Delta (omega cua SF giong w)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    fs = []
    for p in [p for p in re.split(r"(ω|π)", s) if p]:
        fs.append((p, TI(size * 1.12) if p in ("ω", "π") else F(size)))
    tot = sum(tw(d, p, f) for p, f in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f in fs:
        dtext(d, (x, cy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

# ---------------- dia xoay nhin tu tren ----------------
CX, CY, RD = 350, 650, 300
def P(th, r): return (CX + r * math.sin(th), CY - r * math.cos(th))      # th do theo chieu kim dong ho tu dinh

def disc(d, th, sector=None, late=0.0, rline=False, ghost=False):
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    d.rounded_rectangle((70, 300, 640, 990), radius=28, fill=FLOOR)
    d.ellipse([CX - RD, CY - RD, CX + RD, CY + RD], fill=GLASS, outline=GLASS_D, width=6)
    for rr in (230, 150): d.ellipse([CX - rr, CY - rr, CX + rr, CY + rr], outline=(205, 218, 232), width=3)
    rt = R_CM * PXCM
    if sector:                                                            # goc quet trong 1 s
        a0, a1 = (-90 + math.degrees(x) for x in sector)                  # goc quet tu a0 toi a1 (rad, tu dinh)
        if a1 - a0 > 0.5:
            d.pieslice([CX - rt, CY - rt, CX + rt, CY + rt], a0, a1, fill=(254, 215, 170))
            d.arc([CX - rt - 8, CY - rt - 8, CX + rt + 8, CY + rt + 8], a0, a1, fill=ORANGE, width=8)
    # moc co dinh tren thanh lo (dinh) + vach qua mep dia
    d.polygon([(CX - 20, CY - RD - 40), (CX + 20, CY - RD - 40), (CX, CY - RD - 6)], fill=RED)
    for yy in range(int(CY - RD + 2), int(CY - rt + 40), 16):
        d.line([(CX, yy), (CX, min(yy + 8, CY - rt + 40))], fill=RED, width=4)
    text(d, (CX + 34, CY - RD - 26), "mốc", 40, RED, anchor="lm")
    if late > 0:                                                          # cung bang dinh da qua moc khi bam dung
        ra = rt - 36                                                      # cung ngay trong bang dinh (khong bi che)
        d.arc([CX - ra, CY - ra, CX + ra, CY + ra], -90, -90 + math.degrees(late), fill=RED, width=10)
        d.line([P(late, ra - 6), P(late, rt - 26)], fill=RED, width=4)
    # coc nuoc o tam
    d.ellipse([CX - 62, CY - 62, CX + 62, CY + 62], fill=WHITE, outline=NAVY, width=5)
    d.ellipse([CX - 44, CY - 44, CX + 44, CY + 44], fill=(147, 197, 253))
    if rline:
        a, b = P(th, 66), P(th, rt - 26)
        n = 10
        for i in range(0, n, 2):
            d.line([(lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n)), (lerp(a[0], b[0], (i + 1) / n), lerp(a[1], b[1], (i + 1) / n))],
                   fill=TAPE, width=5)
    # bang dinh: hinh chu nhat theo ban kinh
    ur = (math.sin(th), -math.cos(th)); ut = (math.cos(th), math.sin(th))
    pts = [(CX + ur[0] * (rt + sr) + ut[0] * st, CY + ur[1] * (rt + sr) + ut[1] * st) for sr, st in ((-26, -14), (26, -14), (26, 14), (-26, 14))]
    d.polygon(pts, fill=TAPE, outline=(154, 52, 18))

def theta(R): return 2 * math.pi * R / T0

# ---------------- do thi cham dt ----------------
def XV(v): return 240 + (v - 29.6) / 1.0 * 720
ROWY = [1170 + 58 * i for i in range(5)]; AXY = 1462
def plot(d, n, mean_k=0.0, ring=None):
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 1060), "Δt: thời gian 3 vòng (s)", 40, INK)
    for v in (29.6, 29.8, 30.0, 30.2, 30.4, 30.6):
        d.line([(XV(v), ROWY[0] - 30), (XV(v), AXY)], fill=(240, 236, 228), width=2)
        d.line([(XV(v), AXY), (XV(v), AXY + 12)], fill=NAVY, width=3)
        text(d, (XV(v), AXY + 44), vn(v, 1), 40, INK, bold=False)
    d.line([(XV(29.6) - 20, AXY), (XV(30.6) + 30, AXY)], fill=NAVY, width=4)
    for i in range(5):
        text(d, (66, ROWY[i]), f"Lần {i + 1}", 40, MUTED if i >= n else INK, bold=False, anchor="lm")
    if mean_k > 0:
        xm = XV(30.08)
        for yy in range(ROWY[0] - 26, AXY, 22):
            d.line([(xm, yy), (xm, min(yy + 12, AXY))], fill=A(GREEN, mean_k), width=5)
        text(d, (xm, 1124), "trung bình " + TB, 40, GREEN, alpha=mean_k)
    for i in range(n):
        x, y = XV(DT[i]), ROWY[i]
        if ring == i: d.ellipse([x - 28, y - 28, x + 28, y + 28], outline=NAVY, width=5)
        dot(d, x, y, 15, BLUE, WHITE)
        text(d, (x + 28, y), vn(DT[i], 1), 38, BLUE, anchor="lm")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    th = theta(t - 0.4 + 2.5)                       # quay that (x1) ; bang dinh qua moc luc t = 7,9 s (trong luc nghi)
    disc(d, th, rline=True)
    text(d, (840, 480), "băng dính", 44, TAPE)
    text(d, (840, 550), "cách tâm 14,0 cm", 40, INK)
    text(d, (840, 720), "cốc nước", 40, (37, 99, 235))
    d.line([(CX + 64, CY + 14), (750, 712)], fill=(37, 99, 235), width=3)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 55), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 160, "3 vòng hết khoảng 30 s.", 50, INK, maxw=920, alpha=a)
    eq(d, W / 2, y0 + 260, "Tốc độ góc ω khoảng bao nhiêu?", 50, INK, alpha=a)
    eq(d, W / 2, y0 + 360, "ω: góc quay mỗi giây", 40, INK, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 484], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 484], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
TA, S1, S2 = 0.6, 8.0, 30.0          # bam lan 1 luc t = 0,6 ; tua x8 (lan 1), x30 (lan 2-5)
T_STOP1 = TA + TRIALS[0][1] / S1
def R_of(t, tf):
    """thoi gian that R (s) theo t canh; tf: het dung hinh (= M[1])."""
    if t <= T_STOP1: return (t - TA) * S1
    if t <= tf: return TRIALS[0][1]
    return TRIALS[0][1] + (t - tf) * S2

def watch(R):
    """-> (lan j (0-based, -1 chua bam), so dong ho (s), dang chay?, so vong lan 1, so cham da co)."""
    j = -1
    for i, (a, b) in enumerate(TRIALS):
        if R >= a - 1e-9: j = i
    if j < 0: return -1, 0.0, False, 0, 0
    a, b = TRIALS[j]
    val = math.floor((min(R, b) - a) * 10 + 1e-6) / 10
    run = R < b
    laps = min(3, int(math.floor((R - a) / T0 + 1e-9))) if j == 0 else 0
    ndot = sum(1 for (_, bb) in TRIALS if R >= bb - 1e-9)
    return j, val, run, laps, ndot

def s_do(img, d, t, sc):
    M = sc["M"]; tf = M[1]
    R = R_of(t, tf); j, val, run, laps, ndot = watch(R)
    frozen = T_STOP1 < t <= tf
    disc(d, theta(R), late=theta(TRIALS[0][1] - 30.0) if frozen and t > T_STOP1 + 0.3 else 0.0)
    card(d, (680, 330, 1020, 540), fill=NAVY, r=26)
    text(d, (850, 375), "đồng hồ", 40, (220, 225, 240), bold=False)
    text(d, (850, 465), vn(val, 1) + " s", 66, WHITE)
    if j >= 0: text(d, (850, 600), f"Lần {j + 1}", 44, INK)
    if j == 0:
        text(d, (850, 680), f"vòng: {laps}", 44, BLUE)
    if frozen and t > T_STOP1 + 0.3:                       # o phong to x3 quanh moc (dung hinh)
        kq = appear(t, T_STOP1 + 0.3, 0.4)
        zc = (CX + 6, CY - R_CM * PXCM + 10); hz = 40
        z = img.crop((int(zc[0] - hz), int(zc[1] - hz), int(zc[0] + hz), int(zc[1] + hz))).resize((276, 276), Image.LANCZOS)
        zx, zy = CX - 138, CY - 120
        if kq > 0.05:
            m = Image.new("L", z.size, int(255 * kq)); img.paste(z, (zx, zy), m)
            d.rectangle([zx, zy, zx + 276, zy + 276], outline=A(RED, kq), width=5)
            text(d, (zx + 262, zy + 30), "×3", 40, RED, anchor="rm", alpha=kq)
            d.rectangle([zc[0] - hz, zc[1] - hz, zc[0] + hz, zc[1] + hz], outline=A(RED, kq), width=3)
            lw = tw(d, "đã qua mốc", F(40)) + 36
            card(d, (CX - lw / 2 + 10, zy + 286, CX + lw / 2 + 10, zy + 346), fill=A(WHITE, kq), outline=A(RED, kq), r=28, w=4)
            text(d, (CX + 10, zy + 316), "đã qua mốc", 40, RED, alpha=kq)
    if frozen:
        k = appear(t, T_STOP1 + 0.3, 0.4)
        card(d, (690, 740, 1010, 800), fill=A((254, 242, 242), k), outline=A(RED, k), r=30, w=3)
        text(d, (850, 770), "dừng hình", 40, RED, alpha=k)
        text(d, (850, 880), "bấm trễ ≈ 0,2 s", 40, RED, alpha=k)
    else:
        sp = "tua nhanh ×" + str(int(S1 if t <= T_STOP1 else S2))
        cw = tw(d, sp, F(40)) + 40
        card(d, (850 - cw / 2, 770, 850 + cw / 2, 830), fill=(241, 245, 249), outline=GLASS_D, r=30, w=3)
        text(d, (850, 800), sp, 40, MUTED)
    plot(d, ndot)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · khoảng 0,6 rad/s"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lb, 40, WHITE, alpha=ka)
    card(d, (40, 360, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    k1, k2, k3, k4 = appear(t, 0.6, 0.4), appear(t, 1.6, 0.4), appear(t, 2.6, 0.4), appear(t, 3.6, 0.4)
    text(d, (W / 2, 440), f"Δt = {TB} s", 48, BLUE, alpha=k1)
    text(d, (W / 2, 570), f"T = Δt : 3 ≈ {TT} s", 50, INK, alpha=k2)
    text(d, (W / 2, 635), "T: thời gian 1 vòng", 40, INK, bold=False, alpha=k2)
    eq(d, W / 2, 755, "1 vòng = 2π rad", 46, PURPLE, alpha=k3)
    eq(d, W / 2, 875, f"ω = 2π/T ≈ {WW} rad/s", 54, PURPLE, alpha=k4)
    plot(d, 5, mean_k=appear(t, 0.6, 0.4))

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    Rr = max(0.0, t - 0.5)                           # bang dinh roi moc luc t = 0,5, quay that x1 (T0 = 10,0 s)
    disc(d, theta(Rr), sector=(theta(max(0.0, Rr - 1.0)), theta(Rr)))   # quat = goc quet trong 1 s vua qua
    k0 = appear(t, 1.5, 0.4)
    text(d, (840, 580), "trong 1 s", 44, ORANGE, alpha=k0)
    if t < M[1] - 0.1:
        k = appear(t, 0.5, 0.45)
        card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
        text(d, (W / 2, 1130), f"Tần số f ≈ {FF_} Hz", 50, TEAL, alpha=k)
        text(d, (W / 2, 1210), "0,1 vòng mỗi giây", 40, TEAL, alpha=k)
        k2 = appear(t, 1.6, 0.45)
        eq(d, W / 2, 1380, f"ω ≈ {WW} rad/s", 50, PURPLE, alpha=k2)
        text(d, (W / 2, 1460), "0,63 rad mỗi giây", 40, PURPLE, alpha=k2)
    else:
        k2 = appear(t, M[1] - 0.1, 0.45)
        card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, 1100), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, 1160, 1000, 1540), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, 1270), "Chỉ có T trung bình", 46, RED, alpha=kk)
        text(d, (W / 2, 1420), "Đĩa có đều trong từng vòng?", 46, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    L1 = 780; L3 = L1 / 3; bx = 120
    yA, yB = y0 + 230, y0 + 480
    text(d, (bx, yA - 55), "1 vòng: T lệch cỡ 0,2 s", 44, RED, anchor="lm", alpha=a1)
    d.rectangle([bx, yA, bx + L1, yA + 90], fill=A((252, 165, 165), a1))
    text(d, (bx, yB - 55), "3 vòng: T lệch 0,2 s : 3", 44, BLUE, anchor="lm", alpha=a1)
    d.rectangle([bx, yB, bx + L3, yB + 90], fill=A(BLUE, a1))
    text(d, (bx + L3 + 30, yB + 45), "≈ 0,07 s", 44, BLUE, anchor="lm", alpha=a1)
    kk = appear(t, M[0] + 2.3, 0.5)
    card(d, (90, y0 + 700, 990, y0 + 1060), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 880), "✓ Đo nhiều vòng: lệch nhỏ đi", 50, GREEN, alpha=kk)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        cx, cy, rr = 400, 1110, 150                        # dia nho: vi tri cu 14 cm (dam) -> moi 7 cm (cam)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=A(GLASS, k), outline=A(GLASS_D, k), width=4)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=A((147, 197, 253), k))
        d.rectangle([cx + 140 - 16, cy - 11, cx + 140 + 16, cy + 11], fill=A((203, 207, 218), k), outline=A(NAVY, k), width=4)
        d.rectangle([cx + 70 - 16, cy - 11, cx + 70 + 16, cy + 11], fill=A(TAPE, k))
        arrow(d, (cx + 136, cy + 44), (cx + 76, cy + 44), A(NAVY, k), w=5, head=16)
        d.line([(cx + 140, cy - 14), (640, 1040)], fill=A(NAVY, k), width=3)
        text(d, (650, 1040), "14 cm", 40, NAVY, anchor="lm", alpha=k)
        d.line([(cx + 70, cy + 14), (640, 1180)], fill=A(TAPE, k), width=3)
        text(d, (650, 1180), "7 cm", 40, TAPE, anchor="lm", alpha=k)
        kh = appear(t, M[0] + 2.8, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Mỗi điểm quay 1 vòng hết bao lâu?", 40, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Đo n vòng hết Δt: T = Δt : n",
             "Dời băng dính như hình:\ntốc độ góc đổi thế nào?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    tf = do["M"][1]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for k in (1, 2):                                       # bang dinh qua moc (lan 1, vong 1 va 2)
        cs.append((do["t0"] + TA + 10.0 * k / S1, "tick"))
    cs.append((do["t0"] + T_STOP1, "tap"))
    for a, bb in TRIALS[1:]: cs.append((do["t0"] + tf + (bb - TRIALS[0][1]) / S2, "tap"))
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-trondeu-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động tròn đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đĩa xoay lò vi sóng", draw=s_hook, tail=0.5, caps=[
   ("Mốc đỏ đứng yên.", 2.6),
   ("Dừng video, chọn câu trả lời.", 6.3)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bấm đồng hồ khi băng dính qua mốc.", 6.6),
   ("Làm thêm 4 lần như vậy.", 5.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Trung bình, rồi chia 3.", 5.7)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Mỗi giây quay bao nhiêu?", 3.2),
   ("Còn điều chưa biết.", 4.0)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Chỉ đo 1 vòng, được không?", 5.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
