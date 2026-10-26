# Video doc 9:16 tom tat Bai 1 Chuong 2 (L12): Thuyet dong hoc phan tu chat khi
import math, os, re, subprocess, sys, wave, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FF = "/Users/MAC/Library/Python/3.9/lib/python/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
W, H, FPS = 1080, 1920, 30
AUD = os.path.join(HERE, "audio"); os.makedirs(AUD, exist_ok=True)
PREVIEW = "--preview" in sys.argv

FR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_fc = {}
def F(size, bold=True):
    size = max(4, int(size)); k = (size, bold)
    if k not in _fc:
        f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size)
        f.set_variation_by_name(b"Bold" if bold else b"Regular"); _fc[k] = f
    return _fc[k]

BG = (255, 248, 238); INK = (30, 41, 82); MUTED = (100, 105, 125); WHITE = (255, 255, 255)
BLUE = (37, 99, 235); ORANGE = (234, 88, 12); GREEN = (22, 163, 74); RED = (220, 38, 38)
PURPLE = (124, 58, 237); YELLOW = (250, 204, 21); TEAL = (13, 148, 136); NAVY = (24, 30, 56)
GRAY = (150, 155, 170)

# ---------------- kich ban: (chu hien tren man hinh, cau doc) ----------------
SCENES = [
 dict(key="hook", title="Hạt khói nhảy múa", lines=[
  ("Hộp kính đậy kín, bên trong là khói hương.", "Một hộp kính đậy kín, bên trong là khói hương."),
  ("Rọi đèn vào: mỗi hạt khói nhảy lung tung, không hạt nào đứng yên.", "Rọi đèn vào, mỗi hạt khói nhảy lung tung, không hạt nào đứng yên."),
  ("Hộp kín, không có gió…", "Hộp kín, không có gió."),
  ("Vậy cái gì đang đẩy chúng?", "Vậy cái gì đang đẩy chúng?"),
 ]),
 dict(key="brown", title="1 · Chuyển động Brown", lines=[
  ("Đó là chuyển động Brown.", "Đó là chuyển động Brao."),
  ("Vô số phân tử khí va vào hạt khói từ mọi phía.", "Vô số phân tử khí vô hình va vào hạt khói từ mọi phía."),
  ("Hai phía không bao giờ va đều nhau → hạt bị đẩy lệch, đi đường gấp khúc.", "Hai phía không bao giờ va đều nhau, nên hạt bị đẩy lệch liên tục, đi theo đường gấp khúc."),
  ("Nhớ hình: quả bóng bị ném từ mọi phía.", "Hãy nhớ hình ảnh: một quả bóng bị ném từ mọi phía."),
 ]),
 dict(key="three", title="2 · Ba nội dung của thuyết", lines=[
  ("Thuyết động học phân tử gói trong 3 chữ: NHỎ – LOẠN – ĐẬP.", "Thuyết động học phân tử chất khí gói gọn trong ba chữ: Nhỏ, Loạn, Đập."),
  ("NHỎ: phân tử nhỏ, ở xa nhau → lực hút, đẩy rất yếu (hệ quả của NHỎ).", "Nhỏ: phân tử rất nhỏ so với khoảng cách giữa chúng. Vì ở xa nhau nên lực hút và lực đẩy rất yếu, lực yếu chính là hệ quả của Nhỏ."),
  ("LOẠN: chuyển động hỗn loạn, không ngừng; nhiệt độ càng cao càng nhanh.", "Loạn: phân tử chuyển động hỗn loạn, không ngừng. Nhiệt độ càng cao, chạy càng nhanh."),
  ("ĐẬP: phân tử đập vào thành bình → gây ra áp suất khí.", "Đập: phân tử đập vào thành bình, gây ra áp suất khí."),
 ]),
 dict(key="balloon", title="Thử với bóng bay", lines=[
  ("Thử với quả bóng bay buộc kín.", "Thử với một quả bóng bay buộc kín."),
  ("Nước nóng: phân tử chạy nhanh, đập mạnh → bóng căng phồng.", "Nhúng vào nước nóng, phân tử chạy nhanh, đập mạnh, bóng căng phồng."),
  ("Nước đá: phân tử chậm lại → bóng xẹp xuống.", "Nhúng vào nước đá, phân tử chậm lại, bóng xẹp xuống."),
 ]),
 dict(key="tube", title="3 · Phân tử nhanh, mùi lan chậm", lines=[
  ("Phân tử N₂ ở 0 °C bay khoảng 455 m/s.", "Phân tử khí ni tơ ở không độ bay khoảng bốn trăm năm mươi lăm mét mỗi giây."),
  ("Ống dài 40 cm: NH₃ một đầu, HCl đầu kia.", "Trong ống dài bốn mươi xen ti mét, đặt a mô ni ắc ở một đầu, a xít clo hy đric ở đầu kia."),
  ("Khoảng 3 phút sau mới có vòng khói trắng NH₄Cl, gần đầu HCl hơn.", "Khoảng ba phút sau mới hiện vòng khói trắng, nằm gần đầu a xít hơn."),
  ("Chạy nhanh từng hạt · va liên tục · cả đám lan chậm hàng trăm nghìn lần.", "Mỗi phân tử chạy rất nhanh, nhưng va chạm liên tục, đi đường gấp khúc, nên cả đám lan chậm hơn hàng trăm nghìn lần."),
  ("Như chen chợ Tết: chân chạy nhanh, người đi chậm.", "Giống như chen chợ Tết vậy."),
 ]),
 dict(key="ideal", title="4 · Mô hình khí lí tưởng", lines=[
  ("Để tính toán, ta dùng mô hình khí lí tưởng.", "Để tính toán, ta dùng mô hình khí lí tưởng."),
  ("Tưởng tượng một bàn bi-a hoàn hảo.", "Hãy tưởng tượng một bàn bi a hoàn hảo."),
  ("① Coi phân tử là chất điểm.", "Một: coi phân tử là chất điểm."),
  ("② Bỏ lực tương tác khi chưa va chạm.", "Hai: bỏ lực tương tác khi chưa va chạm."),
  ("③ Giữa hai va chạm: chuyển động thẳng đều.", "Ba: giữa hai va chạm, chuyển động thẳng đều."),
  ("④ Va chạm hoàn toàn đàn hồi.", "Bốn: va chạm hoàn toàn đàn hồi."),
  ("Khí thực ở điều kiện thường gần giống; nén mạnh, lạnh sâu thì sai rõ.", "Khí thực ở điều kiện thường gần giống khí lí tưởng, nhưng khi nén mạnh hay làm lạnh sâu thì sai rõ."),
 ]),
 dict(key="mol", title="5 · Mol và số Avogadro", lines=[
  ("1 tá = 12 cái.", "Một tá là mười hai cái."),
  ("1 mol = 6,02 × 10²³ phân tử — số Avogadro.", "Một mol là sáu phẩy không hai nhân mười mũ hai mươi ba phân tử, gọi là số A vô ga đrô."),
  ("Số mol: n = N / Nₐ = m / M.", "Số mol n bằng N chia N A, cũng bằng m chia M."),
  ("Ở đktc (0 °C, 1 atm): 1 mol khí bất kì chiếm 22,4 lít.", "Ở điều kiện tiêu chuẩn, một mol khí bất kì chiếm hai mươi hai phẩy bốn lít."),
  ("Cỡ một hộp lập phương cạnh 28 cm.", "Cỡ một hộp lập phương cạnh hai mươi tám xen ti mét."),
 ]),
 dict(key="trap", title="Bẫy hay sập nhất", lines=[
  ("22,4 là LÍT, không phải GAM!", "Cái bẫy hay sập nhất: hai mươi hai phẩy bốn là lít, không phải gam."),
  ("1 mol N₂ và 1 mol CO₂ cùng chiếm 22,4 lít…", "Một mol ni tơ và một mol các bô níc cùng chiếm hai mươi hai phẩy bốn lít."),
  ("…nhưng N₂ nặng 28 g, CO₂ nặng 44 g.", "Nhưng ni tơ nặng hai mươi tám gam, còn các bô níc nặng bốn mươi bốn gam."),
 ]),
 dict(key="quiz", title="Thử ngay!", tail=4.2, lines=[
  ("Túi khí ô tô chứa 84 g N₂ ở đktc (M = 28 g/mol).", "Thử ngay nhé. Túi khí ô tô chứa tám mươi tư gam khí ni tơ, ở điều kiện tiêu chuẩn."),
  ("Túi có bao nhiêu mol? Thể tích bao nhiêu lít?", "Túi có bao nhiêu mol, và thể tích bao nhiêu lít?"),
  ("Tạm dừng video, tính thử!", "Dừng video, tính thử nhé."),
 ]),
 dict(key="answer", title="Đáp án", lines=[
  ("Đáp án đây!", "Đáp án đây."),
  ("n = 84 : 28 = 3 mol.", "Số mol bằng tám mươi tư chia hai mươi tám, bằng ba mol."),
  ("N = 3 × 6,02×10²³ = 1,806×10²⁴ phân tử.", "Số phân tử bằng ba nhân sáu phẩy không hai nhân mười mũ hai mươi ba, bằng một phẩy tám không sáu nhân mười mũ hai mươi tư phân tử."),
  ("V = 3 × 22,4 = 67,2 lít.", "Thể tích bằng ba nhân hai mươi hai phẩy bốn, bằng sáu mươi bảy phẩy hai lít."),
 ]),
 dict(key="recap", title="Nhớ 5 hình = nhớ cả bài", tail=2.5, lines=[
  ("Tóm lại năm hình ảnh:", "Tóm lại, năm hình ảnh."),
  ("Hạt khói nhảy múa → chuyển động Brown.", "Hạt khói nhảy múa."),
  ("NHỎ – LOẠN – ĐẬP → ba nội dung của thuyết.", "Ba chữ nhỏ, loạn, đập."),
  ("Ống khói trắng → phân tử nhanh, mùi lan chậm.", "Ống khói trắng."),
  ("Bàn bi-a hoàn hảo → khí lí tưởng.", "Bàn bi a hoàn hảo."),
  ("Thùng 1 mol → 6,02×10²³ phân tử, 22,4 lít.", "Và thùng một mol. Nhớ năm hình, nhớ cả bài."),
 ]),
]

