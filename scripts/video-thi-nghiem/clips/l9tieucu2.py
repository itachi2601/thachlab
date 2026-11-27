# Clip: tn-l9-tieucu-02 - Cach 2: do d, d' o 5 vi tri vat, tinh f trung binh (KHTN 9, lo 5, 18/11/2026)
# So lieu tu content/thi-nghiem/tn-l9-tieucu-02.json (so_lieu_mau):
#   d = 15,0 ; 20,0 ; 25,0 ; 30,0 ; 40,0 cm -> d' = 30,4 ; 19,7 ; 16,9 ; 14,6 ; 13,6 cm -> f = 10,0 ; 9,9 ; 10,1 ; 9,8 ; 10,1 cm
#   rut_ra: f trung binh = 9,98 cm, lam tron 10,0 cm. tham_so f that 10,0 cm.
# Bay (them vao hien_tuong_hay_sai cua kho 18/11): lay trung binh d (26,0) va d' (19,04) roi moi tinh f:
#   26,0.19,04/45,04 = 10,99 -> 11,0 cm (sai) ; dung: trung binh 5 gia tri f = 10,0 cm.
# Hinh: thau kinh co dinh, vat dich ra xa (sang trai), man dich theo toi d' doc (13 px/cm, f = 130 px).
#   Tia song song -> F', tia qua O di thang, anh that nguoc chieu k = d'/d; man o d' doc lech <= 0,4 cm (vet loe <= 2 px).
# Khong tra loi san: Cau 2 ngay sau hop (lan nao lech xa f trung binh nhat) -> clip khong tinh do lech, khong to lan d = 30;
#   Cau 4 (do toi mep gia), Cau 5 (trung diem khoang net), Cau 6 (do mot lan) -> khong dung lam bay.
#   Khac tieucu-03 (anh bang vat, f = L/4): khong noi toi L, 2f.
# THU NGHI: thau kinh khac, (d = 18, d' = 36) va (d = 36, d' = 18) cm -> f = 12 cm moi lan, f tb = 12 cm (bay: 13,5 cm).
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom D): chu >= 55 (ra >= 48 px), K10, thanh dem 70 px, Bay hai hang
#   (11,0 ✗ / 10,0 ✓) moi nhip >= 3 s, man chot KHONG goi y. Du doan + chot giu nhu cu.
from engine import *

AX, LXF, S, HP = 500, 580, 13, 90           # truc chinh, thau kinh co dinh, px/cm, chieu cao vat (px)
F_CM = 10.0; FP = F_CM * S
RAIL = 790; LH = 150
ROWS = [(15.0, 30.4, 10.0), (20.0, 19.7, 9.9), (25.0, 16.9, 10.1), (30.0, 14.6, 9.8), (40.0, 13.6, 10.1)]
F_TB = 9.98
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253)
FS, FM = 58, 56
CH = [(18, 36), (36, 18)]                    # ca chot (kho ghi_chu): f = 12 cm moi lan


def _kiem():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-tieucu-02.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS
    for dd, dp, ff in ROWS: assert abs(dd * dp / (dd + dp) - ff) < 0.051
    assert abs(sum(r[2] for r in ROWS) / 5 - F_TB) < 1e-9 and "f = 648/54 = 12 cm" in k["so_lieu_mau"]["ghi_chu"]
    assert all(a * b / (a + b) == 12 for a, b in CH)


def vn(x, n=1):
    return f"{x:.{n}f}".replace(".", ",")


def dtrue(dd): return dd * F_CM / (dd - F_CM)


def chev(d, p, q, col, s=16, w=4):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def lens(d):
    lx = LXF; pts = []
    for j in range(41):
        y = -LH + 2 * LH * j / 40; pts.append((lx + 3 + 14 * (1 - (y / LH) ** 2), AX + y))
    for j in range(41):
        y = LH - 2 * LH * j / 40; pts.append((lx - 3 - 14 * (1 - (y / LH) ** 2), AX + y))
    d.polygon(pts, fill=A(LBLUE, 0.75), outline=BLUE)


