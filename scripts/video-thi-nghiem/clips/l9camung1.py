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
    text(d, ((CL + CRR) / 2, CY - CR - 40), "cuộn dây", 40, mix(ORANGE, INK, 0.3))

def magnet(d, tip):
    x0, xm = tip - ML, tip - ML / 2
    d.rounded_rectangle([x0, CY - MH / 2, xm, CY + MH / 2], radius=10, fill=BLUE)
    d.rounded_rectangle([xm, CY - MH / 2, tip, CY + MH / 2], radius=10, fill=RED)
    d.rectangle([xm - 10, CY - MH / 2, xm, CY + MH / 2], fill=BLUE)
    d.rectangle([xm, CY - MH / 2, xm + 10, CY + MH / 2], fill=RED)
    text(d, (x0 + ML / 4, CY + 1), "S", 50, WHITE)
    text(d, (tip - ML / 4, CY + 1), "N", 50, WHITE)

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
        if big: text(d, (GX + (GR + 32) * math.sin(a), GY - (GR + 32) * math.cos(a)), str(abs(int(v))), 38, NAVY)
    text(d, (920, 1180), "mA", 38, MUTED, bold=False, anchor="rm")
    text(d, (165, 1180), "điện kế", 38, MUTED, bold=False, anchor="lm")
    if ghost is not None and abs(ghost - i) > 0.1:
        d.line([(GX, GY), needle_xy(ghost, GR - 8)], fill=A(GRAY, 0.8), width=5)
    d.line([(GX, GY), needle_xy(i, GR - 8)], fill=RED, width=9)
    dot(d, GX, GY, 16, NAVY)
    sh = peak if (peak and abs(i) >= 0.5 * abs(peak)) else 0.0      # so nhay thang 0 <-> dinh
    if abs(sh) > 0.05: text(d, (GX, 1256), vn(abs(sh)) + " mA", 48, RED if sh > 0 else BLUE)
    else: text(d, (GX, 1256), "0 mA", 48, MUTED)

def vlabel(d, s):
    if s: text(d, (FAR - ML / 2 + 130, CY - 110), s, 44, PURPLE)

def apparatus(d, tip, i, ghost=None, vtxt="", peak=None):
    coil_back(d); magnet(d, tip); coil_front(d); wires(d); galvo(d, i, ghost, peak); vlabel(d, vtxt)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.6
def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, FAR, 0.0)
    text(d, (160, 1250), "(tuỳ cách nối)", 38, MUTED, bold=False, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1320 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 84), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 53), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 136), "Đưa N lại gần: kim lệch phải.", 42, INK, alpha=a)
    text(d, (W / 2, y0 + 206), "Kéo N ra xa: kim sẽ thế nào?", 46, PURPLE, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 262, 940, y0 + 274], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 262, 140 + 800 * (1 - p), y0 + 274], radius=6, fill=A(PURPLE, a))

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

