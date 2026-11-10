# Clip: tn-l11-conangdddh-02 - Xich du: the nang tren cao doi thanh dong nang o day (9/11/2026, vi_du)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-conangdddh-02.json:
#   tham_so: m = 40 kg ; g = 9,8 ; H = 0,50 m (dieu_chinh 0,1-1,2) ; mo_hinh Et = mgh, Ed = mg(H - h), v = can(2Ed/m),
#   moc the nang tai day, bo ma sat trong mot luot, khong coi xich du la dao dong dieu hoa.
#   so_lieu_mau (h m, Et J, Ed J, v m/s): 0,5 196 0 0 ; 0,25 98 98 2,21 ; 0 0 196 3,13 (minh hoa).
#   Du doan: ghe xuong toi nua do cao (0,25 m), dong nang bang may phan the nang luc tren cao? Dap an mot nua (98 / 196).
#     Lua chon (khung ben canh): mot phan tu / mot nua / ba phan tu / toan bo. KHAC Du doan mo bai ("nang luong
#     luc du dung o tren cao di dau?"), KHAC conangdddh1 (lo xo: x = A/2 -> Ed = 3Et) va KHAC btnangluong2 (ti so v).
#   hien_tuong_hay_sai[0]: tuong du dung (v = 0) la het nang luong -> canh bay.
#   Cau chot: day ghe len cao 1,0 m (gap doi; trong khoang tham_so H) -> toc do qua day co gap doi? (khong, gap can 2;
#     dap so khong hien). Doan sau hop trong bai: "Khac con lac lo xo, W = mgh ti le voi m" -> clip khong noi ve m.
# Dan canh (khac btnangluong2 cung xich du): MOT lan tha tu 0,50 m, THUOC DO CAO dung canh duong di + HAI COT Et/Ed
#   bien doi lien tuc (truc 0-196 J co dinh), dung hinh o hai moc 0,25 m va day; khong bang, khong dien thoai, khong goc.
# Chuyen dong: day ve dai 520 px, thang cao 300 px/m (dai day suy ra ~1,73 m, KHONG ghi tren man); tich phan
#   alpha'' = -(g/l) sin alpha tu bien (chieu that), dung hinh khi h = 0,25 m va khi qua day.
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

_TI = {}
def TI(size):
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    fs = []
    for p in [p for p in re.split(r"(_\{[^}]*\}|\^\{[^}]*\})", s) if p]:
        if p.startswith("_{"): fs.append((p[2:-1], F(max(40, size * 0.8)), size * 0.3))    # chi so "đ" du lon de thay gach ngang
        elif p.startswith("^{"): fs.append((p[2:-1], F(max(36, size * 0.62)), -size * 0.34))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1)
    if L < 1: return
    n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p0[0], p1[0], a), lerp(p0[1], p1[1], a)), (lerp(p0[0], p1[0], b), lerp(p0[1], p1[1], b))], fill=col, width=w)

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
def ruler(d, hl=None, alpha=1.0):
    y0, y1 = BOT - HM * SCY, BOT
    d.rectangle([RX - 12, y0 - 20, RX + 12, y1 + 6], fill=A((250, 240, 200), alpha), outline=A(NAVY, alpha), width=2)
    for k in range(11):
        y = BOT - k * 0.05 * SCY
        L = 22 if k % 5 == 0 else 10
        d.line([(RX - 12, y), (RX - 12 + L, y)], fill=A(NAVY, alpha), width=3 if L == 22 else 2)
    for hv, lab in ((0.50, "0,50 m"), (0.25, "0,25 m"), (0.0, "0")):
        col = ORANGE if hl == hv else INK
        text(d, (RX + 26, BOT - hv * SCY), lab, 38, col, anchor="lm", alpha=alpha)

