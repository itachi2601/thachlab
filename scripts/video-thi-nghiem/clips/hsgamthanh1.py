# Clip: tn-l9-hsgamthanh-01 - Thuoc nhua rung tren mep ban: do cao theo tan so (HSG KHTN 9, CD15, lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-hsgamthanh-01.json (_kiem_so() doi chieu ca mo_hinh f = 25(15/L)^2):
#   so_lieu_mau (L cm, f Hz): 25 9 | 15 25 | 10 56,3 | 5 225 (so minh hoa). ghi_chu: f duoi 20 Hz la ha am, kho nghe.
# Hinh: thuoc rung ve bang QUAT VET MO (khong ve pha theo thoi gian: 25-225 Hz o 30 khung/s bi "chay nguoc" de doc sai);
#   toc do rung doc qua so f va do thi "cung mot khoang thoi gian" (khong ghi so giay de khoi them so ngoai kho).
# Du doan (K10, khong nut A-D): tho 15 cm -> 25 Hz ; tho ngan hon 10 cm: tan so va do cao the nao? -> f lon hon, am cao hon.
#   Khac cau Hinh 2 (doc do thi 500/1000 Hz), cau dinh-day 0,5 ms, cau Mat Trang, cau 680 Hz vao nuoc.
# Bay = hien_tuong_hay_sai[1] + [2] (tho dai rung rong nen keu to va cao; that ra 9 Hz duoi 20 Hz, kho nghe).
#   Khong dung [0] (gay manh -> cao) vi gan y cau Hinh 2 ngay sau hop.
# Chua noi duoc: gia_thiet "f_15 la gia tri minh hoa, tuy loai thuoc".
# Thu nghi: tho 5 cm (225 Hz): mot dao dong mat bao lau? -> T = 1/225 s ≈ 0,0044 s (≈ 4,4 ms) ; T = 1/f hoc o muc III,
#   khong chieu trong clip ; so 0,0044 khong hien tren man, ghi trong ghi_chu kho.
from engine import *

ROWS = [(25, 9), (15, 25), (10, 56.3), (5, 225)]          # so_lieu_mau
def fz(L): return dict(ROWS)[L]
def vn(x): return ("%g" % x).replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-hsgamthanh-01.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    for L, f in ROWS: assert abs(25 * (15 / L) ** 2 - f) / f < 0.03, (L, f)        # mo_hinh
    assert "20 Hz" in k["so_lieu_mau"]["ghi_chu"] and fz(25) < 20
    assert "0,0044" in k["so_lieu_mau"]["ghi_chu"] and abs(1 / 225 - 0.0044) < 5e-5   # ca chot
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert all(tp["L"]["min"] <= L <= tp["L"]["max"] for L, _ in ROWS)
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
RULER = (37, 99, 235); WAVE = (124, 58, 237)

# ---------------- hinh: ban + thuoc + quat rung ----------------
EDGE, TY, PXC, AMP = 330, 560, 26.0, 62       # mep ban x ; mat ban y ; px moi cm ; bien do dau thuoc (px)
def ruler(d, L, vib=True, a=1.0, amp=AMP):
    d.rectangle([40, TY, EDGE, TY + 120], fill=A(WOOD, a), outline=A(WOOD_D, a), width=3)          # ban
    d.rectangle([60, TY - 12, EDGE, TY], fill=A(RULER, a))                                          # phan nam tren ban
    d.rounded_rectangle([210, TY - 92, EDGE - 6, TY - 12], radius=18, fill=A((232, 190, 160), a), outline=A((150, 110, 90), a), width=3)
    x1 = EDGE + L * PXC
    def shape(s): return s * s * (3 - s) / 2          # dang uon thanh cong-xon (chi de ve)
    pts = lambda p: [(EDGE + (x1 - EDGE) * i / 30, TY - 6 + p * amp * shape(i / 30)) for i in range(31)]
    if vib:
        for k in range(-4, 5):
            p = k / 4
            d.line(pts(p), fill=A(RULER, a * (0.5 if abs(k) == 4 else 0.16)), width=12)
    else:
        d.line(pts(0), fill=A(RULER, a), width=12)
    # thuoc do phan tho ra (duoi), chu "tho ra L cm" khong dung ky hieu l
    yb = TY + 160
    d.line([(EDGE, yb), (x1, yb)], fill=A(NAVY, a), width=3)
    for x in (EDGE, x1): d.line([(x, yb - 14), (x, yb + 14)], fill=A(NAVY, a), width=3)
    return x1, yb

def fbox(d, f, a=1.0):
    s = "f = " + (vn(f) + " Hz" if f is not None else "…")
    card(d, (660, 290, 1020, 380), fill=A(NAVY, a), r=20)
    text(d, (840, 335), s, 48, (253, 224, 71), alpha=a)

def graph(d, f, y0=700, a=1.0):
    card(d, (40, y0, 1040, y0 + 270), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (W / 2, y0 + 36), "Đầu thước trong cùng một khoảng thời gian", 38, MUTED, bold=False, alpha=a)
    yc = y0 + 150; x0, x1 = 90, 990
    d.line([(x0, yc), (x1, yc)], fill=A(LIGHT, a), width=3)
    if f is None: return
    WT = 0.2                                             # cua so (chi de ve, khong hien so)
    n = 900 if f > 100 else 300
    pts = [(x0 + (x1 - x0) * i / n, yc - 70 * math.sin(2 * math.pi * f * WT * i / n)) for i in range(n + 1)]
    d.line(pts, fill=A(WAVE, a), width=4)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1060), fill=WHITE, outline=LIGHT, w=3)
    on = t >= 0.8
    x1, yb = ruler(d, 15, vib=on)
    text(d, ((EDGE + x1) / 2, yb + 46), "15 cm", 42, NAVY)
    fbox(d, 25 if on else None)
    graph(d, 25 if on else None, y0=770)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1090 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 54), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 160), "Thò ngắn hơn, 10 cm:", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "âm cao hơn hay trầm hơn?", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 330), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 405, 940, y0 + 419], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 405, 140 + 800 * (1 - p), y0 + 419], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
