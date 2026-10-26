# Clip mo phong 16 giay, khong loi, 16:9 — hop tn-l12-tdhphantu-04 (bong bay va hai chau nuoc).
# Kich ban + quy tac: docs/KE-HOACH-CLIP-ANH-DONG.md, docs/QUY-TAC-THIET-KE.md V9.
# Chay: python3 clip_bong_bay.py            -> clip-bong-bay.mp4 (khong vao git)
#       python3 clip_bong_bay.py --khung    -> 6 anh kiem tra trong preview/
import math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FF = "ffmpeg"
W, H, FPS, T = 1280, 720, 30, 16.0

_fc = {}
def F(size, bold=True):
    k = (size, bold)
    if k not in _fc:
        f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size)
        f.set_variation_by_name(b"Bold" if bold else b"Regular"); _fc[k] = f
    return _fc[k]

BG = (250, 247, 240); INK = (30, 41, 82); GRAY = (150, 155, 170)
HOT = (226, 84, 62); COLD = (70, 140, 220); WHITE = (255, 255, 255)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def mix(a, b, k): return tuple(int(p + (q - p) * k) for p, q in zip(a, b))
def lerp(a, b, k): return a + (b - a) * k
def refl(p, lo, hi):
    L = hi - lo; q = (p - lo) % (2 * L); return lo + (q if q <= L else 2 * L - q)

# ---------- dong thoi gian: (giay, vi tri x bong, do sau nhung 0..1, ban kinh, toc do phan tu) ----------
X_MID, X_HOT, X_COLD = 640, 330, 950
KEYS = [  # t, x, nhung, r, toc_do
    (0.0, X_MID, 0.0, 95, 1.0), (2.0, X_MID, 0.0, 95, 1.0),
    (3.2, X_HOT, 0.0, 95, 1.0), (4.2, X_HOT, 1.0, 95, 1.0),
    (7.6, X_HOT, 1.0, 128, 2.2), (8.6, X_HOT, 0.0, 128, 2.2),
    (9.8, X_COLD, 0.0, 128, 2.0), (10.8, X_COLD, 1.0, 128, 2.0),
    (13.8, X_COLD, 1.0, 74, 0.45), (14.4, X_COLD, 0.0, 74, 0.45), (16.0, X_COLD, 0.0, 74, 0.45),
]
def state(t):
    for (t0, *a), (t1, *b) in zip(KEYS, KEYS[1:]):
        if t <= t1:
            k = ease((t - t0) / (t1 - t0)) if t1 > t0 else 1
            return [lerp(p, q, k) for p, q in zip(a, b)]
    return KEYS[-1][1:]

# thoi gian "pha" cua phan tu = tich phan toc do (de doi toc do muot, khong giat)
PHASE = [0.0]
for i in range(1, int(T * FPS) + 2):
    PHASE.append(PHASE[-1] + state(i / FPS)[3] / FPS)
def phase(t): return PHASE[min(int(t * FPS), len(PHASE) - 1)]

R = random.Random(7)
MOL = [(R.random(), R.random(), *(lambda a, v: (v * math.cos(a), v * math.sin(a)))(R.uniform(0, 6.28), R.uniform(0.5, 0.9)))
       for _ in range(16)]

SUBS = [(3.0, 8.4, "Nóng → chạy nhanh, đập mạnh", HOT),
        (9.4, 13.9, "Lạnh → chậm lại, đập yếu", COLD),
        (14.2, 16.0, "Đập mạnh hơn = áp suất lớn hơn", INK)]

def arrow(d, p, ang, L, col, w=5):
    q = (p[0] + L * math.cos(ang), p[1] + L * math.sin(ang))
    d.line([p, q], fill=col, width=w)
    for s in (-1, 1):
        a = ang + math.pi - s * math.radians(30)
        d.line([q, (q[0] + 12 * math.cos(a), q[1] + 12 * math.sin(a))], fill=col, width=w)

