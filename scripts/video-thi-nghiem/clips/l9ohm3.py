# Clip: tn-l9-ohm-03 - Dien tro day dan theo chieu dai, tiet dien, vat lieu (KHTN 9, lo 6, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-ohm-03.json (so_lieu_mau, U = 1,5 V co_dinh):
#   (1) constantan 1 m 0,1 mm2 R 5 I 0,30 ; (2) constantan 2 m 0,1 R 10 I 0,15 ; (3) constantan 1 m 0,2 R 2,5 I 0,60 ;
#   (4) nichrome 1 m 0,1 R 11 I 0,14 (1,5/11 = 0,136 -> ghi "≈ 0,14", khong cho HS chia lai 1,5 : 0,14).
#   bay = hien_tuong_hay_sai[1] (dien tro chi phu thuoc vat lieu). KHONG dung bay [2] (quen doi mm2: dung nhieu C cua Cau 7).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[1] (nhiet do day coi nhu khong doi).
# Cau sau hop: Cau 3 (cat nua day 12 Ohm -> 6 Ohm), Cau 7 (constantan 4 m, 0,5 mm2, 12 V -> 3 A): clip khong dung cac so nay,
#   khong noi "dai mot nua", khong noi "gap doi day".
# Du doan (K10: chi cau hoi + hinh): day (1) 0,30 A ; thay day (3) cung dai, tiet dien 0,2 mm2 -> ampe ke chi khoang?
#   A. 0,15 A  B. 0,30 A  C. 0,60 A  D. 1,20 A  -> dap an C (khac ohm-01: cung U doi day bat ky ; ohm-02: doi U).
# Cau chot (ghi o kho ghi_chu): nichrome dai 1,5 m, 0,2 mm2, 1,5 V -> R = 8,25 Ohm, I ≈ 0,18 A
#   (hai buoc tu day (4): x1,5 chieu dai va :2 tiet dien ; khong ra bang mot phep tinh tu so tren man).
# Mach: nguon (+ ban dai trai) -> trai -> canh trai len -> ampe ke (+ trai) -> day dang do -> canh phai xuong -> K -> (-).
#   _kiem_dong_bo(): moi 0,05 s K mo <=> 0,00 A ; K dong <=> dung so cua day dang mac ; hang bang chi co sau khi da doc.
# Bo cuc (khac l9ohm1/l9ohm2): mach dai tren + ampe ke so, bang "bon day mau" ve dung ti le dai/day, bang 5 cot.
import copy, math
from engine import *

U0 = 1.5
ROWS = [("(1)", "constantan", 1.0, 0.1, 5.0, 0.30),
        ("(2)", "constantan", 2.0, 0.1, 10.0, 0.15),
        ("(3)", "constantan", 1.0, 0.2, 2.5, 0.60),
        ("(4)", "nichrome", 1.0, 0.1, 11.0, 0.14)]
APPROX = {3}   # hang so lam tron
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def ivn(j): return ("≈ " if j in APPROX else "") + vn(ROWS[j][5], 2)
def rvn(j):
    r = ROWS[j][4]; return vn(r, 1) if r != int(r) else f"{int(r)}"

WIRE = (60, 66, 92); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
CON = (176, 104, 40); NIC = (96, 100, 128)
SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
def wcol(j): return NIC if ROWS[j][1] == "nichrome" else CON
PX_M = 380   # 1 m tren bang day mau

# ---------------- mach dien (dai tren) ----------------
XL, XR, TY, BY = 110, 970, 360, 580
AX, S0, S1, BX, K0, K1 = 270, 470, 900, 420, 700, 790

def sample(d, x0, y, j, a=1.0, L=None, thick=None):
    L = PX_M * ROWS[j][2] if L is None else L
    th = (10 if ROWS[j][3] < 0.15 else 14) if thick is None else thick
    d.rounded_rectangle([x0, y - th / 2, x0 + L, y + th / 2], radius=th / 2, fill=A(wcol(j), a))
    dot(d, x0, y, th / 2 + 6, A(NAVY, a)); dot(d, x0 + L, y, th / 2 + 6, A(NAVY, a))

