# Clip: tn-l11-baitapdaodong-02 - Vat dao dong tu ve do thi li do - thoi gian len bang giay (9/11/2026, vi_du)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapdaodong-02.json:
#   tham_so mac dinh: A = 3,0 cm ; T = 0,8 s ; u = 20 cm/s. so_lieu_mau: u 20, h 6,0, d 16,0, A 3,0, T 0,8
#   (ghi chu kho: "So minh hoa tinh tu mo hinh") -> man hinh ghi "số minh hoạ".
#   mo_hinh: x = A cos(2 pi t / T), s = u t, h = 2A, d = u T ; gia_thiet: keo giay deu, bo qua ma sat dau but.
#   hien_tuong_hay_sai[0]: doc dinh-day la A -> Du doan ; hien_tuong_hay_sai[1]: dinh -> day lien ke la T (that ra T/2) -> Bay.
#   Du doan: dinh cao nhat cach day thap nhat 6,0 cm; bien do? Lua chon (khung ben canh): 1,5 / 3,0 / 6,0 / 12 cm. Dap an 3,0.
#   Cau chot: keo giay nhanh hon -> khoang hai dinh va T doi the nao? (d dai ra, T khong doi; khong hien tren man).
#   Doan sau hop trong bai la "Ho 2: quan he x, v, a" (khong lien quan) -> clip duoc tinh A, T nhu rut_ra kho.
# Dan canh: lo xo treo ben phai, but gan qua nang, bang giay chay sang trai phia sau; truc co dinh 25 px/cm ca hai chieu
#   (u = 20 cm/s -> giay chay 500 px/s). Tha tu x = +A dung luc giay bat dau chay; dung sau 4T + T/4 -> dinh o x man 800, 400;
#   day o 600, 200 (khung bang giay giu nguyen o moi canh sau).
from engine import *

PXC = 25                                   # px / cm (ca hai chieu)
A_CM, T_S, U = 3.0, 0.8, 20.0
YC = 700                                   # duong can bang tren giay
PEN = 900                                  # x dau but
TX0, TX1, TY0, TY1 = 110, 930, 530, 870    # bang giay
SPX = U * PXC                              # 500 px/s
R0, RUN = 0.6, 4 * T_S + T_S / 4           # canh tien hanh: bat dau keo; thoi gian chay 3,4 s
DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55)
BLOCK = (250, 204, 120); PAPER = (255, 255, 252); TRACE = (30, 64, 175)

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    fs = []
    for p in [p for p in re.split(r"(_\{[^}]*\}|\^\{[^}]*\})", s) if p]:
        if p.startswith("_{"): fs.append((p[2:-1], F(max(36, size * 0.62)), size * 0.26))
        elif p.startswith("^{"): fs.append((p[2:-1], F(max(36, size * 0.62)), -size * 0.34))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1); n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p0[0], p1[0], a), lerp(p0[1], p1[1], a)), (lerp(p0[0], p1[0], b), lerp(p0[1], p1[1], b))], fill=col, width=w)

def xcm(s): return A_CM * math.cos(2 * math.pi * s / T_S)          # li do (cm, chieu duong huong len)
def ypx(x): return YC - x * PXC

# ---------------- bang giay + net but ----------------
def tape(d, tau, alpha=1.0, moving=False):
    d.rectangle([TX0, TY0, TX1, TY1], fill=A(PAPER, alpha), outline=A(GRAY, alpha), width=3)
    off = (tau * SPX) % 100                                         # vach mo cho thay giay chay
    for k in range(10):
        x = TX1 - 20 - ((k * 100 + off) % 900)
        if TX0 + 6 < x < TX1 - 6:
            d.line([(x, TY1 - 18), (x, TY1 - 6)], fill=A(LIGHT, alpha), width=3)
    if tau <= 0: return
    pts = []
    n = 400
    for i in range(n + 1):
        s = tau * i / n
        x = PEN - SPX * (tau - s)
        if x < TX0 + 4: continue
        pts.append((x, ypx(xcm(s))))
    if len(pts) > 1: d.line(pts, fill=A(TRACE, alpha), width=6, joint="curve")

def coil(d, x, ya, yb, amp=24, n=11, col=NAVY, w=5, alpha=1.0):
    e = 14; pts = [(x, ya), (x, ya + e)]; L = (yb - e) - (ya + e)
    for i in range(1, 2 * n): pts.append((x + (amp if i % 2 else -amp), ya + e + L * i / (2 * n)))
    pts += [(x, yb - e), (x, yb)]
    d.line(pts, fill=A(col, alpha), width=w, joint="curve")

