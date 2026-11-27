# Clip: tn-l10-moment-luc-01 - Mo cua: tac dung lam quay theo cho dat va huong luc (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-moment-luc-01.json (so lieu mo hinh, M_can = 2 N.m gia dinh; _kiem_so() doi chieu):
#   so_lieu_mau r (m) / alpha (do) / F can (N): 0,8/90/2,5 ; 0,4/90/5,0 ; 0,1/90/20,0 ; 0,8/30/5,0 ; alpha = 0: khong luc nao du.
#   tham_so F max 60 N (lan day thang vao ban le dung 60 N).
# Du doan (K10, khong nut) = hien_tuong_hay_sai[0]: day 60 N thang vao ban le -> cua co quay? (dap an: khong quay).
#   Khac Cau 4 Tu kiem tra (50 N, tinh M) ve so va cach hoi; hop exp tu hoi dung lan day nay ("xem video").
# Bay = hien_tuong_hay_sai[1]: lay r = 0,8 m lam canh tay don khi luc xien 30 do -> d that 0,4 m (khong hien phep nhan).
# Chot (ca tu suy, ghi trong so_lieu_mau.ghi_chu kho): cach ban le 0,5 m, xien 30 do -> d = 0,25 m -> F can = 8,0 N.
#   Khong trung Cau 2 hanh trang (0,4 m, 30 do -> 0,2 m), Cau 3 (12,5 N.m), thu thach (0,9 m, 60 do). 8,0 khong co trong bai.
# Khong tra loi san Cau 1 (36 N.m, 30 cm -> 120 N): man hinh khong co 36/120, khong co F = M/d.
from engine import *

DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
SKIN = (241, 200, 168)
DOOR = (214, 170, 110); DOOR_D = (150, 108, 60)
M_CAN = 2.0
ROWS = [(0.8, 90, 2.5), (0.4, 90, 5.0), (0.1, 90, 20.0), (0.8, 30, 5.0)]   # so_lieu_mau (r, alpha, F can)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-moment-luc-01.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["M_can"]["gia_tri"] == M_CAN and ts["F"]["max"] == 60
    for r, a, fc in ROWS: assert abs(M_CAN / (r * math.sin(math.radians(a))) - fc) < 1e-9
    assert abs(M_CAN / (0.5 * math.sin(math.radians(30))) - 8.0) < 1e-9          # ca chot
_kiem_so()

# ---------------- cua nhin tu tren xuong ----------------
HX, HY = 200, 640            # ban le
PXM = 800                    # px moi met -> cua 0,8 m = 640 px
LD, TH = 0.8 * PXM, 20
ALEN = 150
SWING = 15.0
UP = (0.0, -1.0)                                        # day vuong goc (tu duoi len)
XIEN = (math.cos(math.radians(30)), -math.sin(math.radians(30)))   # xien 30 do voi mat cua
VAO = (-1.0, 0.0)                                       # day doc mat cua, thang vao ban le

def door(d, th=0.0, alpha=1.0, hy=HY, lab=True):
    d.rectangle([40, hy - 18, HX - 14, hy + 18], fill=A((170, 175, 190), alpha))
    r = math.radians(th); u = (math.cos(r), -math.sin(r)); n = (math.sin(r), math.cos(r))
    P = lambda s, h: (HX + u[0] * s + n[0] * h, hy + u[1] * s + n[1] * h)
    pts = [P(0, -TH / 2), P(LD, -TH / 2), P(LD, TH / 2), P(0, TH / 2)]
    d.polygon(pts, fill=A(DOOR, alpha)); d.line(pts + [pts[0]], fill=A(DOOR_D, alpha), width=4)
    dot(d, HX, hy, 16, A(NAVY, alpha), A(WHITE, alpha))
    if lab: text(d, (HX, hy - 72), "bản lề", 55, NOTE, alpha=alpha)

def head_at(r, f, hy=HY):
    if f is UP: return (HX + r * PXM, hy + TH / 2)
    if f is VAO: return (HX + LD + 2, hy)
    return (HX + r * PXM, hy)