# ---------------- am thanh ----------------
GAP, TAIL = 0.28, 0.55
SR = 22050
def tts(text, path):
    # file .txt canh moi .wav ghi cau da doc; doi cau thi doc lai (giong thu that cung bi thay -> phai thu lai cau do)
    side = path[:-4] + ".txt"
    if os.path.exists(path) and not os.path.exists(side): open(side, "w", encoding="utf-8").write(text)
    if os.path.exists(path) and open(side, encoding="utf-8").read() != text:
        print("cau doi, doc lai bang giong may:", os.path.basename(path)); os.remove(path)
    if not os.path.exists(path):
        open(side, "w", encoding="utf-8").write(text)
        aiff = path[:-4] + ".aiff"
        subprocess.run(["say", "-v", "Linh", "-r", "185", "-o", aiff, text], check=True)
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", aiff, "-ar", str(SR), "-ac", "1", path], check=True)
        os.remove(aiff)
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)

track = []; tcur = 0.0
for si, sc in enumerate(SCENES):
    sc["t0"] = tcur; marks = []; ends = []; t = 0.35
    track.append(np.zeros(int(0.35 * SR), np.int16))
    for li, (cap, spk) in enumerate(sc["lines"]):
        a = tts(spk, os.path.join(AUD, f"s{si:02d}_{li:02d}.wav"))
        marks.append(t); t += len(a) / SR; ends.append(t)
        track.append(a); track.append(np.zeros(int(GAP * SR), np.int16)); t += GAP
    tail = sc.get("tail", TAIL)
    track.append(np.zeros(int(tail * SR), np.int16)); t += tail
    sc["M"], sc["E"], sc["T"] = marks, ends, t
    tcur += t
TOTAL = tcur
audio = np.concatenate(track)
with wave.open(os.path.join(HERE, "narration.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes())
print(f"tong thoi luong {TOTAL:.1f}s")

# ---------------- tien ich ve ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def appear(t, at, dur=0.45): return ease((t - at) / dur)
def mix(c1, c2, k): return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))
def A(c, a): return (c[0], c[1], c[2], int(255 * clamp(a)))

