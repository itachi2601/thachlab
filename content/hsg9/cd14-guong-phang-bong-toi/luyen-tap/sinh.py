# -*- coding: utf-8 -*-
"""CĐ14 Gương phẳng, bóng tối và nửa tối (lesson 158) — sinh luyen-tap/bundle.json (8 câu tự chấm: 4 Phần I, 2 Phần II, 2 Phần III).
Chỉ có khối exam (theory_html rỗng, worked_examples []) để upload-lesson.mts giữ nguyên lý thuyết và bài tập mẫu.
Số liệu theo nguon.md mục Luyện tập (đã tính ở tinh.py), khác bài tập mẫu (158.json), khác tự luận (btm158_tl.py) và khác docx.
Mỗi phương án nhiễu ứng với một cách sai cụ thể và khác đáp án đúng (assert).
Chạy: python3 content/hsg9/cd14-guong-phang-bong-toi/luyen-tap/sinh.py"""
import json
from math import radians, tan
from pathlib import Path

T_PX = "Định luật phản xạ ánh sáng"
T_ANH = "Ảnh của vật tạo bởi gương phẳng"
T_BONG = "Bóng tối, bóng nửa tối"


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

# ── Câu 1 · Phần I · góc giữa tia tới và tia phản xạ (đáp án D)
beta = 25
i1 = 90 - beta
goc = 2 * i1
s_2beta, s_i, s_beta = 2 * beta, i1, beta
assert goc == 130 and len({goc, s_2beta, s_i, s_beta}) == 4
opts1 = sorted([s_beta, s_2beta, s_i, goc])
assert opts1.index(goc) == 3
Q.append(mc(
    "<p>Chiếu một tia sáng tới một gương phẳng, tia tới hợp với <em>mặt gương</em> một góc $25^\\circ$. Góc hợp bởi tia tới và tia phản xạ bằng</p>",
    [f"${x}^\\circ$." for x in opts1],
    3,
    "<p>Góc tới đo với pháp tuyến: $i=90^\\circ-25^\\circ=65^\\circ$.</p>"
    "<p>Góc phản xạ $i'=i=65^\\circ$ nên góc giữa tia tới và tia phản xạ là $i+i'=2i=130^\\circ$. Đáp án D.</p>",
    T_PX, "bai_tap", "de",
    {"A": "Lấy luôn góc với mặt gương (25°) làm đáp số.",
     "B": "Nhân đôi góc với mặt gương (2·25°) thay vì nhân đôi góc tới 65°.",
     "C": "65° mới chỉ là góc tới i, chưa cộng góc phản xạ i'."}))

# ── Câu 2 · Phần I · số ảnh qua hai gương 36° (đáp án B) — khác D7a (72°, 60°, 45°, 100°) và tự luận (30°, 120°)
al2 = 36
m2 = 360 // al2
n_anh = m2 - 1            # 360/α = 10 chẵn → 9 ảnh với mọi vị trí vật
assert 360 % al2 == 0 and m2 % 2 == 0 and n_anh == 9 and len({n_anh, n_anh - 1, m2}) == 3
Q.append(mc(
    "<p>Hai gương phẳng đủ rộng, mặt phản xạ quay vào nhau, hợp với nhau góc $36^\\circ$. Đặt một điểm sáng $S$ ở vị trí bất kì trong góc giữa hai gương. Số ảnh của $S$ tạo bởi hệ hai gương là</p>",
    [f"${n_anh - 1}$.", f"${n_anh}$.", f"${m2}$.", "vô số."],
    1,
    "<p>$\\dfrac{360^\\circ}{36^\\circ}=10$ là số nguyên chẵn nên số ảnh là $10-1=9$, không phụ thuộc vị trí của $S$ trong góc. Đáp án B.</p>"
    "<p>Các ảnh nằm trên đường tròn tâm là giao tuyến hai gương, bán kính bằng khoảng cách từ $S$ tới giao tuyến.</p>",
    T_ANH, "bai_tap", "trung-binh",
    {"A": "Trừ 2 (bỏ thêm một ảnh) — chỉ có hai ảnh trùng nhau khi 360°/α lẻ và vật nằm trên phân giác.",
     "C": "Đếm cả vật S: 360°/α = 10 điểm gồm vật và 9 ảnh.",
     "D": "Vô số ảnh chỉ xảy ra khi hai gương song song (α = 0)."}))

