# Clip: tn-l9-hsgamthanh-02 - Do toc do am bang tieng vang truoc buc tuong lon (HSG KHTN 9, CD15, lo 6, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-hsgamthanh-02.json:
#   so_lieu_mau (d m, t s, v = 2d/t m/s): 34 0,21 324 ; 51 0,30 340 ; 68 0,41 332. rut_ra[0]: v xap xi 330-340 m/s.
#   bay = hien_tuong_hay_sai[0] (v = d/t, quen di va ve): 51 : 0,30 = 170 m/s (ghi o kho ghi_chu).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[2] (khong co gio).
# Cau sau hop (KHONG duoc tra loi san): "Vi sao lan do o 34 m lech nhieu nhat?" (sai so ti doi) -> clip khong noi gi ve
#   lech/sai so ; cau do sau 1500 m/s, 0,8 s ; ong thep ; thu thach 1 (170 m -> t) va 2 (hai vach) -> chot khong trung.
# Du doan (K10: chi cau hoi + hinh): o 34 m doc t = 0,21 s ; lui ra 68 m (xa gap doi) -> t khoang?
#   A. khoang 0,2 s  B. khoang 0,4 s  C. khoang 0,8 s  D. khoang 0,1 s  -> dap an B (kho: 0,41 s).
# Cau chot (ghi o kho ghi_chu): chua biet d ; t = 0,25 s ; lui them 17 m -> t = 0,35 s ; v ? -> 340 m/s (hai buoc:
#   them 2 x 17 = 34 m duong di cua am, trong 0,10 s). O chot hien SAU thoi gian nghi va khong neu quy tac/so 340.
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
    if ttxt: text(d, ((x + WX) / 2, 326), f"cách {round(dm)} m", 42, PURPLE)
    if slow: text(d, (70, 300), "chiếu chậm", 40, MUTED, bold=False, anchor="lm")
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

T0X, T1X, AY, PXS = 100, 980, 1012, 1760   # truc thoi gian dang song: 0..0,5 s
def wave(d, tau, tdoc, label=True, a=1.0):
    card(d, (40, 750, 1040, 1142), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (70, 790), "điện thoại ghi âm", 40, MUTED, bold=False, anchor="lm", alpha=a)
    d.line([(T0X, AY), (T1X, AY)], fill=A(LIGHT, a), width=3)
    for k in range(6):
        x = T0X + PXS * 0.1 * k
        d.line([(x, AY + 40), (x, AY + 54)], fill=A(GRAY, a), width=3)
        text(d, (x, AY + 88), "0" if k == 0 else vn(0.1 * k, 1) + (" s" if k == 5 else ""), 40, MUTED, bold=False, alpha=a)
    if tau is None: return
    pts = []; n = int(min(tau, 0.5) / 0.0008)
    for i in range(n + 1):
        u = i * 0.0008; y = 3 * math.sin(u * 900)
        y += 100 * math.exp(-u / 0.008) * math.sin(2 * math.pi * u / 0.0045)
        if u >= tdoc: y += 70 * math.exp(-(u - tdoc) / 0.008) * math.sin(2 * math.pi * (u - tdoc) / 0.0045)
        pts.append((T0X + PXS * u, AY - y))
    if len(pts) > 1: d.line(pts, fill=A(NAVY, a), width=3)
    if label and tau >= tdoc + 0.02:
        x2 = T0X + PXS * tdoc; yb = 858
        d.line([(T0X, yb), (x2, yb)], fill=A(ORANGE, a), width=5)
        for xx in (T0X, x2): d.line([(xx, yb - 16), (xx, yb + 16)], fill=A(ORANGE, a), width=5)
        if x2 > 800: text(d, (x2, yb - 46), f"t = {vn(tdoc)} s", 44, ORANGE, anchor="rm", alpha=a)
        else: text(d, (max(x2 + 20, 300), yb), f"t = {vn(tdoc)} s", 44, ORANGE, anchor="lm", alpha=a)

