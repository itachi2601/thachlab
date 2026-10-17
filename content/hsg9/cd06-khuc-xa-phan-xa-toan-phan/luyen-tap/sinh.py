# -*- coding: utf-8 -*-
"""CĐ06 Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc (lesson 151) — sinh luyen-tap/bundle.json
(8 câu tự chấm: 4 Phần I, 2 Phần II, 2 Phần III). Chỉ có khối exam (theory_html rỗng, worked_examples []) để
upload-lesson.mts giữ nguyên lý thuyết và bài tập mẫu.
Số liệu theo nguon.md mục Luyện tập (tính bằng Python + assert); mỗi phương án nhiễu ứng với một cách sai cụ thể.
Số liệu khác bài tập mẫu (151.json), khác tự luận (btm151_tl.py) và khác ví dụ docx (nguon.txt).
Quy ước: mọi góc đo so với PHÁP TUYẾN; không khí n = 1, nước n = 4/3, c = 3.10^8 m/s.
Chạy: python3 content/hsg9/cd06-khuc-xa-phan-xa-toan-phan/luyen-tap/sinh.py"""
import json
from fractions import Fraction as F
from math import asin, sin, tan, degrees, radians, sqrt, isclose
from pathlib import Path

C = 3e8
NW = F(4, 3)
T_KX = "Mô tả hiện tượng khúc xạ, vẽ đường truyền tia sáng"
T_N = "Chiết suất và định luật khúc xạ ánh sáng"
T_PX = "Điều kiện xảy ra phản xạ toàn phần"
T_LK = "Đường truyền tia sáng qua lăng kính"
T_TS = "Tán sắc ánh sáng qua lăng kính"
TOPICS = (T_KX, T_N, T_PX, T_LK, T_TS)


def igh(n):
    return degrees(asin(1 / float(n)))


def sd(a):
    return sin(radians(a))


def vn(x, nd=1):
    """Số kiểu Việt Nam trong $…$: dấu phẩy thập phân, bỏ ,0 thừa."""
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def mc(question, options, answer, explanation, topic, form, diff, notes):
    assert len(options) == 4 and len(set(options)) == 4, options
    assert set(notes) == {"ABCD"[i] for i in range(4) if i != answer}
    return dict(type="multiple_choice", question=question, options=options, answer=answer,
                explanation=explanation, topic=topic, form=form, difficulty=diff, distractorNotes=notes)


Q = []

# ── Câu 1 · Phần I · n = c/v (đáp án C)
n1 = 1.25
v_dung = C / n1
v_nhan = C * n1          # nhân thay vì chia
v_nham = C / float(NW)    # lấy nhầm chiết suất của nước 4/3
v_ck = C                 # coi như chân không
opts1 = [v_nhan, v_nham, v_dung, v_ck]
assert isclose(v_dung, 2.4e8) and isclose(v_nham, 2.25e8) and v_nham != v_dung and len({round(x / 1e6) for x in opts1}) == 4 and opts1.index(v_dung) == 2
Q.append(mc(
    "<p>Một chất lỏng trong suốt có chiết suất $1{,}25$. Cho tốc độ ánh sáng trong chân không $c=3\\cdot10^8\\ \\text{m/s}$. Tốc độ ánh sáng trong chất lỏng này là</p>",
    [f"${vn(x / 1e8, 2)}\\cdot10^8\\ \\text{{m/s}}$." for x in opts1],
    2,
    "<p>Chiết suất $n=\\dfrac cv$ nên $v=\\dfrac cn=\\dfrac{3\\cdot10^8}{1{,}25}=2{,}4\\cdot10^8\\ \\text{m/s}$. Đáp án C.</p>"
    "<p>Chiết suất lớn hơn $1$ thì ánh sáng đi chậm hơn trong chân không, nên A ($\\gt c$) và D ($=c$) chắc chắn sai.</p>",
    T_N, "bai_tap", "de",
    {"A": "Nhân c với n thay vì chia: ra tốc độ lớn hơn c, vô lí.",
     "B": "Lấy nhầm chiết suất của nước 4/3: v = c/(4/3) = 2,25·10⁸ m/s, không phải chất lỏng n = 1,25.",
     "D": "Coi ánh sáng đi trong chất lỏng nhanh như trong chân không, bỏ qua chiết suất."}))

