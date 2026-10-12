"""Bài tập mẫu Chuyên đề 03 "Điện trở, định luật Ohm" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 159.
Nguồn: content/hsg9/cd03-dien-tro-dinh-luat-ohm/nguon.md (mục C dạng bài, D ví dụ, E tự luyện, G nâng cao; đã tự giải lại từng bài bằng Python).
YCCĐ "bài tương tự": YCCĐ của bài KHTN 9 id 89 (Điện trở. Định luật Ohm) và L11 b23 (id 42) — xem trường `topic` từng dạng.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-159.py   (idempotent; không ghi DB)

Điểm sửa / chưa chắc so với nguồn docx:
 - Dạng 7 (nguồn): ghi "U = 2,4 V ± 0,06 V" trong khi mục B2.7 dạy làm tròn sai số về 1 chữ số (± 0,1 V) — hai chỗ không thống nhất; ở đây ghi theo sai số tính được và nêu rõ δ.
 - G4: nguồn ghi giảm 1,65 % (làm tròn 0,1967 trước khi trừ); tính đúng 1,64 %.
 - E4: nguồn 573 m (π = 3,14); π đúng cho 572 m — ghi ≈ 572 m.
 - G2 b: nguồn hỏi "thực hiện được không" nhưng câu trả lời luôn là được (0,3–0,6 A nằm trong 0,3–0,8 A); đổi thành hai cách hạ I_min xuống 0,2 A.
 - D6 (nguồn): tính số vòng dây bằng π·D, bỏ qua đường kính dây (thực tế vòng dài π(D + d)); giữ π·D và nói rõ là gần đúng. Câu c (nguồn) ra đúng R_max nên suy biến — đổi số.
 - A2 (nguồn) khẳng định ampe kế/vôn kế lí tưởng "không có trong YCCĐ lớp 9": chưa kiểm được trong chương trình → không dùng làm căn cứ.
Mọi đáp số được tự tính lại ở hàm kiem_so() cuối file (assert) trước khi ghi."""
import json, math, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
sys.path.insert(0, HERE)
from dung import *
from hinh_159 import R, circ, txt, tick, wire, resistor, battery, meter, hwire, vwire, graph_axes, mach_bien_tro, GREY

J = os.path.join(HERE, "159.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
FILL_B, FILL_O = "rgba(56,189,248,.18)", "rgba(251,146,60,.18)"


# ═════════════ HÌNH ═════════════
def flow(pts, dur, col=GRN, n=40, r=5):
    """Hạt tải điện chạy MỘT lần dọc đường gấp khúc pts với tốc độ đều (lấy mẫu theo độ dài cung)."""
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; tot = sum(lens)
    xs, ys = [], []
    for k in range(n + 1):
        d = tot * k / n; j = 0
        while j < len(segs) - 1 and d > lens[j]:
            d -= lens[j]; j += 1
        t = d / lens[j] if lens[j] else 0
        xs.append(segs[j][0][0] + t * (segs[j][1][0] - segs[j][0][0])); ys.append(segs[j][0][1] + t * (segs[j][1][1] - segs[j][0][1]))
    return (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{r}" fill="{col}" stroke="currentColor" stroke-width="1.3">'
            f'{smil("cx", xs, dur)}{smil("cy", ys, dur)}</circle>')


def d1(kk):
    p = f"d1{kk}"; b = defs(p)
    b += R(30, 56, 250, 26, BLUE, 2.6, FILL_B, 8) + txt(292, 74, "nhôm", BLUE, 14)
    b += dim(p, "b", 32, 40, 278, 40, "l = 200 m", 155, 30, "middle")
    b += txt(30, 106, "S = 0,5 mm²", "currentColor", 14) + txt(200, 106, "R = ?" if kk == 0 else "R = ρl/S", RED, 15)
    b += R(30, 128, 250, 26, ORG, 2.6, "none", 8, "6 4") + txt(292, 146, "đồng", ORG, 14)
    b += txt(30, 178, "S = ?", "currentColor", 14) + txt(200, 178, "cùng l, cùng R" if kk == 0 else "S ∝ ρ khi cùng l, R", RED, 14)
    if kk == 0:
        b += flow([(40, 69), (270, 69)], 3.5, BLUE) + flow([(40, 141), (270, 141)], 3.5, ORG)
    return fig(f"c159-1-{kk}", "0 0 420 190", "Dây nhôm dài 200 mét tiết diện 0,5 milimét vuông và dây đồng cùng chiều dài cùng điện trở",
               b, ("Mô phỏng: hạt tải điện chạy dọc hai dây có cùng $l$ và cùng $R$ (khác vật liệu). " if kk == 0 else "Dữ kiện: dây nhôm và dây đồng cùng $l$, cùng $R$, khác vật liệu. ") + NOTE)


def d2(kk):
    p = f"d2{kk}"; b = defs(p)
    b += txt(30, 26, "Dây R = 90 Ω", "currentColor", 14) + R(30, 36, 360, 18, "currentColor", 2.4, "none", 4)
    for x in (150, 270):
        b += seg(x, 28, x, 62, ORG, 2, "5 4")
    b += txt(210, 80, "cắt 3 đoạn bằng nhau", ORG, 13, "middle")
    ys = (110, 140, 170)
    b += seg(60, ys[0], 60, ys[-1], "currentColor", 2) + seg(360, ys[0], 360, ys[-1], "currentColor", 2)
    for y in ys:
        b += seg(60, y, 135, y, "currentColor", 2) + R(135, y - 8, 90, 16, "currentColor", 2.4) + seg(225, y, 360, y, "currentColor", 2)
        b += txt(180, y + 4, "R₀ = ?" if kk == 0 else "R₀", "currentColor", 12, "middle", "400")
    b += circ(60, 140, 4, "currentColor", 2, "currentColor") + circ(360, 140, 4, "currentColor", 2, "currentColor")
    b += txt(46, 144, "A", "currentColor", 13, "end") + txt(374, 144, "B", "currentColor", 13, "start")
    b += txt(290, 140 - 14, "U_{AB} = 6 V", RED, 13, "middle")
    if kk == 0:
        b += "".join(flow([(60, y), (360, y)], 3.5, GRN) for y in ys)
    return fig(f"c159-2-{kk}", "0 0 420 190", "Dây điện trở 90 ôm cắt thành ba đoạn bằng nhau rồi ghép song song vào hiệu điện thế 6 vôn",
               b, ("Mô phỏng: dòng điện chia đều cho ba nhánh giống nhau giữa $A$ và $B$. " if kk == 0 else "Dữ kiện: ba đoạn bằng nhau ghép song song giữa $A$ và $B$. ") + NOTE)


def stretch_geom():
    """(l, d) tương đối: ban đầu, sau kéo thêm 50 %, sau khi đường kính giảm một nửa (V không đổi)."""
    l0, d0 = 60.0, 36.0
    l1, d1_ = 1.5 * l0, d0 / math.sqrt(1.5)
    l2, d2_ = 4 * l1, d1_ / 2
    assert abs(l1 * d1_ ** 2 - l0 * d0 ** 2) < 1e-6 and abs(l2 * d2_ ** 2 - l0 * d0 ** 2) < 1e-6
    return [(l0, d0), (l1, d1_), (l2, d2_)]


def d3(kk):
    p = f"d3{kk}"; b = defs(p); G = stretch_geom()
    if kk == 0:
        cy = 100
        vw = ";".join(f"{l:.1f}" for l, _ in G); vh = ";".join(f"{d:.1f}" for _, d in G); vy = ";".join(f"{cy - d / 2:.1f}" for _, d in G)
        b += txt(16, 26, "Dây constantan R₁ = 20 Ω", "currentColor", 14) + txt(404, 26, "R₃ = ?", RED, 14, "end")
        b += (f'<rect x="30" y="{cy - G[0][1] / 2:.1f}" width="{G[0][0]:.1f}" height="{G[0][1]:.1f}" rx="8" fill="{FILL_O}" stroke="{ORG}" stroke-width="2.6">'
              f'<animate attributeName="width" values="{vw}" dur="5s" begin="indefinite" fill="freeze"/>'
              f'<animate attributeName="height" values="{vh}" dur="5s" begin="indefinite" fill="freeze"/>'
              f'<animate attributeName="y" values="{vy}" dur="5s" begin="indefinite" fill="freeze"/></rect>')
        b += txt(30, 160, "Lần 1: dài thêm 50 %", "currentColor", 13, "start", "400") + txt(30, 180, "Lần 2: đường kính còn một nửa so với lúc đó", "currentColor", 13, "start", "400")
        return fig("c159-3-0", "0 0 420 196", "Dây constantan được kéo dài thêm 50 phần trăm rồi kéo tiếp cho đường kính giảm một nửa",
                   b, "Mô phỏng: dây bị kéo dãn hai lần liên tiếp, thể tích không đổi, nên dài ra thì mảnh đi. " + NOTE)
    names = ["R₁ = 20 Ω", "R₂ = ?", "R₃ = ?"]; lab = ["ban đầu", "kéo lần 1", "kéo lần 2"]
    for i, (l, d) in enumerate(G):
        y = 40 + 56 * i
        b += R(30, y - d / 2, l, d, ORG, 2.6, FILL_O, 6) + txt(30, y - 24, lab[i], "currentColor", 13, "start", "400") + txt(390, y - 22, names[i], RED, 14, "end")
    return fig("c159-3-2", "0 0 420 190", "Ba trạng thái của dây: ban đầu, sau lần kéo thứ nhất, sau lần kéo thứ hai; dây dài ra thì mảnh đi",
               b, "Dữ kiện: mỗi lần kéo, thể tích $V=S\\cdot l$ không đổi. " + NOTE)


def d4(kk):
    p = f"d4{kk}"; b = defs(p)
    ox, oy, kx, ky = 56, 176, 300.0, 28.0
    b += graph_axes(ox, oy, 190, 150, "I (A)", "U (V)", (0.25, 0.5), (1.5, 3, 4.5), kx, ky)
    A, B = (0.5, 3.0), (0.5, 4.5)
    b += seg(ox, oy, ox + kx * 0.5, oy - ky * 3.0, BLUE, 2.8) + seg(ox, oy, ox + kx * 0.5, oy - ky * 4.5, ORG, 2.8)
    b += txt(ox + kx * 0.5 + 8, oy - ky * 3.0 + 5, "(1)", BLUE, 14) + txt(ox + kx * 0.5 + 8, oy - ky * 4.5 + 5, "(2)", ORG, 14)
    if kk == 0:
        n = 6
        for (xx, yy), col in ((A, BLUE), (B, ORG)):
            xs = [ox + kx * xx * i / (n - 1) for i in range(n)]; ys = [oy - ky * yy * i / (n - 1) for i in range(n)]
            b += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="5.5" fill="{col}" stroke="currentColor" stroke-width="1.4">'
                  f'{smil("cx", xs, 3.5)}{smil("cy", ys, 3.5)}</circle>')
        return fig("c159-4-0", "0 0 420 214", "Đồ thị hiệu điện thế theo cường độ dòng điện của hai vật dẫn đi qua gốc toạ độ",
                   b, "Mô phỏng: điểm đo trượt dọc từng đường khi cường độ dòng điện tăng dần từ $0$ đến $0{,}5\\ \\text{A}$. " + NOTE)
    for (xx, yy), col, nm in ((A, BLUE, "A"), (B, ORG, "B")):
        b += seg(ox + kx * xx, oy, ox + kx * xx, oy - ky * yy, GREY, 1.2, "4 4", .7) + seg(ox, oy - ky * yy, ox + kx * xx, oy - ky * yy, GREY, 1.2, "4 4", .7)
        b += circ(ox + kx * xx, oy - ky * yy, 4.5, col, 2, col) + txt(ox + kx * xx - 8, oy - ky * yy - 8, nm, col, 14, "end")
    return fig("c159-4-2", "0 0 420 214", "Đồ thị U theo I của hai vật dẫn với hai điểm A và B ứng với dòng điện 0,5 ampe",
               b, "Dữ kiện: trục hoành là $I$, trục tung là $U$. Hai điểm $A$, $B$ cùng $I=0{,}5\\ \\text{A}$. " + NOTE)


