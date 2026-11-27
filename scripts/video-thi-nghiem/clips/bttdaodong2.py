# Clip: tn-l11-baitapdaodong-02 - Vat dao dong tu ve do thi li do - thoi gian len bang giay (9/11/2026, vi_du;
# dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu ve >= 55 px, Du doan K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapdaodong-02.json (_kiem_so() doi chieu):
#   so_lieu_mau: u 20 cm/s, h 6,0 cm, d 16,0 cm, A 3,0 cm, T 0,8 s ("so minh hoa tinh tu mo hinh").
#   mo_hinh: x = A cos(2 pi t / T), s = u t, h = 2A, d = u T. tham_so u: 5..40 cm/s.
# DOI CA Du doan (27/11): ca cu "dinh-day 6,0 cm -> A?" da co san dap so trong hop exp ngay tren video (A = 6,0/2 = 3,0).
#   Ca moi: giu qua nang, keo giay nhanh gap doi (u = 40 cm/s, tham_so max) -> hai dinh lien ke cach? -> d = u.T = 32 cm
#   (so tu suy theo mo hinh, ghi "so minh hoa"). Nhieu: 8 / 16 / 64 cm.
# Bay = hien_tuong_hay_sai[1]: dinh -> day ke nhau (8 cm) chi la nua chu ki.
# Chua noi duoc: giay keo tay co deu khong; ma sat dau but (gia_thiet).
# Thu nghi (= cau_chot khung web): A = 3,0 cm, T = 0,80 s -> toc do cuc dai cua qua nang = A.2pi/T ~ 23,6 ~ 24 cm/s
#   (buoc chua chieu: v_max = A omega). Nhieu: 20 cm/s (toc do giay), 7,5 (2A/T), 3,8 (A/T). So 24 KHONG hien.
from engine import *

A_CM, T_S, U1, U2 = 3.0, 0.8, 20.0, 40.0
H_CM, D_CM = 6.0, 16.0
PX = 20                                    # px / cm theo chieu giay
DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8)
BLOCK = (250, 204, 120); PAPER = (255, 255, 252); TRACE = (30, 64, 175); EMPTY = (148, 140, 128)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-baitapdaodong-02.json")))
    assert k["so_lieu_mau"]["hang"][0] == [U1, H_CM, D_CM, A_CM, T_S]
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["u"]["max"] == U2 and ts["u"]["min"] <= U1 <= ts["u"]["max"]
    assert abs(U1 * T_S - D_CM) < 1e-9 and abs(H_CM / 2 - A_CM) < 1e-9
