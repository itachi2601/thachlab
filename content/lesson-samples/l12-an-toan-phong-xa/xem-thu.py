"""Xem thử bài "Bài 18. An toàn phóng xạ": build_preview -> tách trang mục II (quá cao) -> chup_anh.

Vì sao cần: `chup_anh.py` chụp từng mục <h3> ở scale 2; WebP chỉ cho ảnh cao tối đa 16 383 px,
tức trang preview phải thấp dưới ~8 190 CSS px. Mục "II. Kiến thức" của bài này có 6 mục con nên
cao ~9 500 CSS px (ảnh 19 000 px) — quá giới hạn, Pillow báo "Image size exceeds WebP limit".
Script này cắt riêng trang sec-2.html tại các mốc <h4> thành sec-2.html + sec-21.html + sec-22.html
rồi mới gọi chup_anh.py, nên ảnh xem thử vẫn phủ đủ cả 6 mục con.

Chạy từ thư mục bài: python3 xem-thu.py [--giu-png]
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SKILL = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"
OUT = HERE / "xem-thu"
SO_MANH = 3

if not SKILL.exists():
    ROOT = pathlib.Path("/Users/MAC/Projects/thachlab")
    SKILL = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"

subprocess.run([sys.executable, str(SKILL / "build_preview.py"), str(HERE / "theory.html")], check=True)

trang = OUT / "sec-2.html"
s = trang.read_text(encoding="utf8")
dau = s.index('<span class="exam-content">') + len('<span class="exam-content">')
cuoi = s.rindex("</span></div></div>")
tien, than, hau = s[:dau], s[dau:cuoi], s[cuoi:]

manh = re.split(r"(?=<h4>)", than)
if len(manh) < 2:
    raise SystemExit("sec-2.html không có <h4> để tách")
# gom các mảnh <h4> thành SO_MANH nhóm, cân theo số ký tự
tong = sum(len(m) for m in manh)
gioi_han = tong / SO_MANH * 1.15
nhom, hien = [], [manh[0]]
for m in manh[1:]:
    if sum(len(x) for x in hien) + len(m) > gioi_han and len(nhom) < SO_MANH - 1:
        nhom.append("".join(hien))
        hien = [m]
    else:
        hien.append(m)
nhom.append("".join(hien))

ten_file = ["sec-2.html"] + [f"sec-2{n}.html" for n in range(1, len(nhom))]
for ten, body in zip(ten_file, nhom):
    (OUT / ten).write_text(tien + body + hau, encoding="utf8")
    print(f"{ten}: {len(body)} ký tự")
# dọn các trang tách của lần chạy trước nếu lần này ít nhóm hơn
for p in OUT.glob("sec-2*.html"):
    if p.name not in ten_file:
        p.unlink()
        print("xoá", p.name)

args = sys.argv[1:]
subprocess.run([sys.executable, str(SKILL / "chup_anh.py"), str(OUT), "--kiem-tran"], check=True)
subprocess.run([sys.executable, str(SKILL / "chup_anh.py"), str(OUT)] + args, check=True)
print("xong — xem ảnh trong", OUT)
