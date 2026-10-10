"""Bài 70 — "Bài 25. Động năng, thế năng" (Vật lí 10, chương 4). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-58.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-70.py  → ghi scripts/data/bai-tap-mau/70.json
Dạng theo quét: scripts/logs/batch-ra-soat/ket-qua/70.quet-dang.json (5 dạng, cấp 1,1,2,2,3). Hình: hinh_70.py.
Ví dụ cũ (old/70.json: 4 khối, nhiều "Câu" mỗi khối) — ý tưởng dạng 1, 3, 4, 5 lấy từ các câu cùng loại nhưng ĐỀ viết lại với số mới
(tránh trùng quiz/bài toán mẫu trong lý thuyết: ô tô 1000 kg 72 km/h, trượt băng 50 kg, sách trên giá, tàu lượn 400 kg, thùng 40 kg kéo 300 N).
Vào tu_luan (giữ nguyên lời giải gốc, 18 câu): khối 0 → Câu 2, 7, 11, 12; khối 1 → Câu 1, 2, 4, 5, 6, 7, 10, 12; khối 2 → Câu 1, 2, 10, 12, 14; khối 3 → Câu 5, 11.
BỎ (có lý do):
 • khối 0 Câu 8 — làm tròn sớm: v ≈ 8,5 rồi ×3 cho 224336 J, đúng là 9·25000 = 225000 J;
 • khối 1 Câu 8 — F = 4000 N sai (đúng 12000 N), quãng dừng 200 m sai (đúng ≈ 66,7 m);
 • khối 1 Câu 9 — công suất 2083 W sai (đúng 4·10⁷/120 ≈ 3,3·10⁵ W) và 160 m trong 2 phút mâu thuẫn với lực hãm không đổi; công suất không thuộc bài này;
 • khối 2 Câu 3 — gọi "độ biến thiên thế năng" nhưng tính công của trọng lực (sai dấu nhãn);
 • khối 2 Câu 9 và khối 3 Câu 7 — dùng bảo toàn cơ năng, bài này không dạy;
 • khối 0 Câu 13, khối 2 Câu 13 — kèm hình/đồ thị gốc không kiểm được; khối 1 Câu 13 (công suất thang máy) và Câu 14 (nhiều ý, phần c cắt dở) — ngoài phạm vi / không kiểm trọn được;
 • trùng đề đã có: khối 1 Câu 3 (= Câu 1), Câu 11 (= Câu 4), khối 2 Câu 6 (= Câu 4), khối 3 Câu 8 (= Câu 5); còn lại cùng loại dạng 1 (khối 0 Câu 1, 3, 4, 5, 6, 9, 10) không đưa vào cho gọn."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_70 import BUILD

J = os.path.join(HERE, "70.json")
OLD = json.load(open(os.path.join(HERE, "old/70.json")))["questions"]
T136, T137 = "Động năng và định lí động năng", "Thế năng trọng trường và mốc thế năng"

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
cosd = lambda a: math.cos(math.radians(a)); sind = lambda a: math.sin(math.radians(a))
g = 10.0
# D1: xe tải 4000 kg, 36 → 90 km/h; ô tô con 1000 kg cùng động năng
m, v1, v2, mc = 4000.0, 36 / 3.6, 90 / 3.6, 1000.0
ok("D1 v1", v1, 10, 1e-12); ok("D1 v2", v2, 25, 1e-12)
W1 = 0.5 * m * v1**2; ok("D1 W1", W1, 200000, 1e-6); ok("D1 W2", 0.5 * m * v2**2, 1250000, 1e-6)
vc = math.sqrt(2 * W1 / mc); ok("D1 vc", vc, 20, 1e-9); ok("D1 vc km/h", vc * 3.6, 72, 1e-9)
ok("D1 tỉ số", 0.5 * m * v2**2 / W1, 6.25, 1e-12); ok("D1 tỉ số v²", (v2 / v1) ** 2, 6.25, 1e-12)
# các cách sai khác đáp án đúng
for bad in (0.5 * m * 36**2 / 1000, m * v1**2 / 1000, 0.5 * m * v1 / 1000, 0.5 * m * v1**2 * 3.6 / 1000):
    assert abs(bad - 200) > 5, bad
assert abs(2.5 - 6.25) > 1 and abs((v2 - v1) ** 2 / v1**2 - 6.25) > 1 and abs(v1 - vc) > 5 and abs(m * v1 / mc - vc) > 5
# D2: mốc nền kho
mA, zA, mB, zB, mC, WC = 12.0, 1.5, 5.0, 3.6, 8.0, 240.0
WA, WB = mA * g * zA, mB * g * zB
ok("D2 WA", WA, 180, 1e-9); ok("D2 WB", WB, 180, 1e-9); assert abs(WA - WB) < 1e-9
zC = WC / (mC * g); ok("D2 zC", zC, 3.0, 1e-12)
assert abs(WC / mC - zC) > 10 and abs(WC * mC * g - zC) > 10 and abs(WC / (mC * g) - WC / mC) > 10
assert zB > zA and mA > mB                                     # hai cách so sánh sai cho kết luận khác
# D3: chậu 2,0 kg ở +6,0 m; mốc đường (0), hầm (−4,0), tầng 6 (+15)
m3 = 2.0
Wd, Wh, Wt6 = m3 * g * (6.0 - 0), m3 * g * (6.0 - (-4.0)), m3 * g * (6.0 - 15.0)
ok("D3 mốc đường", Wd, 120, 1e-9); ok("D3 mốc hầm", Wh, 200, 1e-9); ok("D3 mốc tầng 6", Wt6, -180, 1e-9)
ok("D3 hiệu hầm−đường", Wh - Wd, m3 * g * 4.0, 1e-9); ok("D3 hiệu đường−tầng6", Wd - Wt6, m3 * g * 15.0, 1e-9)
assert abs(m3 * g * (6.0 - 4.0) - Wh) > 50 and abs(m3 * g * 6.0 - Wh) > 50 and abs(m3 * g * 9.0 - Wt6) > 50 and Wt6 < 0
# D4: 60 kg; A 40 m, B 12 m, C 25 m
m4, ZA_, ZB_, ZC_ = 60.0, 40.0, 12.0, 25.0
AAB, ABC, AAC = m4 * g * (ZA_ - ZB_), m4 * g * (ZB_ - ZC_), m4 * g * (ZA_ - ZC_)
ok("D4 AB", AAB / 1000, 16.8, 1e-9); ok("D4 BC", ABC / 1000, -7.8, 1e-9); ok("D4 AC", AAC / 1000, 9.0, 1e-9); ok("D4 cộng", AAB + ABC, AAC, 1e-9)
ok("D4 mốc B", m4 * g * (ZA_ - ZB_) / 1000 - m4 * g * (ZC_ - ZB_) / 1000, 9.0, 1e-9)
assert abs(abs(AAB) + abs(ABC) - AAC) > 5000 and abs(-AAB - ABC) > 5000                 # bỏ dấu / đảo hiệu cho kết quả khác
# D5: 20 kg, dốc 10 m nghiêng 30°, F = 150 N, f = 25 N, bắt đầu nghỉ
m5, s5, al, F5, f5 = 20.0, 10.0, 30, 150.0, 25.0
h5 = s5 * sind(al); ok("D5 h", h5, 5.0, 1e-12)
AF, Af, AP = F5 * s5, -f5 * s5, -m5 * g * h5
ok("D5 AF", AF, 1500, 1e-9); ok("D5 Af", Af, -250, 1e-9); ok("D5 AP", AP, -1000, 1e-9); ok("D5 Σ", AF + Af + AP, 250, 1e-9)
v5 = math.sqrt(2 * (AF + Af + AP) / m5); ok("D5 v", v5, 5.0, 1e-12)
v0b = 2.0
Fb = (f5 * s5 + m5 * g * h5 - 0.5 * m5 * v0b**2) / s5; ok("D5 F dừng", Fb, 121, 1e-12)
ab = (Fb - f5 - m5 * g * sind(al)) / m5; ok("D5 b a", ab, -0.2, 1e-12); ok("D5 b v²", v0b**2 + 2 * ab * s5, 0, 1e-9)
assert abs((f5 * s5 + m5 * g * h5) / s5 - Fb) > 3 and abs(f5 + m5 * g * h5 / s5 * 0 - Fb) > 50
a5 = (F5 - f5 - m5 * g * sind(al)) / m5; ok("D5 a", a5, 1.25, 1e-12); ok("D5 t", math.sqrt(2 * s5 / a5), 4.0, 1e-12); ok("D5 v=at", a5 * 4.0, v5, 1e-12)
assert abs(math.sqrt(2 * (AF + Af) / m5) - v5) > 1 and abs(math.sqrt(2 * AF / m5) - v5) > 1 and abs(f5 - Fb) > 50 and abs(m5 * g * sind(al) - Fb) > 20
assert abs(AF + Af - m5 * g * s5 - (AF + Af + AP)) > 100                             # dùng mg·chiều dài dốc cho kết quả khác
# Tự luận cũ (đối chiếu số hiển thị trong lời giải gốc)
ok("TL0.2 v", math.sqrt(2 * 10 / 0.2), 10, 1e-9); ok("TL0.7", 0.5 * 1500 * 10**2, 75000, 1e-9)
ok("TL1.1", 0.5 * 0.5 * (10**2 - 5**2), 18.75, 1e-9); ok("TL1.5", 1500 * 15**2 / (2 * 50), 3375, 1e-9)
ok("TL1.6c", (0.5 * 1500 * 10**2 - 0.5 * 1500 * 5**2) / 100, 562.5, 1e-9)
ok("TL1.2", (0.5 * 0.1 * 300**2 - 0.5 * 0.1 * 100**2) / 0.05, 80000, 1e-6)
ok("TL1.10b", (0.5 * 2000 * (20**2 - 2**2)) / (2000 * 10 * 0.5), 39.6, 1e-9); ok("TL1.10c", 0.5 * 2000 * 20**2 / (2000 * 10 * 200), 0.1, 1e-12)
ok("TL1.12", math.sqrt(2 * (0.5 * 0.05 * 200**2 - 25000 * 0.02) / 0.05), 141.4, 0.05)
ok("TL1.7", math.degrees(math.acos(50 / (45 * 1.5))), 42.0, 0.3); ok("TL1.7m", 2 * 50 / 2.6**2, 14.8, 0.05)
ok("TL2.14", 800 * 9.8 * (10 - 550), -4233600, 1e-6)
ok("TL3.5", math.sqrt(2 * 0.1 * 10 * 4 / 0.1), 4 * math.sqrt(5), 1e-9); ok("TL3.11", 1 * 10 * 4 - 12, 28, 1e-9)
ok("TL0.12", 1.5 * math.sqrt(3), 2.6, 0.05)


# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Tính động năng và so sánh động năng", topic=T136,
      problem_html=r"""<p>Một xe tải khối lượng $4{,}0$ tấn chạy trên đường thẳng với tốc độ $36\ \text{km/h}$.</p>
