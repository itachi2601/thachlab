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
GOLD, MAGENTA = (170, 115, 0), (190, 24, 120)
VCOL = (BLUE, GOLD, MAGENTA)               # 12/11: tach khoi f (do) va v (xanh luc)
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

def bulb(d, field=1.0, rs=(), skip=()):
    cx, cy = BC
    d.ellipse([cx - BR, cy - BR, cx + BR, cy + BR], fill=GLASS, outline=(160, 168, 190), width=5)
    if field > 0:
        for gx in range(cx - 330, cx + 331, 110):
            for gy in range(cy - 330, cy + 331, 110):
                if math.hypot(gx - cx, gy - cy) > BR - 40: continue
                near = any(abs(math.hypot(gx - center(r)[0], gy - center(r)[1]) - r * PX) < 30 for r in rs)
                if near or (abs(gy - P[1]) < 34 and 380 < gx < 560): continue
                if any(x0 - 16 < gx < x1 + 16 and y0 - 16 < gy < y1 + 16 for x0, y0, x1, y1 in skip): continue
                sym(d, gx, gy, "x", 13, PURPLE, 3, alpha=0.75 * field)
    gun(d)

def gun(d):                                # goi lai SAU vet sang de sung de len vet (12/11)
    d.rounded_rectangle([420, P[1] - 15, 512, P[1] + 15], radius=6, fill=NAVY)
    d.polygon([(512, P[1] - 9), (532, P[1] - 5), (532, P[1] + 5), (512, P[1] + 9)], fill=NAVY)

def trail(d, rcm, ph1, col, w=8):
    if ph1 <= 0.01: return
    n = max(2, int(ph1 / (2 * math.pi) * 120))
    pts = [pos(rcm, ph1 * i / n) for i in range(n + 1)]
    d.line(pts, fill=A(col, 0.28), width=w + 12, joint="curve")
    d.line(pts, fill=col, width=w, joint="curve")

HIDE = 0.35                                # an electron khi chui sau than sung (pha > 2pi - HIDE)
def electron(d, x, y, r=13):
    dot(d, x, y, r, NAVY, outline=WHITE)

def vec(d, p, u, L, col, w=7, head=20):
    arrow(d, p, (p[0] + u[0] * L, p[1] + u[1] * L), col, w=w, head=head)

def legend_B(d, y, on=True, full=True, x=150):
    if on:
        sym(d, x, y, "x", 20, PURPLE, 4)
        text(d, (x + 36, y), "B = 2·10⁻³ T, vào trong trang" if full else "B = 2·10⁻³ T", 44, PURPLE, anchor="lm")
    else:
        text(d, (W / 2, y), "B = 0", 44, NOTE)

def legend_vf(d, y, f=True, x=110, alpha=1.0, ftxt="f: lực từ lên electron"):
    """Chu giai mui ten (giu o moi canh co mui ten v, f)."""
    if alpha <= 0: return
    arrow(d, (x, y), (x + 100, y), A(TEAL, alpha), w=8, head=24)
    text(d, (x + 120, y), "v", 48, TEAL, anchor="lm", alpha=alpha)
    if f:
        arrow(d, (x + 220, y), (x + 320, y), A(RED, alpha), w=8, head=24)
        text(d, (x + 340, y), ftxt, 46, RED, anchor="lm", alpha=alpha)

def tag(d, xy, s, alpha=1.0, size=44):
    """Nhan co nen trang (de len luoi B)."""
    w = tw(d, s, F(size)) + 36
    card(d, (xy[0] - w / 2, xy[1] - 34, xy[0] + w / 2, xy[1] + 34), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), r=18, w=3)
    text(d, xy, s, size, INK, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; RH = 5.7; bulb(d, 1.0, rs=(RH,), skip=((360, 700, 720, 850),))            # vong v = 2e7 (to hon de mui ten v, f ro)
    ph = 2 * math.pi * ((t / 2.8) % 1.0)
    trail(d, RH, 2 * math.pi, VCOL[1])
    cx, cy = center(RH)
    d.line([(cx, cy + RH * PX + 6), (cx, 790)], fill=INK, width=3)          # chi nhan vao vet sang
    tag(d, (cx, 812), "chùm electron")
    gun(d)
    if ph < 2 * math.pi - HIDE:
        x, y = pos(RH, ph); electron(d, x, y, 16)
        vec(d, (x, y), vdir(ph), 150, TEAL, w=9, head=28); vec(d, (x, y), fdir(ph), 110, RED, w=9, head=28)
    legend_B(d, 1060)
    legend_vf(d, 1130, alpha=appear(t, 0.5, 0.5))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1190 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 440), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 155), "Tăng v từ 1·10⁷ lên 3·10⁷ m/s.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "Thời gian đi hết một vòng đổi thế nào?", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 320), "Chọn đáp án ở khung câu hỏi", 44, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 385, 940, y0 + 399], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 385, 140 + 800 * (1 - p), y0 + 399], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
