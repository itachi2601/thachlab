# Clip: tn-l12-apsuatdongnang-02 - Do ap suat khi trong binh kin khi doi nhiet do
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-apsuatdongnang-02.json (so_lieu_mau, tham_so); _kiem_so() doi chieu.
# Ban 1 (28/10/2026): mau boyle (dung cu + bang + do thi) + cues nhu phongxa2.
# Ban 2 (21/11/2026, viec 4 lo 20): cong --do-chu (chu >= 56 px khi ve, nhip >= 2,5 s, khong dung yen > 4 s), K10 (khong
#   nut A-D, "Dung lai, tu doan"), bay hinh tu giai thich (hai khung: lay ti so theo °C -> thanh p vuot khung / doi ra K ->
#   khop ap ke), bo cong thuc E_d chu nho, cau THU NGHI = cau_chot khung web.
# Quan niem sai can danh: p ti le voi nhiet do °C (hien_tuong_hay_sai[0]).
# Du doan: dun 10 °C -> 90 °C (°C gap 9 lan), ap ke chi bao nhieu? -> 123,0 kPa (hang 1 va 5 cua so_lieu_mau).
#   Khac ca cua boylecharles2 (25 -> 50 °C, chieu dai cot khi), pttrangthai2 (0 -> 100 °C, dai luong nao khong doi),
#   Cau 7 cua bai (27 -> 327 °C, dong nang).
# Thu nghi: o 10 °C ap ke 96,0 kPa; nuoc phai nong toi may °C thi p gap doi? -> T = 2 x 283 = 566 K -> 293 °C
#   (mo_hinh p = p_0.T/T_0; dap so KHONG hien tren man; khac ca 60 °C cua pttrangthai2, 100 °C cua boylecharles2).
import random
from engine import *

ROWS = [(10, 283, 96.0, 0.3392), (30, 303, 102.8, 0.3393), (50, 323, 109.5, 0.3390),
        (70, 343, 116.4, 0.3394), (90, 363, 123.0, 0.3388)]          # so_lieu_mau: t (C), T (K), p (kPa), p/T
P0, T0 = 96.0, 283                                                    # tham_so p_0 o 283 K
def model(T): return P0 * T / T0                                      # chi de ve duong thang, khong in so
def f1(v): return f"{v:.1f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-apsuatdongnang-02.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for r in ROWS: assert any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang), r
    assert {p["ky_hieu"]: p for p in k["tham_so"]}["p_0"]["gia_tri"] == P0
    assert abs(2 * T0 - 273 - 293) < 1e-9                              # dap so cau THU NGHI (khong in)
_kiem_so()

DRED = (185, 28, 28); DGREEN = (10, 110, 50); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

# ---------------- dung cu: noi nuoc tren bep + binh kin + nhiet ke + ap ke dien tu ----------------
R = random.Random(4)
PART = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.25, 0.45), R.choice((-1, 1)) * R.uniform(0.25, 0.45))
        for _ in range(16)]
STEAM = [(R.uniform(170, 510), R.random()) for _ in range(6)]

PX0, PX1, PY0, PY1 = 130, 560, 560, 930      # noi
BX0, BX1, BY0, BY1 = 240, 420, 690, 890      # binh kim loai (ngap trong nuoc)
TX, TTOP, TBULB = 185, 430, 850              # nhiet ke ben trai binh

def heat_of(tc): return clamp((tc - 10) / 80)

