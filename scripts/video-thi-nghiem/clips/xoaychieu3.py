# Clip: tn-l12-xoaychieu-03 - Mot chieu 12 V so voi xoay chieu 12 V hieu dung
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-xoaychieu-03.json:
#   tham_so: U = 12 V, R = 12 ohm; so_lieu_mau: U0 = 12.can2 = 16,97 ≈ 17 V; P = U^2/R = 12,0 W; hang 24 V -> 48,0 W.
#   p(t) = u^2/R: dinh U0^2/R = 2.144/12 = 24 W (= 2P), trung binh 12 W.
# Ban 2 (26/11/2026, viec 4 lo 32, cong --do-chu moi): canh hook / do / ans / bay / gioi / end nhu mau xoaychieu2.
#   Du doan (K10 khong ve nut; khung web A-D): den xoay chieu 12 V so voi mot chieu 12 V? -> sang nhu nhau
#     (A khong sang: hien_tuong_hay_sai #1; D sang hon: #2 lay dinh 17 V).
#   Bay: dung U0 ≈ 17 V tinh P -> 24 W? -> SAI, dung U hieu dung: 12 W (hien_tuong_hay_sai #2).
#   Chot (khung web A-D, dap an KHONG hien): von ke xoay chieu chi 24 V, bong 12 ohm -> P = 48 W (hang so_lieu_mau).
# Toa do mp4 = 65 + 0,88.x; chu >= 56 px (ra >= 49 px).
from engine import *

U, R = 12, 12
assert round(U * math.sqrt(2), 2) == 16.97 and U * U / R == 12 and 2 * U * U / R == 24 and 24 * 24 / R == 48
AMB = (255, 214, 102)
LAMP_GLOW = (255, 196, 61)
DGREEN = (21, 128, 61); DARK_OR = (181, 71, 8)

# ---------------- ky hieu mach ----------------
def lamp(d, cx, cy, lit, lab=True):
    """Bong den soi dot; lit 0..1 = do sang."""
    if lit > 0:
        for k in range(7, 0, -1):
            r = 50 + k * 16
            dot(d, cx, cy, r, A(LAMP_GLOW, 0.07 * lit))
        for j in range(8):                                      # tia sang
            a = math.radians(j * 45 + 22.5)
            d.line([(cx + 82 * math.cos(a), cy + 82 * math.sin(a)), (cx + 102 * math.cos(a), cy + 102 * math.sin(a))],
                   fill=A(ORANGE, lit), width=6)
    dot(d, cx, cy, 52, mix(WHITE, AMB, lit), outline=NAVY)
    d.line([(cx - 37, cy - 37), (cx + 37, cy + 37)], fill=NAVY, width=5)   # ky hieu den: vong tron + dau X
    d.line([(cx - 37, cy + 37), (cx + 37, cy - 37)], fill=NAVY, width=5)


def battery(d, cx, cy):
    """Ky hieu nguon mot chieu: vach dai mong (+), vach ngan day (-)."""
    d.line([(cx - 14, cy - 48), (cx - 14, cy + 48)], fill=NAVY, width=6)
    d.line([(cx + 14, cy - 26), (cx + 14, cy + 26)], fill=NAVY, width=14)
    text(d, (cx - 44, cy - 60), "+", 56, RED)
    text(d, (cx + 48, cy - 60), "−", 56, NAVY)


def ac_src(d, cx, cy):
    """Ky hieu nguon xoay chieu: vong tron co song sin."""
    dot(d, cx, cy, 46, WHITE, outline=NAVY)
    pts = [(cx - 28 + j * 56 / 30, cy - 15 * math.sin(2 * math.pi * j / 30)) for j in range(31)]
    d.line(pts, fill=ORANGE, width=6, joint="curve")


def vmeter(d, cx, cy, reading):
    card(d, (cx - 80, cy - 58, cx + 80, cy + 40), fill=(255, 236, 160), outline=NAVY, r=18, w=4)
    d.rounded_rectangle([cx - 68, cy - 48, cx + 68, cy + 14], radius=8, fill=NAVY)
    text(d, (cx, cy - 18), reading, 56, (134, 239, 172))


def circuit(d, x0, kind, lit, vread="?", lab=True):
    """Mot o mach: den o tren, nguon o duoi, day noi chu nhat. x0 = mep trai o (rong 460)."""
    cx = x0 + 230
    l, r, top, bot = x0 + 60, x0 + 400, 430, 720
    d.line([(l, top), (r, top)], fill=NAVY, width=5)
    d.line([(l, top), (l, bot)], fill=NAVY, width=5); d.line([(r, top), (r, bot)], fill=NAVY, width=5)
    d.line([(l, bot), (cx - 46, bot)], fill=NAVY, width=5); d.line([(cx + 46, bot), (r, bot)], fill=NAVY, width=5)
    d.rectangle([cx - 60, top - 8, cx + 60, top + 8], fill=BG)
    lamp(d, cx, top, lit)
    if kind == "dc":
        d.rectangle([cx - 46, bot - 8, cx + 46, bot + 8], fill=BG)
        d.line([(cx - 46, bot), (cx - 14, bot)], fill=NAVY, width=5); d.line([(cx + 14, bot), (cx + 46, bot)], fill=NAVY, width=5)
        battery(d, cx, bot)
        text(d, (cx, 815), "một chiều", 56, GREEN)
    else:
        ac_src(d, cx, bot)
        for sg in (-1, 1):                                       # von ke mac song song hai dau nguon
            d.line([(cx + sg * 74, 590), (cx + sg * 112, 590), (cx + sg * 112, bot)], fill=NAVY, width=4, joint="curve")
            dot(d, cx + sg * 112, bot, 11, NAVY)
        vmeter(d, cx, 590, vread)
        text(d, (cx, 815), "xoay chiều", 56, ORANGE)
    if lab: text(d, (cx, 296), "bóng 12 Ω", 56, INK, bold=False)


