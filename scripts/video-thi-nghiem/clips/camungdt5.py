# Clip: tn-l12-camungdt-05 - Thanh truot tren hai ray: CHIEU dong cam ung (dinh luat Lenz)
# Ban 3 (21/11/2026, viec 4 lo 20 KE-HOACH-CAI-TIEN-CLIP): dung lai theo cong --do-chu moi. Quan niem sai can danh:
#   sai chieu dong cam ung ("tu truong cam ung luon nguoc B", nho hinh thay vi suy luan) -> Du doan doi sang CHIEU dong.
# So lieu: kho content/thi-nghiem/tn-l12-camungdt-05.json (B = 0,40 T huong len; R ben trai; cac_buoc lam 4: "keo thanh
#   theo chieu nguoc lai, xem kim miliampe ke lech ve phia nao"; quan_sat 4: "doi chieu truot: kim lech nguoc lai").
#   Clip khong dung so nao ngoai kho (chi ve chieu, khong ghi so do).
# Bai (theory.src.html): FIG4 ve dung ca "B ra khoi trang, thanh truot RA XA R -> dong trong thanh tu ray tren xuong" ->
#   Tien hanh chieu dung ca nay (da co trong bai); Du doan hoi ca NGUOC LAI (day ve phia R) -> chua co trong bai.
# Du doan (K10 khong nut A-D): B huong len, day thanh ve phia R: nhin tu tren, dong chay chieu nao? -> NGUOC chieu kim dong ho.
# Bay: hien_tuong_hay_sai 2 "luc tu day thanh chay tiep" -> hai khung ra xa R / ve phia R, luc tu luon nguoc v; thoi keo thi
#   v va luc tu cung nho dan (cham dan roi dung, kho quan_sat 5).
# Thu nghi (= cau_chot khung web): dao nam cham (B huong xuong), day thanh ve phia R -> CUNG chieu kim dong ho
#   (tu thong huong xuong giam -> tu truong cam ung cung huong xuong). Bat loi "luon nguoc B" lan nua; dap so khong hien.
# Ban 3 v2 (cong B v1): vong chieu dong to + dam, quy uoc kim canh mA ke, chu Bay 66-70 px, Bay ket o 'v = 0', 'mA' xuong 7 px.
# Vat li (kiem bang tich co huong o duoi). Nhin tu tren: x sang phai, y len man hinh, z huong ve nguoi nhin (= "huong len").
from engine import *

def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def bar_iy(sv, bz):             # dau y cua dong trong thanh: q v x B (sv = +1 ra xa R / sang phai, -1 ve phia R)
    return cross((sv, 0, 0), (0, 0, bz))[1]
def bar_fx(sv, bz):             # dau x cua luc tu len thanh: F = I l x B
    return cross((0, bar_iy(sv, bz), 0), (0, 0, bz))[0]
def lenz_ind(sv, bz):           # R ben trai: dien tich tang khi sv = +1; tu truong cam ung chong bien thien tu thong
    return -bz * sv
def is_cw(sv, bz):              # thanh la canh PHAI cua mach: dong trong thanh di XUONG <=> cung chieu kim dong ho
    return bar_iy(sv, bz) < 0
for _sv in (1, -1):
    for _bz in (1, -1):
        assert bar_fx(_sv, _bz) == -_sv                                   # luc tu luon nguoc v
        assert is_cw(_sv, _bz) == (lenz_ind(_sv, _bz) < 0)                # Lenz khop luc Lorentz: B cam ung huong xuong <=> cung chieu kim
assert is_cw(1, 1) and not is_cw(-1, 1)          # Tien hanh (ra xa R) cung chieu; Du doan (ve phia R) NGUOC chieu
assert lenz_ind(1, 1) == -1 and lenz_ind(-1, 1) == 1   # tang: nguoc B; giam: cung chieu B
assert is_cw(-1, -1)                             # cau chot: B huong xuong, ve phia R -> CUNG chieu kim dong ho
assert bar_iy(1, 1) == -1                        # khop FIG4 cua bai: ra xa R, dong trong thanh tu ray tren xuong

COP = (184, 115, 51); BAR = (120, 72, 30); EMPTY = (148, 140, 128); DARK_OR = (181, 71, 8)
CUR = BLUE                                       # dong dien + tu truong cam ung: xanh duong; B ngoai: tim; luc tu: do

def sym(d, x, y, kind, r=17, color=PURPLE, w=4, alpha=1.0):
    """Ve tay: 'o' = huong len (ve phia nguoi nhin tu tren), 'x' = huong xuong."""
    c = A(color, alpha)
    d.ellipse([x - r, y - r, x + r, y + r], outline=c, width=w)
    if kind == "o": d.ellipse([x - r * 0.3, y - r * 0.3, x + r * 0.3, y + r * 0.3], fill=c)
    else:
        q = r * 0.6
        d.line([(x - q, y - q), (x + q, y + q)], fill=c, width=w); d.line([(x - q, y + q), (x + q, y - q)], fill=c, width=w)

