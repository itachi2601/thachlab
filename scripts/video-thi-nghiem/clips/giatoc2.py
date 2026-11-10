# Clip: tn-l10-gia-toc-02 - Dau vet vien bi qua video: deu, nhanh dan, cham dan (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-gia-toc-02.json:
#   so_lieu_mau x0..x4 (cm) tai t = 0; 0,2; 0,4; 0,6; 0,8 s:
#     tren ban  (v0 0,4 m/s, a 0)    : 0, 8, 16, 24, 32   -> khoang 8, 8, 8, 8
#     xuong doc (v0 0,   a 1 m/s2)   : 0, 2, 8, 18, 32    -> khoang 2, 6, 10, 14
#     len doc   (v0 0,8, a -1 m/s2)  : 0, 14, 24, 30, 32  -> khoang 14, 10, 6, 2
#   tham_so dt = 0,2 s; mo_hinh x = v0.t + a.t2/2 (dung de ve bi chay cham giua hai cham, trung so lieu tai cac cham).
# Canh: Du doan (len doc, khoang cach doi the nao; K10: chi cau hoi + hinh) -> Tien hanh (ba lan chay cham, cham
#       moi 0,2 s, thuoc 0-32 cm, dong ho t dong pha voi cham; chip nhac cau hoi toi luc dap an) -> Rut ra (v xanh duong,
#       a xanh la nhu Hinh 1 cua bai) -> Chua noi duoc gi -> Bay (cung 32 cm trong 0,8 s = nhu nhau?) -> Chot + cau
#       hoi (bi dung o 0,8 s roi lan nguoc xuong: a co doi chieu khong? - chua hien tren man, khac ca Du doan).
# Mau: cham vi tri = cam, v = xanh duong, a = xanh la; huy hieu dap an nen NAVY (khong dung xanh la cua a).
from engine import *

DATA = [(0, 8, 16, 24, 32), (0, 2, 8, 18, 32), (0, 14, 24, 30, 32)]       # so_lieu_mau (cm)
V0A = [(0.4, 0.0), (0.0, 1.0), (0.8, -1.0)]                                # (v0 m/s, a m/s2)
NAMES = ["Trên bàn", "Xuống dốc", "Lên dốc"]
KIND = ["đều", "nhanh dần", "chậm dần"]
DT = 0.2
PX0, PX1 = 120, 960; PXCM = (PX1 - PX0) / 32                                # 32 cm = 840 px
STEEL = (148, 163, 184)
RAMP = (226, 232, 240); RAMP_D = (100, 116, 139)
HL = (255, 237, 213)
DRED = (185, 28, 28)

_GK = "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"; _gc = {}
def FG(size):
    size = int(size)
    if size not in _gc: _gc[size] = ImageFont.truetype(_GK, size)
    return _gc[size]
def sym(d, xy, s, size, col, alpha=1.0, anchor="mm"):   # ky hieu dai luong (v, a) chu nghieng co chan
    dtext(d, xy, s, FG(size), col, alpha, anchor)

def X(cm): return PX0 + cm * PXCM
def gaps(i): r = DATA[i]; return [r[k + 1] - r[k] for k in range(4)]
def xpos(i, tau):  # cm theo mo hinh, tau trong [0; 0,8] s (tai tau = n.0,2 dung bang so lieu)
    v0, a = V0A[i]; tau = clamp(tau, 0, 0.8); return 100 * (v0 * tau + a * tau * tau / 2)

