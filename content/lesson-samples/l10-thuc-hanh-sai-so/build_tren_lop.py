"""Bản chiếu trên lớp Thực hành tính sai số -> tren-lop.html + public/dev/tren-lop/l10-thuc-hanh-sai-so.html (khung chung scripts/tren-lop/build.py). Hình trong src chép từ ruột tập (hinh-l10-bai3.mjs). Không đăng DB."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts" / "tren-lop"))
from build import dung
dung(__file__, qr="tren-lop-qr.svg")
