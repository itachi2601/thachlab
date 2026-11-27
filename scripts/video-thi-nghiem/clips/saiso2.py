# Clip: tn-l10-sai-so-02 - Mot thuoc ke, hai vat do (1/11/2026; 22/11 ΔA = 1 DCNN; dung lai 27/11/2026 theo cong moi
#   viec 4: --do-chu 0 LOI, chu ve >= 56 px, Du doan khong nut A-D (K10), thanh dem lien, cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-sai-so-02.json (_kiem_so() doi chieu):
#   so_lieu_mau: Tam bia 250 mm, Cuc tay 12 mm, ΔA = 1 mm (thuoc vach 1 mm, doc hai dau, moi dau ±0,5 mm).
#   ghi_chu (chi de _kiem_so doi chieu, clip KHONG dung ca nay): cuc tay can δ <= 0,5 % thi ΔA <= 0,06 mm.
# Bai 48: khoi video dung TRUOC hop exp. Cau 6 (ngay sau hop) hoi phep do nao chinh xac hon (0,4 % / 8,3 %)
#   -> clip KHONG tinh δ (de "= ?"), khong hien 0,4 / 8,3. Du doan: ΔA hai phep do so nhau the nao (dap an: bang nhau).
# Chot (THU NGHI, chua chieu): cung thuoc 1 mm, vat dai bao nhieu thi δA = 0,5 %? -> 200 mm (mo_hinh δA = ΔA/d, d trong 5..300).
#   Bai co o 🛠️ 'tay can δ 0,5 % -> ΔA 0,06 mm' nen KHONG hoi chieu do.
# Hinh dung ti le: thuoc tong 3,4 px/mm; khung phong to 56 px/mm cho CA HAI vat.
from engine import *

CARD_C = (237, 214, 170); CARD_D = (150, 110, 60)        # tam bia
ERA_C = (251, 182, 206); ERA_D = (190, 60, 110)          # cuc tay
RULER = (253, 230, 138); RULER_D = (161, 98, 7)
BAND = (234, 88, 12)
DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (91, 33, 182); DORANGE = (176, 64, 8); DBAND = (176, 64, 8)
OBJ = {"bia": ("Tấm bìa", 250.0, CARD_C, CARD_D), "tay": ("Cục tẩy", 12.0, ERA_C, ERA_D)}

# ---------- thuoc tong (dung ti le) ----------
S, X0 = 3.4, 85                      # px/mm, vi tri vach 0
def xo(mm): return X0 + mm * S

def ruler(d, xf, m0, m1, y0, h, lab_every, lab_size, thin, alpha=1.0, unit=False, unit_r=False):
    """Thuoc vang vach 1 mm tu m0 den m1 (mm); xf(mm) -> x. Vach tren mep tren."""
    c = lambda col: A(col, alpha)
    d.rectangle([xf(m0), y0, xf(m1), y0 + h], fill=c(RULER), outline=c(RULER_D), width=3)
    for m in range(math.ceil(m0), math.floor(m1) + 1):
        if m % 10 == 0: L, w = h * 0.52, thin + 2
        elif m % 5 == 0: L, w = h * 0.38, thin + 1
        else: L, w = h * 0.22, thin
        d.line([(xf(m), y0), (xf(m), y0 + L)], fill=c(RULER_D), width=w)
        if m % lab_every == 0: text(d, (xf(m), y0 + h * 0.78), str(m), lab_size, RULER_D, alpha=alpha)
    if unit and unit_r: text(d, (xf(m1) - 12, y0 + h * 0.78), "mm", lab_size, RULER_D, anchor="rm", alpha=alpha)
    elif unit: text(d, (xf(m0) + 12, y0 + h * 0.78), "mm", lab_size, RULER_D, anchor="lm", alpha=alpha)

def overview(d, key, y, alpha=1.0, lens=None, note=False):
    """Mot hang: nhan + vat dat tren thuoc tong 0..260 mm. y = mep tren thuoc. lens=(m0, m1): khung chon."""
    name, L, fc, oc = OBJ[key]; c = lambda col: A(col, alpha)
    text(d, (X0, y - 120), name, 58, INK, anchor="lm", alpha=alpha)
    if note: text(d, (985, y - 100), "đầu trái ở vạch 0", 56, NAVY, anchor="rm", alpha=alpha)
    ruler(d, xo, -8, 266, y, 80, 50, 56, 1, alpha)
    hh = 60 if key == "bia" else 70
    d.rectangle([xo(0), y - hh, xo(L), y], fill=c(fc), outline=c(oc), width=3)
    if lens:
        a, b = lens
        d.rectangle([xo(a), y - hh - 12, xo(b), y + 70], outline=c(BAND), width=5)

