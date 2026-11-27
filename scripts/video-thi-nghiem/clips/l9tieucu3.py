# Clip: tn-l9-tieucu-03 - Cach 3 do tieu cu: tim vi tri anh bang vat, f = L/4 (KHTN 9, 05/11/2026)
# So lieu tu content/thi-nghiem/tn-l9-tieucu-03.json:
#   so_lieu_mau: L = 40,4 cm -> f = L/4 = 10,1 cm ; tham_so: h = 3,0 cm, f that 10,0 cm (mo_hinh.gia_thiet), sai_L = +0,4 cm
#   rut_ra: f = 40,4/4 = 10,1 cm khop cach 1, cach 2 ; dL chia 4 khi tinh f.
# Hinh quang hoc ve dung ti le ngang (20 px/cm, f = 200 px); chieu cao keo gian doc (vat 3,0 cm = 140 px) - phep keo
#   gian mot chieu giu nguyen: tia song song truc van song song, tia qua O van qua O, F' khong doi -> dung quy tac tia.
#   Anh o mat phang man: d' = f.d/(d - f), anh cao k.h voi k = d'/d (nguoc chieu). Khong ghi so vi tri d (kho khong co).
#   Ba vi tri thu: d = 1,5f (k = 2, to hon), d = 3f (k = 0,5, nho hon), d = 2f (k = 1, bang vat). Chi ghi chu, khong ghi so.
# Cau hoi sau hop trong bai (Cau 3: L = 48,0 cm -> f): clip KHONG dung 48, khong giai. THU NGHI dung f = 15 cm (trong
#   tham_so f 5..20) hoi d (= 2f = 30 cm, chua tung hien tren man); khac chot l9tieucu2 (trung binh hai lan do).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (3 vi tri thau kinh, man theo cho net, thanh so chieu cao)
#       -> Dap an (d = d' = 2f, L = 4f, f = L/4, sai lech chia 4) -> Bay (f = L/2) roi Chua noi duoc -> Chot + THU NGHI.
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom D): chu >= 55 (ra >= 48 px), K10 NAVY + thanh dem 70 px,
#   Bay hai hang (L:2 ✗ / L:4 ✓) moi nhip >= 3 s, man chot KHONG goi y. Du doan giu (L = 4f); chot giu f = 15 cm -> d = 30 cm.
from engine import *

AX, OX, FP, HP = 560, 80, 200, 140          # truc chinh, vi tri vat, f (px), chieu cao vat (px)
RAIL = 900                                  # ghe quang hoc
LH = 200                                    # nua chieu cao thau kinh
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253)
FS, FM = 58, 56
L_DO, F_DO, CH_F = 40.4, 10.1, 15                # kho so_lieu_mau ; ca chot: f = 15 cm -> d = 2f = 30 cm


def _kiem():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-tieucu-03.json")))
    assert k["so_lieu_mau"]["hang"] == [[L_DO, F_DO]] and abs(L_DO / 4 - F_DO) < 0.001
    tf = {x["ky_hieu"]: x for x in k["tham_so"]}["f"]
    assert tf["min"] <= CH_F <= tf["max"]


def dprime(dd): return FP * dd / (dd - FP)


def dash(d, p1, p2, col, w=3, on=12, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / L, min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)


def chev(d, p, q, col, s=16, w=4):
    """mui chevron 30 do o trung diem doan p->q, chi chieu truyen tia sang"""
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def lens(d, lx):
    pts = []
    for j in range(41):
        y = -LH + 2 * LH * j / 40; pts.append((lx + 3 + 15 * (1 - (y / LH) ** 2), AX + y))
    for j in range(41):
        y = LH - 2 * LH * j / 40; pts.append((lx - 3 - 15 * (1 - (y / LH) ** 2), AX + y))
    d.polygon(pts, fill=A(LBLUE, 0.75), outline=BLUE)
    d.line([(lx, AX - LH - 4), (lx, AX + LH + 4)], fill=A(BLUE, 0.5), width=2)


