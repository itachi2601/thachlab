# Clip: tn-l12-thuchanh-01 - Do nhiet dung rieng cua nuoc (Bai 4 thuc hanh, de TN THPT 2026 cau II.4)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanh-01.json (so_lieu_mau + ghi_chu, "so lieu minh hoa"):
#   P = 150 W, tau = 300 s, t1 = 28,0 °C, c that = 4 180 J/(kg.K)
#   m = 0,200 kg: 45,8 / 63,5 / 81,3 °C luc 100/200/300 s, dt = 53,3, c = 4 221 | m = 0,300 kg: t2 = 63,7, dt = 35,7, c = 4 202
#   m = 0,400 kg: t2 = 54,8, dt = 26,8, c = 4 198.  c tinh ra la so lam tron -> ghi "≈" tren man.
# Quan niem sai can danh (hien_tuong_hay_sai 1): "phai dun nuoc toi 100 °C moi tinh duoc c".
# Du doan (K10: khong ve nut A-D trong mp4; khung web hoi A-D): ba lan dun 300 s, 0,200/0,300/0,400 kg, nuoc chua soi
#   -> ba gia tri c: A chua soi nen chua tinh duoc; B chi lan nong nhat gan dung; C gan nhu bang nhau (DUNG); D tang dan khi m tang.
#   Khong trung quiz mo bai (da tan) va Cau 1-5 Tu kiem tra (Cau 3 hoi phat bieu SAI ve mat nhiet, dap an D).
# Bay (rut_ra 3 + sai_so 1): "dun gan soi cho chac?" -> nuoc cang nong hon phong cang mat nhiet nhanh -> nuoc nhan it hon P.tau
#   -> dt nho -> c do lon hon that (4 221 > 4 180). Khong noi lan 0,200 kg lech nhieu VI nong (mo hinh kho: lech do C_b/m).
# Chot THU NGHI (sai_so 3): dau do nhiet ke cham dien tro luc dun, P, tau, m dung -> so doc cao hon nuoc -> dt lon -> c NHO hon that.
#   Hinh goi y chi ve dau do cham dien tro, khong ve mui ten/so nao gan dap so.
# Ban 3c (21/11, cong B v2): the Du doan them dong 'Ban noi: phai dun toi 100 °C' (phu de hook doi de khong lap).
# Ban 3b (21/11, cong B v1): the Du doan bo chu 'Chua soi' (C de qua); gioi han them '(chi thu 28-81 °C)'.
# Ban 3 (21/11/2026, viec 4 lo 20): cong --do-chu moi (chu >= 56, moc khoi chu cach >= 2,4 s, dem nguoc 5 cham), Du doan
#   doi sang quan niem "phai dun toi 100 °C", bo dong "Chon dap an...", Bay hinh hai binh tu giai thich 3 nhip >= 3 s.
# Ban 1 (12/11), ban 2 (13/11/2026): Du doan "c phu thuoc m", chot dau nhiet ke cham dien tro.
from engine import *

WIRE_C = (190, 60, 40)
DARK_OR = (181, 71, 8)                         # #B54708: chu cam tren nen sang >= 4,5:1
DARK_GR = (21, 128, 61)
RUNS = (("0,200", 0.45, "81,3", "53,3", "4 221"), ("0,300", 0.60, "63,7", "35,7", "4 202"),
        ("0,400", 0.75, "54,8", "26,8", "4 198"))

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=30):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.75, cx + wdt / 2, cy + size * 0.75), fill=A(bg, alpha), r=int(size * 0.75))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def reading_at(run, p):
    """So doc nhiet ke (chi so co trong kho). Lan 0,200 kg: moi 100 s (so_lieu_mau); lan khac chi t1 va t2."""
    if run == 0:
        return ("28,0", "45,8", "63,5", "81,3")[min(3, int(p * 3 + 1e-6))]
    return RUNS[run][2] if p >= 1 else "28,0"

