# Clip: tn-l9-hsgamthanh-01 - Thuoc nhua rung tren mep ban: do cao theo tan so (HSG KHTN 9, CD15, lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-hsgamthanh-01.json (_kiem_so() doi chieu ca mo_hinh f = 25(15/L)^2):
#   so_lieu_mau (L cm, f Hz): 25 9 | 15 25 | 10 56,3 | 5 225 (so minh hoa). ghi_chu: f duoi 20 Hz la ha am, kho nghe.
# Hinh: thuoc rung ve bang QUAT VET MO (khong ve pha theo thoi gian: 25-225 Hz o 30 khung/s bi "chay nguoc" de doc sai);
#   toc do rung doc qua so f va do thi "cung mot khoang thoi gian" (khong ghi so giay de khoi them so ngoai kho).
# Du doan (K10, khong nut A-D): tho 15 cm -> 25 Hz ; tho ngan hon 10 cm: tan so va do cao the nao? -> f lon hon, am cao hon.
#   Khac cau Hinh 2 (doc do thi 500/1000 Hz), cau dinh-day 0,5 ms, cau Mat Trang, cau 680 Hz vao nuoc.
# Bay = hien_tuong_hay_sai[1] + [2] (tho dai rung rong nen keu to va cao; that ra 9 Hz duoi 20 Hz, kho nghe).
#   Khong dung [0] (gay manh -> cao) vi gan y cau Hinh 2 ngay sau hop.
# Chua noi duoc: gia_thiet "f_15 la gia tri minh hoa, tuy loai thuoc".
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, khoi chu cach >= 2,5 s.
# Cau chot cu (T = 1/225 s) la phep tinh tran -> bo. Cau chot MOI (tu suy, kho chua ghi): tho 7,5 cm -> f khoang bao nhieu?
#   HS phai tu rut tu bang: tho ngan con mot nua (10 -> 5 cm) thi f gap 4 (56,3 -> 225) ; ap cho 15 -> 7,5 cm: 25 . 4 = 100 Hz
#   (dung mo_hinh f = 25(15/L)^2). Clip KHONG noi "mot nua -> gap 4"; man chot khong hien bang.
# GĐ2 27/11 (kiem-code: 1/L^2 khong co trong bai CĐ15) -> doi chot: tho 12 cm, f nam trong khoang nao? -> 25-56,3 Hz
#   (12 cm nam giua 15 cm va 10 cm da chieu; chi can xu huong "tho ngan hon -> f lon hon"). Mo hinh cho 39 Hz.
from engine import *

ROWS = [(25, 9), (15, 25), (10, 56.3), (5, 225)]          # so_lieu_mau
CH_L = 12                                                 # cau chot GĐ2: tho 12 cm -> f nam giua 25 va 56,3 Hz (khong can 1/L^2)
def fz(L): return dict(ROWS)[L]
def vn(x): return ("%g" % x).replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-hsgamthanh-01.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    for L, f in ROWS: assert abs(25 * (15 / L) ** 2 - f) / f < 0.03, (L, f)        # mo_hinh
    assert "20 Hz" in k["so_lieu_mau"]["ghi_chu"] and fz(25) < 20
    assert 10 < CH_L < 15 and fz(15) < 25 * (15 / CH_L) ** 2 < fz(10)                    # ca chot nam giua hai diem da chieu
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert all(tp["L"]["min"] <= L <= tp["L"]["max"] for L, _ in ROWS + [(CH_L, 0)])
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
RULER = (37, 99, 235); WAVE = (124, 58, 237)

