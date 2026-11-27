# Clip: tn-l11-songngangdoc-02 - Song doc tren lo xo slinky: doi nhip day - keo (lo 11, 19/11/2026;
# dung lai 27/11/2026 theo cong moi: chu ve >= 55 px (ra >= 48), moi nhip >= 2,5 s, Du doan khong nut A-D (K10),
# thanh dem day 70 px, Bay hai khung tu giai thich, Gioi han rieng, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-songngangdoc-02.json (_kiem_so() doi chieu mo_hinh lam = v/f):
#   v = 7,0 m/s ; so_lieu_mau (f Hz, lam m): 2 -> 3,5 ; 3,5 -> 2,0 ; 5 -> 1,4 (hang 1 Hz -> 7,0 m de danh cho cau chot,
#   KHONG hien tren man). Lo xo keo dai 4 m. Bien do a = 10 cm (tham_so max) de vung nen nhin ro; chieu cham 4 lan.
# Bai l11-song-ngang-song-doc (lesson 28): hop exp o muc II.2. Tranh trung: Bay 2 (vung nen tren do thi u - x: clip KHONG ve
#   do thi), Thu suc (nen - dan 0,2 m -> 850 Hz: clip KHONG hien khoang nen - dan), bai mau 680/425 Hz, thu thach 1000 Hz,
#   Bay 1 (phao doi bao xa sau 10 s: clip khong hoi so), quiz mo bai (phao), cau loa / chuong / A^2.
# Du doan (K10): day - keo nhanh hon, 2 Hz len 5 Hz: hai vung nen lien nhau se ra sao? Dap an: gan nhau hon (3,5 -> 1,4 m).
# Bay = hien_tuong_hay_sai[1] "vong danh dau bi day dan toi dau kia": khung tren (de tuong) vong mau troi dan sang phai ;
#   khung duoi (that) vong mau tien - lui +-10 cm quanh vach cu.
# Gioi han: moi doi f, chua doi bien do day.
# THU NGHI (= cau_chot khung web): lo xo du dai, day - keo 1 Hz: nen - nen cach bao xa? Buoc suy luan chua chieu:
#   f.lam khong doi (2 Hz -> 3,5 m) nen 1 Hz -> 7,0 m. Dap so 7,0 KHONG hien tren man.
# Mo hinh u(x, t) = a.cos(2.pi.f.(t - x/v)); vung nen o u = 0 va du/dx < 0 <=> pha 2.pi.f(t - x/v) = 3.pi/2 (mod 2.pi).
from engine import *

V, LX, AM, SLOW = 7.0, 4.0, 0.10, 4.0                 # m/s, m, m, chieu cham 4 lan
ROWS = [(2.0, 3.5), (3.5, 2.0), (5.0, 1.4)]          # (f Hz, nen - nen m)
X0P = [0.25, 0.5, 0.3]                                # vi tri vung nen dau tien luc dung hinh (m)
DRED, DGREEN, DPURPLE, DORANGE = (185, 28, 28), (21, 110, 55), (91, 33, 182), (176, 64, 8)

def vn(x):
    s = f"{x:g}" if abs(x - round(x)) < 1e-9 else f"{x:.1f}"
    return s.replace(".", ",")
def vn1(x): return f"{x:.1f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-songngangdoc-02.json")))
    hang = k["so_lieu_mau"]["hang"]; tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["v"]["gia_tri"] == V and tp["a"]["max"] * 0.01 == AM
    for f, lam in ROWS + [(1.0, 7.0)]:
        assert any(r[0] == f and r[1] == lam for r in hang), (f, lam)
        assert abs(V / f - lam) < 0.01
    g = k["so_lieu_mau"]["ghi_chu"]
    assert "chậm 4 lần" in g and "10 cm" in g
    assert any("phản xạ" in s for s in k["mo_hinh"]["gia_thiet"])
    for f, lam in ROWS: assert AM * 2 * math.pi / lam < 1    # vong khong cham nhau
