"""Bài tập mẫu Bài 18 "Lực ma sát" (Vật lí 10) — lesson_id 63. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/63.quet-dang.json). Hình: hinh_63.py. Ví dụ cũ (old/63.json, 8 ví dụ):
VD1 bỏ (đề mơ hồ: lực F đặt vào A nhưng lời giải tính như đặt vào B, T lệch), VD2 bỏ (a = 0,71 sai, tính lại 0,165),
VD3 bỏ (cộng P2 thay vì trừ, a = 5,8 sai, tính lại 0,096); VD4, 5, 6, 7, 8 vào tu_luan (đã tính lại đúng).
Chủ đề: dạng 1, 2 gắn 127; dạng 3, 4, 5 gắn 128 (ngân hàng xếp cả câu kéo xiên vào 128).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-63.py   (idempotent, ghi 63.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_63 import *

J = os.path.join(HERE, "63.json")
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOPICS = {t["id"]: t["name"] for t in json.load(open(os.path.join(ROOT, "scripts/data/question-topics.json"))) if t["lesson_id"] == 63}
T127, T128 = TOPICS[127], TOPICS[128]

# ═════════════ SỐ LIỆU + TỰ GIẢI ĐỘC LẬP (assert) ═════════════
g = 9.8
# Dạng 1: tủ 50 kg, nghỉ cực đại 160 N, trượt đều 120 N
m1, Fmax1, Fmst1, Fa1, Fb1 = 50.0, 160.0, 120.0, 140.0, 200.0
a1 = (Fb1 - Fmst1) / m1
assert Fa1 < Fmax1 < Fb1 and Fa1 > Fmst1 and abs(a1 - 1.6) < 1e-9
assert abs((Fb1 - Fmax1) / m1 - 0.8) < 1e-9                       # cách sai (lấy 160 N): 0,8 khác 1,6
# Dạng 2: thùng 40 kg
m2, Fd, Fk, T2 = 40.0, 98.0, 150.0, 4.0
N2 = m2 * g; mu2 = Fd / N2; a2 = (Fk - mu2 * N2) / m2; v2 = a2 * T2; a2p = -mu2 * g; s2 = (0 - v2 ** 2) / (2 * a2p)
assert abs(N2 - 392) < 1e-9 and abs(mu2 - 0.25) < 1e-9 and abs(a2 - 1.3) < 1e-9 and abs(v2 - 5.2) < 1e-9
assert abs(a2p + 2.45) < 1e-9 and abs(s2 - 5.5184) < 1e-3
assert abs(Fk / m2 - 3.75) < 1e-9 and abs(Fk / m2 * T2 - 15) < 1e-9          # bỏ ma sát: khác đáp án
# Dạng 3: thùng 6,0 kg kéo xiên
m3, F3, al3, mu3 = 6.0, 30.0, math.radians(30), 0.30
N3 = m3 * g - F3 * math.sin(al3); Fm3 = mu3 * N3; a3 = (F3 * math.cos(al3) - Fm3) / m3
assert abs(N3 - 43.8) < 1e-9 and abs(Fm3 - 13.14) < 1e-9 and abs(a3 - 2.1402) < 1e-3
assert abs((F3 * math.cos(al3) - mu3 * m3 * g) / m3 - 1.390) < 1e-3          # sai: N = mg
assert abs((F3 - Fm3) / m3 - 2.810) < 1e-3 and abs((F3 * math.sin(al3) - Fm3) / m3 - 0.31) < 1e-2
assert abs(mu3 * m3 * g - 17.64) < 1e-9
# Dạng 4: bao 12 kg trượt xuống ván 5 m, 35°
m4, L4, al4, mu4 = 12.0, 5.0, math.radians(35), 0.30
N4 = m4 * g * math.cos(al4); Fm4 = mu4 * N4; a4 = (m4 * g * math.sin(al4) - Fm4) / m4; v4 = math.sqrt(2 * a4 * L4)
assert abs(N4 - 96.34) < 0.01 and abs(Fm4 - 28.90) < 0.01 and abs(a4 - 3.2127) < 1e-3 and abs(v4 - 5.668) < 2e-3
assert math.tan(al4) > mu4
assert abs(g * math.sin(al4) - 5.621) < 1e-3 and abs(math.sqrt(2 * g * math.sin(al4) * L4) - 7.497) < 2e-3
assert abs(mu4 * m4 * g - 35.28) < 1e-9 and abs(math.sqrt(2 * g * L4 * math.sin(al4)) - 7.497) < 2e-3
# Dạng 5: vật 3,0 kg lên dốc 25°
m5, v05, al5, mu5 = 3.0, 6.0, math.radians(25), 0.20
aup = g * (math.sin(al5) + mu5 * math.cos(al5)); s5 = v05 ** 2 / (2 * aup)
Px5 = m5 * g * math.sin(al5); Fn5 = mu5 * m5 * g * math.cos(al5)
adn = g * (math.sin(al5) - mu5 * math.cos(al5)); vdn = math.sqrt(2 * adn * s5)
assert abs(aup - 5.918) < 1e-3 and abs(s5 - 3.0417) < 1e-3 and Px5 > Fn5 and abs(Px5 - 12.42) < 0.01 and abs(Fn5 - 5.329) < 1e-3
assert abs(adn - 2.365) < 1e-3 and abs(vdn - 3.793) < 2e-3
assert abs(math.sqrt(2 * aup * s5) - 6.0) < 1e-9                                # cách sai: v = v0 (cơ năng bảo toàn)
assert abs(0.5 * m5 * (v05 ** 2 - vdn ** 2) - Fn5 * 2 * s5) < 1e-6              # công ma sát cả đi lẫn về = cơ năng mất
assert abs(g * math.sin(al5) - 4.141) < 1e-3                                    # sai: bỏ ma sát

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Ma sát nghỉ hay ma sát trượt: tủ đứng yên hay trượt", topic=T127,
      problem_html=r"""<p>Một tủ lạnh nặng $50\ \text{kg}$ đặt trên sàn nhà. Dùng lực kế kéo tủ theo phương ngang và tăng lực dần dần: tủ bắt đầu trượt khi lực kế chỉ $160\ \text{N}$. Khi tủ đã trượt, muốn giữ cho tủ trượt đều thì phải kéo bằng lực ngang $120\ \text{N}$.</p><ol type="a"><li>Kéo tủ bằng lực ngang $140\ \text{N}$. Tủ đứng yên hay trượt? Lực ma sát của sàn tác dụng lên tủ bằng bao nhiêu?</li><li>Kéo tủ bằng lực ngang $200\ \text{N}$. Tủ đứng yên hay trượt? Tính lực ma sát và gia tốc của tủ.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Ma sát trượt trên mặt ngang: hệ số ma sát, gia tốc và đoạn trượt thêm", topic=T127,
      problem_html=r"""<p>Một thùng gỗ $40\ \text{kg}$ trượt trên sàn xi măng nằm ngang. Dùng dây kéo theo phương ngang với lực $98\ \text{N}$ thì thùng trượt đều. Lấy $g=9{,}8\ \text{m/s}^2$.</p><ol type="a"><li>Tính hệ số ma sát trượt giữa thùng và sàn.</li><li>Kéo thùng từ trạng thái nghỉ bằng lực ngang $150\ \text{N}$ làm thùng trượt nhanh dần. Tính gia tốc của thùng.</li><li>Sau $4{,}0\ \text{s}$ kể từ lúc bắt đầu kéo bằng lực $150\ \text{N}$, người kéo buông dây. Thùng còn trượt thêm bao xa thì dừng lại?</li></ol>"""),
 dict(label="Dạng 3 · Khá · Kéo xiên lên: áp lực thay đổi, ma sát và gia tốc", topic=T128,
      problem_html=r"""<p>Một thùng $6{,}0\ \text{kg}$ đặt trên sàn nằm ngang, hệ số ma sát trượt giữa thùng và sàn là $0{,}30$. Người ta kéo thùng bằng sợi dây chếch lên, hợp với phương ngang góc $30^\circ$, lực kéo $30\ \text{N}$ làm thùng trượt từ trạng thái nghỉ. Lấy $g=9{,}8\ \text{m/s}^2$.</p><ol type="a"><li>Tính áp lực của thùng lên sàn.</li><li>Tính lực ma sát trượt tác dụng lên thùng.</li><li>Tính gia tốc của thùng.</li></ol>"""),
 dict(label="Dạng 4 · Khá · Trượt xuống mặt phẳng nghiêng: áp lực, ma sát, gia tốc và tốc độ", topic=T128,
      problem_html=r"""<p>Một bao hàng $12\ \text{kg}$ được thả không vận tốc đầu ở đỉnh một tấm ván dốc dài $5{,}0\ \text{m}$, nghiêng $35^\circ$ so với phương ngang. Hệ số ma sát trượt giữa bao hàng và ván là $0{,}30$. Lấy $g=9{,}8\ \text{m/s}^2$.</p><ol type="a"><li>Tính áp lực của bao hàng lên ván và lực ma sát trượt.</li><li>Tính gia tốc của bao hàng.</li><li>Tính tốc độ của bao hàng khi tới chân ván.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Lên dốc rồi có tụt xuống không: ma sát đổi chiều theo chuyển động", topic=T128,
      problem_html=r"""<p>Một vật $3{,}0\ \text{kg}$ ở chân một mặt phẳng nghiêng góc $25^\circ$ so với phương ngang, được truyền vận tốc đầu $6{,}0\ \text{m/s}$ dọc theo mặt dốc, hướng lên. Hệ số ma sát giữa vật và mặt dốc là $0{,}20$ (coi ma sát nghỉ cực đại bằng ma sát trượt). Lấy $g=9{,}8\ \text{m/s}^2$.</p><ol type="a"><li>Tính gia tốc của vật lúc đi lên và quãng đường vật đi lên được trên mặt dốc.</li><li>Tới điểm cao nhất, vật nằm yên lại hay trượt xuống?</li><li>Nếu vật quay về tới chân dốc, tính tốc độ của vật khi đó.</li></ol>"""),
]

ANALYSIS = [
 [(r"“tủ lạnh nặng $50\ \text{kg}$”", r"$m=50\ \text{kg}$", r"Khối lượng dùng trong định luật II Newton"),
  (r"“tủ bắt đầu trượt khi lực kế chỉ $160\ \text{N}$”", r"$160\ \text{N}$ (lúc bắt đầu trượt)", r"⚠ Hai mốc lực đo được là hai dữ kiện khác nhau"),
  (r"“giữ cho tủ trượt đều … kéo $120\ \text{N}$”", r"$120\ \text{N}$ (lúc trượt đều)", r"Vật chuyển động thẳng đều: hợp lực bằng $0$"),
  (r"“a) kéo bằng lực ngang $140\ \text{N}$”", r"$F=140\ \text{N}$", r"Ma sát nghỉ; ma sát trượt"),
  (r"“b) kéo bằng lực ngang $200\ \text{N}$”", r"$F=200\ \text{N}$", r"Định luật II Newton"),
  (r"“Tủ đứng yên hay trượt? lực ma sát?”", r"Cần kết luận và $F_{\text{ms}}$ (N)", r"Đại lượng cần tìm"),
  (r"“gia tốc của tủ”", r"Cần $a$ (m/s²)", r"Đại lượng cần tìm")],
 [(r"“thùng gỗ $40\ \text{kg}$ trượt trên sàn xi măng nằm ngang”", r"$m=40\ \text{kg}$; mặt ngang", r"⚠ Áp lực $N$ phụ thuộc cách đặt vật và hướng lực kéo"),
  (r"“kéo ngang với lực $98\ \text{N}$ thì thùng trượt đều”", r"$F=98\ \text{N}$; $a=0$", r"Chuyển động thẳng đều: hợp lực bằng $0$"),
  (r"“lấy $g=9{,}8\ \text{m/s}^2$”", r"$g=9{,}8\ \text{m/s}^2$", r"Trọng lượng $P=mg$"),
  (r"“b) kéo từ trạng thái nghỉ bằng lực ngang $150\ \text{N}$”", r"$F=150\ \text{N}$; $v_0=0$", r"⚠ Loại ma sát phụ thuộc vật đang đứng yên hay đang trượt"),
  (r"“c) sau $4{,}0\ \text{s}$ … buông dây”", r"$t=4{,}0\ \text{s}$; sau đó lực kéo bằng $0$", r"Mỗi giai đoạn có gia tốc riêng; động học biến đổi đều"),
  (r"“a) hệ số ma sát trượt”", r"Cần $\mu$", r"Đại lượng cần tìm"),
  (r"“b) gia tốc của thùng”", r"Cần $a$ (m/s²)", r"Đại lượng cần tìm"),
  (r"“c) thùng còn trượt thêm bao xa”", r"Cần $s$ (m)", r"Đại lượng cần tìm")],
 [(r"“thùng $6{,}0\ \text{kg}$ … sàn nằm ngang”", r"$m=6{,}0\ \text{kg}$; mặt ngang", r"Trọng lượng; áp lực lên sàn"),
  (r"“hệ số ma sát trượt … $0{,}30$”", r"$\mu=0{,}30$", r"Ma sát trượt $F_{\text{mst}}=\mu N$"),
  (r"“dây chếch lên, hợp với phương ngang góc $30^\circ$, lực kéo $30\ \text{N}$”", r"$F=30\ \text{N}$; $\alpha=30^\circ$", r"⚠ Lực chếch so với mặt tiếp xúc có thành phần theo cả hai phương"),
  (r"“làm thùng trượt từ trạng thái nghỉ”", r"$v_0=0$; thùng đang trượt", r"Định luật II Newton chiếu lên từng phương"),
  (r"“a) áp lực của thùng lên sàn”", r"Cần $N$ (N)", r"Đại lượng cần tìm"),
  (r"“b) lực ma sát trượt”", r"Cần $F_{\text{mst}}$ (N)", r"Đại lượng cần tìm"),
  (r"“c) gia tốc của thùng”", r"Cần $a$ (m/s²)", r"Đại lượng cần tìm")],
 [(r"“bao hàng $12\ \text{kg}$ được thả không vận tốc đầu”", r"$m=12\ \text{kg}$; $v_0=0$", r"Chuyển động biến đổi đều từ trạng thái nghỉ"),
  (r"“tấm ván dốc dài $5{,}0\ \text{m}$”", r"$L=5{,}0\ \text{m}$ (quãng đường)", r"Quãng đường vật đi dọc ván"),
  (r"“nghiêng $35^\circ$ so với phương ngang”", r"$\alpha=35^\circ$", r"⚠ Mặt tiếp xúc nghiêng: xét các lực theo phương dọc và vuông góc mặt tiếp xúc"),
  (r"“hệ số ma sát trượt … $0{,}30$”", r"$\mu=0{,}30$", r"Ma sát trượt ngược chiều trượt"),
  (r"“a) áp lực của bao hàng lên ván và lực ma sát trượt”", r"Cần $N$ (N), $F_{\text{mst}}$ (N)", r"Đại lượng cần tìm"),
  (r"“b) gia tốc của bao hàng”", r"Cần $a$ (m/s²)", r"Đại lượng cần tìm"),
  (r"“c) tốc độ khi tới chân ván”", r"Cần $v$ (m/s)", r"Đại lượng cần tìm")],
 [(r"“vật $3{,}0\ \text{kg}$ ở chân mặt phẳng nghiêng góc $25^\circ$”", r"$m=3{,}0\ \text{kg}$; $\alpha=25^\circ$", r"Trọng lực tách theo hai phương: dọc dốc và vuông góc dốc"),
  (r"“vận tốc đầu $6{,}0\ \text{m/s}$ dọc theo mặt dốc, hướng lên”", r"$v_0=6{,}0\ \text{m/s}$, hướng lên dốc", r"⚠ Ma sát trượt ngược chiều chuyển động tương đối của vật so với mặt tiếp xúc"),
  (r"“hệ số ma sát … $0{,}20$ (coi ma sát nghỉ cực đại bằng ma sát trượt)”", r"$\mu=0{,}20$; $F_{\text{msn max}}=F_{\text{mst}}$", r"⚠ Điều kiện để vật nằm yên hoặc chuyển động trên mặt tiếp xúc"),
  (r"“a) gia tốc lúc đi lên và quãng đường đi lên”", r"Cần $a$ (m/s²), $s$ (m)", r"Đại lượng cần tìm"),
  (r"“b) tới điểm cao nhất, nằm yên lại hay trượt xuống?”", r"Cần kết luận", r"Đại lượng cần tìm"),
  (r"“c) tốc độ khi về tới chân dốc”", r"Cần $v$ (m/s)", r"Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> vật chưa trượt chịu ma sát nghỉ, bằng đúng thành phần ngoại lực song song mặt tiếp xúc, tối đa là $F_{\text{msn max}}$.",
       r"<strong>Khái niệm:</strong> vật đang trượt chịu ma sát trượt $F_{\text{mst}}=\mu N$, thường nhỏ hơn $F_{\text{msn max}}$.",
       r"<strong>Định luật II Newton:</strong> hợp lực bằng $0$ khi vật đứng yên hoặc chuyển động thẳng đều; $F_{\text{hl}}=ma$ khi vật có gia tốc.",
       r"⚠ <strong>Điều kiện:</strong> vật đang đứng yên thì so lực kéo với $F_{\text{msn max}}$ trước, rồi mới chọn loại ma sát."]
RC2 = [r"<strong>Khái niệm:</strong> vật đang trượt chịu ma sát trượt, ngược chiều chuyển động.",
       r"<strong>Công thức:</strong> $F_{\text{mst}}=\mu N$; trên mặt ngang, lực kéo ngang thì $N=mg$.",
       r"<strong>Định luật II Newton:</strong> $F_{\text{hl}}=ma$; trượt đều thì hợp lực bằng $0$.",
       r"<strong>Động học:</strong> $v=v_0+at$; $v^2-v_0^2=2as$.",
       r"⚠ <strong>Điều kiện:</strong> $F_{\text{mst}}$ chỉ phụ thuộc $\mu$ và $N$, không đổi theo lực kéo hay tốc độ."]
RC3 = [r"<strong>Khái niệm:</strong> áp lực $N$ là lực ép vuông góc mặt tiếp xúc; ma sát trượt $F_{\text{mst}}=\mu N$.",
       r"<strong>Lực kéo xiên:</strong> tách thành $F\cos\alpha$ (nằm ngang, kéo vật đi) và $F\sin\alpha$ (thẳng đứng, nhấc bớt vật).",
       r"<strong>Định luật II Newton:</strong> chiếu lên phương đứng (không có gia tốc) và phương ngang ($F_{\text{hl}}=ma$).",
       r"⚠ <strong>Điều kiện:</strong> $N$ chỉ bằng $mg$ khi các lực khác không có thành phần vuông góc mặt tiếp xúc."]
RC4 = [r"<strong>Khái niệm:</strong> trên mặt nghiêng góc $\alpha$, trọng lực tách thành $mg\sin\alpha$ (dọc dốc, kéo vật xuống) và $mg\cos\alpha$ (ép vào dốc).",
       r"<strong>Công thức:</strong> $N=mg\cos\alpha$; $F_{\text{mst}}=\mu N$ hướng lên dốc, ngược chiều trượt.",
       r"<strong>Định luật II Newton</strong> chiếu lên trục dọc dốc: $mg\sin\alpha-F_{\text{mst}}=ma$.",
       r"<strong>Động học:</strong> $v^2-v_0^2=2as$ (không cần thời gian).",
       r"⚠ <strong>Điều kiện:</strong> vật trượt xuống được khi $\mu\lt\tan\alpha$."]
RC5 = [r"<strong>Khái niệm:</strong> ma sát trượt ngược chiều trượt: vật đi lên thì ma sát hướng xuống dốc, vật trượt xuống thì ma sát hướng lên dốc.",
       r"<strong>Công thức:</strong> $a_{\text{lên}}$ có $mg\sin\alpha+\mu mg\cos\alpha$; $a_{\text{xuống}}$ có $mg\sin\alpha-\mu mg\cos\alpha$.",
       r"<strong>Vật nằm yên trên dốc</strong> khi $mg\sin\alpha\le F_{\text{msn max}}=\mu mg\cos\alpha$.",
       r"<strong>Động học:</strong> $v^2-v_0^2=2as$.",
       r"⚠ <strong>Điều kiện:</strong> đổi chiều chuyển động thì đổi chiều ma sát, nên mỗi giai đoạn có gia tốc riêng."]

SOLS = [
 sol(RC1, [
  ("Kéo $140\\ \\text{N}$: so với mức bắt đầu trượt (câu a)", [P(r"Tủ đang đứng yên nên mốc để so là ma sát nghỉ cực đại, bằng lực kéo lúc tủ bắt đầu trượt:"), M(r"F=140\ \text{N}\ \lt\ F_{\text{msn max}}=160\ \text{N}"), P(r"Lực kéo chưa vượt mức cực đại nên tủ vẫn đứng yên. Không so với $120\ \text{N}$: đó là lực ma sát khi tủ đã trượt.")]),
  ("Ma sát nghỉ (câu a)", [P(r"Tủ đứng yên nên hợp lực bằng $0$: ma sát nghỉ cân bằng lực kéo."), M(r"F_{\text{msn}}=F"), A(r"F_{\text{msn}}=140\ \text{N}")]),
  ("Kéo $200\\ \\text{N}$: đứng yên hay trượt (câu b)", [M(r"F=200\ \text{N}\ \gt\ F_{\text{msn max}}=160\ \text{N}"), P(r"Lực kéo vượt mức cực đại, ma sát nghỉ không tăng thêm được nữa nên tủ bắt đầu trượt.")]),
  ("Ma sát khi tủ đang trượt (câu b)", [P(r"Giữ tủ trượt đều ($a=0$) thì lực kéo cân bằng ma sát trượt:"), M(r"F_{\text{mst}}=F_{\text{đều}}"), A(r"F_{\text{mst}}=120\ \text{N}"), P(r"Ma sát trượt không đổi theo lực kéo, nên khi kéo $200\ \text{N}$ vẫn là $120\ \text{N}$.")]),
  ("Gia tốc (câu b)", [M(r"F-F_{\text{mst}}=ma"), M(r"a=\dfrac{200-120}{50}"), A(r"a=1{,}6\ \text{m/s}^2")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{N/kg}=\text{m/s}^2$."), P(r"$a\gt0$ vì lực kéo lớn hơn ma sát trượt: tủ nhanh dần, đúng với việc tủ đã trượt."), P(r"Nếu lấy $160\ \text{N}$ làm lực ma sát khi trượt thì $a=0{,}8\ \text{m/s}^2$, chỉ bằng một nửa: $160\ \text{N}$ là mức để bắt đầu trượt, không phải lực ma sát lúc đang trượt.")])],
  [r"a) Tủ đứng yên; $F_{\text{msn}}=140\ \text{N}$", r"b) Tủ trượt; $F_{\text{mst}}=120\ \text{N}$; $a=1{,}6\ \text{m/s}^2$"],
  r"Nhận dạng: đề cho <strong>lực bắt đầu trượt</strong> và <strong>lực giữ trượt đều</strong> → vật đứng yên thì so lực kéo với $F_{\text{msn max}}$; đã trượt thì dùng ma sát trượt."),
 sol(RC2, [
  ("Hệ số ma sát (câu a)", [P(r"Lực kéo ngang trên mặt ngang nên áp lực bằng trọng lượng:"), M(r"N=mg=40\cdot9{,}8=392\ \text{N}"), P(r"Trượt đều nên ma sát trượt cân bằng lực kéo: $F_{\text{mst}}=98\ \text{N}$."), M(r"\mu=\dfrac{F_{\text{mst}}}{N}=\dfrac{98}{392}"), A(r"\mu=0{,}25")]),
  ("Gia tốc khi kéo $150\\ \\text{N}$ (câu b)", [P(r"Ma sát trượt vẫn là $98\ \text{N}$ (cùng $\mu$, cùng $N$):"), M(r"F-F_{\text{mst}}=ma"), M(r"a=\dfrac{150-98}{40}"), A(r"a=1{,}3\ \text{m/s}^2")]),
  ("Vận tốc lúc buông dây (câu c)", [P(r"Thùng bắt đầu từ trạng thái nghỉ, nhanh dần đều trong $4{,}0\ \text{s}$:"), M(r"v=at=1{,}3\cdot4{,}0"), A(r"v=5{,}2\ \text{m/s}")]),
  ("Gia tốc sau khi buông dây (câu c)", [P(r"Chọn chiều chuyển động làm chiều dương. Theo phương ngang chỉ còn ma sát trượt, ngược chiều chuyển động:"), M(r"-F_{\text{mst}}=ma'"), M(r"a'=-\mu g=-0{,}25\cdot9{,}8"), A(r"a'=-2{,}45\ \text{m/s}^2")]),
  ("Quãng đường trượt thêm (câu c)", [P(r"Thùng dừng lại nên vận tốc cuối bằng $0$:"), M(r"v'^2-v^2=2a's"), M(r"s=\dfrac{0-5{,}2^2}{2\cdot(-2{,}45)}"), A(r"s\approx5{,}52\ \text{m}")]),
  ("Kiểm tra", [P(r"Thời gian dừng $t=\dfrac{5{,}2}{2{,}45}\approx2{,}12\ \text{s}$; vận tốc trung bình $\dfrac{5{,}2}{2}=2{,}6\ \text{m/s}$ nên quãng đường $2{,}6\cdot2{,}12\approx5{,}5\ \text{m}$, khớp."), P(r"$\mu$ không có đơn vị; $|a'|=\mu g$ không phụ thuộc khối lượng thùng."), P(r"Nếu bỏ ma sát thì $a=\dfrac{150}{40}=3{,}75\ \text{m/s}^2$, gấp gần ba lần giá trị thật.")])],
  [r"a) $\mu=0{,}25$", r"b) $a=1{,}3\ \text{m/s}^2$", r"c) $s\approx5{,}52\ \text{m}$"],
  r"Nhận dạng: đề cho <strong>trượt đều</strong> rồi <strong>đổi lực kéo hoặc buông dây</strong> → $\mu$ không đổi; mỗi giai đoạn viết định luật II Newton riêng."),
 sol(RC3, [
  ("Áp lực của thùng lên sàn (câu a)", [P(r"Theo phương thẳng đứng thùng không chuyển động, hợp lực bằng $0$. Lực kéo nhấc bớt thùng một phần $F\sin\alpha$:"), M(r"N+F\sin\alpha-mg=0"), M(r"N=mg-F\sin\alpha=6{,}0\cdot9{,}8-30\cdot\sin30^\circ"), A(r"N=43{,}8\ \text{N}")]),
  ("Lực ma sát trượt (câu b)", [M(r"F_{\text{mst}}=\mu N=0{,}30\cdot43{,}8"), A(r"F_{\text{mst}}=13{,}14\ \text{N}")]),
  ("Gia tốc (câu c)", [P(r"Theo phương ngang chỉ có thành phần $F\cos\alpha$ kéo thùng đi, ma sát ngược lại:"), M(r"F\cos\alpha-F_{\text{mst}}=ma"), M(r"a=\dfrac{30\cdot\cos30^\circ-13{,}14}{6{,}0}"), A(r"a\approx2{,}14\ \text{m/s}^2")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{N/kg}=\text{m/s}^2$."), P(r"$F\cos30^\circ\approx26{,}0\ \text{N}$ lớn hơn nhiều $F_{\text{mst}}$ nên thùng trượt nhanh dần, đúng với đề."), P(r"Nếu coi $N=mg$ thì $F_{\text{mst}}=17{,}64\ \text{N}$ và $a\approx1{,}39\ \text{m/s}^2$: ma sát bị tính thừa vì quên lực kéo nhấc bớt thùng.")])],
  [r"a) $N=43{,}8\ \text{N}$", r"b) $F_{\text{mst}}=13{,}14\ \text{N}$", r"c) $a\approx2{,}14\ \text{m/s}^2$"],
  r"Nhận dạng: đề có <strong>lực kéo chếch một góc</strong> → tách $F$ thành hai thành phần; $N\ne mg$, rồi mới tính ma sát."),
 sol(RC4, [
  ("Áp lực lên ván (câu a)", [P(r"Vuông góc ván, bao hàng không chuyển động nên $N$ cân bằng thành phần $mg\cos\alpha$:"), M(r"N=mg\cos\alpha=12\cdot9{,}8\cdot\cos35^\circ"), A(r"N\approx96{,}3\ \text{N}")]),
  ("Lực ma sát trượt (câu a)", [M(r"F_{\text{mst}}=\mu N=0{,}30\cdot96{,}3"), A(r"F_{\text{mst}}\approx28{,}9\ \text{N}"), P(r"Hướng lên dốc, ngược chiều bao hàng trượt.")]),
  ("Gia tốc (câu b)", [P(r"Chiếu lên trục $x$ dọc ván, chiều dương hướng xuống dốc:"), M(r"mg\sin\alpha-\mu mg\cos\alpha=ma"), M(r"a=g(\sin\alpha-\mu\cos\alpha)"), M(r"a=9{,}8\,(0{,}5736-0{,}30\cdot0{,}8192)"), A(r"a\approx3{,}21\ \text{m/s}^2")]),
  ("Tốc độ ở chân ván (câu c)", [P(r"Thả không vận tốc đầu, quãng đường bằng chiều dài ván:"), M(r"v^2-0=2aL"), M(r"v=\sqrt{2\cdot3{,}21\cdot5{,}0}"), A(r"v\approx5{,}67\ \text{m/s}")]),
  ("Kiểm tra", [P(r"$\tan35^\circ\approx0{,}70\gt0{,}30$ nên bao hàng trượt xuống được, đúng với đề."), P(r"$a\lt g\sin\alpha\approx5{,}62\ \text{m/s}^2$: có ma sát nên gia tốc nhỏ hơn khi không có ma sát."), P(r"Không ma sát thì $v=\sqrt{2\cdot5{,}62\cdot5{,}0}\approx7{,}5\ \text{m/s}$, lớn hơn giá trị tính được.")])],
  [r"a) $N\approx96{,}3\ \text{N}$; $F_{\text{mst}}\approx28{,}9\ \text{N}$", r"b) $a\approx3{,}21\ \text{m/s}^2$", r"c) $v\approx5{,}67\ \text{m/s}$"],
  r"Nhận dạng: đề cho <strong>vật trượt trên mặt nghiêng có ma sát</strong> → $N=mg\cos\alpha$, rồi $a=g(\sin\alpha-\mu\cos\alpha)$; khối lượng triệt tiêu."),
 sol(RC5, [
  ("Gia tốc lúc đi lên (câu a)", [P(r"Chọn chiều dương hướng lên dốc. Thành phần trọng lực dọc dốc và ma sát đều hướng xuống dốc:"), M(r"-mg\sin\alpha-\mu mg\cos\alpha=ma"), M(r"a=-g(\sin\alpha+\mu\cos\alpha)=-9{,}8\,(0{,}4226+0{,}20\cdot0{,}9063)"), A(r"a\approx-5{,}918\ \text{m/s}^2"), P(r"Độ lớn $5{,}92\ \text{m/s}^2$, vật chậm dần.")]),
  ("Quãng đường đi lên (câu a)", [P(r"Tới điểm cao nhất vật dừng lại tức thời, $v=0$:"), M(r"0-v_0^2=2as"), M(r"s=\dfrac{-6{,}0^2}{2\cdot(-5{,}918)}"), A(r"s\approx3{,}04\ \text{m}")]),
  ("Nằm yên hay trượt xuống (câu b)", [P(r"So thành phần trọng lực dọc dốc với ma sát nghỉ cực đại:"), M(r"mg\sin\alpha=3{,}0\cdot9{,}8\cdot0{,}4226\approx12{,}4\ \text{N}"), M(r"F_{\text{msn max}}=\mu mg\cos\alpha=0{,}20\cdot3{,}0\cdot9{,}8\cdot0{,}9063\approx5{,}33\ \text{N}"), P(r"$12{,}4\ \text{N}\gt5{,}33\ \text{N}$: ma sát nghỉ không giữ nổi vật."), A(r"T:Câu b: vật <strong>trượt xuống</strong>.")]),
  ("Gia tốc lúc trượt xuống (câu c)", [P(r"Chiều chuyển động đổi nên ma sát hướng lên dốc. Chọn chiều dương hướng xuống dốc:"), M(r"mg\sin\alpha-\mu mg\cos\alpha=ma'"), M(r"a'=g(\sin\alpha-\mu\cos\alpha)=9{,}8\,(0{,}4226-0{,}20\cdot0{,}9063)"), A(r"a'\approx2{,}365\ \text{m/s}^2")]),
  ("Tốc độ khi về chân dốc (câu c)", [P(r"Vật bắt đầu trượt xuống từ điểm cao nhất, đi lại đúng quãng đường $s$:"), M(r"v^2-0=2a's"), M(r"v=\sqrt{2\cdot2{,}365\cdot3{,}042}"), A(r"v\approx3{,}79\ \text{m/s}")]),
  ("Kiểm tra", [P(r"$v\lt v_0=6{,}0\ \text{m/s}$: ma sát tiêu hao một phần cơ năng."), P(r"Gia tốc lúc xuống ($2{,}365$) nhỏ hơn lúc lên ($5{,}918$) vì ma sát đổi chiều."), P(r"Đối chiếu năng lượng: động năng mất $\tfrac12\cdot3{,}0\,(6{,}0^2-14{,}4)\approx32{,}4\ \text{J}$, bằng công của ma sát trên cả đường đi và về $5{,}33\cdot2\cdot3{,}042\approx32{,}4\ \text{J}$.")])],
  [r"a) $a\approx-5{,}918\ \text{m/s}^2$ (độ lớn $5{,}92$); $s\approx3{,}04\ \text{m}$", r"b) Vật trượt xuống", r"c) $v\approx3{,}79\ \text{m/s}$"],
  r"Nhận dạng: đề có <strong>vật đi lên rồi dừng trên dốc</strong> → kiểm $mg\sin\alpha$ với $F_{\text{msn max}}$ trước khi kết luận; lên và xuống có hai gia tốc khác nhau."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>vật đứng yên, đề cho hai mốc lực</b> → xác định <b>loại ma sát</b> trước khi tính.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Kéo ở câu a: đứng yên hay trượt", r"Kéo ngang tủ bằng lực ở câu a thì tủ đứng yên hay trượt?",
       loi=r"So lực kéo với lực ma sát lúc trượt đều thay vì ma sát nghỉ cực đại, nên kết luận tủ trượt.",
       lua_chon=[(r"Đứng yên, vì lực kéo chưa vượt mức bắt đầu trượt", True),
                 (r"Trượt, vì lực kéo đã lớn hơn lực giữ tủ trượt đều", r"Lực giữ tủ trượt đều là lực ma sát khi tủ ĐÃ trượt. Tủ đang đứng yên phải so với mức bắt đầu trượt là $160\ \text{N}$; lực kéo nhỏ hơn mức đó."),
                 (r"Trượt, vì đã có lực kéo thì tủ phải chuyển động", r"Có lực kéo chưa chắc có chuyển động: ma sát nghỉ tăng theo lực kéo tới giá trị cực đại, chỉ khi lực kéo vượt mức đó vật mới trượt.")]),
  buoc("Ma sát nghỉ ở câu a", r"Lực ma sát nghỉ tác dụng lên tủ ở câu a bằng bao nhiêu (đơn vị N)?", 140, "N", 1,
       loi=r"Dùng $\mu N$ cho vật đứng yên, hoặc lấy luôn mức cực đại làm ma sát nghỉ. Ma sát nghỉ chỉ bằng đúng lực kéo gây xu hướng trượt.",
       ke=[(r"Dùng điều kiện cân bằng (hợp lực bằng $0$) cho tủ đang đứng yên", True),
           (r"Lấy ma sát nghỉ bằng giá trị cực đại của nó, vì đó là giá trị lớn nhất", r"Mức cực đại chỉ là trần mà ma sát nghỉ có thể đạt; chưa chắc đã chạm tới trần."),
           (r"Dùng công thức ma sát trượt $\mu N$ với $N=mg$", r"Công thức $\mu N$ dùng cho vật đang trượt; tủ đứng yên thì dùng cân bằng lực.")]),
  buoc("Kéo ở câu b: đứng yên hay trượt", r"Kéo ngang tủ bằng lực ở câu b thì tủ đứng yên hay trượt?",
       loi=r"Cho rằng ma sát nghỉ luôn cân bằng được lực kéo, quên rằng nó có giá trị cực đại.",
       lua_chon=[(r"Trượt, vì lực kéo vượt mức bắt đầu trượt", True),
                 (r"Đứng yên, vì ma sát nghỉ luôn cân bằng lực kéo", r"Ma sát nghỉ chỉ cân bằng được tới giá trị cực đại; vượt mức đó nó không tăng thêm nữa nên tủ bị kéo đi."),
                 (r"Đứng yên, vì lực kéo nhỏ hơn trọng lượng của tủ", r"Trọng lượng là lực thẳng đứng, không đem so với lực kéo ngang; mốc để so là mức bắt đầu trượt đã đo.")],
       ke=[(r"So lực kéo với mức bắt đầu trượt (ma sát nghỉ cực đại)", True),
           (r"So lực kéo với lực giữ tủ trượt đều", r"Tủ đang đứng yên thì mức để so là ma sát nghỉ cực đại. Lực giữ trượt đều chỉ là ma sát khi tủ đã trượt."),
           (r"Tính ngay gia tốc từ định luật II Newton", r"Chưa biết tủ có trượt chưa thì chưa biết dùng ma sát nghỉ hay ma sát trượt; phải so với mức bắt đầu trượt trước.")]),
  buoc("Ma sát khi tủ đang trượt", r"Khi tủ đang trượt, lực ma sát từ sàn tác dụng lên tủ bằng bao nhiêu (đơn vị N)?", 120, "N", 1,
       loi=r"Lấy ma sát trượt bằng mức bắt đầu trượt, hoặc bằng chính lực kéo đang tác dụng.",
       ke=[(r"Dùng điều kiện trượt đều (hợp lực bằng $0$) cho lúc tủ đang trượt đều", True),
           (r"Lấy ma sát bằng mức bắt đầu trượt", r"Mức bắt đầu trượt là ma sát nghỉ cực đại; khi đã trượt ma sát tụt xuống ma sát trượt, thường nhỏ hơn."),
           (r"Lấy ma sát bằng lực đang kéo", r"Lực kéo lớn hơn ma sát nên mới có gia tốc; ma sát trượt không đổi theo lực kéo.")]),
  buoc("Gia tốc", r"Gia tốc của tủ ở câu b bằng bao nhiêu (đơn vị m/s²)?", 1.6, "m/s²", 0.05,
       loi=r"Lấy mức bắt đầu trượt làm lực ma sát trong định luật II Newton, hoặc bỏ ma sát và chia lực kéo cho khối lượng.",
       ke=[(r"Định luật II Newton với ma sát trượt: $a=\dfrac{F-F_{\text{mst}}}{m}$", True),
           (r"$a=\dfrac{F-F_{\text{msn max}}}{m}$", r"Tủ đã trượt thì ma sát tác dụng là ma sát trượt; ma sát nghỉ cực đại chỉ là mức bắt đầu trượt."),
           (r"$a=\dfrac{F}{m}$", r"Bỏ ma sát thì hợp lực quá lớn; ma sát luôn ngược chiều chuyển động và làm giảm hợp lực.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>trượt đều</b> rồi <b>đổi lực kéo hoặc buông dây</b> → $\mu$ không đổi; mỗi giai đoạn một gia tốc.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Hệ số ma sát", r"Hệ số ma sát trượt $\mu$ bằng bao nhiêu?", 0.25, "", 0.005,
       loi=r"Quên đổi khối lượng thành áp lực (chia lực kéo cho khối lượng thay vì cho $mg$), hoặc quên rằng trượt đều thì ma sát bằng lực kéo."),
  buoc("Gia tốc khi kéo lực lớn hơn", r"Gia tốc của thùng khi kéo bằng lực ngang ở câu b bằng bao nhiêu (đơn vị m/s²)?", 1.3, "m/s²", 0.03,
       loi=r"Cho rằng ma sát tăng theo lực kéo, hoặc bỏ ma sát khi tính gia tốc.",
       ke=[(r"Định luật II Newton với ma sát trượt không đổi: $a=\dfrac{F-F_{\text{mst}}}{m}$", True),
           (r"Lấy ma sát tăng theo lực kéo, bằng chính lực kéo mới", r"Khi đã trượt, ma sát trượt chỉ phụ thuộc $\mu$ và $N$, không đổi theo lực kéo; nếu ma sát bằng lực kéo thì thùng không thể nhanh dần."),
           (r"$a=\dfrac{F}{m}$", r"Bỏ ma sát thì hợp lực quá lớn; ma sát vẫn tác dụng và ngược chiều chuyển động.")]),
  buoc("Vận tốc lúc buông dây", r"Vận tốc của thùng lúc buông dây bằng bao nhiêu (đơn vị m/s)?", 5.2, "m/s", 0.1,
       loi=r"Dùng công thức quãng đường thay công thức vận tốc, hoặc dùng gia tốc không có ma sát.",
       ke=[(r"Nhanh dần đều từ trạng thái nghỉ: $v=at$ với $a$ vừa tìm", True),
           (r"$v=\dfrac{Ft}{m}$ với $F$ là lực kéo", r"Công thức này bỏ ma sát; gia tốc đúng là gia tốc đã tính ở bước trước."),
           (r"$v=\tfrac12at^2$", r"Đó là công thức quãng đường, không phải vận tốc.")]),
  buoc("Gia tốc sau khi buông dây", r"Chọn chiều chuyển động làm chiều dương: gia tốc của thùng sau khi buông dây bằng bao nhiêu (đơn vị m/s²)?", -2.45, "m/s²", 0.05,
       loi=r"Dùng lại gia tốc của giai đoạn kéo, hoặc cho rằng hết lực kéo thì không còn lực nào.",
       ke=[(r"Viết định luật II Newton cho giai đoạn sau khi buông, liệt kê các lực theo phương ngang", True),
           (r"Giữ nguyên gia tốc của giai đoạn kéo, vì ma sát không đổi", r"Lực kéo đã mất, hợp lực chỉ còn ma sát ngược chiều chuyển động nên hợp lực khác trước; phải viết lại định luật II Newton cho giai đoạn mới."),
           (r"Cho gia tốc bằng $0$, vì không còn lực kéo", r"Hết lực kéo không có nghĩa hết lực: ma sát trượt vẫn tác dụng nên thùng chậm dần chứ không chuyển động đều.")]),
  buoc("Quãng đường trượt thêm", r"Thùng còn trượt thêm bao xa thì dừng (đơn vị m)?", 5.52, "m", 0.05,
       loi=r"Dùng thời gian $4{,}0\ \text{s}$ của giai đoạn kéo cho giai đoạn trượt chậm dần, hoặc lấy gia tốc của giai đoạn kéo.",
       ke=[(r"Công thức không có thời gian: $0-v^2=2a's$ với $a'$ vừa tìm", True),
           (r"$s=vt$ với $t=4{,}0\ \text{s}$", r"$4{,}0\ \text{s}$ là thời gian lúc kéo; sau khi buông thùng chậm dần, không chuyển động đều."),
           (r"$s=\tfrac12at^2$ với gia tốc lúc kéo", r"Giai đoạn này gia tốc khác và vận tốc đầu không bằng $0$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực kéo chếch một góc</b> → nghĩ tới <b>áp lực có còn bằng trọng lượng không</b>.",
  cap_do=3, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Áp lực của thùng lên sàn", r"Áp lực của thùng lên sàn bằng bao nhiêu (đơn vị N)?", 43.8, "N", 0.2,
       loi=r"Dùng sai áp lực (lấy $N=mg$ như mặt ngang, hoặc tách sai lực kéo)."),
  buoc("Lực ma sát trượt", r"Lực ma sát trượt tác dụng lên thùng bằng bao nhiêu (đơn vị N)?", 13.1, "N", 0.1,
       loi=r"Nhân $\mu$ với $mg$ thay vì với áp lực vừa tìm, hoặc lấy thành phần nằm ngang của lực kéo làm ma sát.",
       ke=[(r"Lấy áp lực vừa tìm nhân với hệ số ma sát", True),
           (r"$F_{\text{mst}}=\mu mg$", r"Lực kéo chếch lên nhấc bớt thùng nên áp lực nhỏ hơn $mg$; dùng $mg$ thì ma sát bị tính thừa."),
           (r"$F_{\text{mst}}=F\cos\alpha$", r"$F\cos\alpha$ là thành phần nằm ngang của lực kéo, là ngoại lực; ma sát trượt phải tính bằng $\mu N$.")]),
  buoc("Gia tốc", r"Gia tốc của thùng bằng bao nhiêu (đơn vị m/s²)?", 2.14, "m/s²", 0.03,
       loi=r"Dùng cả lực $F$ thay vì thành phần nằm ngang, hoặc nhầm $\sin$ với $\cos$.",
       ke=[(r"Xét các lực theo phương ngang rồi áp dụng định luật II Newton", True),
           (r"Dùng cả lực kéo $F$ mà không tách thành phần, vì thùng chuyển động theo hướng sợi dây", r"Thùng chuyển động theo phương ngang; chỉ thành phần nằm ngang của lực kéo kéo thùng đi, phần còn lại nhấc bớt thùng."),
           (r"Coi thùng cân bằng nên hợp lực bằng $0$", r"Thùng trượt nhanh dần nên hợp lực theo phương ngang khác $0$; chỉ theo phương thẳng đứng thùng mới cân bằng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật trượt trên mặt nghiêng có ma sát</b> → nghĩ tới <b>áp lực và lực dọc mặt nghiêng</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Áp lực lên ván", r"Áp lực của bao hàng lên ván bằng bao nhiêu (đơn vị N)?", 96.3, "N", 0.3,
       loi=r"Lấy $N=mg$ như mặt ngang, hoặc nhầm $\sin$ với $\cos$ khi tách trọng lực."),
  buoc("Lực ma sát trượt", r"Lực ma sát trượt tác dụng lên bao hàng bằng bao nhiêu (đơn vị N)?", 28.9, "N", 0.2,
       loi=r"Nhân $\mu$ với $mg$ thay vì với áp lực vừa tìm.",
       ke=[(r"Lấy áp lực ở bước trước nhân với hệ số ma sát", True),
           (r"$F_{\text{mst}}=\mu mg$", r"Trên mặt nghiêng áp lực chỉ bằng thành phần $mg\cos\alpha$, nhỏ hơn $mg$."),
           (r"$F_{\text{mst}}=\mu mg\sin\alpha$", r"$mg\sin\alpha$ là thành phần dọc ván kéo bao hàng xuống, không phải áp lực.")]),
  buoc("Gia tốc", r"Gia tốc của bao hàng bằng bao nhiêu (đơn vị m/s²)?", 3.21, "m/s²", 0.03,
       loi=r"Cộng ma sát với thành phần trọng lực dọc dốc, hoặc lấy cả $mg$ thay vì $mg\sin\alpha$.",
       ke=[(r"Xét các lực dọc theo ván rồi áp dụng định luật II Newton", True),
           (r"Xét các lực theo phương vuông góc ván, vì bao hàng ép vào ván", r"Vuông góc ván bao hàng không chuyển động; gia tốc nằm dọc ván nên phải xét các lực theo phương đó."),
           (r"Coi bao hàng cân bằng nên hợp lực bằng $0$", r"Bao hàng trượt nhanh dần nên hợp lực dọc ván khác $0$.")]),
  buoc("Tốc độ ở chân ván", r"Tốc độ của bao hàng khi tới chân ván bằng bao nhiêu (đơn vị m/s)?", 5.67, "m/s", 0.05,
       loi=r"Bỏ ma sát khi tính tốc độ, hoặc thế quãng đường vào chỗ của thời gian.",
       ke=[(r"Công thức không có thời gian: $v^2=2aL$ vì $v_0=0$", True),
           (r"$v=\sqrt{2gL\sin\alpha}$, như khi không có ma sát", r"Có ma sát nên gia tốc nhỏ hơn $g\sin\alpha$; công thức này cho tốc độ quá lớn."),
           (r"$v=at$ với $t=L$", r"$L$ là quãng đường, không phải thời gian; công thức $v=at$ cần thời gian.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật lên dốc rồi dừng</b> → hỏi <b>vật dừng rồi thì sao?</b>; lên và xuống khác gia tốc.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Gia tốc lúc đi lên", r"Độ lớn gia tốc của vật lúc đi lên dốc bằng bao nhiêu (đơn vị m/s²)?", 5.92, "m/s²", 0.05,
       loi=r"Tính thiếu hoặc sai một trong các lực cản dọc dốc."),
  buoc("Quãng đường đi lên", r"Vật đi lên được bao xa theo mặt dốc (đơn vị m)?", 3.04, "m", 0.03,
       loi=r"Dùng $g$ thay cho gia tốc dọc dốc có ma sát, hoặc quên dấu của gia tốc khi chậm dần.",
       ke=[(r"Dừng ở điểm cao nhất nên $0-v_0^2=2as$ với gia tốc lúc đi lên", True),
           (r"$s=\dfrac{v_0^2}{2g}$, như ném thẳng đứng", r"Đó là độ cao của vật ném thẳng đứng; ở đây vật chuyển động dọc dốc có ma sát nên gia tốc khác $g$."),
           (r"$s=v_0t$ với $t$ chưa biết", r"Vận tốc giảm dần chứ không đều nên $s\ne v_0t$, và đề chưa cho thời gian.")]),
  buoc("Nằm yên hay trượt xuống", r"Tới điểm cao nhất, vật nằm yên lại hay trượt xuống?",
       loi=r"Cho rằng vật đã dừng thì nằm yên luôn, hoặc cho rằng vật luôn quay lại mà không kiểm ma sát nghỉ cực đại.",
       lua_chon=[(r"Trượt xuống, vì thành phần trọng lực dọc dốc lớn hơn ma sát nghỉ cực đại", True),
                 (r"Nằm yên, vì vật đã dừng lại thì ma sát nghỉ giữ được", r"Vật dừng tức thời chưa có nghĩa nằm yên: phải xem ma sát nghỉ cực đại có giữ nổi $mg\sin\alpha$ không."),
                 (r"Trượt xuống, vì vật luôn quay lại điểm xuất phát", r"Không phải lúc nào cũng vậy: nếu $\mu\ge\tan\alpha$ vật nằm lại trên dốc. Phải so $mg\sin\alpha$ với $F_{\text{msn max}}$.")],
       ke=[(r"So $mg\sin\alpha$ với ma sát nghỉ cực đại $\mu mg\cos\alpha$", True),
           (r"Coi như vật trượt xuống và tính ngay gia tốc", r"Chưa kiểm điều kiện đã cho là trượt; nếu ma sát nghỉ giữ được thì vật nằm yên và $a=0$."),
           (r"Kết luận từ việc vật đã dừng lại tức thời", r"Dừng tức thời ở điểm cao nhất chưa nói gì về việc ma sát nghỉ có giữ nổi vật hay không.")]),
  buoc("Gia tốc lúc trượt xuống", r"Độ lớn gia tốc của vật lúc trượt xuống bằng bao nhiêu (đơn vị m/s²)?", 2.37, "m/s²", 0.03,
       loi=r"Giữ ma sát hướng xuống dốc như lúc đi lên, hoặc bỏ qua ma sát.",
       ke=[(r"Viết lại định luật II Newton cho chiều chuyển động mới, xét lại chiều của ma sát", True),
           (r"Giữ ma sát hướng xuống dốc: $a=g(\sin\alpha+\mu\cos\alpha)$", r"Vật đổi chiều chuyển động nên ma sát cũng đổi chiều, hướng lên dốc; cộng là kết quả của lúc đi lên."),
           (r"Bỏ ma sát: $a=g\sin\alpha$", r"Vật vẫn trượt trên mặt có ma sát nên phải trừ ma sát trượt.")]),
  buoc("Tốc độ khi về chân dốc", r"Tốc độ của vật khi về tới chân dốc bằng bao nhiêu (đơn vị m/s)?", 3.79, "m/s", 0.05,
       loi=r"Cho rằng vật về chân dốc với đúng tốc độ lúc ném, hoặc dùng gia tốc của lúc đi lên.",
       ke=[(r"$v^2=2a's$ với $a'$ của lúc trượt xuống và $s$ là quãng đường đã đi lên", True),
           (r"$v=v_0$, vì cơ năng bảo toàn", r"Có ma sát thực hiện công cản trên cả đường đi và về nên cơ năng giảm; vật về chân dốc chậm hơn lúc ném."),
           (r"$v^2=2as$ với gia tốc của lúc đi lên", r"Lúc trượt xuống ma sát đổi chiều nên gia tốc khác; dùng gia tốc lúc lên chỉ cho lại đúng tốc độ lúc ném.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN: ví dụ cũ đã tính lại ═════════════
OLD = json.load(open(os.path.join(HERE, "old/63.json")))["questions"]
# VD1, 2, 3 (chỉ số 0, 1, 2) bỏ: sai số/đề mơ hồ. Còn lại: VD8 (7), VD6 (5), VD5 (4), VD4 (3), VD7 (6)
ORDER = [4]
MUC = {4: "Trung bình"}
assert abs(2500 * (2 + 0.5) - 6250) < 1e-9 and abs(1000 * 2 + 0.05 * 1000 * 10 - 2500) < 1e-9 and abs(20 ** 2 / (2 * 0.5) - 400) < 1e-9   # VD5
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)
body = TU_LUAN["body_html"]
TU_LUAN["body_html"] = body

# ═════════════ GHI FILE ═════════════
BUILD = [d1, d2, d3, d4, d5]
write(J, 63, "Bài 18. Lực ma sát", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
raw = json.dumps(d, ensure_ascii=False, indent=1)
def _walk(x):
    if isinstance(x, str): yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from _walk(v)
    elif isinstance(x, list):
        for v in x: yield from _walk(v)
for _s in _walk(d):
    assert not re.search(r"[\x00-\x1f]", _s), "còn ký tự điều khiển/TAB: " + repr(_s[:60])
    assert '\\"' not in _s, "còn dấu gạch chéo trước nháy: " + _s[:60]
open(J, "w").write(raw)
print("xong", J, "marker-end:", raw.count("marker-end"))