def refl(p, lo, hi):
    L = hi - lo; m = (p - lo) % (2 * L)
    return lo + (m if m <= L else 2 * L - m)

def tw(d, s, f): return d.textlength(s, font=f)

def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            t = (cur + " " + word).strip()
            if tw(d, t, f) <= maxw or not cur: cur = t
            else: out.append(cur); cur = word
        out.append(cur)
    return out

def text(d, xy, s, size, color=INK, bold=True, anchor="mm", alpha=1.0):
    d.text(xy, s, font=F(size, bold), fill=A(color, alpha), anchor=anchor)

def ctext(d, y, s, size, color=INK, bold=True, maxw=940, alpha=1.0, lh=1.22):
    f = F(size, bold); ls = wrap(d, s, f, maxw)
    y0 = y - (len(ls) - 1) * size * lh / 2
    for i, l in enumerate(ls):
        d.text((W / 2, y0 + i * size * lh), l, font=f, fill=A(color, alpha), anchor="mm")

TOK = re.compile(r"(_\{[^}]*\}|\^\{[^}]*\})")
def rich(d, cx, cy, s, size, color=INK, alpha=1.0):
    parts = [p for p in TOK.split(s) if p]
    segs = []
    for p in parts:
        if p.startswith("_{"): segs.append((p[2:-1], int(size * 0.6), size * 0.28))
        elif p.startswith("^{"): segs.append((p[2:-1], int(size * 0.6), -size * 0.38))
        else: segs.append((p, size, 0))
    tot = sum(tw(d, t, F(sz)) for t, sz, _ in segs)
    x = cx - tot / 2
    for t, sz, dy in segs:
        d.text((x, cy + dy), t, font=F(sz), fill=A(color, alpha), anchor="lm"); x += tw(d, t, F(sz))

def arrow(d, p1, p2, color, w=6, head=22):
    d.line([p1, p2], fill=color, width=w)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for s in (1, -1):
        a = ang + math.pi - s * math.radians(30)
        d.line([p2, (p2[0] + head * math.cos(a), p2[1] + head * math.sin(a))], fill=color, width=w)

def dot(d, x, y, r, c, outline=None):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c, outline=outline, width=3 if outline else 0)

def card(d, box, fill=WHITE, outline=None, r=34, w=4):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=w if outline else 0)

class Gas:
    def __init__(s, n, seed, vmin=80, vmax=220):
        R = random.Random(seed); s.p = []
        for _ in range(n):
            a = R.uniform(0, 2 * math.pi); v = R.uniform(vmin, vmax)
            s.p.append((R.random(), R.random(), v * math.cos(a), v * math.sin(a), R.random()))
    def pos(s, i, tt, box, r=0):
        x0, y0, vx, vy, _ = s.p[i]; X0, Y0, X1, Y1 = box
        return (refl(X0 + r + x0 * (X1 - X0 - 2 * r) + vx * tt, X0 + r, X1 - r),
                refl(Y0 + r + y0 * (Y1 - Y0 - 2 * r) + vy * tt, Y0 + r, Y1 - r))
    def hits_right(s, i, tt, box, r=0, win=0.08):
        x, _ = s.pos(i, tt, box, r); return x > box[2] - r - s.p[i][2].__abs__() * win

class Walk:  # duong gap khuc (chuyen dong Brown)
    def __init__(s, seed, step=0.22, amp=46, n=600, bound=150):
        R = random.Random(seed); s.step = step; x = y = 0.0; s.pts = [(0, 0)]
        for _ in range(n):
            x += R.uniform(-amp, amp); y += R.uniform(-amp, amp)
            x = max(-bound, min(bound, x)); y = max(-bound, min(bound, y)); s.pts.append((x, y))
    def at(s, t):
        k = max(0, t) / s.step; i = int(k); f = k - i
        (x1, y1), (x2, y2) = s.pts[i], s.pts[i + 1]
        return x1 + (x2 - x1) * f, y1 + (y2 - y1) * f

# ---------------- khung chung ----------------
def chrome(d, sc, t, gt):
    # thanh tien trinh
    d.rectangle([0, 0, W, 12], fill=(235, 226, 210))
    d.rectangle([0, 0, int(W * gt / TOTAL), 12], fill=ORANGE)
    card(d, (60, 52, 610, 112), fill=NAVY, r=30)
    text(d, (335, 82), "VẬT LÍ 12 · CHƯƠNG 2 · BÀI 1", 30, WHITE)
    text(d, (1020, 82), "thachlab", 34, ORANGE, anchor="rm")
    k = appear(t, 0.0, 0.5)
    text(d, (W / 2 - (1 - k) * 60, 178), sc["title"], 64, INK, alpha=k)
    # phu de: cau dang doc
    M, E = sc["M"], sc["E"]; cur = None
    for i, m in enumerate(M):
        if t >= m - 0.1: cur = i
    if cur is not None:
        cap = sc["lines"][cur][0]
        f = F(46); ls = wrap(d, cap, f, 900)
        hgt = len(ls) * 58 + 50; y1 = 1790; y0 = y1 - hgt
        a = appear(t, M[cur] - 0.1, 0.25)
        card(d, (60, y0, 1020, y1), fill=A(NAVY, 0.92 * a), r=30)
        for j, l in enumerate(ls):
            d.text((W / 2, y0 + 25 + 29 + j * 58), l, font=f, fill=A(WHITE, a), anchor="mm")
    text(d, (W / 2, 1860), "Thuyết động học phân tử chất khí · thachlab.id.vn", 30, MUTED, bold=False)

def keyword(d, s, t, at, color=ORANGE, y=1400, size=60, sub=None):
    k = back((t - at) / 0.5)
    if t < at: return
    f = F(size); ls = wrap(d, s, f, 900)
    hh = len(ls) * size * 1.2 + 60 + (50 if sub else 0)
    card(d, (60, y - hh / 2, 1020, y + hh / 2), fill=WHITE, outline=color, w=6)
    yy = y - hh / 2 + 30 + size * 0.6
    for l in ls:
        d.text((W / 2, yy), l, font=f, fill=A(color, k), anchor="mm"); yy += size * 1.2
    if sub: text(d, (W / 2, yy + 10), sub, 36, MUTED, alpha=k)

