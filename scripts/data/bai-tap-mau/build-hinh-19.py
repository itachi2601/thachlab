"""Bài tập mẫu Bài 18 "An toàn phóng xạ" (Vật lí 12) — lesson_id 19. 6 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/19.quet-dang.json). Hình: hinh_19.py. Bài chưa có mục bai_tap_mau trong DB nên không có ví dụ cũ / tự luận.
Hằng số và giới hạn chỉ lấy đúng như lý thuyết bài: w_R = 1 (X, gamma, beta), w_R = 20 (alpha); 1 Gy = 1 J/kg;
suất liều ∝ 1/r²; liều = suất liều × thời gian; giới hạn nghề nghiệp 20 mSv/năm; bảng đo ba tấm chắn (360 → 355 giấy, 335 nhôm 3 mm, 154 chì 5 mm).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-19.py   (idempotent, ghi 19.json với review.checked=false)"""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_19 import *

J = os.path.join(HERE, "19.json")
T231 = "Liều chiếu xạ và tác hại của phóng xạ"
T232 = "Nguyên tắc an toàn khi làm việc với nguồn phóng xạ"

# ═════════════ KIỂM SỐ (độc lập với lời giải: nếu lệch thì dừng) ═════════════
def rate(h1, r1, r2): return h1 * (r1 / r2) ** 2          # suất liều theo 1/r²
# Dạng 1
_D1 = 1.2e-3 / 12
assert abs(_D1 - 1e-4) < 1e-12 and abs(_D1 * 1 * 1000 - 0.1) < 1e-9                      # H = 0,1 mSv, D = 1e-4 Gy = 0,1 mGy
# Dạng 2
_D2 = 2.0e-3 / 0.50
assert abs(_D2 * 1000 - 4.0) < 1e-9 and abs(_D2 * 1 * 1000 - 4.0) < 1e-9 and abs(_D2 * 20 * 1000 - 80.0) < 1e-9 and 20 * _D2 / (1 * _D2) == 20
assert abs(_D2 / 20 * 1000 - 0.2) < 1e-9                     # lỗi chia cho w_R
# Dạng 3
assert abs(rate(72, 0.5, 1.5) - 8) < 1e-9
assert abs(72 / 3 - 24) < 1e-9 and abs(72 / 1.5 ** 2 - 32) < 1e-9                         # hai cách sai khác 8
_r3 = 0.5 * math.sqrt(72 / 2.0)
assert abs(_r3 - 3.0) < 1e-9 and abs(rate(72, 0.5, 3.0) - 2.0) < 1e-9
assert abs(0.5 * 36 - 18) < 1e-9 and abs(0.5 * 36 ** 2 - 648) < 1e-9
# nghiệm duy nhất vì r > 0 và suất liều giảm đơn điệu theo r
assert all(rate(72, 0.5, r) > 2.0 for r in [i / 100 for i in range(50, 300)]) and rate(72, 0.5, 3.001) < 2.0
# Dạng 4
_h2 = rate(250, 1.0, 2.5)
assert abs(_h2 - 40) < 1e-9 and abs(_h2 * 12 / 60 - 8) < 1e-9 and abs(20 / _h2 * 60 - 30) < 1e-9
assert abs(250 / 2.5 - 100) < 1e-9 and abs(_h2 * 12 - 480) < 1e-9 and abs(_h2 / 20 - 2) < 1e-9 and abs(_h2 * 20 - 800) < 1e-9     # các cách sai
# Dạng 5
_A = (1.0 / 3.0) ** 2 * 100; _B = 10 / 40 * 100; _C = 154 / 360 * 100; _Dn = 335 / 360 * 100
assert abs(_A - 11.111) < 1e-3 and abs(_B - 25.0) < 1e-9 and abs(_C - 42.778) < 1e-3 and abs(_Dn - 93.056) < 1e-3
assert min((_A, "A"), (_B, "B"), (_C, "C"), (_Dn, "D"))[1] == "A"
assert abs((360 - 154) / 360 * 100 - 57.22) < 0.01 and abs((154 / 360) ** 2 * 100 - 18.3) < 0.05      # hai cách sai khác 42,8
assert abs(1 / 3 * 100 - 33.33) < 0.01 and abs(40 / 10 * 100 - 400) < 1e-9
# Dạng 6
_h6 = rate(160, 1.0, 2.0); _H6 = _h6 * 2000 / 1000; _cp = 20 * 1000 / 2000; _rmin = 1.0 * math.sqrt(160 / _cp)
assert abs(_h6 - 40) < 1e-9 and abs(_H6 - 80) < 1e-9 and abs(_H6 / 20 - 4) < 1e-9 and abs(_cp - 10) < 1e-9 and abs(_rmin - 4.0) < 1e-9
assert abs(rate(160, 1.0, 4.0) * 2000 / 1000 - 20) < 1e-9          # đúng bằng giới hạn tại 4,0 m
assert abs(2.0 * 4 - 8) < 1e-9 and abs(160 / _cp - 16) < 1e-9 and abs(160 * 2000 / 1000 - 320) < 1e-9 and abs(20 / _H6 - 0.25) < 1e-9

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Liều hấp thụ và liều tương đương của tia X",
      topic=T231,
      problem_html=r"""<p>Khi chụp X-quang ngực, khối mô vùng ngực bị chiếu có khối lượng $12\ \text{kg}$ và hấp thụ năng lượng $1{,}2\ \text{mJ}$ từ chùm tia X. Coi năng lượng chia đều trong khối mô; tia X có hệ số chất lượng $w_R = 1$.</p><ol type="a"><li>Tính liều hấp thụ $D$ của khối mô, theo gray.</li><li>Tính liều tương đương $H$ của khối mô, theo mSv.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Cùng năng lượng hấp thụ, khác loại tia",
      topic=T231,
      problem_html=r"""<p>Hai mẫu mô giống nhau, mỗi mẫu có khối lượng $0{,}50\ \text{kg}$. Mẫu A bị chiếu tia gamma, mẫu B bị chiếu tia alpha. Mỗi mẫu hấp thụ cùng một năng lượng $2{,}0\ \text{mJ}$, coi năng lượng chia đều trong mẫu.</p><ol type="a"><li>Tính liều hấp thụ của mỗi mẫu, theo mGy.</li><li>Tính liều tương đương của mỗi mẫu, theo mSv.</li><li>Mẫu nào chịu tác hại sinh học lớn hơn, và lớn hơn bao nhiêu lần?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Suất liều theo khoảng cách tới nguồn",
      topic=T232,
      problem_html=r"""<p>Một máy đo đặt cách một nguồn gamma nhỏ $0{,}50\ \text{m}$ cho suất liều $72\ \mu\text{Sv/h}$. Coi nguồn là nguồn điểm, bức xạ toả đều mọi hướng, bỏ qua tán xạ và vật chắn.</p><ol type="a"><li>Tính suất liều tại điểm cách nguồn $1{,}5\ \text{m}$.</li><li>Phải đặt máy đo cách nguồn bao nhiêu mét thì suất liều chỉ còn $2{,}0\ \mu\text{Sv/h}$?</li></ol>"""),
 dict(label="Dạng 4 · Khá · Liều theo thời gian đứng và thời gian đứng tối đa",
      topic=T232,
      problem_html=r"""<p>Một nguồn gamma nhỏ cho suất liều $250\ \mu\text{Sv/h}$ tại điểm cách nguồn $1{,}0\ \text{m}$. Một kỹ thuật viên đứng cách nguồn $2{,}5\ \text{m}$. Coi nguồn là nguồn điểm, bỏ qua vật chắn.</p><ol type="a"><li>Tính suất liều tại chỗ kỹ thuật viên đứng.</li><li>Đứng $12$ phút thì kỹ thuật viên nhận liều bao nhiêu µSv?</li><li>Để liều mỗi ca không vượt quá $20\ \mu\text{Sv}$ thì được đứng tối đa bao nhiêu phút?</li></ol>"""),
 dict(label="Dạng 5 · Khá · So sánh các biện pháp giảm liều: thời gian, khoảng cách, che chắn",
      topic=T232,
      problem_html=r"""<p>Một kỹ thuật viên làm việc với nguồn gamma, đứng cách nguồn $1{,}0\ \text{m}$ và ở đó $40$ phút mỗi ca. Khi không có tấm chắn, máy đo ở $1{,}0\ \text{m}$ ghi $360$ xung/phút; suất liều tỉ lệ với số xung ghi được (số liệu minh hoạ như bảng đo của bài). Xét bốn biện pháp, mỗi biện pháp áp dụng riêng và giữ nguyên các điều kiện còn lại:</p><ul><li>A: lùi ra xa $3{,}0\ \text{m}$, vẫn ở lại $40$ phút.</li><li>B: vẫn đứng cách $1{,}0\ \text{m}$ nhưng rút thời gian còn $10$ phút.</li><li>C: chèn tấm chì dày $5\ \text{mm}$; máy đo ghi $154$ xung/phút.</li><li>D: chèn tấm nhôm dày $3\ \text{mm}$; máy đo ghi $335$ xung/phút.</li></ul><ol type="a"><li>Tính phần trăm liều mỗi ca còn lại so với ban đầu ứng với từng biện pháp.</li><li>Biện pháp nào giảm liều nhiều nhất?</li></ol>"""),
 dict(label="Dạng 6 · Khó · Liều cả năm so với giới hạn nghề nghiệp và khoảng cách tối thiểu",
      topic=T232,
      problem_html=r"""<p>Một nguồn gamma nhỏ cho suất liều $160\ \mu\text{Sv/h}$ tại điểm cách nguồn $1{,}0\ \text{m}$. Một nhân viên làm việc $2\,000$ giờ mỗi năm tại vị trí cách nguồn $2{,}0\ \text{m}$. Coi nguồn là nguồn điểm, bỏ qua vật chắn. Giới hạn liều nghề nghiệp là $20\ \text{mSv/năm}$.</p><ol type="a"><li>Tính liều nhân viên nhận trong một năm, theo mSv. Liều đó gấp mấy lần giới hạn?</li><li>Giữ nguyên $2\,000$ giờ/năm, nhân viên phải đứng cách nguồn ít nhất bao nhiêu mét để liều cả năm không vượt giới hạn?</li></ol>"""),
]

