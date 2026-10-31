"""Chèn hình 1, 2, 3 (ảnh OpenStax) vào theory.html (idempotent). Chạy từ thư mục này:
python3 build_figs.py"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, re, sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

# ---- Hình 1: ảnh OpenStax Hình 23.6 (đợt 2, 27/10/2026)
OSX = "Hình: OpenStax, College Physics 2e, Hình {n} — CC BY\u2011NC\u2011SA 4.0 — openstax.org/books/college-physics-2e"
fig1 = ('<figure class="fig" data-tl="1" data-exp="tn-l12-camungdt-03"><img src="/assets/openstax/l12-cam-ung-dien-tu/hinh-tu-thong-dong-gia.webp" '
        'alt="Mặt phẳng diện tích A trong từ trường đều B, pháp tuyến hợp với B góc theta, thành phần B cos theta" loading="lazy" width="600" height="607">'
        '<figcaption>Hình 1. Pháp tuyến nghiêng khỏi <strong>B</strong>: số đường sức xuyên qua giảm. θ là α, A là S của bài.<br>'
        'Normal = pháp tuyến<br>'
        + OSX.format(n="23.6") + '</figcaption></figure>')

# ---- Hình 2 và 3: ảnh OpenStax College Physics 2e (CC BY-NC-SA 4.0), chèn trực tiếp (webp trong public/assets/openstax/)
fig2 = ('<figure class="fig" data-tl="1" data-exp="tn-l12-camungdt-01"><img src="/assets/openstax/l12-cam-ung-dien-tu/hinh-2.webp" '
        'alt="Thanh nam châm đưa vào rồi kéo ra khỏi cuộn dây nối điện kế, kim điện kế lệch ngược chiều nhau" loading="lazy" width="420" height="372">'
        '<figcaption>Hình 2. Nam châm vào (a), ra (b): kim lệch ngược nhau.<br>'
        'Galvanometer = điện kế<br>'
        + OSX.format(n="23.4 (hai phần a, b)") + '</figcaption></figure>')

# ---- Hình 3: ảnh OpenStax Hình 23.7 (phần a, cắt bỏ tay phải RHR-2), đợt 2
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l12-cam-ung-dien-tu/hinh-lenz-nam-cham-tien-lai.webp" '
        'alt="Cực Bắc của thanh nam châm tiến lại cuộn dây; từ trường cảm ứng của cuộn hướng ngược lại, đẩy ra" loading="lazy" width="700" height="215">'
        '<figcaption>Hình 3. Từ thông tăng: cuộn dây sinh từ trường ngược, <em>đẩy</em> nam châm ra.<br>'
        'B<sub>mag</sub>, B<sub>coil</sub> = từ trường nam châm, cuộn dây<br>'
        + OSX.format(n="23.7 (phần a)") + '</figcaption></figure>')

src = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
