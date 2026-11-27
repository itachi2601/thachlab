# Clip: tn-l11-motadddh-02 - Doc li do tren thuoc, cham len do thi x-t (31/10/2026; dung lai 27/11/2026 theo cong moi:
#       --do-chu 0 LOI, chu >= 55 px, Du doan K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-motadddh-02.json (_kiem_so() doi chieu):
#   tham_so: A = 5 cm, T = 1 s, phi = 0 ; x_doc = round(5cos(2.pi.t), 1).
#   so_lieu_mau (t s, x doc cm): 0 5,0 ; 0,10 4,0 ; 0,20 1,5 ; 0,30 -1,5 ; 0,40 -4,0.
# DOI CA Du doan (27/11): ca cu "moi 0,10 s li do giam deu?" bi lo boi bang so ngay duoi video + dong "Nhin vao".
#   Ca moi: doc them o t = 0,50 s (chua co trong bang bai) -> x = -5,0 cm (T/2: bien am; tinh tu mo_hinh, ghi
#   "theo mo hinh"). Nhieu: 0 (tuong T/2 ve O), 5,0, -4,0 (chep moc truoc).
# Bay = hien_tuong_hay_sai[0]: lay so doc 4,0 cm (t = 0,10 s) lam bien do.
# Thu nghi (= cau_chot khung web): t = 0,05 s (chua doc) -> 5cos(0,1.pi) = 4,755 -> doc khoang 4,8 cm
#   (buoc chua chieu: thay t vao x = 5cos(2.pi.t) / do thi cong gan bien). Nhieu: 4,5 (noi suy thang), 5,0, 4,0. 4,8 khong hien.
from engine import *

ROWS = [(0.0, 5.0), (0.1, 4.0), (0.2, 1.5), (0.3, -1.5), (0.4, -4.0)]
EXTRA = (0.5, -5.0)                                     # theo mo hinh (Du doan)
AMP, PER = 5.0, 1.0
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
BLOCK = (59, 130, 246); HL = (255, 237, 213)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-motadddh-02.json")))
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["A"]["mac_dinh"] == AMP and ts["T"]["gia_tri"] == PER
    assert [(r[0], r[2]) for r in k["so_lieu_mau"]["hang"]] == ROWS
    assert round(AMP * math.cos(2 * math.pi * EXTRA[0] / PER), 1) == EXTRA[1]
    assert round(AMP * math.cos(2 * math.pi * 0.05 / PER), 1) == 4.8
_kiem_so()

def xof(tp): return AMP * math.cos(2 * math.pi * tp / PER)
def vn(v, nd=1):
    s = f"{abs(v):.{nd}f}".replace(".", ",")
    return ("−" if v < -1e-9 else "") + s
