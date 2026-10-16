# -*- coding: utf-8 -*-
"""CĐ12 Nhiệt học nâng cao (lesson 153) — sinh luyen-tap/bundle.json (8 câu tự chấm: 4 Phần I, 2 Phần II, 2 Phần III).
Chỉ có khối exam (theory_html rỗng, worked_examples []) để upload-lesson.mts giữ nguyên lý thuyết và bài tập mẫu.
Số liệu tính bằng Python + assert; mỗi phương án nhiễu ứng với một cách sai cụ thể và khác đáp án đúng.
Số liệu khác bài tập mẫu (153.json), khác tự luận (btm153_tl.py) và khác ví dụ docx (nguon.txt).
Chạy: python3 content/hsg9/cd12-nhiet-hoc/luyen-tap/sinh.py"""
import json
from fractions import Fraction as F
from pathlib import Path

CN, CD, CAL, CCU, CFE, LAM, L = 4200, 2100, 880, 380, 460, 340000, 2300000
T_CB = "Nhiệt độ và cân bằng nhiệt"
T_Q = "Tính nhiệt lượng theo nhiệt dung riêng"
T_CT = "Nhiệt nóng chảy riêng và nhiệt hoá hơi riêng"


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

# ── Câu 1 · Phần I · ý nghĩa nhiệt dung riêng (đáp án D)
Q.append(mc(
    "<p>Nhiệt dung riêng của nhôm là $880\\ \\text{J/(kg·K)}$. Con số này cho biết điều gì?</p>",
    ["Một kilôgam nhôm ở $1\\ ^\\circ\\text{C}$ chứa nhiệt lượng $880\\ \\text{J}$.",
     "Muốn $880\\ \\text{kg}$ nhôm tăng thêm $1\\ ^\\circ\\text{C}$ cần cung cấp $1\\ \\text{J}$.",
     "Muốn $1\\ \\text{kg}$ nhôm nóng chảy hoàn toàn ở nhiệt độ nóng chảy cần $880\\ \\text{J}$.",
     "Muốn $1\\ \\text{kg}$ nhôm tăng thêm $1\\ ^\\circ\\text{C}$ (hay $1\\ \\text{K}$) cần cung cấp $880\\ \\text{J}$."],
    3,
    "<p>Nhiệt dung riêng $c$ là nhiệt lượng cần để $1\\ \\text{kg}$ chất tăng thêm $1\\ ^\\circ\\text{C}$: $Q=mc\\Delta t=1\\cdot880\\cdot1=880\\ \\text{J}$. Đáp án D.</p>"
    "<p>A sai: nhiệt lượng là phần năng lượng trao đổi khi nhiệt độ thay đổi, không phải thứ vật \"chứa\" ở một nhiệt độ.</p>"
    "<p>B đảo ngược vai trò của khối lượng và nhiệt lượng.</p>"
    "<p>C là ý nghĩa của nhiệt nóng chảy riêng $\\lambda$, không phải $c$.</p>",
    T_Q, "ly_thuyet", "de",
    {"A": "Nhầm nhiệt lượng (năng lượng trao đổi) với thứ vật chứa ở một nhiệt độ.",
     "B": "Đảo vai trò: 880 J ứng với 1 kg tăng 1 °C, không phải 880 kg.",
     "C": "Đó là ý nghĩa của nhiệt nóng chảy riêng λ, không phải nhiệt dung riêng c."}))

