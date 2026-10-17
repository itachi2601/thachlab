# -*- coding: utf-8 -*-
"""CĐ04 Đoạn mạch nối tiếp, song song, hỗn hợp (lesson 157) — sinh luyen-tap/bundle.json
(8 câu tự chấm: 4 Phần I, 2 Phần II, 2 Phần III). Chỉ có khối exam (theory_html rỗng, worked_examples []).
Số liệu tính bằng Python + assert; mỗi phương án nhiễu ứng với một cách sai cụ thể và khác đáp án đúng.
Nguồn lí tưởng, ampe kế/vôn kế lí tưởng, bỏ qua điện trở dây nối. Số liệu khác bài tập mẫu (157.json) và nguon.md.
Chạy: python3 content/hsg9/cd04-mach-noi-tiep-song-song/luyen-tap/sinh.py"""
import json
from fractions import Fraction as F
from pathlib import Path

T_NS = "Đoạn mạch nối tiếp và song song"
T_HH = "Mạch hỗn hợp"
T_CB = "Mạch cầu cân bằng"
T_CT = "Công tắc, biến trở và cực trị"


def vn(x, nd=1):
    """Số kiểu Việt Nam: dấu phẩy thập phân, bỏ ,0 thừa."""
    s = f"{float(x):.{nd}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def par(a, b):
    return F(a) * F(b) / (F(a) + F(b))


def mc(question, correct, wrongs, pos, explanation, topic, form, diff):
    """wrongs: list 3 (text, note). correct được chèn vào vị trí pos."""
    assert len(wrongs) == 3
    opts = [w[0] for w in wrongs]
    opts.insert(pos, correct)
    assert len(set(opts)) == 4, opts
    notes = {}
    wi = iter(wrongs)
    for i in range(4):
        if i != pos:
            notes["ABCD"[i]] = next(wi)[1]
    return dict(type="multiple_choice", question=question, options=opts, answer=pos,
                explanation=explanation, topic=topic, form=form, difficulty=diff, distractorNotes=notes)


O = r"\ \Omega"
Q = []

# ── Câu 1 · Phần I · hai điện trở song song (đáp án C)
a1, b1 = 14, 21
r1 = par(a1, b1)
assert r1 == F(42, 5)
Q.append(mc(
    "<p>Hai điện trở $R_1=14\\ \\Omega$ và $R_2=21\\ \\Omega$ được mắc song song với nhau. Điện trở tương đương của đoạn mạch là</p>",
    f"${vn(r1)}{O}$.",
    [(f"${vn(F(a1 + b1, 2))}{O}$.", "Lấy trung bình cộng hai điện trở."),
     (f"${a1 + b1}{O}$.", "Dùng công thức của đoạn mạch nối tiếp (cộng hai điện trở)."),
     (f"${a1 * b1}{O}$.", "Lấy tích $R_1R_2$ mà quên chia cho tổng $R_1+R_2$.")],
    2,
    "<p>Hai điện trở song song: $\\dfrac{1}{R_{td}}=\\dfrac{1}{14}+\\dfrac{1}{21}=\\dfrac{3+2}{42}=\\dfrac{5}{42}$, nên $R_{td}=\\dfrac{14\\cdot21}{14+21}=\\dfrac{294}{35}=8{,}4\\ \\Omega$. Đáp án C.</p>"
    "<p>Kiểm tra nhanh: điện trở tương đương của đoạn song song luôn nhỏ hơn điện trở nhỏ nhất ($14\\ \\Omega$), nên $17{,}5$, $35$ và $294$ đều không thể đúng.</p>",
    T_NS, "ly_thuyet", "de"))

