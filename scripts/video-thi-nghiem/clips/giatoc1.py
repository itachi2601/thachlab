# Clip: tn-l10-gia-toc-01 - Cam bien ghi v cua xe lan xuong mang nghieng o 5 thoi diem cach 0,2 s (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-gia-toc-01.json:
#   so_lieu_mau: t = 0; 0,2; 0,4; 0,6; 0,8 s ; v doc = 0,20; 0,30; 0,40; 0,49; 0,59 m/s ; Dv/Dt = 0,50; 0,50; 0,45; 0,50.
#   mo_hinh: a = g.sin(alpha) = 0,49 m/s2, v0 = 0,20 m/s (chi dung de ve xe chay giua cac lan ghi; xe tu nghi
#   truoc khi ghi -v0/a = 0,41 s -> "xe da co van toc nho khi bat dau ghi" nhu cac_buoc).
#   So suy ra tu so tren man: Dv = +0,10/+0,10/+0,09/+0,10 ; bay v/t = 0,40/0,4 = 1,0 (gap doi 0,50).
#   KHONG giai cau "Doc bang: vi sao bon khoang cho Dv/Dt hoi khac nhau?" ngay sau hop trong bai: clip khong noi ve
#   lam tron, khong tinh a ca khoang 0-0,8 s (= __A_TONG__), chi tro toi cau do.
#   Cau chot: v 0,10 -> 0,70 m/s trong 0,8 s (v0 trong mien tham_so 0-0,5; a = 0,75 ung sin(alpha) = 0,077 trong mien
#   0,02-0,15) -> a = 0,75 m/s2, chua tung hien; phan xa sai v/t = 0,875.
# Khac ctbdd1 (cung mang + cam bien): ctbdd1 tha tu nghi, cong quang doi vi tri, do thi v-t qua goc o NUA DUOI.
#   Clip nay: DO THI v-t LON O TREN (truc chinh, khong qua goc, bac thang Dv), mang + cam bien chuyen dong o duoi,
#   Du doan = ngoai suy v luc 0,8 s tu hai diem dau.
# Mau: t xanh duong, v cam, Dv / Dv/Dt xanh ngoc; xanh la chi cho ket luan; do = bay.
from engine import *

T5 = (0.0, 0.2, 0.4, 0.6, 0.8)
VD = (0.20, 0.30, 0.40, 0.49, 0.59)
VS = ("0,20", "0,30", "0,40", "0,49", "0,59")
DV = ("+0,10", "+0,10", "+0,09", "+0,10")
AK = ("0,50", "0,50", "0,45", "0,50")
V0, ACC = 0.20, 0.49
C_T, C_V, C_D = BLUE, ORANGE, TEAL
CART = (100, 116, 139); CART_D = (51, 65, 85); RAIL = (203, 207, 218); RAIL_D = (148, 153, 168)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

# ---------------- do thi v-t (truc co dinh ca clip, o TREN) ----------------
GBOX = (40, 265, 1040, 1010)
GX0, GYB = 190, 925
def GXt(t): return GX0 + t * 900            # 0,8 s -> 910
def GYv(v): return GYB - v * 900            # 0,6 m/s -> 385 ; 0,1 m/s = 90 px

