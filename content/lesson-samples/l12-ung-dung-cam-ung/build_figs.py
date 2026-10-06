"""Chèn 4 hình SVG vào theory.src.html -> theory.html.
Chạy từ thư mục này:  python3 build_figs.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

# ---- Hình 1: pickup guitar, nhìn ngang
b = defs("f1")
b += text(16, 28, "3  dây thép", "currentColor", 14)
b += '<line x1="150" y1="46" x2="410" y2="46" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
b += arrow("f1", "o", 330, 68, 330, 28, 2.4)
b += arrow("f1", "o", 352, 28, 352, 68, 2.4)
b += text(366, 86, "rung", ORG, 13)
b += '<rect x="150" y="86" width="120" height="118" rx="10" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += f'<rect x="186" y="104" width="48" height="82" fill="none" stroke="{RED}" stroke-width="2.5"/>'
b += text(210, 128, "N", RED, 16, "middle")
b += text(210, 172, "S", BLUE, 16, "middle")
b += '<path d="M196 104 Q150 74 168 46" fill="none" stroke="#f87171" stroke-width="1.8" stroke-dasharray="5 4"/>'
b += '<path d="M224 104 Q270 74 252 46" fill="none" stroke="#f87171" stroke-width="1.8" stroke-dasharray="5 4"/>'
b += text(16, 118, "1  nam châm", RED, 14)
b += text(16, 146, "2  cuộn dây", "currentColor", 14)
b += '<line x1="270" y1="150" x2="400" y2="150" stroke="currentColor" stroke-width="2"/>'
b += text(278, 172, "vào tăng âm", "currentColor", 13)
b += text(16, 214, "Đường đứt: từ thông qua cuộn", RED, 12)
fig1 = wrap("0 0 430 230", "Dây thép rung phía trên nam châm nằm trong cuộn dây của đàn guitar điện",
            b, "Hình 1. Dây thép bị nam châm từ hoá. Dây rung thì từ thông qua cuộn đổi, dòng cảm ứng cùng tần số với dây đi vào máy tăng âm.",
            exp="tn-l12-udcamung-01")

# ---- Hình 2: sạc không dây, hai cuộn
b = defs("f2")
b += '<rect x="28" y="16" width="230" height="78" rx="10" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += text(40, 36, "điện thoại", "currentColor", 13)
b += f'<ellipse cx="78" cy="62" rx="30" ry="16" fill="none" stroke="{BLUE}" stroke-width="2.4"/>'
b += text(118, 58, "cuộn máy", BLUE, 13)
b += text(118, 78, "nối với pin", BLUE, 12)
b += text(140, 118, "không chạm dây", "currentColor", 13)
b += '<rect x="28" y="132" width="230" height="96" rx="10" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += f'<ellipse cx="78" cy="180" rx="36" ry="18" fill="none" stroke="{RED}" stroke-width="2.4"/>'
b += text(124, 172, "cuộn đế sạc", RED, 13)
b += text(124, 194, "điện xoay chiều", RED, 12)
for x in (62, 78, 94):
    b += f'<line x1="{x}" y1="78" x2="{x}" y2="162" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="4 4"/>'
b += text(278, 48, "thứ cấp", BLUE, 15)
b += text(278, 70, "nhận suất", "currentColor", 13)
b += text(278, 90, "điện động", "currentColor", 13)
b += text(278, 168, "sơ cấp", RED, 15)
b += text(278, 190, "gây từ thông", "currentColor", 13)
b += text(278, 210, "biến thiên", "currentColor", 13)
fig2 = wrap("0 0 430 246", "Đế sạc và điện thoại: hai cuộn đặt sát, từ thông biến thiên đi từ cuộn sơ cấp sang cuộn thứ cấp",
            b, "Hình 2. Sạc không dây là một biến áp có khe hở: cuộn đế chạy điện xoay chiều, cuộn trong máy nhận suất điện động.",
            exp="tn-l12-udcamung-02")

# ---- Hình 3: tấm đặc và tấm rãnh
b = defs("f3")
b += f'<rect x="16" y="48" width="32" height="96" fill="none" stroke="{RED}" stroke-width="2.2"/>'
b += text(32, 102, "N", RED, 15, "middle")
b += '<rect x="62" y="36" width="78" height="120" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += f'<path d="M101 58 A24 24 0 1 1 96 64" fill="none" stroke="{ORG}" stroke-width="2.4" marker-end="url(#f3-o)"/>'
b += f'<rect x="154" y="48" width="32" height="96" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
b += text(170, 102, "S", BLUE, 15, "middle")
b += text(16, 180, "tấm đặc", "currentColor", 14)
b += text(16, 200, "tắt nhanh", ORG, 13)
b += f'<rect x="230" y="48" width="32" height="96" fill="none" stroke="{RED}" stroke-width="2.2"/>'
b += text(246, 102, "N", RED, 15, "middle")
for x in (276, 296, 316, 336):
    b += f'<rect x="{x}" y="36" width="14" height="120" fill="none" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="366" y="48" width="32" height="96" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
b += text(382, 102, "S", BLUE, 15, "middle")
b += text(250, 180, "tấm có rãnh", "currentColor", 14)
b += text(250, 200, "tắt chậm", GRN, 13)
fig3 = wrap("0 0 430 216", "Tấm nhôm đặc và tấm nhôm xẻ rãnh dao động giữa hai cực nam châm",
            b, "Hình 3. Tấm đặc có vòng Foucault kín nên bị hãm mạnh. Rãnh cắt vòng đó, tấm đung đưa lâu hơn.",
            exp="tn-l12-udcamung-04")

# ---- Hình 4: bếp từ, mặt cắt
b = defs("f4")
b += '<path d="M70 36 L70 108 L250 108 L250 36" fill="none" stroke="currentColor" stroke-width="2.6"/>'
b += '<path d="M58 128 L58 44 L262 44 L262 128 Z" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(160, 78, "nước", "currentColor", 14, "middle")
b += f'<ellipse cx="160" cy="118" rx="48" ry="8" fill="none" stroke="{ORG}" stroke-width="2.4"/>'
b += f'<path d="M196 114 A20 6 0 0 1 188 122" fill="none" stroke="{ORG}" stroke-width="2" marker-end="url(#f4-o)"/>'
b += text(270, 118, "đáy nóng", ORG, 13)
b += f'<line x1="24" y1="148" x2="300" y2="148" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>'
b += text(308, 152, "kính", BLUE, 13)
b += f'<ellipse cx="160" cy="190" rx="56" ry="18" fill="none" stroke="{RED}" stroke-width="2.6"/>'
b += text(230, 186, "cuộn bếp", RED, 13)
b += text(230, 206, "xoay chiều", RED, 13)
b += text(16, 228, "Nhiệt ở đáy nồi, không ở mặt kính", "currentColor", 13)
fig4 = wrap("0 0 430 244", "Mặt cắt bếp từ: cuộn dưới mặt kính, dòng Foucault trong đáy nồi",
            b, "Hình 4. Cuộn bếp tạo từ thông biến thiên. Một vòng Foucault trong đáy nồi là vòng của bài toán mẫu.",
            exp="tn-l12-udcamung-05")

src = (HERE / "theory.src.html").read_text(encoding="utf-8")
for n, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG:{n}-->" in src, n
    src = src.replace(f"<!--FIG:{n}-->", f)
(HERE / "theory.html").write_text(src, encoding="utf-8")
print("ok", len(src))