# ── Câu 2 · Phần I · góc giới hạn (đáp án A)
g_dung = igh(n1)
g_phu = 90 - g_dung       # đo góc so với mặt phân cách
g_nuoc = igh(NW)          # dùng chiết suất nước
g_tt = igh(1.5)           # dùng chiết suất thuỷ tinh
opts2 = [g_dung, g_phu, g_nuoc, g_tt]
assert [round(x, 1) for x in opts2] == [53.1, 36.9, 48.6, 41.8]
Q.append(mc(
    "<p>Ánh sáng truyền từ chất lỏng có chiết suất $1{,}25$ ra không khí. Góc giới hạn phản xạ toàn phần (đo so với pháp tuyến) xấp xỉ bằng</p>",
    [f"${vn(x)}^\\circ$." for x in opts2],
    0,
    "<p>$\\sin i_{gh}=\\dfrac{n_2}{n_1}=\\dfrac{1}{1{,}25}=0{,}8$ nên $i_{gh}\\approx53{,}1^\\circ$. Đáp án A.</p>"
    "<p>B là góc hợp với mặt phân cách ($90^\\circ-53{,}1^\\circ$), không phải với pháp tuyến.</p>"
    "<p>C và D là góc giới hạn của nước ($n=\\tfrac43$) và thuỷ tinh ($n=1{,}5$), không phải chất lỏng này.</p>",
    T_PX, "bai_tap", "de",
    {"B": "Đo góc so với mặt phân cách (90° − 53,1°) thay vì so với pháp tuyến.",
     "C": "Dùng góc giới hạn quen thuộc của nước (n = 4/3) thay cho chất lỏng n = 1,25.",
     "D": "Dùng góc giới hạn của thuỷ tinh (n = 1,5) thay cho chất lỏng n = 1,25."}))

# ── Câu 3 · Phần I · màu sắc vật (đáp án D)
Q.append(mc(
    "<p>Trong phòng tối, chiếu một chiếc lá cây xanh lục bằng đèn chỉ phát ánh sáng đỏ. Nhìn chiếc lá ta thấy nó có màu</p>",
    ["đỏ.", "vàng (trộn đỏ với lục).", "xanh lục.", "gần như đen."],
    3,
    "<p>Vật xanh lục hắt lại mạnh ánh sáng lục và hấp thụ phần lớn ánh sáng các màu khác, trong đó có ánh sáng đỏ.</p>"
    "<p>Đèn chỉ có ánh sáng đỏ nên lá hầu như không hắt lại gì tới mắt: lá trông gần như đen. Đáp án D.</p>",
    T_TS, "ly_thuyet", "trung-binh",
    {"A": "Nghĩ vật hắt lại mọi ánh sáng chiếu tới như vật trắng; lá xanh lục hấp thụ ánh sáng đỏ.",
     "B": "Tưởng màu của lá trộn với màu ánh sáng đèn; vật không tự phát ra ánh sáng lục.",
     "C": "Nghĩ màu là tính chất cố định của vật, không phụ thuộc ánh sáng chiếu tới."}))

# ── Câu 4 · Phần I · lăng kính, tia tới vuông góc mặt AB (đáp án B)
A4, n4 = 40, 1.5
s_r2 = n4 * sd(A4)
r2 = degrees(asin(s_r2))
D4 = r2 - A4
assert s_r2 < 1 and A4 < igh(n4)                    # 40° < 41,8° nên tia ló ra được
assert round(s_r2, 4) == 0.9642 and round(r2, 1) == 74.6 and round(D4, 1) == 34.6
opts4 = [f"${A4}^\\circ$.", f"${vn(D4)}^\\circ$.", f"${vn(r2)}^\\circ$.",
         "Tia không ló ra ở mặt $AC$ vì bị phản xạ toàn phần."]