# ── Câu 2 · Phần I · t_cb khác trung bình cộng (đáp án B)
m_cu, t_cu, m_w, t_w = F(5, 10), 90, F(3, 10), 20
Ccu, Cw = m_cu * CCU, m_w * CN
t2 = (Ccu * t_cu + Cw * t_w) / (Ccu + Cw)
s_tbc = F(t_cu + t_w, 2)                                 # trung bình cộng
s_m = (m_cu * t_cu + m_w * t_w) / (m_cu + m_w)           # quên c, chỉ trọng số khối lượng
s_dt = Ccu * t_cu / (Ccu + Cw)                           # coi Δt nước = t (quên nhiệt độ đầu 20 °C)
assert round(float(t2), 1) == 29.2 and round(float(s_m), 1) == 63.8 and round(float(s_dt), 1) == 11.8 and s_tbc == 55
assert len({round(float(x), 1) for x in (t2, s_tbc, s_m, s_dt)}) == 4
Q.append(mc(
    "<p>Thả một miếng đồng $500\\ \\text{g}$ ở $90\\ ^\\circ\\text{C}$ vào $300\\ \\text{g}$ nước ở $20\\ ^\\circ\\text{C}$. Bỏ qua nhiệt dung của bình và trao đổi nhiệt với môi trường. Cho $c_{\\text{đồng}}=380$, $c_{\\text{nước}}=4200\\ \\text{J/(kg·K)}$. Nhiệt độ khi cân bằng xấp xỉ bằng</p>",
    [f"${vn(s_dt)}\\ ^\\circ\\text{{C}}$.", f"${vn(t2)}\\ ^\\circ\\text{{C}}$.",
     f"${vn(s_tbc)}\\ ^\\circ\\text{{C}}$.", f"${vn(s_m)}\\ ^\\circ\\text{{C}}$."],
    1,
    f"<p>Đồng toả: $0{{,}}5\\cdot380\\cdot(90-t)=190\\,(90-t)$. Nước thu: $0{{,}}3\\cdot4200\\cdot(t-20)=1260\\,(t-20)$.</p>"
    f"<p>$190(90-t)=1260(t-20)$ nên $t=\\dfrac{{17\\,100+25\\,200}}{{1450}}\\approx{vn(t2)}\\ ^\\circ\\text{{C}}$. Đáp án B.</p>"
    f"<p>Nhiệt dung của nước ($1260\\ \\text{{J/K}}$) lớn gấp gần $7$ lần của đồng ($190\\ \\text{{J/K}}$) nên nhiệt độ chung gần $20\\ ^\\circ\\text{{C}}$, xa trung bình cộng $55\\ ^\\circ\\text{{C}}$.</p>",
    T_CB, "bai_tap", "de",
    {"A": "Viết phần nước thu là 1260·t, quên trừ nhiệt độ ban đầu 20 °C của nước.",
     "C": "Lấy trung bình cộng hai nhiệt độ — chỉ đúng khi hai vật có cùng nhiệt dung mc.",
     "D": "Chỉ lấy trọng số theo khối lượng, quên nhiệt dung riêng của đồng nhỏ hơn nước nhiều."}))

# ── Câu 3 · Phần I · nhiệt độ khi sôi / nóng chảy (đáp án A)
Q.append(mc(
    "<p>Đun một cục nước đá ở $-10\\ ^\\circ\\text{C}$ bằng bếp cấp nhiệt đều cho tới khi nước sôi được một lúc (áp suất chuẩn). Phát biểu nào sau đây đúng?</p>",
    ["Trong lúc nước sôi, nhiệt độ giữ ở $100\\ ^\\circ\\text{C}$ dù bếp vẫn cấp nhiệt; nhiệt nhận vào dùng để hoá hơi.",
     "Trong lúc đá tan, nhiệt độ tăng dần từ $0\\ ^\\circ\\text{C}$ vì đá vẫn đang nhận nhiệt.",
     "Trong lúc đá tan, nhiệt độ không đổi nên đá không nhận nhiệt của bếp.",
     "Đoạn đun nước lỏng từ $0$ lên $100\\ ^\\circ\\text{C}$ dốc hơn đoạn đun đá từ $-10$ lên $0\\ ^\\circ\\text{C}$ vì nước có nhiệt dung riêng lớn hơn đá."],
    0,
    "<p>Khi chuyển thể (nóng chảy, sôi), nhiệt độ không đổi nhưng chất vẫn nhận nhiệt: $Q=\\lambda m$ khi nóng chảy, $Q=Lm$ khi hoá hơi. Đáp án A.</p>"
    "<p>B và C sai vì trong suốt thời gian đá tan, nhiệt độ giữ $0\\ ^\\circ\\text{C}$ và đá vẫn nhận nhiệt.</p>"
    "<p>D sai: với cùng khối lượng và công suất, nhiệt độ tăng mỗi giây là $\\dfrac{P}{mc}$; $c_{\\text{nước}}=2c_{\\text{đá}}$ nên đoạn nước lỏng <em>thoải</em> hơn.</p>",
    T_CT, "ly_thuyet", "trung-binh",
    {"B": "Lúc nóng chảy, nhiệt độ giữ không đổi ở 0 °C dù vẫn nhận nhiệt.",
     "C": "Nhiệt độ không đổi không có nghĩa là không nhận nhiệt: nhiệt dùng để làm tan đá (λm).",
     "D": "c lớn thì nhiệt độ tăng chậm hơn, nên đoạn nước lỏng thoải hơn chứ không dốc hơn."}))

