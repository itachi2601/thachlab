# Clip: tn-l9-doanmach-01 - Do I va U trong doan mach noi tiep R1 = 10 Ohm, R2 = 20 Ohm (KHTN 9, lo 6, 18/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56 (ra >= 49 px), bo nhan vi tri o dong ho
#   (vi tri doc tren so do), khong nut A-D (K10), thanh dem 90 px, khoi chu cach >= 2,5 s, Bay = hai bieu do cot canh
#   nhau (U chia deu ✗ / U do ✓), bo o "Goi y" o man chot. Lan 2 (4,5 V) chi do von ke (ampe ke dung sau R2).
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-doanmach-01.json (_kiem_so()):
#   so_lieu_mau hang 1, 2 (U1, U2, U_AB, I): 1,0 2,0 3,0 0,10 ; 1,5 3,0 4,5 0,15. R1 = 10, R2 = 20 Ohm (tham_so).
#   KHONG dung hang 3 (2,0 + 4,0 vs 6,1): Cau 1 cua bai hoi ly do lech 0,1 V -> clip khong giai thich.
#   bay = hien_tuong_hay_sai[1] (U chia deu). chua noi duoc = mo_hinh.gia_thiet[0] (bo qua dien tro ampe ke).
# Du doan (K10): ampe ke truoc R1 chi 0,10 A, chuyen vao giua R1 va R2 -> so chi? -> van 0,10 A
#   (hien_tuong_hay_sai[0]). Khac Cau 4 cua bai (ba bong, 0,3 A, ampe ke sau bong thu ba).
# THU NGHI = cau_chot khung web (kho ghi_chu): doi nguon, von ke A-B chi 3,6 V -> von ke A-M? -> 1,2 V
#   (hai buoc: I = 3,6 : 30 = 0,12 A; U1 = 0,12 x 10). Man chot KHONG in 0,12 / 1,2.
# Mach: nguon (+ ban dai ben trai, day duoi) -> K -> canh trai len -> ampe ke -> A -> R1 -> M -> R2 -> B -> canh phai
#   xuong -> (-). Ampe ke chi doi cho khi K mo (an_toan). _kiem_dong_bo(): moi 0,05 s so chi <-> trang thai.
import copy, json, os
from engine import *

R1, R2 = 10.0, 20.0
ROWS = [dict(src=3.0, U1=1.0, U2=2.0, UAB=3.0, I=0.10),        # so_lieu_mau hang 1
        dict(src=4.5, U1=1.5, U2=3.0, UAB=4.5, I=0.15)]        # so_lieu_mau hang 2
UAB_C, U1_C = 3.6, 1.2
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")


def _kiem_so():
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-doanmach-01.json")))
    for r, h in zip(ROWS, k["so_lieu_mau"]["hang"]): assert [r["U1"], r["U2"], r["UAB"], r["I"]] == h, h
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}; assert (ts["R1"]["gia_tri"], ts["R2"]["gia_tri"]) == (R1, R2)
    for r in ROWS:
        assert abs(r["U1"] + r["U2"] - r["UAB"]) < 1e-9
        assert abs(r["U1"] / R1 - r["I"]) < 0.005 and abs(r["U2"] / R2 - r["I"]) < 0.005
    assert abs(UAB_C / (R1 + R2) * R1 - U1_C) < 1e-9
    g = k["so_lieu_mau"]["ghi_chu"]; assert "3,6 V" in g and "1,2 V" in g
_kiem_so()

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); RCOL = (180, 83, 9); DPURP = (76, 29, 149)
FS, FL = 56, 60

# ---------------- so do mach ----------------
TY, BY, XL, XR = 420, 740, 80, 1000
SLOT = (160, 545, 910)                  # ampe ke: truoc R1, giua R1 va R2, sau R2
NA, NM, NB = 240, 470, 830
R1X, R2X = (280, 420), (620, 780)
VY, VR, AR = 595, 44, 44
VCX = {"AM": 355, "MB": 650, "AB": 535}
VNODE = {"AM": (NA, NM), "MB": (NM, NB), "AB": (NA, NB)}
KX0, KX1, SX = 250, 340, 620


