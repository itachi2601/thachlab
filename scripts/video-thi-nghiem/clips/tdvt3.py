# Clip: tn-l10-tdvt-03 - Ve but len dai giay dang bi keo: quy dao va van toc phu thuoc he quy chieu (31/10/2026; dung lai
#   27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu ve >= 56 px, khong chi so duoi (doi thanh chu: but/giay/vet),
#   Du doan khong nut A-D, THU NGHI khong the goi y; video dung SAU hop exp; bai co ca no 4-3-5 nen Bay chi nhac Pythagore).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-tdvt-03.json:
#   so_lieu_mau v_but / v_giay / v_vet (cm/s) / goc (do): 4/0/4,0/0,0 ; 4/3/5,0/36,9 ; 4/6/7,21/56,3.
#   tham_so: v_but 1-8, v_giay 0-8 cm/s (buoc 0,5). Danh so nhu bai: (1) but, (2) giay, (3) ban.
#   Nhin tu tren xuong: but di doc thuoc (v13, xanh la, net dut), vet muc xanh duong tren giay (v12), giay keo sang phai (v23).
#   Hinh ve dung ti le: but di 330 px trong mot lan, giay di 330*v23/4 px -> goc vet = arctan(v23/4).
# Canh: Du doan (hinh dang vet muc, K10: chi cau hoi + hinh) -> Tien hanh (3 lan keo: 0, 3, 6 cm/s; bang dien dung
#       luc but toi dau thuoc) -> Rut ra (hai quy dao + tam giac van toc 3-4-5) -> Chua noi duoc gi (keo khong deu)
#       -> Bay (4 + 3 = 7) -> Chot + cau hoi (giay 4 cm/s = but: goc 45 do, chua tung hien tren man).
from engine import *
DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (91, 33, 182); DORANGE = (176, 64, 8); DBLUE = (29, 78, 216)

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
    text(d, (880, PY0 + 75), "(2) giấy", 56, MUTED, alpha=alpha)
    text(d, (170, TY0 + 50), "(3) bàn", 56, NAVY, alpha=alpha)
    d.rectangle([RX - 52, TY0 + 50, RX - 6, TY1 - 30], fill=c(RULER), outline=c(RULER_D), width=3)   # thuoc co dinh
    for k in range(13):
        yy = TY0 + 80 + k * 40; L = 20 if k % 2 == 0 else 12
        d.line([(RX - 6 - L, yy), (RX - 6, yy)], fill=c(RULER_D), width=3)
    text(d, (RX + 90, TY0 + 50), "thước", 56, RULER_D, alpha=alpha)
    py = YB - SPAN * clamp(u)
    if trace and u > 0: d.line([(RX + sh, YB), (RX, py)], fill=c(INK_C), width=9)
    if path and u > 0: dashed(d, (RX, YB), (RX, py), c(GREEN), w=6)   # ve sau: lan 1 (giay yen) net dut van thay tren vet
    if arc and v23 > 0 and u >= 1:
        ang = math.degrees(math.atan2(SPAN, sh)); R = 95
        d.arc([RX - R, YT - R, RX + R, YT + R], start=ang, end=90, fill=c(PURPLE), width=6)
    d.ellipse([RX - 21, py - 21, RX + 21, py + 21], fill=c(NAVY))
    d.ellipse([RX - 9, py - 9, RX + 9, py + 9], fill=c(INK_C))
    arrow(d, (150, 800), (150, 720), c(GREEN), w=8, head=24)      # van toc but so voi ban
    text(d, (150, 600), "(1) bút", 56, GREEN, alpha=alpha)
    text(d, (150, 670), "4 cm/s", 56, GREEN, alpha=alpha)
    if v23 > 0:
        arrow(d, (600, 405), (790, 405), c(ORANGE), w=7, head=22)
        text(d, (900, 405), f"{v23} cm/s", 56, ORANGE, alpha=alpha)
    else:
        text(d, (720, 405), "giấy đứng yên", 56, ORANGE, alpha=alpha)


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-tdvt-03.json")))
    h = k["so_lieu_mau"]["hang"]
    assert [r[1] for r in h] == [r[0] for r in RUNS] and [r[2] for r in h] == [4.0, 5.0, 7.21] and [r[3] for r in h] == [0.0, 36.9, 56.3]
    assert abs(math.degrees(math.atan(4 / 4)) - 45) < 1e-9
_kiem_so()

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

