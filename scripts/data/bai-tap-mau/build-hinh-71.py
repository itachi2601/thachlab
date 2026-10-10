"""Bài 71 — "Bài 26. Cơ năng và định luật bảo toàn cơ năng" (Vật lí 10, chương 4). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-58.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-71.py  → ghi scripts/data/bai-tap-mau/71.json
Dạng theo quét: scripts/logs/batch-ra-soat/ket-qua/71.quet-dang.json. Hình: hinh_71.py (mọi chuyển động tính thật).
Ví dụ cũ (old/71.json: 3 mục, 17 ví dụ): ví dụ 2 (mục 1) → Dạng 3 (đổi số: ném lên, Wđ = Wt);
ví dụ 7, 8 (mục 1) → Dạng 4 (đổi số: ném từ tầng cao, Wđ = nWt, độ cao cực đại); ví dụ 1, 4, 5, 6, 11, 12 (mục 1), 1, 2 (mục 2), 1, 2 (mục 3) → tự luận.
BỎ: VD3 (mục 1: chọn mốc ở vị trí ném mà vẫn cộng thế năng 200 J, cuối bài lại đổi mốc "cách mặt đất 32,5 m" — vật lí sai, đúng là 12,5 m so với mặt đất),
VD9 (mục 1: "thế năng gấp 2 lần động năng ⇒ z = z_A/3 = 15 m" sai, đúng 30 m), VD10 (phụ thuộc VD9 và F_C ≈ 449 N sai, đúng 451 N),
VD13 (mục 1: đường ướt v' = 11,8 m/s lớn hơn tốc độ đầu 10 m/s — sai dấu, đúng ≈ 7,75 m/s; ngoài phạm vi bài: định lí động năng)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_71 import BUILD

J = os.path.join(HERE, "71.json")
OLD = json.load(open(os.path.join(HERE, "old/71.json")))["questions"]
T30, T138, T139 = ("Cơ năng và định luật bảo toàn cơ năng", "Bảo toàn cơ năng khi chỉ có trọng lực", "Biến thiên cơ năng khi có ma sát")

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
g = 10.0
# D1: đá 0,20 kg ném lên từ cửa sổ 6 m; qua P (8 m) với 3 m/s
m, v0, z0, zP, vP = 0.20, 7.0, 6.0, 8.0, 3.0
ok("D1 v tại P (động học)", math.sqrt(v0**2 - 2 * g * (zP - z0)), vP, 1e-9)
Wd = 0.5 * m * vP**2; ok("D1 Wd", Wd, 0.90, 1e-9)
W_dat = Wd + m * g * zP; W_cs = Wd + m * g * (zP - 6); W_mai = Wd + m * g * (zP - 10)
ok("D1 W đất", W_dat, 16.9, 1e-9); ok("D1 Wt đất", m * g * zP, 16, 1e-9)
ok("D1 W cửa sổ", W_cs, 4.9, 1e-9); ok("D1 Wt cs", m * g * (zP - 6), 4.0, 1e-9)
ok("D1 W mái", W_mai, -3.1, 1e-9); ok("D1 Wt mái", m * g * (zP - 10), -4.0, 1e-9)
ok("D1 W cs = ½mv0² (bảo toàn từ cửa sổ)", 0.5 * m * v0**2, W_cs, 1e-9)
ok("D1 kiểm hiệu 1", W_dat - W_cs, 12.0, 1e-9); ok("D1 kiểm hiệu 2", W_dat - W_mai, 20.0, 1e-9)
assert Wd != W_dat and W_cs != W_mai and abs(W_dat - W_cs) > 5          # các mốc cho kết quả khác nhau
assert abs(0.5 * m * vP**2 + m * g * 2.0 - W_cs) < 1e-9                  # sai: giữ z = 8 m ở mốc cửa sổ
assert abs((Wd + m * g * zP) - W_cs) > 5 and abs((Wd + m * g * abs(zP - 10)) - W_mai) > 5   # sai: |z| thay vì z có dấu
# D2: máng nhẵn
m2, HA, zM, vN = 0.050, 2.45, 1.2, 3.0
WA = m2 * g * HA; ok("D2 WA", WA, 1.225, 1e-9)
vO = math.sqrt(2 * WA / m2); ok("D2 vO", vO, 7.0, 1e-9); ok("D2 vO=√2gH", math.sqrt(2 * g * HA), 7.0, 1e-9)
WtM = m2 * g * zM; WdM = WA - WtM; ok("D2 WtM", WtM, 0.60, 1e-9); ok("D2 WdM", WdM, 0.625, 1e-9)
vM = math.sqrt(2 * WdM / m2); ok("D2 vM", vM, 5.0, 1e-9)
zN = (WA - 0.5 * m2 * vN**2) / (m2 * g); ok("D2 zN", zN, 2.0, 1e-9); ok("D2 0,5mv²N", 0.5 * m2 * vN**2, 0.225, 1e-9)
assert abs(vM - vO / 2) > 1 and abs(vN**2 / (2 * g) - zN) > 1 and abs(zN - HA * vN / vO) > 0.5      # các cách sai khác đáp án
# D3: ném từ mặt đất 12 m/s, m = 0,40
m3, v3 = 0.40, 12.0
W3 = 0.5 * m3 * v3**2; ok("D3 W", W3, 28.8, 1e-9)
z3 = (W3 / 2) / (m3 * g); ok("D3 z(Wd=Wt)", z3, 3.6, 1e-9); ok("D3 zmax", v3**2 / (2 * g), 7.2, 1e-9)
Wt5 = m3 * g * 5.0; Wd5 = W3 - Wt5; ok("D3 Wt5", Wt5, 20.0, 1e-9); ok("D3 Wd5", Wd5, 8.8, 1e-9)
ok("D3 kiểm", Wd5 + Wt5, W3, 1e-9); ok("D3 kiểm Wd=Wt", 2 * m3 * g * z3, W3, 1e-9)
assert 5.0 < 7.2 and 3.6 < 7.2
assert abs(Wd5 - W3) > 5 and abs(Wd5 - (W3 / 2)) > 3 and abs(z3 - 7.2) > 1       # sai: Wd = ½mv0²; Wd = Wt; z = zmax
# D4: ném từ sân thượng 3 m, đạt 8 m, m = 0,20
m4, h0, zmax = 0.20, 3.0, 8.0
W4 = m4 * g * zmax; ok("D4 W", W4, 16.0, 1e-9)
v04 = math.sqrt(2 * (W4 - m4 * g * h0) / m4); ok("D4 v0", v04, 10.0, 1e-9); ok("D4 W tại ném", 0.5 * m4 * v04**2 + m4 * g * h0, W4, 1e-9)
z4 = (W4 / 4) / (m4 * g); ok("D4 z(Wd=3Wt)", z4, 2.0, 1e-9)
ok("D4 Wd=3Wt kiểm", 3 * m4 * g * z4 + m4 * g * z4, W4, 1e-9)
W4p = W4 - m4 * g * h0; ok("D4 W'", W4p, 10.0, 1e-9); ok("D4 W' = ½mv0²", 0.5 * m4 * v04**2, W4p, 1e-9)
ok("D4 zmax'", v04**2 / (2 * g), 5.0, 1e-9); ok("D4 zmax' = 8−3", zmax - h0, 5.0, 1e-9)
assert abs(math.sqrt(2 * g * zmax) - v04) > 1 and abs(zmax / 3 - z4) > 0.3 and abs((W4 / 3) / (m4 * g) - z4) > 0.3   # các cách sai
assert abs(3 * (W4 / 4) / (m4 * g) - z4) > 1                                                                       # Wt = 3Wd
ok("D4 mốc khác: Wd=3Wt", (W4p / 4) / (m4 * g) + h0, 4.25, 1e-9)           # ghi chú: vị trí đó khác 2,0 m
# D5: trượt tuyết 50 kg, A cao 10 m, B 12 m/s; lượt 2 qua A với 5 m/s
m5, hA, vB, vA2 = 50.0, 10.0, 12.0, 5.0
WA5 = m5 * g * hA; WB5 = 0.5 * m5 * vB**2; Ac = WB5 - WA5
ok("D5 WA", WA5, 5000, 1e-9); ok("D5 WB", WB5, 3600, 1e-9); ok("D5 Ac", Ac, -1400, 1e-9)
ok("D5 %", abs(Ac) / WA5 * 100, 28.0, 1e-9)
WA52 = 0.5 * m5 * vA2**2 + m5 * g * hA; WB52 = WA52 + Ac
ok("D5 WA'", WA52, 5625, 1e-9); ok("D5 WB'", WB52, 4225, 1e-9)
v52 = math.sqrt(2 * WB52 / m5); ok("D5 v'", v52, 13.0, 1e-9)
ok("D5 v bảo toàn", math.sqrt(vA2**2 + 2 * g * hA), 15.0, 1e-9); assert vB < v52 < 15.0
assert abs(vB - v52) > 0.5 and abs(WB5 / WA5 * 100 - 28) > 30 and abs(abs(Ac) / WB5 * 100 - 28) > 5   # sai: v cũ; % theo W_B; W_B/W_A
ok("D5 lực cản dốc 30° (hình)", 50 * (10 * 0.5 - 12.0**2 / 40) * 20, 1400, 1e-6)
# Tự luận cũ
ok("TL Ex1", 8 / math.sqrt(2), 5.66, 0.005); ok("TL Ex4", math.sqrt(2 * 9.8 * 10), 14, 0.1)
ok("TL Ex5 đỉnh", 20 * 9.8 * 2, 392, 1e-9); ok("TL Ex5 chân", 0.5 * 20 * 16, 160, 1e-9)
ok("TL Ex6", math.sqrt(16 + 2 * 9.8), 6, 0.05); ok("TL Ex12", (22.5 - 19.6) / 22.5 * 100, 12.9, 0.05)
ok("TL Ex11", 0.25 * 10 * (4.8 + 0.16) / 0.16, 77.5, 1e-9); ok("TL Ex2 mục2", math.sqrt(2 * (30 - 0.1 * 2 * 10 * math.cos(math.radians(30)) * 3) / 2), 4.98, 0.01)

# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Tính cơ năng theo mốc thế năng đã chọn", topic=T30,
      problem_html=r"""<p>Hòn đá khối lượng $0{,}20\ \text{kg}$ được ném thẳng đứng lên từ một cửa sổ cách mặt đất $6{,}0\ \text{m}$. Đang đi lên, hòn đá qua điểm $P$ cách mặt đất $8{,}0\ \text{m}$ với tốc độ $3{,}0\ \text{m/s}$. Mái sân thượng của toà nhà cao $10\ \text{m}$ so với mặt đất. Lấy $g=10\ \text{m/s}^2$.</p>
