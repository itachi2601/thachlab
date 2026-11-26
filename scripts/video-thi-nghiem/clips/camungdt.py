# Clip: tn-l12-camungdt-01 - Nam cham va cuon day noi dien ke (ban 2, 27/10/2026)
# So lieu lay tu content/thi-nghiem/tn-l12-camungdt-01.json -> so_lieu_mau:
#   dung yen 0,0 -> 0 ; dua vao 0,1 -> +1,0 ; dua vao 0,2 -> +2,1 ; dua vao 0,4 -> +3,9 ; rut ra 0,2 -> -2,0 (mA)
# Ban 3 (27/10/2026): thanh dem o hop Du doan, lo dap an B ngay luc nam yen, canh chot + cau hoi doi cuc S, tieng bao.
# Ban 4 (26/11/2026): chu >= 58, bo chip buoc + nhan "DAP AN B" (khong co A-D trong video), so chi la mot so don,
#   hop Du doan / Bay / THU NGHI tu ve, moi noi dung nam tren vung phu de (y <= 1580).
from engine import *
NOTE = (70, 75, 95); EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- bo cuc (toa do khung 1080x1920) ----------------
CX, CY, CR = 640, 470, 118            # tam cuon day, nua chieu cao vong day
NT, CSPAN = 10, 300                   # so vong ve, be dai cuon
CL, CRR = CX - CSPAN // 2, CX + CSPAN // 2
ML, MH = 300, 84                      # be dai, be day nam cham
OUT_TIP, IN_TIP = 400, 700            # vi tri dau cuc N: ngoai cuon / trong cuon
GX, GY, GR = 540, 1090, 250           # tam quay kim dien ke, ban kinh mat so
GMAX, GANG = 5.0, 56                  # thang do +-5 mA, kim lech toi da 56 do
TL, TR = (CL, 752), (CRR, 752)        # hai cuc dien ke (tren mep the)
TAB_Y = 1215                          # bang so lieu / hop du doan (day <= 1575, tren vung phu de)

ROWS = [("Cắm nhanh", 0.4, 3.9), ("Cắm chậm", 0.1, 1.0), ("Nằm yên", 0.0, 0.0), ("Rút ra", 0.2, -2.0)]


def fmt(x, sign=True):
    if abs(x) < 0.05: return "0"
    s = (f"{x:+.1f}" if sign else f"{abs(x):.1f}").replace(".", ",")
    return s.replace("-", "−")


# ---------------- hinh ve ----------------
def turns():
    return [CL + j * CSPAN / (NT - 1) for j in range(NT)]


def coil_back(d):
    c = mix(ORANGE, BG, 0.45)
    for x in turns():
        d.arc([x - 17, CY - CR, x + 17, CY + CR], 90, 270, fill=c, width=7)


def coil_front(d):
    for x in turns():
        d.arc([x - 17, CY - CR, x + 17, CY + CR], 270, 90, fill=A(ORANGE, 0.92), width=9)
    text(d, (900, CY - 175), "600 vòng", 58, NOTE)


def dashed_ellipse(d, box, a0, a1, color, w=4, seg=7, gap=6):
    x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
           for a in [a0 + (a1 - a0) * k / 120 for k in range(121)]]
    acc, on, cur = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        acc += math.dist(p, q); cur.append(q)
        if acc >= (seg if on else gap):
            if on and len(cur) > 1: d.line(cur, fill=color, width=w)
            on, acc, cur = not on, 0.0, [q]
    if on and len(cur) > 1: d.line(cur, fill=color, width=w)


def chevron(d, x, y, ang, color, s=13, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)


def _trace(ang, inset=10):
    """Duong suc cua hai cuc tu dat gan hai dau nam cham (N duong, S am), toa do tuong doi (tip, CY)."""
    nx, sx = -inset, -ML + inset
    x, y = nx + 6 * math.cos(ang), -6 * math.sin(ang); pts = [(x, y)]
    for _ in range(4000):
        ex = ey = 0.0
        for px, q in ((nx, 1), (sx, -1)):
            dx, dy = x - px, y; r3 = (dx * dx + dy * dy) ** 1.5; ex += q * dx / r3; ey += q * dy / r3
        n = math.hypot(ex, ey); x += 3 * ex / n; y += 3 * ey / n; pts.append((x, y))
        if math.hypot(x - sx, y) < 8: break
    return pts

