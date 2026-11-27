# Clip: tn-l10-do-g-01 - Do g bang cong quang: tha bi 5 lan tu s = 0,500 m, xu li sai so (10/11/2026; dung lai 27/11/2026
# theo cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Du doan khong nut, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-g-01.json (_kiem_so() doi chieu):
#   so_lieu_mau: t = 0,319 / 0,322 / 0,321 / 0,323 / 0,320 s ; |t - tTB| = 0,002 / 0,001 / 0 / 0,002 / 0,001 s.
#   ghi_chu: tTB = 0,321 ; gTB = 9,70 ; Dg = 0,15. Dt = 0,0012 + 0,001 (dcnn_t) = 0,0022 s.
# Du doan (moi, vi o Quan sat cua bai da noi "vai phan nghin giay"): dong ho chia 0,001 s, sai so Dt co bao nhieu?
#   -> khoang 0,002 s (lon hon do chia vi con do phan tan). Khung: A 0,0005 / B 0,001 / C 0,002 / D 0,02 s.
# KHONG hien delta = Ds/s + 2Dt/tTB va hai phan 0,2 % / 1,4 % (Cau 2 cua bai). KHONG noi tu du (Cau 4).
# Bay = hien_tuong_hay_sai thu 3: thay 9,70 khac 9,8 lien ket luan hong -> xet khoang 9,55-9,85.
# Thu nghi (= cau_chot khung web, theo mo hinh tre_ht ~ 0,001 trong mien 0-0,006, nhieu <= 0,002): s = 0,700 m, 5 lan
#   t = 0,377/0,381/0,379/0,380/0,378 s -> tTB = 0,379 -> g = 1,4/0,379^2 = 9,75 m/s2 (trong khoang Bay, khac 9,70 va 9,8).
#   Ba buoc; 9,75 khong hien. Khong dung s = 0,800 m (bai da co cau 0,800 m / 0,404 s).
from engine import *

S = 0.500
TS = [0.319, 0.322, 0.321, 0.323, 0.320]
DEV = [0.002, 0.001, 0.0, 0.002, 0.001]
TB, DTB, DT, GTB, DG = 0.321, 0.0012, 0.0022, 9.70, 0.15
CH_S, CH_T = 0.700, [0.377, 0.381, 0.379, 0.380, 0.378]

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-do-g-01.json")))
    h = k["so_lieu_mau"]["hang"]
    assert [r[1] for r in h] == TS and [r[2] for r in h] == DEV
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["s"]["mac_dinh"] == S and ts["dcnn_t"]["gia_tri"] == 0.001
    assert round(sum(TS) / 5, 3) == TB and abs(sum(DEV) / 5 - DTB) < 1e-9 and abs(DTB + 0.001 - DT) < 1e-9
    assert f"{2 * S / TB ** 2:.2f}" == "9.70"
    g0 = 2 * S / TB ** 2; dl = 0.001 / S + 2 * DT / TB; assert f"{g0 * dl:.2f}" == "0.15"
    assert ts["s"]["min"] <= CH_S <= ts["s"]["max"]
    tb = sum(CH_T) / 5; assert abs(tb - 0.379) < 1e-9 and max(abs(x - tb) for x in CH_T) <= ts["nhieu"]["max"]
    tre = tb - math.sqrt(2 * CH_S / ts["g_that"]["gia_tri"]); assert 0 <= tre <= ts["tre_ht"]["max"] + 5e-4
    assert f"{2 * CH_S / tb ** 2:.2f}" == "9.75" and f"{CH_S / tb ** 2:.2f}" == "4.87"
_kiem_so()

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
POST = (71, 85, 105); RED_D = (185, 28, 28); HL = (255, 247, 237)
DRED = (185, 28, 28); DTEAL = (15, 118, 110); EMPTY = (148, 140, 128); C_T = (29, 78, 216); C_DEV = (109, 40, 217)
DGREEN = (21, 128, 61)

