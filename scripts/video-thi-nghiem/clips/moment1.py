# Clip: tn-l10-moment-luc-01 - Mo cua: tac dung lam quay theo cho dat va huong luc (ban 1, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-moment-luc-01.json (so lieu mo hinh, M_can = 2 N.m gia dinh):
#   so_lieu_mau r (m) / alpha (do) / F can (N): 0,8/90/2,5 ; 0,4/90/5,0 ; 0,1/90/20,0 ; 0,8/30/5,0 ; alpha = 0: khong luc nao du.
#   tham_so F max 60 N (lan day thang vao ban le dung 60 N). Kiem bang ma: F = M_can/(r sin alpha) (_kiem_so()).
# Du doan (K10: chi cau hoi + hinh): day vuong goc o mep ngoai 2,5 N la cua quay; day 60 N o mep ngoai, huong thang vao ban le?
#   A. Quay, vi 60 N lon hon nhieu so voi 2,5 N [hien_tuong_hay_sai[0]] ; B. Chi quay khi day manh hon 60 N ;
#   C. Khong quay, day manh bao nhieu cung vay (DUNG).
# Bay = hien_tuong_hay_sai[1]: lay r = 0,8 m lam canh tay don khi luc xien 30 do -> d that 0,4 m (F can 5,0 N, khong phai 2,5 N).
# Cau chot (ca tu suy, ghi trong ghi_chu kho): day cach ban le 0,5 m, xien 30 do -> d = 0,25 m -> F can = 8,0 N (chua hien tren man).
# Khong tra loi san Cau 1 (nho dinh 36 N.m, 30 cm -> 120 N): man hinh khong co so 36/120, khong co F = M/d.
# Bo cuc (khac moment3 = thuoc tren ban): cua nhin tu tren xuong (ban le trai), the so doc o tren, bang 5 hang o duoi.
from engine import *

DRED = (185, 28, 28); NOTE = (60, 64, 84)
SKIN = (241, 200, 168); SKIN_D = (196, 140, 104)
DOOR = (214, 170, 110); DOOR_D = (150, 108, 60)
M_CAN = 2.0
ROWS = [(0.8, 90, 2.5), (0.4, 90, 5.0), (0.1, 90, 20.0), (0.8, 30, 5.0)]   # so_lieu_mau (r, alpha, F can)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    bad = [r for r in ROWS if abs(M_CAN / (r[0] * math.sin(math.radians(r[1]))) - r[2]) > 1e-6]
    assert not bad, bad
    assert abs(M_CAN / (0.5 * math.sin(math.radians(30))) - 8.0) < 1e-9          # ca chot
_kiem_so()

# ---------------- cua nhin tu tren xuong ----------------
HX, HY = 150, 700            # ban le
PXM = 900                    # px moi met -> cua 0,8 m = 720 px
LD, TH = 0.8 * PXM, 20       # dai, day cua (px)
ALEN = 170                   # do dai mui ten luc (chi huong; so ghi o the doc)
SWING = 15.0                 # goc mo cua khi vua quay (do)

def door(d, th=0.0, alpha=1.0):
    d.rectangle([40, HY - 16, HX - 14, HY + 16], fill=A((170, 175, 190), alpha))              # tuong trai
    d.rectangle([HX + LD + 14, HY - 16, 1040, HY + 16], fill=A((170, 175, 190), alpha))      # khung phai
    r = math.radians(th); u = (math.cos(r), -math.sin(r)); n = (math.sin(r), math.cos(r))
    P = lambda s, h: (HX + u[0] * s + n[0] * h, HY + u[1] * s + n[1] * h)
    pts = [P(0, -TH / 2), P(LD, -TH / 2), P(LD, TH / 2), P(0, TH / 2)]
    d.polygon(pts, fill=A(DOOR, alpha)); d.line(pts + [pts[0]], fill=A(DOOR_D, alpha), width=4)
    dot(d, HX, HY, 16, A(NAVY, alpha), A(WHITE, alpha))
    text(d, (HX, HY + 70), "bản lề", 44, NOTE, alpha=alpha)

