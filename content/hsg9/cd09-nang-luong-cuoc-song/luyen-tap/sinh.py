# -*- coding: utf-8 -*-
"""CĐ09 Năng lượng với cuộc sống (lesson 163) — sinh luyen-tap/bundle.json (quiz buổi 16: 8 câu tự chấm,
4 Phần I, 2 Phần II, 2 Phần III). Chỉ có khối exam (theory_html rỗng, worked_examples []) để upload-lesson.mts giữ
nguyên lý thuyết và bài tập mẫu. Số liệu theo nguon.md mục Luyện tập (tính ở tinh.py) + assert ở đây; mỗi phương án
nhiễu ứng với một cách sai cụ thể và khác đáp án đúng. Số liệu khác bài tập mẫu (163.json), khác tự luận
(btm163_tl.py) và khác ví dụ docx. Không biểu giá điện bậc thang, không phương trình hoá học.
Chạy: python3 content/hsg9/cd09-nang-luong-cuoc-song/luyen-tap/sinh.py"""
import json
from math import ceil, isclose
from pathlib import Path

KWH = 3.6e6
# YCCĐ (scripts/data/question-topics.json) — tên y như nguon.md mục "YCCĐ cho Làm bài tương tự"
T_VONG = "Vòng năng lượng trên Trái Đất"                        # 99
T_HT = "Ưu nhược điểm của nhiên liệu hoá thạch"                 # 100
T_TT = "Các dạng năng lượng tái tạo và nguồn gốc"               # 101
T_TK = "Sử dụng năng lượng tiết kiệm, hiệu quả"                 # 102
T_H = "Tính hiệu suất của máy và động cơ"                       # 140
T_HN = "Nhà máy điện hạt nhân và phản ứng nhiệt hạch"           # 227
TOPICS = (T_VONG, T_HT, T_TT, T_TK, T_H, T_HN)


def mc(question, options, answer, explanation, topic, form, diff, notes):
    assert len(options) == 4 and len(set(options)) == 4, options
    assert set(notes) == {"ABCD"[i] for i in range(4) if i != answer}
    return dict(type="multiple_choice", question=question, options=options, answer=answer,
                explanation=explanation, topic=topic, form=form, difficulty=diff, distractorNotes=notes)


Q = []

# ── Câu 1 · Phần I · ngoại lệ không từ bức xạ Mặt Trời (đáp án B)
Q.append(mc(
    r"<p>Dạng năng lượng nào sau đây <strong>không</strong> có nguồn gốc từ bức xạ Mặt Trời?</p>",
    ["Năng lượng gió.", "Năng lượng thuỷ triều.", "Năng lượng sinh khối.", "Năng lượng từ dầu mỏ."],
    1,
    r"<p>Thuỷ triều do lực hấp dẫn của Mặt Trăng (và Mặt Trời) cùng chuyển động tự quay của Trái Đất gây ra, không do bức xạ Mặt Trời. Đáp án B.</p>"
    r"<p>Gió: bức xạ Mặt Trời làm không khí nóng không đều.</p>"
    r"<p>Sinh khối: thực vật quang hợp nhờ ánh sáng Mặt Trời.</p>"
    r"<p>Dầu mỏ: sinh vật cổ (sống nhờ quang hợp) bị chôn vùi hàng triệu năm — năng lượng Mặt Trời được tích trữ.</p>"
    r"<p>Ba ngoại lệ cần nhớ: thuỷ triều, địa nhiệt, hạt nhân.</p>",
    T_VONG, "ly_thuyet", "de",
    {"A": "Gió sinh ra do bức xạ Mặt Trời làm nóng không khí không đều.",
     "C": "Sinh khối tích trữ năng lượng Mặt Trời qua quang hợp.",
     "D": "Dầu mỏ là năng lượng Mặt Trời được sinh vật cổ tích trữ, rồi bị chôn vùi."}))

