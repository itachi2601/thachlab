# Clip: tn-l12-camungdt-03 - Tu thong qua khung quay trong tu truong deu (ban 1, 28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-camungdt-03.json:
#   tham_so mac dinh B = 0,2 T, S = 0,05 m^2; so_lieu_mau (alpha do, Phi Wb):
#   0 -> 0,01 ; 30 -> 0,00866 ; 60 -> 0,005 ; 90 -> 0 ; 120 -> -0,005 ; ket_qua_ky_vong Phi = 0,01 cos(alpha).
# Hinh: tu truong deu = duong suc song song cach deu, ra N vao S; khung nhin doc truc quay (doan thang),
#   phap tuyen n hop voi B goc alpha; dai "duong suc xuyen qua khung" cao = L.|cos alpha| -> khop Phi = BS cos alpha.
# Canh: Du doan (4 do thi cung kieu) -> Tien hanh (quay 0 -> 120 do, dung o tung moc, do thi ve dan, dien ke)
#       -> Dap an C + Rut ra -> Bay (goc giua MAT khung va B) + chua noi duoc -> Chot + cau hoi tu nho lai.
from engine import *

# ---------------- bo cuc (khung 1080x1920) ----------------
PX0, PY0, PX1, PY1 = 60, 236, 1020, 790          # khung hinh tu truong
CX, CY, HL = 540, 520, 190                       # tam truc quay, nua chieu dai khung (nhin canh)
LX0, LX1 = 140, 940                              # duong suc tu mat cuc N toi mat cuc S
LINES = [300 + i * 55 for i in range(9)]         # 9 duong suc cach deu
COPPER = (184, 115, 51)
ROWS = [(0, 0.01), (30, 0.00866), (60, 0.005), (90, 0.0), (120, -0.005)]
PMAX, PMIN = 0.0115, -0.0065


def fphi(p):
    if p == 0: return "0"
    return repr(p).replace(".", ",").replace("-", "−")


def phi_model(a): return 0.2 * 0.05 * math.cos(math.radians(a))     # B.S.cos(alpha)


def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)


def dashed(d, p1, p2, color, w=3, dash=12, gap=9):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))],
               fill=color, width=w)


def tag(d, x, y, s, size, color, alpha=1.0):
    wd = tw(d, s, F(size)) + 20
    d.rounded_rectangle([x - wd / 2, y - size * 0.62, x + wd / 2, y + size * 0.62], radius=10, fill=A(WHITE, 0.92 * alpha))
    text(d, (x, y), s, size, color, alpha=alpha)


# ---------------- hinh tu truong + khung ----------------
def field_panel(d, a, band=True, arc=True, frame_label=False, wires=False):
    card(d, (PX0, PY0, PX1, PY1), fill=WHITE, outline=LIGHT, w=3)
    c = math.cos(math.radians(a)); half = HL * abs(c)
    bcol = ORANGE if c >= 0 else PURPLE
    if band and half > 1:                         # dai dam o quanh khung, mo dan ra hai phia
        for x in range(LX0, LX1, 20):
            al = 0.05 + 0.17 * math.exp(-((x + 10 - CX) / 230) ** 2)
            d.rectangle([x, CY - half, x + 20, CY + half], fill=A(bcol, al))
    for y in LINES:
        inside = band and abs(y - CY) <= half + 0.5
        col = bcol if inside else (150, 170, 210)
        d.line([(LX0, y), (LX1, y)], fill=col, width=4 if inside else 3)
        for x in (300, 780): chevron(d, x, y, 0, col)
    # hai cuc nam cham (mat phang song song -> tu truong giua hai cuc gan deu)
    d.rounded_rectangle([80, 284, LX0, 756], radius=10, fill=RED)
    d.rounded_rectangle([LX1, 284, 1000, 756], radius=10, fill=BLUE)
    text(d, (110, 520), "N", 44, WHITE); text(d, (970, 520), "S", 44, WHITE)
    arrow(d, (170, 266), (260, 266), BLUE, w=4, head=16)
    text(d, (274, 266), "B", 38, BLUE, anchor="lm")
    if band:
        lg = "dải cam: xuyên qua khung" if c >= 0 else "dải tím: xuyên ngược n, Φ < 0"
        text(d, (340, 266), lg, 32, bcol, bold=False, anchor="lm")
    if wires:                                     # day noi tu truc khung xuong dien ke
        for dx in (0, 14):
            d.line([(CX + dx, CY), (CX + dx, 774 + dx * 0.0), (790 + dx, 774), (790 + dx, 812)], fill=(90, 96, 112), width=3)
    # khung (nhin doc truc quay): doan thang vuong goc phap tuyen n
    s, cc = math.sin(math.radians(a)), c
    p1 = (CX - HL * s, CY - HL * cc); p2 = (CX + HL * s, CY + HL * cc)
    d.line([p1, p2], fill=COPPER, width=16)
    for p in (p1, p2): dot(d, p[0], p[1], 10, COPPER)
    dot(d, CX, CY, 9, NAVY, outline=WHITE)
    # phap tuyen n
    tip = (CX + 150 * cc, CY - 150 * s)
    arrow(d, (CX, CY), tip, GREEN, w=6, head=20)
    tag(d, CX + 190 * cc - 32 * s, CY - 190 * s - 32 * cc, "n", 38, GREEN)
    if frame_label:
        tx, ty = CX - 120 * s, CY - 120 * cc; lx, ly = 300, 430
        tag(d, lx, ly, "khung (nhìn cạnh)", 34, COPPER)
        ang = math.atan2(ty - ly, tx - (lx + 162)); e = (tx - 18 * math.cos(ang), ty - 18 * math.sin(ang))
        arrow(d, (lx + 162, ly), e, COPPER, w=4, head=16)
    if arc and a > 2:
        d.arc([CX - 70, CY - 70, CX + 70, CY + 70], 360 - a, 360, fill=GREEN, width=5)
        am = math.radians(a / 2); tag(d, CX + 104 * math.cos(am), CY - 104 * math.sin(am), "α", 36, GREEN)