# ---------------- hinh: ban + thuoc + quat rung ----------------
EDGE, TY, PXC, AMP = 330, 500, 26.0, 62       # mep ban x ; mat ban y ; px moi cm ; bien do dau thuoc (px)
def ruler(d, L, vib=True, a=1.0, amp=AMP):
    d.rectangle([40, TY, EDGE, TY + 120], fill=A(WOOD, a), outline=A(WOOD_D, a), width=3)          # ban
    d.rectangle([60, TY - 12, EDGE, TY], fill=A(RULER, a))                                          # phan nam tren ban
    d.rounded_rectangle([210, TY - 92, EDGE - 6, TY - 12], radius=18, fill=A((232, 190, 160), a), outline=A((150, 110, 90), a), width=3)
    x1 = EDGE + L * PXC
    def shape(s): return s * s * (3 - s) / 2          # dang uon thanh cong-xon (chi de ve)
    pts = lambda p: [(EDGE + (x1 - EDGE) * i / 30, TY - 6 + p * amp * shape(i / 30)) for i in range(31)]
    if vib:
        for k in range(-4, 5):
            p = k / 4
            d.line(pts(p), fill=A(RULER, a * (0.5 if abs(k) == 4 else 0.16)), width=12)
    else:
        d.line(pts(0), fill=A(RULER, a), width=12)
    # thuoc do phan tho ra (duoi), chu "tho ra L cm" khong dung ky hieu l
    yb = TY + 150
    d.line([(EDGE, yb), (x1, yb)], fill=A(NAVY, a), width=3)
    for x in (EDGE, x1): d.line([(x, yb - 14), (x, yb + 14)], fill=A(NAVY, a), width=3)
    return x1, yb

def fbox(d, f, a=1.0):
    s = "f = " + (vn(f) + " Hz" if f is not None else "?")
    card(d, (620, 285, 1025, 385), fill=A(NAVY, a), r=20)
    text(d, (822, 335), s, 56, (253, 224, 71), alpha=a)

def graph(d, f, y0=700, a=1.0, cap=True):
    card(d, (40, y0, 1040, y0 + 270), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    if cap: text(d, (W / 2, y0 + 45), "cùng thời gian", 56, MUTED, alpha=a)
    yc = y0 + 165; x0, x1 = 90, 990
    d.line([(x0, yc), (x1, yc)], fill=A(LIGHT, a), width=3)
    if f is None: return
    WT = 0.2                                             # cua so (chi de ve, khong hien so)
    n = 900 if f > 100 else 300
    pts = [(x0 + (x1 - x0) * i / n, yc - 60 * math.sin(2 * math.pi * f * WT * i / n)) for i in range(n + 1)]
    d.line(pts, fill=A(WAVE, a), width=4)

def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    x1, yb = ruler(d, 15)
    text(d, ((EDGE + x1) / 2, yb + 50), "15 cm", 56, NAVY)
    fbox(d, 25)
    graph(d, 25, y0=780, cap=False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1080 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Thò ra chỉ 10 cm:", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "âm cao hơn hay trầm hơn?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 340, 970, y0 + 430], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 340, 110 + max(90, 860 * (1 - p)), y0 + 430], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: Tien hanh ----------------
# (bat dau doi, xong doi, L moi) ; truoc moc dau: L = 15 dang rung
MOVES = [(0.6, 1.3, 10), (3.9, 4.6, 5), (6.6, 7.6, 25)]
ROW_LAG = 0.6
def do_state(t):
    """-> (L dang ve, dang rung?, f doc (None khi dang doi), cac L da co hang)."""
    L, vib, done = 15.0, True, {15}
    for t0, t1, Ln in MOVES:
        if t < t0: break
        if t < t1: L = lerp(L, Ln, ease((t - t0) / (t1 - t0))); vib = False; break
        L = Ln; vib = True
        if t >= t1 + ROW_LAG: done.add(Ln)
    return L, vib, (fz(L) if vib else None), done

def table(d, y, done, hl=()):
    card(d, (40, y, 1040, y + 450), fill=WHITE, outline=NAVY, w=4)
    xs = (300, 760)
    text(d, (xs[0], y + 55), "thò ra (cm)", 56, NAVY); text(d, (xs[1], y + 55), "f (Hz)", 56, WAVE)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=4)
    for i, (L, f) in enumerate(ROWS):
        yy = y + 155 + i * 80
        if L in hl: d.rounded_rectangle([60, yy - 36, 1020, yy + 36], radius=14, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(L), 56, INK)
        if L in done: text(d, (xs[1], yy), vn(f), 56, INK)

def s_do(img, d, t, sc):
    L, vib, f, done = do_state(t)
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    x1, yb = ruler(d, L, vib=vib)
    if vib: text(d, ((EDGE + x1) / 2, yb + 50), vn(L) + " cm", 56, NAVY)
    fbox(d, f)
    graph(d, f, y0=780)
    table(d, 1070, done)

