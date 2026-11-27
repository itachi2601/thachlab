# Clip: tn-l10-gia-toc-02 - Dau vet vien bi qua video: deu, nhanh dan, cham dan (31/10/2026; dung lai 27/11/2026
# theo cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Du doan khong nut, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-gia-toc-02.json (_kiem_so() doi chieu):
#   so_lieu_mau x0..x4 (cm) tai t = 0; 0,2; 0,4; 0,6; 0,8 s:
#     tren ban  (v0 0,4 m/s, a 0)    : 0, 8, 16, 24, 32   -> khoang 8, 8, 8, 8
#     xuong doc (v0 0,   a 1 m/s2)   : 0, 2, 8, 18, 32    -> khoang 2, 6, 10, 14
#     len doc   (v0 0,8, a -1 m/s2)  : 0, 14, 24, 30, 32  -> khoang 14, 10, 6, 2
# Du doan (bai chi noi "ngan dan" dinh tinh o o Quan sat, nen hoi SO): len doc, hai khoang dau 14, 10 cm -> khoang thu tu? -> 2 cm.
# Bay = hien_tuong_hay_sai "chi nhin vi tri cuoi (cung 32 cm) roi ket luan nhu nhau" (khong dung lai cap 14/10).
# Thu nghi (= cau_chot khung web, theo mo hinh x = v0.t + a.t2/2, a = -1 m/s2 cung mang, v0 = 0,9 m/s trong mien 0-1):
#   khoang dau 16 cm -> toi 0,8 s di bao xa? 16 + 12 + 8 + 4 = 40 cm (moi khoang ngan hon |a|.dt2 = 4 cm). 40 khong hien. Khong trung cau bai
#   (cau 🤔 cua bai hoi bi lan nguoc xuong - chot cu da bo vi trung).
from engine import *

DATA = [(0, 8, 16, 24, 32), (0, 2, 8, 18, 32), (0, 14, 24, 30, 32)]
V0A = [(0.4, 0.0), (0.0, 1.0), (0.8, -1.0)]
NAMES = ["Trên bàn", "Xuống dốc", "Lên dốc"]
KIND = ["đều", "nhanh dần", "chậm dần"]
DT = 0.2
CHOT_V0 = 0.9

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-gia-toc-02.json")))
    h = k["so_lieu_mau"]["hang"]
    for i in range(3):
        assert tuple(h[i][1:3]) == V0A[i] and tuple(int(x) for x in h[i][3:]) == DATA[i]
        for n in range(5): assert abs(100 * (V0A[i][0] * n * DT + V0A[i][1] * (n * DT) ** 2 / 2) - DATA[i][n]) < 1e-6
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["v0"]["min"] <= CHOT_V0 <= ts["v0"]["max"] and ts["dt"]["gia_tri"] == DT
    x = lambda tt: 100 * (CHOT_V0 * tt - tt * tt / 2)
    assert abs(x(0.2) - 16) < 1e-6 and abs(x(0.4) - x(0.2) - 12) < 1e-6 and abs(x(0.8) - 40) < 1e-6
_kiem_so()

PX0, PX1 = 110, 900; PXCM = (PX1 - PX0) / 32
STEEL = (148, 163, 184); RAMP = (226, 232, 240); RAMP_D = (100, 116, 139)
HL = (255, 237, 213); DRED = (185, 28, 28); DTEAL = (15, 118, 110); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
DGREEN = (21, 128, 61)

_GK = "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"; _gc = {}
def FG(size):
    size = int(size)
    if size not in _gc: _gc[size] = ImageFont.truetype(_GK, size)
    return _gc[size]
def sym(d, xy, s, size, col, alpha=1.0, anchor="mm"): dtext(d, xy, s, FG(size), col, alpha, anchor)

def X(cm): return PX0 + cm * PXCM
def xpos(i, tau):
    v0, a = V0A[i]; tau = clamp(tau, 0, 0.8); return 100 * (v0 * tau + a * tau * tau / 2)

def ball(d, x, y, R, alpha=1.0):
    d.ellipse([x - R, y - R, x + R, y + R], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=4)
    d.ellipse([x - R * 0.55, y - R * 0.6, x - R * 0.1, y - R * 0.15], fill=A(WHITE, alpha * 0.8))

