# Clip: tn-l11-dien-tro-ohm-03 - Dien tro nhiet NTC trong coc nuoc am: nong thi dien tro giam (ban 2 cong moi, 27/11/2026)
# Ban 2: chu >= 56 px, bo the Goi y + the chot, cac bac giam hien cung luc, nhip Bay >= 3 s.
# Nhieu cau chot: 15 C (nghi R giam la nguoi di, nhu kim loai), 50 C (R con mot nua -> t gap doi), 60 C (dung buoc giam 1,3 kOhm/10 C).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-tro-ohm-03.json (ghi_chu: "Khong phai so do that" -> nhan
#   "số liệu mô phỏng"):
#   so_lieu_mau (t C, R kOhm): 25 10,0 ; 35 6,5 ; 45 4,3 ; 55 3,0 ; dung_cu: NTC 10 kOhm, dong ho thang 20 kOhm.
#   Duong cong tren do thi = mo_hinh R = R0.exp[B(1/T - 1/T0)], R0 = 10 kOhm, B = 3950 K (di qua 4 diem trong sai so 0,1).
#   Do giam moi 10 C (3,5 ; 2,2 ; 1,3 kOhm) = hieu cac hang so_lieu_mau. "giam hon 3 lan" = quan_sat.
#   Day dong so sanh (bay 2) = goi_y_mo_phong: R = R0[1 + 0,0039(t - 25)], cung 10 kOhm o 25 C.
#   Cau hoi chot: dong ho chi 5,0 kOhm (chua tung hien) -> t ~ 41 C theo mo hinh (r_ntc(41) = 5,09), giua 35 va 45 C.
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

DGREEN = (21, 110, 55); EMPTY = (148, 140, 128)
assert abs(r_ntc(41) - 5.0) < 0.15

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
BX0, BX1, BTOP, BBOT = 380, 760, 520, 940       # coc
TX = 700                                        # ong nhiet ke
def ty(t): return 490 - (t - 20) * 4            # dinh cot nhiet ke (thang 20-60 C o tren mieng coc)

def meter(d, reading, x0=30, x1=300):
    card(d, (x0, 340, x1, 760), fill=BOXF, r=22)
    card(d, (x0 + 12, 368, x1 - 12, 470), fill=SCR, r=10)
    text(d, ((x0 + x1) / 2, 419), reading, 58, (20, 60, 30))
    text(d, ((x0 + x1) / 2 - 10, 540), "thang Ω", 56, WHITE)
    text(d, ((x0 + x1) / 2 - 10, 605), "20 kΩ", 56, WHITE)
    for y, c in ((640, WRED), (700, WBLK)): dot(d, x1 - 18, y, 14, c, outline=WHITE)

