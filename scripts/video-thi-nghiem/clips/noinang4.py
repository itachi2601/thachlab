# Clip: tn-l12-noinang-04 - Xilanh cach nhiet: keo pit-tong ra, day vao; hai ngan co vach (ban 3, 21/11/2026)
# Ban 3 (viec 4 lo 20, cong moi): danh quan niem sai "cach nhiet (Q = 0) nen noi nang khong doi (dU = 0)".
#   Du doan cu (nen nhanh -> T?) da bi Cau 2 cua bai tra loi san (bom nhanh, day ong nong nhat) -> doi sang KEO RA:
#   khi o 50 cm3, ~476 K (hang "Giu pit-tong dung yen" cua kho), keo nhanh ra 100 cm3 -> T? (dap an: giam, ve 300 K).
#   Khong trung quiz mo bai (hai am nuoc), Cau 1-5, Tra bai (cau 6 hoi nen nhanh, khong hoi keo ra).
#   Chu than canh ve >= 56 (ra >= 49 px), khong chu MUTED, khong nut A-D (K10), dong "Dung lai, tu doan", thanh dem >= 70 px.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-noinang-04.json (so_lieu_mau), kiem bang _kiem_so():
#   Giu yen 50 cm3, 476 K | Keo ve 100 cm3, 300 K, A ~ -8,8 J, Q = 0, dU ~ -8,8 J (so voi hang tren)
#   Nen nhanh 100 -> 50 cm3, 300 -> 476 K, A ~ +8,8 J, Q = 0, dU ~ +8,8 J
#   Hai ngan 50 cm3, 300 K -> rut vach 100 cm3, 300 K, A = Q = dU = 0.
# Bay = hien_tuong_hay_sai[3]: "V gap doi thi khi lanh di" -> dung khi khi day pit-tong, sai khi tran vao chan khong.
# Chua noi duoc = khong_chung_minh[0] (thanh xilanh that dan nhiet cham).
# THU NGHI (= cau_chot khung web): khi li tuong, xilanh DAN nhiet, nen cham, T giu 300 K -> Q duong hay am?
#   Dap an: am (dU = 0 vi T khong doi, A > 0 nen Q = -A < 0). Man khong ve mui ten nhiet, khong ghi dU = 0.
from engine import *

NOTE = (70, 75, 95)
WALL = (255, 226, 190); HATCH = (190, 100, 30)
DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (76, 29, 149)
FS, FM = 58, 56          # co chu than canh (ve) -> 51 / 49 px trong mp4

T_NEN = 476              # K, sau khi nen 100 -> 50 cm3 (kho)
DU = 8.8                 # J


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-noinang-04.json")))
    h = {r[0]: r for r in k["so_lieu_mau"]["hang"]}
    assert h["Ban đầu"][1:3] == [100, 300]
    assert h["Sau khi nén nhanh"][1:3] == [50, T_NEN] and h["Sau khi nén nhanh"][4:] == [DU, 0, DU]
    assert h["Giữ pit-tông đứng yên"][1:3] == [50, T_NEN]
    assert h["Kéo pit-tông về"][1:3] == [100, 300] and h["Kéo pit-tông về"][4:] == [-DU, 0, -DU]
    assert h["Hai ngăn, trước khi rút vách"][1:3] == [50, 300]
    assert h["Hai ngăn, sau khi rút vách"][1:3] == [100, 300] and h["Hai ngăn, sau khi rút vách"][4:] == [0, 0, 0]
    assert abs(300 * 2 ** (2 / 3) - T_NEN) < 0.5 and abs(1.5 * 0.004 * 8.31 * (T_NEN - 300) - DU) < 0.05
_kiem_so()


def vn(x):
    if abs(x) < 1e-9: return "0"
    return ("≈ " + f"{x:+.1f}").replace(".", ",").replace("-", "−")


def hatch_h(d, x0, x1, y0, y1, step=22, col=HATCH, fill=WALL):
    d.rectangle([x0, y0, x1, y1], fill=fill)
    h = y1 - y0; x = x0
    while x < x1:
        xa, xb = x, min(x + h, x1); d.line([(xa, y1), (xb, y1 - (xb - xa))], fill=col, width=3); x += step
    d.rectangle([x0, y0, x1, y1], outline=NAVY, width=3)


