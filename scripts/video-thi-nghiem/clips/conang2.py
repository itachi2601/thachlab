# Clip: tn-l10-co-nang-bao-toan-02 - Bong ban nay thap dan: co nang giam khi co luc can (lo 9, 18/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l10-co-nang-bao-toan-02.json:
#   tham_so: h0 = 1,00 m, e2 = 0,8 (ti so hai dinh lien tiep), m = 2,7 g; mo_hinh g = 10 m/s2.
#   so_lieu_mau: n 0..3 -> h_n 1,00 / 0,80 / 0,64 / 0,512 m (bai ghi 0,51) ; W_n = mgh_n 27,0 / 21,6 / 17,28 / 13,824 mJ
#   (cot W_n them vao kho 18/11/2026, tinh tu tham so, lam tron o buoc cuoi: 27,0 / 21,6 / 17,3 / 13,8 mJ).
# Canh: Du doan (tha 1,00 m, dinh lan 1 = 0,80 m; dinh lan nay 3 cao khoang bao nhieu? K10: chi cau hoi + hinh)
#       -> Tien hanh (quay cham x2, danh dau 3 dinh, bang hang hien DUNG luc bong toi dinh) + DAP AN · khoang 0,51 m
#       -> Rut ra (o dinh v = 0 -> W = mgh, cot co nang mJ, moi lan -20 % thanh nhiet + am) + Chua noi duoc
#       -> Bay (co nang luon bao toan -> nay lai 1,00 m: sai) -> Chot + THU NGHI:
#          tha tu 1,50 m (h0 max kho), toi dinh lan nay 2 co nang da giam bao nhieu? 40,5 - 25,92 = 14,58 ~ 14,6 mJ
#          (chua hien; can 2 buoc tu so tren man).
# Khac clip nlcong1 (cung khuon bong nay): o day bong ban 2,7 g / ban da / ti so 0,8 / g = 10, hoi DO CAO dinh 3 va co nang;
#   nlcong1 hoi LUC NAO nang luong thanh nhiet, cot chong 3 dang nang luong.
import copy
from engine import *

H0, E2, M_KG, G = 1.00, 0.8, 0.0027, 10.0
HM = [H0 * E2 ** n for n in range(4)]                       # 1,0 / 0,8 / 0,64 / 0,512 (mo hinh)
HS = ["1,00", "0,80", "0,64", "0,51"]                       # so_lieu_mau (bai ghi 0,51)
WM = [M_KG * G * h * 1000 for h in HM]                      # mJ: 27,0 / 21,6 / 17,28 / 13,824
def fm(x, n=1): return f"{x:.{n}f}".replace(".", ",")

BALL = (255, 255, 255); BALL_D = (200, 120, 40); STONE = (120, 128, 145); STONE_D = (80, 86, 100)
RULER = (250, 222, 140); RULER_D = (170, 130, 40)

# ---------------- thuoc + ban da + bong (khuon chung voi nlcong1, chep, khong import cheo) ----------------
YF, PXM = 1000, 640              # mat ban (y), px ung voi 1 m -> 1,00 m o y 360
XR0, XR1 = 150, 200              # thuoc dung
XB, RB = 340, 22                 # tam bong (x), ban kinh ve

def ym(h): return YF - h * PXM

def ruler(d):
    d.rectangle([XR0, ym(1.08), XR1, YF], fill=RULER, outline=RULER_D, width=3)
    for i in range(0, 11):
        y = ym(i / 10); L = 30 if i % 2 == 0 else 16
        d.line([(XR1 - L, y), (XR1, y)], fill=RULER_D, width=4)
        if i % 2 == 0 and i > 0: text(d, (XR0 - 12, y), fm(i / 10), 40, INK, anchor="rm")
    text(d, (XR0 - 12, ym(1.0) - 58), "m", 40, MUTED, anchor="rm")

def table_top(d):
    d.rectangle([60, YF, 640, YF + 60], fill=STONE)
    d.rectangle([60, YF + 60, 640, YF + 76], fill=STONE_D)
    text(d, (350, YF + 112), "mặt bàn đá", 40, MUTED)

