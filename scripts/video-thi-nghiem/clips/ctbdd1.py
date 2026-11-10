# Clip: tn-l10-ctbdd-01 - Xe lan tha tu nghi tren mang nghieng, cong quang do v tai 4 vi tri (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-ctbdd-01.json:
#   tham_so: a = 0,5 m/s2 (mac dinh, mien 0,2-1,0), d = 2,00 cm (bai goi la b), dong ho chia 0,001 s.
#   so_lieu_mau (cot doc): s = 10/20/40/60 cm ; t doc 0,635/0,892/1,262/1,551 s ; tau doc 0,064/0,045/0,032/0,026 s ;
#                v = d/tau = 0,3125/0,4444/0,625/0,7692 m/s (hien 2 chu so nhu bai: 0,31/0,44/0,63/0,77).
#   v/t hien 0,49/0,49/0,50/0,50: chia lai tu so TREN MAN (0,44/0,892 = 0,493) -> 0,49, khop bang trong bai (kho 0,4983).
#   So suy ra tu so tren man: 0,63/0,44 = 1,43 (~1,4) ; bay s/t = 0,40/1,262 = 0,317 (~0,32, ~ nua 0,63).
#   Cau chot dung a = 0,6 m/s2 (trong mien tham_so) va t = 1,5 s (s = 0,675 m < mang 1 m) -> v = 0,9 m/s, chua tung hien
#   (khong trung vach truc: t 0,4..1,6 ; v 0,2..0,8).
# Truc chinh: DO THI v-t (khac dotocdo3: can canh tam chan che tia). Mang nghieng ~3 do (a = 0,5 m/s2 ~ g.sin 3 do).
# Mau: t xanh duong, v cam, tau tim, a + duong thang xanh ngoc; xanh la chi cho cau ket luan; do = bay.
# Canh: Du doan (cong 2 tu 20 ra 40 cm, K10: chi cau hoi + hinh) -> Tien hanh (4 lan tha, moi lan them 1 diem v-t,
#       chip nhac cau hoi) -> Dap an (0,44 -> 0,63) -> Rut ra (t gap doi -> v gap doi, v/t khong doi, chua noi duoc)
#       -> Bay (v = s/t) -> Chot + cau hoi.
from engine import *

ACC = 0.5
ROWS = [(10, 0.635, 0.064, 0.3125, "0,31"), (20, 0.892, 0.045, 0.4444, "0,44"),
        (40, 1.262, 0.032, 0.6250, "0,63"), (60, 1.551, 0.026, 0.7692, "0,77")]   # s cm, t, tau, v, v hien
VT = ("0,49", "0,49", "0,50", "0,50")                                                # v/t tu so tren man
C_T, C_V, C_TAU, C_A = BLUE, ORANGE, PURPLE, TEAL
CART = (100, 116, 139); CART_D = (51, 65, 85); FLAG = (17, 17, 17); RAIL = (203, 207, 218); RAIL_D = (148, 153, 168); POST = (148, 163, 184)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

# ---------------- mang nghieng (~3 do) ----------------
R0, R1 = (90, 590), (1010, 638)
RL = math.hypot(R1[0] - R0[0], R1[1] - R0[1])
RU = ((R1[0] - R0[0]) / RL, (R1[1] - R0[1]) / RL); RN = (RU[1], -RU[0])
def RP(s, h): return (R0[0] + RU[0] * s + RN[0] * h, R0[1] + RU[1] * s + RN[1] * h)
S0, PXC = 190, 8.4            # px doc mang cua cho tha (s = 0); px / cm (mang 1 m ~ 840 px)
def SP(cm): return S0 + cm * PXC
S_STOP = 84                   # cm: chan cuoi mang
BEAM_H = 92                   # do cao tia sang tren mat mang

