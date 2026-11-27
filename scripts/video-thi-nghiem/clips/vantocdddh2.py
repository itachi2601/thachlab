# Clip: tn-l11-vantocdddh-02 - Ba do thi x, v, a khi pha ban dau bang 0 (vi_du, ve tu mo hinh)
# (9/11/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 56 px khi ve, K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-vantocdddh-02.json (_kiem_so() doi chieu):
#   tham_so: A = 4 cm, T = 0,8 s, phi = 0 ; mo_hinh: x = A cos(wt), v = -Aw sin(wt), a = -Aw^2 cos(wt), w = 2pi/0,8.
#   so_lieu_mau (t s; x cm; v cm/s; a cm/s2): 0 4 0 -246,7 ; 0,2 0 -31,42 0 ; 0,4 -4 0 246,7 ; 0,6 0 31,42 0.
# Khoi video nam TRUOC Hinh 2 nhung SAU muc 1 ("v som x goc pi/2") va cong thuc a (muc 2) -> ca cu "do thi v dang the nao
#   so voi x" da co dap an trong bai. DOI 27/11: Du doan = DAU cua v va a luc t = 0,3 s (3T/8, giua hai moc kho; chi hoi
#   dau, khong hien so le) -> trai dau: v < 0, a > 0 (vat dang ra bien am, cham dan). Nguon: hien_tuong_hay_sai[1].
# Bay = hien_tuong_hay_sai[1] "a cung pha v": t = 0,2 s v = -31,42 (cuc tieu) ma a = 0 -> a som v goc pi/2 (rut_ra[1]).
# Chua noi duoc: gia_thiet "phi = 0 tren hinh" -> hinh x truot khi phi doi, "phi khac 0 thi sao?".
# Thu nghi (= cau_chot khung web): giu A = 4 cm, doi T = 1,6 s (trong dai tham_so 0,4..2), t = 0,8 s = T/2 -> x = -A
#   -> a = +A(2pi/1,6)^2 = +61,7 cm/s2 (theo mo hinh; can 3 buoc: t = T/2, dau, omega^2 giam 4 lan). KHONG hien dap so.
#   Nhieu: -246,7 (doc thang do thi cu tai 0,8 s), -61,7 (sai dau), +123,4 (chia 2 thay vi 4).
from engine import *

AMP, PER = 4.0, 0.8
VM, AM = 31.42, 246.7                                       # |v|max, |a|max trong so_lieu_mau
OMG = 2 * math.pi / PER
ROWS = [("0", "4", "0", "−246,7"), ("0,2", "0", "−31,42", "0"), ("0,4", "−4", "0", "246,7"), ("0,6", "0", "31,42", "0")]
TS = [0.0, 0.2, 0.4, 0.6]
TQ = 0.3                                                    # moc du doan (chi hoi dau)
def xf(t): return AMP * math.cos(OMG * t)
def vf(t): return -VM * math.sin(OMG * t)
def af(t): return -AM * math.cos(OMG * t)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-vantocdddh-02.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["A"]["mac_dinh"] == AMP and tp["T"]["mac_dinh"] == PER and tp["phi"]["mac_dinh"] == 0
    for r, h in zip(ROWS, k["so_lieu_mau"]["hang"]):
        assert [float(s.replace(",", ".").replace("−", "-")) for s in r] == [float(v) for v in h], (r, h)
        t = h[0]
        assert abs(xf(t) - h[1]) < 6e-3 and abs(vf(t) - h[2]) < 6e-3 and abs(af(t) - h[3]) < 0.06
    assert vf(TQ) < 0 and af(TQ) > 0                       # dap an du doan
    assert tp["T"]["min"] <= 1.6 <= tp["T"]["max"]
    assert abs(-AMP * (2 * math.pi / 1.6) ** 2 * math.cos(2 * math.pi / 1.6 * 0.8) - 61.7) < 0.05   # cau chot
_kiem_so()

DGREEN = (21, 110, 55); DRED = (185, 28, 28); DBLUE = (29, 78, 216); DTEAL = (15, 118, 110); EMPTY = (148, 140, 128)
BLOCK = (59, 130, 246); RAILC = (120, 125, 145)