# (bat dau doi, xong doi, L moi) ; truoc moc dau: L = 15 dang rung
MOVES = [(0.6, 1.3, 10), (3.9, 4.6, 5), (6.6, 7.6, 25)]
ROW_LAG = 0.6
def do_state(t):
    """-> (L dang ve, dang rung?, f doc (None khi dang doi), cac L da co hang)."""
    L, vib, done = 15.0, True, {15}
    for t0, t1, Ln in MOVES:
        if t < t0: break
        if t < t1: L = lerp(L, Ln, ease((t - t0) / (t1 - t0))); vib = False; break
        L = Ln; vib = True
        if t >= t1 + ROW_LAG: done.add(Ln)
    return L, vib, (fz(L) if vib else None), done

def table(d, y, done, hl=()):
    card(d, (40, y, 1040, y + 400), fill=WHITE, outline=NAVY, w=4)
    xs = (300, 760)
    text(d, (xs[0], y + 50), "thò ra (cm)", 40, NAVY); text(d, (xs[1], y + 50), "f (Hz)", 40, WAVE)
    d.line([(70, y + 90), (1010, y + 90)], fill=LIGHT, width=4)
    for i, (L, f) in enumerate(ROWS):
        yy = y + 140 + i * 70
        if L in hl: d.rounded_rectangle([60, yy - 32, 1020, yy + 32], radius=14, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(L), 44, INK)
        if L in done: text(d, (xs[1], yy), vn(f), 44, INK)

def s_do(img, d, t, sc):
    L, vib, f, done = do_state(t)
    card(d, (40, 265, 1040, 690), fill=WHITE, outline=LIGHT, w=3)
    x1, yb = ruler(d, L, vib=vib)
    if vib: text(d, ((EDGE + x1) / 2, yb + 46), vn(L) + " cm", 42, NAVY)
    fbox(d, f)
    graph(d, f, y0=710)
    table(d, 1000, done)

def _kiem_dong_bo():
    """Moi 0,05 s: so f chi hien khi thuoc da dung yen o L moi va dung hang kho ; hang bang chi sau khi da doc."""
    bad = []; t = 0.0; seen = {}
    while t < 11.6:
        L, vib, f, done = do_state(t)
        if vib and abs(L - round(L)) > 1e-9: bad.append((round(t, 2), "rung khi dang doi L"))
        if f is not None and f != fz(int(round(L))): bad.append((round(t, 2), "f lech L"))
        for Lx in done:
            if Lx not in seen: seen[Lx] = t
        if vib: seen.setdefault(("f", int(round(L))), t)
        t += 0.05
    for Lx, _ in ROWS:
        if Lx not in seen: bad.append(("thieu hang", Lx))
        elif seen[Lx] < seen.get(("f", Lx), 99) + 0.5 and Lx != 15: bad.append(("hang som", Lx))
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=40):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: f lớn hơn, âm cao hơn", 300, appear(t, 0.15, 0.4))
    table(d, 370, {L for L, _ in ROWS}, hl=(15, 10))
    k1 = appear(t, M[0] + 1.0, 0.5)
    if k1 > 0:
        card(d, (40, 810, 1040, 1010), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        text(d, (W / 2, 880), "Thò ngắn: rung nhanh, f lớn", 46, DGREEN, alpha=k1)
        text(d, (W / 2, 950), "→ âm cao (bổng)", 46, DGREEN, alpha=k1)

# ---------------- canh 4: Bay ; chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    ks = clamp((t - 1.8) / 0.4); kg = appear(t, 2.5, 0.4)
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    x1, yb = ruler(d, 25, amp=AMP * 1.25)
    text(d, ((EDGE + x1) / 2, yb + 46), "25 cm", 42, NAVY)
    fbox(d, 9)
    y = 790
    if a1 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        q = "“Thò dài, rung rộng: to và cao”"; f = F(46); lw = tw(d, q, f); yy = y + 180
        text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 290), "✓ 9 Hz, dưới 20 Hz:", 46, DGREEN, alpha=a1 * kg)
        text(d, (W / 2, y + 360), "thấy rung, gần như không nghe", 44, DGREEN, alpha=a1 * kg)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 180), "Số Hz ở đây là minh hoạ.", 44, INK, alpha=kk)
        text(d, (W / 2, y + 255), "Thước khác thì sao?", 44, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Thò càng ngắn, rung càng nhanh,", 48, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "âm càng cao", 48, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1330), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Thò 5 cm: rung 225 Hz.", "Một dao động mất bao lâu?")):
        text(d, (W / 2, 810 + j * 90), s, 46, INK, alpha=kq)
    kh = appear(t, M[0] + 4.2, 0.5)
    if kh > 0:
        card(d, (90, 1060, 990, 1290), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1115), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1215), "225 dao động trong 1 giây", 44, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + 0.8, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + t1, "tap") for _, t1, _ in MOVES]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.8, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-hsgamthanh-01", header="HSG KHTN 9 · THÍ NGHIỆM", footer="Âm thanh · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thước rung trên mép bàn", draw=s_hook, tail=0.3, caps=[
   ("Gảy đầu thước thò ra.", 3.2),
   ("Tự trả lời trước khi xem.", 6.7)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Thò ngắn dần, gảy lại.", 6.0),
   ("Rồi cho thò dài.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Rung nhanh thì âm cao.", 3.8),
   ("Rung chậm thì âm trầm.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 5.2),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 8.0)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