def gate(d, cm, lab=None, ghost=False, alpha=1.0, blocked=False, flash=0.0):
    bp = RP(SP(cm), BEAM_H)
    yb = RP(SP(cm), 0)[1]                                                  # chan cot dung tren mang (phia sau xe)
    if ghost:
        for yy in range(int(bp[1] + 12), int(yb), 22):
            d.line([(bp[0], yy), (bp[0], min(yy + 12, yb))], fill=A(RAIL_D, alpha), width=6)
        d.rectangle([bp[0] - 22, bp[1] - 28, bp[0] + 22, bp[1] + 12], outline=A(RAIL_D, alpha), width=4)
    else:
        d.rectangle([bp[0] - 6, bp[1] + 12, bp[0] + 6, yb], fill=A(POST, alpha))
        d.rectangle([bp[0] - 22, bp[1] - 28, bp[0] + 22, bp[1] + 12], fill=A(POST, alpha))
        if flash > 0: d.ellipse([bp[0] - 40, bp[1] - 48, bp[0] + 40, bp[1] + 32], outline=A(YELLOW, flash), width=8)
        if not blocked: dot(d, bp[0], bp[1] - 8, 8, A(RED, alpha))
    if lab:                                                                # nhan ben trai (cong 1) / ben phai (cong 2) cot
        left = lab.endswith("1")
        text(d, (bp[0] + 12 if left else bp[0] - 12, 440), lab, 40, INK, anchor="rm" if left else "lm", alpha=alpha)
    return bp

def rig(d, cm_xe, gates, ruler=True, blocked2=False, flash2=0.0):
    """cm_xe: vi tri mep truoc tam chan (cm tu cho tha). gates: [(cm, nhan, ghost)]."""
    # nem ke dau tren + mang
    d.polygon([RP(-40, -24), RP(70, -24), (RP(70, -24)[0], 700), (RP(-40, -24)[0], 700)], fill=(226, 220, 206))
    d.line([(60, 700), (1020, 700)], fill=RAIL_D, width=4)
    d.polygon([RP(0, 0), RP(RL, 0), RP(RL, -24), RP(0, -24)], fill=RAIL, outline=RAIL_D)
    st = min(SP(S_STOP) + 27, RL - 18)                                                    # chan cuoi mang
    d.polygon([RP(st, 0), RP(st + 16, 0), RP(st + 16, 46), RP(st, 46)], fill=CART_D)
    if ruler:                                                              # thuoc tren mat ben mang
        for cm in range(0, 81, 5):
            L = 16 if cm % 10 == 0 else 9
            d.line([RP(SP(cm), -2), RP(SP(cm), -2 - L)], fill=NAVY, width=3 if L == 16 else 2)
        for cm in range(0, 71, 10):
            p = RP(SP(cm), -50); text(d, p, str(cm), 36, INK, bold=False)
        p = RP(SP(80), -50); text(d, p, "cm", 36, INK, bold=False)
    for i, (cm, lab, gh) in enumerate(gates):
        gate(d, cm, lab, gh, blocked=blocked2 and i == 1, flash=flash2 if i == 1 else 0.0)
    p = SP(cm_xe)                                                          # xe: mep truoc tam chan o p
    d.polygon([RP(p - 125, 14), RP(p + 25, 14), RP(p + 25, 62), RP(p - 125, 62)], fill=CART, outline=CART_D)
    for sw in (p - 95, p - 5):
        c = RP(sw, 10); d.ellipse([c[0] - 12, c[1] - 12, c[0] + 12, c[1] + 12], fill=CART_D)
    b = 2.0 * PXC                                                          # tam chan 2,00 cm dung ti le
    d.polygon([RP(p - b, 62), RP(p, 62), RP(p, 120), RP(p - b, 120)], fill=FLAG, outline=WHITE, width=3)
    return RP(p - b / 2, 120)

# ---------------- do thi v-t (truc co dinh ca clip) ----------------
GX0, GYB = 180, 1490
def GXt(t): return GX0 + t / 1.6 * 740
def GYv(v): return GYB - v / 0.8 * 480

