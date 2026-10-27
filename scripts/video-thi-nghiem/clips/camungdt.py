# Clip: tn-l12-camungdt-01 - Nam cham va cuon day noi dien ke (ban 2, 27/10/2026)
# So lieu lay tu content/thi-nghiem/tn-l12-camungdt-01.json -> so_lieu_mau:
#   dung yen 0,0 -> 0 ; dua vao 0,1 -> +1,0 ; dua vao 0,2 -> +2,1 ; dua vao 0,4 -> +3,9 ; rut ra 0,2 -> -2,0 (mA)
# Ban 3 (27/10/2026): thanh dem o hop Du doan, lo dap an B ngay luc nam yen, canh chot + cau hoi doi cuc S, tieng bao.
from engine import *

# ---------------- bo cuc (toa do khung 1080x1920) ----------------
CX, CY, CR = 640, 520, 118            # tam cuon day, nua chieu cao vong day
NT, CSPAN = 10, 300                   # so vong ve, be dai cuon
CL, CRR = CX - CSPAN // 2, CX + CSPAN // 2
ML, MH = 300, 84                      # be dai, be day nam cham
OUT_TIP, IN_TIP = 400, 700            # vi tri dau cuc N: ngoai cuon / trong cuon
GX, GY, GR = 540, 1196, 300           # tam quay kim dien ke, ban kinh mat so
GMAX, GANG = 5.0, 56                  # thang do +-5 mA, kim lech toi da 56 do
TL, TR = (CL, 800), (CRR, 800)        # hai cuc dien ke (tren mep the)
TAB_Y = 1318                          # bang so lieu / hop du doan

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
    text(d, (CX, 334), "600 vòng", 36, MUTED, bold=False)


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


def field(d, tip, alpha):
    """Duong suc ngoai nam cham: ra o N (phai), vao o S (trai). Net dut, mui chevron."""
    if alpha <= 0: return
    c = A(PURPLE, 0.55 * alpha); xs = tip - ML
    for k, h in ((1, 92), (2, 150)):
        box = [xs - 34 * k, CY - h, tip + 34 * k, CY + h]
        dashed_ellipse(d, box, 180, 360, c)      # nua tren
        dashed_ellipse(d, box, 0, 180, c)        # nua duoi
        mx = (box[0] + box[2]) / 2
        chevron(d, mx, CY - h, math.pi, c)       # tren: chay tu N sang S (sang trai)
        chevron(d, mx, CY + h, math.pi, c)
    # duong truc tu cuc N di ra
    d.line([(tip + 6, CY), (tip + 120, CY)], fill=c, width=4)
    chevron(d, tip + 120, CY, 0, c)


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
    text(d, (x0 + ML / 4, CY + 1), "S", 50, WHITE, alpha=alpha)
    text(d, (tip - ML / 4, CY + 1), "N", 50, WHITE, alpha=alpha)


def wires(d):
    l0 = (CL, CY + CR - 4); r0 = (CRR, CY + CR - 4)
    d.line([l0, TL], fill=NAVY, width=5); d.line([r0, TR], fill=NAVY, width=5)
    for p in (TL, TR): dot(d, p[0], p[1], 11, NAVY)


def needle_xy(i, r):
    a = math.radians(clamp(i / GMAX, -1.08, 1.08) * GANG)
    return GX + r * math.sin(a), GY - r * math.cos(a)


def galvo(d, i, ghost=None):
    card(d, (170, 812, 910, 1240), fill=WHITE, outline=NAVY, r=30, w=5)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 270 - GANG - 3, 270 + GANG + 3, fill=NAVY, width=5)
    for v in range(-5, 6):
        a = math.radians(v / GMAX * GANG); big = v % 2 == 0
        r0 = GR - (30 if big else 18)
        d.line([(GX + r0 * math.sin(a), GY - r0 * math.cos(a)), (GX + GR * math.sin(a), GY - GR * math.cos(a))],
               fill=NAVY, width=5 if big else 3)
        if big:
            lx, ly = GX + (GR + 30) * math.sin(a), GY - (GR + 30) * math.cos(a)
            text(d, (lx, ly), str(v).replace("-", "−"), 36, NAVY)
    text(d, (880, 1212), "mA", 34, MUTED, bold=False, anchor="rm")
    if ghost is not None and abs(ghost) > 0.05 and abs(ghost - i) > 0.1:
        d.line([(GX, GY), needle_xy(ghost, GR - 8)], fill=A(GRAY, 0.8), width=5)
    d.line([(GX, GY), needle_xy(i, GR - 8)], fill=RED, width=9)
    dot(d, GX, GY, 16, NAVY)
    col = RED if i > 0.05 else (BLUE if i < -0.05 else MUTED)
    text(d, (GX, 1278), f"i = {fmt(i)} mA", 56, col)


