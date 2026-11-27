# Clip: tn-l10-ctbdd-01 - Xe lan tha tu nghi tren mang nghieng, cong quang do v tai 4 vi tri (31/10/2026; dung lai
# 27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Du doan khong nut, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-ctbdd-01.json (_kiem_so() doi chieu):
#   tham_so: a = 0,5 m/s2 (mien 0,2-1,0), d = 2,00 cm (bai goi la b), dong ho chia 0,001 s.
#   so_lieu_mau (cot doc): s = 10/20/40/60 cm ; t 0,635/0,892/1,262/1,551 s ; tau 0,064/0,045/0,032/0,026 s ;
#                v = b/tau hien 2 chu so nhu bang trong bai: 0,31/0,44/0,63/0,77 m/s ; v/t 0,49/0,49/0,50/0,50.
# Du doan (giu y cu, K10 khong nut): doi cong 2 tu 20 ra 40 cm, v tai cong 2 doi ra sao? -> tang ~1,4 lan, chua toi gap doi.
# Bay = hien_tuong_hay_sai "v = s/t": dung hang 60 cm (khac cap 20/40 cua Du doan): 0,60 : 1,551 = 0,39 m/s, chi bang nua 0,77.
# Thu nghi (= cau_chot khung web, theo mo hinh v = a.t): mang doc hon a = 0,80 (mien 0,2-1,0), t = 1,0 s (s = 0,40 m trong
#   mien 0,1-0,8) -> v = 0,80 m/s -> tau = b/v = 0,025 s. Hai buoc; noi suy tu bang (a = 0,5) ra 0,040 = bay; 0,025 khong hien.
from engine import *

ACC, B = 0.5, 0.02
ROWS = [(10, 0.635, 0.064, "0,31"), (20, 0.892, 0.045, "0,44"), (40, 1.262, 0.032, "0,63"), (60, 1.551, 0.026, "0,77")]
VT = ("0,49", "0,49", "0,50", "0,50")
CHOT_T, CHOT_A = 1.0, 0.8

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-ctbdd-01.json")))
    h = k["so_lieu_mau"]["hang"]
    for r, (s, t, tau, vs) in zip(h, ROWS):
        assert abs(r[0] * 100 - s) < 1e-9 and r[3] == t and r[4] == tau and abs(r[5] - float(vs.replace(",", "."))) <= 0.005 + 1e-9
    for (s, t, tau, vs), q in zip(ROWS, VT): assert f"{float(vs.replace(',', '.')) / t:.2f}".replace(".", ",") == q
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["a"]["mac_dinh"] == ACC and ts["d"]["gia_tri"] == B
    s_ch = CHOT_A * CHOT_T ** 2 / 2; assert ts["s"]["min"] <= s_ch <= ts["s"]["max"]
    assert ts["a"]["min"] <= CHOT_A <= ts["a"]["max"] and all(abs(r[2] - 0.025) > 5e-4 for r in ROWS)
    assert abs(B / (CHOT_A * CHOT_T) - 0.025) < 1e-12 and abs(0.60 / 1.551 - 0.387) < 1e-3
_kiem_so()

C_T, C_V, C_TAU = (29, 78, 216), (176, 64, 8), (109, 40, 217)
DRED = (185, 28, 28); DTEAL = (15, 118, 110); EMPTY = (148, 140, 128)
CART = (100, 116, 139); CART_D = (51, 65, 85); RAIL = (203, 207, 218); RAIL_D = (148, 153, 168); POST = (71, 85, 105)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

# ---------------- mang + cong quang (o tren) ----------------
R0, R1 = (80, 380), (1000, 530)
RL = math.hypot(R1[0] - R0[0], R1[1] - R0[1]); RU = ((R1[0] - R0[0]) / RL, (R1[1] - R0[1]) / RL); RN = (RU[1], -RU[0])
def RP(s, h): return (R0[0] + RU[0] * s + RN[0] * h, R0[1] + RU[1] * s + RN[1] * h)
S0, PXM = 170, 1050                                    # cho tha (px doc mang), px/m

def gate(d, s_px, lab):
    b = RP(s_px, 0); top = (b[0], b[1] - 100)
    d.rectangle([b[0] - 7, top[1], b[0] + 7, b[1] + 20], fill=POST)
    d.rectangle([b[0] - 20, top[1] - 6, b[0] + 20, top[1] + 22], fill=POST)
    dot(d, b[0], top[1] + 8, 7, (239, 68, 68))
    if lab: text(d, (min(b[0], 1015 - tw(d, lab, F(56)) / 2), top[1] - 40), lab, 56, INK)