# ---------- khung phong to (cung 56 px/mm cho ca hai vat) ----------
Z = 56
ZB = (90, 560, 990, 1010)             # khung phong to
def zoom(d, key, m0, edge_k=0.0, band_k=0.0, alpha=1.0, box=ZB, z=Z, lab=True):
    name, L, fc, oc = OBJ[key]; c = lambda col: A(col, alpha)
    bx0, by0, bx1, by1 = box; m1 = m0 + (bx1 - bx0) / z
    xf = lambda mm: bx0 + (mm - m0) * z
    card(d, box, fill=c(WHITE), outline=c(NAVY), r=20, w=4)
    ry = by1 - 160
    ruler(d, xf, m0 + 0.08, m1 - 0.08, ry, 150, 5, 56, 3, alpha, unit=lab and key == "bia")
    hh = min(150 if key == "bia" else 170, ry - by0 - 20)
    if key == "tay": text(d, (xf(12), ry + 150 * 0.78), "12", 56, RULER_D, alpha=alpha)
    a, b = max(m0 + 0.08, 0.0), min(m1 - 0.08, L)
    d.rectangle([xf(a), ry - hh, xf(b), ry], fill=c(fc), outline=c(oc), width=4)
    if lab: text(d, ((xf(a) + xf(b)) / 2, ry - hh / 2), name, 56, oc, alpha=alpha)
    if edge_k > 0:                                       # mep vat trung vach
        ex = xf(L); yy = ry - hh - 10
        while yy < ry + 80:
            d.line([(ex, yy), (ex, min(yy + 14, ry + 80))], fill=A(NAVY, alpha * edge_k), width=4); yy += 24
    if band_k > 0:                                       # dai ±0,5 mm quanh moi dau vat thay duoc trong khung
        ends = [L] + ([0.0] if m0 < -0.6 else [])
        for e in ends:
            ex = xf(e)
            d.rectangle([ex - 0.5 * z, ry - hh - 14, ex + 0.5 * z, ry + 150 - 2], fill=A(BAND, 0.28 * alpha * band_k),
                        outline=A(BAND, alpha * band_k), width=3)
        if lab:
            for e in ends:
                ex = xf(e)
                text(d, (ex, ry - hh - 44), "±0,5 mm", 56, DBAND, alpha=alpha * band_k)
    return xf

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-sai-so-02.json")))
    h = k["so_lieu_mau"]["hang"]
    assert (h[0][1], h[0][2], h[1][1], h[1][2]) == (250.0, 1.0, 12.0, 1.0)
    assert "0,06 mm" in k["so_lieu_mau"]["ghi_chu"] and abs(0.005 * 12 - 0.06) < 1e-9
_kiem_so()

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    overview(d, "bia", 420, alpha=a)
    overview(d, "tay", 680, alpha=a)
    k = appear(t, M[1] - 0.3, 0.45)
    if k <= 0:
        g = 0.5 + 0.5 * math.sin(t * 4)                                   # khung chon chop: hai vat cung mot thuoc
        d.rectangle([xo(-4), 300, xo(256), 770], outline=A(BAND, g), width=5)
        return
    y0 = 860 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 330), "ΔA của hai phép đo", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 440), "so nhau thế nào?", 62, PURPLE, alpha=k)

# ---------------- canh 2: Doc thuoc ----------------
WIN = {"bia": 241.0, "tay": -1.5}
def phases(sc):
    M = sc["M"]
    return dict(edge1=0.9, band1=M[1] - 0.1, p2=M[2] - 0.2, edge2=M[2] + 0.7, band2=M[2] + 0.7, badge=M[2] + 0.7)

