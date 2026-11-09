# Clip: tn-l11-baitapnangluong-02 - Xich du o san truong: co nang va toc do qua day (9/11/2026, vi_du)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapnangluong-02.json:
#   tham_so: l = 2,0 m ; alpha0 5..45 do ; m = 40 kg (co_dinh) ; mo_hinh h = l(1 - cos a0), W = mgh, v = can(2gh), g = 9,8.
#   so_lieu_mau (a0 do, h m, W J, v m/s): 10 0,03 11,9 0,77 ; 20 0,121 47,3 1,54 ; 30 0,268 105,0 2,29 (ghi chu: tinh tu mo hinh).
#   hien_tuong_hay_sai[0]: dung cos a0 thay cho 1 - cos a0 -> canh bay (hinh hoc: l.cos a0 la doan tu diem treo xuong ghe).
#   Du doan: a0 tu 10 len 30 do, toc do qua day gap may lan? Dap an khoang 3 (2,29 : 0,77). Lua chon (khung ben canh):
#     khoang 1,7 / khoang 3 / khoang 9 / khong doi. KHAC Du doan mo bai (5 -> 10 do, co nang gap may) va KHAC clip
#     btnangluong1 (lo xo, W theo A).
#   Cau chot: ban nang hon, cung goc 30 do -> toc do qua day doi khong? (khong doi: v = can(2gh) khong co m; khong hien).
#   Doan sau hop: Cau 4 (l = 0,8 m, 45 do, g = 10) -> clip khong dung 0,8 m / 45 do, khong tinh v cho ca nay.
# Dan canh (khac conangdddh2 cung xich du): nhin ngang, BA LAN DAY 10/20/30 do + dien thoai do goc + BANG 4 cot;
#   dap an so sanh hang 10 va 30 do; bay ve hinh hoc l.cos a0 / h tren chinh xich du. Khong co cot nang luong song.
# Chuyen dong (hoat canh): a = a0 cos(2 pi tau / T), T = 2 pi can(l/g) = 2,84 s (chieu that).
from engine import *

ROWS = [(10, "10°", "0,03", "11,9", "0,77"), (20, "20°", "0,121", "47,3", "1,54"), (30, "30°", "0,268", "105,0", "2,29")]
L_M, G = 2.0, 9.8
TS = 2 * math.pi * math.sqrt(L_M / G)        # 2,84 s
PIV = (360, 330); LPX = 520                  # 260 px / m
DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55)
SEAT = (234, 88, 12); SKIN = (240, 190, 150); SHIRT = (37, 99, 235)

_TI = {}
def TI(size):                                # Times Bold Italic cho alpha va l (SF: alpha giong a, l giong I)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """'α' va '{l}' ve bang Times Bold Italic; _{..} chi so duoi, ^{..} so mu (>= 36 px)."""
    fs = []
    for p in [p for p in re.split(r"(α|\{l\}|_\{[^}]*\}|\^\{[^}]*\})", s) if p]:
        if p == "α": fs.append((p, TI(size * 1.1), 0))
        elif p == "{l}": fs.append(("l", TI(size * 1.1), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(max(36, size * 0.62)), size * 0.26))
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

# ---------------- xich du nhin ngang ----------------
def frame_sw(d, piv=PIV, L=LPX, alpha=1.0):
    c = lambda col: A(col, alpha)
    fy = piv[1] + L + 120                                    # mat san; khung chu A nhin doc xa ngang
    for sgn in (-1, 1):
        d.line([piv, (piv[0] + sgn * 430, fy)], fill=c(GRAY), width=12)
    d.line([(0, fy), (piv[0] + 520, fy)], fill=c(MUTED), width=4)
    dot(d, piv[0], piv[1], 16, c(GRAY), outline=c(NAVY))

def seat_pos(ang, piv=PIV, L=LPX):
    return (piv[0] + L * math.sin(ang), piv[1] + L * math.cos(ang))