def d5(kk):
    L, Rr, T, Bt = 36, 344, 44, 128
    b = hwire(T, L, Rr, [(103, 157), (210, 290)]) + vwire(Rr, T, Bt) + hwire(Bt, L, Rr, [(178, 202)]) + vwire(L, T, Bt, [(74, 100)])
    b += battery(L, 87, "U = 24 V") + resistor(130, T) + txt(130, T - 18, "R = 30 Ω", "currentColor", 13, "middle")
    b += R(210, T - 8, 80, 16, "currentColor", 2.4) + txt(250, T - 32, "biến trở R_max = 50 Ω", ORG, 13, "middle")
    sl = seg(238, T + 18, 262, T - 20, ORG, 2.2) + chevron(262, T - 20, 24, -38, ORG, 2.2, 9)
    if kk == 0:
        b += (f'<g><animateTransform attributeName="transform" type="translate" values="-30 0;30 0" dur="4s" begin="indefinite" fill="freeze"/>{sl}</g>')
    else:
        b += sl
    b += meter(190, Bt, "A", RED) + txt(190, Bt + 30, "I = ?" if kk == 0 else "I = U/(R + R_b)", RED, 13, "middle")
    cap = ("Mô phỏng: con chạy của biến trở trượt từ đầu này sang đầu kia. " if kk == 0 else "Dữ kiện: biến trở nối tiếp với $R$; ampe kế lí tưởng. ") + NOTE
    return fig(f"c159-5-{kk}", "0 0 380 170", "Nguồn 24 vôn nối tiếp điện trở 30 ôm, biến trở 50 ôm có con chạy và ampe kế", b, cap)


def d6(kk):
    L, Rr, T, Bt = 30, 372, 44, 150
    b = hwire(T, L, Rr, [(80, 110), (163, 217), (273, 327)]) + vwire(Rr, T, Bt) + hwire(Bt, L, Rr) + vwire(L, T, Bt, [(84, 110)])
    b += battery(L, 97, "U = 12 V")
    b += meter(95, T, "A", RED) + txt(95, T - 20, "R_A = 0,5 Ω", RED, 13, "middle")
    b += resistor(190, T, "", 54) + txt(190, T - 18, "R₁ = 6 Ω", "currentColor", 13, "middle")
    b += resistor(300, T, "", 54) + txt(300, T - 18, "R₂ = 18 Ω", "currentColor", 13, "middle")
    b += wire((163, T), (163, 104), (178, 104), c=BLUE) + wire((202, 104), (217, 104), (217, T), c=BLUE)
    b += meter(190, 104, "V", BLUE) + txt(190, 136, "R_V = ?" if kk == 0 else "R_V", BLUE, 13, "middle")
    if kk == 0:
        b += flow([(30, 44), (372, 44), (372, 150), (30, 150), (30, 44)], 6, GRN)
    cap = ("Mô phỏng: dòng điện chạy một vòng quanh mạch, qua cả ampe kế và các điện trở. " if kk == 0 else "Dữ kiện: ampe kế nối tiếp, vôn kế (điện trở $R_V$) song song với $R_1$. ") + NOTE
    return fig(f"c159-6-{kk}", "0 0 400 170", "Nguồn 12 vôn, ampe kế có điện trở 0,5 ôm nối tiếp R1 và R2, vôn kế mắc song song với R1", b, cap)


BUILD = [d1, d2, d3, d4, d5, d6]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
T_KT = "Điện trở phụ thuộc kích thước và vật liệu dây dẫn"
T_OHM = "Định luật Ohm cho một điện trở"
T_VA = "Đường đặc trưng vôn – ampe"
DANG = [
 dict(label="Dạng 1 · Dễ · Điện trở dây dẫn R = ρl/S: đổi đơn vị, so sánh hai vật liệu, đường kính dây", topic=T_KT,
      problem_html=r"""<p>Một dây nhôm dài $l=200\ \text{m}$, tiết diện $S=0{,}5\ \text{mm}^2$. Điện trở suất của nhôm là $2{,}8\cdot10^{-8}\ \Omega\cdot\text{m}$, của đồng là $1{,}7\cdot10^{-8}\ \Omega\cdot\text{m}$.</p><ol type="a"><li>Tính điện trở của dây nhôm.</li><li>Thay bằng dây đồng có cùng chiều dài và cùng điện trở. Tính tiết diện của dây đồng.</li><li>Dây đồng đó có tiết diện tròn. Tính đường kính của nó.</li><li>Đặt hiệu điện thế $5{,}6\ \text{V}$ vào hai đầu dây nhôm. Tính cường độ dòng điện qua dây.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Cắt dây thành nhiều đoạn bằng nhau rồi ghép nối tiếp hoặc song song", topic=T_KT,
      problem_html=r"""<p>Một dây dẫn đồng chất, tiết diện đều có điện trở $R=90\ \Omega$ được cắt thành $3$ đoạn bằng nhau.</p><ol type="a"><li>Tính điện trở của mỗi đoạn.</li><li>Ghép $3$ đoạn đó song song với nhau. Tính điện trở tương đương của bộ.</li><li>Nối bộ vào nguồn $U=6\ \text{V}$. Tính cường độ dòng điện qua mạch chính và qua mỗi đoạn.</li><li>Từ dây $90\ \Omega$ ban đầu, phải cắt thành bao nhiêu đoạn bằng nhau rồi ghép song song để điện trở tương đương bằng $0{,}9\ \Omega$?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Kéo dãn dây dẫn, thể tích không đổi: R tỉ lệ với bình phương chiều dài", topic=T_KT,
      problem_html=r"""<p>Một dây constantan tiết diện đều có điện trở $R_1=20\ \Omega$. Coi thể tích dây không đổi khi kéo.</p><ol type="a"><li>Kéo dây cho chiều dài tăng thêm $50\%$. Tính điện trở $R_2$ của dây sau khi kéo.</li><li>Từ dây ở câu a, kéo tiếp cho đường kính của dây giảm còn một nửa so với lúc đó. Tính điện trở $R_3$ sau lần kéo thứ hai.</li><li>Một khối đồng khối lượng $178\ \text{g}$ (khối lượng riêng $8900\ \text{kg/m}^3$) được kéo thành sợi tiết diện đều $S=0{,}5\ \text{mm}^2$. Tính chiều dài sợi và điện trở của nó, biết điện trở suất của đồng là $1{,}7\cdot10^{-8}\ \Omega\cdot\text{m}$.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Đọc đồ thị U–I của hai vật dẫn: điện trở, so sánh độ dốc, ghép nối tiếp – song song", topic=T_VA,
      problem_html=r"""<p>Trên cùng một hệ trục (trục hoành là $I$ tính bằng $\text{A}$, trục tung là $U$ tính bằng $\text{V}$), đồ thị $U$–$I$ của vật dẫn $(1)$ là đường thẳng đi qua gốc toạ độ và điểm $A(0{,}5\ \text{A};\,3{,}0\ \text{V})$. Đồ thị của vật dẫn $(2)$ là đường thẳng đi qua gốc toạ độ và điểm $B(0{,}5\ \text{A};\,4{,}5\ \text{V})$.</p><ol type="a"><li>Tính điện trở của mỗi vật dẫn.</li><li>Đường nào dốc hơn? Vì sao?</li><li>Mắc hai vật dẫn song song vào nguồn $4{,}5\ \text{V}$. Tính cường độ dòng điện qua mạch chính.</li><li>Mắc hai vật dẫn nối tiếp vào nguồn $6\ \text{V}$. Tính hiệu điện thế giữa hai đầu mỗi vật dẫn.</li><li>Vẽ lại đồ thị với trục hoành là $U$, trục tung là $I$. Độ dốc của đường ứng với vật dẫn $(1)$ bằng bao nhiêu?</li></ol>"""),
 dict(label="Dạng 5 · Trung bình · Biến trở mắc nối tiếp: khoảng dòng điều chỉnh, vị trí con chạy, quấn biến trở", topic=T_OHM,
      problem_html=r"""<p>Nguồn có hiệu điện thế không đổi $U=24\ \text{V}$. Một biến trở con chạy có điện trở lớn nhất $R_{max}=50\ \Omega$, chịu được dòng tối đa $1{,}5\ \text{A}$, mắc nối tiếp với điện trở $R=30\ \Omega$. Ampe kế coi là lí tưởng.</p><ol type="a"><li>Tính khoảng giá trị cường độ dòng điện có thể điều chỉnh được trong mạch.</li><li>Muốn dòng điện bằng $0{,}6\ \text{A}$ thì biến trở phải có giá trị bao nhiêu? Con chạy cách đầu đã mắc bao nhiêu phần trăm chiều dài cuộn dây (cuộn dây quấn đều)?</li><li>Biến trở được quấn bằng dây nicrom, điện trở suất $1{,}1\cdot10^{-6}\ \Omega\cdot\text{m}$, đường kính dây $0{,}4\ \text{mm}$, trên ống sứ đường kính $2\ \text{cm}$. Tính chiều dài dây và số vòng dây (coi mỗi vòng dài $\pi D$ với $D$ là đường kính ống sứ).</li></ol>"""),
 dict(label="Dạng 6 · Khó · Ampe kế và vôn kế có điện trở: số chỉ, độ lệch so với giá trị thật, sai số dụng cụ", topic=T_OHM,
      problem_html=r"""<p>Nguồn có hiệu điện thế không đổi $U=12\ \text{V}$. Ampe kế có điện trở $R_A=0{,}5\ \Omega$ mắc nối tiếp với $R_1=6\ \Omega$ và $R_2=18\ \Omega$. Vôn kế có điện trở $R_V=4000\ \Omega$ mắc song song với $R_1$.</p><ol type="a"><li>Tính số chỉ của ampe kế và của vôn kế.</li><li>Thay vôn kế bằng một vôn kế khác có $R_V=6\ \Omega$. Tính số chỉ của vôn kế đó và độ lệch (theo phần trăm) so với hiệu điện thế thật giữa hai đầu $R_1$ khi <em>không</em> mắc vôn kế.</li><li>Vôn kế $4000\ \Omega$ ở câu a có $30$ vạch chia đều, thang $0$–$6\ \text{V}$, cấp chính xác $1{,}0$. Tính độ chia nhỏ nhất, sai số tuyệt đối lớn nhất của phép đo và sai số tương đối của số chỉ ở câu a.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"dây nhôm dài $200$ m, tiết diện $0{,}5$ mm²"', r"$l=200$ m ; $S=0{,}5$ mm² ; $\rho_{Al}=2{,}8\cdot10^{-8}\ \Omega\cdot$m", r"$R=\rho\dfrac lS$ ; ⚠ đổi $1$ mm² $=10^{-6}$ m² rồi mới thay số, không trộn hai hệ đơn vị"),
  (r'"tính điện trở của dây nhôm" (câu a)', r"Cần $R$", r"$R=\dfrac{\rho l}{S}$"),
  (r'"dây đồng cùng chiều dài và cùng điện trở"', r"$l$ và $R$ như dây nhôm ; $\rho_{Cu}=1{,}7\cdot10^{-8}$", r"⚠ cùng $R$, cùng $l$ nên $S\propto\rho$ : $\dfrac{S_{Cu}}{S_{Al}}=\dfrac{\rho_{Cu}}{\rho_{Al}}$"),
  (r'"tiết diện tròn … đường kính"', r"Có $S_{Cu}$, cần $d$", r"$S=\dfrac{\pi d^2}{4}$ nên $d=\sqrt{\dfrac{4S}{\pi}}$ ; ⚠ $d$ là đường kính, không phải bán kính"),
  (r'"đặt hiệu điện thế $5{,}6$ V … cường độ dòng điện"', r"$U=5{,}6$ V ; $R$ ở câu a", r"Định luật Ohm $I=\dfrac UR$")],
 # Dạng 2
 [(r'"dây đồng chất, tiết diện đều, $R=90\ \Omega$"', r"$R=90\ \Omega$", r"$R=\rho\dfrac lS$ ; ⚠ cùng vật liệu, cùng $S$ thì $R\propto l$"),
  (r'"cắt thành $3$ đoạn bằng nhau"', r"$n=3$ ; mỗi đoạn dài $\dfrac l3$", r"$R_0=\dfrac Rn$ ; ⚠ chỉ đúng khi các đoạn <strong>bằng nhau</strong>"),
  (r'"ghép $3$ đoạn song song"', r"$3$ nhánh giống nhau", r"$\dfrac1{R_{td}}=\dfrac3{R_0}$ nên $R_{td}=\dfrac{R_0}{3}=\dfrac R{n^2}$"),
  (r'"nối vào nguồn $6$ V … dòng mạch chính và mỗi đoạn"', r"$U=6$ V chung cho cả ba nhánh", r"$I=\dfrac U{R_{td}}$ ; $I_0=\dfrac U{R_0}$ ; ⚠ song song thì $U$ bằng nhau"),
  (r'"điện trở tương đương bằng $0{,}9\ \Omega$ … bao nhiêu đoạn"', r"$R_{td}=0{,}9\ \Omega$ ; $R=90\ \Omega$ ; cần $n$", r"$R_{td}=\dfrac R{n^2}$ nên $n=\sqrt{R/R_{td}}$")],
 # Dạng 3
 [(r'"coi thể tích dây không đổi khi kéo"', r"$V=S_1l_1=S_2l_2$", r"⚠ kéo dãn thì $S$ <strong>có</strong> đổi : dài ra thì mảnh đi ; không được dùng $R\propto l$"),
  (r'"kéo cho chiều dài tăng thêm $50\%$" (câu a)', r"$l_2=1{,}5\,l_1$", r"$\dfrac{R_2}{R_1}=\left(\dfrac{l_2}{l_1}\right)^2$"),
  (r'"kéo tiếp … đường kính giảm còn một nửa so với lúc đó"', r"$d_3=\dfrac{d_2}2$", r"$S\propto d^2$ nên $S_3=\dfrac{S_2}4$, từ $V$ không đổi $l_3=4\,l_2$ ; ⚠ tính từ trạng thái ngay trước lần kéo"),
  (r'"khối đồng $178$ g, $D=8900$ kg/m³, tiết diện $0{,}5$ mm²"', r"$m=0{,}178$ kg ; $S=5\cdot10^{-7}$ m²", r"$V=\dfrac mD$ ; $V=S\,l$ nên $l=\dfrac VS$"),
  (r'"điện trở của nó"', r"$\rho=1{,}7\cdot10^{-8}\ \Omega\cdot$m", r"$R=\dfrac{\rho l}{S}$ ; ⚠ $S$ đổi ra m²")],
 # Dạng 4
 [(r'"đi qua gốc toạ độ"', r"$U\propto I$", r"⚠ đường thẳng qua gốc : vật dẫn tuân theo định luật Ohm, $R$ không đổi"),
  (r'"vật dẫn (1) qua $A(0{,}5$ A ; $3{,}0$ V$)$ ; (2) qua $B(0{,}5$ ; $4{,}5)$"', r"$A$ : $0{,}5$ A, $3{,}0$ V ; $B$ : $0{,}5$ A, $4{,}5$ V", r"Trục tung là $U$ nên độ dốc $=R=\dfrac UI$"),
  (r'"đường nào dốc hơn"', r"So hai điện trở", r"⚠ trên đồ thị $U$–$I$ đường dốc hơn có $R$ lớn hơn"),
  (r'"mắc song song vào $4{,}5$ V"', r"$U_1=U_2=4{,}5$ V", r"$R_{td}=\dfrac{R_1R_2}{R_1+R_2}$ ; $I=\dfrac U{R_{td}}$"),
  (r'"mắc nối tiếp vào $6$ V … hiệu điện thế hai đầu mỗi vật dẫn"', r"$I$ chung ; $U=6$ V", r"$R_{td}=R_1+R_2$ ; $U_i=I\,R_i$ ; ⚠ nối tiếp thì $I$ bằng nhau"),
  (r'"trục hoành là $U$, trục tung là $I$ … độ dốc"', r"Cần $\dfrac{\Delta I}{\Delta U}$", r"⚠ trên đồ thị $I$–$U$ độ dốc $=\dfrac1R$")],
 # Dạng 5
 [(r'"biến trở mắc nối tiếp với $R=30\ \Omega$"', r"$R=30\ \Omega$ ; $R_{max}=50\ \Omega$ ; $U=24$ V", r"$R_{mach}=R_b+R$ ; ⚠ biến trở nối tiếp, ampe kế lí tưởng không có điện trở"),
  (r'"khoảng giá trị cường độ dòng điện điều chỉnh được"', r"Hai đầu mút : $R_b=0$ và $R_b=R_{max}$", r"$I_{max}=\dfrac UR$ ; $I_{min}=\dfrac U{R_{max}+R}$"),
  (r'"chịu được dòng tối đa $1{,}5$ A"', r"$I_{dm}=1{,}5$ A", r"⚠ dòng trong mạch không được vượt $I_{dm}$ của biến trở"),
  (r'"dòng điện bằng $0{,}6$ A … giá trị biến trở"', r"$I_0=0{,}6$ A", r"$R_b=\dfrac U{I_0}-R$"),
  (r'"cách đầu đã mắc bao nhiêu phần trăm … quấn đều"', r"Cần $\dfrac{R_b}{R_{max}}$", r"⚠ cuộn dây quấn đều thì $R_b$ tỉ lệ với chiều dài phần dây có dòng đi qua"),
  (r'"nicrom, $d=0{,}4$ mm, ống sứ $D=2$ cm, $R_{max}=50\ \Omega$"', r"$\rho=1{,}1\cdot10^{-6}$ ; $d=4\cdot10^{-4}$ m ; $D=2\cdot10^{-2}$ m", r"$S=\dfrac{\pi d^2}4$ ; $l=\dfrac{R_{max}S}{\rho}$ ; $N=\dfrac l{\pi D}$")],
 # Dạng 6
 [(r'"ampe kế có điện trở $R_A=0{,}5\ \Omega$ mắc nối tiếp"', r"$R_A=0{,}5\ \Omega$", r"⚠ dụng cụ đo là một điện trở trong mạch : đưa $R_A$ vào $R_{mach}$"),
  (r'"vôn kế $R_V=4000\ \Omega$ song song với $R_1$"', r"$R_V=4000\ \Omega$ ; $R_1=6\ \Omega$", r"$R_P=\dfrac{R_1R_V}{R_1+R_V}$ ; ⚠ vôn kế song song làm điện trở đoạn đó nhỏ đi"),
  (r'"số chỉ của ampe kế và của vôn kế" (câu a)', r"Cần $I_A$ và $U_V$", r"$I_A=\dfrac U{R_P+R_2+R_A}$ ; $U_V=I_AR_P$"),
  (r'"thay vôn kế có $R_V=6\ \Omega$ … so với khi không mắc vôn kế"', r"$R_V=6\ \Omega$ ; giá trị thật : bỏ vôn kế", r"Giá trị thật $U_1=\dfrac{U\,R_1}{R_1+R_2+R_A}$ ; độ lệch $=\dfrac{U_1-U_V}{U_1}$"),
  (r'"$30$ vạch chia, thang $0$–$6$ V, cấp $1{,}0$"', r"$N=30$ ; $A_{max}=6$ V ; $x=1{,}0$", r"ĐCNN $=\dfrac{A_{max}}N$ ; $\Delta U=x\%\cdot A_{max}$ ; ⚠ lấy theo <strong>thang</strong>, không theo số chỉ"),
  (r'"sai số tương đối của số chỉ"', r"$U_{doc}$ ở câu a", r"$\delta=\dfrac{\Delta U}{U_{doc}}$")],
]

