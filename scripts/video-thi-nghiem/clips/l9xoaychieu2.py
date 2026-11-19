# Clip: tn-l9-xoaychieu-02 - Den 6 V - 3 W voi nguon mot chieu va nguon xoay chieu cung 6 V; von ke hai dau den (KHTN 9, bai 93)
# Vong 2 (18/11/2026, theo cong B): Du doan KHONG hoi den/so chi ampe ke (bai noi san) ma hoi VON KE XOAY CHIEU hai dau den:
#   "nho hon 6 V, dung 6 V hay lon hon?" -> 6 V (so chi la gia tri hieu dung; khong giai cong thuc).
#   So lieu: so_lieu_mau (Lan, I mot chieu, I xoay chieu): 0,50/0,49 ; 0,49/0,50 ; 0,50/0,50 A; von ke 6,0/6,0 V ghi trong
#   so_lieu_mau.ghi_chu cua kho (minh hoa, bo qua dien tro ampe ke, day noi = mo_hinh.gia_thiet[1]). Ampe ke GHD 1 A, DCNN 0,01 A.
# Tranh Cau 4 (chenh 0,01 A): khong noi chenh/sai so/trung binh; bay KHONG la "den toi hon" (nhieu A) ma la
#   (vong 3) "6 V~ la luc nao cung dung 6 V", dat TRUOC Rut ra.
# Tranh Cau 6: khong mac ampe ke mot chieu vao mach xoay chieu, bo the "moi loai nguon, mot loai ampe ke".
# Hook chi co ampe ke/von ke MOT chieu, K mo; dung cu xoay chieu chi hien khi doi nguon.
# Cau chot: nguon 9 V~ (minh hoa, ghi kho) -> den 6 V - 3 W the nao? (sang hon dinh muc, de chay). Goi y khong neu dap an.
import math
from engine import *

U, P_DM = 6, 3                                  # tham_so
DC = [0.50, 0.49, 0.50]; AC = [0.49, 0.50, 0.50]   # so_lieu_mau
UV_DC, UV_AC = 6.0, 6.0                         # so_lieu_mau.ghi_chu (minh hoa)
R_A = 0.0                                       # mo_hinh.gia_thiet[1]: bo qua dien tro ampe ke, day noi
U_HOI = 9                                       # cau chot (minh hoa, ghi trong so_lieu_mau.ghi_chu)
I_MAX, DCNN = 1.0, 0.01
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
WIRE = (60, 66, 92); DRED = (185, 28, 28); DGREEN = (21, 110, 55); GLOW = (253, 224, 71)

# ---------------- hinh ----------------
XL, XR, TY, BY, LX, AY, KT, KB = 110, 530, 380, 700, 320, 540, 470, 560
VY = 500                                        # von ke song song den, ben trong vong mach
def lamp(d, x, y, on, a=1.0, r=46):
    if on > 0:
        for k in range(6, 0, -1):
            rr = r + k * 10 * on
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=A(GLOW, a * on * 0.10))
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(mix(WHITE, GLOW, on), a), outline=A(NAVY, a), width=5)
    d.line([(x - 22, y + 10), (x - 10, y - 12), (x, y + 10), (x + 10, y - 12), (x + 22, y + 10)],
           fill=A(ORANGE if on else MUTED, a), width=4)

def vmeter(d, cx, cy, ac, a=1.0, r=40):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, a), outline=A(PURPLE, a), width=6)
    text(d, (cx, cy + 2), "V", 44, PURPLE, alpha=a)
    if ac: text(d, (cx + r + 22, cy - r * 0.6), "~", 48, PURPLE, alpha=a)

