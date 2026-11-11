"""Đo khoảng trống cuối trang của sách in: mỗi trang lấy đáy nội dung (chữ + nét vẽ + ảnh, bỏ đầu/chân trang),
báo trang có khoảng trống cuối ≥ NGUONG mm. Chạy: /usr/bin/python3 do_trong.py out/<tep>.pdf [nguong_mm]"""
import sys, fitz
pdf = sys.argv[1]; NG = float(sys.argv[2]) if len(sys.argv) > 2 else 60
d = fitz.open(pdf); mm = 72 / 25.4; tong = 0; ds = []
for i, p in enumerate(d, 1):
    H = p.rect.height; top, bot = 14 * mm, H - 19 * mm   # vùng nội dung (bỏ header/footer)
    ys = [b[3] for b in p.get_text('blocks') if top < b[1] < bot]
    ys += [r.y1 for r in (dr['rect'] for dr in p.get_drawings()) if top < r.y0 < bot and r.height < H * .9]
    ys += [r.y1 for im in p.get_images(full=True) for r in p.get_image_rects(im[0]) if top < r.y0 < bot]
    if not ys: continue
    trong = (bot - max(ys)) / mm
    if trong >= NG: ds.append((i, round(trong)))
    tong += max(trong, 0)
print(f'{len(d)} trang · trống cuối trang tổng {tong/10:.0f} cm · trang trống ≥{NG:.0f} mm: {len(ds)}')
print(' '.join(f'{i}:{t}' for i, t in ds))
