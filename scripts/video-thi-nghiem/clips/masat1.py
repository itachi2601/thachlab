# Clip: tn-l10-luc-ma-sat-01 - Keo hop go bang luc ke: nghi cuc dai va truot (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-luc-ma-sat-01.json (_kiem_so() doi chieu):
#   so_lieu_mau (N, nghi max, truot): 1,96 0,7 0,6 ; 3,92 1,5 1,2 ; 5,88 2,1 1,7 ; 7,84 2,9 2,4 (m = 0,20..0,80 kg, g = 9,8)
#   dung_cu: luc ke 5 N chia 0,1 N ; tham_so mu_n = 0,36, m toi da 1,0 kg.
# Du doan (K10, khong nut): keo tang dan toi luc hop bat di -> ngay luc do so chi luc ke doi ra sao? (dap an: tut xuong).
#   Doi ca so voi ban 1 (keo 0,3 N hop yen -> ma sat?) vi trung quiz mo bai (day 50 N) va Cau 3 Tu kiem tra.
# Bay = hien_tuong_hay_sai[1] (ma sat nghi luon bang muc cuc dai) noi bang so cua hop nay (0,7 N), khong hien mu.
# KHONG tra loi san "Doc so lieu" (F/N, mu, lan do kem tin cay): khong hien N = 1,96..., khong hien ti so, khong noi sai so.
# Chot (ca tu suy, mo hinh F_nghi_max = mu_n.N): tong 1,00 kg -> 0,36 . 9,8 = 3,5 N (= 5 x 0,7). Khong co trong bai/bang.
from engine import *

ROWS = [(0.20, 0.7, 0.6), (0.40, 1.5, 1.2), (0.60, 2.1, 1.7), (0.80, 2.9, 2.4)]   # m (kg), nghi max, truot
G, FMAX = 9.8, 5.0
F_NGHI, F_TRUOT = ROWS[0][1], ROWS[0][2]
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-luc-ma-sat-01.json")))
    for (m, a, b), h in zip(ROWS, k["so_lieu_mau"]["hang"]):
        assert abs(m * G - h[0]) < 1e-9 and a == h[1] and b == h[2], (m, h)
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["μn"]["gia_tri"] == 0.36 and ts["m"]["max"] >= 1.0 and round(0.36 * 1.0 * G, 1) == 3.5
_kiem_so()

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOX = (232, 196, 140); BOX_D = (150, 104, 56)
SKIN = (240, 196, 160); SKIN_D = (190, 140, 105); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
EMPTY = (148, 140, 128); NOTE = (60, 64, 84); DORANGE = (176, 64, 8); WT = (120, 126, 140)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- dan thi nghiem (nhin ngang, keo sang PHAI) ----------------
SURF = 640; BX0, BW, BH = 60, 240, 120
HOOK_Y = SURF - BH / 2; ROPE, BODY = 30, 400

def box(d, xl, y, lab, n_wt=0, a=1.0):
    """Hop go day o y, mep trai xl; n_wt khoi gia trong chong len tren."""
    for j in range(n_wt):
        yy = y - BH - (j + 1) * 46
        d.rounded_rectangle([xl + 50, yy, xl + BW - 50, yy + 42], radius=8, fill=A(WT, a), outline=A(NAVY, a), width=3)
    d.rounded_rectangle([xl, y - BH, xl + BW, y], radius=12, fill=A(BOX, a), outline=A(BOX_D, a), width=4)
    text(d, (xl + BW / 2, y - BH / 2), lab, 56, INK, alpha=a)

