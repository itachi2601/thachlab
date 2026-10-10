"""Bài 68 — "Bài 23. Năng lượng. Công cơ học" (Vật lí 10, chương 4). 5 dạng, KHÔNG có tự luận (bài chưa có ví dụ cũ).
Mẫu: build-hinh-58.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-68.py  → ghi scripts/data/bai-tap-mau/68.json
Dạng lấy từ quét: scripts/logs/batch-ra-soat/ket-qua/68.quet-dang.json (cấp 1,1,2,2,3). Hình: hinh_68.py (vec_luc, tỉ lệ độ dài = k·F).
Ký hiệu theo lý thuyết bài: A = F s cosα (α giữa lực và độ dịch chuyển), A_P = ±Ph, A_ms = −F_ms·s, g = 10 m/s²."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_68 import BUILD

J = os.path.join(HERE, "68.json")
T133, T132 = "Định luật bảo toàn và chuyển hoá năng lượng", "Công của lực và trường hợp lực xiên góc"

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
cosd = lambda a: math.cos(math.radians(a)); sind = lambda a: math.sin(math.radians(a))
# D1: bảo toàn năng lượng
Ein, Ek = 300.0, 240.0
ok("D1b", Ein - Ek, 60, 1e-9); ok("D1c", (Ein - Ek) * 20, 1200, 1e-9)
ok("D1 kiểm tra 1 s", Ek + 60, Ein, 1e-9); ok("D1 kiểm tra 20 s", Ek * 20 + 1200, Ein * 20, 1e-9)
assert (Ein + Ek) != 60 and Ein / Ek != 60                    # cách sai (cộng, chia) cho kết quả khác
# D2: xe đi đều
F, s = 25.0, 12.0
ok("D2a", F * s * cosd(0), 300, 1e-9); Fc = F                    # đều → F_c = F
ok("D2b", Fc * s * cosd(180), -300, 1e-9); ok("D2c", F * s * cosd(0) + Fc * s * cosd(180), 0, 1e-9)
assert F * s != -300 and abs(F * s * sind(0)) < 1e-9          # cách sai: A_c dương; dùng sin
# D3: F = 70 N, s = 8,0 m
F, s = 70.0, 8.0
ok("D3a", F * s * cosd(60), 280, 1e-9); ok("D3b", F * s * cosd(90), 0, 1e-9); ok("D3c", F * s * cosd(120), -280, 1e-9)
assert abs(F * s * sind(60) - 280) > 100 and abs(F * s - 280) > 100  # sin hoặc bỏ cos cho kết quả khác
# D4: thùng 40 kg, dốc 30°, s = 6,0 m, F_ms = 40 N
m, g, th, s, Fms = 40.0, 10.0, 30.0, 6.0, 40.0
Pw = m * g; h = s * sind(th)
ok("D4 Pw", Pw, 400, 1e-9); ok("D4 h", h, 3.0, 1e-9); ok("D4 A_P lên", -Pw * h, -1200, 1e-9)
ok("D4 A_ms lên", -Fms * s, -240, 1e-9); ok("D4 A_P xuống", Pw * h, 1200, 1e-9); ok("D4 A_ms xuống", -Fms * s, -240, 1e-9)
ok("D4 cả vòng A_P", -Pw * h + Pw * h, 0, 1e-9); ok("D4 cả vòng A_ms", -Fms * s * 2, -480, 1e-9)
assert abs(-Pw * s - (-Pw * h)) > 100 and abs(Fms * h - Fms * s) > 50  # dùng s thay h (hoặc ngược lại) cho kết quả khác
assert g * sind(th) - Fms / m > 0                             # thùng thật sự trượt xuống được (a = 4 m/s²)
# D5: thùng 25 kg, F = 100 N chếch lên 30°, μ = 0,20, s = 12 m
m, F, al, mu, s = 25.0, 100.0, 30.0, 0.20, 12.0
Pw = m * g; N = Pw - F * sind(al); Fms = mu * N
ok("D5 Pw", Pw, 250, 1e-9); ok("D5 N", N, 200, 1e-9); ok("D5 F_ms", Fms, 40, 1e-9)
AF = F * s * cosd(al); Ams = -Fms * s
ok("D5 A_F", AF, 1039, 0.5); ok("D5 A_ms", Ams, -480, 1e-9)
ok("D5 A_P", Pw * s * cosd(90), 0, 1e-9); ok("D5 A_N", N * s * cosd(90), 0, 1e-9)
ok("D5 tổng", AF + Ams, 559, 0.5); ok("D5 tổng (cộng số đã làm tròn)", 1039 - 480, 559, 1e-9)
assert abs(mu * Pw - Fms) > 5 and abs(-mu * Pw * s - Ams) > 50       # sai: dùng N = Pw
assert abs(F * s * sind(al) - AF) > 100 and abs((F - Fms) * s - (AF + Ams)) > 100
a5 = (AF / s - Fms) / m
assert a5 > 0

# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Chuyển hoá và bảo toàn năng lượng: tính phần năng lượng còn lại", topic=T133,
      problem_html=r"""<p>Một máy xay sinh tố nhận điện năng từ ổ cắm với tốc độ $300\ \text{J}$ mỗi giây. Trong mỗi giây, lưỡi dao và hoa quả nhận động năng $240\ \text{J}$; phần còn lại làm nóng động cơ và phát ra tiếng ồn.</p>
