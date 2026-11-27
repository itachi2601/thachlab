# Clip: tn-l12-noinang-01 - Bom xe bang tay: than bom nong o dau?
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-noinang-01.json:
#   so_lieu_mau: so lan an 0/10/20/30/45 -> nhiet do than bom (o day) 26,0/27,5/29,0/31,0/34,0 °C.
#   Hang 60 lan (37,0 °C) chi hien o THU NGHI lam moc so sanh. Cot "Tong cong A" khong hien.
# Ban 1 (14/11/2026). Ban 3 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2 s), <= 50 s, K10 (khong nut A-D, khong "chon dap an"), bo canh "chua noi duoc"
#   (giu trong khung web), Bay ve hai hinh canh nhau: "neu do ma sat" (nong deu doc doan pit-tong truot) / "that ra" (day nong nhat).
# Du doan (khung web): "Bom nhanh 45 lan. Cho nao tren than bom nong nhat?" A tren / B deu doc than (y ma sat,
#   hien_tuong_hay_sai[0]) / C day, gan van (DUNG) / D khong nong.
# Co che: khi bi nen nhan cong A > 0, an nhanh Q ≈ 0 -> dU > 0; cuoi moi lan an khi nong nhat don ve day (con 40 cm3).
# THU NGHI (= cau_chot khung, CA TU SUY ghi trong kho): an cham 60 lan -> thap hon 37,0 °C (khi kip toa nhiet, Q < 0).
#   Luu y: hop thi nghiem trong bai co cau "Bom nhanh nong hon bom cham" (du doan neu dung) -> bao phien chinh.
from engine import *

ROWS = ((0, 26.0), (10, 27.5), (20, 29.0), (30, 31.0), (45, 34.0))
T60 = 37.0

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-noinang-01.json")))
    hang = {r[0]: r[2] for r in k["so_lieu_mau"]["hang"]}
    for n, v in ROWS: assert hang[n] == v, (n, v)
    assert hang[60] == T60
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["V0"]["gia_tri"] == 200 and ts["V1"]["gia_tri"] == 40
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
FS = 58
METAL = (205, 210, 222); METAL_D = (120, 126, 140)
SCREEN = (24, 30, 40); LCD = (134, 239, 172)
def vn(x): return f"{x:.1f}".replace(".", ",")

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- ong bom ----------------
BTOP, BBOT = 430, 1050
PY_UP, PY_DN = 470, 930
random.seed(11)
MOL = [(random.random(), random.random(), random.uniform(0.6, 1.0) * random.choice((1, -1)),
        random.uniform(0.6, 1.0) * random.choice((1, -1))) for _ in range(14)]

def hot_bottom(y, heat):
    f = clamp((y - BTOP) / (BBOT - BTOP)) ** 1.6
    return mix(METAL, (239, 68, 68), clamp(heat * f))

def hot_even(y, heat):
    f = 0.55 if PY_UP <= y <= PY_DN + 20 else 0.1
    return mix(METAL, (239, 68, 68), clamp(heat * f))

def pump(d, t, cx, py, heat, tire=False, s_gas=0.0, col=hot_bottom, gas_hot=0.0):
    x0, x1 = cx - 50, cx + 50
    if tire:
        tx, ty = 880, 970
        d.ellipse([tx - 120, ty - 120, tx + 120, ty + 120], fill=(60, 64, 76))
        d.ellipse([tx - 78, ty - 78, tx + 78, ty + 78], fill=BG)
        d.ellipse([tx - 66, ty - 66, tx + 66, ty + 66], outline=GRAY, width=6)
        d.line([(x1, 1030), (640, 1030), (700, 1000), (765, 985)], fill=NAVY, width=9, joint="curve")
    d.rounded_rectangle([cx - 160, 1050, cx + 160, 1090], radius=12, fill=METAL_D)
    for y in range(BTOP, BBOT, 6):
        d.rectangle([x0, y, x1, y + 6], fill=col(y + 3, heat))
    d.rectangle([x0 + 12, py + 22, x1 - 12, BBOT - 10], fill=mix((236, 242, 250), (254, 202, 202), gas_hot))
    y0g, y1g = py + 34, BBOT - 22
    for u0, v0, vu, vv in MOL:
        u = refl(u0 + vu * s_gas, 0, 1); v = refl(v0 + vv * s_gas, 0, 1)
        dot(d, x0 + 26 + u * (x1 - x0 - 52), y0g + v * max(4, y1g - y0g), 8, BLUE)
    d.rectangle([x0, BTOP, x1, BBOT], outline=NAVY, width=5)
    d.rectangle([x0 + 6, py, x1 - 6, py + 22], fill=NAVY)
    d.rectangle([x0 + 44, py - 150, x1 - 44, py], fill=METAL_D)
    d.rounded_rectangle([cx - 140, py - 180, cx + 140, py - 142], radius=18, fill=NAVY)
    dot(d, x1 + 8, 1030, 12, NAVY)

PX = 470                                              # tam ong bom o canh 1-4

