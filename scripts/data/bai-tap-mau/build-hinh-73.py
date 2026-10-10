"""Bài 73 — "Bài 28. Động lượng" (Vật lí 10, chương 5). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-58.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-73.py  → ghi scripts/data/bai-tap-mau/73.json
Dạng xếp theo hệ bắc cầu (quét: scripts/logs/batch-ra-soat/ket-qua/73.quet-dang.json). Hình: hinh_73.py (vec_luc, độ dài = k·độ lớn).
Ví dụ cũ (old/73.json: 2 mục, 17 câu): Dạng cũ 1 Câu 1 + Câu 2 (xe, đổi đơn vị, dấu) → Dạng 1; Dạng cũ 2 Câu 1 (đạn trong nòng, đảo ý hỏi) → Dạng 2;
  Dạng cũ 2 Câu 3 (quả cầu bật vách; bản gốc dấu Δp/F lẫn lộn) → Dạng 4; Dạng 5 viết mới theo ý Câu 4 (tàu hãm) + Câu 6 (người nhảy): đệm kéo dài Δt.
  Vào tự luận: D1 Câu 3, D2 Câu 7 (đã sửa "l,5" thành 1,5), Câu 4 (đã sửa đơn vị Δp, bỏ khối aligned), Câu 11 (bỏ 2 ảnh minh hoạ), Câu 2.
  BỎ: D1 Câu 4 (động lượng máy bay làm tròn 38666666, đúng 38666667), D2 Câu 5 (trùng ý Câu 11; dấu F lẫn), Câu 6 (người nhảy cầu: bỏ quên trọng lực,
  đúng là N − mg = 1138 nên lực cản ≈ 1738 N, đáp số cũ 1138 N sai), Câu 8, 10, 12, 13 (đề phụ thuộc hình vẽ không kiểm được; Câu 12 đề ghi 72 kg
  nhưng lời giải dùng 82 kg; Câu 13 đề 5 m/s nhưng lời giải ghi 8 m/s), Câu 9 (trùng Câu 2, kèm ảnh)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_73 import BUILD

J = os.path.join(HERE, "73.json")
OLD = json.load(open(os.path.join(HERE, "old/73.json")))["questions"]
T142 = "Khái niệm động lượng, xung lượng của lực"
T143 = "Độ biến thiên động lượng của một vật"


# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
cosd = lambda a: math.cos(math.radians(a))
# D1
m1, v1 = 1500.0, 54 / 3.6; m2, v2 = 750.0, -72 / 3.6
ok("D1 v1", v1, 15, 1e-9); ok("D1 v2", v2, -20, 1e-9); ok("D1 p1", m1 * v1, 22500, 1e-6); ok("D1 p2", m2 * v2, -15000, 1e-6)
assert abs(m1 * v1) > abs(m2 * v2) and abs(m2 * 72) > abs(m1 * 54) * 0 and 72 > 54          # ô tô nhanh hơn nhưng nhẹ hơn
assert abs(m2 * 72 - m2 * v2) > 1000                                                         # km/h chưa đổi cho kết quả khác
# D2
m, F, dt = 0.010, 9000.0, 1.0e-3
J_ = F * dt; ok("D2 J", J_, 9.0, 1e-9); ok("D2 v", J_ / m, 900, 1e-6); ok("D2 v'", F * 0.5e-3 / m, 450, 1e-6)
assert abs(F / m - J_ / m) > 1e5 and abs(J_ * m - J_ / m) > 800 and abs(J_ / 10 - J_ / m) > 800   # F/m; nhân m; m=10 g chưa đổi
a = F / m; L = 0.5 * a * dt**2; ok("D2 L", L, 0.45, 1e-9)                                     # nòng 0,45 m → 270 px ở 600 px/m (hinh_73)
# D3
M1, V1, M2, V2 = 50.0, 6.0, 80.0, 5.0; p1, p2 = M1 * V1, M2 * V2
ok("D3 p1", p1, 300, 1e-9); ok("D3 p2", p2, 400, 1e-9)
pa = abs(p1 - p2); pb = math.hypot(p1, p2); pc = math.sqrt(p1**2 + p2**2 + 2 * p1 * p2 * cosd(60))
ok("D3 a", pa, 100, 1e-9); ok("D3 b", pb, 500, 1e-9); ok("D3 c²", pc**2, 370000, 1e-6); ok("D3 c", pc, 608.3, 0.05)
assert len({round(x, 1) for x in (p1 + p2, pa, pb, pc, math.sqrt(p1**2 + p2**2 - 2 * p1 * p2 * cosd(60)))}) == 5
assert abs(pc - pb) > 50 and abs(pc - (p1 + p2)) > 50
assert pa <= pc <= p1 + p2 and pa <= pb <= p1 + p2
# D4
m = 0.10
ok("D4 a", m * (-4.0 - 4.0), -0.80, 1e-9); ok("D4 b", m * (-3.0 - 4.0), -0.70, 1e-9); ok("D4 c", m * (4.0 - (-4.0)), 0.80, 1e-9)
assert abs(m * (4.0 - 4.0)) < 1e-9 and abs(m * (3.0 - 4.0) - (-0.70)) > 0.5               # hiệu hai tốc độ cho 0 hoặc −0,10
# D5
m, v = 0.40, 20.0; dp = m * (0 - v); ok("D5 dp", dp, -8.0, 1e-9)
Fa, Fb = dp / 0.010, dp / 0.050; ok("D5 Fa", Fa, -800, 1e-9); ok("D5 Fb", Fb, -160, 1e-9); ok("D5 tỉ số", Fb / Fa, 0.20, 1e-12)
ok("D5 trọng lượng/Fa", m * 10 / 800, 0.005, 1e-9)
assert abs(dp * 0.010 - Fa) > 5 and abs(m * 10 - Fa) > 100 and abs(Fa / Fb - Fb / Fa) > 1    # nhân thay chia; chỉ trọng lượng; đảo tỉ số
assert abs(v * 0.010 / 2 * 100 - 10) < 1e-9 and abs(v * 0.050 / 2 * 100 - 50) < 1e-9      # quãng dừng 10 px và 50 px ở 100 px/m (hinh_73)


# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Tính động lượng của một vật, đổi đơn vị và xét dấu theo chiều dương", topic=T142,
      problem_html=r"""<p>Trên một đoạn đường thẳng, xe tải khối lượng $1{,}5$ tấn chạy với tốc độ $54\ \text{km/h}$; ô tô con khối lượng $750\ \text{kg}$ chạy ngược chiều với tốc độ $72\ \text{km/h}$. Chọn chiều dương là chiều chuyển động của xe tải, mốc là mặt đường.</p>
