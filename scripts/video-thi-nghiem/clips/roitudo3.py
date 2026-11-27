# Clip: tn-l10-roi-tu-do-03 - Nam cham dien + cong quang + dong ho hien so: g = 2s/t^2 o 5 quang roi (10/11/2026; dung lai
# 27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Du doan khong nut, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-roi-tu-do-03.json (_kiem_so() doi chieu):
#   s = 0,20..1,00 m -> t do = 0,205; 0,289; 0,353; 0,407; 0,455 s -> g = 9,52; 9,58; 9,63; 9,66; 9,66 m/s2.
#   KHONG neu tau, KHONG to sang hang lech: o "Doc bang" duoi hop trong bai hoi "hang nao lech nhieu nhat, vi sao".
# Du doan (moi, vi Rut ra + "Doc bang" cua bai da noi "g sat nhau, gan 9,8, deu nho hon"): 20 cm dau mat 0,205 s;
#   20 cm cuoi (0,80 -> 1,00 m) mat bao lau? -> 0,455 - 0,407 = 0,048 s ~ 0,05 s. Khung: A 0,05 / B 0,10 / C 0,21 / D 0,41 s.
# Bay = hien_tuong_hay_sai thu 3: g = s/t^2 (quen he so 2): 0,40 : 0,289^2 ~ 4,79 vs 2s/t^2 ~ 9,58 m/s2.
# Thu nghi (= cau_chot khung web, sua theo kiem v1: xa cac moc da chieu): lay g = 9,8, cong o s = 1,20 m (bien tren mien
#   s 0,1..1,2, ngoai bang) -> theo mo hinh t = sqrt(2 . 1,2 / 9,8) = 0,495 s ~ 0,49 s. Buoc nguoc + can chua chieu; 0,49 khong hien.
#   Nhieu: 0,55 s (ngoai suy tuyen tinh 0,455 x 1,2 = noi suy tu moc 1,00 m), 0,35 s (quen he so 2), 0,24 s (quen can).
from engine import *

ROWS = [(0.20, 0.205, 9.52), (0.40, 0.289, 9.58), (0.60, 0.353, 9.63), (0.80, 0.407, 9.66), (1.00, 0.455, 9.66)]
G, TAU, CH_S = 9.8, 0.003, 1.20
DT = [round(ROWS[0][1], 3)] + [round(b[1] - a[1], 3) for a, b in zip(ROWS, ROWS[1:])]     # thoi gian moi 20 cm

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-roi-tu-do-03.json")))
    for r, (s, td, g) in zip(k["so_lieu_mau"]["hang"], ROWS):
        assert abs(r[0] - s) < 1e-9 and abs(r[2] - td) < 1e-9 and abs(r[3] - g) < 1e-9
        assert f"{2 * s / td ** 2:.2f}" == f"{g:.2f}"
    assert DT == [0.205, 0.084, 0.064, 0.054, 0.048]
    assert f"{0.40 / 0.289 ** 2:.2f}" == "4.79"
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["g"]["gia_tri"] == G and ts["s"]["min"] <= CH_S <= ts["s"]["max"]
    assert f"{(2 * CH_S / G) ** 0.5:.3f}" == "0.495" and f"{ROWS[-1][1] * CH_S:.2f}" == "0.55"
    assert f"{(CH_S / G) ** 0.5:.2f}" == "0.35" and f"{2 * CH_S / G:.2f}" == "0.24"
_kiem_so()

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
SAND = (233, 205, 150); LCD = (16, 40, 32); LCD_ON = (110, 240, 140); COIL = (196, 120, 40)
DRED = (185, 28, 28); DTEAL = (15, 118, 110); EMPTY = (148, 140, 128); C_S = (37, 99, 235); C_T = (15, 118, 110)
C_G = (194, 65, 12)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def badge(d, y, s, col, a=1.0):
    pw = tw(d, s, F(58)) + 64
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 82), fill=A(col, a), r=40)
    text(d, (W / 2, y + 41), s, 58, WHITE, alpha=a)

# ---------------- dung cu: thuoc + nam cham + cong quang (cot trai) ; dong ho + bang (cot phai) ----------------
Y0, PXM = 340, 880.0
def Y(s): return Y0 + PXM * s
BX, BR = 340, 18
RX0, RX1 = 150, 200
SAND_Y = Y(1.0) + 60

