# Clip: tn-l11-dotansoam-02 - Do tan so am thoa bang dien thoai: ghi am, phong to dang song, dem chu ki (18/11/2026, lo 5)
# dung lai 27/11/2026 theo cong moi: chu ve >= 55 px (ra >= 48), moi nhip >= 2,5 s, Du doan khong nut A-D (K10),
#   "Dung lai, tu doan" + thanh dem >= 5 s; canh Dap an rieng; Bay hai khung + the dung; canh Gioi han rieng; THU NGHI
#   khong goi y (cau chot can mot buoc suy luan khong co tren man, dap so khong hien tren man).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dotansoam-02.json:
#   f nguon = 440 Hz (tham_so), N = 10 chu ki; so_lieu_mau t = 22,6 / 22,8 / 22,7 ms -> f = 442,5 / 438,6 / 440,5 Hz,
#   trung binh ~ 440,5 Hz. Kiem: _kiem_so() (assert khi nap).
# Du doan (khung 6 o): "Am thoa 440 Hz. Doan 10 chu ki tren dang song dai bao lau?" -> ~22,7 ms.
# Bay = hien_tuong_hay_sai[1] (quen doi ms ra s). DOI CA so voi Du doan (khong lap cap 10 chu ki / 22,6 ms):
#   8 chu ki cua chinh am thoa 440 Hz = 18,2 ms -> de tuong 8/18,2 = 0,44 Hz; dung 8/0,0182 = 440 Hz (cong B: 20 ms mau thuan 440 Hz).
# Gioi han = giong noi, song khong deu (chua_noi cua kho).
# THU NGHI (= cau_chot khung web; ca ghi trong kho ghi_chu): am thoa 440 Hz, chi dem N = 2 chu ki, doc t lech 0,1 ms
#   (doc t sai +-0,1 ms) -> f nam trong khoang 430-450 Hz (2/4,645 ms = 430,6 ; 2/4,445 ms = 449,9). Hoi KHOANG (khong hoi "lech 10 Hz")
#   vi so 10 hien tren man (N = 10). Nhieu: 438-442 Hz (do lech khi dem 10 chu ki, gan bang tren man).
from engine import *
import copy

F0, N = 440, 10
ROWS = [(1, 22.6, 442.5), (2, 22.8, 438.6), (3, 22.7, 440.5)]
F_TB = 440.5
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

SCR_BG = (18, 26, 48); WAVE = (74, 222, 128); SEL = (250, 204, 21); GRID = (52, 64, 96); SCR_TXT = (190, 200, 225)
DGREEN, DPURPLE, DRED, DORANGE = (21, 110, 55), (91, 33, 182), (185, 28, 28), (176, 64, 8)
HL = (255, 237, 213); LRED = (254, 202, 202)

def _kiem_so():
    for n, tt, f in ROWS:
        assert abs(N / (tt / 1000) - f) < 0.05, (n, tt, f)
        assert abs(tt - N * 1000 / F0) < 0.15, ("t xa mo hinh", tt)
    assert abs(sum(r[2] for r in ROWS) / 3 - F_TB) < 0.05
    assert abs(8 / F0 * 1000 - 18.2) < 0.05 and abs(8 / 18.2 - 0.44) < 0.005 and abs(8 / 0.0182 - F0) < 0.5   # bay
    hi, lo = 2 / (2000 / F0 - 0.1) * 1000, 2 / (2000 / F0 + 0.1) * 1000          # cau chot: N = 2, lech 0,1 ms
    assert 449 < hi < 451 and 430 < lo < 431, (hi, lo)
    hi10, lo10 = 10 / (10000 / F0 - 0.1) * 1000, 10 / (10000 / F0 + 0.1) * 1000  # nhieu A: dem 10 chu ki
    assert 441.5 < hi10 < 442.5 and 437.5 < lo10 < 438.5, (hi10, lo10)
    import json, os
    k = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..",
                                    "content", "thi-nghiem", "tn-l11-dotansoam-02.json")))
    assert "N = 2" in k["so_lieu_mau"]["ghi_chu"] and "0,1 ms" in k["so_lieu_mau"]["ghi_chu"]
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

