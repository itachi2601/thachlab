# Clip: tn-l12-thuchanh-03 - Phieu nuoc da + day dien tro, hai giai doan (doi chung moi truong) - de TN THPT 2025 cau II.1
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanh-03.json (so_lieu_mau, tham_so, ghi_chu "so lieu minh hoa"):
#   U = 12 V, I = 3,0 A, tau = 300 s moi giai doan; m1 = 5,0 g (chua cap dien), m2 = 36,4 g (cap dien); can +-0,1 g.
#   UI.tau = 10 800 J; m2 - m1 = 31,4 g; lambda = UI.tau/(m2 - m1) ~ 3,44.10^5 J/kg (lon hon that 3%: chi 97% nhiet day vao da);
#   chia cho m2: ~ 2,97.10^5 J/kg (nho hon that 11%); lambda that 3,34.10^5 J/kg. Tren man dung dau phay thap phan.
# Du doan (K10: khong ve nut A-D trong mp4, lua chon nam o khung): giai doan 1 chua cap dien, 300 s, so voi khi cap dien
#   coc hung duoc: A bang 0 (hien_tuong_hay_sai: "khong co gi xay ra"); B it hon nhieu nhung khac 0 (dung, 5,0 g);
#   C gan bang; D nhieu hon.
# Bay: quen tru m1 (chia m2 -> lambda nho hon that 11%) + nhiet day lam am pheu (lambda do lon hon that 3%).
# Chot THU NGHI: phong am dan khi do giai doan 2 -> moi truong lam tan nhieu hon m1 -> m2 - m1 lon hon phan do day ->
#   lambda tinh ra NHO hon (sai_so_thuong_gap 4, khong_chung_minh 2). Goi y chi la cong thuc goc lambda = UItau/(m2 - m1), hien tre.
# Ban 1 (12/11/2026).
from engine import *

NOTE = (70, 75, 95)
ICEC, ICEO = (246, 251, 255), (120, 165, 215)
ENV, WIRE_C = (59, 130, 246), (190, 60, 40)
CUBES = [(258, 378), (322, 378), (386, 378), (450, 378), (296, 440), (356, 440), (414, 440), (352, 500)]
CS = 56
LV1, LV2 = 0.85 * 5.0 / 36.4, 0.85        # muc nuoc trong coc: 5,0 g va 36,4 g (cung mot thang)

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def stopwatch(d, cx, cy, r, p, done_txt=None):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVY, width=6)
    d.rectangle([cx - 14, cy - r - 26, cx + 14, cy - r], fill=NAVY)
    if p > 0:
        d.pieslice([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], -90, -90 + 360 * clamp(p), fill=(255, 220, 190))
        a = math.radians(-90 + 360 * clamp(p))
        d.line([(cx, cy), (cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a))], fill=ORANGE, width=6)
    dot(d, cx, cy, 8, NAVY)
    if done_txt: pill(d, cx, cy + r + 50, done_txt, 40, WHITE, NAVY)

