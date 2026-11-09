# Clip: tn-l10-huongtam-03 - Nut cao su quay tren dau ong, qua nang M treo duoi: so Mg voi m.v^2/r (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-huongtam-03.json:
#   tham_so: m = 0,050 kg, r = 0,50 m, M = 0,10 / 0,20 / 0,30 kg (bo qua nang 3 x 0,10 kg), g = 9,8 (gia_thiet).
#   so_lieu_mau: Mg = 0,98 / 1,96 / 2,94 N ; t10 = 10,2 / 7,0 / 5,7 s ; m.v^2/r = 0,95 / 2,01 / 3,04 N.
# Du doan (K10: chi cau hoi + hinh): M 0,10 -> 0,30 kg (gap 3), giu kep dung yen: t10 doi the nao?
#   Dap an: giam, nhung van con hon mot nua (10,2 -> 5,7 s). Nhieu (khung): tang ; khong doi ; con khoang 1/3.
# Khong giai san cau "Doc so lieu" ngay sau hop (khop toi muc nao, sai so lon nhat tu dau): clip KHONG neu %, KHONG ban sai so.
# Bay: do r tu tay chu khong tu truc ong (kho hien_tuong_hay_sai).
# Cau chot: M = 0,40 kg (chua tung hien, trong mien tham_so 0,05-0,5): m.v^2/r ~ Mg = 3,92 N.
from engine import *

MS = [0.10, 0.20, 0.30]; MG = [0.98, 1.96, 2.94]; T10 = [10.2, 7.0, 5.7]; FHT = [0.95, 2.01, 3.04]
SPD = 3.0                                          # tua nhanh x3 khi bam gio
RUBBER = (234, 88, 12); TUBE = (203, 213, 225); TUBE_D = (71, 85, 105); BLOCK = (148, 163, 184)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

_TI = {}
def TI(size):                                      # Times Bold Italic cho pi
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

TOKR = re.compile(r"(_\{[^}]*\}|\^\{[^}]*\}|π)")
def eqr(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """chu co chi so duoi/tren (>= 40 px) va pi Times nghieng."""
    segs = []
    for p in [p for p in TOKR.split(s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], F(max(40, int(size * 0.7))), size * 0.26))
        elif p.startswith("^{"): segs.append((p[2:-1], F(max(40, int(size * 0.7))), -size * 0.34))
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

# ---------------- dung cu nhin nghieng ----------------
TX, TT, TB = 380, 520, 760                         # truc ong: dinh, day
RX, RY = 270, 62                                   # quy dao (r = 0,50 m -> 270 px), nhin nghieng
def nut_xy(ph): return (TX + RX * math.cos(ph), TT + RY * math.sin(ph))

def rig(d, ph, nblk, f_k=1.0, ften=None, r_bar=True, trail=0.0):
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    pts = [nut_xy(2 * math.pi * i / 120) for i in range(121)]
    for i in range(0, 120, 2):                       # quy dao net dut
        d.line([pts[i], pts[i + 1]], fill=(148, 163, 184), width=3)
    x, y = nut_xy(ph)
    behind = math.sin(ph) < 0
    def nut():
        d.line([(TX, TT), (x, y)], fill=NAVY, width=4)
        d.rounded_rectangle([x - 22, y - 18, x + 22, y + 18], radius=7, fill=RUBBER, outline=(124, 45, 18), width=3)
        if ften:                                     # luc cang chi vao truc ong, chieu nghieng (phuong sau-truoc thu RY/RX)
            ux, uy = -math.cos(ph), -math.sin(ph) * RY / RX
            nn = math.hypot(ux, uy); ux, uy = ux / nn, uy / nn   # do dai co dinh 62.Mg, chi huong theo phoi canh
            L = 62 * ften; x0, y0 = x + ux * 26, y + uy * 26
            arrow(d, (x0, y0), (x0 + ux * L, y0 + uy * L), RED, w=7, head=18)
    if trail:                                        # vet mo sau nut (chong giat khi quay nhanh)
        for i in range(4, 0, -1):
            gx, gy = nut_xy(ph + trail * i / 4)
            d.rounded_rectangle([gx - 20, gy - 16, gx + 20, gy + 16], radius=7, fill=A(RUBBER, 0.12 + 0.06 * (4 - i)))
    if behind: nut()
    d.rectangle([TX - 14, TT, TX + 14, TB], fill=TUBE, outline=TUBE_D, width=4)       # ong
    if not behind: nut()
    d.line([(TX, TB), (TX, TB + 70)], fill=NAVY, width=4)
    d.rectangle([TX - 16, TB + 16, TX + 16, TB + 34], fill=ORANGE)                       # kep
    bh = 44
    for i in range(nblk):
        yb = TB + 70 + i * bh
        d.rounded_rectangle([TX - 42, yb, TX + 42, yb + bh - 4], radius=6, fill=BLOCK, outline=TUBE_D, width=3)
    if r_bar:
        d.line([(TX, 330), (TX + RX, 330)], fill=INK, width=3)
        d.line([(TX, 316), (TX, 344)], fill=INK, width=3); d.line([(TX + RX, 316), (TX + RX, 344)], fill=INK, width=3)
        text(d, (TX + RX / 2, 300), "r = 0,50 m", 40, INK)

