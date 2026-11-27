# Clip: tn-l11-nguon-dien-01 - Tu dien "gia lam" nguon: von ke cua tu va cua pin theo thoi gian.
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nguon-dien-01.json -> so_lieu_mau:
#   t (s): 0, 20, 40, 60, 80, 100, 300 ; U tu (V): 2,70 2,21 1,81 1,48 1,21 0,99 0,13 ; U pin (V): 2,98 moi hang.
#   tham_so: C = 1,0 F, U0 = 2,7 V, R = 100 Ohm (dieu chinh 50-500), E_b = 3,0 V, r_b = 0,6 Ohm.
# Ban 1 (31/10/2026). Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 58 px, <= 180 tu/phut moi canh, nhip >= 2,5 s,
#   K10 (khong nut A-D), bo canh "Chua noi duoc" (giu trong khung web).
# Du doan (DOI CA so voi ban 1): hop exp trong bai da viet "von ke cua tu tut dan, cua pin dung yen" -> ca cu lo.
#   Ca moi: do thi U cua tu theo t co dang nao? -> tut nhanh luc dau, cham dan (hien_tuong_hay_sai[1]).
#   Do: 20 s dau tut 2,70 - 2,21 = 0,49 V; 20 s cuoi (80 -> 100 s) tut 1,21 - 0,99 = 0,22 V (tru thang tu kho).
# Bay (hien_tuong_hay_sai[0]): "tu cung day duoc dong nen la nguon" -> hai hinh canh nhau: tu can dien tich / pin co luc la bu.
# THU NGHI (= cau_chot khung, CA TU SUY trong dai tham_so R 50..500): nap lai 2,7 V, xa qua 200 Ohm -> sau 100 s von ke
#   tu chi TREN 0,99 V (mo hinh kho: 2,7 e^-0,5 = 1,64 V). Buoc suy luan chua chieu: R lon -> dong nho -> xa cham.
from engine import *

ROWS = [(0, 2.70, 2.98), (20, 2.21, 2.98), (40, 1.81, 2.98), (60, 1.48, 2.98), (80, 1.21, 2.98), (100, 0.99, 2.98),
        (300, 0.13, 2.98)]

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-nguon-dien-01.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["R"]["mac_dinh"] == 100 and ts["R"]["min"] <= 200 <= ts["R"]["max"] and ts["C"]["mac_dinh"] == 1
    assert abs(2.7 * math.exp(-100 / 200) - 1.64) < 0.005
_kiem_so()

def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); DBLUE = (29, 78, 216)
BODY = (70, 78, 100); SCR = (220, 240, 225); WIRE = (60, 66, 90)
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

# ---------------- hai mach (ba nhanh song song: nguon | von ke | R) ----------------
def panel(d, x0, kind, reading, alpha=1.0):
    card(d, (x0, 260, x0 + 490, 720), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=4)
    col = DBLUE if kind == "tu" else DORANGE
    text(d, (x0 + 245, 320), "Tụ 1,0 F" if kind == "tu" else "Pin E = 3,0 V", FS, col, alpha=alpha)
    a, m, b, yt, yb = x0 + 70, x0 + 245, x0 + 425, 395, 610
    wc = A(WIRE, alpha)
    d.line([(a, yt), (b, yt)], fill=wc, width=7); d.line([(a, yb), (b, yb)], fill=wc, width=7)
    for x in (a, b): d.line([(x, yt), (x, yb)], fill=wc, width=7)
    d.line([(m, yt), (m, yb)], fill=wc, width=7)
    ym = (yt + yb) / 2
    if kind == "tu":                                       # tu: hai ban song song
        d.rectangle([a - 30, ym - 30, a + 30, ym + 30], fill=A(WHITE, alpha))
        d.line([(a - 44, ym - 16), (a + 44, ym - 16)], fill=A(NAVY, alpha), width=9)
        d.line([(a - 44, ym + 16), (a + 44, ym + 16)], fill=A(NAVY, alpha), width=9)
    else:                                                  # pin: vach dai (+) o tren
        d.rectangle([a - 30, ym - 34, a + 30, ym + 34], fill=A(WHITE, alpha))
        d.line([(a - 46, ym - 14), (a + 46, ym - 14)], fill=A(NAVY, alpha), width=7)
        d.line([(a - 24, ym + 14), (a + 24, ym + 14)], fill=A(NAVY, alpha), width=16)
    card(d, (b - 30, ym - 70, b + 30, ym + 70), fill=A(WHITE, alpha), outline=A(NAVY, alpha), r=8, w=5)
    text(d, (b, ym), "R", 56, INK, alpha=alpha)
    card(d, (m - 108, ym - 56, m + 108, ym + 56), fill=A(BODY, alpha), r=14)
    card(d, (m - 96, ym - 44, m + 96, ym + 44), fill=A(SCR, alpha), r=8)
    text(d, (m, ym), reading, 56, (20, 60, 30), alpha=alpha)
    text(d, (m, 672), "R = 100 Ω", 56, INK, alpha=alpha)