Q.append(mc(
    "<p>Một lăng kính thuỷ tinh có góc chiết quang $A=40^\\circ$, chiết suất $1{,}5$, đặt trong không khí. Chiếu một tia sáng tới mặt bên $AB$ theo phương vuông góc với mặt đó. Cho $\\sin40^\\circ\\approx0{,}6428$. Góc lệch giữa tia ló khỏi mặt $AC$ và tia tới xấp xỉ bằng</p>",
    opts4,
    1,
    "<p>Tia tới vuông góc $AB$ nên đi thẳng vào lăng kính. Góc tới ở mặt $AC$ bằng góc chiết quang: $i_2=A=40^\\circ$ (góc có cạnh tương ứng vuông góc).</p>"
    "<p>Góc giới hạn thuỷ tinh ra không khí $i_{gh}\\approx41{,}8^\\circ$; vì $40^\\circ\\lt41{,}8^\\circ$ nên tia ló ra được.</p>"
    "<p>$\\sin r_2=1{,}5\\sin40^\\circ\\approx0{,}9642$ nên $r_2\\approx74{,}6^\\circ$.</p>"
    "<p>Góc lệch $D=r_2-A\\approx74{,}6^\\circ-40^\\circ=34{,}6^\\circ$. Đáp án B.</p>",
    T_LK, "bai_tap", "kho",
    {"A": "Lấy góc lệch bằng góc chiết quang A; A chỉ là góc tới ở mặt AC.",
     "C": "Dừng ở góc ló r₂ (so với pháp tuyến mặt AC), quên trừ A để ra góc lệch so với tia tới.",
     "D": "Nhớ mang máng thuỷ tinh có i_gh ≈ 42° rồi đoán; thực ra 40° < 41,8° nên chưa phản xạ toàn phần."}))

# ── Câu 5 · Phần II · phản xạ toàn phần, sợi quang
assert round(igh(2.42), 1) == 24.4 and igh(2.42) < igh(1.5)
Q.append(dict(
    type="true_false",
    question="<p>Xét hiện tượng phản xạ toàn phần và ứng dụng của nó. Cho chiết suất của nước $\\tfrac43$, thuỷ tinh $1{,}5$, kim cương $2{,}42$.</p>",
    statements=[
        {"text": "Có thể xảy ra phản xạ toàn phần khi ánh sáng truyền từ nước vào thuỷ tinh nếu góc tới đủ lớn.", "answer": False},
        {"text": "Góc giới hạn của kim cương ra không khí xấp xỉ $24{,}4^\\circ$, nhỏ hơn của thuỷ tinh, nên ánh sáng trong viên kim cương dễ bị phản xạ toàn phần hơn.", "answer": True},
        {"text": "Khi góc tới bằng góc giới hạn, góc khúc xạ bằng $90^\\circ$ và tia khúc xạ đã hoàn toàn biến mất.", "answer": False},
        {"text": "Để ánh sáng truyền được trong sợi quang, lõi sợi phải có chiết suất lớn hơn chiết suất của lớp vỏ.", "answer": True},
    ],
    explanation=(
        "<p>a) Sai: phản xạ toàn phần chỉ xảy ra khi ánh sáng đi từ môi trường chiết quang hơn sang môi trường chiết quang kém; nước ($\\tfrac43$) kém hơn thuỷ tinh ($1{,}5$).</p>"
        "<p>b) Đúng: $\\sin i_{gh}=\\dfrac1{2{,}42}\\approx0{,}413$ nên $i_{gh}\\approx24{,}4^\\circ\\lt41{,}8^\\circ$; nhiều tia gặp mặt trong với góc tới lớn hơn $24{,}4^\\circ$ nên bị phản xạ toàn phần, kim cương lấp lánh.</p>"
        "<p>c) Sai: khi $i=i_{gh}$ thì $r=90^\\circ$, tia khúc xạ đi là là mặt phân cách và rất mờ; chỉ khi $i\\gt i_{gh}$ mới hết tia khúc xạ.</p>"
        "<p>d) Đúng: tia trong lõi gặp mặt lõi–vỏ, muốn phản xạ toàn phần thì phải đi từ môi trường chiết quang hơn (lõi) sang chiết quang kém (vỏ).</p>"),
    topic=T_PX, form="ly_thuyet", difficulty="trung-binh",
    distractorNotes={
        "0": "Hai điều kiện: đi từ môi trường chiết quang hơn sang kém, và i ≥ i_gh. Nước → thuỷ tinh không thoả điều kiện thứ nhất.",
        "1": "sin i_gh = 1/2,42 ≈ 0,413, i_gh ≈ 24,4°: góc giới hạn càng nhỏ càng dễ phản xạ toàn phần.",
        "2": "r = 90° là tia đi là là mặt phân cách, chưa mất; phải i > i_gh mới hết tia khúc xạ.",
        "3": "Lõi chiết quang hơn vỏ thì tia mới phản xạ toàn phần ở mặt lõi–vỏ.",
    }))

