# -*- coding: utf-8 -*-
"""CĐ07 Thấu kính mỏng và kính lúp (lesson 156) — sinh luyen-tap/bundle.json (8 câu tự chấm: 4 Phần I, 2 Phần II, 2 Phần III).
Chỉ có khối exam (theory_html rỗng, worked_examples []) để upload-lesson.mts giữ nguyên lý thuyết và bài tập mẫu.
Số liệu theo nguon.md mục Luyện tập (tinh.py); mỗi phương án nhiễu ứng với một cách sai cụ thể và khác đáp án đúng.
Quy ước dấu: d > 0; d' > 0 ảnh thật, d' < 0 ảnh ảo; f > 0 hội tụ, f < 0 phân kì; 1/f = 1/d + 1/d'.
Chạy: python3 content/hsg9/cd07-thau-kinh-kinh-lup/luyen-tap/sinh.py"""
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

T_DD = "Đặc điểm thấu kính hội tụ, phân kì và tiêu cự"
T_DUNG = "Dựng ảnh của vật qua thấu kính"
T_CT = "Công thức thấu kính và số phóng đại"


def anh(f, d):
    return 1 / (1 / F(f) - 1 / F(d))


def vn(x, nd=2):
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def mc(question, options, answer, explanation, topic, form, diff, notes):
    assert len(options) == 4 and len(set(options)) == 4, options
    assert set(notes) == {"ABCD"[i] for i in range(4) if i != answer}
    return dict(type="multiple_choice", question=question, options=options, answer=answer,
                explanation=explanation, topic=topic, form=form, difficulty=diff, distractorNotes=notes)


Q = []

# ── Câu 1 · Phần I · tia song song qua TK phân kì (đáp án D)
Q.append(mc(
    "<p>Một tia sáng tới thấu kính phân kì theo phương song song với trục chính. Tia ló</p>",
    ["hội tụ tại tiêu điểm ảnh $F'$ ở phía sau thấu kính.",
     "đi song song với trục chính.",
     "truyền thẳng, không đổi hướng.",
     "loe ra xa trục chính, có đường kéo dài đi qua tiêu điểm ảnh $F'$ nằm cùng phía với tia tới."],
    3,
    "<p>Thấu kính phân kì làm chùm song song loe ra; các tia ló có đường kéo dài (nét đứt) gặp nhau tại tiêu điểm ảnh $F'$, nằm cùng phía với ánh sáng tới. Đáp án D.</p>"
    "<p>A là tính chất của thấu kính hội tụ. B là tia ló của tia đi qua tiêu điểm vật. C là tia đi qua quang tâm $O$.</p>",
    T_DUNG, "ly_thuyet", "de",
    {"A": "Lẫn với thấu kính hội tụ; F' của TK phân kì nằm cùng phía vật, tia ló không đi qua thật.",
     "B": "Đó là tia ló của tia có đường kéo dài đi qua tiêu điểm vật F.",
     "C": "Chỉ tia đi qua quang tâm O mới truyền thẳng."}))

# ── Câu 2 · Phần I · HT f = 15, d = 10 (đáp án A)
dp2 = anh(15, 10)
s_dau = 1 / (F(1, 15) + F(1, 10))       # cộng 1/f + 1/d
assert dp2 == -30 and s_dau == 6
Q.append(mc(
    "<p>Vật sáng $AB$ đặt vuông góc với trục chính của một thấu kính hội tụ tiêu cự $15\\ \\text{cm}$, $A$ nằm trên trục chính và cách thấu kính $10\\ \\text{cm}$. Ảnh $A'B'$ là</p>",
    ["ảnh ảo, cùng chiều vật, cách thấu kính $30\\ \\text{cm}$.",
     "ảnh thật, ngược chiều vật, cách thấu kính $30\\ \\text{cm}$.",
     "ảnh ảo, cùng chiều vật, cách thấu kính $6\\ \\text{cm}$.",
     "ảnh thật, ngược chiều vật, cách thấu kính $6\\ \\text{cm}$."],
    0,
    "<p>$\\dfrac1{d'}=\\dfrac1f-\\dfrac1d=\\dfrac1{15}-\\dfrac1{10}=-\\dfrac1{30}$ nên $d'=-30\\ \\text{cm}$.</p>"
    "<p>$d'\\lt0$: ảnh ảo, cùng phía và cùng chiều vật, cách thấu kính $30\\ \\text{cm}$. Đáp án A.</p>"
    "<p>Kiểm nhanh: vật nằm trong khoảng tiêu cự ($d\\lt f$) nên thấu kính hội tụ cho ảnh ảo, lớn hơn vật, xa thấu kính hơn vật ($|d'|\\gt d$).</p>",
    T_CT, "bai_tap", "de",
    {"B": "Giải ra d' = −30 nhưng bỏ dấu trừ, kết luận ảnh thật.",
     "C": "Viết sai 1/d' = 1/f + 1/d nên ra 6 cm; ảnh ảo của TK hội tụ phải xa TK hơn vật.",
     "D": "Vừa cộng sai 1/f + 1/d vừa không xét dấu d'."}))