def lane(d, y, i, n=5, gl=(), hl=0.0, name=True, cm=False, ka=1.0):
    """Lan i: ten o y, nhan khoang o y+75, hang cham o y+135."""
    if hl > 0: d.rounded_rectangle([50, y - 45, 1030, y + 175], radius=24, fill=A(HL, hl))
    if name: text(d, (80, y), NAMES[i], 58, INK, anchor="lm", alpha=ka)
    d.line([(PX0 - 30, y + 135), (PX1 + 30, y + 135)], fill=A(LIGHT, ka), width=4)
    r = DATA[i]
    for k in gl:
        text(d, ((X(r[k]) + X(r[k + 1])) / 2, y + 75), str(r[k + 1] - r[k]), 56, DORANGE, alpha=ka)
    if cm and gl: text(d, (PX1 + 40, y + 75), "cm", 56, DORANGE, anchor="lm", alpha=ka)
    for k in range(n): dot(d, X(r[k]), y + 135, 15, A(ORANGE, ka), outline=A(NAVY, ka))

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
def ramp_pic(d, box, s_frac, varr=0.0, aarr=0.0):
    x0, y0, x1, y1 = box
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    RB, RT = (x0 + 70, y1 - 40), (x1 - 70, y0 + 60)
    UL = math.hypot(RT[0] - RB[0], RT[1] - RB[1]); U = ((RT[0] - RB[0]) / UL, (RT[1] - RB[1]) / UL); N = (U[1], -U[0])
    tri = [RB, (RT[0], RB[1]), RT]
    d.polygon(tri, fill=RAMP); d.line(tri + [tri[0]], fill=RAMP_D, width=5)
    R = 30; s0 = s_frac * UL
    cx, cy = RB[0] + U[0] * s0 + N[0] * R, RB[1] + U[1] * s0 + N[1] * R
    ball(d, cx, cy, R)
    if varr > 0:
        a0 = (cx + U[0] * 50 + N[0] * 40, cy + U[1] * 50 + N[1] * 40); a1 = (a0[0] + U[0] * 200 * varr, a0[1] + U[1] * 200 * varr)
        arrow(d, a0, a1, BLUE, w=8, head=24); sym(d, (a1[0] + N[0] * 45, a1[1] + N[1] * 45), "v", 60, BLUE)
    if aarr > 0:
        a0 = (cx - U[0] * 50 - N[0] * 50, cy - U[1] * 50 - N[1] * 50); a1 = (a0[0] - U[0] * 170 * aarr, a0[1] - U[1] * 170 * aarr)
        arrow(d, a0, a1, DGREEN, w=8, head=24); sym(d, (a1[0] - N[0] * 45, a1[1] - N[1] * 45), "a", 60, DGREEN)

def s_hook(img, d, t, sc):
    M = sc["M"]
    ramp_pic(d, (40, 210, 1040, 640), 0.12 + 0.25 * (1 - (1 - clamp(t / 6)) ** 2), varr=1.0 - 0.4 * clamp(t / 6))
    card(d, (40, 665, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    lane(d, 720, 2, n=3, gl=(0, 1), cm=True)
    text(d, (X(24) + 90, 855), "?", 66, INK)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1190 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 395), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 22, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 165), "Khoảng thứ tư", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "dài bao nhiêu cm?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 300, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (chieu cham x2) ----------------
L0, LG, SLOW = 0.5, 2.0, 2.0
LY = [250, 540, 830]
def lane_tau(i, t): return (t - (L0 + LG * i)) / SLOW
def nshot(tau): return -1 if tau < 0 else min(4, int(tau / DT + 1e-9))

