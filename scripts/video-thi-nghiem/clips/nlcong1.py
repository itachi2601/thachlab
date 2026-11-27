# Clip: tn-l10-nang-luong-cong-01 - Qua bong nay thap dan (ban 2 theo cong moi, 27/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l10-nang-luong-cong-01.json:
#   tham_so: h0 = 1,0 m, k = 0,55, m = 57 g; mo_hinh g = 9,8 m/s2, bo qua can khong khi.
#   so_lieu_mau: n 0..3 -> h 1,00 / 0,550 / 0,303 / 0,166 m ; Wt 0,559 / 0,307 / 0,169 / 0,093 J ; dinh 3: nhiet + am 0,466 J.
# Du doan (K10): phan lon nang luong thanh nhiet + am sinh ra luc nao? -> luc cham san (cot do chi nhay khi cham san).
#   Khong trung Bam xem cua bai (hoi "nang luong di dau het" -> nhiet + am).
# Bay = hien_tuong_hay_sai[1] (san cung thi nay lai dung do cao tha); [0] (nang luong mat) da la Bam xem cua bai.
# Cau chot (ghi_chu kho, chua hien): tha 2,0 m, cung san (k = 0,55): toi dinh 1 da co 0,057 . 9,8 . 2,0 . 0,45 = 0,503 ~ 0,50 J.
# Quay cham x4,2 va chi ghi den dinh 3 de cac hang cach nhau >= 2 s (cong A2).
import copy
from engine import *

H0, K, M_KG, G = 1.0, 0.55, 0.057, 9.8
HM = [H0 * K ** n for n in range(5)]                         # mo hinh: 1 / 0,55 / 0,3025 / 0,166 / 0,0915
HS = ["1,00", "0,550", "0,303", "0,166", "0,092"]          # so_lieu_mau h (m), 3 chu so de nhan ra dung Wt
WS = ["0,559", "0,307", "0,169", "0,093", "0,051"]           # so_lieu_mau Wt (J)
E0 = M_KG * G * H0                                           # 0,5586 J
def fm(x, n=1): return f"{x:.{n}f}".replace(".", ",")

TEN = (205, 222, 60); TEN_D = (120, 140, 20); TILE = (196, 120, 90); TILE_D = (150, 85, 60)
RULER = (250, 222, 140); RULER_D = (170, 130, 40)
C_WT, C_WD, C_Q = BLUE, ORANGE, RED

# ---------------- thuoc + san + bong (khuon chung voi conang2, chep, khong import cheo) ----------------
YF, PXM = 960, 600               # mat san (y), px ung voi 1 m -> 1,0 m o y 360
XR0, XR1 = 150, 200
XB, RB = 330, 28

def ym(h): return YF - h * PXM

def ruler(d):
    d.rectangle([XR0, ym(1.08), XR1, YF], fill=RULER, outline=RULER_D, width=3)
    for i in range(0, 11):
        y = ym(i / 10); L = 30 if i % 2 == 0 else 16
        d.line([(XR1 - L, y), (XR1, y)], fill=RULER_D, width=4)
        if i % 2 == 0 and i > 0: text(d, (XR0 - 10, y), fm(i / 10), 56, INK, anchor="rm")
    text(d, (XR0 - 10, ym(1.08) - 26), "(m)", 56, INK, anchor="rm")

def floor(d, lab=True):
    for i in range(6):
        x = 60 + i * 96
        d.rectangle([x, YF, x + 92, YF + 50], fill=TILE, outline=TILE_D, width=3)
    if lab: text(d, (340, YF + 100), "sàn gạch", 56, INK)

def ball(d, h, alpha=1.0, squash=0.0):
    ry = RB * (1 - squash); rx = RB * (1 + 0.6 * squash); y = ym(h) - ry
    box = [XB - rx, y - ry, XB + rx, y + ry]
    if alpha >= 0.98: d.ellipse(box, fill=TEN, outline=TEN_D, width=3)
    else: d.ellipse(box, fill=A(TEN, alpha), outline=A(TEN_D, alpha), width=3)