# ── Câu 2 · Phần I · hiệu suất chuỗi (đáp án A)
H1, H2, H3 = 0.90, 0.40, 0.95
H = H1 * H2 * H3
s_tb = (H1 + H2 + H3) / 3          # trung bình cộng
s_min = min(H1, H2, H3)            # chỉ lấy khâu yếu nhất
s_max = max(H1, H2, H3)            # chỉ lấy khâu cuối/khâu tốt nhất
assert isclose(H, 0.342) and isclose(s_tb, 0.75) and s_min == 0.40 and s_max == 0.95
assert len({round(x, 4) for x in (H, s_tb, s_min, s_max)}) == 4
Q.append(mc(
    r"<p>Một máy biến đổi năng lượng gồm ba khâu nối tiếp nhau, hiệu suất lần lượt là $90\,\%$, $40\,\%$ và $95\,\%$. Hiệu suất của cả máy là</p>",
    [r"$34{,}2\,\%$.", r"$40\,\%$.", r"$75\,\%$.", r"$95\,\%$."],
    0,
    r"<p>Năng lượng ra của khâu trước là năng lượng vào của khâu sau, nên hiệu suất chung là tích:</p>"
    r"<p>$H=H_1H_2H_3=0{,}90\cdot0{,}40\cdot0{,}95=0{,}342=34{,}2\,\%$. Đáp án A.</p>"
    r"<p>Hiệu suất chung luôn nhỏ hơn hiệu suất của khâu kém nhất ($40\,\%$).</p>",
    T_H, "bai_tap", "de",
    {"B": "Chỉ lấy hiệu suất của khâu kém nhất, bỏ qua hao phí ở hai khâu còn lại.",
     "C": "Lấy trung bình cộng ba hiệu suất thay vì nhân.",
     "D": "Chỉ lấy hiệu suất khâu cuối, quên các khâu phía trước."}))

# ── Câu 3 · Phần I · gió P ∝ v³ (đáp án C)
con_lai = (8 / 10) ** 3
giam = 1 - con_lai
s_tuyen = 1 - 8 / 10                 # coi P ∝ v
s_bp = 1 - (8 / 10) ** 2             # coi P ∝ v² (nhầm động năng)
s_conlai = con_lai                   # đọc "còn lại" thành "giảm"
assert round(giam * 100, 1) == 48.8 and round(s_tuyen * 100) == 20 and round(s_bp * 100) == 36 \
    and round(s_conlai * 100, 1) == 51.2
assert len({round(x, 4) for x in (giam, s_tuyen, s_bp, s_conlai)}) == 4
Q.append(mc(
    r"<p>Một tuabin gió đang làm việc dưới tốc độ định mức, công suất tỉ lệ với lập phương tốc độ gió. Khi tốc độ gió giảm từ $10\ \text{m/s}$ xuống $8\ \text{m/s}$ thì công suất của tuabin</p>",
    [r"giảm $20\,\%$.", r"giảm $36\,\%$.", r"giảm $48{,}8\,\%$.", r"giảm $51{,}2\,\%$."],
    2,
    r"<p>$\dfrac{P'}{P}=\left(\dfrac{8}{10}\right)^3=0{,}512$: công suất còn $51{,}2\,\%$.</p>"
    r"<p>Vậy công suất giảm $100\,\%-51{,}2\,\%=48{,}8\,\%$. Đáp án C.</p>"
    r"<p>Gió chỉ giảm $20\,\%$ mà công suất giảm gần một nửa — vì thế điện gió rất thất thường.</p>",
    T_TT, "bai_tap", "trung-binh",
    {"A": "Coi công suất tỉ lệ bậc nhất với tốc độ gió.",
     "B": "Dùng bình phương tốc độ (nhầm với động năng của 1 kg không khí), quên lượng không khí qua cánh mỗi giây cũng tỉ lệ với v.",
     "D": "51,2 % là phần công suất còn lại, không phải phần giảm."}))

