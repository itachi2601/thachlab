# Clip: tn-l11-conangdddh-01 - Do k bang cach treo qua nang, roi tinh Et, Ed tai cac vach li do
# (31/10/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 56 px khi ve, K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-conangdddh-01.json (_kiem_so() doi chieu):
#   tham_so: m = 0,200 kg ; g = 9,8 ; A = 0,080 m (min 0,02, max 0,12). cac_buoc.lam: delta_l = 0,049 m -> k = 40 N/m.
#   so_lieu_mau (x m, Et, Ed): 0 / 0 / 0,128 ; 0,04 / 0,032 / 0,096 ; 0,08 / 0,128 / 0 (clip chi dung 3 hang nay).
#   hien_tuong_hay_sai: moc the nang o cho lo xo chua dan -> tai VTCB 0,04802 J -> canh bay.
# Du doan (DOI 27/11: ca cu "x = A/2: Ed so voi Et" trung Bai toan mau + bang thi nghiem cua bai):
#   tha tu bien 8 cm; doan 8 -> 4 cm hay 4 -> 0 cm dong nang tang them nhieu hon? -> doan 8 -> 4 (+0,096 J > +0,032 J).
#   Phan xa sai: "gan O vat nhanh nen doan sau tang nhieu hon" / "hai doan dai bang nhau nen bang nhau".
# Thu nghi (= cau_chot khung web): giu lo xo, keo toi A = 10 cm (trong dai tham_so); qua x = 4,0 cm thi Ed = ?
#   -> W = 0,200 J; Ed = 0,200 - 0,032 = 0,168 J. Can 2 buoc (W moi, tru Et). Dap so KHONG hien tren man.
from engine import *

K_, A_CM, W_J, DL = 40.0, 8.0, 0.128, 4.9
OMEGA = math.sqrt(200.0)
SLOW = 22
TV = SLOW * 2 * math.pi / OMEGA                          # chu ki tren video (s) ~ 9,77 s
def et_of(x_cm): return 0.5 * K_ * (x_cm / 100) ** 2

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-conangdddh-01.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["m"]["gia_tri"] == 0.2 and tp["g"]["gia_tri"] == 9.8 and tp["A"]["mac_dinh"] == 0.08
    assert abs(0.2 * 9.8 / (DL / 100) - K_) < 1e-9
    h = {round(r[0], 3): r for r in k["so_lieu_mau"]["hang"]}
    assert h[0.0][1:3] == [0, 0.128] and h[0.04][1:3] == [0.032, 0.096] and h[0.08][1:3] == [0.128, 0]
    assert tp["A"]["min"] <= 0.10 <= tp["A"]["max"]
    assert abs(0.5 * K_ * 0.1 ** 2 - et_of(4.0) - 0.168) < 1e-9                  # cau chot (theo mo hinh)
    assert abs(0.5 * K_ * (DL / 100) ** 2 - 0.04802) < 1e-9                       # bay
_kiem_so()

DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8)
CET = (234, 88, 12); CED = (37, 99, 235)                 # mau Et (cam) / Ed (xanh)
BLOCK = (250, 204, 120); WOOD = (196, 160, 112); EMPTY = (148, 140, 128)

_TI = {}
def TI(size):                                           # Times Bold Italic cho l viet tay (SF khong co glyph)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi cong thuc: _{..} chi so duoi (>= 56 px)."""
    fs = []
    for p in [p for p in re.split(r"(ℓ|_\{[^}]*\})", s) if p]:
        if p == "ℓ": fs.append((p, TI(size * 1.1), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(max(56, size * 0.7)), size * 0.24))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=170, n=5):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9)
    for i in range(n):
        x = x0 + i * 152
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=16)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def pill(d, cy, s, col, a=1.0, size=56):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, cy - 40, W / 2 + pw / 2, cy + 40), fill=A(col, a), r=40)
    text(d, (W / 2, cy), s, size, WHITE, alpha=a)

def coil(d, x, ya, yb, amp=26, n=12, col=NAVY, w=5, alpha=1.0):
    e = 16; pts = [(x, ya), (x, ya + e)]; L = (yb - e) - (ya + e)
    for i in range(1, 2 * n): pts.append((x + (amp if i % 2 else -amp), ya + e + L * i / (2 * n)))
    pts += [(x, yb - e), (x, yb)]
    d.line(pts, fill=A(col, alpha), width=w, joint="curve")

def hcoil(d, xa, xb, y, amp=22, n=12, col=NAVY, w=5, alpha=1.0):
    e = 14; pts = [(xa, y), (xa + e, y)]; L = (xb - e) - (xa + e)
    for i in range(1, 2 * n): pts.append((xa + e + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(xb - e, y), (xb, y)]
    d.line(pts, fill=A(col, alpha), width=w, joint="curve")

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1); n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(p0[0] + (p1[0] - p0[0]) * a, p0[1] + (p1[1] - p0[1]) * a),
                (p0[0] + (p1[0] - p0[0]) * b, p0[1] + (p1[1] - p0[1]) * b)], fill=col, width=w)

