# Clip: tn-l12-thuchanh-03 - Pheu nuoc da + day dien tro, hai giai doan (doi chung moi truong) - de TN THPT 2025 cau II.1
# Ban 1 (12/11/2026). Ban 2 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2,5 s), <= 50 s, K10 (khong nut A-D, khong dong "Chon dap an o khung cau hoi").
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanh-03.json (_kiem_so() doi chieu so_lieu_mau, tham_so, ghi_chu):
#   U = 12 V, I = 3,0 A, tau = 300 s moi giai doan; m1 = 5,0 g (chua cap dien), m2 = 36,4 g (cap dien).
#   UI.tau = 10 800 J; m2 - m1 = 31,4 g; lambda = UI.tau/(m2 - m1) ~ 3,44.10^5 J/kg (lon hon that 3%: chi 97% nhiet day vao da);
#   chia cho m2: ~ 2,97.10^5 J/kg (nho hon that 11%); lambda that 3,34.10^5 J/kg.
# Quan niem sai can danh (hien_tuong_hay_sai[1]): chua cap dien thi "khong co gi xay ra".
# Du doan: giai doan 1 chua cap dien, 300 s, coc hung duoc bao nhieu? -> it hon nhieu nhung khac 0 (5,0 g).
# Thu tu: Du doan -> Tien hanh (2 giai doan) -> Ket qua (cot giai doan 2 tach moi truong + do day, tinh lambda)
#   -> Bay quen tru m1 (2,97) + nhiet day lam am pheu (3,44 > 3,34) -> Chot + THU NGHI.
# Thu nghi (= cau_chot khung web): phong am dan trong giai doan 2 -> moi truong lam tan nhieu hon m1 -> m2 - m1 lon hon
#   phan do day -> lambda tinh ra NHO hon (sai_so_thuong_gap 4). Dap so khong hien o canh chot.
from engine import *

U, I, TAU, M1, M2 = 12, 3.0, 300, 5.0, 36.4
LAM, LAM_TRU, LAM_M2 = 3.34, 3.44, 2.97          # x10^5 J/kg

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-thuchanh-03.json")))
    h = k["so_lieu_mau"]["hang"]
    assert h[0][2] == TAU and h[0][3] == M1 and h[1][2] == TAU and h[1][3] == M2, h
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["U"]["mac_dinh"] == U and ts["I"]["mac_dinh"] == I and ts["lambda_that"]["gia_tri"] == LAM * 1e5
    assert abs(U * I * TAU - 10800) < 1e-6
    assert round(U * I * TAU / ((M2 - M1) / 1000) / 1e5, 2) == LAM_TRU
    assert round(U * I * TAU / (M2 / 1000) / 1e5, 2) == LAM_M2
    assert round((LAM - LAM_M2) / LAM * 100) == 11 and round((LAM_TRU - LAM) / LAM * 100) == 3
_kiem_so()

NOTE = (70, 75, 95); DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128); DGREEN = (10, 110, 50)
ICEC, ICEO = (246, 251, 255), (120, 165, 215)
ENV, WIRE_C = (59, 130, 246), (190, 60, 40)
CUBES = [(258, 378), (322, 378), (386, 378), (450, 378), (296, 440), (356, 440), (414, 440), (352, 500)]
CS = 56
FS = 58
LV1, LV2 = 0.85 * M1 / M2, 0.85

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def stopwatch(d, cx, cy, r, p, done_txt=None):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVY, width=6)
    d.rectangle([cx - 14, cy - r - 26, cx + 14, cy - r], fill=NAVY)
    if p > 0:
        d.pieslice([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], -90, -90 + 360 * clamp(p), fill=(255, 220, 190))
        a = math.radians(-90 + 360 * clamp(p))
        d.line([(cx, cy), (cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a))], fill=ORANGE, width=6)
    dot(d, cx, cy, 8, NAVY)
    if done_txt: pill(d, cx, cy + r + 56, done_txt, NAVY)

