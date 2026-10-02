#!/usr/bin/env python3
"""Chụp ảnh xem thử bằng Google Chrome headless (không cần Playwright) và ghép ảnh toàn bài.

- Mỗi mục sec-<n>.html: chụp ở bề ngang 375 CSS px, scale 2 → tự cắt phần nền thừa.
- Ghép các mục thành xem-thu/toan-bai.png và bản nửa cỡ toan-bai-nho.png.
- Chụp từng hình fig-<n>.html riêng để soi nhãn/chồng chữ.

Dùng: python3 chup_anh.py
"""
import os, pathlib, signal, subprocess, time
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "xem-thu"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BG = (15, 23, 42)
SCALE = 2


def shoot(page: pathlib.Path, out: pathlib.Path, w: int, h: int):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    udd = f"/tmp/chrome-shot-{os.getpid()}-{out.stem}"
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           "--hide-scrollbars", f"--force-device-scale-factor={SCALE}", f"--user-data-dir={udd}",
           f"--window-size={w},{h}", f"--screenshot={out}", page.as_uri()]
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    size = -1
    for _ in range(240):
        time.sleep(0.25)
        if out.exists():
            s = out.stat().st_size
            if s > 0 and s == size:
                break
            size = s
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    except Exception:
        pass
    if not out.exists():
        raise RuntimeError(f"Chrome không tạo được ảnh cho {page.name}")


def crop_bg(img: Image.Image, pad=14):
    """Cắt bỏ phần nền #0f172a thừa quanh nội dung."""
    px = img.convert("RGB").load()
    w, h = img.size
    rows = [y for y in range(h) if any(sum(abs(px[x, y][i] - BG[i]) for i in range(3)) > 18 for x in range(0, w, 3))]
    cols = [x for x in range(w) if any(sum(abs(px[x, y][i] - BG[i]) for i in range(3)) > 18 for y in range(0, h, 3))]
    if not rows or not cols:
        return img, False
    box = (max(0, cols[0] - pad), max(0, rows[0] - pad), min(w, cols[-1] + pad), min(h, rows[-1] + pad))
    touches_bottom = rows[-1] >= h - 4
    return img.crop(box), touches_bottom


secs = sorted([p for p in OUT.glob("sec-*.html") if p.stem != "sec-sai"],
              key=lambda p: int(p.stem.split("-")[1]))
crops = []
for s in secs:
    png = OUT / f"{s.stem}.png"
    shoot(s, png, 375, 9000)
    im, cut = crop_bg(Image.open(png))
    im.save(png)
    print(f"{s.stem}: {im.width}x{im.height}px" + ("  ⚠ CÓ THỂ BỊ CẮT ĐÁY" if cut else ""))
    crops.append(im)

gap = 28 * SCALE
W = max(c.width for c in crops)
H = sum(c.height for c in crops) + gap * (len(crops) - 1)
full = Image.new("RGB", (W, H), BG)
y = 0
for c in crops:
    full.paste(c, (0, y))
    y += c.height + gap
full.save(OUT / "toan-bai.png")
half = full.resize((max(1, W // 2), max(1, H // 2)), Image.LANCZOS)
half.save(OUT / "toan-bai-nho.png")
print(f"toan-bai.png: {full.width}x{full.height} · toan-bai-nho.png: {half.width}x{half.height}")

for f in sorted(OUT.glob("fig-*.html"), key=lambda p: int(p.stem.split("-")[1])):
    png = OUT / f"{f.stem}.png"
    shoot(f, png, 460, 420)
    im, cut = crop_bg(Image.open(png))
    im.save(png)
    print(f"{f.stem}: {im.width}x{im.height}px")

# Trang chụp thử phản hồi ĐỎ (chọn đáp án sai ở quiz đầu)
sai = OUT / "sec-sai.html"
if sai.exists():
    png = OUT / "mau-tra-loi-sai.png"
    shoot(sai, png, 375, 1800)
    im, cut = crop_bg(Image.open(png))
    im.save(png)
    print(f"mau-tra-loi-sai: {im.width}x{im.height}px")