# ── Câu 3 · Phần I · tiêu cự lớn nhất khi L = 90 (đáp án B)
L3 = 90
fmax = F(L3, 4)
f_mot = F(30 * 60, 90)                  # chỉ thử một vị trí d = 30, d' = 60
f_2f = F(L3, 2)                         # nhầm L ≥ 2f
f_L = F(L3)                             # coi màn đặt ở tiêu điểm
assert fmax == F(45, 2) and f_mot == 20 and anh(20, 30) == 60 and f_2f == 45 and f_L == 90
assert len({fmax, f_mot, f_2f, f_L}) == 4
Q.append(mc(
    "<p>Vật sáng và màn ảnh đặt cố định, cách nhau $90\\ \\text{cm}$. Đặt một thấu kính hội tụ ở khoảng giữa vật và màn. Để có ít nhất một vị trí của thấu kính cho ảnh rõ nét trên màn, tiêu cự của thấu kính lớn nhất bằng</p>",
    ["$20\\ \\text{cm}$.", "$22{,}5\\ \\text{cm}$.", "$45\\ \\text{cm}$.", "$90\\ \\text{cm}$."],
    1,
    "<p>Ảnh trên màn là ảnh thật: $d+d'=L$ nên $d^2-Ld+Lf=0$.</p>"
    "<p>Có nghiệm khi $\\Delta=L^2-4Lf\\ge0$, tức $L\\ge4f$, hay $f\\le\\dfrac L4=\\dfrac{90}4=22{,}5\\ \\text{cm}$. Đáp án B.</p>"
    "<p>Khi $f=22{,}5\\ \\text{cm}$, chỉ có một vị trí: $d=d'=45\\ \\text{cm}=2f$, ảnh bằng vật.</p>",
    T_CT, "bai_tap", "trung-binh",
    {"A": "Chỉ thử một vị trí (d = 30, d' = 60 cho f = 20 cm) rồi coi là lớn nhất, không biện luận Δ ≥ 0.",
     "C": "Nhầm điều kiện thành L ≥ 2f (tưởng vật và ảnh đều ở tiêu điểm).",
     "D": "Coi màn đặt tại tiêu điểm nên f = L — chỉ đúng khi vật ở rất xa."}))

# ── Câu 4 · Phần I · kính lúp 12,5× (đáp án C)
G = F(25, 2)
f4 = 25 / G
s_G = G                                  # lấy f = G
s_cc = 1 / (1 / f4 + F(1, 25))           # ngắm chừng ở cực cận
s_25 = F(25)                             # đặt vật ở điểm cực cận
assert f4 == 2 and s_cc == F(50, 27) and round(float(s_cc), 2) == 1.85
opts4 = [s_G, s_cc, f4, s_25]
assert len(set(opts4)) == 4 and opts4[2] == f4
Q.append(mc(
    "<p>Trên vành một kính lúp có ghi $12{,}5\\times$. Một học sinh mắt tốt (điểm cực cận cách mắt $25\\ \\text{cm}$, điểm cực viễn ở vô cực) đặt kính sát mắt và ngắm chừng ở vô cực (mắt không phải điều tiết). Vật phải đặt cách kính</p>",
    ["$12{,}5\\ \\text{cm}$.", f"${vn(s_cc)}\\ \\text{{cm}}$.", "$2\\ \\text{cm}$.", "$25\\ \\text{cm}$."],
    2,
    "<p>$G=\\dfrac{25}{f}$ nên $f=\\dfrac{25}{12{,}5}=2\\ \\text{cm}$.</p>"
    "<p>Ngắm chừng ở vô cực: tia ló song song, vật đặt tại tiêu điểm, $d=f=2\\ \\text{cm}$. Đáp án C.</p>",
    T_DD, "bai_tap", "trung-binh",
    {"A": "Lấy luôn số ghi trên kính làm tiêu cự (f = G = 12,5 cm).",
     "B": "Tính cho ngắm chừng ở điểm cực cận (ảnh ảo tại 25 cm) thay vì ở vô cực.",
     "D": "Đặt vật ở điểm cực cận của mắt — đó là chỗ đặt vật khi nhìn bằng mắt thường, không dùng kính."}))

