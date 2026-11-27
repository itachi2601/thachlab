# Clip: tn-l11-nguon-dien-02 - Do U hai cuc pin khi doi dien tro mach ngoai: U tut khi I tang.
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nguon-dien-02.json:
#   so_lieu_mau (R Ohm, I A, U V): 14 0,10 1,40 ; 9 0,15 1,35 ; 4 0,30 1,20 ; 2 0,50 1,00 ; 1,5 0,60 0,90.
#   cac_buoc.lam: K mo (ho mach) von ke chi 1,50 V. rut_ra[2]: doan mach (R = 0) thi U = 0.
# Ban 1 (31/10/2026). Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 56 px, <= 180 tu/phut moi canh, nhip >= 2,5 s,
#   K10 (khong nut A-D), bo canh "Chua noi duoc" (giu trong khung web).
# Du doan (DOI CA so voi ban 1): hop exp trong bai da viet "R giam, I tang, U tut 1,40 -> 0,90 V" -> ca cu lo.
#   Ca moi: giam R mai ve gan 0, von ke tien toi dau? -> ve 0 (kho rut_ra[2]; tren do thi: keo dai duong thang
#   qua 5 diem toi truc I). Khong ghi so giao diem tren truc I va khong hien r = 1,0 Ohm: cau Tu kiem tra ngay sau
#   video hoi "r bang bao nhieu".
# Bay (hien_tuong_hay_sai[0]): "von ke luon chi 1,5 V ghi tren pin" -> K mo 1,50 V canh K dong R = 4 Ohm 1,20 V.
# THU NGHI (= cau_chot khung, CA TU SUY: R = 5 Ohm trong tham_so 0..20): ampe ke chi 0,25 A -> U = 1,50 - 0,25 = 1,25 V
#   (doc tren duong thang hoac phan hut ti le voi I). Chua tung hien 0,25 A / 1,25 V.
from engine import *

ROWS = [(14, 0.10, 1.40), (9, 0.15, 1.35), (4, 0.30, 1.20), (2, 0.50, 1.00), (1.5, 0.60, 0.90)]   # so_lieu_mau
E0 = 1.50

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-nguon-dien-02.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["E"]["mac_dinh"] == E0 and ts["R"]["min"] <= 5 <= ts["R"]["max"]
    for R, I, U in ROWS: assert abs(E0 / (R + 1.0) - I) < 1e-9 and abs(I * R - U) < 1e-9
    assert abs(E0 / (5 + 1.0) - 0.25) < 1e-9 and abs(0.25 * 5 - 1.25) < 1e-9
_kiem_so()

def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def vr(r): return vn(r, 1) if r != int(r) else str(int(r))
BODY = (70, 78, 100); SCR = (220, 240, 225); WIRE = (60, 66, 90)
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8)
FS = 58

def pill(d, cx, cy, s, fill, alpha=1.0, size=FS, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(LIGHT, a), r=18, w=4)

# ---------------- mach: pin - K - ampe ke - R ; von ke o hai cuc pin ----------------
XL, XR, YT, YB = 150, 930, 380, 820
AM = (640, YT, 290)
VM = (360, 600, 270)
RB = (840, 500, 1020, 720)
KP, KC = (500, YB), (620, YB)
LOOP = [(XL, 560), (XL, YT), (XR, YT), (XR, YB), (XL, YB), (XL, 650)]

def meter(d, c, reading):
    cx, cy, w = c
    card(d, (cx - w / 2, cy - 60, cx + w / 2, cy + 60), fill=BODY, r=18)
    card(d, (cx - w / 2 + 14, cy - 46, cx + w / 2 - 14, cy + 46), fill=SCR, r=10)
    text(d, (cx, cy), reading, FS, (20, 60, 30))

def _along(s):
    segs = list(zip(LOOP, LOOP[1:])); tot = sum(math.dist(a, b) for a, b in segs); s %= tot
    for a, b in segs:
        L = math.dist(a, b)
        if s <= L: return (a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L)
        s -= L
    return LOOP[-1]

