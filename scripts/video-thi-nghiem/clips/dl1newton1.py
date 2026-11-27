# Clip: tn-l10-dl1-newton-01 - Thi nghiem Galilei: hon bi tren hai mang nghieng (lo 7, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dl1-newton-01.json:
#   tham_so h0 = 20 cm, mang (1) 30 do ; so_lieu_mau (goc mang 2, d cm, h cm): 30 37,3 18,7 ; 15 69,4 18,0 ; 5 180,3 15,7.
#   Hinh ve DUNG TI LE (3,85 px/cm) theo so kho: d doc mang (2), h = d.sin(goc) (_kiem_so()).
# Du doan (K10: chi cau hoi + hinh, khung ben canh co lua chon): tha bi o cung 20 cm, ha mang (2) 30 -> 15 -> 5 do,
#   quang duong d tren mang (2)?  A. Ngan di ; B. Gan nhu khong doi ; C. Dai ra ro ret (DUNG).
# KHONG tra loi san cau trong bai: hop "Doc so lieu" ngay sau (vi sao h giam khi mang thoai? cot nao chac hon?) ->
#   clip khong giai thich vi sao h giam, khong noi sai so/cot nao tin cay ; Cau 1 (o to thang deu), Cau 3 (hon da
#   nem len) -> chot/bay khong noi "luc khong duy tri chuyen dong", khong noi "het luc nem".
# Bay = hien_tuong_hay_sai[1] "Tuong mang thoai thi bi len duoc cao hon" -> bang h: 30 do 18,7 ; 5 do 15,7 cm.
# Cau chot (ghi trong ghi_chu kho): mang KHONG ma sat, tha bi o do cao 30 cm (tham_so h0 0,05-0,40 m), mang (2) 30 do
#   -> bi len dung 30 cm, d = 30/sin30 = 60 cm. So 30 cm / 60 cm chua tung hien tren man.
from engine import *

ROWS = [(30, 37.3, 18.7), (15, 69.4, 18.0), (5, 180.3, 15.7)]   # so_lieu_mau
H0, A1 = 20.0, 30
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    return [r for r in ROWS if abs(r[1] * math.sin(math.radians(r[0])) - r[2]) > 0.06 or r[2] >= H0]
assert not _kiem_so()

RAMP = (120, 132, 156); RAMP_D = (70, 80, 104); BALL = (90, 98, 120); DRED = (185, 28, 28); NOTE = (60, 64, 84)
S = 3.85                       # px / cm (dung ti le ca chieu ngang lan chieu cao)
JX, JY, GY = 215, 800, 818     # cho noi hai mang ; mat dat
L1, L2 = 48.0, 195.0           # chieu dai mang (1), mang (2) (cm)
R = 15                         # ban kinh bi ve (px)

def c30(a): return math.cos(math.radians(a))
def s30(a): return math.sin(math.radians(a))
def P1(u): return (JX - u * c30(A1) * S, JY - u * s30(A1) * S)
def P2(u, a): return (JX + u * c30(a) * S, JY - u * s30(a) * S)
N1 = (s30(A1), -c30(A1))
def N2(a): return (-s30(a), -c30(a))

def center(s, a):
    """s < 0: tren mang (1), cach cho noi -s cm ; s >= 0: tren mang (2). Lam tron qua cho noi."""
    def c1(u): p = P1(u); return (p[0] + N1[0] * R, p[1] + N1[1] * R)
    def c2(u): p = P2(u, a); n = N2(a); return (p[0] + n[0] * R, p[1] + n[1] * R)
    if -3 < s < 3:
        k = (s + 3) / 6; p, q = c1(3), c2(3)
        return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
    return c1(-s) if s < 0 else c2(s)

def ground(d):
    d.line([(40, GY), (1040, GY)], fill=INK, width=5)
    for x in range(60, 1040, 40): d.line([(x, GY + 4), (x - 18, GY + 24)], fill=GRAY, width=3)

def ramp_poly(p0, p1, n, th=14):
    return [p0, p1, (p1[0] - n[0] * th, p1[1] - n[1] * th), (p0[0] - n[0] * th, p0[1] - n[1] * th)]

