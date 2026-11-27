# Clip: tn-l10-dt-dctg-02 - Di bo "ve" do thi d-t: di cham ra, dung lai, quay ve nhanh (10/11/2026; dung lai 27/11/2026
# theo cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Bay hai khung co nhan, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dt-dctg-02.json (_kiem_so() doi chieu):
#   so_lieu_mau: (t s, d m) = (0;0) (1;1) (2;2) (3;3) (4;4) (5;5) (6;5) (7;5) (8;5) (9;3) (10;1) (10,5;0).
#   mo_hinh: 0-5 s d = 1.t ; 5-8 s d = 5 ; 8-10,5 s d = 5 - 2(t - 8). Do doc 1 m/s, 0, -2 m/s.
# Du doan (K10: khong nut A-D): doan 1-2 cho san, doan 3 (ve vach 0 trong 2,5 s, khong noi "nhanh") ve ra duong nao? -> xien xuong, doc hon doan 1.
# Bay = hien_tuong_hay_sai "doc doan di xuong la di xuong doc": hai khung tren/duoi (doc nui / hanh lang phang, ve vach 0).
#   KHONG chieu s = 10 m, d = 0 (de danh cho Cau 6 cua bai).
# Thu nghi (= cau_chot khung web): luot khac ra vach 4 m roi ve vach 2 m -> s = 4 + 2 = 6 m (truc d, thuoc khong hien 6 lam dap so).
from engine import *

PTS = [(0, 0.0), (1, 1.0), (2, 2.0), (3, 3.0), (4, 4.0), (5, 5.0), (6, 5.0), (7, 5.0), (8, 5.0),
       (9, 3.0), (10, 1.0), (10.5, 0.0)]
T_END = 10.5
SPEED = 1.5

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-dt-dctg-02.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == [tuple(p) for p in PTS]
    for tt, dm in PTS: assert abs(pos(tt)[0] - dm) < 1e-9
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["v1"]["mac_dinh"] == 1 and ts["v3"]["mac_dinh"] == -2 and ts["t_dung"]["mac_dinh"] == 3

DTEAL = (15, 118, 110); DRED = (185, 28, 28); DORANGE = (176, 64, 8); DBLUE = (29, 78, 216); EMPTY = (148, 140, 128)
SEGC = (DTEAL, (71, 85, 105), DORANGE)
TAPE = (250, 214, 92); TAPE_D = (190, 150, 40)

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def pos(t):
    t = clamp(t, 0, T_END)
    if t <= 5: return t, 1.0
    if t <= 8: return 5.0, 0.0
    return 5.0 - 2.0 * (t - 8), -2.0
_kiem_so()

def segs(d, x, y, parts, size, alpha=1.0, anchor="m"):
    f = F(size); tot = sum(tw(d, s, f) for s, _c in parts)
    xx = x - tot / 2 if anchor == "m" else x
    for s, c in parts:
        dtext(d, (xx, y), s, f, c, alpha, "lm"); xx += tw(d, s, f)

# ---------------- hanh lang + thuoc day + nguoi di ----------------
def walker(d, x, fy, v, phase, alpha=1.0, s=1.0):
    c = A(NAVY, alpha); sw = math.sin(phase) * (22 if abs(v) > 0 else 0) * s
    hip = (x, fy - 62 * s)
    d.line([hip, (x + sw, fy)], fill=c, width=9); d.line([hip, (x - sw, fy)], fill=c, width=9)
    d.line([hip, (x, fy - 140 * s)], fill=c, width=10)
    d.line([(x, fy - 125 * s), (x - sw * 0.8, fy - 80 * s)], fill=c, width=8)
    d.line([(x, fy - 125 * s), (x + sw * 0.8, fy - 80 * s)], fill=c, width=8)
    d.ellipse([x - 24 * s, fy - 192 * s, x + 24 * s, fy - 144 * s], fill=A(WHITE, alpha), outline=c, width=7)

TX0, TPX, TY = 120, 135, 500
def XT(dm): return TX0 + dm * TPX
def tape(d, y=TY, alpha=1.0):
    d.rectangle([XT(0) - 10, y, XT(6) + 30, y + 30], fill=A(TAPE, alpha), outline=A(TAPE_D, alpha), width=2)
    for k in range(7):
        d.line([(XT(k), y), (XT(k), y + 22)], fill=A(INK, alpha), width=4)
        text(d, (XT(k) + (22 if k == 6 else 0), y + 66), "6 m" if k == 6 else str(k), 56, DBLUE, alpha=alpha)

