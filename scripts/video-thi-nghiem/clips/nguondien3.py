# Clip: tn-l11-nguon-dien-03 - Noi tat pin tieu: dong doan mach chi con r gioi han (16/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nguon-dien-03.json -> so_lieu_mau (nguon, E V, r Ohm, R_day Ohm, I A):
#   pin AA moi 1,5 0,3 0 5,0 ; pin AA moi + day 0,05 Ohm 1,5 0,3 0,05 4,3 ; pin AA da dung 1,5 1,0 0 1,5 ;
#   ac quy xe may 12,6 0,02 0 630. tham_so t = 3 s. quan_sat: day nong ro; pin chi am neu giu lau.
#   Kiem: I = E/(r + R_day) tung hang (_kiem_so()).
# AN TOAN (brief 16/11): KHONG ve tay nguoi cam day; kep ca sau co vo cach dien tu kep vao/thao ra; the
#   "Khong tu lam o nha" hien suot canh Tien hanh, o hop Du doan va man Chot; bay nhac khong noi tat ac quy, pin lithium.
# Du doan: noi tat 3 s pin moi roi pin da dung (ho mach deu 1,5 V) -> dong hai lan so voi nhau?
#   Dap an: pin moi lon hon han (5,0 A so voi 1,5 A) vi r nho hon. KHONG tra loi cau Tu kiem tra cua muc II:
#   q2 (y nghia 1,5 V tren vo pin), q3 (r tu bang = 1,0 Ohm - clip noi "r ~ 1,0 Ohm" cua pin DA DUNG, khong tinh tu bang
#   R-I-U), q4 (E 6,0 V, r 0,50, R 2,5 -> 2,0 A).
# Bay = hien_tuong_hay_sai[1]: "nguon E lon moi nguy hiem" -> cung E 1,5 V ma 5,0 A va 1,5 A; ac quy r 0,02 -> 630 A.
# Cau hoi chot (ca tu suy, hang 2 kho, chua tung hien): pin moi + day 0,05 Ohm -> I = 1,5/0,35 = 4,3 A (< 5,0 A).
# Bo cuc (khac nguondien1 do thi U-t, nguondien2 bang R-I-U): hinh pin nam ngang + hai kep + day dong doi mau theo
#   nhiet + ampe ke 10 A + dong ho giay ; Rut ra = cot so sanh I.
from engine import *

ROWS = [("pin AA mới", 1.5, 0.3, 0.0, 5.0), ("pin AA mới, dây 0,05 Ω", 1.5, 0.3, 0.05, 4.3),
        ("pin AA đã dùng", 1.5, 1.0, 0.0, 1.5), ("ắc quy xe máy", 12.6, 0.02, 0.0, 630.0)]
NEW, NEWW, OLD, ACQ = ROWS
T_NOI = 3.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

WIRE = (60, 66, 92); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
PINC = ORANGE; DGREEN = (10, 80, 40); COPPER = (184, 115, 51); HOT = (255, 70, 20); HL = (255, 237, 213)
WARN_BG = (254, 226, 226)

_SX = "/System/Library/Fonts/Supplemental/STIXGeneralBolIta.otf"; _sc = {}
def FS(size):
    if size not in _sc: _sc[size] = ImageFont.truetype(_SX, int(size))
    return _sc[size]
def mt(d, xy, s, size, color=INK, alpha=1.0, anchor="m"):
    parts = [p for p in re.split(r"(ℰ)", s) if p]
    fs = [FS(size * 1.12) if p == "ℰ" else F(size) for p in parts]
    tot = sum(tw(d, p, f) for p, f in zip(parts, fs))
    x = xy[0] - tot / 2 if anchor == "m" else xy[0]; yb = xy[1] + size * 0.36
    for p, f in zip(parts, fs):
        dtext(d, (x, yb), p, f, color, alpha, "ls"); x += tw(d, p, f)

def warn(d, y, a=1.0, size=44):
    s = "⚠ Không tự làm ở nhà"; w = tw(d, s, F(size)) + 70
    card(d, (W / 2 - w / 2, y, W / 2 + w / 2, y + size + 34), fill=A(WARN_BG, a), outline=A(RED, a), r=24, w=4)
    text(d, (W / 2, y + (size + 34) / 2), s, size, RED, alpha=a)

