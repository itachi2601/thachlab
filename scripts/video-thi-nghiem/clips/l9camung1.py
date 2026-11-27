# Clip: tn-l9-camung-01 - Thi nghiem Faraday: nam cham thang va cuon day noi dien ke (KHTN 9, bai 92, 18/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l9-camung-01.json:
#   tham_so: t mac dinh 1 s, K = 1,0 mA.s, mo hinh i = K/t -> dua lai gan trong 1 s: 1,0 mA (khop so_lieu_mau hang
#   t = 1,0 s, trung binh 1,0 mA). Keo ra xa trong 1 s: cung 1,0 mA nhung kim lech PHIA KIA (quan_sat 2; do lon theo mo hinh).
#   Nam cham dung yen: i = 0 (mo_hinh). Chua noi duoc = khong_chung_minh[0] + so_lieu_mau.ghi_chu (so minh hoa).
#   Bay (cong B 18/11): "keo ra xa, kim lech cung phia" (hien_tuong_hay_sai[1]); bay cu = Bay 1/Cau 5 bai.
# Tranh tra loi san cau hoi cua bai:
#   - Cau 4 + Kiem tra nhanh cau 1 (nam cham NAM YEN TRONG cuon day): nam cham trong clip KHONG BAO GIO vao trong cuon.
#   - Cau 1 (D: pin trong dien ke): khong noi "khong pin" (chi ve mach khong co pin).
#   - Cau 3 (dua cuon day lai gan), Cau 5, Cau 6 (quay quanh truc doc): khong co trong clip; bo buoc quay (de clip 03).
#   - Khong dung "duong suc" (muc 3 day sau thi nghiem).
# Du doan (K10: chi cau hoi + hinh): lai gan -> kim lech phai; keo ra xa -> kim the nao? -> lech sang trai (ngược phia).
# Cau chot: lai gan roi ra xa, lap lai lien tuc -> kim lech qua lai (ghep hai lan vua xem; chua chieu trong clip).
#   The chot hien SAU 4 s nghi (nhat ky 18/11), khong dung chot_hoi.
# Hinh: nhin ngang; nam cham (N do ben phai, S xanh) truot tren truc cuon day, chi tu XA toi SAT mieng cuon (khong vao).
# Dung lai 27/11/2026 theo cong moi (viec 4 L9, nhom B): chu than canh >= 55 (ra >= 48 px), moi nhip >= 2,5 s, du doan
#   phu len vung dien ke (thanh dem lien), canh dap an co hinh chuyen dong, Bay doi sang hien_tuong_hay_sai[2]
#   (cuon day ho: hai mach canh nhau), Chua noi duoc = o "Chua noi duoc" cua hop TN1 trong bai (cai gi doi gay ra dong).
import copy
from engine import *

K_BO, T_DUA = 1.0, 1.0                 # tham_so K (mA.s), t mac dinh (s)
I_DUA = K_BO / T_DUA                   # 1,0 mA (so_lieu_mau hang t = 1,0 s: TB 1,0)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

# ---------------- bo cuc (khung 1080x1920) ----------------
CY = 520                               # truc nam cham / cuon day
CL, CRR, CR, NT = 650, 950, 118, 10     # cuon day: mep trai, mep phai, nua chieu cao, so vong ve
ML, MH = 280, 84                       # nam cham
FAR, NEAR = 340, 600                   # vi tri dau cuc N: xa / sat mieng cuon (CL = 650: KHONG vao trong)
GX, GY, GR, GANG, GMAX = 540, 1180, 290, 56, 2.0
TLX, TRX, TY = 650, 880, 790           # hai cuc dien ke (tren mep the)

# ---------------- hinh ve ----------------
def turns(): return [CL + j * (CRR - CL) / (NT - 1) for j in range(NT)]

def coil_back(d):
    c = mix(ORANGE, BG, 0.45)
    for x in turns(): d.arc([x - 17, CY - CR, x + 17, CY + CR], 90, 270, fill=c, width=7)

