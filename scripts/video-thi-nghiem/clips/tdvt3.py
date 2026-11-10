# Clip: tn-l10-tdvt-03 - Ve but len dai giay dang bi keo: quy dao va van toc phu thuoc he quy chieu (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-tdvt-03.json:
#   so_lieu_mau v_but / v_giay / v_vet (cm/s) / goc (do): 4/0/4,0/0,0 ; 4/3/5,0/36,9 ; 4/6/7,21/56,3.
#   tham_so: v_but 1-8, v_giay 0-8 cm/s (buoc 0,5). Danh so nhu bai: (1) but, (2) giay, (3) ban.
#   Nhin tu tren xuong: but di doc thuoc (v13, xanh la, net dut), vet muc xanh duong tren giay (v12), giay keo sang phai (v23).
#   Hinh ve dung ti le: but di 330 px trong mot lan, giay di 330*v23/4 px -> goc vet = arctan(v23/4).
# Canh: Du doan (hinh dang vet muc, K10: chi cau hoi + hinh) -> Tien hanh (3 lan keo: 0, 3, 6 cm/s; bang dien dung
#       luc but toi dau thuoc) -> Rut ra (hai quy dao + tam giac van toc 3-4-5) -> Chua noi duoc gi (keo khong deu)
#       -> Bay (4 + 3 = 7) -> Chot + cau hoi (giay 4 cm/s = but: goc 45 do, chua tung hien tren man).
from engine import *

V13 = 4                                   # but so voi ban (cm/s)
RUNS = [(0, "0", "4,0", "0°"), (3, "3", "5,0", "36,9°"), (6, "6", "7,21", "56,3°")]   # so_lieu_mau
INK_C = BLUE                              # muc but da xanh = vet so voi giay (v12)
TBL = (222, 196, 160); TBL_D = (150, 110, 70)
RULER = (253, 230, 138); RULER_D = (161, 98, 7)

# ---------- hinh nhin tu tren xuong (toa do nguon) ----------
TX0, TY0, TX1, TY1 = 60, 260, 1020, 880   # mat ban
PY0, PY1 = 455, 830                       # dai giay
RX = 345                                  # duong ngoi but (mep phai thuoc)
YB, YT = 810, 480                         # ngoi but: dau -> cuoi (330 px)
SPAN = YB - YT
def shift(v23, u): return SPAN * v23 / V13 * clamp(u)   # giay da di (px) khi but di duoc phan u

def vsub(d, x, y, sub, size=46, col=INK, alpha=1.0, vec=False, anchor="m"):
    """Ve 'v' + chi so duoi >= 36 px (quy tac co chu); vec=True ve mui ten nho tren chu v. Tra ve be rong."""
    fv, fs = F(size), F(36); wv, ws = tw(d, "v", fv), tw(d, sub, fs); w = wv + ws + 2
    x0 = x - w / 2 if anchor == "m" else x
    dtext(d, (x0, y), "v", fv, col, alpha, "lm")
    dtext(d, (x0 + wv + 2, y + size * 0.3), sub, fs, col, alpha, "lm")
    if vec:
        ay = y - size * 0.55; c = A(col, alpha)
        d.line([(x0 + 2, ay), (x0 + wv + 4, ay)], fill=c, width=4)
        d.line([(x0 + wv + 4, ay), (x0 + wv - 6, ay - 7)], fill=c, width=4)
        d.line([(x0 + wv + 4, ay), (x0 + wv - 6, ay + 7)], fill=c, width=4)
    return w

def dashed(d, p1, p2, col, w=6, on=18, off=12):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    if L < 1: return
    ux, uy = (p2[0] - p1[0]) / L, (p2[1] - p1[1]) / L; s = 0
    while s < L:
        e = min(L, s + on)
        d.line([(p1[0] + ux * s, p1[1] + uy * s), (p1[0] + ux * e, p1[1] + uy * e)], fill=col, width=w); s += on + off

