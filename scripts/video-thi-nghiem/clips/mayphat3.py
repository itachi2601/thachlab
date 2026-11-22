# Clip: tn-l12-mayphatdien-03 - Tu quan may bien ap: do dien ap thu cap theo so vong day
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-mayphatdien-03.json (so_lieu_mau, tham_so, mo_hinh, hien_tuong_hay_sai #1).
# Ban 2 (21/11/2026, viec 4 lo 20): dung lai theo cong moi (--do-chu 0 LOI, chu ve >= 56 px, <= 50 s, K10).
# Du doan (khung ben canh, khong ve nut): N1 = 200, U1 = 12 V, N2 = 400 -> von ke chi? A 6 / B 12 / C 24 (dung, do 23,5) / D 48.
# Bay: quan niem sai "tang ap thi tang cong suat" (hien_tuong_hay_sai #1): U2 gap doi thi I2 con mot nua, P = U.I giu nguyen
#   (may li tuong, mo_hinh H = U2.I2/(U1.I1)); chi dung ti so, khong bia so ampe (kho khong do dong).
# Chot: thu cap 100 vong (ha ap, hang dau so_lieu_mau), co tai: I2 so voi I1? -> ~ 2.I1 (suy nguoc chieu tu Bay, chua chieu).
from engine import *

U1, N1 = 12, 200                                                  # tham_so
ROWS = [(100, 5.9), (200, 11.6), (400, 23.5), (600, 35.1)]        # so_lieu_mau: N2, U2 do (V)
def fmt(v): return f"{v:.1f}".replace(".", ",")

COPPER, COPPER_D = (196, 120, 52), (120, 66, 24)
CORE, CORE_L = (148, 158, 178), (190, 198, 214)
DARK_OR = (181, 71, 8)                                            # cam dam tren nen sang

# ---------------- loi sat kin + cuon day ----------------
def core(d, x0, y0, x1, y1, w, a=1.0):
    d.rectangle([x0, y0, x1, y1], fill=A(CORE, a), outline=A(NAVY, a), width=5)
    d.rectangle([x0 + w, y0 + w, x1 - w, y1 - w], fill=A(BG, a), outline=A(NAVY, a), width=5)
    for k in (w * 0.25, w * 0.5, w * 0.75):                       # cac la thep ghep
        d.rectangle([x0 + k, y0 + k, x1 - k, y1 - k], outline=A(CORE_L, a), width=2)

def coil(d, cx, yc, n, cw, pitch, a=1.0):
    """n vong ve (moi vong ve = 25 vong that)."""
    hh = n * pitch; top = yc - hh / 2
    for i in range(n):
        y = top + i * pitch + pitch / 2
        d.rounded_rectangle([cx - cw / 2, y - pitch * 0.38, cx + cw / 2, y + pitch * 0.38], radius=int(pitch * 0.38),
                            fill=A(COPPER, a), outline=A(COPPER_D, a), width=2)
    return top + pitch / 2, top + hh - pitch / 2

def flux(d, t, x0, y0, x1, y1, col=BLUE, size=18, a=0.9):
    """Chevron chay quanh duong giua loi, doi chieu theo nhip xoay chieu."""
    s = math.sin(2 * math.pi * 0.45 * t)
    if abs(s) < 0.15: return
    dirn = 1 if s > 0 else -1; al = a * clamp((abs(s) - 0.15) / 0.5)
    per = 2 * ((x1 - x0) + (y1 - y0)); step = per / 14
    off = (t * 70 * dirn) % step
    for k in range(14):
        p = (k * step + off) % per
        if p < x1 - x0: x, y, ang = x0 + p, y0, 0
        elif p < (x1 - x0) + (y1 - y0): x, y, ang = x1, y0 + p - (x1 - x0), 90
        elif p < 2 * (x1 - x0) + (y1 - y0): x, y, ang = x1 - (p - (x1 - x0) - (y1 - y0)), y1, 180
        else: x, y, ang = x0, y1 - (p - 2 * (x1 - x0) - (y1 - y0)), 270
        r = math.radians(ang + (0 if dirn > 0 else 180))
        for sg in (1, -1):
            b = r + math.pi - sg * math.radians(35)
            d.line([(x + size * 0.5 * math.cos(r), y + size * 0.5 * math.sin(r)),
                    (x + size * 0.5 * math.cos(r) + size * math.cos(b), y + size * 0.5 * math.sin(r) + size * math.sin(b))],
                   fill=A(col, al), width=5)

def n_draw(N): return int(round(N / 25))

def rig(d, t, n2, reading, n2_lbl, lbl_col=BLUE, loi_lbl=False):
    """Loi kin, so cap 200 vong noi nguon 12 V ~, thu cap n2 vong ve noi von ke. Chu >= 56 px (ra mp4 >= 49 px)."""
    cx1, cx2, yc = 340, 740, 630
    if loi_lbl: text(d, (540, 330), "lõi thép kín", 56, NAVY)
    core(d, 300, 400, 780, 860, 80)
    flux(d, t, 340, 440, 740, 820)
    a1, b1 = coil(d, cx1, yc, n_draw(N1), 140, 14)
    # nguon xoay chieu (trai): x 30..240
    card(d, (30, 540, 240, 730), fill=WHITE, outline=NAVY, r=22, w=5)
    pts = [(135 - 60 + j * 120 / 40, 600 - 26 * math.sin(2 * math.pi * j / 40)) for j in range(41)]
    d.line(pts, fill=ORANGE, width=6, joint="curve")
    text(d, (135, 685), f"{U1} V", 56, BLUE)
    text(d, (135, 488), "nguồn ~", 56, INK)
    d.line([(270, a1), (255, a1), (255, 580), (240, 580)], fill=NAVY, width=5)
    d.line([(270, b1), (255, b1), (255, 700), (240, 700)], fill=NAVY, width=5)
    if n2 > 0:
        a2, b2 = coil(d, cx2, yc, n2, 140, 14)
        d.line([(810, a2), (822, a2), (822, 580), (835, 580)], fill=NAVY, width=5)
        d.line([(810, b2), (822, b2), (822, 700), (835, 700)], fill=NAVY, width=5)
    # von ke (phai): x 835..1045 -> mp4 x <= 65 + 0,88.1045 = 985
    card(d, (835, 540, 1045, 730), fill=(255, 236, 160), outline=NAVY, r=22, w=5)
    d.rounded_rectangle([852, 562, 1028, 652], radius=12, fill=NAVY)
    text(d, (940, 607), reading, 58, (134, 239, 172))
    text(d, (940, 692), "V~", 56, INK)
    text(d, (940, 488), "vôn kế", 56, INK)
    text(d, (cx1, 925), f"N₁ = {N1} vòng", 56, INK)
    text(d, (cx2 + 20, 925), n2_lbl, 56, lbl_col)

# ---------------- canh 1: mo bai + du doan ----------------
def dots(d, t, t1, t2, y, a, col=PURPLE):
    """Dem nguoc 5 cham, moi cham tat dan (thanh dem >= 70 px, giu hinh khong dung yen)."""
    n_off = 0 if t < t1 else min(5, int((t - t1) / ((t2 - t1) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y, 40, A(LIGHT, a) if j >= 5 - n_off else A(col, a))

def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, n_draw(400), "?", "N₂ = 400 vòng")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Thứ cấp 400 vòng:", 62, INK, alpha=a)      # K10: khong ve nut A-D, khong HOA goi y
    text(d, (W / 2, y0 + 280), "vôn kế chỉ bao nhiêu?", 62, INK, alpha=a)
    dots(d, t, M[1] + 0.3, sc["T"] - 0.1, y0 + 440, a)

# ---------------- canh 2: quan them vong, do U2, ghi bang ----------------
def wind_at(i, sc):
    """Quan hang i trong 0,85 s cuoi cua phu de truoc; so chi hien dung luc phu de hang i len."""
    m = sc["M"][i]
    return max(0.0, m - 0.9), max(0.35, m - 0.05)

def do_state(t, sc):
    n2, rd, lbl = 0, "---", "N₂ = 0 vòng"
    for i, (N, u) in enumerate(ROWS):
        s, e = wind_at(i, sc)
        if t < s: break
        prev = ROWS[i - 1][0] if i else 0
        n2 = int(round(lerp(n_draw(prev), n_draw(N), clamp((t - s) / (e - s)))))
        if t >= e: rd, lbl = fmt(u), f"N₂ = {N} vòng"
        else: rd = "···"
    return n2, rd, lbl

def s_do(img, d, t, sc):
    n2, rd, lbl = do_state(t, sc)
    rig(d, t, n2, rd, lbl, loi_lbl=True)
    card(d, (50, 1000, 1030, 1600), fill=WHITE, outline=NAVY, w=4)
    xs = [300, 760]
    text(d, (xs[0], 1060), "N₂ (vòng)", 56, INK); text(d, (xs[1], 1060), "U₂ đo (V)", 56, INK)
    d.line([(80, 1102), (1000, 1102)], fill=LIGHT, width=4)
    last = max([i for i in range(4) if t >= wind_at(i, sc)[1]], default=-1)
    for i, (N, u) in enumerate(ROWS):
        e = wind_at(i, sc)[1]; a = appear(t, e, 0.3); y = 1155 + i * 92
        if a <= 0: continue
        if i == last: d.rounded_rectangle([70, y - 40, 1010, y + 40], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(N), 58, BLUE, alpha=a)
        text(d, (xs[1], y), fmt(u), 58, RED, alpha=a)
    text(d, (W / 2, 1555), "Số liệu minh hoạ", 56, MUTED)

# ---------------- canh 3: dap an + vi sao + hao phi ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0] - 0.1, 0.4)
    if ka > 0:
        pw = tw(d, "ĐÁP ÁN: 24 V", F(60)) + 70
        card(d, (W / 2 - pw / 2, 255, W / 2 + pw / 2, 340), fill=A(NAVY, ka), r=40)
        text(d, (W / 2, 297), "ĐÁP ÁN: 24 V", 60, WHITE, alpha=ka)
    # nhip 1: hai hang so sanh, cung nhan x2; cuon day ve mini ben trai (8 vong -> 16 vong)
    card(d, (50, 380, 1030, 960), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    for y, lab, v0, v1 in ((540, "N₂", "200", "400"), (820, "U₂", "11,6 V", "23,5 V")):
        text(d, (130, y), lab, 66, INK, alpha=ka)
        text(d, (370, y), v0, 62, BLUE if lab == "N₂" else RED, alpha=ka)
        kk = ease((t - M[0] - 0.3) / 0.6)
        if kk > 0:
            arrow(d, (500, y), (500 + 150 * kk, y), A(ORANGE, ka), w=8, head=26)
        text(d, (580, y - 70), "×2", 58, ORANGE, alpha=appear(t, M[0] + 0.6, 0.4))
        text(d, (830, y), v1, 62, BLUE if lab == "N₂" else RED, alpha=appear(t, M[0] + 0.6, 0.4))
    d.line([(90, 680), (990, 680)], fill=A(LIGHT, ka), width=3)
    # nhip 2: thanh tinh / do: do hoi thap
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 <= 0: return
    card(d, (50, 1010, 1030, 1560), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=5)
    for y, lab, u, col in ((1170, "tính", 24.0, BLUE), (1380, "đo", 23.5, RED)):
        text(d, (150, y), lab, 58, INK, alpha=k2)
        L = 560 * u / 24.0 * ease((t - M[1]) / 0.8)
        if L > 2: d.rounded_rectangle([240, y - 40, 240 + L, y + 40], radius=14, fill=A(col, k2))
        text(d, (830, y), ("24 V" if u == 24.0 else "23,5 V"), 58, col, anchor="lm", alpha=appear(t, M[1] + 0.7, 0.3))

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (50, 280, 1030, 1560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 400), "Chưa nói được gì?", 64, PURPLE, alpha=k)
    # ampe ke chua co: vong tron net dut + dau ?
    cx, cy, r = W / 2, 860, 230
    if kb <= 0:
        text(d, (W / 2, 860), "?", 260, NAVY, alpha=k)
        return
    for j in range(24):
        a0 = j * 15
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 9, fill=A(NAVY, kb), width=10)
    text(d, (cx, cy - 30), "A", 140, NAVY, alpha=kb)
    text(d, (cx, cy + 120), "?", 110, RED, alpha=kb)
    text(d, (W / 2, 1300), "Chưa đo dòng điện I", 64, INK, alpha=kb)

# ---------------- canh 5: bay tang ap tang cong suat ----------------
BX = 240                                            # goc thanh
def bar(d, y, L, col, lbl, k, lab_col=None):
    if k <= 0: return
    LL = L * ease(k)
    d.rounded_rectangle([BX, y - 30, BX + max(LL, 4), y + 30], radius=12, fill=A(col, k))
    text(d, (BX + LL + 22, y), lbl, 62, lab_col or col, anchor="lm", alpha=k)

def s_bay(img, d, t, sc):
    M = sc["M"]; b1, b2, b3 = (m - 0.1 for m in M)
    k1 = appear(t, b1, 0.4); k2 = appear(t, b2, 0.5); k3 = appear(t, b3, 0.5)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 326), fill=A(RED, k1), r=38)
    text(d, (W / 2, 288), "BẪY", 56, WHITE, alpha=k1)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1030 - pw2, 250, 1030, 326), fill=A(RED, k3), r=38)
        text(d, (1030 - pw2 / 2, 288), "SAI", 56, WHITE, alpha=k3)
    text(d, (W / 2, 395), "U₂ gấp đôi thì P gấp đôi?", 60, INK, alpha=k1)
    # chu giai mau: so cap xanh, thu cap cam
    dot(d, 150, 490, 22, A(BLUE, k1)); text(d, (185, 490), "sơ cấp", 56, BLUE, anchor="lm", alpha=k1)
    dot(d, 560, 490, 22, A(ORANGE, k1)); text(d, (595, 490), "thứ cấp", 56, DARK_OR, anchor="lm", alpha=k1)
    rows = ((650, "U", k1, (280, "U₁"), (560, "U₂ ≈ 2U₁")),
            (920, "I", k2, (480, "I₁"), (240, "I₂ ≈ I₁/2")),
            (1190, "P", k3, (400, "P₁"), (400, "P₂ ≈ P₁")))
    for y, q, k, (L1, l1), (L2, l2) in rows:
        if k <= 0: continue
        text(d, (120, y), q, 72, INK, alpha=k)
        bar(d, y - 45, L1, BLUE, l1, k)
        bar(d, y + 45, L2, ORANGE, l2, k, DARK_OR)
    if k3 > 0:
        card(d, (90, 1330, 990, 1470), fill=A((220, 252, 231), k3), r=24)
        text(d, (W / 2, 1400), "Không tự sinh năng lượng", 60, GREEN, alpha=k3)

