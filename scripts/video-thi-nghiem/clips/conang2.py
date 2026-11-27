# Clip: tn-l10-co-nang-bao-toan-02 - Bong ban nay thap dan (ban 2 theo cong moi, 27/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l10-co-nang-bao-toan-02.json:
#   tham_so: h0 = 1,00 m (dai 0,3-1,5), e2 = 0,8, m = 2,7 g; g = 10 m/s2.
#   so_lieu_mau: h_n 1,00 / 0,80 / 0,64 / 0,512 m (bai ghi 0,51) ; W_n = 27,0 / 21,6 / 17,28 / 13,824 mJ (man: 17,3 / 13,8).
# Du doan (K10): tha 1,00 m, dinh 1 = 0,80 m; dinh lan nay thu 3 cao khoang bao nhieu? Dap an ~0,51 m.
# Bay: hien_tuong_hay_sai[0] "co nang bao toan -> nay lai 1,00 m": hai bong canh nhau (nghi 1,00 m / that 0,80 m).
# Cau chot (ghi_chu kho): tha tu 1,50 m, toi dinh 2 co nang giam 40,5 - 25,92 = 14,58 ~ 14,6 mJ (KHONG hien tren man).
import copy
from engine import *

H0, E2, M_KG, G = 1.00, 0.8, 0.0027, 10.0
HM = [H0 * E2 ** n for n in range(4)]
HS = ["1,00", "0,80", "0,64", "0,51"]
WM = [M_KG * G * h * 1000 for h in HM]                      # mJ
def fm(x, n=1): return f"{x:.{n}f}".replace(".", ",")

BALL = (255, 255, 255); BALL_D = (200, 120, 40); STONE = (120, 128, 145); STONE_D = (80, 86, 100)
RULER = (250, 222, 140); RULER_D = (170, 130, 40)
EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

YF, PXM = 1010, 640              # mat ban (y), px ung voi 1 m -> 1,00 m o y 370
XR0, XR1 = 150, 200
XB, RB = 330, 24

def ym(h): return YF - h * PXM

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); w = 780 / n
    for i in range(n):
        x = 150 + i * w
        if i < on: card(d, (x, y, x + w - 20, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w - 20, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def ruler(d):
    d.rectangle([XR0, ym(1.08), XR1, YF], fill=RULER, outline=RULER_D, width=3)
    for i in range(0, 11):
        y = ym(i / 10); L = 30 if i % 2 == 0 else 16
        d.line([(XR1 - L, y), (XR1, y)], fill=RULER_D, width=4)
        if i % 2 == 0 and i > 0: text(d, (XR0 - 10, y), fm(i / 10), 56, INK, anchor="rm")
    text(d, (XR0 + 25, ym(1.08) - 40), "m", 56, INK)

def table_top(d):
    d.rectangle([40, YF, 640, YF + 60], fill=STONE)
    d.rectangle([40, YF + 60, 640, YF + 76], fill=STONE_D)

def ball(d, h, alpha=1.0, x=XB):
    y = ym(h) - RB
    d.ellipse([x - RB, y - RB, x + RB, y + RB], fill=A(BALL, alpha), outline=A(BALL_D, alpha), width=4)

def peak_mark(d, h, lab, color=BLUE, alpha=1.0, x1=420):
    y = ym(h)
    for xx in range(XR1 + 6, x1, 22): d.line([(xx, y), (xx + 12, y)], fill=A(color, alpha), width=4)
    text(d, (x1 + 10, y), lab, 56, color, anchor="lm", alpha=alpha)

SL = 2.0
def _tu(h): return math.sqrt(2 * h / G)
def peak_times():
    out, t = [], _tu(HM[0])
    for h in HM[1:]:
        out.append((t + _tu(h)) * SL); t += 2 * _tu(h)
    return out
PT = peak_times()

def traj(tau):
    if tau <= 0: return HM[0]
    tau = min(tau, PT[2]); t = tau / SL; tf = _tu(HM[0])
    if t < tf: return HM[0] - 0.5 * G * t * t
    t -= tf
    for h in HM[1:]:
        tu = _tu(h)
        if t < 2 * tu: return max(0.0, G * tu * t - 0.5 * G * t * t)
        t -= 2 * tu
    return 0.0
def n_peaks(tau): return sum(1 for p in PT if tau >= p - 1e-9)

# ---------------- canh 1: du doan ----------------
REL0 = 0.6
def s_hook(img, d, t, sc):
    M = sc["M"]; tau = t - REL0
    ruler(d); table_top(d)
    peak_mark(d, HM[0], "thả 1,00 m", INK)
    if tau < PT[0] + 0.5: ball(d, traj(min(tau, PT[0])))
    else: ball(d, HM[0], appear(t, REL0 + PT[0] + 0.5, 0.5))
    if tau >= PT[0]: peak_mark(d, HM[1], "đỉnh 1: 0,80 m", BLUE, appear(t, REL0 + PT[0], 0.3))
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1150 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 480), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 170), "Đỉnh lần nảy thứ 3", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 260), "cao khoảng bao nhiêu?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 360, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: tien hanh + dap an ----------------
REL1 = 0.5
def row_t(j): return 0.0 if j == 0 else REL1 + PT[j - 1]