def graph(d, n, alpha=1.0, ring=(), labs=None, line_k=0.0, card_box=(40, 880, 1040, 1590)):
    card(d, card_box, fill=WHITE, outline=LIGHT, w=3)
    for v in (0.2, 0.4, 0.6, 0.8): d.line([(GX0, GYv(v)), (GXt(1.6), GYv(v))], fill=(240, 236, 228), width=2)
    for t in (0.4, 0.8, 1.2, 1.6): d.line([(GXt(t), GYB), (GXt(t), GYv(0.8))], fill=(240, 236, 228), width=2)
    arrow(d, (GX0, GYB), (GXt(1.6) + 50, GYB), NAVY, w=5, head=18)
    arrow(d, (GX0, GYB), (GX0, GYv(0.8) - 50), NAVY, w=5, head=18)
    for t in (0.4, 0.8, 1.2, 1.6):
        d.line([(GXt(t), GYB), (GXt(t), GYB + 12)], fill=NAVY, width=3)
        text(d, (GXt(t), GYB + 42), vn(t, 1), 36, C_T, bold=False)
    for v in (0.2, 0.4, 0.6, 0.8):
        d.line([(GX0 - 12, GYv(v)), (GX0, GYv(v))], fill=NAVY, width=3)
        text(d, (GX0 - 20, GYv(v)), vn(v, 1), 36, C_V, bold=False, anchor="rm")
    text(d, (GX0 - 20, GYB + 30), "0", 36, INK, bold=False, anchor="rm")
    text(d, (GXt(1.6) + 58, GYB - 40), "t (s)", 40, C_T, anchor="rm")
    text(d, (GX0 + 22, GYv(0.8) - 46), "v (m/s)", 40, C_V, anchor="lm")
    if line_k > 0:                                                        # duong thang qua goc, do doc a = 0,50
        te = 1.6 * line_k
        d.line([(GXt(0), GYv(0)), (GXt(te), GYv(0.5 * te))], fill=C_A, width=7)
    for i in range(n):
        s, t, tau, v, vs = ROWS[i]
        x, y = GXt(t), GYv(v)
        if i in ring: d.ellipse([x - 30, y - 30, x + 30, y + 30], outline=NAVY, width=5)
        dot(d, x, y, 15, C_V, WHITE)
        if labs and i in labs: text(d, (x + 40, y + 40), labs[i], 38, INK, anchor="lm", alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 740), fill=WHITE, outline=LIGHT, w=3)
    rig(d, 0, [(0, "cổng 1", False), (20, "cổng 2", False), (40, None, True)])
    a0 = RP(SP(20) + 30, BEAM_H + 150); a1 = RP(SP(40) - 30, BEAM_H + 150)
    arrow(d, (a0[0], 385), (a1[0], 385), INK, w=5, head=18)
    text(d, (RP(SP(40), 0)[0], 440), "?", 44, INK)
    tp = RP(SP(0) - 2.0 * PXC, 95)                                          # nhan sat trai tam chan
    text(d, (tp[0] - 14, tp[1]), "tấm chắn", 40, INK, anchor="rm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 790 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 770), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 180, "Thả xe từ nghỉ, máng cố định.", 50, INK, maxw=900, alpha=a)
    ctext(d, y0 + 260, "Dời cổng 2 từ 20 cm ra 40 cm.", 50, INK, maxw=900, alpha=a)
    ctext(d, y0 + 380, "v tại cổng 2 thay đổi thế nào?", 52, INK, maxw=900, alpha=a)
    ctext(d, y0 + 510, "v: vận tốc xe khi qua cổng 2", 40, INK, bold=False, maxw=900, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 670, 940, y0 + 684], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 670, 140 + 800 * (1 - p), y0 + 684], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (thoi gian that, 4 lan tha) ----------------
RUN0, HOLD = 0.5, 1.1
SLOWK, SLOWD = 0.2, 0.5
def schedule():
    out = []; s = RUN0
    for r in ROWS: out.append(s); s += r[1] + HOLD
    return out
SCHED = schedule()