def ball(d, h, alpha=1.0):
    y = ym(h) - RB
    if alpha >= 0.98: dot(d, XB, y, RB, BALL, BALL_D)
    else: d.ellipse([XB - RB, y - RB, XB + RB, y + RB], fill=A(BALL, alpha), outline=A(BALL_D, alpha), width=3)

def peak_mark(d, h, lab, color=BLUE, alpha=1.0, x1=470):
    y = ym(h)                                                 # do cao tinh o day bong: vach trung vach thuoc
    for xx in range(XR1 + 6, x1, 22): d.line([(xx, y), (xx + 12, y)], fill=A(color, alpha), width=4)
    text(d, (x1 + 8, y), lab, 40, color, anchor="lm", alpha=alpha)

# quy dao: tha khong van toc dau, nay voi cac dinh HM[1..], quay cham SL lan
SL = 2.0
def _tu(h): return math.sqrt(2 * h / G)
def peak_times():
    """Moc (giay video sau khi tha) bong toi dinh lan nay 1, 2, 3."""
    out, t = [], _tu(HM[0])
    for h in HM[1:]:
        out.append((t + _tu(h)) * SL); t += 2 * _tu(h)
    return out
PT = peak_times()

def traj(tau):
    """Do cao day bong (m) tau giay video sau khi tha; dung hinh o dinh lan 3."""
    if tau <= 0: return HM[0]
    tau = min(tau, PT[2])
    t = tau / SL; tf = _tu(HM[0])
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
    IMG_REF[0] = img
    M = sc["M"]; tau = t - REL0
    ruler(d); table_top(d)
    peak_mark(d, HM[0], "thả 1,00 m", INK)
    if tau < PT[0] + 0.5: ball(d, traj(min(tau, PT[0])))
    else:                                                    # nhat bong len, giu lai o 1,00 m
        k = appear(t, REL0 + PT[0] + 0.5, 0.5); ball(d, HM[0], k)
    if tau >= PT[0]: peak_mark(d, HM[1], "đỉnh 1: 0,80 m", BLUE, appear(t, REL0 + PT[0], 0.3))
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 1170 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 400), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 58), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 150, "Đỉnh lần nảy thứ 3", 48, INK, maxw=880, alpha=k)
    ctext(d, y0 + 215, "cao khoảng bao nhiêu?", 48, INK, maxw=880, alpha=k)
    text(d, (W / 2, y0 + 285), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))     # thanh dem thoi gian nghi
    d.rounded_rectangle([200, y0 + 340, 880, y0 + 356], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 340, 200 + 680 * (1 - q), y0 + 356], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