def chevron(d, x, y, ang, color, s=22, w=7):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def circ(d, cx, cy, r, cw, color, w=8, head=22):
    """Mui ten vong: cw = True cung chieu kim dong ho tren man hinh (= nhin tu tren xuong)."""
    s0, s1 = -70, 220                            # goc PIL (do, tang = theo chieu kim dong ho tren man)
    d.arc([cx - r, cy - r, cx + r, cy + r], s0, s1, fill=color, width=w)
    th = math.radians(s1 if cw else s0)
    px, py = cx + r * math.cos(th), cy + r * math.sin(th)
    ang = math.atan2(math.cos(th), -math.sin(th)) if cw else math.atan2(-math.cos(th), math.sin(th))
    chevron(d, px, py, ang, color, s=head, w=w)

# ---------------- hinh chinh (nhin tu tren xuong) ----------------
YT, YB, XL, XE, YC = 430, 730, 160, 1010, 580
def dial(d, k):
    """Miliampe ke kim giua (so 0 o giua): k = +1 lech phai, -1 lech trai."""
    d.ellipse([XL - 100, YC - 100, XL + 100, YC + 100], fill=WHITE, outline=NAVY, width=6)
    px, py = XL, YC + 8
    for a in (-40, 0, 40):
        r = math.radians(a)
        d.line([(px + 62 * math.sin(r), py - 62 * math.cos(r)), (px + 78 * math.sin(r), py - 78 * math.cos(r))], fill=NAVY, width=5)
    r = math.radians(40 * k)
    d.line([(px, py), (px + 74 * math.sin(r), py - 74 * math.cos(r))], fill=RED, width=7)
    dot(d, px, py, 9, NAVY)
    text(d, (XL, YC + 52), "mA", 56, NAVY)                                   # cong B v1: khong de mep duoi vong

def legend(d, bz):
    sym(d, 95, 290, "o" if bz > 0 else "x", 24, PURPLE, 5)
    text(d, (138, 290), "B hướng lên" if bz > 0 else "B hướng xuống", 58, PURPLE, anchor="lm")

def rig(d, xb, bz=1, sv=0, kv=1.0, needle=0.0, ki=0.0, ind=True, quyuoc=False):
    """xb: vi tri thanh; sv: chieu truot (0 = chua ve v); kv: do dai tuong doi mui ten v; ki: do dam B cam ung + chieu dong."""
    cx = (XL + 100 + xb) / 2; rr = 110
    d.rectangle([XL, YT, xb, YB], fill=A(PURPLE, 0.09))                    # dien tich mach (to nhat)
    for x in range(330, 1000, 110):                                        # B ngoai: cham trong tron / dau x
        for y in (480, 680):
            if -60 < x - xb < 90: continue
            if ki > 0 and math.hypot(x - cx, y - YC) < rr + 45: continue
            sym(d, x, y, "o" if bz > 0 else "x")
    d.line([(XL, YT), (XE, YT)], fill=COP, width=12); d.line([(XL, YB), (XE, YB)], fill=COP, width=12)
    d.line([(XL, YT), (XL, YB)], fill=NAVY, width=6)
    d.rectangle([300, YT - 24, 420, YT + 24], fill=WHITE, outline=NAVY, width=5)
    text(d, (360, YT - 70), "R", 60, NAVY)
    dial(d, needle)
    d.rounded_rectangle([xb - 11, YT - 36, xb + 11, YB + 36], radius=7, fill=BAR)
    if sv and kv > 0.05:
        L = 150 * kv; x1 = xb + sv * L
        arrow(d, (xb, 862), (x1, 862), TEAL, w=8, head=24)
        text(d, (x1 + sv * 20, 862), "v", 60, TEAL, anchor="lm" if sv > 0 else "rm")
    if quyuoc:                                   # chu giai (duyet v2): o rieng duoi the, tach khoi kim; hien tu dau canh
        f = F(56); w1 = tw(d, "Quy ước:", f); w2 = tw(d, "kim lệch phải", f); tot = w1 + 30 + 70 + 30 + 60 + 30 + w2
        x = W / 2 - tot / 2; y = 1505
        card(d, (x - 30, y - 50, x + tot + 30, y + 50), fill=(241, 245, 249), outline=GRAY, r=22, w=3)
        text(d, (x, y), "Quy ước:", 56, INK, anchor="lm"); x += w1 + 30
        circ(d, x + 35, y, 30, True, CUR, w=7, head=18); x += 70 + 30
        arrow(d, (x, y), (x + 60, y), INK, w=6, head=18); x += 60 + 30
        text(d, (x, y), "kim lệch phải", 56, INK, anchor="lm")
    if ki > 0 and sv:
        cw = is_cw(sv, bz); c = A(CUR, ki)
        if ind: sym(d, cx, YC, "o" if lenz_ind(sv, bz) > 0 else "x", 40, CUR, 7, alpha=ki)
        circ(d, cx, YC, rr, cw, c, w=12, head=36)
        y0, y1 = (505, 655) if bar_iy(sv, bz) < 0 else (655, 505)
        arrow(d, (xb + 42, y0), (xb + 42, y1), c, w=11, head=32)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 72 px, tat lan luot tu phai sang trai."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 72), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 72), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=5)

