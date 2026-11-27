# Clip: tn-l11-nguon-dien-03 - Noi tat pin tieu: dong doan mach chi con r gioi han.
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nguon-dien-03.json -> so_lieu_mau (nguon, E V, r Ohm, R_day Ohm, I A):
#   pin AA moi 1,5 0,3 0 5,0 ; pin AA moi + day 0,05 Ohm 1,5 0,3 0,05 4,3 ; pin AA da dung 1,5 1,0 0 1,5 ;
#   ac quy xe may 12,6 0,02 0 630. tham_so t = 3 s (co_dinh).
# Ban 1 (16/11/2026). Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 56 px, <= 180 tu/phut moi canh, nhip >= 2 s,
#   K10 (khong nut A-D, phu de "Dung lai, tu doan."), thanh dem 5 o, the CHUA NOI DUOC >= 4 s, nhip Bay >= 3 s.
# AN TOAN: KHONG ve tay nguoi; kep cach dien tu kep vao/thao ra; the "Khong tu lam o nha" o moi canh co mach.
# Du doan (giu ca cu): noi tat 3 s pin moi roi pin da dung (cung 1,5 V ho mach) -> dong nao lon hon? -> pin moi
#   (5,0 A so voi 1,5 A). Hop exp trong bai chi bao "so hai lan do", khong neu ket qua.
#   KHONG hien r = 1,0 Ohm cua pin da dung (cau Tu kiem tra o bai truoc do r = 1,0 Ohm tu bang): chi ghi "r lon hon".
# Bay (hien_tuong_hay_sai[1]): "E lon moi nguy hiem" -> pin 9 V co r vai om (CA TU SUY: E 9 V, r 2 Ohm trong
#   tham_so -> 4,5 A) cho dong NHO hon pin AA 1,5 V r 0,3 Ohm (5,0 A). Khong dung cap so Du doan (5,0 / 1,5).
# CHUA NOI DUOC (sai_so_thuong_gap[1]): giu lau hon 3 s, r co doi?
# THU NGHI v2 (27/11, = cau_chot khung, CA TU SUY): khong noi tat, moi pin noi R = 1,0 Ohm -> pin moi 1,5/1,3 = 1,15 A,
#   pin da dung 1,5/2,0 = 0,75 A -> gap ~1,5 lan (khong phai 3,3 lan nhu luc noi tat). Bo ca day 0,05 Ohm (trung khuon
#   Tu kiem tra 4: the so I = E/(R + r)); bo ca hai pin noi tiep vi ghep nguon day SAU hop nay.
from engine import *

ROWS = [("pin AA mới", 1.5, 0.3, 0.0, 5.0), ("pin AA mới, dây 0,05 Ω", 1.5, 0.3, 0.05, 4.3),
        ("pin AA đã dùng", 1.5, 1.0, 0.0, 1.5), ("ắc quy xe máy", 12.6, 0.02, 0.0, 630.0)]
NEW, NEWW, OLD, ACQ = ROWS
T_NOI = 3.0

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-nguon-dien-03.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == [tuple(r) for r in ROWS]
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["t"]["gia_tri"] == T_NOI and ts["E"]["min"] <= 9 <= ts["E"]["max"] and ts["r"]["min"] <= 2 <= ts["r"]["max"]
    for name, E, r, Rd, I in ROWS: assert abs(E / (r + Rd) - I) <= 0.05 * max(1, I / 10), name
    assert NEW[4] > OLD[4] and NEW[2] < OLD[2] and NEW[1] == OLD[1]
    assert abs(9 / 2 - 4.5) < 1e-9 and 4.5 < NEW[4]                    # bay: pin 9 V, r 2 Ohm -> 4,5 A < 5,0 A
_kiem_so()

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
FS = 58
WIRE = (60, 66, 92); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
COPPER = (184, 115, 51); HOT = (255, 70, 20); WARN_BG = (254, 226, 226)
PIN_NEW = ((255, 237, 213), ORANGE); PIN_OLD = ((226, 228, 234), (100, 106, 120))

_SX = "/System/Library/Fonts/Supplemental/STIXGeneralBolIta.otf"; _sc = {}
def FX(size):
    if size not in _sc: _sc[size] = ImageFont.truetype(_SX, int(size))
    return _sc[size]
def mt(d, xy, s, size, color=INK, alpha=1.0):
    parts = [p for p in re.split(r"(ℰ)", s) if p]
    fs = [FX(size * 1.12) if p == "ℰ" else F(size) for p in parts]
    tot = sum(tw(d, p, f) for p, f in zip(parts, fs))
    x = xy[0] - tot / 2; yb = xy[1] + size * 0.36
    for p, f in zip(parts, fs):
        dtext(d, (x, yb), p, f, color, alpha, "ls"); x += tw(d, p, f)