def rig(d, t, tc, p_lbl, t_lbl):
    """tc: nhiet do nuoc de ve; p_lbl/t_lbl: chu tren hai man hinh ('···' khi dang dun)."""
    h = heat_of(tc)
    d.rounded_rectangle([PX0 - 30, PY1 + 6, PX1 + 30, PY1 + 62], radius=14, fill=NAVY)
    d.rounded_rectangle([PX0 + 40, PY1 + 6, PX1 - 40, PY1 + 22], radius=6, fill=mix((120, 125, 140), (239, 68, 68), h))
    d.rectangle([PX0, PY0 + 50, PX1, PY1], fill=mix((191, 219, 254), (254, 205, 170), h))
    d.line([(PX0, PY0), (PX0, PY1), (PX1, PY1), (PX1, PY0)], fill=NAVY, width=8, joint="curve")
    d.line([(PX0 - 24, PY0), (PX0, PY0)], fill=NAVY, width=8); d.line([(PX1, PY0), (PX1 + 24, PY0)], fill=NAVY, width=8)
    if h > 0.6:                                                        # hoi nuoc khi nong
        sa = clamp((h - 0.6) / 0.4)
        for x, ph0 in STEAM:
            q = (ph0 + t * 0.5) % 1
            y = PY0 + 30 - q * 120
            pts = [(x + 10 * math.sin((y - k * 10) / 18 + ph0 * 6), y - k * 10) for k in range(5)]
            d.line(pts, fill=A((160, 165, 180), sa * (1 - q)), width=5)
    d.rounded_rectangle([BX0, BY0, BX1, BY1], radius=26, fill=mix((225, 232, 245), (255, 225, 210), h), outline=(70, 78, 100), width=8)
    sp = math.sqrt((tc + 273) / T0)                                    # v ti le can T
    for (ux, uy, vx, vy) in PART:
        x = BX0 + 24 + refl(ux + vx * t * sp, 0, 1) * (BX1 - BX0 - 48)
        y = BY0 + 24 + refl(uy + vy * t * sp, 0, 1) * (BY1 - BY0 - 48)
        dot(d, x, y, 8, mix(BLUE, RED, h))
    cx = (BX0 + BX1) / 2                                               # ong noi binh -> ap ke
    d.line([(cx, BY0), (cx, 470), (620, 470)], fill=GRAY, width=14, joint="curve")
    d.line([(510, 520), (470, 880)], fill=(160, 120, 80), width=10)    # que khuay
    d.rounded_rectangle([TX - 14, TTOP, TX + 14, TBULB], radius=14, fill=WHITE, outline=NAVY, width=4)
    dot(d, TX, TBULB + 14, 24, RED, NAVY)
    d.rectangle([TX - 6, lerp(TBULB - 40, TTOP + 30, tc / 100), TX + 6, TBULB], fill=RED)
    # man hinh ap ke dien tu
    card(d, (620, 240, 1030, 580), fill=WHITE, outline=NAVY, r=28, w=4)
    text(d, (825, 292), "Áp kế", 58, INK)
    d.rounded_rectangle([650, 340, 1000, 466], radius=16, fill=NAVY)
    text(d, (825, 403), p_lbl, 76, (134, 239, 172))
    text(d, (825, 525), "kPa", 58, INK)
    # man hinh nhiet ke
    card(d, (620, 610, 1030, 950), fill=WHITE, outline=NAVY, r=28, w=4)
    text(d, (825, 662), "Nhiệt kế", 58, INK)
    d.rounded_rectangle([650, 710, 1000, 836], radius=16, fill=WHITE, outline=NAVY, width=4)
    text(d, (825, 773), t_lbl, 76, RED)
    text(d, (825, 895), "°C", 58, INK)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def pill(d, y, s, col, a=1.0):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, a), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: khong nut A-D) ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, t, 10, f1(ROWS[0][2]), str(ROWS[0][0]))
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 24, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 185), "Đun nước 10 °C → 90 °C.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 280), "Áp kế chỉ bao nhiêu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 380, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: dun dan, doc p va t, ghi bang ----------------
ROW_T = [0.4, 1.4, 2.4, 3.4, 4.4]      # moc (trong canh) hien tung hang
HEAT = 0.8                             # dun trong 0,8 s truoc moi hang; man hinh hien '···' (khong in so noi suy)