def rig(d, s_cart, s_gate, glab="cổng 2", box=(40, 205, 1040, 560)):
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    d.polygon([RP(0, 0), RP(RL, 0), RP(RL, -18), RP(0, -18)], fill=RAIL, outline=RAIL_D)
    gate(d, S0, "")
    text(d, (70, 500), "cổng 1 = chỗ thả", 56, INK, anchor="lm")
    if s_gate is not None: gate(d, S0 + s_gate * PXM, glab)
    p = S0 + s_cart * PXM
    d.polygon([RP(p - 120, 8), RP(p, 8), RP(p, 56), RP(p - 120, 56)], fill=CART, outline=CART_D)
    d.polygon([RP(p - 70, 56), RP(p - 56, 56), RP(p - 56, 100), RP(p - 70, 100)], fill=(17, 17, 17))
    for sw in (p - 95, p - 25):
        c = RP(sw, 6); d.ellipse([c[0] - 11, c[1] - 11, c[0] + 11, c[1] + 11], fill=CART_D)

# ---------------- do thi v-t ----------------
GB = (40, 690, 1040, 1290)
GX0, GYB = 200, 1190
def GX(t): return GX0 + t * 440
def GY(v): return GYB - v * 560
def graph(d, n, line=0.0, ring=(), vlab=True, box=GB):
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    for v in (0.2, 0.4, 0.6, 0.8): d.line([(GX0, GY(v)), (GX(1.7), GY(v))], fill=(240, 236, 228), width=2)
    arrow(d, (GX0, GYB), (GX(1.7) + 50, GYB), NAVY, w=5, head=18); arrow(d, (GX0, GYB), (GX0, GY(0.8) - 45), NAVY, w=5, head=18)
    for t in (0.5, 1.0, 1.5):
        d.line([(GX(t), GYB), (GX(t), GYB + 12)], fill=NAVY, width=4); text(d, (GX(t), GYB + 48), vn(t, 1), 56, C_T)
    for v in (0.2, 0.4, 0.6, 0.8):
        d.line([(GX0 - 12, GY(v)), (GX0, GY(v))], fill=NAVY, width=4); text(d, (GX0 - 22, GY(v)), vn(v, 1), 56, C_V, anchor="rm")
    text(d, (1030, GYB - 45), "t (s)", 58, C_T, anchor="rm")
    text(d, (GX0 + 35, GY(0.8) - 48), "v (m/s)", 58, C_V, anchor="lm")
    if line > 0: d.line([(GX(0), GY(0)), (GX(1.65 * line), GY(ACC * 1.65 * line))], fill=DTEAL, width=8)
    for i in range(n):
        s, t, tau, vs = ROWS[i]; v = float(vs.replace(",", "."))
        if i in ring: d.ellipse([GX(t) - 34, GY(v) - 34, GX(t) + 34, GY(v) + 34], outline=NAVY, width=6)
        dot(d, GX(t), GY(v), 16, C_V, WHITE)
        if vlab: text(d, (GX(t) - 26, GY(v) - 40), vs, 56, C_V, anchor="rm")

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

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    sg = 0.20 + 0.20 * ease((t - 1.2) / 1.2)
    rig(d, 0.0, sg, glab=f"cổng 2: {int(round(sg * 100))} cm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 640 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 26, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Cổng 2: từ 20 ra 40 cm.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "v tại cổng 2 đổi ra sao?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 350, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 lan tha) ----------------
RUN0, RG = 0.4, 1.7
def run_state(t):
    i = min(3, max(0, int((t - RUN0) / RG)))
    tau_ = t - RUN0 - RG * i
    return i, tau_

def s_do(img, d, t, sc):
    i, tr = run_state(t); s, tt, tau, vs = ROWS[i]
    trun = clamp(tr, 0, tt); sc_ = ACC * trun * trun / 2
    if tr >= tt: sc_ = s / 100 + 0.04 * clamp((tr - tt) / 0.3)
    rig(d, sc_ if t >= RUN0 else 0.0, s / 100, glab=f"cổng 2: {s} cm")
    card(d, (40, 575, 1040, 675), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 625), "t = " + vn(clamp(tr, 0, tt) if t >= RUN0 else 0, 3) + " s", 58, C_T, anchor="lm")
    text(d, (1000, 625), "τ = " + (vn(tau, 3) if tr >= tt else "0,000") + " s", 58, C_TAU, anchor="rm")
    n = i + (1 if tr >= tt + 0.1 else 0)
    graph(d, n)
    card(d, (40, 1310, 1040, 1450), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 1380), "v = b / τ,  b = 2,00 cm", 58, INK)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 560), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL, ka)
    text(d, (W / 2, 400), "Tăng, nhưng", 64, DTEAL, alpha=ka)
    text(d, (W / 2, 485), "chưa tới gấp đôi", 64, DTEAL, alpha=ka)
    graph(d, 4, ring=(1, 2), box=(40, 690, 1040, 1290))
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 1310, 1040, 1590), fill=A(WHITE, k2), outline=A(C_T, k2), w=5)
    text(d, (W / 2, 1390), "t: 0,892 → 1,262 s", 60, C_T, alpha=k2)
    text(d, (W / 2, 1500), "v: 0,44 → 0,63 m/s", 60, C_V, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 280), "v / t (m/s²)", 60, DTEAL)
    for i in range(4):
        ki = appear(t, 0.6 + 0.3 * i, 0.3)
        text(d, (180 + i * 240, 400), VT[i], 62, DTEAL, alpha=ki)
    kb = appear(t, M[1] + 0.1, 0.45)
    text(d, (W / 2, 505), "v = a·t,  a ≈ 0,50 m/s²", 60, GREEN, alpha=kb)
    graph(d, 4, line=ease((t - M[1]) / 1.0), vlab=False)

