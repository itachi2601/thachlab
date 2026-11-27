# Clip: tn-l11-vantocdddh-01 - Con lac lo xo nam ngang: do A, T roi tinh v_max va a
# (31/10/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 56 px khi ve, K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-vantocdddh-01.json (_kiem_so() doi chieu):
#   tham_so: A = 4,0 cm (sai so thuoc 0,1 cm); T tb 0,800 s (sai_so_do 0,007 s); x tu -4 toi 4 cm.
#   cac_buoc.lam: t10 nam lan 8,02; 7,96; 8,08; 7,94; 8,00 s. quan_sat: T tb 0,800 s; omega = 7,854 rad/s; v_max = 31,42 cm/s;
#   x = 2,0 cm: a = -123,4 cm/s2.
# Du doan (DOI 27/11: ca cu "tu O ra bien toc do/|a| doi the nao" trung quiz mo bai + quiz Bay 2 cua bai):
#   thuoc lech 1 mm hay bam gio lech vai phan tram giay lam v_max sai nhieu hon? -> THUOC (dA/A = 2,5 % > dT/T ~ 0,9 %).
#   Nguon: hien_tuong_hay_sai[2] "coi lech bam gio lon hon sai so thuoc do A", sai_so_thuong_gap, rut_ra[2].
# Bay = hien_tuong_hay_sai[1] "tuong a cung dau x": vat o x = +2,0 cm, a = -123,4 cm/s2 chi ve O (hai nhip >= 3 s).
# Chua noi duoc: gia_thiet "bo qua ma sat, bien do khong doi" -> hinh dao dong tat dan, "ma sat lon thi sao?".
# Thu nghi (= cau_chot khung web): x = -3,0 cm (trong dai tham_so x, chua chieu) -> a = -omega^2 x = +185,1 cm/s2
#   (theo mo hinh; can 2 buoc: doi dau + ti le 3/2 tu x = 2,0 cm). Dap so KHONG hien tren man.
from engine import *

A_CM, T_TB, OMEGA, DT = 4.0, 0.800, 7.854, 0.007
T10 = [8.02, 7.96, 8.08, 7.94, 8.00]                    # cac_buoc.lam (lan 5 = lan quay)
VMAX = 31.42; X2, A2 = 2.0, -123.4
FAST = 2.0                                              # tua nhanh x2
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-vantocdddh-01.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["A"]["mac_dinh"] == A_CM and tp["A"]["sai_so_do"] == 0.1 and tp["T"]["sai_so_do"] == DT
    assert [h[1] for h in k["so_lieu_mau"]["hang"]] == T10
    q = " ".join(k["cac_buoc"]["quan_sat"])
    for s in ("0,800", "7,854", "31,42", "−123,4"): assert s in q, s
    w = 2 * math.pi / T_TB
    assert abs(w - OMEGA) < 6e-4 and abs(A_CM * w - VMAX) < 6e-3 and abs(-w * w * X2 - A2) < 0.06
    assert abs(sum(T10) / 50 - T_TB) < 1e-9 and abs((max(T10) - min(T10)) / 20 - DT) < 1e-9
    assert abs(-w * w * -3.0 - 185.1) < 0.06 and -4 <= -3.0 <= 4              # cau chot (theo mo hinh)
_kiem_so()

DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8)
BLOCK = (59, 130, 246); RAILC = (120, 125, 145); EMPTY = (148, 140, 128)

_TI = {}
def TI(size):                                           # Times Bold Italic cho omega (omega cua SF giong chu w)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi cong thuc: 'ω' ve bang Times Bold Italic; _{..} chi so duoi (>= 56 px)."""
    fs = []
    for p in [p for p in re.split(r"(ω|_\{[^}]*\})", s) if p]:
        if p == "ω": fs.append((p, TI(size * 1.12), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(max(56, size * 0.7)), size * 0.24))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

# ---------------- ray (khung nguon 1080x1920; mp4 x = 65 + 0,88 x) ----------------
XO, PX = 560, 90                    # x man hinh cua O; px moi cm -> +-4 cm = 200..920 (+55 = 975 -> mp4 923)
BW, BH = 110, 90
WALL = 72
def X(x_cm): return XO + x_cm * PX

