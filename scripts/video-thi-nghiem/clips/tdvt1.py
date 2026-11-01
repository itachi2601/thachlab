# Clip: tn-l10-tdvt-01 - Do toc do trung binh khi di bo tren doan 10 m bang dong ho bam giay (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-tdvt-01.json:
#   s = 10,0 m; so_lieu_mau t (s) = 7,9 ; 8,3 ; 8,1 ; 7,7 ; 8,0 -> trung binh 8,0 s; v_tb = 10,0 : 8,0 = 1,25 m/s.
#   Dong ho do chia 0,01 s (dung_cu) -> hien 2 chu so thap phan.
# Khac tdvt3 (nhin tu tren xuong + bang): o day nhin ngang hanh lang (nguoi di dung ti le 80 px/m, cao 1,6 m),
#   truc chinh la DAI CHAM t (s) tu 7,5 den 8,5 s, khong co bang.
# Dong pha: lan i tua nhanh x5, nguoi di deu v_i = s / t_i (m/s that); dong ho chay tu luc chan cham vach 1,
#   dung dung luc cham vach 2 -> so chi = t_i dung luc nguoi o x = 10,0 m (kiem bang ma moi 0,05 s).
# Cau hoi ngay sau hop trong bai ("vi sao lan 2 va lan 4 lech nhieu nhat, sai so den tu dau") KHONG giai trong clip.
# Canh: Du doan (5 so do t se the nao) -> Tien hanh (5 lan, cham hien dung luc dong ho dung) -> Rut ra (trung binh,
#       v_tb = s : t tung dong) -> Chua noi duoc gi (toc do tung buoc) -> Bay (lay mot lan) -> Chot + cau hoi (1 gio -> km).
from engine import *

S_M = 10.0
TS = [7.9, 8.3, 8.1, 7.7, 8.0]            # so_lieu_mau, cot t (s)
T_TB = 8.0                                # trung binh 5 lan (ghi_chu kho)
FF_K = 6                                  # tua nhanh x6
X_START, X_END = -1.0, 10.6               # nguoi bat dau 1,0 m truoc vach 1, di qua vach 2 them 0,6 m
GAP = 0.30                                # nghi giua hai lan (giay man hinh)
DRED = (185, 28, 28)
TAPE = (234, 88, 12)
WALL = (241, 235, 224)
SUB = (60, 66, 92)                        # chu phu dam
V_THAT = 1.25                             # tham_so v_that: ban di deu nhu nhau moi lan

# ---------- hanh lang nhin ngang ----------
PXM = 80.0; X0PX = 140                    # 0 m -> x 140, 10 m -> x 940
FLOOR = 600
def mx(m): return X0PX + PXM * m

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def walker(d, xm, alpha=1.0, col=NAVY):
    """Nguoi que cao 1,6 m dung ti le (128 px), buoc chan theo quang duong (buoc 0,7 m)."""
    c = A(col, alpha); x = mx(xm)
    hip = FLOOR - 0.9 * PXM; sh = FLOOR - 1.38 * PXM; hr = 0.11 * PXM
    ph = math.sin(2 * math.pi * xm / 1.4); a = math.radians(24) * ph; L = 0.9 * PXM
    for s in (1, -1):
        d.line([(x, hip), (x + s * L * math.sin(a), hip + L * math.cos(a))], fill=c, width=8)
        d.line([(x, sh + 8), (x - s * 0.55 * PXM * math.sin(a), sh + 8 + 0.55 * PXM * math.cos(a))], fill=c, width=7)
    d.line([(x, hip), (x, sh)], fill=c, width=9)
    d.ellipse([x - hr, sh - 2 * hr - 4, x + hr, sh - 4], fill=c)