def coil_front(d):
    for x in turns(): d.arc([x - 17, CY - CR, x + 17, CY + CR], 270, 90, fill=A(ORANGE, 0.95), width=9)
    text(d, ((CL + CRR) / 2, CY - CR - 50), "cuộn dây", 58, mix(ORANGE, INK, 0.3))

def magnet(d, tip):
    x0, xm = tip - ML, tip - ML / 2
    d.rounded_rectangle([x0, CY - MH / 2, xm, CY + MH / 2], radius=10, fill=BLUE)
    d.rounded_rectangle([xm, CY - MH / 2, tip, CY + MH / 2], radius=10, fill=RED)
    d.rectangle([xm - 10, CY - MH / 2, xm, CY + MH / 2], fill=BLUE)
    d.rectangle([xm, CY - MH / 2, xm + 10, CY + MH / 2], fill=RED)
    text(d, (x0 + ML / 4, CY + 1), "S", 58, WHITE)
    text(d, (tip - ML / 4, CY + 1), "N", 58, WHITE)

def wires(d):
    d.line([(CL, CY + CR - 4), (CL, TY - 20), (TLX, TY)], fill=NAVY, width=5)
    d.line([(CRR, CY + CR - 4), (CRR, TY - 40), (TRX, TY - 40), (TRX, TY)], fill=NAVY, width=5)
    for x in (TLX, TRX): dot(d, x, TY, 11, NAVY)

def needle_xy(i, r):
    a = math.radians(clamp(i / GMAX, -1.08, 1.08) * GANG)
    return GX + r * math.sin(a), GY - r * math.cos(a)

def galvo(d, i, ghost=None, peak=None):
    card(d, (120, TY, 960, 1300), fill=WHITE, outline=NAVY, r=30, w=5)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 270 - GANG - 3, 270 + GANG + 3, fill=NAVY, width=5)
    for k in range(-4, 5):
        v = k / 2; a = math.radians(v / GMAX * GANG); big = k % 2 == 0
        r0 = GR - (30 if big else 18)
        d.line([(GX + r0 * math.sin(a), GY - r0 * math.cos(a)), (GX + GR * math.sin(a), GY - GR * math.cos(a))],
               fill=NAVY, width=5 if big else 3)
        if big: text(d, (GX + (GR + 42) * math.sin(a), GY - (GR + 42) * math.cos(a)), str(abs(int(v))), 56, NAVY)
    text(d, (930, 1180), "mA", 56, NAVY, anchor="rm")
    text(d, (155, 1180), "điện kế", 56, NAVY, anchor="lm")
    if ghost is not None and abs(ghost - i) > 0.1:
        d.line([(GX, GY), needle_xy(ghost, GR - 8)], fill=A(GRAY, 0.8), width=5)
    d.line([(GX, GY), needle_xy(i, GR - 8)], fill=RED, width=9)
    dot(d, GX, GY, 16, NAVY)
    sh = peak if (peak and abs(i) >= 0.5 * abs(peak)) else 0.0      # so nhay thang 0 <-> dinh
    if abs(sh) > 0.05: text(d, (GX, 1250), vn(abs(sh)) + " mA", 58, RED if sh > 0 else BLUE)
    else: text(d, (GX, 1250), "0 mA", 58, NAVY)

def vlabel(d, s):
    if s: text(d, (FAR - ML / 2 + 130, CY - 115), s, 60, PURPLE)

def apparatus(d, tip, i, ghost=None, vtxt="", peak=None):
    coil_back(d); magnet(d, tip); coil_front(d); wires(d); galvo(d, i, ghost, peak); vlabel(d, vtxt)

# ---------------- canh 1: Du doan (the phu len vung dien ke) ----------------
THINK_END = 0.3
DPURP = (76, 29, 149); DGREEN = (10, 110, 50); DRED = (185, 28, 28); DINK = (60, 66, 90)