def tri(d, O, s, k, labs=True):
    """Tam giac van toc lan 2: but 4 (xanh la, len), giay 3 (cam, ngang), vet 5 (xanh duong). Don vi cm/s."""
    Q = (O[0], O[1] - 4 * s); P = (O[0] - 3 * s, O[1] - 4 * s)
    arrow(d, O, P, A(INK_C, k), w=9, head=28)
    arrow(d, P, Q, A(ORANGE, k), w=9, head=28)
    arrow(d, O, Q, A(GREEN, k), w=9, head=28)
    if labs:
        text(d, (O[0] - 1.5 * s - 40, O[1] - 2 * s - 25), "bút/giấy", 56, DBLUE, anchor="rm", alpha=k)
        text(d, (O[0] - 1.5 * s - 40, O[1] - 2 * s + 45), "5 cm/s", 56, DBLUE, anchor="rm", alpha=k)
        text(d, (O[0] - 1.5 * s, Q[1] - 50), "giấy 3 cm/s", 56, DORANGE, alpha=k)
        text(d, (O[0] + 30, O[1] - 2 * s), "bút 4 cm/s", 56, DGREEN, anchor="lm", alpha=k)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    topview(d, 3, 0, alpha=appear(t, 0.1), trace=False)
    k = appear(t, M[1] - 0.3, 0.45)
    if k <= 0: return
    y0 = 920 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 310), "Vệt mực trên giấy", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 420), "có dạng thế nào?", 62, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 520 + 10 * math.sin(t * 3)), "?", 72, PURPLE, alpha=k)

# ---------------- canh 2: Tien hanh (3 lan keo) ----------------
R0, RGAP, DUR = 0.6, 3.0, 2.3
BADGE = 9.3
XS = (130, 380, 690, 920)

def run_u(i, t): return (t - (R0 + RGAP * i)) / DUR

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    cur = max(0, min(2, int((t - R0) // RGAP))) if t >= R0 else 0
    u = run_u(cur, t); v23 = RUNS[cur][0]
    topview(d, v23, u, path=True, arc=True)
    card(d, (60, 905, 1020, 1330), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, 960), "Bút so với bàn: 4 cm/s", 56, DGREEN)
    text(d, (XS[0], 1040), "Lần", 56, INK)
    text(d, (XS[1], 1040), "Giấy (cm/s)", 56, DORANGE)
    text(d, (XS[2], 1040), "Vệt (cm/s)", 56, DBLUE)
    text(d, (XS[3], 1040), "Góc", 56, INK)
    d.line([(90, 1078), (990, 1078)], fill=LIGHT, width=4)
    ka = appear(t, BADGE, 0.4)
    for i, (_, g, vv, gc) in enumerate(RUNS):
        ui = run_u(i, t)
        if ui < 0 and i > 0: continue
        yy = 1125 + i * 70
        if i == cur and ui < 1.25:
            d.rounded_rectangle([80, yy - 32, 1000, yy + 32], radius=14, fill=(239, 246, 255))
        text(d, (XS[0], yy), str(i + 1), 56, MUTED)
        text(d, (XS[1], yy), g, 56, NAVY)
        if ui >= 1.0:
            text(d, (XS[2], yy), vv, 56, DBLUE); text(d, (XS[3], yy), gc, 56, DBLUE)
    if ka > 0:
        s_ = "ĐÁP ÁN: xiên, ngược chiều kéo"; pw = tw(d, s_, F(56)) + 70
        card(d, (W / 2 - pw / 2, 1370, W / 2 + pw / 2, 1470), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1420), s_, 56, DGREEN, alpha=ka)

# ---------------- canh 3: Rut ra ----------------
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 260, 1020, 680), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    g = clamp((t - 0.3) / 1.6)
    dashed(d, (300, 590), (300, 590 - 190 * g), A(GREEN, a), w=8)
    d.line([(860, 590), (860 - 143 * g, 590 - 190 * g)], fill=A(INK_C, a), width=9)   # 36,9 do (lan 2)
    text(d, (300, 635), "so với bàn", 56, DGREEN, alpha=a)
    text(d, (790, 635), "so với giấy", 56, DBLUE, alpha=a)
    k = appear(t, M[1] - 0.05, 0.4)
    if k <= 0: return
    card(d, (60, 720, 1020, 1480), fill=A(WHITE, k), outline=A(NAVY, k), w=4)
    tri(d, (640, 1400), 120 * clamp((t - M[1]) / 1.0) + 0.01 if t < M[1] + 1.0 else 120, k)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35)
    card(d, (60, 260, 1020, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 350), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 470), "Kéo không đều?", 62, BLUE, alpha=k)
    n = int(40 * clamp((t % 3.0) / 2.4))                                     # vet ngoan ngoeo ve dan, lap lai
    pts = [(W / 2 - 300 + 600 * j / 40, 1050 - 300 * (j / 40) ** 0.6 + 50 * math.sin(j / 40 * 9)) for j in range(41)]
    if n >= 1: d.line(pts[:n + 1], fill=A(INK_C, k), width=9, joint="curve")
    text(d, (880, 700 + 16 * math.sin(t * 3)), "?", 80, PURPLE, alpha=k)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 260, 1020, 560), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    text(d, (W / 2, 345), "✗ Bút/giấy", 60, DRED, alpha=a)
    text(d, (W / 2, 465), "4 + 3 = 7 cm/s", 60, DRED, alpha=a)
    card(d, (60, 600, 1020, 1520), fill=A(WHITE, a), outline=A(GREEN if t >= M[1] - 0.05 else NAVY, a), w=5)
    if t < M[1] - 0.05:                                                     # hai mui ten noi thang hang: cach cong sai
        u = 100; X0 = 190; y = 900; pu = 0.6 + 0.4 * math.sin(t * 4)
        arrow(d, (X0, y), (X0 + 4 * u, y), A(GREEN, a), w=12, head=30)
        arrow(d, (X0 + 4 * u, y), (X0 + 7 * u, y), A(ORANGE, a), w=12, head=30)
        text(d, (X0 + 2 * u, y - 60), "bút 4", 56, DGREEN, alpha=a)
        text(d, (X0 + 5.5 * u, y - 60), "giấy 3", 56, DORANGE, alpha=a)
        d.rounded_rectangle([X0 - 20, y - 110, X0 + 7 * u + 20, y + 40], radius=20, outline=A(DRED, a * pu), width=6)
        return
    kb = appear(t, M[1] - 0.05, 0.35)
    text(d, (W / 2, 690), "✓ Vuông góc", 60, DGREEN, alpha=kb)
    tri(d, (640, 1440), 130, kb)