# ---------------- do thi Phi theo alpha (truc co dinh 0..120 do) ----------------
def plot(d, box, a_drawn, recs, hl=0.0, pen=False):
    x0, yt, x1, yb = box
    X = lambda a: x0 + a / 120 * (x1 - x0)
    Y = lambda p: yt + (PMAX - p) / (PMAX - PMIN) * (yb - yt)
    if hl > 0:
        d.rounded_rectangle([X(0) - 6, yt - 6, X(90) + 6, yb + 6], radius=14, fill=A((187, 247, 208), 0.6 * hl),
                            outline=A(GREEN, hl), width=4)
    for p in (0.01, 0.005, -0.005):
        dashed(d, (x0, Y(p)), (x1, Y(p)), LIGHT, 3)
        text(d, (x0 - 14, Y(p)), fphi(p), 34, MUTED, bold=False, anchor="rm")
    for a in (30, 60, 90, 120):
        dashed(d, (X(a), yt), (X(a), yb), LIGHT, 3)
    for a in (0, 30, 60, 90, 120):
        text(d, (X(a), yb + 32), str(a), 34, MUTED, bold=False)
    d.line([(x0, yb + 4), (x0, yt - 14)], fill=NAVY, width=5)
    d.polygon([(x0, yt - 30), (x0 - 10, yt - 12), (x0 + 10, yt - 12)], fill=NAVY)
    d.line([(x0, Y(0)), (x1 + 20, Y(0))], fill=NAVY, width=5)
    text(d, (x0 - 14, Y(0)), "0", 34, MUTED, bold=False, anchor="rm")
    text(d, (x0 + 20, yt - 20), "Φ (Wb)", 34, INK, anchor="lm")
    text(d, (x1 + 40, Y(0) - 30), "α (°)", 34, INK, anchor="rm")
    if a_drawn > 0.2:
        n = max(2, int(a_drawn * 1.5))
        d.line([(X(a_drawn * k / (n - 1)), Y(phi_model(a_drawn * k / (n - 1)))) for k in range(n)],
               fill=BLUE, width=7, joint="curve")
    for a, p in recs: dot(d, X(a), Y(p), 12, ORANGE, outline=WHITE)
    if pen and 0.2 < a_drawn < 119.8: dot(d, X(a_drawn), Y(phi_model(a_drawn)), 12, RED, outline=WHITE)
    return X, Y


# ---------------- canh 1: mo dau + Du doan ----------------
OPTS = [("A", lambda x: 0.85), ("B", lambda x: math.sin(x * math.pi / 2)),
        ("C", lambda x: math.cos(x * math.pi / 2)), ("D", lambda x: 0.9 * math.sin(x * math.pi))]


