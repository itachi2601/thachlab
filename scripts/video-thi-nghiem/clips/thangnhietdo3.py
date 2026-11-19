# Clip: tn-l12-thangnhietdo-03 - Binh khi kin ngam nuoc o 5 muc nhiet do, keo dai do thi p theo t toi p = 0 (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-03.json:
#   so_lieu_mau (so lieu minh hoa): (0 °C; 100,0 kPa) (25; 109,2) (50; 118,3) (75; 127,5) (100; 136,6)
#   mo_hinh: p = p0.(1 + alpha.t), alpha = 1/273,15 -> t_cat = -273,15 °C (ghi "≈ -273 °C" tren man)
#   tham_so p0: 80-150 kPa -> hai duong "khi B" (p0 = 80) va "khi C" (p0 = 150) o canh bay, khong ghi so, chi ve duong.
# Khac thangnhietdo1 (tron nuoc nong/lanh) va thangnhietdo4 (ba nhiet ke): clip nay = binh kin + bang + do thi p-t truc co dinh.
# Du doan (K10: mp4 KHONG ve nut A-D; 4 lua chon cho khung ben canh):
#   "Keo dai do thi p theo t toi p = 0: cat truc nhiet do o dau?"
#   A. Ngay tai 0 °C          (nham 0 °C la thap nhat - hien_tuong_hay_sai 1)
#   B. Khoang −100 °C         (nham p giam 1 kPa moi do: 100 kPa -> 100 do)
#   C. Khoang −273 °C         <- DAP AN
#   D. Tuy luong khi trong binh (nham diem cat phu thuoc khi - hien_tuong_hay_sai 2)
# Bay: "Doi luong khi, diem cat doi" (hien_tuong_hay_sai 2) -> luong khi A/B/C (p o 0 °C = 100/80/150 kPa) cung cat ≈ −273 °C.
# Chua noi duoc (khong_chung_minh 1, 2): khi that hoa long truoc −273 °C (diem cat chi la ngoai suy); o 0 K vat ra sao.
# Chot THU NGHI (ban 2 theo cong B: ca can 2 buoc, so 273 °C / 200 kPa chua hien; truc do thi dung o 108 °C, 164 kPa
#   nen duong ke/keo dai khong cham gia tri hoi):
#   "Coi khi li tuong, dun binh toi 273 °C, giu the tich: ap suat khoang bao nhieu?"
#   -> 273 °C ≈ 546 K, gap doi 273 K (0 °C) -> p ≈ 2 x 100,0 = 200 kPa (mo_hinh: p = p0.(1 + t/273,15) = 199,9 ≈ 200 kPa).
#   Goi y (hien tre ~2,5 s, trung tinh): "Doc lai diem 0 °C".
from engine import *

NOTE = (70, 75, 95)
LV = ((0, 100.0, "nước đá đang tan"), (25, 109.2, "nước phòng"), (50, 118.3, "nước ấm"),
      (75, 127.5, "nước nóng"), (100, 136.6, "nước đang sôi"))
TCUT = -273.15


def f1(x): return f"{x:.1f}".replace(".", ",")


def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)


def dashed(d, p1, p2, color, w=5, dash=18, gap=12):
    L = math.dist(p1, p2)
    if L < 1: return
    n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))],
               fill=color, width=w)


# ---------------- dung cu: noi nuoc + binh kin + hai man hinh ----------------
ICE = (200, 228, 252); HOT = (250, 176, 146)