def apparatus(d, j, warm=None, pour=0.0, read=None, tlabel=None):
    """j = chi so hang dang chi (nhiet ke + dong ho); warm = 0..1 mau nuoc (mac dinh theo j); pour > 0 ve mui ten rot."""
    tj, rj = ROWS[j]
    if warm is None: warm = (tj - 25) / 30
    lvl = 650 - 30 * (warm * 3)
    d.rectangle([BX0 + 6, lvl, BX1 - 6, BBOT - 6], fill=water(warm))
    d.line([(BX0 + 6, lvl), (BX1 - 6, lvl)], fill=mix((120, 160, 210), (230, 140, 100), warm), width=4)
    d.line([(BX0, BTOP), (BX0, BBOT), (BX1, BBOT), (BX1, BTOP)], fill=NAVY, width=7, joint="curve")
    d.line([(BX0 - 18, BTOP), (BX0, BTOP)], fill=NAVY, width=7); d.line([(BX1, BTOP), (BX1 + 18, BTOP)], fill=NAVY, width=7)
    text(d, (565, lvl + 60), "nước", 56, MUTED, bold=False)
    d.rounded_rectangle([TX - 13, 330, TX + 13, 880], radius=13, fill=WHITE, outline=NAVY, width=4)
    dot(d, TX, 892, 24, RED, outline=NAVY)
    d.rectangle([TX - 5, ty(tj), TX + 5, 885], fill=RED)
    for tt in range(20, 61, 10):
        d.line([(TX + 13, ty(tt)), (TX + 31, ty(tt))], fill=NAVY, width=3)
    card(d, (800, 610, 1040, 720), fill=WHITE, outline=NAVY, r=20, w=4)
    text(d, (920, 570), "nhiệt kế", 56, MUTED, bold=False)
    text(d, (920, 665), tlabel if tlabel else f"{tj} °C", 58, RED)
    d.line([(470, 400), (483, 845)], fill=GRAY, width=5); d.line([(510, 400), (497, 845)], fill=GRAY, width=5)
    d.ellipse([470, 842, 510, 882], fill=(35, 35, 40), outline=NAVY, width=3)
    text(d, (600, 862), "NTC", 56, INK)
    d.line([(300, 640), (318, 640), (318, 360), (510, 360), (510, 392)], fill=WRED, width=6, joint="curve")
    d.line([(300, 700), (342, 700), (342, 380), (470, 380), (470, 392)], fill=WBLK, width=6, joint="curve")
    for x, c in ((470, WBLK), (510, WRED)): d.rectangle([x - 9, 388, x + 9, 418], fill=c)
    meter(d, read if read is not None else f"{vn(rj)} kΩ")
    if pour > 0:
        k = clamp(pour / 0.25) * clamp((1 - pour) / 0.2)
        if k > 0:
            arrow(d, (1000, 500), (790, 560), A(ORANGE, k), w=11, head=30)
            pill(d, 860, 300, "nước nóng", ORANGE, k, size=56)

def table(d, n, y=1000, hl=None):
    card(d, (120, y, 960, y + 110 + 4 * 80), fill=WHITE, outline=NAVY, w=4)
    xs = (340, 740)
    for x, c in zip(xs, ("t (°C)", "R (kΩ)")): text(d, (x, y + 52), c, 56, INK)
    d.line([(150, y + 96), (930, y + 96)], fill=LIGHT, width=4)
    for i in range(min(n, 4)):
        yy = y + 140 + i * 80
        if hl == i: d.rounded_rectangle([140, yy - 36, 940, yy + 36], radius=18, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(ROWS[i][0]), 58, INK); text(d, (xs[1], yy), vn(ROWS[i][1]), 58, BLUE)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, 0)
    a = appear(t, M[1] - 0.2, 0.4)
    if a <= 0: return
    y0 = 990 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Pha nước nóng lên", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 280), "35, 45 rồi 55 °C.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 380), "Số chỉ kΩ đổi thế nào?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 485, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
TREC = 1.6
FF0, FFW, SW = 0.2, 1.5, 0.7

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
    table(d, n, hl=n - 1 if n > 0 else None)
    if t >= M[1] and pour == 0: pill(d, 900, 245, "tua nhanh", ORANGE, appear(t, M[1], 0.25), size=56)

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
GX0, GX1, GY0, GY1 = 220, 930, 880, 470         # t 20-60 C ; R 0-12 kOhm (co dinh)
def gx(t): return GX0 + (t - 20) / 40 * (GX1 - GX0)
def gy(r): return GY0 - r / 12 * (GY0 - GY1)