def push(d, head, f, alpha=1.0, col=RED):
    tail = (head[0] - f[0] * ALEN, head[1] - f[1] * ALEN)
    fx = (head[0] - f[0] * (ALEN + 50), head[1] - f[1] * (ALEN + 50))
    d.line([tail, fx], fill=A(SKIN, alpha), width=46); dot(d, fx[0], fx[1], 23, A(SKIN, alpha))
    arrow(d, tail, head, A(col, alpha), w=9, head=30)

def dash(d, p, q, col, alpha=1.0, w=5, on=18, off=12):
    L = math.dist(p, q); u = ((q[0] - p[0]) / L, (q[1] - p[1]) / L); s = 0.0
    while s < L:
        e = min(L, s + on)
        d.line([(p[0] + u[0] * s, p[1] + u[1] * s), (p[0] + u[0] * e, p[1] + u[1] * e)], fill=A(col, alpha), width=w)
        s += on + off

def goc30(d, head, alpha=1.0):
    """Danh dau goc 30 do giua luc va mat cua: keo dai mat cua + gia luc (net dut) ve phia truoc diem dat."""
    dash(d, head, (head[0] + 150, head[1]), DOOR_D, alpha, w=4)
    dash(d, head, (head[0] + XIEN[0] * 150, head[1] + XIEN[1] * 150), RED, alpha, w=4)
    R = 105; d.arc([head[0] - R, head[1] - R, head[0] + R, head[1] + R], -30, 0, fill=A(NAVY, alpha), width=5)
    a = math.radians(-15); text(d, (head[0] + 175 * math.cos(a), head[1] + 175 * math.sin(a) - 10), "30°", 55, NAVY, alpha=alpha)

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

XS = (230, 540, 850)
def table(d, n, hl=-1, last=False):
    y = 920; card(d, (60, y, 1020, y + 610), fill=WHITE, outline=NAVY, w=4)
    for x, h1, h2 in zip(XS, ("Cách bản lề", "Góc", "F cần"), ("(m)", "(với cửa)", "(N)")):
        text(d, (x, y + 62, ), h1, 55, INK); text(d, (x, y + 124), h2, 55, NOTE)
    d.line([(90, y + 166), (990, y + 166)], fill=LIGHT, width=4)
    rows = ROWS[:n] + ([(0.8, 0, None)] if last else [])
    for i, (r, ang, fc) in enumerate(rows):
        yy = y + 218 + i * 78
        if i == hl: d.rounded_rectangle([85, yy - 35, 995, yy + 35], radius=14, fill=(255, 237, 213))
        text(d, (XS[0], yy), vn(r), 55, INK); text(d, (XS[1], yy), f"{ang}°", 55, INK)
        text(d, (XS[2], yy), vn(fc) if fc is not None else "không quay", 55, BLUE if fc is not None else DRED)

# ---------------- moi lan day: 0..RAMP tang luc (mui ten nhap nhay), toi F can thi cua quay + hang bang hien ----------------
RAMP, OPEN, HOLD, BACK = 0.9, 0.4, 0.6, 0.3
def phase(x):
    if x < 0: return None, 0
    if x < RAMP: return "ramp", x / RAMP
    if x < RAMP + OPEN + HOLD: return "open", ease((x - RAMP) / OPEN)
    if x < RAMP + OPEN + HOLD + BACK: return "back", 1 - ease((x - RAMP - OPEN - HOLD) / BACK)
    return "done", 0

def one_push(d, x, r, f):
    ph, p = phase(x)
    th = SWING * p if ph in ("open", "back") else 0.0
    door(d, th)
    if ph == "ramp": push(d, head_at(r, f), f, alpha=0.55 + 0.45 * abs(math.sin(p * 9)))
    elif ph == "open": push(d, head_at(r, f), f, alpha=1 - clamp(p * 1.4))
    return ph

