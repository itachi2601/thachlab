# Clip: tn-l11-dotocdoam-03 - Do toc do am bang do tre giua hai micro noi chung mot may ghi (18/11/2026, lo 5)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dotocdoam-03.json -> so_lieu_mau (d m, dt ms, v m/s):
#   2,0 5,8 344,8 ; 4,0 11,7 341,9 ; 6,0 17,5 342,9. Mo hinh v = 343 m/s. Kiem: _kiem_so().
# Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 56 px, <= 180 tu/phut moi canh, nhip >= 2 s, K10 ("Dung lai, tu doan."),
#   dem 5 o, the CHUA NOI DUOC >= 4 s, nhip Bay >= 3 s, man chot khong cong thuc/goi y.
# Bo cuc: tren = hai micro thang hang, vo tay sat micro 1, mat song lan ra; giua = man may ghi hai ranh chung mot truc
#   t (ms), gai 2 hien dung luc mat song cham micro 2, ngoac Dt; duoi = bang d - Dt (- v o canh Rut ra).
# Du doan: doi micro 2 tu 2 m ra 4 m, tieng vo toi micro 2 tre doi ra sao? -> gap doi (5,8 -> 11,7 ms).
#   Hop exp trong bai chi neu d = 6,00 m, Dt = 17,5 ms (khong lo ti le).
# Bay = hien_tuong_hay_sai[0]: hai dien thoai ghi rieng -> dong ho lech nhau.
# CHUA NOI DUOC: am cao, am tram cung toc do? (Bay 3 cua bai tra loi sau).
# THU NGHI (DOI so voi ban 1): vo tay o CHINH GIUA hai micro cach 6,0 m -> hai gai cung luc, Dt = 0 (khong hien so 0).
#   Ca cu (phong 35 °C, v = 331 + 0,6.t) bo vi: can cong thuc + phep chia, va trung chu de "Thu suc: doi nhiet do" cua bai.
#   Kho tn-l11-dotocdoam-03.json so_lieu_mau.ghi_chu van ghi ca 35 °C -> bao phien chinh sua kho.
from engine import *
import copy

ROWS = [(2.0, 5.8, 344.8), (4.0, 11.7, 341.9), (6.0, 17.5, 342.9)]
V0 = 343
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

SCR_BG = (18, 26, 48); TR1 = (96, 165, 250); TR2 = (74, 222, 128); GRID = (52, 64, 96); SCR_TXT = (205, 214, 235)
SEL = (250, 204, 21); DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8); HL = (255, 237, 213)
SKIN = (240, 190, 150); FS = 58

def pill(d, cx, cy, s, fill, alpha=1.0, size=FS, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(LIGHT, a), r=18, w=4)

# ---------------- hai micro ----------------
MX0, PXM, MY, HX = 230, 118, 420, 140  # micro 1 o x = 230; 1 m = 118 px; dau micro o y = 420; tay vo sat micro 1
def mx(dm): return MX0 + PXM * dm

def mic(d, x, label, alpha=1.0, ghost=False):
    c = A(GRAY if ghost else NAVY, alpha)
    d.line([(x, MY + 26), (x, 540)], fill=c, width=6)
    d.line([(x - 36, 540), (x + 36, 540)], fill=c, width=8)
    d.rounded_rectangle([x - 22, MY - 34, x + 22, MY + 30], radius=22, fill=A(WHITE, alpha) if ghost else c,
                        outline=c, width=5)
    if label: text(d, (min(x, 915), MY - 84), label, 56, NAVY, alpha=alpha)

def hands(d, x, y, k=0.0, alpha=1.0):
    g = 34 * (1 - k)
    d.ellipse([x - 40 - g, y - 34, x - 4 - g, y + 34], fill=A(SKIN, alpha), outline=A(NAVY, alpha), width=3)
    d.ellipse([x + 4 + g, y - 34, x + 40 + g, y + 34], fill=A(SKIN, alpha), outline=A(NAVY, alpha), width=3)

