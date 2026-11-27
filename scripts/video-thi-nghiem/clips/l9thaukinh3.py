# Clip: tn-l9-thaukinh-03 - Do d, d' tren thuoc quang hoc va tinh tieu cu (KHTN 9, lo 5, 18/11/2026)
# So lieu tu content/thi-nghiem/tn-l9-thaukinh-03.json (so_lieu_mau):
#   d = 12, 16, 24, 36, 50 cm ; d' doc = 57,0 ; 26,9 ; 17,2 ; 13,8 ; 12,6 cm ; f tinh ra = 9,91 ; 10,03 ; 10,02 ; 9,98 ; 10,06 cm
#   tham_so f = 10 cm. Bay (hien_tuong_hay_sai 1): f = (d + d')/2 -> hang d = 24: (24 + 17,2)/2 = 20,6 cm (sai),
#   24.17,2/41,2 = 10,02 cm (dung) -- da ghi vao ghi_chu cua kho.
# Hinh: vat co dinh, dich thau kinh toi d roi dich man toi d' doc (ti le ngang 14 px/cm, f = 140 px). Tia song song -> F',
#   tia qua O di thang, hoi tu tai anh that theo d' = d.f/(d - f); man dat o d' doc (lech <= 3 cm -> vet loe <= 3 px).
#   Chieu cao keo gian doc (vat 50 px): k = d'/d, anh nguoc chieu.
# Khong tra loi san: Cau 3 (f = 8, d = 12 -> d'), hop "Doc so lieu" (trung binh f, lan lech nhieu nhat) -> clip khong
#   tinh trung binh, khong chi lan lech nhat. Khong noi lai Du doan cua thaukinh-02 (anh nho, nguoc chieu).
# THU NGHI: thau kinh khac, d = 30 cm, d' = 60 cm -> f = 20 cm (bay (d + d')/2 = 45 cm); so 30, 60, 20 chua hien tren man.
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom D): chu >= 55 (ra >= 48 px), K10, thanh dem 70 px, Bay hai hang
#   (20,6 ✗ / 10,02 ✓) moi nhip >= 3 s, man chot KHONG goi y. Du doan + chot giu nhu cu (khong trung Cau 3, hop Doc so lieu,
#   khong trung thaukinh2: clip do hoi giay cach kinh bao nhieu, chot 2 m -> 10,5 cm).
from engine import *

AX, OX, S, HP = 500, 70, 14, 50             # truc chinh, vat, px/cm, chieu cao vat (px)
F_CM = 10.0; FP = F_CM * S
RAIL = 800; LH = 150
ROWS = [(12, 57.0, 9.91), (16, 26.9, 10.03), (24, 17.2, 10.02), (36, 13.8, 9.98), (50, 12.6, 10.06)]
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253)
FS, FM = 58, 56
CH_D, CH_DP = 30, 60                         # ca chot (kho ghi_chu): f = 20 cm


def _kiem():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-thaukinh-03.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS
    for dd, dp, ff in ROWS: assert abs(dd * dp / (dd + dp) - ff) < 0.006 and abs(dp - dd * 10 / (dd - 10)) < 3.01
    assert "d = 30 cm, d' = 60 cm" in k["so_lieu_mau"]["ghi_chu"] and CH_D * CH_DP / (CH_D + CH_DP) == 20


def vn(x, n=1):
    return f"{x:.{n}f}".replace(".", ",")


def dtrue(dd): return dd * F_CM / (dd - F_CM)


def chev(d, p, q, col, s=16, w=4):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def lens(d, lx):
    pts = []
    for j in range(41):
        y = -LH + 2 * LH * j / 40; pts.append((lx + 3 + 14 * (1 - (y / LH) ** 2), AX + y))
    for j in range(41):
        y = LH - 2 * LH * j / 40; pts.append((lx - 3 - 14 * (1 - (y / LH) ** 2), AX + y))
    d.polygon(pts, fill=A(LBLUE, 0.75), outline=BLUE)