def do_state(t):
    tc, pl, tl = ROWS[0][0], f1(ROWS[0][2]), str(ROWS[0][0])
    for i in range(1, 5):
        s = ROW_T[i] - HEAT
        if t < s: break
        tc = lerp(ROWS[i - 1][0], ROWS[i][0], ease((t - s) / HEAT))
        if t < ROW_T[i]: pl, tl = "···", "···"
        else: pl, tl = f1(ROWS[i][2]), str(ROWS[i][0])
    return tc, pl, tl

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tc, pl, tl = do_state(t)
    rig(d, t, tc, pl, tl)
    card(d, (60, 1020, 1020, 1580), fill=WHITE, outline=NAVY, w=4)
    xs = [230, 540, 840]
    for x, c, col in zip(xs, ["t (°C)", "T (K)", "p (kPa)"], [RED, INK, BLUE]): text(d, (x, 1078), c, 58, col)
    d.line([(90, 1120), (990, 1120)], fill=NAVY, width=3)
    last = max([i for i in range(5) if t >= ROW_T[i]], default=-1)
    for i, (tt, TK, p, _) in enumerate(ROWS):
        a = appear(t, ROW_T[i], 0.35); y = 1170 + i * 82
        if a <= 0: continue
        if i == last: d.rounded_rectangle([80, y - 36, 1000, y + 36], radius=16, fill=A((225, 236, 255), a))
        for x, s, col in zip(xs, [str(tt), str(TK), f1(p)], [RED, INK, BLUE]):
            text(d, (x, y), s, 58, col, alpha=a)

# ---------------- canh 3: Dap an + do thi p-T qua goc O + p/T ----------------
GX0, GX1, GYB, GYT = 200, 960, 900, 330
def GX(T): return GX0 + T / 400 * (GX1 - GX0)
def GY(p): return GYB - p / 140 * (GYB - GYT)

def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 215, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    for p in (40, 80, 120): d.line([(GX0, GY(p)), (GX1, GY(p))], fill=(236, 230, 218), width=2)
    d.line([(GX0, GYB), (GX1 + 25, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 50)], fill=NAVY, width=5)
    text(d, (GX0 + 24, GYT - 62), "p (kPa)", 58, BLUE, anchor="lm")
    text(d, (GX1 + 25, GYB - 50), "T (K)", 58, INK, anchor="rm")
    text(d, (GX0 - 34, GYB + 40), "O", 58, INK)
    for T in (100, 200, 300, 400):
        d.line([(GX(T), GYB), (GX(T), GYB + 12)], fill=NAVY, width=3)
        text(d, (GX(T), GYB + 50), str(T), 56, INK)
    for p in (40, 80, 120):
        d.line([(GX0 - 12, GY(p)), (GX0, GY(p))], fill=NAVY, width=4); text(d, (GX0 - 22, GY(p)), str(p), 56, INK, anchor="rm")
    kl = ease((t - 1.6) / 1.6)                                         # keo dai net dut ve goc O
    if kl > 0:
        Ta = 400 - (400 - 0) * kl
        for j in range(40):
            a_, b_ = lerp(400, Ta, j / 40), lerp(400, Ta, (j + 0.55) / 40)
            d.line([(GX(a_), GY(model(a_))), (GX(b_), GY(model(b_)))], fill=A(BLUE, 0.75), width=6)
        if kl >= 1:
            pr = 14 + 5 * math.sin(t * 5)
            d.ellipse([GX0 - pr - 10, GYB - pr - 10, GX0 + pr + 10, GYB + pr + 10], outline=GREEN, width=6)
    for i, (_, TK, p, _) in enumerate(ROWS):
        a = appear(t, 0.4 + i * 0.2, 0.4)
        if a > 0: dot(d, GX(TK), GY(p), 16 * back(a), ORANGE, WHITE)
    k = appear(t, M[1] - 0.1, 0.5)
    if k <= 0: return
    card(d, (60, 1060, 1020, 1330), fill=A((236, 253, 243), k), outline=A(GREEN, k), r=24, w=5)
    text(d, (W / 2, 1140), "p/T ≈ 0,339 kPa/K", 64, DGREEN, alpha=k)
    text(d, (W / 2, 1245), "ở cả 5 mốc đo", 58, INK, alpha=k)

