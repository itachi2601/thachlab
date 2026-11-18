# Clip: tn-l11-dotocdoam-03 - Do toc do am bang do tre giua hai micro noi chung mot may ghi (18/11/2026, lo 5)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dotocdoam-03.json -> so_lieu_mau (d m, dt ms, v m/s):
#   2,0 5,8 344,8 ; 4,0 11,7 341,9 ; 6,0 17,5 342,9. Mo hinh v = 343 m/s; v = 331 + 0,6.t. Kiem: _kiem_so().
# Bo cuc (hai micro + truc thoi gian tre; KHAC dotansoam2 la dang song theo t): tren = hai micro thang hang, vo tay sat
#   micro 1, mat song lan ra; giua = man may ghi hai ranh (micro 1, micro 2) chung mot truc t (ms), gai 2 hien dung luc
#   mat song cham micro 2, ngoac Dt; duoi = bang d - Dt (- v o canh Rut ra).
# Du doan (khung 6 o): "Doi micro 2 xa gap doi (2 m -> 4 m). Gai thu hai tre so voi gai dau the nao?"
#   A. tre gap doi  B. tre nhu cu  C. tre gap bon  D. tre bang mot nua   -> dap an A (5,8 -> 11,7 ms).
#   Hop Du doan trong mp4 chi co cau hoi + hinh hai micro (K10), chua co may ghi/so.
# Bay = hien_tuong_hay_sai[0]: hai dien thoai ghi rieng -> dong ho lech nhau.
# Cau chot (ghi trong kho ghi_chu): phong 35 do C, van d = 6,00 m -> v = 331 + 0,6.35 = 352 m/s, Dt = 6/352 = 17,0 ms
#   (17,05) -> ngan hon 17,5 ms co 0,5 ms. 35 do C chua hien tren man; khong suy duoc bang mot phep tinh tu so da hien.
# Cau ngay sau hop trong bai (Bay 1, ong cong huong l1/l2) khong lien quan clip.
from engine import *
import copy

ROWS = [(2.0, 5.8, 344.8), (4.0, 11.7, 341.9), (6.0, 17.5, 342.9)]
V0 = 343
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

SCR_BG = (18, 26, 48); TR1 = (96, 165, 250); TR2 = (74, 222, 128); GRID = (52, 64, 96); SCR_TXT = (190, 200, 225)
SEL = (250, 204, 21); DGREEN = (10, 80, 40); HL = (255, 237, 213); WIRE = (60, 66, 92); SKIN = (240, 190, 150)

# ---------------- hai micro ----------------
MX0, PXM, MY, HX = 250, 115, 420, 160  # micro 1 o x = 250; 1 m = 115 px; dau micro o y = 420; tay vo sat micro 1 o x = 160
def mx(dm): return MX0 + PXM * dm

def mic(d, x, label, alpha=1.0, ghost=False):
    c = A(GRAY if ghost else NAVY, alpha)
    d.line([(x, MY + 26), (x, 540)], fill=c, width=6)
    d.line([(x - 36, 540), (x + 36, 540)], fill=c, width=8)
    d.rounded_rectangle([x - 22, MY - 34, x + 22, MY + 30], radius=22, fill=A(WHITE, alpha) if ghost else c,
                        outline=c, width=5)
    if label: text(d, (x, MY - 80), label, 40, GRAY if ghost else NAVY, alpha=alpha)

def hands(d, x, y, k=0.0, alpha=1.0):
    """Hai ban tay vo vao nhau: k = 0 xa, 1 cham. Toa phat ra khi cham."""
    g = 34 * (1 - k)
    d.ellipse([x - 40 - g, y - 34, x - 4 - g, y + 34], fill=A(SKIN, alpha), outline=A(NAVY, alpha), width=3)
    d.ellipse([x + 4 + g, y - 34, x + 40 + g, y + 34], fill=A(SKIN, alpha), outline=A(NAVY, alpha), width=3)