def rig(d, sg, sb, on=True, ka=1.0):
    d.rectangle([RX0, Y0 - 20, RX1, Y(1.0) + 20], fill=WOOD, outline=WOOD_D, width=3)
    for c in range(0, 101, 10):
        y = Y(c / 100); L = 34 if c % 20 == 0 else 18
        d.line([(RX1 - L, y), (RX1, y)], fill=INK, width=3)
    text(d, (RX0 - 12, Y0), "0", 56, C_S, anchor="rm"); text(d, (RX0 - 12, Y(1.0)), "1,0", 56, C_S, anchor="rm")
    d.rectangle([RX1, 262, BX - 50, 274], fill=NAVY)
    card(d, (BX - 50, 236, BX + 50, Y0 - BR - 2), fill=NAVY, r=10)
    for i in range(4):
        d.line([(BX - 40, 248 + i * 16), (BX + 40, 248 + i * 16)], fill=COIL if on else GRAY, width=6)
    d.rectangle([BX - 80, SAND_Y, BX + 80, SAND_Y + 50], fill=SAND, outline=WOOD_D, width=3)
    y = Y(sg)                                                                      # cong quang
    d.rectangle([BX - 70, y - 44, BX - 50, y + 44], fill=NAVY); d.rectangle([BX + 50, y - 44, BX + 70, y + 44], fill=NAVY)
    for x in range(BX - 50, BX + 50, 14): d.line([(x, y), (min(x + 8, BX + 50), y)], fill=RED, width=3)
    yb = Y(sb)
    d.ellipse([BX - BR, yb - BR, BX + BR, yb + BR], fill=A(STEEL, ka), outline=A(NAVY, ka), width=2)
    d.ellipse([BX - 8, yb - 9, BX - 2, yb - 3], fill=A(STEEL_L, ka))

def timer(d, val):
    card(d, (560, 215, 1040, 400), fill=NAVY, r=22)
    card(d, (584, 235, 1016, 380), fill=LCD, r=12)
    text(d, (800, 308), vn(val, 3) + " s", 72, LCD_ON)

def table(d, nrow, hi=-1):
    card(d, (560, 425, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    XS = (680, 900)
    text(d, (XS[0], 490), "s (m)", 56, C_S); text(d, (XS[1], 490), "t (s)", 56, C_T)
    d.line([(584, 540), (1016, 540)], fill=LIGHT, width=3)
    for j, (s, td, g) in enumerate(ROWS):
        yy = 625 + j * 145
        if j == hi: d.rounded_rectangle([576, yy - 52, 1024, yy + 52], radius=18, fill=(236, 248, 246))
        text(d, (XS[0], yy), vn(s, 2), 60, C_S)
        if j < nrow: text(d, (XS[1], yy), vn(td, 3), 60, C_T)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0.20, 0.0); timer(d, 0.205)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: table(d, 1); return
    y0 = 620 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 26, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 170), "20 cm đầu: 0,205 s.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "20 cm cuối (0,80 → 1,00 m):", 60, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 355), "mất bao lâu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 445, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (5 lan tha, chieu cham) ----------------
SLOW, C0, MOVE, REST = 1.5, 0.3, 0.3, 0.2
SMAX = (SAND_Y - BR - Y0) / PXM
T_LAND = (2 * SMAX / G) ** 0.5 + TAU
def plan():
    out, c = [], C0
    for i, (s, td, g) in enumerate(ROWS):
        r = c + (MOVE if i else 0.0) + 0.15
        out.append((c, r, r + td * SLOW)); c = r + T_LAND * SLOW + REST
    return out
PLAN = plan()

def state(t):
    i = 0
    for k, (c, r, e) in enumerate(PLAN):
        if t >= c: i = k
    c, r, e = PLAN[i]
    sg = lerp(ROWS[i - 1][0], ROWS[i][0], ease((t - c) / MOVE)) if i else ROWS[0][0]
    if t < r: return i, sg, 0.0, (ROWS[i - 1][1] if i else 0.0), i, False
    tau = (t - r) / SLOW; tb = max(0.0, tau - TAU)
    return i, sg, min(0.5 * G * tb * tb, SMAX), min(tau, ROWS[i][1]), i + (1 if tau >= ROWS[i][1] else 0), True

def s_do(img, d, t, sc):
    i, sg, sb, shown, nrow, off = state(t)
    rig(d, sg, sb, on=not off); timer(d, shown)
    c, r, e = PLAN[i]
    table(d, nrow, i if (off and e <= t < e + 0.6) else -1)
    card(d, (40, 1440, 1040, 1560), fill=NAVY, r=30)
    text(d, (W / 2, 1500), "chiếu chậm", 58, YELLOW)

# ---------------- canh 3: Dap an (thoi gian moi 20 cm) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=(236, 253, 243), outline=GREEN, w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL)
    text(d, (W / 2, 400), "≈ 0,05 s,", 64, DTEAL)
    text(d, (W / 2, 485), "ngắn hơn 4 lần", 64, DTEAL)
    card(d, (40, 590, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 665), "Thời gian mỗi 20 cm", 58, C_T)
    text(d, (90, 750), "tới s (m)", 56, C_S, anchor="lm"); text(d, (990, 750), "t (s)", 56, C_T, anchor="rm")
    k = ease(clamp((t - 0.2) / 1.2))
    for j, v in enumerate(DT):
        y = 810 + j * 115; L = 560 * v / DT[0] * k
        text(d, (90, y + 30), vn(ROWS[j][0], 1), 56, C_S, anchor="lm")
        d.rounded_rectangle([200, y, 200 + max(L, 12), y + 60], radius=12, fill=C_T if j < 4 else C_G)
        text(d, (990, y + 30), vn(v, 3), 56, C_T if j < 4 else C_G, anchor="rm")
    k2 = appear(t, M[1] + 0.1, 0.45)
    text(d, (W / 2, 1450), "0,455 − 0,407 = 0,048 s", 60, C_G, alpha=k2)

