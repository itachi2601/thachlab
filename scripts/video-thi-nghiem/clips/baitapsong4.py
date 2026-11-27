# Clip: tn-l11-baitapsong-04 - Thoi vao ong nhua mot dau kin: not co ban theo chieu dai ong (lo 11, 19/11/2026;
# dung lai 27/11/2026 theo cong moi: chu ve >= 55 px (ra >= 48), moi nhip >= 2,5 s, Du doan khong nut A-D (K10),
# thanh dem day 70 px, Bay hai khung tu giai thich, Gioi han rieng, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapsong-04.json (_kiem_so() doi chieu ca mo_hinh f1 = v/(4L), v = 340):
#   so_lieu_mau (L m, f1 Hz): 0,17 500 ; 0,34 250 ; 0,68 125. Kho ghi "Tinh tu mo hinh" -> man dien thoai ghi "≈".
# Du doan (K10, khong nut A-D): ong 0,17 m keu 500 Hz; noi dai gap doi (0,34 m) -> not co ban? Dap an 250 Hz (giam mot nua).
#   Hop exp cua bai (Rut ra: f1 = v/(4L) = 500 Hz) cho cong thuc -> cau hoi hoi SO, van can mot buoc.
#   Khong trung Cau 3 (bung tren day 0,9 m), Cau 5 (nut-bung), Thu thach (day 1,2 m).
# Bay = hien_tuong_hay_sai[0]: dung f = v/(2L) cua day cho ong kin. Doi ca so voi ban cu (0,34 m -> 500 Hz) sang
#   0,68 m -> 250 Hz (that 125 Hz) de Bay KHONG lap cap so cua Du doan (0,34 m / 250 Hz). Kho ghi_chu con ghi ca cu.
# Gioi han = sai_so_thuong_gap[1]: khi rung lo ra ngoai mieng ong (hieu chinh mieng ong) -> ong that keu thap hon chut.
# THU NGHI (= cau_chot khung web): ong 0,17 m, not co ban 500 Hz; not cao KE TIEP ong keu duoc? -> 3.500 = 1500 Hz
#   (m le; 1000 Hz la bay "nhu day"). Buoc suy luan chua chieu (mau 3λ/4); so 1500 KHONG hien tren man.
from engine import *

V = 340
ROWS = [(0.17, 500), (0.34, 250), (0.68, 125)]       # (L m, f1 Hz)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DGREEN, DPURPLE, DRED, DORANGE = (21, 110, 55), (91, 33, 182), (185, 28, 28), (176, 64, 8)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-baitapsong-04.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["v"]["gia_tri"] == V
    for L, f in ROWS:
        assert (L, f) in hang, (L, f)
        assert abs(V / (4 * L) - f) < 0.5, (L, f)        # mo_hinh f1 = v/(4L)
    assert abs(V / (2 * 0.68) - 250) < 0.5               # bay: v/(2L) voi 0,68 m
    assert "1500" in k["so_lieu_mau"]["ghi_chu"]         # cau chot ghi trong kho
