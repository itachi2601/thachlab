"""Bài 79 — "Bài 34. Khối lượng riêng. Áp suất chất lỏng" (Vật lí 10, chương 7). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-57.py / 58. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-79.py  → ghi scripts/data/bai-tap-mau/79.json
Dạng xếp theo hệ bắc cầu (quét: scripts/logs/batch-ra-soat/ket-qua/79.quet-dang.json). Hình: hinh_79.py.
Ví dụ cũ (old/79.json, 3 mục): VD3 (thùng trụ 1,5 m, áp suất đáy và điểm A) → Dạng 3 (đổi số: 1,8 m, A cách đáy 50 cm, thêm áp kế và đổi chiều);
VD1 (quả cầu 20 cm³ lơ lửng, F_A = 0,196 N, g = 9,8) và VD2 (lực kế + bình tràn, m = 1,35 kg, d = 2,7·10⁴ N/m³) → tự luận, giữ nguyên lời giải gốc
(đã kiểm lại: 1000·9,8·20·10⁻⁶ = 0,196 N đúng; 10000·5·10⁻⁴ = 5 N, P = 8,5 + 5 = 13,5 N, d = 13,5/5·10⁻⁴ = 2,7·10⁴ N/m³ đúng).
Không bỏ ví dụ nào."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_79 import BUILD

J = os.path.join(HERE, "79.json")
OLD = json.load(open(os.path.join(HERE, "old/79.json")))["questions"]
T152 = "Khối lượng riêng và áp suất chất lỏng theo độ sâu"
T153 = "Lực đẩy Archimedes và điều kiện nổi"
topics = {t["name"]: t for t in json.load(open(os.path.join(HERE, "../question-topics.json")))}
assert topics[T152]["lesson_id"] == 79 and topics[T153]["lesson_id"] == 79

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
g = 10.0
# D1
m, a, b_, c = 1.26, 3.0, 4.0, 15.0
V = a * b_ * c * 1e-6; ok("D1 V", V, 1.8e-4, 1e-12); rho = m / V; ok("D1 ρ", rho, 7000, 1e-6)
Fk = m * g; ok("D1 F", Fk, 12.6, 1e-9)
S1, S2 = b_ * c * 1e-4, a * b_ * 1e-4; ok("D1 S1", S1, 6.0e-3, 1e-12); ok("D1 S2", S2, 1.2e-3, 1e-12)
p1, p2 = Fk / S1, Fk / S2; ok("D1 p1", p1, 2100, 1e-6); ok("D1 p2", p2, 10500, 1e-6); ok("D1 tỉ số", p2 / p1, S1 / S2, 1e-9)
# các cách sai (khác đáp số đúng)
assert abs(Fk / S1 - m / S1) > 1000 and abs(p1 - Fk / S2) > 1000 and abs(p2 - p1 / (S1 / S2)) > 5000   # quên g; dùng nhầm mặt; đảo tỉ số
assert abs(p1 * (S2 / S1) - p2) > 5000 and abs(p1 * (S2 / S1) - 420) < 1e-6
assert abs(p1 - Fk / (b_ * c)) > 1000                                                               # để S ở cm²
assert abs(rho - m / (a * b_ * c * 1e-3)) > 1000 and abs(rho - m / (a * b_ * c)) > 1000                # đổi cm³ sai bậc
# D2
rho_o, h1, hM, Sv = 800.0, 2.5, 1.0, 20e-4
q1 = rho_o * g * h1; qM = rho_o * g * hM; Fv = q1 * Sv
ok("D2 đáy", q1, 20000, 1e-6); ok("D2 M", qM, 8000, 1e-6); ok("D2 F", Fv, 40, 1e-9); ok("D2 Δp", rho_o * g * (h1 - hM), q1 - qM, 1e-9); ok("D2 Δp=12000", q1 - qM, 12000, 1e-9)
assert abs(rho_o * g * (h1 - hM) - qM) > 1000 and abs(0.5 * q1 - qM) > 1000                         # đo h từ đáy; lấy nửa
assert abs(q1 * 20 - Fv) > 100 and abs(qM * Sv - Fv) > 10                                         # S ở cm²; dùng áp suất M
# D3
pa, rho_w, H3, hA_floor = 1.0e5, 1000.0, 1.8, 0.50
d_n = rho_w * g * H3; ok("D3 do nước", d_n, 18000, 1e-6); ok("D3 tuyệt đối đáy", pa + d_n, 118000, 1e-6)
hA = H3 - hA_floor; ok("D3 hA", hA, 1.3, 1e-12); pdu = rho_w * g * hA; ok("D3 dư A", pdu, 13000, 1e-6); pA = pa + pdu; ok("D3 abs A", pA, 113000, 1e-6)
ok("D3 kiểm", (pa + d_n) - pA, rho_w * g * hA_floor, 1e-6)
pB = 1.12e5; hB = (pB - pa) / (rho_w * g); ok("D3 hB", hB, 1.2, 1e-9); assert hB < H3
assert abs(rho_w * g * hA_floor - pdu) > 1000 and abs((pa + pdu) - pdu) > 1000                        # h từ đáy; cộng pa vào số chỉ áp kế
assert abs((pa - pdu) - pA) > 1000 and abs((pa + d_n) - pA) > 1000                                  # pa trừ; giữ p đáy
assert abs(pB / (rho_w * g) - hB) > 1 and abs((pB - pa) / rho_w - hB) > 1                           # chia cả pa; bỏ g
# D4
r1, r2, hh1 = 1000.0, 13600.0, 0.204
pcol = r1 * g * hh1; ok("D4 p cột nước", pcol, 2040, 1e-9)
hh2 = pcol / (r2 * g); ok("D4 h2", hh2 * 100, 1.5, 1e-9)
ok("D4 chênh", (hh1 - hh2) * 100, 18.9, 1e-9)
hh1b = r2 * 0.030 / r1; ok("D4 h1 mới", hh1b * 100, 40.8, 1e-9)
ok("D4 kiểm", r1 * hh1b, r2 * 0.030, 1e-9); ok("D4 tỉ số", hh1 / hh2, r2 / r1, 1e-9)
assert abs(hh1 * 100 - hh2 * 100) > 1 and abs(hh1 * 100 * r2 / r1 - hh2 * 100) > 1 and abs((hh1 + hh2) * 100 - 18.9) > 1       # cùng mực; đảo tỉ số; cộng
assert abs(hh1 * 100 - 18.9) > 1 and abs(3.0 * r1 / r2 - 40.8) > 1 and abs(20.4 + 3.0 - 40.8) > 1                              # lấy h1; đảo tỉ số; cộng 3,0
# D5
S5, H5, m5 = 0.20 * 0.20, 0.10, 2.4
V5 = S5 * H5; ok("D5 V", V5, 4.0e-3, 1e-12); r5 = m5 / V5; ok("D5 ρ", r5, 600, 1e-9); assert r5 < 1000
FA = m5 * g; ok("D5 F_A", FA, 24, 1e-9)
Vch = FA / (1000 * g); ok("D5 V chìm", Vch, 2.4e-3, 1e-12); hch = Vch / S5; ok("D5 h chìm", hch * 100, 6.0, 1e-9); assert hch < H5
FAmax = 1000 * g * V5; ok("D5 F_A max", FAmax, 40, 1e-9); mp = FAmax / g - m5; ok("D5 m'", mp, 1.6, 1e-9)
ok("D5 kiểm", (m5 + mp) * g, FAmax, 1e-9); ok("D5 thêm 4,0 cm", (1000 * g * S5 * 0.01) * 4.0, mp * g, 1e-9)
assert abs(1000 * g * V5 - FA) > 5 and abs(m5 - FA) > 5                                           # V cả khối; quên g
assert abs(H5 * 100 * 1000 / r5 - hch * 100) > 5 and abs(Vch / 0.20 * 100 - hch * 100) > 3       # tỉ số ngược; chia cho một cạnh
assert abs(1000 * g * V5 / g - mp) > 1 and abs(FA / g - m5) < 1e-9 and abs((FA / g - m5) - mp) > 1  # nước chiếm chỗ; dùng phần chìm cũ → 0
# Tự luận cũ
ok("TL1", 1000 * 9.8 * 20e-6, 0.196, 1e-12)
ok("TL2 F_A", 10000 * 0.0005, 5, 1e-12); ok("TL2 P", 8.5 + 5, 13.5, 1e-12); ok("TL2 d", 13.5 / 0.0005, 2.7e4, 1e-6)
# nhan_dang ≤ 25 chữ được kiểm sau khi dựng


# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Khối lượng riêng và áp suất p = F/S (đổi đơn vị)", topic=T152,
      problem_html=r"""<p>Một khối kim loại hình hộp chữ nhật có kích thước $3{,}0\ \text{cm}\times4{,}0\ \text{cm}\times15\ \text{cm}$, khối lượng $1{,}26\ \text{kg}$. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính khối lượng riêng của kim loại, theo kg/m³.</li>