# ---------------- dung cu: pin nam ngang, hai kep cach dien, day dong, ampe ke ----------------
def rig(d, oy, label, att, heat, cap=True):
    """att 0..1: kep phai tu kep vao cuc (+) (khong co tay). heat 0..1: do nong day dong (mau theo I^2)."""
    py = 520 + oy                                       # truc pin
    # day: kep trai -> xuong -> day dong -> ampe ke -> len -> kep phai
    d.line([(250, py), (210, py), (210, 800 + oy), (300, 800 + oy)], fill=WIRE, width=7, joint="curve")
    if heat > 0.02:
        d.line([(300, 800 + oy), (600, 800 + oy)], fill=A(HOT, 0.30 * heat), width=int(10 + 34 * heat))
    d.line([(300, 800 + oy), (600, 800 + oy)], fill=mix(COPPER, HOT, heat), width=8)
    d.line([(600, 800 + oy), (656, 800 + oy)], fill=WIRE, width=7)
    d.ellipse([656, 756 + oy, 744, 844 + oy], fill=WHITE, outline=BLUE, width=6); text(d, (700, 802 + oy), "A", 42, BLUE)
    d.line([(744, 800 + oy), (890, 800 + oy), (890, 640 + oy)], fill=WIRE, width=7, joint="curve")
    # pin
    card(d, (330, py - 50, 730, py + 50), fill=(255, 237, 213), outline=PINC, r=22, w=5)
    d.rounded_rectangle([730, py - 24, 760, py + 24], radius=6, fill=PINC)
    text(d, (690, py), "+", 46, PINC); text(d, (370, py), "−", 46, PINC)
    text(d, (530, py), label, 40, INK)
    # kep trai (cuc -): vo cach dien den
    d.polygon([(330, py - 22), (296, py - 30), (296, py + 30), (330, py + 22)], fill=(90, 90, 100))
    card(d, (236, py - 30, 300, py + 30), fill=(40, 44, 60), r=12)
    # kep phai (cuc +): vo cach dien do, tu nang len 90 px khi chua kep
    dy = -90 * (1 - att)
    d.line([(890, 640 + oy), (890, py + dy + 60), (850, py + dy)], fill=WIRE, width=7, joint="curve")
    d.polygon([(760, py - 22 + dy), (794, py - 30 + dy), (794, py + 30 + dy), (760, py + 22 + dy)], fill=(90, 90, 100))
    card(d, (790, py - 30 + dy, 854, py + 30 + dy), fill=(185, 28, 28), r=12)

def readout(d, x0, y0, label, reading):
    card(d, (x0, y0, x0 + 440, y0 + 126), fill=BODY, r=20)
    card(d, (x0 + 18, y0 + 16, x0 + 422, y0 + 78), fill=SCREEN, r=10)
    text(d, (x0 + 220, y0 + 47), reading, 46, SCR_INK)
    text(d, (x0 + 220, y0 + 100), label, 40, WHITE, bold=False)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
Q_AT = 1.2
def s_hook(img, d, t, sc):
    rig(d, 440, "pin", 0.0, 0.0, cap=False)
    warn(d, 1370)
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 250 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 250, "Nối tắt pin mới, rồi pin đã dùng\n(cùng 1,5 V khi hở mạch).\nHai dòng so với nhau thế nào?",
          44, INK, maxw=940, alpha=a)
    text(d, (W / 2, y0 + 440), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 510, 940, y0 + 522], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 510, 140 + 800 * (1 - p), y0 + 522], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (hai lan noi tat 3 s) ----------------
TA1, TA2, T_KEP, T_NGUOI = 1.0, 5.8, 0.25, 1.2    # bat dau kep ; kep vao mat 0,25 s ; giu dung 3 s ; day nguoi 1,2 s
T_SWAP, T_ROW1, T_ROW2, T_ANS = 5.5, 4.4, 9.2, 10.2
def run_state(t):
    """-> (nhan pin, att, heat, so ampe ke, so dong ho giay, so hang bang)."""
    def one(ta, I):
        tc = ta + T_KEP                                  # luc kep cham han cuc (+): bat dau 3 s
        att = clamp((t - ta) / T_KEP) if t < tc + T_NOI else 1 - clamp((t - tc - T_NOI) / T_KEP)
        on = tc <= t < tc + T_NOI
        tt = clamp(t - tc, 0, T_NOI)
        hmax = (I / NEW[4]) ** 2                         # nhiet trong day ti le I^2 (cung day, cung 3 s)
        heat = hmax * clamp((t - tc) / T_NOI)
        if t > tc + T_NOI: heat = hmax * max(0.0, 1 - (t - tc - T_NOI) / T_NGUOI)
        return att, on, tt, heat
    if t < T_SWAP:
        att, on, tt, heat = one(TA1, NEW[4]); lab, I = "pin mới", NEW[4]
    else:
        att, on, tt, heat = one(TA2, OLD[4]); lab, I = "pin đã dùng", OLD[4]
    n = (t >= T_ROW1) + (t >= T_ROW2)
    return lab, att, heat, (vn(I) if on else "0,0") + " A", vn(tt) + " s", n

