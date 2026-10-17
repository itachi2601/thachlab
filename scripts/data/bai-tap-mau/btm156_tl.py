# -*- coding: utf-8 -*-
"""CĐ07 Thấu kính mỏng và kính lúp (lesson 156) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 17/10/2026 theo dàn ý content/hsg9/cd07-thau-kinh-kinh-lup/nguon.md (mục Tự luận TL1–TL8; số trong tinh.py),
phỏng theo kiểu đề HSG 9 / tuyển sinh 10 chuyên phổ biến, không chép đề cụ thể nào; số liệu khác 7 dạng mẫu và khác docx.
Quy ước dấu (nguon.md): d > 0 vật thật; d' > 0 ảnh thật, d' < 0 ảnh ảo; f > 0 hội tụ, f < 0 phân kì; 1/f = 1/d + 1/d'.
Hình SVG vẽ trong file này (bài 1, bài 5): hình đề không vẽ sẵn ảnh; hình lời giải nằm trong <details>."""
from fractions import Fraction as F
from math import isqrt

# ───────────────────────── hình SVG ─────────────────────────
RAY, OBJ, IMG, GRID = "#dc2626", "#2563eb", "#16a34a", "#94a3b8"


def _txt(x, y, s, c="currentColor", size=18, anchor="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" text-anchor="{anchor}" font-weight="600">{s}</text>'


def _ln(x1, y1, x2, y2, c="currentColor", w=1.6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def _arrow_mid(x1, y1, x2, y2, c, L=9):
    """Đầu mũi tên chữ V ở giữa đoạn, chỉ chiều truyền ánh sáng."""
    import math
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    a = math.atan2(y2 - y1, x2 - x1)
    pts = []
    for s in (+1, -1):
        b = a + math.pi - s * math.radians(30)
        pts.append((mx + L * math.cos(b), my + L * math.sin(b)))
    return (f'<polyline points="{pts[0][0]:.1f},{pts[0][1]:.1f} {mx:.1f},{my:.1f} {pts[1][0]:.1f},{pts[1][1]:.1f}" '
            f'fill="none" stroke="{c}" stroke-width="2"/>')


def _ray(p, q, c=RAY):
    return _ln(*p, *q, c=c, w=2) + _arrow_mid(*p, *q, c)


def _lens_ht(x, y1, y2):
    """Thấu kính hội tụ: đoạn thẳng, hai đầu mũi tên hướng ra."""
    s = _ln(x, y1, x, y2, w=2.4)
    for y, dy in ((y1, 1), (y2, -1)):
        s += f'<polyline points="{x-7:.1f},{y+9*dy:.1f} {x:.1f},{y:.1f} {x+7:.1f},{y+9*dy:.1f}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    return s


def _vec(x, y0, y1, c, label, lx_off=-12):
    """Mũi tên vật/ảnh thẳng đứng từ (x,y0) tới (x,y1)."""
    dy = 1 if y1 > y0 else -1
    s = _ln(x, y0, x, y1, c=c, w=3)
    s += f'<polyline points="{x-6:.1f},{y1-9*dy:.1f} {x:.1f},{y1:.1f} {x+6:.1f},{y1-9*dy:.1f}" fill="none" stroke="{c}" stroke-width="3"/>'
    return s


def _wrap(vb, label, body, cap):
    return (f'<figure class="fig"><svg viewBox="{vb}" role="img" aria-label="{label}" '
            f'style="max-width:100%;height:auto">{body}</svg><figcaption>{cap}</figcaption></figure>')


def fig_tl1(giai=False):
    """Giấy ô ly 1 ô = 1 cm; x từ −11 đến 21 cm, y từ −4 đến 3 cm; O ở gốc."""
    u, x0, y0 = 14, 11 * 14 + 14, 3 * 14 + 16       # px/cm, gốc O
    X = lambda c: x0 + c * u
    Y = lambda c: y0 - c * u
    W, H = X(21) + 10, Y(-4) + 10
    s = "".join(_ln(X(i), Y(3), X(i), Y(-4), c=GRID, w=0.6) for i in range(-11, 22))
    s += "".join(_ln(X(-11), Y(j), X(21), Y(j), c=GRID, w=0.6) for j in range(-4, 4))
    s += _ln(X(-11), Y(0), X(21), Y(0), w=1.6)                      # trục chính
    s += _lens_ht(X(0), Y(2.8), Y(-3.8))
    for c, n in ((-6, "F"), (6, "F′")):
        s += f'<circle cx="{X(c):.1f}" cy="{Y(0):.1f}" r="3" fill="currentColor"/>' + _txt(X(c), Y(0) + 22, n)
    s += _txt(X(0) + 10, Y(0) + 22, "O", anchor="start")
    s += _vec(X(-9), Y(0), Y(1), OBJ, "B") + _txt(X(-9) - 10, Y(1) - 2, "B", c=OBJ, anchor="end")
    s += _txt(X(-9), Y(0) + 22, "A", c=OBJ)
    if giai:
        B, I, K, Bp = (X(-9), Y(1)), (X(0), Y(1)), (X(0), Y(-2)), (X(18), Y(-2))
        s += _ray(B, I) + _ray(I, Bp)                                  # tia song song → qua F′
        s += _ray(B, (X(0), Y(0))) + _ray((X(0), Y(0)), Bp)            # tia qua O
        s += _ray(B, K) + _ray(K, Bp)                                  # tia qua F → song song
        s += _vec(X(18), Y(0), Y(-2), IMG, "B′") + _txt(X(18) + 10, Y(-2) + 6, "B′", c=IMG, anchor="start")
        s += _txt(X(18), Y(0) - 8, "A′", c=IMG)
        cap = "Ba tia từ B gặp nhau tại B′ (18 ô; 2 ô dưới trục). 1 ô = 1 cm."
        lab = "Lời giải bài 1: ba tia đặc biệt từ B qua thấu kính hội tụ gặp nhau tại B′ phía sau thấu kính"
    else:
        cap = "Giấy ô ly, 1 ô = 1 cm: trục chính, thấu kính hội tụ, F, F′ và vật AB."
        lab = "Đề bài 1: lưới ô ly có trục chính, thấu kính hội tụ tại O, tiêu điểm F và F′ cách O 6 ô, vật AB cao 1 ô cách O 9 ô"
    return _wrap(f"0 0 {W:.0f} {H:.0f}", lab, s, cap)


def fig_tl5(giai=False):
    """Điểm sáng S trên trục chính, TK hội tụ f = 10 cm, SO = 25 cm; 1 cm = 9 px."""
    u, x0, y0 = 9, 27 * 9 + 12, 6 * 9 + 16
    X = lambda c: x0 + c * u
    Y = lambda c: y0 - c * u
    W, H = X(21) + 14, Y(-4) + 14
    s = _ln(X(-27), Y(0), X(21), Y(0), w=1.6) + _lens_ht(X(0), Y(5.6), Y(-3.6))
    for c, n in ((-10, "F"), (10, "F′")):
        s += f'<circle cx="{X(c):.1f}" cy="{Y(0):.1f}" r="3" fill="currentColor"/>' + _txt(X(c), Y(0) + 23, n)
    s += _txt(X(0) + 10, Y(0) + 23, "O", anchor="start")
    s += f'<circle cx="{X(-25):.1f}" cy="{Y(0):.1f}" r="4.5" fill="{OBJ}"/>' + _txt(X(-25), Y(0) + 23, "S", c=OBJ)
    if giai:
        yF1 = F(4, 25) * 10
        S_, I_, F1, Sp = (X(-25), Y(0)), (X(0), Y(4)), (X(10), Y(float(yF1))), (X(float(F(50, 3))), Y(0))
        s += _ray(S_, I_) + _ray(I_, Sp)
        s += _ln(X(-6), Y(-6 * 0.16), X(16), Y(16 * 0.16), c="currentColor", w=1.2, dash="6 4")   # trục phụ
        s += _ln(X(10), Y(5), X(10), Y(-3.5), c=GRID, w=1.2, dash="4 4")                         # tiêu diện ảnh
        s += f'<circle cx="{F1[0]:.1f}" cy="{F1[1]:.1f}" r="3" fill="currentColor"/>' + _txt(F1[0] + 6, F1[1] - 8, "F′₁", anchor="start")
        s += _txt(I_[0] - 8, I_[1] - 6, "I", anchor="end")
        s += f'<circle cx="{Sp[0]:.1f}" cy="{Sp[1]:.1f}" r="4.5" fill="{IMG}"/>' + _txt(Sp[0] + 4, Sp[1] + 19, "S′", c=IMG, anchor="start")
        cap = "Trục phụ (nét đứt) song song SI cắt tiêu diện ảnh tại F′₁; tia ló đi qua F′₁ và cắt trục chính tại S′."
        lab = "Lời giải bài 5: tia SI, trục phụ song song SI, tiêu điểm phụ F′1 và ảnh S′ trên trục chính"
    else:
        cap = "Điểm sáng S nằm trên trục chính của thấu kính hội tụ."
        lab = "Đề bài 5: điểm sáng S trên trục chính, thấu kính hội tụ tại O, tiêu điểm F và F′"
    return _wrap(f"0 0 {W:.0f} {H:.0f}", lab, s, cap)


# ───────────────────────── đề + hướng dẫn ─────────────────────────
QUY_UOC = (r"<p><em>Quy ước dùng trong các bài:</em> thấu kính mỏng; vật sáng $AB$ đặt vuông góc với trục chính, $A$ nằm trên trục chính; "
           r"$d=OA\gt0$; $d'\gt0$ là ảnh thật, $d'\lt0$ là ảnh ảo; $f\gt0$ với thấu kính hội tụ, $f\lt0$ với thấu kính phân kì; "
           r"$\dfrac1f=\dfrac1d+\dfrac1{d'}$, $\dfrac{h'}{h}=\dfrac{|d'|}{d}$. Mọi khoảng cách tính bằng cm.</p>")

TL = [
 # ── Bài 1 · Dễ: dựng ảnh trên giấy ô ly + tính
 ("Dễ", r"""<p>Một thấu kính hội tụ có tiêu cự $6\ \text{cm}$. Vật sáng $AB$ cao $1\ \text{cm}$ đặt vuông góc với trục chính, $A$ nằm trên trục chính và cách thấu kính $9\ \text{cm}$.</p>
<p>a) Vẽ lại hình dưới đây lên giấy ô ly (1 ô = 1 cm) rồi dựng ảnh $A'B'$ bằng hai tia đặc biệt; dùng tia thứ ba để kiểm tra. Đọc trên lưới: ảnh cách thấu kính bao nhiêu ô, cao bao nhiêu ô?</p>
<p>b) Dùng công thức thấu kính tính khoảng cách từ ảnh đến thấu kính và chiều cao của ảnh; so với kết quả đọc trên lưới.</p>
<p>c) Nêu tính chất của ảnh (thật hay ảo, cùng chiều hay ngược chiều, lớn hay nhỏ hơn vật) và tính khoảng cách giữa vật và ảnh.</p>"""
  + fig_tl1(False),
  r"""<p>a) Từ $B$ vẽ hai tia: tia song song trục chính tới thấu kính ở $I$ (1 ô trên trục) thì tia ló đi qua $F'$; tia qua quang tâm $O$ truyền thẳng.</p>
<p>Hai tia ló cắt nhau tại $B'$; hạ đường vuông góc xuống trục chính được $A'$.</p>
<p>Tia thứ ba: tia từ $B$ đi qua $F$ tới thấu kính ở $K$, tia ló song song trục chính, cũng đi qua $B'$.</p>"""
  + fig_tl1(True) +
  r"""<p>Đọc trên lưới: $A'$ cách thấu kính $18$ ô, $A'B'$ dài $2$ ô (dưới trục chính).</p>
<p>b) $\dfrac1{d'}=\dfrac1f-\dfrac1d=\dfrac16-\dfrac19=\dfrac1{18}$ nên $d'=18\ \text{cm}$.</p>
<p>$h'=h\cdot\dfrac{|d'|}{d}=1\cdot\dfrac{18}{9}=2\ \text{cm}$. Khớp với lưới.</p>
<p>c) $d'\gt0$ nên ảnh thật, ngược chiều vật, lớn gấp $2$ lần vật.</p>
<p>Ảnh thật nằm khác phía vật nên khoảng cách vật–ảnh $L=d+d'=9+18=27\ \text{cm}$.</p>
<p>Đáp số: $d'=18\ \text{cm}$; $h'=2\ \text{cm}$; ảnh thật, ngược chiều, lớn hơn vật; $L=27\ \text{cm}$.</p>
<p>Lỗi hay gặp: đặt $F$, $F'$ lệch một ô; dựng tia từ $A$ thay vì từ $B$ (tia từ $A$ nằm trên trục chính, không cho giao điểm).</p>"""),

 # ── Bài 2 · Dễ: thấu kính phân kì
 ("Dễ", r"""<p>Một thấu kính phân kì có tiêu cự $10\ \text{cm}$ (theo quy ước dấu, $f=-10\ \text{cm}$). Vật sáng $AB$ cao $5\ \text{cm}$ đặt vuông góc với trục chính, $A$ nằm trên trục chính và cách thấu kính $40\ \text{cm}$.</p>
<p>a) Dựng ảnh $A'B'$ (vẽ phác, không cần đúng tỉ lệ). Ảnh nằm cùng phía hay khác phía vật?</p>
<p>b) Tính khoảng cách từ ảnh đến thấu kính và chiều cao của ảnh.</p>
<p>c) Tính khoảng cách giữa vật và ảnh.</p>""",
  r"""<p>a) Tia từ $B$ song song trục chính tới thấu kính ở $I$, tia ló loe ra như xuất phát từ $F'$ (nằm cùng phía vật); tia qua $O$ truyền thẳng.</p>
<p>Đường kéo dài của tia ló thứ nhất (nét đứt, qua $F'$) cắt tia qua $O$ tại $B'$: ảnh ảo, cùng phía vật, cùng chiều vật, nằm trong khoảng $OF'$.</p>
<p>b) $\dfrac1{d'}=\dfrac1f-\dfrac1d=-\dfrac1{10}-\dfrac1{40}=-\dfrac5{40}=-\dfrac18$ nên $d'=-8\ \text{cm}$.</p>
<p>$d'\lt0$: ảnh ảo, cách thấu kính $8\ \text{cm}$.</p>
<p>$h'=h\cdot\dfrac{|d'|}{d}=5\cdot\dfrac{8}{40}=1\ \text{cm}$.</p>
<p>c) Ảnh ảo nằm cùng phía vật nên $L=d-|d'|=40-8=32\ \text{cm}$.</p>
<p>Đáp số: ảnh ảo cách thấu kính $8\ \text{cm}$, cao $1\ \text{cm}$; vật–ảnh $32\ \text{cm}$.</p>
<p>Lỗi hay gặp: quên $f=-10$ nên tính ra $d'=\dfrac{40}{3}\ \text{cm}$ (ảnh thật — vô lí với thấu kính phân kì); cộng $d+|d'|=48\ \text{cm}$ cho ảnh ảo.</p>"""),

 # ── Bài 3 · Trung bình: kính lúp mắt tốt
 ("Trung bình", r"""<p>Một kính lúp là thấu kính hội tụ có tiêu cự $4\ \text{cm}$. Một học sinh mắt tốt (điểm cực cận cách mắt $25\ \text{cm}$, điểm cực viễn ở vô cực) dùng kính để quan sát một con kiến nhỏ; kính đặt sát mắt nên coi khoảng cách từ ảnh tới mắt bằng khoảng cách từ ảnh tới kính.</p>
<p>a) Trên vành kính phải ghi số bội giác bao nhiêu? (dùng $G=\dfrac{25}{f}$, $f$ tính bằng cm)</p>
<p>b) Mắt chỉ nhìn rõ ảnh ảo nằm trong khoảng từ điểm cực cận tới điểm cực viễn. Hỏi phải đặt con kiến trong khoảng nào trước kính?</p>
<p>c) Con kiến dài $0{,}5\ \text{mm}$. Khi ngắm chừng ở điểm cực cận (ảnh ảo hiện ở điểm cực cận), ảnh của nó dài bao nhiêu milimét?</p>""",
  r"""<p>a) $G=\dfrac{25}{f}=\dfrac{25}{4}=6{,}25$: vành kính ghi $6{,}25\times$.</p>
<p>b) Ngắm chừng ở điểm cực cận: ảnh ảo tại $C_c$ nên $d'=-25\ \text{cm}$.</p>
<p>$\dfrac1d=\dfrac1f-\dfrac1{d'}=\dfrac14+\dfrac1{25}=\dfrac{29}{100}$ nên $d=\dfrac{100}{29}\approx3{,}45\ \text{cm}$.</p>
<p>Ngắm chừng ở vô cực: ảnh ở rất xa, tia ló song song, vật đặt tại tiêu điểm: $d=f=4\ \text{cm}$.</p>
<p>Vậy phải đặt con kiến cách kính từ $3{,}45\ \text{cm}$ đến $4\ \text{cm}$ (chỉ xê dịch được khoảng $0{,}55\ \text{cm}$).</p>
<p>c) $\dfrac{h'}{h}=\dfrac{|d'|}{d}=\dfrac{25}{100/29}=7{,}25$ nên $h'=0{,}5\cdot7{,}25=3{,}625\ \text{mm}\approx3{,}6\ \text{mm}$.</p>
<p>Đáp số: $6{,}25\times$; $3{,}45\ \text{cm}\le d\le4\ \text{cm}$; ảnh dài $\approx3{,}6\ \text{mm}$.</p>
<p>Lỗi hay gặp: lấy $\dfrac{h'}{h}=G=6{,}25$ khi ngắm chừng ở điểm cực cận — số bội giác ghi trên kính ứng với ngắm chừng ở vô cực, không phải tỉ số chiều cao ảnh–vật.</p>"""),

 # ── Bài 4 · Trung bình: chứng minh tính chất ảnh qua thấu kính phân kì
 ("Trung bình", r"""<p>Chứng minh (bằng chữ, không dùng số cụ thể): một vật thật đặt ở vị trí bất kì trước thấu kính phân kì luôn cho ảnh ảo, cùng chiều, nhỏ hơn vật và nằm trong khoảng từ tiêu điểm ảnh $F'$ đến thấu kính.</p>
<p><em>Gợi ý:</em> đặt $f=-|f|$ rồi giải $d'$ theo $d$ và $|f|$.</p>""",
  r"""<p>Với $f=-|f|$: $\dfrac1{d'}=\dfrac1f-\dfrac1d=-\dfrac1{|f|}-\dfrac1d=-\dfrac{d+|f|}{d\,|f|}$.</p>
<p>Suy ra $d'=-\dfrac{d\,|f|}{d+|f|}$. Vì $d\gt0$, $|f|\gt0$ nên $d'\lt0$ với mọi $d$: ảnh luôn ảo, cùng phía vật, cùng chiều vật.</p>
<p>Khoảng cách ảnh–thấu kính $|d'|=\dfrac{d\,|f|}{d+|f|}$.</p>
<p>Vì $d+|f|\gt d$ nên $|d'|\lt|f|$: ảnh nằm giữa $F'$ và thấu kính.</p>
<p>Vì $d+|f|\gt|f|$ nên $|d'|\lt d$: ảnh gần thấu kính hơn vật.</p>
<p>Tỉ số chiều cao $\dfrac{h'}{h}=\dfrac{|d'|}{d}=\dfrac{|f|}{d+|f|}\lt1$: ảnh nhỏ hơn vật.</p>
<p>Nhận xét: khi $d$ rất lớn, $|d'|$ tiến tới $|f|$ (ảnh tiến về $F'$); khi $d$ rất nhỏ, $|d'|$ xấp xỉ $d$ và ảnh xấp xỉ bằng vật.</p>
<p>Lỗi hay gặp: chỉ thử vài số rồi kết luận "luôn luôn" — thử số chỉ minh hoạ, không phải chứng minh.</p>"""),

 # ── Bài 5 · Trung bình: điểm sáng trên trục chính
 ("Trung bình", r"""<p>Một điểm sáng $S$ nằm trên trục chính của thấu kính hội tụ tiêu cự $10\ \text{cm}$, cách thấu kính $25\ \text{cm}$.</p>
<p>a) Ba tia đặc biệt quen thuộc đều trùng với trục chính nên không dùng được. Nêu cách dựng ảnh $S'$ của $S$ bằng một tia bất kì, rồi dựng (vẽ lại hình, có thể dùng tỉ lệ 1 cm trên hình ứng với 5 cm thật).</p>
<p>b) Tính khoảng cách từ $S'$ đến thấu kính. $S'$ là ảnh thật hay ảo?</p>"""
  + fig_tl5(False),
  r"""<p>a) Từ $S$ vẽ tia bất kì $SI$ tới thấu kính ở $I$.</p>
<p>Vẽ trục phụ: đường thẳng qua $O$ song song với $SI$.</p>
<p>Vẽ tiêu diện ảnh: đường vuông góc trục chính tại $F'$; trục phụ cắt tiêu diện tại tiêu điểm phụ $F'_1$.</p>
<p>Chùm tia song song với trục phụ hội tụ tại $F'_1$, nên tia ló từ $I$ đi qua $F'_1$; tia ló cắt trục chính tại $S'$.</p>"""
  + fig_tl5(True) +
  r"""<p>b) $\dfrac1{d'}=\dfrac1f-\dfrac1d=\dfrac1{10}-\dfrac1{25}=\dfrac3{50}$ nên $d'=\dfrac{50}3\approx16{,}67\ \text{cm}$.</p>
<p>$d'\gt0$: $S'$ là ảnh thật, nằm khác phía $S$, cách thấu kính khoảng $16{,}67\ \text{cm}$.</p>
<p>Kiểm bằng hình: chọn $I$ cao $4\ \text{cm}$; trục phụ có độ dốc $\dfrac4{25}$ nên $F'_1$ cao $\dfrac4{25}\cdot10=1{,}6\ \text{cm}$; tia $IF'_1$ hạ $2{,}4\ \text{cm}$ sau mỗi $10\ \text{cm}$, cắt trục chính sau $\dfrac{4}{2{,}4}\cdot10=\dfrac{50}3\ \text{cm}$ ✓.</p>
<p>Lỗi hay gặp: dùng "tia qua quang tâm" cho $S$ — tia đó chính là trục chính, không cho giao điểm.</p>"""),

 # ── Bài 6 · Khó: tìm vị trí đặt thấu kính khi biết vật–màn
 ("Khó", r"""<p>Một vật sáng $AB$ và một màn ảnh đặt cố định, song song với nhau, cách nhau $L=81\ \text{cm}$. Đặt một thấu kính hội tụ tiêu cự $18\ \text{cm}$ trong khoảng giữa vật và màn, trục chính vuông góc với màn và đi qua $A$.</p>
<p>a) Phải đặt thấu kính cách vật bao nhiêu để thu được ảnh rõ nét trên màn? Mỗi vị trí, ảnh lớn hay nhỏ hơn vật bao nhiêu lần?</p>
<p>b) Giữ thấu kính đó, đưa màn lại gần vật. Khoảng cách vật–màn nhỏ nhất bằng bao nhiêu thì còn hứng được ảnh rõ nét? Giải thích vì sao nhỏ hơn giá trị đó thì không làm được.</p>""",
  r"""<p>a) Ảnh hứng được trên màn là ảnh thật: $d'\gt0$ và $d+d'=L$, tức $d'=L-d$.</p>
<p>Thay vào công thức: $\dfrac1f=\dfrac1d+\dfrac1{L-d}=\dfrac{L}{d(L-d)}$ nên $d^2-Ld+Lf=0$.</p>
<p>Với $L=81$, $f=18$: $d^2-81d+1458=0$; $\Delta=81^2-4\cdot1458=729=27^2$.</p>
<p>$d_1=\dfrac{81-27}2=27\ \text{cm}$ thì $d'_1=54\ \text{cm}$: ảnh lớn gấp $\dfrac{54}{27}=2$ lần vật.</p>
<p>$d_2=\dfrac{81+27}2=54\ \text{cm}$ thì $d'_2=27\ \text{cm}$: ảnh bằng $\dfrac{27}{54}=\dfrac12$ vật.</p>
<p>b) Phương trình $d^2-Ld+Lf=0$ có nghiệm khi $\Delta=L^2-4Lf\ge0$, tức $L\ge4f=72\ \text{cm}$.</p>
<p>Khi $L=72\ \text{cm}$: nghiệm kép $d=d'=36\ \text{cm}=2f$, ảnh bằng vật.</p>
<p>Khi $L\lt72\ \text{cm}$: $\Delta\lt0$, không có vị trí nào của thấu kính cho ảnh thật trên màn (ảnh thật luôn cách vật ít nhất $4f$).</p>
<p>Đáp số: $27\ \text{cm}$ (ảnh gấp 2) hoặc $54\ \text{cm}$ (ảnh bằng một nửa); $L_{\min}=72\ \text{cm}$.</p>
<p>Lỗi hay gặp: chỉ tìm một nghiệm; quên điều kiện $\Delta\ge0$.</p>"""),

 # ── Bài 7 · Khó: Bessel ngược — biết hai ảnh
 ("Khó", r"""<p>Một vật sáng $AB$ và một màn đặt cố định, cách nhau $72\ \text{cm}$. Dịch chuyển một thấu kính hội tụ trong khoảng giữa vật và màn (trục chính luôn vuông góc màn, đi qua $A$) thì thấy có hai vị trí của thấu kính cho ảnh rõ nét trên màn: một ảnh cao $9\ \text{cm}$, một ảnh cao $1\ \text{cm}$. Không đo được chiều cao của vật.</p>
<p>a) Chứng minh hai vị trí đó "đổi chỗ" cho nhau: $d$ ở vị trí này bằng $d'$ ở vị trí kia. Từ đó tính chiều cao của vật.</p>
<p>b) Tính tiêu cự của thấu kính và khoảng cách giữa hai vị trí của thấu kính.</p>
<p>c) Kiểm lại tiêu cự bằng công thức $f=\dfrac{L^2-\ell^2}{4L}$ ($\ell$ là khoảng cách hai vị trí).</p>""",
  r"""<p>a) Ảnh thật trên màn: $d+d'=L$ và $\dfrac1f=\dfrac1d+\dfrac1{d'}$. Hai phương trình này đối xứng giữa $d$ và $d'$: nếu cặp $(d;\,d')$ thoả thì cặp $(d';\,d)$ cũng thoả.</p>
<p>Vậy hai vị trí là $d_1=d$, $d_2=d'$ (và $d'_2=d$).</p>
<p>Tỉ số chiều cao: $\dfrac{h'_1}{h}=\dfrac{d'}{d}$, $\dfrac{h'_2}{h}=\dfrac{d}{d'}$, nhân lại: $h'_1h'_2=h^2$.</p>
<p>$h=\sqrt{9\cdot1}=3\ \text{cm}$.</p>
<p>b) Ở vị trí cho ảnh $9\ \text{cm}$: $\dfrac{d'}{d}=\dfrac93=3$, kết hợp $d+d'=72$: $d=18\ \text{cm}$, $d'=54\ \text{cm}$.</p>
<p>$f=\dfrac{dd'}{d+d'}=\dfrac{18\cdot54}{72}=13{,}5\ \text{cm}$.</p>
<p>Hai vị trí của thấu kính cách vật $18\ \text{cm}$ và $54\ \text{cm}$, cách nhau $\ell=54-18=36\ \text{cm}$.</p>
<p>c) $f=\dfrac{72^2-36^2}{4\cdot72}=\dfrac{5184-1296}{288}=13{,}5\ \text{cm}$ ✓; điều kiện $L=72\ge4f=54$ thoả.</p>
<p>Đáp số: $h=3\ \text{cm}$; $f=13{,}5\ \text{cm}$; $\ell=36\ \text{cm}$.</p>
<p>Lỗi hay gặp: lấy trung bình cộng $\dfrac{9+1}2=5\ \text{cm}$ làm chiều cao vật — đúng là trung bình nhân.</p>"""),

 # ── Bài 8 · Nâng cao: hệ hai thấu kính hội tụ
 ("Nâng cao", r"""<p>Hai thấu kính hội tụ $L_1$ (tiêu cự $f_1=10\ \text{cm}$) và $L_2$ (tiêu cự $f_2=15\ \text{cm}$) đặt đồng trục, cách nhau $a=40\ \text{cm}$. Vật sáng $AB$ cao $1\ \text{cm}$ đặt vuông góc với trục chính, $A$ trên trục chính, trước $L_1$ (ở phía không có $L_2$) và cách $L_1$ $15\ \text{cm}$. Ánh sáng đi từ vật qua $L_1$ rồi qua $L_2$.</p>
<p>a) Xác định ảnh $A_1B_1$ của vật qua $L_1$ (vị trí, tính chất, chiều cao).</p>
<p>b) Xác định ảnh cuối cùng $A_2B_2$ qua hệ: vị trí so với $L_2$ và so với $L_1$, tính chất, chiều so với vật, chiều cao.</p>
<p>c) Mắt đặt sau $L_2$ có nhìn thấy ảnh cuối không? Có hứng được ảnh cuối trên màn không?</p>""",
  r"""<p>Sơ đồ: $AB\xrightarrow{L_1}A_1B_1\xrightarrow{L_2}A_2B_2$; ảnh qua $L_1$ là vật của $L_2$.</p>
<p>a) $\dfrac1{d'_1}=\dfrac1{10}-\dfrac1{15}=\dfrac1{30}$ nên $d'_1=30\ \text{cm}$: $A_1B_1$ là ảnh thật, sau $L_1$ $30\ \text{cm}$, ngược chiều vật.</p>
<p>$h_1=1\cdot\dfrac{30}{15}=2\ \text{cm}$.</p>
<p>b) $A_1B_1$ nằm giữa hai thấu kính, cách $L_2$: $d_2=a-d'_1=40-30=10\ \text{cm}$ (vật thật đối với $L_2$).</p>
<p>$d_2=10\lt f_2=15$ nên $L_2$ đóng vai kính lúp: $\dfrac1{d'_2}=\dfrac1{15}-\dfrac1{10}=-\dfrac1{30}$, $d'_2=-30\ \text{cm}$.</p>
<p>$A_2B_2$ là ảnh ảo, cùng phía với $A_1B_1$ (phía $L_1$), cách $L_2$ $30\ \text{cm}$, tức cách $L_1$ $40-30=10\ \text{cm}$ — nằm giữa hai thấu kính, phía sau $L_1$.</p>
<p>Số phóng đại từng thấu kính $k=-\dfrac{d'}{d}$ ($k\gt0$: cùng chiều, $k\lt0$: ngược chiều): $k_1=-\dfrac{30}{15}=-2$, $k_2=-\dfrac{-30}{10}=3$.</p>
<p>Số phóng đại của hệ $k=k_1k_2=-6$: $k\lt0$ nên $A_2B_2$ ngược chiều vật $AB$, cao $h_2=|k|\,h=6\cdot1=6\ \text{cm}$.</p>
<p>c) Mắt sau $L_2$ đón chùm tia ló loe ra như xuất phát từ $A_2B_2$ nên nhìn thấy ảnh. Ảnh ảo nên không hứng được trên màn.</p>
<p>Đáp số: $A_1B_1$ thật, sau $L_1$ $30\ \text{cm}$, cao $2\ \text{cm}$; $A_2B_2$ ảo, cách $L_2$ $30\ \text{cm}$ (cách $L_1$ $10\ \text{cm}$, giữa hai thấu kính), ngược chiều vật, cao $6\ \text{cm}$.</p>
<p>Lỗi hay gặp: lấy $d_2=a=40\ \text{cm}$; kết luận ảnh cuối cùng chiều vật vì "ảnh ảo thì cùng chiều" — chiều của ảnh cuối so với vật xét bằng dấu của $k=k_1k_2$, không xét riêng thấu kính cuối.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + QUY_UOC + "".join(parts))


def anh(f, d):
    return 1 / (1 / F(f) - 1 / F(d))


def kiem_so():
    # Bài 1
    dp = anh(6, 9); assert dp == 18 and F(1) * dp / 9 == 2 and 9 + dp == 27
    # Bài 2
    dp = anh(-10, 40); assert dp == -8 and 5 * F(8, 40) == 1 and 40 - 8 == 32
    assert anh(10, 40) == F(40, 3) and 40 + 8 == 48                    # hai bẫy
    # Bài 3
    assert F(25, 4) == F(625, 100)
    dcc = 1 / (F(1, 4) + F(1, 25)); assert dcc == F(100, 29) and round(float(dcc), 2) == 3.45
    assert anh(4, dcc) == -25 and round(4 - float(dcc), 2) == 0.55
    k = 25 / dcc; assert k == F(29, 4) and k * F(1, 2) == F(29, 8)
    # Bài 4 (kiểm vài giá trị cho công thức chữ)
    for fa in (5, 12, 30):
        for d in (1, 7, 20, 100):
            dp = anh(-fa, d)
            assert dp == -F(d * fa, d + fa) and -dp < fa and -dp < d and -dp / d == F(fa, d + fa) < 1
    # Bài 5
    dp = anh(10, 25); assert dp == F(50, 3) and round(float(dp), 2) == 16.67
    yF1 = F(4, 25) * 10; assert yF1 == F(8, 5)
    xS = (4 / (4 - yF1)) * 10; assert xS == F(50, 3)                    # tia I(0;4)–F'1(10;1,6) cắt trục
    # Bài 6
    L, f = 81, 18
    D = L * L - 4 * L * f; assert D == 729 and isqrt(D) ** 2 == D
    d1, d2 = (L - 27) // 2, (L + 27) // 2; assert (d1, d2) == (27, 54)
    assert anh(f, d1) == 54 and anh(f, d2) == 27 and 4 * f == 72 and anh(18, 36) == 36
    # Bài 7
    L, H1, H2 = 72, 9, 1
    h = isqrt(H1 * H2); assert h * h == H1 * H2 == 9 and h == 3
    d = F(L, 1 + F(H1, h)); dp = L - d; assert (d, dp) == (18, 54)
    f = d * dp / L; assert f == F(27, 2) and anh(f, d) == dp and anh(f, dp) == d
    ell = dp - d; assert ell == 36 and F(L * L - ell * ell, 4 * L) == f and L >= 4 * f
    assert dp / d * h == 9 and d / dp * h == 1
    # Bài 8
    d1p = anh(10, 15); assert d1p == 30 and 1 * d1p / 15 == 2
    d2 = 40 - d1p; assert d2 == 10 < 15
    d2p = anh(15, d2); assert d2p == -30 and 40 + d2p == 10 and 0 < 40 + d2p < 40
    k1, k2 = -d1p / 15, -d2p / d2; assert k1 == -2 and k2 == 3 and k1 * k2 == -6
    print("kiểm số liệu tự luận 156: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
