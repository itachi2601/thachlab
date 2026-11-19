# Clip: tn-l11-songdung-01 - Day thun rung bang tay, dau kia buoc chan ghe (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-songdung-01.json (_kiem_so() doi chieu ca mo_hinh f_k = k.v/(2l)):
#   so_lieu_mau (k, f Hz, lam m): 1 2 2 ; 2 4 1 ; 3 6 0,67 voi day rung dai 1,0 m, v = 4 m/s (so minh hoa).
#   Clip chi hien f va so mui (khong hien lam, khong hien do dai mui bang so).
# Bai l11-song-dung (lesson 32): hop exp nam o muc II.2, TRUOC cong thuc l = k.lam/2 (muc II.3).
#   Tranh trung: Cau 0 (bam phim -> f cao hon), Cau 1 (nut-nut = lam/2), Cau 2 (1,2 m 3 bo), Cau 6 (3 bo -> 4 nut:
#   clip KHONG danh dau/dem nut), Cau 7 (1 m, 20 m/s, 30 Hz), bai mau 1 m/20 m/s/40 Hz, thu thach 1,2 m/24 m/s.
# Du doan (K10): dang vung 2 Hz, day 1 mui; vung 4 Hz thi day may mui? Dap an: 2 mui, moi mui ngan bang nua.
# Bay = hien_tuong_hay_sai[0] "mui chay doc day roi bien mat" -> cham bang dinh o cho dung yen khong doi cho.
# Chua noi duoc: moi doi nhip vung, chua doi do cang day (gia_thiet kho: v = 4 m/s cho day cang vua).
# Thu nghi: van 4 Hz, cang nhu cu, day rung chi dai 0,5 m -> may mui? (1 mui: f_1 = 4/(2.0,5) = 4 Hz; ghi trong ghi_chu kho).
#   Can mot buoc suy luan: o 4 Hz moi mui dai nua day 1 m -> day 0,5 m vua 1 mui. Gia tri 0,5 m chua tung hien.
# Hinh day: y = A.sin(pi(k - 0,03)s).cos(2pi f t), s = 0 o chan ghe (nut that), dau tay lech nut mot chut (tay vung nho).
from engine import *

V, L_DAY = 4.0, 1.0
ROWS = [(2, 1), (4, 2), (6, 3)]                       # (f Hz, so mui)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-songdung-01.json")))
    hang = k["so_lieu_mau"]["hang"]
    for f, n in ROWS:
        assert any(r[0] == n and r[1] == f for r in hang), (f, n)
        assert abs(n * V / (2 * L_DAY) - f) < 1e-9          # mo_hinh f_k = k.v/(2l)
    assert "4 m/s" in " ".join(k["mo_hinh"]["gia_thiet"])
    assert abs(1 * V / (2 * 0.5) - 4) < 1e-9                  # thu nghi: 0,5 m, 4 Hz -> 1 mui
    assert "0,5 m" in k["so_lieu_mau"]["ghi_chu"]
_kiem_so()

# ---------------- day rung ----------------
X0, X1 = 190, 890                                      # chan ghe -> tay
AMP = 105
ENV = (214, 226, 250)
def phi(s, n): return math.pi * (n - 0.03) * s
def shape(n, s): return math.sin(phi(s, n))

def _kiem_hinh():
    for n in (1, 2, 3):
        assert abs(shape(n, 0.0)) < 1e-12                        # chan ghe la nut
        assert abs(shape(n, 1.0)) < 0.1                          # dau tay gan nut (tay vung nho)
        nuts = [j / (n - 0.03) for j in range(n)]                # nut trong khoang [0, 1)
        assert len(nuts) == n and all(0 <= x < 1 for x in nuts)  # n mui giua chan ghe va tay
        for j in range(n):                                       # moi mui co mot bung bien do ~ AMP
            sb = (j + 0.5) / (n - 0.03)
            if sb < 1: assert abs(abs(shape(n, sb)) - 1) < 1e-9
_kiem_hinh()

