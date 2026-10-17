# -*- coding: utf-8 -*-
"""CĐ17 Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà (bài 178) — sinh luyen-tap/bundle.json (8 câu tự chấm:
4 Phần I (A–D), 2 Phần II (a)–d) Đúng/Sai), 2 Phần III (đáp số ≤ 4 ký tự)).
Chỉ có khối exam (theory_html rỗng, worked_examples []) để upload-lesson.mts giữ nguyên lý thuyết và bài tập mẫu.
Câu theo dàn ý nguon.md mục "Luyện tập"; số liệu tính ở đây + assert; mỗi phương án nhiễu ứng với một cách sai cụ thể.
topic: 3 YCCĐ con "Trái Đất và bầu trời" đã tạo trên DB (T_PHA, T_MUA, T_HMT).
Chạy: python3 content/hsg9/cd17-thien-van/luyen-tap/sinh.py"""
import json
from pathlib import Path

OUT = Path(__file__).with_name("bundle.json")
T_PHA = "Pha Mặt Trăng, nhật thực và nguyệt thực"          # YCCĐ con đã có trên DB
T_MUA = "Chuyển động nhìn thấy của Mặt Trời, ngày đêm và mùa"
T_HMT = "Hệ Mặt Trời và Ngân Hà"
TOPIC = T_PHA                   # topic chung của đề
AU, C_AS = 1.5e8, 3e5           # km, km/s


def vn(x, nd=1):
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def vnk(x, nd=1):
    return vn(x, nd).replace(",", "{,}")


def ps(*lines):
    """Mỗi ý một dòng (<p> riêng)."""
    return "".join(f"<p>{x}</p>" for x in lines)


def mc(question, options, answer, explanation, notes, topic, form, diff):
    assert len(options) == 4 and len(set(options)) == 4 and 0 <= answer <= 3
    assert set(notes) == {"ABCD"[i] for i in range(4) if i != answer}, "mỗi phương án nhiễu cần một ghi chú lỗi"
    return dict(type="multiple_choice", question=question, options=options, answer=answer,
                explanation=explanation, distractorNotes=notes, topic=topic, form=form, difficulty=diff)


def tf(question, statements, explanation, notes, topic, form, diff):
    assert len(statements) == 4 and set(notes) == {"0", "1", "2", "3"}
    return dict(type="true_false", question=question,
                statements=[dict(text=t, answer=a) for t, a in statements],
                explanation=explanation, distractorNotes=notes, topic=topic, form=form, difficulty=diff)


def sa(question, answer, explanation, topic, form, diff):
    assert 0 < len(answer) <= 4
    return dict(type="short_answer", question=question, answer=answer,
                explanation=explanation, topic=topic, form=form, difficulty=diff)


Q = []

# ── Câu 1 · Phần I · pha có nhật thực (đáp án B)
Q.append(mc(
    "<p>Nhật thực chỉ có thể xảy ra vào ngày Mặt Trăng ở pha nào?</p>",
    ["Trăng tròn.",
     "Không trăng (trăng non).",
     "Bất kì pha nào, miễn là vào ban ngày.",
     "Trăng lưỡi liềm đầu tháng."],
    1,
    ps("Nhật thực xảy ra khi Mặt Trăng nằm giữa Mặt Trời và Trái Đất (thứ tự Mặt Trời – Mặt Trăng – Trái Đất), bóng Mặt Trăng rơi xuống mặt đất.",
       "Lúc đó nửa được chiếu sáng của Mặt Trăng quay hẳn về phía Mặt Trời, nửa tối quay về ta: đó là ngày không trăng. Đáp án B.",
       "A là điều kiện của nguyệt thực (Mặt Trời – Trái Đất – Mặt Trăng).",
       "C, D: Mặt Trăng không thẳng hàng giữa Mặt Trời và Trái Đất nên bóng của nó không rơi xuống Trái Đất."),
    {"A": "Nhầm với nguyệt thực: trăng tròn thì Trái Đất ở giữa, bóng Trái Đất che Mặt Trăng.",
     "C": "Quên điều kiện thẳng hàng Mặt Trời – Mặt Trăng – Trái Đất; ban ngày chưa đủ.",
     "D": "Tưởng phần tối của trăng lưỡi liềm là do bị che; thật ra Mặt Trăng chưa ở đúng giữa Mặt Trời và Trái Đất."},
    T_PHA, "ly_thuyet", "de"))

