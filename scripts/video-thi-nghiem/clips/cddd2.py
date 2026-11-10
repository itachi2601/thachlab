# Clip: tn-l11-cuong-do-dong-dien-02 - Do dien luong sac vao dien thoai bang dong ho USB o dong khong doi (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-cuong-do-dong-dien-02.json (ghi_chu: "Tinh tu mo hinh voi I = 1,50 A;
#   khong phai so do that" -> nhan "số liệu mô phỏng"):
#   so_lieu_mau (dt phut, mAh, dq C): 10 250 900 ; 20 500 1800 ; 30 750 2700 ; 40 1000 3600 ; 50 1250 4500
#   I = 1,50 A dao dong +-0,02 A (dung_cu, tham_so dI) ; 1 mAh = 3,6 C (rut_ra) ; mo_hinh dq = I.(dt.60), mAh = dq/3,6.
#   So dem mAh va dong ho bam gio chay theo mo hinh (cung mot ham sim_s), hang bang hien DUNG luc dem cham moc 600 s.
#   Cau hoi chot: I = 0,80 A (trong tham_so I 0,5..3,0), 15 phut (trong dt 0..60) -> dq = 0,8.900 = 720 C;
#     phan xa nhan phut ra 0,8.15 = 12 -> chua tung hien tren man (khong ve +-12 C de khong lo cau hoi sai so trong bai).
# Mach: cuc sac -> dong ho USB (mac NOI TIEP tren day sac) -> dien thoai. Khong ve U (kho khong co so U).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (10 phut lam cham, tua nhanh 20..50 phut) -> Dap an (do thi
#       dq-dt qua goc + cot dq + phep doi mAh->C) -> Bay (nhan voi so phut) roi Chua noi duoc -> Chot + cau hoi tu nho lai.
from engine import *

ROWS = [(10, 250, 900), (20, 500, 1800), (30, 750, 2700), (40, 1000, 3600), (50, 1250, 4500)]   # so_lieu_mau
I0 = 1.50
FLICK = [1.50, 1.51, 1.50, 1.49, 1.50, 1.52, 1.50, 1.48]    # dao dong trong +-0,02 A (dI)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DRED = (185, 28, 28)
SCRB = (18, 26, 40)                 # nen man dong ho USB
AMP_C = (250, 204, 21)              # chu dong (vang)
MAH_C = (110, 231, 183)             # chu mAh (xanh ngoc)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
def mm_ss(s): s = int(round(s)); return f"{s // 60:02d}:{s % 60:02d}"

def devices(d, sim=0.0, amp=I0, t=0.0, charging=False):
    """Cuc sac -> day -> dong ho USB -> day -> dien thoai; dong ho bam gio ben duoi. sim = giay da sac (mo hinh)."""
    mah = int(round(sim * I0 / 3.6))
    # day sac (noi tiep): cuc sac -> dong ho -> dien thoai
    d.line([(230, 500), (300, 500)], fill=NAVY, width=10)
    d.line([(740, 500), (830, 500)], fill=NAVY, width=10)
    # cuc sac
    for yy in (450, 550): d.rectangle([28, yy - 9, 60, yy + 9], fill=GRAY)
    card(d, (60, 390, 230, 610), fill=WHITE, outline=NAVY, r=26, w=5)
    d.rectangle([215, 480, 236, 520], fill=NAVY)
    text(d, (145, 655), "cục sạc", 38, INK)
    # dong ho USB
    card(d, (300, 330, 740, 670), fill=(48, 56, 78), r=30)
    card(d, (326, 356, 714, 644), fill=SCRB, r=18)
    text(d, (520, 432), vn(amp) + " A", 64, AMP_C)
    text(d, (520, 562), f"{mah} mAh", 64, MAH_C)
    text(d, (520, 715), "đồng hồ USB", 38, INK)
    if charging:                                     # mui ten chieu dong qui uoc tren day (cuc sac -> dien thoai)
        for x0, x1 in ((240, 296), (748, 826)):
            arrow(d, (x0, 450), (x1, 450), (194, 65, 12), w=10, head=26)
    # dien thoai
    card(d, (830, 300, 1030, 760), fill=NAVY, r=34)
    card(d, (846, 336, 1014, 724), fill=(226, 232, 240), r=18)
    bx0, by0, bx1, by1 = 892, 430, 968, 640                       # pin (khong ghi %)
    d.rectangle([915, by0 - 16, 945, by0], fill=NAVY)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=NAVY, width=6)
    fill = 0.08 + mah / 2500                                      # tuyen tinh theo q: dung luong ve co dinh, khong ghi so
    d.rectangle([bx0 + 10, by1 - 10 - (by1 - by0 - 20) * fill, bx1 - 10, by1 - 10], fill=GREEN)
    # dong ho bam gio
    card(d, (300, 770, 740, 900), fill=WHITE, outline=NAVY, r=24, w=4)
    dot(d, 380, 840, 40, WHITE, outline=NAVY); d.rectangle([372, 788, 388, 798], fill=NAVY)
    a = -math.pi / 2 + 2 * math.pi * (sim % 600) / 600
    d.line([(380, 840), (380 + 30 * math.cos(a), 840 + 30 * math.sin(a))], fill=RED, width=5)
    text(d, (580, 838), mm_ss(sim), 60, INK)

