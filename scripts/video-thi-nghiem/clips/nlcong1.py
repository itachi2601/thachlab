# Clip: tn-l10-nang-luong-cong-01 - Qua bong nay thap dan: nang luong chuyen hoa, khong mat (lo 9, 18/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l10-nang-luong-cong-01.json:
#   tham_so: h0 = 1,0 m, k = 0,55, m = 57 g; mo_hinh g = 9,8 m/s2, bo qua can khong khi.
#   so_lieu_mau: n 0..4 -> h 1,0 / 0,55 / 0,30 / 0,17 / 0,09 m ; Wt 0,559 / 0,307 / 0,169 / 0,093 / 0,051 J
#   Nhiet + am cong don sau lan cham n = m g (h0 - h_n) (them vao kho 18/11/2026): 0,251 / 0,390 / 0,466 / 0,507 J.
#   Tren man CHI hien 0,466 J (dinh 3) -- khop ca hai cach tinh (0,559 - 0,093); 0,251 va 0,507 lech 0,001 so voi phep tru
#   so da lam tron nen khong hien (K5).
# Canh: Du doan (phan lon nang luong thanh nhiet + am sinh ra luc nao? K10: chi cau hoi + hinh)
#       -> Tien hanh (quay cham x2, cot chong the nang / dong nang / nhiet + am, tong khong doi; cot do chi nhay khi cham san;
#          bang Wt o moi dinh) + DAP AN · luc cham san
#       -> Rut ra (dinh 3: 0,093 + 0,466 = 0,559 J; khong mat, chi doi dang) + Chua noi duoc (nhiet chua do, suy ra)
#       -> Bay (nay thap -> nang luong mat: sai) -> Chot + THU NGHI:
#          tha tu 2,0 m (h0 max kho), k van 0,55: toi dinh lan nay 1, bao nhieu J da thanh nhiet + am?
#          0,057 . 9,8 . 2,0 . 0,45 = 0,503 ~ 0,50 J (chua hien; 2 buoc tu so tren man).
# Khac clip conang2 (cung khuon bong nay): o day bong tennis 57 g / san gach / k = 0,55 / g = 9,8, hoi LUC NAO chuyen hoa,
#   cot chong 3 dang nang luong; conang2 hoi do cao dinh 3 va co nang (mJ).
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
        if i % 2 == 0 and i > 0: text(d, (XR0 - 12, y), fm(i / 10), 40, INK, anchor="rm")
    text(d, (XR0 - 12, ym(1.0) - 58), "m", 40, MUTED, anchor="rm")

def floor(d, lab=True):
    for i in range(6):
        x = 60 + i * 96
        d.rectangle([x, YF, x + 92, YF + 50], fill=TILE, outline=TILE_D, width=3)
    if lab: text(d, (340, YF + 96), "sàn gạch", 40, MUTED)

def ball(d, h, alpha=1.0, squash=0.0):
    ry = RB * (1 - squash); rx = RB * (1 + 0.6 * squash); y = ym(h) - ry
    box = [XB - rx, y - ry, XB + rx, y + ry]
    if alpha >= 0.98: d.ellipse(box, fill=TEN, outline=TEN_D, width=3)
    else: d.ellipse(box, fill=A(TEN, alpha), outline=A(TEN_D, alpha), width=3)

def peak_mark(d, h, lab, color=BLUE, alpha=1.0, x1=400):
    y = ym(h)                                     # do cao tinh o day bong: vach trung vach thuoc
    for xx in range(XR1 + 6, x1, 22): d.line([(xx, y), (xx + 12, y)], fill=A(color, alpha), width=4)
    text(d, (x1 + 8, y), lab, 40, color, anchor="lm", alpha=alpha)

SL = 2.0
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
CX0, CX1, CB, CH = 600, 740, 960, 560
def stack(d, wt, wd, q, alpha=1.0, x0=CX0, x1=CX1, legend=True, total=True, cb=CB, ch=CH):
    d.rectangle([x0, cb - ch, x1, cb], outline=A(GRAY, alpha), width=3)
    y = cb
    for v, c in ((wt, C_WT), (wd, C_WD), (q, C_Q)):
        hh = ch * v / E0
        if hh > 2: d.rectangle([x0 + 3, y - hh, x1 - 3, y], fill=A(c, alpha))
        y -= hh
    if total: text(d, ((x0 + x1) / 2, cb - ch - 40), "tổng 0,559 J", 40, INK, alpha=alpha)
    if legend:
        for i, (lab, c) in enumerate((("nhiệt + âm", C_Q), ("động năng", C_WD), ("thế năng", C_WT))):
            yy = CB - CH + 70 + i * 90
            d.rectangle([x1 + 22, yy - 18, x1 + 58, yy + 18], fill=A(c, alpha))
            text(d, (x1 + 70, yy), lab, 40, c, anchor="lm", alpha=alpha)