def hatch_v(d, x0, x1, y0, y1, step=22, col=HATCH, fill=WALL):
    d.rectangle([x0, y0, x1, y1], fill=fill)
    w = x1 - x0; y = y0 + w
    while y < y1 + w:
        ya = min(y, y1); xa = x0 + (y - ya)
        d.line([(xa, ya), (x1, max(y - w, y0))], fill=col, width=3); y += step
    d.rectangle([x0, y0, x1, y1], outline=NAVY, width=3)


# ---- phan tu khi: vi tri xac dinh (seed co dinh), toc do ~ sqrt(T) ----
random.seed(4)
MOL = [(random.random(), random.random(), random.uniform(0.18, 0.32) * random.choice((1, -1)),
        random.uniform(0.18, 0.32) * random.choice((1, -1))) for _ in range(26)]


def phase(t, Tfun, dt=0.05):
    """tich phan sqrt(T/300) theo thoi gian -> quang duong 'chuan hoa' (khong nhay khi T doi)."""
    s, tau = 0.0, 0.0
    while tau < t:
        h = min(dt, t - tau); s += math.sqrt(Tfun(tau) / 300.0) * h; tau += h
    return s


def gas(d, s, xl, xr, yt, yb, n=26, r=10, col=BLUE):
    for u0, v0, vu, vv in MOL[:n]:
        u = refl(u0 + vu * s, 0, 1); v = refl(v0 + vv * s, 0, 1)
        dot(d, xl + r + 2 + u * (xr - xl - 2 * r - 4), yt + r + 2 + v * (yb - yt - 2 * r - 4), r, col)


def cyl(d, V, s, x0=150, yt=360, yb=600, L=560, wall=26, rod=224, push=0, n=26, r=10):
    """Xilanh nam ngang cach nhiet, day trai kin, pit-tong ben phai. V (cm3): 100 <-> L px. push: -1 day vao, +1 keo ra."""
    xr_wall = x0 + L + 90
    hatch_h(d, x0 - wall, xr_wall, yt - wall, yt); hatch_h(d, x0 - wall, xr_wall, yb, yb + wall); hatch_v(d, x0 - wall, x0, yt, yb)
    xp = x0 + L * V / 100.0
    gas(d, s, x0, xp, yt, yb, n=n, r=r)
    hatch_v(d, xp, xp + wall, yt + 2, yb - 2)
    ym = (yt + yb) / 2
    d.rectangle([xp + wall, ym - 10, xp + wall + rod, ym + 10], fill=NAVY)
    d.rounded_rectangle([xp + wall + rod, ym - 50, xp + wall + rod + 24, ym + 50], radius=8, fill=NAVY)
    if push:
        ya = yt - 50
        if push < 0: arrow(d, (xp + wall + rod, ya), (xp + wall + 60, ya), RED, w=8, head=24)
        else: arrow(d, (xp + wall + 60, ya), (xp + wall + rod, ya), RED, w=8, head=24)
    return xp


def readout(d, vals, y, alpha=1.0):
    for (a, b), s in zip(((90, 520), (560, 990)), vals):
        card(d, (a, y - 48, b, y + 48), fill=A(WHITE, alpha), outline=A(NAVY, alpha), r=24, w=4)
        text(d, ((a + b) / 2, y), s, FS, INK, alpha=alpha)


def countdown(d, y, t, tc, tend, a=1.0):
    if t <= tc: return
    p = clamp((t - tc) / (tend - tc))
    d.rounded_rectangle([110, y, 970, y + 70], radius=35, fill=A((237, 233, 254), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(70, 860 * (1 - p)), y + 70], radius=35, fill=A(DPURP, a))


def pill(d, s, y, a, color=NAVY, size=FM):
    if a <= 0: return
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    xp = cyl(d, 50, phase(t, lambda _: T_NEN))
    text(d, (124, 290), "cách nhiệt", FS, HATCH, anchor="lm")
    if t >= M[1] - 0.2:                                   # vach dich 100 cm3 (net dut)
        xg = 150 + 560
        for y in range(366, 594, 30): d.line([(xg, y), (xg, y + 15)], fill=PURPLE, width=6)
    readout(d, ("V = 50 cm³", "T ≈ 476 K"), 730)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 850 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, color=PURPLE)
    for j, s in enumerate(("Kéo pit-tông ra", "tới vạch 100 cm³.", "Nhiệt độ khí thế nào?")):
        text(d, (W / 2, y0 + 170 + j * 78), s, 60, INK, alpha=a)
    countdown(d, y0 + 410, t, M[1] + 0.3, sc["T"] - 0.1, a)