# ---------------- canh 6: chot + thu nghi ----------------
def s_end(img, d, t, sc):
    k0 = appear(t, 0.2, 0.5); kc = k0 * (1 - appear(t, 1.9, 0.4))   # khung chot mo dan truoc khi the THU NGHI hien
    if kc > 0:
        card(d, (50, 255, 1030, 420), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), w=6)
        text(d, (W / 2, 337), "Đổi U, P gần như giữ nguyên", 60, GREEN, alpha=kc)
    # may ha ap mini: so cap 8 vong ve (200), thu cap 4 vong ve (100), bong den lam tai
    core(d, 300, 470, 720, 850, 70, a=k0)
    flux(d, t, 335, 505, 685, 815, a=0.9 * k0)
    a1, b1 = coil(d, 335, 660, n_draw(N1), 130, 18, a=k0)
    a2, b2 = coil(d, 685, 660, n_draw(100), 130, 18, a=k0)
    d.line([(750, a2), (800, a2), (800, 615), (850, 615)], fill=A(NAVY, k0), width=5)
    d.line([(750, b2), (800, b2), (800, 705), (850, 705)], fill=A(NAVY, k0), width=5)
    dot(d, 900, 660, 55, A((254, 240, 138), k0), A(NAVY, k0))      # bong den (tai)
    d.line([(880, 645), (900, 675), (920, 645)], fill=A(ORANGE, k0), width=5)
    d.line([(270, a1), (230, a1), (230, 615), (180, 615)], fill=A(NAVY, k0), width=5)
    d.line([(270, b1), (230, b1), (230, 705), (180, 705)], fill=A(NAVY, k0), width=5)
    pts = [(150 - 40 + j * 80 / 30, 660 - 22 * math.sin(2 * math.pi * j / 30)) for j in range(31)]
    d.line(pts, fill=A(ORANGE, k0), width=6)
    text(d, (335, 905), f"N₁ = {N1}", 60, INK, alpha=k0)          # du dieu kien ngay canh may (so vong ve: 8 / 4)
    text(d, (685, 905), "N₂ = 100", 60, BLUE, alpha=k0)
    k = appear(t, 2.4, 0.5)
    if k <= 0: return
    card(d, (50, 960, 1030, 1600), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 990, W / 2 + pw / 2, 1070), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 1030), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 1150), "Có tải, máy lí tưởng:", 60, INK, alpha=k)
    text(d, (W / 2, 1250), "I₂ so với I₁?", 66, DARK_OR, alpha=k)
    kh = appear(t, 4.9, 0.5)                           # goi y tre ~2,5 s, trung tinh, khong neu cong thuc
    if kh > 0:
        card(d, (110, 1340, 970, 1560), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1400), "Gợi ý:", 56, INK, alpha=kh)
        text(d, (W / 2, 1490), "So U₂ với U₁?", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, g, b, e = (sc[k] for k in ("hook", "do", "dapan", "gioi", "bay", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + wind_at(2, do)[1], "tap"), (da["t0"] + da["M"][0] - 0.1, "ding"),
            (g["t0"] + 2.4, "tap"), (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (e["t0"] + 2.4, "open")]

CLIP = dict(id="tn-l12-mayphatdien-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Máy biến áp · thachlab.id.vn", scenes=[
 dict(key="hook", title="Tự quấn máy biến áp", draw=s_hook, tail=0.3, caps=[
   ("Hai cuộn chung một lõi.", 2.9),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Quấn thêm vòng, đo U₂", draw=s_do, tail=0.3, caps=[
   ("100 vòng: 5,9 V", 2.5), ("200 vòng: 11,6 V", 2.5),
   ("400 vòng: 23,5 V", 2.5), ("600 vòng: 35,1 V", 2.5)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Mỗi vòng góp cùng điện áp.", 3.0),
   ("Hơi thấp do hao phí.", 3.0)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Chỉ có vôn kế.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Nối tải, máy lí tưởng.", 3.0),
   ("Dòng I₂ chỉ còn một nửa.", 3.0),
   ("Tích U·I giữ nguyên.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự đoán.", 7.0)]),
])
