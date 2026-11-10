# Clip: tn-l10-do-g-01 - Do g bang cong quang: tha bi 5 lan tu s = 0,500 m, xu li sai so (10/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-g-01.json:
#   so_lieu_mau: t = 0,319 / 0,322 / 0,321 / 0,323 / 0,320 s ; |t - tTB| = 0,002 / 0,001 / 0 / 0,002 / 0,001 s.
#   rut_ra: tTB = 0,321 s ; DtTB = 0,0012 s ; Dt = 0,0012 + 0,001 = 0,0022 s ; gTB = 9,70 ; Dg = 0,15 ; khoang chua 9,8.
#   ket_qua_ky_vong: khoang 9,55 - 9,85.  tham_so: dcnn_t = 0,001 s, s = 0,5 m, g_that = 9,8.
# KHONG hien delta = Ds/s + 2Dt/tTB va hai phan 0,2 % / 1,4 %: Cau 2 ngay sau hop trong bai hoi phan nao chi phoi.
# KHONG noi tu du / bi roi muon (Cau 4 cua bai).
# Bo cuc khac dog2 (do thi s-t^2) va dog3 (dem khung): gia do cao ben trai, dong ho + bang 5 lan ben phai,
#   truc so g o canh bay. Cau chot: lan 2 rieng (t = 0,322 s) cho g lon hay nho hon 9,70 -> nho hon (9,64, chua hien).
# Mau: t = INK/NAVY ; |t - tTB| = PURPLE ; do chia dong ho = TEAL ; g = GREEN ; 9,8 = RED_D ; Du doan = PURPLE.
from engine import *

S = 0.500
TS = [0.319, 0.322, 0.321, 0.323, 0.320]                 # so_lieu_mau
DEV = [0.002, 0.001, 0.0, 0.002, 0.001]
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
POST = (71, 85, 105); RED_D = (185, 28, 28); PURPLE_BG = (245, 243, 255); HL = (255, 247, 237)

def vn(x, nd):
    return f"{x:.{nd}f}".replace(".", ",")