<li>Đặt khối nằm trên mặt bàn nằm ngang bằng mặt lớn nhất ($4{,}0\ \text{cm}\times15\ \text{cm}$). Tính áp suất khối ép lên mặt bàn.</li>
<li>Dựng khối đứng trên mặt nhỏ nhất ($3{,}0\ \text{cm}\times4{,}0\ \text{cm}$). Tính áp suất khối ép lên mặt bàn lúc này.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Áp suất chất lỏng theo độ sâu: p = ρgh", topic=T152,
      problem_html=r"""<p>Một bể chứa dầu hoả có khối lượng riêng $0{,}80\ \text{g/cm}^3$, mực dầu cao $2{,}5\ \text{m}$. Lấy $g=10\ \text{m/s}^2$. Chỉ xét áp suất do dầu gây ra.</p>
<ol type="a"><li>Tính áp suất do dầu gây ra ở đáy bể.</li>
<li>Điểm $M$ trong dầu cách mặt thoáng $1{,}0\ \text{m}$. Tính áp suất do dầu gây ra tại $M$.</li>
<li>Ở đáy bể có một nắp van tròn diện tích $20\ \text{cm}^2$. Tính áp lực của dầu lên nắp van.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Áp suất tuyệt đối và áp suất dư", topic=T152,
      problem_html=r"""<p>Một thùng hình trụ cao $1{,}8\ \text{m}$, miệng hở, đựng đầy nước có khối lượng riêng $1000\ \text{kg/m}^3$. Áp suất khí quyển là $1{,}0\cdot10^5\ \text{Pa}$; lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính áp suất do nước gây ra ở đáy thùng và áp suất tuyệt đối tại đáy thùng.</li>
<li>Điểm $A$ trong nước cách đáy thùng $50\ \text{cm}$. Tính áp suất tuyệt đối tại $A$ và số chỉ của áp kế (đo áp suất dư) gắn tại $A$.</li>
<li>Một điểm $B$ trong thùng có áp suất tuyệt đối $1{,}12\cdot10^5\ \text{Pa}$. Tính khoảng cách từ $B$ đến mặt thoáng.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Bình thông nhau chứa hai chất lỏng không hoà tan", topic=T152,
      problem_html=r"""<p>Một ống chữ U tiết diện đều, hai đầu hở, chứa thuỷ ngân (khối lượng riêng $13\,600\ \text{kg/m}^3$). Rót nước (khối lượng riêng $1000\ \text{kg/m}^3$) vào nhánh trái, tạo cột nước cao $20{,}4\ \text{cm}$ tính từ mặt phân cách nước – thuỷ ngân. Hai chất lỏng đứng yên.</p>
<ol type="a"><li>Mặt thuỷ ngân ở nhánh phải cao hơn mặt phân cách bao nhiêu centimet?</li>
<li>Mặt nước ở nhánh trái cao hơn mặt thuỷ ngân ở nhánh phải bao nhiêu centimet?</li>
<li>Để mặt thuỷ ngân ở nhánh phải cao hơn mặt phân cách $3{,}0\ \text{cm}$, cột nước ở nhánh trái phải cao bao nhiêu centimet?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Lực đẩy Archimedes: khối nổi và điều kiện chìm hẳn", topic=T153,
      problem_html=r"""<p>Một khối gỗ hình hộp chữ nhật có đáy $20\ \text{cm}\times20\ \text{cm}$, cao $10\ \text{cm}$, khối lượng $2{,}4\ \text{kg}$, được thả vào nước (khối lượng riêng $1000\ \text{kg/m}^3$) sao cho đáy nằm ngang. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính khối lượng riêng của gỗ. Khối nổi hay chìm trong nước?</li>
