# Bo dung video thi nghiem doc 9:16 (khong loi: phu de + nhac nen tong hop). Khung lay tu
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

def text(d, xy, s, size, color=INK, bold=True, anchor="mm", alpha=1.0):
    d.text(xy, s, font=F(size, bold), fill=A(color, alpha), anchor=anchor)

def ctext(d, y, s, size, color=INK, bold=True, maxw=940, alpha=1.0, lh=1.22):
    f = F(size, bold); ls = wrap(d, s, f, maxw)
    y0 = y - (len(ls) - 1) * size * lh / 2
    for i, l in enumerate(ls):
        d.text((W / 2, y0 + i * size * lh), l, font=f, fill=A(color, alpha), anchor="mm")

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

def keyword(d, s, t, at, color=ORANGE, y=1400, size=54, sub=None):
    if t < at: return
    k = back((t - at) / 0.5); f = F(size); ls = wrap(d, s, f, 880)
    hh = len(ls) * size * 1.2 + 60 + (50 if sub else 0)
    card(d, (60, y - hh / 2, 1020, y + hh / 2), fill=WHITE, outline=color, w=6)
    yy = y - hh / 2 + 30 + size * 0.6
    for l in ls:
        d.text((W / 2, yy), l, font=f, fill=A(color, k), anchor="mm"); yy += size * 1.2
    if sub: text(d, (W / 2, yy + 10), sub, 34, MUTED, alpha=k)

# ---------------- nhip phu de ----------------
def cap_dur(s): return max(2.3, 0.052 * len(s) + 0.9)
def build(clip):
    t0 = 0.0
    for sc in clip["scenes"]:
        sc["t0"] = t0; t = 0.4; sc["M"] = []
        durs = [c[1] if isinstance(c, tuple) else cap_dur(c) for c in sc["caps"]]
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
    text(d, (W / 2 - (1 - k) * 60, 178), sc["title"], 60, INK, alpha=k)
    cur = cur_cap(sc, t)
    if cur >= 0:
        f = F(46); ls = wrap(d, sc["caps"][cur], f, 900)
        hgt = len(ls) * 58 + 50; y1 = 1790; y0 = y1 - hgt
        a = appear(t, sc["M"][cur] - 0.05, 0.25)
        card(d, (60, y0, 1020, y1), fill=A(NAVY, 0.92 * a), r=30)
        for j, l in enumerate(ls):
            d.text((W / 2, y0 + 25 + 29 + j * 58), l, font=f, fill=A(WHITE, a), anchor="mm")
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

def frame(clip, gt):
    for sc in clip["scenes"]:
        if gt < sc["t0"] + sc["T"]: break
    t = gt - sc["t0"]
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img, "RGBA")
    sc["draw"](img, d, t, sc)
    chrome(d, clip, sc, t, gt)
    if t < 0.25: img = Image.blend(Image.new("RGB", (W, H), BG), img, ease(t / 0.25))
    return img

def run(clip, argv):
    build(clip); total = clip["TOTAL"]; print(f"{clip['id']}: {total:.1f}s")
    if "--preview" in argv:
        pd = os.path.join(OUT, clip["id"] + "-preview"); os.makedirs(pd, exist_ok=True)
        for sc in clip["scenes"]:
            for fr in (0.3, 0.6, 0.97):
                frame(clip, sc["t0"] + sc["T"] * fr).resize((540, 960)).save(os.path.join(pd, f"{sc['key']}_{int(fr*100)}.png"))
        return
    wav = os.path.join(OUT, clip["id"] + ".wav"); a = music(total)
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
