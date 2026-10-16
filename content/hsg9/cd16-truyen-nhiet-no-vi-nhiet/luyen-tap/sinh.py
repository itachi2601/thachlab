# -*- coding: utf-8 -*-
"""CĐ16 Truyền nhiệt và sự nở vì nhiệt (bài 164) — sinh luyen-tap/bundle.json (8 câu tự chấm).
4 câu Phần I (A–D), 2 câu Phần II (a)–d) Đúng/Sai), 2 câu Phần III (đáp số ≤ 4 ký tự).
Mỗi phương án nhiễu ứng với một cách sai cụ thể (ghi ở distractorNotes); số liệu tính ở đây và assert.
Số liệu khác bài tập mẫu D1–D6 (nguon.md). Chạy: python3 sinh.py"""
import json
from fractions import Fraction as F
from pathlib import Path

OUT = Path(__file__).with_name("bundle.json")
YC_NHIET = "Nhiệt độ và cân bằng nhiệt"
YC_NOI_NANG = "Nội năng và hai cách làm biến đổi nội năng"


def vn(x, nd=1):
    """Số kiểu Việt: dấu phẩy thập phân, bỏ số 0 thừa."""
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def vnk(x, nd=1):
    """Số dùng TRONG $…$: dấu phẩy bọc {,} để KaTeX không chèn khoảng trắng."""
    return vn(x, nd).replace(",", "{,}")


def br(text):
    """ContentHtml không giữ \n — mỗi ý một dòng bằng <br>."""
    return text.strip().replace("\n", "<br>")


def mc(question, options, answer, explanation, notes, topic, form, diff):
    assert len(options) == 4 and len(set(options)) == 4 and 0 <= answer <= 3
    letters = "ABCD"
    assert set(notes) == {letters[i] for i in range(4) if i != answer}, "mỗi phương án nhiễu cần một ghi chú lỗi"
    return dict(type="multiple_choice", question=question, options=options, answer=answer,
                explanation=br(explanation), distractorNotes=notes, topic=topic, form=form, difficulty=diff)


def tf(question, statements, explanation, notes, topic, form, diff):
    assert len(statements) == 4
    return dict(type="true_false", question=question,
                statements=[dict(text=t, answer=a) for t, a in statements],
                explanation=br(explanation), distractorNotes=notes, topic=topic, form=form, difficulty=diff)


def sa(question, answer, explanation, topic, form, diff):
    assert 0 < len(answer) <= 4
    return dict(type="short_answer", question=question, answer=answer,
                explanation=br(explanation), topic=topic, form=form, difficulty=diff)


Q = []

# ── Câu 1 · Phần I · đối lưu (đáp án C)
Q.append(mc(
    "Đun nước trong nồi bằng bếp đặt dưới đáy. Nước ở phía trên cũng nhanh chóng nóng lên, chủ yếu nhờ cách truyền nhiệt nào?",
    ["Dẫn nhiệt, vì nước dẫn nhiệt tốt như kim loại",
     "Bức xạ nhiệt từ đáy nồi xuyên qua lớp nước",
     "Đối lưu: nước nóng ở đáy nở ra, nhẹ hơn nên đi lên, nước lạnh hơn chìm xuống",
     "Lạnh từ lớp nước trên truyền xuống đáy nồi và bị bếp làm mất đi"],
    2,
    "Chất lỏng dẫn nhiệt kém, nên lớp nước trên không nóng nhanh nhờ dẫn nhiệt.\n"
    "Nước ở đáy nhận nhiệt, nở ra, khối lượng riêng giảm nên nổi lên; nước lạnh hơn ở trên nặng hơn chìm xuống thế chỗ.\n"
    "Dòng tuần hoàn đó là đối lưu, là cách truyền nhiệt chủ yếu trong chất lỏng và chất khí.\n"
    "Đáp án C.",
    {"A": "Chất lỏng (trừ thuỷ ngân) dẫn nhiệt kém; nước không dẫn nhiệt tốt như kim loại.",
     "B": "Bức xạ có xảy ra nhưng rất ít; trong chất lỏng đối lưu mới là chủ yếu.",
     "D": "Không có \"lạnh\" truyền đi; chỉ có nhiệt truyền từ vật nóng hơn sang vật lạnh hơn."},
    YC_NOI_NANG, "ly_thuyet", "de"))

