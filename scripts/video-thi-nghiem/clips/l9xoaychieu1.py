# Clip: tn-l9-xoaychieu-01 - Nam cham dien: dong doi chieu thi cuc tu doi theo, kim nam cham lac qua lai (KHTN 9, bai 93)
# Vong 2 (18/11/2026, theo cong B): Du doan KHONG hoi dinh sat (bai noi san 4 cho) va KHONG hoi kim voi 50 Hz (Cau 2):
#   hoi kim voi nguon DOI CHIEU THAT CHAM, moi 2 giay mot lan (mo hinh minh hoa, ghi trong so_lieu_mau.ghi_chu cua kho).
#   -> kim lac qua lai theo tung lan doi chieu. Bo dinh sat (khong ve lo lung). Vong 3: Bay "nguon that 50 Hz, kim van lac ro"
#   (khong viet "doi chieu 50 lan/giay": 50 Hz doi chieu 100 lan/giay), dat TRUOC Rut ra. Rut ra: cuc tu doi theo chieu dong; nguon that doi chieu rat nhanh -> luc len kim doi chieu lien tuc,
#   kim rung quanh cho cu (KHONG noi "100 lan moi giay", "khong kip quay" = dap an Cau 6). Chua noi duoc = so_lieu_mau.ghi_chu
#   + mo_hinh.gia_thiet[1] (tu du, viet "sat con tu tinh chut it"). Cau chot (vong 3): doi hai dau day noi vao nguon mot chieu
#   -> kim lech sang phia kia (bai 93 khong co cau Tu kiem tra nao hoi y vay; hop exp ghi buoc dao cuc). Hop quy tac hien sau >= 4 s.
# Vat li (mo hinh): i > 0 -> dau phai loi (gan kim) la N, day dau N cua kim sang phai (lech +); i < 0 -> S, hut N sang trai.
#   Nguon cham: i = sin(2*pi*t/(2*HALF)), kim lech DEV*i (gan dung tinh). Kiem: _kiem_so(), _kiem_dong_bo() moi 0,05 s.
import math
from engine import *

U, FHZ = 6, 50                       # tham_so U (V), f (Hz)
HALF = 2.0                           # so_lieu_mau.ghi_chu: doi chieu moi 2 giay (mo hinh)
ROWS = [("dc", "một chiều", "lệch một phía"), ("slow", "đổi chiều chậm", "lắc qua lại")]   # so_lieu_mau (rut gon)
DEV = math.radians(55); JIT = math.radians(3)
WIRE = (60, 66, 92); CU = (184, 115, 51); FE = (150, 155, 170); DRED = (185, 28, 28); DGREEN = (21, 110, 55)

def pole_right(i):
    """Cuc o dau loi gan kim: i > 0 -> N, i < 0 -> S, gan 0 -> None."""
    return "N" if i > 0.15 else ("S" if i < -0.15 else None)
def kim_sign(pole):
    return {"N": 1, "S": -1}.get(pole, 0)
def i_slow(t):
    return math.sin(math.pi * t / HALF)

# ---------------- hinh dung cu ----------------
CX0, CX1, CY = 200, 760, 470
KIM = (900, 470)

def needle(d, x, y, ang, L=150, hw=16, a=1.0):
    c, s = math.cos(ang), math.sin(ang); px, py = -s * hw, c * hw
    n = (x + c * L / 2, y + s * L / 2); so = (x - c * L / 2, y - s * L / 2)
    d.polygon([(x + px, y + py), n, (x - px, y - py)], fill=A(RED, a), outline=A(NAVY, a))
    d.polygon([(x + px, y + py), so, (x - px, y - py)], fill=A(BLUE, a), outline=A(NAVY, a))
    dot(d, x, y, 7, A(WHITE, a), A(NAVY, a))