def scene_top(d, d2, wave_r=None, clap_k=0.0, flash=0.0, show_d=True):
    d.line([(60, 560), (1020, 560)], fill=LIGHT, width=4)
    hands(d, HX, MY, clap_k)
    if flash > 0:
        for a in (-50, -20, 20, 50):
            r0, r1 = 52, 52 + 34 * flash
            ang = math.radians(180 + a)
            d.line([(HX + r0 * math.cos(ang), MY + r0 * math.sin(ang)),
                    (HX + r1 * math.cos(ang), MY + r1 * math.sin(ang))], fill=ORANGE, width=5)
    if wave_r is not None and wave_r > 0:
        cx, cy = HX, MY
        for j, al in ((0, 0.9), (1, 0.5), (2, 0.25)):
            r = wave_r - 26 * j
            if r <= 10: continue
            ha = min(38, math.degrees(math.asin(min(1, 150 / r))))     # khong tran xuong may ghi
            d.arc([cx - r, cy - r, cx + r, cy + r], start=-ha, end=ha, fill=A(ORANGE, al), width=6)
    mic(d, mx(0), "micro 1"); mic(d, mx(d2), "micro 2")
    if show_d:
        y = 588; x0, x1 = mx(0), mx(d2)
        arrow(d, ((x0 + x1) / 2, y), (x0 + 4, y), MUTED, w=4, head=16); arrow(d, ((x0 + x1) / 2, y), (x1 - 4, y), MUTED, w=4, head=16)
        text(d, ((x0 + x1) / 2, y + 44), f"d = {vn(d2)} m", 42, INK)

# ---------------- man may ghi: hai ranh chung mot truc t ----------------
RX0, RX1 = 300, 960; TAU_MAX = 20.0
def rx(tau): return RX0 + (RX1 - RX0) * tau / TAU_MAX
RY0, RY1 = 690, 1115; TY1, TY2, TAX = 800, 955, 1050
def burst(tau, t0, amp):
    u = tau - t0
    if u < 0: return 0.0
    return amp * math.exp(-u / 0.55) * math.sin(2 * math.pi * u / 0.32) * min(1, u / 0.04)

def recorder(d, tau, dt, show_dt):
    card(d, (60, RY0, 1020, RY1), fill=SCR_BG, r=30)
    text(d, (90, RY0 + 34), "một máy ghi chung", 40, SCR_TXT, bold=False, anchor="lm")
    for y, lab, col in ((TY1, "micro 1", TR1), (TY2, "micro 2", TR2)):
        text(d, (90, y), lab, 40, col, anchor="lm")
        d.line([(RX0, y), (RX1, y)], fill=GRID, width=2)
    d.line([(RX0, TAX), (RX1 + 10, TAX)], fill=SCR_TXT, width=3)
    for tk in (0, 10, 20):
        d.line([(rx(tk), TAX), (rx(tk), TAX - 12)], fill=SCR_TXT, width=3)
        text(d, (rx(tk), TAX + 32), str(tk) if tk < 20 else "20 ms", 40, SCR_TXT, bold=False)
    if tau is None: return
    for y, t0, col in ((TY1, 0.0, TR1), (TY2, dt, TR2)):
        pts = []; s = 0.0
        while s <= tau:
            pts.append((rx(s), y - burst(s, t0, 62))); s += 0.04
        if len(pts) > 1: d.line(pts, fill=col, width=4, joint="curve")
    d.line([(rx(tau), RY0 + 70), (rx(tau), TAX)], fill=(120, 130, 160), width=2)   # con tro ghi
    if show_dt:
        x0, x1, yb = rx(0), rx(dt), (TY1 + TY2) / 2
        for xx in (x0, x1):
            for yy in range(int(TY1 - 40), int(TY2 + 40), 18): d.line([(xx, yy), (xx, yy + 9)], fill=SEL, width=3)
        arrow(d, ((x0 + x1) / 2, yb), (x0 + 3, yb), SEL, w=4, head=14); arrow(d, ((x0 + x1) / 2, yb), (x1 - 3, yb), SEL, w=4, head=14)
        lab = f"Δt = {vn(dt)} ms"; lw = tw(d, lab, F(42)) + 24; cx = max(RX0 + lw / 2, (x0 + x1) / 2)
        d.rectangle([cx - lw / 2, yb - 26, cx + lw / 2, yb + 26], fill=SCR_BG)
        text(d, (cx, yb), lab, 42, SEL)

