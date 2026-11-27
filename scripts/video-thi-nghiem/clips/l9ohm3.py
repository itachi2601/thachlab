# Clip: tn-l9-ohm-03 - Dien tro day dan theo chieu dai, tiet dien, vat lieu (KHTN 9, lo 6, 18/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56 (ra >= 49 px), bang + day mau gop mot
#   (day ve dai theo l, day theo S, mau theo vat lieu), khong nut A-D (K10), thanh dem 90 px, khoi chu cach >= 2,5 s,
#   Bay = hai bieu do cot canh nhau (gia thiet "chi do vat lieu" ✗ / R do that ✓), bo o "Goi y" o man chot.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-ohm-03.json (so_lieu_mau, U = 1,5 V co_dinh; _kiem_so()):
#   (1) constantan 1 m 0,1 mm2 R 5 I 0,30 ; (2) constantan 2 m 0,1 R 10 I 0,15 ; (3) constantan 1 m 0,2 R 2,5 I 0,60 ;
#   (4) nichrome 1 m 0,1 R 11 I 0,14 (1,5/11 = 0,136 -> ghi "≈ 0,14").
#   bay = hien_tuong_hay_sai[1] (dien tro chi phu thuoc vat lieu). KHONG dung bay [2] (quen doi mm2: dap an C cua Cau 7).
#   chua noi duoc = mo_hinh.gia_thiet[1] (nhiet do day coi nhu khong doi).
# Cau trong bai: Cau 3 (cat nua day 12 Ohm -> 6 Ohm), Cau 7 (constantan 4 m, 0,5 mm2, 12 V -> 3 A), ⭐⭐ (gap doi 12 Ohm -> 3 Ohm):
#   clip khong dung cac so nay, khong noi "dai mot nua", khong noi "gap doi day".
# Du doan (K10): day (1) 0,30 A ; day (3) cung chat, cung dai, tiet dien 0,2 mm2 -> ampe ke chi khoang? -> 0,60 A.
# THU NGHI = cau_chot khung web (ghi o kho ghi_chu): nichrome dai 1,5 m, 0,2 mm2, 1,5 V -> R = 8,25 Ohm, I ≈ 0,18 A
#   (hai buoc tu day (4): x1,5 chieu dai va :2 tiet dien). Man chot KHONG in 8,25 / 0,18.
import copy, math
from engine import *

U0 = 1.5
ROWS = [("(1)", "constantan", 1.0, 0.1, 5.0, 0.30),
        ("(2)", "constantan", 2.0, 0.1, 10.0, 0.15),
        ("(3)", "constantan", 1.0, 0.2, 2.5, 0.60),
        ("(4)", "nichrome", 1.0, 0.1, 11.0, 0.14)]
APPROX = {3}   # hang so lam tron
C_L, C_S, C_R, C_I = 1.5, 0.2, 8.25, 0.18     # cau chot (kho ghi_chu)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def ivn(j): return ("≈ " if j in APPROX else "") + vn(ROWS[j][5], 2)
def rvn(j):
    r = ROWS[j][4]; return vn(r, 1) if r != int(r) else f"{int(r)}"


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-ohm-03.json")))
    hang = k["so_lieu_mau"]["hang"]
    for (nm, mat, L, S, R, I), h in zip(ROWS, hang): assert [mat, L, S, R, I] == h, (nm, h)
    rho = {o["ten"]: o["rho"] for o in k["tham_so"][2]["lua_chon"]}
    for (nm, mat, L, S, R, I) in ROWS:
        assert abs(rho[mat] * L / (S * 1e-6) - R) < 1e-9 and abs(U0 / R - I) < 0.005
    assert abs(rho["nichrome"] * C_L / (C_S * 1e-6) - C_R) < 1e-9 and round(U0 / C_R, 2) == C_I
    g = k["so_lieu_mau"]["ghi_chu"]; assert "1,5 m" in g and "0,2 mm²" in g and "0,18 A" in g
_kiem_so()

