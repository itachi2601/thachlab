"""Bài tập mẫu bài 7 "Bài 6. Định luật Boyle. Định luật Charles" (Vật lí 12) — 5 dạng theo quét ket-qua/7.quet-dang.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-7.py   (idempotent)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_7 import *

J = os.path.join(HERE, "7.json")

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Nén khí ở nhiệt độ không đổi (định luật Boyle)",
      topic="Quá trình đẳng nhiệt và định luật Boyle",
      problem_html=r"""<p>Thân một bơm xe đạp được bịt kín đầu ra, bên trong có $240\ \text{cm}^3$ không khí ở áp suất $1{,}0\cdot10^5\ \text{Pa}$. Ấn cán bơm thật chậm cho thể tích khí còn $80\ \text{cm}^3$. Coi nhiệt độ khí không đổi và khí không lọt ra ngoài.</p><ol type="a"><li>Tính áp suất khí lúc này.</li><li>Nếu tiếp tục ấn đến khi áp suất khí đạt $4{,}8\cdot10^5\ \text{Pa}$ thì thể tích khí còn bao nhiêu?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Nung khí ở áp suất không đổi, đổi sang kenvin (định luật Charles)",
      topic="Quá trình đẳng áp và định luật Charles",
      problem_html=r"""<p>Một xilanh đặt thẳng đứng, miệng hướng lên, có pittông nhẹ trượt không ma sát. Phía trên pittông thông với khí trời nên áp suất khí trong xilanh luôn không đổi. Ban đầu khí chiếm $450\ \text{cm}^3$ ở $17\ ^\circ\text{C}$.</p><ol type="a"><li>Đặt xilanh vào chậu nước nóng cho khí nóng đều tới $75\ ^\circ\text{C}$. Tính thể tích khí lúc đó và phần thể tích tăng thêm.</li><li>Sau đó làm lạnh khí (áp suất vẫn không đổi) cho thể tích chỉ còn $360\ \text{cm}^3$. Tính nhiệt độ của khí lúc đó theo $^\circ\text{C}$.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị V–T của các đường đẳng áp",
      topic="Đọc đồ thị các đẳng quá trình",
      problem_html=r"""<p>Trên hệ trục $V$–$T$ (trục tung $V$ tính bằng lít, trục hoành $T$ tính bằng kenvin), một lượng khí xác định được vẽ hai đường (1) và (2), mỗi đường là một đoạn thẳng kéo dài đi qua gốc toạ độ $O$. Tại $T=300\ \text{K}$, đường (1) có điểm $A$ ứng với $V=4\ \text{lít}$ và đường (2) có điểm $B$ ứng với $V=6\ \text{lít}$.</p><ol type="a"><li>Mỗi đường mô tả quá trình nào? Đường nào ứng với áp suất lớn hơn?</li><li>Tính tỉ số $\dfrac{p_1}{p_2}$ giữa áp suất khí ở đường (1) và đường (2).</li><li>Khí ở đường (2) được nung đến $450\ \text{K}$. Tính thể tích khí lúc đó.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Hai giai đoạn nối tiếp: đẳng nhiệt rồi đẳng áp",
      topic="Quá trình đẳng áp và định luật Charles",
      problem_html=r"""<p>Một xilanh kín có pittông chứa $3{,}0$ lít khí ở áp suất $1{,}0\ \text{atm}$ và nhiệt độ $27\ ^\circ\text{C}$. Giai đoạn 1: đẩy pittông thật chậm (nhiệt độ khí không đổi) đến khi áp suất đạt $2{,}5\ \text{atm}$. Giai đoạn 2: giữ nguyên áp suất $2{,}5\ \text{atm}$ và nung nóng khí tới $127\ ^\circ\text{C}$.</p><ol type="a"><li>Tính thể tích khí sau giai đoạn 1.</li><li>Tính thể tích khí sau giai đoạn 2.</li><li>So với lúc đầu, thể tích khí cuối cùng giảm bao nhiêu lít?</li></ol>"""),
 dict(label="Dạng 5 · Nâng cao · Khí bị cột thuỷ ngân giam trong ống, lật ống",
      topic="Quá trình đẳng nhiệt và định luật Boyle",
      problem_html=r"""<p>Một ống thuỷ tinh dài $80\ \text{cm}$, tiết diện đều, một đầu kín, một đầu hở. Đặt ống thẳng đứng, miệng hướng lên: một cột thuỷ ngân cao $20\ \text{cm}$ giam ở đáy ống (đầu kín) một cột không khí dài $28\ \text{cm}$. Áp suất khí quyển $p_0=760\ \text{mmHg}$. Lật nhẹ nhàng ống $180^\circ$ cho miệng hướng xuống; thuỷ ngân không chảy ra ngoài và nhiệt độ khí không đổi.</p><ol type="a"><li>Tính áp suất khí bị giam khi miệng ống hướng lên (theo $\text{mmHg}$).</li><li>Tính áp suất khí bị giam sau khi lật ống.</li><li>Tính chiều dài cột khí sau khi lật ống.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [(r'"bịt kín đầu ra … khí không lọt ra ngoài"', r"Lượng khí xác định", r"⚠ Khối lượng khí không đổi mới dùng được định luật Boyle"),
  (r'"có $240\ \text{cm}^3$ không khí ở $1{,}0\cdot10^5$ Pa"', r"$V_1=240\ \text{cm}^3$ ; $p_1=1{,}0\cdot10^5$ Pa", r"Trạng thái 1: ba thông số $p$, $V$, $T$"),
  (r'"ấn cán bơm thật chậm … nhiệt độ không đổi"', r"$T$ không đổi", r"⚠ Nhiệt độ không đổi → đẳng nhiệt → $p_1V_1=p_2V_2$"),
  (r'"thể tích khí còn $80\ \text{cm}^3$"', r"$V_2=80\ \text{cm}^3$", r"Trạng thái 2 ; hai thể tích chỉ cần cùng đơn vị"),
  (r'"tính áp suất khí lúc này"', r"Cần $p_2$", r"$p_2=\dfrac{p_1V_1}{V_2}$"),
  (r'"áp suất khí đạt $4{,}8\cdot10^5$ Pa"', r"$p_3=4{,}8\cdot10^5$ Pa ; cần $V_3$", r"$V_3=\dfrac{p_1V_1}{p_3}$")],
 [(r'"pittông nhẹ trượt không ma sát … thông với khí trời"', r"Áp suất khí không đổi", r"⚠ Áp suất không đổi → đẳng áp → định luật Charles"),
  (r'"khí chiếm $450\ \text{cm}^3$ ở $17\ ^\circ\text{C}$"', r"$V_1=450\ \text{cm}^3$ ; $t_1=17\ ^\circ\text{C}$", r"⚠ Đổi sang kenvin: $T=t+273$"),
  (r'"nóng đều tới $75\ ^\circ\text{C}$"', r"$t_2=75\ ^\circ\text{C}$", r"$\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}$ ; $T$ là nhiệt độ tuyệt đối"),
  (r'"thể tích khí lúc đó và phần thể tích tăng thêm"', r"Cần $V_2$ và $\Delta V$", r"$V_2=V_1\dfrac{T_2}{T_1}$ ; $\Delta V=V_2-V_1$"),
  (r'"làm lạnh … thể tích chỉ còn $360\ \text{cm}^3$"', r"$V_3=360\ \text{cm}^3$ ; $p$ vẫn không đổi", r"Lại dùng Charles với trạng thái 3"),
  (r'"nhiệt độ của khí lúc đó theo $^\circ\text{C}$"', r"Cần $t_3$", r"$T_3=T_1\dfrac{V_3}{V_1}$ ; $t=T-273$")],
 [(r'"hai đường … mỗi đường là đoạn thẳng kéo dài qua gốc $O$"', r"Đồ thị $V$–$T$, đường thẳng qua $O$", r"⚠ Đường thẳng kéo dài qua $O$ trên $V$–$T$ là đẳng áp ; mỗi đường ứng với một áp suất"),
  (r'"tại $T=300$ K, điểm $A$ ứng với $V=4$ lít"', r"$A$: $T=300$ K ; $V_A=4$ lít", r"Điểm trên đường (1)"),
  (r'"điểm $B$ ứng với $V=6$ lít"', r"$B$: $T=300$ K ; $V_B=6$ lít", r"Điểm trên đường (2) ; ⚠ $A$ và $B$ cùng nhiệt độ nên so sánh $p$ bằng định luật Boyle"),
  (r'"mỗi đường mô tả quá trình nào? đường nào áp suất lớn hơn?"', r"Cần tên quá trình ; so sánh $p_1$ với $p_2$", r"Áp suất càng nhỏ, đường càng cao"),
  (r'"tính tỉ số $p_1/p_2$"', r"Cần $\dfrac{p_1}{p_2}$", r"$p_AV_A=p_BV_B$ (cùng $T$)"),
  (r'"khí ở đường (2) được nung đến $450$ K"', r"$T=450$ K trên đường (2) ; cần $V$", r"Cùng một đường (cùng $p$): $\dfrac{V_B}{T_B}=\dfrac{V}{T}$")],
 [(r'"xilanh kín có pittông chứa $3{,}0$ lít khí ở $1{,}0$ atm và $27\ ^\circ\text{C}$"', r"$V_1=3{,}0$ lít ; $p_1=1{,}0$ atm ; $t_1=27\ ^\circ\text{C}$", r"Trạng thái 1 ; đổi $T_1$ ra kenvin"),
  (r'"giai đoạn 1: đẩy pittông thật chậm (nhiệt độ không đổi) đến $2{,}5$ atm"', r"$T$ không đổi ; $p_2=2{,}5$ atm", r"⚠ Giai đoạn 1 đẳng nhiệt → định luật Boyle: $p_1V_1=p_2V_2$"),
  (r'"giai đoạn 2: giữ nguyên $2{,}5$ atm, nung tới $127\ ^\circ\text{C}$"', r"$p$ không đổi ; $t_3=127\ ^\circ\text{C}$", r"⚠ Giai đoạn 2 đẳng áp → định luật Charles, dùng nhiệt độ kenvin"),
  (r'"thể tích sau giai đoạn 1"', r"Cần $V_2$", r"$V_2=\dfrac{p_1V_1}{p_2}$"),
  (r'"thể tích sau giai đoạn 2"', r"Cần $V_3$ ; xuất phát từ $V_2$, không phải $V_1$", r"$\dfrac{V_2}{T_2}=\dfrac{V_3}{T_3}$"),
  (r'"so với lúc đầu, thể tích cuối giảm bao nhiêu"', r"Cần $V_1-V_3$", r"Hiệu hai thể tích, cùng đơn vị lít")],
 [(r'"ống tiết diện đều … giam một cột không khí dài $28$ cm"', r"$l_1=28$ cm ; $V=S\,l$", r"Tiết diện đều nên $V$ tỉ lệ với chiều dài $l$: $p_1l_1=p_2l_2$"),
  (r'"cột thuỷ ngân cao $20$ cm"', r"$h=20$ cm $=200$ mm", r"⚠ Đổi $h$ ra mm cho cùng đơn vị mmHg với $p_0$"),
  (r'"$p_0=760$ mmHg"', r"$p_0=760$ mmHg", r"Cột Hg cao $h$ mm gây thêm áp suất $h$ mmHg"),
  (r'"miệng hướng lên … đáy ống kín"', r"Hg nằm trên khí", r"⚠ Miệng hướng lên: khí chịu cả $p_0$ và cột Hg đè lên, $p=p_0+h$"),
  (r'"lật ống … miệng hướng xuống"', r"Hg nằm dưới khí", r"⚠ Miệng hướng xuống: khí cân bằng với $p_0$ đẩy lên và cột Hg kéo xuống, $p=p_0-h$"),
  (r'"nhiệt độ không đổi ; Hg không chảy ra"', r"$T$ không đổi ; lượng khí xác định", r"Định luật Boyle: $p_1l_1=p_2l_2$"),
  (r'"chiều dài cột khí sau khi lật"', r"Cần $l_2$", r"$l_2=\dfrac{p_1l_1}{p_2}$")],
]

# ═════════════ LỜI GIẢI (mỗi bước một khối, mỗi công thức một dòng) ═════════════
R1 = [r"<strong>Khái niệm:</strong> ba thông số trạng thái $p$, $V$, $T$ ; đẳng nhiệt là quá trình giữ $T$ không đổi.",
      r"<strong>Định luật Boyle:</strong> $T$ không đổi thì $p$ tỉ lệ nghịch với $V$, tức $pV=\text{hằng số}$.",
      r"<strong>Công thức:</strong> $p_1V_1=p_2V_2$ ($p$ cùng đơn vị, $V$ cùng đơn vị).",
      r"⚠ <strong>Điều kiện:</strong> khối lượng khí xác định (không lọt ra ngoài) và nhiệt độ không đổi (ấn thật chậm)."]
R2 = [r"<strong>Khái niệm:</strong> đẳng áp là quá trình giữ $p$ không đổi ; nhiệt độ tuyệt đối $T(\text{K})=t(^\circ\text{C})+273$.",
      r"<strong>Định luật Charles:</strong> $p$ không đổi thì $V$ tỉ lệ thuận với $T$ (kenvin).",
      r"<strong>Công thức:</strong> $\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}$.",
      r"⚠ <strong>Điều kiện:</strong> $p$ không đổi (pittông tự do, thông khí trời) ; $T$ phải đổi ra kenvin trước khi lập tỉ số."]
R3 = [r"<strong>Khái niệm:</strong> trên đồ thị $V$–$T$, đường thẳng kéo dài qua $O$ là đường đẳng áp ; áp suất càng nhỏ, đường càng cao.",
      r"<strong>Định luật Charles:</strong> trên một đường (cùng $p$): $\dfrac{V}{T}=\text{hằng số}$.",
      r"<strong>Định luật Boyle:</strong> hai điểm cùng $T$: $p_1V_1=p_2V_2$.",
      r"⚠ <strong>Điều kiện:</strong> Charles chỉ dùng cho hai điểm cùng một đường ; Boyle chỉ dùng cho hai điểm cùng nhiệt độ."]
R4 = [r"<strong>Khái niệm:</strong> một khối khí có thể qua nhiều quá trình nối tiếp ; mỗi quá trình dùng đúng một định luật.",
      r"<strong>Công thức:</strong> $T$ không đổi: $p_1V_1=p_2V_2$ · $p$ không đổi: $\dfrac{V_2}{T_2}=\dfrac{V_3}{T_3}$ · $T=t+273$.",
      r"Thể tích cuối của giai đoạn trước là thể tích đầu của giai đoạn sau.",
      r"⚠ <strong>Điều kiện:</strong> Boyle chỉ cho giai đoạn giữ $T$ ; Charles chỉ cho giai đoạn giữ $p$ ; $T$ đổi ra kenvin."]
R5 = [r"<strong>Khái niệm:</strong> khí bị giam bởi cột thuỷ ngân chịu áp suất khí quyển và áp suất cột Hg (cao $h$ mm gây $h$ mmHg).",
      r"<strong>Công thức:</strong> miệng hướng lên: $p=p_0+h$ · miệng hướng xuống: $p=p_0-h$ · Boyle: $p_1V_1=p_2V_2$.",
      r"Tiết diện đều nên $V=S\,l$, Boyle viết thành $p_1l_1=p_2l_2$.",
      r"⚠ <strong>Điều kiện:</strong> $p_0$ và $h$ cùng đơn vị mmHg ; nhiệt độ không đổi (lật nhẹ nhàng) ; thuỷ ngân không chảy ra ngoài."]

SOLS = [
 sol(R1, [
  ("Nhận dạng quá trình", [P("Khí bị bịt kín nên khối lượng khí không đổi ; ấn thật chậm nên nhiệt độ không đổi."),
     A(r"T:Quá trình <strong>đẳng nhiệt</strong>, dùng định luật Boyle $p_1V_1=p_2V_2$.")]),
  ("Áp suất sau khi nén (câu a)", [P(r"Hai thể tích cùng đơn vị $\text{cm}^3$ nên không cần đổi:"), M(r"p_2=\dfrac{p_1V_1}{V_2}=\dfrac{1{,}0\cdot10^5\cdot240}{80}"),
     A(r"p_2=3{,}0\cdot10^5\ \text{Pa}")]),
  ("Thể tích khi áp suất đạt $4{,}8\cdot10^5$ Pa (câu b)", [P("Vẫn là quá trình đẳng nhiệt của cùng lượng khí, xuất phát từ trạng thái 1:"),
     M(r"V_3=\dfrac{p_1V_1}{p_3}=\dfrac{1{,}0\cdot10^5\cdot240}{4{,}8\cdot10^5}"), A(r"V_3=50\ \text{cm}^3")]),
  ("Kiểm tra", [P(r"Tích $pV$: $3{,}0\cdot10^5\cdot80=2{,}4\cdot10^7$ và $4{,}8\cdot10^5\cdot50=2{,}4\cdot10^7$, bằng $p_1V_1=1{,}0\cdot10^5\cdot240$ ✓."),
     P(r"Thể tích giảm $3$ lần thì áp suất tăng $3$ lần ✓."),
     P(r"$p_3\gt p_2$ nên $V_3\lt V_2$ ✓ (nén thêm thì thể tích nhỏ hơn).")])],
  [r"a) $p_2=3{,}0\cdot10^5\ \text{Pa}$", r"b) $V_3=50\ \text{cm}^3$"],
  r"Nhận dạng: đề có <strong>nhiệt độ không đổi / ấn (kéo) thật chậm</strong> và cho ba trong bốn giá trị $p_1,V_1,p_2,V_2$ → $p_1V_1=p_2V_2$."),

 sol(R2, [
  ("Đổi nhiệt độ ra kenvin", [P(r"Hệ thức Charles chỉ đúng với nhiệt độ tuyệt đối:"), M(r"T_1=17+273=290\ \text{K}"), M(r"T_2=75+273"), A(r"T_2=348\ \text{K}")]),
  ("Thể tích sau khi nung (câu a)", [P("Áp suất không đổi nên dùng định luật Charles:"), M(r"\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}\Rightarrow V_2=V_1\dfrac{T_2}{T_1}"),
     M(r"V_2=450\cdot\dfrac{348}{290}"), A(r"V_2=540\ \text{cm}^3")]),
  ("Thể tích tăng thêm (câu a)", [M(r"\Delta V=V_2-V_1=540-450"), A(r"\Delta V=90\ \text{cm}^3")]),
  ("Nhiệt độ khi làm lạnh (câu b)", [P(r"Trạng thái 3 có $V_3=360\ \text{cm}^3$, áp suất vẫn không đổi, so với trạng thái 1:"),
     M(r"\dfrac{V_3}{T_3}=\dfrac{V_1}{T_1}\Rightarrow T_3=T_1\dfrac{V_3}{V_1}"), M(r"T_3=290\cdot\dfrac{360}{450}"), A(r"T_3=232\ \text{K}")]),
  ("Đổi về độ C (câu b)", [P("Đề hỏi nhiệt độ theo $^\\circ\\text{C}$:"), M(r"t_3=T_3-273=232-273"), A(r"t_3=-41\ ^\circ\text{C}")]),
  ("Kiểm tra", [P(r"Tỉ số $\dfrac{348}{290}=1{,}2=\dfrac{540}{450}$ ✓ ; $\dfrac{232}{290}=0{,}8=\dfrac{360}{450}$ ✓."),
     P(r"Nếu lấy tỉ số Celsius: $450\cdot\dfrac{75}{17}\approx1985\ \text{cm}^3$, gấp hơn $4$ lần dù nhiệt độ tuyệt đối chỉ tăng $20\%$ — vô lí."),
     P(r"$V_3\lt V_1$ nên $T_3\lt T_1$ ✓ (làm lạnh thì thể tích giảm).")])],
  [r"a) $V_2=540\ \text{cm}^3$ · $\Delta V=90\ \text{cm}^3$", r"b) $t_3=-41\ ^\circ\text{C}$"],
  r"Nhận dạng: đề cho <strong>áp suất không đổi</strong> và nhiệt độ theo <strong>°C</strong> → đổi sang kenvin rồi dùng $\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}$."),

 sol(R3, [
  ("Nhận dạng đường trên đồ thị", [P(r"Mỗi đường là đoạn thẳng kéo dài qua $O$ trên đồ thị $V$–$T$, nên $V$ tỉ lệ thuận với $T$ dọc theo từng đường."),
     A(r"T:Cả hai đường đều là đường <strong>đẳng áp</strong> (mỗi đường ứng với một áp suất).")]),
  ("So sánh áp suất hai đường", [P(r"Hai điểm $A$, $B$ cùng $T=300\ \text{K}$ : $V_A=4\ \text{lít}\lt V_B=6\ \text{lít}$."),
     P("Cùng nhiệt độ, thể tích nhỏ hơn thì áp suất lớn hơn (định luật Boyle). Cách nhớ: áp suất càng nhỏ, đường càng cao."),
     A(r"T:Đường (1) ứng với <strong>áp suất lớn hơn</strong>.")]),
  ("Tỉ số áp suất", [P(r"$A$ và $B$ cùng nhiệt độ nên dùng định luật Boyle:"), M(r"p_1V_A=p_2V_B\Rightarrow\dfrac{p_1}{p_2}=\dfrac{V_B}{V_A}"),
     M(r"\dfrac{p_1}{p_2}=\dfrac{6}{4}"), A(r"\dfrac{p_1}{p_2}=1{,}5")]),
  ("Thể tích khi nung đến 450 K", [P(r"Điểm mới nằm trên đường (2), cùng áp suất với $B$ nên dùng định luật Charles:"), M(r"\dfrac{V}{T}=\dfrac{V_B}{T_B}\Rightarrow V=V_B\dfrac{T}{T_B}"),
     M(r"V=6\cdot\dfrac{450}{300}"), A(r"V=9\ \text{lít}")]),
  ("Kiểm tra", [P(r"Đường (1) ở $450\ \text{K}$ có $V=4\cdot\dfrac{450}{300}=6\ \text{lít}$ ; đường (2) có $9\ \text{lít}$ nên đường (2) cao hơn ✓ (áp suất nhỏ hơn)."),
     P(r"Tỉ số thể tích cùng $T$: $\dfrac{9}{6}=1{,}5=\dfrac{p_1}{p_2}$ ✓, cùng kết quả ở $300\ \text{K}$.")])],
  [r"a) Cả hai đều đẳng áp ; đường (1) ứng với áp suất lớn hơn", r"b) $\dfrac{p_1}{p_2}=1{,}5$", r"c) $V=9\ \text{lít}$"],
  r"Nhận dạng: <strong>đường thẳng qua $O$ trên $V$–$T$</strong> → đẳng áp ; hai điểm <strong>cùng $T$</strong> → so sánh $p$ bằng $pV$ không đổi."),

 sol(R4, [
  ("Nhận dạng hai giai đoạn", [P("Giai đoạn 1: nhiệt độ không đổi, áp suất tăng. Giai đoạn 2: áp suất không đổi, nhiệt độ tăng."),
     A(r"T:Giai đoạn 1 <strong>đẳng nhiệt</strong> (Boyle) ; giai đoạn 2 <strong>đẳng áp</strong> (Charles).")]),
  ("Thể tích sau giai đoạn 1 (câu a)", [M(r"p_1V_1=p_2V_2\Rightarrow V_2=\dfrac{p_1V_1}{p_2}"), M(r"V_2=\dfrac{1{,}0\cdot3{,}0}{2{,}5}"), A(r"V_2=1{,}2\ \text{lít}"),
     P(r"Nhiệt độ vẫn $T_2=T_1=27+273=300\ \text{K}$.")]),
  ("Nhiệt độ cuối (kenvin)", [P("Đổi nhiệt độ cuối ra kenvin cho giai đoạn 2:"), M(r"T_3=127+273"), A(r"T_3=400\ \text{K}")]),
  ("Thể tích sau giai đoạn 2 (câu b)", [P(r"Xuất phát từ $V_2$ (không phải $V_1$), áp suất $2{,}5\ \text{atm}$ không đổi:"),
     M(r"\dfrac{V_2}{T_2}=\dfrac{V_3}{T_3}\Rightarrow V_3=V_2\dfrac{T_3}{T_2}"), M(r"V_3=1{,}2\cdot\dfrac{400}{300}"), A(r"V_3=1{,}6\ \text{lít}")]),
  ("Độ giảm thể tích (câu c)", [M(r"\Delta V=V_1-V_3=3{,}0-1{,}6"), A(r"\Delta V=1{,}4\ \text{lít}")]),
  ("Kiểm tra", [P(r"Nén $2{,}5$ lần rồi nở $\dfrac{400}{300}=\dfrac{4}{3}$ lần: $V_3=3{,}0\cdot\dfrac{1}{2{,}5}\cdot\dfrac{4}{3}=1{,}6\ \text{lít}$ ✓."),
     P(r"Nếu bỏ giai đoạn 1 và dùng Charles từ $3{,}0\ \text{lít}$ ra $4{,}0\ \text{lít}$ — thể tích tăng, ngược với thực tế vì khí đã bị nén."),
     P(r"Ba trạng thái đều có $p_3V_3\ne p_1V_1$ vì nhiệt độ khác nhau ; chỉ hai trạng thái cùng $T$ mới có $pV$ bằng nhau.")])],
  [r"a) $V_2=1{,}2\ \text{lít}$", r"b) $V_3=1{,}6\ \text{lít}$", r"c) $\Delta V=1{,}4\ \text{lít}$"],
  r"Nhận dạng: <strong>hai giai đoạn liên tiếp</strong> → tách từng giai đoạn: giữ $T$ thì Boyle, giữ $p$ thì Charles, nối bằng thể tích cuối của giai đoạn trước."),

 sol(R5, [
  ("Áp suất khí khi miệng hướng lên (câu a)", [P(r"Cột Hg nằm trên khí, khí chịu $p_0$ và áp suất cột Hg. Đổi $h=20\ \text{cm}=200\ \text{mm}$:"),
     M(r"p_1=p_0+h=760+200"), A(r"p_1=960\ \text{mmHg}")]),
  ("Áp suất khí sau khi lật (câu b)", [P(r"Hg nằm dưới khí: khí cùng cột Hg cân bằng với áp suất khí quyển đẩy lên từ miệng ống:"),
     M(r"p_2+h=p_0\Rightarrow p_2=p_0-h=760-200"), A(r"p_2=560\ \text{mmHg}")]),
  ("Chiều dài cột khí sau khi lật (câu c)", [P(r"Nhiệt độ không đổi, tiết diện đều nên $V\sim l$ :"), M(r"p_1l_1=p_2l_2\Rightarrow l_2=\dfrac{p_1l_1}{p_2}"),
     M(r"l_2=\dfrac{960\cdot28}{560}"), A(r"l_2=48\ \text{cm}")]),
  ("Kiểm tra", [P(r"$p_1l_1=960\cdot28=26880$ và $p_2l_2=560\cdot48=26880$ ✓."),
     P(r"$l_2+h=48+20=68\ \text{cm}\lt80\ \text{cm}$ nên cột Hg vẫn còn trong ống, đúng giả thiết 'không chảy ra ngoài'."),
     P(r"$p_2\lt p_1$ nên khí dãn ra, $l_2\gt l_1$ ✓.")])],
  [r"a) $p_1=960\ \text{mmHg}$", r"b) $p_2=560\ \text{mmHg}$", r"c) $l_2=48\ \text{cm}$"],
  r"Nhận dạng: <strong>cột thuỷ ngân giam khí</strong> → áp suất khí $=p_0\pm h$ (miệng lên: cộng, miệng xuống: trừ), rồi $p_1l_1=p_2l_2$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>nhiệt độ không đổi</b> hoặc <b>ấn/kéo thật chậm</b> → nghĩ tới <b>p₁V₁ = p₂V₂</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhận dạng quá trình", "Khí trong thân bơm biến đổi theo quá trình nào?",
       loi=r"Thấy chữ 'ấn' nên cho rằng thể tích không đổi, hoặc bỏ qua hai điều kiện 'bịt kín' và 'nhiệt độ không đổi' của định luật Boyle.",
       lua_chon=[(r"Đẳng nhiệt: nhiệt độ giữ không đổi, $p$ và $V$ cùng thay đổi", True),
                 (r"Đẳng áp: áp suất giữ không đổi", r"Khi nén, khí bị dồn lại nên áp suất tăng ; áp suất không giữ nguyên."),
                 (r"Đẳng tích: thể tích giữ không đổi", r"Ấn cán bơm làm thể tích khí giảm, nên thể tích không giữ nguyên.")]),
  buoc("Áp suất sau khi nén", "Áp suất khí $p_2$ sau khi nén (đơn vị $10^5\\ \\text{Pa}$)?", 3.0, "×10⁵ Pa", 0.05,
       loi=r"Nhân $p_1$ với $V_2$ thay vì chia (p tỉ lệ nghịch với V), hoặc nghĩ thể tích giảm thì áp suất cũng giảm.",
       ke=[(r"Dùng $p_1V_1=p_2V_2$ vì nhiệt độ không đổi", True),
           (r"Dùng $\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}$", r"Hệ thức đó (Charles) dành cho áp suất không đổi ; ở đây áp suất đổi còn nhiệt độ không đổi."),
           (r"Dùng $\dfrac{p_1}{V_1}=\dfrac{p_2}{V_2}$", r"Đó là $p$ tỉ lệ thuận với $V$ ; thực tế $V$ giảm thì $p$ tăng, nên tích $pV$ mới không đổi.")]),
  buoc("Thể tích ở áp suất cao hơn", "Thể tích khí $V_3$ khi áp suất đạt $4{,}8\\cdot10^5\\ \\text{Pa}$ ($\\text{cm}^3$)?", 50, "cm³", 1,
       loi=r"Đảo tỉ số thành $\dfrac{p_3}{p_1}$ (ra thể tích lớn hơn $V_1$) ; áp suất tăng thì thể tích phải nhỏ đi.",
       ke=[(r"$V_3=\dfrac{p_1V_1}{p_3}$ (từ $p_1V_1=p_3V_3$)", True),
           (r"$V_3=\dfrac{p_3V_1}{p_1}$", r"Nhân thay vì chia ; $p$ tăng thì $V$ phải giảm."),
           (r"$V_3=V_1-(p_3-p_1)$", r"Hai đại lượng khác đơn vị không trừ được ; định luật Boyle nói tích $pV$ không đổi, không phải hiệu.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>áp suất không đổi</b> và nhiệt độ theo <b>°C</b> → đổi sang <b>kenvin</b> rồi dùng <b>V₁/T₁ = V₂/T₂</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi nhiệt độ ra kenvin", "Nhiệt độ $T_2$ ứng với $75\\ ^\\circ\\text{C}$ là bao nhiêu kenvin?", 348, "K", 0.5,
       loi=r"Quên đổi và lấy luôn $75$ hoặc cộng nhầm $273$ thành $27$."),
  buoc("Thể tích sau khi nung", "Thể tích khí $V_2$ ở $75\\ ^\\circ\\text{C}$ ($\\text{cm}^3$)?", 540, "cm³", 1,
       loi=r"Lập tỉ số bằng nhiệt độ Celsius ($\dfrac{75}{17}$) nên ra thể tích lớn gấp hơn $4$ lần — vô lí.",
       ke=[(r"$V_2=V_1\dfrac{T_2}{T_1}$ với $T$ đo bằng kenvin", True),
           (r"$V_2=V_1\dfrac{t_2}{t_1}$ với $t$ đo bằng $^\circ\text{C}$", r"Tỉ lệ thuận chỉ đúng với nhiệt độ tuyệt đối ; nhiệt độ Celsius có gốc $0$ ở nước đá tan."),
           (r"$V_2=V_1\dfrac{T_1}{T_2}$", r"Đảo tỉ số ; nung nóng thì thể tích phải tăng, không giảm.")]),
  buoc("Thể tích tăng thêm", "Thể tích khí tăng thêm $\\Delta V$ ($\\text{cm}^3$)?", 90, "cm³", 1,
       loi=r"Lấy $V_2$ hoặc tỉ số $\dfrac{V_2}{V_1}$ làm phần tăng thêm, thay vì hiệu hai thể tích.",
       ke=[(r"$\Delta V=V_2-V_1$", True),
           (r"$\Delta V=V_2+V_1$", r"Phần tăng thêm là hiệu hai thể tích, không phải tổng."),
           (r"$\Delta V=t_2-t_1$ (hiệu nhiệt độ Celsius)", r"Hiệu nhiệt độ là độ, khác đơn vị với thể tích ; phải tính từ hai thể tích.")]),
  buoc("Nhiệt độ khi làm lạnh", "Nhiệt độ $T_3$ của khí khi $V_3=360\\ \\text{cm}^3$ (kenvin)?", 232, "K", 0.5,
       loi=r"Lật ngược tỉ số thành $\dfrac{V_1}{V_3}$ (ra nhiệt độ cao hơn ban đầu) hoặc lập tỉ số bằng độ C.",
       ke=[(r"$T_3=T_1\dfrac{V_3}{V_1}$ (thể tích tỉ lệ thuận với $T$)", True),
           (r"$T_3=T_1\dfrac{V_1}{V_3}$", r"Làm lạnh thì thể tích giảm nên $T_3$ phải nhỏ hơn $T_1$ ; tỉ số ngược sẽ cho $T_3$ lớn hơn."),
           (r"$t_3=t_1\dfrac{V_3}{V_1}$", r"Tỉ lệ thuận chỉ đúng với nhiệt độ tuyệt đối, không dùng $^\circ\text{C}$.")]),
  buoc("Đổi về độ C", "Nhiệt độ $t_3$ theo $^\\circ\\text{C}$?", -41, "°C", 0.5,
       loi=r"Cộng $273$ thay vì trừ, hoặc trả lời bằng kenvin dù đề hỏi theo $^\circ\text{C}$.",
       ke=[(r"$t=T-273$", True),
           (r"$t=T+273$", r"Đó là công thức đổi từ $^\circ\text{C}$ sang kenvin ; ở đây đổi ngược lại."),
           (r"Giữ nguyên số kenvin vì đề hỏi 'nhiệt độ'", r"Đề hỏi theo $^\circ\text{C}$ nên phải đổi lại bằng $t=T-273$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>đường thẳng qua O trên V–T</b> → đẳng áp ; hai điểm <b>cùng T</b> → so <b>p</b> bằng <b>pV không đổi</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhận dạng đường trên đồ thị", "Mỗi đường (1), (2) mô tả quá trình nào?",
       loi=r"Chỉ nhìn 'đường thẳng' mà không đọc tên hai trục ; nhầm với quá trình giữ nhiệt độ hay giữ thể tích.",
       lua_chon=[(r"Đẳng áp: $V$ tăng tỉ lệ với $T$, đường thẳng kéo dài qua $O$", True),
                 (r"Đẳng nhiệt: nhiệt độ giữ không đổi", r"Dọc theo mỗi đường, $T$ ở trục hoành thay đổi ; nhiệt độ không giữ nguyên."),
                 (r"Đẳng tích: thể tích giữ không đổi", r"Dọc theo mỗi đường, $V$ ở trục tung tăng theo $T$ ; thể tích không giữ nguyên.")]),
  buoc("So sánh áp suất hai đường", "Đường nào ứng với áp suất lớn hơn?",
       loi=r"Cho rằng đường nằm cao hơn thì áp suất lớn hơn. Thực tế ở cùng nhiệt độ, thể tích lớn hơn ứng với áp suất nhỏ hơn.",
       lua_chon=[(r"Đường (1): cùng nhiệt độ mà thể tích nhỏ hơn nên bị nén nhiều hơn", True),
                 (r"Đường (2): đường nằm cao hơn thì áp suất lớn hơn", r"Cùng nhiệt độ, thể tích lớn hơn ứng với áp suất nhỏ hơn (Boyle). Quy tắc: áp suất càng nhỏ, đường càng cao."),
                 (r"Hai đường cùng áp suất vì cùng một lượng khí", r"Cùng lượng khí nhưng hai đường là hai quá trình đẳng áp ở hai áp suất khác nhau ; nếu cùng áp suất thì $A$ và $B$ phải trùng nhau."),],
       ke=[(r"Lấy hai điểm cùng nhiệt độ rồi so thể tích", True),
           (r"So độ cao hai điểm cuối của đường", r"Độ cao cuối đường phụ thuộc cả nhiệt độ lẫn áp suất ; phải so tại cùng một nhiệt độ."),
           (r"Tính $\dfrac{V}{T}$ rồi coi lớn hơn thì áp suất lớn hơn", r"Giá trị $\dfrac{V}{T}$ lớn hơn ứng với áp suất nhỏ hơn.")]),
  buoc("Tỉ số áp suất", "Tỉ số $\\dfrac{p_1}{p_2}$ bằng bao nhiêu?", 1.5, "", 0.02,
       loi=r"Lật ngược tỉ số thành $\dfrac{V_A}{V_B}$, hoặc dùng Charles cho hai điểm không cùng đường.",
       ke=[(r"$A$ và $B$ cùng $T=300\ \text{K}$ nên dùng $pV$ không đổi", True),
           (r"Dùng $\dfrac{V_A}{T_A}=\dfrac{V_B}{T_B}$ cho hai điểm", r"Charles chỉ dùng cho hai điểm cùng một đường (cùng áp suất) ; $A$ và $B$ nằm trên hai đường khác nhau."),
           (r"Coi $p$ tỉ lệ thuận với $V$ : $\dfrac{p_1}{p_2}=\dfrac{V_A}{V_B}$", r"Cùng nhiệt độ thì $p$ tỉ lệ nghịch với $V$ ; tỉ số bị lật ngược.")]),
  buoc("Thể tích khi nung đến 450 K", "Thể tích khí trên đường (2) tại $T=450\\ \\text{K}$ (lít)?", 9, "lít", 0.1,
       loi=r"Cộng thêm số kenvin tăng vào thể tích ($6+150$) thay vì lập tỉ lệ ; hoặc đọc nhầm sang đường (1).",
       ke=[(r"Cùng đường (2) nên dùng $\dfrac{V}{T}$ không đổi", True),
           (r"Cộng: $V=V_B+(450-300)$", r"Thể tích tỉ lệ thuận với $T$, không tăng cộng theo từng kenvin."),
           (r"Dùng đường (1) vì có sẵn số liệu", r"Điểm cần tìm nằm trên đường (2) nên phải dùng số liệu điểm $B$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>hai giai đoạn liên tiếp</b> → tách ra: <b>giữ T → Boyle</b>, <b>giữ p → Charles</b>, nối bằng thể tích cuối.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Nhận dạng hai giai đoạn", "Hai giai đoạn lần lượt là quá trình nào?",
       loi=r"Gộp cả hai giai đoạn vào một định luật hoặc đảo thứ tự hai định luật.",
       lua_chon=[(r"Đẳng nhiệt rồi đẳng áp", True),
                 (r"Đẳng áp rồi đẳng nhiệt", r"Giai đoạn 1 giữ nhiệt độ còn áp suất tăng, nên là đẳng nhiệt ; giai đoạn 2 mới giữ áp suất."),
                 (r"Cả hai đều đẳng nhiệt", r"Giai đoạn 2 có nung nóng, nhiệt độ thay đổi nên không còn là đẳng nhiệt.")]),
  buoc("Thể tích sau giai đoạn 1", "Thể tích khí $V_2$ sau giai đoạn 1 (lít)?", 1.2, "lít", 0.02,
       loi=r"Nhân $V_1$ với $\dfrac{p_2}{p_1}$ (ra thể tích tăng) ; nén thì thể tích phải giảm.",
       ke=[(r"Giai đoạn 1 giữ $T$ nên dùng $p_1V_1=p_2V_2$", True),
           (r"Dùng $\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}$", r"Giai đoạn 1 áp suất thay đổi nên không dùng Charles."),
           (r"Dùng $V_2=V_1\dfrac{p_2}{p_1}$", r"Nhân thay vì chia ; áp suất tăng thì thể tích phải giảm.")]),
  buoc("Nhiệt độ cuối", "Nhiệt độ cuối $T_3$ của khí (kenvin)?", 400, "K", 0.5,
       loi=r"Giữ nguyên $127$ hoặc lấy $T_3=127-273$ vì nhầm chiều đổi đơn vị.",
       ke=[(r"Đổi $t_3=127\ ^\circ\text{C}$ ra kenvin bằng $T=t+273$", True),
           (r"Giữ $127$ vì Charles dùng được nhiệt độ Celsius", r"Hệ thức tỉ lệ thuận chỉ đúng với nhiệt độ tuyệt đối."),
           (r"$T_3=127-273$", r"Công thức đổi sang kenvin là cộng $273$, không phải trừ.")]),
  buoc("Thể tích sau giai đoạn 2", "Thể tích khí $V_3$ sau giai đoạn 2 (lít)?", 1.6, "lít", 0.02,
       loi=r"Dùng Charles từ thể tích ban đầu $3{,}0$ lít (bỏ qua giai đoạn nén) nên ra thể tích lớn hơn ban đầu.",
       ke=[(r"Charles xuất phát từ $V_2$ và $T_2=300\ \text{K}$", True),
           (r"Charles xuất phát từ thể tích ban đầu $V_1$", r"Áp suất đã đổi ở giai đoạn 1 nên thể tích gốc của giai đoạn 2 phải là thể tích cuối của giai đoạn 1."),
           (r"Dùng Boyle lần nữa", r"Giai đoạn 2 giữ áp suất chứ không giữ nhiệt độ.")]),
  buoc("Độ giảm thể tích", "Thể tích khí cuối cùng giảm bao nhiêu lít so với lúc đầu?", 1.4, "lít", 0.02,
       loi=r"Lấy $V_1-V_2$ (chỉ giảm sau giai đoạn 1) hoặc lấy $V_3-V_1$ (ra số âm).",
       ke=[(r"$\Delta V=V_1-V_3$", True),
           (r"$\Delta V=V_1-V_2$", r"Đó là độ giảm sau giai đoạn 1 ; nung nóng ở giai đoạn 2 làm thể tích tăng trở lại."),
           (r"$\Delta V=V_2-V_3$", r"Đó là số âm, bằng trừ đi phần thể tích tăng ở giai đoạn 2, và không so với lúc đầu.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>cột thuỷ ngân giam khí</b> → áp suất khí <b>p₀ ± h</b> (lên: cộng, xuống: trừ), rồi <b>p₁l₁ = p₂l₂</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Áp suất khí khi miệng hướng lên", "Áp suất $p_1$ của khí bị giam khi miệng ống hướng lên (mmHg)?", 960, "mmHg", 5,
       loi=r"Quên đổi $h=20\ \text{cm}$ ra mm nên cộng $760+20$ ; hoặc trừ thay vì cộng vì nhầm với miệng hướng xuống."),
  buoc("Áp suất khí sau khi lật", "Áp suất $p_2$ của khí bị giam sau khi lật ống (mmHg)?", 560, "mmHg", 5,
       loi=r"Vẫn cộng $p_0+h$ vì nghĩ cột Hg 'luôn đè lên khí' ; sau khi lật, Hg nằm dưới khí nên áp suất khí nhỏ hơn $p_0$.",
       ke=[(r"Khí cùng cột Hg cân bằng với $p_0$ đẩy lên nên $p_2=p_0-h$", True),
           (r"$p_2=p_0+h$ vì cột Hg vẫn nặng như trước", r"Khi miệng hướng xuống, Hg kéo xuống chứ không đè lên khí ; khí phải có áp suất nhỏ hơn $p_0$."),
           (r"$p_2=p_1$ vì lượng khí không đổi", r"Lượng khí không đổi nhưng áp suất khí phụ thuộc cách đặt ống ; $p_2$ khác $p_1$.")]),
  buoc("Chiều dài cột khí sau khi lật", "Chiều dài cột khí $l_2$ sau khi lật (cm)?", 48, "cm", 1,
       loi=r"Dùng $p_0$ thay cho $p_1$ làm áp suất đầu (ra kết quả sai) hoặc dùng Charles dù nhiệt độ không đổi.",
       ke=[(r"Nhiệt độ không đổi, tiết diện đều: $p_1l_1=p_2l_2$", True),
           (r"Dùng $p_0\,l_1=p_2\,l_2$", r"Áp suất ban đầu của khí là $p_1=p_0+h$, không phải $p_0$."),
           (r"Dùng $\dfrac{l_1}{T_1}=\dfrac{l_2}{T_2}$", r"Nhiệt độ không đổi nên không dùng Charles ; áp suất mới là thông số thay đổi.")]),
  buoc("Kiểm tra")]),
]

write(J, 7, "Bài 6. Định luật Boyle. Định luật Charles", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
