# -*- coding: utf-8 -*-
"""CĐ03 Điện trở và định luật Ohm (lesson 159) — sinh luyen-tap/bundle.json (8 câu tự chấm: 4 Phần I, 2 Phần II, 2 Phần III).
Chỉ có khối exam (theory_html rỗng, worked_examples []) để upload-lesson.mts giữ nguyên lý thuyết và bài tập mẫu.
Số liệu tính bằng Python + assert; mỗi phương án nhiễu ứng với một cách sai cụ thể và khác đáp án đúng.
Số liệu khác bài tập mẫu (159.json) và khác ví dụ trong nguon.md.
Chạy: python3 content/hsg9/cd03-dien-tro-dinh-luat-ohm/luyen-tap/sinh.py"""
import json
import math
from fractions import Fraction as F
from pathlib import Path

T_OHM = "Định luật Ohm và đồ thị U–I"
T_RHO = "Điện trở phụ thuộc kích thước và vật liệu dây dẫn"
T_CAT = "Cắt dây, kéo dãn dây"
T_BT = "Biến trở"
T_DUNG = "Ampe kế, vôn kế có điện trở"


def vn(x, nd=1):
    """Số kiểu Việt Nam: dấu phẩy thập phân, bỏ ,0 thừa."""
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def mc(question, options, answer, explanation, topic, form, diff, notes):
    assert len(options) == 4 and len(set(options)) == 4, options
    assert set(notes) == {"ABCD"[i] for i in range(4) if i != answer}
    return dict(type="multiple_choice", question=question, options=options, answer=answer,
                explanation=explanation, topic=topic, form=form, difficulty=diff, distractorNotes=notes)


Q = []

# ── Câu 1 · Phần I · bản chất R = U/I (đáp án C)
Q.append(mc(
    "<p>Một sợi dây kim loại được giữ ở nhiệt độ không đổi. Đặt vào hai đầu dây hiệu điện thế $6\\ \\text{V}$ thì cường độ dòng điện là $0{,}3\\ \\text{A}$. Phát biểu nào sau đây đúng khi tăng hiệu điện thế lên $9\\ \\text{V}$?</p>",
    ["Điện trở của dây tăng lên vì $R=\\dfrac{U}{I}$ và $U$ tăng.",
     "Điện trở của dây giảm đi vì cường độ dòng điện tăng.",
     "Cường độ dòng điện tăng lên $0{,}45\\ \\text{A}$, còn điện trở của dây vẫn là $20\\ \\Omega$.",
     "Cường độ dòng điện vẫn là $0{,}3\\ \\text{A}$ vì điện trở của dây không đổi."],
    2,
    "<p>Điện trở $R=\\dfrac{6}{0{,}3}=20\\ \\Omega$ chỉ phụ thuộc vật liệu, kích thước và nhiệt độ của dây. Nhiệt độ không đổi nên $R$ không đổi.</p>"
    "<p>Theo định luật Ohm, $I=\\dfrac{U}{R}=\\dfrac{9}{20}=0{,}45\\ \\text{A}$. Đáp án C.</p>"
    "<p>A và B hiểu $R=\\dfrac{U}{I}$ như quan hệ phụ thuộc: $U$ và $I$ đổi theo cùng tỉ lệ, thương số của chúng giữ nguyên.</p>"
    "<p>D sai vì $R$ không đổi thì $I$ phải tăng theo $U$.</p>",
    T_OHM, "ly_thuyet", "de",
    {"A": "Hiểu công thức R = U/I như R tỉ lệ với U; thực tế U tăng thì I tăng theo, thương số không đổi.",
     "B": "Hiểu R tỉ lệ nghịch với I; R là đặc trưng của vật dẫn, không đổi theo I.",
     "D": "Cho rằng R không đổi thì I không đổi; phải có I = U/R tăng theo U."}))

