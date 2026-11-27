# Clip: tn-l10-sai-so-01 - Bam gio 10 dao dong con lac don, 5 lan (9/11/2026; dung lai 27/11/2026 theo cong moi viec 4:
#   --do-chu 0 LOI, chu ve >= 56 px, Du doan khong nut A-D (K10), thanh dem lien, cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-sai-so-01.json (_kiem_so() doi chieu):
#   so_lieu_mau: t = 20,19; 19,85; 20,14; 19,94; 20,23 s ; Δt_i = 0,12; 0,22; 0,07; 0,13; 0,16 s ; t̄ = 20,07 s.
# Bai 48: khoi video dung TRUOC hop exp. Cau 2 hoi Δt (0,15; nhieu 0,14/0,70/0,22) -> clip KHONG tinh Δt ("Δt = ?"),
#   khong hien 0,14 / 0,15 / 0,75 %. Doc bang (sau hop) giai thich tay bam 0,1-0,2 s -> Du doan hoi DO LON chenh lech.
# Chot (THU NGHI, chua chieu): bam 20 dao dong, tay lech nhu cu -> sai so cua MOT chu ki giam con khoang mot nua
#   (ΔT = Δt/so dao dong; bai chi chieu ΔT = Δt/10 o loi giai g, khong hoi doi so dao dong).
# Canh: Du doan -> Bam gio 5 lan (bang + cham tren truc) + DAP AN -> Lay trung binh (t̄, cot lech, Δt = ?)
#       -> Chua noi duoc -> Bay (dong ho 0,01 s nen sai 0,01 s, so cung ti le) -> THU NGHI.
from engine import *

T_DO = [20.19, 19.85, 20.14, 19.94, 20.23]
D_I = ["0,12", "0,22", "0,07", "0,13", "0,16"]
TBAR = 20.07
DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (91, 33, 182); DORANGE = (176, 64, 8)
BOB = (234, 88, 12)
def vn(x): return f"{x:.2f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-sai-so-01.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert [h[1] for h in hang] == T_DO and [vn(h[2]) for h in hang] == D_I
    assert abs(sum(T_DO) / 5 - TBAR) < 0.005 and abs(sum(T_DO) - 100.35) < 1e-6
    for tt, di in zip(T_DO, D_I): assert vn(abs(tt - TBAR)) == di
_kiem_so()

def tbar_text(d, cx, cy, s, size, color, alpha=1.0, anchor="mm"):
    """Ve chuoi bat dau bang 't' roi ke gach ngang tren chu t (dau macron ghep cua font SF lech trai)."""
    f = F(size); text(d, (cx, cy), s, size, color, anchor=anchor, alpha=alpha)
    l, tp, r, b = d.textbbox((cx, cy), s, font=f, anchor=anchor)
    tl, tt, tr, tb_ = d.textbbox((l, tp), "t", font=f, anchor="lt")
    d.line([(tl + 1, tt - size * 0.12), (tr + 2, tt - size * 0.12)], fill=A(color, alpha), width=max(3, size // 14))

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

# ---------- hinh dung chung ----------
def pendulum(d, px, py, L, ang_deg, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([px - 90, py - 16, px + 90, py], fill=c(GRAY))
    a = math.radians(ang_deg); bx, by = px + L * math.sin(a), py + L * math.cos(a)
    yy = py
    while yy < py + L:
        d.line([(px, yy), (px, min(yy + 14, py + L))], fill=c(LIGHT), width=3); yy += 26
    d.line([(px, py), (bx, by)], fill=c(NAVY), width=5)
    dot(d, bx, by, 28, c(BOB), outline=c((154, 52, 18)))

def stopwatch(d, box, s, alpha=1.0, sub=None):
    x0, y0, x1, y1 = box; c = lambda col: A(col, alpha)
    card(d, box, fill=c(NAVY), r=30)
    card(d, (x0 + 24, y0 + 24, x1 - 24, y1 - (84 if sub else 24)), fill=c((222, 247, 236)), r=18)
    cy = (y0 + 24 + y1 - (84 if sub else 24)) / 2
    text(d, ((x0 + x1) / 2, cy), s, 84, NAVY, alpha=alpha)
    if sub: text(d, ((x0 + x1) / 2, y1 - 44), sub, 56, WHITE, alpha=alpha)

AX0, AX1, V0, V1 = 140, 940, 19.8, 20.4
def ax(v): return AX0 + (v - V0) / (V1 - V0) * (AX1 - AX0)
def axis(d, y, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.line([(AX0 - 40, y), (AX1 + 40, y)], fill=c(INK), width=4)
    for v in (19.8, 20.0, 20.2, 20.4):
        d.line([(ax(v), y - 14), (ax(v), y + 14)], fill=c(INK), width=4)
        text(d, (ax(v), y + 56), vn(v)[:-1], 56, INK, alpha=alpha)
    text(d, (AX1 + 40, y - 50), "t (s)", 56, INK, anchor="rm", alpha=alpha)

def dots(d, y, ks, hl=None):
    for i, k in enumerate(ks):
        if k <= 0: continue
        col = DRED if (hl and i in hl) else BOB
        dot(d, ax(T_DO[i]), y, 20, A(col, k))

TX = (200, 500, 820)
def table(d, y0, n, lech=0, alpha=1.0, hl=-1):
    c = lambda col: A(col, alpha); rh = 76
    card(d, (60, y0, 1020, y0 + 92 + rh * 5), fill=c(WHITE), outline=c(NAVY), w=4, r=24)
    text(d, (TX[0], y0 + 46), "Lần", 56, INK, alpha=alpha)
    text(d, (TX[1], y0 + 46), "t (s)", 56, INK, alpha=alpha)
    if lech: text(d, (TX[2], y0 + 46), "lệch (s)", 56, DPURP, alpha=alpha)
    d.line([(90, y0 + 90), (990, y0 + 90)], fill=c(LIGHT), width=3)
    for i in range(n):
        yy = y0 + 92 + rh * i + rh / 2
        if i == hl: d.rounded_rectangle([80, yy - 34, 1000, yy + 34], radius=14, fill=c((255, 241, 222)))
        text(d, (TX[0], yy), str(i + 1), 56, INK, alpha=alpha)
        text(d, (TX[1], yy), vn(T_DO[i]), 58, INK, alpha=alpha)
        if i < lech: text(d, (TX[2], yy), D_I[i], 58, DPURP, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    pendulum(d, 250, 300, 430, 6 * math.sin(2 * math.pi * t / 2.0), alpha=a)
    stopwatch(d, (480, 360, 1010, 680), "?", alpha=a, sub="chia 0,01 s")
    k = appear(t, M[1] - 0.3, 0.45)
    if k <= 0: return
    y0 = 860 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 620), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 290), "Bấm 10 dao động, 5 lần:", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 400), "5 số lệch nhau", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 490), "cỡ bao nhiêu giây?", 62, PURPLE, alpha=k)

