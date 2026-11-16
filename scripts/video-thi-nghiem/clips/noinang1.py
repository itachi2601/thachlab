# Clip: tn-l12-noinang-01 - Bom xe bang tay: than bom nong o dau? (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-noinang-01.json:
#   so_lieu_mau: so lan an 0/10/20/30/45 -> nhiet do than bom 26,0/27,5/29,0/31,0/34,0 °C (hang 60 lan, 37,0 °C de danh cho THU NGHI)
#   tham_so: V0 = 200 cm3, V1 = 40 cm3. Cot "Tong cong A" KHONG hien: 258 J/10 lan = 25,8 J/lan lech A1 ≈ 32,2 J cua ghi_chu (bao phien chinh).
#   Q ≈ 0 khi an nhanh, bo qua nhiet tu tay (cac_buoc.lam[3]) -> dong "Coi rằng".
# Du doan (khung; K10: trong mp4 KHONG ve nut A-D, chi cau hoi + hinh co nhan ba vung cung kieu):
#   "Bom nhanh 45 lan. Cho nao tren than bom nong nhat?"
#   A. Phan tren, gan tay cam   B. Deu doc ca than bom   C. Phan day, gan van (DUNG)   D. Khong cho nao nong len
#   (B la y "do ma sat" - pit-tong co doc ca ong; A la y "tay cam nong vi tay"; D sai ro vi so do tang 26,0 -> 34,0)
# Rut ra: cuoi moi lan an khi nong don ve day (con 40 cm3), Q ≈ 0, A > 0, Q ≈ 0 -> dU > 0; ma sat doc ca ong khong giai thich duoc day nong nhat.
# Bay (hien_tuong_hay_sai[1] + dau trong dU = A + Q): "khi nong len vi nhan nhiet" -> khi nhan CONG (A > 0);
#   sau do khi TOA nhiet ra than bom: Q cua khi < 0 (rut_ra[1]).
# Chua noi duoc (khong_chung_minh): nhiet do khi ben trong; ma sat gop bao nhieu.
# THU NGHI (so moi 37,0 °C chua hien; ca bom cham khong hien o cho nao trong clip):
#   "An nhanh 60 lan: than bom 37,0 °C. An cham 60 lan: cao hay thap hon 37,0 °C?"
#   Dap: THAP hon - an cham thi nhiet kip thoat ra (Q < 0 trong luc nen) nen dU = A + Q nho hon.
#   Goi y (tre ~4 s, cau hoi trung tinh): "Q còn ≈ 0 không?"
# Ban 2 (14/11/2026, cong B vong 1): bo y "nen manh nhat o day" (khi nen gan deu) -> "cuoi moi lan an khi don ve day";
#   nhan "màu: minh hoạ", so doc "thân bơm, ở đáy"; them dong Q ≈ 0; the Q < 0 hien ≥ 3,5 s; hop chot co hinh to hon.
from engine import *