<ol type="a"><li>Tính động lượng của xe tải.</li>
<li>Tính động lượng của ô tô con (kể cả dấu).</li>
<li>Xe nào có động lượng với độ lớn lớn hơn?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Xung lượng của lực và tốc độ vật thu được", topic=T142,
      problem_html=r"""<p>Trong nòng một khẩu súng trường nằm ngang, khí thuốc súng đẩy viên đạn khối lượng $10\ \text{g}$ bằng một lực trung bình $9000\ \text{N}$ trong thời gian $1{,}0\ \text{ms}$. Viên đạn đứng yên trước khi bắn; bỏ qua ma sát và lực cản của không khí.</p>
<ol type="a"><li>Tính xung lượng của lực đẩy.</li>
<li>Tính tốc độ của viên đạn khi ra khỏi nòng.</li>
<li>Nòng ngắn đi sao cho thời gian đẩy chỉ còn $0{,}50\ \text{ms}$ với cùng lực đẩy. Tính tốc độ của viên đạn khi ra khỏi nòng.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Động lượng của hệ hai vật theo góc giữa hai chuyển động", topic=T142,
      problem_html=r"""<p>Hai xe đẩy trong kho trượt trên sàn nhẵn: xe 1 khối lượng $50\ \text{kg}$ chạy với tốc độ $6{,}0\ \text{m/s}$, xe 2 khối lượng $80\ \text{kg}$ chạy với tốc độ $5{,}0\ \text{m/s}$. Tính độ lớn động lượng của hệ hai xe (đối với sàn) khi:</p>
<ol type="a"><li>hai xe chạy ngược chiều nhau trên cùng một đường thẳng;</li>
<li>hai xe chạy trên hai đường vuông góc nhau;</li>
<li>hai vận tốc hợp nhau góc $60^\circ$.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Độ biến thiên động lượng khi vật bật ngược lại", topic=T143,
      problem_html=r"""<p>Quả bóng cao su khối lượng $0{,}10\ \text{kg}$ lăn trên sàn nhẵn, đập vuông góc vào một vách cứng với tốc độ $4{,}0\ \text{m/s}$.</p>
<ol type="a"><li>Bóng bật ngược lại với cùng tốc độ $4{,}0\ \text{m/s}$. Chọn chiều dương là chiều bóng tới vách. Tính độ biến thiên động lượng của bóng.</li>
<li>Lần khác, bóng tới vách cũng với $4{,}0\ \text{m/s}$ nhưng bật lại với tốc độ $3{,}0\ \text{m/s}$. Tính độ biến thiên động lượng (chiều dương như ý a).</li>
<li>Ở ý a, nếu chọn chiều dương là chiều bóng bật ra khỏi vách thì độ biến thiên động lượng bằng bao nhiêu?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Lực trung bình từ độ biến thiên động lượng và thời gian tác dụng", topic=T143,
      problem_html=r"""<p>Thủ môn bắt quả bóng khối lượng $0{,}40\ \text{kg}$ đang bay ngang với tốc độ $20\ \text{m/s}$ và giữ cho bóng dừng hẳn. Coi lực của tay lên bóng nằm ngang và bỏ qua trọng lượng của bóng trong lúc bắt. Chọn chiều dương là chiều bay của bóng.</p>