def circuit(d, t, rlab, closed, I=0.0, U=E0):
    w = 8
    d.line([(XL, 570), (XL, YT), (AM[0] - AM[2] / 2, YT)], fill=WIRE, width=w, joint="curve")
    d.line([(AM[0] + AM[2] / 2, YT), (XR, YT), (XR, RB[1])], fill=WIRE, width=w, joint="curve")
    d.line([(XR, RB[3]), (XR, YB), (KC[0], YB)], fill=WIRE, width=w, joint="curve")
    d.line([(KP[0], YB), (XL, YB), (XL, 630)], fill=WIRE, width=w, joint="curve")
    d.line([(VM[0], YT), (VM[0], VM[1] - 60)], fill=WIRE, width=w); d.line([(VM[0], VM[1] + 60), (VM[0], YB)], fill=WIRE, width=w)
    for y in (YT, YB): dot(d, VM[0], y, 13, WIRE)
    d.line([(XL - 52, 584), (XL + 52, 584)], fill=NAVY, width=7)          # vach dai = (+)
    d.line([(XL - 27, 616), (XL + 27, 616)], fill=NAVY, width=16)
    text(d, (XL - 82, 545), "+", 62, RED); text(d, (XL - 82, 660), "−", 66, INK)
    text(d, (XL, YB + 62), "pin", FS, INK)
    card(d, RB, fill=BODY, r=16)
    card(d, (RB[0] + 10, 595, RB[2] - 10, 705), fill=SCR, r=10)
    text(d, ((RB[0] + RB[2]) / 2, 650), rlab, 56, (20, 60, 30))
    text(d, ((RB[0] + RB[2]) / 2, 548), "R", FS, WHITE)
    dot(d, KP[0], KP[1], 12, WIRE); dot(d, KC[0], KC[1], 12, WHITE, outline=WIRE)
    ang = 0.0 if closed else math.radians(-32); L = KC[0] - KP[0]
    d.line([KP, (KP[0] + L * math.cos(ang), KP[1] + L * math.sin(ang))], fill=WIRE, width=9)
    text(d, (560, YB + 62), "K", FS, INK)
    meter(d, AM, vn(I) + " A" if closed else "0,00 A")
    meter(d, VM, vn(U) + " V" if closed else "1,50 V")
    if closed:
        sp = 80 + 300 * I
        for k in range(22):
            x, y = _along(k * 115 + t * sp)
            if abs(x - AM[0]) < AM[2] / 2 + 8 and abs(y - YT) < 70: continue
            if RB[0] - 8 < x < RB[2] + 8 and RB[1] - 8 < y < RB[3] + 8: continue
            dot(d, x, y, 13, ORANGE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    circuit(d, t, "14 Ω", False)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 980 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 540), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 190), "Đóng K, giảm R dần về 0.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 290), "Số chỉ vôn kế", 64, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 375), "tiến tới đâu?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 445, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: doi R, doc I va U ----------------
def do_state(t):
    j = -1
    for i in range(5):
        if t >= 0.4 + 1.5 * i: j = i
    closed = j >= 0 and 0.7 + 1.5 * j <= t < 1.6 + 1.5 * j
    n = sum(1 for i in range(5) if t >= 0.7 + 1.5 * i)
    return j, closed, n

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    j, closed, n = do_state(t)
    R, I, U = ROWS[max(j, 0)]
    circuit(d, t, vr(R) + " Ω", closed, I, U)
    card(d, (40, 960, 1040, 1580), fill=WHITE, outline=LIGHT, w=4)
    for x, h in ((230, "R"), (540, "I"), (850, "U")): text(d, (x, 1015), h, 62, INK)
    d.line([(80, 1060), (1000, 1060)], fill=LIGHT, width=4)
    for i in range(n):
        R, I, U = ROWS[i]; yy = 1110 + 92 * i
        if i == n - 1: d.rounded_rectangle([70, yy - 40, 1010, yy + 40], radius=18, fill=(255, 237, 213))
        text(d, (230, yy), vr(R) + " Ω", FS, INK)
        text(d, (540, yy), vn(I) + " A", FS, INK)
        text(d, (850, yy), vn(U) + " V", FS, DRED)