# ── Câu 4 · Phần I · hiệu suất bếp (đáp án C)
m_w4, m_noi, dt4, H, q = 3, F(8, 10), 85, F(35, 100), 44000000
Qich = (m_w4 * CN + m_noi * CFE) * dt4
mg = Qich / H / q
s_nhanH = Qich * H / q                     # nhân H thay vì chia
s_quennoi = m_w4 * CN * dt4 / H / q        # quên nồi
s_dt100 = (m_w4 * CN + m_noi * CFE) * 100 / H / q   # lấy Δt = 100
assert Qich == 1102280
opts4 = sorted([s_nhanH, s_quennoi, mg, s_dt100])
assert [round(float(x) * 1000, 1) for x in opts4] == [8.8, 69.5, 71.6, 84.2] and opts4.index(mg) == 2
Q.append(mc(
    "<p>Đun $3$ lít nước ở $15\\ ^\\circ\\text{C}$ đựng trong nồi thép $0{,}8\\ \\text{kg}$ tới sôi ($100\\ ^\\circ\\text{C}$) bằng bếp dầu có hiệu suất $35\\,\\%$. Cho $c_{\\text{nước}}=4200$, $c_{\\text{thép}}=460\\ \\text{J/(kg·K)}$, năng suất toả nhiệt của dầu $q=4{,}4\\cdot10^7\\ \\text{J/kg}$. Khối lượng dầu cần đốt xấp xỉ</p>",
    [f"${vn(x * 1000)}\\ \\text{{g}}$." for x in opts4],
    2,
    f"<p>$Q_{{\\text{{ích}}}}=(3\\cdot4200+0{{,}}8\\cdot460)(100-15)=12\\,968\\cdot85=1\\,102\\,280\\ \\text{{J}}$.</p>"
    f"<p>$Q_{{\\text{{tp}}}}=\\dfrac{{Q_{{\\text{{ích}}}}}}{{H}}=\\dfrac{{1\\,102\\,280}}{{0{{,}}35}}\\approx3{{,}}15\\cdot10^6\\ \\text{{J}}$.</p>"
    f"<p>$m=\\dfrac{{Q_{{\\text{{tp}}}}}}{{q}}\\approx0{{,}}0716\\ \\text{{kg}}\\approx{vn(mg * 1000)}\\ \\text{{g}}$. Đáp án C.</p>",
    T_Q, "bai_tap", "trung-binh",
    {"A": "Nhân Q_ích với H thay vì chia: nhiệt toàn phần phải lớn hơn nhiệt có ích.",
     "B": "Quên nhiệt lượng làm nóng nồi thép.",
     "D": "Lấy Δt = 100 °C thay vì 100 − 15 = 85 °C."}))