_kiem_so()

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    fs = []
    for p in [p for p in re.split(r"(_\{[^}]*\})", s) if p]:
        if p.startswith("_{"): fs.append((p[2:-1], F(56), size * 0.3))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def dashed(d, p0, p1, col, w=4, on=14, off=10):
    L = math.dist(p0, p1)
    if L < 1: return
    n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p0[0], p1[0], a), lerp(p0[1], p1[1], a)), (lerp(p0[0], p1[0], b), lerp(p0[1], p1[1], b))], fill=col, width=w)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem lien khoi, tat lan luot tu PHAI sang TRAI; cao 76 px."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); wseg = 820 / n
    for i in range(n):
        x = 130 + i * wseg
        if i < on: card(d, (x, y, x + wseg - 14, y + 76), fill=A(col, a), r=16)
        else: card(d, (x, y, x + wseg - 14, y + 76), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def xcm(s): return A_CM * math.cos(2 * math.pi * s / T_S)          # li do (cm), chieu duong huong len

def bracket_h(d, x0, x1, y, col, alpha=1.0, w=6, k=1.0):
    x1 = x0 + (x1 - x0) * k
    d.line([(x0, y), (x1, y)], fill=A(col, alpha), width=w)
    for xx in (x0, x1): d.line([(xx, y - 16), (xx, y + 16)], fill=A(col, alpha), width=w)

def bracket_v(d, x, y0, y1, col, alpha=1.0, w=6):
    d.line([(x, y0), (x, y1)], fill=A(col, alpha), width=w)
    for yy in (y0, y1): d.line([(x - 16, yy), (x + 16, yy)], fill=A(col, alpha), width=w)

class Strip:
    """Bang giay: x0..x1, tam yc, py px/cm theo phuong dao dong; but o x = pen; giay chay sang trai toc do u (cm/s).
    trace(tau): net but sau tau giay (tau = thoi gian giay da chay)."""
    def __init__(s, x0, x1, y0, y1, py, pen, u):
        s.x0, s.x1, s.y0, s.y1, s.py, s.pen, s.u = x0, x1, y0, y1, py, pen, u; s.yc = (y0 + y1) / 2
    def y(s, xc): return s.yc - xc * s.py
    def xs(s, sig, tau): return s.pen - s.u * PX * (tau - sig)      # vi tri tren man cua diem but ve luc sig
    def draw(s, d, tau, alpha=1.0, col=TRACE):
        d.rectangle([s.x0, s.y0, s.x1, s.y1], fill=A(PAPER, alpha), outline=A(GRAY, alpha), width=3)
        dashed(d, (s.x0 + 8, s.yc), (s.x1 - 8, s.yc), A(GRAY, alpha), w=3)
        if tau <= 0: return
        pts = []
        for i in range(601):
            sig = tau * i / 600; x = s.xs(sig, tau)
            if s.x0 + 4 <= x <= s.x1 - 4: pts.append((x, s.y(xcm(sig))))
        if len(pts) > 1: d.line(pts, fill=A(col, alpha), width=7, joint="curve")

def coil(d, x, ya, yb, amp=24, n=10, col=NAVY, w=5):
    e = 14; pts = [(x, ya), (x, ya + e)]; L = (yb - e) - (ya + e)
    for i in range(1, 2 * n): pts.append((x + (amp if i % 2 else -amp), ya + e + L * i / (2 * n)))
    pts += [(x, yb - e), (x, yb)]
    d.line(pts, fill=col, width=w, joint="curve")

MX = 980
def hanger(d, st, x_cm):
    d.rectangle([1044, 250, 1064, st.y1 + 60], fill=GRAY, outline=NAVY, width=3)
    d.rectangle([930, 246, 1064, 268], fill=GRAY, outline=NAVY, width=3)
    yb = st.y(x_cm)
    coil(d, MX, 268, yb - 40)
    d.rounded_rectangle([MX - 44, yb - 40, MX + 44, yb + 40], radius=12, fill=BLOCK, outline=NAVY, width=4)
    d.polygon([(st.pen, yb), (MX - 44, yb - 12), (MX - 44, yb + 12)], fill=NAVY)
    dot(d, st.pen, yb, 7, TRACE)

def speed_arrow(d, x, y, u, col=DBLUE, a=1.0):
    arrow(d, (x + 150, y), (x - 30, y), A(col, a), w=7, head=24)
    text(d, (x + 170, y), f"{int(u)} cm/s", 60, col, anchor="lm", alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
SH = Strip(110, 930, 430, 790, 30, 900, U1)                # bang giay canh Du doan / Tien hanh
RUN_H = (0.3, 2.7, 3 * T_S)                                # ve 3 chu ki trong 2,4 s that
def s_hook(img, d, t, sc):
    M = sc["M"]
    tau = clamp((t - RUN_H[0]) / (RUN_H[1] - RUN_H[0])) * RUN_H[2]
    SH.draw(d, tau)
    hanger(d, SH, xcm(tau))
    speed_arrow(d, 300, 340, U1)
    kb = appear(t, 2.6, 0.4)                                # dinh o x = 260 va 580 (3T: dinh tai sig = 0,8 va 1,6)
    if kb > 0:
        xa, xb = SH.xs(0.8, RUN_H[2]), SH.xs(1.6, RUN_H[2]); yb = SH.y(A_CM) - 26
        bracket_h(d, xa, xb, yb, DGREEN, kb)
        text(d, ((xa + xb) / 2, yb - 46), "16 cm", 60, DGREEN, alpha=kb)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 100), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Kéo nhanh gấp đôi: 40 cm/s.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Hai đỉnh liền kề", 62, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 350), "cách bao xa?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh - keo 40 cm/s, chieu cham x2 ----------------
SD = Strip(110, 930, 430, 790, 30, 900, U2)
SLOW = 2.0
RUN_D = (0.3, 0.3 + 2 * T_S * SLOW, 2 * T_S)              # 2 chu ki, chieu cham x2 -> 3,2 s
def s_do(img, d, t, sc):
    M = sc["M"]
    tau = clamp((t - RUN_D[0]) / (RUN_D[1] - RUN_D[0])) * RUN_D[2]
    SD.draw(d, tau)
    hanger(d, SD, xcm(tau) if t >= RUN_D[0] else A_CM)
    speed_arrow(d, 300, 340, U2)
    card(d, (60, 880, 330, 966), fill=TEAL, r=40); text(d, (195, 923), "chậm ×2", 56, WHITE)
    kr = appear(t, M[1] + 0.2, 0.4)
    if kr > 0:                                              # thuoc + ngoac 32 cm (dinh o x = 260 va 900)
        xa, xb = SD.xs(0.0, RUN_D[2]), SD.xs(1.6, RUN_D[2]); yr = 1010
        d.rectangle([xa - 24, yr, xb + 24, yr + 44], fill=A((250, 240, 200), kr), outline=A(NAVY, kr), width=2)
        for c in range(0, 33):
            xx = xa + c * PX; L = 30 if c % 8 == 0 else 14
            d.line([(xx, yr), (xx, yr + L)], fill=A(NAVY, kr), width=3)
        for c in (0, 8, 16, 24, 32): text(d, (xa + c * PX, yr + 90), str(c), 58, INK, alpha=kr)
        for xx in (xa, xb): dashed(d, (xx, SD.y(A_CM) + 10), (xx, yr), A(DGREEN, kr), w=4)
        kg = clamp((t - M[1] - 0.6) / 1.0)
        if kg > 0:
            yb = SD.y(A_CM) - 26
            bracket_h(d, xa, xb, yb, DGREEN, 1.0, k=kg)
            if kg >= 1: text(d, ((xa + xb) / 2, yb - 46), "32 cm", 62, DGREEN)

# ---------------- canh 3: Ket qua + rut ra + chua noi duoc ----------------
S1 = Strip(300, 1030, 280, 560, 22, 0, U1); S2 = Strip(300, 1030, 600, 880, 22, 0, U2)
def peaks_strip(d, st, xp0, n, col=TRACE):
    """Ve net tinh: dinh dau o xp0, n chu ki (theo u cua bang)."""
    lam = st.u * PX * T_S
    st.draw(d, 0)
    pts = []
    for i in range(601):
        x = st.x0 + 4 + (st.x1 - st.x0 - 8) * i / 600
        pts.append((x, st.y(A_CM * math.cos(2 * math.pi * (x - xp0) / lam))))
    d.line(pts, fill=col, width=7, joint="curve")
    return lam

def s_dapan(img, d, t, sc):
    M = sc["M"]
    for st, u, lab in ((S1, U1, "16 cm"), (S2, U2, "32 cm")):
        lam = peaks_strip(d, st, 340, 1)
        text(d, (180, st.yc), f"{int(u)} cm/s", 58, DBLUE)
        yb = st.y(A_CM) - 24
        bracket_h(d, 340, 340 + lam, yb, DGREEN)
        text(d, (340 + lam / 2, yb - 42), lab, 58, DGREEN)
    k1 = appear(t, 2.6, 0.45)
    if k1 > 0:
        card(d, (60, 920, 1020, 1040), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=5)
        text(d, (W / 2, 980), "T = 16 : 20 = 32 : 40 = 0,80 s", 60, DGREEN, alpha=k1)
    k2 = appear(t, M[1] + 0.2, 0.45)
    if k2 > 0:                                              # bien do doc tren bang 2: dinh x = 980, day x = 660
        xv = 660; bracket_v(d, xv, S2.y(A_CM), S2.y(-A_CM), ORANGE, k2)
        dashed(d, (xv, S2.y(A_CM)), (980, S2.y(A_CM)), A(ORANGE, k2), w=3)
        text(d, (xv - 24, S2.yc), "6,0 cm", 58, DORANGE, anchor="rm", alpha=k2)
        card(d, (60, 1070, 1020, 1190), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), r=24, w=5)
        text(d, (W / 2, 1130), "A = 6,0 : 2 = 3,0 cm", 60, DORANGE, alpha=k2)
    k3 = appear(t, M[2] - 0.05, 0.4)
    if k3 > 0:
        card(d, (60, 1220, 1020, 1530), fill=A(WHITE, k3), outline=A(NAVY, k3), r=24, w=5)
        text(d, (W / 2, 1280), "Chưa nói được", 60, NAVY, alpha=k3)
        text(d, (100, 1370), "• Giấy kéo tay: có đều?", 58, INK, anchor="lm", alpha=k3)
        text(d, (100, 1460), "• Ma sát đầu bút: bỏ qua", 58, INK, anchor="lm", alpha=appear(t, M[2] + 2.5, 0.4))

