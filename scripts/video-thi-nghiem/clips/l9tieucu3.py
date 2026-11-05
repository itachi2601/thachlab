# Clip: tn-l9-tieucu-03 - Cach 3 do tieu cu: tim vi tri anh bang vat, f = L/4 (KHTN 9, 05/11/2026)
# So lieu tu content/thi-nghiem/tn-l9-tieucu-03.json:
#   so_lieu_mau: L = 40,4 cm -> f = L/4 = 10,1 cm ; tham_so: h = 3,0 cm, f that 10,0 cm (mo_hinh.gia_thiet), sai_L = +0,4 cm
#   rut_ra: f = 40,4/4 = 10,1 cm khop cach 1, cach 2 ; dL chia 4 khi tinh f.
# Hinh quang hoc ve dung ti le ngang (20 px/cm, f = 200 px); chieu cao keo gian doc (vat 3,0 cm = 140 px) - phep keo
#   gian mot chieu giu nguyen: tia song song truc van song song, tia qua O van qua O, F' khong doi -> dung quy tac tia.
#   Anh o mat phang man: d' = f.d/(d - f), anh cao k.h voi k = d'/d (nguoc chieu). Khong ghi so vi tri d (kho khong co).
#   Ba vi tri thu: d = 1,5f (k = 2, to hon), d = 3f (k = 0,5, nho hon), d = 2f (k = 1, bang vat). Chi ghi chu, khong ghi so.
# Cau hoi sau hop trong bai (Cau 3: L = 48,0 cm -> f): clip KHONG dung 48, khong giai. THU NGHI dung f = 15 cm (trong
#   tham_so f 5..20) hoi d (= 2f = 30 cm, chua tung hien tren man).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (3 vi tri thau kinh, man theo cho net, thanh so chieu cao)
#       -> Dap an (d = d' = 2f, L = 4f, f = L/4, sai lech chia 4) -> Bay (f = L/2) roi Chua noi duoc -> Chot + THU NGHI.
from engine import *

AX, OX, FP, HP = 560, 80, 200, 140          # truc chinh, vi tri vat, f (px), chieu cao vat (px)
RAIL = 900                                  # ghe quang hoc
LH = 200                                    # nua chieu cao thau kinh
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253)


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
        text(d, (OX + 8, AX + HP + 40), "mức 3,0 cm", 40, MUTED, bold=False, anchor="lm")
    d.rounded_rectangle([sx - 9, AX - 230, sx + 9, AX + 300], radius=4, fill=WHITE, outline=NAVY, width=3)   # man
    lens(d, lx)
    for x, nm in ((lx - FP, "F"), (lx + FP, "F'")):
        dot(d, x, AX, 8, NAVY)
    text(d, (lx - FP, AX + 36), "F", 40, NAVY)
    text(d, (lx + FP + 24, AX - 34), "F'", 40, NAVY)
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
        text(d, (OX + 10, AX - HP - 40), "vật 3,0 cm", 40, RED, anchor="lm")
        text(d, (lx, AX - LH - 40), "thấu kính", 40, BLUE)
        text(d, (sx, AX - 262), "màn", 40, NAVY)
    return lx, sx, k