def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, FAR, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 790 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 175), "Đưa N lại gần: kim lệch phải.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Kéo N ra xa: kim thế nào?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 360, 970, y0 + 460], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 360, 110 + max(90, 860 * (1 - p)), y0 + 460], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh (dung yen -> lai gan -> ra xa, MOT canh) ----------------
DLY, DUR = 0.6, T_DUA                 # tre sau phu de, thoi gian dua (1 s that)
def moves(sc):
    M = sc["M"]
    return [(M[1] + DLY, FAR, NEAR, +I_DUA), (M[2] + DLY, NEAR, FAR, -I_DUA)]

def do_state(t, sc):
    """-> tip, i (mA), van toc (+ lai gan), ghost, peak, so hang bang da xong, nhan v."""
    tip, i, v, ghost, pk, vt = FAR, 0.0, 0, None, None, "đứng yên"
    rows = 1 if t >= sc["M"][0] + 1.2 else 0
    for n, (t0, xa, xb, im) in enumerate(moves(sc)):
        t1 = t0 + DUR
        if t < t0: break
        tip = lerp(xa, xb, clamp((t - t0) / DUR))
        i = im * ease((t - t0) / 0.12) * (1 - ease((t - t1) / 0.15)); pk = im
        if t < t1: v = 1 if xb > xa else -1; vt = "lại gần →" if v > 0 else "← ra xa"
        else: vt = "đứng yên"
        if t > t1 + 0.2: ghost = im; rows = n + 2
    return tip, i, v, ghost, pk, rows, vt

ROWS = [("Đứng yên", "ở số 0", 0.0), ("Lại gần", "lệch phải", I_DUA), ("Ra xa", "lệch trái", -I_DUA)]
def s_do(img, d, t, sc):
    tip, i, v, ghost, pk, rows, vt = do_state(t, sc)
    apparatus(d, tip, i, ghost, vt, pk)

def _kiem_vat_li():
    """Chieu kim theo chieu chuyen dong; dung yen thi 0; nam cham khong vao cuon; bang khop kim da hien."""
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        tip, i, v, ghost, pk, rows, vt = do_state(t, sc)
        if tip > CL - 20: bad.append((round(t, 2), "nam cham vao cuon"))
        if v != 0 and abs(i) > 0.05 and (i > 0) != (v > 0): bad.append((round(t, 2), "kim nguoc chieu chuyen dong"))
        moving = any(t0 - 0.01 <= t <= t0 + DUR + 0.3 for t0, *_ in moves(sc))
        if not moving and abs(i) > 1e-6: bad.append((round(t, 2), "dung yen ma kim lech"))
        if rows > 1 and ghost is not None and abs(ghost - ROWS[rows - 1][2]) > 1e-9: bad.append((round(t, 2), "bang lech kim"))
        t += 0.02
    if moves(sc)[-1][0] + DUR + 0.3 > sc["T"]: bad.append("ra xa chua xong khi het canh")
    return bad

def _kiem_so():
    bad = []
    if abs(I_DUA - 1.0) > 1e-9: bad.append("I_DUA khac hang so_lieu_mau t = 1,0 s (TB 1,0 mA)")
    if not (0.25 <= T_DUA <= 3): bad.append("t ngoai tham_so")
    if ROWS[1][2] != -ROWS[2][2]: bad.append("ra xa phai nguoc chieu lai gan")
    return bad