# ---------------- canh 4: Bay - dinh -> day ke nhau ----------------
SB = Strip(60, 1020, 300, 760, 30, 0, U1)
def s_bay(img, d, t, sc):
    M = sc["M"]
    lam = peaks_strip(d, SB, 200, 1)                        # dinh o 200, 520, 840; day o 360, 680
    yp, yt = SB.y(A_CM), SB.y(-A_CM)
    kr = clamp((t - 0.2) / 1.0)                             # do: dinh 200 -> day 360
    yr = yt + 60
    for xx, yy in ((200, yp), (360, yt)): dashed(d, (xx, yy + 8), (xx, yr), DRED, w=4)
    bracket_h(d, 200, 360, yr, DRED, k=kr)
    card(d, (60, 860, 1020, 980), fill=(254, 242, 242), outline=DRED, r=24, w=5)
    text(d, (W / 2, 920), "✗ 8 cm: mới nửa chu kì", 60, DRED)
    kg = clamp((t - M[1] + 0.05) / 1.0)
    if kg > 0:
        yg = yp - 60
        for xx in (520, 840): dashed(d, (xx, yp - 8), (xx, yg), DGREEN, w=4)
        bracket_h(d, 520, 840, yg, DGREEN, k=kg)
        card(d, (60, 1010, 1020, 1130), fill=(236, 253, 243), outline=GREEN, r=24, w=5)
        text(d, (W / 2, 1070), "✓ 16 cm: đủ 1 chu kì", 60, DGREEN)
    if t < M[1]: xd = 200 + 160 * (((t - 0.2) / 1.6) % 1.0)          # cham chay theo net: dinh -> day (do)
    else: xd = 520 + 320 * (((t - M[1]) / 2.4) % 1.0)                 # dinh -> dinh (xanh)
    xs0, col = (200, DRED) if t < M[1] else (520, DGREEN)
    yy = lambda x: SB.y(A_CM * math.cos(2 * math.pi * (x - 200) / lam))
    seg = [(x, yy(x)) for x in range(xs0, int(xd) + 1, 4)]
    if len(seg) > 1: d.line(seg, fill=col, width=18, joint="curve")   # to dam doan da di: doc theo net
    dot(d, xd, yy(xd), 28, col)