<li>Khi khối đứng yên trên mặt nước, tính lực đẩy Archimedes tác dụng lên khối.</li>
<li>Tính chiều cao phần khối chìm trong nước.</li>
<li>Đặt lên mặt trên của khối một vật nhỏ (thể tích không đáng kể) để khối vừa chìm hẳn, mặt trên ngang với mặt nước. Bể đủ rộng để mực nước coi như không đổi. Tính khối lượng tối thiểu của vật.</li></ol>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“khối kim loại hình hộp chữ nhật $3{,}0\ \text{cm}\times4{,}0\ \text{cm}\times15\ \text{cm}$”", r"Ba cạnh: $3{,}0$; $4{,}0$; $15$ (cm)", r"⚠ Thể tích hình hộp là tích ba cạnh; đổi cm³ ra m³ trước khi thế số"),
  (r"“khối lượng $1{,}26\ \text{kg}$”", r"$m=1{,}26\ \text{kg}$", r"Khối lượng riêng: khối lượng của một đơn vị thể tích"),
  (r"“Lấy $g=10\ \text{m/s}^2$”", r"$g=10\ \text{m/s}^2$", r"Áp lực của khối lên bàn do trọng lượng của khối"),
  (r"“a) khối lượng riêng của kim loại, theo kg/m³”", r"Cần $\rho$ (kg/m³)", r"Đại lượng cần tìm"),
  (r"“b) nằm trên mặt bàn bằng mặt lớn nhất ($4{,}0\ \text{cm}\times15\ \text{cm}$)”", r"Mặt chạm bàn: $4{,}0\times15\ \text{cm}^2$", r"⚠ $S$ là diện tích mặt chạm bàn; đổi cm² ra m²"),
  (r"“c) dựng đứng trên mặt nhỏ nhất ($3{,}0\ \text{cm}\times4{,}0\ \text{cm}$)”", r"Mặt chạm bàn: $3{,}0\times4{,}0\ \text{cm}^2$", r"Cùng một khối; mặt chạm bàn đổi thì diện tích $S$ đổi"),
  (r"“Tính áp suất khối ép lên mặt bàn”", r"Cần áp suất ở hai tư thế (Pa)", r"Đại lượng cần tìm")],
 [(r"“bể chứa dầu hoả có khối lượng riêng $0{,}80\ \text{g/cm}^3$”", r"$\rho=0{,}80\ \text{g/cm}^3$", r"⚠ Đổi $\rho$ sang kg/m³ trước khi thế số"),
  (r"“mực dầu cao $2{,}5\ \text{m}$”", r"Đáy ở độ sâu $2{,}5\ \text{m}$", r"⚠ $h$ là độ sâu đo từ mặt thoáng xuống điểm đang xét"),
  (r"“Chỉ xét áp suất do dầu gây ra”", r"Không tính khí quyển", r"Áp suất do chất lỏng gây ra là phần $\rho gh$"),
  (r"“a) áp suất do dầu gây ra ở đáy bể”", r"Cần $p$ ở đáy (Pa)", r"Đại lượng cần tìm"),
  (r"“b) điểm $M$ trong dầu cách mặt thoáng $1{,}0\ \text{m}$”", r"Độ sâu của $M$: $1{,}0\ \text{m}$", r"Cùng chất lỏng, độ sâu khác thì áp suất khác"),
  (r"“c) nắp van tròn diện tích $20\ \text{cm}^2$ ở đáy bể”", r"$S=20\ \text{cm}^2$ (đặt tại đáy)", r"Áp lực từ áp suất và diện tích; đổi cm² ra m²"),
  (r"“Lấy $g=10\ \text{m/s}^2$”", r"$g=10\ \text{m/s}^2$", r"Hệ số trong $\rho gh$")],
 [(r"“thùng hình trụ cao $1{,}8\ \text{m}$, miệng hở, đựng đầy nước”", r"Mặt thoáng ở miệng thùng, cao $1{,}8\ \text{m}$ so với đáy", r"⚠ Miệng thùng hở thì mặt thoáng chịu áp suất nào?"),
  (r"“khối lượng riêng $1000\ \text{kg/m}^3$”, “$p_a=1{,}0\cdot10^5\ \text{Pa}$”", r"$\rho=1000\ \text{kg/m}^3$; $p_a=1{,}0\cdot10^5\ \text{Pa}$", r"Áp suất tại điểm ở độ sâu $h$ gồm hai phần"),
  (r"“a) áp suất do nước gây ra ở đáy … và áp suất tuyệt đối tại đáy”", r"Hai đại lượng khác nhau tại cùng một điểm", r"⚠ Hai cách hỏi này khác nhau ở điểm nào?"),
  (r"“b) điểm $A$ … cách đáy thùng $50\ \text{cm}$”", r"$A$ cao $0{,}50\ \text{m}$ so với đáy", r"⚠ Độ cao so với đáy có phải độ sâu $h$ không?"),
  (r"“số chỉ của áp kế (đo áp suất dư) gắn tại $A$”", r"Cần $p$ dư tại $A$ (Pa)", r"Áp suất dư: phần vượt trên khí quyển"),
  (r"“c) điểm $B$ … áp suất tuyệt đối $1{,}12\cdot10^5\ \text{Pa}$”", r"$p_B=1{,}12\cdot10^5\ \text{Pa}$; cần $h_B$ (m)", r"Đổi chiều: biết áp suất, tìm độ sâu")],
 [(r"“ống chữ U tiết diện đều, hai đầu hở, chứa thuỷ ngân”", r"$\rho_2=13\,600\ \text{kg/m}^3$; hai mặt thoáng cùng chịu $p_a$", r"⚠ Hai nhánh hở: $p_a$ như nhau ở hai bên"),
  (r"“Rót nước … vào nhánh trái”", r"$\rho_1=1000\ \text{kg/m}^3$", r"Nước và thuỷ ngân không hoà tan, có mặt phân cách"),
  (r"“cột nước cao $20{,}4\ \text{cm}$ tính từ mặt phân cách”", r"$h_1=20{,}4\ \text{cm}$", r"$h$ đo từ mặt phân cách đến mặt thoáng của nước"),
  (r"“Hai chất lỏng đứng yên”", r"Cân bằng áp suất", r"⚠ Điều kiện để hai điểm có cùng áp suất là gì?"),
  (r"“a) mặt thuỷ ngân ở nhánh phải cao hơn mặt phân cách”", r"Cần $h_2$ (cm)", r"Đại lượng cần tìm"),
  (r"“b) mặt nước ở nhánh trái cao hơn mặt thuỷ ngân ở nhánh phải”", r"Cần hiệu hai mực (cm)", r"Đại lượng cần tìm"),
  (r"“c) mặt thuỷ ngân ở nhánh phải cao hơn mặt phân cách $3{,}0\ \text{cm}$”", r"$h_2=3{,}0\ \text{cm}$; cần $h_1$ (cm)", r"Đổi chiều: biết cột thuỷ ngân, tìm cột nước")],
 [(r"“khối gỗ hình hộp chữ nhật có đáy $20\ \text{cm}\times20\ \text{cm}$, cao $10\ \text{cm}$”", r"$S=0{,}040\ \text{m}^2$; $H=0{,}10\ \text{m}$", r"Thể tích hộp: $V=S\cdot H$"),
  (r"“khối lượng $2{,}4\ \text{kg}$”, “Lấy $g=10\ \text{m/s}^2$”", r"$m=2{,}4\ \text{kg}$; $g=10\ \text{m/s}^2$", r"Khối lượng riêng $\rho=m/V$; trọng lượng $P=mg$"),
  (r"“thả vào nước (khối lượng riêng $1000\ \text{kg/m}^3$)”", r"$\rho_\ell=1000\ \text{kg/m}^3$", r"⚠ Lực đẩy Archimedes: $F_A=\rho_\ell gV$; xác định $V$ là thể tích của phần nào"),
  (r"“a) khối lượng riêng của gỗ. Khối nổi hay chìm”", r"Cần $\rho_{\text{gỗ}}$; so với $\rho_\ell$", r"Vật đặc: so $\rho_{\text{vật}}$ với $\rho_\ell$"),
  (r"“b) khi khối đứng yên trên mặt nước”", r"Khối cân bằng", r"⚠ Khối đang ở trạng thái nào?"),
  (r"“c) chiều cao phần khối chìm”", r"Cần $h'$ (cm)", r"Đại lượng cần tìm"),
  (r"“d) vật nhỏ … để khối vừa chìm hẳn, mặt trên ngang với mặt nước”", r"Cần $m'$ tối thiểu (kg)", r"Mốc “vừa chìm hẳn” cho biết điều gì về $V$?")],
]

