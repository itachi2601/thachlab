"""Bài tập mẫu Bài 7 "Phương trình trạng thái của khí lí tưởng" (Vật lí 12) — lesson_id 8. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/8.quet-dang.json). Hình: hinh_8.py. Bài chưa có mục bai_tap_mau trong DB nên không có ví dụ cũ / tự luận.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-8.py   (idempotent, ghi 8.json với review.checked=false)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_8 import *

J = os.path.join(HERE, "8.json")
T209 = "Vận dụng phương trình trạng thái"
T210 = "Phương trình Clapeyron – Mendeleev"

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Quá trình đẳng tích: nung nóng bình kín",
      topic=T209,
      problem_html=r"""<p>Một bình thép kín chứa khí nén ở $27\ ^\circ\text{C}$, áp suất $2{,}4.10^5\ \text{Pa}$. Bình được đặt gần lò nung nên khí trong bình nóng lên tới $117\ ^\circ\text{C}$. Thể tích bình coi như không đổi.</p><ol type="a"><li>Tính áp suất khí trong bình lúc đó.</li><li>Bình có van an toàn tự mở khi áp suất đạt $3{,}6.10^5\ \text{Pa}$. Khí nóng tới bao nhiêu độ C thì van mở?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Phương trình trạng thái khi cả p, V, T cùng đổi",
      topic=T209,
      problem_html=r"""<p>Trong xi lanh của một động cơ đốt trong có $2{,}4\ \text{dm}^3$ hỗn hợp khí ở áp suất $1{,}0\ \text{atm}$ và nhiệt độ $27\ ^\circ\text{C}$. Pit-tông nén hỗn hợp xuống còn $0{,}20\ \text{dm}^3$ thì áp suất tăng lên $18\ \text{atm}$. Coi lượng khí không đổi.</p><ol type="a"><li>Tính nhiệt độ của khí cuối quá trình nén, theo kelvin và theo độ C.</li><li>Nếu nén thật chậm để nhiệt độ vẫn là $27\ ^\circ\text{C}$ thì áp suất cuối là bao nhiêu atm? So sánh với $18\ \text{atm}$.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị p–T của hai đường đẳng tích",
      topic=T209,
      problem_html=r"""<p>Một lượng khí xác định được nung nóng trong bình kín có thể tích $V_1=4{,}0$ lít. Quá trình này được biểu diễn trên đồ thị $p$–$T$ bởi đoạn MN thuộc đường thẳng (1) kéo dài đi qua gốc toạ độ O. Tại M: $T_M=300\ \text{K}$, $p_M=3{,}0.10^5\ \text{Pa}$; tại N: $T_N=500\ \text{K}$.</p><p>Cũng lượng khí đó, khi đặt trong một bình kín khác, được biểu diễn bởi đường thẳng (2) đi qua gốc toạ độ O và qua điểm Q có $T_Q=300\ \text{K}$, $p_Q=1{,}5.10^5\ \text{Pa}$.</p><ol type="a"><li>Tính áp suất tại N.</li><li>Tính thể tích bình ứng với đường (2).</li><li>Đường (1) hay đường (2) ứng với thể tích lớn hơn?</li></ol>"""),
 dict(label="Dạng 4 · Khá · Phương trình Clapeyron – Mendeleev: số mol, khối lượng, thể tích",
      topic=T210,
      problem_html=r"""<p>Một bình thép dung tích $12$ lít chứa khí nitrogen ($M=28\ \text{g/mol}$) ở $27\ ^\circ\text{C}$, áp suất $2{,}0.10^6\ \text{Pa}$. Lấy $R=8{,}31\ \text{J/(mol·K)}$.</p><ol type="a"><li>Tính số mol khí trong bình.</li><li>Tính khối lượng khí nitrogen trong bình.</li><li>Nếu đưa lượng khí này về điều kiện tiêu chuẩn ($0\ ^\circ\text{C}$, $1\ \text{atm}$) thì nó chiếm bao nhiêu lít?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Lượng khí thay đổi: tính khối lượng khí đã dùng",
      topic=T210,
      problem_html=r"""<p>Một bình thép dung tích $8{,}0$ lít chứa khí oxygen ($M=32\ \text{g/mol}$). Lúc mới nạp, bình ở $27\ ^\circ\text{C}$ và áp suất khí trong bình là $4{,}5.10^6\ \text{Pa}$. Sau một thời gian dùng để hàn, van được đóng lại; bình để trong kho ở $17\ ^\circ\text{C}$, áp suất khí còn lại là $1{,}5.10^6\ \text{Pa}$. Lấy $R=8{,}31\ \text{J/(mol·K)}$, coi oxygen là khí lí tưởng.</p><ol type="a"><li>Tính khối lượng oxygen trong bình lúc mới nạp và lúc còn lại.</li><li>Tính khối lượng oxygen đã dùng.</li></ol>"""),
]