def rig(d, t, wk, n_read, idx, heat):
    """wk: 0..1 mau nuoc (0 = nuoc da, 1 = soi); n_read: so lan doc da xong (-1 = chua doc) -> man hinh;
    idx: muc nuoc dang ngam (nhan duoi noi); heat: 0..1 bep do."""
    # bep
    d.rounded_rectangle([110, 770, 450, 792], radius=8, fill=mix((90, 96, 110), (234, 88, 12), heat))
    # noi
    d.rounded_rectangle([90, 560, 470, 776], radius=26, fill=(214, 220, 230), outline=(110, 118, 135), width=5)
    d.rectangle([60, 572, 92, 590], fill=(110, 118, 135)); d.rectangle([468, 572, 500, 590], fill=(110, 118, 135))
    d.rounded_rectangle([100, 592, 460, 766], radius=20, fill=mix(ICE, HOT, wk))
    d.line([(102, 592), (458, 592)], fill=mix(BLUE, ORANGE, wk), width=4)
    if idx == 0:                                       # da vien
        for (x, y, a) in ((135, 610, 12), (330, 606, -10), (372, 640, 18), (150, 700, -6)):
            pts = [(x + 26 * math.cos(math.radians(a + 45 + 90 * k)), y + 26 * math.sin(math.radians(a + 45 + 90 * k))) for k in range(4)]
            d.polygon(pts, fill=(240, 248, 255), outline=(150, 190, 230))
    if idx == 4:                                       # bot soi
        for k in range(7):
            ph = (t * 0.9 + k * 0.37) % 1
            x = 120 + k * 50 + 8 * math.sin(t * 5 + k); y = lerp(756, 600, ph)
            d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=WHITE, width=3)
    # binh kin (thuy tinh day) chim trong nuoc
    d.ellipse([175, 610, 325, 760], fill=(236, 244, 252), outline=(90, 120, 160), width=5)
    d.rectangle([228, 478, 272, 622], fill=(236, 244, 252), outline=(90, 120, 160), width=5)
    d.rectangle([233, 612, 267, 628], fill=(236, 244, 252))
    d.rounded_rectangle([220, 458, 280, 486], radius=6, fill=NAVY)        # nut kin
    d.line([(250, 458), (250, 432)], fill=NAVY, width=8)                  # ong noi cam bien
    # que nhiet ke
    d.line([(425, 432), (425, 740)], fill=(90, 96, 110), width=9)
    dot(d, 425, 742, 9, NAVY)
    # hai man hinh + nhan (moi ky hieu kem ten)
    text(d, (185, 300), "áp suất p", 44, NOTE)
    text(d, (425, 300), "nhiệt độ t", 44, NOTE)
    card(d, (60, 330, 310, 432), fill=(24, 30, 40), r=16)
    card(d, (330, 330, 520, 432), fill=(24, 30, 40), r=16)
    sp = "—" if n_read < 0 else f1(LV[n_read][1]) + " kPa"
    st = "—" if n_read < 0 else f"{LV[n_read][0]} °C"
    text(d, (185, 381), sp, 46, (134, 239, 172))
    if n_read >= 0: text(d, (220, 530), "minh hoạ", 44, MUTED, bold=False, anchor="rm")   # trai co binh, duoi nut kin
    text(d, (425, 381), st, 46, (134, 239, 172))
    pill(d, 280, 834, LV[idx][2], 44, WHITE, mix(BLUE, ORANGE, wk))


def table(d, n_rows, hl=-1):
    card(d, (560, 270, 1030, 800), fill=WHITE, outline=LIGHT, w=3)
    text(d, (680, 318), "t (°C)", 44, NOTE)
    text(d, (900, 318), "p (kPa)", 44, NOTE)
    d.line([(590, 352), (1000, 352)], fill=LIGHT, width=3)
    for j in range(n_rows):
        y = 400 + 70 * j
        if j == hl: d.rounded_rectangle([580, y - 30, 1010, y + 30], radius=14, fill=(255, 237, 213))
        text(d, (680, y), str(LV[j][0]), 46, INK)
        text(d, (900, y), f1(LV[j][1]), 46, ORANGE)
    if n_rows: text(d, (795, 756), "minh hoạ", 44, MUTED, bold=False)


# ---------------- do thi p - t (truc co dinh tu canh Tien hanh toi het) ----------------
def X(tc): return 150 + (tc + 300) * 2.05
def Y(p): return 1450 - p * 3.3
def pmod(p0, tc): return p0 * (1 - tc / TCUT)       # p = p0.(1 + t/273,15)