def s_do(img, d, t, sc):
    card(d, (40, 205, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    for i, y in enumerate(LY):
        tau = lane_tau(i, t); n = nshot(tau)
        lane(d, y, i, n=n + 1)
        if 0 <= tau < 0.85: ball(d, X(xpos(i, tau)), y + 135, 24)
    card(d, (40, 1130, 1040, 1260), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 1195), "chiếu chậm ×2", 58, INK)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 540), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL, ka)
    text(d, (W / 2, 420), "Khoảng thứ tư: 2 cm", 64, DTEAL, alpha=ka)
    card(d, (40, 570, 1040, 1000), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    lane(d, 630, 2, gl=(0, 1, 2, 3), cm=True, ka=ka)
    k2 = appear(t, M[1] + 0.1, 0.45)
    r = DATA[2]; cx = [(X(r[k]) + X(r[k + 1])) / 2 for k in range(4)]
    if k2 > 0:
        for k in range(3):
            xa, xb = cx[k], cx[k + 1]; yy = 880
            d.arc([xa, yy - 50, xb, yy + 50], 0, 180, fill=A(PURPLE, k2), width=7)
        text(d, ((cx[0] + cx[1]) / 2, 965), "−4", 56, PURPLE, alpha=k2)
        text(d, ((cx[1] + cx[2]) / 2 + 10, 965), "−4", 56, PURPLE, alpha=k2)
        text(d, ((cx[2] + cx[3]) / 2 + 40, 965), "−4", 56, PURPLE, alpha=k2)
        card(d, (40, 1030, 1040, 1250), fill=A((245, 243, 255), k2), outline=A(PURPLE, k2), w=5)
        text(d, (W / 2, 1140), "14 → 10 → 6 → 2", 64, PURPLE, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 205, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    show = (0.4, 2.9, 5.4)
    for i, y in enumerate(LY):
        k = appear(t, show[i], 0.4)
        lane(d, y, i, gl=range(4), hl=k, cm=(i == 0))
        if k > 0: text(d, (1000, y), "→ " + KIND[i], 58, DORANGE, anchor="rm", alpha=k)
    kv = appear(t, M[1] + 0.1, 0.45)
    ramp_pic(d, (40, 1130, 1040, 1585), 0.45, varr=1.0, aarr=ease((t - M[1] - 0.6) / 0.6))

# ---------------- canh 5: Bay ----------------
BY = [560, 830, 1100]
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 500), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 300), "✗ Cùng 32 cm, 0,8 s:", 60, DRED)
    text(d, (W / 2, 410), "như nhau?", 60, DRED)
    ks = clamp((t - M[1]) / 0.5)
    if ks > 0:
        lw = tw(d, "như nhau?", F(60)); d.line([(W / 2 - lw / 2 - 10, 412), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, 412)], fill=DRED, width=8)
    card(d, (40, 520, 1040, 1350), fill=WHITE, outline=LIGHT, w=3)
    km = t >= M[1]
    for yy in range(545, 1330, 26): d.line([(X(32), yy), (X(32), yy + 13)], fill=MUTED, width=4)
    card(d, (X(32) - 85, 530, X(32) + 85, 590), fill=WHITE, r=14)
    text(d, (X(32), 560), "32 cm", 56, NAVY)
    for i, y in enumerate(BY):
        r = DATA[i]
        text(d, (80, y), NAMES[i], 58, INK, anchor="lm")
        d.line([(PX0 - 30, y + 135), (PX1 + 30, y + 135)], fill=LIGHT, width=4)
        for k in ((0, 1, 2, 3, 4) if km else (0, 4)): dot(d, X(r[k]), y + 135, 15, ORANGE, outline=NAVY)
        if km:
            for k in range(4): text(d, ((X(r[k]) + X(r[k + 1])) / 2, y + 75), str(r[k + 1] - r[k]), 56, DORANGE)
    if km:
        card(d, (40, 1375, 1040, 1585), fill=WHITE, outline=DTEAL, w=6)
        text(d, (W / 2, 1480), "✓ Khoảng giữa khác nhau", 60, DTEAL)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 450), "v lúc bi qua từng chấm?", 62, INK)
    card(d, (40, 590, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    yb = 900; xa, xb = 260, 820
    d.line([(120, yb), (960, yb)], fill=LIGHT, width=4)
    for xx in (xa, xb): dot(d, xx, yb, 16, ORANGE, outline=NAVY)
    u = (t * 0.6) % 1.0; ball(d, xa + (xb - xa) * u, yb, 30)
    text(d, (xa, yb - 120), "v = ?", 62, BLUE, alpha=appear(t, 2.2, 0.4))

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "Cùng máng lên dốc,", 60, INK, alpha=k)
    text(d, (W / 2, 485), "bi lên nhanh hơn:", 60, INK, alpha=k)
    text(d, (W / 2, 590), "Tới 0,8 s, đi bao xa?", 64, DORANGE, alpha=k)
    y = 760
    d.line([(PX0 - 30, y + 135), (PX1 + 30, y + 135)], fill=A(LIGHT, k), width=4)
    for cm in (0, 16): dot(d, X(cm), y + 135, 15, A(ORANGE, k), outline=A(NAVY, k))
    text(d, (X(8), y + 75), "16 cm", 56, DORANGE, alpha=k)
    text(d, (X(16) + 110, y + 135), "?", 66, INK, alpha=k)
    seg_bar(d, 1100, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + L0 + LG * i, "tap") for i in range(3)]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-gia-toc-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Gia tốc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Viên bi lăn lên máng", draw=s_hook, tail=0.3, caps=[
   ("Chấm vị trí mỗi 0,2 s.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Ba đoạn, cùng cách chấm.", 3.0),
   ("Bàn, xuống dốc, lên dốc.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Khoảng thứ tư chỉ 2 cm.", 3.4),
   ("Mỗi khoảng ngắn hơn 4 cm.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("So khoảng trong từng đoạn.", 3.0),
   ("Lên dốc: a ngược chiều v.", 3.6)]),
 dict(key="bay", title="Bẫy: chỉ nhìn chấm cuối", draw=s_bay, tail=0.3, caps=[
   ("Chấm cuối trùng nhau.", 3.5),
   ("Khoảng giữa khác hẳn.", 3.5)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Chấm chỉ cho biết khoảng.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.4)]),
])
