# Clip: tn-l10-gia-toc-01 - Cam bien ghi v cua xe lan xuong mang nghieng o 5 thoi diem cach 0,2 s (1/11/2026; dung lai
# 27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Bay ve bang do thi, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-gia-toc-01.json (_kiem_so() doi chieu):
#   so_lieu_mau: t = 0; 0,2; 0,4; 0,6; 0,8 s ; v doc = 0,20; 0,30; 0,40; 0,49; 0,59 m/s ; Dv/Dt = 0,50; 0,50; 0,45; 0,50.
#   mo_hinh: a = g.sin(alpha) = 0,49 m/s2, v0 = 0,20 m/s (chi dung de ve xe chay).
#   KHONG tinh a ca khoang 0-0,8 s (= __A_TONG__ cua "Doc bang" trong bai), khong giai thich 0,45 vs 0,50 (cau do).
# Du doan (giu y cu, K10 khong nut): biet v luc 0 va 0,2 s -> v luc 0,8 s? -> khoang 0,60 m/s (do 0,59).
# Bay = hien_tuong_hay_sai "lay v/t thay Dv/Dt": tren do thi, v/t = do doc duong tu goc O (do, 1,0 m/s2) khac
#   duong qua cac diem (xanh, 0,50 m/s2) vi luc t = 0 xe da co 0,20 m/s.
# Thu nghi (= cau_chot khung web): cung mang (cung a), xe bat dau ghi voi v0 = 0,40 m/s (trong mien tham_so 0-0,5) ->
#   moi 0,2 s Dv van khoang 0,10 m/s (a khong phu thuoc v0, mo_hinh a = g.sin(alpha)). Khong trung Cau 1-6 cua bai.
from engine import *

T5 = (0.0, 0.2, 0.4, 0.6, 0.8)
VD = (0.20, 0.30, 0.40, 0.49, 0.59)
VS = ("0,20", "0,30", "0,40", "0,49", "0,59")
DV = ("+0,10", "+0,10", "+0,09", "+0,10")
AK = ("0,50", "0,50", "0,45", "0,50")
V0, ACC = 0.20, 0.49

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-gia-toc-01.json")))
    h = k["so_lieu_mau"]["hang"]
    assert [r[0] for r in h] == list(T5) and [r[2] for r in h] == list(VD)
    assert [f"{r[3]:.2f}".replace(".", ",") for r in h[1:]] == list(AK)
    for i in range(4): assert abs(VD[i + 1] - VD[i] - float(DV[i][1:].replace(",", "."))) < 1e-9
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["v0"]["mac_dinh"] == V0 and ts["v0"]["min"] <= 0.40 <= ts["v0"]["max"]
    assert abs(9.8 * ts["sin_alpha"]["mac_dinh"] - ACC) < 1e-9
_kiem_so()

C_T, C_V, C_D = (29, 78, 216), (176, 64, 8), (15, 118, 110)
DRED = (185, 28, 28); EMPTY = (148, 140, 128)
CART = (100, 116, 139); CART_D = (51, 65, 85); RAIL = (203, 207, 218); RAIL_D = (148, 153, 168)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

# ---------------- do thi v-t (o tren) ----------------
GBOX = (40, 205, 1040, 900)
GX0, GYB, SV = 200, 800, 850
def GXt(t): return GX0 + t * 900
def GYv(v): return GYB - v * SV