# ---------------- canh 1: du doan ----------------
REL0 = 0.6
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; tau = t - REL0
    ruler(d); floor(d)
    text(d, (780, 420), "bóng tennis", 44, INK); text(d, (780, 480), "57 g", 44, INK)
    peak_mark(d, HM[0], "1,0 m", INK)
    if tau < PT[0] + 0.5: ball(d, state(min(tau, PT[0]), 1)[0], squash=squash_at(tau))
    else: ball(d, HM[0], appear(t, REL0 + PT[0] + 0.5, 0.5))
    if tau >= PT[0]: peak_mark(d, HM[1], "đỉnh 1: 0,55 m", BLUE, appear(t, REL0 + PT[0], 0.3))
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 1150 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 400), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 58), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 150, "Phần lớn năng lượng thành nhiệt", 46, INK, maxw=900, alpha=k)
    ctext(d, y0 + 215, "và âm sinh ra lúc nào?", 46, INK, maxw=900, alpha=k)
    text(d, (W / 2, y0 + 290), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 345, 880, y0 + 361], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 345, 200 + 680 * (1 - q), y0 + 361], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
REL1 = 0.5
def row_t(j): return 0.0 if j == 0 else REL1 + PT[j - 1]

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; tau = t - REL1
    ruler(d); floor(d, lab=False)
    peak_mark(d, HM[0], "thả", INK)
    for j in range(1, 5):
        if tau >= PT[j - 1]: peak_mark(d, HM[j], HS[j] if j <= 3 else "", BLUE, appear(t, row_t(j), 0.25))
    y, n = state(tau); ball(d, y, squash=squash_at(tau))
    for th in HIT:                                            # "bop" luc cham san
        if 0 <= tau - th < 0.5: text(d, (470, YF - 30), "bộp!", 44, RED, anchor="lm", alpha=1 - (tau - th) / 0.5)
    stack(d, *energies(tau))
    # bang: lan | h (m) | Wt (J)
    ka = appear(t, M[1], 0.4)
    nr = sum(1 for j in range(5) if t >= row_t(j))           # the cao dan theo so hang
    card(d, (60, 1140, 1020, 1265 + (max(nr, 1) - 1) * 70 + 45), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 520, 820)
    for x, s in zip(xs, ("lần", "đỉnh (m)", "thế năng (J)")): text(d, (x, 1185), s, 40, INK)
    d.line([(90, 1218), (990, 1218)], fill=LIGHT, width=4)
    for j in range(5):
        a = appear(t, row_t(j), 0.3); yy = 1265 + j * 70
        if a <= 0: continue
        text(d, (xs[0], yy), "thả" if j == 0 else str(j), 42, INK, alpha=a)
        text(d, (xs[1], yy), HS[j], 42, BLUE, alpha=a); text(d, (xs[2], yy), WS[j], 42, C_WT, alpha=a)
    if ka > 0:
        card(d, (60, 1045, 1020, 1125), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1085), "ĐÁP ÁN · lúc chạm sàn", 46, GREEN, alpha=ka)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k0 = appear(t, M[0], 0.4)
    # cot chong o dinh lan 3 (0,093 + 0,466)
    wt3 = M_KG * G * HM[3]
    stack(d, wt3, 0.0, E0 - wt3, k0, x0=180, x1=320, legend=False, total=False)
    text(d, (250, CB + 50), "đỉnh 3", 40, INK, alpha=k0)
    text(d, (340, CB - CH * wt3 / E0 / 2 - 10), "0,093 J", 40, C_WT, anchor="lm", alpha=k0)
    kq = appear(t, M[0] + 1.0, 0.4)
    text(d, (340, CB - CH * (1 + wt3 / E0) / 2), "0,466 J", 40, C_Q, anchor="lm", alpha=kq)
    card(d, (520, 480, 1040, 760), fill=A(WHITE, kq), outline=A(LIGHT, kq), w=3)
    text(d, (780, 540), "thế năng 0,093 J", 40, C_WT, alpha=kq)
    text(d, (780, 610), "+ nhiệt, âm 0,466 J", 40, C_Q, alpha=kq)
    d.line([(560, 655), (1000, 655)], fill=A(INK, kq), width=3)
    text(d, (780, 705), "= 0,559 J", 44, INK, alpha=kq)
    kk = appear(t, M[1] + 0.4, 0.4)
    if kk > 0:
        card(d, (60, 1060, 1020, 1180), fill=A((236, 253, 243), kk), outline=A(GREEN, kk), r=28, w=4)
        text(d, (W / 2, 1120), "Không mất, chỉ đổi dạng", 46, GREEN, alpha=kk)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1240 + (1 - k3) * 20
        card(d, (40, y1, 1040, y1 + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 55), "Chưa nói được gì?", 44, NAVY, alpha=k3)
        card(d, (80, y1 + 105, 1000, y1 + 290), fill=A((239, 246, 255), k3), r=24)
        ctext(d, y1 + 155, "Thước chỉ đo thế năng;", 42, INK, alpha=k3)
        ctext(d, y1 + 235, "nhiệt + âm là suy ra", 42, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1, 0.4)
    card(d, (60, 262, 1020, 560), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 288, W / 2 + pw / 2, 352), fill=A(RED, a), r=32)
    text(d, (W / 2, 320), "Bẫy", 40, WHITE, alpha=a)
    ks = clamp((t - 1.0) / 0.4)
    q = "Nảy thấp dần → năng lượng mất"; f = F(44); lw = tw(d, q, f); yy = 430
    text(d, (W / 2, yy), q, 44, mix(INK, MUTED, ks), alpha=a)
    if ks > 0: d.line([(W / 2 - lw / 2 - 8, yy + 2), (W / 2 - lw / 2 - 8 + (lw + 16) * ks, yy + 2)], fill=A(RED, 0.85 * a), width=6)
    text(d, (W / 2 - lw / 2 - 14, yy), "✗", 44, RED, anchor="rm", alpha=ks)
    # hinh: cot lúc tha / dinh 4, cung tong. Cot sai (rong o dinh 4) hien cung cau sai, cot dung hien sau.
    wt4 = M_KG * G * HM[4]; cb, ch = 1040, 380
    text(d, (290, cb + 45), "lúc thả", 42, INK, alpha=a)
    stack(d, E0, 0, 0, a, x0=220, x1=360, legend=False, total=False, cb=cb, ch=ch)
    text(d, (790, cb + 45), "đỉnh 4", 42, INK, alpha=a)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 <= 0:                                               # cach nghi sai: chi con 0,051 J, phan con lai bien mat
        d.rectangle([720, cb - ch, 860, cb], outline=A(GRAY, a), width=3)
        hh = ch * wt4 / E0
        if hh > 2: d.rectangle([723, cb - hh, 857, cb], fill=A(C_WT, a))
        for yy2 in range(int(cb - ch) + 20, int(cb - hh) - 30, 46):
            d.line([(735, yy2), (845, yy2 + 30)], fill=A(RED, 0.5 * a * ks), width=4)
    else:
        stack(d, wt4, 0, E0 - wt4, k2, x0=720, x1=860, legend=False, total=False, cb=cb, ch=ch)
        card(d, (60, 1140, 1020, 1430), fill=A((220, 252, 231), k2), outline=A(GREEN, k2), w=5)
        ctext(d, 1240, "Phần đỏ: nhiệt và âm thanh", 44, INK, alpha=k2)
        ctext(d, 1340, "Tổng vẫn 0,559 J", 46, GREEN, alpha=k2)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 262, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 391, "Chạm sàn: cơ năng thành nhiệt, âm", 48, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1220), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 676), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 643), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    ctext(d, 790, "Thả từ 2,0 m. Tới đỉnh 1,", 46, INK, alpha=kq)
    ctext(d, 865, "bao nhiêu J thành nhiệt, âm?", 46, INK, alpha=kq)
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh > 0:
        card(d, (110, 980, 970, 1180), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1030, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1110, "đỉnh 1 = 55 % độ cao thả", 42, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + REL1, "tap"), (do["t0"] + do["M"][1], "ding"), (r["t0"] + r["M"][2] - 0.1, "tap"),
            (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-nang-luong-cong-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Năng lượng. Công cơ học · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bóng tennis nảy trên sàn", draw=s_hook, tail=0.6, caps=[
   ("Thả bóng từ 1,0 m, không ném.", 3.6),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Năng lượng đổi dạng", draw=s_do, tail=0.6, caps=[
   ("Xem cột đỏ tăng lúc nào.", 5.8),
   ("Cột đỏ chỉ tăng khi chạm sàn.", 3.6)]),
 dict(key="rut", title="Năng lượng đi đâu?", draw=s_rut, tail=0.6, caps=[
   ("Ở đỉnh 3 cộng hai phần lại.", 3.4),
   ("Tổng vẫn như lúc thả.", 3.4),
   ("Giới hạn của thí nghiệm.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Nhiều bạn nghĩ năng lượng biến mất.", 3.0),
   ("Phần đỏ vẫn còn, thước không đo được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])

def _kiem_dong_bo():
    """Moi 0,05 s canh Tien hanh: so hang = so dinh da toi; tong 3 cot = 0,559 J; cot do chi doi khi vua cham san."""
    c = copy.deepcopy(CLIP); build(c); sc = c["scenes"][1]; t = 0.0; loi = 0; q_prev = None
    while t < sc["T"]:
        tau = t - REL1; y, n = state(tau)
        rows = sum(1 for j in range(1, 5) if t >= row_t(j)); peaks = sum(1 for p in PT if tau >= p - 1e-9)
        wt, wd, q = energies(tau)
        if rows != peaks or abs(wt + wd + q - E0) > 1e-9 or wd < -1e-9: loi += 1
        if q_prev is not None and abs(q - q_prev) > 1e-9 and not any(0 <= tau - th < 0.06 for th in HIT): loi += 1
        for j in range(1, 5):
            if abs(t - row_t(j)) < 0.026 and abs(y - HM[j]) > 0.01: loi += 1
        q_prev = q; t += 0.05
    return loi