def rig(d, t, on, lvl, scale_txt, p_watch, flow, watch_txt=None, labels=True):
    """on: day dien tro co dien; lvl: muc nuoc trong coc (0..1); flow: 0 khong chay, 1 nho giot cham, 2 chay nhanh."""
    # --- nguon (doc U, I) ---
    card(d, (650, 290, 1030, 520), fill=WHITE, outline=NAVY, w=5, r=24)
    text(d, (840, 326), "Nguồn", 40, INK)
    card(d, (680, 362, 1000, 500), fill=(24, 30, 40), r=14)
    if on:
        text(d, (840, 400), "U = 12 V", 42, (134, 239, 172))
        text(d, (840, 462), "I = 3,0 A", 42, (134, 239, 172))
    else:
        text(d, (840, 431), "TẮT", 46, GRAY)
    # --- pheu + da ---
    pts = [(200, 370), (560, 370), (398, 600), (398, 650), (362, 650), (362, 600)]
    d.polygon(pts, fill=(236, 244, 252)); d.line(pts + [pts[0]], fill=(130, 160, 200), width=5)
    for x, y in CUBES:
        d.rounded_rectangle([x, y, x + CS, y + CS], radius=10, fill=ICEC, outline=ICEO, width=4)
    # --- day dien tro (zigzag vui trong da) + day noi kin mach ---
    col = WIRE_C if on else (120, 90, 80)
    zz = [(300 + 20 * k, 476 + (14 if k % 2 else -14)) for k in range(9)]
    d.line(zz, fill=col, width=7, joint="curve")
    if on:
        for k in range(3):
            g = 0.35 + 0.25 * math.sin(t * 6 + k)
            d.line(zz, fill=A((255, 140, 60), g * 0.5), width=15, joint="curve")
    d.line([(300, 476), (300, 320), (610, 320), (610, 400), (650, 400)], fill=NAVY, width=5, joint="curve")
    d.line([(460, 476), (460, 348), (580, 348), (580, 458), (650, 458)], fill=NAVY, width=5, joint="curve")
    dot(d, 650, 400, 9, RED); dot(d, 650, 458, 9, NAVY)
    # --- nhan ---
    if labels:
        text(d, (850, 572), "dây điện trở", 40, WIRE_C)
        d.line([(728, 580), (472, 492)], fill=NOTE, width=3); dot(d, 470, 491, 6, NOTE)
    # --- giot nuoc ---
    if flow == 1:
        u = (t * 0.9) % 1; dot(d, 380, 660 + u * 70, 8, ENV)
    elif flow == 2:
        for k in range(4):
            u = (t * 2.6 + k / 4) % 1; dot(d, 380, 658 + u * 72, 8, ENV)
    # --- coc ---
    cup = [(300, 735), (460, 735), (446, 852), (314, 852)]
    if lvl > 0.002:
        yw = 852 - 112 * lvl
        xl = 314 - 14 * (852 - yw) / 117; xr = 446 + 14 * (852 - yw) / 117
        d.polygon([(xl, yw), (xr, yw), (446, 852), (314, 852)], fill=(165, 205, 248))
    d.line(cup, fill=(130, 160, 200), width=5)
    text(d, (488, 790), "cốc", 40, INK, anchor="lm")
    # --- can ---
    d.rounded_rectangle([250, 852, 510, 868], radius=6, fill=(150, 155, 170))
    card(d, (230, 868, 530, 962), fill=NAVY, r=18)
    card(d, (272, 884, 488, 946), fill=(20, 60, 40), r=10)
    text(d, (380, 915), scale_txt, 42, (134, 239, 172))
    text(d, (550, 915), "cân", 40, INK, anchor="lm")
    stopwatch(d, 850, 760, 92, p_watch, watch_txt)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut A-D) ----------------
def mini_cup(d, cx, y, lab, col, a):
    cup = [(cx - 70, y), (cx + 70, y), (cx + 58, y + 110), (cx - 58, y + 110)]
    d.line(cup, fill=A(col, a), width=5)
    text(d, (cx, y + 58), "? g", 46, col, alpha=a)
    text(d, (cx, y + 160), lab, 40, col, alpha=a)
    text(d, (cx + 150, y + 58), "300 s", 40, NOTE, bold=False, anchor="lm", alpha=a)

def s_hook(img, d, t, sc):
    rig(d, t, False, 0.0, "? g", 0.0, 0)
    a = appear(t, 0.8, 0.5)
    if a <= 0: return
    y0 = 990 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 630), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 56, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 160), "Chưa cấp điện, sau 300 s,", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 240), "cốc có bao nhiêu nước?", 48, PURPLE, alpha=a)
    k = appear(t, 1.4, 0.5)
    mini_cup(d, 220, y0 + 300, "chưa cấp điện", NAVY, k)
    mini_cup(d, 700, y0 + 300, "cấp điện", NAVY, k)
    text(d, (W / 2, y0 + 540), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=appear(t, sc["M"][1], 0.4))
    tc, tend = sc["M"][1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 596, 940, y0 + 608], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 596, 140 + 800 * (1 - p), y0 + 608], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (hai giai doan, cung 300 s) ----------------
def phases(sc):
    M = sc["M"]
    return (0.9, M[1] - 0.6), (M[1] + 0.5, M[1] + 3.3)      # (bat dau, ket thuc) giai doan 1, 2