def core(d, x0, x1, y, pr, a=1.0, h=50, end=60):
    d.rectangle([x0, y - h / 2, x1, y + h / 2], fill=A(FE, a), outline=A(NAVY, a), width=3)
    if pr:
        pl = "S" if pr == "N" else "N"
        for xa, xb, p in ((x0, x0 + end, pl), (x1 - end, x1, pr)):
            d.rectangle([xa, y - h / 2, xb, y + h / 2], fill=A(RED if p == "N" else BLUE, a), outline=A(NAVY, a), width=3)
            text(d, ((xa + xb) / 2, y + 1), p, 40, WHITE, alpha=a)
    n = int((x1 - x0 - 2 * end - 40) / 30)
    for k in range(n + 1):
        x = x0 + end + 20 + k * (x1 - x0 - 2 * end - 40) / n
        d.line([(x - 8, y - h / 2 - 12), (x + 8, y + h / 2 + 12)], fill=A(CU, a), width=6)

def stand(d, x, y, dev, a=1.0, L=150, hw=16):
    d.line([(x, y), (x, y + 140)], fill=A(NAVY, a), width=6); d.line([(x - 40, y + 142), (x + 40, y + 142)], fill=A(NAVY, a), width=8)
    needle(d, x, y, -math.pi / 2 + dev, L=L, hw=hw, a=a)

def apparatus(d, src, closed, i, dev, src_a=1.0):
    card(d, (40, 260, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    pr = pole_right(i) if closed else None
    d.line([(300, 512), (300, 580)], fill=WIRE, width=5); d.line([(300, 650), (300, 720), (340, 720)], fill=WIRE, width=5, joint="curve")
    d.line([(700, 512), (700, 720), (660, 720)], fill=WIRE, width=5, joint="curve")
    dot(d, 300, 580, 8, WIRE); dot(d, 300, 650, 8, WIRE)
    if closed: d.line([(300, 650), (300, 580)], fill=NAVY, width=7)
    else: d.line([(300, 650), (352, 592)], fill=NAVY, width=7)
    text(d, (256, 615), "K", 40, NAVY)
    card(d, (340, 655, 660, 785), fill=(245, 243, 255), outline=NAVY, r=18, w=4)
    name = "một chiều" if src == "dc" else "đổi chiều chậm"
    text(d, (500, 700), name, 40, mix(BG, INK, src_a)); text(d, (500, 750), f"{U} V", 40, mix(BG, ORANGE, src_a))
    if closed and abs(i) > 0.15:          # nhanh phai: i > 0 chay tu cuon xuong
        y0, y1 = (560, 640) if i > 0 else (640, 560)
        arrow(d, (735, y0), (735, y1), RED, w=5, head=16); text(d, (770, 600), "I", 40, RED)
    core(d, CX0, CX1, CY, pr)
    stand(d, KIM[0], KIM[1], dev)

def table(d, n, hl=None, y=830):
    card(d, (40, y, 1040, y + 330), fill=WHITE, outline=LIGHT, w=3)
    XS = (300, 760)
    for x, h in zip(XS, ("Nguồn", "Kim")): text(d, (x, y + 50), h, 42, INK)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=3)
    for j, (k, a, c) in enumerate(ROWS):
        yy = y + 160 + j * 100
        if hl == j: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=(255, 237, 213))
        if j < n: text(d, (XS[0], yy), a, 44, NAVY); text(d, (XS[1], yy), c, 44, PURPLE)
        else:
            for x in XS: text(d, (x, yy), "·", 44, GRAY)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, "slow", False, 0.0, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 830 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 720), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 61), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 300, f"Nguồn đổi chiều thật chậm,\nmỗi {HALF:.0f} giây một lần (mô hình).\nKim nam châm thế nào?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 620, 940, y0 + 632], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 620, 140 + 800 * (1 - p), y0 + 632], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_C1, T_O1, T_SW, T_C2 = 0.8, 2.6, 3.0, 3.6