def pill(d, s, y, col, a, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(col, a), r=36)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; legend(d, 1)
    kv = appear(t, 1.0, 0.5)
    rig(d, 760, 1, -1, kv=kv)                                              # thanh dung yen, mui ten: se day ve phia R
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 620), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 40, PURPLE, a)
    text(d, (W / 2, y0 + 170), "Đẩy thanh về phía R.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "Dòng trong mạch", 62, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 370), "chạy chiều nào?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 480, t, M[1] + 0.3, sc["T"] - 0.2, PURPLE, a)

# ---------------- chuoi suy luan (canh 2, 3) ----------------
def chain(d, t, sc, sv, rows):
    """rows: [(dong chu, mau, bieu tuong)], dong 1 hien o M[1], dong 2 o M[2]; chieu dong: vong tron tren hinh + phu de."""
    M = sc["M"]; k1 = appear(t, M[1] - 0.05, 0.45); k2 = appear(t, M[2] - 0.05, 0.45)
    if k1 <= 0: return
    card(d, (40, 900, 1040, 1420), fill=A(WHITE, k1), outline=A(NAVY, k1), w=4)
    for j, (s, col, ic) in enumerate(rows):
        k = k1 if j == 0 else k2
        if k <= 0: continue
        y = 1040 + j * 230; c = A(col, k)
        if ic == "up" or ic == "down":
            text(d, (W / 2 - 30, y), s, 62, col, alpha=k)
            xa = W / 2 - 30 + tw(d, s, F(62)) / 2 + 50
            arrow(d, (xa, y + (34 if ic == "up" else -34)), (xa, y + (-34 if ic == "up" else 34)), c, w=9, head=24)
        else:
            if ic in ("o", "x"): sym(d, 130, y, ic, 32, col, 6, alpha=k)
            else: circ(d, 130, y, 34, ic == "cw", c, w=7, head=18)
            text(d, (190, y), s, 60, col, anchor="lm", alpha=k)

# ---------------- canh 2: Tien hanh (keo ra xa R) ----------------
def s_do(img, d, t, sc):
    M = sc["M"]; legend(d, 1)
    xb = 520 + 32 * max(0.0, t - 0.5)
    rig(d, xb, 1, 1, kv=appear(t, 0.5, 0.3), needle=appear(t, 0.5, 0.4), ki=appear(t, M[2] - 0.05, 0.45), quyuoc=True)
    chain(d, t, sc, 1, [("Từ thông tăng", PURPLE, "up"),
                        ("B cảm ứng ngược chiều B", CUR, "x" if lenz_ind(1, 1) < 0 else "o")])

# ---------------- canh 3: Ket qua (day ve phia R) = dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; legend(d, 1)
    xb = 870 - 28 * max(0.0, t - 0.5)
    rig(d, xb, 1, -1, kv=appear(t, 0.5, 0.3), needle=-appear(t, 0.5, 0.4), ki=appear(t, M[2] - 0.05, 0.45), quyuoc=True)
    chain(d, t, sc, -1, [("Từ thông giảm", PURPLE, "down"),
                         ("B cảm ứng cùng chiều B", CUR, "o" if lenz_ind(-1, 1) > 0 else "x")])

