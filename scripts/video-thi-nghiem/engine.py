# Bo dung video thi nghiem doc 9:16 (khong loi: phu de + tieng bao o moc chinh, clip cu: nhac nen tong hop). Khung lay tu
# content/lesson-samples/l12-thuyet-dong-hoc-phan-tu/video/make_video.py.
#   python3 scripts/video-thi-nghiem/render.py boyle --preview   -> anh 540x960 o ra/<id>/preview
#   python3 scripts/video-thi-nghiem/render.py boyle             -> ra/<id>.mp4
import math, os, re, subprocess, sys, wave, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ra"); os.makedirs(OUT, exist_ok=True)
FF = "/Users/MAC/Library/Python/3.9/lib/python/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
W, H, FPS, SR = 1080, 1920, 30, 22050

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
GRAY = (150, 155, 170); LIGHT = (232, 226, 214)
# Vung an toan (V12, 28/10/2026): khi dung video, thanh dieu khien trinh duyet che ~10% tren va ~10% duoi khung.
# Canh van ve tren khung 1080x1920 nhu cu; frame() thu vung y SRC0..SRC1 vao tu DST0 (ti le SCALE), tieu de canh
# o TITLE_Y, phu de mot dong ket thuc o CAP_Y1 -- ca hai nam ngoai vung bi che.
SRC0, SRC1, DST0, SCALE = 200, 1690, 285, 0.88
TITLE_Y, CAP_Y1 = 232, 1705
WPM = 140   # toc do doc chu Viet tren dien thoai (docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def appear(t, at, dur=0.45): return ease((t - at) / dur)
def lerp(a, b, k): return a + (b - a) * k
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

# Pillow 11 bo qua kenh alpha khi ve chu len anh RGB -> chu khong mo dan duoc. Khi alpha < 1 ve chu
# len mat na L roi dan mau qua mat na. IMG_REF[0] = anh dang ve (frame() gan san; canh tu gan lai cung duoc).
IMG_REF = [None]
def dtext(d, xy, s, f, color, alpha=1.0, anchor="mm"):
    if alpha <= 0.02: return
    col = tuple(color[:3])
    if alpha >= 0.98 or IMG_REF[0] is None:
        d.text(xy, s, font=f, fill=col, anchor=anchor); return
    l, t, r, b = d.textbbox(xy, s, font=f, anchor=anchor); l, t, r, b = int(l) - 3, int(t) - 3, int(r) + 3, int(b) + 3
    m = Image.new("L", (r - l, b - t), 0)
    ImageDraw.Draw(m).text((xy[0] - l, xy[1] - t), s, font=f, fill=int(255 * alpha), anchor=anchor)
    IMG_REF[0].paste(col, (l, t, r, b), m)

def text(d, xy, s, size, color=INK, bold=True, anchor="mm", alpha=1.0):
    dtext(d, xy, s, F(size, bold), color, alpha, anchor)

def ctext(d, y, s, size, color=INK, bold=True, maxw=940, alpha=1.0, lh=1.22):
    f = F(size, bold); ls = wrap(d, s, f, maxw)
    y0 = y - (len(ls) - 1) * size * lh / 2
    for i, l in enumerate(ls):
        dtext(d, (W / 2, y0 + i * size * lh), l, f, color, alpha)

TOK = re.compile(r"(_\{[^}]*\}|\^\{[^}]*\})")
def rich(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    segs = []
    for p in [p for p in TOK.split(s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], int(size * 0.6), size * 0.28))
        elif p.startswith("^{"): segs.append((p[2:-1], int(size * 0.6), -size * 0.38))
        else: segs.append((p, size, 0))
    tot = sum(tw(d, t, F(sz)) for t, sz, _ in segs)
    x = cx - tot / 2 if anchor == "m" else cx
    for t, sz, dy in segs:
        dtext(d, (x, cy + dy), t, F(sz), color, alpha, "lm"); x += tw(d, t, F(sz))

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

def keyword(d, s, t, at, color=ORANGE, y=1400, size=54, sub=None):
    if t < at: return
    k = back((t - at) / 0.5); f = F(size); ls = wrap(d, s, f, 880)
    hh = len(ls) * size * 1.2 + 60 + (50 if sub else 0)
    card(d, (60, y - hh / 2, 1020, y + hh / 2), fill=WHITE, outline=color, w=6)
    yy = y - hh / 2 + 30 + size * 0.6
    for l in ls:
        d.text((W / 2, yy), l, font=f, fill=A(color, k), anchor="mm"); yy += size * 1.2
    if sub: text(d, (W / 2, yy + 10), sub, 34, MUTED, alpha=k)

