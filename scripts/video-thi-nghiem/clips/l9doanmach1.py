# Clip: tn-l9-doanmach-01 - Do I va U trong doan mach noi tiep R1 = 10 Ohm, R2 = 20 Ohm (KHTN 9, lo 6, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-doanmach-01.json:
#   so_lieu_mau hang 1, 2 (U1, U2, U_AB, I): 1,0 2,0 3,0 0,10 ; 1,5 3,0 4,5 0,15. R1 = 10, R2 = 20 Ohm (tham_so).
#   KHONG dung hang 3 (2,0 + 4,0 vs 6,1): Cau 1 ngay sau hop hoi ly do lech 0,1 V -> clip khong duoc giai thich.
#   rut_ra: I = I1 = I2 ; U = U1 + U2 ; U1/U2 = R1/R2. bay = hien_tuong_hay_sai[1] (U chia deu).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[0].
# Du doan (K10: chi cau hoi + hinh): ampe ke truoc R1 chi 0,10 A, chuyen vao giua R1 va R2 -> so chi? -> van 0,10 A
#   (hien_tuong_hay_sai[0]: nghi dong giam dan sau moi dien tro).
# Cau chot (ghi o kho ghi_chu): doi nguon, von ke giua A, B chi 3,6 V -> von ke giua A, M chi? -> 1,2 V (hai buoc: I = 0,12 A)
#   (I = 0,12 A, U_AB = 3,6 V trong khoang tham_so U 0..6,5 V). 1,2 V chua tung hien tren man.
# Mach: nguon (+ ban dai ben trai, day duoi) -> K -> canh trai len -> ampe ke (+ trai) -> A -> R1 -> M -> R2 -> B -> canh phai
#   xuong -> (-). Ampe ke chi doi cho khi K mo (an_toan). Von ke song song dung doan do (+ o nut phia nguon +).
#   _kiem_dong_bo(): moi 0,05 s so chi ampe/von ke <-> trang thai K, vi tri ampe ke, cap nut von ke, o bang da ghi.
import copy
from engine import *

R1, R2 = 10.0, 20.0
ROWS = [dict(src=3.0, U1=1.0, U2=2.0, UAB=3.0, I=0.10),        # so_lieu_mau hang 1
        dict(src=4.5, U1=1.5, U2=3.0, UAB=4.5, I=0.15)]        # so_lieu_mau hang 2
UAB_C, U1_C = 3.6, 1.2                                          # cau chot: A-B 3,6 V -> I = 0,12 A -> A-M 1,2 V
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); RCOL = (180, 83, 9)

# ---------------- so do mach ----------------
TY, BY, XL, XR = 400, 700, 80, 1000
SLOT = (160, 545, 910)                  # ampe ke: truoc R1, giua R1 va R2, sau R2
POSN = ("trước R1", "giữa R1, R2", "sau R2")
NA, NM, NB = 240, 470, 830              # nut A, M, B
R1X, R2X = (280, 420), (620, 780)
VY, VR, AR = 585, 42, 38
VCX = {"AM": 355, "MB": 650, "AB": 535}
VNODE = {"AM": (NA, NM), "MB": (NM, NB), "AB": (NA, NB)}
VLAB = {"AM": "giữa A, M", "MB": "giữa M, B", "AB": "giữa A, B"}
KX0, KX1, SX = 250, 340, 620

def resistor(d, x0, x1, y, name, val, a=1.0, lab=True):
    card(d, (x0, y - 30, x1, y + 30), fill=A(mix(WHITE, RCOL, 0.18), a), outline=A(RCOL, a), r=10, w=5)
    if lab: text(d, ((x0 + x1) / 2, y - 66), f"{name} = {val:.0f} Ω", 40, mix(RCOL, INK, 0.3), alpha=a)

def ammeter(d, x, y, a=1.0):
    d.ellipse([x - AR, y - AR, x + AR, y + AR], fill=A(WHITE, a), outline=A(BLUE, a), width=6)
    text(d, (x, y + 2), "A", 42, BLUE, alpha=a)