BX = (955, 1040); BW = 64; BH = 300            # cot Et, Ed: 196 J = 300 px
def bars(d, et, nums=None, alpha=1.0):
    ed = 196 - et
    for cx, val, col, lab in ((BX[0], et, CET, "E_{t}"), (BX[1], ed, CED, "E_{đ}")):
        d.rectangle([cx - BW / 2, BOT - BH, cx + BW / 2, BOT], outline=A(LIGHT, alpha), width=3)
        h = val / 196 * BH
        if h > 2: d.rectangle([cx - BW / 2 + 3, BOT - h, cx + BW / 2 - 3, BOT - 2], fill=A(col, alpha))
        eq(d, cx, BOT + 44, lab, 42, col, alpha=alpha)
    dashed(d, (BX[0] - 50, BOT - BH), (BX[1] + 50, BOT - BH), A(MUTED, alpha), w=3, on=8, off=8)
    if nums:
        for cx, s, col in ((BX[0], nums[0], CET), (BX[1], nums[1], CED)):
            text(d, (cx, BOT - BH - 40), s, 40, col, alpha=alpha)
    text(d, ((BX[0] + BX[1]) / 2, BOT + 104), "đơn vị: J", 36, MUTED, alpha=alpha)

def vbadge(d, s, ang, alpha=1.0):
    x, y = 950, 420                                          # co dinh tren hai cot, khong de thuoc/ghe
    card(d, (x - 125, y - 32, x + 125, y + 32), fill=A(WHITE, alpha), outline=A(DGREEN, alpha), r=20, w=3)
    text(d, (x, y), s, 38, DGREEN, alpha=alpha)

# ---------------- canh: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    frame_sw(d)
    k1 = appear(t, 1.2, 0.5)
    swing(d, A_HALF, alpha=k1, ghost=True)
    if k1 > 0:
        sx, sy = seat_pos(A_HALF)
        dashed(d, (sx + 64, sy), (RX - 14, sy), A(ORANGE, k1), w=3, on=10, off=8)
        text(d, (sx - 70, sy + 4), "?", 56, PURPLE, anchor="rm", alpha=k1)
    swing(d, A0)
    sx, sy = seat_pos(A0)
    dashed(d, (sx + 64, sy), (RX - 14, sy), MUTED, w=3, on=10, off=8)
    dashed(d, (PIV[0] - 120, BOT), (RX - 14, BOT), MUTED, w=3, on=10, off=8)
    ruler(d, hl=0.25 if k1 > 0.5 else None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 235, "Ghế xuống tới nửa độ cao (0,25 m).\nĐộng năng lúc đó bằng mấy phần\nthế năng lúc ở trên cao?", 46, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 410, 940, y0 + 422], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 410, 140 + 800 * (1 - p), y0 + 422], radius=6, fill=A(PURPLE, a))

# ---------------- canh: Tien hanh - mot lan tha, dung hinh hai moc ----------------
REL, FZ = 1.0, 2.8                               # luc tha; thoi gian dung hinh o moc 0,25 m
def do_state(t):
    """-> (goc, moc dang dung hinh: 0 tren cao / 1 giua / 2 day / None dang chay). Mot nguon cho ghe, cot, so."""
    if t < REL: return A0, 0
    tr = t - REL
    if tr < T_HALF: return ang_at(tr), None
    if tr < T_HALF + FZ: return A_HALF, 1
    tr -= FZ
    if tr < T_BOT: return ang_at(tr), None
    return 0.0, 2

def s_do(img, d, t, sc):
    ang, mk = do_state(t)
    frame_sw(d)
    dashed(d, (PIV[0] - 120, BOT), (RX - 14, BOT), MUTED, w=3, on=10, off=8)
    swing(d, ang)
    hv = MARKS[mk][0] if mk is not None else None
    ruler(d, hl=hv)
    et = M_KG * G * h_of(ang)
    if mk is not None: et = float(MARKS[mk][1])
    bars(d, min(196, et), nums=(MARKS[mk][1], MARKS[mk][2]) if mk in (0, 2) else None)   # moc 0,25 m: de trong, hien o Ket qua
    if mk is not None:
        vbadge(d, "v = " + MARKS[mk][3] + (" m/s" if mk else ""), ang)
        if mk == 1 or mk == 2:
            text(d, (W / 2 + 80, 1070), "dừng hình", 38, MUTED)
    text(d, (W / 2, 1130), "m = 40 kg · g = 9,8 m/s² · số minh hoạ", 38, MUTED)