# ── Câu 2 · Phần I · R = ρl/S từ đường kính (đáp án B)
rho2, l2, d2 = F(5, 10) * F(1, 10**6), 15, F(3, 10) * F(1, 10**3)
S2 = math.pi * float(d2) ** 2 / 4
R2 = float(rho2) * l2 / S2
s_pid2 = float(rho2) * l2 / (math.pi * float(d2) ** 2)            # S = πd²
s_sq = float(rho2) * l2 / float(d2) ** 2                          # S = d²
s_half = float(rho2) * l2 / (math.pi * float(d2) ** 2 / 2)        # S = πd²/2
assert round(R2) == 106 and round(s_pid2) == 27 and round(s_sq) == 83 and round(s_half) == 53
opts2 = sorted([round(R2), round(s_pid2), round(s_sq), round(s_half)])
assert len(set(opts2)) == 4
Q.append(mc(
    "<p>Dây constantan có điện trở suất $\\rho=0{,}5\\cdot10^{-6}\\ \\Omega\\cdot\\text{m}$, dài $15\\ \\text{m}$, tiết diện tròn, đường kính $0{,}3\\ \\text{mm}$. Điện trở của dây xấp xỉ</p>",
    [f"${x}\\ \\Omega$." for x in opts2],
    opts2.index(round(R2)),
    "<p>Tiết diện: $S=\\dfrac{\\pi d^2}{4}=\\dfrac{\\pi\\,(0{,}3\\cdot10^{-3})^2}{4}\\approx7{,}07\\cdot10^{-8}\\ \\text{m}^2$.</p>"
    "<p>$R=\\rho\\dfrac{l}{S}=0{,}5\\cdot10^{-6}\\cdot\\dfrac{15}{7{,}07\\cdot10^{-8}}\\approx106\\ \\Omega$. Đáp án đúng là $106\\ \\Omega$.</p>"
    "<p>Đổi $0{,}3\\ \\text{mm}=0{,}3\\cdot10^{-3}\\ \\text{m}$ trước khi tính; lỗi hay gặp nằm ở công thức tiết diện.</p>",
    T_RHO, "bai_tap", "trung-binh",
    {"ABCD"[i]: {27: "Dùng S = πd² (quên chia 4) nên S lớn gấp 4, R nhỏ đi 4 lần.",
                 53: "Dùng S = πd²/2 (nhầm chia 2 thay vì chia 4).",
                 83: "Coi tiết diện là d² (hình vuông), quên hệ số π/4."}[x]
     for i, x in enumerate(opts2) if x != round(R2)}))

# ── Câu 3 · Phần I · so sánh hai dây cùng vật liệu (đáp án A)
k_l, k_d = 3, 2
ratio = F(k_l, k_d ** 2)
assert ratio == F(3, 4)
Q.append(mc(
    "<p>Hai dây dẫn cùng vật liệu, tiết diện tròn. So với dây 1, dây 2 dài gấp $3$ lần và có đường kính gấp $2$ lần. Tỉ số $\\dfrac{R_2}{R_1}$ bằng</p>",
    ["$0{,}75$.", "$1{,}5$.", "$6$.", "$12$."],
    0,
    "<p>$R=\\rho\\dfrac{l}{S}$ với $S=\\dfrac{\\pi d^2}{4}$ nên $S_2=4S_1$ (đường kính gấp $2$ thì tiết diện gấp $4$).</p>"
    "<p>$\\dfrac{R_2}{R_1}=\\dfrac{l_2/l_1}{S_2/S_1}=\\dfrac{3}{4}=0{,}75$. Đáp án A.</p>",
    T_RHO, "bai_tap", "de",
    {"B": "Coi tiết diện tỉ lệ với đường kính (S2 = 2S1): 3/2 = 1,5.",
     "C": "Nhân chiều dài với đường kính (3·2) thay vì chia cho tiết diện.",
     "D": "Nhân chiều dài với tiết diện (3·4) thay vì chia."}))