def run_state(t):
    """-> (lan j, so dong ho t (s), vi tri mep truoc tam chan (cm), da qua cong (tau hien), so diem tren do thi)."""
    j = 0
    for i, s in enumerate(SCHED):
        if t >= s: j = i
    s_cm, td, tau, v, vs = ROWS[j]
    c0 = max(0.0, t - SCHED[j])
    # tam chan qua cong 2: chieu cham 5 lan trong 0,5 s (xe ngay sau cong) roi chay tiep
    c = c0 if c0 < td else (td + (c0 - td) * SLOWK if c0 < td + SLOWD else td + SLOWD * SLOWK + (c0 - td - SLOWD))
    clock = min(round(c * 1000) / 1000, td)
    ae = 2 * (s_cm / 100) / (td * td)                     # xe toi cong 2 dung luc dong ho = t doc
    x = min(0.5 * ae * c * c * 100, S_STOP)
    passed = c >= td and x >= s_cm + 2.0                  # tam chan (b = 2,00 cm) da qua het tia cong 2 -> tau, v hien
    blocked = c >= td and not passed                      # tia cong 2 dang bi che
    flash = (1.0 - clamp((c0 - td - SLOWD) / 0.3)) if c0 >= td else 0.0
    npts = j + (1 if passed and c0 >= td + SLOWD else 0)
    return j, clock, x, passed, npts, blocked, flash