def bench(d, d_cm, sx, sharp, rays=1.0, labels=True):
    """thau kinh co dinh o LXF, vat cach d_cm ve ben trai, man o sx; sharp -> tia + anh tai man"""
    ox = LXF - d_cm * S
    d.rounded_rectangle([20, RAIL - 8, 1060, RAIL + 8], radius=8, fill=(205, 198, 186))
    for j in range(-40, 41, 10):
        x = LXF + j * S; d.line([(x, RAIL - 8), (x, RAIL + 8)], fill=NAVY, width=3)
    for x, y0 in ((ox, AX + 6), (LXF, AX + LH), (sx, AX + 222)):
        d.rectangle([x - 5, y0, x + 5, RAIL - 8], fill=GRAY)
    d.line([(20, AX), (1060, AX)], fill=A(NAVY, 0.6), width=3)
    d.rounded_rectangle([sx - 9, AX - 130, sx + 9, AX + 222], radius=4, fill=WHITE, outline=NAVY, width=3)
    lens(d)
    dot(d, LXF + FP, AX, 7, NAVY); text(d, (LXF + FP, AX - 44), "F'", FM, NAVY)
    arrow(d, (ox, AX), (ox, AX - HP), RED, w=8, head=22)
    if sharp and rays > 0:
        dp = dtrue(d_cm) * S; k = dp / (d_cm * S)
        B, P, Bt = (ox, AX - HP), (LXF, AX - HP), (LXF + dp, AX + k * HP)
        def at(p, q, x): return (x, p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0]))
        c = A(ORANGE, 0.9 * rays)
        d.line([B, P], fill=c, width=4); chev(d, B, P, c)
        q1 = at(P, Bt, sx); d.line([P, q1], fill=c, width=4); chev(d, P, (LXF + FP, AX), c)
        q2 = at(B, Bt, sx); d.line([B, q2], fill=c, width=4); chev(d, B, (LXF, AX), c)
        arrow(d, (sx, AX), (sx, (q1[1] + q2[1]) / 2), BLUE, w=8, head=22)
    if labels:
        text(d, (ox + 8, AX - HP - 44), "vật", FM, RED, anchor="lm")
        text(d, (LXF, AX - LH - 42), "thấu kính", FM, BLUE)
        text(d, (min(sx, 1000), AX - 172), "màn", FM, NAVY)
    return ox


TX = (250, 540, 830)
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
            text(d, (TX[0], y), vn(dd), FS, INK, alpha=a)
            text(d, (TX[1], y), vn(dp), FS, INK, alpha=a)
        if i < n_f:
            text(d, (TX[2], y), vn(ff), FS, DGREEN, alpha=a * (1 if fa is None else fa(i)))