def spring(d, xa, xb, y, amp=24, n=9, col=NAVY, w=5):
    e = 12; pts = [(xa, y), (xa + e, y)]
    L = (xb - e) - (xa + e)
    for i in range(1, 2 * n):
        pts.append((xa + e + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(xb - e, y), (xb, y)]
    d.line(pts, fill=col, width=w, joint="curve")

def rail(d, x_cm, ry=400, ruler=True, alpha=1.0):
    """Tuong trai, lo xo, vat tam X(x_cm), vach O net dut, thuoc duoi ray (nhan chan, 56 px)."""
    c = lambda col: A(col, alpha)
    d.rectangle([50, ry - 70, WALL, ry + 62], fill=c(GRAY))
    for yy in range(ry - 60, ry + 60, 24): d.line([(50, yy + 14), (WALL - 2, yy)], fill=c(NAVY), width=2)
    d.rectangle([50, ry + 48, 1020, ry + 62], fill=c(RAILC))
    for yy in range(ry - 70, ry + 48, 22): d.line([(XO, yy), (XO, yy + 11)], fill=c(NAVY), width=3)
    xc = X(x_cm)
    spring(d, WALL, xc - BW / 2, ry, col=c(NAVY))
    d.rounded_rectangle([xc - BW / 2, ry - BH / 2, xc + BW / 2, ry + BH / 2], radius=12, fill=c(BLOCK), outline=c(NAVY), width=4)
    text(d, (xc, ry), "m", 56, WHITE, alpha=alpha)
    if not ruler: return
    y0 = ry + 75
    d.rectangle([X(-4.5), y0, X(4.5), y0 + 40], fill=c((250, 240, 200)), outline=c(NAVY), width=2)
    for k in range(-45, 46, 5):
        L = 22 if k % 10 == 0 else 12
        d.line([(X(k / 10), y0), (X(k / 10), y0 + L)], fill=c(NAVY), width=3 if L == 22 else 2)
    for k in (-4, -2, 0, 2, 4):
        text(d, (X(k), y0 + 85), (str(k) if k >= 0 else "−" + str(-k)), 56, INK, alpha=alpha)
    text(d, (1000, y0 + 85), "cm", 56, INK, alpha=alpha)

def stopwatch(d, box, s, alpha=1.0, sub=None):
    x0, y0, x1, y1 = box; cx = (x0 + x1) / 2
    card(d, box, fill=A((70, 78, 100), alpha), r=24)
    card(d, (x0 + 30, y0 + 28, x1 - 30, y0 + 138), fill=A((220, 240, 225), alpha), r=14)
    text(d, (cx, y0 + 83), vn(s) + " s", 76, (20, 60, 30), alpha=alpha)
    if sub: text(d, (cx, y0 + 192), sub, 56, WHITE, alpha=alpha)

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

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rail(d, A_CM)
    k = appear(t, 0.6, 0.5)                              # do lech 4,0 cm (O -> vat), mui ten tren vat
    if k > 0:
        arrow(d, (XO + 6, 300), (X(A_CM) - 6, 300), A(ORANGE, k), w=6, head=20)
        text(d, ((XO + X(A_CM)) / 2, 250), "4,0 cm", 58, DORANGE, alpha=k)
    a = appear(t, M[1] - 0.2, 0.5)
    stopwatch(d, (300, 700, 780, 920), 0.0, alpha=max(appear(t, 1.2, 0.5), 0))
    if a <= 0: return
    y0 = 960 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 170), "Thước lệch 1 mm.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Bấm giờ 10 dao động,", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 330), "lệch vài phần trăm giây.", 58, INK, alpha=a)
    eq(d, W / 2, y0 + 425, "Cái nào làm v_{max} sai hơn?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 500, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
REL = 0.3                       # tha vat sau M[1] + REL
def do_state(t, sc):
    """-> (s dong ho, x cm, so dao dong dem duoc, da dung). Mot nguon duy nhat cho vat, dong ho, bang."""
    M = sc["M"]
    if t < M[1] + REL: return 0.0, A_CM, 0, False
    s = min(T10[4], (t - M[1] - REL) * FAST)
    x = A_CM * math.cos(2 * math.pi * s / T_TB)
    n = int(s / T_TB + 1e-6)
    return s, x, n, s >= T10[4] - 1e-9

def s_do(img, d, t, sc):
    M = sc["M"]
    s, x, n, stop = do_state(t, sc)
    rail(d, x)
    ka = appear(t, 0.9, 0.4)                             # thuoc: A = 4,0 cm (chi khi vat con o bien)
    if ka > 0 and t < M[1] + REL:
        y = 300
        d.line([(XO, y), (X(A_CM), y)], fill=A(ORANGE, ka), width=6)
        for xx in (XO, X(A_CM)): d.line([(xx, y - 18), (xx, y + 18)], fill=A(ORANGE, ka), width=6)
        text(d, ((XO + X(A_CM)) / 2, 250), "A = 4,0 cm", 58, DORANGE, alpha=ka)
    if t < M[1] - 0.2: return
    kb = appear(t, M[1] - 0.2, 0.4)
    stopwatch(d, (50, 700, 500, 940), s, alpha=kb, sub=f"đếm {n}/10")
    if not stop:
        card(d, (70, 965, 480, 1045), fill=A(ORANGE, kb), r=40); text(d, (275, 1005), "tua nhanh ×2", 56, WHITE, alpha=kb)
    tx0, tx1, ty0 = 540, 1030, 700                       # bang t10: lan 1-4 da do, lan 5 dien khi dong ho dung
    card(d, (tx0, ty0, tx1, ty0 + 470), fill=A(WHITE, kb), outline=A(NAVY, kb), r=20, w=3)
    text(d, (630, ty0 + 48), "Lần", 56, INK, alpha=kb)
    eq(d, 860, ty0 + 48, "t_{10} (s)", 56, INK, alpha=kb)
    d.line([(tx0 + 10, ty0 + 92), (tx1 - 10, ty0 + 92)], fill=A(NAVY, kb), width=3)
    for i, v in enumerate(T10):
        y = ty0 + 140 + i * 70
        if i == 4:
            if not stop: text(d, (630, y), "5", 56, INK, alpha=kb); continue
            kr = appear(t, M[1] + REL + T10[4] / FAST + 0.05, 0.3)
            d.rounded_rectangle([tx0 + 14, y - 32, tx1 - 14, y + 32], radius=10, fill=A((255, 237, 213), kr))
        text(d, (630, y), str(i + 1), 56, INK, alpha=kb)
        text(d, (860, y), vn(v), 56, INK, alpha=kb)
    if stop:                                             # T trung binh, omega, v_max
        kt = appear(t, M[1] + REL + T10[4] / FAST + 0.4, 0.45)
        card(d, (40, 1200, 1040, 1440), fill=A((239, 246, 255), kt), outline=A(BLUE, kt), r=22, w=3)
        eq(d, W / 2, 1265, "T = 0,800 s       ω = 7,854 rad/s", 58, INK, alpha=kt)
        eq(d, W / 2, 1370, "v_{max} = Aω = 31,42 cm/s", 58, DBLUE, alpha=kt)

def _kiem_dong_bo():
    sc = {"M": [0.4, 3.6]}; bad = []
    s, x, n, stop = do_state(3.6 + REL + T10[4] / FAST + 0.01, sc)
    if not (stop and n == 10 and abs(x - A_CM) < 1e-6): bad.append(("dung sai", s, x, n))
    return bad

# ---------------- canh 3: Ket qua = so hai phan sai so ----------------
PCT = 240.0                                             # px moi 0,01 (1 %)
BX0 = 330
def bar(d, y, lab, col, pct, k, val, a):
    text(d, (BX0 - 30, y), lab, 58, col, anchor="rm", alpha=a)
    d.rounded_rectangle([BX0, y - 38, BX0 + 2.5 * PCT, y + 38], radius=14, outline=A(EMPTY, a), width=3)
    if k > 0: d.rounded_rectangle([BX0, y - 38, BX0 + max(30, pct * PCT * k), y + 38], radius=14, fill=A(col, a))
    text(d, (W / 2 + 30, y + 105), val, 56, col, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 820), fill=WHITE, outline=LIGHT, w=3)
    bar(d, 330, "thước", DORANGE, 2.5, ease((t - 0.4) / 1.4), "0,1 cm / 4,0 cm = 0,025", appear(t, 0.4, 0.4))
    if t > 2.9:
        bar(d, 600, "bấm giờ", DBLUE, DT / T_TB * 100, ease((t - 2.9) / 1.4), "0,007 s / 0,800 s ≈ 0,009", appear(t, 2.9, 0.4))
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        pill(d, 920, "ĐÁP ÁN · thước đo A", NAVY, kb)
        card(d, (60, 1030, 1020, 1300), fill=A((239, 246, 255), kb), outline=A(BLUE, kb), r=24, w=4)
        eq(d, W / 2, 1110, "T = t_{10} / 10", 60, DBLUE, alpha=kb)
        k = ease((t - M[1]) / 2.5)                       # vach "10 dao dong" chay dan: loi bam chia deu cho 10
        for i in range(10):
            xx = 150 + i * 78
            d.rounded_rectangle([xx, 1200, xx + 60, 1250], radius=10, fill=A(BLUE if i < 10 * k else LIGHT, kb))