# ── Câu 2 · Phần I · phích (đáp án B)
Q.append(mc(
    "Trong phích (bình thuỷ) giữ nước nóng, lớp chân không giữa hai vỏ thuỷ tinh có tác dụng chính là gì?",
    ["Phản xạ bức xạ nhiệt trở lại nước",
     "Ngăn truyền nhiệt bằng dẫn nhiệt và đối lưu",
     "Ngăn hơi lạnh bên ngoài truyền vào nước",
     "Chỉ ngăn đối lưu, còn dẫn nhiệt vẫn truyền qua được"],
    1,
    "Dẫn nhiệt và đối lưu đều cần hạt vật chất (rắn, lỏng, khí); chân không không có hạt nên chặn cả hai.\n"
    "Bức xạ nhiệt truyền được qua chân không; phích chặn bức xạ bằng mặt tráng bạc sáng bóng.\n"
    "Đáp án B.",
    {"A": "Phản xạ bức xạ là việc của mặt tráng bạc; bức xạ vẫn đi qua chân không được.",
     "C": "Không có \"hơi lạnh\" truyền vào; phích giữ nhiệt của nước không thoát ra ngoài.",
     "D": "Chân không không có hạt vật chất nên chặn cả dẫn nhiệt chứ không riêng đối lưu."},
    YC_NOI_NANG, "ly_thuyet", "de"))

# ── Câu 3 · Phần I · băng kép (đáp án D)
Q.append(mc(
    "Một băng kép gồm lá đồng và lá thép tán chặt vào nhau, thẳng ở nhiệt độ phòng. Biết đồng nở vì nhiệt nhiều hơn thép. Phát biểu nào sau đây đúng?",
    ["Khi hơ nóng, băng kép cong về phía lá đồng",
     "Khi hơ nóng, băng kép vẫn thẳng, chỉ dài ra",
     "Khi làm lạnh, băng kép cong về phía lá thép",
     "Khi hơ nóng, băng kép cong về phía lá thép"],
    3,
    "Khi nóng, lá đồng dài ra nhiều hơn lá thép; hai lá tán chặt nên băng phải cong, lá dài hơn (đồng) nằm ở mặt lồi.\n"
    "Vậy khi hơ nóng băng kép cong về phía lá thép.\n"
    "Khi làm lạnh, lá đồng co nhiều hơn, ngắn hơn, nên băng kép cong về phía lá đồng.\n"
    "Đáp án D.",
    {"A": "Lá nở nhiều (đồng) dài hơn nên nằm ở mặt lồi; băng cong về phía lá nở ít.",
     "B": "Hai lá nở khác nhau nhưng bị tán chặt, nên băng buộc phải cong chứ không thẳng.",
     "C": "Khi lạnh đồng co nhiều hơn nên ngắn hơn; băng cong về phía đồng, ngược với khi nóng."},
    YC_NHIET, "ly_thuyet", "de"))