def pill(d, s, y, a, color=NAVY, size=FM):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    dd, dp, _ = ROWS[0]
    bench(d, dd, LXF + dp * S, True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 870 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(NAVY, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(NAVY, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    for j, s_ in enumerate(("Dịch vật ra xa: 15 → 40 cm.", "Muốn ảnh nét lại,", "màn phải dịch thế nào?")):
        text(d, (W / 2, y0 + 170 + j * 82), s_, 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 520, 970, y0 + 590], radius=35, fill=A((226, 232, 240), a))
        if p < 1: d.rounded_rectangle([110, y0 + 520, 110 + max(70, 860 * (1 - p)), y0 + 590], radius=35, fill=A(NAVY, a))


# ---------------- canh 2: Tien hanh ----------------
T1, STEP, MV, MS = 0.9, 1.95, 0.6, 0.7      # hang 1 hien o T1; moi lan sau: dich vat MV, dich man MS


def do_state(t):
    """vat, man, anh ro, so hang (dong bo): hang i chi hien khi vat o d_i va man o d'_i"""
    dcm, sx = ROWS[0][0], LXF + ROWS[0][1] * S
    rows = 1 if t >= T1 else 0
    for i in range(1, 5):
        ti = T1 + 0.4 + (i - 1) * STEP
        if t < ti: break
        dd, dp, _ = ROWS[i]
        dcm = lerp(ROWS[i - 1][0], dd, ease((t - ti) / MV))
        sx = lerp(LXF + ROWS[i - 1][1] * S, LXF + dp * S, ease((t - ti - MV) / MS))
        if t >= ti + MV + MS: rows = i + 1
    r = ROWS[max(rows, 1) - 1]
    sharp = abs(dcm - r[0]) < 1e-6 and abs(sx - (LXF + r[1] * S)) < 1e-6
    return dict(d=dcm, sx=sx, rows=rows, sharp=sharp)


def s_do(img, d, t, sc):
    st = do_state(t)
    bench(d, st["d"], st["sx"], st["sharp"])
    table(d, st["rows"], 0, hl=st["rows"] - 1 if st["sharp"] and st["rows"] else -1)


# ---------------- canh 3: Dap an + rut ra ----------------
DA_F, DA_R = 1.0, 5.4
def s_dapan(img, d, t, sc):
    pill(d, "ĐÁP ÁN: màn dịch lại gần", 260, appear(t, 0.15, 0.4))
    dd, dp, _ = ROWS[-1]
    bench(d, dd, LXF + dp * S, True, rays=0.5, labels=False)
    def under(d):                                              # o f to nen xanh nhat khi tinh xong tung lan
        for i in range(5):
            kf = appear(t, DA_F + 0.6 * i, 0.4)
            if kf > 0:
                y = 850 + 144 + i * RH
                d.rounded_rectangle([80, y - 36, 80 + 920 * kf, y + 36], radius=16, fill=(187, 247, 208))
    table(d, 5, 5, fa=lambda i: appear(t, DA_F + 0.6 * i + 0.2, 0.3), under=under)
    k2 = appear(t, DA_R, 0.5)
    if k2 > 0:
        pw = 110 + 25 * math.sin(2.4 * (t - DA_R)) ** 2          # khung cot f nhap nhay: lay trung binh ca cot
        d.rounded_rectangle([TX[2] - pw, 850 + 100, TX[2] + pw, 850 + 112 + 5 * RH - 6], radius=20, outline=A(GREEN, k2), width=6)
        card(d, (60, 1390, 1020, 1530), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=26, w=4)
        text(d, (W / 2, 1460), "f trung bình = 9,98 ≈ 10,0 cm", FS, DGREEN, alpha=k2)


# ---------------- canh 4: Bay + chua noi duoc ----------------
D_TB = sum(r[0] for r in ROWS) / 5; DP_TB = sum(r[1] for r in ROWS) / 5; F_SAI = D_TB * DP_TB / (D_TB + DP_TB)
BAY_R, BAY_E = 3.4, 6.6
def s_bay(img, d, t, sc):
    dd, dp, _ = ROWS[-1]
    bench(d, dd, LXF + dp * S, True, rays=0.4, labels=False)
    a1 = appear(t, 0.3, 0.45)
    if a1 > 0:
        pill(d, "BẪY", 880, a1, color=DRED)
        card(d, (40, 940, 1040, 1140), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
        text(d, (90, 992), "Trung bình d, d' rồi tính:", FM, DRED, anchor="lm", alpha=a1)
        l2 = vn(D_TB) + " · " + vn(DP_TB, 2) + " : " + vn(D_TB + DP_TB, 2) + " = " + vn(F_SAI)
        text(d, (90, 1080), l2, FS, DRED, anchor="lm", alpha=a1)
        text(d, (980, 1040), "✗", 80, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (40, 1160, 1040, 1350), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (90, 1212), "Trung bình 5 giá trị f:", FM, DGREEN, anchor="lm", alpha=a2)
        text(d, (90, 1295), "= 10,0 cm", FS, DGREEN, anchor="lm", alpha=a2)
        text(d, (980, 1255), "✓", 80, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (40, 1370, 1040, 1565), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1420), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1505), "số liệu minh hoạ; sai số của f", FM, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 4.3
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Lấy trung bình các giá trị f", FM, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 630), "Thấu kính khác, đo hai lần.", FS, INK, alpha=k1)
    text(d, (W / 2, 712), "f trung bình bằng bao nhiêu?", FS, INK, alpha=k1)
    if k1 > 0:   # bang hai lan do, cot f de trong
        y0 = 830
        card(d, (110, y0, 970, y0 + 340), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        for x, h in zip((300, 540, 780), ("d (cm)", "d' (cm)", "f (cm)")):
            text(d, (x, y0 + 56), h, FM, NAVY, alpha=k1)
        d.line([(140, y0 + 100), (940, y0 + 100)], fill=A(LIGHT, k1), width=3)
        kq = 0.55 + 0.45 * math.sin(2.4 * t) ** 2
        for j, (a_, b_) in enumerate(CH):
            y = y0 + 160 + j * 100
            text(d, (300, y), str(a_), FS, INK, alpha=k1); text(d, (540, y), str(b_), FS, INK, alpha=k1)
            text(d, (780, y), "?", FS, ORANGE, alpha=k1 * kq)
        text(d, (W / 2, 1360), "?", 150, ORANGE, alpha=k1 * kq)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T1, "tap")] + [(do["t0"] + T1 + 0.4 + (i - 1) * STEP + MV + MS, "tap") for i in range(1, 5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-tieucu-02", header="KHTN 9 · THÍ NGHIỆM", footer="Đo tiêu cự thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đổi vị trí vật 5 lần", draw=s_hook, tail=0.3, caps=[
   ("Ảnh nét trên màn khi d = 15 cm.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Dịch vật xa dần, tìm lại ảnh nét.", 5.0),
   ("Đọc d' tới 1 mm.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Mỗi lần tính một giá trị f.", 4.4),
   ("Năm f hơi khác nhau.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("So hai cách lấy trung bình.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 8.2)]),
])

_kiem()
