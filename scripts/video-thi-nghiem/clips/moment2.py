# Clip: tn-l10-moment-luc-02 - Thuoc co truc quay o giua, qua nang va luc ke (ban 1, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-moment-luc-02.json:
#   P1 = 2,0 N, d1 = 15 cm ; luc ke 0-5 N ; so_lieu_mau d2 (cm) / F2 (N) / F2.d2 (N.cm): 10/3,10/31,0 ; 15/2,00/30,0 ;
#   20/1,52/30,4 ; 30/0,99/29,7. P1.d1 = 30 N.cm. Kiem bang ma: F2.d2 khop cot 3 (_kiem_so()).
# Du doan (K10: chi cau hoi + hinh): o 10 cm luc ke chi 3,1 N; moc xa gap doi (20 cm) thi luc ke chi khoang?
#   A. khoang 6,2 N (gap doi) ; B. khoang 3,1 N (khong doi) ; C. khoang 1,5 N (mot nua, DUNG: do 1,52 N).
# Bay = hien_tuong_hay_sai[0] "so luc hai ben thay vi so moment": o 30 cm F2 = 0,99 N khac 2,0 N ma thuoc van ngang.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): doi qua nang 2,0 N ra 20 cm, luc ke o 25 cm -> F2 = 2,0.20/25 = 1,6 N (mo hinh).
# Khong tra loi san cau trong muc: "Doc so lieu" (lan nao lech nhieu nhat, vi sao) -> khong noi lech/sai so;
#   Cau 2 (bap benh 30 kg/1,5 m, 45 kg -> 1,0 m) -> khong co so cua cau nay tren man.
# Bo cuc (khac moment3 = ngau luc tren ban): thuoc ngang treo tren gia, qua nang trai, luc ke treo duoi ben phai,
#   thuoc nghieng khi doi cho moc roi keo ve nam ngang; bang d2-F2 o duoi.
from engine import *

DRED = (185, 28, 28); NOTE = (60, 64, 84)
WOOD = (205, 210, 222); WOOD_D = (120, 128, 150)        # thuoc nhom
BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); SKIN = (240, 196, 160)
P1, D1 = 2.0, 15
ROWS = [(10, 3.10, 31.0), (15, 2.00, 30.0), (20, 1.52, 30.4), (30, 0.99, 29.7)]   # so_lieu_mau
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    for d2, f2, m in ROWS: assert abs(d2 * f2 - m) < 0.051, (d2, f2, m)
    assert abs(P1 * 20 / 25 - 1.6) < 1e-9                                         # ca chot
_kiem_so()

OX, OY = 540, 560            # truc O
PXC = 13                     # px moi cm -> nua thuoc 35 cm = 455 px
HL, HT = 35 * PXC, 18        # nua dai, nua day thuoc
TILT = -6.0                  # goc nghieng khi chua keo (trai xuong)

def rot(x, y, phi):
    a = math.radians(phi)
    return (OX + x * math.cos(a) - y * math.sin(a), OY + x * math.sin(a) + y * math.cos(a))

def ruler(d, phi):
    d.rounded_rectangle([OX - 11, 290, OX + 11, OY], radius=6, fill=(160, 165, 180))      # thanh gia
    d.rectangle([OX - 120, 280, OX + 120, 300], fill=(140, 145, 162))
    pts = [rot(-HL, -HT, phi), rot(HL, -HT, phi), rot(HL, HT, phi), rot(-HL, HT, phi)]
    d.polygon(pts, fill=WOOD); d.line(pts + [pts[0]], fill=WOOD_D, width=4)
    for c in range(-35, 36, 5):
        L = 16 if c % 10 == 0 else 9
        d.line([rot(c * PXC, -HT, phi), rot(c * PXC, -HT + L, phi)], fill=NAVY, width=3)
    dot(d, OX, OY, 13, NAVY, WHITE)

def weight(d, phi, alpha=1.0):
    p = rot(-D1 * PXC, HT, phi)
    d.line([p, (p[0], 650)], fill=A(NAVY, alpha), width=4)
    d.rounded_rectangle([p[0] - 50, 650, p[0] + 50, 760], radius=12, fill=A(BRASS, alpha), outline=A(BRASS_D, alpha), width=3)
    text(d, (p[0], 705), "2,0 N", 40, WHITE, alpha=alpha)

