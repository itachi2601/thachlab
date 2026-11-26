# Clip: tn-l12-thangnhietdo-03 - Binh khi kin ngam nuoc o 5 muc nhiet do, keo dai do thi p theo t toi p = 0.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-03.json:
#   so_lieu_mau (minh hoa): (0 °C; 100,0 kPa) (25; 109,2) (50; 118,3) (75; 127,5) (100; 136,6)
#   mo_hinh: p = p0.(1 + alpha.t), alpha = 1/273,15 -> t_cat = −273,15 °C (ghi "−273 °C" tren man)
#   tham_so p0: 80-150 kPa -> Bay ve ba duong p0 = 80/100/150, khong ghi so.
# Ban 1 (14/11/2026). Ban 2 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2 s), <= 50 s, K10 (khong nut A-D), bo canh "chua noi duoc" (giu trong khung web;
#   rieng y "khi that hoa long truoc do, diem cat la ngoai suy" giu mot phu de o canh ket de khoi sai vat li).
# Du doan (khung web): keo dai p(t) toi p = 0 cat truc o dau? A 0 °C (hien_tuong_hay_sai[0]) / B −100 °C / C −273 °C (DUNG)
#   / D tuy luong khi.
# Bay (hien_tuong_hay_sai[1]): doi luong khi -> diem cat doi? Hai hinh canh nhau: "neu tuy khi" / "do that".
# THU NGHI (= cau_chot khung, CA TU SUY ghi trong kho): dun toi 273 °C, giu the tich -> p ≈ 200 kPa (546 K = 2 x 273 K).
from engine import *

