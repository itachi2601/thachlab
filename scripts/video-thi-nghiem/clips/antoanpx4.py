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
from engine import *

WEEKS = [0.12, 0.09, 0.15, 0.10]           # so_lieu_mau (mSv)
TONG, TB, NAM, GH = "0,46", "0,115", "5,8", 20
NOTE = (70, 75, 95)
TEAL_L = (204, 240, 236)
def vn(x): return f"{x:.2f}".replace(".", ",")

def badge(d, x, y, s=1.0, a=1.0, lab=None):
    w, h = 70 * s, 92 * s
    d.rounded_rectangle([x - w, y - h, x + w, y + h], radius=int(16 * s), fill=A(WHITE, a), outline=A(NAVY, a), width=5)
    d.rectangle([x - w + 10 * s, y - h + 14 * s, x + w - 10 * s, y - h + 50 * s], fill=A(TEAL, a))
    for k in range(3): dot(d, x - 34 * s + k * 34 * s, y + 22 * s, 13 * s, A((226, 214, 196), a), A(NAVY, a))
    text(d, (x, y + 66 * s), "TLD", int(36 * s), NAVY, alpha=a)
    if lab: text(d, (x, y - h - 34), lab, 44, NOTE, alpha=a)

def person(d, x, y):
    dot(d, x, y - 260, 70, (244, 214, 186), NAVY)
    d.rounded_rectangle([x - 130, y - 175, x + 130, y + 170], radius=60, fill=(147, 197, 253), outline=NAVY, width=5)
    badge(d, x - 50, y - 70, 0.55)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    person(d, 260, 720)
    card(d, (520, 300, 1020, 820), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (770, 370), "Sổ ghi liều", 46, NOTE)
    text(d, (770, 520), "4 tuần", 60, INK)
    text(d, (770, 660), f"tổng {TONG} mSv", 54, TEAL)
    a = appear(t, M[1] - 0.6, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 430), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 175), "Làm như vậy 50 tuần.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Liều năm khoảng bao nhiêu?", 50, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 370, 940, y0 + 384], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 370, 140 + 800 * (1 - p), y0 + 384], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: doc lieu ke tung tuan, ghi so ----------------
SLIDE, READ = 0.5, 0.3
def week_at(i, sc): return sc["M"][0] + 0.2 + i * 1.1

def do_state(t, sc):
    """(tuan dang doc, muc truot, so tren may doc, so hang da ghi) -- may doc va bang doi cung moc."""
    wk, k, rd, n = -1, 0.0, "···", 0
    for i in range(4):
        s = week_at(i, sc)
        if t < s: break
        wk = i; k = clamp((t - s) / SLIDE)
        if t >= s + SLIDE + READ: rd = vn(WEEKS[i]); n = i + 1
        else: rd = "···"
    return wk, k, rd, n

