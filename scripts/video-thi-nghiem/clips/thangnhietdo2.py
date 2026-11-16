# Clip: tn-l12-thangnhietdo-02 - Kiem nhiet ke o hai moc: nuoc da dang tan va hoi nuoc dang soi (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-02.json (so lieu minh hoa):
#   so_lieu_mau: lan 1: 0,2 / 99,6 · lan 2: 0,1 / 99,7 · lan 3: 0,3 / 100,1 (°C); sai_so_dc = ±0,5 °C; p_kq = 101,325 kPa
#   mo_hinh.ghi_chu: ap suat 80 kPa -> nuoc soi o khoang 94 °C (dung cho cau chot).
# Khac thangnhietdo1 (tron nuoc) va thangnhietdo4 (ba nhiet ke mot coc): clip nay = hai coc hai moc + bang 3 lan doc + dai sai so.
# KHONG hien trung binh hoi nuoc (bai ghi "em tu tinh" ngay sau hop) va KHONG neu co che "nhiet nhan them dung de chuyen the"
#   (dap an Cau 2 ngay sau hop).
# Du doan (K10: mp4 KHONG ve nut A-D; 4 lua chon cho khung ben canh):
#   "Nhiet ke chia dung, sai so ±0,5 °C, cam vao nuoc da dang tan, doc 3 lan: so doc se ra sao?"
#   A. Dung 0,0 °C ca ba lan
#   B. Quanh 0 °C, lech duoi 0,5 °C     <- DAP AN (0,2 · 0,1 · 0,3)
#   C. Tang dan khi da tan bot          (so doc 0,2 -> 0,1 -> 0,3 khong tang dan)
#   D. Duoi 0 °C vi da lanh hon nuoc
# Bay (hien_tuong_hay_sai 1): "Doc 0,2 °C: nuoc da nay tan o 0,2 °C" -> 0,2 ± 0,5 °C chua 0 °C.
# Chua noi duoc (khong_chung_minh 1, 2): chia deu giua hai moc (vd 50 °C)?; do dung ngoai 0-100 °C?
# Chot THU NGHI (ca moi: 80 kPa va 94 °C chua hien tren man; lay tu mo_hinh.ghi_chu cua kho):
#   "Tren nui, ap suat khi quyen 80 kPa. Nhiet ke nay doc 94 °C trong hoi nuoc soi. Nhiet ke hong?"
#   -> Khong (chua chac hong): ap suat thap hon 1 atm (101,325 kPa) nen nuoc soi duoi 100 °C, ≈ 94 °C; moc 100 °C chi dung o 1 atm.
#   Goi y (hien tre ~2,5 s): "Ap ke luc dau chi bao nhieu?" (cau hoi trung tinh, khong neu cong thuc).
from engine import *

NOTE = (70, 75, 95)
ICE_R = (0.2, 0.1, 0.3)
STM_R = (99.6, 99.7, 100.1)
ICE_S = ("0,2", "0,1", "0,3")
STM_S = ("99,6", "99,7", "100,1")
SCREEN = (134, 239, 172)


def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)


# ---------------- dung cu: coc nuoc da (trai) + coc nuoc soi tren bep (phai) ----------------
def beaker(d, x0, x1, y0, y1, wy, wcol):
    d.rectangle([x0 + 6, wy, x1 - 6, y1 - 6], fill=wcol)
    d.line([(x0 + 6, wy), (x1 - 6, wy)], fill=(110, 160, 220), width=4)
    d.line([(x0, y0), (x0, y1), (x1, y1), (x1, y0)], fill=(90, 120, 160), width=6, joint="curve")