# ── Câu 3 · Phần I · gương quay (đáp án C)
dlt = 12
quay = 2 * dlt
assert quay == 24 and len({quay, dlt, dlt / 2, 4 * dlt}) == 4
Q.append(mc(
    "<p>Giữ cố định một tia sáng chiếu tới gương phẳng. Quay gương một góc $12^\\circ$ quanh một trục nằm trong mặt gương, đi qua điểm tới và vuông góc với mặt phẳng tới. Tia phản xạ quay một góc</p>",
    ["$6^\\circ$.", "$12^\\circ$.", "$24^\\circ$.", "$48^\\circ$."],
    2,
    "<p>Gương quay $\\delta$ thì pháp tuyến quay $\\delta$, góc tới thay đổi $\\delta$.</p>"
    "<p>Tia tới đứng yên còn tia phản xạ đối xứng với tia tới qua pháp tuyến, nên tia phản xạ quay $2\\delta=24^\\circ$ cùng chiều quay của gương. Đáp án C.</p>",
    T_PX, "bai_tap", "trung-binh",
    {"A": "Chia đôi thay vì nhân đôi góc quay.",
     "B": "Cho rằng tia phản xạ quay cùng góc với gương (quên 2δ).",
     "D": "Nhân 4: nhân đôi hai lần (một lần cho góc tới, một lần cho góc giữa hai tia)."}))

# ── Câu 4 · Phần I · khái niệm vùng nửa tối (đáp án A)
Q.append(mc(
    "<p>Đặt một vật chắn sáng giữa một nguồn sáng rộng (bóng đèn tròn lớn) và màn chắn. Vùng nửa tối trên màn là vùng</p>",
    ["chỉ nhận được ánh sáng từ một phần của nguồn sáng.",
     "nhận ánh sáng yếu vì nằm xa nguồn sáng.",
     "hoàn toàn không nhận được ánh sáng từ nguồn.",
     "chỉ xuất hiện khi nguồn sáng là nguồn điểm."],
    0,
    "<p>Từ một điểm trong vùng nửa tối nhìn về nguồn, vật chắn che mất một phần nguồn, phần còn lại vẫn chiếu tới. Đáp án A.</p>"
    "<p>Vùng không nhận ánh sáng nào là vùng tối; nguồn điểm chỉ cho vùng tối, không có vùng nửa tối.</p>",
    T_BONG, "ly_thuyet", "de",
    {"B": "Nửa tối do bị che một phần nguồn, không phải do ở xa nguồn.",
     "C": "Đó là vùng tối (bóng tối).",
     "D": "Ngược lại: nguồn điểm chỉ cho vùng tối; vùng nửa tối cần nguồn rộng."}))

# ── Câu 5 · Phần II · gương thấy toàn thân
h, hm, kc = 1.60, 1.50, 2.0
nguoi_anh = 2 * kc
cao_min = h / 2
mep_duoi = hm / 2
mep_tren = (hm + h) / 2
assert nguoi_anh == 4.0 and round(cao_min, 2) == 0.80 and round(mep_duoi, 2) == 0.75 and round(mep_tren - mep_duoi, 2) == 0.80
Q.append(dict(
    type="true_false",
    question="<p>Một người cao $1{,}60\\ \\text{m}$, mắt cách sàn $1{,}50\\ \\text{m}$, đứng thẳng trước một gương phẳng treo thẳng đứng trên tường, cách gương $2{,}0\\ \\text{m}$. Sàn nằm ngang.</p>",
    statements=[
        {"text": "Ảnh của người cách người đó $4{,}0\\ \\text{m}$.", "answer": True},
        {"text": "Để thấy được toàn bộ ảnh của mình, gương phải cao ít nhất $0{,}80\\ \\text{m}$.", "answer": True},
        {"text": "Khi đó mép dưới của gương phải cách sàn đúng $0{,}80\\ \\text{m}$.", "answer": False},
        {"text": "Nếu người lùi ra xa gương thì cần gương cao hơn mới thấy được toàn thân.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: ảnh đối xứng với người qua gương, cách gương $2{,}0\\ \\text{m}$, nên cách người $2\\cdot2{,}0=4{,}0\\ \\text{m}$.</p>"
        "<p>b) Đúng: tia từ chân và từ đỉnh đầu tới mắt cắt gương tại trung điểm các đoạn tương ứng (đường trung bình), nên gương tối thiểu $\\dfrac{h}{2}=0{,}80\\ \\text{m}$.</p>"
        "<p>c) Sai: mép dưới ở trung điểm của đoạn từ chân tới mắt: $\\dfrac{h_m}{2}=0{,}75\\ \\text{m}$ (mép trên $\\dfrac{1{,}50+1{,}60}{2}=1{,}55\\ \\text{m}$).</p>"
        "<p>d) Sai: các kết quả $\\dfrac{h}{2}$, $\\dfrac{h_m}{2}$ không chứa khoảng cách tới gương, nên lùi xa không thấy thêm và cũng không cần gương cao hơn.</p>"),
    topic=T_ANH, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "Khoảng người–ảnh bằng 2 lần khoảng người–gương.",
        "1": "Gương tối thiểu bằng nửa chiều cao người: 1,60/2 = 0,80 m.",
        "2": "Mép dưới = h_m/2 = 0,75 m, không phải h/2 = 0,80 m (lệch nửa khoảng mắt–đỉnh đầu).",
        "3": "h/2 và h_m/2 không phụ thuộc khoảng cách; lùi xa không thấy nhiều hơn, cũng không cần gương cao hơn.",
    }))