# ---------------- canh 3: Dap an + Rut ra ----------------
def mini(d, box, v, k):
    x0, y0, x1, y1 = box
    card(d, box, fill=A(WHITE, k), outline=A(RED if v > 0 else BLUE, k), w=4)
    text(d, ((x0 + x1) / 2, y0 + 46), "Lại gần" if v > 0 else "Ra xa", 42, INK, alpha=k)
    mx, my = (x0 + x1) / 2, y0 + 160          # nam cham nho (< 60 px: chi hai mau, khong chu)
    d.rounded_rectangle([mx - 120, my - 24, mx, my + 24], radius=8, fill=A(BLUE, k))
    d.rounded_rectangle([mx, my - 24, mx + 120, my + 24], radius=8, fill=A(RED, k))
    if v > 0: arrow(d, (mx - 90, my - 58), (mx + 90, my - 58), A(PURPLE, k), w=6, head=20)
    else: arrow(d, (mx + 90, my - 58), (mx - 90, my - 58), A(PURPLE, k), w=6, head=20)
    cx, cy, r = (x0 + x1) / 2, y1 - 40, 150     # mat so nho
    d.arc([cx - r, cy - r, cx + r, cy + r], 270 - 50, 270 + 50, fill=A(NAVY, k), width=4)
    d.line([(cx, cy - r - 10), (cx, cy - r + 14)], fill=A(NAVY, k), width=4)
    a = math.radians(40 * (1 if v > 0 else -1))
    d.line([(cx, cy), (cx + (r - 10) * math.sin(a), cy - (r - 10) * math.cos(a))], fill=A(RED, k), width=7)
    dot(d, cx, cy, 10, A(NAVY, k))

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · lệch trái"
    pw = tw(d, lab, F(44)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 338), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 300), lab, 44, WHITE, alpha=ka)
    mini(d, (60, 380, 525, 820), +1, appear(t, 0.5, 0.4))
    mini(d, (555, 380, 1020, 820), -1, appear(t, 0.9, 0.4))
    k2 = appear(t, 1.4, 0.45)
    if k2 > 0:
        card(d, (40, 870, 1040, 1080), fill=A(WHITE, k2), outline=A(PURPLE, k2), w=5)
        text(d, (W / 2, 975), "Ngược phía với lúc lại gần", 48, PURPLE, alpha=k2)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 1130, 1040, 1420), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1210), "Nam châm và cuộn dây", 50, GREEN, alpha=k1)
        text(d, (W / 2, 1290), "chuyển động đối với nhau", 50, GREEN, alpha=k1)
        text(d, (W / 2, 1370), "→ có dòng điện", 50, GREEN, alpha=k1)

# ---------------- canh 4: Bay + Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    apparatus(d, (FAR + NEAR) / 2, -I_DUA, vtxt="← ra xa", peak=-I_DUA)
    k2 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 1320
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 84), fill=A(RED, a1), r=31)
        text(d, (W / 2, y0 + 53), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        q = "“Kéo ra xa, kim lệch cùng phía”"
        lw = tw(d, q, F(42)); yy = y0 + 140
        text(d, (W / 2, yy), q, 42, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        text(d, (W / 2, y0 + 228), "✓ Ra xa: lệch phía ngược lại", 44, GREEN, alpha=a1 * appear(t, M[0] + 2.2, 0.4))
    if k2 > 0:
        y0 = 1320
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 56), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, s in enumerate(("• Vì sao có dòng?", "• Số trên kim chỉ minh hoạ")):
            text(d, (90, y0 + 140 + j * 84), s, 42, INK, bold=False, anchor="lm", alpha=k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4))

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.0
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(38)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
        ctext(d, 820, "Đưa N lại gần, ra xa liên tục.\nKim thế nào?", 46, INK, maxw=920,
              alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        mx, my = 540, 1080
        d.rounded_rectangle([mx - 130, my - 30, mx, my + 30], radius=8, fill=A(BLUE, ka))
        d.rounded_rectangle([mx, my - 30, mx + 130, my + 30], radius=8, fill=A(RED, ka))
        arrow(d, (mx - 40, my - 80), (mx + 120, my - 80), A(PURPLE, ka), w=6, head=20)
        arrow(d, (mx + 40, my + 80), (mx - 120, my + 80), A(PURPLE, ka), w=6, head=20)
        text(d, (mx + 300, my), "?", 72, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.9, 0.5)
        card(d, (110, 1260, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1380, "Mỗi lần lệch phía nào?", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 410, "Nam châm và cuộn dây chuyển động đối với nhau → có dòng cảm ứng", 46, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    cs += [(do["t0"] + t0, "tap") for t0, *_ in moves(do)]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l9-camung-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nam châm và cuộn dây", draw=s_hook, tail=THINK_END, caps=[
   ("Cuộn dây kín nối điện kế.", 3.0),
   ("Tự trả lời trước khi xem.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Nam châm đứng yên trước cuộn dây.", 3.8),
   ("Đưa lại gần trong 1 giây.", 3.6),
   ("Kéo ra xa trong 1 giây.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Ngược phía với lúc lại gần.", 3.6),
   ("Đó là dòng điện cảm ứng.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Có đúng không?", 4.4),
   ("Chưa nói được.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.8, caps=[
   ("Tự trả lời trước gợi ý.", 6.8)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch vật lí:", _kiem_vat_li() or "không")
