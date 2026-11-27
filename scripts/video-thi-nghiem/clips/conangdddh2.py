# Clip: tn-l11-conangdddh-02 - Xich du: the nang tren cao doi thanh dong nang o day (vi_du)
# (9/11/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 56 px khi ve, K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-conangdddh-02.json (_kiem_so() doi chieu):
#   m = 40 kg ; g = 9,8 ; H = 0,50 m (0,1-1,2) ; moc the nang o day, bo ma sat trong mot luot.
#   so_lieu_mau (h m, Et J, Ed J, v m/s): 0,5 196 0 0 ; 0,25 98 98 2,21 ; 0 0 196 3,13.
# Du doan (giu, = dong "Nhin vao" cua hop vi du trong bai; khong trung quiz/Tu kiem tra): ghe xuong 0,25 m,
#   dong nang bang may phan the nang luc tren cao? -> mot nua (98/196).
# Bay = hien_tuong_hay_sai[0] "tuong du dung (v = 0) la het nang luong" (hai nhip >= 3 s).
# Thu nghi (= cau_chot khung web): tha tu 1,00 m (trong dai H) -> toc do qua day = can(2*9,8*1) = 4,43 m/s
#   (khong phai gap doi 6,26). Dap so KHONG hien tren man.
from engine import *

M_KG, G, HM = 40.0, 9.8, 0.50
PIV = (220, 330); LPX = 520; SCY = 300          # px/m theo phuong dung
LM = LPX / SCY                                  # dai day theo thang ve (khong hien)
A0 = math.acos(1 - HM / LM)
BOT = PIV[1] + LPX                              # y ghe o day
DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55)
SEAT = (234, 88, 12); SKIN = (240, 190, 150); SHIRT = (124, 58, 237)
CET, CED = (37, 99, 235), (234, 88, 12)
MARKS = [(0.50, "196", "0", "0"), (0.25, "98", "98", "2,21"), (0.0, "0", "196", "3,13")]   # so_lieu_mau

# --- tich phan chuyen dong con lac (chieu that) ---
def _sim():
    a, w, t, dt = A0, 0.0, 0.0, 1e-4; out = [(0.0, a)]
    t_half = None
    while a > 0:
        w += -(G / LM) * math.sin(a) * dt; a += w * dt; t += dt
        if t_half is None and LM * (1 - math.cos(a)) <= 0.25: t_half = t
        out.append((t, max(a, 0.0)))
    return out, t_half, t
TRAJ, T_HALF, T_BOT = _sim()
A_HALF = math.acos(1 - 0.25 / LM)
def ang_at(tr):
    if tr <= 0: return A0
    if tr >= T_BOT: return 0.0
    lo, hi = 0, len(TRAJ) - 1
    while hi - lo > 1:
        mi = (lo + hi) // 2
        if TRAJ[mi][0] <= tr: lo = mi
        else: hi = mi
    return TRAJ[lo][1]

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-conangdddh-02.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["m"]["gia_tri"] == M_KG and tp["g"]["gia_tri"] == G and tp["H"]["mac_dinh"] == HM
    assert k["so_lieu_mau"]["hang"] == [[0.5, 196, 0, 0], [0.25, 98, 98, 2.21], [0, 0, 196, 3.13]]
    assert tp["H"]["min"] <= 1.0 <= tp["H"]["max"] and abs(math.sqrt(2 * G * 1.0) - 4.43) < 0.005
_kiem_so()
DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