def table(d, n, qn=0, y=960, hl=None, ka=1.0, rh=78):
    """Bang dt - mAh - dq; n hang da co; qn = so hang da hien cot dq (con lai '?')."""
    card(d, (40, y, 1040, y + 132 + 5 * rh), fill=WHITE, outline=NAVY, w=4)
    xs = (200, 540, 870)
    for x, c in zip(xs, ("Δt (phút)", "Đồng hồ (mAh)", "Δq (C)")): text(d, (x, y + 50), c, 40, INK)
    d.line([(70, y + 90), (1010, y + 90)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 136 + i * rh; m, q, c = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - rh / 2 + 3, 1020, yy + rh / 2 - 3], radius=18, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), str(m), 44, INK); text(d, (xs[1], yy), str(q), 44, INK)
        text(d, (xs[2], yy), str(c) if i < qn else "?", 44, BLUE if i < qn else GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    devices(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 270, "Dòng giữ 1,50 A. Cứ sau\n10 phút, số mAh trên\nđồng hồ thay đổi thế nào?", 50, INK,
          maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
S0, S1 = 0.8, 3.6        # 10 phut dau: dong ho bam gio 0 -> 600 s trong [S0, S1]
FF0, FFW = 0.2, 1.3      # tua nhanh: doan j (600 s) bat dau M[1] + FF0 + (j-1).FFW

def sim_s(t, M):
    """Giay da sac (mo hinh) theo thoi gian canh: mot nguon duy nhat cho dong ho, so mAh va so hang bang."""
    if t < M[1] + FF0: return 600 * clamp((t - S0) / (S1 - S0))
    return 600 + 2400 * clamp((t - M[1] - FF0) / (4 * FFW))

def s_do(img, d, t, sc):
    M = sc["M"]
    s = sim_s(t, M)
    charging = (S0 <= t < S1) or (M[1] + FF0 <= t < M[1] + FF0 + 4 * FFW)
    amp = FLICK[int(t * 2.5) % len(FLICK)] if charging else I0
    if t >= M[1] + FF0 - 0.3:
        card(d, (760, 214, 1000, 274), fill=ORANGE, r=30); text(d, (880, 244), "tua nhanh", 38, WHITE)
    devices(d, s, amp, t, True)
    table(d, min(5, int(s / 600 + 1e-6)))

# ---------------- canh 3: Dap an + rut ra ----------------
GX0, GX1, GY0, GY1 = 220, 940, 880, 420        # truc dq theo dt: 0-55 phut, 0-5000 C
def gx(m): return GX0 + m / 55 * (GX1 - GX0)
def gy(q): return GY0 - q / 5000 * (GY0 - GY1)

def dash(d, p1, p2, col, w=3, on=12, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / L, min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · mỗi 10 phút thêm 250 mAh"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W / 2 - pw / 2, 234, W / 2 + pw / 2, 298), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 266), lab, 40, WHITE, alpha=ka)
    card(d, (40, 320, 1040, 950), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1000, 362), "số liệu mô phỏng", 40, MUTED, bold=False, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 44), "Δq (C)", 42, INK, anchor="lm")
    text(d, (1000, GY0 - 46), "Δt (phút)", 42, INK, anchor="rm")
    for m in (10, 20, 30, 40, 50):
        d.line([(gx(m), GY0), (gx(m), GY0 + 12)], fill=NAVY, width=3)
        if m in (10, 30, 50): text(d, (gx(m), GY0 + 40), str(m), 42, INK)
    for q in (2000, 4000):
        d.line([(GX0 - 12, gy(q)), (GX0, gy(q))], fill=NAVY, width=3)
        text(d, (GX0 - 18, gy(q)), str(q), 40, INK, anchor="rm")
    kl = appear(t, M[0] + 0.6, 0.8)                # duong thang qua goc, do doc I = 90 C/phut
    if kl > 0:
        m1 = 52 * kl
        d.line([(gx(0), gy(0)), (gx(m1), gy(90 * m1))], fill=A(GREEN, 0.9), width=5)
        if kl >= 1: text(d, (250, 490), "đường thẳng qua gốc", 42, GREEN, anchor="lm")
    for i, (m, q, c) in enumerate(ROWS):
        k = appear(t, 0.3 + 0.2 * i, 0.3)
        if k > 0: dot(d, gx(m), gy(c), 13, A(ORANGE if (i == 0 and t >= M[1] - 0.1) else BLUE, k), outline=WHITE)
    hl = 0 if t >= 1.4 else None                   # cot dq hien CUNG luc dong I.dt = 900 C (khong truoc)
    table(d, 5, qn=sum(t >= 1.6 + 0.2 * i for i in range(5)), y=965, hl=hl, ka=appear(t, 1.4, 0.3), rh=68)
    k1 = appear(t, 1.4, 0.4)
    k2 = appear(t, M[1] + 0.2, 0.4)
    if k1 > 0:                                     # dong 1 giu toi het canh; dong 2 them khi phu de doi don vi
        card(d, (40, 1450, 1040, 1450 + 100 + 90 * k2), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=20, w=3)
        text(d, (W / 2, 1500), "10 phút = 600 s: 1,50 · 600 = 900 C", 42, (21, 110, 55), alpha=k1)
    if k2 > 0:
        text(d, (W / 2, 1590), "250 mAh · 3,6 = 900 C", 42, (154, 52, 18), alpha=k2)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    devices(d, 600)
    if a1 > 0:
        y0 = 960
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, 1.6, 0.5)
        text(d, (470, y0 + 200), "1,50 · 10 = 15 C", 54, DRED, alpha=k3)
        text(d, (880, y0 + 235), "✗", 110, DRED, alpha=k3)
        text(d, (470, y0 + 285), "sai: để nguyên số phút", 44, DRED, alpha=k3)
        text(d, (470, y0 + 425), "1,50 · 600 = 900 C", 54, (21, 110, 55), alpha=k4)
        text(d, (880, y0 + 460), "✓", 110, (21, 110, 55), alpha=k4)
        text(d, (470, y0 + 510), "đúng: 10 phút = 600 s", 44, (21, 110, 55), alpha=k4)
    if k2 > 0:
        y0 = 960 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Gần đầy pin, dòng còn 1,50 A?", "• Pin nhận bao nhiêu năng lượng?")):
            kk = k2 * appear(t, M[1] + 0.1 + 0.3 * j, 0.4)
            text(d, (90, y0 + 230 + j * 150), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: 0,80 A trong 15 phut -> bao nhieu C (720 C); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Dòng không đổi: Δq = I · Δt,\ntỉ lệ thuận với thời gian", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (40, 600, 1040, lerp(1010, 1360, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 840, "Sạc ở 0,80 A trong 15 phút:\nđiện lượng qua dây\nkhoảng bao nhiêu C?", 50, INK, maxw=920,
          alpha=appear(t, M[0] + 0.9, 0.5))
    if kh > 0:
        card(d, (110, 990, 970, 1310), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1060, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1190, "1 C = 1 A · 1 s", 56, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
           (do["t0"] + S1, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(1, 5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-cuong-do-dong-dien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Cường độ dòng điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Sạc điện thoại qua đồng hồ USB", draw=s_hook, tail=0.8, caps=[
   ("Đồng hồ USB đo dòng sạc.", 2.8),
   ("Tự đoán trước khi xem tiếp.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Sạc 10 phút, ghi số mAh.", 4.0),
   ("Ghi tiếp ở 20, 30, 40, 50 phút.", 5.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Δq = I·Δt: đường thẳng qua gốc.", 4.2),
   ("Đổi đơn vị: 1 mAh = 3,6 C.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.9, caps=[
   ("Bẫy: nhân với số phút.", 3.6),
   ("Mới đo khi pin còn xa đầy.", 5.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 6.8)]),
])