# ═════════════ Lời giải từng bước ═════════════
R1 = [r"<strong>Khái niệm:</strong> khối lượng riêng $\rho=m/V$ (kg/m³); áp lực $F$ vuông góc mặt ép; áp suất $p=F/S$ (Pa).",
      r"Đổi: $1\ \text{cm}^3=10^{-6}\ \text{m}^3$ · $1\ \text{cm}^2=10^{-4}\ \text{m}^2$.",
      r"Khối đặt trên bàn: áp lực lên bàn bằng trọng lượng, $F=mg$.",
      r"⚠ <strong>Điều kiện:</strong> đổi mọi đại lượng về kg, m, N trước khi thế số; $S$ là diện tích mặt chạm bàn."]
R2 = [r"<strong>Khái niệm:</strong> chất lỏng đứng yên gây áp suất theo mọi phương; phần do chất lỏng tại độ sâu $h$ là $\rho gh$.",
      r"$h$ đo từ mặt thoáng xuống điểm đang xét · $1\ \text{g/cm}^3=1000\ \text{kg/m}^3$.",
      r"Hai điểm chênh nhau độ sâu $\Delta h$: $\Delta p=\rho g\Delta h$.",
      r"Áp lực lên diện tích $S$: $F=pS$ ($S$ đổi ra m²).",
      r"⚠ <strong>Điều kiện:</strong> đề hỏi “do dầu gây ra” thì không cộng $p_a$."]
R3 = [r"<strong>Khái niệm:</strong> áp suất tuyệt đối tại điểm ở độ sâu $h$: $p=p_a+\rho gh$.",
      r"Áp suất dư (số chỉ áp kế) là phần vượt trên khí quyển: $p-p_a=\rho gh$.",
      r"Áp suất “do chất lỏng gây ra” cũng là $\rho gh$.",
      r"Đổi chiều: $h=\dfrac{p-p_a}{\rho g}$.",
      r"⚠ <strong>Điều kiện:</strong> miệng thùng hở nên mặt thoáng chịu $p_a$; $h$ đo từ mặt thoáng xuống điểm."]
R4 = [r"<strong>Khái niệm:</strong> trong cùng một chất lỏng đứng yên, hai điểm cùng mức ngang có cùng áp suất.",
      r"Hai chất lỏng không hoà tan: chọn $A$ ở mặt phân cách, $B$ cùng mức ngang với $A$ ở nhánh kia.",
      r"$p_A=p_B$ nên $p_a+\rho_1gh_1=p_a+\rho_2gh_2$, tức $\rho_1h_1=\rho_2h_2$.",
      r"⚠ <strong>Điều kiện:</strong> hai nhánh hở (cùng $p_a$); $A$ và $B$ cùng nằm trong thuỷ ngân."]
R5 = [r"<strong>Khái niệm:</strong> khối lượng riêng $\rho=m/V$; lực đẩy Archimedes hướng lên, $F_A=\rho_\ell gV$.",
      r"Vật đặc: $\rho_{\text{vật}}\lt\rho_\ell$ thì nổi; $\rho_{\text{vật}}\gt\rho_\ell$ thì chìm; bằng nhau thì lơ lửng.",
      r"Trọng lượng $P=mg$; vật đứng yên thì các lực tác dụng cân bằng nhau.",
      r"⚠ <strong>Điều kiện:</strong> $V$ trong $F_A$ là thể tích phần chìm, không phải cả vật khi vật chưa chìm hết."]

