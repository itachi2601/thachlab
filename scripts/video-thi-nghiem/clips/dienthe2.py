# Clip: tn-l11-dien-the-02 - Von ke chi do hieu dien the: pin 1,5 V va day dan (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-the-02.json:
#   so_lieu_mau (lan, que do, que den, U): 1 cuc+ cuc- 1,5 ; 2 cuc- cuc+ -1,5 ; 3 day diem1 day diem2 0,00
#   tham_so: E_pin 1,5 V (dieu chinh 1,2-9 V). mo_hinh: pin ho mach, von ke dien tro rat lon -> khong co dong.
#   hien_tuong_hay_sai (kho khong co sai_so_thuong_gap): von ke do dien the MOT diem; day noi cuc + co U = 1,5 V.
#   Cau hoi chot: pin 9 V (max tham_so, chua tung hien), que do o cuc (-) -> -9 V.
# Canh: Du doan (K10: chi cau hoi + hinh, que tren day dong) -> Tien hanh 3 lan (bang) + "Dap an · 0,00 V" ->
#       Rut ra (so chi = V_do - V_den, doi dau, cung day U ~ 0) -> Bay (von ke do V mot diem) roi Chua noi duoc ->
#       Chot + cau hoi tu nho lai.
# Mach: pin de ho, day dong chi noi vao cuc (+), dau kia tu do -> KHONG ve chieu dong. Que do cam o jack V, que den o COM.
from engine import *

ROWS = [(1, "cực (+)", "cực (−)", "1,5"), (2, "cực (−)", "cực (+)", "−1,5"), (3, "dây, điểm 1", "dây, điểm 2", "0,00")]
READ = ["1,5 V", "−1,5 V", "0,00 V"]
BODY = (70, 78, 100); METAL = (170, 175, 185); COPPER = (200, 120, 62); DCOP = (140, 70, 25)
BLACKP = (30, 30, 36); DRED = (185, 28, 28)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
MINUS = (194, 522); PLUS = (575, 497); W1 = (740, 478); W2 = (920, 478)   # dau kim cham (tu duoi len)
POS = [(PLUS, MINUS), (MINUS, PLUS), (W1, W2)]                             # (que do, que den) moi lan
JR, JB = (640, 850), (440, 850)                                             # jack V (do) va COM (den) tren von ke

def battery(d, labels=True):
    d.rounded_rectangle([200, 400, 560, 544], radius=18, fill=BODY, outline=NAVY, width=3)
    d.rectangle([186, 418, 200, 526], fill=METAL)                            # mat cuc am phang
    d.rounded_rectangle([560, 446, 592, 498], radius=6, fill=METAL, outline=NAVY, width=2)   # num cuc duong
    text(d, (380, 472), "1,5 V", 44, WHITE)
    text(d, (232, 470), "−", 56, WHITE); text(d, (530, 470), "+", 52, WHITE)
    # day dong noi cuc (+), dau kia de tu do
    d.line([(592, 472), (990, 472)], fill=COPPER, width=12)
    dot(d, 992, 472, 9, DCOP)
    if labels:
        text(d, (840, 372), "dây đồng", 40, DCOP)
        text(d, (W1[0], 430), "1", 40, DCOP); text(d, (W2[0], 430), "2", 40, DCOP)

def probe(d, tip, col, yc):
    x, y = tip
    d.line([(x, y), (x, y + 44)], fill=(90, 92, 100), width=6)                # kim
    d.line([(x, y + 44), (x, y + 200)], fill=col, width=26)                   # tay cam
    jx = JR[0] if col == RED else JB[0]
    d.line([(x, y + 200), (x, yc), (jx, yc), (jx, JR[1])], fill=col, width=6, joint="curve")

def meter(d, reading):
    card(d, (300, 826, 750, 1066), fill=BODY, r=22)
    card(d, (360, 886, 720, 980), fill=(220, 240, 225), r=12)
    text(d, (540, 933), reading, 56, (20, 60, 30))
    text(d, (540, 1026), "vôn kế số", 38, WHITE)
    dot(d, JB[0], JB[1], 12, BLACKP, outline=WHITE); dot(d, JR[0], JR[1], 12, RED, outline=WHITE)
    text(d, (JB[0] - 22, JB[1]), "COM", 36, WHITE, anchor="rm"); text(d, (JR[0] + 22, JR[1]), "V", 36, (255, 170, 170), anchor="lm")

def setup(d, rtip, btip, reading="– – –", labels=True):
    battery(d, labels)
    probe(d, btip, BLACKP, 800)
    probe(d, rtip, RED, 772)
    meter(d, reading)

def table(d, n, y=1135, hl=(), ka=1.0):
    card(d, (40, y, 1040, y + 330), fill=WHITE, outline=NAVY, w=4)
    xs = (120, 340, 640, 920)
    for xx, c in zip(xs, ("Lần", "Que đỏ", "Que đen", "U (V)")): text(d, (xx, y + 48), c, 38, INK)
    d.line([(70, y + 86), (1010, y + 86)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 132 + i * 66; k, r, b, u = ROWS[i]
        if i in hl: d.rounded_rectangle([58, yy - 31, 1022, yy + 31], radius=16, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), str(k), 40, INK); text(d, (xs[1], yy), r, 38, RED)
        text(d, (xs[2], yy), b, 38, NAVY); text(d, (xs[3], yy), u, 42, BLUE)

Q_AT = 1.4   # hop Du doan hien som: ~8,8 s im lang truoc ding (T - 0,6)
# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    setup(d, W1, W2, "?")
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 1120 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 230, "Hai que chạm hai điểm trên\ndây đồng nối cực (+).\nVôn kế chỉ bao nhiêu?", 48, INK, maxw=900, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 404, 940, y0 + 416], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 404, 140 + 800 * (1 - p), y0 + 416], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan trong MOT canh) ----------------
def steps(sc):   # (luc bat dau truot toi vi tri k, luc hien so chi)
    M = sc["M"]
    return [(None, 0.9), (3.2, 3.9), (M[1] + 0.4, M[1] + 1.1)]