def corridor(d, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([40, 300, 1040, FLOOR], fill=c(WALL))
    d.rectangle([40, FLOOR, 1040, FLOOR + 14], fill=c((214, 200, 178)))
    for m in range(11):
        L = 16 if m % 5 == 0 else 9
        d.line([(mx(m), FLOOR + 14), (mx(m), FLOOR + 14 + L)], fill=c(MUTED), width=3)
    for m in (0, 10):
        d.rectangle([mx(m) - 7, FLOOR - 4, mx(m) + 7, FLOOR + 14], fill=c(TAPE))
    text(d, (mx(0), FLOOR + 62), "vạch 1", 40, TAPE, alpha=alpha)
    text(d, (mx(10), FLOOR + 62), "vạch 2", 40, TAPE, alpha=alpha)
    y = FLOOR + 118
    arrow(d, (mx(5) - 130, y), (mx(0) + 4, y), c(INK), w=4, head=16)
    arrow(d, (mx(5) + 130, y), (mx(10) - 4, y), c(INK), w=4, head=16)
    text(d, (mx(5), y), "s = 10,0 m", 40, INK, alpha=alpha)

def stopwatch(d, val, running, alpha=1.0, note=True):
    c = lambda col: A(col, alpha)
    card(d, (170, 770, 770, 960), fill=c(NAVY), r=30)
    text(d, (470, 812), "đồng hồ bấm giây", 40, (205, 210, 232), alpha=alpha)
    s = "?" if val is None else vn(val, 2)
    text(d, (620, 887), s, 84, WHITE, anchor="rm", alpha=alpha)
    text(d, (635, 895), "s", 50, WHITE, anchor="lm", alpha=alpha)
    if running: dot(d, 220, 887, 14, c(RED))
    if note: text(d, (900, 845), "tua", 40, SUB, alpha=alpha); text(d, (900, 895), "nhanh", 40, SUB, alpha=alpha); text(d, (900, 945), "×6", 40, SUB, alpha=alpha)

# ---------- dai cham t ----------
AX0, AX1, TLO, THI = 160, 920, 7.5, 8.5
def tx(t): return AX0 + (AX1 - AX0) * (t - TLO) / (THI - TLO)

def strip(d, y0, n_dot, alpha=1.0, hi=None, dim=False, avg=0.0):
    """Khung dai cham: truc t co dinh 7,5-8,5 s; n_dot cham dau. hi = chi so cham to dam (bay)."""
    c = lambda col: A(col, alpha)
    card(d, (60, y0, 1020, y0 + 385), fill=c(WHITE), outline=c(NAVY), w=4)
    text(d, (W / 2, y0 + 45), "Thời gian t mỗi lần đo", 40, INK, alpha=alpha)
    ya = y0 + 240
    d.line([(AX0 - 20, ya), (AX1 + 20, ya)], fill=c(INK), width=4)
    for k in range(11):
        tt = TLO + 0.1 * k; L = 18 if k % 5 == 0 else 10
        d.line([(tx(tt), ya - L), (tx(tt), ya + L)], fill=c(INK), width=3)
    for tt in (7.5, 8.0, 8.5):
        text(d, (tx(tt), ya + 50), vn(tt), 40, INK, alpha=alpha)
    text(d, (AX1 + 48, ya - 40), "t (s)", 40, SUB, alpha=alpha)
    text(d, (W / 2, ya + 108), "trục cắt · mỗi vạch 0,1 s", 40, SUB, alpha=alpha)
    if avg > 0:                                       # vach trung binh ve duoi cham
        for yy in range(int(ya - 100), int(ya + 10), 22):
            d.line([(tx(T_TB), yy), (tx(T_TB), yy + 12)], fill=A(GREEN, avg), width=5)
    for i in range(n_dot):
        x = tx(TS[i]); yd = ya - 70
        col = NAVY if hi is None or i == hi else GRAY
        a2 = alpha * (0.45 if dim and hi is not None and i != hi else 1.0)
        dot(d, x, yd, 29, A(col, a2))
        text(d, (x, yd + 1), str(i + 1), 40, WHITE, alpha=a2)
        text(d, (x, yd - 64), vn(TS[i]), 40, col, alpha=a2)
    return ya

# ---------- lich chay 5 lan (giay man hinh trong canh "do") ----------
R0 = 0.5
def schedule():
    out = []; t = R0
    for ti in TS:
        v = V_THAT * FF_K                           # m/s man hinh: moi lan nguoi di cung toc do
        tA = t + (0 - X_START) / v; tB = tA + S_M / v; tE = t + (X_END - X_START) / v
        out.append(dict(t0=t, tA=tA, tB=tB, tE=tE, v=v, ti=ti)); t = tE + GAP
    return out
SCH = schedule()
T_DONE = SCH[-1]["tE"]                      # nguoi qua vach 2 lan 5 xong
BADGE = T_DONE + 0.25

def run_state(t):
    """Tra ve (x_nguoi hoac None, so dong ho, dang chay, so cham da hien)."""
    prev = 0.0; n = 0
    for i, r in enumerate(SCH):
        if t < r["t0"]:
            return None, prev, False, n
        if t < r["tE"] + GAP:
            x = X_START + r["v"] * (t - r["t0"]) if t < r["tE"] else None
            if t < r["tA"]: return x, prev, False, n
            if t < r["tB"]: return x, r["ti"] * (t - r["tA"]) / (r["tB"] - r["tA"]), True, n   # dem ti le: dung dung ti khi x = 10 m
            return x, r["ti"], False, n + 1
        prev = r["ti"]; n = i + 1
    return None, prev, False, n

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    corridor(d, a); walker(d, X_START, a)
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0:
        stopwatch(d, 0.0, False, a, note=False); return
    y0 = 790 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 640), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 170, "Cùng bạn ấy đi đều qua 10 m,", 44, INK, alpha=k)
    ctext(d, y0 + 230, "bấm giờ 5 lần.", 44, INK, alpha=k)
    ctext(d, y0 + 320, "Năm số đo t sẽ thế nào?", 46, INK, alpha=k)
    for j in range(5):                                   # 5 o trong, cung mau
        bx = 165 + j * 160
        card(d, (bx, y0 + 400, bx + 130, y0 + 500), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=18, w=3)
        text(d, (bx + 65, y0 + 450), "?", 56, PURPLE, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 570, 880, y0 + 586], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 570, 200 + 680 * (1 - q), y0 + 586], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh (5 lan) ----------------
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    x, val, running, n = run_state(t)
    corridor(d)
    if x is not None: walker(d, x)
    stopwatch(d, val, running)
    strip(d, 995, n)
    ka = appear(t, BADGE, 0.4)
    if ka > 0:
        s_ = "ĐÁP ÁN · Lệch chút ít, quanh một giá trị"; pw = tw(d, s_, F(40)) + 60
        card(d, (W / 2 - pw / 2, 1400, W / 2 + pw / 2, 1490), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=26, w=4)
        text(d, (W / 2, 1445), s_, 40, GREEN, alpha=ka)

