# Clip: tn-l10-biendang-03 - Hai lo xo, cung mot qua nang (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-biendang-03.json:
#   so_lieu_mau: lo xo day to k = 50 N/m, dl = 1,96 cm ; lo xo day manh k = 25 N/m, dl = 3,92 cm (qua 100 g)
#   mo_hinh.gia_thiet: g = 9,8 m/s2, trong gioi han dan hoi -> P = 0,1 . 9,8 = 0,98 N (the so ngay tren man)
#   tham_so: F toi da 3 N (cau THU NGHI dung 1,5 N - trong thang).
# Hinh: 60 px moi cm (do dan ve dung ti le so kho), vach 0 cua thuoc ngang dau duoi luc chua treo -> so doc = dl.
#   Hai lo xo cung chieu dai tu nhien l0 (net dut ngang), chi khac do day day (cung mau, khong goi y dap an).
# Canh: Du doan (K10, khong nut A-D) -> Tien hanh (treo lan luot, kim thuoc dong pha, bang) + DAP AN
#       -> Rut ra (2 luc cung dat len qua nang can bang, k = F/dl tung dong mot nhip, chua noi duoc)
#       -> Bay (dan nhieu hon = bi keo manh hon?) -> Chot + THU NGHI (3 cm -> ? N: gia tri chua hien, chieu nguoc).
from engine import *

G = 9.8
M_KG = 0.1
P = 0.98                                         # = 0,1 . 9,8
DL = (1.96, 3.92)                                # so_lieu_mau (cm)
KK = (50, 25)                                    # so_lieu_mau (N/m)
NAME = ("dây to", "dây mảnh")
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")

BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); RULER = (255, 241, 205)

_TI = {}
def TI(size):                                    # Times Bold Italic cho ky hieu l (SF: l giong I)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def sym(d, x, y, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chu co chi so duoi: 'F_{đh}', 'l_{0}'; chi so >= 40 px; 'l' ve bang Times nghieng."""
    segs = []
    for p in [p for p in re.split(r"(_\{[^}]*\})", s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], F(max(40, int(size * 0.78))), size * 0.26))
        else:
            for q in [q for q in re.split(r"((?<=Δ)l|(?<![^\W\d_])l(?![^\W\d_]))", p) if q]:
                segs.append((q, TI(int(size * 1.1)) if q == "l" else F(size), 0))
    tot = sum(tw(d, t, f) for t, f, _ in segs)
    xx = x - tot / 2 if anchor == "m" else (x - tot if anchor == "r" else x)
    for t, f, dy in segs:
        dtext(d, (xx, y + dy), t, f, color, alpha, "lm"); xx += tw(d, t, f)

def ptext(d, cx, y, s, size, color=INK, maxw=420, alpha=1.0, lh=1.22):
    f = F(size); ls = wrap(d, s, f, maxw)
    for j, l in enumerate(ls): dtext(d, (cx, y + j * size * lh), l, f, color, alpha)
    return y + len(ls) * size * lh

# ---------------- gia treo, hai lo xo, hai thuoc ----------------
SX = (180, 430)                                  # truc hai lo xo
TOP, Y0N, PX = 320, 640, 90                      # moc tren; dau duoi khi chua treo; px moi cm
RX = (250, 500)                                  # mep trai hai thuoc
MW, MH = 124, 84                                 # qua nang
BASE = 1560                                      # mat de gia treo
FREE_Y = BASE - 18 - MH - 4                      # qua nang nam tren de
COIL = ((8, 30, 9), (12, 22, 4))                 # (so vong, bien do, net): day to it vong net day; day manh nhieu vong net manh

def spring(d, x, yb, thick, alpha=1.0):
    lead = 26; n, amp, w = COIL[0 if thick else 1]
    pts = [(x, TOP), (x, TOP + lead)]
    for i in range(1, 2 * n):
        pts.append((x + (amp if i % 2 else -amp), lerp(TOP + lead, yb - lead, i / (2 * n))))
    pts += [(x, yb - lead), (x, yb)]
    d.line(pts, fill=A(NAVY, alpha), width=w, joint="curve")
    d.ellipse([x - 9, yb - 4, x + 9, yb + 14], outline=A(NAVY, alpha), width=4)