def s_hook(img, d, t, sc):
    field_panel(d, 0, frame_label=True)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    if k <= 0: return
    y0 = 806 + (1 - k) * 40
    card(d, (40, y0, 1040, y0 + 840), fill=A(WHITE, k), outline=A(PURPLE, k), w=5)
    text(d, (W / 2, y0 + 46), "Dự đoán", 40, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 104), "Quay khung từ 0° tới 90°,", 38, INK, alpha=k)
    text(d, (W / 2, y0 + 152), "B, S không đổi. Đồ thị Φ theo α?", 38, INK, alpha=k)
    for i, (lab, f) in enumerate(OPTS):
        bx = 80 + (i % 2) * 470; by = y0 + 196 + (i // 2) * 300
        card(d, (bx, by, bx + 450, by + 280), fill=A((247, 248, 252), k), outline=A(NAVY, k), r=24, w=4)
        text(d, (bx + 40, by + 44), lab + ".", 40, NAVY, alpha=k)
        gx0, gy0, gx1, gy1 = bx + 110, by + 220, bx + 410, by + 40
        d.line([(gx0, gy1), (gx0, gy0), (gx1, gy0)], fill=A(MUTED, k), width=4)
        text(d, (gx0 - 14, gy1 + 10), "Φ", 32, MUTED, anchor="rm", alpha=k)
        text(d, (gx0, gy0 + 30), "0", 32, MUTED, bold=False, alpha=k)
        text(d, (gx1 - 20, gy0 + 30), "90°", 32, MUTED, bold=False, alpha=k)
        P = [(gx0 + 6 + u / 30 * (gx1 - gx0 - 26), gy0 - 4 - f(u / 30) * (gy0 - gy1 - 20)) for u in range(31)]
        d.line(P, fill=A(NAVY, k), width=7, joint="curve")
    t1, t2 = sc["M"][1] + 0.4, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))     # thanh dem thoi gian nghi
    d.rounded_rectangle([140, y0 + 800, 940, y0 + 812], radius=6, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, y0 + 800, 140 + 800 * (1 - q), y0 + 812], radius=6, fill=A(PURPLE, k))


# ---------------- canh 2: tien hanh ----------------
def segs(sc):
    M = sc["M"]
    return [(M[1], M[1] + 0.9, 0, 30), (M[1] + 1.5, M[1] + 2.4, 30, 60), (M[2], M[2] + 0.9, 60, 90),
            (M[3], M[3] + 2.0, 90, 120)]


def alpha_at(t, sc):
    a = 0.0
    for s0, s1, a0, a1 in segs(sc):
        if t >= s0: a = lerp(a0, a1, ease((t - s0) / (s1 - s0)))
    return a


def records(t, sc):
    times = [sc["M"][0] + 0.5] + [s1 + 0.05 for s0, s1, a0, a1 in segs(sc)]
    return [r for r, tm in zip(ROWS, times) if t >= tm]


def galvo(d, g):
    card(d, (680, 806, 1020, 966), fill=WHITE, outline=NAVY, w=4, r=24)
    gx, gy, gr = 850, 950, 100
    text(d, (700, 838), "điện kế", 34, MUTED, bold=False, anchor="lm")
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 270 - 55, 270 + 55, fill=NAVY, width=4)
    d.line([(gx, gy - gr), (gx, gy - gr + 18)], fill=NAVY, width=4)
    for v in (-1, -0.5, 0.5, 1):
        an = math.radians(v * 50)
        d.line([(gx + (gr - 12) * math.sin(an), gy - (gr - 12) * math.cos(an)),
                (gx + gr * math.sin(an), gy - gr * math.cos(an))], fill=NAVY, width=3)
    an = math.radians(clamp(g, -1, 1) * 50)
    d.line([(gx, gy), (gx + (gr - 6) * math.sin(an), gy - (gr - 6) * math.cos(an))], fill=RED, width=7)
    dot(d, gx, gy, 10, NAVY)


def s_do(img, d, t, sc):
    a = alpha_at(t, sc)
    rot = any(s0 < t < s1 for s0, s1, a0, a1 in segs(sc))
    dadt = (alpha_at(t + 0.01, sc) - alpha_at(t - 0.01, sc)) / 0.02
    g = math.sin(math.radians(a)) * dadt / 45.0              # kim lech chi khi Phi dang bien thien (dang quay)
    field_panel(d, a, frame_label=t < sc["M"][2], wires=True)
    recs = records(t, sc)
    card(d, (60, 806, 650, 966), fill=WHITE, outline=NAVY, w=4, r=24)
    if recs and not rot:
        ra, rp = recs[-1]
        text(d, (96, 850), f"α = {ra}°", 46, GREEN, anchor="lm")
        text(d, (96, 920), f"Φ = {fphi(rp)} Wb", 46, ORANGE, anchor="lm")
    else:
        text(d, (355, 886), "đang quay…", 40, MUTED, bold=False)
    galvo(d, g)
    card(d, (60, 990, 1020, 1660), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (200, 1060, 940, 1570), a, recs, pen=True)


# ---------------- canh 3: dap an + rut ra ----------------
def kcard(d, y, title, ev, color, k, h=180):
    if k <= 0: return
    yy = y + (1 - k) * 30
    card(d, (60, yy, 1020, yy + h), fill=A(WHITE, k), outline=A(color, k), w=5)
    text(d, (W / 2, yy + 50), title, 42, color, alpha=k)
    text(d, (W / 2, yy + h - 48), ev, 36, MUTED, bold=False, alpha=k)