def segs(d, x, y, parts, size, alpha=1.0, anchor="m"):
    """Chu nhieu mau mot dong. parts = [(chu, mau)] hoac [(chu, mau, True)] -> gach ngang tren (t trung binh)."""
    f = F(size); tot = sum(tw(d, p[0], f) for p in parts)
    xx = x - tot / 2 if anchor == "m" else x
    for p in parts:
        s, c = p[0], p[1]; w = tw(d, s, f)
        dtext(d, (xx, y), s, f, c, alpha, "lm")
        if len(p) > 2 and p[2]:
            yb = y - size * 0.58
            d.line([(xx + w * 0.08, yb), (xx + w * 0.92, yb)], fill=A(c, alpha), width=max(3, size // 14))
        xx += w
    return tot

# ---------------- gia do: nam cham, bi, thuoc, cong quang ----------------
SY0, SPX = 385, 1560.0                    # y day bi luc con o nam cham ; px / m
def SYp(s): return SY0 + SPX * s
BX, BR = 270, 20
def rig(d, ball_s, ball_a=1.0, hook=False):
    card(d, (40, 265, 420, 1290), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([150, SY0 - 6, 180, SYp(0.5) + 10], fill=WOOD, outline=WOOD_D, width=3)          # thuoc
    for i in range(6):
        y = SYp(i / 10)
        d.line([(150, y), (176, y)], fill=INK, width=3)
        text(d, (140, y), "0" if i == 0 else vn(i / 10, 1), 36, INK, anchor="rm")
    for i in range(1, 10, 2):
        y = SYp(i / 20); d.line([(150, y), (166, y)], fill=INK, width=2)
    text(d, (60, 300), "s (m)", 36, BLUE, anchor="lm")
    d.rectangle([225, 290, 315, SY0 - 2 * BR], fill=NAVY)                                        # nam cham dien
    yg = SYp(S)                                                                                   # cong quang
    d.line([(235, yg), (305, yg)], fill=RED, width=4)
    d.rectangle([210, yg - 20, 235, yg + 20], fill=POST); d.rectangle([305, yg - 20, 335, yg + 20], fill=POST)
    text(d, (272, yg + 62), "cổng quang", 36, INK)
    if hook:
        text(d, (400, (SY0 + yg) / 2 - 140), "s", 40, BLUE)
        arrow(d, (370, SY0 + 40), (370, yg - 8), BLUE, w=4, head=16); arrow(d, (370, yg - 40), (370, SY0 + 8), BLUE, w=4, head=16)
    if ball_s is not None and ball_a > 0.02:
        y = SYp(ball_s) - BR
        d.ellipse([BX - BR, y - BR, BX + BR, y + BR], fill=A(STEEL, ball_a), outline=A(NAVY, ball_a), width=2)
        d.ellipse([BX - 9, y - 10, BX - 2, y - 3], fill=A(STEEL_L, ball_a))

def clock(d, val, lit=True):
    card(d, (440, 265, 1040, 420), fill=WHITE, outline=LIGHT, w=3)
    text(d, (560, 342), "đồng hồ", 38, INK)
    card(d, (680, 290, 1015, 395), fill=NAVY, r=18)
    text(d, (848, 342), vn(val, 3) + " s", 56, YELLOW if lit else GRAY)

# ---------------- bang 5 lan ----------------
CX = (520, 690, 905); RY0, RDY = 560, 105
def table(d, n_t, cur=None, n_dev=0, tb_t=0.0, tb_dev=0.0, mark=None):
    card(d, (440, 440, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    text(d, (CX[0], 495), "Lần", 38, INK)
    text(d, (CX[1], 495), "t (s)", 38, INK)
    segs(d, CX[2], 495, [("|t − ", PURPLE), ("t", PURPLE, True), ("|", PURPLE)], 38)
    d.line([(460, 535), (1020, 535)], fill=LIGHT, width=3)
    for i in range(5):
        y = RY0 + 45 + i * RDY
        if cur == i: d.rounded_rectangle([455, y - 40, 1025, y + 40], radius=16, fill=HL)
        if mark and i in mark: d.rounded_rectangle([CX[1] - 90, y - 38, CX[1] + 90, y + 38], radius=16, outline=ORANGE, width=5)
        text(d, (CX[0], y), str(i + 1), 40, MUTED)
        if i < n_t: text(d, (CX[1], y), vn(TS[i], 3), 44, INK)
        if i < n_dev: text(d, (CX[2], y), vn(DEV[i], 3), 44, PURPLE)
    if tb_t > 0 or tb_dev > 0:
        y = RY0 + 45 + 5 * RDY + 10
        d.line([(460, y - 55), (1020, y - 55)], fill=A(INK, max(tb_t, tb_dev)), width=3)
        text(d, (CX[0], y), "TB", 40, INK, alpha=max(tb_t, tb_dev))
        text(d, (CX[1], y), "0,321", 46, NAVY, alpha=tb_t)
        text(d, (CX[2], y), "0,0012", 46, PURPLE, alpha=tb_dev)

def chip(d, s, y, col=PURPLE, bg=PURPLE_BG, tc=None):
    card(d, (60, y - 30, 1020, y + 30), fill=bg, outline=col, r=28, w=3)
    text(d, (W / 2, y), s, 38, tc or col)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0.0, hook=True); clock(d, 0.0, lit=False); table(d, 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 940 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 655), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 165, "Thả bi 5 lần, cùng s = 0,500 m.", 46, INK, maxw=920, alpha=a)
    ctext(d, y0 + 240, "Đồng hồ chia tới 0,001 s.", 46, INK, maxw=920, alpha=a)
    ctext(d, y0 + 390, "5 số t đo được sẽ thế nào?", 54, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 545, 940, y0 + 559], radius=7, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 545, 140 + 800 * (1 - p), y0 + 559], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (5 lan tha, chieu cham 3 lan) ----------------
SLOW, PAUSE, HOLD, RUN0 = 3.0, 0.35, 0.4, 0.4
def schedule():
    out = []; s = RUN0
    for i in range(5):
        f0 = s + PAUSE; f1 = f0 + TS[i] * SLOW
        out.append((s, f0, f1)); s = f1 + HOLD
    return out
SCHED = schedule()

def run_state(t):
    """-> (s day bi, alpha bi, so dong ho, dong ho sang?, so hang xong, luot j)."""
    j = 0
    for i, (s0, *_r) in enumerate(SCHED):
        if t >= s0: j = i
    s0, f0, f1 = SCHED[j]
    prev = TS[j - 1] if j > 0 else 0.0
    if t < f0:                                         # bi moi gan lai nam cham; dong ho giu so lan truoc
        return 0.0, appear(t, s0, 0.2) if j > 0 else 1.0, prev, j > 0, j, j
    u = clamp((t - f0) / (f1 - f0))                     # tien do roi 0..1 (s ti le t^2)
    if t < f1:
        return S * u * u, 1.0, round(TS[j] * u, 3), True, j, j
    return S, 1 - clamp((t - f1) / 0.25), TS[j], True, j + 1, j

def s_do(img, d, t, sc):
    bs, ba, cv, lit, done, j = run_state(t)
    rig(d, bs, ba); clock(d, cv, lit); table(d, done, cur=j if done <= j else None)
    chip(d, "Câu hỏi: 5 số t sẽ thế nào?", 1360)
    chip(d, "chiếu chậm 3 lần", 1460, col=NAVY, bg=NAVY, tc=YELLOW)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, None); clock(d, TS[4]); table(d, 5, mark=(0, 3) if t > 0.9 else None)
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · lệch nhau vài phần nghìn giây"
    pw = tw(d, lb, F(38)) + 56
    card(d, (W / 2 - pw / 2, 1325, W / 2 + pw / 2, 1395), fill=A(NAVY, ka), r=35)
    text(d, (W / 2, 1360), lb, 38, WHITE, alpha=ka)
    k1 = appear(t, 0.9, 0.5)
    segs(d, W / 2, 1480, [("0,319 s", ORANGE), ("  →  ", INK), ("0,323 s", ORANGE)], 46, alpha=k1)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    rig(d, None)
    tb = appear(t, 0.6, 0.4)
    nd = sum(1 for i in range(5) if t >= M[0] + 1.6 + 0.35 * i)
    tbd = appear(t, M[0] + 3.5, 0.4)
    table(d, 5, n_dev=nd, tb_t=tb, tb_dev=tbd)
    clock(d, TS[4])
    card(d, (40, 1315, 1040, 1595), fill=WHITE, outline=LIGHT, w=3)
    k1 = appear(t, M[1] - 0.1, 0.4)
    segs(d, W / 2, 1375, [("Δt = ", INK), ("0,0012", PURPLE), (" + ", INK), ("0,001", TEAL), (" = 0,0022 s", INK)], 46, alpha=k1)
    segs(d, W / 2, 1435, [("độ chia đồng hồ: ", TEAL), ("0,001 s", TEAL)], 38, alpha=k1)
    k2 = appear(t, M[1] + 1.9, 0.4)
    if k2 > 0: d.line([(90, 1475), (990, 1475)], fill=A(LIGHT, k2), width=3)
    segs(d, W / 2, 1535, [("Kết quả: ", INK), ("g = 9,70 ± 0,15 m/s²", GREEN)], 48, alpha=k2)
    kc = appear(t, M[2] - 0.1, 0.45)
    if kc > 0:
        y0 = 700 + (1 - kc) * 30
        card(d, (40, y0, 1040, y0 + 470), fill=A((254, 242, 242), kc), outline=A(NAVY, kc), w=5)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=kc)
        kk = kc * appear(t, M[2] + 0.3, 0.4)
        text(d, (W / 2, y0 + 210), "Mới thả ở một độ cao.", 46, RED_D, alpha=kk)
        text(d, (W / 2, y0 + 320), "Độ cao khác có cùng g?", 46, RED_D, alpha=kk)

