# Clip: tn-l12-boylecharles-01 - Nen khi trong xilanh kin, doc ap ke (Boyle).
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-boylecharles-01.json (_kiem_so() doi chieu so_lieu_mau, tham_so).
# Ban 2-3 (27/10/2026): mau goc. Ban 4 (21/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 20): cong --do-chu
#   (chu ve >= 55 px, <= 180 tu/phut moi canh, nhip >= 2,5 s), <= 50 s, K10 (khong nut A-D, khong so nhay thoang qua).
# Quan niem sai can danh (hien_tuong_hay_sai[0]): nen con 1/2 the tich thi p chi "tang chut it".
# Du doan: 8,0 -> 4,0 ml, ap ke (dang 100 kPa) chi bao nhieu? -> dap an: gan gap doi (215 kPa, so_lieu_mau hang 4).
# Thu tu: Du doan -> Tien hanh (4 hang dau bang) -> Vi sao (mat do, va cham) -> Tich p.V (4 cot, lech toi 8%)
#   -> Bay an nhanh (hai khung canh nhau: an tu tu / an that nhanh) -> Chot + THU NGHI.
#   Hang 5 (3,0 ml) KHONG chieu: bai ly thuyet de o p.V hang 5 "em tu tinh".
# Thu nghi (= cau_chot khung web): ap ke do toi 300 kPa (dung_cu), van 8,0 ml / 100 kPa -> kim cham 300 khi V = 800/300
#   ~ 2,7 ml. Dap so khong hien tren man (khong ve duong hypebol, kim khong toi 300).
import random
from engine import *

ROWS = [(8.0, 100), (6.0, 142), (5.0, 170), (4.0, 215)]               # so_lieu_mau hang 1-4: V (ml), p (kPa)
PV = [round(v * p) for v, p in ROWS]                                   # 800 852 850 860
T_PHONG, P0V0, P_MAX = 25, 800, 300                                    # tham_so t; p0*V0 = 100*8; thang ap ke 300 kPa
def fmt(v): return f"{v:.1f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-boylecharles-01.json")))
    hang = [(r[1], r[2], r[3]) for r in k["so_lieu_mau"]["hang"]]
    for (v, p), pv in zip(ROWS, PV): assert (v, p, pv) in hang, (v, p, pv)
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["t"]["gia_tri"] == T_PHONG and ts["p0"]["gia_tri"] * ts["V0"]["gia_tri"] == P0V0
    assert any("300 kPa" in d["ten"] for d in k["dung_cu"])
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
FS = 60                                   # chu phu nho nhat khi ve (x0,88 = 53 px trong mp4; cong B v1: phong to tu 56)

R = random.Random(11)
PART = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.25, 0.5), R.choice((-1, 1)) * R.uniform(0.25, 0.5))
        for _ in range(30)]

# ---------------- xilanh dung + ap ke ----------------
BX0, BX1, Y0ML, PXML = 250, 450, 1000, 46       # thanh xilanh trong; y cua vach 0 ml; px moi ml
def ymL(v, y0=Y0ML, px=PXML): return y0 - v * px

