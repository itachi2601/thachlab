# Clip: tn-l10-dt-dctg-02 - Di bo "ve" do thi d-t: di cham ra, dung lai, quay ve nhanh (10/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dt-dctg-02.json:
#   so_lieu_mau: (t s, d m) = (0;0) (1;1) (2;2) (3;3) (4;4) (5;5) (6;5) (7;5) (8;5) (9;3) (10;1) (10,5;0).
#   mo_hinh: 0-5 s d = 1.t ; 5-8 s d = 5 ; 8-10,5 s d = 5 - 2(t - 8) ; s = |Dd1| + |Dd2| + |Dd3| = 5 + 0 + 5 = 10 m.
#   ket_qua_ky_vong: do doc 1 m/s, 0, -2 m/s ; d cuoi = 0, s = 10 m. ghi_chu: do that co goc bo tron (chua noi duoc).
# Khac dtdctg1 (bot khi, hoi dang ca do thi): o day doan 1-2 cho san, Du doan hoi DOAN 3 (quay ve nhanh) ve ra gi.
# Cau chot: luot khac ra vach 4 m roi ve vach 2 m -> s = 6 m (truc d chi ghi so toi 5, khong co 6 tren do thi;
#   khong doc duoc tu duong da ve).
# Mau: doan 1 = TEAL, doan 2 = MUTED, doan 3 = ORANGE ; diem do = NAVY ; d = BLUE ; t = INK ; Du doan = PURPLE.
from engine import *

PTS = [(0, 0.0), (1, 1.0), (2, 2.0), (3, 3.0), (4, 4.0), (5, 5.0), (6, 5.0), (7, 5.0), (8, 5.0),
       (9, 3.0), (10, 1.0), (10.5, 0.0)]                                     # so_lieu_mau
T_END = 10.5
SEGC = (TEAL, MUTED, ORANGE)
PALE = (205, 205, 215); RED_D = (185, 28, 28); TAPE = (250, 214, 92); TAPE_D = (190, 150, 40)

def vn(x, nd=None):
    s = (f"{x:.{nd}f}" if nd is not None else f"{x:g}").replace(".", ",")
    return s.replace("-", "−")

def pos(t):
    """Mo hinh ba doan (mo_hinh.phuong_trinh) -> (d m, v m/s)."""
    t = clamp(t, 0, T_END)
    if t <= 5: return t, 1.0
    if t <= 8: return 5.0, 0.0
    return 5.0 - 2.0 * (t - 8), -2.0

def seg_of(t): return 0 if t <= 5 else (1 if t <= 8 else 2)

def segs(d, x, y, parts, size, alpha=1.0, anchor="m"):
    f = F(size); tot = sum(tw(d, s, f) for s, _c in parts)
    xx = x - tot / 2 if anchor == "m" else x
    for s, c in parts:
        dtext(d, (xx, y), s, f, c, alpha, "lm"); xx += tw(d, s, f)
    return tot

# ---------------- hanh lang + thuoc day + nguoi di ----------------
TX0, TPX, TY = 150, 140, 585                   # x cua vach 0 ; px / m ; mep tren thuoc
def XT(dm): return TX0 + dm * TPX
def walker(d, dm, v, phase, alpha=1.0):
    x = XT(dm); c = A(NAVY, alpha); fy = TY - 4
    sw = math.sin(phase) * (22 if abs(v) > 0 else 0)
    hip = (x, fy - 62)
    d.line([hip, (x + sw, fy)], fill=c, width=9); d.line([hip, (x - sw, fy)], fill=c, width=9)
    d.line([hip, (x, fy - 140)], fill=c, width=10)
    d.line([(x, fy - 125), (x - sw * 0.8, fy - 80)], fill=c, width=8)
    d.line([(x, fy - 125), (x + sw * 0.8, fy - 80)], fill=c, width=8)
    d.ellipse([x - 24, fy - 192, x + 24, fy - 144], fill=A(WHITE, alpha), outline=c, width=7)
    if v != 0:                                                     # mui ten van toc tren dau, dai ti le |v|
        L = 55 * abs(v); sgn = 1 if v > 0 else -1; y = fy - 209
        arrow(d, (x, y), (x + sgn * L, y), A(RED_D, alpha), w=7, head=20)