# ── Câu 2 · Phần I · R1 nối tiếp (R2 // R3), dòng qua R2 (đáp án A)
R1, R2, R3, U2 = 9, 24, 40, 48
p = par(R2, R3)
Rt = R1 + p
I = F(U2) / Rt
Up = I * p
i2, i3 = Up / R2, Up / R3
assert p == 15 and Rt == 24 and I == 2 and Up == 30 and i2 == F(5, 4) and i3 == F(3, 4) and i2 + i3 == I
Q.append(mc(
    "<p>Đoạn mạch gồm điện trở $R_1=9\\ \\Omega$ mắc nối tiếp với đoạn gồm $R_2=24\\ \\Omega$ song song $R_3=40\\ \\Omega$, đặt vào hiệu điện thế không đổi $48\\ \\text{V}$. Cường độ dòng điện qua $R_2$ là</p>",
    f"${vn(i2, 2)}\\ \\text{{A}}$.",
    [(f"${vn(i3, 2)}\\ \\text{{A}}$.", "Tính ra dòng qua $R_3$ (đảo hai nhánh) chứ không phải qua $R_2$."),
     (f"${vn(I / 2, 2)}\\ \\text{{A}}$.", "Cho rằng dòng mạch chính chia đều cho hai nhánh song song."),
     (f"${vn(I, 2)}\\ \\text{{A}}$.", "Lấy luôn cường độ dòng điện mạch chính làm dòng qua $R_2$.")],
    0,
    "<p>Đoạn song song: $R_{23}=\\dfrac{24\\cdot40}{24+40}=15\\ \\Omega$. Toàn mạch: $R_{td}=9+15=24\\ \\Omega$, nên $I=\\dfrac{48}{24}=2\\ \\text{A}$.</p>"
    "<p>Hiệu điện thế hai đầu đoạn song song: $U_{23}=I\\cdot R_{23}=2\\cdot15=30\\ \\text{V}$ (cũng là hiệu điện thế hai đầu $R_2$ và $R_3$).</p>"
    "<p>$I_2=\\dfrac{30}{24}=1{,}25\\ \\text{A}$. Đáp án A. Kiểm tra: $I_3=\\dfrac{30}{40}=0{,}75\\ \\text{A}$ và $1{,}25+0{,}75=2\\ \\text{A}$ khớp với dòng mạch chính.</p>",
    T_HH, "bai_tap", "trung-binh"))

# ── Câu 3 · Phần I · khoá K nối tắt R2 (đáp án D)
U3, Ra, Rb_ = 40, 10, 30
I_mo = F(U3, Ra + Rb_)
I_dong = F(U3, Ra)
s_nham = F(U3, Rb_)
assert I_mo == 1 and I_dong == 4 and round(float(s_nham), 1) == 1.3
Q.append(mc(
    "<p>Mạch điện gồm điện trở $R_1=10\\ \\Omega$ nối tiếp với điện trở $R_2=30\\ \\Omega$, nối với nguồn có hiệu điện thế không đổi $40\\ \\text{V}$ qua ampe kế lí tưởng. Khoá K mắc song song với $R_2$. Ban đầu K mở. Sau khi đóng K, số chỉ của ampe kế là</p>",
    "$4{,}0\\ \\text{A}$.",
    [("$0\\ \\text{A}$.", "Cho rằng đóng khoá là làm hở mạch nên không còn dòng điện."),
     (f"${vn(I_mo)}\\ \\text{{A}}$.", "Cho rằng đóng K không làm đổi cường độ dòng điện (vẫn là số chỉ lúc K mở)."),
     (f"${vn(s_nham)}\\ \\text{{A}}$.", "Nối tắt nhầm $R_1$ thay vì $R_2$ nên chỉ còn $R_2$ trong mạch.")],
    3,
    "<p>K mở: $I=\\dfrac{40}{10+30}=1\\ \\text{A}$.</p>"
    "<p>K đóng: K có điện trở bằng $0$ và song song với $R_2$ nên $R_2$ bị nối tắt (không có dòng điện qua $R_2$). Mạch chỉ còn $R_1$: $I=\\dfrac{40}{10}=4\\ \\text{A}$. Đáp án D.</p>"
    "<p>Đóng khoá làm điện trở tương đương giảm từ $40\\ \\Omega$ xuống $10\\ \\Omega$ nên dòng điện tăng gấp $4$ lần.</p>",
    T_CT, "bai_tap", "trung-binh"))

