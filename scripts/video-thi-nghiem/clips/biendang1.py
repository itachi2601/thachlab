# Clip: tn-l10-biendang-01 - Lo xo but bi: bien dang dan hoi va bien dang deo (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-biendang-01.json:
#   tham_so k = 200 N/m (0,5 cm moi N), F_gh = 4 N, l0 = 4,0 cm ; so_lieu_mau F = 1 / 3 N -> dl 0,5 / 1,5 cm, tha ve
#   dung chieu dai cu ; 6 N: dang keo dai 9,5 cm (l_keo_6N), tha ra dai 6,5 cm (l_tha_6N).
# Du doan (K10, khong ve nut A-D, khung ben canh co lua chon): keo 6 N roi tha, lo xo dai bao nhieu?
#   A. ve dung 4,0 cm ; B. dai hon 4,0 cm, khong ve (DUNG) ; C. ngan hon 4,0 cm.
# Bay = hien_tuong_hay_sai[1] (chi vat mem nhu dat nan moi bien dang deo): hai hinh canh nhau - dat nan bep, kep giay
#   thep be cong - ca hai tha ra KHONG ve (khong lap cap so 6 N / 6,5 cm cua Du doan).
# Chot (ca tu suy, ghi_chu kho): lo xo MOI cung loai, keo 1,5 N -> dai 4,0 + 1,5 . 0,5 = 4,75 cm (v2: doi so tranh gan quiz bai). So 1,5 N va 4,75
#   khong hien truoc; can 2 buoc (dan moi N tu bang, cong l0).
from engine import *

K_CM = 0.5                                       # cm moi N (k = 200 N/m)
L0, F_GH = 4.0, 4.0
ROWS = [(1, 4.5, 4.0), (3, 5.5, 4.0), (6, 9.5, 6.5)]   # (F N, dai khi dang keo cm, dai sau khi tha cm)
L_DU = 6.5
FMAX = 8.0
NOTE = (60, 64, 84); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
def vn(x, n=1): return f"{x:.{n}f}".replace(".", ",")

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

def l_model(f, peak, loading):
    """Chieu dai (cm) khi luc f, lan keo co luc lon nhat peak."""
    if peak <= F_GH: return L0 + K_CM * f
    if loading: return L0 + K_CM * f if f <= F_GH else L0 + K_CM * F_GH + (f - F_GH) * 1.75
    return L_DU + K_CM * f                       # tha: co lai dan hoi theo cung k

# ---------------- bo cuc ----------------
X0, SY, PX = 92, 520, 56                          # dau trai lo xo (vach 0), truc lo xo, px moi cm
RY = 610                                         # mep tren thuoc
def xl(l): return X0 + l * PX

def spring_at(d, x0, xe, y, alpha=1.0, n=13, amp=22, w=5, col=NAVY):
    lead = 12
    pts = [(x0, y), (x0 + lead, y)]
    for i in range(1, 2 * n):
        pts.append((lerp(x0 + lead, xe - lead, i / (2 * n)), y + (amp if i % 2 else -amp)))
    pts += [(xe - lead, y), (xe, y)]
    d.line(pts, fill=A(col, alpha), width=w, joint="curve")

def clamp_wall(d, alpha=1.0):
    d.rounded_rectangle([40, SY - 90, X0 - 4, SY + 90], radius=8, fill=A((150, 155, 172), alpha))
    for y in range(SY - 80, SY + 90, 26): d.line([(40, y + 18), (X0 - 8, y)], fill=A((120, 125, 140), alpha), width=3)

def ruler(d, alpha=1.0):
    d.rectangle([X0 - 14, RY, xl(10) + 14, RY + 64], fill=A((255, 241, 205), alpha), outline=A((140, 100, 40), alpha), width=3)
    for k in range(101):
        x = X0 + k * PX / 10; L = 30 if k % 10 == 0 else (20 if k % 5 == 0 else 10)
        d.line([(x, RY), (x, RY + L)], fill=A(NAVY, alpha), width=3 if k % 10 == 0 else 2)
    for c in range(0, 11, 2): text(d, (xl(c), RY + 105), str(c), 56, INK, alpha=alpha)
    text(d, (xl(10) + 110, RY + 105), "cm", 56, INK, alpha=alpha)

