# Clip: tn-l10-tdvt-01 - Do toc do trung binh khi di bo tren doan 10 m bang dong ho bam giay (1/11/2026; dung lai
#   27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu ve >= 56 px, Du doan khong nut A-D, THU NGHI cau chot A-D o web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-tdvt-01.json (_kiem_so() doi chieu):
#   s = 10,0 m; so_lieu_mau t (s) = 7,9 ; 8,3 ; 8,1 ; 7,7 ; 8,0 -> trung binh 8,0 s; v_tb = 10,0 : 8,0 = 1,25 m/s.
# Video dung SAU hop exp (hop da noi v_tb ~ 1,25 m/s, lay trung binh). Hop 'Doc bang' hoi vi sao lan 2, 4 lech -> clip khong giai.
# Chot (THU NGHI, chua chieu): cung ban di deu nhu cu qua doan 15 m -> t = 15 : 1,25 = 12 s (theo mo hinh, s trong 5..30 m).
#   Bai co bai doi don vi km/h <-> m/s (⭐ 72 km/h) nen KHONG hoi doi don vi.
from engine import *

S_M = 10.0
TS = [7.9, 8.3, 8.1, 7.7, 8.0]            # so_lieu_mau, cot t (s)
T_TB = 8.0                                # trung binh 5 lan (ghi_chu kho)
FF_K = 6                                  # tua nhanh x6
X_START, X_END = -1.0, 10.6
GAP = 0.30
DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (91, 33, 182); DORANGE = (176, 64, 8)
TAPE = (234, 88, 12)
WALL = (241, 235, 224)
SUB = (60, 66, 92)
V_THAT = 1.25

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-tdvt-01.json")))
    assert [r[1] for r in k["so_lieu_mau"]["hang"]] == TS
    assert abs(sum(TS) / 5 - T_TB) < 1e-9 and abs(S_M / T_TB - 1.25) < 1e-9 and abs(15 / 1.25 - 12) < 1e-9
_kiem_so()

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

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
    text(d, (mx(0), FLOOR + 62), "vạch 1", 56, TAPE, alpha=alpha)
    text(d, (mx(10), FLOOR + 62), "vạch 2", 56, TAPE, alpha=alpha)
    y = FLOOR + 118
    arrow(d, (mx(5) - 170, y), (mx(0) + 4, y), c(INK), w=4, head=16)
    arrow(d, (mx(5) + 170, y), (mx(10) - 4, y), c(INK), w=4, head=16)
    text(d, (mx(5), y), "s = 10,0 m", 56, INK, alpha=alpha)

def stopwatch(d, val, running, alpha=1.0, note=True):
    c = lambda col: A(col, alpha)
    card(d, (170, 770, 770, 960), fill=c(NAVY), r=30)
    s = "?" if val is None else vn(val, 2)
    text(d, (620, 865), s, 96, WHITE, anchor="rm", alpha=alpha)
    text(d, (640, 875), "s", 60, WHITE, anchor="lm", alpha=alpha)
    if running: dot(d, 220, 865, 16, c(RED))
    if note: text(d, (900, 835), "tua", 56, SUB, alpha=alpha); text(d, (900, 905), "×6", 56, SUB, alpha=alpha)


# ---------- dai cham t ----------
AX0, AX1, TLO, THI = 150, 870, 7.5, 8.5
def tx(t): return AX0 + (AX1 - AX0) * (t - TLO) / (THI - TLO)
HIGH = {7.9: True, 8.1: True}                 # nhan so le hai tang: 7,9 va 8,1 o tang tren