def push(d, head, ang, alpha=1.0, col=RED):
    """Mui ten luc dau o 'head', huong ang (do, 0 = sang trai doc mat cua, 90 = thang len). Ngon tay sau mui ten."""
    a = math.radians(ang); f = (-math.cos(a), -math.sin(a))
    tail = (head[0] - f[0] * ALEN, head[1] - f[1] * ALEN)
    fx = (head[0] - f[0] * (ALEN + 70), head[1] - f[1] * (ALEN + 70))
    d.line([tail, fx], fill=A(SKIN, alpha), width=46); dot(d, fx[0], fx[1], 23, A(SKIN, alpha))
    arrow(d, tail, head, A(col, alpha), w=9, head=30)
    return tail, f

def head_at(r, ang):
    return (HX + r * PXM, HY + TH / 2) if ang == 90 else (HX + r * PXM + 2, HY)

def gia(d, p, f, alpha=1.0, col=GRAY, ymin=280):
    for k in range(-30, 40):
        a, b = k * 28, k * 28 + 16
        p1 = (p[0] + f[0] * a, p[1] + f[1] * a); p2 = (p[0] + f[0] * b, p[1] + f[1] * b)
        if all(30 <= q[0] <= 1050 and ymin <= q[1] <= 940 for q in (p1, p2)): d.line([p1, p2], fill=A(col, alpha), width=4)

def readout(d, l1, l2, a=1.0, col2=INK):
    card(d, (60, 280, 1020, 450), fill=A(WHITE, a), outline=A(LIGHT, a), r=26, w=3)
    text(d, (W / 2, 326), l1, 42, NOTE, alpha=a)
    text(d, (W / 2, 398), l2, 56, col2, alpha=a)

def where(r, ang): return f"{vn(r)} m · " + ("vuông góc" if ang == 90 else f"xiên {ang}°" if ang else "vào bản lề")

def table(d, n, hl=-1, last=None, note=False):
    y = 970; card(d, (60, y, 1020, y + 560), fill=WHITE, outline=NAVY, w=4)
    if note: text(d, (1000, y + 40), "số liệu mô phỏng", 40, NOTE, anchor="rm")
    xs = (230, 540, 850)
    for x, h1, h2 in zip(xs, ("Cách bản lề", "Góc", "F cần"), ("(m)", "", "(N)")):
        text(d, (x, y + 95), h1, 42, INK)
        if h2: text(d, (x, y + 143), h2, 42, INK)
    d.line([(90, y + 180), (990, y + 180)], fill=LIGHT, width=4)
    rows = ROWS[:n] + ([(0.8, 0, None)] if last is not None else [])
    for i, (r, ang, fc) in enumerate(rows):
        yy = y + 232 + i * 70
        if i == hl: d.rounded_rectangle([85, yy - 32, 995, yy + 32], radius=14, fill=(255, 237, 213))
        a = last if (fc is None) else 1.0
        text(d, (xs[0], yy), vn(r), 46, INK, alpha=a); text(d, (xs[1], yy), f"{ang}°", 46, INK, alpha=a)
        text(d, (xs[2], yy), vn(fc) if fc is not None else "không quay", 46, BLUE if fc is not None else DRED, alpha=a)

def pill(d, y, s, bg, size=40):
    pw = tw(d, s, F(size)) + 56
    card(d, (W / 2 - pw / 2, y - 33, W / 2 + pw / 2, y + 33), fill=bg, r=33)
    text(d, (W / 2, y), s, size, WHITE)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    door(d); push(d, head_at(0.8, 0), 0)
    text(d, (930, HY - 90), "60 N", 50, RED)
    readout(d, "Đẩy vuông góc ở mép ngoài:", "2,5 N là quay", a=appear(t, 0.3))
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 920 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 610), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 200), "Đẩy 60 N thẳng vào bản lề.", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 345), "Cửa thế nào?", 54, INK, alpha=a)
    text(d, (W / 2, y0 + 450), "Chọn đáp án ở khung câu hỏi", 40, NOTE, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 540, 940, y0 + 554], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 540, 140 + 800 * (1 - p), y0 + 554], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2, 3: Tien hanh ----------------