# ---------------- canh 6: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    d.rectangle([110, 470, 970, 820], fill=A((248, 250, 252), k1), outline=A(GRAY, k1), width=3)     # dai giay
    d.rectangle([440, 450, 480, 860], fill=A(RULER, k1), outline=A(RULER_D, k1), width=3)          # thuoc co dinh
    py = 800 - 290 * ((t * 0.45) % 1.0)
    d.ellipse([502 - 20, py - 20, 502 + 20, py + 20], fill=A(NAVY, k1))
    text(d, (580, py - 10 + 10 * math.sin(t * 3)), "?", 72, PURPLE, alpha=k1)
    arrow(d, (250, 760), (250, 560), A(GREEN, k1), w=9, head=28)
    text(d, (250, 860), "bút 4 cm/s", 56, DGREEN, alpha=k1)
    arrow(d, (690, 410), (900, 410), A(ORANGE, k1), w=9, head=28)
    text(d, (690, 410), "giấy 4 cm/s ", 56, DORANGE, anchor="rm", alpha=k1)
    text(d, (W / 2, 1080), "Vệt lệch khỏi thước", 60, INK, alpha=k1)
    text(d, (W / 2, 1170), "khoảng bao nhiêu độ?", 60, ORANGE, alpha=k1)
    cbar(d, 1300, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + BADGE, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1], "ding"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-tdvt-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Tốc độ và vận tốc · thachlab.id.vn", scenes=[
 dict(key="hook", title="Vẽ trên giấy đang kéo", draw=s_hook, tail=0.3, caps=[
   ("Bút và giấy cùng chạy đều.", 3.4),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Kéo giấy ba lần", draw=s_do, tail=0.3, caps=[
   ("Nét đứt: bút so với bàn.", 4.6),
   ("Vệt xanh: bút so với giấy.", 4.6),
   ("Giấy nhanh hơn, vệt nghiêng hơn.", 3.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Một ngòi bút, hai đường.", 3.6),
   ("Ba vận tốc thành tam giác.", 3.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Mới xét chuyển động đều.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Dễ tưởng: cộng thẳng.", 3.4),
   ("Dùng Pythagore.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.8)]),
])
