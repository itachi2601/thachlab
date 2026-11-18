# Clip: tn-l10-dl2-newton-01 - Gia toc cua xe theo luc keo, khoi luong khong doi (lo 7, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dl2-newton-01.json:
#   tham_so M = 0,50 kg, s = 0,50 m ; so_lieu_mau (F N, t s, a m/s2): 0,10 2,29 0,19 ; 0,20 1,56 0,41 ; 0,30 1,31 0,58 ;
#   0,40 1,11 0,81. a = 2s/t^2 tinh lai tu t da lam tron (_kiem_so()). Cot F/a KHONG hien (hop "Doc so lieu" ngay sau
#   bai bat HS tu tinh F/a va chon lan do kem tin cay nhat -> clip khong noi sai so, khong hien F/a).
# Xe chay THOI GIAN THAT: x = s.(tau/t)^2, toi cong 2 dung luc dong ho dung o t cua hang (_kiem_dong_bo()).
# Du doan (K10: chi cau hoi + hinh, khung ben canh co lua chon): xe 0,50 kg, F tang 0,10 -> 0,40 N, do thi a theo F?
#   A. Duong thang qua goc toa do (DUNG) ; B. Duong nam ngang ; C. Duong cong di len, cang luc cang doc ; D. Duong thang di xuong.
# KHONG tra loi san: Cau 1 (F 0,20 -> 0,60 N, a?) -> khong noi "gap ba", khong dung bay "tang them 0,40" ;
#   Cau 2 (m gap 3) -> chua noi duoc chi hoi, khong tra loi.
# Bay = hien_tuong_hay_sai (them 18/11) "F gap doi thi t giam mot nua" (goi_y_mo_phong: t giam can 2 lan): 0,10 -> 0,20 N:
#   a 0,19 -> 0,41 (gap doi) nhung t 2,29 -> 1,56 s (chua giam mot nua).
# Cau chot (ghi trong ghi_chu kho): xe 0,50 kg, F = 0,25 N (tham_so F 0,05-0,6) -> a = 0,50 m/s2,
#   t = can(2.0,50/0,50) = 1,41 s. So 0,25 N / 1,41 s chua tung hien tren man.
from engine import *

ROWS = [(0.10, 2.29, 0.19), (0.20, 1.56, 0.41), (0.30, 1.31, 0.58), (0.40, 1.11, 0.81)]   # so_lieu_mau
M_XE, S_M = 0.50, 0.50
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    return [r for r in ROWS if abs(round(2 * S_M / r[1] ** 2, 2) - r[2]) > 0.005]
assert not _kiem_so()
SLOPE = sum(f * a for f, _, a in ROWS) / sum(f * f for f, _, _ in ROWS)   # duong qua goc, binh phuong toi thieu (~2,0)

DRED = (185, 28, 28); NOTE = (60, 64, 84); TRACK = (176, 184, 200); TRACK_D = (110, 118, 140)
SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100); WEIGHT = (90, 98, 120)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
TY = 400                      # mat mang dem khi
PX = 1000                     # m/px ; 0,50 m = 360 px
PPM = 720
G1, G2 = 330, 330 + S_M * PPM  # cong 1, cong 2 (x)
CW, CH = 170, 64              # xe
PUX, PUY, PUR = 960, TY + 6, 26
MY0 = 430                     # dinh qua nang khi xe o cong 1

def track(d):
    d.rectangle([40, TY, 930, TY + 34], fill=TRACK); d.line([(40, TY), (930, TY)], fill=TRACK_D, width=4)
    for x in range(70, 920, 44): dot(d, x, TY + 17, 4, TRACK_D)
    d.rectangle([60, TY + 34, 84, 560], fill=TRACK_D); d.rectangle([880, TY + 34, 904, 560], fill=TRACK_D)
    d.line([(40, 560), (1040, 560)], fill=INK, width=4)
    d.line([(930, TY + 17), (PUX, PUY)], fill=TRACK_D, width=8)                      # gia ong rong roc
    d.ellipse([PUX - PUR, PUY - PUR, PUX + PUR, PUY + PUR], fill=WHITE, outline=NAVY, width=5); dot(d, PUX, PUY, 6, NAVY)

def gates(d, lab=True):
    for x, s in ((G1, "cổng 1"), (G2, "cổng 2")):
        d.rectangle([x - 8, TY - 120, x + 8, TY], fill=PURPLE)
        d.line([(x, TY - 105), (x, TY - 20)], fill=A(RED, 0.5), width=3)
        if lab: text(d, (x, TY - 150), s, 40, PURPLE)
    yb = TY + 82
    d.line([(G1, yb), (G2, yb)], fill=NAVY, width=3)
    for x in (G1, G2): d.line([(x, yb - 14), (x, yb + 14)], fill=NAVY, width=3)
    card(d, ((G1 + G2) / 2 - 80, yb - 26, (G1 + G2) / 2 + 80, yb + 26), fill=BG, r=10)
    text(d, ((G1 + G2) / 2, yb), "0,50 m", 40, NAVY)