def swing(d, ang, piv=PIV, L=LPX, alpha=1.0, ghost=False, seat_col=SEAT):
    """ang (rad), duong = lech sang phai. Day + ghe + nguoi ngoi (than doc theo day)."""
    c = lambda col: A(col, alpha)
    sx, sy = seat_pos(ang, piv, L)
    d.line([piv, (sx, sy)], fill=c(NAVY), width=5)
    seat = rot([(sx - 60, sy), (sx + 60, sy), (sx + 60, sy + 16), (sx - 60, sy + 16)], (sx, sy), -ang)
    d.polygon(seat, fill=c(seat_col if not ghost else LIGHT), outline=c(NAVY))
    if ghost: return
    body = rot([(sx - 22, sy - 96), (sx + 22, sy - 96), (sx + 22, sy - 4), (sx - 22, sy - 4)], (sx, sy), -ang)
    d.polygon(body, fill=c(SHIRT))
    hx, hy = rot([(sx, sy - 128)], (sx, sy), -ang)[0]
    d.ellipse([hx - 28, hy - 28, hx + 28, hy + 28], fill=c(SKIN), outline=c(NAVY), width=3)
    leg = rot([(sx + 4, sy + 2), (sx + 56, sy + 4), (sx + 66, sy + 60)], (sx, sy), -ang)
    d.line(leg, fill=c(NAVY), width=12, joint="curve")
    dot(d, piv[0], piv[1], 9, c(NAVY))

def angle_arc(d, a_deg, col, alpha=1.0, r=150, lab=None, piv=PIV, lab_xy=None):
    d.arc([piv[0] - r, piv[1] - r, piv[0] + r, piv[1] + r], 90 - a_deg, 90, fill=A(col, alpha), width=5)
    if lab and lab_xy: text(d, lab_xy, lab, 42, col, anchor="lm", alpha=alpha)

def phone(d, val, x0=720, y0=340, alpha=1.0):
    card(d, (x0, y0, x0 + 280, y0 + 300), fill=A(NAVY, alpha), r=28)
    d.rounded_rectangle([x0 + 14, y0 + 18, x0 + 266, y0 + 282], radius=16, fill=A((40, 52, 90), alpha))
    text(d, (x0 + 140, y0 + 75), "đo góc", 36, (200, 210, 235), alpha=alpha)
    text(d, (x0 + 140, y0 + 165), val, 72, WHITE, alpha=alpha)
    text(d, (x0 + 140, y0 + 245), "lớn nhất", 36, (200, 210, 235), alpha=alpha)

TBX = [140, 360, 600, 860]; TBY = 1090; TBH = 72
def table(d, n_a, n_hw, n_v, hl=None, alpha=1.0, y0=TBY):
    card(d, (40, y0 - 70, 1040, y0 + TBH * 3 + 20), fill=A(WHITE, alpha), outline=A(NAVY, alpha), r=18, w=3)
    for cx, hd in zip(TBX, ("α", "h (m)", "W (J)", "v (m/s)")):
        if hd == "α": eq(d, cx, y0 - 30, "α_{0}", 42, INK, alpha=alpha)
        else: text(d, (cx, y0 - 30), hd, 40, INK, alpha=alpha)
    d.line([(56, y0 + 4), (1024, y0 + 4)], fill=A(NAVY, alpha), width=3)
    for j in range(3):
        y = y0 + TBH * (j + 0.5) + 10
        if hl is not None and j in hl: d.rounded_rectangle([52, y - 30, 1028, y + 30], radius=10, fill=A((255, 237, 213), alpha))
        _, al, hh, ww, vv = ROWS[j]
        if j < n_a: text(d, (TBX[0], y), al, 42, INK, alpha=alpha)
        if j < n_hw:
            text(d, (TBX[1], y), hh, 42, DBLUE, alpha=alpha)
            text(d, (TBX[2], y), ww, 42, DBLUE, alpha=alpha)
        if j < n_v: text(d, (TBX[3], y), vv, 42, DGREEN, alpha=alpha)

# ---------------- canh: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    frame_sw(d)
    k1 = appear(t, 0.6, 0.6); k2 = appear(t, 1.4, 0.6)
    swing(d, math.radians(10), alpha=0.45 * k1, seat_col=DBLUE)
    angle_arc(d, 10, DBLUE, k1, r=200, lab="10°", lab_xy=(425, 915))
    swing(d, math.radians(30) * ease((t - 1.4) / 0.8))
    angle_arc(d, 30, ORANGE, k2, r=320, lab="30°", lab_xy=(720, 830))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 235, "Góc lệch lớn nhất tăng từ 10° lên 30°.\nTốc độ qua chỗ thấp nhất gấp mấy lần?", 48, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 412], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 412], radius=6, fill=A(PURPLE, a))