<ol type="a"><li>Tay giữ cứng, bóng dừng hẳn sau $0{,}010\ \text{s}$. Tính lực trung bình của tay lên bóng.</li>
<li>Tay co lại theo bóng, bóng dừng hẳn sau $0{,}050\ \text{s}$. Tính lực trung bình của tay lên bóng.</li>
<li>Lực ở ý b bằng bao nhiêu lần lực ở ý a? Vì sao co tay lại thì đỡ đau hơn?</li></ol>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“xe tải khối lượng $1{,}5$ tấn … tốc độ $54$ km/h”", r"$m_1=1{,}5\ \text{tấn}$; $v_1=54\ \text{km/h}$", r"⚠ Đổi sang đơn vị chuẩn trước khi tính: kg, m/s"),
  (r"“ô tô con khối lượng $750$ kg chạy ngược chiều … $72$ km/h”", r"$m_2=750\ \text{kg}$; $v_2=72\ \text{km/h}$; ngược chiều xe tải", r"Vận tốc là đại lượng có hướng"),
  (r"“Chọn chiều dương là chiều chuyển động của xe tải, mốc là mặt đường”", r"Chiều dương = chiều xe tải; mốc: mặt đường", r"⚠ Động lượng là vectơ cùng hướng với vận tốc; dấu theo chiều dương đã chọn"),
  (r"“a) động lượng của xe tải”", r"Cần $p_1$", r"Đại lượng cần tìm: động lượng $p=mv$"),
  (r"“b) động lượng của ô tô con (kể cả dấu)”", r"Cần $p_2$ (có dấu)", r"Đại lượng cần tìm"),
  (r"“c) xe nào có động lượng với độ lớn lớn hơn”", r"So hai độ lớn", r"Độ lớn của đại lượng vectơ: bỏ dấu")],
 [(r"“viên đạn khối lượng $10$ g”", r"$m=10\ \text{g}$", r"⚠ Đổi gam sang kilôgam trước khi tính"),
  (r"“lực trung bình $9000$ N trong thời gian $1{,}0$ ms”", r"$F=9000\ \text{N}$; $\Delta t=1{,}0\ \text{ms}$", r"Xung lượng của lực là tích của $F$ với $\Delta t$; ⚠ đổi ms sang s"),
  (r"“nằm ngang … bỏ qua ma sát và lực cản của không khí”", r"Lực đẩy là hợp lực lên viên đạn", r"⚠ Liên hệ xung lượng với độ biến thiên động lượng dùng với hợp lực"),
  (r"“Viên đạn đứng yên trước khi bắn”", r"$v_1=0$, nên $p_1=0$", r"Độ biến thiên động lượng: sau trừ trước"),
  (r"“a) xung lượng của lực đẩy”", r"Cần xung lượng (N·s)", r"Đại lượng cần tìm"),
  (r"“b) tốc độ của viên đạn khi ra khỏi nòng”", r"Cần $v_2$ (m/s)", r"Đại lượng cần tìm"),
  (r"“c) thời gian đẩy chỉ còn $0{,}50$ ms với cùng lực”", r"$\Delta t'=0{,}50\ \text{ms}$; $F$ giữ nguyên", r"Xét đại lượng nào đổi, đại lượng nào giữ nguyên")],
 [(r"“xe 1 khối lượng $50$ kg … tốc độ $6{,}0$ m/s”", r"$m_1=50\ \text{kg}$; $v_1=6{,}0\ \text{m/s}$", r"Động lượng của từng vật: $p=mv$"),
  (r"“xe 2 khối lượng $80$ kg … tốc độ $5{,}0$ m/s”", r"$m_2=80\ \text{kg}$; $v_2=5{,}0\ \text{m/s}$", r"Động lượng của từng vật: $p=mv$"),
  (r"“trượt trên sàn nhẵn … (đối với sàn)”", r"Mọi vận tốc đo so với sàn", r"⚠ Hai động lượng phải cùng một hệ quy chiếu mới cộng được"),
  (r"“a) ngược chiều nhau trên cùng một đường thẳng”", r"Góc giữa hai vectơ: $\alpha=180^\circ$", r"Động lượng của hệ là tổng vectơ"),
  (r"“b) hai đường vuông góc nhau”", r"$\alpha=90^\circ$", r"⚠ Cộng vectơ, không cộng độ lớn; $\alpha$ là góc giữa hai vectơ chung gốc"),
  (r"“c) hai vận tốc hợp nhau góc $60^\circ$”", r"$\alpha=60^\circ$", r"Tổng hai vectơ qua góc $\alpha$ bất kì"),
  (r"“độ lớn động lượng của hệ hai xe”", r"Cần $p$ (kg·m/s) ở ba trường hợp", r"Đại lượng cần tìm")],
 [(r"“Quả bóng cao su khối lượng $0{,}10$ kg lăn trên sàn nhẵn”", r"$m=0{,}10\ \text{kg}$", r"Độ biến thiên động lượng: $\Delta\vec p=\vec p_2-\vec p_1$"),
  (r"“đập vuông góc vào một vách cứng với tốc độ $4{,}0$ m/s”", r"Tốc độ trước va chạm: $4{,}0\ \text{m/s}$", r"Tốc độ là độ lớn; vận tốc có hướng"),
  (r"“a) bật ngược lại với cùng tốc độ … chiều dương là chiều bóng tới vách”", r"Tốc độ sau: $4{,}0\ \text{m/s}$; chiều dương = chiều tới vách", r"⚠ Bật ngược lại: hướng vận tốc đổi — xét dấu theo chiều dương đã chọn"),
  (r"“b) bật lại với tốc độ $3{,}0$ m/s”", r"Tốc độ sau: $3{,}0\ \text{m/s}$; chiều dương như ý a", r"Giữ nguyên chiều dương đã chọn"),
  (r"“Tính độ biến thiên động lượng”", r"Cần $\Delta p$ ở ý a và ý b", r"Đại lượng cần tìm"),
  (r"“c) chọn chiều dương là chiều bóng bật ra khỏi vách”", r"Cùng sự kiện ở ý a, chiều dương ngược lại", r"⚠ Đổi chiều dương thì dấu của các vận tốc đổi theo")],
 [(r"“quả bóng khối lượng $0{,}40$ kg đang bay ngang với tốc độ $20$ m/s”", r"$m=0{,}40\ \text{kg}$; $v_1=20\ \text{m/s}$", r"Động lượng $p=mv$"),
  (r"“giữ cho bóng dừng hẳn”", r"$v_2=0$", r"Độ biến thiên động lượng: sau trừ trước"),
  (r"“lực của tay … nằm ngang, bỏ qua trọng lượng của bóng”", r"Lực của tay là hợp lực lên bóng", r"⚠ $\Delta\vec p=\vec F\Delta t$ dùng với hợp lực; đề cho phép bỏ qua trọng lượng"),
  (r"“Chọn chiều dương là chiều bay của bóng”", r"$v_1\gt0$", r"Dấu của $\Delta p$ và của lực theo chiều dương này"),
  (r"“a) tay giữ cứng, bóng dừng hẳn sau $0{,}010$ s”", r"$\Delta t=0{,}010\ \text{s}$", r"Lực trung bình qua độ biến thiên động lượng"),
  (r"“b) tay co lại theo bóng, dừng hẳn sau $0{,}050$ s”", r"$\Delta t'=0{,}050\ \text{s}$", r"Xét đại lượng nào đổi, đại lượng nào giữ nguyên so với ý a"),
  (r"“c) bằng bao nhiêu lần … vì sao đỡ đau hơn”", r"Cần tỉ số hai lực và lời giải thích", r"Đại lượng cần tìm")],
]

# ═════════════ Lời giải từng bước ═════════════
R1 = [r"<strong>Khái niệm:</strong> động lượng là vectơ $\vec p=m\vec v$, cùng hướng với vận tốc.",
      r"Độ lớn $p=mv$, đơn vị $\text{kg}\cdot\text{m/s}$.",
      r"Chọn chiều dương: vận tốc cùng chiều mang dấu $+$, ngược chiều mang dấu $-$.",
      r"⚠ <strong>Điều kiện:</strong> $m$ tính bằng kg, $v$ bằng m/s (đổi tấn, km/h trước), vận tốc đo so với mặt đường."]
R2 = [r"<strong>Khái niệm:</strong> xung lượng của lực là tích $\vec F\Delta t$, đơn vị $\text{N}\cdot\text{s}$.",
      r"<strong>Định luật:</strong> $\Delta\vec p=\vec F\,\Delta t$, tức $mv_2-mv_1=F\Delta t$ ($\text{N}\cdot\text{s}=\text{kg}\cdot\text{m/s}$).",
      r"Đổi $1\ \text{ms}=10^{-3}\ \text{s}$ và $1\ \text{g}=10^{-3}\ \text{kg}$ trước khi tính.",
      r"⚠ <strong>Điều kiện:</strong> $F$ là hợp lực lên vật, lấy giá trị trung bình trong $\Delta t$."]
