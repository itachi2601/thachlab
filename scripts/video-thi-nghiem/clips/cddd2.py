# Clip: tn-l11-cuong-do-dong-dien-02 - Do dien luong sac vao dien thoai bang dong ho USB (ban 2 cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-cuong-do-dong-dien-02.json (ghi_chu "khong phai so do that"
#   -> nhan "số liệu mô phỏng"): so_lieu_mau (phut, mAh, C): 10 250 900 ; 20 500 1800 ; ... ; 50 1250 4500.
#   I = 1,50 A dao dong +-0,02 A ; 1 mAh = 3,6 C (rut_ra).
# Du doan (khung, K10 khong nut): ve so mAh theo thoi gian sac, 5 diem nam tren duong nao? -> thang qua goc.
#   (Doi ca so ban cu "mAh thay doi the nao" vi hop exp in san "moi 10 phut them 250 mAh".)
# KHONG LO "Bam xem" cua bai (+-0,02 A -> +-12 C): clip khong ve sai so, khong chieu so 12.
# Bay (hien_tuong_hay_sai[1]): nhan I voi so phut: 1,50 . 10 = 15 C (sai) | 1,50 . 600 = 900 C (dung).
# Cau chot (tu suy trong dai tham_so I 0,5..3,0 A, dt 0..60 phut): 0,80 A trong 15 phut ->
#   dq = 0,8 . 900 = 720 C -> 720 / 3,6 = 200 mAh. So 200 va 720 khong hien trong clip.
#   Nhieu: 720 (quen doi C ra mAh), 375 (250.15/10, bo qua dong), 3,3 (0,8.15 = 12 C nhan so phut).
# Mach: cuc sac -> dong ho USB (noi tiep tren day sac) -> dien thoai.
from engine import *

ROWS = [(10, 250, 900), (20, 500, 1800), (30, 750, 2700), (40, 1000, 3600), (50, 1250, 4500)]   # so_lieu_mau
I0 = 1.50
assert all(abs(I0 * m * 60 - c) < 1e-6 and abs(c / 3.6 - q) < 1e-6 for m, q, c in ROWS)
assert abs(0.8 * 15 * 60 / 3.6 - 200) < 1e-9
FLICK = [1.50, 1.51, 1.50, 1.49, 1.50, 1.52, 1.50, 1.48]    # dao dong trong +-0,02 A
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DRED = (185, 28, 28); DGREEN = (21, 110, 55); EMPTY = (148, 140, 128)
SCRB = (18, 26, 40); AMP_C = (250, 204, 21); MAH_C = (110, 231, 183); ARR = (194, 65, 12)

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

def mm_ss(s): s = int(round(s)); return f"{s // 60:02d}:{s % 60:02d}"

# ---------------- dung cu ----------------
def devices(d, sim=0.0, amp=I0, charging=False, mah=None, clock=None):
    """Cuc sac -> dong ho USB -> dien thoai; dong ho bam gio ben duoi. sim = giay da sac (mo hinh)."""
    if mah is None: mah = int(round(sim * I0 / 3.6))
    d.line([(230, 500), (300, 500)], fill=NAVY, width=10)
    d.line([(740, 500), (830, 500)], fill=NAVY, width=10)
    for yy in (450, 550): d.rectangle([28, yy - 9, 60, yy + 9], fill=GRAY)
    card(d, (60, 390, 230, 610), fill=WHITE, outline=NAVY, r=26, w=5)
    d.rectangle([215, 480, 236, 520], fill=NAVY)
    text(d, (145, 660), "cục sạc", 56, INK)
    card(d, (300, 330, 740, 670), fill=(48, 56, 78), r=30)
    card(d, (326, 356, 714, 644), fill=SCRB, r=18)
    text(d, (520, 432), vn(amp) + " A", 64, AMP_C)
    text(d, (520, 562), f"{mah} mAh", 64, MAH_C)
    text(d, (520, 720), "đồng hồ USB", 56, INK)
    if charging:
        for x0, x1 in ((236, 298), (744, 828)):
            arrow(d, (x0, 450), (x1, 450), ARR, w=10, head=26)
    card(d, (830, 300, 1030, 760), fill=NAVY, r=34)
    card(d, (846, 336, 1014, 724), fill=(226, 232, 240), r=18)
    bx0, by0, bx1, by1 = 892, 430, 968, 640
    d.rectangle([915, by0 - 16, 945, by0], fill=NAVY)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=NAVY, width=6)
    fill = 0.08 + mah / 2500
    d.rectangle([bx0 + 10, by1 - 10 - (by1 - by0 - 20) * fill, bx1 - 10, by1 - 10], fill=GREEN)
    text(d, (930, 805), "điện thoại", 56, INK)
    card(d, (300, 770, 740, 900), fill=WHITE, outline=NAVY, r=24, w=4)
    dot(d, 380, 835, 40, WHITE, outline=NAVY); d.rectangle([372, 783, 388, 793], fill=NAVY)
    a = -math.pi / 2 + 2 * math.pi * (sim % 600) / 600
    d.line([(380, 835), (380 + 30 * math.cos(a), 835 + 30 * math.sin(a))], fill=RED, width=5)
    text(d, (580, 835), clock if clock else mm_ss(sim), 60, INK)