def s_do(img, d, t, sc):
    M = sc["M"]; tau = t - REL1
    ruler(d); table_top(d)
    peak_mark(d, HM[0], "thả", INK)
    for j in range(1, 4):
        if tau >= PT[j - 1]: peak_mark(d, HM[j], f"đỉnh {j}", BLUE, appear(t, row_t(j), 0.25))
    ball(d, traj(tau))
    ka = appear(t, M[1], 0.4); kx = appear(t, M[1] + 2.5, 0.4)
    x0, x1 = 660, 1040
    card(d, (x0, 330, x1, 960), fill=WHITE, outline=NAVY, w=4)
    text(d, (750, 390), "lần", 56, INK); text(d, (935, 390), "đỉnh", 56, INK)
    d.line([(x0 + 20, 435), (x1 - 20, 435)], fill=LIGHT, width=4)
    for j in range(4):
        a = appear(t, row_t(j), 0.3); y = 510 + j * 120
        if a <= 0: continue
        if j == 3 and ka > 0: d.rounded_rectangle([x0 + 10, y - 44, x1 - 10, y + 44], radius=16, fill=A((220, 252, 231), ka))
        text(d, (750, y), "thả" if j == 0 else str(j), 58, INK, alpha=a)
        text(d, (935, y), HS[j], 60, BLUE if j else INK, alpha=a)
    if kx > 0:                                             # x0,8 giua cac hang (chu don, hinh doi)
        for j in range(3):
            y = 510 + j * 120 + 60
            d.line([(x0 - 10, y - 40), (x0 + 6, y), (x0 - 10, y + 40)], fill=A(GREEN, kx), width=5)
    if ka > 0:
        card(d, (60, 1150, 1020, 1300), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1225), "Đáp án: khoảng 0,51 m", 62, GREEN, alpha=ka)
    if kx > 0:
        card(d, (60, 1340, 1020, 1490), fill=A(WHITE, kx), outline=A(GREEN, kx), r=28, w=4)
        text(d, (W / 2, 1415), "Nhân 0,8, không trừ đều", 60, INK, alpha=kx)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.3, 0.4)
    card(d, (40, 230, 1040, 440), fill=A(WHITE, k0), outline=A(BLUE, k0), w=4)
    text(d, (W / 2, 290), "Ở đỉnh v = 0: W = mgh", 60, INK, alpha=k0)
    text(d, (W / 2, 380), "m = 2,7 g; g = 10 m/s²", 58, BLUE, alpha=k0)
    kb = appear(t, 2.6, 0.4)
    if kb > 0:
        card(d, (40, 470, 1040, 1180), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        text(d, (W / 2, 530), "W ở đỉnh (mJ)", 58, INK, alpha=kb)
        base, hmax, wmax = 1050, 300, WM[0]
        xs = [190, 410, 630, 850]
        for j in range(4):
            g = ease((t - 2.8 - j * 0.35) / 0.4)
            text(d, (xs[j], base + 62), "thả" if j == 0 else f"đỉnh {j}", 56, INK, alpha=kb)
            d.rectangle([xs[j] - 40, base - hmax, xs[j] + 40, base], outline=A(LIGHT, kb), width=3)
            if g > 0:
                hh = hmax * WM[j] / wmax * g
                if hh > 2: d.rectangle([xs[j] - 40, base - hh, xs[j] + 40, base], fill=BLUE)
                text(d, (xs[j], base - hmax * WM[j] / wmax - 40), fm(WM[j]), 56, BLUE, alpha=clamp(g * 2 - 1))
        kc = appear(t, M[1], 0.4)
        if kc > 0:
            for j in range(3):
                xm = (xs[j] + xs[j + 1]) / 2; yb = 625
                card(d, (xm - 78, yb - 34, xm + 78, yb + 34), fill=A((254, 242, 242), kc), r=14)
                text(d, (xm, yb), "−20%", 56, RED, alpha=kc)
    kd = appear(t, M[1] + 2.5, 0.4)
    if kd > 0:
        card(d, (40, 1220, 1040, 1370), fill=A((254, 242, 242), kd), outline=A(RED, kd), r=28, w=4)
        text(d, (W / 2, 1295), "Phần mất: thành nhiệt, âm", 60, RED, alpha=kd)

# ---------------- canh 4: bay + gioi han ----------------
XA, XT = 330, 520
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    ruler(d); table_top(d)
    # hai bong canh nhau, cung tha 1,00 m: (nghi) lai len 1,00 m - (that) len 0,80 m; lap lai cho hinh luon dong
    ph = (t % 3.2) / 3.2
    def hb(top):                                               # roi tu 1,00 m, nay len top, ve lai tren cung
        if ph < 0.45: return HM[0] * (1 - (ph / 0.45) ** 2)
        u = (ph - 0.45) / 0.55; return top * (1 - (1 - u) ** 2)
    kk = appear(t, 0.3, 0.4)
    for y in (ym(HM[0]), ym(HM[1])):
        for xx in range(XR1 + 6, 700, 22): d.line([(xx, y), (xx + 12, y)], fill=A(GRAY, kk), width=3)
    ball(d, hb(HM[0]), 0.9 * kk, x=XA)
    ball(d, hb(HM[1]), kk, x=XT)
    text(d, (XA, YF + 120), "nghĩ", 56, RED, alpha=kk)
    text(d, (XT, YF + 120), "thật", 56, GREEN, alpha=kk)
    text(d, (720, ym(HM[0])), "1,00 m", 56, RED, anchor="lm", alpha=kk)
    text(d, (720, ym(HM[1])), "0,80 m", 56, GREEN, anchor="lm", alpha=kk)
    ks = clamp((t - mk) / 0.4)
    if ks > 0:                                                 # gach bong "nghi"
        y = ym(HM[0]) - RB
        for s in (1, -1): d.line([(XA - 40, y - 40 * s), (XA - 40 + 80 * ks, y - 40 * s + 80 * s * ks)], fill=RED, width=7)
    k0 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3); y = 1200
    if a1 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        q = "“Bảo toàn: nảy lại 1,00 m”"
        lw = tw(d, q, F(60)); yy = y + 190
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        k2 = appear(t, mk + 0.2, 0.45)
        if k2 > 0: text(d, (W / 2, y + 320), "Va chạm lấy bớt cơ năng", 60, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 210), "Mới thử một mặt bàn", 62, INK, alpha=k3)