def two_circuits(d, lit_dc, lit_ac, vread, lab=True):
    card(d, (40, 250, 530, 870), fill=WHITE, outline=LIGHT, w=3)
    card(d, (550, 250, 1040, 870), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, 55, "dc", lit_dc, lab=lab)
    circuit(d, 565, "ac", lit_ac, vread, lab=lab)


# ---------------- do thi theo thoi gian ----------------
GX0, GX1 = 190, 990
def axes(d, ytop, ybot, vmin, vmax, ticks, ylab, ycol=INK):
    Y = lambda v: ybot - (v - vmin) / (vmax - vmin) * (ybot - ytop)
    y0 = Y(0)
    for v, s in ticks:
        d.line([(GX0, Y(v)), (GX1, Y(v))], fill=(236, 232, 222), width=2)
        d.line([(GX0 - 10, Y(v)), (GX0, Y(v))], fill=NAVY, width=4)
        text(d, (GX0 - 18, Y(v)), s, 56, INK, bold=False, anchor="rm")
    d.line([(GX0, y0), (GX1 + 20, y0)], fill=NAVY, width=5)
    d.line([(GX0, ybot + 10), (GX0, ytop - 30)], fill=NAVY, width=5)
    text(d, (GX0 + 16, ytop - 30), ylab, 56, ycol, anchor="lm")
    text(d, (GX1 + 20, y0 + 40), "t", 56, INK, anchor="rm")
    return Y


PER = 2.6                                     # so chu ki ve tren truc t
def u_ac(x): return U * math.sqrt(2) * math.cos(2 * math.pi * PER * x)


def curve(d, f, Y, k, color, w=6, x0=0.0):
    if k <= 0: return
    n = int(240 * k); pts = []
    for j in range(n + 1):
        x = x0 + (1 - x0) * j / 240
        pts.append((lerp(GX0, GX1, x), Y(f(x))))
    if len(pts) > 1: d.line(pts, fill=color, width=w, joint="curve")


def dashed_h(d, y, x0, x1, color, w=4, dash=18, gap=12, a=1.0):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=A(color, a), width=w); x += dash + gap


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    two_circuits(d, 0, 0, "12 V", lab=False)
    M = sc["M"]; a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 185), "Cùng 12 V: đèn xoay chiều", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "so với đèn một chiều?", 60, INK, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 340, 970, y0 + 450], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 340, 110 + 860 * (1 - p), y0 + 450], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh, ve u(t) ----------------
UY0, UY1 = 960, 1520
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    on_dc = appear(t, M[0] + 0.5, 0.4)
    mac = M[0] + 2.6
    on_ac = appear(t, mac + 0.6, 0.4)
    two_circuits(d, on_dc, on_ac, "12 V" if t > mac + 0.4 else "0 V")
    card(d, (40, 900, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    Y = axes(d, UY0 + 60, UY1, -20, 20, [(-17, "−17"), (12, "12"), (17, "17"), (0, "0")], "u (V)")
    text(d, (1010, 1555), "minh hoạ", 56, MUTED, bold=False, anchor="rm")
    curve(d, lambda x: U, Y, ease((t - M[0] - 0.6) / 1.0), GREEN, w=7)
    curve(d, u_ac, Y, ease((t - mac - 0.7) / 1.6), ORANGE, w=6)
    a = appear(t, M[1] - 0.1)
    if a > 0:
        xp = lerp(GX0, GX1, 1 / PER)
        dashed_h(d, Y(17), GX0, GX1, RED, a=a)
        dot(d, xp, Y(U * math.sqrt(2)), 13, RED, outline=WHITE)
        text(d, (700, 950), "U₀ = 12√2 ≈ 17 V", 56, RED, alpha=a)
    if t > mac + 2.3:                                   # con tro chay tren u(t): den xoay chieu van sang deu
        x = ((t - mac - 2.3) * 0.18) % 1.0
        dot(d, lerp(GX0, GX1, x), Y(u_ac(x)), 16, NAVY, outline=WHITE)
        d.line([(lerp(GX0, GX1, x), Y(-20)), (lerp(GX0, GX1, x), Y(20))], fill=A(NAVY, 0.35), width=3)

# ---------------- canh 3: Dap an + p(t) ----------------
PY0, PY1 = 380, 900
def p_ac(x): return u_ac(x) ** 2 / R

def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    s = "ĐÁP ÁN: sáng như nhau"; pw = tw(d, s, F(56)) + 70                  # hien ngay tu 0 s
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 340), fill=GREEN, r=39)
    text(d, (W / 2, 301), s, 56, WHITE)
    card(d, (40, 370, 1040, 1080), fill=WHITE, outline=LIGHT, w=3)
    Y = axes(d, PY0 + 70, PY1, 0, 26, [(0, "0"), (12, "12"), (24, "24")], "p = u²/R (W)")
    text(d, (1010, 1030), "minh hoạ", 56, MUTED, bold=False, anchor="rm")
    curve(d, p_ac, Y, ease(t / 1.4), ORANGE, w=6)
    a = appear(t, M[1] - 0.1)
    if a > 0:
        d.line([(GX0, Y(12)), (GX1, Y(12))], fill=A(GREEN, a), width=10)
        dashed_h(d, Y(12), GX0, GX1, PURPLE, w=5, a=a)
        text(d, (W / 2, 965), "trung bình 12 W", 56, PURPLE, alpha=a)
    c = appear(t, M[1] + 2.2, 0.4)
    if c > 0:
        card(d, (40, 1120, 1040, 1320), fill=A((236, 253, 243), c), outline=A(GREEN, c), w=5)
        text(d, (W / 2, 1180), "12 V hiệu dụng: toả nhiệt", 60, DGREEN, alpha=c)
        text(d, (W / 2, 1260), "bằng một chiều 12 V", 60, DGREEN, alpha=c)

