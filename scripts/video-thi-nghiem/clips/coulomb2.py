# Clip: tn-l11-coulomb-02 - Can dien tu do luc Coulomb theo khoang cach (30/10/2026, ban 2 sau cong B)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-coulomb-02.json (kho ghi "khong phai so do that" -> nhan "số liệu mô phỏng"):
#   so_lieu_mau (r cm, so can g, F.r2 10^-6 N.m2): 2 0,92 3,61 ; 3 0,41 3,62 ; 4 0,23 3,61 ; 5 0,15 3,68 ; 6 0,10 3,53
#   tham_so: r 2-8 cm (cau hoi chot dung r = 8 cm, chua tung hien tren man) ; can doc 0,01 g ; g = 9,8 m/s2.
#   Mo hinh: o r = 8 cm so can = 3,6e-6/(9,8e-3 . 64e-4) = 0,057 g -> khoang 0,06 g. Bay: 0,92e-3 . 9,8 = 9,0e-3 N.
#   Khong ghi 20 nC tren the: qua cau ve ban kinh 0,68 cm, 20 nC cho E be mat ~3,9e6 V/m (cỡ nguong danh thung) ->
#   chi ghi "cùng dấu (+)"; khe hai mat cau o r = 2 cm la 0,64 cm.
# Khac dientruong11: khong co bang o canh Tien hanh; truc chinh la DO THI so can theo r (o duoi, co dinh suot clip),
#   moi lan doc can la mot diem roi xuong do thi; thuoc do r dung canh qua cau (ben trai), B treo tu gia cao.
# Canh: Du doan (K10) -> Tien hanh (tru bi khi B o xa ngoai khung, ha B toi 2 cm, tua nhanh 3..6 cm, diem roi len do thi)
#       -> Dap an (bang F.r2 + "F = so can x g", do thi chia 4 khi r x 2) -> Bay (doc so can la luc) roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (r = 8 cm).
# Hinh vat li: A va B cung dau (+) day nhau -> luc tren A huong xuong (can tang), luc tren B huong len, cung do lon.
from engine import *

ROWS = [(2, 0.92, 3.61), (3, 0.41, 3.62), (4, 0.23, 3.61), (5, 0.15, 3.68), (6, 0.10, 3.53)]   # so_lieu_mau
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DRED = (185, 28, 28)
PINK = (254, 226, 226)                          # nen hang "lech nhieu" (khac cam cua cap chia 4)
METAL, METAL_D = (205, 210, 222), (120, 128, 148)
INSUL = (250, 228, 170)                         # tru / thanh cach dien

# ---------------- dung cu (khung nguon 1080x1920) ----------------
CX, YA, R, PXCM = 330, 700, 34, 50              # tam qua A; ban kinh qua cau; 50 px / cm khoang cach tam-tam
POLE = 620
FAR = 30                                        # B o rat xa (ngoai khung): so can mo hinh 3,67/30^2 = 0,004 g -> 0,00 g
def yb(r): return YA - r * PXCM                 # tam qua B khi cach A r (cm)

def sphere(d, x, y, alpha=1.0):
    d.ellipse([x - R, y - R, x + R, y + R], fill=A(METAL, alpha), outline=A(METAL_D, alpha), width=3)
    d.ellipse([x - R * 0.55, y - R * 0.6, x - R * 0.05, y - R * 0.15], fill=A(WHITE, 0.7 * alpha))
    text(d, (x + 2, y + 2), "+", 44, RED, alpha=alpha)

def ruler(d, r, show):
    """Thuoc dung ben trai: 0 ngang tam A, vach moi cm, so 2 4 6; con tro xanh ngang tam B khi show."""
    x = 205
    d.rectangle([x - 12, yb(7) - 20, x + 12, YA + 14], fill=(255, 250, 225), outline=NAVY, width=2)
    for c in range(0, 8):
        y = yb(c); d.line([(x + 12, y), (x + (-12 if c % 2 == 0 else 0), y)], fill=NAVY, width=3)
        if c in (0, 2, 4, 6): text(d, (x - 24, y), str(c), 38, MUTED, bold=False, anchor="rm")
    text(d, (x - 24, yb(7) - 4), "cm", 36, MUTED, bold=False, anchor="rm")
    for x0 in range(x + 16, CX - R - 6, 14): d.line([(x0, YA), (x0 + 7, YA)], fill=GRAY, width=2)
    if show:
        y = yb(r)
        for x0 in range(x + 16, CX - R - 6, 14): d.line([(x0, y), (x0 + 7, y)], fill=BLUE, width=3)
        d.polygon([(x + 14, y), (x + 34, y - 12), (x + 34, y + 12)], fill=BLUE)
        text(d, (CX + R + 76, y), f"r = {r:g} cm", 40, BLUE, anchor="lm")