def circuit(d, j, closed, wa=1.0, reading="0,00 A"):
    card(d, (40, 270, 1040, 650), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(BX - 20, BY), (XL, BY), (XL, TY), (AX - 44, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(AX + 44, TY), (S0, TY)], fill=WIRE, width=w)
    d.line([(S1, TY), (XR, TY), (XR, BY), (K1, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(K0, BY), (BX + 20, BY)], fill=WIRE, width=w)
    # ampe ke noi tiep, + phia nguon +
    d.ellipse([AX - 44, TY - 44, AX + 44, TY + 44], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", 44, BLUE)
    text(d, (AX - 64, TY - 38), "+", 44, BLUE)
    card(d, (180, 420, 440, 520), fill=SCREEN, r=14)
    text(d, (310, 470), reading, 50, SCR_INK)
    # cho mac day
    dot(d, S0, TY, 9, WIRE); dot(d, S1, TY, 9, WIRE)
    if j is None or wa < 1:
        for x in range(S0 + 14, S1 - 14, 26): d.line([(x, TY), (x + 12, TY)], fill=GRAY, width=4)
    if j is not None and wa > 0:
        th = 10 if ROWS[j][3] < 0.15 else 14
        d.rounded_rectangle([S0 + 12, TY - th / 2, S1 - 12, TY + th / 2], radius=th / 2, fill=A(wcol(j), wa))
        text(d, ((S0 + S1) / 2, TY - 52), "dây " + ROWS[j][0], 42, mix(wcol(j), INK, 0.3), alpha=wa)
    # nguon 1,5 V: ban dai (+) trai, ban ngan (-) phai
    d.line([(BX - 20, BY - 50), (BX - 20, BY + 50)], fill=NAVY, width=6)
    d.line([(BX + 20, BY - 26), (BX + 20, BY + 26)], fill=NAVY, width=14)
    text(d, (BX - 54, BY - 44), "+", 44, ORANGE); text(d, (BX + 56, BY - 44), "−", 44, ORANGE)
    text(d, (BX + 150, BY - 46), "1,5 V", 42, INK)
    # khoa K tren day duoi
    dot(d, K0, BY, 9, WIRE); dot(d, K1, BY, 9, WIRE)
    if closed: d.line([(K0, BY), (K1, BY)], fill=NAVY, width=7)
    else: d.line([(K1, BY), (K0 + 12, BY - 56)], fill=NAVY, width=7)
    text(d, ((K0 + K1) / 2 + 10, BY + 46), "K", 42, NAVY)
    if closed:   # chieu dong: tu + qua canh trai di len
        arrow(d, (XL + 40, 545), (XL + 40, 455), RED, w=7, head=20)

def board(d, hl=None, a=1.0):
    card(d, (40, 680, 1040, 1090), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for j in range(4):
        y = 750 + j * 92
        if hl == j: d.rounded_rectangle([56, y - 40, 1024, y + 40], radius=20, fill=A((255, 237, 213), a))
        text(d, (95, y), ROWS[j][0], 42, mix(wcol(j), INK, 0.3), alpha=a)
        sample(d, 150, y, j, a)

XS = (95, 290, 525, 715, 920)
def table(d, n, hl=None, y=1120):
    card(d, (40, y, 1040, y + 455), fill=WHITE, outline=LIGHT, w=3)
    for x, h in zip(XS[1:], ("vật liệu", "dài (m)", "S (mm²)", "I (A)")): text(d, (x, y + 50), h, 42, INK)
    text(d, (XS[0], y + 50), "dây", 42, INK)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=3)
    for j, (nm, mat, L, S, R, I) in enumerate(ROWS):
        yy = y + 145 + j * 85
        if hl == j: d.rounded_rectangle([56, yy - 38, 1024, yy + 38], radius=20, fill=(255, 237, 213))
        if j < n:
            text(d, (XS[0], yy), nm, 44, mix(wcol(j), INK, 0.3)); text(d, (XS[1], yy), mat, 42, INK)
            text(d, (XS[2], yy), f"{int(L)}", 44, NAVY); text(d, (XS[3], yy), vn(S), 44, NAVY)
            text(d, (XS[4], yy), ivn(j), 44, BLUE)
        else:
            for x in XS: text(d, (x, yy), "·", 44, GRAY)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, 0, True, reading="0,30 A")
    board(d, hl=0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 680 + (1 - a) * 40
    card(d, (26, y0 - 12, 1054, y0 + 900), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 84), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 53), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for k, (j, lab) in enumerate(((0, "0,1 mm²"), (2, "0,2 mm²"))):
        y = y0 + 180 + k * 110
        text(d, (95, y), ROWS[j][0], 44, mix(CON, INK, 0.3), alpha=a)
        sample(d, 150, y, j, a)
    ctext(d, y0 + 520, "Dây (1): ampe kế chỉ 0,30 A.\nDây (3): cũng constantan, dài 1 m,\nnhưng tiết diện 0,2 mm².\n"
          "Ampe kế chỉ khoảng?", 46, INK, maxw=940, alpha=a)
    text(d, (W / 2, y0 + 740), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 830, 940, y0 + 842], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 830, 140 + 800 * (1 - p), y0 + 842], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (4 lan do) ----------------