# ---------------- ba do thi (khung nguon 1080x1920; mp4 x = 65 + 0,88 x) ----------------
GX0, GSX = 230, 837.5               # t = 0 o px 230 ; 0,8 s o px 900
H2 = 85                             # nua chieu cao duong cong
def gx(t): return GX0 + t * GSX
SER = {   # khoa: (tam y, ham, dinh, ten, don vi, mau)
    "x": (350, xf, AMP, "x", "cm", DTEAL),
    "v": (590, vf, VM, "v", "cm/s", DBLUE),
    "a": (830, af, AM, "a", "cm/s²", DRED),
}
TLAB = 965
def gy(k, val):
    c, _, pk, *_ = SER[k]
    return c - val / pk * H2

def axes(d, a=1.0, tlab=True):
    top = SER["x"][0] - 110; bot = SER["a"][0] + 105
    for tt in (0.2, 0.4, 0.6, 0.8):
        for yy in range(int(top), int(bot), 26): d.line([(gx(tt), yy), (gx(tt), yy + 12)], fill=A(LIGHT, a), width=3)
    for k, (c, _, pk, nm, un, col) in SER.items():
        arrow(d, (GX0, c + 100), (GX0, c - 112), A(NAVY, a), w=4, head=16)
        arrow(d, (GX0, c), (gx(0.88), c), A(NAVY, a), w=4, head=16)
        text(d, (115, c - 34), nm, 64, col, alpha=a)
        text(d, (115, c + 36), un, 56, col, alpha=a)
    if tlab:
        for tt in (0.2, 0.4, 0.6):
            text(d, (gx(tt), TLAB), f"{tt:.1f}".replace(".", ","), 56, NAVY, alpha=a)
        text(d, (GX0, TLAB), "0", 56, NAVY, alpha=a)
        text(d, (gx(0.8) + 20, TLAB), "0,8 s", 56, NAVY, alpha=a)

def curve(d, k, t1, a=1.0, w=7, phi=0.0):
    if t1 <= 0: return
    c, f, pk, _, _, col = SER[k]
    n = max(2, int(t1 * 300))
    pts = []
    for i in range(n + 1):
        tt = t1 * i / n
        val = f(tt) if phi == 0 else pk * math.cos(OMG * tt + phi)
        pts.append((gx(tt), c - val / pk * H2))
    d.line(pts, fill=A(col, a), width=w, joint="curve")

def cursor(d, tt, keys=("x", "v", "a"), col=PURPLE, a=1.0):
    d.line([(gx(tt), SER["x"][0] - 105), (gx(tt), SER["a"][0] + 100)], fill=A(col, 0.85 * a), width=5)
    for k in keys:
        dot(d, gx(tt), gy(k, SER[k][1](tt)), 15, A(SER[k][5], a), outline=A(WHITE, a))

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=170, n=5):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI; o da tat: nen trang, vien dam."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9)
    for i in range(n):
        x = x0 + i * 152
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=16)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def pill(d, cy, s, col, a=1.0, size=56):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, cy - 40, W / 2 + pw / 2, cy + 40), fill=A(col, a), r=40)
    text(d, (W / 2, cy), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh; v, a de trong) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    axes(d)
    curve(d, "x", PER * clamp((t - 0.6) / 1.8))
    kq = appear(t, 2.8, 0.45)
    if kq > 0:
        d.line([(gx(TQ), SER["x"][0] - 105), (gx(TQ), SER["a"][0] + 100)], fill=A(PURPLE, 0.85 * kq), width=5)
        dot(d, gx(TQ), gy("x", xf(TQ)), 15, A(DTEAL, kq), outline=A(WHITE, kq))
        for k in ("v", "a"): text(d, (gx(TQ) + 90, SER[k][0] - 45), "?", 64, PURPLE, alpha=kq)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1050 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Lúc t = 0,3 s,", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "v và a cùng dấu hay trái dấu?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (con tro dung o 4 moc kho, dien bang) ----------------