MX = 975                                   # tam qua nang
def hanger(d, x_cm, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([1040, 300, 1062, 1000], fill=c(GRAY), outline=c(NAVY), width=3)        # cot
    d.rectangle([930, 296, 1062, 318], fill=c(GRAY), outline=c(NAVY), width=3)          # xa ngang
    yb = ypx(x_cm)
    coil(d, MX, 318, yb - 46, alpha=alpha)
    d.rounded_rectangle([MX - 48, yb - 46, MX + 48, yb + 46], radius=12, fill=c(BLOCK), outline=c(NAVY), width=4)
    d.polygon([(PEN, yb), (MX - 48, yb - 12), (MX - 48, yb + 12)], fill=c(NAVY))        # but da
    dot(d, PEN, yb, 6, c(TRACE))

def bracket_v(d, x, y0, y1, col, alpha=1.0, w=5):
    d.line([(x, y0), (x, y1)], fill=A(col, alpha), width=w)
    for yy in (y0, y1): d.line([(x - 14, yy), (x + 14, yy)], fill=A(col, alpha), width=w)

def bracket_h(d, x0, x1, y, col, alpha=1.0, w=5):
    d.line([(x0, y), (x1, y)], fill=A(col, alpha), width=w)
    for xx in (x0, x1): d.line([(xx, y - 14), (xx, y + 14)], fill=A(col, alpha), width=w)

def h_mark(d, alpha=1.0, lab="6,0 cm"):
    """Dinh o x man 800, day lien truoc o 600: duong gioi han + ngoac doc o x = 800."""
    yp, yt = ypx(A_CM), ypx(-A_CM)
    dashed(d, (600, yt), (800, yt), A(ORANGE, alpha), w=3, on=10, off=8)
    bracket_v(d, 800, yp, yt, ORANGE, alpha)
    text(d, (782, yt + 38), lab, 40, ORANGE, anchor="rm", alpha=alpha)          # duoi duong day: khong de nét song

def d_mark(d, alpha=1.0, lab="16,0 cm"):
    yb = ypx(A_CM) - 30
    bracket_h(d, 400, 800, yb, DGREEN, alpha)
    for xx in (400, 800): dashed(d, (xx, yb), (xx, ypx(A_CM) - 4), A(DGREEN, alpha), w=3, on=8, off=6)
    text(d, (600, TY0 + 30), lab, 40, DGREEN, alpha=alpha)

def ruler(d, alpha=1.0, y=900):
    d.rectangle([370, y, 830, y + 70], fill=A((250, 240, 200), alpha), outline=A(NAVY, alpha), width=2)
    for k in range(0, 17):
        x = 400 + k * PXC
        L = 26 if k % 4 == 0 else 14
        d.line([(x, y), (x, y + L)], fill=A(NAVY, alpha), width=3 if L == 26 else 2)
    for k in (0, 4, 8, 12, 16): text(d, (400 + k * PXC, y + 50), str(k), 36, INK, alpha=alpha)
    text(d, (850, y + 35), "cm", 36, INK, anchor="lm", alpha=alpha)

# ---------------- canh: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    hanger(d, 0.0)
    tape(d, RUN)
    k = appear(t, 1.2, 0.5)
    if k > 0: h_mark(d, k)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 235, "Đỉnh cao nhất cách đáy thấp nhất 6,0 cm.\nBiên độ dao động bằng bao nhiêu?", 48, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 412], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 412], radius=6, fill=A(PURPLE, a))

# ---------------- canh: Tien hanh ----------------
def s_do(img, d, t, sc):
    M = sc["M"]
    tau = clamp(t - R0, 0, RUN)
    kf = appear(t, R0 + RUN + 0.4, 0.6)                 # thao giay: gia treo mo di
    if t < R0: x = A_CM                                   # giu o +A
    elif t < R0 + RUN: x = xcm(tau)
    else: x = 0.0
    tape(d, tau, moving=True)
    if kf < 1: hanger(d, x, 1 - kf)
    ka = appear(t, 0.2, 0.4) * (1 - kf)
    if ka > 0:                                            # mui ten giay chay
        arrow(d, (560, 470), (340, 470), A(DBLUE, ka), w=6, head=22)
        text(d, (580, 470), "giấy chạy 20 cm/s", 40, DBLUE, anchor="lm", alpha=ka)
    km = appear(t, M[1] + 0.3, 0.5)
    if km > 0:
        ruler(d, km)
        h_mark(d, km)
        kg = appear(t, M[1] + 1.2, 0.5)
        d_mark(d, kg)
        if kg > 0:                                        # giong doc tu hai dinh xuong vach 0 va 16 cua thuoc
            for xx in (400, 800): dashed(d, (xx, ypx(A_CM) + 8), (xx, 900), A(DGREEN, kg), w=3, on=8, off=8)
        text(d, (W / 2, 1060), "số minh hoạ", 36, MUTED, alpha=km)