def syringe(d, t, V, bx0=BX0, bx1=BX1, y0=Y0ML, px=PXML, scale_lbl=True, heat=0.0, push=False, vmin=3.0, a=1.0):
    top = ymL(10.4, y0, px); yh = ymL(V, y0, px); cx = (bx0 + bx1) / 2; s = px / PXML
    d.rounded_rectangle([bx0 - 10, top, bx1 + 10, y0 + 10], radius=int(16 * s), fill=A((246, 249, 255), a))
    d.rectangle([bx0, yh, bx1, y0], fill=A(mix((214, 232, 255), (255, 214, 200), heat), a))   # khoi khi nhot kin
    for (ux, uy, vx, vy) in PART:                                     # cung so hat, vung chua nho lai -> day len
        sp = 1 + 1.6 * heat
        x = bx0 + 14 * s + refl(ux + vx * t * sp, 0, 1) * (bx1 - bx0 - 28 * s)
        y = yh + 14 * s + refl(uy + vy * t * sp, 0, 1) * (y0 - yh - 28 * s)
        dot(d, x, y, 9 * s, A(mix(ORANGE, RED, heat), a))
    d.rounded_rectangle([bx0 - 10, top, bx1 + 10, y0 + 10], radius=int(16 * s), outline=A(NAVY, a), width=max(3, int(6 * s)))
    for v in range(0, 11):
        L = (24 if v % 2 == 0 else 14) * s
        d.line([(bx0 - 10, ymL(v, y0, px)), (bx0 - 10 + L, ymL(v, y0, px))], fill=A(NAVY, a), width=max(2, int(3 * s)))
        if scale_lbl and v % 2 == 0 and v > 0:
            text(d, (bx0 - 24, ymL(v, y0, px)), str(v), FS, INK, anchor="rm", alpha=a)
    if scale_lbl: text(d, (bx0 - 24, y0 + 10), "ml", FS, INK, anchor="rm", alpha=a)
    hh = 26 * s; d.rectangle([bx0 + 2, yh - hh, bx1 - 2, yh], fill=A((70, 78, 100), a))       # pit-tong + can + tay nam
    rod_top = yh - hh - ((10.4 - vmin) * px - hh + 18)
    d.rectangle([cx - 11 * s, rod_top, cx + 11 * s, yh - hh], fill=A(GRAY, a), outline=A(NAVY, a), width=max(2, int(3 * s)))
    d.rounded_rectangle([cx - 110 * s, rod_top - 22 * s, cx + 110 * s, rod_top], radius=int(10 * s), fill=A(NAVY, a))
    if push:
        ax = cx + 110 * s + 40 * s
        arrow(d, (ax, rod_top - 70 * s), (ax, rod_top + 20 * s), A(ORANGE, a), w=max(5, int(9 * s)), head=int(24 * s))
    d.rectangle([cx - 20 * s, y0 + 10, cx + 20 * s, y0 + 40 * s], fill=A(GRAY, a), outline=A(NAVY, a), width=max(2, int(3 * s)))
    return cx, y0 + 40 * s

def gang(p): return math.radians(-225 + clamp(p / 300) * 270)
def gauge(d, cx, cy, r, p, labels=True, mark=None, mark_a=1.0, a=1.0, mark_lbl=True):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, a), outline=A(NAVY, a), width=7)
    a0, a1 = math.degrees(gang(270)), math.degrees(gang(300))
    d.arc([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], a0, a1, fill=A((248, 180, 170), a), width=14)
    for k in range(0, 13):
        g = gang(k * 25); L = 26 if k % 2 == 0 else 13
        d.line([(cx + (r - 14 - L) * math.cos(g), cy + (r - 14 - L) * math.sin(g)),
                (cx + (r - 14) * math.cos(g), cy + (r - 14) * math.sin(g))], fill=A(NAVY, a), width=4 if k % 2 == 0 else 3)
    if labels:
        for v in (0, 100, 200, 300):
            g = gang(v); rr = r + 54
            text(d, (cx + rr * math.cos(g), cy + rr * math.sin(g)), str(v), FS, INK, alpha=a)
        text(d, (cx, cy + r * 0.52), "kPa", FS, INK, alpha=a)
    if mark is not None and mark_a > 0:
        g = gang(mark)
        d.line([(cx + (r - 2) * math.cos(g), cy + (r - 2) * math.sin(g)), (cx + (r + 24) * math.cos(g), cy + (r + 24) * math.sin(g))],
               fill=A(DGREEN, mark_a), width=9)
        if mark_lbl: text(d, (cx + (r + 62) * math.cos(g), cy + (r + 62) * math.sin(g)), str(mark), FS, DGREEN, alpha=mark_a)
    g = gang(p)
    d.line([(cx - 22 * math.cos(g), cy - 22 * math.sin(g)), (cx + (r - 34) * math.cos(g), cy + (r - 34) * math.sin(g))],
           fill=A(RED, a), width=9)
    dot(d, cx, cy, 14, A(NAVY, a))