# ---------------- canh 5: Bay (v = s/t) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 285), "✗ v = s / t", 62, DRED)
    text(d, (W / 2, 385), "s = 0,60 m, t = 1,551 s", 58, INK)
    text(d, (W / 2, 480), "0,60 m : 1,551 s ≈ 0,39 m/s", 58, DRED)
    graph(d, 4, vlab=False, box=(40, 580, 1040, 1290))
    s, tt, tau, vs = ROWS[3]
    k1 = ease((t - 0.6) / 0.8)
    x = GX0
    while x < GX0 + (GX(tt) - GX0) * k1: d.line([(x, GY(0.387)), (min(x + 22, GX(tt)), GY(0.387))], fill=DRED, width=7); x += 38
    if k1 > 0.99: dot(d, GX(tt), GY(0.387), 16, DRED, WHITE)
    if t >= M[1] - 0.1:
        dot(d, GX(tt), GY(0.77), 22, C_V, WHITE); d.ellipse([GX(tt) - 38, GY(0.77) - 38, GX(tt) + 38, GY(0.77) + 38], outline=DTEAL, width=7)
        card(d, (40, 1310, 1040, 1590), fill=WHITE, outline=DTEAL, w=6)
        text(d, (W / 2, 1395), "✓ Đo tại cổng: 0,77 m/s", 60, DTEAL)
        text(d, (W / 2, 1500), "s / t chỉ bằng một nửa", 60, DTEAL)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 450), "Xa hơn 60 cm: a còn đều?", 62, INK)
    u = (t * 0.45) % 1.0
    card(d, (40, 590, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    y = 900
    d.line([(100, y), (980, y)], fill=RAIL_D, width=10)
    for k in range(7):
        x = 100 + k * 120; col = C_V if x <= 700 else EMPTY
        d.line([(x, y - 14), (x, y + 14)], fill=col, width=5)
    for yy in range(700, 1060, 26): d.line([(700, yy), (700, yy + 13)], fill=MUTED, width=4)
    text(d, (700, 1060), "60 cm", 56, INK)
    xc = 380 + 520 * u
    d.rectangle([xc - 80, y - 60, xc + 40, y - 12], fill=CART, outline=CART_D)
    text(d, (860, 760), "a = ?", 62, DTEAL, alpha=appear(t, 2.2, 0.4))

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "Máng dốc hơn: a = 0,80 m/s².", 60, INK, alpha=k)
    text(d, (W / 2, 485), "t = 1,0 s, b = 2,00 cm.", 60, INK, alpha=k)
    text(d, (W / 2, 590), "τ đọc được bao nhiêu?", 64, C_TAU, alpha=k)
    gx, gy = 540, 960
    d.rectangle([gx - 9, gy - 230, gx + 9, gy + 60], fill=A(POST, k))
    d.rectangle([gx - 26, gy - 240, gx + 26, gy - 205], fill=A(POST, k))
    d.polygon([(gx - 330, gy - 10), (gx - 90, gy - 10), (gx - 90, gy + 50), (gx - 330, gy + 50)], fill=A(CART, k), outline=A(CART_D, k))
    d.rectangle([gx - 200, gy - 110, gx - 180, gy - 10], fill=A((17, 17, 17), k))
    arrow(d, (gx - 60, gy + 110), (gx + 160, gy + 110), A(C_V, k), w=7, head=22)
    text(d, (gx + 170, gy - 120), "τ = ?", 64, C_TAU, alpha=k)
    seg_bar(d, 1260, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + RUN0 + RG * i + ROWS[i][1], "tap") for i in range(4)]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-ctbdd-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động thẳng biến đổi đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe lăn trên máng nghiêng", draw=s_hook, tail=0.3, caps=[
   ("Thả xe từ nghỉ.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cổng 2 ở bốn chỗ.", 3.4),
   ("Mỗi lần thả: thêm một điểm.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So hai điểm khoanh tròn.", 3.0),
   ("t chỉ tăng khoảng 1,4 lần.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Chia v cho t từng lần.", 3.4),
   ("Đồ thị thẳng, qua gốc.", 3.2)]),
 dict(key="bay", title="Bẫy: lấy s chia t", draw=s_bay, tail=0.3, caps=[
   ("Lấy s chia t được không?", 3.4),
   ("Đó là v trung bình.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Mới đo tới 60 cm.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.2)]),
])