D0, HOLD, MOVE = 0.4, 1.2, 0.9
def phase(v):
    """-> (t do thi, so cot bang da co, chi so moc dang dung hoac None)."""
    if v < D0: return 0.0, 0, None
    u = v - D0
    for i in range(4):
        if u < HOLD: return TS[i], i + 1, i
        u -= HOLD
        if u < MOVE: return TS[i] + 0.2 * u / MOVE, i + 1, None
        u -= MOVE
    return PER, 4, None

TY0 = 1060
def table(d, ncol, cur=None):
    card(d, (40, TY0, 1040, TY0 + 330), fill=WHITE, outline=NAVY, r=20, w=3)
    labs = ("t", "x", "v", "a"); cols = (INK, DTEAL, DBLUE, DRED)
    for r in range(4):
        y = TY0 + 48 + r * 78
        if r: d.line([(56, y - 39), (1024, y - 39)], fill=LIGHT, width=2)
        text(d, (110, y), labs[r], 60, cols[r])
        for i in range(4):
            cx = 290 + i * 215
            if r == 0:
                if cur == i: card(d, (cx - 104, TY0 + 8, cx + 104, TY0 + 322), fill=(255, 237, 213), r=14)
                text(d, (cx, y), ROWS[i][0], 58, INK)
            elif i < ncol: text(d, (cx, y), ROWS[i][r], 58, cols[r])

def s_do(img, d, t, sc):
    tt, n, cur = phase(t)
    axes(d)
    for k in ("x", "v", "a"): curve(d, k, tt)
    if t >= D0: cursor(d, tt)
    table(d, n, cur)

def _kiem_dong_bo():
    bad = []
    for i, ts in enumerate(TS):
        tt, n, cur = phase(D0 + i * (HOLD + MOVE) + 0.5)
        if not (abs(tt - ts) < 1e-9 and n == i + 1 and cur == i): bad.append((i, tt, n, cur))
    return bad

# ---------------- canh 3: Dap an (dau tai t = 0,3 s) + co che ----------------
XO, PX = 560, 70
def mini(d, y, x_cm, a=1.0):
    d.rectangle([60, y - 50, 78, y + 50], fill=A(GRAY, a))
    d.rectangle([60, y + 42, 1020, y + 54], fill=A(RAILC, a))
    for yy in range(y - 56, y + 42, 18): d.line([(XO, yy), (XO, yy + 9)], fill=A(NAVY, a), width=3)
    xc = XO + x_cm * PX
    pts = [(78, y)]; L = xc - 45 - 78
    for i in range(1, 16): pts.append((78 + L * i / 16, y + (16 if i % 2 else -16)))
    pts.append((xc - 45, y)); d.line(pts, fill=A(NAVY, a), width=4)
    d.rounded_rectangle([xc - 45, y - 36, xc + 45, y + 36], radius=10, fill=A(BLOCK, a), outline=A(NAVY, a), width=3)
    return xc

def s_dapan(img, d, t, sc):
    M = sc["M"]
    axes(d)
    for k in ("x", "v", "a"): curve(d, k, PER)
    cursor(d, TQ)
    k1 = appear(t, 0.4, 0.4)
    if k1 > 0:
        text(d, (gx(TQ) + 40, 695), "v < 0", 60, DBLUE, anchor="lm", alpha=k1)
        text(d, (gx(TQ) - 40, 770), "a > 0", 60, DRED, anchor="rm", alpha=k1)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0: pill(d, 1075, "ĐÁP ÁN · trái dấu", NAVY, kb)
    km = appear(t, M[1] + 2.4, 0.45)                       # vat that: 0,2 -> 0,4 s di tu O ra bien am
    if km > 0:
        card(d, (40, 1160, 1040, 1560), fill=A(WHITE, km), outline=A(LIGHT, km), w=3)
        u = clamp((t - M[1] - 2.4) / 2.0)
        tt = 0.2 + 0.2 * u * 0.75                           # 0,2 -> 0,35 s: con dang ra bien, chua dung
        xc = mini(d, 1300, xf(tt), km)
        lv = 40 + 140 * abs(vf(tt)) / VM; la = 40 + 140 * af(tt) / AM
        arrow(d, (xc, 1210), (xc - lv, 1210), A(BLUE, km), w=8, head=24)
        text(d, (xc + 30, 1210), "v", 60, DBLUE, anchor="lm", alpha=km)
        arrow(d, (xc, 1400), (xc + la, 1400), A(RED, km), w=8, head=24)
        text(d, (xc - 30, 1400), "a", 60, DRED, anchor="rm", alpha=km)
        text(d, (XO, 1490), "O", 58, NAVY, alpha=km)
        text(d, (XO - 4 * PX, 1490), "−4 cm", 58, NAVY, alpha=km)