GX, GY, GR = 820, 860, 165
def shown(V, p, moving):
    """Chu tren the V/p: dang an -> dau ba cham (khong so noi suy); dung -> dung so hang kho."""
    if moving: return "…", "…"
    return fmt(V), f"{p:.0f}"

def rig(d, t, V, p, push=False):
    nx, ny = syringe(d, t, V, push=push)
    d.line([(nx, ny), (nx, 1085), (GX, 1085), (GX, GY + GR)], fill=GRAY, width=16, joint="curve")
    gauge(d, GX, GY, GR, p)
    card(d, (600, 265, 1040, 555), fill=WHITE, outline=LIGHT, r=28, w=4)
    sv, sp = shown(V, p, push)
    text(d, (820, 330), f"V = {sv} ml", 62, BLUE)
    text(d, (820, 415), f"p = {sp} kPa", 62, RED)
    text(d, (820, 497), f"t = {T_PHONG} °C", FS, INK)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI; o da tat: nen trang, vien dam."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, t, 8.0, 100)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1110 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 475), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 98), fill=A(PURPLE, k), r=36)
    text(d, (W / 2, y0 + 60), "DỰ ĐOÁN", 56, WHITE, alpha=k)
    text(d, (W / 2, y0 + 175), "Nén còn 4,0 ml.", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 265), "Áp kế chỉ bao nhiêu?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 360, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh, ghi bang (4 lan do) ----------------
MOVE = 1.0
PUSH = [None, 0.4, 1.9, 3.4]               # moc bat dau an toi hang i (tua nhanh, hang cach 1,5 s, so chi len deu)
def state(t):
    V, c, moving = ROWS[0][0], PV[0], False
    for i in range(1, 4):
        if t < PUSH[i]: break
        k = ease((t - PUSH[i]) / MOVE); V = lerp(ROWS[i - 1][0], ROWS[i][0], k); c = lerp(PV[i - 1], PV[i], k)
        moving = t - PUSH[i] < MOVE
    return V, c / V, moving

def row_at(i): return 0.3 if i == 0 else PUSH[i] + MOVE + 0.3

XV, XP = 330, 640
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    V, p, mv = state(t); rig(d, t, V, p, push=mv)
    card(d, (60, 1110, 1020, 1560), fill=WHITE, outline=NAVY, w=4)
    text(d, (XV, 1165), "V (ml)", 60, BLUE); text(d, (XP, 1165), "p (kPa)", 60, RED)
    for j in range(2): d.polygon([(655 + j * 30, 600), (655 + j * 30, 644), (683 + j * 30, 622)], fill=DORANGE)   # dau tua nhanh
    text(d, (730, 622), "tua nhanh", FS, DORANGE, anchor="lm")
    d.line([(100, 1205), (980, 1205)], fill=LIGHT, width=4)
    kh = appear(t, M[1], 0.4)
    for i, (v, pp) in enumerate(ROWS):
        a = appear(t, row_at(i), 0.35); y = 1255 + i * 80
        if a <= 0: continue
        if kh > 0 and i in (0, 3): d.rounded_rectangle([250, y - 36, 720, y + 36], radius=16, fill=A((255, 237, 213), kh))
        text(d, (XV, y), fmt(v), 60, BLUE, alpha=a); text(d, (XP, y), str(pp), 60, RED, alpha=a)
    ya, yb = 1255, 1255 + 3 * 80
    for x0, lab, col, at in ((215, "÷2", BLUE, M[1]), (765, "≈ ×2", RED, M[1] + 1.3)):
        g = ease((t - at) / 0.6)
        if g <= 0: continue
        d.line([(x0, ya), (x0, ya + (yb - 30 - ya) * g)], fill=col, width=7)
        if g >= 1: arrow(d, (x0, yb - 60), (x0, yb - 8), col, w=7, head=22)
        lx = 140 if x0 < 500 else 880
        text(d, (lx, (ya + yb) / 2), lab, 64, col, alpha=g)

# ---------------- canh 3: vi sao p tang ----------------
def hits(u0, s, L, t):  # so lan dap vao hai thanh trai/phai trong [0, t]
    return abs(math.floor((u0 + s * t) / L) - math.floor(u0 / L))

