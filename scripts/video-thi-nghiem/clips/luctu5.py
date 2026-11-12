# Clip: tn-l12-luctu-05 - Electron trong tu truong deu: quy dao tron (ban 1, 12/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-luctu-05.json (so_lieu_mau, "so lieu minh hoa"):
#   B = 2e-3 T; v = 1, 2, 3 (1e7 m/s) -> r = 2,8 ; 5,7 ; 8,5 cm ; T = 1,8e-8 s ca ba lan.
#   Hang B = 4e-3 T (r 2,8 cm; T 0,9e-8 s) KHONG chieu: la dap so cau THU NGHI cuoi clip.
# Du doan (khung ben canh, K10 khong ve nut): tang v tu 1e7 len 3e7 m/s, thoi gian mot vong? -> khong doi.
# Vat li (kiem bang tich co huong o duoi): nhin doc duong suc, B vao trong trang (-z), electron q < 0.
#   Tai diem ra sung v = +x -> f = q v x B = -y (xuong) -> tam o duoi, electron quay CUNG chieu kim dong ho tren man.
#   f luon huong tam, vuong goc v: khong sinh cong, toc do khong doi; T = 2 pi r / v khong phu thuoc v.
from engine import *

def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
_f = tuple(-c for c in cross((1, 0, 0), (0, 0, -1)))       # q = -|q|, v = +x, B = -z (vao trong trang)
assert _f == (0, -1, 0), _f                                   # luc huong xuong (toan hoc, y len) -> tam duoi diem ra sung

PX = 32                                    # px / cm (hinh ve, khong theo ti le that cua bong)
P = (540, 340)                             # diem ra khoi sung
BC, BR = (540, 640), 380                   # bong thuy tinh
DATA = ((1, 2.8), (2, 5.7), (3, 8.5))      # v (1e7 m/s), r (cm) -- T ~ 1,8e-8 s ca ba
VCOL = (BLUE, ORANGE, GREEN)
NOTE = (70, 75, 95)
GLASS = (236, 241, 250)

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def sym(d, x, y, kind, r=14, color=PURPLE, w=3, alpha=1.0):
    """Ve tay: kind = 'x' (vao trong trang), 'o' (ra khoi trang). Font thieu glyph cham-trong-tron."""
    c = A(color, alpha)
    d.ellipse([x - r, y - r, x + r, y + r], outline=c, width=w)
    if kind == "o": d.ellipse([x - r * 0.3, y - r * 0.3, x + r * 0.3, y + r * 0.3], fill=c)
    else:
        q = r * 0.6
        d.line([(x - q, y - q), (x + q, y + q)], fill=c, width=w); d.line([(x - q, y + q), (x + q, y - q)], fill=c, width=w)

def center(rcm): return (P[0], P[1] + rcm * PX)
def pos(rcm, ph):
    cx, cy = center(rcm); r = rcm * PX
    return (cx + r * math.sin(ph), cy - r * math.cos(ph))
def vdir(ph): return (math.cos(ph), math.sin(ph))           # tiep tuyen, cung chieu kim dong ho tren man
def fdir(ph): return (-math.sin(ph), math.cos(ph))          # huong tam

# kiem: tai moi pha, f vuong goc v va huong vao tam
for _ph in (0, 1, 2, 3, 4, 5):
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
    # sung electron (ve nho, ben trai diem ra)
    d.rounded_rectangle([420, P[1] - 15, 512, P[1] + 15], radius=6, fill=NAVY)
    d.polygon([(512, P[1] - 9), (532, P[1] - 5), (532, P[1] + 5), (512, P[1] + 9)], fill=NAVY)

def trail(d, rcm, ph1, col, w=8):
    if ph1 <= 0.01: return
    n = max(2, int(ph1 / (2 * math.pi) * 120))
    pts = [pos(rcm, ph1 * i / n) for i in range(n + 1)]
    d.line(pts, fill=A(col, 0.28), width=w + 12, joint="curve")
    d.line(pts, fill=col, width=w, joint="curve")

def electron(d, x, y, r=13):
    dot(d, x, y, r, NAVY, outline=WHITE)

def vec(d, p, u, L, col, w=7, head=20):
    arrow(d, p, (p[0] + u[0] * L, p[1] + u[1] * L), col, w=w, head=head)