def s_rut(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 236, 1020, 860), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (200, 320, 940, 770), 120, ROWS, hl=appear(t, M[0] + 0.3, 0.5))
    ka = appear(t, M[0] + 0.3, 0.4)
    if ka > 0:
        pw = tw(d, "ĐÁP ÁN C", F(34)) + 48
        card(d, (1000 - pw, 256, 1000, 314), fill=A(GREEN, ka), r=29)
        text(d, (1000 - pw / 2, 285), "ĐÁP ÁN C", 34, WHITE, alpha=ka)
    kcard(d, 890, "Càng nghiêng, càng ít đường sức qua", "", GREEN,
          appear(t, M[1], 0.45))
    kcard(d, 1100, "Φ = BS cosα = 0,01 cosα (Wb)", "B = 0,2 T, S = 0,05 m²", ORANGE,
          appear(t, M[1] + 1.5, 0.45))
    kcard(d, 1310, "Quay đều → Φ tuần hoàn", "máy phát điện", PURPLE,
          appear(t, M[2], 0.45))


# ---------------- canh 4: cai bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    field_panel(d, 60, arc=False)
    d.arc([CX - 75, CY - 75, CX + 75, CY + 75], 300, 360, fill=GREEN, width=5)      # n voi B: 60 do
    tag(d, CX + 150 * math.cos(math.radians(30)), CY - 150 * math.sin(math.radians(30)) - 6, "α = 60°", 34, GREEN)
    d.arc([CX - 120, CY - 120, CX + 120, CY + 120], 0, 30, fill=RED, width=5)       # mat khung voi B: 30 do
    tag(d, CX + 180 * math.cos(math.radians(15)), CY + 180 * math.sin(math.radians(15)) + 10, "30°", 34, RED)
    k1 = appear(t, 0.3, 0.45); k3 = appear(t, M[1] + 3.3, 0.45); a1 = k1 * (1 - k3)
    y = 830
    if a1 > 0:
        card(d, (60, y, 1020, y + 520), fill=A(WHITE, a1), outline=A(RED, a1), w=5)
        text(d, (W / 2, y + 56), "Cái bẫy", 44, RED, alpha=a1)
        text(d, (W / 2, y + 150), "Lấy góc mặt khung và B → SAI", 42, INK, alpha=a1)
        k2 = appear(t, M[1], 0.45) * a1
        text(d, (W / 2, y + 276), "Lấy 30°: 0,00866 Wb (sai)", 42, RED, bold=False, alpha=k2)
        text(d, (W / 2, y + 376), "Đúng α = 60°: 0,005 Wb", 44, GREEN, alpha=k2)
    if k3 > 0:
        card(d, (60, y, 1020, y + 520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, y + 56), "Chưa nói được", 44, NAVY, alpha=k3)
        for j, s in enumerate(("• Chiều dòng: Lenz", "• Độ lớn: Faraday", "• Số liệu minh hoạ")):
            text(d, (110, y + 170 + j * 110), s, 40, INK, bold=False, anchor="lm", alpha=k3)


# ---------------- canh 5: chot + cau hoi ----------------
def _end_body(d, t, k):
    text(d, (W / 2, 1110), "B = 0,2 T · S = 0,05 m²", 40, MUTED, bold=False, alpha=k)


def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "B, S không đổi, Φ vẫn đổi",
             "Φ = 0,005 Wb ứng với\ngóc α bằng bao nhiêu?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)                 # goi y hien sau, de HS tu nghi truoc
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 36, MUTED, bold=False, alpha=kh)
        ctext(d, 1440, "Nhớ lại dạng đồ thị Φ theo α", 42, ORANGE, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][1], "tap"), (do["t0"] + do["M"][3], "tap"), (do["t0"] + do["M"][4], "tap"),
            (r["t0"] + r["M"][0] + 0.3, "ding"), (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]


CLIP = dict(id="tn-l12-camungdt-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khung quay trong từ trường", draw=s_hook, tail=0.3, caps=[
   ("Khung quay giữa hai cực.", 2.4),
   ("Chọn A, B, C hay D.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bắt đầu α = 0°.", 2.8),
   ("Dừng ở 30°, rồi 60°.", 3.2),
   ("90°: song song đường sức.", 2.6),
   ("Quay tiếp: kim lệch.", 2.6),
   ("120°: Φ đổi dấu.", 3.0)]),
 dict(key="rut", title="Kết luận", draw=s_rut, tail=0.4, caps=[
   ("0° → 90°: Φ về 0.", 2.8),
   ("Chú ý công thức.", 2.8),
   ("Quay đều: Φ lặp lại.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("α đo từ pháp tuyến n.", 3.6),
   ("Giới hạn.", 6.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("α bằng mấy?", 5.0)]),
])
