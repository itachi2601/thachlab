# Clip: tn-l10-roi-tu-do-03 - Nam cham dien + cong quang + dong ho hien so: g = 2s/t^2 o 5 quang roi (10/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-roi-tu-do-03.json:
#   so_lieu_mau: s = 0,20..1,00 m -> t do = 0,205; 0,289; 0,353; 0,407; 0,455 s -> g = 9,52; 9,58; 9,63; 9,66; 9,66
#                g trung binh 9,610 (ghi_chu). tham_so: g that 9,8; tau = 0,003 s (KHONG neu tren man: cau sau hop
#                trong bai hoi "hang nao lech nhieu nhat, vi sao" -> clip khong to sang hang lech, khong noi nguyen nhan).
#   Cau chot: quen he so 2 (hien_tuong_hay_sai) o hang s = 1,00 m: 1,00/0,455^2 = 4,83 -> chua tung hien tren man.
# Truc chinh: gia dung + cong quang doi vi tri + dong ho dem/dung + bang s-t, roi truc so g voi vach 9,8
#   (khac roitudo2: day doi + bong bi moi 0,1 s; khac dog2/dog3: do thi s-t^2, dem khung).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (5 lan tha) -> Dap an (cot g + truc so) -> Rut ra
#       (sat nhau, chua noi duoc) -> Bay (lay trung binh) -> Chot.
# Mau: s / thuoc = BLUE, t / dong ho = TEAL (so xanh la tren nen toi), g = ORANGE, vach 9,8 = GREEN, du doan = PURPLE.
from engine import *

ROWS = [(0.20, 0.205, 9.52), (0.40, 0.289, 9.58), (0.60, 0.353, 9.63), (0.80, 0.407, 9.66), (1.00, 0.455, 9.66)]
G_TRUE, G_TB, TAU = 9.8, 9.61, 0.003
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
SAND = (233, 205, 150); LCD = (16, 40, 32); LCD_ON = (110, 240, 140); COIL = (196, 120, 40)

def vn(x, nd):
    return f"{x:.{nd}f}".replace(".", ",")

# ---------------- dung cu ----------------
Y0, PXM = 380, 1100.0                  # y tam bi luc giu (vach 0) ; px / m
def Y(s): return Y0 + PXM * s
BX, BR = 300, 16                       # duong roi, ban kinh bi
RX0, RX1 = 110, 172                    # than thuoc
SAND_Y = 1528

def ruler(d, marks=False):
    d.rectangle([RX0, Y0 - 20, RX1, Y(1.0) + 30], fill=WOOD, outline=WOOD_D, width=3)
    for c in range(0, 101, 5):
        y = Y(c / 100)
        L = 30 if c % 20 == 0 else (20 if c % 10 == 0 else 10)
        d.line([(RX1 - L, y), (RX1, y)], fill=INK, width=3 if c % 10 == 0 else 2)
        if c % 20 == 0:
            text(d, (RX0 - 10, y), vn(c / 100, 1), 36, INK, anchor="rm")
    text(d, (60, 300), "s (m)", 38, BLUE, anchor="lm")
    if marks:                          # 5 vi tri se dat cong quang
        for s, _, _ in ROWS:
            y = Y(s)
            d.polygon([(RX1 + 6, y), (RX1 + 26, y - 12), (RX1 + 26, y + 12)], fill=ORANGE)

def magnet(d, on=True):
    d.rectangle([RX1, 292, BX - 46, 304], fill=NAVY)                     # tay doi
    card(d, (BX - 46, 270, BX + 46, Y0 - BR - 2), fill=NAVY, r=10)
    for i in range(4):
        yy = 282 + i * 16
        d.line([(BX - 38, yy), (BX + 38, yy)], fill=COIL if on else GRAY, width=6)

def ball(d, s, alpha=1.0):
    y = Y(s)
    d.ellipse([BX - BR, y - BR, BX + BR, y + BR], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=2)
    d.ellipse([BX - 8, y - 9, BX - 2, y - 3], fill=A(STEEL_L, alpha))

def gate(d, s, beam=True, label=True):
    y = Y(s)
    d.rectangle([BX - 62, y - 40, BX - 44, y + 40], fill=NAVY)            # nhanh phat
    d.rectangle([BX + 44, y - 40, BX + 62, y + 40], fill=NAVY)            # nhanh thu
    d.rectangle([BX + 44, y + 28, BX + 82, y + 40], fill=NAVY)            # than cong
    if beam:
        for x in range(int(BX - 44), int(BX + 44), 14):
            d.line([(x, y), (min(x + 8, BX + 44), y)], fill=RED, width=3)
    if label:
        text(d, (BX + 92, y), "cổng quang", 36, NAVY, anchor="lm")

