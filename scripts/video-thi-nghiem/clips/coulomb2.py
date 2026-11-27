# Clip: tn-l11-coulomb-02 - Can dien tu do luc Coulomb theo khoang cach (ban 3 cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-coulomb-02.json (kho ghi "khong phai so do that" -> nhan "mô phỏng"):
#   so_lieu_mau (r cm, so can g, F.r2 10^-6 N.m2): 2 0,92 3,61 ; 3 0,41 3,62 ; 4 0,23 3,61 ; 5 0,15 3,68 ; 6 0,10 3,53
#   tham_so: r 2-8 cm (cau chot dung r = 8 cm, KHONG hien so can o 8 cm; do thi chi toi r = 7 truc, diem toi r = 6).
#   Tu suy (mo hinh kho F.r2 = 3,6e-6): o r = 8 cm so can = 3,6e-6/(9,8e-3 . 64e-4) = 0,057 g -> can chi 0,06 g = dap so chot.
#   Bay (tu suy): doc so can la luc; o r = 3 cm 0,41 g -> F = 0,41e-3 . 9,8 = 4,0e-3 N (khong dung cap 2 -> 4 cua Du doan).
#   Khong ghi 20 nC: qua cau ve ban kinh 0,68 cm -> chi ve dau (+) tren hai qua.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (tru bi khi B o xa, ha B toi 2 cm, tua nhanh 3..6 cm, diem roi len
#   do thi) -> Ket qua (2 so doc 2 cm / 4 cm, chia 4 tren do thi; Rut ra; cap 3 -> 6 cm cung chia 4) -> Bay (so can = luc?)
#   + Chua noi duoc -> THU NGHI r = 8 cm (khong hop chot chua quy tac; goi y tre "r gấp mấy lần?").
# Hinh vat li: A va B cung dau (+) day nhau -> luc tren A huong xuong (can tang), luc tren B huong len, cung do lon.
# Cong moi 27/11: chu than canh >= 56, moi canh <= 180 tu/phut, khoi chu cach >= 2 s, thanh dem 5 o 70 px.
from engine import *

ROWS = [(2, 0.92, 3.61), (3, 0.41, 3.62), (4, 0.23, 3.61), (5, 0.15, 3.68), (6, 0.10, 3.53)]   # so_lieu_mau
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-coulomb-02.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    assert abs(0.41e-3 * 9.8 - 4.0e-3) < 0.05e-3                         # bay
    assert round(3.6e-6 / (9.8e-3 * 0.08 ** 2), 2) == 0.06                 # dap so chot (khong hien)
    for (r1, m1, _), (r2, m2, _) in ((ROWS[0], ROWS[2]), (ROWS[1], ROWS[4])):
        assert r2 == 2 * r1 and abs(m1 / m2 - 4) < 0.25                     # hai cap r x 2 -> so can chia ~4
_kiem_so()

def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
METAL, METAL_D = (205, 210, 222), (120, 128, 148)
INSUL = (250, 228, 170)                         # tru / thanh cach dien

def pill(d, s, y, a, color=NAVY, size=58, cx=W / 2):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
CX, YA, R, PXCM = 330, 700, 34, 50              # tam qua A; ban kinh qua cau; 50 px / cm khoang cach tam-tam
POLE = 900
FAR = 30                                        # B o rat xa (ngoai khung): so can mo hinh 3,67/30^2 = 0,004 g -> 0,00 g
def yb(r): return YA - r * PXCM                 # tam qua B khi cach A r (cm)

def sphere(d, x, y, alpha=1.0):
    d.ellipse([x - R, y - R, x + R, y + R], fill=A(METAL, alpha), outline=A(METAL_D, alpha), width=3)
    text(d, (x + 1, y + 1), "+", 58, RED, alpha=alpha)

