# Clip: tn-l10-sai-so-02 - Mot thuoc ke, hai vat do (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-sai-so-02.json:
#   so_lieu_mau: Tam bia d = 250,0 mm, ΔA = 0,5 mm ; Cuc tay d = 12,0 mm, ΔA = 0,5 mm (thuoc vach 1 mm, do 1 lan).
#   mo_hinh: ΔA = DCNN/2 ; δA = ΔA/d·100 % ; gia_thiet: do 1 lan, chi sai so dung cu, dau vat dung vach.
#   tham_so d: 5..300 mm -> cau hoi chot dung quyen vo 5 mm (δ = 10 %, chua tung hien).
# Cau hoi ngay SAU hop trong bai (Cau 6: phep do nao chinh xac hon) -> clip KHONG tinh δ, de "= ?".
# Hinh dung ti le: thuoc tong 3,4 px/mm (bia 850 px, tay 41 px); khung phong to 56 px/mm cho CA HAI vat
#   -> dai ±0,5 mm rong bang nhau o hai lan doc.
# Canh: Du doan (ΔA hai phep do so nhau the nao, K10: chi cau hoi + hinh) -> Doc thuoc (phong to dau bia, dau tay)
#       -> Rut ra (δA = ΔA/A, the so "= ?") -> Chua noi duoc gi -> Bay (vat nho thi it sai so) -> Chot + cau hoi.
from engine import *

CARD_C = (237, 214, 170); CARD_D = (150, 110, 60)        # tam bia
ERA_C = (251, 182, 206); ERA_D = (190, 60, 110)          # cuc tay
RULER = (253, 230, 138); RULER_D = (161, 98, 7)
BAND = (234, 88, 12)
DRED = (185, 28, 28)
OBJ = {"bia": ("Tấm bìa", 250.0, CARD_C, CARD_D), "tay": ("Cục tẩy", 12.0, ERA_C, ERA_D)}

# ---------- thuoc tong (dung ti le) ----------
S, X0 = 3.4, 95                      # px/mm, vi tri vach 0
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
    text(d, (X0, y - 110), name, 40, INK, anchor="lm", alpha=alpha)
    if note: text(d, (985, y - 110), "đầu trái ở vạch 0", 36, MUTED, anchor="rm", alpha=alpha)
    ruler(d, xo, -8, 266, y, 70, 50, 40, 1, alpha)
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
    ruler(d, xf, m0 + 0.08, m1 - 0.08, ry, 150, 5, 40, 3, alpha, unit=lab, unit_r=(key == "tay"))
    hh = min(150 if key == "bia" else 170, ry - by0 - 20)
    if key == "tay": text(d, (xf(12), ry + 150 * 0.78), "12", 40, RULER_D, alpha=alpha)
    a, b = max(m0 + 0.08, 0.0), min(m1 - 0.08, L)
    d.rectangle([xf(a), ry - hh, xf(b), ry], fill=c(fc), outline=c(oc), width=4)
    if lab: text(d, ((xf(a) + xf(b)) / 2, ry - hh / 2), name, 40, oc, alpha=alpha)
    if edge_k > 0:                                       # mep vat trung vach
        ex = xf(L); yy = ry - hh - 10
        while yy < ry + 80:
            d.line([(ex, yy), (ex, min(yy + 14, ry + 80))], fill=A(NAVY, alpha * edge_k), width=4); yy += 24
    if band_k > 0:                                       # dai ±0,5 mm quanh mep
        ex = xf(L)
        d.rectangle([ex - 0.5 * z, ry - hh - 14, ex + 0.5 * z, ry + 150 - 2], fill=A(BAND, 0.28 * alpha * band_k),
                    outline=A(BAND, alpha * band_k), width=3)
        if lab:
            text(d, (ex - 0.5 * z - 6, ry - hh - 40), "−0,5", 40, BAND, anchor="rm", alpha=alpha * band_k)
            text(d, (ex + 0.5 * z + 6, ry - hh - 40), "+0,5", 40, BAND, anchor="lm", alpha=alpha * band_k)
    return xf

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    overview(d, "bia", 420, alpha=a)
    overview(d, "tay", 660, alpha=appear(t, 0.6))
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 850 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 530), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 180, "Thước kẻ vạch 1 mm.", 46, INK, alpha=k)
    ctext(d, y0 + 290, "Sai số dụng cụ ΔA", 48, INK, alpha=k)
    ctext(d, y0 + 360, "của hai phép đo so nhau thế nào?", 48, INK, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 460, 880, y0 + 476], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 460, 200 + 680 * (1 - q), y0 + 476], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: doc thuoc ----------------