def legend_B(d, y, on=True, full=True):
    if on:
        sym(d, 150, y, "x", 18, PURPLE, 4)
        text(d, (184, y), "B = 2·10⁻³ T, vào trong trang" if full else "B = 2·10⁻³ T", 40, PURPLE, anchor="lm")
    else:
        text(d, (W / 2, y), "B = 0", 40, NOTE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; bulb(d, 1.0, rs=(2.8,))
    ph = 2 * math.pi * ((t / 2.4) % 1.0)
    trail(d, 2.8, 2 * math.pi, VCOL[0])
    x, y = pos(2.8, ph); electron(d, x, y)
    vec(d, (x, y), vdir(ph), 120, TEAL); vec(d, (x, y), fdir(ph), 74, RED)
    legend_B(d, 1060)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0:
        k = appear(t, 0.5, 0.5)
        card(d, (60, 1110, 1020, 1250), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
        arrow(d, (130, 1180), (230, 1180), A(TEAL, k), w=7, head=20); text(d, (252, 1180), "v", 42, TEAL, anchor="lm", alpha=k)
        arrow(d, (380, 1180), (480, 1180), A(RED, k), w=7, head=20)
        text(d, (502, 1180), "f: lực từ lên electron", 42, RED, anchor="lm", alpha=k)
        return
    y0 = 1110 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 400), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Tăng v từ 1·10⁷ lên 3·10⁷ m/s.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 255), "Thời gian đi hết một vòng đổi thế nào?", 46, INK, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 340, 940, y0 + 354], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 340, 140 + 800 * (1 - p), y0 + 354], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
LOOP, GAP = 1.3, 1.6
def loops(sc):
    t_on = sc["M"][1]
    return t_on, [t_on + 0.4 + GAP * k for k in range(3)]

COLX = ((210, "v (10⁷ m/s)"), (560, "r (cm)"), (880, "T (10⁻⁸ s)"))
def table(d, y0, ks, alpha=1.0):
    card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, s in COLX: text(d, (x, y0 + 46), s, 40, NOTE, bold=False, alpha=alpha)
    d.line([(70, y0 + 84), (1010, y0 + 84)], fill=A(LIGHT, alpha), width=3)
    for j, ((v, r), k) in enumerate(zip(DATA, ks)):
        if k <= 0: continue
        yy = y0 + 84 + 76 * (j + 0.5) + 4
        dot(d, 105, yy, 14, A(VCOL[j], k))
        text(d, (210, yy), str(v), 44, INK, alpha=k)
        text(d, (560, yy), "≈ " + vn(r), 44, INK, alpha=k)
        text(d, (880, yy), "≈ 1,8", 44, INK, alpha=k)
    text(d, (1020, y0 + 370), "minh hoạ", 40, NOTE, bold=False, anchor="rm", alpha=alpha)

def s_do(img, d, t, sc):
    t_on, st = loops(sc)
    on = appear(t, t_on - 0.1, 0.4)
    done = [r for r, s in zip((2.8, 5.7, 8.5), st) if t >= s]
    bulb(d, on, rs=tuple(done))
    if t < t_on:                                   # chua co B: vet thang tu sung toi thanh bong
        xe = BC[0] + math.sqrt(BR ** 2 - (P[1] - BC[1]) ** 2) - 6
        u = (t % 1.2) / 1.2
        d.line([P, (lerp(P[0], xe, min(1, u * 1.6)), P[1])], fill=A(VCOL[0], 0.3), width=20)
        d.line([P, (lerp(P[0], xe, min(1, u * 1.6)), P[1])], fill=VCOL[0], width=8)
        electron(d, lerp(P[0], xe, min(1, u * 1.6)), P[1])
    for j, (rc, s) in enumerate(zip((2.8, 5.7, 8.5), st)):
        if t < s: continue
        ph = 2 * math.pi * clamp((t - s) / LOOP)
        trail(d, rc, ph, VCOL[j])
        if ph < 2 * math.pi - 1e-6:
            x, y = pos(rc, ph); electron(d, x, y)
    legend_B(d, 1060, on=t >= t_on)
    table(d, 1110, [appear(t, s + LOOP, 0.35) for s in st])