def s_do(img, d, t, sc):
    P = phases(sc); key = "bia" if t < P["p2"] else "tay"
    tl = t if key == "bia" else t - P["p2"]
    m0 = WIN[key]; m1 = m0 + (ZB[2] - ZB[0]) / Z
    overview(d, key, 400, lens=(m0, m1))
    for xa, xb in ((xo(m0), ZB[0] + 20), (xo(m1), ZB[2] - 20)):
        d.line([(xa, 480), (xb, ZB[1])], fill=A(BAND, 0.8), width=3)
    ek = 1.0 if t >= (P["edge1"] if key == "bia" else P["edge2"]) else 0.0
    bk = 1.0 if t >= (P["band1"] if key == "bia" else P["band2"]) else 0.0
    zoom(d, key, m0, edge_k=ek * (0.6 + 0.4 * math.sin(t * 5)), band_k=bk, alpha=1.0)
    if t >= P["band1"]: card(d, (60, 1110, 1020, 1330), fill=WHITE, outline=NAVY, w=4)
    rows = [("Tấm bìa", "(250 ± 1) mm", CARD_D, P["band1"])] + ([("Cục tẩy", "(12 ± 1) mm", ERA_D, P["band2"])] if key == "tay" else [])
    for i, (nm, val, col, at) in enumerate(rows):
        if t < at: continue
        yy = 1170 + i * 100
        text(d, (110, yy), nm, 58, col, anchor="lm")
        text(d, (970, yy), val, 58, INK, anchor="rm")
    if t >= P["badge"]:
        s_ = "ĐÁP ÁN: cùng ΔA = 1 mm"; pw = tw(d, s_, F(58)) + 70
        card(d, (W / 2 - pw / 2, 1390, W / 2 + pw / 2, 1490), fill=(220, 252, 231), outline=GREEN, r=28, w=5)
        text(d, (W / 2, 1440), s_, 58, DGREEN)

# ---------------- canh 3: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 260, 1020, 560), fill=A(WHITE, a), outline=A(GREEN, a), w=5)
    text(d, (W / 2, 350), "δA = ΔA : A · 100 %", 64, DGREEN, alpha=a)
    text(d, (W / 2, 470), "ΔA: sai số · A: độ dài", 56, INK, alpha=a)
    for i, (nm, num, col, L) in enumerate((("Tấm bìa", "1 : 250", CARD_D, 250), ("Cục tẩy", "1 : 12", ERA_D, 12))):
        yy = 680 + i * 360
        text(d, (110, yy), nm, 58, col, anchor="lm", alpha=a)
        g = ease((t - 0.4 - 0.6 * i) / 1.4)                                  # thanh: ΔA (cam) so voi A, cung ti le moi hang
        x0, x1 = 110, 970; wfull = (x1 - x0) * g
        d.rectangle([x0, yy + 60, x0 + wfull, yy + 130], fill=A(CARD_C if i == 0 else ERA_C, a), outline=A(col, a), width=3)
        d.rectangle([x0, yy + 60, x0 + wfull / L, yy + 130], fill=A(BAND, a))
        text(d, (x1 - 90, yy), num + " =", 60, DPURP, anchor="rm", alpha=a)
        text(d, (x1 - 30, yy + 18 * math.sin(t * 3 + i)), "?", 72, DPURP, alpha=a)
        kl = 1.0                                                           # nhan: phan cam = ΔA, ca thanh = A (hien cung luc)
        text(d, (x0, yy + 195), "ΔA = 1 mm", 56, DBAND, anchor="lm", alpha=a * kl)
        text(d, (x1, yy + 195), "A = %d mm" % L, 56, col, anchor="rm", alpha=a * kl)
        if i == 1:                                                         # phan cam (ΔA) chop: nho so voi ca vat
            g2 = 0.5 + 0.5 * math.sin(t * 4)
            d.rectangle([x0, yy + 50, x0 + wfull / L, yy + 140], outline=A(DRED, a * g2), width=6)
            if t > 2.0:                                                    # kinh lup truot doc thanh cuc tay
                mx = 400 + 250 * math.sin((t - 2.0) * 1.5); my = yy + 330
                d.ellipse([mx - 70, my - 70, mx + 70, my + 70], outline=A(NAVY, a), width=10)
                d.line([(mx + 50, my + 50), (mx + 110, my + 110)], fill=A(NAVY, a), width=16)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35)
    card(d, (60, 250, 1020, 760), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 335), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 485), "Thước đặt lệch?", 60, BLUE, alpha=k)
    text(d, (W / 2, 635), "Mắt nhìn xiên?", 60, BLUE, alpha=k)
    ang = 6 * math.sin(t * 2.4)                                             # thuoc lac lu: dat lech
    cx, cy = W / 2, 1150; L = 400; ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [(cx + dx * ca - dy * sa, cy + dx * sa + dy * ca) for dx, dy in ((-L, -50), (L, -50), (L, 50), (-L, 50))]
    d.polygon(pts, fill=A(RULER, k), outline=A(RULER_D, k))
    text(d, (cx, 1360 + 30 * math.sin(t * 3)), "?", 120, NAVY, alpha=k)

