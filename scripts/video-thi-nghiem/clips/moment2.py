# Clip: tn-l10-moment-luc-02 - Thuoc co truc quay o giua, qua nang va luc ke (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-moment-luc-02.json (_kiem_so() doi chieu):
#   P1 = 2,0 N, d1 = 15 cm ; luc ke 0-5 N ; d2 min 5 cm ; so_lieu_mau d2 (cm) / F2 (N) / F2.d2 (N.cm):
#   10/3,10/31,0 ; 15/2,00/30,0 ; 20/1,52/30,4 ; 30/0,99/29,7.
# Du doan (K10, khong nut): moc luc ke sat truc o 5 cm (d2 min) -> luc ke 5 N co giu thuoc ngang duoc khong?
#   (dap an: khong; mo hinh can 30/5 = 6 N > 5 N, so 6 khong hien). Doi ca so voi ban 1 (20 cm -> 1,5 N) vi
#   bang d2-F2 nam ngay duoi clip trong bai lam lo dap an.
# Bay = hien_tuong_hay_sai[0] (so luc hai ben thay vi so tich): o 30 cm luc ke 0,99 N < 2,0 N ma thuoc van ngang.
#   Khong noi lan nao lech / vi sao lech (cau "Doc so lieu" + Bam xem). Keo xien = hien_tuong_hay_sai[1] -> chi o CHUA NOI.
# Chot (ca tu suy, ghi trong so_lieu_mau.ghi_chu kho): qua nang 2,0 N ra 20 cm, luc ke o 25 cm -> 2,0.20/25 = 1,6 N.
#   1,6 khong co trong bai; khong trung Cau 2 (bap benh 30/45 kg).
from engine import *

DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
RUL = (205, 210, 222); RUL_D = (120, 128, 150)
BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); SKIN = (240, 196, 160)
P1, D1, FMAX = 2.0, 15, 5.0
ROWS = [(10, 3.10, 31.0), (15, 2.00, 30.0), (20, 1.52, 30.4), (30, 0.99, 29.7)]   # so_lieu_mau
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-moment-luc-02.json")))
    for (d2, f2, m), h in zip(ROWS, k["so_lieu_mau"]["hang"]): assert (d2, f2, m) == tuple(h[:3]), h
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["P1"]["gia_tri"] == P1 and ts["d1"]["gia_tri"] == D1 and ts["d2"]["min"] == 5
    assert "0–5 N" in " ".join(x["ten"] for x in k["dung_cu"])
    assert P1 * D1 / 5 > FMAX                                                     # du doan: 5 cm can hon 5 N
    assert abs(P1 * 20 / 25 - 1.6) < 1e-9                                         # ca chot
_kiem_so()

OX, OY = 540, 560            # truc O
PXC = 13                     # px moi cm -> nua thuoc 35 cm = 455 px
HL, HT = 35 * PXC, 18
TILT = -6.0                  # nghieng (trai xuong) khi luc ke chua du

def rot(x, y, phi, oy):
    a = math.radians(phi)
    return (OX + x * math.cos(a) - y * math.sin(a), oy + x * math.sin(a) + y * math.cos(a))

def ruler(d, phi, oy=OY, a=1.0):
    d.rounded_rectangle([OX - 11, oy - 270, OX + 11, oy], radius=6, fill=A((160, 165, 180), a))
    d.rectangle([OX - 120, oy - 280, OX + 120, oy - 260], fill=A((140, 145, 162), a))
    pts = [rot(-HL, -HT, phi, oy), rot(HL, -HT, phi, oy), rot(HL, HT, phi, oy), rot(-HL, HT, phi, oy)]
    d.polygon(pts, fill=A(RUL, a)); d.line(pts + [pts[0]], fill=A(RUL_D, a), width=4)
    for c in range(-35, 36, 5):
        L = 16 if c % 10 == 0 else 9
        d.line([rot(c * PXC, -HT, phi, oy), rot(c * PXC, -HT + L, phi, oy)], fill=A(NAVY, a), width=3)
    dot(d, OX, oy, 13, A(NAVY, a), A(WHITE, a))

def weight(d, phi, d1=D1, oy=OY, a=1.0):
    p = rot(-d1 * PXC, HT, phi, oy); top = oy + 90
    d.line([p, (p[0], top)], fill=A(NAVY, a), width=4)
    d.rounded_rectangle([p[0] - 78, top, p[0] + 78, top + 110], radius=12, fill=A(BRASS, a), outline=A(BRASS_D, a), width=3)
    text(d, (p[0], top + 55), "2,0 N", 55, WHITE, alpha=a)

def meter(d, phi, d2, f, oy=OY, a=1.0):
    """Luc ke treo duoi thuoc o d2 (cm), keo thang dung xuong. f = so chi (N) hoac None (che '?')."""
    p = rot(d2 * PXC, HT, phi, oy)
    Q = lambda s, h: (p[0] + h, p[1] + s)
    se = luc_ke(d, Q, 30, 50, 380, FMAX, f, nho=0.2, so=(0, 1, 2, 3, 4), hw=40, ben=-1, alpha=a, co=55)
    hx, hy = Q(se + 30, 0); dot(d, hx, hy, 30, A(SKIN, a), A((190, 140, 105), a))