def meter(d, phi, d2, f, alpha=1.0, hide=False):
    """Luc ke treo duoi thuoc o d2 (cm), keo thang dung xuong. f = so chi (N) hoac None (che '?')."""
    p = rot(d2 * PXC, HT, phi)
    Q = lambda s, h: (p[0] + h, p[1] + s)
    se = luc_ke(d, Q, 40, 60, 440, 5.0, None if hide else f, nho=0.2, so=(0, 1, 2, 3, 4, 5), hw=40, ben=-1, alpha=alpha, co=40)
    d.line([Q(0, 0), Q(28, 0)], fill=A(NAVY, alpha), width=5)
    hx, hy = Q(se + 30, 0); dot(d, hx, hy, 30, A(SKIN, alpha), A((190, 140, 105), alpha))

def labels(d, phi, d2, ftxt, a=1.0, lab=True):
    pl, pr = rot(-D1 * PXC, -HT, phi), rot(d2 * PXC, -HT, phi)
    if lab:
        text(d, (250, 345), "quả nặng kéo thước", 40, NOTE, alpha=a)
        text(d, (820, 345), "lực kế kéo thước", 40, NOTE, alpha=a)
    for p, s, col in ((pl, "P1 = 2,0 N", BLUE), (pr, ftxt, RED)):
        arrow(d, (p[0], p[1] - 90), (p[0], p[1] - 6), A(col, a), w=7, head=22)
        text(d, (p[0], p[1] - 125), s, 44, col, alpha=a)

def readout(d, val, col=INK, a=1.0):
    card(d, (60, 820, 470, 1010), fill=A(WHITE, a), outline=A(LIGHT, a), r=26, w=3)
    text(d, (265, 870), "Lực kế chỉ", 42, NOTE, alpha=a)
    text(d, (265, 950), val, 60, col, alpha=a)

def table(d, n, prod=0, y=1110, hl=-1):
    card(d, (60, y, 1020, y + 470), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 520, 820) if prod else (330, 750)
    heads = ("d2 (cm)", "F2 (N)", "F2·d2 (N·cm)") if prod else ("d2 (cm)", "F2 (N)")
    for x, h in zip(xs, heads): text(d, (x, y + 55), h, 42, INK)
    d.line([(90, y + 95), (990, y + 95)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 150 + i * 82; d2, f2, m = ROWS[i]
        if i == hl: d.rounded_rectangle([85, yy - 34, 995, yy + 34], radius=14, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(d2), 46, INK); text(d, (xs[1], yy), vn(f2, 2), 46, BLUE)
        if prod: text(d, (xs[2], yy), vn(m), 46, GREEN, alpha=appear(prod, 0.4 + 0.5 * i, 0.3))

def rig(d, phi, d2, f, ftxt, val, hide=False, malpha=1.0, lab=True):
    ruler(d, phi); weight(d, phi); meter(d, phi, d2, f, alpha=malpha, hide=hide); labels(d, phi, d2, ftxt, lab=lab)
    readout(d, val)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0, 10, 3.10, "F2", "3,10 N")
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 160), "Ở 10 cm: lực kế chỉ 3,10 N.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "Móc ở 20 cm (xa gấp đôi),", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 320), "lực kế chỉ khoảng mấy N?", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 415), "Chọn đáp án ở khung câu hỏi", 40, NOTE, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 514], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 514], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
TS = [0.6, 3.0, 5.4]                 # doi moc toi 15, 20, 30 cm
MOVE, HOOK, PULL = 0.7, 0.3, 0.9

def do_state(t):
    """-> (d2, phi, f kim, so hien tren the (None = '···'), so hang bang, alpha luc ke)."""
    k = -1
    for i, s in enumerate(TS):
        if t >= s: k = i
    if k < 0: return 10, 0.0, 3.10, 3.10, 1, 1.0
    x = t - TS[k]; old, new = ROWS[k], ROWS[k + 1]
    if x < MOVE:
        e = ease(x / MOVE); return old[0], TILT * e, old[1] * (1 - e), None, k + 1, 1 - e
    if x < MOVE + HOOK:
        return new[0], TILT, 0.0, None, k + 1, ease((x - MOVE) / HOOK)
    e = ease((x - MOVE - HOOK) / PULL)
    if e < 1: return new[0], TILT * (1 - e), new[1] * e, None, k + 1, 1.0
    return new[0], 0.0, new[1], new[1], k + 2, 1.0

def s_do(img, d, t, sc):
    d2, phi, f, shown, n, ma = do_state(t)
    rig(d, phi, d2, f, "F2", "···" if shown is None else vn(shown, 2) + " N", malpha=ma)
    hl = n - 1 if shown is not None and t > TS[0] else -1
    table(d, n, hl=hl)