# ── Câu 6 · Phần II · nguồn rộng: vùng tối, nửa tối
Dn, d, a, L = 10, 20, 40, 100
k = L / a
bong_diem = d * k
d_t = Dn + (d - Dn) * k
d_n = (d + Dn) * k - Dn
assert bong_diem == 50 and d_t == 35 and d_n == 65 and (d_n - d_t) / 2 == 15
assert Dn + (d - Dn) * 150 / a > d_t     # lùi màn (L = 150 cm) thì vùng tối lớn lên vì d > D_n
Q.append(dict(
    type="true_false",
    question="<p>Một bóng đèn hình đĩa đường kính $10\\ \\text{cm}$ chiếu sáng một màn đặt song song, cách đèn $100\\ \\text{cm}$. Giữa đèn và màn, cách đèn $40\\ \\text{cm}$, đặt một đĩa chắn sáng đường kính $20\\ \\text{cm}$ song song với màn; tâm đèn, tâm đĩa và tâm vùng bóng cùng nằm trên một đường thẳng vuông góc với màn.</p>",
    statements=[
        {"text": "Nếu coi đèn là nguồn điểm thì bóng của đĩa trên màn có đường kính $50\\ \\text{cm}$.", "answer": True},
        {"text": "Với đèn thật (nguồn rộng), vùng tối trên màn có đường kính $35\\ \\text{cm}$.", "answer": True},
        {"text": "Mép ngoài của vùng nửa tối là đường tròn đường kính $50\\ \\text{cm}$.", "answer": False},
        {"text": "Lùi màn ra xa đèn hơn thì vùng tối trên màn nhỏ lại.", "answer": False},
    ],
    explanation=(
        "<p>Mọi khoảng cách đo từ đèn: $a=40\\ \\text{cm}$, $L=100\\ \\text{cm}$, $\\dfrac{L}{a}=2{,}5$.</p>"
        "<p>a) Đúng: nguồn điểm, đồng dạng đỉnh tại nguồn: $20\\cdot2{,}5=50\\ \\text{cm}$.</p>"
        "<p>b) Đúng: tia cùng mép: $d_t=D_n+(d-D_n)\\dfrac{L}{a}=10+10\\cdot2{,}5=35\\ \\text{cm}$.</p>"
        "<p>c) Sai: tia chéo mép: $d_n=(d+D_n)\\dfrac{L}{a}-D_n=30\\cdot2{,}5-10=65\\ \\text{cm}$; $50\\ \\text{cm}$ là bóng khi coi đèn là nguồn điểm.</p>"
        "<p>d) Sai: đĩa chắn ($20\\ \\text{cm}$) lớn hơn đèn ($10\\ \\text{cm}$) nên hai tia cùng mép loe ra, $d_t$ tăng theo $L$: lùi màn thì vùng tối lớn lên.</p>"),
    topic=T_BONG, form="bai_tap", difficulty="kho",
    distractorNotes={
        "0": "Nguồn điểm: d' = d·L/a = 20·100/40 = 50 cm (đo từ nguồn, không phải từ đĩa).",
        "1": "Vùng tối giới hạn bởi tia cùng mép: 10 + (20 − 10)·2,5 = 35 cm.",
        "2": "Mép ngoài nửa tối do tia chéo mép: (20 + 10)·2,5 − 10 = 65 cm; 50 cm là bóng của nguồn điểm.",
        "3": "Vật chắn lớn hơn nguồn thì vùng tối lớn lên khi lùi màn; chỉ khi vật nhỏ hơn nguồn vùng tối mới thu hẹp.",
    }))