# ---------------- cac canh ----------------
smoke = [Walk(100 + i, step=0.18, amp=26, bound=60) for i in range(14)]
R0 = random.Random(7); smoke_base = [(R0.uniform(260, 820), R0.uniform(620, 880)) for _ in range(14)]

def s_hook(img, d, t, sc):
    M = sc["M"]
    box = (140, 330, 940, 1180)
    d.rounded_rectangle(box, radius=24, fill=(28, 34, 58), outline=(150, 175, 215), width=8)
    d.rectangle([120, 318, 960, 342], fill=(150, 175, 215))  # nap
    text(d, (540, 300), "nắp đậy kín", 30, MUTED, bold=False)
    # den + chum sang
    on = appear(t, M[1] - 0.3, 0.6)
    d.rounded_rectangle([40, 700, 150, 800], radius=16, fill=(90, 90, 100))
    d.polygon([(150, 700), (150, 800), (940, 960), (940, 540)], fill=(255, 230, 120, int(70 * on)))
    for i, (bx, by) in enumerate(smoke_base):
        x, y = smoke[i].at(t + i * 0.7); x += bx; y += by
        dot(d, x, y, 18, (255, 250, 220, int(60 * on)))
        dot(d, x, y, 8, (255, 255, 240, int(255 * max(on, 0.15))))
    if t > M[2]:
        d.line([(980, 420), (1040, 420)], fill=GRAY, width=4)
        for k in range(3):
            yy = 470 + k * 40
            d.line([(985, yy), (1035, yy)], fill=GRAY, width=4)
        d.line([(970, 400), (1050, 560)], fill=RED, width=8)
        text(d, (1010, 600), "gió", 30, RED)
    if t > M[3] - 0.2:
        k = back((t - M[3] + 0.2) / 0.5); s = 1 + 0.06 * math.sin(t * 6)
        text(d, (540, 760), "?", int(260 * k * s), YELLOW)
    keyword(d, "Cái gì đẩy hạt khói?", t, M[3], color=RED)

brown_walk = Walk(5, step=0.3, amp=60, bound=150)
bgas = Gas(70, 11, 250, 420)
def s_brown(img, d, t, sc):
    M = sc["M"]; cx, cy, R = 540, 760, 420
    d.ellipse([cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14], fill=(70, 75, 95))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(236, 244, 255))
    text(d, (cx, cy - R - 40), "phóng to dưới kính hiển vi", 30, MUTED, bold=False)
    show_mol = appear(t, M[1] - 0.2, 0.6)
    box = (cx - R, cy - R, cx + R, cy + R)
    for i in range(len(bgas.p)):
        x, y = bgas.pos(i, t, box, 8)
        if (x - cx) ** 2 + (y - cy) ** 2 < (R - 10) ** 2:
            dot(d, x, y, 8, A(BLUE, show_mol))
    # vet duong gap khuc
    trail = [brown_walk.at(t - k * 0.05) for k in range(0, 80)]
    trail = [(cx + x, cy + y) for x, y in trail]
    if t > M[2] - 0.3:
        d.line(trail, fill=(234, 88, 12, 200), width=5, joint="curve")
    px, py = cx + brown_walk.at(t)[0], cy + brown_walk.at(t)[1]
    dot(d, px, py, 58, (190, 190, 200), outline=(120, 120, 135))
    text(d, (px, py), "hạt khói", 24, INK)
    # mui ten va dap khong can bang
    if t > M[1] + 0.5:
        R2 = random.Random(int(t / 0.3))
        for k in range(5):
            a = R2.uniform(0, 2 * math.pi); L = R2.uniform(30, 90)
            p1 = (px + (60 + L + 26) * math.cos(a), py + (60 + L + 26) * math.sin(a))
            p2 = (px + 66 * math.cos(a), py + 66 * math.sin(a))
            arrow(d, p1, p2, RED, 6, 18)
    if t > M[3] - 0.2:
        keyword(d, "Quả bóng bị ném từ mọi phía", t, M[3] - 0.2, color=ORANGE, size=54,
                sub="va đập không cân bằng → đường gấp khúc")
    elif t > M[2]:
        keyword(d, "Va đập KHÔNG cân bằng", t, M[2], color=RED)

g1, g2, g3 = Gas(7, 21, 40, 70), Gas(16, 22, 150, 260), Gas(14, 23, 160, 260)
def s_three(img, d, t, sc):
    M = sc["M"]
    rows = [("NHỎ", BLUE, "xa nhau"), ("LOẠN", PURPLE, "T↑ nhanh↑"),
            ("ĐẬP", ORANGE, "áp suất")]
    for i, (w, c, sub) in enumerate(rows):
        y0 = 260 + i * 320; k = appear(t, M[i + 1] - 0.15, 0.5)
        if t < M[0] + 0.4 + i * 0.5 and t < M[i + 1] - 0.15:
            continue
        a = max(k, 0.35) if t >= M[0] + 0.4 + i * 0.5 else k
        hl = k > 0.5
        card(d, (60, y0, 1020, y0 + 290), fill=WHITE, outline=c if hl else (225, 220, 210), w=6)
        dot(d, 175, y0 + 120, 92, A(c, a))
        text(d, (175, y0 + 120), w, 46 if len(w) > 3 else 52, WHITE, alpha=1)
        text(d, (175, y0 + 250), sub.split(" · ")[0], 26, c, alpha=a)
        box = (320, y0 + 26, 990, y0 + 264)
        d.rounded_rectangle(box, radius=18, fill=(246, 248, 252), outline=(210, 215, 228), width=3)
        if not hl:
            continue
        lt = t - M[i + 1]
        if i == 0:
            for j in range(7):
                x, y = g1.pos(j, lt, box, 12); dot(d, x, y, 7, BLUE)
            p, q = g1.pos(0, lt, box, 12), g1.pos(1, lt, box, 12)
            d.line([p, q], fill=(37, 99, 235, 120), width=3)
            text(d, ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 - 22), "khoảng cách lớn", 26, BLUE)
        elif i == 1:
            sp = 1 + 0.25 * lt
            tt = lt + 0.125 * lt * lt
            ib = (box[0], box[1], box[2] - 90, box[3])
            for j in range(16):
                x, y = g2.pos(j, tt, ib, 10); dot(d, x, y, 9, PURPLE)
            # nhiet ke
            tx = box[2] - 45
            d.rounded_rectangle([tx - 14, box[1] + 20, tx + 14, box[3] - 40], radius=14, fill=WHITE, outline=GRAY, width=3)
            lvl = clamp(0.25 + 0.15 * lt, 0, 0.95)
            top = box[3] - 40 - lvl * (box[3] - box[1] - 60)
            d.rectangle([tx - 7, top, tx + 7, box[3] - 40], fill=RED)
            dot(d, tx, box[3] - 32, 20, RED)
            text(d, (tx, box[1] + 8), "T↑", 26, RED)
        else:
            wall = box[2] - 30
            d.rectangle([wall, box[1], box[2], box[3]], fill=(120, 125, 140))
            ib = (box[0], box[1], wall, box[3])
            for j in range(14):
                x, y = g3.pos(j, lt, ib, 9); dot(d, x, y, 9, ORANGE)
                if x > wall - 22:
                    dot(d, wall, y, 22, (250, 204, 21, 200))
            arrow(d, (wall - 70, box[1] + 40), (wall - 4, box[1] + 40), RED, 6, 18)
            text(d, (wall - 110, box[1] + 40), "p", 36, RED)
    keyword(d, "NHỎ – LOẠN – ĐẬP", t, M[0] + 0.2, color=INK, y=1330 + 70, size=78)

