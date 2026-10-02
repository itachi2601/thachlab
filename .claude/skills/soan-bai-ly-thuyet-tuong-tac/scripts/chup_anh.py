#!/usr/bin/env python3
"""Chụp ảnh xem thử cho bài lý thuyết bằng Google Chrome headless (Mac không có Playwright).

Dùng: python3 chup_anh.py <thư-mục-xem-thu> [--fig-rong 460] [--cao 9000] [--chi-hinh]

Đầu vào là thư mục do build_preview.py sinh ra (xem-thu.html, sec-*.html, sec-sai.html, fig-*.html).
Sinh ra (WebP, không để lại PNG):
  xem-thu-desktop.webp   — ảnh trang xem thử ở bề ngang máy tính
  sec-<n>.webp           — từng mục <h3> ở bề ngang 375 px (đã mở sẵn <details> + đáp án đúng)
  mau-tra-loi-sai.webp   — trạng thái chọn đáp án sai (phản hồi đỏ), nếu có sec-sai.html
  fig-<n>.webp           — từng hình SVG chụp riêng để soi nhãn

Chrome headless không tự thoát sau khi ghi ảnh → script tự kill đúng nhóm tiến trình của nó.
"""
import os, pathlib, signal, subprocess, sys, time
from PIL import Image

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
    """Cắt bỏ phần nền #0f172a thừa quanh nội dung. Trả về (ảnh, có_chạm_đáy)."""
    px = img.convert("RGB").load()
    w, h = img.size
    rows = [y for y in range(h) if any(sum(abs(px[x, y][i] - BG[i]) for i in range(3)) > 18 for x in range(0, w, 3))]
    cols = [x for x in range(w) if any(sum(abs(px[x, y][i] - BG[i]) for i in range(3)) > 18 for y in range(0, h, 3))]
    if not rows or not cols:
        return img, False
    box = (max(0, cols[0] - pad), max(0, rows[0] - pad), min(w, cols[-1] + pad), min(h, rows[-1] + pad))
    return img.crop(box), rows[-1] >= h - 4


def shot_webp(page: pathlib.Path, out: pathlib.Path, w: int, h: int, quality=88, crop=True):
    tmp = out.with_suffix(".png")
    shoot(page, tmp, w, h)
    im = Image.open(tmp)
    cut = False
    if crop:
        im, cut = crop_bg(im)
    im.save(out, "WEBP", quality=quality, method=6)
    tmp.unlink()
    print(f"{out.name:26s} {im.width}x{im.height}  {out.stat().st_size/1024:5.0f} KB" + ("  ⚠ CÓ THỂ BỊ CẮT ĐÁY" if cut else ""))
    return cut


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    out = pathlib.Path(argv[0]).resolve()
    fig_w = int(argv[argv.index("--fig-rong") + 1]) if "--fig-rong" in argv else 460
    only_figs = "--chi-hinh" in argv
    tall = int(argv[argv.index("--cao") + 1]) if "--cao" in argv else 9000
    if not out.exists():
        print(f"Không thấy thư mục {out} — chạy build_preview.py trước")
        return 1

    if only_figs:
        figs = sorted(out.glob("fig-*.html"), key=lambda p: int(p.stem.split("-")[1]))
        for f in figs:
            shot_webp(f, out / f"{f.stem}.webp", fig_w, 520)
        return 0

    if (out / "xem-thu.html").exists():
        shot_webp(out / "xem-thu.html", out / "xem-thu-desktop.webp", 820, 1150, crop=False)

    secs = sorted([p for p in out.glob("sec-*.html") if p.stem != "sec-sai"],
                  key=lambda p: int(p.stem.split("-")[1]))
    for s in secs:
        shot_webp(s, out / f"{s.stem}.webp", 375, tall, quality=85)
    if not secs:
        print("⚠ không thấy sec-*.html — chạy build_preview.py trước")

    if (out / "sec-sai.html").exists():
        shot_webp(out / "sec-sai.html", out / "mau-tra-loi-sai.webp", 375, 1800, quality=85)

    for f in sorted(out.glob("fig-*.html"), key=lambda p: int(p.stem.split("-")[1])):
        shot_webp(f, out / f"{f.stem}.webp", fig_w, 520)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