def rig(d, t, on, lvl, scale_txt, p_watch, flow, watch_txt=None, labels=True):
    """on: day dien tro co dien; lvl: muc nuoc trong coc (0..1); flow: 0 khong chay, 1 nho giot cham, 2 chay nhanh."""
    card(d, (640, 270, 1040, 540), fill=WHITE, outline=NAVY, w=5, r=24)
    text(d, (840, 316), "Nguồn", FS, INK)
    card(d, (665, 360, 1015, 520), fill=(24, 30, 40), r=14)
    if on:
        text(d, (840, 402), f"U = {U} V", FS, (134, 239, 172))
        text(d, (840, 476), "I = 3,0 A", FS, (134, 239, 172))
    else:
        text(d, (840, 440), "TẮT", 62, GRAY)
    pts = [(200, 370), (560, 370), (398, 600), (398, 650), (362, 650), (362, 600)]
    d.polygon(pts, fill=(236, 244, 252)); d.line(pts + [pts[0]], fill=(130, 160, 200), width=5)
    for x, y in CUBES:
        d.rounded_rectangle([x, y, x + CS, y + CS], radius=10, fill=ICEC, outline=ICEO, width=4)
    col = WIRE_C if on else (120, 90, 80)
    zz = [(300 + 20 * k, 476 + (14 if k % 2 else -14)) for k in range(9)]
    d.line(zz, fill=col, width=7, joint="curve")
    if on:
        g = 0.4 + 0.3 * math.sin(t * 6)
        d.line(zz, fill=A((255, 140, 60), g), width=22, joint="curve")
    d.line([(300, 476), (300, 320), (610, 320), (610, 410), (640, 410)], fill=NAVY, width=5, joint="curve")
    d.line([(460, 476), (460, 348), (590, 348), (590, 470), (640, 470)], fill=NAVY, width=5, joint="curve")
    if labels:
        text(d, (840, 600), "dây điện trở", FS, WIRE_C)
        d.line([(700, 630), (472, 492)], fill=NOTE, width=4); dot(d, 470, 491, 7, NOTE)
    if flow == 1:
        u = (t * 0.9) % 1; dot(d, 380, 660 + u * 70, 9, ENV)
    elif flow == 2:
        for k in range(4):
            u = (t * 2.6 + k / 4) % 1; dot(d, 380, 658 + u * 72, 9, ENV)
    cup = [(300, 735), (460, 735), (446, 852), (314, 852)]
    d.polygon(cup, fill=(232, 242, 252))
    if lvl > 0.002:
        yw = 852 - 112 * lvl
        xl = 314 - 14 * (852 - yw) / 117; xr = 446 + 14 * (852 - yw) / 117
        d.polygon([(xl, yw), (xr, yw), (446, 852), (314, 852)], fill=(165, 205, 248))
    d.line(cup, fill=(90, 130, 185), width=8)
    text(d, (180, 790), "cốc", FS, INK)
    d.rounded_rectangle([250, 852, 510, 868], radius=6, fill=(150, 155, 170))
    card(d, (220, 868, 540, 990), fill=NAVY, r=18)
    card(d, (250, 882, 510, 976), fill=(20, 60, 40), r=10)
    text(d, (380, 929), scale_txt, 62, (134, 239, 172))
    text(d, (130, 929), "cân", FS, INK)
    stopwatch(d, 850, 770, 92, p_watch, watch_txt)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut A-D) ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, t, False, 0.0, "? g", 0.0, 0)
    ka = appear(t, M[1] - 0.2, 0.5)
    if ka <= 0: return
    y0 = 1070 + (1 - ka) * 30
    card(d, (60, y0, 1020, y0 + 470), fill=A(WHITE, ka), outline=A(PURPLE, ka), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, ka)
    text(d, (W / 2, y0 + 175), "Chưa cấp điện, 300 s:", 64, INK, alpha=ka)
    text(d, (W / 2, y0 + 265), "cốc hứng được bao nhiêu?", 64, PURPLE, alpha=ka)
    seg_bar(d, y0 + 360, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, ka)

# ---------------- canh 2: Tien hanh (hai giai doan, cung 300 s) ----------------
def phases(sc):
    M = sc["M"]
    return (0.6, M[1] - 0.3), (M[2] + 0.4, M[3] - 0.3)      # (bat dau, ket thuc) giai doan 1, 2

def state(t, sc):
    (a1, b1), (a2, b2) = phases(sc); M = sc["M"]
    if t < M[2]:
        p = clamp((t - a1) / (b1 - a1))
        return dict(stg=1, on=False, lvl=LV1 * p, p=p, flow=1 if 0 < p < 1 else 0,
                    txt="5,0 g" if p >= 1 else "· · ·", done=p >= 1)
    p = clamp((t - a2) / (b2 - a2))
    return dict(stg=2, on=True, lvl=LV2 * p, p=p, flow=2 if 0 < p < 1 else 0,
                txt="36,4 g" if p >= 1 else "· · ·", done=p >= 1)