def marker(d, l, col=RED, alpha=1.0):
    x = xl(l)
    for y in range(SY + 30, RY, 16): d.line([(x, y), (x, y + 8)], fill=A(col, alpha), width=4)
    d.polygon([(x, RY + 2), (x - 11, RY - 16), (x + 11, RY - 16)], fill=A(col, alpha))

def rig(d, l, f_read, alpha=1.0, gap=0.0):
    clamp_wall(d, alpha); ruler(d, alpha)
    xe = xl(l); spring_at(d, X0, xe, SY, alpha=alpha, amp=24)
    Q = lambda s, h: (xe + gap + s, SY + h)
    luc_ke(d, Q, 0, 22, 352, FMAX, f_read, nho=0.5, so=(0, 3, 6), hw=42, ben=-1, alpha=alpha, co=62)
    marker(d, l, alpha=alpha)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    text(d, (W / 2, 300), "Chưa kéo: dài 4,0 cm", 60, INK)
    rig(d, L0, 0.0, gap=140 * (1 - ease((t - 0.5) / 1.2)))     # luc ke truot vao moc lo xo
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 180), "Kéo 6 N rồi thả ra.", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "Lò xo dài bao nhiêu?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 380, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: tien hanh ----------------
UP = (1.0, 1.0, 1.5)                              # thoi gian keo len moi lan
HOLD, DOWN, SET = 1.0, 0.7, 0.15
def plan(sc):
    """-> [(bat dau, het keo, het giu, het tha)] theo moc phu de."""
    out = []
    for i in range(3):
        a = sc["M"][i] + 0.15; b = a + UP[i]; c = b + HOLD; e = c + DOWN
        out.append((a, b, c, e))
    return out

def do_state(t, sc):
    """-> (f, l, o bang da ghi [(hang, cot)], on dinh?, lan keo hien tai)."""
    P = plan(sc); f, l, cells, steady, cur = 0.0, L0, [], True, -1
    for i, (a, b, c, e) in enumerate(P):
        F0 = ROWS[i][0]
        if t < a: break
        cur = i
        if t < b:   f = F0 * ease((t - a) / (b - a)); l = l_model(f, F0, True); steady = False
        elif t < c: f = F0; l = l_model(f, F0, True); steady = t >= b + SET
        elif t < e: f = F0 * (1 - ease((t - c) / (e - c))); l = l_model(f, F0, False); steady = False
        else:       f = 0.0; l = l_model(0.0, F0, False); steady = t >= e + SET
        if t >= b + SET: cells.append((i, 1))
        if t >= e + SET: cells.append((i, 2))
    return f, l, cells, steady, cur

def table(d, cells, hl=None, a=1.0, y0=820):
    card(d, (40, y0, 1040, y0 + 520), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (W / 2, y0 + 55), "Chiều dài lò xo (cm)", 58, NAVY, alpha=a)
    xs = (190, 520, 860)
    for x, s in zip(xs, ("lực", "đang kéo", "đã thả")): text(d, (x, y0 + 140), s, 56, NOTE, alpha=a)
    d.line([(60, y0 + 185), (1020, y0 + 185)], fill=A(LIGHT, a), width=4)
    for i, (f, l1, l2) in enumerate(ROWS):
        y = y0 + 250 + i * 95
        if hl == i: d.rounded_rectangle([56, y - 44, 1024, y + 44], radius=16, fill=A((254, 226, 226), a))
        if any(r == i for r, _ in cells): text(d, (xs[0], y), f"{f} N", 60, BLUE, alpha=a)
        if (i, 1) in cells: text(d, (xs[1], y), vn(l1), 60, INK, alpha=a)
        if (i, 2) in cells: text(d, (xs[2], y), vn(l2), 60, RED if l2 != L0 else INK, alpha=a)

def t_dapan(sc): return plan(sc)[2][3] + SET + 0.3

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    f, l, cells, steady, cur = do_state(t, sc)
    rig(d, l, f)
    ta = t_dapan(sc)
    table(d, cells, hl=2 if t >= ta else None)
    k = appear(t, ta, 0.4)
    if k > 0:
        card(d, (40, 1370, 1040, 1500), fill=A(NAVY, k), r=30)
        text(d, (W / 2, 1435), "Dài hơn 4,0 cm: không về", 60, WHITE, alpha=k)