# ---------------- do thi U theo t (0..100 s, 0..3 V) ----------------
GX0, GX1, GY0, GY1 = 200, 960, 1430, 1000
def gx(t): return GX0 + t / 100 * (GX1 - GX0)
def gy(u): return GY0 - u / 3 * (GY0 - GY1)
def graph(d, n, extra=0.0):
    card(d, (40, 730, 1040, 1580), fill=WHITE, outline=LIGHT, w=4)
    d.line([(GX0, GY1 - 50), (GX0, GY0)], fill=NAVY, width=5); d.line([(GX0, GY0), (GX1 + 40, GY0)], fill=NAVY, width=5)
    text(d, (GX0 + 20, 800), "U (V)", FS, INK, anchor="lm")
    text(d, (1025, 1385), "t (s)", FS, INK, anchor="rm")
    for u in (1, 2, 3):
        d.line([(GX0 - 14, gy(u)), (GX0, gy(u))], fill=NAVY, width=4)
        text(d, (GX0 - 30, gy(u)), str(u), FS, INK, anchor="rm")
    for tt in (0, 20, 40, 60, 80, 100):
        d.line([(gx(tt), GY0), (gx(tt), GY0 + 14)], fill=NAVY, width=4)
    for tt in (0, 50, 100):
        text(d, (gx(tt), GY0 + 50), str(tt), FS, INK)
    pts_t = [(gx(r[0]), gy(r[1])) for r in ROWS[:n]]
    pts_p = [(gx(r[0]), gy(r[2])) for r in ROWS[:n]]
    if n > 1:
        d.line(pts_p, fill=ORANGE, width=7); d.line(pts_t, fill=BLUE, width=7)
    for (x, y) in pts_p: dot(d, x, y, 15, ORANGE, outline=WHITE)
    for (x, y) in pts_t: dot(d, x, y, 15, BLUE, outline=WHITE)
    if extra > 0:                                          # do tut 20 s dau va 20 s cuoi
        for (ta, ua), (tb, ub), lab, lx, ly in (((0, 2.70), (20, 2.21), "−0,49 V", gx(24), gy(2.55)),
                                                 ((80, 1.21), (100, 0.99), "−0,22 V", gx(72), gy(0.55))):
            d.line([(gx(ta), gy(ua)), (gx(tb), gy(ua))], fill=A(DRED, extra), width=5)
            d.line([(gx(tb), gy(ua)), (gx(tb), gy(ub))], fill=A(DRED, extra), width=11)
            text(d, (lx, ly), lab, FS, DRED, anchor="lm" if lx < 500 else "mm", alpha=extra)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    panel(d, 40, "tu", "2,70 V"); panel(d, 550, "pin", "2,98 V")
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 780 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 190), "Đọc vôn kế của tụ mỗi 20 s.", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 290), "Đồ thị U theo t", 64, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 375), "có dạng nào?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 450, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: doc moi 20 s ----------------
P0, DP = 0.5, 0.8                    # moc cham diem 0, 20, ..., 100 s
def n_do(t): return max(0, min(6, int((t - P0) / DP) + 1)) if t >= P0 else 0
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    n = n_do(t); r = ROWS[max(0, n - 1)]
    panel(d, 40, "tu", vn(r[1]) + " V"); panel(d, 550, "pin", vn(r[2]) + " V")
    graph(d, n, appear(t, M[1] + 0.3, 0.5))
    card(d, (640, 765, 1010, 845), fill=NAVY, r=36)
    text(d, (825, 805), f"t = {r[0]} s", 56, WHITE)