def graph(d, n, steps=0, dvlab=0, vlab=(), ring=(), q=False, vmax=0.6):
    card(d, GBOX, fill=WHITE, outline=LIGHT, w=3)
    for v in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
        if v <= vmax + 1e-9: d.line([(GX0, GYv(v)), (GXt(0.8) + 20, GYv(v))], fill=(240, 236, 228), width=2)
    arrow(d, (GX0, GYB), (GXt(0.8) + 80, GYB), NAVY, w=5, head=18)
    arrow(d, (GX0, GYB), (GX0, GYv(0.6) - 40), NAVY, w=5, head=18)
    for t in T5[1:]:
        d.line([(GXt(t), GYB), (GXt(t), GYB + 12)], fill=NAVY, width=4)
        text(d, (GXt(t), GYB + 48), vn(t, 1), 56, C_T)
    for v in (0.2, 0.4, 0.6):
        if v <= vmax + 1e-9:
            d.line([(GX0 - 12, GYv(v)), (GX0, GYv(v))], fill=NAVY, width=4)
            text(d, (GX0 - 22, GYv(v)), vn(v, 1), 56, C_V, anchor="rm")
    text(d, (1030, GYB - 50), "t (s)", 58, C_T, anchor="rm")
    text(d, (GX0 + 25, GYv(0.6) - 30), "v (m/s)", 58, C_V, anchor="lm")
    if q:
        x = GXt(0.8)
        card(d, (x - 34, GYB - 230, x + 34, GYB - 140), fill=WHITE, outline=INK, r=14, w=5)
        text(d, (x, GYB - 185), "?", 62, INK)
    for i in range(min(steps, n - 1)):
        x0, y0 = GXt(T5[i]), GYv(VD[i]); x1, y1 = GXt(T5[i + 1]), GYv(VD[i + 1])
        for xx in range(int(x0) + 16, int(x1), 24): d.line([(xx, y0), (min(xx + 12, x1), y0)], fill=C_D, width=5)
        d.line([(x1, y0), (x1, y1 + 16)], fill=C_D, width=8)
        if i < dvlab:
            if i < 3: text(d, (x1 + 12, (y0 + y1) / 2), DV[i], 56, C_D, anchor="lm")
            else: text(d, (x1 - 16, (y0 + y1) / 2 + 6), DV[i], 56, C_D, anchor="rm")
    for i in range(n):
        x, y = GXt(T5[i]), GYv(VD[i])
        if i in ring: d.ellipse([x - 34, y - 34, x + 34, y + 34], outline=NAVY, width=6)
        dot(d, x, y, 16, C_V, WHITE)
        if i in vlab:
            if i == 0: text(d, (x + 24, y - 44), VS[i], 56, C_V, anchor="lm")
            else: text(d, (x - 24, y - 44), VS[i], 56, C_V, anchor="rm")

# ---------------- mang + cam bien (o giua) ----------------
RBOX = (40, 915, 1040, 1180)
R0, R1 = (90, 1040), (1010, 1088)
RL = math.hypot(R1[0] - R0[0], R1[1] - R0[1])
RU = ((R1[0] - R0[0]) / RL, (R1[1] - R0[1]) / RL); RN = (RU[1], -RU[0])
def RP(s, h): return (R0[0] + RU[0] * s + RN[0] * h, R0[1] + RU[1] * s + RN[1] * h)
P0, PXM, PSTOP = 330, 1700, 880

def rig(d, front, ping=0.0):
    card(d, RBOX, fill=WHITE, outline=LIGHT, w=3)
    d.polygon([RP(-10, -22), RP(110, -22), (RP(110, -22)[0], 1155), (RP(-10, -22)[0], 1155)], fill=(226, 220, 206))
    d.line([(60, 1155), (1020, 1155)], fill=RAIL_D, width=4)
    d.polygon([RP(0, 0), RP(RL, 0), RP(RL, -22), RP(0, -22)], fill=RAIL, outline=RAIL_D)
    d.polygon([RP(PSTOP + 6, 0), RP(PSTOP + 22, 0), RP(PSTOP + 22, 46), RP(PSTOP + 6, 46)], fill=CART_D)
    d.polygon([RP(14, 4), RP(74, 4), RP(74, 64), RP(14, 64)], fill=NAVY)
    d.polygon([RP(74, 18), RP(84, 18), RP(84, 50), RP(74, 50)], fill=(120, 130, 160))
    text(d, (420, 955), "cảm biến", 56, INK, anchor="rm")
    if ping > 0:
        c = RP(84, 34)
        for k in range(3):
            r = 30 + 34 * k
            d.arc([c[0] - r, c[1] - r, c[0] + r, c[1] + r], -40, 40, fill=A(C_V, ping), width=6)
    p = min(front, PSTOP)
    d.polygon([RP(p - 150, 12), RP(p, 12), RP(p, 64), RP(p - 150, 64)], fill=CART, outline=CART_D)
    for sw in (p - 118, p - 32):
        c = RP(sw, 8); d.ellipse([c[0] - 13, c[1] - 13, c[0] + 13, c[1] + 13], fill=CART_D)