def state(t, sc):
    (a1, b1), (a2, b2) = phases(sc); M = sc["M"]
    if t < M[1] - 0.2:
        p = clamp((t - a1) / (b1 - a1))
        return dict(stg=1, on=False, lvl=LV1 * p, p=p, flow=1 if 0 < p < 1 else 0,
                    txt="5,0 g" if p >= 1 else "· · ·", done=p >= 1)
    p = clamp((t - a2) / (b2 - a2))
    return dict(stg=2, on=t >= M[1] + 0.1, lvl=LV2 * p, p=p, flow=2 if 0 < p < 1 else 0,
                txt="36,4 g" if p >= 1 else "· · ·", done=p >= 1)

COLX = ((160, "Giai đoạn"), (400, "Cấp điện"), (650, "Thời gian τ (s)"), (910, "m (g)"))
ROWS = (("1", "không", "300", "5,0"), ("2", "có", "300", "36,4"))

def table(d, y0, ks):
    for x, s in COLX: text(d, (x, y0), s, 44, NOTE, bold=False)
    d.line([(70, y0 + 38), (1010, y0 + 38)], fill=LIGHT, width=3)
    for j, (r, k) in enumerate(zip(ROWS, ks)):
        if k <= 0: continue
        yy = y0 + 86 + 72 * j
        for (x, _), s in zip(COLX, r): text(d, (x, yy), s, 44, BLUE if j == 0 else ORANGE, alpha=k)

def s_do(img, d, t, sc):
    st = state(t, sc)
    rig(d, t, st["on"], st["lvl"], st["txt"], st["p"], st["flow"], "300 s" if st["done"] else None)
    card(d, (40, 1010, 1040, 1640), fill=WHITE, outline=LIGHT, w=3)
    if st["stg"] == 1: text(d, (W / 2, 1064), "Giai đoạn 1", 46, BLUE)
    else: text(d, (W / 2, 1064), "Giai đoạn 2", 46, ORANGE)
    (a1, b1), (a2, b2) = phases(sc)
    table(d, 1140, (appear(t, b1, 0.35), appear(t, b2, 0.35)))
    # thanh so sanh khoi luong nuoc vao coc (cung thang)
    for j, (lab, m, col, (a, b)) in enumerate((("m₁", 5.0, BLUE, (a1, b1)), ("m₂", 36.4, ORANGE, (a2, b2)))):
        y = 1392 + 80 * j; p = clamp((t - a) / (b - a))
        text(d, (110, y), lab, 44, col)
        d.rounded_rectangle([180, y - 22, 940, y + 22], radius=22, fill=(244, 240, 232))
        wpx = 760 * m / 36.4 * p
        if wpx > 4: d.rounded_rectangle([180, y - 22, 180 + max(44, wpx), y + 22], radius=22, fill=col)
    text(d, (W / 2, 1540), "m₁, m₂: nước vào cốc", 44, INK, bold=False)
    text(d, (W / 2, 1598), "Số liệu mẫu", 44, MUTED, bold=False)

