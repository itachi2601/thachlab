"""Bài 58 — "Bài 13. Tổng hợp và phân tích lực. Cân bằng lực" (Vật lí 10, chương 3). 6 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-57.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-58.py  → ghi scripts/data/bai-tap-mau/58.json
Dạng xếp theo hệ bắc cầu (quét: scripts/logs/batch-ra-soat/ket-qua/58.quet-dang.json). Hình: hinh_58.py (vec_luc, tỉ lệ độ dài = k·F).
Ví dụ cũ (old/58.json, 20 mục): VD1→Dạng 1 (đổi số), VD2→Dạng 2 (đổi số, thêm khoảng giá trị); VD6, 8, 9, 10, 11, 13 → tự luận;
BỎ: VD3 (làm tròn 15454 thay vì 15455, ý a vẽ hình), VD4 (góc 36° thay vì 36,9°), VD5/12/14/15/17/18/19 (đề phụ thuộc hình, không kiểm được),
VD7 (d₂ = 0,825 m sai, đúng 0,875 m), VD16 (T≈47 N sai, đúng ≈46,2 N), VD20 (góc α₁, α₂ chỉ xác định bằng hình; m=15,2 kg làm tròn sai)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_58 import BUILD

J = os.path.join(HERE, "58.json")
OLD = json.load(open(os.path.join(HERE, "old/58.json")))["questions"]
T119, T120, T121 = "Tổng hợp hai lực đồng quy", "Phân tích lực theo hai phương vuông góc", "Điều kiện cân bằng của chất điểm"

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
cosd = lambda a: math.cos(math.radians(a)); sind = lambda a: math.sin(math.radians(a))
# D1
F1, F2 = 5.0, 12.0
ok("D1a", F1 + F2, 17, 1e-9); ok("D1b", abs(F1 - F2), 7, 1e-9); ok("D1c", math.hypot(F1, F2), 13, 1e-9)
ok("D1d F²", F1**2 + F2**2 + 2 * F1 * F2 * cosd(60), 229, 1e-9); ok("D1d", math.sqrt(229), 15.1, 0.05)
ok("D1 sai: 5·cos60+12", math.sqrt(F1**2 + F2**2), 13, 1e-9)
assert abs(math.sqrt(229) - 13) > 1 and abs(math.sqrt(229) - 17) > 1       # các cách sai cho kết quả khác đáp án
# D2
F1, F2, F = 7.0, 15.0, 20.0
ok("D2 min", abs(F1 - F2), 8, 1e-9); ok("D2 max", F1 + F2, 22, 1e-9)
assert 5 < 8 and 8 <= 12 <= 22
c = (F**2 - F1**2 - F2**2) / (2 * F1 * F2); ok("D2 cos", c, 0.6, 1e-12); al = math.degrees(math.acos(c)); ok("D2 α", al, 53.1, 0.05)
ok("D2 thế lại", F1**2 + F2**2 + 2 * F1 * F2 * c, 400, 1e-9)
assert abs(F / (F1 + F2) - c) > 0.3 and abs((F1**2 + F2**2 - F**2) / (2 * F1 * F2) - c) > 1
assert abs(math.degrees(math.asin(c)) - al) > 10 and abs(180 - al - al) > 10
# D3
F, a = 45.0, 40
ok("D3 Fx", F * cosd(a), 34.5, 0.05); ok("D3 Fy", F * sind(a), 28.9, 0.05); ok("D3 Fx60", F * cosd(60), 22.5, 1e-9)
ok("D3 kiểm", math.hypot(F * cosd(a), F * sind(a)), 45, 1e-9)
assert abs((F - F * cosd(a)) - F * sind(a)) > 10 and abs(F * cosd(a) - F * sind(a)) > 5           # F−Fx; cos thay sin
# D4
m, g, a = 8.0, 10.0, 40; PW = m * g
ok("D4 PW", PW, 80, 1e-9); ok("D4 Px", PW * sind(a), 51.4, 0.05); ok("D4 Py", PW * cosd(a), 61.3, 0.05); ok("D4 Px20", PW * sind(20), 27.4, 0.05)
ok("D4 kiểm", math.hypot(PW * sind(a), PW * cosd(a)), 80, 1e-9)
assert min(abs(PW * cosd(a) - PW * sind(a)), abs(PW * math.tan(math.radians(a)) - PW * sind(a)), abs(PW - PW * sind(a) - PW * cosd(a)), abs(PW * cosd(20) - PW * sind(20))) > 5
# D5
m, b = 3.0, 30; PW = m * 10
ok("D5 PW", PW, 30, 1e-9); TB = PW / cosd(b); TA = TB * sind(b); ok("D5 TB", TB, 34.6, 0.05); ok("D5 TA", TA, 17.3, 0.05)
ok("D5 TA=PW·tan", PW * math.tan(math.radians(b)), TA, 1e-9)
assert abs(PW / sind(b) - TB) > 5 and abs(PW - TB) > 3 and abs(PW - TA) > 5 and abs(TA - TB) > 5
# D6
L, h, PW = 6.0, 0.5, 40.0
th = math.degrees(math.atan(h / (L / 2))); ok("D6 θ", th, 9.46, 0.005)
T = PW / (2 * sind(th)); ok("D6 T", T, 121.7, 0.05); ok("D6 T/PW", T / PW, 3.04, 0.005)
ok("D6 kiểm nhánh", math.hypot(L / 2, h) * 2 * 0 + 2 * T * sind(th), PW, 1e-9)
assert abs(PW / 2 - T) > 50 and abs(PW - T) > 50 and abs(math.degrees(math.atan(h / L)) - th) > 3            # PW/2, PW, dùng cả nhịp
# Tự luận cũ
ok("VD6", abs(10 - 2 * 5 * cosd(60)), 5, 1e-9)
ok("VD9", 240 / 3, 80, 1e-9)
ok("VD10 O2A", (30 * 0.5 + 50 * 1) / 100, 0.65, 1e-9)
ok("VD11", 100 / (2 * cosd(75)), 193.2, 0.05); ok("VD13", 20 / cosd(45), 20 * math.sqrt(2), 1e-9)
ok("VD8", 100 / 200, (2 / 3) / (4 / 3), 1e-9)


# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Độ lớn hợp lực của hai lực đồng quy theo góc", topic=T119,
      problem_html=r"""<p>Hai sợi dây buộc vào một vòng nhẫn $O$, mỗi dây kéo qua một lực kế. Lực kế thứ nhất chỉ $F_1=5{,}0\ \text{N}$, lực kế thứ hai chỉ $F_2=12\ \text{N}$. Hai dây có thể hợp với nhau một góc $\alpha$ tuỳ ý. Tính độ lớn hợp lực tác dụng lên vòng nhẫn khi:</p>
