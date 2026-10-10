"""Bài tập mẫu Bài 27 "Hiệu suất" (Vật lí 10, chương 4) — lesson_id 72. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/72.quet-dang.json). Hình: hinh_72.py. Bài chưa có ví dụ cũ (không có old/72.json) nên không có tự luận.
Số liệu cố ý KHÁC bài toán mẫu và quiz trong lý thuyết (thang máy 300 kg/5 m/20 s/1,25 kW; xe máy 2000/500 kJ; động cơ 5,0/4,0 kW;
máy X/Y; 800/200 J; 90 %·80 %; thang máy 10 s) để học sinh không gặp lại đúng đề đã làm.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-72.py   (idempotent, ghi 72.json với review.checked=false)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_72 import *

J = os.path.join(HERE, "72.json")
T140 = "Tính hiệu suất của máy và động cơ"
T141 = "Hao phí năng lượng và cách giảm hao phí"

# ═════════════ KIỂM SỐ (tự giải lại độc lập với lời giải: lệch thì dừng) ═════════════
def ok(name, got, want, tol=1e-9):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
# D1: máy khoan
Wtp, Wci = 150, 105
ok("D1a", Wtp - Wci, 45)
ok("D1c", Wci + 25, 130)
ok("D1 điện giảm = hao phí giảm", Wtp - 130, (Wtp - Wci) - 25)
assert Wtp + Wci != 45 and Wci != 45                                                 # sai: cộng; lấy phần có ích
assert Wci - 25 != 130 and Wtp - 25 != 130                                           # sai: trừ thay vì cộng; lấy 150 − 25
# D2: máy bơm
Wtp2, Wci2, t2 = 540e3, 405e3, 5 * 60
H2 = Wci2 / Wtp2; Ptp2 = Wtp2 / t2; Pci2 = Wci2 / t2
ok("D2 H", H2 * 100, 75); ok("D2 Ptp", Ptp2, 1800); ok("D2 Pci", Pci2, 1350); ok("D2 H công suất", Pci2 / Ptp2, H2)
assert Wtp2 / 1e3 / 5 != Ptp2 and Wtp2 / 1e3 * t2 != Ptp2                            # sai: chia số phút; nhân
assert Wtp2 / Wci2 > 1 and Ptp2 - Wci2 / 1e3 != Pci2                                 # sai: đảo tử/mẫu
# D3: xe đạp điện
H3 = 0.80
Pci3 = H3 * 250; Wtp3 = 144 / H3; Whp3 = Wtp3 - 144
ok("D3a", Pci3, 200); ok("D3b", Wtp3, 180); ok("D3c", Whp3, 36)
assert 250 / H3 != Pci3 and 144 * H3 != Wtp3 and 144 * 1.2 != Wtp3                    # sai: chia; nhân; +20 % của W_ci
assert 0.2 * 144 != Whp3 and H3 * Wtp3 != Whp3                                       # sai: 20 % của W_ci; H·W_tp
# D4: tời kéo thùng vữa
m4, h4, t4, Ptp4, g = 350, 12, 24, 2500, 10
Wci4 = m4 * g * h4; Pci4 = Wci4 / t4; H4 = Pci4 / Ptp4; Wtp4 = Ptp4 * t4; Whp4 = Wtp4 - Wci4
ok("D4a", Wci4, 42000); ok("D4b P", Pci4, 1750, 1e-9); ok("D4b H", H4 * 100, 70); ok("D4c", Whp4, 18000)
ok("D4 H theo năng lượng", Wci4 / Wtp4, H4)
assert m4 * h4 != Wci4 and Wci4 * t4 != Pci4 and Ptp4 / Pci4 != H4                    # sai: quên g; nhân t; đảo tử/mẫu
assert (Ptp4 - Pci4) != Whp4 and (1 - H4) * Wci4 != Whp4                              # sai: hiệu công suất; (1 − H)·W_ci
# D5: xe điện ba khâu
H5 = 0.95 * 0.80 * 0.75
ok("D5a", H5 * 100, 57, 1e-9); ok("D5b", 5.7 / H5, 10, 1e-9)
opts = {"hộp số": 0.95 * 0.80 * 0.90, "động cơ": 0.95 * 0.90 * 0.75, "bộ điều khiển": 0.90 * 0.80 * 0.75}
assert max(opts, key=opts.get) == "hộp số"
ok("D5c", opts["hộp số"] * 100, 68.4, 1e-9)
assert abs(opts["động cơ"] * 100 - 64.125) < 1e-9 and abs(opts["bộ điều khiển"] * 100 - 54) < 1e-9
assert opts["bộ điều khiển"] < H5 < opts["động cơ"] < opts["hộp số"]
assert abs((0.95 + 0.80 + 0.75) / 3 * 100 - 57) > 1 and abs((0.95 + 0.80 + 0.75) * 100 - 57) > 1   # sai: trung bình; cộng
assert abs(5.7 / 0.75 - 10) > 1 and abs(5.7 * H5 - 10) > 1                                       # sai: chia H khâu cuối; nhân
assert abs((57 + 15) - 68.4) > 1                                                                 # sai: cộng 15 điểm %

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Năng lượng toàn phần, có ích, hao phí", topic=T141,
      problem_html=r"<p>Một máy khoan cầm tay chạy điện, mỗi lần khoan một lỗ nhận điện năng $150\ \text{kJ}$. Trong đó $105\ \text{kJ}$ thành cơ năng quay mũi khoan (phần có ích); phần còn lại làm vỏ máy nóng lên, phát tiếng ồn và rung.</p>"
      r"""<ol type="a"><li>Tính năng lượng hao phí của máy trong một lần khoan.</li><li>Phần năng lượng hao phí ấy đã mất đi hay chuyển sang dạng khác? Nêu các dạng đó.</li><li>Sau khi tra dầu bôi trơn ổ trục, hao phí mỗi lần khoan chỉ còn $25\ \text{kJ}$, cơ năng có ích vẫn $105\ \text{kJ}$. Máy phải nhận bao nhiêu điện năng cho một lần khoan?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Tính hiệu suất theo năng lượng và theo công suất", topic=T140,
      problem_html=r"<p>Một máy bơm nước chạy điện bơm nước từ ao lên bể cao trong $5$ phút. Trong thời gian đó máy nhận điện năng $540\ \text{kJ}$ và truyền cho nước cơ năng $405\ \text{kJ}$.</p>"
      r"""<ol type="a"><li>Tính hiệu suất của máy bơm.</li><li>Tính công suất toàn phần và công suất có ích của máy bơm.</li><li>Dùng hai công suất đó tính lại hiệu suất và so với câu a.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Cho hiệu suất, tìm công suất hoặc năng lượng", topic=T140,
      problem_html=r"<p>Động cơ gắn ở moay-ơ bánh sau của một xe đạp điện có hiệu suất $80\,\%$.</p>"
      r"""<ol type="a"><li>Khi xe chạy, động cơ nhận công suất điện $250\ \text{W}$. Tính công suất cơ học có ích của động cơ.</li><li>Trên một đoạn đường dốc khác, xe cần động cơ sinh công có ích $144\ \text{kJ}$. Động cơ phải nhận bao nhiêu điện năng?</li><li>Tính năng lượng hao phí của động cơ ở câu b.</li></ol>"""),
 dict(label="Dạng 4 · Khá · Hiệu suất của tời kéo vật lên cao", topic=T140,
      problem_html=r"<p>Một tời điện kéo đều một thùng vữa (kể cả vữa) khối lượng $350\ \text{kg}$ từ mặt đất lên tầng cao $12\ \text{m}$ trong $24\ \text{s}$ qua một ròng rọc cố định. Công suất điện mà động cơ tời tiêu thụ là $2{,}5\ \text{kW}$. Bỏ qua khối lượng dây, lấy $g=10\ \text{m/s}^2$.</p>"
      r"""<ol type="a"><li>Tính công có ích mà tời thực hiện.</li><li>Tính công suất có ích và hiệu suất của hệ thống tời.</li><li>Tính phần năng lượng hao phí toả ra (chủ yếu dưới dạng nhiệt) trong thời gian kéo.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Ghép nhiều khâu nối tiếp và giảm hao phí", topic=T141,
      problem_html=r"<p>Hệ truyền động của một xe điện nhỏ gồm ba khâu nối tiếp: điện năng từ pin đi qua bộ điều khiển (hiệu suất $95\,\%$), tới động cơ (hiệu suất $80\,\%$), rồi qua hộp số (hiệu suất $75\,\%$) mới tới bánh xe. Năng lượng ra của khâu trước là năng lượng vào của khâu sau.</p>"
      r"""<ol type="a"><li>Tính hiệu suất của cả hệ truyền động.</li><li>Để bánh xe nhận cơ năng có ích $5{,}7\ \text{kJ}$, pin phải cấp bao nhiêu điện năng?</li><li>Cần chọn một khâu để thay: người ta thay riêng MỘT khâu bằng khâu mới có hiệu suất $90\,\%$. Thay khâu nào thì hiệu suất cả hệ lớn nhất? Tính hiệu suất cả hệ khi đó.</li></ol>"""),
]
BUILD = BUILD  # từ hinh_72

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (hàng "cần tìm" chỉ ghi "Đại lượng cần tìm"; ô ⚠ chỉ nêu câu hỏi điều kiện) ═════════════
ANALYSIS = [
 [(r"“máy khoan … mỗi lần khoan một lỗ nhận điện năng $150\ \text{kJ}$”", r"$W_{tp}=150$ kJ", "Khái niệm: năng lượng toàn phần là năng lượng máy nhận vào"),
  (r"“$105\ \text{kJ}$ thành cơ năng quay mũi khoan (phần có ích)”", r"$W_{ci}=105$ kJ", "Khái niệm: năng lượng có ích là phần thành dạng ta cần"),
  (r"“phần còn lại làm vỏ máy nóng lên, phát tiếng ồn và rung”", "Nhiệt, âm, rung", "⚠ Phần này thuộc loại nào trong ba loại năng lượng của máy?"),
  (r"“a) năng lượng hao phí”", r"Cần $W_{hp}$", "Đại lượng cần tìm"),
  (r"“b) mất đi hay chuyển sang dạng khác”", "Cần nêu các dạng năng lượng", "Định luật: bảo toàn năng lượng"),
  (r"“c) hao phí chỉ còn $25\ \text{kJ}$, cơ năng có ích vẫn $105\ \text{kJ}$”", r"$W_{hp}'=25$ kJ; $W_{ci}=105$ kJ", "⚠ Đại lượng nào đổi, đại lượng nào giữ nguyên? Viết lại công thức nối ba năng lượng cho đại lượng cần tìm."),
  (r"“máy phải nhận bao nhiêu điện năng”", r"Cần $W_{tp}'$", "Đại lượng cần tìm")],
 [(r"“trong $5$ phút”", r"$t=5$ phút $=300$ s", "⚠ Công suất tính bằng W, thời gian dùng đơn vị nào?"),
  (r"“nhận điện năng $540\ \text{kJ}$”", r"$W_{tp}=540$ kJ", "Khái niệm: toàn phần là năng lượng máy nhận vào"),
  (r"“truyền cho nước cơ năng $405\ \text{kJ}$”", r"$W_{ci}=405$ kJ", "Khái niệm: có ích là phần thành cơ năng của nước"),
  (r"“a) hiệu suất của máy bơm”", r"Cần $H$", "Công thức: tỉ số có ích trên toàn phần; kết quả không có đơn vị"),
  (r"“b) công suất toàn phần và công suất có ích”", r"Cần $P_{tp}$ và $P_{ci}$", "Công thức: $P=W/t$"),
  (r"“c) dùng hai công suất tính lại hiệu suất”", r"Cần $H$ lần hai", "⚠ Hai cách tính có cùng khoảng thời gian không? Kết quả hai cách phải thế nào?")],
 [(r"“hiệu suất $80\,\%$”", r"$H=80\,\%=0{,}80$", "⚠ $H$ viết dưới dạng số thập phân hay phần trăm khi đưa vào công thức?"),
  (r"“a) nhận công suất điện $250\ \text{W}$”", r"$P_{tp}=250$ W", "Công thức: hiệu suất theo công suất"),
  (r"“công suất cơ học có ích”", r"Cần $P_{ci}$", "Đại lượng cần tìm"),
  (r"“b) sinh công có ích $144\ \text{kJ}$”", r"$W_{ci}=144$ kJ", "Công thức: hiệu suất theo năng lượng"),
  (r"“phải nhận bao nhiêu điện năng”", r"Cần $W_{tp}$", "⚠ Đề cho phần có ích, hỏi phần toàn phần: đại lượng nào đứng ở mẫu số?"),
  (r"“c) năng lượng hao phí”", r"Cần $W_{hp}$", "Đại lượng cần tìm")],
 [(r"“kéo đều … khối lượng $350\ \text{kg}$ … lên cao $12\ \text{m}$”", r"$m=350$ kg; $h=12$ m", "⚠ Kéo đều thì lực kéo có ích liên hệ với trọng lượng thế nào? Công có ích tính từ những đại lượng nào?"),
  (r"“trong $24\ \text{s}$”", r"$t=24$ s", "Công thức: $P=W/t$"),
  (r"“công suất điện … tiêu thụ là $2{,}5\ \text{kW}$”", r"$P_{tp}=2500$ W (đổi từ kW)", "Khái niệm: công suất toàn phần là công suất máy nhận vào"),
  (r"“lấy $g=10\ \text{m/s}^2$”", r"$g=10$ m/s²", "Công thức: trọng lượng $mg$"),
  (r"“a) công có ích”", r"Cần $W_{ci}$", "Đại lượng cần tìm"),
  (r"“b) công suất có ích và hiệu suất”", r"Cần $P_{ci}$ và $H$", "Công thức: hiệu suất theo công suất"),
  (r"“c) phần năng lượng hao phí … trong thời gian kéo”", r"Cần $W_{hp}$ trong $24$ s", "⚠ Muốn có năng lượng hao phí thì cần biết năng lượng toàn phần trong cùng khoảng thời gian: tính từ đại lượng nào?")],
 [(r"“ba khâu nối tiếp … năng lượng ra của khâu trước là năng lượng vào của khâu sau”", "Ba khâu nối tiếp", "⚠ Hiệu suất cả hệ liên hệ với hiệu suất từng khâu bằng phép tính nào?"),
  (r"“bộ điều khiển $95\,\%$, động cơ $80\,\%$, hộp số $75\,\%$”", r"$H_1=0{,}95$; $H_2=0{,}80$; $H_3=0{,}75$", "Khái niệm: mỗi khâu lấy đi thêm một phần hao phí"),
  (r"“a) hiệu suất của cả hệ”", r"Cần $H$", "Đại lượng cần tìm"),
  (r"“bánh xe nhận cơ năng có ích $5{,}7\ \text{kJ}$”", r"$W_{ci}=5{,}7$ kJ ở cuối hệ", "Khái niệm: có ích là năng lượng ở khâu cuối"),
  (r"“b) pin phải cấp bao nhiêu điện năng”", r"Cần $W_{tp}$ ở đầu hệ", "Công thức: hiệu suất theo năng lượng, áp dụng cho cả hệ"),
  (r"“thay riêng MỘT khâu bằng khâu mới có hiệu suất $90\,\%$”", r"Một trong ba $H$ đổi thành $0{,}90$; hai khâu còn lại giữ nguyên", "⚠ Có mấy khả năng thay?"),
  (r"“c) thay khâu nào … lớn nhất”", r"Cần khâu thay và $H$ mới", "Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> toàn phần $W_{tp}$ là năng lượng máy nhận vào; có ích $W_{ci}$ là phần thành dạng ta cần; hao phí $W_{hp}$ là phần thành nhiệt, âm, rung.",
       r"<strong>Định luật:</strong> năng lượng bảo toàn, hao phí không biến mất mà chuyển sang dạng không dùng được.",
       r"<strong>Công thức:</strong> $W_{tp}=W_{ci}+W_{hp}$.",
       r"⚠ <strong>Điều kiện:</strong> ba năng lượng cùng đơn vị và tính cho cùng một lần máy hoạt động."]
RC2 = [r"<strong>Khái niệm:</strong> hiệu suất cho biết bao nhiêu phần trăm năng lượng nhận vào thành có ích; không có đơn vị.",
       r"<strong>Công thức:</strong> $H=\dfrac{W_{ci}}{W_{tp}}\cdot100\,\%=\dfrac{P_{ci}}{P_{tp}}\cdot100\,\%$ và $P=\dfrac{W}{t}$.",
       r"⚠ <strong>Điều kiện:</strong> tử số là có ích, mẫu số là toàn phần; thời gian đổi ra giây khi tính công suất (W)."]
RC3 = [r"<strong>Khái niệm:</strong> $H$ là tỉ số có ích trên toàn phần nên biết $H$ và một vế thì tìm được vế còn lại.",
       r"<strong>Công thức:</strong> $P_{ci}=H\cdot P_{tp}$ và $W_{tp}=\dfrac{W_{ci}}{H}$; $W_{hp}=W_{tp}-W_{ci}$.",
       r"⚠ <strong>Điều kiện:</strong> đổi $H$ ra số thập phân ($80\,\%=0{,}80$) trước khi thay vào công thức."]
RC4 = [r"<strong>Khái niệm:</strong> kéo đều thì lực kéo có ích bằng trọng lượng của vật; công có ích là công nâng vật lên cao.",
       r"<strong>Công thức:</strong> $W_{ci}=mgh$ · $P=\dfrac{W}{t}$ · $H=\dfrac{P_{ci}}{P_{tp}}$ · $W_{tp}=P_{tp}\,t$ · $W_{hp}=W_{tp}-W_{ci}$.",
       r"⚠ <strong>Điều kiện:</strong> kéo đều (động năng không đổi); kW đổi ra W; $W_{ci}$ và $W_{tp}$ tính trong cùng khoảng thời gian."]
RC5 = [r"<strong>Khái niệm:</strong> ghép nối tiếp thì máy sau nhận năng lượng ra của máy trước; mỗi khâu lấy đi thêm một phần hao phí.",
       r"<strong>Công thức:</strong> $H=H_1\cdot H_2\cdot H_3$ (đổi mỗi $H$ ra số thập phân) · $W_{tp}=\dfrac{W_{ci}}{H}$.",
       r"⚠ <strong>Điều kiện:</strong> nhân các hiệu suất, không cộng; muốn so sánh các phương án phải tính lại cả tích cho từng phương án."]

SOLS = [
 sol(RC1, [
  ("Năng lượng hao phí", [P("Toàn phần bằng có ích cộng hao phí, suy ra hao phí bằng toàn phần trừ có ích:"), M(r"W_{hp}=W_{tp}-W_{ci}"), M(r"W_{hp}=150-105"), A(r"W_{hp}=45\ \text{kJ}")]),
  ("Hao phí đi đâu", [A("T:Hao phí <strong>không mất đi</strong>. Nó chuyển thành <strong>nhiệt</strong> (vỏ máy nóng lên), <strong>âm</strong> (tiếng ồn) và <strong>rung</strong>: những dạng không dùng được vào việc khoan. Tổng năng lượng vẫn bảo toàn.")]),
  ("Điện năng khi hao phí giảm", [P(r"Cơ năng có ích giữ nguyên, hao phí mới $W_{hp}'=25\ \text{kJ}$:"), M(r"W_{tp}'=W_{ci}+W_{hp}'"), M(r"W_{tp}'=105+25"), A(r"W_{tp}'=130\ \text{kJ}")]),
  ("Kiểm tra", [P(r"Điện năng giảm $150-130=20\ \text{kJ}$, đúng bằng hao phí giảm $45-25=20\ \text{kJ}$ ✓"), P(r"Cơ năng có ích vẫn $105\ \text{kJ}$ ✓")])],
  [r"a) $W_{hp}=45\ \text{kJ}$", "b) Hao phí không mất đi: chuyển thành nhiệt, âm, rung", r"c) $W_{tp}'=130\ \text{kJ}$"],
  r"Nhận dạng: đề cho <strong>năng lượng nhận vào</strong> và <strong>phần thành cơ năng</strong> → $W_{tp}=W_{ci}+W_{hp}$, đại lượng nào chưa biết thì rút từ công thức đó."),
 sol(RC2, [
  ("Hiệu suất theo năng lượng", [P(r"Có ích chia toàn phần (cùng đơn vị kJ):"), M(r"H=\dfrac{W_{ci}}{W_{tp}}\cdot100\,\%"), M(r"H=\dfrac{405}{540}\cdot100\,\%"), A(r"H=75\,\%")]),
  ("Công suất toàn phần", [P(r"Đổi $t=5\ \text{phút}=300\ \text{s}$ rồi chia năng lượng cho thời gian:"), M(r"P_{tp}=\dfrac{W_{tp}}{t}"), M(r"P_{tp}=\dfrac{540\,000}{300}"), A(r"P_{tp}=1800\ \text{W}")]),
  ("Công suất có ích", [P("Cùng khoảng thời gian $300\\ \\text{s}$:"), M(r"P_{ci}=\dfrac{W_{ci}}{t}"), M(r"P_{ci}=\dfrac{405\,000}{300}"), A(r"P_{ci}=1350\ \text{W}")]),
  ("Kiểm tra", [P("Tính lại hiệu suất theo công suất:"), M(r"H=\dfrac{P_{ci}}{P_{tp}}=\dfrac{1350}{1800}=0{,}75"), P(r"Trùng kết quả bước 1 vì cùng thời gian $t$ ✓; $H$ nhỏ hơn $100\,\%$ ✓")])],
  [r"a) $H=75\,\%$", r"b) $P_{tp}=1800\ \text{W}$; $P_{ci}=1350\ \text{W}$", r"c) $H=75\,\%$, trùng câu a"],
  r"Nhận dạng: đề cho <strong>năng lượng nhận vào</strong> và <strong>năng lượng có ích</strong> → $H=W_{ci}/W_{tp}$; muốn công suất thì chia cho thời gian đã đổi ra giây."),
 sol(RC3, [
  ("Công suất có ích", [P(r"Đổi $H=80\,\%=0{,}80$ rồi nhân với công suất toàn phần:"), M(r"P_{ci}=H\cdot P_{tp}"), M(r"P_{ci}=0{,}80\cdot250"), A(r"P_{ci}=200\ \text{W}")]),
  ("Điện năng phải nhận", [P(r"Từ $H=\dfrac{W_{ci}}{W_{tp}}$ suy ra toàn phần bằng có ích chia hiệu suất:"), M(r"W_{tp}=\dfrac{W_{ci}}{H}"), M(r"W_{tp}=\dfrac{144}{0{,}80}"), A(r"W_{tp}=180\ \text{kJ}")]),
  ("Năng lượng hao phí", [M(r"W_{hp}=W_{tp}-W_{ci}"), M(r"W_{hp}=180-144"), A(r"W_{hp}=36\ \text{kJ}")]),
  ("Kiểm tra", [P(r"Hao phí chiếm $\dfrac{36}{180}=20\,\%$ năng lượng nhận vào, đúng bằng $100\,\%-80\,\%$ ✓"), P(r"Dùng lại công thức: $\dfrac{144}{180}=0{,}80$ ✓")])],
  [r"a) $P_{ci}=200\ \text{W}$", r"b) $W_{tp}=180\ \text{kJ}$", r"c) $W_{hp}=36\ \text{kJ}$"],
  r"Nhận dạng: đề cho <strong>hiệu suất</strong> và <strong>một trong hai vế (có ích hoặc toàn phần)</strong> → rút vế còn lại từ $H$; đã biết có ích mà tìm toàn phần thì <strong>chia</strong> cho $H$."),
 sol(RC4, [
  ("Công có ích", [P(r"Kéo đều nên lực kéo có ích bằng trọng lượng $mg$:"), M(r"W_{ci}=mgh"), M(r"W_{ci}=350\cdot10\cdot12"), A(r"W_{ci}=42\,000\ \text{J}=42\ \text{kJ}")]),
  ("Công suất có ích", [M(r"P_{ci}=\dfrac{W_{ci}}{t}"), M(r"P_{ci}=\dfrac{42\,000}{24}"), A(r"P_{ci}=1750\ \text{W}")]),
  ("Hiệu suất", [P(r"Đổi $P_{tp}=2{,}5\ \text{kW}=2500\ \text{W}$:"), M(r"H=\dfrac{P_{ci}}{P_{tp}}\cdot100\,\%"), M(r"H=\dfrac{1750}{2500}\cdot100\,\%"), A(r"H=70\,\%")]),
  ("Năng lượng hao phí", [P(r"Điện năng tiêu thụ trong $24\ \text{s}$:"), M(r"W_{tp}=P_{tp}\,t=2500\cdot24=60\,000\ \text{J}"), P("Hao phí là phần điện năng không thành công có ích:"), M(r"W_{hp}=W_{tp}-W_{ci}=60\,000-42\,000"), A(r"W_{hp}=18\,000\ \text{J}=18\ \text{kJ}")]),
  ("Kiểm tra", [P(r"Hiệu suất tính theo năng lượng: $\dfrac{42}{60}=0{,}70$, trùng bước 3 ✓"), P(r"$H\lt100\,\%$ ✓; đơn vị công suất là W, đơn vị năng lượng là J ✓")])],
  [r"a) $W_{ci}=42\ \text{kJ}$", r"b) $P_{ci}=1750\ \text{W}$; $H=70\,\%$", r"c) $W_{hp}=18\ \text{kJ}$"],
  r"Nhận dạng: đề cho <strong>khối lượng, độ cao, thời gian</strong> và <strong>công suất điện</strong> → tự tính $W_{ci}=mgh$, $P_{ci}=W_{ci}/t$ rồi mới lập $H=P_{ci}/P_{tp}$."),
 sol(RC5, [
  ("Hiệu suất cả hệ", [P(r"Đổi mỗi hiệu suất ra số thập phân rồi nhân:"), M(r"H=H_1\cdot H_2\cdot H_3"), M(r"H=0{,}95\cdot0{,}80\cdot0{,}75"), A(r"H=0{,}57=57\,\%")]),
  ("Điện năng pin phải cấp", [P(r"Cơ năng có ích ở cuối hệ chia cho hiệu suất cả hệ:"), M(r"W_{tp}=\dfrac{W_{ci}}{H}"), M(r"W_{tp}=\dfrac{5{,}7}{0{,}57}"), A(r"W_{tp}=10\ \text{kJ}")]),
  ("Chọn khâu thay", [P(r"Thay riêng từng khâu bằng khâu $90\,\%$, giữ hai khâu còn lại, tính lại tích:"),
                     M(r"\text{thay bộ điều khiển: }0{,}90\cdot0{,}80\cdot0{,}75=0{,}540"), M(r"\text{thay động cơ: }0{,}95\cdot0{,}90\cdot0{,}75\approx0{,}641"), M(r"\text{thay hộp số: }0{,}95\cdot0{,}80\cdot0{,}90=0{,}684"),
                     A(r"T:Thay <strong>hộp số</strong> (khâu có hiệu suất thấp nhất) cho hiệu suất cả hệ lớn nhất.")]),
  ("Hiệu suất cả hệ sau khi thay", [P(r"Thay hộp số $75\,\%$ bằng khâu $90\,\%$:"), M(r"H'=0{,}95\cdot0{,}80\cdot0{,}90"), A(r"H'=0{,}684=68{,}4\,\%")]),
  ("Kiểm tra", [P(r"Thay bộ điều khiển ($95\,\%\to90\,\%$) làm hệ kém đi: $0{,}540\lt0{,}57$ ✓"), P(r"Hiệu suất cả hệ luôn nhỏ hơn hiệu suất của mỗi khâu: $0{,}684\lt0{,}80$ ✓"), P(r"Hao phí cả hệ giảm từ $43\,\%$ xuống $31{,}6\,\%$ điện năng pin ✓")])],
  [r"a) $H=57\,\%$", r"b) $W_{tp}=10\ \text{kJ}$", r"c) Thay hộp số; $H'=68{,}4\,\%$"],
  r"Nhận dạng: đề cho <strong>nhiều khâu nối tiếp</strong> và hỏi <strong>thay khâu nào có lợi nhất</strong> → nhân các hiệu suất, tính lại tích cho từng phương án rồi so sánh."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>năng lượng nhận vào</b> và <b>phần thành cơ năng</b> → nghĩ tới <b>W_tp = W_ci + W_hp</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Năng lượng hao phí", r"Năng lượng hao phí $W_{hp}$ trong một lần khoan bằng bao nhiêu $\text{kJ}$?", 45, "kJ", 0.5,
       loi=r"Cộng hai số đã cho thay vì lấy toàn phần trừ có ích, hoặc lấy luôn phần có ích làm hao phí."),
  buoc("Hao phí đi đâu", "Phần năng lượng hao phí đã đi đâu?",
       loi=r"Cho rằng phần không dùng được thì biến mất, trong khi năng lượng chỉ đổi dạng.",
       lua_chon=[(r"Chuyển thành nhiệt, âm, rung", True),
                 (r"Biến mất, vì máy không dùng tới nó", r"Năng lượng không tự mất đi; nó chuyển sang dạng khác. Đó là nội dung định luật bảo toàn năng lượng."),
                 (r"Quay trở lại thành điện năng trong dây dẫn", r"Nhiệt và âm toả ra môi trường, không tự quay lại thành điện năng.")]),
  buoc("Điện năng khi hao phí giảm", r"Hao phí chỉ còn $25\ \text{kJ}$, cơ năng có ích vẫn như cũ. Máy phải nhận bao nhiêu $\text{kJ}$ điện năng?", 130, "kJ", 0.5,
       loi=r"Lấy cơ năng có ích trừ hao phí mới thay vì cộng, hoặc cộng nhầm với hao phí cũ.",
       ke=[(r"Cộng cơ năng có ích với hao phí mới", True),
           (r"Lấy cơ năng có ích trừ hao phí mới", r"Toàn phần gồm cả có ích và hao phí nên phải cộng, không trừ."),
           (r"Giữ nguyên điện năng ban đầu vì cơ năng có ích không đổi", r"Hao phí đã thay đổi mà có ích không đổi thì toàn phần phải đổi theo công thức $W_{tp}=W_{ci}+W_{hp}$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>năng lượng nhận vào</b> và <b>năng lượng có ích</b> → nghĩ tới <b>H = W_ci / W_tp</b>.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Hiệu suất theo năng lượng", r"Hiệu suất $H$ của máy bơm bằng bao nhiêu phần trăm?", 75, "%", 0.5,
       loi=r"Đảo tử số và mẫu số (toàn phần chia có ích), hoặc quên nhân $100\,\%$."),
  buoc("Công suất toàn phần", r"Công suất toàn phần $P_{tp}$ của máy bơm bằng bao nhiêu $\text{W}$?", 1800, "W", 10,
       loi=r"Chia năng lượng cho số phút thay vì số giây, nên kết quả lệch $60$ lần.",
       ke=[(r"Chia điện năng cho thời gian đã đổi ra giây", True),
           (r"Chia điện năng cho số phút rồi ghi đơn vị W", r"Công suất tính bằng W là J chia cho s; chia cho phút thì sai đơn vị."),
           (r"Nhân điện năng với thời gian", r"Nhân ra đơn vị kJ·s, không phải đơn vị công suất; công suất là năng lượng chia thời gian.")]),
  buoc("Công suất có ích", r"Công suất có ích $P_{ci}$ của máy bơm bằng bao nhiêu $\text{W}$?", 1350, "W", 10,
       loi=r"Lấy công suất toàn phần trừ năng lượng có ích (khác loại đại lượng), hoặc dùng thời gian tính bằng phút.",
       ke=[(r"Chia năng lượng có ích cho thời gian đã đổi ra giây", True),
           (r"Lấy công suất toàn phần trừ năng lượng có ích", r"Hai đại lượng khác loại (W và J) nên không trừ cho nhau được."),
           (r"Chia năng lượng có ích cho công suất toàn phần", r"Phép chia này ra một khoảng thời gian (đơn vị s), không phải công suất.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hiệu suất cho sẵn</b> và <b>một vế (có ích hoặc toàn phần)</b> → nghĩ tới <b>rút vế còn lại từ H</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Công suất có ích", r"Công suất có ích $P_{ci}$ của động cơ bằng bao nhiêu $\text{W}$?", 200, "W", 1,
       loi=r"Chia công suất điện cho hiệu suất thay vì nhân, hoặc đưa $80$ vào công thức mà không đổi ra số thập phân."),
  buoc("Điện năng phải nhận", r"Động cơ phải nhận điện năng $W_{tp}$ bằng bao nhiêu $\text{kJ}$ để sinh công có ích đã cho?", 180, "kJ", 1,
       loi=r"Nhân công có ích với hiệu suất thay vì chia, hoặc cộng thêm một phần trăm của công có ích.",
       ke=[(r"Chia công có ích cho hiệu suất (đã đổi ra số thập phân)", True),
           (r"Nhân công có ích với hiệu suất", r"Phép nhân là chiều ngược lại: tính phần có ích từ phần toàn phần. Ở đây đã biết phần có ích, cần tìm toàn phần."),
           (r"Cộng thêm $20\,\%$ của công có ích vào công có ích", r"$20\,\%$ là tỉ lệ hao phí so với toàn phần, không phải so với công có ích.")]),
  buoc("Năng lượng hao phí", r"Năng lượng hao phí $W_{hp}$ của động cơ ở câu b bằng bao nhiêu $\text{kJ}$?", 36, "kJ", 0.5,
       loi=r"Lấy $20\,\%$ của công có ích, hoặc lấy hiệu suất nhân điện năng (ra phần có ích).",
       ke=[(r"Lấy năng lượng toàn phần trừ năng lượng có ích", True),
           (r"Lấy $20\,\%$ của công có ích", r"$20\,\%$ là tỉ lệ so với năng lượng toàn phần, không phải so với công có ích."),
           (r"Lấy hiệu suất nhân với điện năng nhận vào", r"Hiệu suất nhân điện năng cho ra phần có ích, không phải hao phí.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>khối lượng, độ cao, thời gian</b> và <b>công suất điện</b> → nghĩ tới <b>tự tính W_ci = mgh</b> rồi lập H.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Công có ích", r"Công có ích $W_{ci}$ của tời bằng bao nhiêu $\text{kJ}$?", 42, "kJ", 0.5,
       loi=r"Quên nhân gia tốc rơi tự do $g$ (lấy $mh$), hoặc nhân thêm thời gian."),
  buoc("Công suất có ích", r"Công suất có ích $P_{ci}$ của tời bằng bao nhiêu $\text{W}$?", 1750, "W", 10,
       loi=r"Nhân công với thời gian thay vì chia, hoặc để công tính bằng kJ mà chia ra kW rồi ghi W.",
       ke=[(r"Chia công có ích cho thời gian kéo", True),
           (r"Nhân công có ích với thời gian kéo", r"Phép nhân cho đơn vị J·s, không phải W."),
           (r"Chia công có ích cho khối lượng thùng", r"Kết quả có đơn vị J/kg, không phải công suất.")]),
  buoc("Hiệu suất", r"Hiệu suất $H$ của hệ thống tời bằng bao nhiêu phần trăm?", 70, "%", 0.5,
       loi=r"Đảo tử số và mẫu số, hoặc quên đổi $\text{kW}$ ra $\text{W}$ nên hai công suất khác đơn vị.",
       ke=[(r"Chia công suất có ích cho công suất điện tiêu thụ (cùng đơn vị W)", True),
           (r"Chia công suất điện tiêu thụ cho công suất có ích", r"Tử số và mẫu số bị đảo: máy thật không thể có hiệu suất trên $100\,\%$."),
           (r"Lấy công suất điện trừ công suất có ích", r"Hiệu đó là công suất hao phí (đơn vị W). Hiệu suất là một tỉ số, không có đơn vị.")]),
  buoc("Năng lượng hao phí", r"Năng lượng hao phí $W_{hp}$ trong thời gian kéo bằng bao nhiêu $\text{kJ}$?", 18, "kJ", 0.3,
       loi=r"Lấy hiệu hai công suất rồi ghi kJ (quên nhân thời gian), hoặc nhân $(1-H)$ với công có ích thay vì với điện năng tiêu thụ.",
       ke=[(r"Tính điện năng tiêu thụ trong thời gian kéo rồi trừ công có ích", True),
           (r"Lấy công suất điện trừ công suất có ích rồi ghi kJ", r"Hiệu hai công suất là công suất hao phí (W). Muốn có năng lượng phải nhân với thời gian."),
           (r"Nhân tỉ lệ hao phí $(1-H)$ với công có ích", r"Tỉ lệ hao phí $(1-H)$ tính so với năng lượng toàn phần; công có ích chưa phải toàn phần.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nhiều khâu nối tiếp</b> → nghĩ tới <b>nhân các hiệu suất</b>; so sánh phương án thì tính lại tích từng phương án.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Hiệu suất cả hệ", r"Hiệu suất của cả hệ truyền động bằng bao nhiêu phần trăm?", 57, "%", 0.3,
       loi=r"Lấy trung bình ba hiệu suất, hoặc cộng ba hiệu suất rồi thấy vượt quá $100\,\%$ mà vẫn ghi kết quả."),
  buoc("Điện năng pin phải cấp", r"Pin phải cấp điện năng bằng bao nhiêu $\text{kJ}$ để bánh xe nhận cơ năng có ích đã cho?", 10, "kJ", 0.1,
       loi=r"Chia cơ năng có ích cho hiệu suất của riêng khâu cuối, hoặc nhân thay vì chia.",
       ke=[(r"Chia cơ năng có ích ở bánh xe cho hiệu suất cả hệ", True),
           (r"Chia cơ năng có ích cho hiệu suất của khâu cuối (hộp số)", r"Hộp số chỉ nhận phần năng lượng đã qua hai khâu trước. Năng lượng toàn phần của pin ứng với hiệu suất cả hệ."),
           (r"Nhân cơ năng có ích với hiệu suất cả hệ", r"Phép nhân là chiều từ pin ra bánh xe. Ở đây đã biết đầu ra, cần tìm đầu vào.")]),
  buoc("Chọn khâu thay", r"Thay riêng một khâu bằng khâu mới có hiệu suất $90\,\%$: thay khâu nào thì hiệu suất cả hệ lớn nhất?",
       loi=r"Thay ngay khâu đầu tiên trong danh sách mà không so sánh các phương án.",
       lua_chon=[(r"Thay hộp số (khâu $75\,\%$)", True),
                 (r"Thay động cơ (khâu $80\,\%$)", r"Thay động cơ thì tích là $0{,}95\cdot0{,}90\cdot0{,}75\approx0{,}641$, vẫn thấp hơn so với khi thay khâu $75\,\%$."),
                 (r"Thay bộ điều khiển (khâu $95\,\%$)", r"Khâu mới ($90\,\%$) kém hơn khâu cũ ($95\,\%$), thay vào chỉ làm hệ tệ đi.")],
       ke=[(r"Tính hiệu suất cả hệ cho từng trường hợp thay một khâu rồi so sánh", True),
           (r"Thay ngay khâu đầu tiên trong danh sách, không so sánh các phương án", r"Khâu đầu tiên đã có hiệu suất cao hơn khâu mới, thay vào chỉ làm hệ kém đi. Chưa so sánh thì chưa biết khâu nào đáng thay."),
           (r"Thay khâu nào cũng được vì hệ chỉ là một phép nhân", r"Ba thừa số khác nhau nên thay thừa số nào thì tích cũng khác nhau.")]),
  buoc("Hiệu suất cả hệ sau khi thay", r"Hiệu suất cả hệ sau khi thay khâu đã chọn bằng bao nhiêu phần trăm?", 68.4, "%", 0.2,
       loi=r"Cộng thêm phần tăng của khâu được thay vào hiệu suất cả hệ cũ, thay vì nhân lại các hiệu suất.",
       ke=[(r"Nhân lại ba hiệu suất, trong đó khâu đã chọn nhận giá trị mới", True),
           (r"Cộng phần tăng của khâu thay vào hiệu suất cả hệ cũ", r"Hiệu suất ghép là một tích; khâu tăng bao nhiêu điểm phần trăm thì cả hệ không tăng bấy nhiêu điểm."),
           (r"Lấy hiệu suất khâu mới làm hiệu suất cả hệ", r"Cả hệ còn hai khâu kia, mỗi khâu vẫn lấy đi một phần hao phí.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 72, "Bài 27. Hiệu suất", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