# ---------------- canh 2: Tien hanh ----------------
K0, K1 = 0.6, 1.8          # keo ra 50 -> 100
R1 = 2.3                   # hang "Keo ra"
P0, P1 = 3.5, 4.7          # day vao 100 -> 50
R2 = 5.0                   # hang "Day vao"
HQ = 6.5                   # to cot Q


def V_at(t):
    if t < K0: return 50.0
    if t < K1: return lerp(50, 100, ease((t - K0) / (K1 - K0)))
    if t < P0: return 100.0
    if t < P1: return lerp(100, 50, ease((t - P0) / (P1 - P0)))
    return 50.0


def T_at(t):  # chi de phan tu chay nhanh/cham (khong in so trung gian): T.V^(2/3) khong doi (mo_hinh)
    return 300.0 * (100.0 / V_at(t)) ** (2.0 / 3.0)


ROWS = (("Kéo ra", -DU, 0, -DU), ("Đẩy vào", DU, 0, DU))
COLX = (200, 480, 700, 900)


def table(d, y0, ks, hlq=0.0):
    rh = 96; h = 92 + rh * 2 + 10
    card(d, (40, y0, 1040, y0 + h), fill=WHITE, outline=LIGHT, w=3)
    if hlq > 0:
        d.rounded_rectangle([620, y0 + 10, 780, y0 + h - 10], radius=18, fill=A((255, 237, 213), hlq), outline=A(ORANGE, hlq), width=5)
    for x, s in zip(COLX[1:], ("A (J)", "Q (J)", "ΔU (J)")): text(d, (x, y0 + 48), s, FS, NAVY)
    d.line([(70, y0 + 92), (1010, y0 + 92)], fill=LIGHT, width=3)
    for j, (r, k) in enumerate(zip(ROWS, ks)):
        if k <= 0: continue
        yy = y0 + 92 + rh * (j + 0.5) + 4
        text(d, (COLX[0], yy), r[0], FS, INK, alpha=k)
        for x, v in zip(COLX[1:], r[1:]):
            col = DGREEN if v > 0 else (DRED if v < 0 else INK)
            text(d, (x, yy), vn(v), FS, col, alpha=k)


def s_do(img, d, t, sc):
    V = V_at(t)
    push = 1 if K0 - 0.3 < t < K1 else (-1 if P0 - 0.3 < t < P1 else 0)
    cyl(d, V, phase(t, T_at), push=push)
    if t < K0: vals = ("V = 50 cm³", "T ≈ 476 K")
    elif t < K1: vals = ("V ↑", "T ↓")
    elif t < P0: vals = ("V = 100 cm³", "T = 300 K")
    elif t < P1: vals = ("V ↓", "T ↑")
    else: vals = ("V = 50 cm³", "T ≈ 476 K")
    readout(d, vals, 730)
    table(d, 820, [appear(t, R1, 0.4), appear(t, R2, 0.4)], hlq=appear(t, HQ, 0.4))
    text(d, (W / 2, 1180), "A, Q: phần khí nhận vào", FS, NAVY)
    text(d, (W / 2, 1280), "ΔU = A + Q", 66, INK)
    text(d, (W / 2, 1385), "số liệu mô hình", FM, NOTE)


# ---------------- canh 3: Dap an + rut ra ----------------
MECH = 4.4