<ol type="a"><li>Tính động năng của xe tải (đơn vị kJ).</li>
<li>Một ô tô con khối lượng $1{,}0$ tấn có động năng đúng bằng động năng của xe tải. Tính tốc độ của ô tô con theo m/s.</li>
<li>Sau đó xe tải tăng tốc đến $90\ \text{km/h}$. Động năng của xe tải khi đó gấp mấy lần lúc đầu?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Thế năng trọng trường khi mốc ở mặt đất", topic=T137,
      problem_html=r"""<p>Trong một kho hàng, thùng $A$ khối lượng $12\ \text{kg}$ đặt trên giá ở độ cao $1{,}5\ \text{m}$, thùng $B$ khối lượng $5{,}0\ \text{kg}$ đặt trên giá ở độ cao $3{,}6\ \text{m}$ (cùng so với nền kho). Chọn mốc thế năng tại nền kho, lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính thế năng trọng trường của mỗi thùng.</li>
<li>So sánh thế năng của hai thùng.</li>
<li>Thùng $C$ khối lượng $8{,}0\ \text{kg}$ có thế năng $240\ \text{J}$ (cùng mốc ở nền kho). Tính độ cao của thùng $C$.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đổi mốc thế năng và xét dấu thế năng", topic=T137,
      problem_html=r"""<p>Một toà nhà có tầng hầm với sàn nằm sâu $4{,}0\ \text{m}$ dưới mặt đường. Sàn tầng 3 cao $6{,}0\ \text{m}$ và sàn tầng 6 cao $15\ \text{m}$ so với mặt đường. Một chậu cây khối lượng $2{,}0\ \text{kg}$ đặt trên sàn tầng 3. Lấy $g=10\ \text{m/s}^2$.</p>
