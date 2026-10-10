"""Bài 78 — "Bài 33. Biến dạng của vật rắn" (Vật lí 10, chương 7). 5 dạng, không có tự luận (bài chưa có ví dụ cũ).
Mẫu: build-hinh-57.py / 58. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-78.py  → ghi scripts/data/bai-tap-mau/78.json
Dạng theo quét: scripts/logs/batch-ra-soat/ket-qua/78.quet-dang.json (5 dạng, cấp 1,1,2,3,4). Hình: hinh_78.py.
Quy ước: g = 10 m/s²; lò xo nhẹ, luôn trong giới hạn đàn hồi; ký hiệu như lý thuyết bài 33 (F_đh, Δl, l₀, l, k)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_78 import BUILD, D1_L, D2_K, D2_F, D2_DL, D4_K, D4_M, D4_L0, D4_L1, D5_K, D5_L0, D5_M1, D5_M2, D5_L1, D5_L2

J = os.path.join(HERE, "78.json")
T150, T151 = "Biến dạng kéo, nén và giới hạn đàn hồi", "Định luật Hooke và lực đàn hồi của lò xo"
g0 = 10.0

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị và mọi cách sai cho kết quả khác ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"

# D1 — bảng của đề (đồng bộ với hình)
F1s = [2, 4, 6, 8, 10]; l1s = [22, 24, 26, 28, 33]; lp1 = [20, 20, 20, 20, 22]; L01 = 20
assert [D1_L[f] for f in F1s] == l1s and D1_L[0] == L01
dep = [f for f, lp in zip(F1s, lp1) if lp != L01]; assert dep == [10]                     # chỉ lần 10 N bị dẻo
ela = max(f for f, lp in zip(F1s, lp1) if lp == L01); assert ela == 8
assert all(l - L01 == f for f, l in zip(F1s[:4], l1s[:4])) and l1s[4] - L01 != 10         # vùng tỉ lệ 1 cm/N, 10 N lệch
ok("D1 kiểm tra", L01 + 10, 30, 1e-9); assert l1s[4] > 30
assert len({ela, max(F1s), min(F1s)}) == 3                                               # các cách sai cho kết quả khác 8 N
# D2
k2 = D2_F / D2_DL; ok("D2 k", k2, 150, 1e-9); ok("k2 const", k2, D2_K, 1e-9)
ok("D2 b", 9.0 / k2 * 100, 6.0, 1e-9); ok("D2 c", k2 * 0.020, 3.0, 1e-9)
ok("D2 kiểm", 6.0 / 4.0, 3.0 / 2.0, 1e-9); ok("D2 kiểm 2", 9.0 / 6.0, 1.5, 1e-9)
assert abs(D2_F * D2_DL - k2) > 100 and abs(D2_DL / D2_F - k2) > 100                       # k = F·Δl; k = Δl/F
assert 4.0 + (9.0 - 6.0) != 6.0 and abs(k2 * 2.0 - 3.0) > 100 and abs(k2 / 0.020 - 3.0) > 100   # cộng 3 cm; thế 2,0 cm chưa đổi; k/Δl
# D3
k3, l03 = 120.0, 24.0
d1c = 3.6 / k3 * 100; ok("D3 Δl kéo", d1c, 3.0, 1e-9); ok("D3 l kéo", l03 + d1c, 27, 1e-9)
d2c = 4.8 / k3 * 100; ok("D3 Δl nén", d2c, 4.0, 1e-9); ok("D3 l nén", l03 - d2c, 20, 1e-9)
d3c = 30 - l03; ok("D3 Δl c", d3c, 6.0, 1e-9); ok("D3 F c", k3 * d3c / 100, 7.2, 1e-9)
assert len({round(x, 4) for x in (l03 + d1c, d1c, l03 - d1c, l03 + d2c, l03 - d2c, d2c)}) == 6 and l03 - d2c != l03 + d1c
assert abs(k3 * 0.30 - 7.2) > 20 and abs(k3 * 0.24 - 7.2) > 20 and abs(k3 * d3c - 7.2) > 100 and l03 + d1c != l03 + d2c
ok("D3 kiểm tỉ lệ", 7.2 / 3.6, d3c / d1c, 1e-9)
# D4
F4 = D4_M * g0; ok("D4 F", F4, 1.2, 1e-9); dl4 = D4_L1 - D4_L0; ok("D4 Δl", dl4, 3.0, 1e-9)
k4 = F4 / (dl4 / 100); ok("D4 k", k4, 40, 1e-9); ok("k4 const", k4, D4_K, 1e-9)
m4b = 0.120 + 0.080; F4b = m4b * g0; ok("D4 F'", F4b, 2.0, 1e-9); dl4b = F4b / k4 * 100; ok("D4 Δl'", dl4b, 5.0, 1e-9); l4b = D4_L0 + dl4b; ok("D4 l'", l4b, 25, 1e-9)
dl4c = 32 - D4_L0; ok("D4 Δl''", dl4c, 12, 1e-9); F4c = k4 * dl4c / 100; ok("D4 F''", F4c, 4.8, 1e-9); m4c = F4c / g0 * 1000; ok("D4 m''", m4c, 480, 1e-9)
add4 = m4c - 120; ok("D4 thêm", add4, 360, 1e-9)
assert len({round(x, 3) for x in (k4, F4 / 0.23, F4 / 0.20)}) == 3                          # k sai: chia cho l; cho l₀
assert len({round(x, 2) for x in (l4b, D4_L0 + 0.8 / k4 * 100, D4_L1, dl4b)}) == 4          # chỉ 80 g; giữ 3 cm; độ dãn thành chiều dài
assert len({round(x, 1) for x in (m4c, 120 * 32 / D4_L1, k4 * 0.32 / g0 * 1000)}) == 3      # tỉ lệ 32/23; thế 32 cm là độ dãn
assert len({round(x, 1) for x in (add4, m4c, m4c + 120)}) == 3
ok("D4 kiểm", 120 / 3, 200 / 5, 1e-9); ok("D4 kiểm 2", 480 / 12, 40, 1e-9); ok("D4 kiểm 3", 120 / (dl4), 40, 1e-9)
assert D4_L0 == 20
# D5
F5a, F5b = D5_M1 * g0, D5_M2 * g0; ok("D5 F1", F5a, 1.6, 1e-9); ok("D5 F2", F5b, 4.8, 1e-9); dF = F5b - F5a; ok("D5 ΔF", dF, 3.2, 1e-9)
dl5 = (D5_L2 - D5_L1) / 100; ok("D5 hiệu l", dl5, 0.04, 1e-9); k5 = dF / dl5; ok("D5 k", k5, 80, 1e-9); ok("k5 const", k5, D5_K, 1e-9)
d51 = F5a / k5 * 100; ok("D5 Δl1", d51, 2.0, 1e-9); l05 = D5_L1 - d51; ok("D5 l0", l05, 22, 1e-9); ok("l05 const", l05, D5_L0, 1e-9)
ok("D5 l2 kiểm", l05 + F5b / k5 * 100, 28, 1e-9)
l5c = l05 + (0.400 * g0) / k5 * 100; ok("D5 l3", l5c, 27, 1e-9)
assert len({round(x, 2) for x in (k5, F5b / (D5_L2 / 100), F5a / dl5, dF / D5_L1)}) == 4   # lực sau/chiều dài; lực đầu/hiệu dài; chia cho chiều dài đầu
assert len({round(x, 2) for x in (d51, dl5 * 100, D5_L1)}) == 3 and len({round(x, 2) for x in (l05, D5_L1, dl5 * 100)}) == 3
assert len({round(x, 2) for x in (l5c, l05 + d51, l05 + F5b / k5 * 100)}) == 3


# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Nhận biết biến dạng kéo, nén, đàn hồi, dẻo và giới hạn đàn hồi", topic=T150,
      problem_html=r"""<p>Một lò xo có chiều dài tự nhiên $20\ \text{cm}$, một đầu gắn vào tường. Tác dụng lên đầu còn lại một lực kéo hướng ra xa tường, độ lớn $F$ tăng dần qua năm lần thử. Mỗi lần thử, đọc chiều dài $l$ khi có lực, rồi thôi lực và đọc chiều dài $l'$ của lò xo:</p>