# ---------------- canh: Tien hanh - ba lan day ----------------
RS0, PULL, HOLD, RUNS = 0.5, 0.6, 0.5, 1.6
RD = PULL + HOLD + RUNS                       # 2,7 s moi lan
def sw_state(t):
    """-> (i lan, goc rad, da tha, da qua day). Mot nguon cho ghe, dien thoai, bang."""
    if t < RS0: return -1, 0.0, False, False
    i = min(2, int((t - RS0) // RD)); s = t - RS0 - i * RD
    a0 = math.radians(ROWS[i][0])
    if s < PULL + HOLD:
        prev = 0.0 if i == 0 else math.radians(ROWS[i - 1][0]) * math.cos(2 * math.pi * RUNS / TS)
        return i, lerp(prev, a0, ease(s / PULL)), False, False
    tau = s - PULL - HOLD
    return i, a0 * math.cos(2 * math.pi * tau / TS), True, tau >= TS / 4

def s_do(img, d, t, sc):
    i, ang, rel, past = sw_state(t)
    frame_sw(d)
    by = PIV[1] + LPX                                        # muc ghe thap nhat
    dashed(d, (PIV[0] - 120, by), (PIV[0] + 300, by), MUTED, w=3, on=10, off=8)
    swing(d, ang)
    if i >= 0:
        a0d = ROWS[i][0]
        hold = (t - RS0 - i * RD) >= PULL
        if hold:
            angle_arc(d, a0d, ORANGE, 1.0 if not rel else 0.5, r=220)
            if not rel:                                      # h cua lan nay (ghe dang giu o bien)
                sx, sy = seat_pos(math.radians(a0d))
                d.line([(sx + 80, sy), (sx + 80, by)], fill=DBLUE, width=5)
                for yy in (sy, by): d.line([(sx + 66, yy), (sx + 94, yy)], fill=DBLUE, width=5)
                text(d, (sx + 110, (sy + by) / 2 + 4), "h", 42, DBLUE, anchor="lm")
        phone(d, ROWS[i][1] if hold else "…")
    else:
        phone(d, "…")
    n_a = i + 1 if i >= 0 and (t - RS0 - i * RD) >= PULL else max(0, i)
    n_hw = n_a
    n_v = 0                                                  # v de trong: HS tu tinh, hien o Ket qua
    table(d, n_a, n_hw, n_v, hl=[i] if i >= 0 else None)
    text(d, (W / 2, TBY + TBH * 3 + 70), "m = 40 kg · dây 2,0 m · số minh hoạ", 38, MUTED)

# ---------------- canh: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · khoảng 3 lần"
    pw = tw(d, lab, F(44)) + 56
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 366), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 333), lab, 44, WHITE, alpha=ka)
    kv = appear(t, M[1] + 1.4, 0.4)
    table(d, 3, 3, 3 if kv > 0.5 else 0, hl=[0, 2], y0=500)
    kc = kv
    if kc > 0:
        for j in (0, 2):
            y = 500 + TBH * (j + 0.5) + 10
            d.ellipse([TBX[3] - 80, y - 34, TBX[3] + 80, y + 34], outline=A(DRED, kc), width=5)
    k2 = appear(t, M[0] + 1.0, 0.4)
    if k2 > 0:
        for j in (0, 2):
            y = 500 + TBH * (j + 0.5) + 10
            d.ellipse([TBX[2] - 90, y - 34, TBX[2] + 90, y + 34], outline=A(DBLUE, k2), width=5)
        card(d, (60, 830, 1020, 960), fill=A((239, 246, 255), k2), outline=A(DBLUE, k2), r=20, w=3)
        text(d, (W / 2, 895), "W: 105,0 : 11,9 ≈ 9", 52, DBLUE, alpha=k2)
    k1 = appear(t, M[1] + 1.4, 0.4)
    if k1 > 0:
        card(d, (60, 1000, 1020, 1130), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=20, w=3)
        text(d, (W / 2, 1065), "v: 2,29 : 0,77 ≈ 3", 52, DRED, alpha=k1)
    k3 = appear(t, M[1] + 2.6, 0.4)
    if k3 > 0:
        card(d, (60, 1170, 1020, 1300), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=20, w=3)
        text(d, (W / 2, 1235), "v = √(2gh): W gấp 9, v gấp √9", 46, DGREEN, alpha=k3)