def sandbox(d):
    d.rectangle([BX - 70, SAND_Y, BX + 70, SAND_Y + 52], fill=SAND, outline=WOOD_D, width=3)

def timer(d, val, box=(600, 400, 1040, 570)):
    x0, y0, x1, y1 = box
    card(d, box, fill=NAVY, r=22)
    card(d, (x0 + 24, y0 + 20, x1 - 24, y1 - 62), fill=LCD, r=12)
    text(d, ((x0 + x1) / 2, (y0 + y1 - 42) / 2), vn(val, 3) + " s", 66, LCD_ON)
    text(d, ((x0 + x1) / 2, y1 - 32), "đồng hồ hiện số", 36, WHITE, bold=False)

def text_cx(d, cx, y, s, size, color=INK, bold=True, maxw=380, alpha=1.0, lh=1.22):
    f = F(size, bold); ls = wrap(d, s, f, maxw)
    y0 = y - (len(ls) - 1) * size * lh / 2
    for i, l in enumerate(ls):
        dtext(d, (cx, y0 + i * size * lh), l, f, color, alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    ruler(d, marks=True); sandbox(d); gate(d, 0.20); magnet(d); ball(d, 0.0)
    text(d, (BX + 62, 322), "nam châm điện", 36, NAVY, anchor="lm")
    a = appear(t, M[0] + 0.4, 0.5)
    if a <= 0: return
    y0 = 450 + (1 - a) * 40; QX0, QX1 = 600, 1040; QC = (QX0 + QX1) / 2
    card(d, (QX0, y0, QX1, y0 + 1000), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (QC - pw / 2, y0 + 30, QC + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (QC, y0 + 61), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text_cx(d, QC, y0 + 210, "Đo t ở 5 quãng rơi s.", 40, INK, bold=False, alpha=a)
    text_cx(d, QC, y0 + 330, "Tính g = 2s/t².", 44, ORANGE, alpha=a)
    text_cx(d, QC, y0 + 590, "So với 9,8 m/s², năm giá trị g thế nào?", 48, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.8
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([QX0 + 40, y0 + 900, QX1 - 40, y0 + 914], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([QX0 + 40, y0 + 900, QX0 + 40 + (QX1 - QX0 - 80) * (1 - p), y0 + 914], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (5 lan tha) ----------------
SLOW, C0, MOVE, HOLD = 2.6, 0.5, 0.5, 0.75
def plan():
    """Moi lan i: (c = bat dau doi cong, r = luc ngat dien, e = luc dong ho dung)."""
    out, c = [], C0
    for i, (s, td, g) in enumerate(ROWS):
        r = c + (MOVE if i else 0.0) + 0.3
        e = r + td * SLOW
        out.append((c, r, e)); c = e + HOLD
    return out
PLAN = plan()

def state(t):
    """-> (i lan hien tai, s cong, s bi | None, bi mo, so dong ho, so hang da co t, ngat dien?)."""
    i = 0
    for k, (c, r, e) in enumerate(PLAN):
        if t >= c: i = k
    c, r, e = PLAN[i]
    s_prev = ROWS[i - 1][0] if i else ROWS[0][0]
    sg = lerp(s_prev, ROWS[i][0], ease((t - c) / MOVE)) if i else ROWS[0][0]
    smax = (SAND_Y - BR - Y0) / PXM
    if t < r:                                         # dang giu bi; dong ho giu so lan truoc
        k = appear(t, c, 0.3) if i else 1.0
        return i, sg, 0.0, k, (ROWS[i - 1][1] if i else 0.0), i, False
    tau = (t - r) / SLOW
    shown = min(tau, ROWS[i][1])
    tb = max(0.0, tau - TAU)
    sb = min(0.5 * G_TRUE * tb * tb, smax)
    return i, sg, sb, 1.0, shown, i + (1 if tau >= ROWS[i][1] else 0), True

def table_st(d, nrow, hi=-1, box=(600, 610, 1040, 1300)):
    x0, y0, x1, y1 = box
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    XS = (x0 + 110, x0 + 320)
    text(d, (XS[0], y0 + 55), "s (m)", 42, BLUE)
    text(d, (XS[1], y0 + 55), "t (s)", 42, TEAL)
    d.line([(x0 + 24, y0 + 100), (x1 - 24, y0 + 100)], fill=LIGHT, width=3)
    for j, (s, td, g) in enumerate(ROWS):
        yy = y0 + 160 + j * 112
        if j == hi:
            d.rounded_rectangle([x0 + 16, yy - 44, x1 - 16, yy + 44], radius=18, fill=(236, 248, 246))
        text(d, (XS[0], yy), vn(s, 2), 48, BLUE)
        if j < nrow: text(d, (XS[1], yy), vn(td, 3), 48, TEAL)

def s_do(img, d, t, sc):
    i, sg, sb, ka, shown, nrow, off = state(t)
    ruler(d); sandbox(d); gate(d, sg); magnet(d, on=not off)
    if off and t - PLAN[i][1] < 0.9:
        text(d, (BX + 62, 322), "ngắt điện", 36, RED, anchor="lm")
    else:
        text(d, (BX + 62, 322), "nam châm điện", 36, NAVY, anchor="lm")
    if off:                                           # vet mo khi bi roi nhanh (>30 px/khung)
        for k in (3, 2, 1):
            sk = state(t - k / 90)[2]
            if sk is not None and 0 < sk < sb: ball(d, sk, 0.18 * (4 - k) / 3)
    ball(d, sb, ka)
    timer(d, shown)
    c, r, e = PLAN[i]
    hi = i if (off and t >= e and t - e < 0.9) else -1
    table_st(d, nrow, hi)

# ---------------- truc so g ----------------
NX0, NX1, G0, G1 = 140, 940, 9.4, 9.9
def gx(g): return NX0 + (g - G0) / (G1 - G0) * (NX1 - NX0)

def numline(d, y, kdots=lambda j: 1.0, alpha=1.0):
    d.line([(NX0 - 30, y), (NX1 + 30, y)], fill=A(INK, alpha), width=4)
    for k in range(6):
        g = G0 + 0.1 * k; x = gx(g)
        d.line([(x, y - 14), (x, y + 14)], fill=A(INK, alpha), width=3)
        text(d, (x, y + 52), vn(g, 1), 38, GREEN if k == 4 else INK, alpha=alpha)
    x8 = gx(G_TRUE)                                   # vach 9,8 net dut
    for yy in range(int(y - 250), int(y - 16), 22):
        d.line([(x8, yy), (x8, yy + 12)], fill=A(GREEN, alpha), width=4)
    text(d, (x8, y - 280), "9,8", 40, GREEN, alpha=alpha)
    seen = {}
    for j, (_, _, g) in enumerate(ROWS):
        k = kdots(j) * alpha
        n = seen.get(g, 0); seen[g] = n + 1
        if k > 0: dot(d, gx(g), y - 40 - 40 * n, 16, A(ORANGE, k), outline=A(WHITE, k))

# ---------------- canh 3: Dap an ----------------
def table_g(d, kg, x0=60, x1=1020, y0=360):
    card(d, (x0, y0, x1, y0 + 700), fill=WHITE, outline=LIGHT, w=3)
    XS = (x0 + 160, x0 + 470, x0 + 780)
    text(d, (XS[0], y0 + 55), "s (m)", 44, BLUE)
    text(d, (XS[1], y0 + 55), "t (s)", 44, TEAL)
    text(d, (XS[2], y0 + 55), "g = 2s/t²", 44, ORANGE)
    text(d, (XS[2], y0 + 108), "(m/s²)", 36, MUTED, bold=False)
    d.line([(x0 + 30, y0 + 140), (x1 - 30, y0 + 140)], fill=LIGHT, width=3)
    for j, (s, td, g) in enumerate(ROWS):
        yy = y0 + 210 + j * 106
        text(d, (XS[0], yy), vn(s, 2), 50, BLUE)
        text(d, (XS[1], yy), vn(td, 3), 50, TEAL)
        text(d, (XS[2], yy), vn(g, 2), 50, ORANGE, alpha=kg(j))

def s_dapan(img, d, t, sc):
    M = sc["M"]
    table_g(d, lambda j: appear(t, M[0] + 0.3 + 0.4 * j, 0.3))
    kn = appear(t, M[1] - 0.1, 0.4)
    if kn > 0:
        numline(d, 1420, kdots=lambda j: appear(t, M[1] + 0.2 + 0.25 * j, 0.3), alpha=kn)
        text(d, (NX0 - 30, 1530), "g (m/s²)", 36, MUTED, bold=False, anchor="lm", alpha=kn)
    ka = appear(t, M[1] + 1.8, 0.4)
    lb = "ĐÁP ÁN · cả năm đều nhỏ hơn 9,8"
    pw = tw(d, lb, F(38)) + 56
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 332), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 300), lb, 38, WHITE, alpha=ka)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 270, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    numline(d, 700)
    ya = 520; xa, xb = gx(9.52), gx(9.66)                 # ngoac "sat nhau"
    k1 = appear(t, 0.5, 0.4)
    if k1 > 0:
        d.line([(xa, ya + 20), (xa, ya), (xb, ya), (xb, ya + 20)], fill=A(ORANGE, k1), width=4)
        text(d, ((xa + xb) / 2, ya - 40), "sát nhau", 40, ORANGE, alpha=k1)
    k2 = appear(t, 1.0, 0.45)
    card(d, (40, 930, 1040, 1170), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
    ctext(d, 1000, "Cùng một nơi:", 44, INK, alpha=k2)
    ctext(d, 1090, "bi rơi với cùng một gia tốc", 46, GREEN, alpha=k2)
    k3 = appear(t, M[1] - 0.1, 0.45)
    if k3 > 0:
        y0 = 1200 + (1 - k3) * 30
        card(d, (40, y0, 1040, y0 + 390), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        ctext(d, y0 + 60, "Chưa nói được", 44, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.4, 0.4)
        card(d, (80, y0 + 120, 1000, y0 + 350), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        ctext(d, y0 + 235, "Vì sao cả năm đều dưới 9,8?", 48, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    card(d, (40, 265, 1040, 815), fill=WHITE, outline=LIGHT, w=3)
    numline(d, 690)
    kk = appear(t, 1.6, 0.45)
    if kk > 0:                                         # duong trung binh hien CUNG luc chu ket luan
        xm = gx(G_TB)
        d.line([(xm, 400), (xm, 676)], fill=A(BLUE, kk), width=5)
        text(d, (xm, 370), "TB 9,61", 40, BLUE, alpha=kk)
    a1 = appear(t, 0.2, 0.45); y0 = 845
    card(d, (40, y0, 1040, y0 + 745), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "“Lấy trung bình là hết lệch”"
    ks = clamp((t - 1.0) / 0.4); f = F(48); lw = tw(d, q, f); yy = y0 + 200
    text(d, (W / 2 + 30, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
    xq = W / 2 + 30 - lw / 2
    if ks > 0:
        d.line([(xq - 6, yy + 2), (xq - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        text(d, (xq - 40, yy), "✗", 52, RED, alpha=ks)
    card(d, (90, y0 + 320, 990, y0 + 690), fill=A((239, 246, 255), kk), r=24)
    ctext(d, y0 + 445, "Trung bình 9,61", 54, BLUE, alpha=kk)
    ctext(d, y0 + 560, "vẫn nhỏ hơn 9,8", 54, NAVY, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        ctext(d, 870, "Quên số 2, tính g = s/t² ở hàng s = 1,00 m. Ra khoảng bao nhiêu?", 46, INK,
              maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
        kh = appear(t, M[0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1180, 970, 1420), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1240, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1340, "Đồng hồ hàng này: 0,455 s", 42, INK, alpha=kh)
    chot_hoi(d, t, sc, "5 quãng rơi cho g sát nhau,\ngần 9,8 m/s²", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][0] + 0.4, "open"), (h["t0"] + h["T"] - 0.8, "ding")]
    for c, rr, ee in PLAN: cs.append((do["t0"] + rr, "tap"))
    cs += [(da["t0"] + da["M"][1] + 1.8, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"),
           (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-roi-tu-do-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Sự rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo g bằng cổng quang", draw=s_hook, tail=0.5, caps=[
   ("Nam châm giữ bi, cổng quang dưới.", 2.8),
   ("Dừng video, chọn câu trả lời.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Ngắt điện: bi rơi, đồng hồ chạy.", 4.0),
   ("Bi qua cổng quang: đồng hồ dừng.", 3.8),
   ("Dời cổng xuống, đo tiếp.", 3.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Tính g cho từng hàng.", 3.0),
   ("Đặt năm giá trị lên trục số.", 3.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Năm giá trị chụm sát nhau.", 3.4),
   ("Còn một điều chưa giải thích.", 3.4)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Năm số cùng lệch một phía.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Tự trả lời.", 5.2)]),
])
