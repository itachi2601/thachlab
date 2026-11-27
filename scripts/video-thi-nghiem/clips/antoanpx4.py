# Clip: tn-l12-antoanpx-04 - Doc lieu ke ca nhan TLD 4 tuan, suy ra lieu nam (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-antoanpx-04.json:
#   so_lieu_mau: tuan 1-4 = 0,12; 0,09; 0,15; 0,10 mSv (da tru lieu phong phong doc) -> tong 0,46 (ghi_chu).
#   mo_hinh: L_tb = 0,46/4 = 0,115 mSv/tuan; L_nam = 0,115 x 50 (so_tuan_nam, tham_so) = 5,75 ~ 5,8 mSv; gioi han 20 mSv/nam.
#   hien_tuong_hay_sai #2 (lieu ghi la lieu ca nam), #3 (vuot 20 mSv mot tuan la nho). khong_chung_minh: tuan co su co; lieu tay/mat.
# Du doan (khung ben canh, K10 khong ve nut; "deo 4 tuan, tong 0,46 mSv; lam nhu the 50 tuan, lieu nam khoang bao nhieu?"):
#   A. Khoang 0,46 mSv (coi tong 4 tuan la lieu nam, hien_tuong_hay_sai #2)
#   B. Khoang 5,8 mSv  <- dung (ket_qua_ky_vong)
#   C. Khoang 23 mSv (nham: nhan TONG 4 tuan voi 50 = 0,46 x 50; so nhieu tu loi tinh, khong phai so do)
# Cau chot (ca moi, khong trung Du doan): moi tuan doc 0,5 mSv (tham_so L_tuan max = 0,5), 50 tuan -> 25 mSv > 20: vuot.
# Dung lai 26/11/2026 (viec 4 lo 32): cong --do-chu, chu >= 56 px, <= 50 s; mot bay (#3: 20 mSv mot tuan), bo the goi y o canh chot.
from engine import *

WEEKS = [0.12, 0.09, 0.15, 0.10]           # so_lieu_mau (mSv)
TONG, TB, NAM, GH = "0,46", "0,115", "5,8", 20
NOTE = (70, 75, 95)
TEAL_L = (204, 240, 236)
def vn(x): return f"{x:.2f}".replace(".", ",")

DORANGE = (154, 52, 18)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def badge(d, x, y, s=1.0, a=1.0, glow=0.0):
    w, h = 70 * s, 92 * s
    if glow > 0: d.rounded_rectangle([x - w - 14, y - h - 14, x + w + 14, y + h + 14], radius=int(24 * s), outline=A(ORANGE, glow), width=8)
    d.rounded_rectangle([x - w, y - h, x + w, y + h], radius=int(16 * s), fill=A(WHITE, a), outline=A(NAVY, a), width=5)
    d.rectangle([x - w + 10 * s, y - h + 14 * s, x + w - 10 * s, y - h + 50 * s], fill=A(TEAL, a))
    for k in range(3): dot(d, x - 34 * s + k * 34 * s, y + 22 * s, 13 * s, A((226, 214, 196), a), A(NAVY, a))

def person(d, x, y, t=0.0):
    dot(d, x, y - 260, 70, (244, 214, 186), NAVY)
    d.rounded_rectangle([x - 130, y - 175, x + 130, y + 170], radius=60, fill=(147, 197, 253), outline=NAVY, width=5)
    badge(d, x - 50, y - 70, 0.55, glow=0.5 + 0.5 * math.sin(t * 4))

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    person(d, 260, 720, t)
    card(d, (520, 330, 1020, 800), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (770, 500), "4 tuần", 64, INK)
    text(d, (770, 600), f"{TONG} mSv", 64, TEAL)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 130, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 290), "Làm vậy 50 tuần:", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 390), "liều năm bao nhiêu?", 62, PURPLE, alpha=a)

# ---------------- canh 2: doc lieu ke tung tuan, ghi so ----------------
SLIDE, READ = 0.5, 0.3
def week_at(i, sc): return 2.0 + i * 1.1

def do_state(t, sc):
    wk, k, rd, n = -1, 0.0, "···", 0
    for i in range(4):
        s = week_at(i, sc)
        if t < s: break
        wk = i; k = clamp((t - s) / SLIDE)
        if t >= s + SLIDE + READ: rd = vn(WEEKS[i]); n = i + 1
        else: rd = "···"
    return wk, k, rd, n