def bars(d, t, y0, ka1, ka2, p1=1.0, p2=1.0, kv=(None, None)):
    for j, (lab, m, col, k, p) in enumerate((("m₁", M1, ENV, ka1, p1), ("m₂", M2, ORANGE, ka2, p2))):
        kval = k if kv[j] is None else kv[j]
        y = y0 + 120 * j
        if k <= 0: continue
        text(d, (115, y), lab, 64, col, alpha=k)
        d.rounded_rectangle([180, y - 30, 800, y + 30], radius=30, fill=(244, 240, 232))
        wpx = 620 * m / M2 * p
        if wpx > 4: d.rounded_rectangle([180, y - 30, 180 + max(60, wpx), y + 30], radius=30, fill=col)
        if kval > 0: text(d, (990, y), (f"{m:.1f}".replace(".", ",")) + " g", 62, col, anchor="rm", alpha=kval)

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    st = state(t, sc)
    rig(d, t, st["on"], st["lvl"], st["txt"], st["p"], st["flow"], "300 s" if st["done"] else None, labels=False)
    card(d, (60, 1080, 1020, 1540), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 1160), f"Giai đoạn {st['stg']}", 66, ENV if st["stg"] == 1 else ORANGE)
    (a1, b1), (a2, b2) = phases(sc)
    p1 = clamp((t - a1) / (b1 - a1))
    bars(d, t, 1300, 1.0, appear(t, b2, 0.3), p1=p1, kv=(appear(t, b1, 0.3), None))

# ---------------- canh 3: Ket qua + Rut ra ----------------
BASE, HMAX = 900, 470
def s_ket(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (60, 270, 1020, 1010), fill=WHITE, outline=LIGHT, w=3)
    h1, h2 = HMAX * M1 / M2, HMAX
    split = appear(t, M[0] + 0.6, 0.5)
    d.rounded_rectangle([150, BASE - h1, 290, BASE], radius=10, fill=ENV)
    text(d, (220, BASE - h1 - 45), "5,0 g", 62, ENV)
    d.rounded_rectangle([430, BASE - h2, 570, BASE], radius=10, fill=ORANGE)
    if split > 0:
        d.rounded_rectangle([430, BASE - h1, 570, BASE], radius=10, fill=A(ENV, split))
        d.line([(430, BASE - h1), (570, BASE - h1)], fill=A(WHITE, split), width=5)
        text(d, (600, BASE - h1 / 2 - 10), "môi trường", FS, ENV, anchor="lm", alpha=split)
    text(d, (500, BASE - h2 - 45), "36,4 g", 62, ORANGE)
    d.line([(100, BASE), (980, BASE)], fill=NAVY, width=4)
    text(d, (220, BASE + 55), "lần 1", FS, INK); text(d, (500, BASE + 55), "lần 2", FS, INK)
    k2 = appear(t, M[1], 0.4)
    if k2 > 0:
        text(d, (600, BASE - h2 / 2 - 40), "do dây:", FS, DORANGE, anchor="lm", alpha=k2)
        text(d, (600, BASE - h2 / 2 + 35), "31,4 g", 62, DORANGE, anchor="lm", alpha=k2)
    k3 = appear(t, M[2], 0.4)
    if k3 > 0:
        card(d, (60, 1060, 1020, 1540), fill=A(WHITE, k3), outline=A(ORANGE, k3), w=5)
        text(d, (W / 2, 1125), "λ: nhiệt nóng chảy riêng", FS, INK, alpha=k3)
        text(d, (W / 2, 1225), "λ = U·I·τ / (m₂ − m₁)", 66, INK, alpha=k3)
        text(d, (W / 2, 1325), "U·I·τ = 12·3,0·300 = 10 800 J", 58, NAVY, alpha=k3)
        text(d, (W / 2, 1440), "λ ≈ 3,44·10⁵ J/kg", 72, DORANGE, alpha=k3)

# ---------------- canh 4: Bay ----------------
X0, X1, L0, L1 = 150, 930, 2.9, 3.6
def XL(v): return X0 + (v - L0) / (L1 - L0) * (X1 - X0)

