# Clip: tn-l12-luctu-05 - Electron trong tu truong deu (ban 1, 12/11/2026; dung lai 21/11/2026 theo Viec 4 lo 20:
# cong --do-chu, chu >= 55 px khi ve, Du doan khong nut, Bay hinh tu giai thich, cau chot can mot buoc suy luan).
# Quan niem sai can danh (KE-HOACH-CAI-TIEN-CLIP muc 14): tuong luc tu lam doi toc do (do lon van toc).
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-luctu-05.json (_kiem_so() doi chieu so_lieu_mau):
#   B = 2e-3 T; v = 1, 2, 3 (1e7 m/s) -> r = 2,8 ; 5,7 ; 8,5 cm.  Hang B = 4e-3 T, v = 2e7 -> r 2,8 cm, T 0,9e-8 s
#   KHONG chieu dap so: la cau THU NGHI cuoi clip (T = 2 pi r / v, can buoc "toc do khong doi" -> 0,9e-8 s).
# Du doan (v2, cong B 21/11: doi ca cho khac Cau 6): v = 2e7 m/s, TANG B 2e-3 -> 4e-3 T; nua vong sau toc do? -> van 2e7.
#   Tien hanh chieu hang 2 va 4 (v = 2e7; B 2 -> 4e-3 T; r 5,7 -> 2,8 cm). Hang v = 1, 3 khong dung.
#   Khac Cau 6 (proton, chon dai luong khong doi) va Cau 7 (gap doi v -> r, T) cua bai; khong dung so 0,9.
# Bang chung: vet sang trung khit mot vong (r khong doi); Bay: "gia su nhanh dan" thi vet phai no ra (r = mv/(|q|B)).
# Vat li (kiem bang tich co huong o duoi): nhin doc duong suc, B vao trong trang (-z), electron q < 0.
#   Tai diem ra sung v = +x -> f = q v x B = -y (xuong) -> tam o duoi, electron quay CUNG chieu kim dong ho tren man.
from engine import *

def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
_f = tuple(-c for c in cross((1, 0, 0), (0, 0, -1)))       # q = -|q|, v = +x, B = -z (vao trong trang)
assert _f == (0, -1, 0), _f                                   # luc huong xuong (toan hoc, y len) -> tam duoi diem ra sung

DATA = ((1, 2.8), (2, 5.7), (3, 8.5))      # v (1e7 m/s), r (cm) voi B = 2e-3 T
CHOT = (2, 4, 2.8, 0.9)                    # v, B, r, T -- dap so T KHONG hien
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-luctu-05.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for v, r in DATA: assert any(h[0] == v and h[1] == 2 and abs(h[2] - r) < 1e-9 for h in hang), (v, r)
    assert any(all(abs(a - b) < 1e-9 for a, b in zip(CHOT, h)) for h in hang), CHOT
    assert abs(2 * math.pi * CHOT[2] / 100 / (CHOT[0] * 1e7) / 1e-8 - CHOT[3]) < 0.05
_kiem_so()

PX = 40                                    # px / cm (hinh ve, khong theo ti le that cua bong)
P = (540, 340)                             # diem ra khoi sung
BC, BR = (540, 630), 360                   # bong thuy tinh: y 270..990
GOLD, MAGENTA = (170, 115, 0), (190, 24, 120)
VCOL = (BLUE, GOLD, MAGENTA)
GLASS = (236, 241, 250)
DRED = (185, 28, 28); DGREEN = (10, 110, 50); EMPTY = (148, 140, 128)

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def sym(d, x, y, kind, r=14, color=PURPLE, w=3, alpha=1.0):
    """Ve tay: kind = 'x' (vao trong trang). Font thieu glyph cham-trong-tron."""
    c = A(color, alpha)
    d.ellipse([x - r, y - r, x + r, y + r], outline=c, width=w)
    q = r * 0.6
    d.line([(x - q, y - q), (x + q, y + q)], fill=c, width=w); d.line([(x - q, y + q), (x + q, y - q)], fill=c, width=w)