# ---------------- canh 3: do thi U theo I, keo dai ----------------
GX0, GX1, GY0, GY1 = 220, 980, 1180, 460      # I 0..1,6 A ; U 0..1,6 V
def gx(i): return GX0 + i / 2.0 * (GX1 - GX0)
def gy(u): return GY0 - u / 1.6 * (GY0 - GY1)
def s_thang(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 260, 1040, 1300), fill=WHITE, outline=LIGHT, w=4)
    d.line([(GX0, GY1 - 60), (GX0, GY0)], fill=NAVY, width=5); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=5)
    text(d, (GX0 + 25, 350), "U (V)", FS, INK, anchor="lm")
    text(d, (1020, GY0 + 52), "I (A)", FS, INK, anchor="rm")
    for u in (0.5, 1.0, 1.5):
        d.line([(GX0 - 14, gy(u)), (GX0, gy(u))], fill=NAVY, width=4)
        text(d, (GX0 - 24, gy(u)), vn(u, 1), FS, INK, anchor="rm")
    for i in (0.3, 0.6):
        d.line([(gx(i), GY0), (gx(i), GY0 + 14)], fill=NAVY, width=4)
        text(d, (gx(i), GY0 + 52), vn(i, 1), FS, INK)
    dot(d, gx(0), gy(E0), 15, PURPLE, outline=WHITE)                    # ho mach: I = 0, U = 1,50 V
    text(d, (GX0 + 40, gy(E0) - 60), "K mở", FS, PURPLE, anchor="lm")
    kl = appear(t, 4.0, 0.5)
    if kl > 0:
        d.line([(gx(0), gy(E0)), (gx(0.6), gy(0.9))], fill=A(BLUE, kl), width=7)
    cur = -1
    for k, (R, I, U) in enumerate(ROWS):
        kk = appear(t, 0.4 + 0.75 * k, 0.3)
        if kk > 0: dot(d, gx(I), gy(U), 16, A(DRED, kk), outline=A(WHITE, kk)); cur = k
    if 0 <= cur and t < 4.0:                                           # duong gióng diem vua cham
        R, I, U = ROWS[cur]
        for s in range(12):
            y1 = gy(U) + (GY0 - gy(U)) * s / 12; y2 = y1 + (GY0 - gy(U)) / 24
            d.line([(gx(I), y1), (gx(I), y2)], fill=MUTED, width=6)
            x1 = GX0 + (gx(I) - GX0) * s / 12; x2 = x1 + (gx(I) - GX0) / 24
            d.line([(x1, gy(U)), (x2, gy(U))], fill=MUTED, width=6)
    ke = appear(t, M[1], 1.0)
    if ke > 0:                                                         # keo dai net dut toi U = 0
        i1 = 0.6 + (1.5 - 0.6) * ke
        n = 14
        for s in range(n):
            a = 0.6 + (i1 - 0.6) * s / n; b = 0.6 + (i1 - 0.6) * (s + 0.55) / n
            d.line([(gx(a), gy(E0 - a)), (gx(b), gy(E0 - b))], fill=BLUE, width=7)
        if ke >= 1: dot(d, gx(1.5), gy(0), 17, ORANGE, outline=WHITE)
    k2 = appear(t, M[1] + 1.2, 0.45)
    if k2 > 0:
        card(d, (80, 1360, 1000, 1530), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1445), "R về 0: U về 0", 64, DGREEN, alpha=k2)

