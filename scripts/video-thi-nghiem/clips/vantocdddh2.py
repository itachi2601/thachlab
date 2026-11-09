# Clip: tn-l11-vantocdddh-02 - Ba do thi x, v, a khi pha ban dau bang 0 (vi_du, ve tu mo hinh) (9/11/2026, L11 Ch.1)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-vantocdddh-02.json:
#   tham_so: A = 4 cm, T = 0,8 s, phi = 0 ; mo_hinh: x = A cos(wt), v = -Aw sin(wt), a = -Aw^2 cos(wt), w = 2pi/0,8.
#   so_lieu_mau (t s; x cm; v cm/s; a cm/s2): 0 4 0 -246,7 ; 0,2 0 -31,42 0 ; 0,4 -4 0 246,7 ; 0,6 0 31,42 0.
#   rut_ra: v som x mot goc pi/2 ; a nguoc pha voi x. Hinh 2 cua bai (anh OpenStax, data-exp = id nay) la cho dat.
#   hien_tuong_hay_sai[0] (v trung x) -> Du doan ; [1] (a cung pha v) -> Bay (t = 0,2 s: |v| lon nhat, a = 0).
#   Cau chot: A = 2 cm (trong khoang tham_so, chua hien), T giu 0,8 s, t = 0,4 s -> a = +123,4 cm/s2 (KHONG hien;
#     phan xa sai: -123,4 hoac 246,7). Khong neu "a_max o bien am" bang loi (cau trac nghiem ngay sau Hinh 2 trong bai).
# Bo cuc: ba do thi xep doc cung truc t (0..0,8 s), con tro thoi gian dung o 4 moc, bang so ben duoi.
# Canh: Du doan (K10: chi cau hoi + hinh; truc v trong) -> Tien hanh -> Dap an + Rut ra -> Bay roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (goi y tre 2,5 s).
from engine import *

AMP, PER = 4.0, 0.8
VM, AM = 31.42, 246.7                                       # |v|max, |a|max trong so_lieu_mau
OMG = 2 * math.pi / PER
ROWS = [("0", "4", "0", "−246,7"), ("0,2", "0", "−31,42", "0"), ("0,4", "−4", "0", "246,7"), ("0,6", "0", "31,42", "0")]
TS = [0.0, 0.2, 0.4, 0.6]
def xf(t): return AMP * math.cos(OMG * t)
def vf(t): return -VM * math.sin(OMG * t)
def af(t): return -AM * math.cos(OMG * t)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DBLUE = (29, 78, 216)

# ---------------- ba do thi (khung nguon 1080x1920; vung thay y 200..1690) ----------------
GX0, GSX = 210, 850                  # t = 0 o px 210 ; 0,8 s = 680 px
H2 = 110                             # nua chieu cao duong cong
def gx(t): return GX0 + t * GSX
SER = {   # khoa: (tam y, ham, dinh, nhan truc, mau, nhan dinh)
    "x": (430, xf, AMP, "x (cm)", TEAL, ("4", "−4")),
    "v": (750, vf, VM, "v (cm/s)", BLUE, ("31,42", "−31,42")),
    "a": (1070, af, AM, "a (cm/s²)", RED, ("246,7", "−246,7")),
}
def gy(k, val):
    c, _, pk, *_ = SER[k]
    return c - val / pk * H2

def axes(d, keys, tlab_y, a=1.0):
    top = SER[keys[0]][0] - 150; bot = SER[keys[-1]][0] + 130
    for tt in (0.2, 0.4, 0.6, 0.8):
        for yy in range(int(top + 20), int(bot), 26): d.line([(gx(tt), yy), (gx(tt), yy + 12)], fill=A(LIGHT, a), width=3)
    for k in keys:
        c, _, pk, lab, col, (lp, ln) = SER[k]
        arrow(d, (GX0, c + 130), (GX0, c - 150), A(NAVY, a), w=4, head=16)
        arrow(d, (GX0, c), (gx(0.86), c), A(NAVY, a), w=4, head=16)
        text(d, (GX0 + 16, c - 150), lab, 40, col, anchor="lm", alpha=a)
        for yy, s in ((c - H2, lp), (c + H2, ln)):
            d.line([(GX0 - 8, yy), (GX0 + 8, yy)], fill=A(NAVY, a), width=3)
            text(d, (GX0 - 16, yy), s, 40, NAVY, anchor="rm", alpha=a)
    for tt in (0.2, 0.4, 0.6, 0.8):
        text(d, (gx(tt), tlab_y), f"{tt:.1f}".replace(".", ","), 40, NAVY, alpha=a)
    text(d, (GX0, tlab_y), "0", 40, NAVY, alpha=a)
    text(d, (gx(0.86) + 12, tlab_y), "t (s)", 40, INK, anchor="lm", alpha=a)