NOTE = (70, 75, 95)
METAL = (205, 210, 222); METAL_D = (120, 126, 140)
SCREEN = (24, 30, 40); LCD = (134, 239, 172)
ROWS = ((0, "26,0"), (10, "27,5"), (20, "29,0"), (30, "31,0"), (45, "34,0"))
BX0, BX1, BTOP, BBOT = 300, 400, 430, 1050       # than ong bom
PY_UP, PY_DN = 470, 930                          # vi tri pit-tong

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def dashed(d, p1, p2, color, w=4, dash=16, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

random.seed(11)
MOL = [(random.random(), random.random(), random.uniform(0.6, 1.0) * random.choice((1, -1)),
        random.uniform(0.6, 1.0) * random.choice((1, -1))) for _ in range(14)]

def wall_col(y, heat):
    """Mau thanh ong: nong dan ve phia day (cho khi bi nen manh nhat)."""
    f = clamp((y - BTOP) / (BBOT - BTOP)) ** 1.6
    return mix(METAL, (239, 68, 68), clamp(heat * f))

def pump(d, t, py, heat, labels=False, tire=True, s_gas=0.0):
    # lop xe (non hoi) + ong dan tu van
    if tire:
        cx, cy = 880, 970
        d.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(60, 64, 76))
        d.ellipse([cx - 78, cy - 78, cx + 78, cy + 78], fill=BG)
        d.ellipse([cx - 66, cy - 66, cx + 66, cy + 66], outline=GRAY, width=6)
        d.line([(BX1, 1030), (560, 1030), (680, 1000), (765, 985)], fill=NAVY, width=9, joint="curve")
    # chan de
    d.rounded_rectangle([210, 1050, 520, 1090], radius=12, fill=METAL_D)
    # than ong: ve tung dai ngang de to mau theo do cao
    for y in range(BTOP, BBOT, 6):
        d.rectangle([BX0, y, BX1, y + 6], fill=wall_col(y + 3, heat))
    d.rectangle([BX0 + 12, py + 22, BX1 - 12, BBOT - 10], fill=(236, 242, 250))       # khi trong ong
    # phan tu khi duoi pit-tong (cang nen cang dong)
    y0g, y1g = py + 34, BBOT - 22
    for u0, v0, vu, vv in MOL:
        u = refl(u0 + vu * s_gas, 0, 1); v = refl(v0 + vv * s_gas, 0, 1)
        dot(d, BX0 + 26 + u * (BX1 - BX0 - 52), y0g + v * max(4, y1g - y0g), 8, BLUE)
    d.rectangle([BX0, BTOP, BX1, BBOT], outline=NAVY, width=5)
    # pit-tong + can + tay cam
    d.rectangle([BX0 + 6, py, BX1 - 6, py + 22], fill=NAVY)
    d.rectangle([BX0 + 44, py - 150, BX1 - 44, py], fill=METAL_D)
    d.rounded_rectangle([210, py - 180, 490, py - 142], radius=18, fill=NAVY)
    dot(d, BX1 + 8, 1030, 12, NAVY)                                                 # van
    if labels:
        for y, s in ((560, "phần trên"), (760, "giữa"), (970, "đáy,")):
            d.line([(BX0 - 14, y), (BX0 - 2, y)], fill=NOTE, width=4)
            text(d, (BX0 - 24, y), s, 44, NOTE, bold=False, anchor="rm")
        text(d, (BX0 - 24, 1015), "gần van", 44, NOTE, bold=False, anchor="rm")
    elif heat > 0:                                  # mau nong tren than ong chi la minh hoa
        text(d, (BX0 - 20, 900), "màu:", 44, NOTE, bold=False, anchor="rm")
        text(d, (BX0 - 20, 956), "minh hoạ", 44, NOTE, bold=False, anchor="rm")

def readout(d, n, temp, ff=False):
    card(d, (560, 290, 1030, 470), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (795, 330), "lần ấn", 44, NOTE, bold=False)
    text(d, (795, 415), str(n), 64, INK)
    card(d, (560, 500, 1030, 720), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (795, 540), "thân bơm, ở đáy", 44, NOTE, bold=False)
    card(d, (585, 580, 1005, 700), fill=SCREEN, r=14)
    text(d, (795, 640), temp + " °C", 58, LCD)
    dashed(d, (585, 690), (BX1 + 10, 990), A(RED, 0.8), w=4)                        # tia nhiet ke hong ngoai
    if ff:
        wdt = tw(d, "TUA NHANH", F(44)) + 96
        card(d, (795 - wdt / 2, 760, 795 + wdt / 2, 826), fill=ORANGE, r=33)
        text(d, (795 + 22, 793), "TUA NHANH", 44, WHITE)
        for j in range(2):
            tx = 795 - wdt / 2 + 22 + j * 16; d.polygon([(tx, 778), (tx, 808), (tx + 16, 793)], fill=WHITE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    pump(d, t, PY_UP, 0.0, labels=True, s_gas=t * 0.25)
    readout(d, 0, "26,0")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1130 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 44, WHITE, PURPLE, a)
    ctext(d, y0 + 205, "Bơm nhanh 45 lần.\nChỗ nào nóng nhất?", 54, PURPLE, maxw=920, alpha=a)
    text(d, (W / 2, y0 + 360), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 415, 940, y0 + 427], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 415, 140 + 800 * (1 - p), y0 + 427], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
P0, P1 = 0.6, 6.6                     # bom nhanh tu P0 toi P1 (giay trong canh)
MARKS = (1.8, 3.0, 4.2, 6.0)          # moc doc 10/20/30/45 lan
STROKE = 0.42                         # mot lan an (tua nhanh)

