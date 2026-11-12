# Clip: tn-l12-thuchanh-01 - Do nhiet dung rieng cua nuoc, kiem gia thuyet "c phu thuoc m" (de TN THPT 2026 cau II.4)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanh-01.json (so_lieu_mau + ghi_chu, "so lieu minh hoa"):
#   P = 150 W, tau = 300 s, Q = P.tau = 45 000 J, t1 = 28,0 °C, c that = 4 180 J/(kg.K)
#   m = 0,200 kg: t2 = 81,3, dt = 53,3, c = 4 221 | m = 0,300 kg: t2 = 63,7, dt = 35,7, c = 4 202 | m = 0,400 kg: t2 = 54,8, dt = 26,8, c = 4 198
#   c tinh ra la so lam tron -> ghi "≈" tren man.
# Du doan (K10: khong ve nut A-D trong mp4): cung 150 W, 300 s, doi m -> ba gia tri c: A tang theo m; B giam khi m tang;
#   C gan nhu bang nhau (dung, chenh duoi 1%); D khong so sanh duoc vi dt khac nhau.
# Bay: "Coi rang toan bo P.tau lam nong nuoc" -> binh, day, nhiet ke cung nong, nhiet mat ra ngoai -> dt nho di -> c do LON hon 4 180.
# Chot THU NGHI: dau nhiet ke cham dien tro (sai_so_thuong_gap 3) -> so doc cao hon -> dt lon -> c NHO hon that (nguoc chieu bay).
#   Goi y chi cho du kien: dien tro nong hon nuoc.
# Ban 1 (12/11/2026).
from engine import *

NOTE = (70, 75, 95)
WIRE_C = (190, 60, 40)
RUNS = (("0,200", 0.45, "81,3", "53,3", "4 221", 4221), ("0,300", 0.60, "63,7", "35,7", "4 202", 4202),
        ("0,400", 0.75, "54,8", "26,8", "4 198", 4198))

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def rig(d, t, run, reading, p_timer, on, heat, labels=True):
    """run: chi so RUNS; reading: chu tren nhiet ke; p_timer: tien do 300 s (1 = xong); heat: 0..1 mau nuoc nong."""
    m_txt, lvl = RUNS[run][0], RUNS[run][1]
    # --- binh nhiet luong ke vo xop + nap ---
    card(d, (170, 440, 570, 920), fill=(232, 226, 214), outline=(170, 160, 140), r=30, w=4)
    for k in range(9):                                     # van xop
        y = 470 + k * 50; d.line([(182, y), (204, y + 20)], fill=(200, 192, 176), width=3)
        d.line([(536, y), (558, y + 20)], fill=(200, 192, 176), width=3)
    d.rounded_rectangle([210, 470, 530, 890], radius=18, fill=(250, 252, 255), outline=(150, 175, 205), width=4)
    yw = 890 - 400 * lvl
    d.rounded_rectangle([214, yw, 526, 886], radius=14, fill=mix((175, 212, 250), (250, 190, 160), heat))
    d.line([(216, yw), (524, yw)], fill=(110, 160, 220), width=4)
    d.rounded_rectangle([155, 410, 585, 445], radius=10, fill=(120, 126, 140))
    # --- dien tro (zigzag chim trong nuoc) + day noi kin mach toi oat ke ---
    zz = [(280 + 20 * k, 846 + (14 if k % 2 else -14)) for k in range(10)]
    d.line(zz, fill=WIRE_C if on else (120, 90, 80), width=7, joint="curve")
    if on:
        g = 0.35 + 0.25 * math.sin(t * 6)
        d.line(zz, fill=A((255, 140, 60), g), width=15, joint="curve")
    d.line([(280, 846), (280, 320), (650, 320)], fill=NAVY, width=5, joint="curve")
    d.line([(460, 846), (460, 365), (650, 365)], fill=NAVY, width=5, joint="curve")
    dot(d, 650, 320, 9, RED); dot(d, 650, 365, 9, NAVY)
    # --- que khuay ---
    d.line([(240, 395), (240, 860)], fill=(150, 110, 70), width=10)
    dot(d, 240, 392, 12, (150, 110, 70))
    # --- dau do nhiet ke + day toi dong ho ---
    d.line([(500, 820), (500, 392)], fill=(90, 96, 110), width=10)
    dot(d, 500, 822, 10, NAVY)
    d.line([(500, 392), (610, 392), (610, 660), (650, 660)], fill=(90, 96, 110), width=5, joint="curve")
    # --- oat ke ---
    card(d, (650, 270, 1030, 530), fill=WHITE, outline=NAVY, w=5, r=24)
    if labels: text(d, (840, 302), "oát kế", 40, INK)
    card(d, (675, 335, 1005, 515), fill=(24, 30, 40), r=14)
    text(d, (840, 385), "150 W", 48, (134, 239, 172))
    if p_timer >= 1: text(d, (840, 465), "300 s", 46, (134, 239, 172))
    else:
        d.rounded_rectangle([705, 455, 975, 475], radius=10, fill=(60, 66, 80))
        if p_timer > 0: d.rounded_rectangle([705, 455, 705 + 270 * p_timer, 475], radius=10, fill=(134, 239, 172))
    # --- nhiet ke ---
    card(d, (650, 590, 1030, 770), fill=WHITE, outline=NAVY, w=5, r=24)
    if labels: text(d, (840, 622), "nhiệt kế", 40, INK)
    card(d, (675, 652, 1005, 752), fill=(24, 30, 40), r=14)
    rising = reading is None
    text(d, (840, 702), "đang tăng ↑" if rising else reading, 44 if rising else 48, ORANGE if rising else (134, 239, 172))
    pill(d, 840, 860, f"m = {m_txt} kg", 44, WHITE, NAVY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut A-D) ----------------