# ---------------- ray ngang (khung nguon 1080x1920; mp4 x = 65 + 0,88 x) ----------------
XO = 330
def rail(d, x_cm, ry=420, px=80, alpha=1.0, labs=(0, 4, 8), vfrac=0.0):
    c = lambda col: A(col, alpha)
    X = lambda v: XO + v * px
    d.rectangle([60, ry - 90, 84, ry + 60], fill=c(GRAY), outline=c(NAVY), width=3)
    d.rectangle([60, ry + 50, 1040, ry + 70], fill=c(WOOD), outline=c(NAVY), width=2)
    xc = X(x_cm)
    hcoil(d, 84, xc - 50, ry, alpha=alpha)
    d.rounded_rectangle([xc - 50, ry - 46, xc + 50, ry + 46], radius=12, fill=c(BLOCK), outline=c(NAVY), width=4)
    for v in labs:
        d.line([(X(v), ry + 72), (X(v), ry + 100)], fill=c(NAVY), width=5)
        text(d, (X(v), ry + 145), str(v), 56, INK, alpha=alpha)
    text(d, (X(labs[0]) - 60, ry + 145), "cm", 56, INK, anchor="rm", alpha=alpha)
    if vfrac > 0.01:
        L = 170 * vfrac
        arrow(d, (xc, ry - 80), (xc - L, ry - 80), A((21, 110, 55), alpha), w=7, head=22)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rail(d, 8.0)
    X = lambda v: XO + v * 80
    for (a_, b_), col, lab in (((8, 4), CET, "đoạn 1"), ((4, 0), CED, "đoạn 2")):
        y = 680
        d.line([(X(a_) - 6, y), (X(b_) + 6, y)], fill=col, width=7)
        for xx in (X(a_), X(b_)): d.line([(xx, y - 18), (xx, y + 18)], fill=col, width=7)
        text(d, ((X(a_) + X(b_)) / 2, y + 60), lab, 58, col)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Động năng tăng thêm", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "ở đoạn nào nhiều hơn?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: do k (treo dung) ----------------
SX, TOP, BASE, HX = 170, 300, 1180, 430
Y0, PXC = 640, 60
YE = Y0 + DL * PXC
RX = 560
H0, H1 = 0.3, 1.6

def stand(d, sx, top, base, arm1):
    d.rectangle([sx - 120, base, sx + 300, base + 30], fill=GRAY, outline=NAVY, width=3)
    d.rectangle([sx - 10, top - 10, sx + 10, base], fill=GRAY, outline=NAVY, width=3)
    d.rectangle([sx - 10, top - 14, arm1, top + 10], fill=GRAY, outline=NAVY, width=3)

def hang(d, cx, top, yend, mass=1.0, label=True):
    coil(d, cx, top + 10, yend)
    d.line([(cx, yend), (cx, yend + 22)], fill=NAVY, width=5)
    if mass <= 0: return
    d.rounded_rectangle([cx - 80, yend + 22, cx + 80, yend + 140], radius=14, fill=A(BLOCK, mass), outline=A(NAVY, mass), width=4)
    if label: text(d, (cx, yend + 81), "200 g", 56, INK, alpha=mass)

def s_dok(img, d, t, sc):
    M = sc["M"]
    stand(d, SX, TOP, BASE, HX + 40)
    d.rectangle([RX, Y0 - 20, RX + 44, Y0 + 6 * PXC + 20], fill=(250, 240, 200), outline=NAVY, width=2)
    for k in range(0, 61):
        y = Y0 + k * PXC / 10; L = 24 if k % 10 == 0 else (15 if k % 5 == 0 else 8)
        d.line([(RX, y), (RX + L, y)], fill=NAVY, width=3 if L == 24 else 2)
    for k in (0, 2, 4, 6): text(d, (RX + 90, Y0 + k * PXC), str(k), 56, INK, anchor="lm")
    ye = Y0 + DL * PXC * ease((t - H0) / (H1 - H0))
    hang(d, HX, TOP, ye, mass=1.0)
    dashed(d, (HX + 40, Y0), (RX - 4, Y0), GRAY, w=4)
    d.line([(HX + 90, ye), (RX - 4, ye)], fill=ORANGE, width=5)
    kb = appear(t, 2.1, 0.4)
    if kb > 0:
        bx = RX + 150
        d.line([(bx, Y0), (bx, YE)], fill=A(ORANGE, kb), width=6)
        for yy in (Y0, YE): d.line([(bx - 16, yy), (bx + 16, yy)], fill=A(ORANGE, kb), width=6)
        eq(d, bx + 24, (Y0 + YE) / 2, "Δℓ = 4,9 cm", 56, DORANGE, alpha=kb, anchor="l")
    card(d, (60, 1260, 1020, 1560), fill=WHITE, outline=NAVY, r=24, w=4)
    text(d, (W / 2, 1330), "m = 0,200 kg · g = 9,8 m/s²", 56, INK)
    kk = appear(t, 2.1, 0.5)
    if kk > 0:
        eq(d, W / 2, 1460, "k = mg / Δℓ = 40 N/m", 62, DBLUE, alpha=kk)