def rig(d, r, reading, rlabel=True, force=False, tare=0.0, far=0.0):
    """Gia cao (cot vuot khoi khung) + qua B treo duoi tay doi + qua A tren tru cach dien dat tren can."""
    d.rectangle([POLE - 9, 150, POLE + 9, 1002], fill=(150, 156, 172), outline=NAVY, width=2)
    d.rectangle([POLE - 60, 1002, POLE + 60, 1020], fill=NAVY)
    ruler(d, r, rlabel)
    y = yb(r); yarm = y - R - 110
    if yarm > 150:
        d.rectangle([CX - 8, yarm - 7, POLE, yarm + 7], fill=(150, 156, 172), outline=NAVY, width=2)
        d.rectangle([POLE - 18, yarm - 22, POLE + 18, yarm + 22], fill=(110, 116, 136), outline=NAVY, width=2)
        dot(d, POLE + 32, yarm, 14, (90, 96, 116), outline=NAVY)
    if y - R + 2 > max(150, yarm + 7):
        d.rectangle([CX - 6, max(150, yarm + 7), CX + 6, y - R + 2], fill=INSUL, outline=(160, 130, 70), width=2)
    sphere(d, CX, y)
    d.rectangle([CX - 8, YA + R - 2, CX + 8, 840], fill=INSUL, outline=(160, 130, 70), width=2)
    sphere(d, CX, YA)
    d.rectangle([180, 840, 480, 856], fill=(200, 205, 215), outline=NAVY, width=3)
    d.rectangle([CX - 10, 856, CX + 10, 876], fill=(120, 125, 140))
    card(d, (110, 876, 550, 1004), fill=(70, 78, 100), r=22)
    card(d, (190, 896, 470, 984), fill=(220, 240, 225), r=12)
    text(d, (CX, 940), reading, 52, (20, 60, 30) if reading != "…" else (110, 130, 115))
    if tare > 0:
        card(d, (110, 784, 290, 832), fill=A(ORANGE, tare), r=24); text(d, (200, 808), "trừ bì", 36, WHITE, alpha=tare)
    if far > 0:
        card(d, (240, 300, 560, 360), fill=A(WHITE, far), outline=A(GRAY, far), r=28, w=3)
        text(d, (400, 330), "B ở rất xa ↑", 38, INK, alpha=far)
    if force:                                   # cap luc day: tren A huong xuong, tren B huong len, cung do dai
        L = 90
        arrow(d, (CX + R + 32, YA), (CX + R + 32, YA + L), ORANGE, w=6, head=20)
        arrow(d, (CX + R + 32, y), (CX + R + 32, y - L), ORANGE, w=6, head=20)
        text(d, (CX + R + 58, YA + L / 2 + 6), "F", 40, ORANGE, anchor="lm")
        text(d, (CX + R + 58, y - L / 2 - 6), "F", 40, ORANGE, anchor="lm")

def info(d, alpha=1.0):
    card(d, (680, 300, 1040, 500), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), r=22, w=3)
    text(d, (860, 345), "A, B cùng dấu (+)", 38, INK, alpha=alpha)
    text(d, (860, 400), "cân đọc 0,01 g", 38, MUTED, bold=False, alpha=alpha)
    text(d, (860, 455), "số liệu mô phỏng", 36, MUTED, bold=False, alpha=alpha)

# ---------------- do thi so can theo r: co dinh o duoi (Tien hanh + Ket qua) ----------------
GX0, GX1, GY0, GY1 = 170, 960, 1460, 1130       # r 0-7 cm, so can 0-1,0 g
def gx(r): return GX0 + r / 7 * (GX1 - GX0)
def gy(m): return GY0 - m / 1.0 * (GY0 - GY1)

