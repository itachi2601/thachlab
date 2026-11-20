# Clip: tn-l10-luc-ma-sat-01 - Ma sat nghi cuc dai va ma sat truot: so luc ke theo thoi gian (lo 7, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-luc-ma-sat-01.json:
#   so_lieu_mau hang 1 (hop 0,20 kg, N = 1,96 N): nghi cuc dai 0,7 N, truot 0,6 N ; hang 3 (0,60 kg): 2,1 N / 1,7 N (cau chot).
#   goi_y_mo_phong.diem_nhan: "keo 0,3 N ma hop chua di thi ma sat bang bao nhieu?" -> cau Du doan (dap an 0,3 N,
#   mo_hinh: dung yen F_ms = F_keo). Luc ke 5 N chia do 0,1 N (dung_cu), nam ngang chi ghi so nguyen.
# Hinh chinh: DO THI so chi luc ke theo thoi gian khi keo tang dan (doan cheo -> dinh 0,7 N -> tut 0,6 N -> ngang).
#   (masat2: dien tich/toc do/lan, masat3: goc nghieng se dung bo cuc khac.) Truc thoi gian khong ghi so (khong bia so giay).
# KHONG tra loi san cau "Doc so lieu" sau hop (tinh F_truot/N, mu = ?, lan do nao kem tin cay): clip khong hien N = 1,96,
#   khong hien mu, khong noi ve sai so lan do nhe.
# Bay = hien_tuong_hay_sai[1] (ma sat nghi luon bang muN). Chua noi duoc = mo_hinh.gia_thiet[2] (dien tich, toc do: chua doi).
# Chot: chat gia trong, tong 0,40 kg -> luc de hop bat di ~1,4-1,5 N (gap doi vi ap luc gap doi; mo hinh 1,41, bang hang 2 doc 1,5).
# Tu kiem: python clips/masat1.py --kiem
import math
from engine import *

M_HOP = 0.20
F_NGHI, F_TRUOT = 0.7, 0.6          # so_lieu_mau hang 1
F_HOI = 0.3                         # goi_y_mo_phong.diem_nhan
FMAX = 5.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOX = (214, 170, 110); BOX_D = (150, 104, 56)
SKIN = (240, 196, 160); SKIN_D = (190, 140, 105); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
MS = TEAL                           # mau luc ma sat

# Times Bold Italic cho mu (mu cua SF de doc nham)
_TI = {}
def TI(size):
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

# ---------------- dan thi nghiem (nhin ngang, keo sang PHAI) ----------------
SURF = 640                          # mat ban
BX0, BW, BH = 170, 190, 110         # hop: mep trai luc dau, rong, cao
HOOK_Y = SURF - BH / 2
ROPE, BODY = 30, 400