<ol type="a"><li>Khi máy chạy, điện năng chuyển hoá thành những dạng năng lượng nào?</li>
<li>Tính phần năng lượng biến thành nhiệt năng và âm thanh trong mỗi giây.</li>
<li>Máy chạy liên tục $20\ \text{s}$. Tính phần năng lượng biến thành nhiệt năng và âm thanh trong thời gian đó.</li>
<li>Bạn An nói: “Tắt máy rồi thì phần năng lượng ấy đã mất hẳn.” Nhận xét câu nói của An.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Công của lực cùng phương với dịch chuyển, đơn vị jun", topic=T132,
      problem_html=r"""<p>Nam đẩy một xe chở hàng trong siêu thị đi thẳng đều quãng đường $12\ \text{m}$ trên sàn nằm ngang. Lực đẩy có độ lớn $25\ \text{N}$, hướng theo chiều chuyển động của xe. Sàn tác dụng lên xe một lực cản dọc đường đi.</p>
<ol type="a"><li>Tính công của lực đẩy.</li>
<li>Tính công của lực cản.</li>
<li>Tính tổng công của hai lực này.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Công của lực xiên góc và dấu của công", topic=T132,
      problem_html=r"""<p>Một thùng đồ trượt thẳng $8{,}0\ \text{m}$ trên sàn nằm ngang. Trong ba tình huống dưới đây, lực $\vec F$ tác dụng lên thùng đều có độ lớn $F=70\ \text{N}$ nhưng khác hướng:</p>
<ol type="a"><li>$\vec F$ hợp với hướng chuyển động góc $60^\circ$;</li>
<li>$\vec F$ thẳng đứng, hướng lên;</li>
<li>$\vec F$ hợp với hướng chuyển động góc $120^\circ$.</li></ol>
<p>Tính công của $\vec F$ trong từng tình huống và cho biết đó là công phát động, công cản hay lực không sinh công.</p>"""),
 dict(label="Dạng 4 · Trung bình · Công của trọng lực (lên, xuống dốc) và của lực ma sát", topic=T132,
      problem_html=r"""<p>Công nhân kéo đều một thùng hàng khối lượng $40\ \text{kg}$ lên theo mặt dốc nghiêng $30^\circ$ so với phương ngang, đi được $6{,}0\ \text{m}$ dọc mặt dốc thì dừng. Lực ma sát trượt giữa thùng và dốc có độ lớn $40\ \text{N}$. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính độ cao thùng được nâng lên và công của trọng lực trong lúc kéo lên.</li>