def dims(d, d2, d1=D1, oy=OY, a=1.0):
    y = oy - 52
    for x0, x1, s, col in ((OX - d1 * PXC, OX, f"{d1} cm", BLUE), (OX, OX + d2 * PXC, f"{d2} cm", RED)):
        d.line([(x0 + 4, y), (x1 - 4, y)], fill=A(col, a), width=5)
        for X in (x0 + 4, x1 - 4): d.line([(X, y - 14), (X, y + 14)], fill=A(col, a), width=5)
        if x1 - x0 >= 150: text(d, ((x0 + x1) / 2 + (0 if col == BLUE else 25), y - 42), s, 55, col, alpha=a)
        else: text(d, (x1 + 20, y - 42), s, 55, col, anchor="lm", alpha=a)

def readout(d, val, col=INK, a=1.0):
    card(d, (60, 830, 400, 950), fill=A(WHITE, a), outline=A(RED, a), r=24, w=4)
    text(d, (230, 890), val, 60, col, alpha=a)

def rig(d, phi, d2, f, val, oy=OY, am=1.0):
    ruler(d, phi, oy); weight(d, phi, oy=oy); meter(d, phi, d2, f, oy, a=am); dims(d, d2, oy=oy, a=am); readout(d, val)

XS3 = (230, 540, 850)
def table(d, n, y=1050, prod=None, hl=-1, h=500):
    card(d, (60, y, 1020, y + h), fill=WHITE, outline=NAVY, w=4)
    heads = (("Chỗ móc", "(cm)"), ("Lực kế", "(N)")) + ((("Tích", "(N·cm)"),) if prod is not None else ())
    xs = XS3 if prod is not None else (330, 750)
    for x, (h1, h2) in zip(xs, heads): text(d, (x, y + 55), h1, 55, INK); text(d, (x, y + 115), h2, 55, NOTE)
    d.line([(90, y + 155), (990, y + 155)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 205 + i * 76; d2, f2, m = ROWS[i]
        if i == hl: d.rounded_rectangle([85, yy - 34, 995, yy + 34], radius=14, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(d2), 55, INK); text(d, (xs[1], yy), vn(f2, 2), 55, BLUE)
        if prod is not None and prod > i: text(d, (xs[2], yy), vn(m), 55, DGREEN)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan (K10) ----------------
H_P0, H_P1 = 0.5, 2.2            # keo tu 0 toi 3,10 N o 10 cm, thuoc tu nghieng ve ngang
def s_hook(img, d, t, sc):
    M = sc["M"]
    e = ease((t - H_P0) / (H_P1 - H_P0)); done = t >= H_P1
    rig(d, TILT * (1 - e), 10, ROWS[0][1] * e, vn(ROWS[0][1], 2) + " N" if done else "···")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    for j, s1 in enumerate(("Móc lực kế ở 5 cm:", "lực kế 5 N có đủ", "giữ thước ngang?")):
        text(d, (W / 2, y0 + 185 + j * 85), s1, 60, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 450, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (15, 20, 30 cm) ----------------
TS = [0.5, 3.0, 5.5]
MOVE, HOOK, PULL = 0.7, 0.3, 0.9

def do_state(t):
    """-> (d2, phi, f kim, so hien tren the (None = '···'), so hang bang)."""
    k = max([i for i, s in enumerate(TS) if t >= s], default=-1)
    if k < 0: return 10, 0.0, 3.10, 3.10, 1
    x = t - TS[k]; old, new = ROWS[k], ROWS[k + 1]
    if x < MOVE:
        e = ease(x / MOVE); return old[0], TILT * e, old[1] * (1 - e), None, k + 1
    if x < MOVE + HOOK: return new[0], TILT, 0.0, None, k + 1
    e = ease((x - MOVE - HOOK) / PULL)
    if e < 1: return new[0], TILT * (1 - e), new[1] * e, None, k + 1
    return new[0], 0.0, new[1], new[1], k + 2

def s_do(img, d, t, sc):
    d2, phi, f, shown, n = do_state(t)
    rig(d, phi, d2, f, "···" if shown is None else vn(shown, 2) + " N")
    table(d, n, hl=n - 1 if shown is not None and t > TS[0] else -1)

# ---------------- canh 3: moc sat truc 5 cm, keo het thang ----------------
T5_MOVE, T5_PULL, PULL5 = 0.3, 1.3, 1.8
def s_do5(img, d, t, sc):
    M = sc["M"]
    if t < T5_MOVE + 0.7:
        e = ease((t - T5_MOVE) / 0.7)
        d2 = 30 if e < 0.5 else 5; phi = TILT * e; f = ROWS[3][1] * (1 - e); am = abs(1 - 2 * e)
    else:
        d2 = 5; phi = TILT; f = FMAX * ease((t - T5_PULL) / PULL5); am = 1.0
    rig(d, phi, d2, f, vn(f, 2) + " N" if t >= T5_PULL + PULL5 else "···", am=am)
    table(d, 4)
    if t >= M[1] - 0.1:
        text(d, (230, 1000), "hết thang", 58, DRED)
        text(d, (255, 380), "thước vẫn nghiêng", 58, DRED)

def _kiem_dong_bo():
    """Do: so tren the = kim = hang cuoi bang khi on dinh, thuoc ngang khi va chi khi so hien. Do5: khong bao gio ngang."""
    import copy; clip = copy.deepcopy(CLIP); build(clip); bad = []
    sc = {s["key"]: s for s in clip["scenes"]}; t = 0.0
    while t < sc["do"]["T"]:
        d2, phi, f, shown, n = do_state(t)
        if shown is not None:
            if abs(shown - f) > 1e-9 or abs(phi) > 1e-9 or ROWS[n - 1][0] != d2 or abs(ROWS[n - 1][1] - shown) > 1e-9:
                bad.append(round(t, 2))
        elif abs(phi) < 1e-9 and t > TS[0] + 0.05: bad.append(("ngang ma chua co so", round(t, 2)))
        t += 0.05
    if TS[-1] + MOVE + HOOK + PULL + 0.4 > sc["do"]["T"]: bad.append("do: lan cuoi qua sat cuoi canh")
    if T5_PULL + PULL5 > sc["do5"]["M"][1] - 0.1: bad.append("do5: chu 'het thang' truoc khi kim toi 5 N")
    return bad

# ---------------- canh 4: Ket qua + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    np_ = 0 if t < 0.6 else min(4, 1 + int((t - 0.6) / 0.5))
    table(d, 4, y=290, prod=np_, h=500)
    kr = appear(t, M[1] - 0.1, 0.4)
    if kr <= 0: return
    y0 = 860 + (1 - kr) * 30
    card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pill(d, W / 2, y0 + 70, "RÚT RA", GREEN, kr)
    text(d, (W / 2, y0 + 200), "2,0 N × 15 cm = 30 N·cm", 58, BLUE, alpha=kr)
    text(d, (W / 2, y0 + 305), "Hai bên trục: tích như nhau", 58, DGREEN, alpha=kr)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    rig(d, 0, 30, ROWS[3][1], vn(ROWS[3][1], 2) + " N")
    k3 = appear(t, M[2] - 0.1, 0.4); y = 1030
    if k3 < 1:
        a1 = 1 - k3
        card(d, (40, y, 1040, y + 500), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", DRED, a1)
        q = "“Ngang khi hai lực bằng nhau”"
        ks = clamp((t - M[0] - 1.4) / 0.4); lw = tw(d, q, F(58)); yy = y + 200
        text(d, (W / 2, yy), q, 58, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        if t >= M[1]:
            text(d, (W / 2, y + 315), "0,99 N ≠ 2,0 N", 58, DGREEN, alpha=a1)
            text(d, (W / 2, y + 405), "mà thước vẫn ngang", 58, DGREEN, alpha=a1)
    if k3 > 0:
        yk = y + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 215), "Kéo lực kế xiên thì sao?", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
E_OY = 700
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 290, 1040, 1500), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 350, "THỬ NGHĨ", ORANGE, k)
    ruler(d, 0, E_OY, k); weight(d, 0, d1=20, oy=E_OY, a=k); meter(d, 0, 25, None, E_OY, a=k); dims(d, 25, d1=20, oy=E_OY, a=k)
    text(d, (330, 1060), "Thước ngang.", 60, INK, alpha=k)
    text(d, (W / 2, 1250), "Lực kế chỉ bao nhiêu?", 62, DORANGE, alpha=k)
    seg_bar(d, 1360, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, d5, da, b, e = sc["hook"], sc["do"], sc["do5"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + H_P1, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + s + MOVE + HOOK + PULL, "tap") for s in TS]
            + [(d5["t0"] + T5_PULL + PULL5, "buzz"), (da["t0"] + 0.1, "ding"), (b["t0"] + b["M"][0] + 1.4, "buzz"),
               (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-moment-luc-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Moment lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thước quay quanh trục O", draw=s_hook, tail=0.2, caps=[
   ("Kéo cho thước nằm ngang.", 3.0),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Dời chỗ móc lực kế", draw=s_do, tail=0.4, caps=[
   ("Dời chỗ móc, kéo cho thước ngang.", 3.8),
   ("Ghi số chỉ ở mỗi chỗ móc.", 3.8)]),
 dict(key="do5", title="Móc sát trục", draw=s_do5, tail=0.3, caps=[
   ("Móc sát trục, ở 5 cm.", 3.4),
   ("Đáp án: không giữ được.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Nhân hai cột.", 3.4),
   ("So với bên quả nặng.", 3.5)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("So tích, không so lực.", 3.4),
   ("Còn bỏ ngỏ.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