# ---------------- canh 1: Du doan (K10) ----------------
H_PUSH, H_VAO = 0.5, 3.0
def s_hook(img, d, t, sc):
    M = sc["M"]
    if t < H_VAO:
        one_push(d, t - H_PUSH, 0.8, UP)
    else:
        door(d); push(d, head_at(0.8, VAO), VAO, alpha=0.6 + 0.4 * abs(math.sin((t - H_VAO) * 4)))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    text(d, (930, HY - 70), "60 N", 58, RED, alpha=a)
    y0 = 900 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 220), "Đẩy 60 N thẳng vào bản lề.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 330), "Cửa có quay không?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 480, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: vuong goc, 3 cho dat ----------------
TS1 = [0.5, 3.1, 5.7]
def s_do(img, d, t, sc):
    k = max([i for i, s in enumerate(TS1) if t >= s], default=-1)
    if k < 0: door(d); table(d, 0); return
    ph = one_push(d, t - TS1[k], ROWS[k][0], UP)
    n = k + (0 if ph == "ramp" else 1)
    table(d, n, hl=n - 1 if ph in ("open", "back") else -1)

# ---------------- canh 3: xien 30 do, roi thang vao ban le ----------------
T_X, T_V, RAMP_V = 0.5, 3.6, 2.0
def s_do2(img, d, t, sc):
    if t < T_V:
        ph = one_push(d, t - T_X, 0.8, XIEN)
        if ph in ("ramp", "open", None): goc30(d, head_at(0.8, XIEN), alpha=1 if ph != "open" else 1 - clamp(phase(t - T_X)[1] * 1.4))
        n = 3 + (1 if ph not in ("ramp", None) else 0)
        table(d, n, hl=3 if ph in ("open", "back") else -1)
        return
    x = t - T_V
    door(d); push(d, head_at(0.8, VAO), VAO, alpha=0.55 + 0.45 * abs(math.sin(x * 9)) if x < RAMP_V else 1.0)
    text(d, (930, HY - 70), "60 N", 58, RED)
    table(d, 4, hl=4 if x >= RAMP_V else -1, last=x >= RAMP_V)

def _kiem_dong_bo():
    """Hang bang moi chi hien khi cua da quay (het RAMP); lan day cuoi xong truoc cuoi canh; hang 'khong quay' sau RAMP_V."""
    import copy; clip = copy.deepcopy(CLIP); build(clip); bad = []
    sc = {s["key"]: s for s in clip["scenes"]}
    if TS1[-1] + RAMP + OPEN + HOLD + BACK > sc["do"]["T"]: bad.append("do: lan cuoi qua cuoi canh")
    if T_X + RAMP + OPEN + HOLD + BACK > T_V: bad.append("do2: lan xien chua xong da day vao ban le")
    if T_V + RAMP_V + 1.2 > sc["do2"]["T"]: bad.append("do2: hang khong quay hien qua ngan")
    if H_PUSH + RAMP + OPEN + HOLD + BACK > H_VAO: bad.append("hook: lan day mau chua xong")
    if any(b - a < 2.0 for a, b in zip(TS1, TS1[1:])): bad.append("do: hai lan day cach < 2 s")
    return bad

