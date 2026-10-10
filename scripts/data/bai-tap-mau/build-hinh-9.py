"""Bài tập mẫu Bài 8 "Áp suất - động năng của phân tử khí" (Vật lí 12) — lesson_id 9. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/9.quet-dang.json). Hình: hinh_9.py. DB chưa có mục bai_tap_mau cho bài này nên không có ví dụ cũ / tự luận.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-9.py   (idempotent, ghi 9.json với review.checked=false)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_9 import *

J = os.path.join(HERE, "9.json")
T211 = "Liên hệ áp suất với động năng phân tử"
T212 = "Động năng trung bình phân tử và nhiệt độ"

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Động năng tịnh tiến trung bình ở một nhiệt độ",
      topic=T212,
      problem_html=r"""<p>Trong một phòng sấy, khí hydrogen ($\text{H}_2$) và khí oxygen ($\text{O}_2$) trộn lẫn trong một bình kín, cùng ở $47\ ^\circ\text{C}$. Lấy $k=1{,}38\cdot10^{-23}\ \text{J/K}$.</p><ol type="a"><li>Tính động năng tịnh tiến trung bình của một phân tử hydrogen.</li><li>Động năng tịnh tiến trung bình của một phân tử oxygen lớn hơn, nhỏ hơn hay bằng của phân tử hydrogen? Giải thích.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Nhiệt độ đổi thì động năng, tốc độ, áp suất đổi mấy lần",
      topic=T212,
      problem_html=r"""<p>Khí heli trong một bình kín (thể tích và lượng khí không đổi) được hơ nóng từ $27\ ^\circ\text{C}$ lên $147\ ^\circ\text{C}$. Coi heli là khí lí tưởng.</p><ol type="a"><li>Động năng tịnh tiến trung bình của phân tử tăng bao nhiêu lần?</li><li>Tốc độ căn quân phương của phân tử tăng bao nhiêu lần?</li><li>Áp suất khí tăng bao nhiêu lần?</li></ol><p>Làm tròn các tỉ số đến hai chữ số thập phân.</p>"""),
 dict(label="Dạng 3 · Trung bình · Áp suất từ khối lượng riêng và tốc độ căn quân phương",
      topic=T211,
      problem_html=r"""<p>Một bình kín chứa khí neon (coi là khí lí tưởng) có khối lượng riêng $0{,}90\ \text{kg/m}^3$. Căn bậc hai của trung bình bình phương tốc độ của các phân tử là $600\ \text{m/s}$.</p><ol type="a"><li>Tính áp suất khí trong bình.</li><li>Nung nóng khí trong bình (thể tích và lượng khí không đổi) đến khi căn bậc hai của trung bình bình phương tốc độ là $900\ \text{m/s}$. Tính áp suất khí khi đó.</li></ol>"""),
 dict(label="Dạng 4 · Khá · Tốc độ căn quân phương từ nhiệt độ và khối lượng mol",
      topic=T212,
      problem_html=r"""<p>Một bình kín chứa khí argon ($M=40\ \text{g/mol}$) ở $77\ ^\circ\text{C}$. Lấy $N_A=6{,}02\cdot10^{23}\ \text{mol}^{-1}$ và $k=1{,}38\cdot10^{-23}\ \text{J/K}$.</p><ol type="a"><li>Tính khối lượng của một phân tử argon.</li><li>Tính động năng tịnh tiến trung bình và tốc độ căn quân phương của phân tử argon.</li><li>Thay argon bằng heli ($M=4\ \text{g/mol}$) ở cùng nhiệt độ. Tốc độ căn quân phương của phân tử heli lớn gấp bao nhiêu lần của phân tử argon?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Bài ngược: từ áp suất và mật độ tìm nhiệt độ, rồi đổi trạng thái",
      topic=T211,
      problem_html=r"""<p>Một bình kín chứa khí heli (coi là khí lí tưởng) có mật độ phân tử $2{,}4\cdot10^{25}\ \text{m}^{-3}$ và áp suất $1{,}0\cdot10^{5}\ \text{Pa}$. Lấy $k=1{,}38\cdot10^{-23}\ \text{J/K}$.</p><ol type="a"><li>Tính động năng tịnh tiến trung bình của một phân tử heli.</li><li>Tính nhiệt độ tuyệt đối của khí.</li><li>Hút bớt khí qua van để số phân tử trong bình còn một nửa, rồi nung đến $117\ ^\circ\text{C}$ (bình vẫn là bình đó). Tính áp suất khí lúc này.</li></ol>"""),
]

BUILD = [d1, d2, d3, d4, d5]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
CT = "Đại lượng cần tìm"
ANALYSIS = [
 [("\"khí hydrogen và khí oxygen trộn lẫn trong một bình kín\"", "hai khí khác nhau, cùng một bình", "Khí lí tưởng: phân tử rất nhỏ, chuyển động hỗn loạn"),
  ("\"cùng ở $47\\ ^\\circ\\text{C}$\"", "$t=47\\ ^\\circ\\text{C}$ cho cả hai khí", "⚠ Nhiệt độ dùng trong hệ thức của bài là nhiệt độ tuyệt đối (Kelvin), không dùng Celsius"),
  ("\"$k=1{,}38\\cdot10^{-23}\\ \\text{J/K}$\"", "$k$", "Hằng số Boltzmann"),
  ("\"a) động năng tịnh tiến trung bình của một phân tử hydrogen\"", "Cần $\\overline{E_d}$ của $\\text{H}_2$", CT),
  ("\"b) … oxygen lớn hơn, nhỏ hơn hay bằng … hydrogen\"", "So sánh $\\overline{E_d}$ của $\\text{O}_2$ với $\\text{H}_2$", "Cần xét $\\overline{E_d}$ phụ thuộc vào những đại lượng nào")],
 [("\"khí heli trong một bình kín (thể tích và lượng khí không đổi)\"", "$V$ và số phân tử $N$ giữ nguyên", "⚠ Bình kín: thể tích $V$ và số phân tử $N$ giữ nguyên"),
  ("\"hơ nóng từ $27\\ ^\\circ\\text{C}$ lên $147\\ ^\\circ\\text{C}$\"", "$t_1=27\\ ^\\circ\\text{C}$; $t_2=147\\ ^\\circ\\text{C}$", "⚠ Mọi tỉ số về nhiệt độ phải lấy với nhiệt độ tuyệt đối (Kelvin)"),
  ("\"a) động năng tịnh tiến trung bình … tăng bao nhiêu lần\"", "Cần $\\overline{E_d}'/\\overline{E_d}$", CT),
  ("\"b) tốc độ căn quân phương … tăng bao nhiêu lần\"", "Cần $v_{rms}'/v_{rms}$", CT),
  ("\"c) áp suất khí tăng bao nhiêu lần\"", "Cần $p'/p$", CT)],
 [("\"bình kín chứa khí neon (coi là khí lí tưởng)\"", "khí lí tưởng", "⚠ Mô hình khí lí tưởng: phân tử bỏ qua kích thước, va chạm đàn hồi với thành bình"),
  ("\"khối lượng riêng $0{,}90\\ \\text{kg/m}^3$\"", "$\\rho=0{,}90\\ \\text{kg/m}^3$", "Khối lượng riêng $\\rho=\\mu m$"),
  ("\"căn bậc hai của trung bình bình phương tốc độ … $600\\ \\text{m/s}$\"", "$\\sqrt{\\overline{v^2}}=600\\ \\text{m/s}$", "Tốc độ căn quân phương $v_{rms}=\\sqrt{\\overline{v^2}}$"),
  ("\"a) áp suất khí trong bình\"", "Cần $p$", CT),
  ("\"Nung nóng … (thể tích và lượng khí không đổi) … $900\\ \\text{m/s}$\"", "$\\sqrt{\\overline{v^2}}'=900\\ \\text{m/s}$; $V$, lượng khí giữ nguyên", "⚠ Thể tích và lượng khí trong bình giữ nguyên"),
  ("\"Tính áp suất khí khi đó\"", "Cần $p'$", CT)],
 [("\"khí argon ($M=40\\ \\text{g/mol}$) ở $77\\ ^\\circ\\text{C}$\"", "$M=40\\ \\text{g/mol}$; $t=77\\ ^\\circ\\text{C}$", "⚠ $T$ phải là Kelvin; $M$ phải ở kg/mol thì khối lượng phân tử mới ra kg"),
  ("\"$N_A=6{,}02\\cdot10^{23}\\ \\text{mol}^{-1}$ và $k=1{,}38\\cdot10^{-23}\\ \\text{J/K}$\"", "$N_A$; $k$", "Số Avogadro; hằng số Boltzmann"),
  ("\"a) khối lượng của một phân tử argon\"", "Cần $m$", CT),
  ("\"b) động năng tịnh tiến trung bình và tốc độ căn quân phương\"", "Cần $\\overline{E_d}$ và $v_{rms}$", CT),
  ("\"c) heli ($M=4\\ \\text{g/mol}$) ở cùng nhiệt độ\"", "$M_{He}=4\\ \\text{g/mol}$; cùng $T$", "⚠ Cùng nhiệt độ: hai khí chỉ khác nhau ở khối lượng phân tử"),
  ("\"lớn gấp bao nhiêu lần\"", "Cần $v_{He}/v_{Ar}$", CT)],
 [("\"khí heli (coi là khí lí tưởng) có mật độ phân tử $2{,}4\\cdot10^{25}\\ \\text{m}^{-3}$\"", "$\\mu=2{,}4\\cdot10^{25}\\ \\text{m}^{-3}$", "Mật độ phân tử $\\mu=N/V$ (số phân tử trong $1\\ \\text{m}^3$)"),
  ("\"áp suất $1{,}0\\cdot10^{5}\\ \\text{Pa}$\"", "$p=1{,}0\\cdot10^{5}\\ \\text{Pa}$", "⚠ Đề không cho nhiệt độ nên chưa thế ngay vào hệ thức có $T$"),
  ("\"a) động năng tịnh tiến trung bình\"", "Cần $\\overline{E_d}$", CT),
  ("\"b) nhiệt độ tuyệt đối\"", "Cần $T$", CT),
  ("\"hút bớt khí … số phân tử còn một nửa (bình vẫn là bình đó)\"", "$N'=N/2$; $V$ không đổi", "⚠ Bình cố định nên $V$ không đổi, chỉ $N$ đổi"),
  ("\"nung đến $117\\ ^\\circ\\text{C}$\"", "$t'=117\\ ^\\circ\\text{C}$", "Nhiệt độ phải đổi sang Kelvin"),
  ("\"c) áp suất khí lúc này\"", "Cần $p'$", CT)],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> động năng tịnh tiến trung bình $\overline{E_d}=\dfrac{m\overline{v^2}}{2}$ của một phân tử; nhiệt độ tuyệt đối $T$ (K).",
       r"<strong>Định luật:</strong> $\overline{E_d}$ tỉ lệ thuận với nhiệt độ tuyệt đối và chỉ phụ thuộc $T$.",
       r"<strong>Công thức:</strong> $\overline{E_d}=\dfrac{3}{2}kT$, với $k=1{,}38\cdot10^{-23}\ \text{J/K}$ và $T=t+273$.",
       r"⚠ <strong>Điều kiện:</strong> $T$ phải là Kelvin; khí lí tưởng ở trạng thái cân bằng nhiệt."]
RC2 = [r"<strong>Khái niệm:</strong> $\overline{E_d}=\dfrac{m\overline{v^2}}{2}$; tốc độ căn quân phương $v_{rms}=\sqrt{\overline{v^2}}$; mật độ phân tử $\mu=\dfrac{N}{V}$.",
       r"<strong>Định luật:</strong> $\overline{E_d}$ tỉ lệ thuận với $T$; áp suất do va chạm của phân tử với thành bình.",
       r"<strong>Công thức:</strong> $\overline{E_d}=\dfrac{3}{2}kT$ · $p=\dfrac{2}{3}\mu\overline{E_d}$.",
       r"⚠ <strong>Điều kiện:</strong> tỉ số chỉ lấy với $T$ (Kelvin); cùng một khí nên $m$ không đổi."]
RC3 = [r"<strong>Khái niệm:</strong> khối lượng riêng $\rho=\mu m$; $\overline{v^2}$ là trung bình của bình phương tốc độ; $v_{rms}=\sqrt{\overline{v^2}}$.",
       r"<strong>Định luật:</strong> chỉ một trong ba phương bình đẳng vuông góc với thành bình nên xuất hiện hệ số $\dfrac{1}{3}$.",
       r"<strong>Công thức:</strong> $p=\dfrac{1}{3}\rho\overline{v^2}$.",
       r"⚠ <strong>Điều kiện:</strong> dùng $\overline{v^2}$ (đã bình phương), không dùng thẳng $v_{rms}$; $\rho$ tính bằng kg/m³ thì $p$ ra Pa."]
RC4 = [r"<strong>Khái niệm:</strong> $M$ (kg/mol) là khối lượng một mol; khối lượng một phân tử $m=\dfrac{M}{N_A}$.",
       r"<strong>Định luật:</strong> $\overline{E_d}=\dfrac{m\overline{v^2}}{2}=\dfrac{3}{2}kT$; cùng $T$ thì mọi khí cùng $\overline{E_d}$.",
       r"<strong>Công thức:</strong> $v_{rms}=\sqrt{\overline{v^2}}=\sqrt{\dfrac{2\overline{E_d}}{m}}=\sqrt{\dfrac{3kT}{m}}$.",
       r"⚠ <strong>Điều kiện:</strong> $T$ phải là Kelvin; $M$ đổi ra kg/mol thì $m$ mới ra kg."]
RC5 = [r"<strong>Khái niệm:</strong> mật độ phân tử $\mu=\dfrac{N}{V}$; động năng tịnh tiến trung bình $\overline{E_d}$.",
       r"<strong>Định luật:</strong> áp suất do va chạm: $p=\dfrac{2}{3}\mu\overline{E_d}$; $\overline{E_d}$ tỉ lệ thuận với $T$.",
       r"<strong>Công thức:</strong> $p=\dfrac{2}{3}\mu\overline{E_d}$ · $\overline{E_d}=\dfrac{3}{2}kT$ · $p=\mu kT$.",
       r"⚠ <strong>Điều kiện:</strong> đề không cho $T$ thì đi từ $p$ và $\mu$ tìm $\overline{E_d}$ trước; $T$ luôn tính bằng Kelvin."]

SOLS = [
 sol(RC1, [
  ("Đổi nhiệt độ sang Kelvin", [M(r"T=47+273"), A(r"T=320\ \text{K}")]),
  ("Động năng của phân tử hydrogen (câu a)", [P("Chỉ phụ thuộc nhiệt độ, chưa cần khối lượng phân tử:"), M(r"\overline{E_d}=\dfrac{3}{2}kT"),
        M(r"\overline{E_d}=1{,}5\cdot1{,}38\cdot10^{-23}\cdot320"), A(r"\overline{E_d}\approx6{,}62\cdot10^{-21}\ \text{J}")]),
  ("So sánh với phân tử oxygen (câu b)", [P("Hai khí trong cùng bình nên cùng $T=320$ K, và công thức không chứa khối lượng phân tử:"),
        M(r"\overline{E_d}(\text{O}_2)=\dfrac{3}{2}kT=\overline{E_d}(\text{H}_2)"),
        A(r"T:<strong>Bằng nhau.</strong> Phân tử $\text{O}_2$ nặng hơn nên bay chậm hơn, nhưng tích $m\overline{v^2}$ vẫn như nhau.")]),
  ("Kiểm tra", [P(r"Đơn vị: J/K × K = J; cỡ $10^{-21}$ J, hợp lí cho một phân tử ở nhiệt độ phòng sấy."),
        P(r"Nếu thế thẳng $t=47$ thay cho $T=320$ K thì ra $\overline{E_d}\approx9{,}7\cdot10^{-22}$ J, nhỏ hơn giá trị đúng khoảng $6{,}8$ lần: vô lí.")])],
  [r"a) $\overline{E_d}\approx6{,}62\cdot10^{-21}\ \text{J}$", "b) Bằng nhau (cùng nhiệt độ)"],
  r"Nhận dạng: đề cho <strong>nhiệt độ của khí</strong> và hỏi <strong>động năng tịnh tiến trung bình</strong> → dùng $\dfrac{3}{2}kT$, đổi sang Kelvin trước."),
 sol(RC2, [
  ("Đổi nhiệt độ sang Kelvin", [M(r"T_1=27+273=300\ \text{K}"), M(r"T_2=147+273"), A(r"T_2=420\ \text{K}")]),
  ("Tỉ số động năng (câu a)", [P("Cùng hằng số $k$:"), M(r"\dfrac{\overline{E_d}'}{\overline{E_d}}=\dfrac{\frac{3}{2}kT_2}{\frac{3}{2}kT_1}=\dfrac{T_2}{T_1}"),
        M(r"\dfrac{T_2}{T_1}=\dfrac{420}{300}"), A(r"\dfrac{\overline{E_d}'}{\overline{E_d}}=1{,}40")]),
  ("Tỉ số tốc độ căn quân phương (câu b)", [P(r"Cùng một khí nên $m$ không đổi; từ $\overline{E_d}=\dfrac{1}{2}m\overline{v^2}$ thì $\overline{v^2}$ tăng đúng bằng số lần $\overline{E_d}$ tăng:"),
        M(r"\dfrac{v_{rms}'}{v_{rms}}=\sqrt{\dfrac{\overline{v^2}'}{\overline{v^2}}}=\sqrt{\dfrac{T_2}{T_1}}=\sqrt{1{,}4}"), A(r"\dfrac{v_{rms}'}{v_{rms}}\approx1{,}18")]),
  ("Tỉ số áp suất (câu c)", [P(r"$V$ và $N$ không đổi nên $\mu$ không đổi; thế $\overline{E_d}=\dfrac{3}{2}kT$ vào $p=\dfrac{2}{3}\mu\overline{E_d}$ được $p=\mu kT$:"),
        M(r"\dfrac{p'}{p}=\dfrac{\mu kT_2}{\mu kT_1}=\dfrac{T_2}{T_1}"), A(r"\dfrac{p'}{p}=1{,}40")]),
  ("Kiểm tra", [P(r"Nếu lấy tỉ số Celsius $\dfrac{147}{27}\approx5{,}4$ thì áp suất tăng hơn $5$ lần: vô lí khi nhiệt độ chỉ từ $300$ K lên $420$ K."),
        P(r"Tốc độ tăng ít hơn động năng vì $v_{rms}\propto\sqrt{T}$; bình phương lại: $1{,}18^2\approx1{,}4$, khớp tỉ số động năng.")])],
  ["a) $\\overline{E_d}$ tăng $1{,}40$ lần", "b) $v_{rms}$ tăng khoảng $1{,}18$ lần", "c) $p$ tăng $1{,}40$ lần"],
  r"Nhận dạng: đề hỏi <strong>tăng bao nhiêu lần</strong> khi <strong>nhiệt độ đổi</strong> → lấy tỉ số $T_2/T_1$ (Kelvin); $\overline{E_d}$ và $p$ theo $T$, $v_{rms}$ theo $\sqrt{T}$."),
 sol(RC3, [
  ("Trung bình bình phương tốc độ", [P("Đề cho căn bậc hai của $\\overline{v^2}$ nên phải bình phương:"), M(r"\overline{v^2}=\left(\sqrt{\overline{v^2}}\right)^2=600^2"), A(r"\overline{v^2}=3{,}6\cdot10^{5}\ \text{m}^2/\text{s}^2")]),
  ("Áp suất ban đầu (câu a)", [M(r"p=\dfrac{1}{3}\rho\overline{v^2}"), M(r"p=\dfrac{1}{3}\cdot0{,}90\cdot3{,}6\cdot10^{5}"), A(r"p=1{,}08\cdot10^{5}\ \text{Pa}")]),
  ("Áp suất sau khi nung nóng (câu b)", [P(r"$V$ và lượng khí không đổi nên $\rho=0{,}90\ \text{kg/m}^3$ giữ nguyên, chỉ $\overline{v^2}$ đổi:"), M(r"\overline{v^2}'=900^2=8{,}1\cdot10^{5}\ \text{m}^2/\text{s}^2"),
        M(r"p'=\dfrac{1}{3}\cdot0{,}90\cdot8{,}1\cdot10^{5}"), A(r"p'=2{,}43\cdot10^{5}\ \text{Pa}")]),
  ("Kiểm tra", [P(r"Đơn vị: kg/m³ × m²/s² = Pa. Áp suất ban đầu khoảng $1{,}07$ atm, cỡ khí quyển: hợp lí."),
        P(r"$p$ tỉ lệ với $\overline{v^2}$ nên $\dfrac{p'}{p}=\left(\dfrac{900}{600}\right)^2=2{,}25$, khớp $\dfrac{2{,}43}{1{,}08}$.")])],
  [r"a) $p=1{,}08\cdot10^{5}\ \text{Pa}$", r"b) $p'=2{,}43\cdot10^{5}\ \text{Pa}$"],
  r"Nhận dạng: đề cho <strong>khối lượng riêng</strong> và <strong>căn bậc hai của trung bình bình phương tốc độ</strong> → $p=\dfrac{1}{3}\rho\overline{v^2}$, nhớ bình phương tốc độ."),
 sol(RC4, [
  ("Đổi nhiệt độ sang Kelvin", [M(r"T=77+273"), A(r"T=350\ \text{K}")]),
  ("Khối lượng một phân tử (câu a)", [P(r"Đổi $M=40\ \text{g/mol}=0{,}040\ \text{kg/mol}$:"), M(r"m=\dfrac{M}{N_A}=\dfrac{0{,}040}{6{,}02\cdot10^{23}}"), A(r"m\approx6{,}64\cdot10^{-26}\ \text{kg}")]),
  ("Động năng tịnh tiến trung bình (câu b)", [M(r"\overline{E_d}=\dfrac{3}{2}kT=1{,}5\cdot1{,}38\cdot10^{-23}\cdot350"), A(r"\overline{E_d}\approx7{,}25\cdot10^{-21}\ \text{J}")]),
  ("Tốc độ căn quân phương (câu b)", [P(r"Từ $\overline{E_d}=\dfrac{1}{2}m\overline{v^2}$ suy ra $\overline{v^2}$ rồi lấy căn:"), M(r"\overline{v^2}=\dfrac{2\overline{E_d}}{m}=\dfrac{2\cdot7{,}25\cdot10^{-21}}{6{,}64\cdot10^{-26}}\approx2{,}18\cdot10^{5}\ \text{m}^2/\text{s}^2"),
        M(r"v_{rms}=\sqrt{2{,}18\cdot10^{5}}"), A(r"v_{rms}\approx467\ \text{m/s}")]),
  ("So sánh với heli (câu c)", [P(r"Cùng $T$ nên cùng $\overline{E_d}$, tức $\dfrac{1}{2}m_{Ar}\overline{v^2_{Ar}}=\dfrac{1}{2}m_{He}\overline{v^2_{He}}$:"),
        M(r"\dfrac{v_{He}}{v_{Ar}}=\sqrt{\dfrac{m_{Ar}}{m_{He}}}=\sqrt{\dfrac{M_{Ar}}{M_{He}}}=\sqrt{\dfrac{40}{4}}"), A(r"\dfrac{v_{He}}{v_{Ar}}\approx3{,}16")]),
  ("Kiểm tra", [P("Tính lại bằng công thức một lần:"), M(r"v_{rms}=\sqrt{\dfrac{3kT}{m}}=\sqrt{\dfrac{3\cdot1{,}38\cdot10^{-23}\cdot350}{6{,}64\cdot10^{-26}}}\approx467\ \text{m/s}"),
        P("Hai cách cùng ra. Cỡ vài trăm m/s là hợp lí cho phân tử khí ở nhiệt độ này; khí nhẹ hơn thì nhanh hơn.")])],
  [r"a) $m\approx6{,}64\cdot10^{-26}\ \text{kg}$", r"b) $\overline{E_d}\approx7{,}25\cdot10^{-21}\ \text{J}$ ; $v_{rms}\approx467\ \text{m/s}$", r"c) $v_{He}\approx3{,}16\,v_{Ar}$"],
  r"Nhận dạng: đề cho <strong>khối lượng mol và nhiệt độ</strong>, hỏi <strong>tốc độ căn quân phương</strong> → $m=\dfrac{M}{N_A}$, $\overline{E_d}=\dfrac{3}{2}kT$, rồi $v=\sqrt{2\overline{E_d}/m}$."),
 sol(RC5, [
  ("Chọn hệ thức để tìm động năng", [P("Đề cho $p$ và $\\mu$, chưa cho $T$:"), M(r"p=\dfrac{2}{3}\mu\overline{E_d}"),
        A(r"T:Dùng liên hệ áp suất với động năng. Chưa dùng được $\overline{E_d}=\dfrac{3}{2}kT$ vì chưa biết $T$.")]),
  ("Động năng tịnh tiến trung bình (câu a)", [M(r"\overline{E_d}=\dfrac{3p}{2\mu}=\dfrac{3\cdot1{,}0\cdot10^{5}}{2\cdot2{,}4\cdot10^{25}}"), A(r"\overline{E_d}\approx6{,}25\cdot10^{-21}\ \text{J}")]),
  ("Nhiệt độ tuyệt đối (câu b)", [M(r"\overline{E_d}=\dfrac{3}{2}kT\Rightarrow T=\dfrac{2\overline{E_d}}{3k}"), M(r"T=\dfrac{2\cdot6{,}25\cdot10^{-21}}{3\cdot1{,}38\cdot10^{-23}}"), A(r"T\approx302\ \text{K}")]),
  ("Áp suất sau khi hút bớt và nung nóng (câu c)", [P(r"$V$ không đổi, $N$ còn một nửa nên $\mu'=\dfrac{\mu}{2}=1{,}2\cdot10^{25}\ \text{m}^{-3}$; $T'=117+273=390$ K:"),
        M(r"p'=\mu'kT'=1{,}2\cdot10^{25}\cdot1{,}38\cdot10^{-23}\cdot390"), A(r"p'\approx6{,}46\cdot10^{4}\ \text{Pa}")]),
  ("Kiểm tra", [P("Tính theo tỉ số, không dùng $\\mu'$ trực tiếp:"), M(r"p'=p\cdot\dfrac{\mu'}{\mu}\cdot\dfrac{T'}{T}=1{,}0\cdot10^{5}\cdot0{,}5\cdot\dfrac{390}{302}\approx6{,}46\cdot10^{4}\ \text{Pa}"),
        P(r"Kiểm ngược đề: $\mu kT=2{,}4\cdot10^{25}\cdot1{,}38\cdot10^{-23}\cdot302\approx1{,}0\cdot10^{5}\ \text{Pa}$, khớp áp suất ban đầu.")])],
  [r"a) $\overline{E_d}\approx6{,}25\cdot10^{-21}\ \text{J}$", r"b) $T\approx302\ \text{K}$", r"c) $p'\approx6{,}46\cdot10^{4}\ \text{Pa}$"],
  r"Nhận dạng: đề <strong>không cho nhiệt độ</strong> mà cho <strong>áp suất và mật độ phân tử</strong> → tìm $\overline{E_d}$ từ $p=\dfrac{2}{3}\mu\overline{E_d}$ trước, rồi mới ra $T$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>nhiệt độ của khí</b> và hỏi <b>động năng tịnh tiến trung bình</b> → nghĩ tới <b>3kT/2</b>, đổi Kelvin trước.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi nhiệt độ sang Kelvin", "Nhiệt độ của khí theo Kelvin là bao nhiêu?", 320, "K", 0.5,
       loi=r"Thế thẳng số đo Celsius vào công thức, hoặc cộng nhầm $237$ thay cho $273$."),
  buoc("Động năng của phân tử hydrogen", "Động năng tịnh tiến trung bình của một phân tử hydrogen bằng bao nhiêu (đơn vị $10^{-21}$ J)?", 6.62, "×10⁻²¹ J", 0.03,
       loi=r"Quên hệ số $\dfrac{3}{2}$ (chỉ lấy $kT$), hoặc thế số đo Celsius thay cho nhiệt độ Kelvin.",
       ke=[(r"Thế vào $\overline{E_d}=\dfrac{3}{2}kT$ với $T$ theo Kelvin", True),
           (r"Thế vào $\overline{E_d}=\dfrac{3}{2}kt$ với $t$ theo Celsius", r"Hệ thức tỉ lệ thuận chỉ đúng với nhiệt độ tuyệt đối; Celsius không có gốc $0$ thật."),
           (r"Tìm khối lượng một phân tử hydrogen trước, rồi mới tính $\overline{E_d}$", r"Đề không cho khối lượng mol của hydrogen, và $\overline{E_d}=\dfrac{3}{2}kT$ không chứa khối lượng phân tử.")]),
  buoc("So sánh với phân tử oxygen", "So với phân tử hydrogen, động năng tịnh tiến trung bình của phân tử oxygen như thế nào?",
       loi=r"Cho rằng phân tử nặng hơn thì động năng lớn hơn; hoặc cho rằng bay chậm hơn thì động năng nhỏ hơn. Động năng phụ thuộc cả khối lượng lẫn tốc độ, không chỉ một trong hai.",
       lua_chon=[(r"Bằng nhau, vì hai khí cùng nhiệt độ", True),
                 (r"Lớn hơn, vì phân tử oxygen nặng hơn", r"$\overline{E_d}=\dfrac{3}{2}kT$ chỉ phụ thuộc $T$, không chứa khối lượng phân tử; phân tử nặng hơn thì bay chậm hơn."),
                 (r"Nhỏ hơn, vì phân tử oxygen bay chậm hơn", r"Chỉ nhìn tốc độ là thiếu: động năng còn phụ thuộc khối lượng, và cùng $T$ thì mọi khí có cùng $\overline{E_d}$.")],
       ke=[(r"So $\overline{E_d}$ của hai khí tại cùng một nhiệt độ", True),
           (r"So khối lượng hai phân tử rồi kết luận khí nặng hơn có $\overline{E_d}$ lớn hơn", r"$\overline{E_d}$ không phụ thuộc khối lượng phân tử, nên so khối lượng không cho kết luận về $\overline{E_d}$."),
           (r"Phải biết khối lượng phân tử oxygen mới so sánh được", r"Không cần: $\overline{E_d}=\dfrac{3}{2}kT$ không chứa khối lượng phân tử.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Hỏi <b>tăng bao nhiêu lần</b> khi <b>nhiệt độ đổi</b> → lấy tỉ số hai <b>nhiệt độ Kelvin</b>, rồi xét từng đại lượng.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Đổi nhiệt độ sang Kelvin", "Nhiệt độ sau khi hơ nóng theo Kelvin là bao nhiêu?", 420, "K", 0.5,
       loi=r"Dùng thẳng số đo Celsius để lấy tỉ số, hoặc chỉ đổi một trong hai nhiệt độ."),
  buoc("Tỉ số động năng", "Động năng tịnh tiến trung bình tăng bao nhiêu lần?", 1.4, "lần", 0.01,
       loi=r"Lấy tỉ số hai số đo Celsius; hoặc lật ngược tỉ số nên ra động năng giảm.",
       ke=[(r"$\overline{E_d}\propto T$ nên lấy $\dfrac{T_2}{T_1}$ theo Kelvin", True),
           (r"$\overline{E_d}\propto T$ nên lấy $\dfrac{t_2}{t_1}$ theo Celsius", r"Celsius không có gốc $0$ thật nên tỉ số hai số đo Celsius vô nghĩa."),
           (r"$\overline{E_d}\propto T^2$ nên bình phương tỉ số nhiệt độ", r"$\overline{E_d}=\dfrac{3}{2}kT$ bậc nhất theo $T$, không có bình phương.")]),
  buoc("Tỉ số tốc độ căn quân phương", "Tốc độ căn quân phương tăng bao nhiêu lần?", 1.18, "lần", 0.01,
       loi=r"Cho tốc độ tăng cùng số lần với động năng, quên rằng động năng tỉ lệ với bình phương tốc độ.",
       ke=[(r"$\overline{v^2}$ tăng cùng số lần với $\overline{E_d}$, nên $v_{rms}$ tăng căn bậc hai số lần đó", True),
           (r"$v_{rms}$ tăng cùng số lần với $\overline{E_d}$", r"$\overline{E_d}=\dfrac{1}{2}m\overline{v^2}$ tỉ lệ với bình phương tốc độ chứ không phải tốc độ."),
           (r"$v_{rms}$ tăng bằng bình phương số lần $\overline{E_d}$ tăng", r"Ngược lại: $\overline{v^2}$ mới tăng đúng bằng số lần $\overline{E_d}$ tăng, còn $v_{rms}$ là căn của nó.")]),
  buoc("Tỉ số áp suất", "Áp suất khí tăng bao nhiêu lần?", 1.4, "lần", 0.01,
       loi=r"Cho rằng bình kín thì áp suất không đổi; hoặc coi $p$ tỉ lệ với $v_{rms}$ thay vì với $\overline{E_d}$.",
       ke=[(r"$\mu$ không đổi, $p=\dfrac{2}{3}\mu\overline{E_d}$ tỉ lệ với $\overline{E_d}$ nên tỉ số bằng tỉ số $T$", True),
           (r"Bình kín nên $p$ không đổi", r"Bình kín chỉ giữ nguyên mật độ phân tử; $\overline{E_d}$ tăng nên mỗi va chạm mạnh hơn và dồn dập hơn, $p$ tăng."),
           (r"$p$ tỉ lệ với $v_{rms}$ nên lấy tỉ số tốc độ", r"$p=\dfrac{1}{3}\mu m\overline{v^2}$ tỉ lệ với $\overline{v^2}$, không tỉ lệ với tốc độ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Cho <b>khối lượng riêng</b> và <b>căn quân phương tốc độ</b> → nghĩ tới <b>p = ρ·v̄²/3</b>, nhớ bình phương tốc độ.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Trung bình bình phương tốc độ", "Trung bình bình phương tốc độ $\\overline{v^2}$ bằng bao nhiêu (đơn vị $10^{5}\\ \\text{m}^2/\\text{s}^2$)?", 3.6, "×10⁵ m²/s²", 0.01,
       loi=r"Đề cho căn bậc hai của $\overline{v^2}$ mà thế thẳng vào công thức áp suất, không bình phương."),
  buoc("Áp suất ban đầu", "Áp suất khí ban đầu bằng bao nhiêu (đơn vị $10^{5}$ Pa)?", 1.08, "×10⁵ Pa", 0.01,
       loi=r"Quên hệ số $\dfrac{1}{3}$, hoặc thay $\overline{v^2}$ bằng chính $v_{rms}$ chưa bình phương.",
       ke=[(r"$p=\dfrac{1}{3}\rho\overline{v^2}$", True),
           (r"$p=\rho\overline{v^2}$", r"Thiếu hệ số $\dfrac{1}{3}$: chỉ một trong ba phương bình đẳng vuông góc với thành bình."),
           (r"$p=\dfrac{1}{3}\rho\,v_{rms}$", r"Công thức cần $\overline{v^2}$, tức bình phương của $v_{rms}$; thế thẳng $v_{rms}$ là sai đơn vị.")]),
  buoc("Áp suất sau khi nung nóng", "Áp suất khí sau khi nung nóng bằng bao nhiêu (đơn vị $10^{5}$ Pa)?", 2.43, "×10⁵ Pa", 0.02,
       loi=r"Cho áp suất tăng cùng số lần với tốc độ (tỉ lệ bậc nhất), quên rằng $p$ tỉ lệ với bình phương tốc độ.",
       ke=[(r"$\rho$ giữ nguyên, thế $\overline{v^2}$ mới vào $p=\dfrac{1}{3}\rho\overline{v^2}$", True),
           (r"$p$ tỉ lệ với tốc độ nên nhân $p$ với tỉ số tốc độ", r"$p$ tỉ lệ với $\overline{v^2}$ (bình phương tốc độ), không phải tốc độ."),
           (r"Khối lượng riêng cũng đổi khi nung nóng nên phải tính lại $\rho$", r"Thể tích và lượng khí không đổi nên khối lượng riêng giữ nguyên.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Cho <b>khối lượng mol và nhiệt độ</b>, hỏi <b>tốc độ căn quân phương</b> → đi từ <b>động năng trung bình</b> của một phân tử.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi nhiệt độ sang Kelvin", "Nhiệt độ của khí theo Kelvin là bao nhiêu?", 350, "K", 0.5,
       loi=r"Dùng thẳng số đo Celsius, hoặc cộng nhầm hằng số đổi."),
  buoc("Khối lượng một phân tử", "Khối lượng một phân tử argon bằng bao nhiêu (đơn vị $10^{-26}$ kg)?", 6.64, "×10⁻²⁶ kg", 0.02,
       loi=r"Để $M$ theo gam rồi chia cho $N_A$ nên kết quả lệch ba bậc; hoặc nhân với $N_A$ thay vì chia.",
       ke=[(r"$m=\dfrac{M}{N_A}$ với $M$ đổi ra kg/mol", True),
           (r"$m=M\cdot N_A$", r"$m$ là khối lượng của một phân tử, rất nhỏ; nhân với $N_A$ cho số khổng lồ."),
           (r"$m=\dfrac{M}{N_A}$ giữ $M$ theo g/mol", r"Kết quả sẽ ra gam chứ không phải kg, lệch $1000$ lần so với đơn vị SI.")]),
  buoc("Động năng tịnh tiến trung bình", "Động năng tịnh tiến trung bình của một phân tử argon bằng bao nhiêu (đơn vị $10^{-21}$ J)?", 7.25, "×10⁻²¹ J", 0.03,
       loi=r"Thế nhiệt độ Celsius, hoặc dùng $R$ (hằng số theo mol) thay cho $k$.",
       ke=[(r"$\overline{E_d}=\dfrac{3}{2}kT$ với $T$ theo Kelvin", True),
           (r"$\overline{E_d}=\dfrac{3}{2}kt$ với $t$ theo Celsius", r"Phải dùng nhiệt độ tuyệt đối trong hệ thức tỉ lệ thuận."),
           (r"$\overline{E_d}=\dfrac{3}{2}RT$", r"$R$ ứng với một mol; động năng của một phân tử phải dùng $k=\dfrac{R}{N_A}$.")]),
  buoc("Tốc độ căn quân phương", "Tốc độ căn quân phương của phân tử argon bằng bao nhiêu m/s?", 467, "m/s", 3,
       loi=r"Quên lấy căn, hoặc quên hệ số $2$ khi suy $\overline{v^2}$ từ $\overline{E_d}=\dfrac{1}{2}m\overline{v^2}$.",
       ke=[(r"$\overline{v^2}=\dfrac{2\overline{E_d}}{m}$ rồi $v_{rms}=\sqrt{\overline{v^2}}$", True),
           (r"$v_{rms}=\dfrac{2\overline{E_d}}{m}$", r"Đó mới là $\overline{v^2}$ (đơn vị m²/s²); còn phải lấy căn bậc hai."),
           (r"$v_{rms}=\sqrt{\dfrac{\overline{E_d}}{m}}$", r"Từ $\overline{E_d}=\dfrac{1}{2}m\overline{v^2}$ thì $\overline{v^2}=\dfrac{2\overline{E_d}}{m}$; thiếu hệ số $2$.")]),
  buoc("So sánh với heli", "Tốc độ căn quân phương của heli lớn gấp bao nhiêu lần của argon?", 3.16, "lần", 0.02,
       loi=r"Cho rằng tốc độ tỉ lệ nghịch với khối lượng (không lấy căn), hoặc cho rằng cùng nhiệt độ thì cùng tốc độ.",
       ke=[(r"Cùng $T$ thì cùng $\overline{E_d}$, nên $v$ tỉ lệ nghịch với căn bậc hai của khối lượng", True),
           (r"$v$ tỉ lệ nghịch với khối lượng, lấy thẳng tỉ số khối lượng", r"Cùng $\overline{E_d}=\dfrac{1}{2}mv^2$ thì $v\propto\dfrac{1}{\sqrt{m}}$, không phải $\dfrac{1}{m}$."),
           (r"Cùng nhiệt độ nên cùng tốc độ", r"Cùng nhiệt độ chỉ cho cùng động năng trung bình; khối lượng khác nhau thì tốc độ khác nhau.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"<b>Không cho nhiệt độ</b>, cho <b>áp suất và mật độ phân tử</b> → tìm <b>động năng trung bình</b> trước.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chọn hệ thức để tìm động năng", "Đề chưa cho nhiệt độ. Muốn tìm động năng tịnh tiến trung bình, nên bắt đầu từ hệ thức nào?",
       loi=r"Dùng ngay $\overline{E_d}=\dfrac{3}{2}kT$ khi chưa biết $T$; hoặc đi tìm khối lượng riêng và tốc độ mà đề không cho.",
       lua_chon=[(r"Từ liên hệ giữa áp suất với mật độ phân tử và động năng, vì đề cho $p$ và $\mu$", True),
                 (r"Dùng ngay $\overline{E_d}=\dfrac{3}{2}kT$", r"Chưa biết $T$ nên chưa thế được; $T$ là đại lượng phải tìm sau."),
                 (r"Dùng $p=\dfrac{1}{3}\rho\overline{v^2}$", r"Đề không cho khối lượng riêng hay tốc độ phân tử, nên không đủ dữ kiện.")]),
  buoc("Động năng tịnh tiến trung bình", "Động năng tịnh tiến trung bình của một phân tử bằng bao nhiêu (đơn vị $10^{-21}$ J)?", 6.25, "×10⁻²¹ J", 0.03,
       loi=r"Quên hệ số $\dfrac{3}{2}$ khi giải $\overline{E_d}$ từ $p=\dfrac{2}{3}\mu\overline{E_d}$, hoặc để $\mu$ ở tử số.",
       ke=[(r"Giải $\overline{E_d}=\dfrac{3p}{2\mu}$", True),
           (r"$\overline{E_d}=\dfrac{2p}{3\mu}$", r"Đảo hệ số: từ $p=\dfrac{2}{3}\mu\overline{E_d}$ chuyển $\dfrac{2}{3}$ sang bên kia thì thành $\dfrac{3}{2}$."),
           (r"$\overline{E_d}=\dfrac{3p\mu}{2}$", r"$\mu$ nằm ở mẫu: áp suất bằng $\mu$ nhân với đại lượng khác, nên chia cho $\mu$.")]),
  buoc("Nhiệt độ tuyệt đối", "Nhiệt độ tuyệt đối của khí bằng bao nhiêu Kelvin?", 302, "K", 2,
       loi=r"Quên hệ số $\dfrac{3}{2}$ hoặc giải sai chiều: lấy $T=\dfrac{3\overline{E_d}}{2k}$.",
       ke=[(r"$T=\dfrac{2\overline{E_d}}{3k}$", True),
           (r"$T=\dfrac{\overline{E_d}}{k}$", r"Thiếu hệ số $\dfrac{3}{2}$ trong $\overline{E_d}=\dfrac{3}{2}kT$."),
           (r"$T=\dfrac{3\overline{E_d}}{2k}$", r"Giải ngược: từ $\overline{E_d}=\dfrac{3}{2}kT$ thì $T=\dfrac{2\overline{E_d}}{3k}$.")]),
  buoc("Áp suất sau khi hút bớt và nung nóng", "Áp suất khí lúc này bằng bao nhiêu (đơn vị $10^{4}$ Pa)?", 6.46, "×10⁴ Pa", 0.05,
       loi=r"Chỉ tính đến việc hút bớt khí (chia đôi áp suất) mà quên nhiệt độ đã đổi; hoặc thế nhiệt độ Celsius.",
       ke=[(r"$p'=\mu'kT'$ với $\mu'=\dfrac{\mu}{2}$ và $T'$ theo Kelvin", True),
           (r"$p'=\dfrac{p}{2}$ vì số phân tử còn một nửa", r"Nhiệt độ cũng đã đổi nên $\overline{E_d}$ đổi; mật độ giảm một nửa chưa đủ để kết luận."),
           (r"$p'=\mu'kt'$ với $t'$ theo Celsius", r"Phải dùng nhiệt độ tuyệt đối trong $p=\mu kT$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 9, "Bài 8. Áp suất - động năng của phân tử khí", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