WIN = {"bia": 241.0, "tay": -1.5}    # dau trai khung phong to (mm)
def phases(sc):
    M = sc["M"]
    return dict(edge1=M[0] + 1.0, band1=M[1] - 0.1, row1=M[1] + 1.4, p2=M[2] - 0.2,
                edge2=M[2] + 0.9, band2=M[2] + 1.7, row2=M[2] + 2.5, badge=M[2] + 3.5)

def s_do(img, d, t, sc):
    P = phases(sc); key = "bia" if t < P["p2"] else "tay"
    tl = t if key == "bia" else t - P["p2"]
    a = appear(tl, 0.1, 0.4)
    m0 = WIN[key]; m1 = m0 + (ZB[2] - ZB[0]) / Z
    overview(d, key, 400, alpha=a, lens=(m0, m1), note=True)
    kz = appear(tl, 0.5, 0.4)
    if kz > 0:                                           # duong noi khung chon -> khung phong to
        for xa, xb in ((xo(m0), ZB[0] + 20), (xo(m1), ZB[2] - 20)):
            d.line([(xa, 470), (xb, ZB[1])], fill=A(BAND, 0.8 * kz), width=3)
        ek = appear(t, P["edge1"] if key == "bia" else P["edge2"], 0.4)
        bk = appear(t, P["band1"] if key == "bia" else P["band2"], 0.4)
        zoom(d, key, m0, edge_k=ek, band_k=bk, alpha=kz)
        if bk > 0: text(d, (W / 2, 1055), "ΔA = ± nửa vạch = 0,5 mm", 40, BAND, alpha=bk)
    # bang ket qua
    k1 = appear(t, P["row1"], 0.4)
    if k1 > 0:
        card(d, (60, 1110, 1020, 1310), fill=WHITE, outline=NAVY, w=4)
        for i, (nm, val, at) in enumerate((("Tấm bìa", "(250,0 ± 0,5) mm", P["row1"]),
                                           ("Cục tẩy", "(12,0 ± 0,5) mm", P["row2"]))):
            kk = appear(t, at, 0.4)
            if kk <= 0: continue
            yy = 1165 + i * 90
            text(d, (130, yy), nm, 44, OBJ["bia" if i == 0 else "tay"][3], anchor="lm", alpha=kk)
            text(d, (960, yy), val, 46, INK, anchor="rm", alpha=kk)
    kb = appear(t, P["badge"], 0.4)
    if kb > 0:
        s_ = "ĐÁP ÁN · Bằng nhau, cùng 0,5 mm"; pw = tw(d, s_, F(44)) + 70
        card(d, (W / 2 - pw / 2, 1370, W / 2 + pw / 2, 1470), fill=A((220, 252, 231), kb), outline=A(GREEN, kb), r=26, w=4)
        text(d, (W / 2, 1420), s_, 44, GREEN, alpha=kb)