# moi lan: 0..RAMP tang dan luc ("···"), toi F can thi cua quay (so hien + hang bang cung luc), roi dong lai.
RAMP, OPEN, HOLD, BACK = 0.9, 0.4, 0.6, 0.3
TS1 = [0.5, 2.9, 5.3]          # canh do: r = 0,8 ; 0,4 ; 0,1 (vuong goc)
TS2 = [0.5]                     # canh do2: 0,8 m xien 30 ; lan 0 do tu T0 (khong quay)
T0, RAMP0 = 3.3, 1.8

def trial(t, ts):
    """-> (k lan dang lam, pha: 'ramp'|'open'|'back'|None, tien do 0..1)."""
    k = -1
    for i, s in enumerate(ts):
        if t >= s: k = i
    if k < 0: return -1, None, 0
    x = t - ts[k]
    if x < RAMP: return k, "ramp", x / RAMP
    if x < RAMP + OPEN + HOLD: return k, "open", ease((x - RAMP) / OPEN)
    return k, "back", 1 - ease((x - RAMP - OPEN - HOLD) / BACK)

def run_trial(d, t, ts, rows, n_before):
    k, ph, p = trial(t, ts)
    if k < 0:
        door(d); readout(d, "", "···"); return n_before
    r, ang, fc = rows[k]
    th = SWING * p if ph in ("open", "back") else 0.0
    door(d, th)
    if ph == "ramp":
        push(d, head_at(r, ang), ang, alpha=0.55 + 0.45 * abs(math.sin(p * 9)))
        readout(d, where(r, ang), "···", col2=NOTE)
    else:
        if ph == "open": push(d, head_at(r, ang), ang, alpha=1 - clamp(p * 1.4))
        readout(d, where(r, ang), f"F cần = {vn(fc)} N", col2=BLUE)
    return n_before + k + (0 if ph == "ramp" else 1)

def s_do(img, d, t, sc):
    n = run_trial(d, t, TS1, ROWS[:3], 0)
    k, ph, p = trial(t, TS1)
    table(d, n, hl=n - 1 if ph in ("open", "back") else -1, note=True)

def s_do2(img, d, t, sc):
    if t < T0:
        n = run_trial(d, t, TS2, ROWS[3:], 3)
        k, ph, p = trial(t, TS2)
        table(d, n, hl=n - 1 if ph in ("open", "back") else -1)
        return
    x = t - T0; p = clamp(x / RAMP0)
    door(d); push(d, head_at(0.8, 0), 0, alpha=0.55 + 0.45 * abs(math.sin(x * 9)) if p < 1 else 1.0)
    if p < 1: readout(d, where(0.8, 0), "···", col2=NOTE)
    else: readout(d, where(0.8, 0), "60 N: cửa đứng yên", col2=DRED)
    table(d, 4, last=appear(x, RAMP0, 0.3) if p >= 1 else 0)

def _kiem_dong_bo():
    """Moi 0,05 s: cua chi quay khi so F can da hien; hang bang moi = lan dang quay; lan 0 do khong bao gio quay."""
    import copy; clip = copy.deepcopy(CLIP); build(clip); bad = []
    sc = {s["key"]: s for s in clip["scenes"]}
    for key, ts in (("do", TS1), ("do2", TS2)):
        t = 0.0
        while t < sc[key]["T"]:
            if key == "do2" and t >= T0: t += 0.05; continue
            k, ph, p = trial(t, ts)
            if ph == "ramp" and p > 1: bad.append((key, round(t, 2)))
            if ph in ("open", "back") and (t - ts[k]) < RAMP: bad.append((key, round(t, 2)))
            t += 0.05
        last = ts[-1] + RAMP + OPEN + HOLD + BACK
        lim = T0 if key == "do2" else sc[key]["T"]
        if last > lim + 1e-6: bad.append((key, "lan cuoi qua cuoi canh", round(last, 2), round(lim, 2)))
    if T0 + RAMP0 + 1.0 > sc["do2"]["T"]: bad.append("lan 0 do qua sat cuoi canh")
    return bad