# ---------------- canh 3: Ket qua + Rut ra ----------------
BASE, HMAX = 860, 420
def s_ket(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 950), fill=WHITE, outline=LIGHT, w=3)
    ka = appear(t, M[0] + 0.1, 0.4)
    pill(d, W / 2, 308, "ĐÁP ÁN · Ít hơn nhiều, khác 0", 42, WHITE, NAVY, ka)
    h1, h2 = HMAX * 5.0 / 36.4, HMAX
    split = appear(t, M[1] + 0.1, 0.5)
    # cot giai doan 1
    d.rounded_rectangle([140, BASE - h1, 260, BASE], radius=10, fill=ENV)
    text(d, (200, BASE - h1 - 38), "5,0 g", 42, ENV)
    # cot giai doan 2: day = 5,0 g moi truong + 31,4 g do day
    d.rounded_rectangle([460, BASE - h2, 580, BASE], radius=10, fill=ORANGE)
    if split > 0:
        d.rounded_rectangle([460, BASE - h1, 580, BASE], radius=10, fill=A(ENV, split))
        d.line([(460, BASE - h1), (580, BASE - h1)], fill=A(WHITE, split), width=4)
    text(d, (520, BASE - h2 - 38), "36,4 g", 42, ORANGE)
    d.line([(100, BASE), (640, BASE)], fill=NAVY, width=4)
    text(d, (200, BASE + 46), "Giai đoạn 1", 40, INK)
    text(d, (520, BASE + 46), "Giai đoạn 2", 40, INK)
    if split > 0:
        text(d, (610, BASE - h2 / 2 - 30), "do dây:", 40, ORANGE, anchor="lm", alpha=split)
        text(d, (610, BASE - h2 / 2 + 24), "m₂ − m₁ = 31,4 g", 42, ORANGE, anchor="lm", alpha=split)
        text(d, (610, BASE - h1 / 2), "môi trường", 40, ENV, anchor="lm", alpha=split)
    # nguon nhiet tung giai doan + tinh lambda
    k2 = appear(t, M[0] + 1.0, 0.5)
    k3 = appear(t, M[1] + 0.3, 0.5)
    card(d, (40, 990, 1040, 1290 + 230 * k3), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=4)   # the co lai cho toi khi hien lambda
    text(d, (W / 2, 1070), "λ = U·I·τ / (m₂ − m₁)", 56, INK, alpha=k2)
    text(d, (W / 2, 1150), "λ: nhiệt nóng chảy riêng", 44, INK, bold=False, alpha=k2)
    text(d, (W / 2, 1232), "U·I·τ = 10 800 J;   m₂ − m₁ = 31,4 g", 40, NOTE, alpha=k2)
    text(d, (W / 2, 1380), "λ ≈ 3,44·10⁵ J/kg", 64, ORANGE, alpha=k3)

# ---------------- canh 4: Chua noi duoc gi ----------------
def s_chua(img, d, t, sc):
    rig(d, t, True, LV2, "36,4 g", 1.0, 0, "300 s", labels=False)
    k = appear(t, 0.3, 0.45)
    card(d, (40, 1030, 1040, 1520), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 1100), "Chưa nói được", 48, NAVY, alpha=k)
    for j, s in enumerate(("• Nhiệt dây thất thoát: bao nhiêu?", "• Phòng có ấm dần lên không?")):
        kk = appear(t, 0.6 + 0.4 * j, 0.4)
        text(d, (90, 1240 + 150 * j), s, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Bay ----------------
X0, X1, L0, L1 = 130, 950, 2.9, 3.6
def XL(v): return X0 + (v - L0) / (L1 - L0) * (X1 - X0)

def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 780), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 306, "BẪY", 40, WHITE, RED)
    q = "“Chia luôn cho m₂ = 36,4 g”"
    text(d, (W / 2, 420), q, 46, INK)
    ks = clamp((t - (M[0] + 2.2)) / 0.4)
    if ks > 0:
        lw = tw(d, q, F(46)); d.line([(W / 2 - lw / 2, 422), (W / 2 - lw / 2 + lw * ks, 422)], fill=RED, width=5)
    k1 = appear(t, M[0] + 0.8, 0.45)
    text(d, (W / 2, 545), "λ = U·I·τ / m₂ ≈ 2,97·10⁵ J/kg", 50, RED, alpha=k1)
    text(d, (W / 2, 680), "nhỏ hơn thật 11%", 48, RED, alpha=appear(t, M[0] + 1.5, 0.4))
    # truc so lambda (hinh co ngay tu dau canh)
    card(d, (40, 820, 1040, 1640), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 890), "λ (·10⁵ J/kg)", 44, NAVY)
    text(d, (W / 2, 952), "vạch chia 0,1", 44, NOTE, bold=False)
    ya = 1180
    d.line([(X0 - 20, ya), (X1 + 20, ya)], fill=NAVY, width=5); chevron_r(d, X1 + 24, ya)
    for i in range(8):                               # vach chia 0,1 (khong ghi so; so chi o 3 moc co trong kho)
        x = XL(2.9 + 0.1 * i); d.line([(x, ya - 14), (x, ya + 14)], fill=NAVY, width=3)
    def mark(v, s, lab, col, up, a):
        if a <= 0: return
        x = XL(v); d.line([(x, ya - 22), (x, ya + 22)], fill=A(col, a), width=6); dot(d, x, ya, 13, A(col, a))
        if up:
            text(d, (x, ya - 66), s, 44, col, alpha=a); text(d, (x, ya - 128), lab, 44, col, alpha=a)
        else:
            text(d, (x, ya + 66), s, 44, col, alpha=a); text(d, (x, ya + 128), lab, 44, col, alpha=a)
    mark(3.34, "3,34", "thật", GREEN, True, appear(t, 0.2, 0.4))
    mark(2.97, "2,97", "chia m₂", RED, False, appear(t, M[0] + 0.8, 0.4))
    mark(3.44, "3,44", "chia m₂ − m₁", ORANGE, False, appear(t, M[1] + 0.2, 0.4))
    k2 = appear(t, M[1] + 0.6, 0.45)
    text(d, (W / 2, 1460), "Chỉ 97% nhiệt dây vào đá", 46, INK, alpha=k2)
    text(d, (W / 2, 1560), "→ λ đo lớn hơn thật 3%", 48, ORANGE, alpha=appear(t, M[1] + 1.3, 0.4))