# ── Câu 4 · Phần I · mạch cầu cân bằng, R5 giữa P và Q (đáp án B)
c1, c3, c2, c4, c5 = 9, 15, 6, 10, 8
assert F(c1, c2) == F(c3, c4)
Rb4 = (c1 + c3) * (c2 + c4) / F(c1 + c3 + c2 + c4)
Rchap = par(c1, c2) + par(c3, c4)
assert Rb4 == F(48, 5) == Rchap
s_ns = Rb4 + c5
s_sai = F((c1 + c2) * (c3 + c4), c1 + c2 + c3 + c4)
assert round(float(s_sai), 1) == 9.4 and s_ns == F(88, 5)
Q.append(mc(
    "<p>Giữa hai điểm M và N có hai nhánh song song: nhánh trái gồm $R_1=9\\ \\Omega$ nối tiếp $R_3=15\\ \\Omega$ (điểm nối là P); nhánh phải gồm $R_2=6\\ \\Omega$ nối tiếp $R_4=10\\ \\Omega$ (điểm nối là Q); $R_1$ và $R_2$ cùng nối với M, $R_3$ và $R_4$ cùng nối với N. Mắc thêm điện trở $R_5=8\\ \\Omega$ vào giữa P và Q. Điện trở tương đương giữa M và N là</p>",
    f"${vn(Rb4)}{O}$.",
    [(f"${vn(s_ns)}{O}$.", "Cộng thêm $R_5$ nối tiếp vào mạch, trong khi $R_5$ không nằm trên đường đi chung của dòng."),
     (f"${c1 + c3 + c2 + c4}{O}$.", "Cộng cả bốn điện trở như nối tiếp, không nhìn ra hai nhánh song song."),
     (f"${vn(s_sai)}{O}$.", "Ghép sai: lấy $(R_1+R_2)$ song song $(R_3+R_4)$ thay vì $(R_1+R_3)$ song song $(R_2+R_4)$.")],
    1,
    "<p>Kiểm tra cân bằng: $\\dfrac{R_1}{R_2}=\\dfrac{9}{6}=1{,}5$ và $\\dfrac{R_3}{R_4}=\\dfrac{15}{10}=1{,}5$, hai tỉ số bằng nhau nên hai điểm P và Q cùng điện thế.</p>"
    "<p>Không có hiệu điện thế giữa P và Q nên $R_5$ không có dòng điện, có thể bỏ $R_5$ ra khỏi mạch. Còn lại hai nhánh $(9+15)=24\\ \\Omega$ và $(6+10)=16\\ \\Omega$ song song: $R_{td}=\\dfrac{24\\cdot16}{24+16}=9{,}6\\ \\Omega$. Đáp án B.</p>"
    "<p>Kiểm tra bằng cách chập P với Q: $\\dfrac{9\\cdot6}{15}+\\dfrac{15\\cdot10}{25}=3{,}6+6=9{,}6\\ \\Omega$, khớp.</p>",
    T_CB, "bai_tap", "kho"))