def waves(d, cx, cy, wave_r, both=False):
    for j, al in ((0, 0.9), (1, 0.5), (2, 0.25)):
        r = wave_r - 26 * j
        if r <= 10: continue
        ha = min(38, math.degrees(math.asin(min(1, 150 / r))))
        d.arc([cx - r, cy - r, cx + r, cy + r], start=-ha, end=ha, fill=A(ORANGE, al), width=6)
        if both: d.arc([cx - r, cy - r, cx + r, cy + r], start=180 - ha, end=180 + ha, fill=A(ORANGE, al), width=6)

def scene_top(d, d2, wave_r=None, clap_k=0.0, flash=0.0, show_d=True):
    d.line([(60, 560), (1020, 560)], fill=LIGHT, width=4)
    hands(d, HX, MY, clap_k)
    if flash > 0:
        for a in (-50, -20, 20, 50):
            r0, r1 = 52, 52 + 34 * flash; ang = math.radians(180 + a)
            d.line([(HX + r0 * math.cos(ang), MY + r0 * math.sin(ang)),
                    (HX + r1 * math.cos(ang), MY + r1 * math.sin(ang))], fill=ORANGE, width=5)
    if wave_r is not None and wave_r > 0: waves(d, HX, MY, wave_r)
    mic(d, mx(0), "micro 1"); mic(d, mx(d2), "micro 2")
    if show_d:
        y = 590; x0, x1 = mx(0), mx(d2)
        arrow(d, ((x0 + x1) / 2, y), (x0 + 4, y), NAVY, w=4, head=16); arrow(d, ((x0 + x1) / 2, y), (x1 - 4, y), NAVY, w=4, head=16)
        text(d, ((x0 + x1) / 2, y + 50), f"d = {vn(d2)} m", 56, INK)

# ---------------- man may ghi: hai ranh chung mot truc t ----------------
RX0, RX1 = 330, 960; TAU_MAX = 20.0
def rx(tau): return RX0 + (RX1 - RX0) * tau / TAU_MAX
RY0, RY1 = 680, 1140; TY1, TY2, TAX = 815, 960, 1060
def burst(tau, t0, amp):
    u = tau - t0
    if u < 0: return 0.0
    return amp * math.exp(-u / 0.55) * math.sin(2 * math.pi * u / 0.32) * min(1, u / 0.04)