def ruler(d, y, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([PX0 - 14, y, PX1 + 14, y + 34], fill=c((253, 230, 138)), outline=c((161, 98, 7)), width=3)
    for cm in range(0, 33, 2):
        L = 22 if cm % 8 == 0 else 11
        d.line([(X(cm), y), (X(cm), y + L)], fill=c(NAVY), width=3 if L == 22 else 2)
    for cm in (0, 8, 16, 24, 32): text(d, (X(cm), y + 66), str(cm), 36, INK, alpha=alpha)
    text(d, (PX1 + 34, y + 66), "cm", 36, INK, anchor="lm", alpha=alpha)

def dots(d, y, i, n, alpha=1.0, r=12):
    for k in range(n): dot(d, X(DATA[i][k]), y, r, A(ORANGE, alpha), outline=A(NAVY, alpha))

def gap_labels(d, y, i, alpha=1.0, col=INK, which=range(4)):
    r = DATA[i]
    for k in which:
        text(d, ((X(r[k]) + X(r[k + 1])) / 2, y), str(r[k + 1] - r[k]), 38, col, alpha=alpha)

def ball(d, x, y, R, alpha=1.0):
    d.ellipse([x - R, y - R, x + R, y + R], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=4)
    d.ellipse([x - R * 0.55, y - R * 0.6, x - R * 0.1, y - R * 0.15], fill=A(WHITE, alpha * 0.8))

def chip(d, s, alpha=1.0, y=262, col=PURPLE, bg=(245, 243, 255)):
    f = F(36); pw = tw(d, s, f) + 56
    card(d, (W / 2 - pw / 2, y - 32, W / 2 + pw / 2, y + 32), fill=A(bg, alpha), outline=A(col, alpha), r=30, w=3)
    text(d, (W / 2, y), s, 36, col, alpha=alpha)

def varrow(d, x0, x1, y, col, lab, alpha=1.0):  # mui ten ngang + ky hieu canh DAU mui ten
    arrow(d, (x0, y), (x1, y), A(col, alpha), w=7, head=20)
    sym(d, (x1 + (28 if x1 > x0 else -28), y - 4), lab, 50, col, alpha)

# ---------------- canh 1: du doan ----------------
RB = (120, 880); RT = (960, 470)
UL = math.hypot(RT[0] - RB[0], RT[1] - RB[1]); U = ((RT[0] - RB[0]) / UL, (RT[1] - RB[1]) / UL); NR = (U[1], -U[0])
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = appear(t, 0.1)
    tri = [RB, (RT[0], RB[1]), RT]
    d.polygon(tri, fill=A(RAMP, k)); d.line(tri + [tri[0]], fill=A(RAMP_D, k), width=5)
    d.line([(60, RB[1]), (1020, RB[1])], fill=A(NAVY, k), width=6)
    text(d, (760, 820), "Máng nghiêng", 40, MUTED, alpha=k)
    s0 = 0.30 * UL; R = 34
    cx, cy = RB[0] + U[0] * s0 + NR[0] * R, RB[1] + U[1] * s0 + NR[1] * R
    for j in (1, 2, 3):                                             # vet mo phia sau: bi dang lan
        bx, by = cx - U[0] * 26 * j, cy - U[1] * 26 * j
        d.ellipse([bx - R, by - R, bx + R, by + R], fill=A(STEEL, k * (0.28 - 0.07 * j)))
    ball(d, cx, cy, R, alpha=k)
    kv = appear(t, 0.6)
    a0 = (cx + U[0] * 50, cy + U[1] * 50); a1 = (cx + U[0] * 240, cy + U[1] * 240)
    arrow(d, a0, a1, A(BLUE, kv), w=7, head=22)
    sym(d, (a1[0] + NR[0] * 48, a1[1] + NR[1] * 48), "v", 52, BLUE, kv)
    kq = appear(t, M[1] - 0.4, 0.5)
    if kq <= 0: return
    y0 = 960 + (1 - kq) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, kq), outline=A(PURPLE, kq), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, kq), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=kq)
    ctext(d, y0 + 160, "Bi đang lăn lên máng, chưa dừng.", 42, MUTED, maxw=880, alpha=kq)
    ctext(d, y0 + 230, "Chấm vị trí bi mỗi 0,2 s.", 46, INK, maxw=880, alpha=kq)
    ctext(d, y0 + 370, "Khoảng cách hai chấm liên tiếp đổi thế nào?", 48, INK, maxw=860, alpha=kq)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 500, 880, y0 + 516], radius=8, fill=A(LIGHT, kq))
    if q < 1: d.rounded_rectangle([200, y0 + 500, 200 + 680 * (1 - q), y0 + 516], radius=8, fill=A(PURPLE, kq))