def peak_mark(d, h, lab, color=BLUE, alpha=1.0, x1=360):
    y = ym(h)                                     # do cao tinh o day bong: vach trung vach thuoc
    for xx in range(XR1 + 6, x1, 22): d.line([(xx, y), (xx + 12, y)], fill=A(color, alpha), width=4)
    text(d, (x1 + 8, y), lab, 56, color, anchor="lm", alpha=alpha)

SL = 4.2
def _tu(h): return math.sqrt(2 * h / G)
def _events():
    """Moc (giay video sau khi tha): cham san lan 1..4 va toi dinh lan 1..4."""
    hits, peaks, t = [], [], _tu(HM[0])
    for h in HM[1:]:
        hits.append(t * SL); peaks.append((t + _tu(h)) * SL); t += 2 * _tu(h)
    return hits, peaks
HIT, PT = _events()

def state(tau, stop=4):
    """(do cao day bong m, so lan da cham san n) tau giay video sau khi tha; dung hinh o dinh lan `stop`."""
    if tau <= 0: return HM[0], 0
    tau = min(tau, PT[stop - 1]); t = tau / SL; tf = _tu(HM[0])
    if t < tf: return HM[0] - 0.5 * G * t * t, 0
    t -= tf; n = 1
    for h in HM[1:]:
        tu = _tu(h)
        if t < 2 * tu: return max(0.0, G * tu * t - 0.5 * G * t * t), n
        t -= 2 * tu; n += 1
    return 0.0, n

def energies(tau, stop=4):
    y, n = state(tau, stop)
    wt = M_KG * G * y; mech = M_KG * G * HM[n]; return wt, max(0.0, mech - wt), E0 - mech

def squash_at(tau):
    for th in HIT:
        if abs(tau - th) < 0.12: return 0.35 * (1 - abs(tau - th) / 0.12)
    return 0.0

# cot chong nang luong (tong = 0,559 J, thang co dinh)
CX0, CX1, CB, CH = 540, 650, 960, 520
def stack(d, wt, wd, q, alpha=1.0, x0=CX0, x1=CX1, legend=True, total=True, cb=CB, ch=CH):
    d.rectangle([x0, cb - ch, x1, cb], outline=A(GRAY, alpha), width=3)
    y = cb
    for v, c in ((wt, C_WT), (wd, C_WD), (q, C_Q)):
        hh = ch * v / E0
        if hh > 2: d.rectangle([x0 + 3, y - hh, x1 - 3, y], fill=A(c, alpha))
        y -= hh
    if total: text(d, ((x0 + x1) / 2 + 60, cb - ch - 45), "tổng 0,559 J", 56, INK, alpha=alpha)
    if legend:
        for i, (lab, c) in enumerate((("nhiệt + âm", C_Q), ("động năng", C_WD), ("thế năng", C_WT))):
            yy = CB - CH + 90 + i * 100
            d.rectangle([x1 + 18, yy - 20, x1 + 58, yy + 20], fill=A(c, alpha))
            text(d, (x1 + 70, yy), lab, 56, c, anchor="lm", alpha=alpha)

EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

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

def burst(d, tau):
    """Tia ngan quanh cho cham san (thay chu 'bop' de khong them khoi chu)."""
    for th in HIT:
        u = (tau - th) / 0.5
        if 0 <= u < 1:
            for ang in (-150, -120, -60, -30):
                r0, r1 = 40 + 30 * u, 70 + 40 * u; c = math.cos(math.radians(ang)); s = math.sin(math.radians(ang))
                d.line([(XB + c * r0, YF + s * r0), (XB + c * r1, YF + s * r1)], fill=A(RED, 1 - u), width=6)