def zone_labels(d, alpha=1.0):
    for y, s in ((560, "phần trên"), (760, "giữa"), (960, "đáy,")):
        d.line([(PX - 64, y), (PX - 52, y)], fill=A(INK, alpha), width=5)
        text(d, (PX - 76, y), s, FS, INK, anchor="rm", alpha=alpha)
    text(d, (PX - 76, 1030), "gần van", FS, INK, anchor="rm", alpha=alpha)

def readout(d, n, temp, lab="đáy thân bơm"):
    card(d, (610, 270, 1040, 450), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (825, 318), "lần ấn", FS, INK)
    text(d, (825, 400), str(n), 66, NAVY)
    card(d, (610, 480, 1040, 720), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (825, 528), lab, FS, INK)
    card(d, (640, 575, 1010, 695), fill=SCREEN, r=14)
    text(d, (825, 635), temp + " °C", 64, LCD)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    pump(d, t, PX, PY_UP, 0.0, tire=True, s_gas=t * 0.25)
    zone_labels(d)
    readout(d, 0, vn(ROWS[0][1]), "thân bơm")
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1150 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 430), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 180), "Bơm nhanh 45 lần:", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 265), "chỗ nào nóng nhất?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 335, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
def n_at(t, sc):
    a, b = sc["M"][0] + 0.2, sc["M"][1] - 0.2
    return int(45 * clamp((t - a) / (b - a)) + 1e-6)

def temp_at(n):
    """noi suy tuyen tinh giua cac hang so_lieu_mau"""
    for (m0, v0), (m1, v1) in zip(ROWS, ROWS[1:]):
        if n <= m1: return v0 + (v1 - v0) * (n - m0) / (m1 - m0)
    return ROWS[-1][1]

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    n = n_at(t, sc)
    a, b = M[0] + 0.2, M[1] - 0.2
    pumping = a <= t < b
    if pumping:
        ph = ((t - a) / 0.4) % 1                     # hinh: 1 lan an / 0,4 s (tua nhanh, so dem chay theo 45 lan)
        py = lerp(PY_UP, PY_DN, ease(ph / 0.45)) if ph < 0.45 else lerp(PY_DN, PY_UP, ease((ph - 0.45) / 0.55))
    else:
        py = PY_UP
    heat = (temp_at(n) - 26.0) / 8.0
    pump(d, t, PX, py, 0.0, tire=True, s_gas=t * (0.25 + 0.5 * heat))
    readout(d, n, vn(round(temp_at(n), 1)))
    if pumping:
        arrow(d, (210, 300), (210, 450), RED, w=9, head=26)
    if t < b:
        wdt = tw(d, "TUA NHANH", F(FS)) + 100
        card(d, (825 - wdt / 2, 732, 825 + wdt / 2, 804), fill=ORANGE, r=36)
        text(d, (825 + 24, 768), "TUA NHANH", FS, WHITE)
        for kk in range(2):
            tx = 825 - wdt / 2 + 26 + kk * 18; d.polygon([(tx, 750), (tx, 786), (tx + 18, 768)], fill=WHITE)
    for j in range(5):                                  # tia nhiet ke hong ngoai toi day
        u = j / 4
        d.line([(lerp(640, PX + 56, u) - 4, lerp(695, 990, u)), (lerp(640, PX + 56, u) + 4, lerp(695, 990, u))], fill=RED, width=5)
    k = appear(t, M[1] + 0.3, 0.4)
    if k <= 0: return
    card(d, (40, 1150, 1040, 1420), fill=A(WHITE, k), outline=A(LIGHT, k), w=4)
    text(d, (70, 1215), "Lần ấn", FS, INK, anchor="lm", alpha=k)
    text(d, (70, 1345), "°C", FS, INK, anchor="lm", alpha=k)
    d.line([(60, 1280), (1020, 1280)], fill=A(LIGHT, k), width=3)
    for j, (m, v) in enumerate(ROWS):
        x = 340 + j * 150
        text(d, (x, 1215), str(m), FS, INK, alpha=k)
        text(d, (x, 1345), vn(v), FS, DORANGE, alpha=k)
    text(d, (1010, 1110), "số minh hoạ", FS, PURPLE, anchor="rm", alpha=k)

