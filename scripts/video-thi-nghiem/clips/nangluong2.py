# Clip: tn-l11-nang-luong-dien-02 - Kiem nhan 12 V - 21 W cua den xe may bang von ke va ampe ke (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nang-luong-dien-02.json:
#   so_lieu_mau (U V, I A, P = UI W, R = U/I Ohm): 12,0 1,75 21,0 6,86 ; 9,0 1,55 13,95 5,81 ; 6,0 1,30 7,8 4,62
#   rut_ra: R sang ~ 6,9 Ohm (bai ghi do mo ~ 4,6 Ohm); tham_so U_dm 12 V, P_dm 21 W.
#   Bay 2 = hien_tuong_hay_sai[1]: coi R = U_dm^2/P_dm khong doi -> P(6 V) = 21.(6/12)^2 = 5,25 W (do that 7,80 W).
#   Chua noi duoc = sai_so_thuong_gap[1]: dong trong vai giay dau khi vua bat (so doc luc da on dinh).
#   Du doan: den 12 V - 21 W o 6,0 V tieu thu khoang bao nhieu? (dap an khoang 8 W; nhieu: 21 / 10 / 5 W).
#   Cau hoi chot: den 9 V - 4,5 W sang binh thuong -> I = P/U = 0,5 A (chua tung hien; phan xa sai U/P = 2 A
#   hoac lay 1,55 A cua hang 9,0 V).
# Mach (vat li): nguon (+) o tren -> day tren -> AMPE KE NOI TIEP -> den -> day duoi -> (-). VON KE SONG SONG voi den
#   (nhanh ben phai, hai diem noi tren/duoi den). Mui ten I quy uoc chieu + -> mach ngoai -> -. Nguon o 0 V: hai
#   dong ho chi 0, den tat. Luc xoay num: hai dong ho hien "· · ·" (khong hien so thoang qua), xoay xong hai so chi +
#   do sang den + hang bang doi CUNG luc (kiem bang ma moi 0,05 s: _kiem_dong_bo()).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh 12 / 9 / 6 V (bang U-I-P) + "Dap an · khoang 8 W" ->
#       Rut ra (P = UI dung nhan o 12 V; R = U/I sang 6,9 / do mo 4,6; Chua noi duoc) -> Bay (thanh P o 6,0 V) ->
#       Chot + cau hoi tu nho lai.
from engine import *

ROWS = [(12.0, 1.75), (9.0, 1.55), (6.0, 1.30)]                 # so_lieu_mau (U, I)
P_DM, U_DM = 21.0, 12.0
def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")
def P_of(i): return ROWS[i][0] * ROWS[i][1]
BODY = (70, 78, 100); SCR = (220, 240, 225); WIRE = (60, 66, 90); DRED = (185, 28, 28)
OFF = (205, 208, 215)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
XL, XR, YT, YB = 130, 700, 400, 820          # vong mach chinh
XV, YJ1, YJ2 = 920, 460, 760                 # nhanh von ke + hai diem noi
AMC, VMC, LC = (400, YT), (XV, 610), (XR, 610)

def knob_ang(u): return math.radians(-225 + 270 * u / 15)   # thang 0-15 V

def meter(d, c, reading, name, horiz):
    cx, cy = c
    card(d, (cx - 100, cy - 66, cx + 100, cy + 66), fill=BODY, r=18)
    card(d, (cx - 86, cy - 54, cx + 86, cy + 12), fill=SCR, r=10)
    text(d, (cx, cy - 21), reading, 44, (20, 60, 30))
    text(d, (cx, cy + 38), name, 40, WHITE, bold=False)

def lamp(d, b):
    """b = P/P_dm (0 = tat). Do sang + mau day toc theo cong suat."""
    cx, cy = LC
    if b > 0:
        for k in range(6, 0, -1):
            r = 66 + (40 + 150 * b) * k / 6
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(YELLOW, 0.10 * b * (7 - k) / 6 + 0.02 * b))
    glass = OFF if b <= 0 else mix((255, 236, 200), (255, 245, 170), b)
    d.ellipse([cx - 66, cy - 66, cx + 66, cy + 66], fill=glass, outline=NAVY, width=5)
    fil = GRAY if b <= 0 else mix((200, 60, 30), (255, 200, 40), clamp((b - 0.3) / 0.7))
    pts = [(cx, cy - 66), (cx, cy - 34)] + [(cx + (22 if i % 2 else -22), cy - 26 + i * 13) for i in range(5)] + \
          [(cx, cy + 34), (cx, cy + 66)]
    d.line(pts, fill=fil, width=6, joint="curve")