def rig(d, t, run, reading, p_timer, on, heat, labels=True, mpill=True):
    """run: chi so RUNS; reading: so doc nhiet ke; p_timer: tien do 300 s; heat: 0..1 mau nuoc nong."""
    m_txt, lvl = RUNS[run][0], RUNS[run][1]
    # --- binh nhiet luong ke vo xop + nap ---
    card(d, (110, 400, 510, 880), fill=(232, 226, 214), outline=(170, 160, 140), r=30, w=4)
    for k in range(8):                                     # van xop
        y = 440 + k * 52; d.line([(122, y), (140, y + 20)], fill=(200, 192, 176), width=3)
        d.line([(480, y), (498, y + 20)], fill=(200, 192, 176), width=3)
    d.rounded_rectangle([150, 430, 470, 850], radius=18, fill=(250, 252, 255), outline=(150, 175, 205), width=4)
    yw = 850 - 400 * lvl
    d.rounded_rectangle([154, yw, 466, 846], radius=14, fill=mix((175, 212, 250), (250, 190, 160), heat))
    d.line([(156, yw), (464, yw)], fill=(110, 160, 220), width=4)
    d.rounded_rectangle([95, 370, 525, 405], radius=10, fill=(120, 126, 140))
    # --- dien tro (zigzag chim trong nuoc) + day noi toi oat ke ---
    zz = [(220 + 20 * k, 806 + (14 if k % 2 else -14)) for k in range(10)]
    d.line(zz, fill=WIRE_C if on else (120, 90, 80), width=7, joint="curve")
    if on:
        d.line(zz, fill=A((255, 140, 60), 0.35 + 0.25 * math.sin(t * 6)), width=15, joint="curve")
    d.line([(220, 806), (220, 330), (600, 330)], fill=NAVY, width=5, joint="curve")
    d.line([(400, 806), (400, 380), (600, 380)], fill=NAVY, width=5, joint="curve")
    dot(d, 600, 330, 9, RED); dot(d, 600, 380, 9, NAVY)
    # --- que khuay ---
    d.line([(180, 345), (180, 820)], fill=(150, 110, 70), width=10)
    dot(d, 180, 342, 12, (150, 110, 70))
    # --- dau do nhiet ke + day toi dong ho ---
    d.line([(440, 420), (440, 780)], fill=(90, 96, 110), width=10)
    dot(d, 440, 782, 10, NAVY)
    d.line([(440, 420), (560, 420), (560, 770), (600, 770)], fill=(90, 96, 110), width=5, joint="curve")
    # --- oat ke ---
    card(d, (600, 290, 1040, 610), fill=WHITE, outline=NAVY, w=5, r=24)
    if labels: text(d, (820, 336), "oát kế", 56, INK)
    card(d, (625, 380, 1015, 590), fill=(24, 30, 40), r=14)
    text(d, (820, 432), "150 W", 60, (134, 239, 172))
    text(d, (820, 532), f"{int(round(300 * clamp(p_timer)))} s", 60, (134, 239, 172))
    # --- nhiet ke ---
    card(d, (600, 650, 1040, 900), fill=WHITE, outline=NAVY, w=5, r=24)
    if labels: text(d, (820, 696), "nhiệt kế", 56, INK)
    card(d, (625, 740, 1015, 880), fill=(24, 30, 40), r=14)
    text(d, (820, 810), reading + " °C", 64, (134, 239, 172))
    if mpill: pill(d, 310, 945, f"m = {m_txt} kg", 56, WHITE, NAVY)

def dots5(d, t, t0, t1, y, color, a=1.0):
    """Dem nguoc 5 cham to (r 36), moi cham tat sau (t1-t0)/5 s: giu hinh khong dung yen."""
    n_off = 0 if t < t0 else min(5, int((t - t0) / ((t1 - t0) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 130, y, 36, A(LIGHT, a) if j >= 5 - n_off else A(color, a))

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut A-D) ----------------
HOOK_CARD = 2.4
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 0, "28,0", 0.0, False, 0.0, labels=False, mpill=False)
    a = appear(t, HOOK_CARD, 0.45)
    if a <= 0: return
    y0 = 955 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 525), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 155), "Bạn nói: phải đun tới 100 °C", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "Đun 300 s, cùng 150 W", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 315), "m = 0,200 · 0,300 · 0,400 kg", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 395), "Ba giá trị c ra sao?", 58, INK, alpha=a)
    dots5(d, t, M[1] + 0.3, sc["T"] - 0.1, y0 + 470, PURPLE, a)