def recorder(d, tau, dt, show_dt):
    card(d, (60, RY0, 1020, RY1), fill=SCR_BG, r=30)
    text(d, (W / 2, RY0 + 46), "một máy ghi chung", 56, SCR_TXT)
    for y, lab, col in ((TY1, "mic 1", TR1), (TY2, "mic 2", TR2)):
        text(d, (90, y), lab, 56, col, anchor="lm")
        d.line([(RX0, y), (RX1, y)], fill=GRID, width=2)
    d.line([(RX0, TAX), (RX1 + 10, TAX)], fill=SCR_TXT, width=3)
    for tk in (0, 10, 20):
        d.line([(rx(tk), TAX), (rx(tk), TAX - 12)], fill=SCR_TXT, width=3)
        text(d, (rx(tk) - (40 if tk == 20 else 0), TAX + 40), str(tk) if tk < 20 else "20 ms", 56, SCR_TXT)
    if tau is None: return
    for y, t0, col in ((TY1, 0.0, TR1), (TY2, dt, TR2)):
        pts = []; s = 0.0
        while s <= tau:
            pts.append((rx(s), y - burst(s, t0, 62))); s += 0.04
        if len(pts) > 1: d.line(pts, fill=col, width=4, joint="curve")
    d.line([(rx(tau), RY0 + 90), (rx(tau), TAX)], fill=(120, 130, 160), width=2)
    if show_dt:
        x0, x1, yb = rx(0), rx(dt), (TY1 + TY2) / 2
        for xx in (x0, x1):
            for yy in range(int(TY1 - 40), int(TY2 + 40), 18): d.line([(xx, yy), (xx, yy + 9)], fill=SEL, width=3)
        arrow(d, ((x0 + x1) / 2, yb), (x0 + 3, yb), SEL, w=4, head=14); arrow(d, ((x0 + x1) / 2, yb), (x1 - 3, yb), SEL, w=4, head=14)
        lab = f"Δt = {vn(dt)} ms"; lw = tw(d, lab, F(56)) + 24; cx = max(RX0 + lw / 2, (x0 + x1) / 2)
        cx = min(cx, 1010 - lw / 2)
        d.rectangle([cx - lw / 2, yb - 34, cx + lw / 2, yb + 34], fill=SCR_BG)
        text(d, (cx, yb), lab, 56, SEL)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    wr = ((t * 260) % 900) + 40                                  # tieng vo lap lai, song lan ra
    scene_top(d, 2.0, wave_r=wr, clap_k=1.0 if wr < 120 else 0.0, show_d=False)
    mic(d, mx(4.0), "", ghost=True)
    arrow(d, (mx(2.0) + 50, MY + 10), (mx(4.0) - 50, MY + 10), NAVY, w=5, head=20)
    text(d, (mx(2.0), 620), "2 m", 56, INK); text(d, (mx(4.0), 620), "4 m", 56, INK)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 760 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 185), "Dời micro 2 từ 2 m ra 4 m.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "Tiếng vỗ tới micro 2", 64, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 370), "trễ đổi ra sao?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 450, t, M[1], sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
TR = [(1.5, 2.0), (4.6, 1.8), (7.3, 1.8)]   # (luc vo tay, thoi gian quet 0 -> 20 ms tren may ghi) moi lan
MOVE = 0.6
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
    if rows <= 0: return
    card(d, (60, ty0 - 56, 1020, ty0 + 46 + rows * RH + 14), fill=WHITE, outline=LIGHT, w=3)
    text(d, (TX[0], ty0), "d (m)", 56, INK); text(d, (TX[1], ty0), "Δt (ms)", 56, INK)
    if kv is not None: text(d, (TX[2], ty0), "v (m/s)", 56, INK)
    d.line([(80, ty0 + 38), (1000, ty0 + 38)], fill=LIGHT, width=3)
    for j in range(rows):
        y = ty0 + 46 + RH * j + RH / 2
        if j == hl: d.rounded_rectangle([80, y - 38, 1000, y + 38], radius=14, fill=HL)
        dd, dt, v = ROWS[j]
        text(d, (TX[0], y), vn(dd), 56, NAVY); text(d, (TX[1], y), vn(dt), 56, INK)
        if kv is not None and kv[j] > 0: text(d, (TX[2], y), vn(v), 56, BLUE, alpha=kv[j])

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    k, d2, tau, rows, show_dt = do_state(t)
    s, g = TR[k]
    clap_k = clamp((t - (s - 0.25)) / 0.25) if t < s + 0.3 else 1 - clamp((t - s - 0.3) / 0.3)
    flash = clamp(1 - abs(t - s - 0.1) / 0.25) if abs(t - s - 0.1) < 0.25 else 0.0
    wr = None
    if tau is not None:
        wr = PXM * ROWS[k][0] * tau / ROWS[k][1] + (MX0 - HX)
        if wr > 1040 - HX: wr = None
    scene_top(d, d2, wave_r=wr, clap_k=clap_k, flash=flash)
    recorder(d, tau, ROWS[k][1], show_dt)
    table(d, rows, 1240, hl=rows - 1 if show_dt else -1)