def pill(d, cx, cy, s, fill, alpha=1.0, size=FS, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(LIGHT, a), r=18, w=4)

def warn(d, y, a=1.0):
    s = "⚠ Không tự làm ở nhà"; w = tw(d, s, F(56)) + 70
    card(d, (W / 2 - w / 2, y, W / 2 + w / 2, y + 90), fill=A(WARN_BG, a), outline=A(DRED, a), r=24, w=4)
    text(d, (W / 2, y + 45), s, 56, DRED, alpha=a)

# ---------------- dung cu: pin nam ngang, hai kep cach dien, day dong, ampe ke ----------------
def rig(d, label, old, att, heat, nhan_day=True):
    """att 0..1: kep phai tu kep vao cuc (+) (khong co tay). heat 0..1: do nong day dong (mau theo I^2)."""
    py = 540
    d.line([(250, py), (210, py), (210, 810), (300, 810)], fill=WIRE, width=7, joint="curve")
    if heat > 0.02:
        d.line([(300, 810), (600, 810)], fill=A(HOT, 0.30 * heat), width=int(10 + 34 * heat))
    d.line([(300, 810), (600, 810)], fill=mix(COPPER, HOT, heat), width=8)
    d.line([(600, 810), (652, 810)], fill=WIRE, width=7)
    d.ellipse([652, 762, 748, 858], fill=WHITE, outline=BLUE, width=6); text(d, (700, 812), "A", 58, BLUE)
    d.line([(748, 810), (890, 810), (890, 660)], fill=WIRE, width=7, joint="curve")
    fill, edge = PIN_OLD if old else PIN_NEW
    card(d, (330, py - 56, 730, py + 56), fill=fill, outline=edge, r=22, w=5)
    d.rounded_rectangle([730, py - 26, 760, py + 26], radius=6, fill=edge)
    text(d, (700, py - 92), "+", 60, edge); text(d, (360, py - 92), "−", 60, edge)
    text(d, (530, py), label, 56, INK)
    d.polygon([(330, py - 22), (296, py - 30), (296, py + 30), (330, py + 22)], fill=(90, 90, 100))
    card(d, (236, py - 30, 300, py + 30), fill=(40, 44, 60), r=12)
    dy = -90 * (1 - att)
    d.line([(890, 660), (890, py + dy + 60), (850, py + dy)], fill=WIRE, width=7, joint="curve")
    d.polygon([(760, py - 22 + dy), (794, py - 30 + dy), (794, py + 30 + dy), (760, py + 22 + dy)], fill=(90, 90, 100))
    card(d, (790, py - 30 + dy, 854, py + 30 + dy), fill=DRED, r=12)
    if nhan_day: text(d, (450, 880), "dây đồng", 56, INK)

def readout(d, x0, y0, label, reading):
    card(d, (x0, y0, x0 + 440, y0 + 160), fill=BODY, r=20)
    card(d, (x0 + 18, y0 + 14, x0 + 422, y0 + 90), fill=SCREEN, r=10)
    text(d, (x0 + 220, y0 + 52), reading, FS, SCR_INK)
    text(d, (x0 + 220, y0 + 124), label, 56, WHITE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    warn(d, 255)
    rig(d, "pin", False, 0.0, 0.0, nhan_day=False)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1010 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 160), "Cùng 1,5 V khi hở mạch", 58, INK, alpha=k)
    text(d, (W / 2, y0 + 245), "Nối tắt pin mới,", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 325), "rồi pin đã dùng.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 410), "Dòng nào lớn hơn?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 475, t, M[1], sc["T"] - 0.2, PURPLE, k)

