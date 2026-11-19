# Clip: tn-l11-songngangdoc-02 - Song doc tren lo xo slinky: doi nhip day - keo (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-songngangdoc-02.json (_kiem_so() doi chieu mo_hinh lam = v/f):
#   v = 7,0 m/s ; so_lieu_mau (f Hz, lam m): 2 -> 3,5 ; 3,5 -> 2,0 ; 5 -> 1,4 (hang 1 Hz -> 7,0 m de danh cho THU NGHI).
#   Lo xo keo dai 4 m (cac_buoc). Bien do a = 10 cm (tham_so max) de vung nen nhin ro; chieu cham 4 lan
#   (ghi trong ghi_chu kho + gia_thiet "khong xet song phan xa o tay giu dau kia"; kho sinh boi build_thi_nghiem.py -> sua ca hai).
# Bai l11-song-ngang-song-doc (lesson 28): hop exp o muc II.2. Tranh trung: Bay 2 (vung nen tren do thi u - x: clip KHONG ve
#   do thi), Thu suc (nen - dan 0,2 m -> 850 Hz: clip KHONG hien khoang nen - dan), bai mau 680/425 Hz, thu thach 1000 Hz,
#   Bay 1 (phao doi bao xa sau 10 s: clip khong hoi so).
# Du doan (K10): day - keo nhanh hon, 2 Hz len 5 Hz: hai vung nen lien nhau se ra sao? Dap an: gan nhau hon (3,5 -> 1,4 m).
# Bay = hien_tuong_hay_sai[1] "vong danh dau bi day dan toi dau kia" -> vong mau tien - lui quanh vach cu.
# Chua noi duoc: moi doi f, chua doi bien do day.
# Thu nghi: lo xo 4 m, day - keo 1 Hz: co luc nao thay hai vung nen cung luc? (Khong: nen - nen cach 7,0 m > 4 m.)
# Mo hinh u(x, t) = a.cos(2.pi.f.(t - x/v)); vung nen o u = 0 va du/dx < 0 <=> pha 2.pi.f(t - x/v) = 3.pi/2 (mod 2.pi).
from engine import *

V, LX, AM, SLOW = 7.0, 4.0, 0.10, 4.0                 # m/s, m, m, chieu cham 4 lan
ROWS = [(2.0, 3.5), (3.5, 2.0), (5.0, 1.4)]          # (f Hz, nen - nen m)
X0P = [0.25, 0.5, 0.3]                                # vi tri vung nen dau tien luc dung hinh (m)

def vn(x):
    s = f"{x:g}" if abs(x - round(x)) < 1e-9 else f"{x:.1f}"
    return s.replace(".", ",")
def vn1(x): return f"{x:.1f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-songngangdoc-02.json")))
    hang = k["so_lieu_mau"]["hang"]; tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["v"]["gia_tri"] == V and tp["a"]["max"] * 0.01 == AM
    for f, lam in ROWS + [(1.0, 7.0)]:
        assert any(r[0] == f and r[1] == lam for r in hang), (f, lam)
        assert abs(V / f - lam) < 0.01
    assert 7.0 > LX                                       # thu nghi: 1 Hz -> 7 m dai hon lo xo
    g = k["so_lieu_mau"]["ghi_chu"]
    assert "chậm 4 lần" in g and "10 cm" in g
    assert any("phản xạ" in s for s in k["mo_hinh"]["gia_thiet"])
    for f, lam in ROWS: assert AM * 2 * math.pi / lam < 1    # vong khong cham nhau
_kiem_so()

# ---------------- lo xo ----------------
X0, X1 = 140, 940                                    # 0 m -> 4 m
S = (X1 - X0) / LX
NR = 73                                              # so vong (cach nhau 5,6 cm)
MARK = 36                                            # vong dan bang mau (x = 2,0 m)
def u(x, tp, f, ka=1.0): return ka * AM * math.cos(2 * math.pi * f * (tp - x / V))
def comps(tp, f):
    """Vi tri cac vung nen trong [0, LX] luc tp."""
    lam = V / f; x = V * (tp - 0.75 / f); x -= math.floor(x / lam) * lam
    out = []
    while x <= LX + 1e-9: out.append(x); x += lam
    return out

def _kiem_nen():
    """Vung nen tinh theo pha phai trung cho cac vong sit nhat (kiem tren chinh luoi vong dang ve)."""
    for i, (f, lam) in enumerate(ROWS):
        tp = t_freeze(i); cs = comps(tp, f)
        assert abs(cs[0] - X0P[i]) < 1e-6 and abs(cs[1] - cs[0] - lam) < 1e-6
        xs = [j * LX / (NR - 1) + u(j * LX / (NR - 1), tp, f) for j in range(NR)]
        gaps = [(xs[j + 1] - xs[j], (xs[j + 1] + xs[j]) / 2) for j in range(NR - 1)]
        for c in cs:
            near = [g for g in gaps if abs(g[1] - c) < lam / 2]
            gmin = min(near)[1]
            assert abs(gmin - c) < 0.09, (f, c, gmin)          # cho sit nhat cach vung nen tinh < 1 khoang vong
        assert min(g[0] for g in gaps) > 0                      # vong khong de len nhau

