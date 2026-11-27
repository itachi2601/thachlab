# Clip: tn-l11-tatdan-02 - Cung mot con lac, tha trong khong khi, nuoc, dau nhot (9/11/2026, chang B L11 Dao dong;
# dung lai 27/11/2026 theo cong moi: chu ve >= 55 px (ra >= 48), moi nhip >= 2,5 s, Du doan khong nut A-D (K10),
# thanh dem day 70 px, Bay hai khung tu giai thich, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tatdan-02.json (_kiem_so()):
#   tham_so: A0 = 5,0 cm ; T = 1,0 s ; t doc dinh = 2,0 s ; beta (khong khi 0,4 ; nuoc 1,15 ; dau 2,8 /s).
#   mo_hinh: x = A0 e^(-beta t) cos(2 pi t / T), bao A(t) = A0 e^(-beta t) (net dut o canh Ket qua).
#   so_lieu_mau (lam tron 0,1 cm): sau 2 s con 2,2 ; 0,5 ; 0,0 cm. "Khong phai so do that" -> "so minh hoa".
# Du doan: sau 2 s, dinh con lai cua ba con lac xep the nao? -> khong khi > nuoc > dau.
# Bay = hien_tuong_hay_sai[0] "tat dan van la dieu hoa": khung tren (de tuong) dinh giu 5,0 cm moi nhip ;
#   khung duoi (khong khi that) dinh thap dan, net dut ngang muc 5,0 cm de thay dinh sau thap hon.
# Gioi han = gia_thiet "bo qua viec nuoc/dau lam nhip cham hon" + "so minh hoa".
# Cau tu kiem ngay sau hop: "Dau dac hon ... ve can bang roi dung" -> clip KHONG noi y do.
# THU NGHI (= cau_chot khung web): khong khi 5,0 -> 2,2 cm sau 2 s; co nang con khoang bao nhieu phan tram?
#   Buoc suy luan chua chieu: o dinh vat dung tuc thoi, W = 1/2 k A^2 -> (2,2/5,0)^2 = 0,19 -> ~19 %.
#   Dap so KHONG hien tren man (chi hien 5,0 va 2,2 cm).
from engine import *

A0, PER = 5.0, 1.0
MED = [("Không khí", 0.4, "2,2", BLUE), ("Nước", 1.15, "0,5", TEAL), ("Dầu nhớt", 2.8, "0,0", ORANGE)]
DRED, DGREEN, DPURPLE = (185, 28, 28), (21, 110, 55), (91, 33, 182)
def xt(beta, t): return A0 * math.exp(-beta * t) * math.cos(2 * math.pi * t / PER)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-tatdan-02.json")))
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["A0"]["gia_tri"] == A0 and ts["T"]["gia_tri"] == PER and ts["t"]["gia_tri"] == 2.0
    for (lab, b, v, _), h in zip(MED, k["so_lieu_mau"]["hang"]):
        assert abs(h[1] - b) < 1e-9 and f"{h[4]:.1f}".replace(".", ",") == v, (lab, h)
        assert abs(A0 * math.exp(-2 * b) - h[3]) < 6e-4, h