# ---------------- canh 3: cot nang luong + bang ----------------
REL, FZ = 0.8, 1.2
MB, MC = TV / 6, TV / 4                          # thoi gian chay toi 4,0 / 0 cm
TB = REL + MB; TC = TB + FZ + (MC - MB)
ROW_T = [0.0, TB + 0.1, TC + 0.1]
ROWS = [("8,0", 8.0, "0,128", "0"), ("4,0", 4.0, "0,032", "0,096"), ("0", 0.0, "0", "0,128")]

def vach_state(t):
    if t < REL: return 8.0, 0.0, False
    m = MB if TB <= t < TB + FZ else (MC if t >= TC else (t - REL if t < TB else MB + t - TB - FZ))
    ph = 2 * math.pi * m / TV
    frozen = (TB <= t < TB + FZ) or t >= TC
    return 8.0 * math.cos(ph), math.sin(ph), frozen

def column(d, et, ed, x0, x1, yb, yt):
    h = yb - yt
    d.rectangle([x0, yt, x1, yb], fill=(248, 246, 240), outline=NAVY, width=3)
    ht = h * et / W_J; hd = h * ed / W_J
    if ht > 2: d.rectangle([x0 + 3, yb - ht, x1 - 3, yb - 2], fill=CET)
    if hd > 1: d.rectangle([x0 + 3, yb - ht - hd, x1 - 3, yb - ht], fill=CED)
    d.line([(x0 - 16, yt), (x1 + 16, yt)], fill=INK, width=4)

TX = [470, 700, 920]; TY = [850, 950, 1050]
def s_vach(img, d, t, sc):
    x, vf, frozen = vach_state(t)
    rail(d, x, vfrac=vf if t >= REL else 0.0)
    pw = tw(d, "quay chậm ×22", F(56)) + 56
    card(d, (1040 - pw, 230, 1040, 310), fill=ORANGE, r=40); text(d, (1040 - pw / 2, 270), "quay chậm ×22", 56, WHITE)
    et = et_of(x); ed = W_J - et
    column(d, et, ed, 90, 230, 1150, 720)
    eq(d, 70, 1210, "E_{t}", 58, CET, anchor="l"); eq(d, 190, 1210, "E_{d}", 58, CED, anchor="l")
    card(d, (300, 690, 1040, 1100), fill=WHITE, outline=NAVY, r=20, w=3)
    for cx, hd, col in zip(TX, ("x (cm)", "E_{t} (J)", "E_{d} (J)"), (INK, CET, CED)): eq(d, cx, 735, hd, 56, col)
    d.line([(310, 790), (1030, 790)], fill=NAVY, width=3)
    for i, (xl, xv, e1, e2) in enumerate(ROWS):
        if t < ROW_T[i]: continue
        ka = appear(t, ROW_T[i], 0.3) if i else 1.0
        cur = (i == 0 and t < REL) or (frozen and abs(x - xv) < 0.02)
        if cur: d.rounded_rectangle([308, TY[i] - 42, 1032, TY[i] + 42], radius=12, fill=A((255, 237, 213), ka))
        for cx, v, col in zip(TX, (xl, e1, e2), (INK, CET, CED)):
            text(d, (cx, TY[i]), v, 58, col, alpha=ka)
    card(d, (60, 1300, 1020, 1570), fill=(240, 244, 255), r=22)
    text(d, (W / 2, 1370), "k = 40 N/m · A = 8,0 cm", 56, INK)
    text(d, (W / 2, 1480), "Tổng luôn 0,128 J", 60, DBLUE)

# ---------------- canh 4: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    for j, (lab, val, e, col, at) in enumerate((("8 → 4 cm", "+0,096 J", 0.096, CET, 0.3),
                                                  ("4 → 0 cm", "+0,032 J", 0.032, CED, 2.3))):
        k = appear(t, at, 0.4)
        if k <= 0: continue
        y = 420 + j * 300
        text(d, (90, y), lab, 60, INK, anchor="lm", alpha=k)
        L = 820 * e / 0.096 * ease(clamp((t - at) / 0.8))
        d.rounded_rectangle([110, y + 70, 110 + max(L, 8), y + 160], radius=14, fill=A(CED, k))
        text(d, (1000, y), val, 62, DBLUE, anchor="rm", alpha=k)
    kp = appear(t, M[1] - 0.1, 0.4)
    if kp > 0:
        pill(d, 1080, "ĐÁP ÁN · đoạn 8 → 4 cm", NAVY, kp, size=58)
        eq(d, W / 2, 1250, "E_{t}: 0,128 → 0,032 → 0 J", 56, DORANGE, alpha=kp)