BUILD = [d1, d2, d3, d4, d5]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [("\"bình thép kín … khí nén ở 27 °C, áp suất $2{,}4.10^5$ Pa\"", "$t_1=27\\ ^\\circ\\text{C}$; $p_1=2{,}4.10^5\\ \\text{Pa}$", "Trạng thái 1; $T=t+273$ nên đổi ra Kelvin"),
  ("\"Thể tích bình coi như không đổi\"", "$V$ không đổi; khí kín", "⚠ Đẳng tích: $\\dfrac{p_1}{T_1}=\\dfrac{p_2}{T_2}$ — chỉ dùng khi lượng khí và $V$ không đổi"),
  ("\"nóng lên tới 117 °C\"", "$t_2=117\\ ^\\circ\\text{C}$", "Trạng thái 2; đổi ra Kelvin trước khi lấy tỉ số"),
  ("\"Tính áp suất khí lúc đó\"", "Cần $p_2$", "$p_2=p_1\\dfrac{T_2}{T_1}$"),
  ("\"van an toàn tự mở khi áp suất đạt $3{,}6.10^5$ Pa\"", "$p_3=3{,}6.10^5\\ \\text{Pa}$", "Vẫn đẳng tích: so với trạng thái 1"),
  ("\"nóng tới bao nhiêu độ C thì van mở\"", "Cần $t_3$", "$T_3=T_1\\dfrac{p_3}{p_1}$, rồi $t=T-273$")],
 [("\"$2{,}4\\ \\text{dm}^3$ hỗn hợp khí ở $1{,}0$ atm và $27\\ ^\\circ\\text{C}$\"", "$V_1=2{,}4\\ \\text{dm}^3$; $p_1=1{,}0$ atm; $t_1=27\\ ^\\circ\\text{C}$", "Trạng thái 1; $T_1=t_1+273$"),
  ("\"nén … còn $0{,}20\\ \\text{dm}^3$ thì áp suất tăng lên $18$ atm\"", "$V_2=0{,}20\\ \\text{dm}^3$; $p_2=18$ atm", "Trạng thái 2: $p$, $V$ cùng đổi"),
  ("\"Coi lượng khí không đổi\"", "Lượng khí không đổi", "⚠ Điều kiện dùng $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$; $p$, $V$ cùng đơn vị ở hai vế, $T$ phải là Kelvin"),
  ("\"Tính nhiệt độ của khí cuối quá trình nén\"", "Cần $T_2$ (K và °C)", "$T_2=T_1\\dfrac{p_2V_2}{p_1V_1}$"),
  ("\"nén thật chậm để nhiệt độ vẫn là $27\\ ^\\circ\\text{C}$\"", "$T$ không đổi", "⚠ Nhiệt độ không đổi nên dùng định luật Boyle: $p_1V_1=p'_2V_2$"),
  ("\"áp suất cuối là bao nhiêu atm?\"", "Cần $p'_2$", "$p'_2=p_1\\dfrac{V_1}{V_2}$")],
 [("\"nung nóng trong bình kín $V_1=4{,}0$ lít … đoạn MN thuộc đường thẳng (1) kéo dài qua gốc toạ độ\"", "$V_1=4{,}0$ lít; đường (1) qua O", "Đường thẳng qua gốc trên đồ thị $p$–$T$: $\\dfrac{p}{T}$ không đổi"),
  ("\"Tại M: $300$ K, $3{,}0.10^5$ Pa; tại N: $T_N=500$ K\"", "$T_M$, $p_M$, $T_N$", "M, N cùng nằm trên đường (1)"),
  ("\"Cũng lượng khí đó, bình kín khác … đường (2) qua gốc O và qua Q\"", "$T_Q=300$ K; $p_Q=1{,}5.10^5$ Pa", "⚠ $\\dfrac{p}{T}$ chỉ bằng nhau khi cùng một đường; M và Q thuộc hai đường (hai thể tích khác nhau)"),
  ("\"a) Tính áp suất tại N\"", "Cần $p_N$", "$p_N=p_M\\dfrac{T_N}{T_M}$"),
  ("\"b) Tính thể tích bình ứng với đường (2)\"", "Cần $V_2$", "M, Q cùng $T$: từ $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$ ra hệ thức giữa $p$ và $V$"),
  ("\"c) Đường nào ứng với thể tích lớn hơn?\"", "So sánh $V_1$ và $V_2$", "Kẻ đường thẳng đứng tại một $T$, so hai giá trị $p$")],
 [("\"bình thép dung tích $12$ lít … khí nitrogen ($M=28$ g/mol)\"", "$V=12$ lít; $M=28$ g/mol", "Lượng khí xác định: $n=\\dfrac{m}{M}$"),
  ("\"ở $27\\ ^\\circ\\text{C}$, áp suất $2{,}0.10^6$ Pa\"", "$t=27\\ ^\\circ\\text{C}$; $p=2{,}0.10^6$ Pa", "Một trạng thái nên dùng $pV=nRT$; $T=t+273$"),
  ("\"Lấy $R=8{,}31$ J/(mol·K)\"", "$R=8{,}31$", "⚠ $R$ này đòi $p$ theo Pa, $V$ theo m³, $T$ theo K"),
  ("\"a) Tính số mol khí\"", "Cần $n$", "$n=\\dfrac{pV}{RT}$"),
  ("\"b) khối lượng khí nitrogen\"", "Cần $m$", "$m=nM$"),
  ("\"c) điều kiện tiêu chuẩn ($0\\ ^\\circ\\text{C}$, $1$ atm) chiếm bao nhiêu lít?\"", "Cần $V_0$", "1 mol ở điều kiện tiêu chuẩn chiếm 22,4 lít")],
 [("\"bình thép dung tích $8{,}0$ lít … khí oxygen ($M=32$ g/mol)\"", "$V=8{,}0$ lít; $M=32$ g/mol", "$n=\\dfrac{m}{M}$; đổi $V$ ra m³"),
  ("\"Lúc mới nạp, $27\\ ^\\circ\\text{C}$, $4{,}5.10^6$ Pa\"", "$t_1=27\\ ^\\circ\\text{C}$; $p_1=4{,}5.10^6$ Pa", "Trạng thái 1: $p_1V=n_1RT_1$"),
  ("\"Sau một thời gian dùng để hàn … khí còn lại\"", "Lượng khí đã giảm", "⚠ Lượng khí đã đổi: không dùng $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$; tính $n$ riêng cho từng trạng thái"),
  ("\"bình để trong kho ở $17\\ ^\\circ\\text{C}$, áp suất còn lại $1{,}5.10^6$ Pa\"", "$t_2=17\\ ^\\circ\\text{C}$; $p_2=1{,}5.10^6$ Pa", "Trạng thái 2: $p_2V=n_2RT_2$"),
  ("\"a) khối lượng oxygen lúc mới nạp và lúc còn lại\"", "Cần $m_1$, $m_2$", "$m=nM=\\dfrac{pVM}{RT}$"),
  ("\"b) khối lượng oxygen đã dùng\"", "Cần $\\Delta m$", "$\\Delta m=m_1-m_2$")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = ["<strong>Khái niệm:</strong> trạng thái một lượng khí xác định có ba thông số $p$, $V$, $T$; $T(\\text{K})=t(^\\circ\\text{C})+273$.",
       "<strong>Định luật:</strong> đẳng tích ($V$ không đổi) thì $p$ tỉ lệ thuận với $T$ (Kelvin).",
       "<strong>Công thức:</strong> $\\dfrac{p_1}{T_1}=\\dfrac{p_2}{T_2}$.",
       "⚠ <strong>Điều kiện:</strong> bình kín, lượng khí và thể tích không đổi; $T$ phải đổi ra Kelvin."]
RC2 = ["<strong>Khái niệm:</strong> ba thông số $p$, $V$, $T$ (Kelvin) của một lượng khí xác định.",
       "<strong>Định luật:</strong> phương trình trạng thái; giữ $T$ không đổi thì ra Boyle.",
       "<strong>Công thức:</strong> $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$ · Boyle: $p_1V_1=p_2V_2$",
       "⚠ <strong>Điều kiện:</strong> lượng khí không đổi; $p$, $V$ cùng đơn vị ở hai vế, $T$ Kelvin."]
RC3 = ["<strong>Khái niệm:</strong> trên đồ thị $p$–$T$, đường đẳng tích là đường thẳng kéo dài qua gốc toạ độ.",
       "<strong>Định luật:</strong> trên một đường đẳng tích, $\\dfrac{p}{T}$ không đổi.",
       "<strong>Công thức:</strong> cùng một đường: $\\dfrac{p_1}{T_1}=\\dfrac{p_2}{T_2}$ · hai đường cùng $T$: $p_1V_1=p_2V_2$",
       "⚠ <strong>Điều kiện:</strong> $\\dfrac{p}{T}$ chỉ bằng nhau khi hai điểm cùng một đường; khác đường là khác thể tích."]
RC4 = ["<strong>Khái niệm:</strong> $n=\\dfrac{m}{M}$; điều kiện tiêu chuẩn ($0\\ ^\\circ\\text{C}$, 1 atm): 1 mol chiếm 22,4 lít.",
       "<strong>Định luật:</strong> phương trình Clapeyron – Mendeleev cho một trạng thái của khí.",
       "<strong>Công thức:</strong> $pV=nRT$, $R=8{,}31\\ \\text{J/(mol·K)}$.",
       "⚠ <strong>Điều kiện:</strong> $R$ này đòi $p$ theo Pa, $V$ theo m³, $T$ theo K."]
RC5 = ["<strong>Khái niệm:</strong> hằng số $\\dfrac{pV}{T}=nR$ gắn với lượng khí (số mol $n$).",
       "<strong>Định luật:</strong> $pV=nRT$ viết được cho từng trạng thái, kể cả khi lượng khí đổi.",
       "<strong>Công thức:</strong> $n=\\dfrac{pV}{RT}$ · $m=nM$",
       "⚠ <strong>Điều kiện:</strong> lượng khí đã đổi (xả bớt, bơm thêm) thì không dùng $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$."]

SOLS = [
 sol(RC1, [
  ("Đổi nhiệt độ sang Kelvin", [M(r"T_1=27+273=300\ \text{K}"), M(r"T_2=117+273=390\ \text{K}"), A(r"T_2=390\ \text{K}")]),
  ("Áp suất khi nóng lên (câu a)", [P("Thể tích và lượng khí không đổi:"), M(r"\dfrac{p_1}{T_1}=\dfrac{p_2}{T_2}"),
        M(r"p_2=p_1\dfrac{T_2}{T_1}=2{,}4.10^5\cdot\dfrac{390}{300}"), A(r"p_2=3{,}12.10^5\ \text{Pa}")]),
  ("Nhiệt độ để van mở (câu b)", [P("Van mở khi $p_3=3{,}6.10^5$ Pa, vẫn đẳng tích:"), M(r"T_3=T_1\dfrac{p_3}{p_1}=300\cdot\dfrac{3{,}6.10^5}{2{,}4.10^5}"), A(r"T_3=450\ \text{K}")]),
  ("Đổi về độ C", [M(r"t_3=T_3-273=450-273"), A(r"t_3=177\ ^\circ\text{C}")]),
  ("Kiểm tra", [P("$p_2=3{,}12.10^5\\ \\text{Pa}\\lt3{,}6.10^5\\ \\text{Pa}$ nên ở $117\\ ^\\circ\\text{C}$ van chưa mở; hợp lí vì $117\\ ^\\circ\\text{C}\\lt177\\ ^\\circ\\text{C}$."),
        P("Nếu lấy tỉ số Celsius $117/27\\approx4{,}3$ thì ra $p_2\\approx10{,}4.10^5\\ \\text{Pa}$, vô lí so với mức tăng thật.")])],
  ["a) $p_2=3{,}12.10^5\\ \\text{Pa}$", "b) $t_3=177\\ ^\\circ\\text{C}$"],
  "Nhận dạng: đề nói <strong>bình kín, thể tích không đổi</strong> và nhiệt độ thay đổi → dùng $\\dfrac{p_1}{T_1}=\\dfrac{p_2}{T_2}$, đổi sang Kelvin trước."),
 sol(RC2, [
  ("Đổi nhiệt độ ban đầu sang Kelvin", [M(r"T_1=27+273"), A(r"T_1=300\ \text{K}"), P("$p$ và $V$ chỉ lấy tỉ số nên giữ nguyên atm và dm³, không cần đổi.")]),
  ("Nhiệt độ cuối quá trình nén (câu a)", [P("Cả $p$, $V$, $T$ cùng đổi, lượng khí không đổi:"), M(r"\dfrac{p_1V_1}{T_1}=\dfrac{p_2V_2}{T_2}"),
        M(r"T_2=T_1\cdot\dfrac{p_2V_2}{p_1V_1}=300\cdot\dfrac{18\cdot0{,}20}{1{,}0\cdot2{,}4}=300\cdot1{,}5"), A(r"T_2=450\ \text{K}")]),
  ("Đổi sang độ C", [M(r"t_2=T_2-273=450-273"), A(r"t_2=177\ ^\circ\text{C}")]),
  ("Nén thật chậm (câu b)", [P("Nhiệt độ giữ $27\\ ^\\circ\\text{C}$ nên dùng định luật Boyle:"), M(r"p_1V_1=p'_2V_2"),
        M(r"p'_2=p_1\dfrac{V_1}{V_2}=1{,}0\cdot\dfrac{2{,}4}{0{,}20}"), A(r"p'_2=12\ \text{atm}"),
        P("Nhỏ hơn $18$ atm: nén nhanh làm khí nóng lên nên áp suất cao hơn.")]),
  ("Kiểm tra", [M(r"\dfrac{p_1V_1}{T_1}=\dfrac{1{,}0\cdot2{,}4}{300}=0{,}008"), M(r"\dfrac{p_2V_2}{T_2}=\dfrac{18\cdot0{,}20}{450}=0{,}008"), P("Hai vế bằng nhau, đúng một lượng khí.")])],
  ["a) $T_2=450\\ \\text{K}$, tức $t_2=177\\ ^\\circ\\text{C}$", "b) $p'_2=12\\ \\text{atm}$, nhỏ hơn $18\\ \\text{atm}$"],
  "Nhận dạng: đề cho <strong>cả áp suất, thể tích, nhiệt độ cùng đổi</strong> với lượng khí không đổi → dùng $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$."),
 sol(RC3, [
  ("Nhận ra quá trình MN", [P("Đường thẳng đi qua gốc toạ độ trên đồ thị $p$–$T$: $p$ tỉ lệ thuận với $T$, thể tích bình không đổi."), A("T:MN là quá trình <strong>đẳng tích</strong>.")]),
  ("Áp suất tại N (câu a)", [M(r"\dfrac{p_M}{T_M}=\dfrac{p_N}{T_N}"), M(r"p_N=p_M\dfrac{T_N}{T_M}=3{,}0.10^5\cdot\dfrac{500}{300}"), A(r"p_N=5{,}0.10^5\ \text{Pa}")]),
  ("Thể tích ứng với đường (2) (câu b)", [P("M và Q cùng nhiệt độ $300$ K, cùng lượng khí. Từ phương trình trạng thái với $T_M=T_Q$:"), M(r"p_MV_1=p_QV_2"),
        M(r"V_2=V_1\dfrac{p_M}{p_Q}=4{,}0\cdot\dfrac{3{,}0.10^5}{1{,}5.10^5}"), A(r"V_2=8{,}0\ \text{lít}")]),
  ("So sánh hai đường (câu c)", [P("Tại $T=300$ K: $p_Q\\lt p_M$ nên đường (2) nằm <strong>dưới</strong> đường (1)."),
        A("T:Đường nằm dưới ứng với thể tích <strong>lớn hơn</strong>: $V_2=8{,}0\\ \\text{lít}\\gt V_1=4{,}0\\ \\text{lít}$.")]),
  ("Kiểm tra", [P("$p_MV_1=3{,}0.10^5\\cdot4{,}0$ và $p_QV_2=1{,}5.10^5\\cdot8{,}0$ đều bằng $12.10^5$ (Pa·lít), đúng cùng nhiệt độ và cùng lượng khí."),
        P("Hằng số $\\dfrac{p}{T}$: đường (1) là $1000$ Pa/K, đường (2) là $500$ Pa/K; tỉ lệ nghịch với thể tích ($\\dfrac{p}{T}=\\dfrac{nR}{V}$).")])],
  ["a) $p_N=5{,}0.10^5\\ \\text{Pa}$", "b) $V_2=8{,}0\\ \\text{lít}$", "c) Đường (2) (nằm dưới) ứng với thể tích lớn hơn"],
  "Nhận dạng: đề cho <strong>đường thẳng qua gốc trên đồ thị $p$–$T$</strong> → đẳng tích; so hai đường thì kẻ đường thẳng đứng tại cùng $T$."),
 sol(RC4, [
  ("Đổi đơn vị sang SI", [M(r"V=12\ \text{lít}=12.10^{-3}\ \text{m}^3=0{,}012\ \text{m}^3"), M(r"T=27+273=300\ \text{K}"), P("$p=2{,}0.10^6$ Pa đã đúng đơn vị."), A(r"V=0{,}012\ \text{m}^3")]),
  ("Số mol khí (câu a)", [M(r"pV=nRT\Rightarrow n=\dfrac{pV}{RT}"), M(r"n=\dfrac{2{,}0.10^6\cdot0{,}012}{8{,}31\cdot300}=\dfrac{24000}{2493}"), A(r"n\approx9{,}63\ \text{mol}")]),
  ("Khối lượng khí (câu b)", [M(r"m=nM=9{,}63\cdot28"), A(r"m\approx270\ \text{g}")]),
  ("Thể tích ở điều kiện tiêu chuẩn (câu c)", [P("1 mol khí ở $0\\ ^\\circ\\text{C}$, 1 atm chiếm $22{,}4$ lít:"), M(r"V_0=n\cdot22{,}4=9{,}63\cdot22{,}4"), A(r"V_0\approx216\ \text{lít}")]),
  ("Kiểm tra", [P("Khí đang ở gần $20$ atm nên bị nén: $12$ lít $\\ll216$ lít ở $1$ atm, hợp lí."),
        P("Cách khác, dùng phương trình trạng thái cho cùng lượng khí:"), M(r"V_0=\dfrac{p_1V_1}{T_1}\cdot\dfrac{T_0}{p_0}=\dfrac{2{,}0.10^6\cdot12}{300}\cdot\dfrac{273}{1{,}013.10^5}\approx216\ \text{lít}")])],
  ["a) $n\\approx9{,}63\\ \\text{mol}$", "b) $m\\approx270\\ \\text{g}$", "c) $V_0\\approx216\\ \\text{lít}$"],
  "Nhận dạng: đề cho <strong>$p$, $V$, $T$ của một trạng thái</strong> và hỏi số mol, khối lượng → $pV=nRT$, đổi $V$ ra m³ và $T$ ra K."),
 sol(RC5, [
  ("Nhận ra lượng khí đã đổi", [P("Khí đã được dùng bớt nên lượng khí lúc đầu và lúc sau khác nhau; hằng số $pV/T=nR$ không còn chung."),
        A("T:Không dùng $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$; viết $pV=nRT$ riêng cho từng trạng thái.")]),
  ("Lúc mới nạp (câu a)", [P("$V=8{,}0$ lít $=8{,}0.10^{-3}\\ \\text{m}^3$; $T_1=27+273=300$ K."), M(r"n_1=\dfrac{p_1V}{RT_1}=\dfrac{4{,}5.10^6\cdot8{,}0.10^{-3}}{8{,}31\cdot300}=\dfrac{36000}{2493}"),
        A(r"n_1\approx14{,}44\ \text{mol}"), M(r"m_1=n_1M=14{,}44\cdot32"), A(r"m_1\approx462\ \text{g}")]),
  ("Lúc còn lại (câu a)", [P("$T_2=17+273=290$ K."), M(r"n_2=\dfrac{p_2V}{RT_2}=\dfrac{1{,}5.10^6\cdot8{,}0.10^{-3}}{8{,}31\cdot290}=\dfrac{12000}{2409{,}9}"),
        A(r"n_2\approx4{,}98\ \text{mol}"), M(r"m_2=n_2M=4{,}98\cdot32"), A(r"m_2\approx159\ \text{g}")]),
  ("Khối lượng đã dùng (câu b)", [M(r"\Delta m=m_1-m_2=462-159"), A(r"\Delta m\approx303\ \text{g}")]),
  ("Kiểm tra", [P("Khối lượng còn lại $\\dfrac{159}{462}\\approx34{,}4\\%$, gần tỉ số áp suất $\\dfrac{1{,}5}{4{,}5}\\approx33{,}3\\%$; chênh nhẹ vì nhiệt độ hai lần khác nhau ($300$ K và $290$ K)."),
        P("Khối lượng đã dùng nhỏ hơn $m_1$: hợp lí.")])],
  ["a) $m_1\\approx462\\ \\text{g}$ ; $m_2\\approx159\\ \\text{g}$", "b) $\\Delta m\\approx303\\ \\text{g}$"],
  "Nhận dạng: đề có <strong>xả bớt, đã dùng</strong> khí → lượng khí đổi, tính $n$ riêng bằng $pV=nRT$ cho từng trạng thái rồi trừ."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>bình kín, thể tích không đổi</b> và nhiệt độ đổi → nghĩ tới <b>$\dfrac{p_1}{T_1}=\dfrac{p_2}{T_2}$</b>, đổi sang Kelvin.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi nhiệt độ sang Kelvin", "Nhiệt độ sau khi nóng lên, tính theo Kelvin, là bao nhiêu?", 390, "K", 0.5,
       loi=r"Quên đổi, cứ dùng $117$ (độ C) hoặc cộng nhầm $273$ cho cả hai nhiệt độ rồi lại lấy tỉ số Celsius."),
  buoc("Áp suất khi nóng lên", "Áp suất khí sau khi nóng lên là bao nhiêu (đơn vị $10^5$ Pa)?", 3.12, "×10⁵ Pa", 0.02,
       loi=r"Lấy tỉ số Celsius $\dfrac{117}{27}$ nên ra áp suất lớn gấp hơn 4 lần; hoặc lật ngược tỉ số $\dfrac{T_1}{T_2}$ và ra áp suất nhỏ đi.",
       ke=[(r"Đẳng tích: $p_2=p_1\dfrac{T_2}{T_1}$ với $T$ Kelvin", True),
           (r"$p_2=p_1\dfrac{t_2}{t_1}$ với nhiệt độ Celsius", r"Thang Celsius không có gốc $0$ thật nên tỉ số $\dfrac{117}{27}$ vô nghĩa; phải dùng Kelvin."),
           (r"$p_2=p_1$ vì bình kín nên áp suất không đổi", r"Bình kín chỉ giữ $V$ và lượng khí; nhiệt độ tăng thì áp suất phải tăng.")]),
  buoc("Nhiệt độ để van mở", "Van mở khi khí nóng tới nhiệt độ nào, tính theo Kelvin?", 450, "K", 1,
       loi=r"Lật ngược tỉ số ($T_3=T_1\dfrac{p_1}{p_3}$) nên ra nhiệt độ thấp hơn $T_1$, hoặc nhân tỉ số áp suất với nhiệt độ Celsius.",
       ke=[(r"Vẫn đẳng tích: $T_3=T_1\dfrac{p_3}{p_1}$", True),
           (r"$T_3=T_1\dfrac{p_1}{p_3}$", r"Áp suất cần tăng thì nhiệt độ phải tăng, tức $T_3\gt T_1$; tỉ số lật ngược cho $T_3\lt T_1$."),
           (r"Tính theo Celsius: $t_3=t_1\dfrac{p_3}{p_1}$", r"Tỉ lệ thuận chỉ đúng với nhiệt độ Kelvin, Celsius không có gốc $0$ thật.")]),
  buoc("Đổi về độ C", "Nhiệt độ van mở, tính theo độ C, là bao nhiêu?", 177, "°C", 1,
       loi=r"Cộng $273$ thay vì trừ, hoặc quên đổi nên trả lời bằng kelvin."),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cả $p$, $V$, $T$ cùng đổi</b> với lượng khí không đổi → nghĩ tới <b>$\dfrac{p_1V_1}{T_1}=\dfrac{p_2V_2}{T_2}$</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi nhiệt độ ban đầu sang Kelvin", "Nhiệt độ ban đầu theo Kelvin là bao nhiêu?", 300, "K", 0.5,
       loi=r"Dùng thẳng $27$ (độ C) vào công thức."),
  buoc("Nhiệt độ cuối quá trình nén", "Nhiệt độ cuối quá trình nén theo Kelvin là bao nhiêu?", 450, "K", 1,
       loi=r"Dùng $\dfrac{p_1}{T_1}=\dfrac{p_2}{T_2}$ (bỏ quên thể tích đổi) sẽ ra $T_2=5400$ K; hoặc lật ngược một tỉ số.",
       ke=[(r"Dùng $\dfrac{p_1V_1}{T_1}=\dfrac{p_2V_2}{T_2}$ vì cả $p$, $V$, $T$ cùng đổi", True),
           (r"Dùng $\dfrac{p_1}{T_1}=\dfrac{p_2}{T_2}$ vì khí ở trong xi lanh kín", r"Thể tích đổi (từ $2{,}4$ xuống $0{,}20$ dm³) nên không dùng được hệ thức đẳng tích."),
           (r"Dùng $p_1V_1=p_2V_2$ (Boyle)", r"Boyle cần nhiệt độ không đổi, mà nhiệt độ cuối đã khác $27\,^\circ$C.")]),
  buoc("Đổi sang độ C", "Nhiệt độ cuối quá trình nén theo độ C là bao nhiêu?", 177, "°C", 1,
       loi=r"Cộng $273$ thay vì trừ."),
  buoc("Nén thật chậm", "Nếu nén thật chậm thì áp suất cuối là bao nhiêu atm?", 12, "atm", 0.2,
       loi=r"Vẫn dùng $T_2=450$ K cho trường hợp nén chậm, hoặc lật ngược tỉ số thể tích.",
       ke=[(r"Nhiệt độ không đổi nên $p_1V_1=p'_2V_2$ (Boyle)", True),
           (r"Vẫn dùng $\dfrac{p_1V_1}{T_1}=\dfrac{p_2V_2}{T_2}$ với $T_2$ vừa tìm được", r"Nén chậm thì khí không nóng lên, $T_2=T_1$; $T_2$ vừa tìm ứng với nén nhanh."),
           (r"$p'_2=p_1\dfrac{V_2}{V_1}$", r"Thể tích giảm thì áp suất phải tăng; tỉ số này cho áp suất nhỏ đi.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đường thẳng qua gốc trên đồ thị $p$–$T$</b> → nghĩ tới <b>đẳng tích, $\dfrac{p}{T}$ không đổi</b>; so hai đường tại cùng $T$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhận ra quá trình MN", "Quá trình MN là quá trình gì?", loi=r"Nhầm đường thẳng qua gốc với đẳng áp (đường nằm ngang); đẳng áp có $p$ không đổi còn MN có $p$ tăng theo $T$.",
       lua_chon=[(r"Đẳng tích ($V$ không đổi)", True),
                 (r"Đẳng nhiệt ($T$ không đổi)", r"Đẳng nhiệt thì $T$ không đổi, nhưng ở MN nhiệt độ tăng từ $300$ K lên $500$ K."),
                 (r"Đẳng áp ($p$ không đổi)", r"Đẳng áp thì $p$ không đổi, nhưng ở MN áp suất tăng theo $T$ (đường thẳng qua gốc).")]),
  buoc("Áp suất tại N", "Áp suất khí tại N là bao nhiêu (đơn vị $10^5$ Pa)?", 5.0, "×10⁵ Pa", 0.05,
       loi=r"Lật ngược tỉ số nhiệt độ ($p_N=p_M\dfrac{T_M}{T_N}$) ra $1{,}8.10^5$ Pa, hoặc cộng thêm hiệu nhiệt độ.",
       ke=[(r"Cùng đường (1): $p_N=p_M\dfrac{T_N}{T_M}$", True),
           (r"$p_N=p_M\dfrac{T_M}{T_N}$", r"Nhiệt độ tăng thì áp suất phải tăng, tức $p_N\gt p_M$; tỉ số lật ngược cho $p_N\lt p_M$."),
           (r"$p_N=p_M+(T_N-T_M)$", r"$p$ và $T$ khác đơn vị, không cộng được; $p$ tỉ lệ thuận với $T$ chứ không tăng thêm một lượng bằng nhau.")]),
  buoc("Thể tích ứng với đường (2)", "Thể tích bình ứng với đường (2) là bao nhiêu lít?", 8.0, "lít", 0.1,
       loi=r"Dùng $\dfrac{p_M}{T_M}=\dfrac{p_Q}{T_Q}$ cho M và Q; hai điểm thuộc hai đường khác nhau nên hằng số $\dfrac{p}{T}$ khác nhau.",
       ke=[(r"M, Q cùng $T$ nên $p_MV_1=p_QV_2$", True),
           (r"$V_2=V_1\dfrac{p_Q}{p_M}$", r"Cùng $T$, áp suất nhỏ hơn thì thể tích phải lớn hơn; tỉ số này cho $V_2\lt V_1$."),
           (r"Dùng $\dfrac{p}{T}$ không đổi cho M và Q", r"M và Q thuộc hai đường (hai thể tích) khác nhau; $\dfrac{p}{T}$ chỉ không đổi trên cùng một đường.")]),
  buoc("So sánh hai đường", "Đường nào ứng với thể tích lớn hơn?", loi=r"Đoán theo cảm giác «đường dốc hơn thì to hơn»; phải so hai giá trị $p$ tại cùng một $T$.",
       lua_chon=[(r"Đường nằm dưới (đường (2))", True),
                 (r"Đường nằm trên (đường (1))", r"Cùng $T$, đường trên có $p$ lớn hơn; vì $\dfrac{pV}{T}$ không đổi nên $V$ phải nhỏ hơn."),
                 (r"Không so sánh được vì hai đường ở hai bình khác nhau", r"Cùng một lượng khí, so tại cùng $T$ là so sánh được.")],
       ke=[(r"So $p$ tại cùng một $T$, rồi suy ra $V$ từ $\dfrac{pV}{T}$ không đổi", True),
           (r"Chọn đường dốc hơn là thể tích lớn hơn", r"Độ dốc chỉ cho biết đường nằm trên hay dưới; muốn suy ra $V$ phải dùng $\dfrac{pV}{T}$ không đổi."),
           (r"So $V$ bằng cách so $\dfrac{p}{T}$ của hai đường rồi cho $V$ tỉ lệ thuận", r"$\dfrac{p}{T}=\dfrac{nR}{V}$ nên $V$ tỉ lệ nghịch với $\dfrac{p}{T}$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Đề cho <b>$p$, $V$, $T$ của một trạng thái</b> và hỏi số mol, khối lượng → nghĩ tới <b>$pV=nRT$</b>, đổi $V$ ra m³.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi đơn vị sang SI", "Thể tích bình theo m³ là bao nhiêu?", 0.012, "m³", 0.0005,
       loi=r"Quên đổi lít sang m³ (lấy $V=12$) làm $n$ lớn gấp $1000$ lần; hoặc đổi sai thành $0{,}12\ \text{m}^3$."),
  buoc("Số mol khí", "Số mol khí trong bình là bao nhiêu?", 9.63, "mol", 0.05,
       loi=r"Dùng $V=12$ (lít) với $R=8{,}31$ làm $n$ lớn gấp $1000$ lần; hoặc dùng $t=27$ thay cho $T=300$ K.",
       ke=[(r"$n=\dfrac{pV}{RT}$ với $V$ theo m³ và $T$ theo K", True),
           (r"$n=\dfrac{pV}{RT}$ giữ $V$ theo lít", r"$R=8{,}31$ J/(mol·K) đòi $V$ theo m³; để lít sẽ sai $1000$ lần."),
           (r"$n=\dfrac{RT}{pV}$", r"Lật ngược: $n$ tỉ lệ thuận với $p$ và $V$, không phải với $T$ ở tử số.")]),
  buoc("Khối lượng khí", "Khối lượng khí nitrogen trong bình là bao nhiêu gam?", 270, "g", 2,
       loi=r"Chia thay vì nhân ($m=\dfrac{n}{M}$), hoặc đọc kết quả là kilôgam.",
       ke=[(r"$m=nM$ với $M=28$ g/mol cho ra gam", True),
           (r"$m=\dfrac{n}{M}$", r"Từ $n=\dfrac{m}{M}$ suy ra $m=nM$; chia cho $M$ là sai đại lượng."),
           (r"$m=nM$ rồi đọc kết quả là kilôgam", r"$M=28$ g/mol nên $nM$ ra gam; muốn kilôgam phải đổi thêm $10^{-3}$.")]),
  buoc("Thể tích ở điều kiện tiêu chuẩn", "Thể tích lượng khí này ở điều kiện tiêu chuẩn là bao nhiêu lít?", 216, "lít", 1,
       loi=r"Dùng $24{,}79$ lít/mol (điều kiện chuẩn $25\ ^\circ\text{C}$, $1$ bar) hoặc giữ nguyên $12$ lít vì «bình không đổi».",
       ke=[(r"$V_0=n\cdot22{,}4$ lít", True),
           (r"$V_0=12$ lít vì thể tích bình không đổi", r"Đưa về điều kiện tiêu chuẩn là đổi $p$ và $T$ nên thể tích khí thay đổi, không còn là thể tích bình."),
           (r"$V_0=n\cdot24{,}79$ lít", r"$24{,}79$ lít/mol ứng với điều kiện chuẩn ($25\ ^\circ\text{C}$, $1$ bar); đề hỏi điều kiện tiêu chuẩn ($0\ ^\circ\text{C}$, $1$ atm).")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>xả bớt, đã dùng</b> khí → lượng khí đổi, nghĩ tới <b>$pV=nRT$</b> riêng từng trạng thái, rồi trừ.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhận ra lượng khí đã đổi", "Có dùng $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$ cho hai trạng thái này không?", loi=r"Thấy bình vẫn kín và thể tích không đổi nên dùng luôn phương trình trạng thái, quên rằng khí đã được dùng bớt.",
       lua_chon=[(r"Không: lượng khí đã giảm nên phải tính $n$ riêng cho từng trạng thái", True),
                 (r"Có, vì bình thép vẫn kín", r"Bình kín lúc đo, nhưng khí đã được dùng bớt trước đó; hằng số $\dfrac{pV}{T}=nR$ đã nhỏ đi."),
                 (r"Có, vì thể tích bình không đổi", r"Thể tích không đổi chưa đủ; còn phải giữ nguyên lượng khí.")]),
  buoc("Lúc mới nạp", "Số mol oxygen lúc mới nạp là bao nhiêu?", 14.44, "mol", 0.1,
       loi=r"Quên đổi lít sang m³, hoặc thế $t=27$ thay cho $T=300$ K.",
       ke=[(r"$n_1=\dfrac{p_1V}{RT_1}$ với $V$ theo m³, $T_1=300$ K", True),
           (r"Thế $t_1=27$ trực tiếp vào mẫu số", r"$T$ phải đổi ra Kelvin."),
           (r"Dùng $n=\dfrac{V}{22{,}4}$ cho cả bình", r"Bình không ở điều kiện tiêu chuẩn (đang ở $27\ ^\circ\text{C}$ và áp suất rất lớn).")]),
  buoc("Lúc còn lại", "Số mol oxygen còn lại trong bình là bao nhiêu?", 4.98, "mol", 0.03,
       loi=r"Giữ $T=300$ K cho trạng thái 2, hoặc suy $n_2=n_1\dfrac{p_2}{p_1}$ (chỉ đúng khi nhiệt độ không đổi) ra $4{,}81$ mol.",
       ke=[(r"$n_2=\dfrac{p_2V}{RT_2}$ với $T_2=290$ K", True),
           (r"Vẫn dùng $T=300$ K vì cùng một bình", r"Bình đã để trong kho ở $17\ ^\circ\text{C}$, tức $290$ K."),
           (r"$n_2=n_1\dfrac{p_2}{p_1}$", r"Chỉ đúng khi nhiệt độ không đổi; ở đây nhiệt độ đã đổi từ $300$ K sang $290$ K.")]),
  buoc("Khối lượng đã dùng", "Khối lượng oxygen đã dùng là bao nhiêu gam?", 303, "g", 2,
       loi=r"Lấy hiệu số mol rồi quên nhân $M$, hoặc dùng cùng một nhiệt độ cho hai áp suất.",
       ke=[(r"$\Delta m=(n_1-n_2)M$", True),
           (r"$\Delta m=(p_1-p_2)\dfrac{V}{RT}$ với $T=300$ K", r"Hai áp suất ứng với hai nhiệt độ khác nhau ($300$ K và $290$ K), không dùng chung một $T$; kết quả còn là số mol, thiếu nhân $M$."),
           (r"$\Delta m=n_1-n_2$", r"Hiệu số mol chưa phải khối lượng; phải nhân $M=32$ g/mol.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 8, "Bài 7. Phương trình trạng thái của khí lí tưởng", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
