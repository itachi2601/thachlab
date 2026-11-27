# Clip: tn-l10-dl2-newton-01 - Gia toc cua xe theo luc keo, khoi luong khong doi (lo 7, 18/11/2026; dung lai 27/11/2026
# theo viec 4: cong --do-chu, chu >= 55 px khi ve, K10, Bay hinh tu giai thich, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dl2-newton-01.json (_kiem_so() doi chieu):
#   tham_so M = 0,50 kg, s = 0,50 m ; so_lieu_mau (F N, t s, a m/s2, F/a kg): 0,10 2,29 0,19 | 0,20 1,56 0,41 |
#   0,30 1,31 0,58 | 0,40 1,11 0,81. Cot F/a KHONG hien (hop "Doc so lieu" bat HS tu tinh F/a, chon lan do kem tin cay).
# Xe chay thoi gian that: x = s.(tau/t)^2; dong ho chi hien "…" khi xe dang chay, hien t khi xe qua cong 2
#   (khong de so 1,41 s cua cau chot thoang qua tren dong ho chay).
# Du doan (K10: khong nut A-D, khung web co lua chon): xe 0,50 kg, F 0,10 -> 0,40 N, do thi a theo F dang nao?
#   -> duong thang qua goc toa do. Khong trung quiz mo bai (so 2 nguoi tren san bang), Cau 1 (F 0,20 -> 0,60 N), Cau 2 (m gap 3).
# Bay = hien_tuong_hay_sai "F gap doi thi t giam mot nua": hai thanh thoi gian 2,29 s / 1,56 s ve cung thang,
#   vach "mot nua" o 1,145 s -> thanh 1,56 s dai qua vach (hinh tu giai thich). Khong lap cap so 0,10 -> 0,40 cua Du doan.
# Chua noi duoc: doi khoi luong xe (thi nghiem 02).
# Cau chot (ghi_chu kho): xe 0,50 kg, F = 0,25 N -> a = 0,50 m/s2, t = can(2.0,50/0,50) = 1,41 s (2 buoc, chua hien).
from engine import *

ROWS = [(0.10, 2.29, 0.19), (0.20, 1.56, 0.41), (0.30, 1.31, 0.58), (0.40, 1.11, 0.81)]   # so_lieu_mau
M_XE, S_M = 0.50, 0.50
CHOT = (0.25, 0.50, 1.41)                                                                 # ghi_chu kho
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-dl2-newton-01.json")))
    hang = [tuple(r[:3]) for r in k["so_lieu_mau"]["hang"]]
    assert all(any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang) for r in ROWS)
    assert all(abs(round(2 * S_M / r[1] ** 2, 2) - r[2]) <= 0.005 for r in ROWS)
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["M"]["gia_tri"] == M_XE and tp["s"]["gia_tri"] == S_M and tp["F"]["min"] <= CHOT[0] <= tp["F"]["max"]
    assert abs(CHOT[0] / M_XE - CHOT[1]) < 1e-9 and abs(math.sqrt(2 * S_M / CHOT[1]) - CHOT[2]) < 0.005
    assert "0,25 N" in k["so_lieu_mau"]["ghi_chu"] and "1,41 s" in k["so_lieu_mau"]["ghi_chu"]
_kiem_so()
SLOPE = sum(f * a for f, _, a in ROWS) / sum(f * f for f, _, _ in ROWS)   # duong qua goc, binh phuong toi thieu (~2,0)

DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
TRACK = (176, 184, 200); TRACK_D = (110, 118, 140); WEIGHT = (90, 98, 120)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- dung cu (khung nguon 1080x1920; mp4 x = 65 + 0,88x) ----------------
TY = 470                       # mat mang dem khi
PPM = 720                      # px/m ; 0,50 m = 360 px
G1, G2 = 360, 360 + S_M * PPM  # cong 1, cong 2
CW, CH = 230, 80
PUX, PUY, PUR = 985, TY + 6, 28
MY0 = 500

def track(d):
    d.rectangle([40, TY, 955, TY + 34], fill=TRACK); d.line([(40, TY), (955, TY)], fill=TRACK_D, width=4)
    for x in range(70, 940, 44): dot(d, x, TY + 17, 4, TRACK_D)
    d.rectangle([60, TY + 34, 84, 610], fill=TRACK_D); d.rectangle([880, TY + 34, 904, 610], fill=TRACK_D)
    d.line([(40, 610), (1040, 610)], fill=INK, width=4)
    d.line([(955, TY + 17), (PUX, PUY)], fill=TRACK_D, width=8)
    d.ellipse([PUX - PUR, PUY - PUR, PUX + PUR, PUY + PUR], fill=WHITE, outline=NAVY, width=5); dot(d, PUX, PUY, 6, NAVY)

