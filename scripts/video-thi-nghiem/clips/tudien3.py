# Clip: tn-l11-tudien-03 - Tu phang tu che tu hai tam nhom (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l11-tudien-03.json (mo hinh C = eps.S/(9e9.4pi.d), khong phai so do that):
#   so_lieu_mau (S m2, d mm, eps, C pF): 0,04 1 1 354 ; 0,04 2 1 177 ; 0,02 1 1 177 ; 0,04 1 3 1061.
#   Moi lan chi doi mot yeu to roi tra ve goc (d = 1 mm, S = 0,04 m2) - dung cac_buoc.lam.
# Du doan (khung, K10): truot lech con nua phan chong nhau -> C ? ; B. con khoang mot nua (DUNG).
# Bay (hien_tuong_hay_sai[0] "phai noi nguon moi co dien dung"): hai tu canh nhau, da tich dien / chua tich dien,
#   dong ho deu 354 pF.
# Cau chot v3 (TU SUY, phien chinh chot 27/11; gia tri CHUA do): khe d = 4 mm (tham_so d max 4) VA nhua eps = 3 kin
#   khe, S = 0,04 -> C = cap_pf(0,04; 4; 3) ~ 265 pF. Clip khong chieu so 265, khong chieu "x 1/4".
from engine import *

def cap_pf(S, d_mm, eps): return eps * S / (9e9 * 4 * math.pi * d_mm * 1e-3) * 1e12
assert abs(cap_pf(0.04, 4, 3) - 265.3) < 0.1   # cau chot v3
ROWS = [("gốc", 0.04, 1, 1, 354), ("d = 2 mm", 0.04, 2, 1, 177), ("lệch nửa", 0.02, 1, 1, 177), ("chèn nhựa", 0.04, 1, 3, 1061)]
for _, S, dm, e, c in ROWS: assert round(cap_pf(S, dm, e)) == c
CHOT = round(cap_pf(0.02, 1, 3)); assert CHOT == 531 and CHOT not in [r[4] for r in ROWS]
RATIO = ["", "× 0,5", "× 0,5", "× 3"]

AL = (170, 178, 192); ALD = (95, 105, 125); PLA = (253, 224, 140); OVL = (191, 219, 254)
SCR = (220, 240, 225); BOXF = (70, 78, 100); DRED = (185, 28, 28); DGREEN = (21, 110, 55); EMPTY = (148, 140, 128)
X0, L, YB = 120, 600, 760
PXMM = 50

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

def dash(d, p1, p2, col, w=3, on=14, off=10):
    Ln = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(Ln // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / Ln, min(1, (i * (on + off) + on) / Ln)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)

def rig(d, dmm=1.0, shift=0.0, plastic=0.0, reading="354 pF", ghost=False, a=1.0, labels=True, meter=True, pl_ovl=False):
    gap = dmm * PXMM; yt = YB - gap; sx = shift * L / 2
    xa0, xa1 = X0 + sx, X0 + L + sx
    o0, o1 = max(X0, xa0), min(X0 + L, xa1)
    d.rectangle([o0, yt, o1, YB], fill=A(OVL, a))
    if plastic > 0:
        p0 = o0 if pl_ovl else X0
        px1 = p0 + (o1 - p0) * ease(plastic)
        d.rectangle([p0, yt, px1, YB], fill=A(PLA, a), outline=A((180, 140, 40), a), width=2)
    d.rectangle([X0, YB, X0 + L, YB + 16], fill=A(AL, a), outline=A(ALD, a), width=3)
    d.rectangle([xa0, yt - 16, xa1, yt], fill=A(AL, a), outline=A(ALD, a), width=3)
    if ghost:
        g = A(PURPLE, a)
        for (p, q) in (((X0 + L / 2, yt - 16), (X0 + L * 1.5, yt - 16)), ((X0 + L * 1.5, yt - 16), (X0 + L * 1.5, yt)),
                       ((X0 + L / 2, yt), (X0 + L * 1.5, yt))):
            dash(d, p, q, g, w=5)
        arrow(d, (560, yt - 80), (760, yt - 80), g, w=8, head=24)
    if meter:
        d.line([(100, 540), (100, YB + 44), (170, YB + 44), (170, YB + 16)], fill=A(NAVY, a), width=5, joint="curve")
        d.line([(330, 540), (330, yt - 60), (xa0 + 250, yt - 60), (xa0 + 250, yt - 16)], fill=A(NAVY, a), width=5, joint="curve")
        card(d, (50, 300, 430, 540), fill=A(BOXF, a), r=22)
        text(d, (240, 345), "đo C", 58, WHITE, alpha=a)
        card(d, (70, 395, 410, 520), fill=A(SCR, a), r=12)
        text(d, (240, 458), reading, 62, (20, 60, 30), alpha=a)
    if not labels: return
    text(d, (1040, YB + 75), "khe vẽ phóng to", 56, INK, anchor="rm", alpha=a)
    kd = a * (1 - ease(shift * 4))
    if kd > 0.02:
        xr = X0 + L + 20
        arrow(d, (xr + 20, yt + gap / 2), (xr + 20, yt + 2), A(INK, kd), w=4, head=12)
        arrow(d, (xr + 20, yt + gap / 2), (xr + 20, YB - 2), A(INK, kd), w=4, head=12)
        text(d, (xr + 44, yt + gap / 2), f"d = {round(dmm)} mm", 58, INK, anchor="lm", alpha=kd)

def table(d, n, y=960, ratio=0, hl=None, ka=1.0, hdr=False):
    card(d, (40, y, 1040, y + 110 + 85 * 4), fill=WHITE, outline=NAVY, w=4)
    xs = (240, 580, 860)
    text(d, (xs[1], y + 55), "C (pF)", 58, INK)
    if ratio or hdr: text(d, (xs[2], y + 55), "so gốc", 58, INK)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 145 + i * 85; lab, *_, c = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - 38, 1020, yy + 38], radius=18, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), lab, 58, INK); text(d, (xs[1], yy), str(c), 60, BLUE)
        if i < ratio and RATIO[i]: text(d, (xs[2], yy), RATIO[i], 60, GREEN)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    a = appear(t, M[1] - 0.2, 0.4)
    rig(d, ghost=a > 0.5, labels=False)
    if a <= 0: return
    y0 = 930 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 185), "Trượt tấm trên lệch,", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "chỉ còn nửa phần chồng nhau.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 365), "C sẽ thế nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 470, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 nhip, moi nhip mot phu de) ----------------
