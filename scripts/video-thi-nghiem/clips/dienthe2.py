# Clip: tn-l11-dien-the-02 - Von ke chi do hieu dien the: pin 1,5 V va day dan (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-the-02.json:
#   so_lieu_mau (lan, que do, que den, U): 1 cuc+ cuc- 1,5 ; 2 cuc- cuc+ -1,5 ; 3 day diem1 day diem2 0,00
#   tham_so: E_pin 1,5 V (dieu chinh 1,2-9 V). mo_hinh: pin ho mach, von ke dien tro rat lon -> khong co dong.
#   hien_tuong_hay_sai (kho khong co sai_so_thuong_gap): von ke do dien the MOT diem; day noi cuc + co U = 1,5 V.
#   Cau chot (cong B v1, o khung, khong hien): hai pin 1,5 V noi tiep bang day dong (+ pin trai -> - pin phai); que do
#     cham (+) pin phai, que den cham (-) pin trai -> 1,5 + 0 + 1,5 = 3,0 V (buoc moi: day giua hai pin la MOT dien the,
#     moi pin them 1,5 V; so 3,0 khong co trong bang).
# Canh: Du doan (K10: chi cau hoi + hinh, que tren day dong) -> Tien hanh 3 lan (bang) + "Dap an · 0,00 V" ->
#       Rut ra (so chi = V_do - V_den, doi dau, cung day U ~ 0) -> Bay (von ke do V mot diem) roi Chua noi duoc ->
#       Chot + cau hoi tu nho lai.
# Mach: pin de ho, day dong chi noi vao cuc (+), dau kia tu do -> KHONG ve chieu dong. Que do cam o jack V, que den o COM.
from engine import *

ROWS = [(1, "cực (+)", "cực (−)", "1,5"), (2, "cực (−)", "cực (+)", "−1,5"), (3, "dây 1", "dây 2", "0,00")]
READ = ["1,5 V", "−1,5 V", "0,00 V"]
BODY = (70, 78, 100); METAL = (170, 175, 185); COPPER = (200, 120, 62); DCOP = (140, 70, 25)
BLACKP = (30, 30, 36); DRED = (185, 28, 28); DGREEN = (21, 110, 55)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
MINUS = (194, 522); PLUS = (575, 497); W1 = (740, 478); W2 = (920, 478)   # dau kim cham (tu duoi len)
POS = [(PLUS, MINUS), (MINUS, PLUS), (W1, W2)]                             # (que do, que den) moi lan
JR, JB = (660, 850), (420, 850)                                             # jack V (do) va COM (den) tren von ke

def pill(d, s, y, a, color=NAVY, size=58, cx=W / 2):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A((148, 140, 128), a), r=18, w=4)

def battery(d, la=1.0):
    d.rounded_rectangle([200, 400, 560, 544], radius=18, fill=BODY, outline=NAVY, width=3)
    d.rectangle([186, 418, 200, 526], fill=METAL)                            # mat cuc am phang
    d.rounded_rectangle([560, 446, 592, 498], radius=6, fill=METAL, outline=NAVY, width=2)   # num cuc duong
    text(d, (380, 472), "1,5 V", 56, WHITE)
    text(d, (240, 470), "−", 60, WHITE); text(d, (528, 470), "+", 56, WHITE)
    # day dong noi cuc (+), dau kia de tu do
    d.line([(592, 472), (990, 472)], fill=COPPER, width=12)
    dot(d, 992, 472, 9, DCOP)
    if la > 0:
        text(d, (800, 368), "dây đồng", 56, DCOP, alpha=la)
        text(d, (W1[0], 424), "1", 56, DCOP, alpha=la); text(d, (W2[0], 424), "2", 56, DCOP, alpha=la)

def probe(d, tip, col, yc):
    x, y = tip
    d.line([(x, y), (x, y + 44)], fill=(90, 92, 100), width=6)                # kim
    d.line([(x, y + 44), (x, y + 200)], fill=col, width=26)                   # tay cam
    jx = JR[0] if col == RED else JB[0]
    d.line([(x, y + 200), (x, yc), (jx, yc), (jx, JR[1])], fill=col, width=6, joint="curve")