def strip(d, y0, n_dot, alpha=1.0, hi=None, avg=0.0):
    """Khung dai cham: truc t co dinh 7,5-8,5 s; n_dot cham dau. hi = chi so cham to dam (bay)."""
    c = lambda col: A(col, alpha)
    card(d, (60, y0, 1020, y0 + 440), fill=c(WHITE), outline=c(NAVY), w=4)
    text(d, (W / 2, y0 + 50), "Thời gian t mỗi lần đo", 56, INK, alpha=alpha)
    ya = y0 + 330
    d.line([(AX0 - 20, ya), (AX1 + 20, ya)], fill=c(INK), width=4)
    for k in range(11):
        tt = TLO + 0.1 * k; L = 18 if k % 5 == 0 else 10
        d.line([(tx(tt), ya - L), (tx(tt), ya + L)], fill=c(INK), width=3)
    for tt in (7.5, 8.0, 8.5):
        text(d, (tx(tt), ya + 60), vn(tt), 56, INK, alpha=alpha)
    text(d, (AX1 + 60, ya - 50), "t (s)", 56, SUB, alpha=alpha)
    for i in range(n_dot):
        x = tx(TS[i]); yd = ya - 50
        col = NAVY if hi is None or i == hi else GRAY
        dot(d, x, yd, 24, A(col, alpha))
        text(d, (x, yd - (130 if HIGH.get(TS[i]) else 65)), vn(TS[i]), 56, col, alpha=alpha)
    if avg > 0:                                       # vach trung binh: ve SAU cham, chua cho nhan "8,0" (khong che so)
        for y_a, y_b in ((ya - 215, ya - 150), (ya - 84, ya + 34)):
            yy = y_a
            while yy < y_b:
                d.line([(tx(T_TB), yy), (tx(T_TB), min(yy + 16, y_b))], fill=A(GREEN, avg), width=14); yy += 26
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


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    corridor(d, a); walker(d, X_START + 0.15 * math.sin(t * 2.5), a)
    k = appear(t, M[1] - 0.3, 0.45)
    if k <= 0:
        stopwatch(d, 0.0, False, a, note=False); return
    y0 = 790 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 700), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 300), "Cùng bạn, bấm giờ 5 lần.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 400), "Năm số đo t thế nào?", 62, PURPLE, alpha=k)
    for j in range(5):                                   # 5 o trong, dau ? nhap nho
        bx = 165 + j * 160; by = y0 + 500 + 10 * math.sin(t * 3 + j)
        card(d, (bx, by, bx + 130, by + 110), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=18, w=3)
        text(d, (bx + 65, by + 55), "?", 64, PURPLE, alpha=k)

# ---------------- canh 2: Tien hanh (5 lan) ----------------
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    x, val, running, n = run_state(t)
    corridor(d)
    if x is not None: walker(d, x)
    stopwatch(d, val, running)
    strip(d, 990, n)
    ka = appear(t, BADGE, 0.4)
    if ka > 0:
        s_ = "ĐÁP ÁN: lệch ít, quanh 8 s"; pw = tw(d, s_, F(58)) + 70
        card(d, (W / 2 - pw / 2, 1445, W / 2 + pw / 2, 1545), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1495), s_, 58, DGREEN, alpha=ka)

# ---------------- canh 3: Rut ra ----------------
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    strip(d, 260, 5, a, avg=a * (0.75 + 0.25 * math.sin(t * 4)))
    card(d, (60, 730, 1020, 1480), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (W / 2, 830), "t trung bình = 8,0 s", 64, DGREEN, alpha=a)
    text(d, (W / 2, 920), "(vạch xanh)", 56, SUB, alpha=a)
    k2 = appear(t, M[1] - 0.05, 0.4)
    text(d, (W / 2, 1080), "v trung bình = s : t", 62, INK, alpha=k2)
    text(d, (W / 2, 1190), "= 10,0 m : 8,0 s", 62, INK, alpha=k2)
    text(d, (W / 2, 1300), "= 1,25 m/s", 64, BLUE, alpha=k2)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35)
    card(d, (60, 260, 1020, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 900), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 1020), "Tốc độ từng bước?", 62, BLUE, alpha=k)
    xm = 4.6 + 3.6 * math.sin(t * 1.3) + 0.6 * math.sin(t * 5.1)          # buoc nhanh buoc cham
    walker(d, xm, k)
    d.line([(mx(-0.5), FLOOR), (mx(10.5), FLOOR)], fill=A(MUTED, k), width=4)
    text(d, (mx(xm) + 70, FLOOR - 190 + 16 * math.sin(t * 3)), "?", 72, PURPLE, alpha=k)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 260, 1020, 520), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    text(d, (W / 2, 340), "✗ Chỉ lần 2: t = 8,3 s", 60, DRED, alpha=a)
    text(d, (W / 2, 440), "v ≈ 1,20 m/s", 60, DRED, alpha=a)
    ok = appear(t, M[1] - 0.05, 0.4)
    strip(d, 560, 5, a, hi=1, avg=ok * (0.75 + 0.25 * math.sin(t * 4)))
    pulse = 0.5 + 0.5 * math.sin(t * 5)
    if ok <= 0:                                                             # vong chop quanh cham lan 2
        x = tx(TS[1]); yd = 560 + 330 - 50
        d.ellipse([x - 44, yd - 44, x + 44, yd + 44], outline=A(DRED, pulse), width=6)
        return
    card(d, (60, 1030, 1020, 1260), fill=A((220, 252, 231), ok), outline=A(GREEN, ok), w=5)
    text(d, (W / 2, 1095), "✓ Trung bình 5 lần", 60, DGREEN, alpha=ok)
    text(d, (W / 2, 1190), "8,0 s → 1,25 m/s", 60, DGREEN, alpha=ok)