def s_hook(img, d, t, sc):
    rig(d, t, 0, "28,0 °C", 0.0, False, 0.0)
    a = appear(t, 0.8, 0.5)
    if a <= 0: return
    y0 = 990 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 56, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 160), "Nhóm bạn cho rằng: c phụ thuộc m.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "m = 0,200; 0,300; 0,400 kg", 44, INK, alpha=appear(t, 1.3, 0.5))
    text(d, (W / 2, y0 + 345), "Ba giá trị c sẽ ra sao?", 48, PURPLE, alpha=appear(t, 1.8, 0.5))
    tc, tend = sc["M"][1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 456, 940, y0 + 468], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 456, 140 + 800 * (1 - p), y0 + 468], radius=6, fill=A(PURPLE, a))

# ---------------- bang so lieu (dung chung) ----------------
COLX = ((170, "m (kg)"), (410, "t₂ (°C)"), (640, "Δt (°C)"), (880, "c (J/(kg·K))"))
def table(d, y0, ks, kc, hl=0.0, rh=78):
    if hl > 0:
        d.rounded_rectangle([775, y0 - 34, 985, y0 + 40 + rh * 3], radius=18, fill=A((255, 237, 213), hl), outline=A(ORANGE, hl), width=4)
    for x, s in COLX: text(d, (x, y0), s, 40, NOTE, bold=False)
    d.line([(70, y0 + 36), (1010, y0 + 36)], fill=LIGHT, width=3)
    for j, r in enumerate(RUNS):
        yy = y0 + 36 + rh * (j + 0.6)
        if ks[j] > 0:
            for x, s in zip((170, 410, 640), r[:1] + r[2:4]): text(d, (x, yy), s, 42, INK, alpha=ks[j])
        if kc[j] > 0: text(d, (880, yy), "≈ " + r[4], 42, ORANGE, alpha=kc[j])

