# Clip: tn-l9-xoaychieu-01 - Nam cham dien: dong doi chieu thi cuc tu doi theo, kim nam cham lac qua lai (KHTN 9, bai 93)
# Vong 2 (18/11/2026, theo cong B): Du doan KHONG hoi dinh sat (bai noi san 4 cho) va KHONG hoi kim voi 50 Hz (Cau 2):
#   hoi kim voi nguon DOI CHIEU THAT CHAM, moi 2 giay mot lan (mo hinh minh hoa, ghi trong so_lieu_mau.ghi_chu cua kho).
#   -> kim lac qua lai theo tung lan doi chieu. Bo dinh sat (khong ve lo lung). Vong 3: Bay "nguon that 50 Hz, kim van lac ro"
#   (khong viet "doi chieu 50 lan/giay": 50 Hz doi chieu 100 lan/giay), dat TRUOC Rut ra. Rut ra: cuc tu doi theo chieu dong; nguon that doi chieu rat nhanh -> luc len kim doi chieu lien tuc,
#   kim rung quanh cho cu (KHONG noi "100 lan moi giay", "khong kip quay" = dap an Cau 6). Chua noi duoc = so_lieu_mau.ghi_chu
#   GD2 27/11 (kiem-v1): Chua noi duoc = "kim rung manh co nao (chua do)" (bo "tu du" ngoai chuong trinh).
#   Vong 3 (kiem-v2): cau "dinh sat luon bi hut" bai da noi san -> cau chot DEM: nguon mo hinh doi chieu moi 2 s (kho
#   so_lieu_mau.ghi_chu). Vong 4 (kiem-v3): "0-2 s kim lech phai; giay 5 lech phia nao?" -> phai (4-6 s lai nhu 0-2 s).
#   Phia lech khop mo phong: i_slow > 0 o 0-2 s -> cuc N gan kim -> lech + = phai. Man ghi "theo mô hình", bo the chot xanh.
#   Bay: hai o canh nhau "2 s/lần: lắc rõ" va "50 Hz: chỉ rung". Hop quy tac hien sau >= 4 s.
# Vat li (mo hinh): i > 0 -> dau phai loi (gan kim) la N, day dau N cua kim sang phai (lech +); i < 0 -> S, hut N sang trai.
#   Nguon cham: i = sin(2*pi*t/(2*HALF)), kim lech DEV*i (gan dung tinh). Kiem: _kiem_so(), _kiem_dong_bo() moi 0,05 s.
import math
from engine import *

U, FHZ = 6, 50                       # tham_so U (V), f (Hz)
HALF = 2.0                           # so_lieu_mau.ghi_chu: doi chieu moi 2 giay (mo hinh)
ROWS = [("dc", "một chiều", "lệch một phía"), ("slow", "đổi chiều chậm", "lắc qua lại")]   # so_lieu_mau (rut gon)
DEV = math.radians(55); JIT = math.radians(3)
WIRE = (60, 66, 92); CU = (184, 115, 51); FE = (150, 155, 170); DRED = (185, 28, 28); DGREEN = (21, 110, 55)

def pole_right(i):
    """Cuc o dau loi gan kim: i > 0 -> N, i < 0 -> S, gan 0 -> None."""
    return "N" if i > 0.15 else ("S" if i < -0.15 else None)
def kim_sign(pole):
    return {"N": 1, "S": -1}.get(pole, 0)
def i_slow(t):
    return math.sin(math.pi * t / HALF)

# ---------------- hinh dung cu ----------------
CX0, CX1, CY = 200, 760, 470
KIM = (900, 470)

def needle(d, x, y, ang, L=150, hw=16, a=1.0):
    c, s = math.cos(ang), math.sin(ang); px, py = -s * hw, c * hw
    n = (x + c * L / 2, y + s * L / 2); so = (x - c * L / 2, y - s * L / 2)
    d.polygon([(x + px, y + py), n, (x - px, y - py)], fill=A(RED, a), outline=A(NAVY, a))
    d.polygon([(x + px, y + py), so, (x - px, y - py)], fill=A(BLUE, a), outline=A(NAVY, a))
    dot(d, x, y, 7, A(WHITE, a), A(NAVY, a))

