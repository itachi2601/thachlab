# Clip ON CHUONG (chang D, docs/KE-HOACH-MOTION-GRAPHIC.md, 6/11/2026) - L12 Chuong 3 Tu truong. 1 clip thu cho thay duyet.
# Kieu moi "hoi truoc, hien sau": 5 cau tu khoa (moi cau doc + dung 4 s dem nguoc, A.-D. cung mau) -> hien dap an = CHINH
# dong 🔑 cua bai (content/lesson-samples/l12-*/theory.src.html) -> cuoi: 1 cau noi Bai 12 -> Bai 13 + cau tu nho lai.
# Doc the o 200 tu/phut (cau ngan, HS da hoc) roi dem 4 s; tong 60-90 s.
# Cau hoi lay tu muc Tra bai cua bai, uu tien chu de HS sai nhieu o chang C (tu thong 83 %, luc tu / cam ung tu 60-70 %).
#   Cau 1 Bai 9  Tra bai 4 (duong suc)            Cau 2 Bai 10 Tra bai 3 (F = BIl sin a, song song F = 0)
#   Cau 3 Bai 12 Tra bai 1 (Phi lon nhat khi nao)  Cau 4 Bai 12 Tra bai 2 (dieu kien dong cam ung)
#   Cau 5 Bai 13 Tra bai 3 (50 Hz doi chieu 100 lan/s)
# Khong sua engine; dung qcard/badge cua bay_chung.
from clips.bay_chung import *

READ = 200          # tu/phut: thoi gian doc the cau hoi truoc khi dem nguoc
THINK = 4.0         # giay dung nghi (dem nguoc 4-3-2-1)
QY = 380            # dinh the cau hoi

QS = [
    dict(bai="Bài 9", lines=["Đường sức từ có tính chất nào?"],
         opts=["Cắt nhau ở hai cực", "Khép kín, không cắt", "Mau ở chỗ từ yếu", "Luôn thẳng, song song"], ans=1,
         key="Tiếp tuyến chỉ hướng · Khép kín · Không cắt · Mau thì mạnh", sub=None,
         cap="Mỗi câu: nghĩ 4 giây."),
    dict(bai="Bài 10", lines=["Dây dẫn song song đường sức.", "Lực từ lên dây…"],
         opts=["bằng B·I·l", "bằng nửa B·I·l", "bằng 0", "bằng 2·B·I·l"], ans=2,
         key="F = B·I·l·sinα · Song song thì F = 0", sub="song song: α = 0°, sin α = 0",
         cap="Chủ đề: lực từ lên dây"),
    dict(bai="Bài 12", lines=["Từ thông qua khung lớn nhất", "khi mặt khung…"],
         opts=["vuông góc đường sức", "song song đường sức", "nghiêng 45°", "ở đâu cũng như nhau"], ans=0,
         key="Φ = BS cos α · đơn vị Wb · α là góc của pháp tuyến", sub=None,
         cap="Chủ đề: từ thông"),
    dict(bai="Bài 12", lines=["Khung kín có dòng cảm ứng khi…"],
         opts=["từ thông rất lớn", "đứng yên cạnh nam châm", "khung bằng đồng", "từ thông biến thiên"], ans=3,
         key="Mạch kín · Từ thông biến thiên · Dòng cảm ứng", sub="lớn mà không đổi: không có dòng",
         cap="Chủ đề: dòng cảm ứng"),
    dict(bai="Bài 13", lines=["Dòng xoay chiều 50 Hz đổi chiều", "bao nhiêu lần mỗi giây?"],
         opts=["50 lần", "100 lần", "25 lần", "200 lần"], ans=1,
         key="T = 2π/ω · f = 1/T · Đổi chiều 2f lần/s", sub="2 × 50 = 100",
         cap="Chủ đề: dòng xoay chiều"),
]


def read_s(q):
    s = " ".join(q["lines"] + q["opts"])
    return max(3.5, n_tu(s) * 60 / READ)


def think_win(q):   # [bat dau dem, het dem] tinh tu dau canh
    a = 0.4 + read_s(q)
    return a, a + THINK


def countdown(d, t, a, b):
    if not (a - 0.3 <= t < b + 0.2): return
    k = appear(t, a - 0.3, 0.3) * (1 - clamp((t - b) / 0.2))
    n = max(1, min(4, int(math.ceil(b - t))))
    cx, cy, r = W / 2, 1060, 92
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=A(LIGHT, k), width=12)
    frac_left = clamp((b - t) / (b - a))
    if frac_left > 0:
        d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac_left, fill=A(PURPLE, k), width=12)
    text(d, (cx, cy), str(n), 96, PURPLE, alpha=k)
    text(d, (cx, cy + r + 50), "Nghĩ trước khi xem", 36, MUTED, bold=False, alpha=k)