# ═════════════ LỜI GIẢI (mỗi bước một khối, mỗi công thức một dòng) ═════════════
R1 = [r"<strong>Khái niệm:</strong> điện trở của dây phụ thuộc vật liệu ($\rho$), chiều dài $l$, tiết diện $S$.",
      r"<strong>Công thức:</strong> $R=\dfrac{\rho l}{S}$ ; $S=\dfrac{\pi d^2}{4}$ ; $I=\dfrac UR$.",
      r"Cùng $l$ và cùng $R$ : $\dfrac{S_1}{S_2}=\dfrac{\rho_1}{\rho_2}$.",
      r"⚠ <strong>Điều kiện:</strong> đổi mọi đại lượng về một hệ ; $1\ \text{mm}^2=10^{-6}\ \text{m}^2$."]
R2 = [r"<strong>Khái niệm:</strong> cùng vật liệu, cùng tiết diện thì $R$ tỉ lệ với chiều dài.",
      r"<strong>Công thức:</strong> cắt $n$ đoạn bằng nhau : $R_0=\dfrac Rn$ ; $n$ nhánh song song : $R_{td}=\dfrac{R_0}n=\dfrac R{n^2}$.",
      r"Song song : $U$ bằng nhau, $I=I_1+I_2+\dots$ ; $I_0=\dfrac U{R_0}$.",
      r"⚠ <strong>Điều kiện:</strong> các đoạn phải <strong>bằng nhau</strong> thì mới có $R_0=R/n$."]
R3 = [r"<strong>Khái niệm:</strong> kéo dãn thì thể tích $V=S\,l$ không đổi : dài ra thì mảnh đi.",
      r"<strong>Công thức:</strong> $S_1l_1=S_2l_2$ ; $\dfrac{R_2}{R_1}=\left(\dfrac{l_2}{l_1}\right)^2$ ; đường kính giảm $k$ lần thì $R$ tăng $k^4$ lần.",
      r"$V=\dfrac mD$ ; $l=\dfrac VS$ ; $R=\dfrac{\rho l}{S}$.",
      r"⚠ <strong>Điều kiện:</strong> $R\propto l$ chỉ đúng khi $S$ không đổi ; mỗi lần kéo tính từ trạng thái ngay trước đó."]
R4 = [r"<strong>Khái niệm:</strong> đường thẳng qua gốc toạ độ : $U\propto I$, $R$ không đổi.",
      r"<strong>Công thức:</strong> đồ thị $U$–$I$ : độ dốc $=R=\dfrac{\Delta U}{\Delta I}$ ; đồ thị $I$–$U$ : độ dốc $=\dfrac1R$.",
      r"Song song : $R_{td}=\dfrac{R_1R_2}{R_1+R_2}$ ; nối tiếp : $R_{td}=R_1+R_2$, $U_i=IR_i$.",
      r"⚠ <strong>Điều kiện:</strong> xem trục nào là $U$ rồi mới nói độ dốc là $R$ hay $1/R$."]
R5 = [r"<strong>Khái niệm:</strong> biến trở mắc nối tiếp : $R_b$ tăng thì $I$ giảm.",
      r"<strong>Công thức:</strong> $I=\dfrac U{R_b+R}$ ; $I_{max}=\dfrac UR$ ; $I_{min}=\dfrac U{R_{max}+R}$ ; $R=\dfrac{\rho l}{S}$.",
      r"Cuộn dây quấn đều : $R_b$ tỉ lệ với chiều dài phần dây dùng ; số vòng $N=\dfrac l{\pi D}$.",
      r"⚠ <strong>Điều kiện:</strong> $0\le R_b\le R_{max}$ và $I$ không vượt dòng định mức của biến trở."]