def corridor(d, t_run, flash=None):
    card(d, (40, 265, 1040, 690), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([XT(0) - 10, TY, XT(6) + 30, TY + 30], fill=TAPE, outline=TAPE_D, width=2)
    for k in range(7):
        x = XT(k); d.line([(x, TY), (x, TY + 22)], fill=INK, width=4)
        text(d, (x, TY + 62), str(k), 38, BLUE)
    text(d, (1020, 300), "thước dây", 36, MUTED, anchor="rm", bold=False)
    if t_run is None:
        walker(d, 0.0, 0.0, 0.0); return
    dm, v = pos(t_run)
    if t_run <= 0 or t_run >= T_END: v = 0.0
    walker(d, dm, v, t_run * 2.2 * math.pi * (1.0 if t_run <= 5 else 1.6))

def clock(d, tt):
    card(d, (60, 285, 330, 355), fill=NAVY, r=18)
    text(d, (195, 320), "t = " + vn(tt, 1) + " s", 40, YELLOW)

# ---------------- do thi d-t (truc co dinh ca clip) ----------------
GX0, GX1, GYB, GYT = 170, 980, 1225, 795
def X(t): return GX0 + t / 11 * (GX1 - GX0)
def Y(dm): return GYB - dm / 6 * (GYB - GYT)
def axes(d, box=(40, 715, 1040, 1300), alpha=1.0):
    c = lambda col: A(col, alpha)
    card(d, box, fill=c(WHITE), outline=c(LIGHT), w=3)
    arrow(d, (GX0, GYB), (GX1 + 40, GYB), c(NAVY), w=5, head=18)
    arrow(d, (GX0, GYB), (GX0, GYT - 30), c(NAVY), w=5, head=18)
    for tt in (2, 4, 6, 8, 10):
        d.line([(X(tt), GYB), (X(tt), GYB + 10)], fill=c(NAVY), width=3)
        text(d, (X(tt), GYB + 38), str(tt), 36, INK, bold=False, alpha=alpha)
    for dm in (1, 2, 3, 4, 5):
        d.line([(GX0 - 10, Y(dm)), (GX0, Y(dm))], fill=c(NAVY), width=3)
        d.line([(GX0, Y(dm)), (GX1, Y(dm))], fill=c((242, 238, 230)), width=2)
        text(d, (GX0 - 18, Y(dm)), str(dm), 36, INK, bold=False, anchor="rm", alpha=alpha)
    text(d, (GX0 - 18, GYB + 6), "0", 36, INK, bold=False, anchor="rm", alpha=alpha)
    text(d, (1030, GYB - 50), "t (s)", 38, INK, anchor="rm", alpha=alpha)
    text(d, (GX0 + 22, GYT - 22), "d (m)", 38, BLUE, anchor="lm", alpha=alpha)

def trail(d, t_upto, colored=False, width=6, segs_on=(1, 1, 1)):
    """Duong d(t) tu 0 toi t_upto (mo hinh); colored: moi doan mot mau."""
    if t_upto <= 0: return
    bounds = ((0, 5), (5, 8), (8, T_END))
    for i, (a, b) in enumerate(bounds):
        if t_upto <= a or not segs_on[i]: continue
        e = min(b, t_upto)
        col = SEGC[i] if colored else NAVY
        d.line([(X(a), Y(pos(a)[0])), (X(e), Y(pos(e)[0]))], fill=col, width=width)

def dots(d, t_upto, pop_t=None):
    for tt, dm in PTS:
        if tt <= t_upto + 1e-9:
            k = 1.0 if pop_t is None else back(clamp((pop_t - tt) / 0.35))
            if k > 0: dot(d, X(tt), Y(dm), 12 * k, NAVY, WHITE)

def badge(d, x, y, n, col, r=28, alpha=1.0):
    """So doan trong vong tron to mau (font SF ve ①②③ qua nho)."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(col, alpha))
    text(d, (x, y + 1), str(n), int(r * 1.45), WHITE, alpha=alpha)

def chip(d, s, y, col=PURPLE, bg=(245, 243, 255)):
    card(d, (60, y - 30, 1020, y + 30), fill=bg, outline=col, r=28, w=3)
    text(d, (W / 2, y), s, 38, col)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 690), fill=WHITE, outline=LIGHT, w=3)
    rows = [(1, "Đi chậm ra vạch 5 m", "5 s"), (2, "Đứng yên", "3 s"), (3, "Bước nhanh về vạch 0", "2,5 s")]
    for i, (n, s, tt) in enumerate(rows):
        y = 350 + i * 115; ka = appear(t, 0.3 + 0.5 * i, 0.4)
        badge(d, 100, y, n, SEGC[i], alpha=ka)
        text(d, (160, y), "Đoạn " + str(n) + ": " + s, 42, INK, anchor="lm", alpha=ka)
        text(d, (1005, y), tt, 44, INK, anchor="rm", alpha=ka)
    axes(d)
    trail(d, 8.0, colored=True)
    for i, tt in ((0, 2.5), (1, 6.5)):
        badge(d, X(tt) - (40 if i == 0 else 0), Y(pos(tt)[0]) - 50, i + 1, SEGC[i])
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1315 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 280), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 20, W / 2 + pw / 2, y0 + 80), fill=A(PURPLE, a), r=30)
    text(d, (W / 2, y0 + 50), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 140, "Đoạn 3 vẽ ra đường nào?", 52, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 225, 940, y0 + 239], radius=7, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 225, 140 + 800 * (1 - p), y0 + 239], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (thoi gian that) ----------------
RUN0 = 0.8
def run_t(t): return clamp(t - RUN0, 0, T_END)
def s_do(img, d, t, sc):
    tr = run_t(t)
    corridor(d, tr if t >= RUN0 else None)
    clock(d, tr)
    axes(d)
    trail(d, tr)
    dots(d, tr, pop_t=tr)
    chip(d, "Câu hỏi: đoạn 3 vẽ ra đường nào?", 1360)
    chip(d, "chấm điểm (t, d) mỗi giây", 1460, col=NAVY, bg=WHITE)
    for i, (a, b) in enumerate(((0, 5), (5, 8), (8, T_END))):     # so doan dang di, o duoi truc t
        if a < tr <= b + 0.6 and tr > 0:
            tm = (a + b) / 2
            badge(d, X(tm) + (-40 if i == 0 else (0 if i == 1 else 40)), Y(pos(tm)[0]) - 50, i + 1, SEGC[i])

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · đi xuống, dốc hơn đoạn 1"
    pw = tw(d, lb, F(42)) + 56
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 342), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 306), lb, 42, WHITE, alpha=ka)
    k1 = appear(t, 0.8, 0.5)
    card(d, (40, 380, 1040, 690), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    segs(d, W / 2, 460, [("d", BLUE), (" giảm: quay về", INK)], 44, alpha=k1)
    k2 = appear(t, M[0] + 1.4, 0.5)
    segs(d, W / 2, 590, [("dốc hơn: về nhanh hơn", INK)], 44, alpha=k2)
    axes(d)
    trail(d, T_END, colored=True, width=8)
    dots(d, T_END)

# ---------------- canh 4: Rut ra (do doc tung doan) ----------------
def tri(d, ta, tb, k, col):
    """Tam giac do doc net dut tren doan [ta, tb]: ngang (Dt) roi doc (Dd)."""
    if k <= 0: return
    xa, ya, xb, yb = X(ta), Y(pos(ta)[0]), X(tb), Y(pos(tb)[0])
    kx = clamp(k * 2); ky = clamp(k * 2 - 1)
    for i in range(12):
        u0, u1 = i / 12, (i + 0.55) / 12
        if u0 < kx: d.line([(xa + (xb - xa) * u0, ya), (xa + (xb - xa) * min(u1, kx), ya)], fill=col, width=5)
    for i in range(8):
        u0, u1 = i / 8, (i + 0.55) / 8
        if u0 < ky: d.line([(xb, ya + (yb - ya) * u0), (xb, ya + (yb - ya) * min(u1, ky))], fill=col, width=5)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    axes(d)
    trail(d, T_END, colored=True, width=8)
    dots(d, T_END)
    tri(d, 0, 5, clamp((t - 0.6) / 1.0), TEAL)
    tri(d, 8, T_END, clamp((t - 2.2) / 1.0), ORANGE)
    card(d, (40, 265, 1040, 690), fill=WHITE, outline=TEAL, w=5)
    text(d, (W / 2, 320), "Độ dốc = vận tốc", 46, INK)
    d.line([(90, 365), (990, 365)], fill=LIGHT, width=3)
    k1 = appear(t, 0.9, 0.5); k2 = appear(t, 1.8, 0.5); k3 = appear(t, 2.6, 0.5)
    for i, kk_ in enumerate((k1, k2, k3)): badge(d, 108, 425 + 85 * i, i + 1, SEGC[i], alpha=kk_)
    segs(d, 160, 425, [("5 m / 5 s", INK), (" = 1 m/s", TEAL)], 44, alpha=k1, anchor="l")
    segs(d, 160, 510, [("nằm ngang", INK), (": v = 0", MUTED)], 44, alpha=k2, anchor="l")
    segs(d, 160, 595, [("−5 m / 2,5 s", INK), (" = −2 m/s", ORANGE)], 44, alpha=k3, anchor="l")
    kc = appear(t, M[1] - 0.1, 0.45)
    if kc <= 0: return
    y0 = 1315 + (1 - kc) * 30
    card(d, (40, y0, 1040, y0 + 280), fill=A((254, 242, 242), kc), outline=A(NAVY, kc), w=5)
    text(d, (W / 2, y0 + 55), "Chưa nói được", 42, NAVY, alpha=kc)
    kk = kc * appear(t, M[1] + 0.3, 0.4)
    text(d, (W / 2, y0 + 135), "Lúc bắt đầu đi, lúc dừng:", 42, RED_D, alpha=kk)
    text(d, (W / 2, y0 + 205), "góc gãy thật bo tròn ra sao?", 42, RED_D, alpha=kk)

# ---------------- canh 5: Bay (quang duong doc o diem cuoi) ----------------
def s_bay(img, d, t, sc):
    axes(d)
    trail(d, T_END, colored=True, width=8)
    dots(d, T_END)
    a1 = appear(t, 0.15, 0.4)
    ex, ey = X(T_END), Y(0)
    if a1 > 0: d.ellipse([ex - 24, ey - 24, ex + 24, ey + 24], outline=A(RED, a1), width=6)
    card(d, (40, 265, 1040, 690), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(RED, a1), r=32)
    text(d, (W / 2, 322), "BẪY", 38, WHITE, alpha=a1)
    q = "“d cuối = 0 → s = 0”"
    ks = clamp((t - 1.4) / 0.4); f = F(44); lw = tw(d, q, f); yy = 440
    text(d, (W / 2, yy), q, 44, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        text(d, (W / 2 + lw / 2 + 50, yy), "✗", 52, RED, alpha=ks * a1)
    kk = appear(t, 2.0, 0.5)
    segs(d, W / 2, 560, [("s = ", INK), ("5", TEAL), (" + ", INK), ("0", MUTED), (" + ", INK), ("5", ORANGE),
                         (" = 10 m", INK)], 50, alpha=kk)
    segs(d, W / 2, 635, [("cộng độ dài từng đoạn", INK)], 38, alpha=kk)
    k2 = appear(t, 2.6, 0.5)                                        # |Dd| tung doan tren do thi
    if k2 > 0:
        text(d, (X(2.5) - 40, Y(2.5) - 20), "5 m", 40, TEAL, anchor="rm", alpha=k2)
        text(d, (X(9.25) + 40, Y(2.5) - 20), "5 m", 40, ORANGE, anchor="lm", alpha=k2)
    card(d, (40, 1315, 1040, 1595), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    segs(d, W / 2, 1400, [("Độ dịch chuyển ", INK), ("d", BLUE), (" = 0", BLUE)], 46, alpha=appear(t, 3.4, 0.5))
    segs(d, W / 2, 1500, [("Quãng đường ", INK), ("s", INK), (" = 10 m", INK)], 46, alpha=appear(t, 3.4, 0.5))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
HOI = "Đi ra vạch 4 m, rồi về vạch 2 m.\nQuãng đường s = ?"
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        ctext(d, 940, HOI, 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
        kh = appear(t, M[0] + 3.0, 0.5)
        if kh <= 0: return
        card(d, (110, 1260, 970, 1420), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1340), "Chia hành trình thành từng đoạn", 44, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Độ dốc d–t là vận tốc;\nd cuối khác quãng đường", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + RUN0, "tap"), (do["t0"] + RUN0 + 8.0, "tap"),
          (da["t0"] + 0.15, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-dt-dctg-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đồ thị độ dịch chuyển – thời gian · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đi bộ vẽ đồ thị", draw=s_hook, tail=0.6, caps=[
   ("Ba đoạn đi trên thước dây.", 2.6),
   ("Dừng video, chọn câu trả lời.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Bạn B hô từng giây, bạn C chấm điểm.", 8.4),
   ("Bước nhanh về vạch 0.", 2.7)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("So đoạn 3 với đoạn 1.", 4.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Lấy hai đầu mỗi đoạn.", 4.0),
   ("Còn điều chưa biết.", 3.6)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.5, caps=[
   ("Quãng đường đọc ở đâu?", 5.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])