# ---------------- canh 3: rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 290, 1020, 470), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (W / 2, 380), "Cùng ΔA = 0,5 mm", 54, INK, alpha=a)
    k = appear(t, M[0] + 0.6, 0.4)
    if k <= 0: return
    card(d, (60, 520, 1020, 1330), fill=A(WHITE, k), outline=A(GREEN, k), w=5)
    text(d, (W / 2, 640), "δA = (ΔA / A) · 100 %", 60, GREEN, alpha=k)
    k2 = appear(t, M[0] + 1.6, 0.4)
    text(d, (W / 2, 770), "δA: sai số tỉ đối", 42, INK, alpha=k2)
    text(d, (W / 2, 840), "A: giá trị đo", 42, INK, alpha=k2)
    d.line([(120, 920), (960, 920)], fill=A(LIGHT, k2), width=3)
    for i, (nm, num, col) in enumerate((("Tấm bìa", "0,5 / 250,0", CARD_D), ("Cục tẩy", "0,5 / 12,0", ERA_D))):
        kk = appear(t, M[0] + 2.8 + 1.0 * i, 0.4)
        if kk <= 0: continue
        yy = 1030 + i * 160
        text(d, (130, yy), nm, 44, col, anchor="lm", alpha=kk)
        text(d, (590, yy), num + " =", 46, INK, alpha=kk)
        card(d, (850, yy - 42, 950, yy + 42), fill=A((245, 243, 255), kk), outline=A(PURPLE, kk), r=18, w=3)
        text(d, (900, yy), "?", 54, PURPLE, alpha=kk)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 900), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 360), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 265, "Chỉ sai số dụng cụ", 50, BLUE, alpha=k)
    card(d, (110, y1 + 400, 970, y1 + 680), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 495, "Thước lệch, nhìn xiên:", 50, BLUE, alpha=k)
    ctext(d, y1 + 585, "chưa tính", 50, BLUE, alpha=k)
    ctext(d, y1 + 790, "số liệu minh hoạ", 42, MUTED, bold=False, alpha=k)

# ---------------- canh 5: bay ----------------
BZ_L = (80, 760, 520, 1080); BZ_R = (560, 760, 1000, 1080)
def s_bay(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 620), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    q = "Vật nhỏ thì sai số nhỏ"; f = F(54); lw = tw(d, q, f); yy = 490
    text(d, (W / 2, yy), q, 54, DRED, alpha=a)
    ks = clamp((t - 0.9) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=7)
    kb = appear(t, M[1] - 0.05, 0.4)                 # dai ±0,5 + ket luan hien cung luc phu de thu hai
    text(d, (300, 715), "Tấm bìa", 40, CARD_D, alpha=a)
    text(d, (780, 715), "Cục tẩy", 40, ERA_D, alpha=a)
    zoom(d, "bia", 246.0, band_k=kb, alpha=a, box=BZ_L, lab=False)
    zoom(d, "tay", 8.0, band_k=kb, alpha=a, box=BZ_R, lab=False)
    if kb > 0:
        for bx0, L, m0 in ((BZ_L[0], 250.0, 246.0), (BZ_R[0], 12.0, 8.0)):
            ex = bx0 + (L - m0) * Z
            text(d, (ex, 1125), "±0,5 mm", 40, BAND, alpha=kb)
    kc = appear(t, M[1] + 2.0, 0.4)
    if kc > 0:
        ctext(d, 1260, "✓ ΔA do thước, không do vật", 46, GREEN, alpha=kc)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    def body(d, t, k):
        ka = appear(t, sc["M"][0] + 0.4, 0.5)
        ctext(d, 880, "Thước 1 mm đo vở dày 5 mm.\nδA bằng bao nhiêu?", 52, INK, maxw=880, alpha=ka)
        # hinh: quyen vo 5 mm tren thuoc (cung 56 px/mm nhu khung phong to)
        x0, ry = 260, 1330
        ruler(d, lambda mm: x0 + mm * Z, -2.2, 9.5, ry, 130, 5, 40, 3, ka, unit=True)
        d.rectangle([x0, ry - 150, x0 + 5 * Z, ry], fill=A((191, 219, 254), ka), outline=A(BLUE, ka), width=4)
        text(d, (x0 + 2.5 * Z, ry - 75), "vở", 40, BLUE, alpha=ka)
    chot_hoi(d, t, sc, "So δA, không so ΔA", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    P = phases(do)
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + P["badge"], "ding"), (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-sai-so-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Sai số phép đo · thachlab.id.vn", scenes=[
 dict(key="hook", title="Một thước, hai vật đo", draw=s_hook, tail=0.5, caps=[
   ("Đo mỗi vật một lần.", 2.8),
   ("Dừng video, tự đoán.", 5.6)]),
 dict(key="do", title="Đọc thước", draw=s_do, tail=0.3, caps=[
   ("Mép bìa trùng vạch 250.", 3.2),
   ("Mép thật nằm trong dải cam.", 3.4),
   ("Cục tẩy, cùng độ phóng to.", 4.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Chính xác như nhau chưa?", 4.0),
   ("Em tự tính hai ô dấu ?", 4.2)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Còn sai số khác.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Có đúng không?", 2.6),
   ("Hai dải rộng như nhau.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