def chips(d, cur, done):
    for j, s in enumerate(("1. Đỏ ở (+)", "2. Đổi que", "3. Trên dây")):
        x0 = 60 + j * 330; box = (x0, 236, x0 + 300, 302)
        if j == cur: card(d, box, fill=ORANGE, r=33); text(d, (x0 + 150, 269), s, 36, WHITE)
        elif j < done: card(d, box, fill=LIGHT, r=33); text(d, (x0 + 150, 269), s, 36, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=33, w=3); text(d, (x0 + 150, 269), s, 36, GRAY)

ANS_DL = 0.3
def s_do(img, d, t, sc):
    st = steps(sc); k = 0
    for j, (mv, rd) in enumerate(st):
        if mv is not None and t >= mv: k = j
    mv, rd = st[k]
    if mv is not None and t < mv + 0.6:                       # dang nhac que sang vi tri moi
        u = ease((t - mv) / 0.6); (r0, b0), (r1, b1) = POS[k - 1], POS[k]
        lift = 60 * math.sin(math.pi * u)
        rt = (lerp(r0[0], r1[0], u), lerp(r0[1], r1[1], u) + lift); bt = (lerp(b0[0], b1[0], u), lerp(b0[1], b1[1], u) + lift)
        shown = False
    else:
        rt, bt = POS[k]; shown = t >= rd
    n = k + (1 if shown else 0)
    chips(d, k, n)
    setup(d, rt, bt, READ[k] if shown else "– – –")
    table(d, n, hl=(k,) if shown else ())
    ka = appear(t, st[2][1] + ANS_DL, 0.12)
    if ka > 0 and k == 2:                                     # huy hieu dap an to, ben phai von ke
        card(d, (770, 846, 1050, 1046), fill=A((21, 110, 52), ka), outline=A(WHITE, ka), r=28, w=4)
        text(d, (910, 905), "ĐÁP ÁN", 46, WHITE, alpha=ka)
        text(d, (910, 985), "0,00 V", 52, WHITE, alpha=ka)
    if k == 2 and shown:
        text(d, (380, 342), "Pin hở: không có dòng chạy", 40, INK, bold=False)

# ---------------- canh 3: Rut ra ----------------
def kcard(d, y, title, color, k, h=220):
    if k <= 0: return
    yy = y + (1 - k) * 30
    card(d, (60, yy, 1020, yy + h), fill=A(WHITE, k), outline=A(color, k), w=6)
    rich(d, W / 2, yy + h / 2, title, 60, color, alpha=k)

def s_rut(img, d, t, sc):
    M = sc["M"]
    k1, k2, k3 = appear(t, 0.3, 0.45), appear(t, M[0] + 0.1, 0.45), appear(t, M[1] + 0.1, 0.45)
    kcard(d, 360, "Số chỉ = V_{đỏ} − V_{đen}", GREEN, k1)
    kcard(d, 700, "U_{NM} = −U_{MN}", ORANGE, k2)
    kcard(d, 1040, "Cùng một dây dẫn: U ≈ 0", PURPLE, k3)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    setup(d, PLUS, MINUS, "1,5 V", labels=False)
    if a1 > 0:
        y0 = 1120
        card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "Cực (+) có điện thế 1,5 V"
        ks = clamp((t - 1.2) / 0.4); f = F(46); lw = tw(d, q, f); yy = y0 + 190
        text(d, (W / 2, yy), q, 46, DRED, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=4)
        ka = a1 * appear(t, 1.7, 0.5)
        text(d, (W / 2, y0 + 300), "✓ Chỉ biết hiệu:", 46, (10, 80, 40), alpha=ka)
        text(d, (W / 2, y0 + 375), "V cực (+) − V cực (−) = 1,5 V", 46, (10, 80, 40), alpha=ka)
    if k2 > 0:
        y0 = 1120 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        ctext(d, y0 + 250, "Dây có dòng lớn chạy qua,\nU còn bằng 0?", 48, INK, maxw=900, alpha=k2 * appear(t, M[1] + 0.3, 0.4))

# ---------------- canh 5: Chot + cau hoi tu nho lai (hop gon, goi y tre ~2,5 s) ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: pin 9 V, que do o cuc (-), que den o cuc (+) -> -9 V."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 430, 1020, 690), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 560, "Vôn kế đo hiệu điện thế\ngiữa hai điểm", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 750, 1040, 1410), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 780, W / 2 + pw / 2, 844), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 812), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 990, "Pin 9 V. Que đỏ chạm cực (−),\nque đen chạm cực (+).\nVôn kế chỉ bao nhiêu?", 48, INK, maxw=920,
          alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1160, 970, 1370), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1210, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    rich(d, W / 2, 1295, "Số chỉ = V_{đỏ} − V_{đen}", 60, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    st = steps(do)
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + rd, "tick") for _, rd in st[:2]]
    out += [(do["t0"] + st[2][1] + ANS_DL, "ding"), (r["t0"] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-dien-the-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện thế · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vôn kế và dây đồng", draw=s_hook, tail=0.8, caps=[
   ("Pin 1,5 V để hở, vôn kế số.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.2, caps=[
   ("Lần 1 và 2: que chạm hai cực.", 5.4),
   ("Lần 3: hai que trên dây đồng.", 4.4)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.8, caps=[
   ("Đổi que là đổi thứ tự hai điểm.", 4.0),
   ("Mọi điểm trên dây cùng điện thế.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 3.6),
   ("Giới hạn.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