# ── Câu 4 · Phần I · điện hạt nhân (đáp án D)
Q.append(mc(
    r"<p>Phát biểu nào sau đây về năng lượng hạt nhân là <strong>đúng</strong>?</p>",
    ["Năng lượng hạt nhân là năng lượng tái tạo vì urani có rất nhiều trong tự nhiên.",
     "Nhà máy điện hạt nhân hiện nay dùng phản ứng nhiệt hạch giống như trong lõi Mặt Trời.",
     "Khi vận hành, nhà máy điện hạt nhân thải nhiều khí CO₂ như nhà máy nhiệt điện than.",
     "Nhà máy điện hạt nhân dùng phản ứng phân hạch urani; phần sau (hơi nước → tuabin → máy phát) giống nhà máy nhiệt điện."],
    3,
    r"<p>Năng lượng phân hạch làm nóng nước thành hơi, hơi quay tuabin, tuabin quay máy phát — nửa sau giống hệt nhà máy nhiệt điện. Đáp án D.</p>"
    r"<p>A sai: urani là khoáng chất có hạn, tự nhiên không bổ sung lại nên không tái tạo.</p>"
    r"<p>B sai: nhiệt hạch (hạt nhân nhẹ kết hợp) chưa dùng phát điện thương mại; nhà máy dùng phân hạch (hạt nhân nặng vỡ ra).</p>"
    r"<p>C sai: không có sự cháy nên khi vận hành gần như không thải CO₂.</p>",
    T_HN, "ly_thuyet", "trung-binh",
    {"A": "Urani có hạn trong vỏ Trái Đất, không được bổ sung — không tái tạo.",
     "B": "Nhầm phân hạch (nhà máy điện) với nhiệt hạch (Mặt Trời).",
     "C": "Nhà máy hạt nhân không đốt nhiên liệu nên khi vận hành không thải CO₂ như nhà máy than."}))

# ── Câu 5 · Phần II · thuỷ điện
d, L, h, Ht = 1e4, 100, 60, 0.85
Pn = d * L * h
Pd = Ht * Pn
assert isclose(Pn, 60e6) and isclose(Pd, 51e6)
assert isclose(Ht * d * L * 30 / Pd, 0.5)          # h giảm một nửa → P giảm 2 lần, không phải 4
assert L * 3600 == 3.6e5
Q.append(dict(
    type="true_false",
    question=r"<p>Một nhà máy thuỷ điện có độ cao cột nước $h=60\ \text{m}$, lưu lượng nước qua tuabin $L=100\ \text{m}^3/\text{s}$, hiệu suất cả nhà máy $85\,\%$. Trọng lượng riêng của nước $d=10\,000\ \text{N/m}^3$.</p>",
    statements=[
        {"text": r"Công suất của dòng nước chảy qua tuabin là $60\ \text{MW}$.", "answer": True},
        {"text": r"Công suất điện của nhà máy là $51\ \text{MW}$.", "answer": True},
        {"text": r"Nếu mực nước hạ làm $h$ còn $30\ \text{m}$ (giữ nguyên $L$ và hiệu suất) thì công suất điện giảm $4$ lần.", "answer": False},
        {"text": r"Trong $1$ giờ có $3{,}6\cdot10^5\ \text{m}^3$ nước chảy qua tuabin.", "answer": True},
    ],
    explanation=(
        r"<p>a) Đúng: mỗi giây có trọng lượng nước $dL=10^4\cdot100=10^6\ \text{N}$ rơi qua độ cao $60\ \text{m}$, nên $P_n=dLh=10^6\cdot60=6\cdot10^7\ \text{W}=60\ \text{MW}$.</p>"
        r"<p>b) Đúng: $P_đ=HP_n=0{,}85\cdot60=51\ \text{MW}$.</p>"
        r"<p>c) Sai: $P_đ=HdLh$ tỉ lệ bậc nhất với $h$; $h$ giảm $2$ lần thì $P_đ$ giảm $2$ lần (còn $25{,}5\ \text{MW}$).</p>"
        r"<p>d) Đúng: $V=Lt=100\cdot3600=3{,}6\cdot10^5\ \text{m}^3$.</p>"),
    topic=T_TT, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "P_n = d·L·h = 10 000·100·60 = 6·10⁷ W.",
        "1": "P_đ = H·P_n = 0,85·60 MW = 51 MW.",
        "2": "Công suất tỉ lệ bậc nhất với h, không phải bình phương: h giảm 2 lần thì P giảm 2 lần.",
        "3": "V = L·t = 100 m³/s · 3600 s = 360 000 m³.",
    }))