# ── Câu 6 · Phần II · ảnh qua mặt phân cách, bản mặt song song
h_ho, e_k, n_k = 2, 3, F(3, 2)
assert h_ho / NW == F(3, 2) and e_k * (1 - 1 / n_k) == 1
Q.append(dict(
    type="true_false",
    question="<p>Xét ảnh của vật khi nhìn qua mặt nước và qua tấm kính phẳng hai mặt song song. Cho chiết suất của nước $\\tfrac43$.</p>",
    statements=[
        {"text": "Một hồ nước trong, sâu $2\\ \\text{m}$; nhìn gần vuông góc với mặt nước thì đáy hồ trông như sâu $1{,}50\\ \\text{m}$.", "answer": True},
        {"text": "Đặt tấm kính dày $3\\ \\text{cm}$, chiết suất $1{,}5$ lên trang sách; nhìn gần vuông góc thì chữ trông gần mắt hơn $1{,}0\\ \\text{cm}$ so với khi không có kính.", "answer": True},
        {"text": "Tia sáng ló ra khỏi tấm kính phẳng hai mặt song song bị lệch về phía pháp tuyến so với tia tới.", "answer": False},
        {"text": "Nhìn xiên (không vuông góc với mặt nước) thì đáy hồ trông sâu hơn so với khi nhìn vuông góc.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: $h'=\\dfrac hn=\\dfrac{2}{4/3}=1{,}5\\ \\text{m}$.</p>"
        "<p>b) Đúng: ảnh dịch lại gần mắt $e\\left(1-\\dfrac1n\\right)=3\\left(1-\\dfrac1{1{,}5}\\right)=1\\ \\text{cm}$.</p>"
        "<p>c) Sai: hai mặt song song nên góc ló ở mặt dưới bằng góc tới ở mặt trên; tia ló song song với tia tới, chỉ bị dời ngang.</p>"
        "<p>d) Sai: nhìn càng xiên thì đáy trông càng <em>nông</em> hơn; công thức $h/n$ chỉ đúng khi nhìn gần vuông góc.</p>"),
    topic=T_KX, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "h' = h/n = 2 : (4/3) = 1,5 m; ảnh dịch về phía không khí (chiết quang kém).",
        "1": "Δ = e(1 − 1/n) = 3·(1 − 1/1,5) = 1 cm.",
        "2": "Tia ló khỏi bản mặt song song luôn song song với tia tới, chỉ bị dời ngang.",
        "3": "Nhìn xiên thì đáy trông còn nông hơn khi nhìn vuông góc.",
    }))

