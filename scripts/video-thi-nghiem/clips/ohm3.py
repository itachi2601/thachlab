# Clip: tn-l11-dien-tro-ohm-03 - Dien tro nhiet NTC trong coc nuoc am: nong thi dien tro giam (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-tro-ohm-03.json (ghi_chu: "Khong phai so do that" -> nhan
#   "số liệu mô phỏng"):
#   so_lieu_mau (t C, R kOhm): 25 10,0 ; 35 6,5 ; 45 4,3 ; 55 3,0 ; dung_cu: NTC 10 kOhm, dong ho thang 20 kOhm.
#   Duong cong tren do thi = mo_hinh R = R0.exp[B(1/T - 1/T0)], R0 = 10 kOhm, B = 3950 K (di qua 4 diem trong sai so 0,1).
#   Do giam moi 10 C (3,5 ; 2,2 ; 1,3 kOhm) = hieu cac hang so_lieu_mau. "giam hon 3 lan" = quan_sat.
#   Day dong so sanh (bay 2) = goi_y_mo_phong: R = R0[1 + 0,0039(t - 25)], cung 10 kOhm o 25 C.
#   Cau hoi chot: dong ho chi 5,0 kOhm (chua tung hien) -> t ~ 41 C theo mo hinh, nam giua 35 va 45 C.
# Do (vat li): ohm ke mac thang hai chan NTC (khong nguon ngoai). Nhiet ke, so chi dong ho va hang bang doi CUNG luc
#   o moi lan do (kiem bang ma moi 0,05 s: _kiem_dong_bo()).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (25 C cham, tua nhanh 35/45/55 C) -> Dap an (do thi R-t cong,
#       buoc giam nho dan) + Rut ra -> Bay (kim loai tang nhe / NTC giam manh) roi Chua noi duoc -> Chot + tu nho lai.
import math
from engine import *

ROWS = [(25, 10.0), (35, 6.5), (45, 4.3), (55, 3.0)]          # so_lieu_mau
R0, B = 10.0, 3950.0                                           # tham_so
def r_ntc(t): return R0 * math.exp(B * (1 / (t + 273.15) - 1 / 298.15))
def r_cu(t): return R0 * (1 + 0.0039 * (t - 25))               # goi_y_mo_phong (day dong)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
DROPS = [round(ROWS[i][1] - ROWS[i + 1][1], 1) for i in range(3)]  # 3,5 2,2 1,3
DRED = (185, 28, 28)
BOXF = (70, 78, 100)
SCR = (220, 240, 225)
WRED, WBLK = (200, 40, 40), (40, 40, 48)
COLD, WARM, HOT = (200, 228, 250), (253, 240, 185), (255, 190, 135)
def water(w):   # w 0..1 ung 25..55 C: xanh (25) -> vang nhat (35) -> cam (45-55)
    return mix(COLD, WARM, w * 3) if w < 1 / 3 else mix(WARM, HOT, (w - 1 / 3) * 1.5)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
BX0, BX1, BTOP, BBOT = 380, 760, 520, 940       # coc
TX = 680                                        # ong nhiet ke
def ty(t): return 490 - (t - 20) * 4            # dinh cot nhiet ke (thang 20-60 C o tren mieng coc)

