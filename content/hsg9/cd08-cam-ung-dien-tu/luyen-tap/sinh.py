# -*- coding: utf-8 -*-
"""CĐ08 Cảm ứng điện từ và dòng điện xoay chiều (lesson 152) — sinh luyen-tap/bundle.json
(8 câu tự chấm: 4 Phần I, 2 Phần II, 2 Phần III). Chỉ có khối exam (theory_html rỗng, worked_examples [])
để upload-lesson.mts giữ nguyên lý thuyết và bài tập mẫu.
Số liệu theo nguon.md mục Luyện tập (tính lại bằng Python + assert); mỗi phương án nhiễu ứng với một cách sai cụ thể.
Số liệu khác bài tập mẫu (152.json), khác tự luận (btm152_tl.py) và khác ví dụ docx (nguon.txt).
Không có lực từ / quy tắc bàn tay trái. R là điện trở tổng cả hai dây; P, U đo ở đầu đường dây.
Chạy: python3 content/hsg9/cd08-cam-ung-dien-tu/luyen-tap/sinh.py"""
import json
from fractions import Fraction as F
from math import sqrt
from pathlib import Path

T_DK = "Điều kiện xuất hiện dòng điện cảm ứng"
T_XC = "Nguyên tắc tạo ra dòng điện xoay chiều"
T_TD = "Các tác dụng nhiệt, quang, từ của dòng xoay chiều"
T_BA = "Máy biến áp"      # truyền tải điện năng cũng gắn topic này (chưa có YCCĐ riêng)


def vn(x, nd=1):
    """Số kiểu Việt Nam: dấu phẩy thập phân, bỏ ,0 thừa."""
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def mc(question, options, answer, explanation, topic, form, diff, notes):
    assert len(options) == 4 and len(set(options)) == 4, options
    assert set(notes) == {"ABCD"[i] for i in range(4) if i != answer}
    return dict(type="multiple_choice", question=question, options=options, answer=answer,
                explanation=explanation, topic=topic, form=form, difficulty=diff, distractorNotes=notes)