LOOP, GAP = 1.3, 1.6
def loops(sc):
    t_on = sc["M"][1]
    return t_on, [t_on + 0.4 + GAP * k for k in range(3)]

COLX = ((235, "v (10⁷ m/s)"), (575, "r (cm)"), (870, "T (10⁻⁸ s)"))
def table(d, y0, ks, alpha=1.0):
    card(d, (40, y0, 1040, y0 + 370), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, s in COLX: text(d, (x, y0 + 52), s, 48, INK, alpha=alpha)
    d.line([(70, y0 + 98), (1010, y0 + 98)], fill=A(LIGHT, alpha), width=3)
    for j, ((v, r), k) in enumerate(zip(DATA, ks)):
        if k <= 0: continue
        yy = y0 + 98 + 86 * (j + 0.5) + 4
        dot(d, 95, yy, 16, A(VCOL[j], k))
        text(d, (235, yy), str(v), 50, INK, alpha=k)
        text(d, (575, yy), "≈ " + vn(r), 50, INK, alpha=k)
        text(d, (870, yy), "≈ 1,8", 50, INK, alpha=k)
    text(d, (1020, y0 + 412), "số liệu minh hoạ", 44, NOTE, anchor="rm", alpha=alpha)

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
        d.line([(700, P[1] + 16), (700, P[1] + 62)], fill=INK, width=3)
        tag(d, (700, P[1] + 96), "chùm electron")
    for j, (rc, s) in enumerate(zip((2.8, 5.7, 8.5), st)):
        if t < s: continue
        ph = 2 * math.pi * clamp((t - s) / LOOP)
        trail(d, rc, ph, VCOL[j])
    gun(d)
    for j, (rc, s) in enumerate(zip((2.8, 5.7, 8.5), st)):
        ph = 2 * math.pi * clamp((t - s) / LOOP)
        if t >= s and ph < 2 * math.pi - HIDE:
            x, y = pos(rc, ph); electron(d, x, y)
    legend_B(d, 1060, on=t >= t_on)
    table(d, 1120, [appear(t, s + LOOP, 0.35) for s in st])

# ---------------- canh 3: Dap an + Rut ra ----------------
LAP = 2.2
T_BACK = 0.4 + LAP              # ba electron chay MOT vong roi DUNG o cho xuat phat
T_DA = T_BACK + 1.8             # dap an hien sau 1,8 s chi co hinh ba electron da ve cho cu
def s_dapan(img, d, t, sc):
    M = sc["M"]; bulb(d, 1.0, rs=(2.8, 5.7, 8.5))
    ph = 2 * math.pi * clamp((t - 0.4) / LAP)
    for j, (v, rc) in enumerate(DATA):
        trail(d, rc, 2 * math.pi, VCOL[j], w=6)
    gun(d)
    if t < T_BACK:
        if ph < 2 * math.pi - HIDE:
            for j, (v, rc) in enumerate(DATA):
                x, y = pos(rc, ph); vec(d, (x, y), vdir(ph), 50 * v, TEAL, w=7, head=22); electron(d, x, y)
    else:                                            # ca ba cung ve diem xuat phat
        kb = appear(t, T_BACK, 0.3)
        d.ellipse([P[0] - 30, P[1] - 30, P[0] + 30, P[1] + 30], outline=A(NAVY, kb), width=5)
        electron(d, P[0], P[1], 15)
    legend_B(d, 1060, full=False)
    legend_vf(d, 1060, f=False, x=600)
    ka = appear(t, T_DA, 0.4)
    if ka > 0:
        s = "ĐÁP ÁN · T không đổi"
        pw = tw(d, s, F(44)) + 60
        card(d, (W / 2 - pw / 2, 1112, W / 2 + pw / 2, 1186), fill=A(NAVY, ka), r=36)
        text(d, (W / 2, 1149), s, 44, WHITE, alpha=ka)
    k1 = appear(t, T_DA + 0.8, 0.45)                # moi dong mot nhip ~1,4 s
    card(d, (40, 1215, 1040, 1650), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    if k1 > 0:
        text(d, (W / 2, 1280), "f vuông góc v: f là lực hướng tâm", 44, RED, alpha=k1)
        k2 = appear(t, T_DA + 2.2, 0.45)
        text(d, (W / 2, 1375), "r = mv/(|q|B) tỉ lệ với v", 46, INK, alpha=k2)
        text(d, (W / 2, 1450), "m, |q|: khối lượng, độ lớn điện tích electron", 44, NOTE, bold=False, alpha=k2)
        k3 = appear(t, T_DA + 3.6, 0.45)
        text(d, (W / 2, 1570), "T = 2πr/v ≈ 1,8·10⁻⁸ s cả ba lần", 46, NAVY, alpha=k3)

# ---------------- canh 4: Bay + chua noi duoc ----------------
RC4 = (540, 590); R4 = 230
def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 1010), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    cx, cy = RC4
    for gx in (120, 960):
        for gy in (360, 590, 820): sym(d, gx, gy, "x", 15, PURPLE, 3, alpha=0.75 * k0)
    d.ellipse([cx - R4, cy - R4, cx + R4, cy + R4], outline=A((90, 100, 130), k0), width=7)
    sym(d, 92, 300, "x", 20, PURPLE, 4); text(d, (128, 300), "B vào trang", 44, PURPLE, anchor="lm", alpha=k0)
    mk = M[0] + 2.4; kf = k0 * appear(t, mk + 0.2, 0.45)    # f hien cung luc gach cau sai
    dot(d, cx, cy, 8, A(NOTE, k0))
    for ph in (0, math.pi / 2, math.pi, 3 * math.pi / 2):    # 4 cap, cap nao cung ghi nhan v, f
        x, y = cx + R4 * math.sin(ph), cy - R4 * math.cos(ph)
        u, fd = vdir(ph), fdir(ph)
        vec(d, (x, y), u, 130, TEAL, w=8, head=24)
        if kf > 0: vec(d, (x, y), fd, 100, A(RED, kf), w=8, head=24)
        electron(d, x, y, 14)
        text(d, (x + u[0] * 168, y + u[1] * 168), "v", 48, TEAL, alpha=k0)
        text(d, (x + fd[0] * 62 - u[0] * 40, y + fd[1] * 62 - u[1] * 40), "f", 48, RED, alpha=kf)
    legend_vf(d, 950, f=False, alpha=k0); legend_vf(d, 950, alpha=kf, ftxt="f: lực từ")
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = k0 * (1 - k3)
    y = 1050
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
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa kết luận được", 48, NAVY, alpha=k3)
        lines = ("• Chỉ thấy vệt sáng cả chùm", "• Chỉ xét v vuông góc B")
        for j, l in enumerate(lines):
            kk = k3 * appear(t, M[1] + 0.2 + 0.4 * j, 0.4)
            text(d, (100, y + 200 + j * 110), l, 48, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    cx, cy, r = 540, 1110, 80
    for gx in (380, 700):
        sym(d, gx, cy, "x", 13, PURPLE, 3, alpha=0.75 * k)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=A(VCOL[1], k), width=6)
    x, y = cx, cy - r; electron(d, x, y, 11)
    sym(d, 360, 1235, "x", 20, PURPLE, 4, alpha=k); text(d, (396, 1235), "B vào trang", 44, PURPLE, anchor="lm", alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "T không phụ thuộc v",
             "Electron v = 2·10⁷ m/s, tăng B. Bán kính và chu kì đổi thế nào?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)                 # goi y hien tre: chi cho cong thuc goc
    if kh > 0:
        card(d, (110, 1320, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1368, "Gợi ý", 44, MUTED, bold=False, alpha=kh)
        ctext(d, 1460, "B: 2·10⁻³ → 4·10⁻³ T", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    t_on, st = loops(do)
    return ([(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + t_on, "tap")]
            + [(do["t0"] + s, "tick") for s in st]
            + [(da["t0"] + T_DA, "ding"), (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-luctu-05", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Lực từ · Cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Electron trong từ trường", draw=s_hook, tail=0.3, caps=[
   ("Chùm electron trong từ trường đều.", 3.0),
   ("Tự nghĩ trước khi xem tiếp.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   "Chưa bật B: vệt sáng thẳng.",
   ("Bật B, tăng v gấp 2, gấp 3.", 6.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.96, caps=[
   "Ba electron cùng xuất phát.",
   ("Ba electron về chỗ cũ cùng lúc.", 6.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 5.4),
   ("Giới hạn của thí nghiệm.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video và trả lời.", 6.4)]),
])