def rig(d, xl, f_read, state=None):
    card(d, (40, 260, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([40, SURF, 1040, SURF + 40], fill=WOOD); d.line([(40, SURF), (1040, SURF)], fill=WOOD_D, width=4)
    d.rounded_rectangle([xl, SURF - BH, xl + BW, SURF], radius=10, fill=BOX, outline=BOX_D, width=4)
    xr = xl + BW
    Q = lambda s, h=0.0: (xr + s, HOOK_Y + h)
    d.line([Q(0), Q(ROPE - 13)], fill=NAVY, width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, f_read, nho=0.1, so=(0, 1, 2, 3, 4, 5), hw=44, ben=-1, co=40)
    d.line([Q(se - 16), Q(se + 12)], fill=NAVY, width=8)
    hx, hy = Q(se + 40); dot(d, hx, hy, 28, SKIN, outline=SKIN_D)
    if state:
        s, c = state
        pw = tw(d, s, F(40)) + 40
        card(d, (xl + BW / 2 - pw / 2, 300, xl + BW / 2 + pw / 2, 360), fill=WHITE, outline=c, w=4, r=26)
        text(d, (xl + BW / 2, 330), s, 40, c)

def readout(d, s, y=815, color=RED):
    card(d, (W / 2 - 150, y - 42, W / 2 + 150, y + 42), fill=(254, 242, 242), r=24)
    text(d, (W / 2, y), s, 52, color)

def think_bar(d, t, t1, t2, y, a):
    q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, y, 940, y + 12], radius=6, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 12], radius=6, fill=A(PURPLE, a))

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    f = F_HOI * ease((t - 0.6) / 0.9)
    rig(d, BX0, f, None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 250, "Kéo 0,3 N, hộp vẫn yên.\nMa sát của bàn lên hộp\nbằng bao nhiêu?", 52, INK,
          maxw=900, alpha=a)
    text(d, (W / 2, y0 + 440), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    if t > M[1] + 0.6: think_bar(d, t, M[1] + 0.6, sc["T"] - THINK_END, y0 + 510, a)

# ---------------- canh 2: Tien hanh (keo tang dan, do thi F theo t) ----------------
T0, T_SLIP, T_DROP, T_END = 0.4, 3.6, 0.25, 7.0      # bat dau keo, luc hop bat di, thoi gian tut so, het ve
RATE = F_NGHI / (T_SLIP - T0)                        # N/s khi keo tang dan
V_PX = 30.0                                          # px/s khi truot deu

def f_at(t):
    """So chi luc ke (= luc keo) theo thoi gian; hop dung yen tới T_SLIP thi bat di."""
    if t < T0: return 0.0
    if t < T_SLIP: return RATE * (t - T0)
    if t < T_SLIP + T_DROP: return lerp(F_NGHI, F_TRUOT, ease((t - T_SLIP) / T_DROP))
    return F_TRUOT

def x_at(t):
    return BX0 + (max(0.0, min(t, T_END) - T_SLIP) * V_PX if t > T_SLIP else 0.0)

def do_state(t):
    """-> (x hop, so kim, chu o so chi, trang thai hop)."""
    f = f_at(t)
    if t < T_SLIP: read, st = "tăng dần…", ("đứng yên", MUTED)
    elif t < T_SLIP + T_DROP: read, st = vn(F_NGHI) + " N", ("bật đi", ORANGE)
    else: read, st = vn(F_TRUOT) + " N", ("trượt đều", DGREEN)
    if t < T0: read = "0 N"
    return x_at(t), f, read, st

# do thi
GX0, GX1, GYB, GYT = 190, 990, 1430, 950
def gx(t): return GX0 + (t - T0) / (T_END - T0) * (GX1 - GX0 - 30)
def gy(f): return GYB - f / 1.0 * (GYB - GYT)

def graph(d, t_now, hl=None, a_lab=1.0, top=870):
    card(d, (40, top, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GYB), (GX1 + 20, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 40)], fill=NAVY, width=5)
    text(d, (GX0 + 18, GYT - 44), "F (N)", 40, INK, anchor="lm")
    text(d, (GX1 + 20, GYB + 44), "t", 40, INK, anchor="rm")
    for v in (0, 1.0):
        d.line([(GX0 - 10, gy(v)), (GX0, gy(v))], fill=NAVY, width=4); text(d, (GX0 - 18, gy(v)), vn(v) if v else "0", 40, INK, anchor="rm")
    pts = []; tt = T0
    while tt <= min(t_now, T_END) + 1e-9:
        pts.append((gx(tt), gy(f_at(tt)))); tt += 0.02
    if len(pts) > 1: d.line(pts, fill=RED, width=7, joint="curve")
    if hl: hl(d)
    k1 = a_lab * appear(t_now, T_SLIP + 0.1, 0.35)
    if k1 > 0:
        x = gx(T_SLIP); y = gy(F_NGHI)
        dot(d, x, y, 12, ORANGE, WHITE)
        text(d, (x + 24, y - 50), "0,7 N: bật đi", 40, ORANGE, anchor="lm", alpha=k1)
    k2 = a_lab * appear(t_now, T_SLIP + 1.2, 0.35)
    if k2 > 0:
        text(d, (gx(T_END) - 10, gy(F_TRUOT) + 54), "0,6 N: trượt đều", 40, DGREEN, anchor="rm", alpha=k2)

def s_do(img, d, t, sc):
    x, f, read, st = do_state(t)
    rig(d, x, f, st)
    graph(d, t, top=870)
    readout(d, read, y=815)

