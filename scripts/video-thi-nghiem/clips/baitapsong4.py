# Clip: tn-l11-baitapsong-04 - Thoi vao ong nhua mot dau kin: not co ban theo chieu dai ong (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapsong-04.json (_kiem_so() doi chieu ca mo_hinh f1 = v/(4L), v = 340):
#   so_lieu_mau (L m, f1 Hz): 0,17 500 ; 0,34 250 ; 0,68 125. Kho ghi "Tinh tu mo hinh" -> man dien thoai ghi "≈".
# Du doan (K10, khong nut A-D): ong 0,17 m keu 500 Hz; noi dai gap doi (0,34 m) -> not co ban? Dap an 250 Hz (giam mot nua).
#   Hop exp cua bai (Rut ra: "L tang thi f1 giam") da lo CHIEU -> cau hoi hoi SO (1000/500/250/125), van con cho nghi.
#   Khong trung Cau 3 (bung tren day 0,9 m), Cau 5 (nut-bung), Thu thach (day 1,2 m).
# Bay = hien_tuong_hay_sai[0]: dung f = v/(2L) cua day cho ong kin -> 0,34 m cho 500 Hz, ma dien thoai do 250 Hz.
# Chua noi duoc = sai_so_thuong_gap[1]: khi rung lo ra ngoai mieng ong (hieu chinh mieng ong) -> ong that keu thap hon chut.
# Thu nghi: ong 0,17 m, not co ban 500 Hz; not cao KE TIEP ong keu duoc? -> 3·500 = 1500 Hz (m le; 1000 Hz la bay "nhu day").
#   Can mot buoc suy luan chua chieu (mau 3λ/4); so 1500 KHONG hien tren man, ghi trong ghi_chu kho.
from engine import *

V = 340
ROWS = [(0.17, 500), (0.34, 250), (0.68, 125)]       # (L m, f1 Hz)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-baitapsong-04.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["v"]["gia_tri"] == V
    for L, f in ROWS:
        assert (L, f) in hang, (L, f)
        assert abs(V / (4 * L) - f) < 0.5, (L, f)        # mo_hinh f1 = v/(4L)
    assert abs(V / (2 * 0.34) - 500) < 0.5               # bay: v/(2L) voi 0,34 m
    assert "1500" in k["so_lieu_mau"]["ghi_chu"]         # cau chot ghi trong kho
_kiem_so()

# ---------------- hinh: ong nam ngang, dau kin ben TRAI, mieng ho ben PHAI ----------------
XC, PX, HH = 120, 1150, 46                            # dau kin x = 120 ; 1150 px/m ; nua chieu cao long ong
TUBE = (226, 232, 240); WALL = (70, 80, 105); AIR = (14, 116, 144); ENV = (124, 58, 237)
SCR = (18, 26, 48); SCR_T = (190, 200, 225); NUM = (74, 222, 128); DGREEN = (10, 80, 40); DRED = (185, 28, 28)

def env_amp(x, Lpx):
    """Bien do dao dong cua khi tai x (px tu dau kin): nut o dau kin, bung o mieng (L = λ/4)."""
    return math.sin(math.pi / 2 * x / Lpx)

def _kiem_vat_li():
    Lp = 0.34 * PX
    assert abs(env_amp(0, Lp)) < 1e-9                    # dau kin: nut
    assert abs(env_amp(Lp, Lp) - 1) < 1e-9               # mieng: bung
    assert all(env_amp(x, Lp) <= env_amp(x + 1, Lp) + 1e-12 for x in range(int(Lp)))   # tang don dieu: chi 1/4 buoc song
    for i in range(1, 3): assert abs(ROWS[i][0] / ROWS[i - 1][0] - 2) < 1e-9 and ROWS[i][1] * 2 == ROWS[i - 1][1]
_kiem_vat_li()