# ---------------- canh 3: sau 5 phut ----------------
FF0, FF1 = 0.4, 2.6                  # tua nhanh 100 s -> 300 s
def s_lau(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    done = t >= FF1
    panel(d, 40, "tu", "0,13 V" if done else "…"); panel(d, 550, "pin", "2,98 V")
    card(d, (40, 730, 1040, 1580), fill=WHITE, outline=LIGHT, w=4)
    cx, cy, R = 300, 960, 150
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(248, 250, 252), outline=NAVY, width=8)
    p = clamp((t - FF0) / (FF1 - FF0)); ang = -math.pi / 2 + 2 * math.pi * (p * 3.33)
    d.line([(cx, cy), (cx + 120 * math.cos(ang), cy + 120 * math.sin(ang))], fill=RED, width=9)
    dot(d, cx, cy, 14, NAVY)
    text(d, (720, 900), "t = 300 s" if done else "tua nhanh", 62, NAVY if done else ORANGE)
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        card(d, (80, 1180, 1000, 1350), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1265), "Pin duy trì được U", 64, DGREEN, alpha=k2)
    k3 = appear(t, M[1] + 2.6, 0.45)
    text(d, (W / 2, 1460), "tụ: hết điện tích có sẵn", FS, DRED, alpha=k3)

# ---------------- canh 4: Bay (tu cung la nguon?) ----------------
def loop_pt(s, x0):
    pts = [(x0 + 100, 620), (x0 + 100, 430), (x0 + 400, 430), (x0 + 400, 900), (x0 + 100, 900), (x0 + 100, 700)]
    segs = list(zip(pts, pts[1:])); tot = sum(math.dist(a, b) for a, b in segs); s %= tot
    for a, b in segs:
        L = math.dist(a, b)
        if s <= L: return (a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L)
        s -= L
    return pts[-1]

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ka = appear(t, 0.2, 0.4)
    for x0, lab, col in ((40, "Tụ", DBLUE), (550, "Pin", DORANGE)):
        card(d, (x0, 260, x0 + 490, 1220), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=4)
        text(d, (x0 + 245, 330), lab, 64, col, alpha=ka)
        for seg in (((x0 + 100, 620), (x0 + 100, 430), (x0 + 400, 430), (x0 + 400, 900), (x0 + 100, 900), (x0 + 100, 700)),):
            d.line(seg, fill=A(WIRE, ka), width=7, joint="curve")
        card(d, (x0 + 370, 580, x0 + 430, 760), fill=A(WHITE, ka), outline=A(NAVY, ka), r=8, w=5)
        text(d, (x0 + 400, 670), "R", 56, INK, alpha=ka)
    # tu: hai ban, dien tich tren ban giam dan; dong cham dan
    q = math.exp(-max(0, t - 0.8) / 2.2); nq = int(round(4 * q))
    x0 = 40
    d.line([(x0 + 30, 620), (x0 + 170, 620)], fill=NAVY, width=10); d.line([(x0 + 30, 700), (x0 + 170, 700)], fill=NAVY, width=10)
    for j in range(nq):
        xx = x0 + 50 + j * 34
        text(d, (xx, 578), "+", 56, RED); text(d, (xx, 742), "−", 56, BLUE)
    s0 = 2.5 * (1 - q) * 520
    for k in range(int(round(8 * q))):
        x, y = loop_pt(k * 170 + s0 * 1.0 + 0, x0); dot(d, x, y, 13, ORANGE)
    # pin: luc la bu lai, dong deu
    x0 = 550
    d.line([(x0 + 54, 640), (x0 + 146, 640)], fill=NAVY, width=7); d.line([(x0 + 76, 680), (x0 + 124, 680)], fill=NAVY, width=16)
    for k in range(8):
        x, y = loop_pt(k * 170 + t * 260, x0); dot(d, x, y, 13, ORANGE)
    arrow(d, (x0 + 200, 730), (x0 + 200, 590), DGREEN, w=9, head=26)
    kb = appear(t, 0.9, 0.4)
    text(d, (285, 1010), "điện tích", FS, DRED, alpha=kb); text(d, (285, 1090), "cạn dần", FS, DRED, alpha=kb)
    text(d, (795, 1010), "lực lạ", FS, DGREEN, alpha=kb); text(d, (795, 1090), "bù lại", FS, DGREEN, alpha=kb)
    k2 = appear(t, M[1], 0.45); k3 = appear(t, M[2] - 0.7, 0.45)
    if k2 * (1 - k3) > 0:
        a2 = k2 * (1 - k3)
        card(d, (80, 1290, 1000, 1460), fill=A((254, 242, 242), a2), outline=A(DRED, a2), w=5)
        text(d, (W / 2, 1375), "Tụ không phải nguồn điện", 62, DRED, alpha=a2)
    if k3 > 0:
        card(d, (40, 1250, 1040, 1600), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1320, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1440), "Vì sao pin chỉ 2,98 V,", 62, INK, alpha=k3)
        text(d, (W / 2, 1530), "chưa đủ 3,0 V?", 62, INK, alpha=k3)