# ── Câu 7 · Phần III · tốc độ đỉnh bóng
H7, h7, v7 = 4.0, 1.6, 1.2
v_dinh = v7 * H7 / (H7 - h7)
s_v, s_bong = v7, v7 * h7 / (H7 - h7)
assert round(v_dinh, 2) == 2.0 and round(s_bong, 2) == 0.8 and len({round(v_dinh, 2), s_v, round(s_bong, 2)}) == 3
Q.append(dict(
    type="short_answer",
    question="<p>Một bóng đèn nhỏ treo cách mặt đường nằm ngang $4{,}0\\ \\text{m}$. Một người cao $1{,}6\\ \\text{m}$ đi thẳng ra xa chân cột đèn với tốc độ không đổi $1{,}2\\ \\text{m/s}$. Đỉnh bóng của người trên mặt đường chuyển động với tốc độ bao nhiêu $\\text{m/s}$?</p>",
    answer=vn(v_dinh).replace("{,}", ","),
    explanation=(
        "<p>Người cách chân cột $x$, bóng dài $\\ell$: $\\dfrac{\\ell}{x}=\\dfrac{h}{H-h}=\\dfrac{1{,}6}{2{,}4}=\\dfrac23$.</p>"
        "<p>Đỉnh bóng cách chân cột $x+\\ell=\\dfrac{H}{H-h}\\,x=\\dfrac53x$, nên chạy nhanh gấp $\\dfrac53$ lần người: $v_{\\text{đỉnh}}=\\dfrac53\\cdot1{,}2=2{,}0\\ \\text{m/s}$.</p>"
        "<p>Bẫy: trả lời $1{,}2\\ \\text{m/s}$ (bằng tốc độ người) hoặc $0{,}8\\ \\text{m/s}$ (đó là tốc độ bóng dài thêm, không phải tốc độ đỉnh bóng).</p>"),
    topic=T_BONG, form="bai_tap", difficulty="trung-binh"))

# ── Câu 8 · Phần III · vệt laser khi gương quay
R8, d8 = 2.5, 4
dx = R8 * tan(radians(2 * d8))
s_quen = R8 * tan(radians(d8))
assert round(dx * 100) == 35 and round(dx * 100, 1) == 35.1 and round(s_quen * 100, 1) == 17.5
Q.append(dict(
    type="short_answer",
    question="<p>Chiếu một tia laser cố định vào một gương phẳng nhỏ; tia phản xạ đập vuông góc vào một bức tường cách điểm tới $2{,}5\\ \\text{m}$. Quay gương một góc $4^\\circ$ quanh trục đi qua điểm tới, vuông góc với mặt phẳng tới. Vệt sáng trên tường dịch đi bao nhiêu xentimét? Làm tròn đến xentimét.</p>",
    answer=str(round(dx * 100)),
    explanation=(
        "<p>Gương quay $4^\\circ$ nên tia phản xạ quay $2\\cdot4^\\circ=8^\\circ$.</p>"
        "<p>Lúc đầu tia phản xạ vuông góc tường; sau khi quay, vệt dịch $x=2{,}5\\cdot\\tan8^\\circ\\approx0{,}351\\ \\text{m}\\approx35\\ \\text{cm}$.</p>"
        "<p>Bẫy: quên nhân đôi góc quay, lấy $2{,}5\\cdot\\tan4^\\circ\\approx17{,}5\\ \\text{cm}$.</p>"),
    topic=T_PX, form="bai_tap", difficulty="kho"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) == [0, 1, 2, 3]
assert [[s["answer"] for s in q["statements"]] for q in Q[4:6]] == [[True, True, False, False]] * 2
for q in Q[6:]:
    assert len(q["answer"]) <= 4
for q in Q:
    assert q["topic"] in (T_PX, T_ANH, T_BONG)
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 and ch not in "\n" for ch in s), s

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Gương phẳng, bóng tối và nửa tối",
        "topic": T_ANH,
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