def front_at(tau):
    tau = max(tau, -V0 / ACC)
    return P0 + (V0 * tau + 0.5 * ACC * tau * tau) * PXM

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

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    graph(d, 2 if t > 1.0 else (1 if t > 0.5 else 0), vlab=(0, 1), q=True)
    rig(d, front_at(0.0))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1195 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 395), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 22, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 165), "Lúc t = 0,8 s,", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "v bằng bao nhiêu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 300, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (chieu cham x5) ----------------
RUN0, SLOW = 0.5, 5.0
PRE = V0 / ACC
def tau_at(t): return (t - RUN0) / SLOW - PRE
def rec_k(t):
    tau = tau_at(t)
    return -1 if tau < -1e-9 else min(4, int(tau / 0.2 + 1e-6))

def s_do(img, d, t, sc):
    tau = tau_at(t); k = rec_k(t); n = k + 1
    graph(d, n, steps=max(0, n - 1), dvlab=max(0, n - 1), vlab=range(n))
    ping = 1.0 - clamp((tau - 0.2 * k) * SLOW / 0.6) if k >= 0 else 0.0
    rig(d, front_at(tau) if t >= RUN0 else front_at(-PRE), ping)
    card(d, (40, 1200, 1040, 1330), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 1265), "chiếu chậm ×5", 58, INK, anchor="lm")
    text(d, (1000, 1265), "ghi lúc " + ("…" if k < 0 else vn(T5[k], 1) + " s"), 58, C_T, anchor="rm")

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    graph(d, 5, steps=4, dvlab=4, vlab=range(5), ring=(4,))
    ka = appear(t, 0.15, 0.4)
    card(d, (40, 915, 1040, 1590), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 945, "ĐÁP ÁN", C_D, ka)
    text(d, (W / 2, 1120), "Khoảng 0,60 m/s", 66, C_V, alpha=ka)
    k2 = appear(t, M[1] + 0.1, 0.45)
    text(d, (W / 2, 1300), "0,20 + 4 × 0,10", 64, C_D, alpha=k2)
    text(d, (W / 2, 1400), "≈ 0,60 m/s", 64, C_D, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    graph(d, 5, steps=4, dvlab=4, vlab=())
    card(d, (40, 915, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 990), "Δv/Δt (m/s²), Δt = 0,2 s", 58, C_D)
    for i in range(4):
        ki = appear(t, 0.6 + 0.3 * i, 0.3)
        text(d, (180 + i * 240, 1110), AK[i], 62, C_D, alpha=ki)
    kb = appear(t, M[1] + 0.1, 0.45)
    if kb > 0:
        card(d, (80, 1200, 1000, 1550), fill=A((236, 253, 243), kb), r=24)
        text(d, (W / 2, 1310), "Gần như không đổi", 62, GREEN, alpha=kb)
        text(d, (W / 2, 1430), "= gia tốc a", 62, GREEN, alpha=kb)

# ---------------- canh 5: Bay (v/t = doc tu goc O) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    graph(d, 5, vlab=(2,), vmax=0.6)
    k1 = ease((t - 0.4) / 0.8)
    if k1 > 0:
        te = 0.6 * k1; d.line([(GXt(0), GYv(0)), (GXt(te), GYv(te * 1.0))], fill=DRED, width=9)
    card(d, (40, 915, 1040, 1240), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 1000), "✗ v/t = 0,40 : 0,4", 62, DRED)
    text(d, (W / 2, 1110), "= 1,0 m/s²", 62, DRED)
    if t >= M[1] - 0.1:
        k2 = ease((t - M[1]) / 0.8)
        d.line([(GXt(0), GYv(VD[0])), (GXt(0.8 * k2), GYv(VD[0] + (VD[4] - VD[0]) * k2))], fill=C_D, width=9)
        d.line([(GX0 + 20, GYv(0)), (GX0 + 20, GYv(VD[0]))], fill=C_V, width=10)
        card(d, (40, 1265, 1040, 1590), fill=WHITE, outline=C_D, w=6)
        text(d, (W / 2, 1350), "✓ Δv/Δt = 0,10 : 0,2", 62, C_D)
        text(d, (W / 2, 1460), "= 0,50 m/s²", 62, C_D)