def corridor(d, tr, moving):
    card(d, (40, 205, 1040, 610), fill=WHITE, outline=LIGHT, w=3)
    tape(d)
    dm, v = pos(tr)
    walker(d, XT(dm), TY - 4, v if moving else 0.0, tr * 2.2 * math.pi)
    if moving and v != 0:
        sg = 1 if v > 0 else -1; L = 60 * abs(v)
        arrow(d, (XT(dm), TY - 215), (XT(dm) + sg * L, TY - 215), DRED, w=8, head=22)

def clock(d, tt):
    card(d, (720, 222, 1020, 305), fill=NAVY, r=18)
    text(d, (870, 264), "t = " + (vn(tt) if abs(tt - round(tt)) > 1e-9 else str(int(round(tt)))) + " s", 58, YELLOW)

# ---------------- do thi d-t (truc co dinh) ----------------
GX0, GX1, GYB, GYT = 200, 960, 1080, 700
def X(t): return GX0 + t / 11 * (GX1 - GX0)
def Y(dm): return GYB - dm / 6 * (GYB - GYT)
def axes(d, y0=625, y1=1180):
    card(d, (40, y0, 1040, y1), fill=WHITE, outline=LIGHT, w=3)
    arrow(d, (GX0, GYB), (GX1 + 40, GYB), NAVY, w=5, head=18); arrow(d, (GX0, GYB), (GX0, GYT - 30), NAVY, w=5, head=18)
    for tt in (2, 4, 6, 8, 10):
        d.line([(X(tt), GYB), (X(tt), GYB + 12)], fill=NAVY, width=4); text(d, (X(tt), GYB + 48), str(tt), 56, INK)
    for dm in (1, 2, 3, 4, 5):
        d.line([(GX0 - 12, Y(dm)), (GX0, Y(dm))], fill=NAVY, width=4)
        d.line([(GX0, Y(dm)), (GX1, Y(dm))], fill=(238, 233, 224), width=2)
        text(d, (GX0 - 22, Y(dm)), str(dm), 56, INK, anchor="rm")
    text(d, (1035, GYB + 48), "t (s)", 58, INK, anchor="rm")
    text(d, (GX0 + 25, GYT - 18), "d (m)", 58, DBLUE, anchor="lm")

def trail(d, t_upto, colored=True, width=9):
    if t_upto <= 0: return
    for i, (a, b) in enumerate(((0, 5), (5, 8), (8, T_END))):
        if t_upto <= a: continue
        e = min(b, t_upto)
        d.line([(X(a), Y(pos(a)[0])), (X(e), Y(pos(e)[0]))], fill=SEGC[i] if colored else NAVY, width=width)

def dots(d, t_upto, pop_t=None):
    for tt, dm in PTS:
        if tt <= t_upto + 1e-9:
            k = 1.0 if pop_t is None else back(clamp((pop_t - tt) / 0.35))
            if k > 0: dot(d, X(tt), Y(dm), 13 * k, NAVY, WHITE)

def badge_n(d, x, y, n, col, r=40, alpha=1.0):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(col, alpha))
    text(d, (x, y + 2), str(n), 58, WHITE, alpha=alpha)

BPOS = ((2.5, -1, 75), (6.5, 0, 70), (9.25, 1, 75))
def seg_badges(d, upto=3, alpha=1.0):
    for i in range(upto):
        tm, sx, off = BPOS[i]
        badge_n(d, X(tm) + sx * 55, Y(pos(tm)[0]) - off, i + 1, SEGC[i], alpha=alpha)

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
def s_hook(img, d, t, sc):
    M = sc["M"]
    tr = clamp((t - 0.3) / 2.8) * 8.0
    corridor(d, tr, 0 < tr < 8)
    axes(d); trail(d, tr); dots(d, tr)
    seg_badges(d, (1 if tr > 0 else 0) + (1 if tr > 5 else 0))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1195 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 395), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 22, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 160), "Đoạn 3: về vạch 0 trong 2,5 s.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 240), "Đường đoạn 3 thế nào?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 300, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (tua nhanh 1,5 lan) ----------------