def resistor(d, x0, x1, y, name, val, a=1.0, lab=True):
    card(d, (x0, y - 36, x1, y + 36), fill=A(mix(WHITE, RCOL, 0.18), a), outline=A(RCOL, a), r=10, w=5)
    text(d, ((x0 + x1) / 2, y + 2), name, FS, mix(RCOL, INK, 0.35), alpha=a)
    if lab: text(d, ((x0 + x1) / 2, y - 78), f"{val:.0f} Ω", FS, mix(RCOL, INK, 0.3), alpha=a)


def ammeter(d, x, y, a=1.0):
    d.ellipse([x - AR, y - AR, x + AR, y + AR], fill=A(WHITE, a), outline=A(BLUE, a), width=6)
    text(d, (x, y + 2), "A", FS, BLUE, alpha=a)


def circuit(d, st):
    card(d, (40, 262, 1040, 845), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    seat = int(round(st["pos"])) if st["seated"] else None
    xs = [XL]
    for k, sx in enumerate(SLOT):
        if seat == k: xs += [sx - AR, sx + AR]
    xs.append(XR)
    for j in range(0, len(xs), 2): d.line([(xs[j], TY), (xs[j + 1], TY)], fill=WIRE, width=w)
    d.line([(XL, TY), (XL, BY), (KX0, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(KX1, BY), (SX - 20, BY)], fill=WIRE, width=w)
    d.line([(SX + 20, BY), (XR, BY), (XR, TY)], fill=WIRE, width=w, joint="curve")
    resistor(d, *R1X, TY, "R1", R1); resistor(d, *R2X, TY, "R2", R2)
    for x, nm in ((NA, "A"), (NM, "M"), (NB, "B")):
        dot(d, x, TY, 9, WIRE); text(d, (x + 30, TY + 66), nm, FS, INK)
    if seat is not None: ammeter(d, SLOT[seat], TY)
    else:
        p = st["pos"]; k = min(1, int(p)); f = p - k
        x = lerp(SLOT[k], SLOT[min(2, k + 1)], f) if p < 2 else SLOT[2]
        ammeter(d, x, TY - 100)
    vp = st["vpair"]
    if vp:
        cx = VCX[vp]; x1, x2 = VNODE[vp]
        d.line([(cx - VR, VY), (x1, VY), (x1, TY)], fill=PURPLE, width=5, joint="curve")
        d.line([(cx + VR, VY), (x2, VY), (x2, TY)], fill=PURPLE, width=5, joint="curve")
        d.ellipse([cx - VR, VY - VR, cx + VR, VY + VR], fill=WHITE, outline=PURPLE, width=6)
        text(d, (cx, VY + 2), "V", FS, PURPLE)
    dot(d, KX0, BY, 9, WIRE); dot(d, KX1, BY, 9, WIRE)
    if st["closed"]: d.line([(KX0, BY), (KX1, BY)], fill=NAVY, width=7)
    else: d.line([(KX0, BY), (KX1 - 12, BY - 50)], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, BY + 58), "K", FS, NAVY)
    d.line([(SX - 20, BY - 50), (SX - 20, BY + 50)], fill=NAVY, width=6)
    d.line([(SX + 20, BY - 26), (SX + 20, BY + 26)], fill=NAVY, width=14)
    text(d, (SX - 58, BY - 46), "+", FS, ORANGE)
    text(d, (SX + 215, BY + 58), f"nguồn {vn(st['src']).replace(',0', '')} V", FS, INK)
    if st["closed"]:
        arrow(d, (XL, 660), (XL, 520), RED, w=7, head=20)
        arrow(d, (XR, 520), (XR, 660), RED, w=7, head=20)


def meters(d, st):
    i, u = readings(st)
    card(d, (40, 862, 530, 1050), fill=BODY, r=22)
    ammeter(d, 285, 905)
    card(d, (80, 945, 490, 1035), fill=SCREEN, r=12)
    text(d, (285, 990), "…" if i is None else vn(i, 2) + " A", 60, SCR_INK)
    card(d, (550, 862, 1040, 1050), fill=BODY, r=22)
    d.ellipse([795 - VR, 905 - VR, 795 + VR, 905 + VR], fill=WHITE, outline=PURPLE, width=6); text(d, (795, 907), "V", FS, PURPLE)
    card(d, (590, 945, 1000, 1035), fill=SCREEN, r=12)
    text(d, (795, 990), "–" if u is None else vn(u) + " V", 60, SCR_INK)


TCX = (250, 590, 760, 930)
def table(d, cells, y=1075, hl=None):
    card(d, (40, y, 1040, y + 400), fill=WHITE, outline=LIGHT, w=3)
    text(d, (TCX[0], y + 50), "ampe kế (A)", FS, BLUE)
    text(d, (760, y + 50), "vôn kế (V)", FS, PURPLE)
    for x, h in zip(TCX[1:], ("A–M", "M–B", "A–B")): text(d, (x, y + 120), h, FS, INK)
    d.line([(70, y + 165), (1010, y + 165)], fill=LIGHT, width=3)
    d.line([(470, y + 20), (470, y + 380)], fill=LIGHT, width=3)
    for r, row in enumerate(ROWS):
        yy = y + 235 + r * 100
        if hl == r: d.rounded_rectangle([56, yy - 44, 1024, yy + 44], radius=20, fill=(255, 237, 213))
        for k in range(3):
            x = TCX[0] - 135 + k * 135
            if (r, "I%d" % k) in cells: text(d, (x, yy), vn(row["I"], 2), FS, BLUE)
            else: text(d, (x, yy), "·", FS, GRAY)
        for x, key, col in zip(TCX[1:], ("AM", "MB", "AB"), ("U1", "U2", "UAB")):
            if (r, key) in cells: text(d, (x, yy), vn(row[col]), FS, NAVY)
            else: text(d, (x, yy), "·", FS, GRAY)


# ---------------- dong thoi gian canh Tien hanh ----------------
MOVE = 0.4
EVT = [(0.6, "close", None), (1.4, "open", None), (1.5, "move", 1), (2.1, "close", None), (2.9, "open", None),
       (3.0, "move", 2), (3.5, "close", None), (4.4, "v", "AM"), (5.5, "v", "MB"), (6.6, "v", "AB"),
       (7.7, "open", None), (7.9, "src", 1), (8.2, "close", None), (9.2, "v", "AM"), (10.2, "v", "MB")]
T_CELL = 0.35
N_CELLS = 10


def do_state_raw(t, evt=EVT):
    st = dict(pos=0.0, seated=True, closed=False, row=0, vpair=None)
    for te, kind, arg in evt:
        if t < te: break
        if kind == "close": st["closed"] = True
        elif kind == "open": st["closed"] = False
        elif kind == "src": st["row"] = arg
        elif kind == "v": st["vpair"] = arg
        elif kind == "move":
            p0 = st["pos"]; f = clamp((t - te) / MOVE)
            st["pos"] = lerp(p0, float(arg), ease(f)); st["seated"] = f >= 1
            if f >= 1: st["pos"] = float(arg)
    st["src"] = ROWS[st["row"]]["src"]
    return st


def do_state(t, evt=EVT):
    st = do_state_raw(t, evt); cells = set()
    for te, kind, arg in evt:
        if t < te + T_CELL: continue
        s2 = do_state_raw(te + 0.001, evt)
        if kind == "close" and s2["seated"]:
            cells.add((s2["row"], "I%d" % int(round(s2["pos"]))))
            if s2["vpair"]: cells.add((s2["row"], s2["vpair"]))
        if kind == "v" and s2["closed"]: cells.add((s2["row"], arg))
    st["cells"] = cells
    return st


def readings(st):
    row = ROWS[st["row"]]
    i = None if not st["seated"] else (row["I"] if st["closed"] else 0.0)
    if st["vpair"] is None: u = None
    else: u = {"AM": row["U1"], "MB": row["U2"], "AB": row["UAB"]}[st["vpair"]] if st["closed"] else 0.0
    return i, u


def s_do(img, d, t, sc):
    st = do_state(t)
    circuit(d, st); meters(d, st)
    table(d, st["cells"], hl=st["row"] if st["cells"] else None)


def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        st = do_state(t); i, u = readings(st); row = ROWS[st["row"]]
        if st["closed"] and not st["seated"]: bad.append((round(t, 2), "doi cho ampe ke khi K dong"))
        if not st["closed"] and i not in (None, 0.0): bad.append((round(t, 2), "K mo ma ampe co so"))
        if st["closed"] and st["seated"] and i != row["I"]: bad.append((round(t, 2), "ampe sai so"))
        if st["vpair"] and not st["closed"] and u != 0.0: bad.append((round(t, 2), "K mo ma von co so"))
        for (r, key) in st["cells"]:
            if r > st["row"]: bad.append((round(t, 2), "o bang lan sau truoc khi do", key))
        t += 0.05
    end = do_state(sc["T"] - 0.01)["cells"]
    if len(end) != N_CELLS: bad.append(("cuoi canh", "bang thieu o", sorted(end)))
    return bad


# ---------------- canh 1: Du doan ----------------
HOOK_ST = dict(pos=0.0, seated=True, closed=True, row=0, vpair=None, src=3.0)
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, HOOK_ST); meters(d, HOOK_ST)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 870 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 690), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 106), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 66), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    text(d, (W / 2, y0 + 200), "Ampe kế trước R1: 0,10 A.", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "Chuyển vào giữa R1 và R2.", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 370), "Ampe kế chỉ thế nào?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 500, 970, y0 + 590], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 500, 110 + max(90, 860 * (1 - p)), y0 + 590], radius=45, fill=A(DPURP, a))