# ---------------- canh 4: Rut ra (g = 2s/t^2) ----------------
NX0, NX1, G0, G1 = 140, 940, 9.4, 9.9
def gx(g): return NX0 + (g - G0) / (G1 - G0) * (NX1 - NX0)
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 320), "s = ½·g·t²", 64, INK)
    text(d, (W / 2, 445), "→ g = 2s : t²", 66, C_G)
    card(d, (40, 580, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 680), "9,52 · 9,58 · 9,63 · 9,66 · 9,66 m/s²", 56, C_G)
    y = 900
    d.line([(NX0, y), (NX1, y)], fill=INK, width=4)
    for gv in (9.5, 9.8):
        d.line([(gx(gv), y - 18), (gx(gv), y + 18)], fill=GREEN if gv == 9.8 else INK, width=6 if gv == 9.8 else 4)
    text(d, (NX1, y - 80), "g (m/s²)", 56, C_G, anchor="rm")
    text(d, (gx(9.5), y + 70), "9,5", 56, INK); text(d, (gx(9.8), y + 70), "9,8", 56, GREEN)
    for j, (s, td, g) in enumerate(ROWS):
        kd = appear(t, 0.6 + 0.25 * j, 0.3)
        if kd > 0: dot(d, gx(g), y - 4 - 34 * (j % 2), 16 * kd, C_G)
    k2 = appear(t, M[1] - 0.1, 0.45)
    text(d, (W / 2, 1180), "Sát nhau, gần 9,8 m/s²:", 60, INK, alpha=k2)
    text(d, (W / 2, 1290), "cùng một gia tốc", 62, DTEAL, alpha=k2)

# ---------------- canh 5: Bay (quen he so 2) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; ok = t >= M[1] - 0.1
    card(d, (40, 215, 1040, 655), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 300), "✗ Quên số 2: g = s : t²", 60, DRED)
    text(d, (W / 2, 420), "0,40 : 0,289² ≈ 4,79 m/s²", 60, DRED)
    pu = 0.5 + 0.5 * math.sin(t * 5)
    text(d, (W / 2, 560), "chỉ bằng nửa 9,8", 58, mix(DRED, RED, pu))
    if ok:
        card(d, (40, 690, 1040, 1130), fill=WHITE, outline=DTEAL, w=6)
        text(d, (W / 2, 775), "✓ g = 2s : t²", 60, DTEAL)
        text(d, (W / 2, 895), "2 · 0,40 : 0,289² ≈ 9,58 m/s²", 58, DTEAL)
        text(d, (W / 2, 1035), "gần 9,8", 60, mix(DTEAL, GREEN, pu))

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    tt = (t * 0.25) % 0.5
    rig(d, 1.0, min(0.5 * G * tt * tt, SMAX))
    card(d, (560, 215, 1040, 1290), fill=WHITE, outline=NAVY, w=6)
    text(d, (800, 520), "Cả năm g", 58, INK); text(d, (800, 610), "nhỏ hơn 9,8:", 58, INK)
    text(d, (800, 820), "vì sao?", 64, DTEAL, alpha=appear(t, 1.6, 0.4))

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "g = 9,8 m/s².", 60, INK, alpha=k)
    text(d, (W / 2, 495), "Cổng cách điểm thả", 60, INK, alpha=k)
    text(d, (W / 2, 590), "1,20 m.", 60, C_S, alpha=k)
    text(d, (W / 2, 715), "Bi tới cổng", 60, ORANGE, alpha=k)
    text(d, (W / 2, 805), "mất bao lâu?", 62, ORANGE, alpha=k)
    yb = 900 + 180 * ((t * 0.5) % 1.0) ** 2
    d.ellipse([W / 2 - 20, yb - 20, W / 2 + 20, yb + 20], fill=A(STEEL, k), outline=A(NAVY, k), width=2)
    d.line([(W / 2 - 90, 1110), (W / 2 + 90, 1110)], fill=A(RED, k), width=5)
    text(d, (W / 2, 1195), "t = ? s", 62, NAVY, alpha=k)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + ee, "tap") for (c, r, ee) in PLAN if ee < do["T"]]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-roi-tu-do-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Sự rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo g bằng cổng quang", draw=s_hook, tail=0.3, caps=[
   ("Ngắt điện, đồng hồ đếm.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Dời cổng quang, thả lại.", 3.3),
   ("Bi qua cổng: đồng hồ dừng.", 3.3)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Mỗi 20 cm, ngắn dần.", 3.2),
   ("Lấy hai số đo trừ nhau.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Tính g cho từng lần đo.", 3.4),
   ("Năm giá trị sát nhau.", 3.6)]),
 dict(key="bay", title="Bẫy: quên số 2", draw=s_bay, tail=0.3, caps=[
   ("Quên số 2?", 3.2),
   ("Nhớ: g bằng 2s chia t².", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Clip chưa giải thích.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.0)]),
])
