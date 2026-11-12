# Clip bay phu dao L12 Ch.2 so 04 - Nen nhanh khong con dang nhiet (topic 206 "Qua trinh dang nhiet va dinh luat Boyle",
# lesson_topic 62, bai l12-boyle-charles). Theo mau bay-ch1-04 (the sai -> the dung).
# TU SOAN (khong co cau that cung bay trong 30 ngay toi 12/11/2026).
#   "Bit dau bom, an that nhanh pit-tong de the tich khi con mot nua. Ngay sau khi nen, ap suat khi..."
#   A. lon hon 2 lan  <- DUNG   B. dung bang 2 lan (ap Boyle may moc)   C. nho hon 2 lan (nghi khi mat nhiet khi nen)
#   D. khong doi (nghi nen nhanh khi "chua kip" doi ap suat).
# Kiem (chi kien thuc L12): nen nhanh -> khi chua kip truyen nhiet ra ngoai, Q ~ 0; khi nhan cong A > 0 -> dU = A + Q > 0 -> T tang.
#   pV/T = hang so -> p2 = p1.(V1/V2).(T2/T1) = 2p1.(T2/T1) > 2p1. Khong dung pV^gamma tren man.
#   Hinh (chi de ve, khong ghi so): T2/T1 = 2^0,4 ~ 1,32 -> p2 ~ 2,64 p1; thanh p vuot vach 2p1.
# THU NGHI (ca khac): giu yen pit-tong cho khi nguoi ve nhiet do phong -> dang tich ve T1 -> p = 2p1. Tren man khong noi dieu nay.
from clips.bay_chung import *

QY = 830
Q_LINES = ["Bịt đầu bơm, ấn thật nhanh pit-tông", "để thể tích khí còn một nửa.", "Ngay sau khi nén, áp suất khí…"]
OPTS = ["lớn hơn 2 lần", "đúng bằng 2 lần", "nhỏ hơn 2 lần", "không đổi"]
ANS = 0
XL, YT, YB = 120, 430, 590          # day bit, thanh tren/duoi ong bom
XP0 = 740                            # mat trai pit-tong luc dau; V/2 -> XP1
G0 = XL + 8
XP1 = G0 + (XP0 - G0) / 2
R = random.Random(7); DOTS = [(R.uniform(0.05, 0.95), R.uniform(0.1, 0.9), R.uniform(0, 6.28)) for _ in range(20)]
PX0, PK = 160, 260                   # thanh ap suat: x tai p = 0, px moi p1


def state(xp):
    r = (XP0 - G0) / (xp - G0); tr = r ** 0.4     # tr = T/T1 (chi de ve)
    return r, tr, r * tr


def pump(d, t, xp, tr, glow=0.0):
    hot = clamp((tr - 1) / 0.32)
    d.rectangle([G0, YT, xp, YB], fill=mix((224, 236, 255), (255, 214, 190), hot))
    amp = 5 + 9 * hot
    for u, v, ph in DOTS:
        x = G0 + 14 + u * (xp - G0 - 28) + amp * math.sin((8 + 10 * hot) * t + ph)
        y = YT + 14 + v * (YB - YT - 28) + amp * math.cos((7 + 10 * hot) * t + 2 * ph)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=mix(BLUE, RED, hot))
    wall = mix(NAVY, ORANGE, glow)
    d.line([(800, YT), (XL, YT), (XL, YB), (800, YB)], fill=wall, width=10)
    d.rectangle([XL - 18, YT - 10, XL, YB + 10], fill=wall)                  # dau bit
    d.rectangle([xp, YT + 6, xp + 28, YB - 6], fill=GRAY)                    # pit-tong
    d.rectangle([xp + 28, 500, xp + 240, 520], fill=GRAY)                    # can
    d.rectangle([xp + 240, 450, xp + 262, 570], fill=NAVY)                   # tay nam
    # nhiet ke cam qua thanh tren
    d.rounded_rectangle([222, 300, 242, 470], radius=10, fill=WHITE, outline=INK, width=3)
    d.ellipse([214, 462, 250, 498], fill=RED)
    top = 420 - 110 * hot
    d.rectangle([228, top, 236, 470], fill=RED)
    text(d, (262, 330), "t", 40, INK, anchor="lm")