def mass(d, cx, ytop, alpha=1.0):
    d.arc([cx - 13, ytop, cx + 13, ytop + 24], 180, 360, fill=A(NAVY, alpha), width=5)
    d.line([(cx, ytop + 10), (cx, ytop + 20)], fill=A(NAVY, alpha), width=5)
    d.rounded_rectangle([cx - MW / 2, ytop + 18, cx + MW / 2, ytop + 18 + MH], radius=12,
                        fill=A(BRASS, alpha), outline=A(BRASS_D, alpha), width=3)
    text(d, (cx, ytop + 18 + MH / 2), "100 g", 40, WHITE, alpha=alpha)

def ruler(d, rx, dl=None):
    d.rectangle([rx, Y0N - 22, rx + 44, Y0N + 5 * PX + 22], fill=RULER, outline=BRASS_D, width=3)
    for k in range(51):
        y = Y0N + k * PX / 10; L = 26 if k % 10 == 0 else (17 if k % 5 == 0 else 9)
        d.line([(rx, y), (rx + L, y)], fill=NAVY, width=3 if k % 10 == 0 else 2)
    for c in range(6): text(d, (rx + 54, Y0N + c * PX), str(c), 40, INK, anchor="lm")
    text(d, (rx + 22, Y0N + 5 * PX + 56), "cm", 40, INK)
    if dl is not None:                           # kim do: ngang dau duoi lo xo
        y = Y0N + dl * PX
        d.line([(rx - 40, y), (rx + 30, y)], fill=RED, width=5)
        d.polygon([(rx + 2, y), (rx - 16, y - 9), (rx - 16, y + 9)], fill=RED)

def rig(d, dls, masses=(), free_mass=None, labels=True, rulers=True):
    """dls: do dan hien tai (cm) cua hai lo xo. masses: chi so lo xo dang treo qua. free_mass: (x, ytop, alpha)."""
    d.rounded_rectangle([28, 296, 48, BASE], radius=6, fill=(170, 175, 190))
    d.rounded_rectangle([28, 292, 585, 318], radius=8, fill=(150, 155, 172))
    d.rounded_rectangle([14, BASE, 585, BASE + 42], radius=10, fill=(176, 124, 74))
    # chieu dai tu nhien: net dut ngang dau duoi khi chua treo + ngoac l0 chung
    for xx in range(70, 560, 30): d.line([(xx, Y0N), (xx + 16, Y0N)], fill=GRAY, width=3)
    d.line([(80, TOP), (80, Y0N)], fill=INK, width=4)
    for y in (TOP, Y0N): d.line([(70, y), (92, y)], fill=INK, width=4)
    d.rectangle([94, 440, 140, 500], fill=BG)
    sym(d, 116, 470, "l_{0}", 46, INK)
    for i in (0, 1):
        if labels: text(d, (SX[i], 262), NAME[i], 38, INK)
        if rulers: ruler(d, RX[i], dls[i])
        yb = Y0N + dls[i] * PX
        spring(d, SX[i], yb, i == 0)
        if i in masses: mass(d, SX[i], yb + 4)
    if free_mass: mass(d, free_mass[0], free_mass[1], free_mass[2])

# ---------------- dong hoc treo qua (do dan dao dong tat dan roi dung) ----------------
def osc(D, tt):  return D * (1 - math.exp(-3.4 * tt) * math.cos(2 * math.pi * 1.4 * tt))
def back0(D, tt): return D * math.exp(-4.0 * tt) * math.cos(2 * math.pi * 1.4 * tt)
HANG, SETTLE, MOVE = 0.6, 1.6, 0.9

def state(t, sc):
    """-> (dl1, dl2, masses, free_mass, doc: list cac (i, so doc) da on dinh)."""
    M = sc["M"]; a1, a2 = M[0] + 0.3, M[1] + 0.2
    dl, masses, fm_, doc = [0.0, 0.0], (), None, []
    if t < a1:                                   # qua nang dang o tren de
        fm_ = (310, FREE_Y, 1.0)
    elif t < a1 + HANG:                          # dua qua len moc lo xo 1
        k = ease((t - a1) / HANG); fm_ = (lerp(310, SX[0], k), lerp(FREE_Y, Y0N + 4, k), 1.0)
    elif t < a2:
        tt = t - a1 - HANG; dl[0] = osc(DL[0], tt); masses = (0,)
        if tt > SETTLE: doc = [(0, DL[0])]
    elif t < a2 + MOVE:                          # chuyen qua sang lo xo 2; lo xo 1 ve lai l0
        tau = t - a2; k = ease(tau / MOVE); dl[0] = back0(DL[0], tau)
        y1, y2 = Y0N + DL[0] * PX + 4, Y0N + 4
        fm_ = (lerp(SX[0], SX[1], k), lerp(y1, y2, k) - 90 * math.sin(math.pi * k), 1.0); doc = [(0, DL[0])]
    else:
        tau = t - a2; dl[0] = back0(DL[0], tau); tt = tau - MOVE
        dl[1] = osc(DL[1], tt); masses = (1,); doc = [(0, DL[0])]
        if tt > SETTLE: doc.append((1, DL[1]))
    if abs(dl[0]) < 0.004: dl[0] = 0.0
    return dl, masses, fm_, doc

