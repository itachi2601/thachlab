"""Bài 77 — "Bài 32. Lực hướng tâm và gia tốc hướng tâm" (Vật lí 10, chương 6). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-58.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-77.py  → ghi scripts/data/bai-tap-mau/77.json
Dạng theo quét: scripts/logs/batch-ra-soat/ket-qua/77.quet-dang.json. Hình: hinh_77.py (chuyển động tròn tính thật, chạy một lần).
Ví dụ cũ (old/77.json, 2 mục): cả hai đều đủ dữ kiện bằng chữ nên KHÔNG bỏ → vào tự luận, giữ lời giải gốc.
 · VD2 (xe đua): lời giải gốc ghi ω ≈ 0,22 rồi 0,22²·80 ≈ 3,92 (lệch do làm tròn sớm: 0,22²·80 = 3,87) → chỉ sửa chữ số hiển thị thành 0,2212 để khớp 3,92.
 · VD1 (Mặt Trăng): kiểm lại 1023,98 m/s; 2,73·10⁻³ m/s²; 2,0·10²⁰ N; 13,4 vòng → khớp, giữ nguyên.
Không có ví dụ cũ nào hợp để biên tập thành dạng (ví dụ cũ đều là bài thiên văn / xe đua nhiều ý, trùng bài toán mẫu xe qua cua trong lý thuyết)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_77 import BUILD

J = os.path.join(HERE, "77.json")
OLD = json.load(open(os.path.join(HERE, "old/77.json")))["questions"]
T35 = "Lực hướng tâm và gia tốc hướng tâm"
T148 = "Tính gia tốc hướng tâm"
T149 = "Lực hướng tâm trong các tình huống thực tế"

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
pi = math.pi
# D1
v1, r1 = 2.0, 0.50
ok("D1 a", v1**2 / r1, 8.0, 1e-9)
assert abs(v1 / r1 - 8.0) > 3 and abs(v1**2 * r1 - 8.0) > 5                      # cách sai: v/r ; v²·r
# D2
T2, r2 = 40.0, 15.0
w2 = 2 * pi / T2; v2 = w2 * r2; a2 = w2**2 * r2
ok("D2 ω", w2, 0.1571, 5e-5); ok("D2 v", v2, 2.356, 5e-4); ok("D2 a", a2, 0.370, 5e-4)
ok("D2 v²/r", v2**2 / r2, a2, 1e-12); ok("D2 2.356²/15", 2.356**2 / 15, 0.370, 5e-4); ok("D2 %g", a2 / 9.8, 0.038, 5e-4)
assert abs(w2 * r2 - a2) > 1 and abs(2 * pi * T2 - w2) > 1 and abs(v2**2 * r2 - a2) > 10  # ωr ; 2πT ; v²r
# D3
w3, rA, rB = 20.0, 0.10, 0.30
ok("D3 aA", w3**2 * rA, 40.0, 1e-9); ok("D3 aB", w3**2 * rB, 120.0, 1e-9)
v3, ra, rb = 10.0, 20.0, 40.0
ok("D3 a1", v3**2 / ra, 5.0, 1e-9); ok("D3 a2", v3**2 / rb, 2.5, 1e-9)
v3b = 12.0; ok("D3 a1'", v3b**2 / ra, 7.2, 1e-9); ok("D3 tỉ số", (v3b**2 / ra) / (v3**2 / ra), 1.44, 1e-9)
assert abs(v3b / v3 * 5.0 - 7.2) > 1 and abs(5.0 + 2 - 7.2) > 0.1 and abs(w3**2 * rB - v3**2 / rb) > 10   # nhân 1,2 ; cộng 2 ; dùng ω²r cho xe
# D4
m4, r4, f4 = 0.050, 0.20, 1.0
w4 = 2 * pi * f4; F4 = m4 * w4**2 * r4
ok("D4 ω", w4, 6.283, 1e-3); ok("D4 F", F4, 0.395, 5e-4); ok("D4 a", w4**2 * r4, 7.90, 5e-3); ok("D4 m·a", m4 * w4**2 * r4, 0.395, 5e-4)
assert abs(m4 * 60**2 * r4 - F4) > 10 and abs(50 * w4**2 * 20 - F4) > 100        # ω = 60 rad/s ; không đổi đơn vị
# D5
m5, v5, rr5 = 200.0, 15.0, 50.0
ok("D5 v", 54 / 3.6, v5, 1e-9); Fht = m5 * v5**2 / rr5; ok("D5 Fht", Fht, 900.0, 1e-9)
Pw = m5 * 10; Fk, Fu = 0.60 * Pw, 0.30 * Pw
ok("D5 Fk", Fk, 1200.0, 1e-9); ok("D5 Fu", Fu, 600.0, 1e-9)
assert Fht <= Fk and Fht > Fu                                                      # khô không trượt, ướt trượt
rk, ru = m5 * v5**2 / Fk, m5 * v5**2 / Fu
ok("D5 r khô", rk, 37.5, 1e-9); ok("D5 r ướt", ru, 75.0, 1e-9)
ok("D5 kiểm khô", m5 * v5**2 / rk, Fk, 1e-9); ok("D5 kiểm ướt", m5 * v5**2 / ru, Fu, 1e-9)
assert rk < rr5 < ru
assert abs(v5**2 / 10 - rk) > 5 and abs(m5 * 54**2 / Fk - rk) > 100                # r = v²/g ; không đổi km/h
# Tự luận cũ
ok("VD Trăng v", 2 * pi * 384403e3 / (27.3 * 86400), 1023.98, 0.01)
ok("VD Trăng a", 1023.98**2 / 384403e3, 2.73e-3, 5e-6); ok("VD Trăng F", 7.347e22 * 2.73e-3, 2e20, 1e18); ok("VD Trăng N", 365 / 27.3, 13.4, 0.05)
w_xe = 2 * pi / 28.4; ok("VD xe ω", w_xe, 0.22124, 5e-6); ok("VD xe a", w_xe**2 * 80, 3.92, 0.01); ok("VD xe μ", w_xe**2 * 80 / 9.8, 0.4, 0.005)

# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Khái niệm: vận tốc đổi hướng nên có gia tốc hướng tâm", topic=T35,
      problem_html=r"""<p>Một hòn bi buộc vào đầu sợi dây nhẹ, đầu kia giữ cố định tại $O$. Hòn bi chuyển động tròn đều trên mặt bàn nhẵn nằm ngang với tốc độ $2{,}0\ \text{m/s}$, bán kính quỹ đạo $r=0{,}50\ \text{m}$. Gọi $A$ và $B$ là hai vị trí của bi ở hai đầu một đường kính.</p>