def cart(d, xf, nmass):
    """xf: mep truoc xe (phia rong roc). Qua nang treo ha xuong dung bang quang duong xe da di."""
    x0 = xf - CW
    d.polygon([(x0, TY), (xf, TY), (xf - 18, TY - CH), (x0 + 18, TY - CH)], fill=BLUE)
    d.line([(x0, TY), (xf, TY), (xf - 18, TY - CH), (x0 + 18, TY - CH), (x0, TY)], fill=NAVY, width=4)
    text(d, (xf - CW / 2, TY - CH / 2), "0,50 kg", 40, WHITE)
    d.rectangle([xf - 6, TY - 52, xf + 26, TY - 20], fill=ORANGE, outline=NAVY, width=3)     # cam bien luc
    hx, hy = xf + 26, TY - 36
    d.line([(hx, hy), (PUX, PUY - PUR)], fill=NAVY, width=3)
    drop = xf - G1
    my = MY0 + drop; mh = 26 + 12 * nmass
    d.line([(PUX + PUR, PUY), (PUX + PUR, my)], fill=NAVY, width=3)
    d.rectangle([PUX + PUR - 26, my, PUX + PUR + 26, my + mh], fill=WEIGHT, outline=NAVY, width=3)

def readout(d, x0, x1, label, reading, flash=0.0, y=650):
    card(d, (x0, y, x1, y + 130), fill=BODY, r=20)
    card(d, (x0 + 16, y + 14, x1 - 16, y + 78), fill=mix(SCREEN, (255, 237, 160), flash), r=10)
    text(d, ((x0 + x1) / 2, y + 46), reading, 44, SCR_INK)
    text(d, ((x0 + x1) / 2, y + 104), label, 40, WHITE)

def readouts(d, F_s, t_s, a_s, flash=0.0):
    readout(d, 40, 330, "lực kéo F", F_s)
    readout(d, 345, 635, "thời gian t", t_s)
    readout(d, 650, 920, "a = 2s/t²", a_s, flash)

# ---------------- do thi a theo F (truc co dinh) ----------------
GX0, GX1, GY0, GY1 = 210, 950, 1500, 1010      # F 0-0,5 N ; a 0-1,0 m/s2
def gx(f): return GX0 + f / 0.5 * (GX1 - GX0)
def gy(a): return GY0 - a / 1.0 * (GY0 - GY1)

def axes(d, y_top=880):
    card(d, (40, y_top, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    for a in (0.2, 0.4, 0.6, 0.8, 1.0):
        d.line([(GX0, gy(a)), (GX1, gy(a))], fill=LIGHT, width=3)
        text(d, (GX0 - 18, gy(a)), vn(a, 1), 40, NOTE, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 36), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 36, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 22, GY1 - 50), "a (m/s²)", 40, INK, anchor="lm")
    text(d, (1020, GY0 - 44), "F (N)", 40, INK, anchor="rm")
    text(d, (GX0 - 18, GY0 + 6), "0", 40, NOTE, anchor="rm")
    for f in (0.1, 0.2, 0.3, 0.4, 0.5):
        d.line([(gx(f), GY0), (gx(f), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(f), GY0 + 44), vn(f, 1), 40, NOTE)

def pts(d, n, pop=None, col=BLUE):
    for j in range(n):
        r = 15 if (pop is None or j < n - 1) else 15 + 10 * (1 - pop)
        dot(d, gx(ROWS[j][0]), gy(ROWS[j][2]), r, col, outline=WHITE)

def line_origin(d, k, col=GREEN, w=6):
    if k <= 0: return
    f1 = 0.45 * k
    d.line([(gx(0), gy(0)), (gx(f1), gy(SLOPE * f1))], fill=A(col, 0.85), width=w)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    track(d); gates(d); cart(d, G1, 1); readouts(d, "0,10 N", "0,00 s", "?")
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Xe 0,50 kg. Tăng lực kéo F", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "từ 0,10 N lên 0,40 N.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "Đồ thị a theo F", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 420), "có dạng nào?", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 515), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 580, 940, y0 + 594], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 580, 140 + 800 * (1 - p), y0 + 594], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (4 lan, xe chay thoi gian that) ----------------
GAP, BACK = 0.6, 0.45
def run_starts():
    ts = [0.6]
    for f, tk, a in ROWS[:-1]: ts.append(ts[-1] + tk + GAP + BACK + 0.15)
    return ts
RS = run_starts()

def do_state(t):
    """-> (k lan dang chieu, mep truoc xe, dong ho (s), so diem da cham, xe dang ve cho cu)."""
    k = max(0, sum(1 for r in RS if t >= r) - 1)
    if t < RS[0]: return 0, G1, 0.0, 0
    tau = t - RS[k]; tk = ROWS[k][1]
    if tau < tk: return k, G1 + S_M * PPM * (tau / tk) ** 2, tau, k
    n = k + 1
    if k < 3 and tau > tk + GAP:                                   # day xe ve cong 1 cho lan sau
        x = clamp((tau - tk - GAP) / BACK)
        return k, lerp(G1 + S_M * PPM, G1, ease(x)), tk, n
    return k, G1 + S_M * PPM, tk, n