def topview(d, v23, u, alpha=1.0, path=False, trace=True, arc=False):
    """Mat ban + giay + thuoc + but. u: phan duong but da di (0..1). path: ve net dut but-so-voi-ban."""
    c = lambda col: A(col, alpha)
    card(d, (TX0, TY0, TX1, TY1), fill=c(TBL), outline=c(TBL_D), r=18, w=4)
    sh = shift(v23, u)
    d.rectangle([TX0 + 4, PY0, TX1 - 4, PY1], fill=c(WHITE))
    d.line([(TX0 + 4, PY0), (TX1 - 4, PY0)], fill=c(GRAY), width=3)
    d.line([(TX0 + 4, PY1), (TX1 - 4, PY1)], fill=c(GRAY), width=3)
    x = TX0 + 40 + (sh % 120)                                     # van giay chay theo giay (thay giay truot)
    while x < TX1 - 10:
        d.line([(x, PY0 + 14), (x, PY0 + 40)], fill=c(GRAY), width=6)
        d.line([(x, PY1 - 40), (x, PY1 - 14)], fill=c(GRAY), width=6); x += 120
    text(d, (920, PY0 + 70), "(2) giấy", 38, MUTED, alpha=alpha)
    text(d, (165, TY0 + 42), "(3) bàn", 38, NAVY, alpha=alpha)
    d.rectangle([RX - 52, TY0 + 50, RX - 6, TY1 - 30], fill=c(RULER), outline=c(RULER_D), width=3)   # thuoc co dinh
    for k in range(13):
        yy = TY0 + 80 + k * 40; L = 20 if k % 2 == 0 else 12
        d.line([(RX - 6 - L, yy), (RX - 6, yy)], fill=c(RULER_D), width=3)
    text(d, (RX - 29, TY0 + 30), "thước", 36, RULER_D, alpha=alpha)
    py = YB - SPAN * clamp(u)
    if trace and u > 0: d.line([(RX + sh, YB), (RX, py)], fill=c(INK_C), width=9)
    if path and u > 0: dashed(d, (RX, YB), (RX, py), c(GREEN), w=6)   # ve sau: lan 1 (giay yen) net dut van thay tren vet
    if arc and v23 > 0 and u >= 1:
        ang = math.degrees(math.atan2(SPAN, sh)); R = 95
        d.arc([RX - R, YT - R, RX + R, YT + R], start=ang, end=90, fill=c(PURPLE), width=6)
    d.ellipse([RX - 21, py - 21, RX + 21, py + 21], fill=c(NAVY))
    d.ellipse([RX - 9, py - 9, RX + 9, py + 9], fill=c(INK_C))
    arrow(d, (245, 700), (245, 560), c(GREEN), w=7, head=22)      # van toc but so voi ban
    text(d, (135, 610), "(1) bút", 38, GREEN, alpha=alpha)
    text(d, (135, 660), "4 cm/s", 38, GREEN, alpha=alpha)
    if v23 > 0:
        arrow(d, (600, 405), (790, 405), c(ORANGE), w=7, head=22)
        text(d, (900, 405), f"{v23} cm/s", 38, ORANGE, alpha=alpha)
    else:
        text(d, (720, 405), "giấy đứng yên", 38, ORANGE, alpha=alpha)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    topview(d, 3, 0, alpha=appear(t, 0.1), trace=False)
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 930 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 175, "Vệt mực để lại trên giấy", 46, INK, alpha=k)
    ctext(d, y0 + 240, "có dạng thế nào?", 46, INK, alpha=k)
    card(d, (W / 2 - 80, y0 + 300, W / 2 + 80, y0 + 450), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=26, w=4)
    text(d, (W / 2, y0 + 375), "?", 90, PURPLE, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 500, 880, y0 + 516], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 500, 200 + 680 * (1 - q), y0 + 516], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh (3 lan keo) ----------------
R0, RGAP, DUR = 0.6, 3.0, 2.3
BADGE = 9.3
XS = (140, 370, 640, 890)