_TI = {}
def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi cong thuc: _{..} chi so duoi (>= 56 px)."""
    fs = []
    for p in [p for p in re.split(r"(_\{[^}]*\})", s) if p]:
        if p.startswith("_{"): fs.append((p[2:-1], F(max(56, size * 0.7)), size * 0.24))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=170, n=5):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9)
    for i in range(n):
        x = x0 + i * 152
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=16)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def pill(d, cy, s, col, a=1.0, size=56):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, cy - 40, W / 2 + pw / 2, cy + 40), fill=A(col, a), r=40)
    text(d, (W / 2, cy), s, size, WHITE, alpha=a)

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1)
    if L < 1: return
    n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(p0[0] + (p1[0] - p0[0]) * a, p0[1] + (p1[1] - p0[1]) * a),
                (p0[0] + (p1[0] - p0[0]) * b, p0[1] + (p1[1] - p0[1]) * b)], fill=col, width=w)

def rot(pts, c, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]

def seat_pos(ang): return (PIV[0] + LPX * math.sin(ang), PIV[1] + LPX * math.cos(ang))
def h_of(ang): return LM * (1 - math.cos(ang))

# ---------------- xich du + thuoc do cao ----------------
def frame_sw(d):
    fy = BOT + 70
    for sgn in (-1, 1): d.line([PIV, (PIV[0] + sgn * 400, fy)], fill=LIGHT, width=12)
    d.line([(0, fy), (800, fy)], fill=MUTED, width=4)
    dot(d, PIV[0], PIV[1], 16, GRAY, outline=NAVY)

def swing(d, ang, alpha=1.0, ghost=False):
    c = lambda col: A(col, alpha)
    sx, sy = seat_pos(ang)
    d.line([PIV, (sx, sy)], fill=c(NAVY if not ghost else GRAY), width=5)
    seat = rot([(sx - 60, sy), (sx + 60, sy), (sx + 60, sy + 16), (sx - 60, sy + 16)], (sx, sy), -ang)
    d.polygon(seat, fill=c(SEAT if not ghost else LIGHT), outline=c(NAVY if not ghost else GRAY))
    if ghost: return
    body = rot([(sx - 22, sy - 96), (sx + 22, sy - 96), (sx + 22, sy - 4), (sx - 22, sy - 4)], (sx, sy), -ang)
    d.polygon(body, fill=c(SHIRT))
    hx, hy = rot([(sx, sy - 128)], (sx, sy), -ang)[0]
    d.ellipse([hx - 28, hy - 28, hx + 28, hy + 28], fill=c(SKIN), outline=c(NAVY), width=3)
    leg = rot([(sx + 4, sy + 2), (sx + 56, sy + 4), (sx + 66, sy + 60)], (sx, sy), -ang)
    d.line(leg, fill=c(NAVY), width=12, joint="curve")
    dot(d, PIV[0], PIV[1], 9, c(NAVY))


RX = 720
def ruler(d, hl=None):
    y0 = BOT - HM * SCY
    d.rectangle([RX - 12, y0 - 20, RX + 12, BOT + 6], fill=(250, 240, 200), outline=NAVY, width=2)
    for k in range(11):
        y = BOT - k * 0.05 * SCY; L = 22 if k % 5 == 0 else 10
        d.line([(RX - 12, y), (RX - 12 + L, y)], fill=NAVY, width=3 if L == 22 else 2)
    for hv, lab in ((0.50, "0,50 m"), (0.25, "0,25 m"), (0.0, "0")):
        text(d, (RX + 30, BOT - hv * SCY), lab, 56, DORANGE if hl == hv else INK, anchor="lm")

BX0, BL = 200, 600                                # thanh ngang: 196 J = 600 px
def hbars(d, et, nums=False, alpha=1.0, y=1060):
    ed = 196 - et
    for j, (val, col, lab) in enumerate(((et, CET, "E_{t}"), (ed, CED, "E_{d}"))):
        yy = y + j * 140
        eq(d, 70, yy, lab, 60, col, alpha=alpha, anchor="l")
        d.rounded_rectangle([BX0, yy - 40, BX0 + BL, yy + 40], radius=12, outline=A(LIGHT, alpha), width=3)
        L = val / 196 * BL
        if L > 4: d.rounded_rectangle([BX0, yy - 40, BX0 + L, yy + 40], radius=12, fill=A(col, alpha))
        if nums: text(d, (1030, yy), f"{val:.0f} J", 58, col, anchor="rm", alpha=alpha)
    dashed(d, (BX0 + BL, y - 70), (BX0 + BL, y + 210), A(INK, alpha), w=4, on=10, off=8)

def vbadge(d, s, alpha=1.0):
    card(d, (640, 260, 1040, 350), fill=A(WHITE, alpha), outline=A(DGREEN, alpha), r=24, w=4)
    text(d, (840, 305), s, 56, DGREEN, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    frame_sw(d)
    swing(d, A_HALF, ghost=True)
    sx, sy = seat_pos(A_HALF)
    dashed(d, (sx + 64, sy), (RX - 14, sy), ORANGE, w=4, on=10, off=8)
    swing(d, A0)
    sx, sy = seat_pos(A0)
    dashed(d, (sx + 64, sy), (RX - 14, sy), GRAY, w=4, on=10, off=8)
    ruler(d, hl=0.25)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 980 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 180), "Bỏ ma sát. Ghế xuống tới 0,25 m.", 56, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Động năng bằng mấy phần", 60, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 350), "thế năng lúc trên cao?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 460, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: tha, dung hinh hai moc (quay cham x3) ----------------
REL, FZ, SL = 1.0, 2.0, 3.0
def do_state(t):
    if t < REL: return A0, 0
    tr = (t - REL) / SL
    if tr < T_HALF: return ang_at(tr), None
    if t < REL + T_HALF * SL + FZ: return A_HALF, 1
    tr = (t - REL - FZ) / SL
    if tr < T_BOT: return ang_at(tr), None
    return 0.0, 2

def s_do(img, d, t, sc):
    ang, mk = do_state(t)
    frame_sw(d)
    swing(d, ang)
    ruler(d, hl=MARKS[mk][0] if mk is not None else None)
    pw = tw(d, "quay chậm ×3", F(56)) + 56
    card(d, (60, 1380, 60 + pw, 1460), fill=ORANGE, r=40); text(d, (60 + pw / 2, 1420), "quay chậm ×3", 56, WHITE)
    et = float(MARKS[mk][1]) if mk is not None else M_KG * G * h_of(ang)
    hbars(d, min(196.0, et), nums=mk is not None)
    if mk is not None: vbadge(d, "v = " + MARKS[mk][3] + " m/s")

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    frame_sw(d); swing(d, A_HALF); ruler(d, hl=0.25)
    hbars(d, 98.0, nums=True)
    k2 = appear(t, 2.3, 0.4)
    if k2 > 0: text(d, (W / 2, 1400), "98 J = 196 J : 2", 62, DBLUE, alpha=k2)
    kp = appear(t, M[1] - 0.1, 0.4)
    if kp > 0: pill(d, 1530, "ĐÁP ÁN · một nửa", NAVY, kp, size=58)

# ---------------- canh 4: Bay ----------------
def s_bay(img, d, t, sc):
    kc = appear(t, 3.4, 0.5)
    frame_sw(d); swing(d, A0); ruler(d, hl=0.5)
    vbadge(d, "v = 0")
    y0 = 980
    card(d, (40, y0, 1040, y0 + 560), fill=WHITE, outline=DRED, w=6)
    pill(d, y0 + 70, "BẪY", DRED)
    text(d, (W / 2, y0 + 200), "✗ Dừng là hết năng lượng", 60, DRED)
    if kc > 0:
        lw = tw(d, "✗ Dừng là hết năng lượng", F(60))
        d.line([(W / 2 - lw / 2, y0 + 202), (W / 2 - lw / 2 + lw * kc, y0 + 202)], fill=(140, 15, 15), width=7)
        eq(d, W / 2, y0 + 330, "✓ v = 0 nhưng E_{t} = 196 J", 60, DGREEN, alpha=kc)


# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 980, 1040, 1320), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 1065), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 1210), "Nếu có ma sát?", 62, INK)
    frame_sw(d)
    swing(d, A0 * math.exp(-0.25 * t) * math.cos(2 * math.pi * t / 2.6))

# ---------------- canh 6: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 290, "THỬ NGHĨ", ORANGE, k1)
    card(d, (80, 380, 1000, 500), fill=A((239, 246, 255), k1), r=20)
    text(d, (W / 2, 440), "Thả từ 0,50 m: qua đáy 3,13 m/s", 56, DBLUE, alpha=k1)
    kq = appear(t, 2.2, 0.45)
    if kq > 0:
        text(d, (W / 2, 700), "Bỏ ma sát, thả từ 1,00 m.", 62, INK, alpha=kq)
        text(d, (W / 2, 810), "Qua đáy, tốc độ bao nhiêu?", 62, DORANGE, alpha=kq)
        seg_bar(d, 960, t, 2.8, sc["T"] - 0.2, ORANGE, kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + REL, "tap"), (do["t0"] + REL + T_HALF * SL, "tick"),
            (do["t0"] + REL + FZ + T_BOT * SL, "tick"), (da["t0"] + da["M"][1] - 0.1, "ding"),
            (b["t0"] + 0.3, "buzz"), (e["t0"] + 2.2, "open")]

CLIP = dict(id="tn-l11-conangdddh-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Cơ năng dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xích đu trên cao", draw=s_hook, tail=0.3, caps=[
   ("Ghế dừng trên cao, cách đáy 0,50 m.", 3.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Thả ghế xuống", draw=s_do, tail=0.2, caps=[
   ("Thả ghế, dừng hình ở hai mốc.", 3.6),
   ("Thế năng giảm, động năng tăng.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.2, caps=[
   ("So động năng với lúc trên cao.", 4.0),
   ("Tổng vẫn là 196 J.", 3.0)]),
 dict(key="bay", title="Bẫy: đu dừng", draw=s_bay, tail=0.3, caps=[
   ("Lúc dừng, tốc độ bằng không.", 3.4),
   ("Năng lượng nằm ở thế năng.", 3.2)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Mô hình bỏ qua ma sát.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Đổi độ cao thả.", 3.0),
   ("Dừng lại, tự tính.", 4.8)]),
])