def graph(d, n, steps=0, dvlab=0, vlab=None, ring=(), q=False, alpha=1.0):
    vmax = 0.4 if q else 0.6                                # hook: khong vach so v tren 0,4 (khong ro dap an)
    """n diem dau; steps: so bac thang Dv ve; dvlab: so nhan Dv; vlab: cac chi so ghi so v."""
    card(d, GBOX, fill=WHITE, outline=LIGHT, w=3)
    for v in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
        if v > vmax + 1e-9: continue
        d.line([(GX0, GYv(v)), (GXt(0.8) + 20, GYv(v))], fill=(240, 236, 228), width=2)
    for t in T5[1:]: d.line([(GXt(t), GYB), (GXt(t), GYv(vmax))], fill=(240, 236, 228), width=2)
    arrow(d, (GX0, GYB), (GXt(0.8) + 80, GYB), NAVY, w=5, head=18)
    arrow(d, (GX0, GYB), (GX0, GYv(0.6) - 50), NAVY, w=5, head=18)
    for t in T5[1:]:
        d.line([(GXt(t), GYB), (GXt(t), GYB + 12)], fill=NAVY, width=3)
        text(d, (GXt(t), GYB + 44), vn(t, 1), 40, C_T, bold=False)
    for v in (0.2, 0.4, 0.6):
        if v > vmax + 1e-9: continue
        d.line([(GX0 - 12, GYv(v)), (GX0, GYv(v))], fill=NAVY, width=3)
        text(d, (GX0 - 20, GYv(v)), vn(v, 1), 40, C_V, bold=False, anchor="rm")
    text(d, (GX0 - 20, GYB + 32), "0", 40, INK, bold=False, anchor="rm")
    text(d, (1030, GYB - 62), "t (s)", 40, C_T, anchor="rm")
    text(d, (GX0 + 22, GYv(0.6) - 50), "v (m/s)", 40, C_V, anchor="lm")
    if q:                                                    # dau hoi tren truc t o 0,8 s (khong co chieu cao)
        x = GXt(0.8)
        card(d, (x - 26, GYB - 34, x + 26, GYB + 22), fill=WHITE, outline=INK, r=12, w=4)   # nam tren truc
        text(d, (x, GYB - 6), "?", 42, INK)
    for i in range(min(steps, n - 1)):                       # bac thang: ngang tu diem i, dung len diem i+1
        x0, y0 = GXt(T5[i]), GYv(VD[i]); x1, y1 = GXt(T5[i + 1]), GYv(VD[i + 1])
        for xx in range(int(x0) + 16, int(x1), 22): d.line([(xx, y0), (min(xx + 11, x1), y0)], fill=C_D, width=4)
        d.line([(x1, y0), (x1, y1 + 16)], fill=C_D, width=6)
        if i < dvlab: text(d, (x1 + 10, (y0 + y1) / 2 + 4), DV[i], 40, C_D, anchor="lm", alpha=alpha)
    for i in range(n):
        x, y = GXt(T5[i]), GYv(VD[i])
        if i in ring: d.ellipse([x - 30, y - 30, x + 30, y + 30], outline=NAVY, width=5)
        dot(d, x, y, 15, C_V, WHITE)
        if vlab is not None and i in vlab:
            if i == 0: text(d, (x + 22, y - 40), VS[i], 40, C_V, anchor="lm")
            else: text(d, (x - 22, y - 40), VS[i], 40, C_V, anchor="rm")

# ---------------- mang + cam bien (o DUOI do thi) ----------------
RBOX = (40, 1030, 1040, 1290)
R0, R1 = (90, 1150), (1010, 1198)
RL = math.hypot(R1[0] - R0[0], R1[1] - R0[1])
RU = ((R1[0] - R0[0]) / RL, (R1[1] - R0[1]) / RL); RN = (RU[1], -RU[0])
def RP(s, h): return (R0[0] + RU[0] * s + RN[0] * h, R0[1] + RU[1] * s + RN[1] * h)
P0, PXM, PSTOP = 330, 1700, 880           # px doc mang cua mep truoc xe luc bat dau ghi; px / m; chan cuoi

def rig(d, front, ping=0.0):
    card(d, RBOX, fill=WHITE, outline=LIGHT, w=3)
    d.polygon([RP(-10, -22), RP(110, -22), (RP(110, -22)[0], 1262), (RP(-10, -22)[0], 1262)], fill=(226, 220, 206))
    d.line([(60, 1262), (1020, 1262)], fill=RAIL_D, width=4)
    d.polygon([RP(0, 0), RP(RL, 0), RP(RL, -22), RP(0, -22)], fill=RAIL, outline=RAIL_D)
    d.polygon([RP(PSTOP + 6, 0), RP(PSTOP + 22, 0), RP(PSTOP + 22, 46), RP(PSTOP + 6, 46)], fill=CART_D)   # chan cuoi
    # cam bien chuyen dong o dau tren mang, mat quay ve phia xe
    d.polygon([RP(14, 4), RP(74, 4), RP(74, 64), RP(14, 64)], fill=NAVY)
    d.polygon([RP(74, 18), RP(84, 18), RP(84, 50), RP(74, 50)], fill=(120, 130, 160))
    text(d, (RP(44, 0)[0] + 10, 1058), "cảm biến", 40, INK, anchor="mm")
    if ping > 0:                                           # song do toa ra khi ghi mot so
        c = RP(84, 34)
        for k in range(3):
            r = 30 + 34 * k
            d.arc([c[0] - r, c[1] - r, c[0] + r, c[1] + r], -40, 40, fill=A(C_V, ping), width=5)
    p = min(front, PSTOP)
    d.polygon([RP(p - 150, 12), RP(p, 12), RP(p, 64), RP(p - 150, 64)], fill=CART, outline=CART_D)
    for sw in (p - 118, p - 32):
        c = RP(sw, 8); d.ellipse([c[0] - 13, c[1] - 13, c[0] + 13, c[1] + 13], fill=CART_D)

def front_at(tau):  # tau: giay that tinh tu luc bat dau ghi (am = truoc khi ghi, xe tu nghi luc -v0/a)
    tau = max(tau, -V0 / ACC)
    return P0 + (V0 * tau + 0.5 * ACC * tau * tau) * PXM