# ── Câu 2 · Phần I · vì sao không tháng nào cũng có thực (đáp án D)
Q.append(mc(
    "<p>Tháng nào cũng có ngày không trăng và đêm trăng tròn, nhưng mỗi năm chỉ có vài lần nhật thực, nguyệt thực. Nguyên nhân chính là</p>",
    ["Trái Đất tự quay quanh trục nên phần lớn thời gian ta đứng ở phía không nhìn thấy.",
     "quỹ đạo Trái Đất quanh Mặt Trời là elip nên khoảng cách giữa chúng luôn thay đổi.",
     "Mặt Trăng tự quay quanh trục nên có lúc quay mặt che được, có lúc không.",
     "quỹ đạo Mặt Trăng nghiêng khoảng $5^\\circ$ so với mặt phẳng quỹ đạo Trái Đất."],
    3,
    ps("Quỹ đạo Mặt Trăng nghiêng khoảng $5^\\circ$ nên trăng non, trăng tròn thường đi ngang phía trên hoặc phía dưới đường nối Mặt Trời – Trái Đất; bóng trượt qua mà không chạm.",
       "Chỉ khi trăng non/tròn rơi gần giao tuyến của hai mặt phẳng quỹ đạo (hai \"mùa thực\" mỗi năm, cách nhau khoảng $6$ tháng) mới có thực. Đáp án D.",
       "A: Trái Đất tự quay chỉ quyết định nơi nào thấy được, không quyết định có thực hay không.",
       "B: quỹ đạo elip chỉ làm Mặt Trời trông to nhỏ một chút (ảnh hưởng toàn phần hay hình khuyên).",
       "C: Mặt Trăng tự quay không làm thay đổi vị trí của nó so với đường Mặt Trời – Trái Đất."),
    {"A": "Nhầm vai trò của sự tự quay (nơi thấy được) với điều kiện thẳng hàng (có thực hay không).",
     "B": "Elip chỉ đổi khoảng cách, ảnh hưởng loại nhật thực chứ không làm mất thẳng hàng.",
     "C": "Sự tự quay của Mặt Trăng không đổi vị trí tâm của nó trên quỹ đạo."},
    T_PHA, "ly_thuyet", "de"))

# ── Câu 3 · Phần I · góc cao trưa đông chí ở Đà Lạt (đáp án A) — khác D5 (Hà Nội, TP.HCM)
phi, dl = 11.9, -23.5
h_dung = 90 - abs(phi - dl)          # 54,6
s_xp = 90 - phi                       # 78,1: quên δ (dùng ngày xuân phân)
s_goc = abs(phi - dl)                 # 35,4: lấy nhầm |φ−δ| (góc giữa tia nắng và phương thẳng đứng)
s_qphi = 90 - abs(dl)                 # 66,5: quên φ (như đứng ở xích đạo)
assert tuple(round(x, 1) for x in (h_dung, s_xp, s_goc, s_qphi)) == (54.6, 78.1, 35.4, 66.5)
assert len({h_dung, s_xp, s_goc, s_qphi}) == 4
Q.append(mc(
    "<p>Đà Lạt ở vĩ độ $11{,}9^\\circ$B. Ngày đông chí, xích vĩ Mặt Trời là $\\delta=-23{,}5^\\circ$. Góc cao của Mặt Trời lúc giữa trưa ở Đà Lạt ngày đông chí xấp xỉ</p>",
    [f"${vnk(h_dung)}^\\circ$.", f"${vnk(s_xp)}^\\circ$.", f"${vnk(s_goc)}^\\circ$.", f"${vnk(s_qphi)}^\\circ$."],
    0,
    ps("$h=90^\\circ-|\\varphi-\\delta|=90^\\circ-|11{,}9^\\circ-(-23{,}5^\\circ)|=90^\\circ-35{,}4^\\circ=54{,}6^\\circ$. Đáp án A.",
       "Mặt Trời ở phía Nam; bóng cọc ngả về Bắc."),
    {"B": "Quên xích vĩ δ: 90° − 11,9° = 78,1° là góc cao ngày xuân phân/thu phân.",
     "C": "Lấy |φ − δ| = 35,4° (góc giữa tia nắng và phương thẳng đứng) mà quên lấy 90° trừ đi.",
     "D": "Quên vĩ độ Đà Lạt: 90° − 23,5° = 66,5° chỉ đúng ở xích đạo."},
    T_MUA, "bai_tap", "trung-binh"))