<ol type="a"><li>Vận tốc của bi tại $A$ và tại $B$ có giống nhau không?</li>
<li>Hòn bi có gia tốc không?</li>
<li>Gia tốc của bi tại $A$ hướng như thế nào?</li>
<li>Tính độ lớn gia tốc của bi.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Tính gia tốc hướng tâm từ chu kì và bán kính", topic=T148,
      problem_html=r"""<p>Một vòng quay công viên bán kính $15\ \text{m}$ quay đều, mỗi vòng hết $40\ \text{s}$. Một khách ngồi trong cabin ở mép vòng. Tính:</p>
<ol type="a"><li>tốc độ góc của vòng quay;</li><li>tốc độ dài của khách;</li><li>gia tốc hướng tâm của khách.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · So sánh gia tốc hướng tâm khi giữ nguyên ω hoặc v", topic=T148,
      problem_html=r"""<p>Một quạt trần quay đều với tốc độ góc $\omega=20\ \text{rad/s}$. Điểm $A$ cách trục quay $10\ \text{cm}$, điểm $B$ ở đầu cánh quạt cách trục $30\ \text{cm}$.</p>
<ol type="a"><li>Tính gia tốc hướng tâm của $A$ và của $B$.</li>
<li>Hai xe máy cùng chạy với tốc độ $10\ \text{m/s}$ qua hai khúc cua tròn có bán kính $r_1=20\ \text{m}$ và $r_2=40\ \text{m}$. Tính gia tốc hướng tâm của mỗi xe.</li>
<li>Xe thứ nhất tăng tốc độ lên $12\ \text{m/s}$ trên khúc cua $r_1$ (vẫn chạy đều). Tính gia tốc hướng tâm lúc này và cho biết nó gấp mấy lần lúc trước.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Xác định lực đóng vai lực hướng tâm", topic=T149,
      problem_html=r"""<p>Một vật nhỏ khối lượng $50\ \text{g}$ đặt trên đĩa nằm ngang, cách trục quay $20\ \text{cm}$. Đĩa quay đều $60$ vòng/phút, vật nằm yên so với đĩa (không trượt).</p>
<ol type="a"><li>Lực nào đóng vai lực hướng tâm của vật?</li>
<li>Tính độ lớn lực hướng tâm.</li>
<li>Nêu lực đóng vai lực hướng tâm của (i) ô tô chạy đều qua khúc cua nằm ngang; (ii) vệ tinh nhân tạo chuyển động tròn đều quanh Trái Đất.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Lực hướng tâm so với lực ma sát nghỉ cực đại", topic=T149,
      problem_html=r"""<p>Một mô tô cùng người lái có tổng khối lượng $200\ \text{kg}$ chạy đều $54\ \text{km/h}$ vào một đoạn đường vòng nằm ngang. Lực ma sát nghỉ cực đại giữa lốp và mặt đường bằng $0{,}60$ lần trọng lượng khi đường khô và $0{,}30$ lần trọng lượng khi đường ướt. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Đường vòng có bán kính $50\ \text{m}$. Tính lực hướng tâm cần có và cho biết xe có trượt không trên đường khô, trên đường ướt.</li>