SOLS = [
 sol(R1, [
  (r"Khối lượng riêng", [P(r"Thể tích hộp, đổi ra m³:"), M(r"V=3{,}0\cdot4{,}0\cdot15=180\ \text{cm}^3=1{,}8\cdot10^{-4}\ \text{m}^3"),
                         P(r"Khối lượng riêng:"), M(r"\rho=\dfrac{m}{V}=\dfrac{1{,}26}{1{,}8\cdot10^{-4}}"), A(r"\rho=7000\ \text{kg/m}^3"), P(r"Tức $7{,}0\ \text{g/cm}^3$.")]),
  (r"Áp suất khi khối nằm", [P(r"Áp lực lên bàn bằng trọng lượng của khối:"), M(r"F=mg=1{,}26\cdot10=12{,}6\ \text{N}"),
                            P(r"Mặt chạm bàn $4{,}0\times15=60\ \text{cm}^2=6{,}0\cdot10^{-3}\ \text{m}^2$:"), M(r"p_1=\dfrac{F}{S_1}=\dfrac{12{,}6}{6{,}0\cdot10^{-3}}"), A(r"p_1=2100\ \text{Pa}")]),
  (r"Áp suất khi khối đứng", [P(r"Cùng áp lực $F=12{,}6\ \text{N}$; mặt chạm bàn nhỏ nhất $3{,}0\times4{,}0=12\ \text{cm}^2=1{,}2\cdot10^{-3}\ \text{m}^2$:"),
                             M(r"p_2=\dfrac{F}{S_2}=\dfrac{12{,}6}{1{,}2\cdot10^{-3}}"), A(r"p_2=10\,500\ \text{Pa}")]),
  (r"Kiểm tra", [P(r"Khối lượng riêng cỡ kim loại thông thường (nhôm $2700$, sắt $7800\ \text{kg/m}^3$) ✓."),
                 P(r"Diện tích chạm bàn đổi từ $60$ xuống $12\ \text{cm}^2$ (nhỏ đi $5$ lần), $F$ không đổi: $2100\cdot5=10\,500\ \text{Pa}$ ✓.")])],
  [r"a) $\rho=7000\ \text{kg/m}^3$", r"b) $p_1=2100\ \text{Pa}$", r"c) $p_2=10\,500\ \text{Pa}$"],
  r"Nhận dạng: đề cho <strong>kích thước, khối lượng</strong> và hỏi <strong>áp suất lên mặt bàn</strong> → $\rho=m/V$ và $p=F/S$ với $F=mg$; đổi cm về m trước khi thế số."),
 sol(R2, [
  (r"Áp suất do dầu ở đáy", [P(r"Đổi $\rho=0{,}80\ \text{g/cm}^3=800\ \text{kg/m}^3$; đáy ở độ sâu $h_1=2{,}5\ \text{m}$:"), M(r"p_1=\rho gh_1=800\cdot10\cdot2{,}5"), A(r"p_1=20\,000\ \text{Pa}")]),
  (r"Áp suất do dầu tại $M$", [P(r"$M$ cách mặt thoáng $h_M=1{,}0\ \text{m}$:"), M(r"p_M=\rho gh_M=800\cdot10\cdot1{,}0"), A(r"p_M=8000\ \text{Pa}")]),
  (r"Áp lực lên nắp van", [P(r"Diện tích nắp $S=20\ \text{cm}^2=2{,}0\cdot10^{-3}\ \text{m}^2$; nắp nằm ở đáy nên dùng áp suất ở đáy:"), M(r"F=p_1S=20\,000\cdot2{,}0\cdot10^{-3}"), A(r"F=40\ \text{N}")]),
  (r"Kiểm tra", [M(r"\Delta p=\rho g\Delta h=800\cdot10\cdot(2{,}5-1{,}0)=12\,000\ \text{Pa}"), P(r"Khớp với $20\,000-8000=12\,000\ \text{Pa}$ ✓."), P(r"Đáy sâu hơn $M$ nên áp suất ở đáy lớn hơn ✓.")])],
  [r"a) $p_1=20\,000\ \text{Pa}$", r"b) $p_M=8000\ \text{Pa}$", r"c) $F=40\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>mực chất lỏng</strong> và hỏi <strong>áp suất ở độ sâu h</strong> → $p=\rho gh$ với $h$ đo từ mặt thoáng; đổi $\rho$ về kg/m³."),
 sol(R3, [
  (r"Áp suất ở đáy thùng", [P(r"Đáy sâu $h=1{,}8\ \text{m}$ so với mặt thoáng. Phần do nước:"), M(r"\rho gh=1000\cdot10\cdot1{,}8=18\,000\ \text{Pa}"),
                           P(r"Áp suất tuyệt đối thêm áp suất khí quyển:"), M(r"p_{\text{đáy}}=p_a+\rho gh=1{,}0\cdot10^5+18\,000"), A(r"p_{\text{đáy}}=118\,000\ \text{Pa}")]),
  (r"Điểm $A$: áp suất dư", [P(r"Độ sâu của $A$ so với mặt thoáng:"), M(r"h_A=1{,}8-0{,}50=1{,}3\ \text{m}"),
                            P(r"Áp kế đo áp suất dư, tức phần do nước:"), M(r"p_{\text{dư}}=\rho gh_A=1000\cdot10\cdot1{,}3"), A(r"p_{\text{dư}}=13\,000\ \text{Pa}")]),
  (r"Điểm $A$: áp suất tuyệt đối", [M(r"p_A=p_a+\rho gh_A=1{,}0\cdot10^5+13\,000"), A(r"p_A=113\,000\ \text{Pa}")]),
  (r"Điểm $B$: độ sâu", [P(r"Bỏ phần khí quyển trước:"), M(r"\rho gh_B=p_B-p_a=1{,}12\cdot10^5-1{,}0\cdot10^5=12\,000\ \text{Pa}"),
                         M(r"h_B=\dfrac{12\,000}{\rho g}=\dfrac{12\,000}{1000\cdot10}"), A(r"h_B=1{,}2\ \text{m}"), P(r"$B$ nằm trong thùng vì $1{,}2\ \text{m}\lt1{,}8\ \text{m}$.")]),
  (r"Kiểm tra", [M(r"p_{\text{đáy}}-p_A=\rho g\cdot0{,}50=5000\ \text{Pa}"), P(r"Khớp với $118\,000-113\,000=5000\ \text{Pa}$ ✓."), P(r"Áp suất dư luôn nhỏ hơn áp suất tuyệt đối đúng $p_a$ ✓.")])],
  [r"a) do nước: $18\,000\ \text{Pa}$ · tuyệt đối: $118\,000\ \text{Pa}$", r"b) tuyệt đối tại $A$: $113\,000\ \text{Pa}$ · áp kế chỉ $13\,000\ \text{Pa}$", r"c) $h_B=1{,}2\ \text{m}$"],
  r"Nhận dạng: đề hỏi <strong>áp suất tuyệt đối</strong> hay <strong>áp suất dư (áp kế)</strong> → xét có cộng $p_a$ hay không; $h$ luôn đo từ mặt thoáng."),
 sol(R4, [
  (r"Áp suất tại mặt phân cách", [P(r"Chọn $A$ ở mặt phân cách (nhánh trái), $B$ ở nhánh phải cùng mức ngang với $A$. Phần áp suất do cột nước phía trên $A$:"),
                                  M(r"\rho_1gh_1=1000\cdot10\cdot0{,}204"), A(r"\rho_1gh_1=2040\ \text{Pa}")]),
  (r"Cột thuỷ ngân phía trên $B$", [P(r"$A$, $B$ cùng nằm trong thuỷ ngân, cùng mức ngang nên $p_A=p_B$; hai nhánh hở nên $p_a$ triệt tiêu:"),
                                   M(r"\rho_2gh_2=\rho_1gh_1"), M(r"h_2=\dfrac{2040}{13\,600\cdot10}=0{,}015\ \text{m}"), A(r"h_2=1{,}5\ \text{cm}")]),
  (r"Chênh mực hai mặt thoáng", [P(r"Cả hai mặt thoáng đều ở phía trên mặt phân cách; hai độ cao đo từ mặt phân cách:"), M(r"\Delta h=h_1-h_2=20{,}4-1{,}5"), A(r"\Delta h=18{,}9\ \text{cm}")]),
  (r"Đổi chiều: tìm cột nước", [P(r"Biết $h_2'=3{,}0\ \text{cm}$, tìm $h_1'$ từ $\rho_1h_1'=\rho_2h_2'$:"), M(r"h_1'=\dfrac{\rho_2h_2'}{\rho_1}=\dfrac{13\,600\cdot3{,}0}{1000}"), A(r"h_1'=40{,}8\ \text{cm}")]),
  (r"Kiểm tra", [M(r"\rho_1h_1'=1000\cdot40{,}8=40\,800=13\,600\cdot3{,}0=\rho_2h_2'"), P(r"Thuỷ ngân nặng gấp $13{,}6$ lần nước nên cột nước cao gấp $13{,}6$ lần cột thuỷ ngân: $20{,}4/1{,}5=13{,}6$ ✓.")])],
  [r"a) $h_2=1{,}5\ \text{cm}$", r"b) $\Delta h=18{,}9\ \text{cm}$", r"c) cột nước cao $40{,}8\ \text{cm}$"],
  r"Nhận dạng: <strong>ống chữ U</strong> với <strong>hai chất lỏng không hoà tan</strong> → chọn hai điểm cùng mức ngang trong cùng một chất lỏng, rồi cho hai áp suất bằng nhau."),
 sol(R5, [
  (r"Khối lượng riêng của gỗ", [P(r"Thể tích khối:"), M(r"V=S\cdot H=0{,}20\cdot0{,}20\cdot0{,}10=4{,}0\cdot10^{-3}\ \text{m}^3"), M(r"\rho=\dfrac{m}{V}=\dfrac{2{,}4}{4{,}0\cdot10^{-3}}"), A(r"\rho=600\ \text{kg/m}^3"),
                                P(r"$600\lt1000$ nên gỗ <strong>nổi</strong> trong nước.")]),
  (r"Lực đẩy khi khối nổi", [P(r"Khối đứng yên nên lực đẩy cân bằng với trọng lượng:"), M(r"F_A=P=mg=2{,}4\cdot10"), A(r"F_A=24\ \text{N}")]),
  (r"Chiều cao phần chìm", [P(r"Từ $F_A=\rho_\ell gV_{\text{chìm}}$, thể tích phần chìm:"), M(r"V_{\text{chìm}}=\dfrac{F_A}{\rho_\ell g}=\dfrac{24}{1000\cdot10}=2{,}4\cdot10^{-3}\ \text{m}^3"),
                           P(r"Chia cho diện tích đáy $S=0{,}040\ \text{m}^2$:"), M(r"h'=\dfrac{V_{\text{chìm}}}{S}=\dfrac{2{,}4\cdot10^{-3}}{0{,}040}=0{,}060\ \text{m}"), A(r"h'=6{,}0\ \text{cm}"), P(r"Nhỏ hơn $10\ \text{cm}$: khối nổi, khớp với ý a.")]),
  (r"Vừa chìm hẳn", [P(r"Khi vừa chìm hẳn, phần chìm là cả khối, $V=4{,}0\cdot10^{-3}\ \text{m}^3$. Lực đẩy lúc này:"), M(r"F_{A}=\rho_\ell gV=1000\cdot10\cdot4{,}0\cdot10^{-3}=40\ \text{N}"),
                     P(r"Lực đẩy cân bằng với trọng lượng của khối và vật:"), M(r"(m+m')g=F_A\ \Rightarrow\ m+m'=4{,}0\ \text{kg}"), M(r"m'=4{,}0-2{,}4"), A(r"m'=1{,}6\ \text{kg}")]),
  (r"Kiểm tra", [M(r"(2{,}4+1{,}6)\cdot10=40\ \text{N}=F_A\ ✓"),
                 P(r"Mỗi centimet chìm thêm của khối cần thêm $\rho_\ell gS\cdot0{,}01=4\ \text{N}$ lực đẩy; phần $4{,}0\ \text{cm}$ còn lại ứng với $16\ \text{N}$, đúng bằng trọng lượng vật $1{,}6\cdot10$ ✓.")])],
  [r"a) $\rho=600\ \text{kg/m}^3$ · khối nổi", r"b) $F_A=24\ \text{N}$", r"c) $h'=6{,}0\ \text{cm}$", r"d) $m'=1{,}6\ \text{kg}$"],
  r"Nhận dạng: <strong>vật thả vào chất lỏng</strong>, <strong>nổi</strong> hoặc <strong>vừa chìm hẳn</strong> → $F_A=\rho_\ell gV$ với $V$ là phần chìm, rồi cân bằng với trọng lượng."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>kích thước và khối lượng</b> rồi hỏi <b>áp suất lên mặt bàn</b> → nghĩ tới <b>ρ = m/V</b>, <b>p = F/S</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Khối lượng riêng", r"Khối lượng riêng của kim loại bằng bao nhiêu kg/m³?", 7000, "kg/m³", 50,
       loi=r"Thế thể tích còn ở cm³ hoặc đổi sai bậc, nên khối lượng riêng lệch luỹ thừa của 10."),
  buoc(r"Áp suất khi khối nằm", r"Áp suất khối ép lên bàn khi nằm bằng mặt lớn nhất là bao nhiêu Pa?", 2100, "Pa", 10,
       loi=r"Lấy khối lượng (kg) làm áp lực, hoặc chia cho diện tích còn ở cm².",
       ke=[(r"Lấy trọng lượng chia cho diện tích mặt chạm bàn, đã đổi ra m²", True),
           (r"Lấy khối lượng 1,26 kg làm áp lực rồi chia cho diện tích đã đổi ra m²", r"Áp lực là lực (N), không phải khối lượng (kg); phải nhân với $g$ trước."),
           (r"Lấy trọng lượng chia cho diện tích của mặt nhỏ nhất", r"Mặt chạm bàn ở tư thế này là mặt lớn nhất, không phải mặt nhỏ nhất.")]),
  buoc(r"Áp suất khi khối đứng", r"Áp suất khối ép lên bàn khi dựng đứng bằng bao nhiêu Pa?", 10500, "Pa", 50,
       loi=r"Giữ nguyên diện tích của ý trước, hoặc nhầm mặt chạm bàn với mặt không chạm bàn.",
       ke=[(r"Giữ áp lực, đổi sang diện tích mặt chạm bàn mới", True),
           (r"Giữ diện tích của mặt lớn nhất vì vẫn là cùng một khối", r"Áp suất phụ thuộc diện tích mặt đang chạm bàn; mặt chạm bàn đã đổi nên $S$ đổi."),
           (r"Lấy áp suất ở ý trước nhân với (diện tích mới / diện tích cũ)", r"Áp suất tỉ lệ nghịch với diện tích, nên phải nhân với (diện tích cũ / diện tích mới); nhân ngược lại cho kết quả sai.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>mực chất lỏng</b> và hỏi <b>áp suất ở độ sâu h</b> → nghĩ tới <b>p = ρgh</b>, h đo từ mặt thoáng.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Áp suất do dầu ở đáy", r"Áp suất do dầu gây ra ở đáy bể bằng bao nhiêu Pa?", 20000, "Pa", 100,
       loi=r"Thế ρ = 0,80 vào công thức khi chưa đổi sang kg/m³."),
  buoc(r"Áp suất do dầu tại $M$", r"Áp suất do dầu gây ra tại $M$ bằng bao nhiêu Pa?", 8000, "Pa", 50,
       loi=r"Dùng khoảng cách từ $M$ đến đáy bể thay cho khoảng cách từ $M$ đến mặt thoáng.",
       ke=[(r"Lấy độ sâu của $M$ từ mặt thoáng, nhân với $\rho g$", True),
           (r"Lấy khoảng cách từ $M$ xuống đáy bể làm $h$", r"$h$ trong $\rho gh$ là độ sâu tính từ mặt thoáng xuống điểm, không tính từ đáy lên."),
           (r"Lấy một nửa áp suất ở đáy vì $M$ ở khoảng giữa bể", r"Áp suất tỉ lệ với độ sâu thật của điểm; $M$ không nằm đúng giữa bể.")]),
  buoc(r"Áp lực lên nắp van", r"Áp lực của dầu lên nắp van bằng bao nhiêu N?", 40, "N", 0.5,
       loi=r"Nhân áp suất với diện tích còn ở cm², hoặc dùng áp suất của điểm khác.",
       ke=[(r"Nhân áp suất ở đáy với diện tích nắp (đổi ra m²)", True),
           (r"Nhân áp suất ở đáy với 20, giữ nguyên đơn vị cm²", r"Áp suất tính bằng Pa = N/m², nên diện tích phải đổi ra m² trước khi nhân."),
           (r"Nhân áp suất tại $M$ với diện tích của nắp van", r"Nắp nằm ở đáy bể, nên áp suất tác dụng lên nắp là áp suất ở đáy, không phải ở $M$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>áp suất tuyệt đối</b> hoặc <b>áp suất dư</b> (áp kế) trong đề → nghĩ tới <b>có cộng pₐ hay không</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Áp suất ở đáy thùng", r"Áp suất tuyệt đối tại đáy thùng bằng bao nhiêu Pa?", 118000, "Pa", 500,
       loi=r"Chỉ tính phần do nước, bỏ quên phần khí quyển trên mặt thoáng."),
  buoc(r"Điểm $A$: áp suất dư", r"Áp kế gắn tại $A$ chỉ áp suất dư bằng bao nhiêu Pa?", 13000, "Pa", 100,
       loi=r"Lấy độ cao của $A$ so với đáy làm $h$, hoặc cộng thêm áp suất khí quyển vào số chỉ của áp kế.",
       ke=[(r"Lấy độ sâu của $A$ từ mặt thoáng, nhân với $\rho g$", True),
           (r"Lấy độ cao 0,50 m của $A$ so với đáy để làm $h$", r"$h$ đo từ mặt thoáng xuống điểm, không đo từ đáy lên."),
           (r"Cộng thêm $p_a$ vì áp kế đo áp suất tại điểm $A$", r"Áp kế đo áp suất dư, phần vượt trên khí quyển; cộng $p_a$ cho áp suất tuyệt đối.")]),
  buoc(r"Điểm $A$: áp suất tuyệt đối", r"Áp suất tuyệt đối tại $A$ bằng bao nhiêu Pa?", 113000, "Pa", 500,
       loi=r"Trừ thay vì cộng áp suất khí quyển, hoặc lấy luôn áp suất ở đáy.",
       ke=[(r"Cộng áp suất khí quyển với phần do nước tại $A$", True),
           (r"Lấy $p_a$ trừ phần do nước tại $A$", r"Nước phía trên $A$ ép thêm xuống nên áp suất lớn hơn $p_a$, không nhỏ hơn."),
           (r"Giữ áp suất tuyệt đối ở đáy vì cùng một thùng nước", r"Chỉ các điểm cùng độ sâu mới cùng áp suất; $A$ nông hơn đáy.")]),
  buoc(r"Điểm $B$: độ sâu", r"Điểm $B$ cách mặt thoáng bao nhiêu mét?", 1.2, "m", 0.02,
       loi=r"Chia cả áp suất tuyệt đối cho $\rho g$, hoặc bỏ quên $g$ khi chia.",
       ke=[(r"Trừ $p_a$, rồi chia phần còn lại cho $\rho g$", True),
           (r"Chia thẳng áp suất tuyệt đối của $B$ cho $\rho g$", r"Phần $p_a$ do khí quyển, không do nước; chia cả $p_a$ cho $\rho g$ cho độ sâu vô lí, lớn hơn chiều cao thùng."),
           (r"Trừ $p_a$ rồi chia phần còn lại cho $\rho$, bỏ $g$", r"Phần do nước là $\rho gh$ đủ ba thừa số; thiếu $g$ thì sai đơn vị.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>ống chữ U</b> với <b>hai chất lỏng không hoà tan</b> → nghĩ tới <b>hai điểm cùng mức ngang</b> trong cùng chất lỏng.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Áp suất tại mặt phân cách", r"Áp suất do cột nước gây ra tại mặt phân cách (điểm $A$) bằng bao nhiêu Pa?", 2040, "Pa", 10,
       loi=r"Để chiều cao cột nước còn ở cm khi thế vào $\rho gh$."),
  buoc(r"Cột thuỷ ngân phía trên $B$", r"Mặt thuỷ ngân ở nhánh phải cao hơn mặt phân cách bao nhiêu cm?", 1.5, "cm", 0.05,
       loi=r"Cho hai mặt thoáng ngang nhau như khi chỉ có một chất lỏng, hoặc đảo tỉ số hai khối lượng riêng.",
       ke=[(r"Cho áp suất cột thuỷ ngân trên $B$ bằng áp suất tại $A$", True),
           (r"Cho độ cao thuỷ ngân bằng độ cao cột nước vì cùng một ống chữ U", r"Mực ngang nhau chỉ khi cùng một chất lỏng; ở đây hai chất lỏng có khối lượng riêng khác nhau."),
           (r"Nhân độ cao cột nước với tỉ số $\rho_2/\rho_1$", r"Tỉ số bị đảo: thuỷ ngân nặng hơn nước nên cột thuỷ ngân thấp hơn cột nước chứ không cao hơn.")]),
  buoc(r"Chênh mực hai mặt thoáng", r"Mặt nước ở nhánh trái cao hơn mặt thuỷ ngân ở nhánh phải bao nhiêu cm?", 18.9, "cm", 0.1,
       loi=r"Cộng hai độ cao với nhau, hoặc coi mặt thuỷ ngân bên phải ngang với mặt phân cách.",
       ke=[(r"Lấy hiệu hai độ cao, cùng đo từ mặt phân cách", True),
           (r"Cộng hai độ cao", r"Cả hai mặt thoáng nằm phía trên mặt phân cách, cùng phía; chênh lệch là hiệu chứ không phải tổng."),
           (r"Lấy luôn độ cao cột nước, coi thuỷ ngân bên phải ngang mặt phân cách", r"Mặt thuỷ ngân bên phải cao hơn mặt phân cách, chính là $h_2$ ở ý a.")]),
  buoc(r"Đổi chiều: tìm cột nước", r"Cột nước ở nhánh trái phải cao bao nhiêu cm?", 40.8, "cm", 0.2,
       loi=r"Đảo tỉ số hai khối lượng riêng, hoặc cộng thêm vào cột nước cũ.",
       ke=[(r"Dùng lại cân bằng áp suất với $h_2'$ đã biết", True),
           (r"Nhân 3,0 cm với tỉ số khối lượng riêng $\rho_1/\rho_2$", r"Nước nhẹ hơn thuỷ ngân nên cột nước phải cao hơn cột thuỷ ngân; tỉ số bị đảo."),
           (r"Cộng thêm 3,0 cm vào cột nước 20,4 cm cũ", r"Cột nước tỉ lệ với $h_2$ theo tỉ số khối lượng riêng, không tăng thêm đúng bằng độ tăng của $h_2$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật thả vào chất lỏng</b>, <b>nổi</b> hoặc <b>vừa chìm hẳn</b> → nghĩ tới <b>F_A = ρgV</b> với V là phần chìm.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Khối lượng riêng của gỗ", r"Khối lượng riêng của gỗ bằng bao nhiêu kg/m³?", 600, "kg/m³", 5,
       loi=r"Thế thể tích còn ở cm³, hoặc nhầm thể tích khối với diện tích đáy."),
  buoc(r"Lực đẩy khi khối nổi", r"Lực đẩy Archimedes lên khối khi nổi yên bằng bao nhiêu N?", 24, "N", 0.3,
       loi=r"Dùng thể tích cả khối trong công thức lực đẩy, hoặc quên nhân $g$ khi đổi khối lượng sang lực.",
       ke=[(r"Cho lực đẩy cân bằng với trọng lượng của khối", True),
           (r"Tính $\rho_\ell gV$ với $V$ là thể tích cả khối", r"$V$ trong công thức lực đẩy là thể tích phần chìm; khối nổi nên chưa chìm hết."),
           (r"Lấy lực đẩy bằng khối lượng 2,4 kg, không nhân $g$", r"Lực đẩy là lực (N), khối lượng là kg; phải nhân với $g$ mới ra trọng lượng.")]),
  buoc(r"Chiều cao phần chìm", r"Chiều cao phần khối chìm trong nước bằng bao nhiêu cm?", 6.0, "cm", 0.1,
       loi=r"Chia thể tích phần chìm cho một cạnh đáy thay vì diện tích đáy, hoặc đảo tỉ số khối lượng riêng.",
       ke=[(r"Tìm thể tích phần chìm từ lực đẩy, rồi chia cho diện tích đáy", True),
           (r"Nhân chiều cao 10 cm với tỉ số $\rho_{\text{nước}}/\rho_{\text{gỗ}}$", r"Kết quả vượt chiều cao khối; khối đang nổi nên phần chìm phải thấp hơn 10 cm."),
           (r"Chia thể tích phần chìm cho một cạnh đáy 20 cm", r"Chiều cao bằng thể tích chia cho diện tích đáy (tích hai cạnh), không chia cho một cạnh.")]),
  buoc(r"Vừa chìm hẳn", r"Vật đặt thêm phải có khối lượng tối thiểu bao nhiêu kg?", 1.6, "kg", 0.05,
       loi=r"Dùng lực đẩy của lúc nổi, hoặc coi khối lượng vật bằng khối lượng nước bị chiếm chỗ.",
       ke=[(r"Cho lực đẩy lớn nhất cân bằng với trọng lượng của khối và vật", True),
           (r"Cho vật nặng bằng khối lượng nước bị khối chiếm chỗ khi chìm hẳn", r"Lượng nước bị chiếm chỗ cân bằng với cả khối lẫn vật cộng lại, không riêng vật."),
           (r"Dùng lực đẩy ứng với phần chìm 6,0 cm ở ý trước", r"Khi chìm hẳn, $V$ là cả khối nên lực đẩy lớn hơn lúc nổi; dùng phần chìm cũ thì không cần thêm vật.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập (idx 0-based trong old/79.json), xếp dễ → khó ═════════════
# VD1 (idx0): quả cầu 20 cm³ lơ lửng, F_A (g = 9,8) · VD2 (idx1): lực kế + bình tràn, m và trọng lượng riêng
def _cat(i):
    h = OLD[i]["body_html"]
    k = h.index('<p class="text-base leading-relaxed my-2"><strong class="font-bold">Ví dụ:')
    h = h[k:]
    j = h.index('<p class="text-base leading-relaxed my-2"><strong class="font-bold">Lời giải:')
    h = re.sub(r'alt="[^"]*"', 'alt=""', h)
    return h[:j], h[j:].replace("Lời giải:", "Lời giải gốc:", 1)
parts = []
for k, (i, muc) in enumerate(((0, "Dễ"), (1, "Trung bình")), 1):
    de, gi = _cat(i)
    de = de.replace("Ví dụ:", "Đề:", 1)
    if i == 0:
        de = r'<p class="text-base leading-relaxed my-2"><strong class="font-bold">Đề:</strong> Một quả cầu có thể tích $20\ \text{cm}^3$ lơ lửng trong nước, khối lượng riêng của nước là $1\ \text{g/cm}^3$, lấy $g = 9{,}8\ \text{m/s}^2$. Lực đẩy Archimedes tác dụng lên quả cầu là bao nhiêu?</p>'
        gi = r'<p class="text-base leading-relaxed my-2"><strong class="font-bold">Lời giải gốc:</strong> Trọng lượng riêng của nước $d = \rho g = 1000\cdot9{,}8 = 9800\ \text{N/m}^3$. $F_A = d\cdot V = 9800\cdot20\cdot10^{-6} = 0{,}196\ \text{N}$.</p>'
    else:
        de = de.replace("N/$m^3$", r"N/$\text{m}^3$")
        gi = ('<p class="text-base leading-relaxed my-2"><strong class="font-bold">Lời giải gốc:</strong></p>'
              r'<p class="text-base leading-relaxed my-2">a) Thể tích nước tràn ra đúng bằng thể tích vật chiếm chỗ: $V = 0{,}5\ \text{lít} = 0{,}0005\ \text{m}^3$. Lực đẩy Archimedes: $F_A = d_n\cdot V = 10000\cdot0{,}0005 = 5\ \text{N}$. Trọng lượng vật: $P = F + F_A = 8{,}5 + 5 = 13{,}5\ \text{N}$; với $g = 10\ \text{m/s}^2$ thì $m = 1{,}35\ \text{kg}$.</p>'
              r'<p class="text-base leading-relaxed my-2">b) Trọng lượng riêng của vật: $d = \dfrac{P}{V} = \dfrac{13{,}5}{0{,}0005} = 2{,}7\cdot10^4\ \text{N/m}^3$, nên vật làm bằng nhôm.</p>')
    parts.append(f'<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>')
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))

write(J, 79, "Bài 34. Khối lượng riêng. Áp suất chất lỏng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
for q in d["dang_bai"]:
    w = len(re.sub(r"<[^>]+>", "", q["nhan_dang"]).split())
    assert w <= 25, (q["label"], w)
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