def core(d, x0, x1, y, pr, a=1.0, h=64, end=60):
    d.rectangle([x0, y - h / 2, x1, y + h / 2], fill=A(FE, a), outline=A(NAVY, a), width=3)
    if pr:
        pl = "S" if pr == "N" else "N"
        for xa, xb, p in ((x0, x0 + end, pl), (x1 - end, x1, pr)):
            d.rectangle([xa, y - h / 2, xb, y + h / 2], fill=A(RED if p == "N" else BLUE, a), outline=A(NAVY, a), width=3)
            text(d, ((xa + xb) / 2, y + 1), p, 54, WHITE, alpha=a)
    n = int((x1 - x0 - 2 * end - 40) / 30)
    for k in range(n + 1):
        x = x0 + end + 20 + k * (x1 - x0 - 2 * end - 40) / n
        d.line([(x - 8, y - h / 2 - 12), (x + 8, y + h / 2 + 12)], fill=A(CU, a), width=6)

def stand(d, x, y, dev, a=1.0, L=150, hw=16):
    d.line([(x, y), (x, y + 140)], fill=A(NAVY, a), width=6); d.line([(x - 40, y + 142), (x + 40, y + 142)], fill=A(NAVY, a), width=8)
    needle(d, x, y, -math.pi / 2 + dev, L=L, hw=hw, a=a)

def apparatus(d, src, closed, i, dev, src_a=1.0):
    card(d, (40, 260, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    pr = pole_right(i) if closed else None
    d.line([(300, 512), (300, 580)], fill=WIRE, width=5); d.line([(300, 650), (300, 720), (340, 720)], fill=WIRE, width=5, joint="curve")
    d.line([(700, 512), (700, 720), (660, 720)], fill=WIRE, width=5, joint="curve")
    dot(d, 300, 580, 8, WIRE); dot(d, 300, 650, 8, WIRE)
    if closed: d.line([(300, 650), (300, 580)], fill=NAVY, width=7)
    else: d.line([(300, 650), (352, 592)], fill=NAVY, width=7)
    text(d, (250, 615), "K", 58, NAVY)
    card(d, (330, 642, 670, 788), fill=(245, 243, 255), outline=NAVY, r=18, w=4)
    name = "một chiều" if src == "dc" else "đổi chiều"
    text(d, (500, 684), name, 56, mix(BG, INK, src_a)); text(d, (500, 749), f"{U} V", 56, mix(BG, ORANGE, src_a))
    if closed and abs(i) > 0.15:          # nhanh phai: i > 0 chay tu cuon xuong
        y0, y1 = (560, 640) if i > 0 else (640, 560)
        arrow(d, (735, y0), (735, y1), RED, w=5, head=16); text(d, (775, 600), "I", 58, RED)
    core(d, CX0, CX1, CY, pr)
    stand(d, KIM[0], KIM[1], dev)

def table(d, n, hl=None, y=830):
    card(d, (40, y, 1040, y + 330), fill=WHITE, outline=LIGHT, w=3)
    XS = (300, 760)
    for x, h in zip(XS, ("Nguồn", "Kim")): text(d, (x, y + 50), h, 56, INK)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=3)
    for j, (k, a, c) in enumerate(ROWS):
        yy = y + 160 + j * 100
        if hl == j: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=(255, 237, 213))
        if j < n: text(d, (XS[0], yy), a, 56, NAVY); text(d, (XS[1], yy), c, 56, PURPLE)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.3


def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, "slow", False, 0.0, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 840 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 620), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 170), "Nguồn đổi chiều chậm,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 255), f"mỗi {HALF:.0f} giây một lần.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 340), "Kim thế nào?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 440, 970, y0 + 540], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 440, 110 + max(90, 860 * (1 - p)), y0 + 540], radius=45, fill=A((76, 29, 149), a))