R3 = [r"<strong>Khái niệm:</strong> động lượng của hệ là tổng vectơ $\vec p=\vec p_1+\vec p_2$.",
      r"Mỗi vật $p_i=m_iv_i$, hệ quy chiếu gắn với sàn.",
      r"Cùng hướng: $p=p_1+p_2$ · ngược hướng: $p=\lvert p_1-p_2\rvert$ · vuông góc: $p=\sqrt{p_1^2+p_2^2}$.",
      r"Góc $\alpha$ bất kì: $p^2=p_1^2+p_2^2+2p_1p_2\cos\alpha$.",
      r"⚠ <strong>Điều kiện:</strong> cộng vectơ, không cộng độ lớn; $\alpha$ là góc giữa hai vectơ chung gốc."]
R4 = [r"<strong>Khái niệm:</strong> $\Delta\vec p=\vec p_2-\vec p_1$ (sau trừ trước), cũng là vectơ.",
      r"Chọn chiều dương trước; vận tốc cùng chiều mang dấu $+$, ngược chiều mang dấu $-$.",
      r"Chiếu lên chiều dương: $\Delta p=m(v_2-v_1)$.",
      r"⚠ <strong>Điều kiện:</strong> bóng bật ngược lại thì $v_1$ và $v_2$ trái dấu."]
R5 = [r"<strong>Khái niệm:</strong> $\Delta\vec p=\vec p_2-\vec p_1$; xung lượng của lực là $\vec F\Delta t$.",
      r"<strong>Định luật:</strong> $\Delta\vec p=\vec F\,\Delta t$, suy ra $\vec F=\dfrac{\Delta\vec p}{\Delta t}$ (lực trung bình).",
      r"Chọn chiều dương rồi chiếu: $\Delta p=m(v_2-v_1)$.",
      r"⚠ <strong>Điều kiện:</strong> $F$ là hợp lực; ở đây lực của tay nằm ngang, trọng lượng bóng không đáng kể."]