<li>Tính bán kính cong nhỏ nhất của đường vòng để xe không trượt khi đường khô, khi đường ướt.</li></ol>"""),
]
FORMS = ["ly_thuyet", "bai_tap", "bai_tap", "bai_tap", "bai_tap"]

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“hòn bi buộc vào đầu sợi dây nhẹ … chuyển động tròn đều”", r"Tâm quỹ đạo là $O$", r"⚠ Điều kiện: chuyển động tròn đều (tốc độ không đổi, quỹ đạo tròn)"),
  (r"“với tốc độ $2{,}0\ \text{m/s}$”", r"$v=2{,}0\ \text{m/s}$", r"Phân biệt tốc độ và vận tốc"),
  (r"“bán kính quỹ đạo $r=0{,}50\ \text{m}$”", r"$r=0{,}50\ \text{m}$", r"Đại lượng cùng $v$ quyết định độ lớn gia tốc"),
  (r"“a) vận tốc của bi tại $A$ và tại $B$ có giống nhau không?”", r"So hai vectơ ở hai đầu đường kính", r"Phân biệt tốc độ và vận tốc"),
  (r"“b) hòn bi có gia tốc không?”", r"Cần kết luận có / không", r"Gia tốc đo sự thay đổi của đại lượng nào?"),
  (r"“c) gia tốc của bi tại $A$ hướng như thế nào?”", r"Cần phương và chiều", r"Gốc, phương, chiều của gia tốc hướng tâm"),
  (r"“d) độ lớn gia tốc”", r"Cần $a_{\text{ht}}$ (m/s²)", r"Đại lượng cần tìm")],
 [(r"“vòng quay công viên bán kính $15\ \text{m}$”", r"$r=15\ \text{m}$", r"Quỹ đạo của khách là đường tròn tâm ở trục quay"),
  (r"“quay đều”", r"Tròn đều", r"⚠ Điều kiện: quay đều thì $\omega$ và $v$ không đổi"),
  (r"“mỗi vòng hết $40\ \text{s}$”", r"$T=40\ \text{s}$", r"Liên hệ chu kì với tốc độ góc"),
  (r"“khách ngồi trong cabin ở mép vòng”", r"Khách cách trục đúng $r$", r"Bán kính quỹ đạo của khách"),
  (r"“a) tốc độ góc”", r"Cần $\omega$ (rad/s)", r"Đại lượng cần tìm"),
  (r"“b) tốc độ dài”", r"Cần $v$ (m/s)", r"Liên hệ $v$, $\omega$, $r$ (Bài 31)"),
  (r"“c) gia tốc hướng tâm của khách”", r"Cần $a_{\text{ht}}$ (m/s²)", r"Đại lượng cần tìm")],
 [(r"“quạt trần quay đều, $\omega=20\ \text{rad/s}$”", r"$\omega=20\ \text{rad/s}$", r"⚠ Quay đều: các điểm trên quạt có chung đại lượng nào?"),
  (r"“$A$ cách trục $10\ \text{cm}$, $B$ cách trục $30\ \text{cm}$”", r"$r_A=0{,}10\ \text{m}$; $r_B=0{,}30\ \text{m}$", r"Đổi cm sang m"),
  (r"“a) gia tốc hướng tâm của $A$ và của $B$”", r"Cần $a_A$, $a_B$ (m/s²)", r"Đại lượng cần tìm"),
  (r"“hai xe máy cùng chạy với tốc độ $10\ \text{m/s}$”", r"$v=10\ \text{m/s}$ cho cả hai xe", r"⚠ Đề giữ nguyên đại lượng nào? Chọn công thức theo đại lượng đó"),
  (r"“hai khúc cua $r_1=20\ \text{m}$ và $r_2=40\ \text{m}$”", r"$r_1=20\ \text{m}$; $r_2=40\ \text{m}$", r"Hai khúc cua có bán kính khác nhau"),
  (r"“b) gia tốc hướng tâm của mỗi xe”", r"Cần $a_1$, $a_2$ (m/s²)", r"Đại lượng cần tìm"),
  (r"“c) tăng tốc độ lên $12\ \text{m/s}$ trên khúc cua $r_1$”", r"$v'=12\ \text{m/s}$; $r_1$ giữ nguyên", r"Đổi tốc độ, giữ bán kính"),
  (r"“gấp mấy lần lúc trước”", r"Cần tỉ số $a_1'/a_1$", r"Hai giá trị cùng đơn vị mới so sánh được")],
 [(r"“vật nhỏ khối lượng $50\ \text{g}$”", r"$m=0{,}050\ \text{kg}$", r"Đổi g sang kg"),
  (r"“đặt trên đĩa nằm ngang, cách trục quay $20\ \text{cm}$”", r"$r=0{,}20\ \text{m}$", r"Quỹ đạo của vật là đường tròn tâm ở trục quay"),
  (r"“đĩa quay đều $60$ vòng/phút”", r"$f=1$ vòng/s", r"⚠ Đổi sang tốc độ góc (rad/s) trước khi dùng công thức"),
  (r"“vật nằm yên so với đĩa (không trượt)”", r"Vật quay cùng đĩa, cùng $\omega$", r"⚠ Vật chuyển động tròn đều: hợp lực phải hướng vào đâu?"),
  (r"“a) lực nào đóng vai lực hướng tâm”", r"Liệt kê các lực do vật cụ thể tác dụng lên vật", r"Mỗi lực do một vật gây ra; lực hướng tâm có phải một lực riêng?"),
  (r"“b) độ lớn lực hướng tâm”", r"Cần $F_{\text{ht}}$ (N)", r"Đại lượng cần tìm"),
  (r"“c) ô tô qua khúc cua nằm ngang; vệ tinh quanh Trái Đất”", r"Hai tình huống khác", r"Tìm lực đang chĩa vào tâm trong mỗi trường hợp")],
 [(r"“tổng khối lượng $200\ \text{kg}$”", r"$m=200\ \text{kg}$", r"Khối lượng của cả hệ chuyển động"),
  (r"“chạy đều $54\ \text{km/h}$”", r"$v=54\ \text{km/h}$", r"Đổi sang đơn vị chuẩn; chuyển động tròn đều"),
  (r"“đoạn đường vòng nằm ngang”", r"Đường phẳng", r"⚠ Trọng lực và phản lực theo phương đứng thế nào? Lực nằm ngang còn lại là lực nào?"),
  (r"“ma sát nghỉ cực đại … $0{,}60$ lần trọng lượng (khô), $0{,}30$ lần (ướt)”", r"$F_{\text{max}}=0{,}60\,mg$; $0{,}30\,mg$", r"⚠ Ma sát nghỉ có giá trị lớn nhất; vượt giới hạn thì lốp trượt"),
  (r"“a) bán kính $50\ \text{m}$ … lực hướng tâm cần có … có trượt không”", r"$r=50\ \text{m}$; cần $F_{\text{ht}}$ và kết luận", r"So hai lực cùng loại"),
  (r"“b) bán kính cong nhỏ nhất để xe không trượt”", r"Cần $r_{\text{min}}$ (m) cho hai loại đường", r"Giới hạn không trượt ứng với quan hệ nào giữa hai lực?")],
]

# ═════════════ Lời giải từng bước ═════════════
R_D1 = [r"<strong>Khái niệm:</strong> vận tốc là vectơ (độ lớn và hướng); gia tốc đo sự thay đổi của vận tốc, cả độ lớn lẫn hướng.",
        r"Chuyển động tròn đều: độ lớn vận tốc không đổi, hướng vận tốc đổi liên tục.",
        r"<strong>Gia tốc hướng tâm:</strong> gốc tại vật, phương trùng bán kính, chiều vào tâm.",
        r"$a_{\text{ht}}=\dfrac{v^2}{r}=\omega^2 r$.",
        r"⚠ <strong>Điều kiện:</strong> chuyển động tròn đều."]
R_D2 = [r"<strong>Khái niệm:</strong> quay đều thì $\omega$ và $v$ không đổi.",
        r"$\omega=\dfrac{2\pi}{T}$ và $v=\omega r$ (Bài 31).",
        r"$a_{\text{ht}}=\dfrac{v^2}{r}=\omega^2 r$.",
        r"⚠ <strong>Điều kiện:</strong> chuyển động tròn đều; $r$ là khoảng cách từ vật tới trục quay."]
R_D3 = [r"<strong>Khái niệm:</strong> các điểm của một vật rắn quay quanh trục có cùng $\omega$; hai xe cùng tốc độ thì cùng $v$.",
        r"Cùng $\omega$: $a_{\text{ht}}=\omega^2 r$ · cùng $v$: $a_{\text{ht}}=\dfrac{v^2}{r}$.",
        r"Đổi đơn vị về m, s trước khi thế.",
        r"⚠ <strong>Điều kiện:</strong> chọn công thức theo đại lượng được giữ nguyên."]
R_D4 = [r"<strong>Khái niệm:</strong> lực hướng tâm là tên một vai: hợp lực hướng vào tâm, không phải lực mới.",
        r"Chỉ tính lực do một vật cụ thể tác dụng lên vật.",
        r"$F_{\text{ht}}=m\omega^2 r$ và $\omega=2\pi f$.",
        r"⚠ <strong>Điều kiện:</strong> vật chuyển động tròn đều trong hệ gắn với mặt đất; không vẽ thêm lực hướng tâm, không có lực li tâm."]
R_D5 = [r"<strong>Khái niệm:</strong> trên đường nằm ngang, ma sát nghỉ là lực đóng vai lực hướng tâm.",
        r"$F_{\text{ht}}=m\dfrac{v^2}{r}$ · trọng lượng $P=mg$.",
        r"Không trượt khi $F_{\text{ht}}\le F_{\text{max}}$; giới hạn ứng với $F_{\text{ht}}=F_{\text{max}}$.",
        r"⚠ <strong>Điều kiện:</strong> đổi km/h sang m/s trước khi thế."]

SOLS = [
 sol(R_D1, [
  (r"Vận tốc tại $A$ và $B$", [P(r"Tại $A$ và $B$ vận tốc đều có độ lớn $2{,}0\ \text{m/s}$, vuông góc với bán kính."),
                               P(r"Hai vận tốc có hướng ngược nhau nên là hai vectơ khác nhau: <strong>vận tốc thay đổi</strong> dù tốc độ không đổi.")]),
  (r"Bi có gia tốc không", [P(r"Gia tốc đo sự thay đổi của vectơ vận tốc, kể cả khi chỉ đổi hướng."),
                           P(r"Hướng vận tốc đổi liên tục nên bi <strong>có gia tốc</strong>.")]),
  (r"Phương và chiều tại $A$", [P(r"Vận tốc đổi hướng về phía trong vòng tròn nên gia tốc có gốc tại bi, phương trùng bán kính $OA$, chiều từ $A$ về $O$."),
                               P(r"Gia tốc vuông góc với vận tốc nên không làm đổi độ lớn vận tốc.")]),
  (r"Độ lớn gia tốc", [M(r"a_{\text{ht}}=\dfrac{v^2}{r}=\dfrac{2{,}0^2}{0{,}50}"), A(r"a_{\text{ht}}=8{,}0\ \text{m/s}^2")]),
  (r"Kiểm tra", [P(r"Đơn vị: $\dfrac{(\text{m/s})^2}{\text{m}}=\text{m/s}^2$ ✓."),
                 P(r"Tại mọi vị trí gia tốc đều chĩa vào $O$, nên hướng của nó đổi cùng với bi.")])],
  [r"a) Hai vận tốc khác nhau (cùng độ lớn, khác hướng)", r"b) Có gia tốc", r"c) Phương $OA$, chiều từ $A$ về $O$", r"d) $a_{\text{ht}}=8{,}0\ \text{m/s}^2$"],
  r"Nhận dạng: <strong>tốc độ không đổi nhưng quỹ đạo tròn</strong> → vận tốc đổi hướng nên có gia tốc hướng tâm, chĩa vào tâm."),
 sol(R_D2, [
  (r"Tốc độ góc", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{40}"), A(r"\omega\approx0{,}1571\ \text{rad/s}")]),
  (r"Tốc độ dài", [P(r"Khách ở mép vòng nên cách trục đúng $r=15\ \text{m}$:"), M(r"v=\omega r=\dfrac{2\pi}{40}\cdot15"), A(r"v\approx2{,}356\ \text{m/s}"), P(r"Khoảng $8{,}5\ \text{km/h}$: hợp lí với vòng quay.")]),
  (r"Gia tốc hướng tâm", [M(r"a_{\text{ht}}=\omega^2 r=\left(\dfrac{2\pi}{40}\right)^2\cdot15"), A(r"a_{\text{ht}}\approx0{,}370\ \text{m/s}^2"), P(r"Hướng từ cabin vào trục quay.")]),
  (r"Kiểm tra", [M(r"a_{\text{ht}}=\dfrac{v^2}{r}=\dfrac{2{,}356^2}{15}\approx0{,}370\ \text{m/s}^2"), P(r"Hai công thức cho cùng kết quả ✓."), P(r"Bằng khoảng $4\,\%$ gia tốc rơi tự do: khách chỉ thấy bị ép rất nhẹ.")])],
  [r"a) $\omega\approx0{,}1571\ \text{rad/s}$", r"b) $v\approx2{,}356\ \text{m/s}$", r"c) $a_{\text{ht}}\approx0{,}370\ \text{m/s}^2$"],
  r"Nhận dạng: đề cho <strong>chu kì và bán kính</strong> → $\omega=2\pi/T$, rồi $a_{\text{ht}}=\omega^2 r$."),
 sol(R_D3, [
  (r"Đại lượng giữ nguyên với $A$ và $B$", [P(r"$A$ và $B$ nằm trên cùng một cánh nên trong cùng một chu kì cùng quay được một vòng: <strong>cùng tốc độ góc</strong> $\omega$."),
                                          P(r"Quãng đường mỗi điểm đi được khác nhau (bán kính khác nhau) nên tốc độ dài khác nhau.")]),
  (r"Gia tốc của $A$ và $B$ (cùng $\omega$)", [P(r"Đổi: $r_A=0{,}10\ \text{m}$, $r_B=0{,}30\ \text{m}$."), M(r"a_A=\omega^2 r_A=20^2\cdot0{,}10"), A(r"a_A=40\ \text{m/s}^2"),
                                              M(r"a_B=\omega^2 r_B=20^2\cdot0{,}30"), A(r"a_B=120\ \text{m/s}^2"), P(r"Cùng $\omega$ thì $a_{\text{ht}}$ tỉ lệ thuận với $r$: $B$ xa trục gấp ba lần nên $a_B$ gấp ba lần ✓.")]),
  (r"Hai xe cùng tốc độ", [P(r"Hai xe cùng $v=10\ \text{m/s}$, bán kính khác nhau, nên dùng $a_{\text{ht}}=v^2/r$:"), M(r"a_1=\dfrac{v^2}{r_1}=\dfrac{10^2}{20}"), A(r"a_1=5{,}0\ \text{m/s}^2"),
                           M(r"a_2=\dfrac{v^2}{r_2}=\dfrac{10^2}{40}"), A(r"a_2=2{,}5\ \text{m/s}^2"), P(r"Cùng $v$ thì $a_{\text{ht}}$ tỉ lệ nghịch với $r$.")]),
  (r"Tăng tốc độ trên khúc cua $r_1$", [M(r"a_1'=\dfrac{v'^2}{r_1}=\dfrac{12^2}{20}"), A(r"a_1'=7{,}2\ \text{m/s}^2"), M(r"\dfrac{a_1'}{a_1}=\dfrac{7{,}2}{5{,}0}"), A(r"\dfrac{a_1'}{a_1}\approx1{,}44"),
                                       P(r"$v$ tăng $1{,}2$ lần nên $a_{\text{ht}}$ tăng $1{,}2^2=1{,}44$ lần ✓.")]),
  (r"Kiểm tra", [P(r"Đã đổi cm sang m trước khi thế ✓."), P(r"Cùng $\omega$: xa trục thì $a$ lớn hơn. Cùng $v$: cua rộng thì $a$ nhỏ hơn."), P(r"Hai kết luận không mâu thuẫn vì giữ nguyên hai đại lượng khác nhau.")])],
  [r"a) $a_A=40\ \text{m/s}^2$ · $a_B=120\ \text{m/s}^2$", r"b) $a_1=5{,}0\ \text{m/s}^2$ · $a_2=2{,}5\ \text{m/s}^2$", r"c) $a_1'=7{,}2\ \text{m/s}^2$ · gấp $1{,}44$ lần"],
  r"Nhận dạng: đề <strong>so sánh gia tốc</strong> của nhiều điểm hay nhiều xe → hỏi đại lượng nào giữ nguyên ($\omega$ hay $v$) rồi chọn công thức."),
 sol(R_D4, [
  (r"Các lực theo phương thẳng đứng", [P(r"Vật không chuyển động theo phương đứng nên hợp lực theo phương đó bằng $0$."),
                                      P(r"Trọng lực $\vec P$ và phản lực $\vec N$ của đĩa cân bằng nhau.")]),
  (r"Lực đóng vai lực hướng tâm", [P(r"Lực nằm ngang duy nhất còn lại là <strong>lực ma sát nghỉ</strong> của đĩa tác dụng lên vật."),
                                  P(r"Vật chuyển động tròn đều nên hợp lực hướng vào trục: ma sát nghỉ chính là lực hướng tâm, không thêm lực nào khác.")]),
  (r"Độ lớn lực hướng tâm", [P(r"Đổi: $m=50\ \text{g}=0{,}050\ \text{kg}$, $r=20\ \text{cm}=0{,}20\ \text{m}$, $60$ vòng/phút $=1$ vòng/s."), M(r"\omega=2\pi f=2\pi\cdot1\approx6{,}283\ \text{rad/s}"),
                            M(r"F_{\text{ht}}=m\omega^2 r=0{,}050\cdot(2\pi)^2\cdot0{,}20"), A(r"F_{\text{ht}}\approx0{,}395\ \text{N}"), P(r"Lực ma sát nghỉ tác dụng lên vật có đúng độ lớn này.")]),
  (r"Ô tô qua khúc cua nằm ngang", [P(r"Trọng lực và phản lực của mặt đường cân bằng nhau theo phương đứng."), P(r"Lực chĩa vào tâm cua là <strong>lực ma sát nghỉ</strong> giữa lốp xe và mặt đường.")]),
  (r"Vệ tinh quanh Trái Đất", [P(r"Lực đáng kể duy nhất tác dụng lên vệ tinh là lực hấp dẫn của Trái Đất."), P(r"Lực này chĩa vào tâm Trái Đất nên chính là <strong>lực hướng tâm</strong>.")]),
  (r"Kiểm tra", [M(r"a_{\text{ht}}=\omega^2 r=(2\pi)^2\cdot0{,}20\approx7{,}90\ \text{m/s}^2"), M(r"F_{\text{ht}}=m a_{\text{ht}}=0{,}050\cdot7{,}90\approx0{,}395\ \text{N}"),
                 P(r"Khớp ✓. Không vẽ thêm lực hướng tâm bên cạnh ma sát nghỉ.")])],
  [r"a) Lực ma sát nghỉ của đĩa", r"b) $F_{\text{ht}}\approx0{,}395\ \text{N}$", r"c) (i) ma sát nghỉ giữa lốp và mặt đường · (ii) lực hấp dẫn của Trái Đất"],
  r"Nhận dạng: <strong>vật quay cùng đĩa, không trượt</strong> → mỗi lực do một vật gây ra; lực nằm ngang chĩa vào tâm đóng vai lực hướng tâm."),
 sol(R_D5, [
  (r"Lực hướng tâm cần có", [P(r"Đổi $54\ \text{km/h}=15\ \text{m/s}$."), M(r"F_{\text{ht}}=m\dfrac{v^2}{r}=200\cdot\dfrac{15^2}{50}"), A(r"F_{\text{ht}}=900\ \text{N}")]),
  (r"So với lực ma sát nghỉ cực đại", [M(r"P=mg=200\cdot10=2000\ \text{N}"), M(r"F_{\text{max,khô}}=0{,}60\,P=1200\ \text{N}"), M(r"F_{\text{max,ướt}}=0{,}30\,P=600\ \text{N}"),
                                      P(r"Đường khô: $900\ \text{N}\lt1200\ \text{N}$ nên <strong>không trượt</strong>."), P(r"Đường ướt: $900\ \text{N}\gt600\ \text{N}$ nên <strong>trượt</strong>.")]),
  (r"Bán kính nhỏ nhất, đường khô", [P(r"Giới hạn không trượt: lực hướng tâm bằng lực ma sát nghỉ cực đại."), M(r"m\dfrac{v^2}{r_{\text{min}}}=F_{\text{max}}"),
                                    M(r"r_{\text{min}}=\dfrac{mv^2}{F_{\text{max}}}=\dfrac{200\cdot15^2}{1200}"), A(r"r_{\text{min}}=37{,}5\ \text{m}")]),
  (r"Bán kính nhỏ nhất, đường ướt", [M(r"r_{\text{min}}=\dfrac{mv^2}{F_{\text{max}}}=\dfrac{200\cdot15^2}{600}"), A(r"r_{\text{min}}=75\ \text{m}")]),
  (r"Kiểm tra", [P(r"Thế ngược: $r=37{,}5\ \text{m}$ cho $F_{\text{ht}}=1200\ \text{N}=F_{\text{max,khô}}$; $r=75\ \text{m}$ cho $F_{\text{ht}}=600\ \text{N}=F_{\text{max,ướt}}$ ✓."),
                 P(r"Bán kính $50\ \text{m}$ của ý a nằm giữa hai giá trị, khớp với kết luận: đường khô qua được, đường ướt trượt ✓.")])],
  [r"a) $F_{\text{ht}}=900\ \text{N}$ · đường khô: không trượt · đường ướt: trượt", r"b) $r_{\text{min}}=37{,}5\ \text{m}$ (khô) · $r_{\text{min}}=75\ \text{m}$ (ướt)"],
  r"Nhận dạng: đề hỏi <strong>không trượt</strong> hay <strong>tốc độ, bán kính giới hạn</strong> → so $F_{\text{ht}}$ với lực ma sát nghỉ cực đại."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>tốc độ không đổi nhưng quỹ đạo tròn</b> → nghĩ tới <b>gia tốc hướng tâm</b> chĩa vào tâm.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Vận tốc tại $A$ và $B$", r"Chọn nhận xét đúng về vận tốc của bi tại $A$ và tại $B$.",
       loi=r"Chỉ so độ lớn rồi kết luận vận tốc giống nhau, quên vận tốc còn có hướng.",
       lua_chon=[(r"Cùng độ lớn nhưng khác hướng, nên là hai vectơ khác nhau", True),
                 (r"Giống nhau, vì cùng tốc độ $2{,}0\ \text{m/s}$", r"Vận tốc là vectơ: ngoài độ lớn còn có hướng, nên cùng tốc độ chưa đủ để nói hai vận tốc giống nhau."),
                 (r"Ngược hướng nên độ lớn là $+2{,}0$ và $-2{,}0\ \text{m/s}$", r"Độ lớn không âm: hai vận tốc cùng độ lớn $2{,}0\ \text{m/s}$, chỉ khác hướng.")]),
  buoc(r"Bi có gia tốc không", r"Chọn kết luận đúng về gia tốc của hòn bi.",
       loi=r"Cho rằng tốc độ không đổi thì không có gia tốc, vì chỉ nghĩ gia tốc là việc nhanh lên hay chậm đi.",
       lua_chon=[(r"Có gia tốc, vì vận tốc đổi hướng liên tục", True),
                 (r"Không có gia tốc, vì tốc độ không đổi", r"Gia tốc đo sự thay đổi của vectơ vận tốc, gồm cả hướng; tốc độ không đổi chưa đủ để kết luận."),
                 (r"Không có gia tốc, vì bi chỉ đi theo quán tính", r"Bi đi vòng chứ không đi thẳng, nên không thể chỉ do quán tính.")],
       ke=[(r"Xét xem vectơ vận tốc có đổi không", True),
           (r"Chỉ so độ lớn của vận tốc ở hai thời điểm", r"Độ lớn không đổi chưa nói được gì về hướng, mà gia tốc liên quan tới cả hai."),
           (r"Tìm lực đẩy bi ra xa tâm", r"Không có vật nào đẩy bi ra xa tâm; bước này chưa cần xét lực.")]),
  buoc(r"Phương và chiều tại $A$", r"Chọn phát biểu đúng về gia tốc của bi tại $A$.",
       loi=r"Lấy hướng gia tốc cùng hướng vận tốc (tiếp tuyến), như khi xe tăng tốc trên đường thẳng.",
       lua_chon=[(r"Trùng bán kính $OA$, chiều hướng vào tâm $O$", True),
                 (r"Theo hướng vận tốc tại $A$ (tiếp tuyến với quỹ đạo)", r"Gia tốc cùng hướng vận tốc làm tốc độ thay đổi, mà tốc độ của bi giữ nguyên."),
                 (r"Trùng bán kính $OA$, chiều ra xa tâm $O$", r"Vận tốc đổi hướng về phía trong vòng tròn, không phải ra ngoài.")],
       ke=[(r"Xét vận tốc đổi hướng về phía nào khi bi đi tiếp", True),
           (r"Lấy hướng của vận tốc làm hướng gia tốc", r"Thành phần gia tốc cùng hướng vận tốc chỉ làm đổi độ lớn vận tốc; ở đây tốc độ không đổi."),
           (r"Dùng “lực li tâm” để suy ra hướng gia tốc", r"Không vật nào gây ra lực li tâm; bài này xét trong hệ gắn với mặt đất.")]),
  buoc(r"Độ lớn gia tốc", r"Độ lớn gia tốc hướng tâm của bi bằng bao nhiêu?", 8.0, r"m/s²", 0.1,
       loi=r"Quên bình phương tốc độ, hoặc đặt bán kính ở tử số.",
       ke=[(r"Chia bình phương tốc độ cho bán kính", True),
           (r"Chia tốc độ cho bán kính", r"Thiếu bình phương: đơn vị của $v/r$ là $1/\text{s}$, không phải m/s²."),
           (r"Nhân bình phương tốc độ với bán kính", r"Bán kính nằm ở mẫu số; đơn vị của $v^2r$ không phải m/s².")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>chu kì và bán kính</b> → nghĩ tới <b>ω = 2π/T</b>, rồi <b>a = ω²r</b>.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Tốc độ góc", r"Tốc độ góc $\omega$ bằng bao nhiêu?", 0.1571, r"rad/s", 0.002,
       loi=r"Đảo ngược công thức ($2\pi T$ hoặc $T/2\pi$), hoặc để máy tính ở chế độ độ."),
  buoc(r"Tốc độ dài", r"Tốc độ dài $v$ của khách bằng bao nhiêu?", 2.356, r"m/s", 0.02,
       loi=r"Chia $\omega$ cho $r$ thay vì nhân.",
       ke=[(r"Nhân tốc độ góc với bán kính quỹ đạo của khách", True),
           (r"Chia tốc độ góc cho bán kính", r"Đơn vị của $\omega/r$ là $1/(\text{s}\cdot\text{m})$, không phải m/s."),
           (r"Lấy chu kì chia cho bán kính", r"Chu kì và bán kính không cho trực tiếp tốc độ; cần qua tốc độ góc hoặc chu vi.")]),
  buoc(r"Gia tốc hướng tâm", r"Gia tốc hướng tâm của khách bằng bao nhiêu?", 0.370, r"m/s²", 0.005,
       loi=r"Dùng $\omega r$ (chính là $v$) hoặc quên bình phương $\omega$.",
       ke=[(r"Dùng $\omega^2 r$ với $\omega$ vừa tính", True),
           (r"Dùng $\omega r$", r"$\omega r$ là tốc độ dài $v$ (m/s), chưa phải gia tốc."),
           (r"Dùng $v^2 r$", r"Phải chia $v^2$ cho $r$; nhân sẽ cho đơn vị không phải m/s².")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>so sánh gia tốc</b> của nhiều điểm hay nhiều xe → hỏi <b>đại lượng nào giữ nguyên</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Đại lượng giữ nguyên với $A$ và $B$", r"Hai điểm $A$ và $B$ trên cùng một cánh quạt có đại lượng nào bằng nhau?",
       loi=r"Cho rằng hai điểm có cùng tốc độ dài vì “cùng đi theo cánh quạt”, rồi dùng $v^2/r$ với cùng $v$.",
       lua_chon=[(r"Tốc độ góc $\omega$", True),
                 (r"Tốc độ dài $v$", r"Trong cùng một chu kì, hai điểm đi hết hai đường tròn có bán kính khác nhau nên quãng đường khác nhau, tốc độ dài khác nhau."),
                 (r"Gia tốc hướng tâm", r"Gia tốc còn phụ thuộc bán kính, mà hai điểm cách trục khác nhau.")]),
  buoc(r"Gia tốc của $A$ và $B$", r"Gia tốc hướng tâm của điểm $B$ bằng bao nhiêu?", 120, r"m/s²", 1,
       loi=r"Quên đổi cm sang m (lấy $r=30$) hoặc dùng $v^2/r$ với $v$ chọn bừa.",
       ke=[(r"Dùng công thức ứng với đại lượng giữ nguyên ở bước trước", True),
           (r"Dùng $v^2/r$ với $v$ của hai điểm bằng nhau", r"Hai điểm không có cùng tốc độ dài, nên không dùng được cách này."),
           (r"Cho hai điểm cùng gia tốc", r"Gia tốc phụ thuộc cả bán kính; hai bán kính khác nhau thì kết quả cũng khác.")]),
  buoc(r"Hai xe cùng tốc độ", r"Xe vào khúc cua $r_2=40\ \text{m}$ có gia tốc hướng tâm bằng bao nhiêu?", 2.5, r"m/s²", 0.05,
       loi=r"Dùng $\omega^2 r$ với $\omega=20\ \text{rad/s}$ của quạt, hoặc coi $\omega$ của hai xe bằng nhau.",
       ke=[(r"Dùng công thức theo đại lượng hai xe giống nhau", True),
           (r"Dùng $\omega^2 r$ với $\omega$ của quạt", r"$\omega$ của quạt không liên quan tới hai xe; mỗi xe có $\omega$ riêng."),
           (r"Coi $\omega$ của hai xe bằng nhau", r"Đề cho hai xe cùng tốc độ dài, không cho cùng tốc độ góc.")]),
  buoc(r"Tăng tốc độ trên khúc cua $r_1$", r"Với $v'=12\ \text{m/s}$ trên khúc cua $r_1$, gia tốc hướng tâm bằng bao nhiêu?", 7.2, r"m/s²", 0.1,
       loi=r"Nhân gia tốc cũ với tỉ số tốc độ ($12/10$) thay vì bình phương, hoặc cộng thêm hiệu tốc độ.",
       ke=[(r"Giữ bán kính, thay tốc độ mới vào công thức", True),
           (r"Nhân gia tốc cũ với $12/10$", r"$a_{\text{ht}}$ tỉ lệ với $v^2$, không tỉ lệ với $v$."),
           (r"Cộng gia tốc cũ với hiệu tốc độ $2\ \text{m/s}$", r"Gia tốc không cộng theo hiệu tốc độ; phải tính lại từ công thức.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật quay cùng đĩa, không trượt</b> → nghĩ tới <b>lực do vật cụ thể</b> đóng vai lực hướng tâm.",
  cap_do=2, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Các lực theo phương thẳng đứng", r"Chọn nhận xét đúng về các lực theo phương thẳng đứng tác dụng lên vật.",
       loi=r"Cho rằng phản lực phải lớn hơn trọng lực để vật không rơi.",
       lua_chon=[(r"Trọng lực và phản lực của đĩa cân bằng nhau", True),
                 (r"Phản lực lớn hơn trọng lực để giữ vật không rơi", r"Vật không có gia tốc theo phương đứng nên hợp lực theo phương đó bằng $0$, hai lực phải bằng nhau."),
                 (r"Chỉ có trọng lực, vì đĩa không tác dụng lực lên vật", r"Mặt đĩa đỡ vật bằng phản lực; thiếu lực này vật đã rơi xuyên qua đĩa.")]),
  buoc(r"Lực đóng vai lực hướng tâm", r"Lực nào đóng vai lực hướng tâm của vật trên đĩa?",
       loi=r"Vẽ thêm một “lực hướng tâm” riêng hoặc dùng “lực li tâm” để cân bằng.",
       lua_chon=[(r"Lực ma sát nghỉ của đĩa tác dụng lên vật", True),
                 (r"Phản lực $\vec N$ của đĩa", r"$\vec N$ vuông góc với mặt đĩa nên không chĩa vào trục quay."),
                 (r"Một lực hướng tâm riêng, hướng vào trục", r"Lực hướng tâm không phải một lực mới mà là tên một vai của lực đã có.")],
       ke=[(r"Tìm lực nằm ngang duy nhất còn lại sau khi $\vec P$ và $\vec N$ cân bằng", True),
           (r"Thêm một lực hướng vào trục để vật đi vòng", r"Mọi lực phải do một vật cụ thể tác dụng lên vật; không được vẽ thêm lực cho đủ."),
           (r"Lấy lực li tâm cân bằng với lực kéo vào trục", r"Lực li tâm không do vật nào gây ra; bài này xét trong hệ gắn với mặt đất.")]),
  buoc(r"Độ lớn lực hướng tâm", r"Lực hướng tâm tác dụng lên vật bằng bao nhiêu?", 0.395, r"N", 0.01,
       loi=r"Thế thẳng 60 vòng/phút như $\omega=60\ \text{rad/s}$, hoặc để khối lượng ở đơn vị gam.",
       ke=[(r"Đổi sang đơn vị chuẩn, tính $\omega=2\pi f$ rồi dùng $m\omega^2 r$", True),
           (r"Dùng $m\omega^2 r$ với $\omega=60\ \text{rad/s}$", r"60 là số vòng mỗi phút, chưa phải rad/s; phải đổi ($1$ vòng $=2\pi\ \text{rad}$, $1$ phút $=60\ \text{s}$)."),
           (r"Thế $m=50$ và $r=20$ vào công thức", r"Phải đổi gam sang kg và cm sang m trước khi thế.")]),
  buoc(r"Ô tô qua khúc cua nằm ngang", r"Lực nào đóng vai lực hướng tâm của ô tô chạy đều qua khúc cua nằm ngang?",
       loi=r"Chọn lực kéo của động cơ vì nó “làm xe chạy”.",
       lua_chon=[(r"Lực ma sát nghỉ giữa lốp xe và mặt đường", True),
                 (r"Lực kéo của động cơ", r"Lực kéo của động cơ nằm dọc theo hướng chạy, không chĩa vào tâm khúc cua."),
                 (r"Phản lực của mặt đường", r"Phản lực vuông góc với mặt đường, cân bằng với trọng lực theo phương đứng.")],
       ke=[(r"Tìm lực nằm ngang chĩa vào tâm khúc cua", True),
           (r"Lấy lực làm xe tiến về phía trước", r"Lực đó nằm dọc theo hướng chạy, mà lực hướng tâm vuông góc với hướng chạy."),
           (r"Lấy trọng lực vì nó lớn nhất", r"Trọng lực thẳng đứng, không chĩa vào tâm khúc cua.")]),
  buoc(r"Vệ tinh quanh Trái Đất", r"Lực nào đóng vai lực hướng tâm của vệ tinh chuyển động tròn đều quanh Trái Đất?",
       loi=r"Cho rằng cần lực đẩy của động cơ, hoặc “lực li tâm” cân bằng với hấp dẫn.",
       lua_chon=[(r"Lực hấp dẫn của Trái Đất tác dụng lên vệ tinh", True),
                 (r"Lực đẩy của động cơ vệ tinh", r"Vệ tinh bay vòng khi không bật động cơ; lực đẩy không phải lực chĩa vào tâm Trái Đất."),
                 (r"Lực li tâm do vệ tinh sinh ra", r"Không vật nào gây ra lực li tâm lên vệ tinh.")],
       ke=[(r"Tìm lực do một vật cụ thể tác dụng lên vệ tinh và chĩa vào tâm quỹ đạo", True),
           (r"Tìm lực làm vệ tinh tiến về phía trước", r"Vệ tinh đi vòng đều nên không cần lực dọc theo hướng chuyển động; lực hướng tâm vuông góc với hướng đó."),
           (r"Coi vệ tinh chỉ chuyển động theo quán tính", r"Chỉ có quán tính thì vệ tinh bay thẳng; muốn đi vòng phải có lực chĩa vào tâm.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>không trượt</b> hay <b>giá trị giới hạn</b> → so lực hướng tâm với <b>ma sát nghỉ cực đại</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Lực hướng tâm cần có", r"Lực hướng tâm cần có để xe qua đường vòng bán kính $50\ \text{m}$ bằng bao nhiêu?", 900, r"N", 5,
       loi=r"Thế thẳng $54$ vào công thức mà chưa đổi km/h sang m/s."),
  buoc(r"So với lực ma sát nghỉ cực đại", r"Chọn kết luận đúng về việc xe có trượt hay không ở bán kính $50\ \text{m}$.",
       loi=r"So lực hướng tâm với trọng lượng, hoặc so với một giá trị ma sát tuỳ ý.",
       lua_chon=[(r"Không trượt trên đường khô, trượt trên đường ướt", True),
                 (r"Không trượt ở cả hai loại đường, vì lực hướng tâm nhỏ hơn trọng lượng", r"Giới hạn của lực hướng tâm là lực ma sát nghỉ cực đại, không phải trọng lượng; cần so với $F_{\text{max}}$ của từng loại đường."),
                 (r"Trượt trên đường khô, không trượt trên đường ướt, vì đường khô có ma sát lớn hơn nên xe dễ lao ra", r"Ma sát nghỉ cực đại càng nhỏ thì xe càng dễ trượt, nên đường ướt trượt trước đường khô."),
                 (r"Trượt ở cả hai loại đường, vì ma sát nghỉ luôn nhỏ hơn lực hướng tâm", r"Ma sát nghỉ tự điều chỉnh đến giá trị cần thiết miễn là không vượt $F_{\text{max}}$; phải so với $F_{\text{max}}$.")],
       ke=[(r"So lực hướng tâm cần có với lực ma sát nghỉ cực đại của từng loại đường", True),
           (r"So lực hướng tâm với trọng lượng của xe", r"Trọng lượng thẳng đứng, không phải lực chĩa vào tâm; giới hạn là ma sát nghỉ cực đại."),
           (r"So tốc độ $54\ \text{km/h}$ với bán kính $50\ \text{m}$", r"Hai đại lượng khác loại nên không so trực tiếp được; phải so hai lực cùng loại.")]),
  buoc(r"Bán kính nhỏ nhất, đường khô", r"Bán kính cong nhỏ nhất để xe không trượt trên đường khô là bao nhiêu?", 37.5, r"m", 0.5,
       loi=r"Dùng $r=v^2/g$ như thể gia tốc hướng tâm bằng $g$, hoặc giữ $r=50\ \text{m}$.",
       ke=[(r"Cho lực hướng tâm bằng lực ma sát nghỉ cực đại rồi rút $r$", True),
           (r"Dùng $r=v^2/g$", r"Gia tốc hướng tâm tối đa của xe là $F_{\text{max}}/m$, không phải $g$."),
           (r"Giữ $r=50\ \text{m}$ vì đề đã cho", r"$50\ \text{m}$ chỉ là bán kính ở ý a; ý b hỏi bán kính nhỏ nhất để không trượt.")]),
  buoc(r"Bán kính nhỏ nhất, đường ướt", r"Bán kính cong nhỏ nhất để xe không trượt trên đường ướt là bao nhiêu?", 75, r"m", 1,
       loi=r"Dùng nhầm lực ma sát cực đại của đường khô.",
       ke=[(r"Thế $F_{\text{max}}$ của đường ướt vào công thức cũ", True),
           (r"Lấy $r_{\text{min}}$ của đường khô nhân $0{,}30$", r"Ma sát nhỏ hơn thì bán kính tối thiểu phải lớn hơn, không nhỏ hơn."),
           (r"Lấy $r_{\text{min}}$ của đường khô chia $0{,}30$", r"Tỉ số giữa hai loại đường là $0{,}30/0{,}60$, không phải $0{,}30$; cần thế thẳng $F_{\text{max}}$ mới.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập (idx 0-based trong old/77.json), xếp dễ → khó ═════════════
# idx0: Mặt Trăng · idx1: xe đua trên đường tròn
ORDER = [1, 0]
MUC = {1: "Trung bình", 0: "Khó"}
for _i, _key in ((0, "Mặt trăng"), (1, "xe đua")):
    assert _key.lower() in OLD[_i]["body_html"].lower()

def _sub(i, a, c):
    assert a in OLD[i]["body_html"], (i, a)
    OLD[i]["body_html"] = OLD[i]["body_html"].replace(a, c)
_sub(1, r"\approx 0{,}22$ rad/s. Gia tốc hướng tâm của xe $a_{ht} = \omega^2.R = 0{,}22^2.80 \approx 3{,}92$",
        r"\approx 0{,}22124$ rad/s. Gia tốc hướng tâm của xe $a_{ht} = \omega^2.R = 0{,}22124^2.80 \approx 3{,}92$")
for _i in (0, 1):
    _h = OLD[_i]["body_html"]
    _h = re.sub(r'alt="[^"]*"', 'alt=""', _h).replace("m/$s^2$", r"$\\text{m/s}^2$")
    OLD[_i]["body_html"] = _h
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)

write(J, 77, "Bài 32. Lực hướng tâm và gia tốc hướng tâm", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