T_ROW1, T_ROW2 = T_C1 + 0.5, T_C2 + 2 * HALF        # hang 2 chi ghi sau khi kim da sang ca hai phia
def do_state(t):
    """-> (nguon, alpha chu, K dong?, i, goc lech kim, so hang)."""
    src = "slow" if t >= T_SW else "dc"; sa = clamp((t - T_SW) / 0.3) if t >= T_SW else 1.0
    if T_C1 <= t < T_O1:
        closed, i = True, 1.0; dev = DEV * ease((t - T_C1) / 0.45)
    elif t >= T_C2:
        closed, i = True, i_slow(t - T_C2); dev = DEV * i
    else:
        closed, i = False, 0.0; dev = DEV * (1 - ease((t - T_O1) / 0.45)) if t >= T_O1 else 0.0
    n = (1 if t >= T_ROW1 else 0) + (1 if t >= T_ROW2 else 0)
    return src, sa, closed, i, dev, n

def s_do(img, d, t, sc):
    src, sa, closed, i, dev, n = do_state(t)
    apparatus(d, src, closed, i, dev, src_a=sa)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    if sc["T"] < T_ROW2 + 1.0: bad.append(("canh do ngan", sc["T"]))
    seen = set()
    while t < sc["T"]:
        src, sa, closed, i, dev, n = do_state(t)
        sg = kim_sign(pole_right(i)) if closed else 0
        if sg and t > T_C1 + 0.5 and dev * sg <= 0: bad.append((round(t, 2), "kim sai chieu"))
        if closed and src == "slow" and sg: seen.add(sg)
        if n >= 2 and seen != {1, -1}: bad.append((round(t, 2), "ghi 'lac qua lai' truoc khi kim sang hai phia"))
        if closed and src == "dc" and not (T_C1 <= t < T_O1): bad.append((round(t, 2), "nguon lech"))
        t += 0.05
    return bad

def _kiem_so():
    bad = []
    if not (kim_sign(pole_right(1)) == -kim_sign(pole_right(-1)) != 0): bad.append("doi chieu dong phai doi phia kim")
    if abs(i_slow(HALF) ) > 1e-9 or i_slow(HALF / 2) <= 0 or i_slow(1.5 * HALF) >= 0: bad.append("chu ki nguon cham")
    if kim_sign(pole_right(-1.0)) != -kim_sign(pole_right(1.0)): bad.append("cau chot: dao day phai doi phia kim")
    if 2 * FHZ != 100: bad.append("50 Hz doi chieu 100 lan/giay")
    return bad

