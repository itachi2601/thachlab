# Trich khung 375 px thanh dai 4 khung (moc giay in vang) de soat mat: python khung-375.py <ten clip> <thu muc ra>
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import engine
from PIL import Image, ImageDraw
mod = importlib.import_module("clips." + sys.argv[1]); clip = mod.CLIP; engine.build(clip)
ts = []; n = len(clip["scenes"])
for i, sc in enumerate(clip["scenes"]):
    pts = [sc["t0"] + m + 1.6 for m in sc["M"]] + [sc["t0"] + sc["T"] - 0.1]
    if i >= n - 2 or i == 0: pts += [sc["t0"] + sc["T"] * f for f in (0.35, 0.6, 0.8)]
    else: pts += [sc["t0"] + sc["T"] * 0.5]
    ts += [min(p, sc["t0"] + sc["T"] - 0.05) for p in pts]
ts = sorted(set(round(t, 1) for t in ts))
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for k in range(0, len(ts), 4):
    grp = ts[k:k + 4]; strip = Image.new("RGB", (4 * 375, 667 + 26), (0, 0, 0)); d = ImageDraw.Draw(strip)
    for j, t in enumerate(grp):
        strip.paste(engine.frame(clip, t).resize((375, 667), Image.LANCZOS), (j * 375, 26)); d.text((j * 375 + 8, 6), f"{t:.1f}s", fill=(255, 255, 0))
    strip.save(os.path.join(out, f"{sys.argv[1]}-{k // 4 + 1:02d}.png"))
print(sys.argv[1], len(ts), "khung", clip["TOTAL"])