# ---------------- man hinh ung dung ghi am ----------------
PXMS = 34.0                      # px / ms tren dang song phong to
P = 1000.0 / F0 * PXMS           # 1 chu ki = 77,3 px
SX = 150                         # doan chon luon bat dau o mot dinh tai x = 150
AMP = [130, 112, 96]             # am thoa tat dan: doan sau bien do nho hon
WIN = [0.18, 0.5, 0.8]           # vi tri doan trong ban ghi (dai tren cung)

def screen(d, oy, amp, win, shift=0.0, sel=None, counts=0):
    """oy: dich doc. shift (px): dang song dang cuon. sel = (x0, x1) vung chon. counts: so chu ki da dem (0..10)."""
    X0, X1, Y0, Y1 = 60, 1020, 230 + oy, 800 + oy
    card(d, (X0, Y0, X1, Y1), fill=SCR_BG, r=30)
    by0, by1 = Y0 + 30, Y0 + 100
    text(d, (X0 + 40, (by0 + by1) / 2), "bản ghi", 55, SCR_TXT, anchor="lm")
    bx0, bx1 = X0 + 270, X1 - 40
    for i in range(50):
        x = lerp(bx0, bx1, i / 49); h = 28 * math.exp(-1.2 * i / 49) + 3
        d.line([(x, (by0 + by1) / 2 - h), (x, (by0 + by1) / 2 + h)], fill=GRID if i % 2 else (70, 110, 90), width=5)
    wx = lerp(bx0, bx1, win)
    d.rectangle([wx - 24, by0 - 4, wx + 24, by1 + 4], outline=SEL, width=5)
    cy = Y0 + 380
    d.line([(X0 + 30, cy), (X1 - 30, cy)], fill=GRID, width=2)
    if sel:
        x0, x1 = sel
        d.rectangle([x0, cy - 145, x1, cy + 145], fill=(250, 204, 21, 60))
        d.line([(x0, cy - 145), (x0, cy + 145)], fill=SEL, width=5)
        if x1 - x0 > 3: d.line([(x1, cy - 145), (x1, cy + 145)], fill=SEL, width=5)
    pts = [(x, cy - amp * math.cos(2 * math.pi * (x - SX + shift) / P)) for x in range(X0 + 30, X1 - 30, 3)]
    d.line(pts, fill=WAVE, width=6, joint="curve")
    for j in range(1, counts, 2):                                   # so 2, 4, ... 10 (cong B: to, thua)
        text(d, (SX + (j + 0.5) * P, cy - 195), str(j + 1), 62, SEL)
    return cy

def readout(d, y, t_txt):
    card(d, (60, y, 1020, y + 120), fill=WHITE, outline=LIGHT, w=3)
    text(d, (290, y + 60), f"N = {N} chu kì", 58, INK)
    d.line([(540, y + 24), (540, y + 96)], fill=LIGHT, width=3)
    text(d, (780, y + 60), t_txt, 58, BLUE)

# ---------------- canh 1: Du doan (K10: cau hoi + hinh, khong nut lua chon) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    screen(d, 0, AMP[0], WIN[0], shift=t * 45)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 75, "DỰ ĐOÁN", 58, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 180), "Âm thoa 440 Hz.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Đoạn 10 chu kì trên", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "dạng sóng dài bao lâu?", 62, DPURPLE, alpha=a)
    cbar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (chon doan, dem chu ki, doc t, ghi bang) ----------------