<p>Tính thế năng trọng trường của chậu cây khi chọn mốc thế năng tại:</p>
<ol type="a"><li>mặt đường;</li><li>sàn tầng hầm;</li><li>sàn tầng 6.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Công của trọng lực và độ biến thiên thế năng", topic=T137,
      problem_html=r"""<p>Một người đi xe đạp (tổng khối lượng $60\ \text{kg}$) đi trên đường đồi: từ đỉnh dốc $A$ cao $40\ \text{m}$ xuống chân dốc $B$ cao $12\ \text{m}$, rồi lên đồi $C$ cao $25\ \text{m}$ (các độ cao đều tính từ cùng một mức chuẩn). Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính công của trọng lực khi người đi từ $A$ đến $B$.</li>
<li>Tính công của trọng lực khi người đi từ $B$ đến $C$.</li>
<li>Tính công của trọng lực trên cả đoạn từ $A$ đến $C$. Công này có phụ thuộc vào việc đường đi quanh co thế nào không?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Định lí động năng với nhiều ngoại lực", topic=T136,
      problem_html=r"""<p>Một người kéo thùng hàng khối lượng $20\ \text{kg}$ từ chân dốc lên đỉnh dốc bằng sợi dây song song với mặt dốc. Dốc dài $10\ \text{m}$, nghiêng góc $30^\circ$ so với phương ngang. Thùng bắt đầu chuyển động từ trạng thái nghỉ ở chân dốc. Lực kéo có độ lớn không đổi $150\ \text{N}$, lực ma sát giữa thùng và mặt dốc là $25\ \text{N}$. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính tốc độ của thùng khi tới đỉnh dốc.</li>
<li>Lần khác, thùng được đẩy cho tốc độ đầu $2{,}0\ \text{m/s}$ ở chân dốc, lực ma sát vẫn là $25\ \text{N}$. Lực kéo không đổi phải có độ lớn bao nhiêu để thùng vừa tới đỉnh dốc thì dừng lại?</li></ol>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“xe tải khối lượng $4{,}0$ tấn … tốc độ $36\ \text{km/h}$”", r"$m=4{,}0$ tấn; $v_1=36\ \text{km/h}$", r"⚠ Đổi sang kg và m/s trước khi thay vào công thức động năng"),
  (r"“a) Tính động năng của xe tải”", r"Cần $W_\text{d1}$ (kJ)", r"Đại lượng cần tìm"),
  (r"“ô tô con khối lượng $1{,}0$ tấn có động năng đúng bằng động năng của xe tải”", r"$m'=1{,}0$ tấn; $W_\text{d}'=W_\text{d1}$", r"Hai động năng bằng nhau: viết phương trình cho ô tô con"),
  (r"“b) tốc độ của ô tô con theo m/s”", r"Cần $v'$ (m/s)", r"Đại lượng cần tìm"),
  (r"“c) tăng tốc đến $90\ \text{km/h}$”", r"$v_2=90\ \text{km/h}$; khối lượng không đổi", r"⚠ Cùng một vật nên chỉ so sánh được qua tốc độ; hai tốc độ cùng đơn vị"),
  (r"“gấp mấy lần lúc đầu”", r"Cần $W_\text{d2}/W_\text{d1}$", r"Đại lượng cần tìm")],
 [(r"“thùng $A$ khối lượng $12$ kg … độ cao $1{,}5$ m”", r"$m_A=12\ \text{kg}$; $z_A=1{,}5\ \text{m}$", r"⚠ Mỗi thùng có khối lượng và độ cao riêng"),
  (r"“thùng $B$ khối lượng $5{,}0$ kg … độ cao $3{,}6$ m”", r"$m_B=5{,}0\ \text{kg}$; $z_B=3{,}6\ \text{m}$", r"Thế năng trọng trường $W_\text{t}=mgz$"),
  (r"“Chọn mốc thế năng tại nền kho”", r"Mốc ở nền kho", r"⚠ Mốc ở nền kho thì $z$ bằng độ cao so với nền"),
  (r"“lấy $g=10$”", r"$g=10\ \text{m/s}^2$", r"Gia tốc trọng trường"),
  (r"“a) thế năng trọng trường của mỗi thùng”", r"Cần $W_\text{tA}$, $W_\text{tB}$ (J)", r"Đại lượng cần tìm"),
  (r"“b) So sánh thế năng của hai thùng”", r"So hai kết quả ở câu a", r"Thế năng phụ thuộc cả khối lượng lẫn độ cao"),
  (r"“c) thùng $C$ khối lượng $8{,}0$ kg có thế năng $240$ J”", r"$m_C=8{,}0\ \text{kg}$; $W_\text{tC}=240\ \text{J}$", r"Rút $z$ từ công thức thế năng (mốc vẫn ở nền kho)"),
  (r"“độ cao của thùng $C$”", r"Cần $z_C$ (m)", r"Đại lượng cần tìm")],
 [(r"“sàn nằm sâu $4{,}0$ m dưới mặt đường”", r"Sàn hầm: $z=-4{,}0\ \text{m}$ so với mặt đường", r"⚠ $z$ là toạ độ có dấu, tính từ mốc theo trục hướng lên"),
  (r"“sàn tầng 3 cao $6{,}0$ m và sàn tầng 6 cao $15$ m so với mặt đường”", r"Tầng 3: $6{,}0\ \text{m}$; tầng 6: $15\ \text{m}$ (so với mặt đường)", r"Độ cao cho sẵn so với mặt đường, không phải so với mốc"),
  (r"“chậu cây khối lượng $2{,}0$ kg đặt trên sàn tầng 3”", r"$m=2{,}0\ \text{kg}$; chậu đứng yên ở độ cao $6{,}0\ \text{m}$ so với mặt đường", r"Vị trí của vật không đổi, chỉ đổi mốc"),
  (r"“Lấy $g=10$”", r"$g=10\ \text{m/s}^2$", r"Thế năng trọng trường $W_\text{t}=mgz$"),
  (r"“a) mặt đường”", r"Mốc ở độ cao $0$", r"Tính $z$ của chậu so với mốc này"),
  (r"“b) sàn tầng hầm”", r"Mốc ở $-4{,}0\ \text{m}$ so với mặt đường", r"⚠ Mốc đổi thì $z$ phải tính lại từ mốc mới"),
  (r"“c) sàn tầng 6”", r"Mốc ở $15\ \text{m}$ so với mặt đường", r"⚠ Xét chậu nằm phía nào của mốc để xác định dấu của $z$"),
  (r"“Tính thế năng trọng trường của chậu cây”", r"Cần $W_\text{t}$ (J) ứng với từng mốc", r"Đại lượng cần tìm")],
 [(r"“người đi xe đạp (tổng khối lượng $60$ kg)”", r"$m=60\ \text{kg}$", r"Trọng lực $P=mg$"),
  (r"“đỉnh dốc $A$ cao $40$ m … chân dốc $B$ cao $12$ m … đồi $C$ cao $25$ m”", r"$z_A=40\ \text{m}$; $z_B=12\ \text{m}$; $z_C=25\ \text{m}$", r"⚠ Các độ cao tính từ cùng một mức chuẩn"),
  (r"“Lấy $g=10$”", r"$g=10\ \text{m/s}^2$", r"Gia tốc trọng trường"),
  (r"“a) công của trọng lực khi đi từ $A$ đến $B$”", r"Cần $A_{AB}$ (kJ)", r"Định lí thế năng: công của lực thế bằng hiệu thế năng"),
  (r"“b) từ $B$ đến $C$”", r"Cần $A_{BC}$ (kJ)", r"Cùng công thức cho mọi đoạn đường"),
  (r"“c) cả đoạn từ $A$ đến $C$ … có phụ thuộc vào đường đi quanh co không”", r"Cần $A_{AC}$ (kJ) và kết luận về đường đi", r"⚠ Trọng lực là lực thế: công chỉ phụ thuộc vị trí đầu và cuối")],
 [(r"“thùng hàng khối lượng $20$ kg … sợi dây song song với mặt dốc”", r"$m=20\ \text{kg}$; lực kéo cùng phương, cùng chiều chuyển động", r"Công của lực không đổi: $A=Fs\cos\varphi$"),
  (r"“Dốc dài $10$ m, nghiêng góc $30^\circ$ so với phương ngang”", r"$s=10\ \text{m}$; $\alpha=30^\circ$", r"Liên hệ chiều dài dốc, góc nghiêng và độ cao đỉnh dốc"),
  (r"“bắt đầu chuyển động từ trạng thái nghỉ” (câu a)", r"$v_0=0$, động năng đầu bằng $0$", r"Động năng $\tfrac12mv^2$"),
  (r"“Lực kéo … không đổi $150$ N, lực ma sát … $25$ N”", r"$F=150\ \text{N}$; $F_\text{ms}=25\ \text{N}$", r"⚠ Cộng công của mọi ngoại lực, kể cả công âm; phản lực vuông góc đường đi có công bằng $0$"),
  (r"“Lấy $g=10$”", r"$g=10\ \text{m/s}^2$", r"Trọng lực cũng là ngoại lực"),
  (r"“a) tốc độ của thùng khi tới đỉnh dốc”", r"Cần $v$ (m/s)", r"Định lí động năng: tổng công = độ biến thiên động năng"),
  (r"“b) tốc độ đầu $2{,}0$ m/s … vừa tới đỉnh dốc thì dừng lại”", r"$v_0=2{,}0\ \text{m/s}$; $v=0$ ở đỉnh; cần $F'$ (N)", r"Độ biến thiên động năng giữa lúc đầu và lúc dừng")],
]