def circuit(d, st):
    """st: pos (0..2, co the le khi dang doi cho), seated, closed, src, vpair."""
    card(d, (40, 260, 1040, 830), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    seat = int(round(st["pos"])) if st["seated"] else None
    # day tren: ngat quanh ampe ke dang mac
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
        dot(d, x, TY, 9, WIRE); text(d, (x + 28, TY + 62), nm, 40, INK)
    # ampe ke (dang mac hoac dang nhac len doi cho)
    if seat is not None:
        ammeter(d, SLOT[seat], TY); text(d, (SLOT[seat] - AR - 4, TY - 50), "+", 40, BLUE)
    else:
        p = st["pos"]; k = min(1, int(p)); f = p - k
        x = lerp(SLOT[k], SLOT[min(2, k + 1)], f) if p < 2 else SLOT[2]
        ammeter(d, x, TY - 95)
    # von ke song song
    vp = st["vpair"]
    if vp:
        cx = VCX[vp]; x1, x2 = VNODE[vp]
        d.line([(cx - VR, VY), (x1, VY), (x1, TY)], fill=PURPLE, width=5, joint="curve")
        d.line([(cx + VR, VY), (x2, VY), (x2, TY)], fill=PURPLE, width=5, joint="curve")
        d.ellipse([cx - VR, VY - VR, cx + VR, VY + VR], fill=WHITE, outline=PURPLE, width=6)
        text(d, (cx, VY + 2), "V", 42, PURPLE); text(d, (cx - VR - 22, VY - 40), "+", 40, PURPLE)
    # khoa K tren day duoi
    dot(d, KX0, BY, 9, WIRE); dot(d, KX1, BY, 9, WIRE)
    if st["closed"]: d.line([(KX0, BY), (KX1, BY)], fill=NAVY, width=7)
    else: d.line([(KX0, BY), (KX1 - 12, BY - 50)], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, BY + 52), "K", 40, NAVY)
    # nguon: ban dai (+) trai, ban ngan (-) phai
    d.line([(SX - 20, BY - 50), (SX - 20, BY + 50)], fill=NAVY, width=6)
    d.line([(SX + 20, BY - 26), (SX + 20, BY + 26)], fill=NAVY, width=14)
    text(d, (SX - 52, BY - 44), "+", 44, ORANGE); text(d, (SX + 54, BY - 44), "−", 44, ORANGE)
    text(d, (SX + 200, BY + 56), f"nguồn {vn(st['src']).replace(',0', '')} V", 40, INK)
    if st["closed"]:   # chieu dong dien: ra cuc +, canh trai di len, canh phai di xuong
        arrow(d, (XL, 650), (XL, 500), RED, w=7, head=20)
        arrow(d, (XR, 490), (XR, 640), RED, w=7, head=20)

def meters(d, st):
    i, u = readings(st)
    card(d, (40, 860, 530, 1080), fill=BODY, r=22)
    text(d, (285, 900), "ampe kế", 40, WHITE)
    card(d, (80, 935, 490, 1020), fill=SCREEN, r=12)
    text(d, (285, 978), "…" if i is None else vn(i, 2) + " A", 52, SCR_INK)
    text(d, (285, 1050), POSN[int(round(st["pos"]))] if st["seated"] else "đang đổi chỗ", 40, WHITE)
    card(d, (550, 860, 1040, 1080), fill=BODY, r=22)
    text(d, (795, 900), "vôn kế", 40, WHITE)
    card(d, (590, 935, 1000, 1020), fill=SCREEN, r=12)
    text(d, (795, 978), "–" if u is None else vn(u) + " V", 52, SCR_INK)
    if st["vpair"]: text(d, (795, 1050), VLAB[st["vpair"]], 40, WHITE)