def basin(d, cx, hot, t):
    x0, x1, top, bot = cx - 190, cx + 190, 470, 640
    water = (*HOT, 70) if hot else (*COLD, 70)
    d.polygon([(x0, top), (x1, top), (x1 - 25, bot), (x0 + 25, bot)], fill=water, outline=GRAY)
    d.rectangle([x0 - 8, top - 10, x1 + 8, top + 4], fill=(205, 205, 215))
    if hot:
        for k in range(4):
            sx = x0 + 70 + k * 80; ph = t * 2.2 + k
            d.line([(sx + 12 * math.sin(ph + j * 0.6), top - 18 - j * 12) for j in range(8)], fill=(190, 190, 200, 170), width=4)
    else:
        for k in range(4):
            ix = x0 + 50 + k * 80; iy = top + 40 + (k % 2) * 45
            d.rounded_rectangle([ix, iy, ix + 54, iy + 46], radius=8, fill=(235, 246, 255), outline=(150, 195, 230), width=3)
    lab = "nước nóng ~60 °C" if hot else "nước đá ~0 °C"
    d.text((cx, bot + 30), lab, font=F(30), fill=HOT if hot else COLD, anchor="mm")

def frame(t):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img, "RGBA")
    basin(d, X_HOT, True, t); basin(d, X_COLD, False, t)
    x, dip, r, v = state(t)
    cy = lerp(270, 470, dip)
    warm = clamp((v - 1.0) / 1.2); cool = clamp((1.0 - v) / 0.55)
    col = mix(mix(INK, HOT, warm), COLD, cool)
    # bong (phan duoi mat nuoc ve mo hon cho thay bong dang nhung)
    d.line([(x, cy + r), (x - 6, cy + r + 18), (x + 4, cy + r + 40)], fill=GRAY, width=3)
    d.ellipse([x - r, cy - r, x + r, cy + r], fill=(*mix(col, WHITE, 0.82), 255), outline=col, width=5)
    # phan tu trong bong + cu dap vao vo bong
    ph = phase(t); s = r * 0.68; box = (x - s, cy - s, x + s, cy + s)
    for (u, w, vx, vy) in MOL:
        px = refl(box[0] + u * 2 * s + vx * 160 * ph, box[0], box[2])
        py = refl(box[1] + w * 2 * s + vy * 160 * ph, box[1], box[3])
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col)
        near = min(px - box[0], box[2] - px, py - box[1], box[3] - py)
        if near < 3 + 4 * v:
            ang = math.atan2(py - cy, px - x)
            arrow(d, (x + r * math.cos(ang), cy + r * math.sin(ang)), ang, 10 + 16 * v, col, 4)
    # nuoc phu len phan bong da nhung
    for cx, c in ((X_HOT, HOT), (X_COLD, COLD)):
        d.polygon([(cx - 190, 472), (cx + 190, 472), (cx + 165, 640), (cx - 165, 640)], fill=(*c, 55))
    # canh cuoi: bong luc nong (bong mo) canh bong luc lanh
    if t > 14.2:
        a = ease((t - 14.2) / 0.6); rh, gy = 110, 250
        d.ellipse([X_HOT - rh, gy - rh, X_HOT + rh, gy + rh], outline=(*HOT, int(255 * a)), width=5,
                  fill=(*mix(HOT, WHITE, 0.82), int(200 * a)))
        for k in range(8):
            ang = k * math.pi / 4 + 0.3
            arrow(d, (X_HOT + rh * math.cos(ang), gy + rh * math.sin(ang)), ang, 30, (*HOT, int(255 * a)), 4)
        d.text((X_HOT, gy + rh + 58), "lúc nóng: căng", font=F(30), fill=(*HOT, int(255 * a)), anchor="mm")
        d.text((x, cy + r + 58), "lúc lạnh: xẹp", font=F(30), fill=(*COLD, int(255 * a)), anchor="mm")
    # phu de: tu khoa, nen mo, giua day
    for t0, t1, txt, c in SUBS:
        if t0 <= t <= t1:
            a = min(ease((t - t0) / 0.3), ease((t1 - t) / 0.3)) if t1 < T else ease((t - t0) / 0.3)
            f = F(46); tw = d.textlength(txt, font=f)
            d.rounded_rectangle([W / 2 - tw / 2 - 26, 40, W / 2 + tw / 2 + 26, 112], radius=18, fill=(20, 24, 40, int(185 * a)))
            d.text((W / 2, 76), txt, font=f, fill=(*WHITE, int(255 * a)), anchor="mm")
    return img

if "--khung" in sys.argv:
    os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
    for t in (1.0, 5.0, 7.5, 10.5, 13.5, 15.5):
        frame(t).save(os.path.join(HERE, "preview", f"bong-bay-{t:04.1f}.webp"), quality=80)
    sys.exit()

out = os.path.join(HERE, "clip-bong-bay.mp4")
p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
                      "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(int(T * FPS)):
    p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait()
print("xong", out, os.path.getsize(out) // 1024, "KB")
