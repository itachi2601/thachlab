# Clip: tn-l10-cong-suat-01 - Leo cau thang bon lan, moi lan nhanh hon (31/10/2026;
# dung lai 27/11/2026 theo cong moi L10b: chu >= 55 px khi ve, K10 khong nut A-D, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-cong-suat-01.json (_kiem_so() doi chieu):
#   tham_so: m = 50 kg, h = 3,0 m, g = 10 m/s2, t 3,0..15,0 s ; so_lieu_mau t 12,0/8,5/6,0/4,0 s,
#   P 125/176/250/375 W ; ghi_chu A = 1500 J.
# Du doan (giu, = "Nhin vao" cua hop bai): lan 4 leo nhanh hon lan 1 -> P gap may lan? -> 3 lan.
#   Khung: A nhu nhau ; B khoang 3 lan (DUNG) ; C khoang 9 lan ; D khoang 1/3.
# Ket qua: bang t, P 4 lan (bang cua bai) ; A = mgh = 1500 J nhu nhau ; P = A/t.
# Bay = hien_tuong_hay_sai[0]: "leo nhanh thi cong lon hon" -> hai lan cung A = 1500 J.
#   Chua noi duoc: nang luong co the ton that (gia_thiet: chi tinh cong nang nguoi).
# Cau chot (t trong mien 3..15 s): lan moi P = 120 W -> t = 1500/120 = 12,5 s ; buoc doi ve t = A/P chua chieu,
#   12,5 khong hien tren man. (Khong dung 300 W cua ban cu: trung phuong an B Tu kiem tra Cau 1.)
from engine import *

ROWS = [(1, 12.0, 125), (2, 8.5, 176), (3, 6.0, 250), (4, 4.0, 375)]   # so_lieu_mau
A_J = 1500
CHOT_P = 120
SPEED = 5.0          # tua nhanh 5 lan
GAP = 0.3
NST = 10
def f1(x): return f"{x:.1f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-cong-suat-01.json")))
    for r, h in zip(ROWS, k["so_lieu_mau"]["hang"]): assert list(r) == h, ("lech kho", r)
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert (ts["m"]["gia_tri"], ts["h"]["gia_tri"], ts["g"]["gia_tri"]) == (50, 3.0, 10)
    assert "1500 J" in k["so_lieu_mau"]["ghi_chu"] and A_J == 50 * 10 * 3
    assert ts["t"]["min"] <= A_J / CHOT_P <= ts["t"]["max"] and A_J / CHOT_P == 12.5
    for n, t, P in ROWS: assert round(A_J / t) == P
_kiem_so()

STONE = (214, 206, 192); STONE_D = (150, 140, 124)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); DRED = (185, 28, 28); EMPTY = (148, 140, 128)

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

# ---------------- cau thang + nguoi ----------------
def stairs(d, x0, yb, w, h, n=NST, alpha=1.0, label=True):
    sw, sh = w / n, h / n
    d.line([(x0 - 80, yb), (x0 + w + 30, yb)], fill=A(INK, alpha), width=4)
    pts = [(x0, yb)]
    for i in range(n):
        pts += [(x0 + i * sw, yb - (i + 1) * sh), (x0 + (i + 1) * sw, yb - (i + 1) * sh)]
    pts += [(x0 + w, yb)]
    d.polygon(pts, fill=A(STONE, alpha))
    d.line(pts[:-1], fill=A(STONE_D, alpha), width=4)
    if label:
        xa = x0 + w + 55
        arrow(d, (xa, yb - h / 2), (xa, yb - h + 2), A(NAVY, alpha), w=5, head=18)
        arrow(d, (xa, yb - h / 2), (xa, yb - 2), A(NAVY, alpha), w=5, head=18)
        d.line([(x0 + w + 10, yb - h), (xa + 20, yb - h)], fill=A(NAVY, alpha), width=3)