# ---------------- canh 4: Bay (a cung dau x) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    rail(d, X2, ry=480)
    d.line([(XO + 4, 360), (X(X2) - 4, 360)], fill=ORANGE, width=6)
    arrow(d, (XO + 4, 360), (X(X2) - 4, 360), ORANGE, w=6, head=20)
    text(d, (XO - 30, 360), "x = +2,0 cm", 58, DORANGE, anchor="rm")
    k1 = 1.0
    card(d, (60, 800, 1020, 920), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=24, w=6)
    text(d, (W / 2, 860), "✗ Dễ tưởng: x dương thì a dương", 56, DRED, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)                     # nhip 2: mui ten a chi ve O (lo xo dang dan, keo vat ve)
    if k2 > 0:
        L = 123.4 * 1.6 * ease((t - M[1] + 0.1) / 0.8)
        arrow(d, (X(X2), 700), (X(X2) - max(30, L), 700), A(RED, k2), w=9, head=28)
        text(d, (X(X2) + 70, 700), "a", 64, DRED, alpha=k2)
        card(d, (60, 960, 1020, 1240), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=24, w=6)
        text(d, (W / 2, 1035), "✓ a chỉ về O", 60, DGREEN, alpha=k2)
        text(d, (W / 2, 1150), "a = −123,4 cm/s²", 60, INK, alpha=k2)