# ---------------- canh 2: Tien hanh ----------------
T_C1, T_O1, T_SW, T_C2 = 0.8, 2.6, 3.0, 3.6
T_ROW1, T_ROW2 = T_C1 + 0.5, T_C2 + 2 * HALF        # hang 2 chi ghi sau khi kim da sang ca hai phia
def do_state(t):
    """-> (nguon, alpha chu, K dong?, i, goc lech kim, so hang)."""
    src = "slow" if t >= T_SW else "dc"; sa = clamp((t - T_SW) / 0.3) if t >= T_SW else 1.0
    if T_C1 <= t < T_O1:
        closed, i = True, 1.0; dev = DEV * ease((t - T_C1) / 0.45)
    elif t >= T_C2:
        closed, i = True, i_slow(t - T_C2); dev = DEV * i
    else:
        closed, i = False, 0.0; dev = DEV * (1 - ease((t - T_O1) / 0.45)) if t >= T_O1 else 0.0
    n = (1 if t >= T_ROW1 else 0) + (1 if t >= T_ROW2 else 0)
    return src, sa, closed, i, dev, n

def s_do(img, d, t, sc):
    src, sa, closed, i, dev, n = do_state(t)
    apparatus(d, src, closed, i, dev, src_a=sa)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    if sc["T"] < T_ROW2 + 1.0: bad.append(("canh do ngan", sc["T"]))
    seen = set()
    while t < sc["T"]:
        src, sa, closed, i, dev, n = do_state(t)
        sg = kim_sign(pole_right(i)) if closed else 0
        if sg and t > T_C1 + 0.5 and dev * sg <= 0: bad.append((round(t, 2), "kim sai chieu"))
        if closed and src == "slow" and sg: seen.add(sg)
        if n >= 2 and seen != {1, -1}: bad.append((round(t, 2), "ghi 'lac qua lai' truoc khi kim sang hai phia"))
        if closed and src == "dc" and not (T_C1 <= t < T_O1): bad.append((round(t, 2), "nguon lech"))
        t += 0.05
    return bad

def _kiem_so():
    bad = []
    if not (kim_sign(pole_right(1)) == -kim_sign(pole_right(-1)) != 0): bad.append("doi chieu dong phai doi phia kim")
    if abs(i_slow(HALF) ) > 1e-9 or i_slow(HALF / 2) <= 0 or i_slow(1.5 * HALF) >= 0: bad.append("chu ki nguon cham")
    if not (kim_sign(pole_right(i_slow(1.0))) > 0): bad.append("cau chot: 0-2 s kim phai lech PHAI (chu tren man)")
    if kim_sign(pole_right(i_slow(CHOT_S))) != kim_sign(pole_right(i_slow(1.0))): bad.append("cau chot: giay 5 phai cung phia 0-2 s")
    if kim_sign(pole_right(i_slow(3.0))) != -kim_sign(pole_right(i_slow(1.0))): bad.append("cau chot: 2-4 s phai lech trai")
    if 2 * FHZ != 100: bad.append("50 Hz doi chieu 100 lan/giay")
    return bad