T_FIRST, STEP = 0.5, 2.35
SWAP, CLOSE, ROW, OPEN = 0.5, 0.65, 1.15, 2.05   # moi lan, tinh tu dau lan do
NEEDLE = 0.35
def do_state(t):
    """-> (day dang mac, alpha, K dong?, so hang da ghi, so chi dang hien)."""
    k = int(clamp((t - T_FIRST) / STEP, 0, 3.999)) if t >= T_FIRST else 0
    tl = t - T_FIRST - k * STEP
    j = k
    if t < T_FIRST: return 0, 1.0, False, 0, "0,00 A"
    if tl < SWAP and k > 0:   # thay day: day cu mo di, day moi hien len
        h = SWAP / 2
        if tl < h: return k - 1, 1 - tl / h, False, k, "0,00 A"
        return k, (tl - h) / h, False, k, "0,00 A"
    closed = CLOSE <= tl < OPEN
    n = k + (1 if tl >= ROW else 0)
    if not closed: return j, 1.0, False, n, "0,00 A"
    p = (tl - CLOSE) / NEEDLE
    if p < 1: return j, 1.0, True, n, "…"
    return j, 1.0, True, n, ivn(j).replace("≈ ", "") + " A"

def s_do(img, d, t, sc):
    j, wa, closed, n, rd = do_state(t)
    circuit(d, j, closed, wa, rd)
    board(d, hl=j)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    if sc["T"] < T_FIRST + 4 * STEP: bad.append(("canh ngan hon 4 lan do", round(sc["T"], 2)))
    while t < sc["T"]:
        j, wa, closed, n, rd = do_state(t)
        if not closed and rd != "0,00 A": bad.append((round(t, 2), "K mo ma co so"))
        if closed and rd not in ("…", vn(ROWS[j][5], 2) + " A"): bad.append((round(t, 2), "so sai day", rd))
        if closed and wa < 1: bad.append((round(t, 2), "dong khi dang thay day"))
        if n > j + 1: bad.append((round(t, 2), "hang ghi truoc khi do", n, j))
        if n == j + 1 and rd == "…": bad.append((round(t, 2), "ghi hang khi chua doc xong"))
        t += 0.05
    for (nm, mat, L, S, R, I) in ROWS:
        rho = 0.5e-6 if mat == "constantan" else 1.1e-6
        if abs(rho * L / (S * 1e-6) - R) > 1e-6 or abs(U0 / R - I) > 0.005: bad.append(("so kho lech", nm))
    return bad

# ---------------- canh 3: Dap an (cot dong dien) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · khoảng 0,60 A"
    pw = tw(d, lab, F(44)) + 60
    card(d, (W / 2 - pw / 2, 280, W / 2 + pw / 2, 356), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 318), lab, 44, WHITE, alpha=ka)
    card(d, (40, 390, 1040, 880), fill=WHITE, outline=LIGHT, w=3)
    L = 640
    for j in range(4):
        yy = 465 + j * 115
        text(d, (95, yy), ROWS[j][0], 44, mix(wcol(j), INK, 0.3))
        g = ease((t - 0.5 - 0.25 * j) / 0.5); wb = L * ROWS[j][5] / 0.60 * g
        if wb > 2: d.rounded_rectangle([150, yy - 34, 150 + wb, yy + 34], radius=14, fill=wcol(j) if j != 2 else (37, 99, 235))
        if g > 0.95: text(d, (150 + L * ROWS[j][5] / 0.60 + 24, yy), ivn(j) + " A", 44, INK, anchor="lm")
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 > 0:
        card(d, (40, 920, 1040, 1170), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 995), "(3) so với (1): tiết diện gấp đôi", 44, DGREEN, alpha=k2)
        text(d, (W / 2, 1100), "0,60 A = 0,30 A × 2", 52, DGREEN, alpha=k2)