bh, bc = Gas(22, 31, 220, 330), Gas(22, 32, 40, 80)
def s_balloon(img, d, t, sc):
    M = sc["M"]
    for side in (0, 1):
        x0 = 80 if side == 0 else 560; x1 = x0 + 440
        water = (230, 90, 70) if side == 0 else (90, 160, 230)
        lab = "nước nóng 60 °C" if side == 0 else "nước đá 0 °C"
        go = appear(t, M[1 + side] - 0.2, 1.4)
        r = 150 + (45 * go if side == 0 else -38 * go)
        cx, cy = (x0 + x1) / 2, 820 - (r - 150) * 0.6
        # chau nuoc
        d.polygon([(x0, 880), (x1, 880), (x1 - 30, 1200), (x0 + 30, 1200)], fill=(*water, 120), outline=GRAY)
        d.rectangle([x0, 865, x1, 885], fill=(200, 200, 210))
        if side == 0:
            for k in range(3):
                sx = x0 + 100 + k * 120; ph = t * 2 + k
                pts = [(sx + 14 * math.sin(ph + j * 0.6), 860 - j * 14) for j in range(10)]
                if go > 0.05: d.line(pts, fill=(200, 200, 210, int(200 * go)), width=5)
        else:
            for k in range(3):
                ix = x0 + 90 + k * 110; iy = 960 + (k % 2) * 60
                d.rounded_rectangle([ix, iy, ix + 70, iy + 60], radius=10, fill=(235, 248, 255), outline=(160, 200, 230), width=3)
        # bong
        col = RED if side == 0 else BLUE
        d.line([(cx, cy + r), (cx, cy + r + 50)], fill=GRAY, width=4)
        dot(d, cx, cy, r, A(mix(col, WHITE, 0.55), 1), outline=col)
        g = bh if (side == 0 and go > 0.1) else bc
        if side == 1 and go < 0.1: g = Gas(22, 33, 120, 180)
        bx = (cx - r * 0.68, cy - r * 0.68, cx + r * 0.68, cy + r * 0.68)
        for j in range(22):
            x, y = g.pos(j, t, bx, 6); dot(d, x, y, 6, col)
        text(d, ((x0 + x1) / 2, 1250), lab, 36, col)
        if go > 0.6:
            text(d, ((x0 + x1) / 2, 1310), "CĂNG" if side == 0 else "XẸP", 54, col)
    keyword(d, "Nóng → đập mạnh → căng", t, M[1] + 0.8, color=RED, y=1440, size=52)

crowd = Gas(60, 41, 0, 1)
zig = Walk(42, step=0.12, amp=40, bound=80)
def s_tube(img, d, t, sc):
    M = sc["M"]
    # toc do 1 phan tu
    k0 = appear(t, M[0], 0.6)
    card(d, (60, 260, 1020, 420), fill=WHITE, outline=BLUE, w=4)
    mx = 120 + ((t - M[0]) * 900) % 820 if t > M[0] else 120
    dot(d, mx, 330, 14, BLUE)
    for k in range(1, 6):
        d.line([(mx - 20 - k * 28, 330), (mx - 34 - k * 28, 330)], fill=(37, 99, 235, 200 - k * 35), width=6)
    text(d, (540, 392), "1 phân tử N₂: ~455 m/s", 40, BLUE, alpha=k0)
    # ong khuech tan
    X0, X1, Y = 100, 980, 600
    k1 = appear(t, M[1] - 0.2, 0.5)
    d.rounded_rectangle([X0, Y - 40, X1, Y + 40], radius=40, fill=(240, 248, 255), outline=(150, 175, 215), width=5)
    dot(d, X0 + 30, Y, 34, A(BLUE, k1)); dot(d, X1 - 30, Y, 34, A(ORANGE, k1))
    text(d, (X0 + 30, Y - 80), "NH₃", 40, BLUE, alpha=k1)
    text(d, (X1 - 30, Y - 80), "HCl", 40, ORANGE, alpha=k1)
    p = ease((t - M[1] - 0.5) / (M[2] + 1.2 - M[1] - 0.5))
    meet = X0 + (X1 - X0) * 0.6
    if p > 0:
        for j in range(30):
            a = j / 30
            xa = X0 + 60 + (meet - X0 - 60) * p * a
            xb = X1 - 60 - (X1 - 60 - meet) * p * a
            d.ellipse([xa - 18, Y - 18, xa + 18, Y + 18], fill=(37, 99, 235, int(90 * (1 - a))))
            d.ellipse([xb - 18, Y - 18, xb + 18, Y + 18], fill=(234, 88, 12, int(90 * (1 - a))))
    clock = int(180 * p)
    if t > M[1]:
        text(d, (540, 690), f"t = {clock} s", 44, INK)
    if p >= 1:
        kk = back((t - (M[2] + 1.2)) / 0.4)
        d.ellipse([meet - 22 * kk, Y - 46, meet + 22 * kk, Y + 46], fill=WHITE, outline=(170, 170, 180), width=3)
        text(d, (meet, Y - 84), "NH₄Cl", 34, INK)
        d.line([(X0, 760), (meet, 760)], fill=BLUE, width=4); d.line([(meet, 760), (X1, 760)], fill=ORANGE, width=4)
        for xx in (X0, meet, X1): d.line([(xx, 745), (xx, 775)], fill=INK, width=4)
        text(d, ((X0 + meet) / 2, 795), "24 cm", 32, BLUE); text(d, ((meet + X1) / 2, 795), "16 cm", 32, ORANGE)
    # duong gap khuc giua dam dong
    if t > M[3] - 0.2:
        ka = appear(t, M[3] - 0.2)
        bx = (80, 850, 1000, 1180)
        card(d, bx, fill=WHITE, outline=PURPLE, w=4)
        for j in range(60):
            x, y = crowd.pos(j, 0, bx, 14); dot(d, x, y, 9, A(GRAY, ka))
        lt = t - M[3]
        pts = [zig.at(lt - k * 0.03) for k in range(100)]
        drift = lambda s: 140 + 22 * max(0, s)
        pts = [(drift(lt - k * 0.03) + x, 1015 + y) for k, (x, y) in enumerate(pts)]
        d.line(pts, fill=(124, 58, 237, 220), width=5)
        dot(d, pts[0][0], pts[0][1], 14, PURPLE)
        text(d, (540, 1215), "chạy nhanh · va liên tục · tiến rất chậm", 34, PURPLE, alpha=ka)
    if t > M[4] - 0.2:
        keyword(d, "Như chen chợ Tết", t, M[4] - 0.2, color=PURPLE, y=1400, size=56, sub="cả đám lan ~0,13 cm/s")
    elif t > M[3] + 1:
        keyword(d, "Bẫy: nhanh từng hạt ≠ lan cả đám", t, M[3] + 1, color=RED, y=1400, size=50)