ROW_Y0, ROW_H = 1150, 88
BX0, BX1 = 540, 950
def s_do(img, d, t, sc):
    M = sc["M"]
    wk, k, rd, n = do_state(t, sc)
    card(d, (500, 280, 1020, 760), fill=(226, 232, 240), outline=NAVY, r=28, w=5)
    text(d, (760, 335), "Máy đọc", 56, NOTE)
    d.rounded_rectangle([560, 380, 960, 500], radius=16, fill=NAVY)
    text(d, (760, 440), f"{rd} mSv" if rd != "···" else rd, 62, (134, 239, 172))
    d.rectangle([600, 600, 920, 630], fill=NAVY)
    if wk >= 0:
        x = lerp(250, 760, ease(k)); y = lerp(560, 690, ease(k))
        badge(d, x, y, lerp(0.8, 0.45, ease(k)))
    else:
        badge(d, 250, 560, 0.8, glow=0.5 + 0.5 * math.sin(t * 4))
    card(d, (60, 960, 1020, 1640), fill=WHITE, outline=NAVY, w=4)
    text(d, (160, 1025), "Tuần", 56, NOTE); text(d, (330, 1025), "mSv", 56, NOTE)
    d.line([(440, 990), (440, 1610)], fill=LIGHT, width=4)
    for v, lb in ((0.0, "0"), (0.1, "0,1"), (0.2, "0,2")):
        x = BX0 + v / 0.2 * (BX1 - BX0)
        d.line([(x, 1070), (x, ROW_Y0 + 4 * ROW_H - 40)], fill=(236, 230, 220), width=2)
        text(d, (x, 1025), lb, 56, NOTE)
    d.line([(90, 1072), (990, 1072)], fill=LIGHT, width=4)
    for i in range(4):
        y = ROW_Y0 + i * ROW_H
        if i >= n: continue
        a = appear(t, week_at(i, sc) + SLIDE + READ, 0.3)
        text(d, (160, y), str(i + 1), 56, INK, alpha=a)
        text(d, (330, y), vn(WEEKS[i]), 56, INK, alpha=a)
        x1 = BX0 + WEEKS[i] / 0.2 * (BX1 - BX0) * ease(a)
        if x1 - BX0 > 2: d.rectangle([BX0, y - 24, x1, y + 24], fill=TEAL)
    kt = appear(t, week_at(3, sc) + SLIDE + READ + 1.0, 0.4)
    if kt > 0:
        y = ROW_Y0 + 4 * ROW_H + 20
        d.line([(90, y - 48), (990, y - 48)], fill=A(NAVY, kt), width=4)
        text(d, (160, y + 10), "Tổng", 56, TEAL, alpha=kt); text(d, (330, y + 10), TONG, 60, TEAL, alpha=kt)

# ---------------- canh 3: Dap an: chia 4, nhan 50, so voi 20 ----------------
def s_ans(img, d, t, sc):
    pill(d, W / 2, 290, f"ĐÁP ÁN: {NAM} mSv", NAVY)
    card(d, (60, 360, 1020, 620), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 440), f"{TONG} : 4 = {TB}", 60, INK, alpha=appear(t, 1.6, 0.4))
    text(d, (W / 2, 550), f"{TB} × 50 ≈ {NAM} mSv/năm", 58, TEAL, alpha=appear(t, 3.8, 0.4))
    kc = appear(t, 6.0, 0.4)
    if kc <= 0: return
    card(d, (60, 660, 1020, 1560), fill=A(WHITE, kc), outline=A(LIGHT, kc), w=3)
    yb, yt = 1460, 820; Y = lambda v: yb - v / 25 * (yb - yt)
    d.line([(160, yb), (960, yb)], fill=A(NAVY, kc), width=5); d.line([(160, yb), (160, yt - 30)], fill=A(NAVY, kc), width=5)
    for xx in range(170, 950, 28): d.line([(xx, Y(GH)), (min(xx + 16, 950), Y(GH))], fill=A(RED, kc), width=6)
    text(d, (950, Y(GH) - 44), "giới hạn 20", 56, RED, anchor="rm", alpha=kc)
    g = ease((t - 6.3) / 0.6)
    if g > 0:
        top = yb - (yb - Y(5.75)) * g
        if yb - top > 2: d.rectangle([300, top, 460, yb], fill=TEAL)
        text(d, (380, top - 40), NAM, 60, TEAL, alpha=clamp(g * 2 - 1))