# ── Câu 5 · Phần II · thấu kính phân kì
dp5 = anh(-20, 30); h5 = 5 * (-dp5) / 30
dp5b = anh(-20, 60)
assert dp5 == -12 and h5 == 2 and dp5b == -15 and -dp5b > -dp5 and -dp5b < 20
Q.append(dict(
    type="true_false",
    question="<p>Vật sáng $AB$ cao $5\\ \\text{cm}$ đặt vuông góc với trục chính của một thấu kính phân kì có tiêu cự $20\\ \\text{cm}$ (theo quy ước dấu $f=-20\\ \\text{cm}$), $A$ nằm trên trục chính và cách thấu kính $30\\ \\text{cm}$.</p>",
    statements=[
        {"text": "Ảnh $A'B'$ là ảnh ảo, cùng chiều vật.", "answer": True},
        {"text": "Ảnh cách thấu kính $12\\ \\text{cm}$.", "answer": True},
        {"text": "Ảnh cao $2{,}5\\ \\text{cm}$.", "answer": False},
        {"text": "Dịch vật ra xa thấu kính thì ảnh dịch lại gần thấu kính.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: vật thật qua thấu kính phân kì luôn cho ảnh ảo, cùng chiều, nhỏ hơn vật.</p>"
        "<p>b) Đúng: $\\dfrac1{d'}=-\\dfrac1{20}-\\dfrac1{30}=-\\dfrac1{12}$ nên $d'=-12\\ \\text{cm}$.</p>"
        "<p>c) Sai: $h'=5\\cdot\\dfrac{12}{30}=2\\ \\text{cm}$.</p>"
        "<p>d) Sai: đưa vật ra $60\\ \\text{cm}$ thì $\\dfrac1{d'}=-\\dfrac1{20}-\\dfrac1{60}=-\\dfrac1{15}$, $d'=-15\\ \\text{cm}$: ảnh dịch <em>ra xa</em> thấu kính (từ $12$ lên $15\\ \\text{cm}$), tiến dần về $F'$ nhưng không vượt quá $20\\ \\text{cm}$.</p>"),
    topic=T_CT, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "Vật thật qua TK phân kì luôn cho ảnh ảo, cùng chiều, nhỏ hơn vật.",
        "1": "1/d' = −1/20 − 1/30 = −1/12, ảnh cách TK 12 cm.",
        "2": "h' = h·|d'|/d = 5·12/30 = 2 cm; 2,5 cm là lấy h/2 do tưởng ảnh qua PK luôn bằng nửa vật.",
        "3": "Với TK phân kì, vật ra xa thì ảnh ảo cũng ra xa TK, tiến dần về F'.",
    }))

# ── Câu 6 · Phần II · vật–màn L = 100, f = 21
L6, f6 = 100, 21
D6 = L6 * L6 - 4 * L6 * f6
ell = isqrt(D6)
d_gan, d_xa = (L6 - ell) // 2, (L6 + ell) // 2
assert D6 == 1600 and ell * ell == D6 and ell == 40 and (d_gan, d_xa) == (30, 70)
assert anh(f6, d_gan) == 70 and anh(f6, d_xa) == 30 and F(70, 30) > 1 and 4 * f6 == 84 > 80
Q.append(dict(
    type="true_false",
    question="<p>Vật sáng $AB$ và màn ảnh đặt cố định, cách nhau $100\\ \\text{cm}$. Dịch chuyển một thấu kính hội tụ tiêu cự $21\\ \\text{cm}$ trong khoảng giữa vật và màn (trục chính vuông góc màn, đi qua $A$).</p>",
    statements=[
        {"text": "Có hai vị trí của thấu kính cho ảnh rõ nét trên màn.", "answer": True},
        {"text": "Ở vị trí thấu kính gần vật hơn, ảnh trên màn nhỏ hơn vật.", "answer": False},
        {"text": "Hai vị trí đó cách nhau $40\\ \\text{cm}$.", "answer": True},
        {"text": "Đưa màn lại gần vật cho tới khi vật–màn còn $80\\ \\text{cm}$ thì vẫn tìm được vị trí thấu kính cho ảnh rõ nét.", "answer": False},
    ],
    explanation=(
        "<p>Ảnh thật trên màn: $d+d'=100$ và $\\dfrac1{21}=\\dfrac1d+\\dfrac1{d'}$ nên $d^2-100d+2100=0$, $\\Delta=10\\,000-8400=1600$.</p>"
        "<p>a) Đúng: $\\Delta\\gt0$ nên có hai nghiệm $d=30\\ \\text{cm}$ và $d=70\\ \\text{cm}$.</p>"
        "<p>b) Sai: ở $d=30\\ \\text{cm}$ thì $d'=70\\ \\text{cm}$, ảnh lớn gấp $\\dfrac{70}{30}\\approx2{,}33$ lần vật.</p>"
        "<p>c) Đúng: $\\ell=70-30=40\\ \\text{cm}$ (kiểm: $\\dfrac{100^2-40^2}{400}=21$).</p>"
        "<p>d) Sai: phải có $L\\ge4f=84\\ \\text{cm}$; $80\\lt84$ nên không còn vị trí nào cho ảnh rõ.</p>"),
    topic=T_DD, form="bai_tap", difficulty="kho",
    distractorNotes={
        "0": "Δ = L² − 4Lf = 1600 > 0 nên có hai vị trí d = 30 cm và d = 70 cm.",
        "1": "Thấu kính gần vật thì ảnh xa thấu kính (d' = 70 > d = 30) nên ảnh lớn hơn vật.",
        "2": "ℓ = d₂ − d₁ = 70 − 30 = 40 cm.",
        "3": "Điều kiện có ảnh thật trên màn là L ≥ 4f = 84 cm; 80 cm không đủ.",
    }))