# ---------------- canh 2: Tien hanh (ba lan dun, tua nhanh) ----------------
RUN_AT = ((0.6, 2.6), (3.1, 5.1), (5.6, 7.6))
def s_do(img, d, t, sc):
    j = 0 if t < RUN_AT[1][0] - 0.25 else (1 if t < RUN_AT[2][0] - 0.25 else 2)
    a, b = RUN_AT[j]; p = clamp((t - a) / (b - a))
    pt = min(3, int(p * 3 + 1e-6)) / 3 if j == 0 else p      # lan 0,200 kg: oat ke nhay cung moc doc nhiet ke
    rig(d, t, j, reading_at(j, p), pt, 0 < p < 1, p)
    pill(d, 835, 945, "TUA NHANH", 56, WHITE, ORANGE)
    card(d, (40, 1000, 1040, 1465), fill=WHITE, outline=LIGHT, w=3)
    text(d, (300, 1058), "m (kg)", 56, INK)
    text(d, (760, 1058), "t₂ (°C)", 56, INK)
    d.line([(80, 1100), (1000, 1100)], fill=LIGHT, width=3)
    for k, r in enumerate(RUNS):
        ka = appear(t, RUN_AT[k][1], 0.35)
        if ka > 0:
            yy = 1150 + 85 * k
            text(d, (300, yy), r[0], 60, INK, alpha=ka)
            text(d, (760, yy), r[2], 60, INK, alpha=ka)
    text(d, (W / 2, 1410), "t₁ = 28,0 °C lúc đầu", 56, INK)

# ---------------- canh 3: Ket qua ----------------
KET_C, KET_KEY = 2.4, 5.2
def s_ket(img, d, t, sc):
    card(d, (40, 250, 1040, 790), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 322), "c = P·τ / (m·Δt)", 64, INK)
    hl = appear(t, KET_C, 0.4)
    if hl > 0:
        d.rounded_rectangle([660, 385, 1025, 760], radius=18, fill=A((255, 237, 213), hl), outline=A(ORANGE, hl), width=4)
    for x, s in ((190, "m (kg)"), (470, "Δt (°C)"), (842, "c (J/(kg·K))")): text(d, (x, 425), s, 56, INK)
    d.line([(70, 465), (1010, 465)], fill=LIGHT, width=3)
    for j, r in enumerate(RUNS):
        yy = 520 + 92 * j
        text(d, (190, yy), r[0], 60, INK); text(d, (470, yy), r[3], 60, INK)
        if hl > 0: text(d, (842, yy), "≈ " + r[4], 60, DARK_OR, alpha=hl)
    k = appear(t, KET_KEY, 0.45)
    if k > 0:
        y = 850 + (1 - back((t - KET_KEY) / 0.45)) * 30
        card(d, (60, y, 1020, y + 300), fill=A((236, 253, 243), k), outline=A(GREEN, k), w=6)
        text(d, (W / 2, y + 100), "Chưa sôi vẫn tính được c", 62, DARK_GR, alpha=k)
        text(d, (W / 2, y + 205), "chỉ cần đo được Δt", 58, INK, alpha=k)

# ---------------- canh 4: Bay (3 nhip >= 3 s, moi nhip mot phu de) ----------------
def beaker(d, cx, heat, k):
    d.rounded_rectangle([cx - 130, 480, cx + 130, 790], radius=20, fill=A((250, 252, 255), k), outline=A((150, 175, 205), k), width=5)
    d.rounded_rectangle([cx - 124, 570, cx + 124, 784], radius=16, fill=A(mix((175, 212, 250), (250, 150, 110), heat), k))

def wavy(d, x0, y, dirx, t, k, L=105):
    """Mui ten luon song nam ngang (nhiet mat ra ngoai), pha chay theo t."""
    pts = [(x0 + dirx * s, y + 10 * math.sin(s / 14 - t * 7)) for s in range(0, L, 5)]
    d.line(pts, fill=A(RED, k), width=7, joint="curve")
    xe, ye = pts[-1]; h = 20
    d.polygon([(xe + dirx * h, ye), (xe - dirx * 4, ye - h * 0.7), (xe - dirx * 4, ye + h * 0.7)], fill=A(RED, k))