def table(d, n, hl=None, y=1160):
    card(d, (40, y, 1040, y + 400), fill=WHITE, outline=LIGHT, w=3)
    for x, h in zip((300, 780), ("d (m)", "t (s)")): text(d, (x, y + 55), h, 44, INK)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=3)
    for j, (dm, tt, v) in enumerate(ROWS):
        yy = y + 165 + j * 85
        if hl == j: d.rounded_rectangle([60, yy - 38, 1020, yy + 38], radius=20, fill=(255, 237, 213))
        if j < n: text(d, (300, yy), str(dm), 48, PURPLE); text(d, (780, yy), vn(tt), 48, ORANGE)
        else:
            for x in (300, 780): text(d, (x, yy), "·", 44, GRAY)

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

def s_hook(img, d, t, sc):
    M = sc["M"]
    dm, tdoc = ROWS[0][0], ROWS[0][1]
    tau = (t - H_CLAP) / SLOW if t >= H_CLAP else None
    s = tau * 2 * dm / tdoc if tau is not None and tau * 2 * dm / tdoc <= 2 * dm else None
    stage(d, dm, s)
    wave(d, tau, tdoc)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 750 + (1 - a) * 40
    card(d, (26, y0 - 12, 1054, y0 + 830), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 84), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 53), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for k, (l, r) in enumerate((("cách 34 m", "t = 0,21 s"), ("cách 68 m", "t = ?"))):
        y = y0 + 190 + k * 110
        text(d, (330, y), l, 50, PURPLE, alpha=a); text(d, (750, y), r, 50, ORANGE if k == 0 else INK, alpha=a)
    ctext(d, y0 + 490, "Lùi ra xa tường gấp đôi.\nKhoảng t lúc đó cỡ bao nhiêu?", 46, INK, maxw=940, alpha=a)
    text(d, (W / 2, y0 + 660), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 760, 940, y0 + 772], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 760, 140 + 800 * (1 - p), y0 + 772], radius=6, fill=A(PURPLE, a))
THINK_END = 0.7

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
    if abs(51 / 0.30 - 170) > 0.01 or abs(2 * 17 / (0.35 - 0.25) - 340) > 0.01: bad.append("so bay/chot")
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · khoảng 0,4 s"
    pw = tw(d, lab, F(44)) + 60
    card(d, (W / 2 - pw / 2, 280, W / 2 + pw / 2, 356), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 318), lab, 44, WHITE, alpha=ka)
    card(d, (40, 410, 1040, 920), fill=WHITE, outline=LIGHT, w=3)
    L = 560
    for j, (dm, tt, v) in enumerate(ROWS):
        yy = 525 + j * 140
        text(d, (150, yy), f"{dm} m", 46, PURPLE)
        g = ease((t - 0.5 - 0.3 * j) / 0.5); wb = L * tt / 0.41 * g
        if wb > 2: d.rounded_rectangle([250, yy - 32, 250 + wb, yy + 32], radius=14, fill=ORANGE)
        if g > 0.95: text(d, (250 + L * tt / 0.41 + 24, yy), vn(tt) + " s", 44, INK, anchor="lm")
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 > 0:
        card(d, (40, 980, 1040, 1300), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1080), "34 m → 68 m: xa gấp đôi", 46, DGREEN, alpha=k2)
        text(d, (W / 2, 1200), "0,21 s → 0,41 s: gần gấp đôi", 46, DGREEN, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 640), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    x = xp_of(51)
    d.line([(60, 600), (1020, 600)], fill=A(GRAY, k0), width=4)
    d.rectangle([WX, 330, WX + 50, 600], fill=A(mix(WALL, WHITE, 0.35), k0), outline=A(WALL, k0), width=4)
    ka = appear(t, 0.6, 0.4) * k0
    arrow(d, (x, 400), (WX - 10, 400), A(ORANGE, ka), w=7, head=22)
    text(d, ((x + WX) / 2, 360), "đi: d", 44, ORANGE, alpha=ka)
    kb = appear(t, 1.1, 0.4) * k0
    arrow(d, (WX - 10, 500), (x, 500), A(BLUE, kb), w=7, head=22)
    text(d, ((x + WX) / 2, 460), "về: d", 44, BLUE, alpha=kb)
    kc = appear(t, 1.6, 0.4) * k0
    text(d, (x - 150, 450), "2d", 60, INK, alpha=kc)
    d.line([(x - 20, 380), (x - 20, 520)], fill=A(INK, kc), width=5)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 700, 1040, 1400), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
        for x0, h in zip((200, 500, 820), ("d (m)", "t (s)", "2d : t")): text(d, (x0, 770), h, 44, INK, alpha=k1)
        d.line([(70, 820), (1010, 820)], fill=A(LIGHT, k1), width=3)
        for j, (dm, tt, v) in enumerate(ROWS):
            yy = 905 + j * 120
            text(d, (200, yy), str(dm), 46, PURPLE, alpha=k1); text(d, (500, yy), vn(tt), 46, ORANGE, alpha=k1)
            kv = appear(t, M[1] + 0.3 + 0.45 * j, 0.35) * k1
            text(d, (820, yy), f"{v} m/s", 46, DGREEN, alpha=kv)
        kk = appear(t, M[1] + 1.8, 0.4) * k1
        text(d, (W / 2, 1310), "v ≈ 330 – 340 m/s", 54, DGREEN, alpha=kk)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 270, 1040, 420), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 345), "cách 51 m · t = 0,30 s", 48, INK)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 460
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "v = 51 : 0,30 = 170 m/s"
        ks = clamp((t - M[0] - 1.4) / 0.4)
        lw = tw(d, q, F(52)); yy = y0 + 200
        text(d, (W / 2, yy), q, 52, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 36, yy), "✗", 52, DRED, alpha=a1 * ks)
        text(d, (W / 2, yy + 80), "chỉ bằng một nửa", 44, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 2.0, 0.4)
        card(d, (70, y0 + 370, 1010, y0 + 600), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 440), "✓ Âm đi rồi về: quãng 2d", 46, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 530), "v = 102 : 0,30 = 340 m/s", 46, INK, alpha=kk)
    if k2 > 0:
        y0 = 460 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 90), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ", "• Coi như không có gió")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 220 + j * 120), l1, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi ----------------
