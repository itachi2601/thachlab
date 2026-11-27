# Clip: tn-l11-nang-luong-dien-03 - Hieu suat cua hai pin AA theo dien tro mach ngoai.
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nang-luong-dien-03.json (E = 3,0 V, r = 1,0 Ohm):
#   so_lieu_mau (R Ohm, I A, U V, H %, P_R W): 1,0 1,50 1,50 50 2,25 ; 2,0 1,00 2,00 66,7 2,00 ;
#                                              4,0 0,60 2,40 80 1,44 ; 9,0 0,30 2,70 90 0,81
# Ban 1 (31/10/2026). Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 58 px, <= 180 tu/phut moi canh, nhip >= 2,5 s,
#   K10 (khong nut A-D), bo canh "Chua noi duoc" (giu trong khung web).
# Du doan (DOI CA so voi ban 1): hop exp trong bai da viet "Rut ra: H = U/E tang theo R" -> cau cu "R nao H lon nhat"
#   bi lo. Ca moi: dat R = 1,0 Ohm (bang r), H khoang bao nhieu? -> 50 % (hang 1 kho). Hop exp khong neu so 50 %.
# Bay (hien_tuong_hay_sai[1]): "thay I giam nen nghi H giam" -> hai cot I va U canh nhau o R = 1,0 va 9,0 Ohm.
#   Khong dung bay "R = r thi H lon nhat" vi trung cap so (R = 1,0 Ohm, 50 %) cua Du doan.
# THU NGHI (= cau_chot khung, CA TU SUY trong dai tham_so r 0,2..3): pin rat cu r = 3,0 Ohm, R = 9,0 Ohm
#   -> H = 9/12 = 75 %. Phan xa sai: 90 % (hang R = 9,0 Ohm cua bang). Khong dung r = 0,2 Ohm (83 %) vi bai mau
#   trong bai co dap so 83,3 %.
from engine import *

ROWS = [(1.0, 1.50, 1.50, 50.0, 2.25), (2.0, 1.00, 2.00, 66.7, 2.00),
        (4.0, 0.60, 2.40, 80.0, 1.44), (9.0, 0.30, 2.70, 90.0, 0.81)]      # so_lieu_mau
E_, R_IN = 3.0, 1.0

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-nang-luong-dien-03.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["E"]["gia_tri"] == E_ and ts["r"]["mac_dinh"] == R_IN and ts["r"]["max"] == 3
    for R, I, U, h, p in ROWS:
        assert abs(E_ / (R + R_IN) - I) < 1e-9 and abs(I * R - U) < 1e-9 and abs(100 * U / E_ - h) < 0.05
_kiem_so()

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def hs(h): return (vn(h, 1) if abs(h - round(h)) > 1e-6 else str(int(round(h)))) + " %"
BODY = (70, 78, 100); SCR = (220, 240, 225); WIRE = (60, 66, 90)
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8)
FS = 58