# ---------------- canh 2: Tien hanh (ba lan dun, tua nhanh) ----------------
def runs_at(sc):
    M = sc["M"]
    return ((0.8, M[1] - 0.5), (M[1] + 0.3, M[1] + 1.8), (M[1] + 2.2, M[1] + 3.7))

def s_do(img, d, t, sc):
    R = runs_at(sc)
    j = 0 if t < R[1][0] - 0.25 else (1 if t < R[2][0] - 0.25 else 2)
    a, b = R[j]; p = clamp((t - a) / (b - a))
    reading = "28,0 °C" if p <= 0 else (RUNS[j][2] + " °C" if p >= 1 else None)
    rig(d, t, j, reading, p, 0 < p < 1, p)
    if a < t < b:
        wdt = tw(d, "TUA NHANH", F(40)) + 90
        card(d, (60, 236, 60 + wdt, 296), fill=ORANGE, r=30)
        text(d, (60 + wdt / 2 + 18, 266), "TUA NHANH", 40, WHITE)
        for k in range(2):
            tx = 82 + k * 16; d.polygon([(tx, 252), (tx, 280), (tx + 16, 266)], fill=WHITE)
    text(d, (W / 2, 940), "Nhiệt kế: nhiệt độ chỗ đầu đo", 40, NOTE, alpha=appear(t, 0.2, 0.4))
    card(d, (40, 990, 1040, 1470), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 1045), "t₁ = 28,0 °C", 44, NOTE, anchor="lm")
    text(d, (1000, 1045), "Minh hoạ", 40, PURPLE, bold=False, anchor="rm")
    table(d, 1140, [appear(t, R[k][1], 0.35) for k in range(3)], [0, 0, 0])

# ---------------- canh 3: Ket qua ----------------
def s_ket(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 700), fill=WHITE, outline=LIGHT, w=3)
    hl = appear(t, M[0] + 0.1, 0.4)
    table(d, 310, [1, 1, 1], [appear(t, M[0] + 0.4 + 0.5 * k, 0.35) for k in range(3)], hl=hl)
    text(d, (W / 2, 640), "Q = P·τ = 45 000 J", 42, NOTE)
    text(d, (W / 2, 770), "c = Q / (m·Δt)", 56, INK, alpha=appear(t, 0.2, 0.4))
    pill(d, W / 2, 890, "Chênh nhau dưới 1%", 46, WHITE, NAVY, appear(t, M[0] + 2.2, 0.4))
    k = appear(t, M[1] + 0.3, 0.45)
    if k > 0:
        y = 1000 + (1 - back((t - M[1] - 0.3) / 0.45)) * 30
        card(d, (60, y, 1020, y + 300), fill=WHITE, outline=GREEN, w=6)
        text(d, (W / 2, y + 95), "Giả thuyết “c phụ thuộc m”", 46, INK)
        text(d, (W / 2, y + 205), "bị bác bỏ", 60, GREEN)

# ---------------- canh 4: Chua noi duoc gi ----------------
def s_chua(img, d, t, sc):
    rig(d, t, 2, "54,8 °C", 1.0, False, 1.0, labels=False)
    k = appear(t, 0.3, 0.45)
    card(d, (40, 1000, 1040, 1490), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 1070), "Chưa nói được", 48, NAVY, alpha=k)
    for j, s in enumerate(("• Nhiệt mất ra ngoài: bao nhiêu?", "• c có đổi theo nhiệt độ?")):
        text(d, (90, 1210 + 150 * j), s, 44, INK, anchor="lm", alpha=appear(t, 0.6 + 0.4 * j, 0.4))