R6 = [r"<strong>Khái niệm:</strong> ampe kế, vôn kế thực có điện trở ; chúng là một phần của mạch.",
      r"<strong>Công thức:</strong> $R_P=\dfrac{R_1R_V}{R_1+R_V}$ ; $R_{mach}=R_P+R_2+R_A$ ; $I_A=\dfrac U{R_{mach}}$ ; $U_V=I_AR_P$.",
      r"Dụng cụ chia vạch : ĐCNN $=\dfrac{A_{max}}N$ ; $\Delta A=x\%\cdot A_{max}$ ; $\delta=\dfrac{\Delta A}{A}$.",
      r"⚠ <strong>Điều kiện:</strong> $\Delta A$ tính theo giá trị lớn nhất của <strong>thang</strong> đang dùng, không theo số chỉ."]

SOLS = [
 sol(R1, [
  ("Điện trở dây nhôm", [P(r"Đổi tiết diện : $S=0{,}5\ \text{mm}^2=0{,}5\cdot10^{-6}=5\cdot10^{-7}\ \text{m}^2$."), M(r"R=\dfrac{\rho l}{S}=\dfrac{2{,}8\cdot10^{-8}\cdot200}{5\cdot10^{-7}}"), A(r"R=11{,}2\ \Omega")]),
  ("Tiết diện dây đồng", [P(r"Cùng $l$ và cùng $R$ nên $S$ tỉ lệ thuận với $\rho$ :"), M(r"\dfrac{S_{Cu}}{S_{Al}}=\dfrac{\rho_{Cu}}{\rho_{Al}}=\dfrac{1{,}7}{2{,}8}\approx0{,}607"),
     M(r"S_{Cu}\approx0{,}607\cdot0{,}5"), A(r"S_{Cu}\approx0{,}304\ \text{mm}^2"), P(r"Đồng dẫn điện tốt hơn nhôm nên cần tiết diện nhỏ hơn ✓.")]),
  ("Đường kính dây đồng", [M(r"S=\dfrac{\pi d^2}{4}\ \Rightarrow\ d=\sqrt{\dfrac{4S}{\pi}}"), M(r"d=\sqrt{\dfrac{4\cdot0{,}304}{3{,}14}}"), A(r"d\approx0{,}62\ \text{mm}")]),
  ("Dòng điện qua dây nhôm", [M(r"I=\dfrac UR=\dfrac{5{,}6}{11{,}2}"), A(r"I=0{,}5\ \text{A}")]),
  ("Kiểm tra", [P(r"Dây dài $200\ \text{m}$ mảnh $0{,}5\ \text{mm}^2$ có $R$ cỡ vài đến vài chục ôm : hợp lí. Nếu ra hàng nghìn ôm thì đã quên đổi $\text{mm}^2$ sang $\text{m}^2$."),
     P(r"Tỉ lệ $0{,}304/0{,}5\approx0{,}61$ khớp $1{,}7/2{,}8$ ✓.")])],
  [r"a) $R=11{,}2\ \Omega$", r"b) $S_{Cu}\approx0{,}304\ \text{mm}^2$", r"c) $d\approx0{,}62\ \text{mm}$", r"d) $I=0{,}5\ \text{A}$"],
  r"Nhận dạng: thấy <strong>$\rho$, $l$, $S$ (hay đường kính)</strong> → $R=\rho l/S$, đổi $\text{mm}^2$ trước ; thấy <strong>cùng $R$, cùng $l$, khác vật liệu</strong> → $S\propto\rho$."),
 sol(R2, [
  ("Điện trở mỗi đoạn", [P(r"$3$ đoạn bằng nhau, mỗi đoạn dài $\dfrac l3$ :"), M(r"R_0=\dfrac R3=\dfrac{90}3"), A(r"R_0=30\ \Omega")]),
  ("Điện trở tương đương khi song song", [M(r"R_{td}=\dfrac{R_0}3=\dfrac{30}3"), A(r"R_{td}=10\ \Omega"), P(r"Kiểm tra bằng $R/n^2=90/9=10\ \Omega$ ✓ ; nhỏ hơn mỗi đoạn $30\ \Omega$ ✓.")]),
  ("Dòng điện mạch chính", [M(r"I=\dfrac U{R_{td}}=\dfrac 6{10}"), A(r"I=0{,}6\ \text{A}")]),
  ("Dòng điện qua mỗi đoạn", [P(r"Ba đoạn giống nhau, cùng $U=6\ \text{V}$ :"), M(r"I_0=\dfrac U{R_0}=\dfrac 6{30}"), A(r"I_0=0{,}2\ \text{A}"), P(r"Kiểm tra : $3\cdot0{,}2=0{,}6\ \text{A}=I$ ✓.")]),
  ("Số đoạn cần cắt", [P(r"Cắt $n$ đoạn bằng nhau rồi ghép song song :"), M(r"R_{td}=\dfrac R{n^2}"), M(r"0{,}9=\dfrac{90}{n^2}\ \Rightarrow\ n^2=100"), A(r"n=10\ \text{đoạn}"), P(r"Mỗi đoạn $9\ \Omega$, ghép song song $9/10=0{,}9\ \Omega$ ✓.")]),
  ("Kiểm tra", [P(r"Ghép song song luôn cho điện trở nhỏ hơn điện trở từng đoạn : $10\lt30$ và $0{,}9\lt9$ ✓."),
     P(r"Nếu ghép $3$ đoạn <em>nối tiếp</em> thì lại được $90\ \Omega$ như dây ban đầu.")])],
  [r"a) $R_0=30\ \Omega$", r"b) $R_{td}=10\ \Omega$", r"c) $I=0{,}6\ \text{A}$ ; mỗi đoạn $0{,}2\ \text{A}$", r"d) $n=10$"],
  r"Nhận dạng: thấy <strong>cắt thành $n$ đoạn bằng nhau</strong> → mỗi đoạn $R/n$ ; thấy <strong>ghép song song</strong> → thêm một lần chia $n$, được $R/n^2$."),
 sol(R3, [
  ("Điện trở sau lần kéo thứ nhất", [P(r"Thể tích không đổi nên $R\propto l^2$ ; $l_2=1{,}5\,l_1$ :"), M(r"\dfrac{R_2}{R_1}=\left(\dfrac{l_2}{l_1}\right)^2=1{,}5^2=2{,}25"), M(r"R_2=2{,}25\cdot20"), A(r"R_2=45\ \Omega")]),
  ("Chiều dài tăng ở lần kéo thứ hai", [P(r"Đường kính giảm một nửa nên tiết diện giảm $4$ lần :"), M(r"\dfrac{S_3}{S_2}=\left(\dfrac12\right)^2=\dfrac14"),
     M(r"S_2l_2=S_3l_3\ \Rightarrow\ \dfrac{l_3}{l_2}=\dfrac{S_2}{S_3}"), A(r"\dfrac{l_3}{l_2}=4")]),
  ("Điện trở sau lần kéo thứ hai", [P(r"Lần này tính từ $R_2$ (trạng thái ngay trước) :"), M(r"\dfrac{R_3}{R_2}=\left(\dfrac{l_3}{l_2}\right)^2=4^2=16"), M(r"R_3=16\cdot45"), A(r"R_3=720\ \Omega"),
     P(r"Kiểm tra : tổng cộng $36$ lần $R_1$, bằng $2{,}25\cdot16$ ✓ ; đường kính giảm $2$ lần thì $R$ tăng $2^4=16$ lần ✓.")]),
  ("Chiều dài sợi đồng", [P(r"Đổi : $m=178\ \text{g}=0{,}178\ \text{kg}$ ; $S=0{,}5\ \text{mm}^2=5\cdot10^{-7}\ \text{m}^2$."), M(r"V=\dfrac mD=\dfrac{0{,}178}{8900}=2\cdot10^{-5}\ \text{m}^3"), M(r"l=\dfrac VS=\dfrac{2\cdot10^{-5}}{5\cdot10^{-7}}"), A(r"l=40\ \text{m}")]),
  ("Điện trở sợi đồng", [M(r"R=\dfrac{\rho l}{S}=\dfrac{1{,}7\cdot10^{-8}\cdot40}{5\cdot10^{-7}}"), A(r"R=1{,}36\ \Omega"), P(r"Sợi đồng $40\ \text{m}$ mảnh $0{,}5\ \text{mm}^2$ có $R$ cỡ $1\ \Omega$ : hợp lí ✓.")])],
  [r"a) $R_2=45\ \Omega$", r"b) $R_3=720\ \Omega$", r"c) $l=40\ \text{m}$ ; $R=1{,}36\ \Omega$"],
  r"Nhận dạng: thấy <strong>kéo dãn, thể tích không đổi</strong> → $R_2/R_1=(l_2/l_1)^2$, không dùng $R\propto l$ ; thấy <strong>đường kính giảm $k$ lần</strong> → $R$ tăng $k^4$ lần ; thấy <strong>khối lượng, khối lượng riêng</strong> → $V=m/D$."),
 sol(R4, [
  ("Điện trở vật dẫn (1)", [P(r"Trục tung là $U$ nên độ dốc là $R$ :"), M(r"R_1=\dfrac{U_A}{I_A}=\dfrac{3{,}0}{0{,}5}"), A(r"R_1=6\ \Omega")]),
  ("Điện trở vật dẫn (2)", [M(r"R_2=\dfrac{U_B}{I_B}=\dfrac{4{,}5}{0{,}5}"), A(r"R_2=9\ \Omega")]),
  ("So sánh độ dốc", [P(r"Cùng $I=0{,}5\ \text{A}$ thì $U$ của $(2)$ lớn hơn nên đường $(2)$ nằm trên và <strong>dốc hơn</strong>."), P(r"Trên đồ thị $U$–$I$ độ dốc là $R$ : $R_2\gt R_1$ nên đường $(2)$ dốc hơn.")]),
  ("Dòng mạch chính khi song song", [M(r"R_{td}=\dfrac{R_1R_2}{R_1+R_2}=\dfrac{6\cdot9}{15}=3{,}6\ \Omega"), M(r"I=\dfrac U{R_{td}}=\dfrac{4{,}5}{3{,}6}"), A(r"I=1{,}25\ \text{A}"),
     P(r"Kiểm tra : $I_1=\dfrac{4{,}5}6=0{,}75\ \text{A}$, $I_2=\dfrac{4{,}5}9=0{,}5\ \text{A}$, tổng $1{,}25\ \text{A}$ ✓.")]),
  ("Hiệu điện thế mỗi vật dẫn khi nối tiếp", [M(r"R_{td}=R_1+R_2=15\ \Omega"), M(r"I'=\dfrac{U'}{R_{td}}=\dfrac6{15}=0{,}4\ \text{A}"), M(r"U_1'=I'R_1=0{,}4\cdot6"), A(r"U_1'=2{,}4\ \text{V}"),
     P(r"$U_2'=I'R_2=3{,}6\ \text{V}$ ; $U_1'+U_2'=6\ \text{V}$ ✓.")]),
  ("Độ dốc đồ thị I–U", [P(r"Đổi hai trục : $I=\dfrac UR$, độ dốc là $\dfrac1R$ :"), M(r"k_1=\dfrac{\Delta I}{\Delta U}=\dfrac1{R_1}=\dfrac16"), A(r"k_1\approx0{,}167\ \text{A/V}"), P(r"Đường $(2)$ có $k_2=1/9\approx0{,}111\ \text{A/V}$, thoải hơn : ngược với đồ thị $U$–$I$ ✓.")])],
  [r"a) $R_1=6\ \Omega$ ; $R_2=9\ \Omega$", r"b) đường $(2)$ dốc hơn", r"c) $I=1{,}25\ \text{A}$", r"d) $U_1'=2{,}4\ \text{V}$ ; $U_2'=3{,}6\ \text{V}$", r"e) $k_1\approx0{,}167\ \text{A/V}$"],
  r"Nhận dạng: thấy <strong>đồ thị qua gốc toạ độ</strong> → xem trục rồi nói độ dốc là $R$ ($U$–$I$) hay $1/R$ ($I$–$U$) ; hai vật dẫn <strong>ghép</strong> → tính $R_{td}$ từ hai điện trở vừa đọc."),
 sol(R5, [
  ("Dòng nhỏ nhất", [P(r"Con chạy ở $R_b=R_{max}$ :"), M(r"I_{min}=\dfrac U{R_{max}+R}=\dfrac{24}{50+30}"), A(r"I_{min}=0{,}3\ \text{A}")]),
  ("Dòng lớn nhất", [P(r"Con chạy ở $R_b=0$ :"), M(r"I_{max}=\dfrac UR=\dfrac{24}{30}"), A(r"I_{max}=0{,}8\ \text{A}"), P(r"$0{,}8\lt1{,}5\ \text{A}$ nên biến trở an toàn. Dòng chỉnh được từ $0{,}3$ đến $0{,}8\ \text{A}$.")]),
  ("Giá trị biến trở cho dòng $0{,}6\\ \\text{A}$", [M(r"R_{mach}=\dfrac U{I_0}=\dfrac{24}{0{,}6}=40\ \Omega"), M(r"R_b=R_{mach}-R=40-30"), A(r"R_b=10\ \Omega"), P(r"$0\lt10\lt50$ : đặt được ✓.")]),
  ("Vị trí con chạy", [P(r"Cuộn dây quấn đều nên $R_b$ tỉ lệ với chiều dài phần dây có dòng :"), M(r"\dfrac{R_b}{R_{max}}=\dfrac{10}{50}"), A(r"20\%\ \text{chiều dài cuộn dây}")]),
  ("Chiều dài dây quấn biến trở", [M(r"S=\dfrac{\pi d^2}4=\dfrac{3{,}14\cdot(4\cdot10^{-4})^2}4\approx1{,}26\cdot10^{-7}\ \text{m}^2"), M(r"l=\dfrac{R_{max}S}{\rho}=\dfrac{50\cdot1{,}26\cdot10^{-7}}{1{,}1\cdot10^{-6}}"), A(r"l\approx5{,}7\ \text{m}")]),
  ("Số vòng dây", [P(r"Mỗi vòng dài $\pi D=3{,}14\cdot2\cdot10^{-2}=0{,}0628\ \text{m}$ :"), M(r"N=\dfrac{l}{\pi D}=\dfrac{5{,}7}{0{,}0628}"), A(r"N\approx91\ \text{vòng}"), P(r"Thực tế mỗi vòng dài hơn một chút ($\pi(D+d)$) nên số vòng ít hơn khoảng $2\%$ ; làm tròn lên khi quấn.")])],
  [r"a) $I$ từ $0{,}3\ \text{A}$ đến $0{,}8\ \text{A}$", r"b) $R_b=10\ \Omega$ ; con chạy ở $20\%$", r"c) $l\approx5{,}7\ \text{m}$ ; $N\approx91$ vòng"],
  r"Nhận dạng: thấy <strong>biến trở nối tiếp, khoảng dòng điều chỉnh</strong> → tính hai đầu mút $R_b=0$ và $R_b=R_{max}$ ; thấy <strong>dòng cho trước</strong> → $R_b=U/I_0-R$ rồi kiểm $0\le R_b\le R_{max}$."),
 sol(R6, [
  ("Điện trở đoạn $R_1$ song song vôn kế", [M(r"R_P=\dfrac{R_1R_V}{R_1+R_V}=\dfrac{6\cdot4000}{4006}"), A(r"R_P\approx5{,}99\ \Omega")]),
  ("Số chỉ ampe kế", [M(r"R_{mach}=R_P+R_2+R_A\approx5{,}99+18+0{,}5=24{,}49\ \Omega"), M(r"I_A=\dfrac U{R_{mach}}=\dfrac{12}{24{,}49}"), A(r"I_A\approx0{,}490\ \text{A}")]),
  ("Số chỉ vôn kế", [M(r"U_V=I_AR_P\approx0{,}490\cdot5{,}99"), A(r"U_V\approx2{,}94\ \text{V}"),
     P(r"Bỏ vôn kế : $I'=\dfrac{12}{24{,}5}\approx0{,}4898\ \text{A}$ và $U_1=I'R_1\approx2{,}94\ \text{V}$ : vôn kế $4000\ \Omega$ hầu như không ảnh hưởng.")]),
  ("Số chỉ của vôn kế $6\\ \\Omega$", [M(r"R_P'=\dfrac{6\cdot6}{12}=3\ \Omega"), M(r"R_{mach}'=3+18+0{,}5=21{,}5\ \Omega"), M(r"I_A'=\dfrac{12}{21{,}5}\approx0{,}558\ \text{A}"), M(r"U_V'=I_A'R_P'\approx0{,}558\cdot3"), A(r"U_V'\approx1{,}67\ \text{V}")]),
  ("Độ lệch so với giá trị thật", [P(r"Giá trị thật (không mắc vôn kế) : $U_1=\dfrac{12\cdot6}{24{,}5}\approx2{,}94\ \text{V}$."), M(r"\dfrac{U_1-U_V'}{U_1}=\dfrac{2{,}94-1{,}67}{2{,}94}"), A(r"\approx43\%"),
     P(r"Vôn kế phải có điện trở rất lớn so với điện trở đoạn mạch cần đo.")]),
  ("Độ chia nhỏ nhất của vôn kế", [M(r"\text{ĐCNN}=\dfrac{A_{max}}N=\dfrac6{30}"), A(r"\text{ĐCNN}=0{,}2\ \text{V}")]),
  ("Sai số dụng cụ", [P(r"Sai số tính theo giá trị lớn nhất của <strong>thang</strong> $6\ \text{V}$, không theo số chỉ :"), M(r"\Delta U=1{,}0\%\cdot6"), A(r"\Delta U=0{,}06\ \text{V}"),
     M(r"\delta=\dfrac{\Delta U}{U_V}=\dfrac{0{,}06}{2{,}94}\approx2{,}0\%"), P(r"Kết quả ghi : $U=(2{,}94\pm0{,}06)\ \text{V}$, $\delta\approx2{,}0\%$.")])],
  [r"a) $I_A\approx0{,}490\ \text{A}$ ; $U_V\approx2{,}94\ \text{V}$", r"b) $U_V'\approx1{,}67\ \text{V}$ ; lệch khoảng $43\%$", r"c) ĐCNN $=0{,}2\ \text{V}$ ; $\Delta U=0{,}06\ \text{V}$ ; $\delta\approx2{,}0\%$"],
  r"Nhận dạng: thấy <strong>ampe kế, vôn kế có điện trở</strong> → vẽ chúng thành điện trở trong mạch rồi tính ; thấy <strong>cấp chính xác</strong> → $\Delta A=x\%\cdot A_{max}$ của thang."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>$\rho$, $l$, $S$ hay đường kính</b> → nghĩ tới <b>$R=\rho l/S$</b>, đổi mm² sang m² trước.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Điện trở dây nhôm", "Điện trở của dây nhôm là bao nhiêu?", 11.2, "Ω", 0.1,
       loi=r"Dùng $S=0{,}5$ như đã là $\text{m}^2$ : $R$ ra lớn hơn thật $10^6$ lần."),
  buoc("Tiết diện dây đồng", "Tiết diện của dây đồng là bao nhiêu mm²?", 0.304, "mm²", 0.005,
       loi=r"Lấy $S_{Cu}/S_{Al}=\rho_{Al}/\rho_{Cu}$ (ngược) nên ra $S_{Cu}$ lớn hơn $S_{Al}$ dù đồng dẫn điện tốt hơn.",
       ke=[(r"Cùng $l$ và $R$ nên $S$ tỉ lệ thuận với $\rho$ : $\dfrac{S_{Cu}}{S_{Al}}=\dfrac{\rho_{Cu}}{\rho_{Al}}$", True),
           (r"$\dfrac{S_{Cu}}{S_{Al}}=\dfrac{\rho_{Al}}{\rho_{Cu}}$", r"Từ $R=\rho l/S$ với $R$, $l$ không đổi thì $S\propto\rho$ chứ không tỉ lệ nghịch ; đồng có $\rho$ nhỏ hơn nên cần $S$ nhỏ hơn."),
           (r"Cùng $R$ nên cùng tiết diện", r"$R$ còn phụ thuộc $\rho$ ; hai vật liệu khác nhau thì cùng $R$ vẫn cần tiết diện khác nhau.")]),
  buoc("Đường kính dây đồng", "Đường kính của dây đồng là bao nhiêu mm?", 0.62, "mm", 0.01,
       loi=r"Dùng $d=\sqrt{S/\pi}$ : đó là bán kính, thiếu hệ số $2$.",
       ke=[(r"$d=\sqrt{\dfrac{4S}{\pi}}$ từ $S=\dfrac{\pi d^2}{4}$", True),
           (r"$d=\sqrt{\dfrac S\pi}$", r"Đó là bán kính $r$ (từ $S=\pi r^2$) ; đường kính gấp đôi."),
           (r"$d=\dfrac{S}{\pi}$", r"$S$ tỉ lệ với $d^2$ chứ không tỉ lệ với $d$.")]),
  buoc("Dòng điện qua dây nhôm", "Cường độ dòng điện qua dây nhôm là bao nhiêu A?", 0.5, "A", 0.01,
       loi=r"Đảo thành $I=R/U$, hoặc nhân $U$ với $R$ thay vì chia.",
       ke=[(r"$I=\dfrac UR$ với $R$ vừa tính ở bước đầu", True),
           (r"$I=U\cdot R$", r"Tích $\text{V}\cdot\Omega$ không phải ampe ; $U$ tăng thì $I$ tăng nhưng $R$ tăng thì $I$ giảm."),
           (r"$I=\dfrac RU$", r"Đảo ngược : $I$ phải tăng khi $U$ tăng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cắt thành $n$ đoạn bằng nhau, ghép song song</b> → nghĩ tới <b>$R/n$ mỗi đoạn, $R/n^2$ cả bộ</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Điện trở mỗi đoạn", "Điện trở của mỗi đoạn là bao nhiêu?", 30, "Ω", 0.5,
       loi=r"Giữ nguyên $90\ \Omega$ hoặc nhân $3$ thay vì chia $3$."),
  buoc("Điện trở tương đương khi song song", "Điện trở tương đương của bộ ba đoạn song song là bao nhiêu?", 10, "Ω", 0.2,
       loi=r"Cộng ba điện trở như nối tiếp ($90\ \Omega$), hoặc cộng nghịch đảo nhưng quên lấy nghịch đảo lần nữa.",
       ke=[(r"$R_{td}=\dfrac{R_0}{3}$ vì ba nhánh giống nhau", True),
           (r"$R_{td}=3R_0$", r"Đó là nối tiếp ; song song nhiều nhánh làm điện trở chung nhỏ hơn."),
           (r"$R_{td}=R_0$", r"Thêm nhánh song song luôn làm điện trở chung giảm.")]),
  buoc("Dòng điện mạch chính", "Cường độ dòng điện qua mạch chính là bao nhiêu?", 0.6, "A", 0.01,
       loi=r"Chia $6\ \text{V}$ cho điện trở của <em>một</em> đoạn hay của cả dây $90\ \Omega$.",
       ke=[(r"$I=\dfrac U{R_{td}}$ với $R_{td}$ của cả bộ", True),
           (r"$I=\dfrac U{R_0}$", r"Đó là dòng qua <em>một</em> đoạn, chưa phải dòng mạch chính."),
           (r"$I=\dfrac UR$ với $R=90\ \Omega$", r"$90\ \Omega$ là dây trước khi cắt ; mạch bây giờ là bộ song song.")]),
  buoc("Dòng điện qua mỗi đoạn", "Cường độ dòng điện qua mỗi đoạn là bao nhiêu?", 0.2, "A", 0.005,
       loi=r"Lấy mỗi đoạn có cả $0{,}6\ \text{A}$ (quên chia cho $3$ nhánh).",
       ke=[(r"Ba đoạn giống nhau, chung $U$ : $I_0=\dfrac U{R_0}$", True),
           (r"$I_0=3I$", r"Dòng mạch chính là <em>tổng</em> ba nhánh nên mỗi nhánh nhỏ hơn, không lớn hơn."),
           (r"$I_0=\dfrac U{R_{td}}$", r"Đó là dòng mạch chính.")]),
  buoc("Số đoạn cần cắt", "Phải cắt thành bao nhiêu đoạn bằng nhau?", 10, "đoạn", 0.05,
       loi=r"Dùng $R_{td}=R/n$ (quên một lần chia nữa khi ghép song song) nên ra $n=100$.",
       ke=[(r"$R_{td}=\dfrac R{n^2}$ rồi giải $n^2=\dfrac R{R_{td}}$", True),
           (r"$R_{td}=\dfrac Rn$", r"$R/n$ mới là điện trở <em>mỗi đoạn</em> ; ghép song song $n$ đoạn còn chia thêm $n$ lần."),
           (r"$R_{td}=nR$", r"Cắt dây rồi ghép nối tiếp chỉ được lại $R$, không phải $nR$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>kéo dãn, thể tích không đổi</b> → nghĩ tới <b>$R\propto l^2$</b>, không phải $R\propto l$.",
  cap_do=3, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Điện trở sau lần kéo thứ nhất", "Điện trở của dây sau lần kéo thứ nhất là bao nhiêu?", 45, "Ω", 0.5,
       loi=r"Dùng $R_2/R_1=l_2/l_1$ nên ra $30\ \Omega$ : quên tiết diện giảm theo."),
  buoc("Chiều dài tăng ở lần kéo thứ hai", "Lần kéo thứ hai làm chiều dài tăng bao nhiêu lần?", 4, "lần", 0.05,
       loi=r"Cho rằng đường kính giảm $2$ lần thì chiều dài tăng $2$ lần : bỏ qua $S\propto d^2$.",
       ke=[(r"$S$ giảm $4$ lần, $V$ không đổi nên $l$ tăng $4$ lần", True),
           (r"Đường kính giảm $2$ lần nên $l$ tăng $2$ lần", r"Tiết diện tỉ lệ với $d^2$ nên giảm $4$ lần ; $l$ phải tăng $4$ lần để $V=Sl$ không đổi."),
           (r"Chiều dài không đổi vì chỉ đổi đường kính", r"Đây là kéo dãn, thể tích không đổi : dây mảnh đi thì phải dài ra.")]),
  buoc("Điện trở sau lần kéo thứ hai", "Điện trở của dây sau lần kéo thứ hai là bao nhiêu?", 720, "Ω", 5,
       loi=r"Tính $16\cdot20=320\ \Omega$ : lấy tỉ số $16$ của lần hai nhân với $R_1$ thay vì $R_2$.",
       ke=[(r"$\dfrac{R_3}{R_2}=\left(\dfrac{l_3}{l_2}\right)^2$, tính từ $R_2$", True),
           (r"$R_3=16R_1$", r"Tỉ số $16$ là so với $R_2$ (đã kéo lần một), không phải so với $R_1$."),
           (r"$\dfrac{R_3}{R_2}=\dfrac{l_3}{l_2}$", r"Kéo dãn thì $S$ đổi nên phải bình phương tỉ số chiều dài.")]),
  buoc("Chiều dài sợi đồng", "Chiều dài sợi đồng kéo được là bao nhiêu mét?", 40, "m", 0.5,
       loi=r"Chia khối lượng cho tiết diện, hoặc không đổi $\text{mm}^2$ và $\text{g}$ sang đơn vị SI.",
       ke=[(r"$V=\dfrac mD$ rồi $l=\dfrac VS$", True),
           (r"$l=\dfrac mD$", r"$m/D$ là <em>thể tích</em>, chưa phải chiều dài ; còn phải chia cho $S$."),
           (r"$l=V\cdot S$", r"$V=S\cdot l$ nên $l=V/S$ ; nhân $V$ với $S$ không ra chiều dài.")]),
  buoc("Điện trở sợi đồng", "Điện trở của sợi đồng là bao nhiêu Ω?", 1.36, "Ω", 0.02,
       loi=r"Thay $S=0{,}5$ ($\text{mm}^2$) cùng $\rho$ theo $\Omega\cdot\text{m}$ : trộn hai hệ đơn vị.",
       ke=[(r"$R=\dfrac{\rho l}{S}$ với $S$ đổi ra $\text{m}^2$", True),
           (r"$R=\dfrac{\rho l}{S}$ với $S=0{,}5$ và $\rho$ giữ $\Omega\cdot\text{m}$", r"Trộn hai hệ đơn vị : phải cùng $\text{m}^2$ hoặc dùng $\rho$ theo $\Omega\cdot\text{mm}^2/\text{m}$."),
           (r"$R=\dfrac{\rho S}{l}$", r"Đảo ngược : dây dài hơn thì $R$ tăng.")])]),
 dict(nhan_dang=r"Thấy <b>đồ thị qua gốc toạ độ</b> → nghĩ tới <b>độ dốc là $R$ (trục $U$) hay $1/R$ (trục $I$)</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện trở vật dẫn (1)", "Điện trở của vật dẫn (1) là bao nhiêu?", 6, "Ω", 0.1,
       loi=r"Lấy $I/U$ thay vì $U/I$ : nhầm hệ số góc khi trục tung là $U$."),
  buoc("Điện trở vật dẫn (2)", "Điện trở của vật dẫn (2) là bao nhiêu?", 9, "Ω", 0.1,
       loi=r"Lấy $4{,}5-3{,}0$ rồi chia cho $0{,}5$ : trừ hai điểm của <em>hai đường khác nhau</em> thay vì cùng một đường.",
       ke=[(r"$R_2=\dfrac{U_B}{I_B}$ vì đường $(2)$ đi qua gốc toạ độ", True),
           (r"$R_2=\dfrac{U_B-U_A}{I_B-I_A}$", r"$A$ và $B$ thuộc hai đường khác nhau ; hiệu hai điểm đó không phải hệ số góc của đường nào ($I_B-I_A=0$)."),
           (r"$R_2=U_B\cdot I_B$", r"Tích $\text{V}\cdot\text{A}$ là công suất, không phải điện trở.")]),
  buoc("So sánh độ dốc", "Trên đồ thị $U$–$I$, đường nào dốc hơn?",
       loi=r"Nghĩ điện trở nhỏ thì dốc hơn (nhầm với đồ thị $I$–$U$).",
       ke=[(r"Xét cùng một $I$ rồi so $U$ của hai đường", True),
           (r"Đường nào nằm dưới thì dốc hơn", r"Trên $U$–$I$ đường nằm trên (cùng $I$ mà $U$ lớn hơn) mới dốc hơn."),
           (r"Đường nào vẽ ngắn hơn thì dốc hơn", r"Độ dài đoạn vẽ không liên quan tới độ dốc.")],
       lua_chon=[(r"Đường $(2)$ dốc hơn vì cùng $I$ thì $U$ lớn hơn", True),
                 (r"Đường $(1)$ dốc hơn vì $R_1$ nhỏ hơn", r"Trên $U$–$I$ độ dốc là $R$ ; $R$ nhỏ thì đường thoải hơn."),
                 (r"Hai đường dốc như nhau vì cùng đi qua $I=0{,}5\ \text{A}$", r"Cùng $I$ nhưng $U$ khác nhau thì độ dốc khác nhau.")]),
  buoc("Dòng mạch chính khi song song", "Cường độ dòng điện mạch chính khi hai vật dẫn song song là bao nhiêu?", 1.25, "A", 0.02,
       loi=r"Cộng hai điện trở ($15\ \Omega$) như nối tiếp, hoặc cộng $I_1+I_2$ nhưng tính $I_i$ với sai $U$.",
       ke=[(r"$R_{td}=\dfrac{R_1R_2}{R_1+R_2}$ rồi $I=\dfrac U{R_{td}}$", True),
           (r"$R_{td}=R_1+R_2$", r"Đó là nối tiếp ; song song thì $R_{td}$ nhỏ hơn mỗi điện trở."),
           (r"$I=\dfrac U{R_1}$ (chỉ vật dẫn (1))", r"Chưa tính nhánh còn lại ; dòng mạch chính là tổng hai nhánh.")]),
  buoc("Hiệu điện thế mỗi vật dẫn khi nối tiếp", "Hiệu điện thế giữa hai đầu vật dẫn (1) khi nối tiếp là bao nhiêu?", 2.4, "V", 0.05,
       loi=r"Chia đôi $6\ \text{V}$ vì tưởng nối tiếp thì $U$ chia đều ; $U$ chia theo tỉ lệ điện trở.",
       ke=[(r"$I'=\dfrac{U'}{R_1+R_2}$ rồi $U_1'=I'R_1$", True),
           (r"$U_1'=\dfrac{U'}2$", r"Nối tiếp thì $I$ bằng nhau, $U$ chia theo tỉ lệ $R$ ; hai điện trở khác nhau thì $U$ khác nhau."),
           (r"$U_1'=U'$", r"Chỉ đúng khi song song ; nối tiếp thì $U_1'+U_2'=U'$.")]),
  buoc("Độ dốc đồ thị I–U", "Độ dốc của đường ứng với vật dẫn (1) trên đồ thị $I$–$U$ là bao nhiêu A/V?", 0.167, "A/V", 0.005,
       loi=r"Lấy lại $6$ (độ dốc của đồ thị $U$–$I$) : quên đổi trục thì độ dốc nghịch đảo.",
       ke=[(r"Trục tung là $I$ nên độ dốc là $\dfrac{\Delta I}{\Delta U}=\dfrac1R$", True),
           (r"Độ dốc vẫn là $R=6$", r"Đó là độ dốc của đồ thị $U$–$I$ ; đổi trục thì độ dốc là $1/R$."),
           (r"Độ dốc là $\dfrac1{R_2}$", r"$1/R_2$ ứng với vật dẫn $(2)$, không phải $(1)$.")]),
  ]),
 dict(nhan_dang=r"Thấy <b>biến trở nối tiếp, khoảng dòng điều chỉnh</b> → nghĩ tới <b>hai đầu mút $R_b=0$ và $R_b=R_{max}$</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Dòng nhỏ nhất", "Cường độ dòng điện nhỏ nhất trong mạch là bao nhiêu?", 0.3, "A", 0.01,
       loi=r"Chỉ tính $U/R_{max}$ (quên điện trở phụ $R$)."),
  buoc("Dòng lớn nhất", "Cường độ dòng điện lớn nhất trong mạch là bao nhiêu?", 0.8, "A", 0.01,
       loi=r"Cho $R_b=0$ rồi chia $U$ cho $0$ ; điện trở phụ $R$ vẫn còn trong mạch.",
       ke=[(r"$R_b=0$ nên chỉ còn $R$ : $I_{max}=\dfrac UR$", True),
           (r"$I_{max}=\dfrac U{R_{max}}$", r"Dòng lớn nhất ứng với điện trở <em>nhỏ</em> nhất của biến trở, không phải lớn nhất."),
           (r"$I_{max}=I_{dm}=1{,}5\ \text{A}$", r"$1{,}5\ \text{A}$ là giới hạn chịu đựng, không phải dòng mạch thực sự đạt được.")]),
  buoc("Giá trị biến trở cho dòng $0{,}6\\ \\text{A}$", "Biến trở phải có giá trị bao nhiêu để dòng bằng $0{,}6\\ \\text{A}$?", 10, "Ω", 0.2,
       loi=r"Lấy $U/I_0=40\ \Omega$ làm luôn $R_b$ mà quên trừ điện trở phụ $R$.",
       ke=[(r"$R_b=\dfrac U{I_0}-R$", True),
           (r"$R_b=\dfrac U{I_0}$", r"$U/I_0$ là điện trở <em>cả mạch</em> ; còn phải trừ phần của $R$."),
           (r"$R_b=\dfrac U{I_0}+R$", r"Cộng thay vì trừ : biến trở chỉ là một phần của điện trở cả mạch.")]),
  buoc("Vị trí con chạy", "Con chạy cách đầu đã mắc bao nhiêu phần trăm chiều dài cuộn dây?", 20, "%", 0.5,
       loi=r"Chia $R_b$ cho $R$ thay vì cho $R_{max}$.",
       ke=[(r"Cuộn đều nên $\dfrac{R_b}{R_{max}}$ bằng tỉ lệ chiều dài", True),
           (r"$\dfrac{R_b}{R}$", r"$R$ là điện trở phụ ngoài biến trở, không liên quan chiều dài cuộn dây."),
           (r"$\dfrac{R_b}{R_b+R}$", r"Đó là tỉ lệ hiệu điện thế trên biến trở, không phải vị trí con chạy.")]),
  buoc("Chiều dài dây quấn biến trở", "Chiều dài dây nicrom quấn biến trở là bao nhiêu mét?", 5.7, "m", 0.1,
       loi=r"Dùng $S=\pi d^2$ (quên chia $4$) nên $l$ ra lớn hơn $4$ lần ; hoặc quên đổi $\text{mm}$ sang $\text{m}$.",
       ke=[(r"$S=\dfrac{\pi d^2}4$ rồi $l=\dfrac{R_{max}S}{\rho}$", True),
           (r"$S=\pi d^2$ rồi $l=\dfrac{R_{max}S}{\rho}$", r"Thiếu hệ số $\dfrac14$ : $S=\pi r^2=\pi d^2/4$."),
           (r"$l=\dfrac{\rho S}{R_{max}}$", r"Đảo ngược : từ $R=\rho l/S$ suy ra $l=RS/\rho$.")]),
  buoc("Số vòng dây", "Số vòng dây quấn trên ống sứ là bao nhiêu?", 91, "vòng", 1,
       loi=r"Chia $l$ cho $\pi d$ (đường kính dây) thay vì $\pi D$ (đường kính ống sứ).",
       ke=[(r"Mỗi vòng dài $\pi D$ nên $N=\dfrac l{\pi D}$", True),
           (r"$N=\dfrac l{\pi d}$", r"$d$ là đường kính <em>dây</em> ; chiều dài mỗi vòng theo chu vi ống sứ $D$."),
           (r"$N=\dfrac lD$", r"Thiếu $\pi$ : chu vi vòng tròn là $\pi D$.")]),
  ]),
 dict(nhan_dang=r"Thấy <b>ampe kế, vôn kế có điện trở</b> → nghĩ tới <b>coi dụng cụ là một điện trở trong mạch rồi tính $R_{td}$</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Điện trở đoạn $R_1$ song song vôn kế", "Điện trở của đoạn gồm $R_1$ song song với vôn kế là bao nhiêu Ω?", 5.99, "Ω", 0.02,
       loi=r"Cộng $R_1+R_V$ như nối tiếp, hoặc coi vôn kế không có điện trở."),
  buoc("Số chỉ ampe kế", "Số chỉ của ampe kế là bao nhiêu A?", 0.490, "A", 0.002,
       loi=r"Bỏ $R_A$ ra khỏi điện trở toàn mạch vì coi ampe kế lí tưởng.",
       ke=[(r"$I_A=\dfrac U{R_P+R_2+R_A}$", True),
           (r"$I_A=\dfrac U{R_P+R_2}$", r"Đề cho $R_A=0{,}5\ \Omega$ thì ampe kế là một điện trở nối tiếp, phải cộng vào."),
           (r"$I_A=\dfrac U{R_1+R_2+R_A}$", r"Vôn kế song song với $R_1$ làm đoạn đó nhỏ hơn $R_1$ một chút ; dùng $R_1$ là bỏ qua vôn kế.")]),
  buoc("Số chỉ vôn kế", "Số chỉ của vôn kế là bao nhiêu V?", 2.94, "V", 0.02,
       loi=r"Nhân $I_A$ với $R_V$ thay vì với điện trở của đoạn song song $R_P$.",
       ke=[(r"$U_V=I_AR_P$ (hiệu điện thế hai đầu đoạn song song)", True),
           (r"$U_V=I_AR_V$", r"Dòng qua vôn kế chỉ là một phần rất nhỏ của $I_A$ ; $I_AR_V$ cho giá trị vô lí."),
           (r"$U_V=U$", r"$12\ \text{V}$ là hiệu điện thế cả mạch ; vôn kế chỉ đo hai đầu $R_1$.")]),
  buoc("Số chỉ của vôn kế $6\\ \\Omega$", "Số chỉ của vôn kế $6\\ \\Omega$ là bao nhiêu V?", 1.67, "V", 0.02,
       loi=r"Dùng $R_P=R_1$ như vôn kế lí tưởng, nên vẫn ra gần $2{,}94\ \text{V}$.",
       ke=[(r"Tính lại $R_P'$, $R_{mach}'$, $I_A'$ rồi $U_V'=I_A'R_P'$", True),
           (r"Giữ $I_A$ ở câu a rồi nhân với $R_P'$", r"Vôn kế kém làm $R_{mach}$ đổi nên $I_A$ cũng đổi ; phải tính lại."),
           (r"$U_V'=\dfrac{U_1}2$ vì $R_V=R_1$", r"Điện trở đoạn song song còn một nửa nhưng dòng mạch chính tăng lên nên hiệu điện thế giảm ít hơn một nửa ; phải tính lại cả mạch.")]),
  buoc("Độ lệch so với giá trị thật", "Vôn kế $6\\ \\Omega$ chỉ lệch bao nhiêu phần trăm so với giá trị thật?", 43, "%", 1,
       loi=r"So với $12\ \text{V}$ hoặc so với chính số chỉ thay vì so với giá trị thật khi chưa mắc vôn kế.",
       ke=[(r"$\dfrac{U_1-U_V'}{U_1}$ với $U_1$ khi bỏ vôn kế", True),
           (r"$\dfrac{U_1-U_V'}{U_V'}$", r"Độ lệch đo so với giá trị <em>thật</em> $U_1$, không phải so với số chỉ sai."),
           (r"$\dfrac{U-U_V'}{U}$", r"$U=12\ \text{V}$ là hiệu điện thế cả mạch, không phải giá trị thật trên $R_1$.")]),
  buoc("Độ chia nhỏ nhất của vôn kế", "Độ chia nhỏ nhất của vôn kế thang $0$–$6\\ \\text{V}$ là bao nhiêu V?", 0.2, "V", 0.005,
       loi=r"Chia $6$ cho $6$ hoặc cho số vạch khác ; ĐCNN $=A_{max}/N$.",
       ke=[(r"$\dfrac{A_{max}}N=\dfrac6{30}$", True),
           (r"$\dfrac{N}{A_{max}}$", r"Đảo ngược : ĐCNN là giá trị mỗi vạch, đơn vị V."),
           (r"$\dfrac{A_{max}}{N+1}$", r"$30$ vạch chia đều cho $6\ \text{V}$ nên mỗi vạch $6/30$.")]),
  buoc("Sai số dụng cụ", "Sai số tuyệt đối lớn nhất của phép đo là bao nhiêu V?", 0.06, "V", 0.005,
       loi=r"Lấy $1\%$ của <em>số chỉ</em> $2{,}94\ \text{V}$ (được $0{,}03\ \text{V}$) thay vì của giá trị lớn nhất của thang $6\ \text{V}$.",
       ke=[(r"$\Delta U=x\%\cdot A_{max}$ với $A_{max}$ là cả thang", True),
           (r"$\Delta U=x\%\cdot U_{doc}$", r"Cấp chính xác tính theo giá trị lớn nhất của thang, không theo số chỉ."),
           (r"$\Delta U=\text{ĐCNN}$", r"ĐCNN và sai số dụng cụ là hai đại lượng khác nhau (một là khoảng chia, một là mức sai).")]),
  ]),
]