def circuit(d, ac, closed, vtxt, sa=1.0):
    w = 6
    d.line([(XL, AY - 44), (XL, TY), (LX - 46, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(LX + 46, TY), (XR, TY), (XR, KT)], fill=WIRE, width=w, joint="curve")
    d.line([(XR, KB), (XR, BY), (420, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(220, BY), (XL, BY), (XL, AY + 44)], fill=WIRE, width=w, joint="curve")
    # von ke song song den
    d.line([(LX - 90, TY), (LX - 90, VY), (LX - 40, VY)], fill=WIRE, width=5, joint="curve")
    d.line([(LX + 90, TY), (LX + 90, VY), (LX + 40, VY)], fill=WIRE, width=5, joint="curve")
    dot(d, LX - 90, TY, 9, WIRE); dot(d, LX + 90, TY, 9, WIRE)
    vmeter(d, LX, VY, ac)
    text(d, (LX, VY + 75), vtxt, 44, PURPLE if vtxt[0] != "…" else MUTED)
    lamp(d, LX, TY, 1.0 if closed else 0.0)
    text(d, (LX, 292), "đèn 6 V – 3 W", 40, INK)
    d.ellipse([XL - 44, AY - 44, XL + 44, AY + 44], fill=WHITE, outline=BLUE, width=6); text(d, (XL, AY + 2), "A", 44, BLUE)
    dot(d, XR, KT, 9, WIRE); dot(d, XR, KB, 9, WIRE)
    if closed: d.line([(XR, KB), (XR, KT)], fill=NAVY, width=7)
    else: d.line([(XR, KB), (XR - 52, KT + 14)], fill=NAVY, width=7)
    text(d, (XR + 42, (KT + KB) / 2), "K", 40, NAVY)
    card(d, (220, 650, 420, 750), fill=(245, 243, 255), outline=NAVY, r=16, w=4)
    text(d, (320, 700), "6 V ~" if ac else "6 V", 44, mix(BG, ORANGE, sa))
    if not ac:
        text(d, (200, 660), "+", 40, mix(BG, ORANGE, sa)); text(d, (440, 660), "−", 40, mix(BG, ORANGE, sa))

def ang(v): return math.radians(200 + 140 * clamp(v / I_MAX))
def dial(d, cx, cy, r, v, txt, alpha=1.0):
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=A(NAVY, alpha), width=5)
    for k in range(21):
        a = ang(k * 0.05); L = 30 if k % 10 == 0 else (20 if k % 2 == 0 else 12)
        d.line([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx + (r - L) * math.cos(a), cy + (r - L) * math.sin(a))],
               fill=A(NAVY, alpha), width=4 if k % 2 == 0 else 3)
    for lv in (0, 0.5, 1.0):
        a = ang(lv); s = "0" if lv == 0 else ("1" if lv == 1 else "0,5")
        text(d, (cx + (r - 58) * math.cos(a), cy + (r - 58) * math.sin(a)), s, 40, NAVY, alpha=alpha)
    a = ang(v)
    d.line([(cx, cy), (cx + (r - 18) * math.cos(a), cy + (r - 18) * math.sin(a))], fill=A(RED, alpha), width=7)
    dot(d, cx, cy, 13, A(NAVY, alpha))
    if txt: text(d, (cx, cy + 50), txt, 46, RED if txt[0] != "…" else MUTED, alpha=alpha)

def top(d, ac, closed, needle, txt, vtxt, sa=1.0):
    card(d, (40, 260, 1040, 780), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, ac, closed, vtxt, sa)
    card(d, (590, 290, 1020, 760), fill=(248, 250, 255), outline=LIGHT, r=24, w=3)
    text(d, (805, 336), "ampe kế", 40, BLUE)
    text(d, (805, 392), "xoay chiều" if ac else "một chiều", 40, mix(BG, NAVY, sa))
    dial(d, 805, 650, 190, needle, txt)

XS = (170, 470, 830)
def table(d, ndc, nac, hl=None, y=810, alpha=1.0, vdc=None, vac=None):
    vdc = ndc > 0 if vdc is None else vdc; vac = nac > 0 if vac is None else vac
    card(d, (40, y, 1040, y + 540), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS, ("Lần", "Một chiều", "Xoay chiều")): text(d, (x, y + 52), h, 40, INK, alpha=alpha)
    d.line([(70, y + 96), (1010, y + 96)], fill=A(LIGHT, alpha), width=3)
    for j in range(3):
        yy = y + 160 + j * 95
        text(d, (XS[0], yy), str(j + 1), 46, MUTED, alpha=alpha)
        for col, n, vals, c in ((1, ndc, DC, NAVY), (2, nac, AC, ORANGE)):
            if hl == (col, j): d.rounded_rectangle([XS[col] - 130, yy - 40, XS[col] + 130, yy + 40], radius=18, fill=A((255, 237, 213), alpha))
            text(d, (XS[col], yy), vn(vals[j]) + " A" if j < n else "·", 46 if j < n else 44, c if j < n else GRAY, alpha=alpha)
    yy = y + 160 + 3 * 95 + 10
    d.line([(70, yy - 52), (1010, yy - 52)], fill=A(LIGHT, alpha), width=3)
    text(d, (XS[0], yy), "Vôn kế", 40, PURPLE, alpha=alpha)
    for col, n, v in ((1, vdc, UV_DC), (2, vac, UV_AC)):
        text(d, (XS[col], yy), vn(v) + " V" if n else "·", 46 if n else 44, PURPLE if n else GRAY, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    top(d, False, False, 0.0, "0,00 A", "0,00 V")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 810 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 740), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 61), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 330, "Nguồn xoay chiều 6 V.\nVôn kế xoay chiều chỉ\nnhỏ hơn 6 V, đúng 6 V\nhay lớn hơn?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 660, 940, y0 + 672], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 660, 140 + 800 * (1 - p), y0 + 672], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_C1, T_O1, T_SW, T_C2 = 0.8, 4.2, 5.0, 5.5
