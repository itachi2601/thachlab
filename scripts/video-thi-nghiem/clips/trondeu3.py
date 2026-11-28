# Clip: tn-l10-trondeu-03 - Do chu ki dia xoay lo vi song (3 vong x 5 lan), suy ra f va omega (1/11/2026; cong moi 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trondeu-03.json:
#   tham_so: T0 = 10,0 s (mac dinh, mien 8-12 s), r = 0,14 m (bang dinh cach tam 14,0 cm), n = 3 vong, dt sai so 0,2 s.
#   so_lieu_mau: dt 3 vong = 30,2 / 29,8 / 30,1 / 30,4 / 29,9 s ; ghi_chu: TB 30,08 s -> T = 10,027 s ; rut_ra: T ~ 10,03 s,
#   f ~ 0,100 Hz, omega ~ 0,627 rad/s. Loi hay gap (kho): nham f voi omega.
# Dia ve quay DEU dung T0 = 10,0 s: goc bang dinh theta = 2.pi.R/T0 (R = thoi gian that, s), bang dinh qua moc khi R = 10k.
#   Dong ho bam lech tay (moi lan bam <= 0,2 s) cho ra dung so kho: lan 1 bat dau 0 dung 30,2 ; lan 2: 40 -> 69,8 ;
#   lan 3: 80 -> 110,1 ; lan 4: 119,8 -> 150,2 ; lan 5: 160,1 -> 190,0.
# Du doan (27/11): hop exp + Bam xem cua bai da ghi T, f, omega va "do nhieu vong giam sai so" nen KHONG hoi gia tri omega.
#   Hoi: 3 vong ~ 30 s, bang dinh dang o moc -> sau 5 s o dau? Dap an: doi dien moc (nua vong, vi T ~ 10 s). Bai khong hoi.
# Cau chot: dia khac 3 vong het 24 s (T0 = 8 s, trong mien tham_so 8-12) -> omega = 2.pi/8 ~ 0,79 rad/s. Dap so khong hien.
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
    text(d, (CX + 34, CY - RD - 22), "mốc", 55, RED, anchor="lm")
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
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def watch_card(d, val, sub=None):
    card(d, (680, 320, 1020, 540), fill=NAVY, r=26)
    text(d, (850, 372), "đồng hồ", 55, (220, 225, 240), bold=False)
    text(d, (850, 465), vn(val, 1) + " s", 66, WHITE)