_kiem_so()

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 56
    card(d, (cx - pw / 2, cy - size * 0.82, cx + pw / 2, cy + size * 0.82), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem day 70 px, rut tu phai sang trai theo 10 nac (moi nac la mot thay doi hinh ro)."""
    p = clamp((t - t0) / (t1 - t0)); q = math.floor(p * 10 + 1e-9) / 10
    d.rounded_rectangle([140, y, 940, y + 70], radius=35, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 70], radius=35, fill=A(col, a))

# ---------------- ba con lac + coc ----------------
CXS = (200, 540, 880)
PY, LP, PXP = 330, 300, 14            # tru treo, day 300 px ; 1 cm = 14 px
OIL = (217, 160, 40)
def pend(d, cx, xcm, cup=None):
    dx = xcm * PXP; bx, by = cx + dx, PY + math.sqrt(LP * LP - dx * dx)
    if cup: d.rectangle([cx - 135, 540, cx + 135, 700], fill=A(cup, 0.32))
    d.line([(cx, PY), (bx, by)], fill=NAVY, width=5)
    dot(d, bx, by, 28, PURPLE, outline=WHITE)
    if cup: d.line([(cx - 135, 525), (cx - 135, 702), (cx + 135, 702), (cx + 135, 525)], fill=NAVY, width=5)
    d.line([(cx, by + 42), (cx, by + 60)], fill=GRAY, width=4)          # vach can bang
def rig(d, xs):
    d.rectangle([60, PY - 18, 1020, PY], fill=(190, 195, 210), outline=NAVY, width=3)
    for (lab, beta, _, col), cx, x in zip(MED, CXS, xs):
        pend(d, cx, x, None if lab == "Không khí" else ((120, 190, 240) if lab == "Nước" else OIL))
        text(d, (cx, 765), lab, 58, col)

# ---------------- ba dai x - t (truc co dinh) ----------------
SX0, SX1 = 350, 830                   # t = 0 -> 2 s
SYS = (960, 1190, 1420)               # tam moi dai (x = 0)
PXS = 16                              # 1 cm = 16 px
def sx(t): return SX0 + t / 2.0 * (SX1 - SX0)
def strips(d):
    for (lab, beta, _, col), y in zip(MED, SYS):
        d.line([(SX0, y), (SX1 + 10, y)], fill=GRAY, width=3)
        d.line([(SX0, y - 5 * PXS - 6), (SX0, y + 5 * PXS + 6)], fill=NAVY, width=3)
        text(d, (40, y), lab, 56, col, anchor="lm")
    yb = SYS[-1] + 5 * PXS
    for tt in (0, 1, 2):
        d.line([(sx(tt), yb + 6), (sx(tt), yb + 20)], fill=NAVY, width=4)
        text(d, (sx(tt), yb + 62), str(tt) + (" s" if tt == 2 else ""), 56, INK)

def trace(d, beta, y, tmax, col, w=6, x0=None, x1=None, pxs=PXS):
    x0 = SX0 if x0 is None else x0; x1 = SX1 if x1 is None else x1
    n = max(2, int(tmax / 0.01) + 1)
    pts = [(x0 + (i * tmax / (n - 1)) / 2.0 * (x1 - x0), y - xt(beta, i * tmax / (n - 1)) * pxs) for i in range(n)]
    d.line(pts, fill=col, width=w, joint="curve")

def env(d, beta, y, k, col):
    n = 60; pts = [(sx(2.0 * i / n), y - A0 * math.exp(-beta * 2.0 * i / n) * PXS) for i in range(int(n * k) + 1)]
    for j in range(0, len(pts) - 1, 2): d.line([pts[j], pts[j + 1]], fill=col, width=5)

def end_vals(d):
    for (_, b, v, col), y in zip(MED, SYS):
        yy = y - xt(b, 2.0) * PXS
        dot(d, sx(2.0), yy, 13, col, outline=WHITE)
        text(d, (sx(2.0) + 30, yy - (20 if v == "2,2" else 0)), v + " cm", 58, col, anchor="lm")

# ---------------- canh 1: Du doan (K10: chi cau hoi, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = ease((t - 0.6) / 1.2)
    rig(d, [A0 * k] * 3)
    pill(d, W / 2, 255, "kéo lệch 5,0 cm", 56, WHITE, NAVY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 700), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 80, "DỰ ĐOÁN", 58, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 270), "Sau 2 s, đỉnh ở ba nơi", 66, INK, alpha=a)
    text(d, (W / 2, y0 + 400), "xếp từ cao xuống thấp?", 66, DPURPLE, alpha=a)
    cbar(d, y0 + 560, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
REL, SLOW = 0.8, 2.0                  # tha o giay 0,8 ; 1 s mo hinh = 2 s video
def tsim(t): return clamp((t - REL) / SLOW, 0, 2.0)
def s_do(img, d, t, sc):
    ts = tsim(t)
    rig(d, [xt(b, ts) for _, b, _, _ in MED])
    pill(d, 290, 255, "t = " + f"{ts:.1f}".replace(".", ",") + " s", 56, WHITE, NAVY)
    pill(d, 790, 255, "số minh hoạ", 56, WHITE, ORANGE)
    strips(d)
    for (_, b, v, col), y in zip(MED, SYS):
        if ts > 0: trace(d, b, y, ts, col)
    if ts >= 2.0: end_vals(d)

# ---------------- canh 3: Ket qua + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 215, 1020, 425), fill=WHITE, outline=NAVY, r=26, w=5)
    pill(d, W / 2, 272, "ĐÁP ÁN", 56, WHITE, NAVY)
    text(d, (W / 2, 372), "Không khí > nước > dầu", 62, NAVY)
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr > 0:
        card(d, (60, 455, 1020, 690), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=26, w=5)
        text(d, (W / 2, 572), "Càng nhớt, tụt càng nhanh", 62, DGREEN, alpha=kr)
    strips(d)
    ke = clamp((t - 0.5) / 2.2)
    for (_, b, v, col), y in zip(MED, SYS):
        trace(d, b, y, 2.0, A(col, 0.40), w=5)
        env(d, b, y, ke, col)
        if t > 2.8:                                   # cham chay doc net dut (0 -> 2 s), lap lai: hinh khong dung yen
            u = ((t - 2.8) % 2.4) / 2.4 * 2.0
            dot(d, sx(u), y - A0 * math.exp(-b * u) * PXS, 22, col, outline=WHITE)
    end_vals(d)

# ---------------- canh 4: Bay - "tat dan van la dieu hoa" ----------------
BX0, BX1 = 120, 860; BPX = 15
def bpanel(d, y0, lab, col, beta, k, fill):
    card(d, (40, y0, 1040, y0 + 440), fill=fill, outline=col, w=6)
    text(d, (75, y0 + 62), lab, 58, col, anchor="lm")
    yc = y0 + 260
    d.line([(BX0, yc), (BX1 + 10, yc)], fill=GRAY, width=3)
    yt = yc - A0 * BPX
    x = BX0
    while x < BX1 + 10: d.line([(x, yt), (min(x + 16, BX1 + 10), yt)], fill=A(INK, 0.55), width=3); x += 30
    if k > 0:
        n = max(2, int(200 * k))
        pts = []
        for i in range(n + 1):
            tt = 2.0 * k * i / n
            amp = A0 if beta == 0 else A0 * math.exp(-beta * tt)
            pts.append((BX0 + tt / 2.0 * (BX1 - BX0), yc - amp * math.cos(2 * math.pi * tt) * BPX))
        d.line(pts, fill=col, width=7, joint="curve")
        if k < 1: dot(d, pts[-1][0], pts[-1][1], 30, col, outline=WHITE)      # but ve chay (hinh doi ro)
        for p in (0, 1, 2):
            if k * 2.0 >= p - 1e-9:
                amp = A0 if beta == 0 else A0 * math.exp(-beta * p)
                dot(d, BX0 + p / 2.0 * (BX1 - BX0), yc - amp * BPX, 14, col, outline=WHITE)
    return yc

def s_bay(img, d, t, sc):
    M = sc["M"]
    k1 = clamp((t - 0.3) / 1.6)
    yc = bpanel(d, 215, "✗ Dễ tưởng: vẫn điều hoà", DRED, 0, k1, (254, 242, 242))
    text(d, (BX1 + 40, yc - A0 * BPX), "5,0 cm", 56, DRED, anchor="lm")
    k2 = clamp((t - M[1]) / 1.4)
    yc2 = bpanel(d, 690, "Tắt dần, không khí", BLUE, 0.4, k2, WHITE)
    text(d, (BX0 + 20, yc2 - A0 * BPX - 40), "5,0 cm", 56, BLUE, anchor="lm")
    if k2 >= 1: text(d, (BX1 + 40, yc2 - 2.2 * BPX), "2,2 cm", 56, BLUE, anchor="lm")
    kc = appear(t, M[2] - 0.1, 0.45)
    if kc > 0:
        card(d, (60, 1165, 1020, 1300), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=26, w=5)
        text(d, (W / 2, 1232), "✓ Đỉnh sau thấp hơn đỉnh trước", 58, DGREEN, alpha=kc)

# ---------------- canh 5: Gioi han ----------------
def s_gioi(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Nhịp trong dầu chậm hơn?", 62, INK)
    # con lac trong coc dau, qua lai mot nhip roi gan nhu dung (hinh nhuc nhich ca canh)
    cx, py, lp = 540, 640, 380
    tt = (t * 0.5) % 2.0
    xcm = xt(2.8, tt); dx = xcm * 18; bx, by = cx + dx, py + math.sqrt(lp * lp - dx * dx)
    d.rectangle([280, py - 18, 800, py], fill=(190, 195, 210), outline=NAVY, width=3)
    d.rectangle([cx - 200, 900, cx + 200, 1100], fill=A(OIL, 0.32))
    d.line([(cx, py), (bx, by)], fill=NAVY, width=5); dot(d, bx, by, 32, PURPLE, outline=WHITE)
    d.line([(cx - 200, 880), (cx - 200, 1102), (cx + 200, 1102), (cx + 200, 880)], fill=NAVY, width=5)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 290, "THỬ NGHĨ", 58, WHITE, ORANGE, k1)
    # dai khong khi: chi 5,0 cm (luc tha) va 2,2 cm (sau 2 s)
    yc = 720; x0, x1 = 140, 840; px = 20
    d.line([(x0, yc), (x1 + 10, yc)], fill=A(GRAY, k1), width=3)
    trace(d, 0.4, yc, 2.0, A(BLUE, k1), w=7, x0=x0, x1=x1, pxs=px)
    for tt, v in ((0, "5,0 cm"), (2, "2,2 cm")):
        amp = A0 * math.exp(-0.4 * tt); xx = x0 + tt / 2.0 * (x1 - x0)
        dot(d, xx, yc - amp * px, 14, A(BLUE, k1), outline=WHITE)
    text(d, (x0 + 30, yc - A0 * px - 45), "5,0 cm", 58, BLUE, anchor="lm", alpha=k1)
    text(d, (x1 - 20, yc - 2.2 * px - 60), "2,2 cm", 58, BLUE, anchor="lm" if False else "mm", alpha=k1)
    text(d, (W / 2, 900), "Không khí, sau 2 s", 60, BLUE, alpha=k1)
    text(d, (W / 2, 1060), "Cơ năng còn khoảng", 66, INK, alpha=k1)
    text(d, (W / 2, 1150), "bao nhiêu phần trăm?", 66, INK, alpha=k1)
    cbar(d, 1300, t, 1.2, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + REL, "tap"), (do["t0"] + REL + 2.0 * SLOW, "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (b["t0"] + b["M"][2], "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-tatdan-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tắt dần · cưỡng bức · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Một con lắc, ba môi trường", draw=s_hook, tail=0.3, caps=[
   ("Cùng một con lắc, thả ba nơi.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Mỗi nơi thả một lần.", 4.2),
   ("Đọc đỉnh còn lại lúc 2 s.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Nối đỉnh thành nét đứt.", 3.4),
   ("Dầu cản mạnh nhất.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Tắt dần vẫn là điều hoà?", 3.4),
   ("So đỉnh với vạch 5,0 cm.", 3.6),
   ("Không lặp lại y hệt.", 3.0)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Số minh hoạ, chưa đo thật.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Lực cản lấy dần cơ năng.", 6.4)]),
])