# ---------------- canh 4: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    door(d); push(d, head_at(0.8, VAO), VAO)
    text(d, (930, HY - 70), "60 N", 58, RED)
    kg = clamp((t - 0.2) / 0.8)
    if kg > 0: dash(d, (HX + LD, HY + 34), (HX + LD - (LD + 140) * kg, HY + 34), ORANGE, w=6)
    text(d, (W / 2, HY + 130), "cánh tay đòn = 0", 58, DGREEN)
    kr = appear(t, M[1] - 0.1, 0.4)
    if kr <= 0: return
    y0 = 960 + (1 - kr) * 30
    card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pill(d, W / 2, y0 + 70, "RÚT RA", GREEN, kr)
    text(d, (W / 2, y0 + 210), "Lực × cánh tay đòn = 2 N·m", 58, DGREEN, alpha=kr)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    door(d); hd = head_at(0.8, XIEN); push(d, hd, XIEN); goc30(d, hd)
    d.line([(HX, HY + 52), (HX + LD, HY + 52)], fill=NOTE, width=3)            # khoang cach toi diem dat, doc mat cua
    for x in (HX, HX + LD): d.line([(x, HY + 36), (x, HY + 68)], fill=NOTE, width=3)
    text(d, (440, HY + 100), "0,8 m", 55, NOTE)
    text(d, (800, HY + 190), "5,0 N", 55, RED, anchor="lm")
    kv = appear(t, M[1], 0.4)
    if kv > 0:                                                    # gia luc + doan vuong goc tu ban le
        v = (HX - hd[0], HY - hd[1]); s = v[0] * XIEN[0] + v[1] * XIEN[1]
        foot = (hd[0] + XIEN[0] * s, hd[1] + XIEN[1] * s)
        dash(d, hd, (hd[0] + XIEN[0] * (s - 120), hd[1] + XIEN[1] * (s - 120)), ORANGE, kv, w=6)
        d.line([(HX, HY), foot], fill=A(GREEN, kv), width=8)
        assert abs(math.dist((HX, HY), foot) - 0.4 * PXM) < 1.0
        text(d, (foot[0] - 75, (HY + foot[1]) / 2 + 60), "0,4 m", 58, DGREEN, anchor="rm", alpha=kv)
    k3 = appear(t, M[2] - 0.1, 0.4)
    card(d, (40, 270, 1040, 530), fill=WHITE, outline=DRED, w=6)
    pill(d, W / 2, 320, "BẪY", DRED)
    q = "“Cánh tay đòn = 0,8 m”"
    ks = clamp((t - M[0] - 1.4) / 0.4); f = F(58); lw = tw(d, q, f); yy = 405
    text(d, (W / 2, yy), q, 58, mix(INK, GRAY, ks))
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85), width=6)
    if kv > 0: text(d, (W / 2, 475), "Cánh tay đòn = 0,4 m", 58, DGREEN, alpha=kv)
    if k3 > 0:
        y = 1150 + (1 - k3) * 30
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 210), "Cửa thật cần bao nhiêu N·m?", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
END_HY = 820
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 290, 1040, 1480), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 365, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 480), "Cửa trên cần 2 N·m để quay.", 58, INK, alpha=k)
    door(d, alpha=k, hy=END_HY)
    hd = head_at(0.5, XIEN, END_HY); push(d, hd, XIEN, alpha=k)
    goc30(d, hd, k)
    d.line([(HX, END_HY + 52), (hd[0], END_HY + 52)], fill=A(NOTE, k), width=3)
    for x in (HX, hd[0]): d.line([(x, END_HY + 36), (x, END_HY + 68)], fill=A(NOTE, k), width=3)
    text(d, (310, END_HY + 105), "0,5 m", 55, NOTE, alpha=k)
    text(d, (W / 2, 1180), "Lực đẩy ít nhất?", 62, DORANGE, alpha=k)
    seg_bar(d, 1310, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, do2, da, b, e = sc["hook"], sc["do"], sc["do2"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + H_PUSH + RAMP, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + s + RAMP, "tap") for s in TS1] + [(do2["t0"] + T_X + RAMP, "tap"), (do2["t0"] + T_V + RAMP_V, "buzz")]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + b["M"][0] + 1.4, "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-moment-luc-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Moment lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đẩy cửa, nhìn từ trên xuống", draw=s_hook, tail=0.2, caps=[
   ("Đẩy mép cửa: cửa quay.", 3.0),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Đẩy vuông góc với cửa", draw=s_do, tail=0.2, caps=[
   ("Tăng lực tới khi cửa vừa quay.", 3.8),
   ("Dời chỗ đẩy về gần bản lề.", 4.2)]),
 dict(key="do2", title="Đổi hướng lực", draw=s_do2, tail=0.3, caps=[
   ("Đẩy xiên 30° với mặt cửa.", 3.4),
   ("Đẩy thẳng vào bản lề.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đáp án: không quay.", 3.2),
   ("Nhân lực với khoảng cách.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.2),
   ("Kẻ vuông góc tới giá lực.", 3.6),
   ("Số liệu mô phỏng.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
