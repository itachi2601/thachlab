"""Sinh 4 hình SVG cho bài "Bài 2. Thang nhiệt độ" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def hop(x, y, w, h, s, c, size=12):
    """Hộp chữ nhật có chữ canh giữa."""
    return rect(x, y, w, h, "rgba(148,163,184,.10)") + text(x + w / 2, y + h / 2 + 4, s, c, size, "middle", "700")


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------------- Hình 1: một nhiệt độ, ba con số
b = defs("f1")
b += text(16, 26, "Ba thang đo, một nhiệt độ", "currentColor", 13, "start", "700")
b += rect(196, 46, 30, 132, "rgba(148,163,184,.14)", "currentColor", 2.5, 15)           # ống nhiệt kế
b += rect(205, 86, 12, 96, RED, RED, 0, 6)                                               # cột chất lỏng
b += f'<circle cx="211" cy="190" r="17" fill="rgba(248,113,113,.35)" stroke="{RED}" stroke-width="2"/>'
b += f'<circle cx="211" cy="190" r="11" fill="{RED}"/>'
for y, col, so, ten in ((52, GRN, "38,5 °C", "thang Celsius"),
                        (110, BLUE, "311,5 K", "thang Kelvin"),
                        (168, RED, "101,3 °F", "thang Fahrenheit")):
    b += rect(14, y, 140, 42, f"rgba(148,163,184,.10)", col, 1.6, 8)
    b += text(24, y + 22, so, col, 14, "start", "700")
    b += text(24, y + 37, ten, col, 11, "start", "500")
    b += line(156, y + 21, 208, 90, "currentColor", 1.2, "5 4", .7)
b += text(240, 84, "cùng một mức", "currentColor", 11, "start", "600")
b += text(240, 100, "nhiệt độ", "currentColor", 11, "start", "600")
fig1 = wrap("0 0 420 240", "Một nhiệt kế với ba nhãn nhiệt độ theo ba thang đo cho cùng một mức nhiệt độ",
            b, "Hình 1. Ba thang đo, một nhiệt độ: 38,5 °C = 311,5 K = 101,3 °F — chỉ khác cách chia thang.")

# ------------------------------------------------------- Hình 2, 3, 4: ảnh OpenStax (đợt 2, 27/10/2026)
SRC = "<small>OpenStax College Physics 2e, Hình {n} — CC BY‑NC‑SA 4.0</small>"


def raster(f, w, h, alt, cap):
    return (f'<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-thang-nhiet-do/{f}.webp" alt="{alt}" '
            f'loading="lazy" width="{w}" height="{h}"><figcaption>{cap}</figcaption></figure>')


fig2 = raster("hinh-can-bang-nhiet-lon-da-d2", 875, 854,
              "Lon nước ngọt (nhiệt độ T₁) và viên đá (T₂) khác nhau; sau khi tiếp xúc, cả hai cùng nhiệt độ T′",
              "Hình 2. a) Trước: T₁ ≠ T₂. b) Sau tiếp xúc: cùng T′ — cân bằng nhiệt.<br>"
              + SRC.format(n="14.2"))

# mốc FIG3: ba thang đo (Hình 4 trong bài)
fig3 = raster("hinh-ba-thang-fck-d2", 954, 506,
              "Ba thang nhiệt độ F, C, K đặt cạnh nhau với các mốc độ không tuyệt đối, nước đóng băng, thân nhiệt, nước sôi",
              "Hình 4. 0 °C = 273,15 K = 32 °F; 100 °C = 373,15 K = 212 °F.<br>"
              "Nhãn: Absolute zero = độ không tuyệt đối · Freezing/Boiling point = điểm đóng băng/sôi · Normal body temperature = thân nhiệt.<br>"
              + SRC.format(n="13.7"))

# mốc FIG4: ngoại suy về 0 K (Hình 3 trong bài)
fig4 = raster("hinh-ap-suat-nhiet-do-khi-d2", 412, 421,
              "Đồ thị áp suất theo nhiệt độ của bốn chất khí ở thể tích không đổi, các đường kéo dài cùng cắt trục ở −273,15 °C",
              "Hình 3. Bốn khí, kéo dài (nét đứt) đều cắt trục ở −273,15 °C — gốc 0 K.<br>"
              "Nhãn: Pressure = áp suất · Temperature = nhiệt độ · Gas = khí.<br>"
              + SRC.format(n="13.10"))

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