def apparatus(d, j, warm=None, pour=0.0, read=None):
    """j = chi so hang dang chi (nhiet ke + dong ho); warm = 0..1 mau nuoc (mac dinh theo j); pour > 0 ve mui ten rot."""
    tj, rj = ROWS[j]
    if warm is None: warm = (tj - 25) / 30
    lvl = 650 - 30 * (warm * 3)                                  # muc nuoc nhinh len khi pha them
    # coc nuoc
    d.rectangle([BX0 + 6, lvl, BX1 - 6, BBOT - 6], fill=water(warm))
    d.line([(BX0 + 6, lvl), (BX1 - 6, lvl)], fill=mix((120, 160, 210), (230, 140, 100), warm), width=4)
    d.line([(BX0, BTOP), (BX0, BBOT), (BX1, BBOT), (BX1, BTOP)], fill=NAVY, width=7, joint="curve")
    d.line([(BX0 - 18, BTOP), (BX0, BTOP)], fill=NAVY, width=7); d.line([(BX1, BTOP), (BX1 + 18, BTOP)], fill=NAVY, width=7)
    text(d, (BX0 + 70, BBOT - 40), "nước", 40, MUTED, bold=False)
    # nhiet ke
    d.rounded_rectangle([TX - 13, 330, TX + 13, 880], radius=13, fill=WHITE, outline=NAVY, width=4)
    dot(d, TX, 892, 24, RED, outline=NAVY)
    d.rectangle([TX - 5, ty(tj), TX + 5, 885], fill=RED)
    for tt in range(20, 61, 5):
        L = 18 if tt % 10 == 0 else 10
        d.line([(TX + 13, ty(tt)), (TX + 13 + L, ty(tt))], fill=NAVY, width=3)
        if tt % 10 == 0: text(d, (TX + 40, ty(tt)), str(tt), 40, MUTED, bold=False, anchor="lm")
    card(d, (810, 610, 1040, 720), fill=WHITE, outline=NAVY, r=20, w=4)
    text(d, (925, 580), "nhiệt kế", 40, MUTED, bold=False)
    text(d, (925, 665), f"{tj} °C", 46, RED)
    # NTC: hai chan + hat den trong nuoc
    d.line([(470, 400), (483, 845)], fill=GRAY, width=5); d.line([(510, 400), (497, 845)], fill=GRAY, width=5)
    d.ellipse([470, 842, 510, 882], fill=(35, 35, 40), outline=NAVY, width=3)
    text(d, (545, 862), "NTC", 40, INK, anchor="lm")
    # day do + kep ca sau
    d.line([(290, 640), (318, 640), (318, 360), (510, 360), (510, 392)], fill=WRED, width=6, joint="curve")
    d.line([(290, 700), (342, 700), (342, 380), (470, 380), (470, 392)], fill=WBLK, width=6, joint="curve")
    for x, c in ((470, WBLK), (510, WRED)): d.rectangle([x - 9, 388, x + 9, 418], fill=c)
    # dong ho van nang (thang Ohm)
    card(d, (40, 340, 290, 760), fill=BOXF, r=22)
    card(d, (54, 368, 276, 462), fill=SCR, r=10)
    text(d, (165, 416), read if read is not None else f"{vn(rj)} kΩ", 44, (20, 60, 30))
    text(d, (150, 535), "thang Ω", 40, WHITE, bold=False)
    text(d, (150, 590), "20 kΩ", 40, WHITE)
    for y, c in ((640, WRED), (700, WBLK)): dot(d, 272, y, 14, c, outline=WHITE)
    # rot nuoc nong
    if pour > 0:
        k = clamp(pour / 0.25) * clamp((1 - pour) / 0.2)
        if k > 0:
            arrow(d, (1000, 470), (780, 548), A(ORANGE, k), w=11, head=30)
            text(d, (920, 425), "nước nóng", 40, ORANGE, alpha=k)