# Ba duong phia tren (duoi = doi xung). Ep doc de vua khung (giu dung hinh dang: ra o N, vao o S).
_RAW = [_trace(math.radians(a)) for a in (60, 80, 100)]
_SQ = 190 / max(-y for _, y in _RAW[0])
FIELD = [[(x, y * _SQ) for x, y in ln] for ln in _RAW]


def dashed_poly(d, pts, color, w=4, seg=10, gap=8):
    acc, on, cur = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        acc += math.dist(p, q); cur.append(q)
        if acc >= (seg if on else gap):
            if on and len(cur) > 1: d.line(cur, fill=color, width=w)
            on, acc, cur = not on, 0.0, [q]
    if on and len(cur) > 1: d.line(cur, fill=color, width=w)


def field(d, tip, alpha):
    """Duong suc ngoai nam cham: di ra o cuc N (phai), vong qua, di vao cuc S (trai). Net dut, mui chevron."""
    if alpha <= 0: return
    c = A(PURPLE, 0.55 * alpha)
    for ln in FIELD:
        for sg in (1, -1):
            pts = [(tip + x, CY + sg * y) for x, y in ln]
            dashed_poly(d, pts, c)
            k = min(range(len(pts)), key=lambda n: -abs(pts[n][1] - CY))      # dinh cung: mui ten chi N -> S
            (x0, y0), (x1, y1) = pts[max(0, k - 3)], pts[min(len(pts) - 1, k + 3)]
            chevron(d, pts[k][0], pts[k][1], math.atan2(y1 - y0, x1 - x0), c)
    # duong truc: ra khoi N ben phai, vao S ben trai
    d.line([(tip + 6, CY), (tip + 120, CY)], fill=c, width=4); chevron(d, tip + 120, CY, 0, c)
    xs = tip - ML
    d.line([(xs - 120, CY), (xs - 6, CY)], fill=c, width=4); chevron(d, xs - 40, CY, 0, c)


def magnet(d, tip, alpha=1.0):
    if alpha <= 0: return
    if alpha < 0.999:  # ve tren lop rieng roi dan voi do mo, tranh vet chong mau o giua
        im = d._image; lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        magnet(ImageDraw.Draw(lay, "RGBA"), tip, 1.0)
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
        im.paste(lay, (0, 0), lay); return
    x0, xm = tip - ML, tip - ML / 2
    d.rounded_rectangle([x0, CY - MH / 2, xm, CY + MH / 2], radius=10, fill=A(BLUE, alpha))
    d.rounded_rectangle([xm, CY - MH / 2, tip, CY + MH / 2], radius=10, fill=A(RED, alpha))
    d.rectangle([xm - 10, CY - MH / 2, xm + 10, CY + MH / 2], fill=A(RED, alpha))
    d.rectangle([xm - 10, CY - MH / 2, xm, CY + MH / 2], fill=A(BLUE, alpha))
    text(d, (x0 + ML / 4, CY + 1), "S", 60, WHITE, alpha=alpha)
    text(d, (tip - ML / 4, CY + 1), "N", 60, WHITE, alpha=alpha)


def wires(d):
    l0 = (CL, CY + CR - 4); r0 = (CRR, CY + CR - 4)
    d.line([l0, TL], fill=NAVY, width=5); d.line([r0, TR], fill=NAVY, width=5)
    for p in (TL, TR): dot(d, p[0], p[1], 11, NAVY)


def needle_xy(i, r):
    a = math.radians(clamp(i / GMAX, -1.08, 1.08) * GANG)
    return GX + r * math.sin(a), GY - r * math.cos(a)