def s_do(img, d, t, sc):
    warn(d, 255)
    lab, att, heat, ia, ts, n = run_state(t)
    rig(d, 0, lab, att, heat)
    readout(d, 70, 900, "ampe kế", ia); readout(d, 570, 900, "thời gian", ts)
    card(d, (40, 1070, 1040, 1100 + 46 + 2 * 96), fill=WHITE, outline=LIGHT, w=3)
    text(d, (760, 1110), "I (A)", 40, INK)
    d.line([(60, 1146), (1020, 1146)], fill=LIGHT, width=3)
    for j, (name, I) in enumerate((("pin mới", NEW[4]), ("pin đã dùng", OLD[4]))):
        if n > j:
            y = 1146 + 96 * j + 48
            text(d, (300, y), name, 44, NAVY); text(d, (760, y), vn(I), 44, INK)
    ka = appear(t, T_ANS, 0.15)
    if ka > 0:
        card(d, (60, 1480, 1020, 1590), fill=A((21, 110, 52), ka), r=30)
        text(d, (W / 2, 1535), "ĐÁP ÁN · pin mới lớn hơn hẳn", 42, WHITE, alpha=ka)

# ---------------- canh 3: Rut ra (cot so sanh I) + Chua noi duoc ----------------
BX0, BY0, BY1 = 220, 1330, 860                       # truc I 0-6 A
def by(i): return BY0 - i / 6.0 * (BY0 - BY1)
def s_rut(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 700, 1040, 1440), fill=WHITE, outline=LIGHT, w=3)
    d.line([(BX0, BY0), (BX0, BY1 - 20)], fill=NAVY, width=5); d.line([(BX0, BY0), (980, BY0)], fill=NAVY, width=5)
    for i in (2, 4, 6):
        d.line([(BX0, by(i)), (980, by(i))], fill=LIGHT, width=3); text(d, (BX0 - 16, by(i)), str(i), 40, MUTED, anchor="rm")
    text(d, (BX0 + 20, BY1 - 40), "I (A)", 40, INK, anchor="lm")
    kb = ease(clamp(t / 0.8))
    for cx, name, I, r, col in ((440, "pin mới", NEW[4], NEW[2], ORANGE), (790, "pin đã dùng", OLD[4], OLD[2], GRAY)):
        d.rectangle([cx - 80, by(I * kb), cx + 80, BY0], fill=col)
        text(d, (cx, by(I) - 34), vn(I) + " A", 44, INK, alpha=appear(t, 0.8, 0.3))
        text(d, (cx, BY0 + 40), name, 40, INK)
        kr = appear(t, 0.4, 0.4)
        if kr > 0: text(d, (cx, BY0 + 88), "r ≈ " + vn(r) + " Ω", 40, col if col != GRAY else MUTED, alpha=kr)
    k1 = appear(t, 1.2, 0.45)
    if k1 > 0:
        y = 250 + (1 - k1) * 20
        card(d, (50, y, 1030, y + 200), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
        text(d, (W / 2, y + 62), "Dây ≈ 0 Ω: chỉ còn r chặn dòng", 44, BLUE, alpha=k1)
        mt(d, (W / 2, y + 140), "I = ℰ / r", 50, INK, k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y = 470 + (1 - k2) * 20
        card(d, (50, y, 1030, y + 124), fill=A(WHITE, k2), outline=A(RED, k2), w=6)
        text(d, (W / 2, y + 62), "Nhiệt r·I²·t toả ngay trong pin", 44, RED, alpha=k2)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y = 1462 + (1 - k3) * 20
        card(d, (50, y, 1030, y + 210), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 55), "Chưa nói được", 42, NAVY, alpha=k3)
        mt(d, (W / 2, y + 145), "Giữ lâu, r có đổi?", 44, INK, k3 * appear(t, M[2] + 0.3, 0.4))

# ---------------- canh 4: Bay - "nguon E lon moi nguy hiem" ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    card(d, (40, 260, 1040, 560), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(RED, a1), r=32)
    text(d, (W / 2, 322), "BẪY", 38, WHITE, alpha=a1)
    q = "ℰ lớn mới nguy hiểm"
    mt(d, (W / 2, 450), q, 50, RED, a1)
    ks = clamp((t - (M[1] + 0.3)) / 0.4)
    if ks > 0:
        lw = tw(d, q.replace("ℰ", "E"), F(50)) + 10
        d.line([(W / 2 - lw / 2 - 6, 452), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, 452)], fill=RED, width=6)
    a2 = appear(t, 0.4, 0.4)                             # bang chung tu chinh thi nghiem: cung E, khac r
    if a2 > 0:
        card(d, (60, 620, 1020, 830), fill=A(HL, a2), r=24)
        mt(d, (W / 2, 690), "Cùng ℰ = 1,5 V", 44, INK, a2)
        text(d, (W / 2, 770), "mà 5,0 A và 1,5 A", 42, INK, alpha=a2)
    a3 = appear(t, M[1] + 0.3, 0.4)
    if a3 > 0:
        card(d, (60, 940, 1020, 1200), fill=A(WARN_BG, a3), outline=A(RED, a3), w=5)
        mt(d, (W / 2, 1010), "Ắc quy: ℰ = 12,6 V, r = 0,02 Ω", 44, INK, a3)
        text(d, (W / 2, 1100), "→ 630 A, dây đỏ rực", 48, RED, alpha=a3)
    ka = appear(t, M[1] + 1.6, 0.5)
    if ka > 0:
        text(d, (W / 2, 1270), "✓ r nhỏ → dòng rất lớn", 48, DGREEN, alpha=ka)
        card(d, (60, 1340, 1020, 1560), fill=A(WARN_BG, ka), outline=A(RED, ka), w=6)
        text(d, (W / 2, 1405), "⚠ Không tự làm ở nhà", 48, RED, alpha=ka)
        text(d, (W / 2, 1490), "Không nối tắt ắc quy, pin lithium", 44, RED, alpha=ka)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: pin moi + day 0,05 Ohm, so voi 5,0 A lan dau?"""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    mt(d, (W / 2, 400), "Đoản mạch: I = ℰ / r", 56, GREEN, k0)
    warn(d, 545, k0, 40)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 660, 1040, 1400), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 690, W / 2 + pw / 2, 754), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 722), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 900, "Pin mới, thay dây bằng dây 0,05 Ω.\nSo với 5,0 A lần đầu,\nampe kế chỉ bao nhiêu?",
          44, INK, maxw=950, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1100, 970, 1350), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1225, "Gợi ý: chỉ đổi dây", 44, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.9, "ding")]
    out += [(do["t0"] + TA1, "tap"), (do["t0"] + TA2, "tap"), (do["t0"] + T_ANS, "ding"),
            (r["t0"] + 1.2, "tap"), (b["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

# ---------------- kiem vat li ----------------
def _kiem_so():
    bad = []
    for name, E, r, Rd, I in ROWS:
        if abs(E / (r + Rd) - I) > 0.05 * max(1, I / 10): bad.append((name, E / (r + Rd), I))
    if not (NEW[4] > OLD[4] and NEW[2] < OLD[2] and NEW[1] == OLD[1]): bad.append("dap an: cung E, r nho -> I lon")
    if not (NEWW[4] < NEW[4] and abs(1.5 / 0.35 - 4.3) < 0.05): bad.append("ca chot 0,05 Ohm")
    if NEWW[4] in (NEW[4], OLD[4]): bad.append("so cau chot trung so tren man")
    return bad

def _kiem_dong_bo():
    """Moi 0,05 s: ampe ke chi I khi va chi khi kep da vao het (att = 1) va dong ho giay <= 3 s."""
    bad = []; t = 0.0
    while t < 12.0:
        lab, att, heat, ia, ts, n = run_state(t)
        tt = float(ts.split()[0].replace(",", "."))
        if ia != "0,0 A" and att < 0.99: bad.append((round(t, 2), "co dong khi kep chua vao"))
        if tt > T_NOI + 1e-9: bad.append((round(t, 2), "qua 3 s"))
        if ia != "0,0 A" and ia not in (vn(NEW[4]) + " A", vn(OLD[4]) + " A"): bad.append((round(t, 2), ia))
        t += 0.05
    if not (TA1 + T_KEP + T_NOI < T_ROW1 and TA2 + T_KEP + T_NOI < T_ROW2): bad.append("hang bang truoc khi thao kep")
    if TA1 + T_KEP + T_NOI + T_NGUOI > T_SWAP + 1e-9: bad.append("doi pin khi day con nong")
    return bad

CLIP = dict(id="tn-l11-nguon-dien-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Nguồn điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nối tắt pin tiểu", draw=s_hook, tail=0.4, caps=[
   ("Pin tiểu AA.", 2.6),
   ("Nghĩ trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.8, caps=[
   ("Chỉ nối 3 giây, kẹp cách điện.", 4.4),
   ("Đổi pin, làm lại.", 5.6)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=1.0, caps=[
   ("Chỉ r khác nhau.", 3.0),
   ("Pin cũng toả nhiệt.", 3.0),
   ("Còn bỏ ngỏ.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=1.0, caps=[
   ("Đúng không?", 2.5),
   ("Còn ắc quy?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__":
    print("số lệch:", _kiem_so() or "không")
    print("lệch đồng bộ:", _kiem_dong_bo() or "không")