# ---------------- canh 3: Rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k1 = 1.0
    card(d, (50, 250, 1030, 560), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
    text(d, (W / 2, 330), "v = d : Δt (Δt ra giây)", 60, BLUE, alpha=k1)
    text(d, (W / 2, 470), "6,0 : 0,0175 ≈ 342,9 m/s", 60, INK, alpha=k1)
    kv = [appear(t, M[1] - 0.2, 0.4), appear(t, M[1] - 0.2, 0.4), appear(t, 0.2, 0.4)]
    table(d, 3, 690, kv=kv, hl=2 if t < M[1] - 0.2 else -1)
    if t > M[1]:                                                    # cham nhay qua ba hang v
        u = (t - M[1]) * 0.8 % 2.0; u = u if u < 1 else 2 - u          # khung xanh truot len xuong qua ba hang
        yc = 690 + 46 + RH / 2 + 2 * RH * ease(u)
        d.rounded_rectangle([70, yc - 42, 1010, yc + 42], radius=16, outline=BLUE, width=6)
    km = appear(t, M[1] - 0.2, 0.45)
    if km > 0:
        card(d, (60, 1080, 1020, 1200), fill=A((236, 253, 243), km), outline=A(GREEN, km), w=5)
        text(d, (W / 2, 1140), "Cả ba lần: v ≈ 343 m/s", 60, DGREEN, alpha=km)

# ---------------- canh 4: Bay - hai dien thoai ghi rieng + CHUA NOI DUOC ----------------
B2 = 3.4
def phone(d, x, y, ang, alpha, lab):
    card(d, (x - 120, y - 180, x + 120, y + 180), fill=A(NAVY, alpha), r=30)
    card(d, (x - 102, y - 150, x + 102, y + 150), fill=A(WHITE, alpha), r=14)
    cx, cy, r = x, y - 40, 66
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=A(NAVY, alpha), width=5)
    for a2, L in ((ang, 50), (ang * 0.08 - 90, 34)):
        d.line([(cx, cy), (cx + L * math.cos(math.radians(a2)), cy + L * math.sin(math.radians(a2)))], fill=A(DRED, alpha), width=5)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k3 = appear(t, M[2] - 0.7, 0.45); a1 = 1.0 - k3
    if a1 > 0:
        card(d, (40, 250, 1040, 1300), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 320, "BẪY", DRED, a1)
        q = ("Hai điện thoại,", "mỗi máy ghi riêng")
        for yy, s in zip((450, 540), q): text(d, (W / 2, yy), s, 64, DRED, alpha=a1)
        ks = clamp((t - B2) / 0.5)
        if ks > 0:
            for yy, s in zip((454, 544), q):
                lw = tw(d, s, F(64))
                d.line([(W / 2 - lw / 2 - 6, yy), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy)], fill=A(DRED, 0.85 * a1), width=5)
        ang = t * 120                                                # hai kim chay, lech pha nhau
        phone(d, 290, 860, ang - 90, a1, "máy 1"); phone(d, 790, 860, ang - 20, a1, "máy 2")
        kk = appear(t, B2, 0.4) * a1
        if kk > 0:
            text(d, (W / 2, 820), "≠", 110, DRED, alpha=kk)
            rr = 70 + 26 * math.sin(3.2 * t)
            for x in (290, 790): d.ellipse([x - rr - 40, 820 - rr - 40, x + rr + 40, 820 + rr + 40], outline=A(DRED, kk), width=6)
    if k3 > 0:
        card(d, (40, 300, 1040, 840), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 380, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 540), "Âm cao, âm trầm:", 62, INK, alpha=k3)
        text(d, (W / 2, 640), "cùng tốc độ không?", 62, INK, alpha=k3)
        for j, (lam, col) in enumerate(((50, BLUE), (130, PURPLE))):     # hai song chay: buoc song ngan / dai
            y = 1050 + j * 220
            pts = [(x, y + 50 * math.sin(2 * math.pi * (x - t * 200) / lam * 0.5)) for x in range(120, 961, 6)]
            d.line(pts, fill=A(col, k3), width=6)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    yb = 560; x0, x1 = 160, 920; xm = (x0 + x1) / 2
    d.line([(100, yb), (980, yb)], fill=A(LIGHT, k), width=4)
    for x in (x0, x1):
        d.line([(x, yb - 110), (x, yb)], fill=A(NAVY, k), width=6)
        d.rounded_rectangle([x - 22, yb - 170, x + 22, yb - 106], radius=22, fill=A(NAVY, k))
    hands(d, xm, yb - 140, 1.0 if (t % 1.2) < 0.3 else 0.0, k)
    r = 40 + (t * 220) % 340
    waves(d, xm, yb - 140, r, both=True)
    arrow(d, (xm, 606), (x0 + 4, 606), A(NAVY, k), w=4, head=16); arrow(d, (xm, 606), (x1 - 4, 606), A(NAVY, k), w=4, head=16)
    text(d, (W / 2, 662), "6,0 m", 56, INK, alpha=k)
    text(d, (W / 2, 820), "Vỗ tay ở chính giữa", 64, INK, alpha=k)
    text(d, (W / 2, 910), "hai micro.", 64, INK, alpha=k)
    text(d, (W / 2, 1040), "Gai 2 trễ bao nhiêu?", 66, DORANGE, alpha=k)
    seg_bar(d, 1250, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = (sc[x] for x in ("hook", "do", "rut", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + s, "tap") for s, g in TR]
    out += [(do["t0"] + s + g * ROWS[i][1] / TAU_MAX, "tick") for i, (s, g) in enumerate(TR)]
    out += [(do["t0"] + do["M"][2], "ding"), (r["t0"] + r["M"][1], "tap"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return sorted(out)

# ---------------- kiem so va dong bo ----------------
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-dotocdoam-03.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    bad = []
    for dd, dt, v in ROWS:
        if abs(dd / (dt / 1000) - v) > 0.05: bad.append(("v", dd, dt, v))
        if abs(dd / V0 * 1000 - dt) > 0.06: bad.append(("dt xa mo hinh", dd, dt))
    if abs(ROWS[1][1] / ROWS[0][1] - 2) > 0.05: bad.append("dap an gap doi")
    return bad

def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, d2, tau, rows, show_dt = do_state(t)
        if tau is not None and abs(d2 - ROWS[k][0]) > 1e-9: bad.append((round(t, 2), "micro chua toi cho khi vo tay"))
        if show_dt != (rows == k + 1): bad.append((round(t, 2), "Dt <-> hang", k, rows))
        if tau is not None:
            r_mic = PXM * ROWS[k][0] + (MX0 - HX); wr = PXM * ROWS[k][0] * tau / ROWS[k][1] + (MX0 - HX)
            if (wr >= r_mic - 1e-6) != (tau >= ROWS[k][1] - 1e-6): bad.append((round(t, 2), "mat song"))
        if rows > k + 1: bad.append((round(t, 2), "hang som"))
        t += 0.05
    if sc["M"][2] < TR[-1][0] + TR[-1][1]: bad.append("dap an truoc lan do cuoi")
    return bad

CLIP = dict(id="tn-l11-dotocdoam-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo tốc độ âm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai micro, một tiếng vỗ tay", draw=s_hook, tail=0.3, caps=[
   ("Vỗ tay sát micro 1.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Máy ghi vẽ hai gai âm.", 4.4),
   ("Dời micro 2 xa dần.", 4.6),
   ("Đáp án: trễ gấp đôi.", 2.8)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Đổi Δt ra giây rồi chia.", 3.6),
   ("Ba lần, cùng một tốc độ.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Mỗi máy một đồng hồ riêng.", 3.4),
   ("Lệch vài ms là hỏng.", 3.4),
   ("Còn một chỗ chưa rõ.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.0)]),
])

if __name__ != "__main__":
    _b = _kiem_so(); assert not _b, _b