def bench(d, d_cm, sx, sharp, rays=1.0, labels=True):
    """vat co dinh o OX, thau kinh cach vat d_cm, man o sx; sharp -> ve tia + anh tai man"""
    lx = OX + d_cm * S
    d.rounded_rectangle([20, RAIL - 8, 1060, RAIL + 8], radius=8, fill=(205, 198, 186))
    for j in range(0, 71, 10):                                            # vach 10 cm tren thuoc
        x = OX + j * S; d.line([(x, RAIL - 8), (x, RAIL + 8)], fill=NAVY, width=3)
    for x, y0 in ((OX, AX + 6), (lx, AX + LH), (sx, AX + 262)):
        d.rectangle([x - 5, y0, x + 5, RAIL - 8], fill=GRAY)
    d.line([(20, AX), (1060, AX)], fill=A(NAVY, 0.6), width=3)
    d.rounded_rectangle([sx - 9, AX - 130, sx + 9, AX + 262], radius=4, fill=WHITE, outline=NAVY, width=3)
    lens(d, lx)
    dot(d, lx + FP, AX, 7, NAVY); text(d, (lx + FP, AX - 44), "F'", FM, NAVY)
    arrow(d, (OX, AX), (OX, AX - HP), RED, w=8, head=22)
    if sharp and rays > 0:
        dp = dtrue(d_cm) * S; k = dp / (d_cm * S)
        B, P, Bt = (OX, AX - HP), (lx, AX - HP), (lx + dp, AX + k * HP)
        def at(p, q, x): return (x, p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0]))
        c = A(ORANGE, 0.9 * rays)
        d.line([B, P], fill=c, width=4); chev(d, B, P, c)
        q1 = at(P, Bt, sx); d.line([P, q1], fill=c, width=4); chev(d, P, (lx + FP, AX), c)
        q2 = at(B, Bt, sx); d.line([B, q2], fill=c, width=4); chev(d, B, (lx, AX), c)
        arrow(d, (sx, AX), (sx, (q1[1] + q2[1]) / 2), BLUE, w=8, head=22)
    if labels:
        text(d, (OX + 8, AX - HP - 44), "vật", FM, RED, anchor="lm")
        text(d, (lx, AX - LH - 42), "thấu kính", FM, BLUE)
        if sx - lx >= 220: text(d, (min(sx, 1000), AX - 172), "màn", FM, NAVY)
    return lx