def s_do(img, d, t, sc):
    j, clock, x, passed, npts, blocked, flash = run_state(t)
    card(d, (40, 265, 1040, 740), fill=WHITE, outline=LIGHT, w=3)
    rig(d, x, [(0, "cổng 1", False), (ROWS[j][0], "cổng 2", False)], blocked2=blocked, flash2=flash)
    # chip nhac cau hoi du doan
    chip = "Nhớ: v ở 20 cm và 40 cm?"
    cw = tw(d, chip, F(36)) + 44
    card(d, (W / 2 - cw / 2, 282, W / 2 + cw / 2, 340), fill=(245, 243, 255), outline=PURPLE, r=29, w=3)
    text(d, (W / 2, 311), chip, 36, PURPLE)
    # so doc
    card(d, (40, 755, 1040, 865), fill=NAVY, r=22)
    cols = ((200, "t từ lúc thả", vn(clock, 3) + " s", C_T), (500, "τ chắn sáng", (vn(ROWS[j][2], 3) + " s") if passed else "–", C_TAU),
            (820, "v = b/τ, b = 2,00 cm", (ROWS[j][4] + " m/s") if passed else "–", C_V))
    for cx, h, val, col in cols:
        text(d, (cx, 787), h, 36, (220, 225, 240), bold=False)
        text(d, (cx, 836), val, 46, mix(col, WHITE, 0.45))
    graph(d, npts)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · tăng, chưa tới gấp đôi"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lb, 40, WHITE, alpha=ka)
    card(d, (40, 360, 1040, 850), fill=WHITE, outline=LIGHT, w=3)
    for k_, (i, yy) in enumerate(((1, 450), (2, 560))):
        s, td, tau, v, vs = ROWS[i]
        kk = appear(t, 0.5 + 0.5 * k_, 0.4)
        text(d, (90, yy), f"Cổng 2 ở {s} cm:", 46, INK, anchor="lm", alpha=kk)
        text(d, (990, yy), f"v = {vs} m/s", 50, C_V, anchor="rm", alpha=kk)
    k2 = appear(t, M[0] + 1.4, 0.5)
    card(d, (80, 625, 1000, 815), fill=A((236, 253, 243), k2), r=24)
    text(d, (W / 2, 720), "0,63 / 0,44 ≈ 1,4", 54, GREEN, alpha=k2)
    kr = appear(t, 0.5, 0.4)
    graph(d, 4, ring=(1, 2) if kr > 0.5 else (), labs={1: "20 cm", 2: "40 cm"} if kr > 0.5 else None)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    if t < M[2] - 0.1:
        card(d, (40, 265, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
        text(d, (90, 330), "t: 0,635 → 1,262 s", 46, C_T, anchor="lm")
        text(d, (90, 410), "v: 0,31 → 0,63 m/s", 46, C_V, anchor="lm")
        text(d, (W / 2, 500), "cùng ≈ gấp đôi", 44, GREEN)
        kb = appear(t, M[1] - 0.1, 0.45)
        if kb > 0:
            card(d, (40, 580, 1040, 860), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
            VX = (500, 625, 750, 875)
            text(d, (80, 618), "cổng 2 ở (cm)", 38, INK, bold=False, anchor="lm", alpha=kb)
            text(d, (80, 676), "v/t (m/s²)", 40, INK, anchor="lm", alpha=kb)
            for xx, (r, q) in zip(VX, zip(ROWS, VT)):
                text(d, (xx, 618), str(r[0]), 38, INK, bold=False, alpha=kb)
                text(d, (xx, 676), q, 42, C_A, alpha=kb)
            text(d, (W / 2, 756), "v = a·t,  a ≈ 0,50 m/s²", 48, C_A, alpha=kb)
            text(d, (W / 2, 822), "a: gia tốc = độ dốc đồ thị", 38, INK, bold=False, alpha=kb)
    else:
        k2 = appear(t, M[2] - 0.1, 0.45)
        card(d, (40, 265, 1040, 860), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, 340), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[2] + 0.3, 0.4)
        card(d, (80, 400, 1000, 820), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, 550), "Xa hơn 60 cm chưa đo:", 50, RED, alpha=kk)
        text(d, (W / 2, 670), "a còn không đổi?", 50, RED, alpha=kk)
    ring = (0, 2) if t < M[1] - 0.1 else ()
    lk = ease((t - M[1]) / 1.0)
    graph(d, 4, ring=ring, line_k=lk)
    if lk > 0.9: text(d, (GXt(1.25) - 20, GYv(0.5 * 1.25) - 70), "v = a·t", 40, C_A, anchor="rm", alpha=appear(t, M[1] + 0.9, 0.4))

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    text(d, (W / 2, y0 + 175), "Cổng 2 ở 40 cm, t = 1,262 s", 44, INK, alpha=a1)
    # hai thanh dung ti le: s/t = 0,32 ; cong quang 0,63 (600 px ung 0,63 m/s)
    L63 = 600; L32 = L63 * 0.317 / 0.625
    bx = 100; yA, yB = y0 + 330, y0 + 560
    text(d, (bx, yA - 55), "s/t = 0,40 m / 1,262 s", 44, RED, anchor="lm", alpha=a1)
    d.rectangle([bx, yA, bx + L32, yA + 60], fill=A((252, 165, 165), a1))
    text(d, (bx + L32 + 24, yA + 30), "0,32 m/s", 44, RED, anchor="lm", alpha=a1)
    ks = clamp((t - 1.3) / 0.4)
    if ks > 0: d.line([(bx - 10, yA + 30), (bx - 10 + (L32 + 8) * ks, yA + 30)], fill=A(RED, 0.9 * a1), width=6)
    kb = appear(t, 0.6, 0.4)
    text(d, (bx, yB - 55), "cổng quang: v = b/τ", 44, C_V, anchor="lm", alpha=kb)
    d.rectangle([bx, yB, bx + L63, yB + 60], fill=A(C_V, kb))
    text(d, (bx + L63 + 24, yB + 30), "0,63 m/s", 44, C_V, anchor="lm", alpha=kb)
    kk = appear(t, 1.8, 0.5)
    card(d, (90, y0 + 760, 990, y0 + 1180), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 880), "s/t: vận tốc trung bình cả đoạn", 46, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 1040), "chỉ khoảng một nửa", 50, GREEN, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):                       # goi y tre ~3,7 s sau cau hoi
        kh = appear(t, M[0] + 3.7, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "t = 0 thì v = 0", 42, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "a không đổi, thả từ nghỉ: v tỉ lệ với t",
             "Máng dốc hơn: gia tốc a = 0,6 m/s². Thả từ nghỉ, sau 1,5 s thì v bằng bao nhiêu?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for s, row in zip(SCHED, ROWS): cs.append((do["t0"] + s + row[1], "tap"))      # tam chan toi cong 2
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-ctbdd-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động thẳng biến đổi đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe lăn trên máng nghiêng", draw=s_hook, tail=0.8, caps=[
   ("Cổng quang đo v của xe.", 3.0),
   ("Dừng video, chọn câu trả lời.", 7.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Cổng 2 ở 10, 20, 40, 60 cm.", 4.0),
   ("Mỗi lần thả: thêm một điểm.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So điểm 20 cm với 40 cm.", 4.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("So 10 cm với 40 cm.", 3.4),
   ("Đồ thị thẳng, qua gốc.", 3.4),
   ("Còn điều chưa biết.", 3.0)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.5, caps=[
   ("Lấy s chia t được không?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Dừng video, tự trả lời.", 6.2)]),
])