# ---------------- canh 4: Vi sao p tang + Chua noi duoc ----------------
RB = random.Random(9)
MOL = [(RB.random(), RB.random(), RB.uniform(0, 2 * math.pi)) for _ in range(12)]
TRAIL = 0.45                                                           # vet = quang duong trong 0,45 s cuoi (dai ti le toc do)
def box(d, t, x0, x1, y0, y1, TK, p, col):
    sp = 260 * math.sqrt(TK / T0)                                      # toc do ti le can T (v ~ sqrt T; 363/283 -> x1,13)
    d.rectangle([x0, y0, x1, y1], fill=(246, 249, 255), outline=NAVY, width=5)
    L, Hh = x1 - x0 - 24, y1 - y0 - 24
    for (ux, uy, ang) in MOL:
        pos = lambda tt: (x0 + 12 + refl(ux * L + sp * math.cos(ang) * tt, 0, L), y0 + 12 + refl(uy * Hh + sp * math.sin(ang) * tt, 0, Hh))
        pts = [pos(t - TRAIL * j / 12) for j in range(13)]
        d.line(pts, fill=mix(col, WHITE, 0.45), width=8, joint="curve")
        x, y = pts[0]
        if x - x0 < 24 or x1 - x < 24 or y - y0 < 24 or y1 - y < 24: dot(d, x, y, 20, A(YELLOW, 0.75))
        dot(d, x, y, 11, col)
    text(d, ((x0 + x1) / 2, y0 - 42), f"{TK} K", 60, col)
    text(d, ((x0 + x1) / 2, y1 + 50), f"{f1(p)} kPa", 60, col)

def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    box(d, t, 80, 510, 300, 700, ROWS[0][1], ROWS[0][2], BLUE)
    box(d, t, 570, 1000, 300, 700, ROWS[4][1], ROWS[4][2], RED)
    c = appear(t, M[1] - 0.1, 0.5)
    if c <= 0: return
    card(d, (60, 880, 1020, 1160), fill=A(WHITE, c), outline=A(PURPLE, c), w=6)
    pill(d, 910, "CHƯA NÓI ĐƯỢC", PURPLE, c)
    text(d, (W / 2, 1065), "Chỉ đo p và t", 62, INK, alpha=c)

# ---------------- canh 5: Bay - lay ti so theo °C (hinh tu giai thich, 2 khung, 3 nhip >= 3 s) ----------------
SB = 2.6                               # px / kPa cho thanh ap suat
BXL = 330                              # goc trai thanh
def bar(d, y, p_len, col, lab, val, a=1.0, over=False, t=0.0):
    text(d, (BXL - 24, y), lab, 58, INK, anchor="rm", alpha=a)
    x1 = BXL + p_len * SB
    if over:                                                           # vuot khung: cat o mep, mui ten nhap nhay
        x1 = min(x1, 960)
        d.rounded_rectangle([BXL, y - 30, x1, y + 30], radius=10, fill=A(col, a))
        if x1 >= 960:
            w = 8 + 6 * (0.5 + 0.5 * math.sin(t * 8))
            arrow(d, (930, y), (1005, y), A(col, a), w=int(w), head=30)
        return
    d.rounded_rectangle([BXL, y - 30, x1, y + 30], radius=10, fill=A(col, a))
    if val: text(d, (x1 + 18, y), val, 58, INK, anchor="lm", alpha=a)

