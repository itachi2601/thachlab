# Clip: tn-l9-hsgamthanh-02 - Do toc do am bang tieng vang truoc buc tuong lon (HSG KHTN 9, CD15, lo 6, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-hsgamthanh-02.json:
#   so_lieu_mau (d m, t s, v = 2d/t m/s): 34 0,21 324 ; 51 0,30 340 ; 68 0,41 332. rut_ra[0]: v xap xi 330-340 m/s.
#   bay = hien_tuong_hay_sai[0] (v = d/t, quen di va ve): 51 : 0,30 = 170 m/s (ghi o kho ghi_chu).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[2] (khong co gio).
# Cau sau hop (KHONG duoc tra loi san): "Vi sao lan do o 34 m lech nhieu nhat?" (sai so ti doi) -> clip khong noi gi ve
#   lech/sai so ; cau do sau 1500 m/s, 0,8 s ; ong thep ; thu thach 1 (170 m -> t) va 2 (hai vach) -> chot khong trung.
# Du doan (K10: chi cau hoi + hinh): o 34 m doc t = 0,21 s ; lui ra 68 m (xa gap doi) -> t khoang?
#   A. khoang 0,2 s  B. khoang 0,4 s  C. khoang 0,8 s  D. khoang 0,1 s  -> dap an B (kho: 0,41 s).
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, Du doan khong nut.
# Cau chot cu hoi v (dap so 340 m/s - trung so da chieu o Rut ra va Bay) -> dao chieu cung ca trong kho:
#   dang doc t = 0,25 s ; lui xa tuong them 17 m -> t doc khoang bao nhieu? -> 0,35 s (am di them 2 x 17 = 34 m,
#   v ~ 340 m/s -> them 0,10 s). So 0,35 khong hien tren man.
# Hinh: nguoi cach tuong d (ti le 11,2 px/m), xung am (cung tron) di toi tuong roi doi ve (tam ao doi xung qua tuong),
#   chieu cham 6 lan ; dien thoai ghi dang song: xung vo o 0, xung vang o t_doc. _kiem(): moi 0,05 s xung vang chi ve
#   sau khi cung am ve toi nguoi, hang bang / nhan t chi co sau khi xung vang da ve.
import copy, math
from engine import *

ROWS = [(34, 0.21, 324), (51, 0.30, 340), (68, 0.41, 332)]   # so_lieu_mau
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")

DGREEN = (21, 110, 55); DRED = (185, 28, 28); WALL = (150, 120, 100)
WX, KPX, GY = 950, 760 / 68, 650     # mat tuong, px moi m, mat dat
SLOW = 6.0
def xp_of(dm): return WX - dm * KPX

# ---------------- hinh co ban ----------------
def person(d, x, clap=0.0, a=1.0, col=NAVY):
    c = A(col, a)
    d.ellipse([x - 22, 448, x + 22, 492], outline=c, width=6)
    d.line([(x, 492), (x, 575)], fill=c, width=7)
    d.line([(x, 575), (x - 26, GY - 4)], fill=c, width=7); d.line([(x, 575), (x + 26, GY - 4)], fill=c, width=7)
    hx = lerp(x + 46, x + 30, clap); hy1, hy2 = lerp(505, 520, clap), lerp(545, 520, clap)
    d.line([(x, 515), (hx, hy1)], fill=c, width=6); d.line([(x, 515), (hx, hy2)], fill=c, width=6)

def wall(d, a=1.0):
    d.rectangle([WX, 330, WX + 50, GY], fill=A(mix(WALL, WHITE, 0.35), a), outline=A(WALL, a), width=4)
    for y in range(345, GY, 34): d.line([(WX, y), (WX + 50, y)], fill=A(WALL, a), width=2)