# ---------------- canh 1: du doan ----------------
REL0 = 0.5
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; tau = t - REL0
    ruler(d); floor(d)
    text(d, (800, 420), "bóng tennis", 58, INK); text(d, (800, 500), "57 g", 58, INK)
    peak_mark(d, HM[0], "thả 1,0 m", INK)
    y, n = state(tau, 1); ball(d, y, squash=squash_at(tau)); burst(d, tau)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1110 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 175), "Phần lớn nhiệt và âm", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 265), "sinh ra vào lúc nào?", 60, PURPLE, alpha=k)
    seg_bar(d, y0 + 370, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: tien hanh ----------------
REL1 = 0.5; NR = 4
def row_t(j): return 0.0 if j == 0 else REL1 + PT[j - 1]

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; tau = t - REL1
    ruler(d); floor(d, lab=False)
    peak_mark(d, HM[0], "thả", INK)
    for j in range(1, NR):
        if tau >= PT[j - 1]: peak_mark(d, HM[j], HS[j], BLUE, appear(t, row_t(j), 0.25))
    y, n = state(tau, NR - 1); ball(d, y, squash=squash_at(tau)); burst(d, tau)
    stack(d, *energies(tau, NR - 1))
    xs = (220, 520, 820); y0 = 1150
    card(d, (40, y0, 1040, y0 + 90 + NR * 82), fill=WHITE, outline=NAVY, w=4)
    for x, s in zip(xs, ("lần", "đỉnh (m)", "thế năng (J)")): text(d, (x, y0 + 50), s, 56, INK)
    d.line([(70, y0 + 92), (1010, y0 + 92)], fill=LIGHT, width=4)
    for j in range(NR):
        a = appear(t, row_t(j), 0.3); yy = y0 + 135 + j * 82
        if a <= 0: continue
        text(d, (xs[0], yy), "thả" if j == 0 else str(j), 58, INK, alpha=a)
        text(d, (xs[1], yy), HS[j], 58, BLUE, alpha=a); text(d, (xs[2], yy), WS[j], 58, C_WT, alpha=a)
    ka = appear(t, M[1] + 0.1, 0.4)
    if ka > 0:
        card(d, (60, 1040, 1020, 1130), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1085), "Đáp án: lúc chạm sàn", 58, GREEN, alpha=ka)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k0 = appear(t, 0.2, 0.4)
    wt3 = M_KG * G * HM[3]; x0, x1 = 100, 220
    stack(d, wt3, 0.0, E0 - wt3, k0, x0=x0, x1=x1, legend=False, total=False)
    pu = 0.8 + 0.2 * math.sin(5.0 * t)
    hq = CH * (E0 - wt3) / E0; hw = CH * wt3 / E0
    d.rectangle([x0 + 3, CB - hw - hq, x1 - 3, CB - hw], fill=A(mix(WHITE, C_Q, pu), k0))
    text(d, ((x0 + x1) / 2, CB + 55), "đỉnh 3", 56, INK, alpha=k0)
    text(d, (x1 + 15, CB - hw / 2 - 20), "0,093 J", 56, C_WT, anchor="lm", alpha=k0)
    text(d, (x1 + 15, CB - hw - hq / 2), "0,466 J", 56, C_Q, anchor="lm", alpha=k0)
    card(d, (470, 470, 1050, 800), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    text(d, (760, 535), "thế năng 0,093 J", 56, C_WT, alpha=k0)
    text(d, (760, 615), "+ nhiệt, âm 0,466 J", 56, C_Q, alpha=k0)
    d.line([(510, 665), (1010, 665)], fill=A(INK, k0), width=3)
    text(d, (760, 730), "= 0,559 J", 60, INK, alpha=k0)
    kk = appear(t, M[1] + 0.3, 0.4)
    if kk > 0:
        card(d, (60, 1100, 1020, 1230), fill=A((236, 253, 243), kk), outline=A(GREEN, kk), r=28, w=4)
        text(d, (W / 2, 1165), "Bằng lúc thả: chỉ đổi dạng", 58, GREEN, alpha=kk)

# ---------------- canh 4: bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; mk = M[1]
    ruler(d); floor(d, lab=False)
    peak_mark(d, HM[0], "tưởng: 1,0 m", RED)
    peak_mark(d, HM[1], "thật: 0,55 m", BLUE)
    ks = clamp((t - mk) / 0.4)
    yg = ym(HM[0]) - RB                                       # bong "nghi": vien do, nay lai dung 1,0 m
    d.ellipse([XB - RB, yg - RB, XB + RB, yg + RB], outline=A(RED, 1 - 0.6 * ks), width=5)
    if ks > 0:
        y = ym(HM[0]) - RB
        d.line([(XB - 40, y - 40), (XB + 40, y + 40)], fill=A(RED, ks), width=8)
        d.line([(XB - 40, y + 40), (XB + 40, y - 40)], fill=A(RED, ks), width=8)
    ball(d, HM[1] + 0.03 * math.sin(4 * t))                 # bong that o dinh 1
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3; y = 1110
    if a1 > 0:
        card(d, (40, y, 1040, y + 430), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        yy = y + 195; q = "“Sàn cứng: nảy lại 1,0 m”"
        lw = tw(d, q, F(60))
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 4)], fill=A(RED, 0.85 * a1), width=6)
        k2 = appear(t, mk + 0.2, 0.45)
        if k2 > 0: text(d, (W / 2, y + 330), "Chỉ lên 0,55 m", 60, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 340), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 230), "Nhiệt, âm chỉ suy ra", 62, INK, alpha=k3)

