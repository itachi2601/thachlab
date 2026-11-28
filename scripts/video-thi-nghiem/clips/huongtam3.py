# Clip: tn-l10-huongtam-03 - Nut cao su quay tren dau ong, qua nang M treo duoi: so Mg voi m.v^2/r (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-huongtam-03.json:
#   tham_so: m = 0,050 kg, r = 0,50 m, M = 0,10 / 0,20 / 0,30 kg (bo qua nang 3 x 0,10 kg), g = 9,8 (gia_thiet).
#   so_lieu_mau: Mg = 0,98 / 1,96 / 2,94 N ; t10 = 10,2 / 7,0 / 5,7 s ; m.v^2/r = 0,95 / 2,01 / 3,04 N.
# Du doan (27/11, cong moi): bang + o Quan sat cua bai da ghi "qua nang lon -> quay nhanh hon" va cot t10, nen KHONG hoi t10.
#   Hoi: giu qua nang M = 0,10 kg, quay nhanh hon -> kep di len hay xuong? Dap an: LEN (can m.v^2/r > Mg, luc cang khong du
#   giu nut tren vong cu -> nut ra xa, r tang, keo day len; kho hien_tuong_hay_sai #1 ghi hien tuong nay).
# Khong giai san cau "Doc so lieu" (khop toi muc nao, sai so): clip chi ve cot Mg canh cot m.v^2/r, KHONG ghi so, KHONG neu %.
# Bay: do r tu tay chu khong tu truc ong (kho hien_tuong_hay_sai #2).
# Cau chot: M = 0,40 kg (trong mien tham_so 0,05-0,5), kep dung yen: m.v^2/r ~ Mg = 3,92 N (dap so khong hien).
from engine import *

MS = [0.10, 0.20, 0.30]; MG = [0.98, 1.96, 2.94]; T10 = [10.2, 7.0, 5.7]; FHT = [0.95, 2.01, 3.04]
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
SPD = 2.5                                          # tua nhanh x2,5 khi bam gio (lan 3: 53 do/khung < 60)
RUBBER = (234, 88, 12); TUBE = (203, 213, 225); TUBE_D = (71, 85, 105); BLOCK = (148, 163, 184)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

_TI = {}
def TI(size):                                      # Times Bold Italic cho pi
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