SEG = [(0.6, 2.2), (4.0, 1.3), (6.3, 1.3)]   # (bat dau keo vung chon, thoi gian keo) moi lan
SCROLL = 0.5
def do_state(t):
    """-> (lan k, shift px, bien do, x1 vung chon hoac None, so chu ki da dem, chuoi t, so hang da ghi)."""
    k = 0
    for i in range(1, len(SEG)):
        if t >= SEG[i - 1][0] + SEG[i - 1][1] + 0.7: k = i
    s, g = SEG[k]; shift, amp, scrolling = 0.0, AMP[k], False
    if k > 0:
        tc = SEG[k - 1][0] + SEG[k - 1][1] + 0.7
        q = clamp((t - tc) / SCROLL)
        if q < 1: scrolling = True; shift = ease(q) * 3 * P; amp = lerp(AMP[k - 1], AMP[k], ease(q))
    rows = sum(1 for (s2, g2) in SEG if t >= s2 + g2 - 1e-9)
    if t < s or scrolling: return k, shift, amp, None, 0, "t = …", rows
    q = clamp((t - s) / g)
    L = ROWS[k][1] * PXMS
    x1 = SX + L * ease(q)
    cnt = min(N, int((x1 - SX) / P + 1e-6))
    done = t >= s + g - 1e-9
    return k, shift, amp, x1, (N if done else cnt), (f"t = {vn(ROWS[k][1])} ms" if done else "t = …"), rows

TX = [190, 540, 860]; RH = 96
def table(d, rows, TY0, kf=None, hl=-1):
    """kf: do hien cot f moi hang (None = chua co cot f)."""
    if rows <= 0: return
    card(d, (60, TY0 - 60, 1020, TY0 + 50 + rows * RH + 16), fill=WHITE, outline=LIGHT, w=3)
    text(d, (TX[0], TY0), "Lần", 56, INK); text(d, (TX[1], TY0), "t (ms)", 56, INK)
    if kf is not None: text(d, (TX[2], TY0), "f (Hz)", 56, INK, alpha=max(kf))
    d.line([(80, TY0 + 42), (1000, TY0 + 42)], fill=LIGHT, width=3)
    for j in range(rows):
        y = TY0 + 50 + RH * j + RH / 2
        if j == hl: d.rounded_rectangle([80, y - 40, 1000, y + 40], radius=14, fill=HL)
        n, tt, f = ROWS[j]
        text(d, (TX[0], y), str(n), 58, NAVY); text(d, (TX[1], y), vn(tt), 58, INK)
        if kf is not None and kf[j] > 0: text(d, (TX[2], y), vn(f), 58, BLUE, alpha=kf[j])

def s_do(img, d, t, sc):
    k, shift, amp, x1, cnt, ttxt, rows = do_state(t)
    screen(d, 0, amp, WIN[k], shift=shift, sel=(SX, x1) if x1 is not None else None, counts=cnt)
    readout(d, 830, ttxt)
    hl = rows - 1 if rows > 0 and ttxt != "t = …" else -1
    table(d, rows, 1030, hl=hl)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.1, 0.3)
    card(d, (60, 215, 1020, 345), fill=A((21, 110, 52), k0), r=30)
    text(d, (W / 2, 280), "ĐÁP ÁN · khoảng 22,7 ms", 58, WHITE, alpha=k0)
    k1 = appear(t, M[1], 0.4)
    kf = [k1, k1, k1]
    table(d, 3, 480, kf=kf)
    if k1 > 0:
        card(d, (50, 880, 1030, 1150), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
        text(d, (W / 2, 955), "f = N / t, t đổi ra giây", 58, BLUE, alpha=k1)
        text(d, (W / 2, 1070), "10 / 0,0226 s ≈ 442,5 Hz", 60, INK, alpha=k1)
    km = appear(t, M[2], 0.4)
    if km > 0:
        card(d, (60, 1200, 1020, 1330), fill=A((236, 253, 243), km), outline=A(GREEN, km), w=5)
        text(d, (W / 2, 1265), "Trung bình ≈ 440,5 Hz", 60, DGREEN, alpha=km)

# ---------------- canh 4: Bay - quen doi ms ra s (ca khac: 8 chu ki / 20 ms) ----------------
PB = P
def mini_wave(d, y, t, n=8, a=1.0):
    X0 = 90; x0 = 150; x1 = x0 + n * PB
    d.rectangle([x0, y - 95, x1, y + 95], fill=(250, 204, 21, int(55 * a)))
    pts = [(x, y - 80 * math.cos(2 * math.pi * (x - x0) / PB)) for x in range(X0 + 10, 990, 3)]
    d.line(pts, fill=A(WAVE, a), width=6, joint="curve")
    return x0, x1

def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 820), fill=(254, 242, 242), outline=DRED, w=6)
    text(d, (75, 280), "✗ Chia ngay", 58, DRED, anchor="lm")
    card(d, (70, 330, 1010, 650), fill=SCR_BG, r=26)
    x0, x1 = mini_wave(d, 470, t)
    text(d, ((x0 + x1) / 2, 605), "8 chu kì · t = 18,2 ms", 56, SEL)
    text(d, (W / 2, 740), "f = 8 / 18,2 = 0,44 Hz", 62, DRED)
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        card(d, (40, 860, 1040, 1180), fill=A(WHITE, k2), outline=A(BLUE, k2), w=6)
        text(d, (75, 925), "Đổi: 18,2 ms = 0,0182 s", 58, BLUE, anchor="lm", alpha=k2)
        text(d, (W / 2, 1080), "f = 8 / 0,0182 ≈ 440 Hz", 62, INK, alpha=k2)
    kc = appear(t, M[2], 0.45)
    if kc > 0:
        card(d, (60, 1220, 1020, 1350), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=26, w=5)
        text(d, (W / 2, 1285), "✓ 0,44 Hz: tai không nghe", 60, DGREEN, alpha=kc)