# Canh chot dung chung: mot cau chot (xanh) + cau hoi tu nho lai (cam) + goi y. body(d, t, k) ve them
# trong vung y 1000-1260 neu can (vd. thanh so sanh). Phu de canh nay: 1 cau, hien o M[0].
def chot_hoi(d, t, sc, chot, hoi, goi_y=None, body=None):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, chot, 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 860 if body is None else 820, hoi, 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    if body: body(d, t, k1)
    if goi_y:
        kh = appear(t, M[0] + 1.2, 0.5)
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 36, MUTED, bold=False, alpha=kh)
        ctext(d, 1445, goi_y, 42, ORANGE, maxw=820, alpha=kh)

# ---------------- nhip phu de ----------------
def n_tu(s): return len(re.findall(r"[A-Za-zÀ-ỹđĐ]{2,}|\d+(?:[,.]\d+)?", s))
def cap_dur(s): return max(2.5, n_tu(s) * 60 / WPM + 0.8)   # du thoi gian doc o WPM + 0,8 s nhin hinh
def build(clip):
    t0 = 0.0
    for sc in clip["scenes"]:
        sc["t0"] = t0; t = 0.4; sc["M"] = []
        durs = [max(c[1], cap_dur(c[0])) if isinstance(c, tuple) else cap_dur(c) for c in sc["caps"]]  # khong ngan hon muc doc
        sc["caps"] = [c[0] if isinstance(c, tuple) else c for c in sc["caps"]]
        for dd in durs:
            sc["M"].append(t); t += dd
        sc["T"] = t + sc.get("tail", 0.9); t0 += sc["T"]
    clip["TOTAL"] = t0
def cur_cap(sc, t):  # chi so phu de dang hien (-1 neu chua co)
    c = -1
    for i, m in enumerate(sc["M"]):
        if t >= m - 0.05: c = i
    return c

def chrome(d, clip, sc, t, gt):
    d.rectangle([0, 0, W, 12], fill=(235, 226, 210))
    d.rectangle([0, 0, int(W * gt / clip["TOTAL"]), 12], fill=ORANGE)
    card(d, (60, 52, 640, 112), fill=NAVY, r=30)
    text(d, (350, 82), clip["header"], 28, WHITE)
    text(d, (1020, 82), "thachlab", 34, ORANGE, anchor="rm")
    k = appear(t, 0.0, 0.5)
    text(d, (W / 2 - (1 - k) * 60, TITLE_Y), sc["title"], 56, INK, alpha=k)
    cur = cur_cap(sc, t)
    if cur >= 0:
        f = F(46); ls = wrap(d, sc["caps"][cur], f, 900)
        hgt = len(ls) * 58 + 50; y1 = CAP_Y1; y0 = y1 - hgt
        a = appear(t, sc["M"][cur] - 0.05, 0.25)
        card(d, (60, y0, 1020, y1), fill=A(NAVY, 0.92 * a), r=30)
        for j, l in enumerate(ls):
            dtext(d, (W / 2, y0 + 25 + 29 + j * 58), l, f, WHITE, a)
    text(d, (W / 2, 1860), clip["footer"], 30, MUTED, bold=False)

# ---------------- nhac nen tong hop (khong ban quyen) ----------------
def music(total, seed=7):
    n = int((total + 1.5) * SR); tt = np.arange(n) / SR
    chords = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]
    seg = 4.0; pad = np.zeros(n)
    for i in range(int(total / seg) + 2):
        a, b = int(i * seg * SR), min(n, int((i + 1) * seg * SR + 1.0 * SR))
        if a >= n: break
        x = tt[a:b] - i * seg
        env = np.minimum(1, x / 1.0) * np.minimum(1, (seg + 1.0 - x) / 1.0)
        for f in chords[i % 4]:
            for det, amp in ((0.0, 1.0), (0.4, 0.6)):
                pad[a:b] += env * amp * np.sin(2 * np.pi * (f + det) * x) * (1 + 0.15 * np.sin(2 * np.pi * 0.3 * x))
            pad[a:b] += env * 0.25 * np.sin(2 * np.pi * 2 * f * x)
    R = random.Random(seed); penta = [523.25, 587.33, 659.25, 783.99, 880.0]; pl = np.zeros(n); t = 1.0
    while t < total:
        f = R.choice(penta); a = int(t * SR); L = int(1.6 * SR); b = min(n, a + L)
        x = np.arange(b - a) / SR
        pl[a:b] += 0.5 * np.sin(2 * np.pi * f * x) * np.exp(-3.2 * x) * np.minimum(1, x / 0.01)
        t += R.choice([0.5, 0.5, 1.0, 1.0, 1.5])
    m = pad / (np.abs(pad).max() + 1e-9) * 0.7 + pl / (np.abs(pl).max() + 1e-9) * 0.3
    m *= np.minimum(1, tt / 1.2) * np.minimum(1, np.maximum(0, (total - tt)) / 1.8 + 0.0)
    m = m / (np.abs(m).max() + 1e-9) * 0.35
    return (m[: int(total * SR)] * 32767).astype(np.int16)