def _kiem_dong_bo():
    """Moi 0,05 s: hop chi chay khi so chi da toi nghi cuc dai; so tut DUNG luc hop bat di; o so chi = kim khi
    hien so; do thi ve dung so chi."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        x, f, read, st = do_state(t)
        moving = x > BX0 + 1e-9
        if moving and t < T_SLIP: bad.append((round(t, 2), "hop chay som"))
        if t < T_SLIP and f > F_NGHI + 1e-9: bad.append((round(t, 2), "vuot nghi max khi dung yen", f))
        if t >= T_SLIP + T_DROP and abs(f - F_TRUOT) > 1e-9: bad.append((round(t, 2), "truot khong dung 0,6", f))
        if t >= T_SLIP + T_DROP and st[0] != "trượt đều": bad.append((round(t, 2), "nhan trang thai"))
        if t > T_SLIP + 0.1 and t < T_END and not moving: bad.append((round(t, 2), "hop dung khi da truot"))
        if read.endswith(" N") and read != "0 N":
            v = float(read[:-2].replace(",", "."))
            if abs(v - f) > 0.051 and not (T_SLIP <= t < T_SLIP + T_DROP): bad.append((round(t, 2), "o so != kim", read, round(f, 3)))
        t += 0.05
    if abs(f_at(T_SLIP - 1e-6) - F_NGHI) > 1e-3: bad.append("dinh khong dung 0,7")
    if T_END > sc["T"]: bad.append("do thi chua ve xong")
    if x_at(T_END) + BW + ROPE + 20 + BODY + 30 + 40 + 28 > 1040: bad.append("tay ra ngoai khung")
    return bad

# ---------------- canh 3: Dap an (luc tren hop luc keo 0,3 N) ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

T_HOI = T0 + F_HOI / RATE
LF = 130                                   # px cho 0,3 N (hai mui ten dai bang nhau)
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, BX0, F_HOI, ("đứng yên", MUTED))
    k1 = appear(t, M[0] + 0.5, 0.45)
    if k1 > 0:   # hai luc len HOP: luc ke keo (sang phai), ma sat cua ban (sang trai)
        cx = BX0 + BW / 2
        d.rounded_rectangle([BX0 - 6, SURF - BH - 6, BX0 + BW + 6, SURF + 6], radius=14, outline=A(ORANGE, k1), width=5)
        arrow(d, (cx, SURF - BH - 40), (cx + LF * ease(k1), SURF - BH - 40), A(RED, k1), w=8, head=22)
        text(d, (cx - 10, SURF - BH - 92), "lực kế kéo: lên hộp", 40, RED, anchor="lm", alpha=k1)
        arrow(d, (cx, SURF - 6), (cx - LF * ease(k1), SURF - 6), A(MS, k1), w=8, head=22)
        text(d, (60, SURF + 80), "ma sát của bàn: lên hộp", 40, MS, anchor="lm", alpha=k1)
    def hl(d):
        x, y = gx(T_HOI), gy(F_HOI)
        for xx in range(GX0, int(x), 26): d.line([(xx, y), (xx + 14, y)], fill=MS, width=4)
        dot(d, x, y, 13, MS, WHITE)
        text(d, (x + 26, y + 34), "0,3 N", 40, MS, anchor="lm")
    graph(d, T_END, hl=hl, a_lab=0.0, top=870)
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN · 0,3 N", 815, ka)

# ---------------- canh 4: Rut ra (dinh > muc truot) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1110), fill=WHITE, outline=LIGHT, w=3)
    k1 = appear(t, 0.2, 0.4)
    # hai cot: nghi cuc dai va truot (cung truc tu 0)
    base, top = 990, 390; sp = (base - top) / 0.8
    for i, (v, lab, c) in enumerate(((F_NGHI, "lúc bật đi", ORANGE), (F_TRUOT, "lúc trượt đều", DGREEN))):
        cx = 330 + i * 420; g = ease((t - 0.3 - 0.4 * i) / 0.6); h = v * sp * g
        if h > 2: d.rectangle([cx - 90, base - h, cx + 90, base], fill=c)
        if g > 0.95: text(d, (cx, base - h - 40), vn(v) + " N", 48, c)
        text(d, (cx, base + 50), lab, 42, INK, alpha=k1)
    d.line([(90, base), (990, base)], fill=NAVY, width=4)
    k2 = appear(t, M[0] + 0.4, 0.45)
    if k2 > 0:
        y0 = 1160 + (1 - k2) * 20
        card(d, (40, y0, 1040, y0 + 210), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=5)
        text(d, (W / 2, y0 + 70), "Ma sát nghỉ cực đại", 46, (154, 52, 18), alpha=k2)
        text(d, (W / 2, y0 + 145), "lớn hơn ma sát trượt", 46, (154, 52, 18), alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def mu_line(d, cx, y, pre, post, size, color, alpha):
    """Chu SF + 'μN' bang Times Bold Italic."""
    f, fm = F(size), TI(size * 1.15)
    parts = [(pre, f), ("μN", fm), (post, f)]
    tot = sum(tw(d, p, ff) for p, ff in parts); x = cx - tot / 2
    for p, ff in parts:
        dtext(d, (x, y), p, ff, color, alpha, "lm"); x += tw(d, p, ff)
    return tot

def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    ks = clamp((t - M[0] - 1.6) / 0.4)
    kk = appear(t, M[0] + 1.9, 0.4)
    def hl(d):      # doan cheo (ma sat nghi) to dam khi hien ket luan
        if kk <= 0: return
        pts = [(gx(tt), gy(f_at(tt))) for tt in [T0 + i * 0.02 for i in range(int((T_SLIP - T0) / 0.02) + 1)]]
        d.line(pts, fill=A(MS, kk), width=14, joint="curve")
    graph(d, T_END, hl=hl, a_lab=0.0, top=870)
    if a1 > 0:
        y0 = 270
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        yy = y0 + 200
        lw = mu_line(d, W / 2 - 24, yy, "“Ma sát nghỉ luôn bằng ", "”", 48, mix(INK, MUTED, ks), a1)
        if ks > 0:
            xa = W / 2 - 24 - lw / 2 - 6
            d.line([(xa, yy + 2), (xa + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 - 24 + lw / 2 + 34, yy), "✗", 48, DRED, alpha=a1 * ks)
        k3 = a1 * kk
        card(d, (70, y0 + 300, 1010, y0 + 520), fill=A((236, 253, 243), k3), r=24)
        text(d, (W / 2, y0 + 370), "✓ Ma sát nghỉ của hộp này", 46, DGREEN, alpha=k3)
        text(d, (W / 2, y0 + 450), "đổi từ 0 tới 0,7 N", 46, DGREEN, alpha=k3)
    if k2 > 0:
        y0 = 270 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 360), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kq = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (90, y0 + 180), "• Diện tích, tốc độ kéo:", 44, INK, anchor="lm", alpha=kq)
        text(d, (90, y0 + 265), "  chưa thử", 44, INK, anchor="lm", alpha=kq)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        x0 = 200
        for y, lab, res, wt in ((1060, "0,20 kg", "bật đi: 0,7 N", False), (1240, "0,40 kg", "?", True)):
            d.line([(110, y), (970, y)], fill=A(WOOD_D, k), width=6)
            d.rounded_rectangle([x0, y - 90, x0 + 190, y], radius=10, fill=A(BOX, k), outline=A(BOX_D, k), width=4)
            if wt:   # gia trong chat len hop
                d.rounded_rectangle([x0 + 45, y - 140, x0 + 145, y - 90], radius=8, fill=A(GRAY, k), outline=A(INK, k), width=3)
            text(d, (x0 + 95, y - 45), lab, 40, WHITE, alpha=k)
            arrow(d, (x0 + 190, y - 45), (x0 + 330, y - 45), A(RED, k), w=7, head=22)
            text(d, (x0 + 350, y - 45), res, 42, RED, anchor="lm", alpha=k)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
        card(d, (110, 1310, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1365, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1460, "Áp lực lên bàn?", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Ma sát: nghỉ cực đại\n> trượt",
             "Thêm gia trọng như hình.\nLực để hộp bật đi\nkhoảng bao nhiêu N?", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"), (do["t0"] + T0, "tap"),
            (do["t0"] + T_SLIP, "tap"), (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][0] + 0.4, "tap"),
            (b["t0"] + b["M"][0] + 1.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-luc-ma-sat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực ma sát · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kéo hộp gỗ bằng lực kế", draw=s_hook, tail=1.0, caps=[
   ("Kéo ngang hộp gỗ.", 3.0),
   ("Dừng video, chọn đáp án.", 5.4)]),
 dict(key="do", title="Kéo tăng dần", draw=s_do, tail=0.5, caps=[
   ("Kéo tăng dần, hộp vẫn yên.", 3.3),
   ("Hộp bật đi: số chỉ tụt.", 3.3)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Đứng yên: hai lực cân bằng.", 3.2),
   ("Ma sát lên hộp cũng 0,3 N.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("So lúc bật đi, lúc trượt.", 3.0),
   ("Bật đi rồi, nhẹ tay hơn.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy hay gặp.", 4.2),
   ("Chưa nói được gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 8.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