TOKR = re.compile(r"(_\{[^}]*\}|\^\{[^}]*\}|π)")
def eqr(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """chu co chi so duoi/tren (>= 55 px) va pi Times nghieng."""
    segs = []
    for p in [p for p in TOKR.split(s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], F(max(55, int(size * 0.8))), size * 0.26))
        elif p.startswith("^{"): segs.append((p[2:-1], F(max(55, int(size * 0.8))), -size * 0.34))
        elif p == "π": segs.append((p, TI(size * 1.12), 0))
        else: segs.append((p, F(size), 0))
    tot = sum(tw(d, t, f) for t, f, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for t, f, dy in segs:
        dtext(d, (x, cy + dy), t, f, color, alpha, "lm"); x += tw(d, t, f)
    return tot

def dashed(d, p, q, color, w=4, on=14, off=10):
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    if L < 1: return
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L; s = 0.0
    while s < L:
        e = min(L, s + on)
        d.line([(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)], fill=color, width=w); s = e + off

# ---------------- chung ----------------
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

# ---------------- dung cu nhin nghieng ----------------
TX, TT, TB = 380, 520, 740                         # truc ong: dinh, day
RX, RY = 270, 105                                  # quy dao (r = 0,50 m -> 270 px), nhin nghieng
GAP = 30                                           # kep cach mieng duoi ong (px) khi r dung 0,50 m
def nut_xy(ph, rx=RX): return (TX + rx * math.cos(ph), TT + RY * rx / RX * math.sin(ph))

def rig(d, ph, nblk, ften=None, r_lab="r = 0,50 m", trail=0.0, lift=0.0):
    """lift (px): day bi keo len -> kep, qua nang len ; r tang dung bang lift (day khong gian)."""
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    rx = RX + lift
    pts = [nut_xy(2 * math.pi * i / 120, rx) for i in range(121)]
    for i in range(0, 120, 2):                       # quy dao net dut
        d.line([pts[i], pts[i + 1]], fill=(148, 163, 184), width=3)
    x, y = nut_xy(ph, rx)
    behind = math.sin(ph) < 0
    def nut():
        d.line([(TX, TT), (x, y)], fill=NAVY, width=4)
        d.rounded_rectangle([x - 22, y - 18, x + 22, y + 18], radius=7, fill=RUBBER, outline=(124, 45, 18), width=3)
        if ften:                                     # luc cang: chi VAO truc ong (tam quy dao), doc theo day
            ux, uy = TX - x, TT - y
            nn = math.hypot(ux, uy); ux, uy = ux / nn, uy / nn
            L = min(40 * ften, nn - 60)
            x0, y0 = x + ux * 26, y + uy * 26
            arrow(d, (x0, y0), (x0 + ux * L, y0 + uy * L), RED, w=7, head=18)
    if trail:                                        # vet mo sau nut (chong giat khi quay nhanh)
        for i in range(4, 0, -1):
            gx, gy = nut_xy(ph + trail * i / 4, rx)
            d.rounded_rectangle([gx - 20, gy - 16, gx + 20, gy + 16], radius=7, fill=A(RUBBER, 0.12 + 0.06 * (4 - i)))
    if behind: nut()
    d.rectangle([TX - 14, TT, TX + 14, TB], fill=TUBE, outline=TUBE_D, width=4)       # ong
    if not behind: nut()
    yk = TB + GAP - lift
    d.line([(TX, TB), (TX, yk + 50)], fill=NAVY, width=4)
    d.rectangle([TX - 16, yk, TX + 16, yk + 18], fill=ORANGE)                         # kep
    bh = 40
    for i in range(nblk):
        yb = yk + 50 + i * bh
        d.rounded_rectangle([TX - 42, yb, TX + 42, yb + bh - 4], radius=6, fill=BLOCK, outline=TUBE_D, width=3)
    if r_lab:
        d.line([(TX, 330), (TX + rx, 330)], fill=INK, width=3)
        d.line([(TX, 316), (TX, 344)], fill=INK, width=3); d.line([(TX + rx, 316), (TX + rx, 344)], fill=INK, width=3)
        text(d, (TX + rx / 2, 295), r_lab, 55, INK)

def ph_at(R, T):                                   # goc nut sau thoi gian that R, chu ki T
    return math.pi / 2 - 2 * math.pi * R / T

# ---------------- bang so lieu (chi M, Mg, t10 nhu bang bai) ----------------
COLX = [200, 540, 880]
def table(d, nrow):
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    eqr(d, COLX[0], 1110, "M (kg)", 58, INK)
    eqr(d, COLX[1], 1110, "Mg (N)", 58, DRED)
    eqr(d, COLX[2], 1110, "t_{10} (s)", 58, BLUE)
    d.line([(70, 1170), (1010, 1170)], fill=LIGHT, width=3)
    for i in range(3):
        y = 1260 + i * 110
        if i < nrow[0]:
            text(d, (COLX[0], y), vn(MS[i], 2), 58, INK)
            text(d, (COLX[1], y), vn(MG[i], 2), 58, DRED)
        if i < nrow[1]:
            text(d, (COLX[2], y), vn(T10[i], 1), 58, BLUE)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, ph_at(t, T10[0] / 10), 1, r_lab=None)
    text(d, (450, TB + GAP + 9), "kẹp", 55, DORANGE, anchor="lm")
    text(d, (470, TB + GAP + 75), "quả nặng", 55, INK, anchor="lm")
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("Giữ nguyên quả nặng,", "quay nút nhanh hơn.", "Kẹp đi lên hay xuống?")):
        text(d, (W / 2, y0 + 165 + j * 75), s1, 58, PURPLE if j == 2 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
TR = [0.4, 4.6, 7.5]                               # luc bat dau bam gio tung lan
def trial(t):
    """-> (lan j, thoi gian that R da quay, so dong ho, so vong, da xong?)"""
    j = 0
    for i, s in enumerate(TR):
        if t >= s: j = i
    R = max(0.0, (t - TR[j]) * SPD)
    done = R >= T10[j]
    val = T10[j] if done else math.floor(R * 10 + 1e-6) / 10
    laps = 10 if done else int(math.floor(R / (T10[j] / 10) + 1e-9))
    return j, R, val, laps, done

def s_do(img, d, t, sc):
    j, R, val, laps, done = trial(t)
    ph = ph_at(R, T10[j] / 10)
    w_frame = 2 * math.pi / (T10[j] / 10) * SPD / 30 if not done else 0.0
    rig(d, ph, j + 1, ften=MG[j], trail=w_frame)
    card(d, (700, 380, 1010, 590), fill=NAVY, r=26)
    eqr(d, 855, 430, "t_{10}", 55, (220, 225, 240))
    text(d, (855, 525), vn(val, 1) + " s", 64, WHITE)
    text(d, (855, 650), f"vòng: {laps}/10", 55, BLUE)
    text(d, (855, 725), "M = " + vn(MS[j], 2) + " kg", 55, INK)
    arrow(d, (690, 810), (750, 810), RED, w=7, head=20)
    text(d, (765, 810), "lực căng", 55, DRED, anchor="lm")
    cw = tw(d, "tua ×2,5", F(55)) + 40
    card(d, (855 - cw / 2, 880, 855 + cw / 2, 960), fill=(241, 245, 249), outline=TUBE_D, r=30, w=3)
    text(d, (855, 920), "tua ×2,5", 55, MUTED)
    table(d, [j + 1, j + (1 if done else 0)])

# ---------------- canh 3: Dap an (quay nhanh hon, giu M = 0,10 kg) ----------------
UP = 1.4                                           # quay nhanh x1,4
def lift_at(t): return GAP * ease(clamp((t - 1.2) / 1.8))
def s_dapan(img, d, t, sc):
    M = sc["M"]
    T0 = T10[0] / 10
    sp = 1 + (UP - 1) * ease(clamp((t - 0.4) / 0.8))
    ph = math.pi / 2 - 2 * math.pi * (t * SPD * (1 + (UP - 1) * clamp((t - 0.4) / 0.8) / 2)) / T0
    lf = lift_at(t)
    rig(d, ph, 1, ften=MG[0], r_lab="r tăng" if lf > GAP * 0.6 else None, trail=2 * math.pi / T0 * SPD * sp / 30, lift=lf)
    text(d, (450, TB + GAP - lf + 9), "kẹp", 55, DORANGE, anchor="lm")
    cw = tw(d, "tua ×2,5", F(55)) + 40
    card(d, (855 - cw / 2, 880, 855 + cw / 2, 960), fill=(241, 245, 249), outline=TUBE_D, r=30, w=3)
    text(d, (855, 920), "tua ×2,5", 55, MUTED)
    ka = appear(t, M[1], 0.45)
    if ka <= 0: return
    yk = 1085 + (1 - ka) * 30
    card(d, (40, yk, 1040, yk + 330), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
    pill(d, W / 2, yk + 70, "ĐÁP ÁN", NAVY, ka)
    text(d, (W / 2, yk + 215), "kẹp đi lên, r tăng", 64, BLUE, alpha=ka)

# ---------------- canh 4: Rut ra ----------------
BX0, BPX = 260, 230                                # cot luc: 1 N -> 230 px
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.4, 0.45)
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    pill(d, W / 2, 340, "RÚT RA", GREEN, k1)
    text(d, (W / 2, 480), "Lực căng = Mg,", 60, DRED, alpha=k1)
    text(d, (W / 2, 570), "đóng vai lực hướng tâm", 60, DRED, alpha=k1)
    # nut nhin tu tren: luc cang chi vao tam (truc ong)
    cx, cy = 300, 800
    dot(d, cx, cy, 14, NAVY); text(d, (cx, cy + 65), "trục ống", 55, NAVY, alpha=k1)
    d.rounded_rectangle([780, cy - 22, 830, cy + 22], radius=8, fill=RUBBER, outline=(124, 45, 18), width=3)
    d.line([(cx, cy), (780, cy)], fill=NAVY, width=4)
    g = clamp((t - 0.6) / 2.0)
    if g > 0: arrow(d, (770, cy - 40), (770 - 330 * g, cy - 40), A(RED, k1), w=8, head=24)
    # cot Mg canh cot m.v^2/r (khong ghi so)
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    eqr(d, 300, 1080, "Mg (N)", 58, DRED, alpha=k1)
    eqr(d, 740, 1080, "m·v^{2}/r (N)", 58, PURPLE, alpha=k1)
    text(d, (300, 1150), "trọng lượng", 55, DRED, alpha=k1)
    text(d, (740, 1150), "lực hướng tâm", 55, PURPLE, alpha=k1)
    text(d, (130, 1215), "số quả", 55, INK, anchor="lm", alpha=k1)
    ga = clamp((t - 0.4) / 2.0); gb = clamp((t - M[1]) / 2.0)
    for i in range(3):
        y = 1270 + i * 105
        text(d, (150, y + 18), str(i + 1), 58, INK, alpha=k1)
        if ga > 0: d.rectangle([BX0, y - 10, BX0 + MG[i] * BPX * ga, y + 22], fill=RED)
        if gb > 0: d.rectangle([BX0, y + 26, BX0 + FHT[i] * BPX * gb, y + 58], fill=PURPLE)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
    q = "Đo r từ bàn tay"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(58)); yy = 460
    text(d, (W / 2, yy), q, 58, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    ox, otop, obot = 300, 700, 1120                 # ong dung, tay cam o duoi, nut ngang dinh ong
    nx = ox + 520
    d.rectangle([ox - 14, otop, ox + 14, obot], fill=A(TUBE, a1), outline=A(TUBE_D, a1), width=4)
    d.line([(ox, otop), (nx, otop)], fill=A(NAVY, a1), width=4)
    d.rounded_rectangle([nx - 22, otop - 18, nx + 22, otop + 18], radius=7, fill=A(RUBBER, a1), outline=A((124, 45, 18), a1), width=3)
    hy = 1030
    d.ellipse([ox - 52, hy - 34, ox + 52, hy + 34], fill=A((253, 186, 116), a1), outline=A((154, 52, 18), a1), width=4)
    text(d, (ox - 70, hy), "tay", 55, INK, anchor="rm", alpha=a1)
    kw = 1 - ks
    dashed(d, (ox + 50, hy - 20), (nx - 24, otop + 20), A(DRED, a1 * max(kw, 0.25)), w=6)
    kk = appear(t, M[1], 0.5)
    if kk > 0:
        gl = ease(clamp((t - M[1]) / 1.2))
        xe = ox + (nx - ox) * gl
        d.line([(ox, otop - 70), (xe, otop - 70)], fill=A(GREEN, kk), width=6)
        d.line([(ox, otop - 92), (ox, otop - 48)], fill=A(GREEN, kk), width=6)
        if gl > 0.98: d.line([(nx, otop - 92), (nx, otop - 48)], fill=A(GREEN, kk), width=6)
        dashed(d, (ox, otop - 100), (ox, obot + 30), A(GREEN, kk), w=4)
        text(d, ((ox + nx) / 2, otop - 120), "r", 60, DGREEN, alpha=kk)
        text(d, (W / 2, 1270), "từ trục ống tới tâm nút", 58, DGREEN, alpha=kk)
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 > 0:
        yk = 1180 + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 200), "Mới thử một bán kính", 58, INK, alpha=k3)
        text(d, (W / 2, yk + 290), "r = 0,50 m", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    rig(d, ph_at(t, T10[2] / 10 * 1.4), 4)
    text(d, (470, TB + GAP + 125), "M = 0,40 kg", 55, INK, anchor="lm", alpha=k)
    card(d, (40, 1030, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1215), "Kẹp đứng yên.", 60, INK, alpha=k)
    eqr(d, W / 2, 1310, "m·v^{2}/r khoảng bao nhiêu?", 60, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for j in range(3):
        cs.append((do["t0"] + TR[j], "tap"))
        cs.append((do["t0"] + TR[j] + T10[j] / SPD, "tick"))
    cs += [(da["t0"] + da["M"][1], "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-huongtam-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực hướng tâm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nút quay trên ống", draw=s_hook, tail=0.2, caps=[
   ("Nhìn nghiêng.", 2.3),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bấm giờ 10 vòng, giữ kẹp yên.", 4.2),
   ("Thêm quả nặng, đo lại.", 5.2)]),
 dict(key="dapan", title="Quay nhanh hơn", draw=s_dapan, tail=0.3, caps=[
   ("Giữ M, quay nhanh hơn.", 3.0),
   ("Đáp án: kẹp đi lên, r tăng.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Lực căng = Mg, đóng vai lực hướng tâm.", 4.2),
   ("So Mg với m·v²/r.", 3.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đo r từ bàn tay?", 3.2),
   ("Đo từ trục ống.", 3.0),
   ("Mới thử một bán kính.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