READ = [1.4, 2.4, 3.4]; READ2 = [6.0, 7.0, 8.0]
T_N = 0.35
T_V1, T_V2 = T_C1 + T_N + 0.7, T_C2 + T_N + 0.7      # hang von ke ghi sau khi so V hien 0,7 s
def do_state(t):
    """-> (ac?, alpha doi nguon, K dong?, kim, chu ampe ke, chu von ke, so o mot chieu, so o xoay chieu, o dang to)."""
    ac = t >= T_SW; sa = clamp((t - T_SW) / 0.3) if ac else 1.0
    closed = (T_C1 <= t < T_O1) or t >= T_C2
    vals, reads, tc = (AC, READ2, T_C2) if ac else (DC, READ, T_C1)
    k = sum(1 for r in reads if t >= r)
    if not closed:
        prev = DC[-1]; nd = prev * (1 - ease((t - T_O1) / T_N)) if t >= T_O1 else 0.0
        return ac, sa, False, nd, ("0,00 A" if nd < 0.003 else "…"), "0,00 V", 3 if t >= T_O1 else 0, 0, None
    tgt = vals[max(k - 1, 0)]
    if k == 0: nd = tgt * ease((t - tc) / T_N)
    else:
        ts = reads[k - 1]; prev = vals[k - 2] if k >= 2 else vals[0]; nd = lerp(prev, tgt, ease((t - ts) / T_N))
        if k == 1: nd = tgt
    txt = vn(tgt) + " A" if abs(nd - tgt) < 0.002 and (k > 0 or t - tc > T_N) else "…"
    vtxt = vn(UV_AC if ac else UV_DC) + " V" if t - tc > T_N else "…"
    ndc = 3 if ac else sum(1 for r in READ if t >= r + T_N)
    nac = sum(1 for r in READ2 if t >= r + T_N) if ac else 0
    hl = (2, nac - 1) if ac and nac else ((1, ndc - 1) if not ac and ndc else None)
    return ac, sa, True, nd, txt, vtxt, ndc, nac, hl

def s_do(img, d, t, sc):
    ac, sa, closed, nd, txt, vtxt, ndc, nac, hl = do_state(t)
    top(d, ac, closed, nd, txt, vtxt, sa)
    table(d, ndc, nac, hl, vdc=t >= T_V1, vac=t >= T_V2)

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        ac, sa, closed, nd, txt, vtxt, ndc, nac, hl = do_state(t)
        if txt not in ("…", "0,00 A") and abs(float(txt[:-2].replace(",", ".")) - nd) > 0.003: bad.append((round(t, 2), "chu lech kim", txt, nd))
        if closed and not ac and ndc and txt != "…" and txt != vn(DC[ndc - 1]) + " A" and t < READ[min(ndc, 2)]:
            bad.append((round(t, 2), "bang DC lech so chi", ndc, txt))
        if closed and ac and nac and txt != "…" and txt != vn(AC[nac - 1]) + " A" and (nac == 3 or t < READ2[nac]):
            bad.append((round(t, 2), "bang AC lech so chi", nac, txt))
        if not closed and (txt not in ("…", "0,00 A") or vtxt != "0,00 V"): bad.append((round(t, 2), "K mo ma co so"))
        if (t >= T_V2 and (not ac or vtxt == "…")) or (T_V1 <= t < T_O1 and vtxt == "…"): bad.append((round(t, 2), "bang co U truoc von ke"))
        t += 0.05
    return bad

def _kiem_so():
    bad = []
    if abs(P_DM / U - 0.50) > 1e-9: bad.append("I = P/U khac 0,50")
    for v in DC + AC:
        if abs(v - P_DM / U) > DCNN + 1e-9: bad.append(("lech qua 1 do chia", v))
        if v > I_MAX: bad.append(("qua GHD", v))
    for uv, I in ((UV_DC, P_DM / U), (UV_AC, P_DM / U)):          # von ke chi U hieu dung hai dau den = U - I*R_A
        if abs(uv - (U - I * R_A)) > 1e-9: bad.append(("von ke", uv))
    if not U_HOI > U: bad.append("cau chot phai lon hon U dinh muc")
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · đúng 6 V"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    k = appear(t, 0.4, 0.4)
    for x0, nm, uv in ((40, "một chiều", UV_DC), (560, "xoay chiều", UV_AC)):
        card(d, (x0, 390, x0 + 480, 1100), fill=A(WHITE, k), outline=A(TEAL, k), w=5)
        text(d, (x0 + 240, 440), nm, 44, NAVY, alpha=k)
        vmeter(d, x0 + 240, 600, nm == "xoay chiều", a=k, r=70)
        text(d, (x0 + 240, 740), vn(uv) + " V", 60, PURPLE, alpha=k)
        kb = appear(t, M[1] - 0.1, 0.4) * k
        lamp(d, x0 + 240, 930, kb, a=kb, r=60)
    text(d, (W / 2, 1180), "đèn sáng như nhau", 46, INK, alpha=appear(t, M[1] + 0.3, 0.4))