# ---------------- canh 3: rut ra ----------------
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    strip(d, 270, 5, a, avg=appear(t, 0.9, 0.4))
    card(d, (60, 700, 1020, 1480), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    k1 = appear(t, 1.1, 0.4)
    text(d, (W / 2, 775), "(7,9 + 8,3 + 8,1 + 7,7 + 8,0) : 5", 46, INK, alpha=k1)
    k1b = appear(t, 2.2, 0.4)
    rich(d, W / 2, 860, "t_{tb} = 8,0 s", 60, GREEN, k1b)
    text(d, (W / 2, 925), "trung bình (vạch xanh)", 40, SUB, alpha=k1b)
    k2 = appear(t, M[1] + 0.1, 0.4)
    rich(d, W / 2, 1050, "v_{tb} = s : t_{tb}", 60, INK, k2)
    text(d, (W / 2, 1115), "tốc độ TB = quãng đường : thời gian", 40, SUB, alpha=k2)
    k3 = appear(t, M[1] + 1.4, 0.4)
    text(d, (W / 2, 1225), "= 10,0 m : 8,0 s", 54, INK, alpha=k3)
    k4 = appear(t, M[1] + 2.6, 0.4)
    text(d, (W / 2, 1335), "= 1,25 m/s", 60, BLUE, alpha=k4)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 1120), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 520), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 270, "Nếu bước nhanh bước chậm:", 46, BLUE, alpha=k)
    ctext(d, y1 + 345, "tốc độ từng bước", 46, BLUE, alpha=k)
    ctext(d, y1 + 420, "chưa biết", 46, BLUE, alpha=k)
    # nguoi di + dau hoi tren tung buoc
    gy = y1 + 860
    d.line([(150, gy), (930, gy)], fill=A(MUTED, k), width=4)
    for j, xm in enumerate((-0.6, 2.6, 5.8)):
        xp = 180 + 250 * j
        for s_ in (1, -1):
            a_ = math.radians(22) * s_
            d.line([(xp, gy - 72), (xp + 72 * math.sin(a_), gy)], fill=A(NAVY, k * 0.55), width=7)
        d.line([(xp, gy - 72), (xp, gy - 110)], fill=A(NAVY, k * 0.55), width=8)
        d.ellipse([xp - 9, gy - 132, xp + 9, gy - 114], fill=A(NAVY, k * 0.55))
        text(d, (xp + 100, gy - 150), "?", 64, PURPLE, alpha=k)
    ctext(d, y1 + 1010, "1,25 m/s: cả đoạn 10 m", 42, INK, alpha=k)