PANEL = (40, 1305, 1040, 1590)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    graph(d, 2, vlab=(0, 1), q=True)
    rig(d, front_at(0.0))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0:
        card(d, PANEL, fill=WHITE, outline=LIGHT, w=3)
        text(d, (W / 2, 1448), "v: vận tốc xe do cảm biến đo", 40, INK, bold=False)
        return
    card(d, PANEL, fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, 1322, W / 2 + pw / 2, 1386), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, 1354), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, 1448), "Lúc t = 0,8 s, v bằng bao nhiêu?", 48, INK, alpha=a)
    text(d, (W / 2, 1515), "v: vận tốc xe do cảm biến đo", 40, INK, bold=False, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, 1560, 940, 1572], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, 1560, 140 + 800 * (1 - p), 1572], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (chieu cham) ----------------
RUN0, SLOW = 0.5, 5.0                     # bat dau chay (giay canh); 1 s that = 5 s tren man
PRE = V0 / ACC                            # 0,408 s xe chay tu nghi truoc khi ghi
def tau_at(t): return (t - RUN0) / SLOW - PRE
REC_END = RUN0 + (PRE + 0.8) * SLOW       # giay canh luc ghi so cuoi

def rec_state(t):
    """-> (tau, so lan ghi k (-1 = chua ghi), so dong ho hien)"""
    tau = tau_at(t)
    if tau < -1e-9: return tau, -1, None
    k = min(4, int(tau / 0.2 + 1e-6))
    clock = min(int(tau * 100 + 1e-6), 80)
    return tau, k, clock