def ph_at(R, T):                                   # goc nut sau thoi gian that R, chu ki T (quay nguoc kim, nhin tu tren)
    return math.pi / 2 - 2 * math.pi * R / T

# ---------------- bang so lieu ----------------
COLX = [175, 410, 640, 880]
def table(d, nrow, fcol=0.0, hi=0.0):
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    if hi > 0:
        for cx in (COLX[1], COLX[3]):
            d.rounded_rectangle([cx - 110, 1060, cx + 110, 1560], radius=20, fill=A((254, 243, 199), hi))
    eqr(d, COLX[0], 1110, "M (kg)", 44, INK)
    eqr(d, COLX[1], 1110, "Mg (N)", 44, RED)
    eqr(d, COLX[2], 1110, "t_{10} (s)", 44, BLUE)
    if fcol > 0: eqr(d, COLX[3], 1110, "m·v^{2}/r (N)", 44, PURPLE, alpha=fcol)
    d.line([(70, 1160), (1010, 1160)], fill=LIGHT, width=3)
    for i in range(3):
        y = 1240 + i * 110
        if i < nrow[0]:
            text(d, (COLX[0], y), vn(MS[i], 2), 46, INK)
            text(d, (COLX[1], y), vn(MG[i], 2), 46, RED)
        if i < nrow[1]:
            text(d, (COLX[2], y), vn(T10[i], 1), 46, BLUE)
        if fcol > 0:
            text(d, (COLX[3], y), vn(FHT[i], 2), 46, PURPLE, alpha=appear(fcol * 3, i * 0.7 + 0.5, 0.5) if fcol < 1 else 1.0)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    ph = ph_at(t, T10[0] / 10)
    rig(d, ph, 1, ften=MG[0])
    x, y = nut_xy(math.pi / 2)
    text(d, (850, 440), "nút cao su", 44, RUBBER)
    text(d, (850, 500), "m = 0,050 kg", 40, INK)
    text(d, (470, TB + 25), "kẹp", 40, ORANGE, anchor="lm")
    text(d, (470, TB + 92), "quả nặng", 40, INK, anchor="lm")
    text(d, (470, TB + 150), "M = 0,10 kg", 40, INK, anchor="lm")
    text(d, (470, TB + 202), "trọng lượng Mg", 40, RED, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=33)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    eqr(d, W / 2, y0 + 160, "Đang có t_{10} = 10,2 s", 48, INK, alpha=a)
    eqr(d, W / 2, y0 + 245, "Đổi M = 0,30 kg (gấp 3)", 48, INK, alpha=a)
    eqr(d, W / 2, y0 + 350, "Kẹp đứng yên: t_{10} đổi thế nào?", 48, INK, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 484], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 484], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