# ── Câu 4 · Phần I · đồ thị I–U, hai vật nối tiếp (đáp án A)
R1_4, R2_4 = F(60, 3), F(60, 1)                # I = 0,3 A và 0,1 A tại U = 6 V
assert R1_4 == 20 and R2_4 == 60
U4 = 12
I_nt = F(U4) / (R1_4 + R2_4)
I_ss = F(U4) / (R1_4 * R2_4 / (R1_4 + R2_4))
I_tb = F(3, 10) + F(1, 10)
assert I_nt == F(3, 20) and I_ss == F(4, 5) and I_tb == F(2, 5)
opts4 = [F(3, 20), F(1, 5), F(2, 5), F(4, 5)]
Q.append(mc(
    "<p>Đồ thị cường độ dòng điện $I$ (trục tung) theo hiệu điện thế $U$ (trục hoành) của hai vật dẫn $(1)$ và $(2)$ đều là đường thẳng qua gốc toạ độ. Khi $U=6\\ \\text{V}$, cường độ dòng điện qua vật dẫn $(1)$ là $0{,}3\\ \\text{A}$ và qua vật dẫn $(2)$ là $0{,}1\\ \\text{A}$. Mắc hai vật dẫn nối tiếp vào nguồn $12\\ \\text{V}$ (nguồn lí tưởng) thì cường độ dòng điện trong mạch là</p>",
    [f"${vn(x, 2)}\\ \\text{{A}}$." for x in [F(3, 20), F(1, 5), F(2, 5), F(4, 5)]],
    0,
    "<p>Từ đồ thị: $R_1=\\dfrac{6}{0{,}3}=20\\ \\Omega$, $R_2=\\dfrac{6}{0{,}1}=60\\ \\Omega$.</p>"
    "<p>Nối tiếp: $R=R_1+R_2=80\\ \\Omega$ nên $I=\\dfrac{12}{80}=0{,}15\\ \\text{A}$. Đáp án A.</p>"
    "<p>Hệ số góc của đồ thị $I$–$U$ là $\\dfrac{1}{R}$, không phải $R$.</p>",
    T_OHM, "bai_tap", "trung-binh",
    {"B": "Lấy trung bình hai cường độ (0,3 + 0,1)/2 = 0,2 A; trong mạch nối tiếp dòng điện qua hai vật bằng nhau và cho bởi U/(R1+R2).",
     "C": "Cộng hai cường độ ở 6 V (0,3 + 0,1 = 0,4 A), như thể hai vật mắc song song vào 6 V.",
     "D": "Mắc song song vào 12 V: 12/15 = 0,8 A (nhầm cách mắc)."}))

# ── Câu 5 · Phần II · cắt dây không bằng nhau rồi ghép
R5 = 48
a, b = F(1, 4) * R5, F(3, 4) * R5          # cắt theo tỉ lệ chiều dài 1 : 3
Rss = a * b / (a + b)
U5 = 18
Ia, Ib = F(U5) / a, F(U5) / b
assert a == 12 and b == 36 and Rss == 9 and Ia == F(3, 2) and Ib == F(1, 2) and Ia + Ib == 2 and U5 / Rss == 2
Q.append(dict(
    type="true_false",
    question="<p>Một dây dẫn đồng chất, tiết diện đều có điện trở $48\\ \\Omega$ được cắt thành hai đoạn có chiều dài theo tỉ lệ $1:3$. Bỏ qua điện trở các mối nối và dây nối.</p>",
    statements=[
        {"text": "Đoạn dài có điện trở $36\\ \\Omega$.", "answer": True},
        {"text": "Ghép song song hai đoạn thì điện trở tương đương bằng $24\\ \\Omega$.", "answer": False},
        {"text": "Khi hai đoạn mắc song song vào cùng một nguồn, dòng điện qua đoạn dài lớn hơn dòng điện qua đoạn ngắn.", "answer": False},
        {"text": "Nối bộ hai đoạn song song vào nguồn $18\\ \\text{V}$ thì dòng điện qua mạch chính là $2\\ \\text{A}$, trong đó qua đoạn ngắn là $1{,}5\\ \\text{A}$.", "answer": True},
    ],
    explanation=(
        "<p>a) Đúng: điện trở tỉ lệ với chiều dài (cùng vật liệu và tiết diện). Đoạn ngắn $\\dfrac{1}{4}\\cdot48=12\\ \\Omega$, đoạn dài $\\dfrac{3}{4}\\cdot48=36\\ \\Omega$.</p>"
        "<p>b) Sai: $R_{\\text{td}}=\\dfrac{12\\cdot36}{12+36}=9\\ \\Omega$. Con số $24\\ \\Omega$ là trung bình cộng, không phải điện trở song song.</p>"
        "<p>c) Sai: song song thì hiệu điện thế như nhau, $I=\\dfrac{U}{R}$ nên đoạn có điện trở nhỏ (đoạn ngắn) có dòng điện lớn hơn.</p>"
        "<p>d) Đúng: $I_{\\text{ngắn}}=\\dfrac{18}{12}=1{,}5\\ \\text{A}$, $I_{\\text{dài}}=\\dfrac{18}{36}=0{,}5\\ \\text{A}$, tổng $2\\ \\text{A}=\\dfrac{18}{9}$.</p>"),
    topic=T_CAT, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "R tỉ lệ với chiều dài: 3/4 chiều dài ứng với 3/4·48 = 36 Ω.",
        "1": "Điện trở tương đương song song là 12·36/48 = 9 Ω, không phải trung bình cộng.",
        "2": "Song song cùng U: R nhỏ hơn thì I lớn hơn, đoạn ngắn có dòng lớn hơn.",
        "3": "I = U/R: 18/12 = 1,5 A và 18/36 = 0,5 A; tổng 2 A = 18/9.",
    }))