def s_bay(img, d, t, sc):
    M = sc["M"]; b1, b2, b3 = (m - 0.1 for m in M)
    k1 = appear(t, b1, 0.4); k2 = appear(t, b2, 0.4); k3 = appear(t, b3, 0.4)
    if k1 <= 0: return
    pill(d, W / 2, 292, "BẪY", 56, WHITE, RED, k1)
    text(d, (W / 2, 395), "Đun gần sôi cho chắc?", 62, INK, alpha=k1)
    beaker(d, 290, 0.25, k1); beaker(d, 790, 1.0, k1)
    text(d, (290, 850), "ấm", 60, INK, alpha=k1); text(d, (790, 850), "nóng", 60, RED, alpha=k1)
    if k2 > 0:                                            # mat nhiet: binh am 1 mui ten, binh nong 3 mui ten
        wavy(d, 150, 680, -1, t, k2, L=95)
        for y in (600, 680, 760): wavy(d, 930, y, 1, t, k2, L=95)
    if k3 > 0:
        card(d, (40, 915, 1040, 1300), fill=A(WHITE, k3), outline=A(RED, k3), w=5)
        text(d, (W / 2, 985), "Nước nhận ít hơn P·τ", 60, INK, alpha=k3)
        text(d, (W / 2, 1085), "→ Δt nhỏ → c đo lớn hơn", 60, INK, alpha=k3)
        text(d, (W / 2, 1200), "4 221 > 4 180 thật", 64, RED, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
CHUA_B = 2.4
def s_chua(img, d, t, sc):
    k = appear(t, 0.2, 0.4); kb = appear(t, CHUA_B, 0.4)
    card(d, (40, 300, 1040, 1100), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Mất bao nhiêu nhiệt?", "• c có đổi theo nhiệt độ?")):
        text(d, (100, 540 + j * 240), s, 62, INK, anchor="lm", alpha=kb)
    text(d, (150, 880), "(chỉ thử 28–81 °C)", 58, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 700), "?", 260, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau chot cua khung) ----------------
END_CARD = 1.6
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, END_CARD, 0.5)
    if k <= 0: return
    card(d, (40, 290, 1040, 1300), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 360, "THỬ NGHĨ", 56, WHITE, DARK_OR, k)
    # hinh: nuoc, dien tro dang nong, dau do nhiet ke cham vao (khong chu, khong mui ten)
    d.rounded_rectangle([290, 450, 790, 700], radius=20, fill=A((214, 232, 252), k))
    zz = [(330 + 30 * j, 630 + (18 if j % 2 else -18)) for j in range(15)]
    d.line(zz, fill=A(WIRE_C, k), width=9, joint="curve")
    d.line(zz, fill=A((255, 140, 60), (0.35 + 0.2 * math.sin(t * 6)) * k), width=20, joint="curve")
    d.line([(510, 430), (510, 598)], fill=A((90, 96, 110), k), width=14)
    dot(d, 510, 604, 13, A(NAVY, k))
    d.ellipse([478, 572, 542, 636], outline=A(RED, k), width=6)
    text(d, (W / 2, 790), "Lúc đun, đầu đo chạm điện trở.", 58, INK, alpha=k)
    text(d, (W / 2, 885), "P, τ, m vẫn đúng.", 58, INK, alpha=k)
    text(d, (W / 2, 990), "c lớn hay nhỏ hơn thật?", 62, DARK_OR, alpha=k)
    dots5(d, t, M[1] + 0.3, sc["T"] - 0.1, 1150, DARK_OR, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, b, ch, e = (sc[x] for x in ("hook", "do", "ket", "bay", "chua", "end"))
    out = [(h["t0"] + HOOK_CARD, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for a, z in RUN_AT:
        out.append((do["t0"] + a, "tap")); tt = a + 0.5
        while tt < z: out.append((do["t0"] + tt, "tick")); tt += 0.5
    out += [(k["t0"] + KET_KEY, "ding"), (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (ch["t0"] + CHUA_B, "tap"), (e["t0"] + END_CARD, "open")]
    return out

CLIP = dict(id="tn-l12-thuchanh-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thực hành đo nhiệt dung riêng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nhiệt dung riêng của nước", draw=s_hook, tail=0.3, caps=[
   ("Đo nhiệt dung riêng c của nước.", 3.4),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cùng 150 W, đun 300 s mỗi lần.", 3.7),
   ("Cả ba lần đều dưới 100 °C.", 3.6)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.3, caps=[
   ("Tính c cho từng lần.", 2.5),
   ("Đáp án: ba giá trị gần bằng nhau.", 4.2)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("So hai bình nước.", 3.2),
   ("Nóng xa phòng, mất nhiệt nhanh.", 3.2),
   ("Nên c đo lệch lên.", 3.2)]),
 dict(key="chua", title="Giới hạn của phép đo", draw=s_chua, tail=0.2, caps=[
   ("Còn chưa biết gì?", 5.4)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.3, caps=[
   ("Chưa sôi vẫn đo được c.", 3.0),
   ("Dừng lại, tự trả lời.", 5.0)]),
])