# ── Câu 5 · Phần II · biện luận đá tan
m_d, t_d, m_n, t_n = F(3, 10), -12, F(8, 10), 15
Qmax = m_n * CN * t_n
Qa = m_d * CD * (0 - t_d)
Qtan = m_d * LAM
mtan = (Qmax - Qa) / LAM
assert Qmax == 50400 and Qa == 7560 and Qtan == 102000 and Qa + Qtan == 109560
assert Qa < Qmax < Qa + Qtan and mtan == F(126, 1000) and m_d - mtan == F(174, 1000)
Q.append(dict(
    type="true_false",
    question="<p>Thả $300\\ \\text{g}$ nước đá ở $-12\\ ^\\circ\\text{C}$ vào bình cách nhiệt chứa $800\\ \\text{g}$ nước ở $15\\ ^\\circ\\text{C}$. Bỏ qua nhiệt dung của bình và trao đổi nhiệt với môi trường. Cho $c_{\\text{nước}}=4200$, $c_{\\text{đá}}=2100\\ \\text{J/(kg·K)}$, $\\lambda=3{,}4\\cdot10^5\\ \\text{J/kg}$.</p>",
    statements=[
        {"text": "Nhiệt lượng tối đa mà nước toả ra khi hạ nhiệt độ về $0\\ ^\\circ\\text{C}$ là $50\\,400\\ \\text{J}$.", "answer": True},
        {"text": "Nhiệt lượng cần để đưa toàn bộ đá lên $0\\ ^\\circ\\text{C}$ và làm tan hết là $102\\,000\\ \\text{J}$.", "answer": False},
        {"text": "Đá tan hết và nhiệt độ cân bằng lớn hơn $0\\ ^\\circ\\text{C}$.", "answer": False},
        {"text": "Khi cân bằng, trong bình còn $174\\ \\text{g}$ nước đá.", "answer": True},
    ],
    explanation=(
        "<p>a) Đúng: $Q_{\\text{toả,max}}=0{,}8\\cdot4200\\cdot15=50\\,400\\ \\text{J}$.</p>"
        "<p>b) Sai: đưa đá lên $0\\ ^\\circ\\text{C}$ cần $0{,}3\\cdot2100\\cdot12=7560\\ \\text{J}$, làm tan hết cần $0{,}3\\cdot3{,}4\\cdot10^5=102\\,000\\ \\text{J}$, tổng $109\\,560\\ \\text{J}$; con số $102\\,000\\ \\text{J}$ mới chỉ là phần làm tan.</p>"
        "<p>c) Sai: $7560\\lt50\\,400\\lt109\\,560$ nên đá lên được $0\\ ^\\circ\\text{C}$ nhưng chỉ tan một phần; hệ cân bằng ở đúng $0\\ ^\\circ\\text{C}$.</p>"
        "<p>d) Đúng: khối lượng đá tan $\\dfrac{50\\,400-7560}{3{,}4\\cdot10^5}=0{,}126\\ \\text{kg}=126\\ \\text{g}$, còn $300-126=174\\ \\text{g}$.</p>"),
    topic=T_CT, form="bai_tap", difficulty="trung-binh",
    distractorNotes={
        "0": "Q_toả,max = m·c·(15 − 0) = 0,8·4200·15 = 50 400 J.",
        "1": "Quên phần nhiệt đưa đá từ −12 °C lên 0 °C (7560 J); chỉ tính phần làm tan.",
        "2": "Phải so Q_toả,max với nhiệt cần để tan hết trước; 50 400 J < 109 560 J nên đá không tan hết.",
        "3": "Đá tan (50 400 − 7560)/340 000 = 126 g, còn lại 174 g.",
    }))