# ---------------- canh 1: Du doan (K10: cau hoi + hinh hai micro, chua co may ghi) ----------------
Q_AT = 1.1
def s_hook(img, d, t, sc):
    scene_top(d, 2.0, show_d=False)
    mic(d, mx(4.0), "", ghost=True)
    arrow(d, (mx(2.0) + 50, MY), (mx(4.0) - 50, MY), GRAY, w=5, head=20)
    text(d, (mx(2.0), 610), "2 m", 42, INK); text(d, (mx(4.0), 610), "4 m", 42, GRAY)
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 680 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 490), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 215, "Dời micro 2 từ 2 m ra 4 m.\nTiếng vỗ tay tới micro 2 trễ\nso với micro 1 thế nào?",
          44, INK, maxw=920, alpha=a)
    text(d, (W / 2, y0 + 375), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 438, 940, y0 + 450], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 438, 140 + 800 * (1 - p), y0 + 450], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
TR = [(0.8, 2.2), (4.4, 1.8), (7.2, 1.8)]   # (luc vo tay, thoi gian quet 0 -> 20 ms tren may ghi) moi lan
MOVE = 0.6                                  # doi micro 2 truoc lan k (k >= 1): xong truoc vo tay 0,2 s
T_ANS = 9.6
def do_state(t):
    """-> (lan k, d micro 2 dang dat, tau ms tren may ghi hoac None, so hang da ghi, hien Dt?)."""
    k = 0
    for i in range(1, 3):
        if t >= TR[i][0] - 0.2 - MOVE: k = i
    s, g = TR[k]
    d2 = ROWS[k][0]
    if k > 0:
        q = clamp((t - (s - 0.2 - MOVE)) / MOVE)
        d2 = lerp(ROWS[k - 1][0], ROWS[k][0], ease(q))
    rows = 0
    for i, (s2, g2) in enumerate(TR):
        if t >= s2 + g2 * ROWS[i][1] / TAU_MAX - 1e-9: rows = i + 1
    tau = None if t < s else min(TAU_MAX, (t - s) / g * TAU_MAX)
    show_dt = tau is not None and tau >= ROWS[k][1] - 1e-9
    return k, d2, tau, rows, show_dt

TX = [200, 520, 840]; RH = 86
def table(d, rows, ty0, kv=None, hl=-1):
    if rows <= 0: return                         # an bang toi khi co hang 1
    card(d, (60, ty0 - 56, 1020, ty0 + 46 + rows * RH + 14), fill=WHITE, outline=LIGHT, w=3)   # co theo so hang
    text(d, (TX[0], ty0), "d (m)", 40, INK); text(d, (TX[1], ty0), "Δt (ms)", 40, INK)
    if kv is not None: text(d, (TX[2], ty0), "v (m/s)", 40, INK)
    d.line([(80, ty0 + 36), (1000, ty0 + 36)], fill=LIGHT, width=3)
    for j in range(rows):
        y = ty0 + 46 + RH * j + RH / 2
        if j == hl: d.rounded_rectangle([80, y - 36, 1000, y + 36], radius=14, fill=HL)
        dd, dt, v = ROWS[j]
        text(d, (TX[0], y), vn(dd), 44, NAVY); text(d, (TX[1], y), vn(dt), 44, INK)
        if kv is not None and kv[j] > 0: text(d, (TX[2], y), vn(v), 44, BLUE, alpha=kv[j])