# ── Câu 4 · Phần I · khe hở ray (đáp án A)
alpha, l0, t_lap, t_max = F(12, 10**6), 15, 25, 55
khe = l0 * alpha * (t_max - t_lap) * 1000          # mm
sai_t = l0 * alpha * t_max * 1000                   # dùng t thay cho Δt
sai_3a = l0 * 3 * alpha * (t_max - t_lap) * 1000    # dùng hệ số nở khối 3α
sai_dv = khe / 10                                   # đổi m → mm sai
assert khe == F(54, 10) and sai_t == F(99, 10) and sai_3a == F(162, 10) and sai_dv == F(54, 100)
assert len({khe, sai_t, sai_3a, sai_dv}) == 4 and all(x != khe for x in (sai_t, sai_3a, sai_dv))
Q.append(mc(
    "Mỗi thanh ray thép dài $15\\ \\text{m}$ được lắp ở $25\\ ^\\circ\\text{C}$. Nhiệt độ ray cao nhất có thể tới $55\\ ^\\circ\\text{C}$. "
    "Hệ số nở dài của thép là $12\\cdot10^{-6}\\ \\text{K}^{-1}$. Khe hở tối thiểu giữa hai đầu ray liền nhau là bao nhiêu?",
    [f"${vnk(khe)}\\ \\text{{mm}}$", f"${vnk(sai_t)}\\ \\text{{mm}}$",
     f"${vnk(sai_3a)}\\ \\text{{mm}}$", f"${vnk(sai_dv, 2)}\\ \\text{{mm}}$"],
    0,
    "Độ dãn của một thanh ray: $\\Delta l = l_0\\alpha\\Delta t$.\n"
    "$\\Delta t = 55 - 25 = 30\\ ^\\circ\\text{C}$.\n"
    f"$\\Delta l = 15\\cdot12\\cdot10^{{-6}}\\cdot30 = 5{{,}}4\\cdot10^{{-3}}\\ \\text{{m}} = {vnk(khe)}\\ \\text{{mm}}$.\n"
    "Khe hở phải ít nhất bằng độ dãn này. Đáp án A.",
    {"B": "Dùng nhiệt độ $55\\ ^\\circ\\text{C}$ thay cho độ tăng nhiệt độ $\\Delta t = 30\\ ^\\circ\\text{C}$.",
     "C": "Dùng hệ số nở khối $3\\alpha$; chiều dài ray chỉ cần hệ số nở dài $\\alpha$.",
     "D": "Đổi đơn vị sai: $5{,}4\\cdot10^{-3}\\ \\text{m}$ là $5{,}4\\ \\text{mm}$, không phải $0{,}54\\ \\text{mm}$."},
    YC_NHIET, "bai_tap", "trung-binh"))

# ── Câu 5 · Phần II · nước 4 °C
Q.append(tf(
    "Xét sự nở vì nhiệt đặc biệt của nước và hiện tượng hồ nước ở xứ lạnh vào mùa đông.",
    [("Khối lượng riêng của nước lớn nhất ở $0\\ ^\\circ\\text{C}$.", False),
     ("Khi nước nóng lên từ $0\\ ^\\circ\\text{C}$ đến $4\\ ^\\circ\\text{C}$ thì thể tích của nó giảm.", True),
     ("Khi mặt hồ sâu đã đóng băng, nước ở đáy hồ có nhiệt độ khoảng $4\\ ^\\circ\\text{C}$.", True),
     ("Hồ đóng băng từ đáy lên, vì nước càng lạnh thì càng nặng và chìm xuống.", False)],
    "a) Sai: từ $0$ đến $4\\ ^\\circ\\text{C}$ nước co lại nên khối lượng riêng lớn nhất ở $4\\ ^\\circ\\text{C}$, không phải $0\\ ^\\circ\\text{C}$.\n"
    "b) Đúng: đây là sự nở bất thường của nước, nóng lên trong khoảng $0$–$4\\ ^\\circ\\text{C}$ mà lại co lại.\n"
    "c) Đúng: nước $4\\ ^\\circ\\text{C}$ nặng nhất chìm xuống đáy; lớp băng trên mặt dẫn nhiệt kém che cho nước bên dưới.\n"
    "d) Sai: nước dưới $4\\ ^\\circ\\text{C}$ nhẹ hơn nên nổi lên trên, hồ đóng băng từ mặt xuống.",
    {"0": "Nước co lại từ 0 °C đến 4 °C nên nặng nhất ở 4 °C, không phải 0 °C.",
     "1": "Trong khoảng 0–4 °C nước nóng lên lại co lại; đây là điểm bất thường của nước.",
     "2": "Nước 4 °C nặng nhất nên chìm xuống đáy, đáy hồ giữ khoảng 4 °C.",
     "3": "Nước lạnh dưới 4 °C nhẹ hơn, nổi lên mặt và đóng băng ở mặt trước."},
    YC_NHIET, "ly_thuyet", "de"))