# ── Câu 6 · Phần II · đốt than phát điện, hiệu ứng nhà kính
m_t, q_t, H6 = 1000, 2.7e7, 0.35
Q6 = m_t * q_t
A_khongH = Q6 / KWH
A6 = H6 * Q6 / KWH
assert isclose(Q6, 2.7e10) and isclose(A_khongH, 7500) and isclose(A6, 2625)
co2 = 2.5 * m_t
assert co2 == 2500 and round(co2 / A6, 2) == 0.95 and round(co2 / A_khongH, 2) == 0.33
Q.append(dict(
    type="true_false",
    question=r"<p>Một nhà máy nhiệt điện có hiệu suất $35\,\%$ đốt hết $1$ tấn than đá có năng suất toả nhiệt $q=2{,}7\cdot10^7\ \text{J/kg}$; cứ $1\ \text{kg}$ than cháy thải ra $2{,}5\ \text{kg}$ khí CO₂.</p>",
    statements=[
        {"text": r"Than toả ra nhiệt lượng $2{,}7\cdot10^{10}\ \text{J}$.", "answer": True},
        {"text": r"Điện năng nhà máy thu được là $7500\ \text{kWh}$.", "answer": False},
        {"text": r"Tính trung bình, mỗi kWh điện nhà máy làm ra kèm theo khoảng $0{,}95\ \text{kg}$ khí CO₂ thải ra.", "answer": True},
        {"text": "Nếu khí quyển hoàn toàn không có hiệu ứng nhà kính thì Trái Đất sẽ ấm áp và thuận lợi cho sự sống hơn.", "answer": False},
    ],
    explanation=(
        r"<p>a) Đúng: $Q=qm=2{,}7\cdot10^7\cdot1000=2{,}7\cdot10^{10}\ \text{J}$.</p>"
        r"<p>b) Sai: $A=HQ=0{,}35\cdot2{,}7\cdot10^{10}=9{,}45\cdot10^9\ \text{J}=2625\ \text{kWh}$. Con số $7500\ \text{kWh}$ là toàn bộ nhiệt lượng đổi ra kWh, chưa nhân hiệu suất.</p>"
        r"<p>c) Đúng: CO₂ thải ra $2{,}5\cdot1000=2500\ \text{kg}$; chia cho điện năng $2625\ \text{kWh}$ được $\dfrac{2500}{2625}\approx0{,}95\ \text{kg/kWh}$. (Nếu quên hiệu suất, chia cho $7500\ \text{kWh}$ sẽ ra $0{,}33\ \text{kg/kWh}$ — sai.)</p>"
        r"<p>d) Sai: hiệu ứng nhà kính tự nhiên là cần thiết; không có nó nhiệt độ trung bình của Trái Đất chỉ khoảng $-18\ ^\circ\text{C}$. Điều đáng lo là hiệu ứng bị con người <em>tăng cường</em>.</p>"),
    topic=T_HT, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "Q = q·m với m = 1000 kg.",
        "1": "Phải nhân hiệu suất: chỉ 35 % nhiệt lượng thành điện năng, 2625 kWh.",
        "2": "m_CO₂ = 2,5·1000 = 2500 kg; chia cho 2625 kWh (đã nhân hiệu suất) được ≈ 0,95 kg/kWh.",
        "3": "Không có hiệu ứng nhà kính, Trái Đất trung bình chỉ khoảng −18 °C.",
    }))