def center(rcm, c0=P, px=PX): return (c0[0], c0[1] + rcm * px)
def pos(rcm, ph, c0=P, px=PX):
    cx, cy = center(rcm, c0, px); r = rcm * px
    return (cx + r * math.sin(ph), cy - r * math.cos(ph))
def vdir(ph): return (math.cos(ph), math.sin(ph))           # tiep tuyen, cung chieu kim dong ho tren man
def fdir(ph): return (-math.sin(ph), math.cos(ph))          # huong tam

for _ph in (0, 1, 2, 3, 4, 5):                               # f vuong goc v va huong vao tam
    _v, _fd = vdir(_ph), fdir(_ph)
    assert abs(_v[0] * _fd[0] + _v[1] * _fd[1]) < 1e-9
    _p = pos(5.7, _ph); _c = center(5.7)
    assert (_c[0] - _p[0]) * _fd[0] + (_c[1] - _p[1]) * _fd[1] > 0

def bulb(d, field=1.0, rs=()):
    cx, cy = BC
    d.ellipse([cx - BR, cy - BR, cx + BR, cy + BR], fill=GLASS, outline=(160, 168, 190), width=5)
    if field > 0:
        for gx in range(cx - 330, cx + 331, 110):
            for gy in range(cy - 330, cy + 331, 110):
                if math.hypot(gx - cx, gy - cy) > BR - 40: continue
                near = any(abs(math.hypot(gx - center(r)[0], gy - center(r)[1]) - r * PX) < 30 for r in rs)
                if near or (abs(gy - P[1]) < 34 and 380 < gx < 560): continue
                sym(d, gx, gy, "x", 13, PURPLE, 3, alpha=0.75 * field)

def gun(d):
    d.rounded_rectangle([420, P[1] - 15, 512, P[1] + 15], radius=6, fill=NAVY)
    d.polygon([(512, P[1] - 9), (532, P[1] - 5), (532, P[1] + 5), (512, P[1] + 9)], fill=NAVY)

def trail(d, rcm, ph1, col, w=8, a=1.0, c0=P, px=PX):
    if ph1 <= 0.01 or a <= 0: return
    n = max(2, int(ph1 / (2 * math.pi) * 120))
    pts = [pos(rcm, ph1 * i / n, c0, px) for i in range(n + 1)]
    d.line(pts, fill=A(col, 0.28 * a), width=w + 12, joint="curve")
    d.line(pts, fill=A(col, a), width=w, joint="curve")

HIDE = 0.35                                # an electron khi chui sau than sung (pha gan 2pi)
def electron(d, x, y, r=14, a=1.0):
    dot(d, x, y, r, A(NAVY, a), outline=A(WHITE, a))

def vec(d, p, u, L, col, w=8, head=24):
    arrow(d, p, (p[0] + u[0] * L, p[1] + u[1] * L), col, w=w, head=head)

def right_angle(d, p, u, fd, s=22, col=INK, a=1.0):
    q1 = (p[0] + u[0] * s, p[1] + u[1] * s); q2 = (p[0] + fd[0] * s, p[1] + fd[1] * s)
    q3 = (q1[0] + fd[0] * s, q1[1] + fd[1] * s)
    d.line([q1, q3, q2], fill=A(col, a), width=4)

def legend_B(d, y, s, x=110, a=1.0):
    sym(d, x, y, "x", 22, PURPLE, 4, alpha=a)
    text(d, (x + 42, y), s, 56, PURPLE, anchor="lm", alpha=a)