pool = Gas(10, 51, 180, 320)
def s_ideal(img, d, t, sc):
    M = sc["M"]
    k = appear(t, M[1] - 0.3, 0.6)
    tb = (100, 270, 980, 760)
    d.rounded_rectangle([tb[0] - 30, tb[1] - 30, tb[2] + 30, tb[3] + 30], radius=40, fill=(120, 72, 40))
    d.rectangle(tb, fill=(24, 128, 72))
    cols = [YELLOW, RED, BLUE, WHITE, ORANGE, PURPLE, (20, 20, 20), TEAL, (255, 140, 180), (180, 255, 120)]
    for j in range(10):
        x, y = pool.pos(j, t, tb, 10)
        # vet thang
        vx, vy = pool.p[j][2], pool.p[j][3]
        if t > M[4] - 0.2 and t < M[5] + 0.5:
            d.line([(x, y), (x - vx * 0.18 * np.sign(1), y)], fill=None) if False else None
        dot(d, x, y, 10, cols[j])
        if x < tb[0] + 14 or x > tb[2] - 14 or y < tb[1] + 14 or y > tb[3] - 14:
            if t > M[5] - 0.2: dot(d, x, y, 26, (250, 204, 21, 160))
    text(d, (540, 820), "bàn bi-a hoàn hảo: không ma sát, bi = chấm", 32, MUTED, bold=False)
    rules = [("Chất điểm", "bỏ kích thước"), ("Không lực tương tác", "khi chưa va chạm"),
             ("Thẳng đều", "giữa hai va chạm"), ("Va chạm đàn hồi", "bật lại, không mất năng lượng")]
    for i, (a, b) in enumerate(rules):
        if t < M[2 + i] - 0.15: continue
        kk = back((t - M[2 + i] + 0.15) / 0.45); y = 900 + i * 95
        x0 = 60 + (1 - kk) * 200
        card(d, (x0, y, 1020, y + 80), fill=WHITE, outline=GREEN, r=24, w=4)
        dot(d, x0 + 46, y + 40, 26, GREEN); text(d, (x0 + 46, y + 40), str(i + 1), 34, WHITE)
        text(d, (x0 + 92, y + 40), a, 40, INK, anchor="lm")
        text(d, (1000, y + 40), b, 28, MUTED, bold=False, anchor="rm")
    if t > M[6] - 0.2:
        keyword(d, "Nén mạnh · lạnh sâu → khí thực lệch", t, M[6] - 0.2, color=RED, y=1420, size=46)
    elif t > M[3] + 0.6:
        keyword(d, "Bẫy: bỏ qua ≠ bằng không", t, M[3] + 0.6, color=RED, y=1420, size=50)

def cube(d, cx, cy, s, col, label, alpha=1.0):
    o = s * 0.35
    f = [(cx - s / 2, cy - s / 2 + o / 2), (cx + s / 2 - o, cy - s / 2 + o / 2), (cx + s / 2 - o, cy + s / 2), (cx - s / 2, cy + s / 2)]
    top = [f[0], (f[0][0] + o, f[0][1] - o), (f[1][0] + o, f[1][1] - o), f[1]]
    side = [f[1], top[2], (f[2][0] + o, f[2][1] - o), f[2]]
    d.polygon(top, fill=A(mix(col, WHITE, 0.45), alpha), outline=INK)
    d.polygon(side, fill=A(mix(col, (0, 0, 0), 0.15), alpha), outline=INK)
    d.polygon(f, fill=A(col, alpha), outline=INK)
    text(d, ((f[0][0] + f[1][0]) / 2, (f[0][1] + f[3][1]) / 2), label, int(s * 0.17), WHITE, alpha=alpha)