def vlabel(d, s, alpha=1.0):
    if s: text(d, (250, 690), s, 42, BLUE, alpha=alpha)


def apparatus(d, tip, i, ghost=None, malpha=1.0, vtxt="", field_on=True):
    if field_on: field(d, tip, malpha)
    coil_back(d)
    magnet(d, tip, malpha)
    coil_front(d)
    wires(d)
    galvo(d, i, ghost)
    vlabel(d, vtxt)


# ---------------- canh 1: mo dau + Du doan ----------------
def s_hook(img, d, t, sc):
    apparatus(d, OUT_TIP, 0.0)
    k = appear(t, sc["M"][0] + 1.0, 0.5)
    if k > 0:
        text(d, (905, CY - 22), "không", 36, MUTED, bold=False, alpha=k)
        text(d, (905, CY + 22), "có pin", 36, MUTED, bold=False, alpha=k)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    if k <= 0: return
    y0 = TAB_Y + (1 - k) * 40
    card(d, (60, y0, 1020, y0 + 350), fill=A(WHITE, k), outline=A(PURPLE, k), w=5)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))   # thanh dem thoi gian nghi
    d.rounded_rectangle([140, y0 + 330, 940, y0 + 340], radius=6, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, y0 + 330, 140 + 800 * (1 - q), y0 + 340], radius=6, fill=A(PURPLE, k))
    text(d, (W / 2, y0 + 40), "Dự đoán", 40, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 92), "Nam châm nằm YÊN trong cuộn dây,", 38, INK, alpha=k)
    text(d, (W / 2, y0 + 138), "kim điện kế sẽ…", 38, INK, alpha=k)
    for j, s in enumerate(("A.  lệch, đứng yên ở một vạch", "B.  chỉ đúng số 0", "C.  lệch qua lại liên tục")):
        yy = y0 + 196 + j * 52
        d.rounded_rectangle([110, yy - 22, 970, yy + 22], radius=22, outline=A(LIGHT, k), width=3)
        text(d, (140, yy), s, 36, NAVY, bold=False, anchor="lm", alpha=k)


# ---------------- canh 2: tien hanh ----------------
# (chi so phu de, tre sau phu de, thoi gian chuyen dong, dau N tu, toi, dong mA, nhan v)
PH = [(0, 0.8, 0.75, OUT_TIP, IN_TIP, 3.9, "v = 0,4 m/s →"),
      (1, 0.9, 3.0, OUT_TIP, IN_TIP, 1.0, "v = 0,1 m/s →"),
      (2, 0.0, 0.0, IN_TIP, IN_TIP, 0.0, "v = 0"),
      (3, 0.7, 1.5, IN_TIP, OUT_TIP, -2.0, "← v = 0,2 m/s")]


def do_state(t, sc):
    tip, i, ghost, malpha, vt, done = OUT_TIP, 0.0, None, 1.0, "", 0
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
            vt = lab; done = n + (1 if t > m + 1.2 else 0); continue
        if t >= t0:
            tip = lerp(xa, xb, clamp((t - t0) / dur))
            i = im * ease((t - t0) / 0.14) * (1 - ease((t - t1) / 0.16))
            if t <= t1 + 0.05: vt = lab
            if t > t1 + 0.1: ghost = im; done = n + 1
            else: done = n
        else: done = n
    return tip, i, ghost, malpha, vt, done


def chips(d, cur, done):
    names = ("1. Nhanh", "2. Chậm", "3. Nằm yên", "4. Rút ra")
    for j, s in enumerate(names):
        x0 = 60 + j * 245; box = (x0, 236, x0 + 225, 302)
        if j == cur: card(d, box, fill=ORANGE, r=33); text(d, (x0 + 112, 269), s, 32, WHITE)
        elif j < done: card(d, box, fill=LIGHT, r=33); text(d, (x0 + 112, 269), s, 32, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=33, w=3); text(d, (x0 + 112, 269), s, 32, GRAY)