# ---------------- canh 3: Dap an ----------------
GX0, GX1 = 110, 990
def graph(d, y, half, x_end, a=1.0, amp=110, poles=False, cycles_w=8.0):
    """Do thi i(t) (truc t dai cycles_w giay), ve den x_end."""
    d.line([(GX0, y), (GX1, y)], fill=A(NAVY, a), width=4); d.line([(GX0, y - amp - 40), (GX0, y + amp + 40)], fill=A(NAVY, a), width=4)
    text(d, (GX0 - 40, y - amp - 20), "i", 58, NAVY, alpha=a); text(d, (GX1 + 20, y + 44), "t", 58, NAVY, alpha=a)
    pts = [(x, y - amp * math.sin(math.pi * cycles_w * (x - GX0) / (GX1 - GX0) / half)) for x in range(GX0, int(x_end) + 1, 4)]
    for x, yy in pts: d.line([(x, y), (x, yy)], fill=A(mix(WHITE, RED if yy < y else BLUE, 0.22), a), width=4)
    if len(pts) > 1: d.line(pts, fill=A(ORANGE, a), width=6)
    if poles:
        nq = int(round(cycles_w / half))
        for q in range(nq):
            xc = GX0 + (q + 0.5) * (GX1 - GX0) / nq
            if x_end >= xc:
                p = "N" if q % 2 == 0 else "S"; yc = y - amp * 0.55 if p == "N" else y + amp * 0.55
                dot(d, xc, yc, 36, A(RED if p == "N" else BLUE, a)); text(d, (xc, yc + 1), p, 54, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: lắc qua lại", 305, ka)
    k = appear(t, 0.4, 0.4)
    card(d, (40, 390, 1040, 1330), fill=A(WHITE, k), outline=A(TEAL, k), w=5)
    tt = clamp((t - 0.6) / 6.0) * 6.0                       # 6 s that = 1,5 chu ki, con tro chay theo
    xc = GX0 + (GX1 - GX0) * tt / 8.0
    graph(d, 600, HALF, xc, a=k)
    d.line([(xc, 450), (xc, 750)], fill=A(PURPLE, k), width=3)
    i = i_slow(tt)
    stand(d, W / 2, 960, DEV * i, a=k, L=200, hw=20)
    pr = pole_right(i)
    if pr:
        sg = kim_sign(pr)
        arrow(d, (W / 2 + sg * 140, 960), (W / 2 + sg * 260, 960), A(RED, k), w=6, head=20)
    kb = appear(t, M[1] - 0.1, 0.4)
    text(d, (W / 2, 1240), "dòng đổi chiều → kim đổi phía", 56, PURPLE, alpha=kb)

# ---------------- canh 4: Bay roi Chua noi duoc (truoc Rut ra) ----------------
BAY_ST = 2.0                                # gach o 2,0 s; ✓ o M[1] (>= 3 s sau); Chua noi o M[2] (>= 3 s sau ✓)
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 640), fill=WHITE, outline=LIGHT, w=3)      # hai o canh nhau: cham thi lac ro, 50 Hz chi rung
    d.line([(540, 290), (540, 610)], fill=LIGHT, width=3)
    stand(d, 290, 400, DEV * i_slow(t), L=130, hw=14)
    stand(d, 790, 400, JIT * math.sin(2 * math.pi * 6 * t), L=130, hw=14)
    al = appear(t, 0.2, 0.45)                   # cung luc the Bay (mot khoi)
    text(d, (290, 590), "2 s/lần: lắc rõ", 56, NAVY, alpha=al)
    text(d, (790, 590), f"{FHZ} Hz: chỉ rung", 56, PURPLE, alpha=al)
    k2 = appear(t, M[2] + 0.3, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    y0 = 680
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        ks = clamp((t - BAY_ST) / 0.4)
        for j, q in enumerate((f"“Nguồn {FHZ} Hz:", "kim vẫn lắc rõ”")):
            yy = y0 + 180 + j * 85; lw = tw(d, q, F(58))
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 340, 1010, y0 + 500), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 420), "✓ Kim chỉ rung", 60, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "kim rung mạnh cỡ nào", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(chưa đo)", 56, NAVY, alpha=k2)

# ---------------- canh 5: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 740), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    graph(d, 500, HALF, GX0 + (GX1 - GX0) * clamp((t - 0.4) / 1.4), a=k0, amp=130, poles=True)
    k1 = appear(t, M[1] - 0.1, 0.45)
    stand(d, W / 2, 1120, JIT * math.sin(2 * math.pi * 6 * t) if k1 > 0 else 0, a=1.0, L=200, hw=20)
    if k1 <= 0: return
    card(d, (40, 780, 1040, 1000), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=4)
    text(d, (W / 2, 845), "Nguồn thật: rất nhanh", 58, NAVY, alpha=k1)
    text(d, (W / 2, 935), "lực đổi chiều liên tục", 58, PURPLE, alpha=k1)

# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
CHOT_S = 5                                  # cau chot: 0-2 s kim lech PHAI (i_slow > 0 -> N -> lech +), giay 5 nam trong 4-6 s -> lai PHAI
def s_end(img, d, t, sc):
    # GD2 vong 4 (kiem-v3): hoi phia lech o giay 5 (kiem hieu "kim doi phia moi lan dong doi chieu"), khong chi phep chia
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 300, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 370, k1, ORANGE)
    text(d, (W / 2, 485), f"Nguồn đổi chiều mỗi {HALF:.0f} s.", 60, INK, alpha=k1)
    text(d, (W / 2, 565), "0 → 2 s: kim lệch phải.", 60, INK, alpha=k1)
    text(d, (W / 2, 645), f"Giây thứ {CHOT_S}: lệch phía nào?", 60, INK, alpha=k1)
    if k1 > 0:   # truc 0-6 s, o 2 s: 0-2 phai, 2-4 trai, 4-6 "?"; moc 5 s; KHONG ve kim o giay 5
        X0, PXS, y0, y1 = 120, 140, 820, 1060
        for q in range(3):
            xa, xb = X0 + q * 2 * PXS, X0 + (q + 1) * 2 * PXS
            fill = (237, 233, 254) if q < 1 else (255, 247, 237)       # kiem-v4: chi o 0-2 s co san, 2-4 va 4-6 deu "?"
            d.rectangle([xa, y0, xb, y1], fill=A(fill, k1), outline=A(NAVY, k1), width=4)
            xc, yc = (xa + xb) / 2, (y0 + y1) / 2
            if q == 0:
                arrow(d, (xc - 70, yc - 30), (xc + 70, yc - 30), A(PURPLE, k1), w=8, head=24)
                text(d, (xc, yc + 55), "phải", 58, PURPLE, alpha=k1)
            else:
                rr = 70 + 50 * math.sin(2 * math.pi * t / 2.4 + (q - 1) * math.pi)   # hai o "?" dap nhip lech pha
                d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.7), k1))
                text(d, (xc, yc), "?", 80, ORANGE, alpha=k1)
        for q in range(4):
            text(d, (X0 + q * 2 * PXS, y1 + 50), str(2 * q), 58, NAVY, alpha=k1)
        xm = X0 + CHOT_S * PXS
        d.polygon([(xm, y0 - 8), (xm - 20, y0 - 44), (xm + 20, y0 - 44)], fill=A(DRED, k1))
        text(d, (xm, y0 - 80), f"{CHOT_S} s", 58, DRED, alpha=k1)
        text(d, (W / 2, 1260), "(theo mô hình)", 58, NAVY, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
          (do["t0"] + T_C1, "tap"), (do["t0"] + T_C2, "tap"),
          (da["t0"] + 0.15, "ding"), (b["t0"] + BAY_ST, "buzz"), (b["t0"] + b["M"][1] + 0.1, "tap"),
          (r["t0"] + r["M"][1] - 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-xoaychieu-01", header="KHTN 9 · THÍ NGHIỆM", footer="Dòng điện xoay chiều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kim cạnh nam châm điện", draw=s_hook, tail=THINK_END, caps=[
   ("Kim cạnh lõi sắt.", 2.6),
   ("Tự đoán.", 4.3)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Lần 1: nguồn một chiều.", 3.0),
   ("Lần 2: nguồn đổi chiều chậm.", 4.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Kim đổi phía mỗi 2 giây.", 3.4),
   ("Đổi theo chiều dòng.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 4.9),
   ("Kim chỉ rung.", 3.3),
   ("Còn bỏ ngỏ.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Cực từ đổi theo chiều dòng.", 2.9),
   ("Quá nhanh: chỉ rung.", 2.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 7.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch vật lí:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