# ---------------- canh 5: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
SE = Strip(100, 980, 380, 760, 30, 0, U1)
def s_end(img, d, t, sc):
    k1 = 1.0 if t >= 0.15 else 0.0                          # hien cung luc: tranh 2 khoi chu cach < 2 s
    card(d, (40, 215, 1040, 1585), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 240, W / 2 + pw / 2, 316), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 278), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    if k1 <= 0: return
    lam = peaks_strip(d, SE, 260, 1)                        # dinh 260, 580, 900
    yp, yt = SE.y(A_CM), SE.y(-A_CM)
    bracket_v(d, 420, SE.yc, yp, ORANGE)                    # A: tu duong giua toi dinh (x = 420 nam giua dinh 260 va day 420)
    dashed(d, (260, yp), (420, yp), ORANGE, w=3)
    text(d, (440, SE.yc - 40), "A = 3,0 cm", 58, DORANGE, anchor="lm")
    yb = yt + 50
    for xx in (580, 900): dashed(d, (xx, yp + 8), (xx, yb), DGREEN, w=4)
    bracket_h(d, 580, 900, yb, DGREEN)
    text(d, (740, yb + 56), "T = 0,80 s", 58, DGREEN)
    text(d, (W / 2, 1060), "Tốc độ cực đại", 64, DORANGE)
    text(d, (W / 2, 1150), "của quả nặng?", 64, DORANGE)
    seg_bar(d, 1300, t, 0.8, sc["T"] - 0.2, ORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, dv, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + RUN_H[0], "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (dv["t0"] + RUN_D[0], "tap"), (dv["t0"] + dv["M"][1] + 0.2, "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l11-baitapdaodong-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Bài tập dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bút vẽ lên băng giấy", draw=s_hook, tail=0.3, caps=[
   ("Bút gắn quả nặng vẽ lên giấy chạy.", 4.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.2, caps=[
   ("Thả lại, kéo giấy nhanh gấp đôi.", 4.2),
   ("Đo khoảng hai đỉnh bằng thước.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Kéo nhanh gấp đôi, đỉnh xa gấp đôi.", 4.6),
   ("Biên độ đọc theo chiều dọc.", 4.0),
   ("Số minh hoạ, chưa đo thật.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: lấy đỉnh tới đáy kề nhau.", 3.6),
   ("Phải từ đỉnh tới đỉnh kế tiếp.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Đỉnh tới đỉnh là một chu kì.", 7.0)]),
])
