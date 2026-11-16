# Clip: tn-l12-phongxa-01 - Nhip dem cua mot nguon phong xa: trung binh on dinh, tung phut ngau nhien (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-phongxa-01.json:
#   so_lieu_mau: 5 lan dem 1 phut = 512, 486, 531, 497, 505; phong nen 23 (ghi_chu: trung binh 506,2; tru phong con 483).
#   rut_ra: mot lan dem tan mat co +-20 xung/phut, trung binh 5 lan co +-10. ket_qua_ky_vong: 486-531, khoang +-4 %.
#   tham_so: d = 10 cm, t_dem = 60 s. khong_chung_minh: 5 phut qua ngan de thay giam; chua biet tia alpha, beta hay gamma.
# Khac phongxa2 (chu ki ban ra, bay = ti so khi chua tru phong): clip nay la bay T7 "quen tru phong -> tuong nguon manh hon".
# Du doan (khung ben canh, K10 khong ve nut; nguon khong doi, dem 5 lan x 1 phut, nam so dem se the nao?):
#   A. Bang nhau, vi nguon khong doi (hien_tuong_hay_sai #1)
#   B. Giam dan deu qua 5 lan (nham "nguon yeu dan" trong 5 phut; khong_chung_minh #1)
#   C. Khac nhau, dao dong quanh mot gia tri  <- dung
# Cau chot (ca moi, khong trung Du doan): dem moi lan 4 phut (t_dem trong khoang 30-300 s cua tham_so) -> do lech tuong doi
#   NHO hon (sai so tuong doi 1/sqrt(N), sai_so_thuong_gap #1 "muon giam phai dem lau hon"); man hinh khong ghi y nay.
import random
from engine import *

COUNTS = [512, 486, 531, 497, 505]      # so_lieu_mau
PHONG, MEAN, NET = 23, 506, 483         # so_lieu_mau (phong) + ghi_chu (506,2 -> 506; 483)
NOTE = (70, 75, 95)

# ---------------- dung cu: may dem + dong ho + nguon, ong dem tren ban ----------------
SX, SY = 300, 740          # tam nguon khi dat truoc ong
TX0, TX1, TY = 500, 900, 740
BOX = (110, 790)           # hop chi tren ban (goc trai)
RP = random.Random(5)
RAYS = [(RP.random(), RP.uniform(-1, 1)) for _ in range(16)]

def source(d, x, y, a=1.0):
    d.rounded_rectangle([x - 34, y - 34, x + 34, y + 34], radius=12, fill=A(YELLOW, a), outline=A(NAVY, a), width=5)
    for k in range(3):
        g = 90 + 120 * k
        d.pieslice([x - 24, y - 24, x + 24, y + 24], g - 30, g + 30, fill=A(NAVY, a))
    dot(d, x, y, 6, A(YELLOW, a))

def stopwatch(d, cx, cy, sec, run):
    r = 92
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVY, width=6)
    d.rectangle([cx - 14, cy - r - 24, cx + 14, cy - r], fill=NAVY)
    for k in range(12):
        a = math.radians(k * 30 - 90); L = 18 if k % 3 == 0 else 9
        d.line([(cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a)),
                (cx + (r - 6 - L) * math.cos(a), cy + (r - 6 - L) * math.sin(a))], fill=NAVY, width=4)
    a = math.radians(sec / 60 * 360 - 90)
    if sec > 0: d.pieslice([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], -90, sec / 60 * 360 - 90, fill=A(ORANGE, 0.22))
    d.line([(cx, cy), (cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a))], fill=RED if run else NAVY, width=6)
    dot(d, cx, cy, 8, NAVY)