def _kiem_dong_bo():
    """Moi 0,05 s: so tren the = kim = hang cuoi bang khi da on dinh; thuoc nam ngang khi va chi khi so hien."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        d2, phi, f, shown, n, ma = do_state(t)
        if shown is not None:
            if abs(shown - f) > 1e-9 or abs(phi) > 1e-9 or ROWS[n - 1][0] != d2 or abs(ROWS[n - 1][1] - shown) > 1e-9:
                bad.append(round(t, 2))
        elif abs(phi) < 1e-9 and t > TS[0] + 0.05: bad.append(("ngang ma chua co so", round(t, 2)))
        t += 0.05
    if TS[-1] + MOVE + HOOK + PULL + 0.4 > sc["T"]: bad.append("lan cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    ruler(d, 0); weight(d, 0); meter(d, 0, 20, 1.52)              # ve hinh truoc, nhan dap an de len thanh gia
    lab = "ĐÁP ÁN · Khoảng 1,5 N"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 368), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 334), lab, 42, WHITE, alpha=ka)
    for c0, c1, s, col in ((-D1, 0, "15 cm", BLUE), (0, 20, "20 cm", RED)):        # canh tay don tren thuoc
        y = 470; x0, x1 = OX + c0 * PXC, OX + c1 * PXC
        d.line([(x0 + 4, y), (x1 - 4, y)], fill=col, width=5)
        for X in (x0 + 4, x1 - 4): d.line([(X, y - 14), (X, y + 14)], fill=col, width=5)
        text(d, ((x0 + x1) / 2, y - 40), s, 44, col)
    readout(d, "1,52 N", col=BLUE)
    kp = max(0.0, t - M[0] - 0.1)
    table(d, 4, prod=kp if t > M[0] + 0.1 else 0)
    kr = appear(t, M[1] + 0.1, 0.45)
    if kr <= 0: return
    y0 = 1110 + (1 - kr) * 30
    card(d, (40, y0, 1040, y0 + 480), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pw = tw(d, "RÚT RA", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(GREEN, kr), r=32)
    text(d, (W / 2, y0 + 60), "RÚT RA", 40, WHITE, alpha=kr)
    text(d, (W / 2, y0 + 185), "P1·d1 = 2,0 × 15 = 30 N·cm", 48, BLUE, alpha=kr)
    text(d, (W / 2, y0 + 290), "F2·d2 ≈ 30 N·cm ở mọi lần", 48, GREEN, alpha=kr * appear(t, M[1] + 0.8, 0.4))
    text(d, (W / 2, y0 + 395), "moment hai bên bằng nhau", 46, INK, alpha=kr * appear(t, M[1] + 1.6, 0.4))

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    rig(d, 0, 30, 0.99, "F2", "0,99 N", lab=False)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 1110
    if a1 > 0:
        card(d, (40, y, 1040, y + 480), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        for j, q in enumerate(("“Thước ngang khi", "lực hai bên bằng nhau”")):
            text(d, (W / 2, y + 170 + 70 * j), q, 48, mix(INK, GRAY, clamp((t - 2.0) / 0.4)), alpha=a1)
        ks = clamp((t - 2.0) / 0.4)
        if ks > 0:
            for j, q in enumerate(("“Thước ngang khi", "lực hai bên bằng nhau”")):
                lw = tw(d, q, F(48)); yy = y + 172 + 70 * j
                d.line([(W / 2 - lw / 2 - 6, yy), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 380), "30 cm: 0,99 N ≠ 2,0 N, vẫn ngang", 46, GREEN, alpha=a1 * appear(t, 2.6, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 480), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• Trục lệch khỏi giữa?", "• Nhiều quả nặng?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (100, y + 230 + 120 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot khong chua cong thuc giai -> THU NGHI: qua nang ra 20 cm, luc ke 25 cm (so moi); goi y tre >= 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 420, "F2·d2 gần như không đổi", 48, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 870, "Dời quả nặng 2,0 N ra 20 cm.\nLực kế ở 25 cm, thước ngang.\nLực kế chỉ bao nhiêu?", 48, INK,
          maxw=920, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1160, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1270, "Quả nặng: 15 → 20 cm", 48, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s + MOVE + HOOK + PULL, "tap") for s in TS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-moment-luc-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Moment lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thước quay quanh trục O", draw=s_hook, tail=0.3, caps=[
   ("Kéo thước nằm ngang.", 2.8),
   ("Tự đoán trước.", 8.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Dời lực kế, kéo cho thước ngang.", 3.8),
   ("Đọc lực kế ở mỗi chỗ móc.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Nhân lực với cánh tay đòn.", 3.4),
   ("So hai bên trục.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng hay sai?", 4.0),
   ("Còn bỏ ngỏ.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 8.8)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