# ---------------- canh 5: thu nghi (cau chot o khung: 14,6 mJ) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1620), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    # bong nho nay lien tuc (hinh dong), khong ve do cao dinh
    ph = (t % 1.6) / 1.6; yb = 820 - 380 * (1 - (2 * ph - 1) ** 2)
    d.rectangle([380, 850, 700, 890], fill=A(STONE, k))
    d.ellipse([540 - 30, yb - 30, 540 + 30, yb + 30], fill=A(BALL, k), outline=A(BALL_D, k), width=4)
    text(d, (W / 2, 980), "Cùng bóng, thả từ 1,50 m.", 62, INK, alpha=k)
    text(d, (W / 2, 1070), "m = 2,7 g; g = 10 m/s²", 58, INK, alpha=k)
    text(d, (W / 2, 1190), "Tới đỉnh 2, cơ năng", 64, DORANGE, alpha=k)
    text(d, (W / 2, 1280), "giảm bao nhiêu mJ?", 64, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + REL0, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding"),
            (do["t0"] + REL1, "tap"), (do["t0"] + do["M"][1], "ding"), (r["t0"] + r["M"][1], "tap"),
            (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-co-nang-bao-toan-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng và bảo toàn cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bóng bàn nảy trên bàn đá", draw=s_hook, tail=0.3, caps=[
   ("Thả bóng bàn, đọc đỉnh lần 1.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Quay chậm, đọc từng đỉnh", draw=s_do, tail=0.5, caps=[
   ("Thả nhẹ, không ném.", 5.4),
   ("Mỗi đỉnh còn khoảng 80 % đỉnh trước.", 4.6)]),
 dict(key="rut", title="Cơ năng ở mỗi đỉnh", draw=s_rut, tail=0.6, caps=[
   ("Mốc thế năng: mặt bàn.", 4.2),
   ("Mỗi lần chạm bàn mất 20 %.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng không?", 2.8),
   ("Sai: đỉnh sau thấp hơn.", 3.4),
   ("Giới hạn của lần đo.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 6.8)]),
])

def _kiem_dong_bo():
    """Moi 0,05 s canh Tien hanh: so hang bang da hien = so dinh bong da toi; bong khong xuong duoi mat ban."""
    c = copy.deepcopy(CLIP); build(c); sc = c["scenes"][1]; t = 0.0; loi = 0
    while t < sc["T"]:
        tau = t - REL1; rows = sum(1 for j in range(1, 4) if t >= row_t(j)); h = traj(tau)
        if rows != n_peaks(tau) or h < -1e-9: loi += 1
        for j in range(1, 4):
            if abs(t - row_t(j)) < 0.026 and abs(h - HM[j]) > 0.01: loi += 1
        t += 0.05
    return loi