def tube(d, y, Lm, blow=0.0, env=0.0, t=0.0, labels=0.0, len_lbl=True):
    Lpx = Lm * PX; x1 = XC + Lpx
    d.rectangle([XC, y - HH, x1, y + HH], fill=TUBE)
    d.line([(XC, y - HH), (x1, y - HH)], fill=WALL, width=7); d.line([(XC, y + HH), (x1, y + HH)], fill=WALL, width=7)
    d.rectangle([XC - 20, y - HH - 4, XC, y + HH + 4], fill=WALL)                 # nap bit dau kin
    for Lj in (0.17, 0.34):                                                    # khop noi
        if Lj < Lm - 1e-6:
            xj = XC + Lj * PX; d.rectangle([xj - 7, y - HH - 9, xj + 7, y + HH + 9], fill=(150, 156, 172))
    if env > 0:                                                                # duong bao bien do khi
        sw = 0.55 + 0.45 * math.cos(2 * math.pi * 1.4 * t)
        for s in (1, -1):
            pts = [(XC + x, y + s * sw * (HH - 8) * env_amp(x, Lpx)) for x in range(0, int(Lpx) + 1, 6)]
            d.line(pts, fill=A(ENV, env), width=5)
    if labels > 0:
        text(d, (XC + 6, y - HH - 46), "nút", 44, ENV, anchor="lm", alpha=labels)
        text(d, (x1, y - HH - 46), "bụng", 44, ENV, anchor="rm", alpha=labels)
    if blow > 0:                                                               # luong hoi thoi ngang mieng
        xa = x1 + 34
        for k in range(3):
            yy = y - 120 + ((t * 260 + k * 60) % 180)
            d.line([(xa, yy), (xa, yy + 34)], fill=A(AIR, blow), width=6)
        arrow(d, (xa, y - 120), (xa, y + 70), A(AIR, blow), w=5, head=18)
        text(d, (xa, y - 150), "thổi", 40, AIR, alpha=blow)
    if len_lbl:
        d.line([(XC, y + HH + 34), (x1, y + HH + 34)], fill=MUTED, width=3)
        for xx in (XC, x1): d.line([(xx, y + HH + 22), (xx, y + HH + 46)], fill=MUTED, width=3)
        text(d, ((XC + x1) / 2, y + HH + 80), "dài " + vn(Lm) + " m", 44, INK)
    text(d, (XC - 10, y + HH + 34 + (110 if len_lbl else 30)), "đầu kín", 40, MUTED, anchor="lm")

def phone(d, cx, y, f=None, a=1.0):
    card(d, (cx - 230, y, cx + 230, y + 200), fill=A(SCR, a), r=30)
    text(d, (cx, y + 50), "Đo tần số", 38, SCR_T, alpha=a)
    s = "— Hz" if f is None else "≈ " + str(f) + " Hz"
    text(d, (cx, y + 135), s, 66, NUM if f is not None else SCR_T, alpha=a)