# ── Câu 6 · Phần II · đồ thị T–t
mX, P6 = F(4, 10), 100
c_ran = P6 * 240 / (mX * (70 - 30))
lam_X = P6 * 360 / mX
c_long = P6 * 120 / (mX * (110 - 70))
assert c_ran == 1500 and lam_X == 90000 and c_long == 750 and c_long < c_ran
Q.append(dict(
    type="true_false",
    question="<p>Đun $0{,}4\\ \\text{kg}$ chất rắn X bằng nguồn cấp nhiệt có ích đều $100\\ \\text{W}$. Đồ thị nhiệt độ theo thời gian gồm ba đoạn thẳng nối lần lượt các điểm $(0\\ \\text{min};\\ 30\\ ^\\circ\\text{C})$, $(4\\ \\text{min};\\ 70\\ ^\\circ\\text{C})$, $(10\\ \\text{min};\\ 70\\ ^\\circ\\text{C})$, $(12\\ \\text{min};\\ 110\\ ^\\circ\\text{C})$. Bỏ qua mọi hao phí.</p>",
    statements=[
        {"text": "Nhiệt độ nóng chảy của X là $70\\ ^\\circ\\text{C}$.", "answer": True},
        {"text": "Từ phút $4$ đến phút $10$, X không nhận nhiệt nên nhiệt độ không đổi.", "answer": False},
        {"text": "Nhiệt nóng chảy riêng của X là $9\\cdot10^4\\ \\text{J/kg}$.", "answer": True},
        {"text": "Nhiệt dung riêng của X ở thể lỏng lớn hơn ở thể rắn.", "answer": False},
    ],
    explanation=(
        "<p>a) Đúng: đoạn nằm ngang ở $70\\ ^\\circ\\text{C}$ là lúc X nóng chảy.</p>"
        "<p>b) Sai: nguồn vẫn cấp nhiệt đều; nhiệt nhận vào dùng để nóng chảy nên nhiệt độ không đổi.</p>"
        "<p>c) Đúng: $P\\,\\Delta\\tau=\\lambda m$ nên $\\lambda=\\dfrac{100\\cdot360}{0{,}4}=9\\cdot10^4\\ \\text{J/kg}$.</p>"
        "<p>d) Sai: thể rắn $c_r=\\dfrac{100\\cdot240}{0{,}4\\cdot40}=1500$; thể lỏng $c_l=\\dfrac{100\\cdot120}{0{,}4\\cdot40}=750\\ \\text{J/(kg·K)}$. Đoạn lỏng dốc hơn (tăng $40\\ ^\\circ\\text{C}$ trong $2$ phút so với $4$ phút) nên $c$ nhỏ hơn.</p>"),
    topic=T_CT, form="bai_tap", difficulty="kho",
    distractorNotes={
        "0": "Đoạn nằm ngang trên đồ thị đun là lúc chuyển thể; ở đây là nóng chảy tại 70 °C.",
        "1": "Nguồn vẫn cấp nhiệt đều; nhiệt dùng để nóng chảy nên nhiệt độ không đổi.",
        "2": "λ = PΔτ/m = 100·360/0,4 = 90 000 J/kg; nhớ đổi phút ra giây.",
        "3": "Đoạn dốc hơn thì c nhỏ hơn: c_lỏng = 750 < c_rắn = 1500 J/(kg·K).",
    }))

# ── Câu 7 · Phần III · rót qua lại
m1, t1, m2, t2b, t2p = 3, 50, 1, 10, 25
mr = F(m2 * (t2p - t2b), t1 - t2p)
t1p = ((m1 - mr) * t1 + mr * t2p) / m1
assert mr == F(3, 5) and t1p == 45 and m1 * t1p + m2 * t2p == m1 * t1 + m2 * t2b
Q.append(dict(
    type="short_answer",
    question="<p>Bình 1 chứa $3\\ \\text{kg}$ nước ở $50\\ ^\\circ\\text{C}$, bình 2 chứa $1\\ \\text{kg}$ nước ở $10\\ ^\\circ\\text{C}$. Rót một lượng nước $m$ từ bình 1 sang bình 2; khi bình 2 cân bằng thì nhiệt độ của nó là $25\\ ^\\circ\\text{C}$. Sau đó rót đúng lượng $m$ từ bình 2 về bình 1. Bỏ qua nhiệt dung của bình và trao đổi nhiệt với môi trường. Nhiệt độ của bình 1 khi cân bằng là bao nhiêu $^\\circ\\text{C}$?</p>",
    answer=vn(t1p).replace("{,}", ","),
    explanation=(
        "<p>Lần 1 (bình 2): $m(50-25)=1\\cdot(25-10)$ nên $m=0{,}6\\ \\text{kg}$.</p>"
        "<p>Lần 2 (bình 1 còn $2{,}4\\ \\text{kg}$ ở $50\\ ^\\circ\\text{C}$): $2{,}4(50-t)=0{,}6(t-25)$ nên $4(50-t)=t-25$, $t=45\\ ^\\circ\\text{C}$.</p>"
        "<p>Kiểm tra bằng bảo toàn: $3\\cdot45+1\\cdot25=160=3\\cdot50+1\\cdot10$ ✓.</p>"
        "<p>Bẫy: dùng $3\\ \\text{kg}$ thay vì $2{,}4\\ \\text{kg}$ cho bình 1 ở lần rót về.</p>"),
    topic=T_CB, form="bai_tap", difficulty="kho"))