def stage(d, dm, s=None, ttxt=True, slow=True):
    """dm: khoang cach (m, co the le khi dang di chuyen) ; s: quang am da di (m) hoac None."""
    card(d, (40, 270, 1040, 720), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, GY), (1020, GY)], fill=GRAY, width=4)
    wall(d)
    x = xp_of(dm)
    clap = 1.0 if (s is not None and s < 6) else 0.0
    person(d, x, clap)
    # khoang cach
    d.line([(x, 372), (WX, 372)], fill=PURPLE, width=4)
    for xx in (x, WX): d.line([(xx, 356), (xx, 388)], fill=PURPLE, width=4)
    if ttxt: text(d, ((x + WX) / 2, 318), f"cách {round(dm)} m", 56, PURPLE)
    if slow: text(d, (70, 312), "chiếu chậm", 56, MUTED, anchor="lm")
    if s is None: return
    cy = 520
    if s <= dm:      # di toi tuong
        r = s * KPX
        for k in range(3):
            rr = r - 18 * k
            if rr > 8:
                g = math.degrees(math.asin(min(1.0, 85 / rr))) if rr > 85 else 60
                g = min(g, 60); d.arc([x - rr, cy - rr, x + rr, cy + rr], start=-g, end=g, fill=A(ORANGE, 1 - 0.3 * k), width=6)
    elif s <= 2 * dm:   # doi ve: tam ao doi xung qua tuong
        xi = WX + dm * KPX; r = s * KPX
        for k in range(3):
            rr = r - 18 * k
            if xi - rr < WX - 4:
                g = min(28.0, math.degrees(math.asin(min(1.0, 85 / rr))))
                d.arc([xi - rr, cy - rr, xi + rr, cy + rr], start=180 - g, end=180 + g, fill=A(BLUE, 1 - 0.3 * k), width=6)

T0X, T1X, AY, PXS = 100, 980, 990, 1760   # truc thoi gian dang song: 0..0,5 s
def wave(d, tau, tdoc, label=True, a=1.0):
    card(d, (40, 750, 1040, 1142), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (70, 795), "điện thoại ghi âm", 56, MUTED, anchor="lm", alpha=a)
    text(d, (1010, 1100), "t (s)", 56, MUTED, anchor="rm", alpha=a)
    d.line([(T0X, AY), (T1X, AY)], fill=A(LIGHT, a), width=3)
    for k in range(6):
        x = T0X + PXS * 0.1 * k
        d.line([(x, AY + 20), (x, AY + 34)], fill=A(GRAY, a), width=3)
        if k == 0: text(d, (x, AY + 80), "0", 56, MUTED, alpha=a)      # GĐ2: khong in 0,2/0,4 tren truc (0,4 = dap an Du doan)
    if tau is None: return
    pts = []; n = int(min(tau, 0.5) / 0.0008)
    for i in range(n + 1):
        u = i * 0.0008; y = 3 * math.sin(u * 900)
        y += 100 * math.exp(-u / 0.008) * math.sin(2 * math.pi * u / 0.0045)
        if u >= tdoc: y += 70 * math.exp(-(u - tdoc) / 0.008) * math.sin(2 * math.pi * (u - tdoc) / 0.0045)
        pts.append((T0X + PXS * u, AY - 0.8 * y))
    if len(pts) > 1: d.line(pts, fill=A(NAVY, a), width=3)
    if label and tau >= tdoc + 0.02:
        x2 = T0X + PXS * tdoc; yb = 870
        d.line([(T0X, yb), (x2, yb)], fill=A(ORANGE, a), width=5)
        for xx in (T0X, x2): d.line([(xx, yb - 16), (xx, yb + 16)], fill=A(ORANGE, a), width=5)
        text(d, (max(x2 + 24, 380), yb), f"t = {vn(tdoc)} s", 56, ORANGE, anchor="lm", alpha=a)

def table(d, n, hl=None, y=1160):
    card(d, (40, y, 1040, y + 400), fill=WHITE, outline=LIGHT, w=3)
    for x, h in zip((300, 780), ("d (m)", "t (s)")): text(d, (x, y + 55), h, 56, NAVY)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=3)
    for j, (dm, tt, v) in enumerate(ROWS):
        yy = y + 165 + j * 85
        if hl == j: d.rounded_rectangle([60, yy - 38, 1020, yy + 38], radius=20, fill=(255, 237, 213))
        if j < n: text(d, (300, yy), str(dm), 56, PURPLE); text(d, (780, yy), vn(tt), 56, ORANGE)