def pill(d, y, s, col, a):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y - 38, W / 2 + pw / 2, y + 38), fill=A(col, a), r=36)
    text(d, (W / 2, y), s, 56, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 165 + i * 155
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan ----------------
RH, RS = 5.7, 2.8                          # vong B = 2e-3 T va B = 4e-3 T (v = 2e7 m/s)
CYC = 2.6                                  # electron ra sung, di 1/4 vong roi mo, lap lai
def s_hook(img, d, t, sc):
    M = sc["M"]; bulb(d, 1.0)
    u = (t % CYC)
    ph = (math.pi / 2) * clamp(u / 1.8); ae = 1.0 - clamp((u - 1.9) / 0.4)
    trail(d, RH, ph, VCOL[1], a=ae)
    gun(d)
    x, y = pos(RH, ph); electron(d, x, y, 16, ae)
    if ae > 0:
        vec(d, (x, y), vdir(ph), 150, A(TEAL, ae), w=9, head=28); vec(d, (x, y), fdir(ph), 110, A(RED, ae), w=9, head=28)
    ka = appear(t, 0.4, 0.4)
    legend_B(d, 1030, "B = 2·10⁻³ T, vào trang", a=ka)
    arrow(d, (70, 1105), (160, 1105), A(TEAL, ka), w=9, head=26)
    text(d, (180, 1105), "v = 2·10⁷ m/s", 56, TEAL, anchor="lm", alpha=ka)
    arrow(d, (640, 1105), (730, 1105), A(RED, ka), w=9, head=26)
    text(d, (750, 1105), "f: lực từ", 56, RED, anchor="lm", alpha=ka)
    a = appear(t, Q_ON, 0.45)
    if a <= 0: return
    y0 = 1150
    card(d, (50, y0, 1030, y0 + 420), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 52, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 160), "Tăng B lên 4·10⁻³ T.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Nửa vòng sau, tốc độ bao nhiêu?", 60, INK, alpha=appear(t, M[1] - 0.1, 0.45))
    seg_bar(d, y0 + 315, t, M[1] + 0.2, sc["T"] - 0.2, PURPLE, appear(t, M[1] - 0.1, 0.45))
Q_ON = 2.9

# ---------------- canh 2: Tien hanh: v giu 2e7, B 2e-3 -> 4e-3 T ----------------
LOOP = 1.6                                 # chu ki (chieu cham) khi B = 2e-3 T; B gap doi -> chu ki nua (vat li dung)
S_BIG, S_SMALL = 0.6, 4.4
ROWS = ((2, 5.7, 3.1), (4, 2.8, 6.0))      # B (1e-3 T), r (cm), luc hien dong
def s_do(img, d, t, sc):
    on = appear(t, 0.3, 0.4)
    small = t >= S_SMALL
    bulb(d, on, rs=(RS,) if t >= S_SMALL + 0.3 else (RH,))
    ks = appear(t, S_SMALL, 0.6)               # tang B: vet lon tat dan, vet nho sang len (chum lien tuc, khong chay electron)
    if t >= S_BIG:
        trail(d, RH, min(2 * math.pi, 2 * math.pi * (t - S_BIG) / LOOP), VCOL[1], a=1.0 - ks)
    if ks > 0:
        gl = 0.75 + 0.25 * math.sin(2 * math.pi * (t - S_SMALL) / 1.2)   # vet sang nhap nhay nhe de hinh khong dung yen
        trail(d, RS, 2 * math.pi, VCOL[2], w=8, a=ks * gl)
    gun(d)
    if S_BIG <= t < S_SMALL:
        ph = (2 * math.pi * (t - S_BIG) / LOOP) % (2 * math.pi)
        if ph < 2 * math.pi - HIDE: electron(d, *pos(RH, ph))
    legend_B(d, 1030, "B vào trang; v = 2·10⁷ m/s", a=appear(t, 0.4, 0.4))
    for j, (b, r, at) in enumerate(ROWS):
        k = appear(t, at, 0.4)
        if k <= 0: continue
        yy = 1130 + 95 * j
        d.line([(70, yy), (150, yy)], fill=A(VCOL[1 + j], k), width=12)
        text(d, (175, yy), f"B = {b}·10⁻³ T → r ≈ {vn(r)} cm", 56, INK, anchor="lm", alpha=k)