# ---------------- tieng bao o moc chinh (thay nhac lien mach, 27/10/2026) ----------------
# Moreno & Mayer 2000: nhac nen lam giam nho + van dung -> clip co clip["cues"](clip) -> [(giay, loai)] thi
# chi phat tieng ngan dung moc su kien, con lai im lang. Clip cu khong co "cues" van dung music().
def _tone(x, f, decay, amp):
    return amp * np.sin(2 * np.pi * f * x) * np.exp(-decay * x) * np.minimum(1, x / 0.005)

def sfx(total, cues):
    n = int(total * SR); out = np.zeros(n)
    def put(at, sig):
        a = int(at * SR); b = min(n, a + len(sig))
        if 0 <= a < n: out[a:b] += sig[: b - a]
    for at, kind in cues:
        if kind == "tick":    # tich tac nhe khi tua nhanh
            x = np.arange(int(0.05 * SR)) / SR; put(at, _tone(x, 1900, 90, 0.10))
        elif kind == "tap":   # cham diem moc (bat dau doan nam ngang)
            x = np.arange(int(0.4 * SR)) / SR; put(at, _tone(x, 880, 16, 0.45) + _tone(x, 1320, 22, 0.2))
        elif kind == "open":  # hien cau hoi
            x = np.arange(int(0.9 * SR)) / SR; put(at, _tone(x, 523.25, 4, 0.3)); put(at + 0.14, _tone(x, 783.99, 4, 0.3))
        elif kind == "ding":  # het gio nghi / lo dap an
            x = np.arange(int(1.2 * SR)) / SR; put(at, _tone(x, 659.25, 3.5, 0.4)); put(at + 0.12, _tone(x, 987.77, 3.5, 0.4))
        elif kind == "buzz":  # bay
            x = np.arange(int(0.18 * SR)) / SR
            s = (np.sin(2 * np.pi * 150 * x) + 0.35 * np.sin(2 * np.pi * 450 * x)) * np.minimum(1, x / 0.005) * np.minimum(1, (0.18 - x) / 0.03) * 0.35
            put(at, s); put(at + 0.24, s)
    out = out / (np.abs(out).max() + 1e-9) * 0.5
    return (out * 32767).astype(np.int16)