# ---------------- trang thai cac lan do ----------------
# Hook: do o 34 m. Canh do: lan 51 m roi 68 m.
H_CLAP = 0.6
D_RUNS = [(0.4, 0), (3.9, 1)]          # (bat dau, chi so hang) trong canh "do"
MOVE, CLAPD, ROWD = 0.6, 0.8, 0.3
def run_at(t, start, j, prev_dm):
    """-> (dm, s (m) hay None, tau hay None, da_ghi?)."""
    dm, tdoc = ROWS[j][0], ROWS[j][1]
    if t < start + MOVE: return lerp(prev_dm, dm, ease((t - start) / MOVE)), None, None, False
    tc = start + CLAPD
    if t < tc: return dm, None, None, False
    tau = (t - tc) / SLOW
    s = tau * 2 * dm / tdoc
    return dm, (s if s <= 2 * dm else None), tau, t >= tc + tdoc * SLOW + ROWD

CH_T0, CH_DD, CH_T1 = 0.25, 17, 0.35      # cau chot (kho ghi_chu): t dau, lui them (m), t sau (khong hien)
def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    dm, tdoc = ROWS[0][0], ROWS[0][1]
    tau = (t - H_CLAP) / SLOW if t >= H_CLAP else None
    s = tau * 2 * dm / tdoc if tau is not None and tau * 2 * dm / tdoc <= 2 * dm else None
    stage(d, dm, s)
    wave(d, tau, tdoc)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1158 + (1 - a) * 30                        # GĐ2 v2: duoi khung song (khong che do thi)
    card(d, (40, y0, 1040, y0 + 440), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 52, a, PURPLE)
    for k2, (l, r) in enumerate((("cách 34 m", "t = 0,21 s"), ("cách 68 m", "t = ?"))):
        y = y0 + 135 + k2 * 72
        text(d, (330, y), l, 58, PURPLE, alpha=a); text(d, (760, y), r, 58, ORANGE if k2 == 0 else INK, alpha=a)
    text(d, (W / 2, y0 + 285), "Khi đó t khoảng bao nhiêu?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 340, 970, y0 + 410], radius=35, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 340, 110 + max(70, 860 * (1 - p)), y0 + 410], radius=35, fill=A((76, 29, 149), a))

def d_state(t):
    """-> (j dang do, dm, s, tau, so hang da ghi)."""
    if t >= D_RUNS[1][0]: st, j, prev = D_RUNS[1][0], 2, ROWS[1][0]
    else: st, j, prev = D_RUNS[0][0], 1, ROWS[0][0]
    dm, s, tau, done = run_at(t, st, j, prev)
    return j, dm, s, tau, j + (1 if done else 0)

def s_do(img, d, t, sc):
    j, dm, s, tau, n = d_state(t)
    stage(d, dm, s)
    wave(d, tau, ROWS[j][1])
    table(d, n, hl=n - 1)

def _kiem():
    clip = copy.deepcopy(CLIP); build(clip); bad = []
    sc = [x for x in clip["scenes"] if x["key"] == "do"][0]; t = 0.0
    last = D_RUNS[1][0] + CLAPD + ROWS[2][1] * SLOW + ROWD
    if sc["T"] < last + 0.3: bad.append(("canh do ngan", round(sc["T"], 2), round(last, 2)))
    while t < sc["T"]:
        j, dm, s, tau, n = d_state(t)
        tdoc = ROWS[j][1]
        if n > j + 1: bad.append((round(t, 2), "hang qua som"))
        if n == j + 1 and (tau is None or tau < tdoc): bad.append((round(t, 2), "ghi hang truoc khi vang ve"))
        if tau is not None and tau < tdoc and s is None: bad.append((round(t, 2), "mat xung giua chung"))
        if tau is not None and tau >= tdoc and s is not None: bad.append((round(t, 2), "xung con khi da ve"))
        t += 0.05
    for dm, tt, v in ROWS:
        if abs(2 * dm / tt - v) > 0.6: bad.append(("so kho lech", dm))
    if abs(51 / 0.30 - 170) > 0.01 or abs(CH_T0 + 2 * CH_DD / 340 - CH_T1) > 1e-9: bad.append("so bay/chot")
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: khoảng 0,4 s", 320, 1.0, GREEN, 58)
    card(d, (40, 400, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    L = 500
    for j, (dm, tt, v) in enumerate(ROWS):
        yy = 510 + j * 140
        text(d, (150, yy), f"{dm} m", 56, PURPLE)
        g = ease((t - 0.5 - 0.3 * j) / 0.5); wb = L * tt / 0.41 * g
        if wb > 2: d.rounded_rectangle([260, yy - 32, 260 + wb, yy + 32], radius=14, fill=ORANGE)
        if g > 0.95: text(d, (260 + L * tt / 0.41 + 24, yy), vn(tt) + " s", 56, INK, anchor="lm")
    k2 = appear(t, M[1] + 0.1, 0.4)
    card(d, (40, 940, 1040, 1180), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
    text(d, (W / 2, 1010), "34 m → 68 m: xa gấp đôi", 56, DGREEN, alpha=k2)
    text(d, (W / 2, 1110), "0,21 s → 0,41 s: gần gấp đôi", 56, DGREEN, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 270, 1040, 640), fill=WHITE, outline=LIGHT, w=3)
    x = xp_of(51)
    d.line([(60, 600), (1020, 600)], fill=GRAY, width=4)
    d.rectangle([WX, 330, WX + 50, 600], fill=mix(WALL, WHITE, 0.35), outline=WALL, width=4)
    ka = appear(t, 0.4, 0.4)
    arrow(d, (x, 400), (WX - 10, 400), A(ORANGE, ka), w=7, head=22)
    text(d, ((x + WX) / 2, 350), "đi: d", 56, ORANGE, alpha=ka)
    kb = appear(t, 0.9, 0.4)
    arrow(d, (WX - 10, 520), (x, 520), A(BLUE, kb), w=7, head=22)
    text(d, ((x + WX) / 2, 470), "về: d", 56, BLUE, alpha=kb)
    kc = appear(t, 1.4, 0.4)
    text(d, (x - 150, 460), "2d", 64, INK, alpha=kc)
    d.line([(x - 20, 380), (x - 20, 540)], fill=A(INK, kc), width=5)
    k1 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 680, 1040, 1380), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
    for x0, h in zip((200, 500, 820), ("d (m)", "t (s)", "v = 2d : t (m/s)")): text(d, (x0 if x0 < 800 else 800, 750), h, 56, NAVY, alpha=k1)
    d.line([(70, 800), (1010, 800)], fill=A(LIGHT, k1), width=3)
    for j, (dm, tt, v) in enumerate(ROWS):
        yy = 880 + j * 110
        text(d, (200, yy), str(dm), 56, PURPLE, alpha=k1); text(d, (500, yy), vn(tt), 56, ORANGE, alpha=k1)
        kv = appear(t, M[1] + 0.4 + 0.45 * j, 0.35) * k1
        text(d, (820, yy), f"{v}", 56, DGREEN, alpha=kv)
    kk = appear(t, M[1] + 2.6, 0.4) * k1
    text(d, (W / 2, 1290), "v ≈ 330 – 340 m/s", 60, DGREEN, alpha=kk)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
BAY_ST = 2.2
def s_bay(img, d, t, sc):
    M = sc["M"]
    pu = 0.5 + 0.5 * math.sin(2 * math.pi * t / 1.6)
    card(d, (40, 270, 1040, 620), fill=mix(WHITE, (254, 215, 170), pu), outline=LIGHT, w=3)
    text(d, (W / 2, 335), "cách 51 m · t = 0,30 s", 58, INK)
    d.rectangle([930, 400, 975, 600], fill=mix(WALL, WHITE, 0.35), outline=WALL, width=4)   # hinh di - ve giu suot canh
    arrow(d, (330, 450), (915, 450), ORANGE, w=7, head=22); text(d, (80, 450), "đi: d", 56, ORANGE, anchor="lm")
    arrow(d, (915, 550), (330, 550), BLUE, w=7, head=22); text(d, (80, 550), "về: d", 56, BLUE, anchor="lm")
    k2 = appear(t, M[2] - 0.1, 0.45)
    a1 = 1 - k2; y0 = 660
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        q = "v = 51 : 0,30 = 170 m/s"
        ks = clamp((t - BAY_ST) / 0.4)
        lw = tw(d, q, F(58)); yy = y0 + 190
        text(d, (W / 2, yy), q, 58, INK, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 320, 1010, y0 + 580), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 400), "✓ Âm đi rồi về: 2d", 58, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 490), "102 : 0,30 = 340 m/s", 58, INK, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "gió thổi thì sao?", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(coi như không gió)", 56, NAVY, alpha=k2)