# ---------------- canh 6: Chua noi duoc ----------------
def ramp(d, x0, y0, L, ang, col):
    a = math.radians(ang); x1, y1 = x0 + L * math.cos(a), y0 + L * math.sin(a)
    d.polygon([(x0, y0), (x1, y1), (x0, y1)], fill=col)
    return x1, y1

def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 450), "Nghiêng hơn thì a ra sao?", 62, INK)
    card(d, (40, 590, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    ang = 8 + 17 * ease((t - 0.6) / 1.6)
    d.line([(100, 1210), (980, 1210)], fill=RAIL_D, width=5)
    x0 = 130; y0 = 1210 - 820 * math.sin(math.radians(ang))
    a = math.radians(ang); x1 = x0 + 820 * math.cos(a)
    d.polygon([(x0, y0), (x1, 1210), (x0, 1210)], fill=(226, 220, 206))
    d.line([(x0, y0), (x1, 1210)], fill=RAIL_D, width=8)
    text(d, (820, 760), "a = ?", 64, C_D, alpha=appear(t, 2.2, 0.4))

# ---------------- canh 7: Chot + THU NGHI (= cau_chot khung web) ----------------
EX0, EYB = 220, 1340
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "Cùng máng, nhưng lúc t = 0", 60, INK, alpha=k)
    text(d, (W / 2, 485), "xe đã có v = 0,40 m/s.", 60, INK, alpha=k)
    text(d, (W / 2, 590), "Lúc t = 0,6 s, v = ?", 64, C_V, alpha=k)
    sx, sv = 1150, 620                                        # px/s, px/(m/s)
    X_ = lambda tt: EX0 + tt * sx; Y_ = lambda v: EYB - v * sv
    d.line([(EX0, EYB), (X_(0.68), EYB)], fill=A(NAVY, k), width=5); d.line([(EX0, EYB), (EX0, Y_(0.8))], fill=A(NAVY, k), width=5)
    for tt in (0.2, 0.4, 0.6):
        d.line([(X_(tt), EYB), (X_(tt), EYB + 12)], fill=A(NAVY, k), width=4); text(d, (X_(tt), EYB + 48), vn(tt, 1), 56, C_T, alpha=k)
    for v in (0.2, 0.4):
        d.line([(EX0 - 12, Y_(v)), (EX0, Y_(v))], fill=A(NAVY, k), width=4); text(d, (EX0 - 22, Y_(v)), vn(v, 1), 56, C_V, anchor="rm", alpha=k)
    text(d, (EX0 + 25, Y_(0.8) + 10), "v (m/s)", 58, C_V, anchor="lm", alpha=k)
    text(d, (1020, EYB - 45), "t (s)", 58, C_T, anchor="rm", alpha=k)
    dot(d, X_(0), Y_(0.40), 16, A(C_V, k), WHITE)
    for xx in range(int(X_(0)) + 16, int(X_(0.2)), 24): d.line([(xx, Y_(0.40)), (min(xx + 12, X_(0.2)), Y_(0.40))], fill=A(C_D, k), width=5)
    text(d, (X_(0.2) + 50, Y_(0.40) - 70), "?", 80, C_D, alpha=k)
    seg_bar(d, 1470, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + RUN0 + (PRE + 0.2 * i) * SLOW, "tap") for i in range(5)]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-gia-toc-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động biến đổi. Gia tốc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe lăn xuống máng nghiêng", draw=s_hook, tail=0.3, caps=[
   ("Cảm biến ghi v mỗi 0,2 s.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Xe chạy, cảm biến ghi.", 3.2),
   ("Mỗi lần ghi: thêm một điểm.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đo được 0,59 m/s.", 3.0),
   ("Bốn bậc Δv gần bằng nhau.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Chia Δv cho Δt từng khoảng.", 3.2),
   ("Xe nhanh dần đều.", 3.2)]),
 dict(key="bay", title="Bẫy: lấy v chia t", draw=s_bay, tail=0.3, caps=[
   ("Lấy v chia t được không?", 3.4),
   ("Lúc t = 0 xe đã có 0,20 m/s.", 3.6)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Mới thử một độ nghiêng.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Nhanh dần đều: v tăng đều theo t.", 6.2)]),
])