def rig(d, t, n_read, hl_steam=0.0, baro=True):
    """n_read: so lan doc da xong - 1 (-1 = chua doc) -> hai man hinh; hl_steam: 0..1 nhan 'bau trong hoi'."""
    # coc trai: nuoc da dang tan
    text(d, (260, 292), "nước đá đang tan", 44, NOTE)
    beaker(d, 90, 430, 520, 820, 560, (205, 230, 252))
    for (x, y, a) in ((140, 590, 10), (215, 640, 40), (380, 600, -15), (150, 740, 25), (390, 730, 5), (230, 770, -20)):
        pts = [(x + 28 * math.cos(math.radians(a + 45 + 90 * k)), y + 28 * math.sin(math.radians(a + 45 + 90 * k))) for k in range(4)]
        d.polygon(pts, fill=(240, 248, 255), outline=(150, 190, 230))
    d.line([(300, 432), (300, 742)], fill=(90, 96, 110), width=9)        # que: ngap, khong cham day, khong cham da
    dot(d, 300, 746, 10, NAVY)
    card(d, (110, 330, 410, 432), fill=(24, 30, 40), r=16)
    text(d, (260, 381), "—" if n_read < 0 else ICE_S[n_read] + " °C", 48, SCREEN)
    # coc phai: nuoc dang soi, bau nhiet ke trong hoi nuoc
    text(d, (820, 292), "hơi nước đang sôi", 44, NOTE)
    d.rounded_rectangle([660, 824, 980, 850], radius=8, fill=(234, 88, 12))   # bep dang bat
    beaker(d, 650, 990, 520, 820, 700, (190, 218, 248))
    for k in range(6):                                                         # bot soi
        ph = (t * 0.9 + k * 0.31) % 1
        x = 690 + k * 50 + 6 * math.sin(t * 5 + k); y = lerp(805, 712, ph)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=WHITE, width=3)
    for k in range(4):                                                         # hoi nuoc
        ph = (t * 0.5 + k * 0.25) % 1
        cx = 700 + k * 75; cy = lerp(690, 540, ph)
        d.ellipse([cx - 34, cy - 18, cx + 34, cy + 18], fill=A((255, 255, 255), 0.55 * (1 - ph)))
    d.line([(860, 432), (860, 628)], fill=(90, 96, 110), width=9)        # que: bau trong hoi, tren mat nuoc
    dot(d, 860, 632, 10, NAVY)
    card(d, (670, 330, 970, 432), fill=(24, 30, 40), r=16)
    text(d, (820, 381), "—" if n_read < 0 else STM_S[n_read] + " °C", 48, SCREEN)
    if hl_steam > 0:
        d.ellipse([826, 600, 894, 664], outline=A(ORANGE, hl_steam), width=5)
    if baro: pill(d, 775, 896, "áp kế: 101,325 kPa", 44, WHITE, NAVY)


def table(d, n_rows, hl=-1, y0=940):
    card(d, (40, y0, 1040, y0 + 460), fill=WHITE, outline=LIGHT, w=3)
    for x, s in ((150, "Lần"), (450, "Nước đá (°C)"), (820, "Hơi nước (°C)")): text(d, (x, y0 + 50), s, 44, NOTE)
    d.line([(70, y0 + 86), (1010, y0 + 86)], fill=LIGHT, width=3)
    for j in range(n_rows):
        y = y0 + 140 + 76 * j
        if j == hl: d.rounded_rectangle([60, y - 32, 1020, y + 32], radius=14, fill=(255, 237, 213))
        text(d, (150, y), str(j + 1), 46, INK)
        text(d, (450, y), ICE_S[j], 46, BLUE)
        text(d, (820, y), STM_S[j], 46, ORANGE)
    text(d, (W / 2, y0 + 410), "minh hoạ", 44, MUTED, bold=False)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut A-D) ----------------