<ol type="a"><li>$\alpha=0^\circ$;</li><li>$\alpha=180^\circ$;</li><li>$\alpha=90^\circ$;</li><li>$\alpha=60^\circ$.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Khoảng giá trị của hợp lực và tìm góc giữa hai lực", topic=T119,
      problem_html=r"""<p>Hai lực đồng quy có độ lớn $F_1=7{,}0\ \text{N}$ và $F_2=15\ \text{N}$ cùng tác dụng lên một chất điểm.</p>
<ol type="a"><li>Khi góc giữa hai lực thay đổi, độ lớn hợp lực nhỏ nhất và lớn nhất là bao nhiêu?</li>
<li>Hợp lực có thể có độ lớn $5{,}0\ \text{N}$ không? Có thể có độ lớn $12\ \text{N}$ không?</li>
<li>Biết hợp lực có độ lớn $20\ \text{N}$. Tính góc giữa hai lực.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Phân tích lực kéo xiên thành thành phần ngang và đứng", topic=T120,
      problem_html=r"""<p>Một bạn kéo thùng hàng trượt trên sàn nhà bằng sợi dây nhẹ. Dây hợp với phương ngang góc $\alpha=40^\circ$, lực kéo của dây có độ lớn $F=45\ \text{N}$.</p>
<ol type="a"><li>Tính thành phần nằm ngang $F_x$ và thành phần thẳng đứng $F_y$ của lực kéo.</li>
<li>Thành phần nào làm thùng tiến lên? Thành phần nào làm thùng bớt ép xuống sàn?</li>
<li>Bạn nâng tay cao hơn nên dây hợp với phương ngang góc $60^\circ$, lực kéo vẫn là $45\ \text{N}$. Tính $F_x$ lúc này.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Phân tích trọng lực trên mặt dốc", topic=T120,
      problem_html=r"""<p>Một thùng hàng khối lượng $8{,}0\ \text{kg}$ đặt trên mặt dốc nghiêng góc $\alpha=40^\circ$ so với phương ngang. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính trọng lượng $P$ của thùng.</li>
<li>Phân tích trọng lực thành hai thành phần: $P_x$ song song với mặt dốc, $P_y$ vuông góc với mặt dốc. Tính $P_x$ và $P_y$.</li>
<li>Dốc được hạ xuống thoải hơn, nghiêng $20^\circ$ so với phương ngang. Tính $P_x$ lúc này.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Vật treo bằng hai dây: lực căng khi vòng nhẫn cân bằng", topic=T121,
      problem_html=r"""<p>Một vật khối lượng $3{,}0\ \text{kg}$ được treo vào vòng nhẫn $O$ (coi là chất điểm) bằng một sợi dây nhẹ. Vòng nhẫn được giữ yên bằng hai dây nhẹ khác: dây $OA$ nằm ngang buộc vào tường, dây $OB$ hợp với phương thẳng đứng góc $30^\circ$ buộc vào trần. Lấy $g=10\ \text{m/s}^2$. Tính lực căng của dây $OA$ và của dây $OB$.</p>"""),
 dict(label="Dạng 6 · Khó · Dây võng: lực căng mỗi nhánh", topic=T121,
      problem_html=r"""<p>Hai đầu $A$, $B$ của một dây điện nhẹ buộc vào hai cột ở cùng độ cao, cách nhau $6{,}0\ \text{m}$. Treo một đèn khối lượng $4{,}0\ \text{kg}$ vào chính giữa dây thì chỗ treo võng xuống $0{,}50\ \text{m}$ so với đường thẳng $AB$ và đèn đứng yên. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính góc $\theta$ giữa mỗi nhánh dây và phương ngang.</li>