ROW_Y0, ROW_H = 1150, 78
BX0, BX1 = 470, 930                          # thanh ngang: 0 -> 0,20 mSv (truc tu 0)
def s_do(img, d, t, sc):
    M = sc["M"]
    wk, k, rd, n = do_state(t, sc)
    # may doc
    card(d, (500, 280, 1020, 760), fill=(226, 232, 240), outline=NAVY, r=28, w=5)
    text(d, (760, 330), "Máy đọc liều", 44, NOTE)
    d.rounded_rectangle([560, 370, 960, 490], radius=16, fill=NAVY)
    text(d, (760, 430), f"{rd} mSv" if rd != "···" else rd, 62, (134, 239, 172))
    d.rectangle([580, 560, 720, 590], fill=NAVY); d.rectangle([800, 560, 940, 590], fill=NAVY)       # hai khe
    badge(d, 870, 650, 0.38)
    text(d, (870, 728), "chuẩn", 44, NOTE)
    # lieu ke cua tuan dang doc truot vao khe trai
    if wk >= 0:
        x = lerp(250, 650, ease(k)); y = lerp(520, 650, ease(k))
        badge(d, x, y, 0.38 if k > 0.6 else lerp(0.6, 0.38, (k / 0.6)))
        text(d, (250, 360), f"tuần {wk + 1}", 52, INK)
    ka = appear(t, 0.4, 0.4)
    text(d, (W / 2, 850), "Trừ phông bằng liều kế chuẩn", 44, NOTE, bold=False, alpha=ka)
    # bang so ghi lieu
    card(d, (60, 960, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    text(d, (180, 1020), "Tuần", 44, NOTE); text(d, (330, 1020), "mSv", 44, NOTE)
    for v, lb in ((0.0, "0"), (0.1, "0,1"), (0.2, "0,2")):
        x = BX0 + v / 0.2 * (BX1 - BX0)
        d.line([(x, 1060), (x, ROW_Y0 + 4 * ROW_H - 40)], fill=(236, 230, 220), width=2)
        text(d, (x, 1020), lb, 44, NOTE, bold=False)
    d.line([(90, 1066), (990, 1066)], fill=LIGHT, width=4)
    for i in range(4):
        y = ROW_Y0 + i * ROW_H
        if i >= n: continue
        a = appear(t, week_at(i, sc) + SLIDE + READ, 0.3)
        text(d, (180, y), str(i + 1), 46, INK, alpha=a)
        text(d, (330, y), vn(WEEKS[i]), 46, INK, alpha=a)
        x1 = BX0 + WEEKS[i] / 0.2 * (BX1 - BX0) * ease(a)
        if x1 - BX0 > 2: d.rectangle([BX0, y - 22, x1, y + 22], fill=TEAL)
    kt = appear(t, M[1] + 0.2, 0.4)
    if kt > 0:
        y = ROW_Y0 + 4 * ROW_H + 16
        d.line([(90, y - 44), (990, y - 44)], fill=A(NAVY, kt), width=4)
        text(d, (180, y + 12), "Tổng", 46, TEAL, alpha=kt); text(d, (330, y + 12), TONG, 50, TEAL, alpha=kt)

# ---------------- canh 3: Dap an: chia 4, nhan 50, so voi 20 ----------------
def s_ans(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.3, 0.4)
    s = f"ĐÁP ÁN · khoảng {NAM} mSv"
    pw = tw(d, s, F(42)) + 56
    card(d, (W / 2 - pw / 2, 236, W / 2 + pw / 2, 304), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 270), s, 42, WHITE, alpha=ka)
    card(d, (60, 330, 1020, 600), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 410), f"{TONG} : 4 = {TB} mSv/tuần", 50, INK, alpha=appear(t, 0.7, 0.4))
    text(d, (W / 2, 520), f"{TB} × 50 ≈ {NAM} mSv/năm", 50, TEAL, alpha=appear(t, 2.0, 0.4))
    # cot lieu nam, truc tu 0, vach gioi han 20
    kc = appear(t, M[1] - 0.1, 0.4)
    if kc <= 0: return
    card(d, (60, 640, 1020, 1600), fill=A(WHITE, kc), outline=A(LIGHT, kc), w=3)
    yb, yt = 1480, 800; Y = lambda v: yb - v / 25 * (yb - yt)
    d.line([(230, yb), (960, yb)], fill=A(NAVY, kc), width=5); d.line([(230, yb), (230, yt - 30)], fill=A(NAVY, kc), width=5)
    text(d, (250, 710), "mSv/năm", 44, NOTE, bold=False, anchor="lm", alpha=kc)
    for v in (0, 5, 10, 15, 20, 25):
        d.line([(220, Y(v)), (230, Y(v))], fill=A(NAVY, kc), width=4)
        text(d, (205, Y(v)), str(v), 44, NOTE, bold=False, anchor="rm", alpha=kc)
    gh = appear(t, M[1] + 0.2, 0.4)
    for xx in range(240, 950, 28): d.line([(xx, Y(GH)), (min(xx + 16, 950), Y(GH))], fill=A(RED, gh), width=6)
    text(d, (950, Y(GH) - 36), "giới hạn nghề nghiệp", 44, RED, anchor="rm", alpha=gh)
    g = ease((t - M[1] - 0.6) / 0.6)
    if g > 0:
        top = yb - (yb - Y(5.75)) * g
        if yb - top > 2: d.rectangle([420, top, 580, yb], fill=TEAL)
        text(d, (500, top - 34), f"{NAM}", 48, TEAL, alpha=clamp(g * 2 - 1))

# ---------------- canh 4: rut ra + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    M = sc["M"]
    a = appear(t, 0.2, 0.4)
    card(d, (60, 260, 1020, 700), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    badge(d, 200, 470, 0.8, a)
    text(d, (330, 400), "Liều phải đo và ghi sổ,", 48, INK, anchor="lm", alpha=a)
    text(d, (330, 480), "không đoán.", 48, INK, anchor="lm", alpha=a)
    b = appear(t, M[1] - 0.1, 0.4)
    if b <= 0: return
    card(d, (60, 750, 1020, 1120), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 815), "Chưa nói được gì?", 48, PURPLE, alpha=b)
    text(d, (120, 930), "• Có tuần gặp sự cố?", 46, INK, anchor="lm", alpha=b)
    text(d, (120, 1040), "• Liều ở tay, ở mắt?", 46, INK, anchor="lm", alpha=appear(t, M[1] + 1.4, 0.4))