_kiem_so()

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 56
    card(d, (cx - pw / 2, cy - size * 0.82, cx + pw / 2, cy + size * 0.82), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem day 70 px, rut tu phai sang trai theo 10 nac (moi nac la mot thay doi hinh ro)."""
    p = clamp((t - t0) / (t1 - t0)); q = math.floor(p * 10 + 1e-9) / 10
    d.rounded_rectangle([140, y, 940, y + 70], radius=35, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 70], radius=35, fill=A(col, a))

# ---------------- lo xo ----------------
X0, X1 = 140, 940                                    # 0 m -> 4 m
S = (X1 - X0) / LX
NR = 73                                              # so vong (cach nhau 5,6 cm)
MARK = 36                                            # vong dan bang mau (x = 2,0 m)
def u(x, tp, f, ka=1.0): return ka * AM * math.cos(2 * math.pi * f * (tp - x / V))
def comps(tp, f):
    """Vi tri cac vung nen trong [0, LX] luc tp."""
    lam = V / f; x = V * (tp - 0.75 / f); x -= math.floor(x / lam) * lam
    out = []
    while x <= LX + 1e-9: out.append(x); x += lam
    return out

def t_freeze(i):
    f = ROWS[i][0]; return X0P[i] / V + 0.75 / f

def _kiem_nen():
    """Vung nen tinh theo pha phai trung cho cac vong sit nhat (kiem tren chinh luoi vong dang ve)."""
    for i, (f, lam) in enumerate(ROWS):
        tp = t_freeze(i); cs = comps(tp, f)
        assert abs(cs[0] - X0P[i]) < 1e-6 and abs(cs[1] - cs[0] - lam) < 1e-6
        xs = [j * LX / (NR - 1) + u(j * LX / (NR - 1), tp, f) for j in range(NR)]
        gaps = [(xs[j + 1] - xs[j], (xs[j + 1] + xs[j]) / 2) for j in range(NR - 1)]
        for c in cs:
            near = [g for g in gaps if abs(g[1] - c) < lam / 2]
            gmin = min(near)[1]
            assert abs(gmin - c) < 0.09, (f, c, gmin)          # cho sit nhat cach vung nen tinh < 1 khoang vong
        assert min(g[0] for g in gaps) > 0                      # vong khong de len nhau

def spring(d, yc, tp, f, ka=1.0, mark=True, h=70, mark_dx=0.0, a=1.0):
    xs = [j * LX / (NR - 1) for j in range(NR)]
    d.line([(X0 - 40, yc + h + 22), (X1 + 40, yc + h + 22)], fill=A(LIGHT, a), width=6)          # san
    if ka > 0.05:                                                          # dai mo o vung nen
        bw = min(0.35, V / f / 5) * S / 2
        for c in comps(tp, f):
            pc = X0 + c * S
            d.rectangle([max(X0 - 10, pc - bw), yc - h - 10, min(X1 + 10, pc + bw), yc + h + 10],
                        fill=A((255, 214, 186), 0.85 * ka * a))
    for j, x in enumerate(xs):
        px = X0 + (x + u(x, tp, f, ka)) * S
        if j == MARK and mark: continue
        d.ellipse([px - 6, yc - h, px + 6, yc + h], outline=A((40, 58, 110), a), width=4)
    if mark:
        x = xs[MARK]; px = X0 + (x + u(x, tp, f, ka) + mark_dx) * S
        d.ellipse([px - 9, yc - h - 4, px + 9, yc + h + 4], outline=A(ORANGE, a), width=9)
    pl = X0 + u(0, tp, f, ka) * S; pr = X0 + (LX + u(LX, tp, f, ka)) * S             # hai tay
    for x0 in (pl - 70, pr + 10):
        d.rounded_rectangle([x0, yc - 30, x0 + 60, yc + 30], radius=22, fill=A((240, 196, 160), a),
                            outline=A((170, 110, 80), a), width=4)

def ruler(d, y):
    d.line([(X0, y), (X1, y)], fill=NAVY, width=3)
    for k in range(9):
        x = X0 + k * 0.5 * S; L = 20 if k % 2 == 0 else 10
        d.line([(x, y), (x, y + L)], fill=NAVY, width=3)
        if k % 2 == 0: text(d, (x, y + 52), str(k // 2), 56, INK)
    text(d, (X1 + 62, y + 52), "m", 56, INK)

YC = 450
def stage(d, slow=True):
    card(d, (40, 215, 1040, 880), fill=WHITE, outline=LIGHT, w=3)
    ruler(d, 660)
    if slow: text(d, (W / 2, 825), "quay chậm 4 lần", 56, INK)

def fpill(d, f, y=950, a=1.0):
    pill(d, W / 2, y, vn(f) + " Hz", 60, WHITE, RED, a)

# ---------------- canh 1: Du doan (K10: chi cau hoi, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    stage(d); spring(d, YC, t / SLOW, 2.0, ka=appear(t, 0.2, 0.8)); fpill(d, 2.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 610), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 75, "DỰ ĐOÁN", 58, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 205), "Nhịp đẩy – kéo lên 5 Hz:", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 300), "hai vùng nén liền nhau", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 395), "ra sao?", 64, DPURPLE, alpha=a)
    cbar(d, y0 + 490, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
RUN, STEP = 2.5, 3.6                                  # giay chay truoc khi dung hinh ; giay moi nhip
def starts(): return [i * STEP for i in range(3)]
def do_state(t):
    """-> (i, tp vat li, ka, dung hinh?, so hang da ghi)."""
    st = starts()
    i = max(j for j, s in enumerate(st) if t >= s)
    tf = st[i] + RUN; fz = t >= tf
    tp = t_freeze(i) - (0 if fz else (tf - t) / SLOW)
    ka = 1.0 if i == 0 else ease((t - st[i]) / 0.6)
    rows = i + (1 if fz else 0)
    return i, tp, ka, fz, rows

def bracket(d, xa, xb, y, lab, a=1.0):
    pa, pb = X0 + xa * S, X0 + xb * S
    d.line([(pa, y), (pb, y)], fill=A(ORANGE, a), width=6)
    for p in (pa, pb): d.line([(p, y - 18), (p, y + 18)], fill=A(ORANGE, a), width=6)
    pw = tw(d, lab, F(58)) + 40
    card(d, ((pa + pb) / 2 - pw / 2, y - 90, (pa + pb) / 2 + pw / 2, y - 26), fill=A(WHITE, a), r=18)
    text(d, ((pa + pb) / 2, y - 58), lab, 58, DORANGE, alpha=a)

def ntable(d, y, n, hl=-1):
    card(d, (120, y, 960, y + 100 + 3 * 82), fill=WHITE, outline=NAVY, w=4)
    text(d, (330, y + 52), "f (Hz)", 56, INK); text(d, (720, y + 52), "Nén – nén (m)", 56, INK)
    d.line([(150, y + 98), (930, y + 98)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 142 + i * 82; f, lam = ROWS[i]
        if i == hl: d.rounded_rectangle([140, yy - 36, 940, yy + 36], radius=16, fill=(255, 237, 213))
        text(d, (330, yy), vn(f), 58, INK); text(d, (720, yy), vn1(lam), 58, BLUE)

def s_do(img, d, t, sc):
    i, tp, ka, fz, rows = do_state(t)
    stage(d)
    f = ROWS[i][0]
    spring(d, YC, tp, f, ka=ka)
    fpill(d, f)
    if fz:
        cs = comps(tp, f)
        for c in cs: text(d, (X0 + c * S, YC + 135), "nén", 56, DORANGE)
        bracket(d, cs[0], cs[1], 320, vn1(ROWS[i][1]) + " m")
    ntable(d, 1030, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: hang ghi dung luc dung hinh ; khoang do khop hang bang ; du 3 hang cuoi canh."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, tp, ka, fz, rows = do_state(t)
        if rows > i + 1: bad.append((round(t, 2), "hang som"))
        if rows == i + 1 and not fz: bad.append((round(t, 2), "hang truoc khi do"))
        if fz:
            cs = comps(tp, ROWS[i][0])
            if abs(cs[1] - cs[0] - ROWS[i][1]) > 0.01: bad.append((round(t, 2), "khoang do lech bang"))
            if ka < 0.999: bad.append((round(t, 2), "dung hinh khi bien do chua du"))
        t += 0.05
    if do_state(sc["T"] - 0.05)[4] != 3: bad.append("chua du 3 hang cuoi canh")
    if sc["T"] < starts()[2] + RUN + 1.2: bad.append("hang cuoi hien qua ngan")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 215, 1020, 420), fill=WHITE, outline=NAVY, r=26, w=5)
    pill(d, W / 2, 272, "ĐÁP ÁN", 56, WHITE, NAVY)
    text(d, (W / 2, 368), "Gần nhau hơn", 64, NAVY)
    ntable(d, 450, 3)
    y = 450 + 142
    arrow(d, (175, y), (175, y + 164), ORANGE, w=6, head=18)
    arrow(d, (905, y), (905, y + 164), ORANGE, w=6, head=18)
    kr = appear(t, 2.6, 0.45)
    if kr > 0:
        card(d, (60, 830, 1020, 1060), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=26, w=5)
        text(d, (W / 2, 900), "Nhịp gấp 2,5 lần,", 60, DGREEN, alpha=kr)
        text(d, (W / 2, 990), "nén – nén ngắn 2,5 lần", 60, DGREEN, alpha=kr)
    # lo xo 5 Hz chay suot canh: vung nen sit (hinh khong dung yen)
    card(d, (40, 1100, 1040, 1440), fill=WHITE, outline=LIGHT, w=3)
    spring(d, 1250, t / SLOW, 5.0, h=62)

# ---------------- canh 4: Bay - "vong danh dau troi toi dau kia" ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    tp = t / SLOW
    # khung tren: de tuong - vong mau troi dan sang phai
    card(d, (40, 215, 1040, 700), fill=(254, 242, 242), outline=DRED, w=6)
    text(d, (75, 280), "✗ Dễ tưởng: trôi theo sóng", 58, DRED, anchor="lm")
    drift = 1.6 * clamp((t - 0.4) / 2.8)
    spring(d, 480, tp, 2.0, h=62, mark_dx=drift)
    # khung duoi: that - tien lui quanh vach cu
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        card(d, (40, 740, 1040, 1250), fill=A(WHITE, k2), outline=A(BLUE, k2), w=6)
        text(d, (75, 805), "Thật: quanh vạch cũ", 58, BLUE, anchor="lm", alpha=k2)
        yc = 1030
        xm = X0 + 2.0 * S
        for yy in range(yc - 95, yc + 90, 24): d.line([(xm, yy), (xm, yy + 12)], fill=A(GRAY, k2), width=4)
        spring(d, yc, tp, 2.0, h=62, a=k2)
        lo, hi = X0 + (2.0 - AM) * S, X0 + (2.0 + AM) * S
        d.line([(lo, 1170), (hi, 1170)], fill=A(ORANGE, k2), width=5)
        for p in (lo, hi): d.line([(p, 1156), (p, 1184)], fill=A(ORANGE, k2), width=5)
        text(d, (hi + 30, 1170), "±10 cm", 56, DORANGE, anchor="lm", alpha=k2)
    kc = appear(t, M[2] - 0.1, 0.45)
    if kc > 0:
        card(d, (60, 1290, 1020, 1420), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=26, w=5)
        text(d, (W / 2, 1355), "✓ Sóng đi, vòng ở lại", 60, DGREEN, alpha=kc)

# ---------------- canh 5: Gioi han ----------------
def s_gioi(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Đẩy mạnh hơn thì sao?", 62, INK)
    card(d, (40, 600, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    spring(d, 760, t / SLOW, 2.0, h=62)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1300), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 290, "THỬ NGHĨ", 58, WHITE, ORANGE, k1)
    text(d, (W / 2, 480), "Lò xo đủ dài, 1 Hz:", 66, INK, alpha=k1)
    text(d, (W / 2, 600), "hai vùng nén liền nhau", 66, INK, alpha=k1)
    text(d, (W / 2, 720), "cách bao xa?", 66, DORANGE, alpha=k1)
    cbar(d, 1100, t, 1.2, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + s + RUN, "tap") for s in starts()]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.4, "buzz"), (b["t0"] + b["M"][2], "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-songngangdoc-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Sóng dọc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lò xo slinky trên sàn", draw=s_hook, tail=0.3, caps=[
   ("Đẩy – kéo đầu lò xo, dọc trục.", 3.8),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Tăng dần nhịp, đo hai vùng nén.", 5.4),
   ("Mỗi nhịp, ghi một hàng.", 5.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Nhịp tăng, vùng nén sít lại.", 6.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Vòng màu trôi theo sóng?", 3.2),
   ("Nhìn vạch cũ của nó.", 3.2),
   ("Chỉ dao động tại chỗ.", 3.0)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Mới đổi nhịp.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Đẩy càng nhanh, nén càng sít.", 6.4)]),
])

_kiem_nen()
_b = _kiem_dong_bo(); assert not _b, _b