# ---------------- canh 5: Bay ----------------
X0B = 360
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 600), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 306, "BẪY", 40, WHITE, RED)
    q = "“Coi rằng: toàn bộ P·τ làm nóng nước”"
    text(d, (W / 2, 410), q, 44, INK)
    ks = clamp((t - (M[0] + 1.6)) / 0.4)
    if ks > 0:
        lw = tw(d, q, F(44)); d.line([(W / 2 - lw / 2, 412), (W / 2 - lw / 2 + lw * ks, 412)], fill=RED, width=5)
    text(d, (W / 2, 520), "→ Δt đo được nhỏ đi", 46, ORANGE, alpha=appear(t, M[0] + 2.2, 0.4))
    # so voi c that (hinh co ngay tu dau canh)
    card(d, (40, 640, 1040, 1460), fill=WHITE, outline=LIGHT, w=3)
    d.line([(X0B, 790), (X0B, 1230)], fill=GREEN, width=6)
    text(d, (X0B, 710), "c thật = 4 180", 44, GREEN)
    for j, r in enumerate(RUNS):
        y = 860 + 130 * j; k = appear(t, 0.2 + 0.25 * j, 0.4)
        text(d, (80, y), r[0] + " kg", 42, INK, anchor="lm", alpha=k)
        L = 11 * (r[5] - 4180) * ease((t - 0.2 - 0.25 * j) / 0.6)
        if L > 4: d.rounded_rectangle([X0B, y - 24, X0B + L, y + 24], radius=12, fill=A(ORANGE, k))
        if j == 0: text(d, (X0B + 11 * (r[5] - 4180) + 20, y), "≈ " + r[4], 40, ORANGE, anchor="lm", alpha=appear(t, 0.9, 0.4))
    text(d, (W / 2, 1330), "c đo lớn hơn thật", 52, RED, alpha=appear(t, M[1] + 0.1, 0.4))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    """Hinh: dau nhiet ke cham vao dien tro dang nong (khong chu)."""
    zz = [(400 + 24 * j, 1180 + (16 if j % 2 else -16)) for j in range(12)]
    d.line(zz, fill=A(WIRE_C, k), width=8, joint="curve")
    d.line(zz, fill=A((255, 140, 60), 0.4 * k), width=18, joint="curve")
    d.line([(560, 1000), (560, 1158)], fill=A((90, 96, 110), k), width=12)
    dot(d, 560, 1162, 11, A(NAVY, k))

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "c không phụ thuộc m",
             "Riêng lỗi này (đầu nhiệt kế chạm điện trở), c tính ra lớn hay nhỏ hơn thật?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)                 # goi y hien tre, chi la du kien
    if kh > 0:
        card(d, (110, 1300, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1355), "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1455), "Điện trở nóng hơn nước", 46, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, ch, b, e = sc["hook"], sc["do"], sc["ket"], sc["chua"], sc["bay"], sc["end"]
    out = [(h["t0"] + 0.8, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for a, z in runs_at(do):
        out.append((do["t0"] + a, "tap")); tt = a + 0.5
        while tt < z: out.append((do["t0"] + tt, "tick")); tt += 0.5
    out += [(k["t0"] + k["M"][0] + 2.2, "ding"), (ch["t0"] + 0.3, "tap"),
            (b["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-thuchanh-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thực hành đo nhiệt dung riêng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nhiệt dung riêng của nước", draw=s_hook, tail=0.3, caps=[
   ("Đo c của nước.", 3.4),
   ("Dừng video, chọn đáp án.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đun 300 s với 0,200 kg nước.", 3.4),
   ("Lặp lại: 0,300 kg, 0,400 kg.", 4.2)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.5, caps=[
   ("Tính c cho từng lần đo.", 3.4),
   ("Đáp án C: Δt giảm, c thì không.", 3.8)]),
 dict(key="chua", title="Giới hạn của thí nghiệm", draw=s_chua, tail=0.4, caps=[
   ("Hai điều chưa đo được.", 5.0)]),
 dict(key="bay", title="Cái bẫy “coi rằng”", draw=s_bay, tail=0.5, caps=[
   ("Bình, dây cũng nóng lên.", 4.2),
   ("Cả ba đều lệch lên.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 8.2)]),
])