# ---------------- canh 3: Ket qua ----------------
def s_kq(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    pump(d, t, PX, PY_UP, 1.0, s_gas=t * 0.5)
    zone_labels(d)
    text(d, (825, 340), "Sờ dọc thân bơm", FS, INK)
    text(d, (825, 420), "màu: minh hoạ", FS, PURPLE)
    k = appear(t, 0.3, 0.4)
    if k > 0:
        d.rounded_rectangle((PX - 72, 900, PX + 90, 1070), radius=30, outline=A(RED, k), width=8)
    k2 = appear(t, M[1], 0.4)
    if k2 > 0:
        card(d, (610, 560, 1040, 860), fill=A(WHITE, k2), outline=A(RED, k2), w=5)
        text(d, (825, 620), "đáy, 45 lần", FS, INK, alpha=k2)
        text(d, (825, 720), "+8,0 °C", 80, DRED, alpha=k2)
        text(d, (825, 805), "26,0 → 34,0", FS, DORANGE, alpha=k2)

# ---------------- canh 4: co che ----------------
def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    p = ease(clamp(t / (M[1] + 2.5)))
    py = lerp(PY_UP, 908, p)                       # 908: khi con 20 % = 40/200 cm3
    pump(d, t, PX, py, 0.6 * p, s_gas=t * (0.3 + 1.2 * p), gas_hot=p)
    text(d, (PX - 76, 900), "còn", FS, INK, anchor="rm")
    text(d, (PX - 76, 970), "40 cm³", FS, BLUE, anchor="rm")
    arrow(d, (PX + 140, 330), (PX + 140, 520), RED, w=9, head=26)
    card(d, (555, 600, 1065, 980), fill=WHITE, outline=GREEN, w=5)
    text(d, (810, 680), "ΔU = A + Q", 64, INK)
    k1 = appear(t, 2.0, 0.4)
    text(d, (578, 800), "A > 0: nhận công", 56, DGREEN, anchor="lm", alpha=k1)
    text(d, (578, 900), "Q ≈ 0: ấn nhanh", 56, DORANGE, anchor="lm", alpha=k1)
    k3 = appear(t, M[1], 0.4)
    if k3 > 0:
        for yy in (965, 1015):
            arrow(d, (PX + 10, yy), (PX + 95, yy), A(RED, k3 * (0.6 + 0.4 * math.sin(t * 5))), w=7, head=20)
        card(d, (60, 1180, 1020, 1330), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1255), "→ ΔU > 0: khí nóng lên", 64, DGREEN, alpha=k3)

# ---------------- canh 5: Bay (hai hinh canh nhau) ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for cx, lab, col, fn in ((285, "Nếu do ma sát", DRED, hot_even), (795, "Thật ra", DGREEN, hot_bottom)):
        card(d, (cx - 245, 250, cx + 245, 1330), fill=WHITE, outline=col, w=6)
        text(d, (cx, 310), lab, 62, col)
        pump(d, t, cx, PY_DN, 1.0, s_gas=t * 0.5, col=fn)
    text(d, (285, 1170), "nóng đều", FS, DRED)
    text(d, (285, 1250), "dọc ống?", FS, DRED)
    k = appear(t, M[1], 0.4)
    text(d, (795, 1170), "đáy", FS, DGREEN, alpha=k)
    text(d, (795, 1250), "nóng nhất", FS, DGREEN, alpha=k)

# ---------------- canh 6: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    for j, (lab, val, col) in enumerate((("nhanh, 60 lần", vn(T60) + " °C", LCD), ("chậm, 60 lần", "? °C", YELLOW))):
        x0 = 85 + j * 470
        card(d, (x0, 400, x0 + 440, 720), fill=A(WHITE, k1), outline=A(NAVY, k1), r=22, w=4)
        text(d, (x0 + 220, 460), lab, FS, INK, alpha=k1)
        card(d, (x0 + 30, 520, x0 + 410, 690), fill=A(SCREEN, k1), r=14)
        text(d, (x0 + 220, 605), val, 70, col, alpha=k1)
    text(d, (W / 2, 1000), "Cùng 60 lần, ấn chậm:", 64, INK, alpha=k1)
    text(d, (W / 2, 1090), "cao hay thấp hơn", 64, DORANGE, alpha=k1)
    text(d, (W / 2, 1180), "37,0 °C?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1320, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, w, b, e = (sc[x] for x in ("hook", "do", "kq", "why", "trap", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"), (do["t0"] + do["M"][0] + 0.2, "tap")]
    out += [(do["t0"] + do["M"][1] + 0.3, "tap"), (kq["t0"] + 0.3, "ding"), (w["t0"] + w["M"][1], "tap"),
            (b["t0"] + 0.6, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-noinang-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Nội năng · Định luật 1 NĐLH · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bơm xe bằng tay", draw=s_hook, tail=0.3, caps=[
   ("Bánh xe còn non hơi.", 3.4),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Ấn nhanh, đo đáy thân bơm", draw=s_do, tail=0.4, caps=[
   ("Ấn nhanh liên tục 45 lần.", 3.6),
   ("Nhiệt kế chỉ vào đáy bơm.", 3.8)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.4, caps=[
   ("Đáp án: đáy, gần van nóng nhất.", 3.8),
   ("Số đo ở đáy: tăng 8,0 °C.", 3.4)]),
 dict(key="why", title="Vì sao đáy nóng nhất?", draw=s_why, tail=0.4, caps=[
   ("Nén khí: A > 0; ấn nhanh: Q ≈ 0.", 4.2),
   ("Khí bị nén ở đáy, truyền nhiệt ra thành.", 3.6)]),
 dict(key="trap", title="Bẫy: nóng do ma sát?", draw=s_trap, tail=0.4, caps=[
   ("Ma sát có, nhưng dọc cả ống.", 3.4),
   ("Đáy nóng nhất: do nén khí.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Nén khí: khí nhận công, A > 0.", 6.4)]),
])