# ---------------- canh 5: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 560), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    text(d, (W / 2, 425), "Chỉ lần 2: t = 8,3 s", 46, DRED, alpha=a)
    text(d, (W / 2, 495), "v = 10,0 : 8,3 ≈ 1,20 m/s", 46, DRED, alpha=a)
    ok = appear(t, M[1] + 2.2, 0.4)                       # dau dung tre >= 2 s sau "Co dung khong?"
    strip(d, 590, 5, a, hi=1, dim=True, avg=ok)
    if ok > 0:
        card(d, (60, 1010, 1020, 1240), fill=A((220, 252, 231), ok), outline=A(GREEN, ok), w=4)
        text(d, (W / 2, 1080), "✓ Trung bình 5 lần", 46, GREEN, alpha=ok)
        text(d, (W / 2, 1160), "8,0 s → 1,25 m/s", 46, GREEN, alpha=ok)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):
        ctext(d, 900, "Đi đều như vậy 1 giờ\nđược mấy km?", 50, INK,
              maxw=880, alpha=appear(t, sc["M"][0] + 0.4, 0.5))
        kv = appear(t, sc["M"][0] + 0.4, 0.5)
        if kv > 0:
            card(d, (300, 1035, 780, 1145), fill=A((239, 246, 255), kv), outline=A(BLUE, kv), r=24, w=3)
            rich(d, W / 2, 1090, "v_{tb} = 1,25 m/s", 50, BLUE, kv)
        kh = appear(t, sc["M"][0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1230, 970, 1500), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1365, "1 giờ có bao nhiêu giây?", 46, (154, 52, 18), maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Tốc độ trung bình\n= quãng đường : thời gian", "", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    for r in SCH: cs += [(do["t0"] + r["tA"], "tick"), (do["t0"] + r["tB"], "tick")]
    cs += [(do["t0"] + BADGE, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-tdvt-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Tốc độ và vận tốc · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bấm giờ đi bộ 10 m", draw=s_hook, tail=0.5, caps=[
   ("Chân chạm vạch thì bấm.", 2.8),
   ("Dừng video, tự đoán.", 5.2)]),
 dict(key="do", title="Đo năm lần", draw=s_do, tail=0.4, caps=[
   ("Mỗi lần đo thêm một chấm.", T_DONE - 0.2),
   ("Năm chấm không trùng nhau.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Trung bình năm số đo.", 2.9),
   ("Thế số từng dòng.", 4.0)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Đọc kỹ giới hạn.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đo một lần, lấy luôn?", 2.8),
   ("Có đúng không?", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.2)]),
])