def table(d, nrows, hl=-1, y=TAB_Y, alpha=1.0):
    card(d, (60, y, 1020, y + 288), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, s, an in ((110, "Cách làm", "lm"), (600, "v (m/s)", "mm"), (860, "Số chỉ (mA)", "mm")):
        text(d, (x, y + 38), s, 32, MUTED, bold=False, anchor=an, alpha=alpha)
    d.line([(100, y + 66), (980, y + 66)], fill=A(LIGHT, alpha), width=3)
    for j, (nm, v, im) in enumerate(ROWS[:nrows]):
        yy = y + 100 + j * 52
        if j == hl: d.rounded_rectangle([84, yy - 24, 996, yy + 24], radius=14, fill=A(mix(ORANGE, WHITE, 0.85), alpha))
        col = RED if im > 0 else (BLUE if im < 0 else MUTED)
        text(d, (110, yy), nm, 38, INK, anchor="lm", alpha=alpha)
        text(d, (600, yy), fmt(v, sign=False) if v else "0", 38, INK, alpha=alpha)
        text(d, (860, yy), fmt(im), 40, col, alpha=alpha)


def s_do(img, d, t, sc):
    tip, i, ghost, malpha, vt, done = do_state(t, sc)
    cur = cur_cap(sc, t)
    chips(d, cur, done)
    apparatus(d, tip, i, ghost, malpha, vt)
    table(d, done, hl=done - 1 if done > 0 and (cur == done - 1) else -1)
    ka = appear(t, sc["M"][2] + 1.0, 0.4) * (1 - appear(t, sc["M"][3] - 0.1, 0.3))   # lo dap an luc nam yen, tat khi rut ra
    if ka > 0:
        pw = tw(d, "ĐÁP ÁN B", F(32)) + 44
        card(d, (880 - pw, 828, 880, 882), fill=A(GREEN, ka), r=27)
        text(d, (880 - pw / 2, 855), "ĐÁP ÁN B", 32, WHITE, alpha=ka)


# ---------------- canh 3: rut ra ----------------
def chart(d, t, sc):
    card(d, (60, 236, 1020, 790), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 280), "Số chỉ điện kế theo tốc độ v", 36, MUTED)
    ox, oy, sx, sy = 190, 570, 1700, 56          # px/(m/s), px/mA
    d.line([(ox, 330), (ox, 730)], fill=NAVY, width=4)
    d.line([(ox, oy), (ox + 0.45 * sx, oy)], fill=NAVY, width=4)
    chevron(d, ox, 330, -math.pi / 2, NAVY, s=16); chevron(d, ox + 0.45 * sx, oy, 0, NAVY, s=16)
    text(d, (ox + 22, 336), "i (mA)", 32, MUTED, bold=False, anchor="lm")
    text(d, (ox + 0.45 * sx, oy + 34), "v (m/s)", 32, MUTED, bold=False, anchor="rm")
    for v in (0.1, 0.2, 0.3):
        x = ox + v * sx; d.line([(x, oy - 8), (x, oy + 8)], fill=NAVY, width=3)
        text(d, (x, oy + 34), fmt(v, sign=False), 32, MUTED, bold=False)
    for im in (-2, 2, 4):
        y = oy - im * sy; d.line([(ox - 8, y), (ox + 8, y)], fill=NAVY, width=3)
        text(d, (ox - 18, y), str(im).replace("-", "−"), 32, MUTED, bold=False, anchor="rm")
    k0 = appear(t, sc["M"][1] - 0.1, 0.8)
    if k0 > 0:  # duong qua goc toa do
        x1 = lerp(0, 0.43, k0)
        d.line([(ox, oy), (ox + x1 * sx, oy - x1 * 9.75 * sy)], fill=A(ORANGE, 0.45), width=4)
    pts = [(0.0, 0.0, 0), (0.1, 1.0, 1), (0.2, 2.1, 1), (0.4, 3.9, 1)]
    for j, (v, im, cap) in enumerate(pts):
        k = appear(t, sc["M"][0] + 0.2 + 0.25 * j, 0.35)
        if k <= 0: continue
        x, y = ox + v * sx, oy - im * sy
        dot(d, x, y, 13 * k, ORANGE, outline=WHITE)
        if v == 0.4: text(d, (x + 22, y), fmt(im), 32, ORANGE, anchor="lm", alpha=k)
        elif v: text(d, (x - 16, y - 30), fmt(im), 32, ORANGE, anchor="rm", alpha=k)
    k = appear(t, sc["M"][2] + 0.1, 0.45)
    if k > 0:
        x, y = ox + 0.2 * sx, oy + 2.0 * sy
        dot(d, x, y, 13 * k, PURPLE, outline=WHITE)
        text(d, (x + 26, y), "−2,0 (rút ra)", 32, PURPLE, anchor="lm", alpha=k)
        text(d, (x + 26, oy - 2.1 * sy + 6), "(cắm vào)", 32, ORANGE, bold=False, anchor="lm", alpha=k)
    text(d, (W / 2, 762), "Số liệu minh hoạ, có thêm lần cắm vào 0,2 m/s", 32, MUTED, bold=False,
         alpha=appear(t, sc["M"][0] + 1.0, 0.4))


