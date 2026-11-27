# Clip: tn-l11-baitapnangluong-02 - Xich du o san truong: co nang va toc do qua day (vi_du)
# (9/11/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 56 px khi ve, K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapnangluong-02.json (_kiem_so() doi chieu):
#   l = 2,0 m (1,5-3) ; alpha0 5..45 do ; m = 40 kg ; h = l(1 - cos a0), W = mgh, v = can(2gh), g = 9,8.
#   so_lieu_mau (a0, h m, W J, v m/s): 10 0,03 11,9 0,77 ; 20 0,121 47,3 1,54 ; 30 0,268 105,0 2,29 (tinh tu mo hinh).
# Du doan (giu, = dong "Nhin vao" cua hop vi du): a0 10 -> 30 do, toc do qua day gap may lan? -> khoang 3 (2,29 : 0,77).
# Bay = hien_tuong_hay_sai[0]: dung cos a0 thay cho 1 - cos a0 (hinh: l.cos a0 = 1,73 m la doan tu diem treo xuong ghe).
# Thu nghi (= cau_chot khung web; DOI 27/11: ca cu "ban nang hon -> v khong doi" co dap so 2,29 dang hien trong bang):
#   day 3,0 m (max tham_so), van 30 do -> v = can(2*9,8*3(1 - cos30)) = 2,81 m/s. Dap so KHONG hien.
from engine import *

L_M, M_KG, G = 2.0, 40.0, 9.8
ROWS = [(10, "10°", "0,030", "11,9", "0,77"), (20, "20°", "0,121", "47,3", "1,54"), (30, "30°", "0,268", "105,0", "2,29")]

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-baitapnangluong-02.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["l"]["mac_dinh"] == L_M and tp["m"]["gia_tri"] == M_KG and tp["l"]["max"] >= 3.0
    for r, (a, _, h, w, v) in zip(k["so_lieu_mau"]["hang"], ROWS):
        assert r == [a, float(h.replace(",", ".")), float(w.replace(",", ".")), float(v.replace(",", "."))], a
        hh = L_M * (1 - math.cos(math.radians(a)))
        assert abs(math.sqrt(2 * G * hh) - r[3]) < 0.006
    assert abs(math.sqrt(2 * G * 3.0 * (1 - math.cos(math.radians(30)))) - 2.81) < 0.005     # cau chot
    assert abs(L_M * math.cos(math.radians(30)) - 1.73) < 0.005                               # bay
_kiem_so()

DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8)
SEAT = (234, 88, 12); SKIN = (240, 190, 150); SHIRT = (124, 58, 237); EMPTY = (148, 140, 128)

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi cong thuc: _{..} chi so duoi (>= 56 px)."""
    fs = []
    for p in [p for p in re.split(r"(_\{[^}]*\})", s) if p]:
        if p.startswith("_{"): fs.append((p[2:-1], F(max(56, size * 0.7)), size * 0.24))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=170, n=5):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9)
    for i in range(n):
        x = x0 + i * 152
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=16)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def pill(d, cy, s, col, a=1.0, size=56):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, cy - 40, W / 2 + pw / 2, cy + 40), fill=A(col, a), r=40)
    text(d, (W / 2, cy), s, size, WHITE, alpha=a)

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1)
    if L < 1: return
    n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(p0[0] + (p1[0] - p0[0]) * a, p0[1] + (p1[1] - p0[1]) * a),
                (p0[0] + (p1[0] - p0[0]) * b, p0[1] + (p1[1] - p0[1]) * b)], fill=col, width=w)

# ---------------- xich du nhin ngang (2,0 m = 500 px) ----------------
PIV = (420, 290); LPX = 500
def seat_pos(deg): a = math.radians(deg); return (PIV[0] + LPX * math.sin(a), PIV[1] + LPX * math.cos(a))
def swing(d, deg, ghost=False, alpha=1.0):
    c = lambda col: A(col, alpha)
    sx, sy = seat_pos(deg)
    d.line([PIV, (sx, sy)], fill=c(GRAY if ghost else NAVY), width=5)
    d.rounded_rectangle([sx - 55, sy, sx + 55, sy + 16], radius=6, fill=c(LIGHT if ghost else SEAT), outline=c(GRAY if ghost else NAVY), width=2)
    if ghost: return
    d.rectangle([sx - 20, sy - 90, sx + 20, sy - 2], fill=c(SHIRT))
    d.ellipse([sx - 26, sy - 146, sx + 26, sy - 94], fill=c(SKIN), outline=c(NAVY), width=3)
def frame(d):
    d.rectangle([PIV[0] - 300, PIV[1] - 18, PIV[0] + 300, PIV[1]], fill=GRAY, outline=NAVY, width=3)
    d.ellipse([PIV[0] - 10, PIV[1] - 10, PIV[0] + 10, PIV[1] + 10], fill=NAVY)
    dashed(d, PIV, (PIV[0], PIV[1] + LPX + 40), GRAY, w=3, on=10, off=8)
def arc_lab(d, deg, col, lab, r=150):
    d.arc([PIV[0] - r, PIV[1] - r, PIV[0] + r, PIV[1] + r], 90 - deg, 90, fill=col, width=6)
    a = math.radians(deg); text(d, (PIV[0] + r * math.sin(a) + 24, PIV[1] + r * math.cos(a) - 10), lab, 56, col, anchor="lm")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    frame(d); swing(d, 10, ghost=True); swing(d, 30)
    arc_lab(d, 10, DBLUE, "10°", r=380); arc_lab(d, 30, DORANGE, "30°", r=200)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 980 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 180), "Dây 2,0 m, bỏ ma sát.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Góc từ 10° lên 30°: tốc độ", 60, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 350), "qua đáy gấp mấy lần?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 460, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: ba lan day, bang ----------------
RT = [2.0, 4.0, 6.0]
TX = [150, 390, 640, 900]; TY0 = 1120
def s_do(img, d, t, sc):
    i = min(2, int(t // 2.0))
    a0 = ROWS[i][0]; u = t - 2.0 * i
    deg = a0 * ease(u / 0.5) if u < 0.5 else a0 * math.cos(2 * math.pi * (u - 0.5) / 2.84 * 1.0)
    frame(d); swing(d, deg); arc_lab(d, a0, DORANGE, f"{a0}°", r=200)
    pw = tw(d, "đo góc bằng điện thoại", F(56)) + 56
    card(d, (W / 2 - pw / 2, 880, W / 2 + pw / 2, 960), fill=ORANGE, r=40)
    text(d, (W / 2, 920), "đo góc bằng điện thoại", 56, WHITE)
    card(d, (40, 990, 1040, TY0 + 2 * 90 + 60), fill=WHITE, outline=NAVY, r=20, w=3)
    for cx, h1, h2 in zip(TX, ("α_{0}", "h", "W", "v"), ("", "m", "J", "m/s")):
        eq(d, cx, 1030, h1 + (" (" + h2 + ")" if h2 else ""), 56, INK)
    d.line([(50, 1070), (1030, 1070)], fill=NAVY, width=3)
    for r, (_, al, h, w, v) in enumerate(ROWS):
        if t < RT[r]: continue
        k = appear(t, RT[r], 0.3)
        for cx, s_, col in zip(TX, (al, h, w, v), (INK, INK, DORANGE, DBLUE)): text(d, (cx, TY0 + r * 90), s_, 58, col, alpha=k)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 300, 1040, 560), fill=WHITE, outline=NAVY, r=20, w=3)
    for j, r in enumerate((0, 2)):
        _, al, h, w, v = ROWS[r]
        y = 370 + j * 120
        text(d, (80, y), al, 58, INK, anchor="lm")
        eq(d, 240, y, "h = " + h + " m", 58, INK, anchor="l")
        text(d, (1020, y), "v = " + v + " m/s", 58, DBLUE, anchor="rm")
    k2 = appear(t, 2.3, 0.4)
    if k2 > 0:
        text(d, (W / 2, 700), "h gấp khoảng 9", 62, INK, alpha=k2)
        text(d, (W / 2, 820), "2,29 : 0,77 ≈ 3", 64, DBLUE, alpha=k2)
    kp = appear(t, M[1] - 0.1, 0.4)
    if kp > 0: pill(d, 980, "ĐÁP ÁN · khoảng 3 lần", NAVY, kp, size=58)

# ---------------- canh 4: Bay (cos thay cho 1 - cos) ----------------
def s_bay(img, d, t, sc):
    kc = appear(t, 3.4, 0.5)
    frame(d); swing(d, 30)
    sx, sy = seat_pos(30); by = PIV[1] + LPX
    dashed(d, (sx - 60, sy + 8), (PIV[0] - 60, sy + 8), GRAY, w=3, on=10, off=8)
    d.line([(PIV[0] - 40, PIV[1]), (PIV[0] - 40, sy + 8)], fill=DRED, width=7)
    text(d, (PIV[0] - 60, (PIV[1] + sy) / 2), "l·cos 30°", 56, DRED, anchor="rm")
    if kc > 0:
        d.line([(PIV[0] - 40, sy + 8), (PIV[0] - 40, by + 8)], fill=A(DGREEN, kc), width=9)
        text(d, (PIV[0] - 60, by + 50), "h", 60, DGREEN, anchor="rm", alpha=kc)
    y0 = 960
    card(d, (40, y0, 1040, y0 + 580), fill=WHITE, outline=DRED, w=6)
    pill(d, y0 + 70, "BẪY", DRED)
    s1 = "✗ h = 2,0 · cos 30° = 1,73 m"
    lw = tw(d, s1, F(58))
    text(d, (W / 2, y0 + 200), s1, 58, DRED)
    if kc > 0:
        d.line([(W / 2 - lw / 2, y0 + 202), (W / 2 - lw / 2 + lw * kc, y0 + 202)], fill=(140, 15, 15), width=7)
        text(d, (W / 2, y0 + 330), "✓ h = 2,0(1 − cos 30°)", 60, DGREEN, alpha=kc)
        text(d, (W / 2, y0 + 440), "= 0,268 m", 60, DGREEN, alpha=kc)

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    frame(d); swing(d, 30 * math.exp(-0.3 * t) * math.cos(2 * math.pi * t / 2.84))
    card(d, (40, 1000, 1040, 1340), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 1085), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 1230), "Nếu có ma sát?", 62, INK)

# ---------------- canh 6: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 290, "THỬ NGHĨ", ORANGE, k1)
    card(d, (80, 380, 1000, 500), fill=A((239, 246, 255), k1), r=20)
    text(d, (W / 2, 440), "Dây 2,0 m, 30°: qua đáy 2,29 m/s", 56, DBLUE, alpha=k1)
    kq = appear(t, 2.2, 0.45)
    if kq > 0:
        text(d, (W / 2, 700), "Dây 3,0 m, vẫn 30°, bỏ ma sát.", 62, INK, alpha=kq)
        text(d, (W / 2, 810), "Qua đáy, tốc độ bao nhiêu?", 62, DORANGE, alpha=kq)
        seg_bar(d, 960, t, 2.8, sc["T"] - 0.2, ORANGE, kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open")] + [(do["t0"] + r, "tick") for r in RT] + [
            (da["t0"] + da["M"][1] - 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 2.2, "open")]

CLIP = dict(id="tn-l11-baitapnangluong-02", header="VẬT LÍ 11 · VÍ DỤ", footer="Bài tập năng lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xích đu sân trường", draw=s_hook, tail=0.3, caps=[
   ("Đẩy lệch 10° rồi 30°.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Ba lần đẩy", draw=s_do, tail=0.3, caps=[
   ("Đẩy ba góc: 10°, 20°, 30°.", 3.8),
   ("Tính h, W, v cho từng lần.", 3.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.2, caps=[
   ("So hàng 30° với hàng 10°.", 4.0),
   ("Đọc cột v ở hai hàng.", 3.2)]),
 dict(key="bay", title="Bẫy: độ cao h", draw=s_bay, tail=0.3, caps=[
   ("Dễ lấy nhầm đoạn trên.", 3.4),
   ("h đo từ đáy lên.", 3.2)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Số tính từ mô hình.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Đổi chiều dài dây.", 3.0),
   ("Dừng lại, tự tính.", 4.8)]),
])