# ---------------- canh 5: Bay ----------------
BZ_L = (80, 820, 520, 1140); BZ_R = (560, 820, 1000, 1140)
def s_bay(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 250, 1020, 560), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    text(d, (W / 2, 330), "✗ Vật nhỏ, sai số nhỏ", 60, DRED, alpha=a)
    mx = W / 2 + 260 * math.sin(t * 1.6)                                    # kinh lup di qua lai: nhin ky hai dau
    d.ellipse([mx - 50, 410, mx + 50, 510], outline=A(NAVY, a), width=8)
    d.line([(mx + 36, 496), (mx + 80, 540)], fill=A(NAVY, a), width=12)
    kb = appear(t, M[1] - 0.05, 0.35)
    if kb <= 0: return
    card(d, (60, 600, 1020, 1400), fill=A(WHITE, kb), outline=A(GREEN, kb), w=6)
    text(d, (W / 2, 680), "✓ Dải ±0,5 mm như nhau", 60, DGREEN, alpha=kb)
    text(d, (300, 775), "Tấm bìa", 58, CARD_D, alpha=kb)
    text(d, (780, 775), "Cục tẩy", 58, ERA_D, alpha=kb)
    pulse = 0.55 + 0.45 * math.sin((t - M[1]) * 5)
    zoom(d, "bia", 246.0, band_k=pulse, alpha=kb, box=BZ_L, lab=False)
    zoom(d, "tay", 8.0, band_k=pulse, alpha=kb, box=BZ_R, lab=False)
    for bx in (BZ_L, BZ_R):                                                 # nhan dai cam + don vi thuoc
        text(d, ((bx[0] + bx[2]) / 2, 1200), "±0,5 mm", 56, DBAND, alpha=kb)

# ---------------- canh 6: THU NGHI ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    x0, ry = 100, 720                                                       # thuoc tong 0..260 mm, vat dai chua biet
    ruler(d, lambda mm: x0 + mm * S, -6, (1036 - x0) / S, ry, 90, 10000, 56, 1, k1)   # chay toi mep the, chi so 0: khong loai san dap an
    text(d, (x0 + 40, ry + 70), "mm", 56, RULER_D, anchor="lm", alpha=k1)
    Lx = 120 + 60 * math.sin(t * 1.8)                                       # vat co gian: dai bao nhieu?
    d.rectangle([x0, ry - 110, x0 + Lx * S, ry], fill=A((191, 219, 254), k1), outline=A(BLUE, k1), width=4)
    text(d, (x0 + Lx * S + 50, ry - 55), "?", 72, BLUE, alpha=k1)
    text(d, (W / 2, 960), "Thước vạch 1 mm.", 60, INK, alpha=k1)
    text(d, (W / 2, 1060), "Vật dài bao nhiêu mm", 60, ORANGE, alpha=k1)
    text(d, (W / 2, 1150), "thì δA = 0,5 %?", 60, ORANGE, alpha=k1)
    cbar(d, 1300, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    P = phases(do)
    return [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + P["badge"], "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1] + 0.1, "ding"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-sai-so-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Sai số phép đo · thachlab.id.vn", scenes=[
 dict(key="hook", title="Một thước, hai vật đo", draw=s_hook, tail=0.3, caps=[
   ("Thước vạch 1 mm, đo một lần.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Đọc thước", draw=s_do, tail=0.3, caps=[
   ("Mép bìa trùng vạch 250.", 3.4),
   ("Mỗi đầu lệch tới nửa vạch.", 3.6),
   ("Cục tẩy, cùng độ phóng to.", 4.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Chính xác như nhau chưa?", 3.4),
   ("Em tự tính hai ô.", 3.6)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Còn sai số khác.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Dễ tưởng: vật nhỏ ít sai.", 3.8),
   ("Phóng to hai đầu.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