# ---------------- canh 6: THU NGHI ----------------
PX15 = 52.0; X15 = 150
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    fy = 640
    d.rectangle([80, fy, 1000, fy + 12], fill=A((214, 200, 178), k1))
    for m in (0, 15):
        d.rectangle([X15 + m * PX15 - 7, fy - 4, X15 + m * PX15 + 7, fy + 12], fill=A(TAPE, k1))
    yA = fy + 80
    arrow(d, (X15 + 7.5 * PX15 - 140, yA), (X15 + 4, yA), A(INK, k1), w=4, head=16)
    arrow(d, (X15 + 7.5 * PX15 + 140, yA), (X15 + 15 * PX15 - 4, yA), A(INK, k1), w=4, head=16)
    text(d, (X15 + 7.5 * PX15, yA), "15 m", 56, INK, alpha=k1)
    xm = -0.8 + ((t * 2.2) % 16.6)                                         # nguoi di lap lai qua doan 15 m
    xp = X15 + xm * PX15; hip = fy - 50; sh = fy - 92
    ph = math.sin(2 * math.pi * xm / 1.4); an = math.radians(24) * ph
    for s_ in (1, -1):
        d.line([(xp, hip), (xp + s_ * 50 * math.sin(an), hip + 50 * math.cos(an))], fill=A(NAVY, k1), width=7)
    d.line([(xp, hip), (xp, sh)], fill=A(NAVY, k1), width=8)
    d.ellipse([xp - 10, sh - 24, xp + 10, sh - 4], fill=A(NAVY, k1))
    card(d, (360, 345, 720, 455), fill=A(NAVY, k1), r=26)
    text(d, (540, 400), "? s", 70, WHITE, alpha=k1)
    text(d, (W / 2, 900), "Đi đều như cũ, 1,25 m/s.", 60, INK, alpha=k1)
    text(d, (W / 2, 1010), "Qua 15 m, đồng hồ chỉ", 60, ORANGE, alpha=k1)
    text(d, (W / 2, 1110), "khoảng bao nhiêu giây?", 60, ORANGE, alpha=k1)
    cbar(d, 1300, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for r in SCH: cs += [(do["t0"] + r["tA"], "tick"), (do["t0"] + r["tB"], "tick")]
    cs += [(do["t0"] + BADGE, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1], "ding"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-tdvt-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Tốc độ và vận tốc · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bấm giờ đi bộ 10 m", draw=s_hook, tail=0.3, caps=[
   ("Chân chạm vạch thì bấm.", 3.0),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Đo năm lần", draw=s_do, tail=0.4, caps=[
   ("Mỗi lần đo thêm một chấm.", T_DONE - 0.2),
   ("Năm chấm không trùng nhau.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Lấy trung bình năm số đo.", 3.2),
   ("Chia quãng đường cho thời gian.", 3.6)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("1,25 m/s là của cả đoạn.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đo một lần, lấy luôn?", 3.4),
   ("Lấy trung bình mới tin được.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