LV = ((0, 100.0), (25, 109.2), (50, 118.3), (75, 127.5), (100, 136.6))
TCUT = -273.15

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-thangnhietdo-03.json")))
    assert tuple(tuple(r) for r in k["so_lieu_mau"]["hang"]) == LV
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["p0"]["mac_dinh"] == 100 and ts["p0"]["min"] == 80 and ts["p0"]["max"] == 150
    for tc, p in LV: assert abs(100 * (1 + tc / 273.15) - p) < 0.06
    assert round(100 * (1 + 273 / 273.15)) == 200
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
FS = 58
NOTE = (70, 75, 95)
SCREEN = (24, 30, 40); LCD = (134, 239, 172)
ICE = (200, 228, 252); HOT = (250, 176, 146)
def f1(x): return f"{x:.1f}".replace(".", ",")
def pmod(p0, tc): return p0 * (1 - tc / TCUT)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def dashed(d, p1, p2, color, w=5, dash=18, gap=12):
    L = math.dist(p1, p2)
    if L < 1: return
    for i in range(int(L // (dash + gap)) + 1):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

# ---------------- dung cu: noi nuoc + binh kin + hai man hinh (y 270..860) ----------------
def rig(d, t, idx, n_read, ka=1.0):
    """idx: muc nuoc 0..4; n_read: -1 = chua doc."""
    wk = idx / 4
    d.rounded_rectangle([230, 820, 850, 846], radius=8, fill=mix((90, 96, 110), (234, 88, 12), wk))
    d.rounded_rectangle([210, 560, 870, 826], radius=30, fill=(214, 220, 230), outline=(110, 118, 135), width=5)
    d.rounded_rectangle([222, 594, 858, 814], radius=22, fill=mix(ICE, HOT, wk))
    if idx == 0:
        for (x, y, a) in ((270, 620, 12), (720, 612, -10), (800, 660, 18), (300, 740, -6), (620, 760, 30)):
            pts = [(x + 30 * math.cos(math.radians(a + 45 + 90 * k)), y + 30 * math.sin(math.radians(a + 45 + 90 * k))) for k in range(4)]
            d.polygon(pts, fill=(240, 248, 255), outline=(150, 190, 230))
    for k in range(8):                                   # nuoc chuyen dong (bot nho, nhanh dan theo muc nhiet)
        ph = (t * (0.3 + 0.6 * wk) + k * 0.29) % 1
        x = 250 + k * 78 + 8 * math.sin(t * 4 + k); y = lerp(800, 610, ph)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=A(WHITE, 0.4 + 0.6 * wk), width=3)
    d.ellipse([440, 620, 620, 800], fill=(236, 244, 252), outline=(90, 120, 160), width=5)
    d.rectangle([508, 470, 552, 630], fill=(236, 244, 252), outline=(90, 120, 160), width=5)
    d.rectangle([513, 620, 547, 636], fill=(236, 244, 252))
    d.rounded_rectangle([498, 450, 562, 478], radius=6, fill=NAVY)
    d.line([(530, 450), (530, 400), (330, 400), (330, 380)], fill=NAVY, width=8)
    d.line([(760, 380), (760, 770)], fill=(90, 96, 110), width=9); dot(d, 760, 772, 10, NAVY)
    sp = "—" if n_read < 0 else f1(LV[n_read][1])
    st = "—" if n_read < 0 else str(LV[n_read][0])
    for cx, v, u in ((330, sp, "kPa"), (760, st, "°C")):
        card(d, (cx - 190, 270, cx + 190, 380), fill=SCREEN, r=16)
        text(d, (cx - 40, 325), v, 62, LCD, alpha=ka if n_read >= 0 else 1.0)
        text(d, (cx + 125, 325), u, FS, LCD)

# ---------------- do thi p - t ----------------
def graph(box, tmin, tmax, pmax):
    x0, y0, x1, y1 = box
    return (lambda tc: x0 + (tc - tmin) / (tmax - tmin) * (x1 - x0)), (lambda p: y1 - p / pmax * (y1 - y0))

def axes(d, X, Y, tmin, tmax, pmax, ticks=(-200, -100, 0, 100), ka=1.0, lab=True):
    d.line([(X(tmin), Y(0)), (X(tmax), Y(0))], fill=INK, width=4)
    d.line([(X(tmin), Y(0)), (X(tmin), Y(pmax))], fill=INK, width=4)
    for tc in ticks:
        d.line([(X(tc), Y(0) - 12), (X(tc), Y(0) + 12)], fill=INK, width=4)
        text(d, (X(tc), Y(0) + 48), str(tc).replace("-", "−"), FS, NOTE, alpha=ka)
    if lab:
        for pp in (50, 100, 150):
            d.line([(X(tmin) - 12, Y(pp)), (X(tmin) + 12, Y(pp))], fill=INK, width=4)
            text(d, (X(tmin) - 18, Y(pp)), str(pp), FS, NOTE, anchor="rm", alpha=ka)
        text(d, (X(tmin) + 20, Y(pmax) - 10), "p (kPa)", FS, NOTE, anchor="lm", alpha=ka)
        text(d, (X(tmax), Y(0) - 50), "t (°C)", FS, NOTE, anchor="rm", alpha=ka)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, t, 0, -1)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 960 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 180), "Kéo dài đồ thị p–t", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 280), "tới p = 0, cắt trục t ở đâu?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 420, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh (5 muc) ----------------
LT = tuple(0.3 + 1.4 * j for j in range(5))
def s_do(img, d, t, sc):
    IMG_REF[0] = img; ka = appear(t, 0.3, 0.3)
    n = 0
    for j, a in enumerate(LT):
        if t >= a: n = j
    rig(d, t, n, n, ka)
    card(d, (40, 890, 1040, 1585), fill=WHITE, outline=LIGHT, w=3)
    X, Y = graph((160, 980, 1000, 1460), -300, 110, 160)
    axes(d, X, Y, -300, 110, 160, ka=ka)
    for j in range(n + 1):
        r = 16 * appear(t, LT[j], 0.3)
        if r > 1: dot(d, X(LV[j][0]), Y(LV[j][1]), r, ORANGE, outline=WHITE)