def segs(d, x, y, parts, size, alpha=1.0):
    """Chu nhieu mau mot dong (giua x). parts = [(chu, mau)] hoac [(chu, mau, True)] -> gach ngang tren (t trung binh)."""
    f = F(size); tot = sum(tw(d, p[0], f) for p in parts); xx = x - tot / 2
    for p in parts:
        s, c = p[0], p[1]; w = tw(d, s, f)
        dtext(d, (xx, y), s, f, c, alpha, "lm")
        if len(p) > 2 and p[2]:
            yb = y - size * 0.6
            d.line([(xx + w * 0.1, yb), (xx + w * 0.9, yb)], fill=A(c, alpha), width=max(4, size // 14))
        xx += w
    return tot

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def badge(d, y, s, col, a=1.0):
    pw = tw(d, s, F(58)) + 64
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 82), fill=A(col, a), r=40)
    text(d, (W / 2, y + 41), s, 58, WHITE, alpha=a)

# ---------------- gia do: nam cham, bi, thuoc, cong quang (ben trai) ----------------
SY0, SPX = 360, 1500.0                    # y day bi luc con o nam cham ; px / m
def SYp(s): return SY0 + SPX * s
BX, BR = 285, 22
def rig(d, ball_s, ball_a=1.0, s_lab=False, gate_s=S):
    card(d, (40, 215, 420, 1290), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([150, SY0 - 6, 180, SYp(0.5) + 10], fill=WOOD, outline=WOOD_D, width=3)          # thuoc
    for i in range(6):
        y = SYp(i / 10); d.line([(150, y), (176, y)], fill=INK, width=3)
    text(d, (140, SY0), "0", 56, INK, anchor="rm")
    d.rectangle([240, 235, 330, SY0 - 2 * BR], fill=NAVY)                                        # nam cham dien
    yg = SYp(gate_s)
    d.line([(250, yg), (320, yg)], fill=RED, width=5)
    d.rectangle([222, yg - 22, 250, yg + 22], fill=POST); d.rectangle([320, yg - 22, 348, yg + 22], fill=POST)
    text(d, (230, yg + 75), "cổng quang", 56, INK)
    if s_lab:
        arrow(d, (385, SY0 + 40), (385, yg - 8), C_T, w=5, head=18); arrow(d, (385, yg - 40), (385, SY0 + 8), C_T, w=5, head=18)
        text(d, (345, (SY0 + yg) / 2), "s", 60, C_T, anchor="rm")
    if ball_s is not None and ball_a > 0.02:
        y = SYp(ball_s) - BR
        d.ellipse([BX - BR, y - BR, BX + BR, y + BR], fill=A(STEEL, ball_a), outline=A(NAVY, ball_a), width=2)
        d.ellipse([BX - 10, y - 11, BX - 2, y - 3], fill=A(STEEL_L, ball_a))

def clock(d, val, lit=True, box=(440, 215, 1040, 365)):
    card(d, box, fill=NAVY, r=26)
    text(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), "t = " + vn(val, 3) + " s", 64, YELLOW if lit else GRAY)

# ---------------- bang t (hep, canh do) ----------------
def table_t(d, n, cur=None, a=1.0):
    card(d, (440, 385, 1040, 1290), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (560, 450), "Lần", 56, INK, alpha=a); text(d, (850, 450), "t (s)", 56, C_T, alpha=a)
    d.line([(460, 500), (1020, 500)], fill=A(LIGHT, a), width=3)
    for i in range(5):
        y = 580 + i * 120
        if cur == i: d.rounded_rectangle([455, y - 48, 1025, y + 48], radius=16, fill=A(HL, a))
        text(d, (560, y), str(i + 1), 56, MUTED, alpha=a)
        if i < n: text(d, (850, y), vn(TS[i], 3), 60, C_T, alpha=a)