<div class="table-scroll"><table class="tl-table"><thead><tr><th>$F$ (N)</th><th>$2$</th><th>$4$</th><th>$6$</th><th>$8$</th><th>$10$</th></tr></thead><tbody>
<tr><td>$l$ (cm), khi có lực</td><td>$22$</td><td>$24$</td><td>$26$</td><td>$28$</td><td>$33$</td></tr>
<tr><td>$l'$ (cm), sau khi thôi lực</td><td>$20$</td><td>$20$</td><td>$20$</td><td>$20$</td><td>$22$</td></tr></tbody></table></div>
<ol type="a"><li>Lò xo chịu biến dạng kéo hay biến dạng nén?</li>
<li>Ở lần thử nào lò xo bị biến dạng dẻo?</li>
<li>Trong các lần thử, lực lớn nhất mà lò xo còn đàn hồi bằng bao nhiêu? Giới hạn đàn hồi của lò xo nằm trong khoảng nào?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Định luật Hooke: tìm độ cứng, độ dãn và lực", topic=T151,
      problem_html=r"""<p>Một lò xo nhẹ nằm ngang, một đầu cố định. Kéo đầu còn lại bằng lực $6{,}0\ \text{N}$ thì lò xo dãn thêm $4{,}0\ \text{cm}$. Lò xo luôn trong giới hạn đàn hồi.</p>
<ol type="a"><li>Tính độ cứng $k$ của lò xo.</li>
<li>Kéo bằng lực $9{,}0\ \text{N}$ thì lò xo dãn thêm bao nhiêu xentimét?</li>
<li>Muốn lò xo dãn thêm $2{,}0\ \text{cm}$ thì phải kéo bằng lực bao nhiêu?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Chiều dài của lò xo khi bị kéo dãn hoặc bị nén", topic=T151,
      problem_html=r"""<p>Một lò xo nhẹ nằm ngang, một đầu gắn vào tường, chiều dài tự nhiên $24\ \text{cm}$, độ cứng $120\ \text{N/m}$. Lò xo luôn trong giới hạn đàn hồi.</p>
<ol type="a"><li>Tính chiều dài của lò xo khi tác dụng lên đầu tự do một lực kéo $3{,}6\ \text{N}$ dọc theo trục lò xo.</li>
<li>Tính chiều dài của lò xo khi tác dụng lên đầu tự do một lực đẩy $4{,}8\ \text{N}$ dọc theo trục, hướng về phía tường.</li>
<li>Muốn lò xo dài $30\ \text{cm}$ thì phải tác dụng lực kéo bao nhiêu?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Lò xo treo vật đứng yên: tìm độ cứng, chiều dài và khối lượng", topic=T151,
      problem_html=r"""<p>Một lò xo nhẹ có chiều dài tự nhiên $20\ \text{cm}$, treo thẳng đứng, đầu trên cố định. Treo vào đầu dưới một vật khối lượng $120\ \text{g}$; khi vật đứng yên, lò xo dài $23\ \text{cm}$. Lấy $g=10\ \text{m/s}^2$, lò xo luôn trong giới hạn đàn hồi.</p>
<ol type="a"><li>Tính độ cứng $k$ của lò xo.</li>
<li>Treo thêm vào vật đó một vật $80\ \text{g}$ nữa. Khi đứng yên, lò xo dài bao nhiêu?</li>
<li>Phải treo thêm bao nhiêu gam nữa (so với vật $120\ \text{g}$ ban đầu) để lò xo dài $32\ \text{cm}$?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Bài ngược: biết hai chiều dài, tìm chiều dài tự nhiên và độ cứng", topic=T151,
      problem_html=r"""<p>Một lò xo nhẹ treo thẳng đứng, đầu trên cố định. Treo vào đầu dưới vật khối lượng $160\ \text{g}$, khi đứng yên lò xo dài $24\ \text{cm}$. Treo thêm một vật nữa để tổng khối lượng treo là $480\ \text{g}$, khi đứng yên lò xo dài $28\ \text{cm}$. Lấy $g=10\ \text{m/s}^2$, lò xo luôn trong giới hạn đàn hồi. Chưa biết chiều dài tự nhiên và độ cứng của lò xo.</p>