def axes(d):
    card(d, (40, 882, 1040, 1570), fill=WHITE, outline=LIGHT, w=3)
    for p in (50, 100, 150):
        d.line([(X(-300), Y(p)), (X(108), Y(p))], fill=(238, 233, 224), width=2)
        text(d, (136, Y(p)), str(p), 44, NOTE, bold=False, anchor="rm")
    for tc in (-200, -100, 0, 100):
        d.line([(X(tc), Y(0) - 10), (X(tc), Y(0) + 10)], fill=INK, width=4)
        text(d, (X(tc), Y(0) + 46), str(tc).replace("-", "−"), 44, NOTE, bold=False)
    d.line([(X(-300), Y(0)), (X(108), Y(0))], fill=INK, width=4)
    d.line([(X(-300), Y(0)), (X(-300), Y(164))], fill=INK, width=4)
    text(d, (X(-300) + 16, 905), "p (kPa)", 44, NOTE, anchor="lm")
    text(d, (1022, Y(0) - 36), "t (°C)", 44, NOTE, anchor="rm")


def points(d, n, k_last=1.0):
    for j in range(n):
        r = 13 * (k_last if j == n - 1 else 1.0)
        if r > 1: dot(d, X(LV[j][0]), Y(LV[j][1]), r, ORANGE, outline=WHITE)


def fit_line(d, k_solid, k_ext, col=NAVY, p0=100.0, t_hi=100.0):
    """k_solid: 0..1 ve doan 0 -> t_hi (net lien); k_ext: 0..1 keo dai net dut tu 0 ve -273,15."""
    if k_solid > 0:
        d.line([(X(0), Y(p0)), (X(t_hi * k_solid), Y(pmod(p0, t_hi * k_solid)))], fill=col, width=5)
    if k_ext > 0:
        te = TCUT * k_ext
        dashed(d, (X(0), Y(p0)), (X(te), Y(pmod(p0, te))), col, w=5)


def cut_mark(d, k):
    if k <= 0: return
    dot(d, X(TCUT), Y(0), 14 * k, RED, outline=WHITE)
    pill(d, 300, 1250, "≈ −273 °C", 46, WHITE, RED, k)
    d.line([(262, 1286), (X(TCUT) + 6, Y(0) - 18)], fill=A(RED, k), width=4)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut A-D) ----------------
def s_hook(img, d, t, sc):
    rig(d, t, 0.0, -1, 0, 0.0)
    table(d, 0)
    a = appear(t, 0.6, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 44, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 170), "Đo p ở 0, 25, 50, 75, 100 °C.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 260), "Kéo dài đồ thị p theo t tới p = 0:", 44, INK, alpha=appear(t, 1.6, 0.5))
    text(d, (W / 2, y0 + 360), "cắt trục nhiệt độ ở đâu?", 50, PURPLE, alpha=appear(t, 2.1, 0.5))
    text(d, (W / 2, y0 + 455), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=appear(t, 2.1, 0.5))
    tc, tend = sc["M"][1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 528, 940, y0 + 540], radius=6, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 528, 140 + 800 * (1 - p), y0 + 540], radius=6, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh (5 muc nhiet do; man hinh, bang, diem cung moc) ----------------
def lv_times():
    return [0.5 + 1.45 * k for k in range(5)]        # bat dau ngam muc k; so doc on dinh sau 0,5 s


def do_state(t):
    """-> (idx muc dang ngam, n_read so lan doc xong - 1, wk mau nuoc, heat, k diem moi).
    Dong bo: nhan muc nuoc, hai man hinh, hang bang, diem do thi doi CUNG moc a + 0,5 s (so da on dinh)."""
    L = lv_times(); n_read = -1; wk = 0.0; kn = 1.0
    for k, a in enumerate(L):
        if t >= a + 0.2:
            prev = (k - 1) / 4 if k > 0 else 0.0
            wk = lerp(prev, k / 4, ease((t - a - 0.2) / 0.3))
        if t >= a + 0.5:
            n_read = k; kn = ease((t - a - 0.5) / 0.3)
    idx = max(n_read, 0)
    heat = 1.0 if idx >= 2 else 0.0
    return idx, n_read, wk, heat, kn