def s_hook(img, d, t, sc):
    rig(d, t, -1, baro=False)
    a = appear(t, 0.6, 0.5)
    if a <= 0: return
    y0 = 950 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 44, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 165), "Sai số nhiệt kế ±0,5 °C.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "Đọc 3 lần trong nước đá:", 44, INK, alpha=appear(t, 1.1, 0.5))
    text(d, (W / 2, y0 + 340), "số đọc sẽ ra sao?", 50, PURPLE, alpha=appear(t, 1.6, 0.5))
    text(d, (W / 2, y0 + 430), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=appear(t, 1.6, 0.5))
    tc, tend = sc["M"][1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh (3 lan doc, hai man hinh + bang + dong ho cung moc) ----------------
def read_times(): return (1.0, 3.2, 5.4)


def do_state(t):
    """-> (n_read so lan doc xong - 1, k hang moi). Man hinh, hang bang, nhan 'lan/phut' doi CUNG moc."""
    n = -1; kn = 1.0
    for j, a in enumerate(read_times()):
        if t >= a: n = j; kn = ease((t - a) / 0.3)
    return n, kn


def s_do(img, d, t, sc):
    n, kn = do_state(t)
    rig(d, t, n, hl_steam=appear(t, sc["M"][1] + 0.1, 0.4))
    if n >= 0: pill(d, 250, 896, f"lần {n + 1} · phút {n}", 44, WHITE, PURPLE)
    table(d, n + 1, hl=n)


# ---------------- dai sai so (dung chung canh dap an + bay) ----------------
def strip(d, y, lo, hi, ticks, vals, col, title, k=1.0, band=None, band_col=GREEN, x0=130, x1=950):
    Xs = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    text(d, (x0 - 60, y - 92), title, 44, NOTE, anchor="lm")
    if band:
        d.rounded_rectangle([Xs(band[0]), y - 30, Xs(band[1]), y + 30], radius=12, fill=mix(band_col, WHITE, 0.75))
    d.line([(x0, y), (x1, y)], fill=INK, width=4)
    for v, s in ticks:
        d.line([(Xs(v), y - 12), (Xs(v), y + 12)], fill=INK, width=4)
        text(d, (Xs(v), y + 52), s, 44, NOTE, bold=False)
    for j, v in enumerate(vals):
        kk = k if isinstance(k, float) else k[j]
        if kk > 0.05: dot(d, Xs(v), y, 15 * kk, col, outline=WHITE)
    return Xs


# ---------------- canh 3: Dap an ----------------
def s_ket(img, d, t, sc):
    M = sc["M"]
    table(d, 3)
    kb = appear(t, 0.2, 0.4)
    card(d, (40, 262, 1040, 880), fill=WHITE, outline=LIGHT, w=3)
    ks = [appear(t, 0.3 + 0.25 * j, 0.3) for j in range(3)]
    strip(d, 440, -1.0, 1.0, ((-0.5, "−0,5"), (0, "0"), (0.5, "0,5")), ICE_R, BLUE, "Nước đá (°C)", k=ks, band=(-0.5, 0.5))
    strip(d, 740, 99.0, 101.0, ((99.5, "99,5"), (100, "100"), (100.5, "100,5")), STM_R, ORANGE, "Hơi nước (°C)",
          k=[appear(t, 1.1 + 0.25 * j, 0.3) for j in range(3)], band=(99.5, 100.5))
    ka = appear(t, M[1] + 0.2, 0.4)
    if ka > 0:
        s = "ĐÁP ÁN · quanh 0 °C, lệch dưới 0,5 °C"; wd = tw(d, s, F(44)) + 52
        card(d, (W / 2 - wd / 2, 870, W / 2 + wd / 2, 932), fill=A(GREEN, ka), r=31)
        text(d, (W / 2, 901), s, 44, WHITE, alpha=ka)


# ---------------- canh 4: Rut ra + chua noi duoc ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 900, 1040, 1520), fill=WHITE, outline=LIGHT, w=3)          # nua duoi: hai dai sai so nhu canh ket qua
    strip(d, 1080, -1.0, 1.0, ((-0.5, "−0,5"), (0, "0"), (0.5, "0,5")), ICE_R, BLUE, "Nước đá (°C)", band=(-0.5, 0.5))
    strip(d, 1380, 99.0, 101.0, ((99.5, "99,5"), (100, "100"), (100.5, "100,5")), STM_R, ORANGE, "Hơi nước (°C)",
          band=(99.5, 100.5))
    k1 = appear(t, M[0] + 0.1, 0.45)
    if k1 > 0:
        card(d, (50, 262, 1030, 500), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=6)
        text(d, (W / 2, 330), "Mốc 0 °C, 100 °C: quy ước", 48, GREEN, alpha=k1)
        text(d, (W / 2, 425), "Lệch nhỏ: nằm trong sai số dụng cụ", 46, INK, alpha=appear(t, M[0] + 0.7, 0.45))
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        card(d, (50, 530, 1030, 860), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, 592), "Chưa nói được", 48, NAVY, alpha=k2)
        text(d, (90, 690), "• Chia đều ở 50 °C?", 44, INK, anchor="lm", alpha=appear(t, M[1] + 0.2, 0.4))
        text(d, (90, 790), "• Đúng ngoài 0–100 °C?", 44, INK, anchor="lm", alpha=appear(t, M[1] + 0.6, 0.4))


# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    ks = clamp((t - (M[0] + 1.6)) / 0.4)
    mk = M[0] + 2.0                                   # het gach
    n_ln = 1 + (1 if t > mk + 0.6 else 0)
    card(d, (50, 262, 1030, 262 + (300 if n_ln == 1 else 440)), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 320, "BẪY", 44, WHITE, RED)
    q = "“Đọc 0,2 °C: nước đá này tan ở 0,2 °C”"
    text(d, (W / 2, 440), q, 44, INK)
    if ks > 0:
        lw = tw(d, q, F(44)); d.line([(W / 2 - lw / 2, 444), (W / 2 - lw / 2 + lw * ks, 444)], fill=RED, width=6)
    if t > mk: text(d, (W / 2 + tw(d, q, F(44)) / 2 + 28, 440), "✗", 50, RED, alpha=appear(t, mk, 0.3))
    ka = appear(t, mk + 0.6, 0.4)
    if ka > 0:
        s = "→ 0,2 ± 0,5 °C: chứa cả 0 °C"
        text(d, (W / 2, 590), s, 46, GREEN, alpha=ka)
        text(d, (W / 2 + tw(d, s, F(46)) / 2 + 34, 590), "✓", 50, GREEN, alpha=appear(t, mk + 2.2, 0.3))
    # hinh: so doc 0,2 tren truc; khoang ± 0,5 chi ve SAU khi gach
    card(d, (40, 780, 1040, 1380), fill=WHITE, outline=LIGHT, w=3)
    kb = ease((t - mk - 0.2) / 0.6); Y = 1120
    Xs = strip(d, Y, -1.0, 1.0, ((-0.5, "−0,5"), (0, "0"), (0.5, "0,5")), (), BLUE, "Nước đá (°C)")
    if kb > 0:
        a, b = Xs(0.2 - 0.5 * kb), Xs(0.2 + 0.5 * kb)
        d.rounded_rectangle([a, Y - 45, b, Y + 45], radius=14, fill=A(mix(GREEN, WHITE, 0.7), 0.9))
        d.line([(a, Y - 75), (a, Y + 75)], fill=GREEN, width=6); d.line([(b, Y - 75), (b, Y + 75)], fill=GREEN, width=6)
        d.line([(Xs(-1.0), Y), (Xs(1.0), Y)], fill=INK, width=4)
        text(d, ((a + b) / 2, Y - 130), "0,2 ± 0,5", 48, GREEN, alpha=kb)
    dot(d, Xs(0.2), Y, 19, BLUE, outline=WHITE)
    if kb >= 1: dot(d, Xs(0), Y, 13, GREEN, outline=WHITE)


# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    """Hinh: nui + man hinh nhiet ke 94 °C (khong ghi ap suat chuan de khong tra loi san)."""
    d.polygon([(250, 1240), (420, 1010), (590, 1240)], fill=A((180, 190, 205), k))
    d.polygon([(380, 1064), (420, 1010), (460, 1064), (440, 1056), (420, 1072), (400, 1056)], fill=A(WHITE, k))
    text(d, (420, 1205), "80 kPa", 44, NAVY, alpha=k)
    card(d, (640, 1060, 880, 1160), fill=A((24, 30, 40), k), r=16)
    text(d, (760, 1110), "94 °C", 48, SCREEN, alpha=k)


def end_card(d, t, sc, chot, hoi, body, goi_y, hint_at):
    """Nhu chot_hoi cua engine nhung the THU NGHI co theo noi dung: truoc goi y chi toi het hinh, goi y hien thi the dai ra."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, chot, 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + hint_at, 0.5)
    card(d, (40, 620, 1040, lerp(1290, 1580, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 682, "THỬ NGHĨ", 44, WHITE, ORANGE, k1)
    ctext(d, 820, hoi, 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    body(d, t, k1)
    if kh > 0:
        card(d, (110, 1310, 970, 1545), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1365), "Gợi ý", 44, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1468), goi_y, 44, ORANGE, alpha=kh)


def s_end(img, d, t, sc):
    end_card(d, t, sc, "Số đọc nằm trong ±0,5 quanh mốc: nhiệt kế đúng ở hai mốc",
             "Trên núi, hơi nước sôi đọc 94 °C. Nhiệt kế hỏng?",
             _end_body, "Áp kế lúc đầu chỉ bao nhiêu?", 2.9)   # goi y tre ~2,5 s sau cau hoi


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, r, b, e = sc["hook"], sc["do"], sc["ket"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + 0.6, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + a, "tap") for a in read_times()]
    out += [(k["t0"] + k["M"][1] + 0.2, "ding"), (r["t0"] + r["M"][0] + 0.1, "tap"),
            (b["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out


CLIP = dict(id="tn-l12-thangnhietdo-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thang nhiệt độ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kiểm nhiệt kế ở hai mốc", draw=s_hook, tail=0.3, caps=[
   ("Hai cốc, hai mốc.", 2.8),
   ("Chọn đáp án ở khung câu hỏi.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Cách nhau 1 phút.", 3.8),
   ("Bầu đặt trong hơi.", 3.8)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.6, caps=[
   ("Cả sáu số trong dải xanh.", 3.4),
   ("Phù hợp giả thuyết.", 3.8)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.5, caps=[
   ("Nhiệt kế đúng ở hai mốc.", 3.0),
   ("Còn hai câu hỏi.", 4.2)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.4, caps=[
   ("Đọc 0,2 thì đá tan ở 0,2?", 3.8),
   ("Tính cả sai số ±0,5.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Tự trả lời.", 7.8)]),
])