# ---------------- canh: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · A = 3,0 cm"
    pw = tw(d, lab, F(44)) + 56
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 366), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 333), lab, 44, WHITE, alpha=ka)
    tape(d, RUN)
    dashed(d, (TX0 + 6, YC), (TX1 - 6, YC), MUTED, w=3, on=10, off=8)
    h_mark(d, 1.0, "2A")
    kA = appear(t, 0.8, 0.4)
    if kA > 0:                                            # A: tu duong giua toi dinh 400
        bracket_v(d, 400, YC, ypx(A_CM), DRED, kA)
        text(d, (424, YC - 30), "A", 44, DRED, anchor="lm", alpha=kA)
    k1 = appear(t, M[0] + 1.0, 0.4)
    if k1 > 0:
        card(d, (60, 930, 1020, 1060), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=20, w=3)
        text(d, (W / 2, 995), "A = 6,0 : 2 = 3,0 cm", 50, DRED, alpha=k1)
    kd = appear(t, M[1] + 0.2, 0.4)
    if kd > 0: d_mark(d, kd, "16,0 cm = 1 chu kì")
    k2 = appear(t, M[1] + 1.2, 0.4)
    if k2 > 0:
        card(d, (60, 1100, 1020, 1230), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=20, w=3)
        text(d, (W / 2, 1165), "T = 16 cm : 20 cm/s = 0,80 s", 48, DGREEN, alpha=k2)

# ---------------- canh: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    kc = appear(t, M[0] + 1.4, 0.5)
    tape(d, RUN)
    yb = ypx(-A_CM) + 34                                   # ngoac duoi: dinh 400 -> day 600
    bracket_h(d, 400, 600, yb, DRED, a1)
    for xx, yy in ((400, ypx(A_CM)), (600, ypx(-A_CM))): dashed(d, (xx, yy + 6), (xx, yb), A(DRED, a1), w=3, on=8, off=6)
    if kc > 0:
        yt = ypx(A_CM) - 30
        bracket_h(d, 400, 800, yt, DGREEN, kc * (1 - k2))
    if a1 > 0:
        y0 = 960
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        yy = y0 + 175
        s = "Đỉnh → đáy kề nhau (ngang) = T"
        lw = tw(d, s, F(46))
        text(d, (W / 2 - 20, yy), s, 46, DRED, alpha=a1)
        text(d, (W / 2 - 20 + lw / 2 + 36, yy), "✗", 46, DRED, alpha=a1)
        if kc > 0:
            d.line([(W / 2 - 20 - lw / 2 - 6, yy + 4), (W / 2 - 20 - lw / 2 - 6 + (lw + 12) * kc, yy + 4)], fill=A((140, 15, 15), a1), width=6)
            text(d, (W / 2, y0 + 285), "Mới nửa chu kì", 46, DRED, alpha=a1 * kc)
            text(d, (W / 2, y0 + 380), "✓ Một chu kì: đỉnh → đỉnh", 46, DGREEN, alpha=a1 * kc)
    if k2 > 0:
        y0 = 960 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Giấy kéo tay: có đều không?", "• Ma sát đầu bút: bỏ qua")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 180 + j * 110), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh: Chot + cau hoi tu nho lai ----------------
END_M0 = 0.4
def _end_body(d, t, k1):
    kq = appear(t, END_M0 + 0.4, 0.5) * k1
    if kq > 0:                                             # hinh dieu kien: mui ten giay nhanh hon, khong ve net
        d.rectangle([150, 1110, 930, 1230], fill=A(PAPER, kq), outline=A(GRAY, kq), width=3)
        arrow(d, (670, 1170), (350, 1170), A(DBLUE, kq), w=8, head=26)
        text(d, (690, 1170), "nhanh hơn", 42, DBLUE, anchor="lm", alpha=kq)
    kh = appear(t, END_M0 + 0.4 + 2.5, 0.5) * k1
    if kh > 0:
        card(d, (110, 1300, 970, 1520), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1350), "Gợi ý", 38, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1440), "Mỗi chu kì, giấy đi bao xa?", 42, ORANGE, alpha=kh)

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Đỉnh → đáy là 2A.\nĐỉnh → đỉnh là một chu kì.",
             "Kéo giấy nhanh hơn: khoảng\nhai đỉnh và T đổi ra sao?", goi_y=None, body=_end_body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, dv, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (dv["t0"] + 0.1, "ding"), (dv["t0"] + R0, "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l11-baitapdaodong-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Bài tập dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bút vẽ lên băng giấy", draw=s_hook, tail=0.9, caps=[
   ("Bút gắn quả nặng, giấy chạy ngang.", 3.2),
   ("Tự đoán trước khi xem tiếp.", 5.4)]),
 dict(key="do", title="Thả vật, kéo giấy", draw=s_do, tail=0.8, caps=[
   ("Thả quả nặng, kéo giấy đều.", 4.6),
   ("Tháo giấy, đo bằng thước.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Đỉnh tới đáy là hai lần biên độ.", 4.2),
   ("Hai đỉnh liền kề: một chu kì.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.0, caps=[
   ("Bẫy: đỉnh–đáy kề nhau làm chu kì.", 4.8),
   ("Số minh hoạ, chưa đo thật.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.2, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])