def s_do(img, d, t, sc):
    idx, n_read, wk, heat, kn = do_state(t)
    rig(d, t, wk, n_read, idx, heat)
    table(d, n_read + 1, hl=n_read)
    axes(d)
    points(d, n_read + 1, kn)


def full_top(d, t):
    rig(d, t, 1.0, 4, 4, 1.0)
    table(d, 5)


# ---------------- canh 3: Keo dai + dap an ----------------
def s_ket(img, d, t, sc):
    M = sc["M"]
    full_top(d, t)
    axes(d)
    fit_line(d, ease((t - 0.4) / 0.6), ease((t - 1.1) / (M[1] - 1.3)))
    points(d, 5)
    cut_mark(d, appear(t, M[1] + 0.1, 0.4))
    kb = appear(t, M[1] + 0.5, 0.4)
    if kb > 0:
        s = "ĐÁP ÁN · khoảng −273 °C"; wd = tw(d, s, F(44)) + 52
        card(d, (1022 - wd, 890, 1022, 950), fill=A(GREEN, kb), r=31)
        text(d, (1022 - wd / 2, 920), s, 44, WHITE, alpha=kb)


def graph_done(d):
    axes(d)
    fit_line(d, 1.0, 1.0)
    points(d, 5)
    cut_mark(d, 1.0)


# ---------------- canh 4: Rut ra + chua noi duoc ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    graph_done(d)
    k1 = appear(t, M[0] + 0.2, 0.45)
    if k1 > 0:
        card(d, (50, 262, 1030, 470), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=6)
        text(d, (W / 2, 330), "p = 0 ở ≈ −273 °C", 52, GREEN, alpha=k1)
        text(d, (W / 2, 412), "→ gốc 0 K của thang Kelvin", 46, INK, alpha=appear(t, M[0] + 0.8, 0.45))
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        card(d, (50, 500, 1030, 830), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, 560), "Chưa nói được", 48, NAVY, alpha=k2)
        text(d, (90, 660), "• Khí thật hoá lỏng trước −273 °C", 44, INK, anchor="lm", alpha=appear(t, M[1] + 0.2, 0.4))
        text(d, (90, 760), "• Ở 0 K vật chất ra sao", 44, INK, anchor="lm", alpha=appear(t, M[1] + 0.6, 0.4))


# ---------------- canh 5: Bay (khi khac -> diem cat khac?) ----------------
P0B, P0C = 80.0, 150.0
def t_top(p0, pmax=162.0): return min(100.0, (pmax / p0 - 1) * -TCUT)