def s_do(img, d, t, sc):
    k, d2, tau, rows, show_dt = do_state(t)
    s, g = TR[k]
    clap_k = clamp((t - (s - 0.25)) / 0.25) if t < s + 0.3 else 1 - clamp((t - s - 0.3) / 0.3)
    flash = clamp(1 - abs(t - s - 0.1) / 0.25) if abs(t - s - 0.1) < 0.25 else 0.0
    wr = None
    if tau is not None:
        wr = PXM * ROWS[k][0] * tau / ROWS[k][1] + (MX0 - HX)   # mat song cham micro 2 dung luc tau = Dt
        if wr > 1040 - HX: wr = None                          # cung song khong vuot x = 1040
    scene_top(d, d2, wave_r=wr, clap_k=clap_k, flash=flash)
    recorder(d, tau, ROWS[k][1], show_dt)
    table(d, rows, 1200, hl=rows - 1 if show_dt else -1)
    ka = appear(t, T_ANS, 0.15)
    if ka > 0:
        card(d, (60, 1535, 1020, 1640), fill=A((21, 110, 52), ka), r=30)
        text(d, (W / 2, 1587), "ĐÁP ÁN · trễ gấp đôi: 5,8 → 11,7 ms", 42, WHITE, alpha=ka)

# ---------------- canh 3: Rut ra ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.2, 0.45)
    card(d, (50, 250, 1030, 560), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
    text(d, (W / 2, 330), "v = d / Δt   (Δt tính bằng giây)", 46, BLUE, alpha=k1)
    text(d, (W / 2, 470), "6,0 / 0,0175 s ≈ 342,9 m/s", 50, INK, alpha=appear(t, 0.9, 0.45))
    kv = [appear(t, M[1] - 0.2, 0.4), appear(t, M[1] + 0.3, 0.4), appear(t, 0.9, 0.4)]
    table(d, 3, 690, kv=kv, hl=2 if t < M[1] - 0.2 else -1)
    km = appear(t, M[1] + 0.9, 0.45)
    if km > 0:
        card(d, (60, 1080, 1020, 1190), fill=A((236, 253, 243), km), outline=A(GREEN, km), w=5)
        text(d, (W / 2, 1135), "Cả ba lần: v ≈ 343 m/s", 48, DGREEN, alpha=km)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y = 1250 + (1 - k3) * 20
        card(d, (50, y, 1030, y + 250), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 55), "Chưa nói được", 42, NAVY, alpha=k3)
        ctext(d, y + 165, "Âm cao, âm trầm: cùng tốc độ?", 44, INK, maxw=900, alpha=k3 * appear(t, M[2] + 0.3, 0.4))

# ---------------- canh 4: Bay - hai dien thoai ghi rieng ----------------
def phone(d, x, y, ang, alpha, lab):
    card(d, (x - 110, y - 170, x + 110, y + 170), fill=A(NAVY, alpha), r=30)
    card(d, (x - 92, y - 140, x + 92, y + 140), fill=A(WHITE, alpha), r=14)
    cx, cy, r = x, y - 30, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=A(NAVY, alpha), width=5)
    for a2, L in ((ang, 46), (ang * 0.08 - 90, 32)):
        d.line([(cx, cy), (cx + L * math.cos(math.radians(a2)), cy + L * math.sin(math.radians(a2)))], fill=A(RED, alpha), width=5)
    text(d, (x, y + 90), lab, 40, INK, alpha=alpha)