# ── Câu 5 · Phần II · mạch hỗn hợp, tháo R3
r1_, r2_, r3_, u5 = 5, 20, 30, 51
p5 = par(r2_, r3_)
Rt5 = r1_ + p5
I5 = F(u5) / Rt5
Up5 = I5 * p5
I2_5 = Up5 / r2_
Rt5b = r1_ + r2_
I5b = F(u5, 1) / Rt5b
assert p5 == 12 and Rt5 == 17 and I5 == 3 and Up5 == 36 and I2_5 == F(9, 5)
assert I5b == F(51, 25) and I5b < I5 and I5b > I2_5
Q.append(dict(
    type="true_false",
    question="<p>Điện trở $R_1=5\\ \\Omega$ mắc nối tiếp với đoạn gồm $R_2=20\\ \\Omega$ song song $R_3=30\\ \\Omega$. Đặt vào hai đầu mạch hiệu điện thế không đổi $51\\ \\text{V}$. Ampe kế lí tưởng ở nhánh chính.</p>",
    statements=[
        {"text": "Điện trở tương đương của toàn mạch là $17\\ \\Omega$.", "answer": True},
        {"text": "Cường độ dòng điện qua $R_2$ là $1{,}2\\ \\text{A}$.", "answer": False},
        {"text": "Hiệu điện thế giữa hai đầu $R_3$ là $15\\ \\text{V}$.", "answer": False},
        {"text": "Nếu tháo bỏ $R_3$ thì số chỉ ampe kế giảm, còn dòng điện qua $R_2$ lại tăng lên.", "answer": True},
    ],
    explanation=(
        "<p>a) Đúng: $R_{23}=\\dfrac{20\\cdot30}{50}=12\\ \\Omega$ nên $R_{td}=5+12=17\\ \\Omega$.</p>"
        "<p>b) Sai: $I=\\dfrac{51}{17}=3\\ \\text{A}$, $U_{23}=3\\cdot12=36\\ \\text{V}$ nên $I_2=\\dfrac{36}{20}=1{,}8\\ \\text{A}$. Con số $1{,}2\\ \\text{A}$ là dòng qua $R_3$ ($36/30$).</p>"
        "<p>c) Sai: $R_3$ song song $R_2$ nên chịu $U_3=U_{23}=36\\ \\text{V}$. Giá trị $15\\ \\text{V}$ là hiệu điện thế hai đầu $R_1$ ($3\\cdot5$).</p>"
        "<p>d) Đúng: bỏ $R_3$ thì $R_{td}=5+20=25\\ \\Omega$, $I=\\dfrac{51}{25}=2{,}04\\ \\text{A}<3\\ \\text{A}$ nên ampe kế giảm. Lúc này toàn bộ dòng đi qua $R_2$ nên $I_2=2{,}04\\ \\text{A}>1{,}8\\ \\text{A}$: dòng qua $R_2$ tăng.</p>"),
    topic=T_HH, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "R23 = 20·30/50 = 12 Ω; R_td = 5 + 12 = 17 Ω.",
        "1": "I2 = U23/R2 = 36/20 = 1,8 A; 1,2 A là dòng qua R3 (nhầm nhánh).",
        "2": "R3 song song R2 nên U3 = U23 = 36 V; 15 V là hiệu điện thế trên R1.",
        "3": "Bỏ R3: R_td tăng lên 25 Ω nên I giảm (2,04 A), nhưng cả dòng qua R2 nên I2 tăng từ 1,8 lên 2,04 A.",
    }))

# ── Câu 6 · Phần II · biến trở trong mạch hỗn hợp
u6, q1, q2, rbmax = 45, 15, 30, 60


def kq(rb):
    pp = par(rb, q2) if rb > 0 else F(0)
    i = F(u6) / (q1 + pp)
    return i, i * pp