SOLS = [
 sol(R1, [
  (r"Động lượng của xe tải", [P(r"Đổi đơn vị:"), M(r"m_1=1{,}5\ \text{tấn}=1500\ \text{kg}"), M(r"v_1=54\ \text{km/h}=15\ \text{m/s}"),
                               P(r"Xe tải chạy theo chiều dương nên $v_1=+15\ \text{m/s}$:"), M(r"p_1=m_1v_1=1500\cdot15"), A(r"p_1=22500\ \text{kg}\cdot\text{m/s}"),
                               P(r"Dấu $+$: động lượng cùng chiều dương.")]),
  (r"Động lượng của ô tô con", [P(r"Đổi: $72\ \text{km/h}=20\ \text{m/s}$. Ô tô chạy ngược chiều dương nên $v_2=-20\ \text{m/s}$:"),
                                 M(r"p_2=m_2v_2=750\cdot(-20)"), A(r"p_2=-15000\ \text{kg}\cdot\text{m/s}"), P(r"Dấu $-$: động lượng ngược chiều dương.")]),
  (r"So sánh độ lớn", [P(r"So hai độ lớn, bỏ dấu:"), M(r"\lvert p_1\rvert=22500\ \text{kg}\cdot\text{m/s}\ \gt\ \lvert p_2\rvert=15000\ \text{kg}\cdot\text{m/s}"),
                        A(r"T:Xe tải có động lượng với độ lớn lớn hơn."),
                        P(r"Ô tô chạy nhanh hơn nhưng khối lượng chỉ bằng một nửa xe tải, nên khối lượng thắng.")]),
  (r"Kiểm tra", [P(r"Đơn vị $\text{kg}\cdot\text{m/s}$ ✓."), P(r"Hai động lượng trái dấu vì hai xe chạy ngược chiều ✓.")])],
  [r"a) $p_1=22500\ \text{kg}\cdot\text{m/s}$ (cùng chiều dương)", r"b) $p_2=-15000\ \text{kg}\cdot\text{m/s}$", r"c) Xe tải"],
  r"Nhận dạng: đề cho <strong>khối lượng, tốc độ và chiều chuyển động</strong> → $p=mv$ với đơn vị chuẩn; chiều dương quyết định dấu."),
 sol(R2, [
  (r"Xung lượng của lực đẩy", [P(r"Đổi $\Delta t=1{,}0\ \text{ms}=1{,}0\cdot10^{-3}\ \text{s}$:"), M(r"F\Delta t=9000\cdot1{,}0\cdot10^{-3}"), A(r"F\Delta t=9{,}0\ \text{N}\cdot\text{s}")]),
  (r"Tốc độ ra khỏi nòng", [P(r"Đạn đứng yên lúc đầu nên $p_1=0$; đổi $m=10\ \text{g}=0{,}010\ \text{kg}$:"), M(r"F\Delta t=mv_2-0"),
                             M(r"v_2=\dfrac{F\Delta t}{m}=\dfrac{9{,}0}{0{,}010}"), A(r"v_2=900\ \text{m/s}")]),
  (r"Nòng ngắn hơn", [P(r"Lực giữ nguyên, thời gian đẩy $\Delta t'=0{,}50\ \text{ms}=0{,}50\cdot10^{-3}\ \text{s}$:"),
                       M(r"v_2'=\dfrac{F\Delta t'}{m}=\dfrac{9000\cdot0{,}50\cdot10^{-3}}{0{,}010}"), A(r"v_2'=450\ \text{m/s}")]),
  (r"Kiểm tra", [P(r"Đơn vị: $\text{N}\cdot\text{s}/\text{kg}=\text{m/s}$ ✓."), P(r"Cùng lực, thời gian đẩy giảm một nửa thì tốc độ giảm một nửa ✓."),
                  P(r"$900\ \text{m/s}$ cùng cỡ tốc độ đạn súng trường ✓.")])],
  [r"a) Xung lượng $=9{,}0\ \text{N}\cdot\text{s}$", r"b) $v_2=900\ \text{m/s}$", r"c) $v_2'=450\ \text{m/s}$"],
  r"Nhận dạng: đề cho <strong>lực và thời gian tác dụng</strong>, hỏi tốc độ → xung lượng $F\Delta t$ bằng độ biến thiên động lượng."),
 sol(R3, [
  (r"Động lượng của xe 1", [M(r"p_1=m_1v_1=50\cdot6{,}0"), A(r"p_1=300\ \text{kg}\cdot\text{m/s}")]),
  (r"Động lượng của xe 2", [M(r"p_2=m_2v_2=80\cdot5{,}0"), A(r"p_2=400\ \text{kg}\cdot\text{m/s}")]),
  (r"Ngược chiều ($\alpha=180^\circ$)", [P(r"Chọn chiều dương là chiều của $\vec p_2$; $\vec p_1$ ngược chiều nên mang dấu $-$:"), M(r"p=p_2-p_1=400-300"),
                                         A(r"p=100\ \text{kg}\cdot\text{m/s}"), P(r"Hướng cùng chiều xe 2.")]),
  (r"Vuông góc ($\alpha=90^\circ$)", [M(r"p=\sqrt{p_1^2+p_2^2}=\sqrt{300^2+400^2}=\sqrt{250000}"), A(r"p=500\ \text{kg}\cdot\text{m/s}")]),
  (r"Hợp nhau $60^\circ$", [M(r"p^2=p_1^2+p_2^2+2p_1p_2\cos60^\circ"), M(r"p^2=300^2+400^2+2\cdot300\cdot400\cdot0{,}5=370000"),
                             A(r"p=\sqrt{370000}\approx608\ \text{kg}\cdot\text{m/s}")]),
  (r"Kiểm tra", [P(r"Hợp lực luôn nằm trong khoảng từ hiệu đến tổng hai độ lớn: $100\le p\le700$ ✓."),
                  P(r"Góc giữa hai vectơ càng nhỏ, tổng càng lớn: $100\lt500\lt608\lt700$ ✓.")])],
  [r"a) $p=100\ \text{kg}\cdot\text{m/s}$", r"b) $p=500\ \text{kg}\cdot\text{m/s}$", r"c) $p\approx608\ \text{kg}\cdot\text{m/s}$"],
  r"Nhận dạng: đề cho <strong>động lượng của hệ nhiều vật</strong> và <strong>góc giữa các chuyển động</strong> → tính từng $p_i=m_iv_i$ rồi cộng vectơ theo góc."),
 sol(R4, [
  (r"Chọn chiều dương, vận tốc sau", [P(r"Chọn chiều dương là chiều bóng tới vách:"), M(r"v_1=+4{,}0\ \text{m/s}"),
                                      P(r"Bóng bật ngược lại nên vận tốc sau mang dấu $-$:"), A(r"v_2=-4{,}0\ \text{m/s}")]),
  (r"Ý a — bật lại cùng tốc độ", [M(r"\Delta p=m(v_2-v_1)=0{,}10\,(-4{,}0-4{,}0)"), A(r"\Delta p=-0{,}80\ \text{kg}\cdot\text{m/s}"),
                                  P(r"Dấu $-$: $\Delta\vec p$ hướng ra xa vách.")]),
  (r"Ý b — bật lại chậm hơn", [P(r"Vận tốc sau là $v_2=-3{,}0\ \text{m/s}$:"), M(r"\Delta p=0{,}10\,(-3{,}0-4{,}0)"), A(r"\Delta p=-0{,}70\ \text{kg}\cdot\text{m/s}"),
                               P(r"Bóng bật lại chậm hơn nên $\lvert\Delta p\rvert$ nhỏ hơn ở ý a.")]),
  (r"Ý c — đổi chiều dương", [P(r"Chiều dương là chiều bóng bật ra khỏi vách: cả hai vận tốc đổi dấu, $v_1=-4{,}0\ \text{m/s}$ và $v_2=+4{,}0\ \text{m/s}$:"),
                              M(r"\Delta p=0{,}10\,\bigl(4{,}0-(-4{,}0)\bigr)"), A(r"\Delta p=+0{,}80\ \text{kg}\cdot\text{m/s}"),
                              P(r"Độ lớn không đổi; chỉ dấu đổi theo chiều dương.")]),
  (r"Kiểm tra", [P(r"Hiệu hai tốc độ $4{,}0-4{,}0=0$ cho $\Delta p=0$ — vô lí vì bóng đã đổi hướng ✓."), M(r"\lvert\Delta p\rvert=m(v+v')=0{,}10\,(4{,}0+4{,}0)=0{,}80"),
                  P(r"Khớp với ý a và ý c ✓.")])],
  [r"a) $\Delta p=-0{,}80\ \text{kg}\cdot\text{m/s}$", r"b) $\Delta p=-0{,}70\ \text{kg}\cdot\text{m/s}$", r"c) $\Delta p=+0{,}80\ \text{kg}\cdot\text{m/s}$"],
  r"Nhận dạng: đề nói <strong>bật ngược lại</strong> → chọn chiều dương, hai vận tốc trái dấu, $\Delta p=m(v_2-v_1)$."),
 sol(R5, [
  (r"Độ biến thiên động lượng", [P(r"Bóng dừng hẳn nên $v_2=0$; chiều dương là chiều bay nên $v_1=+20\ \text{m/s}$:"), M(r"\Delta p=m(v_2-v_1)=0{,}40\,(0-20)"),
                                 A(r"\Delta p=-8{,}0\ \text{kg}\cdot\text{m/s}")]),
  (r"Ý a — tay giữ cứng", [M(r"F=\dfrac{\Delta p}{\Delta t}=\dfrac{-8{,}0}{0{,}010}"), A(r"F=-800\ \text{N}"),
                           P(r"Độ lớn $800\ \text{N}$; dấu $-$: lực của tay hướng ngược chiều bay của bóng.")]),
  (r"Ý b — tay co lại", [P(r"Bóng vẫn từ $20\ \text{m/s}$ về $0$ nên $\Delta p$ vẫn là $-8{,}0\ \text{kg}\cdot\text{m/s}$; chỉ $\Delta t$ đổi:"),
                         M(r"F'=\dfrac{\Delta p}{\Delta t'}=\dfrac{-8{,}0}{0{,}050}"), A(r"F'=-160\ \text{N}"), P(r"Độ lớn $160\ \text{N}$.")]),
  (r"So sánh hai lực", [M(r"\dfrac{F'}{F}=\dfrac{\Delta t}{\Delta t'}=\dfrac{0{,}010}{0{,}050}"), A(r"\dfrac{F'}{F}=0{,}20"),
                        P(r"Cùng $\Delta p$ thì thời gian dừng dài gấp $5$ lần làm lực nhỏ đi $5$ lần. Co tay theo bóng nên đỡ đau hơn; đệm, túi khí, găng tay hoạt động theo cùng nguyên tắc.")]),
  (r"Kiểm tra", [P(r"Trọng lượng bóng cỡ $0{,}40\cdot10=4{,}0\ \text{N}$, chỉ khoảng $0{,}5\,\%$ của $800\ \text{N}$, nên bỏ qua trọng lượng là hợp lí ✓."),
                  P(r"Đơn vị: $\text{kg}\cdot\text{m/s}\,/\,\text{s}=\text{N}$ ✓.")])],
  [r"a) $\lvert F\rvert=800\ \text{N}$ (ngược chiều bay)", r"b) $\lvert F'\rvert=160\ \text{N}$", r"c) $F'/F=0{,}20$: dừng chậm hơn thì lực nhỏ hơn"],
  r"Nhận dạng: vật <strong>dừng hẳn sau thời gian Δt</strong> → $F=\Delta p/\Delta t$; muốn lực nhỏ thì kéo dài $\Delta t$."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>khối lượng, tốc độ và chiều chuyển động</b> → nghĩ tới <b>p = mv</b>, ngược chiều dương thì vận tốc mang dấu âm.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Động lượng của xe tải", r"Động lượng $p_1$ của xe tải bằng bao nhiêu?", 22500, "kg·m/s", 100,
       loi=r"Nhân thẳng $1{,}5$ và $54$ mà không đổi tấn sang kg, km/h sang m/s."),
  buoc(r"Động lượng của ô tô con", r"Động lượng $p_2$ của ô tô con (theo chiều dương đã chọn) bằng bao nhiêu?", -15000, "kg·m/s", 100,
       loi=r"Bỏ qua việc xét dấu theo chiều dương đã chọn, hoặc nhân với km/h chưa đổi.",
       ke=[(r"Đổi tốc độ sang m/s, rồi gắn dấu trừ cho vận tốc vì ngược chiều dương", True),
           (r"Thế thẳng số km/h vào $p=mv$ cho đỡ phải đổi", r"Với đơn vị $\text{kg}\cdot\text{m/s}$, vận tốc phải tính bằng m/s; dùng km/h cho kết quả sai."),
           (r"Lấy vận tốc dương vì tốc độ không âm", r"Tốc độ không âm, nhưng vận tốc có hướng: ngược chiều dương thì mang dấu trừ.")]),
  buoc(r"So sánh độ lớn", r"Xe nào có động lượng với độ lớn lớn hơn?",
       loi=r"So sánh theo tốc độ thay vì theo tích $m\cdot v$, hoặc kết luận hai xe bằng nhau vì ngược chiều.",
       lua_chon=[(r"Xe tải, vì $\lvert p_1\rvert\gt\lvert p_2\rvert$", True),
                 (r"Ô tô con, vì chạy nhanh hơn", r"Động lượng phụ thuộc cả khối lượng lẫn tốc độ; ô tô nhanh hơn nhưng nhẹ hơn."),
                 (r"Bằng nhau, vì hai xe ngược chiều", r"Ngược chiều chỉ làm hai động lượng trái dấu; độ lớn vẫn do $m\cdot v$ quyết định.")],
       ke=[(r"Bỏ dấu rồi so hai độ lớn $\lvert p_1\rvert$ và $\lvert p_2\rvert$", True),
           (r"Cộng $p_1+p_2$ rồi xét dấu của tổng", r"Tổng là động lượng của cả hệ, không cho biết xe nào lớn hơn."),
           (r"So tốc độ hai xe rồi kết luận", r"Động lượng còn phụ thuộc khối lượng; chỉ so tốc độ là bỏ quên một nửa.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực tác dụng trong khoảng thời gian ngắn</b> → nghĩ tới <b>xung lượng FΔt</b>, bằng độ biến thiên động lượng.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Xung lượng của lực đẩy", r"Xung lượng của lực đẩy bằng bao nhiêu?", 9.0, "N·s", 0.05,
       loi=r"Dùng $\Delta t$ tính bằng ms mà không đổi sang giây, kết quả gấp nghìn lần."),
  buoc(r"Tốc độ ra khỏi nòng", r"Tốc độ $v_2$ của viên đạn khi ra khỏi nòng bằng bao nhiêu?", 900, "m/s", 5,
       loi=r"Dùng khối lượng tính bằng gam mà không đổi sang kg, hoặc chia lực cho khối lượng rồi quên nhân thời gian.",
       ke=[(r"Đặt xung lượng bằng $mv_2-0$ rồi rút $v_2$", True),
           (r"Lấy $v_2=F/m$", r"$F/m$ là gia tốc (m/s²); muốn tốc độ phải nhân thêm thời gian tác dụng."),
           (r"Lấy $v_2=F\Delta t\cdot m$", r"Xung lượng bằng $m\,v_2$, nên $v_2$ bằng xung lượng chia cho $m$, không nhân.")]),
  buoc(r"Nòng ngắn hơn", r"Tốc độ ra khỏi nòng khi thời gian đẩy chỉ còn $0{,}50\ \text{ms}$ bằng bao nhiêu?", 450, "m/s", 3,
       loi=r"Cho rằng cùng lực thì tốc độ không đổi, quên rằng thời gian đẩy đã đổi.",
       ke=[(r"Giữ nguyên $F$, thay $\Delta t$ mới vào xung lượng", True),
           (r"Giữ nguyên tốc độ vì lực không đổi", r"Cùng lực nhưng tác dụng ngắn hơn thì xung lượng nhỏ hơn, nên $v_2$ cũng nhỏ đi."),
           (r"Nhân đôi lực rồi tính lại với $\Delta t$ cũ", r"Đề giữ nguyên lực, chỉ đổi thời gian đẩy.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>động lượng của hệ nhiều vật</b> và <b>góc giữa các chuyển động</b> → nghĩ tới <b>cộng vectơ theo góc α</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc(r"Động lượng của xe 1", r"Độ lớn động lượng $p_1$ của xe 1 bằng bao nhiêu?", 300, "kg·m/s", 1,
       loi=r"Nhầm khối lượng của hai xe khi thế số."),
  buoc(r"Động lượng của xe 2", r"Độ lớn động lượng $p_2$ của xe 2 bằng bao nhiêu?", 400, "kg·m/s", 1,
       loi=r"Dùng tốc độ của xe 1 cho xe 2."),
  buoc(r"Ngược chiều ($\alpha=180^\circ$)", r"Độ lớn động lượng của hệ khi hai xe chạy ngược chiều bằng bao nhiêu?", 100, "kg·m/s", 1,
       loi=r"Cộng hai độ lớn như khi cùng chiều, hoặc dùng căn tổng bình phương của trường hợp vuông góc.",
       ke=[(r"Chọn chiều dương rồi cộng đại số hai động lượng trái dấu", True),
           (r"Cộng hai độ lớn $p_1+p_2$", r"Chỉ khi cùng chiều mới cộng độ lớn; ngược chiều thì hai vectơ triệt tiêu một phần."),
           (r"Dùng $\sqrt{p_1^2+p_2^2}$", r"Căn tổng bình phương chỉ dành cho hai vectơ vuông góc.")]),
  buoc(r"Vuông góc ($\alpha=90^\circ$)", r"Độ lớn động lượng của hệ khi hai xe chạy trên hai đường vuông góc bằng bao nhiêu?", 500, "kg·m/s", 2,
       loi=r"Cộng thẳng hai độ lớn, hoặc quên khai căn sau khi cộng bình phương.",
       ke=[(r"Dựng hai vectơ làm hai cạnh góc vuông, tổng là cạnh huyền", True),
           (r"Cộng hai độ lớn $p_1+p_2$", r"Cộng thẳng độ lớn chỉ đúng khi hai vectơ cùng hướng; ở đây tổng vectơ ngắn hơn tổng hai độ dài."),
           (r"Lấy hiệu $\lvert p_1-p_2\rvert$", r"Hiệu chỉ đúng khi hai vectơ ngược hướng.")]),
  buoc(r"Hợp nhau $60^\circ$", r"Độ lớn động lượng của hệ khi hai vận tốc hợp nhau $60^\circ$ bằng bao nhiêu?", 608, "kg·m/s", 3,
       loi=r"Dùng nhầm dấu của số hạng chứa $\cos\alpha$, hoặc coi như vuông góc.",
       ke=[(r"Dùng $p^2=p_1^2+p_2^2+2p_1p_2\cos\alpha$ với $\alpha=60^\circ$", True),
           (r"Dùng $p^2=p_1^2+p_2^2-2p_1p_2\cos\alpha$", r"Sai dấu: $\alpha$ là góc giữa hai vectơ chung gốc nên số hạng chứa $\cos\alpha$ mang dấu $+$."),
           (r"Coi như vuông góc: $p=\sqrt{p_1^2+p_2^2}$", r"Công thức đó chỉ đúng khi $\cos\alpha=0$, tức $\alpha=90^\circ$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>bật ngược lại</b> → nghĩ tới <b>chọn chiều dương</b>: hai vận tốc trái dấu, Δp = m(v₂ − v₁).",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Chọn chiều dương, vận tốc sau", r"Chọn chiều dương là chiều bóng tới vách. Vận tốc $v_2$ của bóng sau va chạm (ý a) bằng bao nhiêu?", -4.0, "m/s", 0.05,
       loi=r"Bỏ qua việc xét dấu của vận tốc theo chiều dương đã chọn."),
  buoc(r"Ý a — bật lại cùng tốc độ", r"Độ biến thiên động lượng $\Delta p$ ở ý a bằng bao nhiêu?", -0.80, "kg·m/s", 0.01,
       loi=r"Lấy hiệu hai tốc độ nên ra kết quả không đáng có, hoặc bỏ dấu của $v_2$.",
       ke=[(r"Lấy $m(v_2-v_1)$ với $v_2$ mang dấu trừ", True),
           (r"Lấy $m\,(\lvert v_2\rvert-\lvert v_1\rvert)$", r"Hiệu hai độ lớn bỏ quên việc bóng đã đổi hướng."),
           (r"Chỉ lấy $mv_2$", r"$\Delta p$ là sau trừ trước; còn phải trừ động lượng trước va chạm.")]),
  buoc(r"Ý b — bật lại chậm hơn", r"Độ biến thiên động lượng $\Delta p$ ở ý b bằng bao nhiêu?", -0.70, "kg·m/s", 0.01,
       loi=r"Dùng $v_2$ của ý a, hoặc lấy hiệu hai tốc độ.",
       ke=[(r"Thay $v_2$ mới (trái dấu $v_1$) vào $m(v_2-v_1)$", True),
           (r"Giữ nguyên kết quả ý a vì bóng cũng tới với tốc độ cũ", r"Tốc độ sau đã khác nên $v_2$ khác, $\Delta p$ khác."),
           (r"Lấy hiệu hai tốc độ rồi nhân $m$", r"Hiệu hai tốc độ không cho đúng $\Delta p$ vì $v_1$ và $v_2$ trái dấu.")]),
  buoc(r"Ý c — đổi chiều dương", r"Chọn chiều dương là chiều bóng bật ra khỏi vách. Độ biến thiên động lượng ở ý a bằng bao nhiêu?", 0.80, "kg·m/s", 0.01,
       loi=r"Chỉ đổi dấu một trong hai vận tốc, hoặc giữ nguyên các dấu cũ.",
       ke=[(r"Đổi dấu cả $v_1$ lẫn $v_2$ theo chiều dương mới rồi tính lại", True),
           (r"Giữ nguyên kết quả ý a vì vật không đổi", r"Đổi chiều dương thì cả hai vận tốc phải xét lại dấu, nên kết quả không thể giữ nguyên."),
           (r"Chỉ đổi dấu $v_2$, giữ $v_1$", r"Cả hai vận tốc đều phải xét lại theo chiều dương mới.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật dừng hẳn sau thời gian Δt</b> → nghĩ tới <b>F = Δp/Δt</b>; muốn lực nhỏ thì kéo dài Δt.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Độ biến thiên động lượng", r"Độ biến thiên động lượng $\Delta p$ của bóng (chiều dương là chiều bay) bằng bao nhiêu?", -8.0, "kg·m/s", 0.1,
       loi=r"Lấy $mv_1$ mà không trừ động lượng sau, hoặc bỏ dấu dù $\Delta\vec p$ ngược chiều dương."),
  buoc(r"Ý a — tay giữ cứng", r"Độ lớn lực trung bình của tay lên bóng ở ý a bằng bao nhiêu?", 800, "N", 5,
       loi=r"Nhân $\Delta p$ với $\Delta t$ thay vì chia, hoặc thay trọng lượng bóng vào làm lực dừng.",
       ke=[(r"Lấy độ biến thiên động lượng chia cho thời gian dừng", True),
           (r"Lấy $\Delta p\cdot\Delta t$", r"Xung lượng bằng $F\Delta t$, nên $F=\Delta p/\Delta t$; nhân là sai phép tính."),
           (r"Lấy lực bằng trọng lượng của bóng", r"Trọng lượng là lực hút của Trái Đất; lực làm bóng dừng là lực nằm ngang của tay.")]),
  buoc(r"Ý b — tay co lại", r"Độ lớn lực trung bình của tay lên bóng ở ý b bằng bao nhiêu?", 160, "N", 2,
       loi=r"Cho rằng $\Delta p$ nhỏ đi vì tay mềm; hoặc giữ nguyên lực của ý a.",
       ke=[(r"Giữ nguyên $\Delta p$ (cùng bóng, cùng dừng hẳn), thay thời gian dừng mới", True),
           (r"Cho $\Delta p$ nhỏ đi vì tay mềm", r"Bóng vẫn từ tốc độ cũ về $0$ nên $\Delta p$ như nhau; tay mềm chỉ làm $\Delta t$ dài hơn."),
           (r"Giữ nguyên lực của ý a vì cùng một quả bóng", r"Cùng $\Delta p$ nhưng $\Delta t$ khác thì $F=\Delta p/\Delta t$ khác.")]),
  buoc(r"So sánh hai lực", r"Lực ở ý b bằng bao nhiêu lần lực ở ý a?", 0.20, None, 0.01,
       loi=r"Đảo ngược tỉ số, hoặc so hai độ biến thiên động lượng thay vì so hai lực.",
       ke=[(r"Chia lực ý b cho lực ý a", True),
           (r"Chia lực ý a cho lực ý b", r"“Ý b bằng bao nhiêu lần ý a” là lấy ý b chia ý a; đảo lại sẽ ra tỉ số lớn hơn $1$."),
           (r"Chia $\Delta t$ ở ý b cho $\Delta t$ ở ý a", r"Lực tỉ lệ nghịch với thời gian dừng nên tỉ số lực là nghịch đảo tỉ số thời gian.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập, xếp dễ → khó ═════════════
SEP = '<p class="text-base leading-relaxed my-2"><strong class="font-bold">Câu'
PIECES = [SEP + p for q in OLD for p in q["body_html"].split(SEP)[1:]]
assert len(PIECES) == 17
# chỉ số: D1 Câu k → k−1 ; D2 Câu k → k+3
KEEP = [(2, "Dễ"), (10, "Trung bình"), (7, "Trung bình"), (14, "Trung bình"), (5, "Khó")]


def fix(i, h):
    h = re.sub(r'<img[^>]*>', '', h)
    h = re.sub(r'\$\\left\\\{ \\begin\{aligned\}60 km/h = \\frac\{50\}\{3\}\\\\ m/s\\\\ 30 km/h = 10 m/s\\\\ \\end\{aligned\} \\right\\\}\$',
               r'$60\\ \\text{km/h}=\\frac{50}{3}\\ \\text{m/s};\\ 30\\ \\text{km/h}=10\\ \\text{m/s}$', h)
    h = re.sub(r'\$\\left\\\{ \\begin\{aligned\}v_\{2\}\\\\ = 0 m/s\\\\ v_\{1\} = 54 km/h = 15 m/s\\end\{aligned\} \\right\\\}\$',
               r'$v_{2}=0\\ \\text{m/s};\\ v_{1}=54\\ \\text{km/h}=15\\ \\text{m/s}$', h)
    h = h.replace("l,5 kg", "1,5 kg")
    h = h.replace(r"\left( 400-1000 \right)=-600 N.$", r"\left( 400-1000 \right)=-6\ \text{kg.m/s}\Rightarrow F=-600\ \text{N}.$")
    if i == 7:
        h += '<p class="text-base leading-relaxed my-2">Độ lớn lực hãm là $15000\\ \\text{N}$.</p>'
    h = h.replace("$m=10 gram$", r"$m=10\ \text{g}$").replace("$v_{1}=1000 m/s$", r"$v_{1}=1000\ \text{m/s}$").replace("$v_{2}=400 m/s,$", r"$v_{2}=400\ \text{m/s},$")
    h = h.replace("=-10.000.15=-150000 N.", r"=-10000.15=-150000\ \text{kg.m/s}.")
    return h


parts = []
for k, (i, lv) in enumerate(KEEP, 1):
    h = fix(i, PIECES[i])
    h = re.sub(r'<strong class="font-bold">Câu \d+:?(\s*\[[A-Z]+\])?:?</strong>', f'<strong class="font-bold">Bài {k}.</strong>', h, count=1)
    h = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", h)
    mk = '<p class="text-base leading-relaxed my-2"><strong class="font-bold">Hướng dẫn giải</strong></p>'
    assert mk in h, i
    de, gi = h.split(mk, 1)
    parts.append(f'<h4>Bài {k} · {lv}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>')
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))

write(J, 73, "Bài 28. Động lượng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