# ── Câu 7 · Phần III · độ sâu biểu kiến
h7 = F(18, 10)
h7p = h7 / NW
assert h7p == F(135, 100) and h7 * NW == F(24, 10)
Q.append(dict(
    type="short_answer",
    question="<p>Một hồ nước trong, đáy phẳng, sâu $1{,}8\\ \\text{m}$. Chiết suất của nước $\\tfrac43$. Nhìn đáy hồ theo phương gần vuông góc với mặt nước thì đáy hồ trông như cách mặt nước bao nhiêu mét?</p>",
    answer=vn(h7p, 2).replace("{,}", ","),
    explanation=(
        "<p>Nhìn gần vuông góc: $h'=\\dfrac hn=\\dfrac{1{,}8}{4/3}=1{,}35\\ \\text{m}$.</p>"
        "<p>Bẫy: nhân với $n$ ra $2{,}4\\ \\text{m}$ — ảnh phải dịch lên phía không khí (môi trường chiết quang kém) nên nông hơn độ sâu thật.</p>"),
    topic=T_KX, form="bai_tap", difficulty="de"))

# ── Câu 8 · Phần III · vùng sáng tròn trên mặt nước
h8 = 0.6
tg = 3 / sqrt(7)                      # tan i_gh khi sin = 3/4
assert isclose(tg, tan(radians(igh(NW))))
R8 = h8 * tg
assert round(R8, 2) == 0.68 and round(h8 * tan(radians(90 - igh(NW))), 2) == 0.53 and round(h8 * 0.75, 2) == 0.45
Q.append(dict(
    type="short_answer",
    question="<p>Một bóng đèn rất nhỏ đặt trong nước, ở độ sâu $0{,}6\\ \\text{m}$ dưới mặt nước phẳng lặng; chiết suất của nước $\\tfrac43$. Ánh sáng từ đèn chỉ ló ra không khí qua một vùng tròn trên mặt nước, tâm ở ngay phía trên đèn. Bán kính vùng tròn đó bằng bao nhiêu mét? Làm tròn đến hai chữ số sau dấu phẩy.</p>",
    answer=vn(R8, 2).replace("{,}", ","),
    explanation=(
        "<p>Tia từ đèn tới mặt nước với góc tới $i\\ge i_{gh}$ bị phản xạ toàn phần; mép vùng sáng ứng với $i=i_{gh}$.</p>"
        "<p>$\\sin i_{gh}=\\dfrac{1}{4/3}=0{,}75$, $\\cos i_{gh}=\\dfrac{\\sqrt7}{4}$ nên $\\tan i_{gh}=\\dfrac{3}{\\sqrt7}\\approx1{,}134$.</p>"
        "<p>$R=h\\tan i_{gh}=0{,}6\\cdot1{,}134\\approx0{,}68\\ \\text{m}$.</p>"
        "<p>Bẫy: dùng $R=h\\sin i_{gh}$ ra $0{,}45\\ \\text{m}$, hoặc lấy góc so với mặt nước ra $0{,}53\\ \\text{m}$.</p>"),
    topic=T_PX, form="bai_tap", difficulty="kho"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) == [0, 1, 2, 3]
assert [q["answer"] for q in Q[6:]] == ["1,35", "0,68"]
for q in Q[6:]:
    assert len(q["answer"]) <= 4
for q in Q:
    assert q["topic"] in TOPICS
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 and ch not in "\n" for ch in s), s
        for seg in s.split("$")[1::2]:
            assert "<" not in seg and ">" not in seg, seg
            assert not any("\u00c0" <= ch <= "\u1ef9" for ch in seg.replace("\\text{m/s}", "")) or "\\text" in seg, seg

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Khúc xạ, phản xạ toàn phần, lăng kính và tán sắc",
        "topic": T_N,
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