def meter(d, reading, lbl=True):
    card(d, (290, 826, 790, 1090), fill=BODY, r=22)
    dot(d, JB[0], JB[1], 13, BLACKP, outline=WHITE); dot(d, JR[0], JR[1], 13, RED, outline=WHITE)
    text(d, (JB[0] + 26, JB[1]), "COM", 56, WHITE, anchor="lm"); text(d, (JR[0] + 26, JR[1]), "V", 56, (255, 170, 170), anchor="lm")
    card(d, (340, 895, 740, 990), fill=(220, 240, 225), r=12)
    text(d, (540, 942), reading, 60, (20, 60, 30))
    if lbl: text(d, (540, 1040), "vôn kế số", 56, WHITE, alpha=float(lbl))

def setup(d, rtip, btip, reading="– – –", la=1.0, lbl=True):
    battery(d, la)
    probe(d, btip, BLACKP, 800)
    probe(d, rtip, RED, 772)
    meter(d, reading, lbl)

def table(d, n, y=1140, hl=(), ka=1.0):
    card(d, (40, y, 1040, y + 340), fill=WHITE, outline=NAVY, w=4)
    xs = (110, 340, 630, 900)
    for xx, c in zip(xs, ("Lần", "Que đỏ", "Que đen", "U (V)")): text(d, (xx, y + 50), c, 56, INK)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 138 + i * 72; k, r, b, u = ROWS[i]
        if i in hl: d.rounded_rectangle([58, yy - 34, 1022, yy + 34], radius=16, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), str(k), 56, INK); text(d, (xs[1], yy), r, 56, RED)
        text(d, (xs[2], yy), b, 56, NAVY); text(d, (xs[3], yy), u, 56, BLUE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    setup(d, W1, W2, "?")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1110 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 475), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 65, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Hai que chạm hai điểm", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "trên dây đồng.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 325), "Vôn kế chỉ bao nhiêu?", 60, INK, alpha=a)
    seg_bar(d, y0 + 380, t, M[1] + 0.6, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh (3 lan trong MOT canh) ----------------
def steps(sc):   # (luc bat dau truot toi vi tri k, luc hien so chi)
    M = sc["M"]
    return [(None, 0.9), (3.2, 3.9), (M[1] + 0.4, M[1] + 1.1)]

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
    pill(d, f"Lần {k + 1}", 275, 1.0, ORANGE, size=56, cx=180)
    setup(d, rt, bt, READ[k] if shown else "– – –")
    table(d, n, hl=(k,) if shown else ())
    if k == 2 and shown:                                      # huy hieu dap an, cung luc voi so chi lan 3
        pill(d, "ĐÁP ÁN: 0,00 V", 1540, 1.0, DGREEN)
        kw = appear(t, rd + 2.2, 0.5)                         # nhip hinh: to dam doan day giua hai diem
        if kw > 0: d.rounded_rectangle([W1[0] - 40, 425, W2[0] + 40, 520], radius=24, fill=A((250, 204, 21), 0.8 * kw))

# ---------------- canh 3: Rut ra ----------------
def kcard(d, y, title, color, k, h=200, hl=0.0, sub=None):
    if k <= 0: return
    yy = y + (1 - k) * 30
    fill = mix(WHITE, (237, 233, 254), hl) if hl > 0 else WHITE
    card(d, (60, yy, 1020, yy + h), fill=A(fill, k), outline=A(color, k), w=6)
    text(d, (W / 2, yy + h / 2 - (38 if sub else 0)), title, 60, color, alpha=k)
    if sub: text(d, (W / 2, yy + h / 2 + 50), sub, 56, INK, alpha=k)

def s_rut(img, d, t, sc):
    M = sc["M"]
    k1, k2, k3 = appear(t, 0.3, 0.45), appear(t, 2.8, 0.45), appear(t, M[1] + 0.5, 0.45)
    kcard(d, 330, "Số chỉ = V đỏ − V đen", GREEN, k1, sub="V: điện thế")
    kcard(d, 640, "Đổi que: số chỉ đổi dấu", ORANGE, k2)
    kcard(d, 950, "Cùng dây dẫn: U ≈ 0", PURPLE, k3, hl=appear(t, M[1] + 2.4, 0.5))
    kp = appear(t, M[1] + 2.4, 0.5)               # nhip hinh: day dong + hai diem cung mau (khong chu)
    if kp > 0:
        yw = 1300
        d.line([(200, yw), (880, yw)], fill=A(COPPER, kp), width=14)
        for xx in (380, 700): dot(d, xx, yw, 18, A(PURPLE, kp), outline=WHITE)

# ---------------- canh 4: Bay roi Chua noi duoc (nhip 0 / 3,0 / M1-0,1) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.2) * (1.0 - k2)
    setup(d, PLUS, MINUS, "1,5 V", la=0, lbl=appear(t, 0.0, 0.2))
    y0 = 1110
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 65, a1, DRED)
        q = "“Cực (+) có điện thế 1,5 V”"
        ks = clamp((t - 0.3) / 0.4); f = F(58); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 58, DRED, alpha=a1)
        if ks > 0:                              # gach cheo manh, chu van doc ro
            x0 = W / 2 - lw / 2 - 6; d.line([(x0, yy + 30), (x0 + (lw + 12) * ks, yy + 30 - 64 * ks)], fill=A(DRED, 0.8 * a1), width=4)
        kc = a1 * appear(t, 3.0, 0.4)
        if kc > 0:
            card(d, (90, y0 + 290, 990, y0 + 410), fill=A((236, 253, 243), kc), r=20)
            text(d, (W / 2, y0 + 350), "✓ Chỉ biết hiệu: 1,5 V", 58, DGREEN, alpha=kc)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y0 + 65, k2, NAVY)
        text(d, (W / 2, y0 + 250), "Dây có dòng lớn: chưa thử.", 60, INK, alpha=k2)