# ── Câu 4 · Phần I · Ngân Hà và năm ánh sáng (đáp án C)
Q.append(mc(
    "<p>Phát biểu nào sau đây là đúng?</p>",
    ["Năm ánh sáng là thời gian ánh sáng đi hết một vòng quanh tâm Ngân Hà.",
     "Mặt Trời nằm ở tâm Ngân Hà nên ta thấy Ngân Hà như một dải sáng vắt ngang bầu trời.",
     "Dải sáng mờ Ngân Hà trên bầu trời đêm là đĩa thiên hà của ta nhìn từ bên trong.",
     "Năm ánh sáng là đơn vị đo thời gian, bằng $365{,}25$ ngày."],
    2,
    ps("Ngân Hà là thiên hà dạng đĩa xoắn ốc; Hệ Mặt Trời nằm trong đĩa, ở một nhánh xoắn cách tâm khoảng $26\\,000$ năm ánh sáng.",
       "Nhìn dọc theo mặt đĩa ta thấy rất nhiều sao chồng lên nhau thành một dải sáng mờ. Đáp án C.",
       "A, D sai: năm ánh sáng là đơn vị đo <strong>khoảng cách</strong> — quãng đường ánh sáng đi trong một năm, khoảng $9{,}46\\cdot10^{12}\\ \\text{km}$.",
       "B sai: Mặt Trời không ở tâm Ngân Hà."),
    {"A": "Nhầm năm ánh sáng là một khoảng thời gian (lại gắn với chu kì quay của Ngân Hà).",
     "B": "Tưởng Mặt Trời ở tâm Ngân Hà; thật ra cách tâm khoảng 26 000 năm ánh sáng.",
     "D": "Bẫy kinh điển: chữ \"năm\" khiến tưởng là đơn vị thời gian; năm ánh sáng là quãng đường."},
    T_HMT, "ly_thuyet", "de"))

# ── Câu 5 · Phần II · nhật thực toàn phần / hình khuyên / nửa tối
Q.append(tf(
    "<p>Xét các phát biểu sau về nhật thực.</p>",
    [("Nhật thực toàn phần chỉ quan sát được trong một dải hẹp trên mặt đất, rộng không quá vài trăm kilômét.", True),
     ("Người đứng trong vùng nửa tối của Mặt Trăng thấy nhật thực một phần.", True),
     ("Khi Mặt Trăng ở xa Trái Đất nhất, vùng bóng tối trên mặt đất rộng nhất nên nhật thực toàn phần kéo dài nhất.", False),
     ("Nhật thực hình khuyên xảy ra khi Mặt Trăng ở gần Trái Đất, đĩa Mặt Trăng trông to hơn đĩa Mặt Trời.", False)],
    ps("a) Đúng: chóp nón bóng tối của Mặt Trăng dài xấp xỉ khoảng cách tới mặt đất, nên khi chạm đất vùng tối chỉ rộng cỡ vài trăm km trở xuống.",
       "b) Đúng: trong nửa tối, Mặt Trăng chỉ che một phần đĩa Mặt Trời.",
       "c) Sai: Mặt Trăng ở xa nhất thì góc trông của nó nhỏ hơn Mặt Trời, chóp nón bóng tối không chạm đất — chỉ có nhật thực hình khuyên, không có toàn phần.",
       "d) Sai: hình khuyên xảy ra khi Mặt Trăng ở xa, đĩa Mặt Trăng trông nhỏ hơn đĩa Mặt Trời nên còn hở một vành sáng."),
    {"0": "Vùng tối trên mặt đất nhỏ (cỡ vài trăm km trở xuống) vì nón bóng tối dài xấp xỉ khoảng cách tới mặt đất.",
     "1": "Nửa tối: một phần đĩa Mặt Trời bị che → nhật thực một phần.",
     "2": "Mặt Trăng càng xa, chóp nón bóng tối càng không tới mặt đất → hình khuyên, không có toàn phần.",
     "3": "Đảo ngược: hình khuyên khi Mặt Trăng xa, trông nhỏ hơn Mặt Trời."},
    T_PHA, "ly_thuyet", "trung-binh"))