def gates(d):
    for x, s in ((G1, "cổng 1"), (G2, "cổng 2")):
        d.rectangle([x - 9, TY - 150, x + 9, TY], fill=PURPLE)
        d.line([(x, TY - 135), (x, TY - 20)], fill=A(RED, 0.5), width=3)
        text(d, (x, TY - 190), s, 58, PURPLE)
    yb = TY + 95
    d.line([(G1, yb), (G2, yb)], fill=NAVY, width=4)
    for x in (G1, G2): d.line([(x, yb - 16), (x, yb + 16)], fill=NAVY, width=4)
    card(d, ((G1 + G2) / 2 - 100, yb - 36, (G1 + G2) / 2 + 100, yb + 36), fill=BG, r=12)
    text(d, ((G1 + G2) / 2, yb), "0,50 m", 58, NAVY)

def cart(d, xf, nmass, hang=1.0):
    """xf: mep truoc xe. Qua nang treo ha xuong bang quang duong xe da di; hang < 1: qua nang dang ha vao moc."""
    x0 = xf - CW
    d.polygon([(x0, TY), (xf, TY), (xf - 20, TY - CH), (x0 + 20, TY - CH)], fill=BLUE)
    d.line([(x0, TY), (xf, TY), (xf - 20, TY - CH), (x0 + 20, TY - CH), (x0, TY)], fill=NAVY, width=4)
    text(d, (xf - CW / 2, TY - CH / 2), "0,50 kg", 56, WHITE)
    d.rectangle([xf - 6, TY - 60, xf + 26, TY - 24], fill=ORANGE, outline=NAVY, width=3)     # cam bien luc
    hx, hy = xf + 26, TY - 42
    d.line([(hx, hy), (PUX, PUY - PUR)], fill=NAVY, width=3)
    my = MY0 + (xf - G1) * 0.3 - (1 - hang) * 60; mh = 30 + 12 * nmass
    d.line([(PUX + PUR, PUY), (PUX + PUR, my)], fill=NAVY, width=3)
    d.rectangle([PUX + PUR - 28, my, PUX + PUR + 22, my + mh], fill=WEIGHT, outline=NAVY, width=3)

def readouts(d, F_s, t_s, a_s, flash=0.0, y=650):
    for x0, x1, s in ((40, 520, F_s), (560, 1040, t_s)):
        card(d, (x0, y, x1, y + 100), fill=WHITE, outline=NAVY, w=4, r=20)
        text(d, ((x0 + x1) / 2, y + 50), s, 60, INK)
    card(d, (40, y + 120, 1040, y + 215), fill=mix(WHITE, (255, 237, 160), flash), outline=BLUE, w=4, r=20)
    text(d, (W / 2, y + 167), "a = 2s/t² = " + a_s, 60, BLUE)

# ---------------- do thi a theo F (truc co dinh) ----------------
GX0, GX1, GY0, GY1 = 230, 940, 1560, 1050      # F 0-0,5 N ; a 0-1,0 m/s2
def gx(f): return GX0 + f / 0.5 * (GX1 - GX0)
def gy(a): return GY0 - a / 1.0 * (GY0 - GY1)