def s_bay(img, d, t, sc):
    M = sc["M"]
    ks = clamp((t - (M[0] + 1.6)) / 0.4)            # gach cau sai
    mk = M[0] + 2.0                                  # het gach
    axes(d)
    fit_line(d, 1.0, 1.0)
    points(d, 5)
    text(d, (930, 948), "A", 48, NAVY)
    kl = ease((t - mk - 0.2) / 0.8)                  # duong luong khi B, C chi hien SAU khi gach
    if kl > 0:
        for p0, col, lab, lp in ((P0B, TEAL, "B", (940, 1150)), (P0C, PURPLE, "C", (700, 935))):
            fit_line(d, kl, kl, col=col, p0=p0, t_hi=t_top(p0))
            text(d, lp, lab, 48, col, alpha=appear(t, mk + 0.8, 0.4))
    dot(d, X(TCUT), Y(0), 14, RED, outline=WHITE)
    # the bay co theo so dong da hien
    n_ln = 1 + (1 if t > mk + 0.6 else 0)
    hb = 300 if n_ln == 1 else 440
    card(d, (50, 262, 1030, 262 + hb), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 320, "BẪY", 44, WHITE, RED)
    q = "“Đổi lượng khí, điểm cắt đổi”"
    text(d, (W / 2, 440), q, 46, INK)
    if ks > 0:
        lw = tw(d, q, F(46)); d.line([(W / 2 - lw / 2, 444), (W / 2 - lw / 2 + lw * ks, 444)], fill=RED, width=6)
    if t > mk: text(d, (W / 2 + tw(d, q, F(46)) / 2 + 30, 440), "✗", 52, RED, alpha=appear(t, mk, 0.3))
    ka = appear(t, mk + 0.6, 0.4)
    if ka > 0:
        s = "→ A, B, C: vẫn ≈ −273 °C"
        text(d, (W / 2, 590), s, 46, GREEN, alpha=ka)
        text(d, (W / 2 + tw(d, s, F(46)) / 2 + 34, 590), "✓", 52, GREEN, alpha=appear(t, mk + 2.2, 0.3))
    # chu giai luong khi (p luc 0 °C), mot dong, hien cung duong B, C
    kg = appear(t, mk + 0.8, 0.4)
    if kg > 0:
        segs = (("p ở 0 °C:  ", INK), ("A 100", NAVY), ("  ·  ", MUTED), ("B 80", TEAL), ("  ·  ", MUTED),
                ("C 150", PURPLE), ("  kPa", INK))
        x = W / 2 - sum(tw(d, s_, F(44)) for s_, _ in segs) / 2
        for s_, c_ in segs:
            text(d, (x, 790), s_, 44, c_, anchor="lm", alpha=kg); x += tw(d, s_, F(44))


# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
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


def _end_body(d, t, k):
    """Hinh: binh kin cung luong khi, dun toi 273 °C, ap suat '?' (khong ve them diem/duong tren do thi)."""
    d.ellipse([290, 1050, 430, 1190], fill=A((236, 244, 252), k), outline=A((90, 120, 160), k), width=5)
    d.rectangle([340, 975, 380, 1060], fill=A((236, 244, 252), k), outline=A((90, 120, 160), k), width=5)
    d.rounded_rectangle([330, 958, 390, 982], radius=6, fill=A(NAVY, k))
    d.rounded_rectangle([250, 1200, 470, 1226], radius=8, fill=A(ORANGE, k))
    text(d, (520, 1050), "273 °C", 50, RED, anchor="lm", alpha=k)
    text(d, (520, 1140), "p = ? kPa", 50, ORANGE, anchor="lm", alpha=k)


def s_end(img, d, t, sc):
    end_card(d, t, sc, "Ngoại suy: p = 0 ở ≈ −273 °C",
             "Coi khí lí tưởng, đun bình tới 273 °C, giữ thể tích: áp suất khoảng bao nhiêu?",
             _end_body, "Đọc lại điểm 0 °C", 2.9)          # goi y tre ~2,5 s sau cau hoi (hien o M0 + 0,4)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, r, b, e = sc["hook"], sc["do"], sc["ket"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + 0.6, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + a + 0.5, "tap") for a in lv_times()]
    out += [(k["t0"] + k["M"][1] + 0.5, "ding"), (r["t0"] + r["M"][0] + 0.2, "tap"),
            (b["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out


CLIP = dict(id="tn-l12-thangnhietdo-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thang nhiệt độ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bình khí kín trong nồi nước", draw=s_hook, tail=0.3, caps=[
   ("Thể tích bình giữ không đổi.", 3.0),
   ("Chọn đáp án ở khung câu hỏi.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Mỗi mức chờ số ổn định.", 3.4),
   ("Đun dần tới nước đang sôi.", 4.2)]),
 dict(key="ket", title="Kéo dài đồ thị", draw=s_ket, tail=0.4, caps=[
   ("Kẻ thẳng qua 5 điểm, kéo dài.", 3.4),
   ("Cắt trục nhiệt độ ở đây.", 3.2)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("p không âm, nên có nhiệt độ thấp nhất.", 4.3),
   ("Hai điều chưa nói được.", 4.0)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đổi lượng khí, điểm cắt có đổi?", 3.8),
   ("Chỉ độ dốc thay đổi.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])