def bottom_note(d, a=1.0):                       # cot phai, duoi the dap an
    card(d, (605, 1190, 1035, 1480), fill=A(WHITE, a), outline=A(LIGHT, a), w=4)
    yy = ptext(d, 820, 1250, "Vạch 0 ngang đầu dưới lúc chưa treo", 40, INK, maxw=380, alpha=a)
    sym(d, 820, yy + 10, "→ số đọc = Δl", 40, BLUE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, (0.0, 0.0), free_mass=(310, FREE_Y, 1.0))
    M = sc["M"]; k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 300 + (1 - k) * 30
    card(d, (605, y0, 1035, y0 + 1180), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(42)) + 56
    card(d, (820 - pw / 2, y0 + 30, 820 + pw / 2, y0 + 98), fill=A(PURPLE, k), r=32)
    text(d, (820, y0 + 64), "Dự đoán", 42, WHITE, alpha=k)
    yy = ptext(d, 820, y0 + 190, "Treo lần lượt quả 100 g.", 46, INK, maxw=390, alpha=k)
    ptext(d, 820, yy + 40, "So sánh độ dãn hai lò xo?", 46, INK, maxw=390, alpha=k)
    for j, nm in enumerate(NAME):                # hai o so doc chua biet, cung mau cung co
        yb = y0 + 640 + j * 170
        text(d, (820, yb - 62), nm, 42, INK, alpha=k)
        card(d, (690, yb - 30, 950, yb + 60), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=20, w=4)
        sym(d, 820, yb + 15, "Δl = ?", 44, PURPLE, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([640, y0 + 1110, 1000, y0 + 1126], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([640, y0 + 1110, 640 + 360 * (1 - q), y0 + 1126], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    dl, masses, fm_, doc = state(t, sc)
    rig(d, dl, masses, fm_)
    bottom_note(d)
    card(d, (605, 300, 1035, 530), fill=WHITE, outline=LIGHT, r=28, w=4)
    cur = 1 if (masses == (1,) or (fm_ and t > sc["M"][1])) else 0
    text(d, (820, 360), NAME[cur], 42, BLUE)
    got = [v for i, v in doc if i == cur]
    sym(d, 820, 460, f"Δl = {fm(got[0])} cm" if got else "Δl = đợi…", 54, RED if got else MUTED)
    card(d, (605, 565, 1035, 880), fill=WHITE, outline=NAVY, w=4)
    xs = (720, 925)
    text(d, (xs[0], 620), "lò xo", 40, INK); sym(d, xs[1], 620, "Δl (cm)", 40, INK)
    d.line([(625, 655), (1015, 655)], fill=LIGHT, width=4)
    for i, v in doc:
        y = 710 + i * 95
        text(d, (xs[0], y), NAME[i], 42, BLUE); text(d, (xs[1], y), fm(v), 44, RED)
    kc = appear(t, sc["M"][2], 0.4)
    if kc > 0:
        card(d, (605, 915, 1035, 1150), fill=A((220, 252, 231), kc), outline=A(GREEN, kc), r=26, w=4)
        text(d, (820, 970), "ĐÁP ÁN", 42, GREEN, alpha=kc)
        ptext(d, 820, 1040, "dây mảnh dãn nhiều hơn", 42, INK, maxw=380, alpha=kc)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.2)
    card(d, (40, 270, 1040, 920), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    cx, ytop, ybot = 250, 520, 630               # qua nang (vat duoc xet), ve rieng
    d.rounded_rectangle([cx - 90, ytop, cx + 90, ybot], radius=16, fill=A(BRASS, a), outline=A(BRASS_D, a), width=4)
    text(d, (cx, (ytop + ybot) / 2), "100 g", 42, WHITE, alpha=a)
    L = 165                                      # 0,98 N -> 165 px, hai mui ten bang nhau
    ka = appear(t, 0.7, 0.4)
    if ka > 0:
        arrow(d, (cx, ytop), (cx, ytop - L), A(GREEN, ka), w=9, head=28)
        sym(d, cx + 30, ytop - L + 30, "F_{đh}", 46, GREEN, alpha=ka, anchor="l")
        arrow(d, (cx, ybot), (cx, ybot + L), A(RED, ka), w=9, head=28)
        sym(d, cx + 30, ybot + L - 30, "P", 46, RED, alpha=ka, anchor="l")
        dot(d, cx, ytop, 9, A(GREEN, ka)); dot(d, cx, ybot, 9, A(RED, ka))
    kb = appear(t, 1.4, 0.4)
    if kb > 0:
        sym(d, 500, 360, "F_{đh}: lò xo kéo lên", 40, GREEN, alpha=kb, anchor="l")
        sym(d, 500, 440, "P: Trái Đất hút xuống", 40, RED, alpha=kb, anchor="l")
        text(d, (500, 540), "Cùng đặt lên quả nặng", 40, INK, anchor="lm", alpha=kb)
    kc = appear(t, M[0] + 1.6, 0.4)
    if kc > 0:
        text(d, (500, 680), "m = 100 g = 0,1 kg", 40, MUTED, anchor="lm", alpha=kc)
        sym(d, W / 2, 875, "F_{đh} = P = m·g = 0,1 · 9,8 = 0,98 N", 44, INK, alpha=kc)
    rows = [("k = F_{đh} : Δl   (độ cứng)", None, BLUE),
            ("dây to: k = 0,98 : 0,0196 = 50 N/m", "1,96 cm = 0,0196 m", INK),
            ("dây mảnh: k = 0,98 : 0,0392 = 25 N/m", "3,92 cm = 0,0392 m", INK)]
    for j, (s1, s2, col) in enumerate(rows):     # moi dong mot nhip ~1,8 s
        kr = appear(t, M[1] + 0.1 + j * 1.8, 0.4)
        if kr <= 0: continue
        y = 975 + (0 if j == 0 else 75 + (j - 1) * 135)
        sym(d, W / 2, y, s1, 42, col, alpha=kr)
        if s2: text(d, (W / 2, y + 56), s2, 40, MUTED, alpha=kr)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1320 + (1 - k3) * 30
        card(d, (40, y1, 1040, y1 + 280), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 55), "Chưa nói được gì?", 44, NAVY, alpha=k3)
        ctext(d, y1 + 140, "Chỉ một lực 0,98 N:", 42, INK, alpha=k3)
        ctext(d, y1 + 210, "chưa thấy k không đổi khi đổi lực", 42, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1, 0.4)
    card(d, (40, 265, 1040, 470), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 345), fill=A(RED, a), r=30)
    text(d, (W / 2, 315), "Bẫy", 40, WHITE, alpha=a)
    ctext(d, 410, "Dãn nhiều hơn → bị kéo mạnh hơn?", 44, INK, maxw=920, alpha=a)
    # hai lo xo dang treo qua, da dung yen (cung thang 90 px/cm nhu canh do, chieu dai tu nhien nhu nhau)
    BT, BN = 575, 775                            # moc tren; dau duoi luc chua treo
    for i in (0, 1):
        x = (300, 760)[i]; yb = BN + DL[i] * PX
        text(d, (x, 520), NAME[i], 40, INK, alpha=a)
        d.line([(x - 70, BT - 6), (x + 70, BT - 6)], fill=A((150, 155, 172), a), width=12)
        lead = 26; n, amp, w = COIL[i]
        pts = [(x, BT), (x, BT + lead)] + [(x + (amp if j % 2 else -amp), lerp(BT + lead, yb - lead, j / (2 * n))) for j in range(1, 2 * n)] + [(x, yb - lead), (x, yb)]
        d.line(pts, fill=A(NAVY, a), width=w, joint="curve")
        mass(d, x, yb + 4, alpha=a)
        for xx in range(x - 120, x + 110, 28): d.line([(xx, BN), (xx + 14, BN)], fill=A(GRAY, a), width=3)
        bx = x + 110                             # ngoac do dan tu net dut (dau duoi luc chua treo) toi dau duoi
        d.line([(bx, BN), (bx, yb)], fill=A(RED, a), width=4)
        for y in (BN, yb): d.line([(bx - 10, y), (bx + 10, y)], fill=A(RED, a), width=4)
        sym(d, bx + 18, (BN + yb) / 2, f"{fm(DL[i])} cm", 40, RED, alpha=a, anchor="l")
    ok = appear(t, M[1] + 2.1, 0.45)             # dap an bay: tre >= 2 s sau "Co dung khong?"
    if ok > 0:
        for i in (0, 1):                         # luc dan hoi len qua nang (dat o mep tren qua), bang nhau
            x = (300, 760)[i]; ym = BN + DL[i] * PX + 4 + 18
            arrow(d, (x - 46, ym), (x - 46, ym - 150), A(GREEN, ok), w=8, head=24)
            sym(d, x - 62, ym - 110, "0,98 N", 40, GREEN, alpha=ok, anchor="r")
        card(d, (40, 1270, 1040, 1500), fill=A((220, 252, 231), ok), outline=A(GREEN, ok), w=5)
        text(d, (W / 2, 1340), "✓ Không: cùng quả nặng, cùng 0,98 N", 42, GREEN, alpha=ok)
        ctext(d, 1430, "Khác ở k, không ở lực", 44, INK, alpha=ok)

# ---------------- canh 5: chot ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def pic(d, t, k):                            # du kien + hinh cau hoi (lo xo day to dan 3 cm, luc chua biet)
        kg = appear(t, sc["M"][0] + 0.9, 0.5) * k
        if kg <= 0: return
        card(d, (110, 945, 970, 1070), fill=A((239, 246, 255), kg), r=24)
        sym(d, W / 2, 980, "dây to: k = 50 N/m", 42, BLUE, alpha=kg)
        text(d, (W / 2, 1035), "Giả sử k không đổi khi đổi lực", 40, INK, alpha=kg)
        kh = appear(t, sc["M"][0] + 2.0, 0.5) * k
        if kh <= 0: return
        x, top, nat = 470, 1100, 1210; yb = nat + 3 * PX      # cung thang 90 px/cm
        d.line([(x - 80, top - 6), (x + 80, top - 6)], fill=A((150, 155, 172), kh), width=12)
        n, amp, w = COIL[0]
        pts = [(x, top), (x, top + 22)] + [(x + (amp if j % 2 else -amp), lerp(top + 22, yb - 22, j / (2 * n))) for j in range(1, 2 * n)] + [(x, yb - 22), (x, yb)]
        d.line(pts, fill=A(NAVY, kh), width=w, joint="curve")
        for xx in range(x - 130, x + 120, 28): d.line([(xx, nat), (xx + 14, nat)], fill=A(GRAY, kh), width=3)
        bx = x + 120
        d.line([(bx, nat), (bx, yb)], fill=A(RED, kh), width=4)
        for y in (nat, yb): d.line([(bx - 10, y), (bx + 10, y)], fill=A(RED, kh), width=4)
        text(d, (bx + 20, (nat + yb) / 2), "3 cm", 40, RED, anchor="lm", alpha=kh)
        d.arc([x - 13, yb + 2, x + 13, yb + 24], 180, 360, fill=A(NAVY, kh), width=5)
        d.rounded_rectangle([x - 62, yb + 18, x + 62, yb + 100], radius=12, fill=A(BRASS, kh), outline=A(BRASS_D, kh), width=3)
        text(d, (x, yb + 59), "? N", 44, WHITE, alpha=kh)
    chot_hoi(d, t, sc, "Cùng lực: k lớn dãn ít, k nhỏ dãn nhiều",
             "Lò xo dây to dãn 3 cm. Vật treo nặng bao nhiêu N?", body=pic)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][2], "ding"), (r["t0"] + r["M"][2] - 0.1, "tap"),
            (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1] + 2.1, "ding"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-biendang-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Biến dạng của vật rắn · thachlab.id.vn", scenes=[
 dict(key="hook", title="Hai lò xo, một quả nặng", draw=s_hook, tail=0.5, caps=[
   ("Cùng chiều dài tự nhiên.", 3.0),
   ("Dừng video, tự đoán.", 5.2)]),
 dict(key="do", title="Treo lần lượt, đọc thước", draw=s_do, tail=0.4, caps=[
   ("Treo vào lò xo dây to.", 3.6),
   ("Chuyển sang lò xo dây mảnh.", 4.4),
   ("Cùng quả nặng, dãn gấp đôi.", 3.4)]),
 dict(key="rut", title="Vì sao dãn khác nhau?", draw=s_rut, tail=0.5, caps=[
   ("Đứng yên: hai lực cân bằng.", 3.4),
   ("Tính độ cứng k.", 4.4),
   ("Chưa nói được gì?", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Cùng quả 100 g.", 3.0),
   ("Có đúng không?", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])