def chevron_r(d, x, y, s=18, w=5):
    for sg in (1, -1):
        a = math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=NAVY, width=w)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    """Hinh nhiet ke phong dang len (khong chu)."""
    cx, y0 = W / 2, 990
    d.rounded_rectangle([cx - 22, y0, cx + 22, y0 + 200], radius=22, fill=A(WHITE, k), outline=A(NAVY, k), width=5)
    dot(d, cx, y0 + 230, 42, A(RED, k)); d.ellipse([cx - 42, y0 + 188, cx + 42, y0 + 272], outline=A(NAVY, k), width=5)
    hh = 70 + 70 * (0.5 + 0.5 * math.sin(t * 1.5))
    d.rectangle([cx - 10, y0 + 200 - hh, cx + 10, y0 + 210], fill=A(RED, k))

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Đá tan do dây: m₂ − m₁",
             "Riêng do phòng ấm hơn ở giai đoạn 2, λ tính ra lệch lên hay xuống?", None, body=_end_body)
    kh = appear(t, M[0] + 4.4, 0.5)                 # goi y hien tre >= 4 s sau cau hoi, chi la cong thuc goc (khong neu huong lech)
    if kh > 0:
        card(d, (110, 1330, 970, 1560), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1385), "Gợi ý", 44, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1470), "λ = U·I·τ / (m₂ − m₁)", 46, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, ch, b, e = sc["hook"], sc["do"], sc["ket"], sc["chua"], sc["bay"], sc["end"]
    (a1, b1), (a2, b2) = phases(do)
    return [(h["t0"] + 0.8, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + a1, "tap"), (do["t0"] + do["M"][1] + 0.1, "tap"),
            (k["t0"] + k["M"][0] + 0.1, "ding"), (ch["t0"] + 0.3, "tap"),
            (b["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-thuchanh-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thực hành đo nhiệt nóng chảy riêng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Phễu nước đá, hai lần đo", draw=s_hook, tail=0.3, caps=[
   ("Phễu nước đá, dây điện trở, cốc hứng.", 3.6),
   ("Chọn đáp án ở khung câu hỏi.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chưa cấp điện, hứng 300 s.", 3.7),
   ("Cấp điện, hứng tiếp 300 s.", 3.7)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.3, caps=[
   ("Đá vẫn nhận nhiệt từ môi trường.", 4.2),
   ("Giai đoạn 2: thêm nhiệt từ dây.", 4.0)]),
 dict(key="chua", title="Giới hạn của thí nghiệm", draw=s_chua, tail=0.4, caps=[
   ("Hai điều chưa đo được.", 5.3)]),
 dict(key="bay", title="Cái bẫy khi tính λ", draw=s_bay, tail=0.7, caps=[
   ("Quên trừ m₁ thì sao?", 3.6),
   ("Nhiệt dây có vào hết đá?", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.4)]),
])