# ═════════════ BÀI TỰ LUẬN (ví dụ D, luyện E, nâng cao G của nguồn) ═════════════
def L(*lines):
    return "".join(f"<p>{x}</p>" for x in lines)


TL = [
 ("Dễ", L(r"Dòng điện không đổi $I=1{,}2\ \text{A}$ chạy qua một dây dẫn trong $15$ phút. a) Tính điện lượng chuyển qua tiết diện dây. b) Muốn có điện lượng $900\ \text{C}$ với dòng $0{,}5\ \text{A}$ thì cần bao lâu?"),
        L(r"a) $t=15\cdot60=900\ \text{s}$ ; $q=It=1{,}2\cdot900=1080\ \text{C}$.", r"b) $t'=\dfrac{q'}{I'}=\dfrac{900}{0{,}5}=1800\ \text{s}=30$ phút.")),
 ("Dễ", L(r"Dây đồng chất, tiết diện đều có $R=24\ \Omega$. Cắt dây thành hai đoạn bằng nhau. Tính điện trở mỗi đoạn và điện trở khi nối hai đoạn song song."),
        L(r"Mỗi đoạn $\dfrac{24}2=12\ \Omega$.", r"Song song : $\dfrac{12}2=6\ \Omega$ (hay $R/4$).")),
 ("Dễ", L(r"Điện trở $R_1=15\ \Omega$ mắc nối tiếp với $R_2$. Đặt vào hai đầu đoạn mạch $12\ \text{V}$ thì dòng là $0{,}4\ \text{A}$. Tính $R_2$ và hiệu điện thế hai đầu $R_2$."),
        L(r"$R_{td}=\dfrac{12}{0{,}4}=30\ \Omega$ nên $R_2=30-15=15\ \Omega$.", r"$U_2=IR_2=0{,}4\cdot15=6\ \text{V}$.")),
 ("Dễ", L(r"Đồ thị $U$–$I$ của một vật dẫn là đường thẳng qua gốc toạ độ và điểm $I=0{,}6\ \text{A}$, $U=2{,}4\ \text{V}$. Tính điện trở. Nếu tăng hiệu điện thế lên $3{,}6\ \text{V}$ thì dòng bằng bao nhiêu?"),
        L(r"$R=\dfrac{2{,}4}{0{,}6}=4\ \Omega$.", r"$I'=\dfrac{3{,}6}{4}=0{,}9\ \text{A}$.")),
 ("Trung bình", L(r"Dây dài $50\ \text{m}$, tiết diện $0{,}1\ \text{mm}^2$ có $R=8{,}5\ \Omega$. Tính điện trở suất và cho biết đó có thể là vật liệu gì."),
        L(r"$S=0{,}1\cdot10^{-6}=10^{-7}\ \text{m}^2$.", r"$\rho=\dfrac{RS}{l}=\dfrac{8{,}5\cdot10^{-7}}{50}=1{,}7\cdot10^{-8}\ \Omega\cdot\text{m}$.", r"Đây là điện trở suất của đồng.")),
 ("Trung bình", L(r"Dây đồng chất, tiết diện đều dài $4\ \text{m}$ có $R=20\ \Omega$. Phải cắt bớt bao nhiêu mét để đoạn còn lại có $R=15\ \Omega$?"),
        L(r"$R\propto l$ : $l'=4\cdot\dfrac{15}{20}=3\ \text{m}$.", r"Cắt bớt $4-3=1\ \text{m}$.")),
 ("Trung bình", L(r"Dây nhôm dài $120\ \text{m}$, đường kính tiết diện $0{,}8\ \text{mm}$, $\rho=2{,}8\cdot10^{-8}\ \Omega\cdot\text{m}$. Tính điện trở của dây."),
        L(r"$S=\dfrac{\pi d^2}4=\dfrac{3{,}14\cdot(8\cdot10^{-4})^2}4\approx5{,}02\cdot10^{-7}\ \text{m}^2$.", r"$R=\dfrac{\rho l}S=\dfrac{2{,}8\cdot10^{-8}\cdot120}{5{,}02\cdot10^{-7}}\approx6{,}7\ \Omega$.")),
 ("Trung bình", L(r"Kéo dãn một dây dẫn đồng chất, tiết diện đều sao cho đường kính còn một nửa (thể tích không đổi). Điện trở tăng bao nhiêu lần?"),
        L(r"Đường kính giảm $2$ lần thì $S$ giảm $4$ lần, $l$ tăng $4$ lần.", r"$R$ tăng $4^2=16$ lần (hay $k^4=2^4$).")),
 ("Trung bình", L(r"Từ $1\ \text{kg}$ đồng ($D=8900\ \text{kg/m}^3$) kéo thành sợi dây đường kính $0{,}5\ \text{mm}$. Tính chiều dài sợi dây."),
        L(r"$V=\dfrac mD=\dfrac1{8900}\approx1{,}12\cdot10^{-4}\ \text{m}^3$.", r"$S=\dfrac{\pi d^2}4\approx1{,}96\cdot10^{-7}\ \text{m}^2$.", r"$l=\dfrac VS\approx572\ \text{m}$ (dùng $\pi=3{,}14$ được $573\ \text{m}$ ; cả hai chấp nhận được).")),
 ("Khó", L(r"Hai dây cùng chiều dài $40\ \text{m}$ nối tiếp nhau : dây đồng ($\rho=1{,}7\cdot10^{-8}\ \Omega\cdot\text{m}$) tiết diện $1\ \text{mm}^2$ và dây nhôm ($\rho=2{,}8\cdot10^{-8}\ \Omega\cdot\text{m}$) tiết diện $2{,}5\ \text{mm}^2$. a) Tính điện trở mỗi dây và của cả đoạn. b) Vì sao nhôm dẫn điện kém hơn mà dây nhôm này lại có điện trở nhỏ hơn? c) Đặt $6\ \text{V}$ vào hai đầu đoạn nối tiếp, tính hiệu điện thế mỗi dây."),
        L(r"a) $R_1=\dfrac{1{,}7\cdot10^{-8}\cdot40}{10^{-6}}=0{,}68\ \Omega$ ; $R_2=\dfrac{2{,}8\cdot10^{-8}\cdot40}{2{,}5\cdot10^{-6}}=0{,}448\ \Omega$ ; $R_{td}=1{,}128\ \Omega$.",
          r"b) $\dfrac{R_1}{R_2}=\dfrac{\rho_1}{\rho_2}\cdot\dfrac{S_2}{S_1}=\dfrac{1{,}7}{2{,}8}\cdot2{,}5\approx1{,}52$ : tiết diện lớn hơn $2{,}5$ lần bù được $\rho$ lớn hơn $1{,}65$ lần.",
          r"c) $I=\dfrac6{1{,}128}\approx5{,}32\ \text{A}$ ; $U_1\approx3{,}62\ \text{V}$ ; $U_2\approx2{,}38\ \text{V}$ ; tổng $6{,}00\ \text{V}$ ✓.")),
 ("Khó", L(r"Mạch gồm nguồn $9\ \text{V}$, ampe kế có $R_A=0{,}5\ \Omega$ nối tiếp với điện trở $R$ và một vôn kế lí tưởng song song với $R$. Ampe kế chỉ $0{,}5\ \text{A}$, vôn kế chỉ $8{,}75\ \text{V}$. Tính $R$. Nếu vôn kế thật có $R_V=100\ \Omega$ thì số chỉ vôn kế bằng bao nhiêu?"),
        L(r"$R=\dfrac{8{,}75}{0{,}5}=17{,}5\ \Omega$. Kiểm : $0{,}5\cdot(17{,}5+0{,}5)=9\ \text{V}$ ✓.", r"$R_P=\dfrac{17{,}5\cdot100}{117{,}5}\approx14{,}89\ \Omega$ ; $I=\dfrac9{14{,}89+0{,}5}\approx0{,}585\ \text{A}$.", r"$U_V=IR_P\approx8{,}71\ \text{V}$ : thấp hơn $8{,}75\ \text{V}$ khoảng $0{,}5\%$.")),
 ("Nâng cao", L(r"Mạch như Dạng 5 ($U=24\ \text{V}$, $R=30\ \Omega$, $R_{max}=50\ \Omega$). Muốn dòng nhỏ nhất điều chỉnh được xuống $0{,}2\ \text{A}$, nêu hai cách (có tính toán)."),
        L(r"Cách 1 : thêm $R'$ nối tiếp : $\dfrac{24}{50+30+R'}=0{,}2$ nên $R'=40\ \Omega$.", r"Cách 2 : hạ nguồn : $\dfrac{U'}{80}=0{,}2$ nên $U'=16\ \text{V}$.")),
 ("Nâng cao", L(r"Biến trở bằng nicrom có $R_0=50\ \Omega$ ở $20\ ^\circ\text{C}$, $\alpha=2\cdot10^{-4}\ \text{K}^{-1}$, mắc nối tiếp với $10\ \Omega$ vào $12\ \text{V}$. Dây nóng lên $120\ ^\circ\text{C}$. a) Tính điện trở dây lúc nóng. b) Dòng điện giảm bao nhiêu phần trăm? c) Mắc thêm ampe kế $R_A=0{,}6\ \Omega$ (dây vẫn $120\ ^\circ\text{C}$) : số chỉ ampe kế và sai số tương đối so với khi chưa mắc."),
        L(r"a) $R=50\,[1+2\cdot10^{-4}\cdot100]=51\ \Omega$.", r"b) $I_1=\dfrac{12}{60}=0{,}2\ \text{A}$ ; $I_2=\dfrac{12}{61}\approx0{,}1967\ \text{A}$ ; giảm $\dfrac{0{,}2-0{,}1967}{0{,}2}\approx1{,}64\%$.",
          r"c) $I_A=\dfrac{12}{61{,}6}\approx0{,}1948\ \text{A}$ ; $\delta=\dfrac{0{,}1967-0{,}1948}{0{,}1967}\approx0{,}97\%$ (cũng bằng $\dfrac{R_A}{R_{mach}+R_A}=\dfrac{0{,}6}{61{,}6}$).")),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))