def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    card(d, (40, 260, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(RED, a1), r=32)
    text(d, (W / 2, 322), "BẪY", 38, WHITE, alpha=a1)
    s1 = "Hai điện thoại, mỗi máy ghi riêng"
    text(d, (W / 2, 440), s1, 46, RED, alpha=a1)
    ks = clamp((t - (M[1] + 0.5)) / 0.4)
    if ks > 0:
        lw = tw(d, s1, F(46))
        d.line([(W / 2 - lw / 2 - 8, 442), (W / 2 - lw / 2 - 8 + (lw + 16) * ks, 442)], fill=RED, width=6)
        text(d, (W / 2, 535), "✗ hai đồng hồ lệch nhau", 44, RED, alpha=ks)
    a2 = appear(t, 0.3, 0.4)
    if a2 > 0:   # hai dien thoai, kim dong ho lech nhau
        phone(d, 300, 860, -90, a2, "máy 1"); phone(d, 780, 860, -20, a2, "máy 2")
        text(d, (540, 830), "≠", 70, RED, alpha=a2)
    ka = appear(t, M[1] + 1.3, 0.5)
    if ka > 0:
        card(d, (60, 1110, 1020, 1410), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
        text(d, (W / 2, 1190), "✓ Hai micro, một máy ghi", 48, DGREEN, alpha=ka)
        text(d, (W / 2, 1310), "Chung một đồng hồ", 44, INK, alpha=ka)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 290, 1020, 590), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 440, "Độ trễ Δt tăng tỉ lệ\nvới khoảng cách d", 50, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 2.9, 0.5)
    yb = lerp(1000, 1270, kh)                     # hop THU NGHI co theo noi dung, dai ra khi goi y hien
    card(d, (40, 650, 1040, yb), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 680, W / 2 + pw / 2, 744), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 712), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 865, "Phòng 35 °C, vẫn d = 6,0 m\n(17,5 ms đo ở 20 °C).\nΔt đổi thế nào, cỡ bao nhiêu?", 44, INK, maxw=950, alpha=appear(t, M[0] + 0.4, 0.5))
    if kh <= 0: return
    card(d, (110, 1010, 970, 1230), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1065, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1160, "v ≈ 331 + 0,6·t (t tính bằng °C)", 42, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.9, "ding")]
    out += [(do["t0"] + s, "tap") for s, g in TR]
    out += [(do["t0"] + s + g * ROWS[i][1] / TAU_MAX, "tick") for i, (s, g) in enumerate(TR)]
    out += [(do["t0"] + T_ANS, "ding"), (b["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return sorted(out)

# ---------------- kiem so va dong bo ----------------
def _kiem_so():
    bad = []
    for dd, dt, v in ROWS:
        if abs(dd / (dt / 1000) - v) > 0.05: bad.append(("v", dd, dt, v))
        if abs(dd / V0 * 1000 - dt) > 0.06: bad.append(("dt xa mo hinh", dd, dt))
    if abs(ROWS[1][1] / ROWS[0][1] - 2) > 0.05: bad.append("dap an gap doi")
    if abs(331 + 0.6 * 20 - V0) > 0.5: bad.append("mo hinh 20 do C")
    v35 = 331 + 0.6 * 35; dt35 = 6.0 / v35 * 1000                      # cau chot
    if not (abs(v35 - 352) < 0.01 and abs(dt35 - 17.05) < 0.01 and 0.4 < 17.5 - dt35 < 0.5): bad.append(("chot", v35, dt35))
    return bad

def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, d2, tau, rows, show_dt = do_state(t)
        if tau is not None and abs(d2 - ROWS[k][0]) > 1e-9: bad.append((round(t, 2), "micro chua toi cho khi vo tay"))
        if show_dt != (rows == k + 1): bad.append((round(t, 2), "Dt <-> hang", k, rows))
        if tau is not None:     # mat song cham micro 2 dung luc gai 2 (tau = Dt)
            r_mic = PXM * ROWS[k][0] + (MX0 - HX); wr = PXM * ROWS[k][0] * tau / ROWS[k][1] + (MX0 - HX)
            if (wr >= r_mic - 1e-6) != (tau >= ROWS[k][1] - 1e-6): bad.append((round(t, 2), "mat song"))
        if rows > k + 1: bad.append((round(t, 2), "hang som"))
        t += 0.05
    if T_ANS < TR[-1][0] + TR[-1][1]: bad.append("dap an truoc lan do cuoi")
    return bad

CLIP = dict(id="tn-l11-dotocdoam-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo tốc độ âm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai micro, một tiếng vỗ tay", draw=s_hook, tail=0.4, caps=[
   ("Vỗ tay sát micro 1.", 2.6),
   ("Nghĩ trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Máy ghi vẽ hai gai âm.", 4.6),
   ("Dời micro 2 xa dần.", 6.0)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("Đổi Δt ra giây rồi chia.", 2.8),
   ("Ba lần, cùng một tốc độ.", 2.8),
   ("Còn bỏ ngỏ.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=1.0, caps=[
   ("Lỗi hay gặp.", 2.5),
   ("Mỗi máy một đồng hồ riêng.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__":
    print("số lệch:", _kiem_so() or "không")
    print("lệch đồng bộ:", _kiem_dong_bo() or "không")