def key_card(d, t, at, q):
    k = appear(t, at, 0.5)
    if k <= 0: return
    ls = [x.strip() for x in q["key"].split(" · ")]   # moi muc tu khoa mot dong (khong ngat giua cum)
    h = 110 + len(ls) * 58 + (56 if q["sub"] else 0) + 30
    y = 980 + (1 - k) * 30
    card(d, (60, y, 1020, y + h), fill=A((255, 247, 237), k), outline=A(ORANGE, k), w=6)
    lab = f"TỪ KHOÁ · {q['bai'].upper()}"; pw = tw(d, lab, F(34)) + 52
    card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 86), fill=A(ORANGE, k), r=30)
    text(d, (W / 2, y + 56), lab, 34, WHITE, alpha=k)
    yy = y + 126
    for l in ls:
        text(d, (W / 2, yy), l, 46, INK, alpha=k); yy += 58
    if q["sub"]:
        text(d, (W / 2, yy + 8), q["sub"], 38, MUTED, bold=False, alpha=appear(t, at + 0.8, 0.5))


def make_draw(i):
    q = QS[i]

    def draw(img, d, t, sc):
        a, b = think_win(q)
        rev = sc["M"][1]                           # moc phu de "Dap an X."
        kr = appear(t, rev, 0.5)
        k = appear(t, 0.3, 0.45)
        qcard(d, t, sc, QY, q["lines"], q["opts"], 1e9, 1e9, reveal=q["ans"] if t >= rev else None, kr=kr, k=k,
              head=q["bai"])
        if t < rev: countdown(d, t, a, b)
        key_card(d, t, rev + 0.6, q)
    return draw


# ---------------- cuoi: noi Bai 12 -> Bai 13 ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.2, 0.5)
    card(d, (60, 300, 1020, 760), fill=A((236, 253, 243), k), outline=A(GREEN, k), w=6)
    text(d, (W / 2, 360), "Bài 12 → Bài 13", 38, MUTED, bold=False, alpha=k)
    steps = ["Quay khung", "Φ biến thiên", "Dòng xoay chiều"]
    for j, s in enumerate(steps):
        y = 450 + j * 115
        text(d, (W / 2, y), s, 50, GREEN, alpha=appear(t, 0.5 + 0.6 * j, 0.5))
        if j < 2:   # mui ten ngan, cach chu tren/duoi >= 20 px
            ka = appear(t, 0.8 + 0.6 * j, 0.4)
            d.line([(W / 2, y + 45), (W / 2, y + 68)], fill=A(GREEN, ka), width=6)
            chevron(d, W / 2, y + 70, math.pi / 2, A(GREEN, ka), s=16, w=6)
    k1 = appear(t, 2.0, 0.5)
    if k1 <= 0: return
    card(d, (40, 820, 1040, 1440), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 850, W / 2 + pw / 2, 914), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 882), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 1030, "Khung quay 25 vòng/s: dòng đổi chiều mấy lần mỗi giây?", 48, INK, maxw=860,
          alpha=appear(t, 2.3, 0.5))
    kh = appear(t, GOI_Y, 0.5)   # >= 4 s sau cau hoi
    card(d, (110, 1200, 970, 1400), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1250, "Gợi ý", 36, MUTED, bold=False, alpha=kh)
    ctext(d, 1330, "Mỗi vòng đổi chiều 2 lần", 42, ORANGE, maxw=820, alpha=kh)


GOI_Y = 6.3


def _cues(clip):
    out = []
    for sc in clip["scenes"]:
        if sc["key"].startswith("q"):
            q = QS[int(sc["key"][1:]) - 1]; a, b = think_win(q); t0 = sc["t0"]
            out.append((t0 + 0.3, "open"))
            for s in range(4): out.append((t0 + a + s, "tick"))
            out.append((t0 + sc["M"][1], "ding"))
    e = clip["scenes"][-1]; out.append((e["t0"] + 2.3, "open"))
    return out


def q_scene(i):
    q = QS[i]; a, b = think_win(q)
    return dict(key=f"q{i + 1}", title=f"Câu {i + 1}/5", draw=make_draw(i), tail=0.3, caps=[
        (q["cap"], b - 0.4 + 0.15),                     # phu de 1 giu suot luc doc + dem nguoc
        (f"Đáp án {'ABCD'[q['ans']]}.", 4.7)])


CLIP = dict(id="on-l12-ch3", header="VẬT LÍ 12 · ÔN CHƯƠNG", footer="Chương 3 Từ trường · thachlab.id.vn", cues=_cues,
            scenes=[
 *[q_scene(i) for i in range(5)],
 dict(key="end", title="Nối hai bài", draw=s_end, tail=0.3, caps=[
   ("Tự trả lời trước khi xem gợi ý.", GOI_Y + 2.4)]),
])