def s_mol(img, d, t, sc):
    M = sc["M"]
    # 1 ta trung
    k = appear(t, M[0] - 0.2)
    card(d, (60, 250, 520, 520), fill=WHITE, outline=(225, 220, 210), w=4)
    text(d, (290, 290), "1 tá", 40, INK, alpha=k)
    for j in range(12):
        if t < M[0] + j * 0.08: continue
        x = 115 + (j % 6) * 70; y = 370 + (j // 6) * 80
        d.ellipse([x - 26, y - 33, x + 26, y + 33], fill=(255, 236, 200), outline=(200, 160, 100), width=3)
    text(d, (290, 495), "= 12 quả", 34, MUTED, alpha=k)
    # thung 1 mol
    k2 = appear(t, M[1] - 0.2)
    card(d, (560, 250, 1020, 520), fill=NAVY, r=30)
    R = random.Random(3)
    n = int(clamp((t - M[1]) / 1.5) * 900)
    for j in range(n):
        x = R.uniform(585, 995); y = R.uniform(320, 500)
        d.point((x, y), fill=(120, 200, 255)); d.point((x + 1, y), fill=(120, 200, 255))
    text(d, (790, 290), "1 mol", 40, YELLOW, alpha=k2)
    if t > M[1]:
        rich(d, 540, 590, "N_{A} = 6,02 × 10^{23} phân tử/mol", 52, ORANGE, alpha=appear(t, M[1] + 0.6))
    # cong thuc
    if t > M[2] - 0.2:
        k3 = back((t - M[2] + 0.2) / 0.5)
        card(d, (60, 660, 1020, 900), fill=WHITE, outline=BLUE, w=6)
        rich(d, 540, 750, "n = N / N_{A} = m / M", int(78 * k3) or 1, BLUE)
        text(d, (540, 845), "n: số mol · N: số phân tử · m: khối lượng (g) · M: g/mol", 28, MUTED, bold=False)
    # hop 22,4 L
    if t > M[3] - 0.2:
        k4 = appear(t, M[3] - 0.2, 0.6)
        cube(d, 360, 1110, 250 * (0.6 + 0.4 * k4), TEAL, "22,4 L", alpha=k4)
        text(d, (760, 1040), "1 mol khí bất kì", 40, INK, alpha=k4)
        text(d, (760, 1100), "đktc: 0 °C · 1 atm", 36, TEAL, alpha=k4)
        if t > M[4] - 0.2:
            text(d, (760, 1170), "cạnh ≈ 28 cm", 44, ORANGE, alpha=appear(t, M[4] - 0.2))
    keyword(d, "Mol là cái thùng đếm phân tử", t, M[1] + 2.2, color=TEAL, y=1400, size=50)

def s_trap(img, d, t, sc):
    M = sc["M"]
    ang = math.radians(9) * ease((t - M[2] + 0.1) / 0.9)
    px, py, L = 540, 520, 380
    d.polygon([(px, py), (px - 70, 1000), (px + 70, 1000)], fill=(160, 140, 110))
    d.rectangle([px - 160, 1000, px + 160, 1030], fill=(120, 100, 80))
    lx, ly = px - L * math.cos(ang), py - L * math.sin(ang)
    rx, ry = px + L * math.cos(ang), py + L * math.sin(ang)
    d.line([(lx, ly), (rx, ry)], fill=(90, 70, 50), width=14)
    dot(d, px, py, 18, (90, 70, 50))
    k = appear(t, M[1] - 0.2)
    for (x, y, col, nm, mass, show) in ((lx, ly, BLUE, "N₂", "28 g", True), (rx, ry, (110, 115, 130), "CO₂", "44 g", True)):
        d.line([(x, y), (x - 90, y + 170)], fill=GRAY, width=3); d.line([(x, y), (x + 90, y + 170)], fill=GRAY, width=3)
        d.rounded_rectangle([x - 130, y + 170, x + 130, y + 190], radius=8, fill=(90, 70, 50))
        cube(d, x - 10, y + 85 + 10, 170, col, "22,4 L", alpha=k)
        text(d, (x, y - 50), nm, 48, col, alpha=k)
        if t > M[2] - 0.2:
            text(d, (x, y + 240), mass, 60, col, alpha=appear(t, M[2] - 0.2))
    if t > M[2] + 1:
        text(d, (540, 1120), "cùng thể tích ≠ cùng khối lượng", 44, INK)
    keyword(d, "22,4 là LÍT, không phải GAM!", t, M[0] - 0.1, color=RED, y=1360, size=58)

def car(d, x, y, s, airbag):
    d.rounded_rectangle([x, y + 60 * s, x + 520 * s, y + 200 * s], radius=int(40 * s), fill=BLUE)
    d.polygon([(x + 110 * s, y + 60 * s), (x + 180 * s, y - 20 * s), (x + 380 * s, y - 20 * s), (x + 450 * s, y + 60 * s)], fill=BLUE)
    d.polygon([(x + 200 * s, y + 55 * s), (x + 215 * s, y), (x + 300 * s, y), (x + 300 * s, y + 55 * s)], fill=(200, 230, 255))
    for wx in (x + 120 * s, x + 400 * s):
        dot(d, wx, y + 200 * s, 50 * s, (40, 40, 50)); dot(d, wx, y + 200 * s, 22 * s, GRAY)
    if airbag > 0:
        dot(d, x + 260 * s, y + 40 * s, 90 * s * airbag, (255, 255, 255, 235), outline=ORANGE)
        text(d, (x + 260 * s, y + 40 * s), "84 g N₂", int(34 * s * max(airbag, 0.3)), ORANGE)

def s_quiz(img, d, t, sc):
    M, E = sc["M"], sc["E"]
    car(d, 160, 400, 1.45, back((t - 0.8) / 0.7))
    k = appear(t, M[1] - 0.2)
    card(d, (60, 780, 1020, 1060), fill=WHITE, outline=ORANGE, w=5)
    text(d, (540, 840), "đktc · M(N₂) = 28 g/mol", 38, MUTED, alpha=k)
    text(d, (540, 920), "a)  n = ? mol", 52, INK, alpha=k)
    text(d, (540, 1000), "b)  V = ? lít", 52, INK, alpha=k)
    end = E[-1]
    if t > end:
        rem = sc["T"] - t; n = max(1, math.ceil(rem - 0.2))
        frac = (rem - 0.2) % 1
        cx, cy = 540, 1260
        dot(d, cx, cy, 110, WHITE, outline=(225, 220, 210))
        d.arc([cx - 110, cy - 110, cx + 110, cy + 110], -90, -90 + 360 * frac, fill=ORANGE, width=16)
        text(d, (cx, cy), str(min(n, 4)), 120, ORANGE)
        text(d, (cx, cy + 160), "tạm dừng và tính", 40, MUTED)

def s_answer(img, d, t, sc):
    M = sc["M"]
    car(d, 330, 320, 0.85, 1)
    rows = [(1, "n = 84 : 28 = 3 mol", BLUE), (2, "N = 3 × 6,02×10^{23} = 1,806×10^{24}", PURPLE), (3, "V = 3 × 22,4 = 67,2 L", TEAL)]
    for r, (mi, s_, col) in enumerate(rows):
        if t < M[mi] - 0.2: continue
        k = back((t - M[mi] + 0.2) / 0.5); y0 = 600 + r * 150
        card(d, (60, y0, 1020, y0 + 130), fill=WHITE, outline=col, w=5)
        rich(d, 540, y0 + 65, s_, max(4, int(54 * k)), col)
    if t > M[3] - 0.2:
        for j in range(3):
            kj = appear(t, M[3] + 0.2 + j * 0.35)
            cube(d, 270 + j * 270, 1150, 150 * max(kj, 0.01), TEAL, "22,4 L", alpha=kj)
    keyword(d, "Chia M → mol · nhân Nₐ → phân tử\nnhân 22,4 → lít", t, M[3] + 2.2, color=ORANGE, y=1400, size=46)

def mini(d, i, x, y, t):
    if i == 0:
        d.rounded_rectangle([x - 60, y - 50, x + 60, y + 50], radius=12, fill=(28, 34, 58))
        for j in range(4):
            px, py = smoke[j].at(t + j); dot(d, x + px * 0.6, y + py * 0.6, 6, (255, 250, 220))
    elif i == 1:
        for j, (c, w) in enumerate(((BLUE, "N"), (PURPLE, "L"), (ORANGE, "Đ"))):
            dot(d, x - 44 + j * 44, y, 22, c); text(d, (x - 44 + j * 44, y), w, 26, WHITE)
    elif i == 2:
        d.rounded_rectangle([x - 62, y - 16, x + 62, y + 16], radius=16, fill=(240, 248, 255), outline=(150, 175, 215), width=3)
        dot(d, x - 52, y, 12, BLUE); dot(d, x + 52, y, 12, ORANGE); dot(d, x + 12, y, 10, WHITE, outline=GRAY)
    elif i == 3:
        d.rectangle([x - 60, y - 40, x + 60, y + 40], fill=(24, 128, 72), outline=(120, 72, 40), width=6)
        for j in range(4):
            px, py = pool.pos(j, t, (x - 52, y - 32, x + 52, y + 32), 5); dot(d, px, py, 5, YELLOW)
    else:
        cube(d, x, y + 6, 100, TEAL, "1 mol")

def s_recap(img, d, t, sc):
    M = sc["M"]
    items = [("Hạt khói nhảy múa", "chuyển động Brown", ORANGE), ("NHỎ – LOẠN – ĐẬP", "3 nội dung của thuyết", PURPLE),
             ("Ống khói trắng", "phân tử nhanh, mùi lan chậm", BLUE), ("Bàn bi-a hoàn hảo", "4 giả thiết khí lí tưởng", GREEN),
             ("Thùng 1 mol", "6,02×10²³ phân tử · 22,4 L", TEAL)]
    for i, (a, b, c) in enumerate(items):
        if t < M[i + 1] - 0.2: continue
        k = back((t - M[i + 1] + 0.2) / 0.45); y = 270 + i * 215
        x0 = 60 + (1 - k) * 300
        card(d, (x0, y, 1020, y + 190), fill=WHITE, outline=c, w=5)
        mini(d, i, x0 + 110, y + 95, t)
        text(d, (x0 + 210, y + 70), a, 46, c, anchor="lm")
        text(d, (x0 + 210, y + 130), b, 32, MUTED, bold=False, anchor="lm")
    if t > sc["E"][-1]:
        k = appear(t, sc["E"][-1], 0.5)
        card(d, (160, 1370, 920, 1490), fill=A(ORANGE, k), r=60)
        text(d, (540, 1430), "Lưu lại · xem trước giờ kiểm tra", 40, WHITE, alpha=k)

DRAW = dict(hook=s_hook, brown=s_brown, three=s_three, balloon=s_balloon, tube=s_tube, ideal=s_ideal,
            mol=s_mol, trap=s_trap, quiz=s_quiz, answer=s_answer, recap=s_recap)

def frame(gt):
    for sc in SCENES:
        if gt < sc["t0"] + sc["T"]: break
    t = gt - sc["t0"]
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img, "RGBA")
    DRAW[sc["key"]](img, d, t, sc)
    chrome(d, sc, t, gt)
    if t < 0.25:  # chuyen canh mo dan
        img = Image.blend(Image.new("RGB", (W, H), BG), img, ease(t / 0.25))
    return img