def curve(d, k, t1, a=1.0, w=6):
    if t1 <= 0: return
    c, f, _, _, col, _ = SER[k]
    n = max(2, int(t1 * 300))
    d.line([(gx(t1 * i / n), gy(k, f(t1 * i / n))) for i in range(n + 1)], fill=A(col, a), width=w, joint="curve")

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh; truc v trong, chua ve truc a) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    axes(d, ["x", "v"], 920)
    curve(d, "x", PER * clamp((t - 0.6) / 1.6))
    kq = appear(t, 2.4, 0.4)
    if kq > 0: text(d, (gx(0.4), SER["v"][0] - 60), "v = ?", 56, PURPLE, alpha=kq)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 165, "φ = 0: lúc t = 0 vật ở biên +A.", 44, MUTED, maxw=940, alpha=a)
    ctext(d, y0 + 315, "Đồ thị v có dạng thế nào\nso với đồ thị x?", 52, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 450, 940, y0 + 462], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 450, 140 + 800 * (1 - p), y0 + 462], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (con tro thoi gian dung o 4 moc) ----------------
D0, HOLD, MOVE = 0.4, 1.0, 0.9
def phase(v):
    """-> (t do thi, so cot bang da co, chi so moc dang dung hoac None)."""
    if v < D0: return 0.0, 0, None
    u = v - D0
    for i in range(4):
        if u < HOLD: return TS[i], i + 1, i
        u -= HOLD
        if u < MOVE: return TS[i] + 0.2 * u / MOVE, i + 1, None
        u -= MOVE
    return PER, 4, None

def table(d, ncol, cur=None, y0=1300):
    card(d, (40, y0, 1040, y0 + 270), fill=WHITE, outline=NAVY, r=20, w=3)
    labs = ("t (s)", "x (cm)", "v (cm/s)", "a (cm/s²)"); cols = (INK, TEAL, DBLUE, DRED)
    for r in range(4):
        y = y0 + 40 + r * 64
        if r: d.line([(56, y - 32), (1024, y - 32)], fill=LIGHT, width=2)
        text(d, (145, y), labs[r], 38, cols[r])
        for i in range(4):
            cx = 355 + i * 190
            if r == 0:
                if cur == i: card(d, (cx - 95, y0 + 8, cx + 95, y0 + 262), fill=(255, 237, 213), r=14)
                text(d, (cx, y), ROWS[i][0], 40, INK)
            elif i < ncol: text(d, (cx, y), ROWS[i][r], 40, cols[r])

def cursor(d, tt, keys=("x", "v", "a"), col=PURPLE):
    d.line([(gx(tt), SER["x"][0] - 140), (gx(tt), SER["a"][0] + 125)], fill=A(col, 0.85), width=4)
    for k in keys:
        dot(d, gx(tt), gy(k, SER[k][1](tt)), 12, SER[k][4], outline=WHITE)