# ---------------- canh 5: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k1)
    d.line([(230, 500), (370, 500)], fill=A(NAVY, k1), width=10); d.line([(230, 560), (370, 560)], fill=A(NAVY, k1), width=10)
    text(d, (300, 650), "tụ 1,0 F", 64, DBLUE, alpha=k1)
    card(d, (640, 470, 900, 590), fill=A(WHITE, k1), outline=A(NAVY, k1), r=12, w=6)
    text(d, (770, 530), "200 Ω", 64, INK, alpha=k1)
    text(d, (W / 2, 860), "Nạp lại 2,7 V, xả qua 200 Ω.", 64, INK, alpha=k1)
    text(d, (W / 2, 1040), "Sau 100 s, vôn kế tụ", 66, DORANGE, alpha=k1)
    text(d, (W / 2, 1130), "chỉ khoảng bao nhiêu?", 66, DORANGE, alpha=k1)
    text(d, (W / 2, 1250), "Với 100 Ω: 0,99 V sau 100 s", 54, INK, alpha=k1)
    seg_bar(d, 1390, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, la, b, e = (sc[x] for x in ("hook", "do", "lau", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + P0 + j * DP, "tap") for j in range(6)]
    out += [(do["t0"] + do["M"][1], "ding")]
    out += [(la["t0"] + FF0 + j * 0.3, "tick") for j in range(7)] + [(la["t0"] + FF1, "tap")]
    out += [(b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-nguon-dien-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Nguồn điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tụ đã nạp và pin", draw=s_hook, tail=0.3, caps=[
   ("Mỗi bên nuôi điện trở 100 Ω.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Đọc vôn kế mỗi 20 s", draw=s_do, tail=0.4, caps=[
   ("Chấm hai đường: tụ và pin.", 4.4),
   ("Đáp án: tụt nhanh trước, chậm sau.", 4.6)]),
 dict(key="lau", title="Đọc lại sau 5 phút", draw=s_lau, tail=0.4, caps=[
   ("Tua nhanh tới 300 s.", 3.4),
   ("Tụ còn 0,13 V, pin vẫn 2,98 V.", 4.8)]),
 dict(key="bay", title="Bẫy: tụ cũng là nguồn?", draw=s_bay, tail=0.4, caps=[
   ("Tụ cũng đẩy được dòng, lúc đầu.", 4.0),
   ("Nhưng không giữ được U.", 4.0),
   ("Còn một chỗ chưa rõ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 7.0)]),
])