if "--kiem" in sys.argv:  # moi cau phu de <= 2 dong
    _d = ImageDraw.Draw(Image.new("RGB", (W, H))); bad = 0; n = 0
    for si, sc in enumerate(SCENES):
        for li, (cap, _) in enumerate(sc["lines"]):
            n += 1; k = len(wrap(_d, cap, F(46), 900))
            if k > 2: bad += 1; print(f"  cau {n} (canh {si + 1}): {k} dong -> {cap}")
    print(f"{n} cau, {bad} cau qua 2 dong"); sys.exit(1 if bad else 0)

if PREVIEW:
    os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
    for sc in SCENES:
        for fr in (0.55, 0.97):
            gt = sc["t0"] + sc["T"] * fr
            frame(gt).resize((540, 960)).save(os.path.join(HERE, "preview", f"{sc['key']}_{int(fr*100)}.png"))
    sys.exit()

out = os.path.join(HERE, "tom-tat-thuyet-dong-hoc-phan-tu.mp4")
p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-i", os.path.join(HERE, "narration.wav"), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out],
                     stdin=subprocess.PIPE)
N = int(TOTAL * FPS)
for i in range(N):
    p.stdin.write(frame(i / FPS).tobytes())
    if i % 300 == 0: print(f"{i}/{N}", flush=True)
p.stdin.close(); p.wait()
print("xong", out)
