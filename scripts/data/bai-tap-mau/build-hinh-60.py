"""Bài tập mẫu Bài 15 "Định luật 2 Newton" (Vật lí 10) — lesson_id 60. 6 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/60.quet-dang.json). Hình: hinh_60.py. Ví dụ cũ (old/60.json, 13 ví dụ):
  - VD7 (kéo 45 N, ma sát 15 N, 5 s) → biên tập thành Dạng 4 (số liệu mới);
  - VD1 (xe bán tải phanh) → dạng cùng kiểu là Dạng 5 (số mới); lời giải gốc làm tròn sớm (4,6 → 11 500 N, đúng ≈ 11 160 N) nên BỎ;
  - VD4, VD3, VD2, VD10, VD12, VD9 → tu_luan, đã sửa chữ (VD9 a₂, VD2 "đầu", =&gt; thành \Rightarrow); VD11 bỏ vì dùng g = 9,8 (đã tự tính lại, khớp);
  - BỎ: VD5 (t = (10−2)/0,4 = 20 s, lời giải ghi 12,5 s), VD6 (phép tính 100/3 − 17,5 ra −0,931 chứ không phải −0,947; phụ thuộc hình),
    VD8 (đáp số b ghi 22,4 rồi 22,5), VD13 (lũy thừa 10 trong đề sai, phụ thuộc hình).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-60.py   (idempotent, ghi 60.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_60 import *

J = os.path.join(HERE, "60.json")
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOPICS = {t["id"]: t["name"] for t in json.load(open(os.path.join(ROOT, "scripts/data/question-topics.json"))) if t["lesson_id"] == 60}
T123 = TOPICS[123]
assert T123 == "Định luật 2 Newton — bài toán động lực học"

# ═════════════ SỐ LIỆU + TỰ GIẢI ĐỘC LẬP (assert) ═════════════
def near(x, y, tol=1e-9): return abs(x - y) <= tol * max(1, abs(y))
# D1
m1, F1 = 0.250, 0.8; a1 = F1 / m1
assert near(a1, 3.2) and not near(F1 / 250, a1) and not near(m1 / F1, a1) and not near(F1 * m1, a1)
# D2
m2, F2, Fms2 = 35, 120, 50; Fhl2 = F2 - Fms2; a2 = Fhl2 / m2
assert near(Fhl2, 70) and near(a2, 2.0) and len({a2, F2 / m2, (F2 + Fms2) / m2, Fms2 / m2}) == 4 and Fhl2 not in (F2, F2 + Fms2)
# D3
Fa, aa, mh, Fb = 15, 0.5, 40, 28; mxe = Fa / aa; mtot = mxe + mh; a3 = Fb / mtot
assert near(mxe, 30) and near(mtot, 70) and near(a3, 0.4)
assert len({round(a3, 6), round(Fb / mxe, 6), round(Fb / mh, 6), aa}) == 4              # các cách sai khác đáp án
assert near(a3 / aa, (Fb / Fa) / (mtot / mxe)) and near(a3 / aa, 0.8)
assert 28 / 15 < 2 and 70 / 30 > 2 and Fb / mxe > aa
# D4
m4, F4, Fms4, t4 = 12, 54, 18, 6; Fhl4 = F4 - Fms4; a4 = Fhl4 / m4; v4 = a4 * t4; s4 = 0.5 * a4 * t4 ** 2
assert near(Fhl4, 36) and near(a4, 3) and near(v4, 18) and near(s4, 54) and near(v4 / 2 * t4, s4) and near(v4 * t4, 2 * s4)
assert F4 / m4 != a4 and a4 * t4 ** 2 != s4 and a4 * t4 != s4
# D5
m5, v5k, s5 = 1400, 108, 90; v05 = v5k / 3.6; a5 = (0 - v05 ** 2) / (2 * s5); Fh5 = m5 * abs(a5)
assert near(v05, 30) and near(a5, -5) and near(Fh5, 7000)
assert not near(m5 * (v05 ** 2 / s5), Fh5) and not near(m5 * (v5k ** 2 / (2 * s5)), Fh5) and not near(m5 * v05, Fh5) and not near(m5 / abs(a5), Fh5)
assert near(m5 * (v5k ** 2 / (2 * s5)) / Fh5, 12.96) and near(-v05 / a5, 6) and near(v05 / 2 * 6, s5)
# D6
m6, v6k, Fk6 = 1800, 90, 900; v06 = v6k / 3.6; Fc6 = Fk6; a6 = -Fc6 / m6; t6 = (0 - v06) / a6; s6 = (0 - v06 ** 2) / (2 * a6)
assert near(v06, 25) and near(a6, -0.5) and near(t6, 50) and near(s6, 625) and near(v06 / 2 * t6, s6) and near(v06 * t6, 2 * s6)
assert not near(v06 ** 2 / abs(a6), s6) and not near(v06 / abs(a6), s6) and (Fk6 - Fc6) / m6 == 0 and near(v06 / (-a6) * -1, -t6)
# số liệu đề không trùng ví dụ trong bài lý thuyết (80/40/80 kg; 20 kg/100/60 N; 60 kg/90/30 N/4 s; 1,2 t/15 m/s/25 m; 1 t/36 km/h/30 m; 1000 kg/20 m/s/40 m; 200 g/0,5 N)
for combo in [(m2, F2, Fms2), (m4, F4, Fms4, t4), (m5, v5k, s5), (m6, v6k, Fk6)]:
    assert combo not in [(20, 100, 60), (60, 90, 30, 4), (1200, 15, 25), (1000, 36, 30), (1000, 20, 40)]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Xe điều khiển từ xa: tìm gia tốc từ lực và khối lượng", topic=T123,
      problem_html=r"""<p>Một xe điều khiển từ xa có khối lượng $250\ \text{g}$ đứng yên trên mặt bàn nhẵn. Động cơ kéo xe bằng lực nằm ngang $0{,}8\ \text{N}$; bỏ qua ma sát và lực cản của không khí. Tìm gia tốc của xe.</p>"""),
 dict(label="Dạng 2 · Trung bình · Kéo thùng hàng có ma sát: hợp lực và gia tốc", topic=T123,
      problem_html=r"""<p>Một công nhân kéo thùng hàng $35\ \text{kg}$ trên sàn kho bằng sợi dây nằm ngang với lực $120\ \text{N}$. Sàn tác dụng lên thùng lực ma sát $50\ \text{N}$. Thùng đang trượt về phía người kéo. Tìm độ lớn và hướng gia tốc của thùng.</p>"""),
 dict(label="Dạng 3 · Trung bình · Xe đẩy siêu thị: chất thêm hàng, đổi lực đẩy", topic=T123,
      problem_html=r"""<p>Xe đẩy siêu thị còn rỗng được đẩy bằng lực ngang $15\ \text{N}$ thì có gia tốc $0{,}5\ \text{m/s}^2$. Sau khi chất lên xe một kiện hàng $40\ \text{kg}$, người ta đẩy bằng lực ngang $28\ \text{N}$. Bỏ qua ma sát, lực đẩy là hợp lực lên xe. Tìm gia tốc của xe khi đã chất hàng.</p>"""),
 dict(label="Dạng 4 · Khá · Thùng hàng từ nghỉ: gia tốc, vận tốc và quãng đường theo thời gian", topic=T123,
      problem_html=r"""<p>Một thùng hàng $12\ \text{kg}$ đứng yên trên sàn nằm ngang. Một người kéo thùng bằng lực ngang $54\ \text{N}$; lực ma sát giữa thùng và sàn là $18\ \text{N}$. Tìm vận tốc và quãng đường thùng đi được sau $6\ \text{s}$ kể từ lúc bắt đầu kéo.</p>"""),
 dict(label="Dạng 5 · Khá · Ô tô phanh gấp: từ quãng đường phanh tìm lực hãm", topic=T123,
      problem_html=r"""<p>Ô tô khối lượng $1{,}4$ tấn đang chạy thẳng với tốc độ $108\ \text{km/h}$ thì tài xế phanh gấp. Xe để lại vết phanh dài $90\ \text{m}$ rồi dừng hẳn. Coi lực hãm không đổi và bỏ qua các lực cản khác. Tìm độ lớn của lực hãm và cho biết lực hãm hướng thế nào so với chiều chuyển động.</p>"""),
 dict(label="Dạng 6 · Khó · Tắt máy khi đang chạy đều: thời gian và quãng đường dừng", topic=T123,
      problem_html=r"""<p>Ô tô khối lượng $1{,}8$ tấn chạy thẳng đều với tốc độ $90\ \text{km/h}$ trên đường nằm ngang; khi đó lực kéo của động cơ là $900\ \text{N}$. Tại điểm O tài xế tắt máy, xe chạy chậm dần cho tới khi dừng. Coi lực cản của đường và không khí không đổi trong suốt quá trình. Tìm thời gian và quãng đường xe đi được từ O đến khi dừng.</p>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 3: chỉ khái niệm/điều kiện, hàng cần tìm: Đại lượng cần tìm) ═════════════