BUILD = [d1, d2, d3, d4, d5, d6]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (hàng "cần tìm" chỉ ghi đại lượng cần tìm; ô ⚠ chỉ nêu câu hỏi điều kiện) ═════════════
ANALYSIS = [
 [(r"“khối lượng $12\ \text{kg}$”", r"$m=12\ \text{kg}$", r"Khối lượng mô hấp thụ"),
  (r"“hấp thụ năng lượng $1{,}2\ \text{mJ}$”", r"$E=1{,}2\ \text{mJ}$", r"Năng lượng mô hấp thụ; đơn vị năng lượng trong hệ SI là jun"),
  (r"“tia X có hệ số chất lượng $w_R = 1$”", r"$w_R=1$", r"Hệ số chất lượng: cho biết loại tia gây hại nhiều hay ít so với tia X"),
  (r"“Coi năng lượng chia đều trong khối mô”", r"Mọi phần của khối mô nhận như nhau", r"⚠ Năng lượng có chia đều cho cả khối không? Quyết định lấy một giá trị liều chung cho cả khối"),
  (r"“a) liều hấp thụ $D$, theo gray”", r"Đại lượng cần tìm: $D$ (Gy)", r"Khái niệm liều hấp thụ; đơn vị gray"),
  (r"“b) liều tương đương $H$, theo mSv”", r"Đại lượng cần tìm: $H$ (mSv)", r"Khái niệm liều tương đương; đơn vị sievert, ước mSv")],
 [(r"“khối lượng $0{,}50\ \text{kg}$”", r"$m=0{,}50\ \text{kg}$ (mỗi mẫu)", r"Khối lượng mô hấp thụ"),
  (r"“cùng một năng lượng $2{,}0\ \text{mJ}$”", r"$E=2{,}0\ \text{mJ}$ (mỗi mẫu)", r"Năng lượng mô hấp thụ; đơn vị jun"),
  (r"“mẫu A bị chiếu tia gamma”", r"$w_R=1$", r"Hệ số chất lượng của tia gamma (tra theo bài)"),
  (r"“mẫu B bị chiếu tia alpha”", r"$w_R=20$", r"Hệ số chất lượng của tia alpha (tra theo bài)"),
  (r"“Hai mẫu giống nhau … cùng một năng lượng”", r"Cùng $m$, cùng $E$ cho cả hai mẫu", r"⚠ Hai mẫu hấp thụ như nhau thì mức nguy hiểm có chắc như nhau không? Mức nguy hiểm còn phụ thuộc yếu tố nào?"),
  (r"“a) liều hấp thụ của mỗi mẫu”", r"Đại lượng cần tìm: $D_A$, $D_B$ (mGy)", r"Khái niệm liều hấp thụ"),
  (r"“b) liều tương đương của mỗi mẫu”", r"Đại lượng cần tìm: $H_A$, $H_B$ (mSv)", r"Khái niệm liều tương đương; hệ số chất lượng"),
  (r"“c) Mẫu nào chịu tác hại sinh học lớn hơn, lớn hơn bao nhiêu lần”", r"Đại lượng cần tìm: mẫu nào hại hơn và gấp mấy lần", r"Liều tương đương là thước đo mức nguy hiểm sinh học")],
 [(r"“cách … nguồn gamma nhỏ $0{,}50\ \text{m}$ cho suất liều $72\ \mu\text{Sv/h}$”", r"$r_1=0{,}50\ \text{m}$ ; $\dot H_1=72\ \mu\text{Sv/h}$", r"Suất liều: liều trong một đơn vị thời gian; đơn vị µSv/h"),
  (r"“nguồn điểm, toả đều mọi hướng, bỏ qua tán xạ và vật chắn”", r"Chỉ khoảng cách làm suất liều thay đổi", r"⚠ Bức xạ toả đều mọi hướng và không bị chắn: suất liều phụ thuộc vào yếu tố nào?"),
  (r"“a) tại điểm cách nguồn $1{,}5\ \text{m}$”", r"$r_2=1{,}5\ \text{m}$ ; đại lượng cần tìm: $\dot H_2$", r"Quy luật suất liều thay đổi khi tăng khoảng cách tới nguồn"),
  (r"“b) … suất liều chỉ còn $2{,}0\ \mu\text{Sv/h}$”", r"$\dot H_3=2{,}0\ \mu\text{Sv/h}$ ; đại lượng cần tìm: $r_3$", r"Quy luật trên dùng theo chiều ngược: từ suất liều suy ra khoảng cách")],
 [(r"“suất liều $250\ \mu\text{Sv/h}$ tại điểm cách nguồn $1{,}0\ \text{m}$”", r"$\dot H_1=250\ \mu\text{Sv/h}$ ; $r_1=1{,}0\ \text{m}$", r"Suất liều đã biết ở một khoảng cách"),
  (r"“nguồn nhỏ … bỏ qua vật chắn”", r"Chỉ khoảng cách làm suất liều thay đổi", r"⚠ Nguồn có coi là nguồn điểm và không bị chắn không? Quyết định cách suy suất liều ở chỗ khác"),
  (r"“đứng cách nguồn $2{,}5\ \text{m}$”", r"$r_2=2{,}5\ \text{m}$", r"Quy luật suất liều theo khoảng cách"),
  (r"“đứng $12$ phút”", r"$t=12$ phút", r"Quan hệ giữa liều, suất liều và thời gian; đơn vị thời gian phải khớp với đơn vị của suất liều"),
  (r"“liều mỗi ca không vượt quá $20\ \mu\text{Sv}$”", r"$H_{\max}=20\ \mu\text{Sv}$", r"Liều tối đa cho phép trong một ca"),
  (r"“a) suất liều tại chỗ đứng”", r"Đại lượng cần tìm: $\dot H_2$", r"Suất liều theo khoảng cách"),
  (r"“b) … nhận liều bao nhiêu µSv”", r"Đại lượng cần tìm: $H$", r"Liều theo thời gian phơi nhiễm"),
  (r"“c) … đứng tối đa bao nhiêu phút”", r"Đại lượng cần tìm: $t_{\max}$", r"Liều theo thời gian phơi nhiễm, dùng theo chiều ngược")],
 [(r"“đứng cách nguồn $1{,}0\ \text{m}$ và ở đó $40$ phút mỗi ca”", r"$r=1{,}0\ \text{m}$ ; $t=40$ phút", r"Liều phụ thuộc suất liều và thời gian phơi nhiễm"),
  (r"“ghi $360$ xung/phút; suất liều tỉ lệ với số xung ghi được”", r"$N_0=360$ xung/phút", r"⚠ Suất liều có tỉ lệ với số xung không? Quyết định hai số xung có so với nhau trực tiếp được hay không"),
  (r"“A: lùi ra xa $3{,}0\ \text{m}$, vẫn ở lại $40$ phút”", r"$r'=3{,}0\ \text{m}$ ; $t$ giữ nguyên", r"Quy luật suất liều theo khoảng cách"),
  (r"“B: … rút thời gian còn $10$ phút”", r"$t'=10$ phút ; $r$ giữ nguyên", r"Quan hệ giữa liều và thời gian phơi nhiễm"),
  (r"“C: tấm chì dày $5\ \text{mm}$; ghi $154$ xung/phút”", r"$N_C=154$ xung/phút", r"Che chắn: số xung còn lại phản ánh suất liều còn lại"),
  (r"“D: tấm nhôm dày $3\ \text{mm}$; ghi $335$ xung/phút”", r"$N_D=335$ xung/phút", r"Che chắn: số xung còn lại phản ánh suất liều còn lại"),
  (r"“a) phần trăm liều mỗi ca còn lại so với ban đầu”", r"Đại lượng cần tìm: phần trăm còn lại của A, B, C, D", r"Cách đưa các biện pháp khác loại về cùng một thang so sánh"),
  (r"“b) Biện pháp nào giảm liều nhiều nhất”", r"Đại lượng cần tìm: biện pháp tốt nhất", r"So các giá trị ở câu a với nhau")],
 [(r"“suất liều $160\ \mu\text{Sv/h}$ tại điểm cách nguồn $1{,}0\ \text{m}$”", r"$\dot H_1=160\ \mu\text{Sv/h}$ ; $r_1=1{,}0\ \text{m}$", r"Suất liều đã biết ở một khoảng cách"),
  (r"“nguồn điểm, bỏ qua vật chắn”", r"Chỉ khoảng cách làm suất liều thay đổi", r"⚠ Nguồn có coi là nguồn điểm và không bị chắn không? Quyết định cách suy suất liều ở chỗ khác"),
  (r"“cách nguồn $2{,}0\ \text{m}$”", r"$r_2=2{,}0\ \text{m}$", r"Quy luật suất liều theo khoảng cách"),
  (r"“$2\,000$ giờ mỗi năm”", r"$t=2\,000\ \text{h}$", r"Liều tích luỹ theo thời gian; đơn vị giờ khớp với µSv/h"),
  (r"“giới hạn liều nghề nghiệp là $20\ \text{mSv/năm}$”", r"$H_{gh}=20\ \text{mSv}$", r"Giới hạn liều nghề nghiệp; kiểm tra đơn vị so với µSv/h của suất liều"),
  (r"“a) liều trong một năm; gấp mấy lần giới hạn”", r"Đại lượng cần tìm: $H_{năm}$ và $H_{năm}/H_{gh}$", r"Liều theo thời gian phơi nhiễm; so với giới hạn"),
  (r"“b) … cách nguồn ít nhất bao nhiêu mét”", r"Đại lượng cần tìm: $r_{\min}$", r"Quy luật suất liều theo khoảng cách, dùng theo chiều ngược")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> liều hấp thụ là năng lượng mà mỗi kilôgam mô nhận được; liều tương đương cho biết mức nguy hiểm sinh học, quy về tia X.",
       r"<strong>Quy ước:</strong> hệ số chất lượng $w_R=1$ với tia X, gamma, beta; $w_R=20$ với alpha.",
       r"<strong>Công thức:</strong> $D=\dfrac{E}{m}$ ($1\ \text{Gy}=1\ \text{J/kg}$) · $H=w_R\,D$ (đơn vị sievert).",
       r"⚠ <strong>Điều kiện:</strong> $E$ tính bằng jun, $m$ bằng kilôgam; năng lượng chia đều trong khối mô."]
RC2 = [r"<strong>Khái niệm:</strong> liều hấp thụ (Gy) đo năng lượng mỗi kilôgam mô nhận được, không phân biệt loại tia; liều tương đương (Sv) đo mức nguy hiểm sinh học.",
       r"<strong>Quy ước:</strong> $w_R=1$ với tia gamma; $w_R=20$ với tia alpha.",
       r"<strong>Công thức:</strong> $D=\dfrac{E}{m}$ · $H=w_R\,D$.",
       r"⚠ <strong>Điều kiện:</strong> so tác hại sinh học phải dùng $H$ (Sv), không so $D$ (Gy)."]
RC3 = [r"<strong>Khái niệm:</strong> suất liều ($\mu\text{Sv/h}$) là liều trong một đơn vị thời gian; nguồn điểm phát bức xạ đều mọi hướng.",
       r"<strong>Định luật:</strong> cùng một lượng bức xạ trải trên mặt cầu diện tích $4\pi r^2$ nên suất liều tỉ lệ nghịch với $r^2$.",
       r"<strong>Công thức:</strong> $\dfrac{\dot H_2}{\dot H_1}=\left(\dfrac{r_1}{r_2}\right)^2$.",
       r"⚠ <strong>Điều kiện:</strong> chia theo tỉ số hai khoảng cách, không theo số mét; nguồn điểm, không vật chắn."]
RC4 = [r"<strong>Khái niệm:</strong> suất liều là liều trong mỗi giờ; liều nhận được là suất liều nhân thời gian phơi nhiễm.",
       r"<strong>Định luật:</strong> suất liều tỉ lệ nghịch với $r^2$; liều tỉ lệ thuận với thời gian.",
       r"<strong>Công thức:</strong> $\dot H_2=\dot H_1\left(\dfrac{r_1}{r_2}\right)^2$ · $H=\dot H\,t$ · $t_{\max}=\dfrac{H_{\max}}{\dot H}$.",
       r"⚠ <strong>Điều kiện:</strong> $t$ đổi ra giờ khi suất liều tính theo $\mu\text{Sv/h}$; nguồn điểm, không vật chắn."]
RC5 = [r"<strong>Khái niệm:</strong> ba cách giảm liều là rút thời gian, tăng khoảng cách, che chắn; muốn so phải đưa về cùng một thang: phần trăm liều còn lại.",
       r"<strong>Định luật:</strong> liều tỉ lệ thuận với thời gian; suất liều tỉ lệ nghịch với $r^2$; tấm chắn làm số xung máy đo ghi được giảm theo.",
       r"<strong>Công thức:</strong> khoảng cách $\left(\dfrac{r_1}{r_2}\right)^2$ · thời gian $\dfrac{t_2}{t_1}$ · tấm chắn $\dfrac{N}{N_0}$.",
       r"⚠ <strong>Điều kiện:</strong> mỗi biện pháp tính riêng, giữ nguyên các yếu tố còn lại; “có tấm chắn” chưa đủ, còn phải đúng vật liệu và đủ dày."]
RC6 = [r"<strong>Khái niệm:</strong> liều nhận trong thời gian dài là suất liều nhân thời gian; giới hạn liều nghề nghiệp là $20\ \text{mSv/năm}$.",
       r"<strong>Định luật:</strong> suất liều tỉ lệ nghịch với $r^2$; liều tỉ lệ thuận với thời gian.",
       r"<strong>Công thức:</strong> $\dot H_2=\dot H_1\left(\dfrac{r_1}{r_2}\right)^2$ · $H=\dot H\,t$ · $\dot H_{cp}=\dfrac{H_{gh}}{t}$.",
       r"⚠ <strong>Điều kiện:</strong> $1\ \text{mSv}=1000\ \mu\text{Sv}$, đổi trước khi so sánh; nguồn điểm, không vật chắn."]

SOLS = [
 sol(RC1, [
  ("Liều hấp thụ (câu a)", [P(r"Đổi năng lượng ra jun trước khi chia cho kilôgam:"), M(r"E=1{,}2\ \text{mJ}=1{,}2\cdot10^{-3}\ \text{J}"),
        M(r"D=\dfrac{E}{m}"), M(r"D=\dfrac{1{,}2\cdot10^{-3}}{12}"), A(r"D=1{,}0\cdot10^{-4}\ \text{Gy}=0{,}10\ \text{mGy}")]),
  ("Liều tương đương (câu b)", [M(r"H=w_R\,D"), M(r"H=1\cdot1{,}0\cdot10^{-4}"), A(r"H=1{,}0\cdot10^{-4}\ \text{Sv}=0{,}10\ \text{mSv}"),
        P(r"Với tia X ($w_R=1$) giá trị số của $H$ bằng $D$, chỉ đổi tên đơn vị từ Gy sang Sv.")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{J}/\text{kg}=\text{Gy}$, đúng."),
        P(r"Một lần chụp X-quang ngực cỡ $0{,}1\ \text{mSv}$ (mốc nêu trong bài): khớp.")])],
  [r"a) $D=1{,}0\cdot10^{-4}\ \text{Gy}=0{,}10\ \text{mGy}$", r"b) $H=0{,}10\ \text{mSv}$"],
  r"Nhận dạng: đề cho <strong>năng lượng hấp thụ và khối lượng mô</strong> → $D=\dfrac{E}{m}$, rồi nhân $w_R$ để ra $H$."),
 sol(RC2, [
  ("Liều hấp thụ của mỗi mẫu (câu a)", [P(r"Hai mẫu cùng $E=2{,}0\cdot10^{-3}\ \text{J}$ và cùng $m=0{,}50\ \text{kg}$ nên cùng liều hấp thụ:"),
        M(r"D=\dfrac{E}{m}=\dfrac{2{,}0\cdot10^{-3}}{0{,}50}"), A(r"D_A=D_B=4{,}0\cdot10^{-3}\ \text{Gy}=4{,}0\ \text{mGy}")]),
  ("Liều tương đương của mỗi mẫu (câu b)", [P(r"Mỗi mẫu nhân với hệ số chất lượng của loại tia chiếu vào nó:"),
        M(r"H_A=w_{R,\gamma}\,D=1\cdot4{,}0\ \text{mSv}"), M(r"H_B=w_{R,\alpha}\,D=20\cdot4{,}0\ \text{mSv}"),
        A(r"H_A=4{,}0\ \text{mSv}\quad;\quad H_B=80\ \text{mSv}")]),
  ("So sánh tác hại (câu c)", [P(r"Tác hại sinh học so bằng liều tương đương:"), M(r"\dfrac{H_B}{H_A}=\dfrac{80}{4{,}0}"),
        A(r"T:Mẫu B chịu tác hại lớn hơn, gấp <strong>20 lần</strong> mẫu A.")]),
  ("Kiểm tra", [P(r"Cùng liều hấp thụ nhưng $H$ khác nhau vì alpha dồn năng lượng vào một dải tế bào rất hẹp."),
        P(r"Tỉ số $\dfrac{H_B}{H_A}$ đúng bằng tỉ số hai hệ số chất lượng $\dfrac{20}{1}$: hợp lí.")])],
  [r"a) $D_A=D_B=4{,}0\ \text{mGy}$", r"b) $H_A=4{,}0\ \text{mSv}$ ; $H_B=80\ \text{mSv}$", r"c) Mẫu B, gấp $20$ lần mẫu A"],
  r"Nhận dạng: đề cho <strong>cùng năng lượng hấp thụ, khác loại tia</strong> → cùng $D$ nhưng $H=w_R\,D$ khác nhau; so tác hại bằng $H$."),
 sol(RC3, [
  ("Tỉ số khoảng cách (câu a)", [M(r"\dfrac{r_2}{r_1}=\dfrac{1{,}5}{0{,}50}"), A(r"\dfrac{r_2}{r_1}=3")]),
  (r"Suất liều tại điểm cách $1{,}5\ \text{m}$ (câu a)", [P(r"Xa gấp $3$ lần thì suất liều giảm $3^2$ lần:"),
        M(r"\dot H_2=\dot H_1\left(\dfrac{r_1}{r_2}\right)^2=\dfrac{72}{3^2}"), A(r"\dot H_2=8\ \mu\text{Sv/h}"),
        P(r"Chia $9$ chứ không chia $3$: suất liều giảm theo bình phương khoảng cách.")]),
  ("Tỉ số suất liều (câu b)", [P(r"Suất liều phải giảm từ $72$ xuống $2{,}0\ \mu\text{Sv/h}$:"), M(r"\dfrac{\dot H_1}{\dot H_3}=\dfrac{72}{2{,}0}"), A(r"\dfrac{\dot H_1}{\dot H_3}=36")]),
  ("Khoảng cách cần tìm (câu b)", [P(r"Suất liều giảm $36$ lần nên khoảng cách tăng $\sqrt{36}$ lần:"),
        M(r"\dfrac{r_3}{r_1}=\sqrt{\dfrac{\dot H_1}{\dot H_3}}=\sqrt{36}=6"), M(r"r_3=6\cdot0{,}50"), A(r"r_3=3{,}0\ \text{m}")]),
  ("Kiểm tra", [P(r"Ở $1{,}5\ \text{m}$: xa nguồn hơn $0{,}50\ \text{m}$ nên suất liều nhỏ hơn $72\ \mu\text{Sv/h}$: hợp lí."),
        P(r"Thế ngược: tại $3{,}0\ \text{m}$ khoảng cách gấp $6$ lần, suất liều $\dfrac{72}{6^2}=2{,}0\ \mu\text{Sv/h}$, đúng yêu cầu.")])],
  [r"a) $\dot H_2=8\ \mu\text{Sv/h}$", r"b) $r_3=3{,}0\ \text{m}$"],
  r"Nhận dạng: đề đổi <strong>khoảng cách tới nguồn điểm</strong> → suất liều tỉ lệ nghịch với $r^2$; chia theo <strong>tỉ số</strong> khoảng cách."),
 sol(RC4, [
  ("Suất liều tại chỗ đứng (câu a)", [M(r"\dfrac{r_2}{r_1}=\dfrac{2{,}5}{1{,}0}=2{,}5"), M(r"\dot H_2=\dfrac{\dot H_1}{(r_2/r_1)^2}=\dfrac{250}{2{,}5^2}"), A(r"\dot H_2=40\ \mu\text{Sv/h}")]),
  ("Liều trong $12$ phút (câu b)", [P(r"Suất liều tính theo giờ nên đổi phút ra giờ:"), M(r"t=\dfrac{12}{60}=0{,}20\ \text{h}"),
        M(r"H=\dot H_2\,t=40\cdot0{,}20"), A(r"H=8\ \mu\text{Sv}")]),
  ("Thời gian đứng tối đa (câu c)", [P(r"Thời gian bằng liều cho phép chia cho suất liều:"), M(r"t_{\max}=\dfrac{H_{\max}}{\dot H_2}=\dfrac{20}{40}=0{,}50\ \text{h}"),
        A(r"t_{\max}=0{,}50\ \text{h}=30\ \text{phút}")]),
  ("Kiểm tra", [P(r"Đứng $30$ phút thì $40\cdot0{,}50=20\ \mu\text{Sv}$, đúng bằng liều cho phép."),
        P(r"$12$ phút $\lt30$ phút nên liều $8\ \mu\text{Sv}\lt20\ \mu\text{Sv}$: hợp lí.")])],
  [r"a) $\dot H_2=40\ \mu\text{Sv/h}$", r"b) $H=8\ \mu\text{Sv}$", r"c) $t_{\max}=30$ phút"],
  r"Nhận dạng: đề cho <strong>suất liều, thời gian đứng, liều cho phép</strong> → $H=\dot H\,t$ và đổi <strong>phút ra giờ</strong>."),
 sol(RC5, [
  ("Lùi ra xa — biện pháp A (câu a)", [P(r"Xa gấp $3$ lần nên suất liều còn $\dfrac{1}{3^2}$; thời gian giữ nguyên nên liều đổi theo suất liều:"),
        M(r"\dfrac{H'}{H}=\left(\dfrac{1{,}0}{3{,}0}\right)^2=\dfrac19"), A(r"\dfrac{H'}{H}\approx11{,}1\ \%")]),
  ("Rút thời gian — biện pháp B (câu a)", [P(r"Suất liều giữ nguyên, liều tỉ lệ thuận với thời gian:"), M(r"\dfrac{H'}{H}=\dfrac{t'}{t}=\dfrac{10}{40}"), A(r"\dfrac{H'}{H}=25\ \%")]),
  ("Che chắn — biện pháp C và D (câu a)", [P(r"Suất liều tỉ lệ với số xung, nên phần trăm còn lại bằng tỉ số số xung:"),
        M(r"\text{C (chì)}:\ \dfrac{154}{360}\approx42{,}8\ \%"), M(r"\text{D (nhôm)}:\ \dfrac{335}{360}\approx93{,}1\ \%"),
        A(r"\text{C}\approx42{,}8\ \%\quad;\quad\text{D}\approx93{,}1\ \%")]),
  ("Chọn biện pháp (câu b)", [P(r"Liều còn lại càng nhỏ thì biện pháp càng hiệu quả:"), M(r"11{,}1\ \%\lt25\ \%\lt42{,}8\ \%\lt93{,}1\ \%"),
        A(r"T:Biện pháp <strong>A</strong> (lùi ra xa $3{,}0\ \text{m}$) giảm liều nhiều nhất.")]),
  ("Kiểm tra", [P(r"Chì là vật liệu đúng loại cho gamma, nhưng ở độ dày $5\ \text{mm}$ vẫn để lọt gần một nửa số xung (theo bảng đo ba tấm chắn của bài): chưa bằng lùi xa."),
        P(r"Nhôm mỏng gần như không chắn gamma, liều còn trên $90\ \%$: khớp bảng đo của bài.")])],
  [r"a) A $\approx11{,}1\ \%$ ; B $=25\ \%$ ; C $\approx42{,}8\ \%$ ; D $\approx93{,}1\ \%$", r"b) Biện pháp A"],
  r"Nhận dạng: đề cho <strong>nhiều biện pháp giảm liều khác loại</strong> → quy mỗi biện pháp về <strong>phần trăm liều còn lại</strong> rồi so."),
 sol(RC6, [
  ("Suất liều tại chỗ làm việc", [M(r"\dot H_2=\dot H_1\left(\dfrac{r_1}{r_2}\right)^2=\dfrac{160}{2^2}"), A(r"\dot H_2=40\ \mu\text{Sv/h}")]),
  ("Liều cả năm (câu a)", [M(r"H=\dot H_2\,t=40\cdot2\,000=80\,000\ \mu\text{Sv}"), P(r"Đổi sang mSv (chia $1000$):"), A(r"H=80\ \text{mSv}")]),
  ("So với giới hạn (câu a)", [P(r"Đã cùng đơn vị mSv, lấy tỉ số:"), M(r"\dfrac{H}{H_{gh}}=\dfrac{80}{20}=4"),
        A(r"T:Liều cả năm <strong>gấp 4 lần</strong> giới hạn nghề nghiệp: vượt.")]),
  ("Suất liều lớn nhất cho phép (câu b)", [P(r"Giới hạn $20\ \text{mSv}=20\,000\ \mu\text{Sv}$ chia cho số giờ làm việc:"),
        M(r"\dot H_{cp}=\dfrac{H_{gh}}{t}=\dfrac{20\,000}{2\,000}"), A(r"\dot H_{cp}=10\ \mu\text{Sv/h}")]),
  ("Khoảng cách tối thiểu (câu b)", [P(r"Suất liều từ $160$ phải giảm xuống $10\ \mu\text{Sv/h}$ so với mốc $1{,}0\ \text{m}$:"),
        M(r"\dfrac{r_3}{r_1}=\sqrt{\dfrac{\dot H_1}{\dot H_{cp}}}=\sqrt{\dfrac{160}{10}}=\sqrt{16}=4"), M(r"r_3=4\cdot1{,}0"), A(r"r_{\min}=4{,}0\ \text{m}")]),
  ("Kiểm tra", [P(r"Tại $4{,}0\ \text{m}$: $\dot H=\dfrac{160}{4^2}=10\ \mu\text{Sv/h}$; liều cả năm $10\cdot2\,000=20\,000\ \mu\text{Sv}=20\ \text{mSv}$, đúng bằng giới hạn."),
        P(r"Liều cần giảm $4$ lần nên chỉ phải lùi xa gấp $2$ lần ($2{,}0\ \text{m}\to4{,}0\ \text{m}$), nhỏ hơn số lần cần giảm liều.")])],
  [r"a) $H=80\ \text{mSv}$, gấp $4$ lần giới hạn (vượt)", r"b) $r_{\min}=4{,}0\ \text{m}$"],
  r"Nhận dạng: đề cho <strong>giờ làm việc cả năm và giới hạn mSv/năm</strong> → đổi mSv ra µSv, quy ngược về suất liều cho phép rồi về khoảng cách."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>năng lượng hấp thụ và khối lượng mô</b> → nghĩ tới <b>$D=E/m$</b>, rồi nhân <b>$w_R$</b> để ra $H$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Liều hấp thụ", "Liều hấp thụ của khối mô là bao nhiêu mGy?", 0.1, "mGy", 0.005,
       loi=r"Để nguyên mJ khi chia cho kg nên liều lớn gấp nghìn lần, hoặc ghi đơn vị là Sv vì coi Gy và Sv là một."),
  buoc("Liều tương đương", "Liều tương đương của khối mô là bao nhiêu mSv?", 0.1, "mSv", 0.005,
       loi=r"Quên đổi từ Sv sang mSv, hoặc dùng sai hệ số chất lượng của tia X.",
       ke=[(r"Nhân liều hấp thụ với hệ số chất lượng $w_R$ của tia X", True),
           (r"Nhân liều hấp thụ với khối lượng mô", r"$D$ đã là năng lượng trên mỗi kilôgam; nhân với khối lượng chỉ quay lại năng lượng, không phải mức nguy hiểm."),
           (r"Chia liều hấp thụ cho khối lượng mô", r"$D$ đã được chia cho khối lượng một lần; chia thêm lần nữa là đếm hai lần.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cùng năng lượng hấp thụ, khác loại tia</b> → nghĩ tới <b>$H=w_R\,D$</b>, so tác hại bằng $H$, không bằng $D$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Liều hấp thụ của mỗi mẫu", "Liều hấp thụ của mỗi mẫu là bao nhiêu mGy?", 4, "mGy", 0.1,
       loi=r"Nhân thay vì chia cho khối lượng, hoặc để mJ khi chia cho kg nên liều lớn gấp nghìn lần."),
  buoc("Liều tương đương của mỗi mẫu", "Liều tương đương của mẫu B (tia alpha) là bao nhiêu mSv?", 80, "mSv", 0.5,
       loi=r"Quên nhân hệ số chất lượng nên $H_B$ bằng $D$, hoặc chia $D$ cho $w_R$ thay vì nhân.",
       ke=[(r"Nhân liều hấp thụ với hệ số chất lượng của tia alpha", True),
           (r"Dùng hệ số chất lượng của tia gamma cho cả hai mẫu", r"Hệ số $w_R$ phụ thuộc loại tia; mẫu B bị chiếu tia alpha nên phải dùng $w_R$ của alpha."),
           (r"Chia liều hấp thụ cho hệ số chất lượng", r"Tia càng gây hại thì $H$ phải lớn hơn $D$; phép chia làm $H$ nhỏ hơn $D$.")]),
  buoc("So sánh tác hại", "Mẫu nào chịu tác hại sinh học lớn hơn, và lớn hơn mấy lần?",
       loi=r"Kết luận theo liều hấp thụ nên cho rằng hai mẫu như nhau, hoặc đảo chiều so sánh.",
       lua_chon=[(r"Mẫu B, gấp 20 lần mẫu A", True),
                 (r"Hai mẫu như nhau, vì cùng liều hấp thụ", r"Cùng liều hấp thụ chưa cùng mức hại: $H=w_R\,D$ nên phải xét loại tia."),
                 (r"Mẫu A, gấp 20 lần mẫu B", r"Đó là kết quả của việc chia cho $w_R$; alpha có $w_R$ lớn hơn gamma nên mẫu B mới là mẫu bị hại nhiều hơn.")],
       ke=[(r"So hai liều tương đương $H_A$ và $H_B$", True),
           (r"So hai liều hấp thụ $D_A$ và $D_B$", r"$D$ không phân biệt loại tia nên không cho biết mẫu nào hại hơn."),
           (r"So khả năng đâm xuyên của hai loại tia", r"Đâm xuyên là tính chất của tia; đại lượng đo mức nguy hiểm sinh học là $H$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đổi khoảng cách tới nguồn điểm</b> → nghĩ tới <b>suất liều ∝ 1/r²</b>, chia theo <b>tỉ số</b> khoảng cách.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tỉ số khoảng cách", "Khoảng cách mới gấp bao nhiêu lần khoảng cách cũ?", 3, None, 0.05,
       loi=r"Lấy hiệu hai khoảng cách thay vì lấy tỉ số, hoặc lấy tỉ số ngược (cũ chia mới)."),
  buoc("Suất liều tại điểm cách 1,5 m", "Suất liều tại điểm cách nguồn 1,5 m là bao nhiêu µSv/h?", 8, "µSv/h", 0.1,
       loi=r"Chia cho tỉ số khoảng cách (chỉ chia một lần) thay vì bình phương, hoặc chia cho bình phương số mét của khoảng cách mới.",
       ke=[(r"Chia suất liều cũ cho bình phương tỉ số khoảng cách", True),
           (r"Chia suất liều cũ cho chính tỉ số khoảng cách", r"Bức xạ trải trên mặt cầu diện tích $4\pi r^2$ nên suất liều giảm theo bình phương, không giảm tỉ lệ nghịch bậc nhất."),
           (r"Chia suất liều cũ cho bình phương khoảng cách mới tính bằng mét", r"Phải chia theo tỉ số khoảng cách mới trên cũ; chia theo số mét làm kết quả phụ thuộc đơn vị đo.")]),
  buoc("Tỉ số suất liều", "Suất liều ban đầu gấp bao nhiêu lần suất liều cần đạt?", 36, None, 0.5,
       loi=r"Lấy hiệu hai suất liều thay vì lấy tỉ số, hoặc lấy tỉ số ngược.",
       ke=[(r"Lấy suất liều ban đầu chia cho suất liều cần đạt", True),
           (r"Lấy suất liều ban đầu trừ suất liều cần đạt", r"Quy luật của suất liều là quy luật tỉ lệ (chia), nên phải lấy tỉ số, không lấy hiệu."),
           (r"Lấy suất liều cần đạt chia cho suất liều ban đầu", r"Tỉ số này nhỏ hơn $1$, còn khoảng cách phải tăng khi suất liều giảm; tỉ số ngược sẽ cho khoảng cách giảm.")]),
  buoc("Khoảng cách cần tìm", "Máy đo phải đặt cách nguồn bao nhiêu mét?", 3, "m", 0.05,
       loi=r"Lấy luôn tỉ số suất liều làm tỉ số khoảng cách, quên khai căn.",
       ke=[(r"Khai căn tỉ số suất liều để được tỉ số khoảng cách, rồi nhân với khoảng cách cũ", True),
           (r"Lấy tỉ số khoảng cách bằng chính tỉ số suất liều", r"Suất liều tỉ lệ nghịch với bình phương khoảng cách, nên tỉ số khoảng cách nhỏ hơn tỉ số suất liều (phải khai căn)."),
           (r"Lấy tỉ số khoảng cách bằng bình phương tỉ số suất liều", r"Làm ngược chiều: bình phương làm số lớn thêm, cho khoảng cách quá lớn và vô lí.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>suất liều, thời gian đứng, liều cho phép</b> → nghĩ tới <b>$H=\dot H\,t$</b> và đổi <b>phút ra giờ</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Suất liều tại chỗ đứng", "Suất liều tại chỗ kỹ thuật viên đứng là bao nhiêu µSv/h?", 40, "µSv/h", 0.5,
       loi=r"Chia cho tỉ số khoảng cách (chỉ chia một lần) thay vì bình phương tỉ số."),
  buoc("Liều trong 12 phút", "Đứng 12 phút thì nhận liều bao nhiêu µSv?", 8, "µSv", 0.1,
       loi=r"Nhân suất liều (tính theo giờ) với số phút mà không đổi ra giờ, nên liều lớn gấp 60 lần.",
       ke=[(r"Đổi 12 phút ra giờ rồi nhân với suất liều", True),
           (r"Nhân suất liều với 12 phút, giữ nguyên số phút", r"Suất liều tính theo giờ; nhân với số phút làm kết quả lớn gấp $60$ lần và sai đơn vị."),
           (r"Chia suất liều cho thời gian đứng", r"Liều tăng theo thời gian đứng: liều bằng suất liều nhân thời gian, không phải suất liều chia thời gian.")]),
  buoc("Thời gian đứng tối đa", "Được đứng tối đa bao nhiêu phút?", 30, "phút", 0.5,
       loi=r"Chia ngược suất liều cho liều cho phép, hoặc quên đổi giờ ra phút.",
       ke=[(r"Lấy liều cho phép chia cho suất liều, rồi đổi giờ ra phút", True),
           (r"Lấy suất liều chia cho liều cho phép", r"Phép chia này cho đơn vị $1/\text{h}$, không phải thời gian; thời gian bằng liều chia suất liều."),
           (r"Lấy liều cho phép nhân với suất liều", r"Đơn vị $\mu\text{Sv}\cdot\mu\text{Sv/h}$ không phải đơn vị thời gian; muốn có giờ phải lấy liều chia suất liều.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nhiều biện pháp giảm liều khác loại</b> → nghĩ tới <b>quy mỗi biện pháp về % liều còn lại</b> rồi so.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Lùi ra xa (A)", "Lùi ra xa 3,0 m thì liều mỗi ca còn bao nhiêu phần trăm so với ban đầu?", 11.1, "%", 0.2,
       loi=r"Chia cho tỉ số khoảng cách (chỉ chia một lần) thay vì bình phương, hoặc đảo tỉ số nên ra phần trăm lớn hơn $100\ \%$."),
  buoc("Rút thời gian (B)", "Rút thời gian còn 10 phút thì liều còn bao nhiêu phần trăm?", 25, "%", 0.3,
       loi=r"Áp bình phương cho thời gian như với khoảng cách, hoặc lấy tỉ số ngược nên ra phần trăm lớn hơn $100\ \%$.",
       ke=[(r"Lấy thời gian mới chia thời gian cũ (liều tỉ lệ thuận với thời gian)", True),
           (r"Lấy bình phương tỉ số thời gian mới trên cũ", r"Chỉ khoảng cách mới có quy luật bình phương; liều tỉ lệ thuận (bậc nhất) với thời gian."),
           (r"Coi liều không đổi vì suất liều vẫn như cũ", r"Liều bằng suất liều nhân thời gian; thời gian ngắn lại thì liều giảm dù suất liều giữ nguyên.")]),
  buoc("Che chắn (C)", "Chèn tấm chì dày 5 mm thì liều còn bao nhiêu phần trăm?", 42.8, "%", 0.3,
       loi=r"Lấy hiệu hai số xung rồi chia cho số xung ban đầu nên được phần trăm đã bị chắn bớt, không phải phần còn lại.",
       ke=[(r"Lấy số xung còn lại chia cho số xung ban đầu", True),
           (r"Lấy hiệu hai số xung rồi chia cho số xung ban đầu", r"Cách này ra phần trăm đã bị chắn bớt, không phải phần trăm còn lại mà đề hỏi."),
           (r"Bình phương tỉ số hai số xung", r"Số xung ghi sau tấm chắn đã phản ánh đúng suất liều còn lại; bình phương chỉ dùng cho khoảng cách.")]),
  buoc("Chọn biện pháp", "Biện pháp nào giảm liều nhiều nhất?",
       loi=r"Chọn chì vì cho rằng chì chắn gamma tốt nhất mà không so số liệu.",
       lua_chon=[(r"A: lùi ra xa 3,0 m", True),
                 (r"B: rút thời gian còn 10 phút", r"Biện pháp B vẫn còn lại nhiều liều hơn A; rút thời gian có ích nhưng ở đây kém hơn lùi xa gấp 3 lần."),
                 (r"C: chèn tấm chì dày 5 mm", r"Chì là vật liệu đúng cho gamma nhưng tấm 5 mm vẫn để lọt gần một nửa số xung, nên còn nhiều liều hơn A và B."),
                 (r"D: chèn tấm nhôm dày 3 mm", r"Nhôm mỏng gần như không chắn gamma, liều còn lại trên $90\ \%$.")],
       ke=[(r"Đặt bốn phần trăm liều còn lại cạnh nhau, chọn số nhỏ nhất", True),
           (r"Chọn tấm chắn bằng chì vì chì chắn gamma tốt nhất", r"Đúng vật liệu chưa đủ: tấm chì mỏng vẫn để lọt nhiều; phải so bằng số liệu."),
           (r"Chọn biện pháp làm giảm nhiều đơn vị nhất trong đề", r"Số phút, số mét, số xung là các đại lượng khác nhau, không so trực tiếp; phải quy về phần trăm liều còn lại.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>giờ làm việc cả năm và giới hạn mSv/năm</b> → nghĩ tới <b>đổi mSv ra µSv</b>, rồi quy ngược về suất liều.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Suất liều tại chỗ làm việc", "Suất liều tại chỗ nhân viên làm việc là bao nhiêu µSv/h?", 40, "µSv/h", 0.5,
       loi=r"Chia cho tỉ số khoảng cách (chỉ chia một lần) thay vì bình phương tỉ số."),
  buoc("Liều cả năm", "Liều nhân viên nhận trong một năm là bao nhiêu mSv?", 80, "mSv", 0.5,
       loi=r"Dùng suất liều tại $1{,}0\ \text{m}$ thay vì tại chỗ làm việc, hoặc quên đổi µSv sang mSv.",
       ke=[(r"Nhân suất liều tại chỗ làm việc với số giờ, rồi đổi µSv sang mSv", True),
           (r"Nhân suất liều tại 1,0 m với số giờ", r"Giá trị cho trước chỉ đúng ở $1{,}0\ \text{m}$; nhân viên đứng ở $2{,}0\ \text{m}$ nên phải dùng suất liều tại chỗ đứng."),
           (r"Nhân suất liều với 365 ngày", r"Đề cho số giờ làm việc trong năm; nhân với số ngày là sai đơn vị và sai thời gian phơi nhiễm.")]),
  buoc("So với giới hạn", "Liều cả năm gấp mấy lần giới hạn nghề nghiệp?", 4, None, 0.05,
       loi=r"Quên đổi mSv ra µSv trước khi chia, hoặc chia ngược giới hạn cho liều cả năm.",
       ke=[(r"Đưa về cùng đơn vị rồi lấy liều cả năm chia cho giới hạn", True),
           (r"So thẳng số µSv với số mSv, không đổi đơn vị", r"$1\ \text{mSv}=1000\ \mu\text{Sv}$; không đổi thì tỉ số lệch hàng nghìn lần."),
           (r"Lấy giới hạn chia cho liều cả năm", r"Tỉ số nhỏ hơn $1$ sẽ dẫn tới kết luận ngược là không vượt giới hạn.")]),
  buoc("Suất liều lớn nhất cho phép", "Suất liều lớn nhất cho phép tại chỗ làm việc là bao nhiêu µSv/h?", 10, "µSv/h", 0.1,
       loi=r"Chia cho 365 thay vì số giờ làm việc, hoặc quên đổi mSv ra µSv trước khi chia.",
       ke=[(r"Lấy giới hạn cả năm (đã đổi ra µSv) chia cho số giờ làm việc", True),
           (r"Lấy giới hạn 20 mSv chia số giờ mà không đổi ra µSv", r"Suất liều tính bằng µSv/h; không đổi mSv ra µSv thì kết quả sai hàng nghìn lần."),
           (r"Lấy giới hạn chia cho 365 ngày", r"Đề cho số giờ; suất liều là liều mỗi giờ nên phải chia cho số giờ làm việc.")]),
  buoc("Khoảng cách tối thiểu", "Nhân viên phải đứng cách nguồn ít nhất bao nhiêu mét?", 4, "m", 0.05,
       loi=r"Lấy tỉ số suất liều làm tỉ số khoảng cách, quên khai căn; hoặc nhân khoảng cách hiện tại với số lần vượt giới hạn.",
       ke=[(r"Khai căn tỉ số hai suất liều (suất liều gốc trên mức cho phép) rồi nhân với khoảng cách gốc", True),
           (r"Nhân khoảng cách hiện tại với số lần liều vượt giới hạn", r"Suất liều giảm theo bình phương khoảng cách, nên số lần phải lùi nhỏ hơn số lần cần giảm liều."),
           (r"Lấy luôn tỉ số suất liều làm khoảng cách tính bằng mét", r"Tỉ số “bao nhiêu lần” khác khoảng cách; phải khai căn và nhân với khoảng cách chuẩn đã biết.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 19, "Bài 18. An toàn phóng xạ", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q in d["dang_bai"]: q["form"] = "ly_thuyet"       # ngân hàng chủ đề này < 6 câu bai_tap, câu tính liều nằm ở form ly_thuyet (xem 19.quet-dang.json)
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