# ---------------- canh 4: Bay - luc tu day thanh chay tiep? ----------------
def mini(d, x0, sv, xb, k, kf, kv):
    """Mach thu nho (B huong len, R ben trai): v, chieu dong trong thanh, luc tu tinh tu tich co huong."""
    card(d, (x0, 250, x0 + 480, 840), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    text(d, (x0 + 240, 300), "ra xa R" if sv > 0 else "về phía R", 58, INK, alpha=k)
    yt, yb = 420, 680
    for x in (x0 + 150, x0 + 400): sym(d, x, 470, "o", 15, PURPLE, 4, alpha=k)
    d.line([(x0 + 60, yt), (x0 + 460, yt)], fill=A(COP, k), width=10); d.line([(x0 + 60, yb), (x0 + 460, yb)], fill=A(COP, k), width=10)
    d.line([(x0 + 60, yt), (x0 + 60, yb)], fill=A(NAVY, k), width=5)
    d.rectangle([x0 + 46, 500, x0 + 74, 600], fill=A(WHITE, k), outline=A(NAVY, k), width=4)
    d.rounded_rectangle([xb - 9, yt - 30, xb + 9, yb + 30], radius=6, fill=A(BAR, k))
    if kv > 0.12:
        x1 = xb + sv * 120 * kv
        arrow(d, (xb, 370), (x1, 370), A(TEAL, k), w=11, head=30)
        text(d, (x1 + sv * 16, 370), "v", 66, TEAL, anchor="lm" if sv > 0 else "rm", alpha=k)
    else: text(d, (xb, 370), "v = 0", 66, TEAL, alpha=k)          # cong B v1: thanh da dung, khung khong trong
    if kf <= 0 or kv <= 0.12: return
    iy = bar_iy(sv, 1); fx = bar_fx(sv, 1); xi = xb - fx * 30
    y0, y1 = (490, 610) if iy < 0 else (610, 490)
    arrow(d, (xi, y0), (xi, y1), A(CUR, kf), w=11, head=30)
    text(d, (xi - fx * 26, 550), "I", 70, CUR, anchor="lm" if fx < 0 else "rm", alpha=kf)
    L = 125 * kv
    arrow(d, (xb + fx * 14, 550), (xb + fx * (14 + L), 550), A(RED, kf), w=12, head=32)
    text(d, (xb + fx * 20, 632), "lực từ", 66, RED, anchor="rm" if fx < 0 else "lm", alpha=kf)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4); kf = appear(t, M[1] - 0.05, 0.45); k3 = appear(t, M[2] - 0.05, 0.45)
    kv = 1.0 - ease(clamp((t - M[2]) / 3.6)) if t > M[2] else 1.0             # thoi keo: v va luc tu cung nho dan
    mini(d, 40, 1, 340, k0, kf, kv); mini(d, 560, -1, 790, k0, kf, kv)
    if k0 <= 0: return
    card(d, (40, 880, 1040, 1480), fill=A(WHITE, k0), outline=A(RED, k0), w=6)
    pill(d, "BẪY", 920, RED, k0)
    text(d, (W / 2, 1045), "“Lực từ đẩy thanh", 62, INK, alpha=k0)
    text(d, (W / 2, 1125), "chạy tiếp”", 62, INK, alpha=k0)
    if kf > 0: pill(d, "SAI", 1235, RED, kf, 58)
    if k3 > 0: text(d, (W / 2, 1375), "Lực từ luôn ngược v", 64, RED, alpha=k3)

# ---------------- canh 5: Chot + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = 1.0                                     # the hien cung luc chu thich B (mot nhip, canh mo bang mo dan cua engine)
    legend(d, -1)
    d.rounded_rectangle([60, 250, 560, 330], radius=20, outline=A(ORANGE, appear(t, 0.8, 0.4)), width=6)   # B da dao
    rig(d, 640, -1, -1, kv=1.0)
    if k <= 0: return
    card(d, (50, 880, 1030, 1480), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", 920, DARK_OR, k)
    text(d, (W / 2, 1050), "Đẩy thanh về phía R.", 62, INK, alpha=k)
    text(d, (W / 2, 1160), "Dòng chạy chiều nào?", 64, DARK_OR, alpha=k)
    seg_bar(d, 1290, t, 1.2, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
             (do["t0"] + 0.5, "tap"), (do["t0"] + do["M"][2], "tap"),
             (da["t0"] + 0.5, "tap"), (da["t0"] + da["M"][2], "ding"),
             (b["t0"] + b["M"][0], "buzz"), (b["t0"] + b["M"][1], "tap"), (e["t0"] + 0.1, "open")])

CLIP = dict(id="tn-l12-camungdt-05", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thanh trượt trên hai ray", draw=s_hook, tail=0.3, caps=[
   ("Nhìn từ trên xuống, mạch kín.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Kéo thanh ra xa R.", 3.0),
   ("Mạch rộng ra.", 3.0),
   ("Dòng cùng chiều kim đồng hồ.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đẩy thanh về phía R.", 3.0),
   ("Mạch hẹp lại.", 3.0),
   ("Đáp án: ngược chiều kim đồng hồ.", 3.4)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.2),
   ("Thử cả hai chiều trượt.", 3.2),
   ("Thôi kéo: chậm dần rồi dừng.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tăng thì chống, giảm thì bù.", 3.4),
   ("Dừng lại, tự đoán.", 4.6)]),
])