# ---------------- canh 3: Dap an ----------------
GX0, GX1 = 110, 990
def graph(d, y, half, x_end, a=1.0, amp=110, poles=False, cycles_w=8.0):
    """Do thi i(t) (truc t dai cycles_w giay), ve den x_end."""
    d.line([(GX0, y), (GX1, y)], fill=A(NAVY, a), width=4); d.line([(GX0, y - amp - 40), (GX0, y + amp + 40)], fill=A(NAVY, a), width=4)
    text(d, (GX0 - 40, y - amp - 20), "i", 44, NAVY, alpha=a); text(d, (GX1 + 20, y + 40), "t", 44, NAVY, alpha=a)
    pts = [(x, y - amp * math.sin(math.pi * cycles_w * (x - GX0) / (GX1 - GX0) / half)) for x in range(GX0, int(x_end) + 1, 4)]
    for x, yy in pts: d.line([(x, y), (x, yy)], fill=A(mix(WHITE, RED if yy < y else BLUE, 0.22), a), width=4)
    if len(pts) > 1: d.line(pts, fill=A(ORANGE, a), width=6)
    if poles:
        nq = int(round(cycles_w / half))
        for q in range(nq):
            xc = GX0 + (q + 0.5) * (GX1 - GX0) / nq
            if x_end >= xc:
                p = "N" if q % 2 == 0 else "S"; yc = y - amp * 0.55 if p == "N" else y + amp * 0.55
                dot(d, xc, yc, 30, A(RED if p == "N" else BLUE, a)); text(d, (xc, yc + 1), p, 40, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · lắc qua lại"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    k = appear(t, 0.4, 0.4)
    card(d, (40, 390, 1040, 1330), fill=A(WHITE, k), outline=A(TEAL, k), w=5)
    tt = clamp((t - 0.6) / 6.0) * 6.0                       # 6 s that = 1,5 chu ki, con tro chay theo
    xc = GX0 + (GX1 - GX0) * tt / 8.0
    graph(d, 600, HALF, xc, a=k)
    d.line([(xc, 450), (xc, 750)], fill=A(PURPLE, k), width=3)
    i = i_slow(tt)
    stand(d, W / 2, 960, DEV * i, a=k, L=200, hw=20)
    pr = pole_right(i)
    if pr:
        sg = kim_sign(pr)
        arrow(d, (W / 2 + sg * 140, 960), (W / 2 + sg * 260, 960), A(RED, k), w=6, head=20)
    kb = appear(t, M[1] - 0.1, 0.4)
    text(d, (W / 2, 1240), "dòng đổi chiều → kim đổi phía", 46, PURPLE, alpha=kb)

# ---------------- canh 4: Bay roi Chua noi duoc (truoc Rut ra) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    core(d, 200, 620, 410, None, h=50, end=60)
    stand(d, 800, 400, JIT * math.sin(2 * math.pi * 6 * t), L=120, hw=13)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 820), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        for j, q in enumerate((f"“Nguồn thật {FHZ} Hz,", "kim vẫn lắc rõ”")):
            yy = y0 + 210 + j * 72; lw = tw(d, q, F(50))
            text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y0 + 360), "✗", 56, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 2.2, 0.4)
        card(d, (70, y0 + 440, 1010, y0 + 760), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 600), "✓ Quá nhanh: kim chỉ rung", 54, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 700), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Theo mô hình", ""), ("• Bỏ qua: sắt còn", "chút từ tính"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 270 + j * 250), l1, 50, INK, anchor="lm", alpha=kk)
            if l2: text(d, (132, y0 + 345 + j * 250), l2, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 740), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    graph(d, 500, HALF, GX0 + (GX1 - GX0) * clamp((t - 0.4) / 1.4), a=k0, amp=130, poles=True)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 <= 0: return
    card(d, (40, 780, 1040, 1320), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=4)
    text(d, (W / 2, 850), "Nguồn thật: đổi chiều rất nhanh", 46, NAVY, alpha=k1)
    stand(d, W / 2, 1010, JIT * math.sin(2 * math.pi * 6 * t), a=k1, L=200, hw=20)
    text(d, (W / 2, 1240), "lực lên kim đổi chiều liên tục", 46, PURPLE, alpha=appear(t, M[1] + 0.8, 0.4))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.6                         # >= 4 s sau khi hien cau hoi (M0 + 0.4)
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 260, 1040, 1060), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(40)) + 52
        card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 322), "THỬ NGHĨ", 40, WHITE, alpha=k1)
        ctext(d, 460, "Đảo hai dây nối nguồn\nmột chiều. Kim lệch về đâu?", 48, INK, maxw=900,
              alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        core(d, 200, 600, 650, None, a=ka, h=46, end=56)
        stand(d, 760, 640, 0.0, a=ka, L=110, hw=12)
        text(d, (900, 640), "?", 60, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.4, 0.5)
        card(d, (110, 830, 970, 1020), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 925, "Nhìn lại lần 1 và lần 2", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 1110, 1020, 1420), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 1265, "Dòng đổi chiều:\ncực từ đổi theo", 52, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
          (do["t0"] + T_C1, "tap"), (do["t0"] + T_C2, "tap"),
          (da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (b["t0"] + b["M"][0] + 2.2, "tap"),
          (r["t0"] + r["M"][1] - 0.1, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-xoaychieu-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Dòng điện xoay chiều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kim cạnh nam châm điện", draw=s_hook, tail=0.7, caps=[
   ("Kim nam châm cạnh lõi sắt.", 3.2),
   ("Tự trả lời trước khi xem.", 4.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Lần 1: nguồn một chiều.", 3.0),
   ("Lần 2: nguồn đổi chiều chậm.", 6.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Kim đổi phía mỗi 2 giây.", 3.0),
   ("Theo từng lần dòng đổi chiều.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Có đúng không?", 3.8),
   ("Còn chưa nói được.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Cực từ đổi theo chiều dòng.", 3.4),
   ("Nhanh quá, kim chỉ kịp rung.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước khi xem.", 6.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch vật lí:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