# ---------------- canh 4: Bay roi Chua noi duoc (truoc Rut ra) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    vmeter(d, 540, 410, True, r=70)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 820), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        for j, q in enumerate(("“6 V~ là lúc nào", "cũng đúng 6 V”")):
            yy = y0 + 210 + j * 72; lw = tw(d, q, F(50))
            text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y0 + 360), "✗", 56, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 2.2, 0.4)
        card(d, (70, y0 + 440, 1010, y0 + 760), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 555), "✓ Luôn đổi; 6 V là", 52, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 645), "giá trị hiệu dụng", 52, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 700), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu minh hoạ", ""), ("• Bỏ qua điện trở", "ampe kế"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 270 + j * 250), l1, 50, INK, anchor="lm", alpha=kk)
            if l2: text(d, (132, y0 + 345 + j * 250), l2, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 820), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    for cx, nm in ((290, "một chiều"), (790, "xoay chiều")):
        text(d, (cx, 310), nm, 42, NAVY, alpha=k0)
        lamp(d, cx, 480, k0, a=k0, r=62)
        kh = appear(t, 0.8, 0.4) * k0
        for j in range(3):
            x = cx - 50 + j * 50
            d.line([(x, 640), (x + 10, 655), (x, 670), (x + 10, 685), (x, 700)], fill=A(RED, kh), width=4)
        text(d, (cx - 110, 760), "nóng", 40, RED, alpha=kh); text(d, (cx + 100, 760), "sáng", 40, ORANGE, alpha=kh)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 <= 0: return
    card(d, (40, 860, 1040, 1380), fill=A(WHITE, k1), outline=A(PURPLE, k1), w=4)
    vmeter(d, 300, 1060, True, a=k1, r=80)
    text(d, (300, 1200), "6 V ~", 50, ORANGE, alpha=k1)
    text(d, (720, 1030), "số chỉ là", 48, INK, alpha=k1)
    text(d, (720, 1110), "giá trị hiệu dụng", 48, PURPLE, alpha=k1)
    text(d, (W / 2, 1300), "(làm nóng như một chiều 6 V)", 44, INK, alpha=appear(t, M[1] + 0.6, 0.4))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.6                                    # >= 4 s sau cau hoi (M0 + 0.4)
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 260, 1040, 1060), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(40)) + 52
        card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 322), "THỬ NGHĨ", 40, WHITE, alpha=k1)
        ctext(d, 460, f"Nguồn {U_HOI} V xoay chiều.\nĐèn 6 V – 3 W thế nào?", 48, INK, maxw=900,
              alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        lamp(d, 400, 650, 0.0, a=ka, r=56)
        text(d, (640, 650), f"{U_HOI} V ~", 52, ORANGE, alpha=ka)
        text(d, (820, 650), "?", 60, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.4, 0.5)
        card(d, (110, 800, 970, 1020), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 910, "So với số ghi trên đèn.", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 1110, 1020, 1420), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 1265, "Xoay chiều: nóng, sáng\nnhư một chiều", 50, GREEN, maxw=900, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
          (do["t0"] + T_C1, "tap"), (do["t0"] + T_C2, "tap"),
          (da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (b["t0"] + b["M"][0] + 2.2, "tap"),
          (r["t0"] + r["M"][1] - 0.1, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-xoaychieu-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Dòng điện xoay chiều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Một đèn, hai loại nguồn", draw=s_hook, tail=0.7, caps=[
   ("Vôn kế mắc hai đầu đèn.", 3.0),
   ("Tự trả lời trước khi xem.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Một chiều: đọc 3 lần.", 4.4),
   ("Đổi sang xoay chiều, đọc 3 lần.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Vôn kế chỉ như nhau.", 3.0),
   ("Đèn cũng sáng như nhau.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Có đúng không?", 3.8),
   ("Còn chưa nói được.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Xoay chiều cũng làm nóng, làm sáng.", 3.6),
   ("Số chỉ là giá trị hiệu dụng.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước khi xem.", 6.4)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