# ---------------- canh 5: bay ----------------
def quote(d, y, q, ks, a):
    f = F(46); lw = tw(d, q, f)
    text(d, (W / 2, y), q, 46, mix(INK, GRAY, ks), alpha=a)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, y + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, y + 2)], fill=A(RED, 0.85), width=6)

def s_bay(img, d, t, sc):
    M = sc["M"]; m1, m2 = M[0] + 2.4, M[1] - 0.2
    a1 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 620), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY 1", F(40)) + 52
    card(d, (W / 2 - pw / 2, 276, W / 2 + pw / 2, 340), fill=A(RED, a1), r=32)
    text(d, (W / 2, 308), "BẪY 1", 40, WHITE, alpha=a1)
    quote(d, 430, f"“{TONG} mSv là liều cả năm”", clamp((t - m1) / 0.4), a1)
    text(d, (W / 2, 540), "Mới 4 tuần", 48, GREEN, alpha=appear(t, m1 + 0.2, 0.4))
    a2 = appear(t, m1 + 0.7, 0.4)
    card(d, (40, 660, 1040, 1520), fill=A(WHITE, a2), outline=A(RED, a2), w=6)
    pw = tw(d, "BẪY 2", F(40)) + 52
    card(d, (W / 2 - pw / 2, 686, W / 2 + pw / 2, 750), fill=A(RED, a2), r=32)
    text(d, (W / 2, 718), "BẪY 2", 40, WHITE, alpha=a2)
    quote(d, 840, "“Một tuần 20 mSv cũng không sao”", clamp((t - m2) / 0.4), a2)
    kb = appear(t, m2 + 0.2, 0.45)
    if kb > 0:
        yb, yt = 1330, 960; Y = lambda v: yb - v / 25 * (yb - yt)
        d.line([(200, yb), (900, yb)], fill=A(NAVY, kb), width=5)
        for xx in range(200, 900, 28): d.line([(xx, Y(GH)), (min(xx + 16, 900), Y(GH))], fill=A(RED, kb), width=6)
        text(d, (900, Y(GH) - 34), "20 mSv/năm", 44, RED, anchor="rm", alpha=kb)
        g = ease((t - m2 - 0.5) / 0.6)
        if g > 0 and (yb - Y(GH)) * g > 2: d.rectangle([300, yb - (yb - Y(GH)) * g, 420, yb], fill=RED)
        text(d, (360, yb + 42), "1 tuần", 44, NOTE, bold=False, alpha=kb)
        text(d, (W / 2, 1450), "Hết hạn mức năm", 48, GREEN, alpha=appear(t, m2 + 1.3, 0.4))

# ---------------- canh 6: chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    for i in range(50):                         # 50 o = 50 tuan lam viec
        x = 190 + (i % 10) * 72; y = 1010 + (i // 10) * 52
        d.rounded_rectangle([x, y, x + 56, y + 38], radius=8, fill=A(TEAL_L, k), outline=A(TEAL, k), width=3)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Đo liều, cộng dồn, so giới hạn năm",
             "Mỗi tuần 0,5 mSv, làm 50 tuần:\ncó vượt 20 mSv/năm không?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1360, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1450, "Mỗi ô là một tuần", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, wy, b, e = sc["hook"], sc["do"], sc["ans"], sc["why"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + week_at(i, do) + SLIDE + READ, "tap") for i in range(4)]
    out += [(an["t0"] + 0.3, "ding"), (wy["t0"] + wy["M"][1] - 0.1, "tap"),
            (b["t0"] + b["M"][0] + 2.4, "buzz"), (b["t0"] + b["M"][1] - 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-antoanpx-04", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phóng xạ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Liều kế cá nhân", draw=s_hook, tail=0.3, caps=[
   ("Kỹ thuật viên đeo liều kế ở ngực.", 2.9),
   ("Chọn đáp án ở khung câu hỏi.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Mỗi tuần gửi đọc một liều kế.", 4.6),
   ("Cộng bốn tuần vào sổ.", 2.9)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.5, caps=[
   ("Chia 4 tuần, rồi nhân 50.", 3.4),
   ("So với vạch giới hạn.", 3.4)]),
 dict(key="why", title="Rút ra", draw=s_why, tail=0.4, caps=[
   ("Liều kế cho số thật.", 3.0),
   ("Chưa trả lời được.", 3.6)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.4, caps=[
   ("Đúng hay sai?", 5.4),
   ("Cả hai đều sai.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng video và trả lời.", 6.0)]),
])