def axes(d, y_top=900):
    card(d, (40, y_top, 1040, 1650), fill=WHITE, outline=LIGHT, w=3)
    for a in (0.2, 0.4, 0.6, 0.8, 1.0):
        d.line([(GX0, gy(a)), (GX1, gy(a))], fill=LIGHT, width=3)
        text(d, (GX0 - 18, gy(a)), vn(a, 1), 56, NAVY, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    text(d, (GX0 + 24, GY1 - 70), "a (m/s²)", 56, INK, anchor="lm")
    text(d, (1020, GY0 - 50), "F (N)", 56, INK, anchor="rm")
    text(d, (GX0 - 18, GY0 + 10), "0", 56, NAVY, anchor="rm")
    for f in (0.1, 0.2, 0.3, 0.4, 0.5):
        d.line([(gx(f), GY0), (gx(f), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(f), GY0 + 50), vn(f, 1), 56, NAVY)

def pts(d, n, pop=None, col=BLUE):
    for j in range(n):
        r = 16 if (pop is None or j < n - 1) else 16 + 12 * (1 - pop)
        dot(d, gx(ROWS[j][0]), gy(ROWS[j][2]), r, col, outline=WHITE)

def line_origin(d, k, col=GREEN, w=7):
    if k <= 0: return
    f1 = 0.47 * k
    d.line([(gx(0), gy(0)), (gx(f1), gy(SLOPE * f1))], fill=A(col, 0.85), width=w)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    track(d); gates(d); cart(d, G1, 1, hang=ease((t - 0.5) / 1.0))
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 760 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Xe giữ 0,50 kg.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "F tăng 0,10 → 0,40 N.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 385), "Đồ thị a theo F", 64, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 465), "có dạng nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 535, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 lan, xe chay thoi gian that) ----------------
GAP, BACK = 0.45, 0.4
def run_starts():
    ts = [0.6]
    for f, tk, a in ROWS[:-1]: ts.append(ts[-1] + tk + GAP + BACK + 0.15)
    return ts
RS = run_starts()

def do_state(t):
    """-> (k lan dang chieu, mep truoc xe, dong ho (s), so diem da cham)."""
    k = max(0, sum(1 for r in RS if t >= r) - 1)
    if t < RS[0]: return 0, G1, 0.0, 0
    tau = t - RS[k]; tk = ROWS[k][1]
    if tau < tk: return k, G1 + S_M * PPM * (tau / tk) ** 2, tau, k
    n = k + 1
    if k < 3 and tau > tk + GAP:
        x = clamp((tau - tk - GAP) / BACK)
        return k, lerp(G1 + S_M * PPM, G1, ease(x)), tk, n
    return k, G1 + S_M * PPM, tk, n

def s_do(img, d, t, sc):
    k, xf, clk, n = do_state(t)
    kshow = min(3, k + 1) if (k < 3 and t - RS[k] > ROWS[k][1] + GAP + BACK) else k
    track(d); gates(d); cart(d, xf, kshow + 1)
    done = n > k
    flash = 1 - clamp((t - RS[k] - ROWS[k][1]) / 0.6) if done else 0
    if kshow != k: readouts(d, "F = " + vn(ROWS[kshow][0]) + " N", "t = …", "…")
    elif not done: readouts(d, "F = " + vn(ROWS[k][0]) + " N", "t = …", "…")
    else: readouts(d, "F = " + vn(ROWS[k][0]) + " N", "t = " + vn(clk) + " s", vn(ROWS[k][2]) + " m/s²", flash)
    axes(d)
    pop = clamp((t - RS[k] - ROWS[k][1]) / 0.3) if done else None
    pts(d, n, pop)

def _kiem_dong_bo():
    """Moi 0,05 s: xe toi cong 2 dung luc t cua hang ; diem moi + a hien cung luc ; dong ho khong chay so."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, xf, clk, n = do_state(t)
        tau = t - RS[k]
        if t >= RS[0] and tau < ROWS[k][1] and (xf > G2 + 1e-6 or n != k): bad.append(("chay", round(t, 2)))
        if t >= RS[0] and tau >= ROWS[k][1] and (abs(clk - ROWS[k][1]) > 1e-9 or n != k + 1): bad.append(("dung", round(t, 2)))
        t += 0.05
    if RS[-1] + ROWS[-1][1] + 0.8 > sc["T"]: bad.append("lan cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Ket qua + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    card(d, (40, 250, 1040, 400), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5, r=24)
    text(d, (W / 2, 325), "Đường thẳng qua gốc toạ độ", 62, DGREEN, alpha=ka)
    axes(d); line_origin(d, appear(t, M[0] + 0.2, 1.2)); pts(d, 4)
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr > 0:
        y0 = 470 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        text(d, (W / 2, y0 + 150), "a tỉ lệ thuận với F", 66, DGREEN, alpha=kr)
        text(d, (W / 2, y0 + 270), "(m giữ nguyên)", 62, INK, alpha=kr)

# ---------------- canh 4: Bay - hai thanh thoi gian cung thang ----------------
TPX = 340                                     # px/s
BX0 = 110
def tbar(d, y, f, tk, col, k, lab_col=INK):
    text(d, (BX0, y - 62), "F = " + vn(f) + " N", 60, lab_col, anchor="lm", alpha=k)
    x1 = BX0 + TPX * tk * ease(k)
    d.rounded_rectangle([BX0, y, max(BX0 + 4, x1), y + 70], radius=14, fill=A(col, k))
    if k >= 1: text(d, (x1 - 16, y + 35), vn(tk) + " s", 58, WHITE, anchor="rm")

def s_bay(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.2, 0.45)
    card(d, (40, 230, 1040, 440), fill=A((254, 242, 242), ka), outline=A(DRED, ka), w=6, r=24)
    text(d, (W / 2, 295), "✗ Dễ tưởng: F gấp đôi", 62, DRED, alpha=ka)
    text(d, (W / 2, 375), "thì t còn một nửa", 62, DRED, alpha=ka)
    card(d, (40, 480, 1040, 1150), fill=WHITE, outline=LIGHT, w=3)
    kb = clamp((t - M[1]) / 0.8)
    tbar(d, 620, ROWS[0][0], ROWS[0][1], BLUE, clamp((t - M[1] + 0.2) / 0.8) if t >= M[1] - 0.2 else 0)
    tbar(d, 880, ROWS[1][0], ROWS[1][1], ORANGE, clamp((t - M[1] - 0.6) / 0.8) if t >= M[1] + 0.6 else 0)
    kh = appear(t, M[2] - 0.1, 0.45)                                       # vach "mot nua" cua 2,29 s
    if kh > 0:
        xh = BX0 + TPX * ROWS[0][1] / 2; y = 560
        while y < 1000: d.line([(xh, y), (xh, min(y + 22, 1000))], fill=A(PURPLE, kh), width=6); y += 38
        text(d, (xh, 1060), "một nửa 2,29 s", 58, PURPLE, alpha=kh)
        xe = BX0 + TPX * ROWS[1][1]
        arrow(d, (xh + 8, 980), (xe - 4, 980), A(DRED, kh), w=7, head=20)

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 230, 1040, 520), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 310), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 430), "Xe nặng hơn thì sao?", 64, INK)
    card(d, (40, 560, 1040, 1150), fill=WHITE, outline=LIGHT, w=3)
    y = 900; d.rectangle([80, y, 1000, y + 30], fill=TRACK)
    x0, x1 = 300, 640
    d.polygon([(x0, y), (x1, y), (x1 - 24, y - 110), (x0 + 24, y - 110)], fill=BLUE, outline=NAVY)
    for j in range(2):                                                    # gia trong roi xuong xe
        yy = lerp(620, y - 110 - 70 * (j + 1), ease((t - 0.4 - 1.2 * j) / 0.8))
        d.rectangle([400, yy, 540, yy + 70], fill=WEIGHT, outline=NAVY, width=4)
    text(d, (820, y - 160), "?", 120, PURPLE)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1500), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k1)
    y = 760
    d.rectangle([70, y, 1010, y + 30], fill=A(TRACK, k1))
    d.rectangle([G1 - 9, y - 150, G1 + 9, y], fill=A(PURPLE, k1)); d.rectangle([G2 - 9, y - 150, G2 + 9, y], fill=A(PURPLE, k1))
    d.polygon([(G1 - CW, y), (G1, y), (G1 - 20, y - CH), (G1 - CW + 20, y - CH)], fill=A(BLUE, k1))
    text(d, (G1 - CW / 2, y - CH / 2), "0,50 kg", 56, WHITE, alpha=k1)
    arrow(d, (G1 + 30, y - 40), (G1 + 230, y - 40), A(ORANGE, k1), w=9, head=26)
    text(d, (G1 + 130, y - 110), "0,25 N", 62, DORANGE, alpha=k1)
    yb = y + 95; d.line([(G1, yb), (G2, yb)], fill=A(NAVY, k1), width=4)
    for x in (G1, G2): d.line([(x, yb - 16), (x, yb + 16)], fill=A(NAVY, k1), width=4)
    text(d, ((G1 + G2) / 2, yb + 60), "0,50 m", 60, NAVY, alpha=k1)
    text(d, (W / 2, 1080), "Đi hết 0,50 m", 64, DORANGE, alpha=k1)
    text(d, (W / 2, 1165), "mất bao lâu?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + r + ROWS[i][1], "tap") for i, r in enumerate(RS)]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-dl2-newton-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật 2 Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Gia tốc theo lực kéo", draw=s_hook, tail=0.3, caps=[
   ("Xe chạy trên máng đệm khí.", 3.4),
   ("Dừng lại, tự đoán.", 5.3)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.9, caps=[
   ("Thả xe từ cổng 1, đo t.", 3.4),
   ("Treo nặng dần, đo lại.", 3.4),
   ("Chấm bốn điểm (F, a).", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Kẻ một đường qua bốn điểm.", 3.6),
   ("Điều đồ thị cho thấy.", 3.8)]),
 dict(key="bay", title="Bẫy: thời gian", draw=s_bay, tail=0.5, caps=[
   ("Lực gấp đôi thì sao?", 3.0),
   ("So hai thanh thời gian.", 3.0),
   ("Thời gian chỉ giảm √2 lần.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Ở đây m giữ nguyên.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Giữ m: a tỉ lệ thuận với F.", 5.3)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