def rig(d, xl, f_read):
    card(d, (40, 270, 1040, 720), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([40, SURF, 1040, SURF + 40], fill=WOOD); d.line([(40, SURF), (1040, SURF)], fill=WOOD_D, width=4)
    box(d, xl, SURF, "0,20 kg")
    xr = xl + BW
    Q = lambda s, h=0.0: (xr + s, HOOK_Y + h)
    d.line([Q(0), Q(ROPE - 13)], fill=NAVY, width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, f_read, nho=0.1, so=(0, 1, 2, 3, 4), hw=44, ben=-1, co=55)
    d.line([Q(se - 16), Q(se + 12)], fill=NAVY, width=8)
    hx, hy = Q(se + 40); dot(d, hx, hy, 28, SKIN, outline=SKIN_D)

def readout(d, f, y=790, a=1.0):
    card(d, (W / 2 - 170, y - 46, W / 2 + 170, y + 46), fill=A((254, 242, 242), a), outline=A(RED, a), r=24, w=4)
    text(d, (W / 2, y), vn(f) + " N", 64, RED, alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    f = 0.4 * ease((t - 0.6) / 2.2)                 # keo nhe, hop van yen (0,4 N < 0,7 N)
    rig(d, BX0, f)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 790 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 760), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    for j, s1 in enumerate(("Kéo tăng dần.", "Lúc hộp vừa bật đi,", "số chỉ lực kế ra sao?")):
        text(d, (W / 2, y0 + 220 + j * 100), s1, 62, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 600, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (keo tang dan, do thi F theo t) ----------------
T0, T_SLIP, T_DROP, T_END = 0.4, 3.8, 0.25, 9.0
RATE = F_NGHI / (T_SLIP - T0); V_PX = 24.0

def f_at(t):
    if t < T0: return 0.0
    if t < T_SLIP: return RATE * (t - T0)
    if t < T_SLIP + T_DROP: return lerp(F_NGHI, F_TRUOT, ease((t - T_SLIP) / T_DROP))
    return F_TRUOT
def x_at(t): return BX0 + (max(0.0, min(t, T_END) - T_SLIP) * V_PX if t > T_SLIP else 0.0)
def f_show(t):
    """So hien o o doc: lam tron 0,1 N khi dang tang; dung 0,7 roi 0,6 (hang kho)."""
    if t < T_SLIP: return round(f_at(t) * 10) / 10
    return F_NGHI if t < T_SLIP + T_DROP else F_TRUOT

GX0, GX1, GYB, GYT = 210, 990, 1450, 950
def gx(t): return GX0 + (t - T0) / (T_END - T0) * (GX1 - GX0 - 30)
def gy(f): return GYB - f / 1.0 * (GYB - GYT)

def graph(d, t_now, lab=True, hl=None, top=860):
    card(d, (40, top, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GYB), (GX1 + 20, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 30)], fill=NAVY, width=5)
    text(d, (GX0 + 20, GYT - 50), "F (N): số chỉ lực kế", 55, INK, anchor="lm")
    text(d, (GX1 + 20, GYB + 52), "t: thời gian", 55, INK, anchor="rm")
    for v in (0, 0.5, 1.0):
        d.line([(GX0 - 12, gy(v)), (GX0, gy(v))], fill=NAVY, width=4)
        text(d, (GX0 - 20, gy(v)), "0" if v == 0 else (vn(v) if v < 1 else "1"), 55, INK, anchor="rm")
    if hl: hl(d)
    pts = []; tt = T0
    while tt <= min(t_now, T_END) + 1e-9:
        pts.append((gx(tt), gy(f_at(tt)))); tt += 0.02
    if len(pts) > 1: d.line(pts, fill=RED, width=8, joint="curve")
    if not lab: return
    k1 = appear(t_now, T_SLIP, 0.3)
    if k1 > 0:
        x, y = gx(T_SLIP), gy(F_NGHI); dot(d, x, y, 13, ORANGE, WHITE)
        text(d, (x + 26, y - 50), "0,7 N: bật đi", 55, DORANGE, anchor="lm", alpha=k1)
    k2 = appear(t_now, T_SLIP + 2.6, 0.3)
    if k2 > 0:
        text(d, (GX1, gy(F_TRUOT) + 60), "0,6 N: trượt đều", 55, DGREEN, anchor="rm", alpha=k2)

def s_do(img, d, t, sc):
    rig(d, x_at(t), f_at(t))
    readout(d, f_show(t))
    graph(d, t)

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        if x_at(t) > BX0 + 1e-9 and t < T_SLIP: bad.append((round(t, 2), "hop chay som"))
        if t < T_SLIP and f_at(t) > F_NGHI + 1e-9: bad.append((round(t, 2), "vuot nghi max"))
        if abs(f_show(t) - f_at(t)) > 0.051 and not (T_SLIP <= t < T_SLIP + T_DROP): bad.append((round(t, 2), "o so != kim"))
        t += 0.05
    if T_END > sc["T"] - 0.3: bad.append("do thi chua ve xong")
    if abs(sc["M"][1] - T_SLIP) > 0.05: bad.append("phu de bat di lech")
    xr = x_at(T_END) + BW + ROPE + 20 + BODY + 30 + 40 + 28
    if 65 + 0.88 * xr > 1050: bad.append(("tay sat mep", xr))
    return bad

# ---------------- canh 3: Them gia trong (bang 4 lan do) ----------------
TX = (170, 500, 860)
def table(d, nrow, y0=700, a_h=1.0):
    card(d, (40, y0, 1040, y0 + 560), fill=WHITE, outline=NAVY, w=4)
    for x, (s1, s2), c in zip(TX, (("m", "(kg)"), ("nghỉ cực đại", "(N)"), ("trượt", "(N)")), (INK, DORANGE, DGREEN)):
        text(d, (x, y0 + 45), s1, 55, c, alpha=a_h); text(d, (x, y0 + 102), s2, 55, c, alpha=a_h)
    d.line([(60, y0 + 140), (1020, y0 + 140)], fill=LIGHT, width=4)
    for i in range(nrow):
        m, a, b = ROWS[i]; y = y0 + 195 + i * 98
        for x, s, c in zip(TX, (vn(m, 2), vn(a), vn(b)), (INK, DORANGE, DGREEN)):
            text(d, (x, y), s, 60, c)

def s_bang(img, d, t, sc):
    M = sc["M"]
    rows = 1 + sum(1 for i in range(3) if t >= M[i] + 0.3)
    card(d, (40, 270, 1040, 650), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([40, 560, 1040, 600], fill=WOOD)
    box(d, 300, 560, vn(ROWS[rows - 1][0], 2) + " kg", n_wt=rows - 1)
    table(d, rows)
    text(d, (W / 2, 1330), "m: tổng khối lượng", 55, NOTE)
    kr = appear(t, M[3] + 0.2, 0.45)
    if kr > 0:
        y0 = 1270 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pill(d, W / 2, y0 + 60, "RÚT RA", GREEN, kr)
        text(d, (W / 2, y0 + 160), "Trượt: tỉ lệ với áp lực.", 58, DGREEN, alpha=kr)
        text(d, (W / 2, y0 + 240), "Nghỉ cực đại > trượt.", 58, DGREEN, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3
    kv = appear(t, M[1], 0.4)
    def hl(d):
        if kv <= 0: return
        pts = [(gx(tt), gy(f_at(tt))) for tt in [T0 + i * 0.02 for i in range(int((T_SLIP - T0) / 0.02) + 1)]]
        d.line(pts, fill=A(TEAL, kv), width=22, joint="curve")
    graph(d, T_END, lab=False, hl=hl)
    x, y = gx(T_SLIP), gy(F_NGHI); dot(d, x, y, 13, ORANGE, WHITE)
    text(d, (x + 26, y - 50), "0,7 N", 55, DORANGE, anchor="lm")
    if kv > 0:
        text(d, (gx(T0 + 1.2) + 40, gy(0.25) + 20), "ma sát = lực kéo", 55, TEAL, anchor="lm", alpha=kv)
    if a1 > 0:
        card(d, (40, 280, 1040, 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 350, "BẪY", DRED, a1)
        q = "“Ma sát nghỉ luôn là 0,7 N”"
        ks = clamp((t - M[0] - 1.2) / 0.4); f = F(58); lw = tw(d, q, f); yy = 470
        text(d, (W / 2, yy), q, 58, mix(RED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    if k3 > 0:
        card(d, (40, 280, 1040, 640), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 350, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 520), "Đổi diện tích, tốc độ?", 58, INK, alpha=k3)

# ---------------- canh 5: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 375, "THỬ NGHĨ", ORANGE, k)
    d.rectangle([90, 760, 990, 790], fill=A(WOOD, k))
    box(d, 200, 760, "1,00 kg", n_wt=4, a=k)
    arrow(d, (450, 700), (620, 700), A(RED, k), w=8, head=24)
    text(d, (650, 700), "?", 72, RED, anchor="lm", alpha=k)
    text(d, (W / 2, 890), "Cùng mặt bàn, tổng 1,00 kg.", 60, INK, alpha=k)
    text(d, (W / 2, 985), "Kéo bao nhiêu N", 60, INK, alpha=k)
    text(d, (W / 2, 1075), "thì hộp vừa bật đi?", 60, DORANGE, alpha=k)
    seg_bar(d, 1170, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, bg, b, e = sc["hook"], sc["do"], sc["bang"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + T0, "tap"),
             (do["t0"] + T_SLIP, "ding")] + [(bg["t0"] + bg["M"][i] + 0.3, "tap") for i in range(3)]
            + [(bg["t0"] + bg["M"][3] + 0.2, "tap"), (b["t0"] + b["M"][0] + 1.2, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-luc-ma-sat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực ma sát · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kéo hộp gỗ bằng lực kế", draw=s_hook, tail=0.2, caps=[
   ("Kéo nhẹ, hộp vẫn yên.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Kéo tăng dần", draw=s_do, tail=0.3, caps=[
   ("Hộp yên: số chỉ tăng dần.", 3.4),
   ("Hộp bật đi.", 3.0),
   ("Đáp án: số chỉ tụt xuống.", 3.6)]),
 dict(key="bang", title="Thêm gia trọng, đo lại", draw=s_bang, tail=0.3, caps=[
   ("Thêm từng khối.", 2.6),
   ("Ghi hai số chỉ.", 2.6),
   ("Tổng 0,80 kg.", 2.6),
   ("Áp lực = trọng lượng hộp.", 3.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.4),
   ("Đoạn hộp yên.", 3.4),
   ("Chưa nói được.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.4)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