def ruler(d, r, show):
    """Thuoc dung ben trai: 0 ngang tam A, vach moi cm, so 0 2 4 6; con tro xanh ngang tam B khi show."""
    x = 215
    d.rectangle([x - 12, yb(7) - 20, x + 12, YA + 14], fill=(255, 250, 225), outline=NAVY, width=2)
    for c in range(0, 8):
        y = yb(c); d.line([(x + 12, y), (x + (-12 if c % 2 == 0 else 0), y)], fill=NAVY, width=3)
        if c in (0, 2, 4, 6): text(d, (x - 22, y), str(c), 56, NAVY, anchor="rm")
    text(d, (x - 22, yb(7) - 30), "cm", 56, NAVY, anchor="rm")
    for x0 in range(x + 16, CX - R - 6, 14): d.line([(x0, YA), (x0 + 7, YA)], fill=GRAY, width=2)
    if show:
        y = yb(r)
        for x0 in range(x + 16, CX - R - 6, 14): d.line([(x0, y), (x0 + 7, y)], fill=BLUE, width=3)
        d.polygon([(x + 14, y), (x + 34, y - 12), (x + 34, y + 12)], fill=BLUE)
        text(d, (560, y), f"r = {r:g} cm", 58, BLUE, anchor="lm")

def rig(d, r, reading, rlabel=True, force=False, tare=0.0, far=0.0):
    """Gia cao (cot vuot khoi khung) + qua B treo duoi tay doi + qua A tren tru cach dien dat tren can."""
    d.rectangle([POLE - 9, 150, POLE + 9, 1002], fill=(150, 156, 172), outline=NAVY, width=2)
    d.rectangle([POLE - 60, 1002, POLE + 60, 1020], fill=NAVY)
    ruler(d, r, rlabel)
    y = yb(r); yarm = y - R - 110
    if yarm > 150:
        d.rectangle([CX - 8, yarm - 7, POLE, yarm + 7], fill=(150, 156, 172), outline=NAVY, width=2)
        d.rectangle([POLE - 18, yarm - 22, POLE + 18, yarm + 22], fill=(110, 116, 136), outline=NAVY, width=2)
    if y - R + 2 > max(150, yarm + 7):
        d.rectangle([CX - 6, max(150, yarm + 7), CX + 6, y - R + 2], fill=INSUL, outline=(160, 130, 70), width=2)
    sphere(d, CX, y)
    d.rectangle([CX - 8, YA + R - 2, CX + 8, 840], fill=INSUL, outline=(160, 130, 70), width=2)
    sphere(d, CX, YA)
    d.rectangle([180, 840, 480, 856], fill=(200, 205, 215), outline=NAVY, width=3)
    d.rectangle([CX - 10, 856, CX + 10, 876], fill=(120, 125, 140))
    card(d, (110, 876, 550, 1004), fill=(70, 78, 100), r=22)
    card(d, (190, 896, 470, 984), fill=(220, 240, 225), r=12)
    text(d, (CX, 940), reading, 62, (20, 60, 30) if reading != "…" else (110, 130, 115))
    if tare > 0:
        card(d, (600, 870, 840, 950), fill=A(ORANGE, tare), r=30); text(d, (720, 910), "trừ bì", 56, WHITE, alpha=tare)
    if far > 0:
        card(d, (370, 300, 760, 380), fill=A(WHITE, far), outline=A(GRAY, far), r=30, w=3)
        text(d, (565, 340), "B ở rất xa ↑", 56, INK, alpha=far)
    if force:                                   # cap luc day: tren A huong xuong, tren B huong len, cung do dai
        L = 90
        arrow(d, (CX + R + 32, YA), (CX + R + 32, YA + L), ORANGE, w=7, head=22)
        arrow(d, (CX + R + 32, y), (CX + R + 32, y - L), ORANGE, w=7, head=22)
        text(d, (CX + R + 62, YA + L / 2 + 6), "F", 58, ORANGE, anchor="lm")
        text(d, (CX + R + 62, y - L / 2 - 6), "F", 58, ORANGE, anchor="lm")

# ---------------- do thi so can theo r: o duoi (Tien hanh + Ket qua) ----------------
GX0, GX1, GY0, GY1 = 170, 900, 1450, 1150       # r 0-7 cm, so can 0-1,0 g
def gx(r): return GX0 + r / 7 * (GX1 - GX0)
def gy(m): return GY0 - m / 1.0 * (GY0 - GY1)