RUN0 = 0.4
def run_t(t): return clamp((t - RUN0) * SPEED, 0, T_END)
def s_do(img, d, t, sc):
    tr = run_t(t)
    corridor(d, tr, 0 < tr < T_END)
    clock(d, max([p[0] for p in PTS if p[0] <= tr + 1e-9]))
    text(d, (60, 264), "tua nhanh ×1,5", 58, INK, anchor="lm")
    axes(d); trail(d, tr); dots(d, tr, pop_t=tr)
    seg_badges(d, sum(1 for a in (0, 5, 8) if tr > a))
    card(d, (40, 1200, 1040, 1330), fill=(245, 243, 255), outline=PURPLE, r=28, w=4)
    text(d, (W / 2, 1265), "Đoạn 3 vẽ ra đường nào?", 60, PURPLE)

# ---------------- canh 3: Dap an ----------------
def brace(d, ta, tb, y, col, lab, a):
    if a <= 0: return
    x1, x2 = X(ta) + 6, X(tb) - 6
    d.line([(x1, y), (x2, y)], fill=A(col, a), width=8)
    for xx in (x1, x2): d.line([(xx, y - 18), (xx, y + 18)], fill=A(col, a), width=8)
    text(d, ((x1 + x2) / 2, y + 52), lab, 58, col, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    card(d, (40, 205, 1040, 610), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 235, "ĐÁP ÁN", DTEAL, ka)
    text(d, (W / 2, 410), "Xiên xuống,", 64, DORANGE, alpha=ka)
    text(d, (W / 2, 500), "dốc hơn đoạn 1", 64, DORANGE, alpha=ka)
    axes(d, y1=1330); trail(d, T_END); dots(d, T_END); seg_badges(d)
    kb = appear(t, M[1] + 0.1, 0.4)
    brace(d, 0, 5, 1215, DTEAL, "5 s", kb); brace(d, 8, T_END, 1215, DORANGE, "2,5 s", kb)

# ---------------- canh 4: Rut ra (do doc tung doan) ----------------
def tri(d, ta, tb, k, col):
    if k <= 0: return
    xa, ya, xb, yb = X(ta), Y(pos(ta)[0]), X(tb), Y(pos(tb)[0])
    kx = clamp(k * 2); ky = clamp(k * 2 - 1)
    d.line([(xa, ya), (xa + (xb - xa) * kx, ya)], fill=col, width=6)
    if ky > 0: d.line([(xb, ya), (xb, ya + (yb - ya) * ky)], fill=col, width=6)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 205, 1040, 610), fill=WHITE, outline=TEAL, w=5)
    text(d, (W / 2, 275), "Độ dốc = vận tốc", 62, INK)
    d.line([(90, 330), (990, 330)], fill=LIGHT, width=3)
    k1 = 1.0; k3 = appear(t, M[1] + 0.1, 0.4)
    badge_n(d, 110, 410, 1, SEGC[0], alpha=k1)
    segs(d, 170, 410, [("5 m / 5 s", INK), (" = 1 m/s", DTEAL)], 60, alpha=k1, anchor="l")
    badge_n(d, 110, 530, 3, SEGC[2], alpha=k3)
    segs(d, 170, 530, [("−5 m / 2,5 s", INK), (" = −2 m/s", DORANGE)], 60, alpha=k3, anchor="l")
    axes(d); trail(d, T_END); dots(d, T_END); seg_badges(d)
    tri(d, 0, 5, clamp((t - 0.3) / 1.2), DTEAL)
    tri(d, 8, T_END, clamp((t - M[1]) / 1.2), DORANGE)

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 450), "Chỗ gãy thật ra sao?", 62, INK)
    card(d, (40, 590, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    ox, oy, s = 180, 1200, 120                                    # phong to goc gay luc t = 5 s
    P = lambda tt, dm: (ox + (tt - 1.5) * s, oy - (dm - 1.5) * s)
    d.line([P(1.5, 1.5), P(5, 5), P(8, 5)], fill=SEGC[0], width=10)
    d.line([P(5, 5), P(7.7, 5)], fill=SEGC[1], width=10)
    k = ease((t - 0.8) / 1.2)
    if k > 0:
        pts = []
        for i in range(31):
            u = i / 30 * k; tt = 3.8 + 2.4 * u
            dm = tt if tt < 4.4 else (5 - (5.6 - tt) ** 2 / 4.8 if tt < 5.6 else 5)
            dm = min(dm, 5)
            pts.append(P(tt, dm))
        for a_, b_ in zip(pts[::2], pts[1::2]): d.line([a_, b_], fill=PURPLE, width=14)
    kq = appear(t, 2.2, 0.4)
    if kq > 0:
        cx, cy = P(5, 5); d.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(124, 58, 237, int(50 * kq)), outline=A(PURPLE, kq), width=6)
        text(d, (cx + 10, cy + 200), "?", 96, PURPLE, alpha=kq)

# ---------------- canh 6: Bay (duong di xuong khong phai xuong doc) ----------------
def mini_seg(d, x0, y0):
    d.line([(x0, y0 + 260), (x0 + 260, y0 + 260)], fill=NAVY, width=4); d.line([(x0, y0 + 260), (x0, y0 + 20)], fill=NAVY, width=4)
    d.line([(x0 + 40, y0 + 60), (x0 + 220, y0 + 240)], fill=DORANGE, width=10)
    text(d, (x0 + 30, y0 + 305), "t", 56, INK); text(d, (x0 - 35, y0 + 40), "d", 56, DBLUE)

def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 750), fill=WHITE, outline=DRED, w=6)
    text(d, (75, 275), "✗ Xuống dốc?", 62, DRED, anchor="lm")
    mini_seg(d, 130, 330)
    d.polygon([(470, 420), (1000, 680), (470, 680)], fill=(214, 211, 199))     # con doc
    k = ease((t - 0.6) / 2.0); xw = 520 + 330 * k; yw = 420 + (xw - 470) * 260 / 530
    walker(d, xw, yw, 1, t * 7, s=0.8)
    if t >= M[1] - 0.1:
        card(d, (40, 790, 1040, 1325), fill=WHITE, outline=DTEAL, w=6)
        text(d, (75, 850), "✓ Về vạch 0", 62, DTEAL, anchor="lm")
        mini_seg(d, 130, 905)
        y = 1150; s0, sp = 470, 90
        d.rectangle([s0 - 10, y, s0 + 5 * sp + 30, y + 26], fill=TAPE, outline=TAPE_D, width=2)
        for kk in range(6):
            d.line([(s0 + kk * sp, y), (s0 + kk * sp, y + 20)], fill=INK, width=4)
        text(d, (s0, y + 64), "0", 56, DBLUE); text(d, (s0 + 5 * sp, y + 64), "5", 56, DBLUE)
        k2 = ease((t - M[1] - 0.2) / 2.0); xw2 = s0 + 5 * sp - 5 * sp * k2
        walker(d, xw2, y - 4, -1, t * 9, s=0.8)
        arrow(d, (xw2, y - 180), (xw2 - 110, y - 180), DRED, w=8, head=22)