TR = [0.4, 4.3, 7.1]                               # luc bat dau bam gio tung lan
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
    w_frame = 2 * math.pi / (T10[j] / 10) * SPD / 30 if not done else 0.0   # goc quay moi khung (rad)
    rig(d, ph, j + 1, ften=MG[j], trail=w_frame)
    card(d, (700, 380, 1010, 580), fill=NAVY, r=26)
    eqr(d, 855, 425, "t_{10}", 40, (220, 225, 240))
    text(d, (855, 515), vn(val, 1) + " s", 64, WHITE)
    text(d, (855, 640), f"vòng: {laps}/10", 44, BLUE)
    text(d, (855, 720), "M = " + vn(MS[j], 2) + " kg", 40, INK)
    arrow(d, (720, 820), (790, 820), RED, w=6, head=18)
    text(d, (805, 820), "lực căng", 40, RED, anchor="lm")
    cw = tw(d, "tua nhanh ×3", F(40)) + 40
    card(d, (855 - cw / 2, 890, 855 + cw / 2, 950), fill=(241, 245, 249), outline=TUBE_D, r=30, w=3)
    text(d, (855, 920), "tua nhanh ×3", 40, MUTED)
    nrow = [j + 1, j + (1 if done else 0)]
    table(d, nrow)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · giảm, vẫn lớn hơn 5,1 s"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lb, 40, WHITE, alpha=ka)
    card(d, (40, 360, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    k1, k2, k3 = appear(t, 0.6, 0.4), appear(t, 1.4, 0.4), appear(t, 2.6, 0.4)
    x0, px = 120, 76                                 # 10,2 s -> 775 px
    eqr(d, x0, 450, "M = 0,10 kg", 42, INK, alpha=k1, anchor="l")
    d.rectangle([x0, 490, x0 + T10[0] * px * k1, 560], fill=A(BLUE, k1))
    text(d, (x0 + T10[0] * px - 14, 525), "10,2 s", 40, WHITE, anchor="rm", alpha=k1)
    eqr(d, x0, 650, "M = 0,30 kg", 42, INK, alpha=k2, anchor="l")
    d.rectangle([x0, 690, x0 + T10[2] * px * k2, 760], fill=A(BLUE, k2))
    text(d, (x0 + T10[2] * px - 14, 725), "5,7 s", 40, WHITE, anchor="rm", alpha=k2)
    xm = x0 + T10[0] * px / 2
    for yy in range(470, 790, 22):
        d.line([(xm, yy), (xm, min(yy + 12, 790))], fill=A(RED, k3), width=5)
    text(d, (xm, 840), "một nửa: 5,1 s", 40, RED, alpha=k3)
    table(d, [3, 3])

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    if t < M[1] - 0.1:
        k1, k2, k3 = appear(t, 0.5, 0.45), appear(t, 1.7, 0.45), appear(t, 2.9, 0.45)
        ctext(d, 360, "Quả nặng đứng yên:", 46, INK, alpha=k1)
        ctext(d, 430, "lực căng dây = Mg", 50, RED, alpha=k1)
        ctext(d, 500, "kéo nút vào tâm", 46, RED, alpha=k1)
        eqr(d, W / 2, 640, "T = t_{10}/10", 52, BLUE, alpha=k2)
        eqr(d, W / 2, 735, "v = 2πr/T", 52, BLUE, alpha=k2)
        eqr(d, W / 2, 870, "So Mg với m·v^{2}/r", 50, PURPLE, alpha=k3)
        table(d, [3, 3], fcol=clamp((t - 2.9) / 2.4), hi=appear(t, 5.0, 0.5))
    else:
        k4 = appear(t, M[1] - 0.1, 0.45)
        text(d, (W / 2, 340), "Chưa nói được", 46, NAVY, alpha=k4)
        kk = k4 * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, 410, 1000, 900), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        ctext(d, 540, "Mới thử một bán kính", 46, RED, alpha=kk)
        ctext(d, 610, "r = 0,50 m", 46, RED, alpha=kk)
        ctext(d, 740, "và một nút m = 0,050 kg", 46, RED, alpha=kk)
        table(d, [3, 3], fcol=1.0, hi=1.0)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 96), fill=A(RED, a1), r=33)
    text(d, (W / 2, y0 + 63), "BẪY", 40, WHITE, alpha=a1)
    s = "✗ Đo r từ bàn tay"
    text(d, (W / 2, 450), s, 50, RED, alpha=a1)
    sw = tw(d, s, F(50))
    d.line([(W / 2 - sw / 2 + 60, 452), (W / 2 + sw / 2, 452)], fill=A(RED, a1), width=5)
    # hinh: ong dung, tay cam o duoi, nut ngang dinh ong
    ox, otop, obot = 300, 640, 1080
    nx = ox + 520
    d.rectangle([ox - 14, otop, ox + 14, obot], fill=A(TUBE, a1), outline=A(TUBE_D, a1), width=4)
    d.line([(ox, otop), (nx, otop)], fill=A(NAVY, a1), width=4)
    d.rounded_rectangle([nx - 22, otop - 18, nx + 22, otop + 18], radius=7, fill=A(RUBBER, a1), outline=A((124, 45, 18), a1), width=3)
    hy = 980
    d.ellipse([ox - 52, hy - 34, ox + 52, hy + 34], fill=A((253, 186, 116), a1), outline=A((154, 52, 18), a1), width=4)
    text(d, (ox - 70, hy), "tay", 40, INK, anchor="rm", alpha=a1)
    dashed(d, (ox + 50, hy - 20), (nx - 24, otop + 20), A(RED, a1), w=6)
    text(d, (690, 880), "✗", 50, RED, alpha=a1)
    kk = appear(t, M[0] + 2.3, 0.5)
    if kk <= 0: return
    d.line([(ox, otop - 70), (nx, otop - 70)], fill=A(GREEN, kk), width=6)
    d.line([(ox, otop - 92), (ox, otop - 48)], fill=A(GREEN, kk), width=6)
    d.line([(nx, otop - 92), (nx, otop - 48)], fill=A(GREEN, kk), width=6)
    dashed(d, (ox, otop - 100), (ox, obot + 40), A(GREEN, kk), w=4)
    text(d, ((ox + nx) / 2, otop - 125), "r (từ trục ống)", 44, GREEN, alpha=kk)
    card(d, (80, 1200, 1000, 1500), fill=A((236, 253, 243), kk), r=24)
    ctext(d, 1300, "✓ Đo r từ trục ống", 50, GREEN, alpha=kk)
    ctext(d, 1400, "tới tâm nút", 50, GREEN, alpha=kk)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        cx = 540
        d.line([(cx, 960), (cx, 1040)], fill=A(NAVY, k), width=4)
        d.rectangle([cx - 16, 990, cx + 16, 1008], fill=A(ORANGE, k))
        for i in range(4):
            yb = 1040 + i * 44
            d.rounded_rectangle([cx - 42, yb, cx + 42, yb + 40], radius=6, fill=A(BLOCK, k), outline=A(TUBE_D, k), width=3)
        text(d, (cx + 70, 1120), "M = 0,40 kg", 44, INK, anchor="lm", alpha=k)
        kh = appear(t, M[0] + 2.8, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        eqr(d, W / 2, 1450, "Lấy g = 9,8 m/s^{2}", 44, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Lực căng dây đóng vai lực hướng tâm",
             "Treo 4 quả, kẹp vẫn đứng yên:\nm·v²/r khoảng bao nhiêu N?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for j in range(3):
        cs.append((do["t0"] + TR[j], "tap"))
        cs.append((do["t0"] + TR[j] + T10[j] / SPD, "tick"))
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-huongtam-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực hướng tâm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nút cao su quay trên ống", draw=s_hook, tail=0.5, caps=[
   ("Dây luồn qua ống.", 2.6),
   ("Dừng video, chọn đáp án.", 6.3)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bấm giờ 10 vòng, giữ kẹp yên.", 3.9),
   ("Thêm quả nặng, đo lại.", 2.9),
   ("Lần ba: ba quả nặng.", 2.7)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So thanh dưới với vạch đỏ.", 5.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Lực nào kéo nút vào tâm?", 6.0),
   ("Còn điều chưa biết.", 3.4)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Đo bán kính từ đâu?", 5.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