# ---------------- canh 3: Dap an + Rut ra (hai o nho, nam cham chay qua lai dung chieu) ----------------
def mini(d, box, v, k, t):
    x0, y0, x1, y1 = box
    card(d, box, fill=A(WHITE, k), outline=A(RED if v > 0 else BLUE, k), w=4)
    text(d, ((x0 + x1) / 2, y0 + 50), "Lại gần" if v > 0 else "Ra xa", 58, INK, alpha=k)
    ph = (t % 1.6) / 1.6; u = ease(clamp(ph / 0.7))            # 0 -> 1 trong 70 % chu ki, roi lap lai
    mid = (x0 + x1) / 2; off = (-60 + 120 * u) if v > 0 else (60 - 120 * u)
    mx, my = mid + off - 40, y0 + 170
    d.rounded_rectangle([mx - 100, my - 26, mx, my + 26], radius=8, fill=A(BLUE, k))
    d.rounded_rectangle([mx, my - 26, mx + 100, my + 26], radius=8, fill=A(RED, k))
    cxl = x1 - 50                                             # mep cuon day nho ben phai
    for j in range(4): d.arc([cxl - 12 + 10 * j - 14, my - 50, cxl - 12 + 10 * j + 14, my + 50], 270, 90, fill=A(ORANGE, k), width=5)
    cx, cy, r = (x0 + x1) / 2, y1 - 45, 150
    d.arc([cx - r, cy - r, cx + r, cy + r], 270 - 50, 270 + 50, fill=A(NAVY, k), width=4)
    d.line([(cx, cy - r - 10), (cx, cy - r + 14)], fill=A(NAVY, k), width=4)
    moving = ph < 0.7
    a = math.radians(40 * (1 if v > 0 else -1) * (math.sin(math.pi * ph / 0.7) if moving else 0))
    d.line([(cx, cy), (cx + (r - 10) * math.sin(a), cy - (r - 10) * math.cos(a))], fill=A(RED, k), width=7)
    dot(d, cx, cy, 10, A(NAVY, k))


def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: lệch trái", 300, ka)
    mini(d, (60, 380, 525, 840), +1, ka, t)
    mini(d, (555, 380, 1020, 840), -1, ka, t)
    k1 = appear(t, M[1] + 0.3, 0.45)
    if k1 > 0:
        card(d, (40, 900, 1040, 1120), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 960), "Chuyển động đối với nhau", 58, DGREEN, alpha=k1)
        text(d, (W / 2, 1050), "→ có dòng điện", 58, DGREEN, alpha=k1)