# ═════════════ Lời giải từng bước ═════════════
R_DN = [r"<strong>Khái niệm:</strong> động năng là năng lượng vật có do đang chuyển động.",
        r"$W_\text{d}=\dfrac12mv^2$ ($m$: kg; $v$: m/s; $W_\text{d}$: J).",
        r"Động năng không âm và tỉ lệ với bình phương tốc độ.",
        r"⚠ <strong>Điều kiện:</strong> đổi tấn ra kg, km/h ra m/s ($1\ \text{m/s}=3{,}6\ \text{km/h}$) trước khi thay số."]
R_TN = [r"<strong>Khái niệm:</strong> thế năng trọng trường là năng lượng tương tác giữa Trái Đất và vật, phụ thuộc vị trí của vật.",
        r"$W_\text{t}=mgz$ ($z$: toạ độ trên trục thẳng đứng hướng lên, gốc tại mốc).",
        r"Mốc ở mặt đất thì $z=h$, độ cao so với mặt đất.",
        r"⚠ <strong>Điều kiện:</strong> phải chọn mốc trước; vùng khảo sát nhỏ để $g$ không đổi."]
R_DM = [r"<strong>Khái niệm:</strong> mốc thế năng là vị trí chọn để $W_\text{t}=0$.",
        r"$W_\text{t}=mgz$ với $z$ tính từ mốc, trục hướng lên.",
        r"Trên mốc: $z\gt0$, $W_\text{t}\gt0$ · tại mốc: $W_\text{t}=0$ · dưới mốc: $z\lt0$, $W_\text{t}\lt0$.",
        r"⚠ <strong>Điều kiện:</strong> ghi kết quả thế năng thì phải nói rõ mốc; đổi mốc thì tính lại $z$."]
R_CT = [r"<strong>Khái niệm:</strong> trọng lực là lực thế, công của nó chỉ phụ thuộc điểm đầu và điểm cuối.",
        r"$A_{MN}=W_{\text{t}M}-W_{\text{t}N}=mg(z_M-z_N)$ (thế năng đầu trừ thế năng cuối).",
        r"Đi xuống: công dương · đi lên: công âm.",
        r"⚠ <strong>Điều kiện:</strong> không cần biết đường đi; kết quả không phụ thuộc mốc."]
R_DL = [r"<strong>Định lí động năng:</strong> $\dfrac12mv^2-\dfrac12mv_0^2=A_1+A_2+\dots$ (tổng công mọi ngoại lực).",
        r"Công của lực không đổi: $A=Fs\cos\varphi$ ($\varphi$: góc giữa lực và đường đi).",
        r"Công của trọng lực: $-mgh$ khi vật đi lên độ cao $h$.",
        r"⚠ <strong>Điều kiện:</strong> cộng công của MỌI ngoại lực, kể cả công âm; phản lực vuông góc đường đi có công bằng $0$."]