# ── Câu 7 · Phần III · số tấm pin Mặt Trời
A_can, S_tam, Hp, I, t_d = 9, 1.8, 0.20, 1000, 4.5
a_tam = Hp * I * S_tam * t_d / 1000          # kWh/ngày mỗi tấm
n = A_can / a_tam
n_tam = ceil(n)
assert isclose(a_tam, 1.62) and round(n, 2) == 5.56 and n_tam == 6
assert round(A_can / (Hp * I * S_tam * 12 / 1000), 2) == 2.08    # bẫy lấy 12 h trời sáng
Q.append(dict(
    type="short_answer",
    question=r"<p>Một hộ gia đình cần $9\ \text{kWh}$ điện mỗi ngày và muốn lắp pin Mặt Trời. Mỗi tấm pin có diện tích $1{,}8\ \text{m}^2$, hiệu suất $20\,\%$. Nơi đó mỗi ngày tương đương $4{,}5$ giờ nắng đỉnh với cường độ bức xạ $1000\ \text{W/m}^2$. Bỏ qua mọi hao phí khác. Cần lắp tối thiểu bao nhiêu tấm pin?</p>",
    answer=str(n_tam),
    explanation=(
        r"<p>Công suất đỉnh mỗi tấm: $P=HIS=0{,}2\cdot1000\cdot1{,}8=360\ \text{W}$.</p>"
        r"<p>Điện năng mỗi tấm mỗi ngày: $360\ \text{W}\cdot4{,}5\ \text{h}=1620\ \text{Wh}=1{,}62\ \text{kWh}$.</p>"
        r"<p>$n=\dfrac{9}{1{,}62}\approx5{,}56$; số tấm phải làm tròn <em>lên</em>: $6$ tấm (5 tấm chỉ cho $8{,}1\ \text{kWh}$, thiếu).</p>"
        r"<p>Bẫy: làm tròn thành $5$ hoặc nhân với $12$ giờ trời sáng thay vì $4{,}5$ giờ nắng đỉnh.</p>"),
    topic=T_TK, form="bai_tap", difficulty="trung-binh"))

# ── Câu 8 · Phần III · than đốt mỗi giờ ở nhà máy nhiệt điện
Pd8, H8, q8 = 450e6, 0.375, 2.7e7
Pnl = Pd8 / H8
m_gio = Pnl * 3600 / q8 / 1000                  # tấn
assert isclose(Pnl, 1.2e9) and isclose(m_gio, 160)
assert isclose(Pd8 * H8 * 3600 / q8 / 1000, 22.5)   # bẫy nhân H
Q.append(dict(
    type="short_answer",
    question=r"<p>Một nhà máy nhiệt điện có công suất điện $450\ \text{MW}$, hiệu suất cả nhà máy $37{,}5\,\%$, đốt than có năng suất toả nhiệt $q=2{,}7\cdot10^7\ \text{J/kg}$. Bỏ qua hao phí trên đường dây tải điện. Mỗi giờ nhà máy đốt bao nhiêu tấn than?</p>",
    answer=str(round(m_gio)),
    explanation=(
        r"<p>Công suất nhiệt than cung cấp: $P_{nl}=\dfrac{P_đ}{H}=\dfrac{450}{0{,}375}=1200\ \text{MW}$.</p>"
        r"<p>Nhiệt lượng trong $1$ giờ: $Q=1{,}2\cdot10^9\cdot3600=4{,}32\cdot10^{12}\ \text{J}$.</p>"
        r"<p>$m=\dfrac{Q}{q}=\dfrac{4{,}32\cdot10^{12}}{2{,}7\cdot10^7}=1{,}6\cdot10^5\ \text{kg}=160$ tấn.</p>"
        r"<p>Bẫy: nhân $450\ \text{MW}$ với $H$ thay vì chia (ra $22{,}5$ tấn).</p>"),
    topic=T_H, form="bai_tap", difficulty="trung-binh"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) == [0, 1, 2, 3]
for q in Q[6:]:
    assert len(q["answer"]) <= 4
for q in Q:
    assert q["topic"] in TOPICS
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 and ch not in "\n" for ch in s), s
        assert "<" not in s.replace("<p>", "").replace("</p>", "").replace("<em>", "").replace("</em>", "") \
            .replace("<strong>", "").replace("</strong>", ""), s

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Năng lượng với cuộc sống",
        "topic": T_TT,
        "difficulty": "trung-binh",
        "duration_minutes": 30,
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