# ---------------- canh 3: Dap an ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: vẫn 0,10 A", 310, appear(t, 0.15, 0.4))
    kb = appear(t, 0.4, 0.4)
    card(d, (40, 390, 1040, 900), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
    text(d, (W / 2, 440), "nguồn 3 V", FS, INK, alpha=appear(t, 0.15, 0.4))
    y = 600
    d.line([(80, y), (1000, y)], fill=A(WIRE, kb), width=6)
    resistor(d, *R1X, y, "R1", R1, a=kb); resistor(d, *R2X, y, "R2", R2, a=kb)
    for k, sx in enumerate(SLOT):
        ak = appear(t, 0.7 + 0.35 * k, 0.35) * kb
        if ak <= 0: continue
        card(d, (sx - AR - 6, y - AR - 6, sx + AR + 6, y + AR + 6), fill=A(WHITE, ak), r=AR + 6)
        ammeter(d, sx, y, a=ak)
        text(d, (sx if k else sx + 40, 790), vn(ROWS[0]["I"], 2), FL, BLUE, alpha=ak)
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 > 0:
        card(d, (40, 950, 1040, 1100), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1025), "ba chỗ: cùng một số", 64, DGREEN, alpha=k2)


# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 430), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=5)
    text(d, (W / 2, 350), "Nối tiếp: I như nhau", 64, DGREEN, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 <= 0: return
    card(d, (40, 470, 1040, 1080), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    for x, h in zip((250, 500, 760), ("A–M", "M–B", "A–B")): text(d, (x, 545), h, FS, INK, alpha=k1)
    d.line([(80, 595), (1000, 595)], fill=A(LIGHT, k1), width=3)
    for r, row in enumerate(ROWS):
        yy = 670 + r * 110
        text(d, (250, yy), vn(row["U1"]), FL, NAVY, alpha=k1)
        text(d, (375, yy), "+", FL, MUTED, alpha=k1)
        text(d, (500, yy), vn(row["U2"]), FL, NAVY, alpha=k1)
        text(d, (630, yy), "=", FL, MUTED, alpha=k1)
        text(d, (760, yy), vn(row["UAB"]), FL, NAVY, alpha=k1)
        text(d, (900, yy), "V", FS, MUTED, alpha=k1)
    d.rounded_rectangle([70, 910, 1010, 1050], radius=24, fill=A((236, 253, 243), k1))
    text(d, (W / 2, 980), "U = U1 + U2", 64, DGREEN, alpha=k1)


# ---------------- canh 5: Bay (hai bieu do cot canh nhau) roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def bars(d, x0, vals, col, k, ka):
    base = 1060
    d.line([(x0 + 40, base), (x0 + 430, base)], fill=A(INK, ka), width=4)
    for j, (nm, v) in enumerate(vals):
        cx = x0 + 145 + 190 * j; h = 300 * v / 2.0 * k
        if h > 0: d.rectangle([cx - 55, base - h, cx + 55, base], fill=A(col, ka))
        text(d, (cx, base - 300 * v / 2.0 - 42), vn(v), FL, mix(col, INK, 0.3), alpha=ka * k)
        text(d, (cx, base + 50), nm, FL, mix(RCOL, INK, 0.3), alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“U chia đều hai điện trở”", FL, INK, alpha=a1)
    card(d, (40, 470, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    text(d, (285, 540), "U (V) nghĩ", FL, DRED, alpha=a1)
    bars(d, 50, (("R1", 1.5), ("R2", 1.5)), DRED, appear(t, 0.6, 1.0), a1)
    text(d, (285, 1195), "✗ chia đều", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (795, 540), "U (V) đo", FL, DGREEN, alpha=a2)
        bars(d, 560, (("R1", ROWS[0]["U1"]), ("R2", ROWS[0]["U2"])), DGREEN, appear(t, BAY_R, 0.9), a2)
        text(d, (795, 1195), "✓ R lớn, U lớn", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "bỏ qua điện trở ampe kế", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "I như nhau, U cộng lại", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "Đổi nguồn, giữ R1, R2.", FL, INK, alpha=k1)
    text(d, (W / 2, 735), "Vôn kế A–M chỉ?", FL, INK, alpha=k1)
    y = 960
    d.line([(110, y), (970, y)], fill=A(WIRE, k1), width=6)
    resistor(d, 190, 410, y, "R1", R1, a=k1, lab=False); resistor(d, 620, 840, y, "R2", R2, a=k1, lab=False)
    text(d, (300, y - 75), "10 Ω", FL, RCOL, alpha=k1); text(d, (730, y - 75), "20 Ω", FL, RCOL, alpha=k1)
    for x, nm in ((150, "A"), (515, "M"), (920, "B")):
        dot(d, x, y, 9, A(WIRE, k1)); text(d, (x, y + 60), nm, FS, INK, alpha=k1)
    card(d, (110, 1110, 970, 1220), fill=A(SCREEN, k1), r=20)
    text(d, (540, 1165), "A–B: 3,6 V", 64, SCR_INK, alpha=k1)
    card(d, (110, 1260, 970, 1370), fill=A(SCREEN, k1), r=20)
    text(d, (540, 1315), "A–M: ? V", 64, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    cs += [(do["t0"] + te, "tap") for te, kind, _ in EVT if kind == "close"]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
           (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return cs


CLIP = dict(id="tn-l9-doanmach-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Mạch nối tiếp · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai điện trở nối tiếp", draw=s_hook, tail=0.3, caps=[
   ("Mạch nối tiếp, nguồn 3 V.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Mở K, đổi chỗ ampe kế.", 3.4),
   ("Vôn kế đo từng đoạn.", 3.6),
   ("Lần 2: nguồn 4,5 V.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Ba chỗ: cùng 0,10 A.", 2.9),
   ("Không bị dùng bớt.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Dòng điện như nhau.", 3.0),
   ("U cả đoạn bằng tổng.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Có chia đều không?", 3.0),
   ("R lớn nhận U lớn.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.1)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