def rope(d, yc, n, tph, ka=1.0, env=True, f=2.0, mark=None):
    """n mui, tph = thoi gian vat li (s), ka = he so bien do (0..1). mark: s cua cham bang dinh."""
    N = 160; c = math.cos(2 * math.pi * f * tph)
    xs = [X0 + (X1 - X0) * i / N for i in range(N + 1)]
    if env and ka > 0.02:
        top = [(x, yc - ka * AMP * abs(shape(n, i / N))) for i, x in enumerate(xs)]
        bot = [(x, yc + ka * AMP * abs(shape(n, i / N))) for i, x in enumerate(xs)]
        d.polygon(top + bot[::-1], fill=ENV)
    pts = [(x, yc - ka * AMP * shape(n, i / N) * c) for i, x in enumerate(xs)]
    d.line(pts, fill=BLUE, width=8, joint="curve")
    # chan ghe + nut buoc
    d.rectangle([X0 - 46, yc - 190, X0 - 14, yc + 260], fill=(150, 110, 70), outline=(100, 70, 40), width=3)
    dot(d, X0 - 8, yc, 13, NAVY)
    # tay
    ye = pts[-1][1]
    d.rounded_rectangle([X1 + 2, ye - 34, X1 + 92, ye + 34], radius=26, fill=(240, 196, 160), outline=(170, 110, 80), width=4)
    if mark is not None:
        i = int(round(mark * N)); dot(d, pts[i][0], pts[i][1], 16, RED, outline=WHITE)
    return pts