<li>Tính công của lực ma sát trong lúc kéo lên.</li>
<li>Công nhân buông tay, thùng trượt xuống đúng $6{,}0\ \text{m}$ dọc dốc về chỗ cũ (lực ma sát vẫn là $40\ \text{N}$). Tính công của trọng lực và công của lực ma sát trong lúc trượt xuống.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Nhiều lực trên mặt phẳng: tìm phản lực N, lực ma sát rồi công từng lực", topic=T132,
      problem_html=r"""<p>Trên nền kho nằm ngang, một người kéo thùng khối lượng $25\ \text{kg}$ bằng sợi dây chếch lên, hợp với phương ngang góc $30^\circ$, lực kéo có độ lớn $100\ \text{N}$. Thùng đi thẳng $12\ \text{m}$. Hệ số ma sát trượt giữa thùng và nền là $0{,}20$. Lấy $g=10\ \text{m/s}^2$.</p>
<p>Tính công của lực kéo, của trọng lực, của phản lực và của lực ma sát, rồi tính tổng công của các lực đó.</p>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“Một máy xay sinh tố nhận điện năng từ ổ cắm …”", r"Máy là nơi năng lượng đổi dạng", r"⚠ Phải tính đủ mọi dạng năng lượng sinh ra, kể cả nhiệt năng và âm thanh lan ra môi trường"),
  (r"“tốc độ $300$ J mỗi giây”", r"Điện năng vào: $300\ \text{J}$ mỗi giây", r"Năng lượng đo bằng jun (J); điện năng truyền từ ổ cắm sang máy"),
  (r"“lưỡi dao và hoa quả nhận động năng $240$ J”", r"Động năng: $240\ \text{J}$ mỗi giây", r"Động năng là năng lượng do chuyển động"),
  (r"“phần còn lại làm nóng động cơ và phát ra tiếng ồn”", r"Nhiệt năng và âm thanh", r"Năng lượng chuyển hoá từ dạng này sang dạng khác"),
  (r"“a) … những dạng năng lượng nào?”", r"Cần liệt kê các dạng", r"Đại lượng cần tìm"),
  (r"“b) trong mỗi giây”", r"Cần $E$ (J) trong $1\ \text{s}$", r"Năng lượng vào, năng lượng ra"),
  (r"“c) máy chạy liên tục $20$ s”", r"$t=20\ \text{s}$", r"Năng lượng tích luỹ tỉ lệ với thời gian máy chạy"),
  (r"“d) … phần năng lượng ấy đã mất hẳn”", r"Nhận định cần kiểm tra", r"Năng lượng sau khi tắt máy")],
 [(r"“đi thẳng đều quãng đường $12$ m trên sàn nằm ngang”", r"$s=12\ \text{m}$; chuyển động thẳng đều", r"⚠ Chuyển động thẳng đều: hợp lực lên xe bằng $\vec 0$ (định luật I Newton)"),
  (r"“lực đẩy có độ lớn $25$ N, hướng theo chiều chuyển động”", r"$F=25\ \text{N}$; lực và dịch chuyển cùng phương", r"⚠ $A=Fs$ chỉ dùng khi lực cùng hướng dịch chuyển; hướng khác thì có $\cos\alpha$"),
  (r"“Sàn tác dụng lên xe một lực cản dọc đường đi”", r"$F_c=\,?$", r"Lực cản có tác dụng gì với chuyển động của xe"),
  (r"“a) công của lực đẩy”", r"Cần $A_{\text{đẩy}}$ (J)", r"Đại lượng cần tìm: $A=Fs\cos\alpha$"),
  (r"“b) công của lực cản”", r"Cần $A_c$ (J)", r"Góc giữa lực cản và dịch chuyển quyết định dấu của công"),
  (r"“c) tổng công của hai lực”", r"Cần $A$ (J)", r"Công là đại lượng vô hướng, các công cộng đại số với nhau")],
 [(r"“trượt thẳng $8{,}0$ m trên sàn nằm ngang”", r"$s=8{,}0\ \text{m}$; đường đi nằm ngang", r"⚠ Vật đi thẳng một chiều nên $d=s$"),
  (r"“lực $\vec F$ … độ lớn $F=70$ N nhưng khác hướng”", r"$F=70\ \text{N}$ không đổi", r"Công phụ thuộc cả $F$, $s$ và góc giữa lực với đường đi"),
  (r"“a) hợp với hướng chuyển động góc $60^\circ$”", r"$\alpha=60^\circ$", r"⚠ $\alpha$ là góc giữa $\vec F$ và hướng chuyển động; đề đã cho sẵn góc này"),
  (r"“b) thẳng đứng, hướng lên”", r"Lực thẳng đứng; đường đi nằm ngang", r"Tự xác định $\alpha$ từ hướng của lực và hướng đi"),
  (r"“c) hợp với hướng chuyển động góc $120^\circ$”", r"$\alpha=120^\circ$", r"Thế đúng góc đề cho, không đổi sang góc bù"),
  (r"“công phát động, công cản hay … không sinh công”", r"Cần $A$ (J) và loại công", r"Dấu của $\cos\alpha$ cho biết loại công")],
 [(r"“thùng hàng khối lượng $40$ kg … nghiêng $30^\circ$ … $6{,}0$ m dọc mặt dốc”", r"$m=40\ \text{kg}$; $\theta=30^\circ$; $s=6{,}0\ \text{m}$ dọc dốc", r"⚠ $s$ đo dọc mặt dốc; độ cao $h$ phải tính từ góc dốc"),
  (r"“lực ma sát trượt … $40$ N”", r"$F_{ms}=40\ \text{N}$", r"Ma sát trượt cùng phương với chuyển động"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng $P=mg$"),
  (r"“a) độ cao thùng được nâng lên và công của trọng lực”", r"Cần $h$ (m) và $A_P$ (J)", r"Công của trọng lực chỉ phụ thuộc độ cao, theo chiều lên hay xuống"),
  (r"“b) công của lực ma sát trong lúc kéo lên”", r"Cần $A_{ms}$ (J)", r"Công của ma sát tính theo quãng đường đi thật"),
  (r"“c) thùng trượt xuống đúng $6{,}0$ m … ma sát vẫn là $40$ N”", r"$s'=6{,}0\ \text{m}$; chiều đi đã đổi; $F_{ms}=40\ \text{N}$", r"Chiều chuyển động đổi thì xét lại góc giữa từng lực và dịch chuyển")],
 [(r"“thùng khối lượng $25$ kg … nền kho nằm ngang”", r"$m=25\ \text{kg}$", r"⚠ Công của một lực chỉ tính theo thành phần của lực dọc theo dịch chuyển"),
  (r"“dây chếch lên, hợp với phương ngang góc $30^\circ$, lực kéo $100$ N”", r"$F=100\ \text{N}$; $\alpha=30^\circ$ (cũng là góc giữa lực và hướng đi)", r"Lực kéo chếch lên so với hướng đi"),
  (r"“hệ số ma sát trượt … $0{,}20$”", r"$\mu=0{,}20$", r"$F_{ms}=\mu N$, ngược hướng chuyển động"),
  (r"“đi thẳng $12$ m”", r"$s=12\ \text{m}$", r"Mỗi lực có công $F\,s\cos\alpha$ của riêng nó"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng $P=mg$"),
  (r"“công của lực kéo, trọng lực, phản lực và lực ma sát”", r"Cần $A_F$, $A_P$, $A_N$, $A_{ms}$ (J)", r"Đại lượng cần tìm"),
  (r"“tổng công của các lực đó”", r"Cần $A$ (J)", r"Công là đại lượng vô hướng, cộng đại số")],
]

# ═════════════ Lời giải từng bước ═════════════
R_NL = [r"<strong>Khái niệm:</strong> năng lượng tồn tại ở nhiều dạng; chuyển hoá từ dạng này sang dạng khác hoặc truyền từ vật này sang vật khác.",
        r"<strong>Định luật bảo toàn:</strong> năng lượng không tự sinh ra, không tự mất đi.",
        r"Năng lượng là đại lượng vô hướng, đơn vị jun (J).",
        r"⚠ <strong>Điều kiện:</strong> tính đủ mọi dạng năng lượng, kể cả nhiệt năng và âm thanh tản ra môi trường."]
R_CONG = [r"<strong>Khái niệm:</strong> lực làm vật dịch chuyển thì thực hiện công, truyền năng lượng cho vật.",
          r"$A=Fs\cos\alpha$ ($\alpha$: góc giữa $\vec F$ và độ dịch chuyển; vật đi thẳng một chiều thì $d=s$).",
          r"$\alpha=0^\circ$: $A=Fs$ · $\alpha=180^\circ$: $A=-Fs$.",
          r"Công là đại lượng vô hướng, $1\ \text{J}=1\ \text{N}\cdot\text{m}$.",
          r"⚠ <strong>Điều kiện:</strong> chuyển động thẳng đều thì hợp lực bằng $\vec 0$."]
R_XIEN = [r"$A=Fs\cos\alpha$; chỉ thành phần của lực dọc đường đi, $F\cos\alpha$, sinh công.",
          r"Góc nhọn: $A\gt0$, công phát động · góc vuông: $A=0$ · góc tù: $A\lt0$, công cản.",
          r"Công là đại lượng vô hướng: dương, âm hoặc bằng $0$.",
          r"⚠ <strong>Điều kiện:</strong> $\alpha$ là góc giữa lực và hướng chuyển động, rồi mới thế vào công thức."]
R_TL = [r"Trọng lực: vật đi xuống độ cao $h$ thì $A_P=+Ph$; đi lên thì $A_P=-Ph$; đi ngang thì $A_P=0$.",
        r"Lên hay xuống dốc dài $s$, nghiêng $\theta$: độ cao $h=s\sin\theta$.",
        r"Ma sát trượt ngược hướng chuyển động: $A_{ms}=-F_{ms}\,s$.",
        r"Trọng lượng $P=mg$.",
        r"⚠ <strong>Điều kiện:</strong> công trọng lực tính theo độ cao $h$, công ma sát tính theo quãng đường $s$ đi thật."]
R_NHIEU = [r"Công của từng lực: $A=Fs\cos\alpha$, dấu theo góc giữa lực đó và hướng đi.",
           r"Theo phương thẳng đứng thùng không chuyển động: tổng các lực thẳng đứng bằng $0$.",
           r"$F_{ms}=\mu N$, ngược hướng chuyển động; $P=mg$.",
           r"$\vec P$ và $\vec N$ vuông góc với đường đi nằm ngang nên không sinh công.",
           r"⚠ <strong>Điều kiện:</strong> lực kéo chếch lên có thành phần thẳng đứng, nên $N$ phải tính lại, không được lấy $N=mg$."]

SOLS = [
 sol(R_NL, [
  (r"Các dạng năng lượng xuất hiện", [P(r"Điện năng vào máy, ra là <strong>động năng</strong> (lưỡi dao, hoa quả), <strong>nhiệt năng</strong> (động cơ nóng) và <strong>năng lượng âm thanh</strong> (tiếng ồn).")]),
  (r"Phần nhiệt năng và âm thanh trong mỗi giây", [P(r"Năng lượng điện nhận vào bằng tổng các phần năng lượng sinh ra:"), M(r"E_{\text{điện}}=E_{\text{động}}+E_{\text{nhiệt, âm}}"), M(r"E_{\text{nhiệt, âm}}=300-240"), A(r"E_{\text{nhiệt, âm}}=60\ \text{J mỗi giây}")]),
  (r"Phần nhiệt năng và âm thanh trong $20\ \text{s}$", [P(r"Mỗi giây có $60\ \text{J}$, máy chạy $20\ \text{s}$:"), M(r"E=60\ \text{J/s}\cdot20\ \text{s}"), A(r"E=1200\ \text{J}")]),
  (r"Nhận xét lời An", [P(r"Sau khi tắt máy, nhiệt năng và âm thanh tản ra không khí xung quanh."), P(r"Không còn thấy nóng hay nghe ồn <strong>không có nghĩa</strong> là năng lượng mất đi."), P(r"Năng lượng không tự mất: câu nói của An <strong>sai</strong>.")]),
  (r"Kiểm tra", [M(r"240+60=300\ \text{J}\ \text{(một giây)}"), M(r"240\cdot20+1200=6000=300\cdot20\ \text{J}\ \text{(hai mươi giây)}"), P(r"Tổng các phần ra bằng điện năng vào ✓.")])],
  [r"a) điện năng → động năng, nhiệt năng, năng lượng âm thanh", r"b) $60\ \text{J}$ mỗi giây", r"c) $1200\ \text{J}$", r"d) An sai: năng lượng không mất, chỉ tản vào môi trường"],
  r"Nhận dạng: đề cho <strong>năng lượng vào và một phần năng lượng ra</strong> rồi hỏi phần còn lại → bảo toàn năng lượng: tổng vào bằng tổng ra."),
 sol(R_CONG, [
  (r"Công của lực đẩy", [P(r"Lực đẩy cùng hướng dịch chuyển, $\alpha=0^\circ$:"), M(r"A_{\text{đẩy}}=Fs\cos0^\circ=25\cdot12\cdot1"), A(r"A_{\text{đẩy}}=300\ \text{J}")]),
  (r"Độ lớn lực cản", [P(r"Xe chuyển động thẳng đều nên hợp lực dọc đường đi bằng $0$:"), M(r"F_{\text{đẩy}}-F_c=0"), A(r"F_c=25\ \text{N}")]),
  (r"Công của lực cản", [P(r"Lực cản ngược hướng dịch chuyển, $\alpha=180^\circ$:"), M(r"A_c=F_c\,s\cos180^\circ=25\cdot12\cdot(-1)"), A(r"A_c=-300\ \text{J}")]),
  (r"Tổng công", [P(r"Công là đại lượng vô hướng nên cộng đại số:"), M(r"A=A_{\text{đẩy}}+A_c=300+(-300)"), A(r"A=0")]),
  (r"Kiểm tra", [P(r"Đơn vị: $\text{N}\cdot\text{m}=\text{J}$ ✓."), P(r"Công dương và công âm cùng độ lớn triệt tiêu nhau; xe vẫn đi vì lực đẩy và lực cản cân bằng ✓.")])],
  [r"a) $A_{\text{đẩy}}=300\ \text{J}$", r"b) $A_c=-300\ \text{J}$", r"c) $A=0$"],
  r"Nhận dạng: đề cho <strong>lực cùng hướng hoặc ngược hướng dịch chuyển</strong> → $A=Fs$ với dấu cộng hoặc dấu trừ."),
 sol(R_XIEN, [
  (r"Tình huống a: $\alpha=60^\circ$", [M(r"A=Fs\cos\alpha=70\cdot8{,}0\cdot\cos60^\circ"), M(r"A=560\cdot0{,}5"), A(r"A=280\ \text{J}")]),
  (r"Tình huống b: lực thẳng đứng", [P(r"Đường đi nằm ngang, lực thẳng đứng nên hai phương vuông góc: $\alpha=90^\circ$."), M(r"A=70\cdot8{,}0\cdot\cos90^\circ"), A(r"A=0")]),
  (r"Tình huống c: $\alpha=120^\circ$", [P(r"Thế đúng góc đề cho:"), M(r"A=70\cdot8{,}0\cdot\cos120^\circ"), M(r"A=560\cdot(-0{,}5)"), A(r"A=-280\ \text{J}")]),
  (r"Phân loại công", [P(r"a) $\alpha=60^\circ$ là góc nhọn, $A\gt0$: <strong>công phát động</strong>."), P(r"b) $\alpha=90^\circ$, $A=0$: <strong>lực không sinh công</strong>."), P(r"c) $\alpha=120^\circ$ là góc tù, $A\lt0$: <strong>công cản</strong>.")]),
  (r"Kiểm tra", [P(r"Độ lớn mỗi công không vượt quá $Fs=560\ \text{J}$ ✓."), P(r"Hai góc $60^\circ$ và $120^\circ$ bù nhau nên hai công cùng độ lớn, trái dấu ✓.")])],
  [r"a) $A=280\ \text{J}$, công phát động", r"b) $A=0$, lực không sinh công", r"c) $A=-280\ \text{J}$, công cản"],
  r"Nhận dạng: đề cho <strong>lực chếch một góc so với hướng đi</strong> và hỏi phát động hay cản → $A=Fs\cos\alpha$, xét dấu của $\cos\alpha$."),
 sol(R_TL, [
  (r"Độ cao thùng được nâng lên", [P(r"Độ cao tính từ quãng đường dọc dốc và góc dốc:"), M(r"h=s\sin\theta=6{,}0\cdot\sin30^\circ"), A(r"h=3{,}0\ \text{m}")]),
  (r"Công của trọng lực lúc kéo lên", [P(r"Trọng lượng của thùng:"), M(r"P=mg=40\cdot10=400\ \text{N}"), P(r"Thùng đi lên:"), M(r"A_P=-Ph=-400\cdot3{,}0"), A(r"A_P=-1200\ \text{J}")]),
  (r"Công của lực ma sát lúc kéo lên", [P(r"Ma sát tác dụng suốt quãng đường dọc dốc, không phải độ cao:"), M(r"A_{ms}=-F_{ms}\,s=-40\cdot6{,}0"), A(r"A_{ms}=-240\ \text{J}")]),
  (r"Công của trọng lực lúc trượt xuống", [P(r"Thùng về chỗ cũ, đi xuống độ cao $h=3{,}0\ \text{m}$:"), M(r"A_P=+Ph=400\cdot3{,}0"), A(r"A_P=+1200\ \text{J}")]),
  (r"Công của lực ma sát lúc trượt xuống", [P(r"Ma sát vẫn ngược hướng chuyển động, quãng đường vẫn $6{,}0\ \text{m}$:"), M(r"A_{ms}=-F_{ms}\,s=-40\cdot6{,}0"), A(r"A_{ms}=-240\ \text{J}")]),
  (r"Kiểm tra", [P(r"Cả đi lên rồi trượt xuống, công trọng lực: $-1200+1200=0$ (thùng về đúng độ cao ban đầu)."), P(r"Công ma sát: $-240-240=-480\ \text{J}$, ma sát tiêu hao năng lượng cả hai chiều ✓.")])],
  [r"a) $h=3{,}0\ \text{m}$ · $A_P=-1200\ \text{J}$", r"b) $A_{ms}=-240\ \text{J}$", r"c) $A_P=+1200\ \text{J}$ · $A_{ms}=-240\ \text{J}$"],
  r"Nhận dạng: đề cho <strong>vật lên hoặc xuống dốc có ma sát</strong> → $A_P=\pm Ph$ với $h=s\sin\theta$, $A_{ms}=-F_{ms}s$."),
 sol(R_NHIEU, [
  (r"Phản lực của sàn", [P(r"Trọng lượng của thùng:"), M(r"P=mg=25\cdot10=250\ \text{N}"), P(r"Thùng không dịch chuyển theo phương thẳng đứng. Lực kéo chếch lên có thành phần thẳng đứng $F\sin\alpha$ hướng lên:"), M(r"N+F\sin\alpha=P"), M(r"N=P-F\sin\alpha=250-100\cdot0{,}5"), A(r"N=200\ \text{N}")]),
  (r"Lực ma sát trượt", [M(r"F_{ms}=\mu N=0{,}20\cdot200"), A(r"F_{ms}=40\ \text{N}")]),
  (r"Công của lực kéo", [P(r"Góc giữa lực kéo và hướng đi là $30^\circ$:"), M(r"A_F=Fs\cos30^\circ=100\cdot12\cdot0{,}866"), A(r"A_F\approx1039\ \text{J}")]),
  (r"Công của lực ma sát", [P(r"Ma sát ngược hướng chuyển động, $\alpha=180^\circ$:"), M(r"A_{ms}=-F_{ms}\,s=-40\cdot12"), A(r"A_{ms}=-480\ \text{J}")]),
  (r"Công của trọng lực và phản lực", [P(r"Cả hai vuông góc với hướng đi ($\alpha=90^\circ$, $\cos90^\circ=0$):"), A(r"A_P=A_N=0")]),
  (r"Tổng công", [P(r"Cộng đại số công của cả bốn lực:"), M(r"A=A_F+A_P+A_N+A_{ms}=1039+0+0+(-480)"), A(r"A\approx559\ \text{J}")]),
  (r"Kiểm tra", [P(r"Đơn vị: $\text{N}\cdot\text{m}=\text{J}$ ✓."), P(r"Phản lực $N=200\ \text{N}$ nhỏ hơn trọng lượng $250\ \text{N}$ vì lực kéo chếch lên nâng bớt thùng ✓."), P(r"Tổng công dương: lực kéo truyền vào thùng nhiều năng lượng hơn phần ma sát lấy đi ✓.")])],
  [r"$A_F\approx1039\ \text{J}$ · $A_{ms}=-480\ \text{J}$", r"$A_P=A_N=0$", r"Tổng công $A\approx559\ \text{J}$"],
  r"Nhận dạng: đề cho <strong>lực kéo chếch lên và hệ số ma sát</strong> → tìm $N$ trước, rồi $F_{ms}=\mu N$ và công từng lực."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>năng lượng vào</b> và <b>một phần năng lượng ra</b>, hỏi phần còn lại → nghĩ tới <b>tổng vào bằng tổng ra</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Các dạng năng lượng xuất hiện", r"Chọn mô tả đúng về sự chuyển hoá năng lượng của máy.",
       loi=r"Cho rằng phần không thành động năng bị hao hụt hẳn, hoặc thêm một dạng đề không nhắc tới.",
       lua_chon=[(r"Thành động năng, nhiệt năng và âm thanh", True),
                 (r"Hết thành động năng, phần còn lại mất đi", r"Năng lượng không tự mất đi: phần không thành động năng vẫn tồn tại ở một dạng khác."),
                 (r"Thành động năng và quang năng", r"Đề không nhắc tới ánh sáng; hai hiện tượng của phần còn lại là nóng lên và tiếng ồn.")]),
  buoc(r"Phần nhiệt năng và âm thanh mỗi giây", r"Trong mỗi giây, phần năng lượng thành nhiệt năng và âm thanh là bao nhiêu?", 60, "J", 0.5,
       loi=r"Coi phần không thành động năng là hao đi nên không cần tính, hoặc ghép hai số của đề sai phép tính.",
       ke=[(r"Lấy năng lượng điện vào trừ phần đã thành động năng", True),
           (r"Cộng năng lượng điện vào với động năng", r"Tổng các phần ra phải bằng năng lượng vào; cộng thêm cho một tổng khác năng lượng thật có."),
           (r"Chia năng lượng điện cho động năng", r"Bảo toàn năng lượng nói về tổng và hiệu các phần năng lượng, không phải thương của chúng.")]),
  buoc(r"Phần nhiệt năng và âm thanh trong $20\ \text{s}$", r"Trong $20\ \text{s}$, phần năng lượng thành nhiệt năng và âm thanh là bao nhiêu?", 1200, "J", 5,
       loi=r"Giữ nguyên kết quả của một giây, hoặc chia cho thời gian thay vì nhân.",
       ke=[(r"Nhân năng lượng mỗi giây với thời gian máy chạy", True),
           (r"Chia năng lượng mỗi giây cho thời gian máy chạy", r"Năng lượng tích luỹ theo thời gian nên phải nhân với thời gian, không chia."),
           (r"Giữ nguyên kết quả của một giây", r"Máy chạy lâu hơn thì năng lượng tạo ra nhiều hơn; kết quả một giây chỉ là phần nhỏ của cả quá trình.")]),
  buoc(r"Nhận xét lời An", r"Chọn nhận xét đúng về câu nói của An.",
       loi=r"Nhầm “không còn thấy nóng, không còn nghe ồn” với “năng lượng không còn”.",
       lua_chon=[(r"Sai: năng lượng chỉ tản vào môi trường", True),
                 (r"Đúng: hết nóng và hết ồn thì năng lượng đã hết", r"Hết nóng, hết ồn chỉ cho biết năng lượng đã tản ra xung quanh, không phải đã biến mất."),
                 (r"Đúng: điện năng đã dùng hết nên không còn gì", r"Dùng hết điện không có nghĩa năng lượng mất; nó đã sang các dạng khác.")],
       ke=[(r"Dùng định luật bảo toàn năng lượng", True),
           (r"Dùng công thức $A=Fs\cos\alpha$", r"Đề không nêu lực hay độ dịch chuyển; câu hỏi là năng lượng có mất đi hay không."),
           (r"Dựa vào việc máy còn nóng hay không", r"Máy nóng hay nguội không cho biết năng lượng có được bảo toàn hay không.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực cùng hướng hoặc ngược hướng dịch chuyển</b> → nghĩ tới <b>A = Fs</b>, đặt dấu theo hướng.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Công của lực đẩy", r"Công của lực đẩy bằng bao nhiêu?", 300, "J", 1,
       loi=r"Nhân thêm một hệ số không có trong đề (như $g$) hoặc dùng $\sin$ thay vì $\cos$."),
  buoc(r"Độ lớn lực cản", r"Lực cản của sàn có độ lớn bằng bao nhiêu?", 25, "N", 0.5,
       loi=r"Bỏ qua dữ kiện chuyển động thẳng đều nên không xác định được lực cản.",
       ke=[(r"Dùng điều kiện chuyển động thẳng đều: hợp lực dọc đường đi bằng không", True),
           (r"Dùng $A=Fs$ để suy ra lực cản", r"Công thức công cần biết lực; ở bước này chính lực cản đang cần tìm."),
           (r"Cho lực cản bằng không vì sàn nằm ngang", r"Sàn nằm ngang chỉ cho biết phản lực vuông góc; vẫn có lực cản dọc đường đi.")]),
  buoc(r"Công của lực cản", r"Công của lực cản bằng bao nhiêu?", -300, "J", 1,
       loi=r"Lấy dấu dương cho mọi công, không xét góc giữa lực cản và dịch chuyển.",
       ke=[(r"Thế góc giữa lực cản và dịch chuyển vào $A=Fs\cos\alpha$", True),
           (r"Lấy $A_c=+F_c\,s$ như lực đẩy", r"Dấu của công do góc giữa lực và dịch chuyển quyết định; cần xét lại góc của lực cản."),
           (r"Cho $A_c=0$ vì xe không dừng lại", r"Lực cản cũng có độ dịch chuyển cùng phương nên công của nó khác không.")]),
  buoc(r"Tổng công", r"Tổng công của hai lực bằng bao nhiêu?", 0, "J", 1,
       loi=r"Cộng độ lớn hai công, bỏ qua dấu.",
       ke=[(r"Cộng đại số hai công đã tính", True),
           (r"Cộng độ lớn của hai công", r"Mỗi công mang dấu riêng của nó; bỏ dấu là cộng sai."),
           (r"Nhân hai công với nhau", r"Công là đại lượng vô hướng; các công của nhiều lực cộng với nhau, không nhân.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực chếch một góc so với hướng đi</b>, hỏi phát động hay cản → nghĩ tới <b>A = Fs·cosα</b>, xét dấu cosα.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Tình huống a: $\alpha=60^\circ$", r"Công của lực khi $\alpha=60^\circ$ bằng bao nhiêu?", 280, "J", 1,
       loi=r"Dùng $\sin$ thay cho $\cos$, hoặc bỏ luôn hệ số $\cos\alpha$."),
  buoc(r"Tình huống b: lực thẳng đứng", r"Công của lực thẳng đứng hướng lên bằng bao nhiêu?", 0, "J", 0.5,
       loi=r"Nhân thẳng $F$ với $s$, quên rằng phải xét góc giữa lực và đường đi.",
       ke=[(r"Tìm góc giữa lực thẳng đứng và đường đi nằm ngang", True),
           (r"Bỏ qua góc, nhân thẳng $F$ với $s$", r"Công thức công luôn có $\cos\alpha$; không có góc thì chưa tính được công."),
           (r"Lấy góc giữa lực và trục thẳng đứng", r"$\alpha$ là góc giữa lực và hướng chuyển động, không phải giữa lực và trục thẳng đứng.")]),
  buoc(r"Tình huống c: $\alpha=120^\circ$", r"Công của lực khi $\alpha=120^\circ$ bằng bao nhiêu?", -280, "J", 1,
       loi=r"Đổi sang góc bù của $120^\circ$ rồi coi như tình huống a, hoặc bỏ dấu của kết quả.",
       ke=[(r"Thế đúng góc đề cho vào $A=Fs\cos\alpha$", True),
           (r"Lấy góc bù rồi tính như tình huống a", r"Góc giữa lực và dịch chuyển là góc đề cho; đổi sang góc bù làm mất thông tin về dấu."),
           (r"Lấy trị tuyệt đối vì công không âm", r"Công là đại lượng vô hướng nhưng có thể mang dấu; dấu cho biết lực làm tăng hay giảm năng lượng của vật.")]),
  buoc(r"Phân loại công", r"Chọn cách phân loại đúng cho ba tình huống a, b, c.",
       loi=r"Gán loại công theo độ lớn lực thay vì theo dấu của $\cos\alpha$.",
       lua_chon=[(r"a) phát động · b) không sinh công · c) công cản", True),
                 (r"a) phát động · b) công cản · c) phát động", r"Loại công do dấu của $\cos\alpha$ quyết định; hãy đối chiếu dấu kết quả các ý trước."),
                 (r"a) công cản · b) không sinh công · c) phát động", r"Loại công do dấu của $\cos\alpha$ quyết định; hãy đối chiếu dấu kết quả các ý trước.")],
       ke=[(r"Đối chiếu dấu của mỗi kết quả với loại công", True),
           (r"Phân loại theo độ lớn của lực", r"Cả ba tình huống có cùng độ lớn lực nhưng loại công khác nhau."),
           (r"Phân loại theo khối lượng thùng", r"Đề không cho khối lượng thùng; loại công do góc giữa lực và hướng chuyển động quyết định.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật lên hoặc xuống dốc có ma sát</b> → nghĩ tới <b>A_P = ±Ph</b> (h = s·sinθ) và <b>A_ms = −F_ms·s</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Độ cao thùng được nâng lên", r"Thùng được nâng lên độ cao bao nhiêu?", 3.0, "m", 0.05,
       loi=r"Lấy độ cao bằng quãng đường dọc dốc, quên nhân với $\sin$ của góc dốc."),
  buoc(r"Công của trọng lực lúc kéo lên", r"Công của trọng lực khi thùng được kéo lên bằng bao nhiêu?", -1200, "J", 5,
       loi=r"Tính theo quãng đường dọc dốc thay vì độ cao, hoặc quên xét thùng đi lên hay đi xuống.",
       ke=[(r"Dùng $A_P=\pm Ph$ và chọn dấu theo chiều lên hoặc xuống", True),
           (r"Dùng $A_P=+Ph$ vì thùng có trọng lực", r"Dấu của công trọng lực phụ thuộc thùng lên hay xuống, không phải chỉ vì có trọng lực."),
           (r"Dùng $A_P=\pm Ps$ với $s$ dọc dốc", r"Công của trọng lực tính theo độ cao $h$, không theo quãng đường dọc dốc.")]),
  buoc(r"Công của lực ma sát lúc kéo lên", r"Công của lực ma sát khi thùng được kéo lên bằng bao nhiêu?", -240, "J", 2,
       loi=r"Dùng độ cao $h$ thay cho quãng đường $s$, hoặc đặt dấu theo hướng của lực kéo.",
       ke=[(r"Dùng công thức công của lực ma sát với $s$ là quãng đường dọc dốc", True),
           (r"Dùng $A_{ms}=-F_{ms}\,h$ với $h$ là độ cao", r"Ma sát tác dụng suốt quãng đường dọc dốc, nên phải dùng quãng đường đi thật."),
           (r"Dùng $A_{ms}=+F_{ms}\,s$", r"Dấu của công do góc giữa lực ma sát và dịch chuyển quyết định; cần xét lại góc đó.")]),
  buoc(r"Công của trọng lực lúc trượt xuống", r"Công của trọng lực khi thùng trượt xuống về chỗ cũ bằng bao nhiêu?", 1200, "J", 5,
       loi=r"Giữ nguyên kết quả lúc đi lên mà không xét lại chiều chuyển động.",
       ke=[(r"Xét lại dấu theo chiều đi xuống, vẫn dùng độ cao $h$", True),
           (r"Giữ nguyên kết quả lúc kéo lên", r"Chiều chuyển động đã đổi nên cần xét lại góc giữa trọng lực và dịch chuyển."),
           (r"Dùng $A_P=Ps$ vì thùng trượt dọc dốc", r"Công của trọng lực tính theo độ cao, không theo quãng đường trượt dọc dốc.")]),
  buoc(r"Công của lực ma sát lúc trượt xuống", r"Công của lực ma sát khi thùng trượt xuống bằng bao nhiêu?", -240, "J", 2,
       loi=r"Đổi dấu theo chiều đi mà không xét lại góc giữa lực ma sát và dịch chuyển.",
       ke=[(r"Xét lại góc giữa lực ma sát và dịch chuyển lúc đi xuống", True),
           (r"Đổi dấu so với lúc kéo lên vì chiều đi đã đổi", r"Lực ma sát cũng đổi hướng theo chiều chuyển động; cần xét lại góc giữa nó và dịch chuyển."),
           (r"Cho bằng không vì thùng tự trượt nhờ trọng lực", r"Ma sát vẫn tác dụng và thùng vẫn dịch chuyển, nên công của ma sát khác không.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực kéo chếch lên</b> và <b>hệ số ma sát</b> → nghĩ tới <b>N = P − F·sinα</b> trước, rồi <b>F_ms = μN</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Phản lực của sàn", r"Phản lực $N$ của sàn lên thùng bằng bao nhiêu?", 200, "N", 2,
       loi=r"Cho $N=mg$ ngay, không xét thành phần thẳng đứng của lực kéo chếch lên."),
  buoc(r"Lực ma sát trượt", r"Lực ma sát trượt có độ lớn bao nhiêu?", 40, "N", 0.5,
       loi=r"Dùng $\mu\cdot mg$ thay vì $\mu N$.",
       ke=[(r"Nhân hệ số ma sát với $N$ vừa tìm", True),
           (r"Nhân hệ số ma sát với trọng lượng $P$", r"Ma sát tỉ lệ với áp lực vuông góc, tức phản lực $N$ của bước trước, không phải trọng lượng."),
           (r"Nhân hệ số ma sát với $F\cos\alpha$", r"Thành phần dọc đường đi của lực kéo không phải áp lực của thùng lên sàn.")]),
  buoc(r"Công của lực kéo", r"Công của lực kéo bằng bao nhiêu?", 1039, "J", 5,
       loi=r"Dùng $\sin$ thay cho $\cos$ hoặc bỏ luôn hệ số $\cos\alpha$.",
       ke=[(r"Nhân $F$, $s$ và côsin của góc giữa lực kéo với hướng đi", True),
           (r"Nhân $F$ với $s$, bỏ $\cos\alpha$", r"Chỉ phần lực dọc đường đi, $F\cos\alpha$, mới sinh công; lực chếch nên không bỏ được $\cos\alpha$."),
           (r"Dùng $F\sin\alpha$ thay cho $F\cos\alpha$", r"Góc đã cho là góc với hướng đi (phương ngang), nên thành phần dọc đường đi kề góc đó.")]),
  buoc(r"Công của lực ma sát", r"Công của lực ma sát bằng bao nhiêu?", -480, "J", 2,
       loi=r"Dùng $\mu mg$ thay cho $\mu N$ hoặc quên dấu của công cản.",
       ke=[(r"Nhân $F_{ms}$ với quãng đường rồi đặt dấu theo góc giữa ma sát và hướng đi", True),
           (r"Lấy $A_{ms}=+F_{ms}\,s$", r"Dấu của công do góc giữa lực ma sát và dịch chuyển quyết định; cần xét lại góc đó."),
           (r"Lấy $A_{ms}=-\mu P s$", r"Ma sát phụ thuộc phản lực $N$ đã tìm ở bước đầu, không phụ thuộc trọng lượng.")]),
  buoc(r"Công của trọng lực và phản lực", r"Chọn kết luận đúng về $A_P$ và $A_N$.",
       loi=r"Cho rằng lực lớn thì công khác không, không xét góc với hướng đi.",
       lua_chon=[(r"Cả hai bằng không vì cùng vuông góc với hướng đi", True),
                 (r"Cả hai khác không vì có độ lớn lớn", r"Công không phụ thuộc lực lớn hay nhỏ mà phụ thuộc thành phần của lực dọc đường đi."),
                 (r"$A_P=-Ph$ vì trọng lực hướng xuống", r"Thùng đi ngang, độ cao không đổi; trọng lực vuông góc với đường đi.")],
       ke=[(r"Tìm góc giữa từng lực và hướng đi", True),
           (r"Cộng $P$ và $N$ rồi nhân với $s$", r"Mỗi lực có công riêng theo góc riêng; không gộp lực rồi nhân."),
           (r"Dùng $A=Fs\cos30^\circ$ cho cả hai lực", r"Góc $30^\circ$ là của dây kéo; $\vec P$ và $\vec N$ có góc riêng với hướng đi.")]),
  buoc(r"Tổng công", r"Tổng công của các lực bằng bao nhiêu?", 559, "J", 3,
       loi=r"Cộng độ lớn các công, bỏ dấu của công cản.",
       ke=[(r"Cộng đại số công của cả bốn lực", True),
           (r"Tính tổng công bằng $(F-F_{ms})\,s$", r"$F$ chếch góc nên chỉ thành phần $F\cos\alpha$ dọc đường đi mới sinh công."),
           (r"Lấy công của lực kéo làm tổng công", r"Ma sát cũng chuyển năng lượng (công cản) nên phải tính vào tổng.")]),
  buoc("Kiểm tra")]),
]

TU_LUAN = None
write(J, 68, "Bài 23. Năng lượng. Công cơ học", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