# ---------------- canh 2: Tien hanh (hai lan noi tat 3 s) ----------------
TA1, TA2, T_KEP, T_NGUOI = 1.0, 5.8, 0.25, 1.2    # bat dau kep ; kep vao mat 0,25 s ; giu dung 3 s ; day nguoi 1,2 s
T_SWAP, T_ROW2 = 5.5, 9.2                         # hang 1 hien cung luc doi pin
def run_state(t):
    """-> (nhan pin, pin cu?, att, heat, so ampe ke, so dong ho, so hang bang)."""
    def one(ta, I):
        tc = ta + T_KEP
        att = clamp((t - ta) / T_KEP) if t < tc + T_NOI else 1 - clamp((t - tc - T_NOI) / T_KEP)
        on = tc <= t < tc + T_NOI
        tt = clamp(t - tc, 0, T_NOI)
        hmax = (I / NEW[4]) ** 2
        heat = hmax * clamp((t - tc) / T_NOI)
        if t > tc + T_NOI: heat = hmax * max(0.0, 1 - (t - tc - T_NOI) / T_NGUOI)
        return att, on, tt, heat
    if t < T_SWAP:
        att, on, tt, heat = one(TA1, NEW[4]); lab, old, I = "pin mới", False, NEW[4]
    else:
        att, on, tt, heat = one(TA2, OLD[4]); lab, old, I = "pin đã dùng", True, OLD[4]
    n = (t >= T_SWAP) + (t >= T_ROW2)
    return lab, old, att, heat, (vn(I) if on else "0,0") + " A", vn(tt) + " s", n

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    warn(d, 255)
    lab, old, att, heat, ia, ts, n = run_state(t)
    rig(d, lab, old, att, heat)
    thao = ia == "0,0 A" and float(ts.split()[0].replace(",", ".")) >= T_NOI - 1e-9   # het 3 s: kep da thao
    readout(d, 70, 950, "đã tháo kẹp" if thao else "ampe kế", ia); readout(d, 570, 950, "thời gian", ts)
    card(d, (40, 1150, 1040, 1520), fill=WHITE, outline=LIGHT, w=4)
    text(d, (300, 1215), "nguồn", FS, INK); text(d, (790, 1215), "I (A)", FS, INK)
    d.line([(70, 1260), (1010, 1260)], fill=LIGHT, width=4)
    for j, (name, I) in enumerate((("pin mới", NEW[4]), ("pin đã dùng", OLD[4]))):
        if n > j:
            y = 1320 + 110 * j
            text(d, (300, y), name, FS, NAVY); text(d, (790, y), vn(I), FS, INK)
    kh = appear(t, sc["M"][2], 0.45)
    if kh > 0: d.rounded_rectangle([60, 1268, 1020, 1372], radius=22, outline=A(DGREEN, kh), width=6)