def s_do(img, d, t, sc):
    k, xf, clk, n = do_state(t)
    kshow = min(3, k + 1) if (k < 3 and t - RS[k] > ROWS[k][1] + GAP + BACK) else k   # qua nang moi treo khi xe da ve
    track(d); gates(d); cart(d, xf, kshow + 1)
    done = n > k
    flash = 1 - clamp((t - RS[k] - ROWS[k][1]) / 0.6) if done else 0
    if kshow != k: readouts(d, vn(ROWS[kshow][0]) + " N", "0,00 s", "—")
    else: readouts(d, vn(ROWS[k][0]) + " N", vn(clk) + " s", vn(ROWS[k][2]) if done else "—", flash)
    axes(d)
    pop = clamp((t - RS[k] - ROWS[k][1]) / 0.3) if done else None
    pts(d, n, pop if done else None)

def _kiem_dong_bo():
    """Moi 0,05 s: xe toi cong 2 dung luc dong ho = t cua hang ; diem moi + a hien cung luc ; truoc do khong co diem."""
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

# ---------------- canh 3: Dap an + Rut ra ----------------
def ftable(d, y, a=1.0):
    card(d, (40, y, 1040, y + 450), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (250, 540, 830)
    for x, s in zip(xs, ("F (N)", "t (s)", "a (m/s²)")): text(d, (x, y + 60), s, 44, INK, alpha=a)
    d.line([(70, y + 106), (1010, y + 106)], fill=A(LIGHT, a), width=4)
    for i, (f, tk, ak) in enumerate(ROWS):
        yy = y + 160 + i * 78
        text(d, (xs[0], yy), vn(f), 46, INK, alpha=a); text(d, (xs[1], yy), vn(tk), 46, INK, alpha=a)
        text(d, (xs[2], yy), vn(ak), 46, BLUE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Đường thẳng qua gốc toạ độ"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 338), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 304), lab, 42, WHITE, alpha=ka)
    axes(d); line_origin(d, appear(t, M[0] + 0.2, 1.0)); pts(d, 4)
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr < 1: ftable(d, 380, appear(t, 0.3, 0.4) * (1 - kr))
    if kr > 0:
        y0 = 400 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(GREEN, kr), r=32)
        text(d, (W / 2, y0 + 60), "RÚT RA", 40, WHITE, alpha=kr)
        text(d, (W / 2, y0 + 190), "a tỉ lệ thuận với F", 54, INK, alpha=kr)
        text(d, (W / 2, y0 + 300), "(khối lượng xe giữ nguyên)", 44, (21, 110, 55), alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d); line_origin(d, 1.0); pts(d, 4)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 300
    if a1 > 0:
        for j in (0, 1):                                        # khoanh hai diem dang so
            dot(d, gx(ROWS[j][0]), gy(ROWS[j][2]), 26, None, outline=A(ORANGE, a1))
        card(d, (40, y, 1040, y + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“F gấp đôi thì t giảm một nửa”"
        ks = clamp((t - 2.4) / 0.4); f = F(48); lw = tw(d, q, f); yy = y + 175
        text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 2, yy - 46), "✗", 48, DRED, alpha=a1 * ks)
        ke = a1 * appear(t, 2.8, 0.4)
        text(d, (W / 2, y + 285), "F: 0,10 → 0,20 N", 46, INK, alpha=ke)
        text(d, (W / 2, y + 365), "a: 0,19 → 0,41 m/s² (gấp đôi)", 46, BLUE, alpha=ke)
        text(d, (W / 2, y + 445), "t: 2,29 → 1,56 s (giảm chưa tới nửa)", 46, DRED, alpha=a1 * appear(t, 3.3, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 460), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 230), "Đổi khối lượng xe thì a ra sao?", 46, INK, alpha=kk)
        text(d, (W / 2, y + 350), "→ thí nghiệm tiếp theo", 44, NAVY, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: F = 0,25 N, xe 0,50 kg, di 0,50 m -> t ? ; goi y tre 3 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 400), "Giữ m: a tỉ lệ thuận với F", 52, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Xe 0,50 kg, lực kéo 0,25 N.", "Đi hết 0,50 m giữa hai cổng", "mất bao lâu?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1160), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1270), "Xe thả từ nghỉ ở cổng 1", 48, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + r, "tap") for r in RS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-dl2-newton-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật 2 Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Gia tốc theo lực kéo", draw=s_hook, tail=0.3, caps=[
   ("Xe chạy trên máng đệm khí.", 3.4),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.3, caps=[
   ("Thả xe từ cổng 1, đo thời gian t.", 4.6),
   ("Treo nặng dần, chấm điểm (F, a).", 5.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Bốn điểm gần một đường thẳng.", 3.4),
   ("Điều đồ thị cho thấy.", 3.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.2),
   ("Câu còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