def s_do(img, d, t, sc):
    M = sc["M"]
    def bump(k, back=True):                       # 0 -> 1 khi doi, 1 -> 0 khi tra ve goc (cuoi nhip)
        on = ease((t - M[k] - 0.2) / 0.6)
        off = ease((t - M[k + 1] + 0.7) / 0.5) if back and k + 1 < len(M) else 0
        return on - off
    dmm = 1 + bump(1); sh = bump(2); pl = clamp((t - M[3] - 0.2) / 0.7)
    n = 1 if t >= M[0] + 0.4 else 0; rd = "354 pF"
    for k in (1, 2, 3):
        if t >= M[k] + 0.9:
            n = k + 1; rd = f"{ROWS[k][4]} pF" if (k == 3 or t < M[k + 1] - 0.2) else "354 pF"
    rig(d, dmm, sh, pl if t >= M[3] else 0, rd)
    table(d, n)

# ---------------- canh 3: Ket qua ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, 1, 1, 0, labels=False, meter=False)
    pill(d, W / 2, 420, "ĐÁP ÁN · một nửa", NAVY)
    table(d, 4, y=860, ratio=sum(t >= 0.5 + 0.3 * i for i in range(4)), hl=2, ka=1.0, hdr=True)
    k1 = appear(t, M[1] + 0.3, 0.4)
    if k1 > 0:
        card(d, (40, 1360, 1040, 1520), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1440), "Chỉ phần đối diện", 62, DGREEN, alpha=k1)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def mini(d, cx, charged, a):
    x0, x1 = cx - 190, cx + 190
    d.rectangle([x0, 700, x1, 716], fill=A(AL, a), outline=A(ALD, a), width=3)
    d.rectangle([x0, 634, x1, 650], fill=A(AL, a), outline=A(ALD, a), width=3)
    d.rectangle([x0, 650, x1, 700], fill=A(OVL, a))
    if charged:
        for j in range(4):
            text(d, (x0 + 60 + 87 * j, 600), "+", 58, RED, alpha=a); text(d, (x0 + 60 + 87 * j, 760), "−", 58, BLUE, alpha=a)
    card(d, (cx - 160, 820, cx + 160, 930), fill=A(SCR, a), r=12)
    text(d, (cx, 875), "354 pF", 62, (20, 60, 30), alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    pill(d, W / 2, 290, "BẪY", DRED, k0)
    text(d, (275, 430), "đã tích điện", 58, INK, alpha=k0)
    text(d, (805, 430), "chưa tích điện", 58, INK, alpha=k0)
    mini(d, 275, True, k0)
    k1 = appear(t, M[1] - 0.2, 0.4)
    mini(d, 805, False, k1)
    k3 = appear(t, M[2] - 0.7, 0.4)
    if k3 > 0:
        card(d, (40, 1110, 1040, 1450), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1180, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1330), "Dây đo có góp thêm C không?", 60, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    rig(d, 4, 0, 1, labels=False, meter=False, a=k, pl_ovl=True)
    text(d, (420, 660), "nhựa ε = 3", 58, (110, 65, 0), alpha=k)
    xr = X0 + L + 30
    arrow(d, (xr + 20, 660), (xr + 20, 562), A(INK, k), w=4, head=12); arrow(d, (xr + 20, 660), (xr + 20, 758), A(INK, k), w=4, head=12)
    text(d, (xr + 50, 660), "4 mm", 58, INK, anchor="lm", alpha=k)
    text(d, (W / 2, 960), "Khe 4 mm, nhựa chèn kín khe.", 60, INK, alpha=k)
    text(d, (W / 2, 1060), "Gốc 354 pF (khe 1 mm).", 60, INK, alpha=k)
    text(d, (W / 2, 1160), "C bây giờ bao nhiêu?", 64, DRED, alpha=k)
    seg_bar(d, 1320, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + do["M"][k] + 0.9, "tap") for k in (1, 2, 3)]
    out += [(da["t0"] + 2.2, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-tudien-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tụ điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tụ tự chế từ hai tấm nhôm", draw=s_hook, tail=0.3, caps=[
   ("Hai tấm nhôm, khe 1 mm.", 3.2),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đo lần gốc, khe 1 mm.", 3.4),
   ("Tăng khe lên 2 mm.", 3.0),
   ("Trượt lệch nửa tấm.", 2.8),
   ("Chèn tấm nhựa kín khe.", 2.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Lệch nửa: 177 pF.", 3.4),
   ("Khe hẹp, có nhựa: C lớn.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: phải nối nguồn mới có C?", 3.4),
   ("Chưa tích điện, vẫn 354 pF.", 3.6),
   ("Còn bỏ ngỏ.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự trả lời.", 6.9)]),
])