# ---------------- canh: Bay roi Chua noi duoc ----------------
BPIV = (360, 330)
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    kc = appear(t, M[0] + 1.4, 0.5)
    a0 = math.radians(30)
    by = BPIV[1] + LPX
    sx, sy = seat_pos(a0, BPIV)
    dashed(d, BPIV, (BPIV[0], by), MUTED, w=3)
    swing(d, 0.0, BPIV, ghost=True)
    swing(d, a0, BPIV)
    dashed(d, (BPIV[0], sy), (sx, sy), MUTED, w=3)
    angle_arc(d, 30, ORANGE, 1.0, r=150, piv=BPIV)
    eq(d, BPIV[0] + 16, BPIV[1] + 215, "α_{0}", 40, ORANGE, anchor="l")
    xr = BPIV[0] - 60                                       # doan l.cos a0 (do) va h (xanh) ben trai truc dung
    d.line([(xr, BPIV[1]), (xr, sy)], fill=A(DRED, a1 + k2 * 0.4), width=6)
    for yy in (BPIV[1], sy): d.line([(xr - 14, yy), (xr + 14, yy)], fill=A(DRED, a1 + k2 * 0.4), width=6)
    eq(d, xr - 20, (BPIV[1] + sy) / 2, "{l}·cos α_{0}", 40, DRED, alpha=a1 + k2 * 0.4, anchor="r")
    if kc > 0:
        d.line([(xr, sy), (xr, by)], fill=A(DGREEN, kc), width=6)
        for yy in (sy, by): d.line([(xr - 14, yy), (xr + 14, yy)], fill=A(DGREEN, kc), width=6)
        text(d, (xr - 20, (sy + by) / 2), "h", 46, DGREEN, anchor="rm", alpha=kc)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 440), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        yy = y0 + 180
        lw = eq(d, W / 2, yy, "h = {l}·cos α_{0}", 52, DRED, alpha=a1)
        text(d, (W / 2 + lw / 2 + 40, yy), "✗", 52, DRED, alpha=a1)
        if kc > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * kc, yy + 4)], fill=A((140, 15, 15), a1), width=6)
            eq(d, W / 2, y0 + 320, "✓ h = {l}(1 − cos α_{0})", 52, DGREEN, alpha=a1 * kc)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Ma sát: bỏ qua trong một lượt", "• Người + ghế coi là một điểm")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 180 + j * 110), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh: Chot + cau hoi tu nho lai ----------------
END_M0 = 0.4
def _end_body(d, t, k1):
    kq = appear(t, END_M0 + 0.4, 0.5) * k1
    if kq > 0:                                              # hai ban, cung goc 30 do (dieu kien, khong dap so)
        for cx, lab, sz in ((330, "40 kg", 1.0), (750, "nặng hơn", 1.25)):
            dot(d, cx, 1080, int(34 * sz), A(SHIRT, kq))
            dot(d, cx, 1080 - int(58 * sz), int(22 * sz), A(SKIN, kq), outline=A(NAVY, kq))
            text(d, (cx, 1170), lab, 40, INK, alpha=kq)
    kh = appear(t, END_M0 + 0.4 + 2.5, 0.5) * k1
    if kh > 0:
        card(d, (110, 1300, 970, 1520), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1350), "Gợi ý", 38, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1440), "Biểu thức của v còn m không?", 42, ORANGE, alpha=kh)

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Góc lớn hơn thì h lớn hơn:\nW và v qua đáy đều tăng.",
             "Bạn nặng hơn, cùng góc 30°.\nTốc độ qua đáy đổi không?", goi_y=None, body=_end_body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, dv, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (dv["t0"] + 0.1, "ding")] + [
            (dv["t0"] + RS0 + j * RD + PULL + HOLD, "tap") for j in range(3)] + [
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l11-baitapnangluong-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Năng lượng dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xích đu, hai góc đẩy", draw=s_hook, tail=0.9, caps=[
   ("Cùng xích đu, cùng bạn ngồi.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.4)]),
 dict(key="do", title="Ba lần đẩy rồi thả", draw=s_do, tail=0.6, caps=[
   ("Đẩy tới 10°, 20°, 30° rồi thả.", 4.4),
   ("Tính h và W mỗi lần.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=1.4, caps=[
   ("So hàng 10° với hàng 30°.", 3.6),
   ("W gấp 9, còn v gấp mấy?", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.0, caps=[
   ("Bẫy: lấy cos thay cho 1 − cos.", 4.8),
   ("Số tính từ mô hình, minh hoạ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.8, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])
