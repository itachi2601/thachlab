"""Bản chiếu trên lớp Làm quen với Vật lí -> tren-lop.html + public/dev/tren-lop/l10-lam-quen-voi-vat-li.html (khung chung scripts/tren-lop/build.py). Không đăng DB."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts" / "tren-lop"))
from build import dung
dung(__file__, qr="tren-lop-qr.svg")
