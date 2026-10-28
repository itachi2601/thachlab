"""Sinh theory.html (chèn 3 hình SVG vào theory.src.html), 3 mục kho thí nghiệm và bundle.json.
Chạy từ thư mục này: python3 build.py"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

# ---- Hình 1: con lắc lò xo, VTCB và hai biên
b = defs("f1")
O, A, y = 230, 100, 100
b += f'<line x1="22" y1="55" x2="22" y2="135" stroke="currentColor" stroke-width="4"/>'
for yy in range(60, 135, 12):
    b += f'<line x1="22" y1="{yy}" x2="12" y2="{yy+8}" stroke="currentColor" stroke-width="1.5" opacity=".5"/>'
pts = [(22, y)]
x0, x1 = 22, O - 20
n = 10
for i in range(n):
    pts.append((x0 + (x1 - x0) * (i + .5) / n, y + (-14 if i % 2 == 0 else 14)))
pts.append((x1, y))
b += '<polyline points="' + " ".join(f"{px:.0f},{py:.0f}" for px, py in pts) + '" fill="none" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="{O-20}" y="{y-20}" width="40" height="40" rx="4" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2.5"/>'
for px in (O - A, O + A):
    b += f'<rect x="{px-20}" y="{y-20}" width="40" height="40" rx="4" fill="none" stroke="{ORG}" stroke-width="2" stroke-dasharray="5,4"/>'
b += f'<line x1="20" y1="148" x2="410" y2="148" stroke="currentColor" stroke-width="1.5" opacity=".6" marker-end="url(#f1-b)"/>'
for px, s in ((O - A, "−A"), (O, "O"), (O + A, "+A")):
    b += f'<line x1="{px}" y1="{y+20}" x2="{px}" y2="152" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,3" opacity=".5"/>'
    b += text(px, 170, s, ORG if s != "O" else "currentColor", 14, "middle", "700")
b += text(400, 166, "x", "currentColor", 13, "end")
b += arrow("f1", "g", O - 30, 40, O - A + 22, 40, 2.5) + arrow("f1", "g", O + 30, 40, O + A - 22, 40, 2.5)
b += text(O, 32, "dao động qua lại", GRN, 13, "middle")
b += text(O, 205, "O là vị trí cân bằng", "currentColor", 12, "middle", "500")
FIG1 = wrap("0 0 440 215", "Con lắc lò xo dao động qua lại quanh vị trí cân bằng O giữa hai biên −A và +A", b,
            "Hình 1. Con lắc lò xo: vật dao động quanh vị trí cân bằng O, giữa hai biên −A và +A.", "tn-l11-daodongdieuhoa-01")

# ---- Hình 2, 3 (28/10/2026): ảnh OpenStax College Physics 2e Hình 16.11 và 16.18, thay SVG tự vẽ (ngoại lệ có chủ đích: ảnh raster)
FIG2 = '<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-dao-dong-dieu-hoa/hinh-do-thi-li-do-tren-giay.webp" alt="Vật nặng treo lò xo dao động thẳng đứng, bút gắn vào vật vẽ đường hình sin lên tờ giấy chạy đều; trục đứng là li độ từ −X đến X, T là một chu kì" loading="lazy" width="625" height="678"><figcaption>Hình 2. Bút vẽ trên giấy chạy đều ra đường hình sin.<br>Trục đứng: li độ, từ −X đến X (X là biên độ A).<br>T: một chu kì.<br><small>Hình: OpenStax, College Physics 2e, Hình 16.11 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>'
FIG3 = '<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-dao-dong-dieu-hoa/hinh-hinh-chieu-chuyen-dong-tron.webp" alt="Quả cầu quay đều trên đĩa, ánh sáng chiếu thẳng làm bóng của nó chạy qua lại; bóng vẽ ra đường hình sin trên tờ giấy chạy đều" loading="lazy" width="525" height="768"><figcaption>Hình 3. Quả cầu quay đều, bóng của nó dao động qua lại.<br>Trên giấy chạy đều, bóng vẽ ra đường hình sin.<br>Nhãn: Lights = đèn.<br><small>Hình: OpenStax, College Physics 2e, Hình 16.18 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>'

html = (HERE / "theory.src.html").read_text(encoding="utf-8")
html = html.replace("{{FIG1}}", FIG1).replace("{{FIG2}}", FIG2).replace("{{FIG3}}", FIG3)
(HERE / "theory.html").write_text(margin_figs(html), encoding="utf-8")
print("theory.html", len(html.encode()), "bytes")