def vt(tp): return "0" if tp == 0 else vn(tp, 2)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.8, cx + pw / 2, cy + size * 0.8), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem lien khoi, tat lan luot tu PHAI sang TRAI; cao 76 px."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); wseg = 820 / n
    for i in range(n):
        x = 130 + i * wseg
        if i < on: card(d, (x, y, x + wseg - 14, y + 76), fill=A(col, a), r=16)
        else: card(d, (x, y, x + wseg - 14, y + 76), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

# ---------------- ray ngang + thuoc (khung nguon 1080x1920) ----------------
RX0, RS = 560, 80            # x = 0 o px 560 ; 80 px/cm -> -5..5 o 160..960
TRACK = 400
def rx(x): return RX0 + x * RS

def spring(d, x0, x1, y, n=11, amp=20, col=NAVY):
    pts = [(x0, y), (x0 + 16, y)]
    L = (x1 - 16) - (x0 + 16)
    for i in range(1, 2 * n):
        pts.append((x0 + 16 + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(x1 - 16, y), (x1, y)]
    d.line(pts, fill=col, width=4, joint="curve")

def rig(d, x, y_off=0):
    T_ = TRACK + y_off
    d.rectangle([40, T_ - 120, 62, T_ + 4], fill=GRAY, outline=NAVY, width=3)
    d.line([(40, T_ + 4), (1040, T_ + 4)], fill=NAVY, width=5)
    cx = rx(x)
    spring(d, 62, cx - 40, T_ - 45)
    card(d, (cx - 40, T_ - 90, cx + 40, T_), fill=BLOCK, outline=NAVY, r=10, w=3)
    d.rectangle([rx(-5) - 14, T_ + 16, rx(5) + 14, T_ + 56], fill=(250, 240, 200), outline=NAVY, width=2)
    for k in range(-50, 51):
        X = rx(k / 10); L = 26 if k % 10 == 0 else (16 if k % 5 == 0 else 8)
        d.line([(X, T_ + 16), (X, T_ + 16 + L)], fill=NAVY, width=3 if L >= 26 else 2)
    for c in (-5, 0, 5):
        text(d, (rx(c), T_ + 96), vn(c, 0), 56, NAVY)
    text(d, (rx(5) + 44, T_ + 96), "cm", 56, NAVY, anchor="lm")
    d.line([(cx, T_ - 70), (cx, T_ + 54)], fill=RED, width=5)

# ---------------- do thi x-t ----------------
GX0, GSX, GSC = 170, 1640, 44          # t = 0 o px 170 ; 0,10 s = 164 px ; 44 px/cm
def gx(tp): return GX0 + tp * GSX
def gyf(gy): return lambda x: gy - x * GSC

def graph(d, gy, tp_end=None, pts=(), hl=None, tmax=0.5):
    Y = gyf(gy); top, bot = Y(5) - 50, Y(-5) + 30
    for k in range(1, int(tmax * 10 + 0.01) + 1):
        for yy in range(int(top + 30), int(bot), 26): d.line([(gx(k / 10), yy), (gx(k / 10), yy + 12)], fill=LIGHT, width=3)
    arrow(d, (GX0, bot), (GX0, top), NAVY, w=4, head=18)
    arrow(d, (GX0, Y(0)), (gx(tmax + 0.04), Y(0)), NAVY, w=4, head=18)
    text(d, (GX0 + 22, top - 2), "x (cm)", 56, INK, anchor="lm")
    for xv in (5, -5):
        text(d, (GX0 - 16, Y(xv)), vn(xv, 0), 56, NAVY, anchor="rm")
        for xx in range(GX0, int(gx(tmax + 0.02)), 26): d.line([(xx, Y(xv)), (xx + 12, Y(xv))], fill=LIGHT, width=3)
    for k in ((1, 2) if tmax <= 0.2 else (2, 4)):
        text(d, (gx(k / 10), bot + 44), vn(k / 10, 1), 56, NAVY)
    text(d, (gx(tmax + 0.04), Y(0) + 46), "t (s)", 56, INK, anchor="rm")
    if tp_end is not None and tp_end > 0:
        n = max(2, int(tp_end * 400))
        d.line([(gx(tp_end * i / n), Y(xof(tp_end * i / n))) for i in range(n + 1)], fill=TEAL, width=6, joint="curve")
    for i, (tp, xd) in enumerate(pts):
        dot(d, gx(tp), Y(xd), 14, ORANGE if hl == i else NAVY, outline=WHITE)

# ---------------- bang t / x doc nam ngang ----------------
ALL = ROWS + [EXTRA]
def table_row(d, y0, n, cur=None, qlast=False):
    card(d, (30, y0, 1050, y0 + 210), fill=WHITE, outline=NAVY, r=20, w=3)
    d.line([(30, y0 + 105), (1050, y0 + 105)], fill=LIGHT, width=3)
    text(d, (110, y0 + 52), "t", 56, INK); text(d, (110, y0 + 157), "x", 56, INK)
    for i in range(6):
        cx = 222 + i * 148
        if cur == i: card(d, (cx - 74, y0 + 8, cx + 74, y0 + 202), fill=HL, r=14)
        text(d, (cx, y0 + 52), vt(ALL[i][0]), 56, INK)
        if i < n: text(d, (cx, y0 + 157), vn(ALL[i][1]), 56, DORANGE if i == 5 else NAVY)
        elif qlast and i == 5: text(d, (cx, y0 + 157), "?", 60, PURPLE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = ease((t - 0.4) / 1.2)
    rig(d, AMP * k)
    table_row(d, 600, 1 if t > 1.6 else 0, qlast=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 64, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 180), "Thả từ biên, T = 1,00 s.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "Ở t = 0,50 s,", 62, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 365), "thước chỉ bao nhiêu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 470, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh (quay cham x10, dung o moi moc 0,10 s) ----------------
D0, HOLD, MOVE = 0.4, 0.5, 1.0
def phase(t):
    if t < D0: return 0.0, None
    u = t - D0
    for i in range(6):
        if u < HOLD: return ALL[i][0], i
        u -= HOLD
        if i == 5: return ALL[5][0], 5
        if u < MOVE: return ALL[i][0] + 0.1 * u / MOVE, None
        u -= MOVE
    return ALL[5][0], 5
def n_read(t):
    if t < D0: return 0
    return min(6, 1 + int((t - D0) // (HOLD + MOVE)))

def s_do(img, d, t, sc):
    tp, i = phase(t); n = n_read(t)
    rig(d, xof(tp))
    pill(d, 780, 592, f"t = {vn(tp, 2)} s", 56, WHITE, NAVY)
    pill(d, 230, 592, "chậm ×10", 56, WHITE, ORANGE)
    graph(d, 960, tp_end=tp, pts=ALL[:n], hl=i)
    table_row(d, 1290, n, cur=i)
    kt = appear(t, D0 + 5 * (HOLD + MOVE) + 0.6, 0.4)
    if kt > 0: text(d, (W / 2, 1560), "ô cam: theo mô hình", 56, DORANGE, alpha=kt)

# ---------------- canh 3: Ket qua + rut ra + chua noi duoc ----------------
GYA = 640
def s_dapan(img, d, t, sc):
    M = sc["M"]
    tp = min(0.5, t / 4.0)                              # ve lai duong cong cham
    graph(d, GYA, tp_end=tp, pts=[p for p in ALL if p[0] <= tp + 1e-9], hl=5 if tp >= 0.5 else None)
    Y = gyf(GYA)
    kb = appear(t, 0.5, 0.4)
    if kb > 0:
        card(d, (60, 990, 1020, 1110), fill=A((255, 247, 237), kb), outline=A(ORANGE, kb), r=24, w=5)
        text(d, (W / 2, 1050), "t = 0,50 s = T/2: x = −5,0 cm", 58, DORANGE, alpha=kb)
    kr = appear(t, M[1] - 0.05, 0.45)
    if kr > 0:
        card(d, (60, 1140, 1020, 1260), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=5)
        text(d, (W / 2, 1200), "Nửa chu kì: sang biên kia", 58, DGREEN, alpha=kr)
    kn = appear(t, M[2] - 0.05, 0.45)
    if kn > 0:
        card(d, (60, 1290, 1020, 1580), fill=A(WHITE, kn), outline=A(NAVY, kn), r=24, w=5)
        text(d, (W / 2, 1345), "Chưa nói được", 60, NAVY, alpha=kn)
        text(d, (100, 1430), "• Thước chỉ chia 0,1 cm", 58, INK, anchor="lm", alpha=kn)
        text(d, (100, 1515), "• Bấm giờ lệch: chưa xét", 58, INK, anchor="lm", alpha=appear(t, M[2] + 2.5, 0.4))

# ---------------- canh 4: Bay (lay so doc lam bien do) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    tp = (t / 6.0) % 0.5                                # cham chay doc duong cong (khong dung hinh)
    graph(d, GYA, tp_end=0.5, pts=ROWS, hl=1)
    Y = gyf(GYA)
    dot(d, gx(tp), Y(xof(tp)), 16, TEAL, outline=WHITE)
    text(d, (gx(0.1) + 24, Y(4.0) - 40), "4,0", 58, DORANGE, anchor="lm")
    y0 = 1000
    card(d, (40, y0, 1040, y0 + 150), fill=(254, 242, 242), outline=DRED, r=24, w=5)
    text(d, (W / 2, y0 + 75), "✗ Số đọc 4,0 cm là A", 60, DRED)
    kd = appear(t, M[1] - 0.1, 0.4)
    if kd > 0:
        arrow(d, (GX0 - 70, Y(0)), (GX0 - 70, Y(5) + 4), A(DGREEN, kd), w=7, head=20)
        text(d, (GX0 - 86, (Y(0) + Y(5)) / 2), "A", 60, DGREEN, anchor="rm", alpha=kd)
        card(d, (40, y0 + 190, 1040, y0 + 340), fill=A((236, 253, 243), kd), outline=A(GREEN, kd), r=24, w=5)
        text(d, (W / 2, y0 + 265), "✓ A = 5,0 cm: lệch lớn nhất", 60, DGREEN, alpha=kd)

# ---------------- canh 5: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    if t < 0.15: return
    card(d, (40, 215, 1040, 1585), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, 280, "THỬ NGHĨ", 56, WHITE, ORANGE)
    gy = 700
    graph(d, gy, pts=ROWS[:2], tmax=0.2)
    Y = gyf(gy)
    text(d, (gx(0.1) + 24, Y(4.0) - 40), "4,0", 58, NAVY, anchor="lm")
    text(d, (gx(0.05), Y(0) - 60), "?", 64, PURPLE)
    for yy in range(int(Y(5) - 10), int(Y(0)), 24): d.line([(gx(0.05), yy), (gx(0.05), yy + 12)], fill=PURPLE, width=4)
    text(d, (W / 2, 1110), "Ở t = 0,05 s (chưa đọc),", 62, DORANGE)
    text(d, (W / 2, 1195), "thước chỉ khoảng bao nhiêu?", 62, DORANGE)
    seg_bar(d, 1340, t, 0.8, sc["T"] - 0.2, ORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + D0 + i * (HOLD + MOVE), "tap") for i in range(1, 6)]
    out += [(da["t0"] + 0.5, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-motadddh-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Mô tả dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đọc li độ trên thước", draw=s_hook, tail=0.3, caps=[
   ("Thả từ 5,0 cm, đọc mỗi 0,10 s.", 4.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Dừng hình ở mỗi mốc để đọc.", 4.4),
   ("Mỗi số đọc là một chấm.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Chấm nằm trên đường côsin.", 4.0),
   ("Từ biên dương sang biên âm.", 4.4),
   ("Ô cuối là số theo mô hình.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Bẫy: lấy số đọc làm biên độ.", 3.6),
   ("Biên độ là li độ lớn nhất.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])
