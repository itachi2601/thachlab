"""Bản chiếu trên lớp Độ dịch chuyển và quãng đường -> tren-lop.html + public/dev/tren-lop/l10-do-dich-chuyen-quang-duong.html (khung chung scripts/tren-lop/build.py). Hình chép từ Tập (hinh-l10-bai4.mjs) vào src. Không đăng DB."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts" / "tren-lop"))
from build import dung
dung(__file__, qr="tren-lop-qr.svg")