def graph(d, pts, hl=(), sim=False):
    """pts: list (i, k_roi) -- diem i dang roi tu tren xuong (k_roi 0..1)."""
    card(d, (40, 1040, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 50), "số cân (g)", 38, INK, anchor="lm")
    if sim: text(d, (1010, GY1 - 50), "số liệu mô phỏng", 36, MUTED, bold=False, anchor="rm")
    for r in (2, 4, 6):
        d.line([(gx(r), GY0), (gx(r), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(r), GY0 + 40), str(r), 38, MUTED, bold=False)
    text(d, (GX1 + 34, GY0 + 40), "r (cm)", 38, INK, anchor="rm")
    for m, s in ((0.5, "0,5"), (1.0, "1,0")):
        d.line([(GX0 - 12, gy(m)), (GX0, gy(m))], fill=NAVY, width=3); text(d, (GX0 - 20, gy(m)), s, 38, MUTED, bold=False, anchor="rm")
    for i, k in pts:
        if k <= 0: continue
        r, m, p = ROWS[i]
        y = lerp(GY1 - 60, gy(m), ease(k))
        dot(d, gx(r), y, 13, A(ORANGE if i in hl else BLUE, min(1, 2 * k)), outline=WHITE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut lua chon) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 2, "0,92 g", force=t >= 1.0); info(d, appear(t, 0.5, 0.4))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 250, "Nâng B lên r = 4 cm.\nSố cân sẽ thay đổi\nthế nào?", 48, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 482], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 482], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (khong bang: moi lan doc can mot diem roi len do thi) ----------------
DOWN0, DOWN1 = 1.6, 3.4   # ha B tu rat xa (ngoai khung) xuong r = 2 cm
FF0, FFW = 0.2, 1.0       # tua nhanh: r = 3..6 bat dau tu M[1] + FF0, moi buoc FFW giay (0,4 s nang + doc so)