# ── Câu 6 · Phần II · hao phí tỉ lệ hiệu nhiệt độ (tủ ấp trứng)
P0, t_phong, t_on = 60, 22, 37
k = F(P0, t_on - t_phong)
t_on_lanh = 17 + P0 / k                 # phòng 17 °C, vẫn 60 W
P_can = k * (37 - 17)                    # giữ 37 °C khi phòng 17 °C
assert k == 4 and t_on_lanh == 32 and P_can == 80
Q.append(tf(
    "Một tủ ấp trứng mini được sưởi bằng một bóng đèn sưởi công suất $60\\ \\text{W}$ bật liên tục. Khi phòng ở $22\\ ^\\circ\\text{C}$ thì nhiệt độ trong tủ ổn định ở $37\\ ^\\circ\\text{C}$. "
    "Coi công suất hao phí từ tủ ra phòng tỉ lệ với hiệu nhiệt độ trong tủ – phòng: $P_{hp} = k(t - t_0)$, không khí trong tủ có nhiệt độ đều.",
    [("Hệ số $k = 4\\ \\text{W/}^\\circ\\text{C}$.", True),
     ("Phòng lạnh xuống $17\\ ^\\circ\\text{C}$, vẫn dùng đèn $60\\ \\text{W}$ thì trong tủ vẫn ổn định ở $37\\ ^\\circ\\text{C}$ vì công suất đèn không đổi.", False),
     ("Phòng ở $17\\ ^\\circ\\text{C}$, muốn trong tủ vẫn ổn định ở $37\\ ^\\circ\\text{C}$ thì cần đèn sưởi công suất $80\\ \\text{W}$.", True),
     ("Phòng ở $22\\ ^\\circ\\text{C}$, cứ để đèn $60\\ \\text{W}$ bật lâu hơn nữa thì trong tủ sẽ nóng vượt $37\\ ^\\circ\\text{C}$.", False)],
    "Khi ổn định, công suất cấp bằng công suất hao phí.\n"
    "a) Đúng: $60 = k(37 - 22)$, nên $k = 4\\ \\text{W/}^\\circ\\text{C}$.\n"
    f"b) Sai: $60 = 4(t - 17)$, nên $t = {t_on_lanh}\\ ^\\circ\\text{{C}}$; phòng lạnh hơn thì nhiệt độ ổn định trong tủ thấp hơn.\n"
    f"c) Đúng: $P = 4\\cdot(37 - 17) = {P_can}\\ \\text{{W}}$.\n"
    "d) Sai: ở $37\\ ^\\circ\\text{C}$ nhiệt cấp vào bằng nhiệt mất đi, tủ không nóng thêm dù bật bao lâu.",
    {"0": "Ổn định thì 60 = k(37 − 22), nên k = 4 W/°C.",
     "1": "Nhiệt độ ổn định phụ thuộc cả nhiệt độ phòng: 60 = 4(t − 17) cho t = 32 °C.",
     "2": "Cần bù hao phí ở hiệu nhiệt độ 20 °C: 4 · 20 = 80 W.",
     "3": "Khi đã ổn định, nhiệt cấp bằng nhiệt mất nên tủ không nóng thêm dù bật lâu."},
    YC_NHIET, "bai_tap", "trung-binh"))