<li>Tính lực căng của mỗi nhánh dây.</li>
<li>Lực căng gấp mấy lần trọng lượng của đèn?</li></ol>"""),
]
FORMS = ["bai_tap"] * 6

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“Hai sợi dây buộc vào một vòng nhẫn $O$, mỗi dây kéo qua một lực kế”", r"Hai lực cùng đặt vào $O$", r"⚠ Hai lực đồng quy (cùng tác dụng lên một chất điểm) mới tổng hợp được"),
  (r"“lực kế thứ nhất chỉ $5{,}0$ N, thứ hai chỉ $12$ N”", r"$F_1=5{,}0\ \text{N}$; $F_2=12\ \text{N}$", r"Độ lớn của hai lực thành phần"),
  (r"“hợp với nhau một góc $\alpha$ tuỳ ý”", r"$\alpha$ nhận bốn giá trị của đề", r"⚠ $\alpha$ là góc giữa hai vectơ lực vẽ chung gốc"),
  (r"“a) $\alpha=0^\circ$ … b) $\alpha=180^\circ$ … c) $\alpha=90^\circ$ … d) $\alpha=60^\circ$”", r"Bốn trường hợp về góc", r"Hợp lực là đường chéo hình bình hành"),
  (r"“độ lớn hợp lực tác dụng lên vòng nhẫn”", r"Cần $F$ (N) ở từng trường hợp", r"Đại lượng cần tìm")],
 [(r"“Hai lực đồng quy … $F_1=7{,}0$ N và $F_2=15$ N”", r"$F_1=7{,}0\ \text{N}$; $F_2=15\ \text{N}$", r"⚠ Hai lực đồng quy cùng tác dụng lên một chất điểm"),
  (r"“khi góc giữa hai lực thay đổi”", r"$\alpha$ chạy từ $0^\circ$ đến $180^\circ$", r"Hợp lực phụ thuộc góc giữa hai lực"),
  (r"“a) độ lớn nhỏ nhất và lớn nhất của hợp lực”", r"Cần $F_{min}$, $F_{max}$ (N)", r"Đại lượng cần tìm"),
  (r"“b) có thể có độ lớn $5{,}0$ N không? $12$ N không?”", r"Hai giá trị cần kiểm tra", r"⚠ Cần biết hợp lực nhận những giá trị nào khi góc đổi"),
  (r"“c) hợp lực có độ lớn $20$ N”", r"$F=20\ \text{N}$", r"Công thức độ lớn hợp lực qua $\alpha$"),
  (r"“tính góc giữa hai lực”", r"Cần $\alpha$ (độ)", r"Đại lượng cần tìm")],
 [(r"“sợi dây nhẹ. Dây hợp với phương ngang góc $\alpha=40^\circ$”", r"$\alpha=40^\circ$ (so với phương ngang)", r"⚠ $\alpha$ là góc giữa $\vec F$ và trục $Ox$ nằm ngang"),
  (r"“lực kéo của dây có độ lớn $F=45$ N”", r"$F=45\ \text{N}$", r"Lực cần phân tích"),
  (r"“a) thành phần nằm ngang $F_x$ và thành phần thẳng đứng $F_y$”", r"Cần $F_x$, $F_y$ (N)", r"Đại lượng cần tìm"),
  (r"“b) thành phần nào làm thùng tiến lên? … bớt ép xuống sàn?”", r"Tác dụng của từng thành phần", r"Phân tích lực: thay một lực bằng hai thành phần"),
  (r"“c) dây hợp với phương ngang góc $60^\circ$, lực kéo vẫn là $45$ N”", r"$\alpha'=60^\circ$; $F=45\ \text{N}$", r"Đổi góc, giữ nguyên độ lớn lực"),
  (r"“Tính $F_x$ lúc này”", r"Cần $F_x'$ (N)", r"Đại lượng cần tìm")],
 [(r"“thùng hàng khối lượng $8{,}0$ kg … Lấy $g=10$ m/s²”", r"$m=8{,}0\ \text{kg}$; $g=10\ \text{m/s}^2$", r"Trọng lực hướng thẳng đứng xuống"),
  (r"“mặt dốc nghiêng góc $\alpha=40^\circ$ so với phương ngang”", r"$\alpha=40^\circ$", r"⚠ Hai phương chọn vuông góc: dọc dốc và vuông góc dốc"),
  (r"“a) trọng lượng $P$ của thùng”", r"Cần $P$ (N)", r"Đại lượng cần tìm"),
  (r"“b) $P_x$ song song với mặt dốc, $P_y$ vuông góc với mặt dốc”", r"Cần $P_x$, $P_y$ (N)", r"Phân tích lực theo hai phương vuông góc"),
  (r"“c) dốc nghiêng $20^\circ$ so với phương ngang”", r"$\alpha'=20^\circ$; cùng vật", r"Đổi góc nghiêng, giữ nguyên vật"),
  (r"“Tính $P_x$ lúc này”", r"Cần $P_x'$ (N)", r"Đại lượng cần tìm")],
 [(r"“vật khối lượng $3{,}0$ kg … treo vào vòng nhẫn $O$ bằng một sợi dây nhẹ”", r"$m=3{,}0\ \text{kg}$", r"Trọng lực hướng xuống; dây nhẹ truyền lực"),
  (r"“vòng nhẫn $O$ (coi là chất điểm)”", r"Chất điểm $O$", r"Các lực đều đặt tại $O$"),
  (r"“được giữ yên”", r"Vòng nhẫn đứng yên", r"⚠ Điều kiện cân bằng: tổng các lực bằng $\vec 0$"),
  (r"“dây $OA$ nằm ngang”", r"Phương của $T_{OA}$ là phương ngang", r"Lực căng có phương dọc theo dây"),
  (r"“dây $OB$ hợp với phương thẳng đứng góc $30^\circ$”", r"$\beta=30^\circ$ (so với phương thẳng đứng)", r"⚠ Góc cho so với phương thẳng đứng"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng của vật"),
  (r"“Tính lực căng của dây $OA$ và của dây $OB$”", r"Cần $T_{OA}$, $T_{OB}$ (N)", r"Đại lượng cần tìm")],
 [(r"“dây điện nhẹ … hai đầu $A$, $B$ ở cùng độ cao, cách nhau $6{,}0$ m”", r"$AB=6{,}0\ \text{m}$ (nằm ngang)", r"Dây nhẹ: bỏ qua trọng lượng của dây"),
  (r"“đèn khối lượng $4{,}0$ kg vào chính giữa dây”", r"$m=4{,}0\ \text{kg}$; điểm treo ở giữa", r"⚠ Điều kiện đối xứng: hai nhánh hợp phương ngang cùng một góc"),
  (r"“võng xuống $0{,}50$ m so với đường thẳng $AB$”", r"Độ võng $h=0{,}50\ \text{m}$", r"Số đo hình học của dây"),
  (r"“đèn đứng yên”", r"Điểm treo cân bằng", r"⚠ Điều kiện cân bằng: tổng các lực bằng $\vec 0$"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng của đèn"),
  (r"“a) góc $\theta$ giữa mỗi nhánh dây và phương ngang”", r"Cần $\theta$ (độ)", r"Đại lượng cần tìm"),
  (r"“b) lực căng của mỗi nhánh dây”", r"Cần $T$ (N)", r"Đại lượng cần tìm"),
  (r"“c) gấp mấy lần trọng lượng của đèn”", r"Cần tỉ số $T/P$", r"Đại lượng cần tìm")],
]

# ═════════════ Lời giải từng bước ═════════════
R_HL = [r"<strong>Khái niệm:</strong> hợp lực thay hai lực đồng quy bằng một lực có tác dụng giống hệt.",
        r"<strong>Quy tắc:</strong> hình bình hành, đường chéo xuất phát từ gốc là hợp lực.",
        r"$F^2=F_1^2+F_2^2+2F_1F_2\cos\alpha$ ($\alpha$: góc giữa hai lực).",
        r"Cùng chiều: $F=F_1+F_2$ · ngược chiều: $F=\lvert F_1-F_2\rvert$.",
        r"⚠ <strong>Điều kiện:</strong> hai lực cùng đặt lên một chất điểm (đồng quy)."]
R_PT = [r"<strong>Khái niệm:</strong> phân tích lực là thay một lực bằng hai thành phần vuông góc có tác dụng giống hệt.",
        r"Chọn hai trục vuông góc $Ox$, $Oy$; $\alpha$ là góc giữa $\vec F$ và trục đang xét.",
        r"Thành phần kề góc $\alpha$: $\cos$ · thành phần đối góc $\alpha$: $\sin$.",
        r"⚠ <strong>Điều kiện:</strong> hai thành phần vuông góc nên $F^2=F_x^2+F_y^2$."]
R_CB = [r"<strong>Khái niệm:</strong> chất điểm cân bằng khi tổng các lực tác dụng lên nó bằng $\vec 0$.",
        r"Chiếu lên hai trục vuông góc: tổng các thành phần trên mỗi trục bằng $0$.",
        r"Thành phần kề góc $\alpha$: $\cos$ · thành phần đối góc $\alpha$: $\sin$.",
        r"Trọng lượng $P=mg$, hướng thẳng đứng xuống.",
        r"⚠ <strong>Điều kiện:</strong> dây nhẹ; lực căng có phương dọc theo dây."]

SOLS = [
 sol(R_HL, [
  (r"Cùng chiều ($\alpha=0^\circ$)", [P(r"Hai lực cùng phương, cùng chiều:"), M(r"F=F_1+F_2=5{,}0+12"), A(r"F=17\ \text{N}")]),
  (r"Ngược chiều ($\alpha=180^\circ$)", [M(r"F=\lvert F_1-F_2\rvert=\lvert5{,}0-12\rvert"), A(r"F=7{,}0\ \text{N}"), P(r"Hợp lực cùng chiều với lực lớn hơn ($\vec F_2$).")]),
  (r"Vuông góc ($\alpha=90^\circ$)", [M(r"F=\sqrt{F_1^2+F_2^2}=\sqrt{5{,}0^2+12^2}=\sqrt{169}"), A(r"F=13\ \text{N}")]),
  (r"Hợp nhau $60^\circ$", [M(r"F^2=F_1^2+F_2^2+2F_1F_2\cos60^\circ"), M(r"F^2=25+144+2\cdot5{,}0\cdot12\cdot0{,}5=229"), A(r"F=\sqrt{229}\approx15{,}1\ \text{N}")]),
  (r"Kiểm tra", [P(r"Cả bốn kết quả nằm trong khoảng từ $7{,}0$ đến $17$ N."), P(r"Góc càng mở, hợp lực càng nhỏ: $17\gt15{,}1\gt13\gt7{,}0$ ✓.")])],
  [r"a) $F=17\ \text{N}$", r"b) $F=7{,}0\ \text{N}$", r"c) $F=13\ \text{N}$", r"d) $F\approx15{,}1\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>độ lớn hai lực và góc giữa chúng</strong> → quy tắc hình bình hành; góc đặc biệt thì dùng ngay kết quả riêng."),
 sol(R_HL + [r"Khoảng giá trị: $\lvert F_1-F_2\rvert\le F\le F_1+F_2$."], [
  (r"Hợp lực nhỏ nhất", [P(r"Nhỏ nhất khi hai lực ngược chiều ($\alpha=180^\circ$):"), M(r"F_{min}=\lvert F_1-F_2\rvert=\lvert7{,}0-15\rvert"), A(r"F_{min}=8{,}0\ \text{N}")]),
  (r"Hợp lực lớn nhất", [P(r"Lớn nhất khi hai lực cùng chiều ($\alpha=0^\circ$):"), M(r"F_{max}=F_1+F_2=7{,}0+15"), A(r"F_{max}=22\ \text{N}")]),
  (r"Kiểm tra $5{,}0$ N và $12$ N", [P(r"Hợp lực chỉ nhận giá trị trong đoạn từ $8{,}0$ đến $22$ N."), P(r"$5{,}0\lt8{,}0$: <strong>không thể</strong>."), P(r"$8{,}0\lt12\lt22$: <strong>có thể</strong>, ứng với một góc $\alpha$ nào đó.")]),
  (r"Rút $\cos\alpha$ từ hợp lực $20$ N", [M(r"F^2=F_1^2+F_2^2+2F_1F_2\cos\alpha"), M(r"\cos\alpha=\dfrac{F^2-F_1^2-F_2^2}{2F_1F_2}=\dfrac{20^2-7{,}0^2-15^2}{2\cdot7{,}0\cdot15}=\dfrac{126}{210}"), A(r"\cos\alpha=0{,}6")]),
  (r"Góc giữa hai lực", [M(r"\alpha=\arccos0{,}6"), A(r"\alpha\approx53{,}1^\circ"), P(r"Máy tính để ở chế độ độ (DEG).")]),
  (r"Kiểm tra", [M(r"F^2=7{,}0^2+15^2+2\cdot7{,}0\cdot15\cdot0{,}6=400\ \Rightarrow\ F=20\ \text{N}"), P(r"Và $8{,}0\lt20\lt22$ ✓.")])],
  [r"a) $F_{min}=8{,}0\ \text{N}$ · $F_{max}=22\ \text{N}$", r"b) $5{,}0\ \text{N}$: không thể · $12\ \text{N}$: có thể", r"c) $\alpha\approx53{,}1^\circ$"],
  r"Nhận dạng: đề hỏi <strong>hợp lực có thể bằng bao nhiêu</strong> hoặc cho $F$ rồi hỏi <strong>góc</strong> → khoảng từ hiệu đến tổng; rút $\cos\alpha$ từ công thức hình bình hành."),
 sol(R_PT, [
  (r"Thành phần nằm ngang", [P(r"Chọn $Ox$ nằm ngang, $Oy$ thẳng đứng hướng lên; $\alpha$ là góc giữa $\vec F$ và $Ox$:"), M(r"F_x=F\cos\alpha=45\cos40^\circ"), A(r"F_x\approx34{,}5\ \text{N}")]),
  (r"Thành phần thẳng đứng", [M(r"F_y=F\sin\alpha=45\sin40^\circ"), A(r"F_y\approx28{,}9\ \text{N}"), P(r"Hướng lên.")]),
  (r"Tác dụng của hai thành phần", [P(r"$F_x$ nằm dọc sàn: <strong>kéo thùng tiến lên</strong>."), P(r"$F_y$ hướng lên, vuông góc với sàn: <strong>nhấc bớt thùng</strong>, làm thùng ép xuống sàn nhẹ hơn.")]),
  (r"Dây hợp với phương ngang góc $60^\circ$", [P(r"$\alpha$ vẫn là góc so với phương ngang, $F$ không đổi:"), M(r"F_x'=F\cos60^\circ=45\cdot0{,}5"), A(r"F_x'=22{,}5\ \text{N}"), P(r"Nâng tay cao hơn thì $F_x$ nhỏ đi, $F_y$ lớn lên.")]),
  (r"Kiểm tra", [M(r"\sqrt{F_x^2+F_y^2}=\sqrt{34{,}5^2+28{,}9^2}\approx45\ \text{N}=F"), P(r"Hai thành phần vuông góc nên ghép lại đúng bằng $F$ ✓.")])],
  [r"a) $F_x\approx34{,}5\ \text{N}$ · $F_y\approx28{,}9\ \text{N}$", r"b) $F_x$ kéo thùng tiến lên · $F_y$ nhấc bớt thùng", r"c) $F_x'=22{,}5\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>lực kéo xiên và góc với phương ngang</strong> → phân tích lực thành thành phần ngang và thành phần đứng."),
 sol(R_PT + [r"Dốc nghiêng $\alpha$: $\vec P$ hợp phương vuông góc dốc góc $\alpha$, nên $P_x$ (dọc dốc) đối góc $\alpha$, $P_y$ (vuông góc dốc) kề góc $\alpha$."], [
  (r"Trọng lượng", [M(r"P=mg=8{,}0\cdot10"), A(r"P=80\ \text{N}")]),
  (r"Thành phần dọc dốc", [P(r"Chọn $Ox$ dọc dốc, $Oy$ vuông góc dốc:"), M(r"P_x=P\sin\alpha=80\sin40^\circ"), A(r"P_x\approx51{,}4\ \text{N}"), P(r"Thành phần này kéo thùng trượt xuống dốc.")]),
  (r"Thành phần vuông góc dốc", [M(r"P_y=P\cos\alpha=80\cos40^\circ"), A(r"P_y\approx61{,}3\ \text{N}"), P(r"Thành phần này ép thùng vào mặt dốc.")]),
  (r"Dốc thoải hơn ($20^\circ$)", [M(r"P_x'=P\sin20^\circ=80\cdot0{,}342"), A(r"P_x'\approx27{,}4\ \text{N}"), P(r"$P_x$ giảm: dốc càng thoải, thùng càng ít bị kéo xuống.")]),
  (r"Kiểm tra", [M(r"\sqrt{P_x^2+P_y^2}=\sqrt{51{,}4^2+61{,}3^2}\approx80\ \text{N}=P"), P(r"Dốc nằm ngang ($\alpha=0$): $P_x=0$, $P_y=P$ ✓.")])],
  [r"a) $P=80\ \text{N}$", r"b) $P_x\approx51{,}4\ \text{N}$ · $P_y\approx61{,}3\ \text{N}$", r"c) $P_x'\approx27{,}4\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>vật trên mặt dốc nghiêng góc α</strong> → phân tích trọng lực theo phương dọc dốc và vuông góc dốc."),
 sol(R_CB, [
  (r"Trọng lực và hệ trục", [P(r"Vòng $O$ đứng yên nên $\vec T_{OA}+\vec T_{OB}+\vec P=\vec 0$ ($\vec P$: lực của dây treo vật, bằng trọng lượng vật)."), M(r"P=mg=3{,}0\cdot10"), A(r"P=30\ \text{N}"), P(r"Chọn $Ox$ nằm ngang sang phải, $Oy$ thẳng đứng hướng lên.")]),
  (r"Chiếu lên $Oy$: lực căng dây $OB$", [P(r"Dây $OA$ nằm ngang nên không có thành phần đứng. Dây $OB$ hợp phương thẳng đứng góc $30^\circ$ nên thành phần đứng của nó kề góc $30^\circ$:"), M(r"T_{OB}\cos30^\circ-P=0"), M(r"T_{OB}=\dfrac{P}{\cos30^\circ}=\dfrac{30}{0{,}866}"), A(r"T_{OB}\approx34{,}6\ \text{N}")]),
  (r"Chiếu lên $Ox$: lực căng dây $OA$", [P(r"Thành phần ngang của $\vec T_{OB}$ đối góc $30^\circ$, cân bằng với $\vec T_{OA}$:"), M(r"T_{OB}\sin30^\circ-T_{OA}=0"), M(r"T_{OA}=34{,}6\cdot0{,}5"), A(r"T_{OA}\approx17{,}3\ \text{N}")]),
  (r"Kiểm tra", [P(r"Dây $OB$ là cạnh huyền của tam giác lực nên lớn hơn cả $P$ và $T_{OA}$ ✓."), M(r"\tan30^\circ=\dfrac{T_{OA}}{P}=\dfrac{17{,}3}{30}\approx0{,}577"), P(r"Khớp với $\tan30^\circ\approx0{,}577$ ✓.")])],
  [r"$T_{OB}\approx34{,}6\ \text{N}$", r"$T_{OA}\approx17{,}3\ \text{N}$"],
  r"Nhận dạng: vật <strong>treo bằng dây và đứng yên</strong> → tổng lực bằng không; chiếu lên hai trục, mỗi trục một phương trình."),
 sol(R_CB, [
  (r"Góc của mỗi nhánh dây", [P(r"Mỗi nhánh phủ nửa nhịp theo phương ngang và độ võng theo phương đứng:"), M(r"\tan\theta=\dfrac{h}{AB/2}=\dfrac{0{,}50}{3{,}0}"), A(r"\theta\approx9{,}46^\circ")]),
  (r"Cân bằng theo phương đứng", [P(r"Trọng lượng đèn:"), M(r"P=mg=4{,}0\cdot10=40\ \text{N}"), P(r"Hai nhánh đối xứng nên $T_1=T_2=T$. Hai thành phần đứng hướng lên cùng đỡ $P$:"), M(r"2T\sin\theta-P=0"), M(r"T=\dfrac{P}{2\sin\theta}=\dfrac{40}{2\cdot0{,}1644}"), A(r"T\approx121{,}7\ \text{N}")]),
  (r"So với trọng lượng đèn", [M(r"\dfrac{T}{P}=\dfrac{121{,}7}{40}"), A(r"\dfrac{T}{P}\approx3{,}04"), P(r"Dây chỉ võng nhẹ mà lực căng đã hơn ba lần trọng lượng đèn.")]),
  (r"Kiểm tra", [P(r"Võng càng ít thì $\theta$ càng nhỏ, $\sin\theta$ càng nhỏ, $T$ càng lớn; dây thẳng ngang ($\theta\to0$) thì $T\to\infty$."), P(r"Vì vậy dây treo vật nặng không bao giờ căng thẳng ngang được.")])],
  [r"a) $\theta\approx9{,}46^\circ$", r"b) $T\approx121{,}7\ \text{N}$ mỗi nhánh", r"c) $T\approx3{,}04\,P$"],
  r"Nhận dạng: <strong>dây võng</strong> cho nhịp và độ võng → tìm góc của dây từ hình học, rồi cân bằng theo phương đứng."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>độ lớn hai lực và góc giữa chúng</b> → nghĩ tới <b>quy tắc hình bình hành</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc(r"Cùng chiều ($\alpha=0^\circ$)", r"Khi hai lực cùng chiều, hợp lực bằng bao nhiêu?", 17, "N", 0.1,
       loi=r"Hay trừ hai độ lớn vì tưởng hai lực kéo “đối nhau”."),
  buoc(r"Ngược chiều ($\alpha=180^\circ$)", r"Khi hai lực ngược chiều, hợp lực bằng bao nhiêu?", 7.0, "N", 0.1,
       loi=r"Cộng hai độ lớn bất kể chiều, hoặc quên trị tuyệt đối.",
       ke=[(r"Lấy hiệu hai độ lớn", True),
           (r"Cộng hai độ lớn như khi cùng chiều", r"Chỉ đúng khi cùng chiều; ngược chiều các lực triệt tiêu một phần."),
           (r"Dùng $\sqrt{F_1^2+F_2^2}$", r"Căn tổng bình phương chỉ dành cho hai lực vuông góc.")]),
  buoc(r"Vuông góc ($\alpha=90^\circ$)", r"Khi hai lực vuông góc, hợp lực bằng bao nhiêu?", 13, "N", 0.1,
       loi=r"Cộng thẳng hai độ lớn hoặc quên khai căn.",
       ke=[(r"Cộng bình phương hai độ lớn rồi khai căn", True),
           (r"Cộng hai độ lớn", r"Cộng số chỉ đúng khi hai lực cùng chiều."),
           (r"Lấy hiệu hai độ lớn", r"Hiệu chỉ đúng khi hai lực ngược chiều.")]),
  buoc(r"Hợp nhau $60^\circ$", r"Khi hai lực hợp nhau góc $60^\circ$, hợp lực bằng bao nhiêu?", 15.1, "N", 0.1,
       loi=r"Cộng thẳng độ lớn bất kể góc, hoặc dùng nhầm công thức của góc đặc biệt.",
       ke=[(r"Dùng $F^2=F_1^2+F_2^2+2F_1F_2\cos\alpha$ với $\alpha=60^\circ$", True),
           (r"Dùng $\sqrt{F_1^2+F_2^2}$ như góc vuông", r"Công thức đó chỉ đúng khi $\alpha=90^\circ$, vì khi đó $\cos\alpha=0$."),
           (r"Dùng $F^2=F_1^2+F_2^2-2F_1F_2\cos\alpha$", r"Sai dấu của số hạng chứa $\cos\alpha$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hợp lực có thể bằng</b> bao nhiêu hoặc <b>cho F, hỏi góc</b> → nghĩ tới <b>khoảng từ hiệu đến tổng</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc(r"Hợp lực nhỏ nhất", r"Hợp lực nhỏ nhất bằng bao nhiêu?", 8.0, "N", 0.1,
       loi=r"Cho rằng nhỏ nhất là $0$ (hai lực triệt tiêu); điều đó chỉ xảy ra khi hai lực bằng nhau."),
  buoc(r"Hợp lực lớn nhất", r"Hợp lực lớn nhất bằng bao nhiêu?", 22, "N", 0.1,
       loi=r"Lấy căn tổng bình phương (chỉ đúng khi hai lực vuông góc) hoặc nhân hai độ lớn.",
       ke=[(r"Cho hai lực cùng chiều rồi cộng độ lớn", True),
           (r"Cho hai lực vuông góc", r"Vuông góc cho $F=\sqrt{F_1^2+F_2^2}$, nhỏ hơn tổng hai độ lớn."),
           (r"Cho hai lực ngược chiều", r"Ngược chiều cho hợp lực nhỏ nhất, không phải lớn nhất.")]),
  buoc(r"Kiểm tra $5{,}0$ N và $12$ N", r"Chọn kết luận đúng về hai giá trị $5{,}0$ N và $12$ N.",
       loi=r"Cho rằng hợp lực nhận mọi giá trị vì góc đổi được; góc chỉ làm hợp lực đổi trong một đoạn xác định.",
       lua_chon=[(r"$5{,}0$ N không thể; $12$ N có thể", True),
                 (r"Cả hai đều có thể, vì hai lực hợp góc nào cũng được", r"Góc chỉ làm hợp lực đổi trong đoạn từ hiệu đến tổng hai độ lớn; ngoài đoạn đó không thể."),
                 (r"$5{,}0$ N có thể vì nhỏ hơn cả hai lực; $12$ N không thể", r"Hợp lực có thể nhỏ hơn cả hai lực nhưng không nhỏ hơn hiệu của chúng; hợp lực vẫn bị giới hạn bởi hiệu và tổng hai độ lớn.")],
       ke=[(r"So giá trị đề hỏi với đoạn từ giá trị nhỏ nhất đến lớn nhất", True),
           (r"Tính $F$ ứng với $\alpha=90^\circ$ rồi so", r"Mỗi góc cho một giá trị của $F$; muốn biết $F$ có thể nhận giá trị nào phải xét cả đoạn."),
           (r"Cộng $F_1+F_2$ rồi so", r"Tổng chỉ là giá trị lớn nhất, khi hai lực cùng chiều.")]),
  buoc(r"Rút $\cos\alpha$ từ hợp lực $20$ N", r"$\cos\alpha$ bằng bao nhiêu?", 0.6, None, 0.01,
       loi=r"Đổi dấu khi chuyển vế hoặc quên chia cho $2F_1F_2$.",
       ke=[(r"Chuyển vế từ $F^2=F_1^2+F_2^2+2F_1F_2\cos\alpha$ rồi chia cho $2F_1F_2$", True),
           (r"Dùng $\cos\alpha=\dfrac{F}{F_1+F_2}$", r"Hệ thức này không có; góc phải rút từ công thức hình bình hành."),
           (r"Dùng $\cos\alpha=\dfrac{F_1^2+F_2^2-F^2}{2F_1F_2}$", r"Sai dấu: số hạng chứa $\cos\alpha$ cộng với $F_1^2+F_2^2$ nên $\cos\alpha=\dfrac{F^2-F_1^2-F_2^2}{2F_1F_2}$.")]),
  buoc(r"Góc giữa hai lực", r"Góc giữa hai lực bằng bao nhiêu độ?", 53.1, "°", 0.5,
       loi=r"Dùng arcsin thay cho arccos, hoặc để máy tính ở chế độ rad.",
       ke=[(r"Tra góc từ $\cos\alpha$ vừa tính, máy ở chế độ độ", True),
           (r"Tra góc bằng arcsin của giá trị vừa tính", r"Giá trị vừa tính là $\cos\alpha$, không phải $\sin\alpha$."),
           (r"Lấy $180^\circ$ trừ góc tra được", r"Góc bù ứng với $\cos$ ngược dấu, mà giá trị $\cos\alpha$ vừa tính là số dương.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực kéo xiên</b> và <b>góc so với phương ngang</b> → nghĩ tới <b>phân tích lực</b> thành hai thành phần.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Thành phần nằm ngang", r"Thành phần nằm ngang $F_x$ bằng bao nhiêu?", 34.5, "N", 0.2,
       loi=r"Nhầm cos và sin; chú ý góc cho ở đề là góc so với phương nào."),
  buoc(r"Thành phần thẳng đứng", r"Thành phần thẳng đứng $F_y$ bằng bao nhiêu?", 28.9, "N", 0.2,
       loi=r"Dùng cos cho thành phần đứng, hoặc lấy $F-F_x$ (hiệu độ lớn, không phải thành phần vuông góc).",
       ke=[(r"Dùng $F_y=F\sin\alpha$ vì $F_y$ đối diện góc $\alpha$", True),
           (r"Lấy $F_y=F-F_x$", r"Hai thành phần vuông góc nên $F^2=F_x^2+F_y^2$; không có hệ thức hiệu độ lớn."),
           (r"Dùng $F_y=F\cos\alpha$", r"Với $\alpha$ là góc so với phương ngang, $\cos\alpha$ dành cho thành phần ngang; thành phần đứng đối diện góc $\alpha$ nên dùng $\sin\alpha$.")]),
  buoc(r"Tác dụng của hai thành phần", r"Thành phần nào làm thùng bớt ép xuống sàn?",
       loi=r"Cho rằng thành phần lớn hơn thì quyết định mọi tác dụng; mỗi thành phần chỉ tác dụng theo phương của nó.",
       lua_chon=[(r"$F_y$, vì nó hướng lên và vuông góc với sàn", True),
                 (r"$F_x$, vì nó có độ lớn lớn hơn", r"Độ lớn không quyết định tác dụng của một thành phần."),
                 (r"Cả hai như nhau", r"Hai thành phần vuông góc nên tác dụng độc lập: một theo phương ngang, một theo phương đứng.")],
       ke=[(r"Xét tác dụng của từng thành phần theo phương của nó", True),
           (r"Cộng $F_x+F_y$ để biết tác dụng chung", r"Hai thành phần vuông góc, không cộng độ lớn; tác dụng được xét riêng từng phương."),
           (r"Chỉ xét $F$, bỏ qua các thành phần", r"Muốn biết tác dụng theo từng phương thì phải dùng thành phần của phương ấy.")]),
  buoc(r"Dây hợp với phương ngang góc $60^\circ$", r"Với góc mới, $F_x$ bằng bao nhiêu?", 22.5, "N", 0.2,
       loi=r"Giữ nguyên $F_x$ cũ vì $F$ không đổi, hoặc dùng sin cho thành phần ngang.",
       ke=[(r"Chiếu $\vec F$ lên $Ox$ với góc mới $60^\circ$", True),
           (r"Giữ nguyên $F_x$ cũ vì $F$ không đổi", r"$F_x$ phụ thuộc cả góc: cùng $F$ mà đổi góc thì thành phần ngang đổi."),
           (r"Dùng $F_x=F\sin60^\circ$", r"Góc vẫn là góc so với phương ngang nên thành phần ngang dùng $\cos$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật trên mặt dốc nghiêng góc α</b> → nghĩ tới <b>phân tích trọng lực</b> dọc dốc và vuông góc dốc.",
  cap_do=2, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Trọng lượng", r"Trọng lượng $P$ của thùng bằng bao nhiêu?", 80, "N", 0.5,
       loi=r"Quên nhân với $g$: khối lượng đo bằng kilôgam, trọng lượng (lực) đo bằng niutơn."),
  buoc(r"Thành phần dọc dốc", r"Thành phần dọc dốc $P_x$ bằng bao nhiêu?", 51.4, "N", 0.3,
       loi=r"Dùng cos cho thành phần dọc dốc: nhầm góc nghiêng của dốc với góc giữa $\vec P$ và mặt dốc.",
       ke=[(r"Dùng $P_x=P\sin\alpha$ vì $P_x$ đối diện góc nghiêng $\alpha$", True),
           (r"Dùng $P_x=P\cos\alpha$ như khi kéo xiên", r"Khi kéo xiên, $\alpha$ là góc giữa lực và phương chiếu; ở dốc, trục dọc dốc hợp với $\vec P$ góc $90^\circ-\alpha$ nên cos đổi thành sin."),
           (r"Dùng $P_x=P\tan\alpha$", r"Tang chỉ là tỉ số hai thành phần; thành phần của $\vec P$ không có hệ số $\tan\alpha$.")]),
  buoc(r"Thành phần vuông góc dốc", r"Thành phần vuông góc dốc $P_y$ bằng bao nhiêu?", 61.3, "N", 0.3,
       loi=r"Dùng cùng một hàm (sin) cho cả hai thành phần, hoặc lấy $P-P_x$.",
       ke=[(r"Dùng $P_y=P\cos\alpha$ vì $P_y$ kề góc nghiêng $\alpha$", True),
           (r"Dùng $P_y=P-P_x$", r"Hai thành phần vuông góc nên $P^2=P_x^2+P_y^2$; không có hệ thức hiệu độ lớn."),
           (r"Dùng $P_y=P\sin\alpha$ giống $P_x$", r"Hai thành phần vuông góc không thể cùng một công thức.")]),
  buoc(r"Dốc thoải hơn ($20^\circ$)", r"Với dốc nghiêng $20^\circ$, $P_x$ bằng bao nhiêu?", 27.4, "N", 0.3,
       loi=r"Giữ nguyên $P_x$ cũ vì trọng lượng không đổi, hoặc dùng cos cho thành phần dọc dốc.",
       ke=[(r"Giữ công thức cũ của $P_x$, thay góc mới $20^\circ$", True),
           (r"Giữ nguyên $P_x$ vì trọng lượng không đổi", r"$P_x$ phụ thuộc góc nghiêng."),
           (r"Dùng $P_x=P\cos20^\circ$", r"Thành phần dọc dốc dùng $\sin\alpha$; dùng cos sẽ cho $P_x$ gần bằng $P$, vô lí khi dốc gần nằm ngang.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy vật <b>treo bằng dây và đứng yên</b> → nghĩ tới <b>tổng lực bằng không</b>, chiếu lên hai trục.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Trọng lực và hệ trục", r"Lực của dây treo vật lên vòng nhẫn (bằng trọng lượng vật) là bao nhiêu?", 30, "N", 0.3,
       loi=r"Quên nhân với $g$ rồi chiếu các lực với trọng lượng bằng khối lượng."),
  buoc(r"Chiếu lên $Oy$: lực căng dây $OB$", r"Lực căng dây $OB$ bằng bao nhiêu?", 34.6, "N", 0.3,
       loi=r"Nhầm sin và cos khi chiếu, hoặc cho $T_{OB}$ bằng trọng lượng.",
       ke=[(r"Cho thành phần đứng của $T_{OB}$ cân bằng với $P$", True),
           (r"Chiếu lên $Oy$ với $T_{OB}\sin30^\circ=P$", r"Nhầm hàm khi chiếu: $30^\circ$ là góc so với phương thẳng đứng."),
           (r"Cho $T_{OB}=P$ vì dây $OB$ đỡ vật", r"Dây $OB$ xiên nên chỉ thành phần đứng của nó đỡ vật; $T_{OB}$ không thể bằng $P$.")]),
  buoc(r"Chiếu lên $Ox$: lực căng dây $OA$", r"Lực căng dây $OA$ bằng bao nhiêu?", 17.3, "N", 0.2,
       loi=r"Cho $T_{OA}$ bằng trọng lượng vì dây $OA$ đang giữ vật, hoặc cho hai dây bằng nhau.",
       ke=[(r"Cho $T_{OA}$ cân bằng với thành phần ngang của $T_{OB}$", True),
           (r"Cho $T_{OA}=P$ vì dây $OA$ ngang", r"Dây $OA$ nằm ngang nên không đỡ trọng lượng; nó chỉ cân bằng thành phần ngang của $T_{OB}$."),
           (r"Cho $T_{OA}=T_{OB}$", r"Hai dây không đối xứng (một ngang, một xiên) nên hai lực căng khác nhau.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>dây võng</b> cho nhịp và độ võng → nghĩ tới <b>góc của dây</b>, rồi <b>cân bằng theo phương đứng</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Góc của mỗi nhánh dây", r"Góc $\theta$ giữa mỗi nhánh dây và phương ngang bằng bao nhiêu độ?", 9.46, "°", 0.1,
       loi=r"Dùng nhầm độ dài nhịp trong tỉ số."),
  buoc(r"Cân bằng theo phương đứng", r"Lực căng $T$ của mỗi nhánh dây bằng bao nhiêu?", 121.7, "N", 0.6,
       loi=r"Cho mỗi nhánh đỡ một nửa trọng lượng rồi coi đó là lực căng, quên rằng dây xiên nên lực căng lớn hơn thành phần đứng.",
       ke=[(r"Cho hai thành phần đứng của hai nhánh cùng đỡ $P$, rồi rút $T$ qua $\sin\theta$", True),
           (r"Cho mỗi nhánh đỡ $\dfrac{P}{2}$, nên $T=\dfrac{P}{2}$", r"Chỉ thành phần đứng của mỗi nhánh đỡ $\dfrac{P}{2}$; lực căng $T$ lớn hơn thành phần ấy vì dây xiên."),
           (r"Cho $T=P$ vì đèn treo bằng dây", r"Có hai nhánh cùng đỡ và dây xiên, không thể suy ra $T$ bằng $P$.")]),
  buoc(r"So với trọng lượng đèn", r"Lực căng gấp bao nhiêu lần trọng lượng của đèn?", 3.04, None, 0.05,
       loi=r"Đảo ngược tỉ số, hoặc chia lực căng cho khối lượng (khác đơn vị với trọng lượng).",
       ke=[(r"Chia $T$ cho trọng lượng $P=mg$", True),
           (r"Chia $P$ cho $T$", r"Cho tỉ số nhỏ hơn $1$: đảo ngược, vì “gấp mấy lần” hỏi $T$ so với $P$."),
           (r"Chia $T$ cho khối lượng $m$", r"Khối lượng (kg) và lực (N) khác đơn vị; phải so với trọng lượng $P=mg$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập (idx 0-based trong old/58.json), xếp dễ → khó ═════════════
# VD6 (idx5): ba lực 120° · VD8 (idx7): khiêng thùng · VD9 (idx8): ván bắc mương · VD10 (idx9): ba lực song song
# VD11 (idx10): đèn giữa dây 150° · VD13 (idx12): vòng nhẫn 45°
ORDER = [8, 5, 12, 7, 9]   # bỏ VD11 (idx10): thiếu lời giải ý a; ảnh không kiểm được
MUC = {8: "Dễ", 5: "Trung bình", 12: "Trung bình", 7: "Khó", 9: "Nâng cao"}
# VD10: bản gốc dính thêm ~7 KB lý thuyết phía sau lời giải → cắt ở câu kết luận
_k = "cách B một đoạn 0,35 m</p>"
assert _k in OLD[9]["body_html"]
OLD[9]["body_html"] = OLD[9]["body_html"][:OLD[9]["body_html"].index(_k) + len(_k)]
for _i, _key in ((5, "Ví dụ 6"), (7, "Ví dụ 8"), (8, "Ví dụ 9"), (9, "Ví dụ 10"), (10, "Ví dụ 1"), (12, "Ví dụ 3")):
    assert _key in OLD[_i]["body_html"]

def _sub(i, a, c):
    assert a in OLD[i]["body_html"], (i, a)
    OLD[i]["body_html"] = OLD[i]["body_html"].replace(a, c)
_sub(8, r"F_{1}=80NF_{2}=160N", r"F_{1}=80N\\ F_{2}=160N")
OLD[8]["body_html"] += "<p>Vậy tấm ván tác dụng lên điểm tựa A một lực $F_1=80\\ \\text{N}$.</p>"
_sub(7, r"d_{1}=\frac{4}{3}md_{2}=\frac{2}{3}m", r"d_{1}=\frac{4}{3}m\\ d_{2}=\frac{2}{3}m")
OLD[7]["body_html"] += "<p>Vậy thùng hàng cách người đi sau $\\frac{2}{3}\\ \\text{m}$ (cách người đi trước $\\frac{4}{3}\\ \\text{m}$).</p>"
_sub(9, r"2O_{1}A-5O_{1}B=0O_{1}A+O_{1}B=1", r"2O_{1}A-5O_{1}B=0\\ O_{1}A+O_{1}B=1")
_sub(9, r"O_{1}A=\frac{5}{7}mO_{1}B=\frac{2}{7}m", r"O_{1}A=\frac{5}{7}m\\ O_{1}B=\frac{2}{7}m")
_sub(9, r"7O_{1}O_{2}-3O_{2}I=0O_{1}O_{2}+O_{2}I=\frac{3}{14}", r"7O_{1}O_{2}-3O_{2}I=0\\ O_{1}O_{2}+O_{2}I=\frac{3}{14}")
_sub(9, r"O_{1}O_{2}=\frac{9}{140}mO_{2}I=\frac{3}{20}=0,15m", r"O_{1}O_{2}=\frac{9}{140}m\\ O_{2}I=\frac{3}{20}=0,15m")
_sub(5, "2.5cos60^{0}", r"2\cdot5\cos60^{0}")
for _i in (5, 7, 8, 9, 12):
    _h = OLD[_i]["body_html"]
    _h = re.sub(r'alt="[^"]*"', 'alt=""', _h)
    _h = _h.replace("=&gt;", r"\Rightarrow ").replace("=>", r"\Rightarrow ")
    OLD[_i]["body_html"] = _h
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)

write(J, 58, "Bài 13. Tổng hợp và phân tích lực. Cân bằng lực", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