def graph(d, pts, hl=()):
    """pts: list (i, k_roi) -- diem i dang roi tu tren xuong (k_roi 0..1)."""
    card(d, (40, 1040, 1040, 1585), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 24, GY1 - 50), "số cân (g)", 56, INK, anchor="lm")
    text(d, (1010, GY1 - 50), "mô phỏng", 56, NAVY, anchor="rm")
    for r in (2, 4, 6):
        d.line([(gx(r), GY0), (gx(r), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(r), GY0 + 50), str(r), 56, NAVY)
    text(d, (1030, GY0 + 50), "r (cm)", 56, INK, anchor="rm")
    for m, s in ((0.5, "0,5"), (1.0, "1,0")):
        d.line([(GX0 - 12, gy(m)), (GX0, gy(m))], fill=NAVY, width=3); text(d, (GX0 - 18, gy(m)), s, 56, NAVY, anchor="rm")
    for i, k in pts:
        if k <= 0: continue
        r, m, p = ROWS[i]
        y = lerp(GY1 - 60, gy(m), ease(k))
        dot(d, gx(r), y, 15, A(ORANGE if i in hl else BLUE, min(1, 2 * k)), outline=WHITE)

def pair(d, i, j, col, k):
    """Danh dau cap diem i -> j (r gap doi): duong dong + mui ten xuong + '÷ 4'."""
    (r1, m1, _), (r2, m2, _) = ROWS[i], ROWS[j]
    d.rectangle([gx(r1), gy(m1), gx(r2), GY0], fill=A(col, 0.16 * k))
    for r, m in ((r1, m1), (r2, m2)):
        for y in range(int(gy(m)) + 20, GY0 - 4, 16): d.line([(gx(r), y), (gx(r), y + 8)], fill=A(col, k), width=4)
    for x in range(int(gx(r1)) + 20, int(gx(r2)) - 4, 18): d.line([(x, gy(m1)), (x + 9, gy(m1))], fill=A(col, k), width=4)
    arrow(d, (gx(r2), gy(m1)), (gx(r2), gy(m2) - 20), A(col, k), w=6, head=20)
    text(d, (gx(r2) + 22, (gy(m1) + gy(m2)) / 2), "÷ 4", 60, col, anchor="lm", alpha=k)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 2, "0,92 g", force=t >= 1.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 530), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    for j, s in enumerate(("Nâng B lên r = 4 cm.", "Số cân sẽ thay đổi", "thế nào?")):
        text(d, (W / 2, y0 + 170 + j * 82), s, 62, PURPLE if j else INK, alpha=a)
    seg_bar(d, y0 + 425, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (moi lan doc can mot diem roi len do thi) ----------------
DOWN0, DOWN1 = 1.4, 2.8   # ha B tu rat xa (ngoai khung) xuong r = 2 cm
FF0, FFW = 0.2, 1.0       # tua nhanh: r = 3..6 bat dau tu M[1] + FF0, moi buoc FFW giay (0,4 s nang + doc so)

def s_do(img, d, t, sc):
    M = sc["M"]
    if t < M[1]:
        if t < DOWN0:
            k = 1 - appear(t, 1.1, 0.3)
            rig(d, FAR, "0,00 g", rlabel=False, tare=k, far=k)
        elif t < DOWN1:
            u = t - DOWN0                       # 0,25 s dau: tu 30 cm toi mep khung (10,7 cm), roi ha cham toi 2 cm
            r = lerp(FAR, 10.7, u / 0.25) if u < 0.25 else lerp(10.7, 2, ease((u - 0.25) / (DOWN1 - DOWN0 - 0.25)))
            rig(d, r, "0,00 g" if r >= 10.7 else "…", rlabel=False)
        else:
            rig(d, 2, "0,92 g")
        graph(d, [(0, clamp((t - DOWN1 - 0.4) / 0.5))])
        return
    u = t - M[1] - FF0
    if u < 0:
        rig(d, 2, "0,92 g"); pts = [(0, 1)]
    else:
        j = 1 + max(0, min(3, int(u // FFW))); w = u - (j - 1) * FFW
        r, m, p = ROWS[j]
        if w < 0.4: rig(d, lerp(ROWS[j - 1][0], r, ease(w / 0.4)), "…", rlabel=False)
        else: rig(d, r, vn(m) + " g")
        pts = [(i, 1) for i in range(j)] + [(j, clamp((w - 0.45) / 0.4))]
    if u >= 0:
        card(d, (590, 870, 850, 950), fill=ORANGE, r=30); text(d, (720, 910), "tua nhanh", 56, WHITE)
    graph(d, pts)

# ---------------- canh 3: Ket qua + Rut ra ----------------
def reading_card(d, x0, r, m, k):
    card(d, (x0, 390, x0 + 440, 640), fill=A(WHITE, k), outline=A(NAVY, k), w=4)
    text(d, (x0 + 220, 455), f"r = {r} cm", 58, BLUE, alpha=k)
    text(d, (x0 + 220, 565), vn(m) + " g", 76, INK, alpha=k)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = 1.0
    pill(d, "ĐÁP ÁN: còn một phần tư", 300, ka)
    reading_card(d, 60, 2, 0.92, ka); reading_card(d, 580, 4, 0.23, ka)
    arrow(d, (510, 515), (570, 515), A(ORANGE, ka), w=7, head=20)
    graph(d, [(i, 1) for i in range(5)], hl=(0, 2) if t >= 2.4 else ())
    kp = appear(t, 2.4, 0.45)
    if kp > 0: pair(d, 0, 2, ORANGE, kp)
    k2 = appear(t, M[1] - 0.1, 0.45)              # cap 3 cm -> 6 cm cung chia 4
    if k2 > 0: pair(d, 1, 4, PURPLE, k2)
    kr = appear(t, M[1] + 2.4, 0.45)
    if kr > 0:
        y = 700 + (1 - kr) * 20
        card(d, (60, y, 1020, y + 260), fill=A((255, 247, 237), kr), outline=A(ORANGE, kr), w=5)
        pill(d, "RÚT RA", y + 65, kr, ORANGE)
        text(d, (W / 2, y + 180), "F tỉ lệ nghịch với r²", 64, INK, alpha=kr)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    rig(d, 3, "0,41 g", rlabel=False, force=True)
    if a1 > 0:
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 65, a1, DRED)
        q = "“F = 0,41 N”"
        ks = clamp((t - 1.4) / 0.4); f = F(64); lw = tw(d, q, f); yy = y0 + 180
        text(d, (W / 2, yy), q, 64, mix(DRED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=6)
        ka = a1 * appear(t, 2.3, 0.45)
        if ka > 0:
            text(d, (220, y0 + 330), "0,41 g", 66, INK, alpha=ka)
            arrow(d, (360, y0 + 330), (640, y0 + 330), A(DGREEN, ka), w=7, head=22)
            text(d, (500, y0 + 270), "×10⁻³ ×9,8", 56, DGREEN, alpha=ka)
            text(d, (835, y0 + 330), "4,0·10⁻³ N", 62, DGREEN, alpha=ka)
            text(d, (W / 2, y0 + 450), "✓ đổi kg, nhân g", 58, DGREEN, alpha=ka)
    if k2 > 0:
        y0 = 1040 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y0 + 65, k2, NAVY)
        text(d, (W / 2, y0 + 210), "Hai cầu khác dấu?", 62, INK, alpha=k2)
        kb = k2 * appear(t, M[1] + 2.2, 0.45)
        text(d, (W / 2, y0 + 360), "r rất nhỏ thì sao?", 62, INK, alpha=kb)

# ---------------- canh 5: THU NGHI (cau chot o khung: r = 8 cm -> 0,06 g) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1570), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", 305, k, ORANGE)
    text(d, (W / 2, 470), "Ở r = 2 cm, cân chỉ 0,92 g.", 62, INK, alpha=k)
    text(d, (W / 2, 570), "Nâng B lên r = 8 cm.", 62, INK, alpha=k)
    text(d, (W / 2, 690), "Cân chỉ khoảng bao nhiêu?", 64, DORANGE, alpha=k)
    seg_bar(d, 820, t, 1.0, sc["T"] - 0.2, ORANGE, k)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1000, 970, 1140), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1070), "Gợi ý: r gấp mấy lần?", 60, DORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + DOWN0, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(4)]
    out += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-coulomb-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Lực Coulomb · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cân điện tử đo lực đẩy", draw=s_hook, tail=0.3, caps=[
   ("B đẩy A xuống, số cân tăng.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Trừ bì, rồi hạ B xuống.", 4.6),
   ("Nâng B dần lên, đọc số cân.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("So hai lần đọc cân.", 4.2),
   ("Cặp 3 cm và 6 cm cũng vậy.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 4.2),
   ("Mới đo một cặp cùng dấu.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 7.2)]),
])