# ---------------- canh 2: tien hanh (ba lan chay cham) ----------------
L0, LG, SLOW = 0.6, 2.5, 2.5           # lan i bat dau L0 + i.LG; 0,8 s that chieu cham 2,5 lan = 2,0 s
BADGE = 8.3
LY = [370, 680, 990]                   # dong ten lan; cham o +125; thuoc o +165
def lane_tau(i, t): return (t - (L0 + LG * i)) / SLOW       # thoi gian that cua lan i (s)
def nshot(tau): return -1 if tau < 0 else min(4, int(tau / DT + 1e-9))   # so anh da chup (chi so cham cuoi)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    kb = appear(t, BADGE, 0.4)
    if kb < 1: chip(d, "Đang đoán: lên dốc, khoảng cách?", alpha=1 - kb)
    for i, Y in enumerate(LY):
        tau = lane_tau(i, t)
        ka = appear(t, 0.05 + 0.15 * i, 0.4)
        active = 0 <= tau < 0.8 + 0.35
        if i == 2 and kb > 0:
            d.rounded_rectangle([70, Y - 40, 1060, Y + 250], radius=24, fill=A(HL, kb))
        text(d, (80, Y), NAMES[i], 44, INK if (tau >= 0) else MUTED, anchor="lm", alpha=ka)
        d.line([(PX0 - 30, Y + 125), (PX1 + 30, Y + 125)], fill=A(LIGHT, ka), width=4)
        ruler(d, Y + 165, alpha=ka)
        n = nshot(tau)
        if n >= 0:
            dots(d, Y + 125, i, n + 1)
            if active:   # dong ho = thoi diem anh vua chup, doi cung luc cham moi hien
                text(d, (1000, Y), f"t = {n * 2 / 10:.1f} s".replace(".", ","), 44, NAVY, anchor="rm")
            if tau < 0.8 + 0.05:
                xb = xpos(i, tau); ball(d, X(xb), Y + 125, 24)
        if tau >= 0.8 + 0.2:
            gap_labels(d, Y + 70, i, alpha=appear(t, L0 + LG * i + 0.8 * SLOW + 0.2, 0.3))
    chip(d, "Chiếu chậm", alpha=appear(t, 0.3), y=1290, col=NAVY, bg=(239, 246, 255))
    kr = appear(t, 0.5)
    text(d, (W / 2 - 40, 1530), "Thước dọc chiều lăn", 40, INK, alpha=kr)
    arrow(d, (W / 2 + 170, 1530), (W / 2 + 300, 1530), A(INK, kr), w=6, head=20)
    if kb > 0:
        s_ = "ĐÁP ÁN · Ngắn dần"; pw = tw(d, s_, F(46)) + 80
        card(d, (W / 2 - pw / 2, 1340, W / 2 + pw / 2, 1450), fill=A(NAVY, kb), r=28)
        text(d, (W / 2, 1395), s_, 46, WHITE, alpha=kb)

# ---------------- canh 3: rut ra ----------------
RY = [400, 690, 980]
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k0 = appear(t, 0.05, 0.35)
    sym(d, (300, 300), "v", 50, BLUE, k0); text(d, (330, 300), ": vận tốc", 40, INK, anchor="lm", alpha=k0)
    sym(d, (620, 300), "a", 50, GREEN, k0); text(d, (650, 300), ": gia tốc", 40, INK, anchor="lm", alpha=k0)
    show = [0.2, M[0], M[1]]
    for i, Y in enumerate(RY):
        k = appear(t, show[i] - 0.05, 0.4)
        text(d, (80, Y), NAMES[i], 44, INK, anchor="lm", alpha=k0)
        if k > 0:
            text(d, (80 + tw(d, NAMES[i], F(44)) + 24, Y), "→ " + KIND[i], 44, (154, 52, 18), anchor="lm", alpha=k)
        gap_labels(d, Y + 75, i, alpha=k0)
        d.line([(PX0 - 30, Y + 135), (PX1 + 30, Y + 135)], fill=A(LIGHT, k0), width=4)
        dots(d, Y + 135, i, 5, alpha=k0)
        if k > 0:
            varrow(d, 120, 230, Y + 200, BLUE, "v", k)
            text(d, (290, Y + 200), ("không đổi", "tăng", "giảm")[i], 44, INK, anchor="lm", alpha=k)
            if i == 0: sym(d, (760, Y + 196), "a = 0", 48, GREEN, k)
            elif i == 1: varrow(d, 700, 810, Y + 200, GREEN, "a", k)
            else: varrow(d, 810, 700, Y + 200, GREEN, "a", k)
    kc = appear(t, M[1] + 1.0, 0.4)
    if kc > 0:
        card(d, (60, 1320, 1020, 1480), fill=A((255, 247, 237), kc), outline=A(ORANGE, kc), r=26, w=4)
        text(d, (W / 2, 1400), "Khoảng mỗi 0,2 s đổi → v đổi", 48, INK, alpha=kc)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 1200), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 560), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 320, "Chưa biết v lúc bi", 52, INK, alpha=k)
    ctext(d, y1 + 410, "qua từng chấm", 52, INK, alpha=k)
    k2 = appear(t, 1.0, 0.4)                                         # hai cham ke nhau: chi biet khoang
    yb = y1 + 850; xa, xb = 300, 780
    d.line([(160, yb), (920, yb)], fill=A(LIGHT, k2), width=4)
    for xx in (xa, xb): dot(d, xx, yb, 14, A(ORANGE, k2), outline=A(NAVY, k2))
    d.line([(xa, yb + 40), (xa, yb + 70)], fill=A(INK, k2), width=3); d.line([(xb, yb + 40), (xb, yb + 70)], fill=A(INK, k2), width=3)
    d.line([(xa, yb + 55), (xb, yb + 55)], fill=A(INK, k2), width=3)
    text(d, ((xa + xb) / 2, yb + 105), "khoảng đo được", 40, INK, alpha=k2)
    d.line([(xa, yb - 25), (xa + 60, yb - 120)], fill=A(PURPLE, k2), width=4)
    text(d, (xa + 70, yb - 150), "v ở đây?", 44, PURPLE, anchor="lm", alpha=k2)