# ---------------- canh 4: Bay (cuon day ho) + Chua noi duoc ----------------
BAY_X, BAY_ST, BAY_E = 2.6, 5.2, 7.8
def circuit(d, x0, kin, ka, t, kk):
    """O nho: nam cham chay qua lai truoc cuon day; kin = mach kin hay ho mot dau."""
    card(d, (x0, 470, x0 + 480, 1240), fill=A(WHITE, ka), outline=A(NAVY, ka), w=5)
    text(d, (x0 + 240, 530), "nối kín" if kin else "hở một đầu", 58, NAVY, alpha=ka)
    ph = (t % 1.6) / 1.6; s = math.sin(2 * math.pi * ph) * kk
    mx, my = x0 + 150 + 50 * s, 680
    d.rounded_rectangle([mx - 90, my - 24, mx, my + 24], radius=8, fill=A(BLUE, ka))
    d.rounded_rectangle([mx, my - 24, mx + 90, my + 24], radius=8, fill=A(RED, ka))
    cl = x0 + 330
    for j in range(5): d.arc([cl + 22 * j - 12, my - 60, cl + 22 * j + 12, my + 60], 270, 90, fill=A(ORANGE, ka), width=6)
    cx, cy, r = x0 + 240, 1100, 140
    ty = cy - r + 30                                          # hai cuc dien ke
    d.line([(cl, my + 60), (cl, 850), (cx - 60, 850), (cx - 60, ty)], fill=A(NAVY, ka), width=5)
    if kin: d.line([(cl + 88, my + 60), (cl + 88, 910), (cx + 60, 910), (cx + 60, ty)], fill=A(NAVY, ka), width=5)
    else:   # dut mot doan tren day thu hai
        d.line([(cl + 88, my + 60), (cl + 88, 910), (cx + 120, 910)], fill=A(NAVY, ka), width=5)
        d.line([(cx + 75, 910), (cx + 60, 910), (cx + 60, ty)], fill=A(NAVY, ka), width=5)
        dot(d, cx + 120, 910, 9, A(DRED, ka)); dot(d, cx + 75, 910, 9, A(DRED, ka))
    d.arc([cx - r, cy - r, cx + r, cy + r], 270 - 50, 270 + 50, fill=A(NAVY, ka), width=4)
    ang = math.radians(35 * math.cos(2 * math.pi * ph) * kk) if kin else 0.0     # kim ~ toc do nam cham
    d.line([(cx, cy), (cx + (r - 10) * math.sin(ang), cy - (r - 10) * math.cos(ang))], fill=A(RED, ka), width=7)
    dot(d, cx, cy, 10, A(NAVY, ka))


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pill(d, "BẪY", 300, a1, DRED)
    q = "“Cứ đưa nam châm là có dòng”"
    text(d, (W / 2, 410), q, 58, INK, alpha=a1)
    circuit(d, 50, True, a1, t, clamp((t - 0.6) / 0.6))
    a2 = appear(t, BAY_X, 0.45)
    if a2 > 0: circuit(d, 550, False, a2, t, clamp((t - BAY_X) / 0.6))
    k = appear(t, BAY_ST, 0.45)
    if k > 0:
        qw = tw(d, q, F(58))
        d.line([(W / 2 - qw / 2 - 6, 412), (W / 2 + qw / 2 + 6, 412)], fill=A(DRED, k), width=7)
        text(d, (W / 2, 1295), "✓ phải có mạch kín", 58, DGREEN, alpha=k)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (50, 1345, 1030, 1565), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1400), "Chưa nói được:", 58, NAVY, alpha=k3)
        text(d, (W / 2, 1495), "cái gì đổi mà sinh ra dòng", 56, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Nam châm chuyển động: có dòng", 58, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 518, k1, ORANGE)
    text(d, (W / 2, 620), "Đưa N lại gần, ra xa", 60, INK, alpha=k1)
    text(d, (W / 2, 710), "liên tục. Kim thế nào?", 60, INK, alpha=k1)
    if k1 > 0:   # nam cham chay qua lai truoc cuon day; KHONG ve dien ke
        my = 1150; s = math.sin(2 * math.pi * t / 1.6)
        mx = 420 + 70 * s
        d.rounded_rectangle([mx - 130, my - 34, mx, my + 34], radius=10, fill=A(BLUE, k1))
        d.rounded_rectangle([mx, my - 34, mx + 130, my + 34], radius=10, fill=A(RED, k1))
        text(d, (mx + 65, my), "N", 58, WHITE, alpha=k1)
        for j in range(7): d.arc([700 + 26 * j - 15, my - 100, 700 + 26 * j + 15, my + 100], 270, 90, fill=A(ORANGE, k1), width=8)
        arrow(d, (300, my - 120), (520, my - 120), A(PURPLE, k1), w=6, head=20)
        arrow(d, (520, my + 120), (300, my + 120), A(PURPLE, k1), w=6, head=20)
        text(d, (W / 2, 1450), "kim = ?", 62, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    cs += [(do["t0"] + t0, "tap") for t0, *_ in moves(do)]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + BAY_ST, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return cs


CLIP = dict(id="tn-l9-camung-01", header="KHTN 9 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nam châm và cuộn dây", draw=s_hook, tail=THINK_END, caps=[
   ("Cuộn dây kín nối điện kế.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Nam châm đứng yên.", 2.6),
   ("Đưa lại gần trong 1 giây.", 3.6),
   ("Kéo ra xa trong 1 giây.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ngược phía lúc lại gần.", 3.6),
   ("Đó là dòng điện cảm ứng.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Hai mạch, cùng đưa nam châm.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự nghĩ.", 7.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch vật lí:", _kiem_vat_li() or "không")
