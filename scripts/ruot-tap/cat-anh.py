"""Cắt hình từ Halliday "Fundamentals of Physics 12th" cho ruột tập (thầy chốt 25/10: tài liệu nội bộ, không xét giấy phép).
Chạy: python3 scripts/ruot-tap/cat-anh.py  → scripts/ruot-tap/anh/*.png (≤150 KB, gitignore) + bản sao BACKUP ngoài repo.
Toạ độ bbox tính ở 100 dpi (x0, y0, x1, y1) trên trang PDF; render lại ở 200 dpi rồi cắt. Thêm hình: thêm một dòng vào ANH."""
import re, subprocess, sys, tempfile, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DIR = Path('/Users/MAC/Documents/THPT/số hoá THPT/Fundamentals of Physics 12th')
V2 = DIR / 'Fundamentals of Physics 12th Volume 2.pdf'
OUT = Path(__file__).resolve().parent / 'anh'
BACKUP = Path('/Users/MAC/Documents/THPT/số hoá THPT/ruot-tap-anh')
# tên tệp: (pdf, trang PDF, bbox@100dpi, nguồn hình trong sách)
ANH = {
    'rutherford-bo-thi-nghiem.png':      (V2, 737, (595, 80, 715, 285),   'Fig 42.1.1 — bố trí thí nghiệm Rutherford (bài 14)'),
    'rutherford-alpha-qua-la-vang.png':  (V2, 737, (605, 712, 785, 1032), 'Fig 42.1.3 — đường đi hạt α qua lá vàng (bài 14)'),
    'nang-luong-lien-ket-rieng.png':     (V2, 743, (150, 635, 520, 935),  'Fig 42.2.3 — năng lượng liên kết riêng theo số khối (bài 15)'),
    'lo-phan-ung-nuoc-ap-luc.png':       (V2, 778, (255, 615, 770, 978),  'Fig 43.2.2 — sơ đồ nhà máy điện hạt nhân PWR (bài 16)'),
    'chu-trinh-proton-proton.png':       (V2, 784, (305, 868, 735, 1042),  'Fig 43.5.1 — chu trình proton–proton trong Mặt trời (bài 16)'),
    'phong-xa-do-thi-ln-r.png':          (V2, 748, (440, 716, 775, 942),  'Fig 42.3.1 — đồ thị ln R theo t, độ dốc −λ (bài 17)'),
}
# Dịch nhãn tiếng Anh trong hình (che bằng màu nền rồi viết tiếng Việt). Khoá = tên tệp; giá trị = danh sách bản dịch THEO THỨ TỰ các dòng chữ
# trong bbox (pdftotext -bbox-layout) — dòng nào không muốn đổi thì None. Dòng xoay dọc (nhãn trục y) để nguyên, chú thích HTML nói rõ.
DICH = {
    'rutherford-bo-thi-nghiem.png': ['Nguồn α', 'Lá vàng', 'Máy dò'],
    'rutherford-alpha-qua-la-vang.png': ['Hạt α tới', 'Lá', 'vàng', 'Nguyên tử', 'Hạt nhân'],
    'lo-phan-ung-nuoc-ap-luc.png': ['Hơi (áp cao)', 'Điện', 'năng', 'Máy phát', 'điện', 'Tua bin', 'Hơi (áp thấp)', 'Nước', 'nóng', 'Nước mát vào',
        'Bình', 'sinh hơi', 'Lõi', 'lò', 'Bình', 'ngưng', 'Bơm', 'Nước', 'nguội', 'Bình', 'áp lực lò', 'Vòng sơ cấp', 'Nước mát ra',
        'Bơm', 'Nước', '(áp cao)', 'Nước', '(áp thấp)', 'Vòng thứ cấp'],
}
# nhãn trong nang-luong-lien-ket-rieng.png chỉ dịch theo nội dung (các dòng kí hiệu hạt nhân giữ nguyên)
DICH_THEO_CHU = {'phong-xa-do-thi-ln-r.png': {'Time (min)': 't (phút)'},
    'nang-luong-lien-ket-rieng.png': {'The large nuclei': 'Hạt nhân lớn', 'over here are more': 'ở đây liên kết', 'loosely bound.': 'lỏng hơn',
    'The most tightly': 'Hạt nhân bền', 'bound nuclei lie': 'nhất nằm ở', 'at the peak.': 'đỉnh.', 'Mass number A': 'Số khối A'}}
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'