i0, _ = kq(F(0))
i30, up30 = kq(F(30))
i60, up60 = kq(F(60))
assert i0 == 3 and i30 == F(3, 2) and up30 == F(45, 2) and up60 == F(180, 7)
P1max = i0 ** 2 * q1
assert P1max == 135 and up60 < 28
Q.append(dict(
    type="true_false",
    question="<p>Nguồn $45\\ \\text{V}$ không đổi. Điện trở $R_1=15\\ \\Omega$ mắc nối tiếp với đoạn gồm biến trở $R_b$ (điều chỉnh được từ $0$ đến $60\\ \\Omega$) song song điện trở $R_2=30\\ \\Omega$. Ampe kế lí tưởng ở nhánh chính, vôn kế lí tưởng mắc song song với đoạn song song.</p>",
    statements=[
        {"text": "Khi $R_b=0$ thì ampe kế chỉ $3\\ \\text{A}$.", "answer": True},
        {"text": "Khi $R_b=30\\ \\Omega$ thì vôn kế chỉ $15\\ \\text{V}$.", "answer": False},
        {"text": "Công suất toả nhiệt trên $R_1$ lớn nhất bằng $135\\ \\text{W}$.", "answer": True},
        {"text": "Có thể điều chỉnh $R_b$ để vôn kế chỉ $28\\ \\text{V}$.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: $R_b=0$ làm đoạn song song bị nối tắt (điện trở bằng $0$), mạch chỉ còn $R_1$: $I=\\dfrac{45}{15}=3\\ \\text{A}$, đây cũng là giá trị lớn nhất của dòng điện.</p>"
        "<p>b) Sai: $R_b=30\\ \\Omega$ song song $R_2=30\\ \\Omega$ cho $15\\ \\Omega$; $R_{td}=30\\ \\Omega$, $I=1{,}5\\ \\text{A}$, vôn kế chỉ $1{,}5\\cdot15=22{,}5\\ \\text{V}$ (giá trị $15\\ \\text{V}$ là hiệu điện thế trên $R_1$).</p>"
        "<p>c) Đúng: $P_1=I^2R_1$ lớn nhất khi $I$ lớn nhất, tức $R_b=0$: $P_1=3^2\\cdot15=135\\ \\text{W}$.</p>"
        "<p>d) Sai: $R_b$ càng lớn thì đoạn song song càng lớn nên vôn kế càng chỉ nhiều. Lớn nhất khi $R_b=60\\ \\Omega$: đoạn song song $20\\ \\Omega$, $R_{td}=35\\ \\Omega$, $I=\\dfrac{9}{7}\\ \\text{A}$, $U_{\\max}=\\dfrac{9}{7}\\cdot20\\approx25{,}7\\ \\text{V}<28\\ \\text{V}$ nên không thể đạt $28\\ \\text{V}$.</p>"),
    topic=T_CT, form="bai_tap", difficulty="kho",
    distractorNotes={
        "0": "R_b = 0 nối tắt đoạn song song, chỉ còn R1: I = 45/15 = 3 A.",
        "1": "Vôn kế đo hiệu điện thế đoạn song song = 1,5·15 = 22,5 V; 15 V là hiệu điện thế trên R1.",
        "2": "P1 = I²R1 lớn nhất khi I lớn nhất (R_b = 0): 3²·15 = 135 W.",
        "3": "Vôn kế chỉ lớn nhất khi R_b = 60 Ω, bằng 180/7 ≈ 25,7 V < 28 V.",
    }))

# ── Câu 7 · Phần III · khoá K nối tiếp nhánh R3, tìm R3
u7, r2_7, ik_mo, ik_dong = 60, 30, F(6, 5), F(3, 2)
r1_7 = F(u7) / ik_mo - r2_7
rtd_dong = F(u7) / ik_dong
r23 = rtd_dong - r1_7
r3_7 = 1 / (1 / r23 - F(1, r2_7))
assert r1_7 == 20 and rtd_dong == 40 and r23 == 20 and r3_7 == 60
Q.append(dict(
    type="short_answer",
    question="<p>Điện trở $R_1$ nối tiếp với đoạn gồm $R_2=30\\ \\Omega$ song song với nhánh có khoá K nối tiếp điện trở $R_3$. Nguồn có hiệu điện thế không đổi $60\\ \\text{V}$; ampe kế lí tưởng ở nhánh chính. Khi K mở ampe kế chỉ $1{,}2\\ \\text{A}$, khi K đóng ampe kế chỉ $1{,}5\\ \\text{A}$. Tính $R_3$ (đơn vị $\\Omega$).</p>",
    answer="60",
    explanation=(
        "<p>K mở: nhánh chứa $R_3$ bị cắt, mạch chỉ gồm $R_1$ nối tiếp $R_2$: $R_1+R_2=\\dfrac{60}{1{,}2}=50\\ \\Omega$ nên $R_1=20\\ \\Omega$.</p>"
        "<p>K đóng: $R_{td}=\\dfrac{60}{1{,}5}=40\\ \\Omega$, suy ra đoạn song song $R_{23}=40-20=20\\ \\Omega$.</p>"
        "<p>$\\dfrac{1}{R_3}=\\dfrac{1}{20}-\\dfrac{1}{30}=\\dfrac{1}{60}$ nên $R_3=60\\ \\Omega$.</p>"
        "<p>Kiểm tra: $\\dfrac{30\\cdot60}{90}=20\\ \\Omega$, $R_{td}=40\\ \\Omega$, $I=1{,}5\\ \\text{A}$ khớp.</p>"
        "<p>Bẫy: lấy $R_{23}=20\\ \\Omega$ làm luôn $R_3$ (quên rằng $R_2$ cũng nằm trong đoạn song song).</p>"),
    topic=T_CT, form="bai_tap", difficulty="trung-binh"))

# ── Câu 8 · Phần III · cực trị: dây chia hai đoạn song song, nối tiếp R0
Rday, R0, u8 = 120, 25, 55
rp_max = F(Rday, 4)
Rtd_max = R0 + rp_max
Imin = F(u8) / Rtd_max
assert rp_max == 30 and Rtd_max == 55 and Imin == 1
for x in range(1, Rday):
    assert F(x * (Rday - x), Rday) <= rp_max
Q.append(dict(
    type="short_answer",
    question="<p>Một dây dẫn đồng chất có điện trở $120\\ \\Omega$ được cắt thành hai đoạn có điện trở $x$ và $(120-x)$ (đơn vị ôm, $0\\lt x\\lt120$). Hai đoạn mắc song song với nhau, rồi mắc nối tiếp với điện trở $R_0=25\\ \\Omega$ vào nguồn có hiệu điện thế không đổi $55\\ \\text{V}$. Khi thay đổi cách cắt (thay đổi $x$), cường độ dòng điện chạy qua nguồn có giá trị nhỏ nhất bằng bao nhiêu ampe?</p>",
    answer="1",
    explanation=(
        "<p>Đoạn song song: $R_p=\\dfrac{x(120-x)}{120}$. Với tổng $x+(120-x)=120$ không đổi, tích $x(120-x)\\le\\left(\\dfrac{120}{2}\\right)^2=3600$, dấu bằng khi $x=60\\ \\Omega$.</p>"
        "<p>Vậy $R_{p,\\max}=\\dfrac{3600}{120}=30\\ \\Omega$.</p>"
        "<p>$I=\\dfrac{55}{25+R_p}$ nhỏ nhất khi $R_p$ lớn nhất: $I_{\\min}=\\dfrac{55}{25+30}=1\\ \\text{A}$ (khi $x=60\\ \\Omega$).</p>"
        "<p>Bẫy: lấy $R_p=\\dfrac{120}{2}=60\\ \\Omega$ (nhầm là điện trở một đoạn) cho $I\\approx0{,}65\\ \\text{A}$; hoặc lấy $R_p=x+(120-x)=120\\ \\Omega$ như thể hai đoạn mắc nối tiếp.</p>"),
    topic=T_CT, form="bai_tap", difficulty="kho"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) == [0, 1, 2, 3]
for q in Q[6:]:
    assert len(q["answer"]) <= 4
for q in Q:
    assert q["topic"] in (T_NS, T_HH, T_CB, T_CT)
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 for ch in s), s

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Đoạn mạch nối tiếp, song song và mạch hỗn hợp",
        "topic": T_HH,
        "difficulty": "trung-binh",
        "duration_minutes": 25,
        "subject_code": "hsg-vat-ly",
        "questions": Q,
    },
}
out = Path(__file__).with_name("bundle.json")
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ghi", out, len(Q), "câu; đáp án:",
      ["ABCD"[q["answer"]] if q["type"] == "multiple_choice" else
       ("".join("Đ" if s["answer"] else "S" for s in q["statements"]) if q["type"] == "true_false" else q["answer"])
       for q in Q])