def circuit(d, u, ra, rv, b, tag=True, cur=True):
    """u = vi tri num (V); ra/rv = chuoi so chi ampe ke/von ke; b = do sang den 0..1."""
    w = 7
    # vong chinh (bo qua cho dong ho, den)
    d.line([(XL, 500), (XL, YT), (AMC[0] - 100, YT)], fill=WIRE, width=w, joint="curve")
    d.line([(AMC[0] + 100, YT), (XR, YT), (XR, LC[1] - 66)], fill=WIRE, width=w, joint="curve")
    d.line([(XR, LC[1] + 66), (XR, YB), (XL, YB), (XL, 760)], fill=WIRE, width=w, joint="curve")
    # nhanh von ke song song voi den
    d.line([(XR, YJ1), (XV, YJ1), (XV, VMC[1] - 66)], fill=WIRE, width=w, joint="curve")
    d.line([(XV, VMC[1] + 66), (XV, YJ2), (XR, YJ2)], fill=WIRE, width=w, joint="curve")
    for y in (YJ1, YJ2): dot(d, XR, y, 12, WIRE)
    # nguon chinh duoc
    card(d, (40, 500, 220, 760), fill=WHITE, outline=NAVY, r=20, w=5)
    text(d, (130, 550), "nguồn", 40, INK, bold=False)
    dot(d, 130, 650, 46, (225, 228, 236), outline=NAVY)
    a = knob_ang(u); d.line([(130, 650), (130 + 38 * math.cos(a), 650 + 38 * math.sin(a))], fill=RED, width=8)
    dot(d, XL, 500, 11, RED); dot(d, XL, 760, 11, (30, 30, 36))
    text(d, (176, 466), "+", 48, RED); text(d, (176, 796), "−", 52, INK)
    # dong ho + den
    meter(d, AMC, ra, "ampe kế", True)
    meter(d, VMC, rv, "vôn kế", False)
    lamp(d, b)
    if tag:
        card(d, (360, 578, 622, 642), fill=WHITE, outline=ORANGE, r=18, w=4)
        text(d, (491, 610), "12 V – 21 W", 40, ORANGE)
    if cur and b > 0:   # chieu dong quy uoc: (+) -> day tren -> den -> (-)
        arrow(d, (540, YT), (630, YT), RED, w=7, head=24)
        text(d, (585, 360), "I", 40, RED)

def table(d, n, y=1000, hl=None):
    card(d, (60, y, 1020, y + 400), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 520, 820)
    for x, c in zip(xs, ("U (V)", "I (A)", "P = UI (W)")): text(d, (x, y + 52), c, 40, INK)
    d.line([(90, y + 94), (990, y + 94)], fill=LIGHT, width=4)
    for i in range(3):
        yy = y + 160 + i * 84
        if i < n:
            if hl == i: d.rounded_rectangle([80, yy - 38, 1000, yy + 38], radius=18, fill=(255, 237, 213))
            uu, ii = ROWS[i]
            text(d, (xs[0], yy), vn(uu, 1), 46, INK); text(d, (xs[1], yy), vn(ii, 2), 46, INK)
            text(d, (xs[2], yy), vn(P_of(i), 2), 46, BLUE)
        else:
            for x in xs: text(d, (x, yy), "·", 46, GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
Q_AT = 1.4
def s_hook(img, d, t, sc):
    circuit(d, 0, "0,00 A", "0,0 V", 0)
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 980 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 260, "Chỉnh nguồn để vôn kế chỉ 6,0 V.\nĐèn tiêu thụ khoảng\nbao nhiêu oát?", 50, INK, maxw=900,
          alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 458, 940, y0 + 470], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 458, 140 + 800 * (1 - p), y0 + 470], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 muc U trong MOT canh) ----------------
TURN = 0.6
def steps(sc):   # luc bat dau xoay num toi muc k (xoay xong -> so chi + den + hang bang)
    M = sc["M"]
    return [0.3, M[1] + 0.3, M[1] + 3.0]