def s_do(img, d, t, sc):
    tt, n, cur = phase(t)
    axes(d, ["x", "v", "a"], 1240)
    for k in ("x", "v", "a"): curve(d, k, tt)
    if t >= D0: cursor(d, tt)
    table(d, n, cur)

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    axes(d, ["x", "v", "a"], 1240)
    for k in ("x", "v", "a"): curve(d, k, PER)
    ka = appear(t, 0.1, 0.5)
    pill(d, W / 2, 1310, "ĐÁP ÁN · như x, dịch sang trái T/4", 42, WHITE, NAVY, ka)
    kp = appear(t, 0.8, 0.45)                                  # dinh v (0,6 s) truoc dinh x (0,8 s)
    if kp > 0:
        yv, yx = gy("v", VM), gy("x", AMP)
        for tt, y, col in ((0.6, yv, BLUE), (0.8, yx, TEAL)):
            dot(d, gx(tt), y, 14, A(col, kp), outline=WHITE)
        for yy in range(int(yx - 60), int(yv), 24): d.line([(gx(0.6), yy), (gx(0.6), yy + 12)], fill=A(BLUE, kp), width=4)
        d.line([(gx(0.8), yx - 60), (gx(0.8), yx - 14)], fill=A(TEAL, kp), width=4)
        y = yx - 50
        arrow(d, (gx(0.6) + 4, y), (gx(0.8) - 4, y), A(ORANGE, kp), w=5, head=16)
        arrow(d, (gx(0.8) - 4, y), (gx(0.6) + 4, y), A(ORANGE, kp), w=5, head=16)
        text(d, (gx(0.6) - 16, y - 2), "0,2 s", 40, ORANGE, anchor="rm", alpha=kp)
    k1 = appear(t, M[1] - 0.05, 0.45)
    if k1 > 0:                                                 # a lat nguoc x: hai cham luc t = 0
        dot(d, gx(0), gy("x", AMP), 14, A(TEAL, k1), outline=WHITE)
        dot(d, gx(0), gy("a", -AM), 14, A(RED, k1), outline=WHITE)
        card(d, (60, 1380, 1020, 1600), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        text(d, (W / 2, 1440), "v sớm x một góc π/2", 46, DBLUE, alpha=k1)
        text(d, (W / 2, 1540), "a ngược pha với x", 46, DRED, alpha=appear(t, M[1] + 0.6, 0.45))

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d, ["x", "v", "a"], 1240)
    for k in ("x", "v", "a"): curve(d, k, PER)
    kc = appear(t, 1.8, 0.4)                                  # con tro 0,2 s hien CUNG luc chu ✓
    if kc > 0:
        d.line([(gx(0.2), SER["x"][0] - 140), (gx(0.2), SER["a"][0] + 125)], fill=A(PURPLE, 0.85 * kc), width=4)
        dot(d, gx(0.2), gy("v", -VM), 14, A(BLUE, kc), outline=WHITE)
        dot(d, gx(0.2), gy("a", 0), 14, A(RED, kc), outline=WHITE)
    a1 = appear(t, 0.0, 0.3) * (1 - appear(t, M[1] - 0.3, 0.2))
    if a1 > 0:
        y0 = 1290
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y0 + 56, "BẪY", 40, WHITE, DRED, a1)
        q = "“a cùng pha với v”"
        yy = y0 + 170; f = F(48); lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 48, DRED, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A((140, 15, 15), a1), width=4)
        ctext(d, y0 + 290, "✓ t = 0,2 s: v = −31,42 cm/s, a = 0", 44, DGREEN, maxw=940, alpha=a1 * kc)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1290 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 65), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Mới vẽ một ca φ = 0", "• Bỏ qua ma sát")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 170 + j * 100), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(sc):
    M = sc["M"]
    def body(d, t, k1):
        kq = appear(t, M[0] + 0.4, 0.5)
        for j, (lab, val) in enumerate((("A (cm)", "2"), ("t (s)", "0,4"), ("a (cm/s²)", "?"))):
            x0 = 90 + j * 310
            card(d, (x0, 1040, x0 + 280, 1210), fill=A((245, 243, 255), kq), outline=A(PURPLE, kq), r=18, w=3)
            text(d, (x0 + 140, 1085), lab, 38, MUTED, bold=False, alpha=kq)
            text(d, (x0 + 140, 1155), val, 48, PURPLE if val == "?" else INK, alpha=kq)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)                 # goi y tre 2,5 s sau cau hoi
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1450, "Tìm x lúc đó trước, rồi xét dấu", 42, ORANGE, maxw=820, alpha=kh)
    return body

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "v sớm x góc π/2.\na ngược pha với x.",
             "Cùng T = 0,8 s, đổi A = 2 cm.\nLúc t = 0,4 s, a bằng bao nhiêu?", body=_end_body(sc))

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + D0, "tap")]
    out += [(do["t0"] + D0 + i * (HOLD + MOVE), "tick") for i in (1, 2, 3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-vantocdddh-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Vận tốc, gia tốc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba đồ thị, một trục thời gian", draw=s_hook, tail=0.6, caps=[
   ("A = 4 cm, T = 0,8 s.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Dừng ở mỗi mốc 0,2 s, đọc số.", 4.2),
   ("Ba chấm cùng một thời điểm.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Đỉnh v đến trước đỉnh x.", 4.2),
   ("Đường a lật ngược đường x.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Bẫy khi so v với a.", 4.4),
   ("Kết quả này còn giới hạn.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.4, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