<p>Tính động năng, thế năng và cơ năng của hòn đá tại $P$ khi chọn mốc thế năng ở:</p>
<ol type="a"><li>mặt đất;</li><li>cửa sổ;</li><li>mái sân thượng.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Bảo toàn cơ năng: tìm tốc độ và độ cao", topic=T138,
      problem_html=r"""<p>Hòn bi nhỏ khối lượng $50\ \text{g}$ được thả không vận tốc đầu từ đỉnh $A$ của một máng cong nhẵn. Điểm $A$ cao $2{,}45\ \text{m}$ so với chân máng $O$. Bỏ qua mọi lực cản, lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính tốc độ của bi tại $O$.</li>
<li>Tính tốc độ của bi tại điểm $M$ cao $1{,}2\ \text{m}$ so với chân máng.</li>
<li>Tại một điểm $N$ trên máng, tốc độ của bi bằng $3{,}0\ \text{m/s}$. Tính độ cao của $N$ so với chân máng.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Điều kiện bảo toàn và vị trí động năng bằng thế năng", topic=T138,
      problem_html=r"""<p>Hòn đá khối lượng $0{,}40\ \text{kg}$ được ném thẳng đứng lên từ mặt đất với tốc độ $12\ \text{m/s}$. Bỏ qua sức cản của không khí, lấy $g=10\ \text{m/s}^2$ và chọn mốc thế năng ở mặt đất.</p>
<ol type="a"><li>Trong lúc đi lên, cơ năng của hòn đá thay đổi thế nào? Giải thích.</li>
<li>Tính cơ năng của hòn đá.</li>
<li>Tìm độ cao tại đó động năng bằng thế năng.</li>
<li>Tính động năng của hòn đá khi nó ở độ cao $5{,}0\ \text{m}$.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Ném lên từ sân thượng: tốc độ ném, động năng gấp ba thế năng, đổi mốc", topic=T138,
      problem_html=r"""<p>Từ sân thượng cao $3{,}0\ \text{m}$ so với mặt đất, một bạn ném thẳng đứng lên hòn sỏi khối lượng $0{,}20\ \text{kg}$. Hòn sỏi lên tới độ cao cực đại $8{,}0\ \text{m}$ so với mặt đất rồi rơi xuống. Bỏ qua sức cản của không khí, lấy $g=10\ \text{m/s}^2$ và chọn mốc thế năng ở mặt đất.</p>
<ol type="a"><li>Tính cơ năng của hòn sỏi.</li>
<li>Tính tốc độ lúc ném.</li>
<li>Tìm độ cao (so với mặt đất) tại đó động năng bằng ba lần thế năng.</li>
<li>Chọn lại mốc thế năng ở mặt sân thượng. Tính cơ năng của hòn sỏi và độ cao cực đại của nó so với mốc mới.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Có lực cản: công của lực cản từ độ giảm cơ năng", topic=T139,
      problem_html=r"""<p>Vận động viên trượt tuyết khối lượng $50\ \text{kg}$ (kể cả dụng cụ) xuất phát từ nghỉ ở đỉnh dốc $A$, cao $10\ \text{m}$ so với chân dốc $B$, và trượt xuống chân dốc với tốc độ $12\ \text{m/s}$. Lấy $g=10\ \text{m/s}^2$ và chọn mốc thế năng ở chân dốc.</p>