# ---------------- canh 7: Chot + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 405), "Ra vạch 4 m, rồi về vạch 2 m.", 60, INK, alpha=k)
    y = 1050
    tape(d, y, k)
    ya, yb = 820, 930
    arrow(d, (XT(0), ya), (XT(4), ya), A(DTEAL, k), w=10, head=28)
    d.line([(XT(4), ya), (XT(4), yb)], fill=A(MUTED, k), width=5)
    arrow(d, (XT(4), yb), (XT(2), yb), A(DORANGE, k), w=10, head=28)
    walker(d, XT(2), y - 4, 0, 0, alpha=k, s=0.55)
    text(d, (W / 2, 1300), "Quãng đường đi được?", 64, DORANGE, alpha=k)
    seg_bar(d, 1430, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
          (do["t0"] + RUN0, "tap"), (do["t0"] + RUN0 + 8.0 / SPEED, "tap"),
          (da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-dt-dctg-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đồ thị độ dịch chuyển – thời gian · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đi bộ vẽ đồ thị", draw=s_hook, tail=0.3, caps=[
   ("Đi chậm ra 5 m, đứng 3 s.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Mỗi giây chấm một điểm.", 3.4),
   ("Đứng yên, rồi bước nhanh về.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("d giảm: đang quay về vạch 0.", 3.4),
   ("Cùng 5 m, đoạn 3 nhanh hơn.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Đi ra: độ dốc dương.", 3.0),
   ("Quay về: độ dốc âm.", 3.0)]),
 dict(key="bay", title="Bẫy: đường đi xuống", draw=s_bay, tail=0.3, caps=[
   ("Đường đi xuống là xuống dốc?", 3.4),
   ("Không: hành lang phẳng.", 3.0)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Số liệu từ mô hình.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Độ dốc đồ thị là vận tốc.", 6.0)]),
])