# ---------------- canh 5: bay ----------------
BT0 = 1.7
BY = [800, 1060, 1320]
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 640), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    q = "Cùng 32 cm, 0,8 s → như nhau"; f = F(48); lw = tw(d, q, f); yy = 500
    text(d, (W / 2, yy), q, 48, DRED, alpha=a)
    ks = clamp((t - 0.9) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=7)
    card(d, (60, 680, 1020, 1530), fill=WHITE, outline=NAVY, w=4)
    d.line([(X(32), 700), (X(32), 1440)], fill=A(MUTED, a), width=3)
    text(d, (X(0), 1480), "t = 0", 38, INK, alpha=a); text(d, (X(32), 1480), "0,8 s", 38, INK, alpha=a)
    km = appear(t, BT0, 0.4)
    for i, Y in enumerate(BY):
        text(d, (90, Y - 60), NAMES[i], 40, INK, anchor="lm", alpha=a)
        d.line([(PX0 - 30, Y), (PX1 + 30, Y)], fill=A(LIGHT, a), width=4)
        for kk in (0, 4): dot(d, X(DATA[i][kk]), Y, 12, A(ORANGE, a), outline=A(NAVY, a))
        if km > 0:
            for kk in (1, 2, 3): dot(d, X(DATA[i][kk]), Y, 12, A(ORANGE, km), outline=A(NAVY, km))
            gap_labels(d, Y + 50, i, alpha=km)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def body(d, t, k):
        ctext(d, 880, "Bi dừng lúc 0,8 s rồi lăn xuống.\nGia tốc có đổi chiều?",
              48, INK, maxw=900, alpha=appear(t, sc["M"][0] + 0.4, 0.5))
        kh = appear(t, sc["M"][0] + 3.7, 0.5)
        if kh <= 0: return
        card(d, (110, 1080, 970, 1330), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1140, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1245, "Lăn xuống: nhanh dần hay chậm dần?", 42, (154, 52, 18), maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Dài dần: nhanh dần.\nNgắn dần: chậm dần.", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + BADGE, "ding"), (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-gia-toc-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Gia tốc · thachlab.id.vn", scenes=[
 dict(key="hook", title="Viên bi lăn lên máng", draw=s_hook, tail=0.5, caps=[
   ("Quay video bi lăn.", 2.6),
   ("Dừng video, tự đoán.", 7.2)]),
 dict(key="do", title="Chấm vị trí bi", draw=s_do, tail=0.5, caps=[
   ("Ba đoạn, cùng cách chấm.", 5.4),
   ("Nhìn hàng lên dốc.", 4.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Dài dần: a cùng chiều v.", 3.4),
   ("Ngắn dần: a ngược chiều v.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Chấm cho khoảng, chưa cho v tức thời.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Chỉ nhìn chấm cuối: sai.", 2.9),
   ("Khác ở các khoảng giữa.", 2.9)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