def galvo(d, i, ghost=None, peak=None, hide=False):
    card(d, (150, 760, 930, 1190), fill=WHITE, outline=NAVY, r=30, w=5)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 270 - GANG - 3, 270 + GANG + 3, fill=NAVY, width=5)
    for v in range(-5, 6):
        a = math.radians(v / GMAX * GANG); big = v % 2 == 0
        r0 = GR - (30 if big else 18)
        d.line([(GX + r0 * math.sin(a), GY - r0 * math.cos(a)), (GX + GR * math.sin(a), GY - GR * math.cos(a))],
               fill=NAVY, width=5 if big else 3)
        if big:
            lx, ly = GX + (GR + 40) * math.sin(a), GY - (GR + 40) * math.cos(a)
            text(d, (lx, ly), str(v).replace("-", "−"), 58, NAVY)
    text(d, (895, 1150), "mA", 58, NOTE, anchor="rm")
    if hide:                                               # luc hoi Du doan: che kim, khong lo dap an
        dot(d, GX, GY, 16, NAVY); text(d, (GX, GY - 140), "?", 90, PURPLE); return
    if ghost is not None and abs(ghost) > 0.05 and abs(ghost - i) > 0.1:
        d.line([(GX, GY), needle_xy(ghost, GR - 8)], fill=A(GRAY, 0.8), width=5)
    d.line([(GX, GY), needle_xy(i, GR - 8)], fill=RED, width=9)
    dot(d, GX, GY, 16, NAVY)
    sh = i if not peak else (peak if abs(i) >= 0.5 * abs(peak) else 0.0)   # so nhay thang 0 <-> dinh
    col = RED if sh > 0.05 else (BLUE if sh < -0.05 else NOTE)
    text(d, (250, 1150), fmt(sh), 62, col)                 # mot so don (mA o goc phai)


def vlabel(d, s, alpha=1.0):
    if s: text(d, (250, 680), s, 58, BLUE, alpha=alpha)


def apparatus(d, tip, i, ghost=None, malpha=1.0, vtxt="", field_on=True, peak=None, hide=False):
    if field_on: field(d, tip, malpha)
    coil_back(d)
    magnet(d, tip, malpha)
    coil_front(d)
    if malpha > 0.5:                                   # nhan N/S ve sau cuon day (khong bi vong day de len)
        for cx_, s_, col in ((tip - ML / 4, "N", RED), (tip - 3 * ML / 4, "S", BLUE)):
            d.rounded_rectangle([cx_ - 30, CY - 34, cx_ + 30, CY + 34], radius=12, fill=A(col, malpha))
            text(d, (cx_, CY + 1), s_, 60, WHITE, alpha=malpha)
    wires(d)
    galvo(d, i, ghost, peak, hide)
    vlabel(d, vtxt)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = appear(t, M[1] - 0.2, 0.45)
    apparatus(d, OUT_TIP if k <= 0 else IN_TIP, 0.0, hide=k > 0, malpha=1.0)
    if k <= 0: return
    y0 = TAB_Y + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 360), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 58, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 150), "Nằm yên trong cuộn dây,", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 230), "kim điện kế thế nào?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 275, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)


# ---------------- canh 2: tien hanh ----------------
# (chi so phu de, tre sau phu de, thoi gian chuyen dong, dau N tu, toi, dong mA, nhan v)
PH = [(0, 0.8, 0.75, OUT_TIP, IN_TIP, 3.9, "v = 0,4 m/s →"),
      (1, 0.9, 2.2, OUT_TIP, IN_TIP, 1.0, "v = 0,1 m/s →"),
      (2, 0.0, 0.0, IN_TIP, IN_TIP, 0.0, "v = 0"),
      (3, 0.7, 1.5, IN_TIP, OUT_TIP, -2.0, "← v = 0,2 m/s")]


def do_state(t, sc):
    tip, i, ghost, malpha, vt, done, pk = OUT_TIP, 0.0, None, 1.0, "", 0, None
    for n, (k, dl, dur, xa, xb, im, lab) in enumerate(PH):
        m = sc["M"][k]
        if t < m - 0.05: break
        t0, t1 = m + dl, m + dl + dur
        tip, i, ghost, vt = xa, 0.0, None, ""
        if n == 1:  # dat lai nam cham ra ngoai (mo di, hien lai) truoc lan cam cham
            u = t - m
            if u < 0.6:
                tip = IN_TIP if u < 0.3 else OUT_TIP
                malpha = 1 - ease(u / 0.3) if u < 0.3 else ease((u - 0.3) / 0.3)
            else: malpha = 1.0
        if dur == 0:
            vt = lab; done = n + (1 if t > m + 1.7 else 0); continue
        if t >= t0:
            tip = lerp(xa, xb, clamp((t - t0) / dur))
            i = im * ease((t - t0) / 0.14) * (1 - ease((t - t1) / 0.16)); pk = im
            if t <= t1 + 0.05: vt = lab
            if t > t1 + 0.1: ghost = im; done = n + 1
            else: done = n
        else: done = n
    return tip, i, ghost, malpha, vt, done, pk