def t_freeze(i):
    f = ROWS[i][0]; return X0P[i] / V + 0.75 / f

def spring(d, yc, tp, f, ka=1.0, mark=True):
    xs = [j * LX / (NR - 1) for j in range(NR)]
    d.line([(X0 - 40, yc + 92), (X1 + 40, yc + 92)], fill=LIGHT, width=6)          # san
    for j, x in enumerate(xs):
        px = X0 + (x + u(x, tp, f, ka)) * S
        if j == MARK and mark: continue
        d.ellipse([px - 6, yc - 70, px + 6, yc + 70], outline=(70, 90, 140), width=3)
    if mark:
        x = xs[MARK]; px = X0 + (x + u(x, tp, f, ka)) * S
        d.ellipse([px - 8, yc - 74, px + 8, yc + 74], outline=ORANGE, width=8)
    # hai tay
    pl = X0 + u(0, tp, f, ka) * S; pr = X0 + (LX + u(LX, tp, f, ka)) * S
    d.rounded_rectangle([pl - 70, yc - 30, pl - 10, yc + 30], radius=22, fill=(240, 196, 160), outline=(170, 110, 80), width=4)
    d.rounded_rectangle([pr + 10, yc - 30, pr + 70, yc + 30], radius=22, fill=(240, 196, 160), outline=(170, 110, 80), width=4)

def ruler(d, y):
    d.line([(X0, y), (X1, y)], fill=NAVY, width=3)
    for k in range(9):
        x = X0 + k * 0.5 * S; L = 18 if k % 2 == 0 else 10
        d.line([(x, y), (x, y + L)], fill=NAVY, width=3)
        if k % 2 == 0: text(d, (x, y + 44), str(k // 2), 40, INK)
    text(d, (X1 + 45, y + 44), "m", 40, INK)

def fpill(d, f, y=880, ka=1.0):
    s = f"Đẩy – kéo: {vn(f)} Hz"
    pw = tw(d, s, F(44)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A((254, 242, 242), ka), r=30)
    text(d, (W / 2, y), s, 44, RED, alpha=ka)

YC = 500
def stage(d):
    card(d, (40, 260, 1040, 940), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1010, 305), "quay chậm 4 lần", 40, MUTED, anchor="rm", bold=False)
    ruler(d, 700)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    stage(d); spring(d, YC, t / SLOW, 2.0, ka=appear(t, 0.2, 0.8)); fpill(d, 2.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 980 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Tăng nhịp: 2 Hz → 5 Hz.", "Hai vùng nén liền nhau sẽ ra sao?")):
        text(d, (W / 2, y0 + 190 + j * 86), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 450), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 520, 940, y0 + 534], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 520, 140 + 800 * (1 - p), y0 + 534], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
RUN, STEP = 2.0, 3.6                                  # giay chay truoc khi dung hinh ; giay moi nhip
def starts(): return [0.4 + i * STEP for i in range(3)]
def do_state(t):
    """-> (i, tp vat li, ka, dung hinh?, so hang da ghi)."""
    st = starts()
    if t < st[0]: return -1, 0.0, 0.0, False, 0
    i = max(j for j, s in enumerate(st) if t >= s)
    tf = st[i] + RUN; fz = t >= tf
    tp = t_freeze(i) - (0 if fz else (tf - t) / SLOW)
    ka = ease((t - st[i]) / 0.6)
    rows = i + (1 if t >= tf + 0.8 else 0)
    return i, tp, ka, fz, rows

def bracket(d, xa, xb, y, lab, a=1.0):
    pa, pb = X0 + xa * S, X0 + xb * S
    d.line([(pa, y), (pb, y)], fill=A(ORANGE, a), width=5)
    for p in (pa, pb): d.line([(p, y - 16), (p, y + 16)], fill=A(ORANGE, a), width=5)
    pw = tw(d, lab, F(42)) + 40
    card(d, ((pa + pb) / 2 - pw / 2, y - 76, (pa + pb) / 2 + pw / 2, y - 24), fill=A(WHITE, a), r=16)
    text(d, ((pa + pb) / 2, y - 50), lab, 42, (176, 64, 8), alpha=a)