def rig(d, t, reading, sub, sec=0.0, run=False, src=0.0):
    """src: 0 = nguon truoc ong dem, 1 = nguon da cat trong hop chi."""
    # may dem
    card(d, (60, 270, 650, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    d.rounded_rectangle([110, 360, 600, 480], radius=16, fill=NAVY)
    text(d, (355, 420), str(reading), 70, (134, 239, 172))
    text(d, (355, 530), sub, 44, NOTE, bold=False)
    # dong ho bam giay
    card(d, (690, 270, 1020, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    stopwatch(d, 855, 440, sec, run)
    # ban, gia, ong dem
    d.line([(90, 900), (990, 900)], fill=NAVY, width=6)
    mx = (TX0 + TX1) / 2
    d.rectangle([mx - 8, TY + 40, mx + 8, 896], fill=GRAY); d.rectangle([mx - 70, 882, mx + 70, 898], fill=NAVY)
    d.rounded_rectangle([TX0, TY - 40, TX1, TY + 40], radius=36, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([TX0 - 6, TY - 34, TX0 + 14, TY + 34], fill=(70, 78, 100))
    text(d, (mx + 10, TY), "ống đếm", 44, NAVY)
    d.line([(TX1, TY), (960, TY), (960, 590)], fill=GRAY, width=12, joint="curve")
    # hop chi
    bx, by = BOX
    if src > 0: d.rectangle([bx - 70, by, bx + 70, 896], fill=(110, 115, 128), outline=NAVY, width=4)
    if src > 0: text(d, (bx, 950), "hộp chì", 44, NOTE, bold=False)
    # nguon: truot tu gia vao hop chi
    k = ease(src)
    x = lerp(SX, bx, k); y = lerp(SY, by + 52, k) if k < 1 else by + 52
    if k < 0.98:
        if k < 0.05: d.rectangle([x - 8, y + 34, x + 8, 896], fill=GRAY)
        source(d, x, y)
    if src <= 0:
        # khoang cach 10 cm (tham_so d)
        for xx in (SX, TX0): d.line([(xx, 640), (xx, 670)], fill=NOTE, width=4)
        arrow(d, (SX + 4, 655), (TX0 - 4, 655), NOTE, w=4, head=14); arrow(d, (TX0 - 4, 655), (SX + 4, 655), NOTE, w=4, head=14)
        text(d, ((SX + TX0) / 2, 615), "10 cm", 44, NOTE)
        text(d, (SX, 960), "nguồn", 44, NOTE, bold=False)
        if run:                                     # hat bay vao cua so ong dem (chi khi dang dem)
            for ph, dy in RAYS:
                q = (ph + t * 1.7) % 1
                dot(d, lerp(SX + 40, TX0, q), SY + dy * 30 * q, 6, ORANGE)

# ---------------- bieu do cot: truc tu 0 (nhat ky 13/11) ----------------
BX = [270, 395, 520, 645, 770, 905]
def bar_chart(d, box, vals, alphas, mean_k=0.0, hl=None, labels=True):
    x0b, y0b, x1b, y1b = box
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    yb, yt = y1b - 110, y0b + 110
    Y = lambda n: yb - n / 600 * (yb - yt)
    text(d, (x0b + 40, y0b + 50), "xung/phút", 44, NOTE, bold=False, anchor="lm")
    for n in (200, 400, 600): d.line([(200, Y(n)), (x1b - 30, Y(n))], fill=(240, 236, 228), width=2)
    d.line([(200, yb), (x1b - 30, yb)], fill=NAVY, width=5); d.line([(200, yb), (200, yt - 20)], fill=NAVY, width=5)
    for n in (0, 200, 400, 600):
        text(d, (180, Y(n)), str(n), 44, NOTE, bold=False, anchor="rm")
    labs = ["1", "2", "3", "4", "5", "phông"]
    for i, (v, a) in enumerate(zip(vals, alphas)):
        x = BX[i]
        if v is None: continue
        text(d, (x, yb + 50), labs[i], 44, PURPLE if i == 5 else NOTE, bold=i == 5)
        if a <= 0: continue
        col = PURPLE if i == 5 else (BLUE if hl is None or i in hl else (165, 190, 240))
        top = yb - (yb - Y(v)) * ease(a)
        if yb - top > 2: d.rectangle([x - 42, top, x + 42, yb], fill=A(col, 1))
        if labels: text(d, (x, top - 30), str(v), 44, INK, alpha=clamp(a * 2 - 1))
    if mean_k > 0:
        y = Y(MEAN)
        for xx in range(200, x1b - 40, 26): d.line([(xx, y), (min(xx + 14, x1b - 40), y)], fill=A(GREEN, mean_k), width=5)
    return Y

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, "?", "")
    a = appear(t, M[1] - 0.6, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 430), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 175), "Đếm 5 lần, mỗi lần 1 phút.", 48, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Năm số đếm sẽ thế nào?", 50, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 370, 940, y0 + 384], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 370, 140 + 800 * (1 - p), y0 + 384], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: dem 5 lan, roi do phong ----------------
SWEEP = 0.8
def count_at(i, sc):                       # moc bat dau lan dem i (0..4); lan 5 = phong
    M = sc["M"]
    return M[0] + 0.25 + i * 1.0 if i < 5 else M[1] + 0.9

def do_state(t, sc):
    """(so may dem, nhan, giay dong ho, dang dem, src, so cot da hien) -- mot nguon trang thai cho may dem, dong ho, cot."""
    M = sc["M"]; src = clamp((t - M[1] - 0.1) / 0.6)
    n = 0; reading, sub, sec, run = "?", "chưa đếm", 0.0, False
    for i in range(6):
        s = count_at(i, sc)
        if t < s: break
        if t < s + SWEEP:
            reading, sub, sec, run = "···", "đang đếm", 60 * (t - s) / SWEEP, True
        else:
            n = i + 1; reading = (COUNTS + [PHONG])[i]; sub = "xung/phút" if i < 5 else "phông nền"; sec, run = 60, False
    if n == 5 and t >= M[1] and t < count_at(5, sc):
        reading, sub, sec, run = COUNTS[4], "xung/phút", 60, False
    return reading, sub, sec, run, src, n

def s_do(img, d, t, sc):
    reading, sub, sec, run, src, n = do_state(t, sc)
    rig(d, t, reading, sub, sec, run, src)
    vals = COUNTS + [PHONG]
    bar_chart(d, (60, 1010, 1020, 1600), vals, [appear(t, count_at(i, sc) + SWEEP, 0.35) if i < n else 0 for i in range(6)])

# ---------------- canh 3: Dap an + rut ra (phong to quanh 506) ----------------
ZX0, ZX1, ZV0, ZV1 = 150, 930, 470, 540
def Xz(v): return ZX0 + (v - ZV0) / (ZV1 - ZV0) * (ZX1 - ZX0)

def s_ans(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.3, 0.4)
    s = "ĐÁP ÁN · khác nhau"
    pw = tw(d, s, F(42)) + 56
    card(d, (W / 2 - pw / 2, 236, W / 2 + pw / 2, 304), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 270), s, 42, WHITE, alpha=ka)
    Y = bar_chart(d, (60, 330, 1020, 930), COUNTS + [None], [1] * 5 + [0], mean_k=appear(t, 0.8, 0.5), labels=False)
    km = appear(t, 0.8, 0.5)
    if km > 0: text(d, (1000, Y(MEAN) - 34), "≈ 506", 46, GREEN, anchor="rm", alpha=km)
    # panel phong to
    kz = appear(t, 1.8, 0.45)
    if kz <= 0: return
    card(d, (60, 960, 1020, 1600), fill=A(WHITE, kz), outline=A(LIGHT, kz), w=3)
    text(d, (W / 2, 1010), "phóng to", 44, NOTE, alpha=kz)
    yl = 1170
    d.line([(ZX0 - 20, yl), (ZX1 + 20, yl)], fill=A(NAVY, kz), width=5)
    for v in (480, 500, 520, 540):
        d.line([(Xz(v), yl - 12), (Xz(v), yl + 12)], fill=A(NAVY, kz), width=4)
    for yy in range(yl - 110, yl + 20, 22):
        if yl - 82 < yy < yl - 18: continue          # chua cho chu "505"
        d.line([(Xz(MEAN), yy), (Xz(MEAN), yy + 11)], fill=A(GREEN, kz), width=4)
    up = {486: True, 497: False, 505: True, 512: False, 531: True}
    for v in COUNTS:
        dot(d, Xz(v), yl, 15, A(BLUE, kz), A(WHITE, kz))
        text(d, (Xz(v), yl - 52 if up[v] else yl + 52), str(v), 44, BLUE, alpha=kz)
    # mot lan: +-20 (rut_ra); khoang +-4 % (ket_qua_ky_vong)
    k1 = appear(t, 2.3, 0.4)
    y1 = 1300
    if k1 > 0:
        d.line([(Xz(486), y1), (Xz(526), y1)], fill=A(ORANGE, k1), width=8)
        for v in (486, 526): d.line([(Xz(v), y1 - 20), (Xz(v), y1 + 20)], fill=A(ORANGE, k1), width=6)
        text(d, (W / 2, y1 + 56), "một lần: ±20 ≈ √N (≈ 4 %)", 44, ORANGE, alpha=k1)
    # trung binh 5 lan: +-10
    k2 = appear(t, M[1] + 0.4, 0.4)
    y2 = 1460
    if k2 > 0:
        d.line([(Xz(496), y2), (Xz(516), y2)], fill=A(GREEN, k2), width=8)
        for v in (496, 516): d.line([(Xz(v), y2 - 20), (Xz(v), y2 + 20)], fill=A(GREEN, k2), width=6)
        dot(d, Xz(MEAN), y2, 15, A(GREEN, k2), A(WHITE, k2))
        text(d, (W / 2, y2 + 56), "trung bình 5 lần: ±10", 44, GREEN, alpha=k2)

# ---------------- canh 4: co che + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    M = sc["M"]
    a = appear(t, 0.2, 0.4)
    card(d, (60, 260, 1020, 760), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    # luoi hat nhan: moi khoang 0,3 s mot nhom ngau nhien loe sang (phan ra)
    rr = random.Random(int(t / 0.3))
    fire = set(rr.sample(range(36), rr.randint(2, 6)))
    for i in range(36):
        cx, cy = 165 + (i % 12) * 68, 340 + (i // 12) * 70
        dot(d, cx, cy, 20, A(ORANGE if i in fire else (226, 214, 196), a), A(NAVY, a))
    text(d, (W / 2, 600), "Số hạt nhân rã mỗi phút: ngẫu nhiên", 46, INK, alpha=a)
    text(d, (W / 2, 680), "Trung bình: đặc trưng cho nguồn", 46, BLUE, alpha=appear(t, 0.9, 0.4))
    b = appear(t, M[1] - 0.1, 0.4)
    if b <= 0: return
    card(d, (60, 810, 1020, 1180), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 875), "Chưa nói được gì?", 48, PURPLE, alpha=b)
    text(d, (120, 990), "• Nguồn có yếu dần?", 46, INK, anchor="lm", alpha=b)
    b2 = appear(t, M[1] + 1.4, 0.4)
    text(d, (120, 1100), "• Tia α, β hay γ?", 46, INK, anchor="lm", alpha=b2)

# ---------------- canh 5: bay quen tru phong (T7: sai so co chieu) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    a1 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 520), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, 276, W / 2 + pw / 2, 340), fill=A(RED, a1), r=32)
    text(d, (W / 2, 308), "BẪY", 40, WHITE, alpha=a1)
    q = "“Nguồn cho 506 xung/phút”"
    ks = clamp((t - mk) / 0.4); f = F(48); lw = tw(d, q, f); yy = 440
    text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    # cot chong: 483 nguon + 23 phong = 506 do duoc; truc tu 0
    kb = appear(t, mk - 0.9, 0.45)
    if kb > 0:
        card(d, (40, 560, 1040, 1180), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        yb, yt = 1110, 660; Y = lambda n: yb - n / 600 * (yb - yt)
        d.line([(200, yb), (900, yb)], fill=A(NAVY, kb), width=5); d.line([(200, yb), (200, yt - 20)], fill=A(NAVY, kb), width=5)
        for n in (0, 200, 400, 600): text(d, (180, Y(n)), str(n), 44, NOTE, bold=False, anchor="rm", alpha=kb)
        x = 360
        d.rectangle([x - 70, Y(NET), x + 70, yb], fill=A(GREEN, kb))
        d.rectangle([x - 70, Y(MEAN), x + 70, Y(NET)], fill=A(PURPLE, kb))
        text(d, (x, Y(MEAN) - 34), f"đo được {MEAN}", 44, INK, alpha=kb)
        d.line([(x + 76, (Y(MEAN) + Y(NET)) / 2), (520, 760)], fill=A(PURPLE, kb), width=4)
        text(d, (530, 760), f"phông {PHONG}", 46, PURPLE, anchor="lm", alpha=kb)
        text(d, (x + 100, Y(NET / 2)), f"nguồn {NET}", 48, GREEN, anchor="lm", alpha=kb)
    kv = appear(t, M[1] + 1.6, 0.45)
    if kv > 0:
        card(d, (40, 1220, 1040, 1560), fill=A((254, 242, 242), kv), outline=A(RED, kv), w=4)
        text(d, (W / 2, 1310), "Quên trừ → kết quả lớn hơn thật", 48, RED, alpha=kv)
        text(d, (W / 2, 1460), "Cách giảm: đo phông rồi trừ", 46, GREEN, alpha=appear(t, M[1] + 2.8, 0.4))

# ---------------- canh 6: chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    for cx, lab in ((380, "1 phút"), (700, "4 phút")):
        r = 70
        d.ellipse([cx - r, 1070 - r, cx + r, 1070 + r], fill=A(WHITE, k), outline=A(NAVY, k), width=5)
        ang = 360 if lab == "4 phút" else 90
        d.pieslice([cx - r + 8, 1070 - r + 8, cx + r - 8, 1070 + r - 8], -90, -90 + ang, fill=A(ORANGE, 0.3 * k))
        text(d, (cx, 1185), lab, 44, NOTE, alpha=k)
    arrow(d, (470, 1070), (610, 1070), A(GRAY, k), w=6, head=18)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Từng phút: ngẫu nhiên\nTrung bình: ổn định",
             "Đếm 4 phút mỗi lần: độ lệch (%) nhỏ hơn hay lớn hơn 4 %?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1360, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1450, "√N, với N ≈ 2000", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, wy, b, e = sc["hook"], sc["do"], sc["ans"], sc["why"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for i in range(6):
        s = count_at(i, do); x = s
        while x < s + SWEEP: out.append((do["t0"] + x, "tick")); x += 0.2
        out.append((do["t0"] + s + SWEEP, "tap"))
    out += [(an["t0"] + 0.3, "ding"), (wy["t0"] + wy["M"][1] - 0.1, "tap"),
            (b["t0"] + b["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-phongxa-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Hiện tượng phóng xạ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đếm xung từng phút", draw=s_hook, tail=0.3, caps=[
   ("Nguồn cách ống 10 cm.", 2.9),
   ("Chọn đáp án ở khung câu hỏi.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đếm 1 phút, ghi số; 5 lần.", 5.4),
   ("Cất nguồn, đếm phông nền.", 2.9)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.5, caps=[
   ("Năm số khác nhau, quanh 506.", 3.0),
   ("Trung bình 5 lần ít lệch hơn.", 4.3)]),
 dict(key="why", title="Rút ra", draw=s_why, tail=0.4, caps=[
   ("Vì sao?", 2.6),
   ("Chưa trả lời được.", 4.0)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.4, caps=[
   ("Đúng hay sai?", 2.5),
   ("Sai: 506 còn lẫn phông 23.", 5.7)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng video và trả lời.", 5.6)]),
])