def table(d, n, y=960, hl=None):
    card(d, (140, y, 940, y + 110 + 80 * 5), fill=WHITE, outline=NAVY, w=4)
    xs = (330, 700)
    for x, c in zip(xs, ("t (phút)", "đồng hồ (mAh)")): text(d, (x, y + 55), c, 56, INK)
    d.line([(170, y + 100), (910, y + 100)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 145 + i * 80; m, q, c = ROWS[i]
        if hl == i: d.rounded_rectangle([160, yy - 37, 920, yy + 37], radius=18, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(m), 58, INK); text(d, (xs[1], yy), str(q), 58, INK)

def axes(d, x0, y0, x1, y1, xmax, ymax, a=1.0, ticks=(10, 20, 30, 40, 50), ly="mAh", lx="phút"):
    gx = lambda u: x0 + u / xmax * (x1 - x0); gy = lambda q: y0 - q / ymax * (y0 - y1)
    c = A(NAVY, a)
    d.line([(x0, y1 - 20), (x0, y0)], fill=c, width=5); d.line([(x0, y0), (x1 + 20, y0)], fill=c, width=5)
    arrow(d, (x0, y1 - 10), (x0, y1 - 36), c, w=5, head=18); arrow(d, (x1 + 10, y0), (x1 + 36, y0), c, w=5, head=18)
    text(d, (x0 + 25, y1 - 30), ly, 56, INK, anchor="lm", alpha=a)
    text(d, (x1 + 30, y0 - 50), lx, 56, INK, anchor="rm", alpha=a)
    for u in ticks:
        d.line([(gx(u), y0), (gx(u), y0 + 12)], fill=c, width=4); text(d, (gx(u), y0 + 48), str(u), 56, INK, alpha=a)
    return gx, gy

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    devices(d)
    a = appear(t, M[1] - 0.2, 0.4)
    if a <= 0: return
    y0 = 940 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 650), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Vẽ mAh theo thời gian:", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 260), "năm điểm trên đường nào?", 60, PURPLE, alpha=a)
    axes(d, 400, y0 + 520, 680, y0 + 390, 10, 10, a=a, ticks=(), lx="t (phút)")
    seg_bar(d, y0 + 555, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
S0, S1 = 0.8, 3.6        # 10 phut dau: 0 -> 600 s trong [S0, S1]
FF0, FFW = 0.2, 1.5      # tua nhanh: doan j bat dau M[1] + FF0 + (j-1).FFW

def sim_s(t, M):
    if t < M[1] + FF0: return 600 * clamp((t - S0) / (S1 - S0))
    return 600 + 2400 * clamp((t - M[1] - FF0) / (4 * FFW))

def s_do(img, d, t, sc):
    M = sc["M"]
    s = sim_s(t, M)
    charging = (S0 <= t < S1) or (M[1] + FF0 <= t < M[1] + FF0 + 4 * FFW)
    amp = FLICK[int(t * 2.5) % len(FLICK)] if charging else I0
    devices(d, s, amp, charging)
    table(d, min(5, int(s / 600 + 1e-6)))
    pill(d, 900, 245, "tua nhanh", ORANGE, appear(t, M[1], 0.25), size=56)

# ---------------- canh 3: Ket qua ----------------
GX0, GY0, GX1, GY1 = 200, 860, 900, 380

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1010, 300), "số liệu mô phỏng", 56, (60, 64, 84), anchor="rm")
    gx, gy = axes(d, GX0, GY0, GX1, GY1, 55, 1400, ly="mAh", lx="t (phút)")
    for q in (500, 1000):
        d.line([(GX0 - 12, gy(q)), (GX0, gy(q))], fill=NAVY, width=4)
        text(d, (GX0 - 18, gy(q)), str(q), 56, INK, anchor="rm")
    for i, (m, q, c) in enumerate(ROWS):
        k = appear(t, 0.3 + 0.15 * i, 0.3)
        if k > 0: dot(d, gx(m), gy(q), 16, A(BLUE, k), outline=WHITE)
    kl = appear(t, 1.6, 0.9)
    if kl > 0:
        m1 = 53 * kl
        d.line([(gx(0), gy(0)), (gx(m1), gy(25 * m1))], fill=A(GREEN, 0.9), width=6)
    ka = appear(t, 2.4, 0.4)
    if ka > 0:
        card(d, (40, 1030, 1040, 1190), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
        text(d, (W / 2, 1110), "Thẳng, đi qua gốc toạ độ", 64, NAVY, alpha=ka)
    k2 = appear(t, M[1] + 0.4, 0.4)
    if k2 > 0:
        d.ellipse([gx(10) - 34, gy(250) - 34, gx(10) + 34, gy(250) + 34], outline=A(ORANGE, k2), width=7)
        card(d, (40, 1230, 1040, 1530), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1310), "1 mAh = 3,6 C", 62, DGREEN, alpha=k2)
        text(d, (W / 2, 1430), "250 mAh = 900 C", 62, DGREEN, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    pill(d, W / 2, 290, "BẪY", DRED, k0)
    text(d, (W / 2, 410), "Dòng 1,50 A trong 10 phút", 60, INK, alpha=k0)
    card(d, (60, 480, 1020, 640), fill=A((254, 242, 242), k0), outline=A(DRED, k0), r=24, w=5)
    text(d, (470, 560), "1,50 · 10 = 15 C", 64, DRED, alpha=k0)
    text(d, (900, 560), "✗", 100, DRED, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 > 0:
        card(d, (60, 680, 1020, 840), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=5)
        text(d, (470, 760), "1,50 · 600 = 900 C", 64, DGREEN, alpha=k1)
        text(d, (900, 760), "✓", 100, DGREEN, alpha=k1)
    k3 = appear(t, M[2] - 0.4, 0.4)
    if k3 > 0:
        card(d, (40, 960, 1040, 1300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1030, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1180), "Gần đầy pin, dòng còn 1,50 A?", 60, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    card(d, (300, 400, 780, 720), fill=A((48, 56, 78), k), r=30)
    card(d, (326, 426, 754, 694), fill=A(SCRB, k), r=18)
    text(d, (540, 500), "0,80 A", 64, AMP_C, alpha=k)
    text(d, (540, 620), "? mAh", 64, MAH_C, alpha=k)
    card(d, (300, 760, 780, 880), fill=A(WHITE, k), outline=A(NAVY, k), r=24, w=4)
    text(d, (540, 820), "sạc 15:00", 60, INK, alpha=k)
    text(d, (W / 2, 1030), "Sạc 0,80 A trong 15 phút.", 62, INK, alpha=k)
    text(d, (W / 2, 1130), "Đồng hồ thêm bao nhiêu mAh?", 62, DRED, alpha=k)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + S1, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(1, 5)]
    out += [(da["t0"] + 2.4, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-cuong-do-dong-dien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Cường độ dòng điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Sạc điện thoại qua đồng hồ USB", draw=s_hook, tail=0.3, caps=[
   ("Dòng sạc giữ 1,50 A.", 3.2),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Sạc 10 phút, ghi số mAh.", 4.0),
   ("Ghi tiếp ở 20, 30, 40, 50 phút.", 6.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Năm điểm và gốc thẳng hàng.", 4.0),
   ("Đổi đơn vị sang cu-lông.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: nhân với số phút.", 3.6),
   ("10 phút là 600 giây.", 3.6),
   ("Mới đo lúc pin còn vơi.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự trả lời.", 7.2)]),
])