# ---------------- canh 5: Bay (treo dung, moc the nang) ----------------
BT, BPX = 300, 45
BY0 = 560; BYE = BY0 + DL * BPX
def s_bay(img, d, t, sc):
    kc = appear(t, 3.4, 0.5)
    stand(d, 170, BT, BYE + 190, 520)
    hang(d, 470, BT, BYE, label=False)
    dashed(d, (390, BY0), (700, BY0), DRED if kc < 0.5 else GRAY, w=6)
    text(d, (720, BY0), "chưa dãn", 56, DRED if kc < 0.5 else INK, anchor="lm")
    d.line([(560, BYE), (700, BYE)], fill=DGREEN if kc > 0.5 else GRAY, width=6)
    text(d, (720, BYE), "VTCB", 56, DGREEN if kc > 0.5 else INK, anchor="lm")
    y0 = 980
    card(d, (40, y0, 1040, y0 + 560), fill=WHITE, outline=DRED, w=6)
    pill(d, y0 + 70, "BẪY", DRED)
    text(d, (W / 2, y0 + 190), "✗ Mốc ở chỗ chưa dãn:", 58, DRED)
    lw = eq(d, W / 2, y0 + 290, "VTCB có E_{t} = 0,04802 J", 58, DRED)
    if kc > 0:
        d.line([(W / 2 - lw / 2 - 6, y0 + 292), (W / 2 - lw / 2 - 6 + (lw + 12) * kc, y0 + 292)], fill=(140, 15, 15), width=7)
        eq(d, W / 2, y0 + 430, "✓ Mốc ở VTCB: E_{t} = 0", 60, DGREEN, alpha=kc)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Ma sát lớn thì sao?", 62, INK)
    amp = 8.0 * math.exp(-0.45 * t)
    rail(d, amp * math.cos(2 * math.pi * t / 1.6), ry=800, labs=(0, 4, 8))

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 290, "THỬ NGHĨ", ORANGE, k1)
    card(d, (80, 380, 1000, 500), fill=A((239, 246, 255), k1), r=20)
    eq(d, W / 2, 440, "A = 8,0 cm: x = 4,0 cm có E_{t} = 0,032 J", 56, DBLUE, alpha=k1)
    kq = appear(t, 2.2, 0.45)
    if kq > 0:
        rail(d, 4.0, ry=700, px=60, labs=(0, 4, 10), alpha=kq)
        text(d, (W / 2, 1010), "Kéo tới A = 10 cm.", 62, INK, alpha=kq)
        eq(d, W / 2, 1110, "Qua x = 4,0 cm, E_{d} bằng bao nhiêu?", 58, DORANGE, alpha=kq)
        seg_bar(d, 1260, t, 2.8, sc["T"] - 0.2, ORANGE, kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, dk, v, da, b, e = sc["hook"], sc["dok"], sc["vach"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (dk["t0"] + H1, "tap"), (v["t0"] + REL, "tap"),
            (v["t0"] + TB, "tick"), (v["t0"] + TC, "tick"), (da["t0"] + da["M"][1] - 0.1, "ding"),
            (b["t0"] + 0.3, "buzz"), (e["t0"] + 2.2, "open")]

CLIP = dict(id="tn-l11-conangdddh-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Cơ năng dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Con lắc lò xo nằm ngang", draw=s_hook, tail=0.3, caps=[
   ("Thả từ biên 8,0 cm.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="dok", title="Đo độ cứng", draw=s_dok, tail=0.3, caps=[
   ("Đo độ dãn khi treo.", 3.0),
   ("Tính ra độ cứng k.", 2.6)]),
 dict(key="vach", title="Năng lượng ở từng vạch", draw=s_vach, tail=0.2, caps=[
   ("Thả từ biên, dừng hình ở từng vạch.", 3.8),
   ("Thế năng giảm, động năng tăng.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.2, caps=[
   ("So phần động năng tăng thêm.", 4.0),
   ("Đoạn đầu nhận nhiều hơn.", 3.0)]),
 dict(key="bay", title="Bẫy: mốc thế năng", draw=s_bay, tail=0.3, caps=[
   ("Treo đứng: dễ đặt sai mốc.", 3.4),
   ("Mốc thế năng đặt ở VTCB.", 3.0)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Bỏ qua ma sát.", 3.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Đổi biên độ.", 2.5),
   ("Dừng lại, tự tính.", 4.2)]),
])
