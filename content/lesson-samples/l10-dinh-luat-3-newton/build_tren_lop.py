"""Bản chiếu trên lớp Định luật 3 Newton -> tren-lop.html + public/dev/tren-lop/l10-dinh-luat-3-newton.html (khung chung scripts/tren-lop/build.py). Không đăng DB."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts" / "tren-lop"))
from build import dung
dung(__file__, qr="tren-lop-qr.svg")