# bang: cot I (3 cho) | A-M | M-B | A-B
TCX = (250, 590, 760, 930)
def table(d, cells, y=1110, hl=None):
    card(d, (40, y, 1040, y + 360), fill=WHITE, outline=LIGHT, w=3)
    text(d, (TCX[0], y + 45), "Ampe kế (A)", 40, BLUE)
    text(d, (760, y + 45), "Vôn kế (V)", 40, PURPLE)
    text(d, (TCX[0], y + 105), "3 chỗ", 40, MUTED)
    for x, h in zip(TCX[1:], ("A–M", "M–B", "A–B")): text(d, (x, y + 105), h, 40, INK)
    d.line([(70, y + 145), (1010, y + 145)], fill=LIGHT, width=3)
    d.line([(470, y + 20), (470, y + 340)], fill=LIGHT, width=3)
    for r, row in enumerate(ROWS):
        yy = y + 205 + r * 95
        if hl == r: d.rounded_rectangle([56, yy - 40, 1024, yy + 40], radius=20, fill=(255, 237, 213))
        for k in range(3):
            x = TCX[0] - 130 + k * 130
            if (r, "I%d" % k) in cells: text(d, (x, yy), vn(row["I"], 2), 44, BLUE)
            else: text(d, (x, yy), "·", 44, GRAY)
        for x, key, col in zip(TCX[1:], ("AM", "MB", "AB"), ("U1", "U2", "UAB")):
            if (r, key) in cells: text(d, (x, yy), vn(row[col]), 44, NAVY)
            else: text(d, (x, yy), "·", 44, GRAY)

# ---------------- dong thoi gian canh Tien hanh ----------------
# (moc, viec): close/open K, move (ampe ke tu vi tri hien tai sang vi tri moi trong MOVE giay), src, v (cap nut von ke)
MOVE = 0.4
EVT = [(0.7, "close", None), (1.6, "open", None), (1.7, "move", 1), (2.3, "close", None), (3.0, "open", None),
       (3.1, "move", 2), (3.7, "close", None), (4.9, "v", "AM"), (5.9, "v", "MB"), (6.9, "v", "AB"),
       (8.2, "open", None), (8.4, "src", 1), (8.6, "close", None), (9.0, "open", None), (9.1, "move", 1),
       (9.6, "close", None), (10.0, "open", None), (10.1, "move", 0), (10.6, "close", None),
       (11.1, "v", "AM"), (11.6, "v", "MB")]
T_CELL = 0.35

def do_state(t, evt=EVT):
    st = dict(pos=0.0, seated=True, closed=False, row=0, vpair=None); cells = set()
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
    # o bang: ghi sau T_CELL khi doc so (K dong, ampe ke da ngoi / von ke da mac)
    for te, kind, arg in evt:
        if t < te + T_CELL: continue
        s2 = do_state_raw(te + 0.001, evt)
        if kind == "close" and s2["seated"]:
            cells.add((s2["row"], "I%d" % int(round(s2["pos"]))))
            if s2["vpair"]: cells.add((s2["row"], s2["vpair"]))
        if kind == "v" and s2["closed"]: cells.add((s2["row"], arg))
    st["cells"] = cells
    return st

def do_state_raw(t, evt):
    st = dict(pos=0.0, seated=True, closed=False, row=0, vpair=None)
    for te, kind, arg in evt:
        if t < te: break
        if kind == "close": st["closed"] = True
        elif kind == "open": st["closed"] = False
        elif kind == "src": st["row"] = arg
        elif kind == "v": st["vpair"] = arg
        elif kind == "move":
            f = clamp((t - te) / MOVE); st["seated"] = f >= 1
            st["pos"] = float(arg) if f >= 1 else st["pos"]
    return st

def readings(st):
    """-> (so ampe ke | None khi dang doi cho, so von ke | None khi chua mac)."""
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
    if len(end) != 12: bad.append(("cuoi canh", "bang thieu o", sorted(end)))
    return bad