<ol type="a"><li>Tính độ cứng $k$.</li>
<li>Tính chiều dài tự nhiên $l_0$.</li>
<li>Nếu chỉ treo vật $400\ \text{g}$ thì lò xo dài bao nhiêu?</li></ol>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“lò xo có chiều dài tự nhiên $20$ cm, một đầu gắn vào tường”", r"$l_0=20\ \text{cm}$", r"⚠ Chiều dài tự nhiên là chiều dài khi chưa có lực, dùng làm mốc để so sánh"),
  (r"“lực kéo hướng ra xa tường”", r"Lực hướng ra ngoài lò xo", r"Hướng của cặp lực cho biết biến dạng kéo hay nén"),
  (r"“đọc chiều dài $l$ khi có lực”", r"$l=22;\ 24;\ 26;\ 28;\ 33\ \text{cm}$", r"Chiều dài lúc đang chịu lực"),
  (r"“thôi lực và đọc chiều dài $l'$”", r"$l'=20;\ 20;\ 20;\ 20;\ 22\ \text{cm}$", r"⚠ Đàn hồi hay dẻo chỉ xét sau khi thôi lực"),
  (r"“a) kéo hay nén”", r"Cần loại biến dạng", r"Đại lượng cần tìm"),
  (r"“b) lần thử nào bị biến dạng dẻo”", r"Cần lần thử ($F$, N)", r"Đại lượng cần tìm"),
  (r"“c) lực lớn nhất còn đàn hồi … giới hạn đàn hồi”", r"Cần $F$ (N) và khoảng của giới hạn", r"Giới hạn đàn hồi: mức lực lớn nhất mà vật còn đàn hồi")],
 [(r"“lò xo nhẹ nằm ngang, một đầu cố định”", r"Lò xo đứng yên khi kéo", r"⚠ Lực kéo cân bằng với lực đàn hồi của lò xo"),
  (r"“kéo bằng lực $6{,}0$ N … dãn thêm $4{,}0$ cm”", r"$F=6{,}0\ \text{N}$; $\left|\Delta l\right|=4{,}0\ \text{cm}$", r"Đơn vị trong công thức: N, m, N/m"),
  (r"“luôn trong giới hạn đàn hồi”", r"Hooke dùng được", r"⚠ Định luật Hooke chỉ đúng trong giới hạn đàn hồi"),
  (r"“a) độ cứng $k$”", r"Cần $k$ (N/m)", r"Định luật Hooke"),
  (r"“b) kéo bằng lực $9{,}0$ N … dãn thêm bao nhiêu xentimét”", r"$F'=9{,}0\ \text{N}$; cần $\left|\Delta l'\right|$ (cm)", r"Độ cứng thuộc về lò xo"),
  (r"“c) dãn thêm $2{,}0$ cm … lực”", r"$\left|\Delta l''\right|=2{,}0\ \text{cm}$; cần $F''$ (N)", r"Định luật Hooke")],
 [(r"“lò xo nhẹ nằm ngang, một đầu gắn vào tường”", r"Lò xo nhẹ, một đầu cố định", r"⚠ Lực kéo (đẩy) cân bằng với lực đàn hồi; bỏ qua khối lượng lò xo"),
  (r"“chiều dài tự nhiên $24$ cm”", r"$l_0=24\ \text{cm}$", r"⚠ $\left|\Delta l\right|=\left|l-l_0\right|$: độ biến dạng khác chiều dài $l$"),
  (r"“độ cứng $120$ N/m”", r"$k=120\ \text{N/m}$", r"Độ cứng thuộc về lò xo"),
  (r"“luôn trong giới hạn đàn hồi”", r"Hooke dùng được", r"⚠ Định luật Hooke chỉ đúng trong giới hạn đàn hồi"),
  (r"“a) lực kéo $3{,}6$ N”", r"$F_1=3{,}6\ \text{N}$; cần $l_1$", r"Biến dạng kéo"),
  (r"“b) lực đẩy $4{,}8$ N hướng về phía tường”", r"$F_2=4{,}8\ \text{N}$; cần $l_2$", r"Biến dạng nén"),
  (r"“c) dài $30$ cm … lực kéo”", r"$l_3=30\ \text{cm}$; cần $F_3$ (N)", r"Định luật Hooke")],
 [(r"“lò xo nhẹ … treo thẳng đứng, đầu trên cố định”", r"Đầu dưới chỉ chịu lực của vật treo", r"⚠ Lò xo nhẹ: bỏ qua khối lượng lò xo"),
  (r"“chiều dài tự nhiên $20$ cm”", r"$l_0=20\ \text{cm}$", r"Mốc để tính độ biến dạng"),
  (r"“treo vật $120$ g; khi vật đứng yên, lò xo dài $23$ cm”", r"$m_1=120\ \text{g}$; $l_1=23\ \text{cm}$", r"⚠ Vật đứng yên: các lực tác dụng lên vật cân bằng"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng $P=mg$"),
  (r"“luôn trong giới hạn đàn hồi”", r"Hooke dùng được cho cả ba ý", r"⚠ Định luật Hooke chỉ đúng trong giới hạn đàn hồi"),
  (r"“a) độ cứng $k$”", r"Cần $k$ (N/m)", r"Đại lượng cần tìm"),
  (r"“b) treo thêm vật $80$ g nữa”", r"$m_2=80\ \text{g}$ (vật thêm); cần $l'$", r"Khối lượng treo lúc này"),
  (r"“c) treo thêm bao nhiêu gam để lò xo dài $32$ cm”", r"$l''=32\ \text{cm}$; cần khối lượng treo thêm (g)", r"Đại lượng cần tìm")],
 [(r"“lò xo nhẹ treo thẳng đứng, đầu trên cố định”", r"Đầu dưới chỉ chịu lực của vật treo", r"⚠ Lò xo nhẹ: bỏ qua khối lượng lò xo"),
  (r"“vật $160$ g, khi đứng yên lò xo dài $24$ cm”", r"$m_1=160\ \text{g}$; $l_1=24\ \text{cm}$", r"⚠ Vật đứng yên: các lực tác dụng lên vật cân bằng"),
  (r"“tổng khối lượng treo là $480$ g … dài $28$ cm”", r"$m_2=480\ \text{g}$ (tổng); $l_2=28\ \text{cm}$", r"Dữ kiện của lần treo thứ hai"),
  (r"“chưa biết chiều dài tự nhiên và độ cứng”", r"$l_0$ và $k$ chưa biết", r"Hai ẩn chưa biết"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng $P=mg$"),
  (r"“a) độ cứng $k$; b) chiều dài tự nhiên $l_0$”", r"Cần $k$ (N/m), $l_0$ (cm)", r"Đại lượng cần tìm"),
  (r"“c) chỉ treo vật $400$ g … dài bao nhiêu”", r"$m_3=400\ \text{g}$; cần $l_3$ (cm)", r"Đại lượng cần tìm")],
]

# ═════════════ Lời giải từng bước ═════════════
R_BD = [r"<strong>Biến dạng kéo:</strong> cặp lực hướng ra ngoài vật, vật dài ra.",
        r"<strong>Biến dạng nén:</strong> cặp lực hướng vào trong vật, vật ngắn lại.",
        r"<strong>Đàn hồi:</strong> thôi lực, vật trở lại hình dạng, kích thước ban đầu. <strong>Dẻo:</strong> thôi lực, vật không trở lại như cũ.",
        r"<strong>Giới hạn đàn hồi:</strong> mức lực lớn nhất mà vật còn đàn hồi; vượt qua thì biến dạng thành dẻo.",
        r"⚠ <strong>Điều kiện:</strong> đàn hồi hay dẻo chỉ xét sau khi thôi lực, so với chiều dài ban đầu $l_0$."]
R_HK = [r"<strong>Lực đàn hồi</strong> xuất hiện khi lò xo biến dạng, ngược chiều biến dạng; lò xo đứng yên thì lực kéo (đẩy) cân bằng với nó.",
        r"<strong>Định luật Hooke:</strong> $F_{\text{đh}}=k\left|\Delta l\right|$.",
        r"Đơn vị: $F_{\text{đh}}$ (N), $\Delta l$ (m), $k$ (N/m).",
        r"$k$ thuộc về lò xo, không đổi khi lực đổi.",
        r"⚠ <strong>Điều kiện:</strong> chỉ trong giới hạn đàn hồi."]
R_L = [r"<strong>Lực đàn hồi</strong> xuất hiện khi lò xo biến dạng; lò xo đứng yên thì lực kéo (đẩy) cân bằng với nó.",
       r"<strong>Định luật Hooke:</strong> $F_{\text{đh}}=k\left|\Delta l\right|$; $F$ (N), $\Delta l$ (m), $k$ (N/m).",
       r"$\left|\Delta l\right|=\left|l-l_0\right|$: phần dài thêm hoặc ngắn đi, không phải chiều dài $l$.",
       r"Lò xo bị kéo: $l=l_0+\left|\Delta l\right|$.",
       r"Lò xo bị nén: $l=l_0-\left|\Delta l\right|$.",
       r"⚠ <strong>Điều kiện:</strong> chỉ trong giới hạn đàn hồi."]
R_TR = [r"<strong>Lò xo nhẹ treo vật đứng yên:</strong> lực đàn hồi cân bằng với trọng lượng, $F_{\text{đh}}=P=mg$.",
        r"<strong>Định luật Hooke:</strong> $F_{\text{đh}}=k\left|\Delta l\right|$; $F$ (N), $\Delta l$ (m), $k$ (N/m).",
        r"$\left|\Delta l\right|=\left|l-l_0\right|$; treo vật thì lò xo dãn: $l=l_0+\left|\Delta l\right|$.",
        r"⚠ <strong>Điều kiện:</strong> lò xo nhẹ, trong giới hạn đàn hồi."]

SOLS = [
 sol(R_BD, [
  (r"Loại biến dạng", [P(r"Lực kéo hướng ra xa tường, tức hướng ra ngoài lò xo; lò xo dài ra từ $20\ \text{cm}$."), A(r"T:<strong>Biến dạng kéo</strong>")]),
  (r"Lần thử bị biến dạng dẻo", [P(r"Sau khi thôi lực, so $l'$ với chiều dài ban đầu $l_0=20\ \text{cm}$."),
                                  P(r"$F=2;\ 4;\ 6;\ 8\ \text{N}$: $l'=20\ \text{cm}$, trở về đúng chiều dài cũ: <strong>đàn hồi</strong>."),
                                  P(r"$F=10\ \text{N}$: $l'=22\ \text{cm}\ne20\ \text{cm}$, không trở về như cũ: <strong>dẻo</strong>."), A(r"T:Lần thử $F=10\ \text{N}$")]),
  (r"Lực lớn nhất còn đàn hồi", [P(r"Trong các lần có $l'=20\ \text{cm}$, lực lớn nhất là lần thứ tư."), A(r"F=8\ \text{N}")]),
  (r"Khoảng của giới hạn đàn hồi", [P(r"Ở $8\ \text{N}$ lò xo còn đàn hồi, nên giới hạn không nhỏ hơn $8\ \text{N}$."),
                                    P(r"Ở $10\ \text{N}$ lò xo đã dẻo, nên giới hạn nhỏ hơn $10\ \text{N}$."),
                                    P(r"Chưa thử lực nằm giữa hai giá trị, nên chỉ chặn được một khoảng:"), A(r"T:$8\ \text{N}\le$ giới hạn đàn hồi $\lt10\ \text{N}$")]),
  (r"Kiểm tra", [P(r"Từ $2$ đến $8\ \text{N}$, cứ $1\ \text{N}$ lò xo dài thêm $1\ \text{cm}$."), M(r"l=20+10=30\ \text{cm}\quad(\text{nếu còn tỉ lệ ở }10\ \text{N})"),
                 P(r"Thực tế $l=33\ \text{cm}\gt30\ \text{cm}$: không còn tỉ lệ, khớp với biến dạng dẻo ✓.")])],
  [r"a) Biến dạng kéo", r"b) Lần thử $F=10\ \text{N}$", r"c) Lực lớn nhất còn đàn hồi: $8\ \text{N}$; $8\ \text{N}\le$ giới hạn đàn hồi $\lt10\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>bảng chiều dài khi có lực và sau khi thôi lực</strong> → so chiều dài sau khi thôi lực với $l_0$ để biết đàn hồi hay dẻo."),
 sol(R_HK, [
  (r"Đổi độ dãn ra mét", [M(r"\left|\Delta l\right|=4{,}0\ \text{cm}=0{,}040\ \text{m}")]),
  (r"Độ cứng", [P(r"Lò xo đứng yên nên lực kéo cân bằng với lực đàn hồi:"), M(r"F_{\text{đh}}=F=6{,}0\ \text{N}"),
                M(r"k=\dfrac{F_{\text{đh}}}{\left|\Delta l\right|}=\dfrac{6{,}0}{0{,}040}"), A(r"k=150\ \text{N/m}")]),
  (r"Độ dãn khi kéo $9{,}0\ \text{N}$", [P(r"Cùng lò xo nên $k=150\ \text{N/m}$:"), M(r"\left|\Delta l'\right|=\dfrac{F'}{k}=\dfrac{9{,}0}{150}=0{,}060\ \text{m}"), A(r"\left|\Delta l'\right|=6{,}0\ \text{cm}")]),
  (r"Lực khi dãn thêm $2{,}0\ \text{cm}$", [M(r"\left|\Delta l''\right|=2{,}0\ \text{cm}=0{,}020\ \text{m}"), M(r"F''=k\left|\Delta l''\right|=150\cdot0{,}020"), A(r"F''=3{,}0\ \text{N}")]),
  (r"Kiểm tra", [M(r"\dfrac{F}{\left|\Delta l\right|}=\dfrac{6{,}0}{4{,}0}=\dfrac{9{,}0}{6{,}0}=\dfrac{3{,}0}{2{,}0}=1{,}5\ \text{N/cm}"),
                 P(r"Ba cặp (lực, độ dãn) có cùng tỉ số, đúng tính tỉ lệ thuận ✓.")])],
  [r"a) $k=150\ \text{N/m}$", r"b) $\left|\Delta l'\right|=6{,}0\ \text{cm}$", r"c) $F''=3{,}0\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>lực và độ dãn (cm) của lò xo</strong> → dùng $F_{\text{đh}}=k\left|\Delta l\right|$, đổi cm ra m trước khi thế."),
 sol(R_L, [
  (r"Độ dãn khi kéo", [P(r"Lò xo đứng yên nên lực kéo cân bằng với lực đàn hồi:"), M(r"F_{\text{đh}}=F_1=3{,}6\ \text{N}"),
                       M(r"\left|\Delta l_1\right|=\dfrac{F_{\text{đh}}}{k}=\dfrac{3{,}6}{120}=0{,}030\ \text{m}"), A(r"\left|\Delta l_1\right|=3{,}0\ \text{cm}")]),
  (r"Chiều dài khi kéo", [P(r"Bị kéo nên lò xo dài hơn chiều dài tự nhiên:"), M(r"l_1=l_0+\left|\Delta l_1\right|=24+3{,}0"), A(r"l_1=27\ \text{cm}")]),
  (r"Chiều dài khi nén", [M(r"\left|\Delta l_2\right|=\dfrac{F_2}{k}=\dfrac{4{,}8}{120}=0{,}040\ \text{m}=4{,}0\ \text{cm}"),
                          P(r"Bị nén nên lò xo ngắn hơn chiều dài tự nhiên:"), M(r"l_2=l_0-\left|\Delta l_2\right|=24-4{,}0"), A(r"l_2=20\ \text{cm}")]),
  (r"Lực kéo để lò xo dài $30\ \text{cm}$", [P(r"Lò xo dài $30\ \text{cm}$ lớn hơn $l_0$ nên bị kéo dãn:"), M(r"\left|\Delta l_3\right|=l_3-l_0=30-24=6{,}0\ \text{cm}=0{,}060\ \text{m}"),
                                              M(r"F_3=k\left|\Delta l_3\right|=120\cdot0{,}060"), A(r"F_3=7{,}2\ \text{N}")]),
  (r"Kiểm tra", [P(r"$l_2=20\ \text{cm}\lt l_0=24\ \text{cm}\lt l_1=27\ \text{cm}$: nén thì ngắn đi, kéo thì dài ra ✓."),
                 P(r"Lực $7{,}2\ \text{N}$ gấp đôi $3{,}6\ \text{N}$ nên độ dãn gấp đôi ($6{,}0\ \text{cm}$ so với $3{,}0\ \text{cm}$) ✓.")])],
  [r"a) $l_1=27\ \text{cm}$", r"b) $l_2=20\ \text{cm}$", r"c) $F_3=7{,}2\ \text{N}$"],
  r"Nhận dạng: đề hỏi <strong>chiều dài lò xo</strong> khi kéo hoặc nén → tìm $\left|\Delta l\right|$ bằng Hooke, rồi cộng (kéo) hoặc trừ (nén) với $l_0$."),
 sol(R_TR, [
  (r"Lực đàn hồi khi vật $120\ \text{g}$ đứng yên", [P(r"Vật đứng yên nên lực đàn hồi cân bằng với trọng lượng:"), M(r"F_{\text{đh}}=P=mg=0{,}120\cdot10"), A(r"F_{\text{đh}}=1{,}2\ \text{N}")]),
  (r"Độ cứng", [M(r"\left|\Delta l\right|=l-l_0=23-20=3{,}0\ \text{cm}=0{,}030\ \text{m}"), M(r"k=\dfrac{F_{\text{đh}}}{\left|\Delta l\right|}=\dfrac{1{,}2}{0{,}030}"), A(r"k=40\ \text{N/m}")]),
  (r"Chiều dài khi treo thêm $80\ \text{g}$", [P(r"Lò xo chịu cả hai vật, khối lượng cộng dồn:"), M(r"m'=120+80=200\ \text{g}=0{,}200\ \text{kg}"), M(r"F'=m'g=0{,}200\cdot10=2{,}0\ \text{N}"),
                                               M(r"\left|\Delta l'\right|=\dfrac{F'}{k}=\dfrac{2{,}0}{40}=0{,}050\ \text{m}=5{,}0\ \text{cm}"),
                                               M(r"l'=l_0+\left|\Delta l'\right|=20+5{,}0"), A(r"l'=25\ \text{cm}")]),
  (r"Tổng khối lượng để lò xo dài $32\ \text{cm}$", [M(r"\left|\Delta l''\right|=32-20=12\ \text{cm}=0{,}12\ \text{m}"), M(r"F''=k\left|\Delta l''\right|=40\cdot0{,}12=4{,}8\ \text{N}"),
                                                     M(r"m''=\dfrac{F''}{g}=\dfrac{4{,}8}{10}=0{,}48\ \text{kg}"), A(r"m''=480\ \text{g}\ (\text{tổng})")]),
  (r"Khối lượng treo thêm", [P(r"Đã có sẵn vật $120\ \text{g}$, nên phần cần thêm là:"), M(r"\Delta m=m''-m_1=480-120"), A(r"\Delta m=360\ \text{g}")]),
  (r"Kiểm tra", [P(r"Cứ $40\ \text{g}$ thì lò xo dãn thêm $1\ \text{cm}$ (vì $k=40\ \text{N/m}$, $g=10\ \text{m/s}^2$)."),
                 P(r"$120\ \text{g}$ ứng với $3\ \text{cm}$; $200\ \text{g}$ ứng với $5\ \text{cm}$; $480\ \text{g}$ ứng với $12\ \text{cm}$ ✓.")])],
  [r"a) $k=40\ \text{N/m}$", r"b) $l'=25\ \text{cm}$", r"c) Treo thêm $360\ \text{g}$ (tổng $480\ \text{g}$)"],
  r"Nhận dạng: lò xo <strong>treo vật đứng yên</strong> → lực đàn hồi bằng trọng lượng của <strong>tất cả vật đang treo</strong>, rồi dùng Hooke."),
 sol([r"<strong>Lò xo nhẹ treo vật đứng yên:</strong> lực đàn hồi cân bằng với trọng lượng, $mg=k\left|\Delta l\right|$.",
      r"$\left|\Delta l\right|=l-l_0$ khi lò xo dãn; $F$ (N), $\Delta l$ (m), $k$ (N/m).",
      r"$k$ và $l_0$ thuộc về lò xo, không đổi giữa hai lần treo.",
      r"Hai trạng thái của cùng một lò xo cho hai phương trình.",
      r"⚠ <strong>Điều kiện:</strong> lò xo nhẹ, trong giới hạn đàn hồi."], [
  (r"Phần lực tăng thêm", [P(r"Vật đứng yên nên lực đàn hồi cân bằng với trọng lượng:"), M(r"F_1=m_1g=0{,}160\cdot10=1{,}6\ \text{N}"),
                           M(r"F_2=m_2g=0{,}480\cdot10=4{,}8\ \text{N}"), M(r"\Delta F=F_2-F_1=4{,}8-1{,}6"), A(r"\Delta F=3{,}2\ \text{N}")]),
  (r"Độ cứng", [P(r"Viết Hooke cho hai trạng thái rồi trừ vế theo vế, $l_0$ triệt tiêu:"), M(r"F_1=k\left(l_1-l_0\right),\quad F_2=k\left(l_2-l_0\right)"),
                M(r"F_2-F_1=k\left(l_2-l_1\right)"), M(r"k=\dfrac{\Delta F}{l_2-l_1}=\dfrac{3{,}2}{0{,}28-0{,}24}=\dfrac{3{,}2}{0{,}040}"), A(r"k=80\ \text{N/m}")]),
  (r"Độ dãn của lần treo đầu", [M(r"\left|\Delta l_1\right|=\dfrac{F_1}{k}=\dfrac{1{,}6}{80}=0{,}020\ \text{m}"), A(r"\left|\Delta l_1\right|=2{,}0\ \text{cm}")]),
  (r"Chiều dài tự nhiên", [P(r"Treo vật thì lò xo dãn, nên $l_0$ nhỏ hơn $l_1$:"), M(r"l_0=l_1-\left|\Delta l_1\right|=24-2{,}0"), A(r"l_0=22\ \text{cm}")]),
  (r"Chiều dài khi chỉ treo $400\ \text{g}$", [M(r"F_3=m_3g=0{,}400\cdot10=4{,}0\ \text{N}"), M(r"\left|\Delta l_3\right|=\dfrac{F_3}{k}=\dfrac{4{,}0}{80}=0{,}050\ \text{m}=5{,}0\ \text{cm}"),
                                              M(r"l_3=l_0+\left|\Delta l_3\right|=22+5{,}0"), A(r"l_3=27\ \text{cm}")]),
  (r"Kiểm tra", [P(r"Thế $k=80\ \text{N/m}$, $l_0=22\ \text{cm}$ vào trạng thái thứ hai:"), M(r"l_2=22+\dfrac{4{,}8}{80}\cdot100=28\ \text{cm}"),
                 P(r"Khớp với đề ✓.")])],
  [r"a) $k=80\ \text{N/m}$", r"b) $l_0=22\ \text{cm}$", r"c) $l_3=27\ \text{cm}$"],
  r"Nhận dạng: <strong>hai chiều dài ứng với hai khối lượng</strong>, $l_0$ chưa biết → viết Hooke cho cả hai trạng thái rồi trừ vế để loại $l_0$."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>thôi lực mà chiều dài khác ban đầu</b> → nghĩ tới <b>biến dạng dẻo</b>, đã quá giới hạn đàn hồi.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Loại biến dạng", r"Lò xo trong thí nghiệm chịu biến dạng nào?",
       loi=r"Gọi tên loại biến dạng theo một dấu hiệu khác, không xét cặp lực tác dụng vào lò xo.",
       lua_chon=[(r"Biến dạng kéo", True),
                 (r"Biến dạng nén", r"Biến dạng nén có cặp lực hướng vào trong vật, làm vật ngắn lại; ở đây lò xo dài ra."),
                 (r"Biến dạng dẻo", r"Kéo hay nén phân loại theo hướng của lực; dẻo hay đàn hồi phân loại theo việc vật có trở về sau khi thôi lực.")]),
  buoc(r"Lần thử bị biến dạng dẻo", r"Ở lần thử nào lò xo bị biến dạng dẻo?",
       loi=r"Chỉ nhìn lò xo có co lại hay không, bỏ qua việc có trở về đúng chiều dài ban đầu hay chưa.",
       lua_chon=[(r"Lần thử $F=10\ \text{N}$", True),
                 (r"Không lần nào, vì lò xo luôn co lại", r"Co lại một phần chưa phải trở về như cũ: $22\ \text{cm}$ vẫn khác $20\ \text{cm}$."),
                 (r"Cả năm lần, vì $l'$ khác $l$", r"Mốc so sánh là chiều dài ban đầu $20\ \text{cm}$, không phải chiều dài lúc đang chịu lực.")],
       ke=[(r"So chiều dài sau khi thôi lực với chiều dài tự nhiên", True),
           (r"So chiều dài sau khi thôi lực với chiều dài lúc có lực", r"Mốc để xét đàn hồi hay dẻo là chiều dài ban đầu, không phải chiều dài lúc đang chịu lực."),
           (r"Chọn lần thử có lực nhỏ nhất trong bảng số liệu", r"Lực nhỏ không phải dấu hiệu của biến dạng dẻo; phải xét lò xo có trở về chiều dài cũ không.")]),
  buoc(r"Lực lớn nhất còn đàn hồi", r"Lực lớn nhất trong bảng mà lò xo vẫn trở về đúng chiều dài ban đầu là bao nhiêu?", 8, "N", 0.1,
       loi=r"Lấy lực của lần thử cuối cùng trong bảng.",
       ke=[(r"Chọn lần lớn nhất mà lò xo vẫn trở về chiều dài ban đầu", True),
           (r"Lấy lực của lần thử cuối cùng trong bảng đã cho ở đề", r"Lần thử cuối là lần đã gây biến dạng dẻo, không còn đàn hồi."),
           (r"Lấy lực nhỏ nhất trong bảng vì như vậy là an toàn", r"Giới hạn đàn hồi là mức lực lớn nhất vẫn còn đàn hồi, không phải mức nhỏ nhất.")]),
  buoc(r"Khoảng của giới hạn đàn hồi", r"Giới hạn đàn hồi của lò xo nằm trong khoảng nào?",
       loi=r"Cho rằng giới hạn đàn hồi đúng bằng một lực đã thử trong bảng.",
       lua_chon=[(r"Trong khoảng từ $8\ \text{N}$ đến dưới $10\ \text{N}$", True),
                 (r"Đúng bằng $8\ \text{N}$, vì đó là lần cuối còn đàn hồi", r"Chưa thử lực nằm giữa $8\ \text{N}$ và $10\ \text{N}$ nên chưa thể kết luận giới hạn đúng bằng $8\ \text{N}$."),
                 (r"Đúng bằng $10\ \text{N}$, vì đó là lần thử cuối cùng", r"Ở $10\ \text{N}$ lò xo đã bị dẻo, nên $10\ \text{N}$ đã vượt giới hạn.")],
       ke=[(r"Chặn giới hạn giữa lực lần còn đàn hồi và lực lần đã dẻo", True),
           (r"Lấy trung bình của hai lực ấy làm giá trị giới hạn", r"Không có cơ sở chọn đúng trung bình; chỉ biết giới hạn nằm trong khoảng giữa hai lực."),
           (r"Lấy lực của lần thử cuối cùng trong bảng làm giới hạn", r"Lần cuối đã gây biến dạng dẻo, nên đã vượt qua giới hạn rồi.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực và độ dãn (cm)</b> của lò xo → nghĩ tới <b>F = k|Δl|</b>, đổi cm ra m.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Đổi độ dãn ra mét", r"Độ dãn $4{,}0\ \text{cm}$ bằng bao nhiêu mét?", 0.04, "m", 0.001,
       loi=r"Thế thẳng số xentimét vào công thức mà không đổi đơn vị."),
  buoc(r"Độ cứng", r"Độ cứng $k$ của lò xo bằng bao nhiêu?", 150, "N/m", 1,
       loi=r"Nhân $F$ với độ dãn thay vì chia, hoặc chia ngược độ dãn cho $F$.",
       ke=[(r"Rút $k$ từ định luật Hooke, với độ dãn đã đổi ra mét", True),
           (r"Nhân lực kéo với độ dãn đã đổi ra mét rồi ghi N/m", r"Công thức là $F=k\left|\Delta l\right|$ nên $k$ là thương của $F$ và $\left|\Delta l\right|$, không phải tích."),
           (r"Chia độ dãn đã đổi ra mét cho lực kéo rồi ghi N/m", r"Chia ngược cho đơn vị m/N, không phải N/m.")]),
  buoc(r"Độ dãn khi kéo $9{,}0\ \text{N}$", r"Kéo bằng lực $9{,}0\ \text{N}$, lò xo dãn thêm bao nhiêu xentimét?", 6.0, "cm", 0.1,
       loi=r"Coi số niutơn và số xentimét tăng thêm cùng một lượng.",
       ke=[(r"Dùng độ cứng đã tìm để suy ra độ dãn mới", True),
           (r"Cộng thêm $3\ \text{cm}$ vì lực tăng thêm $3\ \text{N}$", r"Niutơn và xentimét không chuyển đổi $1:1$; phải qua độ cứng $k$."),
           (r"Nhân lực mới với độ cứng của lò xo để ra độ dãn", r"Nhân cho đơn vị N·N/m, không phải mét; độ dãn là thương $F/k$.")]),
  buoc(r"Lực khi dãn thêm $2{,}0\ \text{cm}$", r"Muốn lò xo dãn thêm $2{,}0\ \text{cm}$ thì phải kéo bằng lực bao nhiêu?", 3.0, "N", 0.05,
       loi=r"Thế độ dãn tính bằng xentimét vào công thức, hoặc chia $k$ cho độ dãn.",
       ke=[(r"Nhân độ cứng với độ dãn đã đổi ra mét", True),
           (r"Nhân độ cứng với số xentimét của độ dãn", r"Độ dãn phải đổi sang mét; dùng $2{,}0$ cho kết quả lớn gấp trăm lần."),
           (r"Lấy độ cứng chia cho độ dãn đã đổi ra mét", r"Lực tỉ lệ thuận với độ dãn, không tỉ lệ nghịch.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hỏi chiều dài lò xo</b> khi kéo hoặc nén → nghĩ tới <b>Δl</b> rồi so với <b>l₀</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Độ dãn khi kéo", r"Khi kéo bằng lực $3{,}6\ \text{N}$, độ dãn $\left|\Delta l_1\right|$ bằng bao nhiêu xentimét?", 3.0, "cm", 0.05,
       loi=r"Chia lực cho độ cứng nhưng quên đổi kết quả từ mét sang xentimét, hoặc chia ngược."),
  buoc(r"Chiều dài khi kéo", r"Khi kéo bằng lực $3{,}6\ \text{N}$, lò xo dài bao nhiêu xentimét?", 27, "cm", 0.2,
       loi=r"Lấy độ dãn làm chiều dài của lò xo.",
       ke=[(r"Đổi độ biến dạng sang chiều dài của lò xo", True),
           (r"Coi độ biến dạng chính là chiều dài của lò xo lúc này", r"Độ biến dạng chỉ là phần dài thêm hoặc ngắn đi; chiều dài còn gồm cả chiều dài tự nhiên."),
           (r"Luôn trừ độ biến dạng khỏi chiều dài tự nhiên của lò xo", r"Trừ chỉ đúng khi lò xo bị nén; lò xo bị kéo thì dài hơn chiều dài tự nhiên.")]),
  buoc(r"Chiều dài khi nén", r"Khi đẩy bằng lực $4{,}8\ \text{N}$ về phía tường, lò xo dài bao nhiêu xentimét?", 20, "cm", 0.2,
       loi=r"Dùng lại cách tính chiều dài của lần kéo mà không xét lò xo đang bị đẩy.",
       ke=[(r"Tính độ biến dạng mới, rồi xét lò xo ngắn đi hay dài ra", True),
           (r"Dùng luôn chiều dài của lần kéo vì cùng một lò xo", r"Lực đẩy $4{,}8\ \text{N}$ khác lực kéo $3{,}6\ \text{N}$ nên độ biến dạng cũng khác."),
           (r"Cộng độ biến dạng vào chiều dài tự nhiên như lúc kéo", r"Lò xo bị nén thì ngắn đi, không dài thêm.")]),
  buoc(r"Lực kéo để lò xo dài $30\ \text{cm}$", r"Phải kéo bằng lực bao nhiêu để lò xo dài $30\ \text{cm}$?", 7.2, "N", 0.05,
       loi=r"Thế chiều dài $30\ \text{cm}$ vào công thức Hooke như thể đó là độ dãn.",
       ke=[(r"Tìm độ dãn từ chiều dài đề cho, rồi mới tính lực", True),
           (r"Thế thẳng chiều dài đề cho vào công thức Hooke để tính lực", r"Chiều dài đề cho là $l$, không phải độ biến dạng $\left|\Delta l\right|$."),
           (r"Thế chiều dài tự nhiên vào công thức Hooke để tính lực", r"Chiều dài tự nhiên cũng không phải độ biến dạng; độ dãn là phần dài hơn chiều dài tự nhiên.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy lò xo <b>treo vật đứng yên</b> → nghĩ tới <b>lực đàn hồi cân bằng trọng lượng</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Lực đàn hồi khi vật $120\ \text{g}$ đứng yên", r"Khi vật $120\ \text{g}$ đứng yên, lực đàn hồi của lò xo bằng bao nhiêu?", 1.2, "N", 0.02,
       loi=r"Lấy khối lượng (g hoặc kg) làm lực mà không nhân với $g$."),
  buoc(r"Độ cứng", r"Độ cứng $k$ của lò xo bằng bao nhiêu?", 40, "N/m", 0.5,
       loi=r"Thế chiều dài của lò xo vào công thức Hooke thay cho độ biến dạng.",
       ke=[(r"Chia lực đàn hồi cho độ dãn đã đổi ra mét", True),
           (r"Chia lực đàn hồi cho chiều dài lò xo lúc đứng yên", r"Chiều dài $l$ không phải độ biến dạng; $\left|\Delta l\right|=\left|l-l_0\right|$."),
           (r"Chia lực đàn hồi cho chiều dài tự nhiên của lò xo", r"Chiều dài tự nhiên cũng không phải độ biến dạng.")]),
  buoc(r"Chiều dài khi treo thêm $80\ \text{g}$", r"Sau khi treo thêm vật $80\ \text{g}$, lò xo dài bao nhiêu xentimét?", 25, "cm", 0.2,
       loi=r"Chỉ tính lực của vật treo thêm, bỏ quên vật treo từ đầu; hoặc ghi độ dãn làm chiều dài.",
       ke=[(r"Tìm khối lượng tổng đang treo rồi tính độ dãn tương ứng", True),
           (r"Chỉ lấy trọng lượng của vật $80\ \text{g}$ vừa treo thêm vào", r"Lò xo đang gánh cả hai vật; lực đàn hồi cân bằng với tổng trọng lượng."),
           (r"Giữ nguyên độ dãn đã có ở lần treo đầu tiên", r"Thêm vật thì lực đàn hồi lớn hơn, nên độ dãn cũng khác.")]),
  buoc(r"Tổng khối lượng để lò xo dài $32\ \text{cm}$", r"Khi lò xo dài $32\ \text{cm}$, tổng khối lượng đang treo bằng bao nhiêu gam?", 480, "g", 5,
       loi=r"Thế thẳng chiều dài $32\ \text{cm}$ làm độ dãn, hoặc quên đổi đơn vị.",
       ke=[(r"Tìm độ dãn từ chiều dài rồi suy ra lực và khối lượng", True),
           (r"Lấy khối lượng ban đầu nhân tỉ số hai chiều dài", r"Khối lượng tỉ lệ với độ dãn chứ không tỉ lệ với chiều dài; chiều dài còn gồm cả chiều dài tự nhiên."),
           (r"Thế chiều dài $32\ \text{cm}$ làm độ dãn trong công thức Hooke", r"$32\ \text{cm}$ là chiều dài $l$; độ dãn còn phải bớt đi chiều dài tự nhiên.")]),
  buoc(r"Khối lượng treo thêm", r"Phải treo thêm bao nhiêu gam nữa so với vật $120\ \text{g}$ ban đầu?", 360, "g", 5,
       loi=r"Ghi tổng khối lượng làm khối lượng cần treo thêm.",
       ke=[(r"Bớt phần đã treo khỏi tổng khối lượng cần có", True),
           (r"Lấy luôn tổng khối lượng vừa tìm được ở bước trước", r"Đề hỏi phần cần treo thêm, không phải tổng khối lượng."),
           (r"Cộng tổng khối lượng với phần khối lượng đã treo", r"Cộng làm khối lượng lớn hơn tổng cần có, lò xo sẽ dãn quá $32\ \text{cm}$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hai trạng thái của cùng một lò xo</b>, <b>l₀ chưa biết</b> → nghĩ tới <b>so sánh hai trạng thái</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Phần lực tăng thêm", r"Khi tổng khối lượng treo tăng từ $160\ \text{g}$ lên $480\ \text{g}$, lực đàn hồi tăng thêm bao nhiêu?", 3.2, "N", 0.05,
       loi=r"Lấy lực của lần treo sau thay cho phần lực tăng thêm."),
  buoc(r"Độ cứng", r"Độ cứng $k$ của lò xo bằng bao nhiêu?", 80, "N/m", 1,
       loi=r"Chia lực của một lần treo cho chiều dài lò xo, hoặc quên đổi xentimét sang mét.",
       ke=[(r"Chia phần lực tăng thêm cho phần chiều dài tăng thêm", True),
           (r"Chia lực của lần treo sau cho chiều dài lúc đó", r"Chiều dài $28\ \text{cm}$ còn gồm cả chiều dài tự nhiên chưa biết, nên không phải độ dãn."),
           (r"Chia lực của lần treo đầu cho phần chiều dài tăng thêm", r"Phần chiều dài tăng thêm ứng với phần lực tăng thêm, không ứng với lực của lần treo đầu.")]),
  buoc(r"Độ dãn của lần treo đầu", r"Với vật $160\ \text{g}$, lò xo dãn bao nhiêu xentimét so với chiều dài tự nhiên?", 2.0, "cm", 0.05,
       loi=r"Lấy hiệu hai chiều dài làm độ dãn của lần treo đầu.",
       ke=[(r"Dùng độ cứng vừa tìm với lực của lần treo đầu", True),
           (r"Lấy hiệu hai chiều dài đề cho làm độ dãn cần tìm", r"Hiệu hai chiều dài là phần dãn thêm giữa hai lần treo, không phải độ dãn so với chiều dài tự nhiên."),
           (r"Lấy luôn chiều dài của lần treo đầu làm độ dãn", r"Chiều dài của lò xo không phải độ dãn của nó.")]),
  buoc(r"Chiều dài tự nhiên", r"Chiều dài tự nhiên $l_0$ của lò xo bằng bao nhiêu xentimét?", 22, "cm", 0.2,
       loi=r"Coi chiều dài đo được của lần treo đầu là chiều dài tự nhiên.",
       ke=[(r"Từ chiều dài đo được và độ dãn, suy ra chiều dài ban đầu", True),
           (r"Lấy chiều dài lần treo đầu làm chiều dài tự nhiên của lò xo", r"Lúc treo vật lò xo đã dãn, nên chiều dài ấy không còn là chiều dài tự nhiên."),
           (r"Lấy hiệu hai chiều dài làm chiều dài tự nhiên của lò xo", r"Hiệu hai chiều dài là phần dãn thêm giữa hai lần treo, không phải chiều dài của lò xo.")]),
  buoc(r"Chiều dài khi chỉ treo $400\ \text{g}$", r"Khi chỉ treo vật $400\ \text{g}$, lò xo dài bao nhiêu xentimét?", 27, "cm", 0.2,
       loi=r"Dùng độ dãn của một trong hai lần treo trước mà không xét khối lượng mới.",
       ke=[(r"Tính độ dãn ứng với khối lượng mới, rồi đổi sang chiều dài", True),
           (r"Dùng luôn chiều dài của lần treo đầu tiên cho vật mới", r"Khối lượng $400\ \text{g}$ khác $160\ \text{g}$ nên độ dãn và chiều dài cũng khác."),
           (r"Lấy độ dãn mới tìm được làm chiều dài lò xo", r"Độ dãn chỉ là phần dài thêm; chiều dài còn gồm cả chiều dài tự nhiên.")]),
  buoc("Kiểm tra")]),
]

write(J, 78, "Bài 33. Biến dạng của vật rắn", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