# ---------------- canh 3: Dap an + Rut ra ----------------
LAP = 2.2
def s_dapan(img, d, t, sc):
    M = sc["M"]; bulb(d, 1.0, rs=(2.8, 5.7, 8.5))
    ph = 2 * math.pi * (max(0.0, t - 0.4) / LAP % 1.0)
    for j, (v, rc) in enumerate(DATA):
        trail(d, rc, 2 * math.pi, VCOL[j], w=6)
    for j, (v, rc) in enumerate(DATA):
        x, y = pos(rc, ph); vec(d, (x, y), vdir(ph), 44 * v, TEAL, w=6, head=18); electron(d, x, y)
    legend_B(d, 1060, full=False)
    ka = appear(t, 0.4 + LAP, 0.4)
    if ka > 0:
        s = "ĐÁP ÁN · T không đổi"
        pw = tw(d, s, F(40)) + 56
        card(d, (W / 2 - pw / 2, 1112, W / 2 + pw / 2, 1180), fill=A(NAVY, ka), r=34)
        text(d, (W / 2, 1146), s, 40, WHITE, alpha=ka)
    k1 = appear(t, M[1] - 0.3, 0.45)
    card(d, (40, 1215, 1040, 1600), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    if k1 > 0:
        text(d, (W / 2, 1285), "f vuông góc v: f là lực hướng tâm", 44, RED, alpha=k1)
        k2 = appear(t, M[1] - 0.1, 0.45)
        text(d, (W / 2, 1390), "r = mv/(|q|B) tỉ lệ với v", 46, INK, alpha=k2)
        k3 = appear(t, M[1] + 0.1, 0.45)
        text(d, (W / 2, 1500), "T = 2πr/v ≈ 1,8·10⁻⁸ s cả ba lần", 46, NAVY, alpha=k3)

# ---------------- canh 4: Bay + chua noi duoc ----------------
RC4 = (540, 560); R4 = 190
def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 880), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    cx, cy = RC4
    for gx in (170, 910):
        for gy in (330, 560, 790): sym(d, gx, gy, "x", 13, PURPLE, 3, alpha=0.75 * k0)
    d.ellipse([cx - R4, cy - R4, cx + R4, cy + R4], outline=A(VCOL[1], k0), width=6)
    dot(d, cx, cy, 7, A(NOTE, k0))
    for ph in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        x, y = cx + R4 * math.sin(ph), cy - R4 * math.cos(ph)
        vec(d, (x, y), vdir(ph), 110, TEAL); vec(d, (x, y), fdir(ph), 80, RED)
        electron(d, x, y, 12)
    text(d, (cx + 72, cy - R4 - 44), "v", 42, TEAL, anchor="lm", alpha=k0)
    text(d, (cx + 26, cy - R4 + 74), "f", 42, RED, anchor="lm", alpha=k0)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = k0 * (1 - k3)
    y = 920; mk = M[0] + 2.4
    if a1 > 0:
        card(d, (40, y, 1040, y + 250 + 220 * appear(t, mk + 0.2, 0.45)), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Lực từ làm electron nhanh dần”"
        ks = clamp((t - mk) / 0.4); f = F(46); lw = tw(d, q, f); yy = y + 180
        text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        k2 = a1 * appear(t, mk + 0.2, 0.45)
        text(d, (W / 2, y + 300), "f vuông góc v: không sinh công", 46, INK, alpha=k2)
        text(d, (W / 2, y + 390), "Tốc độ không đổi", 50, ORANGE, alpha=k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        lines = ("• Chỉ thấy vệt sáng cả chùm", "• v suy từ hiệu điện thế", "• v xiên với B: chưa xét")
        for j, l in enumerate(lines):
            kk = k3 * appear(t, M[1] + 0.2 + 0.4 * j, 0.4)
            text(d, (90, y + 210 + j * 120), l, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    cx, cy, r = 540, 1110, 80
    for gx in (380, 700):
        sym(d, gx, cy, "x", 13, PURPLE, 3, alpha=0.75 * k)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=A(VCOL[1], k), width=6)
    x, y = cx, cy - r; electron(d, x, y, 11)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "T không phụ thuộc v",
             "Electron v = 2·10⁷ m/s, tăng B. Bán kính và chu kì đổi thế nào?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)                 # goi y hien tre: chi cho cong thuc goc
    if kh > 0:
        card(d, (110, 1320, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1368, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1460, "B: 2·10⁻³ → 4·10⁻³ T", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    t_on, st = loops(do)
    return ([(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + t_on, "tap")]
            + [(do["t0"] + s, "tick") for s in st]
            + [(da["t0"] + 0.4 + LAP, "ding"), (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-luctu-05", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Lực từ · Cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Electron trong từ trường", draw=s_hook, tail=0.3, caps=[
   ("Chùm electron trong từ trường đều.", 3.0),
   ("Dừng video, tự chọn đáp án.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   "Chưa bật B: vệt sáng thẳng.",
   ("Bật B, tăng v gấp 2, gấp 3.", 6.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Ba electron về chỗ cũ cùng lúc.", 4.4),
   "Bán kính gấp 3 khi v gấp 3."]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 5.4),
   ("Giới hạn của thí nghiệm.", 5.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video và trả lời.", 6.4)]),
])