# ── Câu 6 · Phần II · mùa
phi_cm = 9.2                       # Cà Mau — khác D5 (Hà Nội, TP.HCM)
h6 = 90 - abs(phi_cm - 23.5)
assert 23.5 > phi_cm and round(h6, 1) == 75.7   # hạ chí Cà Mau: Mặt Trời ở phía Bắc → bóng về Nam
Q.append(tf(
    "<p>Xét các phát biểu sau về mùa trên Trái Đất.</p>",
    [("Có mùa là do trục Trái Đất nghiêng khoảng $23{,}5^\\circ$ so với phương vuông góc mặt phẳng quỹ đạo và giữ phương không đổi khi Trái Đất quay quanh Mặt Trời.", True),
     ("Bắc bán cầu có mùa hè vì khi đó Trái Đất ở gần Mặt Trời nhất.", False),
     ("Trưa ngày hạ chí ở Cà Mau (vĩ độ $9{,}2^\\circ$B), bóng của cọc thẳng đứng ngả về phía Nam.", True),
     ("Ở xích đạo, ngày và đêm dài gần bằng nhau quanh năm.", True)],
    ps("a) Đúng: trục nghiêng giữ phương cố định nên góc chiếu của tia nắng và độ dài ngày ở mỗi nơi thay đổi theo vị trí trên quỹ đạo.",
       "b) Sai: Trái Đất gần Mặt Trời nhất vào đầu tháng 1, đúng lúc Bắc bán cầu đang mùa đông; khoảng cách chỉ đổi khoảng $3\\,\\%$.",
       "c) Đúng: ngày hạ chí $\\delta=23{,}5^\\circ\\gt\\varphi=9{,}2^\\circ$, Mặt Trời lúc trưa ở phía Bắc đỉnh đầu (góc cao $90^\\circ-14{,}3^\\circ=75{,}7^\\circ$), bóng ngả về Nam.",
       "d) Đúng: vòng tròn phân chia sáng – tối luôn chia đôi đường xích đạo, nên ở xích đạo ngày luôn xấp xỉ $12$ giờ."),
    {"0": "Mùa do trục nghiêng giữ phương cố định, làm góc chiếu và độ dài ngày đổi theo năm.",
     "1": "Mùa không do gần/xa Mặt Trời: Trái Đất gần Mặt Trời nhất đầu tháng 1 (mùa đông ở Bắc bán cầu).",
     "2": "Khi δ > φ, Mặt Trời trưa ở phía Bắc → bóng về Nam; quen \"bóng luôn về Bắc\" là sai ở vùng nhiệt đới.",
     "3": "Đường phân chia sáng – tối luôn chia đôi xích đạo → ngày ≈ đêm ≈ 12 h quanh năm."},
    T_MUA, "ly_thuyet", "trung-binh"))