def pill(d, cx, cy, s, fill, alpha=1.0, size=FS, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- mach (khung nguon 1080x1920; ra mp4 x = 65 + 0,88x) ----------------
XL, XR, YT, YB = 130, 930, 380, 830
AM = (540, YT, 330)                 # ampe ke tren day tren (tam x, y, rong)
VM = (615, 610, 300)                # von ke song song voi R
YJ1, YJ2 = 450, 775                 # moc noi von ke tren canh phai
RB = (840, 500, 1020, 720)          # hop dien tro (mep phai 1020 -> 963 px trong mp4)
KP, KC = (420, YB), (540, YB)

def meter(d, c, reading):
    cx, cy, w = c
    card(d, (cx - w / 2, cy - 62, cx + w / 2, cy + 62), fill=BODY, r=18)
    card(d, (cx - w / 2 + 14, cy - 48, cx + w / 2 - 14, cy + 48), fill=SCR, r=10)
    text(d, (cx, cy), reading, FS, (20, 60, 30))

LOOP = [(XL, 560), (XL, YT), (XR, YT), (XR, YB), (XL, YB), (XL, 660)]   # chieu dong quy uoc: (+) tren -> ngoai -> (-)
def _along(s):
    segs = list(zip(LOOP, LOOP[1:])); tot = sum(math.dist(a, b) for a, b in segs); s %= tot
    for a, b in segs:
        L = math.dist(a, b)
        if s <= L: return (a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L)
        s -= L
    return LOOP[-1]

def circuit(d, t, rlab, closed, I=0.0):
    w = 8
    d.line([(XL, 560), (XL, YT), (AM[0] - AM[2] / 2, YT)], fill=WIRE, width=w, joint="curve")
    d.line([(AM[0] + AM[2] / 2, YT), (XR, YT), (XR, RB[1])], fill=WIRE, width=w, joint="curve")
    d.line([(XR, RB[3]), (XR, YB), (KC[0], YB)], fill=WIRE, width=w, joint="curve")
    d.line([(KP[0], YB), (XL, YB), (XL, 660)], fill=WIRE, width=w, joint="curve")
    d.line([(XR, YJ1), (VM[0], YJ1), (VM[0], VM[1] - 62)], fill=WIRE, width=w)
    d.line([(VM[0], VM[1] + 62), (VM[0], YJ2), (XR, YJ2)], fill=WIRE, width=w)
    for y in (YJ1, YJ2): dot(d, XR, y, 13, WIRE)
    for yc in (585, 645):                                   # hai pin noi tiep: vach dai = (+), vach ngan day = (-)
        d.line([(XL - 50, yc - 13), (XL + 50, yc - 13)], fill=NAVY, width=7)
        d.line([(XL - 26, yc + 13), (XL + 26, yc + 13)], fill=NAVY, width=16)
    text(d, (XL - 75, 540), "+", 62, RED); text(d, (XL - 75, 700), "−", 66, INK)
    text(d, (330, 560), "E = 3,0 V", FS, INK)
    text(d, (330, 650), "r = 1,0 Ω", FS, INK)
    card(d, RB, fill=BODY, r=16)
    card(d, (RB[0] + 10, 595, RB[2] - 10, 705), fill=SCR, r=10)
    text(d, ((RB[0] + RB[2]) / 2, 650), rlab, 56, (20, 60, 30))
    text(d, ((RB[0] + RB[2]) / 2, 548), "R", FS, WHITE)
    dot(d, KP[0], KP[1], 12, WIRE); dot(d, KC[0], KC[1], 12, WHITE, outline=WIRE)
    ang = 0.0 if closed else math.radians(-32); L = KC[0] - KP[0]
    d.line([KP, (KP[0] + L * math.cos(ang), KP[1] + L * math.sin(ang))], fill=WIRE, width=9)
    text(d, (480, YB + 62), "K", FS, INK)
    meter(d, AM, vn(I, 2) + " A" if closed else "0,00 A")
    meter(d, VM, vn(I * float(rlab.split()[0].replace(",", ".")), 2) + " V" if closed else "0,00 V")
    if closed:                                              # dien tich di theo chieu quy uoc, nhanh ~ I
        sp = 60 + 120 * I
        for k in range(22):
            x, y = _along(k * 115 + t * sp)
            if abs(x - AM[0]) < AM[2] / 2 + 8 and abs(y - YT) < 70: continue
            if RB[0] - 8 < x < RB[2] + 8 and RB[1] - 8 < y < RB[3] + 8: continue
            dot(d, x, y, 13, ORANGE)
        arrow(d, (230, YT - 60), (330, YT - 60), RED, w=8, head=26)
        text(d, (370, YT - 60), "I", FS, RED)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    circuit(d, t, "1,0 Ω", False)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1000 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 520), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 190), "Đặt R = 1,0 Ω, bằng r.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 280), "Hiệu suất H của pin", 62, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 360), "khoảng bao nhiêu %?", 62, PURPLE, alpha=k)
    seg_bar(d, y0 + 425, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: do o R = 1,0 Ohm ----------------
CL = 0.9
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    closed = t >= CL
    circuit(d, t, "1,0 Ω", closed, ROWS[0][1])
    card(d, (40, 1000, 1040, 1560), fill=WHITE, outline=LIGHT, w=4)
    k1 = appear(t, CL + 0.2, 0.4)
    text(d, (W / 2, 1110), "U = 1,50 V, E = 3,0 V", FS, INK, alpha=k1)
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        card(d, (110, 1220, 970, 1380), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1300), "H = U/E = 50 %", 66, DGREEN, alpha=k2)
    k3 = appear(t, M[1] + 2.6, 0.45)
    text(d, (W / 2, 1470), "nửa kia toả nhiệt trong pin", FS, DRED, alpha=k3)