# ── Câu 8 · Phần III · hơi nước ngưng tụ
mw8, t0, tc = 1, 20, 50
mh = F(mw8 * CN * (tc - t0), L + CN * (100 - tc))
s_quen = F(mw8 * CN * (tc - t0), L)
assert round(float(mh) * 1000) == 50 and round(float(s_quen) * 1000, 1) == 54.8
Q.append(dict(
    type="short_answer",
    question="<p>Cần dẫn bao nhiêu gam hơi nước ở $100\\ ^\\circ\\text{C}$ (áp suất chuẩn) vào bình cách nhiệt chứa $1\\ \\text{kg}$ nước ở $20\\ ^\\circ\\text{C}$ để nước trong bình đạt $50\\ ^\\circ\\text{C}$? Hơi ngưng tụ hết trong bình; bỏ qua nhiệt dung của bình và trao đổi nhiệt với môi trường. Cho $c_{\\text{nước}}=4200\\ \\text{J/(kg·K)}$, $L=2{,}3\\cdot10^6\\ \\text{J/kg}$. Làm tròn đến gam.</p>",
    answer=str(round(float(mh) * 1000)),
    explanation=(
        "<p>Nước thu: $1\\cdot4200\\cdot(50-20)=126\\,000\\ \\text{J}$.</p>"
        "<p>Hơi toả khi ngưng tụ rồi nguội từ $100$ xuống $50\\ ^\\circ\\text{C}$: $m(2{,}3\\cdot10^6+4200\\cdot50)=2\\,510\\,000\\,m$.</p>"
        "<p>$m=\\dfrac{126\\,000}{2\\,510\\,000}\\approx0{,}0502\\ \\text{kg}\\approx50\\ \\text{g}$.</p>"
        "<p>Bẫy: chỉ viết $mL$ (quên phần nước ngưng tụ nguội tiếp) sẽ ra $\\approx54{,}8\\ \\text{g}$.</p>"),
    topic=T_CT, form="bai_tap", difficulty="trung-binh"))

# Kiểm chung
assert [q["type"] for q in Q] == ["multiple_choice"] * 4 + ["true_false"] * 2 + ["short_answer"] * 2
assert sorted(q["answer"] for q in Q[:4]) == [0, 1, 2, 3]
for q in Q[6:]:
    assert len(q["answer"]) <= 4
for q in Q:
    blob = json.dumps(q, ensure_ascii=False)
    assert q["topic"] in (T_CB, T_Q, T_CT)
    for s in [q["question"], q["explanation"]] + q.get("options", []) + [s["text"] for s in q.get("statements", [])]:
        assert s.count("$") % 2 == 0, s
        assert not any(ord(ch) < 32 and ch not in "\n" for ch in s), s

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": "",
    "worked_examples": [],
    "exam": {
        "title": "Luyện tập — Nhiệt học nâng cao: cân bằng nhiệt và chuyển thể",
        "topic": T_CB,
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