SOLS = [
 sol(R_DN, [
  (r"Đổi tốc độ ra m/s", [P(r"Khối lượng xe tải: $m=4{,}0$ tấn $=4000\ \text{kg}$."), M(r"v_1=\dfrac{36}{3{,}6}"), A(r"v_1=10\ \text{m/s}")]),
  (r"Động năng của xe tải", [M(r"W_\text{d1}=\dfrac12mv_1^2=\dfrac12\cdot4000\cdot10^2"), A(r"W_\text{d1}=200\,000\ \text{J}=200\ \text{kJ}")]),
  (r"Tốc độ của ô tô con", [P(r"Khối lượng ô tô con: $m'=1{,}0$ tấn $=1000\ \text{kg}$. Hai động năng bằng nhau:"), M(r"\dfrac12m'v'^2=W_\text{d1}"),
                            M(r"v'=\sqrt{\dfrac{2W_\text{d1}}{m'}}=\sqrt{\dfrac{2\cdot200\,000}{1000}}=\sqrt{400}"), A(r"v'=20\ \text{m/s}"),
                            P(r"Đổi lại: $20\ \text{m/s}=72\ \text{km/h}$. Khối lượng chỉ bằng một phần tư nên tốc độ phải gấp đôi để cùng động năng.")]),
  (r"Tăng tốc đến $90\ \text{km/h}$", [P(r"Tốc độ mới: $v_2=\dfrac{90}{3{,}6}=25\ \text{m/s}$. Khối lượng không đổi, lập tỉ số:"),
                                       M(r"\dfrac{W_\text{d2}}{W_\text{d1}}=\dfrac{\frac12mv_2^2}{\frac12mv_1^2}=\left(\dfrac{v_2}{v_1}\right)^2"), M(r"\dfrac{W_\text{d2}}{W_\text{d1}}=\left(\dfrac{25}{10}\right)^2"), A(r"\dfrac{W_\text{d2}}{W_\text{d1}}=6{,}25"),
                                       P(r"Tốc độ chỉ gấp $2{,}5$ lần nhưng động năng gấp hơn $6$ lần.")]),
  (r"Kiểm tra", [M(r"W_\text{d2}=\dfrac12\cdot4000\cdot25^2=1\,250\,000\ \text{J}=1250\ \text{kJ}"), M(r"\dfrac{1250}{200}=6{,}25\ \checkmark"),
                 P(r"Động năng tăng khi tốc độ tăng, đơn vị là J ✓.")])],
  [r"a) $W_\text{d}=200\ \text{kJ}$", r"b) $v'=20\ \text{m/s}$ ($72\ \text{km/h}$)", r"c) gấp $6{,}25$ lần"],
  r"Nhận dạng: đề cho <strong>khối lượng và tốc độ (km/h)</strong> hoặc <strong>so sánh động năng</strong> → đổi ra kg, m/s rồi dùng $\tfrac12mv^2$; so sánh thì lập tỉ số."),
 sol(R_TN, [
  (r"Thế năng của thùng $A$", [M(r"W_{\text{t}A}=m_Agz_A=12\cdot10\cdot1{,}5"), A(r"W_{\text{t}A}=180\ \text{J}")]),
  (r"Thế năng của thùng $B$", [M(r"W_{\text{t}B}=m_Bgz_B=5{,}0\cdot10\cdot3{,}6"), A(r"W_{\text{t}B}=180\ \text{J}")]),
  (r"So sánh hai thế năng", [P(r"Hai thế năng <strong>bằng nhau</strong>."),
                             P(r"Thùng $B$ cao gấp $2{,}4$ lần nhưng khối lượng chỉ bằng $\dfrac{5}{12}$ khối lượng thùng $A$; tích $mz$ như nhau."),
                             P(r"Thế năng phụ thuộc cả khối lượng lẫn độ cao, không chỉ một đại lượng.")]),
  (r"Độ cao của thùng $C$", [M(r"W_{\text{t}C}=m_Cgz_C\ \Rightarrow\ z_C=\dfrac{W_{\text{t}C}}{m_Cg}=\dfrac{240}{8{,}0\cdot10}"), A(r"z_C=3{,}0\ \text{m}")]),
  (r"Kiểm tra", [P(r"Đơn vị: $\text{kg}\cdot\text{m/s}^2\cdot\text{m}=\text{J}$ ✓."), P(r"Mốc ở nền kho nên $z_C$ là độ cao của thùng $C$ so với nền kho, nằm giữa hai giá ✓.")])],
  [r"a) $W_{\text{t}A}=180\ \text{J}$ · $W_{\text{t}B}=180\ \text{J}$", r"b) hai thùng có thế năng bằng nhau", r"c) $z_C=3{,}0\ \text{m}$"],
  r"Nhận dạng: đề cho <strong>độ cao so với mốc</strong> và hỏi <strong>thế năng</strong> → $W_\text{t}=mgz$; so sánh phải tính cả khối lượng lẫn độ cao."),
 sol(R_DM, [
  (r"Mốc tại mặt đường", [P(r"Chậu cây nằm trên mốc, $z=6{,}0\ \text{m}$:"), M(r"W_\text{t}=mgz=2{,}0\cdot10\cdot6{,}0"), A(r"W_\text{t}=120\ \text{J}")]),
  (r"Mốc tại sàn tầng hầm", [P(r"Sàn hầm nằm dưới mặt đường $4{,}0\ \text{m}$ nên chậu cây cao hơn sàn hầm một đoạn bằng tổng hai khoảng:"),
                             M(r"z=6{,}0+4{,}0=10\ \text{m}"), M(r"W_\text{t}=2{,}0\cdot10\cdot10"), A(r"W_\text{t}=200\ \text{J}")]),
  (r"Mốc tại sàn tầng 6", [P(r"Chậu cây nằm dưới mốc nên $z$ mang dấu âm:"), M(r"z=6{,}0-15=-9{,}0\ \text{m}"), M(r"W_\text{t}=2{,}0\cdot10\cdot(-9{,}0)"), A(r"W_\text{t}=-180\ \text{J}")]),
  (r"Kiểm tra", [P(r"Chậu cây không di chuyển nhưng thế năng đổi theo mốc, nên kết quả luôn phải ghi kèm mốc."),
                 P(r"Gọi $W_1$, $W_2$, $W_3$ là thế năng ở câu a, b, c. Hai mốc ở câu a và b cách nhau $4{,}0\ \text{m}$; hai mốc ở câu a và c cách nhau $15\ \text{m}$:"),
                 M(r"W_2-W_1=200-120=80\ \text{J}=mg\cdot4{,}0\ \checkmark"),
                 M(r"W_1-W_3=120-(-180)=300\ \text{J}=mg\cdot15\ \checkmark"),
                 P(r"Hiệu hai thế năng bằng $mg$ nhân khoảng cách giữa hai mốc, không phụ thuộc mốc nào được chọn.")])],
  [r"a) mốc mặt đường: $W_\text{t}=120\ \text{J}$", r"b) mốc sàn hầm: $W_\text{t}=200\ \text{J}$", r"c) mốc sàn tầng 6: $W_\text{t}=-180\ \text{J}$"],
  r"Nhận dạng: đề <strong>đổi mốc</strong> hoặc vật <strong>ở dưới mốc</strong> → tính lại $z$ từ mốc mới, chú ý dấu."),
 sol(R_CT, [
  (r"Từ $A$ đến $B$", [M(r"A_{AB}=W_{\text{t}A}-W_{\text{t}B}=mg(z_A-z_B)=60\cdot10\cdot(40-12)"), A(r"A_{AB}=16\,800\ \text{J}=16{,}8\ \text{kJ}"), P(r"Đi xuống nên công dương.")]),
  (r"Từ $B$ đến $C$", [M(r"A_{BC}=mg(z_B-z_C)=60\cdot10\cdot(12-25)"), A(r"A_{BC}=-7800\ \text{J}=-7{,}8\ \text{kJ}"), P(r"Đi lên nên trọng lực cản, công âm.")]),
  (r"Từ $A$ đến $C$", [P(r"Chỉ cần độ cao đầu và độ cao cuối, không cần đường đi qua $B$:"), M(r"A_{AC}=mg(z_A-z_C)=60\cdot10\cdot(40-25)"), A(r"A_{AC}=9000\ \text{J}=9{,}0\ \text{kJ}"),
                       P(r"Công này <strong>không phụ thuộc</strong> đường đi quanh co thế nào.")]),
  (r"Kiểm tra", [M(r"A_{AB}+A_{BC}=16{,}8+(-7{,}8)=9{,}0\ \text{kJ}=A_{AC}\ \checkmark"),
                 P(r"Chọn mốc tại $B$: $W_{\text{t}A}=60\cdot10\cdot28=16{,}8\ \text{kJ}$ và $W_{\text{t}C}=60\cdot10\cdot13=7{,}8\ \text{kJ}$, hiệu vẫn là $9{,}0\ \text{kJ}$: mốc không ảnh hưởng.")])],
  [r"a) $A_{AB}=16{,}8\ \text{kJ}$", r"b) $A_{BC}=-7{,}8\ \text{kJ}$", r"c) $A_{AC}=9{,}0\ \text{kJ}$, không phụ thuộc đường đi"],
  r"Nhận dạng: đề hỏi <strong>công của trọng lực giữa hai vị trí</strong> → thế năng đầu trừ thế năng cuối, bỏ qua đường đi."),
 sol(R_DL, [
  (r"Công của lực kéo", [P(r"Lực kéo song song mặt dốc, cùng chiều chuyển động ($\varphi=0^\circ$):"), M(r"A_F=Fs=150\cdot10"), A(r"A_F=1500\ \text{J}")]),
  (r"Công của lực ma sát", [P(r"Ma sát ngược chiều chuyển động ($\varphi=180^\circ$):"), M(r"A_\text{ms}=-F_\text{ms}s=-25\cdot10"), A(r"A_\text{ms}=-250\ \text{J}")]),
  (r"Công của trọng lực", [P(r"Độ cao đỉnh dốc so với chân dốc:"), M(r"h=s\sin30^\circ=10\cdot0{,}5=5{,}0\ \text{m}"), M(r"A_P=-mgh=-20\cdot10\cdot5{,}0"), A(r"A_P=-1000\ \text{J}"),
                           P(r"Phản lực $\vec N$ vuông góc mặt dốc nên $A_N=0$.")]),
  (r"Tốc độ ở đỉnh dốc (định lí động năng)", [M(r"\dfrac12mv^2-0=A_F+A_\text{ms}+A_P"), M(r"\dfrac12mv^2=1500-250-1000=250\ \text{J}"), M(r"v=\sqrt{\dfrac{2\cdot250}{20}}=\sqrt{25}"), A(r"v=5{,}0\ \text{m/s}")]),
  (r"Lực kéo để thùng vừa tới đỉnh thì dừng", [P(r"Động năng đầu $\dfrac12mv_0^2$ với $v_0=2{,}0\ \text{m/s}$, động năng cuối bằng $0$:"), M(r"0-\dfrac12mv_0^2=F's+A_\text{ms}+A_P"),
                                              M(r"-\dfrac12\cdot20\cdot2{,}0^2=F'\cdot10-250-1000"), M(r"-40=10F'-1250\ \Rightarrow\ F'=\dfrac{1210}{10}"), A(r"F'=121\ \text{N}")]),
  (r"Kiểm tra", [P(r"Hợp lực dọc dốc: $121-25-100=-4\ \text{N}$, âm nên thùng giảm tốc, gia tốc $a=\dfrac{-4}{20}=-0{,}2\ \text{m/s}^2$."),
                 M(r"v^2=v_0^2+2as=2{,}0^2+2\cdot(-0{,}2)\cdot10=0\ \checkmark")])],
  [r"a) $v=5{,}0\ \text{m/s}$", r"b) $F'=121\ \text{N}$"],
  r"Nhận dạng: đề có <strong>nhiều ngoại lực</strong> (kéo, ma sát, trọng lực) và hỏi tốc độ → cộng công mọi lực, cho bằng độ biến thiên động năng."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>khối lượng và tốc độ (km/h)</b> hoặc <b>so sánh động năng</b> → nghĩ tới <b>đổi ra m/s</b> rồi <b>½mv²</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Đổi tốc độ ra m/s", r"Tốc độ ban đầu của xe tải theo m/s là bao nhiêu?", 10, "m/s", 0.1,
       loi=r"Thế thẳng số km/h vào công thức, hoặc nhân với $3{,}6$ thay vì chia."),
  buoc(r"Động năng của xe tải", r"Động năng của xe tải bằng bao nhiêu kJ?", 200, "kJ", 1,
       loi=r"Quên bình phương tốc độ hoặc quên hệ số $\dfrac12$.",
       ke=[(r"Bình phương tốc độ (m/s) rồi nhân với một nửa khối lượng (kg)", True),
           (r"Nhân khối lượng với tốc độ rồi chia đôi", r"Động năng tỉ lệ với bình phương tốc độ, không phải với tốc độ."),
           (r"Thế thẳng tốc độ theo km/h", r"Kết quả chỉ có đơn vị J khi $m$ tính bằng kg và $v$ tính bằng m/s.")]),
  buoc(r"Tốc độ của ô tô con", r"Tốc độ của ô tô con bằng bao nhiêu m/s?", 20, "m/s", 0.2,
       loi=r"Quên khai căn, hoặc quên đổi tấn ra kg.",
       ke=[(r"Đặt động năng ô tô con bằng động năng xe tải rồi giải ra tốc độ", True),
           (r"Cho tốc độ ô tô con bằng tốc độ xe tải", r"Động năng bằng nhau nhưng khối lượng khác nhau thì tốc độ khác nhau."),
           (r"Cho tích khối lượng nhân tốc độ của hai xe bằng nhau", r"Động năng tỉ lệ với $mv^2$ chứ không phải $mv$.")]),
  buoc(r"Tăng tốc đến $90\ \text{km/h}$", r"Động năng xe tải lúc sau gấp mấy lần lúc đầu?", 6.25, None, 0.05,
       loi=r"Lấy tỉ số hai tốc độ rồi quên bình phương.",
       ke=[(r"Lập tỉ số tốc độ sau với tốc độ đầu rồi bình phương", True),
           (r"Lấy tỉ số tốc độ, không bình phương", r"Động năng tỉ lệ với bình phương tốc độ nên tỉ số động năng là bình phương tỉ số tốc độ."),
           (r"Lấy hiệu hai tốc độ rồi bình phương", r"So sánh hai động năng là lập tỉ số, không phải lấy hiệu hai tốc độ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>độ cao so với mốc</b> và hỏi <b>thế năng</b> → nghĩ tới <b>mgz</b> với z tính từ mốc.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc(r"Thế năng của thùng $A$", r"Thế năng trọng trường của thùng $A$ bằng bao nhiêu J?", 180, "J", 1,
       loi=r"Quên nhân với $g$, hoặc lấy độ cao của thùng khác."),
  buoc(r"Thế năng của thùng $B$", r"Thế năng trọng trường của thùng $B$ bằng bao nhiêu J?", 180, "J", 1,
       loi=r"Thế khối lượng của thùng này vào độ cao của thùng kia.",
       ke=[(r"Dùng cùng công thức với khối lượng và độ cao của chính thùng $B$", True),
           (r"Dùng khối lượng của thùng $A$ vì cùng một mốc", r"Mỗi thùng có khối lượng riêng; mốc chung không làm hai khối lượng bằng nhau."),
           (r"Cộng thế năng của thùng $B$ vào thế năng đã tính của thùng $A$", r"Thế năng của một thùng chỉ tính từ khối lượng và độ cao của chính thùng đó.")]),
  buoc(r"So sánh hai thế năng", r"Chọn kết luận đúng về thế năng của hai thùng.",
       loi=r"Chỉ so độ cao hoặc chỉ so khối lượng mà không tính tích $mgz$.",
       lua_chon=[(r"Hai thùng có thế năng bằng nhau", True),
                 (r"Thùng $B$ lớn hơn vì ở cao hơn", r"Thế năng phụ thuộc cả độ cao lẫn khối lượng; chỉ xét độ cao là bỏ sót khối lượng."),
                 (r"Thùng $A$ lớn hơn vì nặng hơn", r"Thế năng phụ thuộc cả khối lượng lẫn độ cao; chỉ xét khối lượng là bỏ sót độ cao.")],
       ke=[(r"So hai kết quả vừa tính", True),
           (r"So riêng độ cao của hai thùng", r"Thế năng còn phụ thuộc khối lượng nên so riêng độ cao chưa đủ."),
           (r"So riêng khối lượng của hai thùng", r"Thế năng còn phụ thuộc độ cao nên so riêng khối lượng chưa đủ.")]),
  buoc(r"Độ cao của thùng $C$", r"Thùng $C$ ở độ cao bao nhiêu mét so với nền kho?", 3.0, "m", 0.05,
       loi=r"Chia cho khối lượng mà quên $g$, hoặc nhân thay vì chia.",
       ke=[(r"Từ $W_\text{t}=mgz$ rút $z$ rồi thế số", True),
           (r"Nhân $W_\text{t}$ với $m$ và $g$", r"Từ $W_\text{t}=mgz$, muốn có $z$ phải chia cho $mg$, không nhân."),
           (r"Chia $W_\text{t}$ cho $m$ mà bỏ $g$", r"Thiếu $g$ nên kết quả không còn đơn vị mét.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đổi mốc thế năng</b> hoặc vật <b>nằm dưới mốc</b> → nghĩ tới <b>tính lại z có dấu</b> theo mốc mới.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Mốc tại mặt đường", r"Thế năng của chậu cây khi mốc ở mặt đường là bao nhiêu J?", 120, "J", 1,
       loi=r"Quên nhân với $g$ hoặc quên khối lượng."),
  buoc(r"Mốc tại sàn tầng hầm", r"Thế năng của chậu cây khi mốc ở sàn tầng hầm là bao nhiêu J?", 200, "J", 1,
       loi=r"Giữ nguyên $z$ của mốc cũ, hoặc tính sai khoảng cách từ mốc mới tới chậu cây.",
       ke=[(r"Tính lại $z$ từ mốc mới rồi mới thế vào công thức", True),
           (r"Giữ nguyên $z$ vì chậu cây không di chuyển", r"$z$ tính từ mốc nên mốc đổi thì $z$ phải đổi."),
           (r"Lấy $6{,}0-4{,}0$ vì hầm nằm dưới mặt đường", r"Hầm ở phía dưới mặt đường nên khoảng cách từ sàn hầm tới chậu cây là tổng hai khoảng, không phải hiệu.")]),
  buoc(r"Mốc tại sàn tầng 6", r"Thế năng của chậu cây khi mốc ở sàn tầng 6 là bao nhiêu J?", -180, "J", 1,
       loi=r"Bỏ qua dấu của $z$, hoặc lấy khoảng cách làm $z$.",
       ke=[(r"Xét chậu nằm trên hay dưới mốc rồi chọn dấu của $z$", True),
           (r"Lấy $z$ bằng khoảng cách giữa chậu và mốc, bỏ qua dấu", r"$z$ là toạ độ có dấu, khoảng cách chỉ là độ lớn của $z$."),
           (r"Cho $W_\text{t}=0$ vì chậu không đổi chỗ", r"$W_\text{t}=0$ chỉ khi vật ở đúng mốc.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>công của trọng lực</b> giữa hai vị trí → nghĩ tới <b>thế năng đầu trừ thế năng cuối</b>, bỏ qua đường đi.",
  cap_do=2, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Từ $A$ đến $B$", r"Công của trọng lực từ $A$ đến $B$ bằng bao nhiêu kJ?", 16.8, "kJ", 0.1,
       loi=r"Lấy thế năng cuối trừ đầu, quên nhân với $g$, hoặc quên đổi J ra kJ."),
  buoc(r"Từ $B$ đến $C$", r"Công của trọng lực từ $B$ đến $C$ bằng bao nhiêu kJ?", -7.8, "kJ", 0.1,
       loi=r"Lấy độ lớn độ chênh cao rồi bỏ dấu của công.",
       ke=[(r"Dùng cùng công thức thế năng đầu trừ thế năng cuối cho đoạn $BC$", True),
           (r"Lấy giá trị tuyệt đối vì độ cao đổi thì công luôn dương", r"Công có dấu; dấu cho biết trọng lực phát động hay cản chuyển động."),
           (r"Lấy trọng lượng nhân quãng đường $BC$", r"Quãng đường $BC$ không cho; công của trọng lực chỉ cần độ cao đầu và độ cao cuối.")]),
  buoc(r"Từ $A$ đến $C$", r"Công của trọng lực từ $A$ đến $C$ bằng bao nhiêu kJ?", 9.0, "kJ", 0.1,
       loi=r"Cộng độ lớn công hai đoạn thay vì cộng đại số, hoặc đi tìm độ dài đường quanh co.",
       ke=[(r"Lấy thế năng tại $A$ trừ thế năng tại $C$", True),
           (r"Cộng độ lớn công của hai đoạn $AB$ và $BC$", r"Công đi lên mang dấu khác nên phải cộng đại số chứ không cộng độ lớn."),
           (r"Tính độ dài đường đi từ $A$ qua $B$ tới $C$ rồi nhân trọng lực", r"Công của trọng lực không phụ thuộc đường đi; dữ kiện độ dài đường cũng không có.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nhiều ngoại lực</b> (kéo, ma sát, trọng lực) và hỏi <b>tốc độ</b> → nghĩ tới <b>cộng công mọi lực</b> = biến thiên động năng.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Công của lực kéo", r"Công của lực kéo trên cả dốc bằng bao nhiêu J?", 1500, "J", 5,
       loi=r"Nhân lực kéo với độ cao đỉnh dốc thay vì với chiều dài dốc."),
  buoc(r"Công của lực ma sát", r"Công của lực ma sát trên cả dốc bằng bao nhiêu J?", -250, "J", 2,
       loi=r"Bỏ sót công của ma sát, hoặc gán sai dấu.",
       ke=[(r"Xét chiều của ma sát so với chuyển động rồi tính $F_\text{ms}s\cos\varphi$", True),
           (r"Bỏ qua ma sát vì đề đã cho lực kéo", r"Mọi ngoại lực đều phải có mặt trong tổng công, kể cả lực cản."),
           (r"Lấy lực ma sát nhân độ cao đỉnh dốc", r"Ma sát sinh công trên quãng đường thùng trượt dọc mặt dốc, không phải trên độ cao.")]),
  buoc(r"Công của trọng lực", r"Công của trọng lực khi thùng lên tới đỉnh dốc bằng bao nhiêu J?", -1000, "J", 5,
       loi=r"Lấy trọng lượng nhân chiều dài dốc, quên rằng trọng lực chỉ sinh công theo độ cao.",
       ke=[(r"Lấy trọng lượng nhân độ cao đỉnh dốc, xét dấu", True),
           (r"Lấy trọng lượng nhân chiều dài dốc", r"Chiều dài dốc không phải độ cao; trọng lực chỉ sinh công theo độ cao thay đổi."),
           (r"Bỏ qua trọng lực vì đã có lực kéo và ma sát", r"Trọng lực là ngoại lực và sinh công khi vật đổi độ cao.")]),
  buoc(r"Tốc độ ở đỉnh dốc", r"Tốc độ của thùng khi tới đỉnh dốc bằng bao nhiêu m/s?", 5.0, "m/s", 0.1,
       loi=r"Quên một trong ba công, cộng độ lớn thay vì cộng đại số, hoặc quên hệ số $\dfrac12$.",
       ke=[(r"Cộng công của ba lực rồi cho bằng độ biến thiên động năng", True),
           (r"Chỉ lấy công của lực kéo", r"Ma sát và trọng lực cũng sinh công nên phải cộng vào tổng."),
           (r"Cộng độ lớn công của ba lực, bỏ dấu", r"Công cản mang dấu khác công phát động nên phải cộng đại số.")]),
  buoc(r"Lực kéo để thùng vừa tới đỉnh thì dừng", r"Lực kéo phải có độ lớn bao nhiêu N?", 121, "N", 1,
       loi=r"Coi động năng đầu bằng $0$ dù thùng được đẩy sẵn, hoặc bỏ sót công của một lực.",
       ke=[(r"Cho tổng công ba lực bằng độ biến thiên động năng, từ tốc độ đầu về $0$", True),
           (r"Cho lực kéo bằng lực ma sát", r"Đi lên dốc thì trọng lực cũng cản chuyển động nên lực kéo phải thắng cả hai."),
           (r"Cho tổng công của ba lực bằng $0$", r"Động năng không đứng yên từ đầu: đầu khác $0$, cuối bằng $0$ nên độ biến thiên khác $0$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập, giữ NGUYÊN lời giải gốc, xếp dễ → khó ═════════════
def split_cau(block):
    """Tách một khối cũ thành {số câu: (đề_html, lời_giải_html)}."""
    ps = re.findall(r"<p[^>]*>.*?</p>", OLD[block]["body_html"], flags=re.S)
    out, cur = {}, None
    for p in ps:
        mm = re.search(r"Câu (\d+)\.", re.sub(r"<[^>]+>", "", p))
        if mm and re.match(r"<p[^>]*><strong[^>]*>Câu", p):
            cur = int(mm.group(1)); out[cur] = [p, []]
        else:
            out[cur][1].append(p)
    return out

def fix_math(h):
    def f(m):
        return m.group(0).replace("&lt;", r"\lt ").replace("&gt;", r"\gt ").replace("<", r"\lt ").replace(">", r"\gt ")
    return re.sub(r"\$[^$]*\$", f, h)

CAU = {b: split_cau(b) for b in range(4)}
PICK = [(2, 1, "Dễ"), (0, 2, "Dễ"), (0, 11, "Dễ"), (0, 7, "Dễ"),
        (2, 2, "Trung bình"), (2, 12, "Trung bình"), (3, 11, "Trung bình"), (2, 10, "Trung bình"),
        (1, 1, "Trung bình"), (1, 4, "Trung bình"), (1, 5, "Trung bình"), (1, 6, "Trung bình"), (1, 2, "Trung bình"), (1, 7, "Trung bình"),
        (2, 14, "Khó"), (1, 12, "Khó"), (1, 10, "Khó"), (0, 12, "Khó")]
parts = []
for k, (b, c, muc) in enumerate(PICK, 1):
    de, giai = CAU[b][c]
    de = re.sub(r"Câu \d+\.", f"Bài {k}.", de, count=1)
    de = re.sub(r"(?<=[.?:$]) ([a-d])\. ", r"<br>\1. ", de)   # mỗi ý a., b., c. một dòng (chỉ đề, không đụng lời giải)
    parts.append(f'<h4>Bài {k} · {muc}</h4>{fix_math(de)}<details><summary>Hướng dẫn giải</summary>{fix_math("".join(giai))}</details>')
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))

write(J, 70, "Bài 25. Động năng, thế năng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