# ---------------- canh 6: Chot ----------------
END_Q = 0.2
def s_end(img, d, t, sc):
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 465), "Đang đọc t = " + vn(CH_T0) + " s.", 58, INK, alpha=k1)
    text(d, (W / 2, 550), f"Lùi xa tường thêm {CH_DD} m,", 58, INK, alpha=k1)
    text(d, (W / 2, 635), "t khoảng bao nhiêu?", 58, INK, alpha=k1)
    if k1 <= 0: return
    yb = 920
    d.line([(100, yb + 80), (980, yb + 80)], fill=A(GRAY, k1), width=4)
    d.rectangle([920, yb - 90, 970, yb + 80], fill=A(mix(WALL, WHITE, 0.35), k1), outline=A(WALL, k1), width=4)
    for x, c in ((600, NAVY), (360, PURPLE)):
        d.ellipse([x - 18, yb - 56, x + 18, yb - 20], outline=A(c, k1), width=5)
        d.line([(x, yb - 20), (x, yb + 30)], fill=A(c, k1), width=6)
        d.line([(x, yb + 30), (x - 20, yb + 78)], fill=A(c, k1), width=6); d.line([(x, yb + 30), (x + 20, yb + 78)], fill=A(c, k1), width=6)
    arrow(d, (580, yb - 110), (380, yb - 110), A(PURPLE, k1), w=6, head=20)
    text(d, (480, yb - 165), f"thêm {CH_DD} m", 56, PURPLE, alpha=k1)
    text(d, (600, yb + 150), vn(CH_T0) + " s", 56, NAVY, alpha=k1)
    rr = 55 + 25 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = 360, yb + 260
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + H_CLAP, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    cs += [(do["t0"] + st + CLAPD, "tap") for st, _ in D_RUNS]
    cs += [(da["t0"] + 0.2, "ding"), (r["t0"] + r["M"][1] + 0.1, "tap"), (b["t0"] + BAY_ST, "buzz"),
           (b["t0"] + b["M"][1] + 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-hsgamthanh-02", header="KHTN 9 · HSG VẬT LÍ · THÍ NGHIỆM", footer="Tiếng vang · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vỗ tay trước bức tường", draw=s_hook, tail=0.3, caps=[
   ("Vỗ tay trước tường.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Lùi xa tường, đo lại.", 3.4),
   ("Đọc t giữa hai xung.", 3.7)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Ba khoảng cách, ba lần đo.", 3.0),
   ("So hàng đầu và cuối.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.8, caps=[
   ("Âm tới tường rồi quay lại.", 3.0),
   ("Tính tốc độ âm từng lần.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("Âm đi mấy đoạn d?", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch:", _kiem() or "không")