def do_state(t, sc):
    """-> (u num, so chi ampe, so chi von, do sang, so hang da ghi, hang dang chi hoac None)."""
    st = steps(sc); k = -1
    for j, s0 in enumerate(st):
        if t >= s0: k = j
    if k < 0:
        return 0.0, "0,00 A", "0,0 V", 0.0, 0, None
    s0 = st[k]; u_from = 0.0 if k == 0 else ROWS[k - 1][0]; u_to = ROWS[k][0]
    if t < s0 + TURN:                                    # dang xoay: khong hien so thoang qua
        x = ease((t - s0) / TURN)
        b0 = 0.0 if k == 0 else P_of(k - 1) / P_DM
        return lerp(u_from, u_to, x), "· · ·", "· · ·", lerp(b0, P_of(k) / P_DM, x), k, None
    return u_to, vn(ROWS[k][1], 2) + " A", vn(u_to, 1) + " V", P_of(k) / P_DM, k + 1, k

ANS_DL = 0.8
def s_do(img, d, t, sc):
    u, ra, rv, b, n, cur = do_state(t, sc)
    circuit(d, u, ra, rv, b)
    table(d, n, hl=cur)
    st = steps(sc)
    ka = appear(t, st[2] + TURN + ANS_DL, 0.15)
    if ka > 0:
        card(d, (150, 862, 930, 958), fill=A((21, 110, 52), ka), outline=A(WHITE, ka), r=30, w=4)
        text(d, (W / 2, 910), "ĐÁP ÁN · khoảng 8 W", 46, WHITE, alpha=ka)

def _kiem_dong_bo():
    """Moi 0,05 s: von ke = muc num khi khong xoay; ampe ke, do sang, hang cuoi bang cung mot hang; P = U.I."""
    clip = dict(CLIP); clip["scenes"] = [dict(s) for s in CLIP["scenes"]]; build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        u, ra, rv, b, n, cur = do_state(t, sc)
        if cur is not None:
            U, I = ROWS[cur]
            ok = (rv == vn(U, 1) + " V" and abs(u - U) < 1e-9 and ra == vn(I, 2) + " A"
                  and abs(b - U * I / P_DM) < 1e-9 and n == cur + 1)
            if not ok: bad.append(round(t, 2))
        elif ra != "· · ·" and not (ra == "0,00 A" and rv == "0,0 V" and b == 0): bad.append(round(t, 2))
        t += 0.05
    for (U, I), (p, r) in zip(ROWS, ((21.0, 6.86), (13.95, 5.81), (7.8, 4.62))):
        if abs(U * I - p) > 0.005 or abs(U / I - r) > 0.005: bad.append(("so", U))
    return bad

# ---------------- canh 3: Rut ra + Chua noi duoc ----------------
def mini_lamp(d, cx, cy, b, al):
    """Den nho: b = P/P_dm."""
    for k in range(4, 0, -1):
        r = 30 + (14 + 50 * b) * k / 4
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(YELLOW, al * (0.10 * b * (5 - k) / 4 + 0.02 * b)))
    glass = mix((255, 236, 200), (255, 245, 170), b)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=A(glass, al), outline=A(NAVY, al), width=4)
    fil = mix((200, 60, 30), (255, 200, 40), clamp((b - 0.3) / 0.7))
    d.line([(cx - 14, cy + 10), (cx - 7, cy - 10), (cx, cy + 10), (cx + 7, cy - 10), (cx + 14, cy + 10)],
           fill=A(fil, al), width=5, joint="curve")

def s_rut(img, d, t, sc):
    M = sc["M"]
    k1, k2, k3 = appear(t, 0.3, 0.45), appear(t, M[1] + 0.1, 0.45), appear(t, M[2] + 0.1, 0.45)
    if k1 > 0:
        y = 400 + (1 - k1) * 30
        card(d, (60, y, 1020, y + 190), fill=A(WHITE, k1), outline=A(GREEN, k1), w=6)
        text(d, (W / 2, y + 95), "12,0 V × 1,75 A = 21 W", 56, GREEN, alpha=k1)
    if k2 > 0:
        y = 650 + (1 - k2) * 30
        card(d, (60, y, 1020, y + 360), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=6)
        text(d, (W / 2, y + 66), "R = U / I", 52, ORANGE, alpha=k2)
        for yy, b, lab, val in ((y + 175, P_of(0) / P_DM, "12 V", "≈ 6,9 Ω"), (y + 285, P_of(2) / P_DM, "6 V", "≈ 4,6 Ω")):
            mini_lamp(d, 210, yy, b, k2)
            text(d, (380, yy), lab, 46, INK, alpha=k2); text(d, (740, yy), val, 50, ORANGE, alpha=k2)
    if k3 > 0:
        y = 1080 + (1 - k3) * 30
        card(d, (60, y, 1020, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 66), "Chưa nói được", 46, NAVY, alpha=k3)
        ctext(d, y + 205, "Dòng vài giây đầu khi vừa bật\n(chưa ổn định)", 48, INK, maxw=900, alpha=k3)