def svg_ong_day():
    """Ống dây nằm ngang, đầu A trái, đầu B phải; mũi tên trên các vòng phía trước chỉ dòng đi XUỐNG.
    (Vòng trước dòng đi xuống ⇒ nhìn từ B thấy ngược chiều kim đồng hồ ⇒ B là cực Bắc.)"""
    x0, dx, n, top, bot = 70, 34, 7, 40, 120
    g = []
    for i in range(n):
        x = x0 + i * dx
        # nửa sau (khuất) nét đứt mảnh: từ đáy vòng i lên đỉnh vòng i+1
        if i < n - 1:
            g.append(f'<line x1="{x + 8}" y1="{bot}" x2="{x + dx - 8}" y2="{top}" stroke="currentColor" '
                     f'stroke-width="1.5" stroke-dasharray="4 4" opacity="0.55"/>')
        # nửa trước nét liền: từ đỉnh xuống đáy, hơi nghiêng
        g.append(f'<line x1="{x - 8}" y1="{top}" x2="{x + 8}" y2="{bot}" stroke="currentColor" stroke-width="3"/>')
        # mũi tên chevron giữa nửa trước, hướng xuống
        cx, cy = x, (top + bot) / 2 + 6
        g.append(f'<path d="M{cx - 7} {cy - 9} L{cx + 0.6} {cy + 2} L{cx + 6} {cy - 10}" fill="none" '
                 f'stroke="#d9480f" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    xl, xr = x0 - 8, x0 + (n - 1) * dx + 8
    g.append(f'<line x1="{xl}" y1="{top}" x2="{xl - 30}" y2="{top}" stroke="currentColor" stroke-width="3"/>')
    g.append(f'<line x1="{xr}" y1="{bot}" x2="{xr + 30}" y2="{bot}" stroke="currentColor" stroke-width="3"/>')
    g.append(f'<text x="{xl - 34}" y="{(top + bot) / 2 + 6}" font-size="20" font-weight="700" fill="currentColor" text-anchor="end">A</text>')
    g.append(f'<text x="{xr + 34}" y="{(top + bot) / 2 + 6}" font-size="20" font-weight="700" fill="currentColor">B</text>')
    g.append('<text x="200" y="152" font-size="14" fill="currentColor" text-anchor="middle">'
             'Mũi tên: chiều dòng điện ở các vòng phía trước</text>')
    return ('<svg viewBox="0 0 400 162" width="400" style="max-width:100%;height:auto;display:block;margin:8px auto" '
            'role="img" aria-label="Ống dây nằm ngang, đầu A bên trái, đầu B bên phải, mũi tên chỉ chiều dòng điện '
            'trên các vòng dây phía trước hướng xuống">' + "".join(g) + "</svg>")


Q = []

# ── Câu 1 · Phần I · trường hợp KHÔNG có dòng cảm ứng (đáp án C)
Q.append(mc(
    "<p>Một cuộn dây dẫn kín được nối với một điện kế. Trường hợp nào sau đây <strong>không</strong> xuất hiện dòng điện cảm ứng trong cuộn dây?</p>",
    ["Đưa một cực của nam châm thẳng lại gần một đầu cuộn dây, nam châm nằm trên trục của cuộn dây.",
     "Kéo nam châm thẳng đang nằm trong lòng cuộn dây ra xa cuộn dây.",
     "Quay nam châm thẳng quanh chính trục dọc của nó, trục này trùng với trục của cuộn dây.",
     "Đặt yên một nam châm điện trước cuộn dây rồi ngắt khoá của mạch nam châm điện."],
    2,
    "<p>Dòng cảm ứng chỉ xuất hiện khi số đường sức từ xuyên qua tiết diện cuộn dây kín biến thiên.</p>"
    "<p>Khi quay nam châm quanh chính trục dọc của nó (trùng trục cuộn dây), hình dạng từ trường quanh trục không thay đổi nên số đường sức xuyên qua cuộn dây không đổi: không có dòng. Đáp án C.</p>"
    "<p>A: nam châm lại gần, số đường sức tăng — có dòng.</p>"
    "<p>B: kéo ra xa, số đường sức giảm — có dòng.</p>"
    "<p>D: ngắt khoá, từ trường của nam châm điện mất đi, số đường sức giảm về 0 — có dòng (thoáng qua), dù không có vật nào chuyển động.</p>",
    T_DK, "ly_thuyet", "trung-binh",
    {"A": "Lại gần thì số đường sức qua cuộn dây tăng nên có dòng cảm ứng.",
     "B": "Ra xa thì số đường sức qua cuộn dây giảm nên có dòng cảm ứng.",
     "D": "Nghĩ phải có chuyển động mới có dòng; ngắt khoá làm từ trường mất đi, số đường sức biến thiên nên vẫn có dòng."}))

# ── Câu 2 · Phần I · nắm tay phải (đáp án B)
Q.append(mc(
    "<p>Một ống dây nằm ngang có dòng điện một chiều chạy qua như hình (nét liền là các vòng dây ở phía trước, nét đứt là phần khuất phía sau). Phát biểu nào sau đây đúng?</p>"
    + svg_ong_day(),
    ["Đầu A là cực Bắc, đầu B là cực Nam.",
     "Đầu B là cực Bắc, đầu A là cực Nam.",
     "Cả hai đầu đều là cực Bắc vì dòng điện đi vào ở cả hai đầu ống.",
     "Ống dây không có cực từ vì trong lòng ống không có lõi sắt."],
    1,
    "<p>Nắm tay phải sao cho bốn ngón tay chỉ theo chiều dòng điện trong các vòng dây (phía trước đi xuống); ngón cái choãi ra chỉ sang phải: đường sức trong lòng ống đi từ A sang B.</p>"
    "<p>Đường sức đi ra ở đầu B nên B là cực Bắc, A là cực Nam. Đáp án B.</p>"
    "<p>Kiểm tra: nhìn từ đầu B vào lòng ống, dòng ở các vòng phía trước (bên trái người nhìn) đi xuống, phía sau đi lên — ngược chiều kim đồng hồ, nên B là cực Bắc ✓.</p>"
    "<p>Ống dây không có lõi sắt vẫn có từ trường như một nam châm thẳng; lõi sắt non chỉ làm từ trường mạnh hơn.</p>",
    T_DK, "ly_thuyet", "trung-binh",
    {"A": "Dùng ngược quy tắc (hoặc dùng tay trái): ngón cái chỉ chiều đường sức trong lòng ống, tức hướng về cực Bắc.",
     "C": "Một nam châm (kể cả ống dây) luôn có hai cực khác tên ở hai đầu.",
     "D": "Ống dây có dòng điện đã là một nam châm; lõi sắt non chỉ làm nó mạnh hơn."}))

# ── Câu 3 · Phần I · máy biến áp (đáp án D)
N1, N2, U1 = 1200, 60, 220
U2 = F(U1 * N2, N1)
s_nguoc = F(U1 * N1, N2)
assert U2 == 11 and s_nguoc == 4400
Q.append(mc(
    f"<p>Một máy biến áp lí tưởng có cuộn sơ cấp ${N1}$ vòng, cuộn thứ cấp ${N2}$ vòng. Đặt vào hai đầu cuộn sơ cấp hiệu điện thế xoay chiều ${U1}\\ \\text{{V}}$. Hiệu điện thế ở hai đầu cuộn thứ cấp để hở là</p>",
    ["$0\\ \\text{V}$.", "$220\\ \\text{V}$.", f"${s_nguoc}\\ \\text{{V}}$.", f"${U2}\\ \\text{{V}}$."],
    3,
    f"<p>$\\dfrac{{U_1}}{{U_2}}=\\dfrac{{N_1}}{{N_2}}$ nên $U_2=U_1\\dfrac{{N_2}}{{N_1}}=220\\cdot\\dfrac{{60}}{{1200}}={U2}\\ \\text{{V}}$. Đáp án D.</p>"
    "<p>Cuộn thứ cấp ít vòng hơn nên đây là máy hạ áp: $U_2\\lt U_1$.</p>",
    T_BA, "bai_tap", "de",
    {"A": "Nghĩ hai cuộn cách điện nhau nên không có điện ở thứ cấp; thật ra từ trường biến thiên trong lõi gây cảm ứng ở cuộn thứ cấp.",
     "B": "Nghĩ máy biến áp chỉ đổi cường độ dòng điện, giữ nguyên hiệu điện thế.",
     "C": "Viết ngược tỉ số: U₂ = U₁·N₁/N₂."}))

# ── Câu 4 · Phần I · tăng U 3 lần (đáp án A)
k = 3
assert F(1, k ** 2) == F(1, 9)
Q.append(mc(
    "<p>Truyền tải một công suất điện không đổi trên cùng một đường dây. Nếu tăng hiệu điện thế ở đầu đường dây lên $3$ lần thì công suất hao phí trên dây</p>",
    ["giảm $9$ lần.", "giảm $3$ lần.", "tăng $9$ lần.", "giảm $6$ lần."],
    0,
    "<p>$I=\\dfrac{P}{U}$ giảm $3$ lần, nên $P_{\\text{hp}}=RI^2=\\dfrac{P^2R}{U^2}$ giảm $3^2=9$ lần. Đáp án A.</p>",
    T_BA, "ly_thuyet", "de",
    {"B": "Quên bình phương: hao phí tỉ lệ với I², tức với 1/U².",
     "C": "Dùng nhầm P_hp = U²/R với U ở đầu đường dây; hiệu điện thế đặt lên dây chỉ là ΔU = IR.",
     "D": "Nhân 2 thay vì bình phương: 3·2 = 6."}))

# ── Câu 5 · Phần II · máy phát f = np
p, n_ph = 4, 750
f = F(n_ph, 60) * p
assert f == 50 and 2 * f == 100 and F(50, 2) * 60 == 1500
Q.append(dict(
    type="true_false",
    question="<p>Một máy phát điện xoay chiều có rôto là nam châm gồm $4$ cặp cực, quay đều với tốc độ $750$ vòng/phút.</p>",
    statements=[
        {"text": "Tần số dòng điện do máy phát ra là $50\\ \\text{Hz}$.", "answer": True},
        {"text": "Dòng điện do máy phát ra đổi chiều $50$ lần mỗi giây.", "answer": False},
        {"text": "Một máy phát có rôto $2$ cặp cực muốn phát ra cùng tần số thì phải quay $1500$ vòng/phút.", "answer": True},
        {"text": "Dòng điện xoay chiều không có tác dụng từ vì nó đổi chiều liên tục.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: $n=\\dfrac{750}{60}=12{,}5$ vòng/s, $f=np=12{,}5\\cdot4=50\\ \\text{Hz}$.</p>"
        "<p>b) Sai: mỗi chu kì dòng điện đổi chiều $2$ lần, nên đổi chiều $2\\cdot50=100$ lần mỗi giây.</p>"
        "<p>c) Đúng: $n=\\dfrac{f}{p}=\\dfrac{50}{2}=25$ vòng/s $=1500$ vòng/phút.</p>"
        "<p>d) Sai: dòng xoay chiều vẫn có tác dụng từ (nam châm điện, máy biến áp, chuông điện); từ trường của nó đổi chiều theo dòng điện, nên nó hút được sắt và làm kim nam châm dao động.</p>"),
    topic=T_XC, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "Đổi 750 vòng/phút = 12,5 vòng/s rồi nhân với số cặp cực p = 4.",
        "1": "Mỗi chu kì dòng điện đổi chiều 2 lần: 50 Hz ⇒ 100 lần mỗi giây.",
        "2": "Cùng f thì n tỉ lệ nghịch với p: p giảm 2 lần, n tăng 2 lần.",
        "3": "Dòng xoay chiều vẫn có tác dụng từ; chỉ có điều từ trường đổi chiều theo dòng.",
    }))

# ── Câu 6 · Phần II · truyền tải
P6, U6, R6 = 500_000, 25_000, 50
I6 = F(P6, U6); Php6 = R6 * I6 ** 2; H6 = 1 - Php6 / P6
Php6b = R6 * F(P6, 50_000) ** 2
assert I6 == 20 and Php6 == 20_000 and H6 == F(96, 100) and Php6b == 5000
Q.append(dict(
    type="true_false",
    question="<p>Một đường dây truyền đi công suất $500\\ \\text{kW}$ và hiệu điện thế $25\\ \\text{kV}$, cả hai đo ở đầu đường dây. Điện trở tổng cộng của cả hai dây là $50\\ \\Omega$. Bỏ qua hệ số công suất.</p>",
    statements=[
        {"text": "Cường độ dòng điện trên dây là $20\\ \\text{A}$.", "answer": True},
        {"text": "Công suất hao phí trên dây là $20\\ \\text{kW}$.", "answer": True},
        {"text": "Hiệu suất truyền tải là $98\\,\\%$.", "answer": False},
        {"text": "Nếu truyền cùng công suất đó ở $50\\ \\text{kV}$ thì công suất hao phí còn $10\\ \\text{kW}$.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: $I=\\dfrac{P}{U}=\\dfrac{500\\,000}{25\\,000}=20\\ \\text{A}$.</p>"
        "<p>b) Đúng: $P_{\\text{hp}}=RI^2=50\\cdot20^2=20\\,000\\ \\text{W}=20\\ \\text{kW}$.</p>"
        "<p>c) Sai: $H=1-\\dfrac{20}{500}=0{,}96=96\\,\\%$.</p>"
        "<p>d) Sai: $U$ tăng $2$ lần thì hao phí giảm $2^2=4$ lần, còn $5\\ \\text{kW}$.</p>"),
    topic=T_BA, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "Dòng trên dây I = P/U với P, U ở đầu đường dây.",
        "1": "P_hp = R·I² = 50·400 = 20 000 W.",
        "2": "Tỉ lệ hao phí 20/500 = 4 % nên H = 96 %, không phải 98 %.",
        "3": "Hao phí tỉ lệ với 1/U²: tăng U 2 lần thì hao phí giảm 4 lần (5 kW), không phải 2 lần.",
    }))

# ── Câu 7 · Phần III · I1 của máy biến áp
N1c, N2c, U1c, I2c = 880, 48, 220, F(5, 2)
U2c = F(U1c * N2c, N1c); I1c = U2c * I2c / U1c
assert U2c == 12 and round(float(I1c), 3) == 0.136 and I1c == I2c * F(N2c, N1c)
s7 = vn(I1c, 2).replace("{,}", ",")
assert s7 == "0,14"
Q.append(dict(
    type="short_answer",
    question="<p>Một máy biến áp lí tưởng có cuộn sơ cấp $880$ vòng nối với nguồn xoay chiều $220\\ \\text{V}$, cuộn thứ cấp $48$ vòng cung cấp dòng điện $2{,}5\\ \\text{A}$ cho một thiết bị. Cường độ dòng điện qua cuộn sơ cấp là bao nhiêu ampe? Làm tròn đến hai chữ số sau dấu phẩy.</p>",
    answer=s7,
    explanation=(
        "<p>$U_2=220\\cdot\\dfrac{48}{880}=12\\ \\text{V}$.</p>"
        "<p>Máy lí tưởng: $U_1I_1=U_2I_2$ nên $I_1=\\dfrac{12\\cdot2{,}5}{220}\\approx0{,}136\\ \\text{A}\\approx0{,}14\\ \\text{A}$.</p>"
        "<p>Cách khác: $\\dfrac{I_1}{I_2}=\\dfrac{N_2}{N_1}$ nên $I_1=2{,}5\\cdot\\dfrac{48}{880}\\approx0{,}14\\ \\text{A}$.</p>"
        "<p>Bẫy: viết $\\dfrac{I_1}{I_2}=\\dfrac{N_1}{N_2}$ sẽ ra $\\approx45{,}8\\ \\text{A}$ — máy hạ áp thì dòng sơ cấp phải nhỏ hơn dòng thứ cấp.</p>"),
    topic=T_BA, form="bai_tap", difficulty="trung-binh"))

# ── Câu 8 · Phần III · U tối thiểu để hao phí ≤ 4 %
P8, R8, h8 = 1_000_000, 12, 0.04
Umin = sqrt(P8 * R8 / h8)
assert round(Umin / 1000, 1) == 17.3 and round(Umin) == 17321
assert R8 * (P8 / Umin) ** 2 <= h8 * P8 * (1 + 1e-9)
s8 = vn(Umin / 1000, 1).replace("{,}", ",")
assert s8 == "17,3"
# nếu hiểu 1 MW là công suất nơi tiêu thụ: P = 1 MW/0,96
Utt_hieu_sai = sqrt(P8 / 0.96 * R8 / h8)
assert round(Utt_hieu_sai / 1000, 1) == 17.7 and round(Utt_hieu_sai / 1000, 1) != 17.3
Q.append(dict(
    type="short_answer",
    question="<p>Cần truyền công suất $1\\ \\text{MW}$ (công suất đo ở đầu đường dây) trên đường dây có điện trở tổng cộng $12\\ \\Omega$ sao cho công suất hao phí trên dây không vượt quá $4\\,\\%$ công suất truyền đi. Hiệu điện thế ở đầu đường dây ít nhất là bao nhiêu kilôvôn? Bỏ qua hệ số công suất. Làm tròn đến một chữ số sau dấu phẩy.</p>",
    answer=s8,
    explanation=(
        "<p>$P_{\\text{hp}}=\\dfrac{P^2R}{U^2}\\le0{,}04P$ nên $U^2\\ge\\dfrac{PR}{0{,}04}=\\dfrac{10^6\\cdot12}{0{,}04}=3\\cdot10^8$.</p>"
        "<p>$U\\ge\\sqrt{3\\cdot10^8}\\approx17\\,321\\ \\text{V}\\approx17{,}3\\ \\text{kV}$.</p>"
        "<p>Bẫy: viết $P_{\\text{hp}}=\\dfrac{U^2}{R}$ (coi $U$ ở đầu dây đặt lên hai đầu dây) — sai vì hiệu điện thế trên dây chỉ là $\\Delta U=IR$.</p>"),
    topic=T_BA, form="bai_tap", difficulty="kho"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) == [0, 1, 2, 3]
for q in Q[6:]:
    assert len(q["answer"]) <= 5
for q in Q:
    assert q["topic"] in (T_DK, T_XC, T_TD, T_BA)
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 and ch not in "\n" for ch in s), s
        assert "bàn tay trái" not in s and "lực từ" not in s, s

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Cảm ứng điện từ và dòng điện xoay chiều",
        "topic": T_BA,
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