def ramps(d, a, alpha=1.0, ghost=False):
    col = A(RAMP, alpha); cd = A(RAMP_D, alpha)
    e1 = P1(L1); e2 = P2(L2, a)
    if not ghost:
        d.rectangle([e1[0] - 6, e1[1] + 10, e1[0] + 6, GY], fill=A(RAMP_D, alpha))
        d.rectangle([e2[0] - 6, e2[1] + 10, e2[0] + 6, GY], fill=A(RAMP_D, alpha))
        d.polygon(ramp_poly(e1, (JX, JY), N1), fill=col); d.line([e1, (JX, JY)], fill=cd, width=5)
    d.polygon(ramp_poly((JX, JY), e2, N2(a)), fill=col); d.line([(JX, JY), e2], fill=cd, width=5)

def h0_line(d, a=30, alpha=1.0, lab=True):
    y = JY - H0 * S; x = 60
    while x < 1000:
        d.line([(x, y), (min(x + 18, 1000), y)], fill=A(ORANGE, alpha), width=4); x += 30
    # nhan ben TRAI cot do dau mang (2), di theo cot khi mang xoay -> cot khong cat chu (cong B 18/11) ;
    # mang 5 do: dinh bi (d = 180 cm) + ngoac d nam ngay duoi duong 20 cm -> nhac nhan len cao dan tu 15 do xuong 5 do
    yo = 40 if a >= 15 else lerp(120, 40, (a - 5) / 10)
    if lab: text(d, (P2(L2, a)[0] - 24, y - yo - 8), "20 cm", 56, ORANGE, anchor="rm", alpha=alpha)
    arrow(d, (1010, JY), (1010, y + 4), A(ORANGE, alpha), w=4, head=14)

def ball(d, c, alpha=1.0):
    if alpha <= 0.02: return
    d.ellipse([c[0] - R, c[1] - R, c[0] + R, c[1] + R], fill=A(BALL, alpha), outline=A(NAVY, alpha), width=3)
    d.ellipse([c[0] - R * 0.5, c[1] - R * 0.6, c[0] - R * 0.05, c[1] - R * 0.15], fill=A(WHITE, 0.7 * alpha))

def peak_mark(d, a, dist, col=ORANGE, alpha=1.0):
    p = P2(dist, a); n = N2(a)
    d.line([(p[0] - n[0] * 6, p[1] - n[1] * 6), (p[0] + n[0] * 44, p[1] + n[1] * 44)], fill=A(col, alpha), width=6)

def d_bracket(d, a, dist, alpha=1.0, off=62, lab=True):
    """Ngoac do d doc mang (2), song song mat mang, phia tren bi."""
    if alpha <= 0.02: return
    n = N2(a); p0, p1 = P2(0, a), P2(dist, a)
    q0 = (p0[0] + n[0] * off, p0[1] + n[1] * off); q1 = (p1[0] + n[0] * off, p1[1] + n[1] * off)
    d.line([q0, q1], fill=A(BLUE, alpha), width=4)
    for q in (q0, q1): d.line([(q[0] - n[0] * 14, q[1] - n[1] * 14), (q[0] + n[0] * 14, q[1] + n[1] * 14)], fill=A(BLUE, alpha), width=4)
    if lab:
        m = ((q0[0] + q1[0]) / 2 + n[0] * 44, (q0[1] + q1[1]) / 2 + n[1] * 44)
        s = f"d = {vn(dist)} cm"; wl = tw(d, s, F(56))
        x = clamp(m[0], 60 + wl / 2, 1020 - wl / 2)
        card(d, (x - wl / 2 - 14, m[1] - 38, x + wl / 2 + 14, m[1] + 38), fill=A(WHITE, 0.9 * alpha), r=16)
        text(d, (x, m[1]), s, 56, BLUE, alpha=alpha)