def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 215, 1040, 760), fill=(254, 242, 242), outline=DRED, w=6)
    text(d, (W / 2, 285), "10 °C → 90 °C: p × 9 ?", 60, DRED)
    bar(d, 410, ROWS[0][2], GRAY, "10 °C", f1(ROWS[0][2]))
    g = ease((t - 0.8) / 1.4)                                         # nhip 1: thanh 90 °C dai dan, vuot khung
    bar(d, 520, lerp(ROWS[0][2], 9 * ROWS[0][2], g), DRED, "90 °C", None, over=True, t=t)
    x = appear(t, M[1] - 0.1, 0.4)                                     # nhip 2: nhan 864 kPa? + vuot thang ap ke
    if x > 0:
        text(d, (1000, 605), f"{f1(9 * ROWS[0][2]).replace(',0', '')} kPa ?", 60, DRED, anchor="rm", alpha=x)
        text(d, (W / 2, 690), "✗ vượt thang 200 kPa", 60, DRED, alpha=x)
    k = appear(t, M[2] - 0.1, 0.5)                                     # nhip 3: doi ra K, khop ap ke
    if k <= 0: return
    card(d, (40, 800, 1040, 1400), fill=A((236, 253, 243), k), outline=A(DGREEN, k), w=6)
    text(d, (W / 2, 870), "283 K → 363 K", 60, DGREEN, alpha=k)
    bar(d, 1000, ROWS[0][2], GRAY, "283 K", f1(ROWS[0][2]), a=k)
    g2 = ease((t - M[2] - 0.3) / 1.0)
    bar(d, 1120, lerp(ROWS[0][2], ROWS[4][2], g2), DGREEN, "363 K", f1(ROWS[4][2]) if g2 >= 1 else "", a=k)
    y = appear(t, M[2] + 1.4, 0.4)
    if y > 0: text(d, (W / 2, 1270), "✓ Khớp", 64, DGREEN, alpha=y)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 245, "THỬ NGHĨ", ORANGE, k1)
    for y, tl, pl, ct, cp in ((400, "10 °C", f"{f1(ROWS[0][2])} kPa", RED, BLUE), (600, "? °C", "p × 2", DORANGE, BLUE)):
        d.rounded_rectangle([90, y, 470, y + 140], radius=18, fill=A(WHITE, k1), outline=A(NAVY, k1), width=4)
        text(d, (280, y + 70), tl, 66, ct, alpha=k1)
        arrow(d, (500, y + 70), (580, y + 70), A(NAVY, k1), w=6, head=22)
        d.rounded_rectangle([610, y, 990, y + 140], radius=18, fill=A(WHITE, k1), outline=A(NAVY, k1), width=4)
        text(d, (800, y + 70), pl, 66, cp, alpha=k1)
    text(d, (W / 2, 880), "Nóng tới mấy °C để p gấp đôi?", 62, DORANGE, alpha=k1)
    kh = appear(t, 2.75, 0.5)                                          # goi y hien tre ~2,6 s, khong goi y so
    if kh > 0:
        card(d, (140, 970, 940, 1110), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1040), "Gợi ý: T = t + 273", 60, DORANGE, alpha=kh)
    seg_bar(d, 1200, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + ROW_T[4], "ding"), (an["t0"] + an["M"][1] - 0.1, "tap"),
            (tr["t0"] + tr["M"][1] - 0.1, "buzz"), (tr["t0"] + tr["M"][2] + 1.4, "tap"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l12-apsuatdongnang-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Áp suất – động năng phân tử khí · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đun nóng bình khí kín", draw=s_hook, tail=0.3, caps=[
   ("Bình kín ngâm trong nồi nước.", 3.4),
   ("Dừng lại, tự đoán.", 5.3)]),
 dict(key="do", title="Đun dần, đọc t và p", draw=s_do, tail=0.3, caps=[
   ("Đun dần, khuấy, đợi số đứng yên.", 4.2),
   ("Áp kế tăng đều, từng chút.", 3.4)]),
 dict(key="ans", title="Đồ thị p theo T", draw=s_ans, tail=0.3, caps=[
   ("Năm điểm thẳng hàng, qua gốc O.", 3.6),
   ("Tỉ số p/T gần như không đổi.", 3.4)]),
 dict(key="why", title="Vì sao p tăng?", draw=s_why, tail=0.3, caps=[
   ("Nóng hơn: phân tử nhanh hơn.", 3.0),
   ("Tốc độ phân tử: chỉ suy ra.", 3.8)]),
 dict(key="trap", title="Bẫy: tỉ lệ theo °C", draw=s_trap, tail=0.3, caps=[
   ("90/10 = 9: chỉ là số °C.", 3.4),
   ("Con số ×9 vượt cả áp kế.", 3.8),
   ("Đổi ra K: khớp áp kế.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Bình kín: p tỉ lệ thuận T.", 5.0)]),
])