# ---------------- canh 4: Rut ra (R tung day) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 760), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    text(d, (W / 2, 320), "Điện trở R = U : I", 44, PURPLE, alpha=k0)
    for j in range(4):
        y = 420 + j * 95
        kr = appear(t, 0.5 + 0.3 * j, 0.4) * k0
        text(d, (95, y), ROWS[j][0], 42, mix(wcol(j), INK, 0.3), alpha=kr)
        sample(d, 150, y, j, kr, L=PX_M * 0.7 * ROWS[j][2])
        text(d, (1000, y), "R = " + rvn(j) + " Ω", 44, INK, anchor="rm", alpha=kr)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 800, 1040, 1250), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        rows = (("(2) dài gấp đôi:", "R gấp đôi"), ("(3) tiết diện gấp đôi:", "R còn nửa"),
                ("(4) nichrome:", "R lớn hơn"))
        for i, (l1, l2) in enumerate(rows):
            kk = k1 * appear(t, M[1] + 0.2 + 0.5 * i, 0.4)
            text(d, (80, 880 + i * 130), l1, 44, DGREEN, anchor="lm", alpha=kk)
            text(d, (120, 935 + i * 130), "→ " + l2, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 270, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    for cx, j in zip((210, 540, 870), (0, 1, 2)):
        text(d, (cx, 360), ROWS[j][0], 44, mix(CON, INK, 0.3))
        text(d, (cx, 460), "R = " + rvn(j) + " Ω", 46, INK)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 620), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "“Điện trở chỉ do vật liệu”"
        ks = clamp((t - M[0] - 1.4) / 0.4)
        lw = tw(d, q, F(52)); yy = y0 + 210
        text(d, (W / 2, yy), q, 52, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 36, yy), "✗", 52, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 1.9, 0.4)
        card(d, (70, y0 + 320, 1010, y0 + 580), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 400), "✓ Cùng constantan, R khác", 46, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 495), "còn tuỳ chiều dài, tiết diện", 46, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 90), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ", "• Dây nóng: coi R không đổi")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 220 + j * 130), l1, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
T_CHOT = 5.0
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1490), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(40)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
        ka = appear(t, M[0] + 0.4, 0.5)
        text(d, (W / 2, 790), "Dây (4): 1 m · 0,1 mm² · R = 11 Ω", 44, mix(NIC, INK, 0.3), alpha=ka)
        ctext(d, 930, "Cũng nichrome, dài 1,5 m, tiết diện 0,2 mm².\nVẫn 1,5 V. Ampe kế chỉ bao nhiêu?", 46, INK,
              maxw=940, alpha=ka)
        kw = appear(t, M[0] + 0.6, 0.5) * k1
        sample(d, 255, 1110, 3, kw, L=PX_M * 1.5, thick=14)
        kh = appear(t, M[0] + 2.9, 0.5)
        card(d, (110, 1220, 970, 1430), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1325, "Hai thứ cùng đổi", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 270, 1020, 570), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 420, "R tuỳ: dài, tiết diện, vật liệu", 52, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    cs += [(do["t0"] + T_FIRST + k * STEP + CLOSE, "tap") for k in range(4)]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
           (b["t0"] + b["M"][0] + 1.9, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l9-ohm-03", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bốn dây dẫn khác nhau", draw=s_hook, tail=0.8, caps=[
   ("Cùng nguồn, đổi dây.", 2.6),
   ("Nghĩ trước đã.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Đóng K, đọc số, ngắt ngay.", 2.9),
   ("Đổi chiều dài, rồi tiết diện.", 3.3),
   ("Cuối cùng: đổi sang nichrome.", 2.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Bốn dây, bốn số chỉ.", 2.8),
   ("So dây (3) với dây (1).", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Mỗi dây một điện trở.", 2.8),
   ("Mỗi lần đổi một thứ.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Có đúng không?", 4.0),
   ("Giới hạn của clip.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Tự trả lời trước khi xem.", 6.7)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch đồng bộ / số kho:", _kiem_dong_bo() or "không")
