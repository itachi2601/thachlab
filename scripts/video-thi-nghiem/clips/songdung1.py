# Clip: tn-l11-songdung-01 - Day thun rung bang tay, dau kia buoc chan ghe (lo 11, 19/11/2026;
# dung lai 27/11/2026 theo cong moi: chu ve >= 55 px (ra >= 48), moi nhip >= 2,5 s, Du doan khong nut A-D (K10),
# thanh dem day 70 px, Bay hai khung tu giai thich, Gioi han rieng, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-songdung-01.json (_kiem_so() doi chieu ca mo_hinh f_k = k.v/(2l)):
#   so_lieu_mau (k, f Hz, lam m): 1 2 2 ; 2 4 1 ; 3 6 0,67 voi day rung dai 1,0 m, v = 4 m/s (so minh hoa).
#   Clip chi hien f va so mui (khong hien lam, khong hien do dai mui bang so).
# Bai l11-song-dung (lesson 32): hop exp nam o muc II.2, TRUOC cong thuc l = k.lam/2 (muc II.3).
#   Tranh trung: Cau 0 (bam phim -> f cao hon), Cau 1 (nut-nut = lam/2), Cau 2 (1,2 m 3 bo), Cau 6 (3 bo -> 4 nut:
#   clip KHONG danh dau/dem nut), Cau 7 (1 m, 20 m/s, 30 Hz), bai mau 1 m/20 m/s/40 Hz, thu thach 1,2 m/24 m/s.
# Du doan (K10): dang vung 2 Hz, day 1 mui; vung 4 Hz thi day may mui? Dap an: 2 mui, moi mui ngan bang nua.
# Bay = hien_tuong_hay_sai[0] "mui chay doc day roi bien mat": khung tren (de tuong) buou chay doc day, cham do chay theo ;
#   khung duoi (that) 2 mui dung tai cho, cham do o nut giua khong doi cho.
# Gioi han: moi doi nhip vung, chua doi do cang day (gia_thiet kho: v = 4 m/s cho day cang vua).
# THU NGHI (= cau_chot khung web; doi theo cong B 27/11): day 1 m rut con 0,5 m, cang nhu cu, muon 2 mui vung bao nhieu Hz? -> 8 Hz (f = 2.4/(2.0,5)); can buoc "day ngan nua -> f gap doi", 8 khong hien tren man.
#   Buoc suy luan chua chieu: moi mui them can them 2 Hz (f ti le so mui). 8 Hz va "4 mui" KHONG hien tren man
#   (8 Hz nam trong tham_so f max cua kho).
# Hinh day: y = A.sin(pi(k - 0,03)s).cos(2pi f t), s = 0 o chan ghe (nut that), dau tay lech nut mot chut (tay vung nho).
from engine import *

V, L_DAY = 4.0, 1.0
ROWS = [(2, 1), (4, 2), (6, 3)]                       # (f Hz, so mui)
DGREEN, DPURPLE, DRED, DORANGE = (21, 110, 55), (91, 33, 182), (185, 28, 28), (176, 64, 8)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-songdung-01.json")))
    hang = k["so_lieu_mau"]["hang"]; tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    for f, n in ROWS:
        assert any(r[0] == n and r[1] == f for r in hang), (f, n)
        assert abs(n * V / (2 * L_DAY) - f) < 1e-9          # mo_hinh f_k = k.v/(2l)
    assert "4 m/s" in " ".join(k["mo_hinh"]["gia_thiet"])
    assert abs(4 * V / (2 * L_DAY) - 8) < 1e-9 and tp["f"]["max"] >= 8   # cau chot: 4 mui -> 8 Hz