# ---------------- canh: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · một nửa"
    pw = tw(d, lab, F(44)) + 56
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 366), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 333), lab, 44, WHITE, alpha=ka)
    frame_sw(d)
    dashed(d, (PIV[0] - 120, BOT), (RX - 14, BOT), MUTED, w=3, on=10, off=8)
    swing(d, A_HALF)
    ruler(d, hl=0.25)
    bars(d, 98.0, nums=("98", "98"))
    k1 = appear(t, M[0] + 0.9, 0.4)
    if k1 > 0:
        card(d, (60, 1030, 1020, 1160), fill=A((255, 237, 213), k1), outline=A(ORANGE, k1), r=20, w=3)
        eq(d, W / 2, 1095, "E_{đ} = 40·9,8·(0,50 − 0,25) = 98 J", 46, ORANGE, alpha=k1)
    k2 = appear(t, M[1] + 0.3, 0.4)
    if k2 > 0:
        card(d, (60, 1200, 1020, 1330), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=20, w=3)
        eq(d, W / 2, 1265, "E_{t} + E_{đ} = 98 + 98 = 196 J", 46, DGREEN, alpha=k2)

# ---------------- canh: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    kc = appear(t, M[0] + 1.6, 0.5)
    frame_sw(d)
    swing(d, A0)
    ruler(d, hl=0.50)
    bars(d, 196.0, nums=("196", "0"))
    vbadge(d, "v = 0", A0)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 440), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        yy = y0 + 180
        s = "Đu dừng, v = 0 → hết năng lượng"
        lw = tw(d, s, F(46))
        text(d, (W / 2 - 20, yy), s, 46, DRED, alpha=a1)
        text(d, (W / 2 + lw / 2 + 16, yy), "✗", 46, DRED, alpha=a1)
        if kc > 0:
            d.line([(W / 2 - 20 - lw / 2 - 6, yy + 4), (W / 2 - 20 - lw / 2 - 6 + (lw + 12) * kc, yy + 4)], fill=A((140, 15, 15), a1), width=6)
            eq(d, W / 2, y0 + 320, "✓ v = 0 nhưng E_{t} = mgh = 196 J", 48, DGREEN, alpha=a1 * kc)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Ma sát, lực cản: đã bỏ qua", "• Không coi là dao động điều hoà")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 180 + j * 110), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh: Chot + cau hoi tu nho lai ----------------
END_M0 = 0.4
def _end_body(d, t, k1):
    kq = appear(t, END_M0 + 0.4, 0.5) * k1
    if kq > 0:                                     # hai cot do cao: 0,50 m va 1,0 m (dieu kien), toc do: 3,13 va ?
        base = 1220; s = 200
        for bx, hv, lab, vlab in ((260, 0.5, "0,50 m", ""), (620, 0.10, "0,10 m", "E_{đ} = ?")):
            h = hv * 2 * s
            if h > 2: d.rectangle([bx, base - h, bx + 90, base], fill=A(CET, kq), outline=A(NAVY, kq), width=3)
            text(d, (bx + 45, base - h - 30), lab, 40, CET, alpha=kq)
            eq(d, bx + 120, base - 40, vlab, 40, PURPLE if "?" in vlab else INK, alpha=kq, anchor="l")
    kh = appear(t, END_M0 + 0.4 + 2.5, 0.5) * k1
    if kh > 0:
        card(d, (110, 1300, 970, 1520), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1350), "Gợi ý", 38, MUTED, bold=False, alpha=kh)
        eq(d, W / 2, 1440, "Thế năng đã giảm bao nhiêu?", 42, ORANGE, alpha=kh)

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Bỏ ma sát: thế năng giảm bao nhiêu,\nđộng năng tăng bấy nhiêu.",
             "Ghế cách đáy 0,10 m.\nĐộng năng lúc đó bao nhiêu?", goi_y=None, body=_end_body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, dv, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (dv["t0"] + 0.1, "ding"), (dv["t0"] + REL, "tap"),
            (dv["t0"] + REL + T_HALF, "tap"), (dv["t0"] + REL + FZ + T_BOT, "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l11-conangdddh-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Cơ năng dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xích đu trên cao", draw=s_hook, tail=0.9, caps=[
   ("Ghế dừng trên cao, cách đáy 0,50 m.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Thả ghế xuống", draw=s_do, tail=0.6, caps=[
   ("Thả ghế, dừng hình ở hai mốc.", 4.6),
   ("Thế năng giảm, động năng tăng.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Nửa độ cao: mỗi phần 98 J.", 3.8),
   ("Tổng vẫn là 196 J.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.0, caps=[
   ("Bẫy: đu dừng là hết năng lượng.", 5.4),
   ("Số minh hoạ, tính từ mô hình.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.6, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])