def k_at(t): return sum(1 for m in MARKS if t >= m)
def py_at(t):
    if t < P0 or t >= P1: return PY_UP
    ph = ((t - P0) / STROKE) % 1
    return lerp(PY_UP, PY_DN, ease(ph / 0.45)) if ph < 0.45 else lerp(PY_DN, PY_UP, ease((ph - 0.45) / 0.55))

def table(d, y0, ks):
    card(d, (40, y0, 1040, y0 + 230), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, y0 + 60), "Lần ấn", 44, NOTE, bold=False, anchor="lm")
    text(d, (70, y0 + 160), "t (°C)", 44, NOTE, bold=False, anchor="lm")
    d.line([(60, y0 + 110), (1020, y0 + 110)], fill=LIGHT, width=3)
    for j, (n, v) in enumerate(ROWS):
        x = 410 + j * 140
        if ks[j] > 0:
            text(d, (x, y0 + 60), str(n), 46, INK, alpha=ks[j])
            text(d, (x, y0 + 160), v, 46, ORANGE, alpha=ks[j])

def s_do(img, d, t, sc):
    k = k_at(t)
    heat = k / 4
    gs = t * (0.25 + 0.5 * heat)
    pump(d, t, py_at(t), heat, s_gas=gs)
    readout(d, ROWS[k][0], ROWS[k][1], ff=P0 <= t < P1)
    if P0 <= t < P1:
        arrow(d, (170, 470), (170, 620), RED, w=8, head=24)
        text(d, (170, 680), "ấn", 44, RED, anchor="mm")
    table(d, 1150, [1.0] + [appear(t, m, 0.3) for m in MARKS])
    text(d, (W / 2, 1450), "Coi rằng: ấn nhanh, Q ≈ 0", 46, INK)
    text(d, (W / 2, 1520), "Q: nhiệt khí nhận", 44, NOTE, bold=False)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    pump(d, t, PY_DN, 1.0, tire=False, s_gas=t * 0.9)
    ka = appear(t, M[0] + 0.1, 0.4)
    pw = tw(d, "ĐÁP ÁN · Đáy, gần van", F(44)) + 60
    card(d, (W / 2 - pw / 2, 1120, W / 2 + pw / 2, 1194), fill=A(NAVY, ka), r=37)
    text(d, (W / 2, 1157), "ĐÁP ÁN · Đáy, gần van", 44, WHITE, alpha=ka)
    if ka > 0:
        ring = (BX0 - 16, 900, BX1 + 30, 1066)
        d.rounded_rectangle(ring, radius=30, outline=A(RED, ka), width=6)
    k1 = appear(t, M[0] + 1.0, 0.4)
    card(d, (520, 300, 1040, 880), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
    if k1 > 0:
        text(d, (780, 355), "Cuối lần ấn, khí nóng", 44, INK, alpha=k1)
        text(d, (780, 415), "dồn về đáy", 44, BLUE, alpha=k1)
        text(d, (780, 475), "(còn 40 cm³)", 44, BLUE, alpha=k1)
        text(d, (780, 560), "ΔU = A + Q", 56, INK, alpha=k1)
        text(d, (550, 640), "Q ≈ 0", 46, ORANGE, anchor="lm", alpha=k1)
        text(d, (720, 640), "ấn nhanh", 44, NOTE, bold=False, anchor="lm", alpha=k1)
        k2 = appear(t, M[0] + 1.8, 0.4)
        text(d, (550, 705), "A > 0", 46, GREEN, anchor="lm", alpha=k2)
        text(d, (720, 705), "nhận công", 44, NOTE, bold=False, anchor="lm", alpha=k2)
        text(d, (550, 770), "→ ΔU > 0", 46, GREEN, anchor="lm", alpha=k2)
        text(d, (550, 832), "→ đáy nóng nhất", 44, GREEN, anchor="lm", alpha=k2)
    k3 = appear(t, M[1] + 0.1, 0.45)
    if k3 > 0:
        card(d, (40, 1240, 1040, 1590), fill=A(WHITE, k3), outline=A(ORANGE, k3), w=5)
        text(d, (W / 2, 1310), "Ma sát: dọc cả ống", 46, INK, alpha=k3)
        k4 = appear(t, M[1] + 1.4, 0.4)
        ctext(d, 1440, "→ không giải thích\nđáy nóng nhất", 46, ORANGE, maxw=900, alpha=k4)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    pump(d, t, PY_DN, 1.0, tire=False, s_gas=t * 0.9)
    mk = M[0] + 2.0
    kn = appear(t, M[1] - 0.15, 0.45)
    a1 = 1 - kn
    if a1 > 0:
        card(d, (520, 300, 1040, 820), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, 780, 360, "BẪY", 44, WHITE, RED, a1)
        ks = clamp((t - mk) / 0.4)
        f = F(46)
        for j, l in enumerate(("“Khí nóng lên", "vì nhận nhiệt”")):
            yy = 470 + 62 * j
            text(d, (780, yy), l, 46, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                lw = tw(d, l, f)
                d.line([(780 - lw / 2 - 6, yy + 2), (780 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        k2 = a1 * appear(t, mk + 0.2, 0.4)
        text(d, (780, 660), "Khí nhận công:", 44, INK, alpha=k2)
        text(d, (780, 725), "A > 0", 52, GREEN, alpha=k2)
        k3 = a1 * appear(t, mk + 0.9, 0.4)
        if k3 > 0:
            card(d, (40, 1130, 1040, 1420), fill=A(WHITE, k3), outline=A(RED, k3), w=5)
        text(d, (W / 2, 1210), "Rồi khí toả nhiệt ra thân bơm:", 46, INK, alpha=k3)
        text(d, (W / 2, 1320), "Q < 0", 60, RED, alpha=k3)
        if k3 > 0:                                  # nhiet tu khi ra thanh ong
            for yy in (960, 1010):
                arrow(d, (BX1 - 30, yy), (BX1 + 50, yy), A(RED, k3), w=6, head=18)
    if kn > 0:
        card(d, (40, 1120, 1040, 1590), fill=A(WHITE, kn), outline=A(NAVY, kn), w=6)
        text(d, (W / 2, 1195), "Chưa nói được", 50, NAVY, alpha=kn)
        for j, l in enumerate(("• Nhiệt độ khí bên trong", "• Ma sát góp bao nhiêu")):
            kk = kn * appear(t, M[1] + 0.2 + 0.5 * j, 0.35)
            text(d, (90, 1330 + 150 * j), l, 48, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    """Hai o so: an nhanh 60 lan -> 37,0 °C; an cham 60 lan -> ?"""
    if k <= 0: return
    for j, (lab, val, col) in enumerate((("nhanh · 60 lần", "37,0 °C", LCD), ("chậm · 60 lần", "? °C", YELLOW))):
        x0 = 90 + j * 470
        card(d, (x0, 980, x0 + 430, 1320), fill=A(WHITE, k), outline=A(NAVY, k), r=22, w=4)
        text(d, (x0 + 215, 1035), lab, 44, NOTE, bold=False, alpha=k)
        card(d, (x0 + 25, 1085, x0 + 405, 1300), fill=A(SCREEN, k), r=14)
        text(d, (x0 + 215, 1192), val, 66, col, alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Nén nhanh: A > 0, Q ≈ 0\nnên nội năng khí tăng",
             "Bơm chậm: cao hay thấp hơn 37,0 °C?", None, body=_end_body)
    kh = appear(t, M[0] + 4.5, 0.5)                 # goi y tre >= 4 s, chi la du kien thay doi
    if kh > 0:
        card(d, (110, 1350, 970, 1570), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1400), "Gợi ý", 44, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1495), "Q còn ≈ 0 không?", 48, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + P0, "tap")]
    out += [(do["t0"] + m, "tick") for m in MARKS]
    out += [(da["t0"] + da["M"][0] + 0.1, "ding"), (b["t0"] + b["M"][0], "buzz"), (b["t0"] + b["M"][1] - 0.15, "tap"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-noinang-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Nội năng · Định luật 1 NĐLH · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bơm xe bằng tay", draw=s_hook, tail=0.3, caps=[
   ("Bánh xe còn non hơi.", 2.8),
   ("Tự đoán trước.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Ấn nhanh, đo thân bơm.", 4.0),
   ("Nhiệt độ tăng dần.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Vì sao đáy nóng nhất?", 4.8),
   ("Còn ma sát?", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Nhận công hay nhận nhiệt?", 6.6),
   ("Chưa nói được?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.8)]),
])