def s_do(img, d, t, sc):
    tau, k, clock = rec_state(t)
    n = k + 1
    graph(d, n, steps=max(0, n - 1), dvlab=max(0, n - 1), vlab=range(n))
    ping = 0.0
    if k >= 0: ping = 1.0 - clamp((tau - 0.2 * k) * SLOW / 0.6)
    rig(d, front_at(tau) if t >= RUN0 else front_at(-PRE), ping)
    # chip nhac cau hoi du doan (trong khung do thi, goc duoi phai)
    chip = "Nhớ: v lúc 0,8 s?"
    cw = tw(d, chip, F(40)) + 44
    card(d, (1010 - cw, 766, 1010, 828), fill=(245, 243, 255), outline=PURPLE, r=30, w=3)   # vung trong duoi bac thang
    text(d, (1010 - cw / 2, 797), chip, 40, PURPLE)
    # dong ho chay (tach rieng bang so doc)
    text(d, (1010, 1062), "đồng hồ: " + ("–" if clock is None else vn(clock / 100, 2) + " s"), 40, C_T, anchor="rm")
    # bang so doc
    card(d, PANEL, fill=NAVY, r=22)
    cols = ((210, "lần ghi t (s)", "–" if k < 0 else vn(T5[k], 1), C_T),
            (530, "v đọc (m/s)", "–" if k < 0 else VS[k], C_V),
            (850, "Δv (m/s)", DV[k - 1] if k >= 1 else "–", C_D))
    for cx, h, val, col in cols:
        text(d, (cx, 1360), h, 40, (220, 225, 240), bold=False)
        text(d, (cx, 1440), val, 56, mix(col, WHITE, 0.45))
    text(d, (770, 1530), "Δv = v mới − v trước", 40, (220, 225, 240), bold=False)
    text(d, (230, 1530), "chưa ghi" if k < 0 else "chiếu chậm", 40, (220, 225, 240), bold=False)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    graph(d, 5, steps=4, dvlab=4, vlab=range(5), ring=(4,) if t > 0.5 else ())
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · khoảng 0,60 m/s"
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    pw = tw(d, lb, F(42)) + 56
    card(d, (W / 2 - pw / 2, 1060, W / 2 + pw / 2, 1132), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 1096), lb, 42, WHITE, alpha=ka)
    k1 = appear(t, 0.7, 0.45)
    text(d, (W / 2, 1220), "Đo được: v = 0,59 m/s", 50, C_V, alpha=k1)
    k2 = appear(t, M[0] + 1.6, 0.5)
    card(d, (80, 1290, 1000, 1550), fill=A((236, 253, 243), k2), r=24)
    text(d, (W / 2, 1370), "Mỗi 0,2 s, v tăng thêm", 46, GREEN, alpha=k2)
    text(d, (W / 2, 1460), "gần như cùng một lượng", 46, GREEN, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    graph(d, 5, steps=4, dvlab=4, vlab=range(5))
    if t < M[2] - 0.1:
        card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
        text(d, (90, 1085), "Δt = 0,2 s", 40, C_T, anchor="lm")
        text(d, (90, 1150), "Δv/Δt (m/s²)", 42, C_D, anchor="lm")
        for i in range(4):                                  # moi gia tri dat duoi giua khoang tuong ung tren do thi
            ki = appear(t, 0.5 + 0.35 * i, 0.35)
            xm = (GXt(T5[i]) + GXt(T5[i + 1])) / 2
            text(d, (xm, 1222), AK[i], 46, C_D, alpha=ki)
        kb = appear(t, M[1] - 0.1, 0.45)
        if kb > 0:
            card(d, (80, 1275, 1000, 1435), fill=A((236, 253, 243), kb), r=24)
            text(d, (W / 2, 1325), "→ nhanh dần đều", 42, GREEN, alpha=kb)
            text(d, (W / 2, 1393), "a = Δv/Δt: gia tốc", 42, GREEN, alpha=kb)
    else:
        k2 = appear(t, M[2] - 0.1, 0.45)
        card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, 1100), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[2] + 0.3, 0.4)
        card(d, (80, 1160, 1000, 1550), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, 1290), "Mới có một xe, một độ nghiêng:", 46, RED, alpha=kk)
        text(d, (W / 2, 1410), "nghiêng hơn thì a ra sao?", 46, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
    text(d, (W / 2, y0 + 175), "Lúc t = 0,4 s: v = 0,40 m/s", 46, INK, alpha=a1)
    L1 = 640; L05 = L1 * 0.50 / 1.0                         # hai thanh dung ti le 1,0 : 0,50
    bx = 100; yA, yB = y0 + 360, y0 + 640
    ka = appear(t, M[0] + 0.3, 0.4)
    text(d, (bx, yA - 60), "v/t = 0,40 / 0,4", 46, RED, anchor="lm", alpha=ka)
    if ka > 0.05: d.rectangle([bx, yA, bx + L1 * ka, yA + 64], fill=A((252, 165, 165), ka))
    text(d, (bx + L1 + 20, yA + 32), "1,0 m/s²", 46, RED, anchor="lm", alpha=ka)
    kb = appear(t, M[0] + 1.0, 0.4)
    text(d, (bx, yB - 60), "Δv/Δt = (0,40 − 0,30) / 0,2", 46, C_D, anchor="lm", alpha=kb)
    if kb > 0.05: d.rectangle([bx, yB, bx + L05 * kb, yB + 64], fill=A(C_D, kb))
    text(d, (bx + L05 + 20, yB + 32), "0,50 m/s²", 46, C_D, anchor="lm", alpha=kb)
    kk = appear(t, M[0] + 2.2, 0.5)
    card(d, (90, y0 + 900, 990, y0 + 1250), fill=A((254, 242, 242), kk), r=24)
    text(d, (W / 2, y0 + 1000), "v/t gấp đôi Δv/Δt", 50, RED, alpha=kk)
    text(d, (W / 2, y0 + 1110), "v/t tính cả 0,20 có sẵn, Δv thì không", 42, INK, alpha=kk)
    kv = appear(t, M[0] + 2.6, 0.4)                         # dau dung tre >= 2 s sau phu de cau hoi
    if kv > 0:
        cx, cy = bx + L05 + 300, yB + 32
        d.line([(cx - 22, cy), (cx - 6, cy + 18), (cx + 26, cy - 22)], fill=A(GREEN, kv), width=9)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):                       # goi y tre ~3,7 s sau cau hoi
        kh = appear(t, M[0] + 3.7, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Nhớ lại cảnh Bẫy", 42, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Nhanh dần đều: v tăng đều theo thời gian",
             "Xe khác: v từ 0,10 lên 0,70 m/s sau 0,8 s. Gia tốc a?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for i in range(5): cs.append((do["t0"] + RUN0 + (PRE + 0.2 * i) * SLOW, "tap"))   # moi lan cam bien ghi so
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-gia-toc-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động biến đổi. Gia tốc · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe lăn xuống máng nghiêng", draw=s_hook, tail=0.8, caps=[
   ("Cảm biến ghi v mỗi 0,2 s.", 3.0),
   ("Dừng video, chọn câu trả lời.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Chiếu chậm: xe chạy, rồi mới ghi.", 3.2),
   ("Xem v tăng thêm bao nhiêu.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So bốn bậc Δv trên đồ thị.", 4.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Chia Δv cho Δt từng khoảng.", 3.0),
   ("Bốn số gần bằng nhau.", 3.6),
   ("Còn điều chưa biết.", 3.8)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.6, caps=[
   ("Lấy v chia t có được không?", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Dừng video, tự trả lời.", 6.2)]),
])