def axes(d, note=True):
    card(d, (40, 360, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    if note: text(d, (1010, 405), "số liệu mô phỏng", 56, MUTED, bold=False, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 40), "R (kΩ)", 56, INK, anchor="lm")
    text(d, (1020, GY0 - 50), "t (°C)", 56, INK, anchor="rm")
    for r in (4, 8, 12):
        d.line([(GX0 - 12, gy(r)), (GX0, gy(r))], fill=NAVY, width=3)
        text(d, (GX0 - 22, gy(r)), str(r), 56, MUTED, bold=False, anchor="rm")
    for tt, _ in ROWS:
        d.line([(gx(tt), GY0), (gx(tt), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(tt), GY0 + 50), str(tt), 56, MUTED, bold=False)

def curve(d, f, k, col, w=6, a=1.0):
    if k <= 0: return
    t1 = 25 + 30 * k; n = max(2, int(60 * k))
    pts = [(gx(25 + (t1 - 25) * i / n), gy(f(25 + (t1 - 25) * i / n))) for i in range(n + 1)]
    d.line(pts, fill=A(col, a), width=w, joint="curve")

def points(d):
    for tt, r in ROWS: dot(d, gx(tt), gy(r), 15, BLUE, outline=WHITE)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 290, "ĐÁP ÁN · giảm, ít dần", NAVY)
    axes(d)
    curve(d, r_ntc, appear(t, 0.6, 1.0), BLUE, a=0.85)
    points(d)
    k = appear(t, M[1] + 0.2, 0.4)
    if k > 0:
        for i in range(3):
            (ta, ra), (tb, rb) = ROWS[i], ROWS[i + 1]
            col = A(ORANGE, k)
            d.line([(gx(ta), gy(ra)), (gx(tb), gy(ra))], fill=col, width=4)
            d.line([(gx(tb), gy(ra)), (gx(tb), gy(rb) - 16)], fill=col, width=7)
        card(d, (40, 1030, 1040, 1200), fill=A((255, 237, 213), k), outline=A(ORANGE, k), r=20, w=4)
        text(d, (W / 2, 1115), "−3,5   −2,2   −1,3 kΩ", 64, (154, 52, 18), alpha=k)
    kr = appear(t, M[1] + 2.8, 0.45)
    if kr > 0:
        y0 = 1240 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pill(d, W / 2, y0 + 70, "RÚT RA", GREEN, kr)
        text(d, (W / 2, y0 + 200), "NTC: nóng lên thì R giảm", 62, INK, alpha=kr)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d, note=False)
    curve(d, r_ntc, 1.0, BLUE, a=0.85); points(d)
    text(d, (gx(47), gy(r_ntc(47)) - 60), "NTC", 56, BLUE)
    k2 = appear(t, M[1] - 0.1, 0.4); k3 = appear(t, M[2] - 0.1, 0.45)
    if k2 > 0:
        curve(d, r_cu, k2, ORANGE, w=7)
        text(d, (GX1, gy(r_cu(55)) - 50), "dây đồng", 56, ORANGE, anchor="rm", alpha=k2)
    a1 = 1.0 - k3; y0 = 1030
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
        q = "“Nóng lên thì R luôn tăng”"
        f = F(60); lw = tw(d, q, f); yy = y0 + 210
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, k2), alpha=a1)
        if k2 > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * k2, yy + 2)], fill=A(DRED, 0.85 * a1), width=7)
            text(d, (W / 2, y0 + 380), "NTC: R giảm mạnh", 60, BLUE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y0 + 290), "Vì sao nóng lại dẫn tốt hơn?", 60, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    """THU NGHI: dong ho chi 5,0 kOhm -> nuoc khoang bao nhieu do? (~41 C, khong hien)."""
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    card(d, (200, 420, 520, 640), fill=A(BOXF, k), r=22)
    card(d, (220, 445, 500, 545), fill=A(SCR, k), r=10)
    text(d, (360, 495), "5,0 kΩ", 62, (20, 60, 30), alpha=k)
    text(d, (360, 595), "NTC này", 56, WHITE, alpha=k)
    card(d, (600, 450, 880, 610), fill=A(WHITE, k), outline=A(NAVY, k), r=20, w=4)
    text(d, (740, 530), "? °C", 64, RED, alpha=k)
    text(d, (W / 2, 800), "Đồng hồ chỉ 5,0 kΩ.", 64, INK, alpha=k)
    text(d, (W / 2, 900), "Nước khoảng bao nhiêu °C?", 64, DRED, alpha=k)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + TREC, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW + SW, "tick") for j in range(3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-dien-tro-ohm-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="NTC trong cốc nước", draw=s_hook, tail=0.3, caps=[
   ("NTC và nhiệt kế ở 25 °C.", 3.6),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Chờ số ổn định rồi ghi.", 4.0),
   ("Pha nước nóng, đo lại.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Đường cong, đi xuống.", 3.6),
   ("Mỗi 10 °C, R giảm ít dần.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.2, caps=[
   ("Bẫy: nhớ theo kim loại.", 3.6),
   ("Dây đồng: minh hoạ.", 3.6),
   ("Mới đo từ 25 đến 55 °C.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự trả lời.", 7.2)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