# ---------------- canh 5: THU NGHI (cau chot o khung: hai pin noi tiep, do o (+) pin phai, den o (-) pin trai -> 3,0 V) ----------------
def cell(d, x0, w=250):
    """Pin 1,5 V nam ngang: mat (-) phang ben trai, num (+) ben phai."""
    d.rounded_rectangle([x0, 400, x0 + w, 544], radius=18, fill=BODY, outline=NAVY, width=3)
    d.rectangle([x0 - 14, 418, x0, 526], fill=METAL)
    d.rounded_rectangle([x0 + w, 446, x0 + w + 32, 498], radius=6, fill=METAL, outline=NAVY, width=2)
    text(d, (x0 + w / 2 + 6, 472), "1,5 V", 56, WHITE)
    text(d, (x0 + 30, 470), "−", 60, WHITE); text(d, (x0 + w - 26, 470), "+", 56, WHITE)

CA, CB = 90, 570                                  # x0 pin trai, pin phai
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    cell(d, CA); cell(d, CB)
    d.line([(CA + 282, 472), (CB - 14, 472)], fill=COPPER, width=12)          # day dong: (+) pin trai -> (-) pin phai
    text(d, ((CA + 282 + CB - 14) / 2, 368), "dây đồng", 56, DCOP, alpha=k)
    probe(d, (CA - 6, 522), BLACKP, 800)                                       # den: mat (-) pin trai
    probe(d, (CB + 266, 497), RED, 772)                                        # do: num (+) pin phai
    meter(d, "?", lbl=False)
    y0 = 1100
    card(d, (40, y0, 1040, 1600), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", y0 + 55, k, ORANGE)
    text(d, (W / 2, y0 + 150), "Nối thêm pin thứ hai.", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 250), "Vôn kế chỉ bao nhiêu?", 62, (176, 64, 8), alpha=k)
    seg_bar(d, y0 + 330, t, 1.0, sc["T"] - 0.2, ORANGE, k)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1508, 970, 1590), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1549), "Gợi ý: điện thế từng điểm?", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    st = steps(do)
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + rd, "tick") for _, rd in st[:2]]
    out += [(do["t0"] + st[2][1], "ding"), (r["t0"] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-dien-the-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện thế · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vôn kế và dây đồng", draw=s_hook, tail=0.4, caps=[
   ("Pin 1,5 V để hở.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.2, caps=[
   ("Lần 1 và 2: que chạm hai cực.", 5.4),
   ("Lần 3: hai que trên dây đồng.", 4.4)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("Đổi que là đổi thứ tự.", 4.4),
   ("Mọi điểm trên dây cùng điện thế.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy thường gặp.", 5.8),
   ("Mới thử pin để hở.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng lại, tự tính.", 7.6)]),
])