# ---------------- canh 3: tang R ----------------
STEP = [0.5, 3.1, 5.7]              # moc dat R = 2,0 / 4,0 / 9,0 Ohm; K dong sau 0,4 s, mo sau 2,0 s
def tang_state(t):
    i = 0
    for j, x in enumerate(STEP):
        if t >= x: i = j + 1
    closed = i > 0 and STEP[i - 1] + 0.4 <= t < STEP[i - 1] + 2.0
    n = 1 + sum(1 for x in STEP if t >= x + 0.4)          # so hang bang da co
    return i, closed, n

def table(d, n, hl):
    card(d, (40, 960, 1040, 1580), fill=WHITE, outline=LIGHT, w=4)
    for x, h in ((230, "R"), (540, "U"), (850, "H")): text(d, (x, 1030), h, 62, INK)
    d.line([(80, 1080), (1000, 1080)], fill=LIGHT, width=4)
    for j in range(n):
        R, I, U, h, _ = ROWS[j]; yy = 1140 + 105 * j
        if j == hl: d.rounded_rectangle([70, yy - 44, 1010, yy + 44], radius=20, fill=(255, 237, 213))
        text(d, (230, yy), vn(R) + " Ω", FS, INK)
        text(d, (540, yy), vn(U, 2) + " V", FS, INK)
        text(d, (850, yy), hs(h), FS, DGREEN)

def s_tang(img, d, t, sc):
    IMG_REF[0] = img
    i, closed, n = tang_state(t)
    R, I = (ROWS[i][0], ROWS[i][1]) if i else (1.0, 0.0)
    circuit(d, t, vn(R) + " Ω", closed, I)
    table(d, n, n - 1)

# ---------------- canh 4: E chia hai phan ----------------
BX0, BX1 = 300, 1000               # thanh dai = E = 3,0 V
def s_ket(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 260, 1040, 1150), fill=WHITE, outline=LIGHT, w=4)
    text(d, (W / 2, 340), "E = 3,0 V chia thành:", FS, INK)
    for j, (R, I, U, h, _) in enumerate(ROWS):
        kb = appear(t, 0.3 + 0.35 * j, 0.5); yy = 470 + 135 * j
        if kb <= 0: continue
        text(d, (170, yy), vn(R) + " Ω", FS, INK, alpha=kb)
        xu = BX0 + (BX1 - BX0) * (U / E_) * kb
        d.rounded_rectangle([BX0, yy - 44, xu, yy + 44], radius=12, fill=GREEN)
        if kb > 0.95:
            d.rounded_rectangle([xu, yy - 44, BX1, yy + 44], radius=12, fill=(239, 68, 68))
            text(d, ((BX0 + xu) / 2, yy), hs(h), FS, WHITE)
    k2 = appear(t, 2.4, 0.4)
    if k2 > 0:
        d.rounded_rectangle([80, 1010, 150, 1080], radius=12, fill=A(GREEN, k2))
        text(d, (175, 1045), "U, ra ngoài", FS, DGREEN, anchor="lm", alpha=k2)
        d.rounded_rectangle([570, 1010, 640, 1080], radius=12, fill=A((239, 68, 68), k2))
        text(d, (665, 1045), "mất trong r", FS, DRED, anchor="lm", alpha=k2)
    k3 = appear(t, M[1], 0.45)
    if k3 > 0:
        card(d, (80, 1220, 1000, 1400), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1310), "r > 0: H luôn dưới 100 %", 62, DGREEN, alpha=k3)
    k4 = appear(t, M[1] + 2.6, 0.45)
    text(d, (W / 2, 1490), "R lớn: phần đỏ nhỏ dần", FS, INK, alpha=k4)