def count_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem LIEN (tut tung nac 10 %), cao 70 px (brief 27/11)."""
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (175, y, 905, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (175, y, 175 + max(70, 730 * q), y + 70), fill=A(col, a), r=35)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    ground(d); h0_line(d); ramps(d, 30); ball(d, center(-H0 / s30(A1), 30))
    text(d, (P1(L1)[0] - 10, JY - L1 * s30(A1) * S - 70), "máng (1)", 56, NOTE, anchor="lm")
    e2 = P2(L2, 30); text(d, (e2[0] - 30, e2[1] - 50), "máng (2)", 56, NOTE, anchor="rm")
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 106), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 66), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 190), "Hạ máng (2): 30° → 15° → 5°", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 300), "Quãng bi lăn trên máng (2)", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 380), "sẽ thế nào?", 60, INK, alpha=a)
    tc = M[1] + 0.3
    if t > tc: count_bar(d, y0 + 480, t, tc, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh (3 lan tha trong MOT canh) ----------------
ROT, DOWN, UP, BACK = 0.6, 0.9, 1.1, 0.7
def run_state(t, M):
    """-> (k lan tha hien tai, goc mang 2, s vi tri bi, alpha bi, so lan da do xong). Lan k bat dau o M[k]."""
    k = max(0, sum(1 for m in M if t >= m) - 1)
    tk = t - M[k]; a_prev = ROWS[k - 1][0] if k > 0 else ROWS[0][0]; a_k, dk = ROWS[k][0], ROWS[k][1]
    a = lerp(a_prev, a_k, ease(tk / ROT)) if k > 0 else a_k
    s0 = -H0 / s30(A1); t1 = ROT + 0.1; t2 = t1 + DOWN; t3 = t2 + UP; t4 = t3 + 0.3; t5 = t4 + BACK
    al = appear(tk, ROT - 0.2, 0.3) if k > 0 else 1.0
    if tk < t1: s = s0
    elif tk < t2: x = (tk - t1) / DOWN; s = s0 * (1 - x * x)
    elif tk < t3: x = (tk - t2) / UP; s = dk * (1 - (1 - x) ** 2)
    elif tk < t4: s = dk
    else:
        x = clamp((tk - t4) / BACK); s = dk * (1 - x * x)
        if k < 2: al = 1 - clamp((tk - t5 + 0.3) / 0.3)
    done = k + (1 if tk >= t3 else 0)
    return k, a, s, al, done

def chips(d, cur):
    for j, (a, _, _) in enumerate(ROWS):
        x0 = 150 + j * 270; box = (x0, 262, x0 + 240, 342); s = f"{a}°"
        if j == cur: card(d, box, fill=ORANGE, r=40); text(d, (x0 + 120, 302), s, 58, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=40); text(d, (x0 + 120, 302), s, 58, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=40, w=3); text(d, (x0 + 120, 302), s, 58, MUTED)

def table(d, n, y=920, hi=-1, alpha=1.0, hcol=None):
    card(d, (40, y, 1040, y + 440), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    xs = (250, 580, 870)
    for x, s in zip(xs, ("góc máng (2)", "d (cm)", "h (cm)")): text(d, (x, y + 66), s, 56, INK, alpha=alpha)
    d.line([(70, y + 120), (1010, y + 120)], fill=A(LIGHT, alpha), width=4)
    for i in range(n):
        yy = y + 190 + i * 94
        if i == hi: card(d, (70, yy - 42, 1010, yy + 42), fill=A((255, 237, 213), alpha), r=18)
        text(d, (xs[0], yy), f"{ROWS[i][0]}°", 60, INK, alpha=alpha)
        text(d, (xs[1], yy), vn(ROWS[i][1]), 60, hcol or BLUE, alpha=alpha)
        text(d, (xs[2], yy), vn(ROWS[i][2]), 60, PURPLE, alpha=alpha)

def s_do(img, d, t, sc):
    M = sc["M"]; k, a, s, al, done = run_state(t, M)
    chips(d, k); ground(d); h0_line(d, a)
    text(d, (60, 420), "máng có ma sát nhỏ", 56, NOTE, anchor="lm")        # kiem-v1: noi truoc vi sao bi len thap hon
    ramps(d, a)
    if done > k:
        peak_mark(d, a, ROWS[k][1]); d_bracket(d, a, ROWS[k][1], alpha=appear(t - M[k], ROT + 0.1 + DOWN + UP, 0.3))
    ball(d, center(s, a), al)
    table(d, done)

def _kiem_dong_bo():
    """Moi 0,05 s: so hang bang = so lan bi da len toi dinh ; nhan d chi hien khi bi o dinh cua lan dang chieu."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []
    while t < sc["T"]:
        k, a, s, al, done = run_state(t, M)
        tk = t - M[k]; reached = tk >= ROT + 0.1 + DOWN + UP
        if done != k + (1 if reached else 0): bad.append(round(t, 2))
        if reached and abs(s - ROWS[k][1]) > 1e-6 and tk < ROT + 0.1 + DOWN + UP + 0.3: bad.append(("dinh", round(t, 2)))
        if k + 1 < len(M) and M[k + 1] - M[k] < ROT + 0.1 + DOWN + UP + 0.3 + BACK: bad.append(("chong", k))
        t += 0.05
    if M[-1] + ROT + 0.1 + DOWN + UP + 0.6 > sc["T"]: bad.append("lan cuoi qua sat cuoi canh")
    return sorted(set(map(str, bad)))

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    lab = "Đáp án: dài ra rõ rệt"
    pw = tw(d, lab, F(58)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 346), fill=A(NAVY, ka), r=42)
    text(d, (W / 2, 304), lab, 58, WHITE, alpha=ka)
    kr = appear(t, M[1] - 0.1, 0.5)                        # chuyen sang thi nghiem tuong tuong
    ground(d)
    if kr < 1:
        for a, dist, _ in ROWS[:2]: ramps(d, a, alpha=0.35 * (1 - kr), ghost=True)
        ramps(d, 5, alpha=1 - kr)
        for j, (a, dist, _) in enumerate(ROWS):
            peak_mark(d, a, dist, alpha=1 - kr)
            p = P2(dist, a); n = N2(a)
            q = (p[0] + n[0] * 86, p[1] + n[1] * 86 - 10); wl = tw(d, vn(dist), F(56))
            card(d, (q[0] - wl / 2 - 12, q[1] - 36, q[0] + wl / 2 + 12, q[1] + 36), fill=A(WHITE, 0.92 * (1 - kr)), r=16)   # nen sang: khong lan vao mang mo
            text(d, q, vn(dist), 56, BLUE, alpha=1 - kr)
        text(d, (90, 440), "d (cm)", 58, BLUE, anchor="lm", alpha=1 - kr)
    if kr > 0:
        # thi nghiem tuong tuong: mang (2) nam ngang, khong ma sat -> bi lan mai voi van toc khong doi
        e1 = P1(L1)
        d.polygon(ramp_poly(e1, (JX, JY), N1), fill=A(RAMP, kr)); d.line([e1, (JX, JY)], fill=A(RAMP_D, kr), width=5)
        x = JX
        while x < 1030:
            d.line([(x, JY), (min(x + 22, 1030), JY)], fill=A(TEAL, kr), width=6); x += 34
        tt = max(0.0, t - M[1]); u = (tt * 190) % 760; xb = JX + 40 + u   # thang deu; lap lai de hinh khong dung yen
        ball(d, (xb, JY - R - 2), kr * clamp(u / 40) * (1 - clamp((xb - 960) / 60)))
        arrow(d, (620, JY - 90), (900, JY - 90), A(TEAL, kr), w=7, head=22)
        k2 = kr * appear(t, M[1] + 2.1, 0.4)
        y0 = 920 + (1 - k2) * 30
        if k2 > 0:
            card(d, (40, y0, 1040, y0 + 430), fill=A(WHITE, k2), outline=A(GREEN, k2), w=6)
            pw = tw(d, "RÚT RA", F(56)) + 60
            card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 108), fill=A(GREEN, k2), r=40)
            text(d, (W / 2, y0 + 68), "RÚT RA", 56, WHITE, alpha=k2)
            text(d, (W / 2, y0 + 190), "Không ma sát: bi lăn mãi,", 58, INK, alpha=k2)
            text(d, (W / 2, y0 + 275), "vận tốc không đổi", 60, (21, 110, 55), alpha=k2)
            text(d, (W / 2, y0 + 365), "(suy luận, chưa đo)", 56, NOTE, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    """Nhip 1 (0 s): cau sai ; nhip 2 (3,0 s): so do h -> gach ; nhip 3 (M[1]): chua noi duoc."""
    M = sc["M"]
    ground(d); h0_line(d, 5, alpha=appear(t, 0.4, 0.3))
    ramps(d, 30, alpha=0.35, ghost=True); ramps(d, 5)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.4, 0.3) * (1 - k3)
    for a, dist, _ in (ROWS[0], ROWS[2]): ball(d, center(dist, a), 1.0)
    y = 920
    if a1 > 0:
        ke0 = appear(t, 3.4, 0.4); card(d, (40, y, 1040, y + 300 + 220 * ease(ke0)), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)   # kiem-v1: khong de nua the trong
        pw = tw(d, "BẪY", F(56)) + 60
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 108), fill=A(DRED, a1), r=40)
        text(d, (W / 2, y + 68), "BẪY", 56, WHITE, alpha=a1)
        q = "“Máng thoải, bi lên cao hơn”"
        ks = clamp((t - 3.4) / 0.4); f = F(58); lw = tw(d, q, f); yy = y + 200
        text(d, (W / 2, yy), q, 58, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        ke = a1 * appear(t, 3.4, 0.4)
        text(d, (W / 2, y + 330), "30°: h = 18,7 cm", 58, PURPLE, alpha=ke)
        text(d, (W / 2, y + 420), "5°: h = 15,7 cm", 58, PURPLE, alpha=ke)
    if k3 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 100), "Chưa nói được:", 60, NAVY, alpha=k3)
        text(d, (W / 2, y + 240), "Có lực thì vận tốc", 58, INK, alpha=k3)
        text(d, (W / 2, y + 320), "đổi ra sao?", 58, INK, alpha=k3)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """THU NGHI: khong ma sat, tha o 30 cm (ngoai moc 20 cm da chieu), mang (2) 30 do -> d = 60 cm ; hinh dung ti le, d = ?"""
    k1 = appear(t, 0.15, 0.5)
    card(d, (40, 270, 1040, 1380), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 380), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 340), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    text(d, (W / 2, 480), "Không ma sát, thả ở 30 cm.", 60, INK, alpha=k1)
    text(d, (W / 2, 570), "Máng (2) nghiêng 30°.", 60, INK, alpha=k1)
    # hinh: 3,85 px/cm nhu clip ; cho noi (jx, gy)
    jx, gy, sc_ = 440, 1130, S * 1.6
    c, sn = c30(30), s30(30)
    e1 = (jx - 66 * c * sc_, gy - 66 * sn * sc_); e2 = (jx + 66 * c * sc_, gy - 66 * sn * sc_)
    d.line([(80, gy), (1000, gy)], fill=A(INK, k1), width=5)
    for e in (e1, e2): d.rectangle([e[0] - 6, e[1] + 10, e[0] + 6, gy], fill=A(RAMP_D, k1))
    d.polygon(ramp_poly(e1, (jx, gy), N1), fill=A(RAMP, k1)); d.line([e1, (jx, gy)], fill=A(RAMP_D, k1), width=5)
    d.polygon(ramp_poly((jx, gy), e2, N2(30)), fill=A(RAMP, k1)); d.line([(jx, gy), e2], fill=A(RAMP_D, k1), width=5)
    yh = gy - 30 * sc_; x = 100
    while x < 980:
        d.line([(x, yh), (min(x + 18, 980), yh)], fill=A(ORANGE, k1), width=4); x += 30
    text(d, (1000, yh + 42), "30 cm", 56, ORANGE, anchor="rm", alpha=k1)
    p0 = (jx - 60 * c * sc_, gy - 60 * sn * sc_); ball(d, (p0[0] + N1[0] * R, p0[1] + N1[1] * R), k1)
    n = N2(30); q0 = (jx + n[0] * 60, gy + n[1] * 60)
    tt = 0.5 + 0.5 * math.sin(2 * math.pi * 0.6 * t)                     # ngoac d = ? co gian nhe: hinh khong dung yen, khong lo do dai
    L = (35 + 20 * tt) * sc_; q1 = (q0[0] + c * L, q0[1] - sn * L)
    d.line([q0, q1], fill=A(BLUE, k1), width=4)
    for q in (q0, q1): d.line([(q[0] - n[0] * 14, q[1] - n[1] * 14), (q[0] + n[0] * 14, q[1] + n[1] * 14)], fill=A(BLUE, k1), width=4)
    wl = tw(d, "d = ?", F(60)); lx, ly = q1[0] + 20, q1[1] - 40
    card(d, (lx - 10, ly - 38, lx + wl + 10, ly + 38), fill=A(WHITE, 0.92 * k1), r=16)      # nen sang: nhan di dong qua duong 30 cm
    text(d, (lx, ly), "d = ?", 60, BLUE, anchor="lm", alpha=k1)
    count_bar(d, 1220, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + m, "tap") for m in do["M"]]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 3.4, "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-dl1-newton-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật 1 Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hòn bi trên hai máng nghiêng", draw=s_hook, tail=0.3, caps=[
   ("Luôn thả bi ở cùng độ cao 20 cm.", 3.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Máng (2) nghiêng 30°, đo d và h.", 3.8),
   ("Hạ máng (2) xuống 15°.", 3.8),
   ("Hạ tiếp xuống 5°.", 3.7)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So ba giá trị d.", 3.4),
   ("Nếu máng (2) nằm ngang?", 6.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 5.2),
   ("Câu còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.6)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