def table(d, nrows, hl=-1, y=TAB_Y, alpha=1.0):
    card(d, (60, y, 1020, y + 360), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, s, an in ((100, "Cách làm", "lm"), (590, "v (m/s)", "mm"), (860, "mA", "mm")):
        text(d, (x, y + 42), s, 58, NOTE, anchor=an, alpha=alpha)
    d.line([(90, y + 80), (990, y + 80)], fill=A(LIGHT, alpha), width=3)
    for j, (nm, v, im) in enumerate(ROWS[:nrows]):
        yy = y + 120 + j * 64
        if j == hl: d.rounded_rectangle([80, yy - 30, 1000, yy + 30], radius=14, fill=A(mix(ORANGE, WHITE, 0.85), alpha))
        col = RED if im > 0 else (BLUE if im < 0 else NOTE)
        text(d, (100, yy), nm, 58, INK, anchor="lm", alpha=alpha)
        text(d, (590, yy), fmt(v, sign=False) if v else "0", 58, INK, alpha=alpha)
        text(d, (860, yy), fmt(im), 60, col, alpha=alpha)


def s_do(img, d, t, sc):
    tip, i, ghost, malpha, vt, done, pk = do_state(t, sc)
    cur = cur_cap(sc, t)
    apparatus(d, tip, i, ghost, malpha, vt, peak=pk)
    table(d, done, hl=done - 1 if done > 0 and (cur == done - 1) else -1)


# ---------------- canh 3: rut ra ----------------
def chart(d, t, sc):
    M = sc["M"]
    card(d, (60, 250, 1020, 790), fill=WHITE, outline=LIGHT, w=3)
    ox, oy, sx, sy = 210, 560, 1700, 54          # px/(m/s), px/mA
    d.line([(ox, 300), (ox, 740)], fill=NAVY, width=4)
    d.line([(ox, oy), (ox + 0.45 * sx, oy)], fill=NAVY, width=4)
    chevron(d, ox, 300, -math.pi / 2, NAVY, s=18, w=5); chevron(d, ox + 0.45 * sx, oy, 0, NAVY, s=18, w=5)
    text(d, (ox + 26, 310), "i (mA)", 58, NOTE, anchor="lm")
    text(d, (ox + 0.45 * sx, oy + 115), "v (m/s)", 58, NOTE, anchor="rm")
    for v in (0.1, 0.2, 0.3, 0.4):
        x = ox + v * sx; d.line([(x, oy - 8), (x, oy + 8)], fill=NAVY, width=3)
        text(d, (x - 30, oy + 40), fmt(v, sign=False), 58, NOTE)
    for im in (-2, 2, 4):
        y = oy - im * sy; d.line([(ox - 8, y), (ox + 8, y)], fill=NAVY, width=3)
        text(d, (ox - 22, y), str(im).replace("-", "−"), 58, NOTE, anchor="rm")
    k0 = appear(t, M[1] - 0.1, 0.8)
    if k0 > 0:  # duong qua goc toa do
        x1 = lerp(0, 0.4, k0)
        d.line([(ox, oy), (ox + x1 * sx, oy - x1 * 9.75 * sy)], fill=A(ORANGE, 0.45), width=5)
    pts = [(0.0, 0.0), (0.1, 1.0), (0.4, 3.9)]                # chi cac lan da lam o canh Tien hanh
    for j, (v, im) in enumerate(pts):
        k = appear(t, M[0] + 0.2 + 0.25 * j, 0.35)
        if k <= 0: continue
        x, y = ox + v * sx, oy - im * sy
        dot(d, x, y, 15 * k, ORANGE, outline=WHITE)
        if v: text(d, (x - 20, y - 40), fmt(im), 58, ORANGE, anchor="rm", alpha=k)
    k = appear(t, M[2], 0.45)
    if k > 0:
        x, y = ox + 0.2 * sx, oy + 2.0 * sy
        dot(d, x, y, 15 * k, PURPLE, outline=WHITE)
        text(d, (x + 36, y + 16), "−2,0", 58, PURPLE, anchor="lm", alpha=k)


def kcard(d, y, title, color, k, h=120):
    if k <= 0: return
    yy = y + (1 - k) * 30
    card(d, (60, yy, 1020, yy + h), fill=A(WHITE, k), outline=A(color, k), w=5)
    text(d, (W / 2, yy + h / 2), title, 60, color, alpha=k)


def s_rut(img, d, t, sc):
    M = sc["M"]
    chart(d, t, sc)
    kcard(d, 830, "Φ biến thiên: có dòng", GREEN, appear(t, M[0], 0.45))
    kcard(d, 985, "Càng nhanh, dòng càng lớn", ORANGE, appear(t, M[1], 0.45))
    kcard(d, 1140, "Dòng đổi chiều", PURPLE, appear(t, M[2], 0.45))


# ---------------- canh 4: Bay "co tu truong la co dong" + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    apparatus(d, IN_TIP, 0.0, vtxt="v = 0")
    b = appear(t, M[2], 0.45)
    y = TAB_Y
    if b < 1:
        a1 = 1 - b
        card(d, (40, y, 1040, y + 360), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 62, "BẪY", RED, a1)
        q = "“Có từ trường là có dòng”"
        ks = clamp((t - mk) / 0.4); f = F(60); lw = tw(d, q, f); yy = y + 170
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        kc = appear(t, mk + 0.2, 0.45)
        if kc > 0: text(d, (W / 2, y + 285), "Cần Φ biến thiên", 62, mix(GREEN, (21, 128, 61), 0.5), alpha=kc * a1)
    if b > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, b), outline=A(NAVY, b), w=5)
        pill(d, W / 2, y + 62, "CHƯA NÓI ĐƯỢC", NAVY, b)
        text(d, (W / 2, y + 190), "Chiều dòng: định luật Lenz", 60, INK, alpha=b)