# ---------------- canh 4: Bay (a cung pha v?) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d)
    for k in ("x", "v", "a"): curve(d, k, PER)
    card(d, (60, 1060, 1020, 1180), fill=(254, 242, 242), outline=DRED, r=24, w=6)
    text(d, (W / 2, 1120), "✗ Dễ tưởng: a cùng pha với v", 58, DRED)
    k2 = appear(t, M[1] - 0.1, 0.45)                       # nhip 2: con tro truot toi 0,2 s
    if k2 > 0:
        tt = 0.2 * ease((t - M[1] + 0.1) / 1.0)
        cursor(d, tt, keys=("v", "a"), a=k2)
        if tt >= 0.2 - 1e-9:
            text(d, (gx(0.2) + 40, gy("v", -VM) + 10), "v = −31,42", 58, DBLUE, anchor="lm")
            text(d, (gx(0.2) - 30, 780), "a = 0", 58, DRED, anchor="rm")
        card(d, (60, 1220, 1020, 1340), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=24, w=6)
        text(d, (W / 2, 1280), "✓ v cực tiểu thì a = 0", 58, DGREEN, alpha=k2)

# ---------------- canh 5: Chua noi duoc (phi khac 0) ----------------
def s_gioihan(img, d, t, sc):
    axes(d, tlab=False)
    phi = math.pi / 2 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 3.2))   # minh hoa: phi doi -> duong x truot (khong so)
    curve(d, "x", PER, phi=phi)
    card(d, (40, 1040, 1040, 1380), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 1125), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 1270), "φ khác 0 thì sao?", 62, INK)

# ---------------- canh 6: Chot + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 290, "THỬ NGHĨ", ORANGE, k1)
    for j, (lab, val) in enumerate((("A", "4 cm"), ("T", "1,6 s"), ("t", "0,8 s"))):
        x0 = 80 + j * 315
        card(d, (x0, 400, x0 + 290, 610), fill=A((245, 243, 255), k1), outline=A(PURPLE, k1), r=18, w=3)
        text(d, (x0 + 145, 455), lab, 62, PURPLE, alpha=k1)
        text(d, (x0 + 145, 550), val, 60, INK, alpha=k1)
    kq = appear(t, 2.6, 0.45)
    if kq > 0:
        text(d, (W / 2, 760), "Giữ A, đổi T thành 1,6 s.", 60, INK, alpha=kq)
        text(d, (W / 2, 870), "Lúc t = 0,8 s, a bằng bao nhiêu?", 60, DRED, alpha=kq)
        seg_bar(d, 1010, t, 3.2, sc["T"] - 0.2, ORANGE, kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + D0, "tap")]
    out += [(do["t0"] + D0 + i * (HOLD + MOVE), "tick") for i in (1, 2, 3)]
    out += [(da["t0"] + da["M"][1] - 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 2.6, "open")]
    return out

CLIP = dict(id="tn-l11-vantocdddh-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Vận tốc, gia tốc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba đồ thị, một trục thời gian", draw=s_hook, tail=0.3, caps=[
   ("A = 4 cm, T = 0,8 s, φ = 0.", 3.6),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Dừng ở mỗi mốc 0,2 s, đọc số.", 4.2),
   ("Ba chấm cùng một thời điểm.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đọc dấu tại t = 0,3 s.", 3.6),
   ("Vật đang ra biên âm, chậm dần.", 4.8)]),
 dict(key="bay", title="Bẫy: so v với a", draw=s_bay, tail=0.4, caps=[
   ("Hai đỉnh có trùng nhau không?", 3.4),
   ("a sớm v một góc π/2.", 3.6)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Ở đây mới vẽ ca φ = 0.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Đọc cả ba đồ thị ở cùng một t.", 3.4),
   ("Dừng lại, tự tính.", 4.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