# ---------------- canh 4: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k2, k3 = appear(t, b2, 0.4), appear(t, b3, 0.4)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 260, W / 2 + pw / 2, 336), fill=RED, r=38)
    text(d, (W / 2, 298), "BẪY", 56, WHITE)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1030 - pw2, 260, 1030, 336), fill=A((127, 29, 29), k3), r=38)
        text(d, (1030 - pw2 / 2, 298), "SAI", 56, WHITE, alpha=k3)
    ks = clamp((t - b3) / 0.4)
    for j, q in enumerate(("Tính bằng U₀ ≈ 17 V:", "P = 17²/12 ≈ 24 W?")):
        yy = 430 + 95 * j
        text(d, (W / 2, yy), q, 64, mix(INK if j == 0 else RED, GRAY, 0.45 * ks))
        if ks > 0 and j == 1:
            lw = tw(d, q, F(64))
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    # nhip 2: hai den sang nhu nhau (den xoay chieu khong sang gap doi)
    card(d, (40, 610, 1040, 1100), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    if k2 > 0:
        for cx, col in ((290, GREEN), (790, ORANGE)):
            lamp(d, cx, 820, k2)
            d.rounded_rectangle([cx - 90, 960, cx + 90, 990], radius=12, fill=A(col, k2))
        text(d, (540, 820), "=", 90, NAVY, alpha=k2)
    if k3 > 0:
        card(d, (40, 1140, 1040, 1400), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1270), "P = U²/R = 12²/12 = 12 W", 62, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1100), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Đo công suất thật?", "• √2 từ đâu ra?")):
        text(d, (100, 560 + j * 260), s, 66, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 700), "?", 200, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot cua khung; dap an KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Vôn kế xoay chiều chỉ 24 V.", 60, INK, alpha=k)
    text(d, (W / 2, 540), "Bóng 12 Ω: P = ?", 60, DARK_OR, alpha=k)
    cx, top, bot, l, r = 540, 700, 1040, 330, 750
    d.line([(l, top), (r, top), (r, bot), (cx + 46, bot)], fill=NAVY, width=5)
    d.line([(cx - 46, bot), (l, bot), (l, top)], fill=NAVY, width=5)
    lamp(d, cx, top, 0)
    ac_src(d, cx, bot)
    for sg in (-1, 1):
        d.line([(cx + sg * 80, 880), (cx + sg * 120, 880), (cx + sg * 120, bot)], fill=NAVY, width=4)
        dot(d, cx + sg * 120, bot, 11, NAVY)
    vmeter(d, cx, 880, "24 V")
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1230, 990, 1380), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1305), "Gợi ý: vôn kế chỉ giá trị nào?", 56, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][0] + 0.5, "tap"), (do["t0"] + do["M"][0] + 3.2, "tap"),
            (an["t0"] + 0.1, "ding"), (an["t0"] + an["M"][1] + 2.2, "tap"),
            (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")]

CLIP = dict(id="tn-l12-xoaychieu-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Một chiều hay xoay chiều?", draw=s_hook, tail=0.3, caps=[
   ("Một đèn, hai nguồn 12 V.", 3.0),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Nối một chiều, rồi xoay chiều.", 4.6),
   ("So độ sáng hai đèn.", 4.4)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("p = u²/R không bao giờ âm.", 3.0),
   ("Trung bình 12 W, như một chiều.", 5.2)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Hai đèn sáng như nhau.", 3.0),
   ("Phải dùng U hiệu dụng.", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Chưa trả lời được:", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.6)]),
])