def dong_chu(pdf, page, bb):
    """Các dòng chữ ngang nằm trong bbox (đơn vị pt) theo thứ tự trong tệp; bỏ dòng xoay dọc (cao hơn rộng)."""
    subprocess.run(['pdftotext', '-bbox-layout', '-f', str(page), '-l', str(page), str(pdf), '/tmp/_cat_anh.html'], check=True)
    t = open('/tmp/_cat_anh.html').read(); b = [v * .72 for v in bb]; out = []
    for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', t, re.S):
        x0, y0, x1, y1 = [float(v) for v in m.groups()[:4]]
        if b[0] - 2 <= x0 and x1 <= b[2] + 2 and b[1] - 2 <= y0 and y1 <= b[3] + 2:
            out.append(((x0, y0, x1, y1), ' '.join(re.findall(r'>([^<]+)</word>', m.group(5)))))
    return out

def dich(im, name, pdf, page, bb):
    todo = []
    lines = dong_chu(pdf, page, bb)
    if name in DICH:
        ngang = [l for l in lines if (l[0][2] - l[0][0]) >= (l[0][3] - l[0][1])]
        assert len(ngang) == len(DICH[name]), (name, len(ngang), [t for _, t in ngang])
        todo = [(box, vi) for (box, _), vi in zip(ngang, DICH[name]) if vi]
    elif name in DICH_THEO_CHU:
        todo = [(box, DICH_THEO_CHU[name][t]) for box, t in lines if t in DICH_THEO_CHU[name]]
    d = ImageDraw.Draw(im); k = 200 / 72
    for (x0, y0, x1, y1), vi in todo:
        X0, Y0, X1, Y1 = [int(round(v * k)) - o for v, o in zip((x0, y0, x1, y1), (bb[0] * 2, bb[1] * 2, bb[0] * 2, bb[1] * 2))]
        vung = im.crop((max(X0, 0), max(Y0, 0), X1, Y1)).convert('RGB')
        bg = max(vung.getcolors(1 << 20), key=lambda c: c[0])[1]   # màu nền = màu nhiều nhất trong ô chữ
        d.rectangle((X0 - 2, Y0 - 1, X1 + 2, Y1 + 1), fill=bg)
        size = max(int((Y1 - Y0) * 1.05), 12)
        while True:
            f = ImageFont.truetype(FONT, size)
            w = d.textlength(vi, font=f)
            if w <= min((X1 - X0) * 1.3, im.width - X0 - 2) or size <= 12: break
            size -= 1
        d.text((min(max((X0 + X1) / 2 - w / 2, 1), im.width - w - 1), Y0 - 1), vi, font=f, fill=(20, 20, 40))
    return im

OUT.mkdir(parents=True, exist_ok=True); BACKUP.mkdir(parents=True, exist_ok=True)
for name, (pdf, page, bb, src) in ANH.items():
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['pdftoppm', '-r', '200', '-f', str(page), '-l', str(page), '-png', str(pdf), f'{t}/p'], check=True)
        im = Image.open(next(Path(t).glob('p-*.png'))).convert('RGB')
    im = im.crop(tuple(v * 2 for v in bb))
    im = dich(im, name, pdf, page, bb)
    # nén: giảm bảng màu cho ≤150 KB mà nét còn rõ
    for colors in (64, 32, 16):
        q = im.quantize(colors=colors, dither=Image.Dither.NONE)
        q.save(OUT / name, optimize=True)
        if (OUT / name).stat().st_size <= 150_000: break
    shutil.copy(OUT / name, BACKUP / name)
    print(f'{name}: {im.size[0]}×{im.size[1]} px, {(OUT / name).stat().st_size // 1000} KB  ← {src}')
