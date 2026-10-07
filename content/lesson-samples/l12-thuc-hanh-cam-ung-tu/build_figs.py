"""Sinh 4 hình SVG cho bài "Bài 11. Thực hành đo độ lớn cảm ứng từ" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


RED_F, BLUE_F, GREY_F = "rgba(248,113,113,.28)", "rgba(56,189,248,.28)", "rgba(148,163,184,.16)"

# ======================================================= Hình 1: bố trí cân dòng điện
b = ""
b += rect(30, 218, 190, 34, GREY_F)                       # bệ cân
b += rect(140, 226, 70, 20, "rgba(52,211,153,.18)", GRN, 1.5, 4)
b += text(175, 241, "1,45 g", GRN, 14, "middle", "700")
b += line(34, 214, 216, 214, "currentColor", 4)           # đĩa cân
# nam châm chữ U trên đĩa
b += rect(60, 120, 36, 94, RED_F, RED, 2, 3)
b += rect(158, 120, 36, 94, BLUE_F, BLUE, 2, 3)
b += rect(60, 182, 134, 32, GREY_F, "currentColor", 2, 3)
b += text(78, 160, "N", RED, 17, "middle", "700")
b += text(176, 160, "S", BLUE, 17, "middle", "700")
# giá đỡ riêng + khung dây
b += line(346, 40, 346, 252, "currentColor", 5)
b += line(127, 40, 346, 40, "currentColor", 5)
b += line(346, 252, 300, 252, "currentColor", 5)
b += line(127, 40, 127, 150, "currentColor", 2)
b += f'<circle cx="127" cy="152" r="7" fill="{ORG}" stroke="{ORG}" stroke-width="2"/>'
b += text(140, 90, "khung dây", "currentColor", 14, "start", "600")
b += text(140, 108, "(cạnh dưới ở trong khe)", "currentColor", 14, "start", "600")
b += text(140, 28, "giá đỡ riêng, không chạm cân", "currentColor", 14, "start", "700")
b += text(206, 170, "nam châm", "currentColor", 14, "start", "600")
b += text(206, 188, "chữ U", "currentColor", 14, "start", "600")
b += text(30, 272, "cân điện tử chia 0,01 g", "currentColor", 14, "start", "600")
b += text(30, 291, "nguồn một chiều + ampe kế nối với khung", "currentColor", 14, "start", "600")
fig1 = wrap("0 0 380 300", "Cân điện tử có nam châm chữ U trên đĩa; khung dây treo trên giá riêng, cạnh dưới nằm trong khe nam châm, cân chỉ 1,45 gam",
            b, "Hình 1. Bố trí cân dòng điện: nam châm chữ U nằm trên đĩa cân, khung dây treo trên giá đứng riêng với cạnh dưới trong khe. Dây không chạm vào cân hay nam châm.")

# ======================================================= Hình 2: lực và phản lực (mặt cắt khe nam châm)
b = defs("f2")
b += text(20, 28, "⊙ dòng điện hướng ra khỏi trang", "currentColor", 14, "start", "700")
b += rect(20, 240, 230, 40, GREY_F)
b += text(135, 266, "cân điện tử", "currentColor", 14, "middle", "700")
b += rect(30, 110, 50, 130, RED_F, RED, 2, 3)
b += rect(190, 110, 50, 130, BLUE_F, BLUE, 2, 3)
b += rect(30, 200, 210, 40, GREY_F, "currentColor", 2, 3)
b += text(55, 160, "N", RED, 18, "middle", "700")
b += text(215, 160, "S", BLUE, 18, "middle", "700")
b += arrow("f2", "g", 88, 172, 182, 172, 3)
b += arrow("f2", "g", 88, 189, 182, 189, 3)
b += text(106, 166, "B", GRN, 16, "middle", "700")
b += line(135, 50, 135, 141, "currentColor", 1.5)
b += '<circle cx="135" cy="150" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="135" cy="150" r="3" fill="currentColor"/>'
b += arrow("f2", "r", 152, 142, 152, 92, 3.5)
b += text(160, 100, "F lên dây", RED, 14, "start", "700")
b += arrow("f2", "o", 262, 130, 262, 195, 3.5)
b += text(272, 150, "F′ lên", ORG, 14, "start", "700")
b += text(272, 168, "nam châm", ORG, 14, "start", "700")
fig2 = wrap("0 0 380 290", "Mặt cắt khe nam châm: dây có dòng hướng ra khỏi trang chịu lực từ hướng lên, nam châm chịu phản lực hướng xuống làm cân tăng",
            b, "Hình 2. Mặt cắt khe nam châm chữ U. Đường sức từ đi từ cực N sang cực S. Dây chịu lực $F$, nam châm chịu lực $F'$ cùng độ lớn và ngược chiều; cân chỉ cảm nhận $F'$.")

# ======================================================= Hình 3: đồ thị Δm–I
X0, Y0, KX, KY = 56, 215, 56, 62     # gốc, px mỗi A, px mỗi g
pts = [(1, .50), (2, .97), (3, 1.45), (4, 1.97), (5, 2.44)]
SLOPE = sum(i * m for i, m in pts) / sum(i * i for i, _ in pts)
b = text(60, 26, "Δm (g)", "currentColor", 14, "start", "700")
for g in (.5, 1, 1.5, 2, 2.5):
    y = Y0 - g * KY
    b += line(X0, y, 350, y, "currentColor", 1, "", .18)
    b += text(48, y + 5, str(g).replace(".", ",").rstrip("0").rstrip(",") if g != int(g) else str(int(g)), "currentColor", 14, "end", "500")
for i in range(1, 6):
    x = X0 + i * KX
    b += line(x, Y0, x, Y0 + 6, "currentColor", 2)
    b += text(x, Y0 + 24, str(i), "currentColor", 14, "middle", "500")
b += line(X0, Y0, 352, Y0, "currentColor", 2.5)
b += line(X0, Y0, X0, 36, "currentColor", 2.5)
b += text(352, Y0 + 44, "I (A)", "currentColor", 14, "end", "700")
b += line(X0, Y0, X0 + 5.1 * KX, Y0 - SLOPE * 5.1 * KY, GRN, 2.6)
for i, m in pts:
    b += f'<circle cx="{X0 + i * KX}" cy="{Y0 - m * KY:.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>'
b += text(78, 92, "độ dốc ≈ 0,489 g/A", GRN, 14, "start", "700")
b += text(78, 112, "→ B ≈ 0,12 T", GRN, 14, "start", "700")
fig3 = wrap("0 0 380 272", "Đồ thị khối lượng tăng theo cường độ dòng điện: năm điểm đo nằm gần đường thẳng qua gốc toạ độ có độ dốc khoảng 0,489 gam trên ampe",
            b, "Hình 3. Δm tăng gần tỉ lệ với $I$: năm điểm đo (số liệu minh hoạ) nằm sát đường thẳng qua gốc toạ độ. Độ dốc đường thẳng bằng $Bl/g$.",
            "tn-l12-thuchanhtu-01")

# ======================================================= Hình 4: dây hợp góc với đường sức
b = defs("f4")
b += arrow("f4", "g", 40, 150, 330, 150, 3)
b += text(342, 157, "B", GRN, 16, "start", "700")
b += line(120, 150, 195, 20, "currentColor", 4)
b += '<circle cx="120" cy="150" r="5" fill="currentColor"/>'
b += text(206, 46, "dây, dòng I", "currentColor", 14, "start", "700")
b += '<path d="M165,150 A45,45 0 0 0 142.5,111" fill="none" stroke="' + ORG + '" stroke-width="2.5"/>'
b += text(176, 134, "θ = 60°", ORG, 14, "start", "700")
b += '<circle cx="64" cy="204" r="9" fill="none" stroke="' + RED + '" stroke-width="2"/><circle cx="64" cy="204" r="3" fill="' + RED + '"/>'
b += text(82, 209, "lực từ F hướng ra khỏi trang", RED, 14, "start", "700")
b += text(40, 238, "F = B·I·l·sin θ", "currentColor", 16, "start", "700")
fig4 = wrap("0 0 380 250", "Dây hợp với đường sức từ một góc 60 độ; lực từ hướng ra khỏi trang và có độ lớn B nhân I nhân l nhân sin theta",
            b, "Hình 4. Dây hợp với đường sức góc $\\theta$ (vẽ trong mặt phẳng chứa $\\vec B$ và dây). Lực từ vuông góc với mặt phẳng đó; độ lớn $F = BIl\\sin\\theta$.",
            "tn-l12-thuchanhtu-03")


# ======================================================= Mô phỏng (radio + CSS, không JS)
VAL = {1: (0.50, 4.91, 0.123), 2: (0.97, 9.52, 0.119), 3: (1.45, 14.22, 0.119), 4: (1.97, 19.33, 0.121), 5: (2.44, 23.94, 0.120)}
vn = lambda x, d: f"{x:.{d}f}".replace(".", ",")
vm = lambda x, d: f"{x:.{d}f}".replace(".", "{,}")

# Nam châm chữ U: hai cánh 40×140 + gông 190×40; trọng tâm tính từ ba hình chữ nhật.
UP = "M40,112 H80 V252 H190 V112 H230 V292 H40 Z"
_parts = [(40 * 140, 60, 182), (40 * 140, 210, 182), (190 * 40, 135, 272)]
GX = sum(a * x for a, x, _ in _parts) / sum(a for a, _, _ in _parts)
GY = sum(a * y for a, _, y in _parts) / sum(a for a, _, _ in _parts)
GXr, GYr = round(GX), round(GY)

COL = {"F": RED, "Fp": ORG, "Q": "#a78bfa", "N": GRN, "P": "#94a3b8", "B": BLUE}


def arr(cx, cy, key, cls, w):
    """Mũi tên có độ dài/ chiều do CSS (--L, --sg) quyết định; đuôi ở đúng (cx, cy)."""
    c = COL[key]
    return (f'<g transform="translate({cx},{cy})">'
            f'<rect class="sim-sh {cls}" x="{-w/2}" y="-120" width="{w}" height="120" fill="{c}"/>'
            f'<polygon class="sim-hd {cls}" points="0,0 -7,13 7,13" fill="{c}"/></g>')


def wire(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="9" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
            f'<circle class="sim-wp" cx="{cx}" cy="{cy}" r="3" fill="currentColor"/>'
            f'<path class="sim-wn" d="M{cx-5},{cy-5} L{cx+5},{cy+5} M{cx+5},{cy-5} L{cx-5},{cy+5}" stroke="currentColor" stroke-width="2"/>')


def hatch(x1, x2, y, n, c="currentColor"):
    step = (x2 - x1) / n
    return "".join(line(x1 + k * step, y, x1 + k * step - 9, y + 11, c, 1.6, "", .7) for k in range(n + 1))


def sim_html():
    WY = 150  # tâm dây
    sv = defs("sm")
    sv += text(20, 22, "B đi từ N sang S →", GRN, 14, "start", "700")
    # mặt bàn + cân
    sv += line(8, 336, 372, 336, "currentColor", 3) + hatch(14, 366, 337, 26)
    sv += rect(20, 292, 230, 44, GREY_F)
    sv += text(135, 311, "cân điện tử", "currentColor", 14, "middle", "700")
    sv += rect(40, 318, 190, 10, "none", "currentColor", 1, 3)
    sv += '<rect class="sim-bar" x="135" y="318" width="95" height="10" rx="3" fill="#fb923c"/>'
    sv += text(28, 327, "−", "currentColor", 14, "middle", "700") + text(242, 327, "+", "currentColor", 14, "middle", "700")
    # nam châm chữ U: cực N, S ở đầu cánh
    sv += rect(40, 112, 40, 64, RED_F, "none", 0, 0) + rect(190, 112, 40, 64, BLUE_F, "none", 0, 0)
    sv += f'<path d="{UP}" fill="{GREY_F}" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>'
    sv += text(60, 150, "N", RED, 17, "middle", "700") + text(210, 150, "S", BLUE, 17, "middle", "700")
    # đường sức B
    sv += arrow("sm", "g", 88, 122, 122, 122, 3) + arrow("sm", "g", 148, 122, 182, 122, 3)
    # giá gá cứng: đế bắt xuống bàn, trụ, tay đỡ, thanh treo, ngàm ôm dây, bu lông
    sv += rect(284, 326, 60, 10, "rgba(148,163,184,.45)", "currentColor", 2, 2) + hatch(286, 342, 337, 6)
    sv += rect(306, 50, 16, 278, "rgba(148,163,184,.4)", "currentColor", 2, 2)
    sv += rect(135, 50, 187, 14, "rgba(148,163,184,.4)", "currentColor", 2, 2)
    sv += rect(130, 64, 10, 70, "rgba(148,163,184,.4)", "currentColor", 2, 2)
    sv += f'<path d="M118,128 H152 V{WY} a17,17 0 0 1 -34,0 Z" fill="rgba(148,163,184,.55)" stroke="currentColor" stroke-width="2"/>'
    for (bx, by) in ((314, 58), (314, 100), (314, 300), (135, 98), (135, 124)):
        sv += f'<circle cx="{bx}" cy="{by}" r="3.2" fill="currentColor"/>'
    sv += text(150, 42, "giá gá cứng xuống bàn", "currentColor", 14, "start", "700")
    sv += wire(135, WY)
    sv += f'<circle cx="{GXr}" cy="{GYr}" r="4" fill="currentColor"/>' + text(GXr + 9, GYr - 6, "G", "currentColor", 14, "start", "700")
    sv += arr(135, WY, "F", "a-F", 4) + arr(GXr, GYr, "Fp", "a-Fp", 4)
    sv += text(160, 150, "F", RED, 15, "start", "700") + text(GXr + 22, GYr + 20, "F′", ORG, 15, "start", "700")
    scene = (f'<svg viewBox="0 0 380 346" role="img" aria-label="Mô phỏng cân dòng điện: nam châm chữ U đặt trên cân, dây gá cứng trên giá, chọn dòng điện để đổi lực và số cân">{sv}</svg>')

    # biểu đồ lực: ba vật, đuôi mũi tên đặt đúng trọng tâm
    CY = 180
    fb = ""
    for k, (cx, ten) in enumerate(((63, "Dây điện"), (190, "Nam châm"), (317, "Cân"))):
        fb += text(cx, 20, ten, "currentColor", 14, "middle", "700")
    fb += wire(63, CY)
    ux, uy, us = 190, CY, .55
    fb += f'<g transform="translate({ux - GX * us:.2f},{uy - GY * us:.2f}) scale({us})">{rect(40,112,40,64,RED_F,"none",0,0)}{rect(190,112,40,64,BLUE_F,"none",0,0)}<path d="{UP}" fill="{GREY_F}" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round"/></g>'
    fb += rect(262, CY - 22, 110, 44, GREY_F)
    # mũi tên dày (trọng lực, phản lực pháp tuyến) vẽ trước, mũi tên mảnh (lực từ, lực giữ) đè lên
    fb += arr(190, CY, "P", "a-Pm", 6) + arr(190, CY, "N", "a-N", 6)
    fb += arr(317, CY, "P", "a-Pc", 6) + arr(317, CY, "N", "a-Np", 6) + arr(317, CY, "B", "a-Qb", 6)
    fb += arr(63, CY, "F", "a-F", 3.6) + arr(63, CY, "Q", "a-Q", 3.6) + arr(190, CY, "Fp", "a-Fp", 3.6)
    for cx in (63, 190, 317):
        fb += f'<circle cx="{cx}" cy="{CY}" r="4" fill="currentColor"/>'
    fb += text(76, CY - 8, "G", "currentColor", 14, "start", "700") + text(203, CY - 8, "G", "currentColor", 14, "start", "700") + text(330, CY - 8, "G", "currentColor", 14, "start", "700")
    fbd = (f'<div class="tl-sim__fbd"><svg viewBox="0 0 380 300" role="img" aria-label="Biểu đồ lực tác dụng lên dây, nam châm và cân; đuôi mũi tên đặt tại trọng tâm G của từng vật">{fb}</svg>'
           '<ul class="tl-sim__leg">'
           '<li><strong>Dây:</strong> <span class="lg lg-F">●</span> F lực từ · <span class="lg lg-Q">●</span> Q lực giữ của giá (ngược F, dây đứng yên). Trọng lực của dây rất nhỏ nên bỏ qua.</li>'
           '<li><strong>Nam châm:</strong> <span class="lg lg-P">●</span> P trọng lực · <span class="lg lg-Fp">●</span> F′ phản lực của F · <span class="lg lg-N">●</span> N phản lực của cân (N = P + F′).</li>'
           '<li><strong>Cân:</strong> <span class="lg lg-P">●</span> P trọng lực · <span class="lg lg-N">●</span> N′ áp lực của nam châm (bằng N) · <span class="lg lg-B">●</span> phản lực của mặt bàn.</li>'
           '</ul><p>G là trọng tâm: dây ở tâm tiết diện, cân ở tâm bệ, còn nam châm chữ U có G nằm <em>trong khe</em>, trên gông. Mũi tên F, F′ phóng to cho dễ thấy; các mũi tên khác không vẽ theo tỉ lệ.</p></div>')

    h = '<div class="tl-box tl-box--exp tl-sim" data-exp="tn-l12-thuchanhtu-04">\n<p class="tl-label">🎛️ Mô phỏng: tự chỉnh dòng điện, quan sát cân</p>\n'
    h += '<div class="tl-sim__row"><b>Cường độ dòng điện</b>'
    for i in range(6):
        h += f'<input type="radio" name="tls12-i" class="tls-i{i}" id="tls12-i{i}"' + (" checked" if i == 0 else "") + ">"
        h += f'<label for="tls12-i{i}" class="tl-sim__chip">{i} A</label>'
    h += '</div>\n<div class="tl-sim__row"><b>Chiều dòng điện</b>'
    h += '<input type="radio" name="tls12-d" class="tls-dir-f" id="tls12-df" checked><label for="tls12-df" class="tl-sim__chip">⊙ ra khỏi trang</label>'
    h += '<input type="radio" name="tls12-d" class="tls-dir-r" id="tls12-dr"><label for="tls12-dr" class="tl-sim__chip">⊗ vào trong trang</label></div>\n'
    h += '<div class="tl-sim__row"><input type="checkbox" class="tls-force" id="tls12-force"><label for="tls12-force" class="tl-sim__chip">Hiện các lực</label></div>\n'
    h += scene + '\n<div aria-live="polite">\n'
    h += '<div class="tl-sim__st st-0"><p>Cân: <strong>0,00 g</strong></p><p>Không có dòng điện nên không có lực từ.</p></div>\n'
    for i, (m, f, bb) in VAL.items():
        for sg, sc in (("p", "+"), ("n", "−")):
            h += (f'<div class="tl-sim__st st-{i}{sg}"><p>Cân: <strong>{sc}{vn(m, 2)} g</strong></p>'
                  f'<p>$F = \\Delta m\\, g \\approx {vm(f, 2)}\\ \\text{{mN}}$ · $B = \\dfrac{{F}}{{Il}} \\approx {vm(bb, 3)}\\ \\text{{T}}$</p></div>\n')
    h += '</div>\n' + fbd + '\n<p>Thử: (1) tăng $I$ từng nấc — số cân và mũi tên đổi thế nào? (2) đảo chiều ở cùng $I$. (3) bật <em>Hiện các lực</em> và so độ dài $N$ với $P$ của nam châm. Số liệu minh hoạ, khớp bảng ở mục II.3 ($l = 4{,}0\\ \\text{cm}$).</p>\n</div>'
    return h

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
assert "<!--SIM-->" in src
src = src.replace("<!--SIM-->", sim_html())
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes; slope", round(SLOPE, 4))