# ── Câu 6 · Phần II · vôn kế có điện trở
U6, R1_6, R2_6, RV = 9, 200, 100, 300
Utrue = F(U6 * R2_6, R1_6 + R2_6)
Rp = F(R2_6 * RV, R2_6 + RV)
Uv = U6 * Rp / (R1_6 + Rp)
dev = (Utrue - Uv) / Utrue
assert Utrue == 3 and Rp == 75 and round(float(Uv), 2) == 2.45 and round(float(dev) * 100, 1) == 18.2


def dev_for(rv):
    rp = F(R2_6 * rv, R2_6 + rv)
    return (Utrue - U6 * rp / (R1_6 + rp)) / Utrue


assert dev_for(10000) < F(1, 100) and F(1, 50) < dev_for(3000) < F(5, 100) and round(float(dev_for(3000)) * 100, 1) == 2.2
Q.append(dict(
    type="true_false",
    question="<p>Nguồn lí tưởng có hiệu điện thế $9\\ \\text{V}$ nối tiếp với hai điện trở $R_1=200\\ \\Omega$ và $R_2=100\\ \\Omega$. Dùng vôn kế có điện trở $R_V=300\\ \\Omega$ mắc song song với $R_2$ để đo hiệu điện thế giữa hai đầu $R_2$.</p>",
    statements=[
        {"text": "Khi chưa mắc vôn kế, hiệu điện thế giữa hai đầu $R_2$ bằng $3\\ \\text{V}$.", "answer": True},
        {"text": "Khi mắc vôn kế, điện trở tương đương của $R_2$ và vôn kế bằng $75\\ \\Omega$.", "answer": True},
        {"text": "Số chỉ của vôn kế lớn hơn $3\\ \\text{V}$ vì có thêm một nhánh cho dòng điện đi qua.", "answer": False},
        {"text": "Nếu dùng vôn kế $R_V=3\\ \\text{k}\\Omega$ thì số chỉ vẫn thấp hơn giá trị thật quá $5\\,\\%$.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: $U_2=9\\cdot\\dfrac{100}{200+100}=3\\ \\text{V}$.</p>"
        "<p>b) Đúng: $\\dfrac{100\\cdot300}{100+300}=75\\ \\Omega$.</p>"
        "<p>c) Sai: thêm nhánh song song làm điện trở của đoạn chứa $R_2$ giảm, phần hiệu điện thế dồn vào $R_2$ giảm theo: $U_V=9\\cdot\\dfrac{75}{200+75}\\approx2{,}45\\ \\text{V}\\lt3\\ \\text{V}$ (thấp hơn khoảng $18\\,\\%$).</p>"
        "<p>d) Sai: với $R_V=3000\\ \\Omega$, $R_{\\text{td}}\\approx96{,}8\\ \\Omega$, $U_V\\approx2{,}93\\ \\text{V}$, thấp hơn giá trị thật khoảng $2\\,\\%$, nhỏ hơn $5\\,\\%$.</p>"),
    topic=T_DUNG, form="bai_tap", difficulty="kho",
    distractorNotes={
        "0": "Nguồn chia theo tỉ lệ điện trở nối tiếp: U2 = 9·100/300 = 3 V.",
        "1": "Song song: 100·300/(100 + 300) = 75 Ω.",
        "2": "Thêm nhánh song song làm điện trở đoạn giảm nên hiệu điện thế trên đoạn giảm, vôn kế chỉ nhỏ hơn 3 V.",
        "3": "R_V = 3000 Ω chỉ gây lệch khoảng 2 %, không quá 5 %.",
    }))

# ── Câu 7 · Phần III · biến trở bằng dây nicrom, đèn sáng bình thường
U7, Ud, Id = 15, 6, F(1, 2)
Rbt = (U7 - Ud) / Id
rho7, d7 = F(11, 10) * F(1, 10**6), F(2, 10) * F(1, 10**3)
S7 = math.pi * float(d7) ** 2 / 4
l7 = float(Rbt) * S7 / float(rho7)
assert Rbt == 18 and round(l7, 2) == 0.51 and abs(l7 - 0.5141) < 5e-4
Q.append(dict(
    type="short_answer",
    question="<p>Bóng đèn ghi $6\\ \\text{V}-0{,}5\\ \\text{A}$ mắc nối tiếp với một biến trở vào nguồn lí tưởng $15\\ \\text{V}$ sao cho đèn sáng bình thường. Biến trở được quấn bằng dây nicrom có điện trở suất $1{,}1\\cdot10^{-6}\\ \\Omega\\cdot\\text{m}$, đường kính tiết diện $0{,}2\\ \\text{mm}$. Chiều dài dây nicrom của phần biến trở đang được dùng là bao nhiêu mét? Làm tròn đến $0{,}01\\ \\text{m}$.</p>",
    answer=f"{l7:.2f}".replace(".", ","),
    explanation=(
        "<p>Đèn sáng bình thường nên $I=0{,}5\\ \\text{A}$ và hiệu điện thế giữa hai đầu đèn là $6\\ \\text{V}$.</p>"
        "<p>Biến trở chịu $U_b=15-6=9\\ \\text{V}$ nên $R_b=\\dfrac{9}{0{,}5}=18\\ \\Omega$.</p>"
        "<p>$S=\\dfrac{\\pi d^2}{4}=\\dfrac{\\pi\\,(0{,}2\\cdot10^{-3})^2}{4}\\approx3{,}14\\cdot10^{-8}\\ \\text{m}^2$.</p>"
        "<p>$l=\\dfrac{R_bS}{\\rho}=\\dfrac{18\\cdot3{,}14\\cdot10^{-8}}{1{,}1\\cdot10^{-6}}\\approx0{,}51\\ \\text{m}$.</p>"
        "<p>Bẫy: lấy $R_b=\\dfrac{15}{0{,}5}=30\\ \\Omega$ (quên phần hiệu điện thế của đèn) sẽ ra $\\approx0{,}86\\ \\text{m}$.</p>"),
    topic=T_BT, form="bai_tap", difficulty="trung-binh"))

# ── Câu 8 · Phần III · kéo dãn dây, đường kính giảm
R8, k = 4, 3
R8b = R8 * k ** 4
assert R8b == 324 and len(str(R8b)) <= 4
Q.append(dict(
    type="short_answer",
    question="<p>Một dây đồng chất, tiết diện tròn đều có điện trở $4\\ \\Omega$. Kéo dãn dây (thể tích không đổi, vẫn có tiết diện tròn đều) sao cho đường kính tiết diện giảm đi $3$ lần. Điện trở của dây sau khi kéo bằng bao nhiêu $\\Omega$?</p>",
    answer=str(R8b),
    explanation=(
        "<p>Thể tích không đổi: $lS=\\text{const}$. Đường kính giảm $3$ lần thì tiết diện giảm $3^2=9$ lần, nên chiều dài tăng $9$ lần.</p>"
        "<p>$R=\\rho\\dfrac{l}{S}$ tăng $9\\cdot9=81$ lần: $R'=4\\cdot81=324\\ \\Omega$.</p>"
        "<p>Bẫy: chỉ tính theo chiều dài ($\\times9$, ra $36\\ \\Omega$) hoặc theo đường kính ($\\times3$, ra $12\\ \\Omega$) là quên một trong hai thay đổi.</p>"),
    topic=T_CAT, form="bai_tap", difficulty="kho"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) != [0, 0, 0, 0]
for q in Q[6:]:
    assert len(q["answer"]) <= 4
for q in Q:
    assert q["topic"] in (T_OHM, T_RHO, T_CAT, T_BT, T_DUNG)
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 and ch not in "\n" for ch in s), s

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Điện trở và định luật Ohm",
        "topic": T_OHM,
        "difficulty": "trung-binh",
        "duration_minutes": 20,
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