# ---------------- canh 4: Bay (von ke luon chi 1,5 V?) ----------------
def mini(d, x0, closed, reading, lab1, lab2, col, ka):
    card(d, (x0, 260, x0 + 490, 1180), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=4)
    text(d, (x0 + 245, 330), "K mở" if not closed else "K đóng, R = 4 Ω", FS, INK, alpha=ka)
    a, b, yt, yb = x0 + 90, x0 + 400, 440, 760
    d.line([(a, yt), (b, yt), (b, yb), (a, yb)], fill=A(WIRE, ka), width=7)
    d.line([(a, yt), (a, 575)], fill=A(WIRE, ka), width=7); d.line([(a, 625), (a, yb)], fill=A(WIRE, ka), width=7)
    d.line([(a - 46, 586), (a + 46, 586)], fill=A(NAVY, ka), width=7); d.line([(a - 24, 614), (a + 24, 614)], fill=A(NAVY, ka), width=16)
    if not closed:
        d.rectangle([b - 10, 560, b + 10, 640], fill=A(WHITE, ka))
        d.line([(b, 560), (b + 40, 630)], fill=A(WIRE, ka), width=8)
    else:
        card(d, (b - 30, 530, b + 30, 670), fill=A(WHITE, ka), outline=A(NAVY, ka), r=8, w=5)
    d.line([(x0 + 245, yb), (x0 + 245, 870)], fill=A(WIRE, ka), width=6)          # von ke noi hai cuc pin
    d.line([(a, yt), (x0 + 45, yt), (x0 + 45, 920), (x0 + 125, 920)], fill=A(WIRE, ka), width=6, joint="curve")
    for p_ in ((x0 + 245, yb), (a, yt)): dot(d, p_[0], p_[1], 11, A(WIRE, ka))
    card(d, (x0 + 125, 870, x0 + 365, 970), fill=A(BODY, ka), r=14)
    card(d, (x0 + 137, 882, x0 + 353, 958), fill=A(SCR, ka), r=8)
    text(d, (x0 + 245, 920), reading, 56, (20, 60, 30), alpha=ka)
    text(d, (x0 + 245, 1050), lab1, FS, col, alpha=ka)
    text(d, (x0 + 245, 1120), lab2, FS, col, alpha=ka)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    mini(d, 40, False, "1,50 V", "không dòng", "đúng 1,50 V", DGREEN, appear(t, 0.2, 0.4))
    mini(d, 550, True, "1,20 V", "có dòng", "U dưới 1,50 V", DRED, appear(t, 2.4, 0.5))
    if t > 2.4:                                                         # dong chay trong mach phai
        for k in range(8):
            s = (k * 125 + t * 170) % 1000
            pts = [(640, 586), (640, 440), (950, 440), (950, 760), (640, 760), (640, 614)]
            segs = list(zip(pts, pts[1:])); rem = s
            for p, q in segs:
                L = math.dist(p, q)
                if rem <= L: dot(d, p[0] + (q[0] - p[0]) * rem / L, p[1] + (q[1] - p[1]) * rem / L, 12, ORANGE); break
                rem -= L
    k2 = appear(t, M[1], 0.45); k3 = appear(t, M[2] - 0.7, 0.45)
    if k2 * (1 - k3) > 0:
        a2 = k2 * (1 - k3)
        card(d, (80, 1260, 1000, 1430), fill=A((254, 242, 242), a2), outline=A(DRED, a2), w=5)
        text(d, (W / 2, 1345), "Pin cũng cản dòng", 60, DRED, alpha=a2)
    if k3 > 0:
        card(d, (40, 1220, 1040, 1600), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1290, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1420), "Nối tắt hẳn (R = 0),", 62, INK, alpha=k3)
        text(d, (W / 2, 1515), "dòng lớn cỡ nào?", 62, INK, alpha=k3)

# ---------------- canh 5: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k1)
    for (cx, rd) in ((330, "0,25 A"), (750, "? V")):
        card(d, (cx - 140, 460, cx + 140, 580), fill=A(BODY, k1), r=16)
        card(d, (cx - 126, 474, cx + 126, 566), fill=A(SCR, k1), r=10)
        text(d, (cx, 520), rd, 60, (20, 60, 30), alpha=k1)
    for j, (i_, u_) in enumerate((("0,15 A", "1,35 V"), ("0,30 A", "1,20 V"))):
        yy = 680 + 80 * j
        text(d, (330, yy), i_, 58, INK, alpha=k1); text(d, (540, yy), "→", 58, MUTED, alpha=k1)
        text(d, (750, yy), u_, 58, INK, alpha=k1)
    text(d, (W / 2, 920), "Cùng pin, nối R khác:", 64, INK, alpha=k1)
    text(d, (W / 2, 1010), "ampe kế chỉ 0,25 A.", 64, INK, alpha=k1)
    text(d, (W / 2, 1130), "Vôn kế chỉ bao nhiêu?", 66, DORANGE, alpha=k1)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, th, b, e = (sc[x] for x in ("hook", "do", "thang", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + 0.7 + 1.5 * i, "tap") for i in range(5)]
    out += [(th["t0"] + th["M"][1], "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-nguon-dien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Nguồn điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vôn kế ở hai cực pin", draw=s_hook, tail=0.3, caps=[
   ("K mở: vôn kế chỉ 1,50 V.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Đổi R, đọc I và U", draw=s_do, tail=0.4, caps=[
   ("Mỗi lần đóng K ngắn rồi mở.", 3.8),
   ("R nhỏ dần: I tăng, U tụt.", 4.0)]),
 dict(key="thang", title="Đồ thị U theo I", draw=s_thang, tail=0.4, caps=[
   ("Các điểm nằm trên một đường thẳng.", 4.2),
   ("Đáp án: kéo dài tới U = 0.", 4.2)]),
 dict(key="bay", title="Bẫy: vôn kế luôn 1,5 V?", draw=s_bay, tail=0.4, caps=[
   ("1,5 V trên vỏ: chỉ khi hở mạch.", 4.4),
   ("Có dòng thì U nhỏ hơn.", 3.6),
   ("Còn một chỗ chưa đo.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 7.0)]),
])