ANALYSIS = [
 [(r"“khối lượng $250\ \text{g}$”", r"$m=250\ \text{g}$", r"Khối lượng là mức quán tính; đơn vị SI là kg"),
  (r"“đứng yên trên mặt bàn nhẵn … bỏ qua ma sát và lực cản của không khí”", r"Không có lực cản", r"⚠ $F$ trong định luật 2 là hợp lực của các lực tác dụng lên vật"),
  (r"“kéo xe bằng lực nằm ngang $0{,}8\ \text{N}$”", r"$F=0{,}8\ \text{N}$ (nằm ngang)", r"Gia tốc cùng hướng hợp lực"),
  (r"“Tìm gia tốc của xe”", r"Cần $a$ (m/s²)", r"Đại lượng cần tìm")],
 [(r"“thùng hàng $35\ \text{kg}$”", r"$m=35\ \text{kg}$", r"Khối lượng đã ở kg"),
  (r"“kéo … bằng sợi dây nằm ngang với lực $120\ \text{N}$”", r"$F=120\ \text{N}$ (ngang)", r"⚠ $F$ trong định luật 2 là hợp lực; theo phương đứng, trọng lực và phản lực của sàn triệt tiêu nhau"),
  (r"“sàn tác dụng lực ma sát $50\ \text{N}$”", r"$F_{\text{ms}}=50\ \text{N}$", r"⚠ Lực ma sát cản chuyển động nên ngược chiều chuyển động"),
  (r"“đang trượt về phía người kéo”", r"Chiều chuyển động = chiều lực kéo", r"Chọn chiều dương"),
  (r"“độ lớn và hướng gia tốc”", r"Cần $a$ (m/s²) và hướng", r"Đại lượng cần tìm")],
 [(r"“còn rỗng … đẩy bằng lực ngang $15\ \text{N}$ … gia tốc $0{,}5\ \text{m/s}^2$”", r"$F_1=15\ \text{N}$; $a_1=0{,}5\ \text{m/s}^2$", r"Khối lượng xe chưa biết; định luật 2 liên hệ $F$, $m$, $a$"),
  (r"“chất lên xe một kiện hàng $40\ \text{kg}$”", r"$m_{\text{hàng}}=40\ \text{kg}$", r"⚠ Khối lượng cộng được khi các vật chuyển động cùng nhau"),
  (r"“đẩy bằng lực ngang $28\ \text{N}$”", r"$F_2=28\ \text{N}$", r"Lực đẩy mới"),
  (r"“bỏ qua ma sát, lực đẩy là hợp lực”", r"Không ma sát", r"⚠ Lực đẩy là hợp lực ở cả hai trường hợp"),
  (r"“gia tốc của xe khi đã chất hàng”", r"Cần $a_2$ (m/s²)", r"Đại lượng cần tìm")],
 [(r"“thùng hàng $12\ \text{kg}$ đứng yên”", r"$m=12\ \text{kg}$; $v_0=0$", r"Dữ kiện ngầm: đứng yên"),
  (r"“kéo thùng bằng lực ngang $54\ \text{N}$”", r"$F=54\ \text{N}$ (ngang)", r"⚠ $F$ trong định luật 2 là hợp lực, không phải một lực riêng lẻ"),
  (r"“lực ma sát … là $18\ \text{N}$”", r"$F_{\text{ms}}=18\ \text{N}$", r"⚠ Lực ma sát cản chuyển động nên ngược chiều chuyển động"),
  (r"“sau $6\ \text{s}$ kể từ lúc bắt đầu kéo”", r"$t=6\ \text{s}$", r"Công thức chuyển động thẳng biến đổi đều, dùng khi gia tốc không đổi"),
  (r"“vận tốc và quãng đường”", r"Cần $v$ (m/s) và $s$ (m)", r"Đại lượng cần tìm")],
 [(r"“ô tô khối lượng $1{,}4$ tấn”", r"$m=1{,}4$ tấn", r"Đổi tấn ra kg"),
  (r"“đang chạy … $108\ \text{km/h}$”", r"$v_0=108\ \text{km/h}$", r"⚠ Đổi km/h ra m/s trước khi thế số"),
  (r"“vết phanh dài $90\ \text{m}$ rồi dừng hẳn”", r"$s=90\ \text{m}$; $v=0$", r"Đề không cho thời gian phanh"),
  (r"“coi lực hãm không đổi … bỏ qua các lực cản khác”", r"Lực hãm là hợp lực, không đổi", r"⚠ $F$ trong định luật 2 là hợp lực; lực không đổi thì gia tốc không đổi"),
  (r"“độ lớn của lực hãm … hướng thế nào”", r"Cần $F$ (N) và chiều", r"Đại lượng cần tìm")],
 [(r"“ô tô khối lượng $1{,}8$ tấn”", r"$m=1{,}8$ tấn", r"Đổi tấn ra kg"),
  (r"“chạy thẳng đều với tốc độ $90\ \text{km/h}$”", r"$v_0=90\ \text{km/h}$; chuyển động thẳng đều", r"⚠ Đổi km/h ra m/s; liên hệ giữa vận tốc không đổi và gia tốc"),
  (r"“khi đó lực kéo của động cơ là $900\ \text{N}$”", r"$F_{\text{k}}=900\ \text{N}$", r"Các lực cùng phương chuyển động"),
  (r"“tại điểm O tài xế tắt máy”", r"Lực kéo không còn", r"Xét lại các lực tác dụng lên xe"),
  (r"“lực cản … không đổi trong suốt quá trình”", r"$F_{\text{cản}}$ không đổi", r"⚠ Lực không đổi thì gia tốc không đổi, mới dùng được công thức chuyển động thẳng biến đổi đều"),
  (r"“thời gian và quãng đường … đến khi dừng”", r"Cần $t$ (s) và $s$ (m); $v=0$ lúc dừng", r"Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> khối lượng là mức quán tính của vật; gia tốc là tốc độ thay đổi của vận tốc.",
       r"<strong>Định luật 2 Newton:</strong> gia tốc cùng hướng hợp lực, tỉ lệ thuận với hợp lực, tỉ lệ nghịch với khối lượng.",
       r"<strong>Công thức:</strong> $a=\dfrac{F_{\text{hl}}}{m}$, với $1\ \text{N}=1\ \text{kg}\cdot\text{m/s}^2$.",
       r"<strong>Điều kiện:</strong> $F_{\text{hl}}$ là hợp lực; $m$ phải đổi ra kg trước khi thế số."]
RC2 = [r"<strong>Khái niệm:</strong> hợp lực là tổng vectơ mọi lực tác dụng lên vật; lực ma sát cản chuyển động nên ngược chiều chuyển động.",
       r"<strong>Định luật 2 Newton:</strong> gia tốc cùng hướng hợp lực.",
       r"<strong>Công thức:</strong> $a=\dfrac{F_{\text{hl}}}{m}$; hai lực ngược chiều trên một đường thẳng thì hợp lực bằng hiệu hai độ lớn.",
       r"<strong>Điều kiện:</strong> $F$ là hợp lực chứ không phải một lực riêng lẻ; theo phương đứng, trọng lực và phản lực của sàn triệt tiêu nhau."]
RC3 = [r"<strong>Khái niệm:</strong> khối lượng là mức quán tính và cộng được: xe chở hàng chuyển động cùng nhau thì khối lượng cả hệ là tổng.",
       r"<strong>Định luật 2 Newton:</strong> biết $F$ và $a$ thì suy ra $m$; biết $F$ và $m$ thì suy ra $a$.",
       r"<strong>Công thức:</strong> $m=\dfrac{F}{a}$ và $a=\dfrac{F}{m}$.",
       r"<strong>Điều kiện:</strong> bỏ qua ma sát nên lực đẩy là hợp lực ở cả hai trường hợp."]
RC4 = [r"<strong>Khái niệm:</strong> hợp lực quyết định gia tốc; gia tốc quyết định vận tốc và vị trí thay đổi thế nào theo thời gian.",
       r"<strong>Định luật 2 Newton:</strong> $a=\dfrac{F_{\text{hl}}}{m}$, cùng hướng hợp lực.",
       r"<strong>Công thức động học</strong> (gia tốc không đổi): $v=v_0+at$ và $s=v_0t+\tfrac12at^2$.",
       r"<strong>Điều kiện:</strong> hợp lực không đổi nên $a$ không đổi, mới dùng được hai công thức động học; thùng xuất phát từ nghỉ nên $v_0=0$."]
RC5 = [r"<strong>Khái niệm:</strong> lực hãm làm vật chậm dần; hợp lực ngược chiều chuyển động thì gia tốc ngược chiều vận tốc.",
       r"<strong>Định luật 2 Newton:</strong> $F_{\text{hl}}=ma$, với hợp lực chính là lực hãm.",
       r"<strong>Công thức động học</strong> không có $t$: $v^2-v_0^2=2as$.",
       r"<strong>Điều kiện:</strong> lực hãm không đổi nên $a$ không đổi; đổi km/h ra m/s và tấn ra kg trước khi thế số."]
RC6 = [r"<strong>Khái niệm:</strong> chuyển động thẳng đều có gia tốc bằng không, nên hợp lực bằng không (các lực cân bằng).",
       r"<strong>Định luật 2 Newton:</strong> $F_{\text{hl}}=ma$; $a=0$ thì $F_{\text{hl}}=0$.",
       r"<strong>Công thức động học:</strong> $v=v_0+at$ và $v^2-v_0^2=2as$.",
       r"<strong>Điều kiện:</strong> lực cản không đổi nên $a$ không đổi sau khi tắt máy; đổi km/h ra m/s và tấn ra kg."]

SOLS = [
 sol(RC1, [
  ("Đổi khối lượng ra kg", [P(r"Đơn vị lực là $\text{N}=\text{kg}\cdot\text{m/s}^2$ nên $m$ phải tính bằng kg."), M(r"m=250\ \text{g}=\dfrac{250}{1000}\ \text{kg}"), A(r"m=0{,}25\ \text{kg}")]),
  ("Tính gia tốc", [P(r"Bỏ qua ma sát và lực cản nên lực kéo nằm ngang là hợp lực: $F_{\text{hl}}=0{,}8\ \text{N}$."), M(r"a=\dfrac{F_{\text{hl}}}{m}"), M(r"a=\dfrac{0{,}8}{0{,}25}"), A(r"a=3{,}2\ \text{m/s}^2")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{N/kg}=\text{m/s}^2$."), P(r"Gia tốc cùng hướng lực kéo; xe tăng tốc nên hợp lí."), P(r"Nếu để $m=250$ (gam) rồi chia thì $a$ nhỏ đi $1000$ lần, vô lí với xe đồ chơi tăng tốc rõ rệt.")])],
  [r"$a=3{,}2\ \text{m/s}^2$, cùng hướng lực kéo"],
  r"Nhận dạng: đề cho <strong>lực và khối lượng (gam)</strong>, hỏi <strong>gia tốc</strong> → đổi ra kg rồi $a=F_{\text{hl}}/m$."),
 sol(RC2, [
  ("Tìm hợp lực", [P(r"Chọn chiều dương là chiều chuyển động (chiều lực kéo). Lực kéo $F=120\ \text{N}$ cùng chiều dương, lực ma sát $F_{\text{ms}}=50\ \text{N}$ ngược chiều dương."), M(r"F_{\text{hl}}=F-F_{\text{ms}}"), M(r"F_{\text{hl}}=120-50"), A(r"F_{\text{hl}}=70\ \text{N}")]),
  ("Tính gia tốc", [M(r"a=\dfrac{F_{\text{hl}}}{m}"), M(r"a=\dfrac{70}{35}"), A(r"a=2{,}0\ \text{m/s}^2")]),
  ("Hướng của gia tốc", [P(r"Gia tốc cùng hướng hợp lực. Hợp lực dương nên $\vec a$ cùng chiều lực kéo, tức cùng chiều chuyển động."), A(r"T:Gia tốc hướng về phía người kéo (cùng chiều lực kéo).")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{N/kg}=\text{m/s}^2$."), P(r"Lực kéo lớn hơn ma sát nên thùng tăng tốc theo chiều kéo: hợp lí."), P(r"Nếu lấy riêng lực kéo chia cho khối lượng (bỏ ma sát) thì gia tốc lớn hơn thực tế; ma sát luôn làm giảm gia tốc khi cản chuyển động.")])],
  [r"$a=2{,}0\ \text{m/s}^2$", r"Hướng: cùng chiều lực kéo (về phía người kéo)"],
  r"Nhận dạng: có <strong>lực kéo và lực ma sát</strong> cùng tác dụng → tìm <strong>hợp lực</strong> trước, rồi mới chia cho khối lượng."),
 sol(RC3, [
  ("Khối lượng xe rỗng", [P(r"Trường hợp thứ nhất: lực đẩy là hợp lực, $F_1=15\ \text{N}$ và $a_1=0{,}5\ \text{m/s}^2$."), M(r"m_{\text{xe}}=\dfrac{F_1}{a_1}"), M(r"m_{\text{xe}}=\dfrac{15}{0{,}5}"), A(r"m_{\text{xe}}=30\ \text{kg}")]),
  ("Khối lượng khi chở hàng", [P(r"Xe và kiện hàng chuyển động cùng nhau; khối lượng cộng được."), M(r"m=m_{\text{xe}}+m_{\text{hàng}}=30+40"), A(r"m=70\ \text{kg}")]),
  ("Gia tốc khi chở hàng", [M(r"a_2=\dfrac{F_2}{m}"), M(r"a_2=\dfrac{28}{70}"), A(r"a_2=0{,}40\ \text{m/s}^2")]),
  ("Kiểm tra", [P(r"Lực đẩy tăng chưa tới gấp đôi, khối lượng tăng hơn gấp đôi nên gia tốc nhỏ hơn lúc xe rỗng: hợp lí."), P(r"Tỉ số: $\dfrac{a_2}{a_1}=\dfrac{F_2/F_1}{m/m_{\text{xe}}}=\dfrac{28/15}{70/30}=0{,}8$ và $\dfrac{0{,}40}{0{,}5}=0{,}8$: khớp."), P(r"Nếu quên khối lượng hàng thì gia tốc lớn hơn lúc xe rỗng, trái với việc xe nặng hơn.")])],
  [r"$a_2=0{,}40\ \text{m/s}^2$"],
  r"Nhận dạng: <strong>cùng một xe, đổi lực hoặc chất thêm hàng</strong> → suy khối lượng từ $F$ và $a$, cộng khối lượng rồi tính lại."),
 sol(RC4, [
  ("Tìm hợp lực", [P(r"Chọn chiều dương là chiều kéo. Lực kéo cùng chiều dương, lực ma sát ngược chiều dương."), M(r"F_{\text{hl}}=F-F_{\text{ms}}"), M(r"F_{\text{hl}}=54-18"), A(r"F_{\text{hl}}=36\ \text{N}")]),
  ("Tính gia tốc", [M(r"a=\dfrac{F_{\text{hl}}}{m}"), M(r"a=\dfrac{36}{12}"), A(r"a=3{,}0\ \text{m/s}^2")]),
  ("Vận tốc sau 6 s", [P(r"Thùng đứng yên lúc đầu nên $v_0=0$."), M(r"v=v_0+at"), M(r"v=0+3{,}0\cdot6"), A(r"v=18\ \text{m/s}")]),
  ("Quãng đường sau 6 s", [M(r"s=v_0t+\tfrac12at^2"), M(r"s=0+\tfrac12\cdot3{,}0\cdot6^2"), A(r"s=54\ \text{m}")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{N/kg}=\text{m/s}^2$; $\text{m/s}^2\cdot\text{s}=\text{m/s}$."), P(r"Cách kiểm khác: vận tốc trung bình $\dfrac{0+18}{2}=9\ \text{m/s}$, nhân $6\ \text{s}$ ra $54\ \text{m}$: khớp."), P(r"Nếu nhân vận tốc cuối với $t$ thì ra gấp đôi, sai vì vận tốc tăng dần từ $0$.")])],
  [r"$v=18\ \text{m/s}$, cùng chiều lực kéo", r"$s=54\ \text{m}$"],
  r"Nhận dạng: <strong>vật bắt đầu từ nghỉ, có lực kéo và ma sát, hỏi sau t giây</strong> → định luật 2 Newton để có $a$, rồi công thức động học."),
 sol(RC5, [
  ("Đổi đơn vị", [M(r"v_0=108\ \text{km/h}=\dfrac{108}{3{,}6}\ \text{m/s}"), A(r"v_0=30\ \text{m/s}"), P(r"Khối lượng: $m=1{,}4\ \text{tấn}=1400\ \text{kg}$.")]),
  ("Gia tốc", [P(r"Chọn chiều dương là chiều chuyển động; lúc dừng $v=0$, quãng đường $s=90\ \text{m}$. Đề không cho thời gian nên dùng công thức không có $t$."), M(r"v^2-v_0^2=2as"), M(r"a=\dfrac{v^2-v_0^2}{2s}=\dfrac{0-30^2}{2\cdot90}"), A(r"a=-5{,}0\ \text{m/s}^2"), P(r"Dấu âm: gia tốc ngược chiều chuyển động.")]),
  ("Độ lớn lực hãm", [M(r"F_{\text{hl}}=ma"), M(r"|F_{\text{hl}}|=1400\cdot5{,}0"), A(r"|F_{\text{hl}}|=7000\ \text{N}")]),
  ("Chiều của lực hãm", [P(r"Gia tốc âm nên hợp lực (chính là lực hãm) ngược chiều chuyển động; trọng lực và phản lực của đường theo phương đứng triệt tiêu nhau."), A(r"T:Lực hãm hướng ngược chiều chuyển động của xe.")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{kg}\cdot\text{m/s}^2=\text{N}$."), P(r"Thời gian phanh $t=\dfrac{0-30}{-5{,}0}=6\ \text{s}$; vận tốc trung bình $\dfrac{30+0}{2}\cdot6=90\ \text{m}$: khớp quãng đường."), P(r"Nếu thế $108$ (km/h) thẳng vào công thức thì lực hãm lớn gấp gần $13$ lần, vô lí.")])],
  [r"Độ lớn lực hãm: $7000\ \text{N}$", r"Chiều: ngược chiều chuyển động của xe"],
  r"Nhận dạng: đề cho <strong>quãng đường phanh và tốc độ ban đầu, không cho thời gian</strong>, hỏi lực → tìm gia tốc rồi áp dụng định luật 2 Newton."),
 sol(RC6, [
  ("Lực cản lúc chạy đều", [P(r"Xe chạy thẳng đều nên $a=0$, do đó $F_{\text{hl}}=ma=0$: lực kéo cân bằng với lực cản."), M(r"F_{\text{cản}}=F_{\text{k}}"), A(r"F_{\text{cản}}=900\ \text{N}")]),
  ("Gia tốc sau khi tắt máy", [P(r"Tắt máy thì lực kéo không còn; lực cản trở thành hợp lực, ngược chiều chuyển động. Chọn chiều dương là chiều chuyển động; $m=1{,}8\ \text{tấn}=1800\ \text{kg}$."), M(r"a=\dfrac{-F_{\text{cản}}}{m}"), M(r"a=\dfrac{-900}{1800}"), A(r"a=-0{,}50\ \text{m/s}^2")]),
  ("Thời gian dừng", [P(r"Đổi vận tốc đầu."), M(r"v_0=90\ \text{km/h}=25\ \text{m/s}"), M(r"v=v_0+at\ \Rightarrow\ t=\dfrac{v-v_0}{a}=\dfrac{0-25}{-0{,}50}"), A(r"t=50\ \text{s}")]),
  ("Quãng đường dừng", [M(r"v^2-v_0^2=2as"), M(r"s=\dfrac{v^2-v_0^2}{2a}=\dfrac{0-25^2}{2\cdot(-0{,}50)}"), A(r"s=625\ \text{m}")]),
  ("Kiểm tra", [P(r"Vận tốc trung bình $\dfrac{25+0}{2}=12{,}5\ \text{m/s}$; nhân $50\ \text{s}$ ra $625\ \text{m}$: khớp."), P(r"Nếu coi xe vẫn chạy $25\ \text{m/s}$ suốt $50\ \text{s}$ thì ra $1250\ \text{m}$, gấp đôi; sai vì xe chậm dần."), P(r"Lực cản $900\ \text{N}$ lên xe $1{,}8$ tấn cho gia tốc cỡ vài phần mười $\text{m/s}^2$: xe lăn bánh khá lâu mới dừng, hợp lí.")])],
  [r"Thời gian: $t=50\ \text{s}$", r"Quãng đường: $s=625\ \text{m}$"],
  r"Nhận dạng: <strong>chạy đều</strong> thì các lực cân bằng; <strong>tắt máy</strong> thì chỉ còn lực cản làm xe chậm dần."),
]

# ═════════════ BƯỚC TỰ GIẢI ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>lực và khối lượng cho bằng gam</b>, hỏi gia tốc → nghĩ tới <b>định luật 2 Newton</b>, đổi ra <b>kg</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi khối lượng ra kg", r"Khối lượng của xe bằng bao nhiêu kilôgam?", 0.25, "kg", 0.005,
       loi=r"Để nguyên số gam rồi đem chia: đơn vị lực N là kg·m/s², nên kết quả nhỏ đi khoảng một nghìn lần."),
  buoc("Tính gia tốc", r"Gia tốc của xe bằng bao nhiêu?", 3.2, "m/s²", 0.05,
       loi=r"Đảo tỉ số (lấy khối lượng chia lực) hoặc nhân lực với khối lượng; gia tốc tỉ lệ thuận với lực và tỉ lệ nghịch với khối lượng.",
       ke=[(r"Chia hợp lực cho khối lượng đã đổi ra kg", True),
           (r"Chia khối lượng cho lực", r"Đảo tỉ số: gia tốc tỉ lệ thuận với lực, tỉ lệ nghịch với khối lượng, nên lực ở tử số."),
           (r"Nhân lực với khối lượng", r"Khối lượng lớn thì xe khó tăng tốc hơn nên gia tốc phải giảm khi $m$ tăng; phép nhân làm ngược lại, và đơn vị N·kg không phải $\text{m/s}^2$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực kéo và lực ma sát</b> cùng tác dụng → nghĩ tới <b>hợp lực</b>, không phải một lực riêng lẻ.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tìm hợp lực", r"Độ lớn hợp lực nằm ngang tác dụng lên thùng bằng bao nhiêu?", 70, "N", 1,
       loi=r"Lấy luôn lực kéo làm hợp lực vì quên ma sát, hoặc cộng hai lực ngược chiều thay vì lấy hiệu."),
  buoc("Tính gia tốc", r"Độ lớn gia tốc của thùng bằng bao nhiêu?", 2.0, "m/s²", 0.05,
       loi=r"Chia lực kéo (chưa trừ ma sát) cho khối lượng.",
       ke=[(r"Chia hợp lực vừa tìm cho khối lượng của thùng", True),
           (r"Chia lực kéo cho khối lượng của thùng", r"Ma sát cũng tác dụng lên thùng, ngược chiều lực kéo; lực kéo chưa phải hợp lực."),
           (r"Chia lực ma sát cho khối lượng của thùng", r"Lực ma sát chỉ là một trong hai lực nằm ngang; gia tốc do hợp lực của cả hai quyết định.")]),
  buoc("Hướng của gia tốc"),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cùng một xe, đổi lực hoặc chất thêm hàng</b> → nghĩ tới <b>khối lượng cộng được</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Khối lượng xe rỗng", r"Khối lượng của xe khi chưa chất hàng bằng bao nhiêu?", 30, "kg", 0.5,
       loi=r"Nhân lực với gia tốc thay vì chia, hoặc bỏ qua trường hợp thứ nhất vì nghĩ khối lượng xe chưa biết nên không tính được."),
  buoc("Khối lượng khi chở hàng", r"Khối lượng của cả xe và kiện hàng bằng bao nhiêu?", 70, "kg", 0.5,
       loi=r"Chỉ lấy khối lượng kiện hàng (quên xe) hoặc giữ nguyên khối lượng xe rỗng.",
       ke=[(r"Cộng khối lượng xe với khối lượng kiện hàng", True),
           (r"Chỉ lấy khối lượng kiện hàng vì xe đã tính ở trường hợp trước", r"Xe và hàng chuyển động cùng nhau nên cả hai cùng là vật cần tăng tốc."),
           (r"Giữ nguyên khối lượng xe vì chỉ lực đẩy thay đổi", r"Lực đẩy không làm đổi khối lượng; hàng chất lên xe làm tổng khối lượng tăng.")]),
  buoc("Gia tốc khi chở hàng", r"Gia tốc của xe khi đã chất hàng bằng bao nhiêu?", 0.4, "m/s²", 0.01,
       loi=r"Chia lực đẩy mới cho khối lượng xe rỗng (quên hàng), hoặc giữ gia tốc cũ vì vẫn là chiếc xe ấy.",
       ke=[(r"Chia lực đẩy mới cho tổng khối lượng của xe và hàng", True),
           (r"Giữ gia tốc cũ vì vẫn là chiếc xe ấy", r"Lực đẩy và khối lượng đều đã đổi nên gia tốc phải tính lại."),
           (r"Chia lực đẩy mới cho khối lượng xe rỗng", r"Kiện hàng nằm trên xe, chuyển động cùng xe, nên khối lượng cần tăng tốc gồm cả hàng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật bắt đầu từ nghỉ, có lực kéo và ma sát, hỏi sau t giây</b> → định luật 2 Newton kết hợp động học.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tìm hợp lực", r"Độ lớn hợp lực nằm ngang tác dụng lên thùng bằng bao nhiêu?", 36, "N", 1,
       loi=r"Lấy luôn lực kéo làm hợp lực, hoặc cộng lực kéo với lực ma sát."),
  buoc("Tính gia tốc", r"Gia tốc của thùng bằng bao nhiêu?", 3.0, "m/s²", 0.05,
       loi=r"Chia lực kéo (chưa trừ ma sát) cho khối lượng.",
       ke=[(r"Dùng hợp lực vừa tìm: chia cho khối lượng", True),
           (r"Chia lực kéo cho khối lượng", r"Ma sát cũng tác dụng lên thùng nên lực kéo chưa phải hợp lực."),
           (r"Chia khối lượng cho hợp lực", r"Đảo tỉ số: gia tốc tỉ lệ nghịch với khối lượng, khối lượng phải ở mẫu số.")]),
  buoc("Vận tốc sau 6 s", r"Vận tốc của thùng sau 6 s bằng bao nhiêu?", 18, "m/s", 0.3,
       loi=r"Nhầm công thức vận tốc với công thức quãng đường (có ½ và $t^2$), hoặc lấy $s$ làm vận tốc.",
       ke=[(r"Vật xuất phát từ nghỉ: dùng $v=v_0+at$ với $v_0=0$", True),
           (r"Dùng $v=at^2$", r"$t^2$ chỉ xuất hiện ở công thức quãng đường; gia tốc đã là tốc độ đổi vận tốc nên $v=at$ khi xuất phát từ nghỉ."),
           (r"Dùng $v=\tfrac12at$", r"$\tfrac12at$ là vận tốc trung bình trong khoảng thời gian đó (khi xuất phát từ nghỉ), không phải vận tốc tại thời điểm cuối.")]),
  buoc("Quãng đường sau 6 s", r"Quãng đường thùng đi được sau 6 s bằng bao nhiêu?", 54, "m", 1,
       loi=r"Lấy vận tốc cuối nhân với thời gian (như chạy đều) hoặc quên hệ số ½.",
       ke=[(r"Dùng $s=v_0t+\tfrac12at^2$ với $v_0=0$", True),
           (r"Dùng $s=vt$ với $v$ là vận tốc sau 6 s", r"Vận tốc tăng dần từ $0$, không giữ không đổi suốt 6 s; $vt$ cho quãng đường lớn hơn thực tế."),
           (r"Dùng $s=at^2$", r"Thiếu hệ số $\tfrac12$: quãng đường là $s=\tfrac12at^2$ khi xuất phát từ nghỉ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>quãng đường phanh, không cho thời gian</b>, hỏi lực hãm → nghĩ tới <b>định luật 2 Newton</b> kết hợp động học.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi đơn vị", r"Tốc độ ban đầu của ô tô bằng bao nhiêu mét trên giây?", 30, "m/s", 0.5,
       loi=r"Nhân với 3,6 thay vì chia, hoặc không đổi nên thế thẳng km/h vào công thức."),
  buoc("Gia tốc", r"Gia tốc của ô tô (chiều dương là chiều chuyển động) bằng bao nhiêu?", -5.0, "m/s²", 0.1,
       loi=r"Quên số 2 trong $2as$, hoặc chia $v_0$ cho $s$.",
       ke=[(r"Dùng $v^2-v_0^2=2as$ với $v=0$ vì đề cho quãng đường, không cho thời gian", True),
           (r"Dùng $v=v_0+at$", r"Đề không cho thời gian phanh nên công thức này chưa dùng được."),
           (r"Dùng $s=\tfrac12at^2$ như xe xuất phát từ nghỉ", r"Lúc bắt đầu phanh xe đang chạy nhanh nên $v_0\neq0$; công thức đó chỉ đúng khi $v_0=0$.")]),
  buoc("Độ lớn lực hãm", r"Độ lớn lực hãm bằng bao nhiêu?", 7000, "N", 100,
       loi=r"Để khối lượng ở đơn vị tấn khi nhân, nên lực nhỏ đi một nghìn lần.",
       ke=[(r"Áp dụng định luật 2: nhân khối lượng (đã đổi ra kg) với độ lớn gia tốc", True),
           (r"Nhân khối lượng với tốc độ ban đầu", r"Tích $mv_0$ có đơn vị $\text{kg}\cdot\text{m/s}$, không phải N; lực cần gia tốc chứ không phải vận tốc."),
           (r"Chia khối lượng cho gia tốc", r"Đảo tỉ số: định luật 2 là $F=ma$, lực tỉ lệ thuận với cả hai.")]),
  buoc("Chiều của lực hãm"),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>chạy đều</b> rồi <b>tắt máy</b> → nghĩ tới <b>hợp lực</b> của từng giai đoạn.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Lực cản lúc chạy đều", r"Lực cản tác dụng lên xe lúc đang chạy đều bằng bao nhiêu?", 900, "N", 10,
       loi=r"Cho rằng chạy đều thì không có lực cản, hoặc coi lực cản khác lực kéo vì xe đang chuyển động."),
  buoc("Gia tốc sau khi tắt máy", r"Sau khi tắt máy, gia tốc của xe (chiều dương là chiều chuyển động) bằng bao nhiêu?", -0.5, "m/s²", 0.02,
       loi=r"Dùng hợp lực bằng không như lúc chạy đều, hoặc quên đổi tấn ra kg.",
       ke=[(r"Xét lại các lực còn tác dụng sau khi tắt máy, rồi chia hợp lực cho khối lượng đã đổi ra kg", True),
           (r"Hợp lực vẫn là lực kéo trừ lực cản", r"Tắt máy thì lực kéo của động cơ không còn nữa."),
           (r"Hợp lực vẫn bằng không như lúc chạy đều", r"Hợp lực chỉ bằng không khi lực kéo còn cân bằng lực cản; tắt máy rồi lực cản không còn được cân bằng.")]),
  buoc("Thời gian dừng", r"Từ lúc tắt máy đến khi xe dừng mất bao lâu?", 50, "s", 1,
       loi=r"Quên đổi km/h ra m/s, hoặc lẫn dấu của gia tốc nên ra thời gian âm.",
       ke=[(r"Đổi vận tốc đầu ra m/s rồi dùng $v=v_0+at$ với $v=0$", True),
           (r"Lấy vận tốc đầu chia cho lực cản", r"Công thức $v=v_0+at$ cần gia tốc, không phải lực; chia cho lực thì đơn vị không ra giây."),
           (r"Dùng gia tốc của giai đoạn chạy đều", r"Gia tốc lúc chạy đều bằng không; sau khi tắt máy hợp lực đổi nên gia tốc cũng đổi, phải dùng gia tốc mới.")]),
  buoc("Quãng đường dừng", r"Quãng đường xe đi được từ O đến khi dừng bằng bao nhiêu?", 625, "m", 10,
       loi=r"Quên số 2 trong $2as$, hoặc dùng $s=v_0t$ như chạy đều.",
       ke=[(r"Dùng $v^2-v_0^2=2as$ (hoặc $s=v_0t+\tfrac12at^2$) với số liệu đã có", True),
           (r"Dùng $s=v_0t$ như xe chạy đều", r"Xe chậm dần nên quãng đường nhỏ hơn quãng đường nếu giữ nguyên vận tốc đầu."),
           (r"Dùng $s=\dfrac{v_0^2}{a}$", r"Thiếu số 2 ở mẫu: từ $v^2-v_0^2=2as$ suy ra $s=\dfrac{v_0^2}{2|a|}$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN (ví dụ cũ còn dùng được, giữ nguyên lời giải gốc) ═════════════
OLD = json.load(open(os.path.join(HERE, "old/60.json")))["questions"]
TU_LUAN = tu_luan_tu(OLD, [3, 2, 1, 9, 11, 8], {3: "Dễ", 2: "Dễ", 1: "Trung bình", 9: "Trung bình", 11: "Trung bình", 8: "Khó"})
_b = TU_LUAN["body_html"]
for _a, _c in [(r"\frac{1}{2}a_{1}t_{2}^{2}", r"\frac{1}{2}a_{2}t_{2}^{2}"), ("không vận tốc đâu", "không vận tốc đầu"), ("=&gt;", r"\Rightarrow "), ("=>", r"\Rightarrow ")]:
    _b = _b.replace(_a, _c)
TU_LUAN["body_html"] = _b

# ═════════════ GHI FILE ═════════════
write(J, 60, "Bài 15. Định luật 2 Newton", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