def person(d, x, yf, s=1.0, alpha=1.0, col=ORANGE):
    lw = int(9 * s)
    d.line([(x - 12 * s, yf), (x, yf - 45 * s), (x + 12 * s, yf)], fill=A(NAVY, alpha), width=lw, joint="curve")
    d.rounded_rectangle([x - 20 * s, yf - 105 * s, x + 20 * s, yf - 40 * s], radius=int(14 * s), fill=A(col, alpha))
    dot(d, x, yf - 128 * s, 21 * s, A((240, 196, 150), alpha))

def person_on(d, x0, yb, w, h, p, s=1.0, alpha=1.0):
    sw, sh = w / NST, h / NST
    i = int(round(p * NST)) - 1
    if i < 0: person(d, x0 - 40, yb, s, alpha); return
    person(d, x0 + (i + 0.5) * sw, yb - (i + 1) * sh, s, alpha)

SX0, SYB, SW, SH = 330, 870, 480, 400
def scene_stairs(d, p):
    card(d, (40, 265, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    stairs(d, SX0, SYB, SW, SH)
    text(d, (SX0 + SW + 85, SYB - SH / 2 - 40), "h =", 56, NAVY, anchor="lm")
    text(d, (SX0 + SW + 85, SYB - SH / 2 + 30), "3,0 m", 56, NAVY, anchor="lm")
    person_on(d, SX0, SYB, SW, SH, p)
    text(d, (190, SYB - 190), "m = 50 kg", 56, ORANGE)

def tcard(d, y, lab, val):
    card(d, (70, y, 450, y + 86), fill=(255, 247, 237), outline=ORANGE, r=22, w=3)
    text(d, (100, y + 43), lab, 56, INK, anchor="lm")
    text(d, (425, y + 43), val, 56, NAVY, anchor="rm")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene_stairs(d, 0.0)
    tcard(d, 300, "Lần 1", "12,0 s"); tcard(d, 400, "Lần 4", "4,0 s")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 965 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Công suất lần 4", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "gấp mấy lần lần 1?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
RS = 0.6
def schedule():
    out, s = [], RS
    for _, tt, _ in ROWS:
        out.append((s, s + tt / SPEED, tt)); s += tt / SPEED + GAP
    return out
SCHED = schedule()
def state(t):
    cur, p, clk, done = 0, 0.0, 0.0, 0
    for i, (a, b, tt) in enumerate(SCHED):
        if t >= a:
            cur = i; clk = min(tt, (t - a) * SPEED); p = clk / tt
            if t >= b: done = i + 1
    return cur, p, clk, done

XS = (210, 520, 840)
def table(d, ty, n_t, pk=None, hl=()):
    card(d, (40, ty, 1040, ty + 560), fill=WHITE, outline=LIGHT, w=3)
    for x, s, col in zip(XS, ("Lần", "t (s)", "P (W)"), (INK, NAVY, ORANGE)):
        if s != "P (W)" or pk is not None: text(d, (x, ty + 60), s, 58, col)
    d.line([(70, ty + 110), (1010, ty + 110)], fill=LIGHT, width=3)
    for j, (n, tt, P) in enumerate(ROWS):
        yy = ty + 175 + j * 100
        if j in hl: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=(255, 247, 237))
        if j < n_t:
            text(d, (XS[0], yy), str(n), 58, INK)
            text(d, (XS[1], yy), f1(tt), 58, NAVY)
        if pk is not None and pk(j) > 0: text(d, (XS[2], yy), str(P), 58, ORANGE, alpha=pk(j))

def s_do(img, d, t, sc):
    cur, p, clk, done = state(t)
    scene_stairs(d, p)
    card(d, (70, 300, 450, 470), fill=NAVY, r=22)
    text(d, (260, 340), "đồng hồ (s)", 56, WHITE)
    text(d, (260, 420), f1(clk), 60, YELLOW)
    text(d, (W / 2, 975), "tua nhanh ×5", 56, NOTE)
    table(d, 1030, done)

# ---------------- canh 3: Ket qua ----------------
def s_kq(img, d, t, sc):
    M = sc["M"]
    kh = appear(t, 0.9, 0.4)
    table(d, 265, 4, pk=lambda j: appear(t, 0.2 + 0.15 * j, 0.4), hl=(0, 3) if kh > 0.5 else ())
    if kh > 0:
        x = XS[2] + 110; y1, y4 = 265 + 175, 265 + 175 + 300
        arrow(d, (x, y1 + 20), (x, y4 - 20), A(ORANGE, kh), w=6, head=20)
        text(d, (x + 30, (y1 + y4) / 2), "×3", 60, ORANGE, anchor="lm", alpha=kh)
    ka = appear(t, M[1] - 0.1, 0.45)
    if ka > 0:
        card(d, (40, 860, 1040, 1200), fill=A(WHITE, ka), outline=A(NAVY, ka), w=5)
        text(d, (W / 2, 940), "A = m·g·h", 62, INK, alpha=ka)
        text(d, (W / 2, 1035), "= 50·10·3,0 = 1500 J", 62, DGREEN, alpha=ka)
        text(d, (W / 2, 1130), "như nhau cả bốn lần", 56, NOTE, alpha=ka)
    kb = appear(t, M[2] - 0.1, 0.45)
    if kb > 0:
        card(d, (40, 1240, 1040, 1480), fill=A((236, 253, 243), kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, 1320), "P = A / t", 72, DGREEN, alpha=kb)
        text(d, (W / 2, 1420), "t ngắn hơn, P lớn hơn", 56, INK, alpha=kb)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def mini(d, cx, yb, lab, tt, alpha=1.0):
    x0, w, h = cx - 150, 270, 230
    stairs(d, x0, yb, w, h, alpha=alpha, label=False)
    person_on(d, x0, yb, w, h, 1.0, s=0.7, alpha=alpha)
    text(d, (cx, yb - h - 120), f"{lab} {tt}", 56, INK, alpha=alpha)
    text(d, (cx, yb + 60), "A = 1500 J", 56, DGREEN, alpha=alpha)

def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q = "“Leo nhanh thì công lớn hơn”"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(60)); yy = 470
    text(d, (W / 2, yy), q, 60, mix(INK, DRED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0:
        card(d, (40, 640, 1040, 1230), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
        mini(d, 290, 1060, "Lần 1:", "12,0 s", kk); mini(d, 790, 1060, "Lần 4:", "4,0 s", kk)
        d.line([(540, 680), (540, 1120)], fill=A(LIGHT, kk), width=3)
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1270 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 200), "năng lượng cơ thể tốn thật", 60, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: t = 12,5 s) ----------------
def s_end(img, d, t, sc):
    scene_stairs(d, 1.0)
    y0 = 965
    card(d, (40, y0, 1040, 1665), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, y0 + 70, "THỬ NGHĨ", ORANGE)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, y0 + 195), "Lần mới: P = 120 W.", 60, INK, alpha=k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, y0 + 300), "Leo hết bao nhiêu giây?", 62, ORANGE, alpha=k2)
    seg_bar(d, y0 + 370, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, y0 + 475, 990, y0 + 680), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, y0 + 530), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, y0 + 620), "tính công A trước", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for a, bb, _ in SCHED: out += [(do["t0"] + a, "tap"), (do["t0"] + bb, "tap")]
    out += [(kq["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]
    return out

CLIP = dict(id="tn-l10-cong-suat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Công suất · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Leo cầu thang bốn lần", draw=s_hook, tail=0.3, caps=[
   ("Cùng người, cùng cầu thang.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.9, caps=[
   ("Bạn khác bấm giờ.", 3.4),
   ("Leo nhanh dần, bốn lần.", 3.4)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.3, caps=[
   ("Đáp án: gấp 3 lần.", 3.4),
   ("Công nâng người không đổi.", 3.4),
   ("Chỉ t đổi.", 3.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Sai: công như nhau, chỉ P khác.", 4.0),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Lần leo mới.", 2.8),
   ("Dừng lại, tự tính.", 6.6)]),
])