# ---------------- canh 4: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Không quay"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 368), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 334), lab, 42, WHITE, alpha=ka)
    door(d); tail, f = push(d, head_at(0.8, 0), 0)
    kg = appear(t, M[0] + 0.3, 0.5)
    gia(d, head_at(0.8, 0), f, alpha=kg, col=ORANGE)
    text(d, (W / 2, 850), "d = 0  →  M = F · d = 0", 52, NAVY, alpha=appear(t, M[0] + 1.4, 0.5))
    kr = appear(t, M[0] + 1.6, 0.45)
    if kr <= 0: return
    y0 = 960 + (1 - kr) * 30
    card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pw = tw(d, "RÚT RA", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(GREEN, kr), r=32)
    text(d, (W / 2, y0 + 60), "RÚT RA", 40, WHITE, alpha=kr)
    text(d, (W / 2, y0 + 185), "d lớn: lực cần nhỏ", 48, INK, alpha=kr)
    text(d, (W / 2, y0 + 300), "Giá lực qua trục: M = 0", 48, INK, alpha=kr * appear(t, M[1] + 0.4, 0.4))

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    door(d); hd = head_at(0.8, 30); tail, f = push(d, hd, 30)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    kd = appear(t, 2.4, 0.45)
    readout(d, where(0.8, 30), "F cần = 5,0 N", a=1 - kd, col2=BLUE)   # nhuong cho gia luc + doan d
    if kd > 0:                                                  # gia luc + doan d vuong goc tu ban le
        gia(d, hd, f, alpha=kd, col=ORANGE)                         # the so da mo di (a = 1 - kd)
        # chan duong vuong goc: hinh chieu ban le len gia
        v = (HX - hd[0], HY - hd[1]); s = v[0] * f[0] + v[1] * f[1]
        foot = (hd[0] + f[0] * s, hd[1] + f[1] * s)
        d.line([(HX, HY), foot], fill=A(GREEN, kd), width=7)
        mid = ((HX + foot[0]) / 2, (HY + foot[1]) / 2)
        text(d, (mid[0] + 45, mid[1] + 20), "d = 0,4 m", 48, GREEN, anchor="lm", alpha=kd)
        assert abs(math.dist((HX, HY), foot) - 0.4 * PXM) < 1.0
    if a1 > 0:
        y = 960
        card(d, (40, y, 1040, y + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Lực xiên: d = 0,8 m”"
        ks = clamp((t - 2.0) / 0.4); f2 = F(50); lw = tw(d, q, f2); yy = y + 185
        text(d, (W / 2, yy), q, 50, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        kk = a1 * appear(t, 2.6, 0.4)
        text(d, (W / 2, y + 300), "Nếu vậy chỉ cần 2,5 N", 46, INK, alpha=kk)
        text(d, (W / 2, y + 380), "Bảng: cần 5,0 N", 46, GREEN, alpha=kk)
    if k3 > 0:
        y = 960
        card(d, (40, y, 1040, y + 470), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• Bản lề cần 2 N·m: giả định", "• Lực chếch lên?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (100, y + 220 + 120 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot khong chua cong thuc giai -> THU NGHI: 0,5 m, xien 30 do (so moi); goi y tre >= 2,5 s, cau hoi trung tinh."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 420, "Cùng một lực: chỗ đặt và hướng đều quan trọng", 48, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 870, "Đẩy cách bản lề 0,5 m,\nxiên 30° với mặt cửa.\nLực ít nhất?", 46, INK,
          maxw=920, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1160, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1270, "Cánh tay đòn lần này?", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, do2, da, b, e = sc["hook"], sc["do"], sc["do2"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s + RAMP, "tap") for s in TS1] + [(do2["t0"] + s + RAMP, "tap") for s in TS2]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-moment-luc-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Moment lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đẩy cửa, nhìn từ trên xuống", draw=s_hook, tail=0.3, caps=[
   ("Bản lề ở bên trái.", 2.6),
   ("Tự đoán trước.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Tăng lực tới khi cửa vừa quay.", 3.8),
   ("Dời chỗ đẩy gần bản lề.", 3.4)]),
 dict(key="do2", title="Đổi hướng lực", draw=s_do2, tail=0.4, caps=[
   ("Đẩy xiên 30°.", 2.9),
   ("Đẩy thẳng vào bản lề.", 2.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Giá lực đi qua trục quay.", 3.4),
   ("Rút ra.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng hay sai?", 4.0),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 8.0)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