# ---------------- do thi cham dt ----------------
def XV(v): return 240 + (v - 29.6) / 1.0 * 720
ROWY = [1180 + 60 * i for i in range(5)]; AXY = 1475
def plot(d, n, title=True):
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    if title: text(d, (W / 2, 1085), "Δt: thời gian 3 vòng (s)", 55, INK)
    for v in (29.8, 30.0, 30.2, 30.4):
        d.line([(XV(v), ROWY[0] - 30), (XV(v), AXY)], fill=(240, 236, 228), width=2)
        d.line([(XV(v), AXY), (XV(v), AXY + 12)], fill=NAVY, width=3)
        text(d, (XV(v), AXY + 50), vn(v, 1), 55, INK, bold=False)
    d.line([(XV(29.6) + 60, AXY), (XV(30.6), AXY)], fill=NAVY, width=4)
    for i in range(5):
        text(d, (66, ROWY[i]), f"Lần {i + 1}", 55, MUTED if i >= n else INK, bold=False, anchor="lm")
    for i in range(n):
        x, y = XV(DT[i]), ROWY[i]
        dot(d, x, y, 15, BLUE, WHITE)
        text(d, (x + 28, y), vn(DT[i], 1), 55, BLUE, anchor="lm")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    disc(d, 0.0, rline=True)
    text(d, (850, 420), "băng dính", 55, DORANGE)
    text(d, (850, 500), "cách tâm", 55, INK)
    text(d, (850, 570), "14,0 cm", 55, INK)
    text(d, (850, 760), "cốc nước", 55, (37, 99, 235))
    d.line([(CX + 64, CY + 14), (700, 752)], fill=(37, 99, 235), width=3)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("3 vòng hết khoảng 30 s.", "Sau 5 s, băng dính ở đâu?")):
        text(d, (W / 2, y0 + 190 + j * 85), s1, 60, PURPLE if j == 1 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
TA, S1, S2 = 0.6, 10.0, 40.0          # bam lan 1 luc t = 0,6 ; tua x10 (lan 1), x40 (lan 2-5)
T_STOP1 = TA + TRIALS[0][1] / S1
def R_of(t, tf):
    if t <= T_STOP1: return (t - TA) * S1
    if t <= tf: return TRIALS[0][1]
    return TRIALS[0][1] + (t - tf) * S2

def watch(R):
    """-> (lan j (0-based, -1 chua bam), so dong ho (s), so vong lan 1, so cham da co)."""
    j = -1
    for i, (a, b) in enumerate(TRIALS):
        if R >= a - 1e-9: j = i
    if j < 0: return -1, 0.0, 0, 0
    a, b = TRIALS[j]
    val = math.floor((min(R, b) - a) * 10 + 1e-6) / 10
    laps = min(3, int(math.floor((R - a) / T0 + 1e-9))) if j == 0 else 0
    ndot = sum(1 for (_, bb) in TRIALS if R >= bb - 1e-9)
    return j, val, laps, ndot

def s_do(img, d, t, sc):
    M = sc["M"]; tf = M[1]
    R = R_of(t, tf); j, val, laps, ndot = watch(R)
    frozen = T_STOP1 < t <= tf
    disc(d, theta(R), late=theta(TRIALS[0][1] - 30.0) if frozen and t > T_STOP1 + 0.3 else 0.0)
    watch_card(d, val)
    text(d, (850, 600), f"Lần {max(j, 0) + 1}", 58, INK)
    if j <= 0: text(d, (850, 675), f"vòng: {laps}", 58, BLUE)
    if frozen and t > T_STOP1 + 0.3:                       # o phong to x3 quanh moc (dung hinh)
        kq = appear(t, T_STOP1 + 0.3, 0.4)
        zc = (CX + 6, CY - R_CM * PXCM + 10); hz = 40
        z = img.crop((int(zc[0] - hz), int(zc[1] - hz), int(zc[0] + hz), int(zc[1] + hz))).resize((276, 276), Image.LANCZOS)
        zx, zy = CX - 138, CY - 120
        if kq > 0.05:
            m = Image.new("L", z.size, int(255 * kq)); img.paste(z, (zx, zy), m)
            d.rectangle([zx, zy, zx + 276, zy + 276], outline=A(RED, kq), width=5)
            text(d, (zx + 262, zy + 34), "×3", 55, RED, anchor="rm", alpha=kq)
            d.rectangle([zc[0] - hz, zc[1] - hz, zc[0] + hz, zc[1] + hz], outline=A(RED, kq), width=3)
            lw = tw(d, "qua mốc", F(55)) + 40
            card(d, (CX - lw / 2 + 10, zy + 286, CX + lw / 2 + 10, zy + 360), fill=A(WHITE, kq), outline=A(RED, kq), r=30, w=4)
            text(d, (CX + 10, zy + 323), "qua mốc", 55, RED, alpha=kq)
        card(d, (690, 740, 1010, 820), fill=A((254, 242, 242), kq), outline=A(RED, kq), r=34, w=3)
        text(d, (850, 780), "bấm trễ", 55, RED, alpha=kq)
        text(d, (850, 880), "≈ 0,2 s", 55, RED, alpha=kq)
    elif not frozen:
        sp = "tua ×" + str(int(S1 if t <= T_STOP1 else S2))
        cw = tw(d, sp, F(55)) + 44
        card(d, (850 - cw / 2, 740, 850 + cw / 2, 820), fill=(241, 245, 249), outline=GLASS_D, r=34, w=3)
        text(d, (850, 780), sp, 55, MUTED)
    plot(d, ndot)

# ---------------- canh 3: Dap an (sau 5 s: doi dien moc) ----------------
TD0, SD = 0.5, 2.0                      # quay that 5 s, tua x2 (2,5 s canh)
def s_dapan(img, d, t, sc):
    M = sc["M"]
    R = clamp((t - TD0) * SD, 0.0, 5.0)
    th = theta(R)
    disc(d, th, sector=(0.0, th) if R > 0.05 else None)
    watch_card(d, R)
    sp = "tua ×2"; cw = tw(d, sp, F(55)) + 44
    card(d, (850 - cw / 2, 740, 850 + cw / 2, 820), fill=(241, 245, 249), outline=GLASS_D, r=34, w=3)
    text(d, (850, 780), sp, 55, MUTED)
    ka = appear(t, M[1], 0.45)
    if ka < 1: plot(d, 5, title=False)
    if ka <= 0: return
    yk = 1030 + (1 - ka) * 30
    card(d, (40, yk, 1040, yk + 555), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
    pill(d, W / 2, yk + 75, "ĐÁP ÁN", NAVY, ka)
    text(d, (W / 2, yk + 210), "đối diện mốc", 64, BLUE, alpha=ka)
    text(d, (W / 2, yk + 330), "1 vòng ≈ 30 s : 3 = 10 s", 58, DGREEN, alpha=ka)
    text(d, (W / 2, yk + 430), "5 s: nửa vòng", 58, DGREEN, alpha=ka)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    Rr = max(0.0, t - 0.5)                           # quay that x1 (T0 = 10,0 s)
    disc(d, theta(Rr), sector=(theta(max(0.0, Rr - 1.0)), theta(Rr)))   # quat = goc quet trong 1 s vua qua
    k1 = appear(t, 0.4, 0.4)
    card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k1), outline=A(GREEN, k1), w=6)
    pill(d, W / 2, 1100, "RÚT RA", GREEN, k1)
    text(d, (W / 2, 1230), f"chu kì T = Δt : 3 ≈ {TT} s", 58, INK, alpha=k1)
    k2 = appear(t, M[1], 0.4)
    text(d, (W / 2, 1345), f"tần số f = 1/T ≈ {FF_} Hz", 58, TEAL, alpha=k2)
    eq(d, W / 2, 1460, f"tốc độ góc ω = 2π/T ≈ {WW} rad/s", 55, PURPLE, alpha=k2)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
    q = "ω ≈ 0,100 rad/s"
    ks = clamp((t - M[1]) / 0.4); yy = 450
    lw = eq(d, W / 2, yy, q, 60, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    kk = appear(t, M[1], 0.4)
    c = (540, 800); R = 190
    g = ease(clamp((t - M[1]) / 1.4))
    d.ellipse([c[0] - R, c[1] - R, c[0] + R, c[1] + R], fill=A(GLASS, a1), outline=A(GLASS_D, a1), width=5)
    if g > 0.01:
        d.pieslice([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -90, -90 + 36 * g, fill=A((254, 215, 170), kk), outline=A(ORANGE, kk), width=4)
    d.line([c, (c[0], c[1] - R)], fill=A(NAVY, a1), width=4)
    text(d, (W / 2, 545), "0,100 là f", 58, DGREEN, alpha=kk)
    text(d, (850, 700), "0,1 vòng", 55, TEAL, alpha=kk)
    text(d, (230, 700), "trong 1 s", 55, DORANGE, alpha=kk)
    eq(d, W / 2, 1065, f"ω = 2πf ≈ {WW} rad/s", 58, PURPLE, alpha=kk)
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 > 0:
        yk = 1150 + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 420), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 200), "Chỉ có T trung bình", 58, INK, alpha=k3)
        text(d, (W / 2, yk + 300), "Đĩa có đều trong từng vòng?", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
T_END = 8.0                                 # dia khac: 3 vong het 24 s (T0 = 8 s, trong mien kho 8-12 s)
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    th = 2 * math.pi * max(0.0, t - 0.4) * 3 / T_END     # tua x3
    disc(d, th)
    card(d, (680, 320, 1020, 540), fill=A(NAVY, k), r=26)
    text(d, (850, 372), "3 vòng", 55, (220, 225, 240), bold=False, alpha=k)
    text(d, (850, 465), "24,0 s", 66, WHITE, alpha=k)
    text(d, (850, 640), "đĩa khác", 58, INK, alpha=k)
    card(d, (40, 1030, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1215), "3 vòng hết 24 s.", 60, INK, alpha=k)
    eq(d, W / 2, 1310, "Tốc độ góc ω khoảng bao nhiêu?", 58, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    tf = do["M"][1]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for k in (1, 2):                                       # bang dinh qua moc (lan 1, vong 1 va 2)
        cs.append((do["t0"] + TA + 10.0 * k / S1, "tick"))
    cs.append((do["t0"] + T_STOP1, "tap"))
    for a, bb in TRIALS[1:]: cs.append((do["t0"] + tf + (bb - TRIALS[0][1]) / S2, "tap"))
    cs += [(da["t0"] + TD0 + 5.0 / SD, "tick"), (da["t0"] + da["M"][1], "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-trondeu-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động tròn đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đĩa xoay lò vi sóng", draw=s_hook, tail=0.2, caps=[
   ("3 vòng hết khoảng 30 s.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bấm đồng hồ khi băng dính qua mốc.", 4.8),
   ("Làm thêm 4 lần như vậy.", 4.1)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đĩa quay 5 s từ mốc.", 3.4),
   ("Đáp án: đối diện mốc.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Trung bình, rồi chia 3.", 3.0),
   ("Mỗi giây quay 0,63 rad.", 3.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("0,100 là ω?", 3.0),
   ("Không, đó là f.", 3.0),
   ("Chỉ có T trung bình.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