def _kiem_dong_bo():
    """Moi 0,05 s: so f chi hien khi thuoc da dung yen o L moi va dung hang kho ; hang bang chi sau khi da doc."""
    bad = []; t = 0.0; seen = {}
    while t < 11.6:
        L, vib, f, done = do_state(t)
        if vib and abs(L - round(L)) > 1e-9: bad.append((round(t, 2), "rung khi dang doi L"))
        if f is not None and f != fz(int(round(L))): bad.append((round(t, 2), "f lech L"))
        for Lx in done:
            if Lx not in seen: seen[Lx] = t
        if vib: seen.setdefault(("f", int(round(L))), t)
        t += 0.05
    for Lx, _ in ROWS:
        if Lx not in seen: bad.append(("thieu hang", Lx))
        elif seen[Lx] < seen.get(("f", Lx), 99) + 0.5 and Lx != 15: bad.append(("hang som", Lx))
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: âm cao hơn", 320, 1.0, GREEN, 58)
    table(d, 400, {L for L, _ in ROWS}, hl=(15, 10))
    k1 = appear(t, M[1] + 0.1, 0.5)
    card(d, (40, 900, 1040, 1100), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
    text(d, (W / 2, 1000), "Thò ngắn → rung nhanh → âm cao", 56, DGREEN, alpha=k1)

# ---------------- canh 4: Bay ; chua noi duoc ----------------
BAY_ST = 2.2
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    x1, yb = ruler(d, 25, amp=AMP * (1.1 + 0.25 * math.sin(2 * math.pi * t / 1.2)))
    text(d, ((EDGE + x1) / 2, yb + 50), "25 cm", 56, NAVY)
    fbox(d, 9)
    y = 800
    if a1 > 0:
        card(d, (40, y, 1040, y + 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y + 62, a1, DRED)
        for j, q in enumerate(("“Thò dài nên", "to và cao”")):
            yy = y + 170 + j * 80; lw = tw(d, q, F(58))
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            ks = clamp((t - BAY_ST) / 0.4)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y + 320, 1010, y + 580), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y + 400), "✓ 9 Hz: trầm, không cao;", 58, DGREEN, alpha=kk)
        text(d, (W / 2, y + 490), "dưới 20 Hz khó nghe", 58, DGREEN, alpha=kk)
    if k3 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 110), "Chưa nói được:", 60, NAVY, alpha=k3)
        text(d, (W / 2, y + 220), "thước khác?", 58, INK, alpha=k3)
        text(d, (W / 2, y + 320), "(số Hz minh hoạ)", 56, NAVY, alpha=k3)

# ---------------- canh 5: Chot ----------------
END_Q = 0.2
def s_end(img, d, t, sc):
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 465), "Thò ra " + vn(CH_L) + " cm,", 58, INK, alpha=k1)
    text(d, (W / 2, 550), "tần số nằm trong khoảng nào?", 58, INK, alpha=k1)
    if k1 <= 0: return
    global TY
    ty0 = TY; TY = 820
    try:
        x1, yb = ruler(d, CH_L, a=k1)
    finally:
        TY = ty0
    text(d, ((EDGE + x1) / 2 + 60, yb + 50), vn(CH_L) + " cm", 56, NAVY, alpha=k1)
    rr = 60 + 30 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = 820, 1300
    text(d, (560, yc), "f =", 64, NAVY, alpha=k1)
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + t1, "tap") for _, t1, _ in MOVES]
    out += [(da["t0"] + 0.2, "ding"), (da["t0"] + da["M"][1] + 0.1, "tap"), (b["t0"] + BAY_ST, "buzz"),
            (b["t0"] + b["M"][1] + 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(out)

CLIP = dict(id="tn-l9-hsgamthanh-01", header="HSG KHTN 9 · THÍ NGHIỆM", footer="Âm thanh · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thước rung trên mép bàn", draw=s_hook, tail=0.3, caps=[
   ("Gảy đầu thước thò ra.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thò ngắn dần, gảy lại.", 4.0),
   ("Rồi cho thò dài.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Xem hai hàng tô màu.", 3.4),
   ("So hai cột.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("Nhìn số Hz.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