REL1 = 0.5
def row_t(j): return 0.0 if j == 0 else REL1 + PT[j - 1]            # hang j hien dung luc bong toi dinh j

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; tau = t - REL1
    ruler(d); table_top(d)
    peak_mark(d, HM[0], "thả", INK)
    for j in range(1, 4):
        if tau >= PT[j - 1]: peak_mark(d, HM[j], f"đỉnh {j}", BLUE, appear(t, row_t(j), 0.25))
    ball(d, traj(tau))
    # bang ben phai: lan nay n | h_n (m)
    ka = appear(t, M[1], 0.4)
    nr = sum(1 for j in range(4) if t >= row_t(j))           # the cao dan theo so hang da co
    card(d, (650, 330, 1040, 490 + (max(nr, 1) - 1) * 110 + 60), fill=WHITE, outline=NAVY, w=4)
    text(d, (740, 385), "lần", 40, INK); text(d, (920, 385), "đỉnh (m)", 40, INK)
    d.line([(670, 425), (1020, 425)], fill=LIGHT, width=4)
    for j in range(4):
        a = appear(t, row_t(j), 0.3); y = 490 + j * 110
        if a <= 0: continue
        if j == 3 and ka > 0: d.rounded_rectangle([668, y - 40, 1022, y + 40], radius=16, fill=A((220, 252, 231), ka))
        text(d, (740, y), "thả" if j == 0 else str(j), 44, INK, alpha=a)
        text(d, (920, y), HS[j], 46, BLUE if j else INK, alpha=a)
    if ka > 0:                                             # x0,8 giua cac hang
        card(d, (100, 1190, 980, 1290), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1240), "ĐÁP ÁN · khoảng 0,51 m", 46, GREEN, alpha=ka)
        kb = appear(t, M[1] + 0.8, 0.4)
        card(d, (100, 1330, 980, 1560), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        ctext(d, 1390, "1,00 → 0,80 → 0,64 → 0,51", 46, BLUE, alpha=kb)
        ctext(d, 1480, "mỗi lần nhân 0,8, không trừ đều", 42, INK, alpha=kb)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    k0 = appear(t, M[0], 0.4)
    card(d, (40, 262, 1040, 470), fill=A(WHITE, k0), outline=A(BLUE, k0), w=4)
    ctext(d, 320, "Đỉnh: v = 0, mốc mặt bàn", 42, INK, alpha=k0)
    ctext(d, 405, "W = mgh  (m = 2,7 g, g = 10 m/s²)", 44, BLUE, alpha=k0)
    # cot co nang (mJ) theo lan nay, chung thang 0-27 mJ
    kb = appear(t, M[0] + 1.0, 0.4)
    if kb > 0:
        card(d, (40, 500, 1040, 1120), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        base, hmax, wmax = 1000, 340, WM[0]
        xs = [190, 410, 630, 850]
        for j in range(4):
            g = ease((t - M[0] - 1.2 - j * 0.35) / 0.4)
            text(d, (xs[j], base + 50), "thả" if j == 0 else f"đỉnh {j}", 40, INK, alpha=kb)
            d.rectangle([xs[j] - 28, base - hmax, xs[j] + 28, base], outline=A(LIGHT, kb), width=3)
            if g > 0:
                hh = hmax * WM[j] / wmax * g
                if hh > 2: d.rectangle([xs[j] - 28, base - hh, xs[j] + 28, base], fill=BLUE)
                text(d, (xs[j], base - hmax * WM[j] / wmax - 34), fm(WM[j]), 40, BLUE, alpha=clamp(g * 2 - 1))
        text(d, (W / 2, 548), "W ở đỉnh (mJ)", 40, MUTED, alpha=kb)
        kc = appear(t, M[1], 0.4)
        if kc > 0:
            for j in range(3):
                xm = (xs[j] + xs[j + 1]) / 2
                text(d, (xm, base - hmax * WM[j + 1] / wmax + 60), "−20 %", 40, RED, alpha=kc)
    kd = appear(t, M[1] + 0.6, 0.4)
    if kd > 0:
        card(d, (60, 1150, 1020, 1250), fill=A((254, 242, 242), kd), outline=A(RED, kd), r=28, w=4)
        text(d, (W / 2, 1200), "Phần mất: thành nhiệt, âm thanh", 42, RED, alpha=kd)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1290 + (1 - k3) * 20
        card(d, (40, y1, 1040, y1 + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 55), "Chưa nói được gì?", 44, NAVY, alpha=k3)
        card(d, (80, y1 + 105, 1000, y1 + 270), fill=A((239, 246, 255), k3), r=24)
        ctext(d, y1 + 150, "Chỉ một bóng, một mặt bàn", 42, INK, alpha=k3)
        ctext(d, y1 + 225, "mặt nảy khác: chưa biết", 42, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1, 0.4)
    ruler(d); table_top(d)
    # cau sai + hinh sai (bong ma o 1,00 m) hien cung luc
    ks = clamp((t - 1.0) / 0.4)
    gy = ym(1.0) - RB
    d.ellipse([XB - RB, gy - RB, XB + RB, gy + RB], outline=A(RED, a * (1 - 0.6 * ks)), width=4)
    if ks > 0:
        for s in (1, -1): d.line([(XB - 30, gy - 30 * s), (XB - 30 + 60 * ks, gy - 30 * s + 60 * s * ks)], fill=A(RED, a), width=6)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        peak_mark(d, HM[1], "thật: 0,80 m", GREEN, k2)
        ball(d, HM[1], k2)
    Y9 = 580
    card(d, (560, Y9, 1040, Y9 + 340), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (800 - pw / 2, Y9 + 26, 800 + pw / 2, Y9 + 90), fill=A(RED, a), r=32)
    text(d, (800, Y9 + 58), "Bẫy", 40, WHITE, alpha=a)
    for i, q in enumerate(("Cơ năng bảo toàn", "→ nảy lại 1,00 m")):
        yy = Y9 + 160 + i * 70; f = F(42); lw = tw(d, q, f)
        text(d, (800, yy), q, 42, mix(INK, MUTED, ks), alpha=a)
        if i == 0: text(d, (800 - lw / 2 - 12, yy), "✗", 42, RED, anchor="rm", alpha=ks)
        if ks > 0: d.line([(800 - lw / 2 - 6, yy + 2), (800 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a), width=5)
    if k2 > 0:
        card(d, (60, 1210, 1020, 1530), fill=A((220, 252, 231), k2), outline=A(GREEN, k2), w=5)
        ctext(d, 1310, "Va chạm lấy bớt cơ năng", 46, INK, alpha=k2)
        ctext(d, 1430, "→ đỉnh sau thấp hơn", 46, GREEN, alpha=k2)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 262, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 391, "Đỉnh thấp dần: cơ năng giảm", 50, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1230), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 676), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 643), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    ctext(d, 770, "Thả từ 1,50 m. Tới đỉnh 2,", 46, INK, alpha=kq)
    ctext(d, 845, "cơ năng giảm bao nhiêu mJ?", 46, INK, alpha=kq)
    kh = appear(t, M[0] + 2.9, 0.5)                                  # goi y hien tre >= 2,5 s
    if kh > 0:
        card(d, (110, 980, 970, 1190), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1030, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1110, "m = 2,7 g · g = 10 m/s²", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + REL1, "tap"), (do["t0"] + do["M"][1], "ding"), (r["t0"] + r["M"][2] - 0.1, "tap"),
            (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-co-nang-bao-toan-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng và bảo toàn cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bóng bàn nảy trên bàn đá", draw=s_hook, tail=0.6, caps=[
   ("Thả bóng bàn, đọc đỉnh lần 1.", 3.6),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Quay chậm, đọc từng đỉnh", draw=s_do, tail=0.6, caps=[
   ("Thả nhẹ, không ném.", 5.4),
   ("Mỗi đỉnh còn khoảng 80 % đỉnh trước.", 4.4)]),
 dict(key="rut", title="Cơ năng ở mỗi đỉnh", draw=s_rut, tail=0.6, caps=[
   ("Đỉnh tỉ lệ với cơ năng.", 3.4),
   ("Mỗi lần chạm bàn mất 20 %.", 3.6),
   ("Giới hạn của thí nghiệm.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Nhiều bạn quên lực cản, va chạm.", 3.0),
   ("Bảo toàn khi không mất vào nhiệt, âm.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])

def _kiem_dong_bo():
    """Moi 0,05 s canh Tien hanh: so hang bang da hien = so dinh bong da toi; bong khong xuong duoi mat ban."""
    c = copy.deepcopy(CLIP); build(c); sc = c["scenes"][1]; t = 0.0; loi = 0
    while t < sc["T"]:
        tau = t - REL1; rows = sum(1 for j in range(1, 4) if t >= row_t(j)); h = traj(tau)
        if rows != n_peaks(tau) or h < -1e-9: loi += 1
        for j in range(1, 4):                              # dung luc hang j hien, bong dang o dinh j
            if abs(t - row_t(j)) < 0.026 and abs(h - HM[j]) > 0.01: loi += 1
        t += 0.05
    return loi