# ---------------- canh 5: Gioi han ----------------
def s_gioi(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Giọng nói: sóng không đều", 60, INK)
    card(d, (60, 610, 1020, 1000), fill=SCR_BG, r=26)
    cy, sh = 805, t * 160
    pts = []
    for x in range(90, 990, 3):
        u = (x + sh) / P
        pts.append((x, cy - 120 * (0.55 * math.cos(2 * math.pi * u) + 0.3 * math.cos(2 * math.pi * 2.7 * u + 1)
                                   + 0.15 * math.cos(2 * math.pi * 5.3 * u)) * (0.6 + 0.4 * math.sin(u * 0.7))))
    d.line(pts, fill=WAVE, width=6, joint="curve")

# ---------------- canh 6: THU NGHI (= cau_chot khung web), khong goi y ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1300), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 290, "THỬ NGHĨ", 58, WHITE, ORANGE, k1)
    text(d, (W / 2, 450), "Âm thoa 440 Hz, đếm 2 chu kì,", 62, INK, alpha=k1)
    text(d, (W / 2, 570), "đọc t sai ±0,1 ms.", 62, INK, alpha=k1)
    text(d, (W / 2, 690), "f nằm trong khoảng nào?", 64, DORANGE, alpha=k1)
    cbar(d, 1100, t, 1.2, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + s + g, "tick") for s, g in SEG]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][2], "ding"), (e["t0"] + 0.15, "open")]
    return out

def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, shift, amp, x1, cnt, ttxt, rows = do_state(t)
        done = ttxt != "t = …"
        if done:
            if ttxt != f"t = {vn(ROWS[k][1])} ms" or rows != k + 1 or cnt != N: bad.append((round(t, 2), "ghi", k, rows))
            if abs((x1 - SX) - ROWS[k][1] * PXMS) > 0.5: bad.append((round(t, 2), "vung chon", x1))
        else:
            if rows != k: bad.append((round(t, 2), "hang som", k, rows))
        if cnt > 0 and x1 is not None and x1 - SX < cnt * P - 0.2 * PXMS: bad.append((round(t, 2), "dem truoc vung chon"))
        t += 0.05
    if SEG[-1][0] + SEG[-1][1] > sc["T"] - 0.5: bad.append("lan do cuoi sat het canh")
    return bad

CLIP = dict(id="tn-l11-dotansoam-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo tần số âm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Âm thoa và điện thoại", draw=s_hook, tail=0.3, caps=[
   ("Ghi âm tiếng âm thoa.", 3.2),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chọn đúng 10 chu kì.", 4.2),
   ("Làm lại ở hai đoạn khác.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đáp án: cỡ 22,7 ms.", 2.9),
   ("Đổi t ra giây rồi chia.", 2.9),
   ("Ba lần gần nhau.", 2.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("8 chu kì trong 18,2 ms.", 3.4),
   ("Đổi ms ra giây trước.", 3.0),
   ("Số nhỏ, vô lí.", 2.6)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Khó đếm chu kì.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự tính.", 6.2)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