# ---------------- canh 5: thu nghi (cau chot o khung: 0,50 J) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 300, 1040, 1150), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 380, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 530), "Bóng 57 g, thả 2,0 m,", 62, INK, alpha=k)
    text(d, (W / 2, 620), "cùng sàn; g = 9,8 m/s².", 62, INK, alpha=k)
    text(d, (W / 2, 750), "Tới đỉnh 1: nhiệt, âm", 62, DORANGE, alpha=k)
    text(d, (W / 2, 840), "bao nhiêu J?", 62, DORANGE, alpha=k)
    seg_bar(d, 990, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding")]
            + [(do["t0"] + REL1 + th, "tap") for th in HIT[:NR - 1]]
            + [(do["t0"] + do["M"][1] + 0.1, "ding"), (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-nang-luong-cong-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Năng lượng. Công cơ học · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bóng tennis nảy trên sàn", draw=s_hook, tail=0.3, caps=[
   ("Thả bóng từ 1,0 m, không ném.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Năng lượng đổi dạng", draw=s_do, tail=0.4, caps=[
   ("Quay chậm: xem cột đỏ tăng lúc nào.", 9.7),
   ("Cột đỏ chỉ tăng khi chạm sàn.", 3.6)]),
 dict(key="rut", title="Năng lượng đi đâu?", draw=s_rut, tail=0.4, caps=[
   ("Ở đỉnh 3, cộng hai phần lại.", 3.4),
   ("Tổng vẫn như lúc thả.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.2),
   ("Sai: chạm sàn vẫn ra nhiệt, âm.", 3.8),
   ("Giới hạn của lần đo.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])

def _kiem_dong_bo():
    """Moi 0,05 s canh Tien hanh: so hang = so dinh da toi; tong 3 cot = 0,559 J; cot do chi doi khi vua cham san."""
    c = copy.deepcopy(CLIP); build(c); sc = c["scenes"][1]; t = 0.0; loi = 0; q_prev = None
    while t < sc["T"]:
        tau = t - REL1; y, n = state(tau, NR - 1)
        rows = sum(1 for j in range(1, NR) if t >= row_t(j)); peaks = sum(1 for p in PT[:NR - 1] if tau >= p - 1e-9)
        wt, wd, q = energies(tau, NR - 1)
        if rows != peaks or abs(wt + wd + q - E0) > 1e-9 or wd < -1e-9: loi += 1
        if q_prev is not None and abs(q - q_prev) > 1e-9 and not any(0 <= tau - th < 0.06 for th in HIT): loi += 1
        for j in range(1, NR):
            if abs(t - row_t(j)) < 0.026 and abs(y - HM[j]) > 0.01: loi += 1
        q_prev = q; t += 0.05
    return loi