def _kiem_dong_bo():
    """Moi 0,05 s: lo xo on dinh = mo hinh = hang bang ; o bang chi hien khi on dinh ; kho khop k."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        f, l, cells, steady, cur = do_state(t, sc)
        if steady and cur >= 0:
            want = ROWS[cur][1] if f > 0 else ROWS[cur][2]
            if abs(l - want) > 1e-6: bad.append(("lech", round(t, 2)))
            if f > 0 and (cur, 1) not in cells: bad.append(("chua ghi", round(t, 2)))
        t += 0.05
    P = plan(sc)
    for i, (a, b, c, e) in enumerate(P):
        if e + SET > (sc["M"][i + 1] if i + 1 < len(sc["M"]) else sc["T"]): bad.append(("tran", i))
    if t_dapan(sc) + 2.4 > sc["T"] + 1e-6: bad.append("dap an sat cuoi")
    for f, l1, _ in ROWS[:2]:
        if abs(L0 + f * 100 / 200 - l1) > 1e-6: bad.append(("k", f))
    if xl(ROWS[2][1]) + 352 + 40 > 1060: bad.append("luc ke tran mep")
    return bad

# ---------------- canh 3: hai ket cuc ----------------
def mini(d, x0, y, l, alpha, ghost=None):
    """Lo xo nho dung ti le PX/cm + vach chieu dai cu (net dut)."""
    d.rounded_rectangle([x0 - 26, y - 46, x0 - 2, y + 46], radius=6, fill=A((150, 155, 172), alpha))
    spring_at(d, x0, x0 + l * PX, y, alpha=alpha)
    if ghost is not None:
        xg = x0 + ghost * PX
        for yy in range(y - 60, y + 64, 18): d.line([(xg, yy), (xg, yy + 9)], fill=A(RED, alpha), width=4)
        text(d, (xg, y + 95), "4,0 cm", 55, RED, alpha=alpha)

def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2)
    card(d, (40, 300, 1040, 640), fill=A(WHITE, a), outline=A(GREEN, a), w=5)
    text(d, (W / 2, 370), "1 N, 3 N: thả ra còn 4,0 cm", 58, INK, alpha=a)
    mini(d, 120, 520, L0, a)
    text(d, (120 + L0 * PX + 70, 520), "Đàn hồi", 64, GREEN, anchor="lm", alpha=a)
    b = appear(t, M[1] + 0.1, 0.4)
    if b > 0:
        card(d, (40, 680, 1040, 1060), fill=A(WHITE, b), outline=A(RED, b), w=5)
        text(d, (W / 2, 750), "6 N: thả ra còn 6,5 cm", 58, INK, alpha=b)
        mini(d, 120, 900, L_DU, b, ghost=L0)
        text(d, (120 + L_DU * PX + 50, 900), "Dẻo", 64, RED, anchor="lm", alpha=b)

# ---------------- canh 4: bay + chua noi duoc ----------------
def clay(d, cx, cy, k, a):
    """Cuc dat nan: k = 0 tron, k = 1 bep (giu nguyen sau khi bo tay)."""
    rx, ry = lerp(90, 150, k), lerp(90, 45, k)
    d.ellipse([cx - rx, cy + 90 - 2 * ry, cx + rx, cy + 90], fill=A((248, 180, 120), a), outline=A((190, 110, 50), a), width=4)
    d.line([(cx - 190, cy + 92), (cx + 190, cy + 92)], fill=A(NOTE, a), width=5)

def clip_wire(d, cx, cy, ang, a, ghost=True):
    """Kep giay thep duoi thang: nua phai be quanh diem giua mot goc ang (do)."""
    L = 150; p0 = (cx - L, cy); pm = (cx, cy)
    r = math.radians(ang); p1 = (cx + L * math.cos(r), cy - L * math.sin(r))
    if ghost:
        for i in range(8):
            x = cx + i * 20
            d.line([(x, cy), (x + 10, cy)], fill=A(GRAY, a), width=5)
        text(d, (cx + 95, cy + 45), "lúc đầu", 55, NOTE, alpha=a)
    d.line([p0, pm, p1], fill=A((90, 100, 120), a), width=12, joint="curve")

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k0 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3)
    if a1 > 0:
        card(d, (40, 290, 1040, 540), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, 360, "BẪY", RED, a1)
        q = "“Chỉ vật mềm mới bị dẻo”"
        ks = clamp((t - M[1]) / 0.4); f = F(60); lw = tw(d, q, f); yy = 470
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kp = appear(t, M[1] + 0.1, 0.4) * (1 - k3)
    if kp > 0:
        # bop / be trong 1,4 s, roi bo tay (mui ten tat) - hinh giu nguyen
        pr = clamp((t - M[1] - 0.3) / 1.4); hold = t < M[1] + 2.0
        for x0 in (40, 550):
            card(d, (x0, 580, x0 + 490, 1030), fill=A(WHITE, kp), outline=A(NAVY, kp), w=4)
        clay(d, 285, 780, ease(pr), kp)
        if hold and pr > 0:
            arrow(d, (285, 610), (285, 700 + 45 * ease(pr) - 20), A(RED, kp), w=8, head=24)
        text(d, (285, 960), "đất nặn", 58, NAVY, alpha=kp)
        clip_wire(d, 795, 820, 55 * ease(pr), kp)
        if hold and pr > 0:
            r = math.radians(55 * ease(pr)); tip = (795 + 150 * math.cos(r), 820 - 150 * math.sin(r))
            arrow(d, (tip[0] + 10, tip[1] - 90), (tip[0] + 2, tip[1] - 14), A(RED, kp), w=8, head=24)
        text(d, (795, 960), "kẹp giấy thép", 58, NAVY, alpha=kp)
    k2 = appear(t, M[1] + 3.0, 0.45) * (1 - k3)
    if k2 > 0:
        card(d, (40, 1070, 1040, 1200), fill=A(WHITE, k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1135), "Cả hai không về", 60, GREEN, alpha=k2)
    if k3 > 0:
        card(d, (40, 290, 1040, 640), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 360, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 500), "Giới hạn: bao nhiêu N?", 60, INK, alpha=k3)
        # thanh luc 0-8 N: vung da thay dan hoi (1-3 N) va deo (6 N), khoang giua bo trong
        x0, x1, y = 120, 960, 820; fx = lambda f: x0 + (x1 - x0) * f / 8
        d.rounded_rectangle([x0, y - 22, x1, y + 22], radius=20, fill=A(LIGHT, k3))
        d.rounded_rectangle([fx(1), y - 22, fx(3), y + 22], radius=20, fill=A(GREEN, k3))
        dot(d, fx(6), y, 26, A(RED, k3))
        for f_ in (1, 3, 6): text(d, (fx(f_), y + 80), f"{f_} N", 56, INK, alpha=k3)
        text(d, (fx(4.5), y - 80), "?", 72, PURPLE, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    x0, y = 170, 560
    d.rounded_rectangle([x0 - 30, y - 56, x0 - 2, y + 56], radius=6, fill=A((150, 155, 172), k))
    spring_at(d, x0, x0 + L0 * PX, y, alpha=k, amp=24)
    xe = x0 + L0 * PX
    arrow(d, (xe, y), (xe + 230, y), A(RED, k), w=9, head=28)
    text(d, (xe + 250, y), "1,5 N", 60, RED, anchor="lm", alpha=k)
    text(d, (x0 + L0 * PX / 2, y + 110), "4,0 cm", 56, NOTE, alpha=k)
    text(d, (W / 2, 820), "Lò xo mới, cùng loại,", 64, INK, alpha=k)
    text(d, (W / 2, 910), "kéo 1,5 N.", 64, INK, alpha=k)
    text(d, (W / 2, 1040), "Lúc kéo, lò xo dài", 64, DORANGE, alpha=k)
    text(d, (W / 2, 1130), "bao nhiêu cm?", 64, DORANGE, alpha=k)
    seg_bar(d, 1320, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    P = plan(do)
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + a_, "tap") for a_, b_, c, e_ in P]
            + [(do["t0"] + t_dapan(do), "ding"), (r["t0"] + r["M"][1] + 0.1, "tap"),
               (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-biendang-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Biến dạng của vật rắn · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lò xo bút bi trên thước", draw=s_hook, tail=0.3, caps=[
   ("Lò xo nằm trên thước.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Kéo rồi thả", draw=s_do, tail=2.6, caps=[
   ("Kéo nhẹ 1 N rồi thả.", 3.1),
   ("Kéo 3 N rồi thả.", 3.1),
   ("Kéo mạnh 6 N rồi thả.", 3.6)]),
 dict(key="rut", title="Hai kết cục", draw=s_rut, tail=0.6, caps=[
   ("Lực nhỏ: thả ra là về.", 3.4),
   ("Lực lớn: thả ra vẫn dài.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.0),
   ("Bóp rồi bỏ tay.", 6.1),
   ("Chưa nói được.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự tính.", 6.0)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