# ---------------- canh 3: Dap an + Rut ra (vong B = 4e-3 T) ----------------
GH = (0, math.pi / 2, math.pi, 3 * math.pi / 2)      # bon vi tri "chup" lai
HALF = 1.8                                 # thoi gian nua vong trong canh Ket qua (phong to, chieu cham)
ZC, ZP = (540, 330), 75                   # Ket qua: phong to vong B = 4e-3 T (r 2,8 cm -> 210 px), khong ve sung
def s_dapan(img, d, t, sc):
    M = sc["M"]; bulb(d, 1.0)
    trail(d, RS, 2 * math.pi, VCOL[2], w=8, c0=ZC, px=ZP)
    s0 = 0.5; kf = appear(t, M[1] + 0.1, 0.4)
    gl = 0.6 + 0.4 * math.sin(2 * math.pi * t / 1.2)                 # vet nhap nhay nhe: hinh khong dung yen
    trail(d, RS, 2 * math.pi, VCOL[2], w=8, a=0.35 * gl, c0=ZC, px=ZP)
    for g in GH[:3]:                                   # chi NUA VONG (phong to, chieu cham): khong so duoc chu ki
        kg = appear(t, s0 + HALF * g / math.pi, 0.25)
        if kg <= 0: continue
        x, y = pos(RS, g, ZC, ZP)
        vec(d, (x, y), vdir(g), 115, A(TEAL, kg), w=9, head=26)
        if kf > 0:
            vec(d, (x, y), fdir(g), 85, A(RED, kf), w=9, head=24); right_angle(d, (x, y), vdir(g), fdir(g), s=22, a=kf)
        electron(d, x, y, 14, 0.55 * kg)
    if t >= s0:
        ph = math.pi * clamp((t - s0) / HALF)
        electron(d, *pos(RS, ph, ZC, ZP), 16)
    ka = appear(t, 0.5, 0.4)
    if ka > 0:
        card(d, (110, 1000, 970, 1090), fill=A(NAVY, ka), r=40)
        text(d, (W / 2, 1045), "ĐÁP ÁN · vẫn 2·10⁷ m/s", 58, WHITE, alpha=ka)
    if kf > 0:
        text(d, (W / 2, 1170), "Không sinh công", 62, DRED, alpha=kf)
        arrow(d, (150, 1260), (240, 1260), A(TEAL, kf), w=9, head=26)
        text(d, (262, 1260), "v", 60, TEAL, anchor="lm", alpha=kf)
        arrow(d, (440, 1260), (530, 1260), A(RED, kf), w=9, head=26)
        text(d, (552, 1260), "f: lực từ", 56, RED, anchor="lm", alpha=kf)

# ---------------- canh 4: Bay (hai khung) + chua noi duoc ----------------
C1, C2 = (540, 505), (540, 975)
def spiral_pt(ph): r = 60 + 9.5 * ph; return (C1[0] + r * math.sin(ph), C1[1] - r * math.cos(ph))
SP_END = 4 * math.pi
def s_bay(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.3, 0.4)
    card(d, (40, 215, 1040, 690), fill=A(WHITE, k1), outline=A(DRED, k1), w=6)
    for gx, gy in ((970, 600), (970, 420), (110, 600)): sym(d, gx, gy, "x", 15, PURPLE, 3, alpha=0.75 * k1)
    legend_B(d, 265, "B vào trang", x=680, a=k1)
    u = clamp(((t - 0.3) % 3.4) / 3.0)                 # electron chay theo xoan oc (gia su), lap lai
    ph = SP_END * u; n = 160
    pts = [spiral_pt(SP_END * i / n) for i in range(n + 1)]
    for i in range(0, n, 2): d.line([pts[i], pts[i + 1]], fill=A(DRED, 0.8 * k1), width=6)   # net dut: gia su
    x, y = spiral_pt(ph); electron(d, x, y, 13, k1)
    text(d, (70, 265), "✗ giả sử: vệt nở ra", 58, DRED, anchor="lm", alpha=k1)
    k2 = appear(t, M[1] + 0.1, 0.4)
    if k2 > 0:
        card(d, (40, 715, 1040, 1195), fill=A(WHITE, k2), outline=A(DGREEN, k2), w=6)
        for gx, gy in ((110, 1100), (970, 1100), (970, 880)): sym(d, gx, gy, "x", 15, PURPLE, 3, alpha=0.75 * k2)
        R = 150; d.ellipse([C2[0] - R, C2[1] - R, C2[0] + R, C2[1] + R], outline=A(VCOL[1], 0.28 * k2), width=22)
        d.ellipse([C2[0] - R, C2[1] - R, C2[0] + R, C2[1] + R], outline=A(VCOL[1], k2), width=8)
        ph2 = 2 * math.pi * (t - M[1]) / LOOP
        electron(d, C2[0] + R * math.sin(ph2), C2[1] - R * math.cos(ph2), 14, k2)
        text(d, (70, 765), "✓ thật: khép kín", 58, DGREEN, anchor="lm", alpha=k2)
    k3 = appear(t, M[2] + 0.1, 0.4)
    if k3 > 0:
        card(d, (40, 1225, 1040, 1470), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, 1290), "Chưa nói được", 60, NAVY, alpha=k3)
        text(d, (W / 2, 1395), "Khi v xiên góc với B?", 58, INK, alpha=k3)