def frame(clip, gt):
    for sc in clip["scenes"]:
        if gt < sc["t0"] + sc["T"]: break
    t = gt - sc["t0"]
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img, "RGBA"); IMG_REF[0] = img
    sc["draw"](img, d, t, sc)
    bw, bh = int(W * SCALE), int((SRC1 - SRC0) * SCALE)
    body = img.crop((0, SRC0, W, SRC1)).resize((bw, bh), Image.LANCZOS)
    img = Image.new("RGB", (W, H), BG); img.paste(body, ((W - bw) // 2, DST0)); d = ImageDraw.Draw(img, "RGBA")
    chrome(d, clip, sc, t, gt)
    if t < 0.25: img = Image.blend(Image.new("RGB", (W, H), BG), img, ease(t / 0.25))
    return img

def do_chu(clip):
    """Ghi moi chuoi ve len khung (alpha >= 0,6) moi 0,2 s; dem tu moi xuat hien trong tung canh (so doi thanh #)."""
    rec = []; orig = ImageDraw.ImageDraw.text
    def spy(self, xy, s, *a, **k):
        fill = k.get("fill", a[0] if a else None)
        al = fill[3] / 255 if isinstance(fill, tuple) and len(fill) == 4 else 1.0
        if al >= 0.6 and isinstance(s, str) and s.strip(): rec.append((s.strip(), xy[1]))
        return orig(self, xy, s, *a, **k)
    ImageDraw.ImageDraw.text = spy
    tong = 0
    try:
        for sc in clip["scenes"]:
            seen = set(); t = 0.0
            while t < sc["T"]:
                rec.clear(); frame(clip, sc["t0"] + t)
                for s, y in rec:
                    if y < 150 or y > 1840 or s == sc["title"] or any(s in c for c in sc["caps"]): continue
                    if n_tu(s) >= 2: seen.add(re.sub(r"\d+([,.]\d+)?", "#", s))
                t += 0.2
            w = sum(n_tu(s) for s in seen) + sum(n_tu(c) for c in sc["caps"]); tong += w
            tpm = w / sc["T"] * 60
            print(f"[{sc['key']}] {sc['T']:.1f}s  {w} từ  {tpm:.0f} từ/phút" + ("  ← dày" if tpm > 260 else ""))
    finally:
        ImageDraw.ImageDraw.text = orig
    tpm = tong / clip["TOTAL"] * 60
    print(f"CẢ CLIP {tong} từ / {clip['TOTAL']:.1f}s = {tpm:.0f} từ/phút (mức đọc {WPM}; đích ≤ 200)" + ("  ← dày" if tpm > 200 else ""))

def run(clip, argv):
    build(clip); total = clip["TOTAL"]; print(f"{clip['id']}: {total:.1f}s")
    if "--kich-ban" in argv:   # cong A: kich ban dang chu (khong ve, ~1 giay) de duyet truoc khi xem hinh
        for sc in clip["scenes"]:
            print(f"[{sc['key']}] {sc['title']} · bắt đầu {sc['t0']:.1f}s · dài {sc['T']:.1f}s")
            for m, c in zip(sc["M"], sc["caps"]):
                dd = ImageDraw.Draw(Image.new("RGB", (8, 8))); nl = len(wrap(dd, c, F(46), 900))
                canh = ("  ← quá 8 từ" if n_tu(c) > 8 else "") + ("  ← 2 dòng" if nl > 1 else "")
                print(f"  {sc['t0'] + m:5.1f}s  ({n_tu(c)} từ)  {c}{canh}")
        if "cues" in clip:
            print("tiếng:", ", ".join(f"{t:.1f}s {k}" for t, k in clip["cues"](clip) if k != "tick"))
        print(f"TỔNG {total:.1f}s" + ("  ← quá 50 s" if total > 50.05 else ""))
        return
    if "--do-chu" in argv:     # cong A2: tong chu tren man (the, bang, cau hoi + phu de) / thoi luong -> tu/phut
        do_chu(clip); return
    if "--sheet" in argv:      # cong B: MOT anh ghep khung o moi moc phu de (+1,6 s) va cuoi canh -> ra/<id>-sheet.png
        ts = []
        for sc in clip["scenes"]:
            ts += [sc["t0"] + m + 1.6 for m in sc["M"]] + [sc["t0"] + sc["T"] - 0.1]
        cols = 6; rows = (len(ts) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 360, rows * 640), (0, 0, 0))
        for i, t in enumerate(ts): sheet.paste(frame(clip, t).resize((360, 640)), ((i % cols) * 360, (i // cols) * 640))
        sp = os.path.join(OUT, clip["id"] + "-sheet.png"); sheet.save(sp)
        print(sp); print("khung (trái→phải, trên→dưới):", ", ".join(f"{t:.1f}s" for t in ts))
        return
    if "--preview" in argv:
        pd = os.path.join(OUT, clip["id"] + "-preview"); os.makedirs(pd, exist_ok=True)
        for sc in clip["scenes"]:
            for fr in (0.3, 0.6, 0.97):
                frame(clip, sc["t0"] + sc["T"] * fr).resize((540, 960)).save(os.path.join(pd, f"{sc['key']}_{int(fr*100)}.png"))
        return
    wav = os.path.join(OUT, clip["id"] + ".wav"); a = sfx(total, clip["cues"](clip)) if "cues" in clip else music(total)
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
    out = os.path.join(OUT, clip["id"] + ".mp4")
    p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    N = int(total * FPS)
    for i in range(N):
        p.stdin.write(frame(clip, i / FPS).tobytes())
        if i % 300 == 0: print(f"{i}/{N}", flush=True)
    p.stdin.close(); p.wait(); os.remove(wav)
    print("xong", out, round(os.path.getsize(out) / 1e6, 2), "MB")