_kiem_so()

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 56
    card(d, (cx - pw / 2, cy - size * 0.82, cx + pw / 2, cy + size * 0.82), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem day 70 px, rut tu phai sang trai theo 10 nac (moi nac la mot thay doi hinh ro)."""
    p = clamp((t - t0) / (t1 - t0)); q = math.floor(p * 10 + 1e-9) / 10
    d.rounded_rectangle([140, y, 940, y + 70], radius=35, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 70], radius=35, fill=A(col, a))

# ---------------- hinh: ong nam ngang, dau kin ben TRAI, mieng ho ben PHAI ----------------
XC, PX, HH = 120, 1150, 46                            # dau kin x = 120 ; 1150 px/m ; nua chieu cao long ong
TUBE = (226, 232, 240); WALL = (70, 80, 105); AIR = (14, 116, 144); ENV = (124, 58, 237)
SCR = (18, 26, 48); SCR_T = (190, 200, 225); NUM = (74, 222, 128)

def env_amp(x, Lpx):
    """Bien do dao dong cua khi tai x (px tu dau kin): nut o dau kin, bung o mieng (L = λ/4)."""
    return math.sin(math.pi / 2 * x / Lpx)

def _kiem_vat_li():
    Lp = 0.34 * PX
    assert abs(env_amp(0, Lp)) < 1e-9                    # dau kin: nut
    assert abs(env_amp(Lp, Lp) - 1) < 1e-9               # mieng: bung
    assert all(env_amp(x, Lp) <= env_amp(x + 1, Lp) + 1e-12 for x in range(int(Lp)))   # tang don dieu: chi 1/4 buoc song
    for i in range(1, 3): assert abs(ROWS[i][0] / ROWS[i - 1][0] - 2) < 1e-9 and ROWS[i][1] * 2 == ROWS[i - 1][1]
    assert XC + 0.68 * PX + 34 < 1000                     # ong dai nhat + luong hoi van trong khung
_kiem_vat_li()

def tube(d, y, Lm, blow=0.0, env=0.0, t=0.0, labels=0.0, len_lbl=True):
    Lpx = Lm * PX; x1 = XC + Lpx
    d.rectangle([XC, y - HH, x1, y + HH], fill=TUBE)
    if env > 0:                                                                # vung khi dao dong (to dac, phap phong)
        sw = 0.55 + 0.45 * math.cos(2 * math.pi * 1.4 * t)
        top = [(XC + x, y - sw * (HH - 6) * env_amp(x, Lpx)) for x in range(0, int(Lpx) + 1, 6)]
        bot = [(XC + x, y + sw * (HH - 6) * env_amp(x, Lpx)) for x in range(0, int(Lpx) + 1, 6)]
        d.polygon(top + bot[::-1], fill=A((196, 181, 253), env))
        for pts in (top, bot): d.line(pts, fill=A(ENV, env), width=5)
    d.line([(XC, y - HH), (x1, y - HH)], fill=WALL, width=7); d.line([(XC, y + HH), (x1, y + HH)], fill=WALL, width=7)
    d.rectangle([XC - 20, y - HH - 4, XC, y + HH + 4], fill=WALL)                 # nap bit dau kin
    for Lj in (0.17, 0.34):                                                    # khop noi
        if Lj < Lm - 1e-6:
            xj = XC + Lj * PX; d.rectangle([xj - 7, y - HH - 9, xj + 7, y + HH + 9], fill=(150, 156, 172))
    if labels > 0:
        text(d, (XC - 10, y - HH - 46), "nút", 56, ENV, anchor="lm", alpha=labels)
        text(d, (x1 + 10, y - HH - 46), "bụng", 56, ENV, anchor="rm", alpha=labels)
    if blow > 0:                                                               # luong hoi thoi ngang mieng
        xa = x1 + 40
        for k in range(3):
            yy = y - 120 + ((t * 260 + k * 60) % 180)
            d.line([(xa, yy), (xa, yy + 34)], fill=A(AIR, blow), width=8)
        arrow(d, (xa, y - 120), (xa, y + 70), A(AIR, blow), w=6, head=20)
    if len_lbl:
        d.line([(XC, y + HH + 34), (x1, y + HH + 34)], fill=NAVY, width=3)
        for xx in (XC, x1): d.line([(xx, y + HH + 22), (xx, y + HH + 46)], fill=NAVY, width=3)
        text(d, ((XC + x1) / 2, y + HH + 88), vn(Lm) + " m", 56, INK)

def phone(d, cx, y, f=None):
    card(d, (cx - 250, y, cx + 250, y + 210), fill=SCR, r=30)
    text(d, (cx, y + 55), "Đo tần số", 56, SCR_T)
    s = "— Hz" if f is None else "≈ " + str(f) + " Hz"
    text(d, (cx, y + 145), s, 70, NUM if f is not None else SCR_T)

def ftable(d, y, n, hl=-1, ratio=0.0):
    card(d, (60, y, 1020, y + 110 + 3 * 82), fill=WHITE, outline=NAVY, w=4)
    text(d, (330, y + 54), "Ống dài (m)", 56, INK); text(d, (720, y + 54), "Nốt cơ bản (Hz)", 56, INK)
    d.line([(90, y + 100), (990, y + 100)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 146 + i * 82; L, f = ROWS[i]
        if i == hl: d.rounded_rectangle([80, yy - 36, 1000, yy + 36], radius=16, fill=(255, 237, 213))
        text(d, (330, yy), vn(L), 58, INK); text(d, (720, yy), str(f), 58, BLUE)
    if ratio > 0:
        for j in range(2):
            yy = y + 146 + (j + 0.5) * 82
            arrow(d, (130, yy - 34), (130, yy + 34), A(ORANGE, ratio), w=6, head=14)
            arrow(d, (960, yy - 34), (960, yy + 34), A(ORANGE, ratio), w=6, head=14)
        text(d, (160, y + 146 + 82), "×2", 56, ORANGE, anchor="lm", alpha=ratio)
        text(d, (930, y + 146 + 82), "÷2", 56, ORANGE, anchor="rm", alpha=ratio)

YT = 400
def bench(d, L, f, t, blow=True, kin=True):
    card(d, (40, 215, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    tube(d, YT, L, blow=1.0 if blow else 0.0, t=t)
    if kin: text(d, (XC - 20, 290), "đầu kín", 56, INK, anchor="lm")
    phone(d, W / 2, 650, f)

# ---------------- canh 1: Du doan (K10: chi cau hoi, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bench(d, 0.17, ROWS[0][1], t, kin=False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 75, "DỰ ĐOÁN", 58, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 180), "Ống kín 0,17 m kêu 500 Hz.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Nối thành 0,34 m: nốt", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "cơ bản bao nhiêu?", 62, DPURPLE, alpha=a)
    cbar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
STARTS = [0.0, 3.4, 6.8]; GROW = 0.7; READ = 2.5     # so tren dien thoai va hang bang hien CUNG LUC (s + READ)
def do_state(t):
    """-> (i ong dang dung, L dang ve, f dang hien hoac None, so hang da ghi, dang thoi)."""
    i = max(j for j, s in enumerate(STARTS) if t >= s)
    s = STARTS[i]; Lprev = ROWS[i - 1][0] if i > 0 else ROWS[0][0]
    L = lerp(Lprev, ROWS[i][0], ease((t - s) / GROW)) if i > 0 else ROWS[0][0]
    growing = i > 0 and t < s + GROW
    blowing = t >= s + (GROW if i > 0 else 0) + 0.2
    f = ROWS[i][1] if t >= s + READ else None
    rows = i + (1 if f is not None else 0)
    return i, L, f, rows, blowing and not growing

def s_do(img, d, t, sc):
    i, L, f, rows, bl = do_state(t)
    bench(d, L, f, t, blow=bl)
    ftable(d, 940, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: so tren dien thoai = f cua ong dang ve ; hang bang hien cung luc so ; du 3 hang."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        i, L, f, rows, bl = do_state(t)
        if f is not None:
            if abs(L - ROWS[i][0]) > 1e-9: bad.append((round(t, 2), "so hien khi ong chua noi xong"))
            if abs(V / (4 * L) - f) > 0.5: bad.append((round(t, 2), "so lech ong"))
        if rows > i + 1: bad.append((round(t, 2), "hang som"))
        if rows == i + 1 and f is None: bad.append((round(t, 2), "hang truoc so"))
        t += 0.05
    if do_state(sc["T"] - 0.05)[3] != 3: bad.append("chua du 3 hang")
    if sc["T"] < STARTS[2] + READ + 1.2: bad.append("hang cuoi hien qua ngan")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 215, 1020, 420), fill=WHITE, outline=NAVY, r=26, w=5)
    pill(d, W / 2, 272, "ĐÁP ÁN", 56, WHITE, NAVY)
    text(d, (W / 2, 368), "250 Hz", 64, NAVY)
    ftable(d, 450, 3, ratio=1.0)
    k2 = appear(t, M[1] - 0.1, 0.45)
    card(d, (40, 870, 1040, 1300), fill=WHITE, outline=A(ENV, max(0.3, k2)), w=4)
    tube(d, 1080, 0.34, env=1.0, t=t, labels=k2, len_lbl=False)
    if k2 > 0: text(d, (W / 2, 1220), "Ống dài = λ/4", 62, ENV, alpha=k2)

# ---------------- canh 4: Bay - dung v/(2L) cua day cho ong kin ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 690), fill=(254, 242, 242), outline=DRED, w=6)
    text(d, (75, 280), "✗ Dễ tưởng: như dây đàn", 58, DRED, anchor="lm")
    tube(d, 390, 0.68, blow=1.0, t=t)
    text(d, (W / 2, 625), "f = v/(2L) → 250 Hz", 62, DRED)
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        card(d, (40, 730, 1040, 1205), fill=A(WHITE, k2), outline=A(BLUE, k2), w=6)
        text(d, (75, 795), "Đo thật: 125 Hz", 58, BLUE, anchor="lm", alpha=k2)
        tube(d, 960, 0.68, env=k2, t=t, labels=k2, len_lbl=False)
        text(d, (W / 2, 1120), "ống dài = λ/4", 62, ENV, alpha=k2)
    kc = appear(t, M[2], 0.45)
    if kc > 0:
        card(d, (60, 1245, 1020, 1375), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=26, w=5)
        text(d, (W / 2, 1310), "✓ Ống kín: f = v/(4L)", 60, DGREEN, alpha=kc)

# ---------------- canh 5: Gioi han ----------------
def s_gioi(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa tính", 64, NAVY)
    text(d, (W / 2, 440), "khí rung lố ra miệng ống", 62, INK)
    card(d, (40, 600, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    tube(d, 800, 0.34, env=1.0, blow=1.0, t=t, len_lbl=False)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1300), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 290, "THỬ NGHĨ", 58, WHITE, ORANGE, k1)
    text(d, (W / 2, 480), "Ống 0,17 m kêu 500 Hz.", 64, INK, alpha=k1)
    text(d, (W / 2, 600), "Nốt cao kế tiếp", 66, INK, alpha=k1)
    text(d, (W / 2, 720), "bao nhiêu Hz?", 66, DORANGE, alpha=k1)
    cbar(d, 1100, t, 1.2, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + s + READ, "tap") for s in STARTS]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][2], "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-baitapsong-04", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Bài tập về sóng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thổi vào ống bịt một đầu", draw=s_hook, tail=0.3, caps=[
   ("Bịt một đầu, thổi ngang miệng.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Nối thêm ống, thổi lại.", 4.9),
   ("Ghi nốt cơ bản mỗi lần.", 4.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Ống dài gấp đôi, nốt giảm nửa.", 3.4),
   ("Đầu kín là nút, miệng là bụng.", 3.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Tính như dây hai đầu cố định?", 3.2),
   ("Ống kín chỉ chứa λ/4.", 3.0),
   ("Công thức khác dây.", 2.6)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Nốt thật thấp hơn chút.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Ống càng dài, nốt càng trầm.", 6.0)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