# ── Câu 7 · Phần III · thể tích tràn (bình thuỷ tinh chứa rượu)
V0, br_, bb, t7a, t7b = 1000, F(11, 10**4), F(27, 10**6), 10, 40
dt7 = t7b - t7a
tran = V0 * (br_ - bb) * dt7
sai_bo_binh = V0 * br_ * dt7
sai_t = V0 * (br_ - bb) * t7b
assert tran == F(3219, 100) and vn(tran) == "32,2" and sai_bo_binh == 33 and abs(float(sai_t) - 42.92) < 1e-9
assert len({vn(tran), vn(sai_bo_binh), vn(sai_t)}) == 3
Q.append(sa(
    "Một bình thuỷ tinh có dung tích $1$ lít ở $10\\ ^\\circ\\text{C}$, chứa đầy rượu tới miệng ở cùng nhiệt độ đó. "
    "Đặt bình cạnh lò sưởi, cả bình và rượu nóng lên tới $40\\ ^\\circ\\text{C}$. Hệ số nở khối của rượu $1{,}1\\cdot10^{-3}\\ \\text{K}^{-1}$, "
    "hệ số nở khối của thuỷ tinh $27\\cdot10^{-6}\\ \\text{K}^{-1}$. "
    "Thể tích rượu tràn ra là bao nhiêu $\\text{cm}^3$? (Làm tròn đến một chữ số sau dấu phẩy.)",
    vn(tran),
    "Cả rượu và bình đều nở; phần tràn là hiệu hai độ tăng thể tích.\n"
    "$\\Delta t = 40 - 10 = 30\\ ^\\circ\\text{C}$, $V_0 = 1000\\ \\text{cm}^3$.\n"
    "$\\Delta V = V_0(\\beta_r - \\beta_b)\\Delta t = 1000\\cdot(1{,}1\\cdot10^{-3} - 27\\cdot10^{-6})\\cdot30 \\approx 32{,}2\\ \\text{cm}^3$.\n"
    "Sai hay gặp: bỏ qua bình nở ra được $33\\ \\text{cm}^3$; dùng $40\\ ^\\circ\\text{C}$ thay cho $\\Delta t$ ra $42{,}9\\ \\text{cm}^3$.\n"
    "Đáp số: $32{,}2$.",
    YC_NHIET, "bai_tap", "trung-binh"))

# ── Câu 8 · Phần III · dẫn nhiệt qua vách (tỉ lệ)
P1, d1, S1, dT1 = 360, 5, 40, 30
d2, S2, dT2 = 8, 64, 35
P2 = F(P1) * F(S2, S1) * F(dT2, dT1) * F(d1, d2)
assert P2 == 420
Q.append(sa(
    "Kho lạnh thứ nhất có vách bằng tấm panel cách nhiệt dày $5\\ \\text{cm}$, tổng diện tích vách $40\\ \\text{m}^2$; khi trong kho lạnh hơn ngoài trời $30\\ ^\\circ\\text{C}$ "
    "thì nhiệt truyền qua vách vào kho với công suất $360\\ \\text{W}$. Kho thứ hai dùng panel cùng vật liệu nhưng dày $8\\ \\text{cm}$, tổng diện tích vách $64\\ \\text{m}^2$, "
    "trong kho lạnh hơn ngoài trời $35\\ ^\\circ\\text{C}$. Coi nhiệt chỉ truyền vào kho bằng dẫn nhiệt qua vách, với công suất tỉ lệ thuận với diện tích vách và hiệu nhiệt độ, "
    "tỉ lệ nghịch với bề dày vách. Công suất nhiệt truyền vào kho thứ hai là bao nhiêu oát?",
    str(P2),
    "$P \\propto \\dfrac{S\\,\\Delta t}{d}$, nên $\\dfrac{P_2}{P_1} = \\dfrac{S_2}{S_1}\\cdot\\dfrac{\\Delta t_2}{\\Delta t_1}\\cdot\\dfrac{d_1}{d_2}$.\n"
    "$P_2 = 360\\cdot\\dfrac{64}{40}\\cdot\\dfrac{35}{30}\\cdot\\dfrac{5}{8} = 420\\ \\text{W}$.\n"
    "Sai hay gặp: nhân với $\\dfrac{d_2}{d_1}$ (vách dày hơn lại cho nhiệt qua nhiều hơn) ra $1075{,}2\\ \\text{W}$.\n"
    "Đáp số: $420$.",
    YC_NHIET, "bai_tap", "trung-binh"))
assert abs(float(F(P1) * F(S2, S1) * F(dT2, dT1) * F(d2, d1)) - 1075.2) < 1e-9

# kiểm tổng
types = [q["type"] for q in Q]
assert types == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert [q["answer"] for q in Q[:4]] == [2, 1, 3, 0]   # đáp án rải đều C B D A
for q in Q:
    assert q["topic"] in (YC_NHIET, YC_NOI_NANG) and q["explanation"].strip()

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Truyền nhiệt và sự nở vì nhiệt",
        "topic": YC_NHIET,
        "difficulty": "trung-binh",
        "duration_minutes": 20,
        "subject_code": "hsg-vat-ly",
        "questions": Q,
    },
}
OUT.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"đã ghi {OUT} — {len(Q)} câu")