# ── Câu 7 · Phần III · khoảng cách vật–ảnh
dp7 = anh(14, 21)
assert dp7 == 42 and 21 + dp7 == 63
Q.append(dict(
    type="short_answer",
    question="<p>Vật sáng $AB$ đặt vuông góc với trục chính của một thấu kính hội tụ tiêu cự $14\\ \\text{cm}$, $A$ nằm trên trục chính và cách thấu kính $21\\ \\text{cm}$. Khoảng cách giữa vật và ảnh của nó bằng bao nhiêu cm?</p>",
    answer="63",
    explanation=(
        "<p>$\\dfrac1{d'}=\\dfrac1{14}-\\dfrac1{21}=\\dfrac{1}{42}$ nên $d'=42\\ \\text{cm}$: ảnh thật, khác phía vật.</p>"
        "<p>Khoảng cách vật–ảnh $L=d+d'=21+42=63\\ \\text{cm}$.</p>"
        "<p>Bẫy: trả lời $42$ (khoảng cách ảnh–thấu kính) thay vì khoảng cách vật–ảnh.</p>"),
    topic=T_CT, form="bai_tap", difficulty="trung-binh"))

# ── Câu 8 · Phần III · hai thấu kính ghép sát
fs = 1 / (F(1, 30) + F(1, 20))
dp8 = anh(fs, 18)
assert fs == 12 and dp8 == 36 and fs != 50
Q.append(dict(
    type="short_answer",
    question="<p>Hai thấu kính hội tụ có tiêu cự $30\\ \\text{cm}$ và $20\\ \\text{cm}$ được ghép sát nhau, đồng trục (coi như một thấu kính mỏng). Vật sáng $AB$ đặt vuông góc với trục chính, $A$ nằm trên trục chính và cách hệ $18\\ \\text{cm}$. Ảnh của vật qua hệ cách hệ bao nhiêu cm?</p>",
    answer="36",
    explanation=(
        "<p>Ghép sát: $\\dfrac1f=\\dfrac1{30}+\\dfrac1{20}=\\dfrac5{60}=\\dfrac1{12}$ nên $f=12\\ \\text{cm}$.</p>"
        "<p>$\\dfrac1{d'}=\\dfrac1{12}-\\dfrac1{18}=\\dfrac1{36}$ nên $d'=36\\ \\text{cm}$ (ảnh thật).</p>"
        "<p>Bẫy: cộng tiêu cự $30+20=50\\ \\text{cm}$ — với thấu kính ghép sát, các nghịch đảo tiêu cự mới cộng được.</p>"),
    topic=T_CT, form="bai_tap", difficulty="trung-binh"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) == [0, 1, 2, 3]
for q in Q[6:]:
    assert len(q["answer"]) <= 4
for q in Q:
    assert q["topic"] in (T_DD, T_DUNG, T_CT)
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 and ch not in "\n" for ch in s), s
        assert "<" not in s.replace("<p>", "").replace("</p>", "").replace("<em>", "").replace("</em>", ""), s

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Thấu kính mỏng và kính lúp",
        "topic": T_CT,
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