def stage(d, yc, n, tph, ka=1.0, f=2.0, labels=True, mark=None, ruler=True):
    card(d, (40, 260, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    if ruler:
        y = yc - 175
        d.line([(X0, y), (X1, y)], fill=MUTED, width=3)
        for x in (X0, X1): d.line([(x, y - 14), (x, y + 14)], fill=MUTED, width=3)
        card(d, (W / 2 - 110, y - 30, W / 2 + 110, y + 30), fill=WHITE, r=14)
        text(d, (W / 2, y), "dài 1 m", 42, INK)
    rope(d, yc, n, tph, ka, f=f, mark=mark)
    if labels:
        text(d, (X0 - 30, yc + 300), "chân ghế", 40, INK)
        text(d, (X1 + 40, yc + 300), "tay vung", 40, INK)

def fpill(d, f, y=870, ka=1.0):
    s = f"Nhịp vung: {f} Hz"
    pw = tw(d, s, F(44)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A((254, 242, 242), ka), r=30)
    text(d, (W / 2, y), s, 44, RED, alpha=ka)

YC = 560
# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    stage(d, YC, 1, t, ka=appear(t, 0.2, 0.8), f=2)
    fpill(d, 2)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Vung nhanh gấp đôi, 4 Hz:", "dây sẽ có mấy múi?")):
        text(d, (W / 2, y0 + 200 + j * 90), s, 50, INK, alpha=a)
    text(d, (W / 2, y0 + 470), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 540, 940, y0 + 554], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 540, 140 + 800 * (1 - p), y0 + 554], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
STABLE = 1.5                                           # giay tu luc doi nhip toi luc ghi hang
def starts(M): return [0.4, 3.6, M[1] + 1.0]
def do_state(t, M):
    """-> (i nhip dang vung, he so bien do, so hang da ghi)."""
    st = starts(M)
    if t < st[0]: return -1, 0.0, 0
    i = max(j for j, s in enumerate(st) if t >= s)
    ka = ease((t - st[i]) / 0.8)
    if i + 1 < len(st): ka = min(ka, 1 - ease((t - (st[i + 1] - 0.35)) / 0.35))
    rows = i + (1 if t >= st[i] + STABLE else 0)
    return i, ka, rows

def ftable(d, y, n, hl=-1):
    card(d, (120, y, 960, y + 100 + 3 * 78), fill=WHITE, outline=NAVY, w=4)
    text(d, (370, y + 50), "Nhịp vung (Hz)", 42, INK); text(d, (760, y + 50), "Số múi", 42, INK)
    d.line([(150, y + 92), (930, y + 92)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 132 + i * 78; f, k = ROWS[i]
        if i == hl: d.rounded_rectangle([140, yy - 32, 940, yy + 32], radius=16, fill=(255, 237, 213))
        text(d, (370, yy), str(f), 44, INK); text(d, (760, yy), str(k), 44, BLUE)

def s_do(img, d, t, sc):
    M = sc["M"]; i, ka, rows = do_state(t, M)
    f, n = ROWS[max(i, 0)]
    stage(d, YC, n, t, ka=ka if i >= 0 else 0.0, f=f)
    if i >= 0: fpill(d, f)
    ftable(d, 980, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: hang chi ghi khi day da on dinh (bien do du) ; o nhip luon khop so mui dang ve."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []
    st = starts(M)
    while t < sc["T"]:
        i, ka, rows = do_state(t, M)
        if rows > i + 1: bad.append((round(t, 2), "hang som"))
        if i >= 0 and rows == i + 1 and t < st[i] + STABLE - 1e-9: bad.append((round(t, 2), "hang truoc khi on dinh"))
        if i >= 0 and rows == i + 1 and ka < 0.99 and (i + 1 >= len(st) or t < st[i + 1] - 0.35): bad.append((round(t, 2), "ghi khi chua on dinh"))
        t += 0.05
    for j in range(len(st) - 1):
        if st[j] + STABLE > st[j + 1] - 0.35: bad.append(f"nhip {j} chua kip ghi")
    if do_state(sc["T"] - 0.05, M)[2] != 3: bad.append("chua du 3 hang cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def mini(d, yc, n, t, f, lab):
    N = 120; c = math.cos(2 * math.pi * f * t)
    xs = [X0 + (X1 - X0) * i / N for i in range(N + 1)]
    am = 70
    top = [(x, yc - am * abs(shape(n, i / N))) for i, x in enumerate(xs)]
    bot = [(x, yc + am * abs(shape(n, i / N))) for i, x in enumerate(xs)]
    d.polygon(top + bot[::-1], fill=ENV)
    d.line([(x, yc - am * shape(n, i / N) * c) for i, x in enumerate(xs)], fill=BLUE, width=7, joint="curve")
    d.rectangle([X0 - 30, yc - 90, X0 - 10, yc + 90], fill=(150, 110, 70))
    text(d, (W / 2, yc - 112), lab, 42, INK)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: 2 múi", 310, appear(t, 0.15, 0.4))
    card(d, (40, 380, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    mini(d, 560, 1, t, 2, "2 Hz: 1 múi")
    mini(d, 840, 2, t, 4, "4 Hz: 2 múi")
    k1 = appear(t, M[0] + 0.6, 0.45)
    if k1 > 0:
        card(d, (60, 1030, 1020, 1170), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1100), "Nhịp gấp đôi → số múi gấp đôi", 46, (21, 128, 61), alpha=k1)
    k2 = appear(t, M[1] - 0.05, 0.45)
    if k2 > 0:
        card(d, (60, 1210, 1020, 1420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=5)
        text(d, (W / 2, 1275), "Sóng dội lại ở chân ghế:", 46, INK, alpha=k2)
        text(d, (W / 2, 1355), "hai sóng ngược chiều tạo múi", 46, BLUE, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
SM = 1 / (2 - 0.03)                                    # nut giua day (4 Hz, 2 mui)
def s_bay(img, d, t, sc):
    M = sc["M"]
    stage(d, YC, 2, t, f=4, mark=SM, labels=False, ruler=False)
    xm = X0 + (X1 - X0) * SM
    for yy in range(YC - 150, YC + 150, 26):            # vach goc doc qua cham do
        d.line([(xm, yy), (xm, yy + 12)], fill=GRAY, width=3)
    fpill(d, 4, y=860)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 980
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        for j, q in enumerate(("“Múi chạy dọc dây", "rồi biến mất”")):
            f = F(46); lw = tw(d, q, f); yy = y + 160 + j * 66
            text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)],
                       fill=A(RED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 330), "✓ Chấm đỏ đứng yên một chỗ", 44, (10, 80, 40), alpha=a1 * appear(t, 2.2, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 170), "Mới đổi nhịp vung.", 46, INK, alpha=kk)
        text(d, (W / 2, y + 240), "Căng dây hơn thì sao?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: van 4 Hz, day rung chi dai 0,5 m -> may mui?"""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Vung càng nhanh,", 50, (21, 128, 61), alpha=k0)
    text(d, (W / 2, 450), "dây càng nhiều múi", 50, (21, 128, 61), alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Vẫn 4 Hz, căng như cũ,", "dây rung chỉ dài 0,5 m:", "có mấy múi?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (110, 1030, 970, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1080), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1180), "Dây 1 m, 4 Hz: 2 múi đều nhau", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + s, "tap") for s in starts(do["M"])]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-songdung-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Sóng dừng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dây thun rung bằng tay", draw=s_hook, tail=0.3, caps=[
   ("Một đầu buộc chân ghế, tay vung đều.", 3.6),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.7, caps=[
   ("Tăng dần nhịp vung, đếm số múi.", 4.6),
   ("Giữ đều tay rồi mới ghi.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Vung nhanh gấp đôi: hai múi.", 4.0),
   ("Vì sao dây chia múi?", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 4.6),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.8)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