def s_dapan(img, d, t, sc):
    ka = appear(t, 0.1, 0.4)
    pill(d, "ĐÁP ÁN · Giảm", 300, ka)
    text(d, (W / 2, 405), "476 K  →  300 K", 66, DRED, alpha=ka)
    k1 = appear(t, 2.2, 0.45)
    if k1 > 0:
        card(d, (40, 470, 1040, 800), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
        for j, (s, col) in enumerate((("Q = 0 · cách nhiệt", ORANGE), ("A < 0 · đẩy pit-tông", DRED), ("ΔU = A < 0 → T giảm", DRED))):
            text(d, (90, 530 + j * 100), s, FS, col, anchor="lm", alpha=k1)
    k2 = appear(t, MECH, 0.5)
    if k2 > 0:
        card(d, (40, 840, 1040, 1300), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
        # pit-tong lui dan sang phai (lap 2 s); phan tu toi nhanh, bat ve cham
        cyc = ((t - MECH) % 2.4) / 2.4
        px = 690 + 60 * cyc
        hatch_v(d, px, px + 30, 880, 1260)
        arrow(d, (px + 50, 900), (px + 170, 900), A(RED, k2), w=8, head=22)
        # mot phan tu (cham to) chay tren MOT duong y = 1070: toi nhanh (0,9 s), bat ve cham (1,5 s); nhan ngay tren/duoi duong
        xw = px - 28                                          # cho cham cham pit-tong
        if cyc < 0.375: xd = lerp(250, xw, cyc / 0.375)
        else: xd = lerp(xw, xw - 260, (cyc - 0.375) / 0.625)
        d.line([(200, 1070), (px, 1070)], fill=A(LIGHT, k2), width=4)
        arrow(d, (230, 990), (560, 990), A(BLUE, k2), w=8, head=24)
        text(d, (180, 990), "v", 64, BLUE, alpha=k2)
        arrow(d, (640, 1150), (470, 1150), A(BLUE, k2), w=8, head=24)
        text(d, (320, 1150), "v′ < v", FS, BLUE, alpha=k2)
        dot(d, xd, 1070, 26, A(BLUE, k2))


# ---------------- canh 4: Bay + chua noi duoc ----------------
BT = 3.4                    # khung duoi (rut vach) hien
VL0, VL1 = 5.0, 5.5         # vach rut len
SP0, SP1 = 5.5, 6.8         # khi tran sang
BR = 7.2                    # ket qua khung duoi + gach cau bay
BC = 10.2                    # chua noi duoc


def strike(d, y, s, size, ks, alpha):
    text(d, (W / 2, y), s, size, mix(INK, GRAY, ks), alpha=alpha)
    if ks > 0:
        lw = tw(d, s, F(size))
        d.line([(W / 2 - lw / 2 - 8, y + 2), (W / 2 - lw / 2 - 8 + (lw + 16) * ks, y + 2)], fill=A(DRED, 0.9 * alpha), width=6)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pill(d, "BẪY", 300, a1, color=DRED)
    strike(d, 400, "“V gấp đôi thì khí lạnh đi”", 60, clamp((t - BR) / 0.4), a1)
    # khung tren: keo pit-tong 50 -> 100 cm3 (dung la lanh di)
    card(d, (40, 460, 1040, 880), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    if a1 > 0:
        kv = ease((t - 0.5) / 1.2)
        V = lerp(50, 100, kv)
        cyl(d, V, phase(t, lambda tt: 300 * (100 / lerp(50, 100, ease((tt - 0.5) / 1.2))) ** (2 / 3)),
            x0=130, yt=560, yb=720, L=440, wall=22, rod=150, push=1 if t < 1.8 else 0, n=16, r=9)
        text(d, (W / 2, 815), "A < 0 · 476 K → 300 K", FS, DRED, alpha=a1)
    # khung duoi: rut vach, khi tran vao chan khong
    a2 = appear(t, BT, 0.45)
    if a2 > 0:
        card(d, (40, 910, 1040, 1360), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        x0, x1, y0, y1, mid = 130, 870, 990, 1160, 500
        hatch_h(d, x0 - 22, x1 + 22, y0 - 22, y0); hatch_h(d, x0 - 22, x1 + 22, y1, y1 + 22)
        hatch_v(d, x0 - 22, x0, y0, y1); hatch_v(d, x1, x1 + 22, y0, y1)
        kr = ease((t - SP0) / (SP1 - SP0))
        gas(d, phase(t, lambda _: 300) * 1.4, x0, lerp(mid - 10, x1, kr), y0, y1, n=16, r=9)
        if kr < 0.5: text(d, ((mid + x1) / 2, (y0 + y1) / 2), "chân không", FM, NOTE, alpha=a2 * (1 - 2 * kr))
        lift = ease((t - VL0) / (VL1 - VL0))
        if lift < 1:
            yv = y0 - lift * 140
            d.rectangle([mid - 10, yv, mid + 10, yv + (y1 - y0)], fill=A(NAVY, a2 * (1 - lift)))
        if VL0 - 0.4 < t < VL1 + 0.6:
            arrow(d, (mid + 50, y0 - 30), (mid + 50, y0 - 120), RED, w=7, head=20)
        k3 = appear(t, BR, 0.45)
        if k3 > 0: text(d, (W / 2, 1290), "A = 0 · 300 K → 300 K", FS, DGREEN, alpha=k3)
    k4 = appear(t, BC, 0.45)
    if k4 > 0:
        card(d, (40, 1395, 1040, 1530), fill=A(WHITE, k4), outline=A(NAVY, k4), w=5)
        text(d, (W / 2, 1462), "Xilanh thật vẫn dẫn nhiệt chậm", FS, NAVY, alpha=k4)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 3.0


def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 262, 1030, 450), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 315), "Cách nhiệt chưa chắc", 60, DGREEN, alpha=k0)
    text(d, (W / 2, 395), "nội năng không đổi", 60, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 480, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 545, k1, color=ORANGE)
    for j, s in enumerate(("Khí lí tưởng, xilanh dẫn nhiệt.", "Nén chậm, T giữ 300 K.", "Q của khí dương hay âm?")):
        text(d, (W / 2, 650 + j * 80), s, 60, INK, alpha=k1)
    if k1 > 0:   # xilanh thuong (thanh xam, khong gach cach nhiet), mui ten nen, so chi T; KHONG ve mui ten nhiet
        x0, x1, y0, y1 = 150, 700, 945, 1135
        d.rectangle([x0 - 18, y0 - 18, x1, y0], fill=A(GRAY, k1)); d.rectangle([x0 - 18, y1, x1, y1 + 18], fill=A(GRAY, k1))
        d.rectangle([x0 - 18, y0, x0, y1], fill=A(GRAY, k1))
        xp = 560 - 40 * ease(((t - END_Q) % 3.0) / 3.0)
        gas(d, phase(t, lambda _: 300) * 0.8, x0, xp, y0, y1, n=12, r=9)
        d.rectangle([xp, y0 + 2, xp + 20, y1 - 2], fill=A(NAVY, k1))
        d.rectangle([xp + 20, (y0 + y1) / 2 - 9, xp + 200, (y0 + y1) / 2 + 9], fill=A(NAVY, k1))
        arrow(d, (xp + 330, y0 - 40), (xp + 200, y0 - 40), A(RED, k1), w=8, head=22)
        card(d, (300, 1200, 780, 1300), fill=A(WHITE, k1), outline=A(NAVY, k1), r=22, w=4)
        text(d, (540, 1250), "T = 300 K", FS, INK, alpha=k1)
    countdown(d, 1380, t, END_Q + 0.5, sc["T"] - 0.1, k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + K0, "tap"), (do["t0"] + P0, "tap"),
            (da["t0"] + 0.1, "ding"),
            (b["t0"] + 0.3, "buzz"), (b["t0"] + VL0, "tap"),
            (e["t0"] + END_Q + 0.1, "open")]


CLIP = dict(id="tn-l12-noinang-04", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Nội năng · Định luật 1 NĐLH · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xilanh cách nhiệt", draw=s_hook, tail=0.3, caps=[
   ("Khí argon đã nén sẵn.", 2.94),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Kéo ra, ghi A, Q, ΔU.", 3.1),
   ("Rồi đẩy về 50 cm³.", 3.0),
   ("Hai lần đều không nhận nhiệt.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Khí sinh công, nội năng giảm.", MECH - 0.4),
   ("Va pit-tông lùi, bật chậm.", 3.37)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Đúng khi đẩy pit-tông.", BT - 0.4),
   ("Rút vách thì sao?", BR - BT),
   ("Không có gì để đẩy.", BC - BR),
   ("Xilanh thật thì sao?", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.1, caps=[
   ("Dừng lại, tự trả lời.", 9.2)]),
])