def chevron_r(d, x, y, s=22, w=6):
    for sg in (1, -1):
        a = math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=NAVY, width=w)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (60, 270, 1020, 640), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 335, "BẪY", RED)
    q = "“Chia luôn cho m₂”"
    text(d, (W / 2, 450), q, 66, INK)
    ks = clamp((t - (M[0] + 2.6)) / 0.4)
    if ks > 0:
        lw = tw(d, q, F(66)); d.line([(W / 2 - lw / 2, 452), (W / 2 - lw / 2 + lw * ks, 452)], fill=RED, width=7)
    k1 = appear(t, M[0] + 1.2, 0.4)
    text(d, (W / 2, 565), "nhỏ hơn thật 11%", 62, RED, alpha=k1)
    card(d, (60, 690, 1020, 1540), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 770), "λ (·10⁵ J/kg)", 62, NAVY)
    ya = 1090
    d.line([(X0 - 30, ya), (X1 + 30, ya)], fill=NAVY, width=6); chevron_r(d, X1 + 34, ya)
    for i in range(8):
        x = XL(2.9 + 0.1 * i); d.line([(x, ya - 16), (x, ya + 16)], fill=NAVY, width=4)
    def mark(v, lab, col, up, a):
        if a <= 0: return
        x = XL(v); d.line([(x, ya - 26), (x, ya + 26)], fill=A(col, a), width=7); dot(d, x, ya, 15, A(col, a))
        s_ = f"{v:.2f}".replace(".", ",")
        if up: text(d, (x, ya - 75), s_, 62, col, alpha=a); text(d, (x, ya - 150), lab, FS, col, alpha=a)
        else: text(d, (x, ya + 75), s_, 62, col, alpha=a); text(d, (x, ya + 150), lab, FS, col, alpha=a)
    mark(LAM, "tra bảng", DGREEN, True, 1.0)
    mark(LAM_M2, "÷ m₂", DRED, False, k1)
    k2 = appear(t, M[1] + 0.5, 0.4)
    mark(LAM_TRU, "÷ (m₂−m₁)", DORANGE, False, k2)
    text(d, (W / 2, 1430), "lớn hơn thật 3%", 62, DORANGE, alpha=k2)

# ---------------- canh 5: Chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    cx, y0 = W / 2, 400                                    # nhiet ke phong dang len (khong so)
    d.rounded_rectangle([cx - 26, y0, cx + 26, y0 + 330], radius=26, fill=A(WHITE, k1), outline=A(NAVY, k1), width=6)
    dot(d, cx, y0 + 370, 50, A(RED, k1)); d.ellipse([cx - 50, y0 + 320, cx + 50, y0 + 420], outline=A(NAVY, k1), width=6)
    hh = 110 + 140 * ease(clamp((t - 0.6) / 4.0))
    d.rectangle([cx - 12, y0 + 330 - hh, cx + 12, y0 + 340], fill=A(RED, k1))
    for j in range(2):
        yy = y0 + 160 - 50 * j
        arrow(d, (cx + 90, yy + 40), (cx + 90, yy - 40), A(DRED, k1), w=7, head=20) if j == 0 else None
    text(d, (W / 2, 930), "Phòng ấm dần lên", 64, INK, alpha=k1)
    text(d, (W / 2, 1020), "trong giai đoạn 2.", 64, INK, alpha=k1)
    text(d, (W / 2, 1130), "So với phòng không đổi,", 64, INK, alpha=k1)
    text(d, (W / 2, 1220), "λ lệch lên hay xuống?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1370, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, b, e = (sc[x] for x in ("hook", "do", "ket", "bay", "end"))
    (a1, b1), (a2, b2) = phases(do)
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + b1, "ding"), (do["t0"] + do["M"][2], "tap"),
            (k["t0"] + k["M"][2], "tap"), (b["t0"] + 0.1, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l12-thuchanh-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thực hành đo nhiệt nóng chảy riêng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Phễu nước đá, hai lần đo", draw=s_hook, tail=0.3, caps=[
   ("Phễu đá, dây điện trở.", 3.2),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Chưa cấp điện, hứng 300 s.", 3.2),
   ("Đá vẫn tan: ít, nhưng khác 0.", 2.8),
   ("Cấp điện, hứng tiếp 300 s.", 3.2),
   ("Cốc đầy: 36,4 g.", 2.7)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.3, caps=[
   ("Lần 2 môi trường vẫn làm tan.", 3.4),
   ("Phần do dây: m₂ − m₁.", 3.0),
   ("Chia cho đúng phần do dây.", 3.0)]),
 dict(key="bay", title="Bẫy khi tính λ", draw=s_bay, tail=0.5, caps=[
   ("Quên trừ m₁ thì sao?", 3.6),
   ("Một phần nhiệt dây làm ấm phễu.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("m₁ còn là 5,0 g?", 6.0)]),
])