# ---------------- canh 5: Bay (I giam nhung U tang) ----------------
def bars(d, x0, title, vals, unit_max, col, lab, labcol, ka, kb):
    card(d, (x0, 260, x0 + 480, 1180), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=4)
    text(d, (x0 + 240, 340), title, 62, INK, alpha=ka)
    base = 1000
    d.line([(x0 + 40, base), (x0 + 440, base)], fill=A(NAVY, ka), width=5)
    for j, (v, rl) in enumerate(zip(vals, ("1,0 Ω", "9,0 Ω"))):
        cx = x0 + 130 + 220 * j; hh = 500 * v / unit_max * (kb if j else ka)
        d.rectangle([cx - 70, base - hh, cx + 70, base], fill=A(col, ka))
        text(d, (cx, base - hh - 45), vn(v, 2), FS, INK, alpha=ka if j == 0 else kb)
        text(d, (cx, base + 55), rl, FS, INK, alpha=ka)
    text(d, (x0 + 240, 1125), lab, 62, labcol, alpha=kb)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ka = appear(t, 0.2, 0.4); kb = appear(t, 1.2, 0.8)
    bars(d, 40, "I (A)", (1.50, 0.30), 2.7, (147, 180, 240), "giảm", DRED, ka, kb)
    bars(d, 560, "U (V)", (1.50, 2.70), 2.7, GREEN, "tăng", DGREEN, ka, kb)
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        card(d, (80, 1260, 1000, 1440), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1350), "H = U/E: theo U, tăng", 62, DGREEN, alpha=k2)

# ---------------- canh 6: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k1)
    for yc in (500, 560):
        d.line([(230, yc - 13), (330, yc - 13)], fill=A(NAVY, k1), width=7)
        d.line([(254, yc + 13), (306, yc + 13)], fill=A(NAVY, k1), width=16)
    text(d, (280, 660), "r = 3,0 Ω", 64, DRED, alpha=k1)
    card(d, (650, 470, 870, 590), fill=A(BODY, k1), r=16)
    text(d, (760, 530), "9,0 Ω", 60, WHITE, alpha=k1)
    text(d, (760, 660), "R", 64, INK, alpha=k1)
    text(d, (W / 2, 880), "Pin rất cũ, r = 3,0 Ω.", 64, INK, alpha=k1)
    text(d, (W / 2, 975), "Vẫn đặt R = 9,0 Ω.", 64, INK, alpha=k1)
    text(d, (W / 2, 1100), "H khoảng bao nhiêu %?", 66, DORANGE, alpha=k1)
    seg_bar(d, 1280, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, tg, k, b, e = (sc[x] for x in ("hook", "do", "tang", "ket", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"), (do["t0"] + CL, "tap"),
           (do["t0"] + do["M"][1], "ding")]
    out += [(tg["t0"] + x + 0.4, "tap") for x in STEP]
    out += [(k["t0"] + k["M"][1], "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-nang-luong-dien-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Năng lượng điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai pin AA và hộp điện trở", draw=s_hook, tail=0.3, caps=[
   ("Vôn kế đo U ở hai cực.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Đo ở R = 1,0 Ω", draw=s_do, tail=0.4, caps=[
   ("Đóng K, đọc nhanh hai đồng hồ.", 3.8),
   ("Đáp án: chỉ 50 %.", 3.6)]),
 dict(key="tang", title="Tăng dần R", draw=s_tang, tail=0.4, caps=[
   ("Mỗi lần đóng K ngắn rồi mở.", 3.6),
   ("U tăng dần về phía 3,0 V.", 3.8)]),
 dict(key="ket", title="Năng lượng đi đâu?", draw=s_ket, tail=0.4, caps=[
   ("Phần xanh: H của mỗi lần đo.", 3.8),
   ("Một phần luôn mất trong pin.", 4.2)]),
 dict(key="bay", title="Bẫy: I giảm thì H giảm?", draw=s_bay, tail=0.4, caps=[
   ("R tăng: I giảm, U tăng.", 3.6),
   ("H đi theo U, không theo I.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("R càng lớn so với r, H càng cao.", 6.0)]),
])