# ── Câu 7 · Phần III · thời gian ánh sáng Mặt Trời → Sao Thổ (khác D6 và quiz lý thuyết)
t7 = 9.5 * AU / C_AS / 60
assert 9.5 * AU / C_AS == 4750 and round(t7, 1) == 79.2 and vn(t7) == "79,2"
assert round(9.5 * AU / C_AS / 3600, 1) == 1.3      # bẫy: đổi ra giờ
Q.append(sa(
    "<p>Sao Thổ cách Mặt Trời khoảng $9{,}5\\ \\text{AU}$, với $1\\ \\text{AU}=1{,}5\\cdot10^8\\ \\text{km}$; tốc độ ánh sáng $3\\cdot10^5\\ \\text{km/s}$. Ánh sáng từ Mặt Trời tới Sao Thổ mất bao nhiêu phút? (Làm tròn đến một chữ số thập phân.)</p>",
    vn(t7),
    ps("$s=9{,}5\\cdot1{,}5\\cdot10^8=1{,}425\\cdot10^9\\ \\text{km}$.",
       "$t=\\dfrac{s}{c}=\\dfrac{1{,}425\\cdot10^9}{3\\cdot10^5}=4750\\ \\text{s}$.",
       "$4750\\ \\text{s}=\\dfrac{4750}{60}\\approx79{,}2$ phút.",
       "Bẫy: quên đổi AU ra km, hoặc chia cho $3600$ (ra giờ) thay vì $60$.",
       "Đáp số: $79{,}2$."),
    T_HMT, "bai_tap", "de"))

# ── Câu 8 · Phần III · tháng giao hội từ tháng thiên văn
T, Y = 27.3, 365
S8 = 1 / (1 / T - 1 / Y)
assert round(S8, 1) == 29.5 and vn(S8) == "29,5"
assert round(1 / (1 / T + 1 / Y), 1) == 25.4      # bẫy: cộng thay vì trừ
Q.append(sa(
    "<p>Mặt Trăng quay quanh Trái Đất một vòng so với các ngôi sao xa hết $27{,}3$ ngày; Trái Đất quay quanh Mặt Trời một vòng hết $365$ ngày, cùng chiều. Hai lần trăng tròn liên tiếp (tháng giao hội) cách nhau bao nhiêu ngày? (Làm tròn đến một chữ số thập phân.)</p>",
    vn(S8),
    ps("Trăng tròn lặp lại khi Mặt Trăng \"đuổi kịp\" lại hướng Mặt Trời – Trái Đất, mà hướng này cũng quay cùng chiều theo Trái Đất (giống hai kim đồng hồ đuổi nhau).",
       "Tốc độ góc tương đối: $\\dfrac{1}{S}=\\dfrac{1}{T}-\\dfrac{1}{365}=\\dfrac{1}{27{,}3}-\\dfrac{1}{365}$.",
       "$S\\approx29{,}5$ ngày.",
       "Bẫy: cộng hai nghịch đảo (ra khoảng $25{,}4$ ngày) — tháng giao hội phải <strong>dài hơn</strong> tháng thiên văn vì Mặt Trăng phải đi thêm một đoạn.",
       "Đáp số: $29{,}5$."),
    T_PHA, "bai_tap", "trung-binh"))

# ── kiểm tổng
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert [q["answer"] for q in Q[:4]] == [1, 3, 0, 2]          # đáp án rải đều B D A C
assert [q["topic"] for q in Q] == [T_PHA, T_PHA, T_MUA, T_HMT, T_PHA, T_MUA, T_HMT, T_PHA]
assert Q[7]["difficulty"] == "trung-binh"
for q in Q[:4]:   # đáp án đúng không dài nhất hẳn
    L = [len(o) for o in q["options"]]; assert L[q["answer"]] <= max(L[i] for i in range(4) if i != q["answer"]) * 1.15, L
assert ["".join("Đ" if s["answer"] else "S" for s in q["statements"]) for q in Q[4:6]] == ["ĐĐSS", "ĐSĐĐ"]
for q in Q:
    assert q["explanation"].strip() and q["form"] in ("ly_thuyet", "bai_tap")
    assert q["topic"] in (T_PHA, T_MUA, T_HMT)
    texts = [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]
    for s in texts:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 for ch in s), s
        for seg in s.split("$")[1::2]:
            assert "<" not in seg and ">" not in seg, seg

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà",
        "topic": TOPIC,
        "difficulty": "trung-binh",
        "duration_minutes": 20,
        "subject_code": "hsg-vat-ly",
        "questions": Q,
    },
}
OUT.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ghi", OUT, len(Q), "câu; đáp án:",
      ["ABCD"[q["answer"]] if q["type"] == "multiple_choice" else
       ("".join("Đ" if s["answer"] else "S" for s in q["statements"]) if q["type"] == "true_false" else q["answer"])
       for q in Q])