RB = random.Random(5)
MOL = [(RB.random(), RB.random(), RB.choice((-1, 1)) * RB.uniform(110, 210), RB.choice((-1, 1)) * RB.uniform(110, 210)) for _ in range(20)]
def box(d, t, t0, tp, x0, x1, y0, y1, lbl, p_):
    d.rectangle([x0, y0, x1, y1], fill=(236, 244, 255))
    d.line([(x0, y0), (x1, y0)], fill=NAVY, width=4); d.line([(x0, y1), (x1, y1)], fill=NAVY, width=4)
    L, Hh = x1 - x0 - 24, y1 - y0 - 24; n = 0
    flashL, flashR = [], []
    for (ux, uy, vx, vy) in MOL:
        x = x0 + 12 + refl(ux * L + vx * t, 0, L); y = y0 + 12 + refl(uy * Hh + vy * t, 0, Hh)
        dot(d, x, y, 11, ORANGE)
        if t > t0: n += hits(ux * L, vx, L, t) - hits(ux * L, vx, L, t0)
        if t > t0 and x - x0 < 26: flashL.append(y)          # chop va cham chi tu luc bat dau dem (cung luc nhan)
        if t > t0 and x1 - x < 26: flashR.append(y)
    for xx, fl in ((x0, flashL), (x1, flashR)):
        d.line([(xx, y0), (xx, y1)], fill=ORANGE, width=10)
        for y in fl: d.line([(xx, y - 26), (xx, y + 26)], fill=YELLOW, width=18)
    text(d, ((x0 + x1) / 2, y0 - 42), lbl, 60, BLUE)
    if t > t0: text(d, ((x0 + x1) / 2, y1 + 60), f"{n} va chạm", FS, DORANGE)
    a = appear(t, tp)
    if a > 0: text(d, ((x0 + x1) / 2, y1 + 150), f"p = {p_} kPa", 60, RED, alpha=a)

def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; t0 = M[1]
    box(d, t, t0, t0 + 2.5, 120, 520, 370, 1110, "8,0 ml", ROWS[0][1])
    box(d, t, t0, t0 + 2.5, 700, 900, 370, 1110, "4,0 ml", ROWS[3][1])

# ---------------- canh 4: tich p.V ----------------
def s_graph(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (60, 280, 1020, 1530), fill=WHITE, outline=LIGHT, w=3)
    base, k = 1360, 0.85
    band = appear(t, M[1], 0.4)
    if band > 0: d.rectangle([90, base - 860 * k, 990, base - 800 * k], fill=A((187, 247, 208), band))
    if band < 0.5: text(d, (W / 2, 350), "Tích p·V (kPa·ml)", 60, INK)
    else: text(d, (W / 2, 350), "p·V ≈ 800 – 860 kPa·ml", 60, DGREEN)
    d.line([(90, base), (990, base)], fill=NAVY, width=5)
    for i, ((v, p_), pv) in enumerate(zip(ROWS, PV)):
        cx = 210 + i * 220; g = ease((t - M[0] - 0.3 - i * 0.55) / 0.5)
        text(d, (cx, base + 60), f"{fmt(v)} ml", FS, BLUE)
        if g <= 0: continue
        top = base - pv * k * g
        d.rectangle([cx - 65, top, cx + 65, base], fill=ORANGE)
        text(d, (cx, top - 40), str(pv), 60, INK, alpha=clamp(g * 2 - 1))