# ---------------- canh 3: Rut ra (cot so sanh I) ----------------
BX0, BY0, BY1 = 200, 1380, 900                       # truc I 0-6 A
def by(i): return BY0 - i / 6.0 * (BY0 - BY1)
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 720, 1040, 1590), fill=WHITE, outline=LIGHT, w=4)
    d.line([(BX0, BY0), (BX0, BY1 - 40)], fill=NAVY, width=5); d.line([(BX0, BY0), (990, BY0)], fill=NAVY, width=5)
    for i in (2, 4, 6):
        d.line([(BX0, by(i)), (990, by(i))], fill=LIGHT, width=3); text(d, (BX0 - 20, by(i)), str(i), 56, INK, anchor="rm")
    text(d, (BX0 + 24, BY1 - 70), "I (A)", 56, INK, anchor="lm")
    kb = ease(clamp(t / 0.8))
    for cx, name, I, rl, col in ((420, "pin mới", NEW[4], "r = 0,3 Ω", ORANGE), (790, "pin đã dùng", OLD[4], "r lớn hơn", (110, 116, 130))):
        d.rectangle([cx - 80, by(I * kb), cx + 80, BY0], fill=col)
        text(d, (cx, by(I * kb) - 40), vn(I) + " A", FS, INK)
        text(d, (cx, BY0 + 50), name, 56, INK)
        text(d, (cx, BY0 + 125), rl, 56, NAVY)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        y = 270 + (1 - k1) * 20
        card(d, (50, y, 1030, y + 400), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
        text(d, (W / 2, y + 80), "Dây gần 0 Ω:", 62, BLUE, alpha=k1)
        text(d, (W / 2, y + 170), "chỉ còn r chặn dòng", 62, BLUE, alpha=k1)
        mt(d, (W / 2, y + 290), "I = ℰ / r", 68, INK, k1)

# ---------------- canh 4: Bay - "E lon moi nguy hiem" + CHUA NOI DUOC ----------------
B2 = 3.4
def mini(d, x0, top, E, rr, I, col, ka):
    card(d, (x0, 640, x0 + 480, 1180), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=4)
    text(d, (x0 + 240, 710), top, FS, INK, alpha=ka)
    mt(d, (x0 + 240, 800), "ℰ = " + E, FS, INK, ka)
    text(d, (x0 + 240, 885), "r = " + rr, FS, INK, alpha=ka)
    card(d, (x0 + 90, 960, x0 + 390, 1080), fill=A(BODY, ka), r=16)
    card(d, (x0 + 104, 974, x0 + 376, 1066), fill=A(SCREEN, ka), r=10)
    text(d, (x0 + 240, 1020), I, 62, col, alpha=ka)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k3 = appear(t, M[2] - 0.2, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k3)
    if a1 > 0:
        card(d, (40, 260, 1040, 580), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 330, "BẪY", DRED, a1)
        q = "ℰ lớn mới nguy hiểm"; yy = 470
        mt(d, (W / 2, yy), q, 64, DRED, a1)
        ks = clamp((t - B2 - 0.3) / 0.5)
        if ks > 0:
            lw = tw(d, q.replace("ℰ", "E"), F(64)) + 10
            d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 4)], fill=A(DRED, 0.85 * a1), width=5)
        a2 = appear(t, B2, 0.45) * a1
        if a2 > 0:
            mini(d, 40, "Pin 9 V", "9,0 V", "2 Ω", "4,5 A", INK, a2)
            mini(d, 560, "Pin AA mới", "1,5 V", "0,3 Ω", "5,0 A", DRED, a2)
            text(d, (W / 2, 1240), "Số trong ô: dòng nối tắt", 58, INK, alpha=a2)
    if k3 > 0:
        card(d, (40, 300, 1040, 840), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 380, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 520), "Giữ lâu hơn 3 giây,", 62, INK, alpha=k3)
        text(d, (W / 2, 620), "r có đổi không?", 62, INK, alpha=k3)
        cx, cy = W / 2, 1150                                  # dong ho bam giay chay tiep
        d.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], fill=A(WHITE, k3), outline=A(NAVY, k3), width=8)
        d.rectangle([cx - 22, cy - 190, cx + 22, cy - 150], fill=A(NAVY, k3))
        sw = (90 * max(0.0, t - (M[2] - 0.2))) % 360
        if sw > 1: d.pieslice([cx - 140, cy - 140, cx + 140, cy + 140], -90, -90 + sw, fill=A((254, 202, 202), k3))
        ang = math.radians(-90 + sw)
        d.line([(cx, cy), (cx + 120 * math.cos(ang), cy + 120 * math.sin(ang))], fill=A(DRED, k3), width=8)
        dot(d, cx, cy, 14, A(NAVY, k3))

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    mt(d, (W / 2, 440), "ℰ = 1,5 V, nối R = 1,0 Ω", 62, INK, k)
    for cx, nm, rr, pc in ((290, "mới", "r = 0,3 Ω", PIN_NEW), (790, "đã dùng", "r = 1,0 Ω", PIN_OLD)):
        card(d, (cx - 170, 600, cx + 170, 700), fill=A(pc[0], k), outline=A(pc[1], k), r=20, w=5)
        text(d, (cx, 650), nm, 58, INK, alpha=k)
        text(d, (cx, 780), rr, 60, INK, alpha=k)
    text(d, (W / 2, 960), "Dòng pin mới gấp mấy lần?", 64, DORANGE, alpha=k)
    seg_bar(d, 1250, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = (sc[x] for x in ("hook", "do", "rut", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + TA1 + T_KEP, "tap"), (do["t0"] + TA2 + T_KEP, "tap"), (do["t0"] + do["M"][2], "ding")]
    out += [(b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return out

def _kiem_dong_bo():
    """Moi 0,05 s: ampe ke chi I khi va chi khi kep da vao het va dong ho <= 3 s."""
    bad = []; t = 0.0
    while t < 13.0:
        lab, old, att, heat, ia, ts, n = run_state(t)
        tt = float(ts.split()[0].replace(",", "."))
        if ia != "0,0 A" and att < 0.99: bad.append((round(t, 2), "co dong khi kep chua vao"))
        if tt > T_NOI + 1e-9: bad.append((round(t, 2), "qua 3 s"))
        t += 0.05
    if not (TA1 + T_KEP + T_NOI < T_SWAP and TA2 + T_KEP + T_NOI < T_ROW2): bad.append("hang bang truoc khi thao kep")
    if TA1 + T_KEP + T_NOI + T_NGUOI > T_SWAP + 1e-9: bad.append("doi pin khi day con nong")
    return bad

CLIP = dict(id="tn-l11-nguon-dien-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Nguồn điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nối tắt pin tiểu", draw=s_hook, tail=0.3, caps=[
   ("Hai pin AA.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chỉ nối 3 giây, kẹp cách điện.", 4.6),
   ("Đổi pin đã dùng, làm lại.", 4.2),
   ("Đáp án: pin mới lớn hơn hẳn.", 3.4)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Cùng 1,5 V, chỉ r khác nhau.", 3.6),
   ("r càng nhỏ, dòng càng lớn.", 3.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Pin 9 V và pin AA.", 3.2),
   ("r nhỏ, dòng mới lớn.", 3.2),
   ("Còn chỗ chưa rõ.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.0)]),
])

if __name__ == "__main__":
    print("lệch đồng bộ:", _kiem_dong_bo() or "không")