def _kiem_so():
    bad = []
    for r in ROWS:
        if abs(r["U1"] + r["U2"] - r["UAB"]) > 1e-9: bad.append(("U1+U2", r))
        if abs(r["U1"] / R1 - r["I"]) > 0.005 or abs(r["U2"] / R2 - r["I"]) > 0.005: bad.append(("I = U/R", r))
    if abs(UAB_C / (R1 + R2) * R1 - U1_C) > 1e-9: bad.append("chot")
    return bad

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
HOOK_ST = dict(pos=0.0, seated=True, closed=True, row=0, vpair=None, src=3.0)
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, HOOK_ST); meters(d, HOOK_ST)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 850 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 270, "Ampe kế trước R1 chỉ 0,10 A.\nChuyển ampe kế vào giữa R1 và R2.\nSố chỉ ampe kế thế nào?", 50, INK,
          maxw=900, alpha=a)
    text(d, (W / 2, y0 + 470), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 560, 940, y0 + 572], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 560, 140 + 800 * (1 - p), y0 + 572], radius=6, fill=A(PURPLE, a))

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · vẫn 0,10 A"
    pw = tw(d, lab, F(44)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 348), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 310), lab, 44, WHITE, alpha=ka)
    kb = appear(t, 0.5, 0.4)
    card(d, (40, 390, 1040, 1050), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
    y = 560
    d.line([(80, y), (1000, y)], fill=A(WIRE, kb), width=6)
    resistor(d, *R1X, y, "R1", R1, a=kb); resistor(d, *R2X, y, "R2", R2, a=kb)
    text(d, (130, 720), "lần 1", 40, MUTED, anchor="lm", alpha=kb)
    text(d, (130, 900), "lần 2", 40, MUTED, anchor="lm", alpha=kb)
    for k, sx in enumerate(SLOT):
        ak = appear(t, 0.7 + 0.35 * k, 0.35) * kb
        if ak <= 0: continue
        card(d, (sx - AR - 6, y - AR - 6, sx + AR + 6, y + AR + 6), fill=A(WHITE, ak), r=AR + 6)
        ammeter(d, sx, y, a=ak)
        xx = sx if k else sx + 70
        text(d, (xx, 790), vn(ROWS[0]["I"], 2), 54, BLUE, alpha=ak)
        k2 = appear(t, 1.7 + 0.3 * k, 0.35) * kb
        text(d, (xx, 970), vn(ROWS[1]["I"], 2), 54, BLUE, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 470), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=5)
    ctext(d, 370, "Nối tiếp: I như nhau ở mọi chỗ", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 <= 0: return
    card(d, (40, 510, 1040, 1080), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    for x, h in zip((250, 500, 760), ("A–M", "M–B", "A–B")): text(d, (x, 580), h, 44, INK, alpha=k1)
    d.line([(80, 625), (1000, 625)], fill=A(LIGHT, k1), width=3)
    for r, row in enumerate(ROWS):
        kr = appear(t, M[1] + 0.3 + 0.6 * r, 0.4) * k1
        yy = 700 + r * 110
        text(d, (250, yy), vn(row["U1"]), 52, NAVY, alpha=kr)
        text(d, (375, yy), "+", 52, MUTED, alpha=kr)
        text(d, (500, yy), vn(row["U2"]), 52, NAVY, alpha=kr)
        text(d, (630, yy), "=", 52, MUTED, alpha=kr)
        text(d, (760, yy), vn(row["UAB"]), 52, NAVY, alpha=kr)
        text(d, (900, yy), "V", 44, MUTED, alpha=kr)
    k2 = appear(t, M[1] + 1.8, 0.4) * k1
    if k2 > 0:
        d.rounded_rectangle([70, 910, 1010, 1050], radius=24, fill=A((236, 253, 243), k2))
        text(d, (W / 2, 980), "U = U1 + U2", 54, DGREEN, alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    y = 430
    d.line([(80, y), (1000, y)], fill=WIRE, width=6)
    resistor(d, 200, 420, y, "R1", R1, lab=False); resistor(d, 640, 880, y, "R2", R2, lab=False)
    text(d, (310, y - 70), "10 Ω", 44, RCOL); text(d, (760, y - 70), "20 Ω", 44, RCOL)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 820), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        ls = ("“Hiệu điện thế chia đều", "cho hai điện trở”")
        for j, q in enumerate(ls):
            yy = y0 + 210 + j * 72; lw = tw(d, q, F(50))
            text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2 + 330, y0 + 282), "✗", 56, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 2.2, 0.4)
        card(d, (70, y0 + 420, 1010, y0 + 760), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 530), "✓ 1,0 V và 2,0 V", 52, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 650), "không đều", 48, DGREEN, alpha=kk)
        text(d, (310, y0 - 90), "1,0 V", 46, PURPLE, alpha=kk); text(d, (760, y0 - 90), "2,0 V", 46, PURPLE, alpha=kk)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu minh hoạ", ""),
                                      ("• Bỏ qua điện trở", "ampe kế"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 280 + j * 250), l1, 50, INK, anchor="lm", alpha=kk)
            if l2: text(d, (132, y0 + 355 + j * 250), l2, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def end_body(d, t, k):
    """Hinh nho: hai dien tro noi tiep, von ke A-M chi 1,2 V, von ke M-B chi ?; goi y hien tre >= 2,5 s."""
    y = 1090
    d.line([(110, y), (970, y)], fill=A(WIRE, k), width=6)
    resistor(d, 190, 410, y, "R1", R1, a=k, lab=False); resistor(d, 620, 840, y, "R2", R2, a=k, lab=False)
    text(d, (300, y - 62), "10 Ω", 42, RCOL, alpha=k); text(d, (730, y - 62), "20 Ω", 42, RCOL, alpha=k)
    for x, nm in ((150, "A"), (515, "M"), (920, "B")):
        dot(d, x, y, 9, A(WIRE, k)); text(d, (x, y + 50), nm, 40, INK, alpha=k)
    text(d, (300, y + 130), "? V", 46, PURPLE, alpha=k)
    text(d, (535, y + 200), "A–B: 3,6 V", 46, PURPLE, alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Nối tiếp: I như nhau, U cộng lại",
             "Đổi nguồn, vôn kế giữa A, B chỉ 3,6 V. Vôn kế giữa A, M chỉ bao nhiêu?", body=end_body)
    kh = appear(t, M[0] + 2.8, 0.5)
    if kh > 0:
        card(d, (110, 1300 + 60, 970, 1560), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1410, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1495, "R1, R2 không đổi", 42, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    cs += [(do["t0"] + te, "tap") for te, kind, _ in EVT if kind == "close" and te < 8]
    cs += [(do["t0"] + 8.4, "tick")]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
           (b["t0"] + b["M"][0] + 2.2, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l9-doanmach-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Mạch nối tiếp · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai điện trở nối tiếp", draw=s_hook, tail=0.8, caps=[
   ("Nguồn 3 V, K đóng.", 2.5),
   ("Ampe kế đổi sang chỗ khác.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Mở K mỗi lần đổi chỗ ampe kế.", 4.4),
   ("Vôn kế đo từng đoạn.", 3.6),
   ("Lần 2: nguồn 4,5 V.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Giữa R1 và R2: vẫn 0,10 A.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Không bị dùng bớt.", 2.5),
   ("Hai đoạn cộng lại bằng cả đoạn.", 3.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Có đúng không?", 4.0),
   ("Còn chưa nói được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Tự trả lời trước khi xem.", 6.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
        clip = copy.deepcopy(CLIP); build(clip); sc = [s for s in clip["scenes"] if s["key"] == "do"][0]
        prev = None; t = 0.0
        while t < sc["T"]:
            st = do_state(t); i, u = readings(st)
            cur = (st["vpair"], st["closed"], u, ROWS[st["row"]]["src"])
            if cur != prev:
                cap = [c for m, c in zip(sc["M"], sc["caps"]) if t >= m - 0.05]
                print(f"  {sc['t0'] + t:5.2f}s vôn kế {VLAB.get(cur[0], 'chưa mắc')} K={'đóng' if cur[1] else 'mở'} số={u} nguồn={cur[3]} | phụ đề: {cap[-1] if cap else '-'}")
                prev = cur
            t += 0.05