T_CHOT = 4.2
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1340), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(40)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
        ka = appear(t, M[0] + 0.4, 0.5)
        ctext(d, 860, "Chưa biết cách tường bao xa.\nĐọc được t = 0,25 s.\nLùi xa tường thêm 17 m: t = 0,35 s.\nTốc độ âm bằng bao nhiêu?",
              46, INK, maxw=920, alpha=ka)
        kw = appear(t, M[0] + 0.7, 0.5) * k1
        if kw > 0:
            yb = 1180
            d.line([(120, yb + 80), (960, yb + 80)], fill=A(GRAY, kw), width=4)
            d.rectangle([910, yb - 60, 950, yb + 80], fill=A(mix(WALL, WHITE, 0.35), kw), outline=A(WALL, kw), width=4)
            for x, c in ((560, NAVY), (370, NAVY)):
                d.ellipse([x - 16, yb - 50, x + 16, yb - 18], outline=A(c, kw), width=5)
                d.line([(x, yb - 18), (x, yb + 30)], fill=A(c, kw), width=6)
                d.line([(x, yb + 30), (x - 18, yb + 78)], fill=A(c, kw), width=6); d.line([(x, yb + 30), (x + 18, yb + 78)], fill=A(c, kw), width=6)
            arrow(d, (540, yb - 80), (390, yb - 80), A(PURPLE, kw), w=6, head=20)
            text(d, (465, yb - 120), "thêm 17 m", 42, PURPLE, alpha=kw)
            text(d, (740, yb - 10), "?", 50, MUTED, alpha=kw)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 270, 1020, 570), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 420, "Tiếng vang giúp đo tốc độ âm", 52, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + H_CLAP, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    cs += [(do["t0"] + st + CLAPD, "tap") for st, _ in D_RUNS]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
           (b["t0"] + b["M"][0] + 2.0, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l9-hsgamthanh-02", header="KHTN 9 · HSG VẬT LÍ · THÍ NGHIỆM", footer="Tiếng vang · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vỗ tay trước bức tường", draw=s_hook, tail=0.8, caps=[
   ("Vỗ tay, điện thoại ghi âm.", 3.0),
   ("Nghĩ trước đã.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Lùi xa tường, đo lại.", 3.4),
   ("Đọc t giữa hai xung.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Ba khoảng cách, ba giá trị t.", 3.1),
   ("Đi xa hơn, về muộn hơn.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Âm tới tường rồi quay lại.", 3.0),
   ("Tính tốc độ âm từng lần.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Có đúng không?", 4.0),
   ("Giới hạn của thí nghiệm.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Tự trả lời trước khi xem.", 6.6)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch:", _kiem() or "không")