WIRE = (60, 66, 92); DGREEN = (21, 110, 55); DRED = (185, 28, 28); DPURP = (76, 29, 149)
CON = (176, 104, 40); NIC = (96, 100, 128)
SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
FS, FL = 56, 60
def wcol(j): return NIC if ROWS[j][1] == "nichrome" else CON
PX_M = 110   # 1 m tren bang day mau
def th_of(S): return 12 if S < 0.15 else 26


def sample(d, x0, y, L_m, S, col, a=1.0, px=PX_M):
    L = px * L_m; th = th_of(S)
    d.rounded_rectangle([x0, y - th / 2, x0 + L, y + th / 2], radius=th / 2, fill=A(col, a))
    dot(d, x0, y, th / 2 + 6, A(NAVY, a)); dot(d, x0 + L, y, th / 2 + 6, A(NAVY, a))


# ---------------- mach dien (dai tren) ----------------
XL, XR, TY, BY = 110, 970, 360, 550
AX, S0, S1, BX, K0, K1 = 270, 470, 900, 470, 710, 800


def circuit(d, j, closed, wa=1.0, reading="0,00 A"):
    card(d, (40, 262, 1040, 610), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(BX - 20, BY), (XL, BY), (XL, TY), (AX - 48, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(AX + 48, TY), (S0, TY)], fill=WIRE, width=w)
    d.line([(S1, TY), (XR, TY), (XR, BY), (K1, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(K0, BY), (BX + 20, BY)], fill=WIRE, width=w)
    d.ellipse([AX - 48, TY - 48, AX + 48, TY + 48], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", FS, BLUE)
    card(d, (150, 425, 400, 515), fill=SCREEN, r=14)
    text(d, (275, 470), reading, 58, SCR_INK)
    dot(d, S0, TY, 9, WIRE); dot(d, S1, TY, 9, WIRE)
    if j is None or wa < 1:
        for x in range(S0 + 14, S1 - 14, 26): d.line([(x, TY), (x + 12, TY)], fill=GRAY, width=4)
    if j is not None and wa > 0:
        th = th_of(ROWS[j][3])
        d.rounded_rectangle([S0 + 12, TY - th / 2, S1 - 12, TY + th / 2], radius=th / 2, fill=A(wcol(j), wa))
        text(d, ((S0 + S1) / 2, TY - 60), "dây " + ROWS[j][0], FS, mix(wcol(j), INK, 0.3), alpha=wa)
    d.line([(BX - 20, BY - 46), (BX - 20, BY + 46)], fill=NAVY, width=6)
    d.line([(BX + 20, BY - 24), (BX + 20, BY + 24)], fill=NAVY, width=14)
    text(d, (BX - 60, BY - 6), "+", FS, ORANGE)
    text(d, (BX + 125, BY - 46), "1,5 V", FS, INK)
    dot(d, K0, BY, 9, WIRE); dot(d, K1, BY, 9, WIRE)
    if closed: d.line([(K0, BY), (K1, BY)], fill=NAVY, width=7)
    else: d.line([(K1, BY), (K0 + 12, BY - 50)], fill=NAVY, width=7)
    text(d, (K1 + 55, BY - 38), "K", FS, NAVY)
    if closed: arrow(d, (XL + 0, 520), (XL + 0, 420), RED, w=7, head=20)


# ---------------- bang day mau (gop bang so lieu) ----------------
CX = (90, 0, 470, 705, 915)   # (j) | day mau (x 160..380) | dai | S | I
def board(d, n, hl=None, y=635, a=1.0):
    card(d, (40, y, 1040, y + 560), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for x, h in ((CX[2], "dài (m)"), (CX[3], "S (mm²)"), (CX[4], "I (A)")): text(d, (x, y + 55), h, FS, INK, alpha=a)
    d.line([(70, y + 100), (1010, y + 100)], fill=A(LIGHT, a), width=3)
    for j, (nm, mat, L, S, R, I) in enumerate(ROWS):
        yy = y + 155 + j * 92
        if hl == j: d.rounded_rectangle([56, yy - 42, 1024, yy + 42], radius=20, fill=A((255, 237, 213), a))
        text(d, (CX[0], yy), nm, FL, mix(wcol(j), INK, 0.3), alpha=a)
        sample(d, 165, yy, L, S, wcol(j), a)
        text(d, (CX[2], yy), f"{int(L)}", FL, NAVY, alpha=a); text(d, (CX[3], yy), vn(S), FL, NAVY, alpha=a)
        text(d, (CX[4], yy), ivn(j) if j < n else "…", FL, BLUE if j < n else MUTED, alpha=a)
    # chu giai mau = vat lieu
    yl = y + 515
    for x0, col, s in ((80, CON, "constantan"), (560, NIC, "nichrome")):
        d.rounded_rectangle([x0, yl - 12, x0 + 80, yl + 12], radius=12, fill=A(col, a))
        text(d, (x0 + 100, yl), s, FS, mix(col, INK, 0.3), anchor="lm", alpha=a)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    on = t >= 0.6
    circuit(d, 0, on, reading="0,30 A" if t >= 0.95 else ("…" if on else "0,00 A"))
    board(d, 1 if t >= 0.95 else 0, hl=0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 635 + (1 - a) * 40
    card(d, (26, y0 - 10, 1054, y0 + 950), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    for k, (j, rd) in enumerate(((0, "0,30 A"), (2, "? A"))):
        y = y0 + 190 + k * 110
        text(d, (150, y), ROWS[j][0], FL, mix(CON, INK, 0.3), alpha=a)
        sample(d, 230, y, 1.0, ROWS[j][3], CON, a, px=330)
        text(d, (790, y), rd, FL, BLUE if rd[0] != "?" else DPURP, alpha=a)
    text(d, (W / 2, y0 + 440), "(3): cùng chất, cùng dài,", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 525), "tiết diện 0,2 mm².", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 610), "Ampe kế chỉ khoảng?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 730, 970, y0 + 820], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 730, 110 + max(90, 860 * (1 - p)), y0 + 820], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh (4 lan do) ----------------
T_FIRST, STEP = 0.5, 2.3
SWAP, CLOSE, ROW, OPEN = 0.5, 0.65, 1.15, 2.0   # moi lan, tinh tu dau lan do
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
    board(d, n, hl=j)


def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    if sc["T"] < T_FIRST + 3 * STEP + OPEN: bad.append(("canh ngan hon 4 lan do", round(sc["T"], 2)))
    while t < sc["T"]:
        j, wa, closed, n, rd = do_state(t)
        if not closed and rd != "0,00 A": bad.append((round(t, 2), "K mo ma co so"))
        if closed and rd not in ("…", vn(ROWS[j][5], 2) + " A"): bad.append((round(t, 2), "so sai day", rd))
        if closed and wa < 1: bad.append((round(t, 2), "dong khi dang thay day"))
        if n > j + 1: bad.append((round(t, 2), "hang ghi truoc khi do", n, j))
        if n == j + 1 and rd == "…": bad.append((round(t, 2), "ghi hang khi chua doc xong"))
        t += 0.05
    return bad


# ---------------- canh 3: Dap an (cot dong dien) ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: khoảng 0,60 A", 310, ka)
    card(d, (40, 390, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    L = 560
    for j in range(4):
        yy = 480 + j * 125
        text(d, (95, yy), ROWS[j][0], FL, mix(wcol(j), INK, 0.3))
        g = ease((t - 0.5 - 0.3 * j) / 0.5); wb = L * ROWS[j][5] / 0.60 * g
        hi = j in (0, 2) and t >= M[1] - 0.1
        if wb > 2: d.rounded_rectangle([160, yy - 38, 160 + wb, yy + 38], radius=14, fill=wcol(j) if not hi else BLUE)
        if g > 0.95: text(d, (160 + L * ROWS[j][5] / 0.60 + 24, yy), ivn(j) + " A", FL, INK, anchor="lm")
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 > 0:
        card(d, (40, 1010, 1040, 1150), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1080), "(3): 0,60 = 0,30 × 2", 64, DGREEN, alpha=k2)


# ---------------- canh 4: Rut ra (R tung day) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 262, 1040, 790), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    text(d, (W / 2, 325), "R = 1,5 V : I", FL, PURPLE, alpha=k0)
    for j in range(4):
        y = 440 + j * 100
        text(d, (95, y), ROWS[j][0], FL, mix(wcol(j), INK, 0.3), alpha=k0)
        sample(d, 165, y, ROWS[j][2], ROWS[j][3], wcol(j), k0)
        text(d, (990, y), "R = " + rvn(j) + " Ω", FL, INK, anchor="rm", alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 830, 1040, 1250), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        for i, s in enumerate(("(2): dài × 2 → R × 2", "(3): S × 2 → R : 2", "(4): nichrome → R lớn hơn")):
            text(d, (W / 2, 910 + i * 125), s, FL, DGREEN, alpha=k1)


# ---------------- canh 5: Bay (hai bieu do cot canh nhau) roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def bars(d, x0, vals, col, k, ka):
    base = 1060
    d.line([(x0 + 20, base), (x0 + 450, base)], fill=A(INK, ka), width=4)
    for j, (nm, v) in enumerate(vals):
        cx = x0 + 95 + 140 * j; h = 300 * v / 10 * k
        if h > 0: d.rectangle([cx - 45, base - h, cx + 45, base], fill=A(col, ka))
        text(d, (cx, base - 300 * v / 10 - 42), vn(v, 1).replace(",0", ""), FL, mix(col, INK, 0.3), alpha=ka * k)
        text(d, (cx, base + 50), nm, FL, mix(CON, INK, 0.3), alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“R chỉ do vật liệu”", FL, INK, alpha=a1)
    card(d, (40, 470, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    text(d, (285, 540), "R (Ω) nghĩ", FL, DRED, alpha=a1)
    bars(d, 50, (("(1)", 5.0), ("(2)", 5.0), ("(3)", 5.0)), DRED, appear(t, 0.6, 1.0), a1)
    text(d, (285, 1195), "✗ R như nhau", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (795, 540), "R (Ω) tính", FL, DGREEN, alpha=a2)
        bars(d, 560, tuple((ROWS[j][0], ROWS[j][4]) for j in range(3)), DGREEN, appear(t, BAY_R, 0.9), a2)
        text(d, (795, 1195), "✓ R khác nhau", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "coi nhiệt độ dây không đổi", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "R tuỳ dài, tiết diện, vật liệu", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "Nichrome dài 1,5 m, S = 0,2 mm².", FL, INK, alpha=k1)
    text(d, (W / 2, 735), "Vẫn 1,5 V: ampe kế chỉ?", FL, INK, alpha=k1)
    # day moc (4) va day moi, ve cung ti le
    text(d, (70, 890), "(4)", FL, mix(NIC, INK, 0.3), anchor="lm", alpha=k1)
    sample(d, 235, 890, 1.0, 0.1, NIC, k1, px=380)
    text(d, (870, 890), "11 Ω", FL, INK, alpha=k1)
    text(d, (70, 1050), "mới", FL, mix(NIC, INK, 0.3), anchor="lm", alpha=k1)
    sample(d, 235, 1050, 1.5, 0.2, NIC, k1, px=380)
    card(d, (240, 1180, 840, 1320), fill=A(SCREEN, k1), r=20)
    text(d, (540, 1250), "? A", 72, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    cs += [(do["t0"] + T_FIRST + k * STEP + CLOSE, "tap") for k in range(4)]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
           (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return cs


CLIP = dict(id="tn-l9-ohm-03", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bốn dây dẫn khác nhau", draw=s_hook, tail=0.3, caps=[
   ("Cùng nguồn 1,5 V, đổi dây.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.2, caps=[
   ("Đóng K, đọc số, ngắt ngay.", 3.1),
   ("Đổi chiều dài, rồi tiết diện.", 3.3),
   ("Cuối cùng: đổi sang nichrome.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Bốn dây, bốn số chỉ.", 2.9),
   ("So dây (3) với dây (1).", 2.9)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Mỗi dây một điện trở.", 3.0),
   ("Mỗi lần chỉ đổi một thứ.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("So ba dây constantan.", 3.0),
   ("R khác nhau.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.2)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