# ═════════════ TỰ KIỂM SỐ LIỆU (độc lập với chữ trong đề) ═════════════
def kiem_so():
    pi = math.pi
    # D1
    R = 2.8e-8 * 200 / 0.5e-6; assert abs(R - 11.2) < 1e-9
    Scu = 1.7e-8 * 200 / R * 1e6; assert abs(Scu - 0.3036) < 1e-3 and abs(1.7 / 2.8 * 0.5 - Scu) < 1e-9
    d = math.sqrt(4 * Scu / pi); assert abs(d - 0.62) < 0.01 and abs(5.6 / R - 0.5) < 1e-9
    # D2
    assert Fr(90, 3) == 30 and Fr(30, 3) == 10 and Fr(90, 9) == 10 and Fr(6, 10) == Fr(3, 5) and Fr(6, 30) == Fr(1, 5)
    assert 90 / 10 ** 2 == 0.9 and Fr(9, 10) == Fr(9, 10) and 3 * Fr(1, 5) == Fr(3, 5)
    # D3
    assert Fr(3, 2) ** 2 * 20 == 45 and Fr(1, 2) ** 2 == Fr(1, 4) and 16 * 45 == 720 and 720 / 20 == 36 and Fr(9, 4) * 16 == 36
    V = 0.178 / 8900; l = V / 5e-7; assert abs(V - 2e-5) < 1e-12 and abs(l - 40) < 1e-6 and abs(1.7e-8 * l / 5e-7 - 1.36) < 1e-9
    # D4
    assert Fr(30, 5) == 6 and Fr(45, 5) == 9 and Fr(6 * 9, 15) == Fr(18, 5) and Fr(9, 2) / Fr(18, 5) == Fr(5, 4)
    assert Fr(9, 2) / 6 + Fr(9, 2) / 9 == Fr(5, 4) and Fr(6, 15) == Fr(2, 5) and Fr(2, 5) * 6 == Fr(12, 5) and Fr(2, 5) * 9 == Fr(18, 5)
    assert abs(1 / 6 - 0.167) < 1e-3 and abs(1 / 9 - 0.111) < 1e-3
    # D5
    assert Fr(24, 80) == Fr(3, 10) and Fr(24, 30) == Fr(4, 5) and Fr(24) / Fr(3, 5) == 40 and 24 / 0.6 - 30 == 10 and Fr(10, 50) == Fr(1, 5)
    S = pi * (4e-4) ** 2 / 4; lw = 50 * S / 1.1e-6; N = lw / (pi * 2e-2)
    assert abs(S - 1.2566e-7) < 1e-10 and abs(lw - 5.71) < 0.01 and abs(N - 90.9) < 0.1 and round(N) == 91
    assert Fr(24, 50 + 30 + 40) == Fr(1, 5) and Fr(16, 80) == Fr(1, 5)
    # D6
    RP = 6 * 4000 / 4006; Rm = RP + 18 + 0.5; I = 12 / Rm; UV = I * RP
    assert abs(RP - 5.991) < 1e-3 and abs(I - 0.490) < 1e-3 and abs(UV - 2.9355) < 1e-3
    U1 = 12 * 6 / 24.5; assert abs(U1 - 2.9388) < 1e-3
    I2 = 12 / 21.5; UV2 = I2 * 3; assert abs(I2 - 0.558) < 1e-3 and abs(UV2 - 1.674) < 1e-3 and abs((U1 - UV2) / U1 - 0.430) < 2e-3
    assert Fr(6, 30) == Fr(1, 5) and abs(0.01 * 6 - 0.06) < 1e-12 and abs(0.06 / 2.94 - 0.0204) < 1e-3
    # tự luận
    assert 1.2 * 900 == 1080 and 900 / 0.5 == 1800 and Fr(24, 2) == 12 and Fr(12, 2) == 6 and Fr(12) / Fr(2, 5) == 30
    assert abs(2.4 / 0.6 - 4) < 1e-9 and abs(3.6 / 4 - 0.9) < 1e-9 and abs(8.5e-7 / 50 - 1.7e-8) < 1e-12 and 4 * 15 / 20 == 3
    R10 = 2.8e-8 * 120 / (pi * (8e-4) ** 2 / 4); assert abs(R10 - 6.68) < 0.02
    l4 = (1 / 8900) / (pi * (5e-4) ** 2 / 4); assert abs(l4 - 572.2) < 0.5
    R1 = 1.7e-8 * 40 / 1e-6; R2 = 2.8e-8 * 40 / 2.5e-6; Ig = 6 / (R1 + R2)
    assert abs(R1 - 0.68) < 1e-9 and abs(R2 - 0.448) < 1e-9 and abs(Ig - 5.319) < 1e-3 and abs(Ig * R1 - 3.617) < 1e-3 and abs(Ig * R2 - 2.383) < 1e-3 and abs(R1 / R2 - 1.518) < 1e-3
    Rx = 8.75 / 0.5; assert Rx == 17.5 and abs(0.5 * (Rx + 0.5) - 9) < 1e-9
    RPx = Rx * 100 / 117.5; Ix = 9 / (RPx + 0.5); assert abs(Ix * RPx - 8.708) < 1e-2 and abs((8.75 - Ix * RPx) / 8.75 - 0.0048) < 2e-4
    Rt = 50 * (1 + 2e-4 * 100); assert abs(Rt - 51) < 1e-9
    I1, I2t = 12 / 60, 12 / 61; assert abs((I1 - I2t) / I1 - 0.01639) < 1e-4
    IA = 12 / 61.6; assert abs(IA - 0.19481) < 1e-4 and abs((I2t - IA) / I2t - 0.0097) < 1e-4 and abs(0.6 / 61.6 - 0.0097) < 1e-4
    print("kiểm số liệu: đạt")


kiem_so()

# ═════════════ GHI FILE ═════════════
write(J, 159, "Chuyên đề 03. Điện trở và định luật Ohm", DANG, BUILD, ANALYSIS, SOLS, tu_luan())
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-12"
d["review"] = {"checked": False, "notes": "Soạn 12/10/2026 (lesson_id 159). Chờ kiểm chéo độc lập (kiem-code): tự giải từng dạng + kiểm buoc[]."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