TX = (250, 540, 830)                        # cot bang: d, d' doc, f tinh ra
RH = 80
def table(d, n_rows, n_f, hl=-1, y0=850, a=1.0, fa=None, under=None):
    card(d, (60, y0, 1020, y0 + 112 + 5 * RH), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    if under: under(d)
    for x, h in zip(TX, ("d (cm)", "d' (cm)", "f (cm)")):
        text(d, (x, y0 + 56), h, FM, NAVY, alpha=a)
    d.line([(90, y0 + 100), (990, y0 + 100)], fill=A(LIGHT, a), width=3)
    for i, (dd, dp, ff) in enumerate(ROWS):
        y = y0 + 144 + i * RH
        if i == hl: d.rounded_rectangle([80, y - 36, 1000, y + 36], radius=14, fill=A((254, 243, 199), a))
        if i < n_rows:
            text(d, (TX[0], y), str(dd), FS, INK, alpha=a)
            text(d, (TX[1], y), vn(dp), FS, INK, alpha=a)
        if i < n_f:
            text(d, (TX[2], y), vn(ff, 2), FS, DGREEN, alpha=a * (1 if fa is None else fa(i)))


def pill(d, s, y, a, color=NAVY, size=FM):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bench(d, 20, 980, False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 870 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(NAVY, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(NAVY, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    for j, s in enumerate(("Đặt vật ở 5 chỗ. Mỗi lần", "ảnh rõ, tính d·d' : (d + d').", "Năm kết quả thế nào?")):
        text(d, (W / 2, y0 + 170 + j * 82), s, 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 520, 970, y0 + 590], radius=35, fill=A((226, 232, 240), a))
        if p < 1: d.rounded_rectangle([110, y0 + 520, 110 + max(70, 860 * (1 - p)), y0 + 590], radius=35, fill=A(NAVY, a))


# ---------------- canh 2: Tien hanh ----------------
T0, STEP, ML, MS = 0.6, 1.95, 0.6, 0.7      # bat dau, moi lan, dich kinh, dich man
D_HOOK, SX_HOOK = 20.0, 980.0


def do_state(t):
    dcm, sx, rows = D_HOOK, SX_HOOK, 0
    for i, (dd, dp, _) in enumerate(ROWS):
        ti = T0 + i * STEP
        if t < ti: break
        d_prev = dcm
        dcm = lerp(d_prev, dd, ease((t - ti) / ML))
        sx_t = OX + (dd + dp) * S
        sx = lerp(sx, sx_t, ease((t - ti - ML) / MS))
        if t >= ti + ML + MS: rows = i + 1
    sharp = rows > 0 and abs(dcm - ROWS[rows - 1][0]) < 1e-6 and abs(sx - (OX + sum(ROWS[rows - 1][:2]) * S)) < 1e-6
    return dict(d=dcm, sx=sx, rows=rows, sharp=sharp)


def s_do(img, d, t, sc):
    st = do_state(t)
    bench(d, st["d"], st["sx"], st["sharp"])
    table(d, st["rows"], 0, hl=st["rows"] - 1 if st["sharp"] else -1)


# ---------------- canh 3: Dap an + rut ra ----------------
DA_F, DA_R = 1.0, 5.4
def s_dapan(img, d, t, sc):
    pill(d, "ĐÁP ÁN: gần như bằng nhau", 260, appear(t, 0.15, 0.4))
    bench(d, 50, OX + (50 + 12.6) * S, True, rays=0.5, labels=False)
    def under(d):                                              # o f to nen xanh nhat khi tinh xong tung lan
        for i in range(5):
            kf = appear(t, DA_F + 0.6 * i, 0.4)
            if kf > 0:
                y = 850 + 144 + i * RH
                d.rounded_rectangle([TX[2] - 150, y - 36, TX[2] - 150 + 300 * kf, y + 36], radius=16, fill=(220, 252, 231))
    table(d, 5, 5, fa=lambda i: appear(t, DA_F + 0.6 * i + 0.2, 0.3), under=under)
    k2 = appear(t, DA_R, 0.5)
    if k2 > 0:
        for i in range(5):                                     # cot f to dam dan: nam so sat nhau
            y = 850 + 144 + i * RH; pw = 120 + 30 * math.sin(2.4 * (t - DA_R)) ** 2
            d.rounded_rectangle([TX[2] - pw, y - 34, TX[2] + pw, y + 34], radius=16, outline=A(GREEN, k2), width=5)
        card(d, (60, 1390, 1020, 1530), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=26, w=4)
        text(d, (W / 2, 1460), "Lần nào cũng gần 10 cm", FS, DGREEN, alpha=k2)


# ---------------- canh 4: Bay + chua noi duoc ----------------
BAY_R, BAY_E = 3.4, 6.6
WRONG = "(24 + 17,2) : 2 = 20,6"
RIGHT = "24 · 17,2 : 41,2 = 10,02"
def s_bay(img, d, t, sc):
    bench(d, 24, OX + (24 + 17.2) * S, True, rays=0.45, labels=False)
    a1 = appear(t, 0.3, 0.45)
    if a1 > 0:
        pill(d, "BẪY", 865, a1, color=DRED)
        text(d, (W / 2, 945), "Lần d = 24, d' = 17,2 (cm)", FM, INK, alpha=a1)
        card(d, (40, 990, 1040, 1160), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
        text(d, (90, 1040), "Lấy trung bình:", FM, DRED, anchor="lm", alpha=a1)
        text(d, (90, 1112), WRONG, FS, DRED, anchor="lm", alpha=a1)
        text(d, (970, 1075), "✗", 80, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (40, 1180, 1040, 1350), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (90, 1230), "d·d' : (d + d'):", FM, DGREEN, anchor="lm", alpha=a2)
        text(d, (90, 1302), RIGHT, FS, DGREEN, anchor="lm", alpha=a2)
        text(d, (970, 1265), "✓", 80, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (40, 1370, 1040, 1565), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1420), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1505), "số liệu minh hoạ; chưa xét ảnh ảo", FM, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 4.3
EY, EO, EL, EM, ES = 1250, 110, 0, 0, 9     # truc, vat x, ti le 9 px/cm
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Dịch vật: f tính ra không đổi", FM, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 630), "Thấu kính khác: ảnh rõ khi", FS, INK, alpha=k1)
    text(d, (W / 2, 712), f"d = {CH_D} cm, d' = {CH_DP} cm.", FS, INK, alpha=k1)
    if k1 > 0:   # hinh: vat - kinh - man voi hai doan d, d'; khong ve tia, khong ve F
        lx = EO + CH_D * ES; sx = lx + CH_DP * ES
        d.line([(70, EY), (1010, EY)], fill=A(NAVY, 0.6 * k1), width=3)
        arrow(d, (EO, EY), (EO, EY - 70), A(RED, k1), w=8, head=22)
        d.ellipse([lx - 20, EY - 140, lx + 20, EY + 140], fill=A(LBLUE, 0.8 * k1), outline=A(BLUE, k1), width=4)
        d.rounded_rectangle([sx - 8, EY - 160, sx + 8, EY + 160], radius=4, fill=A(WHITE, k1), outline=A(NAVY, k1), width=3)
        for x0, x1, s_ in ((EO, lx, f"{CH_D} cm"), (lx, sx, f"{CH_DP} cm")):
            y = EY + 190
            d.line([(x0, y), (x1, y)], fill=A(NAVY, k1), width=4)
            for x in (x0, x1): d.line([(x, y - 14), (x, y + 14)], fill=A(NAVY, k1), width=4)
            text(d, ((x0 + x1) / 2, y + 50), s_, FS, NAVY, alpha=k1)
        kq = 0.55 + 0.45 * math.sin(2.4 * t) ** 2
        text(d, (W / 2, 900), "f = ?", 84, ORANGE, alpha=k1 * kq)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T0 + i * STEP + ML + MS, "tap") for i in range(5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-thaukinh-03", header="KHTN 9 · THÍ NGHIỆM", footer="Thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo d và d' trên thước", draw=s_hook, tail=0.3, caps=[
   ("Vật sáng, thấu kính hội tụ, màn.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Kính f = 10 cm: dịch kính, rồi màn.", 5.0),
   ("Ảnh rõ nhất thì đọc d'.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Tính f cho từng lần đo.", 4.4),
   ("Năm giá trị f sát nhau.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("So hai cách tính.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 8.2)]),
])

_kiem()