def ntable(d, y, n, hl=-1):
    card(d, (120, y, 960, y + 96 + 3 * 74), fill=WHITE, outline=NAVY, w=4)
    text(d, (330, y + 48), "f (Hz)", 42, INK); text(d, (720, y + 48), "Nén – nén (m)", 42, INK)
    d.line([(150, y + 90), (930, y + 90)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 128 + i * 74; f, lam = ROWS[i]
        if i == hl: d.rounded_rectangle([140, yy - 31, 940, yy + 31], radius=16, fill=(255, 237, 213))
        text(d, (330, yy), vn(f), 44, INK); text(d, (720, yy), vn1(lam), 44, BLUE)

def s_do(img, d, t, sc):
    i, tp, ka, fz, rows = do_state(t)
    stage(d)
    f = ROWS[max(i, 0)][0]
    spring(d, YC, tp, f, ka=ka if i >= 0 else 0.0)
    if i >= 0: fpill(d, f)
    if fz:
        a = appear(t, starts()[i] + RUN + 0.1, 0.3)
        text(d, (W / 2, 800), "hình đứng lại để đo", 40, MUTED, bold=False, alpha=a)
        cs = comps(tp, f)
        for c in cs: text(d, (X0 + c * S, YC + 130), "nén", 40, (176, 64, 8), alpha=a)
        bracket(d, cs[0], cs[1], 380, vn1(ROWS[i][1]) + " m", a)
    ntable(d, 980, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: hang ghi sau khi dung hinh + do ; nhan o f khop nhip dang chay ; khoang do khop hang bang."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, tp, ka, fz, rows = do_state(t)
        if rows > i + 1: bad.append((round(t, 2), "hang som"))
        if i >= 0 and rows == i + 1 and not fz: bad.append((round(t, 2), "hang truoc khi do"))
        if fz:
            cs = comps(tp, ROWS[i][0])
            if abs(cs[1] - cs[0] - ROWS[i][1]) > 0.01: bad.append((round(t, 2), "khoang do lech bang"))
            if ka < 0.999: bad.append((round(t, 2), "dung hinh khi bien do chua du"))
        t += 0.05
    if do_state(sc["T"] - 0.05)[4] != 3: bad.append("chua du 3 hang cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: gần nhau hơn", 310, appear(t, 0.15, 0.4))
    ntable(d, 390, 3)
    k1 = appear(t, 0.6, 0.45)
    if k1 > 0:
        y = 390 + 128
        arrow(d, (175, y), (175, y + 148), A(ORANGE, k1), w=5, head=16)
        text(d, (200, y + 74), "×2,5", 40, ORANGE, anchor="lm", alpha=k1)
        arrow(d, (905, y), (905, y + 148), A(ORANGE, k1), w=5, head=16)
        text(d, (880, y + 74), ":2,5", 40, ORANGE, anchor="rm", alpha=k1)
    k2 = appear(t, M[1] - 0.05, 0.45)
    if k2 > 0:
        card(d, (60, 760, 1020, 980), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 830), "Vòng dao động dọc phương truyền:", 46, (21, 128, 61), alpha=k2)
        text(d, (W / 2, 910), "sóng dọc", 50, (21, 128, 61), alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    stage(d); spring(d, YC, t / SLOW, 2.0)
    xm = X0 + 2.0 * S                                      # vach cu cua vong mau (2,0 m)
    for yy in range(YC - 110, YC + 100, 24): d.line([(xm, yy), (xm, yy + 12)], fill=GRAY, width=3)
    d.polygon([(xm, YC + 96), (xm - 14, YC + 122), (xm + 14, YC + 122)], fill=ORANGE)
    lo, hi = X0 + (2.0 - AM) * S, X0 + (2.0 + AM) * S
    d.line([(lo, 395), (hi, 395)], fill=ORANGE, width=4)
    for p in (lo, hi): d.line([(p, 383), (p, 407)], fill=ORANGE, width=4)
    text(d, (xm, 355), "±10 cm", 40, (176, 64, 8))
    fpill(d, 2.0)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 980
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        for j, q in enumerate(("“Vòng màu trôi dần", "tới đầu kia”")):
            f = F(46); lw = tw(d, q, f); yy = y + 160 + j * 66
            text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)],
                       fill=A(RED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 330), "✓ Vòng màu về vạch cũ", 44, (10, 80, 40), alpha=a1 * appear(t, 2.2, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 170), "Mới đổi f.", 46, INK, alpha=kk)
        text(d, (W / 2, y + 240), "Đẩy mạnh hơn thì sao?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """THU NGHI: lo xo 4 m, 1 Hz -> co luc nao thay hai vung nen cung luc? (khong: 7 m > 4 m)."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Đẩy – kéo càng nhanh,", 50, (21, 128, 61), alpha=k0)
    text(d, (W / 2, 450), "vùng nén càng sít nhau", 50, (21, 128, 61), alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Lò xo dài 4 m, đẩy – kéo 1 Hz.", "Có lúc nào thấy cùng lúc", "hai vùng nén?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (110, 1030, 970, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1080), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1180), "2 Hz: nén – nén 3,5 m", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + s, "tap") for s in starts()]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-songngangdoc-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Sóng dọc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lò xo slinky trên sàn", draw=s_hook, tail=0.3, caps=[
   ("Đẩy – kéo một đầu, dọc theo trục.", 3.6),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.7, caps=[
   ("Tăng dần nhịp, đo hai vùng nén.", 5.4),
   ("Mỗi nhịp, ghi một hàng.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Nhịp tăng, vùng nén sít lại.", 3.8),
   ("Lực đàn hồi đẩy chỗ nén đi tiếp.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 4.6),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.8)]),
])

_kiem_nen()
_b = _kiem_dong_bo(); assert not _b, _b