# ---------------- canh 4: rut ra + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    M = sc["M"]
    a = appear(t, 0.2, 0.4)
    card(d, (60, 260, 1020, 640), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    badge(d, 190, 450, 0.8, a, glow=a * (0.5 + 0.5 * math.sin(t * 4)))
    text(d, (620, 400), "Đo bằng liều kế,", 58, INK, alpha=a)
    text(d, (620, 490), "ghi sổ", 58, INK, alpha=a)
    b = appear(t, M[1] - 0.1, 0.4)
    if b <= 0: return
    card(d, (60, 700, 1020, 1120), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 820), "Tuần có sự cố?", 58, INK, alpha=b)
    text(d, (W / 2, 990), "Liều ở tay, mắt?", 58, INK, alpha=appear(t, M[1] + 1.9, 0.4))

# ---------------- canh 5: bay "mot tuan 20 mSv cung khong sao" ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 560), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 320, "BẪY", RED, a1)
    text(d, (W / 2, 420), "“Một tuần 20 mSv", 60, INK, alpha=a1)
    text(d, (W / 2, 500), "cũng không sao”?", 60, INK, alpha=a1)
    kb = appear(t, 2.6, 0.45)
    if kb <= 0: return
    card(d, (40, 600, 1040, 1420), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
    yb, yt = 1290, 760; Y = lambda v: yb - v / 25 * (yb - yt)
    d.line([(160, yb), (960, yb)], fill=A(NAVY, kb), width=5)
    for xx in range(170, 950, 28): d.line([(xx, Y(GH)), (min(xx + 16, 950), Y(GH))], fill=A(RED, kb), width=6)
    text(d, (950, Y(GH) - 44), "20 mSv/năm", 56, RED, anchor="rm", alpha=kb)
    g = ease((t - 3.0) / 0.6)
    if g > 0:
        pulse = 0.5 + 0.5 * math.sin(t * 5)
        d.rectangle([260, yb - (yb - Y(GH)) * g, 420, yb], fill=mix(RED, (252, 165, 165), pulse * 0.6))
        top = yb - (yb - Y(5.75)) * g
        d.rectangle([620, top, 780, yb], fill=TEAL)
        text(d, (700, top - 40), NAM, 60, TEAL, alpha=clamp(g * 2 - 1))
    text(d, (340, yb + 60), "1 tuần", 56, NOTE, alpha=kb)
    text(d, (700, yb + 60), "cả năm", 56, NOTE, alpha=kb)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1450), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 570), "Làm đủ 50 tuần:", 60, INK, alpha=k1)
    text(d, (W / 2, 665), "vượt 20 mSv/năm không?", 60, DORANGE, alpha=k1)
    nf = int(clamp((t - 0.8) / 5.0) * 50)                # 50 o = 50 tuan, to dan; khong hien tong
    for i in range(50):
        x = 110 + (i % 10) * 66; y = 800 + (i // 10) * 86
        d.rounded_rectangle([x, y, x + 52, y + 58], radius=8, fill=A(TEAL if i < nf else TEAL_L, k1), outline=A(TEAL, k1), width=3)
    km = appear(t, 4.6, 0.4)                             # moc o thu 40 = 20 mSv
    if km > 0:
        ym = 800 + 4 * 86 - 14
        for xx in range(96, 780, 26): d.line([(xx, ym), (min(xx + 15, 780), ym)], fill=A(RED, km), width=7)
        text(d, (800, ym), "20 mSv", 56, RED, anchor="lm", alpha=km)
    kl = appear(t, 2.4, 0.4)
    text(d, (W / 2, 1310), "mỗi ô = 1 tuần (0,5 mSv)", 56, TEAL, alpha=kl * k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, e = sc["hook"], sc["do"], sc["ans"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + week_at(i, do) + SLIDE + READ, "tap") for i in range(4)]
    out += [(an["t0"] + 0.2, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

SCENES = [
 dict(key="hook", title="Liều kế cá nhân", draw=s_hook, tail=0.2, caps=[
   ("Liều kế đeo ở ngực.", 3.4),
   ("Dừng lại, tự đoán.", 4.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Mỗi tuần đọc một liều kế.", 4.6),
   ("Cộng bốn tuần vào sổ.", 3.2)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Chia 4, rồi nhân 50 tuần.", 3.8),
   ("Dưới vạch giới hạn năm.", 3.8)]),
 dict(key="why", title="Rút ra", draw=s_why, tail=0.2, caps=[
   ("Liều kế cho số thật.", 3.4),
   ("Hai điều chưa biết:", 3.8)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.4, caps=[
   ("Đúng hay sai?", 2.8),
   ("Sai: hết hạn mức cả năm.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=3.8, caps=[
   ("Cộng dồn, so giới hạn.", 3.8)]),
]

CLIP = dict(id="tn-l12-antoanpx-04", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phóng xạ · thachlab.id.vn", scenes=SCENES)