def table(d, n, y=1000, hl=None):
    card(d, (120, y, 960, y + 470), fill=WHITE, outline=NAVY, w=4)
    xs = (340, 740)
    for x, c in zip(xs, ("t (°C)", "R (kΩ)")): text(d, (x, y + 50), c, 40, INK)
    d.line([(150, y + 90), (930, y + 90)], fill=LIGHT, width=4)
    for i in range(4):
        yy = y + 136 + i * 80
        if i < n:
            if hl == i: d.rounded_rectangle([140, yy - 36, 940, yy + 36], radius=18, fill=(255, 237, 213))
            text(d, (xs[0], yy), str(ROWS[i][0]), 44, INK); text(d, (xs[1], yy), vn(ROWS[i][1]), 44, BLUE)
        else:
            text(d, (xs[0], yy), "·", 44, GRAY); text(d, (xs[1], yy), "·", 44, GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 270, "Pha nước nóng dần lên\n35, 45 rồi 55 °C. Số chỉ kΩ\nthay đổi thế nào?", 50, INK, maxw=900,
          alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
TREC = 1.6               # lan 25 C: ghi hang 1 o t = TREC (so chi da on dinh tu dau)
FF0, FFW, SW = 0.2, 1.5, 0.7   # tua nhanh: moi lan FFW giay; rot nuoc 0..SW, roi nhiet ke + dong ho + hang bang doi o SW

def do_state(t, M1):
    """-> (j dang chi, so hang da ghi, pour 0..1 hoac 0, warm mau nuoc)."""
    if t < M1 + FF0:
        return 0, (1 if t >= TREC else 0), 0.0, 0.0
    w_all = t - M1 - FF0
    jj = 1 + min(2, int(w_all // FFW)); w = w_all - (jj - 1) * FFW
    if w < SW:
        p = w / SW
        return jj - 1, jj, p, ((ROWS[jj - 1][0] - 25) + 10 * ease(p)) / 30
    return jj, jj + 1, 0.0, (ROWS[jj][0] - 25) / 30

def s_do(img, d, t, sc):
    M = sc["M"]
    j, n, pour, warm = do_state(t, M[1])
    apparatus(d, j, warm=warm, pour=pour)
    hl = n - 1 if n > 0 else None
    table(d, n, hl=hl)
    if t >= M[1]:
        card(d, (760, 214, 1000, 274), fill=ORANGE, r=30); text(d, (880, 244), "tua nhanh", 40, WHITE)

def _kiem_dong_bo():
    """Moi 0,05 s: nhiet ke va dong ho cung mot hang; hang cuoi da ghi = hang dang chi (sau khi ghi)."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M1 = sc["M"][1]; t = 0.0; bad = []
    while t < sc["T"]:
        j, n, pour, warm = do_state(t, M1)
        if n > 0 and pour == 0 and n - 1 != j: bad.append((round(t, 2), "hang", j, n))
        if pour > 0 and n != j + 1: bad.append((round(t, 2), "rot", j, n))
        t += 0.05
    return bad

# ---------------- do thi R theo t (dung chung canh dap an + bay) ----------------
GX0, GX1, GY0, GY1 = 200, 960, 900, 420         # t 20-60 C ; R 0-12 kOhm (co dinh)
def gx(t): return GX0 + (t - 20) / 40 * (GX1 - GX0)
def gy(r): return GY0 - r / 12 * (GY0 - GY1)

def axes(d, note=True):
    card(d, (40, 320, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    if note: text(d, (1010, 362), "số liệu mô phỏng", 40, MUTED, bold=False, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 44), "R (kΩ)", 40, INK, anchor="lm")
    text(d, (1010, GY0 - 40), "t (°C)", 40, INK, anchor="rm")
    for r in (4, 8, 12):
        d.line([(GX0 - 12, gy(r)), (GX0, gy(r))], fill=NAVY, width=3)
        text(d, (GX0 - 22, gy(r)), str(r), 40, MUTED, bold=False, anchor="rm")
    text(d, (GX0 - 22, GY0), "0", 40, MUTED, bold=False, anchor="rm")
    for tt, _ in ROWS:
        d.line([(gx(tt), GY0), (gx(tt), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(tt), GY0 + 40), str(tt), 40, MUTED, bold=False)

def curve(d, f, k, col, w=6, a=1.0):
    if k <= 0: return
    t1 = 25 + 30 * k; n = max(2, int(60 * k))
    pts = [(gx(25 + (t1 - 25) * i / n), gy(f(25 + (t1 - 25) * i / n))) for i in range(n + 1)]
    d.line(pts, fill=A(col, a), width=w, joint="curve")

def points(d, t, at, col=BLUE):
    for i, (tt, r) in enumerate(ROWS):
        k = appear(t, at + 0.15 * i, 0.3)
        if k > 0: dot(d, gx(tt), gy(r), 14, A(col, k), outline=WHITE)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · Giảm, mỗi lần giảm ít dần"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W - 50 - pw, 234, W - 50, 298), fill=A(NAVY, ka), r=32)
    text(d, (W - 50 - pw / 2, 266), lab, 40, WHITE, alpha=ka)
    axes(d)
    curve(d, r_ntc, appear(t, 0.9, 1.0), BLUE, a=0.85)
    points(d, t, 0.2)
    # bac giam moi 10 C: ngang toi t sau, roi doc xuong diem sau
    for i in range(3):
        k = appear(t, M[0] + 0.5 + 0.5 * i, 0.4)
        if k <= 0: continue
        (ta, ra), (tb, rb) = ROWS[i], ROWS[i + 1]
        col = A(ORANGE, k)
        d.line([(gx(ta), gy(ra)), (gx(tb), gy(ra))], fill=col, width=4)
        d.line([(gx(tb), gy(ra)), (gx(tb), gy(rb) - 16)], fill=A(ORANGE, k), width=7)
        text(d, (gx(tb) + 16, (gy(ra) + gy(rb)) / 2 + (10 if i == 2 else 0)), "−" + vn(DROPS[i]), 40, ORANGE,
             anchor="lm", alpha=k)
    k1 = appear(t, M[0] + 0.5, 0.4) * (1 - appear(t, M[2] - 0.1, 0.3))
    if k1 > 0:
        card(d, (40, 1020, 1040, 1150), fill=A((255, 237, 213), k1), outline=A(ORANGE, k1), r=20, w=3)
        segs = ["Mỗi 10 °C giảm: ", vn(DROPS[0]), " → " + vn(DROPS[1]), " → " + vn(DROPS[2]) + " kΩ"]
        f = F(42); x = W / 2 - sum(tw(d, g, f) for g in segs) / 2
        for i, g in enumerate(segs):
            ki = k1 if i == 0 else k1 * appear(t, M[0] + 0.5 + 0.5 * (i - 1), 0.4)   # cung moc voi bac i - 1
            dtext(d, (x, 1085), g, f, (154, 52, 18), ki, "lm"); x += tw(d, g, f)
    k3 = appear(t, M[2] + 0.1, 0.45)
    if k3 > 0:
        y0 = 1020 + (1 - k3) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, k3), outline=A(GREEN, k3), w=6)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(GREEN, k3), r=32)
        text(d, (W / 2, y0 + 60), "RÚT RA", 40, WHITE, alpha=k3)
        ctext(d, y0 + 190, "NTC: hệ số nhiệt điện trở âm", 46, INK, maxw=920, alpha=k3)
        ctext(d, y0 + 290, "(nóng lên, R giảm)", 44, (21, 110, 55), maxw=920, alpha=k3)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d, note=False)
    curve(d, r_ntc, 1.0, BLUE, a=0.85); points(d, t, -1)
    kc = appear(t, 0.3, 0.6)
    if kc > 0:
        curve(d, r_cu, kc, ORANGE, w=7)
        ka = appear(t, 0.9, 0.3)
        text(d, (GX1, gy(r_cu(55)) - 40), "dây đồng", 40, ORANGE, anchor="rm", alpha=ka)
        text(d, (1010, 545), "(minh hoạ, cùng 10 kΩ ở 25 °C)", 40, (154, 52, 18), bold=False, anchor="rm", alpha=ka)
    text(d, (gx(47), gy(r_ntc(47)) - 60), "NTC", 40, BLUE)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 1020
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        k3 = a1 * appear(t, 0.6, 0.5); k4 = a1 * appear(t, 1.6, 0.5)
        ctext(d, y0 + 250, "Kim loại nóng: R tăng nhẹ", 44, (154, 52, 18), maxw=920, alpha=k3)
        ctext(d, y0 + 400, "NTC nóng: R giảm mạnh", 44, BLUE, maxw=920, alpha=k4)
    if k2 > 0:
        y0 = 1020 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Vì sao nóng lại dẫn tốt hơn?", "• Ngoài 25–55 °C có còn vậy?")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (80, y0 + 230 + j * 150), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: dong ho chi 5,0 kOhm thi nuoc bao nhieu do (nguoc chieu hop Du doan);
    goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Nóng lên, điện trở NTC giảm mạnh", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1520), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 880, "NTC này chỉ 5,0 kΩ.\nNước khoảng\nbao nhiêu °C?", 50, INK, maxw=920,
          alpha=appear(t, M[0] + 0.9, 0.5))
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 1140, 970, 1480), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1215, "Gợi ý", 40, INK, alpha=kh)
    ctext(d, 1355, "5,0 kΩ nằm giữa\nhai số chỉ nào?", 46, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding"),
           (do["t0"] + TREC, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW + SW, "tick") for j in range(3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-dien-tro-ohm-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="NTC trong cốc nước", draw=s_hook, tail=0.8, caps=[
   ("NTC cùng nhiệt kế trong nước.", 2.8),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Ở 25 °C, chờ số ổn định rồi ghi.", 4.0),
   ("Pha nước nóng, mỗi lần đo lại.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Đường cong, không phải đường thẳng.", 3.2),
   ("Nóng thêm 30 °C, R giảm hơn 3 lần.", 3.2),
   ("Đo R là suy ra được nhiệt độ.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.0, caps=[
   ("Bẫy: nóng lên thì R luôn tăng.", 3.8),
   ("Hai câu còn bỏ ngỏ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