def ftable(d, y, n, hl=-1, ratio=0.0):
    card(d, (60, y, 1020, y + 110 + 3 * 80), fill=WHITE, outline=NAVY, w=4)
    text(d, (300, y + 52), "Ống dài (m)", 42, INK); text(d, (760, y + 52), "Nốt cơ bản (Hz)", 42, INK)
    d.line([(90, y + 95), (990, y + 95)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 140 + i * 80; L, f = ROWS[i]
        if i == hl or (ratio > 0 and i <= 1):
            d.rounded_rectangle([80, yy - 34, 1000, yy + 34], radius=16, fill=A((255, 237, 213), max(ratio, 1.0 if i == hl else 0)))
        text(d, (300, yy), vn(L), 44, INK); text(d, (760, yy), str(f), 44, BLUE)
    if ratio > 0:
        yy = y + 140 + 0.5 * 80
        arrow(d, (140, yy - 40), (140, yy + 40), A(ORANGE, ratio), w=5, head=14)
        text(d, (180, yy), "×2", 42, ORANGE, anchor="lm", alpha=ratio)
        arrow(d, (950, yy - 40), (950, yy + 40), A(ORANGE, ratio), w=5, head=14)
        text(d, (910, yy), "÷2", 42, ORANGE, anchor="rm", alpha=ratio)

# ---------------- canh 1: Du doan ----------------
YT = 470
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    bl = appear(t, 0.6, 0.4)
    tube(d, YT, 0.17, blow=bl, t=t)
    phone(d, 640, 700, ROWS[0][1] if t > 1.4 else None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Nối dài gấp đôi: 0,34 m.", "Nốt cơ bản bao nhiêu Hz?")):
        text(d, (W / 2, y0 + 180 + j * 80), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 420), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 495, 940, y0 + 509], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 495, 140 + 800 * (1 - p), y0 + 509], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
STARTS = [0.4, 3.4, 6.4]; GROW = 0.7; READ = 1.6; ROW = 1.9
def do_state(t):
    """-> (i ong dang dung, L dang ve, f dang hien hoac None, so hang da ghi, dang thoi)."""
    i = max([j for j, s in enumerate(STARTS) if t >= s], default=-1)
    if i < 0: return 0, ROWS[0][0], None, 0, False
    s = STARTS[i]; Lprev = ROWS[i - 1][0] if i > 0 else ROWS[0][0]
    L = lerp(Lprev, ROWS[i][0], ease((t - s) / GROW)) if i > 0 else ROWS[0][0]
    growing = i > 0 and t < s + GROW
    blowing = t >= s + (GROW if i > 0 else 0) + 0.2
    f = ROWS[i][1] if t >= s + READ else None
    rows = i + (1 if t >= s + ROW else 0)
    return i, L, f, rows, blowing and not growing

def s_do(img, d, t, sc):
    i, L, f, rows, bl = do_state(t)
    card(d, (40, 260, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    tube(d, YT, L, blow=1.0 if bl else 0.0, t=t)
    phone(d, 640, 700, f)
    ftable(d, 1010, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: so tren dien thoai = f cua ong dang ve ; hang bang chi hien sau khi dien thoai da hien so."""
    bad = []; t = 0.0
    while t < 10.5:
        i, L, f, rows, bl = do_state(t)
        if f is not None:
            if abs(L - ROWS[i][0]) > 1e-9: bad.append((round(t, 2), "so hien khi ong chua noi xong"))
            if abs(V / (4 * L) - f) > 0.5: bad.append((round(t, 2), "so lech ong"))
        if rows > i + 1: bad.append((round(t, 2), "hang som"))
        if rows == i + 1 and f is None: bad.append((round(t, 2), "hang truoc so"))
        t += 0.05
    if do_state(9.9)[3] != 3: bad.append("chua du 3 hang")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: 250 Hz, giảm nửa", 310, appear(t, 0.15, 0.4))
    ftable(d, 390, 3, ratio=appear(t, 0.5, 0.45))
    k2 = appear(t, M[1] - 0.1, 0.5)
    if k2 > 0:
        card(d, (40, 830, 1040, 1560), fill=A(WHITE, k2), outline=A(ENV, k2), w=4)
        tube(d, 1080, 0.34, env=k2, t=t, labels=k2, len_lbl=False)
        kq = appear(t, M[1] + 1.2, 0.5)
        text(d, (W / 2, 1340), "Ống dài = λ/4", 54, ENV, alpha=kq)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    tube(d, YT, 0.34, blow=1.0, t=t)
    phone(d, 640, 700, ROWS[1][1])
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 1010
    if a1 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 1.6) / 0.4)
        for j, q in enumerate(("Dùng f = v/(2L) như dây đàn:", "0,34 m → 500 Hz")):
            f = F(48); lw = tw(d, q, f); yy = y + 165 + j * 76
            text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 340), "✓ Điện thoại đo: 250 Hz", 46, DGREEN, alpha=a1 * appear(t, 2.2, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 180), "Khí rung lố ra khỏi miệng:", 46, INK, alpha=kk)
        text(d, (W / 2, y + 255), "nốt thật thấp hơn chút", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Ống kín dài gấp đôi:", 50, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "nốt cơ bản giảm nửa", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Ống 0,17 m: nốt cơ bản 500 Hz.", "Nốt cao kế tiếp là bao nhiêu Hz?")):
        text(d, (W / 2, 790 + j * 76), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (90, 1030, 990, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1080), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1180), "Đầu kín: nút · miệng: bụng", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + s + READ, "tap") for s in STARTS]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-baitapsong-04", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Bài tập về sóng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thổi vào ống bịt một đầu", draw=s_hook, tail=0.3, caps=[
   ("Bịt một đầu, thổi ngang miệng.", 3.6),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Nối thêm ống, thổi lại.", 4.4),
   ("Ghi nốt cơ bản mỗi lần.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ống dài gấp đôi, tần số giảm nửa.", 3.6),
   ("Đầu kín là nút, miệng là bụng.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 4.8),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.8)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