# ---------------- canh 5: Bay (khac 9,8 la hong) ----------------
NX0, NPX, NY = 150, 1900.0, 1150                 # truc so g: x(9,5) ; px / (m/s^2) ; y
def NX(g): return NX0 + (g - 9.5) * NPX
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.15, 0.4)
    card(d, (40, 265, 1040, 800), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 295, W / 2 + pw / 2, 359), fill=A(RED, a1), r=32)
    text(d, (W / 2, 327), "BẪY", 38, WHITE, alpha=a1)
    ks = clamp((t - 1.6) / 0.4); yy = 470
    lw = segs(d, W / 2, yy, [("“", INK), ("g", mix(INK, MUTED, ks), True), (" = 9,70 khác 9,8 → hỏng”", mix(INK, MUTED, ks))], 48, alpha=a1)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        text(d, (W / 2, yy + 85), "✗", 56, RED, alpha=ks * a1)
    kk = appear(t, 2.4, 0.5)
    segs(d, W / 2, 680, [("Xét cả khoảng ", INK), ("9,55 → 9,85", GREEN)], 50, alpha=kk)
    # truc so
    card(d, (40, 830, 1040, 1595), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 900), "g (m/s²)", 40, GREEN)
    arrow(d, (NX0 - 50, NY), (NX(9.9) + 60, NY), INK, w=4, head=18)
    for k in range(5):
        g = 9.5 + 0.1 * k; x = NX(g)
        d.line([(x, NY - 12), (x, NY + 12)], fill=INK, width=3)
        if abs(g - 9.8) > 1e-6: text(d, (x, NY + 50), vn(g, 1), 38, INK, bold=False)
    kb = clamp((t - 2.4) / 0.8)
    if kb > 0:                                                    # khoang 9,55 - 9,85 mo dan tu 9,70 ra hai phia
        xa, xb = NX(9.70 - 0.15 * kb), NX(9.70 + 0.15 * kb)
        d.rounded_rectangle([xa, NY - 20, xb, NY + 20], radius=10, fill=A(GREEN, 0.45))
        for x in (xa, xb): d.line([(x, NY - 34), (x, NY + 34)], fill=GREEN, width=6)
        ke = appear(t, 3.2, 0.4)
        text(d, (NX(9.55), NY - 75), "9,55", 40, GREEN, alpha=ke)
        text(d, (NX(9.85), NY - 75), "9,85", 40, GREEN, alpha=ke)
    dot(d, NX(9.70), NY, 15, NAVY, WHITE)
    segs(d, NX(9.70), NY - 75, [("g", NAVY, True)], 42)
    x8 = NX(9.8)                                                  # moc 9,8 (tham khao): tam giac do o duoi truc
    d.polygon([(x8, NY + 85), (x8 - 16, NY + 115), (x8 + 16, NY + 115)], fill=RED_D)
    text(d, (x8, NY + 150), "9,8", 42, RED_D)
    kc = appear(t, 3.6, 0.5)
    segs(d, W / 2, 1450, [("9,8", RED_D), (" nằm trong khoảng → phù hợp", INK)], 44, alpha=kc)
    text(d, (W / 2, 1530), "✓", 56, GREEN, alpha=appear(t, 4.2, 0.4))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        ka = appear(t, M[0] + 0.4, 0.5)
        ctext(d, 900, "Chỉ dùng lần 2 (t = 0,322 s):", 46, INK, maxw=900, alpha=ka)
        ctext(d, 990, "g lớn hơn hay nhỏ hơn 9,70 m/s²?", 46, INK, maxw=900, alpha=ka)
        kh = appear(t, M[0] + 3.0, 0.5)
        if kh <= 0: return
        card(d, (110, 1220, 970, 1380), fill=A(HL, kh), r=24)
        segs(d, W / 2, 1300, [("So 0,322 s với ", ORANGE), ("t", ORANGE, True)], 44, alpha=kh)
    chot_hoi(d, t, sc, "Kết quả đo là một khoảng:\ng = ḡ ± Δg", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for s0, f0, f1 in SCHED: cs.append((do["t0"] + f1, "tap"))
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 1.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-do-g-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành đo gia tốc rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Năm lần thả, một độ cao", draw=s_hook, tail=0.6, caps=[
   ("Cổng quang cách đáy bi 0,500 m.", 3.0),
   ("Dừng video, chọn câu trả lời.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Ngắt nam châm: bi rơi, đồng hồ chạy.", 4.0),
   ("Bi che tia sáng: đồng hồ dừng.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Năm lần, năm số khác nhau.", 4.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Lấy trung bình, rồi độ lệch từng lần.", 3.7),
   ("Cộng thêm độ chia đồng hồ.", 3.4),
   ("Còn điều chưa biết.", 3.0)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.5, caps=[
   ("Khác 9,8 có phải hỏng?", 4.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