# ---------------- canh 2: Bam gio 5 lan ----------------
RUN0, RUND, RUNC = 0.0, 1.5, 1.0
AXY = 1260
def run_state(t):
    i = int(clamp((t - RUN0) / RUND, 0, 4.999))
    q = clamp((t - (RUN0 + i * RUND)) / RUNC)
    n = i + 1 if (q >= 1 or i == 0) else i
    return i, T_DO[i] * q, n

def s_do(img, d, t, sc):
    M = sc["M"]
    pendulum(d, 210, 290, 230, 6 * math.sin(2 * math.pi * t / 0.9))
    i, v, n = run_state(t)
    stopwatch(d, (400, 270, 1010, 530), vn(v) + " s", sub=f"lần {i + 1}")
    table(d, 570, n, hl=n - 1)
    axis(d, AXY)
    kh = appear(t, M[2] + 0.2, 0.4)
    dots(d, AXY - 60, [1.0 if j < n else 0 for j in range(5)], hl=({1, 4} if kh > 0 else None))
    if kh > 0:
        xa, xb, yb = ax(T_DO[1]), ax(T_DO[4]), AXY - 110
        d.line([(xa, yb), (xb, yb)], fill=A(DRED, kh), width=6)
        for x in (xa, xb): d.line([(x, yb - 16), (x, yb + 16)], fill=A(DRED, kh), width=6)
        s_ = "ĐÁP ÁN: vài phần mười giây"; pw = tw(d, s_, F(58)) + 70
        card(d, (W / 2 - pw / 2, 1400, W / 2 + pw / 2, 1500), fill=A((220, 252, 231), kh), outline=A(GREEN, kh), r=28, w=5)
        text(d, (W / 2, 1450), s_, 58, DGREEN, alpha=kh)