def s_do(img, d, t, sc):
    M = sc["M"]; info(d)
    if t < M[1]:
        if t < DOWN0:
            tare = appear(t, 0.4, 0.3) * (1 - appear(t, 1.4, 0.3))
            rig(d, FAR, "0,00 g", rlabel=False, tare=tare, far=1 - appear(t, 1.4, 0.3))
        elif t < DOWN1:
            u = t - DOWN0                       # 0,25 s dau: tu 30 cm toi mep khung (10,7 cm; can chua kip nhay), roi ha cham toi 2 cm
            r = lerp(FAR, 10.7, u / 0.25) if u < 0.25 else lerp(10.7, 2, ease((u - 0.25) / (DOWN1 - DOWN0 - 0.25)))
            rig(d, r, "0,00 g" if r >= 10.7 else "…", rlabel=False)
        else:
            rig(d, 2, "0,92 g", force=t >= DOWN1 + 0.3)
        graph(d, [(0, clamp((t - DOWN1 - 0.4) / 0.5))])
        return
    u = t - M[1] - FF0
    if u < 0:
        rig(d, 2, "0,92 g")
        pts = [(0, 1)]
    else:
        j = 1 + max(0, min(3, int(u // FFW))); w = u - (j - 1) * FFW
        r, m, p = ROWS[j]
        if w < 0.4: rig(d, lerp(ROWS[j - 1][0], r, ease(w / 0.4)), "…", rlabel=False)
        else: rig(d, r, vn(m) + " g")
        pts = [(i, 1) for i in range(j)] + [(j, clamp((w - 0.45) / 0.4))]
    card(d, (720, 520, 960, 580), fill=ORANGE, r=30); text(d, (840, 550), "tua nhanh", 38, WHITE)
    graph(d, pts)

# ---------------- canh 3: Dap an + rut ra ----------------
TX = (210, 520, 840)
def table(d, y, fr, hl=(), ka=1.0):
    card(d, (40, y, 1040, y + 480), fill=WHITE, outline=NAVY, w=4)
    for x, c in zip(TX, ("r (cm)", "Số cân (g)", "F·r²")): text(d, (x, y + 44), c, 40, INK)
    text(d, (TX[2], y + 86), "(10⁻⁶ N·m²)", 36, MUTED, bold=False)
    d.line([(70, y + 112), (1010, y + 112)], fill=LIGHT, width=4)
    for i in range(5):
        yy = y + 150 + i * 70; r, m, p = ROWS[i]
        if i in hl: d.rounded_rectangle([60, yy - 32, 1020, yy + 32], radius=16, fill=A(PINK, ka))
        text(d, (TX[0], yy), str(r), 44, INK); text(d, (TX[1], yy), vn(m), 44, INK)
        if i < fr: text(d, (TX[2], yy), vn(p), 44, BLUE)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · còn một phần tư"
    pw = tw(d, lab, F(38)) + 52
    card(d, (W - 60 - pw, 236, W - 60, 296), fill=A(NAVY, ka), r=30)
    text(d, (W - 60 - pw / 2, 266), lab, 38, WHITE, alpha=ka)
    hl = (3, 4) if t >= M[1] - 0.1 else ()
    table(d, 316, fr=sum(t >= 0.05 + 0.08 * i for i in range(5)), hl=hl, ka=appear(t, M[1] - 0.1, 0.3))
    text(d, (W / 2, 836), "F = số cân (kg) × g; r đổi ra m", 42, INK, alpha=appear(t, 0.3, 0.4))
    kn = appear(t, M[1] + 0.4, 0.4)
    if kn > 0:
        card(d, (40, 890, 1040, 990), fill=A(PINK, kn), outline=A(RED, kn), r=20, w=3)
        text(d, (W / 2, 940), "Làm tròn 0,01 g gây sai lệch lớn", 40, DRED, alpha=kn)
    graph(d, [(i, 1) for i in range(5)], hl=(0, 2), sim=True)
    kd = appear(t, 0.9, 0.5)                    # r gap doi (2 -> 4) thi so can chia 4 (0,92 -> 0,23)
    if kd > 0:
        for r, m in ((2, 0.92), (4, 0.23)):
            for y in range(int(gy(m)) + 18, GY0 - 4, 16): d.line([(gx(r), y), (gx(r), y + 8)], fill=A(ORANGE, kd), width=3)
        for x in range(int(gx(2)) + 18, int(gx(4)) - 4, 18): d.line([(x, gy(0.92)), (x + 9, gy(0.92))], fill=A(ORANGE, kd), width=3)
        arrow(d, (gx(4), gy(0.92)), (gx(4), gy(0.23) - 18), A(ORANGE, kd), w=5, head=18)
        text(d, (gx(4) + 24, (gy(0.92) + gy(0.23)) / 2), "÷ 4", 46, ORANGE, anchor="lm", alpha=kd)
        text(d, ((gx(2) + gx(4)) / 2, GY0 + 40), "r × 2", 38, ORANGE, alpha=kd)

# ---------------- canh 4: Bay roi Chua noi duoc (khong hien cung luc) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    rig(d, 2, "0,92 g", force=True)
    if a1 > 0:
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Lực F = 0,92 N”"
        ks = clamp((t - 1.2) / 0.4); f = F(48); lw = tw(d, q, f); yy = y0 + 185
        text(d, (W / 2, yy), q, 48, DRED, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=4)
        ka = a1 * appear(t, 1.7, 0.5)
        text(d, (W / 2, y0 + 300), "✓ F = (số cân, đổi ra kg) · g", 46, (21, 110, 55), alpha=ka)
        text(d, (W / 2, y0 + 385), "= 0,92·10⁻³ kg · 9,8 m/s²", 44, (21, 110, 55), alpha=ka)
        text(d, (W / 2, y0 + 465), "≈ 9,0·10⁻³ N", 46, (21, 110, 55), alpha=ka)
    if k2 > 0:
        y0 = 1040 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Hai cầu khác dấu thì sao?", "• r rất nhỏ: còn là điện tích điểm?")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (80, y0 + 220 + j * 140), l1, 42, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: r = 8 cm (chua tung hien) can chi khoang bao nhieu; goi y tre 2,5 s."""
    M = sc["M"]
    def body(d, t, k):
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 36, MUTED, bold=False, alpha=kh)
        ctext(d, 1445, "F·r² không đổi", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "F tỉ lệ nghịch với r²", "Ở r = 2 cm cân chỉ 0,92 g.\nỞ r = 8 cm, cân chỉ\nkhoảng bao nhiêu gam?", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
           (do["t0"] + DOWN0, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-coulomb-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Lực Coulomb · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cân điện tử đo lực đẩy", draw=s_hook, tail=0.8, caps=[
   ("B đẩy A xuống, số cân tăng.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Trừ bì, rồi hạ B tới r = 2 cm.", 4.8),
   ("Nâng B dần lên, mỗi lần một điểm.", 4.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Cột F·r² gần như không đổi.", 4.0),
   ("Hai hàng cuối lệch nhiều nhất.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 3.6),
   ("Mới đo với một cặp điện tích.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