def run_u(i, t):  # phan duong but da di o lan i luc t (giay trong canh); <0 = chua bat dau
    return (t - (R0 + RGAP * i)) / DUR

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    cur = max(0, min(2, int((t - R0) // RGAP))) if t >= R0 else 0
    u = run_u(cur, t); v23 = RUNS[cur][0]
    topview(d, v23, u, path=True, arc=True)
    card(d, (60, 905, 1020, 1250), fill=WHITE, outline=NAVY, w=4)
    w = vsub(d, 0, 0, "13", 42, alpha=0) + tw(d, "Bút so với bàn: ", F(40)) + tw(d, " = 4 cm/s", F(40))
    x0 = W / 2 - w / 2; text(d, (x0, 950), "Bút so với bàn: ", 40, GREEN, anchor="lm"); x0 += tw(d, "Bút so với bàn: ", F(40))
    x0 += vsub(d, x0, 950, "13", 42, GREEN, anchor="l"); text(d, (x0, 950), " = 4 cm/s", 40, GREEN, anchor="lm")
    text(d, (XS[0], 1020), "Lần", 38, INK)
    vsub(d, XS[1] - 60, 1020, "23", 42, ORANGE); text(d, (XS[1] + 40, 1020), "(cm/s)", 36, INK)
    vsub(d, XS[2] - 60, 1020, "12", 42, INK_C); text(d, (XS[2] + 40, 1020), "(cm/s)", 36, INK)
    text(d, (XS[3], 1020), "Góc lệch", 38, INK)
    d.line([(90, 1052), (990, 1052)], fill=LIGHT, width=4)
    ka = appear(t, BADGE, 0.4)
    for i, (_, g, vv, gc) in enumerate(RUNS):
        ui = run_u(i, t)
        if ui < 0: continue
        yy = 1095 + i * 60
        if i == cur and ui < 1.0 + 0.25:
            d.rounded_rectangle([80, yy - 28, 1000, yy + 28], radius=14, fill=(239, 246, 255))
        text(d, (XS[0], yy), str(i + 1), 40, MUTED)
        text(d, (XS[1], yy), g, 40, NAVY)
        if ui >= 1.0:
            text(d, (XS[2], yy), vv, 40, INK_C); text(d, (XS[3], yy), gc, 40, INK_C)
    if ka > 0:
        s_ = "ĐÁP ÁN · Xiên, ngược chiều kéo"; pw = tw(d, s_, F(44)) + 70
        card(d, (W / 2 - pw / 2, 1290, W / 2 + pw / 2, 1390), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=26, w=4)
        text(d, (W / 2, 1340), s_, 44, GREEN, alpha=ka)

# ---------------- canh 3: rut ra ----------------
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 270, 1020, 640), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (W / 2, 320), "Quỹ đạo của ngòi bút", 42, INK, alpha=a)
    dashed(d, (300, 550), (300, 370), A(GREEN, a), w=8)
    text(d, (300, 595), "so với bàn", 40, GREEN, alpha=a)
    d.line([(848, 550), (713, 370)], fill=A(INK_C, a), width=9)          # nghieng 36,9 do (lan 2)
    text(d, (780, 595), "so với giấy", 40, INK_C, alpha=a)
    k = appear(t, M[1] - 0.05, 0.4)
    if k <= 0: return
    card(d, (60, 680, 1020, 1480), fill=A(WHITE, k), outline=A(NAVY, k), w=4)
    text(d, (W / 2, 735), "Lần 2, đơn vị cm/s", 40, MUTED, alpha=k)
    s = 60; O = (600, 1230); Pt = (O[0] - 3 * s, O[1] - 4 * s); Q = (O[0], O[1] - 4 * s)
    arrow(d, O, Pt, A(INK_C, k), w=8, head=26)
    arrow(d, Pt, Q, A(ORANGE, k), w=8, head=26)
    arrow(d, O, Q, A(GREEN, k), w=8, head=26)
    x = 330; x += vsub(d, x, 1120, "12", 48, INK_C, k, anchor="l"); text(d, (x, 1120), " = 5", 46, INK_C, anchor="lm", alpha=k)
    x = 400; x += vsub(d, x, 935, "23", 48, ORANGE, k, anchor="l"); text(d, (x, 935), " = 3", 46, ORANGE, anchor="lm", alpha=k)
    x = 635; x += vsub(d, x, 1120, "13", 48, GREEN, k, anchor="l"); text(d, (x, 1120), " = 4", 46, GREEN, anchor="lm", alpha=k)
    ke = appear(t, M[1] + 0.8, 0.4)                                      # v13 = v12 + v23 (vecto)
    if ke > 0:
        f = F(52); parts = [("13", GREEN), (" = ", INK), ("12", INK_C), (" + ", INK), ("23", ORANGE)]
        ww = sum(tw(d, p, f) if len(p) > 2 or not p.isdigit() else vsub(d, 0, 0, p, 56, alpha=0) for p, _ in parts)
        x = W / 2 - ww / 2; y = 1380
        for p, col in parts:
            if p.isdigit(): x += vsub(d, x, y, p, 56, col, ke, vec=True, anchor="l")
            else: text(d, (x, y), p, 52, col, anchor="lm", alpha=ke); x += tw(d, p, f)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 1150), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 560), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 310, "Kéo không đều:", 50, BLUE, alpha=k)
    ctext(d, y1 + 420, "vệt còn thẳng?", 50, BLUE, alpha=k)
    pts = [(W / 2 - 260 + 520 * j / 40, y1 + 870 - 180 * (j / 40) ** 0.5 + 40 * math.sin(j / 40 * 7)) for j in range(41)]
    for j in range(0, 40, 2): d.line([pts[j], pts[j + 1]], fill=A(GRAY, k), width=7)
    text(d, (880, y1 + 640), "?", 80, PURPLE, alpha=k)
    ctext(d, y1 + 1050, "Số liệu từ mô hình, chưa đo", 42, INK, alpha=k)