# ---------------- canh 5: Chua noi duoc (dao dong tat dan) ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Nếu có ma sát?", 62, INK)
    amp = A_CM * math.exp(-0.45 * t)                     # minh hoa: bien do nho dan khi co ma sat (khong ghi so)
    rail(d, amp * math.cos(2 * math.pi * t / 1.6), ry=760, ruler=False)
    text(d, (W / 2, 620), "biên độ", 56, PURPLE)
    arrow(d, (W / 2 - 10, 680), (X(-amp), 680), PURPLE, w=6, head=18)
    arrow(d, (W / 2 + 10, 680), (X(amp), 680), PURPLE, w=6, head=18)

# ---------------- canh 6: Chot + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 290, "THỬ NGHĨ", ORANGE, k1)
    card(d, (80, 380, 1000, 500), fill=A((239, 246, 255), k1), r=20)
    text(d, (W / 2, 440), "x = +2,0 cm: a = −123,4 cm/s²", 56, DBLUE, alpha=k1)
    kq = appear(t, 2.6, 0.45)                            # ca moi hien sau 2,5 s (nhip rieng)
    rail(d, -3.0, ry=700, alpha=kq)
    if kq > 0:
        text(d, (X(-3.0), 590), "a = ?", 62, PURPLE, alpha=kq)
        text(d, (W / 2, 1010), "Vật ở x = −3,0 cm.", 62, INK, alpha=kq)
        text(d, (W / 2, 1110), "Gia tốc bằng bao nhiêu?", 62, DORANGE, alpha=kq)
        seg_bar(d, 1260, t, 3.2, sc["T"] - 0.2, ORANGE, kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    rel = do["t0"] + do["M"][1] + REL
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + 0.15, "ding"), (rel, "tap")]
    out += [(rel + k * T_TB / FAST, "tick") for k in range(1, 10)]
    out += [(rel + T10[4] / FAST, "tap")]
    out += [(da["t0"] + da["M"][1] - 0.1, "ding"), (b["t0"] + 0.5, "buzz"), (e["t0"] + 2.6, "open")]
    return out

CLIP = dict(id="tn-l11-vantocdddh-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Vận tốc, gia tốc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Con lắc lò xo nằm ngang", draw=s_hook, tail=0.3, caps=[
   ("Kéo lệch 4,0 cm rồi thả.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đo biên độ bằng thước.", 3.2),
   ("Bấm giờ 10 dao động, năm lần.", 6.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So hai phần sai số.", 5.0),
   ("Bấm giờ 10 dao động, chia 10.", 3.6)]),
 dict(key="bay", title="Bẫy: dấu của a", draw=s_bay, tail=0.4, caps=[
   ("Vật lệch sang phải O.", 3.4),
   ("Lò xo kéo vật về O.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Ma sát chưa xét.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Sai số chủ yếu do thước.", 3.4),
   ("Dừng lại, tự tính.", 4.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