# ---------------- canh 3: Lay trung binh ----------------
def s_tb(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 250, 1020, 380), fill=A(WHITE, a), outline=A(BLUE, a), w=4)
    tbar_text(d, W / 2, 315, "t = 100,35 : 5 = 20,07 s", 60, BLUE, alpha=a)
    yax = 560
    axis(d, yax, alpha=a)
    dots(d, yax - 60, [a] * 5)
    x = ax(TBAR); yy = yax - 165
    while yy < yax + 10:
        d.line([(x, yy), (x, min(yy + 16, yax + 10))], fill=A(BLUE, a), width=5); yy += 28
    nl = 0 if t < M[1] - 0.1 else min(5, 1 + int((t - M[1] + 0.1) / 0.3))
    for i in range(nl):
        x0_, x1_ = sorted((ax(T_DO[i]), ax(TBAR)))
        d.line([(x0_, yax - 100 - 10 * i), (x1_, yax - 100 - 10 * i)], fill=A(DPURP, 1), width=5)
    table(d, 700, 5, lech=nl, alpha=a)
    k3 = appear(t, M[2] - 0.05, 0.4)
    if k3 > 0:
        card(d, (180, 1290, 900, 1430), fill=A(WHITE, k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1360), "Δt (sai số) = ?", 60, DGREEN, alpha=k3)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35)
    card(d, (60, 250, 1020, 760), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 335), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 485), "Đếm nhầm?", 60, BLUE, alpha=k)
    text(d, (W / 2, 635), "Góc lệch lớn?", 60, BLUE, alpha=k)
    pendulum(d, W / 2, 880, 520, 28 * math.sin(2 * math.pi * t / 1.6), alpha=k)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 250, 1020, 760), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    text(d, (W / 2, 330), "✗ Đồng hồ chia 0,01 s", 60, DRED, alpha=a)
    text(d, (W / 2, 430), "nên sai số chỉ 0,01 s", 60, DRED, alpha=a)
    cx, cy, r = W / 2, 620, 100                                          # dong ho kim quay: cho nguoi xem doc
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, a), outline=A(NAVY, a), width=8)
    ag = t * 2.2
    d.line([(cx, cy), (cx + 80 * math.sin(ag), cy - 80 * math.cos(ag))], fill=A(DRED, a), width=8)
    kb = appear(t, M[1] - 0.05, 0.35); S_ = 2600; x0 = 300
    if kb <= 0: return
    card(d, (60, 800, 1020, 1570), fill=A(WHITE, kb), outline=A(GREEN, kb), w=6)
    text(d, (W / 2, 870), "✓ Lệch mỗi lần (s), cùng thang", 56, DGREEN, alpha=kb)
    text(d, (100, 960), "chia", 56, TEAL, anchor="lm", alpha=kb)
    d.rectangle([x0, 936, x0 + 0.01 * S_, 986], fill=A(TEAL, kb))
    text(d, (x0 + 0.01 * S_ + 24, 961), "0,01", 56, TEAL, anchor="lm", alpha=kb)
    for i in range(5):
        v = float(D_I[i].replace(",", ".")); yy = 1030 + i * 105
        g = ease((t - M[1] - 0.2 - 0.15 * i) / 0.8)
        text(d, (100, yy + 25), f"lần {i + 1}", 56, INK, anchor="lm", alpha=kb)
        d.rectangle([x0, yy, x0 + v * S_ * g, yy + 50], fill=A(PURPLE, kb))
        text(d, (x0 + v * S_ * g + 20, yy + 25), D_I[i], 56, DPURP, anchor="lm", alpha=kb)

# ---------------- canh 6: THU NGHI ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    pendulum(d, 300, 400, 420, 6 * math.sin(2 * math.pi * t / 2.0), alpha=k1)
    stopwatch(d, (520, 420, 1000, 720), "20", alpha=k1, sub="dao động")
    text(d, (W / 2, 1050), "Sai số của một chu kì", 60, INK, alpha=k1)
    text(d, (W / 2, 1150), "đổi thế nào?", 60, ORANGE, alpha=k1)
    cbar(d, 1300, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")] + \
           [(do["t0"] + RUN0 + i * RUND + RUNC, "tap") for i in range(5)] + \
           [(do["t0"] + do["M"][2] + 0.2, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1] + 0.1, "ding"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-sai-so-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Sai số phép đo · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bấm giờ con lắc đơn", draw=s_hook, tail=0.3, caps=[
   ("Lệch 5° rồi thả.", 2.5),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Đo 5 lần", draw=s_do, tail=0.3, caps=[
   ("Đếm đủ 10 dao động.", 3.6),
   ("Tay bấm lúc sớm, lúc muộn.", 3.9),
   ("So số nhỏ nhất, lớn nhất.", 3.6)]),
 dict(key="tb", title="Lấy trung bình", draw=s_tb, tail=0.3, caps=[
   ("Các số tản quanh trung bình.", 2.8),
   ("Mỗi lần lệch bao nhiêu?", 3.0),
   ("Em tự tính sai số Δt.", 2.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Còn hai lỗi chưa xét.", 3.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Dễ tưởng: lỗi do đồng hồ.", 3.6),
   ("Vẽ cùng tỉ lệ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Tay bấm vẫn lệch như cũ.", 5.6)]),
])