# ---------------- bang rong (dap an / rut ra) ----------------
WX = (150, 450, 800)
def table_w(d, n_dev=0, k_tb=0.0, k_dtb=0.0, box=(40, 580, 1040, 1290)):
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    y0 = box[1] + 60
    text(d, (WX[0], y0), "Lần", 56, INK); text(d, (WX[1], y0), "t (s)", 56, C_T)
    segs(d, WX[2], y0, [("|t − ", C_DEV), ("t", C_DEV, True), ("| (s)", C_DEV)], 56)
    d.line([(60, y0 + 45), (1020, y0 + 45)], fill=LIGHT, width=3)
    for i in range(5):
        y = y0 + 110 + i * 88
        text(d, (WX[0], y), str(i + 1), 56, MUTED); text(d, (WX[1], y), vn(TS[i], 3), 58, C_T)
        if i < n_dev: text(d, (WX[2], y), vn(DEV[i], 3), 58, C_DEV)
    yt = y0 + 110 + 5 * 88 + 10
    if max(k_tb, k_dtb) > 0:
        d.line([(60, yt - 50), (1020, yt - 50)], fill=A(INK, max(k_tb, k_dtb)), width=3)
        text(d, (WX[0], yt), "TB", 56, INK, alpha=max(k_tb, k_dtb))
        text(d, (WX[1], yt), "0,321", 60, C_T, alpha=k_tb)
        text(d, (WX[2], yt), "0,0012", 60, C_DEV, alpha=k_dtb)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0.0, s_lab=True); clock(d, 0.0, lit=False)
    card(d, (440, 385, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    k0 = 1.0
    text(d, (740, 520), "Thả bi 5 lần,", 60, INK, alpha=k0)
    text(d, (740, 610), "s = 0,500 m.", 60, C_T, alpha=k0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 760 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 26, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Đồng hồ chia 0,001 s.", 62, INK, alpha=a)
    segs(d, W / 2, y0 + 265, [("Sai số Δt cỡ bao nhiêu?", PURPLE)], 62, alpha=a)
    seg_bar(d, y0 + 350, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (5 lan tha, chieu cham 2 lan) ----------------
SLOW, PAUSE, HOLD, RUN0 = 2.0, 0.3, 0.35, 0.3
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
    if t < f0: return 0.0, appear(t, s0, 0.2) if j > 0 else 1.0, prev, j > 0, j, j
    u = clamp((t - f0) / (f1 - f0))
    if t < f1: return S * u * u, 1.0, round(TS[j] * u, 3), True, j, j
    return S, 1 - clamp((t - f1) / 0.25), TS[j], True, j + 1, j

def s_do(img, d, t, sc):
    bs, ba, cv, lit, done, j = run_state(t)
    rig(d, bs, ba); clock(d, cv, lit); table_t(d, done, cur=j if done <= j else None)
    card(d, (40, 1310, 1040, 1430), fill=NAVY, r=30)
    text(d, (W / 2, 1370), "chiếu chậm ×2", 58, YELLOW)

# ---------------- canh 3: Dap an (Dt = lech TB + do chia) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 560), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL, ka)
    text(d, (W / 2, 400), "Δt ≈ 0,002 s,", 64, DTEAL, alpha=ka)
    text(d, (W / 2, 485), "lớn hơn độ chia 0,001 s", 60, DTEAL, alpha=ka)
    nd = sum(1 for i in range(5) if t >= 0.6 + 0.3 * i)
    table_w(d, n_dev=nd, k_tb=appear(t, 0.4, 0.3), k_dtb=appear(t, 2.3, 0.3))
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 1310, 1040, 1590), fill=A(WHITE, k2), outline=A(C_DEV, k2), w=5)
    segs(d, W / 2, 1390, [("Δt = ", INK), ("0,0012 s", C_DEV), (" + ", INK), ("0,001 s", DTEAL)], 58, alpha=k2)
    text(d, (W / 2, 1500), "= 0,0022 s", 60, INK, alpha=k2)

# ---------------- canh 4: Rut ra (g tu t trung binh, ket qua la khoang) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    segs(d, W / 2, 300, [("g = 2s / ", INK), ("t", C_T, True), ("²", C_T)], 62)
    k1 = appear(t, 0.5, 0.4)
    segs(d, W / 2, 410, [("= 2 · 0,500 m : (", INK), ("0,321 s", C_T), (")²", INK)], 58, alpha=k1)
    segs(d, W / 2, 510, [("≈ 9,70 m/s²", DGREEN)], 62, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    card(d, (60, 590, 1020, 730), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
    text(d, (W / 2, 660), "g = 9,70 ± 0,15 m/s²", 64, DGREEN, alpha=k2)
    # thuoc so g ben duoi: khoang mo dan tu 9,70
    numline(d, t, kb=clamp((t - M[1] - 0.3) / 0.9), show98=False, box=(40, 780, 1040, 1290))

NX0, NPX = 160, 1900.0
def NX(g): return NX0 + (g - 9.5) * NPX
def numline(d, t, kb, show98=True, box=(40, 780, 1040, 1290), ke=1.0):
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    NY = box[1] + (box[3] - box[1]) * 0.55
    text(d, (W / 2, box[1] + 65), "g (m/s²)", 58, DGREEN)
    arrow(d, (NX0 - 70, NY), (NX(9.9) + 80, NY), INK, w=5, head=20)
    for k in range(5):
        g = 9.5 + 0.1 * k; x = NX(g)
        d.line([(x, NY - 14), (x, NY + 14)], fill=INK, width=4)
        if not (show98 and abs(g - 9.8) < 1e-6): text(d, (x, NY + 62), vn(g, 1), 56, INK)
    if kb > 0:
        xa, xb = NX(GTB - DG * kb), NX(GTB + DG * kb)
        d.rounded_rectangle([xa, NY - 22, xb, NY + 22], radius=10, fill=A(GREEN, 0.45))
        for x in (xa, xb): d.line([(x, NY - 38), (x, NY + 38)], fill=GREEN, width=7)
        if kb >= 1:
            text(d, (NX(9.55), NY - 85), "9,55", 56, DGREEN, alpha=ke); text(d, (NX(9.85), NY - 85), "9,85", 56, DGREEN, alpha=ke)
    dot(d, NX(GTB), NY, 17, NAVY, WHITE)
    if show98:
        x8 = NX(9.8)
        d.polygon([(x8, NY + 40), (x8 - 18, NY + 72), (x8 + 18, NY + 72)], fill=RED_D)
        text(d, (x8, NY + 115), "9,8", 58, RED_D)
    return NY

# ---------------- canh 5: Bay (khac 9,8 la hong) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 300), "✗ 9,70 khác 9,8 m/s²", 62, DRED)
    text(d, (W / 2, 420), "→ thí nghiệm hỏng?", 62, DRED)
    numline(d, t, kb=clamp((t - M[1] + 0.2) / 0.8), box=(40, 580, 1040, 1290))
    if t >= M[1] - 0.1:
        card(d, (40, 1310, 1040, 1590), fill=WHITE, outline=DTEAL, w=6)
        text(d, (W / 2, 1395), "✓ 9,8 nằm trong", 60, DTEAL)
        text(d, (W / 2, 1500), "9,55 → 9,85 m/s²", 60, DTEAL)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (440, 215, 1040, 760), fill=WHITE, outline=NAVY, w=6)
    text(d, (740, 300), "Chưa nói được", 60, NAVY)
    text(d, (740, 430), "Mới thả ở", 60, INK); text(d, (740, 520), "s = 0,500 m.", 60, C_T)
    text(d, (740, 650), "s khác: g = ?", 62, DTEAL, alpha=appear(t, 1.6, 0.4))
    u = 0.4 + 0.1 * math.sin(t * 1.6)
    rig(d, None, gate_s=u, s_lab=True)

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "s = 0,700 m, thả 5 lần:", 60, INK, alpha=k)
    text(d, (W / 2, 520), "t (s): 0,377; 0,381; 0,379;", 58, C_T, alpha=k)
    text(d, (W / 2, 610), "0,380; 0,378.", 58, C_T, alpha=k)
    segs(d, W / 2, 760, [("g", DGREEN, True), (" bằng bao nhiêu (m/s²)?", DGREEN)], 62, alpha=k)
    seg_bar(d, 1260, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + f1, "tap") for s0, f0, f1 in SCHED]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-do-g-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành đo gia tốc rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Năm lần thả, một độ cao", draw=s_hook, tail=0.3, caps=[
   ("Cổng quang cách bi 0,500 m.", 3.2),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Ngắt nam châm: bi rơi.", 3.3),
   ("Bi che tia: đồng hồ dừng.", 3.3)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Lấy trung bình, rồi độ lệch.", 3.4),
   ("Cộng thêm độ chia đồng hồ.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Thay t trung bình vào công thức.", 3.4),
   ("Kết quả là một khoảng.", 3.2)]),
 dict(key="bay", title="Bẫy: khác 9,8 là hỏng", draw=s_bay, tail=0.3, caps=[
   ("Khác 9,8 có phải hỏng?", 3.4),
   ("Xét cả khoảng sai số.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Mới thả ở một độ cao.", 3.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.0)]),
])