def gauge(d, p, boyle=0.0):
    y = 690
    d.rounded_rectangle([PX0, y - 18, PX0 + 3 * PK, y + 18], radius=18, fill=WHITE, outline=GRAY, width=3)
    col = BLUE if p <= 2.02 else RED
    x = PX0 + PK * min(p, 3.0)
    if x - PX0 > 20: d.rounded_rectangle([PX0, y - 18, x, y + 18], radius=18, fill=col)
    text(d, (PX0 - 20, y), "p", 42, INK, anchor="rm")
    for k, s in ((1, "p₁"), (2, "2p₁")):
        xx = PX0 + PK * k
        if k == 1: d.line([(xx, y - 30), (xx, y + 30)], fill=INK, width=4)
        else: dash_line(d, (xx, y - 44), (xx, y + 34), INK, w=4, seg=10, gap=7)
        text(d, (xx, y + 62), s, 40, INK)
    if boyle > 0:
        text(d, (PX0 + PK * 2, y - 62), "Boyle dự đoán", 36, MUTED, alpha=boyle)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    pump(d, t, XP0, 1.0); gauge(d, 1.0)
    d.line([(960, 395), (840, 395)], fill=ORANGE, width=9); chevron(d, 840, 395, math.pi, ORANGE, s=24, w=8)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    pump(d, t, XP0, 1.0); gauge(d, 1.0)
    answer_pill(d, 1000, "A", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    xp = lerp(XP0, XP1, ease((t - 0.5) / 0.5))       # nen trong 0,5 s
    r, tr, p = state(xp)
    kg = appear(t, 1.2, 0.5)
    pump(d, t, xp, tr, glow=kg); gauge(d, p, boyle=appear(t, m0 + 0.9, 0.4))
    badge(d, 760, 360, "ống bơm ấm lên", ORANGE, kg, size=36)
    ka = appear(t, m0 + 0.9, 0.45) * (1 - appear(t, m1 - 0.1, 0.3))
    if ka > 0:   # the sai
        y = 820 + (1 - ka) * 30
        card(d, (60, y, 1020, y + 140), fill=A(WHITE, ka), outline=A(RED, ka), w=5)
        text(d, (W / 2, y + 70), "Sai: pV không đổi → p = 2p₁  ✗", 46, RED, alpha=ka)
    kb = appear(t, m1 + 0.3, 0.45)
    if kb > 0:   # the dung
        y = 820 + (1 - kb) * 30
        card(d, (60, y, 1020, y + 420), fill=A(WHITE, kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, y + 66), "Nén nhanh: chưa kịp toả nhiệt, Q ≈ 0", 42, INK, alpha=kb)
        k2 = appear(t, m1 + 1.3, 0.4) * kb
        text(d, (W / 2, y + 176), "A > 0 → ΔU > 0 → T tăng", 44, ORANGE, alpha=k2)
        k3 = appear(t, m1 + 2.4, 0.4) * kb
        text(d, (W / 2, y + 310), "p₂ = 2p₁ · T₂/T₁ > 2p₁", 50, GREEN, alpha=k3)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Nén nhanh: T tăng, p tăng hơn 2 lần",
             "Giữ yên pit-tông, chờ khí nguội\nvề nhiệt độ phòng: p bằng mấy lần p₁?")


CLIP = dict(id="bay-l12-ch2-04", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Định luật Boyle · thachlab.id.vn",
            cues=bay_cues, scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Ban đầu: nhiệt độ phòng.", 2.8),
   ("Chọn một đáp án.", 6.8)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án A.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Bẫy: áp ngay định luật Boyle.", 3.8),
   ("Khí nhận công nên nóng lên.", 4.8)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