# ---------------- canh 5: THU NGHI (cau chot o khung: doi cuc S, cam nhanh) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1520), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k)
    gx, gy, gr = 540, 1440, 200                                  # dien ke nho, kim che bang "?"
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 270 - GANG, 270 + GANG, fill=A(NAVY, k), width=5)
    for v in range(-4, 5, 2):
        a = math.radians(v / GMAX * GANG)
        d.line([(gx + (gr - 24) * math.sin(a), gy - (gr - 24) * math.cos(a)), (gx + gr * math.sin(a), gy - gr * math.cos(a))], fill=A(NAVY, k), width=5)
    text(d, (gx, gy - gr - 30), "0", 58, NAVY, alpha=k)
    text(d, (gx, gy - 95), "?", 84, PURPLE, alpha=k); dot(d, gx, gy - 10, 14, A(NAVY, k))
    my, x0, x1 = 500, 130, 430                                   # nam cham dao: cuc S quay vao cuon
    xm = (x0 + x1) / 2
    d.rounded_rectangle([x0, my - 42, xm, my + 42], radius=10, fill=A(RED, k))
    d.rounded_rectangle([xm, my - 42, x1, my + 42], radius=10, fill=A(BLUE, k))
    text(d, ((x0 + xm) / 2, my + 1), "N", 60, WHITE, alpha=k); text(d, ((xm + x1) / 2, my + 1), "S", 60, WHITE, alpha=k)
    arrow(d, (200, my + 95), (380, my + 95), A(NAVY, k), w=8, head=26)
    for j in range(8):
        x = 560 + j * 40
        d.arc([x - 16, my - 100, x + 16, my + 100], 0, 360, fill=A(ORANGE, k), width=7)
    text(d, (W / 2, 760), "Đổi cực S vào trước,", 64, INK, alpha=k)
    text(d, (W / 2, 850), "cắm nhanh như lần 1 (+3,9).", 64, INK, alpha=k)
    text(d, (W / 2, 950), "Kim lệch về phía nào?", 64, DORANGE, alpha=k)
    seg_bar(d, 1060, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + do["M"][k] + dl, "tap") for k, dl, dur, *_ in PH if dur > 0]
            + [(r["t0"] + r["M"][0], "tap"), (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2], "tap"),
               (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l12-camungdt-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Cuộn dây không có pin", draw=s_hook, tail=0.3, caps=[
   ("Cuộn 600 vòng, không pin.", 3.2),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Cắm nhanh cực N.", 3.0),
   ("Cắm chậm hơn.", 3.6),
   ("Nằm yên: kim về 0.", 3.0),
   ("Rút ra.", 3.0)]),
 dict(key="rut", title="Kết luận", draw=s_rut, tail=0.6, caps=[
   ("Cắm vào: điểm cam.", 3.0),
   ("Nối các điểm.", 3.0),
   ("Rút ra: điểm tím.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng không?", 2.4),
   ("Sai: nằm yên, i = 0.", 3.0),
   ("Chưa nói được.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự đoán.", 6.2)]),
])