_kiem_so()
assert abs(2 * V / (2 * 0.5) - 8) < 1e-9                    # cau chot (cong B): l = 0,5 m, 2 mui -> 8 Hz

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 56
    card(d, (cx - pw / 2, cy - size * 0.82, cx + pw / 2, cy + size * 0.82), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem day 70 px, rut tu phai sang trai theo 10 nac (moi nac la mot thay doi hinh ro)."""
    p = clamp((t - t0) / (t1 - t0)); q = math.floor(p * 10 + 1e-9) / 10
    d.rounded_rectangle([140, y, 940, y + 70], radius=35, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 70], radius=35, fill=A(col, a))

# ---------------- day rung ----------------
X0, X1 = 190, 890                                      # chan ghe -> tay
ENV = (214, 226, 250)
def phi(s, n): return math.pi * (n - 0.03) * s
def shape(n, s): return math.sin(phi(s, n))

def _kiem_hinh():
    for n in (1, 2, 3):
        assert abs(shape(n, 0.0)) < 1e-12                        # chan ghe la nut
        assert abs(shape(n, 1.0)) < 0.1                          # dau tay gan nut (tay vung nho)
        nuts = [j / (n - 0.03) for j in range(n)]                # nut trong khoang [0, 1)
        assert len(nuts) == n and all(0 <= x < 1 for x in nuts)  # n mui giua chan ghe va tay
        for j in range(n):
            sb = (j + 0.5) / (n - 0.03)
            if sb < 1: assert abs(abs(shape(n, sb)) - 1) < 1e-9
_kiem_hinh()

def rope(d, yc, n, tph, ka=1.0, env=True, f=2.0, mark=None, amp=105, post=190):
    """n mui, tph = thoi gian vat li (s), ka = he so bien do (0..1). mark: s cua cham bang dinh."""
    N = 160; c = math.cos(2 * math.pi * f * tph)
    xs = [X0 + (X1 - X0) * i / N for i in range(N + 1)]
    if env and ka > 0.02:
        top = [(x, yc - ka * amp * abs(shape(n, i / N))) for i, x in enumerate(xs)]
        bot = [(x, yc + ka * amp * abs(shape(n, i / N))) for i, x in enumerate(xs)]
        d.polygon(top + bot[::-1], fill=ENV)
    pts = [(x, yc - ka * amp * shape(n, i / N) * c) for i, x in enumerate(xs)]
    d.line(pts, fill=BLUE, width=8, joint="curve")
    d.rectangle([X0 - 46, yc - post, X0 - 14, yc + post], fill=(150, 110, 70), outline=(100, 70, 40), width=3)
    dot(d, X0 - 8, yc, 13, NAVY)
    ye = pts[-1][1]
    d.rounded_rectangle([X1 + 2, ye - 34, X1 + 92, ye + 34], radius=26, fill=(240, 196, 160), outline=(170, 110, 80), width=4)
    if mark is not None:
        i = int(round(mark * N)); dot(d, pts[i][0], pts[i][1], 20, RED, outline=WHITE)
    return pts

YC = 520
def stage(d, n, tph, ka=1.0, f=2.0):
    card(d, (40, 215, 1040, 860), fill=WHITE, outline=LIGHT, w=3)
    y = 300
    d.line([(X0, y), (X1, y)], fill=NAVY, width=3)
    for x in (X0, X1): d.line([(x, y - 14), (x, y + 14)], fill=NAVY, width=3)
    card(d, (W / 2 - 120, y - 38, W / 2 + 120, y + 38), fill=WHITE, r=14)
    text(d, (W / 2, y), "dài 1 m", 56, INK)
    rope(d, YC, n, tph, ka, f=f, post=150)
    text(d, (X0 - 20, 790), "chân ghế", 56, INK)
    text(d, (X1 - 10, 790), "tay vung", 56, INK)

def fpill(d, f, y=940, a=1.0):
    pill(d, W / 2, y, f"{f} Hz", 60, WHITE, RED, a)

# ---------------- canh 1: Du doan (K10: chi cau hoi, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    stage(d, 1, t, ka=appear(t, 0.2, 0.8), f=2); fpill(d, 2)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 75, "DỰ ĐOÁN", 58, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 210), "Vung nhanh gấp đôi, 4 Hz:", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 320), "dây có mấy múi?", 64, DPURPLE, alpha=a)
    cbar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
STABLE, STEP = 1.8, 3.6                                # giay tu luc doi nhip toi luc ghi hang ; giay moi nhip
def starts(): return [i * STEP for i in range(3)]
def do_state(t):
    """-> (i nhip dang vung, he so bien do, so hang da ghi)."""
    st = starts()
    i = max(j for j, s in enumerate(st) if t >= s)
    ka = 1.0 if i == 0 else ease((t - st[i]) / 0.8)
    if i + 1 < len(st): ka = min(ka, 1 - ease((t - (st[i + 1] - 0.35)) / 0.35))
    rows = i + (1 if t >= st[i] + STABLE else 0)
    return i, ka, rows

def ftable(d, y, n, hl=-1):
    card(d, (120, y, 960, y + 104 + 3 * 82), fill=WHITE, outline=NAVY, w=4)
    text(d, (370, y + 52), "Nhịp (Hz)", 56, INK); text(d, (760, y + 52), "Số múi", 56, INK)
    d.line([(150, y + 100), (930, y + 100)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 144 + i * 82; f, k = ROWS[i]
        if i == hl: d.rounded_rectangle([140, yy - 36, 940, yy + 36], radius=16, fill=(255, 237, 213))
        text(d, (370, yy), str(f), 58, INK); text(d, (760, yy), str(k), 58, BLUE)

def s_do(img, d, t, sc):
    i, ka, rows = do_state(t)
    f, n = ROWS[i]
    stage(d, n, t, ka=ka, f=f); fpill(d, f)
    ftable(d, 1030, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: hang chi ghi khi day da on dinh (bien do du) ; du 3 hang cuoi canh."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    st = starts()
    while t < sc["T"]:
        i, ka, rows = do_state(t)
        if rows > i + 1: bad.append((round(t, 2), "hang som"))
        if rows == i + 1 and ka < 0.99 and (i + 1 >= len(st) or t < st[i + 1] - 0.35): bad.append((round(t, 2), "ghi khi chua on dinh"))
        t += 0.05
    if do_state(sc["T"] - 0.05)[2] != 3: bad.append("chua du 3 hang cuoi canh")
    if sc["T"] < st[2] + STABLE + 1.2: bad.append("hang cuoi hien qua ngan")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def mini(d, yc, n, t, f, lab):
    rope(d, yc, n, t, f=f, amp=70, post=90)
    text(d, (W / 2, yc - 125), lab, 58, INK)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 215, 1020, 420), fill=WHITE, outline=NAVY, r=26, w=5)
    pill(d, W / 2, 272, "ĐÁP ÁN", 56, WHITE, NAVY)
    text(d, (W / 2, 368), "Hai múi", 64, NAVY)
    card(d, (40, 450, 1040, 1050), fill=WHITE, outline=LIGHT, w=3)
    mini(d, 650, 1, t, 2, "2 Hz: 1 múi")
    mini(d, 930, 2, t, 4, "4 Hz: 2 múi")
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr > 0:
        card(d, (60, 1090, 1020, 1320), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=26, w=5)
        text(d, (W / 2, 1160), "Nhịp gấp đôi,", 62, DGREEN, alpha=kr)
        text(d, (W / 2, 1250), "số múi gấp đôi", 62, DGREEN, alpha=kr)

# ---------------- canh 4: Bay - "mui chay doc day roi bien mat" ----------------
SM = 1 / (2 - 0.03)                                    # nut giua day (4 Hz, 2 mui)
def s_bay(img, d, t, sc):
    M = sc["M"]
    # khung tren: de tuong - mot buou chay tu tay ve chan ghe, cham do chay theo
    card(d, (40, 215, 1040, 680), fill=(254, 242, 242), outline=DRED, w=6)
    text(d, (75, 280), "✗ Dễ tưởng: gợn chạy đi", 58, DRED, anchor="lm")
    yc = 490; N = 160
    pos = 1.02 - ((t * 0.45) % 1.04)                     # tam buou chay tu phai sang trai, lap lai
    pts = [(X0 + (X1 - X0) * i / N, yc - 95 * math.exp(-((i / N - pos) / 0.12) ** 2)) for i in range(N + 1)]
    d.line(pts, fill=BLUE, width=8, joint="curve")
    d.rectangle([X0 - 46, yc - 130, X0 - 14, yc + 130], fill=(150, 110, 70), outline=(100, 70, 40), width=3)
    if 0 <= pos <= 1:
        dot(d, X0 + (X1 - X0) * pos, yc - 95, 20, RED, outline=WHITE)
    # khung duoi: that - 2 mui dung tai cho, cham do o nut giua
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        card(d, (40, 720, 1040, 1230), fill=A(WHITE, k2), outline=A(BLUE, k2), w=6)
        text(d, (75, 785), "Thật: múi đứng tại chỗ", 58, BLUE, anchor="lm", alpha=k2)
        yc2 = 1010
        xm = X0 + (X1 - X0) * SM
        for yy in range(yc2 - 140, yc2 + 140, 26): d.line([(xm, yy), (xm, yy + 12)], fill=GRAY, width=4)
        rope(d, yc2, 2, t, f=4, mark=SM, amp=95, post=130)
    kc = appear(t, M[2] - 0.1, 0.45)
    if kc > 0:
        card(d, (60, 1270, 1020, 1400), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=26, w=5)
        text(d, (W / 2, 1335), "✓ Chấm đỏ không rời chỗ", 60, DGREEN, alpha=kc)

# ---------------- canh 5: Gioi han ----------------
def s_gioi(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Căng dây hơn thì sao?", 62, INK)
    card(d, (40, 600, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    rope(d, 800, 2, t, f=4, amp=95, post=130)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1300), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 290, "THỬ NGHĨ", 58, WHITE, ORANGE, k1)
    text(d, (W / 2, 480), "Dây 1 m rút còn 0,5 m,", 64, INK, alpha=k1)
    text(d, (W / 2, 600), "căng như cũ. Muốn 2 múi,", 64, INK, alpha=k1)
    text(d, (W / 2, 720), "vung bao nhiêu Hz?", 66, DORANGE, alpha=k1)
    cbar(d, 1100, t, 1.2, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + s + STABLE, "tap") for s in starts()]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][2], "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-songdung-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Sóng dừng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dây thun rung bằng tay", draw=s_hook, tail=0.3, caps=[
   ("Một đầu buộc chân ghế.", 3.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Tăng dần nhịp vung, đếm số múi.", 5.0),
   ("Giữ đều tay rồi mới ghi.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Sóng dội lại ở chân ghế.", 3.4),
   ("Hai sóng ngược chiều tạo múi.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Múi có chạy dọc dây?", 3.2),
   ("Nhìn chấm đỏ ở giữa.", 3.2),
   ("Đó là sóng dừng.", 3.0)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Mới đổi nhịp.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