<ol type="a"><li>Tính cơ năng của vận động viên tại $A$ và tại $B$.</li>
<li>Tính công của lực cản (ma sát và không khí) trên dốc.</li>
<li>Lực cản đã lấy đi bao nhiêu phần trăm cơ năng ban đầu?</li>
<li>Ở một lượt trượt khác, vận động viên qua $A$ với tốc độ $5{,}0\ \text{m/s}$. Coi công của lực cản trên dốc vẫn như lượt trước, tính tốc độ ở chân dốc.</li></ol>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“Hòn đá khối lượng $0{,}20$ kg”", r"$m=0{,}20\ \text{kg}$", r"Khối lượng có mặt ở cả động năng và thế năng"),
  (r"“ném thẳng đứng lên từ một cửa sổ cách mặt đất $6{,}0$ m”", r"Cửa sổ cao $6{,}0\ \text{m}$ so với mặt đất", r"Độ cao của một điểm phải đo từ mốc thế năng"),
  (r"“qua điểm $P$ cách mặt đất $8{,}0$ m với tốc độ $3{,}0$ m/s”", r"$z_P=8{,}0\ \text{m}$ (so với mặt đất); $v_P=3{,}0\ \text{m/s}$", r"Động năng $\dfrac12mv^2$ · thế năng $mgz$"),
  (r"“mái sân thượng của toà nhà cao $10$ m so với mặt đất”", r"Mái cao $10\ \text{m}$ so với mặt đất", r"Mốc thứ ba, nằm ở phía trên $P$"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Thế năng trọng trường $mgz$"),
  (r"“khi chọn mốc thế năng ở: a) mặt đất; b) cửa sổ; c) mái sân thượng”", r"Ba mốc, cách mặt đất lần lượt $0$; $6{,}0$ m; $10$ m", r"⚠ Thế năng và cơ năng phụ thuộc mốc, động năng thì không; $z$ luôn đo từ mốc đã chọn"),
  (r"“Tính động năng, thế năng và cơ năng tại $P$”", r"Cần $W_\text{d}$, $W_\text{t}$, $W$ (J)", r"$W=W_\text{d}+W_\text{t}$")],
 [(r"“Hòn bi nhỏ khối lượng $50$ g”", r"$m=50\ \text{g}=0{,}050\ \text{kg}$", r"Đổi sang kilôgam trước khi tính"),
  (r"“thả không vận tốc đầu từ đỉnh $A$ của một máng cong nhẵn”", r"$v_A=0$", r"⚠ Máng nhẵn: chỉ trọng lực sinh công; phản lực vuông góc đường đi không sinh công"),
  (r"“$A$ cao $2{,}45$ m so với chân máng $O$”", r"$z_A=2{,}45\ \text{m}$; mốc ở $O$ nên $z_O=0$", r"Độ cao đo từ mốc thế năng"),
  (r"“Bỏ qua mọi lực cản, lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"⚠ Bỏ qua lực cản: được dùng $W_1=W_2$ giữa hai vị trí bất kì"),
  (r"“a) tốc độ của bi tại $O$”", r"Cần $v_O$ (m/s)", r"$W_A=W_O$"),
  (r"“b) điểm $M$ cao $1{,}2$ m so với chân máng”", r"$z_M=1{,}2\ \text{m}$; cần $v_M$ (m/s)", r"$W_A=W_M$, với $W_M=W_\text{d}+W_\text{t}$"),
  (r"“c) tại một điểm $N$, tốc độ của bi bằng $3{,}0$ m/s”", r"$v_N=3{,}0\ \text{m/s}$; cần $z_N$ (m)", r"$W_A=W_N$, rút $z_N$")],
 [(r"“Hòn đá khối lượng $0{,}40$ kg … ném thẳng đứng lên từ mặt đất với tốc độ $12$ m/s”", r"$m=0{,}40\ \text{kg}$; $z_0=0$; $v_0=12\ \text{m/s}$", r"Lúc ném: có động năng, chưa có thế năng (mốc ở mặt đất)"),
  (r"“Bỏ qua sức cản của không khí”", r"Chỉ có trọng lực tác dụng", r"⚠ Chỉ trọng lực (hay lực đàn hồi) sinh công thì mới dùng được định luật bảo toàn cơ năng"),
  (r"“lấy $g=10$ m/s² và chọn mốc thế năng ở mặt đất”", r"$g=10\ \text{m/s}^2$; $z$ đo từ mặt đất", r"Thế năng $mgz$"),
  (r"“a) cơ năng của hòn đá thay đổi thế nào?”", r"Cần kết luận về sự thay đổi của $W$", r"Điều kiện của định luật bảo toàn cơ năng"),
  (r"“b) Tính cơ năng”", r"Cần $W$ (J)", r"$W=W_\text{d}+W_\text{t}$"),
  (r"“c) động năng bằng thế năng”", r"$W_\text{d}=W_\text{t}$; cần $z$ (m)", r"Quan hệ giữa $W$ và $W_\text{t}$ khi hai thành phần bằng nhau"),
  (r"“d) ở độ cao $5{,}0$ m, tính động năng”", r"$z=5{,}0\ \text{m}$; cần $W_\text{d}$ (J)", r"$W_\text{d}=W-W_\text{t}$")],
 [(r"“Từ sân thượng cao $3{,}0$ m … ném thẳng đứng lên hòn sỏi khối lượng $0{,}20$ kg”", r"$z_0=3{,}0\ \text{m}$; $m=0{,}20\ \text{kg}$; $v_0\ne0$", r"Điểm ném đã có cả động năng lẫn thế năng"),
  (r"“Bỏ qua sức cản của không khí, lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"⚠ Chỉ trọng lực sinh công: dùng được $W_1=W_2$"),
  (r"“lên tới độ cao cực đại $8{,}0$ m so với mặt đất”", r"$z_\text{max}=8{,}0\ \text{m}$; tại đó $v=0$", r"Tại điểm cao nhất động năng bằng $0$"),
  (r"“chọn mốc thế năng ở mặt đất”", r"$z$ đo từ mặt đất (ý a, b, c)", r"⚠ Dùng một mốc cho cả ý; đổi mốc thì $z$ và $W$ đổi"),
  (r"“a) cơ năng của hòn sỏi”", r"Cần $W$ (J)", r"$W=W_\text{d}+W_\text{t}$"),
  (r"“b) tốc độ lúc ném”", r"Cần $v_0$ (m/s)", r"$W$ tại điểm ném bằng $W$ đã tính"),
  (r"“c) động năng bằng ba lần thế năng”", r"$W_\text{d}=3W_\text{t}$; cần $z$ (m)", r"$W=W_\text{d}+W_\text{t}$"),
  (r"“d) mốc thế năng ở mặt sân thượng”", r"Mốc mới cách mặt đất $3{,}0\ \text{m}$", r"Độ cao mới $z'=z-3{,}0$; thế năng và cơ năng tính lại")],
 [(r"“khối lượng $50$ kg (kể cả dụng cụ)”", r"$m=50\ \text{kg}$", r"Khối lượng của cả hệ trượt"),
  (r"“xuất phát từ nghỉ ở đỉnh dốc $A$, cao $10$ m so với chân dốc $B$”", r"$v_A=0$; $z_A=10\ \text{m}$ (mốc ở $B$)", r"Tại $A$ chỉ có thế năng"),
  (r"“trượt xuống chân dốc với tốc độ $12$ m/s”", r"$v_B=12\ \text{m/s}$; $z_B=0$", r"Tại $B$ chỉ có động năng"),
  (r"“Lấy $g=10$ m/s² và chọn mốc thế năng ở chân dốc”", r"$g=10\ \text{m/s}^2$", r"Thế năng $mgz$ với $z$ đo từ chân dốc"),
  (r"“công của lực cản (ma sát và không khí)”", r"Cần $A_\text{c}$ (J)", r"⚠ Có ma sát, lực cản sinh công: cơ năng không bảo toàn, dùng $\Delta W=A_\text{c}$"),
  (r"“bao nhiêu phần trăm cơ năng ban đầu”", r"Cần tỉ lệ (%)", r"So với cơ năng ban đầu"),
  (r"“lượt khác, qua $A$ với tốc độ $5{,}0$ m/s”", r"$v_A'=5{,}0\ \text{m/s}$", r"Cơ năng đầu mới gồm cả động năng lẫn thế năng"),
  (r"“Coi công của lực cản vẫn như lượt trước”", r"$A_\text{c}'=A_\text{c}$", r"⚠ Giả thiết đề cho: công cản không đổi giữa hai lượt"),
  (r"“tính tốc độ ở chân dốc”", r"Cần $v_B'$ (m/s)", r"$W_B'=W_A'+A_\text{c}$, rút $v_B'$")],
]

# ═════════════ Lời giải từng bước ═════════════
R_1 = [r"<strong>Khái niệm:</strong> cơ năng là tổng của động năng và thế năng trọng trường, đơn vị jun (J).",
       r"$W=W_\text{d}+W_\text{t}=\dfrac12mv^2+mgz$.",
       r"$z$ đo từ mốc thế năng (trục hướng lên); điểm nằm dưới mốc thì $z\lt0$.",
       r"⚠ <strong>Điều kiện:</strong> thế năng và cơ năng phụ thuộc mốc; động năng không phụ thuộc mốc."]
R_2 = [r"<strong>Khái niệm:</strong> cơ năng $W=W_\text{d}+W_\text{t}=\dfrac12mv^2+mgz$.",
       r"<strong>Định luật:</strong> chỉ trọng lực sinh công thì cơ năng không đổi, $W_1=W_2$.",
       r"$\dfrac12mv_1^2+mgz_1=\dfrac12mv_2^2+mgz_2$; khối lượng $m$ có ở hai vế nên triệt tiêu.",
       r"⚠ <strong>Điều kiện:</strong> máng nhẵn, bỏ qua lực cản; phản lực của máng vuông góc đường đi nên không sinh công."]
R_3 = [r"<strong>Khái niệm:</strong> cơ năng $W=W_\text{d}+W_\text{t}$.",
       r"<strong>Định luật:</strong> chỉ trọng lực sinh công thì cơ năng không đổi, $W_1=W_2$.",
       r"Động năng giảm bao nhiêu thì thế năng tăng bấy nhiêu, và ngược lại.",
       r"$W_\text{d}=W_\text{t}$ thì $W=2W_\text{t}$.",
       r"⚠ <strong>Điều kiện:</strong> bỏ qua sức cản; tốc độ thay đổi không có nghĩa là cơ năng thay đổi."]
R_4 = [r"<strong>Khái niệm:</strong> cơ năng $W=W_\text{d}+W_\text{t}=\dfrac12mv^2+mgz$, $z$ đo từ mốc.",
       r"<strong>Định luật:</strong> chỉ trọng lực sinh công thì $W_1=W_2$.",
       r"Điểm cao nhất: $v=0$ nên $W=W_\text{t}$.",
       r"$W_\text{d}=nW_\text{t}$ thì $W=(n+1)W_\text{t}$.",
       r"⚠ <strong>Điều kiện:</strong> bỏ qua sức cản; mọi độ cao đo từ cùng một mốc, đổi mốc thì $z$ và $W$ đổi."]
R_5 = [r"<strong>Khái niệm:</strong> cơ năng $W=W_\text{d}+W_\text{t}$ theo mốc thế năng đã chọn.",
       r"<strong>Định luật:</strong> lực cản sinh công thì cơ năng đổi: $\Delta W=W_\text{sau}-W_\text{đầu}=A_\text{c}$.",
       r"Lực cản ngược chiều chuyển động nên $A_\text{c}\lt0$, cơ năng giảm.",
       r"Phần cơ năng mất: $\dfrac{\lvert A_\text{c}\rvert}{W_\text{đầu}}\cdot100\,\%$.",
       r"⚠ <strong>Điều kiện:</strong> có ma sát, lực cản thì không dùng $W_1=W_2$; viết $\Delta W=A_\text{c}$."]

SOLS = [
 sol(R_1, [
  (r"Động năng tại $P$", [P(r"Động năng chỉ phụ thuộc $m$ và $v$, không phụ thuộc mốc:"), M(r"W_\text{d}=\dfrac12mv^2=\dfrac12\cdot0{,}20\cdot3{,}0^2"), A(r"W_\text{d}=0{,}90\ \text{J}")]),
  (r"Mốc ở mặt đất", [P(r"Mốc ở mặt đất nên $z_P=8{,}0$ m:"), M(r"W_\text{t}=mgz_P=0{,}20\cdot10\cdot8{,}0=16\ \text{J}"), M(r"W=W_\text{d}+W_\text{t}=0{,}90+16"), A(r"W=16{,}9\ \text{J}")]),
  (r"Mốc ở cửa sổ", [P(r"Mốc ở cửa sổ: $P$ cao hơn mốc $8{,}0-6{,}0=2{,}0$ m nên $z_P=2{,}0$ m:"), M(r"W_\text{t}=mgz_P=0{,}20\cdot10\cdot2{,}0=4{,}0\ \text{J}"), M(r"W=W_\text{d}+W_\text{t}=0{,}90+4{,}0"), A(r"W=4{,}9\ \text{J}")]),
  (r"Mốc ở mái sân thượng", [P(r"Mái cao $10$ m, $P$ cao $8{,}0$ m: $P$ nằm dưới mốc $2{,}0$ m nên $z_P=-2{,}0$ m:"), M(r"W_\text{t}=mgz_P=0{,}20\cdot10\cdot(-2{,}0)=-4{,}0\ \text{J}"), M(r"W=W_\text{d}+W_\text{t}=0{,}90-4{,}0"), A(r"W=-3{,}1\ \text{J}"), P(r"Cơ năng âm không sai: nó chỉ cho biết $P$ nằm dưới mốc và động năng nhỏ hơn độ lớn thế năng.")]),
  (r"Kiểm tra", [P(r"Động năng giữ nguyên $0{,}90$ J ở cả ba mốc; thế năng và cơ năng đổi theo mốc."), M(r"16{,}9-4{,}9=12\ \text{J}=0{,}20\cdot10\cdot6{,}0"), M(r"16{,}9-(-3{,}1)=20\ \text{J}=0{,}20\cdot10\cdot10"), P(r"Hiệu hai cơ năng bằng $mg$ nhân khoảng cách giữa hai mốc ✓.")])],
  [r"a) mặt đất: $W_\text{d}=0{,}90\ \text{J}$ · $W_\text{t}=16\ \text{J}$ · $W=16{,}9\ \text{J}$",
   r"b) cửa sổ: $W_\text{d}=0{,}90\ \text{J}$ · $W_\text{t}=4{,}0\ \text{J}$ · $W=4{,}9\ \text{J}$",
   r"c) mái sân thượng: $W_\text{d}=0{,}90\ \text{J}$ · $W_\text{t}=-4{,}0\ \text{J}$ · $W=-3{,}1\ \text{J}$"],
  r"Nhận dạng: đề cho <strong>vị trí, tốc độ và mốc thế năng</strong> → tính động năng, rồi thế năng với $z$ đo từ mốc; cơ năng là tổng."),
 sol(R_2, [
  (r"Cơ năng tại $A$", [P(r"Mốc ở chân máng $O$. Đổi $m=50\ \text{g}=0{,}050\ \text{kg}$. Tại $A$ bi nghỉ nên chỉ có thế năng:"), M(r"W_A=mgz_A=0{,}050\cdot10\cdot2{,}45"), A(r"W_A=1{,}225\ \text{J}")]),
  (r"Tốc độ tại $O$", [P(r"Máng nhẵn, bỏ qua lực cản nên $W_O=W_A$. Tại $O$: $z_O=0$, chỉ còn động năng:"), M(r"\dfrac12mv_O^2=W_A"), M(r"v_O=\sqrt{\dfrac{2W_A}{m}}=\sqrt{\dfrac{2\cdot1{,}225}{0{,}050}}=\sqrt{49}"), A(r"v_O=7{,}0\ \text{m/s}")]),
  (r"Tốc độ tại $M$", [P(r"Tại $M$ bi còn thế năng:"), M(r"W_\text{t}(M)=mgz_M=0{,}050\cdot10\cdot1{,}2=0{,}60\ \text{J}"), M(r"W_\text{d}(M)=W_A-W_\text{t}(M)=1{,}225-0{,}60=0{,}625\ \text{J}"), M(r"v_M=\sqrt{\dfrac{2W_\text{d}(M)}{m}}=\sqrt{\dfrac{2\cdot0{,}625}{0{,}050}}=\sqrt{25}"), A(r"v_M=5{,}0\ \text{m/s}")]),
  (r"Độ cao của $N$", [P(r"Tại $N$: $v_N=3{,}0$ m/s, chưa biết $z_N$. Viết $W_N=W_A$:"), M(r"\dfrac12mv_N^2+mgz_N=W_A"), M(r"\dfrac12\cdot0{,}050\cdot3{,}0^2+0{,}050\cdot10\cdot z_N=1{,}225"), M(r"0{,}225+0{,}50\,z_N=1{,}225\ \Rightarrow\ z_N=\dfrac{1{,}000}{0{,}50}"), A(r"z_N=2{,}0\ \text{m}")]),
  (r"Kiểm tra", [P(r"Càng xuống thấp, tốc độ càng lớn: $z_N\gt z_M\gt z_O$ ứng với $v_N\lt v_M\lt v_O$ ✓."), M(r"v_O=\sqrt{2gz_A}=\sqrt{2\cdot10\cdot2{,}45}=\sqrt{49}=7{,}0\ \text{m/s}"), P(r"Cách này không cần khối lượng vì $m$ triệt tiêu ✓.")])],
  [r"a) $v_O=7{,}0\ \text{m/s}$", r"b) $v_M=5{,}0\ \text{m/s}$", r"c) $z_N=2{,}0\ \text{m}$"],
  r"Nhận dạng: máng <strong>nhẵn, bỏ qua lực cản</strong>, đề cho độ cao hoặc tốc độ ở hai vị trí → viết $W_1=W_2$, khối lượng triệt tiêu."),
 sol(R_3, [
  (r"Điều kiện áp dụng", [P(r"Đã bỏ qua sức cản nên trong lúc bay hòn đá chỉ chịu trọng lực."), P(r"Chỉ trọng lực sinh công nên cơ năng <strong>không đổi</strong>: động năng giảm bao nhiêu thì thế năng tăng bấy nhiêu."), A(r"T:Cơ năng không đổi trong suốt chuyển động."), P(r"Tốc độ giảm chỉ cho biết động năng giảm, không cho biết cơ năng giảm.")]),
  (r"Cơ năng của hòn đá", [P(r"Lúc ném $z=0$ nên thế năng bằng $0$, chỉ còn động năng:"), M(r"W=W_\text{d}=\dfrac12mv_0^2=\dfrac12\cdot0{,}40\cdot12^2"), A(r"W=28{,}8\ \text{J}")]),
  (r"Vị trí động năng bằng thế năng", [P(r"$W_\text{d}=W_\text{t}$ nên $W=2W_\text{t}$:"), M(r"W_\text{t}=\dfrac W2=14{,}4\ \text{J}"), M(r"z=\dfrac{W_\text{t}}{mg}=\dfrac{14{,}4}{0{,}40\cdot10}"), A(r"z=3{,}6\ \text{m}")]),
  (r"Động năng ở độ cao $5{,}0$ m", [P(r"Cơ năng vẫn $28{,}8$ J. Thế năng ở độ cao đó:"), M(r"W_\text{t}=mgz=0{,}40\cdot10\cdot5{,}0=20\ \text{J}"), M(r"W_\text{d}=W-W_\text{t}=28{,}8-20"), A(r"W_\text{d}=8{,}8\ \text{J}")]),
  (r"Kiểm tra", [M(r"3{,}6\ \text{m}:\ 14{,}4+14{,}4=28{,}8\ \text{J}"), M(r"5{,}0\ \text{m}:\ 8{,}8+20=28{,}8\ \text{J}"), P(r"Độ cao cực đại là $\dfrac{v_0^2}{2g}=7{,}2$ m, nên cả $3{,}6$ m và $5{,}0$ m đều đạt tới được ✓.")])],
  [r"a) Cơ năng không đổi (chỉ trọng lực sinh công)", r"b) $W=28{,}8\ \text{J}$", r"c) $z=3{,}6\ \text{m}$", r"d) $W_\text{d}=8{,}8\ \text{J}$"],
  r"Nhận dạng: đề <strong>bỏ qua sức cản</strong> và hỏi vị trí có <strong>động năng bằng thế năng</strong> → cơ năng không đổi; $W=2W_\text{t}$."),
 sol(R_4, [
  (r"Cơ năng (mốc ở mặt đất)", [P(r"Ở điểm cao nhất sỏi dừng lại thoáng chốc, $v=0$ nên chỉ có thế năng:"), M(r"W=mgz_\text{max}=0{,}20\cdot10\cdot8{,}0"), A(r"W=16\ \text{J}")]),
  (r"Tốc độ ném", [P(r"Điểm ném cao $3{,}0$ m nên tại đó sỏi có cả động năng và thế năng. Bảo toàn cơ năng:"), M(r"\dfrac12mv_0^2+mgz_0=W"), M(r"\dfrac12\cdot0{,}20\,v_0^2+0{,}20\cdot10\cdot3{,}0=16\ \Rightarrow\ 0{,}10\,v_0^2=10"), M(r"v_0=\sqrt{100}"), A(r"v_0=10\ \text{m/s}")]),
  (r"Vị trí động năng bằng ba lần thế năng", [P(r"$W_\text{d}=3W_\text{t}$ nên $W=W_\text{d}+W_\text{t}=4W_\text{t}$:"), M(r"W_\text{t}=\dfrac W4=4{,}0\ \text{J}"), M(r"z=\dfrac{W_\text{t}}{mg}=\dfrac{4{,}0}{0{,}20\cdot10}"), A(r"z=2{,}0\ \text{m}"), P(r"Vị trí này nằm dưới sân thượng, trên đường sỏi rơi xuống.")]),
  (r"Đổi mốc ở sân thượng", [P(r"Mốc mới ở sân thượng: điểm ném có $z'=0$, điểm cao nhất có $z'_\text{max}=8{,}0-3{,}0=5{,}0$ m."), P(r"Tại điểm ném thế năng bằng $0$, chỉ còn động năng:"), M(r"W'=\dfrac12mv_0^2=\dfrac12\cdot0{,}20\cdot10^2"), A(r"W'=10\ \text{J}"), P(r"Độ cao cực đại so với mốc mới:"), A(r"z'_\text{max}=5{,}0\ \text{m}")]),
  (r"Kiểm tra", [M(r"W'=mgz'_\text{max}=0{,}20\cdot10\cdot5{,}0=10\ \text{J}"), M(r"W-W'=16-10=6{,}0\ \text{J}=0{,}20\cdot10\cdot3{,}0"), P(r"Cơ năng giảm đúng bằng thế năng của sân thượng đối với mốc cũ; tốc độ ném không đổi."), P(r"Tỉ lệ $W_\text{d}=3W_\text{t}$ cũng đổi theo mốc, nên đề phải nói rõ mốc.")])],
  [r"a) $W=16\ \text{J}$", r"b) $v_0=10\ \text{m/s}$", r"c) $z=2{,}0\ \text{m}$", r"d) $W'=10\ \text{J}$ · $z'_\text{max}=5{,}0\ \text{m}$"],
  r"Nhận dạng: <strong>ném từ nơi cao</strong>, biết độ cao cực đại, hỏi tốc độ hoặc vị trí có <strong>động năng gấp n lần thế năng</strong> → $W_1=W_2$, một mốc."),
 sol(R_5, [
  (r"Cơ năng tại $A$", [P(r"Mốc ở chân dốc $B$. Tại $A$ vận động viên xuất phát từ nghỉ nên chỉ có thế năng:"), M(r"W_A=mgz_A=50\cdot10\cdot10"), A(r"W_A=5000\ \text{J}")]),
  (r"Cơ năng tại $B$", [P(r"Tại $B$: $z_B=0$ nên chỉ còn động năng:"), M(r"W_B=\dfrac12mv_B^2=\dfrac12\cdot50\cdot12^2"), A(r"W_B=3600\ \text{J}")]),
  (r"Công của lực cản", [P(r"Có lực cản sinh công nên cơ năng không bảo toàn. Cơ năng sau trừ cơ năng đầu:"), M(r"A_\text{c}=W_B-W_A=3600-5000"), A(r"A_\text{c}=-1400\ \text{J}"), P(r"Công âm: lực cản lấy bớt cơ năng, phần này thành nhiệt.")]),
  (r"Phần trăm cơ năng mất", [M(r"\dfrac{\lvert A_\text{c}\rvert}{W_A}\cdot100\,\%=\dfrac{1400}{5000}\cdot100\,\%"), A(r"28\,\%")]),
  (r"Lượt trượt khác", [P(r"Công của lực cản vẫn là $-1400$ J. Cơ năng ban đầu mới, có cả động năng lẫn thế năng:"), M(r"W_A'=\dfrac12m v_A'^2+mgz_A=\dfrac12\cdot50\cdot5{,}0^2+5000=5625\ \text{J}"), M(r"W_B'=W_A'+A_\text{c}=5625-1400=4225\ \text{J}"), M(r"v_B'=\sqrt{\dfrac{2W_B'}{m}}=\sqrt{\dfrac{2\cdot4225}{50}}=\sqrt{169}"), A(r"v_B'=13\ \text{m/s}")]),
  (r"Kiểm tra", [P(r"Xuất phát nhanh hơn thì xuống chân dốc nhanh hơn: $13\gt12$ ✓."), M(r"\sqrt{5{,}0^2+2\cdot10\cdot10}=\sqrt{225}=15\ \text{m/s}"), P(r"Nếu bỏ qua lực cản thì được $15$ m/s; có lực cản thì nhỏ hơn: $12\lt13\lt15$ ✓.")])],
  [r"a) $W_A=5000\ \text{J}$ · $W_B=3600\ \text{J}$", r"b) $A_\text{c}=-1400\ \text{J}$", r"c) $28\,\%$", r"d) $v_B'=13\ \text{m/s}$"],
  r"Nhận dạng: đề có <strong>ma sát, lực cản</strong> và cho tốc độ ở hai vị trí → cơ năng không bảo toàn, $A_\text{c}=W_\text{sau}-W_\text{đầu}$."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>vị trí, tốc độ</b> và <b>mốc thế năng</b> → nghĩ tới <b>W = ½mv² + mgz</b>, z đo từ mốc.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc(r"Động năng tại $P$", r"Động năng của hòn đá tại $P$ bằng bao nhiêu?", 0.9, "J", 0.02,
       loi=r"Thiếu hệ số $\dfrac12$, hoặc quên bình phương tốc độ."),
  buoc(r"Mốc ở mặt đất", r"Khi chọn mốc ở mặt đất, cơ năng của hòn đá tại $P$ bằng bao nhiêu?", 16.9, "J", 0.1,
       loi=r"Chỉ tính thế năng mà bỏ động năng, hoặc đo độ cao của $P$ từ cửa sổ trong khi mốc là mặt đất.",
       ke=[(r"Cộng động năng với thế năng tính theo độ cao của $P$ so với mặt đất", True),
           (r"Cộng động năng với thế năng tính theo độ cao của $P$ so với cửa sổ", r"Mốc đã chọn là mặt đất nên $z$ phải đo từ mặt đất; cửa sổ chỉ là nơi ném."),
           (r"Lấy thế năng trừ động năng", r"Cơ năng là tổng của động năng và thế năng, không phải hiệu.")]),
  buoc(r"Mốc ở cửa sổ", r"Khi chọn mốc ở cửa sổ, cơ năng của hòn đá tại $P$ bằng bao nhiêu?", 4.9, "J", 0.1,
       loi=r"Giữ nguyên độ cao đo từ mặt đất dù mốc đã dời.",
       ke=[(r"Tính lại độ cao của $P$ so với cửa sổ rồi cộng với động năng", True),
           (r"Giữ độ cao của $P$ đo từ mặt đất vì $P$ không đổi chỗ", r"Vị trí thật không đổi nhưng $z$ đo từ mốc; mốc dời thì $z$ đổi."),
           (r"Giữ nguyên cơ năng vì động năng không đổi", r"Thế năng đổi theo mốc nên cơ năng cũng đổi.")]),
  buoc(r"Mốc ở mái sân thượng", r"Khi chọn mốc ở mái sân thượng, cơ năng của hòn đá tại $P$ bằng bao nhiêu?", -3.1, "J", 0.1,
       loi=r"Tính $z$ của $P$ so với mái nhưng thế sai vào công thức thế năng.",
       ke=[(r"Tính $z$ của $P$ so với mái rồi cộng với động năng", True),
           (r"Lấy $z=+2{,}0$ m vì khoảng cách luôn dương", r"$z$ là toạ độ so với mốc, không phải khoảng cách; điểm nằm dưới mốc thì $z$ mang dấu khác và thế năng cũng vậy."),
           (r"Cho cơ năng bằng động năng vì $P$ ở gần mái", r"Thế năng chỉ bằng $0$ khi $P$ trùng mốc; ở gần mốc vẫn phải tính theo $z$ thật.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>bỏ qua ma sát</b> và <b>độ cao hai vị trí</b> → nghĩ tới <b>W₁ = W₂</b>, khối lượng triệt tiêu.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Cơ năng tại $A$", r"Cơ năng của bi tại $A$ (mốc ở chân máng) bằng bao nhiêu?", 1.225, "J", 0.01,
       loi=r"Đưa khối lượng vào công thức khi chưa đổi gam sang kilôgam."),
  buoc(r"Tốc độ tại $O$", r"Tốc độ của bi tại $O$ bằng bao nhiêu?", 7.0, "m/s", 0.05,
       loi=r"Quên khai căn, hoặc quên hệ số $2$ khi rút tốc độ từ $\dfrac12mv^2$.",
       ke=[(r"Cho cơ năng tại $O$ bằng cơ năng tại $A$; tại $O$ chỉ còn động năng", True),
           (r"Dùng gia tốc $g\sin\alpha$ và độ dài máng để tính", r"Máng cong nên gia tốc đổi liên tục, đề lại không cho độ dài hay hình dạng máng; bảo toàn cơ năng chỉ cần độ cao."),
           (r"Cho thế năng tại $O$ bằng thế năng tại $A$", r"Thế năng phụ thuộc độ cao, mà $A$ và $O$ khác độ cao.")]),
  buoc(r"Tốc độ tại $M$", r"Tốc độ của bi tại $M$ bằng bao nhiêu?", 5.0, "m/s", 0.05,
       loi=r"Bỏ thế năng tại $M$, hoặc dùng sai độ cao khi tính động năng.",
       ke=[(r"Viết cơ năng tại $M$ gồm động năng và thế năng, cho bằng cơ năng tại $A$", True),
           (r"Cho tốc độ tại $M$ bằng nửa tốc độ tại $O$ vì $M$ ở khoảng nửa độ cao", r"Tốc độ không tỉ lệ với độ cao: động năng tỉ lệ với $v^2$ và bằng phần thế năng đã giảm."),
           (r"Bỏ thế năng tại $M$ vì bi đang chuyển động", r"$M$ vẫn cao hơn chân máng nên bi còn thế năng.")]),
  buoc(r"Độ cao của $N$", r"Điểm $N$ cách chân máng bao nhiêu?", 2.0, "m", 0.02,
       loi=r"Dùng $z_N=\dfrac{v_N^2}{2g}$ như thể bi bắt đầu chuyển động từ chân máng.",
       ke=[(r"Viết cơ năng tại $N$ gồm động năng và thế năng, cho bằng cơ năng tại $A$, rồi rút $z_N$", True),
           (r"Dùng $z_N=\dfrac{v_N^2}{2g}$", r"Đại lượng $\dfrac{v_N^2}{2g}$ là phần độ cao đã giảm từ $A$ xuống $N$, chưa phải độ cao của $N$."),
           (r"Cho $z_N=z_A\cdot\dfrac{v_N}{v_O}$", r"Độ cao không tỉ lệ thuận với tốc độ; phải so sánh năng lượng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>bỏ qua sức cản</b> và hỏi <b>động năng bằng thế năng</b> → nghĩ tới <b>W không đổi</b>, W = 2Wt.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Điều kiện áp dụng", r"Khi hòn đá đi lên, cơ năng của nó thay đổi thế nào?",
       loi=r"Cho rằng tốc độ giảm thì cơ năng giảm, quên thế năng tăng bù lại.",
       lua_chon=[(r"Không đổi, vì chỉ trọng lực sinh công trong lúc bay", True),
                 (r"Giảm dần, vì tốc độ của đá giảm dần, nên động năng ít đi", r"Tốc độ giảm làm động năng giảm nhưng thế năng tăng bù lại; cơ năng là tổng của cả hai."),
                 (r"Tăng dần, vì độ cao của đá tăng dần, nên thế năng nhiều lên", r"Độ cao tăng làm thế năng tăng nhưng động năng giảm bù lại; cơ năng không chỉ gồm thế năng.")]),
  buoc(r"Cơ năng của hòn đá", r"Cơ năng của hòn đá (mốc ở mặt đất) bằng bao nhiêu?", 28.8, "J", 0.2,
       loi=r"Thiếu hệ số $\dfrac12$, hoặc quên bình phương tốc độ.",
       ke=[(r"Tính tại lúc ném, nơi $z=0$ nên chỉ còn động năng", True),
           (r"Lấy $W=mgz$ với $z=5{,}0$ m", r"$5{,}0$ m là độ cao của ý d, không phải vị trí ném; lúc ném $z=0$."),
           (r"Lấy $W=mgz$ với độ cao cực đại", r"Đề chưa cho độ cao cực đại; lúc ném đã đủ dữ kiện ($m$, $v_0$, $z=0$) và cơ năng bằng nhau ở mọi vị trí.")]),
  buoc(r"Vị trí động năng bằng thế năng", r"Động năng bằng thế năng ở độ cao nào so với mặt đất?", 3.6, "m", 0.05,
       loi=r"Cho thế năng bằng cả cơ năng, hoặc bằng động năng lúc ném.",
       ke=[(r"Viết $W=2W_\text{t}$ rồi rút $z$ từ $W_\text{t}=mgz$", True),
           (r"Cho $W_\text{d}=0$ để tìm $z$", r"$W_\text{d}=0$ ứng với điểm cao nhất, không phải chỗ động năng bằng thế năng."),
           (r"Dùng $z=\dfrac{v_0^2}{2g}$", r"Đó là độ cao cực đại (nơi $v=0$), không phải chỗ $W_\text{d}=W_\text{t}$.")]),
  buoc(r"Động năng ở độ cao $5{,}0$ m", r"Ở độ cao $5{,}0$ m, động năng của hòn đá bằng bao nhiêu?", 8.8, "J", 0.1,
       loi=r"Dùng động năng lúc ném cho mọi độ cao, hoặc cộng thế năng vào cơ năng.",
       ke=[(r"Lấy cơ năng trừ thế năng tại độ cao đó", True),
           (r"Dùng $W_\text{d}=\dfrac12mv_0^2$ vì tốc độ ném đã cho", r"$v_0$ là tốc độ lúc ném; ở độ cao $5{,}0$ m tốc độ đã giảm nên động năng nhỏ hơn."),
           (r"Cho $W_\text{d}=W_\text{t}$ như ý c", r"Chỉ ở độ cao tìm được ở ý c mới có $W_\text{d}=W_\text{t}$; độ cao khác thì khác.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>ném từ nơi cao</b> và <b>Wđ gấp n lần Wt</b> → nghĩ tới <b>W₁ = W₂</b>, giữ một mốc.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Cơ năng (mốc ở mặt đất)", r"Cơ năng của hòn sỏi (mốc ở mặt đất) bằng bao nhiêu?", 16, "J", 0.2,
       loi=r"Tính thêm động năng ở điểm cao nhất dù sỏi đã dừng lại, hoặc dùng độ cao của sân thượng."),
  buoc(r"Tốc độ ném", r"Tốc độ ném $v_0$ bằng bao nhiêu?", 10, "m/s", 0.1,
       loi=r"Coi sỏi được ném từ mặt đất, quên rằng điểm ném đã cao hơn mốc.",
       ke=[(r"Viết cơ năng tại điểm ném gồm cả động năng và thế năng, cho bằng cơ năng đã tính", True),
           (r"Dùng $v_0=\sqrt{2gz_\text{max}}$ như thả rơi từ độ cao cực đại xuống mặt đất", r"Điểm ném cách mặt đất $3{,}0$ m chứ không ở mặt đất."),
           (r"Cho $v_0=0$ vì sỏi dừng lại ở điểm cao nhất", r"Ở điểm cao nhất $v=0$, còn tại điểm ném $v_0\ne0$; hai vị trí khác nhau.")]),
  buoc(r"Vị trí động năng gấp ba thế năng", r"Độ cao (so với mặt đất) tại đó động năng gấp ba lần thế năng là bao nhiêu?", 2.0, "m", 0.05,
       loi=r"Đảo tỉ lệ (coi thế năng gấp ba động năng), hoặc chia cơ năng cho $3$.",
       ke=[(r"Viết $W=W_\text{d}+W_\text{t}=4W_\text{t}$ rồi rút $z$ từ thế năng", True),
           (r"Cho $W_\text{t}=3W_\text{d}$ rồi rút $z$", r"Đề cho động năng gấp ba lần thế năng: $W_\text{d}=3W_\text{t}$, không phải ngược lại."),
           (r"Cho $z$ bằng một phần ba độ cao cực đại", r"Phải viết $W=W_\text{d}+W_\text{t}$ rồi mới suy ra phần thế năng; độ cao không tự chia theo tỉ lệ của động năng.")]),
  buoc(r"Đổi mốc ở sân thượng", r"Khi chọn mốc ở sân thượng, cơ năng của hòn sỏi bằng bao nhiêu?", 10, "J", 0.2,
       loi=r"Giữ nguyên cơ năng cũ dù mốc đã đổi.",
       ke=[(r"Tính lại $z$ từ mốc mới rồi cộng thế năng với động năng", True),
           (r"Giữ nguyên cơ năng vì sỏi chuyển động như cũ", r"Chuyển động thật không đổi nhưng thế năng đổi theo mốc, nên cơ năng đổi."),
           (r"Cộng thêm thế năng của sân thượng đối với mốc cũ", r"Mốc mới cao hơn mốc cũ nên thế năng tại mỗi điểm giảm đi chứ không tăng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>ma sát, lực cản</b> và cơ năng hai vị trí khác nhau → nghĩ tới <b>ΔW = Ac</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Cơ năng tại $A$", r"Cơ năng của vận động viên tại $A$ (mốc ở chân dốc) bằng bao nhiêu?", 5000, "J", 20,
       loi=r"Tính cả động năng tại $A$ dù xuất phát từ nghỉ, hoặc quên nhân với $g$."),
  buoc(r"Cơ năng tại $B$", r"Cơ năng của vận động viên tại $B$ bằng bao nhiêu?", 3600, "J", 20,
       loi=r"Giữ thế năng của $A$ cho $B$, dù $B$ nằm ngay tại mốc.",
       ke=[(r"Tại chân dốc $z=0$ nên cơ năng chỉ còn động năng", True),
           (r"Cho cơ năng tại $B$ bằng cơ năng tại $A$ vì cơ năng bảo toàn", r"Có lực cản sinh công nên cơ năng không bảo toàn; $W_B$ phải tính riêng từ tốc độ tại $B$."),
           (r"Lấy thế năng của $A$ cộng với động năng tại $B$", r"Thế năng của $A$ không còn ở $B$; tại $B$ thế năng bằng $0$ vì $B$ ở mốc.")]),
  buoc(r"Công của lực cản", r"Công của lực cản trên dốc bằng bao nhiêu?", -1400, "J", 10,
       loi=r"Lấy cơ năng đầu trừ cơ năng sau nên mất dấu của công cản.",
       ke=[(r"Lấy cơ năng sau trừ cơ năng đầu", True),
           (r"Lấy cơ năng đầu trừ cơ năng sau", r"Độ biến thiên cơ năng luôn là sau trừ đầu; đảo lại thì sai dấu của công cản."),
           (r"Cho công cản bằng $0$ vì vận động viên vẫn tăng tốc", r"Tốc độ tăng vì công dương của trọng lực lớn hơn công âm của lực cản; lực cản vẫn sinh công.")]),
  buoc(r"Phần trăm cơ năng mất", r"Lực cản đã lấy đi bao nhiêu phần trăm cơ năng ban đầu?", 28, "%", 0.5,
       loi=r"Chia cho cơ năng ở chân dốc thay vì cơ năng ban đầu.",
       ke=[(r"Chia độ lớn công cản cho cơ năng ban đầu", True),
           (r"Chia độ lớn công cản cho cơ năng ở chân dốc", r"Phần trăm mất tính so với lúc đầu, không phải so với lúc cuối."),
           (r"Lấy $W_B$ chia $W_A$ rồi gọi đó là phần mất", r"Thương đó là phần còn lại, không phải phần đã mất.")]),
  buoc(r"Lượt trượt khác", r"Ở lượt trượt khác, tốc độ ở chân dốc bằng bao nhiêu?", 13.0, "m/s", 0.1,
       loi=r"Dùng lại tốc độ của lượt trước, hoặc bỏ lực cản vì lượt này nhanh hơn.",
       ke=[(r"Tính cơ năng đầu mới, cộng công cản cũ, rồi rút tốc độ từ động năng ở chân dốc", True),
           (r"Dùng $A_\text{c}=-1400$ J nhưng lấy cơ năng đầu cũ ($5000$ J)", r"Lượt này qua $A$ với tốc độ khác nên cơ năng đầu khác; phải tính lại cơ năng tại $A$ rồi mới cộng công cản."),
           (r"Cộng $5{,}0$ m/s vào tốc độ của lượt trước", r"Tốc độ không cộng như vậy; động năng tỉ lệ với bình phương tốc độ nên phải cộng năng lượng rồi mới suy tốc độ.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập, xếp dễ → khó ═════════════
def _examples():
    ex = {}
    for mi, q in enumerate(OLD):
        parts = re.split(r'(?=<p class="text-base leading-relaxed my-2"><strong class="font-bold">Ví dụ \d+\.)', q["body_html"])
        fig = re.search(r"<figure.*?</figure>", parts[0], flags=re.S)
        for p in parts[1:]:
            m_ = re.match(r'<p class="text-base leading-relaxed my-2"><strong class="font-bold">Ví dụ (\d+)\.</strong>(.*?)</p>(.*)$', p, flags=re.S)
            n, de, loi = m_.groups()
            assert "Lời giải:" in loi
            ex[(mi, int(n))] = (de.strip(), loi.strip(), fig.group(0) if fig else "")
    return ex
EX = _examples()
assert len(EX) == 17
ORDER = [((0, 4), "Dễ", False), ((0, 1), "Dễ", False), ((0, 5), "Dễ", False), ((0, 6), "Trung bình", False),
         ((1, 1), "Trung bình", True), ((2, 1), "Trung bình", True), ((2, 2), "Trung bình", False),
         ((0, 12), "Khó", False), ((1, 2), "Khó", False), ((0, 11), "Nâng cao", False)]

def _decimals(h):
    """Dấu phẩy thập phân trong $…$ → {,} (KaTeX không chèn khoảng trắng sau dấu phẩy)."""
    return re.sub(r"\$[^$]+\$", lambda m_: re.sub(r"(?<=\d),(?=\d)", "{,}", m_.group(0)), h)

def _fmt(h):
    """Trong $…$: đơn vị `\\,m` → `\\text{m}`; dấu nhân '.' → `\\cdot`."""
    def f(m_):
        t = m_.group(0)
        t = re.sub(r"\\,(m/s\^2|m/s|kg|cm|m|N|J|g)(?![A-Za-z=])", lambda u: r"\ \text{" + u.group(1).replace("^2", "") + "}" + ("^2" if "^2" in u.group(1) else ""), t)
        t = re.sub(r"\.", r"\\cdot ", t)
        return t
    return re.sub(r"\$[^$]+\$", f, h)

parts_tl = []
for k, (key, muc, with_fig) in enumerate(ORDER, 1):
    de, loi, fig = EX[key]
    if key == (0, 4):
        de = de.replace("Ước lượng tốc độ khi chạm nước.", "Lấy $g=9,8\\,m/s^2$. Ước lượng tốc độ khi chạm nước.")
        assert "Lấy $g=9,8" in de
        a_ = r"W_d=W_t \Leftrightarrow \dfrac12mv^2=mgh"
        assert a_ in loi
        loi = loi.replace("Bảo toàn cơ năng:", "Bảo toàn cơ năng giữa đỉnh (1) và lúc chạm nước (2):", 1).replace(a_, r"W_{t1}=W_{d2} \Leftrightarrow mgh=\dfrac12mv^2")
    if key == (0, 5):
        de = de.replace("Cơ năng của em bé có bảo toàn không?", "Lấy $g=9,8\\,m/s^2$. Cơ năng của em bé có bảo toàn không?")
        assert "Lấy $g=9,8" in de
    de, loi = _fmt(_decimals(de)), _fmt(_decimals(loi))
    loi = loi.replace("=&gt;", r"\Rightarrow ")
    parts_tl.append(f'<h4>Bài {k} · {muc}</h4><p><strong>Bài {k}.</strong> {de}</p>' + (fig if with_fig else "")
                    + f'<details><summary>Hướng dẫn giải</summary>{loi}</details>')
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts_tl))

write(J, 71, "Bài 26. Cơ năng và định luật bảo toàn cơ năng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