def bench(d, dd, img_on=True, rays=1.0, guide=False, labels=True, ftag=True, sx_at=None):
    """vat (do, huong len) - thau kinh cach vat dd px - man o mat phang anh; tia 1 song song -> qua F', tia 2 qua O."""
    lx = OX + dd; dp = dprime(dd); sx = lx + dp if sx_at is None else sx_at; k = dp / dd
    d.rounded_rectangle([20, RAIL - 8, 1060, RAIL + 8], radius=8, fill=(205, 198, 186))
    for x, y0 in ((OX, AX + 6), (lx, AX + LH), (sx, AX + 300)):
        d.rectangle([x - 5, y0, x + 5, RAIL - 8], fill=GRAY)
    d.line([(20, AX), (1060, AX)], fill=A(NAVY, 0.6), width=3)              # truc chinh
    if guide:                                                              # muc chieu cao vat, phia duoi truc
        dash(d, (OX, AX + HP), (sx + 30, AX + HP), A(GRAY, 0.9), w=3)
        text(d, (OX + 8, AX + HP + 44), "mức 3,0 cm", FM, NAVY, anchor="lm")   # kiem-v1 muc 4: chu phu mau dam
    d.rounded_rectangle([sx - 9, AX - 230, sx + 9, AX + 300], radius=4, fill=WHITE, outline=NAVY, width=3)   # man
    lens(d, lx)
    for x, nm in ((lx - FP, "F"), (lx + FP, "F'")):
        dot(d, x, AX, 8, NAVY)
    text(d, (lx - FP, AX + 40), "F", FM, NAVY)
    text(d, (lx + FP + 26, AX - 38), "F'", FM, NAVY)
    arrow(d, (OX, AX), (OX, AX - HP), RED, w=9, head=26)                   # vat sang mui ten
    if img_on and rays > 0:
        B, P, Bp = (OX, AX - HP), (lx, AX - HP), (sx, AX + k * HP)
        c = A(ORANGE, 0.9 * rays)
        for p, q in ((B, P), (P, Bp), (B, Bp)):
            d.line([p, q], fill=c, width=4)
        chev(d, B, P, c); chev(d, P, (lx + FP, AX), c); chev(d, (lx, AX), Bp, c); chev(d, B, (lx, AX), c)
    if img_on:
        arrow(d, (sx, AX), (sx, AX + k * HP), BLUE, w=9, head=26)           # anh that, nguoc chieu
    if labels:
        text(d, (OX + 10, AX - HP - 44), "vật 3,0 cm", FM, RED, anchor="lm")
        text(d, (lx, AX - LH - 42), "thấu kính", FM, BLUE)
        text(d, (min(sx, 1010), AX - 266), "màn", FM, NAVY)
    return lx, sx, k


def bar_card(d, k, state, sub=None):
    """so chieu cao: vat (len) va anh (xuong, nguoc chieu) quanh mot duong giua"""
    card(d, (60, 1100, 1020, 1560), fill=WHITE, outline=LIGHT, w=3)
    cy = 1330
    d.line([(110, cy), (470, cy)], fill=NAVY, width=4)
    d.rectangle([170, cy - 100, 230, cy], fill=RED)
    hh = 100 * k
    if hh > 2: d.rectangle([340, cy, 400, cy + hh], fill=BLUE)
    dash(d, (110, cy + 100), (470, cy + 100), GRAY, w=3)
    text(d, (200, cy + 44), "vật", FM, RED)
    text(d, (370, cy - 44), "ảnh", FM, BLUE)
    if state:
        text(d, (745, cy - (40 if sub else 0)), state, FS, INK)
        if sub: text(d, (745, cy + 44), sub, FM, INK)


# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    lx, sx, k = bench(d, 1.5 * FP, img_on=False, sx_at=OX + 3.2 * FP)   # man chua o cho anh net, khong goi boi so
    d.line([(lx, AX + 70), (lx + FP, AX + 70)], fill=NAVY, width=4)       # doan f = OF'
    for x in (lx, lx + FP): d.line([(x, AX + 58), (x, AX + 82)], fill=NAVY, width=4)
    text(d, (lx + FP / 2, AX + 116), "f", FS, NAVY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 940 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 620), fill=A(WHITE, a), outline=A(NAVY, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(NAVY, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    for j, s_ in enumerate(("Ảnh nét, cao bằng vật.", "L (vật – màn)", "bằng mấy lần f?")):
        text(d, (W / 2, y0 + 170 + j * 82), s_, 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 500, 970, y0 + 570], radius=35, fill=A((226, 232, 240), a))
        if p < 1: d.rounded_rectangle([110, y0 + 500, 110 + max(70, 860 * (1 - p)), y0 + 570], radius=35, fill=A(NAVY, a))


# ---------------- canh 2: Tien hanh ----------------
# (bat dau dich, ket thuc dich, d dich toi) ; man luon dich theo cho net (anh o mat phang man)
MOVES = [(1.8, 3.0, 3.0), (6.4, 7.6, 2.0)]
T_EQ = 7.6                                   # anh bang vat, hien L cung luc


def lens_d(t):
    dd = 1.5
    for a, b, to in MOVES:
        if t >= a: dd = lerp(dd, to, ease((t - a) / (b - a)))
    return dd * FP


def s_do(img, d, t, sc):
    dd = lens_d(t)
    lx, sx, k = bench(d, dd, guide=True)
    moving = any(a < t < b for a, b, _ in MOVES)
    if moving: st, sub = None, None
    elif t < MOVES[0][0]: st, sub = "ảnh to hơn vật", None
    elif t < MOVES[1][0]: st, sub = "ảnh nhỏ hơn vật", None
    else: st, sub = "ảnh bằng vật", "thật, ngược chiều"
    bar_card(d, k, st, sub)
    if t >= T_EQ:
        arrow(d, (OX + 40, 960), (OX, 960), NAVY, w=4, head=16)
        arrow(d, (sx - 40, 960), (sx, 960), NAVY, w=4, head=16)
        d.line([(OX, 960), (sx, 960)], fill=NAVY, width=4)
        text(d, ((OX + sx) / 2, 1020), "L = 40,4 cm", FS, NAVY)


# ---------------- canh 3: Dap an + rut ra ----------------
def seg(d, x0, x1, y, col, w=4):
    d.line([(x0, y), (x1, y)], fill=col, width=w)
    for x in (x0, x1): d.line([(x, y - 12), (x, y + 12)], fill=col, width=w)


def pill(d, s, y, a, color=NAVY, size=FM):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


DA_S, DA_C, DA_E = 2.2, 4.4, 6.8
def s_dapan(img, d, t, sc):
    pill(d, "ĐÁP ÁN: L = 4f", 260, appear(t, 0.15, 0.4))
    lx, sx, k = bench(d, 2 * FP, labels=False)
    k1 = appear(t, DA_S, 0.4)
    if k1 > 0:
        seg(d, OX, lx, 945, A(RED, k1)); seg(d, lx, sx, 945, A(BLUE, k1))
        text(d, ((OX + lx) / 2, 995), "d = 2f", FS, RED, alpha=k1)
        text(d, ((lx + sx) / 2, 995), "d' = 2f", FS, BLUE, alpha=k1)
        y = 1060
        d.line([(OX, y), (sx, y)], fill=A(NAVY, k1), width=4)
        for j in range(5): d.line([(OX + j * FP, y - 12), (OX + j * FP, y + 12)], fill=A(NAVY, k1), width=4)
        for j in range(4): text(d, (OX + (j + 0.5) * FP, y + 36), "f", FM, NAVY, alpha=k1)
    k3 = appear(t, DA_C, 0.4)
    if k3 > 0:
        kq = 0.5 + 0.5 * math.sin(2.4 * (t - DA_C)) ** 2              # vien nhap nhay: hinh khong dung yen
        card(d, (60, 1150, 1020, 1310), fill=A((236, 253, 243), k3), outline=A(GREEN, k3 * kq), r=22, w=8)
        text(d, (W / 2, 1230), "f = 40,4 : 4 = 10,1 cm", FS, DGREEN, alpha=k3)
    k4 = appear(t, DA_E, 0.4)
    if k4 > 0:
        card(d, (40, 1340, 1040, 1530), fill=A((255, 247, 237), k4), outline=A(ORANGE, k4), r=22, w=4)
        text(d, (W / 2, 1395), "Nếu L sai 0,4 cm", FS, (154, 52, 18), alpha=k4)      # kiem-v1 muc 2: gia dinh, khong
        text(d, (W / 2, 1475), "thì f chỉ sai 0,1 cm", FS, (154, 52, 18), alpha=k4)  #   neu so lech khong co nguon


# ---------------- canh 4: Bay + chua noi duoc ----------------
BAY_R, BAY_E = 3.4, 6.6
def s_bay(img, d, t, sc):
    lx, sx, k = bench(d, 2 * FP, rays=0.4, labels=False)
    a1 = appear(t, 0.3, 0.45)
    if a1 > 0:
        seg(d, OX, lx, 310, A(DRED, a1), w=8)                          # L:2 = doan vat - kinh = d (kiem-v1 muc 3: dua len tren,
        text(d, ((OX + lx) / 2, 356), "d", FS, DRED, alpha=a1)         #   xa chu BAY, co nhan d / f)
        pill(d, "BẪY", 1000, a1, color=DRED)
        card(d, (40, 1050, 1040, 1190), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
        text(d, (90, 1120), "f = L : 2 = 20,2 cm", FS, DRED, anchor="lm", alpha=a1)
        text(d, (980, 1120), "✗", 80, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        seg(d, lx, lx + FP, 310, A(DGREEN, a2), w=8)                   # f = OF' : mot phan tu L
        text(d, (lx + FP / 2 + 40, 356), "f", FS, DGREEN, alpha=a2)
        card(d, (40, 1205, 1040, 1345), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (90, 1275), "f = L : 4 = 10,1 cm", FS, DGREEN, anchor="lm", alpha=a2)
        text(d, (980, 1275), "✓", 80, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (40, 1360, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1412), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1498), "số liệu minh hoạ; kính mỏng", FM, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 4.3
EY = 1180
def s_end(img, d, t, sc):
    # GD2 kiem-v1 muc 1: bo the xanh "f = L : 4" (tra loi san)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 630), f"Thấu kính f = {CH_F} cm,", FS, INK, alpha=k1)
    text(d, (W / 2, 712), "ảnh cao bằng vật.", FS, INK, alpha=k1)
    text(d, (W / 2, 794), "Kính cách vật bao nhiêu?", FS, INK, alpha=k1)
    if k1 > 0:   # hinh: vat - kinh - man, anh nguoc chieu bang vat; khong ve tia, khong ghi so
        ox, lx, sx = 150, 540, 930
        d.line([(80, EY), (1000, EY)], fill=A(NAVY, 0.6 * k1), width=3)
        arrow(d, (ox, EY), (ox, EY - 120), A(RED, k1), w=9, head=24)
        d.ellipse([lx - 22, EY - 170, lx + 22, EY + 170], fill=A(LBLUE, 0.8 * k1), outline=A(BLUE, k1), width=4)
        arrow(d, (sx, EY), (sx, EY + 120), A(BLUE, k1), w=9, head=24)
        d.rounded_rectangle([sx + 14, EY - 180, sx + 30, EY + 180], radius=4, fill=A(WHITE, k1), outline=A(NAVY, k1), width=3)
        kq = 0.55 + 0.45 * math.sin(2.4 * t) ** 2
        d.rounded_rectangle([ox, EY + 205, lx, EY + 360], radius=20, fill=A((253, 186, 116), k1 * (kq - 0.55) / 0.45))  # nhap nhay: hinh khong dung yen
        seg(d, ox, lx, EY + 230, A(ORANGE, k1), w=5)
        text(d, ((ox + lx) / 2, EY + 290), "?", 84, ORANGE, alpha=k1 * kq)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + T_EQ, "tap"), (da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"),
            (e["t0"] + END_Q + 0.1, "open")]


CLIP = dict(id="tn-l9-tieucu-03", header="KHTN 9 · THÍ NGHIỆM", footer="Đo tiêu cự thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ảnh cao bằng vật", draw=s_hook, tail=0.3, caps=[
   ("Thấu kính hội tụ, vật sáng, màn.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Dịch thấu kính, dịch màn cho nét.", 5.3),
   ("Ảnh bằng vật thì đo L.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Ảnh bằng vật khi d = d' = 2f.", DA_C),
   ("Sai lệch của L bị chia 4.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("So hai cách chia L.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 8.2)]),
])

_kiem()
