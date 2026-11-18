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
from engine import *

AX, OX, S, HP = 500, 70, 14, 50             # truc chinh, vat, px/cm, chieu cao vat (px)
F_CM = 10.0; FP = F_CM * S
RAIL = 800; LH = 150
ROWS = [(12, 57.0, 9.91), (16, 26.9, 10.03), (24, 17.2, 10.02), (36, 13.8, 9.98), (50, 12.6, 10.06)]
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253)


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
    dot(d, lx + FP, AX, 7, NAVY); text(d, (lx + FP, AX - 42), "F'", 40, NAVY)
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
        text(d, (OX + 8, AX - HP - 40), "vật", 40, RED, anchor="lm")
        text(d, (lx, AX - LH - 38), "thấu kính", 40, BLUE)
        if sx - lx >= 220: text(d, (sx, AX - 168), "màn", 40, NAVY)
    return lx


TX = (250, 540, 830)                        # cot bang: d, d' doc, f tinh ra
def table(d, n_rows, n_f, hl=-1, y0=860, a=1.0, fa=None):
    card(d, (60, y0, 1020, y0 + 112 + max(1, n_rows) * 76), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for x, h in zip(TX, ("d (cm)", "d' (cm)", "f (cm)")):
        text(d, (x, y0 + 56), h, 42, MUTED, alpha=a)
    d.line([(90, y0 + 100), (990, y0 + 100)], fill=A(LIGHT, a), width=3)
    for i, (dd, dp, ff) in enumerate(ROWS):
        y = y0 + 140 + i * 76
        if i == hl: d.rounded_rectangle([80, y - 34, 1000, y + 34], radius=14, fill=A((254, 243, 199), a))
        if i < n_rows:
            text(d, (TX[0], y), str(dd), 44, INK, alpha=a)
            text(d, (TX[1], y), vn(dp), 44, INK, alpha=a)
        if i < n_f:
            text(d, (TX[2], y), vn(ff, 2), 44, DGREEN, alpha=a * (1 if fa is None else fa(i)))


# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bench(d, 20, 980, False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 270, "Đặt vật ở 5 chỗ. Mỗi lần\nảnh rõ, tính d·d' : (d + d').\nNăm kết quả sẽ thế nào?",
          50, INK, maxw=930, alpha=a)
    text(d, (W / 2, y0 + 500), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 578, 940, y0 + 590], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 578, 140 + 800 * (1 - p), y0 + 590], radius=6, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
T0, STEP, ML, MS = 0.6, 1.95, 0.6, 0.7      # bat dau, moi lan, dich kinh, dich man
D_HOOK, SX_HOOK = 20.0, 980.0


def do_state(t):
    """mot ham cho thau kinh, man, anh ro, so hang bang (dong bo)"""
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
    table(d, st["rows"], 0, hl=st["rows"] - 1 if st["sharp"] else -1, a=appear(t, 0.2, 0.4))


# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · gần như bằng nhau"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 226, W / 2 + pw / 2, 292), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 259), lab, 42, WHITE, alpha=ka)
    bench(d, 50, OX + (50 + 12.6) * S, True, rays=0.5, labels=False)
    f0 = M[0] + 0.2
    table(d, 5, 5, fa=lambda i: appear(t, f0 + 0.35 * i, 0.35))
    k2 = appear(t, M[1] + 0.2, 0.4)
    if k2 > 0:
        card(d, (60, 1380, 1020, 1580), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=22, w=3)
        text(d, (W / 2, 1440), "Lần nào cũng ra gần 10 cm", 46, DGREEN, alpha=k2)
        text(d, (W / 2, 1515), "1/f = 1/d + 1/d' đúng khi dịch vật", 42, INK, alpha=k2)


# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    bench(d, 24, OX + (24 + 17.2) * S, True, rays=0.45)
    if a1 > 0:
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, M[0] + 2.3, 0.5)
        y0 = 870
        card(d, (40, y0, 1040, lerp(y0 + 380, y0 + 580, k4 / max(a1, 1e-3))), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        text(d, (W / 2, y0 + 150), "Lần d = 24 cm, d' = 17,2 cm", 42, MUTED, alpha=a1)
        text(d, (470, y0 + 250), "f = (24 + 17,2) : 2 = 20,6", 48, DRED, alpha=k3)
        if k3 > 0:
            hw = tw(d, "f = (24 + 17,2) : 2 = 20,6", F(48)) / 2 + 8
            d.line([(470 - hw, y0 + 252), (470 + hw, y0 + 252)], fill=A(DRED, k3), width=6)
        text(d, (900, y0 + 250), "✗", 100, DRED, alpha=k3)
        text(d, (W / 2, y0 + 330), "trung bình d và d' không phải f", 42, DRED, alpha=k3)
        text(d, (470, y0 + 440), "f = 24 · 17,2 : 41,2 = 10,02", 48, DGREEN, alpha=k4)
        text(d, (900, y0 + 440), "✓", 100, DGREEN, alpha=k4)
        text(d, (W / 2, y0 + 525), "đúng công thức d·d' : (d + d')", 42, DGREEN, alpha=k4)
    if k2 > 0:
        y0 = 950 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ, chưa đo thật", "• Chưa thử ảnh ảo, vật trong f")):
            kk = k2 * appear(t, M[1] + 0.1 + 0.3 * j, 0.4)
            text(d, (90, y0 + 165 + j * 95), l1, 44, INK, anchor="lm", alpha=kk)


# ---------------- canh 5: Chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    """THU NGHI: thau kinh khac, d = 30 cm, d' = 60 cm -> f = 20 cm (bay: 45 cm). Goi y tre 2,6 s, trung tinh."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 490, 1020, 790), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 640, "Dịch vật: d, d' đổi,\nf tính ra không đổi", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 0.9 + 2.6, 0.5)
    card(d, (40, 850, 1040, lerp(1240, 1510, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 880, W / 2 + pw / 2, 944), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 912), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 1100, "Thấu kính khác: vật cách\n30 cm, ảnh rõ cách 60 cm.\nTiêu cự f = ?", 48, INK,
          maxw=920, alpha=appear(t, M[0] + 0.9, 0.5))
    if kh > 0:
        card(d, (110, 1260, 970, 1480), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1315, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1410, "Nhớ lại bảng số đo", 46, ORANGE, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + T0 + i * STEP + ML + MS, "tick") for i in range(5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.5, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out


CLIP = dict(id="tn-l9-thaukinh-03", header="KHTN 9 · THÍ NGHIỆM", footer="Thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo d và d' trên thước", draw=s_hook, tail=0.8, caps=[
   ("Vật sáng, thấu kính hội tụ, màn.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Kính f = 10 cm: dịch kính, rồi màn.", 5.0),
   ("Ảnh rõ nhất thì đọc d'.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Tính f cho từng lần đo.", 3.8),
   ("Năm giá trị f sát nhau.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Lấy trung bình d và d'?", 3.8),
   ("Chưa nói được điều gì?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.3, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])