# ---------------- canh 3: Dap an (keo dai) ----------------
def s_ket(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; ka = appear(t, 0.3, 0.3)
    card(d, (40, 250, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    X, Y = graph((160, 380, 1000, 1120), -300, 110, 160)
    axes(d, X, Y, -300, 110, 160, ka=ka)
    d.line([(X(0), Y(pmod(100, 0))), (X(108), Y(pmod(100, 108)))], fill=ORANGE, width=6)
    p = ease((t - 0.5) / 1.8); te = lerp(0, TCUT, p)
    if p > 0: dashed(d, (X(0), Y(100)), (X(te), Y(pmod(100, te))), DORANGE, w=6)
    for tc, pp in LV: dot(d, X(tc), Y(pp), 16, ORANGE, outline=WHITE)
    if p >= 1:
        rr = 26 + 10 * math.sin(t * 5)
        d.ellipse([X(TCUT) - rr, Y(0) - rr, X(TCUT) + rr, Y(0) + rr], outline=DGREEN, width=6)
        text(d, (X(TCUT) + 10, Y(0) - 120), "−273 °C", 64, DGREEN, anchor="lm")
        u = 0.5 + 0.5 * math.sin(t * 1.6)                 # cham truot doc doan keo dai (hinh khong dung yen)
        tu = lerp(TCUT, 0, u); dot(d, X(tu), Y(pmod(100, tu)), 22, A(DORANGE, 0.85))
    k2 = appear(t, M[1], 0.4)
    text(d, (X(-150), Y(115)), "ngoại suy", FS, DORANGE, alpha=k2)

# ---------------- canh 4: Rut ra (thang Kelvin) ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; ka = appear(t, 0.3, 0.3)
    card(d, (40, 250, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    yb, yt = 1430, 420
    Yc = lambda tc: lerp(yb, yt, (tc - TCUT) / (100 - TCUT))
    for x, u in ((330, "°C"), (750, "K")):
        d.rounded_rectangle([x - 26, yt - 30, x + 26, yb + 30], radius=26, fill=(236, 240, 246), outline=NAVY, width=4)
        text(d, (x, yt - 90), u, 66, NAVY, alpha=ka)
    v = lerp(TCUT, 100, 0.5 + 0.5 * math.sin(t * 1.3 - 1.4))
    t1 = M[1] - 1.0                                       # cot do ha dan ve 0 K truoc khi chip "0 K" bat
    if t >= t1:
        v1 = lerp(TCUT, 100, 0.5 + 0.5 * math.sin(t1 * 1.3 - 1.4))
        v = lerp(v1, TCUT + 8 + 8 * math.sin(t * 6), ease((t - t1) / 1.0))
    d.rectangle([330 - 12, Yc(v), 330 + 12, yb + 20], fill=RED); d.rectangle([750 - 12, Yc(v), 750 + 12, yb + 20], fill=RED)
    for tc, kv, col in ((100, 373, DORANGE), (0, 273, BLUE), (TCUT, 0, DGREEN)):
        y = Yc(tc)
        d.line([(300, y), (780, y)], fill=A(col, 0.5), width=3)
        text(d, (270, y), "−273" if tc == TCUT else str(tc), FS, col, anchor="rm", alpha=ka)
        text(d, (800, y), str(kv), FS, col, anchor="lm", alpha=ka)
    k2 = appear(t, M[1], 0.4)
    if k2 > 0:
        y = Yc(TCUT)
        rr = 14 * (0.5 + 0.5 * math.sin(t * 5))
        card(d, (420 - rr, y - 50 - rr, 660 + rr, y + 50 + rr), fill=A(mix(DGREEN, WHITE, 0.6), k2), r=40)
        card(d, (420, y - 50, 660, y + 50), fill=A(DGREEN, k2), r=26)
        text(d, (540, y), "0 K", 62, WHITE, alpha=k2)

# ---------------- canh 5: Bay (hai hinh canh nhau) ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; ka = appear(t, 0.3, 0.3)
    p = ease(((t % 3.0) - 0.2) / 1.6)
    for cx, lab, col, cuts in ((285, "Nếu đổi", DRED, (-130, -210, -290)), (795, "Đo thật", DGREEN, (TCUT,) * 3)):
        card(d, (cx - 245, 250, cx + 245, 1330), fill=WHITE, outline=col, w=6)
        text(d, (cx, 320), lab, 62, col, alpha=ka)
        X, Y = graph((cx - 210, 460, cx + 220, 1060), -300, 110, 230)
        d.line([(X(-300), Y(0)), (X(110), Y(0))], fill=INK, width=4)
        d.line([(X(0), Y(0) - 12), (X(0), Y(0) + 12)], fill=INK, width=4)
        text(d, (X(0), Y(0) + 48), "0", FS, NOTE, alpha=ka)
        for (p0, lc), tcut in zip(((80, BLUE), (100, ORANGE), (150, PURPLE)), cuts):
            f = lambda tc: p0 * (tc - tcut) / (0 - tcut)
            d.line([(X(0), Y(f(0))), (X(108), Y(f(108)))], fill=lc, width=6)
            te = lerp(0, tcut, p)
            if p > 0: dashed(d, (X(0), Y(f(0))), (X(te), Y(f(te))), lc, w=5)
        if cx == 795:
            d.line([(X(TCUT), Y(0) - 12), (X(TCUT), Y(0) + 12)], fill=INK, width=4)
            text(d, (X(TCUT) + 20, Y(0) + 48), "−273", FS, DGREEN, alpha=ka)
    text(d, (285, 1160), "mỗi khí", FS, DRED, alpha=ka)
    text(d, (285, 1240), "một điểm", FS, DRED, alpha=ka)
    k = appear(t, M[1], 0.4)
    text(d, (795, 1160), "cùng một", FS, DGREEN, alpha=k)
    text(d, (795, 1240), "điểm cắt", FS, DGREEN, alpha=k)

# ---------------- canh 6: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    for cx, tt, pp in ((270, "0 °C", "100,0 kPa"), (810, "273 °C", "? kPa")):
        card(d, (cx - 210, 420, cx + 210, 640), fill=A(SCREEN, k1), r=18)
        text(d, (cx, 480), tt, 62, LCD, alpha=k1)
        text(d, (cx, 575), pp, 62, LCD, alpha=k1)
    arrow(d, (500, 530), (580, 530), A(ORANGE, k1), w=8, head=24)
    for k in range(5):                                      # lua bep (hinh khong dung yen)
        h = 60 + 25 * math.sin(t * 7 + k * 1.3)
        x = 690 + k * 60
        d.polygon([(x - 22, 780), (x + 22, 780), (x, 780 - h)], fill=A(ORANGE, k1))
    d.rounded_rectangle([640, 780, 980, 806], radius=8, fill=A((234, 88, 12), k1))
    text(d, (W / 2, 1020), "Cùng bình, giữ thể tích:", 64, INK, alpha=k1)
    text(d, (W / 2, 1120), "p bằng bao nhiêu?", 66, DORANGE, alpha=k1)
    seg_bar(d, 1260, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, r, b, e = (sc[x] for x in ("hook", "do", "ket", "rut", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + a, "tap") for a in LT]
    out += [(k["t0"] + 2.3, "ding"), (r["t0"] + r["M"][1], "tap"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-thangnhietdo-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thang nhiệt độ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bình khí kín trong nồi nước", draw=s_hook, tail=0.3, caps=[
   ("Bình kín, thể tích không đổi.", 3.4),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Đo ở 5 mức nhiệt độ", draw=s_do, tail=0.4, caps=[
   ("Đo p ở 0, 25, 50, 75, 100 °C.", 3.8),
   ("Áp suất tăng đều theo nhiệt độ.", 3.8)]),
 dict(key="ket", title="Kéo dài đồ thị", draw=s_ket, tail=0.4, caps=[
   ("Đáp án: khoảng −273 °C.", 4.0),
   ("Khí thật hoá lỏng trước đó.", 3.6)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.4, caps=[
   ("Nhiệt độ thấp nhất có thể.", 3.8),
   ("Chọn làm gốc thang Kelvin.", 4.0)]),
 dict(key="bay", title="Bẫy: tuỳ lượng khí?", draw=s_bay, tail=0.4, caps=[
   ("Đổi lượng khí, điểm cắt có đổi?", 3.8),
   ("Không: chỉ độ dốc đổi.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự nghĩ.", 5.8)]),
])