# ---------------- canh 4: Bay (thanh cong suat o 6,0 V) ----------------
BX0, BXW = 140, 700
def bar(d, y, label, val, col, k, cross=False, kx=0.0):
    if k <= 0: return
    text(d, (BX0, y), label, 42, INK, anchor="lm", alpha=k)
    L = BXW * val / P_DM * ease(k)
    d.rounded_rectangle([BX0, y + 32, BX0 + max(L, 8), y + 112], radius=14, fill=A(col, k))
    text(d, (BX0 + L + 20, y + 72), vn(val, 2 if val < 10 else 0) + " W", 44, MUTED if col == GRAY else col, anchor="lm", alpha=k)
    if cross and kx > 0:
        text(d, (960, y), "✗", 64, DRED, alpha=kx)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.1, 0.4)
    text(d, (W / 2, 390), "Đèn 12 V – 21 W đặt ở 6,0 V", 46, INK, alpha=k0)
    k1 = appear(t, 0.2, 0.4)
    bar(d, 520, "Tưởng: vẫn đúng nhãn", 21.0, GRAY, k1, cross=True, kx=clamp((t - 1.3) / 0.4))
    k2 = appear(t, M[1] - 0.1, 0.4)
    bar(d, 760, "Coi R không đổi", 21.0 * (6.0 / U_DM) ** 2, ORANGE, k2, cross=True, kx=clamp((t - M[1] - 1.4) / 0.4))
    k3 = appear(t, M[1] + 0.9, 0.4)
    bar(d, 1000, "Đo thật: 6,0 V × 1,30 A", P_of(2), GREEN, k3)
    k4 = appear(t, M[1] + 1.8, 0.4)
    if k4 > 0:
        card(d, (100, 1220, 980, 1350), fill=A((255, 241, 242), k4), outline=A(DRED, k4), r=24, w=4)
        text(d, (W / 2, 1285), "Dây tóc nguội: R nhỏ hơn 6,9 Ω", 44, DRED, alpha=k4)

# ---------------- canh 5: Chot + cau hoi tu nho lai (goi y tre ~2,5 s) ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: den 9 V - 4,5 W sang binh thuong -> I = 0,5 A."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 430, 1020, 690), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 560, "Công suất đèn đổi theo U,\nkhông cố định như số trên nhãn", 50, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 750, 1040, 1410), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 780, W / 2 + pw / 2, 844), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 812), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 990, "Đèn 9 V – 4,5 W\nđang sáng bình thường.\nAmpe kế chỉ bao nhiêu?", 48, INK, maxw=920,
          alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1180, 970, 1380), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1225, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1310, "Ghi trên đèn cho biết những gì?", 46, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    st = steps(do)
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + s + TURN, "tick") for s in st[:2]]
    out += [(do["t0"] + st[2] + TURN + ANS_DL, "ding"), (r["t0"] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-nang-luong-dien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Công suất điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kiểm nhãn đèn xe máy", draw=s_hook, tail=0.8, caps=[
   ("Đèn xe máy, nguồn chỉnh được.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.4, caps=[
   ("Chỉnh tới 12,0 V, đọc ampe kế.", 3.4),
   ("Hạ xuống 9,0 V rồi 6,0 V.", 5.5)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("Ở 12 V, P = UI khớp nhãn.", 3.0),
   ("Dây tóc nguội, điện trở nhỏ hơn.", 3.8),
   ("Số đọc lúc đã ổn định.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.8, caps=[
   ("Bẫy 1: luôn là 21 W.", 3.2),
   ("Bẫy 2: R không đổi ở mọi U.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 8.0)]),
])

if __name__ == "__main__":
    print("lệch:", _kiem_dong_bo() or "không")