def kcard(d, y, title, ev, color, k, h=200):
    if k <= 0: return
    yy = y + (1 - k) * 30
    card(d, (60, yy, 1020, yy + h), fill=A(WHITE, k), outline=A(color, k), w=5)
    f = F(44); ls = wrap(d, title, f, 880)
    for j, l in enumerate(ls):
        text(d, (W / 2, yy + 52 + j * 54), l, 44, color, alpha=k)
    text(d, (W / 2, yy + h - 38), ev, 34, MUTED, bold=False, alpha=k)


def s_rut(img, d, t, sc):
    chart(d, t, sc)
    kcard(d, 830, "Chỉ khi từ thông qua cuộn BIẾN THIÊN mới có dòng", "nằm yên: 0 mA", GREEN, appear(t, sc["M"][0], 0.45))
    kcard(d, 1060, "Biến thiên càng nhanh, dòng càng lớn", "0,1 m/s → 1,0 mA · 0,4 m/s → 3,9 mA", ORANGE,
          appear(t, sc["M"][1], 0.45), h=170)
    kcard(d, 1260, "Rút ra (từ thông giảm): dòng đổi chiều", "cùng 0,2 m/s: vào +2,1 · ra −2,0 mA", PURPLE,
          appear(t, sc["M"][2], 0.45), h=170)


# ---------------- canh 4: cai bay + gioi han ----------------
def s_bay(img, d, t, sc):
    apparatus(d, IN_TIP, 0.0, vtxt="v = 0")
    k1 = appear(t, 0.3, 0.45); k2 = appear(t, sc["M"][1] - 0.1, 0.45)
    a1 = k1 * (1 - k2)
    if a1 > 0:
        y = TAB_Y + (1 - k1) * 30
        card(d, (60, y, 1020, y + 288), fill=A(WHITE, a1), outline=A(RED, a1), w=5)
        text(d, (W / 2, y + 44), "Cái bẫy", 42, RED, alpha=a1)
        text(d, (W / 2, y + 104), "Nam châm nằm yên trong cuộn:", 38, INK, alpha=a1)
        text(d, (W / 2, y + 152), "từ trường MẠNH, nhưng i = 0.", 38, INK, alpha=a1)
        text(d, (W / 2, y + 222), "Cần từ thông BIẾN THIÊN, không chỉ từ trường", 34, GREEN, alpha=a1)
    if k2 > 0:
        y = TAB_Y + (1 - k2) * 30
        card(d, (60, y, 1020, y + 288), fill=A(WHITE, k2), outline=A(NAVY, k2), w=5)
        text(d, (W / 2, y + 44), "Thí nghiệm chưa nói được", 40, NAVY, alpha=k2)
        for j, s in enumerate(("• Quy tắc tìm chiều dòng (định luật Lenz).",
                               "• Số liệu ở đây là minh hoạ,",
                               "  chưa phải số đo thật.")):
            text(d, (100, y + 108 + j * 54), s, 38, INK, bold=False, anchor="lm", alpha=k2)
    # nhac lai: tu truong van con
    k = appear(t, 0.9, 0.5)
    if k > 0 and a1 > 0:
        text(d, (905, CY - 80), "từ trường", 30, PURPLE, bold=False, alpha=k * a1)
        text(d, (905, CY - 44), "vẫn còn", 30, PURPLE, bold=False, alpha=k * a1)


# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Từ thông biến thiên → có dòng cảm ứng",
             "Đổi sang cực S, cắm vào nhanh như lần 1. Kim lệch khoảng bao nhiêu, về phía nào?",
             "Cực N: cắm vào +3,9 · rút ra −2,0 mA\nCực S: từ trường ngược chiều cực N")

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][2] + 1.0, "ding"), (r["t0"] + r["M"][0], "tap"),
            (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-camungdt-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Cuộn dây không có pin", draw=s_hook, tail=0.5, caps=[
   ("Cuộn dây 600 vòng nối điện kế, không pin.", 3.0),
   ("Dự đoán trước, rồi xem tiếp.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Cắm nhanh cực N vào cuộn dây.", 3.0),
   ("Cắm chậm hơn.", 4.4),
   ("Nằm yên trong cuộn: kim về 0, đáp án B.", 3.0),
   ("Rút nam châm ra.", 3.0)]),
 dict(key="rut", title="Kết luận", draw=s_rut, tail=0.9, caps=[
   ("Có dòng chỉ khi từ thông biến thiên.", 3.0),
   ("Nhanh gấp 4 lần, dòng lớn gần gấp 4.", 3.2),
   ("Rút ra thì dòng đổi chiều.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: nằm yên trong cuộn vẫn KHÔNG có dòng.", 3.2),
   ("Thí nghiệm này chưa nói được gì?", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Thử nghĩ: đổi sang cực S thì kim ra sao?", 4.6)]),
])