def bar_card(d, k, state, sub=None, ka=1.0):
    """so chieu cao: vat (len) va anh (xuong, nguoc chieu) quanh mot duong giua"""
    card(d, (60, 1100, 1020, 1560), fill=WHITE, outline=LIGHT, w=3)
    cy = 1340
    d.line([(200, cy), (560, cy)], fill=NAVY, width=4)
    d.rectangle([270, cy - 100, 330, cy], fill=RED)
    hh = 100 * k
    if hh > 2: d.rectangle([430, cy, 490, cy + hh], fill=BLUE)
    dash(d, (200, cy + 100), (560, cy + 100), GRAY, w=3)
    text(d, (300, cy + 36), "vật", 40, RED)
    text(d, (460, cy - 36), "ảnh", 40, BLUE)
    if state:
        text(d, (790, cy - (28 if sub else 0)), state, 46, INK, alpha=ka)
        if sub: text(d, (790, cy + 36), sub, 40, MUTED, bold=False, alpha=ka)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    lx, sx, k = bench(d, 1.5 * FP, img_on=False, sx_at=OX + 3.2 * FP)   # man chua o cho anh net, khong goi boi so
    d.line([(lx, AX + 70), (lx + FP, AX + 70)], fill=NAVY, width=4)       # doan f = OF'
    for x in (lx, lx + FP): d.line([(x, AX + 58), (x, AX + 82)], fill=NAVY, width=4)
    text(d, (lx + FP / 2, AX + 116), "f = tiêu cự", 40, NAVY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 290, "Màn hứng được ảnh nét,\ncao đúng bằng vật. Khoảng\ncách L (vật – màn) bằng\nmấy lần f?",
          50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 530, 940, y0 + 542], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 530, 140 + 800 * (1 - p), y0 + 542], radius=6, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
# (bat dau dich, ket thuc dich, d dich toi) ; man luon dich theo cho net (anh o mat phang man)
MOVES = [(2.2, 3.4, 3.0), (6.2, 7.4, 2.0)]
T_EQ, T_L = 7.4, 7.8                         # anh bang vat ; hien L


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
    elif t < 2.2: st, sub = "ảnh to hơn vật", None
    elif t < 6.2: st, sub = "ảnh nhỏ hơn vật", None
    else: st, sub = "ảnh bằng vật", "ảnh thật, ngược chiều"
    bar_card(d, k, st, sub, ka=1.0)
    kL = appear(t, T_L, 0.4)
    if kL > 0:
        arrow(d, (OX + 40, 955), (OX, 955), A(NAVY, kL), w=4, head=16)
        arrow(d, (sx - 40, 955), (sx, 955), A(NAVY, kL), w=4, head=16)
        d.line([(OX, 955), (sx, 955)], fill=A(NAVY, kL), width=4)
        text(d, ((OX + sx) / 2, 1004), "L = 40,4 cm", 48, NAVY, alpha=kL)


# ---------------- canh 3: Dap an + rut ra ----------------
def seg(d, x0, x1, y, col, w=4):
    d.line([(x0, y), (x1, y)], fill=col, width=w)
    for x in (x0, x1): d.line([(x, y - 12), (x, y + 12)], fill=col, width=w)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · L = 4f"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 226, W / 2 + pw / 2, 292), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 259), lab, 42, WHITE, alpha=ka)
    lx, sx, k = bench(d, 2 * FP, labels=False)
    k1 = appear(t, M[0] + 0.3, 0.4)
    if k1 > 0:
        seg(d, OX, lx, 945, A(RED, k1)); seg(d, lx, sx, 945, A(BLUE, k1))
        text(d, ((OX + lx) / 2, 985), "d = 2f", 44, RED, alpha=k1)
        text(d, ((OX + lx) / 2, 1032), "vật – thấu kính", 40, MUTED, bold=False, alpha=k1)
        text(d, ((lx + sx) / 2, 985), "d' = 2f", 44, BLUE, alpha=k1)
        text(d, ((lx + sx) / 2, 1032), "thấu kính – màn", 40, MUTED, bold=False, alpha=k1)
    k2 = appear(t, M[0] + 1.3, 0.4)
    if k2 > 0:
        y = 1088
        d.line([(OX, y), (sx, y)], fill=A(NAVY, k2), width=4)
        for j in range(5): d.line([(OX + j * FP, y - 12), (OX + j * FP, y + 12)], fill=A(NAVY, k2), width=4)
        for j in range(4): text(d, (OX + (j + 0.5) * FP, y + 30), "f", 40, NAVY, alpha=k2)
        text(d, (975, y), "L = 4f", 46, NAVY, alpha=k2)
    k3 = appear(t, M[0] + 2.3, 0.4)
    if k3 > 0:
        card(d, (60, 1170, 1020, 1350), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=22, w=3)
        text(d, (W / 2, 1226), "f = L/4 = 40,4/4 = 10,1 cm", 48, DGREEN, alpha=k3)
        text(d, (W / 2, 1298), "khớp cách 1 và cách 2", 40, MUTED, bold=False, alpha=k3)
    k4 = appear(t, M[1] + 0.2, 0.4)
    if k4 > 0:
        card(d, (60, 1380, 1020, 1560), fill=A((255, 247, 237), k4), outline=A(ORANGE, k4), r=22, w=3)
        text(d, (W / 2, 1436), "L lệch 0,4 cm → f chỉ lệch 0,1 cm", 44, (154, 52, 18), alpha=k4)
        text(d, (W / 2, 1506), "f thật 10,0 cm (mô hình)", 40, MUTED, bold=False, alpha=k4)


# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    lx, sx, k = bench(d, 2 * FP, rays=0.45, labels=False)
    if a1 > 0:
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, M[0] + 2.3, 0.5)    # sai: cung luc chu ; dung: tre >= 2 s
        if k3 > 0:
            seg(d, OX, lx, 945, A(DRED, k3), w=6)
            text(d, ((OX + lx) / 2, 990), "L/2 = d", 44, DRED, alpha=k3)
        if k4 > 0:
            seg(d, lx, lx + FP, 945, A(DGREEN, k4), w=6)
            text(d, (lx + FP / 2, 990), "f", 44, DGREEN, alpha=k4)
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 520), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        text(d, (440, y0 + 175), "f = L/2", 56, DRED, alpha=k3)
        if k3 > 0: d.line([(330, y0 + 178), (550, y0 + 178)], fill=A(DRED, k3), width=6)
        text(d, (820, y0 + 180), "✗", 100, DRED, alpha=k3)
        text(d, (W / 2, y0 + 255), "L/2 là d: đoạn vật – thấu kính", 42, DRED, alpha=k3)
        text(d, (440, y0 + 365), "f = L/4", 56, DGREEN, alpha=k4)
        text(d, (820, y0 + 370), "✓", 100, DGREEN, alpha=k4)
        text(d, (W / 2, y0 + 445), "L gồm hai đoạn 2f", 42, DGREEN, alpha=k4)
    if k2 > 0:
        y0 = 1040 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ, chưa đo thật", "• Chỉ đúng cho thấu kính mỏng")):
            kk = k2 * appear(t, M[1] + 0.1 + 0.3 * j, 0.4)
            text(d, (90, y0 + 165 + j * 95), l1, 44, INK, anchor="lm", alpha=kk)


# ---------------- canh 5: Chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: f = 15 cm, anh bang vat -> d = ? (30 cm); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Ảnh bằng vật: L = 4f,\nnên f = L/4", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (40, 600, 1040, lerp(1030, 1330, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 850, "Thấu kính f = 15 cm, ảnh\nbằng vật. Thấu kính cách\nvật bao nhiêu cm?", 48, INK,
          maxw=920, alpha=appear(t, M[0] + 0.9, 0.5))
    if kh > 0:
        card(d, (110, 1010, 970, 1290), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1065, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1180, "Thấu kính ở đâu\ngiữa vật và màn?", 46, ORANGE, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + T_EQ, "tap"), (da["t0"] + 0.1, "ding"), (b["t0"] + 0.5, "buzz"),
            (e["t0"] + e["M"][0] + 0.6, "open")]


CLIP = dict(id="tn-l9-tieucu-03", header="KHTN 9 · THÍ NGHIỆM", footer="Đo tiêu cự thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ảnh cao bằng vật", draw=s_hook, tail=0.8, caps=[
   ("Thấu kính hội tụ, vật sáng và màn.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Dịch thấu kính, dịch màn cho nét.", 5.6),
   ("Chỉnh tới khi ảnh bằng vật, đo L.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Ảnh bằng vật khi d = d' = 2f.", 4.2),
   ("Sai lệch của L bị chia 4.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Lấy L chia 2 được f?", 3.8),
   ("Chưa nói được điều gì?", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.3, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])