# ---------------- canh 5: Chot (phu de) + THU NGHI ----------------
PXE = 60; CE = (540, 560)                  # hinh phong to rieng (r = 2,8 cm -> 168 px), khong cung ti le canh truoc
def s_end(img, d, t, sc):
    k1 = appear(t, 0.2, 0.4)
    card(d, (40, 210, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 275, "THỬ NGHĨ", ORANGE, k1)
    text(d, (W / 2, 385), "Một vòng mất bao lâu?", 62, ORANGE, alpha=k1)
    rp = CHOT[2] * PXE; cx, cy = CE[0], CE[1] + rp      # electron o dinh vong, vong o duoi
    for gx, gy in ((190, 600), (890, 600), (190, 900), (890, 900)): sym(d, gx, gy, "x", 15, PURPLE, 3, alpha=0.75 * k1)
    gl = 0.18 + 0.14 * (0.5 + 0.5 * math.sin(2 * math.pi * t / 1.4))      # vet sang nhap nhay nhe (khong chay vong)
    d.ellipse([cx - rp, cy - rp, cx + rp, cy + rp], outline=A(VCOL[1], gl * k1 * 2), width=24)
    d.ellipse([cx - rp, cy - rp, cx + rp, cy + rp], outline=A(VCOL[1], k1), width=8)
    kd = appear(t, 2.8, 0.4)
    if kd > 0:
        d.line([(cx, cy), (cx + rp * 0.707, cy + rp * 0.707)], fill=A(INK, kd), width=5); dot(d, cx, cy, 7, A(INK, kd))
    vec(d, CE, (1, 0), 150, A(TEAL, k1), w=9, head=28); electron(d, CE[0], CE[1], 15, k1)
    text(d, (CE[0] + 185, CE[1]), "v", 60, TEAL, alpha=k1)
    if kd > 0:
        text(d, (W / 2, 1010), "B = 4·10⁻³ T, v = 2·10⁷ m/s", 58, INK, alpha=kd)
        text(d, (W / 2, 1100), "vòng sáng r ≈ 2,8 cm", 58, VCOL[1], alpha=kd)
    kh = appear(t, 5.8, 0.45)
    if kh > 0:
        card(d, (90, 1180, 990, 1300), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1240), "Gợi ý: đổi r ra mét", 56, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    return ([(h["t0"] + Q_ON, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + S_BIG, "tap"), (do["t0"] + S_SMALL, "tick")]
            + [(da["t0"] + 0.5, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-luctu-05", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Lực từ · Cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Electron trong từ trường", draw=s_hook, tail=0.2, caps=[
   ("Electron bay vào từ trường đều.", 5.2),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bật B: vệt sáng là vòng tròn.", 3.6),
   ("Tăng B gấp đôi: vòng nhỏ lại.", 5.7)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Vòng khép kín: bán kính không đổi.", 3.8),
   ("Lực từ luôn vuông góc v.", 4.1)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Dễ tưởng: lực từ làm nhanh dần.", 3.8),
   ("Vòng nào cũng trùng.", 3.6),
   ("Chỉ thấy vệt sáng cả chùm.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Lực từ chỉ đổi hướng bay.", 7.8)]),
])
