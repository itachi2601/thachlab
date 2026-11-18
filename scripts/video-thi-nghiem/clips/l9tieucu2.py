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
from engine import *

AX, LXF, S, HP = 500, 580, 13, 90           # truc chinh, thau kinh co dinh, px/cm, chieu cao vat (px)
F_CM = 10.0; FP = F_CM * S
RAIL = 790; LH = 150
ROWS = [(15.0, 30.4, 10.0), (20.0, 19.7, 9.9), (25.0, 16.9, 10.1), (30.0, 14.6, 9.8), (40.0, 13.6, 10.1)]
F_TB = 9.98
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253)


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
    dot(d, LXF + FP, AX, 7, NAVY); text(d, (LXF + FP, AX - 42), "F'", 40, NAVY)
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
        text(d, (ox + 8, AX - HP - 40), "vật", 40, RED, anchor="lm")
        text(d, (LXF, AX - LH - 38), "thấu kính", 40, BLUE)
        text(d, (sx, AX - 168), "màn", 40, NAVY)
    return ox


TX = (250, 540, 830)
def table(d, n_rows, n_f, hl=-1, y0=850, a=1.0, fa=None):
    card(d, (60, y0, 1020, y0 + 110 + max(1, n_rows) * 74), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for x, h in zip(TX, ("d (cm)", "d' (cm)", "f (cm)")):
        text(d, (x, y0 + 56), h, 42, MUTED, alpha=a)
    d.line([(90, y0 + 100), (990, y0 + 100)], fill=A(LIGHT, a), width=3)
    for i, (dd, dp, ff) in enumerate(ROWS):
        y = y0 + 138 + i * 74
        if i == hl: d.rounded_rectangle([80, y - 33, 1000, y + 33], radius=14, fill=A((254, 243, 199), a))
        if i < n_rows:
            text(d, (TX[0], y), vn(dd), 44, INK, alpha=a)
            text(d, (TX[1], y), vn(dp), 44, INK, alpha=a)
        if i < n_f:
            text(d, (TX[2], y), vn(ff), 44, DGREEN, alpha=a * (1 if fa is None else fa(i)))
    return y0 + 120 + 5 * 74


# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    dd, dp, _ = ROWS[0]
    bench(d, dd, LXF + dp * S, True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 870 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 270, "Dịch vật ra xa thấu kính\n(15 cm → 40 cm). Muốn ảnh\nnét lại, màn phải dịch sao?",
          50, INK, maxw=930, alpha=a)
    text(d, (W / 2, y0 + 500), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 578, 940, y0 + 590], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 578, 140 + 800 * (1 - p), y0 + 590], radius=6, fill=A(PURPLE, a))


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
    table(d, st["rows"], 0, hl=st["rows"] - 1 if st["sharp"] and st["rows"] else -1, a=appear(t, 0.2, 0.4))


# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · màn dịch lại gần"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 226, W / 2 + pw / 2, 292), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 259), lab, 42, WHITE, alpha=ka)
    dd, dp, _ = ROWS[-1]
    bench(d, dd, LXF + dp * S, True, rays=0.5, labels=False)
    f0 = M[0] + 0.2
    yb = table(d, 5, 5, fa=lambda i: appear(t, f0 + 0.35 * i, 0.35))
    k2 = appear(t, M[1] + 0.2, 0.4)
    if k2 > 0:
        card(d, (60, yb + 24, 1020, yb + 214), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=22, w=3)
        text(d, (W / 2, yb + 84), "f trung bình = " + vn(F_TB, 2) + " cm", 46, DGREEN, alpha=k2)
        text(d, (W / 2, yb + 156), "làm tròn: 10,0 cm", 44, INK, alpha=k2)


# ---------------- canh 4: Bay roi Chua noi duoc ----------------
D_TB = sum(r[0] for r in ROWS) / 5; DP_TB = sum(r[1] for r in ROWS) / 5; F_SAI = D_TB * DP_TB / (D_TB + DP_TB)


def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    dd, dp, _ = ROWS[-1]
    bench(d, dd, LXF + dp * S, True, rays=0.4, labels=False)
    if a1 > 0:
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, M[0] + 2.3, 0.5)
        y0 = 860
        card(d, (40, y0, 1040, lerp(y0 + 370, y0 + 580, k4 / max(a1, 1e-3))), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        l1 = "Trung bình: d = " + vn(D_TB) + "; d' = " + vn(DP_TB, 2)
        l2 = "f = " + vn(D_TB) + " · " + vn(DP_TB, 2) + " : " + vn(D_TB + DP_TB, 2) + " = " + vn(F_SAI)
        text(d, (W / 2, y0 + 160), l1, 42, MUTED, alpha=k3)
        text(d, (450, y0 + 240), l2, 44, DRED, alpha=k3)
        if k3 > 0:
            hw = tw(d, l2, F(44)) / 2 + 8; d.line([(450 - hw, y0 + 242), (450 + hw, y0 + 242)], fill=A(DRED, k3), width=5)
        text(d, (930, y0 + 240), "✗", 100, DRED, alpha=k3)
        text(d, (W / 2, y0 + 320), "tính f từ d, d' trung bình", 42, DRED, alpha=k3)
        text(d, (450, y0 + 440), "trung bình 5 giá trị f", 46, DGREEN, alpha=k4)
        text(d, (450, y0 + 512), "= 10,0 cm", 46, DGREEN, alpha=k4)
        text(d, (910, y0 + 470), "✓", 100, DGREEN, alpha=k4)
    if k2 > 0:
        y0 = 950 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ", "• Chưa tính sai số của f")):
            kk = k2 * appear(t, M[1] + 0.1 + 0.3 * j, 0.4)
            text(d, (90, y0 + 165 + j * 95), l1, 44, INK, anchor="lm", alpha=kk)


# ---------------- canh 5: Chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    """THU NGHI: thau kinh khac, (18; 36) va (36; 18) cm -> f = 12 cm (bay: 13,5). Goi y tre 2,6 s, trung tinh."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 490, 1020, 790), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 640, "Tính f từng lần,\nrồi lấy trung bình các f", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 0.9 + 2.6, 0.5)
    card(d, (40, 850, 1040, lerp(1340, 1610, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 880, W / 2 + pw / 2, 944), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 912), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 1130, "Thấu kính khác, đo hai lần:\nd = 18, d' = 36 (cm) rồi\nd = 36, d' = 18 (cm).\nf trung bình là bao nhiêu?",
          48, INK, maxw=930, alpha=appear(t, M[0] + 0.9, 0.5))
    if kh > 0:
        card(d, (110, 1340, 970, 1580), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1395, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1495, "Nhìn lại bảng vừa rồi", 46, ORANGE, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + T1, "tick")] + [(do["t0"] + T1 + 0.4 + (i - 1) * STEP + MV + MS, "tick") for i in range(1, 5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.5, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out


CLIP = dict(id="tn-l9-tieucu-02", header="KHTN 9 · THÍ NGHIỆM", footer="Đo tiêu cự thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đổi vị trí vật 5 lần", draw=s_hook, tail=0.8, caps=[
   ("Ảnh nét trên màn khi d = 15 cm.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Dịch vật xa dần, tìm lại ảnh nét.", 5.0),
   ("Đọc d' tới 1 mm.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Mỗi lần tính f = d·d' : (d + d').", 3.8),
   ("Năm f hơi khác nhau.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Lấy trung bình d, d' trước?", 3.8),
   ("Chưa nói được điều gì?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.3, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])
