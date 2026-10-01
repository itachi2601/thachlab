"""Chèn 3 hình SVG tự vẽ vào theory.html (idempotent: chạy lại thì thay khối cũ)."""
import re
RED, BLUE, ORG, GRN = "#f87171", "#38bdf8", "#fb923c", "#34d399"

def defs(prefix):
    out = "<defs>"
    for n, c in (("r", RED), ("b", BLUE), ("o", ORG), ("g", GRN)):
        out += (f'<marker id="{prefix}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"

def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    col = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}[c]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d} marker-end="url(#{p}-{c})"/>'

def text(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'

def person(x, ground, s=1.0, arm_to=None, arm_y=None):
    """Người trượt băng dạng que: đầu, thân, chân, giày trượt (lưỡi dao)."""
    hy = ground - 100 * s; ty = ground - 62 * s; fy = ground - 6 * s
    g = f'<circle cx="{x}" cy="{hy:.0f}" r="{12*s:.0f}" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x}" y1="{hy+12*s:.0f}" x2="{x}" y2="{ty:.0f}" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x}" y1="{ty:.0f}" x2="{x-12*s:.0f}" y2="{fy:.0f}" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x}" y1="{ty:.0f}" x2="{x+12*s:.0f}" y2="{fy:.0f}" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x-22*s:.0f}" y1="{ground-2}" x2="{x+22*s:.0f}" y2="{ground-2}" stroke="{BLUE}" stroke-width="3" stroke-linecap="round"/>'
    sh = hy + 22 * s
    if arm_to is not None:
        g += f'<line x1="{x}" y1="{sh:.0f}" x2="{arm_to}" y2="{arm_y}" stroke="currentColor" stroke-width="2.5"/>'
    return g

def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

# ---- Hình 1: đẩy thành sân
b = defs("f1")
b += '<line x1="10" y1="190" x2="430" y2="190" stroke="#38bdf8" stroke-width="2" opacity=".6"/>'
b += text(430, 184, "mặt băng", BLUE, 11, "end", "400")
b += '<rect x="14" y="40" width="26" height="150" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
b += text(14, 30, "Thành sân", "currentColor", 12, "start")
b += person(190, 190, 1.0, 42, 112)
b += arrow("f1", "r", 130, 96, 46, 96)
b += text(60, 84, "F₁: em đẩy thành", RED)
b += arrow("f1", "b", 198, 128, 280, 128)
b += text(204, 118, "F₂: thành đẩy em", BLUE)
b += arrow("f1", "g", 150, 214, 300, 214, 2, "6 4")
b += text(310, 218, "em trượt lùi", GRN, 12, "start")
fig1 = wrap("0 0 440 230", "Em đẩy thành sân: lực F1 đặt lên thành, phản lực F2 đặt lên em",
            b, "Hình 1. F₁ đặt lên <strong>thành</strong>, F₂ đặt lên <strong>em</strong>: hai lực bằng nhau về độ lớn, ngược chiều, nhưng ở hai vật khác nhau.", exp="tn-l10-newton3-02")

# ---- Hình 2: sách trên bàn (hình tách rời)
b = defs("f2")
b += '<rect x="150" y="60" width="120" height="60" rx="3" fill="rgba(251,146,60,.15)" stroke="currentColor" stroke-width="2"/>'
b += text(210, 52, "Quyển sách", "currentColor", 12, "middle")
b += '<rect x="90" y="190" width="240" height="40" rx="3" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2"/>'
b += '<line x1="110" y1="230" x2="110" y2="262" stroke="currentColor" stroke-width="2.5"/><line x1="310" y1="230" x2="310" y2="262" stroke="currentColor" stroke-width="2.5"/>'
b += text(120, 214, "Mặt bàn", "currentColor", 12, "start")
b += arrow("f2", "o", 185, 90, 185, 140)
b += text(172, 108, "P", ORG, 15, "end", "700")
b += arrow("f2", "o", 235, 120, 235, 72)
b += text(247, 88, "N", ORG, 15, "start", "700")
b += arrow("f2", "b", 235, 190, 235, 238)
b += text(247, 226, "N′", BLUE, 15, "start", "700")
b += '<line x1="235" y1="124" x2="235" y2="186" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 4" opacity=".7"/>'
b += text(246, 160, "N và N′: cặp lực – phản lực", "currentColor", 11, "start", "400")
b += text(10, 22, "● Cam: lực đặt lên SÁCH (cân bằng nhau)", ORG, 12)
b += text(10, 40, "● Xanh: lực đặt lên BÀN", BLUE, 12)
fig2 = wrap("0 0 420 270", "Sách trên bàn: P và N cân bằng cùng đặt lên sách; N và N' là cặp lực phản lực",
            b, "Hình 3. P và N cùng đặt lên sách (<em>cân bằng</em>). N (lên sách) và N′ (lên bàn) mới là <em>lực – phản lực</em>.", exp="tn-l10-newton3-03")

# ---- Hình 3: hai bạn đẩy nhau
b = defs("f3")
b += '<line x1="10" y1="180" x2="430" y2="180" stroke="#38bdf8" stroke-width="2" opacity=".6"/>'
b += person(110, 180, 0.85, 200, 104) + person(310, 180, 1.1, 200, 104)
b += text(110, 200, "A: 40 kg", "currentColor", 12, "middle")
b += text(310, 200, "B: 60 kg", "currentColor", 12, "middle")
b += arrow("f3", "r", 100, 150, 44, 150) + text(24, 138, "F = 120 N", RED, 12)
b += arrow("f3", "r", 320, 150, 376, 150) + text(340, 138, "F = 120 N", RED, 12)
b += arrow("f3", "g", 200, 52, 80, 52) + text(140, 42, "a<tspan dy=\"4\" font-size=\"9\">A</tspan><tspan dy=\"-4\"> = 3 m/s²</tspan>", GRN, 12, "middle")
b += arrow("f3", "g", 215, 52, 290, 52) + text(255, 42, "a<tspan dy=\"4\" font-size=\"9\">B</tspan><tspan dy=\"-4\"> = 2 m/s²</tspan>", GRN, 12, "middle")
fig3 = wrap("0 0 440 215", "Hai bạn đẩy nhau trên giày trượt: lực bằng nhau, gia tốc của bạn nhẹ hơn lớn hơn",
            b, "Hình 4. Lực (đỏ) bằng nhau; gia tốc (xanh) của bạn A nhẹ hơn <em>dài hơn</em>.", exp="tn-l10-newton3-04")


# ---- Hình 4: hai lực kế móc nhau
b = defs("f4")
b += '<rect x="30" y="70" width="110" height="36" rx="5" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2"/>'
b += '<rect x="280" y="70" width="110" height="36" rx="5" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2"/>'
b += '<line x1="140" y1="88" x2="280" y2="88" stroke="currentColor" stroke-width="2.5"/><circle cx="210" cy="88" r="5" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(85, 94, "5 N", "currentColor", 15, "middle", "700") + text(335, 94, "5 N", "currentColor", 15, "middle", "700")
b += text(85, 128, "Lực kế 1", "currentColor", 12, "middle") + text(335, 128, "Lực kế 2", "currentColor", 12, "middle")
b += arrow("f4", "r", 196, 56, 150, 56) + text(196, 46, "lực kế 2 kéo 1", RED, 12, "end")
b += arrow("f4", "b", 224, 56, 270, 56) + text(224, 46, "lực kế 1 kéo 2", BLUE, 12, "start")
fig4 = wrap("0 0 430 140", "Hai lực kế móc vào nhau luôn chỉ cùng một số",
            b, "Hình 2. Kéo mạnh hay nhẹ, hai lực kế vẫn chỉ <strong>bằng nhau</strong> và đổi cùng lúc.", exp="tn-l10-newton3-01")

def ins(html, anchor, fig, before=True):
    html = re.sub(r'<figure class="fig" data-tl="1"[^>]*>.*?</figure>\n?', lambda m: m.group(0) if fig[:0] else m.group(0), html, flags=re.S)
    return html

h = open("theory.html").read()
h = re.sub(r'<figure class="fig" data-tl="1"[^>]*>.*?</figure>\n', "", h, flags=re.S)
h = h.replace('<div class="tl-sim" data-sim="tn-l10-newton3-04"></div>\n', "")
a0 = '<div class="tl-box tl-box--exp" data-exp="tn-l10-newton3-01">'
a1 = '<p>Muốn nhớ nhanh, em nhớ 4 chữ'
a2 = '<div class="tl-box tl-box--think">\n<p class="tl-label">✍️ Tự kiểm tra ngay (chọn là có đáp án)'
a3 = '<div class="tl-box tl-box--think">\n<p class="tl-label">✍️ Thử sức, tự kiểm tra ngay</p>'
SIM = '<div class="tl-sim" data-sim="tn-l10-newton3-04"></div>'
for a, f in ((a0, fig4), (a1, fig1), (a2, fig2), (a3, fig3 + "\n" + SIM)):
    assert a in h, a
    h = h.replace(a, f + "\n" + a, 1)
open("theory.html", "w").write(h)