# ---------------- canh 5: bay an that nhanh (hai khung canh nhau) ----------------
TS = 0.6                                   # luc ca hai bat dau an
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for j, (cx, lab, col) in enumerate(((285, "Ấn từ từ", DGREEN), (795, "Ấn thật nhanh", DRED))):
        card(d, (cx - 245, 280, cx + 245, 1540), fill=WHITE, outline=col, w=6)
        text(d, (cx, 345), lab, 60, col)
        if j == 0: kc, heat = ease((t - TS) / 2.2), 0.0                       # 8 -> 4 ml trong 2,2 s, nhiet do giu nguyen
        else: kc, heat = ease((t - TS) / 0.3), ease((t - TS) / 1.2)           # 8 -> 4 ml trong 0,3 s, khi nong len
        V = lerp(8.0, 4.0, kc)
        sx = cx - 100
        syringe(d, t, V, bx0=sx - 50, bx1=sx + 50, y0=1000, px=36, scale_lbl=False, heat=heat,
                push=0 < t - TS < (2.2 if j == 0 else 0.4), vmin=4.0)
        tx, tb, tt = cx + 130, 960, 620                                      # nhiet ke
        d.rounded_rectangle([tx - 16, tt, tx + 16, tb], radius=16, fill=WHITE, outline=NAVY, width=4)
        dot(d, tx, tb + 18, 30, RED, NAVY)
        d.rectangle([tx - 8, lerp(tb - 120, tb - 300, heat), tx + 8, tb], fill=RED)
        c = lerp(PV[0], PV[3], kc)                                           # dang nhiet: toi dung 215 kPa (hang 4)
        p = c / V * (1 + 0.25 * heat)
        gauge(d, cx, 1300, 120, p, labels=False, mark=ROWS[3][1])   # ca hai: vach + "215" (muc nhiet do khong doi)
    a = appear(t, M[1] - 0.1, 0.45)
    if a > 0:
        text(d, (900, 560), "nóng lên", FS, DRED, alpha=a)
        text(d, (795, 1480), "p vượt mức", 60, DRED, alpha=a)

# ---------------- canh 6: chot (phu de) + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 238, W / 2 + pw / 2, 314), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 276), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    syringe(d, t, 8.0, bx0=170, bx1=330, y0=930, px=40, a=k1)
    gauge(d, 770, 640, 165, 100, a=k1)
    text(d, (W / 2, 1110), "Kim chạm 300 kPa", 64, INK, alpha=k1)
    text(d, (W / 2, 1200), "khi khí còn mấy ml?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, w, g, tr, e = (sc[k] for k in ("hook", "do", "why", "graph", "trap", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + row_at(3), "ding"), (w["t0"] + w["M"][1], "tap"), (g["t0"] + g["M"][1], "tap"),
            (tr["t0"] + TS, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l12-boylecharles-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Định luật Boyle · thachlab.id.vn", scenes=[
 dict(key="hook", title="Nén khí trong xilanh kín", draw=s_hook, tail=0.3, caps=[
   ("Khí nhốt kín, nối áp kế.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Ấn từ từ, đọc áp kế", draw=s_do, tail=0.3, caps=[
   ("Ấn từ từ, đợi số ổn định.", 4.6),
   ("Gần gấp đôi, không phải chút ít.", 3.9)]),
 dict(key="why", title="Vì sao p tăng?", draw=s_why, tail=0.3, caps=[
   ("Nửa thể tích, mật độ gấp đôi.", 3.4),
   ("Va chạm lên thành nhiều hơn → p tăng.", 3.9)]),
 dict(key="graph", title="Nhân p với V", draw=s_graph, tail=0.3, caps=[
   ("Tính tích ở từng lần đo.", 3.2),
   ("Gần như không đổi, lệch tới 8%.", 3.9)]),
 dict(key="trap", title="Bẫy: ấn thật nhanh", draw=s_trap, tail=0.3, caps=[
   ("Cùng nén còn một nửa.", 3.0),
   ("Không còn đẳng nhiệt nữa.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Nhiệt độ không đổi: p·V không đổi.", 5.4)]),
])

def _kiem_the():
    """Moi 0,05 s canh do: khi khong an, the V/p phai trung dung mot hang kho (khong so lech 142/143)."""
    bad = []; t = 0.0
    while t < 9.0:
        V, p, mv = state(t); sv, sp = shown(V, p, mv)
        if not mv and (sv, sp) not in [(fmt(v), str(q)) for v, q in ROWS]: bad.append((round(t, 2), sv, sp))
        t += 0.05
    return bad
_b = _kiem_the(); assert not _b, _b