# ---------------- canh 5: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 650), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    q = "Bút trên giấy: 4 + 3 = 7 cm/s"; f = F(52); lw = tw(d, q, f); yy = 500
    text(d, (W / 2, yy), q, 52, DRED, alpha=a)
    ks = clamp((t - 0.9) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=7)
    card(d, (60, 690, 1020, 1480), fill=WHITE, outline=GREEN, w=5)
    u = 100; X0 = 160
    text(d, (X0, 790), "Cộng thẳng", 40, DRED, anchor="lm")
    d.rounded_rectangle([X0, 830, X0 + 7 * u, 890], radius=12, fill=(254, 226, 226), outline=DRED, width=3)
    text(d, (X0 + 7 * u + 20, 860), "7", 46, DRED, anchor="lm")
    kb = appear(t, 1.3, 0.4)
    text(d, (X0, 980), "Đúng", 40, INK_C, anchor="lm", alpha=kb)
    d.rounded_rectangle([X0, 1020, X0 + 5 * u * kb + 1, 1080], radius=12, fill=A((219, 234, 254), kb), outline=A(INK_C, kb), width=3)
    text(d, (X0 + 5 * u + 20, 1050), "5", 46, INK_C, anchor="lm", alpha=kb)
    k2 = appear(t, M[1] - 0.05, 0.4)
    if k2 > 0:
        text(d, (W / 2, 1210), "4² + 3² = 5²", 60, INK, alpha=k2)

DRED = (185, 28, 28)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):
        ctext(d, 900, "Bút, giấy cùng 4 cm/s so với bàn.\nVệt lệch mấy độ\nso với thước?", 50, INK,
              maxw=880, alpha=appear(t, sc["M"][0] + 0.4, 0.5))
        kh = appear(t, sc["M"][0] + 6.0, 0.5)
        if kh <= 0: return
        card(d, (110, 1230, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1380, "Nhớ tam giác vận tốc", 48, (154, 52, 18), maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Chuyển động có tính tương đối", "", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + BADGE, "ding"), (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-tdvt-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Tốc độ và vận tốc · thachlab.id.vn", scenes=[
 dict(key="hook", title="Vẽ trên giấy đang kéo", draw=s_hook, tail=0.5, caps=[
   ("Bút và giấy cùng chạy đều.", 3.4),
   ("Dừng video, tự đoán.", 4.9)]),
 dict(key="do", title="Kéo giấy ba lần", draw=s_do, tail=0.3, caps=[
   ("Nét đứt xanh lá: bút so với bàn.", 4.2),
   ("Vệt xanh dương: bút so với giấy.", 4.2),
   ("Giấy càng nhanh, vệt càng nghiêng.", 3.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Một ngòi bút, hai quỹ đạo.", 3.2),
   ("Vận tốc khép kín tam giác.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Chỉ xét chuyển động đều.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Chỉ cộng thẳng khi cùng chiều.", 3.0),
   ("Vuông góc: dùng Pythagore.", 2.9)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 7.2)]),
])
